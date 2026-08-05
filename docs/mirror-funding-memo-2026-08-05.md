# Mirror funding memo — 2026-08-05

*Written so the Day-0 funding decision, made post-downgrade on a weaker model, is a **read**, not an
analysis. Sprint Rank 8 / Task 9.*

> ⚠️ **Date deviation, stated because dates in this repo are lineage records.** The sprint's Task 9
> prompt is written for **2026-08-07** and names the output `mirror-funding-memo-2026-08-07.md`.
> It is being run **2026-08-05**, two days early, because the Day-0 audit
> (`docs/day0-audit-2026-08-05.md`, F-34) made mirror funding a **Day-0 Step-2 dependency** rather
> than a standalone deliverable. **This file is dated for the day it was written.** No figure in it
> is affected.

> ## ⛔ ALL RECOMMENDATIONS ARE DRAFT. Andy accepts, amends or rejects. Nothing here funds anything.

---

## 0. Bottom line — the decision as posed cannot be made, and that is the finding

**Zero of ten mirrors clears the evidence bar. Not one.**

`CLAUDE.md` §4: *"Nothing below T2 with **n≥100 positions / 6 months / a regime change** supports a
live-capital or growth decision."*

| Limb | Mirrors clearing it | Best in fleet |
|---|---|---|
| **n ≥ 100 positions** | **0 of 10** | `3DTE $140-$350`, **n=46** |
| **≥ 6 months** | **0 of 10** | `Nigiri-Paper-v1`, **83 days** (2.7 months) |
| **spans a regime change** | not assessable — the whole window is 2026-04-20 → 2026-07-27, **98 days** | — |

The seven live mirrors hold **n=128 positions between them.** The largest single mirror is less than
half the bar.

**So: there is no FUND verdict available for any mirror at Day-0.** Every live mirror below is
**WATCH**. That is not caution — it is the evidence law applied literally, and it is the single most
useful thing this memo can hand a weaker model, because it converts an analysis into a lookup.

### The asymmetry that makes this memo useful anyway

The bar gates **live-capital and growth** decisions. **It does not gate a decision to withhold
capital.** Declining to fund risks nothing, so DO-NOT-FUND and KILL are available on weaker evidence
than FUND is. **That asymmetry is where every actionable verdict in this memo comes from** — and it
is worth stating explicitly in the runbook, because the natural weak-model error is to read
"insufficient evidence" as "therefore do nothing," which for an already-running bot means
**continue**, which is a capital decision made by default.

---

## 1. Scope — 10 in the baseline, 7 in the funding decision

`data/mirror_baseline.csv` holds **10** mirrors, **174 positions**, zero excluded.
`build-plan.md` §2C funds **7** — the live mirrors in the leave-in-place nine. Three are `OFF` at
capture and are **not** funding candidates:

| Mirror | Status | Disposition |
|---|---|---|
| `1-45pm-Sandwich-Paper-v1` | **OFF** | Out of funding scope |
| `Opening Range Breakout 60m` | **OFF** | Out of scope — **being archived** (`build-plan.md` §2A; ⚠️ not to be confused with `60min-ORB-10W-Paper-v1`, which stays live) |
| `Weekly-IB-SPY-Paper-v1` | **OFF** | Out of funding scope |

They are analysed below anyway, because two of them carry the finding that clarifies the other two.

---

## 2. The record — per mirror, on the `ror` basis, n on every figure

R = `pnl / risk`, **per POSITION**. No condor roll-up: the mirror pillar is heterogeneous — long
calls, broken-wing flies, ORB breakouts — and `build_mirror_baseline.py` states there is no single
correct multi-leg roll-up across them. `ror == pnl / risk` verified **1,386/1,386 rows, 0 mismatches**
(`oa-export-schema.md`), so the `ror` column and this computation are the same number.

**Verification.** Every figure below was computed this session from
`data/captures/oa_export_positions_2026-07-30.csv`, sha `dca69adaf771f064…`, **which matches the
hash the anchor itself cites.** Recomputing `n_with_R`, `mean_R`, `median_R` and `win_rate`
reproduced the anchor **exactly on all 10 mirrors, zero mismatches.** The anchor was read only; its
sha is unchanged at `cdceb0a8d444e570…`. Columns beyond those four are **new, derived this session**
— the anchor does not carry dispersion or drawdown.

### The seven live mirrors (funding candidates)

| Mirror | n | mean R | median R | sd R | worst R | **maxDD (R)** | sum R | win % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `3DTE $140-$350` | 46 | +0.0156 | +0.0423 | 0.1545 | **−1.0000** | **1.0000** | +0.718 | 95.7 |
| `Nigiri-Paper-v1` | 38 | +0.0102 | +0.0102 | **0.0065** | **0.0000** | **0.0000** | +0.387 | 94.7 |
| `Trendy-Paper-v1` | 15 | −0.0365 | +0.0405 | 0.2822 | −0.9842 | 1.2877 | −0.548 | 80.0 |
| `60min-ORB-10W-Paper-v1` | 12 | −0.0328 | +0.0786 | 0.3885 | −1.0000 | 1.0000 | −0.394 | 83.3 |
| `Friday 14 DTE Broken Wing IB (B-70)` | 7 | +0.0893 | +0.0773 | 0.0337 | +0.0634 | 0.0000 | +0.625 | 100.0 |
| `QQQ long call` | 6 | +0.3401 | +0.3045 | 0.1010 | +0.2521 | 0.0000 | +2.040 | 100.0 |
| `Tasty Condor` | 4 | +0.3468 | +0.3794 | 0.0812 | +0.2266 | 0.0000 | +1.387 | 100.0 |

### The three OFF mirrors (not funding candidates; analysed for contrast)

| Mirror | n | mean R | median R | sd R | worst R | maxDD (R) | sum R | win % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `Weekly-IB-SPY-Paper-v1` | 18 | −0.0770 | +0.0217 | 0.3331 | −0.6054 | **3.2359** | −1.386 | 50.0 |
| `Opening Range Breakout 60m` | 19 | −0.1107 | +0.0676 | 0.3778 | −1.0000 | 2.3998 | −2.103 | 68.4 |
| `1-45pm-Sandwich-Paper-v1` | 9 | −0.4125 | **−1.0000** | 1.0489 | −1.0000 | **5.4667** | −3.712 | 22.2 |

---

## 3. ⛔ The finding that changes a verdict: `QQQ long call`'s record is structurally incomplete

**`QQQ long call` is the best-looking mirror in the fleet** — mean R **+0.3401**, **6 of 6** wins,
**zero drawdown**, sum R **+2.040**. It is also **the bot carrying the open exposure.**

**The export contains only closed positions. All 174 rows have a close date; there are zero open
rows.** So the **4 open `QQQ long call` positions — ~$13K risk, ~−$10.8K unrealized** at the
2026-07-30 capture (`build-plan.md` §3) — are not filtered out of the baseline. **They were never in
the source.** The baseline cannot see them and does not claim to.

**Scale of the omission, stated as an estimate and labelled as one:**

| | Recorded (closed, n=6) | Open (n=4, not in baseline) |
|---|---:|---:|
| P/L | **+$5,967** | **≈ −$10,800** unrealized |
| Risk | — | ≈ $13,000 |

⚠️ **ESTIMATE, not a computed figure — the per-position open data is not in any file I read.** The
$13K / −$10.8K figures are quoted from `build-plan.md` §3. On those figures the open book sits at
roughly **−0.83R aggregate**; adding four positions at that level to a sum R of +2.040 gives a
lifetime sum R near **−1.3 across 10 positions, i.e. a mean near −0.13.** **The sign flips, and the
100% win rate becomes 6-of-10.**

**This does not make the baseline wrong.** It is a correctly-built closed-position anchor and its
receipt says so. It makes **one specific inference** wrong — reading `QQQ long call`'s record as
evidence of the strategy — and that is precisely the inference a Day-0 funding decision would make.

**The same caveat applies, far more mildly, to `Tasty Condor`:** 1 open position at ≈ **+$328**, on a
record of n=4. Directionally favourable, and n=4 supports nothing either way.

⛔ **Consequence for Day-0:** the ride-or-close call on those five positions is **Andy's** — this
memo references it and does not decide it (`build-plan.md` §3; runbook §4 Step 2). But
**the funding verdict for `QQQ long call` must not be taken before that call is made and executed**,
because the call determines whether the −$10.8K becomes a realised part of the record or not. The
Day-0 audit's **F-34** already flags that Step 2 requires the decision *logged* but never *executed*,
while Step 3 then arms this very bot.

---

## 4. The positive-median / negative-mean four — narrowed to two, and neither is decidable

The known finding: four mirrors **win often and lose money.** Confirmed exactly — `60min-ORB-10W-Paper-v1`,
`Trendy-Paper-v1`, `Opening Range Breakout 60m`, `Weekly-IB-SPY-Paper-v1`.

**Two of the four are already OFF, and they are the two where the tail is structural.** The
discriminator is what happens to the mean when the single worst position is removed:

| Mirror | n | wins | losses | mean win R | mean loss R | worst R | **mean R ex-worst** | Sign flips? | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| `60min-ORB-10W-Paper-v1` | 12 | 10 | 2 | +0.1260 | −0.8269 | −1.0000 | **+0.0551** | **YES** | **single-event** |
| `Trendy-Paper-v1` | 15 | 12 | 3 | +0.0640 | −0.4385 | −0.9842 | **+0.0312** | **YES** | **single-event** |
| `Opening Range Breakout 60m` | 19 | 13 | 6 | +0.1028 | −0.5731 | −1.0000 | **−0.0613** | no | **structural** |
| `Weekly-IB-SPY-Paper-v1` | 18 | 9 | 9 | +0.2153 | −0.3693 | −0.6054 | **−0.0459** | no | **structural** |

**Read the table this way.** For the two OFF mirrors, removing the worst trade **does not** rescue
the mean — the losses are repeated (6 of 19; 9 of 18, a 50% win rate) and the negative mean is a
property of the strategy, not of one bad day. For the two **in funding scope**, the entire negative
mean is **one max-loss position each**, and removing it flips both positive.

⚠️ **"Single-event" is not "fine."** It means the evidence is consistent with both a healthy strategy
that took one bad loss **and** a strategy whose true loss frequency simply has not shown up yet. At
**n=12** and **n=15**, with **2** and **3** losing positions respectively, those two hypotheses are
not separable. **The honest verdict is UNDETERMINED, and it is undeterminable at this n** — which is
the same place the evidence law puts them anyway.

**What would settle it:** for `60min-ORB-10W-Paper-v1`, roughly **20–25 further positions** would
show whether −1.0R events arrive at ~1-in-6 (structural, matching the OFF pair) or ~1-in-20+
(single-event). For `Trendy-Paper-v1`, roughly **25–30**. Both are far below the n≥100 funding bar
and would settle only the tail question, **not** the funding question.

---

## 5. Two risk shapes the mean does not show

**`3DTE $140-$350` — the largest sample, and the one whose whole question is the tail.**
95.7% win rate, mean win **+0.0411R**, and one **−1.0000R** loss. **One max loss erases ~24 average
wins.** With n=46 the strategy has seen exactly **2** losing positions. This is a premium-collection
shape: the mean is a small positive number sitting on top of a tail that has barely been sampled, and
its maxDD of **1.0000R** is a single event, not a sequence. It is the closest mirror to fundable and
the one where n≥100 matters most — the extra 54 positions are almost entirely about observing the
tail frequency.

**`Nigiri-Paper-v1` — the most consistent record in the fleet, at trivial magnitude.**
**Never a losing position** across n=38: worst R is **0.0000** (two scratches), maxDD **0.0000**, sd
**0.0065** against a mean of **+0.0102**. Mean and median are identical to four decimals. That is an
extraordinarily tight distribution — and it returns **+0.0102R per position**, so the entire lifetime
result is **+0.387R across 38 positions.** ⚠️ A record with no losses at all should raise the
question of whether the loss mode is simply outside the sample window rather than absent; n=38 over
83 days cannot answer it.

---

## 6. DRAFT verdicts

**No FUND verdict is available for any mirror.** The verdicts below distinguish *how* each is
watched, and where the asymmetry in §0 permits an actionable call.

### The seven live mirrors

| Mirror | n | **DRAFT verdict** | Rationale |
|---|---:|---|---|
| `3DTE $140-$350` | 46 | **WATCH — priority 1, nearest to fundable** | Largest n, positive on both mean and median, disciplined risk shape. Fails only on sample. **Reaches n=100 in ~3.2 months** at its observed rate — the only mirror that gets there quickly |
| `Nigiri-Paper-v1` | 38 | **WATCH — priority 2** | Second-largest n; the tightest distribution in the fleet. Reaches n=100 in ~4.4 months. ⚠️ Magnitude is tiny — confirm the edge survives real fills before it is ever sized |
| `Trendy-Paper-v1` | 15 | **WATCH — tail undetermined** | Negative mean is one max-loss event; flips positive without it. n=15 cannot separate the hypotheses |
| `60min-ORB-10W-Paper-v1` | 12 | **WATCH — tail undetermined** | Same shape as Trendy. ⚠️ Do not confuse with `Opening Range Breakout 60m`, which is structural and being archived |
| `Friday 14 DTE Broken Wing IB (B-70)` | 7 | **WATCH — no verdict possible** | 7 of 7 wins, zero drawdown, and n=7. A perfect record at n=7 is not evidence |
| `QQQ long call` | 6 | ⛔ **WATCH — RECORD INCOMPLETE. Do not read the +0.3401** | §3. The 4 open positions at ≈−$10.8K are not in the baseline and would flip the sign. **Verdict blocked until Andy's ride-or-close is executed** |
| `Tasty Condor` | 4 | **WATCH — no verdict possible** | n=4, plus 1 open position (≈+$328) not in the baseline |

### The three OFF mirrors — where the asymmetry permits a call

| Mirror | n | **DRAFT verdict** | Rationale |
|---|---:|---|---|
| `1-45pm-Sandwich-Paper-v1` | 9 | **KILL (draft)** | **Median R = −1.0000** — the median position is a total loss of risk. 22.2% win rate, maxDD **5.4667R**, sum R −3.712. Withholding capital needs no T2 evidence, and nothing here argues for revival |
| `Opening Range Breakout 60m` | 19 | **KILL — already dispositioned** | Structurally negative (mean ex-worst −0.0613, 6 losses of 19). Already slated for archive; this memo concurs and adds no new action |
| `Weekly-IB-SPY-Paper-v1` | 18 | **DO NOT FUND (draft)** | Structurally negative; 50% win rate with mean loss −0.3693 against mean win +0.2153. A coin flip with a worse loss than win |

---

## 7. ⛔ The structural problem Andy has to rule on: for four of seven, the bar is unreachable

Days to reach **n≥100** at each mirror's own observed trade rate:

| Mirror | n | positions/day | needs | days to n=100 | **≈ months** |
|---|---:|---:|---:|---:|---:|
| `3DTE $140-$350` | 46 | 0.561 | +54 | 96 | **3.2** |
| `Nigiri-Paper-v1` | 38 | 0.458 | +62 | 135 | **4.4** |
| `60min-ORB-10W-Paper-v1` | 12 | 0.250 | +88 | 352 | **11.6** |
| `Trendy-Paper-v1` | 15 | 0.197 | +85 | 431 | **14.1** |
| `Friday 14 DTE Broken Wing IB (B-70)` | 7 | 0.111 | +93 | 837 | **27.5** |
| `QQQ long call` | 6 | 0.102 | +94 | 924 | **30.4** |
| `Tasty Condor` | 4 | 0.103 | +96 | 936 | **30.7** |

**Four of the seven live mirrors need more than a year — three of them more than two and a half
years — to reach n≥100.** They are low-frequency by construction: 14-DTE broken wings and long calls
do not produce 100 positions quickly, and no amount of patience fixes that on a useful horizon.

**Under the rule as written, those four are permanently un-fundable.** That is a real consequence and
it is not obviously the intent — the n≥100 bar was set against 0DTE cadence, where 100 positions is a
few months. **This is a decision, not a finding, and it is Andy's:**

- **(a) Accept it** — the low-frequency mirrors stay watch-only indefinitely. Clean, consistent, and
  it permanently forecloses a category.
- **(b) A time-based equivalent for low-frequency strategies** — e.g. 6 months **and** n≥30 — which
  would make `Trendy` and `60min-ORB` assessable in 2026-11 and `Friday 14 DTE` later. ⚠️ This is a
  **weakening of the evidence law** and should be written as one, with its rationale, not slipped in.
- **(c) Fund nothing from the mirror pillar, ever** — treat mirrors as a permanent research surface
  and route capital only to bots built under pre-registration.

The **6-month limb is reachable for all seven** if they keep running: the earliest crossings are
`Nigiri` **2026-10-20** and `3DTE` **2026-10-21`; the latest is `Tasty Condor` **2026-12-17**. So
under any reading, **the first date a mirror could clear the bar is late October 2026** — which is
well after Day-0, and means **no mirror funding decision is due at Day-0 at all.**

---

## 7a. ⏸ DRAFT AMENDMENT SLOT — a cadence-scaled graduation bar for the mirror class

> ## ⏸ DRAFT. NOT IN FORCE. NOT APPLIED ANYWHERE.
> **Ruled 2026-08-05:** *"the n≥100 graduation bar was set against 0DTE cadence and is unreachable
> for the multi-week mirrors. Draft a cadence-scaled alternative for the mirror class as a DRAFT
> amendment slot in the mirror memo — **do not apply it to evidence-standards; I sign it
> separately.**"*
>
> ⛔ **`docs/evidence-standards.md` is UNTOUCHED and the n≥100 bar remains in force as written.**
> Nothing in this section governs anything until Andy signs it. It is drafted here so the design
> exists while there is capacity to reason about it, and so the signature is a read.

### The problem this is scoped to — and the problem it is NOT

**Scoped to:** `CLAUDE.md` §4's **n≥100 positions** limb, **for the mirror class only.** At their own
observed cadence four of the seven live mirrors need over a year to reach it and three need over two
and a half (§7). The bar was calibrated against 0DTE cadence, where 100 positions is a few months. A
14-DTE broken wing and a long call cannot produce 100 positions on any useful horizon, so **under the
rule as written they are not slow to graduate — they are permanently un-fundable**, which is a
consequence of the arithmetic rather than of anything observed about the strategies.

⛔ **NOT scoped to:** the 6-month limb, the regime-change limb, the T1–T5 tiering, or any other
pillar. **This is not a general relaxation of the evidence law and must not become one.** If it is
signed, it should be written as a **named carve-out with its own tier label**, not as an edit to the
general bar — so that a future reader sees a scoped exception rather than a weakened rule.

### What the n≥100 bar actually buys, and why counting positions is a proxy for it

A large n is not wanted for its own sake. It buys **enough independent observations of the loss tail
to estimate how often the tail arrives.** For a 0DTE premium-collection bot with a ~95% win rate,
n=100 delivers roughly 5 losing observations — which is the real quantity, and it is thin even then.
`3DTE $140-$350` makes the point inside this very memo: **n=46, and exactly 2 losing positions.**

**So the cadence-scaled bar should count what the big-n bar was proxying for: losses, calendar, and
a floor — not raw position count.**

### Tier M — the draft

**Class membership.** A bot is **Tier M** if it is in the OA-Mirror pillar **and** its observed
cadence is **< 0.30 positions per calendar day**, measured over **≥ 60 days**.

*Under this test, `3DTE $140-$350` (0.561/day) and `Nigiri-Paper-v1` (0.458/day) are **NOT** Tier M —
they stay on the standard n≥100 bar and reach it in 3.2 and 4.4 months respectively. **The draft
weakens nothing for any bot that can meet the existing bar.** The other five are Tier M.*

**Graduation to a live-capital decision requires ALL FOUR:**

| | Criterion | Why |
|---|---|---|
| **M1** | **n ≥ 30 positions** | A hard floor. Below this, dispersion is not estimable at any cadence and no drawdown figure means anything |
| **M2** | **≥ 9 months of calendar history** | Replaces the 6-month limb **upward**, not downward. Low cadence means fewer independent observations per unit time, so the calendar has to do more of the work |
| **M3** | **≥ 6 losing positions observed** — **OR** the structure is **defined-risk** and its maximum loss has been **observed at least once** | The substantive replacement for n≥100. This is what the big-n bar was proxying for, targeted directly |
| **M4** | The **worst observed drawdown in R** is stated, and **explicitly accepted by Andy at sizing time** | Converts an unbounded unknown into a named, accepted number |

**M3's carve-out is the load-bearing clause and it needs Andy's eye.** Without it, a bot that has
never lost — `Nigiri-Paper-v1` has **zero** losing positions in n=38, and three of the five Tier-M
mirrors have zero — could never graduate at any n, which is perverse. With it, a **defined-risk**
structure (an iron condor, a broken-wing butterfly, a long call) is allowed to substitute *"the
maximum loss is bounded by construction and I have seen it once"* for *"I have seen six of them."*
⚠️ **The carve-out is only sound where max loss is genuinely bounded by structure.** It must not be
extended to undefined-risk positions, and the memo takes no position on borderline cases such as a
stop-managed ORB breakout, where the bound is an execution promise rather than a structural fact.

### What each mirror would need under the draft

*Dates assume the fleet restarts at Day-0 ≈ **2026-08-15** and resumes each bot's own observed
cadence. Nothing has traded since 2026-07-27, so the rate clock restarts — these are projections from
a resumed clock, not extrapolations of a running one.*

| Mirror | Tier | cadence /day | n now | M1 (n≥30) met | M2 (9 mo) met | M3 losses now | **Graduates ≈** | vs current rule |
|---|---|---:|---:|---|---|---|---|---|
| `3DTE $140-$350` | — standard | 0.561 | 46 | n/a | n/a | 2 | **2026-11** (n≥100) | unchanged |
| `Nigiri-Paper-v1` | — standard | 0.458 | 38 | n/a | n/a | **0** | **2026-12** (n≥100) | unchanged |
| `Trendy-Paper-v1` | **M** | 0.197 | 15 | 2026-10-30 | **2027-01-27** | 3 | **2027-01** | 2027-10 → **9 mo earlier** |
| `60min-ORB-10W-Paper-v1` | **M** | 0.250 | 12 | 2026-10-26 | **2027-02-11** | 2 | **2027-02** | 2027-08 → **6 mo earlier** |
| `Friday 14 DTE Broken Wing IB (B-70)` | **M** | 0.111 | 7 | **2027-03-10** | 2027-01-26 | **0** → carve-out | **2027-03** | 2028-12 → **21 mo earlier** |
| `QQQ long call` | **M** | 0.102 | 6 | **2027-04-07** | 2027-01-23 | **0** → carve-out | **2027-04** | 2029-02 → **22 mo earlier** |
| `Tasty Condor` | **M** | 0.103 | 4 | **2027-04-24** | 2027-03-19 | **0** → carve-out | **2027-04** | 2029-03 → **23 mo earlier** |

**Net effect: the five Tier-M mirrors become assessable between January and April 2027, instead of
between August 2027 and March 2029.** The two that can already meet the standard bar are untouched.

⚠️ **"Graduates" means becomes ELIGIBLE FOR A DECISION — never "is funded."** Clearing Tier M makes a
mirror assessable; the verdict is still Andy's and still needs the analysis to support it. **And
`QQQ long call` carries the §3 caveat regardless of any bar:** its record cannot be read until the
open positions are resolved into it.

### Open questions Andy should settle when signing

1. **Is 9 months right for M2, or 12?** 9 crosses more than one quarterly regime; 12 crosses a full
   seasonal cycle and would push the whole Tier-M cohort to mid-2027.
2. **Is 6 the right number for M3?** It is chosen to be *some* multiple of the 2 losses `3DTE` has
   accumulated at n=46 — it is a judgment, not a derivation, and it should be labelled as one.
3. **Does the defined-risk carve-out extend to stop-managed strategies** such as
   `60min-ORB-10W-Paper-v1`? The memo's view is **no** — a stop is an execution promise, and this
   fleet has already paid for the difference between a promised exit and an executed one.
4. **Should Tier M carry its own tier label** (e.g. `T2-M`) so that a claim resting on it is visibly
   distinguishable from one resting on the full bar? The memo's view is **yes** — an exception that
   is invisible downstream is how a carve-out quietly becomes the rule.
5. **Does membership re-test?** If a Tier-M bot's cadence rises above 0.30/day it should presumably
   revert to the standard bar — but not retroactively, or a bot could lose a graduation it already
   holds.

---

## 8. What this means for Day-0

1. **Mirror funding is not a Day-0 decision.** Nothing clears the bar, and nothing can until late
   October at the earliest. Day-0's mirror action is: **re-arm the seven, keep them watch-only, size
   nothing.** That converts a judgment call into a lookup, which was the point.
2. ⛔ **`QQQ long call` is the exception that still needs Andy on the day** — not for funding, but
   because its 4 open positions are ~$13K of live legacy risk, its baseline record cannot see them,
   and Day-0 Step 3 arms the bot that holds them. **Ride-or-close first, then arm** — audit F-34.
3. **Two draft kills and one draft do-not-fund** are available now, all on OFF bots, all permitted by
   the §0 asymmetry. None requires Day-0 action.
4. **Add the "no verdict = do not fund" line to the runbook.** For an already-running bot,
   "insufficient evidence" silently means "keep going," which is a capital decision made by default.
   That is the failure mode this memo exists to prevent.
5. **§7 needs a ruling before late October**, not before Day-0 — but it is cheap to rule now while
   there is capacity to reason about it, and expensive to rediscover in three months.

---

## 9. Provenance

| Input | sha256 (first 16) | Read |
|---|---|---|
| `data/mirror_baseline.csv` | `cdceb0a8d444e570` | read-only; **unchanged after this session** |
| `data/captures/oa_export_positions_2026-07-30.csv` | `dca69adaf771f064` | matches the hash the anchor cites |
| `scripts/build_mirror_baseline.py` | `dd33ae56bdd4a1dc` | methodology only |
| `data/receipts/mirror-baseline.txt` | — | 10 mirrors · 174 positions · 174 with R · 0 excluded |

**Anchor cross-check: PASS.** `n_with_R`, `mean_R`, `median_R` and `win_rate` reproduced exactly for
all **10 of 10** mirrors from the source export. **The anchor was not recomputed, not overwritten,
and `--force` was not used.** Derived columns (sd, worst, maxDD, quantiles, tail decomposition,
trade rates) are new this session and are labelled as such throughout.

**Not done, deliberately:** no OA access, no git, no write to `data/`. The ride-or-close call on the
five open positions is referenced and **not decided**.
