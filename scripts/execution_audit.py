#!/usr/bin/env python3
"""Execution / drift detector — Bot Fleet v2, Phase 3.

WHAT THIS IS
------------
A DETECTOR, not a judge. It reads the post-cutover working ledger and emits
mechanical fingerprints of things that should be impossible or should not have
happened. It never assigns a cause, never scores a strategy, and never says a
bot should be changed. Cause attribution stays a human/Claude layer working from
the position's **Trades list**; the Exit Options panel is never evidence.

Every finding therefore carries a `verify_by` field naming the artifact that
closes it. A finding is a question with an address, not a verdict.

THREE VERDICTS, NEVER BLENDED  (daily-review-design §1)
------------------------------------------------------
Each rule declares which axis it speaks to:
    FIRE       did it enter / act at all, when it should have?
    MECHANICS  did every declared exit actually generate an order?
    STRATEGY   given it ran correctly, was the bet good?
**No rule in this file is on the STRATEGY axis.** Strategy is the counterfactual
engine's job. Mixing them is what let a bot score 100% compliance for five days
while its profit target had been dead for a month.

TWO TIERS
---------
Tier S — STRUCTURAL. Config-free. Always runs. These test the data against
         arithmetic and against the position's own recorded price path, so they
         cannot be wrong about what a bot was *supposed* to do, because they
         never ask.
Tier C — DECLARED-CONFIG. Needs `data/bots_config_v2.csv` (Phase 4). When that
         file is absent every Tier C rule reports **SKIPPED with a reason** and
         the run is marked `reduced`. It never silently passes. A detector that
         quietly answers "no findings" when it is structurally blind is worse
         than no detector.

THE IMPOSSIBLE-FILL RULE IS LOSS-SIDE ONLY:  `pnl < -risk`.
A loss larger than max loss is structurally impossible for a defined-risk
spread. A GAIN larger than the recorded risk is not — a debit spread can return
more than its debit, and a high-credit condor can return more than its recorded
risk. Flagging on `|pnl| > risk` produces false positives on legal wins.

UNIT NOTE — this is the one place the LEG is the correct unit, and it does not
contradict CLAUDE.md §4. §4 fixes the POSITION (condor) as the unit of
*account* for expectancy. The impossible-fill rule is a *structural integrity*
check on a single vertical spread's own max-loss guarantee, which is a per-spread
property. Netted to the condor, T00147 reads R −1.44 (still impossible) but
T00845 reads R −0.99 (invisible). Run it per row.

Usage
-----
  python3 scripts/execution_audit.py                      # audit the working ledger
  python3 scripts/execution_audit.py --since 2026-08-15
  python3 scripts/execution_audit.py --validate           # the validation matrix
  python3 scripts/execution_audit.py --ledger data/archive/trades.csv --no-write
"""
import argparse, csv, hashlib, json, os, sys, collections

# ---------------------------------------------------------------------------
# FROZEN 2026-07-30. The independent audit runs against THIS version only.
# Bump the version and re-run --validate before any behaviour change ships; the
# self-hash below makes an unversioned edit detectable rather than arguable.
# 1.1.0 2026-08-08 — GATE-A9 SPLIT (i), LOADER ONLY (queued task, session-log
# 2026-08-08): load_config() skips '#' comment lines, keys on 'bot' (v1
# contract) or 'name' (v2 capture file), respects object_kind, and gains a
# schema-unrecognized branch alongside the file-absent branch — every Tier-C
# rule whose columns are missing reports SKIPPED BY NAME, loudly; never
# silence, never a crash. DETECTOR RULES UNTOUCHED. Acceptance: the frozen
# 35-row fixture + the validation matrix pass UNCHANGED (V1..V19, 21/21).
# Split (ii) — the Tier-C contract reconciliation — remains open and separate.
VERSION = "1.1.0"
FROZEN_ON = "2026-07-30"
# ---------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")


def self_hash():
    """sha256 of this file, with the stored hash line itself excluded so the
    value is stable. A detector that cannot prove which version produced a
    finding is not frozen, it is merely old."""
    with open(os.path.abspath(__file__), "rb") as fo:
        return hashlib.sha256(fo.read()).hexdigest()[:16]

# --- tunables, all stated out loud in the report so findings stay auditable ---
FILL_GAP_MIN_PRICE   = 0.50   # $/contract of fill beyond the worst observed mark
FILL_GAP_MIN_CREDITS = 0.25   # ...and as a fraction of credit, so both must agree
FLIP_WINDOW          = 10     # positions in the trailing window
FLIP_BASELINE_MIN    = 10     # positions required before it
FLIP_DELTA           = 0.40   # expired-share jump that trips the flip
FLIP_BASELINE_MAX    = 0.25   # ...and the baseline must have been LOW. The signature
                              # is "closes -> expires", not "expires somewhat more".
                              # A ride/unstopped control that already expires half its
                              # positions has no exit engine to lose.
DUP_MIN_DAYS         = 5      # identical (minute, pnl) days before two arms are "duplicate"
PT_BAND              = 0.10   # captured-fraction band ABOVE target that still reads as a PT fill.
                              # Narrowed 0.15 -> 0.10 on 2026-07-30: at 0.15 the band admitted
                              # 21 champion legs that captured 35-40% of credit, which the
                              # forensic deliberately excluded. Too-wide cuts BOTH ways — it
                              # hides a dead PT (PT_NEVER_FIRES cannot trip) and invents a live
                              # one (REMOVED_EXIT_FIRED false-positives on the control clones).
TICK                 = 0.05   # option price grid; a PT can fill one tick short of target
TICK_SLACK_MAX       = 0.05   # CAP on the tick-slack term, in credits. Without it the slack is
                              # TICK/credit, which is UNBOUNDED: at credit 0.10 it is 0.50
                              # credits, so the band becomes [-0.25, 0.40] and essentially any
                              # profitable close reads as a PT fill. Dime credits are routine on
                              # the QQQ bots. Latent bug, capped 2026-07-30.
PT_NEVER_MIN_N       = 20     # positions before "PT never fired" is a finding rather than noise
RISK_TOL_ABS         = 1.00   # $ tolerance on the derived-risk cross-check...
RISK_TOL_REL         = 0.005  # ...or this fraction of OA's risk, whichever is larger

DEBIT_STRUCTURES = {"longcallspread", "longputspread"}
CREDIT_STRUCTURES = {"shortcallspread", "shortputspread", "ironcondor", "ironbutterfly"}

FCOLS = ["window_start", "window_end", "date", "bot", "trade_id", "rule",
         "severity", "axis", "tier", "observed", "threshold", "detail", "verify_by"]


def fl(x, default=None):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


# ---------------------------------------------------------------------------
# derived quantities
# ---------------------------------------------------------------------------
def captured_final(r):
    """Fraction of premium captured at exit, on the same scale as OA's
    highReturnPct / lowReturnPct. Credit: 1 - exit/credit. Debit: exit/credit - 1.
    Verified against DIR-SPX-CallVIXdrop T00038, where it reproduces
    highReturnPct 1.027 exactly."""
    c = fl(r.get("credit"))
    x = fl(r.get("exit_price"))
    if not c or c <= 0 or x is None:
        return None
    return (x / c - 1) if r["structure"] in DEBIT_STRUCTURES else (1 - x / c)


def worst_mark_price(r):
    """The option price implied by the worst recorded mark (MAE)."""
    c = fl(r.get("credit"))
    mae = fl(r.get("mae_pct"))
    if not c or c <= 0 or mae is None:
        return None
    return c * (1 + mae) if r["structure"] in DEBIT_STRUCTURES else c * (1 - mae)


def is_pt_consistent(r, pt):
    """Did this close look like a profit target firing at `pt` (fraction of
    premium)? Must be a real close (not an expiry), must have reached at least
    the target less one tick, and must not be far beyond it — a ride to
    worthless captures 1.00 and is NOT a PT fill."""
    if r.get("status") != "closed":
        return False
    cap = captured_final(r)
    c = fl(r.get("credit")) or 0
    if cap is None or c <= 0:
        return False
    tick_frac = min(TICK / c, TICK_SLACK_MAX)   # see TICK_SLACK_MAX — unbounded otherwise
    return (pt - tick_frac) <= cap <= (pt + PT_BAND)


def derived_risk(r):
    """SECOND WITNESS for the risk column — computed from the leg strikes, with
    no reference to OA's `risk` field.

    Credit structures: max loss = (widest side's width - credit) x 100 x qty.
    Debit structures:  max loss = the debit paid = premium x 100 x qty. A long
                       spread cannot lose more than it cost; width is irrelevant.

    The structure branch is not a refinement, it is the whole thing: under a
    credit-only formula all 13 debit rows in the v1 archive miss by 30-160%.
    With it, all 1,380 rows agree with OA to within $1 / 0.5%.

    Returns (value, branch) or (None, reason)."""
    q = fl(r.get("quantity")) or 1
    c = fl(r.get("credit"))
    if c is None:
        return (None, "no-premium")
    if r.get("structure") in DEBIT_STRUCTURES:
        return (c * 100 * q, "debit")
    sp, lp = fl(r.get("short_put")), fl(r.get("long_put"))
    sc, lc = fl(r.get("short_call")), fl(r.get("long_call"))
    widths = []
    if sp and lp: widths.append(abs(sp - lp))
    if sc and lc: widths.append(abs(sc - lc))
    if not widths:
        return (None, "no-parseable-strikes")
    # Condor risk is the LARGER side — the two sides cannot both lose.
    return ((max(widths) - c) * 100 * q, "credit")


# ---------------------------------------------------------------------------
# rules
# ---------------------------------------------------------------------------
def rule_S1_impossible_fill(rows, add):
    """A defined-risk spread cannot lose more than its own max loss."""
    for r in rows:
        pnl, risk = fl(r.get("pnl")), fl(r.get("risk"))
        if pnl is None or risk is None or risk <= 0:
            continue
        if pnl < -risk:
            add(r, "IMPOSSIBLE_FILL", "RED", "MECHANICS", "S",
                observed=f"R={pnl/risk:+.4f}",
                threshold="R >= -1.0000",
                detail=(f"pnl {pnl:,.0f} on risk {risk:,.0f} — a loss larger than "
                        f"max loss is structurally impossible for this spread"),
                verify_by="the position's Trades list + Trade Details (exit order type and fill)")


def rule_S2_risk_integrity(rows, add):
    """R is uncomputable without a positive risk. Never divide silently.

    Two failure modes, and the second is the dangerous one:
      MISSING  risk blank or <= 0. Loud, obvious, already handled.
      WRONG    risk present and plausible but incorrect. Silent — and a risk that
               is too HIGH masks IMPOSSIBLE_FILL entirely, because pnl < -risk
               stops being true. Every R-based comparison also quietly shifts.
    The derived cross-check is what converts blank/zero coverage into wrong-value
    coverage, and is the reason IMPOSSIBLE_FILL is no longer a single-source claim."""
    for r in rows:
        risk = fl(r.get("risk"))
        if risk is None or risk <= 0:
            add(r, "RISK_INTEGRITY", "RED", "MECHANICS", "S",
                observed=f"risk={r.get('risk')!r}",
                threshold="risk > 0",
                detail="R cannot be computed; this position is excluded from every "
                       "R-based comparison until the export is corrected",
                verify_by="the OA Export Data row for this position")
            continue
        d, branch = derived_risk(r)
        if d is None:
            add(r, "RISK_UNWITNESSED", "AMBER", "MECHANICS", "S",
                observed=branch, threshold="strikes parseable from `description`",
                detail="OA's risk cannot be independently corroborated for this row, so "
                       "IMPOSSIBLE_FILL rests on a single source here. Not a failure — a "
                       "gap in the witness.",
                verify_by="the OA Export Data `description` for this position")
            continue
        if abs(d - risk) > max(RISK_TOL_ABS, RISK_TOL_REL * risk):
            add(r, "RISK_MISMATCH", "RED", "MECHANICS", "S",
                observed=f"OA risk {risk:,.0f} vs derived {d:,.0f} "
                         f"({(d - risk) / risk:+.1%}, {branch} branch)",
                threshold=f"within ${RISK_TOL_ABS:.0f} or {RISK_TOL_REL:.1%}",
                detail="the risk column disagrees with the max loss implied by the leg "
                       "strikes. Every R on this bot is suspect, and a risk that is too "
                       "HIGH would silently hide an impossible fill.",
                verify_by="the position's strikes in the Trades list vs the export's "
                          "`risk` and `description` columns")


def rule_S3_fill_worse_than_mae(rows, add):
    """The exit filled outside the position's own recorded price path. Needs no
    config at all: the position's worst observed mark is its own witness.
    Caveat: OA's MFE/MAE are MARK-based and stop updating when marks stop (e.g.
    a subscription lapse), so a stale mark can create a false positive on a
    long-dated position. Both thresholds must trip, which suppresses that."""
    for r in rows:
        if r.get("status") != "closed":
            continue
        cap, worst, c = captured_final(r), worst_mark_price(r), fl(r.get("credit"))
        x = fl(r.get("exit_price"))
        if cap is None or worst is None or x is None or not c or c <= 0:
            continue
        gap_px = (worst - x) if r["structure"] in DEBIT_STRUCTURES else (x - worst)
        gap_cr = gap_px / c
        if gap_px >= FILL_GAP_MIN_PRICE and gap_cr >= FILL_GAP_MIN_CREDITS:
            add(r, "FILL_WORSE_THAN_MAE", "RED", "MECHANICS", "S",
                observed=f"${gap_px:.2f}/contract ({gap_cr:.2f} credits)",
                threshold=f"${FILL_GAP_MIN_PRICE:.2f} and {FILL_GAP_MIN_CREDITS:.2f} credits",
                detail=(f"exit {x:g} vs worst recorded mark {worst:.2f} — the fill is "
                        f"outside the price path the position ever traded at"),
                verify_by="the Trades list: exit ORDER TYPE (Market vs SmartPricing) and fill time")


def rule_S4_never_in_profit(rows, add):
    for r in rows:
        pnl, mfe = fl(r.get("pnl")), fl(r.get("mfe_pct"))
        if pnl is None or mfe is None:
            continue
        if pnl < 0 and mfe <= 0.0:
            add(r, "NEVER_IN_PROFIT", "INFO", "FIRE", "S",
                observed=f"mfe={mfe:+.4f}",
                threshold="mfe > 0",
                detail="the position was never in profit for a single recorded mark — "
                       "an entry-side question, not an exit-side one",
                verify_by="entry timestamp vs the tape; the C1 regime inputs for that morning")


def rule_S5_closed_at_mae(rows, add):
    for r in rows:
        pnl = fl(r.get("pnl"))
        if pnl is None or pnl >= 0:
            continue
        md, cd = (r.get("mae_date") or "")[:16], (r.get("close_date") or "")[:16]
        if md and cd and md == cd:
            add(r, "CLOSED_AT_MAE", "INFO", "MECHANICS", "S",
                observed=f"mae_date == close_date ({cd})",
                threshold="close should not coincide with the worst mark",
                detail="the exit fired at the worst point of the position's life — "
                       "expected for a stop, a finding for anything else",
                verify_by="the Trades list: which mechanic generated the closing order")


def rule_S6_expiry_ratio_flip(rows, add_bot):
    """A bot whose positions start EXPIRING instead of CLOSING is a mechanic
    that stopped firing. One-line check, the whole Fortress regression."""
    by_bot = collections.defaultdict(list)
    for r in rows:
        by_bot[r["bot"]].append(r)
    for bot, rs in sorted(by_bot.items()):
        rs = sorted(rs, key=lambda r: r.get("open_date", ""))
        need = FLIP_WINDOW + FLIP_BASELINE_MIN
        if len(rs) < need:
            add_bot(bot, "EXPIRY_RATIO_FLIP", "SKIPPED", "MECHANICS", "S",
                    observed=f"n={len(rs)}", threshold=f"n >= {need}",
                    detail="too few positions to evaluate a flip — NOT a pass",
                    verify_by="", date="")
            continue
        for i in range(need - 1, len(rs)):
            recent = rs[i - FLIP_WINDOW + 1: i + 1]
            baseline = rs[: i - FLIP_WINDOW + 1]
            rec = sum(1 for r in recent if r.get("status") == "expired") / len(recent)
            base = sum(1 for r in baseline if r.get("status") == "expired") / len(baseline)
            if rec - base >= FLIP_DELTA and base <= FLIP_BASELINE_MAX:
                # The actionable date is the FIRST position that expired inside the
                # onset window, not the window's own start — that is the position
                # whose Trades list either has an exit order or does not.
                first_exp = next((r for r in recent if r.get("status") == "expired"), None)
                onset = (first_exp or recent[0])["open_date"][:10]
                onset_tid = (first_exp or recent[0]).get("trade_id", "")
                add_bot(bot, "EXPIRY_RATIO_FLIP", "RED", "MECHANICS", "S",
                        observed=f"{rec:.0%} expired over the last {FLIP_WINDOW} "
                                 f"vs {base:.0%} over the prior {len(baseline)}",
                        threshold=f"jump >= {FLIP_DELTA:.0%} from a baseline "
                                  f"<= {FLIP_BASELINE_MAX:.0%}",
                        detail=(f"first expiry of the onset window: {onset} ({onset_tid}); "
                                f"tripped on the position opened {rs[i]['open_date'][:10]}. "
                                f"Positions stopped CLOSING and started EXPIRING — the "
                                f"signature of an exit that no longer generates orders"),
                        verify_by=f"the Trades list of {onset_tid} ({onset}): is there an "
                                  f"exit order at all?",
                        date=onset)
                break


def rule_S7_duplicate_arm(rows, add_bot):
    """Two arms with identical P/L at an identical entry minute are one arm.
    This is how HedgeA-S1 == HedgeD would have surfaced on day one."""
    key = collections.defaultdict(set)
    for r in rows:
        k = ((r.get("open_date") or "")[:16], r.get("pnl"), r.get("structure"))
        if k[0]:
            key[k].add(r["bot"])
    pairs = collections.Counter()
    for bots in key.values():
        s = sorted(bots)
        for i in range(len(s)):
            for j in range(i + 1, len(s)):
                pairs[(s[i], s[j])] += 1
    for (a, b), n in sorted(pairs.items(), key=lambda kv: (-kv[1], kv[0])):
        if n >= DUP_MIN_DAYS:
            add_bot(a, "DUPLICATE_ARM", "AMBER", "FIRE", "S",
                    observed=f"{n} positions identical to {b}",
                    threshold=f"< {DUP_MIN_DAYS}",
                    detail=f"'{a}' and '{b}' produced identical P/L at an identical "
                           f"entry minute {n} times — they are not independent arms "
                           f"and cannot be ranked against each other",
                    verify_by="a capture-diff of the two bots' automation trees",
                    date="")


def rule_S8_silent_bot(rows, meta, add_bot):
    """A bot switched ON that produced nothing. NEVER red from position data
    alone — a correctly-gated bot and a switched-off bot look identical from
    here. DIR-SPX-PutVIX22-SL75 is the standing proof: 0 positions in 22 days
    because its VIX>=22 gate correctly never fired."""
    if not rows:
        # No positions at all means no trading day to have been silent on.
        # Reporting 20 silent bots on an empty window is noise, and the whole
        # point of the AMBER budget is that it stays believable.
        add_bot("(fleet)", "SILENT_BOT", "SKIPPED", "FIRE", "S",
                observed="empty window", threshold="at least 1 position in the window",
                detail="no trading activity in the window — liveness is not evaluable "
                       "from position data. NOT a pass.",
                verify_by="OA bot logs for the window", date="")
        return
    traded = {r["bot"] for r in rows}
    for bot, m in sorted(meta.items()):
        if (m.get("status") or "").upper() != "ON":
            continue
        if bot not in traded:
            add_bot(bot, "SILENT_BOT", "AMBER", "FIRE", "S",
                    observed="0 positions in the window",
                    threshold="1 position, or a scanner run in the logs",
                    detail="correctly-gated and switched-off are indistinguishable from "
                           "position data — this is unverifiable here, not a failure",
                    verify_by="OA bot logs: a scanner run recorded with no entry closes "
                              "this GREEN; zero log entries closes it RED",
                    date="")


# ---------------------------------------------------------------------------
# THE THREE-STATE CELL
# ---------------------------------------------------------------------------
# Every declared-mechanic cell in bots_config_v2.csv has THREE distinct states,
# never two. Collapsing "none" into "blank" is not a cosmetic loss: three of the
# bots that will be live on Day-0 have mechanics REMOVED BY DESIGN — the two
# control clones (PT25 deleted from the Open Position action, not toggled off)
# and QQQ-IC-0DTE-Fortress-NoPT50. Read as blank they become permanent blind
# spots; read as a declared value they false-alarm every single day.
#
#   "0.25" / "15:50"   DECLARED       -> the rule evaluates normally
#   "none"             REMOVED BY     -> the forward rule must NOT fire, and the
#                      DESIGN            INVERSE rule turns on: if the mechanic
#                                        is observed firing anyway, that is RED
#   ""  (blank)        MISSING DATA   -> the rule is SKIPPED and reported as a
#                                        blind spot. BLANK IS NOT NONE.
#   bot absent         MISSING DATA   -> every Tier C rule SKIPPED for that bot
#
# Anything else is rejected loudly rather than coerced — a typo must not silently
# become a threshold.
NONE_TOKENS = {"none", "removed", "n/a", "na"}


def cell(cfg, bot, field):
    """-> ('value', parsed) | ('none', None) | ('missing', None) | ('bad', raw)"""
    row = cfg.get(bot)
    if row is None:
        return ("missing", None)
    raw = (row.get(field) or "").strip()
    if raw == "":
        return ("missing", None)
    if raw.lower() in NONE_TOKENS:
        return ("none", None)
    if field == "pt_pct" or field == "sl_pct":
        v = fl(raw)
        return ("value", v) if v is not None and 0 < v <= 5 else ("bad", raw)
    if field in ("time_exit", "event_backstop"):
        if len(raw) == 5 and raw[2] == ":" and raw[:2].isdigit() and raw[3:].isdigit():
            return ("value", raw)
        return ("bad", raw)
    return ("value", raw)


def _tierC_cell_guard(bot, field, state, raw, add_bot, rule):
    """Emit the SKIPPED / bad-value row for a non-evaluable cell. Returns True if
    the caller should stop. A blind spot is announced, never inferred."""
    if state == "missing":
        add_bot(bot, rule, "SKIPPED", "MECHANICS", "C",
                observed=f"{field} is blank or the bot is absent from the config",
                threshold=f"a value, or the literal 'none' if it was removed by design",
                detail="blank means MISSING DATA, not 'no such mechanic'. This bot is "
                       "unaudited on this rule — NOT a pass. If the mechanic really was "
                       "removed, write 'none' so the inverse check turns on.",
                verify_by="the bot's capture: is the mechanic present in the Open "
                          "Position action?", date="")
        return True
    if state == "bad":
        add_bot(bot, rule, "RED", "MECHANICS", "C",
                observed=f"{field} = {raw!r}", threshold="a number, HH:MM, or 'none'",
                detail="unparseable config cell — refusing to coerce it into a "
                       "threshold. A typo must not silently become a rule.",
                verify_by="data/bots_config_v2.csv", date="")
        return True
    return False


def rule_C1_pt_not_taken(rows, cfg, add, add_bot):
    """The declared profit target was reached and no PT-consistent close
    happened. This is the champion's PT25 death signature."""
    bots = sorted({r["bot"] for r in rows})
    for bot in bots:
        state, pt = cell(cfg, bot, "pt_pct")
        if _tierC_cell_guard(bot, "pt_pct", state,
                             (cfg.get(bot) or {}).get("pt_pct"),
                             add_bot, "PT_DECLARED_NOT_TAKEN"):
            continue
        if state == "none":
            continue  # nothing to miss; the inverse rule C4 covers this bot
        for r in (x for x in rows if x["bot"] == bot):
            mfe = fl(r.get("mfe_pct"))
            if mfe is None or mfe < pt or is_pt_consistent(r, pt):
                continue
            add(r, "PT_DECLARED_NOT_TAKEN", "RED", "MECHANICS", "C",
                observed=f"mfe={mfe:.3f}, captured={captured_final(r)}",
                threshold=f"pt={pt:.3f}",
                detail=f"the declared PT of {pt:.0%} was reached at {r.get('mfe_date')} "
                       f"and the position did not close consistent with it",
                verify_by="the Trades list: is there a PT row attached to this position at all?")


def rule_C2_pt_never_fires(rows, cfg, add_bot):
    by_bot = collections.defaultdict(list)
    for r in rows:
        by_bot[r["bot"]].append(r)
    for bot, rs in sorted(by_bot.items()):
        state, pt = cell(cfg, bot, "pt_pct")
        if state in ("missing", "bad"):
            continue  # already reported once by C1's guard; do not double-count
        if state == "none":
            continue
        if len(rs) < PT_NEVER_MIN_N:
            add_bot(bot, "PT_NEVER_FIRES", "SKIPPED", "MECHANICS", "C",
                    observed=f"n={len(rs)}", threshold=f"n >= {PT_NEVER_MIN_N}",
                    detail="too few positions to call a dead PT — NOT a pass",
                    verify_by="", date="")
            continue
        fired = sum(1 for r in rs if is_pt_consistent(r, pt))
        reached = sum(1 for r in rs if (fl(r.get("mfe_pct")) or -9) >= pt)
        if fired == 0 and reached > 0:
            add_bot(bot, "PT_NEVER_FIRES", "RED", "MECHANICS", "C",
                    observed=f"0 PT-consistent closes in {len(rs)} positions, "
                             f"{reached} of which reached the target",
                    threshold="at least 1",
                    detail=f"declared PT {pt:.0%} generated no orders — the exit engine "
                           f"is dead on this bot, or the PT is not attached",
                    verify_by="the Trades list of the most recent position that reached "
                              "the target", date="")


def rule_C3_time_exit_missed(rows, cfg, add, add_bot):
    bots = sorted({r["bot"] for r in rows})
    for bot in bots:
        state, te = cell(cfg, bot, "time_exit")
        if _tierC_cell_guard(bot, "time_exit", state,
                             (cfg.get(bot) or {}).get("time_exit"),
                             add_bot, "TIME_EXIT_MISSED"):
            continue
        if state == "none":
            continue
        for r in (x for x in rows if x["bot"] == bot):
            if r.get("status") == "expired":
                add(r, "TIME_EXIT_MISSED", "RED", "MECHANICS", "C",
                    observed="expired", threshold=f"closed by {te}",
                    detail=f"a time exit at {te} is declared and the position expired instead",
                    verify_by="the Trades list: is a time-exit row attached?")
                continue
            ct = (r.get("close_date") or "")[11:16]
            if ct and ct > te:
                add(r, "TIME_EXIT_MISSED", "RED", "MECHANICS", "C",
                    observed=f"closed {ct}", threshold=f"<= {te}",
                    detail=f"closed after the declared time exit of {te}",
                    verify_by="the Trades list: exit order timestamp vs the declared time")


def rule_C4_removed_exit_fired(rows, cfg, add_bot):
    """THE INVERSE CHECK — only reachable because 'none' is distinct from blank.

    A mechanic declared REMOVED is firing anyway. On the two control clones this
    is the whole verification: their Day-0 proof is that their Trades lists show
    NO PT row. If PT-consistent closes start appearing on a bot whose PT was
    deleted from the Open Position action, either the deletion did not take or
    something else is closing positions at that price — and the bot has silently
    stopped being the ride benchmark the tournament is measured against."""
    by_bot = collections.defaultdict(list)
    for r in rows:
        by_bot[r["bot"]].append(r)
    for bot, rs in sorted(by_bot.items()):
        state, _ = cell(cfg, bot, "pt_pct")
        if state != "none":
            continue
        # No declared target to test against, so probe the standard rungs.
        for probe in (0.25, 0.50, 0.75):
            hits = [r for r in rs if is_pt_consistent(r, probe)]
            if len(hits) >= 3:
                add_bot(bot, "REMOVED_EXIT_FIRED", "RED", "MECHANICS", "C",
                        observed=f"{len(hits)} closes consistent with PT{probe:.0%} "
                                 f"in {len(rs)} positions",
                        threshold="0 — the PT is declared REMOVED BY DESIGN",
                        detail=f"pt_pct is 'none' for this bot, but {len(hits)} positions "
                               f"closed in the PT{probe:.0%} band. Either the removal did "
                               f"not take, or something else is closing at that price. "
                               f"This bot is no longer the ride benchmark it is being "
                               f"compared as.",
                        verify_by="the Trades list of the most recent such position: is "
                                  "there a PT row attached?",
                        date=max(r["open_date"][:10] for r in hits))
                break


def rule_C5_backstop_caught_it(rows, cfg, add):
    """THE $9,618 RULE, and the reason event_backstop needs its own column.

    `time_exit` is the Exit-Options-side time exit. `event_backstop` is the
    AUTOMATIONS-side Scheduled Event flat-close. They are DIFFERENT EXECUTION
    CLASSES and one column cannot hold both — that separation is the entire
    point of the design (one toggle kills every Exit Option at once; the
    backstop survives it).

    A position that closes at the backstop time rather than the time exit means
    the Exit Options side did not fire and the backstop caught it. Nothing is
    lost that day, which is exactly why it would otherwise go unnoticed — and it
    is the same silent failure that ran for six sessions on the Fortress pair."""
    bots = sorted({r["bot"] for r in rows})
    for bot in bots:
        te_state, te = cell(cfg, bot, "time_exit")
        bs_state, bs = cell(cfg, bot, "event_backstop")
        if te_state != "value" or bs_state != "value" or bs <= te:
            continue
        for r in (x for x in rows if x["bot"] == bot):
            ct = (r.get("close_date") or "")[11:16]
            if ct and te < ct <= bs:
                add(r, "BACKSTOP_CAUGHT_IT", "RED", "MECHANICS", "C",
                    observed=f"closed {ct}", threshold=f"time exit {te}",
                    detail=f"closed in the window between the Exit-Options time exit "
                           f"({te}) and the AUTOMATIONS backstop ({bs}). The backstop "
                           f"did the work. No money was lost today, which is exactly why "
                           f"this is easy to miss — the Exit Options side is dead.",
                    verify_by="the Trades list: which mechanic generated the closing "
                              "order, and the bot's EXIT OPTIONS dashboard toggle")


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------
def load_config(path):
    """`data/bots_config_v2.csv` — the DECLARED config, written from capture in
    Phase 4, never by hand and never from memory (CLAUDE.md §3).

    Columns this detector reads (proposed contract; confirm against the Phase 4
    capture before building the file):

        bot             exact OA bot name, the join key
        pt_pct          profit target as a FRACTION OF PREMIUM (0.25 = PT25)
        sl_pct          stop as a fraction of premium (0.75 = SL75)
        time_exit       'HH:MM' — the EXIT-OPTIONS-side time exit
        event_backstop  'HH:MM' — the AUTOMATIONS-side Scheduled Event flat-close.
                        A SEPARATE COLUMN ON PURPOSE: different execution class.
                        One toggle kills every Exit Option at once; the backstop
                        survives it. One column cannot hold both, and the whole
                        value of rule C5 is that the two can disagree.
        capture_file    the capture this row was read from
        capture_hash    its hash — provenance, not decoration

    Every mechanic cell is THREE-STATE: a value / the literal 'none' (removed by
    design) / blank (missing data). See `cell()`. Absent file -> Tier C SKIPPED,
    loudly.

    AMENDED 2026-08-08 (gate A9, split (i)). The file as built in Phase 4 is a
    CAPTURE INVENTORY, not the proposed contract above: a 77-line '#' preamble,
    heterogeneous object rows keyed by `object_kind` (bot / shared_automation),
    identity in `name`, and NONE of the Tier-C mechanic columns. The two were
    never reconciled (split (ii), still open). This loader now: skips '#'
    comment lines; keys on 'bot' if that column exists (the v1 contract, which
    the synthetic validation configs still use), else on 'name' filtered to
    object_kind == 'bot'; and NEVER crashes on an unrecognized schema — it
    returns what is loadable plus the column set, and run() reports every
    Tier-C rule whose columns are absent as SKIPPED BY NAME. 'Structural rules
    run · Tier C SKIPPED until bots_config_v2.csv carries the mechanic columns'
    is an ACCEPTABLE INTERIM STATE (reactivation-runbook.md §3 Step E), and the
    design working as intended — a blind spot on the page, never silence.

    Returns None (file absent) or {"bots": {key: row}, "columns": set,
    "header": [fieldnames]}. Rules still receive the plain bots dict."""
    if not os.path.exists(path):
        return None
    with open(path, newline="") as fh:
        rdr = csv.DictReader(ln for ln in fh if not ln.lstrip().startswith("#"))
        header = [f.strip() for f in (rdr.fieldnames or [])]
        rows = list(rdr)
    if "bot" in header:                     # the v1 declared contract
        bots = {r["bot"]: r for r in rows if (r.get("bot") or "").strip()}
    elif "name" in header:                  # the v2 capture file
        if "object_kind" in header:
            rows = [r for r in rows if (r.get("object_kind") or "").strip() == "bot"]
        bots = {r["name"]: r for r in rows if (r.get("name") or "").strip()}
    else:                                   # schema-unrecognized: degrade, loudly
        bots = {}
    return {"bots": bots, "columns": set(header), "header": header}


# Which declared-config columns each Tier-C rule reads. A rule with a missing
# column is SKIPPED BY NAME — never silently passed, never a crash.
TIERC_RULE_COLUMNS = (
    ("PT_DECLARED_NOT_TAKEN", ("pt_pct",)),
    ("PT_NEVER_FIRES",        ("pt_pct",)),
    ("TIME_EXIT_MISSED",      ("time_exit",)),
    ("REMOVED_EXIT_FIRED",    ("pt_pct",)),
    ("BACKSTOP_CAUGHT_IT",    ("time_exit", "event_backstop")),
)


def run(ledger_path, config_path, meta_path, since=None, until=None):
    if not os.path.exists(ledger_path):
        sys.exit(f"ERROR: no ledger at {ledger_path} — run scripts/build_ledger.py first")
    rows = list(csv.DictReader(open(ledger_path)))
    if since:
        rows = [r for r in rows if (r.get("open_date") or "")[:10] >= since]
    if until:
        rows = [r for r in rows if (r.get("open_date") or "")[:10] <= until]
    meta = ({r["bot"]: r for r in csv.DictReader(open(meta_path))}
            if os.path.exists(meta_path) else {})
    cfg = load_config(config_path)

    dates = sorted((r.get("open_date") or "")[:10] for r in rows if r.get("open_date"))
    w0, w1 = (dates[0], dates[-1]) if dates else ("", "")

    findings = []

    def add(r, rule, sev, axis, tier, observed, threshold, detail, verify_by):
        findings.append({"window_start": w0, "window_end": w1,
                         "date": (r.get("open_date") or "")[:10], "bot": r.get("bot", ""),
                         "trade_id": r.get("trade_id", ""), "rule": rule,
                         "severity": sev, "axis": axis, "tier": tier,
                         "observed": observed, "threshold": threshold,
                         "detail": detail, "verify_by": verify_by})

    def add_bot(bot, rule, sev, axis, tier, observed, threshold, detail, verify_by, date=""):
        findings.append({"window_start": w0, "window_end": w1, "date": date,
                         "bot": bot, "trade_id": "", "rule": rule, "severity": sev,
                         "axis": axis, "tier": tier, "observed": observed,
                         "threshold": threshold, "detail": detail,
                         "verify_by": verify_by})

    # Tier S — always
    rule_S1_impossible_fill(rows, add)
    rule_S2_risk_integrity(rows, add)
    rule_S3_fill_worse_than_mae(rows, add)
    rule_S4_never_in_profit(rows, add)
    rule_S5_closed_at_mae(rows, add)
    rule_S6_expiry_ratio_flip(rows, add_bot)
    rule_S7_duplicate_arm(rows, add_bot)
    rule_S8_silent_bot(rows, meta, add_bot)

    # Tier C — only with a declared config
    tierc_ran = False
    if cfg is None:
        for rule in ("PT_DECLARED_NOT_TAKEN", "PT_NEVER_FIRES", "TIME_EXIT_MISSED",
                     "REMOVED_EXIT_FIRED", "BACKSTOP_CAUGHT_IT"):
            add_bot("(fleet)", rule, "SKIPPED", "MECHANICS", "C",
                    observed="no declared config",
                    threshold=f"{os.path.relpath(config_path, ROOT)} present",
                    detail="Tier C cannot run without the captured declared config. "
                           "This is NOT a pass — the fleet is unaudited on this rule.",
                    verify_by="Phase 4: build data/bots_config_v2.csv from the "
                              "bookmarklet capture")
    else:
        bots, cols, header = cfg["bots"], cfg["columns"], cfg["header"]
        keyed = ("bot" in cols) or ("name" in cols)
        runners = {
            "PT_DECLARED_NOT_TAKEN": lambda: rule_C1_pt_not_taken(rows, bots, add, add_bot),
            "PT_NEVER_FIRES":        lambda: rule_C2_pt_never_fires(rows, bots, add_bot),
            "TIME_EXIT_MISSED":      lambda: rule_C3_time_exit_missed(rows, bots, add, add_bot),
            "REMOVED_EXIT_FIRED":    lambda: rule_C4_removed_exit_fired(rows, bots, add_bot),
            "BACKSTOP_CAUGHT_IT":    lambda: rule_C5_backstop_caught_it(rows, bots, add),
        }
        for rule, need in TIERC_RULE_COLUMNS:
            missing = [c for c in need if c not in cols]
            if not keyed or missing:
                observed = (f"config file present but carries no 'bot'/'name' key column "
                            f"(header read: {header[:6]}{'…' if len(header) > 6 else ''})"
                            if not keyed else
                            f"config file present but column(s) {missing} absent from its schema")
                add_bot("(fleet)", rule, "SKIPPED", "MECHANICS", "C",
                        observed=observed,
                        threshold="declared-contract column(s): " + ", ".join(need),
                        detail="SKIPPED BY NAME (gate A9 split (i)): the declared config's "
                               "schema does not carry what this rule reads. NOT a pass, NOT "
                               "a crash — structural rules still run; this rule resumes when "
                               "bots_config_v2.csv carries the mechanic columns (split (ii)). "
                               "The runbook's own checklist calls this interim state "
                               "acceptable: the blind spot is on the page, never silent.",
                        verify_by="data/bots_config_v2.csv header vs load_config()'s "
                                  "declared contract")
                continue
            runners[rule]()
            tierc_ran = True

    findings.sort(key=lambda f: ({"RED": 0, "AMBER": 1, "INFO": 2, "SKIPPED": 3}[f["severity"]],
                                 f["rule"], f["date"], f["bot"], f["trade_id"]))
    return rows, findings, tierc_ran, (w0, w1)


def report(rows, findings, has_cfg, window, out_path, write=True):
    w0, w1 = window
    by_sev = collections.Counter(f["severity"] for f in findings)
    print("=" * 74)
    print(f"EXECUTION AUDIT v{VERSION} (frozen {FROZEN_ON}, sha {self_hash()})")
    print(f"{len(rows)} position rows, window {w0 or 'n/a'} .. {w1 or 'n/a'}")
    print(f"mode: {'FULL' if has_cfg else 'REDUCED (Tier C SKIPPED — config absent or its schema lacks the mechanic columns; the SKIPPED rows name the reason)'}")
    print("=" * 74)
    if not rows:
        print("\nNO POSITIONS IN WINDOW. Nothing to audit — this is not a pass.")
        print("Expected before the first post-cutover trading day.")
    reds = [f for f in findings if f["severity"] == "RED"]
    ambers = [f for f in findings if f["severity"] == "AMBER"]
    infos = [f for f in findings if f["severity"] == "INFO"]
    skips = [f for f in findings if f["severity"] == "SKIPPED"]
    if not reds and not ambers:
        print("\nNO FINDINGS.   <- the expected common case")
    for label, group in (("RED", reds), ("AMBER", ambers)):
        if not group:
            continue
        print(f"\n--- {label} ({len(group)}) ---")
        for f in group:
            who = f["bot"] + (f" {f['trade_id']}" if f["trade_id"] else "")
            print(f"  [{f['axis']:9}] {f['rule']:24} {f['date'] or '   -      '}  {who}")
            print(f"      observed : {f['observed']}")
            print(f"      threshold: {f['threshold']}")
            print(f"      {f['detail']}")
            if f["verify_by"]:
                print(f"      VERIFY BY: {f['verify_by']}")
    if infos:
        # Context, not findings. Rolled up so a 4-month backfill does not read as
        # 300 alarms — these are hedge-clinic and entry-timing inputs.
        print(f"\n--- CONTEXT ({len(infos)}) — not findings ---")
        for rule, n in collections.Counter(f["rule"] for f in infos).most_common():
            per_bot = collections.Counter(f["bot"] for f in infos if f["rule"] == rule)
            top = "  ".join(f"{b.split('-')[-1] or b}:{c}" for b, c in per_bot.most_common(6))
            print(f"  {rule:22} {n:>4}   {top}")
    if skips:
        print(f"\n--- NOT EVALUATED ({len(skips)}) — blind spots, not passes ---")
        for f in skips:
            print(f"  {f['rule']:24} {f['bot']:38} {f['observed']}")
    print(f"\nsummary: " + "  ".join(f"{k}={v}" for k, v in sorted(by_sev.items())) or "clean")
    if write:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", newline="") as fo:
            w = csv.DictWriter(fo, fieldnames=FCOLS)
            w.writeheader()
            w.writerows(findings)
        meta_path = os.path.splitext(out_path)[0] + "_meta.json"
        with open(meta_path, "w") as fo:
            json.dump({"detector_version": VERSION, "frozen_on": FROZEN_ON,
                       "detector_sha256_16": self_hash(),
                       "mode": "FULL" if has_cfg else "REDUCED",
                       "window_start": w0, "window_end": w1,
                       "n_position_rows": len(rows),
                       "counts": dict(sorted(by_sev.items())),
                       "contract": "findings are evidence with an address, never a "
                                   "verdict; every RED names the artifact that closes it"},
                      fo, indent=2)
            fo.write("\n")
        print(f"-> {os.path.relpath(out_path, ROOT)}")
        print(f"-> {os.path.relpath(meta_path, ROOT)}")


# ---------------------------------------------------------------------------
# validation matrix
# ---------------------------------------------------------------------------
def validate():
    """Run the detector against the FROZEN v1 archive and the frozen 35-row
    fixture, and assert the known ground truth. These are test assets that
    survive the cutover; they are never a reporting input."""
    ledger = os.path.join(D, "archive", "trades.csv")
    fixture = os.path.join(D, "execution_audit.csv")
    results = []

    def check(name, ok, detail=""):
        results.append((ok, name, detail))

    if not os.path.exists(ledger):
        sys.exit(f"ERROR: validation needs the frozen archive ledger at {ledger}")
    rows = list(csv.DictReader(open(ledger)))
    fx = list(csv.DictReader(open(fixture))) if os.path.exists(fixture) else []

    _, findings, has_cfg, _ = run(ledger, os.path.join(D, "bots_config_v2.csv"),
                                  os.path.join(D, "bots_meta.csv"))
    red = {f["rule"]: set() for f in findings}
    for f in findings:
        if f["severity"] == "RED" and f["trade_id"]:
            red.setdefault(f["rule"], set()).add(f["trade_id"])
    imp = red.get("IMPOSSIBLE_FILL", set())

    # V1 — the impossible-fill set is exactly the two known rows
    check("V1  IMPOSSIBLE_FILL == {T00147, T00845}",
          imp == {"T00147", "T00845"}, f"got {sorted(imp)}")

    # V2/V3 — the legal R>1 WINS are not flagged by any RED rule
    all_red = {f["trade_id"] for f in findings if f["severity"] == "RED" and f["trade_id"]}
    check("V2  T00038 (longcallspread, R +1.03) not RED", "T00038" not in all_red)
    check("V3  T00339 (ironcondor,     R +1.78) not RED", "T00339" not in all_red)

    # V4 — the loss-side rule is load-bearing: the abs-value rule would add
    #      exactly those two legal wins and nothing else.
    absrule = set()
    for r in rows:
        p, k = fl(r.get("pnl")), fl(r.get("risk"))
        if p is not None and k and k > 0 and abs(p) > k:
            absrule.add(r["trade_id"])
    check("V4  |pnl|>risk would add exactly {T00038, T00339}",
          absrule - imp == {"T00038", "T00339"}, f"delta {sorted(absrule - imp)}")

    # V5 — fixture integrity: every fixture trade_id resolves in the ledger
    fx_ids = {r["trade_id"] for r in fx}
    led_ids = {r["trade_id"] for r in rows}
    check(f"V5  fixture is 35 rows and every trade_id resolves",
          len(fx) == 35 and fx_ids <= led_ids,
          f"n={len(fx)}, unresolved={sorted(fx_ids - led_ids)}")

    # V6 — nothing the forensic classed `by_design` is called a RED failure.
    #      Intentional behaviour must not read as a malfunction.
    bd = {r["trade_id"] for r in fx if r.get("cause_class") == "by_design"}
    check("V6  no `by_design` fixture row flagged RED",
          not (bd & all_red), f"overlap {sorted(bd & all_red)}")

    # V7 — the detector knows what it cannot see. With no declared config,
    #      every Tier C rule must report SKIPPED rather than silently pass.
    skipped_c = {f["rule"] for f in findings if f["tier"] == "C" and f["severity"] == "SKIPPED"}
    check("V7  Tier C reports SKIPPED (not silent) with no bots_config_v2.csv",
          (not has_cfg) and skipped_c >= {"PT_DECLARED_NOT_TAKEN", "PT_NEVER_FIRES",
                                          "TIME_EXIT_MISSED"},
          f"has_cfg={has_cfg}, skipped={sorted(skipped_c)}")

    # V8 — positive control: the detector catches the two engine deaths it was
    #      built after. Champion PT25 dies 2026-06-01; Fortress pair 2026-06-12.
    flips = {f["bot"]: f["date"] for f in findings if f["rule"] == "EXPIRY_RATIO_FLIP"
             and f["severity"] == "RED"}
    check("V8a EXPIRY_RATIO_FLIP dates IC-SPX-FastPT25-S2 to 2026-06-01 "
          "(PT25 died on the first session back)",
          flips.get("IC-SPX-FastPT25-S2") == "2026-06-01", f"got {flips}")
    check("V8b EXPIRY_RATIO_FLIP dates BOTH Fortress bots to 2026-06-12 "
          "(the known regression)",
          flips.get("QQQ-IC-0DTE-Fortress") == "2026-06-12"
          and flips.get("QQQ-IC-0DTE-Fortress-NoPT50") == "2026-06-12",
          f"got {flips}")
    # V8c — and it does NOT fire on a bot that was always going to expire.
    #       IC-SPX-Fortress-Unstopped went 50% -> 90% expired; that is drift in a
    #       ride control, not an exit engine that died. The baseline gate holds it.
    check("V8c EXPIRY_RATIO_FLIP silent on IC-SPX-Fortress-Unstopped "
          "(already 50% expired — no engine to lose)",
          "IC-SPX-Fortress-Unstopped" not in flips, f"got {sorted(flips)}")

    # V9 — positive control: the invalid tournament. S1 == D on 73 days.
    dups = {(f["bot"], f["observed"]) for f in findings if f["rule"] == "DUPLICATE_ARM"}
    s1d = [o for b, o in dups if b == "QQQ-IC-0DTE-HedgeA-S1"
           and "HedgeD-Conditional" in o]
    check("V9  DUPLICATE_ARM reproduces HedgeA-S1 == HedgeD on 73 positions",
          any("73 " in o for o in s1d), f"got {s1d}")

    # V10 — determinism: two runs, identical findings
    _, f2, _, _ = run(ledger, os.path.join(D, "bots_config_v2.csv"),
                      os.path.join(D, "bots_meta.csv"))
    check("V10 deterministic across runs", f2 == findings)

    # --- V11-V14: the three-state cell, exercised against a SYNTHETIC config --
    # bots_config_v2.csv does not exist yet, so Tier C's semantics are proved
    # here against a temporary file rather than left as an untested claim. The
    # champion is the perfect subject: it really did fire PT25 pre-lapse, so a
    # 'none' declaration on it MUST light up the inverse rule.
    import tempfile
    CHAMP = "IC-SPX-FastPT25-S2"
    def synth(**per_bot):
        fd = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="")
        w = csv.writer(fd)
        w.writerow(["bot", "pt_pct", "sl_pct", "time_exit", "event_backstop",
                    "capture_file", "capture_hash"])
        for b, vals in per_bot.items():
            w.writerow([b] + list(vals) + ["synthetic-validation", "n/a"])
        fd.close()
        _, f, has, _ = run(ledger, fd.name, os.path.join(D, "bots_meta.csv"))
        os.unlink(fd.name)
        return f, has

    def rules_for(f, bot, rule):
        return [x for x in f if x["bot"] == bot and x["rule"] == rule]

    # V11 — 'none' SUPPRESSES the forward rules. Without this, the two control
    #       clones and NoPT50 would false-alarm every single day.
    f_none, _ = synth(**{CHAMP: ["none", "none", "none", ""]})
    fired = [x for x in f_none if x["bot"] == CHAMP and x["severity"] == "RED"
             and x["rule"] in ("PT_DECLARED_NOT_TAKEN", "PT_NEVER_FIRES",
                               "TIME_EXIT_MISSED")]
    check("V11 pt_pct='none' suppresses the forward PT/time rules "
          "(no daily false alarm on the control clones)",
          not fired, f"got {[x['rule'] for x in fired]}")

    # V12 — BLANK IS NOT NONE. A blank cell must produce an announced blind spot.
    f_blank, _ = synth(**{CHAMP: ["", "", "", ""]})
    sk = [x for x in rules_for(f_blank, CHAMP, "PT_DECLARED_NOT_TAKEN")
          if x["severity"] == "SKIPPED"]
    check("V12 blank pt_pct reports SKIPPED (missing data), NOT silence and NOT 'none'",
          bool(sk) and not rules_for(f_none, CHAMP, "PT_DECLARED_NOT_TAKEN"),
          f"blank->{[x['severity'] for x in rules_for(f_blank, CHAMP, 'PT_DECLARED_NOT_TAKEN')]}, "
          f"none->{[x['severity'] for x in rules_for(f_none, CHAMP, 'PT_DECLARED_NOT_TAKEN')]}")

    # V13 — the INVERSE check fires. The champion's real pre-lapse PT25 fills are
    #       the ground truth: declare its PT removed and the detector must object.
    inv = [x for x in rules_for(f_none, CHAMP, "REMOVED_EXIT_FIRED")
           if x["severity"] == "RED"]
    check("V13 pt_pct='none' + observed PT-consistent closes -> REMOVED_EXIT_FIRED RED "
          "(the control clones' inverted Day-0 proof, automated)",
          bool(inv), f"got {[(x['rule'], x['severity']) for x in rules_for(f_none, CHAMP, 'REMOVED_EXIT_FIRED')]}")

    # V14 — a typo is refused, never coerced into a threshold.
    f_bad, _ = synth(**{CHAMP: ["PT25", "", "", ""]})
    bad = [x for x in rules_for(f_bad, CHAMP, "PT_DECLARED_NOT_TAKEN")
           if x["severity"] == "RED" and "PT25" in x["observed"]]
    check("V14 an unparseable cell ('PT25') is refused loudly, not coerced",
          bool(bad), f"got {[(x['severity'], x['observed']) for x in rules_for(f_bad, CHAMP, 'PT_DECLARED_NOT_TAKEN')]}")

    # --- V16-V18: the derived-risk SECOND WITNESS ---------------------------
    # V16 — the witness corroborates every row in the frozen archive. Under a
    #       credit-only formula the 13 debit rows miss by 30-160%; the structure
    #       branch is load-bearing, not a refinement.
    mism = [f for f in findings if f["rule"] in ("RISK_MISMATCH", "RISK_UNWITNESSED")]
    check("V16 derived risk corroborates all 1,380 archive rows "
          "(0 mismatches, 0 unwitnessed)",
          not mism, f"got {[(f['rule'], f['trade_id']) for f in mism[:5]]}")

    # V17 — T00845's own risk is corroborated, so its IMPOSSIBLE_FILL is a claim
    #       about the FILL, not about a suspect risk column. This is the whole
    #       point of the witness: it must agree here, or the R -1.10 is unsafe.
    t845 = [r for r in rows if r["trade_id"] == "T00845"
            and r["structure"] == "shortcallspread"][0]
    d845, _ = derived_risk(t845)
    check("V17 T00845's risk derives clean (181 == 181) — the witness disagrees "
          "with the FILL, not with the risk column",
          d845 is not None and abs(d845 - fl(t845["risk"])) <= RISK_TOL_ABS,
          f"derived={d845}, oa={t845['risk']}")

    # V18 — THE MASKING CASE. A risk that is wrong-HIGH silently hides an
    #       impossible fill: pnl < -risk simply stops being true. The witness has
    #       to catch what IMPOSSIBLE_FILL can no longer see.
    import tempfile as _tf
    corrupted = _tf.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="")
    with open(ledger) as src:
        rd = csv.DictReader(src)
        wr = csv.DictWriter(corrupted, fieldnames=rd.fieldnames)
        wr.writeheader()
        for r in rd:
            if r["trade_id"] == "T00845" and r["structure"] == "shortcallspread":
                r["risk"] = "500"          # plausible, wrong, and masks the fill
            wr.writerow(r)
    corrupted.close()
    _, f_corrupt, _, _ = run(corrupted.name, os.path.join(D, "bots_config_v2.csv"),
                             os.path.join(D, "bots_meta.csv"))
    os.unlink(corrupted.name)
    imp_c = {f["trade_id"] for f in f_corrupt if f["rule"] == "IMPOSSIBLE_FILL"}
    mis_c = {f["trade_id"] for f in f_corrupt if f["rule"] == "RISK_MISMATCH"
             and f["severity"] == "RED"}
    check("V18 wrong-HIGH risk masks IMPOSSIBLE_FILL on T00845, and RISK_MISMATCH "
          "catches it anyway (the second witness earns its keep)",
          "T00845" not in imp_c and "T00845" in mis_c,
          f"impossible={sorted(imp_c)}, mismatch={sorted(mis_c)}")

    # V19 — the PT band. The forensic record is 119 band closes over the champion's
    #       306 pre-lapse closed LEGS, band [0.25, 0.35]. The shipped band must sit
    #       on that number, not 20 above it.
    champ_pre = [r for r in rows if r["bot"] == "IC-SPX-FastPT25-S2"
                 and r["open_date"][:10] < "2026-06-01"]
    band_n = sum(1 for r in champ_pre if is_pt_consistent(r, 0.25))
    check("V19 PT band reproduces the forensic pre-lapse record "
          "(119-125 of 306 legs, not 141)",
          len(champ_pre) == 306 and 119 <= band_n <= 125,
          f"n_prelapse={len(champ_pre)}, band closes={band_n}")

    # V15 — the backstop rule needs BOTH columns and fires only in the gap
    #       between them. This is the $9,618 failure mode.
    f_bs, _ = synth(**{CHAMP: ["none", "", "13:00", "13:05"]})
    bs = [x for x in f_bs if x["bot"] == CHAMP and x["rule"] == "BACKSTOP_CAUGHT_IT"]
    f_bs_half, _ = synth(**{CHAMP: ["none", "", "13:00", ""]})
    bs_half = [x for x in f_bs_half if x["rule"] == "BACKSTOP_CAUGHT_IT"
               and x["severity"] == "RED"]
    check("V15 BACKSTOP_CAUGHT_IT fires only with BOTH time_exit and "
          "event_backstop, and only inside the gap",
          bool(bs) and not bs_half,
          f"both->{len(bs)}, backstop-blank->{len(bs_half)}")

    print("=" * 74)
    print("VALIDATION MATRIX — detector vs the frozen v1 archive + 35-row fixture")
    print("=" * 74)
    for ok, name, detail in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
        if not ok and detail:
            print(f"        {detail}")
    n_fail = sum(1 for ok, _, _ in results if not ok)
    print("-" * 74)
    print(f"{len(results) - n_fail}/{len(results)} passed")
    return 0 if n_fail == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", default=os.path.join(D, "trades.csv"))
    ap.add_argument("--config", default=os.path.join(D, "bots_config_v2.csv"))
    ap.add_argument("--meta", default=os.path.join(D, "bots_meta.csv"))
    ap.add_argument("--out", default=os.path.join(D, "execution_audit_findings.csv"))
    ap.add_argument("--since"), ap.add_argument("--until")
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()
    if a.validate:
        sys.exit(validate())
    rows, findings, has_cfg, window = run(a.ledger, a.config, a.meta, a.since, a.until)
    report(rows, findings, has_cfg, window, a.out, write=not a.no_write)


if __name__ == "__main__":
    main()
