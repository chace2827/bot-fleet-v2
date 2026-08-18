import sys, os, json, datetime
sys.path.insert(0,'/tmp/tape-backfill')
from probe import call
# find the 5min lookback horizon for SPX by bisecting over business days back from 2026-08-18
def bars(sym, day):
    st, body, _ = call("markets/timesales", {"symbol": sym, "interval":"5min",
        "start": f"{day} 09:30", "end": f"{day} 16:00"})
    if st != 200: return st, -1
    try:
        d = json.loads(body); s = d.get("series")
        if not s: return st, 0
        b = s.get("data"); 
        return st, (len(b) if isinstance(b,list) else 1 if isinstance(b,dict) else 0)
    except Exception: return st, -2
print("5min lookback horizon probe (SPX), asof 2026-08-18:")
for back in [7, 14, 21, 30, 45, 60, 90, 120, 180, 365]:
    d = datetime.date(2026,8,18) - datetime.timedelta(days=back)
    while d.weekday() >= 5: d -= datetime.timedelta(days=1)
    st, n = bars("SPX", d.isoformat())
    print(f"  -{back:>3}d  {d}  HTTP {st}  bars={n}")
print("\nVIX timesales (5min):")
for day in ["2026-08-10","2026-08-14"]:
    st, n = bars("VIX", day); print(f"  VIX {day} HTTP {st} bars={n}")
