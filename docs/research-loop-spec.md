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

Run over the 1,254 same-day closed positions in that capture:

- median `MFE − realised return` = **+0.111** (11 points of credit left on the table at the median)
- 90th percentile = **+1.182**
- of 394 losers, **74 (19%) dipped further than they finished** — they recovered into the close

⛔ **This is frozen v1 data, pre-cutover, and it spans the June regression when exits were not
firing.** Under this project's own rules it cannot support a decision. It is reproduced here to
prove the pipeline computes, and for one directional hint worth carrying into design: **roughly
one loser in five recovers**, so a naive stop-loss would convert recoveries into realised losses.
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
**Loss side** — SL 150% · SL 200% · SL 250% · fixed-$ stop at 1.0×credit and 1.5×credit (`dstop`,
confirmed to exist 2026-08-04)
**Time** — exit 15:45 · 15:50 (control) · 15:55
**Conditional** — "stop only if MAE breached before 14:00" (the non-recovery hypothesis from §1a)

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

- n ≥ 100 positions, **and**
- ≥ 6 months elapsed, **and**
- the window spans a regime change, **and**
- it beats the control by a margin exceeding the noise, **adjusted for the 12-variant count**, with
  the margin **pre-declared** rather than chosen on inspection.

On graduation it does **not** become a config change. It becomes a **drafted, unsigned
pre-registration entry** in `pre-registration-ledger.md` for Andy to sign or reject.

Earliest possible graduation is therefore ~6 months past Day-0 — call it **February 2027** — no
matter how good anything looks in October.

---

## 5a. 📝 APPENDED 2026-08-04 — defects found by building against this spec

*Recorded here rather than silently corrected. All five are in the tracker as the blocking review
item; none is applied to the signed text above except where the code had to choose something.*

1. **The fixed-$ rungs as signed are redundant.** §3 wrote them as "1.0×credit and 1.5×credit",
   which is arithmetically identical to SL100 and SL150 — a percentage of credit by another name.
   As written they duplicate the SL family and waste two of twelve slots. `research_loop.py`
   implements **0.50× and 0.75× RISK** instead, a genuinely independent axis matching
   `hedge-research.md` §9's intent. **This amendment is unsigned.**
2. **The count was wrong.** §3's prose lists 11 experimental variants while stating 12. The twelfth
   is now `CONTROL`, which earns its slot as the engine's self-test: it must reproduce the realised
   P/L, and a mismatch means the engine is wrong rather than the strategy underperforming.
3. **Both `TIME_*` variants are structurally undecidable.** MFE/MAE give extremes and their
   timestamps; the mark *at* 15:45 is neither and is recorded nowhere in the export. The first dry
   run returned 2,508 of 15,048 cells `UNDECIDABLE` — exactly those two variants × 1,254 positions.
   Decide whether they keep their slots as a standing reminder that **time-exit questions require a
   Track B arm**, or are replaced.
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
- [x] **Pre-declared margin:** a variant beats the control only if it wins on **both mean and
      median R**, by **≥ 0.10R per position**, with a 95% confidence interval that excludes zero
      **after Bonferroni correction for the 12-variant count**. Declared here, before any data —
      not to be renegotiated on inspection.
- [x] **Track B may consume ≤ 8 bot slots**, leaving headroom under the 50-bot plan cap.
- [x] **Track A output is advisory-only.** It never enters an instruction card and never appears in
      the three verdicts.
- [x] **`research_loop.py` runs nightly from Day-0, but emits nothing until n ≥ 30 post-cutover
      closed positions.** Before that it prints a single suppressed-output line, so the stage is
      exercised daily without publishing noise.

*Signed in conversation 2026-08-04 ("agreed with all"). The two values that were blank at drafting
— the margin and the start condition — were filled by Claude to the above and are subject to Andy's
correction; everything else is as Andy read it.*
