# `QQQ-IC-0DTE-Baseline` — forensic

**Written 2026-08-07.** Sprint Task 12 (`docs/sprint-2026-08-04.md` §3). Method: three parallel
subagents — time structure, trade anatomy, config archaeology — reconciled and re-derived by the
lead session. Every number below was recomputed from the frozen CSVs by the lead before it was
written down.

---

> ## ⛔ THIS GATES NOTHING
>
> `QQQ-IC-0DTE-Baseline` is **archived**. Its data is **pre-cutover** and frozen in
> `data/archive/` — never a reporting input (`CLAUDE.md` §3.1). Its entire life ended
> **2026-05-22**, before the v2 rebuild existed. **n = 43 condors over 2.5 months**, which clears
> **no** sample gate: B1 needs n ≥ 100, B3 needs a regime change (`docs/evidence-standards.md`
> §4). Nothing here authorizes, blocks, sizes, or modifies anything in v2. It is written for the
> lesson, and to close correction **C3**, which asked for exactly this and nothing more.
>
> **Do not promote any conclusion from this file into a v2 doc.** This is a standalone report.

---

## 0. Provenance and method

| input | sha256 (first 16) | role |
|---|---|---|
| `data/archive/trades.csv` | `218d7f733d6fab87` | primary — the frozen v1 ledger |
| `data/captures/oa_export_positions_2026-07-30.csv` | `dca69adaf771f064` | **second witness** — the raw OA export |
| `data/archive/bots_config.csv` | `d062d4ccffc0b602` | ⚠️ the **discredited** hand-written record |
| `data/archive/corrections.csv` | `3cfd0d9780c40525` | the 8-row correction layer |
| `data/bots_meta.csv` | `5507c8b091c73ca1` | epochs and flags |
| `data/archive/compliance.csv` | `bb5f85adb3dbb7e0` | v1 G5 scores |

### Pairing — stated because it sets every denominator downstream

**43 rows → 43 condors. Zero pairing was required, and this is the one bot in the family where
that is true.** All 43 rows are `structure = ironcondor`, `single_sided = False`, 43 distinct
`trade_id`. Per `docs/oa-export-schema.md` §6 an iron condor arrives as **ONE row**; the
two-spread pairing rule in `CLAUDE.md` §4 is vacuous here. **0 unpaired, 0 single-sided, 0
ambiguity.** Every figure in this file is therefore **per condor**, and per condor = per position
by construction.

⚠️ **A per-leg P/L view does not exist for this bot** in either witness — no per-side `pnl` or
`risk` is recorded. Where this report says "per condor" it is not choosing between two available
views; the other view is absent. Any future comparison against a sibling bot must pair the
sibling's legs first, because **the Baseline is the only member of the 16-bot `QQQ-IC-0DTE-*`
family that exports as condor rows** — all fifteen siblings export as paired
`shortputspread` + `shortcallspread`.

### Second-witness reconciliation — clean

Ledger vs raw export, joined on `openDate`, 43 ↔ 43: **0 mismatches** on `pnl`, `risk`,
`quantity`, `credit`↔`openPrice`, `exit_price`↔`closePrice`, `mfe_pct`↔`highReturnPct`,
`mae_pct`↔`lowReturnPct`, and both MFE/MAE timestamps. `Σpnl` −31,580.00 and `Σrisk` 427,601.00
on both sides, delta 0.0000. `R = pnl/risk` reproduces the export's `ror` to rounding
(max |Δ| 4.8e-7).

**`risk` independently re-derived** from leg strikes as
`quantity × (max(put_width, call_width) − credit) × 100`: **43/43 match, max diff $0.00.** Two
rows carry an asymmetric width (call 2.0 / put 1.0) and `risk` correctly takes the larger side.
**The `risk` column is trustworthy for this bot** — which matters, because it is the R
denominator.

### ⚠️ A tier-name collision, per `evidence-standards.md` §2.1 note 4

In this project **T1–T5 are evidence *classes*, not confidence levels**: T1 LIVE, T2 PAPER, T3 OOS
BACKTEST, T4 IS BACKTEST, T5 IDEA (`evidence-standards.md` §3). **Every observation in this report
is evidence tier T1 LIVE** — real money, real fills, broker-confirmed — and that is the *least*
interesting thing about it, because T1 data at n=43 still fails gate B1. So each hypothesis below
carries **two** labels: its evidence tier (uniformly T1) and a separate **confidence** in the
*inference*, which is where the real variation is. Confidence is not a tier and must not be cited
as one.

---

## 1. The answer, in four sentences

**The exit-engine death of 2026-06-12 explains none of this loss.** The Baseline has **zero
positions on or after 2026-06-12** — its last entry was **2026-05-22**, three weeks before the
boundary. It was killed by two things acting together: **ten sessions with no exit logic at all**
(2026-03-05 → 03-18), which produced three max-loss expiries worth **94.6% of the net loss**; and
a **payoff geometry that needed an 84.6% win rate and delivered 69.8%**. The first is why the
number is large; the second is why it is negative — and per unit of risk the bot is
**unremarkable**, statistically indistinguishable from three of its siblings. **Its 38%-of-the-fleet
dominance is a position-sizing artifact, not an edge finding.**

---

## 2. What the bot was — the record vs. the tape

⚠️ **The "record claimed" column is `data/archive/bots_config.csv`, the discredited hand-written
record, proven wrong on 3 of 4 audited bots (`CLAUDE.md` §3.2). It is cited here only as a claim
about itself. No config fact in this report is read from it.** Verbatim, line 28:

```
QQQ-IC-0DTE-Baseline,IC,control,OFF,QQQ,iron_condor,0,<verify>,none (unfiltered control),
0.75% OTM,$2 (inferred: QQQ/SPY IC = $2),none,none (unstopped),,<verify>,
strike_fix=Y. Unfiltered control. Archive candidate.
```

| field | the record **claimed** | **the tape says** (n=43 condors) | verdict |
|---|---|---|---|
| Entry time | `<verify>` — blank | **13:30** on 42/43; one 14:25 (2026-03-06) | recoverable; record was silent |
| Structure | `iron_condor` | native `ironcondor`, one row | agrees |
| **Wing width** | **`$2` (self-labelled "inferred")** | **$1** on 43/43 puts and 41/43 calls; $2 call wing on exactly 2 rows | **RECORD WRONG — tape = $1** |
| Short put | `0.75% OTM` | median **0.748%** OTM | agrees |
| **Short call** | `0.75% OTM` | median **0.483%** OTM — **closer than the put on 43/43** | **RECORD WRONG — this is `strike_fix` made visible** |
| **Profit target** | **`none`** | **PT50** — 19 intraday closes, capture of credit median exactly **0.500**, min 0.500, all 19 profitable | **RECORD WRONG — tape = PT50** |
| Time exit | not a field | **15:50** — 14 closes stamped 15:50:00–15:52:22 | recoverable; record had nowhere to put it |
| Stop / hedge | `none (unstopped)` | no stop fingerprint; adverse positions ran to 15:50 or to settlement | agrees |
| **Sizing** | blank | **risk pinned $9,944/condor** (sd $63, range $9,600–$10,000), quantity solved 54–192 | recoverable; record was silent |
| Filter | `none (unfiltered control)` | consistent — its trading days are a strict superset of Range075-filtered `Fortress` over the shared window, with zero Fortress-only days | supports the record *(circumstantial)* |

**Four fields wrong or empty out of nine.** The record was not merely inaccurate; on profit target
it asserted the **opposite** of what ran, and on wing width it was wrong by 2× in the denominator
of every risk figure. This is the single most quotable finding in the file.

### The undocumented epoch break — 2026-03-19

**`bots_meta.csv` records no `epoch_boundary` for this bot, and there are two epochs.**

| epoch | n (condors) | $ | **Exp(R) per condor** | exit behaviour |
|---|---|---|---|---|
| **A — pre-arm**, 03-05 → 03-18 | **10** | **−16,460** | **−0.1653** (se 0.185) | **all 10 `expired` at 16:15 — no exit orders of any kind** |
| **B — post-arm**, 03-19 → 05-22 | **33** | **−15,120** | **−0.0460** (se 0.044) | all 33 `closed`; PT50 or 15:50 |
| **whole life** | **43** | **−31,580** | **−0.0737** | mixed — see warning |

> ⚠️ **Any statistic pooled over all 43 condors silently mixes two different configurations.** The
> headline Exp(R) −0.0737 per condor is a blend of a bot with no exits and a bot with exits. It is
> reported because it is the number the archive carries, not because it describes anything that
> ran.

Within epoch B the two exit mechanics separate cleanly, and they point opposite ways:

| mechanic | n (condors) | $ | Exp(R) per condor |
|---|---|---|---|
| **PT50** (closes 14:30–15:45, capture ≥ 0.500) | **19** | **+16,579** | **+0.0877** |
| **15:50 flat close** (13 stamps at 15:50, one 15:52) | **14** | **−31,699** | **−0.2275** |

Reconciliation: −16,460 + 16,579 − 31,699 = **−31,580** ✓. **The entire net loss of the managed
epoch sits in the 15:50 bucket** — that is, in the positions the profit target did not rescue.

---

## 3. Ranked hypotheses

Ranked by share of the loss explained. **Evidence tier is T1 LIVE for all of them** — the
variation that matters is in the confidence column.

### H1 — Ten sessions ran with no exit logic, and three of them were max losses
**Explains 94.6% of the net loss. Tier T1 LIVE · confidence HIGH · gate B1 FAIL (n=10).**

Every position opened 2026-03-05 → 03-18 is `status = expired` with a 16:15 close against a 16:00
expiration — a settlement stamp, not a fill. Three of those ten settled through a short strike for
**exactly −1.000R each**: 03-05 −$9,975, 03-09 −$9,968, 03-10 −$9,918 = **−$29,861 = 94.6% of the
bot's entire net loss, on 7% of its sample.** All three had been green intraday (MFE +0.48, +0.64,
+0.31 of credit, at 14:37 / 15:07 / 14:04) and rode straight through it.

This is **not** the 6/12 exit-engine death. It is three months earlier, it is local to this bot,
and it is a *build* state rather than a failure — the exits were not broken, they were **not there
yet**. Why they appeared on 03-19 is unrecoverable (§5.4).

### H2 — The payoff geometry required a win rate the strategy could not produce
**Explains the sign of Exp(R) in every epoch. Tier T1 LIVE · confidence HIGH · gate B1 FAIL (n=43).**

| | per condor, n = 43 |
|---|---|
| Win rate | **69.8%** (30 W / 11 L / 2 flat) |
| Mean win | **+0.1045R** (n=30) |
| Mean loss | **−0.5731R** (n=11) |
| Payoff ratio | **0.182** |
| **Breakeven win rate** | **84.6%** |
| **Shortfall** | **−14.8 pp** |
| Exp(R) | **−0.0737** (σ 0.353, se 0.054, **95% CI [−0.179, +0.032] — crosses zero**) |
| Max loss | **−1.000R exactly, on 3 condors, never worse** |

The 84.6% breakeven is the number to keep. **Two independent derivations agree to three
significant figures**: geometric, `1 − credit/width` with mean credit 15.4% of width → 84.6%; and
empirical, `mean_loss / (mean_loss + mean_win)` = 0.5731 / 0.6776 → 84.6%. A $1-wide QQQ condor
sold for 6–35¢ is a 1 : 5.5 reward-to-risk bet, and there is no exit rule that repairs a payoff
ratio.

**Max loss never breaches −1.000R**, which independently confirms the `risk` column and rules out
assignment or slippage overshoot.

### H3 — A systematically mis-selected short call strike
**Explains the direction of the tail. Tier T1 LIVE · confidence MEDIUM-HIGH on the observation,
LOW on the cause · gate B1 FAIL (n=7 breaches).**

**On 43 of 43 condors the short call sits closer to spot than the short put** — median 0.483% vs
0.748% OTM. Every sibling QQQ bot is symmetric at ~0.72–0.75% on both sides. The Baseline's call
barrier is roughly a third closer than anyone else's, and it matches `floor(underlying × 1.0075) − 1`
on 37/43 — the fingerprint of a rounding-direction defect, one to two QQQ strikes inside the
intended level.

The tail follows the skew: **8 of 11 losers were upside**, and call-side breaches carry −$33,767
against −$12,762 on the put side. Daily |move| has median 0.217% and p90 0.871%, so a 0.483%
up-barrier sits well inside the 90th percentile — it was going to be touched routinely.

This is what **`strike_fix = Y`** was flagging, and the measurement shows the flag was **earned,
not assumed**. But n=7 breaches has no power to establish the causal link, and **the cause of the
skew — mistyped selector, rounding defect, or deliberate design — is permanently unknowable**
(§5.3).

### H4 — Position sizing at 2× the family, which is why this bot dominates the fleet loss
**Explains the dollar headline, and nothing about the strategy. Tier T1 LIVE · confidence HIGH.**

Risk per position, condor-paired, across the whole `QQQ-IC-0DTE-*` family:

| bot | n (positions) | **risk / position** | **Exp(R) / position** | $ |
|---|---|---|---|---|
| **QQQ-IC-0DTE-Baseline** | **43** | **$9,944** | **−0.0737** | **−31,580** |
| HedgeD-Conditional | 51 | $4,926 | −0.0615 | −15,376 |
| HedgeA-S1 | 51 | $4,926 | −0.0499 | −12,501 |
| HedgeTest | 55 | $4,929 | −0.0414 | −11,196 |
| HedgeB-S2 | 51 | $4,926 | −0.0125 | −3,130 |
| HedgeC-S3 | 50 | $4,928 | −0.0111 | −2,702 |
| Fortress | 27 | $4,931 | −0.0146 | −1,834 |
| Fortress-NoPT50 | 24 | $4,933 | −0.0182 | −2,049 |
| Raw-HoldToExp | 47 | **$187** | −0.0354 | −303 |
| Range075-PT50-Wide2-1230PM | 27 | **$190** | +0.0157 | +78 |

*(Whole-life figures, condor-paired, risk = larger side. The Fortress rows here span the full
ledger and therefore differ from the pre-6/12 figures in `README-v1-ledger.md`, which are
epoch-scoped — both are correct for their scope.)*

**The Baseline runs 2× the Hedge/Fortress arms and ~53× the Wide2/Raw arms.** Its Exp(R) −0.0737
is statistically indistinguishable from HedgeD's −0.0615 at these sample sizes. **It is not the
worst bot in the family per unit of risk. It is the biggest.** −$31,580 vs HedgeD's −$15,376 is
almost entirely the sizing, not the strategy.

### H5 — Nineteen PT50 fills worked; the profit target simply never reached the losers
**Reframes an apparent execution failure. Tier T1 LIVE · confidence MEDIUM.**

Subagent (b) flagged **7 of the 14 time-exit closes whose mark reached ≥ 0.50 of credit and did
not fill** — in every case the mark went *strictly through* a penny-rounded target (e.g. credit
0.20, target 0.10, mark 0.09 at 14:44, closed 0.37 at 15:50). Had all 7 filled, Exp(R) would move
−0.0737 → −0.0454 per condor and P/L −$31,580 → −$19,415.

⚠️ **This must not be reported as a dead exit.** A 0.03–0.04 buyback limit on a $1-wide QQQ condor
is plausibly **unfillable**, and nothing on hand distinguishes "order never generated" from "order
generated, never filled." That distinction lives in the position's **Trades list**
(`CLAUDE.md` §3.3), which is in neither witness and is now unreachable — the account is locked.
**Flagged anomaly. Not a finding.**

### Hypotheses RULED OUT

| ruled out | evidence |
|---|---|
| **The 6/12 exit-engine death** | **n = 0 positions on or after 2026-06-12.** The split is empty for any cut date ≥ 2026-05-23. Cold. **T1, HIGH.** |
| **"It bled steadily"** | 3 condors = 94.6% of net loss; **36 of 43 condors are net positive**; median R **+0.049**. Removing the worst 5 makes the bot **+$14,184, Exp(R) +0.0377**. **T1, HIGH.** |
| **A June/July regime change** | The bot was already dead. **T1, HIGH.** |
| **Exits failed it (epoch B)** | Exits demonstrably fired: 19 PT50 fills at median capture exactly 0.500, plus 14 flat closes at 15:50. **T1, HIGH.** |
| **Scaled into a losing streak** | risk sd **$63** on a $9,944 mean; corr(prior cumulative P/L, next risk) = **−0.037**. Sizing set once, never touched. **T1, HIGH.** |
| **Discretionary shutdown after a bad run** | It stopped on the same day as **12 other bots**, inside a fleet-wide gap — the ledger has **zero legs in ISO week 2026-W22**. **T1, HIGH.** |

---

## 4. What would have helped — the counterfactual grid

Full sample, n = 43 condors. A variant fires iff the recorded mark reached the level; non-firing
positions keep their actual R.

| variant | fired (n) | Exp(R) / condor | vs actual −0.0737 |
|---|---|---|---|
| PT25 | 37 | **−0.0210** | best in grid — **still negative** |
| SL100 | 21 | −0.0222 | still negative |
| PT40 | 35 | −0.0239 | still negative |
| PT50 | 34 | −0.0366 | still negative |
| SL150 | 17 | −0.0406 | still negative |
| PT60 | 28 | −0.0489 | still negative |
| SL200 | 14 | −0.0531 | still negative |
| PT70 | 13 | −0.0764 | worse |

**No profit target and no stop level in the grid turns this bot positive.** That is the point of
the grid, and it is why H2 outranks every execution hypothesis in explanatory weight even though
H1 explains more dollars.

> ⚠️ **Every row above is an optimistic upper bound, in both columns.** `mfe_pct`/`mae_pct` are
> **marks, not fills**, sampled at the bot's Scan Speed, so they are the max *observed*, not the
> true intraday max (`oa-export-schema.md` §4). The error is **one-sided and it flatters tighter
> profit targets** — and it flatters stops too, in the opposite direction: under-sampling means
> the true MAE is worse and a real stop would have fired **more** often, cutting winners that this
> grid lets run. They are `[FIRST-HAND, UNCORROBORATED]` — **no second witness exists.**
> Treat the grid as a bound, never as an estimate.

**Two MAE values print worse than the −1.000R structural floor** (−1.101R on 03-09, −1.040R on
03-05). A 0DTE condor mid can print through max loss on width near expiry. This is a mark, not a
fill, and it is the cleanest available demonstration that **MAE must never be read as an
achievable stop price.**

**UNDECIDABLE from this data, and not guessed:** any **time-exit** counterfactual (the mark at
15:45 is not an extreme and is recorded nowhere — `oa-export-schema.md` §4); any **combined PT+SL**
rule (only the *order* of the two extremes is known, not the path); and a stop's true **cost** in
stopped-out winners (intra-scan paths are unrecorded).

---

## 5. Transferable lessons

Four of the five are already law in v2, which is the useful finding: **this bot is a
retrospective validation of rules the rebuild adopted for other reasons.** The fifth is new.

### 5.1 ✅ Already law — the config record must be captured, never written
The record was wrong on **wing width** (claimed $2, ran $1 — a 2× error in the risk denominator)
and asserted **`profit_target = none`** for a bot that demonstrably ran PT50. `CLAUDE.md` §3.2
already forbids a hand-written config record; `bots_config_v2.csv` is capture-derived. **This
forensic is the fourth audited bot on which the old record was proven wrong, taking the count to
4 of 5.**

### 5.2 ✅ Already law — compliance scoring against a wrong record certifies nothing
`compliance.csv` starts 2026-06-26 and **never scored this bot** — it had stopped trading. That
absence is the lesson: had the Baseline still been running, the G5 system would have scored it
**green** against a record claiming `profit_target = none` while PT50 fired 19 times. It was the
same defect that certified 100% for five straight days while the champion's PT25 fired zero times
(`evidence-standards.md` §7). **A compliance score measures fidelity to a document. If the
document is wrong, a green score is worse than no score.**

### 5.3 ✅ Already law — an epoch break that is not recorded is a silent data-mixing bug
Two epochs, no `epoch_boundary` in `bots_meta.csv`, and the archive's headline number blends them.
`CLAUDE.md` §5 already requires epoch boundaries in `bots_meta.csv` and forbids resetting history
by cloning. **Confirmed by counterexample.**

### 5.4 ⭐ NEW — a control that varies four things at once measures nothing
This is the finding worth carrying, and it is not yet stated anywhere in v2.

The Baseline was built as **the unfiltered control arm** for the `QQQ-IC-0DTE-*` family
(`bots_meta.csv`: `role = control`, `"unfiltered control"`). The intended comparison is legible —
hold entry, structure and strikes fixed, remove the Range075 filter, and price what the filter
buys. **That comparison was never answerable**, because the Baseline differs from every candidate
treatment arm on **four axes simultaneously**:

| | Baseline | Fortress family | Hedge tournament A–D | Wide2 / Raw |
|---|---|---|---|---|
| Wing width | **$1** | $2 | $2 | $2 |
| Short call OTM | **0.48%** | 0.70% | 0.72% | 0.73% |
| Risk / position | **$9,944** | $4,931 | $4,926 | $187 |
| Order structure | **native IC** | 2 one-sided spreads | 2 one-sided spreads | 2 one-sided spreads |
| Entry | 13:30 | 13:31 | **11:01** | 11:01–15:02 |

Against the hedge tournament it is not even **time-matched**. Against Fortress it is time-matched
and nothing else — half the wing width, double the risk, a call strike a third closer to spot, and
a different order structure. **−$31,580 bought no answer to the question it was built to ask.**

This is the same defect the 7/28 HedgeD audit found in the tournament itself — "duplicate arms,
mixed execution classes, no Range075" (`docs/history-index.md` → `hedge-research.md` §5.2). **Two
independent instances of the same failure in one v1 fleet.** The v2 discipline that addresses it
is pre-registration (`CLAUDE.md` §5) and gate **T3.5** — *"beats its control: a variant with the
tested condition removed, run over the same window"* (`evidence-standards.md` §4.5). What neither
currently says out loud is the operational corollary:

> **A control arm must differ from its treatment on exactly ONE axis, and the pre-registration
> entry should name the axis and assert the match on every other.** Naming a bot "control" does
> not make it one. This report does **not** amend either document — that is a decision, and
> decisions are gated (`CLAUDE.md` §5). It is recorded here as a candidate for the
> `evidence-standards.md` redesign pass Andy has already flagged.

### 5.5 ⭐ NEW — rank by R first, and the fleet's biggest loser may be its most ordinary bot
The Baseline is **38% of the v1 fleet loss** and, per unit of risk, **middle of its own family** —
Exp(R) −0.0737 against HedgeD's −0.0615, indistinguishable at these n. It topped the dollar table
because it ran at 2× the family's position risk, not because it was the worst strategy.
`CLAUDE.md` §4's *"compare by R, never raw P/L"* is usually cited to stop a **good** bot being
flattered by size. **This is the mirror case: raw P/L nominated the wrong bot for a forensic.**
The one genuinely anomalous thing about the Baseline — the 43/43 call-side skew — is invisible in
the dollar ranking and would have been found sooner by an R-ranked screen with a per-position risk
column beside it.

---

## 6. What cannot be established — permanently

The OA account is **locked**, no `bots_config_v2.csv` capture exists for an archived bot, and the
hand-written record is discredited. These are gone:

1. **Scan speed (1 / 5 / 15 min).** Not a field in the config schema, not derivable from the tape.
   This matters more than it looks: it is the **sampling rate of `mfe_pct`/`mae_pct`**, so the
   one-sided bias in every counterfactual in §4 is not merely present but **unquantifiable**.
2. **Exit pricing** (Market vs SmartPricing, and the % of bid-ask). The 15:50 closes resemble the
   Fortress "MARKET" convention, but nothing in the tape separates a market close from an
   aggressive smart-priced one — and correction A1 proved OA can fill a credit spread at a
   structurally impossible price under Market.
3. **The intended call-strike rule.** The *deviation* is measured (≈1.7 strikes inside +0.75%,
   matching `floor(u × 1.0075) − 1` on 37/43). **Whether it was a mistyped selector, a
   rounding-direction defect, a deliberate call-side skew, or a different selector entirely is
   undetermined** — and that distinction is the entire content of the `strike_fix` flag. It cannot
   be settled without the bot's scanner definition.
4. **Why exit logic appeared on 2026-03-19.** The break is unambiguous in the tape. Who armed it,
   what exactly was armed, and whether anything else changed at the same moment: no epoch
   boundary, no session-log entry, no capture.
5. **Whether the PT50 order was generated on the 7 anomalous positions** (§H5). Needs the Trades
   list. Nothing substitutes, and the account is locked.
6. **Whether the filter was truly `none`.** The Fortress-superset relation is strong but
   circumstantial — a weak or partial filter that happened never to block on these 43 days is not
   excluded.
7. **Why it skipped 13 sessions** that the 11:01 siblings traded (04-10, 04-13/14/15, 04-17,
   04-20, 04-24, 04-27/28, 05-01, 05-04, 05-06, 05-11). Off, throttled, unfilled or gated —
   undeterminable. This directly weakens the "unfiltered daily control" claim.
8. **Why it stopped on 2026-05-22**, and when it was switched OFF.
9. **Reentry rule, allocation figure, max-positions-per-day.** 1 condor/day at ~$10k risk is
   *consistent with* a $10k allocation at 1/day — and equally with a $50k allocation under a
   per-position cap.
10. **Fill quality / slippage.** `closePrice` is the realized price; no NBBO reference exists to
    judge it.

### Figures the lead session doubts

- **Exp(R) −0.0737 per condor** — arithmetically exact, statistically empty. 95% CI **[−0.179,
  +0.032]** crosses zero; n=43 vs the B1 bar of 100. Worse, it **pools two epochs** (§2). Quote it
  only as "the archive's headline number", never as this bot's expectancy.
- **The whole PT/SL grid** — optimistic bounds in both columns, no second witness. Not estimates.
- **The 7 PT50 non-fills** — the *observation* is solid (two witnesses on marks and prices); the
  *interpretation* as an exit failure rests on evidence that does not exist.
- **MAE values below −1.000R** — real numbers, unusable as prices.
- **`underlying_close` as a settlement proxy** in the breach detector — it is the 16:00 mark, not
  the settlement print, so the detector is unreliable within ~±0.05% of a strike. One case
  (2026-03-18, 0.017% through the short put, +0.385R) was excluded on that basis and is disclosed
  here. All six material breaches clear their strike by far more than the noise band.

---

## 7. Subagent disagreements, adjudicated by the lead

Recorded because the file would otherwise present a false unanimity.

| conflict | resolution |
|---|---|
| **PT50 fill count: 18 (a) vs 19 (b)** | **19.** Re-derived by the lead. The boundary row closes **15:45:32 at capture +0.588** — a PT fill, not a flat close; a `< 15:45` bucket cut splits it into the time bucket. The 15:50 flat-close cluster is 13 stamps at 15:50:00–15:50:32 plus one at 15:52:22 = **14**. 19 + 14 = 33 closed ✓ |
| **PT bucket P/L: (b) reported $15,379 on n=19** | **$16,579 on n=19.** (b) attached an 18-row sum to a 19-row count. Its time-exit figure (−$31,699, n=14) was correct. Reconciliation now closes exactly: −16,460 + 16,579 − 31,699 = −31,580 ✓ |
| **Loss concentration: "47.6%" (b) vs "94.6%" (a, c)** | **Both correct, different denominators.** Worst-3 = −$29,861 = **47.6% of gross loss** ($62,744 across 11 losers) = **94.6% of net loss** ($31,580). This file quotes **net** and labels it. |
| **Headline attribution: "structural" (a) vs "⅔ execution" (b) vs "94.6% pre-arm" (c)** | **Reconciled, not chosen.** Execution (H1) explains the **magnitude**; geometry (H2) explains the **sign**. Decisive test: strip epoch A entirely and epoch B still runs **Exp(R) −0.0460 per condor over n=33**, and no PT or SL level in the §4 grid turns the full sample positive. Both are real; they answer different questions. |
| **(a) "worst-but-one Exp(R) in the cohort" vs (c) "indistinguishable from siblings"** | **(c).** (a)'s ranking used a window-matched peer set; the differences (−0.0737 vs −0.0615 vs −0.0499) are inside the standard errors at these n. **No ranking claim among the QQQ IC arms is supportable.** |

---

## 8. Disposition of the corrections that pointed here

- **C3** (`data/archive/corrections.csv`, `confidence = UNVERIFIED`) — verbatim: *"38% of total
  fleet loss, never audited. Not a correction - a flag that this figure is unexamined. Forensic
  required before any IC-growth conclusion."* **This file is that forensic.** C3 can be read as
  **examined — no decision-grade signal**, which is the answer C1 already gives for the cohort.
  ⚠️ *`corrections.csv` is frozen; this report does not and must not edit it.*
- **C1** — the Baseline is `strike_fix = Y` (`bots_meta.csv`) and is **48.9% of the −$64,621
  cohort by itself.** C1 holds that decision-grade signal from that cohort is approximately nil,
  and the strike measurement in H3 shows the flag was **earned**. Every conclusion above is capped
  at research-only for that reason alone, before the sample gates are even applied.
- **No A-class correction (A1–A4) touches this bot.** Its entire life is pre-lapse — it stopped
  10 days before the A4 quarantine boundary (06-01) and 21 days before the fleet-wide exit death
  (06-12).
- **`docs/history-index.md` says nothing about it.** Sixteen removed v1 docs are indexed; five are
  per-bot execution audits (champion, HedgeD, Range075-PT50-Wide2-1230PM, DIR-PutVIX22, the
  Fortress pair). **None is the Baseline.** Outside the ledger, its only appearances in the folder
  are the C3 flag and the "unresolved at freeze" paragraph in `data/archive/README-v1-ledger.md`.

### One consequence for how the fleet number is read

The −$64,621 `strike_fix = Y` cohort figure contains **−$31,580 of Baseline loss that is not an
execution artifact.** It must **not** be netted out the way A2/A3 net out the Fortress pair's June
damage — that netting is justified by a dead exit engine, and this bot never met one. Its loss is
real, it is 94.6% attributable to a ten-session unarmed build window, and per unit of risk it is
ordinary.

---

*Standalone report. Gates nothing. Cites the frozen v1 ledger as history only, never as the state
of the fleet (`CLAUDE.md` §3.1, §10).*
