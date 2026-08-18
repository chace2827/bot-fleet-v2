#!/usr/bin/env python3
"""Dangling-reference checker + propagator invariants.

Scans tracked Markdown, Python and shell sources for repo-relative paths and
reports the ones that do not exist on disk. The recurring defect this guards
against is a ruling that reached the document it was recorded in and no
further: a doc or a generator citing a file that was renamed, never created,
or lives only in the archive.

It also propagates two invariants:

  1. Ruling-ID freshness: a reference in a non-RULINGS source to a
     `Superseded` ruling is a stale citation and fails the build.
  2. bots_meta.csv row count: a Markdown doc that states a row/bot count for
     `data/bots_meta.csv` which differs from the CSV fails the build.

During the first week all other inconsistencies (dangling refs, Gated rulings,
etc.) are logged but do not fail. After the first week this can be switched to
--strict.
"""
import argparse
import csv
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOW_FILE = os.path.join(ROOT, "scripts", "check_refs_allow.txt")
HISTORY_INDEX = os.path.join(ROOT, "docs", "history-index.md")
RULINGS_FILE = os.path.join(ROOT, "docs", "RULINGS.md")
BOTS_META = os.path.join(ROOT, "data", "bots_meta.csv")

SCAN_EXTS = (".md", ".py", ".sh")
ROOTS = ("docs/", "scripts/", "data/")

# a path under a known root, ending in a real extension, so prose like
# "the docs/ folder" or "see data/" is not treated as a reference
REF = re.compile(r"(?<![\w./-])((?:docs|scripts|data)/[\w./ -]*?\.\w{1,5})(?![\w-])")
PLACEHOLDER = re.compile(r"YYYY|MM-DD|<[^>]+>|\{[^}]+\}|\bNAME\b|\*")

# Historical / frozen / append-only docs may legitimately carry old figures.
# The propagator still scans them for path references, but row-count claims
# in these files are not enforced as invariants.
ROW_COUNT_SKIP = {
    "session-log.md",
    "rules-catalog.md",
    "RULINGS.md",
    "history-index.md",
    "roster-mechanics-ruling.md",
    "build-plan.md",
}

WORD2NUM = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20,
}


def int_val(s):
    s = (s or "").strip().lower()
    if s in WORD2NUM:
        return WORD2NUM[s]
    s = s.replace(",", "")
    try:
        return int(s)
    except ValueError:
        return None


def tracked_files():
    out = subprocess.run(
        ["git", "-C", ROOT, "ls-files"], capture_output=True, text=True, check=True
    )
    return [p for p in out.stdout.splitlines() if p.endswith(SCAN_EXTS)]


def load_allow():
    allowed = {}
    if not os.path.exists(ALLOW_FILE):
        return allowed
    with open(ALLOW_FILE, encoding="utf-8") as fh:
        for line in fh:
            line = line.split("#", 1)[0].strip()
            if line:
                allowed[line] = True
    return allowed


def load_history_index():
    if not os.path.exists(HISTORY_INDEX):
        return ""
    with open(HISTORY_INDEX, encoding="utf-8") as fh:
        return fh.read()


def classify(ref, allowed, history):
    if PLACEHOLDER.search(ref):
        return "PLACEHOLDER"
    if ref in allowed:
        return "DECLARED"
    tail = ref.split("/", 1)[1]
    if os.path.exists(os.path.join(ROOT, "data", "archive", tail)):
        return "ARCHIVED"
    if os.path.basename(ref) in history:
        return "ARCHIVED"
    return "DANGLING"


def load_rulings():
    """Return {ruling_id: (status, superseded_by)} from docs/RULINGS.md."""
    if not os.path.exists(RULINGS_FILE):
        return {}
    text = open(RULINGS_FILE, encoding="utf-8").read()
    blocks = re.findall(r"```yaml(.*?)```", text, re.S)
    rulings = {}
    for block in blocks:
        rid = re.search(r"^ruling_id:\s*(.+)$", block, re.M)
        status = re.search(r"^status:\s*(.+)$", block, re.M)
        sup = re.search(r"^superseded_by:\s*(.+)$", block, re.M)
        if rid:
            rulings[rid.group(1).strip()] = (
                status.group(1).strip() if status else "Unknown",
                sup.group(1).strip()
                if sup and sup.group(1).strip().lower() != "none"
                else None,
            )
    return rulings


def build_ruling_pattern(rulings):
    if not rulings:
        return None
    # Sort by length descending so longer IDs match before shorter prefixes.
    ids = sorted(rulings.keys(), key=len, reverse=True)
    escaped = [re.escape(r) for r in ids]
    return re.compile(r"\b(?:" + "|".join(escaped) + r")\b")


def check_ruling_invariant(files, rulings, pattern):
    """Find any non-RULINGS source that references a Superseded ruling ID."""
    errors = []
    warnings = []
    if pattern is None:
        return errors, warnings
    for rel in files:
        if rel == "docs/RULINGS.md":
            continue
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as fh:
            for lineno, line in enumerate(fh, 1):
                for match in pattern.finditer(line):
                    rid = match.group(0)
                    status, sup = rulings.get(rid, ("Unknown", None))
                    if status == "Superseded":
                        msg = f"{rid} is Superseded"
                        if sup:
                            msg += f" (superseded_by {sup})"
                        errors.append((rel, lineno, rid, msg))
                    elif status == "Gated":
                        warnings.append((rel, lineno, rid, f"{rid} is Gated (not in force)"))
                    elif status == "Unknown":
                        warnings.append((rel, lineno, rid, f"{rid} is not a known ruling"))
    return errors, warnings


def load_bots_meta_count():
    if not os.path.exists(BOTS_META):
        return None
    with open(BOTS_META, encoding="utf-8") as f:
        return sum(1 for _ in csv.DictReader(f))


def check_row_count_invariant(files, actual_count):
    """Find any Markdown doc that states a row/bot count for bots_meta.csv that differs."""
    errors = []
    if actual_count is None:
        return errors
    pat = re.compile(
        r"\b(?:data/)?bots_meta\.csv\b"
        r".{0,60}?"
        r"(?<![\w-])(?:([0-9,]+)|(" + "|".join(WORD2NUM.keys()) + r"))\b"
        r"\s*(?:rows?|bots?|records?|entries)",
        re.I | re.S,
    )
    for rel in files:
        if not rel.endswith(".md") or os.path.basename(rel) in ROW_COUNT_SKIP or rel == "docs/RULINGS.md":
            continue
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as fh:
            for lineno, line in enumerate(fh, 1):
                for m in pat.finditer(line):
                    number = m.group(1) or m.group(2)
                    expected = int_val(number)
                    if expected is None:
                        continue
                    if expected != actual_count:
                        errors.append((
                            rel,
                            lineno,
                            f"says {number} rows/bots in bots_meta.csv; actual is {actual_count}",
                        ))
    return errors


# ---------------------------------------------------------------------------
# Regression fixtures for the row-count invariant.
#
# The first case is the verbatim text that was `docs/devin-queue.md:92` between
# 78b3195 and f602866. It reddened master push CI for two commits: `-` is a word
# boundary, so the old `\b`-anchored number group read the "1" out of "P1-1
# records" as a row count for bots_meta.csv. The `(?<![\w-])` lookbehind is what
# makes it a non-match. The true-positive cases below exist so that lookbehind
# cannot be widened into "the invariant never fires".
# ---------------------------------------------------------------------------
ROW_COUNT_CASES = [
    (
        "false positive: 'P1-1 records' is an item id, not a row count",
        "      but absent from `data/bots_meta.csv` is dropped with **no warning**"
        " \u2014 and P1-1 records that roster\n",
        44,
        False,
    ),
    (
        "true positive: a stale digit row count still fails",
        "The roster in `data/bots_meta.csv` has 43 rows.\n",
        44,
        True,
    ),
    (
        "true positive: a stale word row count still fails",
        "`data/bots_meta.csv` carries twelve bots.\n",
        44,
        True,
    ),
    (
        "true negative: the correct count passes",
        "`data/bots_meta.csv` has 44 rows.\n",
        44,
        False,
    ),
]


def selftest():
    """Exercise check_row_count_invariant against the fixtures above.

    Runs entirely inside a temp dir: this test must not be able to write the
    repo it is checking.
    """
    global ROOT
    original_root = ROOT
    failures = []
    try:
        for name, text, actual, expect_error in ROW_COUNT_CASES:
            with tempfile.TemporaryDirectory() as td:
                ROOT = td
                os.makedirs(os.path.join(td, "docs"))
                with open(os.path.join(td, "docs", "fixture.md"), "w", encoding="utf-8") as fh:
                    fh.write(text)
                errors = check_row_count_invariant(["docs/fixture.md"], actual)
            got_error = bool(errors)
            if got_error != expect_error:
                failures.append(
                    f"  {name}\n"
                    f"    expected {'an error' if expect_error else 'no error'}, "
                    f"got {errors if errors else 'no error'}"
                )
            else:
                print(f"  ok: {name}")
    finally:
        ROOT = original_root

    if failures:
        print("check_refs --selftest: FAIL", file=sys.stderr)
        for f in failures:
            print(f, file=sys.stderr)
        return 1
    print(f"check_refs --selftest: {len(ROW_COUNT_CASES)} row-count cases pass")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--all", action="store_true", help="print every classification")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 on dangling refs too (after the first week)",
    )
    ap.add_argument(
        "--selftest",
        action="store_true",
        help="run the row-count invariant regression fixtures and exit",
    )
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    allowed = load_allow()
    history = load_history_index()
    files = tracked_files()

    rulings = load_rulings()
    ruling_pat = build_ruling_pattern(rulings)

    # Path/dangling reference scan
    buckets = {k: [] for k in ("PLACEHOLDER", "ARCHIVED", "DECLARED", "DANGLING")}
    for rel in files:
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="replace") as fh:
            for lineno, line in enumerate(fh, 1):
                for ref in REF.findall(line):
                    ref = ref.strip()
                    if not ref.startswith(ROOTS):
                        continue
                    if os.path.exists(os.path.join(ROOT, ref)):
                        continue
                    buckets[classify(ref, allowed, history)].append((rel, lineno, ref))

    if args.all:
        for kind in ("PLACEHOLDER", "ARCHIVED", "DECLARED"):
            print(f"{kind}: {len(buckets[kind])}")
            for rel, lineno, ref in buckets[kind]:
                print(f"  {rel}:{lineno}  ->  {ref}")

    bots_meta_count = load_bots_meta_count()
    ruling_errors, ruling_warnings = check_ruling_invariant(files, rulings, ruling_pat)
    row_errors = check_row_count_invariant(files, bots_meta_count)

    # First-week warnings: anything that is not one of the two invariants.
    dangling = buckets["DANGLING"]
    if ruling_warnings:
        print(f"check_refs: {len(ruling_warnings)} RULING WARNING(S)")
        for rel, lineno, rid, msg in ruling_warnings:
            print(f"  {rel}:{lineno}  {rid}  ->  {msg}")
    if dangling:
        print(f"check_refs: {len(dangling)} DANGLING REFERENCE(S)")
        for rel, lineno, ref in dangling:
            print(f"  {rel}:{lineno}  ->  {ref}")

    # Enforced invariants
    failed = False
    if ruling_errors:
        failed = True
        print(f"check_refs: {len(ruling_errors)} STALE RULING REFERENCE(S)")
        for rel, lineno, rid, msg in ruling_errors:
            print(f"  {rel}:{lineno}  {rid}  ->  {msg}")

    if row_errors:
        failed = True
        print(f"check_refs: {len(row_errors)} BOTS_META ROW-COUNT CONTRADICTION(S)")
        for rel, lineno, msg in row_errors:
            print(f"  {rel}:{lineno}  ->  {msg}")

    if args.strict and dangling:
        failed = True

    if not failed:
        print("check_refs: invariants clean")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
