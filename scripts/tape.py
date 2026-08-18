#!/usr/bin/env python3
"""Build the day's TAPE for the Fleet Brief — per-underlying daily OHLC + a
quantified regime read — and write it to data/brief/<date>_tape.json.

DATA SOURCE (two tiers, in order):
  1. TRADIER (preferred): exact daily OHLC for each underlying declared by
     data/bot_gates.csv (currently SPX, QQQ, VIX; SPX index served directly
     → reliable high/low → reliable breach flags). Needs a token: env TRADIER_TOKEN, or a TRADIER_TOKEN=... line in ./.env
     (repo root; .env is git-ignored and NOT backed up — see memory). Endpoint is
     configurable via TRADIER_BASE (default the production host).
  2. RECONSTRUCTION (fallback, spec-endorsed): if there is no token / the feed is
     down, rebuild open+close from the ledger's underlying_open/underlying_close
     prints and the prior session's close, and APPROXIMATE the high/low from the
     open/close envelope + any short-strike breach evidence (a leg that ran to deep
     max-loss proves the underlying reached that strike). Every field carries a
     `source` = "tradier" | "reconstructed" so the brief can say so out loud.

Regime read (under the chart): %move, gap%, realized range%, net move%, a
directionality ratio (chop↔trend), and a Chop/Drift/Trend label. Path-based
numbers are only exact with Tradier intraday; in fallback they're marked approx.

Usage:  python3 scripts/tape.py [YYYY-MM-DD]
        (date defaults to the newest open_date in data/trades.csv)
"""
import argparse, csv, os, sys, json, datetime, urllib.request, urllib.parse, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")
BRIEF = os.path.join(D, "brief")

# Underlyings that get a tape = the union of `underlying` values referenced by
# the signed rows of data/bot_gates.csv (empty cells ignored). Map symbol ->
# the Tradier symbol. VERIFIED on sandbox 2026-07-03: cash indices are PLAIN
# tickers ("SPX", "VIX") — the "$SPX.X"/"$VIX.X" forms return history:null.
TRADIER_SYMBOL = {"SPX": "SPX", "QQQ": "QQQ", "SPY": "SPY", "VIX": "VIX"}


def fl(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


class TradierError(Exception):
    """Raised by _get() so build() can choose the right failure path."""
    def __init__(self, mode, detail=None):
        self.mode = mode
        self.detail = detail or ""
        super().__init__(f"{mode}: {self.detail}")


class GateSymbolError(Exception):
    """Raised by underlyings_on() when the gates table cannot supply the
    symbol set. build() turns this into a loud, non-zero exit so a missing
    data/bot_gates.csv never silently reverts to fill-based selection.
    """



# ----------------------------------------------------------------------------
# token / env
# ----------------------------------------------------------------------------
def load_env():
    """Populate os.environ from ./.env for any TRADIER_* key not already set
    (real env wins over the file). Returns nothing; read via os.environ after."""
    env = os.path.join(ROOT, ".env")
    if not os.path.exists(env):
        return
    for line in open(env):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k.startswith("TRADIER_") and not os.environ.get(k):
            os.environ[k] = v


def load_token():
    return (os.environ.get("TRADIER_TOKEN") or "").strip() or None


def now_iso():
    """Reproducible 'generated' timestamp. SOURCE_DATE_EPOCH wins over wall clock."""
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        return datetime.datetime.fromtimestamp(
            int(epoch), tz=datetime.timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds")
    return datetime.datetime.now().isoformat(timespec="seconds")


def today_iso():
    """Reproducible 'today' for newest_date() fallback."""
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        return datetime.datetime.fromtimestamp(
            int(epoch), tz=datetime.timezone.utc).date().isoformat()
    return datetime.date.today().isoformat()


def _get(base, path, params, token):
    """Call the Tradier v1 endpoint. Never returns None for a failure.

    Raises TradierError with one of four modes:
      - token-absent     : no token was supplied
      - token-rejected   : HTTP 401/403 (present credentials not accepted)
      - feed-down        : other HTTP status, network error, or empty response
      - parse-error      : response was not valid JSON
    """
    if not token:
        raise TradierError("token-absent", "TRADIER_TOKEN not set")
    url = f"{base.rstrip('/')}/v1/{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            body = r.read().decode()
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            raise TradierError("token-rejected", f"HTTP {e.code}") from e
        raise TradierError("feed-down", f"HTTP {e.code}") from e
    except (urllib.error.URLError, OSError) as e:
        raise TradierError("feed-down", str(e)) from e
    try:
        return json.loads(body)
    except ValueError as e:
        raise TradierError("parse-error", str(e)) from e


def tradier_history(symbol, day, token, base):
    """Daily OHLC for `day` + the PRIOR session's close, in one call.
    Returns {open,high,low,close,prior_close} or raises TradierError."""
    start = (datetime.date.fromisoformat(day) - datetime.timedelta(days=10)).isoformat()
    data = _get(base, "markets/history",
                {"symbol": symbol, "interval": "daily", "start": start, "end": day}, token)
    h = data.get("history")
    if not h or h in ("null", None):
        raise TradierError("feed-down", "history returned no data")
    days = h.get("day")
    days = days if isinstance(days, list) else [days] if isinstance(days, dict) else []
    days = [d for d in days if isinstance(d, dict) and d.get("date")]
    if not days:
        raise TradierError("feed-down", "history returned no days")
    days.sort(key=lambda d: d["date"])
    today = next((d for d in days if d["date"] == day), None)
    if not today:
        raise TradierError("feed-down", f"history missing {day}")
    priors = [d for d in days if d["date"] < day]
    out = {k: fl(today.get(k)) for k in ("open", "high", "low", "close")}
    out["prior_close"] = fl(priors[-1].get("close")) if priors else None
    return out


def tradier_timesales(symbol, day, token, base, interval="5min"):
    """Intraday session path for `day`. Returns [{t:'HH:MM', p, h, l}, ...] or raises TradierError."""
    data = _get(base, "markets/timesales",
                {"symbol": symbol, "interval": interval,
                 "start": f"{day} 09:30", "end": f"{day} 16:00"}, token)
    s = data.get("series")
    if not s or s in ("null", None):
        raise TradierError("feed-down", "timesales returned no data")
    bars = s.get("data")
    bars = bars if isinstance(bars, list) else [bars] if isinstance(bars, dict) else []
    out = []
    for b in bars:
        t = (b.get("time") or "")[11:16]
        p = fl(b.get("close")) if b.get("close") is not None else fl(b.get("price"))
        if t and p is not None:
            out.append({"t": t, "p": round(p, 2),
                        "h": fl(b.get("high")), "l": fl(b.get("low"))})
    return out


def _relabel(reg):
    """Chop/Drift/Trend from realized range + real path directionality (Tradier)."""
    r, d = reg.get("range_pct"), reg.get("directionality")
    if r is None:
        return {}
    if r < 0.75 and (d is None or d < 0.5):
        return {"label": "Chop", "meaning": "IC day — price held inside the ±0.75% GO band."}
    if r > 1.5 or (d is not None and d >= 0.6):
        return {"label": "Trend", "meaning": "Directional day — range/one-way move outran the IC band."}
    return {"label": "Drift", "meaning": "In-between — modest range, no clean one-way trend."}


def path_directionality(series):
    """|net move| ÷ total path length over the intraday series (chop↔trend)."""
    pts = [b["p"] for b in series if b.get("p") is not None]
    if len(pts) < 2:
        return None
    path = sum(abs(pts[i] - pts[i - 1]) for i in range(1, len(pts)))
    net = abs(pts[-1] - pts[0])
    return round(net / path, 2) if path > 0 else None


# ----------------------------------------------------------------------------
# ledger reconstruction (fallback)
# ----------------------------------------------------------------------------
def load_trades():
    p = os.path.join(D, "trades.csv")
    if not os.path.exists(p):
        sys.exit(f"ERROR: missing {p} (run build_ledger.py first)")
    return list(csv.DictReader(open(p)))


def _load_gate_symbols(gates_path):
    """Return the set of non-empty `underlying` values from data/bot_gates.csv.
    Skip '#' comment lines and empty underlying cells."""
    syms = set()
    with open(gates_path, newline="") as f:
        reader = csv.DictReader(line for line in f if not line.startswith("#"))
        for r in reader:
            u = (r.get("underlying") or "").strip()
            if u:
                syms.add(u)
    return syms


def underlyings_on(trades, day, gates_path=None):
    """Symbols for the day's tape = the union of `underlying` values in the
    signed data/bot_gates.csv table, not that day's fills.

    The `trades` and `day` arguments are retained for call-site compatibility
    but are no longer used; the symbol set is a static function of the gates
    table (R-2026-08-19-TAPE-SYMBOLS-FROM-GATES).
    """
    if gates_path is None:
        gates_path = os.path.join(D, "bot_gates.csv")
    if not os.path.exists(gates_path):
        raise GateSymbolError(
            f"missing {gates_path} — cannot select tape symbols; "
            "refusing to fall back to fill-based selection "
            "(R-2026-08-19-TAPE-SYMBOLS-FROM-GATES)"
        )
    return sorted(_load_gate_symbols(gates_path))


def prints_for(trades, symbol, day):
    """(open, close) underlying prints for a symbol on a day, from the ledger.
    NOTE: underlying_open in the OA export is the price AT EACH BOT'S ENTRY, not the
    9:30 print — so we take the EARLIEST-opening trade's value as the best proxy for
    the day's open (averaging entry-time snapshots would be meaningless). close is
    the day's settle, consistent across legs, so we take the last one seen."""
    day_legs = sorted((t for t in trades
                       if t["open_date"][:10] == day and t["underlying"] == symbol),
                      key=lambda t: t["open_date"])
    o = c = None
    for t in day_legs:
        if o is None and fl(t["underlying_open"]):
            o = fl(t["underlying_open"])          # earliest entry snapshot
        if fl(t["underlying_close"]):
            c = fl(t["underlying_close"])          # day settle
    return o, c


def prior_close(trades, symbol, day):
    """Prior session's close for a symbol = latest underlying_close before `day`."""
    best_d, best_c = "", None
    for t in trades:
        d = t["open_date"][:10]
        if t["underlying"] == symbol and d < day:
            c = fl(t["underlying_close"])
            if c and d > best_d:
                best_d, best_c = d, c
    return best_c


def breach_lows_highs(trades, symbol, day):
    """Reconstruct an approximate intraday extreme from breach evidence: a short
    leg that ran to (near) MAX LOSS proves price reached ~its short strike. Use
    ror = pnl/risk (unambiguous: -1.0 = full loss) — NOT the leg mae_pct, whose
    units are inconsistent and flag minor excursions as breaches. Returns
    (approx_low, approx_high) or (None, None)."""
    lows, highs = [], []
    for t in trades:
        if t["open_date"][:10] != day or t["underlying"] != symbol:
            continue
        pnl, risk = fl(t["pnl"]), fl(t["risk"])
        ror = (pnl / risk) if (pnl is not None and risk) else None
        maxloss = ror is not None and ror <= -0.9
        if t["structure"] == "shortputspread" and maxloss:
            sp = fl(t["short_put"])
            if sp:
                lows.append(sp)
        if t["structure"] == "shortcallspread" and maxloss:
            sc = fl(t["short_call"])
            if sc:
                highs.append(sc)
    return (min(lows) if lows else None, max(highs) if highs else None)


# ----------------------------------------------------------------------------
# regime read
# ----------------------------------------------------------------------------
def regime(o, h, l, c, pc, has_path):
    """Quantified regime metrics + label from OHLC and prior close.

    has_path=True only when we have a REAL intraday high/low (Tradier). Then the
    directionality ratio (|net| ÷ path length) is meaningful and drives the label.
    In reconstruction mode (has_path=False) we only have the open→close envelope,
    which makes any non-flat day look like a pure trend — so we DON'T compute
    directionality; we label on move magnitude alone and mark the label approx."""
    out = {"pct_move": None, "gap_pct": None, "full_pct": None,
           "range_pct": None, "net_pct": None, "directionality": None,
           "label": "n/a", "label_approx": not has_path, "meaning": ""}
    if o and c:
        out["pct_move"] = round((c - o) / o * 100, 2)     # close vs open
        out["net_pct"] = out["pct_move"]
    if pc and o:
        out["gap_pct"] = round((o - pc) / pc * 100, 2)    # open vs prior close
    if pc and c:
        out["full_pct"] = round((c - pc) / pc * 100, 2)   # close vs prior close
    if h and l and pc:
        out["range_pct"] = round((h - l) / pc * 100, 2)
    elif o and c and pc:  # fallback range floor = open→close envelope
        out["range_pct"] = round(abs(c - o) / pc * 100, 2)
    if has_path and h and l and o and c:
        rng = h - l
        net = abs(c - o)
        path = max(2 * rng - net, net, 1e-9)
        out["directionality"] = round(net / path, 2)
    # label
    if has_path:
        r, d = out["range_pct"], out["directionality"]
        if r is not None:
            if r < 0.75 and (d is None or d < 0.5):
                out["label"], out["meaning"] = "Chop", "IC day — price stayed inside the ±0.75% GO band."
            elif r > 1.5 or (d is not None and d >= 0.6):
                out["label"], out["meaning"] = "Trend", "Directional day — range/one-way move outran the IC band."
            else:
                out["label"], out["meaning"] = "Drift", "In-between — modest range, no clean one-way trend."
    else:
        # magnitude = the biggest of realized range / full move / net move
        mag = max((abs(x) for x in (out["range_pct"], out["full_pct"], out["net_pct"])
                   if x is not None), default=None)
        if mag is not None:
            if mag < 0.75:
                out["label"], out["meaning"] = "Chop", "IC day — move stayed within the ±0.75% band (approx; no intraday path)."
            elif mag > 1.5:
                out["label"], out["meaning"] = "Trend", "Directional day — move outran the IC band (approx; no intraday path)."
            else:
                out["label"], out["meaning"] = "Drift", "In-between move (approx; no intraday path — connect Tradier for a true read)."
    return out


# ----------------------------------------------------------------------------
def build(day):
    fixture_path = os.path.join(BRIEF, f"{day}_tape.json")
    if os.environ.get("TAPE_FIXTURE"):
        if not os.path.exists(fixture_path):
            sys.exit(f"ERROR: TAPE_FIXTURE set but no committed fixture at {fixture_path}")
        with open(fixture_path) as f:
            out = json.load(f)
        out["generated"] = now_iso()
        srcs = ", ".join(f"{s}:{t['source']}" for s, t in out.get("underlyings", {}).items())
        print(f"tape.py: TAPE_FIXTURE using committed {os.path.relpath(fixture_path, ROOT)} | {srcs}")
        return out

    trades = load_trades()
    try:
        syms = underlyings_on(trades, day)
    except GateSymbolError as e:
        print(f"tape.py: ERROR: {e}", file=sys.stderr)
        sys.exit(2)
    if not syms:
        print(f"tape.py: no underlyings declared in data/bot_gates.csv — nothing to chart.")
    load_env()
    token = load_token()
    base = os.environ.get("TRADIER_BASE", "https://api.tradier.com")

    tapes = {}
    # VIX is part of the gates union, but keep it explicit and deduplicate.
    for sym in sorted(set(syms + ["VIX"])):
        src = None
        o = h = l = c = pc = None
        series = []
        rec_reason = None
        tsym = TRADIER_SYMBOL.get(sym, sym)
        if token:
            try:
                rec = tradier_history(tsym, day, token, base)
                if rec and rec.get("close") is not None:
                    o, h, l, c = rec["open"], rec["high"], rec["low"], rec["close"]
                    pc = rec.get("prior_close")
                    src = "tradier"
                    series = tradier_timesales(tsym, day, token, base)
            except TradierError as e:
                if e.mode == "token-rejected":
                    print(f"tape.py: 🔴 TRADIER TOKEN REJECTED ({e.detail}). "
                          "Do not re-issue or rotate the token; resolve the credentials before re-running.",
                          file=sys.stderr)
                    sys.exit(3)
                rec_reason = e.mode
        else:
            rec_reason = "token-absent"
        if src is None and sym != "VIX":
            o, c = prints_for(trades, sym, day)
            bl, bh = breach_lows_highs(trades, sym, day)
            # approx high/low = open/close envelope widened by any breach evidence
            cand_hi = [x for x in (o, c, bh) if x]
            cand_lo = [x for x in (o, c, bl) if x]
            h = max(cand_hi) if cand_hi else None
            l = min(cand_lo) if cand_lo else None
            src = "reconstructed" if (o or c) else None
        if src is None:
            continue
        if pc is None:
            pc = prior_close(trades, sym, day)   # ledger fallback for prior close
        has_path = bool(series)
        rec = {"symbol": sym, "source": src, "prior_close": pc,
               "open": o, "high": h, "low": l, "close": c,
               "series": series, "series_interval": "5min" if series else None}
        if src == "reconstructed":
            rec["reconstructed_reason"] = rec_reason or "unknown"
        if sym != "VIX":
            reg = regime(o, h, l, c, pc, has_path=has_path)
            if has_path:                          # real path → true directionality
                reg["directionality"] = path_directionality(series)
                # relabel using the real directionality
                reg.update(_relabel(reg))
            rec.update(reg)
        else:
            rec["vix_close"] = c
            rec["vix_change_pct"] = (round((c - pc) / pc * 100, 2)
                                     if c and pc else None)
        tapes[sym] = rec

    # SPX-vs-QQQ relative strength divergence line
    div = None
    if "SPX" in tapes and "QQQ" in tapes:
        a, b = tapes["SPX"].get("full_pct"), tapes["QQQ"].get("full_pct")
        if a is not None and b is not None:
            div = {"spx_full_pct": a, "qqq_full_pct": b, "spread_pct": round(a - b, 2)}

    recon_reasons = sorted({t.get("reconstructed_reason")
                            for t in tapes.values() if t.get("source") == "reconstructed"})
    out = {"date": day, "generated": now_iso(),
           "any_reconstructed": any(t["source"] == "reconstructed" for t in tapes.values()),
           "reconstructed_reasons": recon_reasons,
           "underlyings": tapes, "divergence": div}
    os.makedirs(BRIEF, exist_ok=True)
    path = os.path.join(BRIEF, f"{day}_tape.json")
    json.dump(out, open(path, "w"), indent=2)

    srcs = ", ".join(f"{s}:{t['source']}" for s, t in tapes.items())
    note = (f"  ⚠ some tapes RECONSTRUCTED ({', '.join(recon_reasons)})"
            if recon_reasons else "")
    print(f"tape.py: wrote {os.path.relpath(path, ROOT)} | {srcs}{note}")
    return out


def newest_date():
    trades = load_trades()
    return max((t["open_date"][:10] for t in trades), default=today_iso())


def _run_selftest():
    """Hermetic self-test for the new gates-union symbol selection.

    Verifies:
      - non-empty underlying cells become the sorted symbol set
      - empty underlying cells and '#' comment lines are ignored
      - a missing gates file raises GateSymbolError (the loud failure path)
    """
    import tempfile
    import shutil

    td = tempfile.mkdtemp(prefix="tape-selftest-")
    try:
        good = os.path.join(td, "bot_gates.csv")
        with open(good, "w", newline="") as f:
            f.write("# data/bot_gates.csv — comment line\n")
            f.write("bot,pr_id,underlying,entry_window_et,gate_type,gate_params,eval_class,fill_precondition,source\n")
            f.write("A,PR-A,SPX,11:00,band_prior_close,abs_lt=0.75,EVALUABLE,,\n")
            f.write("B,PR-B,QQQ,13:30-14:00,band_prior_close_strict,gt=-0.75;lt=0.75,EVALUABLE,,\n")
            f.write("C,PR-C,,,,unknown,,,\n")  # empty underlying
            f.write("D,PR-D,VIX,11:00,vix_min,threshold=22,EVALUABLE,,\n")

        got = underlyings_on([], "2026-08-10", good)
        want = ["QQQ", "SPX", "VIX"]
        if got != want:
            print(f"SELFTEST FAIL: expected {want}, got {got}", file=sys.stderr)
            return 1

        missing = os.path.join(td, "missing_bot_gates.csv")
        try:
            underlyings_on([], "2026-08-10", missing)
            print("SELFTEST FAIL: missing gates file did not raise GateSymbolError",
                  file=sys.stderr)
            return 1
        except GateSymbolError as e:
            msg = str(e)
            if "missing" not in msg.lower() or "refusing to fall back" not in msg.lower():
                print(f"SELFTEST FAIL: unexpected error message: {msg}", file=sys.stderr)
                return 1

        print("tape.py selftest OK")
        return 0
    finally:
        shutil.rmtree(td, ignore_errors=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build the daily TAPE")
    ap.add_argument("day", nargs="?", help="YYYY-MM-DD (defaults to newest open_date)")
    ap.add_argument("--selftest", action="store_true", help="run hermetic self-test")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(_run_selftest())
    day = args.day or newest_date()
    build(day)
