#!/usr/bin/env python3
"""Read-only Tradier probe. Prints endpoint, params, HTTP status and a TRUNCATED
body. NEVER prints the token."""
import sys, os, json, urllib.request, urllib.parse, urllib.error
sys.path.insert(0, os.path.expanduser("~/bot-fleet-v2/scripts"))
import tape as T

T.load_env()
TOK = T.load_token()
BASE = os.environ.get("TRADIER_BASE", "https://api.tradier.com").rstrip("/")
assert TOK, "no token"

def call(path, params):
    url = f"{BASE}/v1/{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={
        "Authorization": "Bearer <REDACTED>".replace("<REDACTED>", TOK),
        "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400], dict(e.headers)
    except Exception as e:
        return None, f"NETERR {type(e).__name__}: {e}", {}

def show(tag, path, params, trunc=600):
    st, body, hdrs = call(path, params)
    print(f"\n### {tag}\nGET {BASE}/v1/{path}?{urllib.parse.urlencode(params)}\nHTTP {st}")
    rl = {k: v for k, v in hdrs.items() if "ratelimit" in k.lower()}
    if rl: print("ratelimit hdrs:", rl)
    print("BODY[:%d]: %s" % (trunc, body[:trunc]))
    return st, body

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "hist"):
        print("=" * 70); print("A. markets/history — daily OHLC")
        for sym in ["SPX", "QQQ", "VIX", "$VIX.X", "^VIX", "VIX.X", "VIXY", "SPY"]:
            show(f"history {sym}", "markets/history",
                 {"symbol": sym, "interval": "daily", "start": "2026-08-05", "end": "2026-08-11"})
    if which in ("all", "ts"):
        print("\n" + "=" * 70); print("B. markets/timesales — 5min intraday lookback")
        for sym in ["SPX", "QQQ"]:
            for day in ["2026-08-10", "2026-08-11", "2026-08-12", "2026-08-14", "2026-08-17"]:
                st, body = show(f"timesales {sym} {day}", "markets/timesales",
                     {"symbol": sym, "interval": "5min",
                      "start": f"{day} 09:30", "end": f"{day} 16:00"}, trunc=260)
                try:
                    d = json.loads(body); s = d.get("series")
                    bars = (s or {}).get("data") if isinstance(s, dict) else None
                    n = len(bars) if isinstance(bars, list) else (1 if isinstance(bars, dict) else 0)
                    print(f"  -> BAR COUNT: {n}")
                except Exception: pass
    if which in ("all", "ts_vix"):
        print("\n" + "=" * 70); print("C. markets/timesales VIX (expected: none)")
        for day in ["2026-08-10", "2026-08-14"]:
            show(f"timesales VIX {day}", "markets/timesales",
                 {"symbol": "VIX", "interval": "5min", "start": f"{day} 09:30", "end": f"{day} 16:00"}, trunc=260)
