#!/usr/bin/env python3
"""Build the canonical Bot Fleet WORKING ledger from the latest full OA export.

=============================================================================
 DATA CUTOVER — LEDGER_START  (build-plan.md §3, settled 2026-07-30)
=============================================================================
The working ledger is POST-CUTOVER ONLY. `LEDGER_START` is the Day-0
reactivation date. Every row in the export lands in exactly one of three
buckets, decided by its **open_date** and nothing else:

  post-cutover   open_date >= LEDGER_START            -> data/trades.csv
                                                          (the working ledger)
  straddler      open_date <  LEDGER_START            -> data/straddlers.csv
                 and (still open OR close >= START)      (mirror baseline layer)
  pre-cutover    open_date <  LEDGER_START            -> DISCARDED (counted,
                 and closed before it                     never written)

THE STRADDLE RULE — a position's era is its OPEN date. `LEDGER_START` filters
on `open_date`, NEVER `close_date`. A position belongs to the era in which the
decision to enter it was made; when it happens to resolve is an accident of its
structure. A close-date rule would let a position entered under a dead exit
engine, at a strike chosen by a config that no longer exists, land in the clean
post-cutover ledger and be read as evidence about the new fleet.

Straddlers NEVER enter the working ledger. They are written to a separate file
so they are visible rather than silently dropped; only `data/mirror_baseline.csv`
(a one-time frozen snapshot, built from the capture export, read ONLY by funding
decisions) may consume them.

REFUSAL IS THE DEFAULT. With no LEDGER_START resolved, this script exits
non-zero and writes nothing. There is no "just this once" pass-through mode.

Resolution order:  --ledger-start YYYY-MM-DD  >  $LEDGER_START  >  the constant
below. Set the constant on Day-0 (runbook §4 Step 1) and commit it.

-----------------------------------------------------------------------------
Idempotent: rebuilds data/trades.csv + data/bots.csv from scratch every run.
The OA website export is FULL trade history (not a delta), so re-importing the
newest daily file reconstructs the entire ledger. Drop a new export in data/raw/
named YYYY-MM-DD.csv and re-run; the newest file wins.

CLASSIFICATION COMES FROM data/bots_meta.csv, NOT from bot-name heuristics.
That file is the single source for pillar / role / underlying / on-off /
epoch-boundary / strike-fix / superseded / champion, keyed by exact OA bot name.
A rename = edit one row there; nothing keys on the name's shape. Any bot present
in the export but MISSING from bots_meta.csv is tagged UNCLASSIFIED and printed
as a warning, so renames and new bots are caught loudly instead of mis-filed.

Counting: OA models each spread as a separate "position", so a legged iron condor
shows as 2 rows (a call spread + a put spread) while a combined "ironcondor" shows
as 1 row. We track BOTH:
  - n_legs   = position rows (matches OA's "Positions" count)
  - n_trades = condors. We pair ONE call spread with ONE put spread opened in the
    same minute; a combined ironcondor row is already one trade; any leftover
    same-side spread is a single-sided trade.

Usage:
  python3 scripts/build_ledger.py
  python3 scripts/build_ledger.py --ledger-start 2026-08-15
  LEDGER_START=2026-08-15 python3 scripts/build_ledger.py
"""
import argparse, csv, glob, json, os, re, sys, collections

# ---------------------------------------------------------------------------
# SET THIS ON DAY-0. It is the reactivation date, format YYYY-MM-DD.
# Leave as the sentinel until then — the sentinel makes the script REFUSE to
# build a ledger, which is the safe state. See reactivation-runbook.md §4 Step 1.
LEDGER_START = "UNSET"
# ---------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
OUT = os.path.join(ROOT, "data")
META_PATH = os.path.join(OUT, "bots_meta.csv")

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def fl(x):
    try: return float(x)
    except (TypeError, ValueError): return 0.0


def resolve_ledger_start(cli_value):
    """CLI > env > module constant. Refuse anything that is not a real date."""
    for src, val in (("--ledger-start", cli_value),
                     ("$LEDGER_START", os.environ.get("LEDGER_START")),
                     ("the LEDGER_START constant in build_ledger.py", LEDGER_START)):
        if val:
            val = val.strip()
            if _DATE_RE.match(val):
                return val, src
            if val != "UNSET":
                sys.exit(f"ERROR: {src} = {val!r} is not a YYYY-MM-DD date.")
    sys.exit(
        "ERROR: LEDGER_START is not set — refusing to build a ledger.\n"
        "\n"
        "  The working ledger is post-cutover only (build-plan.md §3). Without a\n"
        "  cutover date every pre-cutover row would enter it, which is exactly the\n"
        "  contamination the cutover exists to prevent. Nothing was written.\n"
        "\n"
        "  Set it one of three ways:\n"
        "    python3 scripts/build_ledger.py --ledger-start YYYY-MM-DD\n"
        "    LEDGER_START=YYYY-MM-DD python3 scripts/build_ledger.py\n"
        "    edit the LEDGER_START constant at the top of this file  <- do this on Day-0\n"
    )


# Parse OA's `description` leg list into per-leg strikes. Each leg reads
# "<sign><strike> <side>" e.g. "-709 put", "+7,335 put", "-765 call".
# Sign convention is universal across structures: '-' = SHORT leg, '+' = LONG leg
# (holds for credit spreads, debit spreads, iron condors, iron butterflies).
# Returns {short_put, long_put, short_call, long_call} — blank when a leg is absent.
_LEG_RE = re.compile(r"([+-])\s*([\d,]+(?:\.\d+)?)\s*(put|call)", re.I)
def parse_strikes(desc):
    out = {"short_put": "", "long_put": "", "short_call": "", "long_call": ""}
    for sign, strike, side in _LEG_RE.findall(desc or ""):
        pos = "short" if sign == "-" else "long"
        out[f"{pos}_{side.lower()}"] = strike.replace(",", "")
    return out


def newest_raw():
    files = sorted(glob.glob(os.path.join(RAW, "*.csv")))
    return files[-1] if files else None


def load_meta():
    if not os.path.exists(META_PATH):
        sys.exit(f"ERROR: missing {META_PATH} (the bot classification source)")
    return {r["bot"]: r for r in csv.DictReader(open(META_PATH))}


TCOLS = ["bot", "pillar", "underlying", "role", "epoch", "trade_id", "symbol",
         "structure", "status", "quantity", "credit", "exit_price", "pnl", "risk",
         "open_date", "close_date", "expiration", "tags", "single_sided",
         "short_put", "long_put", "short_call", "long_call", "premium",
         "underlying_open", "underlying_close",
         "mfe_pct", "mae_pct", "mfe_date", "mae_date"]

BCOLS = ["bot", "pillar", "underlying", "role", "status", "n_trades", "n_legs",
         "total_pnl", "win_rate_trade", "win_rate_leg", "first_trade", "last_trade",
         "epoch_start", "needs_strike_fix", "superseded"]

SCOLS = ["bot", "structure", "status", "pnl", "risk", "open_date", "close_date",
         "symbol", "quantity", "note"]

STRADDLER_NOTE = ("PRE-CUTOVER OPEN — mirror baseline layer only; "
                  "NEVER a working-ledger or reporting input")


def write_receipt(path, **kw):
    """Machine-readable run receipt. Downstream scripts assert against this
    instead of re-deriving the cutover date."""
    kw.setdefault("contract",
                  "working ledger is POST-CUTOVER ONLY; the filter is on open_date")
    with open(path, "w") as fo:
        json.dump(kw, fo, indent=2)
        fo.write("\n")


def write_empty_ledger(ledger_start, ls_source, reason):
    """The n=0 state. Header-only files so every downstream script has a schema
    to read rather than a missing file to crash on."""
    os.makedirs(OUT, exist_ok=True)
    for path, cols in ((os.path.join(OUT, "trades.csv"), TCOLS),
                       (os.path.join(OUT, "bots.csv"), BCOLS),
                       (os.path.join(OUT, "straddlers.csv"), SCOLS)):
        with open(path, "w", newline="") as fo:
            csv.writer(fo).writerow(cols)
    write_receipt(os.path.join(OUT, "ledger_meta.json"),
                  ledger_start=ledger_start, ledger_start_source=ls_source,
                  source_export=None,
                  counts={"export_rows": 0, "post_cutover": 0,
                          "straddler": 0, "pre_cutover": 0},
                  n_trades_condors=0, n_bots=0, total_pnl=0.0, note=reason)
    print(f"LEDGER_START: {ledger_start}   (from {ls_source})")
    print(f"NOTE: {reason}")
    print("Wrote header-only data/trades.csv, data/bots.csv, data/straddlers.csv (n=0).")


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--ledger-start", default=None,
                    help="cutover date YYYY-MM-DD (overrides env and the constant)")
    args = ap.parse_args()

    ledger_start, ls_source = resolve_ledger_start(args.ledger_start)

    meta = load_meta()
    src = newest_raw()

    prior_path = os.path.join(OUT, "trades.csv")
    prior_rows = list(csv.DictReader(open(prior_path))) if os.path.exists(prior_path) else []
    prior_bots = {r["bot"] for r in prior_rows}

    if src is None:
        # Pre-Day-0, or every export archived. Writing an empty ledger is correct
        # ONLY if there is nothing to erase.
        if prior_rows:
            sys.exit(
                f"ERROR: no export found in {RAW}/ but data/trades.csv holds "
                f"{len(prior_rows)} rows.\n"
                "  Rebuilding would erase them. Restore an export to data/raw/ first."
            )
        write_empty_ledger(ledger_start, ls_source,
                           "no export in data/raw/ yet — pre-Day-0 empty ledger")
        return

    rows = list(csv.DictReader(open(src)))

    # --- FILTERED-EXPORT GUARD -------------------------------------------
    # OA's positions export respects the Analyze Bot Group filter, so an export
    # taken with any group deselected is a SUBSET — rebuilding from it would
    # silently erase the excluded bots' history. Compare against the PRIOR ledger
    # before we overwrite it (verified 2026-07-03).
    dropped = sorted(prior_bots - {r["botName"] for r in rows})

    # --- THE CUTOVER PARTITION -------------------------------------------
    # Decided by open_date and nothing else. See the module docstring.
    post, straddlers, pre = [], [], []
    for r in rows:
        opened = (r.get("openDate") or "")[:10]
        closed = (r.get("closeDate") or "")[:10]
        if not opened:
            sys.exit("ERROR: export row with no openDate — cannot assign it an era. "
                     f"Row: {dict(list(r.items())[:6])}")
        if opened >= ledger_start:
            post.append(r)
        elif (not closed) or closed >= ledger_start:
            straddlers.append(r)
        else:
            pre.append(r)

    counts = {"export_rows": len(rows), "post_cutover": len(post),
              "straddler": len(straddlers), "pre_cutover": len(pre)}

    # --- straddlers: visible, separate, never a working-ledger input ------
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "straddlers.csv"), "w", newline="") as fo:
        w = csv.writer(fo); w.writerow(SCOLS)
        for r in straddlers:
            w.writerow([r["botName"], r["type"], r["status"], r["pnl"], r["risk"],
                        r["openDate"], r["closeDate"], r["symbol"], r["quantity"],
                        STRADDLER_NOTE])

    rows = post  # from here on, "rows" means the post-cutover working set ONLY

    # --- classification helpers (all from meta; no name guessing) ----------
    def g(bot, field, default=""):
        r = meta.get(bot)
        return (r.get(field) or default) if r else default
    def pillar(bot):     return g(bot, "pillar", "UNCLASSIFIED")
    def underlying(bot): return g(bot, "underlying")
    def role(bot):       return g(bot, "role", "unclassified")
    def status_on(bot):  return g(bot, "status", "OFF").upper()
    def strikefix(bot):  return g(bot, "strike_fix")
    def superseded(bot): return g(bot, "superseded")
    def epoch(bot, open_date):
        b = g(bot, "epoch_boundary")
        if not b: return "baseline"
        return "post-fix" if open_date[:10] >= b else "pre-fix"

    unclassified = sorted({r["botName"] for r in rows if r["botName"] not in meta})

    # --- pair legs into condors --------------------------------------------
    # A legged IC opens its call spread and put spread a few SECONDS apart, but a
    # re-entry can cross a minute boundary (e.g. 6/8: call 11:33:03, put 11:34:03).
    # Keying on the exact open-minute split those into two single-sided trades and
    # under-counted condors. Instead, bucket by (bot, DAY) and pair call<->put
    # greedily by nearest open-time within PAIR_WINDOW_S. Greedy-nearest is safe:
    # a condor's own two legs (seconds apart) are always tighter than the gap to the
    # next re-entry (minutes apart), so they get matched first; a genuinely
    # single-sided open (one side filtered for sub-min credit) is left unpaired.
    PAIR_WINDOW_S = 180

    def secs(i):
        hms = rows[i]["openDate"][11:19]  # 'HH:MM:SS'
        try:
            h, m, s = (int(x) for x in hms.split(":"))
            return h * 3600 + m * 60 + s
        except (ValueError, AttributeError):
            return 0

    buckets = collections.defaultdict(lambda: {"call": [], "put": [], "ic": [], "other": []})
    for i, r in enumerate(rows):
        key = (r["botName"], r["openDate"][:10])  # bucket by day, not minute
        t = r["type"]
        if t == "ironcondor": buckets[key]["ic"].append(i)
        elif t == "shortcallspread": buckets[key]["call"].append(i)
        elif t == "shortputspread": buckets[key]["put"].append(i)
        else: buckets[key]["other"].append(i)

    trade_of = {}
    trade_size = collections.Counter()
    tid = 0
    for (bot, day), b in buckets.items():
        for i in b["ic"]:
            tid += 1; k = f"T{tid:05d}"; trade_of[i] = k; trade_size[k] = 1
        cand = sorted((abs(secs(ci) - secs(pi)), ci, pi)
                      for ci in b["call"] for pi in b["put"]
                      if abs(secs(ci) - secs(pi)) <= PAIR_WINDOW_S)
        used = set()
        for _, ci, pi in cand:
            if ci in used or pi in used: continue
            used.add(ci); used.add(pi)
            tid += 1; k = f"T{tid:05d}"
            trade_of[ci] = k; trade_of[pi] = k; trade_size[k] = 2
        leftovers = [i for i in b["call"] if i not in used] + \
                    [i for i in b["put"] if i not in used] + b["other"]
        for i in leftovers:
            tid += 1; k = f"T{tid:05d}"; trade_of[i] = k; trade_size[k] = 1

    def single_sided(i):
        r = rows[i]
        return trade_size[trade_of[i]] == 1 and r["type"] in ("shortcallspread", "shortputspread")

    # --- trades.csv (THE WORKING LEDGER — post-cutover only) --------------
    out_rows = []
    for i, r in enumerate(rows):
        bot = r["botName"]
        k = parse_strikes(r.get("description", ""))
        out_rows.append([bot, pillar(bot), underlying(bot), role(bot),
                         epoch(bot, r["openDate"]), trade_of[i], r["symbol"],
                         r["type"], r["status"], r["quantity"], r["openPrice"],
                         r["closePrice"], r["pnl"], r["risk"], r["openDate"],
                         r["closeDate"], r["expiration"], r["tags"], single_sided(i),
                         k["short_put"], k["long_put"], k["short_call"], k["long_call"],
                         r.get("premium", ""), r.get("underlyingOpen", ""),
                         r.get("underlyingClose", ""), r.get("highReturnPct", ""),
                         r.get("lowReturnPct", ""), r.get("highReturnPctDate", ""),
                         r.get("lowReturnPctDate", "")])

    # --- THE REFUSAL ASSERTION -------------------------------------------
    # Belt and braces. If a pre-cutover row ever reaches this point the run dies
    # rather than writing a contaminated ledger. This is the guarantee every
    # reporting surface downstream is allowed to rely on.
    od = TCOLS.index("open_date")
    leaked = [r for r in out_rows if str(r[od])[:10] < ledger_start]
    if leaked:
        sys.exit(f"FATAL: {len(leaked)} pre-cutover row(s) reached the working "
                 f"ledger writer (LEDGER_START={ledger_start}). Nothing written. "
                 f"First: {leaked[0][:6]}")

    with open(os.path.join(OUT, "trades.csv"), "w", newline="") as fo:
        w = csv.writer(fo); w.writerow(TCOLS); w.writerows(out_rows)

    # --- per-bot aggregation (legs AND trades) ---------------------------
    legs = collections.defaultdict(lambda: {"n": 0, "pnl": 0.0, "wins": 0,
                                            "first": "9999", "last": "0000"})
    for r in rows:
        a = legs[r["botName"]]
        a["n"] += 1; a["pnl"] += fl(r["pnl"])
        if fl(r["pnl"]) > 0: a["wins"] += 1
        d = r["openDate"][:10]
        a["first"] = min(a["first"], d); a["last"] = max(a["last"], d)

    trade_pnl = collections.defaultdict(float)
    trade_bot = {}
    for i, r in enumerate(rows):
        k = trade_of[i]; trade_pnl[k] += fl(r["pnl"]); trade_bot[k] = r["botName"]
    tr = collections.defaultdict(lambda: {"n": 0, "wins": 0})
    for k, bot in trade_bot.items():
        tr[bot]["n"] += 1
        if trade_pnl[k] > 0: tr[bot]["wins"] += 1

    with open(os.path.join(OUT, "bots.csv"), "w", newline="") as fo:
        w = csv.writer(fo); w.writerow(BCOLS)
        for b, a in sorted(legs.items(), key=lambda x: x[1]["pnl"]):
            t = tr[b]
            w.writerow([b, pillar(b), underlying(b), role(b), status_on(b),
                        t["n"], a["n"], round(a["pnl"]),
                        f'{t["wins"] / t["n"] * 100:.0f}%' if t["n"] else "-",
                        f'{a["wins"] / a["n"] * 100:.0f}%' if a["n"] else "-",
                        a["first"], a["last"], g(b, "epoch_boundary"),
                        strikefix(b), superseded(b)])

    tot = sum(a["pnl"] for a in legs.values())
    ntr = len(trade_bot)

    write_receipt(os.path.join(OUT, "ledger_meta.json"),
                  ledger_start=ledger_start, ledger_start_source=ls_source,
                  source_export=os.path.basename(src), counts=counts,
                  n_trades_condors=ntr, n_bots=len(legs),
                  total_pnl=round(tot, 2), note="")

    print(f"LEDGER_START: {ledger_start}   (from {ls_source})")
    print(f"Source: {os.path.basename(src)}")
    print(f"Export rows: {counts['export_rows']}  ->  post-cutover {counts['post_cutover']}"
          f" | straddlers {counts['straddler']} | pre-cutover discarded {counts['pre_cutover']}")
    print(f"WORKING LEDGER  Legs: {len(rows)}  Trades(condors): {ntr}  "
          f"Bots: {len(legs)}  Total P/L: {tot:,.0f}")
    if not rows:
        print("NOTE: working ledger is EMPTY (n=0). Expected before the first "
              "post-cutover trading day.")
    if straddlers:
        sb = collections.Counter(r["botName"] for r in straddlers)
        print(f"\nSTRADDLERS -> data/straddlers.csv ({len(straddlers)} rows, "
              f"{len(sb)} bot(s)) — mirror baseline layer ONLY, never reporting:")
        for b, n in sb.most_common():
            print(f"    {n:>4}  {b}")
    if unclassified:
        print(f"\nWARNING: {len(unclassified)} unclassified bot(s) — add to data/bots_meta.csv:")
        for b in unclassified: print(f"  - {b}")
    if dropped:
        print("\n" + "!" * 68)
        print(f"!! FILTERED-EXPORT WARNING: {len(dropped)} bot(s) in the prior ledger are")
        print("!! MISSING from this export. If you exported with a Bot Group filter,")
        print("!! re-export with ALL groups selected — otherwise their history is LOST:")
        for b in dropped: print(f"!!   - {b}")
        print("!" * 68)


if __name__ == "__main__":
    main()
