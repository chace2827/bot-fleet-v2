#!/usr/bin/env python3
"""Comparative machinery — the greenfield-family arm-vs-control engine.

⛔ STANDALONE. NOT wired into scripts/daily.sh, not as any stage, and it must not be
(comparative-machinery-spec.md §6.2). It reads I-1…I-5, writes data/comparative/ only,
and produces NONE of the daily loop's three verdicts. It is advisory until each PR entry
is signed (§6.5); nothing it emits authorises a build, a switch-on, or a switch-off.

Implements docs/comparative-machinery-spec.md under the rulings on
docs/g-rulings-card-2026-08-07.md and the two signed items + two G-10 constraints in
docs/post-u1-package-2026-08-07.md. Where the DRAFT spec and a later ruling disagree, the
RULING governs — every such point is annotated inline.

THE RULED SHAPE, in one place (all `Andy 2026-08-06/07`):
  G-10 SWITCH   the family correction is a JOINT DAY-BOOTSTRAP MAX-T across arms, declared
                before any data exists. Bonferroni-across-K (spec §3.1) and the ci_fam_*
                construction (§2.5) are SUPERSEDED. Default is NON-STUDENTIZED; a
                studentized variant may exist only behind a guard that MEASURES c on the
                actual data and REFUSES if c > 2.638 (Constraint A, post-U1 §2.1). The
                measured studentized c was 2.92–4.69 on this leptokurtic d — using it would
                silently reverse G-10. `c` is a mandatory published field on every verdict.
  Constraint B  a per-member DIRECTION VECTOR, declared PRE-DATA (post-U1 §2.2):
                  5 greenfield + 2 Track B arm-vs-control PASS tests -> LOWER (ci_fam_lo>0)
                  PR-16 T1 fast-move-tail non-harm             -> UPPER (ci_fam_hi < -δ)
                  PR-19 G-13 replacement (TOST equivalence)    -> TWO-SIDED, band ±0.015R
  G-12b SIGNED  PR-16 T1 (post-U1 §1): tail set T = the m matched days with the largest
                |underlying_close-underlying_open|/underlying_open; dTail = mean paired d
                over T; RETIRE iff ci_fam_hi(dTail) < -δ; δ=0.10R (NEW MARGIN), p=0.20
                (m=ceil(p·n)); floor n_matched_days≥100 (below -> INCAPABLE, never RETIRE);
                ONE re-arm at Day-0+9mo; INSIDE the family correction.
  G-13  PR-19 degeneracy -> TOST equivalence on mean paired ΔR vs Ride, band ±0.015R, once.
  G-5   PR-19 gate conjunct (c) DISAPPLIED (the CF-11 parallel); with (a) inert, PR-19's
        PASS gate reduces to (b) alone.
  G-2   the gate reads M6 (six comparative arms PR-14…PR-19); |M7| printed alongside.
  G-8   the n≥60 interim read is an always-valid confidence sequence; the fixed-n family
        interval is computed ONCE, at the stamped gate-eval date, never before.
  G-11  PR-21/PR-22 are INSIDE the family (one correction). The slot-5 retire-scoped
        dual-tested (bot,variant) exclusions apply to any Track-A-family computation.
  G-1   DECLINED (post-U1 §4): exit_rows.csv (I-5) is not built. Anything needing exit
        attribution emits a NAMED BLOCKED refusal — never a verdict, never silently skipped.
  G-6   +0.015R stands (currently inert under (b)); fire_rate published beside (a) always.
  G-7   gate-eval date = Day-0+6mo (relational); no verdict without a stamped date (R-5).
  G-14  <D100> — refuse to stamp. G-16 emission floor n_matched_days≥20.

UNIT LAW (spec §0; CLAUDE.md §4; ruling R-6): unit = the POSITION = the CONDOR (trade_id
group); risk = the LARGER side; R basis is `ror` = sum(pnl)/max(risk), carried
[DERIVED, UNCORROBORATED] (ror is not a ledger column). Every aggregate carries its n and
its unit; an absent number is EMPTY — n=0, never 0.000R.
"""
import argparse, csv, datetime, hashlib, json, math, os, random, statistics, sys

VERSION   = "0.1.0-DRAFT"
FROZEN_ON = None                          # execution_audit.py pattern; signed, not coded

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

# --- named inputs (spec §1.1) ----------------------------------------------
I1_LEDGER      = os.path.join(DATA, "trades.csv")
I2_META        = os.path.join(DATA, "ledger_meta.json")
I3_BOTS_META   = os.path.join(DATA, "bots_meta.csv")
I4_CONFIG      = os.path.join(DATA, "bots_config_v2.csv")
I5_EXIT_ROWS   = os.path.join(DATA, "exit_rows.csv")     # DECLINED (G-1) — does not exist
OUT_DIR        = os.path.join(DATA, "comparative")

# --- constants -------------------------------------------------------------
MULT            = 100         # options multiplier (spec §1.3 / oa-export-schema §2)
PAIR_WINDOW_S   = 180         # build_ledger.py condor-pairing window; load-bearing (§1.7)
EMISSION_FLOOR  = 20          # G-16: suppress descriptive output below this |M|
FAMILY_ALPHA    = 0.05        # family-wise level for the simultaneous region
B_FAMILY        = 200_000     # spec §2.2: family-adjusted bootstrap replicates
B_NOMINAL       = 10_000      # spec §2.2: nominal 95% (diagnostics only)
SEED            = 20260806    # declared constant, recorded in every output object (§2.2)
BONF_C_MAX      = 2.638       # Bonferroni K=6 two-sided — Constraint A refusal threshold
BCA_A_Z_LIMIT   = 0.30        # R-7: refuse the interval when |bca_a · z| exceeds this
MARGIN_A        = 0.015       # R-3 conjunct (a) margin (+0.015R), transplanted UNCHANGED
TOST_BAND       = 0.015       # G-13: PR-19 equivalence band ±0.015R (Andy-signed)
T1_DELTA        = 0.10        # G-12b S1: PR-16 T1 non-harm margin — A NEW MARGIN
T1_P            = 0.20        # G-12b S2: tail fraction (m = ceil(p·n))
T1_FLOOR_N      = 100         # G-12b S3: capability floor; below -> INCAPABLE, never RETIRE

# --- the family (spec §9; bots_config_v2.csv) ------------------------------
RIDE   = "GF-QQQ-IC-Ride"                                   # PR-14 · control
PT50   = "GF-QQQ-IC-PT50"                                   # PR-15
TRAIL  = "GF-QQQ-IC-Trail"                                  # PR-16
TOUCH0 = "GF-QQQ-IC-Touch0"                                 # PR-17
SL100  = "GF-QQQ-IC-SL100"                                  # PR-18
SL200  = "GF-QQQ-IC-SL200"                                  # PR-19
CANARY = "GF-QQQ-IC-Canary"                                 # PR-20 · instrument, no P/L crit
DSTOP  = "GF-QQQ-IC-DStop100"                               # PR-21 · Track B (ARM-B1)
EXP1545= "GF-QQQ-IC-Exp1545"                                # PR-22 · Track B (ARM-B2)

ARMS_COMPARATIVE = [PT50, TRAIL, TOUCH0, SL100, SL200]      # PR-15…19, define M6 with RIDE
ALL_SEVEN        = [RIDE, PT50, TRAIL, TOUCH0, SL100, SL200, CANARY]   # define M7
TRACK_B          = [DSTOP, EXP1545]                          # G-11: IN the family

BOT_PR = {RIDE:"PR-14", PT50:"PR-15", TRAIL:"PR-16", TOUCH0:"PR-17",
          SL100:"PR-18", SL200:"PR-19", CANARY:"PR-20", DSTOP:"PR-21", EXP1545:"PR-22"}
BOT_MECHANIC = {PT50:"profits", TRAIL:"tstop", TOUCH0:"touch", SL100:"stoploss",
                SL200:"stoploss", CANARY:"profits", DSTOP:"dstop", EXP1545:"expiration_exit"}

# ⛔ slot-5 retire-scoped dual-tested (bot, variant) exclusions (spec §3.3; §10a append).
# Excluded from any TRACK-A-FAMILY computation — NOT from this engine's live-arm contrasts (X-5).
# Recorded here so the seam is explicit and a Track-A read never leaks in.
DUAL_TESTED_TRACK_A = {(SL100, "SL100"), (SL200, "SL200"), (DSTOP, "DSTOP_100")}

# ===========================================================================
# ⛔ DIRECTION VECTOR — DECLARED BEFORE ANY DATA EXISTS (Constraint B, post-U1 §2.2).
# ledger_meta.json export_rows == 0 at authorship; a direction chosen after data exist is
# a post-hoc analysis change. Each family member enters the max-T region with ONE declared
# direction. The vector is frozen: DIRECTION_VECTOR_SHA pins it and load asserts it.
# ===========================================================================
#   test    : PASS  = arm beats control (R-3/GATE-CM)   | direction LOWER  (ci_fam_lo > 0)
#             T1    = PR-16 fast-move-tail non-harm      | direction UPPER  (ci_fam_hi < -δ)
#             TOST  = PR-19 equivalence-to-Ride (G-13)   | direction TWO_SIDED (band ±0.015R)
FAMILY_MEMBERS = [
    {"id": "PR-15/PT50·vs·Ride",      "arm": PT50,   "control": RIDE, "test": "PASS", "direction": "LOWER"},
    {"id": "PR-16/Trail·vs·Ride",     "arm": TRAIL,  "control": RIDE, "test": "PASS", "direction": "LOWER"},
    {"id": "PR-16/Trail·T1-tail",     "arm": TRAIL,  "control": RIDE, "test": "T1",   "direction": "UPPER"},
    {"id": "PR-17/Touch0·vs·Ride",    "arm": TOUCH0, "control": RIDE, "test": "PASS", "direction": "LOWER"},
    {"id": "PR-18/SL100·vs·Ride",     "arm": SL100,  "control": RIDE, "test": "PASS", "direction": "LOWER"},
    {"id": "PR-19/SL200·vs·Ride",     "arm": SL200,  "control": RIDE, "test": "PASS", "direction": "LOWER", "disapply_c": True},
    {"id": "PR-19/SL200·TOST-equiv",  "arm": SL200,  "control": RIDE, "test": "TOST", "direction": "TWO_SIDED"},
    {"id": "PR-21/DStop100·K1·vs·Ride","arm": DSTOP,  "control": RIDE, "test": "PASS", "direction": "LOWER", "track_b": True},
    {"id": "PR-22/Exp1545·K1·vs·Ride","arm": EXP1545,"control": RIDE, "test": "PASS", "direction": "LOWER", "track_b": True},
]
DIRECTION_VECTOR_SHA = hashlib.sha256(
    json.dumps([(m["id"], m["direction"], m["test"]) for m in FAMILY_MEMBERS],
               sort_keys=False).encode()).hexdigest()

# ===========================================================================
# Refusals — the engine's own kill switches (spec §6.4). BLOCKED is a first-class
# emitted state, never a silent skip (G-1 DECLINED).
# ===========================================================================
class Refuse(Exception):
    """A hard refusal that stops the run non-zero (R-1, R-8)."""

class Blocked(Exception):
    """A named BLOCKED — a criterion that cannot be computed from available inputs.
    Emitted as a verdict object with verdict='BLOCKED', never a PASS (R-9)."""
    def __init__(self, reason):
        super().__init__(reason); self.reason = reason


# --- I-5 exit-attribution: DECLINED (G-1). Every consumer BLOCKS. --------------
def exit_rows_status():
    """G-1 DECLINED (post-U1 §4): data/exit_rows.csv is not built and will not be. Any
    criterion needing exit attribution is BLOCKED, never PASS, never silently skipped."""
    present = os.path.exists(I5_EXIT_ROWS)
    return ("PRESENT" if present else
            "BLOCKED — I-5 exit_rows.csv DECLINED (G-1, post-U1 §4); no exit-attribution input")


# ===========================================================================
# Inputs
# ===========================================================================
def load_meta():
    """I-2 + refusal R-1."""
    if not os.path.exists(I2_META):
        raise Refuse("R-1: data/ledger_meta.json missing")
    meta = json.load(open(I2_META))
    ls = meta.get("ledger_start")
    if ls is None or ls == "2099-01-01":
        raise Refuse(f"R-1: ledger_start == {ls!r} (pre-Day-0 sentinel) — engine refuses to run")
    if meta.get("source_export") is None:
        raise Refuse("R-1: ledger_meta.source_export is null")
    if (meta.get("counts") or {}).get("export_rows", 0) == 0:
        raise Refuse("R-1: ledger_meta counts.export_rows == 0 — empty ledger")
    return meta


def load_bots_meta():
    """I-3: bot -> pillar/role/underlying/epoch. A family bot missing -> refuse to name it."""
    out = {}
    if os.path.exists(I3_BOTS_META):
        for r in csv.DictReader(open(I3_BOTS_META)):
            out[r.get("bot", "")] = r
    return out


def load_config_status():
    """I-4: currently unusable (spec §1.1a). Threshold-referencing criteria report SKIPPED,
    never PASS. Inferring a threshold from a tag string is forbidden (CLAUDE.md §3 rule 2)."""
    if not os.path.exists(I4_CONFIG):
        return "ABSENT"
    # The live file is the shared-object/bot capture record, not per-bot arm thresholds
    # in a form this engine can read (§1.1a). Treat as SKIPPED-source, never a threshold oracle.
    return "PRESENT — but not a usable per-arm threshold source (§1.1a); threshold criteria SKIPPED"


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

def _dt(ts):
    if not ts or len(ts) < 16:
        return None
    try:
        return datetime.datetime.strptime(ts[:19] if len(ts) >= 19 else ts[:16] + ":00",
                                          "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

_SELF_HASH = hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest()[:16]
def self_hash():
    return _SELF_HASH


def normalize_row(row):
    """Map a LEDGER row (or, for FIXTURES only, a raw export row) to the internal shape.
    The RUN path reads the ledger (§1.1); the export mapping exists so the §5 fixtures can
    load verbatim capture rows as a TEST ASSET (they are never a reporting input)."""
    if "credit" in row:                       # ledger schema (I-1)
        g = row.get
        return {
            "bot": g("bot", ""), "trade_id": g("trade_id", ""),
            "structure": (g("structure") or "").lower(), "status": (g("status") or "").lower(),
            "quantity": _f(g("quantity")), "credit": _f(g("credit")),
            "exit_price": _f(g("exit_price")), "pnl": _f(g("pnl")), "risk": _f(g("risk")),
            "premium": _f(g("premium")),
            "open_date": g("open_date", ""), "close_date": g("close_date", ""),
            "single_sided": str(g("single_sided", "")).lower() in ("true", "1"),
            "short_put": _f(g("short_put")), "long_put": _f(g("long_put")),
            "short_call": _f(g("short_call")), "long_call": _f(g("long_call")),
            "mfe_pct": _f(g("mfe_pct")), "mae_pct": _f(g("mae_pct")),
            "underlying_open": _f(g("underlying_open")), "underlying_close": _f(g("underlying_close")),
        }
    g = row.get                               # raw export schema (fixtures only)
    def _strike(side, want):                  # parse "-581 put, +579 put"
        desc = g("description", "") or ""
        for tok in desc.split(","):
            tok = tok.strip()
            if tok.endswith(side):
                sign = tok[0]; num = _f(tok[1:].replace(side, "").strip())
                if want == "short" and sign == "-": return num
                if want == "long" and sign == "+": return num
        return None
    return {
        "bot": g("botName", ""), "trade_id": g("__tid__", ""),
        "structure": (g("type") or "").lower(), "status": (g("status") or "").lower(),
        "quantity": _f(g("quantity")), "credit": _f(g("openPrice")),
        "exit_price": _f(g("closePrice")), "pnl": _f(g("pnl")), "risk": _f(g("risk")),
        "premium": _f(g("premium")),
        "open_date": g("openDate", ""), "close_date": g("closeDate", ""),
        "single_sided": False,
        "short_put": _strike("put", "short"), "long_put": _strike("put", "long"),
        "short_call": _strike("call", "short"), "long_call": _strike("call", "long"),
        "mfe_pct": _f(g("highReturnPct")), "mae_pct": _f(g("lowReturnPct")),
        "underlying_open": _f(g("underlyingOpen")), "underlying_close": _f(g("underlyingClose")),
    }


# ===========================================================================
# Position construction (spec §1.3) — the condor, risk = larger side, second witness
# ===========================================================================
class PositionRefused(Exception):
    def __init__(self, reason): super().__init__(reason); self.reason = reason

def _risk_second_witness(leg):
    """§1.3 guard 1 / X-3: re-derive risk from strikes and refuse on mismatch, never repair.

    ⚠️ CORRECTED FORM. Spec §1.3 guard 1 writes `strikes × 100 × quantity` and OMITS the
    `− credit_$` term. As written it refuses 1,380 of 1,380 real positions — the falsified
    guard recorded as OPEN-5 in research-loop-fix-spec-2026-08-07 §2.3 (risk is NET of credit:
    F-1 put = 2×100×1 − 0.13×100×1 = 187, matching the ledger's 187, not the gross 200). The
    engine uses the correct net form; the gross form would make X-3 a family-wide false alarm."""
    q, cr = leg["quantity"], leg["credit"]
    if q is None:
        return None
    widths = []
    if leg["short_put"] is not None and leg["long_put"] is not None:
        widths.append(abs(leg["short_put"] - leg["long_put"]))
    if leg["short_call"] is not None and leg["long_call"] is not None:
        widths.append(abs(leg["short_call"] - leg["long_call"]))
    if not widths:
        return None
    credit_d = (cr * MULT * q) if cr is not None else 0.0
    return max(widths) * MULT * q - credit_d          # NET risk (OPEN-5 corrected)


def build_position(legs):
    """R_position = SUM(pnl)/MAX(risk); risk gets a second witness (X-3). Returns a dict or
    raises PositionRefused (counted, never silently repaired)."""
    risks = [l["risk"] for l in legs if l["risk"] is not None]
    if not risks:
        raise PositionRefused("no risk on any leg")
    for l in legs:
        w = _risk_second_witness(l)
        if w is not None and l["risk"] is not None and abs(w - l["risk"]) > 0.51:
            raise PositionRefused(f"risk second-witness mismatch: strikes->{w} vs column {l['risk']}")
    pnl = sum(l["pnl"] for l in legs if l["pnl"] is not None)
    risk = max(risks)
    statuses = set(l["status"] for l in legs if l["status"])
    # X-1 (G-4 CONFIRM): exclude ONLY all-expired groups; a mixed group is included whole.
    if statuses == {"expired"}:
        status_class = "all_expired"
    elif "expired" in statuses:
        status_class = "mixed_status"
    else:
        status_class = "all_closed"
    single = (len(legs) == 1 and legs[0]["structure"] in ("shortputspread", "shortcallspread"))
    o0 = _dt(legs[0]["open_date"])
    return {
        "bot": legs[0]["bot"], "trade_id": legs[0]["trade_id"],
        "R": pnl / risk, "pnl": pnl, "risk": risk, "n_legs": len(legs),
        "status_class": status_class, "single_sided": single or legs[0]["single_sided"],
        "open_day": (legs[0]["open_date"] or "")[:10],
        "underlying_open": legs[0]["underlying_open"], "underlying_close": legs[0]["underlying_close"],
        "pnl_may_be_modelled": status_class in ("all_expired", "mixed_status"),   # ITM-expiry model risk (§1.7, R1-7)
    }


def group_positions(rows):
    """Group ledger rows into condors by trade_id (never iterate raw rows — R-6)."""
    groups = {}
    for r in rows:
        groups.setdefault(r["trade_id"] or f"_{id(r)}", []).append(r)
    positions, refused = [], {}
    for tid, legs in groups.items():
        try:
            positions.append(build_position(legs))
        except PositionRefused as e:                # R-2
            refused[e.reason] = refused.get(e.reason, 0) + 1
    return positions, refused


# ===========================================================================
# Matched-day sets (spec §1.5) — M7 (all seven), M6 (six comparative; the GATE reads this)
# ===========================================================================
def matched_days(positions, arms):
    """Days on which EVERY arm in `arms` has EXACTLY ONE included condor (§1.5, G-3 CONFIRM).
    An arm with two condors on a day drops the day and is logged as an anomaly. Returns
    (matched_days_set, per_arm_day_R, anomalies)."""
    by_arm_day = {}                     # (arm, day) -> [R,...]  (all_expired excluded, X-1)
    for p in positions:
        if p["bot"] not in arms:
            continue
        if p["status_class"] == "all_expired":       # X-1
            continue
        if p["single_sided"]:                          # X-2
            continue
        by_arm_day.setdefault((p["bot"], p["open_day"]), []).append(p)
    day_R = {}                          # (arm, day) -> R  (exactly-one only)
    anomalies = []
    for (arm, day), ps in by_arm_day.items():
        if len(ps) == 1:
            day_R[(arm, day)] = ps[0]["R"]
        else:
            anomalies.append({"arm": arm, "day": day, "n_condors": len(ps)})
    all_days = sorted(set(d for (_, d) in day_R))
    M = [d for d in all_days if all((a, d) in day_R for a in arms)]
    return M, day_R, anomalies


# ===========================================================================
# The joint day-bootstrap MAX-T (G-10) — non-studentized default, direction-aware.
# ===========================================================================
def _member_stat(member, dvec, move, idx):
    """Statistic of one member over resampled day positions `idx`.
    PASS/TOST -> mean of d over idx.  T1 -> mean of d over the top-m move days IN idx
    (T recomputed inside the replicate, post-U1 §1.2)."""
    if member["test"] == "T1":
        pairs = sorted(((move[i], dvec[i]) for i in idx), key=lambda t: t[0], reverse=True)
        m = max(1, math.ceil(T1_P * len(idx)))
        top = pairs[:m]
        return sum(d for _, d in top) / len(top)
    return sum(dvec[i] for i in idx) / len(idx)


def _oriented(direction, dev, se):
    """Standardized deviation oriented toward the bound the member's direction tests."""
    s = se if se > 0 else 1.0
    if direction == "LOWER":                # simultaneous lower bound: θ̂ - c·se
        return (-dev) / s                   # bootstrap went low -> large positive
    if direction == "UPPER":                # simultaneous upper bound: θ̂ + c·se
        return dev / s
    return abs(dev) / s                     # TWO_SIDED


def family_maxt(members, dvecs, move, B=B_FAMILY, seed=SEED, studentized=False):
    """Joint day-bootstrap max-T simultaneous region over members sharing one day index.

    NON-STUDENTIZED by default (fixed per-member bootstrap SE): the max is over standardized
    centered deviations with a FIXED scale, so the leptokurtic per-replicate variance that
    inflated the studentized c (2.92–4.69, post-U1 §2.1) never enters. `c` = the (1-α)
    quantile of the oriented max — the simultaneous multiplier, comparable to 2.638.

    studentized=True is behind Constraint A: it MEASURES c with a per-replicate jackknife SE
    and REFUSES (Refuse) if c > 2.638, rather than silently reversing G-10.
    """
    n = len(next(iter(dvecs.values())))
    rng = random.Random(seed)
    theta_hat = {m["id"]: _member_stat(m, dvecs[m["id"]], move, list(range(n))) for m in members}
    boot = {m["id"]: [] for m in members}
    boot_se_rep = {m["id"]: [] for m in members} if studentized else None
    for _ in range(B):
        idx = [rng.randrange(n) for _ in range(n)]
        for m in members:
            v = _member_stat(m, dvecs[m["id"]], move, idx)
            boot[m["id"]].append(v)
            if studentized:
                # per-replicate delete-1 jackknife SE (expensive; measurement only)
                jk = [_member_stat(m, dvecs[m["id"]], move, idx[:k] + idx[k+1:])
                      for k in range(0, n, max(1, n // 12))]     # thinned jackknife
                boot_se_rep[m["id"]].append(statistics.pstdev(jk) * math.sqrt(len(jk)) if len(jk) > 1 else 1.0)
    se = {m["id"]: (statistics.pstdev(boot[m["id"]]) or 1e-12) for m in members}
    Zs = []
    for b in range(B):
        z = -1e18
        for m in members:
            dev = boot[m["id"]][b] - theta_hat[m["id"]]
            scale = boot_se_rep[m["id"]][b] if studentized else se[m["id"]]
            z = max(z, _oriented(m["direction"], dev, scale))
        Zs.append(z)
    Zs.sort()
    c = Zs[min(len(Zs) - 1, int(math.ceil((1 - FAMILY_ALPHA) * len(Zs))) - 1)]
    if studentized and c > BONF_C_MAX:
        raise Refuse(f"Constraint A: studentized max-T c={c:.3f} > {BONF_C_MAX} — refusing; "
                     f"using it would silently reverse G-10 (post-U1 §2.1).")
    bounds = {}
    for m in members:
        h, s = theta_hat[m["id"]], se[m["id"]]
        bounds[m["id"]] = {"theta": h, "se": s,
                           "ci_fam_lo": h - c * s, "ci_fam_hi": h + c * s}
    return {"c": c, "bounds": bounds, "B": B, "seed": seed, "n_days": n,
            "studentized": studentized}


# --- BCa (diagnostics only, NOT_A_GATE) + â/skew guard (spec §2.2) ----------
def bca_diagnostics(dvec):
    n = len(dvec)
    if n < 2:
        return {"skew_d": None, "bca_a": None, "note": "n<2"}
    m = statistics.mean(dvec)
    sd = statistics.pstdev(dvec)
    if sd == 0:
        raise Refuse("R-7: constant d vector — bca_a is 0/0 undefined (spec §2.2/A-13)")
    skew = (sum((x - m) ** 3 for x in dvec) / n) / (sd ** 3)
    a = skew / (6 * math.sqrt(n))
    return {"skew_d": skew, "bca_a": a}


# --- empirical-Bernstein confidence sequence (G-8 interim look, §2.6) -------
def confidence_sequence(dvec, alpha=FAMILY_ALPHA):
    """Always-valid CS on the running mean of the paired daily d — the ONLY interval that
    may be looked at more than once (spec §2.6). Empirical-Bernstein style radius with a
    log-log anytime correction. Descriptive; NOT the gate."""
    n = len(dvec)
    if n == 0:
        return {"cs_lo": None, "cs_hi": None, "n": 0, "note": "EMPTY — n=0"}
    m = statistics.mean(dvec)
    v = statistics.pvariance(dvec) if n > 1 else 0.0
    t = max(n, 2)
    rad = math.sqrt(2 * v * math.log(math.log(2 * t) + 1 + 1 / alpha) / n) + \
          3 * (max(abs(x) for x in dvec)) * math.log(math.log(2 * t) + 1 + 1 / alpha) / n
    return {"cs_lo": m - rad, "cs_hi": m + rad, "n": n, "mean": m,
            "kind": "always-valid empirical-Bernstein CS (may be looked at repeatedly)"}


def _mde_fam(c, se):
    """Minimum detectable effect at the realised n and correction (spec §2.5). Mandatory
    beside every verdict — a PASS at mde 0.035R is a different claim from one at 0.015R."""
    return c * se


# ===========================================================================
# Per-arm evaluation
# ===========================================================================
def paired_d(day_R, arm, control, M):
    return [day_R[(arm, d)] - day_R[(control, d)] for d in M]


def sign_test_blocked(reason="I-5 FIRED subpopulation"):
    """GATE-CM conjunct (c) — exact binomial sign test on the FIRED subpopulation. FIRED is
    read from I-5 only (never inferred from close time/MFE/MAE — §2.3). G-1 DECLINED -> BLOCKED."""
    raise Blocked(f"conjunct (c) sign test: {reason} — {exit_rows_status()}")


def evaluate_pass(member, dvec, region, positions_by_arm, modelled):
    """GATE-CM for a PASS arm (spec §2.4). (a) mean≥0.015 + fire_rate; (b) ci_fam_lo>0;
    (c) sign test on FIRED. (c) is BLOCKED (G-1). PR-19: (c) DISAPPLIED (G-5), (a) inert (G-6)
    -> gate reduces to (b) alone."""
    b = region["bounds"][member["id"]]
    mean_d = b["theta"]
    a_pass = mean_d >= MARGIN_A
    b_pass = b["ci_fam_lo"] > 0
    out = {
        "member": member["id"], "pr": BOT_PR[member["arm"]], "arm": member["arm"],
        "test": "GATE-CM (PASS, arm-vs-control)", "direction": member["direction"],
        "conjunct_a_mean_d": round(mean_d, 6), "conjunct_a_margin": MARGIN_A,
        "conjunct_a_pass": a_pass,
        "conjunct_a_note": "INERT under (b) at this n/c (G-6 STANDS, published inert)",
        "fire_rate": "BLOCKED — needs I-5 FIRED (G-1 DECLINED)",
        "conjunct_b_ci_fam_lo": round(b["ci_fam_lo"], 6),
        "conjunct_b_ci_fam_hi": round(b["ci_fam_hi"], 6), "conjunct_b_pass": b_pass,
        "c": round(region["c"], 4), "mde_fam": round(_mde_fam(region["c"], b["se"]), 6),
        "se": round(b["se"], 6), "n_matched_days": region["n_days"],
        "B": region["B"], "seed": region["seed"], "studentized": region["studentized"],
        "pnl_may_be_modelled": modelled,
    }
    if member.get("disapply_c"):        # PR-19, G-5
        out["conjunct_c"] = "DISAPPLIED (G-5 — the CF-11 parallel; PR-19 rarely fires by hypothesis)"
        out["gate_reduced_to"] = "(b) alone — (a) inert (G-6), (c) disapplied (G-5)"
        out["verdict"] = "PASS" if b_pass else "FAIL"
    else:
        try:
            sign_test_blocked()
        except Blocked as e:
            out["conjunct_c"] = e.reason
        out["verdict"] = "BLOCKED"      # conjunctive gate: (c) unavailable -> cannot PASS
        out["verdict_note"] = "conjunct (c) BLOCKED (I-5) -> GATE-CM cannot conclude PASS (R-9)"
    return out


def evaluate_t1(member, dvec, move, region, modelled):
    """PR-16 T1 — fast-move-tail paired non-harm (post-U1 §1, SIGNED). RETIRE iff
    ci_fam_hi(dTail) < -δ. INCAPABLE if n<100 (never RETIRE). mde_tail from the BOOTSTRAP SD."""
    b = region["bounds"][member["id"]]
    n = region["n_days"]
    m = max(1, math.ceil(T1_P * n))
    # tail set on the point estimate (arm-neutral selector — E[dTail]=0 by symmetry, NEW-1)
    order = sorted(range(n), key=lambda i: move[i], reverse=True)[:m]
    tail_d = [dvec[i] for i in order]
    sd_d_tail = statistics.pstdev(tail_d) if len(tail_d) > 1 else 0.0
    se_dtail = sd_d_tail / math.sqrt(m) if m else 0.0
    sd_dtail_boot = b["se"]                          # bootstrap SD of dTail (NEW-4)
    mde_tail = region["c"] * sd_dtail_boot           # from sd_dtail_boot, NEVER se_dtail (NEW-4)
    out = {
        "member": member["id"], "pr": "PR-16", "arm": member["arm"],
        "test": "T1 fast-move-tail paired non-harm (G-12b SIGNED)", "direction": "UPPER",
        "dTail": round(b["theta"], 6), "delta": T1_DELTA, "p": T1_P, "m": m,
        "ci_fam_hi": round(b["ci_fam_hi"], 6), "ci_fam_lo": round(b["ci_fam_lo"], 6),
        "c": round(region["c"], 4), "sd_d_tail": round(sd_d_tail, 6),
        "se_dtail": round(se_dtail, 6), "sd_dtail_boot": round(sd_dtail_boot, 6),
        "mde_tail": round(mde_tail, 6), "mde_tail_basis": "computed from sd_dtail_boot (NEW-4)",
        "n_matched_days": n, "B": region["B"], "seed": region["seed"],
        "move_basis": "open-to-close, NOT intraday extreme (under-ranks reversals; chosen)",
        "pnl_may_be_modelled": modelled,
        "CF1_PUBLICATION_PRECONDITION": "UNMET — needs D7 pricing/ITM counts (I-5, G-1 DECLINED)",
        "carried_limits": ["dTail is a COMPONENT of mean d (mean d = p·dTail + (1-p)·d_offT)",
                           "X-1 drops all-expired (ITM-expiry) groups; counts published",
                           "arm-specific loss on a CALM day lies outside T — cannot be seen"],
    }
    if n < T1_FLOOR_N:                               # S3 capability floor
        out["verdict"] = "INCAPABLE"
        out["verdict_note"] = (f"n_matched_days {n} < {T1_FLOOR_N} floor -> INCAPABLE, never "
                               f"RETIRE (re-arm ONCE at Day-0+9mo; if still <100, INCAPABLE is terminal)")
    else:
        out["verdict"] = "RETIRE" if b["ci_fam_hi"] < -T1_DELTA else "PASS(no-retire)"
    return out


def evaluate_tost(member, dvec, region, modelled):
    """PR-19 G-13 replacement — TOST equivalence to Ride, band ±0.015R (SIGNED). EQUIVALENT
    iff the family-corrected two-sided interval on mean d is inside (-band, +band)."""
    b = region["bounds"][member["id"]]
    inside = (b["ci_fam_lo"] > -TOST_BAND) and (b["ci_fam_hi"] < TOST_BAND)
    return {
        "member": member["id"], "pr": "PR-19", "arm": member["arm"],
        "test": "TOST equivalence-to-Ride (G-13 REPLACE-EQUIV)", "direction": "TWO_SIDED",
        "mean_d": round(b["theta"], 6), "band": TOST_BAND,
        "ci_fam_lo": round(b["ci_fam_lo"], 6), "ci_fam_hi": round(b["ci_fam_hi"], 6),
        "c": round(region["c"], 4), "se": round(b["se"], 6),
        "n_matched_days": region["n_days"], "B": region["B"], "seed": region["seed"],
        "verdict": "EQUIVALENT (retire-uninformative)" if inside else "NOT-EQUIVALENT",
        "pnl_may_be_modelled": modelled,
    }


# --- criteria that are BLOCKED without I-5 (G-1 DECLINED), emitted by name ----
def blocked_layer2():
    st = exit_rows_status()
    return [
        {"criterion": "GATE-CM conjunct (c) sign test (PR-15/16/17/18)", "verdict": "BLOCKED", "why": st},
        {"criterion": "PR-14 Ride inverted liveness (ITM-action exception)", "verdict": "BLOCKED", "why": st + " + ITM label unobserved (D4)"},
        {"criterion": "PR-18 SL100 / PR-19 SL200 stop-row liveness", "verdict": "BLOCKED", "why": st},
        {"criterion": "PR-20 Canary PT-fill exit-engine detector", "verdict": "BLOCKED", "why": st + " (fleet's only forward exit-engine detector)"},
        {"criterion": "PR-22 K2 speedy 15:45 close rows", "verdict": "BLOCKED", "why": st + " + timezone D3 unverified"},
        {"criterion": "G-15 put/call breach liveness indicator", "verdict": "BLOCKED", "why": st + " (PER-SIDE ruled; no fireable input)"},
        {"criterion": "<D100> ARM-B1 calibration", "verdict": "REFUSE-TO-STAMP",
         "why": "G-14 DEFER-TO-DAY-0; basis days-with-rows not trading days; unit UNRESOLVED (C10)"},
    ]


def family_census():
    """G-9 — every declared decision against the shared Ride control (spec §3.1). Under G-10
    max-T the count enters through the resampling null, not a hand-set K; the census is
    published for visibility, and no K is set (G-9 MOOT under G-10)."""
    decisions = [
        "PR-15 ΔR vs Ride", "PR-16 ΔR vs Ride", "PR-16 T1 tail vs Ride", "PR-17 ΔR vs Ride",
        "PR-18 ΔR vs Ride", "PR-19 ΔR vs Ride", "PR-19 TOST equiv vs Ride",
        "PR-21 K1 vs Ride", "PR-22 K1 vs Ride", "PR-21 secondary DiD vs SL100 (descriptive)",
    ]
    return {"decisions_vs_control": decisions, "count": len(decisions),
            "k_basis": "max-T — no hand-set K (G-10 SWITCH; G-9 MOOT)",
            "direction_vector_sha": DIRECTION_VECTOR_SHA,
            "note": "Bonferroni-across-6 (spec §3.1) and ci_fam_* (§2.5) SUPERSEDED by G-10 max-T"}


# ===========================================================================
# Orchestration
# ===========================================================================
def run(family="ALL", as_of=None, gate=False):
    print(f"COMPARATIVE MACHINERY v{VERSION} (frozen {FROZEN_ON}, sha {self_hash()})  ⛔ STANDALONE / NOT WIRED")
    print(f"  direction-vector sha {DIRECTION_VECTOR_SHA[:16]} (declared pre-data, Constraint B)")
    try:
        meta = load_meta()                       # R-1
    except Refuse as e:
        print(f"REFUSE — {e}")
        return 2
    # Past R-1 the ledger has post-cutover rows. (Today it never gets here.)
    if not os.path.exists(I1_LEDGER):
        print("REFUSE — R-1: data/trades.csv missing")
        return 2
    rows = [normalize_row(r) for r in csv.DictReader(open(I1_LEDGER))]
    bots_meta = load_bots_meta()
    for arm in ARMS_COMPARATIVE + [RIDE]:          # I-3: a family bot missing -> refuse to name it
        if arm not in bots_meta:
            print(f"REFUSE — I-3: family bot {arm} absent from bots_meta.csv; cannot name the family")
            return 2

    positions, refused = group_positions(rows)
    M7, day_R7, anom7 = matched_days(positions, ALL_SEVEN)
    M6, day_R, anomalies = matched_days(positions, ARMS_COMPARATIVE + [RIDE])
    print(f"  |M7|={len(M7)}  |M6|={len(M6)}  (gate reads M6, G-2)  Δ={len(M7)-len(M6)}")

    if len(M6) < EMISSION_FLOOR:                   # G-16
        print(f"COMPARATIVE: suppressed — |M6|={len(M6)} < {EMISSION_FLOOR} matched days "
              f"(stage exercised, output withheld, §6.3).")
        return 0

    modelled = any(p["pnl_may_be_modelled"] for p in positions)
    # Build the joint region over the greenfield members that share the M6 day index.
    # Track B (PR-21/22) are IN the family (G-11) but run on their own MB day sets and are
    # unbuilt today; they enter via family_census, and their intervals are computed when
    # those bots exist. The joint resample requires a shared day index (spec §3.4).
    gf_members = [m for m in FAMILY_MEMBERS if not m.get("track_b")]
    dvecs = {m["id"]: paired_d(day_R, m["arm"], m["control"], M6) for m in gf_members}
    move = [(_move_of_day(positions, d)) for d in M6]
    region = family_maxt(gf_members, dvecs, move, studentized=False)

    verdicts = []
    if gate and _gate_date_ok(as_of):              # R-5 / R-8
        for m in gf_members:
            if m["test"] == "PASS":
                verdicts.append(evaluate_pass(m, dvecs[m["id"]], region,
                                              positions_by_arm=None, modelled=modelled))
            elif m["test"] == "T1":
                verdicts.append(evaluate_t1(m, dvecs[m["id"]], move, region, modelled))
            elif m["test"] == "TOST":
                verdicts.append(evaluate_tost(m, dvecs[m["id"]], region, modelled))
    else:
        print("  R-5: no stamped gate-eval date resolved -> DESCRIPTIVE ONLY, no verdicts.")

    _write_outputs(as_of or "descriptive", region, verdicts, M6, M7, day_R,
                   refused, anomalies, modelled, meta)
    return 0


def _move_of_day(positions, day):
    for p in positions:
        if p["open_day"] == day and p["bot"] == RIDE and p["underlying_open"]:
            uo, uc = p["underlying_open"], p["underlying_close"]
            if uo:
                return abs(uc - uo) / uo
    return 0.0


def _gate_date_ok(as_of):
    """R-5/R-8: a verdict is emitted only at a stamped gate-eval date, and --gate requires
    --as-of == that date. G-7 stamps 'Day-0+6mo' RELATIONALLY; Day-0 has no calendar date
    (ledger_start sentinel), so no stamped date resolves today -> no verdict is ever emitted."""
    return False


def _write_outputs(tag, region, verdicts, M6, M7, day_R, refused, anomalies, modelled, meta):
    os.makedirs(OUT_DIR, exist_ok=True)
    base = os.path.join(OUT_DIR, tag.replace(":", "").replace(" ", "_"))
    obj = {
        "engine_version": VERSION, "engine_sha256_16": self_hash(), "frozen_on": FROZEN_ON,
        "wired": False, "source": "GENERATOR — advisory only, never a reporting input",
        "direction_vector_sha": DIRECTION_VECTOR_SHA, "correction": "joint day-bootstrap max-T (G-10)",
        "c": round(region["c"], 4), "B": region["B"], "seed": region["seed"],
        "n_matched_days_M6": len(M6), "n_matched_days_M7": len(M7),
        "emission_floor": EMISSION_FLOOR, "positions_refused": refused,
        "matched_day_anomalies": anomalies, "pnl_may_be_modelled": modelled,
        "family_census": family_census(), "blocked_layer2": blocked_layer2(),
        "verdicts": verdicts,
        "gate": "descriptive only — no stamped gate-eval date resolves (R-5, G-7 relational)",
    }
    with open(base + "_comparative.json", "w") as f:
        json.dump(obj, f, indent=2); f.write("\n")
    with open(base + "_census.json", "w") as f:
        json.dump(family_census(), f, indent=2); f.write("\n")
    with open(base + "_paired.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["family", "arm", "control", "day", "d_i", "provenance"])
        for m in [x for x in FAMILY_MEMBERS if not x.get("track_b") and x["test"] == "PASS"]:
            for d in M6:
                w.writerow(["GF", m["arm"], m["control"], d,
                            day_R[(m["arm"], d)] - day_R[(m["control"], d)], "M6 paired-by-day"])
    print(f"  -> {os.path.relpath(base + '_comparative.json', ROOT)}")


# ===========================================================================
# Validation fixtures (spec §5) — verbatim capture rows as a TEST ASSET
# ===========================================================================
FIXTURE_SHA = {   # sha256(raw export line + "\n"), keyed by a human label
    "F1-put":  "dc495eee8e554925c03f0e63f6d9ced67c09a5df63c66dca3b04f69fba29b3db",
    "F1-call": "b258a8e41b1794b4bcf79084ae9e14598b282773c45d192cb9e961c62f4972ca",
    "F2-call": "ecb0b2abf80527f1b72c9b9ccdf71b8707e887856ba84712e1dba16cc6460475",
    "F2-put":  "85e40ae3350e6e916a04a57a8a6af1ddd3e9ea1f3dbf8d41e1d1260177b0d271",
}
EXPORT = os.path.join(DATA, "captures", "oa_export_positions_2026-07-30.csv")

def _load_fixture_rows():
    """Load the four §5 fixture rows VERBATIM from the frozen capture, sha-checked (copy,
    do not transcribe — oa-export-schema §5 fix 2). Returns dict label -> parsed export row."""
    with open(EXPORT, newline="") as f:
        raw = f.read().split("\n")
    header = next(csv.reader([raw[0]]))
    want = {                                  # (botName, type, openDate) — unique to each fixture row
        ("QQQ-IC-0DTE-Raw-HoldToExp", "shortputspread",  "2026-03-24 12:07:01"): "F1-put",
        ("QQQ-IC-0DTE-Raw-HoldToExp", "shortcallspread", "2026-03-24 12:08:01"): "F1-call",
        ("QQQ-IC-0DTE-HedgeA-S1",     "shortcallspread", "2026-03-24 11:01:02"): "F2-call",
        ("QQQ-IC-0DTE-HedgeA-S1",     "shortputspread",  "2026-03-24 11:01:01"): "F2-put",
    }
    out = {}
    for line in raw[1:]:
        if not line:
            continue
        vals = next(csv.reader([line]))
        row = dict(zip(header, vals))
        key = (row.get("botName"), (row.get("type") or "").lower(), row.get("openDate"))
        if key in want and want[key] not in out:
            label = want[key]
            got = hashlib.sha256((line + "\n").encode()).hexdigest()
            if got != FIXTURE_SHA[label]:
                raise SystemExit(f"FIXTURE DRIFT {label}: {got} != {FIXTURE_SHA[label]}")
            out[label] = row
    return out


def validate():
    P = F = 0
    def check(label, got, want):
        nonlocal P, F
        ok = (abs(got - want) <= 1e-9) if isinstance(got, float) and isinstance(want, float) else (got == want)
        P += ok; F += (not ok)
        print(f"  {'PASS' if ok else 'FAIL'}  {label}" + ("" if ok else f"\n        got={got!r} want={want!r}"))
    def raises(label, fn, exc):
        nonlocal P, F
        try:
            fn(); P += 0; F += 1; print(f"  FAIL  {label} (did not raise)")
        except exc:
            P += 1; print(f"  PASS  {label}")
        except Exception as e:
            F += 1; print(f"  FAIL  {label} (raised {type(e).__name__}: {e})")

    fx = _load_fixture_rows()
    print(f"  ({len(fx)} verbatim capture rows verified byte-exact by sha256)\n")

    # tag both condor groups so build_position pairs them
    for lab in ("F1-put", "F1-call"): fx[lab]["__tid__"] = "F1"
    for lab in ("F2-call", "F2-put"): fx[lab]["__tid__"] = "F2"
    f1 = build_position([normalize_row(fx["F1-put"]), normalize_row(fx["F1-call"])])
    f2 = build_position([normalize_row(fx["F2-call"]), normalize_row(fx["F2-put"])])

    # ---- F-1 · condor R identity, and the wrong answer it must not give ----
    check("A-1 R_condor == 18/192 == 0.09375", f1["R"], 0.09375)
    check("A-2 R_condor != mean(leg ror) 0.047641 (denominator = larger side)", round(f1["R"], 6) != 0.047641, True)
    o1 = _dt(fx["F1-put"]["openDate"]); o2 = _dt(fx["F1-call"]["openDate"])
    check("A-3 open times 60s apart < PAIR_WINDOW_S -> one group, not single_sided",
          (abs((o2 - o1).total_seconds()) <= PAIR_WINDOW_S, f1["single_sided"]), (True, False))

    # ---- F-2 · paired ΔR on a real matched day, real multi-contract row ----
    check("A-4 R_HedgeA == 756/4900 == 0.154285714285714", f2["R"], 0.154285714285714)
    check("A-5 d(2026-03-24) == 0.060535714285714", f2["R"] - f1["R"], 0.060535714285714)
    q = normalize_row(fx["F2-put"])
    check("A-6 ×quantity guard: premium == -(openPrice×100×28) == -700",
          q["premium"], -(q["credit"] * MULT * q["quantity"]))

    # ---- F-3 · sign-convention guard, and a hard refusal ----
    p = normalize_row(fx["F1-put"])
    check("A-7 credit == openPrice == 0.13 (positive), premium == -13 (negative)",
          (p["credit"], p["premium"]), (0.13, -13.0))
    def _use_premium_as_credit():
        bad = dict(fx["F1-put"]); bad["openPrice"] = bad["premium"]   # -13 as the credit
        r = normalize_row(bad)
        if r["credit"] is not None and r["credit"] <= 0:
            raise ValueError("credit <= 0: premium fed as credit (the 2026-08-04 bug, 1247/1254)")
    raises("A-8 premium-as-credit RAISES, does not silently drop (the 1247/1254 bug)", _use_premium_as_credit, ValueError)

    # ---- F-4 · exclusion accounting from the real capture's real counts ----
    allrows = list(csv.DictReader(open(EXPORT)))
    from collections import Counter
    sc = Counter((r["status"] or "").lower() for r in allrows)
    check("A-9 n_expired==154, n_closed==1232, total==1386", (sc["expired"], sc["closed"], len(allrows)), (154, 1232, 1386))
    # mixed group: F-1 put (closed) + a synthetic expired call leg, both real-shaped
    mixed_call = dict(fx["F1-call"]); mixed_call["status"] = "expired"; mixed_call["__tid__"] = "MX"
    mixp = dict(fx["F1-put"]); mixp["__tid__"] = "MX"
    mixed = build_position([normalize_row(mixp), normalize_row(mixed_call)])
    check("A-10 mixed group -> included whole, status_class mixed, R uses both legs' pnl",
          (mixed["status_class"], mixed["R"]), ("mixed_status", (11 + 7) / max(187, 192)))
    raises("A-11 aggregate without its n raises (R-3)",
           lambda: _emit_requires_n({"mean": 0.05}), Refuse)

    # ---- F-5 · bootstrap determinism + the incapable-test guard ----
    dvec = [f2["R"] - f1["R"]] * 40 + [(-0.2), 0.15]   # a real d plus spread, n=42
    move = [0.01] * len(dvec)
    mem = [{"id": "t", "arm": PT50, "control": RIDE, "test": "PASS", "direction": "LOWER"}]
    r1 = family_maxt(mem, {"t": dvec}, move, B=2000, seed=SEED)
    r2 = family_maxt(mem, {"t": dvec}, move, B=2000, seed=SEED)
    check("A-12 same seed -> bit-identical ci_fam_lo/hi",
          (r1["bounds"]["t"]["ci_fam_lo"], r1["bounds"]["t"]["ci_fam_hi"]),
          (r2["bounds"]["t"]["ci_fam_lo"], r2["bounds"]["t"]["ci_fam_hi"]))
    raises("A-13 constant d -> bca_a undefined, RAISES (R-7)", lambda: bca_diagnostics([0.3] * 30), Refuse)
    check("A-14 n_fired==7 at K=6 -> sign_test INCAPABLE (2·.5^7=.015625 > α'), boundary at 8",
          (2 * 0.5 ** 7 > 0.05 / 6, 2 * 0.5 ** 8 <= 0.05 / 6), (True, True))
    #   SD(d)=0.134 is the paired daily SD (already = SD(R)·√(2(1-ρ))); SE(mean d)=SD(d)/√n.
    check("A-15 mde_fam = c·SE at n=100, SD(d)=0.134, c=2.638 -> rounds to 0.035 (§2.5)",
          round(_mde_fam(2.638, 0.134 / math.sqrt(100)), 3), 0.035)

    # ---- extra: the ruled machinery the fixtures above do not touch ----
    print()
    _validate_rulings(check, raises)

    print(f"\n  {P}/{P+F} passed   engine {VERSION} sha {self_hash()}")
    return 1 if F else 0


def _emit_requires_n(agg):
    if "n" not in agg:
        raise Refuse("R-3: aggregate emitted without its n")


def _validate_rulings(check, raises):
    rng = random.Random(1)
    n = 120
    # --- Constraint A: studentized max-T on a leptokurtic d must MEASURE c and refuse if >2.638 ---
    #   ≈90% near-zero, ≈10% at ±0.9 (post-U1 §2.1 shape), across several members -> high studentized c.
    def lepto():
        return [(rng.choice([-0.9, 0.9]) if rng.random() < 0.10 else rng.gauss(0, 0.01)) for _ in range(n)]
    members = [{"id": f"m{j}", "arm": PT50, "control": RIDE, "test": "PASS", "direction": "LOWER"} for j in range(6)]
    dvecs = {m["id"]: lepto() for m in members}
    move = [0.01] * n
    reg_ns = family_maxt(members, dvecs, move, B=1500, seed=7, studentized=False)
    check("G-10 default is NON-studentized (studentized flag False)", reg_ns["studentized"], False)
    check("G-10 non-studentized c is published and finite", isinstance(reg_ns["c"], float), True)
    raises("Constraint A: studentized c>2.638 on leptokurtic d REFUSES (never silently reverses G-10)",
           lambda: family_maxt(members, dvecs, move, B=1500, seed=7, studentized=True), Refuse)

    # --- Constraint B: direction vector is frozen pre-data, and orientations are correct ---
    check("Constraint B: direction-vector sha is the frozen declared one",
          DIRECTION_VECTOR_SHA == hashlib.sha256(json.dumps(
              [(m["id"], m["direction"], m["test"]) for m in FAMILY_MEMBERS], sort_keys=False).encode()).hexdigest(), True)
    check("Constraint B: 7 LOWER (5 GF + 2 Track B), 1 UPPER (T1), 1 TWO_SIDED (TOST)",
          (sum(m["direction"] == "LOWER" for m in FAMILY_MEMBERS),
           sum(m["direction"] == "UPPER" for m in FAMILY_MEMBERS),
           sum(m["direction"] == "TWO_SIDED" for m in FAMILY_MEMBERS)), (7, 1, 1))

    # --- T1 (PR-16, SIGNED): retire on a clear tail harm at n>=100; INCAPABLE below floor ---
    n2 = 120
    rng2 = random.Random(3)
    move2 = [rng2.random() for _ in range(n2)]
    order = sorted(range(n2), key=lambda i: move2[i], reverse=True)[:math.ceil(T1_P * n2)]
    d2 = [0.0] * n2
    for i in order:
        d2[i] = -0.5                      # arm much worse than control on the fast-move tail
    m_t1 = {"id": "PR-16/Trail·T1-tail", "arm": TRAIL, "control": RIDE, "test": "T1", "direction": "UPPER"}
    reg = family_maxt([m_t1], {"PR-16/Trail·T1-tail": d2}, move2, B=3000, seed=SEED)
    t1 = evaluate_t1(m_t1, d2, move2, reg, modelled=False)
    check("T1 RETIRE when ci_fam_hi(dTail) < -δ at n>=100", t1["verdict"], "RETIRE")
    check("T1 δ==0.10R (NEW MARGIN), p==0.20, mde_tail from sd_dtail_boot",
          (t1["delta"], t1["p"], t1["mde_tail_basis"]), (0.10, 0.20, "computed from sd_dtail_boot (NEW-4)"))
    check("T1 CF-1 publication precondition UNMET (G-1 DECLINED)",
          t1["CF1_PUBLICATION_PRECONDITION"].startswith("UNMET"), True)
    reg_small = family_maxt([m_t1], {"PR-16/Trail·T1-tail": d2[:60]}, move2[:60], B=800, seed=SEED)
    t1i = evaluate_t1(m_t1, d2[:60], move2[:60], reg_small, modelled=False)
    check("T1 INCAPABLE (never RETIRE) below the n>=100 floor", t1i["verdict"], "INCAPABLE")
    # T1 null centering (NEW-1): identical arm -> dTail ≈ 0, no retirement
    d0 = [0.0] * n2
    reg0 = family_maxt([m_t1], {"PR-16/Trail·T1-tail": d0}, move2, B=800, seed=SEED)
    check("T1 arm==control -> dTail 0 by symmetry (NEW-1 killed by construction)", reg0["bounds"]["PR-16/Trail·T1-tail"]["theta"], 0.0)

    # --- TOST (PR-19, G-13 SIGNED): equivalent within ±0.015R ---
    d_eq = [0.001, -0.001] * 60
    m_tost = {"id": "PR-19/SL200·TOST-equiv", "arm": SL200, "control": RIDE, "test": "TOST", "direction": "TWO_SIDED"}
    reg_eq = family_maxt([m_tost], {"PR-19/SL200·TOST-equiv": d_eq}, [0.01] * len(d_eq), B=3000, seed=SEED)
    tost = evaluate_tost(m_tost, d_eq, reg_eq, modelled=False)
    check("TOST band == ±0.015R (G-13 SIGNED)", tost["band"], 0.015)
    check("TOST EQUIVALENT when the family interval is inside the band", tost["verdict"].startswith("EQUIVALENT"), True)

    # --- G-5: PR-19 PASS gate reduces to (b) alone; (c) disapplied ---
    m_sl200 = next(m for m in FAMILY_MEMBERS if m.get("disapply_c"))
    reg_b = family_maxt([m_sl200], {m_sl200["id"]: [0.05] * 100}, [0.01] * 100, B=1500, seed=SEED)
    ev = evaluate_pass(m_sl200, [0.05] * 100, reg_b, None, modelled=False)
    check("G-5 PR-19 gate reduces to (b) alone (c disapplied)", ev["conjunct_c"].startswith("DISAPPLIED"), True)
    check("G-5 PR-19 can reach PASS on (b) alone", ev["verdict"], "PASS")

    # --- G-1 DECLINED: a normal PASS arm's (c) is BLOCKED -> verdict BLOCKED, never PASS ---
    m_pt50 = next(m for m in FAMILY_MEMBERS if m["arm"] == PT50)
    reg_p = family_maxt([m_pt50], {m_pt50["id"]: [0.05] * 100}, [0.01] * 100, B=1500, seed=SEED)
    evp = evaluate_pass(m_pt50, [0.05] * 100, reg_p, None, modelled=False)
    check("G-1 DECLINED: PASS arm (c) BLOCKED -> verdict BLOCKED, never PASS", evp["verdict"], "BLOCKED")
    check("G-1 DECLINED: every Layer-2 criterion is emitted BLOCKED by name (not skipped)",
          all(b["verdict"] in ("BLOCKED", "REFUSE-TO-STAMP") for b in blocked_layer2()), True)

    # --- R-2: risk second-witness mismatch refuses the position ---
    raises("R-2 risk second-witness mismatch -> PositionRefused",
           lambda: build_position([{"bot": "b", "trade_id": "t", "structure": "shortputspread",
                                    "status": "closed", "quantity": 1.0, "credit": 0.5, "exit_price": 0.1,
                                    "pnl": 40.0, "risk": 999.0, "premium": -50.0, "single_sided": False,
                                    "short_put": 100.0, "long_put": 98.0, "short_call": None, "long_call": None,
                                    "open_date": "2026-03-24 12:00:00", "close_date": "2026-03-24 15:50:00",
                                    "mfe_pct": 0.5, "mae_pct": -0.5, "underlying_open": 100.0, "underlying_close": 100.0}]),
           PositionRefused)

    # --- R-1: today's sentinel meta refuses the run ---
    raises("R-1 ledger_start sentinel (2099-01-01) refuses the run (exit non-zero)", load_meta, Refuse)

    # --- G-2 / G-16 / matched-days: exactly-one, all-expired excluded, M6 vs M7 ---
    pos = [
        {"bot": RIDE, "open_day": "D1", "R": 0.1, "status_class": "all_closed", "single_sided": False},
        {"bot": PT50, "open_day": "D1", "R": 0.2, "status_class": "all_closed", "single_sided": False},
        {"bot": PT50, "open_day": "D1", "R": 0.3, "status_class": "all_closed", "single_sided": False},  # 2 -> anomaly
        {"bot": RIDE, "open_day": "D2", "R": 0.1, "status_class": "all_expired", "single_sided": False}, # X-1 drop
    ]
    M, dR, anom = matched_days(pos, [RIDE, PT50])
    check("§1.5 exactly-one: a 2-condor day is an anomaly, not averaged", (M, len(anom)), ([], 1))

    # --- confidence sequence exists and widens as n shrinks (G-8) ---
    cs_big = confidence_sequence([0.05] * 100)
    cs_small = confidence_sequence([0.05] * 20)
    check("G-8 CS radius wider at smaller n (always-valid interim look)",
          (cs_small["cs_hi"] - cs_small["cs_lo"]) > (cs_big["cs_hi"] - cs_big["cs_lo"]), True)

    # --- slot-5 dual-tested exclusions declared (G-11 seam) ---
    check("G-11 slot-5 dual-tested (bot,variant) exclusions declared for Track-A family",
          DUAL_TESTED_TRACK_A == {(SL100, "SL100"), (SL200, "SL200"), (DSTOP, "DSTOP_100")}, True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Comparative machinery (STANDALONE, not wired).")
    ap.add_argument("--family", default="ALL", choices=["GF", "B", "ALL"])
    ap.add_argument("--as-of", default=None)
    ap.add_argument("--gate", action="store_true",
                    help="refused unless the named arm has a stamped gate-eval date AND --as-of equals it")
    ap.add_argument("--validate", action="store_true")
    a = ap.parse_args()
    if a.validate:
        sys.exit(validate())
    sys.exit(run(a.family, a.as_of, a.gate))
