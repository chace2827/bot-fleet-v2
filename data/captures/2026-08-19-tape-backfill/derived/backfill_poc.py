#!/usr/bin/env python3
"""PROOF OF CONCEPT — backfill a historical tape from Tradier.

Writes CANDIDATE tapes to /tmp only. Touches nothing in the repo.
Schema identity is guaranteed by REUSING scripts/tape.py's own helpers
(tradier_history, tradier_timesales, regime, path_directionality, _relabel)
rather than reimplementing them.

Two provenance fields are ADDED beyond the tradier-day schema:
  backfilled_at      — ISO timestamp of the backfill run
  backfill_evidence  — per-underlying endpoint+params actually called

Symbol selection (--symbols):
  ledger  (default) — exactly tape.py's rule: underlyings with ON 0DTE bots
                      that traded that day, from data/trades.csv, plus VIX.
  gates             — the union the gates table can reference: SPX, QQQ, VIX.

VIX intraday (--vix-series): tape.py never requests a VIX series. Tradier
serves one. Off by default so the output stays schema-identical to a
committed tradier day; on to demonstrate availability.

Usage: python3 backfill_poc.py DATE [DATE...] [--symbols ledger|gates]
                               [--vix-series] [--out DIR]
"""
import sys, os, json, argparse, datetime

REPO = os.path.expanduser("~/bot-fleet-v2")
sys.path.insert(0, os.path.join(REPO, "scripts"))
import tape as T   # noqa: E402  — the committed generator, unmodified

GATES_SYMBOLS = ["SPX", "QQQ"]


def evidence(base, path, params):
    """Record the call WITHOUT the credential."""
    return {"endpoint": f"{base.rstrip('/')}/v1/{path}", "params": params,
            "auth": "Bearer <TRADIER_TOKEN from .env — not recorded>"}


def build_backfill(day, symbols_mode, vix_series, base, token, trades):
    if symbols_mode == "gates":
        syms = list(GATES_SYMBOLS)
    else:
        syms = T.underlyings_on(trades, day)
    tapes, ev = {}, {}
    for sym in syms + ["VIX"]:
        if sym in tapes:
            continue
        tsym = T.TRADIER_SYMBOL.get(sym, sym)
        calls = []
        start = (datetime.date.fromisoformat(day) - datetime.timedelta(days=10)).isoformat()
        try:
            rec = T.tradier_history(tsym, day, token, base)
        except T.TradierError as e:
            print(f"  {sym}: TRADIER FAILED ({e.mode}: {e.detail}) — NOT backfilled", file=sys.stderr)
            continue
        calls.append(evidence(base, "markets/history",
                              {"symbol": tsym, "interval": "daily", "start": start, "end": day}))
        o, h, l, c, pc = rec["open"], rec["high"], rec["low"], rec["close"], rec["prior_close"]
        series = []
        want_series = (sym != "VIX") or vix_series
        if want_series:
            try:
                series = T.tradier_timesales(tsym, day, token, base)
                calls.append(evidence(base, "markets/timesales",
                                      {"symbol": tsym, "interval": "5min",
                                       "start": f"{day} 09:30", "end": f"{day} 16:00"}))
            except T.TradierError as e:
                print(f"  {sym}: timesales failed ({e.mode}: {e.detail}) — daily OHLC only",
                      file=sys.stderr)
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
        ev[sym] = calls

    div = None
    if "SPX" in tapes and "QQQ" in tapes:
        a, b = tapes["SPX"].get("full_pct"), tapes["QQQ"].get("full_pct")
        if a is not None and b is not None:
            div = {"spx_full_pct": a, "qqq_full_pct": b, "spread_pct": round(a - b, 2)}

    return {"date": day, "generated": T.now_iso(),
            "any_reconstructed": False, "reconstructed_reasons": [],
            "underlyings": tapes, "divergence": div,
            "backfilled_at": datetime.datetime.now(datetime.timezone.utc)
                             .replace(microsecond=0).isoformat(),
            "backfill_evidence": {
                "tool": "backfill_poc.py (PROOF OF CONCEPT — not a repo script)",
                "provider": "Tradier v1 production",
                "symbol_selection": symbols_mode,
                "vix_series_requested": bool(vix_series),
                "calls": ev}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dates", nargs="+")
    ap.add_argument("--symbols", choices=["ledger", "gates"], default="ledger")
    ap.add_argument("--vix-series", action="store_true")
    ap.add_argument("--out", default="/tmp/tape-backfill/out")
    a = ap.parse_args()

    T.load_env()
    token = T.load_token()
    if not token:
        sys.exit("ERROR: no TRADIER_TOKEN — refusing to fabricate a tape.")
    base = os.environ.get("TRADIER_BASE", "https://api.tradier.com")
    trades = T.load_trades()
    os.makedirs(a.out, exist_ok=True)
    for day in a.dates:
        out = build_backfill(day, a.symbols, a.vix_series, base, token, trades)
        suffix = f"{a.symbols}{'-vixseries' if a.vix_series else ''}"
        p = os.path.join(a.out, f"{day}_tape.CANDIDATE-{suffix}.json")
        json.dump(out, open(p, "w"), indent=2)
        srcs = ", ".join(f"{s}:{t['source']}(bars={len(t['series'])})"
                         for s, t in out["underlyings"].items())
        print(f"wrote {p} | {srcs}")


if __name__ == "__main__":
    main()
