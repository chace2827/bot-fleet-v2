#!/usr/bin/env python3
"""Dangling-reference checker.

Scans tracked Markdown, Python and shell sources for repo-relative paths and
reports the ones that do not exist on disk. The recurring defect this guards
against is a ruling that reached the document it was recorded in and no
further: a doc or a generator citing a file that was renamed, never created,
or lives only in the archive.

Not every missing path is a defect, so each one is classified:

  PLACEHOLDER  a template path (data/raw/YYYY-MM-DD.csv) — not a claim
  ARCHIVED     resolves under data/archive/, or the filename is indexed in
               docs/history-index.md — cited as history, by convention
  DECLARED     listed in scripts/check_refs_allow.txt: an output a script
               writes at runtime, or a deliverable a spec has not built yet
  DANGLING     none of the above — a citation with nothing behind it

Exit status is 1 when a DANGLING reference is found, so this can gate a merge.
Pass --all to print every classification, not just the failures.
"""
import argparse
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOW_FILE = os.path.join(ROOT, "scripts", "check_refs_allow.txt")
HISTORY_INDEX = os.path.join(ROOT, "docs", "history-index.md")
SCAN_EXTS = (".md", ".py", ".sh")
ROOTS = ("docs/", "scripts/", "data/")
# a path under a known root, ending in a real extension, so prose like
# "the docs/ folder" or "see data/" is not treated as a reference
REF = re.compile(r"(?<![\w./-])((?:docs|scripts|data)/[\w./ -]*?\.\w{1,5})(?![\w-])")
PLACEHOLDER = re.compile(r"YYYY|MM-DD|<[^>]+>|\{[^}]+\}|\bNAME\b|\*")


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


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--all", action="store_true", help="print every classification")
    args = ap.parse_args()

    allowed = load_allow()
    history = load_history_index()
    buckets = {k: [] for k in ("PLACEHOLDER", "ARCHIVED", "DECLARED", "DANGLING")}

    for rel in tracked_files():
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

    dangling = buckets["DANGLING"]
    if not dangling:
        print(
            "check_refs: NO FINDINGS "
            f"(placeholder {len(buckets['PLACEHOLDER'])}, "
            f"archived {len(buckets['ARCHIVED'])}, "
            f"declared {len(buckets['DECLARED'])})"
        )
        return 0

    print(f"check_refs: {len(dangling)} DANGLING REFERENCE(S)")
    for rel, lineno, ref in dangling:
        print(f"  {rel}:{lineno}  ->  {ref}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
