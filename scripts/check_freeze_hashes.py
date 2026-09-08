#!/usr/bin/env python3
"""Freeze predicate: recompute sha256 of the fixed panel and compare to docs.

The panel is declared in the authoritative docs. A mismatch means a frozen file
moved without the docs being re-recorded, which breaks comparability of every
banked day. This is the CI check named by the §2.4 version-bump procedure.
"""
import argparse
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCRIPTS = {
    "scripts/execution_audit.py": os.path.join(ROOT, "scripts", "execution_audit.py"),
    "scripts/build_ledger.py": os.path.join(ROOT, "scripts", "build_ledger.py"),
}

DOCS = [
    os.path.join(ROOT, "docs", "daily-loop-spec.md"),
    os.path.join(ROOT, "docs", "roster-mechanics-ruling.md"),
]

SHA_RE = re.compile(r"[0-9a-f]{64}")
SCRIPT_RE = re.compile(r"(scripts/(?:execution_audit|build_ledger)\.py)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fo:
        for chunk in iter(lambda: fo.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def in_lineage(section_titles):
    """Skip the LINEAGE TRACE section and its subsections."""
    return any("lineage trace" in t.lower() for t in section_titles)


def recorded_hashes():
    """Return {script_path: set(recorded_hashes)} from the authoritative docs."""
    recorded = {s: set() for s in SCRIPTS}

    for doc in DOCS:
        with open(doc, "r", encoding="utf-8") as fo:
            lines = fo.readlines()

        sections = []  # stack of (level, title)

        for line in lines:
            m = HEADING_RE.match(line)
            if m:
                level = len(m.group(1))
                title = m.group(2).strip()
                while sections and sections[-1][0] >= level:
                    sections.pop()
                sections.append((level, title))
                continue

            if in_lineage([t for _, t in sections]):
                continue

            if "frozen" not in line.lower():
                continue

            # Find script names and hashes in the order they appear on the line.
            tokens = []
            for m in SCRIPT_RE.finditer(line):
                tokens.append((m.start(), m.group(1)))
            for m in SHA_RE.finditer(line):
                tokens.append((m.start(), m.group(0)))
            tokens.sort(key=lambda x: x[0])

            current = None
            for _, tok in tokens:
                if tok.startswith("scripts/"):
                    current = tok
                elif current and len(tok) == 64:
                    recorded[current].add(tok)

    return recorded


def run():
    """Recompute hashes and compare to the docs. Return 0 if green."""
    recorded = recorded_hashes()
    actual = {s: sha256_file(p) for s, p in SCRIPTS.items()}

    fails = 0
    for script in sorted(SCRIPTS):
        decls = recorded.get(script, set())
        if not decls:
            print(f"FREEZE FAIL: no recorded hash found for {script}", file=sys.stderr)
            fails += 1
            continue
        if len(decls) > 1:
            print(f"FREEZE FAIL: {script} has inconsistent recorded hashes: {sorted(decls)}",
                  file=sys.stderr)
            fails += 1
            continue
        declared = decls.pop()
        got = actual[script]
        if declared != got:
            print(f"FREEZE FAIL: {script}", file=sys.stderr)
            print(f"  declared in docs: {declared}", file=sys.stderr)
            print(f"  actual sha256:    {got}", file=sys.stderr)
            fails += 1
        else:
            print(f"FREEZE OK: {script} == {got}")

    return 1 if fails else 0


def selftest():
    """Red/green test of the parser: build a scratch repo with a known mismatch."""
    import shutil
    import tempfile

    tmp = tempfile.mkdtemp(prefix="freeze-selftest-")
    try:
        # Write two tiny scripts.
        for name, body in (("execution_audit.py", b"# v1.0.0\n"),
                           ("build_ledger.py", b"# ledger\n")):
            with open(os.path.join(tmp, name), "wb") as fo:
                fo.write(body)

        # Write a doc that declares both frozen at the correct hashes.
        h_exec = sha256_file(os.path.join(tmp, "execution_audit.py"))
        h_ledger = sha256_file(os.path.join(tmp, "build_ledger.py"))

        doc = os.path.join(tmp, "roster-mechanics-ruling.md")
        with open(doc, "w", encoding="utf-8") as fo:
            fo.write("## 0. SIGNATURE\n")
            fo.write(f"`scripts/execution_audit.py` frozen at sha `{h_exec}`.\n")
            fo.write(f"`scripts/build_ledger.py` frozen at sha `{h_ledger}`.\n")
            fo.write("## 6. LINEAGE TRACE\n")
            fo.write(f"`scripts/execution_audit.py` originally frozen at `{'0'*64}`.\n")

        # Override the global state inside this function.
        old_scripts = SCRIPTS.copy()
        old_docs = DOCS[:]
        SCRIPTS.clear()
        SCRIPTS["scripts/execution_audit.py"] = os.path.join(tmp, "execution_audit.py")
        SCRIPTS["scripts/build_ledger.py"] = os.path.join(tmp, "build_ledger.py")
        DOCS[:] = [doc]

        rec = recorded_hashes()
        assert rec["scripts/execution_audit.py"] == {h_exec}, rec
        assert rec["scripts/build_ledger.py"] == {h_ledger}, rec
        assert "0" * 64 not in rec["scripts/execution_audit.py"], "lineage section was not skipped"
        print("selftest: parser OK (green)")

        # Now break the ledger file and confirm the check fails.
        with open(os.path.join(tmp, "build_ledger.py"), "ab") as fo:
            fo.write(b"# changed\n")
        red = run()
        assert red == 1, "expected a RED run on broken ledger hash"
        print("selftest: RED run captured")

        return 0
    finally:
        SCRIPTS.clear()
        SCRIPTS.update(old_scripts)
        DOCS[:] = old_docs
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true",
                    help="verify parser against a synthetic doc in a scratch root")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    return run()


if __name__ == "__main__":
    sys.exit(main())
