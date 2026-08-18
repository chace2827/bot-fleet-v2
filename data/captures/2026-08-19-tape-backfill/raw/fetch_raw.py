#!/usr/bin/env python3
"""W0 raw-capture fetcher — saves Tradier v1 responses VERBATIM.

Authorized by Andy 2026-08-19 under R-2026-08-19-TAPE-BACKFILL-AND-VIX-SERIES:
the same call class daily.sh makes daily, explicitly extended to the history
endpoints for this backfill.

Writes one file per endpoint call, named {SYMBOL}_{DATE}_{interval}.json.
The response body is written EXACTLY as received — no parsing, no re-encoding,
no pretty-printing. The credential is never written to disk or stdout.
"""
import os, sys, json, urllib.parse, urllib.request, datetime, hashlib

OUT = sys.argv[1]
DAYS = ["2026-08-10", "2026-08-11", "2026-08-12", "2026-08-13", "2026-08-14", "2026-08-17"]
SYMS = ["SPX", "QQQ", "VIX"]

env = {}
for line in open(os.path.expanduser("~/bot-fleet-v2/.env")):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
TOKEN = env.get("TRADIER_TOKEN")
BASE = env.get("TRADIER_BASE", "https://api.tradier.com")
if not TOKEN:
    sys.exit("TRADIER_TOKEN not found in .env")

os.makedirs(OUT, exist_ok=True)
manifest = []


def get_raw(path, params):
    url = f"{BASE.rstrip('/')}/v1/{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOKEN}", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read(), r.status


def save(name, path, params):
    try:
        body, status = get_raw(path, params)
    except Exception as e:
        print(f"  FAIL {name}: {type(e).__name__}: {e}")
        manifest.append({"file": name, "endpoint": f"{BASE}/v1/{path}", "params": params,
                         "status": "FAILED", "error": f"{type(e).__name__}: {e}"})
        return
    p = os.path.join(OUT, name)
    with open(p, "wb") as fh:
        fh.write(body)                      # VERBATIM bytes, exactly as received
    sha = hashlib.sha256(body).hexdigest()
    manifest.append({"file": name, "endpoint": f"{BASE}/v1/{path}", "params": params,
                     "http_status": status, "bytes": len(body), "sha256": sha,
                     "auth": "Bearer <TRADIER_TOKEN from .env — not recorded>"})
    print(f"  ok {name}  {len(body):>7} bytes  {sha[:16]}…")


for day in DAYS:
    print(day)
    start = (datetime.date.fromisoformat(day) - datetime.timedelta(days=10)).isoformat()
    for sym in SYMS:
        save(f"{sym}_{day}_daily.json", "markets/history",
             {"symbol": sym, "interval": "daily", "start": start, "end": day})
        save(f"{sym}_{day}_5min.json", "markets/timesales",
             {"symbol": sym, "interval": "5min",
              "start": f"{day} 09:30", "end": f"{day} 16:00"})

man = {
    "captured_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
    "provider": "Tradier v1 production",
    "authorization": "R-2026-08-19-TAPE-BACKFILL-AND-VIX-SERIES (Andy, 2026-08-19)",
    "note": "Raw response bodies, written verbatim. Credential never recorded.",
    "calls": manifest,
}
with open(os.path.join(OUT, "MANIFEST.json"), "w") as fh:
    json.dump(man, fh, indent=2, sort_keys=True)
    fh.write("\n")
ok = sum(1 for c in manifest if c.get("sha256"))
print(f"\n{ok}/{len(manifest)} calls captured -> {OUT}")
