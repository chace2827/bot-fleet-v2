#!/usr/bin/env python3
"""Lessons index — turn the daily briefs' write-only "day's lesson" into a
searchable, tagged index (backlog COCKPIT LANE step 4; cleanup-proposal.md
§4 item 6).

SOURCE: data/brief/<date>_brief.json (structured — preferred). Each card's
`rows` list has a "Verdict" row whose `actual` string is built by
daily_brief.py as:
    f"P/L ${day_pnl:,.0f} · {grade.upper()} — {lesson}"
(see daily_brief.py's build_card()/_lesson()). There is NO dedicated
`lesson` JSON key — the lesson clause is the tail of that Verdict row's
`actual` string, after the FIRST " — " that follows the grade token (the
lesson text can itself contain an em-dash, e.g. "good loss — design held,
tape unlucky", so we split on the grade marker, not on the last dash).

FALLBACK: docs/session-log.md free-text "lesson" mentions. Investigated:
session-log.md has no structured per-(date,bot) lesson convention (only ~2
ad-hoc narrative mentions of the word "lesson", not one per graded bot-day) —
so the fallback parser is a best-effort regex over dated section lines and
will typically find nothing for days the brief JSON already covers. It exists
so the script doesn't hard-fail if a brief JSON is ever missing for an
ingested day; it is NOT expected to contribute rows today.

TAGGING (fixed vocabulary, simple keyword rules — NOT an ML classifier):
    entry-timing | hedge | filter | regime | sizing | other
See TAG_RULES below for the exact keyword-to-tag map, checked in order;
first match wins.

OUTPUT: data/lessons.csv — date, bot, tag, lesson. Deduped on (date, bot).
This script has no per-day CLI filter (it always rescans every brief JSON on
disk + all of session-log.md), so each run is a full, idempotent REBUILD of
the CSV from current source — not an upsert-only-the-touched-day like
compliance.csv/hedge_tournament.csv. Re-running never duplicates a row, and
correctly drops a row if its source lesson is later removed/reclassified.

Usage: python3 scripts/lessons.py
Run AFTER daily_brief.py (needs that day's brief JSON) and BEFORE report.py.
"""
import csv, os, re, json, glob, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")
BRIEF = os.path.join(D, "brief")
OUT_CSV = os.path.join(D, "lessons.csv")
SESSION_LOG = os.path.join(ROOT, "docs", "session-log.md")

TAGS = ["entry-timing", "hedge", "filter", "regime", "sizing", "other"]

# Keyword rules, checked IN ORDER — first match wins. Deliberately simple
# substring checks on the lowercased lesson text (+ grade/bot context where
# noted); documented here rather than in a separate spec per the project's
# "no new docs" rule.
TAG_RULES = [
    ("entry-timing", ["entry", "bell drift", "late", "before 11:00", "re-entry", "reentry",
                       "first entry", "timing"]),
    ("hedge", ["hedge", "naked", "cut", "stop", "s2", "defang", "convexity", "breach"]),
    ("filter", ["filter", "range075", "no-go", "outside", "band", "gate"]),
    ("regime", ["regime", "trend", "chop", "drift", "tape unlucky", "vol", "vix"]),
    ("sizing", ["sizing", "allocation", "1-lot", "risk cap", "position size", "quantity", "contract"]),
]


def load(name):
    p = os.path.join(D, name)
    return list(csv.DictReader(open(p))) if os.path.exists(p) else []


def tag_lesson(text):
    """Fixed-vocabulary keyword tagger. First TAG_RULES match wins; else 'other'."""
    low = (text or "").lower()
    for tag, keywords in TAG_RULES:
        if any(kw in low for kw in keywords):
            return tag
    return "other"


VERDICT_RE = re.compile(r"P/L \$[\-\d,.]+ · (GREEN|AMBER|RED) — (.*)$")


def extract_lesson_from_card(card):
    """Pull the lesson clause out of the Verdict row's `actual` string.
    Returns None if the card has no Verdict row or the string doesn't match
    the expected pattern (defensive — daily_brief.py's format could change)."""
    verdict = next((r for r in card.get("rows", []) if r.get("name") == "Verdict"), None)
    if not verdict:
        return None
    m = VERDICT_RE.search(verdict.get("actual", ""))
    if not m:
        return None
    return m.group(2).strip()


def from_briefs():
    """(date, bot) -> lesson text, sourced from every data/brief/*_brief.json."""
    out = {}
    for path in sorted(glob.glob(os.path.join(BRIEF, "*_brief.json"))):
        try:
            j = json.load(open(path))
        except (ValueError, OSError):
            continue
        day = j.get("date") or os.path.basename(path).replace("_brief.json", "")
        for card in j.get("cards", []):
            lesson = extract_lesson_from_card(card)
            if lesson:
                out[(day, card["bot"])] = lesson
    return out


# ----------------------------------------------------------------------------
# Fallback: docs/session-log.md free-text lesson mentions. Investigated —
# session-log.md has NO per-(date,bot) structured lesson line, just occasional
# ad-hoc prose that happens to contain the word "lesson" (including, e.g., a
# line about scheduling THIS backlog task — not a trading lesson at all). Given
# that, this fallback is deliberately narrow: it only runs for a calendar date
# that has NO brief JSON at all (a day the automated pipeline never covered),
# and even then it requires an explicit "**Key lesson" / "lesson surfaced"
# marker (not a bare substring hit) to avoid pulling in unrelated prose that
# merely mentions the word. Attributed to bot="(session-log)" since no bot is
# reliably parseable from freeform text. Expected to contribute ~0 rows today
# (every ingested day already has a brief JSON) — exists so the script
# degrades gracefully rather than silently missing a day with no automation.
SECTION_RE = re.compile(r"^##\s*(\d{4}-\d{2}-\d{2})")
LESSON_MARKER_RE = re.compile(r"key lesson|lesson surfaced", re.IGNORECASE)


def from_session_log(covered_dates):
    out = {}
    if not os.path.exists(SESSION_LOG):
        return out
    cur_date = None
    for line in open(SESSION_LOG):
        m = SECTION_RE.match(line.strip())
        if m:
            cur_date = m.group(1)
            continue
        if cur_date and cur_date not in covered_dates and LESSON_MARKER_RE.search(line):
            text = line.strip().lstrip("-").strip()
            if text:
                out[(cur_date, "(session-log)")] = text
    return out


def upsert(rows):
    """Full rebuild keyed on (date, bot), deduped. Unlike compliance.csv/
    hedge_tournament.csv (which are fed one day at a time via a CLI date arg
    and so upsert-by-touched-day), this script always rescans ALL brief JSONs
    + all of session-log.md on every run (no date filter), so the correct,
    non-stale behavior is a full rebuild from the current source of truth —
    an upsert-only-what-changed here would leave orphaned rows if a source
    lesson is later removed/reclassified (e.g. a session-log false-positive
    fixed by tightening TAG_RULES/markers)."""
    existing = {}
    for r in rows:
        existing[(r["date"], r["bot"])] = r

    # --- SHRINK GUARD ---------------------------------------------------
    # This is a full REBUILD, so a rebuild that produces nothing will happily
    # truncate a populated file. That is how the v1 lessons index would be
    # erased the first time daily.sh ran against an empty post-cutover ledger.
    # Caught by the Phase-3 n=0 dry run, 2026-07-30. Refuse rather than write.
    if os.path.exists(OUT_CSV):
        prior = list(csv.DictReader(open(OUT_CSV)))
        if prior and not existing and os.environ.get("LESSONS_ALLOW_TRUNCATE") != "1":
            print(f"lessons.py: REFUSING to truncate {os.path.relpath(OUT_CSV, ROOT)} "
                  f"from {len(prior)} rows to 0. The rebuild found no source lessons "
                  f"(expected pre-Day-0). Archive the v1 index to "
                  f"data/archive/lessons-v1.csv, then re-run with "
                  f"LESSONS_ALLOW_TRUNCATE=1 to start the post-cutover index clean.")
            return {(r_["date"], r_["bot"]): r_ for r_ in prior}

    with open(OUT_CSV, "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=["date", "bot", "tag", "lesson"])
        w.writeheader()
        for k in sorted(existing):
            row = existing[k]
            w.writerow({c: row.get(c, "") for c in ["date", "bot", "tag", "lesson"]})
    return existing


def ledger_start():
    """The cutover date, read from the run receipt build_ledger.py writes.
    Every surface downstream of the ledger is post-cutover only; the session-log
    fallback is the one input that does not come through the ledger, so it gets
    filtered here explicitly. Absent receipt => refuse the fallback rather than
    let a pre-cutover lesson in."""
    p = os.path.join(D, "ledger_meta.json")
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p)).get("ledger_start")
    except Exception:
        return None


def build():
    brief_lessons = from_briefs()
    covered_dates = {d for d, _ in brief_lessons}
    ls = ledger_start()
    fallback_lessons = from_session_log(covered_dates)
    if ls:
        fallback_lessons = {k: v for k, v in fallback_lessons.items() if k[0] >= ls}
    else:
        if fallback_lessons:
            print("lessons.py: no data/ledger_meta.json — DROPPING all "
                  f"{len(fallback_lessons)} session-log fallback lesson(s) rather "
                  "than risk admitting pre-cutover rows.")
        fallback_lessons = {}
    # fallback only fills dates with NO brief JSON coverage at all
    combined = dict(fallback_lessons)
    combined.update(brief_lessons)  # structured source wins

    rows = []
    tag_counts = collections.Counter()
    for (day, bot), lesson in combined.items():
        tag = tag_lesson(lesson)
        tag_counts[tag] += 1
        rows.append({"date": day, "bot": bot, "tag": tag, "lesson": lesson})

    all_rows = upsert(rows)

    n_brief_days = len({d for d, _ in brief_lessons})
    print(f"lessons.py: {len(brief_lessons)} graded (date,bot) lessons from "
          f"{n_brief_days} brief JSON day(s) + {len(fallback_lessons)} session-log fallback "
          f"mention(s) (only used for keys not already in a brief) "
          f"-> {len(rows)} rows written this run -> {len(all_rows)} total in lessons.csv | "
          f"tags: {dict(tag_counts)} | "
          f"reconciliation: index rows this run ({len(rows)}) == distinct graded (date,bot) "
          f"lessons available ({len(combined)}) "
          f"({'OK' if len(rows) == len(combined) else 'MISMATCH'})")
    bad_tags = [r for r in rows if r["tag"] not in TAGS]
    if bad_tags:
        print(f"lessons.py: WARNING {len(bad_tags)} rows with a tag outside the fixed vocabulary")
    return len(rows) == len(combined) and not bad_tags


if __name__ == "__main__":
    ok = build()
    raise SystemExit(0 if ok else 1)
