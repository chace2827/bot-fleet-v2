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
# LEDGER_START — the data cutover (build-plan.md §3). Set it in build_ledger.py on
# Day-0, or override per-run:   LEDGER_START=2026-08-17 scripts/daily.sh
# With it unset, stage 1 exits non-zero and the whole run stops. That is correct:
# a ledger with no cutover is a contaminated ledger.
#
# Usage:
#   scripts/daily.sh                 # newest export / newest ledger date
#   scripts/daily.sh 2026-08-18      # a specific trading day (for backfill)
#
# Prereq: drop the OA positions CSV in data/raw/ named YYYY-MM-DD.csv first.
# Tape uses Tradier when TRADIER_TOKEN is set (env or ./.env); otherwise it
# reconstructs from the ledger and says so.
#
# TAPE_FIXTURE mode (CI / hermetic runs): set TAPE_FIXTURE=1 and the script will
# use the committed data/brief/<date>_tape.json instead of calling any live API.
#
# n=0: every stage degrades gracefully on an empty post-cutover ledger. Verified
# 2026-07-30 by the Phase-3 dry run. An empty stage says so; none of them crash,
# and none of them render an absent number as a zero.
set -euo pipefail
cd "$(dirname "$0")/.."

DAY="${1:-}"

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
  python3 scripts/heartbeat.py
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

run_stage "build_ledger" python3 scripts/build_ledger.py "$DAY"
run_stage "tape" python3 scripts/tape.py "$DAY"
run_stage "execution_audit" python3 scripts/execution_audit.py
run_stage "daily_brief" python3 scripts/daily_brief.py "$DAY"
run_stage "hedge_tournament" python3 scripts/hedge_tournament.py "$DAY"
run_stage "trade_window" python3 scripts/trade_window.py
run_stage "lessons" python3 scripts/lessons.py
run_stage "report" python3 scripts/report.py

echo "== done -> STATUS.md, dashboard.html, data/brief/${DAY}_brief.json,"
echo "           data/execution_audit_findings.csv =="

# Missing/empty stand-alone research / audit tools are intentionally NOT wired
# into the daily loop (their own docstrings forbid it).  List them so they do
# not silently appear to be passing in CI.
echo "== SKIPPED (not wired to daily loop) =="
for s in research_loop comparative_machinery a_series intraday_read; do
  echo "  $s: SKIPPED — standalone tooling, see scripts/$s.py"
done
