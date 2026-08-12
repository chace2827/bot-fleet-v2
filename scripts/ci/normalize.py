#!/usr/bin/env python3
"""Strip the volatile fields from a generated artifact so two runs can be compared.

The pipeline stamps wall-clock time into everything it writes, so a byte diff of a
rerun is always non-empty and therefore always useless. This removes exactly the
fields that are *expected* to differ between two runs of the same inputs — and
nothing else. Anything still different afterwards is a reproducibility defect.

Deliberately narrow: each pattern is anchored to a `generated` key or a
`generated <date>` caption. A pattern that blanked bare dates would also blank
`open_date` and hide the very drift this exists to catch.

Usage:  normalize.py <path>        # normalized text to stdout
        normalize.py --stdin       # normalized text from stdin
"""
import re
import sys

NORM = "<NORMALIZED>"

PATTERNS = [
    # JSON:  "generated": "2026-08-12T01:19:53"
    (re.compile(r'("generated"\s*:\s*)"[^"]*"'), r'\1"' + NORM + '"'),
    # Markdown / HTML caption:  generated 2026-08-12
    (re.compile(r"(generated\s+)\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2})?)?"),
     r"\1" + NORM),
]


def normalize(text: str) -> str:
    for pat, repl in PATTERNS:
        text = pat.sub(repl, text)
    return text


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__, file=sys.stderr)
        return 2
    if args[0] == "--stdin":
        sys.stdout.write(normalize(sys.stdin.read()))
        return 0
    with open(args[0], encoding="utf-8", errors="replace") as fh:
        sys.stdout.write(normalize(fh.read()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
