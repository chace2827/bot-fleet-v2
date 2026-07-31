> **⚠️ PARTIALLY OVERRULED — read this first (banner added 2026-07-30, Phase 1).**
> This audit is carried for its **evidence machinery only**: the T1–T5 tiers and the sample gates
> (n≥100 / 6 months / regime change). That machinery is adopted.
> Its **verdicts are overruled**, specifically:
> • "kill IC" — overruled; the IC pillar continues at pilot scale under pre-registration.
> • "switch to a third-party platform" — overruled.
> • Any **AUTOMATIC KILL / add-a-stop verdict on the QQQ-Fortress pair** — overruled. That pair's June
>   losses were a dead-exit execution artifact, not a strategy property; see
>   `docs/qqq-fortress-loss-forensic-2026-07-27.md`. The decision is restore & verify, then re-ask.
> • The "94% vs 36% band" argument was computed on the contaminated full ledger (317 pre-fix champion
>   legs opened at 9:xx against an 11:00 config, plus QQQ arms now known mis-built). Not decision-grade.
> Some figures in this file do not reconcile against `data/trades.csv` — see `docs/current-state.md`
> §Known reconciliation gaps. **The CSVs win.**

# INDEPENDENT AUDIT — "BOT FLEET" ALGORITHMIC TRADING PROJECT

**Prepared for:** the family (parents and life partner of the project owner)
**Prepared by:** an independent quantitative trading auditor with no stake in the outcome
**Date:** 27 July 2026
**Evidence base:** the full `bot-fleet` project folder as of last modification 8 July 2026 —
`data/trades.csv` (1,380 leg records / 934 positions), `STATUS.md`, `docs/current-state.md`,
`docs/directional-oa-build-sheet.md`, `docs/session-log.md`, `docs/backlog.md`,
`data/scalp_journal.md`, `investor-profile.md`, and 50+ supporting documents.
All figures below were recomputed from the raw ledger, not taken from the project's own summaries.
Every material number was independently re-verified by a second adversarial pass.

---

## 1. PRE-COMMITMENT LEDGER

*These criteria were written and saved before any P&L, backtest, or status file was opened.
They are anchored to the project's own published evidence standards, not to an outside standard
I invented. I have not loosened a single one. Where I revised, I revised stricter — flagged below.*

### A. Evidence tiers
A system is scored at its highest-quality tier and never allowed to borrow credibility upward.

| Tier | Meaning |
|---|---|
| **T1 LIVE** | Real money, real fills, broker-confirmed |
| **T2 PAPER** | Automated paper execution, forward in time, no lookahead |
| **T3 OOS BACKTEST** | Parameters fixed *before* the test window; window untouched during design |
| **T4 IS BACKTEST** | Any backtest whose window overlaps the data used to select parameters |
| **T5 IDEA** | Spec, roadmap, doc, forum concept. Scores zero. |

A backtest re-run after seeing its own output is T4 by definition.

### B. Sample-adequacy gate (binary, per system)
Pass requires **all** of:

- **B1.** n ≥ 100 closed positions at T1 or T2
- **B2.** Span ≥ 6 calendar months of forward/live time
- **B3.** Span includes ≥ 1 distinct volatility regime change

Failing B1 or B2 stamps the system **THIN**; it cannot contribute to the edge score.
*(This is the project's own floor, adopted unchanged.)*

### C. Expectancy gate
- **C1.** Expectancy per position in R must be **> 0 after costs** (commissions + ≥1 tick per leg slippage, entry and exit)
- **C2.** Must stay > 0 with the single largest winner removed
- **C3.** Must stay > 0 with the worst 5% of days given a 1.5× loss multiplier
- **C4.** Edge visible only in raw P/L but not in R = **FAIL**

### D. Risk-quality gate
- **D1.** Max realized drawdown in R must be known and stated. Unknown = FAIL
- **D2.** Return ÷ max-DD ≥ 1.0 over the measured window
- **D3.** Worst single day < 25% of the window's total profit
- **D4.** **Any undefined-risk or naked exposure = automatic kill regardless of P&L**

### E. Mechanism gate (non-negotiable)
- **E1.** One sentence naming *why* it makes money — a real economic source. "It backtested well" is not a mechanism
- **E2.** The claimed mechanism must match the observed P&L shape
- **E3.** Pattern-only results with no E1 answer are classified **CURVE-FIT by default**; burden of rebuttal is on the system

### F. Overfitting / scanner-count gate
- **F1.** Count the variants tested. A winner selected from N variants requires roughly **|t| > √(2 ln N)**.
  At N=20 → 2.45; N=53 → 2.82; N=150 → 3.17; N=1,200 → 3.77
- **F2.** Parameters changed more than once per 30 trading days → stamped **RE-TUNED**; the live record restarts at the last change
- **F3.** If the headline number depends on a subset chosen after seeing performance, the number is **discarded**
- **F4.** Live materially worse than backtest (>50% of expectancy lost) taints **every** backtest from that process

### G. Live-vs-backtest tracking gate
- **G1.** Live expectancy in R must be ≥ 50% of backtested expectancy in R. Below that, the backtester is not decision-grade and **no backtest from it may be cited as evidence anywhere**

### H. Portfolio gate
- **H1.** If all pillars are net-short-vol, the fleet is **one bet**, scored as one system with one sample
- **H2.** Diversification claims require demonstrated low/negative same-day return correlation
- **H3.** Must survive its own worst historical stress day at current size within a stated max loss

### I. Confidence-score rubric (0–100 = confidence a real tradeable edge is *demonstrated*)

| Band | Meaning |
|---|---|
| **0–15** | No system passes B. Backtest/idea only. Default state of any project without 100 forward trades |
| **16–30** | A system passes B but fails C, E, or F |
| **31–50** | A system passes B+C+E but fails F or G, or sits at the bare minimum sample |
| **51–70** | One or more systems pass every gate. Edge probably real but small or fragile |
| **71–85** | Multiple independent-mechanism systems pass all gates over ≥12 months and a regime change |
| **86–100** | Institutional-grade. No retail 0DTE project should expect this; I do not expect to award it |

### J. Automatic kills
- **J1.** No system has ≥100 forward trades **and** the project is asking to increase size
- **J2.** Any undefined-risk position, or sizing where a 3× expected loss day exceeds 10% of equity
- **J3.** Live diverges from backtest and the response was to re-fit the backtest rather than stand down
- **J4.** Manual override of automated rules for P&L reasons
- **J5.** Position sizing increased following a losing period (loss-chasing) — kills on human-risk grounds independently of the edge

### K. Explicitly worth zero
Hours logged. Years elapsed. Lines of code. Number of bots. Documentation quality. Infrastructure
(VPS, recorders, dashboards, backup automation). Roadmaps. Reddit consensus. The owner's conviction.
My own desire to give an encouraging answer.

> **THESE CRITERIA ARE LOCKED.** I did not loosen any of them after seeing the results.
> **One stricter revision, flagged as required:** the ledger records iron condors as two separate legs.
> The project's own reporting pipeline sums the risk of both sides, which understates return-on-risk
> because a condor can only lose one side. I recomputed everything using **risk = the larger side**,
> which is the correct and *harsher* denominator. This makes several numbers below look worse than
> the project's own `STATUS.md` shows. That is a correction, not a moved goalpost.

---

## 2. EVIDENCE INVENTORY

### 2.1 The whole ledger, in one line

**934 positions · 32 bots · 5 March 2026 → 2 July 2026 · 119 calendar days · −$83,130 · −20.24R**

Every dollar of it is **paper**. There is no live-capital bot record in this project. That is the
project's own honest headline and it is accurate.

The entire dataset is **3.9 months long**. The project's own evidence floor is 6 months. It is
therefore *structurally impossible* for any bot in this ledger to satisfy the project's own
sample-adequacy standard — not as a matter of judgment, but as a matter of arithmetic.

### 2.2 Evidence table — every system with a real record

| System | Pillar | Tier | N pos | Span | Days | P/L | WR | Exp(R) | t | max DD (R) | Flags |
|---|---|---|--:|---|--:|--:|--:|--:|--:|--:|---|
| **IC-SPX-FastPT25-S2** *(champion)* | IC | T2 paper | **221** | 4/09→7/02 | 84 | **−$11,155** | 43.0% | **−0.0105** | −1.25 | −3.06 | THIN (span 2.8mo); negative |
| QQQ-IC-0DTE-HedgeTest | IC | T2 | 55 | 3/16→5/22 | 66 | −$11,196 | 67% | −0.0414 | −1.74 | −2.62 | THIN; contaminated |
| QQQ-IC-0DTE-HedgeD-Cond. | IC | T2 | 51 | 3/19→5/22 | 64 | −$15,376 | 69% | −0.0615 | −2.06 | −3.50 | THIN; contaminated |
| QQQ-IC-0DTE-HedgeA-S1 | IC | T2 | 51 | 3/19→5/22 | 64 | −$12,501 | 67% | −0.0499 | −1.94 | −2.91 | THIN; contaminated |
| QQQ-IC-0DTE-HedgeB-S2 | IC | T2 | 51 | 3/19→5/22 | 64 | −$3,130 | 33% | −0.0125 | −1.87 | −0.88 | THIN; contaminated |
| QQQ-IC-0DTE-HedgeC-S3 | IC | T2 | 50 | 3/19→5/22 | 64 | −$2,702 | 34% | −0.0111 | −1.15 | −0.80 | THIN; contaminated |
| QQQ-IC-0DTE-Raw-HoldToExp | IC | T2 | 47 | 3/24→5/22 | 58 | −$303 | 70% | −0.0354 | −0.85 | −3.29 | THIN |
| QQQ-IC-0DTE-Baseline | IC | T2 | 43 | 3/05→5/22 | 77 | **−$31,580** | 70% | −0.0737 | −1.37 | −3.41 | THIN; largest single loser |
| **3DTE $140-$350** | Mirror | T2 | 43 | 4/20→6/29 | 69 | +$610 | 95% | +0.0147 | +0.60 | −1.00 | THIN (n & span) |
| IC-SPX-FastPT25-S2-130PM | IC | T2 | 42 | 6/22→7/02 | **10** | +$105 | 43% | +0.0006 | +0.14 | −0.15 | THIN (10 days) |
| **Nigiri-Paper-v1** | Mirror | T2 | 37 | 4/20→7/01 | 72 | +$1,810 | 95% | +0.0100 | +9.36 | 0.00 | THIN (n & span) |
| QQQ-IC-…-Wide2-1230PM | IC | T2 | 27 | 3/24→5/22 | 59 | +$78 | 85% | +0.0157 | +0.98 | −0.37 | THIN |
| QQQ-IC-0DTE-Fortress | IC | T2 | 27 | 3/17→6/26 | 101 | −$1,834 | 85% | −0.0146 | −0.28 | −0.81 | THIN; **naked downside** |
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | T2 | 24 | 3/24→6/26 | 93 | −$2,049 | 79% | −0.0182 | −0.31 | −0.81 | THIN; **naked downside** |
| Opening Range Breakout 60m | Mirror | T2 | 19 | 4/20→5/21 | 31 | −$2,602 | 68% | −0.1107 | −1.28 | −1.94 | Killed — correctly |
| IC-SPX-Fortress-Unstopped | IC | T2 | 18 | 5/15→7/02 | 47 | +$2,350 | 44% | +0.0271 | +2.43 | −0.05 | THIN |
| IC-SPX-Fortress-Defang | IC | T2 | 18 | 5/15→7/02 | 47 | +$600 | 39% | +0.0071 | +0.83 | −0.11 | THIN |
| Weekly-IB-SPY-Paper-v1 | Mirror | T2 | 18 | 5/11→6/10 | 30 | −$1,246 | 50% | −0.0770 | −0.98 | −3.24 | THIN; kill candidate |
| Trendy-Paper-v1 | Mirror | T2 | 14 | 4/20→6/30 | 71 | −$181 | 79% | −0.0439 | −0.56 | −1.23 | THIN |
| 60min-ORB-10W-Paper-v1 | Mirror | T2 | 12 | 5/13→6/30 | 47 | −$448 | 83% | −0.0328 | −0.29 | −1.00 | THIN |
| QQQ-IC-0DTE-Fortress-S2 | IC | T2 | 12 | 4/16→5/21 | 35 | −$445 | 58% | −0.0079 | −0.52 | −0.16 | THIN |
| 1-45pm-Sandwich-Paper-v1 | Mirror | T2 | 9 | 5/12→5/22 | 9 | −$473 | 22% | −0.4125 | −1.18 | −4.47 | THIN; kill candidate |
| Friday 14 DTE BWB (B-70) | Mirror | T2 | 7 | 4/24→6/26 | 62 | +$1,120 | 100% | +0.0893 | +7.01 | 0.00 | **VERY THIN** |
| QQQ-IC-0DTE-Fortress-NoFilter | IC | T2 | 7 | 4/07→5/20 | 43 | +$908 | 86% | +0.0264 | +1.32 | 0.00 | VERY THIN |
| **QQQ long call** | Mirror | T2 | **6** | 4/20→6/08 | 49 | **+$5,967** | 100% | +0.3401 | +8.24 | 0.00 | **VERY THIN — see §2.5** |
| QQQ-IC-…-Wide2-155PM | IC | T2 | 6 | 3/19→5/18 | 59 | +$67 | 100% | +0.0619 | +3.59 | 0.00 | VERY THIN |
| **DIR-SPX-Put-Control** | Directional | T2 | 5 | 6/26→7/02 | 6 | −$1,045 | 20% | −0.4182 | −1.18 | −3.09 | VERY THIN (by design) |
| QQQ-IC-0DTE-Range075-PT50 | IC | T2 | 5 | 3/19→4/29 | 40 | +$24 | 80% | +0.0563 | +1.73 | 0.00 | VERY THIN |
| Tasty Condor | Mirror | T2 | 3 | 4/20→5/12 | 22 | +$1,095 | 100% | +0.3391 | +6.02 | 0.00 | VERY THIN |
| QQQ-IC-…-InverseFilter | IC | T2 | 3 | 4/23→5/20 | 27 | +$37 | 100% | +0.0678 | +4.87 | 0.00 | VERY THIN |
| **DIR-SPX-CallVIXdrop** | Directional | T2 | **2** | 6/30→7/02 | 2 | +$360 | 50% | +0.2237 | +0.28 | 0.00 | **VERY THIN** |
| QQQ-IC-VIX25-Range075-PT50 | IC | T2 | 1 | 3/19 | 0 | +$5 | 100% | +0.0549 | — | 0.00 | VERY THIN |

### 2.3 The single most important line in the inventory

**Exactly one bot in the entire project has ≥100 forward positions: the champion, at 221.**
The next largest is 55. Twenty-two of the 32 bots have fewer than 30 positions. Nine have fewer than 10.

And the champion — the one bot with an adequate trade count — **fails the 6-month span gate
(2.8 months) and has negative expectancy.**

**No bot in this project satisfies n≥100 AND span≥6mo AND positive expectancy in R.** Not one.
Given a 119-day total dataset, none could.

### 2.4 Non-ledger evidence

| Claim | Tier | Detail |
|---|---|---|
| Champion backtest: **95.3% WR, MAR 2.1, 3,747 trades, "walk-forward PASSED"** | **T4 / undocumented** | Sourced to a single archived table (`docs/_archive/bot-configs.md`) whose own header says treat as "last-known, not live." **No window, no commission assumption, no slippage assumption, no record of whether walk-forward preceded or followed parameter selection.** Asserted, not documented. |
| Directional **put track**: +9.2% RoR, PF 1.23 in-sample | **T4** | Selected as the best cell of a stop-loss sweep (SL40/50/none/90/75) run on the same data used to report the number |
| Directional **put track OOS**: +6.4% RoR, PF 1.15, **N=76** | **T4, not T3** | The "holdout" (Jul'24→now) is a *subset* of the in-sample range ("max available, ≈2022→now") used to pick VIX≥22, SL75, PT100 and the 11:00 entry. It is not out-of-sample. |
| Directional **call track**: +21.9% RoR, PF 1.63, N=337; IS +24.8% / OOS +19.1%; positive every year 2021–26 | **T4, borderline T3** | Same overlap problem, but a longer history and better year-by-year consistency. **The strongest artifact in the project** — see §3.4 |
| **C1 regime gate**: morning ATM IV predicts the day's range, p 0.000, 956 days | **T3 — genuinely validated** | This is real, well-executed statistical work and I credit it |
| Hedge tournament (9 exit rules, 148 real settled legs) | **T2 counterfactual** | **All nine arms negative.** See §3.3 |
| OO trial backtests (2 queued) | **T5 idea** | Not run |
| IC trailing-stop backtest (5 arms) | **T5 idea** | Not run |
| Reversal-scalp / Lab | **T5 idea** | 5-day signature *did not replicate* on 25 days; project correctly recorded the falsification |
| **Webull discretionary 0DTE, 8 July 2026** | **T1 — REAL MONEY** | The only real-money trading in this project. See §5 |

### 2.5 Data-integrity problems found in the project's own numbers

These are not nitpicks. Each one changes a headline the project relies on.

1. **The readiness board's Exp(R) uses the wrong risk denominator.** `STATUS.md` computes
   return-on-risk by summing *both* sides of a condor. A condor can only lose one side. Every
   Exp(R) on the readiness board is therefore **flattered toward zero** — losses look about half as
   bad in R as they are. My recomputation with the correct denominator is what appears in §2.2.

2. **The "18/15 clean post-fix condors" go-live gate silently drops 11 positions.** The post-fix
   epoch actually contains **29 positions, P/L −$5,455, Exp(R) −0.0383**. The gate counts 18 by
   excluding single-sided positions. The gate was declared CLEARED on a sample that is **losing money
   at nearly four times the champion's overall rate.** This is a textbook F3 violation: the headline
   depends on a subset selected after the fact.

3. **`QQQ long call` (+$5,967 on 6 positions) single-handedly makes the OA-Mirror pillar positive.**
   Pillar total is +$5,652. Remove that one bot and the pillar is **−$315** — negative, not flat.
   The project's own audit doc already flags this bot as the swing item with "membership ambiguity."

4. **~20.9% of the IC data is acknowledged strike-bug contaminated** and the cause is still unisolated.
   The project quarantines it honestly. But it means the QQQ hedge family — 305 of 934 positions,
   a third of the entire dataset — cannot be used as evidence for or against anything.

### 2.6 Time invested — recorded for context only, scored at zero

The project describes "roughly a year of focused, near-daily building," ~45 distinct backtests
totalling 150–1,200+ runs, 12–40+ hours of hands-on backtesting in the OA GUI alone, ~34 bot
configurations, and 59 markdown documents totalling several hundred thousand words.

**Per criterion K, this contributes exactly nothing to the score.** I record it because the family
should know the effort was real and the documentation is genuinely of professional quality. It is
also the single largest source of bias I have had to correct for, because the *volume* of work
creates a strong impression of validation that the *numbers* do not support.

---

## 3. EDGE VERDICT

### 3.1 Gate-by-gate result

| Gate | Result | By how much |
|---|---|---|
| **B1** — n ≥ 100 | **FAIL (31 of 32 bots)** | Only the champion clears it. Median bot has **18** positions |
| **B2** — span ≥ 6 months | **FAIL (universal)** | Entire dataset is 119 days. Champion: 84 days. Needed: ~182 |
| **B3** — regime change | **FAIL** | 3.9 months of 2026; no material vol-regime transition in the live record |
| **C1** — expectancy > 0 after costs | **FAIL, decisively** | Portfolio **−0.0217R**, t = **−2.92**. This is not "unproven" — it is *significantly negative* |
| **C2** — survives removing best win | **FAIL** | Already negative before the adjustment |
| **C3** — survives fill stress | **FAIL** | Already negative before the adjustment |
| **C4** — edge in R, not just $ | **FAIL** | Negative in both |
| **D1** — max DD known | **PASS** | −$14,540 champion; −3.06R. Properly tracked. Credit where due |
| **D2** — return ÷ max-DD ≥ 1.0 | **FAIL** | Return is negative |
| **D3** — worst day < 25% of profit | **FAIL** | There is no profit. A single day (6/17, −$7,530) exceeds the total of every green day in the SPX book |
| **D4** — no undefined risk | **FAIL → AUTOMATIC KILL** | The QQQ-Fortress pair is **downside-naked and still switched ON.** Three consecutive near-max-loss put breaches (6/17 −$7,530; 6/26 −$4,687 ×2). The "toggle off or add a stop" decision has been **overdue since 26 June** and is described in the project's own backlog as a *"2-minute setting flip."* |
| **E1** — named mechanism | **PASS for the concept, FAIL for the implementation** | Short-vol/VRP for the IC, long-gamma for directional. Real mechanisms, correctly named |
| **E2** — P&L shape matches mechanism | **FAIL** | See §3.2 — this is the deepest finding in the audit |
| **F1** — multiple-comparisons haircut | **FAIL** | See §3.4 |
| **F2** — re-tuning frequency | **FAIL → RE-TUNED** | QQQ→SPX, $2→$5 width, PT50→PT25, S1/S2/S3 hedge churn, 9:31→11:00 entry (changed after two losing days), and a live 11am-vs-1:30 A/B started *because the 1:30 clone was winning*. The champion's config has changed materially at least 5 times |
| **F3** — no post-hoc subset selection | **FAIL** | The go-live gate (§2.5 item 2) and the hedge tournament's per-bot cut (§3.3) both rely on it |
| **F4** — live vs backtest | **FAIL, catastrophically** | Backtest 95.3% WR → live **43%**. The project's own documents call this "the 95.3%→57% scar." It is now 43%, i.e. **worse than the failure they already named** |
| **G1** — live ≥ 50% of backtest expectancy | **FAIL** | Live expectancy is *negative* against a backtest claiming MAR 2.1. Per the locked rule, **no backtest produced by this process may be cited as evidence anywhere in this report** — including the directional numbers |
| **H1** — correlated pillars | **FAIL** | IC + Fortress + most mirrors are all short-vol. The project's own methodology doc records the finding that the portfolio was "9-of-10 short-vol." It is one bet |
| **H2** — demonstrated diversification | **FAIL** | Asserted, not demonstrated. The directional pillar has **7 positions total** |
| **H3** — stress test at size | **FAIL** | No such test exists. `rules-of-engagement.md` still has **4 unfilled `<FILL>` blanks**, including the absolute capital ceiling |
| **J1/J2/J5** | **TRIGGERED** | See §5 |

**Gates passed: 1.5 of 22.**

### 3.2 The mechanism does not match the P&L — and the reason is structural

This is the finding that matters most, and the project has all the pieces but has not assembled them.

The champion sells a $5-wide iron condor with short strikes 0.75% out of the money, collecting a
**median credit of $0.30 against $4.70 of risk — 6% of the width.** Unstopped, that structure needs a
**94% win rate** just to break even.

The project's own research (`docs/pivot-vwap-research.md`) states that **only 36% of days stay inside
±0.75% intraday**, meaning the champion's short strike is breached on roughly **64% of days.**

Those two numbers are irreconcilable. A structure requiring 94% survival, sold on strikes that survive
36% of the time, has no edge to defend — the hedge, the stop, and the profit target are all downstream
of a premise that does not hold. This is precisely why the backtest said 95.3% and reality says 43%.

The realized numbers confirm it exactly:

- Average win **+0.0383R** · average loss **−0.0473R** → **breakeven win rate 55.2%**
- **Actual win rate: 43.0%**

The gap between 55.2% needed and 43.0% delivered *is* the negative expectancy. There is no mystery
left to solve here. A vol-risk-premium seller should show many small wins and rare large losses; this
book shows **more losses than wins** (126 vs 95) with losses that are also *larger*. That is not a
short-vol edge underperforming. It is a structure whose payoff geometry is inverted.

### 3.3 The hedge tournament already proved this — and the conclusion was not drawn

The project's own hedge tournament replayed **all 148 real settled legs** through nine different exit
rules. The result, from `STATUS.md`, verified exactly:

| Rule | ride | pt25 | pt50 | pt100 | sl50 | sl75 | sl100 | sl130 | s2 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **Exp(R)** | −4.4% | −1.5% | −4.5% | −3.7% | −2.2% | −1.6% | −1.4% | −0.9% | −1.3% |

**Every single exit rule loses money.** Riding loses. Cutting loses. Every stop level in between
loses. The strike-touch hedge loses.

When no exit rule anywhere on the spectrum can make a structure profitable, **the problem is not the
exit. The problem is the entry.** The project instead read this table selectively — extracting a
30-trade subset where the champion's "ride" arm shows +7.3%, and building an entire queued backtest
program (`ic-trailing-stop-backtest.md`) around optimizing the exit mechanic.

That is the clearest instance of motivated reasoning in the project: the aggregate answer was on the
page and the search moved to a subset that gave a different one.

### 3.4 The directional pillar — the strongest evidence, and why it still fails

I want to be even-handed here, because this is the best work in the folder and it deserves an honest hearing.

**53 distinct backtest arms** were run across 13+ batches on the directional pillar. Under the locked
F1 rule, a winner selected from 53 trials requires **|t| > 2.82** to mean anything.

**Put track** — "OOS PASS," +6.4% RoR, PF 1.15, N=76, with PT100/SL75:

| | |
|---|---|
| Implied win rate | 46.5% |
| Implied σ(R) | 0.873 |
| **Implied t-statistic** | **0.64** |
| Required after 53-arm haircut | 2.82 |
| **95% CI on expectancy** | **[−13.2%, +26.0%]** — straddles zero |
| After the project's own stated 30–40% live haircut | **t = 0.42** |

This result is **statistically indistinguishable from zero.** It is not a weak pass. It is noise.
The project itself flags N=76 < its own 100 floor and that the profit is "LUMPY (mostly a 2026 vol
episode)." Both flags are correct, and both were then set aside in favour of "PASS."

Worse: the "holdout" window (Jul'24→now) sits **inside** the in-sample range ("max available,
≈2022→now") that was used to select VIX≥22, SL75, PT100, and the 11:00 entry. It is not
out-of-sample in any meaningful sense. Under the locked tier rules this is **T4, not T3.**

**Call track** — +21.9% RoR, PF 1.63, N=337, IS +24.8% / OOS +19.1%, positive every year 2021–2026:

| Assumed avg win | Implied t (OOS, n=174) | After the project's own 35% haircut |
|---|--:|--:|
| +1.5R | 2.65 | 1.72 |
| +2.0R | 2.25 | 1.46 |
| +3.0R | 1.81 | 1.18 |

Required after the 53-arm haircut: **2.82.** It does not clear it under any assumption — and after the
project's *own* prescribed live haircut it is not close.

**This is nonetheless the most credible artifact in the project.** Six consecutive positive years,
a coherent long-gamma mechanism, a real regime conditional, and a sensible economic story
(buy convexity when the market stops paying for it). If anything here becomes real, it is this.
But it currently has **2 forward positions**, and 2 is not evidence.

**The C1 regime gate** (morning ATM IV predicts the day's range, p 0.000 across 956 days) is
legitimate, careful statistical work. I credit it without reservation. It is a *permission gate*, not
a strategy — the project describes it correctly — and it does not by itself generate a dollar.

### 3.5 Kill discipline: the rules exist, and they are not being followed

The project wrote good kill rules in advance. That is genuinely to its credit. What happened next is
not.

| Pre-registered rule | Status | Response |
|---|---|---|
| Kill if WR < 75% over any rolling 30 | **Champion at 43% for 221 trades** | **No kill review recorded.** Logged as "DECISION NEEDED — adjudicate" in *four separate documents*, unresolved |
| Kill on single-day loss > 3× avg daily credit | **Triggered twice** (6/11 −$8,050; 6/17 −$7,530) | Flagged both times. **No kill executed.** Bots stayed on |
| QQQ-Fortress: toggle off or add put stop | **Third consecutive near-max-loss breach, 6/26** | **Still ON, still naked, still undecided as of the last file update** |
| #9 substrate: apply F-001/F-004 or pause | **Expired 29 June** | Overdue, unresolved |
| RoE capital ceiling, allocations, sweep % | **4 `<FILL>` blanks** | Never filled since the document was written |

The pattern is consistent and it is the F2/J3 signature: **when a pre-committed rule fired against a
system the owner is attached to, the rule was re-opened for debate rather than executed.** Every one
of these deferrals happens to keep a losing bot running. None of them ever went the other way.

The project's methodology doc says "kill on data, even when uncomfortable," and cites the ORB-60m kill
as proof. That kill was real and correct — but ORB-60m was somebody else's strategy from a marketplace.
**No strategy the owner built himself has ever been killed by a triggered rule.** That asymmetry is
the whole tell.

### 3.6 Confidence score

# **9 / 100**

*(Rubric band 0–15: "No system passes the sample-adequacy gate. Evidence is backtest/idea only.")*

**Why not lower:** the C1 regime gate is real validated science. The call-track backtest is coherent,
mechanism-backed, and positive in six consecutive years. The ledger reconciles to the dollar. The
drawdown tracking, contamination quarantine, R-based comparison discipline, and the honest recording
of the reversal-scalp falsification are all things most retail projects do not do at all. Several
kills (ORB-60m, PT50, S3, the 5-day reversal signature) were executed correctly on data. The
infrastructure is real and the documentation is professional-grade.

**Why not higher:** the portfolio's realized expectancy is not merely unproven — it is **significantly
negative at t = −2.92 across 934 positions.** The one bot with an adequate trade count loses money.
Every exit rule ever tested on the real data loses money. The flagship's backtest-to-live gap is worse
than the failure the project already named and memorialized. The "out-of-sample" directional results
are not out-of-sample and are statistically indistinguishable from zero after the multiple-comparisons
haircut the project's own standards demand. Pre-registered kill triggers have fired repeatedly and
been deferred every time. A naked-downside position has been left switched on for a month past a
"2-minute" fix. And there is a live real-money loss-chasing episode on the record.

### 3.7 The written call

> **DO NOT ADVANCE. DO NOT DEPLOY LIVE CAPITAL.**
>
> **KILL** the IC pillar as currently constructed — the champion, the Fortress family, and the QQQ
> hedge bots. This is not "keep testing." The structure is mathematically broken: it needs a 94%
> survival rate on strikes that survive 36% of the time, it has lost money on 221 forward positions,
> and no exit rule in existence rescues it. Continuing to test it is not research; it is hoping.
>
> **KEEP ON PAPER, UNDER A HARD TIME-BOX** the directional call track and, secondarily, the put
> track. These have a real mechanism, a real regime conditional, and the only genuinely encouraging
> backtest in the folder. They also have 7 forward positions between them, which is nothing.
>
> **TOGGLE OFF TODAY** the QQQ-Fortress pair. Naked downside exposure with three consecutive
> near-max-loss breaches and an overdue decision is an automatic kill under any serious risk policy,
> and it is a two-minute action that has been open for a month.
>
> **STOP the discretionary Webull scalping and the intraday "cockpit" workstream entirely.**
> See §5. This is the highest-risk activity in the project by a wide margin, it is the only real money
> in play, and it is moving in the wrong direction.
>
> **DO NOT SHOW `investor-profile.md` TO ANYONE.** See §5.4.

---

## 4. INSUFFICIENT-EVIDENCE REGISTER

Items where the evidence does not support a verdict either way. I am not guessing at these. Each
lists the exact data that would resolve it.

| # | Unproven claim | What would resolve it |
|---|---|---|
| 1 | **Call track has a real edge** (+21.9% RoR, PF 1.63) | (a) A true holdout: re-run with parameters frozen as of a stated date and tested *only* on data after that date, never touched during selection. (b) **≥100 forward paper positions** post-freeze — at ~1 fire per 5 trading days this is roughly 24 months, so run it at higher frequency or accept the wait. (c) Expectancy recomputed after $0.60/contract commission and ≥$0.05/leg slippage. (d) The t-statistic must clear **2.82** after those costs. Currently t ≈ 1.2–1.7 |
| 2 | **Put track has a real edge** (+6.4% OOS) | **N=76 → N≥250** on a genuine holdout. At the current CI of [−13%, +26%], even 250 trades may not separate it from zero. Recompute the CI at each 50-trade milestone; if it still straddles zero at N=250, kill it |
| 3 | **C1 regime gate converts to dollars** | The statistical validation (p 0.000, 956 days) is sound. What is missing is a **strategy conditioned on it with ≥100 forward trades and positive expectancy after costs.** The gate predicts range; nobody has shown that predicting range is monetisable at these credit levels |
| 4 | **Nigiri mirror is fundable** (+0.0100R, t=9.36, n=37) | The t-statistic is high but n=37 and the max-DD is 0.00, which usually means the sample simply hasn't met its bad regime yet. Needs **≥100 positions and ≥6 months**, including at least one VIX>25 episode. Also needs the G5 instruction-mirror compliance feed the project has already specified |
| 5 | **3DTE mirror is fundable** (+0.0147R, t=0.60, n=43) | t=0.60 is noise. Needs **≥100 positions**; re-evaluate then. Do not fund on 43 |
| 6 | **QQQ long call is a real strategy** (+$5,967, n=6) | Six trades. This number should be **removed from every pillar total until n≥30**, because it is currently the sole reason the OA-Mirror pillar reads positive |
| 7 | **"Riding beats cutting" on the champion** (+7.3% vs +2.0%) | Derived from a 30-position subset of 148. Recompute on **all 148 with no subsetting**; the aggregate ride arm is −4.4%. Moot if the IC pillar is killed as recommended |
| 8 | **1:30pm entry beats 11am** (130PM clone +$480 vs champion −$1,350) | 3 shared days, 42 total positions, 10-day span. Needs **≥100 positions each, same days, same size.** Currently a coin flip being read as a signal |
| 9 | **S2 hedge is production-valid** | Project's own note: "S2 NOT production-validated (backtest-only)." Needs **≥50 S2 fires with logged fills.** Currently 15 |
| 10 | **Live fills match paper fills** | **Zero slippage observations logged.** The v5-slippage task ("≥20 fills vs mid") has been open since at least 8 June. Until ~20 real fills are recorded, *every* number in this project is a modeled fill, and the champion's economics tolerate about **$0.02/leg before a quarter of all credit collected is gone** |
| 11 | **The QQQ strike-resolution bug** (20.9% contamination) | Cause is "unisolated." Until it is found, 305 positions — a third of the dataset — are uninterpretable, and the same class of bug may be present in the SPX data undetected |
| 12 | **Reversal-scalp ≥2σ VWAP fade** (MFE/MAE 1.15, n=234) | Project's own read is "weak but alive." MFE/MAE is not expectancy. Needs a **full forward test with entry/exit rules, costs, and ≥100 completed round-trips.** The 5-day version already failed to replicate on 25 days — that is a warning, not a starting point |
| 13 | **Pillars are diversified** | Needs a **same-day return correlation matrix across pillars over ≥100 shared trading days.** Directional has 7 positions total; this cannot currently be computed |
| 14 | **Fleet survives its worst historical day at target size** | No stress test exists. Needs the worst 5 days in the C1 history replayed at the intended live size against a stated max-loss number — **which requires filling the 4 `<FILL>` blanks in `rules-of-engagement.md` first** |
| 15 | **The champion backtest (95.3% WR / MAR 2.1)** | Currently unfalsifiable — no window, no cost assumptions, no walk-forward protocol recorded. Either produce the full backtest artifact or **delete the claim from every document.** It is currently cited in `current-state.md` as a live fact |

---

## 5. HUMAN-RISK & OVERSIGHT

*This section is assessed entirely separately from §3. A system can have a real edge and still be too
dangerous for a particular person to operate. The reverse is also true. I have not let either
judgment touch the other — the quantitative verdict above would be identical if the owner had no
gambling history at all.*

### 5.1 What the project gets genuinely right

I want to start here because it is real and the family should weigh it.

The owner has built, unprompted, a substantial and sophisticated set of anti-gambling controls:

- `north-star.md` names the risk explicitly — *"the thing I re-read when the craving hits"* — and
  contains a pre-committed refusal of hourly Kalshi scalping: *"activity without outcomes… it's the
  exact impulse these systems exist to retire… Kalshi gives me action that bleeds. I made this call
  once — I don't re-litigate it three times a week."*
- `rules-of-engagement.md` contains cooling-off periods on size increases, a no-changes-during-streaks
  rule, quarterly profit sweeps against house-money psychology, and — notably — a requirement for
  **monthly external review with another person**, with the stated rationale that *"most blow-ups
  would have been avoided if the override had to be explained first."*
- The entire architecture is designed to put a machine between the owner and the market, and to grade
  **behavioural compliance separately from P&L.**
- The `scalp_trading_contract.md` is a well-constructed relapse-prevention document.

This is a person with real insight into his own risk who has built genuine structural defences. That
is materially better than the alternative, and it should be said plainly.

### 5.2 What the evidence shows is actually happening

Every one of those controls is **written but unenforced**, and the one place real money touched the
market, they all failed simultaneously.

**The 8 July 2026 Webull episode** — the only real-money trading in this project:

| Metric | Value |
|---|---|
| Opening trade | 12 QQQ 0DTE calls, ~$228 premium |
| Peak realized P&L | **+$741** |
| Final P&L | **−$282** |
| Give-back | **$1,023 = 138% of peak** (contract cap: 40%) |
| Redeploy-after-win events | **4** (712C, 713C, 714C, 715C — all further OTM, all after banking the win) |
| Contracts at peak | **45** vs a 15 cap (3.8×) |
| Premium deployed | **~$1,400** vs a $450 day cap (3.1×) |
| Trades | **10+** vs a cap of 4 |
| Stops set | **None on any chase leg** |
| Contract rules violated | **7 of 9** |
| Process grade | **RED** |

The owner's own written debrief is accurate and unsparing: *"the leak is give-back via roll-up… 100%
of the day's loss came from the post-win redeploy chain."* The 28 contracts bought at 13:59–14:01
were purchased at the +2σ extension top **that he had personally flagged as the top earlier that day.**

This is not a bad trading day. It is the textbook clinical signature of chasing: bank a win, escalate
size, buy the extension, no stop, hold to zero. It is the specific behaviour the entire Bot Fleet was
built to engineer out — and it happened anyway, at 6× the intended size, in the middle of the project.

**The contract capping this behaviour was written on 8 July, from that day.** It has never been
tested. It has no signature and no date on it. And the file directory shows **no project activity
after 8 July** — nineteen days as of this report.

### 5.3 The direction of travel is the alarm, not the loss

The $282 loss is trivial. The trajectory is not.

The project's most recent work — the `intraday-cockpit`, `reversal-scalp-workstream`, and
`scalp_trading_contract` — represents a **migration away from automated, defined-risk, once-a-day
systematic trading and toward discretionary, screen-watching, real-time intraday 0DTE scalping.**

That is movement in exactly the wrong direction for this person, and it happened for a recognisable
reason: the automated pillars are losing and slow, and the discretionary lane provides immediate
action. The protocol described in `scalp_trading_contract.md` — *"Every trade I take, I share the fill
immediately… Optionally Claude sets the OCO on the Webull screen via computer control; I click
submit"* — converts an AI assistant into a **real-time trading co-pilot for tick-by-tick discretionary
0DTE.** Whatever its intent, its effect is to make high-frequency discretionary trading easier,
faster, and more continuously engaging.

Under criterion **J5** — *position sizing increased following a losing period* — this triggers an
automatic kill on human-risk grounds, independently of any edge finding. The escalation from 12 to 45
contracts occurred within a single session, after a realized win, with no stop.

Two further observations, stated without interpretation:

- `north-star.md`'s pre-commitment to *not* re-litigate Kalshi shows the owner knows his pattern is
  to re-open closed decisions. §3.5 documents that he has done exactly this with **five separate
  pre-registered kill triggers**, every time in the direction of keeping a losing position alive.
- The stated purpose of the whole system — *"a system that trades while I work"* — is contradicted by
  a workstream requiring continuous screen attention during market hours.

### 5.4 `investor-profile.md` — the most serious item in this report

The folder contains a completed, polished investor pitch document dated 8 July 2026, written to
solicit money from *"the founder's own network first — friends, family, and everyday followers."*

Measured against the ledger, it contains representations that a securities regulator would examine:

| Document says | Ledger says |
|---|---|
| *"Two directional engines have cleared out-of-sample testing… That's the highest bar the project applies, and they passed it"* | The holdout window sits inside the parameter-selection window. The put track's t-statistic is **0.64** with a CI of [−13%, +26%]. Combined forward record: **7 positions** |
| *"The flagship range strategy has cleared its internal readiness gate… running in paper with clean, rule-following execution"* | The gate was cleared on a hand-selected 18-of-29 subset that is **losing at −0.038R**. The flagship is down **−$11,155 over 221 positions** and fails its own written kill trigger by 32 percentage points |
| *"The hedging and loss-control logic has been stress-tested against real historical losing days to confirm the caps actually cap"* | The tournament that did this found **all nine exit rules negative.** And a naked-downside bot has taken **three consecutive near-max-loss breaches** with the fix outstanding for a month |
| *"has already spent a year proving to himself, on data, that the edge is real"* | The data demonstrates a **statistically significant negative** expectancy: −0.0217R at **t = −2.92** across 934 positions |
| *"7+ years in finance and options trading"* | Not assessable from this folder |

To the document's real credit, it states plainly: *"No live capital yet. Everything to date is
paper/simulated. That is the honest headline,"* and *"Explicitly not promised: any specific return."*
Those disclosures are genuine and they matter.

But the load-bearing claim — that the edge has been *proven on data* — is **contradicted by the data
in the same folder.** A pitch to friends and family whose central premise is falsified by the
project's own ledger is a category of risk that dwarfs everything else in this audit: financial,
relational, and legal. This is also the point at which a personal harm-reduction question becomes
other people's money.

### 5.5 Recommended control structure

**These are conditions, not suggestions. If any one cannot be met, the answer is that the project
should not continue in any form that touches money.**

**Immediate — this week**

1. **Zero real money. All pillars, all lanes, no exceptions.** Paper only. This is already the stated
   policy for the bots; it must now explicitly extend to the Webull discretionary account.
2. **Close or zero the Webull options-enabled account**, or remove 0DTE options permissions from it.
   This is the only account through which real money has reached the market and the one where every
   control failed at once.
3. **Toggle OFF the QQQ-Fortress pair.** Two minutes. A month overdue. Naked downside.
4. **Shelve `investor-profile.md`.** No version of it goes to any friend, family member, or follower
   until an independent third party — not the owner, not an AI — has verified every performance claim
   against the ledger.
5. **Terminate the discretionary intraday cockpit / reversal-scalp workstream.** Not paused. Ended.

**Structural — before any future real money, ever**

6. **Custody separation.** Any live account is opened and funded by someone other than the owner.
   The owner gets read-only credentials. He can watch and analyse; he cannot deposit, size, or place
   an order. This is the single most important control and it is non-negotiable given §5.2.
7. **Independent go-live authority.** The decision to move from paper to live is **not the owner's to
   make.** It belongs to a named third party — ideally the trading peer named in
   `rules-of-engagement.md` §6, or a fee-only fiduciary advisor with no stake — applying the mechanical
   criteria in §6 below. The owner may present evidence; he does not hold the switch.
8. **Fill the four `<FILL>` blanks in `rules-of-engagement.md` now, in writing, witnessed, before any
   further work.** Absolute capital ceiling; per-pillar allocation; profit-sweep percentage; the named
   accountability person. A governance document with blank ceilings is not a governance document.
   Given the account size described (~$4k Tradier), I would expect that ceiling to be **a low four-figure
   number the household can lose entirely without consequence.**
9. **Monthly external review — actually convened, with a written record.** The rule exists in §6 of the
   RoE and there is no evidence it has ever been held. Put a recurring date on a calendar.
10. **Automated kill enforcement.** Kill triggers must fire in code and toggle bots off without a
    human in the loop. §3.5 demonstrates that when a rule requires a human decision from this owner,
    it does not execute. `report.py` already has the hooks; wire them.
11. **A hard cap on market-hours screen time**, agreed with the accountability partner. The purpose of
    an automated system is to remove the operator from the screen. If the project requires watching
    the tape, it has defeated its own reason for existing.
12. **Clinical support in the loop.** If the owner has a treating clinician for the problem-gambling
    diagnosis, that clinician should see §5.2 and §5.3 of this report. The 8 July episode is clinical
    data, not just a trading debrief, and I am not qualified to weigh it in that frame.

**Should the project exist at all?**

**Yes — but only as pure research, with no money in it, under the controls above.** Killing it
outright is, in my assessment, the *higher*-risk option. This project is currently absorbing an
enormous amount of an evidently compulsive drive and converting it into documentation, statistics,
and falsification tests. Removing that outlet without replacing it does not remove the drive; the
project's own north-star document tells you where it goes instead. Kalshi is named, sitting queued,
and explicitly recognised as the thing being held at bay.

The research, the statistics, and the writing are real skills being genuinely developed. Keep the
lab. Remove the money. Take the go-live switch out of the owner's hands entirely. And watch the
*direction of travel* — a return to discretionary intraday scalping is the relapse signal, and it is
far more diagnostic than any P&L number.

---

## 6. FORWARD TIME-BOX

The purpose of this section is to make the next decision **mechanical**. It is set now, in advance,
so that in six months nobody has to argue about what the numbers mean — they only have to read them.

### The test

- **Duration:** **6 calendar months.** Start date = the day the conditions below are met. Hard end
  date. No extensions, and specifically no extension on the grounds that "it was just starting to work."
- **Capital:** **$0.** Paper only, in all lanes, for the entire window.
- **Scope — exactly three systems. Nothing else runs:**

| # | System | Why |
|---|---|---|
| 1 | **Directional call track** — Long Call Spread · VIXΔ% < −2 · no PT · SL50 · 11:00 | The only mechanism-backed, multi-year-positive artifact in the project |
| 2 | **Directional put track** — Long Put Spread · VIX ≥ 22 · PT100 · SL75 · 11:00 | Second-best; the regime complement |
| 3 | **Nigiri mirror** — as currently configured | Highest t-statistic among the mirrors; someone else's edge, which removes the owner's design bias |

- **Explicitly excluded from the window:** the IC pillar in every form (killed), the Fortress family,
  the QQQ hedge bots, all other mirrors, the Lab, the reversal-scalp, and all discretionary trading.

### Conditions that must be true before the clock starts

1. All parameters for all three systems **frozen in a dated, committed file.** No change to any
   parameter during the window, for any reason, including a losing streak. A change resets the clock to day zero.
2. The four `<FILL>` blanks in `rules-of-engagement.md` filled and witnessed.
3. QQQ-Fortress off. Webull options access closed. `investor-profile.md` shelved.
4. **≥20 real fills logged versus mid** (the open v5-slippage task) so that a measured slippage
   number, not a modelled one, can be applied at the end.
5. The named independent reviewer has agreed to hold the go-live switch.

### Mechanical decision rule at the end of month 6

Compute, per system, from the forward paper ledger only, **after** deducting $0.60/contract commission
and the measured slippage from condition 4:

| Outcome | Criteria — **all** must hold | Decision |
|---|---|---|
| **ADVANCE TO LIVE** | n ≥ 100 forward positions · Exp(R) > 0 after costs · **t > 2.82** · max-DD ≤ 3.0R · zero naked positions all window · zero parameter changes all window · zero discretionary real-money trades all window | Live, at a size where **6 months of the worst observed drawdown is ≤ 2% of household net worth.** Funded and custodied by the third party. Reviewed monthly |
| **KEEP TESTING** *(one extension only, ever)* | Exp(R) > 0 after costs but n < 100 **or** t between 1.50 and 2.82 · all discipline conditions met | Extend **6 months and no more.** At month 12 it either clears the ADVANCE bar or it is killed. There is no month 18 |
| **KILL** | Exp(R) ≤ 0 after costs · **or** t < 1.50 at n ≥ 100 · **or** any parameter changed mid-window · **or** any naked position · **or** any real-money discretionary trade · **or** any kill trigger fired and not executed within 48 hours | System deleted. Not paused, not archived for later, not "revisited when conditions change" |

### The overriding clause

**If any real money is traded discretionarily by the owner at any point during the window — in any
account, in any instrument, in any size — the entire time-box ends that day and the answer is KILL
for all three systems.**

This is deliberately harsh and it is the most important line in this section. The controlling variable
in this project is not the edge. It is whether the operator can go six months without reaching for
action. If he cannot, the edge is irrelevant, because it will never be the thing that determines the
outcome.

### Why six months and not longer

Six months is the project's own stated minimum span, it is long enough for the champion's replacement
to accumulate a real sample, and it is short enough to be a genuine decision point rather than an
indefinite runway. It also spans at least one earnings cycle and, on any reasonable base rate, at
least one volatility episode — which is what the directional systems need in order to show anything
at all.

---

## 7. BOTTOM LINE

*Written to be read aloud.*

After recomputing every number from the raw trade ledger, my confidence that this project has
demonstrated a real, tradeable edge is **9 out of 100** — and that is not a case of "we don't know
yet." Across 934 paper trades the fleet has a **statistically significant negative** expectancy, the
one strategy with enough trades to judge has lost money on 221 of them while failing its own written
kill rule by thirty-two points, and the project's own test of nine different exit strategies found
that **every single one of them loses.** The flagship needs the market to stay inside a narrow band
94% of the time and it does so 36% of the time; that gap is not a tuning problem, and no amount of
further work will close it. My recommendation is to **kill the iron-condor pillar today**, keep only
the two directional strategies and one mirror bot on paper — with zero dollars — for a fixed six-month
window with the pass/fail numbers already written down in §6, and to place the decision to ever go
live in someone else's hands, not Andy's.

Separately, and more urgently: the only real money that has touched the market in this project was a
single discretionary session on 8 July that turned a $741 profit into a $282 loss by breaking seven of
nine of his own written rules within minutes of banking the win — and the newest work in the folder is
moving *toward* that kind of trading and away from the automated systems. **The Webull account should
be closed this week, and `investor-profile.md` — which tells friends and family the edge has been
proven on data — must not be sent to anyone**, because the data in the same folder says the opposite.

I want to be equally direct about what is real: the statistical validation of the volatility regime
gate is genuine work, the call-spread strategy is the one thing here with a coherent economic reason
to make money and six consecutive positive years behind it, the record-keeping is better than most
professionals manage, and Andy built anti-gambling controls into this project before anyone asked him
to. The problem is not that he is fooling himself about the process. **It is that he is judging a
losing system by the quality of the machinery he built to study it.** The machinery is excellent. The
strategies do not work.

**The one thing that would most change my verdict:** the directional call track, with its parameters
frozen today, producing **100 or more forward paper trades over six months with positive expectancy
after real measured costs and a t-statistic above 2.8** — and Andy going that entire six months
without placing a single discretionary trade. If both of those happen, I will have been wrong about
the strategy and, far more importantly, he will have proved the thing that actually matters.

---

*This audit is based solely on the contents of the `bot-fleet` project folder as of 8 July 2026 and
contains no information from outside it. All quantitative figures were recomputed from
`data/trades.csv` and independently re-verified. This is not investment advice, and I am not a
clinician; §5 raises questions that a qualified professional should weigh.*
