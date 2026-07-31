# Is the instrumentation work worth doing? — decision memo

*Written 2026-07-29 · distilled from the session that produced `oa-setup-exploration-2026-07-29.md` and `oa-docs-research-2026-07-29.md` · companion to `approach-reset-2026-07-29.md` §4 and §6.5*

> Written because the reasoning existed only in chat. This is the argument for and against spending the hours, in one place, so the continue-vs-shelve question (reset doc Open Question 5) has something to be decided against.

---

## The case for

**1. It converts four months of runtime into evidence.** There currently is none. The audit's cause split is 66% `settings` / 26% `by_design` / 9% `oa_execution` — 84% of measured losses describe the build, not the strategy. The champion's G2 gate (18/15 clean condors) certified `ride+S2`, a configuration that never ran. `STATUS.md`, the readiness board, the hedge tournament and the daily brief all inherit that error. Instrumentation recovers nothing retroactively; it makes the *next* 100 positions answer a question instead of raising one.

**2. Detection latency: four months → one day.** Not abstract:

| Failure | What catches it | When |
|---|---|---|
| PT25 fired 0/47 (Pattern A) | Shadow PT monitor (C2) or backtest fingerprint diff (I1) | Position 1 |
| PT50 calls 0/15, puts 21/21 (Pattern B) | Exit Option Preset (D1) makes half-attachment unbuildable; per-side fire-rate assert catches the rest | Day 1 |
| Fortress stopped exiting 2026-06-12 | Heartbeat Event (B2) + Excessive Errors Failsafe check (K3) + exit-option re-assertion (C1) | Session 1 of 6 |

The Fortress case alone cost ~$9,700 across two sessions for the absence of a check that takes ~2 hours to build.

**3. The hedge question becomes answerable.** Open since March, currently unanswerable: two arms are the same arm (S1 ≈ Conditional, identical P/L on 73/86), one is mis-implemented (S3 is a %-of-credit stop, not a 50% max-loss stop), one runs in a different execution class (S3 = Exit Option, runs first; S1/S2/D = Monitors, run third), and none carries the declared Range075 filter. Shared automations + inputs make arms differ only by value. If the Touch Exit Option means underlying-touches-strike, the execution-class confound disappears entirely rather than being controlled for.

**4. Experiment rate.** Testing a threshold today: duplicate an automation, edit a node, hope nothing else moved. With inputs: type a number. Experiment rate is the only variable that sets learning speed.

---

## The case against — weigh this seriously

**Every arm in the matched-day standing has negative Exp(R):**

| Arm | Exp(R) |
|---|---|
| S3 | −0.0029 |
| S2 | −0.0095 |
| **Raw / no hedge** | **−0.0211** |
| S1 | −0.0260 |
| Conditional | −0.0308 |

Not one is positive, *including not hedging at all*. And the single mechanic confirmed to execute correctly — S2 on the champion — lost **−$3,285** over the post-fix window (−$6,285 raw, less the $3,000 6/11 artifact). The reset doc puts confidence that fixing everything yields a higher forward score at **~25%**, which is about right.

**So instrumentation can be a sophisticated way of not deciding.** Twelve hours of detector-building on a fleet whose measured expectancy is negative everywhere is a real risk, and "we need better measurement" is the most comfortable possible answer to "is this working?"

---

## The resolution

The negative expectancy is measured on bots that were running something other than what was believed. That makes it impossible to distinguish **a real edge failure** from **an execution artifact** — and those two have opposite correct responses.

That distinction is worth exactly **Phase 0 + Phase 1 (~5 hrs)**. It is *not* worth the full ~12 until those 5 have answered it. This matches the reset doc's own recommendation; nothing in the platform research changes it.

**Two things this does not do:**

- It does not make a losing strategy win. It makes the answer legible when it arrives.
- It is entirely wasted if the fleet stays off. Its whole value is making the next stretch trustworthy.

**If the lean is toward shelving, shelve — do not instrument first.** Instrumentation is only worth it conditional on intending to run the fleet again.

---

## What would change the calculus

| Finding | Effect |
|---|---|
| Touch Exit Option means underlying-touches-strike | Tournament rebuild gets much cheaper; raises the value of the 5 hrs |
| Backtest CSV export is real | I1 and I2 (ranks 2 and 6) become buildable; the ≥100-trade / ≥6-month bar can be cleared without live runtime, which weakens the "must run the fleet" precondition |
| The Excessive Errors Failsafe explains 6/12 | Fortress becomes a known, monitorable failure rather than an unexplained one — removes a reason to distrust every other bot |
| Re-applying Update Position Exit Options generates spurious orders | Kills C1; the Fortress class loses its cheapest fix |
| `QQQ-IC-0DTE-Baseline` gets audited (−$31,580, 43 positions, 38% of fleet loss, never examined) | Largest single unknown in the fleet. Could move the aggregate expectancy read materially in either direction |
