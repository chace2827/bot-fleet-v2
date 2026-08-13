#!/usr/bin/env python3
"""Deterministic spot-check: no .md file states a figure the CSVs contradict.

This is intentionally small.  It starts with two known examples from the Phase 0
prompt — the stale `hedge_tournament.csv` `T00001` example and the `bots_meta.csv`
GF-arm row count — plus a generic parser for `STATUS.md` headline numbers.

Exit 0 if clean, 1 with file:line and expected-vs-actual for each contradiction.
"""
import csv, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WORD2NUM = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
}


def load_csv(name):
    path = os.path.join(ROOT, "data", name)
    return list(csv.DictReader(open(path))) if os.path.exists(path) else []


def load_lines(path):
    with open(path) as f:
        return f.readlines()


def int_val(s):
    s = (s or "").strip().lower()
    if s in WORD2NUM:
        return WORD2NUM[s]
    return int(s.replace(",", ""))


def fl(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def md_files():
    out = [os.path.join(ROOT, "STATUS.md")]
    docs = os.path.join(ROOT, "docs")
    if os.path.isdir(docs):
        for root, _dirs, files in os.walk(docs):
            for f in files:
                if f.endswith(".md") and f not in ("session-log.md", "rules-catalog.md") \
                        and not f.startswith("_"):
                    out.append(os.path.join(root, f))
    return out


def check_status_headline(trades, errors):
    total_pnl = round(sum(fl(r.get("pnl")) for r in trades))
    n_legs = len(trades)
    n_bots = len({r.get("bot") for r in trades})
    pat = re.compile(
        r"Total closed P/L:\s*\$?([\d,]+)\s*·\s*(\d+)\s*legs?\s*·\s*(\d+)\s*bots?",
        re.I,
    )
    path = os.path.join(ROOT, "STATUS.md")
    for i, line in enumerate(load_lines(path)):
        m = pat.search(line)
        if not m:
            continue
        doc_pnl, doc_legs, doc_bots = int_val(m.group(1)), int(m.group(2)), int(m.group(3))
        if doc_pnl != total_pnl:
            errors.append((path, i + 1, f"Total closed P/L says ${doc_pnl}, trades.csv sum is ${total_pnl}"))
        if doc_legs != n_legs:
            errors.append((path, i + 1, f"legs says {doc_legs}, trades.csv has {n_legs}"))
        if doc_bots != n_bots:
            errors.append((path, i + 1, f"bots says {doc_bots}, trades.csv has {n_bots}"))


def check_gf_arm_count(bots, errors):
    """Docs mention a number of GF/greenfield arms; bots_meta.csv is the source."""
    def is_gf(r):
        b = (r.get("bot") or "").lower()
        n = (r.get("notes") or "").lower()
        return "gf-" in b or "greenfield" in b or "greenfield" in n

    gf_count = sum(1 for r in bots if is_gf(r))
    # Digits or spelled-out small numbers followed by GF/greenfield and arm.
    pat = re.compile(
        r"\b(?:([0-9]+)|(one|two|three|four|five|six|seven|eight|nine|ten))\b"
        r"\s+(?:GF|greenfield)\s+arm",
        re.I,
    )
    for path in md_files():
        for i, line in enumerate(load_lines(path)):
            m = pat.search(line)
            if not m:
                continue
            expected = int_val(m.group(1) or m.group(2))
            if expected != gf_count:
                errors.append((path, i + 1, f"says {expected} GF/greenfield arms, bots_meta.csv has {gf_count}"))


def check_trade_id_persistence(ht, errors):
    """The comparative-machinery spec says trade_id is never persisted / not stable.
    If hedge_tournament.csv carries the same trade_id across multiple dates, that is
    a stale/persisted usage of the key and is reported as a contradiction.
    """
    t00001_dates = sorted({r.get("date") for r in ht if r.get("trade_id") == "T00001"})
    if len(t00001_dates) <= 1:
        return
    pat = re.compile(
        r"trade_id.*(?:never persisted|not stable|regenerated T00001)",
        re.I,
    )
    for path in md_files():
        for i, line in enumerate(load_lines(path)):
            if pat.search(line):
                errors.append((path, i + 1, f"claims trade_id not persisted, but hedge_tournament.csv has T00001 on {len(t00001_dates)} dates ({', '.join(t00001_dates)})"))
                return


def main():
    trades = load_csv("trades.csv")
    bots = load_csv("bots_meta.csv")
    ht = load_csv("hedge_tournament.csv")

    errors = []
    check_status_headline(trades, errors)
    check_gf_arm_count(bots, errors)
    check_trade_id_persistence(ht, errors)

    if errors:
        print("CONTRADICTIONS FOUND:")
        for path, line, msg in errors:
            print(f"  {os.path.relpath(path, ROOT)}:{line}: {msg}")
        sys.exit(1)

    print("check_docs_vs_csv.py: no contradictions")


if __name__ == "__main__":
    main()
