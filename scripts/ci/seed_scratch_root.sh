#!/usr/bin/env bash
# Materialise a SCRATCH ROOT for hermetic pipeline runs.
#
# G-3 (docs/ledger-truncation-forensics-2026-08-17.md §7). Every script in this
# repo resolves its paths from its OWN location —
#   ROOT = dirname(dirname(abspath(__file__)))
# — so a copy of scripts/ sitting under DIR makes all eight daily-loop stages
# read and write DIR/data instead of the repo's. That is the whole mechanism:
# there is no per-script flag to thread through, and no cwd to get wrong.
#
# What goes where, and why:
#   scripts/   COPIED, and REFRESHED on every call. A scratch root must never
#              run stale code — that would make CI green against a version of
#              the pipeline that no longer exists.
#   data/      COPIED ONCE, then OWNED by the scratch root. Not refreshed: a
#              determinism run is run-1 -> run-2 against the SAME data, which is
#              what proves the accumulators (hedge_tournament.csv, lessons.csv)
#              are idempotent. Re-seeding between runs would silently downgrade
#              that to two independent from-clean runs.
#   docs/      SYMLINKED. Read-only in the loop — report.py reads backlog.md,
#              lessons.py reads session-log.md; no stage writes docs/.
#
# NOT copied: .env. A scratch run has no Tradier token, so tape.py falls back to
# ledger reconstruction and says so. Scratch roots are for determinism proofs and
# fixture runs; set TAPE_FIXTURE=1 as CI does.
#
# Usage:
#   scripts/ci/seed_scratch_root.sh /tmp/fleet-scratch
#   FLEET_ROOT=/tmp/fleet-scratch scripts/daily.sh 2026-08-10   # seeds on demand
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
DEST="${1:-}"

if [ -z "$DEST" ]; then
  echo "usage: $0 <scratch-root-dir>" >&2
  exit 2
fi

mkdir -p "$DEST"
DEST="$(cd "$DEST" && pwd)"

# A scratch root INSIDE the repo defeats the point: its outputs would land in
# the working tree, show up in git status, and be committable.
case "$DEST" in
  "$REPO"|"$REPO"/*)
    echo "REFUSED: scratch root $DEST is inside the repo ($REPO)." >&2
    echo "  The point of a scratch root is that the repo cannot be written." >&2
    exit 1
    ;;
esac

# --- code: always refreshed ------------------------------------------------
rm -rf "$DEST/scripts"
cp -R "$REPO/scripts" "$DEST/scripts"
rm -rf "$DEST/scripts/__pycache__"

# --- read-only reference tree ---------------------------------------------
ln -sfn "$REPO/docs" "$DEST/docs"

# --- data: seeded once, then the scratch root's own ------------------------
if [ ! -d "$DEST/data" ]; then
  cp -R "$REPO/data" "$DEST/data"
  SEEDED="data/ copied from the repo"
else
  SEEDED="data/ already present — left as it is (run N+1 must see run N's output)"
fi

# report.py rewrites these in place; give it something to overwrite.
for f in STATUS.md dashboard.html; do
  [ -f "$DEST/$f" ] || [ ! -f "$REPO/$f" ] || cp "$REPO/$f" "$DEST/$f"
done

echo "SCRATCH ROOT: $DEST"
echo "  scripts/ refreshed from $REPO"
echo "  docs/    -> symlink to $REPO/docs"
echo "  $SEEDED"
