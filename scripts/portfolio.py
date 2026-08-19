#!/usr/bin/env python3
"""Render the portfolio board from data/portfolio.csv + docs/portfolio.template.html.

Emits portfolio.html at the repo root by replacing everything between the DATA
sentinels in the template. This file is a DATA INJECTOR, not a templating engine:
the styling lives in the template and is not this script's business.

Three facts are derived live rather than transcribed -- roster rows, roster ON
count, and the unsigned-bot count -- so the board carries at least one surface it
did not author. Everything else comes from the CSV.

Never edit portfolio.html by hand; --check is what CI runs.
"""
import argparse, csv, json, os, re, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")

SENT_A = "/* ==== DATA START ==== */"
SENT_B = "/* ==== DATA END ==== */"

STATUSES = {"Not started", "Working on it", "Ready", "Needs sign-off", "Stuck", "Done"}


def set_root(root):
    """Repoint ROOT and D at a scratch root (fixture / live separation)."""
    global ROOT, D
    ROOT = os.path.abspath(root)
    D = os.path.join(ROOT, "data")


def _die(msg):
    sys.stderr.write("FATAL: %s\n" % msg)
    raise SystemExit(2)


# ---------------------------------------------------------------- derived facts
def derive_facts():
    """Live figures read from surfaces this script does not write.

    Absent inputs yield None, never a zero -- a missing file must not render as
    'no unsigned bots'. The template shows a dash for None.
    """
    f = {"roster_rows": None, "roster_on": None, "unsigned": None}

    meta = os.path.join(D, "bots_meta.csv")
    if os.path.exists(meta):
        with open(meta, newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        f["roster_rows"] = len(rows)
        f["roster_on"] = sum(1 for r in rows if (r.get("status") or "").strip().upper() == "ON")

    status = os.path.join(ROOT, "STATUS.md")
    if os.path.exists(status):
        txt = open(status, encoding="utf-8").read()
        m = re.search(r"^##\s*.*UNSIGNED PRE-REGISTRATION BOTS.*$", txt, re.M)
        if m:
            tail = txt[m.end():]
            nxt = re.search(r"^##\s", tail, re.M)
            block = tail[: nxt.start()] if nxt else tail
            f["unsigned"] = len(re.findall(r"^-\s+\S.*$", block, re.M))
    return f


# ---------------------------------------------------------------------- reading
def read_rows(path):
    if not os.path.exists(path):
        _die("missing input: %s" % path)
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        _die("%s has no rows" % path)
    return rows


def build_data(rows, facts):
    progs = [r for r in rows if r["kind"] == "program" and r["id"].lower() != "objective"]
    items = [r for r in rows if r["kind"] == "item"]
    if not progs:
        _die("no kind=program rows -- refusing to render a board with no programs")

    pids = [p["id"] for p in progs]
    dupes = sorted({p for p in pids if pids.count(p) > 1})
    if dupes:
        _die("duplicate program id(s): %s" % ", ".join(dupes))

    seen, dup_items = set(), []
    for it in items:
        if it["id"] in seen:
            dup_items.append(it["id"])
        seen.add(it["id"])
    if dup_items:
        # a duplicate key silently reroutes a row while every other check stays green
        _die("duplicate item id(s): %s" % ", ".join(sorted(set(dup_items))))

    pset = set(pids)
    for it in items:
        if it["program"] not in pset:
            _die("item %s names unknown program %r -- dropping it would read as done"
                 % (it["id"], it["program"]))
        if it["status"] not in STATUSES:
            _die("item %s has unknown status %r (allowed: %s)"
                 % (it["id"], it["status"], ", ".join(sorted(STATUSES))))
        try:
            n = int(it["priority"])
        except (TypeError, ValueError):
            _die("item %s has non-integer priority %r" % (it["id"], it["priority"]))
        if not 1 <= n <= 4:
            _die("item %s has priority %d outside 1-4" % (it["id"], n))

    objective = ""
    for r in rows:
        if r["kind"] == "program" and r["id"].lower() == "objective":
            objective = r["title"].strip()
    if not objective:
        objective = "[ unset — one sentence, signed, changes ~never ]"

    return {
        "objective": objective,
        "facts": facts,
        "programs": [
            {"n": p["id"], "name": p["title"], "q": p["question"], "metric": p["metric"],
             "state": p["metric_state"], "note": p["metric_note"],
             "owner": p["owner"] or "Andy", "wip": p["status"] or "Idle",
             "bet": p.get("bet", ""), "kill": p.get("kill_date", ""),
             "restart": p.get("restart_trigger", "")}
            for p in progs
        ],
        "tasks": [
            [it["id"], it["program"], it["title"], it["owner"], it["status"],
             int(it["priority"]), it["est"], it["blocked_by"]]
            for it in items
        ],
    }


def render(data, template_path):
    if not os.path.exists(template_path):
        _die("missing template: %s" % template_path)
    t = open(template_path, encoding="utf-8").read()
    if t.count(SENT_A) != 1 or t.count(SENT_B) != 1:
        _die("template must contain exactly one DATA START and one DATA END sentinel")
    a, b = t.index(SENT_A), t.index(SENT_B) + len(SENT_B)
    if b <= a:
        _die("DATA END precedes DATA START in the template")
    blob = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1)
    return t[:a] + SENT_A + "\nconst DATA = " + blob + ";\n" + SENT_B + t[b:]


def generate():
    facts = derive_facts()
    rows = read_rows(os.path.join(D, "portfolio.csv"))
    data = build_data(rows, facts)
    html = render(data, os.path.join(ROOT, "docs", "portfolio.template.html"))
    return data, html


# ------------------------------------------------------------------- self-test
def _validate():
    """Build a scratch root, render it, and assert the invariants.

    Every expectation is DERIVED from the fixture it was built from; no literal
    counts appear in any predicate, because a literal freezes today's data into
    tomorrow's test.
    """
    here = ROOT
    tmp = tempfile.mkdtemp(prefix="portfolio-validate-")
    try:
        os.makedirs(os.path.join(tmp, "data"))
        os.makedirs(os.path.join(tmp, "docs"))
        hdr = ("kind,id,program,title,owner,status,priority,est,blocked_by,source,"
               "anchor,question,metric,metric_state,metric_note\n")
        prog_rows = [("PA", "Alpha"), ("PB", "Beta")]
        item_rows = [("i1", "PA", "one"), ("i2", "PA", "two"), ("i3", "PB", "three")]
        with open(os.path.join(tmp, "data", "portfolio.csv"), "w", encoding="utf-8") as fh:
            fh.write(hdr)
            for pid, name in prog_rows:
                fh.write("program,%s,%s,%s,,,,,,,,q,m,Not started,note\n" % (pid, pid, name))
            for iid, pid, title in item_rows:
                fh.write("item,%s,%s,%s,Andy,Not started,2,,,src,anchor,,,,\n" % (iid, pid, title))
        with open(os.path.join(tmp, "data", "bots_meta.csv"), "w", encoding="utf-8") as fh:
            fh.write("bot,status\na,ON\nb,OFF\nc,ON\n")
        tpl = open(os.path.join(here, "docs", "portfolio.template.html"), encoding="utf-8").read()
        open(os.path.join(tmp, "docs", "portfolio.template.html"), "w", encoding="utf-8").write(tpl)

        set_root(tmp)
        data, html = generate()
        ok = 0

        assert len(data["programs"]) == len(prog_rows); ok += 1
        assert len(data["tasks"]) == len(item_rows); ok += 1
        names = {p["n"] for p in data["programs"]}
        assert all(t[1] in names for t in data["tasks"]), "orphan task"; ok += 1
        ids = [t[0] for t in data["tasks"]]
        assert len(ids) == len(set(ids)), "duplicate task id"; ok += 1
        for pid, _ in prog_rows:
            assert any(p["n"] == pid for p in data["programs"]), "program vanished"
        ok += 1
        # facts derived from the fixture, computed independently here
        meta = list(csv.DictReader(open(os.path.join(tmp, "data", "bots_meta.csv"), encoding="utf-8")))
        assert data["facts"]["roster_rows"] == len(meta); ok += 1
        assert data["facts"]["roster_on"] == sum(1 for r in meta if r["status"] == "ON"); ok += 1
        # absent STATUS.md must yield None, never 0
        assert data["facts"]["unsigned"] is None, "missing input rendered as a number"; ok += 1
        # the emitted DATA block must be valid JSON
        blob = html[html.index(SENT_A) + len(SENT_A):html.index(SENT_B)]
        parsed = json.loads(blob.strip().removeprefix("const DATA =").strip().rstrip(";"))
        assert parsed["tasks"] == data["tasks"]; ok += 1
        # idempotent
        assert render(build_data(read_rows(os.path.join(tmp, "data", "portfolio.csv")),
                                 derive_facts()),
                      os.path.join(tmp, "docs", "portfolio.template.html")) == html; ok += 1
        # unknown program must be fatal, not silently dropped
        with open(os.path.join(tmp, "data", "portfolio.csv"), "a", encoding="utf-8") as fh:
            fh.write("item,i9,PZ,rogue,Andy,Not started,2,,,src,anchor,,,,\n")
        try:
            generate()
        except SystemExit:
            ok += 1
        else:
            raise AssertionError("unknown program did not fail")
        print("portfolio.py --validate: %d/%d OK" % (ok, 11))
    finally:
        set_root(here)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the committed portfolio.html differs from a fresh render; writes nothing")
    ap.add_argument("--validate", action="store_true", help="run the self-test in a scratch root")
    ap.add_argument("--root", help="repo root (default: parent of scripts/)")
    a = ap.parse_args()

    if a.root:
        set_root(a.root)
    elif os.environ.get("FLEET_ROOT"):
        set_root(os.environ["FLEET_ROOT"])

    if a.validate:
        _validate()
        return

    data, html = generate()
    out = os.path.join(ROOT, "portfolio.html")

    if a.check:
        if not os.path.exists(out):
            sys.stderr.write("DRIFT: %s does not exist\n" % out)
            raise SystemExit(1)
        cur = open(out, encoding="utf-8").read()
        if cur != html:
            sys.stderr.write("DRIFT: portfolio.html is stale -- run scripts/portfolio.py\n")
            raise SystemExit(1)
        print("portfolio.html up to date (%d programs, %d items)"
              % (len(data["programs"]), len(data["tasks"])))
        return

    open(out, "w", encoding="utf-8").write(html)
    print("wrote %s -- %d programs, %d items"
          % (os.path.relpath(out, ROOT), len(data["programs"]), len(data["tasks"])))


if __name__ == "__main__":
    main()
