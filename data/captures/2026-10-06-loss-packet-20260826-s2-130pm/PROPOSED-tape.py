#!/usr/bin/env python3
"""PROPOSED — one-command §4 tape for a loss packet.

    python3 PROPOSED-tape.py --symbol SPX --date 2026-08-26 \
        --strikes 7655:put 7690:call --repo /path/to/bot-fleet-v2 \
        --window 13:00-16:00 --out 04-tape.csv

Copies nothing: run it with --repo pointing at the repo (scripts/ + .env live
there); it imports scripts/tape.py in place and reads .env for TRADIER_TOKEN.
Writes <window> bars (t,p,h,l) to --out and prints the per-strike milestone
table. Requests 1min first, falls back to 5min, and prints WHICH interval ran.
"""
import argparse, csv, json, os, sys

def load_env(repo):
    env = os.path.join(repo, '.env')
    if os.path.exists(env):
        for line in open(env):
            if '=' in line and not line.lstrip().startswith('#'):
                k, v = line.strip().split('=', 1)
                os.environ.setdefault(k, v)

def parse_strike(s):
    # '7690:call' or '7655:put' or bare '7690' (side inferred later from price)
    k, _, side = s.partition(':')
    return float(k), (side or 'auto').lower()

def milestones(win, strike, side):
    """win = [{t,p,h,l}]. Approach direction: put touched from above (low),
    call from below (high). 'auto' reports BOTH directions' extremes."""
    out = {'strike': strike, 'side': side}
    def first(pred, key):
        b = next((b for b in win if b[key] is not None and pred(b[key])), None)
        return (b['t'], b['h'], b['l'], b['p']) if b else None
    if side in ('put', 'auto'):
        out['put'] = {
            'within_20': first(lambda v: v <= strike + 20, 'l'),
            'within_10': first(lambda v: v <= strike + 10, 'l'),
            'at_or_through': first(lambda v: v <= strike, 'l'),
            'extreme_low': min((b['l'] for b in win if b['l'] is not None), default=None),
        }
        if out['put']['extreme_low'] is not None:
            out['put']['beyond'] = round(strike - out['put']['extreme_low'], 2)
    if side in ('call', 'auto'):
        out['call'] = {
            'within_20': first(lambda v: v >= strike - 20, 'h'),
            'within_10': first(lambda v: v >= strike - 10, 'h'),
            'at_or_through': first(lambda v: v >= strike, 'h'),
            'extreme_high': max((b['h'] for b in win if b['h'] is not None), default=None),
        }
        if out['call']['extreme_high'] is not None:
            out['call']['beyond'] = round(out['call']['extreme_high'] - strike, 2)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--symbol', required=True)
    ap.add_argument('--date', required=True)          # YYYY-MM-DD
    ap.add_argument('--strikes', nargs='+', required=True)
    ap.add_argument('--repo', required=True)
    ap.add_argument('--window', default='13:00-16:00')
    ap.add_argument('--out', default='04-tape.csv')
    a = ap.parse_args()

    load_env(a.repo)
    sys.path.insert(0, os.path.join(a.repo, 'scripts'))
    import tape
    tok = os.environ.get('TRADIER_TOKEN')
    base = os.environ.get('TRADIER_BASE', 'https://api.tradier.com')
    if not tok:
        sys.exit('no TRADIER_TOKEN (repo .env)')

    used, bars, err = None, None, None
    for iv in ('1min', '5min'):
        try:
            bars = tape.tradier_timesales(a.symbol, a.date, tok, base, interval=iv)
            used = iv
            break
        except Exception as e:
            err = e
    if bars is None:
        sys.exit(f'timesales failed (1min+5min): {err}')

    lo, hi = a.window.split('-')
    win = [b for b in bars if lo <= b['t'] <= hi]
    with open(a.out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['t', 'p', 'h', 'l'])
        for b in win:
            w.writerow([b['t'], b['p'], b['h'], b['l']])

    print(f'interval used: {used}')
    print(f'bars written : {len(win)} ({win[0]["t"]} -> {win[-1]["t"]}) -> {a.out}')
    print(f'16:00 close  : {win[-1]}')
    for s in a.strikes:
        k, side = parse_strike(s)
        print(json.dumps(milestones(win, k, side)))

if __name__ == '__main__':
    main()
