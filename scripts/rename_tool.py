#!/usr/bin/env python3
"""Rename safety tool for the OA cleanup (oa-cleanup-runbook.md, Phase 3).

The ledger classifies every leg by its EXACT `botName` in the OA export
(see build_ledger.py). A rename is only safe if OA re-exports a bot's WHOLE
history under the new name. If OA instead keeps old legs under the old name and
only writes new legs under the new one, a rename SPLITS the bot's history — half
of it throws `unclassified bot` warnings and the champion gate can break.

This tool has two jobs:

  check  — Before trusting any rename, probe it. Renames are listed in
           data/renames_pending.csv (old,new,hold,note). For each pending rename
           this compares the leg counts for OLD and NEW names in the newest
           export and prints a verdict:
             CLEAN     old=0, new>0   OA rewrote history -> safe, edit meta
             STRANDED  old>0, new=0   rename ignored by export -> DO NOT rename
                                      for real; freeze history first (runbook P0)
             SPLIT     old>0, new>0   history fractured -> STOP
             NOT-DONE  old=0, new=0   rename not in this export yet
           It also re-checks full meta coverage (any export bot missing from
           bots_meta.csv) so nothing slips through unclassified.

  apply OLD  — After `check` shows CLEAN for a rename, apply its one-row edit to
               data/bots_meta.csv (bot field old->new), preserving every other
               field. Refuses if the row is marked hold=yes. Then you rebuild:
               python3 scripts/build_ledger.py && python3 scripts/report.py

Usage:
  python3 scripts/rename_tool.py check
  python3 scripts/rename_tool.py apply SPX-IC-0DTE-Fortress-Baseline-v1
"""
import csv, glob, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
META = os.path.join(ROOT, "data", "bots_meta.csv")
PENDING = os.path.join(ROOT, "data", "renames_pending.csv")


def exports():
    return sorted(glob.glob(os.path.join(RAW, "*.csv")))


def leg_counts(path):
    rows = list(csv.DictReader(open(path)))
    return collections.Counter(r["botName"] for r in rows)


def meta_names():
    return {r["bot"] for r in csv.DictReader(open(META))}


def pending():
    if not os.path.exists(PENDING):
        sys.exit(f"ERROR: missing {PENDING}")
    return list(csv.DictReader(open(PENDING)))


def cmd_check():
    files = exports()
    if not files:
        sys.exit("ERROR: no export in data/raw/")
    newest = files[-1]
    cur = leg_counts(newest)
    print(f"Newest export: {os.path.basename(newest)}  ({sum(cur.values())} legs, {len(cur)} bots)")

    if len(files) >= 2:
        prev = leg_counts(files[-2])
        appeared = sorted(set(cur) - set(prev))
        gone = sorted(set(prev) - set(cur))
        if appeared:
            print("  Bot names that APPEARED vs previous export:")
            for b in appeared:
                print(f"    + {b}  ({cur[b]} legs)")
        if gone:
            print("  Bot names that DISAPPEARED vs previous export:")
            for b in gone:
                print(f"    - {b}  (was {prev[b]} legs)")
        if not appeared and not gone:
            print("  No bot-name changes vs previous export.")

    print("\nPending-rename verdicts:")
    for r in pending():
        old, new, hold = r["old"], r["new"], r.get("hold", "").strip().lower()
        o, n = cur.get(old, 0), cur.get(new, 0)
        if o == 0 and n > 0:
            v = f"CLEAN     (new={n} legs, old gone)"
        elif o > 0 and n == 0:
            v = f"STRANDED  (old still {o} legs, new absent)"
        elif o > 0 and n > 0:
            v = f"SPLIT     (old={o}, new={n}) -- STOP"
        else:
            v = "NOT-DONE  (neither name in export)"
        tag = " [HOLD]" if hold == "yes" else (" [probe]" if hold == "probe" else "")
        print(f"  {old}{tag}")
        print(f"      -> {new}")
        print(f"      {v}")

    missing = sorted(set(cur) - meta_names())
    print("\nMeta coverage:")
    if missing:
        print(f"  WARNING: {len(missing)} export bot(s) NOT in bots_meta.csv:")
        for b in missing:
            print(f"    - {b}  ({cur[b]} legs)")
    else:
        print("  OK — every export bot is classified in bots_meta.csv.")


def cmd_apply(old):
    row = next((r for r in pending() if r["old"] == old), None)
    if not row:
        sys.exit(f"ERROR: '{old}' is not in renames_pending.csv")
    if row.get("hold", "").strip().lower() == "yes":
        sys.exit(f"REFUSED: '{old}' is marked hold=yes ({row.get('note','')}).")
    if row.get("hold", "").strip().lower() == "probe":
        sys.exit(f"REFUSED: '{old}' is a probe row — rename it back in OA, don't edit meta.")
    new = row["new"]

    rows = list(csv.DictReader(open(META)))
    cols = rows[0].keys() if rows else None
    hit = [r for r in rows if r["bot"] == old]
    if not hit:
        sys.exit(f"ERROR: '{old}' not found in bots_meta.csv (already renamed?)")
    for r in rows:
        if r["bot"] == old:
            r["bot"] = new
    with open(META, "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=list(cols))
        w.writeheader(); w.writerows(rows)
    print(f"bots_meta.csv: {old} -> {new}")
    print("Now rebuild:  python3 scripts/build_ledger.py && python3 scripts/report.py")
    print("Expect: no 'unclassified bot' warning, totals unchanged.")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "check":
        cmd_check()
    elif len(sys.argv) == 3 and sys.argv[1] == "apply":
        cmd_apply(sys.argv[2])
    else:
        sys.exit(__doc__)
