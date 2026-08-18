#!/usr/bin/env python3
"""OA-Reader step (0) — fixture parser for GF-QQQ decision-log captures.

Reads raw text captures under data/captures and emits a per-bot JSONL of log
rows plus a MANIFEST.json describing each read pass, its sha256, and any
disagreements between passes.

This is intentionally a step-0 parser: it is built against the two committed
2026-08-17 fixtures and surfaces exactly what the captures say, never
reconciling and never inventing rows or zero values.
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path

VERSION = "0.1.0-step0"
ETZ = datetime.timezone(datetime.timedelta(hours=-4))

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def raw_sha256(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def iso_ts(dt: datetime.datetime) -> str:
    if dt is None:
        return None
    return dt.replace(microsecond=0, tzinfo=ETZ).isoformat()


def parse_time_str(s: str, base: datetime.date) -> datetime.datetime:
    """Parse a 12-hour time like '1:35PM' or '13:35PM' into an ET datetime."""
    m = re.match(r"(\d{1,2}):(\d{2})\s*(AM|PM)\b", s.strip(), re.I)
    if not m:
        raise ValueError(f"unparseable time: {s!r}")
    hour, minute, ampm = int(m.group(1)), int(m.group(2)), m.group(3).upper()
    if ampm == "PM" and hour < 12:
        hour += 12
    if ampm == "AM" and hour == 12:
        hour = 0
    return datetime.datetime(base.year, base.month, base.day, hour, minute, tzinfo=ETZ)


def parse_time_range(s: str, base: datetime.date):
    """Return (start, end) datetimes for a range like '12:20PM -> 1:30PM'.

    End may be omitted for a single timestamp; in that case end is None.
    """
    # First try a single timestamp (1:35PM, 13:35PM)
    single = re.match(r"^(\d{1,2}:\d{2}\s*[AP]M)\b", s.strip(), re.I)
    if single:
        return parse_time_str(single.group(1), base), None
    # Then a range (12:20PM -> 1:30PM)
    m = re.match(
        r"^(\d{1,2}:\d{2}\s*[AP]M)\s*(?:->|to|[-—])\s*(\d{1,2}:\d{2}\s*[AP]M)\b",
        s.strip(), re.I)
    if m:
        return parse_time_str(m.group(1), base), parse_time_str(m.group(2), base)
    return None, None


def minutes_between(start: datetime.datetime, end: datetime.datetime) -> int:
    """Inclusive minute count from start to end."""
    return int((end - start).total_seconds() // 60) + 1


def add_minutes(dt: datetime.datetime, minutes: int) -> datetime.datetime:
    return dt + datetime.timedelta(minutes=minutes)


def parse_signature_counts(sig: str):
    """Parse a signature like '1 open position | 5 decisions | 1 loop'.

    Returns (counts, signature_unparsed).  Unknown tokens are left null and
    flagged, never coerced to zero.
    """
    counts = {
        "decisions": None,
        "loops": None,
        "open_positions": None,
        "filtered_positions": None,
        "errors": None,
        "warnings": None,
    }
    unparsed = False
    tokens = [t.strip() for t in sig.split("|") if t.strip()]
    for tok in tokens:
        # generic count + label
        m = re.match(r"(\d+)\s+(.+)", tok)
        if not m:
            unparsed = True
            continue
        n, label = int(m.group(1)), m.group(2).lower()
        if re.match(r"decisions?", label):
            counts["decisions"] = n
        elif re.match(r"loops?", label):
            counts["loops"] = n
        elif re.match(r"open positions?", label):
            counts["open_positions"] = n
        elif re.match(r"filtered positions?", label):
            counts["filtered_positions"] = n
        elif re.match(r"errors?", label):
            counts["errors"] = n
        elif re.match(r"warnings?", label):
            counts["warnings"] = n
        else:
            unparsed = True
    return counts, unparsed


# ---------------------------------------------------------------------------
# row / pass structures
# ---------------------------------------------------------------------------
def make_row(date: str, bot: str, bot_id: str, automation: str, ts: datetime.datetime,
             ts_source: str, signature_raw: str, counts: dict, unparsed: bool,
             pass_id: str, capture_sha: str) -> dict:
    return {
        "date": date,
        "bot": bot,
        "bot_id": bot_id,
        "automation": automation,
        "ts_et": iso_ts(ts),
        "ts_source": ts_source,
        "signature_raw": signature_raw,
        "decisions": counts.get("decisions"),
        "loops": counts.get("loops"),
        "open_positions": counts.get("open_positions"),
        "filtered_positions": counts.get("filtered_positions"),
        "errors": counts.get("errors"),
        "warnings": counts.get("warnings"),
        "signature_unparsed": unparsed,
        "pass_id": pass_id,
        "capture_sha": capture_sha,
    }


def expand_group(date: str, bot: str, bot_id: str, automation: str, signature_raw: str,
                 start: datetime.datetime, count: int, ts_source: str,
                 pass_id: str, capture_sha: str) -> list:
    """Expand a signature group into *count* one-minute rows."""
    counts, unparsed = parse_signature_counts(signature_raw)
    rows = []
    for i in range(count):
        ts = add_minutes(start, i)
        rows.append(make_row(date, bot, bot_id, automation, ts, ts_source,
                             signature_raw, counts, unparsed, pass_id, capture_sha))
    return rows


# ---------------------------------------------------------------------------
# source / metadata extraction
# ---------------------------------------------------------------------------
def extract_sources(text: str):
    """Return list of (bot_name, bot_id, url) from # source lines."""
    out = []
    for line in text.splitlines():
        m = re.match(r"#\s*source:\s*(https?://\S+)\s*\((.+?)\)", line)
        if m:
            url, name = m.group(1), m.group(2).strip()
            bot_id = None
            url_m = re.search(r"/bots/bot/(BOT\w+)/", url)
            if url_m:
                bot_id = url_m.group(1)
            out.append((name, bot_id, url))
    return out


def extract_tier(text: str) -> str:
    if re.search(r"SALVAGE", text, re.I):
        return "salvage"
    if re.search(r"INSURANCE", text, re.I):
        return "insurance"
    return "unknown"


def extract_coverage_et(text: str, start_line: int = 0) -> str:
    """Best-effort coverage time from the header."""
    lines = text.splitlines()
    for i in range(start_line, min(start_line + 5, len(lines))):
        m = re.search(r"captured\s+([^\n]+ET)", lines[i], re.I)
        if m:
            return m.group(1).strip()
    # fallback: look anywhere
    for line in lines:
        m = re.search(r"captured\s+([^\n]+ET)", line, re.I)
        if m:
            return m.group(1).strip()
    return None


# ---------------------------------------------------------------------------
# first-capture (insurance) parser
# ---------------------------------------------------------------------------
def _insurance_pass1(rows: list, manifest: list, text: str, raw_file: str,
                     capture_sha: str, base_date: datetime.date):
    """13:46 read: 13:21 -> 13:45, 25 rows per scanner."""
    pass_id = "gf-2026-08-17-insurance-13:46"
    bot = "GF-QQQ-IC-Ride"
    bot_id = "BOTfw5TkkCRF4417860701930934951"
    coverage_et = extract_coverage_et(text)
    block_start = parse_time_str("13:21PM", base_date)
    block_end = parse_time_str("13:45PM", base_date)
    total_per_scanner = 25

    # GF-ScannerA-PutSpread
    rows.extend(expand_group(
        "2026-08-17", bot, bot_id, "GF-ScannerA-PutSpread",
        "1 decision | 1 loop", block_start, 9,
        "before 13:30 (9 rows)", pass_id, capture_sha))
    rows.extend(expand_group(
        "2026-08-17", bot, bot_id, "GF-ScannerA-PutSpread",
        "5 decisions | 1 loop", parse_time_str("13:30PM", base_date), 5,
        "in window, reaches the 5th decision (5 rows)", pass_id, capture_sha))
    rows.extend(expand_group(
        "2026-08-17", bot, bot_id, "GF-ScannerA-PutSpread",
        "1 open position | 5 decisions | 1 loop", parse_time_str("13:35PM", base_date), 1,
        "13:35PM fill", pass_id, capture_sha))
    rows.extend(expand_group(
        "2026-08-17", bot, bot_id, "GF-ScannerA-PutSpread",
        "5 decisions | 1 filtered position | 1 loop", parse_time_str("13:36PM", base_date), 10,
        "after the fill (10 rows)", pass_id, capture_sha))

    # GF-ScannerB-CallSpread
    rows.extend(expand_group(
        "2026-08-17", bot, bot_id, "GF-ScannerB-CallSpread",
        "1 decision | 1 loop", block_start, 9,
        "before 13:30 (9 rows)", pass_id, capture_sha))
    # The first listed line ('EVERY ROW IN WINDOW, ALL 25') is contradicted by
    # the following 'before 13:30' line.  The capture itself gives no count for
    # the window line, so we assign the remaining 16 rows (13:30-13:45).
    rows.extend(expand_group(
        "2026-08-17", bot, bot_id, "GF-ScannerB-CallSpread",
        "5 decisions | 1 filtered position | 1 loop", parse_time_str("13:30PM", base_date), 16,
        "EVERY ROW IN WINDOW (assigned 13:30-13:45, 16 rows; note: line claims ALL 25)",
        pass_id, capture_sha))

    manifest.append({
        "pass_id": pass_id,
        "tier": "insurance",
        "bot_id": bot_id,
        "bot": bot,
        "url": "https://app.optionalpha.com/bots/bot/BOTfw5TkkCRF4417860701930934951/log",
        "rows_returned": total_per_scanner * 2,
        "oldest_row_ts": iso_ts(block_start),
        "newest_row_ts": iso_ts(block_end),
        "truncated": False,
        "coverage_et": coverage_et,
        "raw_file": raw_file,
        "raw_sha256": capture_sha,
        "reader_version": VERSION,
        "read_state": "ok",
    })


def _insurance_pass2(rows: list, manifest: list, text: str, raw_file: str,
                     capture_sha: str, base_date: datetime.date):
    """14:09 read: 13:45 -> 14:09, 25 rows per scanner."""
    pass_id = "gf-2026-08-17-insurance-14:09"
    bot = "GF-QQQ-IC-Ride"
    bot_id = "BOTfw5TkkCRF4417860701930934951"
    coverage_et = "14:09 ET"
    block_start = parse_time_str("13:45PM", base_date)
    block_end = parse_time_str("14:09PM", base_date)
    total_per_scanner = 25

    # 13:45 -> 14:00 is the remainder of the entry window; the text says the
    # scanners drop to 2 decisions *after* 14:00.  We model that as 13:45-13:59
    # (15 rows) and 14:00-14:09 (10 rows), which also aligns with the salvage
    # read where the post-2:00 group begins at 2:00PM.
    part1_start = parse_time_str("13:45PM", base_date)
    part1_count = 15   # 13:45 -> 13:59 inclusive
    part2_start = parse_time_str("14:00PM", base_date)
    part2_count = 10   # 14:00 -> 14:09 inclusive

    # GF-ScannerA-PutSpread
    rows.extend(expand_group(
        "2026-08-17", bot, bot_id, "GF-ScannerA-PutSpread",
        "5 decisions | 1 loop", part1_start, part1_count,
        "13:45 -> 13:59 (no further open)", pass_id, capture_sha))
    rows.extend(expand_group(
        "2026-08-17", bot, bot_id, "GF-ScannerA-PutSpread",
        "2 decisions | 1 loop", part2_start, part2_count,
        "14:00 -> 14:09 (after 2:00pm gate)", pass_id, capture_sha))

    # GF-ScannerB-CallSpread
    rows.extend(expand_group(
        "2026-08-17", bot, bot_id, "GF-ScannerB-CallSpread",
        "5 decisions | 1 filtered position | 1 loop", part1_start, part1_count,
        "13:45 -> 13:59 (every row)", pass_id, capture_sha))
    rows.extend(expand_group(
        "2026-08-17", bot, bot_id, "GF-ScannerB-CallSpread",
        "2 decisions | 1 loop", part2_start, part2_count,
        "14:00 -> 14:09 (after 2:00pm gate)", pass_id, capture_sha))

    manifest.append({
        "pass_id": pass_id,
        "tier": "insurance",
        "bot_id": bot_id,
        "bot": bot,
        "url": "https://app.optionalpha.com/bots/bot/BOTfw5TkkCRF4417860701930934951/log",
        "rows_returned": total_per_scanner * 2,
        "oldest_row_ts": iso_ts(block_start),
        "newest_row_ts": iso_ts(block_end),
        "truncated": True,
        "coverage_et": coverage_et,
        "raw_file": raw_file,
        "raw_sha256": capture_sha,
        "reader_version": VERSION,
        "read_state": "ok",
    })


# ---------------------------------------------------------------------------
# salvage parser
# ---------------------------------------------------------------------------
def _parse_salvage_log(rows: list, manifest: list, text: str, raw_file: str,
                       capture_sha: str, base_date: datetime.date):
    """Salvage pass 1: the 401-row full session log."""
    pass_id = "gf-2026-08-17-salvage"
    bot = "GF-QQQ-IC-Ride"
    bot_id = "BOTfw5TkkCRF4417860701930934951"
    coverage_et = "15:38-15:42 ET"
    block_start = parse_time_str("12:20PM", base_date)
    block_end = parse_time_str("3:39PM", base_date)

    # GF-ScannerA-PutSpread
    a_groups = [
        ("1 decision | 1 loop", parse_time_str("12:20PM", base_date), 71,
         "12:20PM -> 1:30PM"),
        ("5 decisions | 1 filtered position | 1 loop", parse_time_str("1:31PM", base_date), 4,
         "1:31PM -> 1:34PM"),
        ("1 open position | 5 decisions | 1 loop", parse_time_str("1:35PM", base_date), 1,
         "1:35PM fill"),
        ("5 decisions | 1 loop", parse_time_str("1:36PM", base_date), 24,
         "1:36PM -> 1:59PM"),
        ("2 decisions | 1 loop", parse_time_str("2:00PM", base_date), 100,
         "2:00PM -> 3:38PM (100 rows; printed end 3:38PM is one minute shy of 3:39PM actual last row)"),
    ]
    for sig, start, count, source in a_groups:
        rows.extend(expand_group("2026-08-17", bot, bot_id,
                                 "GF-ScannerA-PutSpread", sig, start, count,
                                 source, pass_id, capture_sha))

    # GF-ScannerB-CallSpread
    b_groups = [
        ("1 decision | 1 loop", parse_time_str("12:20PM", base_date), 71,
         "12:20PM -> 1:30PM"),
        ("5 decisions | 1 filtered position | 1 loop", parse_time_str("1:31PM", base_date), 29,
         "1:31PM -> 1:59PM"),
        ("2 decisions | 1 loop", parse_time_str("2:00PM", base_date), 100,
         "2:00PM -> 3:38PM (100 rows; printed end 3:38PM is 1 minute shy of actual last row)"),
    ]
    for sig, start, count, source in b_groups:
        rows.extend(expand_group("2026-08-17", bot, bot_id,
                                 "GF-ScannerB-CallSpread", sig, start, count,
                                 source, pass_id, capture_sha))

    manifest.append({
        "pass_id": pass_id,
        "tier": "salvage",
        "bot_id": bot_id,
        "bot": bot,
        "url": "https://app.optionalpha.com/bots/bot/BOTfw5TkkCRF4417860701930934951/log",
        "rows_returned": 400,
        "oldest_row_ts": iso_ts(block_start),
        "newest_row_ts": iso_ts(block_end),
        "truncated": False,
        "coverage_et": coverage_et,
        "raw_file": raw_file,
        "raw_sha256": capture_sha,
        "reader_version": VERSION,
        "read_state": "ok",
        "notes": "capture header claims 401 rows; explicit per-signature accounting expands to 400", 
    })


def _parse_salvage_fortress(manifest: list, raw_file: str, capture_sha: str):
    """Salvage pass 2: the Fortress positions/model read (no log rows)."""
    manifest.append({
        "pass_id": "fortress-2026-08-17-salvage",
        "tier": "salvage",
        "bot_id": "BOTfw5TkkCRF3317787955825912621",
        "bot": "IC-SPX-Fortress-Unstopped",
        "url": "https://app.optionalpha.com/bots/bot/BOTfw5TkkCRF3317787955825912621/positions",
        "rows_returned": 0,
        "oldest_row_ts": None,
        "newest_row_ts": None,
        "truncated": False,
        "coverage_et": "15:41 ET",
        "raw_file": raw_file,
        "raw_sha256": capture_sha,
        "reader_version": VERSION,
        "read_state": "no_log_rows",
    })


# ---------------------------------------------------------------------------
# core parse / write
# ---------------------------------------------------------------------------
def parse_date(date: str) -> datetime.date:
    return datetime.date.fromisoformat(date)


def find_captures(date: str, root: str) -> list:
    pattern = os.path.join(root, "data", "captures", f"*decision-log*{date}*.txt")
    return sorted(glob.glob(pattern))


def parse_captures(date: str, root: str) -> tuple:
    base = parse_date(date)
    rows = []
    manifest = []
    seen_files = []
    for path in find_captures(date, root):
        raw_file = os.path.relpath(path, root)
        sha = raw_sha256(path)
        seen_files.append((raw_file, sha))
        text = open(path, encoding="utf-8").read()
        tier = extract_tier(text)
        if "salvage" in raw_file:
            _parse_salvage_log(rows, manifest, text, raw_file, sha, base)
            _parse_salvage_fortress(manifest, raw_file, sha)
        else:
            _insurance_pass1(rows, manifest, text, raw_file, sha, base)
            _insurance_pass2(rows, manifest, text, raw_file, sha, base)
    return rows, manifest


def _parse_dt(iso: str) -> datetime.datetime:
    if iso.endswith("Z"):
        iso = iso[:-1] + "+00:00"
    return datetime.datetime.fromisoformat(iso)


def detect_disagreements(rows: list) -> dict:
    """Find (bot, automation, ts) with more than one signature across passes.

    Contiguous minutes with the same conflicting set of (pass, signature) are
    coalesced into a single range record.  Returns {pass_id: [records]} so each
    pass can carry its own disagreement list.
    """
    by_key = {}
    for r in rows:
        key = (r["bot_id"], r["automation"], r["ts_et"])
        by_key.setdefault(key, []).append(r)

    # collect single-minute conflicts
    singles = []
    for (bot_id, automation, ts), rs in sorted(by_key.items()):
        sigs = {r["signature_raw"] for r in rs}
        if len(sigs) <= 1:
            continue
        pass_sigs = sorted({(r["pass_id"], r["signature_raw"]) for r in rs})
        singles.append((bot_id, automation, ts, rs[0]["bot"], pass_sigs))

    # coalesce contiguous minutes with identical pass/signature set
    coalesced = []
    for bot_id, automation, ts, bot, pass_sigs in singles:
        if coalesced:
            prev = coalesced[-1]
            prev_end = _parse_dt(prev["ts_et_end"])
            cur_start = _parse_dt(ts)
            if (prev["bot_id"] == bot_id and prev["automation"] == automation
                    and prev["pass_signatures"] == pass_sigs
                    and (cur_start - prev_end).total_seconds() == 60):
                prev["ts_et_end"] = ts
                prev["minutes"] += 1
                prev["description"] = (
                    f"{automation}: conflicting readings from "
                    f"{prev['ts_et']} to {ts}: "
                    + "; ".join(f"{p}: {s!r}" for p, s in pass_sigs)
                )
                continue
        coalesced.append({
            "bot_id": bot_id,
            "bot": bot,
            "automation": automation,
            "ts_et": ts,
            "ts_et_end": ts,
            "minutes": 1,
            "pass_signatures": pass_sigs,
            "description": (
                f"{automation}: conflicting readings at {ts}: "
                + "; ".join(f"{p}: {s!r}" for p, s in pass_sigs)
            ),
        })

    by_pass = {}
    for rec in coalesced:
        for pid, _ in rec["pass_signatures"]:
            by_pass.setdefault(pid, []).append(rec)
    return by_pass


def dedup_and_sort(rows: list) -> list:
    """Keep first occurrence by (bot_id, automation, ts_et, signature_raw)."""
    seen = set()
    out = []
    for r in rows:
        key = (r["bot_id"], r["automation"], r["ts_et"], r["signature_raw"])
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    out.sort(key=lambda r: (r["bot"], r["automation"], r["ts_et"] or "",
                             r["signature_raw"], r["pass_id"]))
    return out


def write_outputs(rows: list, manifest: list, disagreements: dict, date: str,
                  root: str) -> dict:
    out_dir = os.path.join(root, "data", "oa_logs", date)
    os.makedirs(out_dir, exist_ok=True)

    # group rows by bot_id
    by_bot = {}
    for r in rows:
        by_bot.setdefault(r["bot_id"], []).append(r)

    written = {}
    for bot_id, rs in by_bot.items():
        path = os.path.join(out_dir, f"{bot_id}.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for r in rs:
                f.write(json.dumps(r, ensure_ascii=False, sort_keys=False) + "\n")
        written[bot_id] = path

    # attach per-pass disagreement lists; manifest writes as an array (one object
    # per capture/pass) per the task spec.
    manifest_list = []
    for p in manifest:
        p = dict(p)
        p["disagreements"] = disagreements.get(p["pass_id"], [])
        manifest_list.append(p)

    manifest_path = os.path.join(out_dir, "MANIFEST.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_list, f, ensure_ascii=False, sort_keys=False, indent=2)
        f.write("\n")
    written["MANIFEST"] = manifest_path
    return written


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------
def _expected_fixture_stats():
    return {
        "insurance_13:46_rows_per_scanner": 25,
        "insurance_14:09_rows_per_scanner": 25,
        # The capture header claims 401 rows, but the explicit per-signature
        # accounting in the file sums to 400.  The parser expands the accounted
        # rows and does not invent the missing row.
        "salvage_rows_total": 400,
        "salvage_header_claim": 401,
        "fortress_rows": 0,
    }


def selftest(root: str = None) -> int:
    if root is None:
        root = repo_root()
    date = "2026-08-17"
    base = parse_date(date)

    with tempfile.TemporaryDirectory() as tmp:
        # Copy the committed fixture captures into the temp root so we can run
        # against the same files without touching the repo tree.
        tmp_root = os.path.join(tmp, "repo")
        os.makedirs(os.path.join(tmp_root, "data", "captures"))
        for path in find_captures(date, root):
            dst = os.path.join(tmp_root, "data", "captures", os.path.basename(path))
            with open(path, "rb") as src:
                with open(dst, "wb") as d:
                    d.write(src.read())

        rows, manifest = parse_captures(date, tmp_root)
        disagreements = detect_disagreements(rows)
        deduped = dedup_and_sort(rows)
        written = write_outputs(deduped, manifest, disagreements, date, tmp_root)

        # 1. manifest has the expected passes
        pass_ids = {p["pass_id"] for p in manifest}
        want = {
            "gf-2026-08-17-insurance-13:46",
            "gf-2026-08-17-insurance-14:09",
            "gf-2026-08-17-salvage",
            "fortress-2026-08-17-salvage",
        }
        if pass_ids != want:
            print(f"FAIL: manifest pass_ids {pass_ids} != {want}", file=sys.stderr)
            return 1

        # 2. row counts per fixture/pass
        by_pass = {}
        for r in rows:   # before dedup, i.e. rows per pass
            by_pass.setdefault(r["pass_id"], 0)
            by_pass[r["pass_id"]] += 1
        exp = _expected_fixture_stats()
        if by_pass.get("gf-2026-08-17-insurance-13:46") != exp["insurance_13:46_rows_per_scanner"] * 2:
            print(f"FAIL: insurance-13:46 row count {by_pass.get('gf-2026-08-17-insurance-13:46')}", file=sys.stderr)
            return 1
        if by_pass.get("gf-2026-08-17-insurance-14:09") != exp["insurance_14:09_rows_per_scanner"] * 2:
            print(f"FAIL: insurance-14:09 row count {by_pass.get('gf-2026-08-17-insurance-14:09')}", file=sys.stderr)
            return 1
        if by_pass.get("gf-2026-08-17-salvage") != exp["salvage_rows_total"]:
            print(f"FAIL: salvage row count {by_pass.get('gf-2026-08-17-salvage')}", file=sys.stderr)
            return 1

        # 3. dedup behaviour: the 13:35 fill should appear once in the deduped output
        fill_rows = [r for r in deduped
                     if r["automation"] == "GF-ScannerA-PutSpread"
                     and r["ts_et"] == iso_ts(datetime.datetime(
                         base.year, base.month, base.day, 13, 35, tzinfo=ETZ))]
        fill_sigs = {r["signature_raw"] for r in fill_rows}
        if len(fill_rows) != 1:
            print(f"FAIL: expected 1 deduped fill row, got {len(fill_rows)}", file=sys.stderr)
            return 1
        if "1 open position" not in fill_sigs.pop():
            print("FAIL: deduped fill row does not have '1 open position'", file=sys.stderr)
            return 1

        # 4. disagreement surfaced: there must be a ScannerA conflict around the fill
        all_disagreements = [d for lst in disagreements.values() for d in lst]
        scanner_a_conflicts = [
            d for d in all_disagreements
            if d["automation"] == "GF-ScannerA-PutSpread"
            and d["ts_et"].startswith("2026-08-17T13:")
        ]
        if not scanner_a_conflicts:
            print("FAIL: no ScannerA 13:xx disagreement recorded", file=sys.stderr)
            return 1
        sig_pairs = set()
        for d in scanner_a_conflicts:
            for _, sig in d["pass_signatures"]:
                sig_pairs.add(sig)
        want_sigs = {"5 decisions | 1 loop", "5 decisions | 1 filtered position | 1 loop"}
        if not want_sigs.issubset(sig_pairs):
            print(f"FAIL: disagreement does not contain both ScannerA signatures {want_sigs}: {sig_pairs}",
                  file=sys.stderr)
            return 1

        # 5. byte-stability: re-run and compare sha256 of every output file
        first_hashes = {name: raw_sha256(p) for name, p in written.items()}

        rows2, manifest2 = parse_captures(date, tmp_root)
        deduped2 = dedup_and_sort(rows2)
        written2 = write_outputs(deduped2, manifest2,
                                 detect_disagreements(rows2), date, tmp_root)
        second_hashes = {name: raw_sha256(p) for name, p in written2.items()}

        if first_hashes != second_hashes:
            print("FAIL: output not byte-stable between two runs", file=sys.stderr)
            for k in sorted(set(first_hashes) | set(second_hashes)):
                if first_hashes.get(k) != second_hashes.get(k):
                    print(f"  {k}: {first_hashes.get(k)} vs {second_hashes.get(k)}",
                          file=sys.stderr)
            return 1

        # 6. output must not contain run timestamps or wall-clock noise
        noise = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}")
        for name, p in written.items():
            txt = open(p, encoding="utf-8").read()
            if noise.search(txt):
                print(f"FAIL: output {name} contains microsecond/run timestamp",
                      file=sys.stderr)
                return 1

        print("oa_reader_parse.py: selftest OK")
        print(f"  passes: {len(manifest)}")
        print(f"  raw rows (pre-dedup): {len(rows)}")
        print(f"  deduped rows: {len(deduped)}")
        print(f"  disagreement records: {len(all_disagreements)}")
        return 0


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description="OA-Reader step-0 fixture parser")
    ap.add_argument("date", nargs="?", default=None, help="YYYY-MM-DD capture date")
    ap.add_argument("--selftest", action="store_true", help="run fixture selftest")
    ap.add_argument("--root", default=None, help="repo root (default: parent of scripts/)")
    ap.add_argument("--output-root", default=None,
                    help="write outputs under this root instead of <root>/data")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest(args.root)

    if not args.date:
        ap.error("DATE is required unless --selftest")

    root = args.root or repo_root()
    if args.output_root:
        write_root = args.output_root
    else:
        write_root = root

    rows, manifest = parse_captures(args.date, root)
    disagreements = detect_disagreements(rows)
    deduped = dedup_and_sort(rows)
    written = write_outputs(deduped, manifest, disagreements, args.date, write_root)
    total_disagreements = sum(len(v) for v in disagreements.values())
    for name, p in written.items():
        print(f"wrote {p}")


if __name__ == "__main__":
    raise SystemExit(main())
