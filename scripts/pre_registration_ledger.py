#!/usr/bin/env python3
"""Parser for docs/pre-registration-ledger.md.

Identifies pre-registration entries by structure, not heading hash count:
a section is an entry if its first fenced code block contains an
`ID PR-nn` or `ID INC-nn` line.  A bot is listed as unsigned if its SIGNED line
is missing, blank, or contains "NOT SIGNED".
"""
import os
import re
import sys


def _first_code_block(text):
    """Return the body of the first ```-fenced block, or None."""
    m = re.search(r'^```\n(.*?)\n```', text, re.S | re.M)
    return m.group(1) if m else None


def _bot_name_from_heading(heading):
    """Extract the bot name from a heading line.

    Prefer the first backtick-wrapped token; otherwise strip a PR/INC prefix
    and any annotation, then use the remaining text.
    """
    m = re.search(r'`([^`]+)`', heading)
    if m:
        return m.group(1).strip()

    # strip leading PR-/INC-/R- prefix, leading numbering, em-dash annotation
    s = re.sub(r'^(PR-\d+|INC-\d+|R-\d+|\d+\.\d+|\d+)\s*[—-]\s*', '', heading)
    s = re.split(r'[\s(]', s, 1)[0]
    s = s.strip()
    if s and s != 'exact OA bot name' and not s.startswith('<'):
        return s
    return None


def _is_signed(signed_val):
    """A SIGNED value is signed iff it contains a YYYY-MM-DD and no negation.

    Negation includes an explicit "NOT SIGNED" or a signed-but-unverified
    S2b signature that carries an owed first-trading-day capture.
    """
    if not signed_val:
        return False
    if 'NOT SIGNED' in signed_val:
        return False
    if 'SIGNED != VERIFIED' in signed_val and 'FIRST-TRADING-DAY CAPTURE OWED' in signed_val:
        return False
    return bool(re.search(r'\d{4}-\d{2}-\d{2}', signed_val))


def parse_ledger_text(text):
    """Return (unsigned_bots, warnings) for the given ledger markdown.

    unsigned_bots is a set of bot names whose SIGNED line is missing/blank/NOT SIGNED.
    warnings is a list of strings describing sections that could not be classified.
    """
    unsigned = set()
    warnings = []

    # Split on any ATX heading, capturing level and heading text.
    heading_re = re.compile(r'^(#{1,6})\s+(.*)$', re.M)
    matches = list(heading_re.finditer(text))
    for i, m in enumerate(matches):
        level, heading = m.group(1), m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section = text[start:end]

        # Only classify sections that contain a fenced code block.
        block = _first_code_block(section)
        if block is None:
            continue

        id_m = re.search(r'^ID\s+(\S.*)$', block, re.M)
        if not id_m:
            warnings.append(
                f"WARNING: {level} {heading!r} has a code block but no ID field; skipped")
            continue

        id_val = id_m.group(1).strip()
        # A single PR-nn or INC-nn identifies a pre-registration bot entry.
        if not re.match(r'^(PR|INC)-\d+$', id_val):
            warnings.append(
                f"WARNING: {level} {heading!r} has ID {id_val!r} but is not a single "
                f"PR-nn or INC-nn entry; skipped")
            continue

        bot = _bot_name_from_heading(heading)
        if not bot:
            warnings.append(
                f"WARNING: {level} {heading!r} (ID {id_val}) has no usable bot name; skipped")
            continue

        signed_m = re.search(r'^SIGNED\s+(.*?)(?=^\S|\Z)', block, re.S | re.M)
        signed_val = signed_m.group(1).strip() if signed_m else ''
        if not _is_signed(signed_val):
            unsigned.add(bot)

    return unsigned, warnings


def unsigned_from_ledger(path):
    """Return the set of unsigned bots for the ledger file at *path*.

    Warnings are emitted to stderr; the caller (report.py) may suppress or log them.
    """
    if not os.path.exists(path):
        return set()
    text = open(path).read()
    unsigned, warnings = parse_ledger_text(text)
    for w in warnings:
        print(w, file=sys.stderr)
    return unsigned


# --- selftest / fixture cases ---------------------------------------------

FIXTURE = r"""
# test fixture

#### PR-01 — `IC-SPX-FastPT25-S2`
```
ID               PR-01
SIGNED           2026-08-09 · ANDY
```

### PR-02 — `IC-SPX-FastPT25-S2-130PM`
```
ID               PR-02
SIGNED           2026-08-09 - ANDY - gate cleared at S2b, in-chat.
                 SIGNED != VERIFIED. The INVERTED Step-6 check is DEFERRED to 2026-08-10.
                 FIRST-TRADING-DAY CAPTURE OWED 2026-08-10.
```

### `QQQ-IC-0DTE-Fortress`
```
ID               PR-03
SIGNED           ..............................
```

#### `QQQ-IC-0DTE-Fortress-NoPT50`
```
ID               PR-04
SIGNED           2026-08-09 - ANDY - gate cleared at S2b, in-chat.
                 SIGNED != VERIFIED. Step 6 is DEFERRED to 2026-08-10.
                 FIRST-TRADING-DAY CAPTURE OWED 2026-08-10.
```

### INC-01 — `IC-SPX-Fortress-Unstopped`
```
ID               INC-01
SIGNED           2026-08-17 · ANDY
```

### INC-02 — `Test-Inc-Unsigned`
```
ID               INC-02
SIGNED           ..............................
```

## Some group header (not an entry)
No code block here — should not warn.

### Greenfield IC family
```
ID               PR-14 … PR-17
SIGNED           2026-08-17 · ANDY
```
"""


def selftest():
    unsigned, warnings = parse_ledger_text(FIXTURE)
    expected = {
        'IC-SPX-FastPT25-S2-130PM',
        'QQQ-IC-0DTE-Fortress',
        'QQQ-IC-0DTE-Fortress-NoPT50',
        'Test-Inc-Unsigned',
    }
    if unsigned != expected:
        print(f"FAIL: expected unsigned {expected}, got {unsigned}", file=sys.stderr)
        return 1
    if 'IC-SPX-Fortress-Unstopped' in unsigned:
        print("FAIL: INC-01 is signed and should not be unsigned", file=sys.stderr)
        return 1
    if 'IC-SPX-FastPT25-S2' in unsigned:
        print("FAIL: PR-01 is signed and should not be unsigned", file=sys.stderr)
        return 1
    # PR-02 and PR-04 must render even though one uses #### and one uses ###
    if 'IC-SPX-FastPT25-S2-130PM' not in unsigned:
        print("FAIL: PR-02 (#### heading) did not render", file=sys.stderr)
        return 1
    if 'QQQ-IC-0DTE-Fortress-NoPT50' not in unsigned:
        print("FAIL: PR-04 (mixed heading) did not render", file=sys.stderr)
        return 1
    if 'IC-SPX-Fortress-Unstopped' in unsigned:
        print("FAIL: INC-01 is signed and should not be unsigned", file=sys.stderr)
        return 1
    if 'Test-Inc-Unsigned' not in unsigned:
        print("FAIL: INC-02 did not render as unsigned", file=sys.stderr)
        return 1
    if not any('Greenfield IC family' in w for w in warnings):
        print("FAIL: expected a WARNING for the unclassifiable family section", file=sys.stderr)
        return 1
    if any('Some group header' in w for w in warnings):
        print("FAIL: should not warn about a heading with no code block", file=sys.stderr)
        return 1

    # Live known-positive check: the real ledger must mark PR-02 and PR-04
    # as unsigned because their SIGNED blocks carry SIGNED != VERIFIED +
    # FIRST-TRADING-DAY CAPTURE OWED. Synthetic fixtures are not enough.
    _live_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'docs', 'pre-registration-ledger.md')
    if os.path.exists(_live_path):
        live_unsigned, _ = parse_ledger_text(open(_live_path).read())
        for bot in ('IC-SPX-FastPT25-S2-130PM', 'QQQ-IC-0DTE-Fortress-NoPT50'):
            if bot not in live_unsigned:
                print(f"FAIL: live ledger does not flag {bot} as unsigned", file=sys.stderr)
                return 1
        if 'IC-SPX-Fortress-Unstopped' in live_unsigned:
            print("FAIL: live ledger has INC-01 signed; parser must not flag it", file=sys.stderr)
            return 1

    print("pre_registration_ledger.py: selftest OK")
    for w in warnings:
        print(w)
    return 0


if __name__ == '__main__':
    sys.exit(selftest())
