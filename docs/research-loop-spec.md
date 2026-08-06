# Research Loop — spec

*SIGNED 2026-08-04. Written 2026-08-04 in answer to "apply the research lane to each bot's results
every day." Nothing here is authorized to run until Andy signs §10. Companion to
`daily-loop-spec.md`; it runs AFTER that loop and shares its tape.*

---

## 0. The one thing this document exists to prevent

"How could this bot have made more money today," asked nightly and acted on, is the most reliable
way to overfit a strategy to noise. It is also, plausibly, the habit that killed v1 — not the dead
exit engine, but the reflex of tuning toward whatever just happened. `CLAUDE.md` §5 already blocks
the obvious forms: no changes during streaks, sizing set once at restart, pre-register before
restart.

So this loop is built with a firewall: **generation is free and daily; commitment is rare and
gated.** The loop may propose anything. It may change nothing. Its value is that it accumulates
evidence *while you wait*, not that it tells you what to do tonight.

---

## 1. Feasibility — CONFIRMED 2026-08-04, and better than assumed

The OA position export already carries maximum favourable and adverse excursion **with
minute-resolution timestamps**, populated on 1,386/1,386 rows of
`data/captures/oa_export_positions_2026-07-30.csv`:

| Column | Meaning | Sample |
|---|---|---|
| `highReturnPct` | MFE, as return on credit | `0.92592593` |
| `highReturnPctDate` | **when the peak occurred** | `2026-07-02 15:50:00` |
| `lowReturnPct` | MAE, as return on credit | `-0.4691358` |
| `lowReturnPctDate` | **when the trough occurred** | `2026-07-02 13:59:00` |
| `underlyingOpen` / `underlyingClose` | underlying context | `735.33` / `739.36` |
| `ev`, `alpha` | OA's own EV and alpha | `135.85`, `0.124` |

**This is the whole ballgame.** MFE/MAE with timestamps means a counterfactual can test whether a
price was *ever there* and *whether it was there before the exit* — which is exactly the
fill-plausibility check that makes most post-hoc "PT60 would have done better" arithmetic
worthless. No intraday feed is required.

### 1a. What it already says — DEMONSTRATION ONLY, NOT EVIDENCE

> ### 📝 CORRECTED 2026-08-05 (ruling batch release) — D-14. **The figures were right; the
> ### LABEL and one division were wrong.** Original struck below, per convention.
> **`74 (19%)` is not reproducible from its own stated definition.** Recomputed on the stated rule
> `lowReturnPct < returnPct`, n=394 same-day losers: **101, i.e. 25.6%.** The value 74 appears only
> at `lowReturnPct < returnPct − 0.05`, an **undeclared 5-point epsilon** (n=74, 18.8%); other
> epsilons give 79 at 0.02 and 66 at 0.10, and **none gives 74 under the stated rule.** Separately,
> `1,254 same-day **closed** positions` mislabels the population — 1,254 is same-day **all
> statuses**; same-day **and** `status == closed` is **n=1,136** (`expired` is not a close,
> `oa-export-schema.md` §6). The +0.111 / +1.182 medians are correct **for the all-status
> population**, so the numbers stand and only the label was wrong.
> ⭐ **The correction strengthens the conclusion below rather than weakening it:** the recovery
> rate is **roughly one loser in four**, not one in five.

~~Run over the 1,254 same-day closed positions in that capture:~~
Run over the 1,254 same-day positions in that capture (all statuses; same-day AND `status ==
closed` is n=1,136 — `expired` is not a close, `oa-export-schema.md` §6):

- median `MFE − realised return` = **+0.111** on the credit basis, n=1,254 (closed-only: **+0.125**,
  n=1,136) — 11 points of credit left on the table at the median
- 90th percentile = **+1.182**, n=1,254 (closed-only: **+1.167**, n=1,136)
- ~~of 394 losers, **74 (19%) dipped further than they finished**~~ of 394 losers,
  **101 (25.6%) had `lowReturnPct < returnPct`** — they recovered into the close

⛔ **This is frozen v1 data, pre-cutover, and it spans the June regression when exits were not
firing.** Under this project's own rules it cannot support a decision. It is reproduced here to
prove the pipeline computes, and for one directional hint worth carrying into design: **roughly
one loser in four recovers** (~~five~~ — corrected 2026-08-05, D-14), so a naive stop-loss would convert recoveries into realised losses.
The loss-side question is therefore not "add a stop" but "add a stop *only where MAE predicts
non-recovery*" — which is a testable hypothesis, not a setting.

---

## 2. Stage 9 — what runs nightly

Runs after the three-verdict brief, on the same tape. Reads `data/trades.csv`. Writes
`data/counterfactuals.csv` and appends to `data/research_log.md`.

1. For every position closed today, compute the **fixed variant set** (§3) using MFE/MAE and their
   timestamps. Each variant resolves to one of: `WOULD_HAVE_FILLED` (with the implied P/L),
   `NEVER_REACHED`, or `UNDECIDABLE` (marks were too coarse — see §6).
2. Update each open **arm** comparison (§4) with the day's realised results.
3. Emit **one line** to the brief.

`NO CANDIDATES` is the expected nightly output, exactly as `NO FINDINGS` is for the daily loop. A
loop that produces a candidate most nights is miscalibrated, not productive.

Example line:

```
RESEARCH: 23 positions · 6 variants · 4 arms · no graduations.
          nearest: PT60 on QQQ-IC-0DTE-Fortress (n=41/100, +0.08R, not significant)
```

---

## 3. The fixed variant set — declared ONCE, changed only by signature

The variants are decided in advance and held constant. Choosing variants *after* seeing the day is
storytelling, not experiment.

**Profit side** — PT40 · PT60 · PT70 (incumbent PT50 is the control)
**Loss side** — SL 100% · SL 150% · SL 200% · fixed-$ stop (`dstop`) at **1.00× and 1.50× the bot's
trailing-90-day MEDIAN credit, in dollars, held constant across positions** (`dstop` confirmed to
exist 2026-08-04). The dollar rungs are deliberately pinned to the SAME AVERAGE LEVEL as SL100 /
SL150: they are not a looser stop, they are the same stop anchored in dollars instead of percent,
and they differ only on positions whose credit departs from the bot's median — which is exactly the
population `hedge-research.md` §9 item 6 exists to test. A RISK-basis rung is not this contrast:
0.50×risk lands at ~720% of credit at the fleet's median credit/risk of 0.070 (n=1,254), beyond the
no-stop boundary.

**Conditional (trough-timing rungs)** — stop at 100% if the trough came before 13:00 · stop at 100%
if the trough came before 14:00 · stop at 200% if the trough came before 14:00. This is the §1a
non-recovery hypothesis given a proper level × cutoff rung set: measured on the v1 capture (n=394
same-day losers, demonstration only), a trough before 14:00 recovers 17.2% of the time and a trough
at or after 14:00 recovers 66.2% — the strongest discriminator the export contains.

**Time — NOT A TRACK A VARIANT.** Time exits are structurally undecidable from MFE/MAE (§6.5) and
are funded instead from the Track B allocation in §10: `Expiration` 0.015 and 0.005 against the
0.01 incumbent, a one-field edit on a cloned bot and the cheapest arm in the §9 sweep.

> ### 📝 ANNOTATED 2026-08-05 — the `0.005` (15:55) rung is UNREACHABLE. Only `0.015` funds R-2.
> **This is an annotation, not a restructure.** R-2 stands as ruled; the sentence above is
> unchanged; the Track B allocation is unchanged.
>
> **The finding.** `Expiration 0.005` fires at **15:55**. The greenfield family's
> `GF-Backstop-1552-FlatClose` is a **Repeating Events-class** automation firing at **15:52** —
> three minutes earlier — and it flat-closes the position. **A 15:55 Exit Option can therefore
> never observe a position in this family**; the backstop has already closed it. The rung is not
> merely low-information, it is structurally unobservable.
> Source: `track-b-arms-spec.md` §6.4 (*"The `0.005` (15:55) half of R-2 is NOT buildable in this
> family"*) and its §2 candidate table, row *"Time `expdays` 0.005 … ⛔ NO in this family … drop —
> §6.4, backstop preempts it"*. Corroborated by `oa-platform-reference.md` §4.1: Repeating triggers
> are **not** bound by the Bot Schedule, so the 15:52 backstop fires regardless of the Exit Options
> window.
>
> **Consequence.** **R-2's time question is served by `Expiration` 0.015 (15:45) alone** — that is
> ARM-B2. The 15:55 rung is **deferred with a stated reason**: it requires a family whose backstop
> is later than 15:55, which this family is not and should not become. It is recorded as a **cost,
> not an oversight** (`track-b-arms-spec.md` §11 item 10) and needs a decision Andy has not been
> asked for — a later-backstop family — before it can be funded.
>
> Annotation authorized by Andy 2026-08-05 (row S-6). **§10's signature and the 12-variant §3
> freeze are untouched.**

*📝 AMENDED 2026-08-04 by Andy's rulings **R-1** and **R-2** on
`docs/research-loop-review-2026-08-04.md`. **The set remains 12** — CONTROL · PT40 · PT60 · PT70 ·
SL100 · SL150 · SL200 · DSTOP_100 · DSTOP_150 · COND_100_1300 · COND_100_1400 · COND_200_1400 —
so the §10 freeze holds without a count change. `COND_200_1400` is the former `COND_MAE_1400`,
renamed; the two `TIME_*` slots are retired to Track B, not deleted from the programme.*

That is 12 variants. **The count matters and must be recorded.** Testing 12 variants across ~20
bots is 240 comparisons per day; at any conventional threshold some will look like winners by pure
chance, continuously, forever. The graduation gate (§5) must be adjusted for the variant count,
and **adding a variant opportunistically weakens the evidence for every other variant.**

---

## 4. Two tracks — and the second one is better

**Track A — counterfactual (cheap, biased).** The nightly arithmetic above. Free, instant, and
systematically optimistic about tight targets, because MFE proves a *mark* existed, not a *fill*.

**Track B — arm-splitting (costly, honest).** Run the variant as its own paper bot. Same
underlying, same entry logic, exactly one variable changed, pre-registered. It generates real
fills, real slippage, and real non-fills.

**Track B is strictly better evidence and you can afford it.** The Pro plan allows 50 bots; the
fleet uses ~18–20. Day-0 is paper. A spare slot costs nothing but configuration. The existing
`Fortress` / `-NoPT50` / `-NoFilter` / `-S2` family is already this pattern — it just is not
systematic yet.

**Rule: if a question is worth asking twice, spend a slot.** Track A is for questions that do not
justify a slot, and for pre-screening which arms are worth opening.

Priority for the first arms, given §1a: the **loss side**. `Stop Loss $` and `Touch` are both now
confirmed to exist, loss-tail behaviour is where a 0DTE premium seller lives or dies, and it is
where the fleet currently has the least evidence.

---

## 5. Graduation gate

A variant or arm becomes a **proposal** only when it clears, unchanged from `CLAUDE.md` §4:

- ~~n ≥ 100 positions, **and**~~
  **n ≥ 100 closed positions for that specific (bot, variant) pair**, where a position is a
  `trade_id` group and risk is the larger side, **and**
- ≥ 6 months elapsed, **and**
- the window spans a regime change, **and**
- it beats the control by a margin exceeding the noise, ~~**adjusted for the 12-variant count**~~
  **as tested by §10a's stratified paired sign-flip permutation test with max-T across all
  variants and bots — no Bonferroni term**, with the margin **pre-declared** rather than chosen on
  inspection.

> ### 📝 APPLIED 2026-08-05 on Andy's explicit release — two signed consequences that had been
> ### stranded in §5. **Originals struck above.**
> **1. The `n` line is R-4's signed companion text**, verbatim from
> `research-loop-review-2026-08-04.md` R-4's REPLACEMENT TEXT block. R-4 was **SIGNED 2026-08-04**
> and its §10 half was applied the same day; this half *"is signed but sits in §5, outside the
> §3/§10 application scope"* and was held. It closes the mismatch where §10 said positions are
> `trade_id` groups with `expired` excluded while §5 still said *"n ≥ 100 positions"* unqualified.
> ⚠️ **Three populations shared one symbol** before this: ledger **rows** vs **positions**; with
> vs without `expired`; **fleet-wide pooled** vs **per (bot, variant)**. This line is the last of
> the three — it is the **per-pair** gate `n`, and it is **not** §10's fleet-wide start condition
> of `n ≥ 30`. Do not conflate them.
> **2. The multiplicity clause is replaced by §10a**, added 2026-08-04 by ruling **R-5**, which
> sets the family at **9 computable variants × every bot under test** and states in its own words
> that **no Bonferroni term is applied** — so *"adjusted for the 12-variant count"* contradicted a
> signed section of this same document. ⚠️ **§10a item 2 also binds this gate: it is evaluated
> ONCE**, at a date written into `pre-registration-ledger.md` **before** n reaches 100. Re-running
> a failed gate is a new pre-registration.
> *Nothing else in §5 changed — the 6-month conjunct and the regime-change conjunct stand, and the
> third of those remains **undefined in every document** (`build-plan.md` §5, greenfield §12-12,
> `track-b-arms-spec.md` §11-6). **The gate cannot fire until it is written and signed.***

On graduation it does **not** become a config change. It becomes a **drafted, unsigned
pre-registration entry** in `pre-registration-ledger.md` for Andy to sign or reject.

Earliest possible graduation is therefore ~6 months past Day-0 — call it **February 2027** — no
matter how good anything looks in October.

---

## 5a. 📝 APPENDED 2026-08-04 — defects found by building against this spec

*Recorded here rather than silently corrected. All five are in the tracker as the blocking review
item; none is applied to the signed text above except where the code had to choose something.*

> **📝 STATUS UPDATED 2026-08-05 on Andy's explicit release.** Items **1** and **3** were
> **ruled 2026-08-04** (R-1 and R-2) and had gone stale as written — each now carries its ruling
> beneath the struck text. Item **4** is discharged: §10 is **SIGNED**, and §10a exists. Items
> **2** and **5** stand as written. *The rulings correct the SPEC; **`research_loop.py` is still
> `0.1.0-DRAFT` with three fatal defects and is still not wired into `daily.sh`.***

1. **The fixed-$ rungs as signed are redundant.** §3 wrote them as "1.0×credit and 1.5×credit",
   which is arithmetically identical to SL100 and SL150 — a percentage of credit by another name.
   As written they duplicate the SL family and waste two of twelve slots. `research_loop.py`
   implements **0.50× and 0.75× RISK** instead, a genuinely independent axis matching
   `hedge-research.md` §9's intent. ~~**This amendment is unsigned.**~~
   **📝 RULED 2026-08-04 by R-1 — applied here 2026-08-05 on Andy's explicit release.
   R-1 REJECTED BOTH the signed text AND the code's substitution.** The RISK basis is **rejected
   outright**: *"0.50×risk lands at ~720% of credit at the fleet's median credit/risk of 0.070
   (n=1,254), beyond the no-stop boundary"* — 0.75×risk is ~1,080%, and the substitution **fired
   0 times in n=1,254**, which is why the self-test never caught it. **The signed basis is
   `DSTOP_100` / `DSTOP_150` at 1.00× and 1.50× the bot's trailing-90-day MEDIAN CREDIT, in
   dollars**, applied to §3 as a dated amendment. ⚠️ **The code still implements the rejected
   RISK rungs** — this is a spec correction, not a code fix; `research_loop.py` is
   `0.1.0-DRAFT` and unfixed. ⚠️ **Open, one word from Andy** (`track-b-arms-spec.md` §11-8):
   is *"trailing-90-day median"* a **one-time** calibration or **rolling**? Rolling makes every
   re-stamp a new pre-registration under §10a.
2. **The count was wrong.** §3's prose lists 11 experimental variants while stating 12. The twelfth
   is now `CONTROL`, which earns its slot as the engine's self-test: it must reproduce the realised
   P/L, and a mismatch means the engine is wrong rather than the strategy underperforming.
3. **Both `TIME_*` variants are structurally undecidable.** MFE/MAE give extremes and their
   timestamps; the mark *at* 15:45 is neither and is recorded nowhere in the export. The first dry
   run returned 2,508 of 15,048 cells `UNDECIDABLE` — exactly those two variants × 1,254 positions.
   ~~Decide whether they keep their slots as a standing reminder that **time-exit questions require a
   Track B arm**, or are replaced.~~
   **📝 DECIDED 2026-08-04 by R-2 — applied here 2026-08-05 on Andy's explicit release:
   REPLACE BOTH, and buy the question with Track B slots.** `UNDECIDABLE` on **1,254 of 1,254**,
   confirmed. Both `TIME_*` slots are **retired from Track A** — not deleted from the programme —
   and the time question is funded *"instead from the Track B allocation in §10."* The freed slots
   went to trough-timing rungs; **the §3 set remains 12**, so the §10 freeze holds without a count
   change (`COND_200_1400` is the former `COND_MAE_1400`, renamed). ⚠️ **Only half the question is
   buyable:** R-2's `Expiration 0.005` (15:55) rung is **unreachable under the 15:52 backstop**, so
   the time question is served by **0.015 (15:45) alone** — `track-b-arms-spec.md` §6.4, ARM-B2.
4. **§10's margin and start condition were filled in by Claude, not Andy** — flagged there already.
5. **The export's sign convention is now documented** in `docs/oa-export-schema.md`
   (machine-verified, 0 mismatches on 1,386 rows). §6 below should be read alongside it.

**One defect was real code and is fixed:** the nightly summary printed a mean with no `n`, so a mean
over 7 positions and a mean over 1,254 rendered identically. `research_loop.py` now prints the
decidable count beside every mean, and its fixture carries a **verbatim real capture row** — the 18
synthetic checks were fully green while the harness was wrong, because every row in them was
hand-authored with a positive credit.

---

## 6. Known limits of MFE/MAE as evidence

1. **They are OA's numbers.** This project already refuses OA's `risk` column and derives risk from
   leg strikes (the second-witness rule). MFE/MAE are now load-bearing and have **no second
   witness** — nothing else on hand can check them. Treat as `[FIRST-HAND, UNCORROBORATED]`.
2. **They are marks, not fills.** A PT that "would have filled" at MFE might not have. The error is
   one-sided: it **biases toward optimism on tighter targets.** Never let Track A alone graduate a
   tighter-PT proposal; confirm on an arm.
3. **They are sampled at scan rate.** OA scans at 1/5/15 min per the bot's Scan Speed, so MFE is
   the max *observed*, not the true intraday max. Coarse-scan bots produce coarse excursions —
   hence the `UNDECIDABLE` verdict class.
4. **Same-day identification is by `openDate` == `closeDate`.** For 0DTE that is right; verify it
   does not silently capture non-0DTE same-day closes.
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

> ### 📝 ADDED 2026-08-05 on Andy's explicit release — **§6.5, and it closes a dangling
> ### reference.** *Verbatim from `research-loop-review-2026-08-04.md`'s D-8 REPLACEMENT TEXT.*
> **This block did not exist, and R-2's applied §3 text already cited it as `(§6.5)`** — that
> reference had been dangling since 2026-08-04. It is now resolved.
> **Why it is limit 5 and not a footnote:** D-8 was rated **FATAL** and is *"the finding with the
> longest reach."* The 81.2% → 0.0% collapse in apparent PT70 reachability across three bots is
> not a market fact; **it is the exit erasing the evidence**, and the median MFE of 0.250 on a
> PT25 bot is the signature. ⚠️ **It runs OPPOSITE to §6.2 and is much larger** — §6.2 warns of
> optimism on *tighter* targets; this censors *looser* ones out of existence entirely.
> ⛔ **Not fixable in code.** The `censored` flag **depends on `bots_config_v2.csv`** to know each
> bot's incumbent exit, and that file is written per-bot as each bot is built — so **Track A's
> honesty is gated on Phase-2 config capture.** Ruling **R-6** ("combined MFE for a paired condor
> is a Track B question") sits in the same territory and points the same way.
> ⚠️ **Consequence for the engine, unfixed:** `research_loop.py` is `0.1.0-DRAFT` and still carries
> its three fatal defects (units × 100 × quantity · the tautological `CONTROL` · this censoring).
> **It is not wired into `daily.sh` and must not be.**

---

## 7. What this loop may NEVER do

- Write to `bots_config_v2.csv`, or any bot configuration, ever.
- Propose a variant not in the §3 set.
- Change the §3 set without a signature.
- Report a variant as a winner before the §5 gate.
- Be consulted during a drawdown or a streak to justify a change. **This is the failure mode.**

---

## 8. Discovery — the slower, separate track

Track A and B explore *parameter* space around bots that already exist. Neither will ever find a
new structure. Structural discovery is a **monthly** track, not a nightly one: the mirror pillar,
`hedge-research.md`, `strategy-taxonomy.md` and the operator anchors propose candidate structures →
LEAN backtest → pre-registration → a paper slot. Running structural discovery nightly produces a
fleet of twenty bots that are all the same idea.

---

## 9. Build order

1. `scripts/research_loop.py` — Track A over `data/trades.csv`, with a validation fixture and a
   frozen version + self-hash, matching `execution_audit.py`'s pattern.
2. Wire as stage 9 of `daily.sh`; one line to the brief; must degrade cleanly at n=0.
3. Declare the §3 variant set in a signed entry.
4. Open the first loss-side arms (`Stop Loss $`, `Touch`) as paper bots with pre-registration
   entries.

---

## 10. ✅ SIGNED BY ANDY 2026-08-04 — this spec is live

- [x] **The §3 variant set is FROZEN at 12**, exactly as written. Adding a variant requires a new
      signature and resets nothing — but it weakens every other variant's evidence, so the count is
      deliberately expensive to change.
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
      *(AMENDED 2026-08-04 — ruling R-3.)*
- [x] **Track B may consume ≤ 8 bot slots**, leaving headroom under the 50-bot plan cap.
- [x] **Track A output is advisory-only.** It never enters an instruction card and never appears in
      the three verdicts.
- [x] **`research_loop.py` runs nightly from Day-0, but emits nothing until the working ledger
      holds n ≥ 30 post-cutover CLOSED POSITIONS fleet-wide**, where a position is a `trade_id`
      group (`CLAUDE.md` §4) and `expired` rows are excluded from the count
      (`oa-export-schema.md` §6). Before that it prints a single suppressed-output line, so the
      stage is exercised daily without publishing noise.
      *(AMENDED 2026-08-04 — rulings R-4, R-6 and R-7.)*

*Signed in conversation 2026-08-04 ("agreed with all"). The two values that were blank at drafting
— the margin and the start condition — were filled by Claude to the above and are subject to Andy's
correction; everything else is as Andy read it.*

*📝 AMENDED 2026-08-04 — those two values have now been corrected by Andy on
`docs/research-loop-review-2026-08-04.md`: rulings **R-3** (margin) and **R-4** (start condition).
The bullets above are the ruled text. Ruling **R-6** sets the unit of account to the POSITION
(a `trade_id` group, risk = the larger side) and rules that **combined MFE for a paired condor is a
Track B question**, so paired condors are honestly `UNDECIDABLE` for the PT family in Track A.
Ruling **R-7** stratifies `expired`: excluded from every count and from the PT family's comparison,
retained in `counterfactuals.csv` under an explicit `expired` stratum. §10a below is new and
carries ruling **R-5**.*

---

### §10a — Multiplicity and sequential control

*Added 2026-08-04 by ruling **R-5**, replacing "Bonferroni correction for the 12-variant count".*

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

> ### 📝 APPENDED 2026-08-06 — scoped retirement: dual-tested (bot, variant) pairs excluded from this family. Ruled by Andy (`decision-card-2026-08-06.md` ruling 5, RETIRE-SCOPED package). Applied on Andy's explicit "amend the plan" — this section is signed.
> **Item 1's family is scoped, R-2 precedent.** Excluded from "the 9 computable variants × every
> bot under test": any (bot, variant) pair where the bot belongs to a pre-registered live-arm
> family that runs that same variant as its own arm — at this signature: `SL100`, `SL200` and
> `DSTOP_100` on the seven `greenfield-family-spec.md` ledgers (`GF-SL100`/`GF-SL200`), and on any
> Track B arm ledger running the identical variant (`track-b-arms-spec.md` ARM-B1, `DSTOP_100`).
>
> **Rationale.** A live arm's own ledger re-entering Track A's computed family carries its own
> variant, degenerating toward the tautological-`CONTROL` defect class (§5a) — Track A would be
> testing whether the arm differs from itself. **Precedent already in this document:** the
> `TIME_*` slots were retired from §3 by ruling R-2 when the question moved to a live arm (ARM-B2);
> this is the identical move applied to the SL/DSTOP rungs. The variants **remain in §3** and
> continue to compute normally on every non-family ledger. **The set remains 12; the §10 freeze
> holds without a count change.**
>
> **Non-equivalence, not mere duplication — carried, not solved.** `greenfield-family-spec.md`
> §11 CF-4 establishes that `GF-SL100`/`GF-SL200` are **close-both** mechanics (the shared
> sibling-close force-closes the untested side), while Track A's `SL100`/`SL200` counterfactuals
> are computed **per-spread**. These are not replications of the same estimand; full record in
> `greenfield-family-spec.md` §9 and `track-b-arms-spec.md` §6.3/§5.5.
>
> **No-influence rule, carried into `pre-registration-ledger.md` PR-14…PR-20 / PR-21 / PR-22 at
> signing (Day-0, not yet applied — those entries are unsigned):** a Track A advisory read on a
> dual-tested variant may not trigger, accelerate, or veto any arm disposition before that arm's
> own pre-declared gate date. Kill authority for these variants rests solely with the arm's own
> pre-registered criteria.
>
> ⚠️ **Honesty line.** This scoping removes a degenerate self-comparison; it does **not** create
> cross-engine multiplicity accounting. Within-family multiplicity for the greenfield arms stays
> with `greenfield-family-spec.md` Phase C step C4's declared Bonferroni-across-6; Track A's stays
> with this section's max-T. No pooled alpha exists across the two engines. Recorded as a carried
> limitation, not a solved one.
