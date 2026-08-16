#!/usr/bin/env python3
"""Run every --validate suite and compare the result to a committed baseline.

Why a baseline instead of "all four must exit 0": comparative_machinery is at 35/36
today (R-1 reads live ledger metadata rather than a fixture, so it stopped exercising
the sentinel path when the ledger went live). Making that green by editing the test
would be the wrong fix, and skipping the suite would drop 35 real assertions. So the
current state is recorded, and CI fails on any *movement* from it — a regression and
a silent improvement both demand that someone look.

When a change is intended, update scripts/ci/validate_baseline.txt in the same PR.
The diff then shows the assertion count moving, which is the point.

Exit 0 = matches baseline.  Exit 1 = moved.
"""
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BASELINE = Path(__file__).resolve().parent / "validate_baseline.txt"

SUITES = ["execution_audit", "a_series", "research_loop", "comparative_machinery"]
COUNT = re.compile(r"\b(\d+)/(\d+) passed\b")


def run(suite: str) -> str:
    proc = subprocess.run(
        ["python3", f"scripts/{suite}.py", "--validate"],
        cwd=REPO, capture_output=True, text=True,
    )
    hits = COUNT.findall(proc.stdout)
    count = "/".join(hits[-1]) if hits else "-"
    return f"{suite} exit={proc.returncode} {count}", proc.stdout, proc.stderr


def main() -> int:
    lines, failed = [], False
    for suite in SUITES:
        summary, out, err = run(suite)
        lines.append(summary)
        print(f"== {suite} ==")
        print(out.rstrip() or err.rstrip())
        print()

    actual = "\n".join(lines) + "\n"
    if not BASELINE.exists():
        BASELINE.write_text(actual)
        print(f"wrote new baseline:\n{actual}")
        return 0

    expected = BASELINE.read_text()
    print("== baseline check ==")
    for exp, act in zip(expected.splitlines(), actual.splitlines()):
        mark = "ok  " if exp == act else "MOVED"
        if exp != act:
            failed = True
            print(f"  {mark}  expected: {exp}")
            print(f"         actual:   {act}")
        else:
            print(f"  {mark}  {act}")

    if failed:
        print("\nFAIL: a validation suite moved. If intended, update "
              "scripts/ci/validate_baseline.txt in this PR.")
        return 1
    print("\nPASS: all suites match baseline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
