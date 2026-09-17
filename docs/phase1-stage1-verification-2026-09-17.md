# Phase 1 Stage 1 — independent verification pass

**Written 2026-09-17 by the Cowork session** per `CLAUDE.md` §9.1a. The bundle
`data/captures/2026-09-17-p1-stage1/` is **not modified**; its 18/18 `SHA256SUMS` verify as
delivered. Every figure below was **recomputed from the CSVs**, not taken from the report.

**Devin's numbers reproduce exactly.** N, Exp(R), win rate, worst R, the 353/353 A-row match, the
316 B-rows, the 21 dropped rows and their +$580 — all confirmed. This pass adds four things his
report does not contain.

---

> ### ⛔ AMENDED 2026-09-17 — three overstatements corrected on Devin's challenge. Originals stand below.
> Devin verified this document's arithmetic against the raw CSVs (it reproduces to the digit) and
> then challenged three **claims**, correctly. All three are conceded and the corrections are here,
> at the top, because each one weakens a conclusion this document states more strongly below.
>
> **(a) "The failure is robust" — WITHDRAWN.** This document applied unpaired CIs to the condor arms
> and then asserted robustness for S1-H without holding itself to the same standard. S1-H vs S1-0 is
> a **paired** comparison — same 353 days. Devin's paired test, **reproduced here independently**:
> mean diff **−0.0284 R per condor-day**, sd 0.3151, SE 0.0168, **t = −1.70, 95% CI
> [−0.0613, +0.0044], p ≈ 0.090.** **The CI crosses zero.** The correct statement is **"no
> demonstrated benefit," not "demonstrated failure."** The data do not reject the hedge; they
> **fail to endorse it**, and under the burden-of-proof rule the bar is still not met — the winner
> must BEAT H-0 and both stops, and S1-H does not. The direction is negative and S1-H's drawdown is
> worse (8.28R vs 5.38R, a point this document did not use), but that is evidence of *no case for*,
> not *a case against*.
>
> **(b) "The native-first route is exhausted" — OVERSTATED, amended.** Stage 1 killed one shape:
> unconditional, fixed-time (14:00), fixed-side. **OA can express a conditional this document did
> not consider: an entry filter on the OVERLAY itself** — VIX, Change %, IV Rank, gap — gating which
> *days* the debit is paid. Still fixed-side, still blind to the primary's P/L, so still not H-A.
> But it is the difference between paying premium on **1,109 days** and paying it only in selected
> regimes — and since the overlay's problem is cost (−0.2047 over 1,109 trades), **that is precisely
> the lever that could matter.** Correct wording: **"unconditional fixed-side is exhausted;
> market-state-conditional remains expressible, unpromising, and untested."** Declaring the
> expressible space closed hid this option instead of pricing it.
>
> **(c) The GF-family obituary in §5/§2 — PREMATURE, made conditional.** "Ranking unachievable" was
> generalised to eight arms from a spread measured across **three**. **MDE is the detection floor,
> not the spread**: if PT50 or Trail genuinely move Exp(R) by more than 0.076 R they are detectable.
> Correct wording: **"unachievable IF the remaining mechanics land inside ±0.076 R"** — which is
> exactly what the four-arm confirming test resolves, and why that test is the honest instrument to
> run *before* the family is declared dead.

## 1. ⛔ THE VERDICT — S1-H fails the bar, and the failure survives the drop correction

`R-2026-09-17-PAPER-ARM-PREAUTH` requires the winner to beat H-0 **and** both stop arms.

| Arm | N | Exp(R) | 95% CI | Total P/L | Total risk |
|---|--:|--:|---|--:|--:|
| **S1-0** ride control | 353 | **+0.0367** | [−0.0033, +0.0767] | +$2,030 | $60,751 |
| **S1-a** SL100 | 353 | +0.0323 | [−0.0029, +0.0675] | +$1,933 | $60,751 |
| **S1-b** SL200 | 353 | +0.0382 | [+0.0003, +0.0760] | +$2,148 | $60,751 |
| **S1-c** overlay standalone | 1,109 | **−0.2047** | — | −$6,110 | $32,030 |
| **S1-H** as exported | 353 | **−0.0019** | — | +$83 | — |
| **S1-H** drop-corrected | 353 | **+0.0083** | — | +$663 | — |

**S1-H loses to all three, before and after correcting for the 21 silently dropped rows.** Corrected
it reaches **+0.0083 against a +0.0367 control** — under a quarter of the baseline. This is not
marginal and it is not a measurement artifact. **The drop was reported, not absorbed, and correcting
it does not change the verdict.**

Stops did fire — 66 `stoploss` closes in S1-a, 26 in S1-b — so the incumbent arms are valid.

## 2. ⚠️ NOBODY MAY READ S1-b AS A WINNER — the grid cannot separate the condor arms

All three condor arms sit inside each other's 95% confidence intervals. Per-position R has
**sd ≈ 0.34–0.38** against Exp(R) differences of **0.002–0.006** — an order of magnitude below the
noise. S1-0 and S1-a do not clear zero at all.

**The honest statement: over 353 positions this grid cannot distinguish ride from stop.** S1-b
being "highest" is noise. Any write-up that ranks them is over-reading, and the `PAPER-ARM-PREAUTH`
bar is not met by anything here.

## 3. ⛔ PUT-SIDE-ONLY DOES NOT EXPLAIN THE FAILURE — Stage 2's call side would not rescue it

The obvious objection is that a put-only overlay covers half the risk. **Checked; it does not hold.**

S1-0's 53 losing positions, split by underlying direction (`Price at Open` → `Price at Close`):

| side tested | positions | loss |
|---|--:|--:|
| underlying DOWN (put side) | 28 | −$3,003 |
| underlying UP (call side) | 25 | −$2,435 |

Roughly even — so the put overlay addressed **55% of loss dollars**, not a negligible slice. And it
**failed to recover them**: the overlay cost ≈ **$1,367 net** (control +$2,030 → corrected S1-H
+$663) against the $3,003 of put-side loss it was pointed at.

A call-side overlay is an **unconditional fixed-time** position too, so it would add cost on all
~353 days while addressing $2,435. **Same direction, same arithmetic.** Adding it makes the combined
result worse, not better. ⭐ **Stage 2's call-side arm cannot change this verdict and should not be
bought in the hope that it will.**

## 4. ⭐⭐ THE FOUNDATIONAL CLAIM OF THE PROGRAM IS FALSIFIED

`hedge-design-spec-2026-09-16.md` §2.1, the premise the whole hedge program rests on:

> *"Every dollar of loss came from an exit. Expired losses: **$0 across 0 positions.** All 56
> expired legs in the ledger are winners, totalling +$12,525. **Nothing this fleet has ever held to
> settlement has lost money.**"*

**S1-0 IS that claim, run for five years.** Pure ride to settlement, expiration only, no PT, no SL,
no trail, no touch — all 353 positions close `expired`.

| | |
|---|--:|
| losing positions | **53 of 353 — 15.0%** |
| total loss on those | **−$5,438** |
| worst single position | **−$266** |
| net across all 353 | **+$2,030** |

**The live-ledger claim was a ~27-trading-day small-sample artifact.** Riding to settlement is still
net positive — but "nothing held to settlement has ever lost" is **false at scale**, and the loss it
does take is the thing the hedge was designed to be unnecessary for.

📌 This is precisely the question `docs/hedge-program-thesis.md` §5 was written to pose — *"whether
the clock pattern survives contact with a real sample"* — and the foundational half of it **did
not**. §5 states in advance that a Phase 1 which kills the thesis cheaply is a success of the same
kind as one that confirms it. **This is that outcome.**

⛔ **A correction to `hedge-design-spec` §2.1 is OWED and is GATED** — it changes the premise of the
program, so it is a decision, not an evidence-backed correction (`CLAUDE.md` §5, "when it is
ambiguous, it is gated").

## 5. What Phase 1 did and did not kill

**Killed, on 5 years and 353 positions:** an **unconditional, fixed-time, fixed-side debit-spread
overlay** on a 0DTE QQQ condor. It costs more than it returns — the overlay bleeds at
**Exp(R) −0.2047 over 1,109 trades, 16.4% win rate.** That is the measured price of unconditional
protection, and it is not close.

**NOT tested, because the platform cannot express it:** a hedge that fires **only when the primary
is actually deteriorating**. That is H-A, removed under `R-2026-09-17-COMBO-RULES-PRESENCE-ONLY`
because no P/L predicate exists anywhere in the surface.

⭐ **So the finding is sharper than "the hedge failed":**
**the hedge shape Option Alpha can express does not pay, and the shape that might pay is not
expressible on Option Alpha.** The native-first route of `hedge-north-star.md` §3 is now
**exhausted**, and §3's own words price what remains: the conditional version *"requires a
webhook — signal computed off-platform (VPS), pushed in. Months of plumbing; untestable in either
backtester."*

That is a decision for Andy, not a conclusion of this document.

## 5b. 📌 Devin's open question, tested: are the 21 dropped rows directionally biased?

He flagged that several drops were the big-down-day hedge wins the overlay exists for, and noted he
had not tested for directional bias. Tested here:

| | n | mean P/L | median | win rate | total |
|---|--:|--:|--:|--:|--:|
| retained B rows | 316 | −$6.16 | −$22 | 18.7% | −$1,947 |
| **dropped B rows** | 21 | **+$27.62** | −$22 | **38.1%** | **+$580** |

**Welch t = +1.82 — not distinguishable at n=21.** The medians are identical (−$22), so the gap is
driven by a few large wins in the tail rather than a shifted distribution. **The honest statement:
the point estimate leans toward the drops removing hedge wins, but the sample cannot establish it.**

📌 It does not change the verdict either way, because every conclusion above already uses the
**drop-corrected** figures — the hedge has already been given the benefit of all 21 rows.

⚠️ **But it is a live operational risk for anything that ranks off combined exports.** If OA's drop
mechanism does correlate with row economics, a combined export is not merely incomplete, it is
**non-randomly** incomplete. `R-2026-09-17-PHASE1-EVIDENCE-PROCEDURE`'s reconcile rule handles it —
provided nobody ever absorbs a delta instead of reporting it.

## 6. Procedural notes

- **The silent row-drop replicated at scale** — 21 dropped B-rows here against 1 in Phase 0c, again
  with caps permitting them and no error. `R-2026-09-17-PHASE1-EVIDENCE-PROCEDURE`'s reconcile rule
  caught every one. **The rule earned itself on its first live use.**
- **Devin could not update `session-log.md`** because the dispatch said "touch nothing outside the
  new bundle directory," which conflicts with `CLAUDE.md` §9.1. **That conflict is the dispatch's
  fault, not his** — he flagged it in the README rather than silently violating either. The close-out
  for this run is in this session's log entry instead. Future dispatches should carve out
  `docs/session-log.md` explicitly.
- Two OA driving facts worth carrying into the skill: **`Copy CSV` never writes the clipboard under
  CDP** (permission granted, content stale every attempt) — use `Browser.setDownloadBehavior` plus
  `Download CSV`; and **several delegated `data-click` handlers do not fire on trusted
  `Input.dispatchMouseEvent`** but do fire on a JS `.click()`.
