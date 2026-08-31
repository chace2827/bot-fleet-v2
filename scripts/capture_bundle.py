#!/usr/bin/env python3
"""Build a /bots roster capture bundle.

Takes the raw bookmarklet .txt (the S0b-3 v2.1 /bots capture, with the trailing
`i.sticon[title]` AUTOS/EXITS title block) plus optional screenshots, and writes
`data/captures/<day>-roster/` with:

  01-bots-roster-<title-slug>-<day>-<HHMMSS>.txt   (renamed raw capture)
  02-roster-toggles-<N>-<day>.tsv                   (joined bot_name / bot_id / AUTOS / EXITS)
  screenshots/NN-...                                 (renamed screenshots)
  README.md                                          (files, drift verdict, closing state)
  SHA256SUMS.txt                                     (sha256 of every file except itself and .DS_Store)

The day is taken from the capture's own `captured:` header, never the filename
or wall clock.  The (name, bot_id) pairing is checked against the previous
bundle's TSV; a mismatch is fatal and aborts the bundle, because row-order joins
are not self-checking.
"""
import argparse
import csv
import datetime
import glob
import hashlib
import os
import re
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAPTURES = os.path.join(ROOT, "data", "captures")
CONFIG = os.path.join(ROOT, "data", "bots_config_v2.csv")

# Row stride in the /bots list table: 1 bot name + 18 numeric/empty values.
LIST_ROW_STRIDE = 19

BOT_ID_RE = re.compile(r"^BOT[a-zA-Z0-9]+")
CAPTURED_RE = re.compile(r"^captured:\s*(.+)$")
FOOTER_RE = re.compile(r"^(\d+)\s+active\s+bots")
TITLE_BLOCK_RE = re.compile(r"^#\s*AUTOS/EXITS\b")
LIST_HEADER_RE = re.compile(r"^#\s*Recent_Activity|Bots")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fo:
        for chunk in iter(lambda: fo.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def slugify(s):
    """Lower-case, hyphen-separated slug, like the 2026-08-19 file names."""
    s = re.sub(r"[^\w\s-]+", "", s).strip().lower()
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s


def title_from_text(lines):
    if lines and lines[0].startswith("# "):
        return lines[0][2:].strip()
    return "bots"


def parse_captured(line):
    m = CAPTURED_RE.match(line)
    if not m:
        return None
    # Strip the parenthetical timezone name; Python's %z parses "GMT-0400"
    # but not the trailing "(Eastern Daylight Time)".
    s = m.group(1).split(" (")[0].strip()
    try:
        return datetime.datetime.strptime(s, "%a %b %d %Y %H:%M:%S GMT%z")
    except ValueError:
        return None


def load_bots_config(config_path):
    """oa_id -> name, built ONLY from data/bots_config_v2.csv, skipping comment lines.

    The file has a long leading comment block; a naive csv.DictReader would use
    a comment as the header.  We skip '#' lines and then read the real header.
    """
    if not os.path.exists(config_path):
        return {}
    with open(config_path, newline="", encoding="utf-8") as fo:
        lines = [ln for ln in fo if not ln.startswith("#")]
    if not lines:
        return {}
    r = csv.DictReader(lines)
    return {
        row["oa_id"].strip(): row["name"].strip()
        for row in r
        if row.get("oa_id", "").strip().startswith("BOT") and row.get("name", "").strip()
    }


def parse_list_table(lines):
    """Return the list of bot names in /bots row order.

    The list table starts after a column-header block whose first three lines are
    ICON, BOT, 30D and whose last three lines are CLOSED, AUTOS, EXITS.  Each
    data row is 1 name + 18 values.  We stop at the footer or the AUTOS/EXITS
    title block.
    """
    header_start = None
    for i in range(len(lines) - 2):
        if lines[i] == "ICON" and lines[i + 1] == "BOT" and lines[i + 2] == "30D":
            header_start = i
            break
    if header_start is None:
        raise BundleError("FATAL: cannot find the /bots list table header (ICON/BOT/30D)")

    exits_idx = None
    for j in range(header_start, min(header_start + 30, len(lines))):
        if lines[j] == "EXITS" and j > 0 and lines[j - 1] == "AUTOS":
            exits_idx = j
            break
    if exits_idx is None:
        raise BundleError("FATAL: cannot find the 'EXITS' column header")

    idx = exits_idx + 1
    names = []
    while idx < len(lines):
        line = lines[idx]
        if FOOTER_RE.match(line) or TITLE_BLOCK_RE.match(line):
            break
        names.append(line)
        idx += LIST_ROW_STRIDE
    return names


def parse_title_block(lines):
    """Return list of (bot_id, autos_title, exits_title) triples from the title block."""
    start = None
    for i, line in enumerate(lines):
        if TITLE_BLOCK_RE.match(line):
            start = i
            break
    if start is None:
        raise BundleError("FATAL: cannot find the # AUTOS/EXITS title block")

    triples = []
    for line in lines[start + 1:]:
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) >= 3 and BOT_ID_RE.match(parts[0]):
            triples.append((parts[0], parts[1], parts[2]))
    return triples


def state_from_title(title):
    t = title.lower()
    if t.endswith(" are on"):
        return "ON"
    if t.endswith(" are off"):
        return "OFF"
    raise BundleError(f"FATAL: unrecognised toggle title: {title!r}")


def derive_rows(names, triples, config_map):
    """Pair list-table names with title-block ids, validating against bots_config_v2."""
    if len(names) != len(triples):
        raise BundleError(
            f"FATAL: list table has {len(names)} names but title block has {len(triples)} ids"
        )

    rows = []
    for i, (name, (bot_id, autos_title, exits_title)) in enumerate(zip(names, triples)):
        if bot_id in config_map and config_map[bot_id] != name:
            # The capture's list-table name and the config record disagree.
            # The config is a separate capture and must match; if it does not,
            # the positional join is not trustworthy for this bot.
            raise BundleError(
                f"FATAL: positional join mismatch at row {i + 1}: "
                f"title block bot_id {bot_id} paired with list-table name {name!r}, "
                f"but data/bots_config_v2.csv records that id as {config_map[bot_id]!r}"
            )
        rows.append((
            name,
            bot_id,
            state_from_title(autos_title),
            state_from_title(exits_title),
        ))
    return rows


def load_tsv_rows(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as fo:
        for line in fo:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.rstrip("\n").rstrip("\r").split("\t")
            if len(parts) >= 4 and not parts[0].startswith("#"):
                rows.append((parts[0], parts[1], parts[2], parts[3]))
    return rows


def cross_check(new_rows, prev_rows):
    """Return an empty list if the (name, bot_id) pairing is consistent, else errors.

    A bot present in both bundles must map to the same bot_id, and a bot_id
    present in both must map to the same name.  New or dropped bots are allowed.
    """
    errors = []
    prev_by_name = {r[0]: r[1] for r in prev_rows}
    prev_by_id = {r[1]: r[0] for r in prev_rows}

    for name, bot_id, _, _ in new_rows:
        if name in prev_by_name and prev_by_name[name] != bot_id:
            errors.append(
                f"name {name!r}: previous bot_id {prev_by_name[name]}, new {bot_id}"
            )
        if bot_id in prev_by_id and prev_by_id[bot_id] != name:
            errors.append(
                f"bot_id {bot_id}: previous name {prev_by_id[bot_id]!r}, new {name!r}"
            )
    return errors


def drift_verdict(new_rows, prev_rows, current_day):
    if not prev_rows:
        return "NOT EVALUABLE"
    prev_map = {r[0]: r for r in prev_rows}
    changes = []
    for name, bot_id, a, e in new_rows:
        if name in prev_map:
            prow = prev_map[name]
            if (a, e) != (prow[2], prow[3]):
                changes.append((name, prow[2], prow[3], a, e))
    if not changes:
        return "ZERO. Not one bot changed either toggle."
    lines = [f"{len(changes)} bot(s) changed toggle state vs the previous bundle:"]
    for name, pa, pe, na, ne in changes:
        lines.append(f"  {name}: AUTOS {pa}->{na}, EXITS {pe}->{ne}")
    return "\n".join(lines)


class BundleError(SystemExit):
    pass


def find_previous_bundle(captures_root, current_day):
    """Return the directory of the previous bundle (latest day < current_day), or None."""
    if not os.path.isdir(captures_root):
        return None
    candidates = []
    for entry in os.listdir(captures_root):
        p = os.path.join(captures_root, entry)
        if not os.path.isdir(p):
            continue
        tsvs = glob.glob(os.path.join(p, "02-roster-toggles-*.tsv"))
        if not tsvs:
            continue
        # Try to read the day from the first capture .txt inside the bundle.
        txts = glob.glob(os.path.join(p, "*.txt"))
        day = None
        for t in txts:
            if os.path.basename(t).startswith("SHA256"):
                continue
            try:
                with open(t, encoding="utf-8") as fo:
                    for line in fo:
                        m = CAPTURED_RE.match(line)
                        if m:
                            s = m.group(1).split(" (")[0].strip()
                            dt = datetime.datetime.strptime(s, "%a %b %d %Y %H:%M:%S GMT%z")
                            day = dt.strftime("%Y-%m-%d")
                            break
            except (OSError, ValueError):
                pass
            if day:
                break
        if day and day < current_day:
            candidates.append((day, p))
    if not candidates:
        return None
    # Most recent day before current.
    return max(candidates, key=lambda x: x[0])[1]


def bundle_files(bundle_dir):
    """Yield (relative path, absolute path) for every file under bundle_dir except .DS_Store and SHA256SUMS."""
    for dirpath, dirnames, filenames in os.walk(bundle_dir):
        for fn in filenames:
            if fn == ".DS_Store" or fn == "SHA256SUMS.txt":
                continue
            ap = os.path.join(dirpath, fn)
            rp = os.path.relpath(ap, bundle_dir)
            # Ensure POSIX separators for the checksum file.
            rp = rp.replace(os.sep, "/")
            yield rp, ap


def write_sha256sums(bundle_dir):
    path = os.path.join(bundle_dir, "SHA256SUMS.txt")
    items = sorted(bundle_files(bundle_dir))
    with open(path, "w", encoding="utf-8") as fo:
        for rp, ap in items:
            fo.write(f"{sha256(ap)}  ./{rp}\n")
    return path


def tsv_header(source_name, source_sha, n, day, prev_bundle, verdict, footer, account):
    lines = [
        f"# ROSTER + TOGGLE STATE — all {n} active bots, with bot IDs — {day}",
        f"# DERIVED FILE. Source of every field below: {source_name}",
        f"#   (sha256 {source_sha}), the /bots bookmarklet capture taken",
        f"#   {day} ET. Nothing here is typed from memory.",
        "#",
        "# METHOD:",
        "#   AUTOS / EXITS are the `title` ATTRIBUTE of the two <i class=\"... sticon\"> elements",
        "#   in each /bots row (S0b-3 fix v2.1):",
        "#       AUTOS : \"Scheduled automations are on|off\"",
        "#       EXITS : \"Exit Options for positions managed by this bot are on|off\"",
        "#   The capture emits those (bot_id, autos_title, exits_title) triples in /bots row",
        "#   order but WITHOUT the bot name. Names are the row names of the same capture's",
        f"#   list table, in the same order ({LIST_ROW_STRIDE}-line stride: 1 name + 18 values).",
        "#",
        "# JOIN PROOF:",
    ]
    if prev_bundle:
        lines.append(
            f"#   The (name, bot_id) pairs below are checked against the previous bundle"
        )
        lines.append(f"#   {prev_bundle} before this bundle is accepted.")
    else:
        lines.append("#   No previous bundle available for cross-check.")
    lines.append("#")
    if footer:
        lines.append(f"# FOOTER, verbatim: {footer!r}")
    if account:
        lines.append(f"# Account header (capture text): {account}")
    lines.append("#")
    lines.append(f"# DRIFT VERDICT: {verdict}")
    lines.append("#")
    lines.append("# bot_name\tbot_id\tAUTOS\tEXITS")
    return "\n".join(lines)


def tsv_body(rows):
    return "\n".join("\t".join(r) for r in rows) + "\n"


def write_tsv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as fo:
        fo.write(header)
        fo.write("\n")
        fo.write(tsv_body(rows))


def write_readme(bundle_dir, day, capture_dt, n, rows, source_name, source_sha,
                 tsv_name, tsv_sha, prev_bundle, verdict, footer,
                 screenshot_files):
    autos_on = sum(1 for r in rows if r[2] == "ON")
    exits_on = sum(1 for r in rows if r[3] == "ON")
    readme = os.path.join(bundle_dir, "README.md")

    lines = [
        f"# Capture bundle — {day} roster + toggle state",
        "",
        f"Purpose: the end-of-day `/bots` roster capture for trading day **{day}**.",
        f"Captured **{capture_dt}**.",
        "",
        "## Files",
        "",
        "| file | sha256 | what it is |",
        "|---|---|---|",
    ]
    lines.append(
        f"| `{source_name}` | `{source_sha}` | RAW bookmarklet capture, unmodified. "
        f"{n} list rows + the {n}-row `i.sticon[title]` AUTOS/EXITS block (S0b-3 fix v2.1). |"
    )
    lines.append(
        f"| `{tsv_name}` | `{tsv_sha}` | DERIVED join into `bot_name / bot_id / AUTOS / EXITS`. |"
    )
    for sn, ss in screenshot_files:
        lines.append(
            f"| `screenshots/{sn}` | `{ss}` | Screenshot of the `/bots` roster. |"
        )
    lines.append("")
    lines.append("## Closing state")
    lines.append("")
    if footer:
        lines.append(f"- footer, verbatim: `{footer}`")
    lines.append(f"- rows parsed: {n}")
    lines.append(f"- **AUTOMATIONS ON: {autos_on} of {n}**")
    lines.append(f"- **EXIT OPTIONS ON: {exits_on} of {n}**")
    lines.append(f"- **DRIFT vs previous bundle:** {verdict}")
    lines.append("")

    if prev_bundle:
        lines.append(f"Cross-checked against: `{prev_bundle}`")
    else:
        lines.append("No previous bundle supplied; drift is **NOT EVALUABLE**.")
    lines.append("")

    with open(readme, "w", encoding="utf-8") as fo:
        fo.write("\n".join(lines))
    return readme


def build_bundle(txt_path, screenshots, out_root, prev_bundle=None, force=False):
    """Parse `txt_path` and write a new bundle under `out_root/<day>-roster/`."""
    if not os.path.isfile(txt_path):
        raise BundleError(f"FATAL: capture file not found: {txt_path}")

    with open(txt_path, encoding="utf-8") as fo:
        raw = fo.read()
    source_sha = sha256(txt_path)
    lines = raw.splitlines()

    # ET day from the capture's own header.
    captured_dt = None
    captured_line = None
    for line in lines:
        m = CAPTURED_RE.match(line)
        if m:
            captured_line = line
            captured_dt = parse_captured(line)
            break
    if captured_line is None:
        raise BundleError("FATAL: capture has no 'captured:' header line")
    if captured_dt is None:
        raise BundleError(f"FATAL: cannot parse 'captured:' line: {captured_line!r}")

    day = captured_dt.strftime("%Y-%m-%d")
    time_str = captured_dt.strftime("%H%M%S")
    title = title_from_text(lines)
    title_slug = slugify(title)

    # Parse the two independent surfaces.
    names = parse_list_table(lines)
    triples = parse_title_block(lines)
    config_map = load_bots_config(CONFIG)
    rows = derive_rows(names, triples, config_map)
    n = len(rows)

    # Locate previous bundle if not supplied.
    if prev_bundle is None:
        prev_bundle = find_previous_bundle(out_root, day)

    prev_rows = []
    if prev_bundle:
        tsvs = glob.glob(os.path.join(prev_bundle, "02-roster-toggles-*.tsv"))
        if not tsvs:
            raise BundleError(f"FATAL: previous bundle has no 02-roster-toggles-*.tsv: {prev_bundle}")
        prev_rows = load_tsv_rows(tsvs[0])

    # Fatal cross-check.
    errors = cross_check(rows, prev_rows)
    if errors:
        msg = "\n".join(["FATAL: pairing mismatch against previous bundle:"] + errors)
        raise BundleError(msg)

    verdict = drift_verdict(rows, prev_rows, day)

    # Footer and account header for documentation.
    footer = None
    for line in lines:
        m = FOOTER_RE.match(line)
        if m:
            footer = line
            break
    account = None
    for i, line in enumerate(lines):
        if line == "TOTAL P/L":
            # The first TOTAL P/L is the account header; collect the next few fields.
            parts = [line]
            for j in range(i + 1, min(i + 5, len(lines))):
                parts.append(lines[j])
            account = " ".join(parts)
            break

    bundle_dir = os.path.join(out_root, f"{day}-roster")
    if os.path.isdir(bundle_dir):
        if not force:
            raise BundleError(
                f"FATAL: bundle already exists at {bundle_dir}; "
                f"use --force to overwrite, or choose a different --out-root"
            )
    os.makedirs(bundle_dir, exist_ok=True)
    os.makedirs(os.path.join(bundle_dir, "screenshots"), exist_ok=True)

    # 01: rename the raw capture.
    raw_name = f"01-bots-roster-{title_slug}-{day}-{time_str}.txt"
    raw_path = os.path.join(bundle_dir, raw_name)
    shutil.copy2(txt_path, raw_path)

    # 02: derived TSV.
    tsv_name = f"02-roster-toggles-{n}-{day}.tsv"
    tsv_path = os.path.join(bundle_dir, tsv_name)
    header = tsv_header(
        source_name=raw_name,
        source_sha=source_sha,
        n=n,
        day=day,
        prev_bundle=prev_bundle,
        verdict=verdict,
        footer=footer,
        account=account,
    )
    write_tsv(tsv_path, header, rows)
    tsv_sha = sha256(tsv_path)

    # Screenshots: numbered under screenshots/.
    screenshot_files = []
    for i, spath in enumerate(screenshots, start=1):
        if not os.path.isfile(spath):
            raise BundleError(f"FATAL: screenshot not found: {spath}")
        base = os.path.basename(spath)
        stem, ext = os.path.splitext(base)
        stem = slugify(stem) or "screenshot"
        shot_name = f"{i:02d}-bots-roster-{stem}-{day}-{time_str}{ext}"
        # If the file already has a descriptive leading number, keep it simple.
        shot_path = os.path.join(bundle_dir, "screenshots", shot_name)
        shutil.copy2(spath, shot_path)
        screenshot_files.append((shot_name, sha256(shot_path)))

    # README and SHA256SUMS.
    write_readme(
        bundle_dir, day, captured_dt, n, rows,
        source_name=raw_name,
        source_sha=source_sha,
        tsv_name=tsv_name,
        tsv_sha=tsv_sha,
        prev_bundle=prev_bundle,
        verdict=verdict,
        footer=footer,
        screenshot_files=screenshot_files,
    )
    write_sha256sums(bundle_dir)

    return bundle_dir


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("txt", nargs="?", help="/bots bookmarklet .txt capture")
    ap.add_argument("screenshots", nargs="*", help="optional screenshot files")
    ap.add_argument("--prev-bundle", default=None,
                    help="previous bundle directory for the (name, bot_id) cross-check")
    ap.add_argument("--out-root", default=CAPTURES,
                    help=f"parent directory for data/<day>-roster (default: {CAPTURES})")
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing bundle directory")
    ap.add_argument("--selftest", action="store_true", help="run the self-test")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    if not args.txt:
        ap.error("argument txt is required unless --selftest is given")

    try:
        bundle = build_bundle(
            args.txt, args.screenshots, args.out_root,
            prev_bundle=args.prev_bundle, force=args.force,
        )
    except BundleError as e:
        sys.stderr.write(str(e) + "\n")
        sys.exit(1)

    print(f"capture_bundle.py: wrote {bundle}")
    return 0


# ===========================================================================
# SELF-TEST — fixtures + named check matrix, run with --selftest
# ===========================================================================
def _make_fixture(tmp, name, captured, bots, with_title_block=True, mutate=None):
    """Write a synthetic /bots capture .txt and return its path.

    `bots` is a list of (bot_name, bot_id, autos_title, exits_title).
    `mutate` is an optional callable that receives the assembled text and can
    alter it (used to inject a shifted row for the red-once test).
    """
    os.makedirs(tmp, exist_ok=True)
    path = os.path.join(tmp, f"{name}.txt")
    # Build a plausible list table: 1 name + 18 values per bot.
    list_rows = []
    for bot_name, _, _, _ in bots:
        list_rows.append(bot_name)
        list_rows.extend(["--"] * 18)

    footer = f"{len(bots)} active bots • 0 left in your plan • Upgrade"
    text = [
        "# Recent_Activity",
        "https://app.optionalpha.com/bots",
        f"captured: {captured}",
        "",
        "7:57PM",
        "Bots",
        "TOTAL P/L",
        "-$100",
        "ICON",
        "BOT",
        "30D",
        "TOTAL P/L",
        "RETURN %",
        "CLOSED P/L",
        "CLOSED %",
        "CHANGE",
        "CHANGE %",
        "POS",
        "RISK",
        "ALLOCATION",
        "WIN RATE",
        "BETA WEIGHT",
        "BETA EXPOSURE",
        "AVG P/L",
        "AVG WIN",
        "AVG LOSS",
        "P FACTOR",
        "STREAK",
        "CLOSED",
        "AUTOS",
        "EXITS",
    ]
    text.extend(list_rows)
    text.append(footer)
    if with_title_block:
        text.append("")
        text.append("# AUTOS/EXITS -- i.sticon title attribute. bot_id\tautos_title\texits_title")
        for _, bot_id, autos, exits in bots:
            text.append(f"{bot_id}\t{autos}\t{exits}")

    raw = "\n".join(text)
    if mutate:
        raw = mutate(raw)
    with open(path, "w", encoding="utf-8") as fo:
        fo.write(raw)
    return path


def _make_prev_bundle(tmp, day, bots):
    """Write a previous bundle directory with a 02-roster-toggles-*.tsv."""
    bundle = os.path.join(tmp, f"{day}-prev")
    os.makedirs(bundle, exist_ok=True)
    tsv = os.path.join(bundle, f"02-roster-toggles-{len(bots)}-{day}.tsv")
    with open(tsv, "w", encoding="utf-8", newline="") as fo:
        fo.write("# bot_name\tbot_id\tAUTOS\tEXITS\n")
        for name, bid, a, e in bots:
            fo.write(f"{name}\t{bid}\t{a}\t{e}\n")
    return bundle


def _make_config(tmp, mapping):
    """Write a synthetic data/bots_config_v2.csv with leading comment lines."""
    path = os.path.join(tmp, "bots_config_v2.csv")
    with open(path, "w", encoding="utf-8", newline="") as fo:
        fo.write("# comment line 1\n")
        fo.write("# comment line 2\n")
        fo.write("object_kind,name,oa_id,version\n")
        for name, bot_id in mapping.items():
            fo.write(f"bot,{name},{bot_id},1\n")
    return path


def selftest():
    import shutil

    fails, results = 0, []

    def check(name, got, want):
        nonlocal fails
        ok = got == want
        fails += not ok
        results.append((ok, name, got, want))
        return ok

    repo_captures = os.path.join(ROOT, "data", "captures")
    repo_before = set(os.listdir(repo_captures)) if os.path.isdir(repo_captures) else set()

    tmp = tempfile.mkdtemp(prefix="cap-bundle-selftest-")
    try:
        # A small synthetic fleet.  One bot (Gamma) is in bots_config_v2;
        # Alpha and Beta are not, so their names come from the list table.
        bots = [
            ("Alpha-Bot", "BOTaa111", "Scheduled automations are on",
             "Exit Options for positions managed by this bot are on"),
            ("Beta-Bot", "BOTbb222", "Scheduled automations are off",
             "Exit Options for positions managed by this bot are off"),
            ("Gamma-Bot", "BOTcc333", "Scheduled automations are on",
             "Exit Options for positions managed by this bot are off"),
        ]
        captured = "Mon Aug 18 2026 19:57:13 GMT-0400 (Eastern Daylight Time)"

        # Point the script at the synthetic config for the selftest.
        config_path = _make_config(tmp, {"Gamma-Bot": "BOTcc333"})
        # (We monkey-patch the global CONFIG inside the local fixture where needed.)

        # ---- D1: day and time are derived from the capture header, not filename
        txt = _make_fixture(tmp, "capture", captured, bots)
        with open(txt) as fo:
            lines = fo.read().splitlines()
        cap_line = [ln for ln in lines if ln.startswith("captured:")][0]
        dt = parse_captured(cap_line)
        check("D1  day is derived from the captured: header", dt.strftime("%Y-%m-%d"), "2026-08-18")

        # ---- J1: names come from the list table in row order, toggles from title block
        prev_bundle = _make_prev_bundle(tmp, "2026-08-17", bots)
        out = os.path.join(tmp, "out")
        os.makedirs(out, exist_ok=True)
        # Save the real CONFIG and use the fixture one.
        global CONFIG
        keep_config = CONFIG
        CONFIG = config_path
        bundle = build_bundle(txt, [], out, prev_bundle=prev_bundle, force=True)
        tsv = os.path.join(bundle, "02-roster-toggles-3-2026-08-18.tsv")
        check("J1a bundle directory is data/captures/<day>-roster", os.path.basename(bundle), "2026-08-18-roster")
        check("J1b raw file is renamed 01-bots-roster-...", os.path.exists(os.path.join(bundle, "01-bots-roster-recent-activity-2026-08-18-195713.txt")), True)
        check("J1c TSV file exists", os.path.exists(tsv), True)
        rows = load_tsv_rows(tsv)
        check("J1d TSV has 3 data rows", [r[:2] for r in rows], [("Alpha-Bot", "BOTaa111"), ("Beta-Bot", "BOTbb222"), ("Gamma-Bot", "BOTcc333")])
        check("J1e TSTATES are ON/OFF", [(r[2], r[3]) for r in rows], [("ON", "ON"), ("OFF", "OFF"), ("ON", "OFF")])

        # ---- D3: README and SHA256SUMS are written
        check("D3a README.md written", os.path.exists(os.path.join(bundle, "README.md")), True)
        check("D3b SHA256SUMS.txt written", os.path.exists(os.path.join(bundle, "SHA256SUMS.txt")), True)

        # ---- D4: SHA256SUMS excludes itself and .DS_Store
        sums = open(os.path.join(bundle, "SHA256SUMS.txt")).read()
        check("D4a SHA256SUMS does not list itself", "SHA256SUMS.txt" in sums, False)
        # Inject a .DS_Store and recompute to test exclusion.
        ds = os.path.join(bundle, ".DS_Store")
        with open(ds, "w") as fo:
            fo.write("junk")
        write_sha256sums(bundle)
        sums = open(os.path.join(bundle, "SHA256SUMS.txt")).read()
        check("D4b SHA256SUMS excludes .DS_Store", ".DS_Store" in sums, False)
        os.remove(ds)

        # ---- D5: screenshots are placed under <bundle>/screenshots/ with numbered names
        shot = os.path.join(tmp, "roster.png")
        with open(shot, "w") as fo:
            fo.write("png-bytes")
        bundle2 = build_bundle(txt, [shot], out, prev_bundle=prev_bundle, force=True)
        shots = os.listdir(os.path.join(bundle2, "screenshots"))
        check("D5 screenshot renamed and placed in screenshots/", shots, ["01-bots-roster-roster-2026-08-18-195713.png"])

        # ---- C1: cross-check passes when previous bundle matches
        # Already exercised above; this is the explicit predicate.
        rows = load_tsv_rows(tsv)
        check("C1  (name, bot_id) pairs match the previous bundle", [r[:2] for r in rows], [("Alpha-Bot", "BOTaa111"), ("Beta-Bot", "BOTbb222"), ("Gamma-Bot", "BOTcc333")])

        # ---- C2: ONE SHIFTED ROW makes the cross-check fail (red once)
        shifted_bots = list(bots)
        # Swap the bot_ids of the first and second bots => Gamma stays correct.
        shifted_bots[0] = ("Alpha-Bot", "BOTbb222", bots[0][2], bots[0][3])
        shifted_bots[1] = ("Beta-Bot", "BOTaa111", bots[1][2], bots[1][3])
        shifted_txt = _make_fixture(tmp, "shifted", captured, shifted_bots)
        try:
            build_bundle(shifted_txt, [], out, prev_bundle=prev_bundle, force=True)
            c2_got = "NO ERROR"
        except BundleError as e:
            c2_got = str(e) if str(e) else "BUNDLE_ERROR"
        check("C2  shifted first row is FATAL", c2_got.startswith("FATAL:"), True)

        # ---- C3: a config mismatch is also fatal (red once)
        bad_config_bots = list(bots)
        # Make the list-table name for Gamma disagree with the config record.
        bad_config_bots[2] = ("Wrong-Name", "BOTcc333", bots[2][2], bots[2][3])
        bad_txt = _make_fixture(tmp, "bad-config", captured, bad_config_bots)
        try:
            build_bundle(bad_txt, [], out, prev_bundle=prev_bundle, force=True)
            c3_got = "NO ERROR"
        except BundleError as e:
            c3_got = str(e) if str(e) else "BUNDLE_ERROR"
        check("C3  list-table name / config name mismatch is FATAL", c3_got.startswith("FATAL:"), True)

        # ---- C4: missing captured: header is fatal (red once)
        no_cap = os.path.join(tmp, "no-cap.txt")
        with open(no_cap, "w") as fo:
            fo.write("# Bots\nhttps://x\n")
        try:
            build_bundle(no_cap, [], out, prev_bundle=prev_bundle, force=True)
            c4_got = "NO ERROR"
        except BundleError as e:
            c4_got = str(e) if str(e) else "BUNDLE_ERROR"
        check("C4  missing captured: header is FATAL", c4_got.startswith("FATAL:"), True)

        # ---- D6: with no previous bundle the drift verdict is exactly NOT EVALUABLE
        bundle3 = build_bundle(txt, [], out, prev_bundle=None, force=True)
        readme = open(os.path.join(bundle3, "README.md")).read()
        check("D6  no previous bundle -> drift verdict 'NOT EVALUABLE'", "NOT EVALUABLE" in readme, True)

        # ---- C5: restored fixture with no mutation passes cross-check again
        bundle4 = build_bundle(txt, [], out, prev_bundle=prev_bundle, force=True)
        tsv4 = os.path.join(bundle4, "02-roster-toggles-3-2026-08-18.tsv")
        rows4 = load_tsv_rows(tsv4)
        check("C5  restored fixture still passes cross-check", [r[:2] for r in rows4], [("Alpha-Bot", "BOTaa111"), ("Beta-Bot", "BOTbb222"), ("Gamma-Bot", "BOTcc333")])

    finally:
        if 'keep_config' in locals():
            CONFIG = keep_config
        shutil.rmtree(tmp, ignore_errors=True)

    # The selftest must not have touched the repo's data/captures/ tree.
    repo_after = set(os.listdir(repo_captures)) if os.path.isdir(repo_captures) else set()
    check("Z1  selftest left repo data/captures/ untouched", repo_after, repo_before)

    print("SELF-TEST — capture_bundle.py")
    print("=" * 74)
    for ok, name, got, want in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
        if not ok:
            print(f"        got  {got!r}\n        want {want!r}")
    print("-" * 74)
    print(f"{len(results) - fails}/{len(results)} passed")
    return 1 if fails else 0


if __name__ == "__main__":
    main()
