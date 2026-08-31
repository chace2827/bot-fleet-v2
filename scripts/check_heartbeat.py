#!/usr/bin/env python3
"""Independent heartbeat checker.

Runs on a schedule before market open and fails loudly if the previous
trading day's heartbeat is missing or red. It does not import or call any
daily-loop stage, so a failure in the producer cannot silently hide here.
"""
import argparse
import datetime
import json
import os
import sys

import market_calendar as mcal

ROOT = os.environ.get("FLEET_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEARTBEAT_DIR = os.path.join(ROOT, "artifacts", "heartbeat")


def check(day):
    prev = mcal.previous_trading_day(day)
    path = os.path.join(HEARTBEAT_DIR, f"{prev}.json")

    if not os.path.exists(path):
        print(f"check_heartbeat.py: RED — no heartbeat for previous trading day {prev}",
              file=sys.stderr)
        return 1

    try:
        with open(path) as f:
            hb = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"check_heartbeat.py: RED — heartbeat for {prev} is unreadable: {e}",
              file=sys.stderr)
        return 1

    if hb.get("date") != prev:
        print(f"check_heartbeat.py: RED — heartbeat date mismatch "
              f"(file says {hb.get('date')}, expected {prev})",
              file=sys.stderr)
        return 1

    if hb.get("final_exit_code", -1) != 0:
        print(f"check_heartbeat.py: RED — heartbeat for {prev} shows "
              f"final_exit_code={hb.get('final_exit_code')}",
              file=sys.stderr)
        return 1

    for stage in hb.get("stages", []):
        if stage.get("exit_code", 0) != 0:
            print(f"check_heartbeat.py: RED — stage {stage.get('name')} "
                  f"for {prev} exited {stage.get('exit_code')}",
                  file=sys.stderr)
            return 1

    print(f"check_heartbeat.py: GREEN — heartbeat OK for {prev} "
          f"({len(hb.get('stages', []))} stages)")
    return 0


def selftest():
    """Create a heartbeat, check the next day, delete it, and confirm the check fails."""
    day = "2026-08-11"
    prev = mcal.previous_trading_day(day)
    path = os.path.join(HEARTBEAT_DIR, f"{prev}.json")
    os.makedirs(HEARTBEAT_DIR, exist_ok=True)

    hb = {
        "date": prev,
        "generated": "2026-08-10T17:30:00",
        "stages": [
            {"name": "build_ledger", "exit_code": 0},
            {"name": "tape", "exit_code": 0},
        ],
        "final_exit_code": 0,
    }
    with open(path, "w") as f:
        json.dump(hb, f, indent=2)

    rc = check(day)
    if rc != 0:
        print("check_heartbeat.py: SELFTEST FAIL — expected pass with heartbeat", file=sys.stderr)
        return 1

    os.remove(path)
    rc = check(day)
    if rc == 0:
        print("check_heartbeat.py: SELFTEST FAIL — expected fail without heartbeat", file=sys.stderr)
        return 1

    print("check_heartbeat.py: selftest OK")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true",
                    help="run the deletion-rejection selftest")
    ap.add_argument("--date", default=None,
                    help="date to check from (YYYY-MM-DD; defaults to today)")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    day = args.date or datetime.date.today().isoformat()
    sys.exit(check(day))


if __name__ == "__main__":
    main()
