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
# With no day argument, the close day is derived from the export itself — its
# max openDate, i.e. the last day it has positions for. Right for an
# after-close export (today) and a next-morning one (yesterday) alike.
#
# Capture handling:
#   - If CAPTURE_TXT is set, it is used as the raw /bots capture .txt, and
#     CAPTURE_SCREENSHOTS (colon-separated) are passed as screenshots.
#   - Otherwise, close.sh looks for raw capture files in
#     $CAPTURE_INBOX/<day>/ (default data/captures/<day>/):
#     exactly one .txt and any .png/.jpg/.jpeg/.pdf in the same directory.
#   - Otherwise, the newest oa_*.txt carrying a `captured:` header in the
#     downloads dir ($INGEST_DOWNLOADS or ~/Downloads) is used — the OA Grab
#     bookmarklet lands there. One dated before the close day is stale and
#     ignored with a warning.
#   - If no raw capture is found, the manifest records capture: ABSENT.
#   - capture_bundle.py names the bundle by the CAPTURE's own `captured:`
#     date, which differs from the close day on a catch-up close.  The dir
#     it actually writes is parsed from its output and passed to
#     close_manifest.py --capture-dir, so the manifest records PRESENT for
#     the bundle this run produced rather than looking for <day>-roster.
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

INGEST_ARGS=()
if [ -n "${INGEST_DOWNLOADS:-}" ]; then
  INGEST_ARGS+=("--downloads" "$INGEST_DOWNLOADS")
fi

DAY="${1:-}"
if [ -z "$DAY" ]; then
  # Derive the close day from the export: its max openDate is the last day it
  # has positions for. --dry-run runs every check and prints every derivation
  # while writing nothing.
  echo "== deriving close day from the export =="
  PROBE_RC=0
  if [ ${#INGEST_ARGS[@]} -gt 0 ]; then
    PROBE_OUT="$(python3 "$SCRIPTS/ingest_export.py" --root "$FLEET_ROOT" --dry-run "${INGEST_ARGS[@]}")" || PROBE_RC=$?
  else
    PROBE_OUT="$(python3 "$SCRIPTS/ingest_export.py" --root "$FLEET_ROOT" --dry-run)" || PROBE_RC=$?
  fi
  if [ $PROBE_RC -ne 0 ]; then
    [ -n "$PROBE_OUT" ] && printf '%s\n' "$PROBE_OUT" >&2
    echo "close.sh: FATAL: could not derive the close day from an export in ${INGEST_DOWNLOADS:-~/Downloads}." >&2
    echo "  Pass the day explicitly: scripts/close.sh YYYY-MM-DD" >&2
    exit 2
  fi
  printf '%s\n' "$PROBE_OUT"
  DAY="$(printf '%s\n' "$PROBE_OUT" | sed -n 's/^max openDate: //p')"
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

# Neither CAPTURE_TXT nor the inbox produced a capture: look next to the
# export. The OA Grab bookmarklet downloads oa_*.txt to the same directory.
# A capture whose own `captured:` date precedes the close day is stale —
# ignored with a warning rather than bundled under the wrong day.
if [ -z "$CAPTURE_TXT" ]; then
  CAPTURE_DL="${INGEST_DOWNLOADS:-$HOME/Downloads}"
  DISC="$(python3 - "$CAPTURE_DL" <<'PY'
import datetime, glob, os, re, sys
d = os.path.expanduser(sys.argv[1])
cap_re = re.compile(r"^captured:\s*(.+?)\s*$")
best = None
for p in glob.glob(os.path.join(d, "oa_*.txt")):
    try:
        with open(p, encoding="utf-8", errors="replace") as fo:
            head = fo.read(8192)
    except OSError:
        continue
    cday = None
    for line in head.splitlines():
        m = cap_re.match(line)
        if m:
            try:
                cday = datetime.datetime.strptime(
                    m.group(1).split(" (")[0].strip(),
                    "%a %b %d %Y %H:%M:%S GMT%z").strftime("%Y-%m-%d")
            except ValueError:
                cday = None
            break
    if cday is None:
        continue
    mt = os.path.getmtime(p)
    if best is None or mt > best[0]:
        best = (mt, cday, p)
if best is not None:
    print(best[1] + "\t" + best[2])
PY
)"
  if [ -n "$DISC" ]; then
    CAP_DAY="${DISC%%$'\t'*}"
    CAP_PATH="${DISC#*$'\t'}"
    if [[ "$CAP_DAY" < "$DAY" ]]; then
      echo "close.sh: WARNING: newest capture in $CAPTURE_DL is dated $CAP_DAY, before close day $DAY; ignoring it as stale" >&2
    else
      CAPTURE_TXT="$CAP_PATH"
      echo "close.sh: capture auto-discovered: $CAP_PATH (captured $CAP_DAY)"
    fi
  fi
fi

echo "== 3/5 capture_bundle $DAY =="
CAPTURE_DIR=""
if [ -n "$CAPTURE_TXT" ]; then
  if [ ${#CAPTURE_SCREENSHOTS[@]} -gt 0 ]; then
    BUNDLE_OUT="$(python3 "$SCRIPTS/capture_bundle.py" --out-root "$FLEET_ROOT/data/captures" \
      "$CAPTURE_TXT" "${CAPTURE_SCREENSHOTS[@]}")"
  else
    BUNDLE_OUT="$(python3 "$SCRIPTS/capture_bundle.py" --out-root "$FLEET_ROOT/data/captures" \
      "$CAPTURE_TXT")"
  fi
  echo "$BUNDLE_OUT"
  # The bundle is named by the capture's own `captured:` date; parse the dir
  # capture_bundle.py reports so a catch-up close records capture: PRESENT.
  CAPTURE_DIR="$(printf '%s\n' "$BUNDLE_OUT" | sed -n 's/^capture_bundle\.py: wrote //p')"
  if [ -z "$CAPTURE_DIR" ]; then
    echo "close.sh: FATAL: cannot parse the bundle dir from capture_bundle.py output" >&2
    exit 1
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
if [ -n "$CAPTURE_DIR" ]; then
  python3 "$SCRIPTS/close_manifest.py" --root "$FLEET_ROOT" "$DAY" --capture-dir "$CAPTURE_DIR"
else
  python3 "$SCRIPTS/close_manifest.py" --root "$FLEET_ROOT" "$DAY"
fi

# ---------------------------------------------------------------------------
# 6. Print the derived commit command for Andy to run.
#    This script does NOT run git.
# ---------------------------------------------------------------------------
echo "== commit command for $DAY =="
python3 "$SCRIPTS/close_manifest.py" --root "$FLEET_ROOT" --commit-command "$DAY"

echo "close.sh: done for $DAY."
echo "== remaining manual steps =="
echo "  1. Write the narrative:  data/brief/${DAY}_narrative.md   (six ## slots; judgment, not generated)"
echo "  2. Re-render the brief:  python3 scripts/render_brief.py $DAY"
echo "  3. Commit:               the command printed above (Andy runs it)"
