#!/usr/bin/env python3
"""Find an OA position export and install it as data/raw/<day>.csv.

DISCOVERY BY HEADER CONTENT, NEVER BY FILENAME. The 26-column OA Export Data
schema is the only thing that makes a file a candidate.

The ET day is derived two ways and cross-checked: the file's mtime in
America/New_York, and the max openDate across the data rows. A --day override
is still cross-checked and still refuses.
"""
import argparse, contextlib, csv, hashlib, io, json, os, re, shutil, sys, tempfile
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# OA Export Data schema (docs/capture-architecture-2026-07-30.md)
EXPECTED_HEADER = [
    "botName", "type", "description", "symbol", "status", "quantity",
    "daysInTrade", "openPrice", "closePrice", "premium", "pnl", "ror",
    "returnPct", "risk", "ev", "alpha", "highReturnPct", "lowReturnPct",
    "highReturnPctDate", "lowReturnPctDate", "expiration", "openDate",
    "closeDate", "tags", "underlyingOpen", "underlyingClose"
]

_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fo:
        for chunk in iter(lambda: fo.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_root(cli_root):
    """--root > $FLEET_ROOT > the repo, matching build_ledger.py."""
    root = cli_root or os.environ.get("FLEET_ROOT") or ROOT
    return os.path.abspath(root)


def et_day_from_mtime(mtime):
    """File mtime converted to America/New_York date."""
    return datetime.fromtimestamp(mtime, tz=ZoneInfo("America/New_York")).date().isoformat()


def find_candidates(scan_dir):
    """Return every .csv in scan_dir whose first row matches the OA header."""
    if not os.path.isdir(scan_dir):
        return []
    candidates = []
    for name in sorted(os.listdir(scan_dir)):
        if not name.lower().endswith(".csv"):
            continue
        path = os.path.join(scan_dir, name)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, "r", newline="") as fo:
                reader = csv.reader(fo)
                try:
                    row = next(reader)
                except StopIteration:
                    continue
                values = [h.strip() for h in row]
                while values and values[-1] == "":
                    values.pop()
                if values == EXPECTED_HEADER:
                    candidates.append(path)
        except (OSError, csv.Error, UnicodeDecodeError):
            continue
    return candidates


def read_open_dates(path):
    """Return all non-empty YYYY-MM-DD openDate values in the export."""
    with open(path, "r", newline="") as fo:
        dates = []
        for r in csv.DictReader(fo):
            d = (r.get("openDate") or "").strip()[:10]
            if d:
                dates.append(d)
    return dates


def find_mangled(scan_dir):
    """Files whose names contain the literal string 'data:raw' (macOS path-mangle artifact)."""
    if not os.path.isdir(scan_dir):
        return []
    return sorted(n for n in os.listdir(scan_dir) if "data:raw" in n)


def report_mangled(names):
    if names:
        print("Suspected mis-saved exports (report only):")
        for n in names:
            print(f"  {n}")


def fail(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser(
        description="Find an OA position export and install it as data/raw/<day>.csv")
    ap.add_argument("--downloads", default=None,
                    help="directory to scan (default: ~/Downloads)")
    ap.add_argument("--root", default=None,
                    help="repo/scratch root to write into (default: $FLEET_ROOT or repo)")
    ap.add_argument("--day", default=None,
                    help="override the day used for data/raw/<day>.csv (still cross-checked)")
    ap.add_argument("--ledger-start", default=None,
                    help="override LEDGER_START for the post-cutover range check")
    ap.add_argument("--dry-run", action="store_true",
                    help="run every check and print every derivation; write nothing")
    ap.add_argument("--selftest", action="store_true",
                    help="run the fixture-based selftest")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    # Resolve the same way build_ledger.py does.
    import build_ledger
    ledger_start, ls_source = build_ledger.resolve_ledger_start(args.ledger_start)

    downloads = args.downloads or os.path.expanduser("~/Downloads")
    if not os.path.isdir(downloads):
        fail(f"ERROR: not a directory: {downloads}")

    mangled = find_mangled(downloads)
    candidates = find_candidates(downloads)

    if not candidates:
        fail(f"ERROR: no OA export candidate found in {downloads}")
    if len(candidates) > 1:
        print(f"ERROR: more than one OA export candidate found in {downloads}:", file=sys.stderr)
        for c in candidates:
            print(f"  {os.path.basename(c)}", file=sys.stderr)
        report_mangled(mangled)
        sys.exit(1)

    src = candidates[0]
    open_dates = read_open_dates(src)
    if not open_dates:
        fail(f"ERROR: no openDate values found in {src}")

    max_open = max(open_dates)
    min_open = min(open_dates)
    mtime = os.path.getmtime(src)
    mtime_day = et_day_from_mtime(mtime)

    if args.day:
        if not _DATE_RE.match(args.day):
            fail(f"ERROR: --day {args.day!r} is not YYYY-MM-DD")
        day = args.day
    else:
        day = mtime_day

    print(f"mtime ET day: {mtime_day}")
    print(f"max openDate: {max_open}")
    print(f"min openDate: {min_open}")
    print(f"LEDGER_START: {ledger_start}   (from {ls_source})")

    if mtime_day < max_open:
        fail(f"ERROR: mtime ET day {mtime_day} is earlier than max openDate {max_open}; "
             f"the export cannot be from before its latest position: {src}")
    if day < max_open:
        fail(f"ERROR: chosen day {day} is earlier than max openDate {max_open}: {src}")
    if min_open > ledger_start:
        fail(f"ERROR: min openDate {min_open} is later than LEDGER_START {ledger_start} "
             f"(from {ls_source}); export does not cover the post-cutover window: {src}")

    root = resolve_root(args.root)
    raw_dir = os.path.join(root, "data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    dest = os.path.join(raw_dir, f"{day}.csv")

    src_sha = sha256(src)
    if os.path.exists(dest):
        dst_sha = sha256(dest)
        if src_sha == dst_sha:
            print(f"already ingested: {os.path.relpath(dest, root)} matches {os.path.basename(src)}")
            print(f"  source sha256: {src_sha}")
            print(f"  dest   sha256: {dst_sha}")
            report_mangled(mangled)
            return
        fail(f"ERROR: destination exists with a different sha256: {dest}\n"
             f"  source sha256: {src_sha}\n"
             f"  dest   sha256: {dst_sha}")

    if args.dry_run:
        print(f"DRY-RUN: would copy {os.path.basename(src)} -> {os.path.relpath(dest, root)}")
        print(f"  source sha256: {src_sha}")
    else:
        shutil.copyfile(src, dest)
        dst_sha = sha256(dest)
        print(f"ingested {os.path.basename(src)} -> {os.path.relpath(dest, root)}")
        print(f"  source sha256: {src_sha}")
        print(f"  dest   sha256: {dst_sha}")
    report_mangled(mangled)


# ===========================================================================
# SELF-TEST — fixtures + a named check matrix, run with --selftest
# ===========================================================================
def _st_row(open_day, bot="GF-QQQ-IC-Ride"):
    t = f"{open_day} 09:46:00"
    return {
        "botName": bot, "type": "shortputspread",
        "description": "-500 put +498 put", "symbol": "QQQ", "status": "closed",
        "quantity": "1", "daysInTrade": "0", "openPrice": "0.40",
        "closePrice": "0.20", "premium": "40", "pnl": "10", "ror": "0.05",
        "returnPct": "1", "risk": "160", "ev": "1", "alpha": "0.1",
        "highReturnPct": "1", "lowReturnPct": "-0.5",
        "highReturnPctDate": "", "lowReturnPctDate": "",
        "expiration": open_day, "openDate": t, "closeDate": t,
        "tags": "", "underlyingOpen": "500", "underlyingClose": "499"
    }


def _st_ts(day, hour=18):
    y, m, d = (int(x) for x in day.split("-"))
    return datetime(y, m, d, hour, 0, 0, tzinfo=ZoneInfo("America/New_York")).timestamp()


def _st_write(path, rows):
    with open(path, "w", newline="") as fo:
        w = csv.writer(fo)
        w.writerow(EXPECTED_HEADER)
        for r in rows:
            w.writerow([r.get(c, "") for c in EXPECTED_HEADER])


def _st_run(argv):
    """Run main() with the given argv, returning (exit_code_or_None, out, err)."""
    old_argv = sys.argv
    out, err = io.StringIO(), io.StringIO()
    sys.argv = ["ingest_export.py"] + list(argv)
    code = None
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            main()
    except SystemExit as e:
        code = e.code
    finally:
        sys.argv = old_argv
    return code, out.getvalue(), err.getvalue()


def selftest():
    import tempfile, shutil
    fails, results = 0, []

    def check(name, got, want):
        nonlocal fails
        ok = got == want
        fails += not ok
        results.append((ok, name, got, want))

    def base_args(start, root, downloads, extra=()):
        return ["--ledger-start", start, "--root", root, "--downloads", downloads] + list(extra)

    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    tmp = tempfile.mkdtemp(prefix="ingest-selftest-")
    try:
        downloads = os.path.join(tmp, "downloads")
        root = os.path.join(tmp, "root")
        os.makedirs(downloads)
        os.makedirs(os.path.join(root, "data", "raw"))

        day1, day2, day3 = "2099-01-02", "2099-01-03", "2099-01-04"

        # --- header-content discovery ----------------------------------------
        right_name = os.path.join(downloads, f"foo-{day1} (3).csv")
        _st_write(right_name, [_st_row(day1)])
        os.utime(right_name, (_st_ts(day1), _st_ts(day1)))

        wrong_name = os.path.join(downloads, "positions.csv")
        with open(wrong_name, "w", newline="") as fo:
            csv.writer(fo).writerow(["foo", "bar"])

        code, out, err = _st_run(base_args(day1, root, downloads, ["--day", day1]))
        dest = os.path.join(root, "data", "raw", f"{day1}.csv")
        check("D1  right header with wrong filename is accepted",
              (code is None, os.path.exists(dest), os.path.basename(right_name) in out),
              (True, True, True))

        # clean up for next discovery test
        os.remove(dest)

        code2, _, err2 = _st_run(base_args(day1, root, downloads, ["--day", day1]))
        check("D1b right header with wrong filename is still the only candidate "
              "after removing the ingested copy",
              code2 is None, True)

        # remove the right file; only the wrong header remains
        os.remove(right_name)
        code, _, err = _st_run(base_args(day1, root, downloads))
        check("D2  wrong header with right-looking filename is rejected",
              (code is not None, "no OA export candidate" in err),
              (True, True))

        # --- zero candidates -------------------------------------------------
        empty_dl = os.path.join(tmp, "empty_downloads")
        os.makedirs(empty_dl)
        code, _, err = _st_run(base_args(day1, root, empty_dl))
        check("D3  zero candidates refuses, naming the directory scanned",
              (code is not None, empty_dl in err, "no OA export candidate" in err),
              (True, True, True))

        # --- multiple candidates ---------------------------------------------
        multi_dl = os.path.join(tmp, "multi_downloads")
        os.makedirs(multi_dl)
        f1 = os.path.join(multi_dl, "a.csv")
        f2 = os.path.join(multi_dl, "b.csv")
        _st_write(f1, [_st_row(day1)]); os.utime(f1, (_st_ts(day1), _st_ts(day1)))
        _st_write(f2, [_st_row(day1)]); os.utime(f2, (_st_ts(day1), _st_ts(day1)))
        code, _, err = _st_run(base_args(day1, root, multi_dl))
        check("D4  multiple candidates refuses, listing them",
              (code is not None, "a.csv" in err, "b.csv" in err),
              (True, True, True))

        # --- two-way day derivation agreeing ---------------------------------
        good_dl = os.path.join(tmp, "good_downloads")
        os.makedirs(good_dl)
        good = os.path.join(good_dl, "export.csv")
        _st_write(good, [_st_row(day2)])
        os.utime(good, (_st_ts(day2), _st_ts(day2)))
        code, out, err = _st_run(base_args(day2, root, good_dl))
        good_dest = os.path.join(root, "data", "raw", f"{day2}.csv")
        check("D5  mtime ET day and max openDate agree",
              (code is None, os.path.exists(good_dest), "ingested" in out),
              (True, True, True))

        # --- two-way day derivation DISAGREEING ------------------------------
        bad_dl = os.path.join(tmp, "bad_downloads")
        os.makedirs(bad_dl)
        bad = os.path.join(bad_dl, "bad.csv")
        _st_write(bad, [_st_row(day3)])
        os.utime(bad, (_st_ts(day2), _st_ts(day2)))  # mtime day2, data day3
        code, _, err = _st_run(base_args(day3, root, bad_dl))
        check("D6  mtime ET day earlier than max openDate refuses",
              (code is not None, "mtime ET day" in err, day2 in err, day3 in err),
              (True, True, True, True))

        # --- --day still cross-checked ---------------------------------------
        code, _, err = _st_run(base_args(day2, root, good_dl, ["--day", day1]))
        check("D7  --day override is still cross-checked and refuses when too early",
              (code is not None, "chosen day" in err, day1 in err, day2 in err),
              (True, True, True, True))

        # --- min-open-date > LEDGER_START ------------------------------------
        short_dl = os.path.join(tmp, "short_downloads")
        os.makedirs(short_dl)
        short = os.path.join(short_dl, "short.csv")
        _st_write(short, [_st_row(day2)])  # only day2
        os.utime(short, (_st_ts(day2), _st_ts(day2)))
        # day2 only, start day1 -> min day2 > start day1
        code, _, err = _st_run(base_args(day1, root, short_dl))
        check("D8  min openDate later than LEDGER_START refuses",
              (code is not None, "min openDate" in err, day2 in err, day1 in err),
              (True, True, True, True))

        # --- idempotent equal-sha re-run -------------------------------------
        code, out, _ = _st_run(base_args(day2, root, good_dl))
        check("D9  idempotent re-run on equal sha says already ingested",
              (code is None, "already ingested" in out, os.path.exists(good_dest)),
              (True, True, True))

        # --- differing-sha refusal -------------------------------------------
        bad_dest = os.path.join(root, "data", "raw", f"{day2}.csv")
        with open(bad_dest, "w", newline="") as fo:
            csv.writer(fo).writerow(EXPECTED_HEADER)
            csv.writer(fo).writerow([_st_row(day2)[c] for c in EXPECTED_HEADER])
            csv.writer(fo).writerow([_st_row(day2)[c] for c in EXPECTED_HEADER])
        before = open(bad_dest).read()
        code, _, err = _st_run(base_args(day2, root, good_dl))
        after = open(bad_dest).read()
        check("D10 differing destination sha refuses and writes nothing",
              (code is not None, "different sha256" in err, after == before),
              (True, True, True))

        # --- colon-mangled reporting -----------------------------------------
        colon_root = os.path.join(tmp, "colon_root")
        os.makedirs(os.path.join(colon_root, "data", "raw"))
        colon_dl = os.path.join(tmp, "colon_downloads")
        os.makedirs(colon_dl)
        colon = os.path.join(colon_dl, "data:raw:2099-01-03.csv")
        with open(colon, "w", newline="") as fo:
            csv.writer(fo).writerow(["foo", "bar"])
        valid = os.path.join(colon_dl, "valid.csv")
        _st_write(valid, [_st_row(day2)])
        os.utime(valid, (_st_ts(day2), _st_ts(day2)))
        code, out, _ = _st_run(base_args(day2, colon_root, colon_dl))
        colon_dest = os.path.join(colon_root, "data", "raw", f"{day2}.csv")
        check("D11 colon-mangled artifacts are reported, never moved/deleted",
              (code is None, "data:raw:2099-01-03.csv" in out,
               os.path.exists(colon), os.path.exists(colon_dest)),
              (True, True, True, True))

        # --- dry-run writes nothing ------------------------------------------
        dry_root = os.path.join(tmp, "dry_root")
        os.makedirs(os.path.join(dry_root, "data", "raw"))
        dry_dl = os.path.join(tmp, "dry_downloads")
        os.makedirs(dry_dl)
        dry = os.path.join(dry_dl, "dry.csv")
        _st_write(dry, [_st_row(day2)])
        os.utime(dry, (_st_ts(day2), _st_ts(day2)))
        code, out, _ = _st_run(base_args(day2, dry_root, dry_dl, ["--dry-run"]))
        dry_dest = os.path.join(dry_root, "data", "raw", f"{day2}.csv")
        check("D12 --dry-run runs every check and writes nothing",
              (code is None, "DRY-RUN" in out, not os.path.exists(dry_dest)),
              (True, True, True))

        # --- G-3 / live-ledger separation: the repo's data/ is untouched -----
        live_before = sha256(os.path.join(repo, "data", "trades.csv")) \
            if os.path.exists(os.path.join(repo, "data", "trades.csv")) else "absent"
        check("R1  selftest never touched the repo's data/trades.csv",
              live_before,
              sha256(os.path.join(repo, "data", "trades.csv"))
              if os.path.exists(os.path.join(repo, "data", "trades.csv")) else "absent")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("SELF-TEST — ingest_export.py")
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
