#!/usr/bin/env python3
"""Intraday Cockpit dashboard V1 — sentinel-lite with an auto-refreshing HTML face.

Every run (launchd fires every 5 min during RTH):
  1. Pull today's 5-min bars (Tradier, via tape.py's plumbing + volume).
  2. Compute the cockpit feature set: session VWAP + sigma bands, sigma-extension,
     RSI(14), opening range, prior-day levels, regime read, confluence zones.
  3. Rewrite data/intraday/read.html — self-contained, inline data, 60s meta-refresh,
     gate banner — and data/intraday/read.json (for cockpit-Claude).
  4. Fire a macOS notification ONLY on a gate transition (osascript; deduped via
     data/intraday/.gate_state.json).

Gates: |sigma-ext| crosses 2 mid-session (10:00-14:30 ET) · price within 0.10% of a
confluence zone · regime label flip. Everything it emits about the fade carries the
UNVALIDATED HYPOTHESIS tag (see docs/intraday-cockpit.md) until the Lab backtest
returns a keep.

DUAL-USE RULE: the feature math here is the same math the Lab backtest imports.
No dashboard-only forks.

Usage:
  python3 scripts/intraday_read.py                 # QQQ, today (ET); exits quietly outside RTH
  python3 scripts/intraday_read.py SPX             # other symbol
  python3 scripts/intraday_read.py --date 2026-07-07   # backfill/test (skips RTH guard)
  python3 scripts/intraday_read.py --force         # run now even outside RTH
"""
import json, math, os, shutil, subprocess, sys, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tape import load_env, load_token, _get  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "intraday")

try:
    from zoneinfo import ZoneInfo
    ET = ZoneInfo("America/New_York")
except Exception:  # pragma: no cover
    ET = None

MID_SESSION = ("10:00", "14:30")   # fade-gate window (workstream spec)
CONFLUENCE_PCT = 0.0015            # levels within 0.15% = one zone
PROXIMITY_PCT = 0.0010             # price within 0.10% of a zone = gate


def now_et():
    return datetime.datetime.now(ET) if ET else datetime.datetime.now()


def fl(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------- data
def timesales(symbol, day, token, base):
    """5-min bars WITH volume (tape.py's variant drops volume; VWAP needs it)."""
    data = _get(base, "markets/timesales",
                {"symbol": symbol, "interval": "5min", "session_filter": "open",
                 "start": f"{day} 09:30", "end": f"{day} 16:00"}, token)
    s = (data or {}).get("series")
    if not s or s in ("null", None):
        return []
    bars = s.get("data")
    bars = bars if isinstance(bars, list) else [bars] if isinstance(bars, dict) else []
    out = []
    for b in bars:
        t = (b.get("time") or "")[11:16]
        c = fl(b.get("close"))
        if t and c is not None:
            out.append({"t": t, "o": fl(b.get("open")), "h": fl(b.get("high")),
                        "l": fl(b.get("low")), "c": c, "v": fl(b.get("volume")) or 0.0})
    return out


def prior_session(symbol, day, token, base):
    """Full OHLC of the LAST session strictly before `day` (weekend/holiday-proof)."""
    start = (datetime.date.fromisoformat(day) - datetime.timedelta(days=10)).isoformat()
    data = _get(base, "markets/history",
                {"symbol": symbol, "interval": "daily", "start": start, "end": day}, token)
    h = (data or {}).get("history")
    if not h or h in ("null", None):
        return {}
    days = h.get("day")
    days = days if isinstance(days, list) else [days] if isinstance(days, dict) else []
    days = sorted((d for d in days if isinstance(d, dict) and (d.get("date") or "") < day),
                  key=lambda d: d["date"])
    if not days:
        return {}
    p = days[-1]
    return {k: fl(p.get(k)) for k in ("open", "high", "low", "close")}


# ---------------------------------------------------------------- features
def vwap_bands(bars):
    """Per-bar session VWAP + volume-weighted sigma. Index symbols (no volume)
    fall back to equal weights. Returns list of {vwap, sigma} aligned to bars."""
    cum_v = cum_pv = cum_pv2 = 0.0
    out = []
    for b in bars:
        tp = (b["h"] + b["l"] + b["c"]) / 3 if b["h"] and b["l"] else b["c"]
        w = b["v"] if b["v"] > 0 else 1.0
        cum_v += w
        cum_pv += w * tp
        cum_pv2 += w * tp * tp
        vwap = cum_pv / cum_v
        var = max(cum_pv2 / cum_v - vwap * vwap, 0.0)
        out.append({"vwap": vwap, "sigma": math.sqrt(var)})
    return out


def rsi(closes, n=14):
    if len(closes) < n + 1:
        return None
    gains = losses = 0.0
    for i in range(1, n + 1):
        d = closes[i] - closes[i - 1]
        gains += max(d, 0); losses += max(-d, 0)
    ag, al = gains / n, losses / n
    for i in range(n + 1, len(closes)):
        d = closes[i] - closes[i - 1]
        ag = (ag * (n - 1) + max(d, 0)) / n
        al = (al * (n - 1) + max(-d, 0)) / n
    if al == 0:
        return 100.0
    return round(100 - 100 / (1 + ag / al), 1)


def rsi_series(closes, n=14):
    """Full per-bar RSI(14) with Wilder smoothing. Returns a list aligned to
    `closes`; None for the first n bars where RSI is undefined. Plain importable
    function, no side effects (dual-use: the Lab backtest imports this)."""
    out = [None] * len(closes)
    if len(closes) < n + 1:
        return out
    gains = losses = 0.0
    for i in range(1, n + 1):
        d = closes[i] - closes[i - 1]
        gains += max(d, 0.0); losses += max(-d, 0.0)
    ag, al = gains / n, losses / n
    out[n] = 100.0 if al == 0 else round(100 - 100 / (1 + ag / al), 1)
    for i in range(n + 1, len(closes)):
        d = closes[i] - closes[i - 1]
        ag = (ag * (n - 1) + max(d, 0.0)) / n
        al = (al * (n - 1) + max(-d, 0.0)) / n
        out[i] = 100.0 if al == 0 else round(100 - 100 / (1 + ag / al), 1)
    return out


def _ema_series(vals, span):
    """EMA seeded with an SMA over the first `span` values; None before it is
    defined. Plain helper, no side effects."""
    out = [None] * len(vals)
    if len(vals) < span:
        return out
    prev = sum(vals[:span]) / span
    out[span - 1] = prev
    k = 2.0 / (span + 1)
    for i in range(span, len(vals)):
        prev = vals[i] * k + prev * (1 - k)
        out[i] = prev
    return out


def macd(closes, fast=12, slow=26, signal=9):
    """MACD(12,26,9). Returns {'macd','signal','hist'} lists aligned to `closes`,
    with None where undefined (first ~slow-1 bars for the line; +signal-1 more for
    the signal). Plain importable function, no side effects at import — dual-use
    with the Lab backtest, no dashboard-only fork."""
    ef, es = _ema_series(closes, fast), _ema_series(closes, slow)
    line = [(ef[i] - es[i]) if (ef[i] is not None and es[i] is not None) else None
            for i in range(len(closes))]
    defined = [(i, m) for i, m in enumerate(line) if m is not None]
    sig = [None] * len(closes)
    if len(defined) >= signal:
        idxs = [i for i, _ in defined]
        es9 = _ema_series([m for _, m in defined], signal)
        for j, v in enumerate(es9):
            if v is not None:
                sig[idxs[j]] = v
    hist = [(line[i] - sig[i]) if (line[i] is not None and sig[i] is not None) else None
            for i in range(len(closes))]
    return {"macd": line, "signal": sig, "hist": hist}


def path_directionality(closes):
    if len(closes) < 2:
        return None
    path = sum(abs(closes[i] - closes[i - 1]) for i in range(1, len(closes)))
    return round(abs(closes[-1] - closes[0]) / path, 2) if path > 0 else None


def regime_label(bars, prior_close, bands):
    closes = [b["c"] for b in bars]
    hi, lo = max(b["h"] or b["c"] for b in bars), min(b["l"] or b["c"] for b in bars)
    rng = (hi - lo) / prior_close * 100 if prior_close else None
    d = path_directionality(closes)
    # VWAP slope over the last hour (12 bars)
    v = [x["vwap"] for x in bands]
    slope = (v[-1] - v[-min(12, len(v))]) / v[-1] * 100 if len(v) >= 2 else 0.0
    rng = round(rng, 2) if rng is not None else None
    if rng is None:
        return "n/a", d, rng, slope
    if rng < 0.75 and (d is None or d < 0.5):
        return "Chop", d, rng, slope
    if rng > 1.5 or (d is not None and d >= 0.6):
        return "Trend", d, rng, slope
    return "Drift", d, rng, slope


def build_levels(bars, prior, or_hi, or_lo, vwap, sigma):
    lv = []
    if prior:
        for k, name in (("high", "PDH"), ("low", "PDL"), ("close", "PDC")):
            if prior.get(k):
                lv.append({"px": prior[k], "name": name})
    if or_hi:
        lv.append({"px": or_hi, "name": "ORH"})
    if or_lo:
        lv.append({"px": or_lo, "name": "ORL"})
    lv.append({"px": vwap, "name": "VWAP"})
    for m, name in ((1, "+1σ"), (-1, "-1σ"), (2, "+2σ"), (-2, "-2σ")):
        lv.append({"px": vwap + m * sigma, "name": name})
    lv = [l for l in lv if l["px"]]
    # confluence: greedy cluster within CONFLUENCE_PCT
    lv.sort(key=lambda l: l["px"])
    zones, cur = [], [lv[0]]
    for l in lv[1:]:
        if (l["px"] - cur[-1]["px"]) / cur[-1]["px"] <= CONFLUENCE_PCT:
            cur.append(l)
        else:
            zones.append(cur); cur = [l]
    zones.append(cur)
    out = []
    for z in zones:
        out.append({"px": round(sum(l["px"] for l in z) / len(z), 2),
                    "names": [l["name"] for l in z], "confluence": len(z) >= 2})
    return out


def tod_bucket(t):
    if t < "10:00": return "opening drive"
    if t < "11:30": return "morning session"
    if t < "14:00": return "midday"
    if t < "15:00": return "early afternoon"
    return "power hour"


# ---------------------------------------------------------------- gates
def eval_gates(read, prev_regime):
    g = []
    t = read["last_bar"]
    if abs(read["sigma_ext"]) >= 2 and MID_SESSION[0] <= t <= MID_SESSION[1]:
        g.append(f"FADE {read['sigma_ext']:+.1f}σ mid-session [UNVALIDATED HYPOTHESIS]")
    px = read["price"]
    for z in read["zones"]:
        if z["confluence"] and abs(px - z["px"]) / px <= PROXIMITY_PCT:
            g.append(f"CONFLUENCE {z['px']} ({' · '.join(z['names'])})")
    if prev_regime and read["regime"] != prev_regime and read["regime"] != "n/a":
        g.append(f"REGIME FLIP {prev_regime}→{read['regime']}")
    return g


def notify(title, msg):
    osa = shutil.which("osascript")
    if not osa:
        return
    subprocess.run([osa, "-e",
                    f'display notification "{msg}" with title "{title}"'],
                   capture_output=True)


# ---------------------------------------------------------------- behavioral + sidecars
# Contract caps (display/notify plumbing only — NOT signal definitions).
BEHAV_CAPS = {"day_premium": 450, "trades": 4, "contracts": 15,
              "giveback_pct": 40, "day_loss": 250}
# Gate taxonomy for R7 severity tiers + G7 flashcard.
BEHAVIORAL_TYPES = {"ROLLUP", "EXT_TOP", "SIZE", "COOLDOWN", "GIVEBACK"}
AMBER_MARKET_TYPES = {"CONFLUENCE", "REGIME"}


def load_json(path):
    """Failure-tolerant JSON load. Missing/corrupt → None."""
    try:
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
    except Exception:
        return None
    return None


def behavioral_gates(ss):
    """Derive behavioral-gate trips from session_state.json (F4 schema) against the
    contract caps, plus any explicit `gates` array cockpit-Claude wrote. Display /
    notify plumbing only — no market-signal definition here. Returns a list of
    {type,label,t,px}. Empty on missing/blank state (failure-tolerant)."""
    if not isinstance(ss, dict):
        return []
    out = []
    peak, real = fl(ss.get("peak_realized")), fl(ss.get("realized_pnl"))
    if peak and peak > 0 and real is not None:
        pct = (peak - real) / peak * 100
        if pct > BEHAV_CAPS["giveback_pct"]:
            out.append({"type": "GIVEBACK", "px": None, "t": ss.get("last_fill_t") or "",
                        "label": f"give-back {pct:.0f}% of peak (cap {BEHAV_CAPS['giveback_pct']}%)"})
    prem = fl(ss.get("premium_deployed"))
    if prem is not None and prem > BEHAV_CAPS["day_premium"]:
        out.append({"type": "SIZE", "px": None, "t": ss.get("last_fill_t") or "",
                    "label": f"premium ${prem:.0f} > ${BEHAV_CAPS['day_premium']} cap"})
    trades = fl(ss.get("trades_today"))
    if trades is not None and trades > BEHAV_CAPS["trades"]:
        out.append({"type": "SIZE", "px": None, "t": ss.get("last_fill_t") or "",
                    "label": f"{int(trades)} trades > {BEHAV_CAPS['trades']} cap"})
    for g in (ss.get("gates") or []):
        if isinstance(g, dict) and g.get("type"):
            out.append({"type": g["type"], "px": g.get("px"),
                        "t": g.get("t", ""), "label": g.get("label", g["type"])})
        elif isinstance(g, str) and g.strip():
            out.append({"type": g.split()[0], "px": None, "t": "", "label": g})
    return out


def gate_to_entry(gstr, t, price):
    """Turn a market-gate string into a gate_log entry {t,type,px,label}."""
    typ = gstr.split(" ")[0]
    px = price
    if typ == "CONFLUENCE":
        try:
            px = float(gstr.split(" ")[1])
        except Exception:
            px = price
    return {"t": t, "type": typ,
            "px": round(px, 2) if px is not None else None, "label": gstr}


def append_gate_log(path, day, transitions):
    """Append one JSON line per NEW market-gate transition this run. Resets daily:
    if the file's first line is from another date, truncate first. Behavioral gates
    are written by cockpit-Claude, NOT here (spec C2). Display plumbing only — this
    file must not feed the Lab evidence lane."""
    reset = False
    if os.path.exists(path):
        try:
            with open(path) as f:
                first = f.readline().strip()
            if first:
                if json.loads(first).get("date") != day:
                    reset = True
        except Exception:
            reset = True
    if reset:
        open(path, "w").close()
    if not transitions:
        return
    with open(path, "a") as f:
        for tr in transitions:
            f.write(json.dumps({"date": day, **tr}) + "\n")


def read_gate_log(path, day):
    """Read today's gate-log lines for rendering. Failure-tolerant → []."""
    out = []
    try:
        if os.path.exists(path):
            with open(path) as f:
                for ln in f:
                    ln = ln.strip()
                    if not ln:
                        continue
                    try:
                        e = json.loads(ln)
                    except Exception:
                        continue
                    if e.get("date") == day:
                        out.append(e)
    except Exception:
        return []
    return out


def read_scalp_days(path):
    """Read the append-only history CSV. Missing/corrupt → []."""
    import csv
    if not os.path.exists(path):
        return []
    try:
        with open(path, newline="") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


def build_greed(day, ss):
    """Assemble the greed-panel data from scalp_days.csv (history) + session_state
    (today, if present). Both local + failure-tolerant → 'no history yet'."""
    rows = read_scalp_days(os.path.join(ROOT, "data", "scalp_days.csv"))
    out = {"has_history": bool(rows), "labels": [], "cum_disc": [], "cum_final": [],
           "tax": 0.0, "rollups": 0, "red_days": 0, "today": None}
    cd = cf = 0.0
    for row in rows:
        cd += fl(row.get("disciplined_pnl")) or 0.0
        cf += fl(row.get("final_pnl")) or 0.0
        out["labels"].append(row.get("date", ""))
        out["cum_disc"].append(round(cd, 2))
        out["cum_final"].append(round(cf, 2))
        out["rollups"] += int(fl(row.get("rollup_events")) or 0)
        if (row.get("grade") or "").strip().upper() == "RED":
            out["red_days"] += 1
    out["tax"] = round(cd - cf, 2)
    # today: session_state first, else today's history row, else None (hide)
    today = None
    if isinstance(ss, dict) and ss.get("date") == day and ss.get("peak_realized") is not None:
        peak, fin = fl(ss.get("peak_realized")), fl(ss.get("realized_pnl"))
        if peak is not None and fin is not None:
            gb = peak - fin
            pct = (gb / peak * 100) if peak > 0 else 0.0
            today = {"peak": peak, "final": fin, "giveback": round(gb, 2),
                     "giveback_pct": round(pct, 1), "over_cap": pct > BEHAV_CAPS["giveback_pct"]}
    if today is None:
        for row in rows:
            if row.get("date") == day:
                peak, fin = fl(row.get("peak_realized")), fl(row.get("final_pnl"))
                gb, pct = fl(row.get("giveback")), fl(row.get("giveback_pct"))
                if peak is not None:
                    today = {"peak": peak, "final": fin,
                             "giveback": gb if gb is not None else (peak - (fin or 0)),
                             "giveback_pct": pct if pct is not None else 0.0,
                             "over_cap": (pct or 0) > BEHAV_CAPS["giveback_pct"]}
                break
    out["today"] = today
    return out


# ---------------------------------------------------------------- V3 discipline panels
GOAL_DEFAULT = {"start_bankroll": 800, "target": 10000,
                "start_date": "2026-07-09", "rungs": 13}


def read_goal_config():
    """data/goal_config.json, failure-tolerant → defaults."""
    g = load_json(os.path.join(ROOT, "data", "goal_config.json"))
    out = dict(GOAL_DEFAULT)
    if isinstance(g, dict):
        for k in GOAL_DEFAULT:
            if g.get(k) is not None:
                out[k] = g[k]
    return out


def read_lessons():
    """data/intraday/lessons.json (list of one-liners). Missing/corrupt → []."""
    x = load_json(os.path.join(OUT, "lessons.json"))
    if isinstance(x, list):
        return [str(e) if not isinstance(e, dict) else e.get("text", "") for e in x]
    return []


def build_ladder(goal, rows):
    """G1: deterministic rung replay of scalp_days from start_date. GREEN & final>0
    = +1 rung, RED = −1 (floor 0), AMBER = hold. Process-denominated only — NO
    dollar-countdown, NO required-return, NO date pressure (that is roll-up fuel)."""
    start = fl(goal["start_bankroll"]) or 800.0
    target = fl(goal["target"]) or 10000.0
    R = int(goal["rungs"]) if goal.get("rungs") else 13
    ratio = (target / start) ** (1.0 / R) if start > 0 and R > 0 else 1.0
    targets = [round(start * ratio ** k) for k in range(R + 1)]
    sd = goal.get("start_date", "")
    rung = days_on = 0
    for row in rows:
        if (row.get("date") or "") < sd:
            continue
        grade = (row.get("grade") or "").strip().upper()
        fin = fl(row.get("final_pnl")) or 0.0
        if grade == "GREEN" and fin > 0:
            nr = min(rung + 1, R)
        elif grade == "RED":
            nr = max(rung - 1, 0)
        else:
            nr = rung
        days_on = days_on + 1 if nr == rung else 0
        rung = nr
    return {"targets": targets, "rung": rung, "rungs": R, "days_on": days_on}


def build_streak(rows):
    """G4: consecutive disciplined-GREEN-day streak (current + best)."""
    cur = best = 0
    for row in rows:
        grade = (row.get("grade") or "").strip().upper()
        fin = fl(row.get("final_pnl")) or 0.0
        if grade == "GREEN" and fin > 0:
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return {"current": cur, "best": best}


def build_caps(ss):
    """G2: four cap bars from session_state.json. Missing → None (empty state)."""
    if not isinstance(ss, dict):
        return None
    ratchet = bool(ss.get("green_hour_ratchet"))
    prem_cap = BEHAV_CAPS["day_premium"] // 2 if ratchet else BEHAV_CAPS["day_premium"]
    prem = fl(ss.get("premium_deployed")) or 0.0
    trades = fl(ss.get("trades_today")) or 0.0
    oc = fl(ss.get("open_contracts")) or 0.0
    real = fl(ss.get("realized_pnl")) or 0.0
    day_loss = abs(min(real, 0.0))

    def bar(val, cap, label, unit):
        pct = (val / cap * 100) if cap else 0.0
        tier = "red" if pct >= 100 else ("amber" if pct >= 70 else "ok")
        return {"val": val, "cap": cap, "pct": round(min(pct, 100), 0),
                "raw_pct": round(pct, 0), "label": label, "unit": unit, "tier": tier}
    return {"ratchet": ratchet,
            "bars": [bar(prem, prem_cap, "premium", "$"),
                     bar(trades, BEHAV_CAPS["trades"], "trades", ""),
                     bar(oc, BEHAV_CAPS["contracts"], "open contracts", ""),
                     bar(day_loss, BEHAV_CAPS["day_loss"], "day loss", "$")]}


def market_closed(last_bar, now):
    """B5: closed if the last bar is the 16:00 close or now-ET is outside RTH."""
    if last_bar >= "16:00":
        return True
    hm = now.strftime("%H:%M")
    return now.weekday() >= 5 or not ("09:30" <= hm <= "16:00")


def banner_severity(gates_list, behavioral_active):
    """R7: red/hot = FADE or any behavioral gate; amber = CONFLUENCE/REGIME only."""
    if any(g.split(" ")[0] == "FADE" for g in gates_list) or behavioral_active:
        return "hot"
    return "amber" if gates_list else "ok"


def get_plan(ss):
    """G5: plan{bias,setup,no_trade} from session_state; {} if absent/blank."""
    if not isinstance(ss, dict):
        return {}
    p = ss.get("plan") or {}
    if not isinstance(p, dict):
        return {}
    return {"bias": (p.get("bias") or "").strip(),
            "setup": (p.get("setup") or "").strip(),
            "no_trade": (p.get("no_trade") or "").strip()}


# ---------------------------------------------------------------- render
def render_html(read, bars, bands, rsi_ser, macd_d, gate_log, greed, ctx):
    ladder, caps, streak = ctx["ladder"], ctx["caps"], ctx["streak"]
    plan, flash = ctx["plan"], ctx["flash"]
    closed, after_230 = ctx["closed"], ctx["after_230"]
    last_win = ctx["last_win"]
    data = {"bars": [{"t": b["t"], "c": b["c"]} for b in bars],
            "vwap": [round(x["vwap"], 3) for x in bands],
            "sigma": [round(x["sigma"], 3) for x in bands],
            "rsi": rsi_ser,
            "macd": [None if v is None else round(v, 4) for v in macd_d["macd"]],
            "sig": [None if v is None else round(v, 4) for v in macd_d["signal"]],
            "hist": [None if v is None else round(v, 4) for v in macd_d["hist"]],
            "gates": gate_log,
            "greed": {"cum_disc": greed["cum_disc"], "cum_final": greed["cum_final"],
                      "l0": greed["labels"][0] if greed["labels"] else "",
                      "l1": greed["labels"][-1] if greed["labels"] else ""},
            "cooldown": last_win, "read": read}

    # ---- banner (B5 closed / R7 severity tiers) + G7 flashcard
    if closed:
        b_cls = "closed"
        b_inner = "CLOSED — last gate: " + (" · ".join(read["gates"]) if read["gates"] else "none")
    else:
        b_cls = ctx["banner_class"]
        b_inner = ("⚠ " + " · ".join(read["gates"])) if read["gates"] else "no gate"
    flash_html = (f"<div class='flash'><div class='flash-h'>LAST LESSON — behavioral gate fired "
                  f"today</div>{flash}</div>" if flash else "")
    banner_row = (f"<div class='banner-row'><div class='banner {b_cls}'>{b_inner}</div>"
                  f"{flash_html}</div>")

    # ---- G5 plan strip / no-plan banner
    if plan.get("bias") or plan.get("setup") or plan.get("no_trade"):
        plan_html = (f"<div class='plan'><b>PLAN</b> · bias: {plan.get('bias') or '—'} · "
                     f"setup: {plan.get('setup') or '—'} · no-trade: {plan.get('no_trade') or '—'}</div>")
    elif ctx["plan_banner"]:
        plan_html = ("<div class='banner amber'>No plan filled — contract says read it before "
                     "the first trade.</div>")
    else:
        plan_html = ""

    # ---- greed panel: B4 give-back number line, R8 compact (<5 rows)
    def giveback_bar(t):
        peak = t["peak"] or 0.0
        fin = t["final"] if t["final"] is not None else 0.0
        lo = min(fin, 0.0)
        span = (peak - lo) or 1.0
        pc = lambda v: max(0.0, min(100.0, (v - lo) / span * 100))
        z, f, pk = pc(0.0), pc(fin), pc(peak)
        over = " over" if t["over_cap"] else ""
        green = (f"<div class='gb-seg green' style='left:{min(z, f):.1f}%;width:{abs(f - z):.1f}%'></div>"
                 if fin > 0 else "")
        red = f"<div class='gb-seg red' style='left:{f:.1f}%;width:{max(0.0, pk - f):.1f}%'></div>"
        fin_txt = f"{'-' if fin < 0 else ''}${abs(fin):.0f}"
        return (f"<div class='gbn'>"
                f"<div class='gbn-track'>{red}{green}"
                f"<div class='gbn-zero' style='left:{z:.1f}%'></div>"
                f"<div class='gbn-mark' style='left:{f:.1f}%'></div></div>"
                f"<div class='gbn-lab'><span class='gbn-zl' style='left:{z:.1f}%'>$0</span>"
                f"<span class='l'>final {fin_txt}</span><span class='r'>peak +${peak:.0f}</span></div>"
                f"<div class='gb-sub{over}'>give-back ${t['giveback']:.0f} "
                f"({t['giveback_pct']:.0f}% of peak · cap {BEHAV_CAPS['giveback_pct']}%)</div></div>")

    reds = greed["red_days"]
    tax_frag = (f"<div class='gcol-tax'><div class='gtax'>${greed['tax']:,.0f}</div>"
                f"<div class='gcap'>given back to the chase since 2026-07-08</div>"
                f"<div class='gcap2'>{greed['rollups']} roll-up events · {reds} RED day"
                f"{'s' if reds != 1 else ''}</div></div>")
    n_rows = len(greed["labels"])
    gb_frag = giveback_bar(greed["today"]) if greed["today"] else \
        ("<div class='gb-sub'>today: no intraday state — showing history</div>"
         if greed["has_history"] else "<div class='gb-sub'>no history yet</div>")
    if not greed["has_history"] and greed["today"] is None:
        greed_html = ("<div class='greed'><div class='gtitle'>GREED PANEL — behavioral leakage</div>"
                      "<div class='gcap'>no history yet</div></div>")
    elif n_rows < 5:  # R8 compact
        greed_html = (f"<div class='greed compact'><div class='gtitle'>GREED PANEL — behavioral "
                      f"leakage (compact until 5 logged days)</div><div class='grow'>"
                      f"<div class='gcol-bar'>{gb_frag}</div>{tax_frag}</div></div>")
    else:  # full three-component
        greed_html = (f"<div class='greed'><div class='gtitle'>GREED PANEL — behavioral leakage "
                      f"(not a trade signal)</div><div class='grow'>"
                      f"<div class='gcol-bar'>{gb_frag}</div>"
                      f"<div class='gcol-eq'><canvas id='eq' width='460' height='120'></canvas>"
                      f"<div class='gcap'>Σ disciplined (green) vs Σ actual (white/red) · $ not R</div></div>"
                      f"{tax_frag}</div></div>")

    # ---- G1 Ladder (process-denominated; NO countdown / $-to-go / date pressure)
    R = ladder["rungs"]
    cur = ladder["rung"]
    tg = ladder["targets"]
    ticks = "".join(
        f"<div class='rung{' cur' if k == cur else ''}{' done' if k < cur else ''}' "
        f"title='rung {k}: ${tg[k]:,}'><i>{k}</i></div>" for k in range(R + 1))
    ladder_html = (f"<div class='ladder'><div class='gtitle'>THE LADDER — ${tg[0]:,}→${tg[R]:,} "
                   f"in {R} rungs (process, not a countdown)</div>"
                   f"<div class='ladder-track'>{ticks}</div>"
                   f"<div class='ladder-meta'>on rung <b>{cur}</b> (${tg[cur]:,}) · "
                   f"next rung ${tg[min(cur + 1, R)]:,} · days on this rung: {ladder['days_on']}</div>"
                   f"<div class='ladder-teeth'>a disciplined GREEN day = +1 rung · "
                   f"a RED day costs a rung (one green day to reclaim)</div></div>")

    # ---- G2 caps meter
    if not caps:
        caps_html = ("<div class='caps'><div class='gtitle'>LIVE CAPS</div>"
                     "<div class='gcap'>no fills reported yet</div></div>")
    else:
        cbars = []
        for b in caps["bars"]:
            cs = f"${b['cap']:.0f}" if b["unit"] == "$" else f"{b['cap']:.0f}"
            vs = f"${b['val']:.0f}" if b["unit"] == "$" else f"{b['val']:.0f}"
            rl = (" · ratchet: cap $%d" % b["cap"]) if (b["label"] == "premium" and caps["ratchet"]) else ""
            cbars.append(f"<div class='capbar'><div class='capbar-l'>{b['label']} {vs}/{cs}{rl}</div>"
                         f"<div class='capbar-t'><div class='capbar-f {b['tier']}' "
                         f"style='width:{b['pct']:.0f}%'></div></div></div>")
        caps_html = "<div class='caps'><div class='gtitle'>LIVE CAPS (session)</div>" + "".join(cbars) + "</div>"

    # ---- G3 cooldown (client-side clock) + G4 streak
    cooldown_html = ("<div class='cooldown' id='cooldown' style='display:none'>"
                     "<div class='gtitle'>POST-WIN COOLDOWN</div>"
                     "<div class='cd-clock' id='cdclock'>--:--</div>"
                     "<div class='gcap'>post-win cooldown — the chase is a reflex</div></div>"
                     if last_win else "")
    streak_html = (f"<div class='streak'><div class='gtitle'>DISCIPLINE STREAK</div>"
                   f"<div class='streak-n'>{streak['current']}</div>"
                   f"<div class='gcap'>current green-day streak · best {streak['best']}</div></div>")

    # ---- R1 fired-only legend
    fired = {e.get("type") for e in gate_log}
    def leg(sym, typ, label):
        return f"<span class='{'' if typ in fired else 'dim'}'>{sym} <b>{label}</b></span>"
    legend_html = ("<div class='legend'>"
                   + leg("⛔", "ROLLUP", "ROLLUP") + leg("▲", "EXT_TOP", "EXT_TOP")
                   + leg("↓", "GIVEBACK", "GIVEBACK")
                   + leg("◆", "FADE", "FADE (UNVALIDATED HYPOTHESIS)")
                   + leg("⟳", "REGIME", "REGIME") + leg("▪", "CONFLUENCE", "CONFLUENCE")
                   + "<span class='dim'>┊ <b>0DTE theta cliff (14:30 ET)</b></span></div>")

    # ---- R2 levels table (dist/▲▼ + price divider) + R3 glossary
    px = read["price"]
    zlist = sorted(read["zones"], key=lambda z: -z["px"])
    lrows, inserted = [], False
    for z in zlist:
        if not inserted and z["px"] < px:
            lrows.append(f"<tr class='pxrow'><td>← price</td><td>{px}</td><td></td><td></td></tr>")
            inserted = True
        dpts = z["px"] - px
        dpct = (dpts / px * 100) if px else 0.0
        arrow = "▲" if dpts > 0 else ("▼" if dpts < 0 else "•")
        dist = f"{arrow} {dpts:+.2f} ({dpct:+.2f}%)"
        lrows.append(f"<tr class='{'conf' if z['confluence'] else ''}'>"
                     f"<td>{z['px']}</td><td>{' · '.join(z['names'])}</td>"
                     f"<td>{dist}</td><td>{'ZONE' if z['confluence'] else ''}</td></tr>")
    if not inserted:
        lrows.append(f"<tr class='pxrow'><td>← price</td><td>{px}</td><td></td><td></td></tr>")
    zrows = "".join(lrows)
    delay = " · ⏱ 15m-delayed (sandbox)" if read["delayed"] else ""
    body_cls = "after230" if (after_230 and not closed) else ""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<meta http-equiv="refresh" content="60"><title>{read['symbol']} cockpit</title>
<style>
body{{background:#0d1117;color:#e6edf3;font:14px -apple-system,Helvetica,sans-serif;margin:0;padding:16px}}
body.after230{{filter:brightness(.85);border:2px solid #8b1a1a;padding-bottom:44px}}
body.cooldown-on{{border:2px solid #b8860b}}
.banner-row{{display:flex;gap:10px;align-items:stretch;margin-bottom:10px}}
.banner{{padding:8px 14px;border-radius:8px;font-weight:700;flex:1}}
.hot{{background:#5c1a1a;color:#ffb4b4}} .ok{{background:#12351f;color:#7ee2a8}}
.amber{{background:#4a3a12;color:#ffd479}} .closed{{background:#21262d;color:#8b949e}}
.flash{{background:#161b22;border:1px solid #8b6d1a;border-radius:8px;padding:6px 12px;max-width:360px;font-size:12px}}
.flash-h{{color:#c9a227;font-size:10px;text-transform:uppercase;letter-spacing:.5px;margin-bottom:2px}}
.plan{{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:6px 12px;margin-bottom:10px;font-size:12px;color:#adbac7}}
.row2{{display:flex;gap:10px;margin-bottom:10px;flex-wrap:wrap}}
.row3{{display:flex;gap:10px;margin-bottom:10px;flex-wrap:wrap}}
.greed{{background:#161b22;border-radius:8px;padding:10px 14px;border:1px solid #30363d;flex:1;min-width:420px}}
.gtitle{{color:#8b949e;font-size:11px;letter-spacing:.5px;margin-bottom:8px;text-transform:uppercase}}
.grow{{display:flex;gap:18px;align-items:center;flex-wrap:wrap}}
.gcol-bar{{flex:1;min-width:240px}}
.gbn-track{{position:relative;height:16px;background:#0d1117;border-radius:8px;margin:14px 0 2px;border:1px solid #30363d}}
.gb-seg{{position:absolute;top:0;height:100%}} .gb-seg.green{{background:#2ea043}} .gb-seg.red{{background:#8b1a1a}}
.gbn-zero{{position:absolute;top:-3px;height:22px;width:2px;background:#e6edf3}}
.gbn-mark{{position:absolute;top:-4px;height:24px;width:3px;background:#ffd479;transform:translateX(-1px)}}
.gbn-lab{{position:relative;font-size:11px;color:#8b949e;height:14px}}
.gbn-lab .l{{color:#ff6b6b;font-weight:700}} .gbn-lab .r{{position:absolute;right:0;color:#7ee2a8;font-weight:700}}
.gbn-zl{{position:absolute;transform:translateX(-50%);color:#e6edf3}}
.gb-sub{{font-size:12px;color:#8b949e;margin-top:4px}} .gb-sub.over{{color:#ff6b6b;font-weight:700}}
.gcol-eq{{width:460px}} .gcap{{color:#8b949e;font-size:11px;margin-top:3px}}
.gcol-tax{{text-align:center;min-width:150px}}
.gtax{{font:700 30px ui-monospace,Menlo,monospace;color:#ff4d4d}}
.gcap2{{color:#8b949e;font-size:11px;margin-top:2px}}
.ladder{{background:#161b22;border-radius:8px;padding:10px 14px;border:1px solid #30363d;flex:1;min-width:360px}}
.ladder-track{{display:flex;gap:3px;margin:6px 0}}
.rung{{flex:1;height:22px;background:#0d1117;border:1px solid #30363d;border-radius:3px;display:flex;align-items:center;justify-content:center}}
.rung i{{font-style:normal;font-size:10px;color:#586069}}
.rung.done{{background:#12351f;border-color:#2ea043}} .rung.done i{{color:#7ee2a8}}
.rung.cur{{background:#1f3a52;border-color:#58a6ff;box-shadow:0 0 0 1px #58a6ff}} .rung.cur i{{color:#79c0ff;font-weight:700}}
.ladder-meta{{font-size:12px;color:#adbac7;margin-top:4px}}
.ladder-teeth{{font-size:11px;color:#8b949e;margin-top:2px}}
.caps{{background:#161b22;border-radius:8px;padding:10px 14px;border:1px solid #30363d;flex:2;min-width:320px}}
.capbar{{margin-bottom:5px}} .capbar-l{{font-size:11px;color:#adbac7;margin-bottom:2px}}
.capbar-t{{height:8px;background:#0d1117;border-radius:4px;overflow:hidden;border:1px solid #30363d}}
.capbar-f{{height:100%}} .capbar-f.ok{{background:#2ea043}} .capbar-f.amber{{background:#d29922}} .capbar-f.red{{background:#da3633}}
.cooldown{{background:#161b22;border-radius:8px;padding:10px 14px;border:1px solid #b8860b;flex:1;min-width:160px;text-align:center}}
.cd-clock{{font:700 26px ui-monospace,Menlo,monospace;color:#ffd479}}
.streak{{background:#161b22;border-radius:8px;padding:10px 14px;border:1px solid #30363d;flex:1;min-width:140px;text-align:center}}
.streak-n{{font:700 26px ui-monospace,Menlo,monospace;color:#7ee2a8}}
.stats{{display:flex;gap:22px;flex-wrap:wrap;margin-bottom:8px}}
.stats div{{background:#161b22;padding:8px 14px;border-radius:8px}}
.stats b{{font-size:20px;display:block}}
small{{color:#8b949e}} table{{border-collapse:collapse;margin-top:10px}}
th{{text-align:left;color:#8b949e;font-size:11px;padding:3px 12px;border-bottom:1px solid #30363d}}
td{{padding:3px 12px;border-bottom:1px solid #21262d}} .conf td{{color:#ffd479;font-weight:700}}
.pxrow td{{color:#58a6ff;font-weight:700;border-top:1px solid #30363d;border-bottom:1px solid #30363d}}
.tcap{{color:#8b949e;font-size:11px;padding:2px 12px}}
canvas{{background:#161b22;border-radius:8px;margin-top:8px}}
.legend{{display:flex;gap:14px;flex-wrap:wrap;margin-top:8px;color:#adbac7;font-size:11px}}
.legend b{{color:#e6edf3}} .legend .dim{{opacity:.4}}
.foot{{margin-top:10px;color:#8b949e;font-size:12px}}
.closed-foot,.after-foot{{position:fixed;left:0;right:0;bottom:0;padding:6px 16px;font-size:12px;font-weight:700;text-align:center}}
.after-foot{{background:#3d1414;color:#ffb4b4}} .closed-foot{{background:#21262d;color:#8b949e}}
</style></head><body class="{body_cls}">
{banner_row}
{plan_html}
<div class="row2">{greed_html}{ladder_html}</div>
<div class="row3">{caps_html}{cooldown_html}{streak_html}</div>
<div class="stats">
<div><small>{read['symbol']} · {read['last_bar']} ET{delay}</small><b>{read['price']}</b></div>
<div><small>σ-extension</small><b>{read['sigma_ext']:+.2f}σ</b></div>
<div><small>regime</small><b>{read['regime']}</b><small>dir {read['directionality']} · rng {read['range_pct']}%</small></div>
<div><small>VWAP</small><b>{read['vwap']}</b><small>slope {read['vwap_slope_pct']:+.2f}%/hr</small></div>
<div><small>RSI(14)</small><b>{read['rsi'] if read['rsi'] is not None else '—'}</b></div>
<div><small>session</small><b>{read['tod']}</b></div>
</div>
<canvas id="ch" width="1040" height="580"></canvas>
{legend_html}
<table><tr><th>level</th><th>what</th><th>dist</th><th>zone</th></tr>
<tr><td class="tcap" colspan="4">ZONE = 2+ independent levels within 0.15% — higher-conviction reaction candidates.</td></tr>{zrows}</table>
<div class="foot">PDH/PDL/PDC = prior day high/low/close · ORH/ORL = first-30-min range · ±σ = VWAP bands · ZONE = ≥2 levels within 0.15%</div>
<div class="foot">generated {read['generated']} · auto-refresh 60s · data cadence 5m ·
fade signal = UNVALIDATED HYPOTHESIS until the Lab backtest returns a keep
(docs/intraday-cockpit.md)</div>
{'<div class="after-foot">14:30 past — no new 0DTE (contract rule 6)</div>' if (after_230 and not closed) else ''}
{'<div class="closed-foot">market closed — last bar ' + read['last_bar'] + ' ET</div>' if closed else ''}
<script>
const D={json.dumps(data)};
const cv=document.getElementById('ch'),cx=cv.getContext('2d');
const P=D.bars.map(b=>b.c),V=D.vwap,S=D.sigma,n=P.length;
const W=cv.width,LP=44,RM=76;
const priceH=380,rsiTop=384,rsiH=70,macdTop=458,macdH=90;
let ys=[...P];V.forEach((v,i)=>{{ys.push(v+2*S[i],v-2*S[i]);}});
const pd=D.read.prior||{{}};['high','low','close'].forEach(k=>{{if(pd[k])ys.push(pd[k]);}});
const lo=Math.min(...ys),hi=Math.max(...ys),pad=(hi-lo)*0.05,loB=lo-pad,hiB=hi+pad;
const X=i=>LP+(W-LP-RM)*i/Math.max(n-1,1);
const clamp=p=>Math.max(loB,Math.min(hiB,p));
const Yp=p=>8+(priceH-24)*(1-(clamp(p)-loB)/(hiB-loB));
function tmin(s){{const m=/^(\\d{{1,2}}):(\\d{{2}})/.exec(s||'');return m?(+m[1])*60+(+m[2]):null;}}
const BT=D.bars.map(b=>tmin(b.t));
function xForMin(t){{if(t<=BT[0])return X(0);if(t>=BT[n-1])return X(n-1);
for(let i=1;i<n;i++){{if(BT[i]>=t){{const f=(t-BT[i-1])/((BT[i]-BT[i-1])||1);return X(i-1)+f*(X(i)-X(i-1));}}}}return X(n-1);}}
function nearIdx(s){{const t=tmin(s);if(t==null)return null;let bi=0,bd=1e9;
BT.forEach((v,i)=>{{if(v!=null){{const d=Math.abs(v-t);if(d<bd){{bd=d;bi=i;}}}}}});return bi;}}
function line(a,col,w,dash,Yf){{cx.strokeStyle=col;cx.lineWidth=w;cx.setLineDash(dash||[]);
cx.beginPath();let st=false;a.forEach((p,i)=>{{if(p==null){{st=false;return;}}const y=(Yf||Yp)(p);
if(st)cx.lineTo(X(i),y);else{{cx.moveTo(X(i),y);st=true;}}}});cx.stroke();cx.setLineDash([]);}}
function place(items){{items.sort((a,b)=>a.y-b.y);for(let i=1;i<items.length;i++){{
if(items[i].y-items[i-1].y<12)items[i].y=items[i-1].y+12;}}
for(let i=items.length-1;i>=0;i--){{if(items[i].y>priceH-6)items[i].y=priceH-6;
if(i>0&&items[i].y-items[i-1].y<12)items[i-1].y=items[i].y-12;}}
items.forEach(it=>it.y=Math.max(10,Math.min(priceH-6,it.y)));return items;}}
// ---- R6 hourly gridlines + labels
cx.font='10px sans-serif';cx.textAlign='center';
for(let h=10;h<=16;h++){{const xx=xForMin(h*60);cx.strokeStyle='rgba(139,148,158,0.10)';cx.lineWidth=1;
cx.setLineDash([]);cx.beginPath();cx.moveTo(xx,8);cx.lineTo(xx,macdTop+macdH);cx.stroke();
cx.fillStyle='#8b949e';cx.fillText((h<10?'0':'')+h+':00',xx,macdTop+macdH+16);}}
cx.textAlign='left';
// ---- price pane: sigma band fills + edges
const bnd=m=>V.map((v,i)=>v+m*S[i]);
const U1=bnd(1),D1=bnd(-1),U2=bnd(2),D2=bnd(-2),U3=bnd(3),D3=bnd(-3);
function fillBand(up,dn,al){{cx.save();cx.globalAlpha=al;cx.fillStyle='#4a7dbd';cx.beginPath();
up.forEach((p,i)=>{{const y=Yp(p);i?cx.lineTo(X(i),y):cx.moveTo(X(i),y);}});
for(let i=dn.length-1;i>=0;i--)cx.lineTo(X(i),Yp(dn[i]));cx.closePath();cx.fill();cx.restore();}}
fillBand(U1,D1,0.10);fillBand(U2,U1,0.08);fillBand(D1,D2,0.08);fillBand(U3,U2,0.06);fillBand(D2,D3,0.06);
[U3,U2,U1,D1,D2,D3].forEach(a=>line(a,'#31404f',1));
// ---- B6 right-edge labels (sigma + VWAP), collision-avoided
let RL=[];
[['+3σ',U3],['+2σ',U2],['+1σ',U1],['-1σ',D1],['-2σ',D2],['-3σ',D3]].forEach(z=>{{
const p=z[1][n-1];if(p>=loB&&p<=hiB)RL.push({{y:Yp(p),t:z[0]+' '+p.toFixed(2),c:'#6e7d8c'}});}});
{{const vp=V[n-1];if(vp>=loB&&vp<=hiB)RL.push({{y:Yp(vp),t:'VWAP '+vp.toFixed(2),c:'#c9a227'}});}}
place(RL);cx.font='10px sans-serif';cx.textAlign='left';
RL.forEach(it=>{{cx.fillStyle=it.c;cx.fillText(it.t,W-RM+4,it.y+3);}});
// ---- B6 left labels (prior-day / OR), collision-avoided
function hline(p,col){{cx.strokeStyle=col;cx.lineWidth=1;cx.setLineDash([2,4]);
cx.beginPath();cx.moveTo(LP,Yp(p));cx.lineTo(W-RM,Yp(p));cx.stroke();cx.setLineDash([]);}}
let LL=[];
[[pd.high,'#8b949e','PDH'],[pd.low,'#8b949e','PDL'],[pd.close,'#c9a227','PDC'],
[D.read.or_hi,'#4a7dbd','ORH'],[D.read.or_lo,'#4a7dbd','ORL']].forEach(z=>{{
if(z[0]&&z[0]>=loB&&z[0]<=hiB){{hline(z[0],z[1]);LL.push({{y:Yp(z[0]),t:z[2]+' '+z[0],c:z[1]}});}}}});
place(LL);LL.forEach(it=>{{cx.fillStyle=it.c;cx.fillText(it.t,LP+4,it.y-2);}});
// VWAP + price
line(V,'#c9a227',2,[6,4]);line(P,'#7ee2a8',2);
// ---- B6 boxed current-price tag on right axis
{{const yp=Yp(P[n-1]);cx.fillStyle='#7ee2a8';cx.fillRect(W-RM+2,yp-7,RM-4,14);
cx.fillStyle='#0d1117';cx.font='bold 10px ui-monospace,monospace';cx.textAlign='left';
cx.fillText(P[n-1].toFixed(2),W-RM+5,yp+3);cx.font='10px sans-serif';}}
// ---- 14:30 theta cliff (permanent)
{{const xx=xForMin(870);cx.strokeStyle='#e0574f';cx.lineWidth=1;cx.setLineDash([4,4]);
cx.beginPath();cx.moveTo(xx,8);cx.lineTo(xx,macdTop+macdH);cx.stroke();cx.setLineDash([]);
cx.fillStyle='#e0574f';cx.save();cx.translate(xx+3,20);cx.fillText('0DTE theta cliff',0,0);cx.restore();}}
// ---- gate-trip markers
const MK={{ROLLUP:['⛔','#ff6b6b'],EXT_TOP:['▲','#ff9f43'],GIVEBACK:['↓','#ff6b6b'],
FADE:['◆','#ffd479'],REGIME:['⟳','#8b949e'],CONFLUENCE:['▪','#c9a227'],SIZE:['◆','#ff9f43'],COOLDOWN:['⟳','#8b949e']}};
cx.font='13px sans-serif';cx.textAlign='center';
(D.gates||[]).forEach(gt=>{{const i=nearIdx(gt.t);if(i==null)return;const mk=MK[gt.type]||['•','#ccc'];
const y=(gt.px!=null&&gt.px>=loB&&gt.px<=hiB)?Yp(gt.px):Yp(P[i]);cx.fillStyle=mk[1];cx.fillText(mk[0],X(i),y-6);}});
cx.textAlign='left';
// ---- separators
cx.strokeStyle='#21262d';cx.lineWidth=1;[382,456].forEach(y=>{{cx.beginPath();cx.moveTo(0,y);cx.lineTo(W,y);cx.stroke();}});
// ---- RSI pane (R4)
const RS=D.rsi;const Yr=v=>rsiTop+6+(rsiH-12)*(1-Math.max(0,Math.min(100,v))/100);
cx.save();cx.globalAlpha=0.06;cx.fillStyle='#da3633';cx.fillRect(LP,Yr(100),W-LP-RM,Yr(70)-Yr(100));
cx.fillStyle='#2ea043';cx.fillRect(LP,Yr(30),W-LP-RM,Yr(0)-Yr(30));cx.restore();
[[30,'#8b949e',[2,4]],[50,'#21262d',[]],[70,'#8b949e',[2,4]]].forEach(z=>{{
cx.strokeStyle=z[1];cx.setLineDash(z[2]);cx.beginPath();cx.moveTo(LP,Yr(z[0]));cx.lineTo(W-RM,Yr(z[0]));cx.stroke();cx.setLineDash([]);
cx.fillStyle='#8b949e';cx.font='9px sans-serif';cx.fillText(z[0],W-RM+4,Yr(z[0])+3);}});
line(RS,'#c996ff',1.5,[],Yr);
cx.fillStyle='#8b949e';cx.font='10px sans-serif';cx.fillText('RSI(14)',LP+4,rsiTop+12);
{{let last=null;for(let i=RS.length-1;i>=0;i--){{if(RS[i]!=null){{last=RS[i];break;}}}}
if(last!=null){{cx.fillStyle='#c996ff';cx.fillText(last.toFixed(1),W-RM+4,rsiTop+12);}}}}
// ---- MACD pane (B2 + R5)
const MC=D.macd,SG=D.sig,HS=D.hist;let mx=1e-6;
[MC,SG,HS].forEach(a=>a.forEach(v=>{{if(v!=null)mx=Math.max(mx,Math.abs(v));}}));
const Ym=v=>macdTop+macdH/2-(v/mx)*(macdH/2-10);
const bw=Math.max(1,(X(1)-X(0))*0.6);
HS.forEach((v,i)=>{{if(v==null)return;cx.fillStyle=v>=0?'#2ea043':'#da3633';
const y0=Ym(0),y1=Ym(v);cx.fillRect(X(i)-bw/2,Math.min(y0,y1),bw,Math.abs(y1-y0)||1);}});
cx.strokeStyle='#586069';cx.setLineDash([]);cx.beginPath();cx.moveTo(LP,Ym(0));cx.lineTo(W-RM,Ym(0));cx.stroke();
cx.fillStyle='#586069';cx.font='9px sans-serif';cx.fillText('0',W-RM+4,Ym(0)+3);
line(MC,'#58a6ff',1.5,[],Ym);line(SG,'#f0883e',1.5,[],Ym);
cx.fillStyle='#8b949e';cx.font='10px sans-serif';cx.fillText('MACD (blue) · signal (orange) · histogram',LP+4,macdTop+12);
// ---- equity mini-canvas (B3 low-n)
(function(){{const eq=document.getElementById('eq');if(!eq)return;const ex=eq.getContext('2d');
const A=D.greed.cum_disc||[],B=D.greed.cum_final||[];
if(A.length<2){{ex.fillStyle='#8b949e';ex.font='11px sans-serif';
ex.fillText('1 day logged — curves start at day 2',14,64);return;}}
const all=A.concat(B);let mn=Math.min(...all,0),mxx=Math.max(...all,0),rp=(mxx-mn)*0.1||1;mn-=rp;mxx+=rp;
const EX=i=>44+(eq.width-59)*i/Math.max(A.length-1,1);
const EY=v=>10+(eq.height-28)*(1-(v-mn)/(mxx-mn));
ex.font='9px sans-serif';[mn,0,mxx].forEach(v=>{{ex.strokeStyle='#21262d';ex.beginPath();
ex.moveTo(44,EY(v));ex.lineTo(eq.width-15,EY(v));ex.stroke();ex.fillStyle='#586069';ex.fillText('$'+Math.round(v),2,EY(v)+3);}});
ex.fillStyle='#586069';ex.fillText(D.greed.l0||'',44,eq.height-2);
ex.textAlign='right';ex.fillText(D.greed.l1||'',eq.width-15,eq.height-2);ex.textAlign='left';
function el(a,col){{ex.strokeStyle=col;ex.lineWidth=2;ex.beginPath();
a.forEach((v,i)=>i?ex.lineTo(EX(i),EY(v)):ex.moveTo(EX(i),EY(v)));ex.stroke();}}
el(A,'#2ea043');el(B,B[B.length-1]<0?'#e0574f':'#e6edf3');}})();
// ---- G3 cooldown clock (client-side, from rendered last-win time)
(function(){{const cd=D.cooldown;if(!cd)return;const box=document.getElementById('cooldown'),clk=document.getElementById('cdclock');
if(!box||!clk)return;const m=/^(\\d{{1,2}}):(\\d{{2}})/.exec(cd);if(!m)return;
const end=new Date();end.setHours(+m[1],+m[2],0,0);end.setMinutes(end.getMinutes()+15);
function tick(){{const rem=Math.floor((end-new Date())/1000);
if(rem<=0){{box.style.display='none';document.body.classList.remove('cooldown-on');return;}}
box.style.display='';document.body.classList.add('cooldown-on');
const mm=String(Math.floor(rem/60)).padStart(2,'0'),ss=String(rem%60).padStart(2,'0');clk.textContent=mm+':'+ss;
setTimeout(tick,1000);}}tick();}})();
</script></body></html>"""
    return html


# ---------------------------------------------------------------- main
def main():
    args = [a for a in sys.argv[1:]]
    symbol = next((a for a in args if not a.startswith("-")), "QQQ").upper()
    day = None
    if "--date" in args:
        day = args[args.index("--date") + 1]
    force = "--force" in args or day is not None

    now = now_et()
    if not force:
        if now.weekday() >= 5 or not ("09:35" <= now.strftime("%H:%M") <= "16:10"):
            return  # outside RTH — launchd fires 24/7, script self-gates
    day = day or now.strftime("%Y-%m-%d")

    load_env()
    token = load_token()
    if not token:
        sys.exit("intraday_read: no TRADIER_TOKEN (.env)")
    base = os.environ.get("TRADIER_BASE", "https://api.tradier.com")
    delayed = "sandbox" in base

    bars = timesales(symbol, day, token, base)
    if len(bars) < 3:
        print(f"intraday_read: only {len(bars)} bars for {symbol} {day} — nothing to render")
        return
    prior = prior_session(symbol, day, token, base)

    bands = vwap_bands(bars)
    closes = [b["c"] for b in bars]
    px, vwap, sigma = closes[-1], bands[-1]["vwap"], bands[-1]["sigma"]
    ext = (px - vwap) / sigma if sigma > 0 else 0.0
    or_bars = [b for b in bars if b["t"] < "10:00"]
    or_hi = max((b["h"] or b["c"]) for b in or_bars) if or_bars else None
    or_lo = min((b["l"] or b["c"]) for b in or_bars) if or_bars else None
    label, d, rng, slope = regime_label(bars, prior.get("close"), bands)
    zones = build_levels(bars, prior, or_hi, or_lo, vwap, sigma)

    read = {"symbol": symbol, "date": day, "last_bar": bars[-1]["t"], "price": px,
            "vwap": round(vwap, 2), "sigma": round(sigma, 3),
            "sigma_ext": round(ext, 2), "rsi": rsi(closes),
            "regime": label, "directionality": d, "range_pct": rng,
            "vwap_slope_pct": round(slope, 2), "tod": tod_bucket(bars[-1]["t"]),
            "or_hi": or_hi, "or_lo": or_lo,
            "prior": {k: prior.get(k) for k in ("high", "low", "close")},
            "zones": zones, "delayed": delayed,
            "generated": now.strftime("%Y-%m-%d %H:%M:%S ET")}

    # indicator series for the panes (importable, dual-use)
    rsi_ser = rsi_series(closes)
    macd_d = macd(closes)

    # market gates + dedupe + gate_log persistence (C2)
    os.makedirs(OUT, exist_ok=True)
    state_p = os.path.join(OUT, ".gate_state.json")
    prev = load_json(state_p) or {}
    gates = eval_gates(read, prev.get("regime"))
    read["gates"] = gates
    mkt_sig = "|".join(g.split(" ")[0] for g in gates)  # gate types, not values
    prev_types = {s for s in (prev.get("sig") or "").split("|") if s}
    t_now = bars[-1]["t"]
    transitions = [gate_to_entry(g, t_now, px) for g in gates
                   if g.split(" ")[0] not in prev_types]
    gate_log_p = os.path.join(OUT, "gate_log.jsonl")
    append_gate_log(gate_log_p, day, transitions)

    # behavioral gates from session_state — notify via the same dedupe (F3b)
    ss = load_json(os.path.join(OUT, "session_state.json"))
    bgates = behavioral_gates(ss)
    beh_sig = "|".join(bg["type"] for bg in bgates)
    combined = (mkt_sig + "#" + beh_sig).strip("#")

    # B5: market-closed / after-hours → suppress notify() + neutral banner state
    last_bar = bars[-1]["t"]
    closed = market_closed(last_bar, now)
    after_230 = "14:30" <= last_bar < "16:00"
    if not closed and (gates or bgates) and combined != prev.get("sig_all"):
        msg = " · ".join(gates + [f"{bg['type']}: {bg['label']}" for bg in bgates])
        notify(f"{symbol} cockpit", msg[:180])
    json.dump({"sig": mkt_sig, "sig_all": combined, "regime": label}, open(state_p, "w"))

    # greed-panel data + today's gate markers + V3 discipline panels
    greed = build_greed(day, ss)
    gate_log = read_gate_log(gate_log_p, day)
    rows = read_scalp_days(os.path.join(ROOT, "data", "scalp_days.csv"))
    goal = read_goal_config()
    lessons = read_lessons()
    behavioral_in_log = any(e.get("type") in BEHAVIORAL_TYPES for e in gate_log)
    plan = get_plan(ss)
    plan_filled = bool(plan.get("bias") or plan.get("setup") or plan.get("no_trade"))
    now_hm = now.strftime("%H:%M")
    ctx = {
        "ladder": build_ladder(goal, rows),
        "caps": build_caps(ss),
        "streak": build_streak(rows),
        "plan": plan,
        "plan_banner": (not plan_filled) and now.weekday() < 5 and now_hm >= "09:45",
        "flash": lessons[-1] if (behavioral_in_log and lessons) else None,
        "closed": closed,
        "after_230": after_230,
        "banner_class": banner_severity(gates, bool(bgates) or behavioral_in_log),
        "last_win": (ss.get("last_win_time") if isinstance(ss, dict)
                     and ss.get("date") == day else None),
    }

    json.dump(read, open(os.path.join(OUT, "read.json"), "w"), indent=2)
    with open(os.path.join(OUT, "read.html"), "w") as f:
        f.write(render_html(read, bars, bands, rsi_ser, macd_d, gate_log, greed, ctx))
    print(f"intraday_read: {symbol} {day} {last_bar} px {px} ext {ext:+.2f}σ "
          f"{label} gates:[{'; '.join(gates) or 'none'}] beh:[{beh_sig or 'none'}] "
          f"closed:{closed} → data/intraday/read.html")


if __name__ == "__main__":
    main()
