#!/usr/bin/env python3
"""Rerun the daily pipeline on committed inputs and refuse any unexplained change.

The contract this enforces: given the same inputs, the pipeline produces the same
outputs. A generated artifact that changes on rerun cannot support a graded
conclusion, because the number in the tree is not the number the inputs imply.
That is not hypothetical here — data/hedge_tournament.csv currently carries
trade_ids that its own ledger no longer uses.

Timestamps are excluded via scripts/ci/normalize.py; everything else is a failure.
An artifact the pipeline writes but git does not track is also a failure, since it
means a graded output is living outside the audit trail.

Requires a clean tree (it compares against HEAD and then restores).

Exit 0 = reproducible.  Exit 1 = drift.  Exit 2 = could not run the check.
"""
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from normalize import normalize  # noqa: E402


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO, capture_output=True, text=True, check=True
    ).stdout


def main() -> int:
    dirty = git("status", "--porcelain").strip()
    if dirty:
        print("REFUSING: working tree is not clean. Commit or stash first:\n" + dirty)
        return 2

    print("== running scripts/daily.sh ==")
    run = subprocess.run(
        ["bash", "scripts/daily.sh"], cwd=REPO, capture_output=True, text=True
    )
    if run.returncode != 0:
        print(run.stdout)
        print(run.stderr, file=sys.stderr)
        print(f"FAIL: daily.sh exited {run.returncode}")
        return 1

    status = [ln for ln in git("status", "--porcelain").splitlines() if ln.strip()]
    drifted, untracked = [], []
    for line in status:
        code, path = line[:2].strip(), line[3:].strip().strip('"')
        if code == "??":
            untracked.append(path)
            continue
        before = normalize(git("show", f"HEAD:{path}"))
        after = normalize((REPO / path).read_text(encoding="utf-8", errors="replace"))
        if before != after:
            drifted.append(path)

    # Restore only what this run rewrote. The clean-tree guard above means nothing
    # else can be in flight, and naming the paths keeps it that way if that changes.
    tracked = [line[3:].strip().strip('"') for line in status if line[:2].strip() != "??"]
    if tracked:
        git("checkout", "--", *tracked)

    if not drifted and not untracked:
        print(f"\nPASS: pipeline reproducible ({len(status)} artifact(s) rewritten, "
              "timestamps only)")
        return 0

    print("\nFAIL: the pipeline does not reproduce its own committed outputs.")
    for path in drifted:
        print(f"  DRIFT      {path}  (differs beyond the generated timestamp)")
    for path in untracked:
        print(f"  UNTRACKED  {path}  (written by the pipeline, not tracked by git)")
    print("\nEither the committed artifact is stale — regenerate and commit it — or a "
          "stage is not deterministic. Do not merge until this is green.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
