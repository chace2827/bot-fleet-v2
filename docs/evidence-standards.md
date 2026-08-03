# Evidence standards

*Written 2026-07-31 for Bot Fleet v2. First version.*

> ## ✍️ WRITTEN TO BE REVISED
> Andy has flagged wanting a scoring redesign. **This document is a faithful consolidation of
> the standards already adopted — not a proposal, and not my own design.** Its job is to put
> the machinery in one place, with its seams visible, so a redesign session has something
> concrete to argue with. §10 lists what I think that session should fix.
>
> Nothing here is invented. Every tier, gate, threshold and formula is quoted or closely
> paraphrased from a named source. Where two sources disagree, **both are stated and the
> disagreement is flagged** — none of them are reconciled here, because reconciling them is a
> decision, not a transcription.

---

## 1. Authority — what was adopted, and what was not

The independent audit of 2026-07-27 and its pre-commitment ledger are carried for their
**evidence machinery only**.

**ADOPTED:** the T1–T5 tiers, and the sample gates (n≥100 / 6 months / regime change).

**OVERRULED** *(banner added 2026-07-30; `CLAUDE.md` §4, `build-plan.md` §5)*:

| Verdict | Recorded reason for overruling |
|---|---|
| **"Kill the IC pillar"** | The champion's *declared* strategy (PT25+S2) **never ran**, so it is neither validated nor falsified. What did run (ride+S2 post-fix) is n=29 — THIN under the adopted gates, meaningless either way. The audit's strongest counter-argument, the "94% vs 36% band", was computed on the contaminated full ledger including 317 pre-fix legs opened at 9:xx against an 11:00 config, plus QQQ arms now known mis-built — **not decision-grade either**. Verdict: **continue at pilot scale under pre-registration; "grow it" is earned at gate-clearance, not scheduled.** |
| **AUTOMATIC KILL / add-a-stop on the QQQ-Fortress pair** | The "naked tail" was a broken bot — its own PT50 + 15:50 exits were dead. Restored, June flips **−$4,809 → +$3,227**. Decision is **restore & verify, then re-ask**. |
| **Custody separation + independent go-live authority** (audit §5.5 items 6–7) — *previously mis-recorded as "switch to a third-party platform"* | **Go-live authority stays with Andy.** The substitute controls are external review of `rules-of-engagement.md` and the pre-registration discipline (§8). **Corrected 2026-07-31 — see §9.2.** Flagged for optional reconsideration at the redesign session. |

> **The audit's own locking clause still binds us, and it cuts our way too:**
> *"THESE CRITERIA ARE LOCKED. I WILL NOT LOOSEN THEM AFTER SEEING THE RESULTS. If I find a
> threshold was wrong, I may only make it STRICTER, and I must flag that I did."*
> A redesign that loosens a gate must say so out loud and say why.

---

## 2. The evidence tiers

**A system is scored at its highest-quality tier and never allowed to borrow credibility upward.**

| Tier | Meaning |
|---|---|
| **T1 LIVE** | Real money, real fills, broker-confirmed. |
| **T2 PAPER** | Automated paper execution *with realistic fills*, forward in time, no lookahead. |
| **T3 OOS BACKTEST** | Parameters fixed **before** the test window; window untouched during design. |
| **T4 IS BACKTEST** | Any backtest whose window overlaps the period/data used to select parameters. |
| **T5 IDEA** | Spec, roadmap, doc, forum concept. **Scores zero.** |

**The rules that make the tiers bite:**

- **A T4 result may never be cited as support for a T1/T2 claim.**
- **A backtest re-run after seeing its own output is T4 by definition.**
- Only **T1 or T2** trades count toward the sample gate B1.
- **Nothing below T2 with n≥100 positions / 6 months / a regime change supports a live-capital
  or growth decision.**

### 2.1 ⚠️ Three seams in the tier system — flagged, not fixed

1. **Two source wordings differ.** The pre-commitment ledger's T2 says *"with realistic
   fills"*; the audit's drops it. T4 says *"overlaps the **period**"* (ledger) vs *"overlaps the
   **data**"* (audit). **The T4-citation prohibition appears only in the ledger.** I have used
   the stricter reading of each above, per the locking clause — flagged here because that is a
   choice, not a transcription.
2. **"Nothing below T2 …" is a project synthesis, not audit text.** The audit says T3/T4/T5
   score lower and T5 scores zero; it never phrases a "below T2" bar. The phrasing originates
   in `CLAUDE.md` §4 / `build-plan.md` §5. It is adopted — but it is ours, not theirs.
3. ~~The "separate, weaker gate" for T3 evidence is named and never defined.~~
   **✅ DEFINED 2026-07-31 (Andy) — see §4.5, gate T3.**

### 2.2 Naming collisions — do not import
`T1–T3` also names hedge-mechanic evidence classes and breach-response rules in
`hedge-research.md`; platform-capability priorities in `oa-platform-reference.md`; build
sequencing in the old brief spec; and a backtest batch in `build-plan.md` §6. **None of these
are evidence tiers.** When writing "T2", say "evidence tier T2".

---

## 3. There are TWO gate systems. Keep them apart.

This is the single most confusing thing in the corpus and the letters collide badly.

| | **System I — pre-commitment gates A–K** | **System II — readiness board G1–G6** |
|---|---|---|
| **Source** | independent audit + pre-commitment ledger | `scripts/report.py` (code-enforced) |
| **Grain** | a *system* / pillar / the fleet | **one bot, per condor** |
| **Purpose** | adjudicate whether evidence is admissible at all | graduate a bot along a ladder |
| **Output** | PASS/FAIL + a 0–100 confidence score | `●` pass / `○` fail / `·` pending, and a stage |
| **When** | at a decision point (advance, grow, fund) | every daily run, automatically |

> ⛔ **`G1` means two different things.** In System I it is *"live Exp(R) ≥ 50% of backtested
> Exp(R)"*. In System II it is *"clean data — no strike-bug, single-sided excluded"*. Likewise
> `B1`, `C1`, `C2` and `G2` all collide with unrelated schemes elsewhere in the folder.
> **Always write the system: "audit gate C1" or "board gate G3".**

---

## 4. System I — the pre-commitment gates (A–K)

Binary, per system. The ledger is the source of record; where the audit's abridgement drops
something, the ledger wins.

### B — SAMPLE ADEQUACY. **PASS requires ALL of:**

| | Criterion |
|---|---|
| **B1** | **n ≥ 100 closed positions at T1 or T2.** |
| **B2** | **Span ≥ 6 calendar months** of forward/live time. |
| **B3** | Span includes **≥ 1 distinct volatility regime change** — defined as *"a VIX move of ≥ 10 points peak-to-trough, or both a sub-15 and an above-25 VIX period."* |

**Anything failing B1 or B2 is stamped THIN and cannot contribute to the edge score.**

Calibration note from the ledger: *"For 0DTE strategies specifically, 100 trades ≈ 5 trading
months at 1/day. This is the project's own floor and I am adopting it unchanged."*

⚠️ B1 reads *"closed **trades**"* in the ledger and *"closed **positions**"* in the audit. Given
§6's unit-of-account rule these are different numbers. **Positions is the reading used here.**
⚠️ The operational VIX definition of B3 exists **only** in the ledger — cite B3 from the audit
and you lose the test entirely.

### C — EXPECTANCY (the sanity check)

| | Criterion |
|---|---|
| **C1** | Expectancy per position in R = **(Win% × AvgWin_R) − (Loss% × AvgLoss_R)**, must be **> 0 AFTER costs.** Costs = commissions + exchange fees + modelled slippage of **≥ 1 tick per leg on entry and exit (4-leg IC = 8 ticks round trip)**. |
| **C2** | Expectancy stays **> 0 with the single largest winner removed.** |
| **C3** | Expectancy stays **> 0 with the worst 5% of days given a 1.5× loss multiplier** (fill degradation; 0DTE tails fill worse than modelled). |
| **C4** | **Edge visible only in raw P/L but not in R = FAIL.** Different position sizes make raw P/L uninterpretable. |

**FAIL of C1 = kill. FAIL of C2 or C3 = the edge is tail-dependent, not demonstrated.**

### D — RISK QUALITY
- **D1** Max realized drawdown, in R, must be known and stated. **Unknown = FAIL.**
- **D2** Return ÷ max-DD **≥ 1.0** at T1/T2 over the measured window.
- **D3** Worst single day **< 25% of the window's total profit.**
- **D4** **Undefined-risk or naked exposure at any point = automatic kill regardless of P&L.**

### E — MECHANISM (non-negotiable)
- **E1** State in one sentence **why it makes money** — a named economic source (variance risk
  premium, dealer gamma/pinning, overnight drift, term-structure carry, a validated regime
  conditional). ***"It backtested well" is not a mechanism.***
- **E2** The claimed mechanism must be **consistent with the observed P&L shape.** A VRP seller
  should show many small wins and rare large losses; if the curve doesn't look like the
  mechanism, one of the two is wrong.
- **E3** Pattern-only results with no E1 answer are **CURVE-FIT by default. The burden is on the
  system to rebut.**

### F — OVERFITTING / SCANNER COUNT
- **F1** Multiple-comparisons haircut: a winner chosen from N variants needs roughly
  **|t| > √(2 ln N)** — N=20 → 2.45 · N=53 → 2.82 · N=150 → 3.17 · N=1,200 → 3.77.
  *"A single Sharpe-1 result out of 20 tried is noise."*
- **F2** Parameters changed more than **once per 30 trading days** on average → stamped
  **RE-TUNED**; the live record restarts at the last change and **the sample count resets with it.**
- **F3** If the headline number depends on a subset chosen **after** seeing performance, *"the
  number is discarded entirely."*
- **F4** Live materially worse than backtest (**> 50% of backtested expectancy lost**) is
  evidence the backtest *process* is broken, and **taints every other backtest from that process.**

### G — LIVE-VS-BACKTEST TRACKING
- **G1** Live expectancy in R must be **≥ 50%** of backtested expectancy in R over the same
  period. Below that, the backtester is not decision-grade and **no backtest from it may be
  cited as evidence anywhere.**

### H — PORTFOLIO LEVEL
- **H1** If every pillar is net-short-vol / net-short-gamma, **the fleet is ONE bet, not four,
  and is scored as one system with one sample.**
- **H2** Diversification claims require **demonstrated** near-zero or negative same-day return
  correlation between pillars. ***"Assertion is not demonstration."***
- **H3** Must survive its **worst historical stress day at current size** without breaching a
  stated max loss. **No such test = FAIL.**

### I — CONFIDENCE SCORE (0–100)

| Band | Meaning |
|---|---|
| **0–15** | No system passes B. Backtest/idea only. *"The default state of any project that has not yet accumulated 100 live/paper trades."* |
| **16–30** | At least one system passes B, but fails C, E or F. |
| **31–50** | One passes B + C + E but fails F or G, or the sample is at the bare minimum. |
| **51–70** | One or more pass B + C + D + E + F + G. Edge probably real but small or fragile. **Advance to live at reduced size.** |
| **71–85** | Multiple independent-mechanism systems pass all gates across **≥ 12 months and a regime change**. |
| **86–100** | Institutional-grade. *"No retail 0DTE project should expect to reach this."* |

### J — AUTOMATIC KILLS *(any one ends the system, no discussion)*
- **J1** No system has ≥100 forward positions **and** the project is asking to increase size.
- **J2** Any undefined-risk position, or sizing such that **a 3× expected loss day exceeds 10%
  of account equity.**
- **J3** Live diverges from backtest and the response was **to re-fit the backtest rather than
  stand down.**
- **J4** Evidence of **manual override of automated rules for P&L reasons.**
- **J5** **Position sizing increased after a losing period (loss-chasing)** — a kill on
  human-risk grounds, independent of the edge.

### 4.5 Gate T3 — the weaker gate, DEFINED 2026-07-31 (Andy)

The ledger promised *"(T3 counts for a separate, weaker gate only.)"* and never defined it,
leaving out-of-sample backtest evidence with no home. **Andy's ruling: generalize the
directional OOS protocol — the one thing in this project that actually cleared out-of-sample —
into the standing T3 gate.**

**PASS requires ALL of:**

| | Criterion |
|---|---|
| **T3.1** | **Parameters frozen before the test window.** Dated, committed, unchanged during design. |
| **T3.2** | **The window untouched during design.** Look at it once. Looking twice makes it T4. |
| **T3.3** | **n ≥ 100 backtest trades over ≥ 2 years, including a regime change** (audit gate B3's definition: a VIX move ≥ 10 points peak-to-trough, or both a sub-15 and an above-25 period). |
| **T3.4** | **Positive after a 30–40% haircut plus commissions.** Backtest expectancy is optimistic by construction; a result that survives only at full strength has not cleared anything. |
| **T3.5** | **Beats its control.** A variant with the tested condition removed, run over the same window. An absolute number with no control is not evidence about the condition. |
| **T3.6** | **Clears the F1 multiple-comparisons haircut** — \|t\| > √(2 ln N) for N variants tried. |

### ⛔ WHAT A T3 PASS AUTHORIZES — AND WHAT IT DOES NOT

**AUTHORIZES:** building the experiment · paper-running it · **setting its sizing tier.**

**DOES NOT AUTHORIZE: live capital. Ever, on its own.**

**Sample gate B1 is unchanged** — it still requires **n ≥ 100 closed positions at T1 or T2**. T3
does not substitute for forward evidence and does not shorten the six-month clock. It answers a
narrower question: *is this worth the cost of running?* That is a real question and it now has a
real answer, but it is not the same question as *does this make money.*

*Marked for the redesign session: the 30–40% haircut band in T3.4 is a range, not a number, and
the two ends will disagree on marginal cases. Pick one, or make it structure-dependent.*

### K — EXPLICITLY WORTH ZERO
> Hours logged · years elapsed · lines of code · number of bots · documentation quality ·
> infrastructure sophistication (VPS, recorders, backups, dashboards) · roadmaps · Reddit
> consensus · the owner's conviction · *"my own desire to give an encouraging answer."*

**Where the fleet stood at audit: 1.5 of 22 gates passed. Confidence score 9/100.** The only
passes were D1 (max DD known) and E1 (pass for the concept, fail for the implementation).

---

## 5. System II — the readiness board (G1–G6)

Per bot, **grain = condor (legs summed), not leg.** Six *ordered* gates: the first RED gate is
the named blocker. `●` pass · `○` fail · `·` pending.

**Ladder:** INCUBATE → VALIDATE → CANDIDATE → LIVE-READY (LIVE = real capital).
**Controls and mirror-watch bots are flagged non-graduating** — they cannot go live by design.

| Gate | Criterion | Threshold |
|---|---|---|
| **G1** | Clean data — no strike-bug, single-sided excluded | binary |
| **G2** | Sample | **≥ 20 clean condors** |
| **G3** | Edge — Exp(R) > 0 **and bootstrap 95% CI lower bound > 0** | 3,000 resamples, seed 7. Reports *"~N more trades"* when the CI still includes zero |
| **G4** | Risk — maxDD-R within cap | **maxDD-R ≥ −5.0**. ⚠️ The RoE **$** cap is an unfilled `<FILL>`, so half of G4 is permanently pending |
| **G5** | Compliance — instruction-mirror | **≥ 90% over ≥ 5 graded days.** Under 5 days it stays **pending, never a false pass** |
| **G6** | Robustness — OOS half-split both halves positive, and **≤ 60%** of positive R in any single year | n < 20 → N/A |

> ### ⛔ G5 IS THE GATE THAT LIED
> G5 scored **100% instruction-compliance on five consecutive graded days while the champion's
> PT25 had generated zero orders for a month.** It was measuring fidelity to `bots_config.csv`,
> a hand-written record wrong on 3 of 4 audited bots. The gate worked exactly as specified; the
> specification was the problem.
>
> **In v2, G5 may only read `bots_config_v2.csv`, which is written from capture.** With that
> file absent, `daily_brief.py` runs **CONFIG-BLIND and grades nothing** — G5 stays pending
> rather than passing. A pending gate is honest; a passing gate built on a false record is not.

**The legacy "≥15 clean post-fix condors" go-live gate is retired.** It was declared cleared at
"18/15" — a count that silently dropped 11 positions; the true post-fix epoch is 29 positions,
−$5,455, **Exp(R) −0.0383**. G2's ≥20 supersedes it. Do not reinstate a 15-condor bar.

---

## 6. The R methodology

**R = pnl ÷ capital-at-risk**, so allocation and contract size cancel out.
**Expectancy = (Win% × AvgWin_R) − (Loss% × AvgLoss_R)**, after costs.

**The unit of account is the POSITION** — a condor is its two spread rows paired by `trade_id`.
`trades.csv` carries 1,380 rows = 934 positions: a row is a *leg* for two-legged spreads and a
*whole position* for `ironcondor` / `ironbutterfly` / debit rows.

**Condor risk = the LARGER SIDE**, because a condor can only lose one side. This is the audit's
one flagged *stricter* revision, and it is correct: summing both sides understates
return-on-risk and flatters Exp(R) toward zero.

### 6.1 Labelling law — non-negotiable
**Always label the unit.** Exp(R) with no unit label is untrustworthy: the champion's post-fix
window is **−2.5% per leg raw, −3.8% per condor raw, and −1.7% per condor ex-artifact** — three
numbers for one window, and only the last means anything. Write *"per condor, ex-artifact"* or
*"per leg, raw"*, every time.

**Say "positions" or "condors", never a bare count.** The Fortress pre-June window is *30 rows
and 21 condors*; the champion's post-fix window is *47 rows and 29 condors*. Both pairs describe
the same trades.

### 6.2 ✅ RESOLVED 2026-07-31 — the denominator now matches the rule

**Was:** `scripts/report.py` built its condor series with `c["risk"] += fl(t["risk"])` — it
**summed both sides**, precisely the denominator the audit identified as wrong and replaced.
Board gates G3 and G4, and every Exp(R) in `STATUS.md`, ran on the flattered figure while four
documents asserted the larger-side rule.

**Now:** `c["risk"] = max(c["risk"], fl(t["risk"]))`. Andy's ruling, executed 2026-07-31.

`max()` is correct for every structure, not only condors: two paired spread rows give the larger
side (the real max loss); a single `ironcondor` / `ironbutterfly` / debit row gives itself; a
single-sided spread gives its own risk. **It is a no-op everywhere except legged iron condors,
which is exactly where it should bite.**

**Timing was chosen so nothing live moved.** The working ledger is empty (n=0), and the archive
ledger stays **frozen as-computed** — it is not recomputed. The change affects reporting from
Day-0 forward.

**Receipt: `data/receipts/r-denominator-fix.txt`**, old-vs-new across every bot. The headline:

| | n | OLD (sum) | NEW (larger side) |
|---|--:|--:|--:|
| **`IC-SPX-FastPT25-S2`** (clean post-fix condors) | 18 | −2.9549% | **−5.8293%** |

> **This is not a uniform haircut, it is the removal of one.** Magnitudes roughly double on
> legged ICs because the two sides carry similar risk — **losers get more negative and winners
> get more positive.** `IC-SPX-Fortress-Defang` goes +1.39% → **+2.74%**; the champion goes
> −2.95% → **−5.83%**. Anything quoting a pre-2026-07-31 condor Exp(R) is quoting the flattered
> number and should be restated or dropped.

### 6.3 Compare by R — never dollars, never win rate
- Raw P/L is uninterpretable across bots of different size (audit gate C4).
- **Win rate is a trap.** Credit sellers hit 85–95% until they don't. `oa-mirror-reference.md`
  §3.1 lists it under *"traps that look good and mislead."*
- **Instance profitability beats trade win rate** — the fraction of bot *instances* that are
  profitable, not the fraction of *trades*. On record: 3DTE **91.3% trade WR vs 46% instance
  profitability**; ORB **81.7% vs 55.5%**. This is the single most clarifying distinction in the
  project's own standards.
- **Bootstrap 95% CI replaces the t-stat** on the readiness board; the t-stat blows up for
  low-variance grinders and must not be ranked on alone.
- **Breakeven-WR buffer** is the useful WR derivative: `breakeven_WR = avg_loss ÷ (avg_loss +
  avg_win)`, and `buffer = current_WR − breakeven_WR`.

### 6.4 The data-mining sanity check
Verify `WR × avg_win − (1−WR) × avg_loss ≈ reported Avg P/L`. **A clean match means no
data-mining fingerprint.** A mismatch means the reported figures were assembled, not measured.

### 6.5 The impossible-fill detector rule — LOSS-SIDE ONLY, per leg
*(Lifted verbatim-in-substance from the retired `current-state.md`, 2026-08-03. The fixture and
validation live in `scripts/execution_audit.py --validate`, assertions V1–V4.)*

- **The rule is `pnl < −risk`, never `|pnl| > risk`.** A loss beyond max loss is structurally
  impossible for a defined-risk spread; a *gain* beyond recorded risk is legal (a debit spread can
  return more than its debit; a high-credit IC can beat its recorded risk). The absolute-value rule
  adds **exactly two false positives on clean wins** — T00038 and T00339 — and nothing else (proven
  load-bearing by assertion V4).
- **It runs per LEG, and that does not contradict §6's unit-of-account.** §6 fixes the *position* as
  the unit of expectancy; this is a *structural integrity* check on one vertical spread's own
  max-loss guarantee, a per-spread property. Netted to the condor, T00845 vanishes.
- **The frozen fixture is two rows**: `T00147` (R −1.63; mechanism: Cleanup priced at Market — this
  is correction A1) and `T00845` (R −1.10; logged C4, deliberately uncorrected — immaterial, no
  diagnosed mechanism). The detector must reproduce both and stay silent on the two wins.
- **Second, independent corroboration**: `FILL_WORSE_THAN_MAE` — an exit filled outside the
  position's own recorded price path. It finds T00147 with no risk column and no config (filled 4.81
  credits beyond the worst mark; next-worst of 1,232 closed rows is 0.91), corroborating the
  Market-pricing mechanism from the data alone.

---

## 7. Kill criteria — per bot, R-based, pre-registered

**RETIRED 2026-07-31 (Andy): the fleet-wide "rolling-30 win rate < 75%" criterion.**

It was never the right bar. A 0DTE PT scalper wins small often and loses bigger rarely; the
champion sat at **~43% over 221 positions** and the rule's only observed effect was to fire and
be argued with. The audit's §3.5 finding is the reason it had to go, and it is worth quoting
because it is about people, not statistics:

> *"When a pre-committed rule fired against a system the owner is attached to, the rule was
> re-opened for debate rather than executed. Every one of these deferrals happens to keep a
> losing bot running. None of them ever went the other way. **No strategy the owner built
> himself has ever been killed by a triggered rule.** That asymmetry is the whole tell."*

**Replacement, effective Phase 4:** every active bot carries **its own R-based kill criterion**,
written into its pre-registration entry **before it restarts**, and fired in code.

Design constraints for those criteria:
- **Expressed in R**, never in dollars and never in win rate.
- **One per bot**, matched to that bot's structure and role — a control's criterion is not a
  candidate's.
- **Falsifiable from data the daily loop already produces.** A criterion needing evidence
  nobody collects is not a criterion.
- **Fired automatically.** Per audit §5.5: *"Kill triggers must fire in code and toggle bots off
  without a human in the loop… `report.py` already has the hooks; wire them."*
- **A fired trigger not executed within 48 hours is itself a kill condition.**

**No fleet-wide win-rate bar is reinstated in any form.**

---

## 8. Pre-registration

**Five required fields:** hypothesis · kill criterion (R-based, §7) · sample target · review
date · config-capture hash.

**Plus a per-bot max-loss line** — carried as an open item from Phase 1; the `<FILL>` blanks in
`rules-of-engagement.md` are an active H3 failure and a time-box start condition.

**Written BEFORE the bot starts. No entry, no restart.** All ≈18–20 active bots need one,
**including the nine untouched**. Drafted during the pre-Day-0 build window so **Day-0 is
signing, not authoring**; each entry dated before its bot's restart.

**A behaviour-changing modification must be pre-registered as such** — not slipped in as
instrumentation.

**Why the discipline is load-bearing:** *"Pre-commit kill thresholds in writing before data
arrives"* is the project's own **highest-leverage discipline anchor** — rules written after
seeing data get rationalised away. Parameters are frozen in a dated, committed file for the
measurement window; **a change resets the clock to day zero.**

**Proposed enforcement:** mirror the template VERSION into a `BUILD_ID` bot input so the running
bot self-reports which pre-registration it is executing, and have the nightly script **assert
`BUILD_ID` == the version named in the current pre-registration file, failing loudly on
mismatch**. Assert live input *values* against pre-registered values, not just their presence.
⚠️ Per its own source: **if that assert is not built, do not build the BUILD_ID mechanism** — a
self-report nobody checks is worse than none.

---

## 9. Two things in the record that do not add up

Recorded rather than smoothed over, because a standards document that hides its own seams is
the thing this project keeps failing on.

**9.1 The T3 gate does not exist.** §2.1 item 3. T3 evidence currently has no home.

**9.2 ✅ CORRECTED 2026-07-31 — the "third-party switch" was a garbled transcription.**

The overrule banner said the audit recommended *"switch to a third-party platform."* No such
recommendation exists in the audit body. **Andy's correction: "third-party switch" meant the
GO-LIVE SWITCH held by a third party — it garbled in transit into sounding like a vendor change.**

**What was actually declined** is audit §5.5 items 6–7:

- **Custody separation** — *"Any live account is opened and funded by someone other than the
  owner. The owner gets read-only credentials… This is the single most important control and it
  is non-negotiable."*
- **Independent go-live authority** — *"The decision to move from paper to live is **not the
  owner's to make.** It belongs to a named third party… The owner may present evidence; he does
  not hold the switch."*

**The reason, recorded 2026-07-31: go-live authority stays with Andy.** The substitutes are
**external review of `rules-of-engagement.md`** and **the pre-registration discipline** (§8) —
kill criteria written before data arrives and fired in code.

> **Stated plainly, because the audit's §3.5 finding is about exactly this risk:** the declined
> control existed to solve the problem that *"no strategy the owner built himself has ever been
> killed by a triggered rule."* Declining it means the substitutes have to carry that weight
> alone. **That is what makes §7's "fired in code, without a human in the loop" load-bearing
> rather than a nicety** — it is the only remaining mechanism that can stop a bot the owner is
> attached to. If kill triggers end up requiring a human decision after all, this overrule
> should be reconsidered.

**On the redesign agenda for optional reconsideration** (§10 item 7).

---

## 10. What a redesign should fix

In the order I would take them.

1. ~~Resolve the R denominator~~ — **CLOSED 2026-07-31: fixed** (§6.2). Receipt in
   `data/receipts/r-denominator-fix.txt`.
2. ~~Define or delete the T3 weaker gate~~ — **CLOSED 2026-07-31: defined** (§4.5). The 30–40%
   haircut in T3.4 is still a range rather than a number — pick one, or make it
   structure-dependent.
3. **Reconcile the two gate systems** (§3). Nothing anywhere maps audit A–K onto board G1–G6.
   They measure different things at different grains, which is fine — but a bot can be
   LIVE-READY on the board while its pillar fails audit gate B, and nothing currently notices.
4. **Fill the `<FILL>` blanks** — the RoE $ cap (board G4) and the four in
   `rules-of-engagement.md` (audit H3). Both are permanent-pending until someone writes a number.
5. **Decide what the n=0 cutover does to the gates.** Every bot restarts at zero on Day-0, so
   B1 (≥100 positions) and B2 (≥6 months) are unreachable for roughly six months **by
   construction, and that is accepted and priced in** (`build-plan.md` §1). The question a
   redesign must answer is what evidence *is* admissible in the interim — because the honest
   answer today is "almost none", and a fleet running for six months on inadmissible evidence
   needs that stated rather than discovered.
6. **Score instance profitability alongside Exp(R)** (§6.3). It is the project's own most
   clarifying metric and it appears in no gate.
7. **Reconsider custody separation and independent go-live authority** (§9.2), optional. Both
   were declined 2026-07-31 with go-live authority staying with Andy. **The trigger for
   reopening this is specific:** if kill criteria end up needing a human decision rather than
   firing in code, the substitute controls are not carrying the weight the declined ones were
   meant to carry.

---

*Sources: `docs/independent-audit-2026-07-27-precommitment-ledger.md` §§A–K (source of record
for the tiers and gates) · `docs/independent-audit-2026-07-27.md` §§1–6 (abridged, plus §3.5 and
§5.5) · `docs/oa-mirror-reference.md` §3 (the project's own prior standards, which the audit
anchored to) · `docs/rebuild-audit-2026-07-29.md` · `scripts/report.py` (the board gates, as
implemented) · `CLAUDE.md` §4 · `docs/build-plan.md` §5. Both audit files carry PARTIALLY
OVERRULED banners — machinery adopted, verdicts overruled (§1).*
