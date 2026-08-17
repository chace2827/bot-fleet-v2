#!/usr/bin/env bash
# Fleet Brief — one-command daily pipeline.
#
# Runs eight stages IN ORDER (order matters). Stage order follows CLAUDE.md §2:
# ledger -> tape -> DRIFT AUDIT -> three-verdict brief -> accumulators -> report.
#
#   1. build_ledger.py     — rebuild the POST-CUTOVER working ledger (data/trades.csv +
#                            bots.csv + straddlers.csv + ledger_meta.json) from the newest
#                            OA export. REFUSES to run without LEDGER_START.
#   2. tape.py             — day's OHLC + regime read  -> data/brief/<date>_tape.json
#   3. execution_audit.py  — the DRIFT / EXECUTION DETECTOR. Structural rules always;
#                            declared-config rules only with data/bots_config_v2.csv,
#                            otherwise reported SKIPPED (never a silent pass)
#                            -> data/execution_audit_findings.csv
#   4. daily_brief.py      — config-vs-actual cards, breach flags, hedge counterfactual,
#                            compliance scoring -> data/brief/<date>_brief.json + compliance.csv
#   5. hedge_tournament.py — Free Hedge Tournament: replays that day's settled legs through
#                            the v1 hedge library (Ride/PT/SL/S2/Defang-deferred), R-scored
#                            -> upserts data/hedge_tournament.csv (per-date, idempotent)
#   6. trade_window.py     — Trade-window heat map: buckets every position's MAE timestamp
#                            by hour x tape-regime + a tape-covered short-strike touch rate
#                            -> rebuilds data/trade_window.csv (full rebuild, idempotent)
#   7. lessons.py          — Lessons index: tags each graded bot-day's brief "day's lesson"
#                            (entry-timing/hedge/filter/regime/sizing/other)
#                            -> upserts data/lessons.csv (per date+bot, idempotent)
#   8. report.py           — STATUS.md + dashboard.html (G5 reads compliance.csv; Hedge
#                            tournament / Trade-window heat map / Lessons index sections read
#                            hedge_tournament.csv / trade_window.csv / lessons.csv — all must
#                            be fresh before this step)
#
# The brief JSON is the pack Claude renders (charts + instruction-mirror cards +
# hedge clinic). Everything numeric is regenerated from the ledger.
#
# Then, from the EXIT trap and outside the eight stages: the heartbeat, and a
# per-run RECEIPT appended to data/receipts/daily-runs.jsonl (G-5,
# ledger-truncation-forensics-2026-08-17.md §4). Both are written whether the run
# succeeded, failed or was refused. ledger_meta.json is overwritten every run and
# so records only the last one; the receipts file is append-only and records all
# of them, which is what makes "what changed between these two runs" answerable
# at all. See scripts/run_receipt.py.
#
# LEDGER_START — the data cutover (build-plan.md §3). Set it in build_ledger.py on
# Day-0, or override per-run:   LEDGER_START=2026-08-17 scripts/daily.sh
# With it unset, stage 1 exits non-zero and the whole run stops. That is correct:
# a ledger with no cutover is a contaminated ledger.
#
# Usage:
#   scripts/daily.sh                 # newest export / newest ledger date
#   scripts/daily.sh 2026-08-18      # a specific trading day (for backfill)
#   FLEET_ROOT=/tmp/scratch scripts/daily.sh 2026-08-10   # never touches data/
#
# Prereq: drop the OA positions CSV in data/raw/ named YYYY-MM-DD.csv first.
# Tape uses Tradier when TRADIER_TOKEN is set (env or ./.env); otherwise it
# reconstructs from the ledger and says so.
#
# TAPE_FIXTURE mode (CI / hermetic runs): set TAPE_FIXTURE=1 and the script will
# use the committed data/brief/<date>_tape.json instead of calling any live API.
#
# FLEET_ROOT — the OUTPUT ROOT (G-3, ledger-truncation-forensics-2026-08-17.md §7).
# Unset, it is the repo, and this is the live daily loop. Set to a directory
# outside the repo, the ENTIRE eight-stage pipeline reads and writes THAT tree
# and the repo's data/ is not touched at all:
#
#   FLEET_ROOT=/tmp/fleet-scratch scripts/daily.sh 2026-08-10
#
# This is the isolation that did not exist on 2026-08-12. TAPE_FIXTURE=1 fenced
# the tape stage off from the network, but nothing fenced the ledger stage off
# from the ledger, so `scripts/daily.sh 2026-08-10` — the command used to PROVE
# CI determinism — rebuilt the fleet's real data/trades.csv from a stale fixture
# and deleted 2026-08-11 from it. A determinism proof must not be able to write
# the thing it is measuring.
#
# The mechanism: every script here resolves its paths from its own location
# (ROOT = dirname(dirname(__file__))), so running the stages out of
# $FLEET_ROOT/scripts repoints all of them at once. The root is materialised by
# scripts/ci/seed_scratch_root.sh, called below when it is missing.
#
# n=0: every stage degrades gracefully on an empty post-cutover ledger. Verified
# 2026-07-30 by the Phase-3 dry run. An empty stage says so; none of them crash,
# and none of them render an absent number as a zero.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "${FLEET_ROOT:-$REPO}"
FLEET_ROOT="$(cd "${FLEET_ROOT:-$REPO}" && pwd)"
export FLEET_ROOT

if [ "$FLEET_ROOT" != "$REPO" ]; then
  "$REPO/scripts/ci/seed_scratch_root.sh" "$FLEET_ROOT"
  echo "=================================================================="
  echo " SCRATCH RUN — output root is $FLEET_ROOT"
  echo " The live ledger at $REPO/data is NOT being written."
  echo "=================================================================="
fi

# Stages are invoked out of the ROOT's own scripts/ dir; that is what makes each
# one resolve data/ to this root rather than the repo. cd for the few relative
# paths (heartbeat dir) that are still cwd-based.
SCRIPTS="$FLEET_ROOT/scripts"
cd "$FLEET_ROOT"

DAY="${1:-}"
ALLOW_REWIND=""
if [ "${2:-}" = "--allow-rewind" ]; then
  ALLOW_REWIND="--allow-rewind"
fi

# G-5 — read by scripts/run_receipt.py from the exit trap below.
# FLEET_RUN_STARTED is what lets a receipt tell "the ledger stage rewrote
# ledger_meta.json" from "the ledger stage refused and this is last run's file";
# FLEET_PINNED_DAY records whether an export was PINNED, which is the thing that
# caused the 2026-08-12 truncation in the first place.
export FLEET_RUN_STARTED="$(date +%s)"
export FLEET_PINNED_DAY="${1:-}"
# FLEET_REPO cannot be derived inside run_receipt.py: under G-3 the stages run
# out of a COPY of scripts/ in the scratch root, so that file's own location is
# the ROOT, and every scratch run would label itself live.
export FLEET_REPO="$REPO"

# If no day was supplied, use the newest raw export filename; otherwise fall
# back to today. Resolving here gives every stage a concrete DAY and lets the
# heartbeat file be named after the actual trading day processed.
if [ -z "$DAY" ]; then
  DAY="$(python3 - <<'PY'
import glob, os, datetime
files = sorted(glob.glob('data/raw/*.csv'))
if files:
    print(os.path.basename(files[-1])[:-4])
else:
    print(datetime.date.today().isoformat())
PY
  )"
fi

# Make timestamps deterministic for a given DAY so two runs are byte-identical.
if [ -n "$DAY" ] && [ -z "${SOURCE_DATE_EPOCH:-}" ]; then
  export SOURCE_DATE_EPOCH="$(python3 - <<PY
import datetime
d = "$DAY"
print(int(datetime.datetime(int(d[:4]), int(d[5:7]), int(d[8:10]),
                            tzinfo=datetime.timezone.utc).timestamp()))
PY
  )"
fi
export TAPE_FIXTURE=${TAPE_FIXTURE:-}
export PYTHONDONTWRITEBYTECODE=1

HEARTBEAT_DIR="artifacts/heartbeat"
TOTAL_STAGES=8

declare -a STAGES=()
declare -a CODES=()
HEARTBEAT_WRITTEN=""

write_heartbeat() {
  [ -n "$HEARTBEAT_WRITTEN" ] && return
  HEARTBEAT_WRITTEN=1
  local hb_exit
  if [ ${#CODES[@]} -gt 0 ]; then
    hb_exit=${CODES[$((${#CODES[@]}-1))]}
  else
    hb_exit=0
  fi
  mkdir -p "$HEARTBEAT_DIR"
  local i
  for i in "${!STAGES[@]}"; do
    export "HB_NAME_$i=${STAGES[$i]}"
    export "HB_CODE_$i=${CODES[$i]}"
  done
  export HB_DAY="$DAY"
  export HB_FINAL_EXIT="$hb_exit"
  python3 "$SCRIPTS/heartbeat.py"
  # G-5 — the per-run receipt. Written HERE, from the exit trap, so a run that
  # failed or was refused leaves a trace too; those are the runs most worth
  # having a record of. Never allowed to change the run's own exit code: a
  # receipt that breaks the pipeline is worse than no receipt.
  python3 "$SCRIPTS/run_receipt.py" \
    || echo "run_receipt.py: FAILED to append a receipt (run itself unaffected)" >&2
}

trap 'write_heartbeat' EXIT

run_stage() {
  local name=$1; shift
  local rc
  local n=$(( ${#STAGES[@]} + 1 ))
  echo "== $n/$TOTAL_STAGES $name $DAY =="
  if "$@"; then
    rc=0
  else
    rc=$?
  fi
  STAGES+=("$name")
  CODES+=("$rc")
  if [ $rc -ne 0 ]; then
    write_heartbeat
    exit $rc
  fi
}

run_stage "build_ledger" python3 "$SCRIPTS/build_ledger.py" --root "$FLEET_ROOT" "$DAY" $ALLOW_REWIND
run_stage "tape" python3 "$SCRIPTS/tape.py" "$DAY"
run_stage "execution_audit" python3 "$SCRIPTS/execution_audit.py"
run_stage "daily_brief" python3 "$SCRIPTS/daily_brief.py" "$DAY"
run_stage "hedge_tournament" python3 "$SCRIPTS/hedge_tournament.py" "$DAY"
run_stage "trade_window" python3 "$SCRIPTS/trade_window.py"
run_stage "lessons" python3 "$SCRIPTS/lessons.py"
run_stage "report" python3 "$SCRIPTS/report.py"

echo "== done -> STATUS.md, dashboard.html, data/brief/${DAY}_brief.json,"
echo "           data/execution_audit_findings.csv =="

# Missing/empty stand-alone research / audit tools are intentionally NOT wired
# into the daily loop (their own docstrings forbid it).  List them so they do
# not silently appear to be passing in CI.
echo "== SKIPPED (not wired to daily loop) =="
for s in research_loop comparative_machinery a_series intraday_read; do
  echo "  $s: SKIPPED — standalone tooling, see scripts/$s.py"
done
