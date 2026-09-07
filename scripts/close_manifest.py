#!/usr/bin/env python3
"""close_manifest.py — write the daily close manifest and append a receipt.

Implements R-2026-08-21-CLOSE-RECEIPT-SURFACE (WRAP) and
R-2026-08-21-STAGING-MANIFEST.

Reads the artifacts produced by:
  scripts/ingest_export.py
  scripts/daily.sh <day>
  scripts/capture_bundle.py (when raw captures are present)
  scripts/render_brief.py <day>

Writes:
  data/close/<day>/manifest.json
  data/receipts/close-runs.jsonl (append-only)

Usage:
  python3 scripts/close_manifest.py <YYYY-MM-DD> [--root ROOT] [--capture-dir DIR]
  python3 scripts/close_manifest.py <YYYY-MM-DD> --commit-command
  python3 scripts/close_manifest.py <YYYY-MM-DD> --reconcile [--capture-dir DIR]
  python3 scripts/close_manifest.py --selftest

--capture-dir is the bundle dir capture_bundle.py actually produced in this
run (close.sh passes it explicitly).  It differs from the default
data/captures/<day>-roster on a catch-up close: the bundle is named by the
capture's own `captured:` date, not by the close day.

--reconcile prints what the EXISTING manifest for a day would record under
the current capture rules.  It writes nothing; a recorded manifest is
history and is never rewritten.
"""
import argparse
import contextlib
import csv
import datetime
import glob

import market_calendar as mcal
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DAILY_RUNS = os.path.join("receipts", "daily-runs.jsonl")
CLOSE_RUNS = os.path.join("receipts", "close-runs.jsonl")

NARR_SLOTS = ("since-yesterday", "convexity", "lesson", "tomorrow", "fire", "strategy")

# Re-use the daily loop output list so the two receipts never disagree on scope.
# These are relative paths from the fleet root.
DAILY_OUTPUTS = [
    "data/trades.csv",
    "data/bots.csv",
    "data/straddlers.csv",
    "data/ops_rows.csv",
    "data/ledger_meta.json",
    "data/execution_audit_findings.csv",
    "data/execution_audit_findings_meta.json",
    "data/hedge_tournament.csv",
    "data/trade_window.csv",
    "data/lessons.csv",
    "data/compliance.csv",
    "STATUS.md",
    "dashboard.html",
]


def sha256(path):
    """SHA-256 of a file, in 64 KiB chunks."""
    h = hashlib.sha256()
    with open(path, "rb") as fo:
        for chunk in iter(lambda: fo.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def die(msg, code=2):
    print(f"close_manifest.py: FATAL: {msg}", file=sys.stderr)
    sys.exit(code)


def resolve_root(cli_root):
    """--root > $FLEET_ROOT > repo."""
    return os.path.abspath(cli_root or os.environ.get("FLEET_ROOT") or ROOT)


# ---------------------------------------------------------------------------
# Forbidden-path predicate.  A path matching any of these is a FATAL REFUSAL.
# ---------------------------------------------------------------------------
FORBIDDEN_PATTERNS = [
    re.compile(r"(^|/)\.claude/"),
    re.compile(r"(^|/)_locktrash/"),
    re.compile(r"(^|/)_"),
    re.compile(r"(^|/)one$"),
]


def is_forbidden(rel_path):
    """Return True if a repo-relative path matches a forbidden pattern."""
    for pat in FORBIDDEN_PATTERNS:
        if pat.search(rel_path):
            return True
    return False


def check_forbidden(paths):
    """Refuse if any staged/discovered path is forbidden."""
    for p in paths:
        if is_forbidden(p):
            die(f"forbidden path in output set: {p!r}")


def _untracked_top_level(root):
    """Top-level names that are UNTRACKED and NOT IGNORED, or None if unknowable.

    This is git's own definition of untracked -- exactly what `git status`
    reports as `??` -- via `ls-files --others --exclude-standard`.  Read-only;
    the same `git ls-files` mechanism check_refs.py already relies on.

    Anything the repository has accepted (tracked) or deliberately excluded
    (.gitignore, e.g. `.claude/` and `_locktrash/`) is NOT a stray and is not
    returned.  Returns None when `root` is not a git checkout (a seeded scratch
    root is not), so the caller can skip the arm visibly rather than treat
    every entry as untracked and refuse on all of them.
    """
    try:
        out = subprocess.run(
            ["git", "-C", root, "ls-files", "--others", "--exclude-standard"],
            capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    return {p.split("/", 1)[0] for p in out.splitlines() if p}


def scan_for_forbidden(root, day, capture_dir=None):
    """Walk the close output directories and the repo root (top-level only)
    and refuse on any forbidden file.

    The second scan is intentionally redundant with the staged-path checks:
    a file that is not part of the manifest but sits in an output directory
    (e.g. a planted `_scratch.md`) must still be seen red.

    The repo-root scan is top-level only: the `_` pattern matches any path
    segment beginning with an underscore, so a recursive walk would refuse
    on `scripts/__pycache__/` and similar.  Only top-level entries are
    staged-file sources; subdirectories are output directories covered by
    the explicit directory list above.
    """
    # Top-level repo-root entries are staged-file sources too.  Report the
    # full set, not just the first, so the operator can clean once.
    #
    # R-2026-08-31-ROOT-SCAN-READING-B narrows this arm to UNTRACKED / NEW
    # entries: an entry already committed to the repository has been accepted
    # into it and is not a stray.  Reading A -- refuse on mere presence -- was
    # declined because `(^|/)_` matches six files committed at master, so it
    # would refuse on every run in every clean checkout.
    untracked = _untracked_top_level(root)
    if untracked is None:
        # Tracked-ness is unknowable here (a seeded scratch root is not a git
        # checkout).  Skip the arm VISIBLY: a guard that cannot run must say so
        # rather than pass silently.
        print("close_manifest.py: NOTE: repo-root forbidden scan skipped "
              "(root is not a git checkout, so tracked-ness is unknown)",
              file=sys.stderr)
    else:
        forbidden_root = []
        for name in sorted(untracked):
            ap = os.path.join(root, name)
            rel = name if not os.path.isdir(ap) else name + "/"
            if is_forbidden(rel):
                forbidden_root.append(name)
        if forbidden_root:
            forbidden_root.sort()
            die("forbidden untracked top-level repo entr"
                + ("y: " if len(forbidden_root) == 1 else "ies: ")
                + ", ".join(repr(p) for p in forbidden_root))

    dirs = [
        os.path.join(root, "data", "raw"),
        os.path.join(root, "data", "receipts"),
        os.path.join(root, "data", "close", day),
        resolve_capture_dir(root, day, capture_dir),
    ]
    # data/brief/ for the current day only
    for p in glob.glob(os.path.join(root, "data", "brief", f"{day}_*")):
        if os.path.isfile(p):
            rel = os.path.relpath(p, root)
            if is_forbidden(rel):
                die(f"forbidden path in output set: {rel!r}")
    for d in dirs:
        if not os.path.isdir(d):
            continue
        for dirpath, _dirnames, filenames in os.walk(d):
            for fn in filenames:
                ap = os.path.join(dirpath, fn)
                rel = os.path.relpath(ap, root)
                if is_forbidden(rel):
                    die(f"forbidden path in output set: {rel!r}")


# ---------------------------------------------------------------------------
# Helpers: receipts, dates, narrative, capture bundle, staged paths
# ---------------------------------------------------------------------------
def read_jsonl_last(path, predicate=None):
    """Return the last JSON object in a jsonl that satisfies predicate."""
    if not os.path.exists(path):
        return None
    last = None
    with open(path) as fo:
        for line in fo:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue
            if predicate is None or predicate(rec):
                last = rec
    return last


def previous_close_day(daily_runs_path, current_day):
    """The last daily receipt for a day strictly before current_day.

    Reads data/receipts/daily-runs.jsonl from the first byte — its `day`
    field, never file mtimes.
    """
    def pred(rec):
        d = rec.get("day")
        return d and d < current_day
    rec = read_jsonl_last(daily_runs_path, pred)
    return rec.get("day") if rec else None


def gap_statement(previous_day, current_day):
    """Return the gap object and the human statement.

    Calendar uses the shared market_calendar module: weekends plus US equity
    market holidays (rule-derived) are excluded.  This is the same source of
    truth as check_heartbeat.py and report.py, stated in the manifest.
    """
    CALENDAR = "rule-derived US equity market holidays; weekends excluded"
    if previous_day is None:
        return {
            "last_close": None,
            "unobserved_days": [],
            "unobserved_count": 0,
            "evaluable": False,
            "statement": "no prior close on record",
            "calendar": CALENDAR,
        }
    try:
        p = datetime.date.fromisoformat(previous_day)
        c = datetime.date.fromisoformat(current_day)
    except ValueError:
        die(f"cannot parse gap dates: {previous_day!r}, {current_day!r}")

    unobs = []
    d = p + datetime.timedelta(days=1)
    while d < c:
        if mcal.is_trading_day(d):
            unobs.append(d.isoformat())
        d += datetime.timedelta(days=1)

    if not unobs:
        statement = f"previous close {previous_day}, no gap"
    else:
        if len(unobs) == 1:
            statement = (f"last close {previous_day}, 1 trading day "
                         f"unobserved ({unobs[0]})")
        else:
            statement = (f"last close {previous_day}, {len(unobs)} "
                         f"trading days unobserved ({', '.join(unobs)})")

    return {
        "last_close": previous_day,
        "unobserved_days": unobs,
        "unobserved_count": len(unobs),
        "evaluable": True,
        "statement": statement,
        "calendar": CALENDAR,
    }


def load_daily_receipt(root, day):
    """Return the daily receipt for `day` (last matching), or None."""
    p = os.path.join(root, "data", DAILY_RUNS)
    def pred(rec):
        return rec.get("day") == day
    rec = read_jsonl_last(p, pred)
    if rec is None:
        # Fall back to the very last receipt if the day is not found; this
        # preserves operation on an empty or partially-ordered file.
        rec = read_jsonl_last(p)
    return rec


def load_export(root, day):
    p = os.path.join(root, "data", "raw", f"{day}.csv")
    if not os.path.isfile(p):
        die(f"export not found: {p}")
    return {"path": os.path.relpath(p, root), "sha256": sha256(p)}


def parse_narrative(root, day):
    """Return {slot: bool, unfilled_count, filled_count} for narrative.md."""
    p = os.path.join(root, "data", "brief", f"{day}_narrative.md")
    out = {slot: False for slot in NARR_SLOTS}
    if not os.path.exists(p):
        return {"path": None, "slots": out, "unfilled_count": len(NARR_SLOTS),
                "filled_count": 0}

    cur = None
    with open(p) as fo:
        for line in fo:
            m = re.match(r"^##\s+([a-z-]+)\s*$", line.strip())
            if m:
                cur = m.group(1)
                if cur not in NARR_SLOTS:
                    die(f"narrative {p}: unknown section {cur!r}")
                continue
            if cur and line.strip():
                out[cur] = True

    filled = sum(1 for v in out.values() if v)
    return {
        "path": os.path.relpath(p, root),
        "slots": out,
        "unfilled_count": len(NARR_SLOTS) - filled,
        "filled_count": filled,
    }


def load_brief(root, day):
    html = os.path.join(root, "data", "brief", f"{day}_brief.html")
    if not os.path.isfile(html):
        die(f"brief html not found: {html}")
    brief_json = os.path.join(root, "data", "brief", f"{day}_brief.json")
    p3 = os.path.join(root, "data", "brief", f"{day}_p3_verdicts.tsv")
    tape = os.path.join(root, "data", "brief", f"{day}_tape.json")
    out = {
        "html_path": os.path.relpath(html, root),
        "html_sha256": sha256(html),
        "json_path": os.path.relpath(brief_json, root) if os.path.isfile(brief_json) else None,
        "p3_verdicts_path": os.path.relpath(p3, root) if os.path.isfile(p3) else None,
        "tape_path": os.path.relpath(tape, root) if os.path.isfile(tape) else None,
        "narrative": parse_narrative(root, day),
    }
    return out


def resolve_capture_dir(root, day, capture_dir=None):
    """Return the absolute bundle dir this close should read.

    `capture_dir` is the dir capture_bundle.py actually produced in this run,
    passed explicitly by close.sh; the fallback is data/captures/<day>-roster.
    The two differ on a catch-up close: the bundle is named by the capture's
    own `captured:` date, not the close day.

    An explicit dir lands in staged_paths, so it is validated: it must live
    under <root>/data/captures, be named *-roster, and exist.  A bad explicit
    dir is FATAL -- an operator error is not an absent capture.
    """
    if capture_dir is None:
        return os.path.join(root, "data", "captures", f"{day}-roster")
    # realpath settles the containment question (/var -> /private/var and
    # friends); the returned path stays in root's own terms so that every
    # downstream os.path.relpath(..., root) stays inside the tree.
    d = capture_dir if os.path.isabs(capture_dir) else os.path.join(root, capture_dir)
    d = os.path.abspath(d)
    real = os.path.realpath(d)
    cap_root = os.path.realpath(os.path.join(root, "data", "captures"))
    try:
        inside = os.path.commonpath([real, cap_root]) == cap_root and real != cap_root
    except ValueError:
        inside = False
    if not inside or not os.path.basename(real).endswith("-roster"):
        die(f"--capture-dir must be a *-roster dir inside data/captures: {capture_dir!r}")
    if not os.path.isdir(d):
        die(f"--capture-dir not found: {capture_dir!r}")
    # Re-express in root's own spelling: if the caller passed the path through
    # a symlinked prefix (/var vs /private/var on macOS), relpath(real, root)
    # would escape with ../.. and break the staged-path derivations.
    return os.path.join(root, os.path.relpath(real, os.path.realpath(root)))


def _read_sha256sums(bundle_dir):
    """Parse <bundle>/SHA256SUMS.txt into {rel_path: sha256}, or None."""
    p = os.path.join(bundle_dir, "SHA256SUMS.txt")
    if not os.path.isfile(p):
        return None
    out = {}
    with open(p, encoding="utf-8") as fo:
        for line in fo:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            sha, _sep, rel = line.partition("  ")
            out[rel.strip()] = sha.strip()
    return out


def _verify_capture_txt(bundle_dir):
    """Verify the bundle's raw capture .txt against its SHA256SUMS.txt.

    Returns (status, error, captured_et, capture_day).  status is PRESENT
    only when at least one raw .txt exists and EVERY one matches the sha256
    recorded at bundle time.  `captured_et` is the capture's own `captured:`
    header verbatim; `capture_day` is the ET date derived from it.
    """
    txts = sorted(
        t for t in glob.glob(os.path.join(bundle_dir, "*.txt"))
        if os.path.basename(t) != "SHA256SUMS.txt")
    if not txts:
        return "MISMATCH", "no raw capture .txt in bundle", None, None

    sums = _read_sha256sums(bundle_dir)
    if sums is None:
        return "MISMATCH", "SHA256SUMS.txt missing", None, None
    for t in txts:
        rel = "./" + os.path.relpath(t, bundle_dir).replace(os.sep, "/")
        want = sums.get(rel)
        if want is None:
            return ("MISMATCH",
                    f"{os.path.basename(t)} not listed in SHA256SUMS.txt",
                    None, None)
        if sha256(t) != want:
            return ("MISMATCH",
                    f"sha256 mismatch for {os.path.basename(t)}",
                    None, None)

    captured_et = capture_day = None
    with open(txts[0], encoding="utf-8") as fo:
        for line in fo:
            m = re.match(r"^captured:\s*(.+?)\s*$", line)
            if m:
                captured_et = m.group(1)
                try:
                    dt = datetime.datetime.strptime(
                        captured_et.split(" (")[0].strip(),
                        "%a %b %d %Y %H:%M:%S GMT%z")
                    capture_day = dt.strftime("%Y-%m-%d")
                except ValueError:
                    capture_day = None
                break
    return "PRESENT", None, captured_et, capture_day


def load_capture(root, day, capture_dir=None):
    """Return capture bundle info, or a loud ABSENT object.

    `capture_dir` is the bundle dir produced in this run (see
    resolve_capture_dir); the fallback is data/captures/<day>-roster.

    status is PRESENT only when the bundle's raw .txt verifies against its
    SHA256SUMS.txt.  A verification failure is recorded as MISMATCH -- never
    silently -- with the reason in verification_error.
    """
    bundle_dir = resolve_capture_dir(root, day, capture_dir)
    if not os.path.isdir(bundle_dir):
        return {"present": False, "status": "ABSENT"}

    tsvs = glob.glob(os.path.join(bundle_dir, "02-roster-toggles-*.tsv"))
    if not tsvs:
        die(f"capture bundle directory exists but has no 02-roster-toggles-*.tsv: {bundle_dir}")

    drift = "NOT EVALUABLE"
    with open(tsvs[0]) as fo:
        for line in fo:
            if line.startswith("# DRIFT VERDICT:"):
                drift = line.split(":", 1)[1].strip()
                break

    files = []
    for dirpath, _dirnames, filenames in os.walk(bundle_dir):
        for fn in filenames:
            if fn == ".DS_Store":
                continue
            ap = os.path.join(dirpath, fn)
            rel = os.path.relpath(ap, root)
            files.append({"path": rel, "sha256": sha256(ap)})
    files.sort(key=lambda x: x["path"])

    status, verr, captured_et, capture_day = _verify_capture_txt(bundle_dir)
    out = {
        "present": True,
        "status": status,
        "bundle_dir": os.path.relpath(bundle_dir, root),
        "captured_et": captured_et,
        "capture_day": capture_day,
        "drift_verdict": drift,
        "tsv": os.path.relpath(tsvs[0], root),
        "files": files,
    }
    if verr:
        out["verification_error"] = verr
        print(f"close_manifest.py: WARNING: capture bundle failed "
              f"verification: {verr}", file=sys.stderr)
    return out


# ---------------------------------------------------------------------------
# Staged-path derivations — the R-2026-08-21-STAGING-MANIFEST contract
# ---------------------------------------------------------------------------
def _add_output_files(root, out, paths):
    """Add existing files from an iterable of relative paths."""
    for rel in paths:
        if os.path.isfile(os.path.join(root, rel)):
            out.add(rel)


def derive_staged_first(root, day, manifest, daily_receipt):
    """First derivation: from the manifest fields and the daily receipt."""
    paths = set()

    # Export
    paths.add(manifest["export"]["path"])

    # Daily receipt output hashes, if the files exist
    if daily_receipt and "hashes" in daily_receipt:
        for rel, h in daily_receipt["hashes"].items():
            if h is not None and os.path.isfile(os.path.join(root, rel)):
                paths.add(rel)
    else:
        _add_output_files(root, paths, DAILY_OUTPUTS)

    # Brief artifacts
    brief = manifest["brief"]
    for rel in (brief["html_path"], brief.get("json_path"),
                brief.get("p3_verdicts_path"), brief.get("tape_path")):
        if rel:
            paths.add(rel)
    if brief["narrative"]["path"]:
        paths.add(brief["narrative"]["path"])

    # Capture bundle files
    cap = manifest["capture"]
    if cap.get("present"):
        for f in cap["files"]:
            paths.add(f["path"])

    # Receipts and this manifest
    paths.add(os.path.join("data", "receipts", "daily-runs.jsonl"))
    paths.add(os.path.join("data", "receipts", "close-runs.jsonl"))
    paths.add(os.path.join("data", "close", day, "manifest.json"))

    return sorted(paths)


def derive_staged_second(root, day, capture_rel=None):
    """Second derivation: from a direct filesystem scan.

    `capture_rel` is the bundle dir actually read for this close, relative to
    root (the manifest records it as capture.bundle_dir); the default is the
    historical same-day dir data/captures/<day>-roster.
    """
    paths = set()

    _add_output_files(root, paths, DAILY_OUTPUTS)

    # Brief artifacts
    for rel in (
        f"data/brief/{day}_brief.json",
        f"data/brief/{day}_brief.html",
        f"data/brief/{day}_p3_verdicts.tsv",
        f"data/brief/{day}_tape.json",
        f"data/brief/{day}_narrative.md",
    ):
        if os.path.isfile(os.path.join(root, rel)):
            paths.add(rel)

    # Raw export
    export = os.path.join(root, "data", "raw", f"{day}.csv")
    if os.path.isfile(export):
        paths.add(os.path.relpath(export, root))

    # Receipts and this manifest are always part of the close output, whether
    # they exist yet at the moment of derivation or not; the generator writes
    # them before the commit command is printed.
    paths.add(os.path.join("data", DAILY_RUNS))
    paths.add(os.path.join("data", CLOSE_RUNS))
    manifest_path = os.path.join(root, "data", "close", day, "manifest.json")
    paths.add(os.path.relpath(manifest_path, root))

    # Capture bundle
    bundle_dir = os.path.join(
        root, capture_rel or os.path.join("data", "captures", f"{day}-roster"))
    if os.path.isdir(bundle_dir):
        for dirpath, _dirnames, filenames in os.walk(bundle_dir):
            for fn in filenames:
                if fn == ".DS_Store":
                    continue
                ap = os.path.join(dirpath, fn)
                paths.add(os.path.relpath(ap, root))

    return sorted(paths)


def build_and_write_manifest(root, day, argv, capture_dir=None):
    """Assemble the manifest, run the two staged-path derivations, write files."""
    # Pre-scan for forbidden files in the output directories.
    scan_for_forbidden(root, day, capture_dir=capture_dir)

    export = load_export(root, day)
    daily_receipt = load_daily_receipt(root, day)
    gap = gap_statement(
        previous_close_day(os.path.join(root, "data", DAILY_RUNS), day), day)
    brief = load_brief(root, day)
    capture = load_capture(root, day, capture_dir=capture_dir)

    # Initial manifest without staged paths.
    manifest = {
        "day": day,
        "argv": argv,
        "written_utc": datetime.datetime.now(datetime.timezone.utc)
                        .replace(microsecond=0).isoformat(),
        "calendar": gap["calendar"],
        "gap": gap,
        "export": export,
        "daily_receipt": _summarize_daily_receipt(daily_receipt),
        "brief": brief,
        "capture": capture,
    }

    # The two derivations.
    first = derive_staged_first(root, day, manifest, daily_receipt)
    second = derive_staged_second(root, day, capture.get("bundle_dir"))
    check_forbidden(first)
    check_forbidden(second)
    if first != second:
        die("staged-path derivation mismatch:\n  first  = {!r}\n  second = {!r}".format(first, second))

    manifest["staged_paths"] = first
    manifest["staged_count"] = len(first)
    manifest["commit_message"] = derive_commit_message(manifest)

    # Write manifest.
    close_dir = os.path.join(root, "data", "close", day)
    os.makedirs(close_dir, exist_ok=True)
    manifest_path = os.path.join(close_dir, "manifest.json")
    with open(manifest_path, "w") as fo:
        json.dump(manifest, fo, indent=2, sort_keys=True)
        fo.write("\n")

    # Append close-runs receipt (mode 'a', always).
    close_receipt = {
        "written_utc": manifest["written_utc"],
        "day": day,
        "argv": argv,
        "manifest_path": os.path.relpath(manifest_path, root),
        "manifest_sha256": sha256(manifest_path),
        "daily_final_exit": (daily_receipt or {}).get("final_exit"),
        "daily_rows_out": (daily_receipt or {}).get("rows_out"),
        "capture_present": capture.get("present", False),
        "staged_count": len(first),
    }
    append_close_receipt(root, close_receipt)

    print(f"close_manifest.py: wrote {os.path.relpath(manifest_path, root)}")
    print(f"  gap: {gap['statement']}")
    if capture.get("status") == "PRESENT":
        cap_line = ("PRESENT — " + capture["bundle_dir"]
                    + " — drift: " + capture["drift_verdict"].splitlines()[0])
    elif capture.get("status") == "MISMATCH":
        cap_line = "MISMATCH — " + capture.get("verification_error", "")
    else:
        cap_line = capture.get("status", "?")
    print(f"  capture: {cap_line}")
    print(f"  staged: {len(first)} path(s)")
    return manifest


def _summarize_daily_receipt(rec):
    """Return a summary of the daily receipt for the manifest."""
    if not rec:
        return None
    keep = ("day", "final_exit", "pinned", "ledger_start", "ledger_stale",
            "rows_in", "rows_out", "source_export", "min_open_date",
            "max_open_date", "written_utc")
    return {k: rec.get(k) for k in keep}


def derive_commit_message(manifest):
    day = manifest["day"]
    rows = manifest["daily_receipt"]["rows_out"] if manifest["daily_receipt"] else None
    exitv = manifest["daily_receipt"]["final_exit"] if manifest["daily_receipt"] else None
    cap = manifest["capture"]
    if cap.get("status") == "MISMATCH":
        cap_s = "capture MISMATCH"
    elif cap.get("present"):
        drift = cap["drift_verdict"]
        # Keep the commit message short: first line only, or a short status.
        if drift == "NOT EVALUABLE":
            cap_s = "capture PRESENT, NOT EVALUABLE"
        elif "ZERO" in drift:
            cap_s = "capture PRESENT, drift ZERO"
        else:
            cap_s = "capture PRESENT, " + drift.splitlines()[0]
        bdir = os.path.basename(cap.get("bundle_dir") or "")
        if bdir and bdir != f"{day}-roster":
            cap_s += f" (bundle {bdir})"
    else:
        cap_s = "capture ABSENT"
    narr = manifest["brief"]["narrative"]
    narr_s = f"{narr['filled_count']}/{len(NARR_SLOTS)} narrative slots filled"
    if rows is None:
        rows_s = "rows unknown"
    else:
        rows_s = f"{rows} leg{'s' if rows != 1 else ''}"
    exit_s = f"exit {exitv}" if exitv is not None else "exit unknown"
    return f"close {day}: {rows_s}, {exit_s}, {cap_s}, {narr_s}"


def append_close_receipt(root, receipt):
    path = os.path.join(root, "data", CLOSE_RUNS)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as fo:
        fo.write(json.dumps(receipt, sort_keys=True) + "\n")
    return path


def print_commit_command(root, day):
    """Read the manifest, re-derive the staged list, and print the git commands."""
    manifest_path = os.path.join(root, "data", "close", day, "manifest.json")
    if not os.path.isfile(manifest_path):
        die(f"manifest not found: {manifest_path}")

    with open(manifest_path) as fo:
        manifest = json.load(fo)

    first = manifest.get("staged_paths", [])
    cap_rel = (manifest.get("capture") or {}).get("bundle_dir")
    second = derive_staged_second(root, day, cap_rel)
    check_forbidden(first)
    check_forbidden(second)
    scan_for_forbidden(root, day, capture_dir=cap_rel)
    if first != second:
        die("staged-path mismatch between manifest and second derivation")

    msg = manifest.get("commit_message", f"close {day}")
    print("# Run the following to commit this close:")
    for p in first:
        print(f"git add {p}")
    print(f'git commit -m "{msg}"')
    print("git push origin HEAD")


def reconcile(root, day, capture_dir=None):
    """Print what the EXISTING manifest for `day` would record under the
    current capture rules.  Writes nothing -- the recorded manifest is
    history and is never rewritten.

    Bundle resolution order: explicit --capture-dir, then the same-day
    fallback data/captures/<day>-roster, then the earliest <date>-roster
    bundle dated after the close day -- the bundle a catch-up close would
    have consumed.
    """
    manifest_path = os.path.join(root, "data", "close", day, "manifest.json")
    if not os.path.isfile(manifest_path):
        die(f"manifest not found: {manifest_path}")
    with open(manifest_path) as fo:
        manifest = json.load(fo)

    resolution = None
    if capture_dir:
        resolution = f"explicit --capture-dir: {capture_dir}"
    elif os.path.isdir(os.path.join(root, "data", "captures", f"{day}-roster")):
        resolution = f"same-day fallback data/captures/{day}-roster"
    else:
        cap_root = os.path.join(root, "data", "captures")
        cands = []
        if os.path.isdir(cap_root):
            for entry in os.listdir(cap_root):
                m = re.match(r"^(\d{4}-\d{2}-\d{2})-roster$", entry)
                if (m and m.group(1) > day
                        and os.path.isdir(os.path.join(cap_root, entry))):
                    cands.append(entry)
        if cands:
            pick = sorted(cands)[0]
            capture_dir = os.path.join("data", "captures", pick)
            resolution = ("earliest <date>-roster bundle dated after the "
                          f"close day: {pick}")

    new_capture = load_capture(root, day, capture_dir)

    old_cap = manifest.get("capture") or {}
    old_bdir = old_cap.get("bundle_dir")
    staged = [p for p in manifest.get("staged_paths", [])
              if not (old_bdir and
                      (p == old_bdir or p.startswith(old_bdir + "/")))]
    if new_capture.get("present"):
        staged.extend(f["path"] for f in new_capture["files"])
    staged = sorted(set(staged))

    would = dict(manifest)
    would["capture"] = new_capture
    would["staged_paths"] = staged
    would["staged_count"] = len(staged)
    would["commit_message"] = derive_commit_message(would)

    out = {
        "day": day,
        "note": "what the recorded manifest would say under the current "
                "capture rules; the manifest on disk is unchanged",
        "resolution": resolution or "no capture bundle resolved",
        "recorded_capture": old_cap,
        "would_be": would,
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return out


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
def _st_oa_row(day, bot="GF-QQQ-IC-Ride"):
    # A minimal 26-column OA export row.
    return {
        "botName": bot, "type": "shortputspread",
        "description": "-500 put +498 put", "symbol": "QQQ", "status": "closed",
        "quantity": "1", "daysInTrade": "0", "openPrice": "0.40",
        "closePrice": "0.20", "premium": "40", "pnl": "10", "ror": "0.05",
        "returnPct": "1", "risk": "160", "ev": "1", "alpha": "0.1",
        "highReturnPct": "1", "lowReturnPct": "-0.5",
        "highReturnPctDate": "", "lowReturnPctDate": "",
        "expiration": day, "openDate": f"{day} 09:46:00",
        "closeDate": f"{day} 15:45:00", "tags": "",
        "underlyingOpen": "500", "underlyingClose": "499"
    }


EXPECTED_HEADER = [
    "botName", "type", "description", "symbol", "status", "quantity",
    "daysInTrade", "openPrice", "closePrice", "premium", "pnl", "ror",
    "returnPct", "risk", "ev", "alpha", "highReturnPct", "lowReturnPct",
    "highReturnPctDate", "lowReturnPctDate", "expiration", "openDate",
    "closeDate", "tags", "underlyingOpen", "underlyingClose"
]


def _st_write_csv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as fo:
        w = csv.writer(fo)
        w.writerow(EXPECTED_HEADER)
        for r in rows:
            w.writerow([r.get(c, "") for c in EXPECTED_HEADER])


def _st_build_bundle(root, day, bots, prev_bundle=None):
    """Create a minimal capture bundle directory for self-testing."""
    bundle = os.path.join(root, "data", "captures", f"{day}-roster")
    os.makedirs(bundle, exist_ok=True)
    os.makedirs(os.path.join(bundle, "screenshots"), exist_ok=True)

    n = len(bots)
    time_str = "195713"
    raw_name = f"01-bots-roster-recent-activity-{day}-{time_str}.txt"
    tsv_name = f"02-roster-toggles-{n}-{day}.tsv"

    # raw capture text — the captured: header derives from `day` so the
    # manifest's captured_et/capture_day fields can be checked against it.
    cap_date = datetime.date.fromisoformat(day)
    raw = os.path.join(bundle, raw_name)
    with open(raw, "w", encoding="utf-8") as fo:
        fo.write(f"# Capture bundle fixture for {day}\n"
                 f"captured: {cap_date.strftime('%a %b %d %Y')} "
                 f"19:57:13 GMT-0400 (Eastern Daylight Time)\n")

    # tsv with a drift verdict line
    tsv = os.path.join(bundle, tsv_name)
    with open(tsv, "w", encoding="utf-8") as fo:
        fo.write("# bot_name\tbot_id\tAUTOS\tEXITS\n")
        fo.write("# DRIFT VERDICT: ZERO. Not one bot changed either toggle.\n")
        for name, (bid, autos, exits) in bots.items():
            fo.write(f"{name}\t{bid}\t{autos[:2].upper()}\t{exits[:2].upper()}\n")

    # screenshot
    shot = os.path.join(bundle, "screenshots",
                        f"01-bots-roster-roster-{day}-{time_str}.png")
    with open(shot, "w") as fo:
        fo.write("png-bytes")

    # README and SHA256SUMS
    with open(os.path.join(bundle, "README.md"), "w") as fo:
        fo.write(f"# Capture bundle — {day}\n")
    sums = []
    for dirpath, _dirnames, filenames in os.walk(bundle):
        for fn in filenames:
            if fn == "SHA256SUMS.txt":
                continue
            ap = os.path.join(dirpath, fn)
            rel = os.path.relpath(ap, bundle)
            sums.append(f"{sha256(ap)}  ./{rel}\n")
    with open(os.path.join(bundle, "SHA256SUMS.txt"), "w") as fo:
        fo.write("".join(sorted(sums)))

    return bundle


def _st_write(path, content, append=False):
    os.makedirs(os.path.dirname(path), exist_ok=True) if not append or not os.path.exists(path) else None
    mode = "a" if append else "w"
    with open(path, mode) as fo:
        fo.write(content)


def selftest():
    import tempfile
    fails, results = 0, []

    def check(name, got, want):
        nonlocal fails
        ok = got == want
        fails += not ok
        results.append((ok, name, got, want))
        return ok

    tmp = tempfile.mkdtemp(prefix="close-manifest-selftest-")
    try:
        day = "2099-01-07"
        root = tmp
        data = os.path.join(root, "data")
        os.makedirs(data)

        # --- G1: gap from daily-runs.jsonl ----------------------------------
        # Fixture 1: previous close is two weekdays back (01-03 -> 01-07,
        # skipping 01-06, 01-05 is weekend; only 01-06 is unobserved).
        # Actually 2099-01-03 is a Saturday? Let's pick known weekdays.
        # 2099-01-06 is a Tuesday. Use 01-06 and 01-08.
        day1, prev1 = "2099-01-08", "2099-01-06"  # one trading day gap
        dr = os.path.join(data, "receipts")
        os.makedirs(dr)
        daily_runs = os.path.join(dr, "daily-runs.jsonl")

        def add_daily(d, final=0):
            _st_write(daily_runs, json.dumps({"day": d, "final_exit": final},
                                             sort_keys=True) + "\n", append=True)

        # Empty -> not evaluable
        gap = gap_statement(previous_close_day(daily_runs, day1), day1)
        check("G1a empty receipts -> not evaluable",
              (gap["evaluable"], gap["statement"]),
              (False, "no prior close on record"))

        # Consecutive (01-07 -> 01-08)
        _st_write(daily_runs, "", append=False)  # reset
        add_daily("2099-01-07")
        add_daily("2099-01-08")
        gap = gap_statement(previous_close_day(daily_runs, "2099-01-08"), "2099-01-08")
        check("G1b consecutive days -> no gap",
              (gap["unobserved_count"], gap["statement"]),
              (0, "previous close 2099-01-07, no gap"))

        # Two trading days back (01-06 -> 01-08, skipping 01-07)
        _st_write(daily_runs, "", append=False)
        add_daily("2099-01-06")
        add_daily("2099-01-08")
        gap = gap_statement(previous_close_day(daily_runs, "2099-01-08"), "2099-01-08")
        check("G1c two trading days back -> 1 unobserved",
              (gap["unobserved_count"], gap["unobserved_days"], gap["statement"]),
              (1, ["2099-01-07"],
               "last close 2099-01-06, 1 trading day unobserved (2099-01-07)"))

        # --- G2: market holidays are rule-derived ---------------------------
        check("G2a calendar states rule-derived US market holidays",
              gap["calendar"], "rule-derived US equity market holidays; weekends excluded")

        # --- M1: full manifest on a fixture day -----------------------------
        _st_write(daily_runs, "", append=False)
        add_daily(prev1, 0)
        add_daily(day1, 0)

        # Write daily receipt with hashes for all expected outputs.
        ledger_start = "2099-01-01"
        hashes = {}
        for rel in DAILY_OUTPUTS:
            p = os.path.join(root, rel)
            _st_write(p, f"# fixture {rel}\n", append=False)
            hashes[rel] = sha256(p)

        # Raw export
        export = os.path.join(data, "raw", f"{day1}.csv")
        _st_write_csv(export, [_st_oa_row(day1)])

        # Brief artifacts
        _st_write(os.path.join(data, "brief", f"{day1}_brief.json"),
                  json.dumps({"tape": {"underlyings": {}}}) + "\n")
        _st_write(os.path.join(data, "brief", f"{day1}_brief.html"),
                  "<html><body>brief</body></html>\n")
        _st_write(os.path.join(data, "brief", f"{day1}_p3_verdicts.tsv"),
                  "date\tbot\tverdict\n")
        _st_write(os.path.join(data, "brief", f"{day1}_tape.json"),
                  json.dumps({"date": day1, "underlyings": {}}) + "\n")
        _st_write(os.path.join(data, "brief", f"{day1}_narrative.md"),
                  "## since-yesterday\nobserved.\n## lesson\n\n")

        daily_receipt = {
            "day": day1, "final_exit": 0, "pinned": False,
            "ledger_start": ledger_start, "ledger_stale": False,
            "rows_in": 1, "rows_out": 2,
            "source_export": f"data/raw/{day1}.csv",
            "min_open_date": day1, "max_open_date": day1,
            "written_utc": "2099-01-08T00:00:00+00:00",
            "hashes": hashes,
        }
        _st_write(daily_runs, json.dumps(daily_receipt, sort_keys=True) + "\n",
                  append=False)

        # Capture bundle
        bots = {
            "Alpha-Bot": ("BOTaa111",
                          "Scheduled automations are on",
                          "Exit Options for positions managed by this bot are on"),
            "Beta-Bot": ("BOTbb222",
                         "Scheduled automations are off",
                         "Exit Options for positions managed by this bot are off"),
        }
        bundle = _st_build_bundle(root, day1, bots)

        argv = [day1]
        manifest = build_and_write_manifest(root, day1, argv)

        # (a) Every sha in the manifest equals shasum -a 256 on disk.
        sha_ok = True
        for f in manifest["capture"]["files"]:
            want = sha256(os.path.join(root, f["path"]))
            if f["sha256"] != want:
                sha_ok = False
                break
        if sha_ok:
            want = sha256(os.path.join(root, manifest["export"]["path"]))
            sha_ok = manifest["export"]["sha256"] == want
        if sha_ok:
            want = sha256(os.path.join(root, manifest["brief"]["html_path"]))
            sha_ok = manifest["brief"]["html_sha256"] == want
        check("M1a manifest shas match files on disk", sha_ok, True)

        # (b) staged_paths == second derivation == printed command
        second = derive_staged_second(root, day1)
        check("M1b manifest staged_paths match second derivation",
              manifest["staged_paths"], second)

        # Capture the commit command and check it names the same paths.
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            print_commit_command(root, day1)
        commit_text = out.getvalue()
        printed_paths = [ln.split(None, 2)[2].strip()
                         for ln in commit_text.splitlines()
                         if ln.startswith("git add ")]
        check("M1c printed git add paths match manifest",
              printed_paths, manifest["staged_paths"])

        # (d) close-runs.jsonl append-only: source opens in 'a'.
        src = open(os.path.abspath(__file__)).read()
        body = src.split("def append_close_receipt", 1)[1].split("\ndef ", 1)[0]
        check("M1d append_close_receipt opens close-runs in 'a' mode only",
              ('open(path, "a")' in body) and ('open(path, "w")' not in body),
              True)

        # Two runs -> two lines, line 1 unchanged.
        cr_path = os.path.join(data, "receipts", "close-runs.jsonl")
        before = open(cr_path).read()
        build_and_write_manifest(root, day1, argv)
        after = open(cr_path).read()
        lines = after.splitlines()
        check("M1e second run APPENDS; line 1 is byte-identical",
              (len(lines), after.startswith(before)), (2, True))

        # (c) Planted _scratch.md in the output set makes the generator refuse.
        scratch = os.path.join(data, "close", day1, "_scratch.md")
        _st_write(scratch, "\n", append=False)
        try:
            build_and_write_manifest(root, day1, argv)
            refused = False
        except SystemExit:
            refused = True
        check("M1c forbidden _scratch.md in output set is refused", refused, True)

        # Remove scratch, verify recovery.
        os.remove(scratch)
        manifest2 = build_and_write_manifest(root, day1, argv)
        check("M1c-after removing _scratch.md, manifest succeeds",
              os.path.isfile(os.path.join(data, "close", day1, "manifest.json")),
              True)

        # --- F1: top-level repo-root scan -------------------------------
        # R-2026-08-31-ROOT-SCAN-READING-B: the arm refuses on UNTRACKED /
        # NEW root entries only, so these fixtures must be real git
        # checkouts -- tracked-ness is the whole distinction under test.
        def _st_git_repo(path):
            """Init a git repo at `path` with one tracked committed file."""
            os.makedirs(path, exist_ok=True)
            env = dict(os.environ, GIT_CONFIG_GLOBAL=os.path.join(tmp, "gitcfg"),
                       GIT_CONFIG_SYSTEM=os.devnull)
            run = lambda *a: subprocess.run(
                ["git", "-C", path] + list(a), check=True,
                capture_output=True, text=True, env=env)
            run("init", "-q")
            run("config", "user.email", "selftest@example.invalid")
            run("config", "user.name", "selftest")
            open(os.path.join(path, "README.md"), "w").close()
            run("add", "README.md")
            run("commit", "-q", "-m", "seed")
            return run

        # Plant forbidden files at the root of a clean test repo and confirm
        # scan_for_forbidden refuses, names both, and exits rc=2.
        scan_root = os.path.join(tmp, "scan-root-test")
        _st_git_repo(scan_root)
        open(os.path.join(scan_root, "_root_scratch.md"), "w").close()
        open(os.path.join(scan_root, "one"), "w").close()
        err = io.StringIO()
        try:
            with contextlib.redirect_stderr(err):
                scan_for_forbidden(scan_root, day1)
            refused = False
            code = None
        except SystemExit as e:
            refused = True
            code = e.code
        msg = err.getvalue()
        check("F1a root _root_scratch.md is refused",
              (refused, code), (True, 2))
        check("F1b root file 'one' is still caught by the general rule",
              "one" in msg, True)
        check("F1c refusal names the root offending file(s)",
              "_root_scratch.md" in msg, True)

        # Confirm the scan is top-level only: a nested underscore file under
        # an otherwise-allowed subdirectory must not be discovered.
        clean_root = os.path.join(tmp, "clean-root-test")
        _st_git_repo(clean_root)
        os.makedirs(os.path.join(clean_root, "allowed"), exist_ok=True)
        open(os.path.join(clean_root, "allowed", "_nested.md"), "w").close()
        err2 = io.StringIO()
        try:
            with contextlib.redirect_stderr(err2):
                scan_for_forbidden(clean_root, day1)
            clean_ok = True
            clean_code = 0
        except SystemExit as e:
            clean_ok = False
            clean_code = e.code
        check("F1d top-level-only scan ignores nested _nested.md",
              (clean_ok, clean_code), (True, 0))

        # F1e is the Reading A / Reading B distinction itself, and it is the
        # reason this arm is narrowed: a forbidden-NAMED root entry that the
        # repository already TRACKS is not a stray and must NOT be refused.
        # Under Reading A this case exits 2 and the close pipeline dies in
        # every clean checkout of master, which carries six such files.
        tracked_root = os.path.join(tmp, "tracked-root-test")
        run_tr = _st_git_repo(tracked_root)
        open(os.path.join(tracked_root, "_dispatch-committed.md"), "w").close()
        run_tr("add", "-f", "_dispatch-committed.md")
        run_tr("commit", "-q", "-m", "commit a forbidden-named root file")
        err3 = io.StringIO()
        try:
            with contextlib.redirect_stderr(err3):
                scan_for_forbidden(tracked_root, day1)
            tracked_ok, tracked_code = True, 0
        except SystemExit as e:
            tracked_ok, tracked_code = False, e.code
        check("F1e tracked root _dispatch-committed.md is NOT refused",
              (tracked_ok, tracked_code), (True, 0))

        # F1f: the arm must skip VISIBLY, never pass silently, when tracked-ness
        # cannot be determined (a seeded scratch root is not a git checkout).
        nogit_root = os.path.join(tmp, "nogit-root-test")
        os.makedirs(nogit_root, exist_ok=True)
        open(os.path.join(nogit_root, "_root_scratch.md"), "w").close()
        err4 = io.StringIO()
        try:
            with contextlib.redirect_stderr(err4):
                scan_for_forbidden(nogit_root, day1)
            nogit_ok, nogit_code = True, 0
        except SystemExit as e:
            nogit_ok, nogit_code = False, e.code
        check("F1f non-git root skips the arm rather than refusing",
              (nogit_ok, nogit_code), (True, 0))
        check("F1g the skip is announced on stderr, not silent",
              "repo-root forbidden scan skipped" in err4.getvalue(), True)

        # (e) capture: ABSENT recorded loudly when no bundle.
        day2 = "2099-01-09"
        _st_write_csv(os.path.join(data, "raw", f"{day2}.csv"), [_st_oa_row(day2)])
        _st_write(os.path.join(data, "brief", f"{day2}_brief.json"),
                  json.dumps({"tape": {"underlyings": {}}}) + "\n")
        _st_write(os.path.join(data, "brief", f"{day2}_brief.html"),
                  "<html><body>brief</body></html>\n")
        day2_hashes = {rel: sha256(os.path.join(root, rel)) for rel in DAILY_OUTPUTS
                       if os.path.isfile(os.path.join(root, rel))}
        day2_receipt = {
            "day": day2, "final_exit": 0, "pinned": False,
            "ledger_start": "2099-01-01", "ledger_stale": False,
            "rows_in": 1, "rows_out": 2,
            "source_export": f"data/raw/{day2}.csv",
            "min_open_date": day2, "max_open_date": day2,
            "written_utc": "2099-01-09T00:00:00+00:00",
            "hashes": day2_hashes,
        }
        _st_write(daily_runs, json.dumps(day2_receipt, sort_keys=True) + "\n",
                  append=True)
        m2 = build_and_write_manifest(root, day2, [day2])
        check("M2 capture absent -> status is ABSENT",
              m2["capture"]["status"], "ABSENT")

        # --- M3: catch-up close — bundle dir is named by the CAPTURE day --
        # The T-46 defect: capture_bundle.py names the bundle by the
        # capture's own `captured:` date, so a catch-up close for `day`
        # produces <capture-day>-roster, which <day>-roster never matches.
        day3 = "2099-01-12"
        cap_day3 = "2099-01-13"
        _st_write_csv(os.path.join(data, "raw", f"{day3}.csv"),
                      [_st_oa_row(day3)])
        _st_write(os.path.join(data, "brief", f"{day3}_brief.json"),
                  json.dumps({"tape": {"underlyings": {}}}) + "\n")
        _st_write(os.path.join(data, "brief", f"{day3}_brief.html"),
                  "<html><body>brief</body></html>\n")
        day3_hashes = {rel: sha256(os.path.join(root, rel))
                       for rel in DAILY_OUTPUTS
                       if os.path.isfile(os.path.join(root, rel))}
        day3_receipt = {
            "day": day3, "final_exit": 0, "pinned": False,
            "ledger_start": "2099-01-01", "ledger_stale": False,
            "rows_in": 1, "rows_out": 2,
            "source_export": f"data/raw/{day3}.csv",
            "min_open_date": day3, "max_open_date": day3,
            "written_utc": "2099-01-12T00:00:00+00:00",
            "hashes": day3_hashes,
        }
        _st_write(daily_runs, json.dumps(day3_receipt, sort_keys=True) + "\n",
                  append=True)

        # The bundle the catch-up run produced: named by the capture's own
        # day, not the close day.
        bundle3 = _st_build_bundle(root, cap_day3, bots)
        want_captured = (datetime.date.fromisoformat(cap_day3)
                         .strftime("%a %b %d %Y")
                         + " 19:57:13 GMT-0400 (Eastern Daylight Time)")

        m3 = build_and_write_manifest(root, day3, [day3],
                                      capture_dir=bundle3)
        check("M3a catch-up close: explicit capture dir -> status PRESENT",
              m3["capture"]["status"], "PRESENT")
        check("M3b manifest records the bundle dir actually produced",
              m3["capture"]["bundle_dir"],
              os.path.join("data", "captures", f"{cap_day3}-roster"))
        check("M3c captured_et is the capture's own ET header, verbatim",
              m3["capture"]["captured_et"], want_captured)
        check("M3d capture_day is derived from that header",
              m3["capture"]["capture_day"], cap_day3)
        # The same fixture under the pre-T-46 lookup is still ABSENT: the
        # fallback <day>-roster does not exist for this close.
        check("M3e same fixture, <day>-roster fallback -> still ABSENT",
              load_capture(root, day3)["status"], "ABSENT")
        second3 = derive_staged_second(root, day3,
                                       m3["capture"]["bundle_dir"])
        check("M3f staged_paths match second derivation for produced dir",
              m3["staged_paths"], second3)
        out3 = io.StringIO()
        with contextlib.redirect_stdout(out3):
            print_commit_command(root, day3)
        printed3 = [ln.split(None, 2)[2].strip()
                    for ln in out3.getvalue().splitlines()
                    if ln.startswith("git add ")]
        check("M3g printed git add paths match the recorded bundle_dir",
              printed3, m3["staged_paths"])
        check("M3h bundle files are in staged_paths",
              m3["capture"]["tsv"] in m3["staged_paths"], True)

        # M3i: --reconcile on the recorded manifest resolves the first
        # <date>-roster after the close day and reports PRESENT.
        out4 = io.StringIO()
        with contextlib.redirect_stdout(out4):
            rec_out = reconcile(root, day3)
        check("M3i --reconcile resolves the post-day bundle -> PRESENT",
              (rec_out["would_be"]["capture"]["status"],
               rec_out["resolution"]),
              ("PRESENT",
               "earliest <date>-roster bundle dated after the close day: "
               f"{cap_day3}-roster"))

        # --- M4: the .txt / SHA256SUMS verification is real --------------
        cap_txt3 = sorted(glob.glob(os.path.join(bundle3, "01-*.txt")))[0]
        orig_txt = open(cap_txt3, "rb").read()
        with open(cap_txt3, "ab") as fo:
            fo.write(b"tampered\n")
        check("M4a altered .txt -> MISMATCH",
              load_capture(root, day3, capture_dir=bundle3)["status"],
              "MISMATCH")
        with open(cap_txt3, "wb") as fo:
            fo.write(orig_txt)

        sums3 = os.path.join(bundle3, "SHA256SUMS.txt")
        orig_sums = open(sums3, "rb").read()
        os.remove(sums3)
        check("M4b missing SHA256SUMS.txt -> MISMATCH",
              load_capture(root, day3, capture_dir=bundle3)["status"],
              "MISMATCH")
        with open(sums3, "wb") as fo:
            fo.write(orig_sums)

        moved = cap_txt3 + ".moved"
        os.rename(cap_txt3, moved)
        check("M4c no raw .txt -> MISMATCH",
              load_capture(root, day3, capture_dir=bundle3)["status"],
              "MISMATCH")
        os.rename(moved, cap_txt3)

        # --- M5: --capture-dir validation --------------------------------
        outside = os.path.join(tmp, "elsewhere-roster")
        os.makedirs(outside, exist_ok=True)
        try:
            load_capture(root, day3, capture_dir=outside)
            refused_outside = False
        except SystemExit:
            refused_outside = True
        check("M5a --capture-dir outside data/captures is refused",
              refused_outside, True)
        try:
            load_capture(root, day3,
                         capture_dir="data/captures/2099-12-31-roster")
            refused_missing = False
        except SystemExit:
            refused_missing = True
        check("M5b explicit but missing capture dir is FATAL, not ABSENT",
              refused_missing, True)

    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("SELF-TEST — close_manifest.py")
    print("=" * 74)
    for ok, name, got, want in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
        if not ok:
            print(f"        got  {got!r}\n        want {want!r}")
    print("-" * 74)
    print(f"{len(results) - fails}/{len(results)} passed")
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("day", nargs="?",
                    help="trading day (YYYY-MM-DD)")
    ap.add_argument("--root", default=None,
                    help="output root (default: $FLEET_ROOT or repo)")
    ap.add_argument("--argv", default=None,
                    help="JSON list of the close argv (default: $FLEET_CLOSE_ARGV)")
    ap.add_argument("--capture-dir", default=None,
                    help="capture bundle dir produced by this run (close.sh "
                         "passes the dir capture_bundle.py wrote); default: "
                         "data/captures/<day>-roster")
    ap.add_argument("--commit-command", action="store_true",
                    help="print the derived commit command for this close")
    ap.add_argument("--reconcile", action="store_true",
                    help="print what the existing manifest for DAY would say "
                         "under the current capture rules; writes nothing")
    ap.add_argument("--selftest", action="store_true",
                    help="run the fixture-based self-test")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    if not args.day:
        ap.error("day is required unless --selftest")

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", args.day):
        die(f"day must be YYYY-MM-DD, got {args.day!r}")

    root = resolve_root(args.root)

    if args.argv:
        try:
            argv = json.loads(args.argv)
        except (ValueError, TypeError) as e:
            die(f"--argv is not valid JSON: {e}")
    else:
        raw = os.environ.get("FLEET_CLOSE_ARGV")
        if raw:
            try:
                argv = json.loads(raw)
            except (ValueError, TypeError):
                argv = [args.day]
        else:
            argv = [args.day]

    if args.commit_command:
        print_commit_command(root, args.day)
    elif args.reconcile:
        reconcile(root, args.day, capture_dir=args.capture_dir)
    else:
        build_and_write_manifest(root, args.day, argv,
                                 capture_dir=args.capture_dir)


if __name__ == "__main__":
    main()
