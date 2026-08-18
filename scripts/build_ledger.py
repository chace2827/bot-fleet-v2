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

=============================================================================
 SECOND EXCLUSION AXIS — LAB OPS-CLASS  (E-3 / exploratory-bots-design-2026-08-07
 §3.3, RULED 2026-08-07; HARD PRECONDITION on any Lab bot's AUTOMATIONS toggle)
=============================================================================
The cutover is a TIME axis. This is a CLASS axis, and it is independent: a row
can be post-cutover and still barred from the working ledger because the bot
that opened it is an ops-class (Lab) probe substrate. Ops bots exist to be
mutated at will; their numbers are activity, never evidence. Guardrail G1
(pre-registration-ledger.md) forbids an ops number entering any Exp(R), any arm
or variant comparison, any funding decision or any tiered claim — and G2 says
that interdict is "enforced in code, not by intent".

  ops-class      bots_meta.ops_class == "lab-ops"   -> data/ops_rows.csv
                                                       (visible, never a ledger
                                                        or reporting input)

CLASSIFICATION COMES FROM data/bots_meta.csv's `ops_class` COLUMN. NOT from the
export's `tags` string (OA normalises tags — lossy, and `tags` is pass-through
here), and NOT from the bot name. Same principle as pillar/role/underlying.

THE GROUP/TAG FENCE (the third exclusion surface). Group reconciles to the
`pillar` column exactly (oa-ops-runbook.md §3), and §3.5 puts every ops bot in
group `Lab` with tag `ops` as the cohort handle. This script therefore REFUSES,
loudly and without writing, when the three surfaces disagree:
  - an unknown `ops_class` value                       -> FATAL
  - ops_class=lab-ops but pillar != Lab                -> FATAL
  - pillar == Lab but ops_class not declared           -> FATAL
  - an export row TAGGED `ops` whose bot is undeclared -> FATAL
The tag is never a classifier here; it is only ever a tripwire that catches a
Lab bot somebody forgot to declare. A bot that reached OA's `Lab` group without
reaching this file is exactly the leak E-3 exists to prevent.

⛔ BUILD-ORDER CONSTRAINT (§3.3 item 5). This exclusion must ship BEFORE the
first ops bot trades. Ops rows that once reached data/trades.csv cannot be
removed later without tripping the FILTERED-EXPORT GUARD and requiring surgery
on the ledger. The daily export must still INCLUDE the ops bots — group-based
EXPORT exclusion is the wrong mechanism and produces exactly the subset the
guard exists to catch. The ledger excludes them POST-INGEST.

REFUSAL IS THE DEFAULT. With no LEDGER_START resolved, this script exits
non-zero and writes nothing. There is no "just this once" pass-through mode.

Resolution order:  --ledger-start YYYY-MM-DD  >  $LEDGER_START  >  the constant
below. Set the constant on Day-0 (runbook §4 Step 1) and commit it.

-----------------------------------------------------------------------------
Idempotent: rebuilds data/trades.csv + data/bots.csv from scratch every run.
The OA website export is FULL trade history (not a delta), so re-importing the
newest daily file reconstructs the entire ledger. Drop a new export in data/raw/
named YYYY-MM-DD.csv and re-run; the newest file wins.

-----------------------------------------------------------------------------
 THE MONOTONICITY GUARD  (G-2, ledger-truncation-forensics-2026-08-17.md §7)
-----------------------------------------------------------------------------
Because that rebuild is FULL and destructive, aiming it at a STALE or PINNED
export DELETES every trading day newer than that export. On 2026-08-12 a CI
determinism run pinned to the 2026-08-10 fixture did exactly that: five legs
across 2026-08-11 vanished from data/trades.csv, the truncated file was
committed in 0051b5e6, and it was the state of the fleet's numbers on master
for five days before anyone noticed.

None of the three pre-existing guards covers that axis. The FILTERED-EXPORT
GUARD protects against a *bot* vanishing; the refusal assertion protects
against *pre-cutover* rows reaching the writer; the "would erase them" check
only fires when data/raw/ is empty. The axis that actually moved — the ledger's
maximum open_date going BACKWARDS — was unguarded.

So: this script REFUSES, and writes nothing, when the maximum `open_date` of
the working ledger it is about to write is EARLIER than the maximum `open_date`
of the data/trades.csv already on disk. Rewinding is a legitimate operation but
it is never an accident — ask for it with `--allow-rewind`, and the rewind is
printed as a banner so it lands in the run log.

-----------------------------------------------------------------------------
 FIXTURE / LIVE SEPARATION — --root  (G-3, same forensics doc §7)
-----------------------------------------------------------------------------
G-2 stops a backwards rebuild. G-3 removes the reason one was ever aimed at the
live ledger: there was no way to run this script WITHOUT writing data/. The
command used to prove CI determinism — `scripts/daily.sh 2026-08-10` — wrote to
exactly the same data/trades.csv that carries the fleet's real numbers.
TAPE_FIXTURE=1 isolated the tape stage from the network; nothing isolated the
ledger stage from the ledger.

`--root DIR` (or $FLEET_ROOT) points RAW, OUT and META_PATH at DIR/data instead
of the repo's. A determinism run against a scratch root cannot touch the live
ledger no matter which export it is pinned to. `scripts/daily.sh` honours
$FLEET_ROOT for the whole nine-stage pipeline, and `scripts/ci/seed_scratch_root.sh`
materialises such a root. This removes the incident class, not just the instance.

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
  python3 scripts/build_ledger.py 2026-08-10 --allow-rewind   # deliberate rewind
  python3 scripts/build_ledger.py --root /tmp/scratch 2026-08-10   # never touches data/
  FLEET_ROOT=/tmp/scratch python3 scripts/build_ledger.py
  python3 scripts/build_ledger.py --selftest      # exclusion + rewind-guard tests
"""
import argparse, csv, glob, json, os, re, sys, collections

# ---------------------------------------------------------------------------
# SET THIS ON DAY-0. It is the reactivation date, format YYYY-MM-DD.
# Leave as the sentinel until then — the sentinel makes the script REFUSE to
# build a ledger, which is the safe state. See reactivation-runbook.md §4 Step 1.
LEDGER_START = "2026-08-10"
# ---------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
OUT = os.path.join(ROOT, "data")
META_PATH = os.path.join(OUT, "bots_meta.csv")


def set_root(root):
    """Repoint every path this script reads or writes at `root` (G-3).

    The default root is the repo, so `data/` means the LIVE ledger. A fixture or
    determinism run must never resolve to that — see the G-3 block in the module
    docstring. Resolution order is --root > $FLEET_ROOT > the repo.

    This is also what the selftest uses, so the flag CI depends on is exercised
    by every selftest case rather than sitting on an untested path.
    """
    global ROOT, RAW, OUT, META_PATH
    ROOT = os.path.abspath(root)
    RAW = os.path.join(ROOT, "data", "raw")
    OUT = os.path.join(ROOT, "data")
    META_PATH = os.path.join(OUT, "bots_meta.csv")
    return ROOT

# --- E-3 §3.3 — the ops-class (Lab) exclusion axis -------------------------
OPS_CLASS_COL   = "ops_class"      # the declaring column in data/bots_meta.csv
OPS_CLASS_VALUE = "lab-ops"        # the ONLY non-empty value this column accepts
OPS_PILLAR      = "Lab"            # §3.5 — group == pillar, single-select
OPS_TAG         = "ops"            # §3.5 — the cohort handle (tripwire only)

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


def _tid_int(s):
    try:
        return int(s[1:]) if s and s[0] == "T" else 0
    except (ValueError, TypeError):
        return 0


def max_existing_tid(day, out_dir=None):
    """Largest trade_id already assigned to a day other than `day`.

    build_ledger.py overwrites data/trades.csv, so the counter must continue from
    the persisted hedge_tournament.csv (and any trades.csv rows from other days)
    rather than resetting.  Re-running the same day ignores that day's own rows
    so trade_ids are deterministic.

    G-3: reads from OUT, not from the repo. Bound to the module-level ROOT as a
    default argument this resolved at import time, so a --root or selftest run
    read the LIVE hedge_tournament.csv and trades.csv to seed the counter — a
    fixture run reaching into live data is exactly the class of leak G-3 closes.
    """
    m = 0
    base = out_dir or OUT
    for name, date_key in (("hedge_tournament.csv", "date"),
                           ("trades.csv", "open_date")):
        path = os.path.join(base, name)
        if not os.path.exists(path):
            continue
        with open(path) as f:
            for r in csv.DictReader(f):
                d = (r.get(date_key) or "")[:10]
                if d == day:
                    continue
                t = _tid_int(r.get("trade_id", ""))
                if t > m:
                    m = t
    return m


def max_open_date(rows, key):
    """Largest YYYY-MM-DD open date across `rows`, or "" when there are none.

    `key` differs by side of the comparison: export rows carry `openDate`, ledger
    rows carry `open_date`. Blank/absent dates are ignored rather than sorting to
    the front, so a malformed row cannot fake a rewind.
    """
    days = [d for d in ((r.get(key) or "")[:10] for r in rows) if d]
    return max(days) if days else ""


def rewind_refusal(prior_max, new_max, prior_legs, new_legs, src, ledger_start):
    """The G-2 refusal text. Names BOTH dates, the export that caused it, and the
    one flag that overrides it. Returned (not raised) so the selftest can read it."""
    bar = "!" * 72
    return (
        "\n" + bar + "\n"
        "REFUSED: this rebuild would walk the working ledger BACKWARDS in time.\n"
        "\n"
        f"  prior data/trades.csv  max open_date : {prior_max}"
        f"   ({prior_legs} leg(s))\n"
        f"  this rebuild would write max open_date: "
        f"{new_max or '(none — the ledger would be emptied)'}   ({new_legs} leg(s))\n"
        f"  source export                        : {os.path.basename(src)}\n"
        f"  LEDGER_START                         : {ledger_start}\n"
        "\n"
        "  build_ledger.py is a FULL rebuild from ONE export: it truncates\n"
        "  data/trades.csv and rewrites it from the source named above. Every\n"
        f"  trading day after {new_max or 'the cutover'} would therefore be DELETED from the\n"
        "  working ledger — and from every reporting surface derived from it.\n"
        "\n"
        "  This is the exact shape of the 2026-08-12 truncation (commit 0051b5e6):\n"
        "  a run pinned to a stale fixture erased 2026-08-11 and the loss was\n"
        "  committed to master. See docs/ledger-truncation-forensics-2026-08-17.md.\n"
        "\n"
        "  NOTHING WAS WRITTEN.\n"
        "\n"
        "  To rebuild from the NEWEST export, drop the pinned date argument:\n"
        "      python3 scripts/build_ledger.py\n"
        "  To prove determinism without touching the live ledger, use a scratch\n"
        "  root rather than a pinned rebuild of data/ (G-3).\n"
        "  If you genuinely intend to rewind the ledger, say so explicitly:\n"
        f"      python3 scripts/build_ledger.py {os.path.basename(src)[:10]} --allow-rewind\n"
        + bar
    )


def load_meta():
    if not os.path.exists(META_PATH):
        sys.exit(f"ERROR: missing {META_PATH} (the bot classification source)")
    rd = csv.DictReader(open(META_PATH))
    rows = list(rd)
    if OPS_CLASS_COL not in (rd.fieldnames or []):
        sys.exit(
            f"FATAL: {META_PATH} has no `{OPS_CLASS_COL}` column.\n"
            "\n"
            "  The Lab ops-class exclusion (E-3, exploratory-bots-design-2026-08-07\n"
            "  §3.3) is a HARD PRECONDITION and it declares the ops set in that\n"
            "  column. Without it every ops row would enter the working ledger\n"
            "  silently, which is the contamination the exclusion exists to prevent.\n"
            f"  Add a `{OPS_CLASS_COL}` column (empty | {OPS_CLASS_VALUE!r}). Nothing was written."
        )
    return {r["bot"]: r for r in rows}


def _tag_tokens(s):
    """OA normalises tags to lowercase and non-alphanumeric to space. Tokenize the
    same way so `ops`, `Ops`, `lab,ops` and `lab ops` all read alike."""
    return {t for t in re.split(r"[^a-z0-9]+", (s or "").lower()) if t}


def ops_set_from_meta(meta):
    """The declared ops set, PLUS the group/tag fence (E-3 §3.3, surface 3).

    Classification is the `ops_class` column and nothing else. The fence only
    ever REFUSES on disagreement between the declaring column and the pillar
    (== OA Bot Group) it must reconcile to; it never promotes a bot into the
    ops set on the strength of a pillar or a tag."""
    ops, bad_value, bad_pillar, undeclared = set(), [], [], []
    for bot, r in sorted(meta.items()):
        v = (r.get(OPS_CLASS_COL) or "").strip().lower()
        pil = (r.get("pillar") or "").strip()
        if v == OPS_CLASS_VALUE:
            ops.add(bot)
            if pil != OPS_PILLAR:
                bad_pillar.append(f"{bot}: {OPS_CLASS_COL}={v!r} but pillar={pil!r}")
        elif v:
            bad_value.append(f"{bot}: {OPS_CLASS_COL}={v!r}")
        elif pil == OPS_PILLAR:
            undeclared.append(f"{bot}: pillar={OPS_PILLAR!r} but {OPS_CLASS_COL} is empty")

    if bad_value:
        sys.exit(
            f"FATAL: unrecognised `{OPS_CLASS_COL}` value(s) in {META_PATH}. Nothing written.\n"
            f"  Allowed: empty, or {OPS_CLASS_VALUE!r} (E-3 §3.3 item 1).\n"
            + "".join(f"    - {b}\n" for b in bad_value)
            + "  A value this script does not recognise is NOT treated as 'not ops' —\n"
              "  guessing which side of the exclusion a bot falls on is the failure."
        )
    if bad_pillar:
        sys.exit(
            f"FATAL: ops-class bot(s) not in pillar {OPS_PILLAR!r}. Nothing written.\n"
            "  §3.5: every ops bot sits in Bot Group `Lab`, and oa-ops-runbook.md §3\n"
            "  requires groups to reconcile to the `pillar` column EXACTLY.\n"
            + "".join(f"    - {b}\n" for b in bad_pillar)
        )
    if undeclared:
        sys.exit(
            f"FATAL: pillar-{OPS_PILLAR} bot(s) with no `{OPS_CLASS_COL}` declaration. "
            "Nothing written.\n"
            "  A Lab bot that is not declared ops-class would enter the WORKING LEDGER\n"
            "  (E-3 §3.3 / guardrail G1). Declare it, or move it out of the Lab pillar.\n"
            + "".join(f"    - {b}\n" for b in undeclared)
        )
    return ops


def fence_export_tags(rows, ops_bots):
    """Tripwire, not a classifier: an export row tagged `ops` whose bot is not
    declared in bots_meta.ops_class means a Lab bot reached OA without reaching
    the exclusion. Refuse rather than write a ledger that may already be dirty."""
    offenders = sorted({r.get("botName", "") for r in rows
                        if OPS_TAG in _tag_tokens(r.get("tags"))
                        and r.get("botName") not in ops_bots})
    if offenders:
        sys.exit(
            f"FATAL: export row(s) tagged {OPS_TAG!r} from bot(s) with no "
            f"`{OPS_CLASS_COL}` declaration. Nothing written.\n"
            "  §3.5 uses the `ops` tag as the ops cohort handle. A bot carrying it that\n"
            "  is undeclared here would be written straight into the working ledger.\n"
            + "".join(f"    - {b}\n" for b in offenders)
            + f"  Fix: add `{OPS_CLASS_COL}={OPS_CLASS_VALUE}` (pillar {OPS_PILLAR}) to "
              "data/bots_meta.csv,\n"
              "  or remove the tag in OA if the bot is genuinely not ops-class.\n"
              "  (The tag never CLASSIFIES a bot here — it only catches this disagreement.)"
        )


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

# Ops rows keep the FULL ledger schema (not the straddler shape) so the FROZEN
# execution_audit.py can be pointed at this file as an explicitly-invoked
# fixture — the mechanism it already uses for data/archive/trades.csv
# (§3.3 item 8) — plus a `note` column mirroring STRADDLER_NOTE's visibility.
# ⚠️ `trade_id` is BLANK by construction: the partition happens BEFORE the condor
# pairing block (§3.3 item 2), because pairing assigns trade_id from a global
# counter and excluding afterwards would corrupt the numbering. Whether ops rows
# should get their own trade_id namespace is NOT ruled — see the hand-off.
OPSCOLS = TCOLS + ["note"]

OPS_NOTE = ("LAB OPS-CLASS — excluded from the working ledger by declaration "
            "(bots_meta.csv ops_class=lab-ops, E-3 §3.3); NEVER a reporting, "
            "ranking, comparison or funding input (guardrail G1)")


def write_receipt(path, **kw):
    """Machine-readable run receipt. Downstream scripts assert against this
    instead of re-deriving the cutover date."""
    kw.setdefault("contract",
                  "working ledger is POST-CUTOVER ONLY; the filter is on open_date. "
                  "AND LAB-OPS-EXCLUDED; the filter is bots_meta.csv "
                  "ops_class == 'lab-ops' (E-3 §3.3). Two independent axes: "
                  "time and class.")
    with open(path, "w") as fo:
        json.dump(kw, fo, indent=2)
        fo.write("\n")


def assert_no_ops_leak(out_rows, ops_bots):
    """§3.3 item 3 — the CLASS-axis refusal assertion, mirroring the pre-cutover
    one. If a single ops row reaches the working-ledger writer the run dies and
    nothing is written. This is the guarantee guardrail G1 is allowed to rely on."""
    bc = TCOLS.index("bot")
    leaked = [r for r in out_rows if r[bc] in ops_bots]
    if leaked:
        names = sorted({r[bc] for r in leaked})
        sys.exit(f"FATAL: {len(leaked)} LAB OPS-CLASS row(s) reached the working "
                 f"ledger writer. Nothing written. Bot(s): {names}. "
                 f"First: {leaked[0][:6]}")


def write_empty_ledger(ledger_start, ls_source, reason):
    """The n=0 state. Header-only files so every downstream script has a schema
    to read rather than a missing file to crash on."""
    os.makedirs(OUT, exist_ok=True)
    for path, cols in ((os.path.join(OUT, "trades.csv"), TCOLS),
                       (os.path.join(OUT, "bots.csv"), BCOLS),
                       (os.path.join(OUT, "straddlers.csv"), SCOLS),
                       (os.path.join(OUT, "ops_rows.csv"), OPSCOLS)):
        with open(path, "w", newline="") as fo:
            csv.writer(fo).writerow(cols)
    write_receipt(os.path.join(OUT, "ledger_meta.json"),
                  ledger_start=ledger_start, ledger_start_source=ls_source,
                  source_export=None,
                  counts={"export_rows": 0, "post_cutover": 0,
                          "straddler": 0, "pre_cutover": 0, "ops_rows": 0},
                  n_trades_condors=0, n_bots=0, total_pnl=0.0,
                  ops_bots=[], ops_rows=0, note=reason)
    print(f"LEDGER_START: {ledger_start}   (from {ls_source})")
    print(f"NOTE: {reason}")
    print("Wrote header-only data/trades.csv, data/bots.csv, data/straddlers.csv, "
          "data/ops_rows.csv (n=0).")


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("date", nargs="?", default=None,
                    help="use data/raw/DATE.csv as the export source; otherwise newest")
    ap.add_argument("--ledger-start", default=None,
                    help="cutover date YYYY-MM-DD (overrides env and the constant)")
    ap.add_argument("--selftest", action="store_true",
                    help="run the E-3 §3.3 ops-class exclusion tests and exit")
    ap.add_argument("--allow-rewind", action="store_true",
                    help="permit a rebuild whose max open_date is EARLIER than the "
                         "prior data/trades.csv's (G-2). Never implicit.")
    ap.add_argument("--root", default=None,
                    help="read and write DIR/data instead of the repo's, so a "
                         "fixture run cannot touch the live ledger (G-3). "
                         "Defaults to $FLEET_ROOT, then the repo.")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    # G-3 — before anything resolves a path. --root > $FLEET_ROOT > the repo.
    root_arg = args.root or os.environ.get("FLEET_ROOT")
    if root_arg:
        repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        resolved = set_root(root_arg)
        if resolved != repo:
            print(f"SCRATCH ROOT: {resolved}   "
                  f"(from {'--root' if args.root else '$FLEET_ROOT'}) — "
                  "the live ledger in the repo is NOT being written")

    ledger_start, ls_source = resolve_ledger_start(args.ledger_start)

    meta = load_meta()
    # E-3 §3.3 — resolve the declared ops set (and run the group/pillar fence)
    # BEFORE anything reads the export, so the FILTERED-EXPORT GUARD below can
    # subtract it and so a mis-declared roster refuses without touching disk.
    ops_bots = ops_set_from_meta(meta)
    if args.date:
        src = os.path.join(RAW, f"{args.date}.csv")
        if not os.path.exists(src):
            sys.exit(f"ERROR: raw export fixture not found: {src}")
        day = args.date
    else:
        src = newest_raw()
        day = os.path.basename(src)[:10] if src else ""

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
    # §3.3 item 5: subtract the ops set defensively — an ops bot is ABSENT from
    # the working ledger by design, so its absence is never evidence of a
    # filtered export and must not shout as if it were.
    dropped = sorted(prior_bots - {r["botName"] for r in rows} - ops_bots)

    # §3.3 surface 3 — the tag tripwire, before any partitioning.
    fence_export_tags(rows, ops_bots)

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

    # --- THE MONOTONICITY GUARD (G-2) ------------------------------------
    # Runs BEFORE the first byte is written — ahead of straddlers.csv, ops_rows.csv
    # and trades.csv — so a refusal here leaves the whole ledger untouched.
    # The comparison is against the WORKING ledger, so the ops set is subtracted
    # on the new side exactly as it will be by the partition below; ops rows are
    # absent from data/trades.csv by design and must not count as forward motion.
    new_working = [r for r in post if r["botName"] not in ops_bots]
    new_max   = max_open_date(new_working, "openDate")
    prior_max = max_open_date(prior_rows, "open_date")
    if prior_max and new_max < prior_max:
        if not args.allow_rewind:
            sys.exit(rewind_refusal(prior_max, new_max, len(prior_rows),
                                    len(new_working), src, ledger_start))
        print("\n" + "!" * 72)
        print("!! LEDGER REWIND — explicitly authorised with --allow-rewind.")
        print(f"!!   max open_date  {prior_max}  ->  {new_max or '(empty ledger)'}")
        print(f"!!   legs           {len(prior_rows)}  ->  {len(new_working)}")
        print(f"!!   source export  {os.path.basename(src)}")
        print("!! Every trading day after "
              f"{new_max or 'the cutover'} is being removed from data/trades.csv.")
        print("!" * 72)

    # --- straddlers: visible, separate, never a working-ledger input ------
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "straddlers.csv"), "w", newline="") as fo:
        w = csv.writer(fo); w.writerow(SCOLS)
        for r in straddlers:
            w.writerow([r["botName"], r["type"], r["status"], r["pnl"], r["risk"],
                        r["openDate"], r["closeDate"], r["symbol"], r["quantity"],
                        STRADDLER_NOTE])

    rows = post  # from here on, "rows" means the post-cutover working set ONLY

    # --- THE OPS-CLASS PARTITION (E-3 §3.3 item 2) ------------------------
    # Immediately after the cutover partition and BEFORE the condor pairing
    # block: pairing assigns trade_id from a global counter, so excluding
    # afterwards would corrupt the numbering.
    # `post_cutover` keeps its own meaning (the TIME axis alone); `ops_rows` is
    # the second axis, counted separately. Working-ledger legs = post_cutover
    # minus ops_rows.
    ops_src = [r for r in rows if r["botName"] in ops_bots]
    rows    = [r for r in rows if r["botName"] not in ops_bots]
    counts["ops_rows"] = len(ops_src)

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
    if unclassified:
        print("\nERROR: UNCLASSIFIED bot(s) in the post-cutover working set:")
        for b in unclassified:
            print(f"  - {b}")
        print("Refusing to write the working ledger. Add them to data/bots_meta.csv first.")
        sys.exit(1)

    # --- ops rows: visible, separate, never a working-ledger input --------
    with open(os.path.join(OUT, "ops_rows.csv"), "w", newline="") as fo:
        w = csv.writer(fo); w.writerow(OPSCOLS)
        for r in ops_src:
            k = parse_strikes(r.get("description", ""))
            bot = r["botName"]
            w.writerow([bot, pillar(bot), underlying(bot), role(bot),
                        epoch(bot, r["openDate"]), "", r["symbol"],
                        r["type"], r["status"], r["quantity"], r["openPrice"],
                        r["closePrice"], r["pnl"], r["risk"], r["openDate"],
                        r["closeDate"], r["expiration"], r["tags"], "",
                        k["short_put"], k["long_put"], k["short_call"], k["long_call"],
                        r.get("premium", ""), r.get("underlyingOpen", ""),
                        r.get("underlyingClose", ""), r.get("highReturnPct", ""),
                        r.get("lowReturnPct", ""), r.get("highReturnPctDate", ""),
                        r.get("lowReturnPctDate", ""), OPS_NOTE])

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
    tid = max_existing_tid(day)
    for (bot, bday), b in buckets.items():
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

    # The same guarantee on the CLASS axis (E-3 §3.3 item 3). Guardrail G2:
    # G1 is enforced in code, not by intent.
    assert_no_ops_leak(out_rows, ops_bots)

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
    trade_ss = set()
    for i, r in enumerate(rows):
        k = trade_of[i]; trade_pnl[k] += fl(r["pnl"]); trade_bot[k] = r["botName"]
        if single_sided(i):
            trade_ss.add(k)
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
    # A condor is two spread rows paired by trade_id with single_sided=False.
    n_cond = sum(1 for k in trade_size
                 if trade_size[k] == 2 and k not in trade_ss)
    n_one_sided = ntr - n_cond
    condor_word = "condor" if n_cond == 1 else "condors"

    write_receipt(os.path.join(OUT, "ledger_meta.json"),
                  ledger_start=ledger_start, ledger_start_source=ls_source,
                  source_export=os.path.basename(src), counts=counts,
                  n_trades_condors=ntr, n_bots=len(legs),
                  total_pnl=round(tot, 2),
                  ops_bots=sorted(ops_bots), ops_rows=counts["ops_rows"], note="")

    print(f"LEDGER_START: {ledger_start}   (from {ls_source})")
    print(f"Source: {os.path.basename(src)}")
    print(f"Export rows: {counts['export_rows']}  ->  post-cutover {counts['post_cutover']}"
          f" | straddlers {counts['straddler']} | pre-cutover discarded {counts['pre_cutover']}")
    print(f"WORKING LEDGER  Legs: {len(rows)}  Positions: {ntr} "
          f"({n_cond} {condor_word}, {n_one_sided} single-sided)  "
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
    if ops_bots:
        # §3.3 item 7 — never silent. Printed whenever the class is DECLARED,
        # even at zero rows, so an ops bot cannot vanish without a line.
        ob = collections.Counter(r["botName"] for r in ops_src)
        print(f"\nLAB OPS-CLASS -> data/ops_rows.csv ({counts['ops_rows']} rows, "
              f"{len(ops_bots)} declared bot(s)) — EXCLUDED from the working ledger "
              f"by declaration (E-3 §3.3);\n    never a reporting, ranking, comparison "
              f"or funding input (guardrail G1):")
        for b in sorted(ops_bots):
            n = ob.get(b, 0)
            print(f"    {n:>4}  {b}" + ("" if n else "   (declared; no rows in this export)"))
    if dropped:
        print("\n" + "!" * 68)
        print(f"!! FILTERED-EXPORT WARNING: {len(dropped)} bot(s) in the prior ledger are")
        print("!! MISSING from this export. If you exported with a Bot Group filter,")
        print("!! re-export with ALL groups selected — otherwise their history is LOST:")
        for b in dropped: print(f"!!   - {b}")
        print("!" * 68)


# ===========================================================================
# SELF-TEST — E-3 §3.3 ops-class exclusion (house style: fixtures + a named
# check matrix, asserted against ground truth, run with --selftest)
# ===========================================================================
def _st_env(tmp, meta_rows, export_rows, meta_header=None, exports=None,
            keep_prior=False):
    """Build a throwaway ROOT/data tree and point the module globals at it.

    `export_rows` is written as data/raw/2099-01-02.csv. `exports` is an optional
    {YYYY-MM-DD: rows} of ADDITIONAL exports, for tests that need more than one
    file to choose between. RAW is cleared first so exports never leak across
    cases within a shared tmp dir.

    trades.csv is reset to header-only unless `keep_prior` — otherwise one case's
    ledger is the next case's PRIOR ledger, and the G-2 monotonicity guard reads
    a rewind that the case never meant to set up. N14 is the one case that does
    want the previous run's ledger, and says so.

    G-3: the throwaway tree is a real scratch ROOT (tmp/data/...) driven through
    set_root(), and every case runs with `--root tmp`. The selftest used to patch
    the module globals into a flat, bespoke shape that no production run ever
    took — so the isolation CI now depends on had no test behind it.
    """
    set_root(tmp)
    os.makedirs(RAW, exist_ok=True)
    for stale in glob.glob(os.path.join(RAW, "*.csv")):
        os.remove(stale)
    if not keep_prior:
        with open(os.path.join(OUT, "trades.csv"), "w", newline="") as fo:
            csv.writer(fo).writerow(TCOLS)
    hdr = meta_header or ["bot", "pillar", "role", "underlying", "status",
                          "epoch_boundary", "strike_fix", "superseded", OPS_CLASS_COL]
    with open(META_PATH, "w", newline="") as fo:
        w = csv.writer(fo); w.writerow(hdr)
        for r in meta_rows:
            w.writerow([r.get(c, "") for c in hdr])
    ecols = ["botName", "type", "description", "symbol", "status", "quantity",
             "openPrice", "closePrice", "premium", "pnl", "risk", "expiration",
             "openDate", "closeDate", "tags", "underlyingOpen", "underlyingClose",
             "highReturnPct", "lowReturnPct", "highReturnPctDate", "lowReturnPctDate"]
    for day, rws in [("2099-01-02", export_rows)] + sorted((exports or {}).items()):
        with open(os.path.join(RAW, f"{day}.csv"), "w", newline="") as fo:
            w = csv.writer(fo); w.writerow(ecols)
            for r in rws:
                w.writerow([r.get(c, "") for c in ecols])


def _st_row(bot, day="2099-01-02", qty="1", tags="", pnl="10", typ="shortputspread"):
    return {"botName": bot, "type": typ, "description": "-500 put +498 put",
            "symbol": "QQQ", "status": "closed", "quantity": qty, "openPrice": "0.40",
            "closePrice": "0.20", "premium": "40", "pnl": pnl, "risk": "160",
            "expiration": day, "openDate": f"{day} 09:46:00",
            "closeDate": f"{day} 15:50:00", "tags": tags}


def _st_out(tmp, name):
    """A path inside the scratch root's data/ dir."""
    return os.path.join(tmp, "data", name)


def _st_run(tmp, argv_start="2099-01-01", extra=()):
    """Run main() against the scratch root at `tmp`, capturing stdout. Returns
    (exit_code_or_None, stdout, sys_exit_message_or_None). `extra` appends argv
    (a pinned date, --allow-rewind, ...).

    `--root` is passed explicitly rather than leaned on from _st_env's globals:
    it exercises the flag CI depends on, and it makes the case immune to an
    ambient $FLEET_ROOT in the environment running the selftest."""
    import io, contextlib
    buf = io.StringIO()
    old_argv = sys.argv
    sys.argv = (["build_ledger.py", "--ledger-start", argv_start, "--root", tmp]
                + list(extra))
    try:
        with contextlib.redirect_stdout(buf):
            main()
        return None, buf.getvalue(), None
    except SystemExit as e:
        return e.code, buf.getvalue(), str(e.code)
    finally:
        sys.argv = old_argv


def selftest():
    import tempfile, shutil, hashlib
    global ROOT, RAW, OUT, META_PATH
    keep = (ROOT, RAW, OUT, META_PATH)
    fails, results = 0, []

    # G-3 — the selftest asserts on itself: whatever these cases do, the repo's
    # live working ledger must be byte-identical when they are finished.
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def live_sha():
        p = os.path.join(repo, "data", "trades.csv")
        if not os.path.exists(p):
            return "absent"
        with open(p, "rb") as fo:
            return hashlib.sha256(fo.read()).hexdigest()

    live_before = live_sha()

    def check(name, got, want):
        nonlocal fails
        ok = got == want
        fails += not ok
        results.append((ok, name, got, want))
        return ok

    OPSBOT, NORMBOT = "TESTOPS-LAB-OPS", "GF-QQQ-IC-Ride"
    ops_meta = {"bot": OPSBOT, "pillar": OPS_PILLAR, "role": "ops",
                "underlying": "QQQ", "status": "ON", OPS_CLASS_COL: OPS_CLASS_VALUE}
    norm_meta = {"bot": NORMBOT, "pillar": "IC", "role": "experiment",
                 "underlying": "QQQ", "status": "ON", OPS_CLASS_COL: ""}

    tmp = tempfile.mkdtemp(prefix="bl-selftest-")
    try:
        # ---- N1-N6: the declared ops bot is excluded, and reported -------
        _st_env(tmp, [norm_meta, ops_meta],
                [_st_row(NORMBOT), _st_row(NORMBOT, day="2099-01-03"),
                 _st_row(OPSBOT, qty="3", tags="experiment,ops,lab"),
                 _st_row(OPSBOT, day="2099-01-03", qty="3", tags="experiment,ops,lab")])
        code, out, _ = _st_run(tmp)
        led = list(csv.DictReader(open(_st_out(tmp, "trades.csv"))))
        ops = list(csv.DictReader(open(_st_out(tmp, "ops_rows.csv"))))
        meta_j = json.load(open(_st_out(tmp, "ledger_meta.json")))
        check("N1  run succeeds with an ops bot present", code, None)
        check("N2  ZERO ops rows in the working ledger",
              sorted({r["bot"] for r in led}), [NORMBOT])
        check("N3  ops rows land in data/ops_rows.csv, in full ledger schema",
              (len(ops), sorted({r["bot"] for r in ops}),
               list(ops[0].keys()) == OPSCOLS), (2, [OPSBOT], True))
        check("N4  every ops row carries OPS_NOTE (visible, not silent)",
              all(r["note"] == OPS_NOTE for r in ops), True)
        check("N5  receipt counts + ops_bots/ops_rows name the exclusion",
              (meta_j["counts"]["post_cutover"], meta_j["counts"]["ops_rows"],
               meta_j["ops_bots"], meta_j["ops_rows"], len(led)),
              (4, 2, [OPSBOT], 2, 2))
        check("N6  stdout prints the LAB OPS-CLASS block naming the bot",
              ("LAB OPS-CLASS -> data/ops_rows.csv" in out) and (OPSBOT in out), True)
        check("N6b receipt contract names the SECOND axis",
              "LAB-OPS-EXCLUDED" in meta_j["contract"], True)
        check("N6c ops bot is absent from data/bots.csv (no aggregate row)",
              OPSBOT in open(_st_out(tmp, "bots.csv")).read(), False)

        # ---- N7: a declared ops bot with NO rows is still reported -------
        _st_env(tmp, [norm_meta, ops_meta], [_st_row(NORMBOT)])
        code, out, _ = _st_run(tmp)
        check("N7  declared-but-absent ops bot still prints (zero rows, not silent)",
              (code is None) and ("declared; no rows in this export" in out)
              and (OPSBOT in out), True)

        # ---- N8: the export-tag tripwire (undeclared Lab-tagged row) -----
        _st_env(tmp, [norm_meta],
                [_st_row(NORMBOT), _st_row("TESTOPS-LAB-DSTOP", tags="lab,ops")])
        before = open(_st_out(tmp, "trades.csv")).read()
        code, out, msg = _st_run(tmp)
        check("N8  undeclared `ops`-tagged row REFUSES the build (FATAL)",
              isinstance(code, str) and code.startswith("FATAL:")
              and "TESTOPS-LAB-DSTOP" in code, True)
        check("N8b nothing was written on that refusal",
              open(_st_out(tmp, "trades.csv")).read(), before)

        # ---- N9-N11: the group/pillar fence, both directions -------------
        _st_env(tmp, [norm_meta, dict(ops_meta, pillar="IC")], [_st_row(NORMBOT)])
        code, _, _ = _st_run(tmp)
        check("N9  ops_class=lab-ops with pillar != Lab REFUSES",
              isinstance(code, str) and "not in pillar 'Lab'" in code, True)

        _st_env(tmp, [norm_meta, dict(ops_meta, **{OPS_CLASS_COL: ""})], [_st_row(NORMBOT)])
        code, _, _ = _st_run(tmp)
        check("N10 pillar-Lab bot with no ops_class declaration REFUSES",
              isinstance(code, str) and "no `ops_class` declaration" in code, True)

        _st_env(tmp, [norm_meta, dict(ops_meta, **{OPS_CLASS_COL: "lab"})], [_st_row(NORMBOT)])
        code, _, _ = _st_run(tmp)
        check("N11 an unrecognised ops_class value REFUSES (never 'assume not ops')",
              isinstance(code, str) and "unrecognised `ops_class` value" in code, True)

        # ---- N12: the schema addition is load-bearing --------------------
        _st_env(tmp, [norm_meta], [_st_row(NORMBOT)],
                meta_header=["bot", "pillar", "role", "underlying", "status"])
        code, _, _ = _st_run(tmp)
        check("N12 bots_meta.csv without an ops_class column REFUSES",
              isinstance(code, str) and "has no `ops_class` column" in code, True)

        # ---- N13: the class-axis leak assertion itself -------------------
        fake = [["x"] * len(TCOLS) for _ in range(2)]
        fake[1][TCOLS.index("bot")] = OPSBOT
        try:
            assert_no_ops_leak(fake, {OPSBOT})
            got = "NO EXIT"
        except SystemExit as e:
            got = "FATAL" if str(e.code).startswith("FATAL: 1 LAB OPS-CLASS row") else str(e.code)
        check("N13 assert_no_ops_leak kills the run if an ops row reaches the writer",
              got, "FATAL")
        try:
            assert_no_ops_leak([["x"] * len(TCOLS)], {OPSBOT})
            got = "CLEAN"
        except SystemExit:
            got = "FALSE POSITIVE"
        check("N13b …and does not fire on a clean writer", got, "CLEAN")

        # ---- N14: FILTERED-EXPORT GUARD does not shout about an ops bot --
        _st_env(tmp, [norm_meta, ops_meta],
                [_st_row(NORMBOT), _st_row(OPSBOT, tags="lab,ops")])
        _st_run(tmp)                                   # seed a prior ledger
        _st_env(tmp, [norm_meta, ops_meta], [_st_row(NORMBOT)], keep_prior=True)
        # keep the prior trades.csv written by the seeding run
        code, out, _ = _st_run(tmp)
        check("N14 an ops bot missing from the export does NOT trip the "
              "FILTERED-EXPORT GUARD", "FILTERED-EXPORT WARNING" in out, False)

        # ---- N15: with NOTHING declared, behaviour is untouched ----------
        _st_env(tmp, [norm_meta], [_st_row(NORMBOT), _st_row(NORMBOT, day="2099-01-03")])
        code, out, _ = _st_run(tmp)
        opsf = list(csv.DictReader(open(_st_out(tmp, "ops_rows.csv"))))
        mj = json.load(open(_st_out(tmp, "ledger_meta.json")))
        check("N15 no ops bots declared -> no ops block, empty ops_rows.csv, counts 0",
              ("LAB OPS-CLASS" in out, len(opsf), mj["counts"]["ops_rows"], mj["ops_bots"]),
              (False, 0, 0, []))

        # ---- G1-G8: THE MONOTONICITY GUARD (G-2) -------------------------
        # G2 is commit 0051b5e6 rebuilt to scale: a ledger holding two days, then
        # a rebuild PINNED to the older, stale export. That is the run that
        # silently deleted 2026-08-11 on 2026-08-12. It must now refuse.
        day1, day2 = "2099-01-02", "2099-01-03"
        stale = [_st_row(NORMBOT)]                             # day1 only
        full  = [_st_row(NORMBOT), _st_row(NORMBOT, day=day2)]  # day1 + day2
        _st_env(tmp, [norm_meta], stale, exports={day2: full})

        code, out, _ = _st_run(tmp)                     # newest export -> both days
        led = list(csv.DictReader(open(_st_out(tmp, "trades.csv"))))
        check("G1  baseline — the newest export builds a two-day ledger",
              (code, sorted({r["open_date"][:10] for r in led})), (None, [day1, day2]))

        before = open(_st_out(tmp, "trades.csv")).read()
        code, out, _ = _st_run(tmp, extra=[day1])
        check("G2  0051b5e6 scenario — rebuild pinned to the OLDER export REFUSES",
              isinstance(code, str)
              and "REFUSED: this rebuild would walk the working ledger BACKWARDS" in code,
              True)
        check("G2b the refusal names BOTH max open_dates and the source export",
              isinstance(code, str) and (f": {day2}" in code) and (f": {day1}" in code)
              and (f"{day1}.csv" in code), True)
        check("G2c nothing was written — trades.csv is byte-identical",
              open(_st_out(tmp, "trades.csv")).read(), before)

        code, out, _ = _st_run(tmp, extra=[day1, "--allow-rewind"])
        led = list(csv.DictReader(open(_st_out(tmp, "trades.csv"))))
        check("G3  --allow-rewind permits the rewind, and says so in a banner",
              (code, "LEDGER REWIND" in out,
               sorted({r["open_date"][:10] for r in led})), (None, True, [day1]))

        code, out, _ = _st_run(tmp)                     # newest again -> forward
        led = list(csv.DictReader(open(_st_out(tmp, "trades.csv"))))
        check("G4  a FORWARD rebuild is never refused",
              (code, sorted({r["open_date"][:10] for r in led})), (None, [day1, day2]))

        code, out, _ = _st_run(tmp)
        check("G5  an idempotent re-run at the same max open_date is not a rewind",
              (code, "REFUSED" in out), (None, False))

        code, _, _ = _st_run(tmp, argv_start="2099-06-01")
        check("G6  a rebuild that would EMPTY a non-empty ledger refuses too",
              isinstance(code, str) and "the ledger would be emptied" in code, True)

        os.remove(_st_out(tmp, "trades.csv"))
        code, _, _ = _st_run(tmp, extra=[day1])
        check("G7  no prior ledger -> nothing to rewind, the pinned build runs",
              code, None)

        check("G8  max_open_date ignores blanks rather than sorting them first",
              (max_open_date([{"open_date": ""}, {"open_date": f"{day1} 09:46:00"}],
                             "open_date"),
               max_open_date([], "open_date")), (day1, ""))

        # ---- R1-R3: FIXTURE / LIVE SEPARATION (G-3) ----------------------
        check("R1  set_root points RAW/OUT/META at <root>/data",
              (RAW, OUT, META_PATH),
              (os.path.join(tmp, "data", "raw"), os.path.join(tmp, "data"),
               os.path.join(tmp, "data", "bots_meta.csv")))

        # R2 is the leak that made this selftest non-hermetic in the first place:
        # max_existing_tid()'s root defaulted to the module ROOT, bound at import
        # time, so a --root or selftest run seeded its trade_id counter from the
        # REPO's hedge_tournament.csv and trades.csv. A scratch run must read the
        # scratch accumulator and nothing outside its root.
        _st_env(tmp, [norm_meta], [_st_row(NORMBOT)])
        with open(_st_out(tmp, "hedge_tournament.csv"), "w", newline="") as fo:
            w = csv.writer(fo); w.writerow(["date", "trade_id"])
            w.writerow(["2099-01-01", "T00042"])
        code, _, _ = _st_run(tmp)
        led = list(csv.DictReader(open(_st_out(tmp, "trades.csv"))))
        check("R2  trade_id continues from the SCRATCH accumulator, not the repo's",
              (code, [r["trade_id"] for r in led]), (None, ["T00043"]))

        check("R3  the whole selftest left the repo's data/trades.csv byte-identical",
              live_sha(), live_before)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        ROOT, RAW, OUT, META_PATH = keep

    print("SELF-TEST — build_ledger.py")
    print("  N* = E-3 §3.3 LAB OPS-CLASS EXCLUSION")
    print("  G* = G-2 MONOTONICITY GUARD (ledger-truncation-forensics-2026-08-17.md §7)")
    print("  R* = G-3 FIXTURE / LIVE SEPARATION (--root)")
    print("=" * 74)
    for ok, name, got, want in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
        if not ok:
            print(f"        got  {got!r}\n        want {want!r}")
    print("-" * 74)
    print(f"{len(results) - fails}/{len(results)} passed")
    return 1 if fails else 0


if __name__ == "__main__":
    main()
