# Research loop — review ruling sheet

*Written 2026-08-04 in answer to "review this properly before it goes live." Reviews
`docs/research-loop-spec.md` (sha256 `ca927b24…1f45`) and `scripts/research_loop.py`
(sha256 `4960ab9e…6028`) as they stand on disk. Three independent adversarial reviewers —
statistics, design, code-vs-spec — each prompted to refute rather than summarise.*

> ⛔ **This file amends nothing.** It does not edit `research-loop-spec.md`, does not wire
> `research_loop.py` into `daily.sh`, and does not freeze the engine. **The §3 variant set changes
> only by signature** — the spec says so twice, at §7 (`- Change the §3 set without a signature.`)
> and at §10 (`- [x] **The §3 variant set is FROZEN at 12**, exactly as written. Adding a variant requires a new`).
> Every ruling below is a proposal with the exact replacement text pre-written, so that signing is
> a single decision and not a drafting session.

---

## 0. RULINGS — ALL SEVEN RECORDED 2026-08-04

Andy ruled all seven slots in conversation 2026-08-04: **R-1 SIGN · R-2 SIGN · R-3 SIGN · R-4 SIGN ·
R-5 SIGN · R-6 RULE position, combined MFE is a Track B question · R-7 SIGN.**

**Applied to `research-loop-spec.md` as dated amendments** (§3 and §10 only, per the authorisation):
R-1, R-2 → §3 · R-3 → §10 bullet 2 · R-4 → §10 bullet 5 · R-5 → new §10a · R-6, R-7 → recorded in
§10's amendment note. **The §3 set remains 12, so the §10 freeze holds without a count change.**

**NOT applied — signed or found, but outside the §3/§10 scope. Listed in §9.** These leave the spec
internally inconsistent in four places until ruled on separately.

## 1. Verdict

**Do not wire it in.** The signature is not the blocker — three defects are, and none of them is in
§5a:

1. **Every counterfactual P/L the engine produces is wrong by a factor of 100 × quantity.** Not a
   rounding issue — the `delta` column is not a counterfactual at all.
2. **The `CONTROL` self-test is a tautology.** `abs(pnl - pnl) < 1e-9`. The one check whose entire
   justification is catching engine error compares a variable to itself, and so did not catch (1).
3. **The §10 gate as signed can never fire, for any variant, on any data.** The median-R half is an
   unconditional `False`, and the margin is ~7× the largest effect the instrument can produce.

There is also a fourth problem that is not a bug and cannot be coded away: **MFE/MAE are censored by
the incumbent exit**, so Track A can only honestly evaluate variants *tighter* than the bot already
runs. That invalidates roughly half the current slots and is the single most important thing in this
document. It is §5 D-8.

The spec's architecture — generation free, commitment gated, Track B better than Track A — survives
intact. Nothing below argues against the loop. It argues that the loop as built would produce
confident wrong numbers nightly for months, which is the exact failure the project was rebuilt to
stop.

**Seven ruling slots follow. Three were requested; four more turned out to be load-bearing.**

---

## 2. Evidence base — read this before any number below

Every empirical figure in this sheet was computed read-only over
`data/captures/oa_export_positions_2026-07-30.csv`, **n=1,386 export rows**, of which **n=1,254 are
same-day (`openDate[:10] == closeDate[:10]`, all statuses)** and **n=1,136 are same-day and
`status == closed`**.

⛔ **This is frozen v1 pre-cutover data** (`CLAUDE.md` §3: never a reporting input). It is used here
exactly as spec §1a uses it — to establish **arithmetic feasibility**, which is a property of the
instrument and the export, not of the regime. **No figure here supports a live-capital decision, and
none is offered as one.** `data/trades.csv`, the post-cutover working ledger, is header-only:
**n=0**. Absent is not zero.

Reviewer figures that disagreed with each other were recomputed from the capture directly; the
numbers printed below are the recomputed ones, and the definition is stated wherever a definition
could differ.

---

## 3. The seven ruling slots

| # | Ruling | Recommendation | Severity if unruled |
|---|---|---|---|
| **R-1** | The fixed-$ rungs: sign or reject 0.50×/0.75× RISK | **REJECT BOTH** — as coded *and* as spec'd; sign a third value | 2 of 12 slots produce a constant |
| **R-2** | `TIME_*` slot disposition | **REPLACE BOTH**, and buy the question with 2 Track B slots | 2 of 12 slots produce a constant |
| **R-3** | §10 margin (`≥ 0.10R`, mean **and** median) | **CORRECT** — withdraw the median test, drop the margin to +0.015R | gate can never fire |
| **R-4** | §10 start condition (`n ≥ 30`) | **CORRECT** — it counts legs, not positions, and includes `expired` | starts early, on the wrong unit |
| **R-5** | Multiplicity: Bonferroni-for-12 | **CORRECT** — the family is ~180, and the real inflation is sequential | false graduation likely |
| **R-6** | Unit of account: row vs position | **RULE: position** (`trade_id` group) — and accept what it costs | flattered denominator, reintroduced |
| **R-7** | `expired` rows: close or not a close? | **STRATIFY** — exclude from counts, keep as the uncensored control | reviewers genuinely split |

---

### R-1 — the fixed-$ rungs. **Recommendation: reject as coded, and do not revert. Sign a third value.**

**Reject as coded.** `DSTOP_50R` / `DSTOP_75R` can never fire, on any real ledger row, ever. The
comparison is

```
133:                thresh = param * risk
134:                if (mae * credit) <= -thresh:
```

`credit` is a per-contract price (`build_ledger.py` writes it from `openPrice`); `risk` is dollars.
Adverse excursion in dollars is bounded by max loss, so `|mae × credit| ≤ risk / (100 × qty)`, while
firing needs `|mae × credit| ≥ param × risk` — impossible by a factor of ≥200 for any `param ≥ 0.5`
and `qty ≥ 1`. **Measured: 0 fires out of n=1,254 same-day rows, for both rungs.** They report
`+0/pos (n=1254)`, which reads as 1,254 observations of "the dollar stop is neutral" and is 1,254
observations of a comparison that cannot be true.

**And do not simply revert to the signed text either — but §5a defect 1's premise is half wrong.**
"1.0×credit" is identical to SL100 *for a single position*. OA's `dstop` is a fixed dollar typed
once and held constant; `stoploss` is a percentage re-evaluated against each position's own credit.
Across a population with dispersed credit those are **different rules**, and that dispersion is
precisely what `hedge-research.md` §9 item 6 wants tested. The signed text was **under-specified,
not redundant** — it never said *which* credit.

**And fixing the units does not rescue the risk basis.** Measured credit\$/risk\$ over n=1,254
same-day rows: p10 0.036, **median 0.0695**, p90 0.156. So 0.50×risk ≈ **720% of credit** at the
median and 0.75×risk ≈ 1,080% — far past the point `hedge-research.md` treats as effectively
no-stop. With units corrected they fire on **42/1,254 (3.3%)** and **26/1,254 (2.1%)**. They are not
an independent axis; they are two more no-stop controls, and `CONTROL` already is one.

**REPLACEMENT TEXT** — `research-loop-spec.md` §3, replacing the single line
`**Loss side** — SL 150% · SL 200% · SL 250% · fixed-$ stop at 1.0×credit and 1.5×credit (`dstop`,`
and its continuation:

```
**Loss side** — SL 100% · SL 150% · SL 200% · fixed-$ stop (`dstop`) at **1.00× and 1.50× the bot's
trailing-90-day MEDIAN credit, in dollars, held constant across positions** (`dstop` confirmed to
exist 2026-08-04). The dollar rungs are deliberately pinned to the SAME AVERAGE LEVEL as SL100 /
SL150: they are not a looser stop, they are the same stop anchored in dollars instead of percent,
and they differ only on positions whose credit departs from the bot's median — which is exactly the
population `hedge-research.md` §9 item 6 exists to test. A RISK-basis rung is not this contrast:
0.50×risk lands at ~720% of credit at the fleet's median credit/risk of 0.070 (n=1,254), beyond the
no-stop boundary.
```

☑ **RULED 2026-08-04 — SIGN as above.** Applied to `research-loop-spec.md` §3 as a dated amendment.

---

### R-2 — `TIME_1545` / `TIME_1555`. **Recommendation: replace both, and buy the question in Track B.**

Confirmed: both return `UNDECIDABLE` on 1,254 of 1,254 same-day rows. Three dispositions, ruled:

- **Keep as reminders — reject.** The cost is not only the slot. The nightly headline prints
  `{undec}/{len(recs)} cells UNDECIDABLE`, whose **floor is a hardcoded 16.67%** (2 of 12). A
  standing reminder indistinguishable from a data-quality defect is not a reminder, and the actual
  reminder already exists in prose in three places (`research_loop.py` docstring,
  `oa-export-schema.md` §4, spec §5a defect 3).
- **Drop to 10 — reject.** The multiple-comparison saving is negligible: Bonferroni z goes
  2.86 → 2.81, and required n scales as z², so dropping two slots buys **3.6%** of n. Dead slots
  should be cut because they are dead, not for the denominator.
- **Replace — recommended.** The highest-information decidable axis in the export is trough timing,
  and it currently has one slot. Measured over n=394 same-day losers, recovery defined as
  `lowReturnPct < returnPct`: **trough before 14:00 → 56/326 recovered (17.2%); trough at or after
  14:00 → 45/68 recovered (66.2%)** — a 3.9:1 discriminator on the exact §1a non-recovery
  hypothesis. On deep losers (MAE ≤ −200%, n=101): 15/56 (27%) early vs 30/45 (67%) late. One
  conditional slot cannot resolve a two-dimensional (level × cutoff) question.

**And the time question is the cheapest Track B arm available, not the most expensive.** The three
exits the spec names — 15:45 / 15:50 / 15:55 — are the OA `Expiration` control's `0.015` / `0.01` /
`0.005` settings, and the fleet already sits at `0.01`. A time arm is a **one-field edit on a
cloned bot** — cheaper than any `Stop Loss $` or `Touch` arm in the §9 build order. Spending two
Track A slots on the one question Track A provably cannot answer, while leaving it unfunded in the
track that answers it trivially, is the worst allocation on the board.

**REPLACEMENT TEXT** — §3, replacing `**Time** — exit 15:45 · 15:50 (control) · 15:55`:

```
**Conditional (trough-timing rungs)** — stop at 100% if the trough came before 13:00 · stop at 100%
if the trough came before 14:00 · stop at 200% if the trough came before 14:00. This is the §1a
non-recovery hypothesis given a proper level × cutoff rung set: measured on the v1 capture (n=394
same-day losers, demonstration only), a trough before 14:00 recovers 17.2% of the time and a trough
at or after 14:00 recovers 66.2% — the strongest discriminator the export contains.

**Time — NOT A TRACK A VARIANT.** Time exits are structurally undecidable from MFE/MAE (§6.5) and
are funded instead from the Track B allocation in §10: `Expiration` 0.015 and 0.005 against the
0.01 incumbent, a one-field edit on a cloned bot and the cheapest arm in the §9 sweep.
```

☑ **RULED 2026-08-04 — SIGN as above.** Applied to `research-loop-spec.md` §3 as a dated amendment. Set stays at 12; `TIME_*` retired to Track B.

---

### R-3 — the §10 margin. **Recommendation: correct. As signed the gate cannot fire.**

The signed text:

```
      median R**, by **≥ 0.10R per position**, with a 95% confidence interval that excludes zero
```

**The median half is an unconditional `False`.** Every non-triggering position yields `delta = 0.0`
*exactly*, and those rows are included in the variant's family. So the median is nonzero only if the
variant fires on more than half of all positions. Measured, corrected units, n=1,254 same-day rows:

| variant | fires | rate | mean ΔR | **median ΔR** |
|---|---|---|---|---|
| PT40 | 749 | 59.7% | +0.0093 | **0.0000** |
| PT60 | 461 | 36.8% | −0.0024 | **0.0000** |
| PT70 | 299 | 23.8% | −0.0020 | **0.0000** |
| SL75 | 331 | 26.4% | +0.0150 | **0.0000** |
| SL100 | 279 | 22.2% | +0.0132 | **0.0000** |
| SL150 | 200 | 15.9% | +0.0114 | **0.0000** |
| SL200 | 172 | 13.7% | +0.0083 | **0.0000** |
| SL250 | 154 | 12.3% | +0.0048 | **0.0000** |
| DSTOP_50R | 42 | 3.3% | +0.0050 | **0.0000** |
| DSTOP_75R | 26 | 2.1% | +0.0025 | **0.0000** |
| COND_MAE_1400 | 99 | 7.9% | +0.0012 | **0.0000** |

**Eleven of eleven have a median ΔR of exactly zero** — including PT40, the only variant clearing a
50% trigger rate, because its triggered deltas straddle zero. "Wins on **both** mean and median" is
therefore `something AND False`.

**And the margin is unreachable independently.** R is on the `ror` basis. At median credit/risk
0.0695 (n=1,254), moving a profit target from 50% to 70% of credit changes P/L by 0.20 × credit =
**0.014R on the positions where it fires** — that is the arithmetic ceiling. The largest mean effect
any variant produces on the capture is **SL75 at +0.0150R (n=1,254)**. The signed margin of 0.10R is
**~7× the largest observable effect** and ~50× the median-credit ceiling for a PT move.

This is not conservatism. A gate that mathematically cannot open is not a high bar, it is a nullity —
and it is dangerous, because the first thing that ever crosses 0.10R will be a units bug, not a
discovery. Note that R-6's units fix is a prerequisite: the current engine reports dollars, so
nothing above is what it would print today.

**REPLACEMENT TEXT** — §10 bullet 2, replacing both lines:

```
- [x] **Pre-declared margin.** A variant beats the control only if all three hold:
      (a) its **mean ΔR ≥ +0.015R per position** over that bot's full post-cutover population;
      (b) a **paired bootstrap 95% CI on that mean excludes zero** under the §10a procedure; and
      (c) on the **subpopulation where the variant actually fires**, a paired sign test against the
      control is significant at the same level.
      **The median-ΔR test is WITHDRAWN.** A non-triggering position contributes an exact 0.0, so
      the median is pinned at 0.0000R for any variant firing on under half of positions — measured
      0.0000R for 11 of 11 variants on n=1,254 v1 rows. It is not a statistic.
      **+0.015R is calibrated, not chosen:** the arithmetic ceiling on a PT50→PT70 move at the
      fleet's median credit/risk of 0.070 is 0.014R per fired position, so the previously declared
      0.10R was unreachable by construction. Declared here, before any post-cutover data.
```

☑ **RULED 2026-08-04 — SIGN as above.** Applied to `research-loop-spec.md` §10 bullet 2 as a dated amendment.

---

### R-4 — the §10 start condition. **Recommendation: correct. It counts the wrong thing.**

Signed: `- [x] **`research_loop.py` runs nightly from Day-0, but emits nothing until n ≥ 30 post-cutover`
… closed positions.

The code's `n` is `len(rows)` after this filter:

```
169:            if (r.get("status") or "").lower() in ("closed", "expired")]
```

Three mismatches with the signed words. It counts **ledger rows, not positions** (R-6); it includes
**`expired`**, which `oa-export-schema.md` states is not a close (`**`expired` is not a close**` —
n=154 of 1,386 export rows, n=118 of the 1,254 same-day rows); and it is **fleet-wide across all
bots pooled**, whereas §5's gate `n` is per bot per variant. Same symbol, three populations, none
qualified in the signed text.

**REPLACEMENT TEXT** — §10 bullet 5, and §5's `- n ≥ 100 positions, **and**`:

```
- [x] **`research_loop.py` runs nightly from Day-0, but emits nothing until the working ledger holds
      n ≥ 30 post-cutover CLOSED POSITIONS fleet-wide**, where a position is a `trade_id` group
      (`CLAUDE.md` §4) and `expired` rows are excluded from the count (`oa-export-schema.md` §6).
      Before that it prints a single suppressed-output line, so the stage is exercised daily without
      publishing noise.
```
```
- n ≥ 100 closed positions **for that specific (bot, variant) pair**, where a position is a
  `trade_id` group and risk is the larger side, **and**
```

☑ **RULED 2026-08-04 — SIGN as above.** §10 bullet 5 amended. ⚠️ The companion §5 line (`- n ≥ 100 positions, **and**`) is signed but sits in §5, outside the §3/§10 application scope — NOT yet applied, see §9.

---

### R-5 — the multiplicity correction. **Recommendation: correct. Bonferroni-for-12 is wrong on three axes.**

Signed: `      **after Bonferroni correction for the 12-variant count**. Declared here, before any data —`

The spec contradicts itself four lines apart. §3 says
`That is 12 variants. **The count matters and must be recorded.** Testing 12 variants across ~20`
bots is 240 comparisons per day — then §10 corrects for 12.

1. **12 is not even the within-bot family.** `CONTROL` is a self-test, not a comparison, and both
   `TIME_*` emit no delta. **The real per-bot family is 9.**
2. **The bot dimension is dropped.** 9 × ~20 bots = **~180 comparisons**, not 12. α = 0.05/12 =
   4.2×10⁻³ against a required ~2.8×10⁻⁴ — roughly a **15× under-correction**, anti-conservative.
3. **The real inflation is sequential and is not addressed at all.** The gate is re-evaluated
   nightly as n accumulates toward 100 (the spec's own example line reads `n=41/100`). That is
   unlimited optional stopping. Nothing in §10 or the code caps peeks.

Working the other way: the variants are evaluated on the *same* positions and are strongly
correlated, so Bonferroni over-corrects within a bot by roughly 1.5×. That does not come close to
offsetting (2) and (3).

**REPLACEMENT TEXT** — new §10a:

```
### §10a — Multiplicity and sequential control

1. **The family is the 9 computable variants × every bot under test**, re-stated in each night's
   log. `CONTROL` and any structurally-undecidable slot are not comparisons and are not counted.
2. **No nightly gate evaluation.** Track A output is descriptive every night. The gate is evaluated
   ONCE, at the pre-declared n=100 for that (bot, variant), on a date written into
   `pre-registration-ledger.md` BEFORE n reaches 100. Re-running a failed gate is a new
   pre-registration.
3. **The test is a stratified paired sign-flip permutation test** on the per-position ΔR vector,
   strata = bot, with max-T across all variants and bots, 10,000 sign-flips. It is exactly
   calibrated on a zero-inflated skewed distribution (no normal approximation) and the max-T null
   absorbs the inter-variant correlation, so **no Bonferroni term is applied**.
4. Any nightly monitoring of the gate statistic must use an **always-valid confidence sequence**,
   not a fixed-n CI.
```

☑ **RULED 2026-08-04 — SIGN as above.** Added to `research-loop-spec.md` as new §10a.

---

### R-6 — unit of account. **Recommendation: rule POSITION, and accept what it costs.**

`CLAUDE.md` §4 is unambiguous: the unit is the position, a condor is its two spread rows paired by
`trade_id`, risk is the larger side, and "Any condor Exp(R) computed before the 2026-07-31
denominator fix is the flattered number." **The engine never groups by `trade_id`** — it iterates
raw rows, and copies `trade_id` to the output as a label it never uses. It takes each leg's own
`risk`.

Scale of the issue: of n=1,386 export rows, only **102 are native `ironcondor`** (plus 25
`ironbutterfly`); **1,246 are single-sided legs** (687 `shortputspread` + 559 `shortcallspread`)
that `build_ledger.py` pairs into condors on a time window. So `n` is ~2× the position count for
legged bots and 1× for native-IC bots — an inconsistent denominator across the fleet, applied to
every threshold in §5 and §10.

**The cost of ruling correctly, stated plainly:** per-leg MFE cannot reconstruct a condor's combined
MFE. OA applies a PT to the *combined* position; "the put leg peaked at 0.60" is not "the condor
peaked at 0.60". Ruling POSITION therefore means paired condors are **honestly `UNDECIDABLE` for the
PT family**, and Track A's decidable population shrinks toward native `ironcondor` rows and
genuinely single-sided bots. That is a real reduction in scope. It is also the correct answer, and
it is the same class of error the 2026-07-31 denominator fix already corrected once.

☑ **RULED 2026-08-04 — RULE: position, and treat combined MFE as a Track B question.** Recorded in §10's amendment note. ⚠️ No pre-written replacement block existed for this slot; spec text for §4/§6 still needs drafting — see §9.

---

### R-7 — `expired` rows. **Recommendation: stratify. The reviewers split, and both are right.**

Against including them: `oa-export-schema.md` §6 says `expired` is not a close, and
`execution_audit.py` excludes it from PT-consistency because a ride to worthless captures 1.00 and
is not a PT fill. Included, those rows carry `mfe_pct ≈ 1.00` and realised = full credit, so every
PT variant reports a structural negative delta from positions that had no exit to counterfactual —
n=118 of the 1,254 same-day rows.

For including them: a ride to worthless is the **least censored observation in the file** (see D-8),
and censoring is the biggest threat to Track A's validity. Throwing them away discards exactly the
rows that show what the tape would have offered an unstopped bot.

**Recommendation:** exclude `expired` from every *count* (`n≥30`, `n≥100`) and from the PT family's
comparison, but retain the rows in `counterfactuals.csv` under an explicit `expired` stratum, and
report the stratum's size beside every aggregate.

☑ **RULED 2026-08-04 — SIGN as above.** Stratify: excluded from counts and the PT comparison, retained under an `expired` stratum. Recorded in §10's amendment note.

---

## 4. The five §5a defects — ruling and replacement text

| §5a | Defect as recorded | Ruling |
|---|---|---|
| 1 | fixed-$ rungs redundant; code substitutes 0.50×/0.75× RISK, unsigned | **PARTLY WRONG → R-1.** The premise ("identical to SL100/SL150") holds per position but not across a population — the signed text was under-specified, not redundant. The substitution is worse than what it replaced: 0 fires in n=1,254. Sign the third value in R-1. |
| 2 | count was wrong; the twelfth is `CONTROL`, "which earns its slot as the engine's self-test" | **HALF CONFIRMED.** The count arithmetic is right (11 experimental + 1 control). The claim quoted at spec line 153 is **false as implemented** — see D-7. Also note `TIME_1550`, the control the signed §3 names, was silently deleted; only the `dstop` change is flagged as an amendment. |
| 3 | both `TIME_*` structurally undecidable | **CONFIRMED**, 1,254/1,254. Disposition → R-2. |
| 4 | §10's margin and start condition were filled in by Claude | **CONFIRMED, and both are wrong** → R-3 (margin), R-4 (start condition), R-5 (correction). |
| 5 | the export's sign convention is now documented | **CONFIRMED but incomplete.** Documenting the convention fixed the **sign** and left the **scale** wrong — see D-6. `oa-export-schema.md` §6 already warns `Every per-contract identity above needs the `× quantity`` term; `research_loop.py` never reads `quantity` at all. |

**REPLACEMENT TEXT** for §5a defect 2's second sentence (spec line 153 onward), if R-6/D-7 are signed:

```
2. **The count was wrong.** §3's prose lists 11 experimental variants while stating 12. The twelfth
   is now `CONTROL`, which earns its slot ONLY IF it independently recomputes realised P/L from the
   export's own verified identity (`pnl == (openPrice − closePrice) × 100 × quantity`,
   `oa-export-schema.md` §3) and compares that to the recorded `pnl`. As first implemented it
   compared `pnl` to itself and could never fail; that is corrected before the engine is frozen.
   `CONTROL` is not a comparison and does not enter the multiplicity family (§10a).
```

---

## 5. Defects this review found that §5a does not record

| # | Defect | Severity |
|---|---|---|
| **D-6** | Every `cf` and `delta` is off by 100 × quantity — price units subtracted from dollars | **FATAL** |
| **D-7** | `CONTROL` is a tautology; the "engine is wrong" abort is dead code | **FATAL** |
| **D-8** | MFE/MAE are censored by the incumbent exit — looser variants cannot be evaluated at all | **FATAL** |
| **D-9** | The nightly summary is a descending-ranked top-4 leaderboard — spec §7 forbids exactly this | MATERIAL |
| **D-10** | `COND_*` uses the trough time as a proxy for the breach time; one-sided, unflagged | MATERIAL |
| **D-11** | `mfe_date` is never read — §1's headline "was it there *before the exit*" is unimplemented | MATERIAL |
| **D-12** | No same-day / 0DTE filter (§6.4's "verify it does not silently capture non-0DTE" was not done) | MATERIAL |
| **D-13** | Reprocesses the whole ledger nightly with `"w"`, clobbering history; `research_log.md` never written | MATERIAL |
| **D-14** | §1a's `74 (19%)` recovery figure is not reproducible from its own stated definition | MATERIAL |

### D-6 — the units. Every counterfactual number is wrong.

```
115:                cf = param * credit
```

`credit` is a per-contract price; `pnl` is dollars. Worked on the fixture's own verbatim real row
(credit 0.5, risk 950, pnl 35, mfe 0.84, qty 1): the code yields `PT70 cf=0.35, delta=−34.65`. That
position closed at exactly 70% of credit, so **the true delta is 0.00** — the engine reports that a
profit target set precisely where the position actually exited would have lost $34.65. Because
`cf` is two orders of magnitude smaller than `pnl` on every `FILLED` row, `delta ≈ −pnl`: the delta
column is not a counterfactual, it is the negated realised P/L of whichever subset the variant
selects.

**The fixture cannot catch this and does not.** Of its 23 checks, **21 assert only a verdict
string**; verdicts depend on dimensionless ratios that units cannot break. The one numeric assertion
(`V17`) uses a synthetic row where `credit="100"` is implicitly dollars — it is a regression test
*for* the bug. There is **no real-row check on the `dstop` family**, the one family whose verdict
does depend on units. So the "verbatim real capture row" defence from `oa-export-schema.md` §5 was
satisfied in form and not in substance: a real row was added, and nothing asserts a value on it.

### D-7 — the CONTROL tautology.

```
108:            ok = abs(pnl - pnl) < 1e-9
```

`pnl - pnl` is `0.0` for every finite float. `CONTROL_MISMATCH` is unreachable, and with it the
`THE ENGINE IS WRONG` abort. Fixture checks V4 and V21 assert `"CONTROL_OK" == "CONTROL_OK"` by
construction. This is the one check whose entire justification is catching engine error, and it is
exactly the check that would have caught D-6.

### D-8 — censoring by the incumbent exit. The finding with the longest reach.

MFE/MAE accumulate only until the position closed. A position the incumbent PT closed at +50% has
`mfe_pct ≈ 0.50` and **can never evidence 0.70**. The engine scores that `NEVER_REACHED` and writes
`delta = 0.0` — asserting "position unchanged" for a position that under PT70 would still have been
open. `CLAUDE.md` §3: an absent number is not a zero.

Measured over same-day rows, by bot:

| bot | n | MFE ≥ 0.70 | closed within 0.02 of own peak | median MFE |
|---|---|---|---|---|
| `QQQ-IC-0DTE-Raw-HoldToExp` (no PT) | 80 | **65 (81.2%)** | 2 (2.5%) | **1.000** |
| `IC-SPX-FastPT25-S2` (PT25) | 364 | **39 (10.7%)** | 181 (49.7%) | 0.286 |
| `IC-SPX-FastPT25-S2-130PM` (PT25) | 70 | **0 (0.0%)** | 34 (48.6%) | 0.250 |

An 81% → 0% collapse in apparent PT70 reachability is not a market fact. It is the exit erasing the
evidence — note the median MFE of 0.250 on a PT25 bot, which is the signature.

**The general law, which the spec does not state:** *Track A can only evaluate variants **tighter**
than the incumbent exit on the same side. Every looser variant is right-censored, and its
`NEVER_REACHED` verdict is a false negative rather than a null result.* This runs **opposite** to
the bias §6.2 documents (`2. **They are marks, not fills.** A PT that "would have filled" at MFE might not have. The error is`
one-sided, biasing toward optimism on tighter targets) and is much larger.

**REPLACEMENT TEXT** — new §6 limit 5:

```
5. **⛔ CENSORING BY THE INCUMBENT EXIT — the largest bias, and it runs opposite to §6.2.**
   MFE/MAE accumulate only until the position closed. A position the incumbent PT closed at +50%
   has `mfe_pct ≈ 0.50` and can never evidence 0.70. **Track A can only evaluate variants TIGHTER
   than the incumbent exit on the same side; every looser variant is right-censored and its
   `NEVER_REACHED` verdict is a false negative, not a null result.** A `delta = 0.0` on a censored
   cell is a fabricated zero (`CLAUDE.md` §3). Measured on the v1 capture, demonstration only:
   `QQQ-IC-0DTE-Raw-HoldToExp` (no PT) shows MFE ≥ 0.70 on 65/80 positions (81.2%, median MFE
   1.000); `IC-SPX-FastPT25-S2` (PT25) on 39/364 (10.7%, median MFE 0.286); its `-130PM` clone on
   0/70 (0.0%, median MFE 0.250). The difference is the exit, not the tape.
   **Rule: the engine must carry a per-position `censored` flag and every looser-side variant must
   report `CENSORED`, never `NEVER_REACHED`. Looser-side questions are Track B questions.**
```

### D-9 — the nightly line is a leaderboard.

```
203:    for v in sorted(fam, key=lambda k: -statistics.mean(fam[k])):
213:        print("          " + " · ".join(parts[:4]) + "  [ADVISORY ONLY]")
```

Descending sort plus truncation to four is a podium, and spec §7 forbids
`- Report a variant as a winner before the §5 gate.` The `[ADVISORY ONLY]` suffix labels a ranking,
it does not cure one. It is worse than cosmetic because D-6 makes the ranking an artefact: with
`delta ≈ −pnl`, a variant ranks high purely by how much realised loss it selects, so the headline
becomes "a stop loss saves you $N per position", printed nightly, years before the gate opens.
`parts[:4]` also drops 5 of 9 families with no "showing 4 of 9".

### D-10 — trough time is not breach time.

`lowReturnPctDate` is when the extreme occurred, which is at or *after* the first crossing of the
stop level. So `mae_t < 14:00` is strictly stronger than `breach < 14:00`: a position that crossed
−200% at 13:50 and bottomed at 15:30 is scored `NEVER_REACHED` though the stop would have fired.
`COND_*` therefore **systematically under-counts fills** and understates the §1a hypothesis; it
never over-counts. The variant's own note text silently rewrote "breached" to "trough", and unlike
the `dstop` change this substitution is recorded nowhere.

### D-11 — `mfe_date` is never read.

The only timestamp loaded is `mae_date` (`    mae_t  = _hhmm(row.get("mae_date"))`). Spec §1's
headline claim is that timestamps let a counterfactual test "whether it was there *before the
exit*… the fill-plausibility check that makes most post-hoc 'PT60 would have done better' arithmetic
worthless." **That check does not exist**, and what is implemented is the form the spec calls
worthless. On the fixture's own real row the engine would report a PT fill at a peak dated
2026-07-01 and an SL fill at a trough dated 2026-06-29 — the stop preceding the peak by two days,
with nothing flagging that the two are mutually exclusive.

### D-12 — no same-day filter.

§6.4 says `4. **Same-day identification is by `openDate` == `closeDate`.** For 0DTE that is right; verify it`
does not silently capture non-0DTE same-day closes. **No such filter exists in the code**, and
`_hhmm` discards the date entirely, so `mae_t < cutoff` on a multi-day position asks whether a
trough's clock time was before 14:00 on an arbitrary day. The fixture's own real row is a 3DTE
position whose MFE and MAE fall on different days, narrated in a comment as if it were an intraday
fact. Separately: the OA-Mirror pillar is multi-day and watch-only, and its positions would be
pooled into the same per-variant mean — blending pillars, which the three-verdict contract forbids.

### D-13 — history is clobbered nightly.

`run()` reads the whole ledger with no date filter and writes with `"w"`. Each night rebuilds every
cell for all history and truncates the file, so the `engine_version` / `engine_hash` stamped on each
row is destroyed the moment a newer engine runs — which defeats the purpose of stamping it.
`data/research_log.md`, which §2 requires, is never written; the literal `NO CANDIDATES` that §2
declares as the expected nightly output is never printed.

### D-14 — §1a's recovery figure cannot be reproduced from its own definition.

`- of 394 losers, **74 (19%) dipped further than they finished** — they recovered into the close`

Recomputed on the stated definition (`lowReturnPct < returnPct`, n=394 same-day losers):
**101, i.e. 25.6%** — not 74/19%. The value 74 appears only at `lowReturnPct < returnPct − 0.05`, an
undeclared 5-point epsilon (n=74, 18.8%). Other epsilons give 79 at 0.02 and 66 at 0.10; none give
74 under the stated rule.

Also `Run over the 1,254 same-day closed positions in that capture:` — 1,254 is same-day **all
statuses**; same-day *and closed* is **n=1,136**, on which the medians shift: MFE − realised median
**+0.125** (not +0.111) and p90 **+1.167** (not +1.182). The +0.111 / +1.182 figures are correct for
the all-status population, so the numbers are right and the **label** is wrong.

The direction matters: the corrected recovery rate is **roughly one loser in four**, not one in
five, which *strengthens* §1a's "a naive stop-loss would convert recoveries into realised losses"
conclusion. But a load-bearing figure no auditor can regenerate is the exact failure
`oa-export-schema.md` was written to prevent.

**REPLACEMENT TEXT** — §1a's three bullets and the sentence that follows:

```
Run over the 1,254 same-day positions in that capture (all statuses; same-day AND `status == closed`
is n=1,136 — `expired` is not a close, `oa-export-schema.md` §6):

- median `MFE − realised return` = **+0.111** on the credit basis, n=1,254 (closed-only: +0.125, n=1,136)
- 90th percentile = **+1.182**, n=1,254 (closed-only: +1.167, n=1,136)
- of 394 losers, **101 (25.6%) had `lowReturnPct < returnPct`** — they recovered into the close
```
and: `**roughly one loser in four recovers**`

---

## 6. Reviewer objections — what survived, what did not

**Surviving, statistics (a):** gate not computable from `counterfactuals.csv` at all — `risk` and
`open_date` are never written, so R is unrecoverable downstream and the "≥6 months" clause cannot be
evaluated from the file; no median, CI, or correction exists anywhere in the code; the printed `n`
counts `NEVER_REACHED` rows, so a variant firing 26 times prints `(n=1254)`; the mean is rounded to
whole dollars with `:+.0f` and carries no unit label; `n≥100` and `n≥30` are in different units and
neither is scoped; "spans a regime change" has no definition and no detector anywhere in the repo.
Also, contrary to expectation, **n=100 is over-powered, not under-powered**, for a 0.10R margin
(per-position `ror` sd = 0.195, n=1,386) — the margin's problem is its size, not the sample.

**Surviving, design (b):** censoring (D-8); the set's own **#1 ordered sweep item is missing** —
`hedge-research.md` §9 opens `1. **SL100 + SL150 on the Range075-filtered base**, controls SL50 / current / Unstopped. Fills`
the empty middle, and SL100 is absent from §3 while SL250 (12.3% fire rate, n=1,254) occupies a slot
past the no-stop boundary; the loss rungs cluster where marginal separation is 6–28 positions while
the 159-position gap between SL50 and SL75 is unsampled; the profit ladder is centred on a PT50
control that the fleet's highest-n bot does not run (`IC-SPX-FastPT25-S2` is PT25, n=364 of 1,254 =
29%); Track B's ≤8 slots are capped and never allocated, leaving the one question Track A cannot
answer unfunded in the track that can.

**Surviving, code (c):** D-6, D-7, D-9 through D-13, plus: the engine diverges from the
`execution_audit.py` pattern §9 requires (`FROZEN_ON = None` and never read, no `ROOT` anchoring, no
version banner in `run()`, no `_meta.json` receipt); the missing-ledger branch prints a cheerful
"pre-Day-0" whenever cwd is wrong, since `build_ledger.py` always writes `data/trades.csv` even at
n=0, so its absence never means pre-Day-0; `os.makedirs(os.path.dirname(out))` raises on a bare
filename; `self_hash()` is recomputed once per output record (15,048 file reads per run at capture
scale).

**Discarded, with reason:**

- *"`--ledger data/trades.csv` violates `CLAUDE.md` §3."* — No. `data/trades.csv` is the
  **post-cutover working ledger** written by `build_ledger.py`; the frozen v1 ledger is
  `data/archive/trades.csv` and is not referenced. Downgraded to the cwd/false-green point above.
- *"12 variants is too many — cut for the Bonferroni penalty."* — The family-size cost is 3.6% of
  required n going 12 → 10. Cut dead slots because they are dead. §3's warning that adding a variant
  "weakens the evidence for every other variant" overstates the statistical cost at this scale; the
  real cost of the frozen count is the signature, which is the right reason to keep it expensive.
- *"MFE-is-a-mark-not-a-fill invalidates the gate."* — Correctly handled: §6.2 states it, and the
  spec forbids Track-A-only graduation of a tighter-PT proposal.
- *"MFE/MAE have no second witness."* — Disclosed and correctly tiered
  `[FIRST-HAND, UNCORROBORATED]` in both the spec and `oa-export-schema.md`.
- *"`Touch` and the Range075 × SL% grid are missing from §3."* — Correctly missing. Neither is
  expressible as a per-position MFE/MAE counterfactual; §8 and §9 already place them in Track B and
  LEAN.
- *"`74/394 = 19%` is an arithmetic error."* — 18.78% rounds to 19%. The defect is the numerator's
  provenance, not the division (D-14).
- *"n≥100 is underpowered for 0.10R."* — Computed and false; the opposite holds.
- *"`recs[0]` crashes on an empty list."* — Unreachable: `evaluate()` yields 12 tuples per row
  unconditionally and the call is guarded by `n ≥ 30`.
- *"`x["delta"] == ""` is a float-vs-string comparison bug."* — Correct as written; `float == ""`
  is `False` and never raises.
- *"`abs(_prem)` mishandles debit structures."* — No; `abs(premium) == openPrice × 100 × qty` holds
  for both signs (0 mismatches, n=1,386). Only the scale is wrong (D-6).
- *"`NEVER_REACHED` zeros contaminate the family mean."* — Defensible on its own: an unchanged
  position genuinely contributes zero. It becomes fatal only for the **median** criterion (R-3) and
  only where the zero is fabricated by censoring (D-8).

---

## 7. Recommended order of work

1. **Rule R-1 … R-7.** Nothing else can be sequenced until the variant set and the gate are settled.
2. **Fix D-6 (units) and D-7 (CONTROL) before anything else in code.** A real CONTROL that
   recomputes P/L from `(openPrice − closePrice) × 100 × quantity` catches the whole D-6 class, and
   every number the engine has ever printed is wrong until both land.
3. **Add the fixture checks that would have caught them:** real-row assertions on `cf` and `delta`
   (not verdict strings), a real-row `dstop` check, and one end-to-end `run()` check over a
   30-row temp ledger.
4. **Then D-8's `censored` flag**, which requires `bots_config_v2.csv` to know each bot's incumbent
   exit — so Track A's honesty is blocked on Phase-2 config capture. Worth knowing now.
5. **Then D-12, D-13, D-9**, then the `execution_audit.py`-pattern items, then freeze, then wire.
6. **Track B first arms are unaffected by all of the above** and remain the better half of the
   program. If anything, this review argues for starting them sooner: every finding here is a limit
   on Track A, and none of them applies to an arm.

---

## 8. Verification record

- Source files read directly from the device; sha256 recorded in the header line above.
- **27 quotations** in this file were asserted **byte-exact and single-match** against their source
  files by substring count; **0 were not single-match.** Every quote resolves to exactly one line:
  `research-loop-spec.md` lines 45, 49, 89, 91, 94, 128, 153, 177, 183, 192, 193, 221, 225, 226,
  231; `research_loop.py` lines 99, 108, 115, 133, 134, 169, 203, 207, 213; `oa-export-schema.md`
  lines 87, 95; `hedge-research.md` line 318.
- Every empirical figure recomputed independently from
  `data/captures/oa_export_positions_2026-07-30.csv` (n=1,386) rather than taken from a reviewer.
  Where reviewers disagreed — PT40's trigger rate, the trough-timing recovery split — the
  recomputed value is the one printed, with its definition stated.
- All capture-derived figures are **v1 pre-cutover, demonstration only**, per spec §1a and
  `CLAUDE.md` §3. `data/trades.csv` holds **n=0**.
- No file in the repo was modified by this review except this one. `research-loop-spec.md`,
  `research_loop.py` and `daily.sh` are untouched.

**Changed files for Andy's commit:** `docs/research-loop-review-2026-08-04.md` (new).

---

## 9. Not applied — the spec is internally inconsistent until these are ruled

Andy's authorisation covered the signed REPLACEMENT TEXT blocks for **§3 and §10**. These four sit
elsewhere and were deliberately left alone. Each is one word from being applied.

1. **§5's gate line** — `- n ≥ 100 positions, **and**`. Signed verbatim inside R-4's block, but it
   lands in §5. Until applied, §10 says "positions are `trade_id` groups, `expired` excluded" while
   §5 still says "n ≥ 100 positions" unqualified.
2. **§5's `**adjusted for the 12-variant count**`** — now contradicted by §10a, which sets the
   family at 9 × bots and applies no Bonferroni term. Not covered by any signed block.
3. **§6 limit 5, the censoring block (D-8)** — drafted in §5 of this sheet, never put to signature
   because it was a finding rather than a ruling slot. ⚠️ **R-2's applied text references `(§6.5)`,
   which does not yet exist** — that reference dangles until this block is added. R-6's ruling
   ("combined MFE is a Track B question") is the same territory and argues for adding it.
4. **§1a's recovery figures (D-14)** and **§5a defect 2's rewrite** — both drafted here, neither
   signed. §1a still reads `74 (19%)`, which is not reproducible from its own stated definition;
   the correct value is 101/394 = 25.6%.

Recommended: rule 1–3 together, since each is a direct consequence of a ruling already signed.
