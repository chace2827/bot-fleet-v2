#!/usr/bin/env python3
"""W0 cross-check: rebuild the PoC candidate tapes from the RAW captures and
compare against the candidates the PoC produced live.

A match validates the PoC pipeline: the derived tapes are exactly what the raw
Tradier bytes imply, with no drift between fetch and derivation.

Two fields are NECESSARILY volatile and are normalized before comparison, with
the normalization stated in the output rather than hidden:
    generated      — wall-clock stamp written by tape.now_iso()
    backfilled_at  — wall-clock stamp of the backfill run
Everything else, including every OHLC value and every one of the 79 5-min bars,
is compared exactly.
"""
import os, sys, json, urllib.parse, datetime

SP = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(SP, "w0-raw")
CAND = os.path.join(SP, "w0-evidence", "out")
REPO = os.path.expanduser("~/bot-fleet-v2")
sys.path.insert(0, os.path.join(REPO, "scripts"))
import tape as T  # noqa: E402

DAYS = ["2026-08-10", "2026-08-11", "2026-08-12", "2026-08-13"]
GATES = ["SPX", "QQQ"]


def raw_get(base, path, params, token):
    """Replay _get from the saved raw bodies instead of the network."""
    sym = params["symbol"]
    if path == "markets/history":
        day = params["end"]
        name = f"{sym}_{day}_daily.json"
    else:
        day = params["start"][:10]
        name = f"{sym}_{day}_5min.json"
    with open(os.path.join(RAW, name), "rb") as fh:
        return json.loads(fh.read().decode())


T._get = raw_get  # monkeypatch: derivation now reads ONLY the raw captures


def build(day, vix_series):
    tapes = {}
    for sym in GATES + ["VIX"]:
        if sym in tapes:
            continue
        tsym = T.TRADIER_SYMBOL.get(sym, sym)
        rec = T.tradier_history(tsym, day, "x", "https://api.tradier.com")
        o, h, l, c, pc = rec["open"], rec["high"], rec["low"], rec["close"], rec["prior_close"]
        series = []
        if (sym != "VIX") or vix_series:
            series = T.tradier_timesales(tsym, day, "x", "https://api.tradier.com")
        has_path = bool(series)
        out = {"symbol": sym, "source": "tradier", "prior_close": pc,
               "open": o, "high": h, "low": l, "close": c,
               "series": series, "series_interval": "5min" if series else None}
        if sym != "VIX":
            reg = T.regime(o, h, l, c, pc, has_path=has_path)
            if has_path:
                reg["directionality"] = T.path_directionality(series)
                reg.update(T._relabel(reg))
            out.update(reg)
        else:
            out["vix_close"] = c
            out["vix_change_pct"] = round((c - pc) / pc * 100, 2) if (c and pc) else None
        tapes[sym] = out
    div = None
    if "SPX" in tapes and "QQQ" in tapes:
        a, b = tapes["SPX"].get("full_pct"), tapes["QQQ"].get("full_pct")
        if a is not None and b is not None:
            div = {"spx_full_pct": a, "qqq_full_pct": b, "spread_pct": round(a - b, 2)}
    return {"date": day, "underlyings": tapes, "divergence": div,
            "any_reconstructed": False, "reconstructed_reasons": []}


def norm(d):
    d = json.loads(json.dumps(d))
    for k in ("generated", "backfilled_at", "backfill_evidence"):
        d.pop(k, None)
    return d


fails = 0
for day in DAYS:
    p = os.path.join(CAND, f"{day}_tape.CANDIDATE-gates-vixseries.json")
    live = norm(json.load(open(p)))
    mine = norm(build(day, vix_series=True))
    a = json.dumps(live, sort_keys=True, indent=2)
    b = json.dumps(mine, sort_keys=True, indent=2)
    if a == b:
        nb = {s: len(v.get("series") or []) for s, v in mine["underlyings"].items()}
        print(f"  MATCH  {day}  bars {nb}")
    else:
        fails += 1
        print(f"  DIFF   {day}")
        import difflib
        for l in list(difflib.unified_diff(a.split("\n"), b.split("\n"),
                                           "live-candidate", "from-raw", lineterm=""))[:40]:
            print("      " + l)

print()
print("normalized-away (volatile, stated not hidden): generated, backfilled_at, backfill_evidence")
print(f"{len(DAYS)-fails}/{len(DAYS)} candidate tapes reproduce EXACTLY from the raw captures")
sys.exit(1 if fails else 0)
