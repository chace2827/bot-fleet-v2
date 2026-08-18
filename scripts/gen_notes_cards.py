#!/usr/bin/env python3
"""Generate OA Notes cards from the pre-registration ledger.

Reads only committed repo files and emits one card per currently-armed bot:

  data/notes_cards/<bot_id>.txt
  data/notes_cards/index.csv

The card format is the canonical pre-registration ledger template with every
field naming its source file. A field with no known source is emitted as
"[NO SOURCE]".

Usage:
  python3 scripts/gen_notes_cards.py
  python3 scripts/gen_notes_cards.py --selftest
"""
import argparse
import csv
import hashlib
import io
import os
import re
import sys
import tempfile
from collections import OrderedDict
from pathlib import Path

# ---------------------------------------------------------------------------
# Canonical card template.
#
# Every generated card contains these fields in this order, followed by any
# additional source-specific fields found in the pre-registration ledger entry.
#
# Field sources:
#   BOT              -> data/bots_meta.csv
#   ID               -> docs/pre-registration-ledger.md (or greenfield-family-spec.md table for GF bots)
#   DISPOSITION      -> docs/pre-registration-ledger.md
#   PILLAR/ROLE      -> docs/pre-registration-ledger.md (PILLAR/ROLE or ROLE line)
#   STATUS           -> docs/pre-registration-ledger.md
#   HYPOTHESIS       -> docs/pre-registration-ledger.md
#   MECHANISM        -> docs/pre-registration-ledger.md (MECHANISM or CLOSE MECHANISM)
#   ARM VARIABLE     -> docs/greenfield-family-spec.md §3 roster table (GF bots only)
#   KILL CRITERION   -> docs/pre-registration-ledger.md
#   SAMPLE TARGET    -> docs/pre-registration-ledger.md (SAMPLE TARGET or SAMPLE)
#   REVIEW DATE      -> docs/pre-registration-ledger.md
#   GATE EVAL DATE   -> docs/pre-registration-ledger.md
#   MAX LOSS         -> docs/pre-registration-ledger.md
#   SIZING TIER      -> docs/pre-registration-ledger.md
#   CONFIG HASH      -> docs/pre-registration-ledger.md
#   VERIFICATION     -> docs/pre-registration-ledger.md (VERIFICATION or LAYER 2)
#   SIGNED           -> docs/pre-registration-ledger.md
# ---------------------------------------------------------------------------

CANONICAL_FIELDS = [
    "BOT",
    "ID",
    "DISPOSITION",
    "PILLAR/ROLE",
    "STATUS",
    "HYPOTHESIS",
    "MECHANISM",
    "ARM VARIABLE",
    "KILL CRITERION",
    "SAMPLE TARGET",
    "REVIEW DATE",
    "GATE EVAL DATE",
    "MAX LOSS",
    "SIZING TIER",
    "CONFIG HASH",
    "VERIFICATION",
    "SIGNED",
]

# Source field labels that map to canonical fields.
CANONICAL_ALIASES = {
    "ROLE": "PILLAR/ROLE",
    "SAMPLE": "SAMPLE TARGET",
    "LAYER 2": "VERIFICATION",
    "CLOSE MECHANISM": "MECHANISM",
}

# All field labels we want to recognise while parsing a ledger code block.
FIELD_NAMES = set(CANONICAL_FIELDS) | set(CANONICAL_ALIASES.keys()) | {
    "SOURCE",
    "PRIMARY READ",
    "ALLOCATION",
    "STARTING DELTA",
    "RISK NOTE",
    "STRATEGY IDENTITY",
    "ENTRY",
    "SHARED-AUTOMATION SURFACE",
    "RECORD AS SIGNED",
    "NAMING",
    "BOT ID",
    "PHASE LOG",
    "RETIREMENT DATE",
}

# Column where ledger continuation lines start. We strip this much leading
# whitespace from continuation lines while preserving any further indentation.
VALUE_COL = 17

# Fixed output column at which values start. Must be >= the longest label.
LABEL_WIDTH = 27

NO_SOURCE = "[NO SOURCE]"


def root():
    return Path(__file__).resolve().parent.parent


def read_file(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Markdown / ledger parsing
# ---------------------------------------------------------------------------

def parse_markdown_sections(text):
    """Split a Markdown file into (heading_line, body) sections."""
    heading_re = re.compile(r'^(#{2,6})\s+(.*)$', re.M)
    matches = list(heading_re.finditer(text))
    sections = []
    for i, m in enumerate(matches):
        level = len(m.group(1))
        heading = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections.append((heading, text[start:end]))
    return sections


def first_code_block(section):
    """Return the body of the first ```-fenced block in a section, or None."""
    m = re.search(r'^```\s*\n(.*?)\n^```\s*$', section, re.S | re.M)
    return m.group(1) if m else None


def bot_name_from_heading(heading):
    """Extract the bot name from a section heading."""
    m = re.search(r'`([^`]+)`', heading)
    if m:
        return m.group(1).strip()
    # strip leading PR-/INC-/R- prefix, numbering, em-dash annotation
    s = re.sub(r'^(PR-\d+|INC-\d+|R-\d+|\d+\.\d+|\d+)\s*[—-]\s*', '', heading)
    s = re.split(r'[\s(]', s, 1)[0]
    s = s.strip()
    if s and s != 'exact OA bot name' and not s.startswith('<'):
        return s
    return None


def split_field_line(line):
    """Return [(label, value), ...] for one ledger code-block line.

    A line may contain multiple fields separated by two or more spaces, or a
    single field whose value starts after one space or on the following line.
    Field labels are word-bounded and may only begin at the start of a line or
    after two spaces, so "BOT" inside "BOTfw5..." and "SIGNED" inside value
    text are not treated as labels.
    """
    labels = sorted(FIELD_NAMES, key=len, reverse=True)

    # 1. Detect a label at the start of the line (value may follow after one or
    #    more spaces, or be on the next line).
    start_label = None
    rest = line
    for label in labels:
        if line.startswith(label):
            after = line[len(label):]
            if not after or after[0].isspace():
                start_label = label
                rest = after.lstrip(' ')
                break

    pairs = []
    if start_label is not None:
        # 2. Look for additional fields in the *rest*, separated by two or more
        #    spaces and followed by two or more spaces (or end-of-line).
        internal_pattern = re.compile(
            r'(?<=  )\b(' + '|'.join(re.escape(l) for l in labels) + r')\b(?:\s{2,}|$)'
        )
        matches = list(internal_pattern.finditer(rest))
        if matches:
            pairs.append((start_label, rest[:matches[0].start()].rstrip()))
            for i, m in enumerate(matches):
                label = m.group(1)
                start = m.end()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(rest)
                val = rest[start:end].strip()
                pairs.append((label, val))
        else:
            pairs.append((start_label, rest.rstrip()))
    else:
        # 3. No start label; allow any field on the line that is preceded and
        #    followed by at least two spaces. This is a fallback for malformed
        #    single lines that do not start with a label.
        pattern = re.compile(
            r'(?:^|(?<=  ))\b(' + '|'.join(re.escape(l) for l in labels) + r')\b\s{2,}'
        )
        matches = list(pattern.finditer(line))
        for i, m in enumerate(matches):
            label = m.group(1)
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(line)
            val = line[start:end].strip()
            pairs.append((label, val))
    return pairs


def parse_code_block(text):
    """Parse a ledger code block into an OrderedDict of field -> text."""
    fields = OrderedDict()
    current = None
    for raw in text.splitlines():
        raw = raw.rstrip('\n')
        leading = len(raw) - len(raw.lstrip(' '))
        stripped = raw.lstrip(' ')
        if not stripped:
            if current is not None:
                fields[current].append('')
            continue
        if leading >= VALUE_COL:
            # continuation line
            if current is not None:
                cont = raw[VALUE_COL:] if leading >= VALUE_COL else raw.lstrip(' ')
                fields[current].append(cont)
            continue
        pairs = split_field_line(stripped)
        if not pairs:
            # non-field line with leading spaces below the threshold
            if current is not None:
                fields[current].append(stripped)
            continue
        for label, first_line in pairs:
            current = label
            if label not in fields:
                fields[label] = []
            if first_line:
                fields[label].append(first_line)
    # join value lines with newlines
    for k in fields:
        fields[k] = '\n'.join(fields[k])
    return fields


def normalise_fields(fields, bot_name, pr, role=None, arm_variable=None):
    """Map aliases, inject computed fields, and return a canonical OrderedDict."""
    out = OrderedDict()
    # Canonical fields first
    for label in CANONICAL_FIELDS:
        if label == 'BOT':
            out[label] = bot_name
        elif label == 'ID':
            out[label] = pr if pr else NO_SOURCE
        elif label == 'PILLAR/ROLE' and role is not None:
            out[label] = role
        elif label == 'ARM VARIABLE' and arm_variable is not None:
            out[label] = arm_variable
        else:
            # look for canonical field or alias
            src_label = None
            if label in fields:
                src_label = label
            else:
                for alias, target in CANONICAL_ALIASES.items():
                    if target == label and alias in fields:
                        src_label = alias
                        break
            out[label] = fields[src_label] if src_label else NO_SOURCE
    # Append any extra source fields in source order, except those we consumed
    consumed = set(CANONICAL_FIELDS) | set(CANONICAL_ALIASES.keys())
    for label, value in fields.items():
        if label in consumed:
            continue
        out[label] = value
    return out


# ---------------------------------------------------------------------------
# Source files
# ---------------------------------------------------------------------------

def load_bots_meta(path):
    """Return a list of currently-armed bots from data/bots_meta.csv."""
    bots = []
    with open(path, encoding='utf-8', newline='') as fh:
        for row in csv.DictReader(fh):
            if (row.get('status') or '').strip().upper() == 'ON':
                bots.append(row['bot'].strip())
    bots.sort()
    return bots


def load_ledger(path):
    """Parse docs/pre-registration-ledger.md and return two dicts:

    direct:  bot_name -> {heading, code_block, id, fields}
    groups:  group_key -> {heading, code_block, id, fields}

    group keys are derived from the ID line or heading.
    """
    text = read_file(path)
    direct = {}
    groups = {}
    for heading, body in parse_markdown_sections(text):
        block = first_code_block(body)
        if not block:
            continue
        fields = parse_code_block(block)
        if 'ID' not in fields:
            continue
        id_val = fields['ID'].split('\n')[0].strip()
        bot = bot_name_from_heading(heading)
        rec = {
            'heading': heading,
            'code_block': block,
            'id_raw': id_val,
            'fields': fields,
        }
        # direct per-bot entries have a single PR/INC id and a bot name in heading
        if re.match(r'^(PR|INC)-\d+$', id_val) and bot:
            direct[bot] = rec
        else:
            # classify as a group template
            key = None
            if 'PR-14' in id_val and 'PR-17' in id_val:
                key = 'pr14-17'
            elif 'PR-18' in id_val:
                key = 'pr18-'
            elif 'next free ID' in id_val.lower() or 'Optional 1-lot canary' in heading:
                key = 'canary'
            elif 'PR-07' in id_val and 'PR-13' in id_val:
                key = 'pr07-13'
            elif bot:
                # direct but with non-PR/INC id? keep under bot too
                direct[bot] = rec
            if key:
                groups[key] = rec
    return direct, groups


def load_greenfield_spec(path):
    """Parse greenfield-family-spec.md §3 roster table.

    Returns {bot_name: {'pr': ..., 'role': ..., 'arm_variable': ...}}.
    """
    mapping = {}
    text = read_file(path)
    in_table = False
    for line in text.splitlines():
        # the roster table header
        if '| Bot name |' in line and '| Role |' in line and '| PR |' in line:
            in_table = True
            continue
        if not in_table:
            continue
        if not line.strip().startswith('|'):
            break
        # skip separator row
        if re.match(r'^\|[-\s|]*\|$', line.strip()):
            continue
        parts = [p.strip().strip('`').strip('*') for p in line.split('|')]
        parts = [p for p in parts if p]
        if len(parts) < 5:
            continue
        # columns: #, Bot name, Role, Arm variable, PR
        bot, role, arm, pr = parts[-4], parts[-3], parts[-2], parts[-1]
        if not re.match(r'^PR-\d+$', pr):
            continue
        if not bot.startswith('GF-QQQ-IC-'):
            continue
        mapping[bot] = {
            'pr': pr,
            'role': role,
            'arm_variable': arm,
        }
    return mapping


# ---------------------------------------------------------------------------
# Card generation
# ---------------------------------------------------------------------------

def source_for_bot(bot, direct, groups, greenfield):
    """Return (code_block_text, fields, pr, role, arm_variable) for a bot."""
    if bot in greenfield:
        spec = greenfield[bot]
        pr = spec['pr']
        role = f"IC · {spec['role']}"
        arm = spec['arm_variable']
        if pr == 'PR-23':
            # direct entry
            if bot in direct:
                return direct[bot]['code_block'], direct[bot]['fields'], pr, role, arm
        if pr in ('PR-14', 'PR-15', 'PR-16', 'PR-17'):
            group_key = 'pr14-17'
        elif pr in ('PR-18', 'PR-19'):
            group_key = 'pr18-'
        elif pr == 'PR-20':
            group_key = 'canary'
        else:
            group_key = None
        if group_key and group_key in groups:
            return groups[group_key]['code_block'], groups[group_key]['fields'], pr, role, arm
    # direct entry
    if bot in direct:
        rec = direct[bot]
        pr = rec['fields'].get('ID', '').split('\n')[0].strip()
        return rec['code_block'], rec['fields'], pr, None, None
    raise KeyError(f"No pre-registration source for {bot}")


def slugify(bot):
    """Return a filesystem-safe, deterministic filename fragment for a bot."""
    return re.sub(r'[^A-Za-z0-9]+', '_', bot).strip('_')


def render_card(fields):
    """Render an OrderedDict of fields into a byte-stable card text."""
    lines = []
    indent = ' ' * LABEL_WIDTH
    for label, value in fields.items():
        if '\n' in value:
            first, rest = value.split('\n', 1)
            padding = ' ' * (LABEL_WIDTH - len(label))
            lines.append(f"{label}{padding}{first}")
            for rline in rest.split('\n'):
                lines.append(f"{indent}{rline}")
        else:
            padding = ' ' * (LABEL_WIDTH - len(label))
            lines.append(f"{label}{padding}{value}")
    return '\n'.join(lines) + '\n'


def no_source_fields(fields):
    """Return a comma-separated list of canonical fields with [NO SOURCE]."""
    missing = [k for k in CANONICAL_FIELDS if fields.get(k) == NO_SOURCE]
    return ','.join(missing)


def generate(output_dir, bots, direct, groups, greenfield):
    """Generate cards and index. Return a list of index rows."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    expected = {slugify(bot) + '.txt' for bot in bots}
    for old in output_dir.glob('*.txt'):
        if old.name not in expected:
            old.unlink()
    index = []
    for bot in bots:
        code, fields, pr, role, arm = source_for_bot(bot, direct, groups, greenfield)
        parsed = parse_code_block(code)
        normalised = normalise_fields(parsed, bot, pr, role=role, arm_variable=arm)
        text = render_card(normalised)
        slug = slugify(bot)
        filename = f"{slug}.txt"
        path = output_dir / filename
        with open(path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
        sha = hashlib.sha256(text.encode('utf-8')).hexdigest()
        index.append({
            'bot': bot,
            'pr': pr,
            'filename': filename,
            'sha256': sha,
            'no_source_fields': no_source_fields(normalised),
        })
    # write index
    index_path = output_dir / 'index.csv'
    with open(index_path, 'w', encoding='utf-8', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=['bot', 'pr', 'filename', 'sha256', 'no_source_fields'])
        writer.writeheader()
        writer.writerows(index)
    return index


# ---------------------------------------------------------------------------
# Selftest
# ---------------------------------------------------------------------------

FIXTURE_BOTS_META = """bot,pillar,role,underlying,status
GF-QQQ-IC-Ride,IC,control,QQQ,ON
GF-QQQ-IC-PT50,IC,experiment,QQQ,ON
IC-SPX-Fortress-Unstopped,IC,control,SPX,ON
DIR-SPX-PutVIX22-SL75,Directional,experiment,SPX,ON
"""

FIXTURE_LEDGER = r"""## 6. Group D — fresh builds

### Greenfield IC family — 4 matched arms
```
ID               PR-14 … PR-17
DISPOSITION      fresh build          PILLAR/ROLE  IC · experiment      STATUS  DRAFT
HYPOTHESIS       Family hypothesis.
MECHANISM        Family mechanism.
KILL CRITERION   R < 0 at n≥60.
SAMPLE TARGET    n = 100 positions.
REVIEW DATE      Day-0 + 6 months.
MAX LOSS         1 lot.
SIZING TIER      1 lot.
CONFIG HASH      STAMPED.
VERIFICATION     Capture-diff.
SIGNED           2026-08-17 · ANDY.
```

### `IC-SPX-Fortress-Unstopped`
```
ID               INC-01
BOT              IC-SPX-Fortress-Unstopped   BOTfw5TkkCRF1234567890
DISPOSITION      re-opened
ROLE             SIGNED INCUMBENT BENCHMARK
STATUS           SIGNED
STRATEGY IDENTITY disableExits:1 is the design.
CLOSE MECHANISM  hold to expiration.
KILL CRITERION   p-factor < 1.0
SAMPLE           n = 15 new closes
REVIEW DATE      n=30 or 2026-11-30
CONFIG HASH      9f86d08...
LAYER 2          no exit rows.
SIGNED           2026-08-17 · ANDY.
```

### `DIR-SPX-PutVIX22-SL75`
```
ID               PR-05
DISPOSITION      untouched            PILLAR/ROLE  Directional · experiment   STATUS  DRAFT
HYPOTHESIS       VIX≥22 gate.
MECHANISM        VIX gate.
KILL CRITERION   R < -0.10.
SAMPLE TARGET    n = 50.
REVIEW DATE      Day-0 + 6 months.
GATE EVAL DATE   same.
MAX LOSS         1 lot.
SIZING TIER      1 lot.
CONFIG HASH      pending.
VERIFICATION     bot log.
SIGNED           2026-08-09 · ANDY.
```
"""

FIXTURE_GREENFIELD = """## 3. The roster

|| # | Bot name | Role | Arm variable (the whole bundle) | PR |
||---|---|---|---|---|
|| 1 | `GF-QQQ-IC-Ride` | **control** | time exit only | PR-14 |
|| 2 | `GF-QQQ-IC-PT50` | **experiment** | time exit + Profit Taking % 50 | PR-15 |
"""


def selftest():
    errors = []

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / 'data').mkdir()
        (tmp / 'docs').mkdir()
        open(tmp / 'data' / 'bots_meta.csv', 'w', encoding='utf-8').write(FIXTURE_BOTS_META)
        open(tmp / 'docs' / 'pre-registration-ledger.md', 'w', encoding='utf-8').write(FIXTURE_LEDGER)
        open(tmp / 'docs' / 'greenfield-family-spec.md', 'w', encoding='utf-8').write(FIXTURE_GREENFIELD)

        bots = load_bots_meta(tmp / 'data' / 'bots_meta.csv')
        if set(bots) != {'DIR-SPX-PutVIX22-SL75', 'GF-QQQ-IC-PT50', 'GF-QQQ-IC-Ride', 'IC-SPX-Fortress-Unstopped'}:
            errors.append(f"unexpected active bots: {bots}")

        direct, groups = load_ledger(tmp / 'docs' / 'pre-registration-ledger.md')
        greenfield = load_greenfield_spec(tmp / 'docs' / 'greenfield-family-spec.md')

        # PR-14 should come from the greenfield group in this fixture
        code, fields, pr, role, arm = source_for_bot('GF-QQQ-IC-Ride', direct, groups, greenfield)
        if pr != 'PR-14':
            errors.append(f"PR-14 expected PR-14, got {pr}")
        if role is None or 'control' not in role:
            errors.append(f"PR-14 role should be control, got {role}")
        if arm is None or 'time exit only' not in arm:
            errors.append(f"PR-14 arm variable wrong: {arm}")

        # PT50 comes from the same greenfield group
        code, fields, pr, role, arm = source_for_bot('GF-QQQ-IC-PT50', direct, groups, greenfield)
        if pr != 'PR-15':
            errors.append(f"PT50 expected PR-15, got {pr}")
        if role is None or 'experiment' not in role:
            errors.append(f"PT50 role should be experiment, got {role}")
        if arm is None or 'Profit Taking' not in arm:
            errors.append(f"PT50 arm variable wrong: {arm}")

        # INC-01 parsing
        if 'IC-SPX-Fortress-Unstopped' not in direct:
            errors.append("INC-01 direct section not found")
        else:
            inc_fields = parse_code_block(direct['IC-SPX-Fortress-Unstopped']['code_block'])
            if 'BOT' not in inc_fields:
                errors.append("INC-01 BOT field not parsed")
            if 'LAYER 2' not in inc_fields:
                errors.append("INC-01 LAYER 2 not parsed")
            if 'CLOSE MECHANISM' not in inc_fields:
                errors.append("INC-01 CLOSE MECHANISM not parsed")

        # Render a card and verify determinism
        card_fields = normalise_fields(
            parse_code_block(direct['IC-SPX-Fortress-Unstopped']['code_block']),
            'IC-SPX-Fortress-Unstopped',
            'INC-01',
            role='IC · control',
            arm_variable=None,
        )
        text1 = render_card(card_fields)
        text2 = render_card(card_fields)
        if text1 != text2:
            errors.append("card text not deterministic")
        if 'HYPOTHESIS' in card_fields and card_fields['HYPOTHESIS'] == NO_SOURCE:
            pass  # expected
        else:
            errors.append("INC-01 HYPOTHESIS should be [NO SOURCE]")

        # parse_code_block must not split BOT inside BOTfw5...
        if 'IC-SPX-Fortress-Unstopped' in direct:
            bot_val = parse_code_block(direct['IC-SPX-Fortress-Unstopped']['code_block']).get('BOT', '')
            if 'BOTfw5TkkCRF1234567890' not in bot_val:
                errors.append(f"bot id lost in BOT value: {bot_val!r}")

    if errors:
        for e in errors:
            print(f"selftest FAIL: {e}", file=sys.stderr)
        return 1
    print("gen_notes_cards.py: selftest OK")
    return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--selftest', action='store_true', help='run the selftest')
    ap.add_argument('--root', default=str(root()), help='repo root')
    ap.add_argument('--output', default=None, help='output directory')
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    repo = Path(args.root)
    output = Path(args.output) if args.output else repo / 'data' / 'notes_cards'

    bots = load_bots_meta(repo / 'data' / 'bots_meta.csv')
    direct, groups = load_ledger(repo / 'docs' / 'pre-registration-ledger.md')
    greenfield = load_greenfield_spec(repo / 'docs' / 'greenfield-family-spec.md')

    index = generate(output, bots, direct, groups, greenfield)
    print(f"gen_notes_cards: generated {len(index)} cards in {output}")
    for row in index:
        print(f"  {row['bot']:<45} {row['pr']:<10} {row['sha256'][:16]}...")
    return 0


if __name__ == '__main__':
    sys.exit(main())
