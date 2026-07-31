> **⚠️ Carried for machinery, not verdicts (banner added 2026-07-30, Phase 1).**
> The tiers and sample gates in this ledger are **adopted**. The parent audit's kill-IC and
> third-party-switch verdicts are **overruled** — see `docs/independent-audit-2026-07-27.md`.
> Andy has flagged wanting to redesign the scoring; `docs/evidence-standards.md` is written to be revised.

# PRE-COMMITMENT LEDGER — LOCKED 2026-07-27, BEFORE ANY RESULTS WERE READ

Written before opening any P&L, backtest, or status file. Anchored to the project's own
stated evidence standards (oa-mirror-reference.md §3, as summarized in the project
instructions): min ~100 trades / ~6 months, expectancy sanity check, instance-profitability
over win rate, compare in R not raw P/L, out-of-sample survival, count the scanners.

## A. EVIDENCE TIERS (a system is scored at its HIGHEST-QUALITY tier, never averaged up)
- T1 LIVE  — real money, real fills, broker-confirmed.
- T2 PAPER — automated paper execution with realistic fills, forward in time, no lookahead.
- T3 OOS BACKTEST — parameters fixed BEFORE the test window; window untouched during design.
- T4 IS BACKTEST — any backtest whose window overlaps the period used to select parameters.
- T5 IDEA — spec, roadmap, doc, or Reddit/forum-sourced concept. Scores zero.
A T4 result may never be cited as support for a T1/T2 claim. A backtest that has been
re-run after seeing its own output is T4 by definition.

## B. SAMPLE-ADEQUACY GATE (binary, per system)
PASS requires ALL of:
- B1. n >= 100 closed trades at T1 or T2. (T3 counts for a separate, weaker gate only.)
- B2. Span >= 6 calendar months of forward/live time.
- B3. Span includes >= 1 distinct volatility regime change (a VIX move of >= 10 points
      peak-to-trough, or both a sub-15 and an above-25 VIX period).
Anything failing B1 or B2 is stamped THIN and cannot contribute to the edge score.
For 0DTE strategies specifically, 100 trades ~ 5 trading months at 1/day. This is the
project's own floor and I am adopting it unchanged.

## C. EXPECTANCY GATE (the sanity check)
- C1. Expectancy per trade, in R, computed as (Win% x AvgWin_R) - (Loss% x AvgLoss_R),
      must be > 0 AFTER costs. Costs = commissions + exchange fees + a modeled slippage
      of at least 1 tick per leg on entry and exit (4-leg IC = 8 ticks round trip).
- C2. Expectancy must remain > 0 when the single largest winning trade is removed.
- C3. Expectancy must remain > 0 when the worst 5% of days are given a 1.5x loss
      multiplier (fill-degradation stress; 0DTE tails fill worse than modeled).
- C4. If a system's edge exists only in raw P/L but not in R, it FAILS. Different position
      sizes across bots make raw P/L uninterpretable.
FAIL of C1 = kill. FAIL of C2 or C3 = the edge is tail-dependent, not demonstrated.

## D. RISK-QUALITY GATE
- D1. Max realized drawdown, in R, must be known and stated. Unknown = FAIL.
- D2. Return/max-DD >= 1.0 over the measured window at T1/T2. Below 1.0 = not worth
      the operational risk of an automated 0DTE book for a retail account.
- D3. Worst single day must be < 25% of the measured window's total profit. If one bad
      day erases a quarter of everything earned, the tail is not controlled.
- D4. Undefined-risk or naked exposure at any point = automatic kill regardless of P&L.

## E. MECHANISM GATE (non-negotiable)
- E1. Each system must state, in one sentence, WHY it makes money — a named economic
      source (variance risk premium, dealer gamma/pinning, overnight drift, term-structure
      carry, a validated regime conditional). "It backtested well" is not a mechanism.
- E2. The claimed mechanism must be consistent with the observed P&L shape. A VRP seller
      should show many small wins and rare large losses; if the equity curve doesn't look
      like the mechanism, one of the two is wrong.
- E3. Pattern-only results with no E1 answer are classified CURVE-FIT by default. Burden
      is on the system to rebut, not on me to disprove.

## F. OVERFITTING / SCANNER-COUNT GATE
- F1. Count the strategy variants tested (bots, backtest runs, parameter sets). Apply a
      multiple-comparisons haircut: a "winner" selected from N variants needs roughly
      t > sqrt(2 ln N) to mean anything. At N=20 bots that is t ~ 2.45; at N=100 runs,
      t ~ 3.03. A single Sharpe-1 result out of 20 tried is noise.
- F2. Parameter-change frequency: if a system's parameters have been changed more than
      once per 30 trading days on average, it is stamped RE-TUNED and its live record is
      treated as restarted at the date of the last change. Sample count resets with it.
- F3. If the fleet's headline number depends on which subset of bots is included, and that
      subset was chosen after seeing performance, the number is discarded entirely.
- F4. Any strategy whose live results are materially worse than its backtest (>50% of
      backtested expectancy lost) is evidence the backtest process is broken, and taints
      every other backtest produced by the same process.

## G. LIVE-VS-BACKTEST TRACKING GATE
- G1. For any system running live, live expectancy in R must be >= 50% of backtested
      expectancy in R over the same period. Below that = the backtester is not
      decision-grade and no backtest from it may be cited as evidence anywhere.

## H. PORTFOLIO-LEVEL GATE
- H1. Correlation: if all four pillars are net-short-vol / net-short-gamma, the fleet is
      ONE bet, not four. It is scored as one system with one sample, not four samples.
- H2. Diversification claims require demonstrated negative or near-zero return correlation
      between pillars on the same days. Assertion is not demonstration.
- H3. The fleet must survive its own worst historical stress day at current size without
      breaching a stated max loss. If no such stress test exists, FAIL.

## I. CONFIDENCE SCORE RUBRIC (0-100 = confidence a real tradeable edge is DEMONSTRATED)
- 0-15   No system passes B. Evidence is backtest/idea only. Default state of any project
         that has not yet accumulated 100 live/paper trades.
- 16-30  At least one system passes B, but fails C, E, or F.
- 31-50  One system passes B + C + E, but fails F (scanner count) or G (tracking), or the
         sample sits at the bare minimum.
- 51-70  One or more systems pass B + C + D + E + F + G. Edge is probably real but small
         or fragile. Advance to live at reduced size.
- 71-85  Multiple independent-mechanism systems pass all gates across >= 12 months and a
         regime change.
- 86-100 Institutional-grade: multi-year, multi-regime, out-of-sample, cost-verified.
         No retail 0DTE project should expect to reach this. I do not expect to award it.

## J. AUTOMATIC KILLS (any one of these ends the system, no discussion)
- J1. No system has >= 100 forward trades AND the project is asking to increase size.
- J2. Any undefined-risk position, or any position sized such that a 3x-expected loss day
      exceeds 10% of account equity.
- J3. Live results materially diverge from backtest and the response was to re-fit the
      backtest rather than stand down.
- J4. Evidence of manual override of automated rules for P&L reasons (i.e., discretionary
      intervention on a system sold as systematic).
- J5. Position sizing increased following a losing period (loss-chasing) — this is a kill
      on human-risk grounds independent of the edge.

## K. WHAT IS EXPLICITLY WORTH ZERO
Hours logged. Years elapsed. Lines of code. Number of bots. Documentation quality.
Infrastructure sophistication (VPS, recorders, backup automation, dashboards). Roadmaps.
Reddit consensus. The owner's conviction. My own desire to give an encouraging answer.

THESE CRITERIA ARE LOCKED. I WILL NOT LOOSEN THEM AFTER SEEING THE RESULTS.
If I find a threshold was wrong, I may only make it STRICTER, and I must flag that I did.
