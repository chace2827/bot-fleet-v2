#!/usr/bin/env python3
"""Base-rate / forward test for the reversal fingerprint.
For every bar: if price is extended from session VWAP and a candle-run is aligned
with the extension, does price REVERT over the next N bars more than baseline?
This is the test that matters (not the n=7 look-back). Still tiny sample (5 days)."""
import json, glob, os
import numpy as np, pandas as pd
from reversal_probe import load_day, features, RES

FWD = 6  # forward horizon in bars (30 min)

allbars=[]
for p in sorted(glob.glob(os.path.join(RES,"qqq_5m_*.json"))):
    try:
        raw = load_day(p)
    except Exception:
        continue
    if len(raw) < 30:   # skip holidays/empty sessions
        continue
    df = features(raw)
    df["fwd_ret"] = (df.close.shift(-FWD)/df.close - 1)*100   # forward % move
    # reversion return = move against the current extension direction
    df["rev_ret"] = -np.sign(df.dist_sigma)*df.fwd_ret
    allbars.append(df)
A = pd.concat(allbars, ignore_index=True).dropna(subset=["fwd_ret","dist_sigma","run"])

base_mean = A.rev_ret.mean(); base_hit = (A.rev_ret>0).mean()
print(f"BASELINE (all {len(A)} bars): mean reversion move over next {FWD} bars = {base_mean:+.3f}%  |  hit rate = {base_hit*100:.0f}%\n")

print(f"{'sigma>=':>7} {'run>=':>6} {'n':>4} {'mean_rev%':>10} {'hit%':>6} {'lift_vs_base%':>14}")
for T in [1.0,1.25,1.5,1.75,2.0]:
    for R in [0,2,3,4]:
        aligned = np.sign(A.run)==np.sign(A.dist_sigma)
        m = (A.dist_sigma.abs()>=T) & (A.run.abs()>=R) & (aligned if R>0 else True)
        sub=A[m]
        if len(sub)<5:
            print(f"{T:>7} {R:>6} {len(sub):>4} {'--':>10} {'--':>6} {'--':>14}")
            continue
        print(f"{T:>7} {R:>6} {len(sub):>4} {sub.rev_ret.mean():>+10.3f} {(sub.rev_ret>0).mean()*100:>6.0f} {sub.rev_ret.mean()-base_mean:>+14.3f}")

# best cell detail
aligned = np.sign(A.run)==np.sign(A.dist_sigma)
best = A[(A.dist_sigma.abs()>=1.5)&(A.run.abs()>=3)&aligned]
print(f"\nSIGNAL CELL (|sigma|>=1.5 & aligned run>=3): n={len(best)}")
print(f"  mean reversion {best.rev_ret.mean():+.3f}%  vs baseline {base_mean:+.3f}%  |  hit {(best.rev_ret>0).mean()*100:.0f}% vs {base_hit*100:.0f}%")
print(f"  win/loss of reverting moves: avg win {best[best.rev_ret>0].rev_ret.mean():+.3f}% / avg loss {best[best.rev_ret<0].rev_ret.mean():+.3f}%")
