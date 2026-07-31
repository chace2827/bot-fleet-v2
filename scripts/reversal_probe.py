#!/usr/bin/env python3
"""Reversal-signature probe: does a common indicator fingerprint separate Andy's
7 marked reversals from the rest of the tape? Hypothesis-generation only (n=7)."""
import json, glob, os
import numpy as np, pandas as pd

RES = os.path.join(os.path.dirname(__file__), "..", "data", "research")

def load_day(path):
    d = json.load(open(path))
    rows = d["series"]["data"]
    df = pd.DataFrame(rows)
    df["time"] = pd.to_datetime(df["time"])
    df["day"] = df["time"].dt.strftime("%Y-%m-%d")
    return df[["time","day","open","high","low","close","volume"]].reset_index(drop=True)

def rsi(close, n=14):
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1/n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False).mean()
    rs = up/dn.replace(0,np.nan)
    return 100 - 100/(1+rs)

def features(df):
    df = df.copy()
    tp = (df.high+df.low+df.close)/3
    cv = df.volume.cumsum()
    df["vwap"] = (tp*df.volume).cumsum()/cv
    var = (df.volume*(tp-df["vwap"])**2).cumsum()/cv
    sig = np.sqrt(var)
    df["dist_sigma"] = (df.close-df["vwap"])/sig          # extension in session-VWAP sigmas
    ma = df.close.rolling(20, min_periods=5).mean()
    sd = df.close.rolling(20, min_periods=5).std()
    df["pctB"] = (df.close-(ma-2*sd))/((ma+2*sd)-(ma-2*sd))
    df["rsi"] = rsi(df.close)
    ema12 = df.close.ewm(span=12, adjust=False).mean()
    ema26 = df.close.ewm(span=26, adjust=False).mean()
    macd = ema12-ema26
    df["macd_hist"] = macd - macd.ewm(span=9, adjust=False).mean()
    tr = pd.concat([df.high-df.low,(df.high-df.close.shift()).abs(),(df.low-df.close.shift()).abs()],axis=1).max(axis=1)
    df["atr"] = tr.rolling(14, min_periods=5).mean()
    df["range_atr"] = (df.high-df.low)/df["atr"]
    df["rvol"] = df.volume/df.volume.rolling(20, min_periods=5).median()
    dirn = np.sign(df.close.diff()).fillna(0)
    run=[]; c=0; prev=0
    for x in dirn:
        c = c+1 if x==prev and x!=0 else (1 if x!=0 else 0); prev=x; run.append(c*x)
    df["run"] = run
    df["ret3"] = df.close.pct_change(3)*100
    return df

MARKS = [
    ("2026-06-30","11:00","LOW"),
    ("2026-07-01","11:00","HIGH"),
    ("2026-07-02","10:00","HIGH"),
    ("2026-07-06","09:45","LOW"),
    ("2026-07-06","13:00","HIGH"),
    ("2026-07-07","10:30","LOW"),
    ("2026-07-07","14:00","HIGH"),
]

frames={}
for p in sorted(glob.glob(os.path.join(RES,"qqq_5m_*.json"))):
    try:
        raw = load_day(p)
    except Exception:
        continue
    if len(raw) < 30:   # skip holidays/empty sessions
        continue
    df = features(raw)
    frames[df.day.iloc[0]] = df

def snap(day, hhmm, typ, win=8):
    df = frames[day]
    t = pd.to_datetime(f"{day} {hhmm}:00")
    i = (df.time-t).abs().idxmin()
    lo,hi = max(0,i-win), min(len(df)-1,i+win)
    seg = df.iloc[lo:hi+1]
    j = seg.close.idxmax() if typ=="HIGH" else seg.close.idxmin()
    return j

rows=[]; pct_rows=[]
for day,hhmm,typ in MARKS:
    j = snap(day,hhmm,typ)
    df = frames[day]; r = df.loc[j]
    s = 1 if typ=="HIGH" else -1
    oriented = {
        "dist_sigma":  s*r.dist_sigma,
        "pctB_dev":    s*(r.pctB-0.5),
        "rsi_dev":     s*(r.rsi-50),
        "run_dir":     s*r.run,
        "ret3_dir":    s*r.ret3,
        "macd_hist":   s*r.macd_hist,
    }
    undirected = {"range_atr": r.range_atr, "rvol": r.rvol}
    rows.append(dict(day=day, time=str(r.time)[11:16], type=typ, close=round(r.close,2),
                     **{k:round(v,2) for k,v in oriented.items()},
                     **{k:round(v,2) for k,v in undirected.items()}))
    prow={"day":day,"time":str(r.time)[11:16],"type":typ}
    for k,v in oriented.items():
        col = df.dist_sigma*s if k=="dist_sigma" else \
              (df.pctB-0.5)*s if k=="pctB_dev" else \
              (df.rsi-50)*s if k=="rsi_dev" else \
              df.run*s if k=="run_dir" else \
              df.ret3*s if k=="ret3_dir" else df.macd_hist*s
        prow[k]=round((col<v).mean()*100)
    for k in undirected:
        col=df[k]; prow[k]=round((col<undirected[k]).mean()*100)
    pct_rows.append(prow)

vals=pd.DataFrame(rows); pcts=pd.DataFrame(pct_rows)
pd.set_option("display.width",200,"display.max_columns",30)
print("=== RAW ORIENTED FEATURE VALUES AT THE 7 MARKS ===")
print("(oriented: positive = in the direction of the exhausted move; undirected: range_atr, rvol)")
print(vals.to_string(index=False))
print("\n=== PERCENTILE RANK WITHIN EACH DAY (100 = most extreme that day) ===")
print(pcts.to_string(index=False))
feat_cols=[c for c in pcts.columns if c not in ("day","time","type")]
print("\n=== SEPARATION SUMMARY: median percentile across the 7 marks, & #/7 in the tail ===")
summ=pd.DataFrame({
    "median_pctile":[int(pcts[c].median()) for c in feat_cols],
    "min_pctile":[int(pcts[c].min()) for c in feat_cols],
    "n_above_80":[int((pcts[c]>=80).sum()) for c in feat_cols],
    "n_above_90":[int((pcts[c]>=90).sum()) for c in feat_cols],
}, index=feat_cols).sort_values("median_pctile",ascending=False)
print(summ.to_string())
vals.to_csv(os.path.join(RES,"reversal_marks_values.csv"),index=False)
pcts.to_csv(os.path.join(RES,"reversal_marks_percentiles.csv"),index=False)
