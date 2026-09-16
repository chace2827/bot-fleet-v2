#!/usr/bin/env python3
"""oa_normalize.py — make two /bots captures comparable, and summarise what a capture asserts.

WHY: docs/oa-ops-runbook.md §1.5 — "Normalise before diffing, or you get false positives
every single day." The sidebar clock, the `captured:` line, the Opportunities counter, the
account-inactive banner and the plan footer change on every pull and mean nothing.

WHAT IT DOES NOT DO: reconcile, infer, or fill. It strips known-noisy lines and reports
what the file says. An absent value is reported absent, never as zero (CLAUDE.md §10).

USAGE
  python3 oa_normalize.py normalize CAPTURE.txt              # noise-stripped text to stdout
  python3 oa_normalize.py summary   CAPTURE.txt              # structural facts (JSON)
  python3 oa_normalize.py diff      OLD.txt NEW.txt          # unified diff, normalised
  python3 oa_normalize.py compare   OLD.txt NEW.txt          # STRUCTURAL comparison — use this

`compare` is the one that matters for a driver swap. P/L moves between captures and
always will; the bot-ID SET and the toggle states must not. If `compare` says the ID sets
are identical and the toggle counts match, the new driver is reading the same page the
bookmarklet reads. If it does not, you have a finding, not a formatting problem.
"""

import difflib
import hashlib
import json
import re
import sys

# --- §1.5 noise rules -------------------------------------------------------

CLOCK = re.compile(r"^\d{1,2}:\d{2}\s*(AM|PM)$", re.I)
FOOTER = re.compile(r"^\d+\s+active bots\b|left in your plan\b", re.I)
DROP_EXACT = {
    "Account inactive, no changes will be saved",
    "See plans",
    "Upgrade",
}
DROP_PREFIX = ("captured: ",)

TOGGLE_HEADER = "# AUTOS/EXITS"


def normalize(text: str) -> str:
    """Strip the lines §1.5 says will diff on every pull without meaning anything."""
    out, skip_next_numeric = [], False
    for line in text.splitlines():
        s = line.strip()
        if skip_next_numeric:
            skip_next_numeric = False
            if s.isdigit():
                continue
        if s.startswith(DROP_PREFIX):
            continue
        if s in DROP_EXACT:
            continue
        if CLOCK.match(s) or FOOTER.search(s):
            continue
        if s == "Opportunities":
            skip_next_numeric = True  # the counter renders as its own following line
            continue
        if re.match(r"^Opportunities\s+\d+$", s):
            continue
        out.append(line.rstrip())
    return "\n".join(out) + "\n"


# --- structural read --------------------------------------------------------

def toggle_rows(text: str):
    """Parse the appended AUTOS/EXITS section. Returns {} when the section is absent —
    which per §1.2 is itself a result (selectors missed), not an empty fleet."""
    rows = {}
    in_section = False
    for line in text.splitlines():
        if line.startswith(TOGGLE_HEADER):
            in_section = True
            continue
        if not in_section:
            continue
        parts = line.split("\t")
        if len(parts) >= 3 and parts[0].startswith("BOT"):
            rows[parts[0]] = {"autos": parts[1], "exits": parts[2]}
    return rows


def summarize(text: str) -> dict:
    rows = toggle_rows(text)
    anchors = re.findall(r"^# (.+)$", text, re.M)
    url = text.splitlines()[1] if len(text.splitlines()) > 1 else None
    captured = next((l[len("captured: "):] for l in text.splitlines() if l.startswith("captured: ")), None)

    def on(v):
        # "Scheduled automations are off" / "...are on" — the state is the trailing word.
        return None if not v else (not v.rstrip(". ").lower().endswith("off"))

    autos_on = [b for b, r in rows.items() if on(r["autos"]) is True]
    exits_on = [b for b, r in rows.items() if on(r["exits"]) is True]
    return {
        "page": anchors[0] if anchors else None,
        "url": url,
        "captured": captured,
        "sha256_raw": hashlib.sha256(text.encode()).hexdigest(),
        "sha256_normalized": hashlib.sha256(normalize(text).encode()).hexdigest(),
        "toggle_section_present": bool(rows),
        "bot_count": len(rows) if rows else None,
        "autos_on": len(autos_on) if rows else None,
        "exits_on": len(exits_on) if rows else None,
        "bot_ids": sorted(rows.keys()),
    }


def compare(a_text: str, b_text: str) -> dict:
    a, b = summarize(a_text), summarize(b_text)
    ids_a, ids_b = set(a["bot_ids"]), set(b["bot_ids"])
    ra, rb = toggle_rows(a_text), toggle_rows(b_text)
    changed = {
        bot: {"old": ra[bot], "new": rb[bot]}
        for bot in sorted(ids_a & ids_b)
        if ra[bot] != rb[bot]
    }
    verdict = []
    if not a["toggle_section_present"] or not b["toggle_section_present"]:
        verdict.append("INCONCLUSIVE — a capture has no AUTOS/EXITS section; nothing structural to compare")
    else:
        verdict.append("bot ID sets IDENTICAL" if ids_a == ids_b else "⛔ bot ID sets DIFFER")
        verdict.append("toggle states IDENTICAL" if not changed else f"⛔ {len(changed)} bot(s) differ in toggle state")
    return {
        "old": {k: a[k] for k in ("captured", "bot_count", "autos_on", "exits_on", "sha256_raw")},
        "new": {k: b[k] for k in ("captured", "bot_count", "autos_on", "exits_on", "sha256_raw")},
        "only_in_old": sorted(ids_a - ids_b),
        "only_in_new": sorted(ids_b - ids_a),
        "toggle_changes": changed,
        "verdict": verdict,
    }


# --- cli --------------------------------------------------------------------

def read(p):
    with open(p, encoding="utf-8", errors="replace") as f:
        return f.read()


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    mode, paths = argv[1], argv[2:]
    if mode == "normalize":
        sys.stdout.write(normalize(read(paths[0])))
    elif mode == "summary":
        print(json.dumps(summarize(read(paths[0])), indent=2))
    elif mode == "diff":
        if len(paths) != 2:
            print("diff needs two files")
            return 2
        a, b = normalize(read(paths[0])), normalize(read(paths[1]))
        sys.stdout.writelines(
            difflib.unified_diff(a.splitlines(True), b.splitlines(True), paths[0], paths[1])
        )
    elif mode == "compare":
        if len(paths) != 2:
            print("compare needs two files")
            return 2
        print(json.dumps(compare(read(paths[0]), read(paths[1])), indent=2))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
