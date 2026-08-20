#!/usr/bin/env python3
"""render_brief.py — turn the daily pack into the readable brief.

`daily_brief.py` writes data/brief/<DAY>_brief.json and calls it "structured pack
Claude renders" (daily_brief.py:14). This is that renderer. Before it existed the
loop produced a JSON nobody opened, and the reading step of the daily ritual was
done by hand or not at all.

Reads   data/brief/<DAY>_brief.json      (REQUIRED — tape + cards + grades)
        data/brief/<DAY>_p3_verdicts.tsv (optional — says so when absent)
        data/trades.csv                  (REQUIRED — what actually opened)
        data/brief/<PREV>_brief.json     (optional — for the since-yesterday delta)
Writes  data/brief/<DAY>_brief.html

It renders SECTIONS 1-5 AND THE VERDICT SCAFFOLD MECHANICALLY. It does NOT write
the narrative: §0's grading of yesterday's watch list, §6's lesson, and tomorrow's
watch are judgment, and it emits labelled empty slots for them rather than
generating filler. A slot left unfilled is visible on the page as unfilled.

⛔ RULES THIS FILE OBEYS
  - No figure is a literal. Every number is derived from an input file at run time.
    A day-specific constant in here would silently mis-describe every other day.
  - An ABSENT value never falls through to a pass. Missing evidence renders as
    NOT EVALUABLE with the missing artifact named, never as 0, "clean", or "-".
  - Failure is loud. A missing required input exits non-zero with the path.

Usage:  python3 scripts/render_brief.py [YYYY-MM-DD] [--root R] [--check]
        no date -> newest <DAY>_brief.json in data/brief/
        --check -> render every day that has a pack, assert invariants, write nothing
"""
import argparse, csv, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Bot hue assignment is positional, not hard-coded per bot: bot names change,
# and a name->colour map would silently mis-colour a renamed bot.
HUES = ["#c2543d", "#2f7d78", "#6b5b95", "#b07d1f", "#3f6f4a", "#8a4b6b"]
PRICE = "#3d5a8a"

def die(msg, code=2):
    sys.stderr.write("render_brief.py: FATAL: %s\n" % msg)
    sys.exit(code)

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def money(v):
    if v is None: return "&mdash;"
    return ("&minus;$%s" % format(abs(int(round(v))), ",")) if v < 0 else ("$%s" % format(int(round(v)), ","))

def pct(v, dp=2, sign=True):
    if v is None: return "&mdash;"
    return ("%+.*f%%" if sign else "%.*f%%") % (dp, v)

def fnum(s):
    try:
        if s is None or str(s).strip() == "": return None
        return float(s)
    except (TypeError, ValueError):
        return None

# ---------------------------------------------------------------- inputs
def load_pack(root, day):
    p = os.path.join(root, "data", "brief", "%s_brief.json" % day)
    if not os.path.exists(p):
        die("required pack not found: %s  (run scripts/daily.sh %s first)" % (p, day))
    with open(p) as f:
        return json.load(f), p

def load_verdicts(root, day):
    p = os.path.join(root, "data", "brief", "%s_p3_verdicts.tsv" % day)
    if not os.path.exists(p):
        return None, p
    with open(p) as f:
        return list(csv.DictReader(f, delimiter="\t")), p

def load_trades(root):
    p = os.path.join(root, "data", "trades.csv")
    if not os.path.exists(p):
        die("required ledger not found: %s" % p)
    with open(p) as f:
        return list(csv.DictReader(f)), p

def prev_pack_total(root, day, trades):
    """Ledger P/L banked BEFORE `day`, derived from the ledger itself."""
    tot = 0.0; n = 0
    for r in trades:
        od = r.get("open_date", "")
        if od and od[:10] < day:
            v = fnum(r.get("pnl"))
            if v is not None: tot += v
            n += 1
    return tot, n

# ---------------------------------------------------------------- derivations
def regime(series, prior_close, open_px, high, low, close):
    """All figures derived from the bar series. None where an input is absent."""
    px = [b["p"] for b in series if b.get("p") is not None]
    if len(px) < 3 or not prior_close:
        return None
    path = sum(abs(px[i] - px[i - 1]) for i in range(1, len(px)))
    net = px[-1] - px[0]
    flips = sum(1 for i in range(2, len(px)) if (px[i] - px[i - 1]) * (px[i - 1] - px[i - 2]) < 0)
    d = {
        "bars": len(px),
        "gap": 100.0 * (open_px - prior_close) / prior_close if open_px else None,
        "day": 100.0 * (close - prior_close) / prior_close if close else None,
        "range": 100.0 * (high - low) / prior_close if (high and low) else None,
        "path": 100.0 * path / px[0] if px[0] else None,
        "dirratio": (abs(net) / path) if path else None,
        "flips": flips,
    }
    # Label from the ratio, with the threshold stated on the page, not hidden here.
    r = d["dirratio"]
    d["label"] = "&mdash;" if r is None else ("Chop" if r < 0.15 else ("Drift" if r < 0.40 else "Trend"))
    return d

def opened_on(trades, day):
    return [r for r in trades if (r.get("open_date") or "").startswith(day)]

def by_bot(rows):
    out = {}
    for r in rows:
        out.setdefault(r.get("bot", "?"), []).append(r)
    return out

def pl_of(rows):
    vals = [fnum(r.get("pnl")) for r in rows]
    known = [v for v in vals if v is not None]
    # An absent pnl is NOT zero. Report the count so the page can say so.
    return (sum(known) if known else None), len(vals) - len(known)

def positions_of(rows):
    ids = {r.get("trade_id") for r in rows if r.get("trade_id")}
    return len(ids) if ids else len(rows)

def series_extremes(series, from_hhmm=None):
    """(low, high) over bars at/after from_hhmm. None when the window is empty —
    NEVER a default that would read as 'no breach'."""
    bars = [b for b in series if (from_hhmm is None or b.get("t", "") >= from_hhmm)]
    los = [b["l"] for b in bars if b.get("l") is not None]
    his = [b["h"] for b in bars if b.get("h") is not None]
    if not los or not his:
        return None, None
    return min(los), max(his)

def breach_rows(day_rows, tapes):
    """One row per (position, short strike) with the post-entry extreme.
    An empty price window yields NOT EVALUABLE, not NO BREACH (defect class F-1)."""
    out = []
    for r in day_rows:
        u = r.get("underlying")
        t = tapes.get(u)
        entry = (r.get("open_date") or "")[11:16] or None
        for side, key in (("put", "short_put"), ("call", "short_call")):
            k = fnum(r.get(key))
            if k is None:
                continue
            if not t or not t.get("series"):
                out.append({"bot": r.get("bot"), "u": u, "side": side, "strike": k,
                            "extreme": None, "verdict": "NOT EVALUABLE",
                            "why": "no tape series for %s" % u, "entry": entry})
                continue
            lo, hi = series_extremes(t["series"], entry)
            if lo is None:
                out.append({"bot": r.get("bot"), "u": u, "side": side, "strike": k,
                            "extreme": None, "verdict": "NOT EVALUABLE",
                            "why": "empty price window after %s" % (entry or "open"), "entry": entry})
                continue
            ext = lo if side == "put" else hi
            hit = (ext <= k) if side == "put" else (ext >= k)
            out.append({"bot": r.get("bot"), "u": u, "side": side, "strike": k,
                        "extreme": ext, "verdict": "BREACH" if hit else "NO BREACH",
                        "why": "", "entry": entry,
                        "clear": (ext - k) if side == "put" else (k - ext)})
    return out

# ---------------------------------------------------------------- narrative
NARR_SLOTS = ("since-yesterday", "convexity", "lesson", "tomorrow", "fire", "strategy")

def load_narrative(root, day):
    """data/brief/<DAY>_narrative.md - the judgment half of the brief, versioned.

    Sections are `## slot-name` using the names in NARR_SLOTS. An absent file or
    an absent section renders as a visible UNFILLED slot; it is never faked and
    never silently dropped.
    """
    path = os.path.join(root, "data", "brief", "%s_narrative.md" % day)
    if not os.path.exists(path):
        return {}, path
    out, cur = {}, None
    for line in open(path):
        m = re.match(r"^##\s+([a-z-]+)\s*$", line.strip())
        if m:
            cur = m.group(1)
            if cur not in NARR_SLOTS:
                die("narrative %s: unknown section %r (allowed: %s)" % (path, cur, ", ".join(NARR_SLOTS)))
            out[cur] = []
        elif cur is not None:
            out[cur].append(line.rstrip("\n"))
    return {k: md(v) for k, v in out.items() if any(x.strip() for x in v)}, path

def md(lines):
    """Deliberately small markdown: paragraphs, - bullets, 1. items, **bold**, `code`."""
    def inline(t):
        t = esc(t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"`(.+?)`", r'<span class="mono">\1</span>', t)
        return t
    o, buf, mode = [], [], [None]
    def flush():
        if not buf: return
        if mode[0] == "ul": o.append("<ul>%s</ul>" % "".join("<li>%s</li>" % inline(x) for x in buf))
        elif mode[0] == "ol": o.append("<ol>%s</ol>" % "".join("<li>%s</li>" % inline(x) for x in buf))
        else: o.append("<p>%s</p>" % inline(" ".join(buf)))
        buf[:] = []
    for ln in lines:
        st = ln.strip()
        if not st:
            flush(); mode[0] = None; continue
        if st.startswith("- "):
            if mode[0] != "ul": flush(); mode[0] = "ul"
            buf.append(st[2:])
        elif re.match(r"^\d+\.\s", st):
            if mode[0] != "ol": flush(); mode[0] = "ol"
            buf.append(re.sub(r"^\d+\.\s", "", st))
        else:
            if mode[0] in ("ul", "ol"): flush(); mode[0] = None
            buf.append(st)
    flush()
    return "".join(o)


# ---------------------------------------------------------------- chart
W, H, ML, MR, MT, MB = 980, 300, 54, 160, 16, 30
PW, PH = W - ML - MR, H - MT - MB

def svg_chart(series, prior_close, marks, strikes, band, title):
    """% change from prior close. Y range adapts to the data so a big day is not
    clipped; gridline step stays 0.25% until the range forces coarser."""
    pts = [(b["t"], 100.0 * (b["p"] - prior_close) / prior_close) for b in series if b.get("p") is not None]
    if len(pts) < 2:
        return '<p class="note">No usable bar series for %s.</p>' % esc(title)
    vals = [v for _, v in pts] + [s[1] for s in strikes]
    if band: vals += [band[0], band[1]]
    span = max(1.0, max(abs(min(vals)), abs(max(vals))) * 1.15)
    step = 0.25 if span <= 1.25 else (0.5 if span <= 2.5 else 1.0)
    ymin, ymax = -span, span
    n = len(pts)
    X = lambda i: ML + PW * i / (n - 1)
    Y = lambda v: MT + PH * (ymax - v) / (ymax - ymin)
    o = ['<svg viewBox="0 0 %d %d" width="100%%" role="img" aria-label="%s">' % (W, H, esc(title))]
    o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#fbfbfa"/>' % (ML, MT, PW, PH))
    if band:
        y1, y2 = Y(band[1]), Y(band[0])
        o.append('<rect x="%d" y="%.1f" width="%d" height="%.1f" fill="#2f7d78" opacity="0.07"/>' % (ML, y1, PW, y2 - y1))
        for yy in (y1, y2):
            o.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="#2f7d78" stroke-dasharray="4 3" opacity=".55"/>' % (ML, ML + PW, yy, yy))
    v = -span
    while v <= span + 1e-9:
        yy = Y(v); zero = abs(v) < 1e-9
        o.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"/>'
                 % (ML, ML + PW, yy, yy, "#8a8a85" if zero else "#e3e3e0", "1.2" if zero else "1"))
        o.append('<text x="%d" y="%.1f" text-anchor="end" font-size="10" fill="#6b6b66">%+.2f%%</text>' % (ML - 8, yy + 3.5, v))
        v = round(v + step, 4)
    for i, (t, _) in enumerate(pts):
        if t.endswith(":00"):
            o.append('<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" stroke="#eeeeeb"/>' % (X(i), X(i), MT, MT + PH))
            o.append('<text x="%.1f" y="%d" text-anchor="middle" font-size="10" fill="#6b6b66">%s</text>' % (X(i), MT + PH + 16, t))
    for lbl, val, col in strikes:
        yy = Y(val)
        o.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="%s" stroke-width="1.4" stroke-dasharray="7 4"/>' % (ML, ML + PW, yy, yy, col))
        o.append('<text x="%d" y="%.1f" font-size="10.5" fill="%s">%s</text>' % (ML + PW + 6, yy + 3.5, col, esc(lbl)))
    o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.8"/>'
             % (" ".join("%.1f,%.1f" % (X(i), Y(v)) for i, (_, v) in enumerate(pts)), PRICE))
    idx = {t: i for i, (t, _) in enumerate(pts)}
    for t, col, lab in marks:
        key = t if t in idx else next((k for k in sorted(idx) if k >= t), None)
        if key is None: continue
        i = idx[key]; v = pts[i][1]
        o.append('<circle cx="%.1f" cy="%.1f" r="6" fill="%s" stroke="#fff" stroke-width="1.6"/>' % (X(i), Y(v), col))
        o.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="10" font-weight="600" fill="%s">%s</text>' % (X(i), Y(v) - 11, col, esc(lab)))
    o.append("</svg>")
    return "".join(o)

CSS = """:root{--ink:#1c1c1a;--mut:#6b6b66;--line:#e3e3e0;--bg:#fdfdfc}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
.wrap{max-width:1020px;margin:0 auto;padding:32px 22px 80px}
h1{font-size:26px;margin:0 0 2px;letter-spacing:-.02em}
h2{font-size:12px;text-transform:uppercase;letter-spacing:.09em;color:var(--mut);
margin:38px 0 10px;padding-bottom:7px;border-bottom:1px solid var(--line)}
h3{font-size:15.5px;margin:20px 0 6px}
.sub{color:var(--mut);font-size:13.5px;margin-bottom:22px}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin:18px 0 6px}
.tile{border:1px solid var(--line);border-radius:8px;padding:11px 13px;background:#fff}
.tile .k{font-size:10.5px;text-transform:uppercase;letter-spacing:.07em;color:var(--mut)}
.tile .v{font-size:21px;font-weight:600;letter-spacing:-.02em;margin-top:3px}
.tile .n{font-size:11.5px;color:var(--mut);margin-top:1px}
table{width:100%;border-collapse:collapse;font-size:13.5px;margin:10px 0}
th{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);
border-bottom:1px solid var(--line);padding:6px 8px 6px 0;font-weight:600}
td{padding:7px 8px 7px 0;border-bottom:1px solid #f0f0ee;vertical-align:top}
td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px}
.pill{display:inline-block;font-size:10.5px;font-weight:700;letter-spacing:.04em;padding:2px 7px;border-radius:20px;white-space:nowrap}
.g{background:#e3f0e6;color:#2c6b3f}.a{background:#faf0d8;color:#8a6712}
.r{background:#f8e0da;color:#a03a22}.n{background:#ececeb;color:#5c5c58}
figure{margin:14px 0 6px;border:1px solid var(--line);border-radius:9px;background:#fff;padding:10px 8px 4px}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-size:12.5px;padding:2px 10px 10px}
.legend i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;vertical-align:middle}
.note{font-size:12.5px;color:var(--mut);margin-top:6px}
.warn{border-left:3px solid #b07d1f;background:#fdfaf2;padding:11px 15px;margin:14px 0;font-size:14px}
.slot{border:1px dashed #bdbdb8;border-radius:8px;padding:13px 15px;margin:13px 0;background:#fafaf8}
.slot .k{font-size:10.5px;text-transform:uppercase;letter-spacing:.07em;color:#8a6712;font-weight:700}
.slot p{margin:6px 0 0;color:var(--mut);font-size:13.5px}
.narr p{margin:10px 0}.narr ul,.narr ol{margin:10px 0;padding-left:22px}.narr li{margin:4px 0}"""

def tile(k, v, n=""):
    return '<div class="tile"><div class="k">%s</div><div class="v">%s</div><div class="n">%s</div></div>' % (k, v, n)

def slot(key, name, hint, narr):
    if narr.get(key):
        return '<div class="narr">%s</div>' % narr[key]
    return ('<div class="slot"><div class="k">&#9679; NARRATIVE SLOT &mdash; %s</div>'
            '<p>%s</p><p><em>Unfilled. Write it in <span class="mono">data/brief/&lt;DAY&gt;_narrative.md</span> '
            'under <span class="mono">## %s</span>. This section is judgment and is not auto-generated; '
            'a renderer that wrote it would be inventing it.</em></p></div>'
            % (esc(name), esc(hint), esc(key)))

def render(root, day, pack, pack_path, verdicts, v_path, trades, tr_path):
    narr, narr_path = load_narrative(root, day)
    tapes = (pack.get("tape") or {}).get("underlyings") or {}
    day_rows = opened_on(trades, day)
    tot_pl, tot_missing = pl_of(day_rows)
    prev_tot, prev_n = prev_pack_total(root, day, trades)
    all_pl, all_missing = pl_of(trades)
    bots = by_bot(day_rows)
    cards = pack.get("cards") or []
    grades = pack.get("grades") or {}
    config_blind = not cards
    breaches = breach_rows(day_rows, tapes)
    n_breach = sum(1 for b in breaches if b["verdict"] == "BREACH")
    n_uneval = sum(1 for b in breaches if b["verdict"] == "NOT EVALUABLE")
    src = "reconstructed" if (pack.get("tape") or {}).get("any_reconstructed") else "tradier"

    o = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         '<title>Daily brief &mdash; %s</title><style>%s</style></head><body><div class="wrap">' % (day, CSS)]
    o.append('<h1>Daily brief &mdash; %s</h1>' % day)
    o.append('<div class="sub">tape source <span class="mono">%s</span> &middot; rendered by '
             '<span class="mono">scripts/render_brief.py</span> from <span class="mono">%s</span>, '
             '<span class="mono">%s</span>, <span class="mono">%s</span></div>'
             % (src, esc(os.path.relpath(pack_path, root)),
                esc(os.path.relpath(v_path, root)) + ("" if verdicts is not None else " (ABSENT)"),
                esc(os.path.relpath(tr_path, root))))

    # tiles
    reg_any = None
    for u, t in tapes.items():
        r = regime(t.get("series") or [], t.get("prior_close"), t.get("open"), t.get("high"), t.get("low"), t.get("close"))
        if r and reg_any is None: reg_any = (u, r)
    struct = ev = None
    if verdicts is not None:
        sus = [v for v in verdicts if v.get("verdict") == "SUSPECT"]
        struct, ev = len(sus), 0  # split lives in STATUS.md; count SUSPECT here, label it
    o.append('<div class="tiles">')
    o.append(tile("Opened today", money(tot_pl) if tot_pl is not None else "NOT EVALUABLE",
                  "%d legs &middot; %d positions &middot; %d bots%s"
                  % (len(day_rows), positions_of(day_rows), len(bots),
                     "" if not tot_missing else " &middot; %d legs missing pnl" % tot_missing)))
    o.append(tile("Ledger total", money(all_pl), "%d legs &middot; prior %s over %d legs" % (len(trades), money(prev_tot), prev_n)))
    o.append(tile("Breaches", ("NOT EVALUABLE" if (n_breach == 0 and n_uneval and n_uneval == len(breaches)) else str(n_breach)),
                  "%d short strikes checked%s" % (len(breaches), "" if not n_uneval else " &middot; %d unevaluable" % n_uneval)))
    if reg_any:
        o.append(tile("Regime (%s)" % reg_any[0], reg_any[1]["label"],
                      "dir. ratio %.3f &middot; %d flips" % (reg_any[1]["dirratio"], reg_any[1]["flips"])))
    else:
        o.append(tile("Regime", "NOT EVALUABLE", "no usable bar series"))
    o.append(tile("SUSPECT bots", ("NOT EVALUABLE" if verdicts is None else str(struct)),
                  "of %s judged" % ("&mdash;" if verdicts is None else len(verdicts))))
    o.append("</div>")
    carry_rows = [r for r in trades
                  if not (r.get("open_date") or "").startswith(day)
                  and (r.get("close_date") or "").startswith(day)]
    carry_pl, _ = pl_of(carry_rows)
    return o, dict(tapes=tapes, day_rows=day_rows, bots=bots, cards=cards, grades=grades,
                   config_blind=config_blind, breaches=breaches, verdicts=verdicts,
                   tot_pl=tot_pl, all_pl=all_pl, prev_tot=prev_tot,
                   carry_in={"rows": carry_rows, "pl": carry_pl},
                   narr=narr, narr_path=narr_path)

def render_body(root, day, ctx, o):
    tapes, day_rows, bots = ctx["tapes"], ctx["day_rows"], ctx["bots"]
    breaches, verdicts = ctx["breaches"], ctx["verdicts"]

    # §0
    o.append("<h2>&sect;0 &middot; Since yesterday</h2>")
    carry = ctx["carry_in"]
    o.append("<p>Ledger %s &rarr; <strong>%s</strong>. %s of that came from positions "
             "<strong>opened today</strong> across %d legs%s.</p>"
             % (money(ctx["prev_tot"]), money(ctx["all_pl"]),
                money(ctx["tot_pl"]) if ctx["tot_pl"] is not None else "An unevaluable amount",
                len(day_rows),
                "" if not carry["rows"] else
                ", and %s from %d multi-day position(s) opened earlier that settled today (%s)"
                % (money(carry["pl"]), len(carry["rows"]),
                   esc(", ".join(sorted({r.get("bot", "?") for r in carry["rows"]}))))))
    if carry["rows"]:
        o.append('<p class="note"><strong>&quot;Opened today&quot; and &quot;ledger delta&quot; are different '
                 'numbers and the brief states both.</strong> A multi-day position banks on the day it settles, '
                 'not the day it was opened, so the ledger can move on a day the fleet opened nothing.</p>')
    o.append(slot("since-yesterday", "grade yesterday's watch list",
                  "One row per item carried in from the previous brief, each marked played-out / did-not / still-open. "
                  "This is what makes the brief a chain rather than a snapshot.", ctx["narr"]))

    # §1
    o.append("<h2>&sect;1 &middot; The tape</h2>")
    traded = sorted({r.get("underlying") for r in day_rows if r.get("underlying")})
    if not traded:
        o.append('<p class="note">No positions opened today, so no underlying is charted.</p>')
    hue_of, hi = {}, 0
    for b in sorted(bots):
        hue_of[b] = HUES[hi % len(HUES)]; hi += 1
    for u in traded:
        t = tapes.get(u)
        if not t or not t.get("series"):
            o.append('<p class="note">%s traded today but has no tape series &mdash; <strong>NOT EVALUABLE</strong>, '
                     'not charted.</p>' % esc(u)); continue
        pc = t.get("prior_close")
        rows_u = [r for r in day_rows if r.get("underlying") == u]
        marks, seen = [], set()
        for r in sorted(rows_u, key=lambda r: r.get("open_date") or ""):
            hhmm = (r.get("open_date") or "")[11:16]
            key = (hhmm, r.get("bot"))
            if not hhmm or key in seen: continue
            seen.add(key)
        # collapse a swarm: one marker per entry minute, labelled with the count
        per_min = {}
        for r in rows_u:
            hhmm = (r.get("open_date") or "")[11:16]
            if hhmm: per_min.setdefault(hhmm, []).append(r)
        for hhmm, rs in sorted(per_min.items()):
            nb = len({x.get("bot") for x in rs})
            lab = "&#9679; %d" % len(rs) if len(rs) > 1 else "&#9679;"
            marks.append((hhmm, hue_of.get(rs[0].get("bot"), HUES[0]), lab))
        strikes = []
        for key, side in (("short_put", "put"), ("short_call", "call")):
            vals = sorted({fnum(r.get(key)) for r in rows_u if fnum(r.get(key)) is not None})
            for v in vals:
                strikes.append(("short %s %g (%s)" % (side, v, pct(100.0 * (v - pc) / pc)), 100.0 * (v - pc) / pc,
                                "#c2543d" if side == "put" else "#2f7d78"))
        o.append("<figure>")
        o.append(svg_chart(t["series"], pc, marks, strikes, None, "%s intraday" % u))
        leg = ['<span><i style="background:%s"></i>%s, %% from prior close %g</span>' % (PRICE, esc(u), pc)]
        for hhmm, rs in sorted(per_min.items()):
            leg.append('<span><i style="background:%s"></i>%s &mdash; %d leg(s), %d bot(s)</span>'
                       % (hue_of.get(rs[0].get("bot"), HUES[0]), hhmm, len(rs), len({x.get("bot") for x in rs})))
        o.append('<div class="legend">%s</div>' % "".join(leg))
        o.append("</figure>")

    # §2
    o.append("<h2>&sect;2 &middot; The read</h2>")
    regs = {}
    for u in traded:
        t = tapes.get(u) or {}
        r = regime(t.get("series") or [], t.get("prior_close"), t.get("open"), t.get("high"), t.get("low"), t.get("close"))
        if r: regs[u] = r
    vix = tapes.get("VIX")
    if regs:
        us = list(regs)
        o.append("<table><tr><th>Metric</th>%s<th>Meaning</th></tr>" % "".join('<th class="num">%s</th>' % esc(u) for u in us))
        for lbl, k, f in (("Gap from prior close", "gap", lambda v: pct(v)),
                          ("Close vs prior close", "day", lambda v: pct(v)),
                          ("Realized range", "range", lambda v: pct(v, sign=False)),
                          ("Path length", "path", lambda v: pct(v, sign=False)),
                          ("Directionality ratio", "dirratio", lambda v: "%.3f" % v),
                          ("Direction changes", "flips", lambda v: str(v))):
            cells = "".join('<td class="num">%s</td>' % (f(regs[u][k]) if regs[u].get(k) is not None else "&mdash;") for u in us)
            meaning = {"dirratio": "|net| &divide; path. &lt;0.15 chop, &lt;0.40 drift, else trend",
                       "flips": "of %d bars" % regs[us[0]]["bars"]}.get(k, "")
            o.append("<tr><td>%s</td>%s<td>%s</td></tr>" % (lbl, cells, meaning))
        if vix and vix.get("prior_close") and vix.get("close"):
            o.append('<tr><td>VIX</td><td class="num" colspan="%d">%g &rarr; %g, <strong>%s</strong></td><td></td></tr>'
                     % (len(us), vix["prior_close"], vix["close"],
                        pct(100.0 * (vix["close"] - vix["prior_close"]) / vix["prior_close"], 1)))
        o.append("</table>")
        o.append('<p class="note">Regime label per underlying: %s</p>'
                 % ", ".join("<strong>%s %s</strong>" % (esc(u), regs[u]["label"]) for u in us))
    else:
        o.append('<p class="note"><strong>NOT EVALUABLE</strong> &mdash; no usable bar series.</p>')
    return o

PILL = {"JUSTIFIED": "g", "SUSPECT": "r", "BREACH": "r", "NO BREACH": "g"}

def pill(text):
    cls = PILL.get(text, "n" if ("UNEVAL" in text or "NOT EVAL" in text) else "a")
    return '<span class="pill %s">%s</span>' % (cls, esc(text))

def render_tail(root, day, ctx, o):
    day_rows, bots, breaches, verdicts = ctx["day_rows"], ctx["bots"], ctx["breaches"], ctx["verdicts"]

    # §3
    o.append("<h2>&sect;3 &middot; Who should have fired</h2>")
    if verdicts is None:
        o.append('<p class="warn"><strong>NOT EVALUABLE.</strong> '
                 '<span class="mono">data/brief/%s_p3_verdicts.tsv</span> is absent. '
                 'This is not a pass &mdash; stage 5 either did not run or did not write.</p>' % day)
    elif not verdicts:
        o.append('<p class="note">Stage 5 ran and judged no bot. Every ON bot traded, or none was evaluable.</p>')
    else:
        o.append("<table><tr><th>Bot</th><th>PR</th><th>Verdict</th><th>Basis</th></tr>")
        order = {"SUSPECT": 0, "JUSTIFIED": 2}
        for v in sorted(verdicts, key=lambda v: (order.get(v.get("verdict", ""), 1), v.get("bot", ""))):
            o.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                     % (esc(v.get("bot", "")), esc(v.get("pr_id", "")), pill(v.get("verdict", "?")), esc(v.get("reason", ""))))
        o.append("</table>")
        un = [v for v in verdicts if "UNEVAL" in (v.get("verdict") or "")]
        if un:
            o.append('<p class="note"><strong>%d of %d are NOT EVALUABLE, which is never a pass.</strong> '
                     'The detector cannot say whether those bots were right to stay silent, because what they '
                     'were waiting for is not written down.</p>' % (len(un), len(verdicts)))

    # §4
    o.append("<h2>&sect;4 &middot; Per-bot review</h2>")
    if ctx["config_blind"]:
        g = ctx["grades"] or {}
        o.append('<p class="warn"><strong>The instruction-mirror cards do not exist for this day.</strong> '
                 '<span class="mono">daily_brief.py</span> produced <span class="mono">cards: []</span> and '
                 '<span class="mono">grades: %s</span> &mdash; it ran CONFIG-BLIND, because '
                 '<span class="mono">data/bots_config_v2.csv</span> is not a mechanics table (finding F-6). '
                 '<strong>This is correct behaviour</strong>: grading against a record that does not exist is what '
                 'produced the false 100%% in v1. The ledger below is real and is <em>not</em> a substitute for the '
                 'cards.</p>' % esc(json.dumps(g, sort_keys=True)))
    if day_rows:
        o.append("<table><tr><th>Bot</th><th class=\"num\">Legs</th><th class=\"num\">Pos</th>"
                 "<th class=\"num\">P/L</th><th>Structures</th><th>Sides</th></tr>")
        for b in sorted(bots, key=lambda b: -(pl_of(bots[b])[0] or 0)):
            rows = bots[b]; p, miss = pl_of(rows)
            ss = sorted({r.get("single_sided") for r in rows})
            sides = "two-sided" if ss == ["False"] else ("single-sided" if ss == ["True"] else "mixed")
            o.append("<tr><td>%s</td><td class=\"num\">%d</td><td class=\"num\">%d</td>"
                     "<td class=\"num\">%s</td><td>%s</td><td>%s</td></tr>"
                     % (esc(b), len(rows), positions_of(rows),
                        (money(p) if p is not None else "NOT EVALUABLE") + ("" if not miss else " (%d legs no pnl)" % miss),
                        esc(", ".join(sorted({r.get("structure", "?") for r in rows}))), sides))
        o.append("</table>")
        two = [b for b in bots if sorted({r.get("single_sided") for r in bots[b]}) == ["False"]]
        o.append('<p class="note"><strong>Two-sided (condor) bots today: %d of %d.</strong> '
                 'Unit of account is the POSITION; a condor is its two spread rows sharing a '
                 '<span class="mono">trade_id</span>. Two single-sided spreads are two positions, not one condor.</p>'
                 % (len(two), len(bots)))
    else:
        o.append('<p class="note">No positions opened today.</p>')

    # §5
    o.append("<h2>&sect;5 &middot; Hedge clinic</h2>")
    if not breaches:
        o.append('<p class="note">No short strikes recorded on today\'s positions &mdash; nothing to check.</p>')
    else:
        nb = sum(1 for b in breaches if b["verdict"] == "BREACH")
        nu = sum(1 for b in breaches if b["verdict"] == "NOT EVALUABLE")
        o.append("<p><strong>%d breach(es)</strong> across %d short strikes checked%s.</p>"
                 % (nb, len(breaches), "" if not nu else ", <strong>%d NOT EVALUABLE</strong>" % nu))
        groups = {}
        for b in breaches:
            k = (b["side"], b["strike"], b["extreme"], b["verdict"], b["why"])
            groups.setdefault(k, []).append(b["bot"])
        o.append("<table><tr><th>Bots</th><th>Side</th><th class=\"num\">Strike</th>"
                 "<th class=\"num\">Post-entry extreme</th><th class=\"num\">Clearance</th><th>Result</th></tr>")
        def sort_key(item):
            (side, strike, ext, verdict, why), bots_ = item
            clear = None if ext is None else ((ext - strike) if side == "put" else (strike - ext))
            return (verdict != "BREACH", clear if clear is not None else 9e9)
        for (side, strike, ext, verdict, why), bots_ in sorted(groups.items(), key=sort_key):
            clear = None if ext is None else ((ext - strike) if side == "put" else (strike - ext))
            names = sorted(set(bots_))
            label = names[0] if len(names) == 1 else "%s <span class=\"note\">+%d more</span>" % (esc(names[0]), len(names) - 1)
            o.append("<tr><td>%s</td><td>%s</td><td class=\"num\">%g</td><td class=\"num\">%s</td>"
                     "<td class=\"num\">%s</td><td>%s %s</td></tr>"
                     % (label if len(names) == 1 and False else (esc(names[0]) if len(names) == 1 else label),
                        side, strike, ("%g" % ext) if ext is not None else "&mdash;",
                        ("%+.2f" % clear) if clear is not None else "&mdash;", pill(verdict), esc(why)))
        o.append("</table>")
    o.append(slot("convexity", "convexity watch",
                  "Would a cheap long-put or long-vol overlay have paid today? One line either way. "
                  "The empirical case for convexity is built by accumulation, including the days against it.", ctx["narr"]))

    # §6 + verdicts
    o.append("<h2>&sect;6 &middot; What today teaches</h2>")
    o.append(slot("lesson", "the day's single durable lesson",
                  "One pattern, drawn from full post-cutover history, not a restatement of today's P/L.", ctx["narr"]))
    o.append("<h2>Verdicts &mdash; separately, never blended</h2>")
    o.append("<table><tr><th>Axis</th><th>Answerable from</th><th>Status</th></tr>")
    o.append("<tr><td><strong>FIRE</strong></td><td>capture + regime + bot logs</td><td>%s</td></tr>"
             % slot_inline("FIRE", "fire", ctx["narr"]))
    o.append("<tr><td><strong>MECHANICS</strong></td><td>the position's <strong>Trades list</strong> &mdash; "
             "the Exit Options panel is never evidence</td><td>%s</td></tr>"
             % (pill("NOT EVALUABLE") + ' <span class="note">no Trades-list pull is recorded for this day</span>'))
    o.append("<tr><td><strong>STRATEGY</strong></td><td>counterfactual replay</td><td>%s</td></tr>"
             % slot_inline("STRATEGY", "strategy", ctx["narr"]))
    o.append("</table>")
    o.append('<p class="note">A RED on an evidenced axis emits an instruction card. '
             'A SUSPECT row whose bot has no declared gate is <strong>structural</strong> &mdash; it repeats every '
             'night until the gate is signed and carries no information about this day.</p>')
    o.append("<h2>Tomorrow's watch</h2>")
    o.append(slot("tomorrow", "tomorrow's watch", "The specific, falsifiable things to look for in the next brief. "
                                      "Section §0 of the next brief grades them.", ctx["narr"]))
    o.append("</div></body></html>")
    return o

VERDICT_TOKENS = ("GREEN", "AMBER", "RED", "NOT EVALUABLE", "UNSET")

def slot_inline(axis, key, narr):
    """A narrative verdict section may OPEN with a bare token (GREEN / AMBER / RED /
    NOT EVALUABLE) which becomes the pill. Raw HTML in the narrative is escaped by
    design, so the token is the only way to set a status - and it is machine-readable,
    which a hand-written span never was."""
    if narr.get(key):
        html = narr[key]
        for tok in VERDICT_TOKENS:
            m = re.match(r"^<p>%s\b[\s:.,\u2014-]*" % re.escape(tok), html)
            if m:
                return pill(tok) + " <p>" + html[m.end():]
        return html
    return ('<span class="pill a">UNSET</span> <span class="note">%s is a judgment call; the renderer '
            'will not assign it. Set it in <span class="mono">## %s</span>.</span>' % (axis, key))

def build(root, day):
    pack, pack_path = load_pack(root, day)
    verdicts, v_path = load_verdicts(root, day)
    trades, tr_path = load_trades(root)
    o, ctx = render(root, day, pack, pack_path, verdicts, v_path, trades, tr_path)
    o = render_body(root, day, ctx, o)
    o = render_tail(root, day, ctx, o)
    return "".join(o), ctx

def newest_day(root):
    ps = glob.glob(os.path.join(root, "data", "brief", "*_brief.json"))
    days = sorted(re.match(r"^(\d{4}-\d{2}-\d{2})_brief\.json$", os.path.basename(p)).group(1)
                  for p in ps if re.match(r"^\d{4}-\d{2}-\d{2}_brief\.json$", os.path.basename(p)))
    if not days:
        die("no data/brief/<DAY>_brief.json found under %s" % root)
    return days[-1]

def all_days(root):
    ps = glob.glob(os.path.join(root, "data", "brief", "*_brief.json"))
    return sorted(re.match(r"^(\d{4}-\d{2}-\d{2})_brief\.json$", os.path.basename(p)).group(1)
                  for p in ps if re.match(r"^\d{4}-\d{2}-\d{2}_brief\.json$", os.path.basename(p)))

def check(root):
    """Render every day with a pack and assert invariants. Writes nothing.

    The predicates are DERIVATIONS, never literals: a hard-coded '$4,706' here
    would pass on one day and be meaningless on every other.
    """
    import xml.etree.ElementTree as ET
    days = all_days(root)
    if not days: die("--check: no packs to render")
    bad = 0
    for d in days:
        try:
            html, ctx = build(root, d)
        except SystemExit:
            print("  %s  FATAL during build" % d); bad += 1; continue
        errs = []
        for s in re.findall(r"<svg.*?</svg>", html, re.S):
            try: ET.fromstring(s)
            except Exception as e: errs.append("malformed svg: %s" % e)
        # every bot that opened a position must appear in the body
        for b in ctx["bots"]:
            if esc(b) not in html: errs.append("bot missing from page: %s" % b)
        # the ledger figure on the page must equal the ledger recomputed here
        want = money(ctx["all_pl"])
        if want not in html: errs.append("ledger total %s absent from page" % want)
        # an absent verdict file must render as NOT EVALUABLE, never silently
        if ctx["verdicts"] is None and "NOT EVALUABLE" not in html:
            errs.append("missing p3 verdicts did not render as NOT EVALUABLE")
        # Every narrative region must render as EITHER a filled block OR a visible
        # unfilled slot. Asserting on the marker string alone fails the moment a day
        # is fully written up — the predicate must state the property, not a literal.
        regions = html.count('class="slot"') + html.count('class="narr"')
        if regions < 4:
            errs.append("narrative regions rendered: %d, expected >= 4 (filled or unfilled)" % regions)
        n_narr = len(ctx["narr"])
        if n_narr and ctx["narr_path"] and not os.path.exists(ctx["narr_path"]):
            errs.append("narrative parsed but path missing: %s" % ctx["narr_path"])
        print("  %s  %-7s %5d bytes  %d legs  %d bots  %s"
              % (d, "OK" if not errs else "FAIL", len(html), len(ctx["day_rows"]), len(ctx["bots"]),
                 "" if not errs else "; ".join(errs)))
        bad += 1 if errs else 0
    print("--check: %d day(s), %d failing" % (len(days), bad))
    return 1 if bad else 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("day", nargs="?")
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--out")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    if a.check:
        sys.exit(check(root))
    day = a.day or newest_day(root)
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", day):
        die("day must be YYYY-MM-DD, got %r" % day)
    html, ctx = build(root, day)
    out = a.out or os.path.join(root, "data", "brief", "%s_brief.html" % day)
    with open(out, "w") as f:
        f.write(html)
    unfilled = html.count("NARRATIVE SLOT")
    print("render_brief.py: wrote %s (%d bytes) — %d legs, %d bots, %s banked today, %d narrative slot(s) UNFILLED"
          % (os.path.relpath(out, root), len(html), len(ctx["day_rows"]), len(ctx["bots"]),
             re.sub(r"&[a-z]+;", "-", money(ctx["tot_pl"]) if ctx["tot_pl"] is not None else "NOT EVALUABLE"), unfilled))
    if ctx["config_blind"]:
        print("render_brief.py: WARNING — CONFIG-BLIND, §4 has no instruction-mirror cards (finding F-6)")

if __name__ == "__main__":
    main()
