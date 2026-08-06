# Hedging philosophy and library — v2

*REWRITTEN FROM SCRATCH 2026-07-31 for Bot Fleet v2. Supersedes the v1 file at
`~/bot-fleet/docs/hedge-research.md` entirely — do not read the old one.*

> **This file GATES the tournament rebuild.** Nothing in the hedge tournament gets built,
> ranked, or selected until this document says what a valid arm is.
>
> **What carried:** the philosophy, the operator evidence anchors, the SL% spectrum, the
> mechanic catalog, the failure modes, the S2 production diagnostic, and the free-tournament
> engine.
> **What did NOT carry:** every ranking, and the whole hedge→bot matrix. Both are stamped
> **INVALIDATED** below, and they stay invalidated until matched arms exist.
> **What is corrected:** the `Conditional` mechanic was never buildable on this platform. See §7.

> ### ⛔ ROSTER CHANGES ARE ANDY'S CALL, EXPLICITLY
> This document treats every new finding — including the three-identical-arms result in §6 —
> as **INPUT to a decision, never as a disposition decision.** `build-plan.md` is under
> decision freeze and its fleet table is the authority. Nothing here changes which bots exist,
> which are archived, or which arms get built. Where a finding has roster implications, it is
> flagged as **[ROSTER IMPLICATION — ANDY]** and stops there.

---

## 1. Philosophy — how we hedge

Unchanged from v1. This is the part that survived contact with the data.

1. **No single hedge wins all patterns.** Hedge choice is pattern-dependent, not a universal
   winner. Sandvand tested VIX as a filter and **rejected it**, attributing P&L variance to
   *"the size of the intraday moves"* — exactly what Range075 captures. This points toward
   per-side / conditional monitoring, not one global stop.
2. **The entry filter is the first line of defence.** Range075 (skip if |Δ% since prior close|
   > 0.75%) prevents more loss than any stop repairs. Hedges are the *second* line, for the
   days that get through.
3. **A hedge is config, not a pillar.** It is a parameter on a strategy — a stop level, a
   defang, a strike-touch close — not its own bot. Standalone hedge *bots* are reserved for
   genuine separate protective positions (tail put, VIX ladder), which this fleet does not run.
4. **Decide by tournament, backtest-first.** Never by intuition, and never off the contaminated
   QQQ live data. Narrow the field on clean backtest history, then run only the finalists live
   as matched parallel arms.
5. **Match the hedge to the structure.** Credit structures need loss-capping mechanics; debit
   structures are defined-risk by construction — their hedge *is* the tight stop/PT. Do not
   bolt IC hedges onto debit bots.

**A sixth principle, added 2026-07-31 from the v1 post-mortem:**

6. **A hedge that cannot be proven to have fired is not a hedge.** Every mechanic in this
   library must name, in advance, the artifact that proves it executed — and for exits that
   artifact is the position's **Trades list**, never the Exit Options panel
   (`oa-platform-reference.md` §0.3). A mechanic with no proof-of-fire is a hypothesis wearing
   a hedge's name, and this fleet ran one for four months.

---

## 2. The evidence anchors — three credible operators

| Operator | Dataset | Anchors | Rating |
|---|---|---|---|
| **John Einar Sandvand** (Theta Profits) | **~9,100 documented 0DTE SPX IC trades, Apr 2021 – Feb 2026** — the largest public dataset in this regime. ~40% wins / 60% losses, avg win ≈ 2.0–2.3× avg loss, double-stop-loss day rate **8.6%**. Net profitable every year since inception except one month (Jan 2022). | The **~100%-of-credit "Breakeven" stop** | ★★★★★ |
| **Tammy Chambless** | MEIC (Multiple Entry Iron Condors), ≥5 yrs public daily postings, Option Omega / Trade Steward backtests | **SL200** | ★★★★ |
| **Sean Pearce 2025** (SSRN) | 3,100+ trades 2013–2025; 3:58 PM entry → 89.2% WR | **SL130** | ★★★★ |

Pearce's own caveat is the important one: *"when a loss occurs it is almost always large and
nearly unpreventable."* **SL130 is a cap, not a save.**

### 2.1 The SL% calibration spectrum

**~70–80% (anecdotal) → ~100% Sandvand (★★★★★) → 130% Pearce (★★★★) → 200% Chambless (★★★★).**
Above ~200% is effectively no-stop on a $5-wide SPX IC.

> **The fleet's SL50 is a genuine outlier — below the lower bound of every rigorously
> documented operator.** None publishes a stop tighter than ~70% of credit. SL50 is tail
> exploration, not a validated choice, and it should never have been the default.

**Missing rungs, each with a published comparable:** SL75 · SL100 · SL130 · SL150 · SL200.

**Dollar-anchored stops are now runnable.** OA's June 2026 release added **Stop Loss $ /
Profit Taking $** in both backtest and bots. This matters because on thin-credit 0DTE the same
*percentage* is a very different dollar risk. Both the % rungs and fixed-$ variants belong in
the sweep.

---

## 3. Mechanic catalog

**Tier 1 — well-evidenced**
~100% Sandvand "Breakeven" two-layer OCO · SL200 (Chambless) · SL130 (Pearce) ·
**strike-touch close-all** (this fleet's **S2**) · intraday stop-tightening (Sandvand) ·
last-hour shift to shorts-only · hard time exits (Pearce) ·
**defang** — close shorts at ~$0.05, let longs ride (Sandvand SOP; safe on SPX because it is
cash-settled, so no assignment risk).

**Tier 2 — structural**
Defensive roll of the untested side · convert IC → iron butterfly (recenter) · defang.

**Tier 3 — portfolio overlays, thin 0DTE evidence, NOT applied**
Long-gamma ATM straddle overlay · iron-fly hedge bot · VIX call ladder · far-OTM weekly SPX put
· ES/MES delta hedge · ATR/realized-vol-scaled SL. Park in Lab until there is a reason.

### 3.1 The fleet's own hedge codes

| Code | Mechanic | Status |
|---|---|---|
| **S1** | On tested-side strike touch, close the **tested spread only** | Buildable. See §7.2 — may become an Exit Option. |
| **S2** | On strike touch, close the **entire iron condor** | Buildable. The fleet default. Diagnostic in §4. |
| **S3** | A **50% max-loss stop** | Buildable as an Exit Option. Killed as a sole hedge (5W/9L; whipsaws winners) though it specifically wins call grinds. |
| **Conditional** | *Was defined as:* close the tested spread after price is sustained ~$1 past the strike for ~10 minutes | ⛔ **NOT BUILDABLE AS DEFINED.** See §7. |

---

## 4. S2 — the production diagnostic that still stands

This is real evidence about a mechanic that genuinely executed, and it survives the cutover as
**archive-era context**. It is not a v2 prior — under `build-plan.md` §3 every bot restarts at
n=0 — but the *mechanism* it identified is a design input.

**Diagnostic, 2026-06-10, `IC-SPX-FastPT25-S2`, 326 legs / 131 losses / −$27,890:**

- **False-fire** (closed for a loss, day's move then reverted to the safe side): only **7 legs,
  −$400.** Not material.
- **Ride-to-max-loss:** worst loss ror −0.47. **No −1.0 blowups.** Only 4 legs worse than −0.30
  ror (−$7,825). S2 caps losses well.
- **The bleed is entry, not the hedge.** 124 *small, genuine-direction* stops total −$17,915,
  median loss ror −0.03. The 0.75%-OTM short strike is **touched on ~40% of legs** and S2
  dutifully takes each small loss. Avg loss $213 > avg win $118. The put side does the damage
  (−$7,130 net / 75 stops vs call +$640 net).

> **The conclusion, and it is a standing rule: S2 is healthy. Better hedges will not fix this.**
> The lever is **strike-touch frequency** — wider OTM strikes, a stronger trend/day filter, or
> fewer entries. **Do not re-tune the hedge to solve an entry problem.**

⚠️ **The S2 backtest validation (964 trades, zero false positives) never had its
production-validation closed**, and the cutover means it now starts over. Treat S2 as
*mechanically sound, expectancy-unproven* on the v2 fleet.

---

## 5. ⛔ INVALIDATED — the hedge→bot matrix and every tournament ranking

**Stamped INVALIDATED-2026-07-28, re-affirmed 2026-07-31. Nothing below this line ranks
anything.**

### 5.1 Why the v1 tournament cannot select

Four independent defects, any one of which is disqualifying:

1. **Arms were not independent.** `HedgeA-S1` and `HedgeD-Conditional` produced **identical P/L
   at an identical entry minute on 73 positions**. They are one arm wearing two names.
2. **Arms were not in the same execution class.** S3 ran as an Exit Option (1-minute cadence,
   first in the cycle); S1/S2/D ran as Monitors (scan speed, third in the cycle). **S3's win is
   inseparable from its execution class.**
3. **The Conditional arm tested something other than its name.** §7.
4. **No arm carried Range075**, the fleet's primary filter — so the tournament measured hedges
   on unfiltered days the production strategy would never have traded.

**Every arm's Exp(R) was negative anyway** — S3 −0.0029 · S2 −0.0095 · **Raw/no-hedge −0.0211**
· S1 −0.0260 · Conditional −0.0308. Including no-hedge-at-all. That is not a ranking; it is a
statement that the measurement was not measuring hedges.

### 5.2 What a valid arm requires — the definition of done

An arm may enter a ranking only when **all five** hold:

1. **Shared automation, shared inputs.** Arms differ in **exactly one input value**, and the
   proof is a **capture-diff showing one differing line**. Not a claim — a diff.
2. **Same execution class.** All arms as Exit Options, or all as Monitors. Never mixed.
3. **Range075 carried as a preset** on every arm, so the tournament measures hedges on the days
   the strategy actually trades.
   > ⚠️ **FLAGGED 2026-08-06 — "carried as a preset" is a category error; corrected in substance
   > by Architecture E.** Presets are an Exit Options object (`oa-platform-reference.md` §6.1);
   > Range075 is `a symbol %-change decision` (§8 below), an entry decision — an entry decision
   > cannot be an exit preset. Under the Architecture-E ruling (Decision 4, `decision-memo-2026-08-04.md`)
   > the requirement is stronger, not weaker: Range075 lives in the SHARED entry automation, so it
   > is identical across arms by construction rather than by repetition. Rule 3 is not withdrawn;
   > it is marked. `build-plan.md` §2D carries the corresponding frozen-doc amendment
   > (2026-08-06, ruling 1a). Applied on Andy's explicit "amend the plan"
   > (`decision-card-2026-08-06.md` ruling 1).
4. **A pre-registration entry** naming the hypothesis, the kill criterion, the sample target,
   the review date — **and the platform primitive the mechanic will be built from** (§7's
   lesson).
5. **A proof-of-fire artifact** identified in advance (philosophy §6), and the first live
   position's Trades list checked against it before the arm accrues any evidence.

An arm failing any of these is **not a weak arm, it is not an arm.** Exclude it from the
ranking rather than caveating it.

### 5.3 The matrix, deliberately left empty

The v1 hedge→bot matrix mapped hedges onto bots that `build-plan.md` §2 now archives, deletes,
or rebuilds. Reproducing it would be worse than useless — it would read as current.

**It gets rebuilt after the v2 roster is built and pre-registered, not before.** The only
standing entries are structural, and they follow from philosophy §5 rather than from evidence:

| Structure | Hedge family | Why |
|---|---|---|
| Credit ICs | loss-capping: SL% rungs, strike-touch close, defang | Undefined loss without one |
| Debit / directional spreads | **tight SL + PT only. No spread-close hedge.** | Defined-risk by construction — the exit *is* the hedge |
| Mirrors | per source bot | ~70% of this research transfers; SL% and defang are the portable parts, Range075 is IC-specific |

---

## 6. New input — the tournament had THREE identical arms, not two

**[ROSTER IMPLICATION — ANDY. Recorded as input; no disposition proposed.]**

`execution_audit.py` v1.0.0's `DUPLICATE_ARM` rule, run over the frozen archive ledger,
independently reproduces the known S1≈D result and extends it:

| Pair | Identical positions |
|---|---|
| `QQQ-IC-0DTE-HedgeA-S1` ≈ `QQQ-IC-0DTE-HedgeD-Conditional` | **73** |
| `QQQ-IC-0DTE-HedgeA-S1` ≈ `QQQ-IC-0DTE-HedgeTest` | **73** |
| `QQQ-IC-0DTE-HedgeD-Conditional` ≈ `QQQ-IC-0DTE-HedgeTest` | **70** |
| `QQQ-IC-0DTE-HedgeA-S1` ≈ `QQQ-IC-0DTE-HedgeC-S3` | 42 |
| `IC-SPX-Fortress-Defang` ≈ `IC-SPX-Fortress-Unstopped` | 10 |
| `QQQ-IC-0DTE-Fortress` ≈ `QQQ-IC-0DTE-Fortress-NoPT50` | 14 |

*(Identical = same P/L, same structure, same entry minute, different bots.)*

**What this changes:** the INVALIDATED verdict is unchanged in direction and **broader in
scope** — a three-way identity class, not a pair. It also shows the Fortress A/B arms were less
independent than their names imply.

**What this does not change:** anything about the roster. All six bots named above are already
in `build-plan.md` §2's archive-directly group. **No disposition follows from this finding, and
none is proposed.**

**What it is genuinely for:** it validates §5.2 rule 1. A capture-diff requirement is not
bureaucratic caution — the identity was invisible for four months and a single diff would have
caught it on day one. The detector now runs this check on every ingest, so a v2 tournament
cannot repeat it silently.

---

## 7. ⛔ CORRECTION OF RECORD — "Conditional" was never buildable

The v1 file defined the `Conditional` mechanic as *"short touched + held N min, then close"* and
listed it as an arm of a live tournament.

**Option Alpha cannot express time persistence at all.** This is affirmative, not an omission:

> *"If a price, indicator, etc. exceeds a threshold between intervals, the bot does not know
> about it… even if a bot is logging information or position data between intervals, it will
> not act upon it until automation execution at the next interval."*
> — `technical-documentation/platform/automation-behavior.md`

A full keyword sweep for *sustained · persisted · consecutive · for at least · duration ·
elapsed · in a row* returns **zero hits in any decision context**. See
`oa-platform-reference.md` §0.1 and §11.

**What actually ran.** Whoever built `QQQ-IC-0DTE-HedgeD-Conditional` hit that platform wall and
substituted the nearest expressible thing — **position age** (`open 30 minutes or more`) —
without recording the substitution. The bot tested an **immediate $1-ITM stop** and lost
**−$15,376** while its documentation, its config record and its automation tree all agreed it
was testing a 10-minute sustained breach.

> **This is a distinct failure pattern: an undocumented substitution made at a platform limit.**
> Config-vs-reality diffing cannot catch it — the config and the tree agreed with each other
> and both were wrong about the *intent*. The defence is §5.2 rule 4: pre-registration names
> the mechanic **and the primitive it will be built from**, so a substitution has something to
> contradict.

**Separately:** HedgeD's `strike_fix=Y` contamination flag was **wrong** — 0 of 86 strikes are
malformed (`bots_meta.csv` corrected 2026-07-30). The −$15,376 is **real evidence about an
immediate $1-ITM stop**, and a genuinely useful data point about a mechanic nobody intended to
test.

### 7.1 The build path that does exist — the tag ladder

Tags are the only writable state on the platform (`oa-platform-reference.md` §5.3). At 1-minute
scan speed: tag `brch1` on first breach; `brch2` when `brch1` is present and the breach still
holds; … `brch10` fires the close. Any non-breach scan runs Reset Position Tags.

That is a real 10-minute sustain condition built from documented primitives.

> **Cost and risk, stated before anyone builds it.** ~10 decision/action node pairs, consuming
> the bot's entire 1-minute scan budget. **Every rung is a place the ladder can break, and a
> broken rung fails *safe-looking*** — no close, no error, no signal. It is a silent-failure
> generator by construction and needs a shadow monitor as a divergence detector.
>
> **Recommendation: do not build it for the v2 tournament.** Drop the Conditional arm rather
> than spend the scan budget and the failure surface on a mechanic with no public comparator
> (§8). **[ROSTER IMPLICATION — ANDY.]** If it is wanted later, it is scoped to one dead bot
> first.

### 7.2 The Touch trigger could dissolve the execution-class confound

OA documents a **`Touch`** Exit Option trigger. **What it references is not documented** —
underlying-touches-short-strike, or position-price-touches-a-level.

**If it is the strike reading**, S1 and S2 stop needing monitors entirely: 1-minute cadence,
running *first* in the cycle. Every arm could then sit in one execution class, which retires
defect 2 of §5.1 — the confound that made S3's win unreadable.

**This is a two-minute UI check and it is the single highest-value open question for the
tournament rebuild.** It is item 1 in `oa-platform-reference.md` §9.

⚠️ Its own failure mode: Exit Options are subject to the **Bid-Ask Guard**, which disables them
while the spread is wide. A touch hedge that stops working exactly when the market is fast is
the worst-timed failure available. Leave the guard OFF on touch hedges and keep a shadow
monitor.

---

## 8. Range075 — the novel edge, and its uncalibrated risk

**No public operator runs an intraday-range filter as a % of price.** Range075 — skip if
|change% since prior close| > 0.75% — has no documented analog. The closest thing is Sandvand
rejecting VIX and naming intraday-move-size as the right filter family.

This is simultaneously the fleet's competitive advantage and its least-calibrated parameter.
**The single highest-information experiment available is the SL% × Range075 interaction grid** —
no public dataset of it exists.

Note it is a **gap filter, not an intraday-range filter**: implement as a symbol %-change
decision, not a high-low range check. VIX filtering is redundant once Range075 is present
(validated; the no-VIX test passed).

---

## 9. Recommended backtest sweep

Ordered. Each ties to a published comparable, so a result has something to be judged against.

1. **SL100 + SL150 on the Range075-filtered base**, controls SL50 / current / Unstopped. Fills
   the empty middle of the spectrum; SL100 is Sandvand's anchor.
2. **SL200** — test whether it collapses to Unstopped on a $5-wide SPX IC.
3. **Intraday stop-tightening schedule** — 200% at entry → 100% by 1 PM → 50% by 2 PM →
   shorts-only after 3 PM.
4. **Defang** — close shorts at $0.05, longs ride.
5. **Range075 × SL% interaction grid** — the meta-experiment. The core research thesis and the
   one no public operator has published.
6. **Fixed-$ SL variants** alongside the % rungs, now that OA supports them.

**Judge every one by R, never by $ or win rate.** OA's own Top Backtests views sort by 82–90%
win rate, which is precisely the trap.

---

## 10. Failure modes to design against

- **Double-stop-loss day** — 8.6% of Sandvand's trades.
- **Stop-limit skip on gaps** → the two-layer OCO exists for this.
- **Trending-day cascade** across MEIC tranches.
- **"Busted trade" — never leg out of a spread.** Perryman's $116,600 loss.
- **Late-day gamma whipsaw.**
- **False-fire on calm tape** — the SL50 / tight-strike-touch disease.
- **Max-loss on volatile tape** with loose stops.
- **SL-trigger slippage is worse than PT slippage.** Backtests ignoring it overstate tight stops.
- **Market-order fills outside the spread** — the 6/11 fill came in **$5.05/contract beyond the
  worst price the position was ever marked at**, producing R −1.63 on a defined-risk spread.
  Market pricing is banned on every v2 entry and exit except a hard end-of-day flat close.
  ⚠️ *Extended to entries 2026-08-06 (Decision 5, ruled 2026-08-04) — order-type-specific, not
  side-specific; a market order takes no limit on either side. Originally scoped to exits only;
  see `oa-platform-reference.md` §7's dated append for the full rationale and the accepted-cost
  caveat (n=1 position, below the T2 gate).*
- **Silent suppression** — the Bid-Ask Guard disables Exit Options without an error (§7.2).
- **Undocumented substitution at a platform limit** — §7. The newest one, and the hardest to see.

---

## 11. Validated decisions carried forward

Confirm each still holds before relying on it; all predate the cutover.

- **Range075** is the most powerful single filter.
- **Stop losses are counterproductive on the Fortress structure** — sizing and hedging are the
  risk management there.
- **$2-wide is most hedgeable on QQQ; SPX production structure is $5-wide.** Symmetric 0.75%
  strikes confirmed; asymmetric rejected.
- **Min-credit filter hurts** — winners averaged *lower* credit than losers.
- **The 3:50 PM flat rule is QQQ-only.** It backfires on SPX cash settlement.
- **PT50 killed across all configs except Scalp** (redundant with S2). **S3 killed.**
  **VIX<25 filter killed** (redundant with Range075).

---

## 12. The free hedge tournament — the engine that already runs

`scripts/hedge_tournament.py`, wired into `daily.sh` stage 5. Replays each day's real settled
legs through a fixed hedge library and scores each by **R**. Every trading day is ~6 free hedge
experiments at zero marginal cost.

**Library v1** (R = modeled_pnl / risk): ride/no-stop · PT+25/50/100 · SL−50/75/100/130 ·
S2 strike-touch cut (`approx`, 5-min tape grain) · defang (`approx` or deferred).

**Correctness rules, baked in:**

- **MFE/MAE are path extremes, not fill guarantees.** "Would have booked ±X%" assumes the
  threshold *filled* at the threshold. **Label the whole engine an optimistic bound, never a
  live estimate.**
- **Order resolution:** if a position breached both a PT and an SL intraday, use the MFE/MAE
  **timestamps** to decide which fired first. That is why the ledger carries them. Do not assume.
- **Compare by R, never $.** Standings per rule: Exp(R), Tot R, WR, maxDD-R, worst-position-R, N.
  Regime-bucket the losers so "what would have worked" is regime-conditioned, not pooled.
- **Real positions only** — counterfactual on *exits*, never entries. No lookahead, no invented
  trades.
- **Unit test:** the ride arm must reconcile against the ledger's own expired-position P/L **to
  the dollar**.

⚠️ **Post-cutover this engine restarts at n=0** with the rest of the fleet, and it needs
`data/brief/<date>_tape.json` coverage to score the S2 arm at all. Expect thin standings for
months. That is the accepted cost of the clean slate, not a defect.

**What it is for:** after 30–60 days it produces a **live-data hedge ranking** that
cross-checks the OA/OO backtest tournament. It is a corroborator, not a selector — it inherits
every optimistic-bound caveat above.

---

## 13. Where the tournament can actually be run

The 2026-06-25 finding that Option Omega *"can't express our touch/cross-leg hedges"* is
**substantially outdated**. Docs-verified inventory:

**OO expresses natively:** the full SL% spectrum (Percentage / Fixed / Closing Order) ·
per-leg stop loss · trailing SL (immediate or after a minimum PT) · **0DTE intra-minute stops
using 1-second quote data** (SPX/SPY 0DTE only, and it applies to the SL *value* check, not to
"Exit When Tested") · profit targets · profit actions (scale out, adjust SL) · **time actions**
(→ the intraday tighten schedule) · early exit by DTE/DIT/MIT · VIX and VIX9D exits ·
RSI/SMA/EMA exits · **"Exit When Tested"** (touch/approach the short strike, **1-minute
sampling, explicitly "an exit — it is not a stop loss"**) · delta exits · re-enter after exit ·
**leg groups** (→ defang: *"exit the short upon SL and leave the long as a runner"*, verify).

By default *"when any leg is closed in OO, the whole trade closes"* — which is S2 close-all.

**Still needs LEAN — the genuine gaps:** cross-leg reciprocal triggers ("close the call side
*because* the put short was tested") · sub-second strike-touch with a latch · a tunable
sustain/dwell timer on touch · regime-conditional breach routing · opening hedge legs mid-trade
· mid-trade morphing (roll, widen, IC→fly).

> **Verdict: the exit-rule calibration core of the tournament — §9 items 1, 2, 3, 4, 6 — is
> expressible in OO today.** Only the advanced breach engine needs LEAN. That is materially
> more on the cheap side than previously assumed, and it should be re-checked against the
> paid-tier buy trigger.
>
> ⚠️ Inventory is **docs-verified, not trial-tested.** Defang-via-leg-groups and reclaim
> re-entry both need one real backtest before being relied on. OO also does not check margin
> when a long leg is held alone.

---

## 14. Future architecture — the breach-response engine

Kept as a target, with its platform constraints now stated honestly.

**The goal:** when an IC side is breached at a pivot-anchored level, *branch* the response —
exit / hold-and-wait / re-enter on reclaim — instead of the single S2 close-all. Pivots say
where a breach is meaningful; the regime classifier says which response is valid; VWAP confirms;
the S-codes are the actions. **Extends S2, does not replace it.**

State machine per tested side: `S0 open → S1 touched → {Sustained | Reclaim}`.

| At breach | Range regime | Trend regime |
|---|---|---|
| **Touch** | Wait — pivot likely to reject | Don't wait — bias is continuation |
| **Sustained** | Exit, S2 close-all | Exit fast; do **not** re-enter the broken side |
| **Reclaim** | Re-enter candidate (new mechanic, gated) | Skip — trend reclaims are traps |

> ### ⛔ THE MARTINGALE GATE
> Distinguish **re-enter on reclaim** (a NEW trade after the level holds — adding on
> *confirmation*, defensible, gated on its own backtest) from **double-down / average into the
> breached IC** (adding size while the short is beyond the strike — **martingale**, F-004
> reject, and the direct cause of the "trending-day cascade" and "busted trade" failure modes).
> **Double-down is default OFF and stays OFF** unless a test overturns F-004.

**Why none of this is buildable on OA today**, and it is worth being blunt: it needs sub-second
breach detection (OA is 1-minute at best), a tunable sustain timer (§7 — not expressible), and
mid-trade regime branching (not expressible). It also needs intraday pivots and VWAP, which OA
**cannot compute** — all its indicators are daily bars cached pre-market
(`oa-platform-reference.md` §5.1). The path is WebSocket strike-touch → webhook, with the
fast branches possibly direct-to-broker. Simple S2 close-all can stay in OA.

**Dependency chain — do not build out of order:** level-respect null test → regime classifier →
*then* this engine. Each new branch gets its own backtest under the density/null discipline.

### 14.1 Candidate — trailing profit-stop after PT

Once an IC reaches its profit target, activate a trailing stop on the position's profit instead
of closing flat, ratcheting a floor up as profit grows.

**Honest framing — this is not free.** It swaps a *certain* profit for a *probabilistic* larger
one while keeping a 0DTE position exposed longer. The risk concentrates in the fast-move tail:
a gap can slip *through* the trailing stop (0DTE gamma → fills worse than the floor, sometimes
a loss), and chop can whipsaw the exit *below* the target. Calm tape is nearly free upside; the
tail is where it bites — and the tail is where IC losses already live.

**Judge it on the loss tail and maxDD, not mean R.** That tail metric *is* the test of the
"no new risk" claim. Not martingale — no sizing up — so F-004 does not bite. Verify whether OA
supports a true intraday trailing stop on a 4-leg condor before assuming it needs building
elsewhere.

---

## Changelog

- **2026-07-31 — REWRITTEN FROM SCRATCH for v2.** Philosophy (+ a sixth principle: a hedge that
  cannot be proven to have fired is not a hedge), operator anchors, SL% spectrum, mechanic
  catalog, S2 diagnostic, failure modes, validated decisions, the OO inventory and the free
  tournament all carry. **The hedge→bot matrix and every ranking are stamped INVALIDATED and
  left empty** pending matched arms; §5.2 defines what a valid arm is. **`Conditional`
  corrected: never buildable on OA** — HedgeD tested an immediate $1-ITM stop and the
  substitution was never recorded (§7). Added the `Touch`-trigger finding that could dissolve
  the execution-class confound (§7.2), the three-identical-arms detector result as **input
  only** (§6), and the platform constraints that block the breach engine (§14).
- **2026-06-25** — OO hedge-expressibility inventory added; the "OO can't express our hedges"
  decision reversed.
- **2026-06-10** — S2 production diagnostic: the bleed is entry, not the hedge. Trailing
  profit-stop logged as a candidate. Breach engine formalised into `trigger-rules.md`.
- **2026-06-09** — Breach-response decision engine target architecture added.
- **2026-06-08** — Reframed from research-only into philosophy + application.
- **2026-06-07** — Initial population from the Hedge Mechanic Catalog.
