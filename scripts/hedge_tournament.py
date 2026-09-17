#!/usr/bin/env python3
"""Free Hedge Tournament — daily counterfactual engine (spec: docs/hedge-research.md
§"Free Hedge Tournament — daily counterfactual engine (build spec, 2026-07-03)").

Replays every REAL leg in data/trades.csv with risk > 0 — BOTH populations,
status=expired AND status=closed (widened per
R-2026-09-16-TOURNAMENT-BASELINE; the expired-only universe never saw a losing
leg) — through a library of hedge/exit rules and books what each rule WOULD
have returned, in R (modeled_pnl / risk). This is the "loss autopsy on every
losing day" made automatic: every trading day = ~6 free hedge experiments, no
new backtest.

THE BASELINE IS PER-POPULATION, AND THE POPULATIONS ARE NEVER POOLED:
  status=expired -> `actual` = settlement pnl (riding IS what happened)
  status=closed  -> `actual` = the recorded early-exit fill (NOT settlement)
A rule that does not fire on a closed leg books the leg's actual exit pnl —
it does not claim the position would have recovered. Any question that
requires the position to have lived past its recorded close (the hold-longer /
"would it have recovered" counterfactual) is NOT EVALUABLE — no post-exit data
exists — and gets a marker row, never a modeled number.

WHY LEGS, NOT CONDORS: risk in data/trades.csv is a PER-LEG defined-risk figure
(each call-spread / put-spread carries its own risk; verified — 403/446 multi-leg
trade_ids have DIFFERING risk across their legs, e.g. a $5-wide put spread with
$0.20 credit books risk=4800 while its call-spread sibling books risk=4900). So
this engine, like daily_brief.py's leg_breach(), operates at the LEG grain — one
row of trades.csv is one hedge-tournament "position". Condor-level rollups (if
ever wanted) would sum legs by trade_id after the fact.

BASIS FOR PT/SL %: verified against the ledger — for a leg that expired worthless
(the clean full-winner case), pnl / |premium| == mfe_pct exactly (e.g. T00001 put
leg: premium=-200, pnl=200, mfe_pct=1 -> pnl/|premium|=1.0). That means mfe_pct/
mae_pct are ALREADY expressed as a fraction of the CREDIT COLLECTED (|premium|),
the standard options convention (spec's explicit fallback when in doubt) — NOT a
fraction of risk. So:
    credit_basis = abs(premium)          # $ credit collected on this leg
    PT+X% booked pnl  = +X/100 * credit_basis
    SL-X% booked pnl  = -X/100 * credit_basis
R (for every arm) = modeled_pnl / risk — risk stays the denominator throughout,
per project law (compare by R, never $), independent of the PT/SL basis choice.

DEBIT STRUCTURES (longcallspread/longputspread — the Directional book): premium
is POSITIVE (a debit paid), credit_basis using abs(premium) still gives the
$ amount at stake, but "PT/SL % of credit collected" is a credit-structure idiom.
For debit legs we still apply the same mechanical rule (mfe_pct/mae_pct are
already computed by OA consistently regardless of structure — verified above,
T00038 longcallspread: pnl/premium = 1.027 = mfe_pct) so the arms are directly
comparable in R even though the economic interpretation of "credit_basis" differs
(it's the debit paid, i.e. max-loss basis, for a long spread). Not a special case
in the code — just noted here so the PT/SL % isn't misread as "% of credit" for
the debit book.

ARMS (v1 library):
  actual      Arm 1: the leg's recorded outcome as-is (pnl column verbatim —
              settlement for expired legs, the real early-exit fill for closed
              legs). Was 'ride' pre-R-2026-09-16-TOURNAMENT-BASELINE.
  pt25/50/100 Arm 2: if mfe_pct >= X/100 -> book +X/100*credit_basis; else actual.
  sl50/75/100/130
              Arm 3: if mae_pct <= -X/100 -> book -X/100*credit_basis; else actual.
  s2          Arm 4: if the tape's high/low touched this leg's short strike
              WHILE THE POSITION WAS OPEN -> cut at the touch-implied loss
              (approx=True always; 5-min tape grain, not a sub-second latch).
              For closed legs the touch window ends at the recorded close — a
              touch after the actual exit is post-exit data and does not fire
              the rule. N/A when no tape exists for that (date, underlying) —
              most of history predates tape.py.
  defang      Arm 5: v1 = NOT MODELED. Needs the premium-decay path (mark to a
              $0.05 close on the short leg), which isn't in the ledger. Emits a
              single 'deferred' marker row per leg so the standings table can
              show N/A honestly instead of faking precision (spec: "v1 = mark
              approx or defer with a clear TODO; do not fake precision").
  settle      MARKER, not an arm — emitted only for closed legs. The
              held-to-settlement counterfactual is NOT EVALUABLE: the position
              stopped generating data at its actual exit. Empty modeled_pnl/R,
              like defang. Never model it.

ORDER RESOLUTION (mandatory correctness rule): when a leg's mfe_pct and mae_pct
BOTH cross a rule's thresholds (e.g. hit PT25 AND later blew through SL75), use
mfe_date/mae_date to see which happened first and only book the one that would
have fired first; a rule can't fire on an extreme that happened after its
opposite-side exit already closed the position.

OPTIMISTIC-BOUND LABELING (mandatory): every modeled arm except 'actual'
assumes a fill exactly at the threshold. Real fills slip. This engine is an
upper bound, NOT a live-achievable estimate — never presented as executable P/L
(mirrors the "real returns run below backtest" project law).

CHECKS (replaced the old ride-vs-ledger reconciliation, which summed the same
number from the same leg in the same pass and could not fail — see
docs/decision-card-2026-09-16-tournament-baseline.md):
  1. POPULATION  replayed legs == trades.csv legs with risk > 0 in scope
                 (catches a silently-dropped leg).
  2. ORDERING    every FIRED pt/sl rule on a closed leg must have its trigger
                 timestamp (mfe_date / mae_date) <= the leg's actual close_date
                 — a fired rule that fired only after the exit is fabricated.
                 (s2 is bounded to the position's lifetime by construction.)
  3. BOUNDS      every modeled_pnl lies within [-risk, credit_basis] — a booked
                 loss deeper than defined risk or a gain above the credit basis
                 is fabrication, not modeling.
Each failure prints a loud specific line and sets the exit code non-zero.

OUTPUT: appends/upserts data/hedge_tournament.csv, one row per
(bot, open_date, short_put, short_call, rule). Columns: date, open_date,
trade_id, bot, pillar, underlying, structure, short_put, short_call, regime,
rule, modeled_pnl, risk, R, approx_flag, basis_note.
Idempotent per date: re-running a date replaces that date's rows (like
compliance.csv's upsert pattern in daily_brief.py), so daily.sh can call this
every day without duplicating history. The persistent key is the natural key
(bot, open_date, short_put, short_call, rule). trade_id is build_ledger.py's
natural-key hash (stable across rebuilds since T-10); on every run the rows
kept from earlier dates are re-keyed from the ledger by their natural key, so
an accumulator written under an older id scheme migrates forward on contact
(G-4) and never goes stale against the trades.csv beside it.

Usage:  python3 scripts/hedge_tournament.py [YYYY-MM-DD]
        (date filters which day's LEDGER rows get (re)computed; default = ALL
        risk>0 legs in the ledger, i.e. a full rebuild — matches build_ledger.py's
        idempotent-rebuild convention. Pass a date to (re)compute just that day,
        e.g. after a backfill, without touching other days' rows.)
        build(day, expired_only=True) is the regression/acceptance harness for
        R-2026-09-16-TOURNAMENT-BASELINE — replay the pre-change universe; it is
        not a CLI mode (a restricted run must never upsert over live output).
Run AFTER tape.py + daily_brief.py (S2 arm reads the day's tape JSON) and BEFORE
report.py (report.py renders the standings from data/hedge_tournament.csv).
"""
import csv, os, sys, json, datetime, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")
BRIEF = os.path.join(D, "brief")
OUT_CSV = os.path.join(D, "hedge_tournament.csv")

PT_LEVELS = (25, 50, 100)
SL_LEVELS = (50, 75, 100, 130)

COLS = ["date", "open_date", "trade_id", "bot", "pillar", "underlying", "structure",
        "short_put", "short_call", "regime", "rule", "modeled_pnl", "risk", "R",
        "approx_flag", "basis_note", "status"]


def fl(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load(name):
    p = os.path.join(D, name)
    return list(csv.DictReader(open(p))) if os.path.exists(p) else []


def hhmm(ts):
    return ts[11:16] if ts and len(ts) >= 16 else ""


# ----------------------------------------------------------------------------
# tape access (for the S2 arm) — mirrors daily_brief.py's post_entry_window
# ----------------------------------------------------------------------------
def load_tapes():
    """date -> {underlying: tape_record} for every *_tape.json on disk."""
    out = {}
    if not os.path.isdir(BRIEF):
        return out
    for fn in sorted(os.listdir(BRIEF)):
        if not fn.endswith("_tape.json"):
            continue
        day = fn[: -len("_tape.json")]
        try:
            tape = json.load(open(os.path.join(BRIEF, fn)))
        except (ValueError, OSError):
            continue
        out[day] = tape.get("underlyings", {})
    return out


def post_entry_window(series, entry_hm, end_hm=None):
    """(low, high) of the intraday path from entry onward. Same logic as
    daily_brief.py.post_entry_window — a pre-entry spike isn't this leg's breach.
    end_hm caps the window at the position's actual close: for a closed leg a
    touch after the exit is post-exit data and must not fire the rule. None =
    unbounded (expired legs — byte-identical to the pre-widening behavior)."""
    if not series:
        return None, None
    post = [b for b in series if b.get("t", "") >= (entry_hm or "00:00")]
    post = post or series
    if end_hm:
        post = [b for b in post if b.get("t", "") <= end_hm]
        if not post:
            return None, None
    lows = [b["l"] for b in post if b.get("l") is not None]
    highs = [b["h"] for b in post if b.get("h") is not None]
    return (min(lows) if lows else None, max(highs) if highs else None)


def regime_label(tape_u):
    if not tape_u:
        return "n/a"
    return tape_u.get("label") or "n/a"


# ----------------------------------------------------------------------------
# per-leg helpers
# ----------------------------------------------------------------------------
def credit_basis(leg):
    """$ magnitude of the leg's premium (credit collected, or debit paid for a
    long spread) — the basis PT/SL % are expressed against. See module docstring."""
    p = fl(leg.get("premium"))
    return abs(p) if p is not None else None


def short_strike(leg):
    """(side, strike) for this leg's SHORT strike, or (None, None) if n/a
    (long-only structures, or a leg with no short leg parsed)."""
    if leg["structure"] == "shortputspread":
        sp = fl(leg.get("short_put"))
        return ("put", sp) if sp is not None else (None, None)
    if leg["structure"] == "shortcallspread":
        sc = fl(leg.get("short_call"))
        return ("call", sc) if sc is not None else (None, None)
    return (None, None)


def order_resolve(mfe_pct, mae_pct, mfe_date, mae_date, pt_frac, sl_frac):
    """Did PT (mfe_pct >= pt_frac) or SL (mae_pct <= -sl_frac) fire first?
    Returns 'pt' | 'sl' | None (neither threshold reached -> ride).
    Ties / missing timestamps: if only one threshold is crossed, that one wins
    outright (no ordering needed). If BOTH are crossed, use the timestamps —
    whichever extreme was reached earlier in the session fired first."""
    hit_pt = mfe_pct is not None and pt_frac is not None and mfe_pct >= pt_frac
    hit_sl = mae_pct is not None and sl_frac is not None and mae_pct <= -sl_frac
    if hit_pt and not hit_sl:
        return "pt"
    if hit_sl and not hit_pt:
        return "sl"
    if hit_pt and hit_sl:
        tpt, tsl = hhmm(mfe_date), hhmm(mae_date)
        if tpt and tsl:
            return "pt" if tpt <= tsl else "sl"
        return "sl"  # unknown order -> conservative (loss-side) assumption
    return None


# ----------------------------------------------------------------------------
# arms
# ----------------------------------------------------------------------------
def arm_actual(leg):
    """The baseline: what the leg ACTUALLY returned. Settlement pnl for expired
    legs, the recorded early-exit fill for closed legs — both are the pnl column
    verbatim; the label differs, the number does not."""
    return fl(leg["pnl"]), False


def arm_pt(leg, x):
    """PT+X%: if mfe_pct >= X/100, book +X/100*credit_basis UNLESS an SL level
    at the same X reached first per order_resolve — here we resolve against the
    SAME X threshold on the loss side is not symmetric (PT and SL levels differ
    in the sweep), so order_resolve compares this specific PT frac against
    whether mae_pct crossed ANY loss at all (mae_pct <= 0 alone doesn't mean a
    stop rule fired — only the SL arms carry their own thresholds). For the PT
    arm in isolation the only question is "did price reach +X% before the
    position's own settlement" — settlement is what 'actual' already books, so
    we only need mfe_pct vs the threshold; no cross-arm resolution is meaningful
    here (each arm is evaluated independently, per the spec's per-rule design).
    On a closed leg a firing mfe is bounded by the position's life (verified:
    mfe_date <= close_date — the ordering check enforces it); a non-fired rule
    books the leg's actual exit pnl, never a modeled recovery."""
    pt_frac = x / 100.0
    mfe = fl(leg.get("mfe_pct"))
    cb = credit_basis(leg)
    if mfe is not None and cb is not None and mfe >= pt_frac:
        return pt_frac * cb, True
    return fl(leg["pnl"]), False


def arm_sl(leg, x):
    """SL-X%: if mae_pct <= -X/100, book -X/100*credit_basis; else actual.
    Independent per-rule evaluation (see arm_pt note) — each SL rung is its own
    counterfactual world, not stacked with the PT arms."""
    sl_frac = x / 100.0
    mae = fl(leg.get("mae_pct"))
    cb = credit_basis(leg)
    if mae is not None and cb is not None and mae <= -sl_frac:
        return -sl_frac * cb, True
    return fl(leg["pnl"]), False


def arm_s2(leg, tapes_by_date):
    """S2 strike-touch cut: if the tape's post-entry high/low touched this leg's
    short strike, cut at the touch-implied loss. Touch-implied loss is modeled
    as the leg riding to its OWN mae_pct*credit_basis (the worst excursion
    reached) as the cut price IF that worst excursion coincides with (at/after)
    the touch — approximated here as: on touch, book the leg's mae_pct (the
    worst path point) as the cut, since we don't have a tick-level premium path
    to know the exact P/L AT the moment of touch (spec explicitly allows this:
    S2 is approx/5-min grain, not a sub-second latch). For a CLOSED leg the
    touch window ends at the recorded close — a touch after the actual exit is
    post-exit data, and post-exit data never fires a rule. Returns (pnl, approx,
    applicable) — applicable=False when no tape covers this leg's (date,
    underlying), or when a closed leg has no close_date to bound the window by,
    so the caller can skip emitting a row rather than fabricate one."""
    day = leg["open_date"][:10]
    und = leg["underlying"]
    tape_u = (tapes_by_date.get(day) or {}).get(und)
    if not tape_u:
        return None, True, False
    side, strike = short_strike(leg)
    if side is None or strike is None:
        return None, True, False
    end_hm = None
    if leg["status"] == "closed":
        end_hm = hhmm(leg["close_date"])
        if not end_hm:
            return None, True, False  # can't bound the window -> don't model
    series = tape_u.get("series") or []
    entry_hm = hhmm(leg["open_date"])
    post_lo, post_hi = post_entry_window(series, entry_hm, end_hm)
    touched = False
    if side == "put" and post_lo is not None and post_lo <= strike:
        touched = True
    if side == "call" and post_hi is not None and post_hi >= strike:
        touched = True
    if not touched:
        # no touch in-life -> S2 never fires -> the leg's actual outcome stands
        return fl(leg["pnl"]), True, True
    cb = credit_basis(leg)
    mae = fl(leg.get("mae_pct"))
    if cb is None or mae is None:
        return None, True, False
    # cut at the touch-implied loss = the worst excursion reached (approx: we
    # don't have the intraday premium path, only the leg's own MAE extreme).
    cut_pnl = mae * cb
    return cut_pnl, True, True


# ----------------------------------------------------------------------------
def build(day_filter=None, expired_only=False):
    trades = load("trades.csv")
    tapes_by_date = load_tapes()
    # Universe (R-2026-09-16-TOURNAMENT-BASELINE): every leg with risk > 0, both
    # statuses — the expired-only population never contained a losing leg.
    # expired_only=True replays the pre-change universe for the acceptance test.
    universe = [t for t in trades if not expired_only or t["status"] == "expired"]
    if day_filter:
        scope = [t for t in universe if t["open_date"][:10] == day_filter]
    else:
        scope = universe  # full idempotent rebuild, like build_ledger.py
    expected_legs = sum(1 for t in scope if (fl(t["risk"]) or 0) > 0)

    rows_out = []
    n_replayed = 0
    n_skipped = 0
    n_by_status = collections.Counter()
    ordering_violations = []   # (rule, trade_id, trigger_ts, close_date)
    bounds_violations = []     # (rule, trade_id, modeled_pnl, lo, hi)

    def _check_bounds(rule, t, risk, pnl):
        cb = credit_basis(t)
        lo, hi = -risk, cb
        if pnl is None:
            bounds_violations.append((rule, t["trade_id"], "n/a — no pnl", lo, hi))
        elif cb is None:
            bounds_violations.append((rule, t["trade_id"], pnl, "n/a", "n/a — no premium"))
        elif pnl < lo - 0.01 or pnl > hi + 0.01:
            bounds_violations.append((rule, t["trade_id"], pnl, lo, hi))

    def _check_ordering(rule, t, fired, trigger_ts):
        if not fired or t["status"] != "closed":
            return
        cd = t.get("close_date") or ""
        if not trigger_ts or not cd or trigger_ts > cd:
            ordering_violations.append((rule, t["trade_id"], trigger_ts or "missing", cd or "missing"))

    for t in scope:
        day = t["open_date"][:10]
        risk = fl(t["risk"])
        if not risk or risk <= 0:
            n_skipped += 1
            continue  # can't book an R without a risk denominator
        n_replayed += 1
        n_by_status[t["status"]] += 1
        is_closed = t["status"] == "closed"
        tape_u = (tapes_by_date.get(day) or {}).get(t["underlying"])
        regime = regime_label(tape_u)
        base = dict(date=day, open_date=t["open_date"], trade_id=t["trade_id"],
                    bot=t["bot"], pillar=t["pillar"], underlying=t["underlying"],
                    structure=t["structure"], short_put=t.get("short_put") or "",
                    short_call=t.get("short_call") or "", regime=regime,
                    risk=risk, status=t["status"])

        # Arm 1: actual — the leg's recorded outcome. Per-population basis:
        # expired -> riding IS settlement; closed -> the real early-exit fill.
        pnl, approx = arm_actual(t)
        _check_bounds("actual", t, risk, pnl)
        rows_out.append({**base, "rule": "actual", "modeled_pnl": round(pnl, 2),
                          "R": round(pnl / risk, 4), "approx_flag": approx,
                          "basis_note": ("actual exit pnl (ledger, verbatim) - NOT settlement"
                                         if is_closed else
                                         "settlement pnl (ledger, verbatim)")})

        # Arm 2: PT+X% — non-fired legs book the actual outcome (else actual);
        # on a closed leg a firing mfe is verified in-life by the ordering check.
        for x in PT_LEVELS:
            pnl, fired = arm_pt(t, x)
            _check_ordering(f"pt{x}", t, fired, t.get("mfe_date"))
            _check_bounds(f"pt{x}", t, risk, pnl)
            if fired:
                note = f"booked +{x}% of credit_basis at mfe_pct threshold"
            else:
                note = ("no PT hit -> actual exit pnl (ledger)" if is_closed
                        else "no PT hit -> rode to settlement")
            rows_out.append({**base, "rule": f"pt{x}", "modeled_pnl": round(pnl, 2),
                              "R": round(pnl / risk, 4), "approx_flag": True,
                              "basis_note": f"optimistic bound: {note}"})

        # Arm 3: SL-X% — same else-actual fallback, same in-life trigger law.
        for x in SL_LEVELS:
            pnl, fired = arm_sl(t, x)
            _check_ordering(f"sl{x}", t, fired, t.get("mae_date"))
            _check_bounds(f"sl{x}", t, risk, pnl)
            if fired:
                note = f"booked -{x}% of credit_basis at mae_pct threshold"
            else:
                note = ("no SL hit -> actual exit pnl (ledger)" if is_closed
                        else "no SL hit -> rode to settlement")
            rows_out.append({**base, "rule": f"sl{x}", "modeled_pnl": round(pnl, 2),
                              "R": round(pnl / risk, 4), "approx_flag": True,
                              "basis_note": f"optimistic bound: {note}"})

        # Arm 4: S2 strike-touch cut (only where tape exists; window bounded at
        # the actual close for closed legs — a later touch is post-exit data).
        s2_pnl, s2_approx, s2_ok = arm_s2(t, tapes_by_date)
        if s2_ok and s2_pnl is not None:
            _check_bounds("s2", t, risk, s2_pnl)
            rows_out.append({**base, "rule": "s2", "modeled_pnl": round(s2_pnl, 2),
                              "R": round(s2_pnl / risk, 4), "approx_flag": True,
                              "basis_note": "strike-touch cut, 5-min tape grain (not sub-second latch); "
                                            "cut priced at the leg's own worst-excursion (mae_pct) extreme"
                                            + ("; touch window bounded at actual close" if is_closed else "")})
        # else: no tape for this (date, underlying) -> emit nothing (honest N/A,
        # not a fabricated row); most pre-2026-06-26 history has no tape file.

        # Arm 5: Defang — v1 explicitly deferred, per spec ("mark approx or
        # defer with a clear TODO; do not fake precision"). Emit one 'deferred'
        # marker row so the standings table can report N (count) = 0 modeled,
        # rather than silently omitting the rule from the library entirely.
        rows_out.append({**base, "rule": "defang", "modeled_pnl": "",
                          "R": "", "approx_flag": True,
                          "basis_note": "DEFERRED v1 — needs the intraday premium-decay path "
                                        "(mark short leg to ~$0.05) not present in the ledger. "
                                        "TODO: model once tick/1-min option-premium history is available."})

        # NOT EVALUABLE marker — closed legs only. The held-to-settlement
        # counterfactual requires post-exit path data that does not exist;
        # per R-2026-09-16-TOURNAMENT-BASELINE item 4 it is marked, never
        # modeled. (Answerable only in OA's zdte.* backtester, gated on
        # written OA authorization.)
        if is_closed:
            rows_out.append({**base, "rule": "settle", "modeled_pnl": "",
                              "R": "", "approx_flag": True,
                              "basis_note": "NOT EVALUABLE — position closed early; what it would "
                                            "have returned held to settlement needs post-exit path "
                                            "data that does not exist. Never modeled."})

    # --- three checks that can actually fail (replaces the dead recon) -------
    checks_ok = True
    # 1. POPULATION: every in-scope risk>0 leg must have been replayed — the
    #    old skip at the risk guard was silent.
    if n_replayed != expected_legs:
        checks_ok = False
        print(f"hedge_tournament.py: POPULATION CHECK FAILED — replayed {n_replayed} "
              f"legs but {expected_legs} in-scope trades.csv legs have risk > 0 "
              f"({n_skipped} skipped with risk<=0)")
    # 2. ORDERING: a fired rule on a closed leg must have fired in-life.
    for rule, tid, trig, cd in ordering_violations:
        checks_ok = False
        print(f"hedge_tournament.py: ORDERING CHECK FAILED — {rule} fired on {tid} "
              f"(closed leg) with trigger {trig} after close_date {cd}")
    # 3. BOUNDS: every modeled_pnl inside [-risk, credit_basis].
    for rule, tid, pnl, lo, hi in bounds_violations:
        checks_ok = False
        print(f"hedge_tournament.py: BOUNDS CHECK FAILED — {rule} on {tid} modeled "
              f"{pnl} outside [{lo}, {hi}]")

    # --- write / upsert data/hedge_tournament.csv ----------------------------
    # Idempotent per date: keep all existing rows for dates NOT in this run,
    # replace rows for dates that ARE in this run (mirrors compliance.csv's
    # upsert-by-key pattern in daily_brief.py). Within a day the persistent key
    # is (bot, open_date, short_put, short_call, rule). trade_id is carried
    # from the ledger and re-keyed below (G-4).
    trades_by_tid = {t["trade_id"]: t for t in trades if t.get("trade_id")}
    status_by_key = {(t["bot"], t["open_date"], t.get("short_put") or "",
                      t.get("short_call") or ""): t["status"] for t in trades}
    existing = []
    if os.path.exists(OUT_CSV):
        existing = list(csv.DictReader(open(OUT_CSV)))
    # Back-fill the natural-key columns for rows written by the old schema.
    for r in existing:
        if "open_date" not in r:
            r["open_date"] = (trades_by_tid.get(r.get("trade_id"), {}).get("open_date")
                              or r["date"])
        if "short_put" not in r:
            r["short_put"] = (trades_by_tid.get(r.get("trade_id"), {}).get("short_put")
                              or "")
        if "short_call" not in r:
            r["short_call"] = (trades_by_tid.get(r.get("trade_id"), {}).get("short_call")
                               or "")
        if not r.get("status"):
            r["status"] = status_by_key.get((r["bot"], r.get("open_date") or "",
                                             r["short_put"], r["short_call"]), "")
    touched_days = {r["date"] for r in rows_out}
    kept = [r for r in existing if r["date"] not in touched_days]
    # G-4: re-key kept rows on the natural key. Every leg in the ledger resolves
    # by (bot, open_date, short_put, short_call); a kept row whose key resolves
    # takes the ledger's current trade_id. One that does not is left as written
    # and counted out loud — never silently dropped, never silently re-keyed.
    tid_by_key = {(t["bot"], t["open_date"], t.get("short_put") or "",
                   t.get("short_call") or ""): t["trade_id"] for t in trades}
    rekeyed = unresolved = 0
    for r in kept:
        k = (r["bot"], r.get("open_date") or "", r.get("short_put") or "",
             r.get("short_call") or "")
        tid = tid_by_key.get(k)
        if tid is None:
            unresolved += 1
        elif tid != r.get("trade_id"):
            r["trade_id"] = tid
            rekeyed += 1
    if rekeyed or unresolved:
        print(f"hedge_tournament.py: G-4 re-key of kept rows — {rekeyed} trade_id(s) "
              f"updated from the ledger, {unresolved} natural key(s) unresolved "
              f"(left as written)")
    all_rows = kept + rows_out
    all_rows.sort(key=lambda r: (
        r["date"], r["bot"], r.get("open_date") or r["date"],
        r.get("short_put") or "", r.get("short_call") or "",
        r["rule"], r["trade_id"]))
    with open(OUT_CSV, "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=COLS)
        w.writeheader()
        for r in all_rows:
            w.writerow({c: r.get(c, "") for c in COLS})

    n_days = len(touched_days)
    pop_desc = " / ".join(f"{n} {s}" for s, n in sorted(n_by_status.items()))
    print(f"hedge_tournament.py: {'ALL' if not day_filter else day_filter} | "
          f"{n_replayed} legs replayed ({pop_desc}) across {n_days} day(s) | "
          f"{n_skipped} skipped (risk<=0) | "
          f"{len(rows_out)} rows (this run) -> {len(all_rows)} total in hedge_tournament.csv | "
          f"checks {'OK' if checks_ok else 'FAILED — see failures above'}")
    return checks_ok


def newest_date():
    trades = load("trades.csv")
    return max((t["open_date"][:10] for t in trades), default=datetime.date.today().isoformat())


if __name__ == "__main__":
    day = sys.argv[1] if len(sys.argv) > 1 else None
    ok = build(day)
    sys.exit(0 if ok else 1)
