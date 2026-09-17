# Hedge program — the thesis, the calendar, and the honest risk

**STATUS: rationale document. It authorizes nothing and decides nothing.** Written 2026-09-17 at
Andy's instruction, after he asked in-chat: *"explain what this hedging contest is doing for us.
Where could we be in 6 months if successful? If 12 months? What would a success mean for these
hedge tests?"* — and then asked that the answer be saved rather than left in a chat.

**Relationship to the other hedge docs.** `hedge-north-star.md` is **the aim** — the signed
definition, the loss signature, the native-first strategy, what winning produces.
`hedge-design-spec-2026-09-16.md` is **the measurement** — the ledger evidence and the open rulings.
This file is **the case**: why the program is worth running at all, what "success" buys in calendar
terms, and the argument against it. Where it restates a number, the cited file wins
(`CLAUDE.md` §10 — narrative docs never carry authority over a CSV).

⚠️ **All fleet figures below are PAPER** (`STATUS.md` banner) and post-cutover
(`LEDGER_START = 2026-08-10`).

---

## 1. What the program is actually for

The usual framing — *"add downside protection to the condors"* — is wrong for this fleet, and the
ledger says why.

From `hedge-design-spec-2026-09-16.md` §2, derived from the working ledger:

- **Every dollar of loss came from an exit.** −$11,211 across 35 positions.
- **Expired losses: $0 across 0 positions.** All 56 expired legs are winners, **+$12,525**.
  Nothing this fleet has ever held to settlement has lost money.
- The exits are **booking the extreme, not capping it**: 40% of losers close within five minutes of
  their own MAE, against 6% of winners (§2.4).
- **The losers were green first** — 24 of 30 carried positive MFE, median +0.70%, median MAE
  −2.30% (§2.5). These are working positions that gave it back in the last two hours.
- The damage is concentrated: the top ten losers by R are **−$7,459 on $31,500 risk**, aggregate R
  **−23.7%**, and account for **67% of every dollar the fleet has lost** (§2.2 table).
- And it is **a clock, not a magnitude**: 75% of losers take their worst tick after 14:00 ET vs 32%
  of winners; **89% of all loss** (−$9,827 of −$11,011 carrying an MAE timestamp) has its MAE inside
  **14:00–15:30 ET** (§2.3). Underlying net move on the worst days is ±0.20–0.78%; the single
  largest-move day in the sample was a **+$1,142 winner**.

⭐ **The thesis, in one sentence: the hedge exists so this fleet can stop exiting.**

Today a stop-loss is the only thing between a losing 0DTE condor and an uncapped tail, and that stop
is provably realizing the worst tick of the day. A hedge replaces the stop with a different trade —
**hold to settlement, where the record is perfect, and carry a separate position that pays through
the 14:00–15:30 window where the loss actually lives.**

That is the swap under test. Not *"make money hedging."* **Replace a mechanism that books the
extreme with one that costs a premium.**

## 2. What "success" means — and the bar that follows from it

`R-2026-09-17-PAPER-ARM-PREAUTH` fixes the bar, conjunct, set before any result exists: the winning
arm beats **H-0** (ride, no stop, no hedge) on Exp(R) per condor ex-artifact, **and** beats **both**
H-C stop arms, **and** its fire count implies ≥10 fires within 3 months.

📌 **Note what that bar permits, because it is the point.** The hedge may **lose money on most
fires and still win**, provided ride-plus-hedge beats ride-and-get-stopped-out. That is why the bar
is relative to H-0 and H-C rather than absolute. A hedge judged on its own P/L would be killed for
doing exactly the job it was bought for.

Success produces one concrete artifact — the Monitor automation's spec (`hedge-north-star.md` §6):
which trigger at what threshold, which structure at what size ratio, a no-hedge-after cutoff, the
hedge's own exit rule, and a pre-registered paper expectation so the paper bots have a bar to hit.

## 3. Six months — March 2027, if it works

Grid runs → winner identified → paper arm starts under the B3 pre-authorization → **north-star §6's
unshortenable paper phase**: *"A 3–5 fires/month trigger needs 2–3 months for ~10 fires."*

**The realistic March state:** one signed hedge bot running on paper; the exit stack coming off the
GF family in favour of hedge-plus-ride; and a measurably different loss profile in the paper ledger.

**What it is NOT:** live capital at size. `CLAUDE.md` §4's gate is T2 with n≥100 positions / 6 months
/ a regime change. Backtest figures are T4; paper does not clear T2. **Six months buys conviction,
not size.**

**The second return, easy to undervalue.** `hedge-north-star.md` §3: the native version **prices**
the webhook version. If the dumb 14:00 trigger already recovers most of the give-back, the VPS
regime filter never gets built — months of plumbing not spent. If it bleeds on whipsaw, the
false-fire cluster specifies exactly what signal the webhook must compute. **Both outcomes pay for
the grid.**

## 4. Twelve months — September 2027

If paper holds, live at small size from roughly Q1, which puts the fleet ~6 months into a live
sample by next September — **approaching T2, not past it.**

⭐ **The real prize at twelve months is not one bot.** The loss signature is a **fleet property, not
a bot property** — it is a statement about how this program exits, and the roster carries 44 bots.
If holding-plus-hedging beats stopping, **the exits come off broadly.** The program is not testing a
hedge; it is testing whether this fleet's entire exit philosophy is backwards.

## 5. The argument against — read this before the grid runs

**The loss signature rests on n=28 losers across roughly 27 live trading days.** If the 14:00–15:30
clock is an artifact of a short sample, the hedge gets optimised for noise — and this project is
well-governed enough to produce a confident, thoroughly-documented **wrong** answer. The governance
does not protect against a thin sample; it only guarantees the thin sample is accurately described.

This is the counterweight to §1. §1's numbers are real and they are small.

**The backtest grid is the check on exactly that**, over years of OA history rather than 27 days —
and `hedge-design-spec-2026-09-16.md` §3 makes it structural rather than optional: **no arm may be
ranked from the live ledger at all** while the §3.1 defect stands. The backtester is not a
convenience here. It is the only ranking surface the program has.

⭐ **Therefore: the most valuable output of Phase 1 may not be a winning hedge.** It may be finding
out whether the clock pattern survives contact with a real sample. If it does not, the program has
saved itself the paper phase, the webhook build, and a fleet-wide exit change made on 28 data points.
**That is a good outcome and it must be allowed to be one** — a Phase 1 that kills the thesis cheaply
is a success of the same kind as one that confirms it.

## 6. On pace — why the lane matters to the calendar

Every date above assumes the grid is run on the Devin lane, not by hand. The UI path has no sweep
(`docs/dispatch-oa-capture-2026-09-16.md`: *"the order is the budget"*), size ratio came back
**absent** from the platform so the ratio must be swept as separate backtests, and the arm count
grows accordingly. Andy's own read, in-chat 2026-09-17: the Devin lane is doing this *"at a much
faster rate than myself."*

The dependency runs the other way too, and should be stated plainly: **if the lane stalls, every
date in §3 and §4 moves with it.** The calendar is a function of run throughput, not of analysis.

---

## Sources

`STATUS.md` (2026-09-16 generation — headline figures, PAPER) · `hedge-design-spec-2026-09-16.md`
§2.1–§2.5 and §3 · `hedge-north-star.md` §1, §3, §6 · `docs/RULINGS.md`
`R-2026-09-16-HEDGE-DEFINITION`, `R-2026-09-17-PAPER-ARM-PREAUTH`,
`R-2026-09-17-PHASE1-SUBSTRATE-SPLIT`, `R-2026-09-17-COMBO-RULES-PRESENCE-ONLY` ·
`docs/dispatch-oa-capture-2026-09-16.md` Phase 1 · `CLAUDE.md` §4, §10.
