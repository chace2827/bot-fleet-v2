# Comparative machinery — implementation spec

*Written 2026-08-06. **STATUS: DRAFT — this document is a build specification, not a decision.**
It changes no signed text. Everything it proposes that would alter a pre-registration, a declared
analysis convention, or a signed margin is marked ⛔ **GATED** and listed in §8 for Andy.*

**What this closes.** `greenfield-family-spec.md` §12 row 13 and `track-b-arms-spec.md` §11 item 7
say the same thing: *"The comparative machinery does not exist … Needs scoping as its own task
before Day-0."* This is that scoping. It is the hand-off artifact for a Claude Code build.

**What this does NOT close.** `pre-registration-ledger.md` §7 item 3 makes the machinery a
**signing gate**: *"Kill criterion re-read against the daily loop — does the loop actually produce
that number? If not, fix one of the two now."* This spec answers that question honestly and the
answer is **partly no**. Roughly half of the declared criteria are computable from data that
exists; the other half depend on an **exit-attribution record that no input carries**. §1.4
specifies that missing input. Building this engine does not by itself discharge §7 item 3 — it
discharges it for Layer 1 and converts Layer 2 from an unnamed hole into a named, buildable
capture surface with a schema.

**Adversarial record.** Two subagents were spawned against §2 with instructions to refute it,
defaulting to "this is wrong." **Both succeeded.** Between them: 12 FATAL and 26 MATERIAL
objections. The text below is the post-review text; §7 is the record of what survived, what was
fixed, and what is carried.

---

## 0. The unit law, restated once so every section below can be short

- **Unit of account = the POSITION = the CONDOR** — the `trade_id` group; **risk = the larger
  side** (`CLAUDE.md` §4, ruling R-6).
- **R basis is `ror`** (return on **risk**), never `returnPct` (return on credit)
  (`oa-export-schema.md` §3).
- **Every aggregate carries its `n`, and its `n` carries its unit.** A count of matched days and a
  count of condors are different numbers and are never printed with the same label
  (`oa-export-schema.md` §5 fix 1).
- **An absent number is not a zero** (`CLAUDE.md` §10). The engine's empty state prints
  `EMPTY — n=0`, never `0.000R`.

---

## 1. Inputs

### 1.1 The named inputs, and why the ledger and not the export

| # | Path | Role | Refusal condition |
|---|---|---|---|
| **I-1** | `data/trades.csv` | the post-cutover working ledger — **the only source of numbers** | absent, or header-only → `EMPTY — n=0`, exit 0 |
| **I-2** | `data/ledger_meta.json` | cutover assertion + provenance | `ledger_start` absent, or `== "2099-01-01"` (the pre-Day-0 sentinel currently on disk), or `source_export == null`, or `counts.export_rows == 0` → **refuse, exit non-zero** |
| **I-3** | `data/bots_meta.csv` | `bot → pillar/role/underlying/epoch_boundary` | a family bot missing → refuse to name a family |
| **I-4** | `data/bots_config_v2.csv` | `bot → declared mechanic and threshold` | **currently unusable — see 1.1a.** Absent or lacking the arm's mechanic → the affected criterion is reported **SKIPPED**, never PASS (`execution_audit.py` precedent, `daily.sh` stage 3) |
| **I-5** | `data/exit_rows.csv` | **DOES NOT EXIST.** Exit attribution. Specified in §1.4 | absent → all of Layer 2 reports `BLOCKED — no exit-attribution input`, never PASS |

**The engine reads the LEDGER, not the raw export.** `build_ledger.py` already performs four
things correctly that a second reader would have to re-implement: the `credit = openPrice` sign fix
(`oa-export-schema.md` §2 — `premium` is **negative** on all 1,373 credit rows), the `trade_id`
condor pairing, the `LEDGER_START` filter, and the leak-refusal assertion. Re-reading the export
re-opens the exact bug class of `oa-export-schema.md` §5, where a hand-mapped `credit = premium`
silently rejected **1,247 of 1,254** positions and printed the survivor mean as if it were the
population mean.

> ### ⚠️ 1.1a — I-4 does not currently contain what this engine needs. [FIRST-HAND 2026-08-06, direct `device_bash` read of `data/bots_config_v2.csv`.]
> The **template** (`bots_config_v2.template.csv`) has per-bot mechanic columns. The **live file**
> does not. Its actual header is
> `object_kind,name,oa_id,version,attached_to,input_id,input_type,input_label,input_default,a7_hash,captured,layer2_status`
> and it holds **one row** — `shared_automation,GF-ScannerA-PutSpread,…` — whose `input_default`
> reads `NOT SET — see FINDING F-4`. Its own comment block says *"PARTIAL: Phase A is incomplete
> — only 1 of 3 shared objects exists."* No `GF-*` bot rows exist in `bots_meta.csv` either
> (n=33 rows, none `GF-`).
>
> **Consequence:** every threshold-referencing criterion is `SKIPPED` until Phase 2 config capture
> writes per-bot rows. ⛔ **Inferring an arm's threshold from its OA tag string (`arm sl100`) is
> forbidden** — that is a memory-derived config fact, `CLAUDE.md` §3 rule 2.

### 1.2 The fields consumed, named

From **I-1**, verbatim from the ledger header:

`bot · trade_id · structure · status · quantity · credit · exit_price · pnl · risk · open_date ·
close_date · tags · single_sided · short_put · long_put · short_call · long_call · mfe_pct ·
mae_pct · mfe_date · mae_date · epoch`

Not consumed: `pillar · underlying · role · symbol · expiration · premium · underlying_open ·
underlying_close`. **`premium` is explicitly forbidden as a credit source** (§1.1).

> ⭐ **`ror` IS NOT A LEDGER COLUMN.** `build_ledger.py`'s `TCOLS` drops it. The export verifies
> `ror == pnl / risk` **per row**, 0 mismatches on n=1,386 (`oa-export-schema.md` §3) — that is a
> **leg-level** identity. The condor-level R is computed here and has **no second witness and no
> verified identity**. Treat it as `[DERIVED, UNCORROBORATED]` and label it as such in the output.

### 1.3 Position construction

```
group        := all ledger rows sharing a trade_id
R_position   := SUM(pnl over group) / MAX(risk over group)
```

Origin of the grouping, stated so a substitution has something to contradict: `build_ledger.py`
buckets rows by `(botName, openDate[:10])` and pairs `shortcallspread` ↔ `shortputspread`
**greedily by nearest open time within `PAIR_WINDOW_S = 180` seconds**. A `type == "ironcondor"`
row arrives as a **single** row and is its own group (n=102 on the v1 capture,
`oa-export-schema.md` §6).

**Two mandatory guards, both from the folder's own rules:**

1. ⭐ **`risk` gets a second witness.** `oa-export-schema.md` §6: *"`execution_audit.py` re-derives
   it from leg strikes as a second witness and **never trusts this column alone**."* This engine
   puts `risk` in the denominator of every number the gate reads, so it re-derives risk from
   `short_put/long_put/short_call/long_call` × 100 × `quantity` per row and **refuses the position**
   on mismatch, counting refusals. Trusting the column alone here would be a stricter reliance than
   the detector permits itself.
2. ⭐ **`trade_id` is never persisted.** It is regenerated `T00001…` in export row order on every
   rebuild (`build_ledger.py`), so it is **not stable across runs**. Any cached matched-day set,
   anomaly log or exclusion log keys on `(bot, open_date, short_put, short_call)`, never on
   `trade_id`.

### 1.4 ⛔ I-5 — the input that does not exist, specified

The 26-column OA export **carries no exit-reason field** (`oa-export-schema.md` §1, column list
read verbatim). `tags` is set at **open** and is bot-level (`gfam`, `arm sl100`, `pr 18`). There is
therefore **no field anywhere in the named inputs from which "which mechanic closed this position"
is derivable.** This is `greenfield-family-spec.md` §11 CF-19 and §12 row 13, and
`track-b-arms-spec.md` §11 item 7, all naming the same gap.

**A proxy was drafted and is REJECTED.** The rejected proxy: *close time < 15:44 ET, and not
attributable to the ITM action, and MFE/MAE confirms the threshold.* It fails five ways, each
verified against the folder:

- **15:44 is a dead constant.** It was ruling S-4's gate on `GF-SiblingClose`; the C8 ruling removed
  that object and `greenfield-family-spec.md` §6.2 now reads *"SUPERSEDED 2026-08-06 — Rule 0 is
  MOOT: sibling-close is not built."* No mechanic sits at 15:44.
- **It empties PR-22.** `GF-QQQ-IC-Exp1545` closes at **15:45**, which is later than 15:44, so the
  one arm whose treatment *is* an early time exit is classified NOT FIRED on every day.
- **The clock is unverified.** No file states the export's timezone; the DST question is an open
  pre-switch-on check (`greenfield-family-spec.md` Phase D **D3**, promoted there by PE-14). A
  one-hour error moves every close across any wall-clock cut.
- **The ITM limb is unimplementable.** §6.2 Rule 2's discriminators are the **memo** and the
  **SmartPricing mode**, neither of which is exported; and Rule 2 is *"provisional until it is
  read"* (open check **D4**). §6.2 Rule 3 says ambiguous fills *"are **NOT assigned**"* and go to
  an `UNATTRIBUTED` bucket — a predicate that requires an attribution the folder refuses to make.
- **MFE/MAE censors at the trigger.** A PT that filled at 50% leaves `mfe_pct ≈ 0.50`, so the test
  `mfe_pct ≥ 0.50` sits **on** the value the mechanic created and resolves on the sign of the
  slippage — which is monotone in that position's P/L, i.e. in `d_i`. Conditioning on it selects
  on the outcome. Independently, `Touch0`'s trigger references the **underlying** against the
  strike and no intraday underlying path is exported; and `Trail`'s armed shape needs the **trough
  after the high**, which two timestamps cannot supply when `mae_date < mfe_date`.

**Therefore: specify the input rather than approximate it.** `pre-registration-ledger.md` §7 item
3's instruction is *"fix one of the two now"* — fix the loop.

```
data/exit_rows.csv   — one row per EXIT ORDER observed in a position's Trades list
bot,open_date,short_put,short_call,exit_ts,row_type,pricing_mode,memo,fill_price,quantity,capture_file,capture_sha
```

- `row_type` ∈ `profit_taking | trailing_stop | touch | stop_loss | expiration_exit |
  event_backstop | itm_action | UNATTRIBUTED` — §6.2 Rule 3's third bucket is a **first-class
  value**, never a forced binary.
- `pricing_mode` ∈ `speedy | normal | patient | market` — §6.2 Rule 1's discriminator.
- `memo` carries `1552 backstop flat close` where present — §6.2 Rule 2's discriminator.
- Source: the **Trades list**, read per position. ⛔ **The Exit Options panel is never evidence**
  (`CLAUDE.md` §3 item 3).
- Keyed on `(bot, open_date, short_put, short_call)` — not `trade_id` (§1.3 guard 2).

⛔ **GATED — Andy's.** This is a **new capture surface**, not a doc correction. It costs a capture
step per trading day and it is the only thing that makes five of the declared criteria fireable.
§8 item **G-1**.

### 1.5 Day-pairing and matching

**Trading-day key = `open_date[:10]`.** Not `close_date` — an early-exit arm closes earlier than
its control by construction, and keying on close would sort the same day into two buckets.

**Matched-day sets are declared per comparison family, never derived:**

| Set | Definition | Used by |
|---|---|---|
| `M7` | days on which **all seven** greenfield arms PR-14…PR-20 each have exactly one included condor | **the declared set** (`greenfield-family-spec.md` §8.4, verbatim: *"A trading day is **matched** iff **all seven arms opened a condor on it**"*) |
| `M6` | the same over the **six comparative** arms only (PR-14…PR-19), excluding the Canary PR-20 | computed and reported alongside, **never read by the gate** |
| `MB(x)` | days on which arm `x` ∈ {PR-21, PR-22} **and** PR-14 each have exactly one included condor | PR-21 / PR-22 K1 |

The engine computes `M7`, `M6` and every `MB`, and **prints `|M7|`, `|M6|` and their difference
every run**. The gate reads `M7`, because that is the declared convention and changing it is a
decision.

> ⛔ **GATED FINDING — G-2.** PR-20 is *"an INSTRUMENT hypothesis … its P/L is expected to be ~flat
> and **is not evidence about anything**"* with *"KILL CRITERION: NONE ON P/L"*
> (`greenfield-family-spec.md` §9). Requiring its fill to declare a day matched costs `n` for zero
> inferential gain, and PR-20 carries a 2-consecutive-day RED that switches it **off** — at which
> point `M7` stops accruing and **all five real comparisons halt.** The declared convention installs
> the one bot with no scientific role as a single point of failure over the family. `|M7|` vs `|M6|`
> is printed every run so the cost of the declared choice is visible while it stands.

**"Exactly one condor"** — a day on which an arm shows two included condors is **dropped from the
matched set and logged as an anomaly**, never averaged. The shared entry automation carries a
position-tag re-entry gate (check C7, PASS), so two is a finding.

> ⛔ **GATED — G-3.** "Exactly one" is a **tightening** of §8.4's *"opened a condor on it."* It is
> what makes the day-level mean and the condor-level mean the same number (§2.4 rationale 1), so it
> is load-bearing, not cosmetic. It is a third departure from R-3 and §12 row 16 names only two.

### 1.6 Exclusions — each applied in this order, each counted, each printed

| # | Rule | Notes |
|---|---|---|
| **X-1** | **`status == 'expired'` — applied at the GROUP, not the row.** A group is excluded iff **every** row in it is `expired`. A **mixed** group (one leg closed, one expired) is **included whole**, with every row's `pnl` in the numerator | see the box below |
| **X-2** | `single_sided == True` → excluded from the primary comparison; counted per arm per day | an unpaired short spread is not a condor |
| **X-3** | risk second-witness mismatch (§1.3 guard 1) → position refused, counted | never silently repaired |
| **X-4** | rows outside `LEDGER_START` | already impossible via `build_ledger.py`'s leak assertion; asserted again against **I-2** |
| **X-5** | ⭐ **the retire-scoped dual-tested pairs — a NON-exclusion here.** See §3.3 | removes no row from this engine |

> ### ⛔ GATED — G-4. X-1's group-level reading is a READING of R-7, and R-7's text is row-level.
> R-7 (`research-loop-spec.md` §10) stratifies `expired`: *"excluded from every count and from the
> PT family's comparison."* `status` is a **per-row** field (`oa-export-schema.md` §6: `closed`
> 1,232 / `expired` 154). The unit here is a **group**. Both naive readings are wrong, in opposite
> directions:
> - **Row-wise** drops the expired leg and keeps the closed one. That deletes a **positive** P/L
>   contribution (retained credit on a side that decayed to zero) while keeping the tested side's
>   loss, and may change `MAX(risk)`. `single_sided` is computed at **open** time by
>   `build_ledger.py`, so the resulting half-condor is **not flagged** and enters silently.
> - **Group-wise-if-any** drops the whole condor whenever either leg expired. Under the **C8
>   ruling** the untested side running to its own expiry *is the designed behaviour* of `Touch0`,
>   `SL100`, `SL200` and both Track B arms — *"the untested side IS left to decay exactly as the
>   anchor assumes"* (§9, PR-18). Dropping those deletes the arms' signature outcome, and deletes
>   it at a rate that **differs by arm**, which biases every `d_i`.
>
> **X-1 as written** — exclude only all-expired groups — is the only reading that neither mangles a
> condor nor deletes an arm's designed outcome. It is stated here as the operative reading and
> flagged because it is an interpretation of a signed ruling, not a quotation of one. The engine
> prints `n_all_expired`, `n_mixed_status` and `n_all_closed` **per arm** every run regardless, so
> the incidence asymmetry is visible whichever way it is ruled.

### 1.7 Two instrumentation outputs the review forced

- ⭐ **`pairing_at_risk`.** The family opens via **two separate Library automations**
  (`GF-ScannerA-PutSpread` / `GF-ScannerB-CallSpread`) in OA's parallel work queue —
  `greenfield-family-spec.md` §8.4 H2, [DOCUMENTED]: *"pushed into a **distributed work queue and
  executed in parallel** … no guarantee an automation will run exactly on the 15-minute marks."*
  A put/call fill gap **> 180 s** leaves two rows that `build_ledger.py` cannot pair, both flagged
  `single_sided`, both dropped by X-2 → that arm has **zero** condors that day → **the day dies for
  all six comparisons.** The engine emits the per-arm put/call open-time gap distribution and counts
  gaps in `[120, 180)` s as `pairing_at_risk`. `PAIR_WINDOW_S = 180` is an unversioned constant in
  a script and it is load-bearing on the gate; this makes its margin observable before it bites.
- ⭐ **`pnl_may_be_modelled`.** `greenfield-family-spec.md` §7: under `itmlive = auto`, an
  ITM-expiring position's P/L is *"estimated from the underlying close price — a modeled number,
  not a fill — and it lands in the export and therefore in the ledger."* `itmlive` was read
  **`auto`** on 2026-08-06 (`state.md`, Phase A block) and **D2 sets it to `market` before any
  capital is live.** No ledger field flags a modelled row. Until a capture confirms
  `itmlive == market`, every output object carries `pnl_may_be_modelled: true` and no verdict is
  emitted (§6.4 refusal R-6).

---

## 2. The statistics, exactly

### 2.1 Paired ΔR construction

For arm `X` against control `C` over matched-day set `M`:

```
d_i := R_X(day i) − R_C(day i)          i = 1 … n,   n := |M|
```

`n` is the **matched-day count**, and it is labelled `n_matched_days` everywhere. The per-arm
**condor count** is a different number, labelled `n_condors`, and both appear in every output
object. Because of the exactly-one rule (§1.5) they coincide on the matched set; they diverge on
the arm's full population, and the divergence is printed.

**RESAMPLE UNIT = THE DAY** — the paired difference `d_i`. Not the position, not the leg. The seven
arms share one entry signal and one underlying, so positions are **not** independent across arms
within a day; the day is the exchangeable unit and the differencing is what removes the shared
market factor.

> ⛔ **A stated premise of the original draft was FALSE and is struck.** The draft justified BCa by
> calling `d` *"zero-inflated — a non-firing arm contributes an exact 0.0 that day."* That is true
> of **Track A**, where the same position is scored under two rules. It is **false here**: this is
> a **between-bot** contrast, so on a non-firing day the arm and the control hold **different
> condors at different credits** (§8.4 H1: *"seven SmartPricing ladders walking separately produce
> seven possibly-different entry credits … `ror` is return on risk, so a differing credit moves the
> denominator"*). There is no atom at zero. Three consequences carried into the design: the
> zero-inflation rationale for BCa is withdrawn (§2.2), non-firing days inject fill-dispersion
> variance that pushes ρ **below** the declared 0.90 and SE **above** the declared figure (§2.5),
> and that dispersion is **not** pure noise — `profits`, `stoploss` and `tstop` are all
> credit-referenced, so *"at $0.30 vs $0.34 fills … **their trigger levels are different prices**"*
> (§8.4 H1), i.e. it has a component aligned with the treatment.

### 2.2 Bootstrap CI — procedure, stated so it is reproducible

| Parameter | Value | Reason |
|---|---|---|
| resample unit | **the day-level difference `d_i`** | §2.1 |
| method | nonparametric paired bootstrap, resample `n` days **with replacement** | |
| interval | **BCa**, jackknife acceleration over days | `d` is skewed (a stop arm's tail is one-sided); the percentile interval is biased on skewed data and BCa needs no normality |
| `B` (nominal 95%) | **10,000** | endpoint at order statistic ~250 of 10,000 |
| `B` (family-adjusted) | ⭐ **≥ 200,000** | at α′ = 0.05/6, each tail is 0.4167 % → the endpoint is order statistic **~42 of 10,000**, and BCa's shift can push it to the 4th. A verdict resting on the 4th order statistic is a verdict made by the RNG. `B` is sized so the endpoint sits above the 100th replicate per tail |
| seed | declared constant, **recorded in every output object** | bit-identical reruns |
| reported alongside | plain percentile interval, **flagged `NOT_A_GATE`** | stability read only |

⭐ **`â` and the skew are reported.** For the mean, jackknife acceleration reduces to
`â = skew / (6√n)`, and it is **0/0 undefined on a constant `d` vector**. At `n = 60–100` with an
arm whose entire hypothesis is the loss tail, `â` is driven by one or two days and enters the
endpoint multiplicatively. The engine emits `bca_a`, `skew_d` and `n_matched_days` beside every
interval, and **raises rather than emitting a verdict** if `|â · z| > 0.30` — the regime where
BCa's second-order accuracy is not available.

**Block bootstrap: NOT emitted.** A stationary block bootstrap was drafted as a serial-dependence
sensitivity and is **withdrawn**: `M` is a **gap-deleted** index whose gaps are arm-dependent
(§8.4 H2), so a block of five consecutive *matched* days can span two calendar weeks. Block
resampling on a gap-deleted series resamples an artifact. Serial dependence is instead reported as
the lag-1 autocorrelation of `d` on the matched index, labelled descriptive.

### 2.3 Sign test

**Exact two-sided binomial sign test on the FIRED subpopulation** of `M` — matched days on which
the arm's declared trigger actually fired.

- **FIRED is read from I-5 `exit_rows.csv`**, `row_type` == the arm's declared mechanic. It is
  **not** inferred from close time, from MFE/MAE, or from anything in I-1 (§1.4).
- Exact-zero differences are dropped; `n_dropped_zero` is reported. **Wilcoxon is not used** — the
  tie structure and the non-symmetric null break it.
- ⭐ **`sign_test_capable` is emitted as a boolean.** A two-sided exact sign test can reach
  significance at α′ = 0.05/K only if `2 · 0.5^n_fired ≤ α′`. At `K = 6` that is
  **`n_fired ≥ 8`, every one of them signed the same way.** Below that the test **cannot** be
  significant and the engine reports `INCAPABLE`, never `FAIL`.

> ⛔ **GATED — G-5. Conjunct (c) is unpassable by construction for PR-19, whose hypothesis is that
> it rarely fires.** `hedge-research.md` §2.1, quoted in PR-19: *"Above ~200% is effectively
> no-stop."* PR-19 is *predicted* to produce `n_fired` near zero. Because GATE-CM is conjunctive,
> (c) blocks the gate regardless of (a) and (b). **This is CF-11's defect one layer up** — CF-11
> disapplied the liveness rule on PR-19 for exactly this reason (*"would have switched the arm off
> precisely when it was CONFIRMING itself"*) and the same asymmetry was reintroduced in the PASS
> gate. Andy's: disapply (c) on PR-19, or accept that PR-19 has a kill criterion and no gate.
>
> ⚠️ **Separately — (c) conditions on a post-treatment, outcome-correlated variable.** An arm fires
> when the day's path crossed its threshold: `SL100`'s fired set is the worst days by construction,
> `PT50`'s the best. So (c) estimates *"given the market did the thing that triggers this mechanic,
> did the mechanic help"* — a **different estimand** from (a) and (b), on a different `n`, ANDed to
> them as though it were a third check on one quantity. Carried, named, not fixed here: fixing it
> means re-specifying (c) on a **pre-treatment** subpopulation (e.g. days the **control's** MAE
> crossed the arm's level), which is a different test and a signed-text change.

### 2.4 ⭐ THE R-3 GATE, RESTATED FOR THE FAMILY'S PER-CONDOR DAY-PAIRED FORM

**R-3's signed text** (`research-loop-spec.md` §10, ruled 2026-08-04): a variant beats the control
only if **(a)** mean ΔR **≥ +0.015R per position** over that bot's **full post-cutover population**;
**(b)** a **paired bootstrap 95 % CI on that mean excludes zero** under §10a; **(c)** on the
**subpopulation where the variant actually fires**, a **paired sign test** against the control is
significant at the same level. The median-ΔR test is **WITHDRAWN**.

**The family's form** (`greenfield-family-spec.md` §9): *"the paired **per-condor** ΔR (arm −
control) has a bootstrap 95 % CI entirely above 0 after **Bonferroni** correction across the 6
arm-vs-control tests, on **matched days**, at the declared n."*

**GATE-CM — the restatement. Conjunctive. Every conjunct reported with its own `n`:**

```
GATE-CM(arm X vs control C, family F, at the stamped gate-eval date):

 (a)  mean over M of d_i  ≥  +0.015 R          [per condor, ror basis, risk = larger side]
 (b)  ci_fam_lo(mean d)   >  0                 [BCa at level 1 − 0.05/K, K per §3]
 (c)  exact binomial sign test on the FIRED subpopulation of M, p ≤ 0.05/K,
      AND sign_test_capable == true

 emitted with, mandatory and inseparable:
   n_matched_days · n_condors_X · n_condors_C · n_fired · K · seed · B ·
   mde_fam · bca_a · skew_d · n_all_expired · n_mixed_status · n_single_sided ·
   n_unmatched_X · n_unmatched_C · pairing_at_risk · pnl_may_be_modelled
```

**The rationale, departure by departure — this is what §12 row 16 asks for:**

1. **Unit — "per position" vs "per condor" is NOT a departure.** `CLAUDE.md` §4 and ruling R-6
   define the position **as** the condor (`trade_id` group, risk = larger side). The two phrases
   name one unit. This half of row 16's objection collapses on the project's own definition.
2. **Averaging unit — this IS a departure, and row 16 does not name it.** R-3's mean is over
   **positions** (`n` = position count); GATE-CM's mean is over **days** (`n` = matched-day count).
   They coincide **only** under §1.5's exactly-one-condor-per-arm-per-day rule, which is itself a
   tightening of §8.4 (⛔ G-3). Where the rule holds, the numbers are identical; where it is
   violated the day is dropped, so the identity is maintained by construction rather than by
   assumption.
3. **Population — this IS a departure, and it is the substantive one.** Track A's ΔR is a
   **within-bot counterfactual**: the same position scored under two rules, so pairing is free and
   the full population is available. The family's ΔR is a **between-bot contrast**: two different
   positions on the same day. **The matched-day restriction is the only way to obtain between bots
   the pairing R-3 already had within one.** It is the same estimand pursued the only way it can be
   pursued here. **Its cost, carried and named:** the estimand becomes *"the effect on days all
   arms traded"*, and under §8.4 H2's arm-specific fill selection near the 0.75 % band edge that
   conditioning event is **not ignorable** — the excluded days are disproportionately the
   highest-information ones. Every ΔR is therefore published beside `n_unmatched_X` /
   `n_unmatched_C`, and §7 carries the residual.
4. **Threshold — +0.015R is transplanted UNCHANGED and NOT re-derived.** R-3 calibrated it as *"the
   arithmetic ceiling on a PT50→PT70 move at the fleet's median credit/risk of 0.070 is 0.014R per
   fired position."* This family's credit/risk is 0.083–0.162, **above** the calibration point, so
   the value is reachable here (§12 row 10, resolved). Re-scaling it to this family's credit would
   be a **new margin needing a new signature** and is not done. ⚠️ **Two limits on that transplant,
   recorded not resolved:** the ceiling was computed for a **PT move**, while three of the five arms
   are **stop/touch** mechanics that can move R by ±1.0 in a day — reusing a PT-derived ceiling as
   the materiality bar for a stop arm is a category stretch; and R-3's figure is **per fired
   position** while (a) is a mean **diluted by non-firing days**, so a single 0.015R bar means
   ≈0.025R per fired condor for a 60 %-firing arm and ≈0.30R per fired condor for a 5 %-firing arm.
   **The bar is materially harsher on the hedge arms than on the profit-target arms, and nothing in
   R-3's text sets the fire rate that decides it.** The engine therefore emits `fire_rate` beside
   (a), always. ⛔ **G-6.**
5. **Multiplicity — R-3's (b) points at §10a's max-T; the family declares Bonferroni-across-6.**
   Kept separate, §3.
6. **Sign test — retained in substance**, with FIRED sourced from I-5 rather than inferred (§1.4,
   §2.3).

### 2.5 ⛔ THE FINDING THAT MATTERS MOST — conjunct (a) is INERT under conjunct (b)

Using the family's **own** declared power arithmetic (`greenfield-family-spec.md` §9 / §11 CF-3:
SD(R) ≈ 0.30, day-pairing ρ ≈ 0.90, n = 100 → ±0.026R at 95 %):

```
SE(mean d) = 0.30 · √(2 · (1 − 0.90)) / √100          = 0.013416
95 %      half-width = 1.960 · 0.013416               = 0.0263 R   ← matches §9's stated ±0.026R
Bonferroni K=6 (α′ = 0.008333, z = 2.638):
family    half-width = 2.638 · 0.013416               = 0.0354 R
```

**Conjunct (b) therefore requires an observed mean(d) ≥ +0.035R — 2.4× conjunct (a)'s +0.015R
threshold. Every sample that satisfies (b) satisfies (a) automatically. (a) can never bind.**

Two things follow, and both are reported rather than argued away:

- The operative bar is set by the **CI width**, not by the calibrated margin. R-3's calibration
  story does no work at this `n` and `K`.
- **+0.035R is 2.4× the largest effect this program has ever measured** (SL75, **+0.0150R**,
  n=1,254 — `state.md`). A gate that can only fire on estimates 2.4× larger than anything real is a
  gate whose passes are **Type-M inflated**. This is `greenfield-family-spec.md` §12 row 16 —
  *"the threshold is now finer than the family can resolve at n=100"* — quantified with the declared
  Bonferroni term included, which row 16 states at ±0.026R (unadjusted) and not at ±0.035R.

⭐ **Mandatory output: `mde_fam` — the minimum detectable effect at the realised `n` and `K`.** It
is emitted beside every verdict, PASS or FAIL, and **a PASS may not be published without it.** A
PASS at an `mde_fam` of 0.035R is a different claim from a PASS at 0.015R, and the number that
distinguishes them must travel with the verdict.

### 2.6 Sequencing — the interim kill look and the gate are the same vector

Every PR-14…PR-19 entry carries *"CI entirely below 0 at n ≥ 60"*, and PR-21/PR-22 K1 carries
*"bootstrap 95 % CI entirely below 0 at n >= 60 matched condors."* These are **fixed-n interim
looks on the same statistic** the gate reads at n=100 — precisely what `research-loop-spec.md`
§10a item 4 forbids: *"Any nightly monitoring of the gate statistic must use an **always-valid
confidence sequence**, not a fixed-n CI."* Labelling them separately does not decouple them: the
kill is **one-sided**, so it removes arms whose first-60 draw came in low, and the arms surviving
to the gate are conditioned on a favourable interim draw. That inflates the pass rate under the
null. It is the clearest null-looks-like-pass path in the design.

**Engine behaviour, and it is conservative:**

- The **n≥60 interim read is emitted ONLY as an always-valid confidence sequence** (`cs_lo`/`cs_hi`,
  empirical-Bernstein), which is the only interval in this engine that may be looked at more than
  once.
- The **fixed-n BCa interval is computed once, at the stamped gate-eval date**, and the engine
  **refuses to compute it on any other date**.
- ⛔ **G-7 — PR-14…PR-20 have NO `GATE EVAL DATE` field.** `pre-registration-ledger.md` §2's
  template has none (`track-b-arms-spec.md` §11 item 5); only PR-21/PR-22 carry one voluntarily.
  §10a item 2 requires the date be written **before n reaches 100**. **Until a date is stamped, the
  engine emits no verdict for that arm** — descriptive numbers only. This is structural enforcement
  of §10a item 2 and it surfaces §11 item 5 as a signing blocker rather than a footnote.
- ⛔ **G-8 — the kill side is uncorrected and fires 40 days earlier than the gate.** Seven arms ×
  an uncorrected 95 % absolute CI at n=60 gives a family-wise kill rate far above 5 %, and an arm
  can be switched **off** before its comparative gate is reachable. This is CF-2's finding —
  *"kill criteria absolute … **so the criteria would fire on the winners**"* — marked FIXED because
  a comparative criterion was **added**; the absolute one was never brought under the correction
  and nothing sequences the two. Andy's.

---

## 3. Multiplicity — two engines, two corrections, no pooled alpha

### 3.1 The greenfield family

- `BONFERRONI_K` is a **declared constant, default 6**, recorded in every output object. The
  engine **never** switches it silently.
- Per-test two-sided level = `0.05 / K`. Conjunct (b) reads the **`(1 − 0.05/K)`** BCa interval,
  emitted as `ci_fam_lo` / `ci_fam_hi`.
- ⭐ **`ci95_*` is emitted in a separate `diagnostics` block flagged `NOT_A_GATE`.** The verdict
  object carries `ci_fam_*` **only**. Three intervals will exist on quantities a reader will treat
  as one — `ci_fam_*`, `ci95_*`, and the uncorrected 95 % CI inside every kill criterion — and a
  narrower unlabelled interval sitting in the same output is a number waiting to be quoted in prose.
  Under `CLAUDE.md` §10 (*"no number without its source file"*), separation is structural, not
  editorial. ⚠️ Note in passing: the PR entries' phrase *"bootstrap 95 % CI"* is the **nominal
  per-comparison** level; the declared Bonferroni implies the gate reads a different interval. That
  is arguably a wording correction in the PR text — **PR text is gated, so it is flagged here and
  not touched.**
- ⛔ **G-9 — K is wrong in both directions at once, and the smaller error is the one that is
  obvious.** Six is the declared count, but PR-20 (Canary) carries no comparative criterion, so
  only **five** comparative tests run — K=6 over-corrects by ~2.4 % on z, in an engine that has no
  power to spare. That is the small end. Enumerating the decisions actually taken **against the
  single `GF-QQQ-IC-Ride` control** across the named documents gives: PR-15 ΔR · PR-16 ΔR · PR-17
  ΔR · PR-18 ΔR · PR-19 ΔR · PR-16's **second** test (worst-condor-R vs Ride) · PR-19's degeneracy
  equivalence test vs Ride · **PR-21 K1** vs Ride · **PR-22 K1** vs Ride — **nine**, plus PR-21's
  secondary vs GF-SL100. **K=6 is under-corrected by roughly 1.8× against the family that actually
  exists.** The engine emits a `family_census` block enumerating every declared decision against
  the shared control, so the undercount is visible on every run. It does not change K. Andy's.

### 3.2 Track A

Unchanged and untouched: `research-loop-spec.md` §10a item 3 — *"a stratified paired sign-flip
permutation test on the per-position ΔR vector, strata = bot, with max-T across all variants and
bots, 10,000 sign-flips … **no Bonferroni term is applied**."* Different engine, different family,
different correction.

⚠️ Recorded, not resolved: the two corrections are arguably **swapped relative to where power is
scarce** — Bonferroni is conservative under the strong positive dependence this family has (one
control, one day-series, one entry signal), while max-T absorbs exactly that dependence and is
applied to the engine under the looser sample constraint. A joint day-bootstrap with max-T across
arms would recover most of the 2.638 → ~2.3 gap at no cost. **`greenfield-family-spec.md` Phase C
step C4's "Bonferroni across the 6" is a declared analysis convention**, so this is a decision for
the queue, not a fix. ⛔ **G-10.**

### 3.3 The seam — and the retire-scoped ruling, read precisely

The slot-5 retirement (`decision-card-2026-08-06.md` ruling 5, applied to `research-loop-spec.md`
§10a) excludes dual-tested `(bot, variant)` pairs — `SL100`, `SL200`, `DSTOP_100` on the greenfield
and ARM-B1 ledgers — from **Track A's computed family**. Those counterfactuals live in
`counterfactuals.csv`. **It removes no row from this engine's input** (X-5), because this engine
computes live-arm contrasts, not Track A counterfactuals.

It lands here as **three** things, and the third was missed in the draft:

1. **A forbidden input.** This engine never opens `data/counterfactuals.csv` (§6.2).
2. **A limitation, quoted rather than paraphrased.** §10a's honesty line: *"This scoping removes a
   degenerate self-comparison; it does **not** create cross-engine multiplicity accounting … **No
   pooled alpha exists across the two engines. Recorded as a carried limitation, not a solved
   one.**"* ⛔ **Not opening a file does not enforce independence of error rates — it enforces
   ignorance of them.** §12 row 11's surviving clause is still open and still Andy's:
   `GF-SL100`/`GF-SL200` *"still **pool error rates nowhere**."*
3. ⭐ **An obligation this engine must carry: the no-influence rule.** Package part 3 — *"a Track A
   advisory read on a dual-tested variant may not trigger, accelerate, or veto any arm disposition
   **before that arm's own pre-declared gate date**"* — is carried into PR-14…PR-22 **at signing**.
   It is anchored on a date that, for five of the seven greenfield arms, **does not exist** (G-7).
   The engine enforces what it can: no verdict without a stamped gate-eval date, and no read of
   Track A output at all.

⚠️ **The retirement's stated reason has been narrowed since it was ruled**, and this spec adopts
no premise beyond what stands. `greenfield-family-spec.md` §9's own append: *"THIS PARAGRAPH'S
STATED REASON IS NARROWED BY THE C8 RULING … these arms are no longer close-both … the same exit
unit as Track A's counterfactuals … ⛔ FLAGGED FOR ANDY — not resolved here: whether the surviving
grounds alone still support 'non-equivalent estimands'."* The retirement itself stands; its
rationale is under Andy's review.

### 3.4 Track B

PR-21 and PR-22 are each their own pre-registration. ⛔ **G-11 — the draft claimed they sit outside
the greenfield Bonferroni family "per ruling S-1." That is a category error and it is withdrawn.**
S-1 is a **bot-slot allocation** ruling (`track-b-arms-spec.md` §3.3: *"the seven family bots are
`build-plan.md` §2D fresh builds; Track B's 8 slots are yours"*). It says nothing about error rates.
Both Track B arms declare **`GF-QQQ-IC-Ride` as their control** — same control, same underlying,
same shared entry automations, same day-series, same 1-lot sizing. By every definition except the
budget line that is **one family**. The engine emits them with `K` from the same `family_census`
and flags `k_basis: "DECLARED — statistical family not ruled"`. Andy's.

**PR-21's secondary DiD vs GF-SL100 is emitted `descriptive: true`, no verdict — and restricted to
the overlap.** PR-21 switches on at **Day-0 + 90** (its `<D100>` calibration window), so its
day-series is **disjoint** from GF-SL100's first 90 days. A difference-in-differences over
non-overlapping day sets is not a difference-in-differences; unrestricted it confounds arm with
calendar. The engine computes it on the overlap only, prints `n_overlap`, and prints the discarded
count. ⚠️ PR-21's own hypothesis calls this *"the real question"*, so a descriptive number here
will be read as an answer — the label must be on the number, not in a footnote.

---

## 4. Outputs — the exact numbers each pre-registration needs

**Legend:** ✅ computable from I-1…I-4 today · ⚠️ computable but degraded (named) · ⛔ **BLOCKED —
needs I-5** (§1.4) · ⬛ not this engine's surface.

| PR | Criterion, as written | Exact emitted fields | |
|---|---|---|---|
| **PR-14** Ride | *"Exp(R) per condor < 0 with the CI entirely below 0 at n ≥ 60 condors"* | `exp_r_mean` · `exp_r_ci_lo/hi` (one-sample BCa; **resample unit = the CONDOR**, not the day-difference) · `n_condors` | ✅ |
| | inverted liveness: *any PT/trail/touch/stop row → RED, except ITM-action rows* | `row_type` counts by class, `n_itm_action`, `n_UNATTRIBUTED` | ⛔ + **D4 open** (ADVISORY, not fireable, per §9) |
| **PR-15** PT50 | Exp(R)<0, CI below 0, n≥60 | as PR-14 | ✅ |
| | GATE-CM vs Ride | full GATE-CM block (§2.4) | ⚠️ (a)(b) ✅ / (c) ⛔ |
| **PR-16** Trail | Exp(R)<0, CI below 0, n≥60 | as PR-14 | ✅ |
| | *"worst-condor-R worse than the Ride control's at n ≥ 60"* | `worst_r_X` · `worst_r_C` · their dates · `n_matched_days` | ⚠️ see box |
| | GATE-CM vs Ride | full block | ⚠️ / ⛔ |
| **PR-17** Touch0 | Exp(R)<0, CI below 0, n≥60 | as PR-14 | ✅ |
| | liveness *conditioned on threshold breached* | needs **intraday underlying path vs short strike** — the ledger has `underlying_open`/`underlying_close` only, endpoints not extremes | ⛔ **and not fixable by I-5 either** |
| **PR-18** SL100 | Exp(R)<0, CI below 0, n≥60 | as PR-14 | ✅ |
| | liveness on breach | `mae_pct` vs declared `stoploss` (credit basis) + `row_type == stop_loss` | ⛔ (row) / ⚠️ (basis, see box) |
| **PR-19** SL200 | Exp(R)<0, CI below 0, n≥60 **matched days** | as PR-14 + `n_matched_days` | ✅ |
| | **degeneracy:** *\|R_X − R_C\| ≤ 0.005R on ≥20 of any 40 consecutive matched days AND stop-row count == 0 over that window* | `degeneracy_windows[]` with `within_tol_count`, `stop_row_count`, `window_start`, `window_end` | ⛔ + **unfireable, see box** |
| | liveness | **disapplied by design** (CF-11) | ⬛ |
| **PR-20** Canary | **no P/L criterion** — exempt | `n_days_held` | ✅ |
| | *"no profit-taking fill on ≥2 consecutive days on which it held a position → RED"* | `pt_fill_by_day[]` | ⛔ — and PR-20's own text notes the 5 % threshold is **sub-tick**, so any price-based proxy is indistinguishable from a one-cent early close. **This is the fleet's only forward exit-engine detector** |
| **PR-21** DStop100 | **K1** paired mean ΔR vs Ride < 0, CI below 0, n≥60 matched condors | `mean_d` · `cs_lo/hi` at n≥60 · `ci_fam_*` at the gate date · `n_matched_days` | ✅ (as a confidence sequence, §2.6) |
| | **K2** liveness on `<D100>` breach | `row_type == stop_loss` count + `mae` breach count | ⛔ |
| | **K3** family / capture-diff, A1–A8 | ⬛ — `execution_audit.py` + the capture-diff, not this engine. Named so the boundary is explicit | ⬛ |
| | **K4** sentinel A4 (config) / **A4b** (closes within 5 min of open, ≥2 consecutive days) | A4: needs I-4 ⚠️ · **A4b: `close_date − open_date < 300 s`, `consecutive_fast_close_days`** ✅ | mixed |
| | **K5** 48-hour execution rule | ⬛ operational | ⬛ |
| | `<D100>` calibration | see box | ⛔ |
| **PR-22** Exp1545 | **K1** as PR-21 | as PR-21 | ✅ |
| | **K2** liveness: *zero `speedy` close rows at ~15:45 across 10 consecutive matched days* | `row_type == expiration_exit` **and** `pricing_mode == speedy` **and** `exit_ts ≈ 15:45` | ⛔ + **timezone unverified (D3)** |
| | K3/K4/K5 | as PR-21 | as PR-21 |

> ### ⚠️ PR-16's second criterion is a coin flip, and it is reported as one.
> *"Worst-condor-R worse than the Ride control's"* compares two **sample minima** — an extreme
> order statistic — with no CI, no tolerance, no correction and no membership in the Bonferroni
> family. Under a null of exchangeable arms, `P(min_X < min_C) ≈ 0.5`. **The Trail arm is retired
> on a coin flip and the retirement is worded as a refuted claim.** The engine emits `worst_r_*`
> with the explicit annotation `no_inference: "sample minimum, uncorrected"`. ⛔ **G-12** — Andy's
> to re-specify (a tail quantile with a CI would be the natural repair) or to accept as a
> deliberately blunt tripwire.

> ### ⚠️ PR-19's degeneracy criterion is not computable, not well-posed, and cannot fire. Three separate defects.
> **(1) Not computable** — the second limb needs a stop-row count (I-5).
> **(2) Not well-posed** — *"any 40 consecutive matched days"* is a **scan over overlapping
> windows**: with N matched days there are N−39 windows sharing 39 days each. The criterion fires
> if **any** window hits — a maximum over a strongly dependent sequence, with no declared start
> date, no correction and no evaluation cadence. It also collides with §10a item 2's *"no nightly
> gate evaluation"*: a rolling scan **is** repeated evaluation. And *"consecutive"* is undefined —
> consecutive in matched-day index, or in calendar days with gaps?
> **(3) Cannot fire.** At the family's declared SD(R) ≈ 0.30 and ρ ≈ 0.90, the paired daily SD is
> `0.30·√0.20 ≈ 0.134R`. `P(|d| ≤ 0.005) ≈ 2(0.005)/(0.134·√(2π)) ≈ 0.030`, so the expected count
> in a 40-day window is **≈1.2 against a requirement of 20**. Meanwhile the AND-limb (zero stop
> rows) is near-certain for SL200 **by hypothesis**. Impossible ∧ near-certain = **never fires.**
> CF-11's status line reads *"**FIXED** — degeneracy rewritten with a tolerance and a config-backed
> second condition."* The rewrite exchanged one unfireable rule for another. The engine emits the
> window array and `degeneracy_fireable: false` with this arithmetic attached. ⛔ **G-13.**

> ### ⚠️ `<D100>` — four defects, and two of them change its value.
> *"median of (credit × 100 × quantity) over `GF-QQQ-IC-Ride`'s closed condors in the first 90
> post-cutover **trading days**"*.
> **(i) "trading days" needs an exchange calendar**, and none of the named inputs is one. From the
> ledger, a holiday, a no-fill day and a bot-off day are indistinguishable; only *"the first 90 days
> on which a row exists"* is computable, which is a **different and shorter window**.
> **(ii) Per-condor vs per-side.** The formula is stated over **condors**, but `dstop` is carried in
> `GF_EXITS_PUT` / `GF_EXITS_CALL` — **per side**. A condor-level median stamped into a per-spread
> control is ≈2× the intended level. `track-b-arms-spec.md` names this class by name: *"the D-6
> units failure one layer up — the same class that made every Track A counterfactual wrong by
> 100 × quantity."*
> **(iii) The target unit is still unknown.** C10 (`dstop` per contract / position / leg) is
> **ASSIGNED, not answered**; the spec's own words: *"**assignment is not an answer**"*, and the arm
> *"is NOT AN ARM until both close."*
> **(iv) An estimated constant is treated as known.** A median over ≤90 condors, stamped once and
> held for the life of the pre-registration, with its estimation error never propagated. If the
> credit regime shifts after day 90 — which is what B3 **defines** a regime change to be — the arm
> silently tests a different rung than the one pre-registered, and nothing detects it.
> The engine emits `d100_candidate` with `basis: "days-with-rows, NOT trading days"` and
> `unit: "UNRESOLVED — C10"`, and **refuses to stamp**. ⛔ **G-14.**

> ### ⚠️ Basis and unit mixing inside one liveness test — label every emission.
> `mfe_pct` / `mae_pct` are on the **credit** basis (`oa-export-schema.md` §4: *"the same basis as
> `returnPct`"*). `stoploss` thresholds are **% of credit** (C1 PASS: *"-100% of credit = 1"*), so
> the basis matches for PR-18/PR-19's breach test — but `d_i`, the effect it gates, is on the
> **risk** basis. Every emission names its basis. Separately: under C8 the **exit mechanic's unit is
> the SPREAD** while the **analysis unit is the CONDOR**, and `mfe_pct`/`mae_pct` are **per row**.
> "The declared threshold was reached" is therefore a per-spread indicator classifying a per-condor
> `d_i`, with **no rule for the case where the put side breached and the call side did not**.
> Undefined in the folder; the engine emits `breach_put`, `breach_call` and `breach_either`
> separately and takes no verdict from them. ⛔ **G-15.**

### 4.1 Output artifacts

```
data/comparative/<date>_comparative.json    the verdict + diagnostics objects
data/comparative/<date>_paired.csv          one row per (family, arm, day): d_i and its provenance
data/comparative/<date>_census.json         family_census — every declared decision vs the control
```

**Refusal rules, hard (§6.4):** no aggregate is written without its `n`; no verdict is written
without `K`, `mde_fam`, `seed`, `B`, the exclusion counts and the unmatched counts; no verdict at
all without a stamped gate-eval date; no verdict while `pnl_may_be_modelled` is true.

---

## 5. Validation fixtures

**Fixture assets live in `data/fixtures/comparative/`, copied VERBATIM from
`data/captures/oa_export_positions_2026-07-30.csv` (sha256
`dca69adaf771f064e39184851fe97fd8cdbb85ee71ab85bc0d850bbecedfcadc`, n=1,386).** They have exactly
the status of `data/execution_audit.csv`, the frozen 35-row detector validation fixture: **a TEST
ASSET that survives the cutover, never a reporting input** (`CLAUDE.md` §6). No number below may be
quoted as a fact about the fleet.

`oa-export-schema.md` §5 fix 2, the rule these exist to satisfy: *"Every validation fixture must
include at least one row copied verbatim from a real capture. Synthetic rows test logic; only real
rows test conventions. The 18-check fixture was fully green while the harness was wrong, because
every row in it was hand-authored with a positive credit."*

### F-1 — condor R identity, and the wrong answer it must not give

Verbatim, both rows of one real condor (`QQQ-IC-0DTE-Raw-HoldToExp`, 2026-03-24):

```
"QQQ-IC-0DTE-Raw-HoldToExp","shortputspread","-581 put, +579 put","QQQ","closed",1,0,0.13,0.02,-13,11,0.058824,0.846154,187,"12.98288","0.0698","1","-1.84615385","2026-03-24 15:42:00","2026-03-24 13:18:00","2026-03-24 16:00:00","2026-03-24 12:07:01","2026-03-24 15:50:00","put side",585.34,584.17
"QQQ-IC-0DTE-Raw-HoldToExp","shortcallspread","-590 call, +592 call","QQQ","closed",1,0,0.08,0.01,-8,7,0.036458,0.875,192,"8.15184","0.04268","1","-1.25","2026-03-24 15:29:00","2026-03-24 12:23:00","2026-03-24 16:00:00","2026-03-24 12:08:01","2026-03-24 15:50:00","call side",585.51,584.17
```

- **A-1 (VALUE):** `R_condor == (11 + 7) / max(187, 192) == 18/192 == 0.09375` exactly, to 1e-9.
- **A-2 (VALUE, the wrong answer):** `R_condor != mean(0.058824, 0.036458) == 0.047641`. Averaging
  the legs' `ror` understates this condor by **50.8 %**; the assertion pins the denominator rule
  (`risk = the larger side`) rather than a verdict string.
- **A-3 (VALUE):** open times `12:07:01` and `12:08:01` are **60 s** apart, inside
  `PAIR_WINDOW_S = 180` → one group, `single_sided == False`.

### F-2 — paired ΔR on a real matched day, on a real multi-contract row

Same day, second bot (`QQQ-IC-0DTE-HedgeA-S1`, `quantity = 28`), verbatim:

```
"QQQ-IC-0DTE-HedgeA-S1","shortputspread","-581 put, +579 put","QQQ","closed",28,0,0.25,0.12,-700,364,0.074286,0.52,4900,"24.54576","0.141068","0.56","-0.04","2026-03-24 11:23:00","2026-03-24 11:01:01","2026-03-24 16:00:00","2026-03-24 11:01:01","2026-03-24 11:23:11","put side",585.78,586.97
"QQQ-IC-0DTE-HedgeA-S1","shortcallspread","-590 call, +592 call","QQQ","closed",28,0,0.27,0.13,-756,392,0.080925,0.518519,4844,"25.65504","0.149157","0.55555556","-0.62962963","2026-03-24 12:02:00","2026-03-24 11:26:00","2026-03-24 16:00:00","2026-03-24 11:01:02","2026-03-24 12:02:10","call side",585.72,585.61
```

- **A-4 (VALUE):** `R_HedgeA == (364 + 392) / max(4900, 4844) == 756/4900 == 0.154285714285714`,
  to 1e-9.
- **A-5 (VALUE):** `d(2026-03-24) == 0.154285714285714 − 0.09375 == 0.060535714285714`, to 1e-9.
- **A-6 (VALUE, the ×quantity guard):** on the `quantity = 28` row,
  `premium == −(openPrice × 100 × quantity) == −(0.25 × 100 × 28) == −700`. A per-contract bug
  shows here as a factor of **28** — this is `oa-export-schema.md` §5's exact bug class caught on a
  **real** multi-contract row, which is the thing a synthetic 1-lot fixture cannot do.

### F-3 — sign-convention guard, and a hard refusal

Uses the F-1 put row verbatim.

- **A-7 (VALUE):** `credit == openPrice == 0.13` (positive) and `premium == −13` (negative), and
  the engine's `credit` field equals `openPrice`, never `premium`.
- **A-8 (BEHAVIOUR, VALUE-backed):** handed `premium` as `credit`, the engine **raises**. It does
  **not** silently drop the position. On 2026-08-04 a `credit <= 0` guard silently rejected
  **1,247 of 1,254** positions and the survivor mean printed identically to a population mean
  (`oa-export-schema.md` §5). The assertion is on the exception and on the count `1247`, not on a
  verdict string.

### F-4 — exclusion accounting, from the real capture's real counts

- **A-9 (VALUE):** over the full fixture, `n_all_expired_rows == 154`, `n_closed_rows == 1232`,
  `total == 1386` — the machine-verified counts in `oa-export-schema.md` §6.
- **A-10 (VALUE):** a hand-built **mixed** group (one closed leg + one expired leg, both real rows)
  is classified `mixed_status`, is **included whole** under X-1, and its `R` uses **both** legs'
  `pnl`. The assertion is on the resulting R value, not on the classification string.
- **A-11 (BEHAVIOUR):** an aggregate emitted without its `n` raises. Not a warning.

### F-5 — bootstrap determinism and the incapable-test guard

Anchored on F-2's real `d`.

- **A-12 (VALUE):** the same seed gives **bit-identical** `ci_fam_lo` / `ci_fam_hi` across runs.
- **A-13 (VALUE):** on a constant `d` vector, `bca_a` is **undefined** and the engine raises rather
  than emitting an interval — the 0/0 case of `â = skew/(6√n)`.
- **A-14 (VALUE):** with `n_fired == 7` at `K = 6`, `sign_test_capable == false` and the verdict is
  `INCAPABLE`, **not** `FAIL`. `2 · 0.5^7 == 0.015625 > 0.008333`; `2 · 0.5^8 == 0.0078125 ≤
  0.008333`, so the boundary sits at exactly 8.
- **A-15 (VALUE):** at `n = 100`, `SD(d) = 0.134`, `K = 6`, `mde_fam` rounds to **0.035** — the
  §2.5 arithmetic asserted as a number, so a future change to `K` or `B` that quietly moves the
  detectable effect fails a test rather than a review.

---

## 6. Interface note

### 6.1 It runs standalone

```
python3 scripts/comparative_machinery.py [--family GF|B|ALL] [--as-of YYYY-MM-DD] [--gate]
```

`--gate` is refused unless the named arm has a stamped gate-eval date **and** `--as-of` equals it.

### 6.2 ⛔ It is NOT wired into `daily.sh`. Not as stage 9, not as any stage.

`research_loop.py` is `0.1.0-DRAFT`, carries **three fatal defects** (units × 100 × quantity · the
tautological `CONTROL` · censoring), is not wired in, and **must not be** (`state.md`,
`track-b-arms-spec.md` §11 item 7). Wiring a second research engine into the daily pipeline beside
it invites the two to be run, read and quoted as a pair, and puts an advisory number one rendering
step away from an instruction card. The daily loop's contract is three verdicts, never blended
(`daily-loop-spec.md`); this engine produces none of them.

**Reads:** I-1 … I-5 (§1.1).
**Never reads:** `data/counterfactuals.csv` (§3.3) · `data/archive/*` (v1 is frozen and is never a
reporting input, `CLAUDE.md` §3) · the raw export directly (§1.1).
**Writes:** `data/comparative/` only. Never a bot config, never an instruction card, never
`STATUS.md`, never `trades.csv`.

### 6.3 Emission floor

Descriptive output is suppressed below **`n_matched_days ≥ 20`** for the family in question — a
single suppressed-output line, so the stage is exercised without publishing noise. This mirrors
R-4's start condition in form; ⛔ **the value 20 is a proposal and needs a signature (G-16)**, since
R-4's own threshold was ruled rather than assumed.

Verdicts are emitted only at a stamped gate-eval date (§2.6). At `n=0` the engine prints
`EMPTY — n=0 matched days` and exits 0 — an absent number is never rendered as a zero.

### 6.4 Refusals — the engine's own kill switches

| R | Condition | Behaviour |
|---|---|---|
| R-1 | `ledger_meta.json` missing, `ledger_start == "2099-01-01"`, or `export_rows == 0` | refuse, exit non-zero |
| R-2 | `risk` second-witness mismatch on a position | drop the position, count it, never repair |
| R-3 | aggregate without its `n` | raise |
| R-4 | verdict without `K` / `mde_fam` / `seed` / `B` / exclusion counts | raise |
| R-5 | verdict without a stamped gate-eval date | refuse the verdict, emit descriptive only |
| R-6 | `pnl_may_be_modelled == true` (`itmlive != market`) | refuse the verdict |
| R-7 | `\|bca_a · z\| > 0.30` | refuse the interval |
| R-8 | `--gate` on a date ≠ the stamped date | refuse |
| R-9 | I-5 absent and the criterion needs it | `BLOCKED`, never `PASS` |

### 6.5 Version discipline

`VERSION` constant, `FROZEN_ON = None` until Andy freezes it — the `execution_audit.py` pattern.
The engine is **advisory until each PR entry is signed**; signing is what makes its numbers
operative, and nothing it emits authorises a build, a switch-on, or a switch-off.

---

## 7. Adversarial review — what survived

*Two subagents, instructed to refute, defaulting to "this is wrong": one on general statistical
validity, one on computability and the two-engine seam. **Both succeeded** — 12 FATAL and 26
MATERIAL objections. Every load-bearing claim below was re-verified by this session directly on the
device before adoption; the ones that changed the design are already in the text above. This section
records what could not be fixed here.*

**Reading key: FIXED** — the spec above changed. **CARRIED** — real, unfixable at this level, travels
with the machinery. **GATED** — needs Andy; listed in §8.

| # | Objection | Status |
|---|---|---|
| **CM-1** | **FATAL — conjunct (a) is inert.** (b) at K=6, n=100 demands ≥0.035R; (a) demands ≥0.015R. Every sample passing (b) passes (a). The calibrated margin does no work, and any pass is Type-M inflated ≥2.4× over the largest effect the program has measured | **CARRIED and quantified** — §2.5. `mde_fam` is mandatory on every verdict. This is §12 row 16 with the Bonferroni term included; row 16 states ±0.026R and the operative figure is ±0.035R |
| **CM-2** | **FATAL — (c) is uncomputable.** No exit-reason field exists in the 30-column ledger or the 26-column export; `tags` is bot-level and set at open; the ITM label is unobserved (D4) | **FIXED in form, GATED in substance** — the proxy is rejected outright (§1.4) and I-5 is specified instead. Building I-5 is G-1 |
| **CM-3** | **FATAL — the `expired` exclusion is a row-level filter on a group-level unit**, and under C8 mixed-status condors are the *designed* shape for every early-exit arm. Both naive readings bias `d_i`, in opposite directions, at arm-dependent rates | **FIXED as a reading, GATED as a ruling** — X-1 + the G-4 box. Incidence is printed per arm regardless of how it is ruled |
| **CM-4** | **FATAL — `d` is not zero-inflated** in a between-bot contrast; the stated BCa rationale is false, ρ≈0.90 is unearned, and the extra dispersion is confounded with the treatment because `profits`/`stoploss`/`tstop` are credit-referenced | **FIXED (rationale struck, §2.1) + CARRIED (the confounding)** — H1's trigger-level effect is a standing limit, not a fixable one |
| **CM-5** | **FATAL — the 15:44 FIRED cut is a dead constant** (S-4 gated an object C8 removed), **empties PR-22** (which closes at 15:45), and rests on an unverified timezone (D3 open) | **FIXED** — the whole proxy is withdrawn, §1.4 |
| **CM-6** | **FATAL — MFE/MAE censor at the trigger**, so a threshold test sits *on* the value the mechanic created and resolves on the sign of the slippage, which is monotone in `d_i`. Selection on outcome, at an arm-dependent rate (CF-1) | **FIXED** — no MFE-based FIRED test. **CARRIED** for PR-17/PR-18's liveness, which have no other route |
| **CM-7** | **FATAL — the n≥60 kill is a one-sided fixed-n interim look on the gate's own vector**, forbidden by §10a item 4; arms reaching the gate are conditioned on a favourable draw | **FIXED in the engine** (interim = confidence sequence only, §2.6) — **GATED** in the PR text, G-8 |
| **CM-8** | **FATAL — (c) cannot pass for PR-19 by construction** (n_fired ≥ 8 required; the arm's hypothesis is that it never fires). CF-11's defect one layer up | **GATED — G-5.** Engine reports `INCAPABLE`, never `FAIL` |
| **CM-9** | **FATAL — PR-19's degeneracy criterion**: uncomputable, ill-posed (overlapping-window scan, no cadence, "consecutive" undefined), and arithmetically unfireable (expected 1.2 of 40 against a requirement of 20) | **GATED — G-13.** `degeneracy_fireable: false` emitted with the arithmetic |
| **CM-10** | **FATAL — K is under-corrected ~1.8×**: nine declared decisions run against the single Ride control, not six | **GATED — G-9.** `family_census` enumerates them; K is not changed |
| **CM-11** | **FATAL — "S-1 puts Track B outside the family" is a category error**; S-1 is slot budget, not error rates, and both Track B arms share Ride, the day-series and the entry automations | **FIXED (claim withdrawn) + GATED — G-11** |
| **CM-12** | **FATAL — PR-14…PR-20 have no gate-eval date**, so GATE-CM is an open-ended peeking machine and the no-influence rule has no anchor | **FIXED structurally** (R-5 refuses the verdict) — **GATED — G-7** |
| **CM-13** | **MATERIAL — `<D100>` needs an exchange calendar, mixes per-condor with per-side, has an unresolved unit (C10), and propagates no estimation error** | **GATED — G-14.** Engine refuses to stamp |
| **CM-14** | **MATERIAL — `PAIR_WINDOW_S = 180` can delete a day for the entire family**, selectively on fast days, and the loss is reported as a non-fill that never happened | **FIXED (mitigated)** — `pairing_at_risk`, §1.7. The constant remains load-bearing and unversioned |
| **CM-15** | **MATERIAL — `pnl` may be a model output** under `itmlive = auto`, with no flag, landing disproportionately on Ride and PT50 | **FIXED (refusal R-6)** — but see CM-16 |
| **CM-16** | **MATERIAL — CF-1's own mitigation is itself uncomputable.** *"Every arm-vs-control ΔR is reported alongside [the per-arm count of Market-priced and ITM-action closes]"* — that count needs the **pricing field**, which lives in the Trades list | **CARRIED, and it is the sharpest surviving item.** The publication precondition CF-1 sets for every ΔR in this family cannot be met from the export. I-5 supplies it; without I-5, no ΔR meets its own declared publication condition |
| **CM-17** | **MATERIAL — the unmatched-day count is not computable.** An absent row conflates no-signal / non-fill / bot-off / pairing artifact / filtered export, and there is no trading-day calendar, so all-arms-no-fill days are invisible entirely | **CARRIED** — §8.4 H2 *requires* this instrumentation ("log non-fills per arm, report unequal n") and the named inputs cannot supply it. A per-bot per-day state record is a further missing input |
| **CM-18** | **MATERIAL — including the Canary in the matching predicate** costs `n` for zero inference and makes a bot with no scientific role a single point of failure over all five real comparisons | **GATED — G-2.** `\|M7\|` vs `\|M6\|` printed every run |
| **CM-19** | **MATERIAL — PR-16's worst-condor test is a coin flip** (P ≈ 0.5 under the null), uncorrected and outside the family | **GATED — G-12.** `no_inference` annotation emitted |
| **CM-20** | **MATERIAL — `B = 10,000` cannot resolve a family-adjusted BCa endpoint** (order statistic ~42, or the 4th after the BCa shift) | **FIXED** — `B ≥ 200,000` for the family interval, §2.2 |
| **CM-21** | **MATERIAL — `â = skew/(6√n)` is driven by one or two days at n=60–100** and is undefined on a constant vector | **FIXED (mitigated)** — `bca_a`/`skew_d` emitted, refusal R-7 |
| **CM-22** | **MATERIAL — block bootstrap on a gap-deleted, arm-dependently-gapped index resamples an artifact** | **FIXED** — withdrawn, §2.2 |
| **CM-23** | **MATERIAL — emitting `ci95_*` beside `ci_fam_*` is a forking path**; three intervals will exist on quantities a reader treats as one | **FIXED** — `diagnostics` block, `NOT_A_GATE`, §3.1 |
| **CM-24** | **MATERIAL — (c) conditions on a post-treatment outcome-correlated variable**, so it estimates a different estimand from (a)/(b) and is ANDed to them as though it did not | **CARRIED** — §2.3. Repair requires a pre-treatment subpopulation, i.e. a signed-text change |
| **CM-25** | **MATERIAL — the +0.015R bar is ~12× harsher on a 5 %-firing arm than on a 60 %-firing one**, because R-3's figure is per *fired* position and (a) is diluted by non-firing days | **GATED — G-6.** `fire_rate` emitted beside (a), always |
| **CM-26** | **MATERIAL — "not opening `counterfactuals.csv` enforces independence" is false**; it enforces ignorance. And the retirement's stated rationale was narrowed by C8 and is flagged for Andy | **FIXED (wording corrected to §10a's own honesty line) + CARRIED** — §3.3 |
| **CM-27** | **MATERIAL — `ledger_meta.json` was not a named input**, so the cutover assertion the design promised was unwritable; and `trade_id` is not stable across rebuilds | **FIXED** — I-2 added, refusal R-1; §1.3 guard 2 |
| **CM-28** | **MATERIAL — I-4 does not contain what the design said it contains**, and inferring thresholds from tag strings is memory-derived config | **FIXED** — §1.1a; affected criteria report `SKIPPED` |
| **CM-29** | **MATERIAL — basis and unit mixing** inside one liveness conjunct (credit-basis MFE gating a risk-basis effect; per-row breach classifying a per-condor `d_i`, with the put-breached/call-not case undefined) | **GATED — G-15.** Three breach flags emitted, no verdict taken |
| **CM-30** | **MATERIAL — PR-21's DiD runs over disjoint day-sets** (day 91+ vs day 1+), so unrestricted it confounds arm with calendar | **FIXED** — overlap-only, `n_overlap` printed, §3.4 |
| **CM-31** | **MATERIAL — Bonferroni and max-T are swapped relative to where power is scarce** | **GATED — G-10** |
| **CM-32** | **MATERIAL — "matched days" names three different populations** (`M7`, `MB(21)`, `MB(22)`) and any sentence about "the family's mean ΔR" is ambiguous over them | **FIXED** — §1.5 names all three; every emission carries its set |
| **CM-33** | **MATERIAL — no n=0 contract, no suppression rule, no mandatory-field rule** was stated | **FIXED** — §6.3, §6.4 |
| **CM-34** | **WEAK/MATERIAL — the Canary occupies one of the six Bonferroni slots** while being *"not evidence about anything"* | **GATED — G-9** (the 6-vs-5 limb) |

**Attacks that failed**, recorded because a review that reports only hits is not a review:

- *"The retire-scoped ruling removes rows from this engine's input."* Defeated — it scopes Track A's
  computed family in `counterfactuals.csv`; no ledger row changes. Both reviewers conceded this
  limb explicitly.
- *"Per position vs per condor is a real unit departure."* Defeated on the project's own
  definitions — R-6 and `CLAUDE.md` §4 make them one unit. The **averaging** unit is the real
  departure, and it is now named separately (§2.4 rationale 2).
- *"The day is the wrong resample unit."* Not sustained — neither reviewer produced a better
  exchangeable unit for a between-bot contrast on a shared signal; the objections landed on the
  *set* of days, not the choice of unit.
- *"Reading the raw export directly would be simpler."* Defeated — §1.1; it re-implements four
  things `build_ledger.py` already does correctly and re-opens the §5 bug class.

---

## 8. ⛔ What Andy must rule before this can discharge the signing gate

*Nothing below is applied. Each is a decision, and `CLAUDE.md` §5 keeps decisions gated.*

| G | Ruling needed | Consequence if unruled |
|---|---|---|
| **G-1** | **Authorise `data/exit_rows.csv`** — a per-position exit-attribution capture from the Trades list (§1.4 schema). A new capture surface, one step per trading day | Five declared criteria across all seven arms stay unfireable. `pre-registration-ledger.md` §2 rule 2: *"A criterion needing evidence nobody collects is not a criterion."* §7 item 3 stays open |
| **G-2** | Matched-day predicate: **`M7` (declared, all seven) or `M6` (six comparative arms)** | `M7` stands. The Canary's 2-day RED can halt all five comparisons |
| **G-3** | Confirm **"exactly one condor per arm per day"** as the matched-day tightening | The day-mean / condor-mean identity in §2.4 rationale 2 rests on an unratified reading |
| **G-4** | Confirm **X-1's group-level reading of R-7** (exclude only all-expired groups) | The exclusion is an interpretation of a signed ruling. Both alternatives bias `d_i`, in opposite directions, at arm-dependent rates |
| **G-5** | **Disapply conjunct (c) on PR-19**, or accept that PR-19 has a kill criterion and no reachable gate | PR-19 can never pass GATE-CM |
| **G-6** | Whether **+0.015R** stands as a bar on a **fire-rate-diluted** mean, given it is ~12× harsher on a 5 %-firing arm than a 60 %-firing one, and was derived from a **PT** move | The bar means something different on each arm and nothing says so |
| **G-7** | **Stamp a `GATE EVAL DATE` for PR-14…PR-20** (and add the field to `pre-registration-ledger.md` §2's template — `track-b-arms-spec.md` §11 item 5) | No verdict is emitted for those arms. §10a item 2 is unsatisfiable and the no-influence rule has no anchor |
| **G-8** | Bring the **absolute n≥60 kill criteria** under the family correction and sequence them against the gate | CF-2's finding is live: the kill fires on the winners, 40 days before the gate is reachable |
| **G-9** | `BONFERRONI_K`: **6 (declared) / 5 (tests that run) / ≥9 (decisions against the shared control)** | K=6 ships. Over-corrected by ~2.4 % on z, under-corrected ~1.8× against the real family |
| **G-10** | Whether to replace **Bonferroni-across-6 with a joint day-bootstrap max-T** (`greenfield-family-spec.md` Phase C step C4 is a declared analysis convention) | The engine with no power to spare keeps the conservative correction; Track A keeps the efficient one |
| **G-11** | Whether **PR-21/PR-22 are statistically in the greenfield family** (S-1 ruled slots, not error rates) | `k_basis: "DECLARED — statistical family not ruled"` ships on both |
| **G-12** | Re-specify or accept **PR-16's worst-condor test** (P ≈ 0.5 under the null) | The Trail arm can be retired on a coin flip, worded as a refuted claim |
| **G-13** | Re-specify **PR-19's degeneracy criterion** — it is uncomputable, ill-posed and unfireable (expected 1.2 of 40 vs a requirement of 20) | `degeneracy_fireable: false` ships. CF-11 is not actually fixed |
| **G-14** | **`<D100>`**: the calendar basis, the per-condor vs per-side unit, and C10 | The engine refuses to stamp `<D100>`; ARM-B1 is not an arm |
| **G-15** | The **put-breached / call-not-breached** case for a per-spread threshold classifying a per-condor `d_i` | Three breach flags emitted, no verdict taken from them |
| **G-16** | The **`n_matched_days ≥ 20`** emission floor (R-4's analogue, proposed not ruled) | 20 ships as an assumption where R-4's own threshold was ruled |

**Two dependencies outside this list, already open and already Andy's or Day-0's:** **D3** (the
export/backstop timezone — no wall-clock predicate is safe until it is answered) and **D2/D4**
(`itmlive = market`, and whether the ITM action appears in a Trades list and under what label —
refusal R-6 and PR-14's inverted liveness both wait on these).

---

## 9. What this spec is measured against

- `research-loop-spec.md` §10 / §10a — **restated, not amended.** No text in that file was edited.
- `greenfield-family-spec.md` §9 / §8.4 / §12 rows 13 and 16 — row 13 is scoped by this document;
  **row 16's sample-size question is answered with a number (§2.5) and remains Andy's.**
- `track-b-arms-spec.md` §11 item 7 — scoped; items 5 and 9 are surfaced as blockers (G-7, §1.1a).
- `pre-registration-ledger.md` §2 rules 1–3 and §7 item 3 — **§7 item 3 is discharged for Layer 1
  and explicitly NOT discharged for Layer 2**, with the missing input named and specified.
- `evidence-standards.md` §4 — B3 is the ratified regime-change conjunct; **this engine does not
  evaluate B3**, and no arm graduates on GATE-CM alone. `build-plan.md` §5's gate stays conjunctive.
- `CLAUDE.md` §4 (unit law, compare by R) and §9.1a (a tool success message is not verification).
