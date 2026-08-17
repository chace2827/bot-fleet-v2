#!/usr/bin/env python3
"""Track A of the research loop — counterfactual variants over closed POSITIONS.

⛔ DO-NOT-WIRE.  This script is NOT wired into scripts/daily.sh and MUST NOT be
(research-loop-spec.md §5a, §6.5; research-loop-review-2026-08-04.md §1). It is a
GENERATOR: it writes data/counterfactuals.csv + data/research_log.md and NOTHING
else. It may never write a bot config, emit an instruction card, or report a
winner. Graduation is a human decision at the §5 gate, evaluated ONCE (§10a).

This is the 0.2.0-DRAFT rewrite specified by
docs/research-loop-fix-spec-2026-08-07.md — the fix for the three fatal defects
of the 2026-08-04 review (D-6 units, D-7 CONTROL tautology, D-8 censoring) plus
the material defects that share the same code paths (D-9…D-17). Every empirical
constant below was recomputed read-only over the two FROZEN v1 sources named in
the spec §1 and reproduced this session; NONE supports a live-capital decision
(CLAUDE.md §3: v1 pre-cutover, demonstration only; an absent number is not zero).

UNIT OF ACCOUNT (CLAUDE.md §4; ruling R-6; spec §2.2)
  The unit is the POSITION — a `trade_id` group. risk = the LARGER side (MAX over
  legs), never the sum. delta_R is defined ONLY at the position (D-15). Combined
  MFE for a paired condor is a Track B question, so the PT family is UNDECIDABLE
  on any multi-leg group (R-6).

UNITS (D-6; spec §2.2). credit is a per-contract PRICE ($/ct); pnl and risk are
  DOLLARS. The counterfactual must scale credit by MULT × quantity:
      credit_$ = credit [$/ct] × MULT [$/ct/$] × quantity [ct]   -> [$]
  The old engine subtracted a price from a dollar amount — wrong by 100 ×
  quantity (median 1,100×, max 19,200×). `quantity` was never read.

VERDICTS
  FILLED / NEVER_REACHED   decidable; would / would not have triggered
  UNDECIDABLE              MFE/MAE cannot answer it (TIME_* class; multi-leg PT)
  CENSORED                 incumbent exit on that side is looser/equal — a
                           right-censored FALSE NEGATIVE, never a null (D-8)
  BLOCKED                  no incumbent-exit config for this bot — the state the
                           engine is in TODAY for every bot (D-8, spec §4.2)
  N/A — structure          loss-side family on a debit structure (D-16)
  SKIPPED                  a GATED variant whose value Andy has not signed (§10)
  CONTROL_OK/CONTROL_MISMATCH
                           the control must reproduce realised P/L. A mismatch
                           means THIS ENGINE IS WRONG, not that the strategy
                           underperformed — the run aborts non-zero (D-7).

WHY MFE/MAE IS ENOUGH FOR PT/SL AND NOT FOR TIME
  MFE/MAE give the extreme and its timestamp. A profit target at x is decidable
  (if the mark reached x, the order fills). A time exit at 15:45 needs the mark
  AT 15:45, which is not an extreme and is recorded nowhere. Time exits are a
  Track B question (R-2) and are NOT in the signed variant set.

KNOWN, IRREDUCIBLE BIASES carried in the output header, never coded away:
  * D-8  censoring by the incumbent exit — the largest bias; per-bot, distributional
  * D-10 COND uses trough time as breach time — one-sided, under-counts fills only
  * D-11 order conflict — a stop dated before a peak cannot co-exist with the peak
"""
import argparse, csv, datetime, hashlib, json, os, statistics, sys

VERSION   = "0.2.0-DRAFT"
FROZEN_ON = None          # stays None until every §6 acceptance box is green AND
                          # Andy signs. Freezing is a signature, not a code change.
MIN_N     = 30            # spec §10/R-4: emit nothing below this many CLOSED POSITIONS

# --- units (spec §2.2) -----------------------------------------------------
MULT        = 100         # [$ per contract per $1.00 of price] — the OA multiplier.
                          # DERIVED and asserted per row (G-1), never trusted blind.
TOL_CONTROL = 0.01        # [$] CONTROL residual tolerance; load-bearing (spec §3.2):
                          # T00554 recomputes to 192.00000000000017, so == is False.
BRACKET_EPS = 0.51        # [$] MFE/MAE bracketing slack (G-3 / D-17)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # execution_audit.py pattern
DATA = os.path.join(ROOT, "data")

# --- structure sign classes (spec §2.2) ------------------------------------
CREDIT_STRUCTURES = {"ironcondor", "ironbutterfly", "shortputspread", "shortcallspread"}
DEBIT_STRUCTURES  = {"longcallspread", "longputspread"}
#  anything else (calendar, diagonal, naked, …) -> REFUSE the position, count it,
#  never emit a verdict (spec §2.2, guard G-7, fixture N-4).

# --- the SIGNED variant set (research-loop-spec.md §3, as amended 2026-08-04) --
# name            family  param              note
# param for cond is (level, "HH:MM"); for dstop it is the k multiplier on M_bot_$.
VARIANTS = [
    ("CONTROL",       "control", None,           "engine self-test — recompute realised P/L"),
    ("PT40",          "pt",      0.40,           "profit target 40% of credit"),
    ("PT60",          "pt",      0.60,           "profit target 60% of credit"),
    ("PT70",          "pt",      0.70,           "profit target 70% of credit"),
    ("SL100",         "sl",      1.00,           "stop at 100% of credit"),
    ("SL150",         "sl",      1.50,           "stop at 150% of credit"),
    ("SL200",         "sl",      2.00,           "stop at 200% of credit"),
    ("DSTOP_100",     "dstop",   1.00,           "fixed-$ stop at 1.00x M_bot_$ (one-time median POSITION $-credit, trailing 90d — RULED)"),
    ("DSTOP_150",     "dstop",   1.50,           "fixed-$ stop at 1.50x M_bot_$ (one-time median POSITION $-credit, trailing 90d — RULED)"),
    ("COND_100_1300", "cond",    (1.00, "13:00"),"stop 100% only if the trough came before 13:00"),
    ("COND_100_1400", "cond",    (1.00, "14:00"),"stop 100% only if the trough came before 14:00"),
    ("COND_200_1400", "cond",    (2.00, "14:00"),"stop 200% only if the trough came before 14:00"),
]
# V-0 (spec §5): the SIGNED twelve, verbatim and in order. The bare count assert
# passes on the WRONG twelve — this list assert is what catches variant drift.
SIGNED_NAMES = ["CONTROL", "PT40", "PT60", "PT70", "SL100", "SL150", "SL200",
                "DSTOP_100", "DSTOP_150", "COND_100_1300", "COND_100_1400", "COND_200_1400"]
assert len(VARIANTS) == 12, "the signed count is 12 including CONTROL"
assert [v[0] for v in VARIANTS] == SIGNED_NAMES, "variant list drifted from the signed §3 set"

LOSS_SIDE = {"sl", "dstop", "cond"}     # families that read MAE (loss side)
PROFIT_SIDE = {"pt"}                     # families that read MFE (profit side)

# ---------------------------------------------------------------------------
# §10 decisions. Two RULED 2026-08-07 (implemented); the rest stay named refusals.
# The engine still makes NO unsigned choice.
# ---------------------------------------------------------------------------
#  OPEN-1/OPEN-2  ✅ RULED 2026-08-07 — M_bot_$ = ONE-TIME calibration, median over
#                 POSITIONS, computed at the stamp date over the trailing 90 days,
#                 SKIPPED before 90 days of history exist. See compute_m_bot().
#  OPEN-3         ✅ RULED 2026-08-07 — PT family is REPORTED (R-6 unit), with a
#                 MANDATORY split: every PT line prints decidable/undecidable +
#                 single_sided share, DESCRIPTIVE-ONLY — no gate reads it.
#  OPEN-4         mixed-status / mixed-quantity groups -> REFUSED and counted.
#  OPEN-5         comparative-machinery-spec.md §1.3 risk re-derivation is wrong
#                 (omits -credit_$, no debit form). Recorded; THAT FILE UNTOUCHED.
#  OPEN-6/OPEN-7  regime-change conjunct + max-T direction vector undefined ->
#                 the §5 gate is UNREACHABLE. gate_evaluate() REFUSES (below).
#  §10a item 1 / G-11  dual-tested (bot, variant) pairs are excluded from Track A's
#                 family. The set is data-dependent (the 7 greenfield ledgers +
#                 ARM-B1) and cannot be enumerated here — REFUSAL hook below.
DUAL_TESTED_EXCLUSIONS = frozenset()     # populated ONLY before the gate runs; empty
                                         # is safe because the gate is not run nightly.


def gate_evaluate(*_a, **_k):
    """⛔ NOT IMPLEMENTED — the §5/§10a gate is GATED and UNREACHABLE today.

    Refuses rather than returning a value. Blocked on, all unsigned/undefined:
      * OPEN-6  the regime-change conjunct is undefined in every document
                (build-plan.md §5) — 'the gate cannot fire until it is written'.
      * OPEN-7 / §8 Constraint B  the per-member direction vector for the max-T
                region must be declared BEFORE any data exists; it is not.
      * §8 Constraint A  bootstrap-t studentization is forbidden unless realised
                c <= 2.638 is demonstrated and PUBLISHED. Not measured.
      * §10a item 2  the gate is evaluated ONCE, at a stamped date, never nightly.
    Nightly output is DESCRIPTIVE ONLY. `c` is emitted as GATE_NOT_RUN, never a
    fabricated number (§8: c is a mandatory published field — so it is named, not
    invented).
    """
    raise NotImplementedError(
        "GATED: the Track A gate is unreachable — OPEN-6 (regime-change conjunct), "
        "OPEN-7/§8-B (direction vector), §8-A (unproven c). §10a: gate runs ONCE, "
        "never nightly. This generator is descriptive only.")


# --- small helpers ---------------------------------------------------------
def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

def _dt(ts):
    """'2026-07-02 15:50:00' -> datetime, or None. Full datetime — D-11 needs the
    DATE, not just the clock: mae_date can precede mfe_date by days."""
    if not ts or len(ts) < 16:
        return None
    try:
        return datetime.datetime.strptime(ts[:19] if len(ts) >= 19 else ts[:16] + ":00",
                                          "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

_SELF_HASH = hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest()[:16]
def self_hash():
    """Computed ONCE at import (the old engine recomputed it per output record —
    15,048 file reads per run at capture scale, spec §6 step 7)."""
    return _SELF_HASH


# --- schema normalisation (ledger form AND raw export form) ----------------
def _normalize(row):
    """Map either the trades.csv ledger schema or the raw OA export schema to a
    common internal dict. build_ledger.py writes `credit`<-openPrice and
    `exit_price`<-closePrice (read from the code, not prose — review §6(c))."""
    if "credit" in row:                       # ledger form
        return {
            "trade_id":  row.get("trade_id", ""),
            "bot":       row.get("bot", ""),
            "pillar":    row.get("pillar", ""),
            "underlying":row.get("underlying", ""),
            "structure": (row.get("structure") or "").lower(),
            "status":    (row.get("status") or "").lower(),
            "quantity":  _f(row.get("quantity")),
            "credit":    _f(row.get("credit")),
            "exit_price":_f(row.get("exit_price")),
            "pnl":       _f(row.get("pnl")),
            "risk":      _f(row.get("risk")),
            "premium":   _f(row.get("premium")),
            "mfe_pct":   _f(row.get("mfe_pct")),
            "mae_pct":   _f(row.get("mae_pct")),
            "mfe_date":  row.get("mfe_date", ""),
            "mae_date":  row.get("mae_date", ""),
            "open_date": row.get("open_date", ""),
            "close_date":row.get("close_date", ""),
            "short_put": _f(row.get("short_put")),  "long_put":  _f(row.get("long_put")),
            "short_call":_f(row.get("short_call")), "long_call": _f(row.get("long_call")),
        }
    # raw export form (oa-export-schema.md §1) — no trade_id; each row is its own unit
    return {
        "trade_id":  row.get("__rowid__", ""),
        "bot":       row.get("botName", ""),
        "pillar":    "",
        "underlying":row.get("symbol", ""),
        "structure": (row.get("type") or "").lower(),
        "status":    (row.get("status") or "").lower(),
        "quantity":  _f(row.get("quantity")),
        "credit":    _f(row.get("openPrice")),
        "exit_price":_f(row.get("closePrice")),
        "pnl":       _f(row.get("pnl")),
        "risk":      _f(row.get("risk")),
        "premium":   _f(row.get("premium")),
        "mfe_pct":   _f(row.get("highReturnPct")),
        "mae_pct":   _f(row.get("lowReturnPct")),
        "mfe_date":  row.get("highReturnPctDate", ""),
        "mae_date":  row.get("lowReturnPctDate", ""),
        "open_date": row.get("openDate", ""),
        "close_date":row.get("closeDate", ""),
        "short_put": None, "long_put": None, "short_call": None, "long_call": None,
    }


class Refusal(Exception):
    """A position (trade_id group) that must not be scored, with a counted reason."""
    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


# --- per-leg metrics (units named at every term, spec §2.2) ----------------
def leg_metrics(r):
    """Compute the dollar-denominated metrics for one ledger leg. Raises Refusal
    on a structure outside the enumerated sign classes (G-7) or a broken MULT
    identity (G-1)."""
    st = r["structure"]
    if st in CREDIT_STRUCTURES:
        sign = "credit"
    elif st in DEBIT_STRUCTURES:
        sign = "debit"
    else:
        raise Refusal(f"structure {st!r} outside enumerated sign classes")

    q, cr, pnl, risk, prem = r["quantity"], r["credit"], r["pnl"], r["risk"], r["premium"]
    if None in (q, cr, pnl):
        raise Refusal("missing quantity / credit / pnl")

    credit_d = cr * MULT * q                                   # [$]
    # G-1 — MULT sanity assert (NOT a second witness; spec §2.3). abs(premium)
    # and credit come from two export columns with no independent derivation, so
    # this cannot vary; it is one division and it is labelled as what it is.
    if prem is not None and abs(abs(prem) - credit_d) > TOL_CONTROL:
        raise Refusal(f"MULT identity broken: |premium|={abs(prem)} != credit_$={credit_d}")

    mfe, mae = r["mfe_pct"], r["mae_pct"]
    MFE_d = None if mfe is None else mfe * credit_d            # [$]
    MAE_d = None if mae is None else mae * credit_d            # [$]

    # CONTROL cf_$ by sign class (spec §2.2). credit=openPrice, exit=closePrice.
    ex = r["exit_price"]
    control_cf = None
    if ex is not None:
        if sign == "credit":
            control_cf = (cr - ex) * MULT * q
        else:
            control_cf = (ex - cr) * MULT * q

    # G-2 — real second witness on risk (spec §2.3). credit: width×MULT×q − credit_$;
    # debit: risk == credit_$. Diagnostic only (some legged rows lack both strikes).
    risk_witness = None
    if sign == "credit" and None not in (r["short_put"], r["long_put"], r["short_call"], r["long_call"]):
        width = max(abs(r["short_put"] - r["long_put"]), abs(r["short_call"] - r["long_call"]))
        risk_witness = width * MULT * q - credit_d
    elif sign == "debit":
        risk_witness = credit_d

    # G-3 / D-17 — bracketing: the realised outcome must lie in the excursion envelope.
    bracket_ok = True
    if MAE_d is not None and MFE_d is not None:
        bracket_ok = (MAE_d - BRACKET_EPS) <= pnl <= (MFE_d + BRACKET_EPS)

    return {
        "structure": st, "sign": sign, "quantity": q,
        "credit_d": credit_d, "risk": risk, "pnl": pnl,
        "mfe_pct": mfe, "mae_pct": mae, "MFE_d": MFE_d, "MAE_d": MAE_d,
        "control_cf": control_cf, "risk_witness": risk_witness, "bracket_ok": bracket_ok,
        "mae_dt": _dt(r["mae_date"]), "mfe_dt": _dt(r["mfe_date"]),
    }


def _clamp(cf, risk):
    """cf_$ = max(cf, -risk_$) — D-16. Returns (cf_clamped, was_clamped)."""
    if risk is not None and cf < -risk:
        return -risk, True
    return cf, False


def leg_variant(m, name, fam, param, dstop_dollars=None):
    """Per-leg (verdict, cf_$, was_clamped) for one variant, PRE-aggregation and
    PRE-censoring. Emits the raw counterfactual arithmetic the fixture asserts."""
    credit_d, risk, pnl = m["credit_d"], m["risk"], m["pnl"]
    mfe, mae = m["mfe_pct"], m["mae_pct"]

    if fam == "control":
        if m["control_cf"] is None:
            return ("UNDECIDABLE", None, False)
        cf = m["control_cf"]
        ok = abs(cf - pnl) <= TOL_CONTROL
        return ("CONTROL_OK" if ok else "CONTROL_MISMATCH", cf, False)

    if fam == "pt":
        if mfe is None:
            return ("UNDECIDABLE", None, False)
        if mfe >= param:
            return ("FILLED", param * credit_d, False)
        return ("NEVER_REACHED", pnl, False)

    if fam == "sl":
        if m["sign"] == "debit":
            return ("N/A — structure", None, False)     # D-16
        if mae is None:
            return ("UNDECIDABLE", None, False)
        if mae <= -param:
            cf, cl = _clamp(-param * credit_d, risk)
            return ("FILLED", cf, cl)
        return ("NEVER_REACHED", pnl, False)

    if fam == "dstop":
        if m["sign"] == "debit":
            return ("N/A — structure", None, False)     # D-16
        if dstop_dollars is None:
            # GATED — OPEN-1/OPEN-2: M_bot_$ basis unsigned. No value picked.
            return ("SKIPPED", None, False)
        if m["MAE_d"] is None:
            return ("UNDECIDABLE", None, False)
        if m["MAE_d"] <= -dstop_dollars:
            cf, cl = _clamp(-dstop_dollars, risk)
            return ("FILLED", cf, cl)
        return ("NEVER_REACHED", pnl, False)

    if fam == "cond":
        if m["sign"] == "debit":
            return ("N/A — structure", None, False)     # D-16 (loss-side stop)
        lvl, before = param
        if mae is None or m["mae_dt"] is None:
            return ("UNDECIDABLE", None, False)
        cutoff = datetime.datetime.strptime(before, "%H:%M").time()
        # D-10: trough time is used as breach time — one-sided, under-counts fills.
        if mae <= -lvl and m["mae_dt"].time() < cutoff:
            cf, cl = _clamp(-lvl * credit_d, risk)
            return ("FILLED", cf, cl)
        return ("NEVER_REACHED", pnl, False)

    raise Refusal(f"unknown family {fam!r}")


# --- incumbent-exit config (D-8 censoring) ---------------------------------
def load_incumbent_config(path=None):
    """Return {bot_name: {'pt': v|None|'HOLD', 'sl': v|None|'HOLD'}}. A bot ABSENT
    from the dict is UNKNOWN -> every same-side cell BLOCKED (spec §4.2).

    ⚠️ TODAY this returns {} for the tested v1-ledger bots. data/bots_config_v2.csv
    carries greenfield/clone rows whose exits are decoded free-text, not a per-bot
    incumbent PT/SL threshold in a form this surface can trust, and the spec's
    scaffolding row reads `input_default = NOT SET`. Extracting a numeric incumbent
    from that free-text is a DECISION about what counts as the incumbent exit and
    is therefore GATED — so the loader deliberately trusts NOTHING and the engine's
    default is BLOCKED, never a fabricated NEVER_REACHED (spec §4.2, §4.5)."""
    return {}


def _tighter(fam, param, incumbent):
    """FALSE (evaluable) / TRUE (censored) / UNKNOWN for censoring (spec §4.2).
    A tighter variant closes SOONER: smaller PT target, smaller SL threshold. A
    bot with no exit on that side (HOLD) is the loosest incumbent — every variant
    is tighter (FALSE)."""
    side = "pt" if fam in PROFIT_SIDE else "sl"
    if incumbent is None or side not in incumbent:
        return "UNKNOWN"
    v = incumbent[side]
    if v == "HOLD" or v is None:
        return "FALSE"                       # hold-to-expiry: any exit is tighter
    thresh = param[0] if isinstance(param, tuple) else param
    return "FALSE" if thresh <= v else "TRUE"


# --- position assembly (the unit of account, D-15) -------------------------
def eval_position(legs_raw, incumbent=None, dstop_dollars=None,
                  apply_censoring=True, apply_order_conflict=True):
    """Yield one record dict per (position, variant). Raises Refusal for a group
    that must not be scored (mixed status/quantity, bad structure, MULT break)."""
    metrics, structs, statuses, quants = [], [], [], []
    for r in legs_raw:
        metrics.append(leg_metrics(r))          # may raise Refusal
        structs.append(r["structure"]); statuses.append(r["status"])
        quants.append(r["quantity"])

    # OPEN-4 — mixed-status and mixed-quantity groups have no signed rule -> REFUSE.
    if len(set(s for s in statuses if s)) > 1:
        raise Refusal("mixed-status group (OPEN-4 — no signed rule)")
    if len(set(q for q in quants if q is not None)) > 1:
        raise Refusal("mixed-quantity group (OPEN-4 — no signed rule)")

    n_legs = len(metrics)
    risk_pos = max(m["risk"] for m in metrics if m["risk"] is not None)   # MAX = larger side
    pnl_pos  = sum(m["pnl"] for m in metrics)
    credit_pos = sum(m["credit_d"] for m in metrics)
    bracket_violation = not all(m["bracket_ok"] for m in metrics)
    sign_pos = "debit" if any(m["sign"] == "debit" for m in metrics) else "credit"
    single_sided = (n_legs == 1 and metrics[0]["structure"] in ("shortputspread", "shortcallspread"))

    # position-level excursion timestamps (single-leg PT is the only PT that is
    # decidable, and D-11 order conflict only bites there)
    mfe_dt = metrics[0]["mfe_dt"] if n_legs == 1 else None
    mae_dt = metrics[0]["mae_dt"] if n_legs == 1 else None

    r0 = legs_raw[0]
    base = {
        "trade_id": r0["trade_id"], "bot": r0["bot"], "pillar": r0["pillar"],
        "underlying": r0["underlying"], "structures": "+".join(structs),
        "close_date": r0["close_date"], "n_legs": n_legs,
        "risk_pos_dollars": round(risk_pos, 2), "single_sided": single_sided,
        "bracket_violation": bracket_violation,
    }

    # first pass: raw per-position verdicts, so order-conflict can see PT vs loss.
    raw = {}
    for name, fam, param, _note in VARIANTS:
        if fam == "control":
            cfs = [m["control_cf"] for m in metrics]
            if any(c is None for c in cfs):
                raw[name] = ("UNDECIDABLE", None, None, [], 0)
            else:
                cf_pos = sum(cfs)
                ok = abs(cf_pos - pnl_pos) <= TOL_CONTROL
                # delta is 0 by construction and is EXCLUDED from every aggregate (§3.5)
                raw[name] = ("CONTROL_OK" if ok else "CONTROL_MISMATCH", cf_pos, 0.0, cfs, 0)
            continue

        if fam == "pt" and n_legs > 1:
            # R-6: combined MFE for a paired condor is a Track B question.
            raw[name] = ("UNDECIDABLE", None, None, [], 0)
            continue

        dd = dstop_dollars.get(name) if isinstance(dstop_dollars, dict) else dstop_dollars
        leg_verdicts, leg_cfs, leg_deltas, clamped = [], [], [], 0
        for m in metrics:
            v, cf, cl = leg_variant(m, name, fam, param, dstop_dollars=dd)
            leg_verdicts.append(v)
            clamped += int(cl)
            if cf is None:
                leg_cfs.append(None); leg_deltas.append(None)
            else:
                leg_cfs.append(cf); leg_deltas.append(cf - m["pnl"])

        if any(v in ("N/A — structure", "SKIPPED", "UNDECIDABLE") for v in leg_verdicts):
            # a structural / gated / undecidable leg poisons the position verdict
            for tag in ("N/A — structure", "SKIPPED", "UNDECIDABLE"):
                if tag in leg_verdicts:
                    raw[name] = (tag, None, None, [], 0)
                    break
            continue

        cf_pos = sum(leg_cfs)
        delta_pos = sum(leg_deltas)              # SUM over legs (D-15), NOT per leg
        verdict = "FILLED" if "FILLED" in leg_verdicts else "NEVER_REACHED"
        raw[name] = (verdict, cf_pos, delta_pos, leg_deltas, clamped)

    # D-11 / §4.3 — order conflict: a FILLED PT that a FILLED loss-side stop
    # precedes (mae_date < mfe_date) cannot co-exist. Downgrade the PT.
    loss_filled = any(raw[n][0] == "FILLED" for n, f, *_ in VARIANTS if f in LOSS_SIDE)
    order_conflict = bool(apply_order_conflict and loss_filled and mfe_dt and mae_dt and mae_dt < mfe_dt)

    for name, fam, param, note in VARIANTS:
        verdict, cf_pos, delta_pos, leg_deltas, clamped = raw[name]
        estimand = ("position" if fam in ("pt", "control")
                    else "per_spread_summed" if n_legs > 1 else "position")
        censored, tighter = "FALSE", "FALSE"
        conflict = False

        if fam == "pt" and order_conflict and verdict == "FILLED":
            verdict, cf_pos, delta_pos, leg_deltas = "UNDECIDABLE", None, None, []
            conflict = True

        # D-8 censoring overlay — applies to PT (profit) and SL/DSTOP/COND (loss).
        # CONTROL is a self-test and is NEVER censored (§3.5). SKIPPED/N-A/UNDECIDABLE
        # already carry no number, so leave them.
        if (apply_censoring and fam != "control"
                and verdict in ("FILLED", "NEVER_REACHED")):
            tighter = _tighter(fam, param, incumbent.get(base["bot"]) if incumbent else None)
            if tighter == "UNKNOWN":
                verdict, cf_pos, delta_pos, leg_deltas, censored = "BLOCKED", None, None, [], "UNKNOWN"
            elif tighter == "TRUE":
                verdict, cf_pos, delta_pos, leg_deltas, censored = "CENSORED", None, None, [], "TRUE"

        delta_R = (round(delta_pos / risk_pos, 6)
                   if delta_pos is not None and risk_pos else "")
        yield {
            **base, "variant": name, "family": fam, "verdict": verdict,
            "estimand": estimand,
            "cf_pos_dollars": "" if cf_pos is None else round(cf_pos, 2),
            "delta_pos_dollars": "" if delta_pos is None else round(delta_pos, 2),
            "delta_R": delta_R,
            "delta_legs": "" if not leg_deltas else "|".join(
                f"{d:.2f}" if d is not None else "" for d in leg_deltas),
            "censored": censored,
            "incumbent_exit_side": ("profit" if fam in PROFIT_SIDE
                                    else "loss" if fam in LOSS_SIDE else ""),
            "incumbent_exit_value": "",
            "incumbent_exit_source": "",          # empty -> forces UNKNOWN (§4.2)
            "variant_is_tighter": tighter if fam != "control" else "",
            "clamped_legs": clamped,
            "bracket_violation": bracket_violation,
            "order_conflict": conflict,
            "note": note,
            "engine_version": VERSION, "engine_hash": self_hash(),
            "c": "GATE_NOT_RUN",                  # §8: mandatory field, never fabricated
        }


FIELDNAMES = [
    "trade_id", "bot", "pillar", "underlying", "structures", "close_date",
    "n_legs", "single_sided", "variant", "family", "verdict", "estimand",
    "cf_pos_dollars", "delta_pos_dollars", "risk_pos_dollars", "delta_R",
    "delta_legs", "censored", "incumbent_exit_side", "incumbent_exit_value",
    "incumbent_exit_source", "variant_is_tighter", "clamped_legs",
    "bracket_violation", "order_conflict", "note", "engine_version",
    "engine_hash", "c",
]

CENSORING_BLOCK = """\
# CENSORING LIMIT — READ BEFORE ANY NUMBER BELOW
# MFE/MAE accumulate only until the position closed. Track A can therefore evaluate ONLY
# variants TIGHTER than the incumbent exit on the same side. Every LOOSER-side variant is
# right-censored: its NEVER_REACHED is a FALSE NEGATIVE, not a null result, and its delta of
# 0.0 is a FABRICATED ZERO (CLAUDE.md §3, research-loop-spec.md §6.5).
# Looser-side questions are TRACK B questions and are not answerable from this file.
# incumbent-exit source : data/bots_config_v2.csv   status: {cfg_status}
# censored cells        : {censored} of {total}   ({censored_pct}%)   blocked cells: {blocked}
# censoring UNKNOWN for : {unknown_bots}   -> every same-side cell BLOCKED
"""


# --- grouping + population filters -----------------------------------------
def _same_day(legs):
    """G-5 / D-12: a group is same-day (0DTE) iff every leg opened and closed on
    the same calendar day. Multi-day groups (OA-Mirror by construction) are
    excluded — pooling them blends pillars, which the 3-verdict contract forbids."""
    for r in legs:
        od, cd = (r["open_date"] or "")[:10], (r["close_date"] or "")[:10]
        if not od or od != cd:
            return False
    return True

def _group_status(legs):
    ss = set(r["status"] for r in legs if r["status"])
    if ss == {"closed"}:
        return "closed"
    if ss == {"expired"}:
        return "expired"
    return "mixed"


def compute_m_bot(rows, stamp_date):
    """M_bot_$ calibration — RULED 2026-08-07 (was OPEN-1/OPEN-2).
        * ONE-TIME (not rolling): computed once, at the stamp date.
        * median over POSITIONS of the position's $-credit (SUM of leg credit_$).
        * trailing 90 DAYS as of the stamp date.
        * SKIPPED before 90 days of history exist for that bot.
    Returns {bot: median_position_credit_$ or None}. None -> that bot's DSTOP is
    SKIPPED. No stamp date (the one-time stamp is a pre-registration decision, not
    yet made) -> {} -> DSTOP SKIPPED everywhere. DSTOP is credit-only, so debit
    positions never contribute."""
    if stamp_date is None:
        return {}
    win_start = stamp_date - datetime.timedelta(days=90)
    groups, earliest = {}, {}
    for r in rows:
        groups.setdefault((r["bot"], r["trade_id"]), []).append(r)
    per_bot = {}
    for (bot, tid), legs in groups.items():
        try:
            metrics = [leg_metrics(x) for x in legs]
        except Refusal:
            continue
        if any(m["sign"] != "credit" for m in metrics):
            continue
        odt, cdt = _dt(legs[0]["open_date"]), _dt(legs[0]["close_date"])
        if odt is None or cdt is None:
            continue
        earliest[bot] = min(earliest.get(bot, odt), odt)
        per_bot.setdefault(bot, []).append((cdt, sum(m["credit_d"] for m in metrics)))
    out = {}
    for bot, poss in per_bot.items():
        if (stamp_date - earliest[bot]).days < 90:      # SKIP: <90 days of history
            out[bot] = None
            continue
        window = [c for cdt, c in poss if win_start <= cdt <= stamp_date]
        out[bot] = statistics.median(window) if window else None
    return out


def _control_scan(rows):
    """⛔ D-7 — the engine self-test, over EVERY row (spec §3.5: 1,380/1,380). Recompute
    realised P/L from (credit-exit)×MULT×quantity, both sign classes. Independent of
    leg_metrics/the MULT guard (so a quantity corruption reaches CONTROL, per N-3) and
    independent of the same-day/MIN_N gate (a multi-day engine error must still abort).
    Returns (mismatches, worst_abs_residual)."""
    bad, worst = [], 0.0
    for r in rows:
        st = r["structure"]
        if st in CREDIT_STRUCTURES:
            sign = "credit"
        elif st in DEBIT_STRUCTURES:
            sign = "debit"
        else:
            continue                                  # unenumerated -> refused elsewhere (N-4)
        q, cr, ex, pnl = r["quantity"], r["credit"], r["exit_price"], r["pnl"]
        if None in (q, cr, ex, pnl):
            continue
        cf = (cr - ex) * MULT * q if sign == "credit" else (ex - cr) * MULT * q
        resid = abs(cf - pnl)
        worst = max(worst, resid)
        if resid > TOL_CONTROL:
            bad.append((r, cf))
    return bad, worst


def run(ledger, out, min_n=MIN_N, log_path=None, quiet=False, stamp_date=None):
    print(f"RESEARCH LOOP v{VERSION} (frozen {FROZEN_ON}, sha {self_hash()})  ⛔ DO-NOT-WIRE")
    if log_path is None:
        log_path = os.path.join(os.path.dirname(out) or ".", "research_log.md")

    if not os.path.exists(ledger):
        # build_ledger.py ALWAYS writes data/trades.csv, even at n=0, so a MISSING
        # file never means pre-Day-0 — it means the working directory is wrong.
        print(f"RESEARCH: ledger not found at {ledger} — working directory wrong? (build_ledger.py "
              f"writes it even at n=0). Nothing done, but this is NOT a clean pre-Day-0 state.")
        return 0

    raw_rows = list(csv.DictReader(open(ledger)))
    rows = [_normalize(r) for r in raw_rows]

    # ⛔ D-7 — CONTROL first, over every row, before any gate. A mismatch means THE
    # ENGINE IS WRONG; abort non-zero (spec §3.5) and print the offending fields.
    mism, worst_resid = _control_scan(rows)
    if mism:
        print(f"RESEARCH: !! {len(mism)} CONTROL_MISMATCH over {len(rows)} rows — THE ENGINE "
              f"IS WRONG. Ignore every number in this file.")
        for r, cf in mism[:20]:
            print(f"          {r['trade_id']} {r['structure']} qty={r['quantity']} "
                  f"credit={r['credit']} exit={r['exit_price']} cf_$={cf:.4f} pnl_$={r['pnl']}")
        return 1

    # group by trade_id (never iterate raw rows — R-6)
    groups = {}
    for r in rows:
        groups.setdefault(r["trade_id"] or f"__row{id(r)}", []).append(r)

    # population = same-day groups; count CLOSED positions for the MIN_N gate,
    # `expired` EXCLUDED (R-4/R-7).
    refusals = {}
    population, closed_positions, multiday = [], 0, 0
    for tid, legs in groups.items():
        if not _same_day(legs):
            multiday += 1
            continue
        gs = _group_status(legs)
        if gs == "mixed":
            refusals["mixed-status group (OPEN-4)"] = refusals.get("mixed-status group (OPEN-4)", 0) + 1
            continue
        population.append((tid, legs, gs))
        if gs == "closed":
            closed_positions += 1

    if closed_positions < min_n:
        line = (f"RESEARCH: suppressed — {closed_positions}/{min_n} closed positions "
                f"(same-day; expired excluded). Stage exercised, output withheld (spec §10/R-4).")
        print(line)
        _write_log(log_path, cfg_status="ABSENT (suppressed run)", records=[],
                   unknown_bots=[], nightly=line, suppressed=True)
        return 0

    # score (CONTROL already verified 0 mismatches above)
    records, bracket_rows = [], 0
    incumbent = load_incumbent_config()
    dstop_k = {name: param for name, fam, param, _ in VARIANTS if fam == "dstop"}
    m_bot = compute_m_bot(rows, stamp_date)     # {} until a one-time stamp date is set
    dstop_bots = sum(1 for v in m_bot.values() if v is not None)
    seen_bots = set()
    for tid, legs, gs in population:
        bot = legs[0]["bot"]
        seen_bots.add(bot)
        mb = m_bot.get(bot)
        dd = None if mb is None else {n: k * mb for n, k in dstop_k.items()}
        try:
            recs = list(eval_position(legs, incumbent=incumbent, dstop_dollars=dd))
        except Refusal as e:
            refusals[e.reason] = refusals.get(e.reason, 0) + 1
            continue
        records.extend(recs)
        if recs and recs[0]["bracket_violation"]:
            bracket_rows += 1

    # incumbent-exit status + censoring tallies for the header block
    unknown_bots = sorted(b for b in seen_bots if b not in incumbent)
    cfg_status = (f"PRESENT n={len(incumbent)} rows" if incumbent
                  else "ABSENT (0 usable per-bot incumbent rows -> all BLOCKED)")
    censored = sum(1 for r in records if r["verdict"] == "CENSORED")
    blocked  = sum(1 for r in records if r["verdict"] == "BLOCKED")
    numeric_delta = sum(1 for r in records if r["delta_R"] != "" and r["family"] != "control")

    # write counterfactuals.csv — APPEND, never clobber (D-13). Each run stamps its
    # engine_version/engine_hash so history of what produced a row survives.
    d = os.path.dirname(out)
    if d:
        os.makedirs(d, exist_ok=True)
    new_file = not os.path.exists(out)
    with open(out, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        if new_file:
            w.writeheader()
        w.writerows(records)

    # _meta.json receipt (execution_audit.py pattern, §6 step 7)
    meta_path = os.path.splitext(out)[0] + "_meta.json"
    with open(meta_path, "w") as f:
        json.dump({
            "engine_version": VERSION, "frozen_on": FROZEN_ON, "engine_sha256_16": self_hash(),
            "wired": False, "source": "GENERATOR — advisory only, never a reporting input",
            "closed_positions": closed_positions, "multiday_groups_excluded": multiday,
            "records": len(records), "control_mismatch": 0,
            "control_worst_residual_dollars": worst_resid,
            "censored_cells": censored, "blocked_cells": blocked,
            "cells_with_numeric_delta": numeric_delta, "bracket_violation_positions": bracket_rows,
            "refusals": refusals, "incumbent_config": cfg_status,
            "m_bot_calibration": (f"one-time median-POSITION $-credit, trailing 90d @ "
                                  f"{stamp_date.date()}, {dstop_bots} bots calibrated"
                                  if stamp_date else
                                  "NO STAMP DATE — DSTOP SKIPPED (one-time stamp is a "
                                  "pre-registration decision, RULED method 2026-08-07)"),
            "gate": "NOT RUN — descriptive only (§10a item 2); gate is GATED (OPEN-6/7, §8)",
        }, f, indent=2)
        f.write("\n")

    # descriptive nightly line — NO leaderboard, NO ranking (D-9), NO graduations.
    pt = [r for r in records if r["family"] == "pt"]
    pt_undec = sum(1 for r in pt if r["verdict"] == "UNDECIDABLE")
    pt_ss = sum(1 for r in pt if r["single_sided"])
    nightly = (
        f"RESEARCH: {closed_positions} positions x 12 variants.  "
        f"{censored} CENSORED, {blocked} BLOCKED, {numeric_delta} cells with a numeric delta.  "
        f"CENSORING: Track A is BLIND on the loose side for {len(unknown_bots)} of {len(seen_bots)} "
        f"bots (no incumbent-exit config).  PT decidable/undecidable: "
        f"{len(pt)-pt_undec}/{pt_undec}, single_sided {pt_ss} "
        f"(R: PT reported with mandatory split, descriptive-only — no gate reads it).  "
        f"NO GRADUATIONS (gate: n>=100 positions + 6mo + regime change, GATED). "
        f"{'NO CANDIDATES' if numeric_delta == 0 else ''}")
    print(nightly)

    _write_log(log_path, cfg_status=cfg_status, records=records,
               unknown_bots=unknown_bots, nightly=nightly, suppressed=False,
               censored=censored, blocked=blocked)
    return 0


def _write_log(path, cfg_status, records, unknown_bots, nightly, suppressed,
               censored=0, blocked=0):
    """research_log.md — APPEND only (D-13: never clobbered, never previously written).
    Each nightly entry opens with the censoring block VERBATIM (spec §4.2(1))."""
    total = len(records)
    block = CENSORING_BLOCK.format(
        cfg_status=cfg_status, censored=censored, total=total,
        censored_pct=round(100 * censored / total, 1) if total else 0,
        blocked=blocked, unknown_bots=", ".join(unknown_bots) or "(none)")
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    new = not os.path.exists(path)
    with open(path, "a") as f:
        if new:
            f.write("# research_log.md — Track A nightly log (APPEND-ONLY). "
                    "⛔ DO-NOT-WIRE; advisory only, never a reporting input.\n\n")
        f.write(f"## run engine v{VERSION} sha {self_hash()}\n\n")
        f.write("```\n" + block + "```\n\n")
        f.write(nightly + "\n\n")


# ===========================================================================
# --- REGRESSION HARNESS (spec §2.8, Gate B) --------------------------------
# Read-only over the two FROZEN v1 sources. NOT a reporting input (CLAUDE.md §3):
# v1 pre-cutover, demonstration only. Reproduces the re-run expectations exactly.
# ===========================================================================
EXPORT = os.path.join(DATA, "captures", "oa_export_positions_2026-07-30.csv")
LEDGER = os.path.join(DATA, "archive", "trades.csv")

def _load_norm(path):
    with open(path, newline="") as f:
        rd = csv.DictReader(f)
        rows = []
        for i, raw in enumerate(rd):
            raw.setdefault("__rowid__", f"R{i}")
            rows.append(_normalize(raw))
    return rows

def rerun():
    print(f"RESEARCH LOOP v{VERSION} — REGRESSION HARNESS  (v1 pre-cutover · demonstration only · "
          f"NOT a reporting input, CLAUDE.md §3)\n")
    results = []
    def check(label, got, want):
        ok = got == want
        results.append(ok)
        print(f"  {'PASS' if ok else 'FAIL'}  {label}: got {got}  want {want}")
    def note(label, val):
        print(f"  ----  {label}: {val}")

    # ---- EXPORT, same-day (the review's own base) ----
    ex = [r for r in _load_norm(EXPORT) if r["open_date"][:10] == r["close_date"][:10] and r["open_date"]]
    print(f"[EXPORT] {EXPORT.split('/')[-1]} — same-day rows: {len(ex)}")
    check("same-day n (review reproduces)", len(ex), 1254)
    sl100 = d50 = d75 = 0
    for r in ex:
        m = leg_metrics_safe(r)
        if m is None:
            continue
        if m["sign"] == "credit" and m["mae_pct"] is not None and m["mae_pct"] <= -1.0:
            sl100 += 1
        # units-corrected rejected RISK-basis probe (spec §2.8a): the units
        # regression probe, all structures, no clamp — MAE_$ <= -(param×risk_$)
        if m["MAE_d"] is not None and r["risk"] is not None:
            if m["MAE_d"] <= -(0.50 * r["risk"]): d50 += 1
            if m["MAE_d"] <= -(0.75 * r["risk"]): d75 += 1
    check("(a) DSTOP_50R rejected-risk probe fires", d50, 42)
    check("(a) DSTOP_75R rejected-risk probe fires", d75, 26)
    check("SL100 fires (credit structures)", sl100, 279)

    # ---- LEDGER (n=1,380 legs -> grouped) ----
    led = _load_norm(LEDGER)
    print(f"\n[LEDGER] {LEDGER.split('/')[-1]} — legs: {len(led)}")
    check("ledger legs", len(led), 1380)
    sl = {1.0: 0, 1.5: 0, 2.0: 0}; clamp = {1.0: 0, 1.5: 0, 2.0: 0}
    mae_gt = mfe_lt = bracket = mult_bad = mae_pos = mfe_neg = 0
    for r in led:
        m = leg_metrics_safe(r)
        if m is None:
            mult_bad += 1
            continue
        # G-7 domain: mae_pct<=0 false on 89, mfe_pct>=0 false on 30 (spec §2.3)
        if m["mae_pct"] is not None and m["mae_pct"] > 0: mae_pos += 1
        if m["mfe_pct"] is not None and m["mfe_pct"] < 0: mfe_neg += 1
        # D-17 bracket (all structures)
        if m["MAE_d"] is not None and m["MFE_d"] is not None:
            v1 = m["MAE_d"] > m["pnl"] + BRACKET_EPS
            v2 = m["MFE_d"] < m["pnl"] - BRACKET_EPS
            mae_gt += v1; mfe_lt += v2; bracket += (v1 or v2)
        # D-16 clamp guard: p×credit_$ > risk_$ over ALL rows (spec §2.6/§2.8e)
        for p in (1.0, 1.5, 2.0):
            if r["risk"] is not None and p * m["credit_d"] > r["risk"]:
                clamp[p] += 1
        if m["sign"] == "credit" and m["mae_pct"] is not None:
            for p in (1.0, 1.5, 2.0):
                if m["mae_pct"] <= -p:
                    sl[p] += 1
    check("(e) MULT identity holds on every row", mult_bad, 0)
    check("SL100/150/200 fire (credit, ledger)", (sl[1.0], sl[1.5], sl[2.0]), (316, 226, 192))
    check("(e) clamp guard binds p×credit_$>risk_$ (16/48/52)",
          (clamp[1.0], clamp[1.5], clamp[2.0]), (16, 48, 52))
    check("(D-17) bracket violations union", bracket, 291)
    note("bracket detail: MAE_$>pnl / MFE_$<pnl", f"{mae_gt} / {mfe_lt}")
    note("G-7 domain: mae_pct>0 / mfe_pct<0", f"{mae_pos} / {mfe_neg}")

    # ---- (d) no mean position ΔR near the gate margin; (c) DSTOP_100 ~ SL100 ----
    print()
    _rerun_positions(led, check, note)

    ok = sum(results); tot = len(results)
    print(f"\n  {ok}/{tot} regression checks passed   engine {VERSION} sha {self_hash()}")
    return 0 if ok == tot else 1


def leg_metrics_safe(r):
    try:
        return leg_metrics(r)
    except Refusal:
        return None


def _rerun_positions(led, check, note):
    """Group the ledger into positions and check §2.8(c)/(d): mean position ΔR must
    stay well inside the gate margin (|ΔR| < 0.10R is a units-bug tripwire), and the
    median-credit DSTOP_100 fire rate must sit near SL100's (calibration). Both
    DSTOP bases are printed WITHOUT certifying either (OPEN-2)."""
    groups = {}
    for r in led:
        groups.setdefault(r["trade_id"], []).append(r)
    sd = []
    for tid, legs in groups.items():
        if _same_day(legs) and _group_status(legs) == "closed":
            sd.append((tid, legs))

    # per-position ΔR with censoring OFF (raw arithmetic — this is the units check,
    # NOT a graduation; the nightly engine BLOCKS all of these).
    fam_deltas = {}
    for tid, legs in sd:
        try:
            recs = list(eval_position(legs, incumbent=None, dstop_dollars=None,
                                      apply_censoring=False))
        except Refusal:
            continue
        for rec in recs:
            if rec["family"] in ("control", "dstop"):
                continue
            if rec["delta_R"] != "":
                fam_deltas.setdefault(rec["variant"], []).append(float(rec["delta_R"]))
    worst = 0.0
    for v in SIGNED_NAMES:
        if v in fam_deltas and fam_deltas[v]:
            mean = statistics.mean(fam_deltas[v])
            worst = max(worst, abs(mean))
            note(f"mean position ΔR {v} (n={len(fam_deltas[v])})", f"{mean:+.4f}R")
    check("(d) no |mean position ΔR| >= 0.10R (units-bug tripwire)", worst < 0.10, True)

    # DSTOP_100 median-credit calibration vs SL100 (spec §2.8c). Compute the bot's
    # median $ credit on BOTH bases; print, certify NEITHER (OPEN-2).
    by_bot_leg, by_bot_pos = {}, {}
    for tid, legs in sd:
        for r in legs:
            m = leg_metrics_safe(r)
            if m and m["sign"] == "credit":
                by_bot_leg.setdefault(r["bot"], []).append(m["credit_d"])
        m0 = leg_metrics_safe(legs[0])
        if m0 and all(leg_metrics_safe(x) and leg_metrics_safe(x)["sign"] == "credit" for x in legs):
            by_bot_pos.setdefault(legs[0]["bot"], []).append(sum(leg_metrics_safe(x)["credit_d"] for x in legs))
    med_leg = {b: statistics.median(v) for b, v in by_bot_leg.items() if v}
    med_pos = {b: statistics.median(v) for b, v in by_bot_pos.items() if v}
    fired_leg = fired_pos = tot = 0
    for tid, legs in sd:
        bot = legs[0]["bot"]
        for r in legs:
            m = leg_metrics_safe(r)
            if not m or m["sign"] != "credit" or m["MAE_d"] is None:
                continue
            tot += 1
            if bot in med_leg and m["MAE_d"] <= -(1.0 * med_leg[bot]): fired_leg += 1
            if bot in med_pos and m["MAE_d"] <= -(1.0 * med_pos[bot]): fired_pos += 1
    if tot:
        note("(c) DSTOP_100 fire — leg-median basis", f"{fired_leg}/{tot} ({100*fired_leg/tot:.1f}%)")
        note("(c) DSTOP_100 fire — position-median basis", f"{fired_pos}/{tot} ({100*fired_pos/tot:.1f}%)")
        note("(c) SL100 fires near this (calibration holds if DSTOP_100 ~ SL100's 22-23%)", "see above")
    note("OPEN-2 UNSIGNED", "leg vs position median differ — the fixture certifies NEITHER")


# ===========================================================================
# --- VALIDATION FIXTURE (spec §5) ------------------------------------------
# Verbatim real rows loaded from data/archive/trades.csv with a pinned sha256 per
# raw line (drift between fixture and archive is LOUD). VALUE assertions in $ and R.
# ===========================================================================
# sha256(raw_line + "\n") for each fixture leg, keyed (trade_id, structure).
FIXTURE_SHA = {
    ("T00002", "shortcallspread"): "65e7494a585d8288fed8077c585f1698bc248963713113a63711993c0dc5544e",
    ("T00002", "shortputspread"):  "96204e5d58cb8105c517f6f83837749261b27874a0b7efbde015a580f043095e",
    ("T00012", "longcallspread"):  "e8b045dff03ba09ff6a5b28803636d9131fddda73563e7492c84eeb65ed33bbf",
    ("T00034", "ironcondor"):      "1d15b4f8a2af2c955000b3183cf703c45a81cabf43213344a870271c5303e635",
    ("T00083", "shortputspread"):  "b5cfffc34af1f3352a90006cf7a217c0ecf430a46804d4507539b78e95cbbe00",
    ("T00083", "shortcallspread"): "10f69776b61c974d188281d117eb9c4346d3850751a47f7114dd03f058ef2978",
    ("T00554", "ironcondor"):      "1f6f4d9e265d97d28525970c48fd6c59bd1a719bdbf5218882bb8e43d9ff7c1f",
    ("T00626", "ironcondor"):      "e05480b8dbec0b38b982266ae9d4b2f2e78a52fde559c96ac82176447d13ff51",
}

def _load_fixture(trade_ids):
    """Return {trade_id: [normalized legs]} loaded VERBATIM from the archive, with
    every raw line's sha256 checked against FIXTURE_SHA. Copy, do not transcribe."""
    with open(LEDGER, newline="") as f:
        raw = f.read().split("\n")
    header = raw[0]
    cols = next(csv.reader([header]))
    out, checked = {}, 0
    for line in raw[1:]:
        if not line:
            continue
        vals = next(csv.reader([line]))
        row = dict(zip(cols, vals))
        tid = row.get("trade_id")
        if tid not in trade_ids:
            continue
        key = (tid, (row.get("structure") or "").lower())
        want = FIXTURE_SHA.get(key)
        got = hashlib.sha256((line + "\n").encode()).hexdigest()
        if want is None:
            raise SystemExit(f"FIXTURE: unpinned row {key} — refuse to run on unverified data")
        if got != want:
            raise SystemExit(f"FIXTURE DRIFT: {key} sha {got} != pinned {want}")
        checked += 1
        out.setdefault(tid, []).append(_normalize(row))
    return out, checked


def _pos(legs, **kw):
    kw.setdefault("apply_censoring", False)   # value assertions test the ARITHMETIC
    return {r["variant"]: r for r in eval_position(legs, **kw)}


def validate():
    P = F = string_only = total = 0
    def check(label, got, want, string_verdict=False):
        nonlocal P, F, string_only, total
        ok = (abs(got - want) <= 0.01) if isinstance(got, float) and isinstance(want, float) else (got == want)
        P += ok; F += (not ok); total += 1; string_only += int(string_verdict)
        print(f"  {'PASS' if ok else 'FAIL'}  {label}" + ("" if ok else f"\n        got={got!r} want={want!r}"))

    fx, nchecked = _load_fixture({"T00002", "T00012", "T00034", "T00083", "T00554", "T00626"})
    print(f"  ({nchecked} verbatim archive rows verified byte-exact by sha256)\n")

    # ---------- F-1 · T00034 · the review's D-6 worked example (multi-day, OA-Mirror) ----------
    f1 = fx["T00034"]
    p1 = _pos(f1)
    r0 = f1[0]
    check("F1-a same-day filter REJECTS this multi-day position", _same_day(f1), False)
    m1 = leg_metrics(r0)
    check("F1-b credit_$ = 0.5×100×1", m1["credit_d"], 50.0)
    check("F1-c PT70 FILLED (raw, MFE 0.84>=0.70)", _pos(f1, apply_order_conflict=False)["PT70"]["verdict"], "FILLED")
    check("F1-d PT70 cf_$ = +35.00", _pos(f1, apply_order_conflict=False)["PT70"]["cf_pos_dollars"], 35.0)
    check("F1-e PT70 delta_$ = 0.00 EXACTLY", _pos(f1, apply_order_conflict=False)["PT70"]["delta_pos_dollars"], 0.0)
    check("F1-f PT60 cf_$ / delta_$ = +30.00 / -5.00",
          (_pos(f1, apply_order_conflict=False)["PT60"]["cf_pos_dollars"],
           _pos(f1, apply_order_conflict=False)["PT60"]["delta_pos_dollars"]), (30.0, -5.0))
    check("F1-g PT40 delta_$ = -15.00", _pos(f1, apply_order_conflict=False)["PT40"]["delta_pos_dollars"], -15.0)
    check("F1-h MAE_$ = -1.1×50 = -55.00", m1["MAE_d"], -55.0)
    check("F1-i SL150 NEVER_REACHED (-1.1 > -1.5)", p1["SL150"]["verdict"], "NEVER_REACHED", True)
    check("F1-j PT70 downgraded UNDECIDABLE/ORDER_CONFLICT (mae_date<mfe_date)", p1["PT70"]["verdict"], "UNDECIDABLE")
    check("F1-j' order_conflict flag set on PT70", p1["PT70"]["order_conflict"], True)

    # ---------- F-2 · T00554 · quantity witness (qty 192), same-day ----------
    f2 = fx["T00554"]; m2 = leg_metrics(f2[0]); p2 = _pos(f2)
    check("F2-a credit_$ = 0.5×100×192", m2["credit_d"], 9600.0)
    check("F2-b CONTROL cf_$ = 192.00 ±$0.01 (tolerance load-bearing)", p2["CONTROL"]["cf_pos_dollars"], 192.0)
    check("F2-b' CONTROL_OK", p2["CONTROL"]["verdict"], "CONTROL_OK")
    check("F2-c MAE_$ = -0.1×9600 = -960.00", m2["MAE_d"], -960.0)
    check("F2-d group size 1 -> risk_pos_$ 9600 / pnl_pos +192",
          (p2["CONTROL"]["risk_pos_dollars"], m2["pnl"]), (9600.0, 192.0))

    # ---------- F-2b · T00626 · large-quantity PT that FIRES ----------
    f2b = fx["T00626"]; m2b = leg_metrics(f2b[0]); p2b = _pos(f2b)
    check("F2b-a credit_$ = 0.31×100×144", m2b["credit_d"], 4464.0)
    check("F2b-b CONTROL cf_$ = 2304.00 = pnl", p2b["CONTROL"]["cf_pos_dollars"], 2304.0)
    check("F2b-c PT40 FILLED (0.5806>=0.40)", p2b["PT40"]["verdict"], "FILLED")
    check("F2b-d PT40 cf_$ = +1785.60", p2b["PT40"]["cf_pos_dollars"], 1785.6)
    check("F2b-e PT40 delta_$ = -518.40", p2b["PT40"]["delta_pos_dollars"], -518.4)
    check("F2b-f PT40 delta_R = -0.0521739", float(p2b["PT40"]["delta_R"]), -0.052174)
    check("F2b-g PT60 NEVER_REACHED (0.5806<0.60)", p2b["PT60"]["verdict"], "NEVER_REACHED", True)

    # ---------- F-3 · T00002 (BOTH legs) · position aggregation + dstop witness ----------
    f3 = fx["T00002"]
    assert len(f3) == 2, "F-3 must load both legs of T00002"
    p3 = _pos(f3)
    put = next(m for m in map(leg_metrics, f3) if m["structure"] == "shortputspread")
    check("F3-a put leg credit_$ = 0.35×100×10", put["credit_d"], 350.0)
    v_put, cf_put, _ = leg_variant(put, "CONTROL", "control", None)
    check("F3-b CONTROL cf_$ (put) = -1950.00, the only LOSER control", (round(cf_put, 2), v_put), (-1950.0, "CONTROL_OK"))
    check("F3-c risk_pos_$ = MAX(4650,4850) = 4850 (not 4650, not 9500)", p3["CONTROL"]["risk_pos_dollars"], 4850.0)
    check("F3-d pnl_pos_$ = -1850", sum(m["pnl"] for m in map(leg_metrics, f3)), -1850.0)
    check("F3-e credit_pos_$ = 500", sum(m["credit_d"] for m in map(leg_metrics, f3)), 500.0)
    # SL150 leg cf/delta on the put leg
    v150, cf150, _ = leg_variant(put, "SL150", "sl", 1.50)
    check("F3-f SL150 put-leg cf_$ / delta_$ = -525 / +1425", (round(cf150, 2), round(cf150 - put["pnl"], 2)), (-525.0, 1425.0))
    check("F3-g SL150 POSITION delta_R = +0.293814 (NOT +0.306452)", float(p3["SL150"]["delta_R"]), 0.293814)
    check("F3-h SL100 POSITION delta_R = +0.329897", float(p3["SL100"]["delta_R"]), 0.329897)
    # F3-i: DSTOP threshold INJECTED as $350 (not derived — the derivation is GATED).
    # cf_$=-350 and leg delta_$=+1600 are LEG-level (put leg), per the spec's wording.
    p3d = _pos(f3, dstop_dollars={"DSTOP_100": 350.0})
    vD, cfD, _ = leg_variant(put, "DSTOP_100", "dstop", 1.00, dstop_dollars=350.0)
    check("F3-i DSTOP D_$=350 put-leg FILLED, cf_$=-350", (vD, round(cfD, 2)), ("FILLED", -350.0))
    check("F3-i' DSTOP position delta_$ = +1600 (put +1600, call 0)", p3d["DSTOP_100"]["delta_pos_dollars"], 1600.0)
    check("F3-i''' DSTOP_100 position FILLED", p3d["DSTOP_100"]["verdict"], "FILLED")
    # F3-j: under the D-6 bug MAE_$ would be -1.95 (mae×per-contract-credit), silent
    check("F3-j buggy per-contract MAE (-1.95) would NOT fire the $350 stop", (put["mae_pct"] * put["credit_d"] / (MULT * put["quantity"])) > -350, True)
    check("F3-i'' DSTOP_100 SKIPPED when no M_bot_$ (no stamp / <90d history — RULED)", p3["DSTOP_100"]["verdict"], "SKIPPED")

    # ---------- M_bot_$ calibration (RULED 2026-08-07: one-time, median POSITION $-credit, trailing 90d) ----------
    def synth(bot, tid, credit, q, open_d, close_d):
        return _normalize({"bot": bot, "trade_id": tid, "structure": "shortputspread",
                           "status": "closed", "quantity": str(q), "credit": str(credit),
                           "exit_price": "0", "pnl": "0", "risk": "1000",
                           "premium": str(-credit * 100 * q), "mfe_pct": "0", "mae_pct": "0",
                           "open_date": open_d + " 10:00:00", "close_date": close_d + " 15:00:00"})
    stamp = _dt("2026-07-01 00:00:00")
    # bot with >90 days history: earliest position 2026-01-01, three in-window positions
    hist = [synth("BOT-A", "P1", 0.5, 10, "2026-01-01", "2026-01-01"),   # credit_$ 500 (out of window)
            synth("BOT-A", "P2", 0.3, 10, "2026-05-05", "2026-05-05"),   # 300 in window
            synth("BOT-A", "P3", 0.5, 10, "2026-06-01", "2026-06-01"),   # 500 in window
            synth("BOT-A", "P4", 0.7, 10, "2026-06-20", "2026-06-20")]   # 700 in window
    mb = compute_m_bot(hist, stamp)
    check("MB-1 M_bot_$ = median POSITION $-credit over trailing 90d (median[300,500,700]=500)", mb.get("BOT-A"), 500.0)
    # bot with <90 days history at the stamp -> SKIPPED (None)
    young = [synth("BOT-B", "Q1", 0.4, 10, "2026-06-01", "2026-06-01"),
             synth("BOT-B", "Q2", 0.6, 10, "2026-06-15", "2026-06-15")]
    check("MB-2 <90 days of history -> M_bot None (DSTOP SKIPPED for that bot)", compute_m_bot(young, stamp).get("BOT-B"), None)
    check("MB-3 no stamp date -> {} (one-time stamp is a pre-registration decision)", compute_m_bot(hist, None), {})

    # ---------- F-4 · T00083 (BOTH legs) · the stop that HURTS + COND negative ----------
    f4 = fx["T00083"]
    assert len(f4) == 2
    p4 = _pos(f4)
    call = next(m for m in map(leg_metrics, f4) if m["structure"] == "shortcallspread")
    vc, cfc, _ = leg_variant(call, "CONTROL", "control", None)
    check("F4-a CONTROL cf_$ (call) = +50.00, CONTROL_OK", (round(cfc, 2), vc), (50.0, "CONTROL_OK"))
    v2c, cf2c, _ = leg_variant(call, "SL200", "sl", 2.00)
    check("F4-b SL200 call-leg cf_$/delta_$ = -200/-250 (stop HURTS a recovered loser)", (round(cf2c, 2), round(cf2c - call["pnl"], 2)), (-200.0, -250.0))
    check("F4-c risk_pos_$ = MAX(4800,4900) = 4900", p4["SL200"]["risk_pos_dollars"], 4900.0)
    check("F4-d SL200 POSITION delta_R = -0.0510204", float(p4["SL200"]["delta_R"]), -0.051020)
    check("F4-e SL150 POSITION delta_$/delta_R = -600 / -0.1224490 (BOTH legs fire)", (p4["SL150"]["delta_pos_dollars"], float(p4["SL150"]["delta_R"])), (-600.0, -0.122449))
    check("F4-f COND_200_1400 NEVER_REACHED (mae<=-2 but trough 14:30 not <14:00)", p4["COND_200_1400"]["verdict"], "NEVER_REACHED", True)

    # ---------- F-5 · T00012 · the DEBIT-structure CONTROL branch ----------
    f5 = fx["T00012"]; m5 = leg_metrics(f5[0]); p5 = _pos(f5)
    check("F5-a CONTROL cf_$ = (2.9-6.9)×100×1 = -400, CONTROL_OK", (p5["CONTROL"]["cf_pos_dollars"], p5["CONTROL"]["verdict"]), (-400.0, "CONTROL_OK"))
    check("F5-b credit identity here would give +400 -> MISMATCH", round((m5["credit_d"] - f5[0]["exit_price"] * MULT * f5[0]["quantity"]), 2), 400.0)
    check("F5-c risk_$ = 690 == credit_$ (R basis collapses to credit)", (m5["risk"], m5["credit_d"]), (690.0, 690.0))
    check("F5-d SL100/150/200 = N/A — structure, never NEVER_REACHED",
          (p5["SL100"]["verdict"], p5["SL150"]["verdict"], p5["SL200"]["verdict"]),
          ("N/A — structure", "N/A — structure", "N/A — structure"), True)

    # ---------- N-1 … N-4 · negative controls (§3.4) ----------
    print()
    base = dict(zip(next(csv.reader([open(LEDGER).readline().strip()])),
                    next(csv.reader([_raw_line("T00034")]))))
    def run_tmp(mutation):
        import tempfile
        row = dict(base); row.update(mutation)
        # T00034 is one closed ironcondor; give run() min_n=0 so CONTROL is exercised.
        fd, path = tempfile.mkstemp(suffix=".csv"); os.close(fd)
        outfd, outp = tempfile.mkstemp(suffix=".csv"); os.close(outfd)
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(base.keys())); w.writeheader(); w.writerow(row)
        rc = run(path, outp, min_n=0, log_path=os.path.splitext(outp)[0] + "_log.md", quiet=True)
        for p in (path, outp, os.path.splitext(outp)[0] + "_meta.json", os.path.splitext(outp)[0] + "_log.md"):
            if os.path.exists(p): os.remove(p)
        return rc
    check("N-1 pnl->9999 -> CONTROL_MISMATCH, run() exits non-zero", run_tmp({"pnl": "9999"}) != 0, True)
    check("N-2 exit_price->99 -> CONTROL_MISMATCH (corrupts a recompute input)", run_tmp({"exit_price": "99"}) != 0, True)
    check("N-3 quantity->100 -> CONTROL_MISMATCH (the only ×quantity check inside CONTROL)", run_tmp({"quantity": "100"}) != 0, True)
    n4 = list(_safe_eval({**base, "structure": "calendar"}))
    check("N-4 structure=calendar -> REFUSED (no verdict emitted)", n4, [])

    # ---------- E-1 … E-4 · end-to-end + boundary ----------
    print()
    _e_tests(check)

    # ---------- V-0 · variant-list assertion ----------
    check("V-0 variant list == signed twelve, verbatim and in order", [v[0] for v in VARIANTS], SIGNED_NAMES)

    # ---------- D-8 · the absence-of-coverage assertions (§4.2 items 5-6) ----------
    print()
    print("  SKIP  D-8 CENSORING: NOT COVERED BY ANY FIXTURE — unobservable from historical rows.")
    print("        Blocked on data/bots_config_v2.csv (no usable per-bot incumbent-exit row; the")
    print("        signature is an 81%->0% distributional collapse across bots, spec §4.1).")
    # the testable tripwire: no incumbent config -> every PT and SL cell BLOCKED, never FILLED
    ptsl_blocked = all(
        _pos(fx["T00554"], apply_censoring=True, incumbent={})[v]["verdict"] == "BLOCKED"
        for v in ("PT40", "PT60", "PT70", "SL100", "SL150", "SL200"))
    check("D-8 tripwire: no config -> PT/SL BLOCKED (not FILLED, not NEVER_REACHED)", ptsl_blocked, True)
    check("D-8 tripwire: BLOCKED cells carry NO numeric delta",
          all(_pos(fx["T00554"], apply_censoring=True, incumbent={})[v]["delta_R"] == ""
              for v in ("PT40", "SL100")), True)

    # ---------- the DO-NOT-WIRE mechanical guard (§4.2 item 6, Gate A) ----------
    daily = os.path.join(ROOT, "scripts", "daily.sh")
    content = open(daily).read()
    wired = os.path.exists(daily) and any(
        "research_loop" in line and "python3" in line
        for line in content.splitlines()
        if not line.strip().startswith("#") and not line.strip().startswith("echo")
    )
    check("DO-NOT-WIRE: research_loop.py is absent from scripts/daily.sh", wired, False)

    # ---------- fixture self-audit: verdict-string-only share < 15% (§7 Gate A) ----------
    pct = round(100 * string_only / total, 1)
    print(f"\n  verdict-string-only assertions: {string_only}/{total} ({pct}%)  "
          f"(old fixture 21/23 = 91%; target < 15%)")
    if pct >= 15:
        print("  ⚠️  FAIL: too many verdict-string-only checks — units errors slip a string-only fixture.")
        F += 1

    print(f"\n  {P}/{P+F} passed   engine {VERSION} sha {self_hash()}")
    return 1 if F else 0


def _raw_line(trade_id):
    with open(LEDGER) as f:
        for line in f:
            parts = line.split(",")
            if len(parts) > 5 and parts[5] == trade_id:
                return line.rstrip("\n")
    raise SystemExit(f"raw line {trade_id} not found")


def _safe_eval(row):
    """Yield eval_position records, or nothing if the group is Refused (N-4)."""
    try:
        yield from eval_position([_normalize(row)], apply_censoring=False)
    except Refusal:
        return


def _e_tests(check):
    import tempfile
    with open(LEDGER, newline="") as f:
        lines = f.read().split("\n")
    header = lines[0]
    cols = next(csv.reader([header]))

    # E-1: 30 verbatim CONSECUTIVE rows (archive lines 2-31) — includes debit
    # (T00011/T00012), losers, quantity>1. run() with min_n=0 must complete, write
    # both files, 0 CONTROL_MISMATCH.
    block = lines[1:31]
    fd, path = tempfile.mkstemp(suffix=".csv"); os.close(fd)
    with open(path, "w") as f:
        f.write(header + "\n" + "\n".join(block) + "\n")
    outfd, outp = tempfile.mkstemp(suffix=".csv"); os.close(outfd)
    logp = os.path.splitext(outp)[0] + "_log.md"
    rc = run(path, outp, min_n=0, log_path=logp, quiet=True)
    wrote_both = os.path.exists(outp) and os.path.exists(logp)
    check("E-1 run() over 30 verbatim rows: completes rc=0", rc, 0)
    check("E-1' writes BOTH counterfactuals.csv and research_log.md", wrote_both, True)
    for p in (path, outp, logp, os.path.splitext(outp)[0] + "_meta.json"):
        if os.path.exists(p): os.remove(p)

    # E-2/E-3/E-4: build temp ledgers of N CLOSED positions (+ expired) to test the
    # position-counted MIN_N gate and expired EXCLUSION.
    groups = {}
    for line in lines[1:]:
        if not line: continue
        vals = next(csv.reader([line]))
        row = dict(zip(cols, vals))
        groups.setdefault(row["trade_id"], []).append((line, row))
    closed = [(t, g) for t, g in groups.items()
              if all(r["status"] == "closed" for _, r in g)
              and all(r["open_date"][:10] == r["close_date"][:10] for _, r in g)]
    expired = [(t, g) for t, g in groups.items()
               if all(r["status"] == "expired" for _, r in g)
               and all(r["open_date"][:10] == r["close_date"][:10] for _, r in g)]

    def build(nclosed, nexp):
        picked = []
        for _, g in closed[:nclosed]:
            picked += [ln for ln, _ in g]
        for _, g in expired[:nexp]:
            picked += [ln for ln, _ in g]
        fd, p = tempfile.mkstemp(suffix=".csv"); os.close(fd)
        with open(p, "w") as f:
            f.write(header + "\n" + "\n".join(picked) + "\n")
        return p

    def emits(nclosed, nexp):
        p = build(nclosed, nexp)
        outfd, outp = tempfile.mkstemp(suffix=".csv"); os.close(outfd)
        logp = os.path.splitext(outp)[0] + "_log.md"
        if os.path.exists(outp): os.remove(outp)
        run(p, outp, min_n=30, log_path=logp, quiet=True)
        emitted = os.path.exists(outp)
        for q in (p, outp, logp, os.path.splitext(outp)[0] + "_meta.json"):
            if os.path.exists(q): os.remove(q)
        return emitted

    check("E-2 29 closed positions -> suppressed, emits nothing", emits(29, 0), False)
    check("E-3 30 closed positions -> emits", emits(30, 0), True)
    check("E-4 29 closed + 5 expired -> suppressed (expired don't count)", emits(29, 5), False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Track A counterfactual generator (DO-NOT-WIRE).")
    ap.add_argument("--ledger", default=os.path.join(DATA, "trades.csv"))
    ap.add_argument("--out", default=os.path.join(DATA, "counterfactuals.csv"))
    ap.add_argument("--validate", action="store_true", help="run the §5 fixture set")
    ap.add_argument("--rerun", action="store_true", help="regression harness over the frozen v1 capture (§2.8)")
    ap.add_argument("--stamp-date", default=None,
                    help="YYYY-MM-DD one-time M_bot_$ calibration stamp (pre-registration decision). "
                         "Absent -> DSTOP SKIPPED (RULED method 2026-08-07).")
    a = ap.parse_args()
    if a.validate:
        sys.exit(validate())
    if a.rerun:
        sys.exit(rerun())
    stamp = _dt((a.stamp_date + " 00:00:00")) if a.stamp_date else None
    sys.exit(run(a.ledger, a.out, stamp_date=stamp))
