#!/usr/bin/env python3
"""W2 replay harness: rebuild the six 2026-08-10..17 tape files from the
committed W0 Tradier raw captures by monkeypatching scripts/tape.py's _get().

Emits:
  data/brief/2026-08-10..17_tape.json

Each emitted tape:
  - uses the gates union (SPX, QQQ, VIX) per R-2026-08-19-TAPE-SYMBOLS-FROM-GATES
  - sets source = "tradier" for every underlying
  - includes the VIX 5-min series (79 bars)
  - carries backfilled_at and backfill_evidence citing the raw captures and the
    authorizing ruling R-2026-08-19-TAPE-BACKFILL-AND-VIX-SERIES

Does NOT call the Tradier API and does NOT read any credential.
"""
import datetime, json, os, sys

# ---------------------------------------------------------------------------
# paths
SP = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(SP, "..", "..", "..", ".."))
RAW = os.path.join(ROOT, "data", "captures", "2026-08-19-tape-backfill", "raw")
CAND = os.path.normpath(SP)
BRIEF = os.path.join(ROOT, "data", "brief")

DAYS = ["2026-08-10", "2026-08-11", "2026-08-12", "2026-08-13", "2026-08-14", "2026-08-17"]
CANDIDATE_DAYS = ["2026-08-10", "2026-08-11", "2026-08-12", "2026-08-13"]

BACKFILL_EVIDENCE = (
    "Backfilled from committed raw Tradier response bodies in "
    "data/captures/2026-08-19-tape-backfill/raw/ (SPX, QQQ, VIX daily + 5min). "
    "No Tradier API call was made and no credential was read. "
    "Authorized by R-2026-08-19-TAPE-BACKFILL-AND-VIX-SERIES and "
    "R-2026-08-19-TAPE-SYMBOLS-FROM-GATES."
)

# ---------------------------------------------------------------------------
# Make sure tape.py sees a non-empty token so it follows the live/_get path,
# but never uses a real credential.  Base is a placeholder.
os.environ["TRADIER_TOKEN"] = "REPLAY"
os.environ["TRADIER_BASE"] = "https://replay.invalid"

sys.path.insert(0, os.path.join(ROOT, "scripts"))
import tape as T  # noqa: E402


def _get(base, path, params, token):
    """Replay _get from the committed raw response bodies."""
    sym = params["symbol"]
    if path == "markets/history":
        day = params["end"]
        name = f"{sym}_{day}_daily.json"
    elif path == "markets/timesales":
        day = params["start"][:10]
        name = f"{sym}_{day}_5min.json"
    else:
        raise RuntimeError(f"unexpected _get path: {path}")
    fpath = os.path.join(RAW, name)
    if not os.path.exists(fpath):
        raise RuntimeError(f"raw capture missing: {fpath}")
    with open(fpath, "rb") as fh:
        return json.loads(fh.read().decode())


T._get = _get


def capture_old_pct_move(day):
    p = os.path.join(BRIEF, f"{day}_tape.json")
    if not os.path.exists(p):
        return None
    try:
        old = json.load(open(p))
        return old.get("underlyings", {}).get("SPX", {}).get("pct_move")
    except Exception:
        return None


def add_provenance(day, now):
    p = os.path.join(BRIEF, f"{day}_tape.json")
    with open(p) as fh:
        tape = json.load(fh)
    tape["backfilled_at"] = now
    tape["backfill_evidence"] = BACKFILL_EVIDENCE
    # ensure these reflect the real raw-capture source
    for u in tape.get("underlyings", {}).values():
        if u.get("source") == "reconstructed":
            raise RuntimeError(
                f"{day} {u.get('symbol')} source is reconstructed — raw capture was not used"
            )
    with open(p, "w") as fh:
        json.dump(tape, fh, indent=2)
    return tape


def norm(tape):
    """Drop volatile/provenance fields before comparison."""
    t = json.loads(json.dumps(tape))
    for k in ("generated", "backfilled_at", "backfill_evidence"):
        t.pop(k, None)
    return t


def write_stop(reason):
    with open("/tmp/w2-STOP.txt", "w") as fh:
        fh.write(reason + "\n")
    print(f"\nSTOP: wrote /tmp/w2-STOP.txt\n{reason}")
    sys.exit(1)


def main():
    old_pct = {day: capture_old_pct_move(day) for day in DAYS}
    now = datetime.datetime.now().isoformat(timespec="seconds")

    # build the six tapes using tape.py's own build path
    for day in DAYS:
        print(f"building {day}...")
        T.build(day)
        add_provenance(day, now)

    # -----------------------------------------------------------------------
    # Check 1: per-date underlyings, source, bar counts
    print("\n=== Check 1: per-date underlyings/source/bar counts ===")
    table = []
    all_ok = True
    for day in DAYS:
        p = os.path.join(BRIEF, f"{day}_tape.json")
        tape = json.load(open(p))
        row = {"date": day, "underlyings": []}
        for sym, u in tape.get("underlyings", {}).items():
            n = len(u.get("series") or [])
            src = u.get("source")
            row["underlyings"].append((sym, src, n))
            if src != "tradier":
                all_ok = False
                print(f"  FAIL {day} {sym}: source={src} (expected tradier)")
            if sym in ("SPX", "QQQ", "VIX") and n != 79:
                all_ok = False
                print(f"  FAIL {day} {sym}: bars={n} (expected 79)")
        table.append(row)
        parts = ", ".join(f"{s}:{src}({n})" for s, src, n in row["underlyings"])
        print(f"  {day} | {parts}")

    if not all_ok:
        write_stop("Check 1 failed: one or more underlyings had wrong source or bar count.")

    # -----------------------------------------------------------------------
    # Check 2: cross-check 08-10..13 against W0 independent candidates
    print("\n=== Check 2: cross-check vs W0 candidate tapes ===")
    print("normalized-away (volatile/provenance): generated, backfilled_at, backfill_evidence")
    cross_ok = True
    for day in CANDIDATE_DAYS:
        cand_path = os.path.join(CAND, f"{day}_tape.CANDIDATE-gates-vixseries.json")
        our_path = os.path.join(BRIEF, f"{day}_tape.json")
        cand = norm(json.load(open(cand_path)))
        ours = norm(json.load(open(our_path)))
        a = json.dumps(cand, sort_keys=True, indent=2)
        b = json.dumps(ours, sort_keys=True, indent=2)
        if a == b:
            print(f"  MATCH  {day}")
        else:
            cross_ok = False
            print(f"  DIFF   {day}")
            import difflib
            for line in list(difflib.unified_diff(a.split("\n"), b.split("\n"),
                                                  "candidate", "ours", lineterm=""))[:60]:
                print("    " + line)
    if not cross_ok:
        write_stop("Check 2 failed: one or more backfilled tapes differs from the W0 candidate.")

    # -----------------------------------------------------------------------
    # Check 3: 08-10 pct_move old vs new
    print("\n=== Check 3: 2026-08-10 pct_move old vs new ===")
    new_pct = json.load(open(os.path.join(BRIEF, "2026-08-10_tape.json")))
    new_pct = new_pct.get("underlyings", {}).get("SPX", {}).get("pct_move")
    old = old_pct.get("2026-08-10")
    print(f"  old (reconstructed): {old}")
    print(f"  new (tradier):       {new_pct}")
    if old is not None and new_pct is not None and old == new_pct:
        write_stop(f"Check 3 failed: 08-10 pct_move unchanged at {old}.")

    print("\nAll W2 checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
