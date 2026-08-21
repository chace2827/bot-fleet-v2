#!/usr/bin/env python3
"""Append a per-run receipt for the daily loop (G-5).

=============================================================================
 WHY THIS EXISTS  (docs/ledger-truncation-forensics-2026-08-17.md §4, §7)
=============================================================================
On 2026-08-12 a rebuild pinned to a stale fixture deleted 2026-08-11 from the
working ledger. It stayed deleted, on master, for five days. The forensic §4
finding is one line long:

    "There are none for August. data/receipts/ stops at mirror-baseline.txt,
     2026-08-04. Nothing in the eight-stage pipeline writes a per-run receipt;
     data/ledger_meta.json is the only per-run artifact and it is OVERWRITTEN
     by each run, so it records the last run and no history." [the pipeline is nine-stage as of PR #44]

A single overwritten file cannot show that anything changed. The truncation was
invisible not because it was subtle but because no run left a trace that could
be diffed against the run before it. This script leaves that trace.

APPEND-ONLY, AND THAT IS THE WHOLE POINT. Receipts are written to
data/receipts/daily-runs.jsonl, one JSON object per line, opened 'a' and never
'w'. A receipts file that can be rewritten is `ledger_meta.json` again.

WRITTEN FROM THE EXIT TRAP, so a run that FAILED or was REFUSED leaves a receipt
too. Those are the runs worth having a record of: a G-2 rewind refusal, an
UNCLASSIFIED-bot refusal and a clean run must all be distinguishable afterwards
from the file alone.

What each receipt carries:
  - the resolved export path the ledger was rebuilt from, and whether the run
    was PINNED to a date or took the newest export
  - LEDGER_START and where it was resolved from
  - rows in (export rows) and rows out (working-ledger legs)
  - the min and max open_date actually written  <- the axis G-2 guards
  - sha256 of every output file
  - the per-stage exit codes and the final exit code
  - the ROOT it ran against, so a scratch run (G-3) can never be mistaken for a
    live one when the file is read back months later

STALENESS IS FLAGGED, NEVER SMOOTHED OVER. ledger_meta.json is only this run's
if the ledger stage actually rewrote it. When it did not — a refusal, a crash in
stage 1 — the receipt still reports the values but sets `ledger_meta_stale: true`
so the numbers are never read as this run's work.

Usage:
  python3 scripts/run_receipt.py              # env-driven; called by daily.sh
  python3 scripts/run_receipt.py --root DIR   # G-3 scratch root
  python3 scripts/run_receipt.py --selftest
"""
import argparse, csv, hashlib, json, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RECEIPT_NAME = os.path.join("receipts", "daily-runs.jsonl")

# Everything the loop regenerates. Hashed so two runs can be compared field by
# field, and so a file that changed when nothing should have is visible.
OUTPUTS = ["data/trades.csv", "data/bots.csv", "data/straddlers.csv",
           "data/ops_rows.csv", "data/ledger_meta.json",
           "data/execution_audit_findings.csv",
           "data/execution_audit_findings_meta.json",
           "data/hedge_tournament.csv", "data/trade_window.csv",
           "data/lessons.csv", "data/compliance.csv",
           "STATUS.md", "dashboard.html"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fo:
        for chunk in iter(lambda: fo.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def stages_from_env(env):
    """daily.sh exports HB_NAME_i / HB_CODE_i for the heartbeat; reuse them so
    the two artifacts can never disagree about what ran."""
    out, i = [], 0
    while f"HB_NAME_{i}" in env:
        try:
            code = int(env.get(f"HB_CODE_{i}", ""))
        except ValueError:
            code = None
        out.append({"stage": env[f"HB_NAME_{i}"], "exit": code})
        i += 1
    return out


def build_receipt(root, env=None, now=None):
    """Assemble one receipt. Pure: reads the tree, returns a dict, writes nothing."""
    env = os.environ if env is None else env
    data = os.path.join(root, "data")
    meta_path = os.path.join(data, "ledger_meta.json")
    trades_path = os.path.join(data, "trades.csv")

    try:
        started = float(env["FLEET_RUN_STARTED"])
    except (KeyError, ValueError, TypeError):
        started = None

    meta, ledger_stale = {}, None
    if os.path.exists(meta_path):
        try:
            with open(meta_path) as fo:
                meta = json.load(fo)
        except (ValueError, OSError):
            meta = {}
        # "Stale" = stage 1 did not rewrite the ledger on THIS run, so every
        # ledger field below (source_export, ledger_start, rows_in/out, the
        # open_date range) belongs to some EARLIER run and must not be read as
        # this one's work. ledger_meta.json is a faithful proxy for the whole
        # stage-1 output set: build_ledger.py writes it last, and every refusal
        # path in it writes nothing at all.
        # Without a run-start we cannot tell — null, never a guess.
        if started is not None:
            ledger_stale = os.path.getmtime(meta_path) < started

    counts = meta.get("counts", {}) or {}

    opens, n_legs = [], 0
    if os.path.exists(trades_path):
        with open(trades_path) as fo:
            for r in csv.DictReader(fo):
                n_legs += 1
                d = (r.get("open_date") or "")[:10]
                if d:
                    opens.append(d)

    src = meta.get("source_export")
    stages = stages_from_env(env)
    try:
        final_exit = int(env.get("HB_FINAL_EXIT", ""))
    except ValueError:
        final_exit = None

    hashes = {}
    for rel in OUTPUTS:
        p = os.path.join(root, rel)
        hashes[rel] = sha256(p) if os.path.exists(p) else None

    # R-2026-08-21-RECEIPT-ARGV: capture the invocation argv when daily.sh
    # exported it; absent means UNKNOWN. overrides are read from ledger_meta.json
    # like the other meta-derived fields and are null when the meta is old-shape.
    argv = None
    raw_argv = env.get("FLEET_ARGV")
    if raw_argv:
        try:
            argv = json.loads(raw_argv)
        except (ValueError, TypeError):
            argv = None
    overrides = meta.get("overrides") if isinstance(meta, dict) else None

    ts = now or datetime.datetime.now(datetime.timezone.utc)
    # NOT derived from __file__: under G-3 the stages run out of a COPY of
    # scripts/ inside the scratch root, so this file's own location IS the root
    # and would report every scratch run as live. daily.sh exports FLEET_REPO
    # for exactly this comparison; the __file__ form is only the fallback for a
    # direct invocation from the repo.
    repo = os.path.abspath(env.get("FLEET_REPO")
                           or os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return {
        "written_utc": ts.replace(microsecond=0).isoformat(),
        "day": env.get("HB_DAY") or None,
        "pinned": bool(env.get("FLEET_PINNED_DAY")),
        "root": root,
        "repo": repo,
        "scratch_run": os.path.abspath(root) != repo,
        "source_export": (os.path.join("data", "raw", src) if src else None),
        "ledger_start": meta.get("ledger_start"),
        "ledger_start_source": meta.get("ledger_start_source"),
        "ledger_stale": ledger_stale,
        "rows_in": counts.get("export_rows"),
        "rows_out": n_legs,
        "counts": counts,
        "min_open_date": min(opens) if opens else None,
        "max_open_date": max(opens) if opens else None,
        "stages": stages,
        "final_exit": final_exit,
        "hashes": hashes,
        "argv": argv,
        "overrides": overrides,
    }


def append_receipt(root, receipt):
    """The only writer. Mode 'a', always — see the module docstring."""
    path = os.path.join(root, "data", RECEIPT_NAME)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as fo:
        fo.write(json.dumps(receipt, sort_keys=True) + "\n")
    return path


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--root", default=None,
                    help="write the receipt under DIR/data instead of the repo's "
                         "(G-3). Defaults to $FLEET_ROOT, then the repo.")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    root = args.root or os.environ.get("FLEET_ROOT") or ROOT
    receipt = build_receipt(root)
    path = append_receipt(root, receipt)
    rel = os.path.relpath(path, root)
    print(f"run_receipt.py: appended 1 receipt -> {rel} "
          f"(rows_in {receipt['rows_in']} -> rows_out {receipt['rows_out']}, "
          f"open_date {receipt['min_open_date']}..{receipt['max_open_date']}, "
          f"exit {receipt['final_exit']})")


# ===========================================================================
# SELF-TEST — house style: fixtures + a named check matrix, run with --selftest
# ===========================================================================
def selftest():
    import tempfile, shutil
    fails, results = 0, []

    def check(name, got, want):
        nonlocal fails
        ok = got == want
        fails += not ok
        results.append((ok, name, got, want))

    tmp = tempfile.mkdtemp(prefix="rcpt-selftest-", dir=ROOT)
    try:
        data = os.path.join(tmp, "data")
        os.makedirs(data)
        with open(os.path.join(data, "trades.csv"), "w", newline="") as fo:
            w = csv.writer(fo); w.writerow(["bot", "trade_id", "open_date"])
            w.writerow(["GF-QQQ-IC-Ride", "T00001", "2099-01-02 09:46:00"])
            w.writerow(["GF-QQQ-IC-Ride", "T00002", "2099-01-03 09:46:00"])
        with open(os.path.join(data, "ledger_meta.json"), "w") as fo:
            json.dump({"ledger_start": "2099-01-01",
                       "ledger_start_source": "$LEDGER_START",
                       "source_export": "2099-01-03.csv",
                       "counts": {"export_rows": 17, "post_cutover": 2}}, fo)

        env = {"HB_DAY": "2099-01-03", "HB_FINAL_EXIT": "0",
               "HB_NAME_0": "build_ledger", "HB_CODE_0": "0",
               "HB_NAME_1": "tape", "HB_CODE_1": "0",
               "FLEET_RUN_STARTED": "0"}          # 0 => everything reads fresh

        r1 = build_receipt(tmp, env=env)
        check("S1  the five spec'd fields are all present and populated",
              (r1["source_export"], r1["ledger_start"], r1["rows_in"],
               r1["rows_out"], r1["min_open_date"], r1["max_open_date"]),
              (os.path.join("data", "raw", "2099-01-03.csv"), "2099-01-01",
               17, 2, "2099-01-02", "2099-01-03"))

        check("S2  output hashes are real sha256 of the files on disk",
              r1["hashes"]["data/trades.csv"],
              sha256(os.path.join(data, "trades.csv")))

        check("S2b a missing output is null, not an empty hash",
              r1["hashes"]["dashboard.html"], None)

        check("S3  per-stage exit codes come through from the heartbeat env",
              r1["stages"], [{"stage": "build_ledger", "exit": 0},
                             {"stage": "tape", "exit": 0}])

        # --- APPEND-ONLY: two runs, two lines, line 1 untouched -----------
        p = append_receipt(tmp, r1)
        first = open(p).read()
        r2 = build_receipt(tmp, env=dict(env, HB_FINAL_EXIT="1"))
        append_receipt(tmp, r2)
        both = open(p).read()
        lines = both.splitlines()
        check("S4  a second run APPENDS — two lines, and line 1 is byte-identical",
              (len(lines), both.startswith(first)), (2, True))

        check("S4b every line is independently parseable JSON",
              [json.loads(x)["final_exit"] for x in lines], [0, 1])

        # --- a FAILED / REFUSED run still leaves a receipt ------------------
        failed_env = {"HB_DAY": "2099-01-03", "HB_FINAL_EXIT": "1",
                      "HB_NAME_0": "build_ledger", "HB_CODE_0": "1",
                      "FLEET_RUN_STARTED": "0"}
        rf = build_receipt(tmp, env=failed_env)
        check("S5  a run that died in stage 1 still produces a receipt naming it",
              (rf["final_exit"], rf["stages"]), (1, [{"stage": "build_ledger",
                                                      "exit": 1}]))

        # --- staleness is FLAGGED, not smoothed over -----------------------
        # This is the G-2-refusal case: stage 1 wrote nothing, so the ledger
        # fields in the receipt are the PREVIOUS run's and must say so.
        future = str(os.path.getmtime(os.path.join(data, "ledger_meta.json")) + 3600)
        rs = build_receipt(tmp, env=dict(env, FLEET_RUN_STARTED=future))
        check("S6  a ledger stage 1 did not rewrite this run is flagged stale",
              (rs["ledger_stale"], rs["ledger_start"]), (True, "2099-01-01"))
        check("S6b …and is NOT flagged stale when the run did write it",
              r1["ledger_stale"], False)
        check("S6c with no run-start to compare against, staleness is null, "
              "never a guess",
              build_receipt(tmp, env={k: v for k, v in env.items()
                                      if k != "FLEET_RUN_STARTED"}
                            )["ledger_stale"], None)

        # --- G-3: a scratch run is labelled as one -------------------------
        # The regression this pins: derived from __file__, `repo` equals the
        # SCRATCH root whenever the stages run from the root's own copy of
        # scripts/, and every scratch run reports itself as live.
        check("S7  a run outside the repo is marked scratch_run",
              (r1["scratch_run"],
               build_receipt(ROOT, env=env)["scratch_run"]), (True, False))
        check("S7b the repo is taken from $FLEET_REPO, not from this file's path",
              (build_receipt(tmp, env=dict(env, FLEET_REPO=tmp))["scratch_run"],
               build_receipt(ROOT, env=dict(env, FLEET_REPO=tmp))["scratch_run"]),
              (False, True))

        # --- the writer never truncates ------------------------------------
        src = open(os.path.abspath(__file__)).read()
        body = src.split("def append_receipt", 1)[1].split("\ndef ", 1)[0]
        check("S8  append_receipt opens the receipts file in append mode only",
              ('open(path, "a")' in body) and ('open(path, "w")' not in body), True)

        # --- R-2026-08-21-RECEIPT-ARGV ---------------------------------------
        check("S9  FLEET_ARGV absent -> argv is null",
              r1["argv"], None)
        check("S10 old-shape ledger_meta.json (no override block) -> overrides is null",
              r1["overrides"], None)

        # overrides all-false, with a FLEET_ARGV that exercises JSON escaping
        with open(os.path.join(data, "ledger_meta.json"), "w") as fo:
            json.dump({"ledger_start": "2099-01-01",
                       "ledger_start_source": "$LEDGER_START",
                       "source_export": "2099-01-03.csv",
                       "counts": {"export_rows": 17, "post_cutover": 2},
                       "overrides": {"allow_rewind": False,
                                     "allow_front_truncate": False,
                                     "allow_ops_reclass": False}}, fo)
        tricky = ["2026-08-21", "--allow-rewind", 'a"b\\c']
        env_with_argv = dict(env, FLEET_ARGV=json.dumps(tricky))
        raf = build_receipt(tmp, env=env_with_argv)
        check("S11 override absent (all-false) is recorded as all-false",
              raf["overrides"],
              {"allow_rewind": False,
               "allow_front_truncate": False,
               "allow_ops_reclass": False})
        check("S12 FLEET_ARGV present with quotes/backslash -> argv parsed",
              raf["argv"], tricky)

        # override present and recorded true
        with open(os.path.join(data, "ledger_meta.json"), "w") as fo:
            json.dump({"ledger_start": "2099-01-01",
                       "ledger_start_source": "$LEDGER_START",
                       "source_export": "2099-01-03.csv",
                       "counts": {"export_rows": 17, "post_cutover": 2},
                       "overrides": {"allow_rewind": True,
                                     "allow_front_truncate": False,
                                     "allow_ops_reclass": False}}, fo)
        rt = build_receipt(tmp, env=env)
        check("S13 override present and recorded true",
              (rt["overrides"]["allow_rewind"],
               rt["overrides"]["allow_front_truncate"],
               rt["overrides"]["allow_ops_reclass"]),
              (True, False, False))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("SELF-TEST — run_receipt.py (G-5 per-run receipts)")
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
