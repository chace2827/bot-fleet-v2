#!/usr/bin/env python3
"""Compute Bot Fleet metrics from data/trades.csv + data/bots.csv and render the
backlog from docs/backlog.md. Emits STATUS.md (numeric source of truth) and
dashboard.html (numbers + backlog). Never edit STATUS.md by hand.

N reporting: 'Trades' = condors (legs paired into one entry); 'Legs' = OA position
rows (matches OA's "Positions" count). Win rate shown is trade-level (per condor).
"""
import argparse, collections, csv, datetime, json, math, os, random, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")


def set_root(root):
    """Repoint ROOT and D at a scratch root (G-3 fixture / live separation)."""
    global ROOT, D
    ROOT = os.path.abspath(root)
    D = os.path.join(ROOT, "data")


CLI_TODAY = None


def add_weekdays(d, n):
    """Add n trading days (Mon-Fri) to date d; n may be negative."""
    step = 1 if n >= 0 else -1
    count = 0
    while count < abs(n):
        d += datetime.timedelta(days=step)
        if d.weekday() < 5:
            count += 1
    return d


def count_weekdays(start, end):
    """Count weekdays in [start, end] inclusive."""
    n = 0
    d = start
    while d <= end:
        if d.weekday() < 5:
            n += 1
        d += datetime.timedelta(days=1)
    return n


DECIDABILITY_WINDOW = 20          # trading days
DECIDABILITY_MIN_CLOSES = 3       # closes in window needed to project


def resolve_report_today(cli_today, status_today, epoch, ledger_start, trades):
    """Deterministic projection anchor; never uses the system clock."""
    if cli_today:
        return datetime.date.fromisoformat(cli_today)
    if status_today:
        return datetime.date.fromisoformat(status_today)
    if epoch:
        return datetime.datetime.fromtimestamp(
            int(epoch), tz=datetime.timezone.utc).date()
    close_dates = []
    for t in trades:
        cd = t.get("close_date")
        if cd:
            try:
                close_dates.append(datetime.date.fromisoformat(cd[:10]))
            except ValueError:
                pass
    if close_dates:
        return max(close_dates)
    if ledger_start:
        try:
            return datetime.date.fromisoformat(ledger_start)
        except ValueError:
            pass
    return datetime.date(1970, 1, 1)


def _position_close_dates(trades):
    """Group legs by trade_id and return two (bot, close_date) lists: condors and one-sided spreads.

    A position is one-sided if any of its legs is flagged `single_sided` == "True".
    The ledger (build_ledger.py) already made this determination; we only consume it.
    """
    by_id = collections.defaultdict(list)
    for t in trades:
        by_id[t["trade_id"]].append(t)
    condors = []
    one_sided = []
    for legs in by_id.values():
        if not legs or not all(l.get("close_date") for l in legs):
            continue
        cd = max(l["close_date"][:10] for l in legs)
        bot = legs[0]["bot"]
        if any(l.get("single_sided") == "True" for l in legs):
            one_sided.append((bot, cd))
        else:
            condors.append((bot, cd))
    return condors, one_sided


def decidability_countdown(trades, meta, today, ledger_start,
                           window=DECIDABILITY_WINDOW, min_closes=DECIDABILITY_MIN_CLOSES):
    """Render a PROJECTION section: fire rate and 100-condor date per armed arm.

    Unit of account is the POSITION (a two-sided condor). One-sided spreads are
    reported in their own column and do NOT count toward the 100-condor target.
    An arm is "armed" if its bots_meta status is ON.  Insufficient data is explicit.
    """
    condors, one_sided = _position_close_dates(trades)
    condors_by_bot = collections.defaultdict(list)
    for bot, cd in condors:
        condors_by_bot[bot].append(cd)
    one_sided_by_bot = collections.defaultdict(list)
    for bot, cd in one_sided:
        one_sided_by_bot[bot].append(cd)

    armed = sorted(b for b, r in meta.items() if r.get("status", "").upper() == "ON")
    if not armed:
        return []

    # The recent window is the last *window* trading days ending at today, inclusive.
    window_start = add_weekdays(today, -(window - 1))
    effective_start = max(window_start,
                          datetime.date.fromisoformat(ledger_start) if ledger_start else window_start)
    trading_days_present = count_weekdays(effective_start, today)

    lines = ["", "---", "",
             "## Decidability countdown — per armed arm (PROJECTION, not evidence)",
             "> **This is a forward projection, not a result.** It extrapolates the recent fire rate "
             "and assumes that rate holds. Calendar projection skips weekends and does **not** model "
             "market holidays, so the date is approximate. The unit of account is the **POSITION** "
             "(a two-sided condor = two spread rows paired by `trade_id`); *n* = 100 means **100 condors**, "
             "not 100 legs. One-sided spreads are listed separately and do **not** count toward the "
             "100-condor target. The recent window is the last **{} trading days**; the post-cutover "
             "ledger currently contributes **{} trading day{}** to this window.".format(
                 window, trading_days_present, "s" if trading_days_present != 1 else ""),
             "",
             "| Arm | Pillar | Current condors, positions | One-sided positions, spreads | Closes in "
             "{}-trading-day window | Fire rate (closes/trading-day, condors) | Projected 100-condor date |".format(window),
             "|---|---|--:|--:|--:|--:|---|"]

    for bot in armed:
        rec = meta[bot]
        pillar = rec.get("pillar", "—")
        all_dates = sorted(condors_by_bot.get(bot, []))
        total = len(all_dates)
        window_dates = [d for d in all_dates if window_start <= datetime.date.fromisoformat(d) <= today]
        n_window = len(window_dates)
        n_one_sided = len(one_sided_by_bot.get(bot, []))

        if n_window < min_closes or trading_days_present == 0:
            rate_s = "insufficient data"
            proj_s = "insufficient data"
        else:
            fire_rate = n_window / trading_days_present
            rate_s = f"{fire_rate:.2f}"
            remaining = 100 - total
            if remaining <= 0:
                # 100th close already happened
                hundredth = all_dates[99] if len(all_dates) > 99 else all_dates[-1]
                proj_s = f"reached (n=100 at {hundredth})"
            else:
                needed = math.ceil(remaining / fire_rate)
                proj_date = add_weekdays(today, needed)
                proj_s = proj_date.isoformat()

        lines.append(f"| {bot} | {pillar} | {total} | {n_one_sided} | {n_window} | {rate_s} | {proj_s} |")

    return lines


def _parse_table_row(status, arm):
    """Return the split cells of the countdown table row for *arm*."""
    m = re.search(r"## Decidability countdown.*?\n(.*?)\n## ", status, re.S)
    if not m:
        return []
    section = m.group(1)
    for line in section.splitlines():
        if line.startswith(f"| {arm} "):
            return [c.strip() for c in line.split("|")]
    return []


def validate():
    """Self-test: fire-rate fixture with a scratch root (never touches live data/)."""
    root = tempfile.mkdtemp(prefix="report-validate-")
    try:
        os.makedirs(os.path.join(root, "data"), exist_ok=True)

        today = datetime.date(2026, 8, 14)
        # The 20-trading-day window ends at today.  Ledger starts on the first day of
        # the window so every present trading day has a condor (fire rate = 1.00).
        ledger_start = add_weekdays(today, -(DECIDABILITY_WINDOW - 1)).isoformat()

        # bots_meta.csv fixture
        with open(os.path.join(root, "data", "bots_meta.csv"), "w") as f:
            f.write("bot,pillar,role,underlying,status,champion,epoch_boundary,hedge,strike_fix,superseded,focus,notes,ops_class\n")
            f.write("TestArm,IC,experiment,SPX,ON,,,,,,,,\n")
            f.write("SparseArm,IC,experiment,SPX,ON,,,,,,,,\n")
            f.write("OneSidedArm,IC,experiment,SPX,ON,,,,,,,,\n")

        # bots.csv fixture (report.py uses this for roster, totals, etc.)
        with open(os.path.join(root, "data", "bots.csv"), "w") as f:
            f.write("bot,pillar,underlying,role,status,n_trades,n_legs,total_pnl,win_rate_trade,win_rate_leg,first_trade,last_trade,epoch_start,needs_strike_fix,superseded\n")
            f.write(f"TestArm,IC,SPX,experiment,ON,20,20,0,100%,100%,{ledger_start},{today.isoformat()},{ledger_start},,\n")
            f.write(f"SparseArm,IC,SPX,experiment,ON,1,1,0,100%,100%,{today.isoformat()},{today.isoformat()},{ledger_start},,\n")
            f.write(f"OneSidedArm,IC,SPX,experiment,ON,1,1,0,100%,100%,{today.isoformat()},{today.isoformat()},{ledger_start},,\n")

        # trades.csv fixture:
        #  - TestArm: 20 two-sided condors, one closing on each trading day of the window (1.00 condors/day).
        #  - SparseArm: 1 condor -> insufficient data.
        #  - OneSidedArm: 1 one-sided shortputspread -> 0 condors, 1 one-sided position.
        with open(os.path.join(root, "data", "trades.csv"), "w") as f:
            f.write("bot,pillar,underlying,role,epoch,trade_id,symbol,structure,status,quantity,credit,exit_price,pnl,risk,open_date,close_date,expiration,tags,single_sided,short_put,long_put,short_call,long_call,premium,underlying_open,underlying_close,mfe_pct,mae_pct,mfe_date,mae_date\n")
            condor_row = "{},IC,SPX,experiment,post-fix,{},SPX,ironcondor,closed,1,0.20,0.10,0,50,{},{},2026-08-14 16:00:00,,False,100,95,110,115,0.20,100,100,1,0,2026-08-14 15:00:00,2026-08-14 10:00:00\n"
            one_sided_row = "OneSidedArm,IC,SPX,experiment,post-fix,TOS1,SPX,shortputspread,closed,1,0.20,0.10,0,50,2026-08-14 10:00:00,2026-08-14 16:00:00,2026-08-14 16:00:00,,True,100,95,,,0.20,100,100,1,0,2026-08-14 15:00:00,2026-08-14 10:00:00\n"
            for i in range(DECIDABILITY_WINDOW):
                cd = add_weekdays(today, -(DECIDABILITY_WINDOW - 1 - i))
                od = f"{cd.isoformat()} 10:00:00"
                cdts = f"{cd.isoformat()} 16:00:00"
                f.write(condor_row.format("TestArm", f"T{i:04d}", od, cdts))
            f.write(condor_row.format("SparseArm", "T9000", "2026-08-14 10:00:00", "2026-08-14 16:00:00"))
            f.write(one_sided_row)

        # ledger_meta.json fixture
        with open(os.path.join(root, "data", "ledger_meta.json"), "w") as f:
            json.dump({"ledger_start": ledger_start}, f)

        # Run report.py against the scratch root, pinned today.
        proc = subprocess.run(
            [sys.executable, __file__, "--root", root, "--today", today.isoformat()],
            capture_output=True, text=True,
        )
        if proc.returncode != 0:
            print("report.py selftest subprocess failed:", file=sys.stderr)
            print(proc.stdout, file=sys.stderr)
            print(proc.stderr, file=sys.stderr)
            return 1

        status_path = os.path.join(root, "STATUS.md")
        status = open(status_path).read()

        # Defect-1: one-sided spreads do NOT count as condors.
        one_sided_cells = _parse_table_row(status, "OneSidedArm")
        if not one_sided_cells or one_sided_cells[3] != "0" or one_sided_cells[4] != "1":
            print(f"FAIL: OneSidedArm row should have 0 condors and 1 one-sided spread; got {one_sided_cells}", file=sys.stderr)
            print(status, file=sys.stderr)
            return 1

        # Defect-2: an arm closing on every present trading day must render fire rate 1.00.
        test_cells = _parse_table_row(status, "TestArm")
        if not test_cells or test_cells[6] != "1.00" or test_cells[7] != "2026-12-04":
            print(f"FAIL: TestArm row should have fire rate 1.00 and projected date 2026-12-04; got {test_cells}", file=sys.stderr)
            print(status, file=sys.stderr)
            return 1

        # SparseArm has only 1 close in window -> insufficient data.
        if "insufficient data" not in status.lower():
            print("FAIL: expected 'insufficient data' state not found", file=sys.stderr)
            print(status, file=sys.stderr)
            return 1

        print("report.py selftest OK")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


# --- pre-registration ledger parsing (T-13) -------------------------------
import pre_registration_ledger


def fl(x):
    try: return float(x)
    except (TypeError, ValueError): return 0.0


def now_iso():
    """Reproducible 'generated' timestamp. SOURCE_DATE_EPOCH wins over wall clock."""
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        return datetime.datetime.fromtimestamp(
            int(epoch), tz=datetime.timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds")
    return datetime.datetime.now().isoformat(timespec="seconds")


def today_iso():
    """Reproducible 'today' for the report date. SOURCE_DATE_EPOCH wins over wall clock."""
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        return datetime.datetime.fromtimestamp(
            int(epoch), tz=datetime.timezone.utc).date().isoformat()
    return datetime.date.today().isoformat()


if __name__ == "__main__":
    _ap = argparse.ArgumentParser()
    _ap.add_argument("--today", default=None, help="YYYY-MM-DD projection anchor")
    _ap.add_argument("--root", default=None, help="scratch root for data/ output (G-3)")
    _ap.add_argument("--validate", action="store_true", help="run self-test in a scratch root")
    _args = _ap.parse_args()
    if _args.validate:
        sys.exit(validate())
    if _args.root:
        set_root(_args.root)
    elif os.environ.get("FLEET_ROOT"):
        set_root(os.environ["FLEET_ROOT"])
    CLI_TODAY = _args.today


trades = list(csv.DictReader(open(os.path.join(D, "trades.csv"))))
bots = list(csv.DictReader(open(os.path.join(D, "bots.csv"))))

# --- G5 instruction-mirror compliance feed (from daily_brief.py) ----------
# data/compliance.csv carries one graded row per (bot, day). G5 lights when a
# bot has enough graded days AND averages >=90% instruction compliance. Absent
# file / too few days => G5 stays pending (honest: the daily brief hasn't run
# enough days yet), never a false pass.
G5_MIN_DAYS = 5
G5_THRESH = 90.0
compliance = collections.defaultdict(list)   # bot -> [compliance_pct, ...]
_comp_path = os.path.join(D, "compliance.csv")
if os.path.exists(_comp_path):
    for r in csv.DictReader(open(_comp_path)):
        v = fl(r.get("compliance_pct"))
        if r.get("compliance_pct") not in (None, "") and v is not None:
            compliance[r["bot"]].append(v)

def g5_eval(bot):
    """(value, detail) for the G5 gate. value True/False/None(pending)."""
    vals = compliance.get(bot, [])
    n = len(vals)
    if n < G5_MIN_DAYS:
        return (None, f"compliance {n}/{G5_MIN_DAYS} graded days (daily brief)")
    mean = sum(vals) / n
    if mean >= G5_THRESH:
        return (True, f"{mean:.0f}% mirror-compliance over {n} days")
    return (False, f"{mean:.0f}% < {G5_THRESH:.0f}% mirror-compliance over {n} days")

tot = sum(fl(t["pnl"]) for t in trades)
bypillar = collections.defaultdict(float)
byunder = collections.defaultdict(float)            # (pillar, underlying)
for t in trades:
    bypillar[t["pillar"]] += fl(t["pnl"])
    byunder[(t["pillar"], t["underlying"] or "—")] += fl(t["pnl"])

# champion: resolved from bots_meta.csv (champion=yes), NOT a hardcoded name
meta = {r["bot"]: r for r in csv.DictReader(open(os.path.join(D, "bots_meta.csv")))}
_ledger_path = os.path.join(ROOT, "docs", "pre-registration-ledger.md")
_ledger_unsigned = pre_registration_ledger.unsigned_from_ledger(_ledger_path)
unsigned_bots = sorted(b for b in meta if b in _ledger_unsigned)
champ = next((b for b, r in meta.items() if (r.get("champion") or "").lower() == "yes"), None)
champ_t = [t for t in trades if t["bot"] == champ]
champ_trades = len(set(t["trade_id"] for t in champ_t))
sd = collections.defaultdict(float)
for t in champ_t: sd[t["open_date"][:10]] += fl(t["pnl"])
green = sum(1 for v in sd.values() if v > 0)
red = sum(1 for v in sd.values() if v < 0)
champ_pnl = sum(fl(t["pnl"]) for t in champ_t)
# Gate = CLEAN post-fix condors: post-fix, and not single-sided (a side filtered
# for sub-min credit doesn't count as clean IC data, per the #1a single-sided rule).
post_trades = len(set(t["trade_id"] for t in champ_t
                      if t["epoch"] == "post-fix" and t["single_sided"] != "True"))
cum = peak = dd = 0.0
cumlist = []
for d in sorted(sd):
    cum += sd[d]; peak = max(peak, cum); dd = min(dd, cum - peak)
    cumlist.append({"d": d, "c": round(cum)})

ss = sum(1 for t in trades if t["single_sided"] == "True")
date = today_iso()

# --- R-metrics (normalized: Return on Risk = pnl/risk per leg) ------------
# allocation- and size-independent. R is the unit; the right summary column
# depends on the decision (kill / graduate / size). PROV_N = ranking cutoff.
PROV_N = 20
botmeta = {b["bot"]: b for b in bots}
rbybot = collections.defaultdict(list)
for t in trades:
    risk = fl(t["risk"])
    if risk > 0:
        rbybot[t["bot"]].append((t["open_date"], fl(t["pnl"]) / risk))

def rmetrics(bot):
    rs = [r for _, r in sorted(rbybot[bot])]
    n = len(rs)
    if n == 0: return None
    mean = sum(rs) / n
    sd = (sum((x - mean) ** 2 for x in rs) / n) ** 0.5 if n > 1 else 0.0
    wins = sum(1 for r in rs if r > 0)
    cum = peak = mdd = 0.0
    for r in rs:
        cum += r; peak = max(peak, cum); mdd = min(mdd, cum - peak)
    return {"n": n, "exp": mean, "tot": sum(rs), "sd": sd,
            "t": (mean / (sd / math.sqrt(n))) if sd > 0 else None,
            "wr": wins / n * 100, "mdd": mdd}

rm = {b: m for b in rbybot if (m := rmetrics(b))}
ranked = sorted((b for b in rm if rm[b]["n"] >= PROV_N), key=lambda b: -rm[b]["exp"])
prov = sorted((b for b in rm if rm[b]["n"] < PROV_N), key=lambda b: -rm[b]["exp"])
def tfmt(v): return "—" if v is None else (f"{v:.1f}" if abs(v) < 100 else "∞")

# --- STATUS.md -----------------------------------------------------------
# --- cutover receipt: STATUS must state the era it describes ------------
_lm_path = os.path.join(D, "ledger_meta.json")
_lm = json.load(open(_lm_path)) if os.path.exists(_lm_path) else {}
_ledger_start = _lm.get("ledger_start")
_cut = (f"> **POST-CUTOVER LEDGER — `LEDGER_START = {_ledger_start}`.** Every figure "
        f"below is drawn from positions **opened on or after** that date. The v1 era "
        f"is frozen in `data/archive/` and is never an input here."
        if _ledger_start else
        "> ⚠️ **NO `data/ledger_meta.json`** — the cutover date is unknown to this "
        "report. Re-run `scripts/build_ledger.py`. Do not quote these figures.")

L = [f"# Bot Fleet — STATUS  ·  generated {date}", "",
     "> **Numeric source of truth.** Auto-generated from `data/trades.csv` by "
     "`scripts/report.py`. Do not edit by hand. All figures are PAPER. Task backlog: "
     "`docs/backlog.md` (also in `dashboard.html`).", "",
     _cut, ""]
if not trades:
    L += ["## ⏳ EMPTY LEDGER — n=0", "",
          "**No positions have been opened since the cutover.** Every table below is "
          "empty by construction, not by failure. There is nothing here to read as a "
          "result: an absent number is not a zero, and a blank expectancy is not a "
          "flat one. This page becomes meaningful on the first post-cutover trading "
          "day.", ""]

if unsigned_bots:
    L += ["", "## ⚠️ UNSIGNED PRE-REGISTRATION BOTS — DO NOT SWITCH ON", "",
          "> The following bots have a pre-registration ledger entry with a blank, "
          "missing, or `NOT SIGNED` `SIGNED` line. No bot may be switched ON until "
          "the entry is signed and dated.", ""]
    for b in unsigned_bots:
        L.append(f"- {b}")
    L.append("")

L += ["## Headline",
     f"- **Total closed P/L:** ${tot:,.0f}  ·  {len(trades)} legs  ·  {len(bots)} bots"]
for p in sorted(bypillar):
    subs = "  ·  ".join(f"{u} ${byunder[(p,u)]:,.0f}"
                        for (pp, u) in sorted(byunder) if pp == p and u != "—")
    L.append(f"  - {p}: ${bypillar[p]:,.0f}" + (f"  ({subs})" if subs else ""))
L += ["", f"## Champion — {champ or '(none flagged in bots_meta.csv)'}",
      f"- P/L **${champ_pnl:,.0f}**  ·  {champ_trades} condors ({len(champ_t)} legs)  ·  "
      f"{len(sd)} trading days ({green} green / {red} red)",
      f"- Max drawdown (daily cumulative): ${dd:,.0f}", ""]

# --- Roster by STATE (mirrors the OA groups) --------------------------------
# State rule (matches the OA Bot Groups): focus=yes -> Focus (*-Focus groups);
# ON & not focus -> Monitor; OFF -> Archive. All three are derivable from
# bots_meta's focus flag + status, so the local view and OA stay in agreement.
_order = {"IC": 0, "Directional": 1, "OA-Mirror": 2, "Lab": 3}
def _state(b):
    if (meta.get(b["bot"], {}).get("focus") == "yes"): return "Focus"
    return "Monitor" if b["status"].upper() == "ON" else "Archive"
def _roster(title, sub, want):
    rs = [b for b in bots if _state(b) == want]
    if not rs: return []
    out = [f"## {title}", f"> {sub}", "",
           "| Pillar | Bot | Status | Trades | P/L | WR |", "|---|---|---|--:|--:|--:|"]
    tot = 0.0
    for b in sorted(rs, key=lambda x: (_order.get(x["pillar"], 9), fl(x["total_pnl"]))):
        tot += fl(b["total_pnl"])
        out.append(f'| {b["pillar"]} | {b["bot"]} | {b["status"]} | {b["n_trades"]} | '
                   f'${fl(b["total_pnl"]):,.0f} | {b["win_rate_trade"]} |')
    out += [f'| **Total** | | | | **${tot:,.0f}** | |', ""]
    return out
L += _roster("Focus roster — the bots you're actively perfecting  (OA: `*-Focus` groups)",
             "Close-to-live per pillar; for an A/B only the leading side. Select one group = per-pillar, "
             "all three = combined. Read per-bot R (readiness board), not the subtotal.", "Focus")
L += _roster("Monitor — live but not focus  (OA: `Monitor` group)",
             "Running and watched — A/B laggards, controls, other active mirrors, the pending-decision "
             "QQQ-Fortress pair. Not promotion candidates yet.", "Monitor")
_arch = [b for b in bots if _state(b) == "Archive"]
if _arch:
    L += [f"**Archive (OA: `Archive` group):** {len(_arch)} off/dead bots · "
          f"${sum(fl(b['total_pnl']) for b in _arch):,.0f} closed — excluded from the working view "
          f"(still exported for the ledger).", ""]

# ======================================================================
# ALLOCATION AUDIT (per-position sizing realism — ON bots)
# ----------------------------------------------------------------------
# R normalizes size away, so this does NOT change any ranking — it flags
# whether the PAPER sizing is realistic to carry to live. Grain = position
# (trade_id; legs share the position-level defined risk). Hold class matters:
# a 0DTE bot recycles its risk daily; a multi-week bot ties capital up for the
# whole hold, so "max risk/day" means concurrent open risk, not daily deploy.
def _pos_agg():
    from collections import defaultdict
    byid = defaultdict(list)
    for t in trades:
        byid[t["trade_id"]].append(t)
    agg = defaultdict(lambda: {"q": [], "risk": [], "dte": []})
    for tid, legs in byid.items():
        b = legs[0]["bot"]
        q = max(fl(l["quantity"]) for l in legs)
        risk = max(fl(l["risk"]) for l in legs)
        a = agg[b]; a["q"].append(q); a["risk"].append(risk)
        try:
            o = legs[0]["open_date"][:10].split("-")
            e = (legs[0]["expiration"] or legs[0]["close_date"])[:10].split("-")
            d = (datetime.date(*map(int, e)) - datetime.date(*map(int, o))).days
            a["dte"].append(d)
        except Exception:
            pass
    return agg
def _med(xs):
    xs = sorted(xs); n = len(xs)
    return xs[n // 2] if n else 0
_alloc = _pos_agg()
L += ["## Allocation audit — sizing realism  (ON bots, per-position)",
      "> R (pnl÷risk) already cancels size, so this changes **no ranking** — it flags whether the "
      "paper sizing is realistic to carry live. Hold class sets the rule: **0DTE** recycles risk "
      "daily; **swing/multi-week** ties capital up for the whole hold (max-risk/day = concurrent open "
      "risk, not daily deploy). **1-lot bots are fill-untested at scale** — their edge won't survive "
      "the slippage of a real order size (ties to the v5-slippage task).", "",
      "| Bot | Pillar | Hold | Pos | med Qty | med Risk$ | max Risk$ | Realism |",
      "|---|---|---|--:|--:|--:|--:|:--|"]
_on = [b for b in bots if b["status"].upper() == "ON"]
_alloc_rows_written = 0
for b in sorted(_on, key=lambda x: (_order.get(x["pillar"], 9), -_med(_alloc[x["bot"]]["risk"]))):
    a = _alloc.get(b["bot"])
    if not a or not a["risk"]: continue
    _alloc_rows_written += 1
    dte = _med(a["dte"]) if a["dte"] else 0
    hold = "0DTE" if dte == 0 else (f"{dte:.0f}d swing" if dte < 10 else f"{dte:.0f}d multi-wk")
    mq = _med(a["q"])
    flag = ("**1-lot — fill-untested**" if mq <= 1
            else ("sized ✓" if _med(a["risk"]) >= 3000 else "small — verify vs OA alloc"))
    L.append(f'| {b["bot"]} | {b["pillar"]} | {hold} | {len(a["q"])} | {mq:.0f} | '
             f'${_med(a["risk"]):,.0f} | ${max(a["risk"]):,.0f} | {flag} |')
# Interpretive commentary is suppressed when its table is empty — a hardcoded
# "Read:" paragraph asserting facts about bots with no data is exactly the kind
# of confident-sounding stale narrative this rebuild exists to remove.
if _alloc_rows_written:
    L += ["", "> **Read:** SPX-IC + Nigiri run ~10-lot (~$4.8k/position, comparable to the champion). Every "
      "other mirror + both directional bots run **1 lot** ($0.5k–$2.9k) — realistic for tracking W/L, "
      "not for reading a live-scale edge. Sizing rule is per-bot by hold class (see backlog COCKPIT LANE "
          "step 1); the go-live target is ~$10k max risk/day with a hedge reserve carved out first.", ""]

# ======================================================================
# HEDGE TOURNAMENT (live-data counterfactual — data/hedge_tournament.csv)
# ----------------------------------------------------------------------
# Built by scripts/hedge_tournament.py: replays every REAL, SETTLED (status=
# expired) leg through the v1 hedge library (Ride / PT+X% / SL-X% / S2 touch-
# cut / Defang-deferred) and books R = modeled_pnl/risk per (leg, rule). This
# section just aggregates and ranks what's already on disk — no modeling here.
# Absent file => section is skipped entirely (honest: hasn't been run yet).
_ht_path = os.path.join(D, "hedge_tournament.csv")
if os.path.exists(_ht_path):
    ht_rows = [r for r in csv.DictReader(open(_ht_path)) if r.get("R") not in (None, "")]

    def _ht_stats(rs):
        """Exp(R)/Tot R/WR/maxDD-R/worst-R for one rule's rows, walking the
        cumulative-R drawdown in chronological (date, trade_id) order."""
        n = len(rs)
        if n == 0:
            return None
        vals = [fl(r["R"]) for r in rs]
        mean = sum(vals) / n
        wins = sum(1 for v in vals if v > 0)
        ordered = sorted(rs, key=lambda r: (r["date"], r["trade_id"]))
        cum = peak = mdd = 0.0
        worst = None
        for r in ordered:
            v = fl(r["R"])
            cum += v; peak = max(peak, cum); mdd = min(mdd, cum - peak)
            worst = v if worst is None else min(worst, v)
        return {"n": n, "exp": mean, "tot": sum(vals), "wr": wins / n * 100,
                "mdd": mdd, "worst": worst}

    RULE_ORDER = ["ride", "pt25", "pt50", "pt100", "sl50", "sl75", "sl100", "sl130", "s2"]
    by_rule = collections.defaultdict(list)
    for r in ht_rows:
        by_rule[r["rule"]].append(r)
    n_defang = sum(1 for r in csv.DictReader(open(_ht_path)) if r["rule"] == "defang")

    L += ["## Hedge tournament (live-data counterfactual)",
          "> **The productized loss autopsy.** Every real, settled (status=expired) leg replayed "
          "through the v1 hedge library — Ride/no-stop, PT+X%/SL-X% return-threshold rules, and "
          "an S2 strike-touch cut (tape-gated, 5-min grain). **Optimistic bound, not a live "
          "estimate** — every non-Ride arm assumes a fill exactly at the threshold; real fills "
          "slip. Compare rules by **R** (pnl÷risk), never $. Basis: PT/SL % are of the credit "
          "collected (`|premium|`), per `mfe_pct`/`mae_pct` already carrying that unit (verified "
          "against the ledger — see `scripts/hedge_tournament.py` docstring). "
          f"**Defang: deferred v1** ({n_defang} legs marked, not modeled — needs an intraday "
          "premium-decay path not yet in the ledger).",
          "",
          "| Rule | N | Exp(R) | Tot R | WR | maxDD-R | worst-R |",
          "|---|--:|--:|--:|--:|--:|--:|"]
    for rule in RULE_ORDER:
        st = _ht_stats(by_rule.get(rule, []))
        if st is None:
            note = " (no legs — S2 needs a tape file for that day/underlying)" if rule == "s2" else " (no legs)"
            L.append(f"| {rule} | 0 | — | — | — | — | —{note} |")
            continue
        L.append(f"| {rule} | {st['n']} | {st['exp']*100:+.1f}% | {st['tot']:+.2f} | "
                  f"{st['wr']:.0f}% | {st['mdd']:.2f} | {st['worst']*100:+.1f}% |")

    # --- per-bot cut (Ride vs SL75, the mid-spectrum published rung) ---------
    L += ["", "#### Per-bot cut  (Ride vs SL75 — the mid-spectrum published rung)",
          "| Bot | N | Ride Exp(R) | SL75 Exp(R) | Δ |",
          "|---|--:|--:|--:|--:|"]
    ride_by_bot = collections.defaultdict(list)
    sl75_by_bot = collections.defaultdict(list)
    for r in ht_rows:
        if r["rule"] == "ride":
            ride_by_bot[r["bot"]].append(fl(r["R"]))
        elif r["rule"] == "sl75":
            sl75_by_bot[r["bot"]].append(fl(r["R"]))
    for bot in sorted(ride_by_bot, key=lambda b: -sum(ride_by_bot[b])):
        rr = ride_by_bot[bot]
        sr = sl75_by_bot.get(bot, [])
        if not rr:
            continue
        re_ = sum(rr) / len(rr)
        if sr:
            se_ = sum(sr) / len(sr)
            se_fmt, delta = f"{se_*100:+.1f}%", f"{(se_-re_)*100:+.1f}pp"
        else:
            se_fmt, delta = "—", "—"
        L.append(f"| {bot} | {len(rr)} | {re_*100:+.1f}% | {se_fmt} | {delta} |")

    # --- regime cut -----------------------------------------------------------
    L += ["", "#### Regime cut  (Ride vs SL75, by tape-derived regime label)",
          "| Regime | N | Ride Exp(R) | SL75 Exp(R) |",
          "|---|--:|--:|--:|"]
    ride_by_regime = collections.defaultdict(list)
    sl75_by_regime = collections.defaultdict(list)
    for r in ht_rows:
        if r["rule"] == "ride":
            ride_by_regime[r["regime"]].append(fl(r["R"]))
        elif r["rule"] == "sl75":
            sl75_by_regime[r["regime"]].append(fl(r["R"]))
    for reg in sorted(ride_by_regime, key=lambda x: (x == "n/a", x)):
        rr = ride_by_regime[reg]
        sr = sl75_by_regime.get(reg, [])
        re_ = sum(rr) / len(rr) if rr else 0.0
        se_ = f"{(sum(sr)/len(sr))*100:+.1f}%" if sr else "—"
        L.append(f"| {reg} | {len(rr)} | {re_*100:+.1f}% | {se_} |")
    L += ["", "> N is small and concentrated in the last few tape-covered trading days (tape.py "
          "is new); the S2 arm and the regime cut will thicken as more days accrue. Read this as "
          "an early ranking to cross-check the LEAN/OA backtest tournament, not a standalone "
          "verdict.", ""]

# ======================================================================
# TRADE-WINDOW HEAT MAP (when do shorts get touched — data/trade_window.csv)
# ----------------------------------------------------------------------
# Built by scripts/trade_window.py: buckets every ledger position's worst-
# excursion (MAE) timestamp by hour-of-day x tape-derived regime, plus a
# same-day-tape-only touch rate (short strike vs post-entry intraday path).
# This section just renders what's already on disk. Absent file => skipped
# (honest: hasn't been run yet).
_tw_path = os.path.join(D, "trade_window.csv")
if os.path.exists(_tw_path):
    tw_rows = list(csv.DictReader(open(_tw_path)))
    _TW_HOURS = ["09:30-10", "10-11", "11-12", "12-13", "13-14", "14-15", "15-16"]
    _TW_REGIMES = ["Chop", "Drift", "Trend", "n/a"]
    tw_by_key = {(r["hour"], r["regime"]): r for r in tw_rows}
    hours_present = [h for h in _TW_HOURS if any(k[0] == h for k in tw_by_key)]
    regimes_present = [g for g in _TW_REGIMES if any(k[1] == g for k in tw_by_key)]

    def _tw_cell(h, g):
        r = tw_by_key.get((h, g))
        if not r:
            return "—"
        n = int(r["n_positions"])
        tr = r["touch_rate"]
        mae = r["avg_mae_pct"]
        parts = [f"n={n}"]
        if tr not in (None, ""):
            parts.append(f"touch {float(tr)*100:.0f}%")
        if mae not in (None, ""):
            parts.append(f"MAE {float(mae):+.1f}%")
        return " · ".join(parts)

    L += ["## Trade-window heat map — when do shorts actually get touched (hour x regime)",
          "> **The 11am-vs-1:30 question, generalized.** Every ledger position's worst-adverse-"
          "excursion (MAE) timestamp, bucketed by hour-of-day x tape-derived regime (Drift/Trend/"
          "Chop/n-a). `touch %` = short-strike touch rate, scored only on positions with same-day "
          "tape coverage (a small, recent subset — most history predates `tape.py`); `MAE` = mean "
          "adverse excursion as % of credit, computed on ALL positions in the bucket regardless of "
          "tape coverage. Cells are `n=… · touch …% · MAE …%`; blank touch% = no tape-covered "
          "position fell in that cell. **Small-n cells are directional, not conclusive** — read the "
          "n before the rate.",
          "",
          "| Hour | " + " | ".join(regimes_present) + " |",
          "|---|" + "---|" * len(regimes_present)]
    for h in hours_present:
        L.append(f"| {h} | " + " | ".join(_tw_cell(h, g) for g in regimes_present) + " |")

    # one-line read: which (hour, regime) cell has the highest tape-covered touch rate
    scored = [(r["hour"], r["regime"], int(r["n_positions"]), int(r["n_touches"]),
               float(r["touch_rate"])) for r in tw_rows if r["touch_rate"] not in (None, "")]
    if scored:
        worst = max(scored, key=lambda x: (x[4], x[3]))
        h, g, n_pos, n_touch, rate = worst
        denom = round(n_touch / rate) if rate else n_touch
        L.append("")
        L.append(f"> **Read:** touches cluster at **{h} ({g})** — "
                 f"{n_touch} of {denom} tape-covered position(s) scored there touched "
                 f"(touch rate {rate*100:.0f}%). Tape coverage is thin (5 days) — treat as "
                 "an early signal, not a verdict.")
    L.append("")

# ======================================================================
# LESSONS INDEX (searchable, tagged — data/lessons.csv)
# ----------------------------------------------------------------------
# Built by scripts/lessons.py: pulls each graded bot-day's "day's lesson"
# out of the brief JSON's Verdict row (fallback: docs/session-log.md, only
# for dates with no brief coverage at all), tags it from a fixed vocabulary
# (entry-timing/hedge/filter/regime/sizing/other) via keyword rules. This
# section renders what's on disk — no tagging logic here. Absent file =>
# skipped (honest: hasn't been run yet).
_lessons_path = os.path.join(D, "lessons.csv")
if os.path.exists(_lessons_path):
    lesson_rows = list(csv.DictReader(open(_lessons_path)))
    _LESSON_TAGS = ["entry-timing", "hedge", "filter", "regime", "sizing", "other"]
    tag_counts = collections.Counter(r["tag"] for r in lesson_rows)
    by_tag = collections.defaultdict(list)
    for r in lesson_rows:
        by_tag[r["tag"]].append(r)

    L += ["## Lessons index — tagged, searchable  (data/lessons.csv)",
          "> Every graded bot-day's \"day's lesson\" (from the brief JSON's Verdict row; "
          "session-log fallback only for dates the brief never covered), tagged from a fixed "
          "vocabulary (`entry-timing · hedge · filter · regime · sizing · other`) by simple "
          "keyword rules (see `scripts/lessons.py` docstring) — not an ML classifier. Grouped by "
          "tag, most recent first.",
          "",
          "**Tag counts:** " + "  ·  ".join(
              f"{t} {tag_counts[t]}" for t in _LESSON_TAGS if tag_counts.get(t)),
          ""]
    for tag in sorted(by_tag, key=lambda t: -tag_counts[t]):
        rs = sorted(by_tag[tag], key=lambda r: r["date"], reverse=True)
        L.append(f"#### {tag} ({len(rs)})")
        for r in rs:
            L.append(f"- **{r['date']}** · {r['bot']} — {r['lesson']}")
        L.append("")

L += ["## Per-bot (sorted by P/L)",
      "| Bot | Pillar | Und | Role | Status | Trades | Legs | P/L | WR | Fix? |",
      "|---|---|---|---|---|--:|--:|--:|--:|:--:|"]
for b in bots:
    L.append(f'| {b["bot"]} | {b["pillar"]} | {b["underlying"] or "—"} | {b["role"]} | '
             f'{b["status"]} | {b["n_trades"]} | {b["n_legs"]} | ${fl(b["total_pnl"]):,.0f} | '
             f'{b["win_rate_trade"]} | {b["needs_strike_fix"] or "-"} |')
# ======================================================================
# READINESS BOARD (per-CONDOR grain; 6 ordered gates; bootstrap CI)
# ----------------------------------------------------------------------
# Answers "which bots are close to live, and what's the ONE blocker" — the
# view the flat scorecard couldn't give. Grain = condor (legs summed), NOT leg.
# Stage ladder INCUBATE→VALIDATE→CANDIDATE→LIVE-READY (LIVE = real capital).
# First gate that's RED (fails) = the named blocker. Controls & mirror-watch
# are flagged non-graduating (they can't go live by design).
random.seed(7)
MAXDD_R_CAP = -5.0        # maxDD-R floor for G4 (RoE $ cap still a <FILL> blank)
BOOT_B = 3000             # bootstrap resamples

def pctile(sorted_xs, q):
    if not sorted_xs: return None
    i = q / 100 * (len(sorted_xs) - 1)
    lo = int(math.floor(i)); hi = int(math.ceil(i))
    if lo == hi: return sorted_xs[lo]
    return sorted_xs[lo] + (sorted_xs[hi] - sorted_xs[lo]) * (i - lo)

def boot_ci(rs):
    """Bootstrap 95% CI of the mean R (replaces the t-stat)."""
    n = len(rs)
    if n < 2: return (None, None)
    means = sorted(sum(random.choices(rs, k=n)) / n for _ in range(BOOT_B))
    return (pctile(means, 2.5), pctile(means, 97.5))

# --- aggregate legs → condors, keyed by trade_id -----------------------
#
# ⛔ RISK = THE LARGER SIDE, NEVER THE SUM.  (fixed 2026-07-31, Andy's ruling)
#
# A condor can only lose ONE side. Summing both sides' risk inflates the
# denominator and flatters Exp(R) toward zero — it makes a losing book look
# less negative and a winning one look less positive. The independent audit
# identified this as its single *stricter* revision and the project adopted the
# larger-side rule in four separate documents (CLAUDE.md §4, build-plan.md §5,
# rebuild-audit, the audit itself) — but this line kept summing, so every
# Exp(R) in STATUS.md and both code-enforced gates (G3 edge, G4 maxDD-R) ran on
# the wrong denominator. See docs/evidence-standards.md §6.2.
#
# max() is correct for every structure, not just condors:
#   two paired spread rows  -> the larger side, which is the real max loss
#   one `ironcondor` row    -> max of one value = itself, unchanged
#   a single-sided spread   -> its own risk, unchanged
# So this is a no-op for every non-paired structure and only bites where it
# should. The archive ledger stays frozen as-computed; this changes reporting
# going forward, and the working ledger is empty, so no live number moved.
cond = collections.defaultdict(lambda: {"pnl": 0.0, "risk": 0.0, "date": "9999-99-99",
                                         "epoch": "", "ss": False})
cond_bot = {}
for t in trades:
    k = t["trade_id"]; c = cond[k]
    c["pnl"] += fl(t["pnl"])
    c["risk"] = max(c["risk"], fl(t["risk"]))      # larger side, NOT the sum
    c["date"] = min(c["date"], t["open_date"][:10])
    c["epoch"] = t["epoch"]
    if t["single_sided"] == "True": c["ss"] = True
    cond_bot[k] = t["bot"]

# clean per-bot condor-R series (post-fix/baseline epoch, risk>0).
# Single-sided handling: the ledger flags an unpaired call/put spread as
# `single_sided`. For an IC bot that's an anomaly day (drop it); but for a
# single-structure bot (mirror bots that trade ONE spread by design) EVERY
# trade is "single-sided" — those ARE its real trades, so keep them. Rule:
# drop single-sided days only when the bot also has paired condors.
_by_bot_all = collections.defaultdict(list)      # bot -> [(date, R, ss)]
for k, b in cond_bot.items():
    c = cond[k]
    if c["risk"] <= 0 or c["epoch"] == "pre-fix": continue
    _by_bot_all[b].append((c["date"], c["pnl"] / c["risk"], c["ss"]))
bot_rs = {}                                        # bot -> [(date, R)]
for b, lst in _by_bot_all.items():
    paired = [(d, r) for d, r, ss in lst if not ss]
    bot_rs[b] = paired if paired else [(d, r) for d, r, ss in lst]

def gate_eval(bot):
    """Return (dots, stage, blocker, n, mean, ci, needed) for one bot."""
    role = botmeta.get(bot, {}).get("role", "")
    fix  = botmeta.get(bot, {}).get("needs_strike_fix", "")
    series = sorted(bot_rs.get(bot, []))
    rs = [r for _, r in series]
    n = len(rs)
    mean = sum(rs) / n if n else 0.0
    sd = (sum((x - mean) ** 2 for x in rs) / n) ** 0.5 if n > 1 else 0.0
    ci = boot_ci(rs) if n >= 2 else (None, None)
    # cumulative-R drawdown
    cum = peak = mdd = 0.0
    for _, r in series:
        cum += r; peak = max(peak, cum); mdd = min(mdd, cum - peak)

    # --- the six ordered gates: value True/False/None(pending) + detail ---
    g = []
    # G1 clean data
    if fix == "Y": g.append((False, "strike-bug contamination"))
    else:          g.append((True,  "clean"))
    # G2 sample (>=20 clean condors)
    g.append((n >= 20, f"{n} clean condors (need 20)"))
    # G3 edge: Exp(R)>0 AND bootstrap 95% CI lower bound >0
    lo, hi = ci
    needed = None
    if n < 2:
        g.append((False, "n<2, no CI"))
    elif mean <= 0:
        g.append((False, "negative/zero edge"))
    elif lo is not None and lo > 0:
        g.append((True, "CI above 0"))
    else:
        # trades needed for the CI to clear zero at current mean/sd (normal approx)
        if sd > 0 and mean > 0:
            n_need = math.ceil((1.96 * sd / mean) ** 2)
            needed = max(0, n_need - n)
        g.append((False, f"CI includes 0 (~{needed} more trades)" if needed
                         else "CI includes 0"))
    # G4 risk: maxDD-R within cap (RoE $ cap still a <FILL> blank -> that half pending)
    g.append((mdd >= MAXDD_R_CAP, f"maxDD-R {mdd:.1f} (RoE $ cap pending)"))
    # G5 compliance: instruction-mirror >=90% graded days -> from the daily brief (data/compliance.csv)
    g.append(g5_eval(bot))
    # G6 robustness: OOS half-split positive + not >60% single-year concentrated
    if n >= 20:
        mid = n // 2
        h1 = sum(rs[:mid]) / mid if mid else 0.0
        h2 = sum(rs[mid:]) / (n - mid) if n - mid else 0.0
        oos_ok = h1 > 0 and h2 > 0
        years = collections.Counter()
        for d, r in series:
            if r > 0: years[d[:4]] += r
        tot_pos = sum(years.values())
        multiyear = len({d[:4] for d, _ in series}) >= 2
        conc_ok = True
        if multiyear and tot_pos > 0:
            conc_ok = (max(years.values()) / tot_pos) <= 0.60
        detail = "OOS both-halves +" if oos_ok else f"OOS split ({h1:+.1%}/{h2:+.1%})"
        if oos_ok and not conc_ok: detail = ">60% one-year concentrated"
        g.append((oos_ok and conc_ok, detail))
    else:
        g.append((None, "n<20, robustness N/A"))

    names = ["G1", "G2", "G3", "G4", "G5", "G6"]
    dots = "".join("●" if v is True else ("○" if v is False else "·") for v, _ in g)
    passed = sum(1 for v, _ in g if v is True)
    # blocker = first RED (False) in order; else first PENDING (None); else clear
    blocker = "— all gates clear"
    for nm, (v, d) in zip(names, g):
        if v is False: blocker = f"{nm}: {d}"; break
    else:
        for nm, (v, d) in zip(names, g):
            if v is None: blocker = f"{nm}: {d}"; break
    # stage
    if role in ("control", "mirror-watch"):
        stage = "CONTROL" if role == "control" else "MIRROR-WATCH"
    else:
        stage = ["INCUBATE", "VALIDATE", "VALIDATE", "CANDIDATE",
                 "CANDIDATE", "LIVE-READY", "LIVE-READY"][passed]
    return dots, stage, blocker, n, mean, ci, needed, passed, role

board = {b: gate_eval(b) for b in bot_rs}
grad = sorted((b for b in board if board[b][8] not in ("control", "mirror-watch")),
              key=lambda b: (-board[b][7], -board[b][4]))
nongrad = sorted((b for b in board if board[b][8] in ("control", "mirror-watch")),
                 key=lambda b: (-board[b][7], -board[b][4]))

def cifmt(ci):
    lo, hi = ci
    if lo is None: return "—"
    return f"[{lo*100:+.1f}, {hi*100:+.1f}]"

L += ["", "## Readiness board — per-condor, gated (the graduation view)",
      "> **Grain = condor** (legs summed), not leg. Six ordered gates; the **first red (○) gate "
      "is the named blocker**. `●`=pass `○`=fail `·`=pending. Exp(R) shows the **bootstrap 95% CI** "
      "(replaces the t-stat). Stage: INCUBATE→VALIDATE→CANDIDATE→LIVE-READY (LIVE = real capital). "
      "Controls & mirror-watch are listed separately — they can't graduate by design.",
      "> **Gates:** G1 clean data (no strike-bug, single-sided excluded) · G2 ≥20 clean condors · "
      "G3 Exp(R)>0 w/ 95% CI above 0 · G4 maxDD-R within cap (RoE $ cap still a `<FILL>` blank) · "
      f"G5 instruction-mirror ≥{G5_THRESH:.0f}% (from the daily brief / `data/compliance.csv`; "
      f"pending until ≥{G5_MIN_DAYS} graded days) · G6 OOS/regime robustness.",
      "",
      "| Bot | Role | Stage | Gates | n | Exp(R) [95% CI] | Blocker |",
      "|---|---|---|:--:|--:|--:|---|"]
for b in grad:
    dots, stage, blocker, n, mean, ci, needed, passed, role = board[b]
    L.append(f"| {b} | {role} | {stage} | {dots} | {n} | {mean*100:+.1f}% {cifmt(ci)} | {blocker} |")
L += ["", "#### Non-graduating (controls / mirror-watch — tracked, can't go live)",
      "| Bot | Role | Gates | n | Exp(R) [95% CI] | Note |",
      "|---|---|:--:|--:|--:|---|"]
for b in nongrad:
    dots, stage, blocker, n, mean, ci, needed, passed, role = board[b]
    L.append(f"| {b} | {role} | {dots} | {n} | {mean*100:+.1f}% {cifmt(ci)} | {blocker} |")

L += ["", "## Scorecard — normalized (Return on Risk) · legacy per-LEG view",
      "> ⚠️ **Per-LEG grain** (kept for continuity) — for the graduation decision use the "
      "**Readiness board** above (per-condor, gated). Each trade = **pnl ÷ capital-at-risk** (\"R\"), "
      "so allocation and contract size cancel out. Sorted by expectancy. t-stat blows up for "
      "low-variance grinders (e.g. 3DTE) — don't rank on it alone.",
      "",
      f"### Ranked (n ≥ {PROV_N})",
      "| Bot | Pillar | n | Exp(R) | t | Tot R | maxDD-R | WR |",
      "|---|---|--:|--:|--:|--:|--:|--:|"]
for b in ranked:
    m = rm[b]; p = botmeta[b]["pillar"]
    L.append(f"| {b} | {p} | {m['n']} | {m['exp']:+.3f} | {tfmt(m['t'])} | "
             f"{m['tot']:+.1f} | {m['mdd']:.1f} | {m['wr']:.0f}% |")
L += ["", f"### Provisional (n < {PROV_N} — tracked, not ranked; samples too small to trust)",
      "| Bot | Pillar | n | Exp(R) | Tot R | raw P/L |",
      "|---|---|--:|--:|--:|--:|"]
for b in prov:
    m = rm[b]; p = botmeta[b]["pillar"]
    L.append(f"| {b} | {p} | {m['n']} | {m['exp']:+.3f} | {m['tot']:+.1f} | "
             f"${fl(botmeta[b]['total_pnl']):,.0f} |")
L += ["",
      "### Decision rules (read against the right column)",
      "- **Kill** — Exp(R) < 0 held with conviction (|t| ≳ 2, or n large). Raw P/L size is irrelevant.",
      "- **Graduate** — Exp(R) > 0 **and** |t| ≳ 2 **and** n ≥ threshold (edge is real, not noise).",
      "- **Size live capital** — among graduates, weight by Tot R + low maxDD-R (consistency); never size on raw P/L.",
      "- **Exp(R)** = avg return per $1 risked. **Tot R** = size-free analog of total P/L. "
      "**maxDD-R** = worst cumulative-R drawdown (risk shape). **t** = evidence the edge is real."]

L += decidability_countdown(
    trades, meta,
    resolve_report_today(CLI_TODAY, os.environ.get("STATUS_TODAY"),
                         os.environ.get("SOURCE_DATE_EPOCH"), _ledger_start, trades),
    _ledger_start)

L += ["", "## Caveats",
      "- **Trades = condors** (the two legs of one entry paired); **Legs = OA position "
      "rows** (matches OA's \"Positions\" count). Win rate shown is per-condor.",
      "- A combined-`ironcondor` bot logs 1 leg per condor; a legged bot logs 2 — so Legs "
      "≈ 2× Trades only for legged bots. That's why they were confusing before.",
      "- `Fix? = Y`: QQQ-IC bot carrying the call-side strike-resolution bug; data "
      "contaminated until fixed.",
      f"- Single-sided condors (only one leg opened): {ss} legs flagged.",
      "- Tiny-N bots are tracked but **not** evidence; read Trades before P/L."]
open(os.path.join(ROOT, "STATUS.md"), "w").write("\n".join(L) + "\n")

# --- backlog ---------------------------------------------------------------
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    return s
backlog_html = ""
bl = os.path.join(ROOT, "docs", "backlog.md")
if os.path.exists(bl):
    groups, cur = [], None
    for line in open(bl):
        line = line.rstrip("\n")
        m = re.match(r"^## (.+)", line)
        if m: cur = {"name": m.group(1), "items": []}; groups.append(cur); continue
        m = re.match(r"^- (.+)", line)
        if m and cur is not None: cur["items"].append(m.group(1))
    parts = []
    for g in groups:
        if not g["items"]: continue
        parts.append(f'<h3>{esc(g["name"])} <span class="ct">{len(g["items"])}</span></h3><ul>')
        for it in g["items"]: parts.append(f"<li>{inline(it)}</li>")
        parts.append("</ul>")
    backlog_html = "".join(parts)

# --- dashboard.html -------------------------------------------------------
rows_json = json.dumps([{"bot": b["bot"], "proj": b["pillar"], "status": b["status"],
    "trades": int(b["n_trades"]), "legs": int(b["n_legs"]), "pnl": round(fl(b["total_pnl"])),
    "wr": b["win_rate_trade"], "fix": b["needs_strike_fix"]} for b in bots])

TPL = r"""<!doctype html>
<script type="application/json" id="cowork-artifact-meta">
{ "name": "Bot Fleet Dashboard", "schemaVersion": 1, "description": "Bot Fleet status + backlog, generated from the local ledger (data/trades.csv + docs/backlog.md). Static snapshot; refreshed by the daily task.", "mcpTools": [], "mcpServerNames": [] }
</script>
<html><head><meta charset="utf-8">
<title>Bot Fleet Status</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.5.0/dist/chart.umd.js" integrity="sha384-iU8HYtnGQ8Cy4zl7gbNMOhsDTTKX02BTXptVP/vqAWIaTfM7isw76iyZCsjL2eVi" crossorigin="anonymous"></script>
<style>
body{font-family:system-ui,Arial,sans-serif;margin:24px;color:#1a1a1a;max-width:920px}
h1{font-size:20px;margin:0 0 2px}.sub{color:#777;font-size:12px}
.card{display:inline-block;border:1px solid #eee;border-radius:8px;padding:8px 16px;margin:12px 8px 4px 0}
.card span{color:#777;font-size:12px}.card b{display:block;font-size:18px}
table{border-collapse:collapse;width:100%;font-size:13px;margin-top:18px}
th,td{border-bottom:1px solid #eee;padding:6px 8px;text-align:right}
th:first-child,td:first-child{text-align:left}
.neg{color:#c0392b}.pos{color:#1e7e34}.off{color:#bbb}
canvas{margin-top:16px;max-height:240px}
h2{font-size:15px;margin:30px 0 6px;border-top:1px solid #eee;padding-top:18px}
#bl h3{font-size:11.5px;text-transform:uppercase;letter-spacing:.05em;color:#555;margin:16px 0 5px}
#bl .ct{color:#bbb;font-weight:400}#bl ul{margin:0;padding-left:18px}#bl li{margin:3px 0;font-size:13px}
code{background:#f0f0f3;padding:1px 4px;border-radius:4px;font-size:12px}
</style></head><body>
<h1>Bot Fleet — Status</h1>
__UNSIGNED__
<div class="sub">generated __DATE__ · PAPER · source: data/trades.csv + docs/backlog.md</div>
<div>
<div class="card"><span>Total P/L</span><b class="__TOTC__">$__TOT__</b></div>
<div class="card"><span>Legs</span><b>__NLEGS__</b></div>
<div class="card"><span>Bots</span><b>__NBOTS__</b></div>
<div class="card"><span>Scalp P/L</span><b class="__SCALPC__">$__SCALP__</b></div>
</div>
<canvas id="ch"></canvas>
<h2>Per-bot</h2>
<table id="t"><thead><tr><th>Bot</th><th>Proj</th><th>Status</th><th>Trades</th><th>Legs</th>
<th>P/L</th><th>WR</th><th>Fix?</th></tr></thead><tbody></tbody></table>
<div class="sub" style="margin-top:6px">Trades = condors · Legs = OA position rows (≈2× trades for legged bots) · WR is per-condor</div>
<h2>Backlog</h2><div id="bl">__BACKLOG__</div>
<script>
const rows=__ROWS__, cum=__CUM__;
const tb=document.querySelector('#t tbody');
rows.sort((a,b)=>a.pnl-b.pnl).forEach(r=>{
 const tr=document.createElement('tr');
 tr.innerHTML='<td>'+r.bot+'</td><td>'+r.proj+'</td>'+
  '<td class="'+(r.status==='OFF'?'off':'')+'">'+r.status+'</td>'+
  '<td>'+r.trades+'</td><td>'+r.legs+'</td>'+
  '<td class="'+(r.pnl<0?'neg':'pos')+'">$'+r.pnl.toLocaleString()+'</td>'+
  '<td>'+r.wr+'</td><td>'+(r.fix||'-')+'</td>';
 tb.appendChild(tr);
});
new Chart(document.getElementById('ch'),{type:'line',
 data:{labels:cum.map(x=>x.d),datasets:[{label:'Scalp-SPX cumulative P/L',
  data:cum.map(x=>x.c),borderColor:'#2962ff',backgroundColor:'rgba(41,98,255,.08)',
  fill:true,tension:.2,pointRadius:0}]},
 options:{plugins:{legend:{display:true}},scales:{x:{ticks:{maxTicksLimit:8}}}}});
</script></body></html>"""

if unsigned_bots:
    _u = "\n".join(f"<li>{esc(b)}</li>" for b in unsigned_bots)
    unsigned_html = (
        '<div style="background:#fff0f0;border:1px solid #c0392b;color:#c0392b;'
        'padding:12px 16px;margin:12px 0;border-radius:6px;">'
        '<h2 style="margin:0 0 6px;font-size:14px;">'
        'UNSIGNED PRE-REGISTRATION BOTS — DO NOT SWITCH ON</h2>'
        f'<ul style="margin:0;padding-left:18px;">{_u}</ul></div>'
    )
else:
    unsigned_html = ""

repl = {"__DATE__": date, "__TOT__": f"{tot:,.0f}", "__NLEGS__": str(len(trades)),
        "__NBOTS__": str(len(bots)), "__SCALP__": f"{champ_pnl:,.0f}",
        "__TOTC__": "neg" if tot < 0 else "pos",
        "__SCALPC__": "neg" if champ_pnl < 0 else "pos",
        "__ROWS__": rows_json, "__CUM__": json.dumps(cumlist),
        "__UNSIGNED__": unsigned_html,
        "__BACKLOG__": backlog_html}
html = TPL
for k, v in repl.items(): html = html.replace(k, v)
open(os.path.join(ROOT, "dashboard.html"), "w").write(html)

print(f"Wrote STATUS.md + dashboard.html | total ${tot:,.0f} | champion {champ}: {champ_trades} condors")
