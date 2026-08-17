#!/usr/bin/env python3
"""Write the daily heartbeat artifact.

daily.sh sets the environment variables:
  HB_DAY           the trading day (YYYY-MM-DD)
  HB_NAME_0..N     stage names
  HB_CODE_0..N     the exit code for each stage
  HB_FINAL_EXIT    the final daily run exit code

This script is intentionally simple and is not imported by any other script,
so the checker failure domain stays separate from the producer.
"""
import json
import os
import sys
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEARTBEAT_DIR = os.path.join(ROOT, "artifacts", "heartbeat")


def now_iso():
    """Reproducible 'generated' timestamp. SOURCE_DATE_EPOCH wins over wall clock."""
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        return datetime.datetime.fromtimestamp(
            int(epoch), tz=datetime.timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds")
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds")


def load_stages():
    stages = []
    i = 0
    while True:
        name = os.environ.get(f"HB_NAME_{i}")
        code = os.environ.get(f"HB_CODE_{i}")
        if name is None or code is None:
            break
        try:
            code = int(code)
        except ValueError:
            code = -1
        stages.append({"name": name, "exit_code": code})
        i += 1
    return stages


def main():
    day = os.environ.get("HB_DAY")
    if not day and len(sys.argv) > 1:
        day = sys.argv[1]
    if not day:
        day = datetime.date.today().isoformat()

    final_exit = 0
    if os.environ.get("HB_FINAL_EXIT"):
        try:
            final_exit = int(os.environ["HB_FINAL_EXIT"])
        except ValueError:
            final_exit = -1

    out = {
        "date": day,
        "generated": now_iso(),
        "stages": load_stages(),
        "final_exit_code": final_exit,
    }

    os.makedirs(HEARTBEAT_DIR, exist_ok=True)
    path = os.path.join(HEARTBEAT_DIR, f"{day}.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)

    print(f"heartbeat.py: wrote {os.path.relpath(path, ROOT)}")


if __name__ == "__main__":
    main()
