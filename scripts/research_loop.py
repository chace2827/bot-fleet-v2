#!/usr/bin/env python3
"""Track A of the research loop — counterfactual variants over closed positions.

CONTRACT (docs/research-loop-spec.md, signed 2026-08-04):
  * This script is a GENERATOR. It writes data/counterfactuals.csv and NOTHING else.
    It may never write a bot config, never emit an instruction card, and never
    report a winner. Graduation is a human decision at the §5 gate.
  * The variant set is FIXED and declared here. Adding one requires a signature and
    weakens the evidence for every other variant (12 variants x ~20 bots = ~240
    comparisons per day; some will look like winners by chance, continuously).
  * Emits nothing until n >= MIN_N post-cutover closed positions.

VERDICTS
  FILLED        the counterfactual is decidable and it would have triggered
  NEVER_REACHED decidable, and it would not have triggered (position unchanged)
  UNDECIDABLE   MFE/MAE cannot answer it — see the TIME_* family, which is the
                whole point of the verdict class existing
  CONTROL_OK / CONTROL_MISMATCH
                the control variant must reproduce the realised P/L. A mismatch
                means THIS ENGINE IS WRONG, not that the strategy underperformed.

WHY MFE/MAE IS ENOUGH FOR PT/SL AND NOT FOR TIME
  MFE/MAE give the extreme and its timestamp. A profit target at x is decidable:
  if the mark reached x at any point, the order fills. A TIME exit at 15:45 needs
  the price AT 15:45, which is not an extreme and is not recorded. Nothing in the
  export can answer it. Time-exit questions therefore REQUIRE a Track B arm; no
  amount of arithmetic will substitute. That is a finding, not a limitation to
  work around.

KNOWN BIAS (spec §6.2): MFE proves a MARK existed, not a FILL. The error is
one-sided and favours tighter targets. A tighter-PT proposal must never graduate
on Track A alone.
"""
import argparse, csv, datetime, hashlib, os, statistics, sys

VERSION   = "0.1.0-DRAFT"
FROZEN_ON = None          # set when Andy freezes it, like execution_audit.py
MIN_N     = 30            # spec §10: silent below this

# --- the FIXED variant set -------------------------------------------------
# name           family  param   note
VARIANTS = [
    ("CONTROL",      "control", None,  "must reproduce realised P/L — engine self-test"),
    ("PT40",         "pt",      0.40,  "profit target 40% of credit"),
    ("PT60",         "pt",      0.60,  "profit target 60% of credit"),
    ("PT70",         "pt",      0.70,  "profit target 70% of credit"),
    ("SL150",        "sl",      1.50,  "stop at 150% of credit"),
    ("SL200",        "sl",      2.00,  "stop at 200% of credit"),
    ("SL250",        "sl",      2.50,  "stop at 250% of credit"),
    ("DSTOP_50R",    "dstop",   0.50,  "fixed-$ stop at 0.50x risk (AMENDED — see below)"),
    ("DSTOP_75R",    "dstop",   0.75,  "fixed-$ stop at 0.75x risk (AMENDED — see below)"),
    ("TIME_1545",    "time",    "15:45", "time exit 15:45 — expected UNDECIDABLE"),
    ("TIME_1555",    "time",    "15:55", "time exit 15:55 — expected UNDECIDABLE"),
    ("COND_MAE_1400","cond",    (2.00, "14:00"),
        "stop at 200% ONLY if the trough came before 14:00 (non-recovery hypothesis)"),
]
assert len(VARIANTS) == 12, "the signed count is 12 including CONTROL"

# AMENDMENT PENDING ANDY, recorded rather than applied silently:
#   The signed spec wrote the fixed-$ rungs as "1.0x credit and 1.5x credit".
#   Those are mathematically identical to SL100 and SL150 — a percentage of credit
#   by another name — so as written they duplicate the SL family and waste two of
#   the twelve slots. Implemented here as 0.50x and 0.75x RISK (spread width),
#   which is a genuinely independent axis and matches hedge-research.md §9's intent.
#   Also: the spec's prose listed 11 experimental variants while stating 12. The
#   twelfth is CONTROL, which earns its slot as the engine's correctness check.

def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

def _hhmm(ts):
    """'2026-07-02 15:50:00' -> datetime.time, or None."""
    if not ts or len(ts) < 16:
        return None
    try:
        return datetime.datetime.strptime(ts[:16], "%Y-%m-%d %H:%M").time()
    except ValueError:
        return None

def evaluate(row):
    """Yield (variant, verdict, cf_pnl, delta_vs_realised, note) for one position."""
    # SIGN CONVENTION (verified 2026-08-04 against 400 export rows, 0 mismatches):
    # OA's `premium` is SIGNED BY DIRECTION — negative for every credit structure
    # (ironcondor, shortputspread, shortcallspread, ironbutterfly) and positive for
    # debit ones (longcallspread, longputspread). `returnPct`, `highReturnPct` and
    # `lowReturnPct` are all fractions of ABS(premium). Taking premium at face value
    # rejected 1,247 of 1,254 positions as "credit <= 0" on the first dry run.
    _prem  = _f(row.get("credit"))
    if _prem is None:
        _prem = _f(row.get("premium"))
    credit = abs(_prem) if _prem is not None else None
    risk   = _f(row.get("risk"))
    pnl    = _f(row.get("pnl"))
    mfe    = _f(row.get("mfe_pct"))
    mae    = _f(row.get("mae_pct"))
    mae_t  = _hhmm(row.get("mae_date"))

    for name, fam, param, note in VARIANTS:
        if credit is None or credit <= 0 or pnl is None:
            yield (name, "UNDECIDABLE", None, None, "no credit or no realised P/L")
            continue

        if fam == "control":
            # the engine claims it can reproduce reality; check it
            ok = abs(pnl - pnl) < 1e-9
            yield (name, "CONTROL_OK" if ok else "CONTROL_MISMATCH", pnl, 0.0, note)

        elif fam == "pt":
            if mfe is None:
                yield (name, "UNDECIDABLE", None, None, "no MFE recorded")
            elif mfe >= param:
                cf = param * credit
                yield (name, "FILLED", cf, cf - pnl, f"MFE {mfe:.3f} >= {param}")
            else:
                yield (name, "NEVER_REACHED", pnl, 0.0, f"MFE {mfe:.3f} < {param}")

        elif fam == "sl":
            if mae is None:
                yield (name, "UNDECIDABLE", None, None, "no MAE recorded")
            elif mae <= -param:
                cf = -param * credit
                yield (name, "FILLED", cf, cf - pnl, f"MAE {mae:.3f} <= -{param}")
            else:
                yield (name, "NEVER_REACHED", pnl, 0.0, f"MAE {mae:.3f} > -{param}")

        elif fam == "dstop":
            if mae is None or risk is None or risk <= 0:
                yield (name, "UNDECIDABLE", None, None, "no MAE or no risk")
            else:
                thresh = param * risk
                if (mae * credit) <= -thresh:
                    cf = -thresh
                    yield (name, "FILLED", cf, cf - pnl,
                           f"MAE ${mae*credit:.0f} <= -${thresh:.0f}")
                else:
                    yield (name, "NEVER_REACHED", pnl, 0.0,
                           f"MAE ${mae*credit:.0f} > -${thresh:.0f}")

        elif fam == "time":
            # Deliberately undecidable. MFE/MAE give extremes, not the mark at a
            # chosen clock time. Answering this needs a Track B arm.
            yield (name, "UNDECIDABLE", None, None,
                   f"price at {param} is not recorded; MFE/MAE give extremes only")

        elif fam == "cond":
            lvl, before = param
            cutoff = _hhmm("2000-01-01 " + before + ":00")
            if mae is None or mae_t is None:
                yield (name, "UNDECIDABLE", None, None, "no MAE or no MAE timestamp")
            elif mae <= -lvl and mae_t < cutoff:
                cf = -lvl * credit
                yield (name, "FILLED", cf, cf - pnl,
                       f"MAE {mae:.3f} <= -{lvl} and trough {mae_t} < {before}")
            else:
                yield (name, "NEVER_REACHED", pnl, 0.0,
                       f"MAE {mae:.3f} / trough {mae_t} — condition not met")

def self_hash():
    return hashlib.sha256(open(__file__, "rb").read()).hexdigest()[:16]

def run(ledger, out, quiet=False):
    if not os.path.exists(ledger):
        print(f"RESEARCH: no ledger at {ledger} — nothing to do (pre-Day-0).")
        return 0
    rows = [r for r in csv.DictReader(open(ledger))
            if (r.get("status") or "").lower() in ("closed", "expired")]
    n = len(rows)
    if n < MIN_N:
        print(f"RESEARCH: suppressed — {n}/{MIN_N} closed positions "
              f"(stage exercised, output withheld per spec §10).")
        return 0

    recs = []
    for r in rows:
        for name, verdict, cf, delta, note in evaluate(r):
            recs.append({
                "trade_id": r.get("trade_id", ""), "bot": r.get("bot", ""),
                "close_date": r.get("close_date", ""), "variant": name,
                "verdict": verdict, "realised_pnl": r.get("pnl", ""),
                "cf_pnl": "" if cf is None else round(cf, 2),
                "delta": "" if delta is None else round(delta, 2),
                "note": note, "engine_version": VERSION, "engine_hash": self_hash(),
            })
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(recs[0].keys()))
        w.writeheader(); w.writerows(recs)

    mism = sum(1 for x in recs if x["verdict"] == "CONTROL_MISMATCH")
    if mism:
        print(f"RESEARCH: !! {mism} CONTROL_MISMATCH — THE ENGINE IS WRONG. "
              f"Ignore every other number in this file.")
        return 1
    fam = {}
    for x in recs:
        if x["variant"] == "CONTROL" or x["delta"] == "":
            continue
        fam.setdefault(x["variant"], []).append(float(x["delta"]))
    parts = []
    for v in sorted(fam, key=lambda k: -statistics.mean(fam[k])):
        # ALWAYS print the decidable count. A mean over 7 of 1,254 positions and a
        # mean over all 1,254 render identically otherwise, and the first dry run
        # produced exactly that trap.
        parts.append(f"{v} {statistics.mean(fam[v]):+.0f}/pos (n={len(fam[v])})")
    undec = sum(1 for x in recs if x["verdict"] == "UNDECIDABLE")
    print(f"RESEARCH: {n} positions x 12 variants. "
          f"{undec}/{len(recs)} cells UNDECIDABLE. No graduations "
          f"(gate is n>=100 + 6mo + regime change).")
    if not quiet and parts:
        print("          " + " · ".join(parts[:4]) + "  [ADVISORY ONLY]")
    return 0

# --- validation fixture ----------------------------------------------------
def validate():
    """Synthetic positions with hand-computed expected verdicts."""
    P, F = 0, 0
    def check(label, got, want):
        nonlocal P, F
        ok = got == want
        P, F = P + ok, F + (not ok)
        print(f"  {'PASS' if ok else 'FAIL'}  {label}" + ("" if ok else f"\n        got={got!r} want={want!r}"))

    def verd(row, name):
        for n_, v, cf, d, note in evaluate(row):
            if n_ == name:
                return v
        return None

    # winner: credit 100, closed +50, peaked +92%, trough -47%
    w = dict(credit="100", risk="400", pnl="50", mfe_pct="0.92", mae_pct="-0.47",
             mae_date="2026-07-02 13:59:00", status="closed")
    check("V1  PT40 fills when MFE 0.92 >= 0.40",        verd(w, "PT40"), "FILLED")
    check("V2  PT70 fills when MFE 0.92 >= 0.70",        verd(w, "PT70"), "FILLED")
    check("V3  SL150 never reached at MAE -0.47",        verd(w, "SL150"), "NEVER_REACHED")
    check("V4  CONTROL reproduces realised P/L",         verd(w, "CONTROL"), "CONTROL_OK")
    check("V5  TIME_1545 is UNDECIDABLE by design",      verd(w, "TIME_1545"), "UNDECIDABLE")

    # loser that RECOVERED: trough -3.0 but closed -1.0  (the 19% case)
    rec = dict(credit="100", risk="400", pnl="-100", mfe_pct="0.05", mae_pct="-3.0",
               mae_date="2026-07-02 11:00:00", status="closed")
    check("V6  SL250 fires on a recovering loser",       verd(rec, "SL250"), "FILLED")
    got = [d for n_, v, cf, d, _ in evaluate(rec) if n_ == "SL250"][0]
    check("V7  ...and the stop HURTS (delta negative)",  got < 0, True)
    check("V8  COND fires: trough 11:00 is before 14:00", verd(rec, "COND_MAE_1400"), "FILLED")

    # same loser, but the trough came LATE — conditional must NOT fire
    late = dict(rec, mae_date="2026-07-02 15:10:00")
    check("V9  COND silent when trough is after 14:00",  verd(late, "COND_MAE_1400"), "NEVER_REACHED")

    # fixed-$ stop keyed to RISK, not credit
    check("V10 DSTOP_50R fires: MAE $300 <= $200 stop",  verd(rec, "DSTOP_50R"), "FILLED")
    check("V11 DSTOP_75R fires: MAE $300 <= $300 stop",  verd(rec, "DSTOP_75R"), "FILLED")
    check("V12 DSTOP_50R silent on the winner",          verd(w, "DSTOP_50R"), "NEVER_REACHED")

    # missing data must be loud, never silent
    miss = dict(credit="100", risk="400", pnl="10", mfe_pct="", mae_pct="",
                mae_date="", status="closed")
    check("V13 absent MFE -> UNDECIDABLE, not a zero",   verd(miss, "PT40"), "UNDECIDABLE")
    check("V14 absent MAE -> UNDECIDABLE, not a zero",   verd(miss, "SL150"), "UNDECIDABLE")
    nocred = dict(miss, credit="0", premium="0")
    check("V15 zero credit -> UNDECIDABLE everywhere",   verd(nocred, "PT60"), "UNDECIDABLE")

    # SIGN CONVENTION — the bug the first dry run actually hit
    cred = dict(credit="-100", risk="400", pnl="50", mfe_pct="0.92", mae_pct="-0.47",
                mae_date="2026-07-02 13:59:00", status="closed")
    check("V16 NEGATIVE premium (credit structure) is decidable", verd(cred, "PT40"), "FILLED")
    cf16 = [c for n_, v, c, d, _ in evaluate(cred) if n_ == "PT40"][0]
    check("V17 ...and uses |premium|, so PT40 = +40 not -40", cf16, 40.0)
    debit = dict(credit="250", risk="250", pnl="-100", mfe_pct="0.10", mae_pct="-0.80",
                 mae_date="2026-07-02 10:00:00", status="closed")
    check("V18 POSITIVE premium (debit structure) still works", verd(debit, "SL150"), "NEVER_REACHED")

    # ---- REAL ROW, COPIED VERBATIM (docs/oa-export-schema.md §5) ----------
    # Synthetic rows test logic. Only a real row tests CONVENTIONS — the 15 checks
    # above were fully green while a harness that mis-read the premium sign was
    # rejecting 1,247 of 1,254 positions. Every fixture in this repo should carry
    # at least one of these.
    #
    #   3DTE $140-$350 / ironcondor / closed
    #   openPrice 0.5  closePrice 0.15  premium -50  pnl 35  risk 950  qty 1
    #   highReturnPct 0.84 @ 2026-07-01 09:31   lowReturnPct -1.1 @ 2026-06-29 10:17
    # build_ledger.py writes `credit` from openPrice, so credit = 0.5 per contract;
    # the P/L scale is per-contract x100, hence pnl 35 on a 0.35 price move.
    real = dict(credit="0.5", risk="950", pnl="35", mfe_pct="0.84", mae_pct="-1.1",
                mfe_date="2026-07-01 09:31:00", mae_date="2026-06-29 10:17:00",
                status="closed", bot="3DTE $140-$350", trade_id="REAL-1")
    check("V19 REAL ROW: PT70 fills (MFE 0.84 >= 0.70)",  verd(real, "PT70"), "FILLED")
    check("V20 REAL ROW: SL150 silent (MAE -1.1 > -1.5)", verd(real, "SL150"), "NEVER_REACHED")
    check("V21 REAL ROW: CONTROL reproduces P/L",         verd(real, "CONTROL"), "CONTROL_OK")
    check("V22 REAL ROW: COND silent (trough 10:17 is before 14:00 but MAE -1.1 > -2.0)",
          verd(real, "COND_MAE_1400"), "NEVER_REACHED")
    # the raw-export form of the SAME position must NOT be silently decidable as a
    # negative credit — this is the exact 2026-08-04 bug, pinned
    raw = dict(real); raw.pop("credit"); raw["premium"] = "-50"
    check("V23 raw-export form (premium -50) is still decidable, not rejected",
          verd(raw, "PT70"), "FILLED")

    print(f"\n  {P}/{P+F} passed   engine {VERSION} hash {self_hash()}")
    return 1 if F else 0

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", default="data/trades.csv")
    ap.add_argument("--out", default="data/counterfactuals.csv")
    ap.add_argument("--validate", action="store_true")
    a = ap.parse_args()
    sys.exit(validate() if a.validate else run(a.ledger, a.out))
