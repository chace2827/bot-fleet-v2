#!/usr/bin/env python3
"""tail_score.py: score backtest arms vs a control, from OA "Download CSV" position exports.

Usage: python3 scripts/tail_score.py CONTROL.csv ARM1.csv [ARM2.csv ...] [--split 2024-12-31]

Per arm, paired by expiration date ("Exp" column) against the control:
  BAD-DAY RULE (R-2026-10-06-TAIL-SCORING-RULE, gross): bad day = R <= -0.5; fixed/created;
    exact two-sided sign test; mean R and keep% of control.
  WIN-SIDE TABLE (Andy 2026-10-06): flips win->loss and loss->win; $ given up on flipped
    wins vs $ saved on control bad days; win rate; avg win / avg loss; longest losing streak.
With --split, every figure is reported for the choose window (<= split) and the holdout (> split)
(R-2026-10-06-TAIL-HOLDOUT). Read-only: prints a markdown report to stdout.
"""
import csv, sys, math, datetime

def load(p):
    out = {}
    for r in csv.DictReader(open(p, newline='')):
        risk = float(r['Risk'] or 0)
        if risk <= 0: continue
        d = datetime.datetime.strptime(r['Exp'].strip(), '%b %d, %Y').date()
        out[d] = (float(r['P/L']), risk)
    return out

def sign_p(a, b):
    n, k = a + b, min(a, b)
    if n == 0: return 1.0
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)

def streak(xs):
    best = cur = 0
    for x in xs:
        cur = cur + 1 if x < 0 else 0; best = max(best, cur)
    return best

def score(C, A, dates, name):
    rc = [C[d][0] / C[d][1] for d in dates]; ra = [A[d][0] / A[d][1] for d in dates]
    pc = [C[d][0] for d in dates]; pa = [A[d][0] for d in dates]
    fixed = sum(1 for x, y in zip(rc, ra) if x <= -0.5 < y)
    created = sum(1 for x, y in zip(rc, ra) if y <= -0.5 < x)
    mc, ma = sum(rc) / len(rc), sum(ra) / len(ra)
    keep = (ma / mc * 100) if mc > 0 else float('nan')
    passes = fixed > created and sign_p(fixed, created) < 0.05 and (ma >= 0.8 * mc if mc > 0 else ma >= mc)
    w2l = [(x, y) for x, y in zip(pc, pa) if x > 0 and y <= 0]
    l2w = [(x, y) for x, y in zip(pc, pa) if x <= 0 and y > 0]
    given_up = sum(x - y for x, y in w2l)
    saved = sum(y - x for x, y, r in zip(pc, pa, rc) if r <= -0.5)
    wins = [p for p in pa if p > 0]; losses = [p for p in pa if p <= 0]
    return dict(arm=name, n=len(dates), bad=sum(1 for r in ra if r <= -0.5), fixed=fixed, created=created,
                p=sign_p(fixed, created), meanR=ma, keep=keep, PASS=passes, pnl=sum(pa),
                w2l=len(w2l), l2w=len(l2w), given_up=given_up, saved_on_bad=saved,
                winrate=len(wins) / len(pa), avgwin=(sum(wins) / len(wins)) if wins else 0,
                avgloss=(sum(losses) / len(losses)) if losses else 0, maxlossstreak=streak(pa))

def report(C, arms, dates, title):
    print(f"\n### {title} — n={len(dates)} paired days ({dates[0]} → {dates[-1]})\n")
    print("| arm | bad | fixed/created | p | mean R | keep % | P/L | win% | avg win | avg loss | win→loss | loss→win | $ given up on flips | $ saved on bad days | max loss streak | rule |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    ctl = score(C, C, dates, 'CONTROL')
    # each arm is scored on the control's dates; arm-missing days = no trade
    # a day the arm did not trade (no fill at its strike) counts as P/L 0 / R 0: not trading is a real outcome
    rows = [ctl] + [score(C, {d: A.get(d, (0.0, C[d][1])) for d in dates}, dates, n) for n, A in arms]
    for s in rows:
        print(f"| {s['arm']} (n={s['n']}) | {s['bad']} | {s['fixed']}/{s['created']} | {s['p']:.2g} | {s['meanR']:+.4f} | {s['keep']:.0f} | "
              f"${s['pnl']:,.0f} | {s['winrate']:.1%} | ${s['avgwin']:.0f} | ${s['avgloss']:.0f} | {s['w2l']} | {s['l2w']} | "
              f"${s['given_up']:,.0f} | ${s['saved_on_bad']:,.0f} | {s['maxlossstreak']} | {'—' if s['arm']=='CONTROL' else ('PASS' if s['PASS'] else 'fail')} |")

def main():
    args = sys.argv[1:]; split = None
    if '--split' in args:
        i = args.index('--split'); split = datetime.date.fromisoformat(args[i + 1]); del args[i:i + 2]
    if len(args) < 2: sys.exit(__doc__)
    C = load(args[0]); arms = [(p.split('/')[-1], load(p)) for p in args[1:]]
    dates = sorted(C)  # control's dates; arms pair on their own overlap (see report)
    missing = {n: len(set(C) ^ set(A)) for n, A in arms}
    print(f"# Tail + win-side score — control `{args[0].split('/')[-1]}`\n\nControl days the arm did not trade (scored as 0) / arm-only days ignored: {missing}")
    if split:
        report(C, arms, [d for d in dates if d <= split], f"CHOOSE window (≤ {split})")
        report(C, arms, [d for d in dates if d > split], f"HOLDOUT (> {split})")
    else:
        report(C, arms, dates, "Full window")

if __name__ == '__main__':
    main()
