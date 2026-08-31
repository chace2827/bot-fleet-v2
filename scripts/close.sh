#!/usr/bin/env bash
# close.sh — one-command daily close orchestrator.
#
# Implements R-2026-08-21-CLOSE-RECEIPT-SURFACE (WRAP, Option 1):
#   ingest_export -> daily.sh <day> -> capture_bundle -> render_brief ->
#   close_manifest -> print derived commit command.
#
# This script NEVER runs git. It prints the derived commit command for Andy
# to run.  TOTAL_STAGES=9 in daily.sh is untouched.
#
# Usage:
#   scripts/close.sh [YYYY-MM-DD]
#   FLEET_ROOT=/tmp/scratch scripts/close.sh 2026-08-21
#   INGEST_DOWNLOADS=/path/to/exports scripts/close.sh 2026-08-21
#
# Capture handling:
#   - If CAPTURE_TXT is set, it is used as the raw /bots capture .txt, and
#     CAPTURE_SCREENSHOTS (colon-separated) are passed as screenshots.
#   - Otherwise, close.sh looks for raw capture files in
#     $CAPTURE_INBOX/<day>/ (default data/captures/<day>/):
#     exactly one .txt and any .png/.jpg/.jpeg/.pdf in the same directory.
#   - If no raw capture is found, the manifest records capture: ABSENT.
#
# Scratch runs:
#   If FLEET_ROOT is outside the repo and has no scripts/ directory, the
#   seed_scratch_root.sh helper copies the daily-loop scripts and a one-time
#   snapshot of data/ so the scratch root is self-contained.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "${FLEET_ROOT:-$REPO}"
FLEET_ROOT="$(cd "${FLEET_ROOT:-$REPO}" && pwd)"
export FLEET_ROOT

SCRIPTS="$FLEET_ROOT/scripts"
[ -d "$SCRIPTS" ] || SCRIPTS="$REPO/scripts"

DAY="${1:-}"
if [ -z "$DAY" ]; then
  DAY="$(python3 - <<'PY'
import glob, os
files = sorted(glob.glob(os.path.join(os.environ.get('FLEET_ROOT','.'), 'data/raw/*.csv')))
if files:
    print(os.path.basename(files[-1])[:-4])
else:
    import datetime
    print(datetime.date.today().isoformat())
PY
  )"
fi

if ! [[ "$DAY" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "close.sh: FATAL: day must be YYYY-MM-DD, got $DAY" >&2
  exit 2
fi

# R-2026-08-21-RECEIPT-ARGV: the close invocation itself is recorded.
export FLEET_CLOSE_ARGV="$(python3 -c 'import json,sys; print(json.dumps(sys.argv[1:]))' "$@")"

export PYTHONDONTWRITEBYTECODE=1

# If this is a scratch root, daily.sh needs its own copy of scripts/ in the
# root so its stages resolve to the root's data/ (G-3).
if [ "$FLEET_ROOT" != "$REPO" ] && [ ! -d "$FLEET_ROOT/scripts" ]; then
  "$SCRIPTS/ci/seed_scratch_root.sh" "$FLEET_ROOT"
fi

echo "== close $DAY FLEET_ROOT=$FLEET_ROOT =="

# ---------------------------------------------------------------------------
# 1. Ingest the OA export from the downloads/fallback inbox into data/raw.
# ---------------------------------------------------------------------------
INGEST_ARGS=()
if [ -n "${INGEST_DOWNLOADS:-}" ]; then
  INGEST_ARGS+=("--downloads" "$INGEST_DOWNLOADS")
fi
echo "== 1/5 ingest_export $DAY =="
if [ ${#INGEST_ARGS[@]} -gt 0 ]; then
  python3 "$SCRIPTS/ingest_export.py" --root "$FLEET_ROOT" --day "$DAY" "${INGEST_ARGS[@]}"
else
  python3 "$SCRIPTS/ingest_export.py" --root "$FLEET_ROOT" --day "$DAY"
fi

# ---------------------------------------------------------------------------
# 2. Run the nine-stage daily loop (untouched).
# ---------------------------------------------------------------------------
echo "== 2/5 daily.sh $DAY =="
"$SCRIPTS/daily.sh" "$DAY"

# ---------------------------------------------------------------------------
# 3. Build the /bots roster capture bundle, ONLY if raw files are present.
# ---------------------------------------------------------------------------
CAPTURE_TXT="${CAPTURE_TXT:-}"
CAPTURE_SCREENSHOTS_STR="${CAPTURE_SCREENSHOTS:-}"
CAPTURE_SCREENSHOTS=()

if [ -n "$CAPTURE_TXT" ]; then
  if [ -n "$CAPTURE_SCREENSHOTS_STR" ]; then
    IFS=':' read -ra CAPTURE_SCREENSHOTS <<< "$CAPTURE_SCREENSHOTS_STR"
  fi
else
  CAPTURE_IN="${CAPTURE_INBOX:-$FLEET_ROOT/data/captures}/$DAY"
  if [ -d "$CAPTURE_IN" ]; then
    # exactly one .txt, plus any screenshots in the same directory
    TXTS=("$CAPTURE_IN"/*.txt)
    if [ -f "${TXTS[0]}" ]; then
      if [ ${#TXTS[@]} -gt 1 ]; then
        echo "close.sh: FATAL: more than one raw /bots capture .txt in $CAPTURE_IN" >&2
        exit 1
      fi
      CAPTURE_TXT="${TXTS[0]}"
      for ext in png jpg jpeg pdf; do
        for s in "$CAPTURE_IN"/*.$ext; do
          [ -f "$s" ] && CAPTURE_SCREENSHOTS+=("$s")
        done
      done
    fi
  fi
fi

echo "== 3/5 capture_bundle $DAY =="
if [ -n "$CAPTURE_TXT" ]; then
  if [ ${#CAPTURE_SCREENSHOTS[@]} -gt 0 ]; then
    python3 "$SCRIPTS/capture_bundle.py" --out-root "$FLEET_ROOT/data/captures" \
      "$CAPTURE_TXT" "${CAPTURE_SCREENSHOTS[@]}"
  else
    python3 "$SCRIPTS/capture_bundle.py" --out-root "$FLEET_ROOT/data/captures" \
      "$CAPTURE_TXT"
  fi
else
  echo "close.sh: no raw capture files found for $DAY; manifest will record capture: ABSENT"
fi

# ---------------------------------------------------------------------------
# 4. Render the human-readable brief.
# ---------------------------------------------------------------------------
echo "== 4/5 render_brief $DAY =="
python3 "$SCRIPTS/render_brief.py" --root "$FLEET_ROOT" "$DAY"

# ---------------------------------------------------------------------------
# 5. Write the close manifest and the close-runs receipt (append-only).
# ---------------------------------------------------------------------------
echo "== 5/5 close_manifest $DAY =="
python3 "$SCRIPTS/close_manifest.py" --root "$FLEET_ROOT" "$DAY"

# ---------------------------------------------------------------------------
# 6. Print the derived commit command for Andy to run.
#    This script does NOT run git.
# ---------------------------------------------------------------------------
echo "== commit command for $DAY =="
python3 "$SCRIPTS/close_manifest.py" --root "$FLEET_ROOT" --commit-command "$DAY"

echo "close.sh: done for $DAY. Review the printed commands, then run them."
