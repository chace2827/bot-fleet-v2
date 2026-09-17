# Decision card — 2026-09-17 — the Phase 1 arm table, respec'd

**Status: ✅ PART A APPLIED · PART B RULED 2026-09-17** (Andy, in-chat: *"go with your reccos"* — `R-2026-09-17-PHASE1-ARM-TABLE`, all four slots as recommended). Drafted at Andy's
instruction — *"help me do slot 4 and arm respec."* Slot 4 itself is ruled and recorded as
`R-2026-09-17-PHASE1-EVIDENCE-PROCEDURE`; this card is the arm table.

The original table (`docs/dispatch-oa-capture-2026-09-16.md`) was written before Phase 0b and 0c.
Three of its four arms are now wrong in some respect.

---

## ⛔ THE FINDING THAT DRIVES THE RESPEC — the hedge cannot be tested-side-reactive

H-A as written reads: *"a separate protective position opened at/after 14:00 ET, only on days the
primary is already losing"* — and `hedge-north-star.md` §4's V1 speaks of a **"tested-side"** debit
spread.

**Neither the conditionality nor the side selection is expressible.** The complete predicate surface,
established first-hand across both captures:

| surface | vocabulary | reaches position state? |
|---|---|---|
| `Combo Rules` | `open` \| `not open` — and nothing else (`rule0-state`, 0b raw lines 259-267) | presence only, never P/L |
| Entry Filters | VIX, IV Rank, Change %, Change SD, Gap %, indicators, MAs, GEX templates | no — all underlying/market state |
| Position Criteria | mid price, reward/risk, bid/ask, one-per-expiration | no — filters the entry, not a sibling position |
| Strategy picker | 8 fixed single structures | chosen at config time, never at runtime |

So the overlay's **structure is fixed when the backtest is written.** It cannot look at the condor
and choose the pressured side. **Every hedge arm in Phase 1 is a fixed-side, unconditional overlay
with at most a presence gate.** Anything described as "tested-side" is not buildable here and must
not be smuggled in under a different label — that is `R-2026-09-16-HEDGE-DEFINITION`'s failure mode
in a new costume.

## ⭐ AND THE PRESENCE GATE IS NEAR-NO-OP FOR THIS FLEET

Phase 0c proved `open` is **concurrent presence at the gated test's entry moment**. In the fixture
the primary closed before 15:00 on **240 of 249 days** — but that was **manufactured**: the fixture
specified a tight profit target precisely to create early closes
(`docs/phase0c-verification-2026-09-17.md` §4).

The real primary is a 0DTE condor carried into 14:00–15:30 (`hedge-design-spec` §2.3). **It is open
at hedge time essentially always.** A presence gate on the real structure therefore filters only the
days the primary never *entered* — real, but small.

**Consequence: gated and ungated H-B are not two arms.** Gate it on (it costs nothing and removes
no-entry days) and spend the saved arm on the time or ratio sweep, where the budget actually bites.

---

## PART A — applied, mechanical propagation of signed rulings

Entailed by rulings Andy has already signed; applied under `R-2026-08-31-DERIVED-RULING-AUTHORITY`
(a), with the entailment cited. No new judgment.

| change | entailed by |
|---|---|
| **H-A is REMOVED** from the table. Not renamed, not weakened — removed, because no P/L predicate exists. | `R-2026-09-17-COMBO-RULES-PRESENCE-ONLY` |
| **H-C's bar is restated in R against H-0.** Its −$173 / −$584 become context, not the bar. | `R-2026-09-17-PHASE1-SUBSTRATE-SPLIT` |
| **The "assume no export / transcribe by hand" bullet is superseded** by the narrowed regime. | `R-2026-09-17-PHASE1-EVIDENCE-PROCEDURE` (a) |
| **Every combine pins `posLimit` / `posLimitDay` in `crules`** and records them with the run. | same, (b) |
| **Every combine is reconciled against standalone exports** before ranking. | same, (a) |
| **What ran is verified from URL + row count, never the drawer.** | same, (c) |

## PART B — ✅ RULED 2026-09-17 as drafted. The new table, staged.

The UI path has no sweep, so **arm count is the budget.** The proposal spends the minimum needed to
answer the program's actual question, and defers every sweep behind a result that earns it.

### Stage 1 — the decision stage. 4 backtests + 1 combine, fits one 7-way Compare.

| # | Arm | Build | Answers |
|---|---|---|---|
| **S1-0** | **H-0 control** — primary condor, ride to settlement. No PT, no SL, expiration only. | 1 backtest | The baseline. Run FIRST; without it nothing else means anything. |
| **S1-a** | **SL100** — primary + stop | 1 backtest | incumbent exit |
| **S1-b** | **SL200** — primary + stop | 1 backtest | incumbent exit |
| **S1-c** | **Overlay** — long put debit spread, fixed entry time, 1 contract | 1 backtest | the hedge leg, standalone cost |
| **S1-H** | **H-B** = S1-0 ⊕ S1-c, presence-gated, caps pinned | 1 combine | ⭐ **the question**: does hold-plus-hedge beat stop? |

**The comparison that decides everything: S1-H against S1-a and S1-b, in R, against S1-0.** Per
`R-2026-09-17-PAPER-ARM-PREAUTH` the winner must beat H-0 **and** both stops.

📌 **Put side first, and state why.** The loss signature is late-day give-back to a short strike on
small-net-move days (`hedge-design-spec` §2.2–2.3), not a directional-magnitude pattern. One side
must be chosen because side selection is not expressible; **put-side first is a choice, not a
finding**, and the call side is Stage 2. If Stage 1 passes on the put side alone, that result is
labelled *put-side only* in every write-up.

### Stage 2 — only if Stage 1's S1-H clears the bar. Nothing here runs otherwise.

| sweep | arms | why deferred |
|---|--:|---|
| **Entry time** — 13:30 / 14:00 / 14:30 / 15:00 | 4 | §2.3 puts 89% of loss in 14:00–15:30; the clock is the most likely lever, but pointless if the mechanic fails. |
| **Size ratio** — overlay at 2ct, 3ct | 2 | **Forced into a sweep**: no relative-sizing control exists (0b Q4). `hedge-north-star.md` §6 makes ratio a required Monitor field, so it cannot be skipped — only deferred. |
| **Call side** | 1–2 | completes the structure; a strangle overlay is S1-0 ⊕ put ⊕ call, 3 tests, inside the 7-cap. |
| **No-hedge-after cutoff** | 1–2 | §6 field; cheapest to infer from the time sweep first. |

### Measurement — state the denominator or the number is untrustworthy

`CLAUDE.md` §4: compare by **R**, never raw $, and label the unit every time. For a combined arm
the denominator must be stated explicitly — **primary risk + overlay debit**, per condor,
ex-artifact. A combined Exp(R) whose denominator is not written down is not a result.

---

## ⭐ UPGRADE to the presence-gate finding — the gate is worth MORE than §4 said

`docs/phase0c-verification-2026-09-17.md` §4 called the presence gate "near-no-op" for the real
fleet, reasoning that a condor carried into 14:00–15:30 is open at hedge time essentially always.
**That reasoning was incomplete.** Reading the primary's actual config closed the gap:

The GF entry is not unconditional. `greenfield-family-spec.md` §3's `Loop QQQ` gates on
**Range075** — *"Symbol change % > −0.75 since previous close"* AND *"< 0.75"*. **On any day the
underlying has already moved more than ±0.75%, the condor never enters at all.**

So the presence gate removes **precisely the Range075-rejected days** — the large-move days. That
is not a trivial filter, and without the gate a fixed-time overlay would fire on exactly those days
with no primary to protect, booking pure cost. **The gate earns its place.** §4's conclusion that
gated and ungated H-B are not worth two separate arms still holds, and now holds for a better
reason: **gated is simply correct**, so the ungated variant is not a comparison worth buying.

## Slots — ✅ ALL FOUR RULED 2026-09-17

1. ✅ **Staged structure ACCEPTED.** (Stage 1 = 4 backtests + 1 combine; Stage 2 gated on S1-H clearing)? Draft recommends **yes** — it spends 5 arms to reach the decision instead of 11.
2. ✅ **Put side first**, call side to Stage 2, labelled **put-side only** in every write-up.
3. ✅ **Stage-1 overlay clock = 14:00 ET.** Swept in Stage 2, never tuned inside Stage 1. Original slot text: — one clock must be picked before the sweep. Draft recommends **14:00**, as the start of the window carrying 89% of loss.
4. ✅ **Primary config taken from the spec, not invented** — see the table below. Original slot text: — the Stage 1 primary should mirror the fleet's actual 0DTE IC, not the 0c fixture's short put spread. Draft recommends specifying it from `greenfield-family-spec.md` rather than inventing one; **the exact config is owed and is not proposed here.**

## What this card does NOT do

- It does not authorize a run, name a threshold, or touch the live fleet.
- It does not rewrite `docs/dispatch-oa-capture-2026-09-16.md` — the Phase 1 table there still
  carries its 2026-09-17 banner and stays NOT-rewritten until Part B is ruled.
- It does not resolve the `Ride`/`Touch0` identity (scoped to the ledger-side deliverable) or
  `hedge-design-spec` §3.3 (still owed for V3).


---

## The Stage-1 primary, as specified (slot 4, ruled)

Read first-hand from `greenfield-family-spec.md` §3 — the `Open Short Put Spread` action table and
the `Loop QQQ` automation listing. **Not invented, not carried from the 0c fixture.**

| Field | Value | Source |
|---|---|---|
| Symbol | `QQQ` | §2 scope decision — the 15:52 backstop is a QQQ mechanic |
| Expiration | `exactly 0 days` | §3 |
| Short strikes | **0.75% OTM** both sides | §3 — "matches the champion structure" |
| Width | **$2.00** | §3 — "most hedgeable on QQQ" (`hedge-research.md` §11) |
| Size | **1 contract** | §3 |
| Entry time | **after 13:30 ET** | §3 `Loop QQQ` |
| Entry gate | **Range075** — symbol change % between −0.75 and +0.75 since previous close | §3; expressible as the backtester's `Change %` entry filter |
| Minimum credit | mid ≥ **$0.08** | §3 — the pilot's live floor |

⚠️ **One divergence, recorded rather than smoothed.** The fleet builds the condor as **two paired
spreads** (ScannerA put / ScannerB call, two automations, two exit inputs). The backtester offers
**Iron Condor as one structure**. Stage 1 uses the single structure. The difference is real — it
collapses the fleet's per-side exit independence — and it is stated in the bundle README so no
later reader mistakes the backtest primary for a byte-equal model of the live bot.

⚠️ **Entry-time note.** OA's backtester takes entry times in 5-minute increments or a custom time
between 9:35am and 3:55pm (`data/oa_facts.csv` `OA-1110`). 13:30 primary and 14:00 overlay both sit
cleanly inside that.
