#!/usr/bin/env python3
"""Render the fleet roster board from data/bots_meta.csv, docs/pre-registration-ledger.md,
data/trades.csv and STATUS.md.

Two layers on one page:
  INVENTORY  -- every bot: what it IS (family, pillar, role, hedge code, ON/OFF)
  SCOREBOARD -- for bots carrying a pre-registration entry: what it was PREDICTED to do
                (HYPOTHESIS), how (MECHANISM), what would kill it, and what it actually did

Family is DERIVED here, not stored. bots_meta.csv is roster authority (CLAUDE.md 2.5) and
adding a column to it is a data decision, not a rendering one -- so the taxonomy lives in
FAMILY_RULES below and any bot it cannot place is FATAL, never silently bucketed as "other".

Never edit roster.html by hand; --check is what CI runs.
"""
import argparse, collections, csv, json, os, re, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")

SENT_A = "/* ==== DATA START ==== */"
SENT_B = "/* ==== DATA END ==== */"


def set_root(root):
    global ROOT, D
    ROOT = os.path.abspath(root)
    D = os.path.join(ROOT, "data")


def _die(msg):
    sys.stderr.write("FATAL: %s\n" % msg)
    raise SystemExit(2)


# ------------------------------------------------------------------- taxonomy
# (order matters -- first match wins). Each entry: (label, predicate over (bot, row)).
FAMILY_RULES = [
    ("Archived clones",        lambda b, r: "ARCHIVED" in b),
    ("Greenfield QQQ IC",      lambda b, r: b.startswith("GF-QQQ-IC-")),
    ("SPX FastPT25 line",      lambda b, r: b.startswith("IC-SPX-FastPT25")),
    ("SPX Fortress",           lambda b, r: b.startswith("IC-SPX-Fortress")),
    ("QQQ hedge tournament",   lambda b, r: b.startswith("QQQ-IC-0DTE-Hedge")),
    ("Range075 experiments",   lambda b, r: "Range075" in b),
    ("QQQ Fortress line",      lambda b, r: b.startswith("QQQ-IC-0DTE-Fortress")),
    ("QQQ controls / baseline",
     lambda b, r: b in {"QQQ-IC-0DTE-Baseline", "QQQ-IC-0DTE-Raw-HoldToExp",
                        "QQQ-IC-0DTE-InverseFilter-HoldToExp"}),
    ("SPX directional",        lambda b, r: b.startswith("DIR-SPX-")),
    ("Killed mirrors",         lambda b, r: r.get("pillar") == "OA-Mirror"
                                            and (r.get("superseded") or "").strip() == "kill"),
    ("Straddler mirrors",      lambda b, r: b in {"QQQ long call", "Tasty Condor"}),
    ("Live mirrors",           lambda b, r: r.get("pillar") == "OA-Mirror"),
]

FAMILY_ORDER = [f for f, _ in FAMILY_RULES]


def family_of(bot, row):
    for label, pred in FAMILY_RULES:
        if pred(bot, row):
            return label
    _die("bot %r matches no family rule -- add a rule rather than let it fall into 'other', "
         "because an unclassified bot silently disappears from every family view" % bot)


# --------------------------------------------------------------- ledger parse
LEDGER_FIELD = re.compile(r"^([A-Z][A-Z /\-]+?)\s{2,}(.*)$")


def _clean_heading(h):
    h = re.sub(r"^(PR|INC)-\d+\s*[—-]\s*", "", h)
    h = re.sub(r"\s*\((clone|original).*$", "", h)
    h = re.sub(r"\s*[—✅⚠].*$", "", h)
    return h.strip().strip("`").strip()


def read_ledger(path):
    """Entries are fenced key/value blocks; the bot name is a BOT field on some and the
    nearest preceding ### heading on the rest. Both forms are read -- keying on only one
    silently loses two thirds of the file."""
    if not os.path.exists(path):
        return {}
    txt = open(path, encoding="utf-8").read()
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"^###\s+(.*?)\s*$", txt, re.M)]
    out = {}
    for m in re.finditer(r"```\n(ID\s+.*?)\n```", txt, re.S):
        d, k = {}, None
        for line in m.group(1).split("\n"):
            fm = LEDGER_FIELD.match(line)
            if fm:
                k = fm.group(1).strip()
                d[k] = fm.group(2).strip()
            elif k and line.strip():
                d[k] += " " + line.strip()
        prior = [t for p, t in heads if p < m.start()]
        name = (d.get("BOT", "").split("  ")[0].strip().strip("`")
                or (_clean_heading(prior[-1]) if prior else ""))
        if name:
            out[name] = d
    return out


def unsigned_from_status(path):
    """The DO-NOT-SWITCH-ON list. Returns None when STATUS.md is absent -- an empty set
    would render as 'nothing unsigned', which is the dangerous reading."""
    if not os.path.exists(path):
        return None
    txt = open(path, encoding="utf-8").read()
    m = re.search(r"^##\s*.*UNSIGNED PRE-REGISTRATION BOTS.*$", txt, re.M)
    if not m:
        return None
    tail = txt[m.end():]
    nxt = re.search(r"^##\s", tail, re.M)
    block = tail[: nxt.start()] if nxt else tail
    return {b.strip() for b in re.findall(r"^-\s+(\S.*?)\s*$", block, re.M)}


def read_trades(path):
    n, pnl = collections.Counter(), collections.defaultdict(float)
    if not os.path.exists(path):
        return n, pnl, None
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    for r in rows:
        b = r.get("bot")
        if not b:
            continue
        n[b] += 1
        try:
            pnl[b] += float(r.get("pnl") or 0)
        except ValueError:
            pass
    return n, pnl, len(rows)


SAMPLE_N = re.compile(r"n\s*=\s*(\d+)")


def build_data():
    meta_path = os.path.join(D, "bots_meta.csv")
    if not os.path.exists(meta_path):
        _die("missing %s" % meta_path)
    meta = list(csv.DictReader(open(meta_path, newline="", encoding="utf-8")))
    if not meta:
        _die("bots_meta.csv has no rows")

    names = [r["bot"] for r in meta]
    dupes = sorted({b for b in names if names.count(b) > 1})
    if dupes:
        # the roster-invariant defect class: a dup row reroutes P&L with every guard green
        _die("duplicate bot row(s) in bots_meta.csv: %s" % ", ".join(dupes))

    led = read_ledger(os.path.join(ROOT, "docs", "pre-registration-ledger.md"))
    unsigned = unsigned_from_status(os.path.join(ROOT, "STATUS.md"))
    n, pnl, trade_rows = read_trades(os.path.join(D, "trades.csv"))

    bots = []
    for r in meta:
        b = r["bot"]
        e = led.get(b, {})
        tgt = None
        if e.get("SAMPLE TARGET"):
            mm = SAMPLE_N.search(e["SAMPLE TARGET"])
            if mm:
                tgt = int(mm.group(1))
        is_unsigned = None if unsigned is None else (b in unsigned)
        cnt = n.get(b, 0)

        if is_unsigned:
            verdict = "UNSIGNED"
        elif not e:
            verdict = "No pre-registration"
        elif cnt == 0:
            verdict = "Silent"
        elif tgt is None:
            # a bot with no stated target cannot be "at" one -- saying so would manufacture
            # a pass out of a missing number
            verdict = "No target stated"
        elif cnt < tgt:
            verdict = "Below sample"
        else:
            verdict = "At sample"

        bots.append({
            "bot": b,
            "family": family_of(b, r),
            "pillar": r.get("pillar", ""),
            "role": r.get("role", ""),
            "underlying": r.get("underlying", ""),
            "status": r.get("status", ""),
            "hedge": r.get("hedge", ""),
            "focus": (r.get("focus") or "").strip() == "yes",
            "champion": (r.get("champion") or "").strip() == "yes",
            "superseded": (r.get("superseded") or "").strip(),
            "strike_fix": (r.get("strike_fix") or "").strip(),
            "pr": e.get("ID", ""),
            "hypothesis": e.get("HYPOTHESIS", ""),
            "mechanism": e.get("MECHANISM", ""),
            "kill": e.get("KILL CRITERION", ""),
            "sample_target": tgt,
            "sample_raw": e.get("SAMPLE TARGET", ""),
            "max_loss": e.get("MAX LOSS", ""),
            "signed": e.get("SIGNED", ""),
            "n": cnt,
            "pnl": round(pnl.get(b, 0.0), 2),
            "unsigned": is_unsigned,
            "verdict": verdict,
        })

    fams = [f for f in FAMILY_ORDER if any(x["family"] == f for x in bots)]
    return {
        "generated_from": {"bots_meta_rows": len(meta), "ledger_entries": len(led),
                           "trade_rows": trade_rows,
                           "unsigned_known": unsigned is not None},
        "families": fams,
        "bots": bots,
    }


def render(data, template_path):
    if not os.path.exists(template_path):
        _die("missing template: %s" % template_path)
    t = open(template_path, encoding="utf-8").read()
    if t.count(SENT_A) != 1 or t.count(SENT_B) != 1:
        _die("template needs exactly one DATA START and one DATA END sentinel")
    a, b = t.index(SENT_A), t.index(SENT_B) + len(SENT_B)
    blob = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1)
    return t[:a] + SENT_A + "\nconst DATA = " + blob + ";\n" + SENT_B + t[b:]


def generate():
    d = build_data()
    return d, render(d, os.path.join(ROOT, "docs", "roster.template.html"))


def _validate():
    here = ROOT
    tmp = tempfile.mkdtemp(prefix="roster-validate-")
    ok = 0
    try:
        os.makedirs(os.path.join(tmp, "data"))
        os.makedirs(os.path.join(tmp, "docs"))
        meta_rows = [("GF-QQQ-IC-Ride", "IC", "control", "QQQ", "ON"),
                     ("DIR-SPX-Put-Control", "Directional", "control", "SPX", "OFF"),
                     ("Nigiri-Paper-v1", "OA-Mirror", "mirror-watch", "SPX", "ON")]
        with open(os.path.join(tmp, "data", "bots_meta.csv"), "w", encoding="utf-8") as f:
            f.write("bot,pillar,role,underlying,status,champion,epoch_boundary,hedge,"
                    "strike_fix,superseded,focus,notes,ops_class\n")
            for b, p, r, u, s in meta_rows:
                f.write("%s,%s,%s,%s,%s,,,,,,,,\n" % (b, p, r, u, s))
        with open(os.path.join(tmp, "data", "trades.csv"), "w", encoding="utf-8") as f:
            f.write("bot,pnl\nGF-QQQ-IC-Ride,10\nGF-QQQ-IC-Ride,5\n")
        with open(os.path.join(tmp, "docs", "pre-registration-ledger.md"), "w", encoding="utf-8") as f:
            f.write("### PR-14 — `GF-QQQ-IC-Ride`\n```\n"
                    "ID               PR-14\n"
                    "HYPOTHESIS       does a thing\n"
                    "SAMPLE TARGET    n = 100 condors.\n"
                    "SIGNED           2026-08-09\n```\n")
        tpl = open(os.path.join(here, "docs", "roster.template.html"), encoding="utf-8").read()
        open(os.path.join(tmp, "docs", "roster.template.html"), "w", encoding="utf-8").write(tpl)

        set_root(tmp)
        d, html = generate()

        assert len(d["bots"]) == len(meta_rows); ok += 1
        # every bot placed in a family, none unclassified
        assert all(x["family"] for x in d["bots"]); ok += 1
        assert set(x["family"] for x in d["bots"]) <= set(FAMILY_ORDER); ok += 1
        # families listed are exactly those in use, in canonical order
        used = [f for f in FAMILY_ORDER if any(x["family"] == f for x in d["bots"])]
        assert d["families"] == used; ok += 1
        # trades joined by name, counted independently here
        tr = list(csv.DictReader(open(os.path.join(tmp, "data", "trades.csv"), encoding="utf-8")))
        want = collections.Counter(t["bot"] for t in tr)
        assert all(x["n"] == want.get(x["bot"], 0) for x in d["bots"]); ok += 1
        assert sum(x["n"] for x in d["bots"]) == len(tr); ok += 1
        # ledger fields land on the right bot and nowhere else
        ride = [x for x in d["bots"] if x["bot"] == "GF-QQQ-IC-Ride"][0]
        assert ride["pr"] == "PR-14" and ride["sample_target"] == 100; ok += 1
        assert all(not x["pr"] for x in d["bots"] if x["bot"] != "GF-QQQ-IC-Ride"); ok += 1
        # absent STATUS.md must not read as "nothing unsigned"
        assert all(x["unsigned"] is None for x in d["bots"]); ok += 1
        assert d["generated_from"]["unsigned_known"] is False; ok += 1
        # verdicts derived, not literal
        assert ride["verdict"] == "Below sample"; ok += 1
        assert [x for x in d["bots"] if x["bot"] == "DIR-SPX-Put-Control"][0]["verdict"] \
            == "No pre-registration"; ok += 1
        # a traded bot with a pre-reg entry but NO parsed target must not read as "At sample"
        assert all(x["verdict"] != "At sample" for x in d["bots"] if x["sample_target"] is None); ok += 1
        # valid JSON + idempotent
        blob = html[html.index(SENT_A) + len(SENT_A):html.index(SENT_B)]
        json.loads(blob.strip().removeprefix("const DATA =").strip().rstrip(";")); ok += 1
        assert render(build_data(), os.path.join(tmp, "docs", "roster.template.html")) == html; ok += 1
        # a duplicate roster row is fatal
        with open(os.path.join(tmp, "data", "bots_meta.csv"), "a", encoding="utf-8") as f:
            f.write("GF-QQQ-IC-Ride,IC,control,QQQ,ON,,,,,,,,\n")
        try:
            build_data()
        except SystemExit:
            ok += 1
        else:
            raise AssertionError("duplicate bots_meta row did not fail")
        print("roster.py --validate: %d/16 OK" % ok)
    finally:
        set_root(here)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if roster.html differs from a fresh render; writes nothing")
    ap.add_argument("--validate", action="store_true", help="self-test in a scratch root")
    ap.add_argument("--root")
    a = ap.parse_args()
    if a.root:
        set_root(a.root)
    elif os.environ.get("FLEET_ROOT"):
        set_root(os.environ["FLEET_ROOT"])

    if a.validate:
        _validate()
        return

    d, html = generate()
    out = os.path.join(ROOT, "roster.html")
    if a.check:
        if not os.path.exists(out):
            sys.stderr.write("DRIFT: %s does not exist\n" % out)
            raise SystemExit(1)
        if open(out, encoding="utf-8").read() != html:
            sys.stderr.write("DRIFT: roster.html is stale -- run scripts/roster.py\n")
            raise SystemExit(1)
        print("roster.html up to date (%d bots, %d families)"
              % (len(d["bots"]), len(d["families"])))
        return
    open(out, "w", encoding="utf-8").write(html)
    print("wrote %s -- %d bots, %d families"
          % (os.path.relpath(out, ROOT), len(d["bots"]), len(d["families"])))


if __name__ == "__main__":
    main()
