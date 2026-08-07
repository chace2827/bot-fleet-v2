# Post-U-1 decision package — 2026-08-07

**STATUS: DECISION NOTE. Two ruling slots, plus two implementation constraints recorded for the
comparative-machinery build. This document edits nothing.**

It is a new file. No existing doc, no config, no OA object, no git operation was touched by the
session that wrote it. Where it finds an existing document falsified, it **flags it** rather than
applying the correction — both items below are decisions, and `CLAUDE.md` §5 keeps decisions gated.

**Why it exists.** Check **U-1** came back **NEGATIVE** overnight 2026-08-06/07. G-1 was ruled
*"AUTHORIZE, conditional on U-1 positive … reverts to HOLD if U-1 negative"*
(`g-rulings-card-2026-08-07.md`, ruling sheet line 32), so **G-1 is on HOLD** and the
`exit_rows.csv` question re-presents under a degraded schema. Separately, **G-12** was ruled
**RESPEC** with the replacement statistic deliberately not invented by the applying session; §1
drafts it for signature.

**Evidence rules used throughout.** Every aggregate carries its `n` and its unit. Quotes are
byte-exact against the named file. The v1 archive (`data/archive/trades.csv`) is cited **only for
column semantics and format** — never as a number about the fleet — per `CLAUDE.md` §3 and
`data/archive/README-v1-ledger.md`. `data/trades.csv` is header-only (`n = 0` rows);
`data/ledger_meta.json` carries `"ledger_start": "2099-01-01"`, `"export_rows": 0`. **An absent
number is not a zero.** Simulated figures are labelled as such and are from the adversarial review
recorded in §1.6, whose model reproduces `comparative-machinery-spec.md` §2.5's own
`SE(mean d) = 0.013416` to three significant figures.

---

# ⚡ RULING SLOTS

```
G-12b  PR-16 T1 — FAST-MOVE TAIL PAIRED NON-HARM TEST          (drafted in §1)
       Replaces the struck worst-condor-R clause. Three signed constants:

       S1  delta  = 0.10 R per condor, on the tail set T   [ 0.10 | other: ........ ]
           A NEW MARGIN. No inherited authority from R-3's +0.015R (§1.4).
       S2  p      = 0.20  (tail fraction; m = ceil(p*n))   [ 0.20 | other: ........ ]
       S3  floor  = n_matched_days >= 100, plus ONE re-arm at Day-0 + 9 months
                                                           [ as stated | other: .... ]

       Family membership   [ INSIDE the family correction (recommended) |
                             uncorrected one-sided 5% ]
       Acknowledge the standing publication cap of §3        [ acknowledged ]

       Ruled ..................................  Date ..........


G-1'   exit_rows.csv, re-presented under the degraded schema   (§4)
       [ AUTHORIZE-DEGRADED | DECLINE | DEFER ]

       Recommendation: DECLINE, plus two ~5-minute Day-0 checks —
       D3 (export timezone) and the Automation Log link's target (§4.1).

       Acknowledge that no option available here makes CF-1's publication
       precondition meetable (§3)                            [ acknowledged ]

       Ruled ..................................  Date ..........
```

**Not a ruling slot, but read before ruling either:** §2 records two **family-level implementation
constraints on G-10**. They are not PR-16 items and they are not for Andy to rule tonight — they are
flagged for the comparative-machinery implementation (Claude Code, post-downgrade). One of them, if
missed, silently undoes G-10's entire stated rationale for **every arm in the family**.

---

# 1 · G-12 REPLACEMENT — PR-16 T1, redrafted

## 1.1 What was struck, and what the replacement has to do

The struck text, verbatim from `greenfield-family-spec.md` §9's PR-16 entry:

> worst-condor-R worse than the Ride control's at n ≥ 60 → the "no new risk" claim is refuted and
> the arm is retired.

Why (`comparative-machinery-spec.md` §4): it compared *"two **sample minima** — an extreme order
statistic — with no CI, no tolerance, no correction and no membership in the Bonferroni family.
Under a null of exchangeable arms, `P(min_X < min_C) ≈ 0.5`."*

**PR-16's actual question**, from its own HYPOTHESIS block, verbatim:

> Judge on the LOSS TAIL and maxDD-R, not mean R — `hedge-research.md` §14.1: the mechanic is nearly
> free on calm tape and **bites in the fast-move tail**, and the tail is where IC losses already live.

**Four binding constraints:** computable from **Layer 1 alone** (G-1 on HOLD) · evaluated **once**
at the stamped gate-eval date (G-7, spec §2.6) · consistent with the **family correction** (G-10) ·
consistent with the **CS kill rule** — no fixed-n interim look, no retirement before the gate-eval
date (G-8).

## 1.2 THE TEST

**Definitions.** All from Layer 1: `data/trades.csv` + `data/ledger_meta.json` + `data/bots_meta.csv`.

- `R` per condor `= Σ pnl / max(risk)` over the `trade_id` group, **risk = the larger side**
  (`CLAUDE.md` §4, ruling R-6). Carried as **`[DERIVED, UNCORROBORATED]`** per
  `comparative-machinery-spec.md` §1.2 (*`ror` is not a ledger column*); §1.3 guard-1's
  risk-from-strikes re-derivation and its refusal count apply unchanged.
- `M6` = the **G-2** matched-day set over the six comparative arms PR-14…PR-19. `n := |M6|`,
  labelled `n_matched_days`.
- `X` = PR-16 `GF-QQQ-IC-Trail`; `C` = PR-14 `GF-QQQ-IC-Ride`.
- `d_i := R_X(i) − R_C(i)` for `i ∈ M6` — the family's existing paired construction, spec §2.1,
  **unchanged**.

⭐ **THE TAIL SET IS SELECTED ON AN ARM-NEUTRAL DAY-LEVEL VARIABLE:**

```
move_i := | underlying_close − underlying_open | / underlying_open        (day i)
T      := the m days in M6 with the LARGEST move_i,   m := ceil(p · n),   p = 0.20 declared
```

Both fields are in the 30-column ledger header. **`move_i` is identical for every arm**, because
every arm trades the same underlying on the same day. That single property is what everything below
depends on.

**STATISTIC:**

```
dTail := (1/m) · Σ_{i ∈ T} d_i
```

`dTail < 0` means: **on the fastest-moving fifth of matched days, the Trail arm did worse than the
Ride control.** That is the arm's own declared mechanism domain — *"bites in the fast-move tail"* —
so the selection variable and the hypothesis now name the same set of days.

**Interval.**

- Joint day bootstrap: resample matched-day indices with replacement, the **same** resampled index
  vector applied to every family member. `B ≥ 200 000`; seed declared and recorded (spec §2.2).
- **`T` is recomputed inside each replicate** from that replicate's `move` series, so the uncertainty
  about *which* days are the fast-move days is bootstrapped, not conditioned away.
- ⛔ **The simultaneous-bound construction is NOT specified here, deliberately.** G-10's ruling box:
  *"this spec's `BONFERRONI_K` (§3.1) and `ci_fam_*` construction (§2.5) are now superseded and need
  restating under max-T; **not done here**."* T1 **consumes** that restatement; it must not dictate
  it. An earlier draft of T1 did dictate it and thereby damaged every other arm in the family — that
  finding is now §2, where it belongs.
- Percentile and BCa intervals are still computed and emitted in `diagnostics`, flagged `NOT_A_GATE`.

**Decision rule.**

```
RETIRE PR-16   iff   ci_fam_hi(dTail)  <  −δ
```

Retire only when the family-corrected evidence says the Trail arm's mean R on the fast-move tail is
worse than the control's **by at least δ**. `INCAPABLE` is a distinct verdict from `PASS` and `FAIL`
and is **never** read as a retirement.

**Sequencing — G-8 compliant, and stricter than G-8 requires.**

- Computed **exactly once**, at PR-16's stamped `GATE EVAL DATE` (Day-0 + 6 months per G-7), or once
  more at the S3 re-arm date.
- ⛔ **No confidence sequence is emitted for `dTail`.** This draft **declines** to claim
  empirical-Bernstein CS validity for a tail-restricted statistic; §2.6's CS machinery is specified
  for means of the full paired sequence. Pre-gate, `dTail` is descriptive and flagged `NOT_A_GATE`.
  Retirement cannot fire before the gate-eval date.

## 1.3 What this redraft kills, and what it does not

Stated plainly, against the reviewer's round-2 findings.

### KILLED

| # | The objection | Why the redraft kills it |
|---|---|---|
| **NEW-1** | ⛔ FATAL. *"`dTail` is biased **positive** under the null."* Selecting `T` on the **control's** own outcome makes regression-to-the-mean the dominant signal: with ρ < 1, `E[R_X ǀ R_C ∈ worst-p] > E[R_C ǀ R_C ∈ worst-p]` strictly, so **an arm identical to the control "outperforms" on the control's worst days**. Measured null offset: **+0.0057R at ρ=0.99, +0.0277R at ρ=0.95, +0.0553R at the family's declared ρ=0.90, +0.1108R at ρ=0.80** — i.e. at ρ=0.90 the offset is **55 % of δ in the direction that prevents retirement**, and at ρ=0.80 it **exceeds δ outright**. Spec §2.1 states the true ρ runs *below* the declared 0.90. On 400,000 null draws the realised one-sided Type-I rate was **< 2.5 × 10⁻⁶** against a nominal 0.05 | **KILLED BY CONSTRUCTION.** `move_i` is a day-level variable **identical for every arm**, so conditional on `T`, `X` and `C` are exchangeable under the null and `E[dTail] = 0` **by symmetry**. The offset is not estimated, bounded or corrected — it does not exist. There is no ρ-dependent nuisance parameter left |
| **NEW-2** | ⛔ FATAL. *"structurally blind to arm-specific new tail risk, which is the literal claim under test."* "No new risk" means loss days the **arm** has and the control does not — days which, under control-selection, are **by construction not in `T`**. Measured: against a simulated arm-specific new-loss mode, `dTail` registered **3.1 % / 2.9 % / 4.0 %** of the arm's own tail harm at new-loss rates of 2 % / 5 % / 10 %. *"The criterion **cannot fire on new risk at any effect size**"* | **SUBSTANTIALLY KILLED.** Fast-move days enter `T` **regardless of which arm lost on them**, so an arm-specific tail event that occurs on a fast-move day is inside the selection window rather than definitionally outside it. ⚠️ **Not fully killed — see the residual below** |
| **NEW-6** | MATERIAL. *"`p = 0.10` sits **exactly on** the loss rate, so `T`'s composition is a coin flip, resampled inside every replicate."* The family's own `SD(R)=0.30` and `R_max ≈ +0.083…+0.162` force a loss rate `q = 0.10`; at `p = 0.10`, **11.9 %** of tail slots were filled by a *winning* day and **45.3 %** of samples contained at least one. Plus: tie-breaking by calendar date made membership depend on a property of the sample, not of `F`, *"and therefore not a property the bootstrap can be consistent for"* | **KILLED.** `move_i` is continuous with no atom and no cluster boundary at any quantile. No tie rule is needed, no calendar-order dependence, no regime-switching tail set inside the bootstrap. **`p` is thereby freed from the arm's loss rate** and can be set for power — which is why S2 restores `p = 0.20` (§1.4) |

### NOT KILLED — carried, and named

| # | Sev | The objection | Status under this redraft |
|---|---|---|---|
| **NEW-2 residual** | MATERIAL | An arm-specific loss mode that occurs on a **calm** day is still outside `T` | **CARRIED. This is the honest limit on what T1 can conclude.** T1 answers *"does the trail harm the tail in the regime it claims to operate in"* — not *"does the trail add loss anywhere."* That narrowing is deliberate (it is the arm's own declared domain) and it is declared, not discovered |
| **NEW-4** | MATERIAL | The conditional-on-`T` SE *"is not a jackknife of the estimator, is biased low by 22 %, and is 77 %-noisy."* Measured `E[SE_hat] = 0.0504` vs true `SD(dTail) = 0.0643` (**0.78×**); across datasets median 0.0527 with **IQR 0.0101–0.0824** — an 8× span. Not a validity defect (bootstrap-t stays first-order valid), but `se_dtail` and `mde_tail` are **mandatory published outputs** | **MITIGATED, NOT REPAIRED.** `sd_dtail_boot` (the bootstrap SD of `dTail`) is mandatory **alongside** `se_dtail`, and **`mde_tail` must be computed from `sd_dtail_boot`**, never from `se_dtail` (§1.5) |
| **NEW-7** | MATERIAL | The δ transport-from-R-3 argument fails twice | **ACCEPTED — the argument is WITHDRAWN.** δ is presented as a new margin with no inherited authority (§1.4) |
| **NEW-8** | FATAL to the claim | *"the headline claim ('easier to fire than the PASS gate') is false under every correction"* | **ACCEPTED — the claim is WITHDRAWN.** Replaced by mandatory `mde_tail` and by the honest arithmetic in §1.4, which shows T1 firing at roughly the **same order** as the PASS gate, not below it |
| **R1-1 residual** | MATERIAL | `mean d = p·dTail + (1−p)·d_offT` is an exact decomposition, so `dTail` is a **component** of GATE-CM's own (a)/(b) statistic, not an orthogonal column | **CARRIED.** Measured `corr(dTail, mean d) ≈ 0.70` under selection-on-outcome — they do disagree in sign, so this is not the vacuous restatement the *first* draft was (`corr ≈ 0.999`). But the family contains a statistic and a part of it, and a max-type correction over partly-collinear members is conservative in an unquantified way |
| **R1-2 residual** | MATERIAL | `SD(d ǀ T) ≠ 0.134`. Measured `SD(d ǀ control's worst decile) = 0.147` — *"conditioning on control-bad days **raises** paired dispersion, because those are precisely the days the mechanic acts"* | **CARRIED.** The equivalent figure under `move_i` selection is **unmeasured**. `sd_d_tail` is a mandatory published output and δ's power claim is explicitly conditional on it (§1.4) |
| **R1-7** | MATERIAL | **R-6 / modelled P&L.** Spec §6.4: `pnl_may_be_modelled == true` (`itmlive != market`) → **refuse the verdict**; §1.7: *"No ledger field flags a modelled row."* Greenfield §7: an ITM-expiring position's P/L is *"estimated from the underlying close price — a modeled number, not a fill"*, and *"ITM-at-expiry is by definition the losing tail."* **A tail statistic concentrates modelled rows where a mean dilutes them** | **CARRIED.** `itmlive = market` is already a hard Day-0 gate (greenfield §7 assumption 2); the verdict is refused until it is set. `pnl_may_be_modelled` is a mandatory output |
| **R1-8** | MATERIAL | **X-1 deletes the tail before the tail is formed.** Spec §1.6 X-1 excludes a group iff **every** row is `expired` — under `itmlive = auto`, exactly the ITM-expiry condors. Compounded by §1.5's exactly-one rule, one arm's exclusion drops the day **for all six** | **CARRIED.** `n_all_expired_*` and `n_days_dropped_all_expired` are mandatory outputs. Instrumentation, not repair |
| **R1-9** | FATAL to publication | **CF-1.** *"no tail-based ranking is published without"* the D7 per-arm Market-priced / ITM-action counts — which need a label U-1 proved absent | **CARRIED — and it is the standing cap. See §3** |
| **NEW-3, NEW-5** | FATAL to the family | — | **MOVED OUT of PR-16.** These are constraints on the G-10 implementation, not on this criterion. **See §2** |

## 1.4 The three named signature slots

| Slot | Quantity | Proposed | Status |
|---|---|---|---|
| **S1** | `δ` — non-harm margin, R per condor, on `T` | **0.10 R** | ⛔ **A NEW MARGIN** |
| **S2** | `p` — tail fraction | **0.20** (⇒ `m = 20` at `n = 100`) | new |
| **S3** | capability floor + re-arm | `n ≥ 100`; **one** re-arm at Day-0 + 9 months | new |

### S1 · δ = 0.10R — presented per NEW-7 as a new margin with no inherited authority

⛔ **The transport argument is withdrawn.** An earlier draft argued that a harm of `δ` on a fraction
`p` of days contributes `p·δ` to the unconditional mean, so `δ` "inherits" R-3's signed materiality.
The reviewer refuted it on two independent grounds and both are accepted:

1. It requires `d ≈ 0` off the tail, which is false for this arm — *"the trail's dominant effect is
   on winning days, all of which are off `T`."* Measured at 60 % winner truncation:
   `mean d = −0.0485` while `dTail = +0.0451`. **The two channels are not separable, so the
   transported number does not mean what it was used to mean.**
2. *"Dividing R-3's signed `+0.015R` mean-margin by `p` to obtain a conditional-decile margin is a
   re-derivation, not a transport."* Spec §2.4 item 4 already ruled on this exact move: *"Re-scaling
   it to this family's credit would be a **new margin needing a new signature** and is not done."*

**So δ is a new margin, and it occupies a signature slot with no borrowed authority.** The honest
anchors, post-review:

- **Scale.** The family's declared paired daily SD of `d` is `0.30 · √(2·(1−0.90)) ≈ **0.134 R**`
  (spec §2.5). `δ = 0.10R ≈ 0.75 ×` that SD. Against the measured *conditional* dispersion on a
  selected tail (`0.147`, R1-2), `δ ≈ 0.68 ×`. Sub-SD either way.
- **Money.** Per-condor net risk ≈ **$185** (`greenfield-family-spec.md` §9 conventions), so
  `0.10R ≈ $18.50 per condor` across the fast-moving fifth of matched days.
- **What it takes to fire — with the corrected SE, not the refuted one.** `SE(dTail) =
  SD(d ǀ T)/√m`. At `m = 20` and a **planning value** of `SD(d ǀ T) ≈ 0.15`, `SE ≈ 0.0335R`. The
  rule fires at about `−(δ + c·SE)`:

  | `c` (simultaneous critical value) | source of the value | fires at `dTail ≈` |
  |---|---|---|
  | 2.30 | G-10's own hoped-for figure (*"recover most of the 2.638 → ~2.3 gap"*) | **−0.177 R** |
  | 2.638 | Bonferroni K=6, two-sided — the value G-10 replaced | **−0.188 R** |
  | 2.92 – 4.69 | **measured** under a studentized construction (§2, NEW-3) | **−0.198 to −0.257 R** |

- ⛔ **Whether that is reachable is not knowable today**, because `c` is not knowable until the G-10
  restatement exists and the data exist. **The "easier to fire than the PASS gate" claim is
  withdrawn** (NEW-8): scaled by `p` for comparability, the fire points above correspond to roughly
  **0.035R – 0.051R** of mean-R impact, against GATE-CM's own operative bar of *"an observed
  mean(d) ≥ +0.035R"* (spec §2.5). **T1 fires at the same order as the PASS gate, not below it.**
  That is stated rather than sold.
- **What replaces the withdrawn claim is structural, not arithmetic.** `mde_tail` — the minimum
  detectable tail harm at the **realised** `n`, `m` and `c` — is a **mandatory output**, and a
  `RETIRE` may not be published without it. That is the discipline spec §2.5 already imposes on
  `mde_fam`: *"A PASS at an `mde_fam` of 0.035R is a different claim from a PASS at 0.015R, and the
  number that distinguishes them must travel with the verdict."*
- **The bracket, so the choice is visible.** `δ = 0` retires on any detectable tail harm
  (≈0.08–0.16R here) — the over-eagerness G-12 struck. `δ = 0.20R` fires at ≈0.28–0.36R and is the
  **G-13 / CF-11 unfireable-criterion failure mode**. `0.10R` sits between them. It is a judgement,
  offered for signature.

⚠️ **`SD(d ǀ T) ≈ 0.15` is a planning value, not a measurement**, and the `move_i`-selected figure
is unmeasured. `sd_d_tail` is a mandatory output; if it lands materially above 0.15, `mde_tail` will
say so at the gate date and δ's power claim degrades accordingly.

### S2 · p = 0.20

`p` must be large enough that `m` supports an interval and small enough that `T` is a tail. At
`n = 100`: `p = 0.20 ⇒ m = 20`; `p = 0.10 ⇒ m = 10` and `SE` rises by √2. Because NEW-6 is killed —
`move_i` is continuous, so no cluster boundary pins `p` to the loss rate — **`p` is now free to be
set for power**, and 0.20 is that setting. It is a signature slot because it changes what the
criterion measures.

### S3 · capability floor and the re-arm, declared now

- `tail_test_capable := (n_matched_days ≥ 100)`. Below it the verdict is **`INCAPABLE`, never
  `RETIRE`, never `FAIL`** — mirroring §2.3's `sign_test_capable`, which reports `INCAPABLE` rather
  than `FAIL` for the same reason.
- ⚠️ **`n ≥ 100` is not comfortably reachable at Day-0 + 6 months.** ≈**126** NYSE trading days, and
  `M6` needs **all six** of PR-14…PR-19 to produce exactly one included condor after X-1/X-2/X-3 and
  after `build_ledger.py`'s 180-second pairing window. Required per-arm per-day survival for
  `n ≥ 100` in 126 days is **0.962**; at 0.95 survival you need ≈136 trading days, at 0.90 ≈188.
- **Therefore, declared now — before any data exists, which is the point:** if `n < 100` at the
  first stamped date the verdict is `INCAPABLE` and the test **re-arms exactly once**, at
  **Day-0 + 9 months** (≈**189** trading days; per-arm survival of **0.899** suffices). If `n < 100`
  again, `INCAPABLE` is **terminal** and PR-16 carries no tail retirement rule — written here so
  that outcome is chosen rather than discovered.
- ⚠️ **Implementation note, not a decision:** spec §2.6's refusal and refusal **R-8** assume a single
  stamped date. Admitting a second declared date is an engine change and belongs to Claude Code.

## 1.5 Mandatory outputs — inseparable from the verdict

A `RETIRE` may not be published without all of them.

```
n_matched_days · m · p · delta · sd_d_tail · se_dtail · sd_dtail_boot · c · seed · B ·
mde_tail            (minimum detectable tail harm at the REALISED n, m and c —
                     COMPUTED FROM sd_dtail_boot, never from se_dtail; see NEW-4)
n_condors_X · n_condors_C · n_unmatched_X · n_unmatched_C ·
n_all_expired_X · n_all_expired_C · n_days_dropped_all_expired ·
pnl_may_be_modelled · family_census ·
move_basis: "open-to-close, NOT intraday extreme"
CF1_PUBLICATION_PRECONDITION: <MET | UNMET>
```

**`move_basis` is a declared limitation, chosen and not discovered.** `move_i` is open-to-close, so
it **under-ranks reversal days** — a day that travelled far and came back scores low. The spec
already records that the extremes are unavailable (§4, PR-17 row: *"the ledger has
`underlying_open`/`underlying_close` only, endpoints not extremes"*, marked *"⛔ and not fixable by
I-5 either"*). **It costs power. It does not cost the null centering**, which is the property NEW-1's
kill depends on — and that trade is taken deliberately: an arm-neutral selector with less power beats
an outcome-based selector with a +0.055R null offset.

## 1.6 Adversarial record

**Procedure.** One subagent, instructed to refute, defaulting to *"this is wrong."* Run **twice** —
once against a first draft, once against the revision that adopted its repairs. **Both rounds
succeeded.** Round 1: **14** objections, 3 FATAL. Round 2: **8 new** objections, 3 FATAL, plus a
triage of the original 14. The text above is the post-review text.

**Two headline claims were withdrawn as refuted, not softened:** the δ transport-from-R-3 argument
(NEW-7) and *"easier to fire than the PASS gate"* (NEW-8).

**Design changes forced by the review, largest first:**

| Change | Forced by |
|---|---|
| Statistic changed from a **difference of two separately-selected tail means** to a **mean of paired differences over one commonly-selected tail set** | R1-6 — separately-selected tail sets destroy the day-pairing the SE depends on |
| Tail set moved from **the arm's own worst days** → **the control's worst days** → **the largest-`move_i` days** | R1-3, then NEW-1 — selecting on *any* arm's outcome biases `dTail` under the null |
| `p` restored 0.10 → **0.20** | NEW-6 killed, so the loss-rate constraint lifts |
| Every claim that T1 dictates the family's interval construction — **removed** | NEW-3 (now §2) |
| δ transport argument — **withdrawn** | NEW-7 |
| "Easier to fire than the PASS gate" — **withdrawn** | NEW-8 |
| `mde_tail` computed from `sd_dtail_boot`, not `se_dtail` | NEW-4 |

**The reviewer's own summary of the highest-value edit**, which this redraft adopts in full:

> **Select `T` on an arm-neutral, day-level variable instead of on the control's outcome.** …
> Conditional on a day-level variable common to both arms, `X` and `C` are exchangeable under the
> null, so `E[dTail] = 0` **by symmetry**. … **It is the estimand PR-16 actually declares.**

## 1.7 Exact ledger text — ready to paste at signing

Replaces the struck `worst-condor-R` clause in `greenfield-family-spec.md` §9's **PR-16** entry (and
its mirror in `pre-registration-ledger.md` when PR-16 is entered there). ⛔ **Not applied by this
session** — PR text is gated. The original struck text is left standing per the doc's own convention.

```
KILL CRITERION   [ ... existing Exp(R) and family/liveness/sentinel text unchanged ... ]

                 TAIL RETIREMENT CRITERION — PR-16 T1, FAST-MOVE TAIL PAIRED NON-HARM
                 TEST. Replaces the struck worst-condor-R clause per ruling G-12
                 (RESPEC, Andy, 2026-08-06); method signed <DATE> under ruling G-12b.

                 STATISTIC.  Over the G-2 matched-day set M6 (PR-14..PR-19), with
                 d_i = R_X(i) - R_C(i) per condor (X = this arm, C = GF-QQQ-IC-Ride,
                 R = sum(pnl)/max(risk), risk = larger side, [DERIVED, UNCORROBORATED]):
                   move_i = |underlying_close - underlying_open| / underlying_open
                   T      = the m days in M6 with the LARGEST move_i,
                            m = ceil(p*n), n = n_matched_days
                   dTail  = mean of d_i over i in T
                 T is selected on move_i -- a day-level variable IDENTICAL for every arm --
                 and NEVER on any arm's own outcome. X and C are therefore exchangeable
                 under the null and E[dTail] = 0 BY SYMMETRY. This is the arm's own
                 declared mechanism domain: "bites in the fast-move tail"
                 (hedge-research.md 14.1, quoted in this entry's HYPOTHESIS).
                 DECLARED LIMITATION, CHOSEN NOT DISCOVERED: move_basis is OPEN-TO-CLOSE,
                 NOT the intraday extreme, so it under-ranks reversal days. The ledger
                 carries endpoints only and this is not fixable by exit_rows.csv. It costs
                 power; it does not cost the null centering.

                 SIGNED CONSTANTS.   p     = 0.20        (tail fraction)
                                     delta = 0.10 R      (non-harm margin, per condor, on T)
                                     floor = n_matched_days >= 100   (so m >= 20)
                 delta IS A NEW MARGIN. It is NOT re-scaled or transported from R-3's
                 +0.015R; that argument was refuted in adversarial review and withdrawn.
                 It carries no inherited authority and stands only on this signature.

                 DECISION.  RETIRE this arm iff ci_fam_hi(dTail) < -delta, where ci_fam_hi
                 is the family-corrected upper bound from the joint day-bootstrap
                 simultaneous region under ruling G-10, with THIS MEMBER'S DIRECTION
                 DECLARED **UPPER** BEFORE ANY DATA EXISTS. B >= 200,000; seed declared and
                 recorded. T is recomputed inside every bootstrap replicate.
                 If n_matched_days < 100 the verdict is INCAPABLE -- never RETIRE, never
                 FAIL, and never read as a retirement.

                 SEQUENCING.  Computed EXACTLY ONCE, at this arm's stamped GATE EVAL DATE
                 (G-7). No confidence sequence is emitted for dTail; pre-gate it is
                 descriptive and flagged NOT_A_GATE, and retirement cannot fire before the
                 gate-eval date (G-8). RE-ARM, DECLARED IN ADVANCE: if n_matched_days < 100
                 at that date, the test re-arms ONCE at Day-0 + 9 months. If n < 100 again,
                 INCAPABLE is TERMINAL and this arm carries no tail retirement rule.

                 PUBLICATION.  A RETIRE verdict may not be published without mde_tail
                 (computed from sd_dtail_boot, never from se_dtail), sd_d_tail,
                 n_matched_days, m, c, seed, B, family_census, pnl_may_be_modelled,
                 n_all_expired_X/C, n_days_dropped_all_expired and move_basis.
                 Refusal R-6 stands: no verdict while pnl_may_be_modelled == true
                 (itmlive != market).
                 CF-1's precondition -- "no tail-based ranking is published without" the D7
                 per-arm Market-priced / ITM-action counts -- is UNMET while G-1 is on HOLD.
                 The verdict therefore carries CF1_PUBLICATION_PRECONDITION: UNMET.

                 CARRIED LIMITS, declared: (1) dTail is a COMPONENT of mean d, not an
                 orthogonal statistic (mean d = p*dTail + (1-p)*d_offT). (2) X-1 excludes
                 all-expired groups, which is the ITM-expiry tail; counts are published.
                 (3) An arm-specific loss mode occurring on a CALM day lies outside T and
                 this criterion cannot see it -- T1 answers "does the trail harm the tail in
                 the regime it claims to operate in", not "does the trail add loss anywhere".
```

---

# 2 · FAMILY-LEVEL IMPLEMENTATION CONSTRAINTS ON G-10

**⛔ FLAGGED FOR THE COMPARATIVE-MACHINERY IMPLEMENTATION — Claude Code, post-downgrade
(`CLAUDE.md` §7). NOT PR-16 items. NOT applied to any document tonight. NOT a ruling slot.**

These surfaced while T1 was being attacked, but they are **not about T1**. They are about the max-T
restatement G-10 requires and §3.2 explicitly defers: *"this spec's `BONFERRONI_K` (§3.1) and
`ci_fam_*` construction (§2.5) are now superseded and need restating under max-T; **not done here**."*
Both bite on **every arm in the family**. They are recorded here because this is where they were
measured, and because a session that writes the restatement without them will silently break G-10.

## 2.1 ⛔ CONSTRAINT A — the max-T implementation must not silently undo G-10

**G-10's entire stated rationale**, verbatim from `comparative-machinery-spec.md` §3.2:

> A joint day-bootstrap with max-T across arms would **recover most of the 2.638 → ~2.3 gap** at no
> cost.

**Measured, and it goes the wrong way.** A draft of T1 specified a **studentized bootstrap-t** family
object. On this family's `d` — which is ≈90 % near-degenerate and ≈10 % at ±0.9, i.e. extremely
leptokurtic — the reviewer measured:

| within-day dispersion | single `dR` member, one-sided 95 % bootstrap-t | **max over 9 members = `c`** |
|---|---|---|
| 0.02 | 1.73 | **4.69** |
| 0.05 | 1.60 | **2.92** |

Against Bonferroni K=6 two-sided = **2.638**. The reviewer's conclusion, verbatim:

> The revision's interval construction therefore makes **every PASS test in the family harder than
> the correction G-10 replaced**, at no benefit. This is not a `dTail` problem — it is a family-wide
> consequence the draft imports silently by restating the family object as studentized.

⭐ **And a clean negative result worth recording, because it locates the fault precisely:** adding
`dTail` to the maximum inflated `c` by **0 %** (measured) — *"because `dTail`'s own bootstrap-t
quantile (median 1.41–1.59) sits below the `dR` members' max. The family is defeated by the
studentization decision, not by `dTail`'s membership."*

**THE CONSTRAINT.** The G-10 implementation must either:

- **(i)** avoid bootstrap-t studentization for the family region; **or**
- **(ii)** demonstrate **on real data**, and publish the number, that its realised `c` **does not
  exceed 2.638** — the Bonferroni value G-10 was ruled in order to improve on.

**A max-T implementation whose `c` exceeds 2.638 has not implemented G-10; it has silently reversed
it while carrying G-10's name.** `c` should be a mandatory published field on every verdict object
for exactly this reason.

## 2.2 ⛔ CONSTRAINT B — the family region needs a per-member direction vector, declared pre-data

**The family's members do not point the same way.** Three directions coexist:

| Member | Direction needed | Source |
|---|---|---|
| the five arm-vs-control PASS tests | **LOWER** bound (`ci_fam_lo > 0`) | spec §2.4 conjunct (b) |
| PR-19's G-13 replacement | **TWO-SIDED** — TOST equivalence, band ±0.015R | G-13, ruled 2026-08-06 |
| **PR-16 T1** | **UPPER** bound (`ci_fam_hi < −δ`) | §1.2 above |

The reviewer, verbatim:

> A signed max over statistics whose pivots enter with opposite signs is not the right object, and
> one `c` cannot simultaneously calibrate a one-sided upper region, a one-sided lower region, and a
> two-sided equivalence band.

**THE CONSTRAINT.** The family object must be either **(a)** an explicitly **signed** simultaneous
region with **each member's direction declared in advance**, or **(b)** a two-sided region using
`max_j |T_j*|`.

⚠️ **And it must be declared BEFORE any data exists — which is still true today**
(`data/ledger_meta.json`: `"export_rows": 0`). That timing is the same reason G-10 itself was ruled
when it was: *"declared **before** any data exists — which is today, and stops being true at Day-0."*
A direction vector chosen after the data exist is a post-hoc analysis change, which is the class of
move spec §2.6's whole sequencing discipline exists to prevent.

**A second, smaller item in the same family** (recorded, not elevated): membership makes retirement
**harder** as the family grows — multiplicity conservatism protects an arm from its own safety
criterion. The alternative is to run T1 at an uncorrected one-sided 5 %. **This note recommends
keeping T1 inside the family**, because retiring the arm is a *claim* (*"the 'no new risk' claim is
refuted"*) and this project's evidence law puts the burden on the claim — and because the arm's
execution-integrity protections (family-level, liveness, sentinel) are unaffected by this correction
and are what actually protect against a broken arm. **It is on the G-12b ruling slot; Andy may take
the other side.**

---

# 3 · THE STANDING CAP — stated honestly

⛔ **Under U-1 NEGATIVE plus CF-1, no `RETIRE` verdict from this criterion is publishable until G-1
is re-ruled. The criterion is being drafted now so that it can be signed once — not because it is
live.**

The chain, each link quoted rather than paraphrased:

1. **CF-1's mitigation is a publication precondition**, `greenfield-family-spec.md` §11 CF-1:
   *"D7 records the per-arm count and R-contribution of Market-priced and ITM-action closes; every
   arm-vs-control ΔR is reported **alongside** that count; and **no tail-based ranking is published
   without it**."*
2. **T1 is a tail-based ranking.** It is the tail-based ranking CF-1 was written about.
3. **D7's counts need the pricing field and an ITM label**, `comparative-machinery-spec.md` §7 CM-16:
   *"CF-1's own mitigation is itself uncomputable … that count needs the **pricing field**, which
   lives in the Trades list."*
4. **U-1 established that neither renders**, `docs/state.md`: *"⛔ **U-1 RESOLVED — NEGATIVE.**
   Trades-list rows carry no per-row pricing-mode label and no memo field."*
5. **G-1 therefore reverted to HOLD**, and I-5 does not exist.

⚠️ **And §4 shows no available ruling closes it.** AUTHORIZE-DEGRADED makes the Market-priced count
partly time-identifiable — the 15:52 backstop is the family's only Market close by design — but the
**ITM-action count stays unidentifiable**, because identifying it needs a label and there is no
label. **The choice on §4 is between paying a daily capture cost and not meeting the precondition,
or not paying and not meeting it.**

**What that means in practice, and it is the reason to sign G-12b anyway:**

- T1 is **computable** from Layer 1 today. Its verdict is **emitted**, carrying
  `CF1_PUBLICATION_PRECONDITION: UNMET`.
- Retiring PR-16 on that verdict would be a decision taken **against a declared precondition** —
  legitimate if it is *chosen*, and exactly the kind of thing this project writes down rather than
  absorbs.
- **Signing now is what makes it a pre-registration.** §10a item 2 requires the method be fixed
  before `n` reaches 100; a criterion specified after the data exist is not a kill criterion, it is
  an analysis. The publication cap is a reason to sign early and publish late — **not** a reason to
  defer the signature.

---

# 4 · G-1 RE-PRESENTED UNDER THE DEGRADED SCHEMA

**One ruling slot. AUTHORIZE-DEGRADED / DECLINE / DEFER.**

## 4.1 What U-1 established

`docs/state.md`, verbatim:

> ⛔ **U-1 RESOLVED — NEGATIVE.** Trades-list rows carry no per-row pricing-mode label and no memo
> field (only description/qty/timestamp, a bid→fill price pair, an Automation Log link, "filled at
> $X"); the linked Automation Log detail view's Close Position action card likewise has none.

It was predicted. The G-card's U-1 row said in advance: *"If they do not render, the schema degrades
to `(exit_ts, fill_price)` and `row_type` becomes hand-assigned — which is a materially different
capture cost and should change the ruling."*

**Three things it kills, named because they are load-bearing elsewhere:**

1. **`pricing_mode`** — §1.4's discriminator for `greenfield-family-spec.md` §6.2 **Rule 1**
   (*"pricing separates mechanic 1 from mechanics 2 and 3"*). Rule 1 now has no readable field.
   ⚠️ Flagged, not edited.
2. **`memo`** — §6.2 **Rule 2**'s discriminator, carried as *"provisional until it is read"* (open
   check **D-2/D4**). **It has been read. It is not there.** Rule 2 is dead as written, and with it
   the ITM-action exception that fences PR-14's inverted liveness rule.
3. **Per-arm pricing-mode tagging as a build strategy** — already handled: the six research arms are
   stamped uniform `{"smart":"normal"}` under G-1-HOLD (`state.md`, 2026-08-07 block).

**One thing U-1 did NOT test.** The observation records *"an Automation Log link"* on the rows read.
**Whether that link's target names the closing object for an Exit-Option close is UNOBSERVED.** It
plausibly does for the Events-class 15:52 backstop (an automation) and plausibly does not for Exit
Options (a bot-level bundle). `oa-platform-reference.md` §0.2 applies: *inference from absence is not
an observation.* One ~5-minute read at Day-0 settles it, and it would reopen this ruling on much
better terms. It is **not** assumed anywhere below.

## 4.2 ⭐ The finding that reframes the ruling: most of the degraded schema is already in the ledger

The degraded capture is `(exit_ts, fill_price)` per exit row. **The ledger already carries a
per-spread exit timestamp and a per-spread exit price.**

`data/trades.csv` header, byte-exact, the two relevant columns marked:

```
bot,pillar,underlying,role,epoch,trade_id,symbol,structure,status,quantity,credit,→exit_price←,pnl,risk,open_date,→close_date←,expiration,tags,single_sided,short_put,long_put,short_call,long_call,premium,underlying_open,underlying_close,mfe_pct,mae_pct,mfe_date,mae_date
```

`build_ledger.py` writes **one row per spread**, paired into condors by `trade_id` (ruling R-6). So
each *side* carries its own `close_date` and its own `exit_price`.

**Verified against the frozen v1 archive — schema and format evidence only, never a fleet number**
(`data/archive/trades.csv`, `n = 1,380` spread rows):

| Measurement | Value | Establishes |
|---|---|---|
| rows with `status == closed` | **1,232 of 1,380 spread rows** | the normal case |
| `closed` rows with `exit_price` non-empty | **1,232 of 1,232 (100 %)** | the exit fill price is populated, always |
| `closed` rows with `exit_price == 0` | **0 of 1,232** | it is a price, not a placeholder |
| `close_date` resolution on `closed` rows | **seconds** — `15:50:00` (101 rows), `15:50:01` (44), `11:34:11` (13), `09:45:02` (12) | a fill timestamp, not a date stamp |
| `close_date` on `status == expired` | `16:15:00` on **140 of 148** | a settlement stamp, **not** a fill |
| `trade_id` groups | **934**, of which **446** are two-row (condor) groups | |
| two-row groups with **different** `close_date` on the two sides | **374 of 446 = 83.9 %**; median gap **448.5 s**, max **14,530 s** | per-spread exit timing is real and already resolved |

**Consequence.** Under **C8** there is no `GF-SiblingClose`, so each side exits on its own; and at
**1 lot** (§5.4) each side has exactly one exit fill. The `(exit_ts, fill_price)` pair the degraded
schema would capture is, for this family, **the pair `build_ledger.py` already writes as
`(close_date, exit_price)`**.

**Honest marginal list — what a degraded Trades-list capture would still add:**

- the **bid→fill pair** on the exit order (a direct per-exit slippage measurement);
- **working orders that did not fill** — SmartPricing ladder steps, and the 15:50 exit order still
  live when the 15:52 backstop fires (§6.2 Rule 3, memo finding N-6);
- a usable **exit time for `expired` rows** (shrinking at Day-0, since under `itmlive = market` an
  expiring-ITM position is *closed*, not expired);
- an independent **second witness** on `(close_date, exit_price)`, which `oa-export-schema.md` §6's
  own discipline (*"never trusts this column alone"*) would otherwise lack.

Real — and **much smaller than the list G-1 was authorized against**, because that authorization
rested on `pricing_mode` and `memo`.

## 4.3 What a degraded capture can and cannot discriminate

§1.4 rejected the close-time proxy on **five** grounds. A **per-arm, per-exit-order, time-based**
assignment is stronger on three, self-resolving on one, **unchanged on one** — and the unchanged one
is the one that matters.

| §1.4's ground | Under a degraded `(exit_ts, fill_price)` capture |
|---|---|
| *"15:44 is a dead constant"* — S-4's gate on an object C8 removed | **GONE.** No shared constant; each arm is read against **its own** declared mechanic times (15:50 Expiration, 15:52 backstop, 15:45 for PR-22) |
| *"It empties PR-22"* — `Exp1545` closes at 15:45, later than 15:44 | **GONE.** At second resolution 15:45 / 15:50 / 15:52 are three separated times |
| *"The clock is unverified"* (open check **D3**) | **SELF-RESOLVING, cheaply.** The 15:52 Events backstop fires at a known wall clock on every arm; one day of `close_date` calibrates the offset from data already on disk. ⚠️ **A proposed test, not a resolution — D3 stays open until it is run.** (Suggestive only: 145 of 1,232 v1 `closed` rows sit at `15:50:00`/`15:50:01`, expired SPX rows stamp `16:15:00`. Both consistent with ET. That is an inference from the archive, not an observation) |
| *"MFE/MAE censor at the trigger"* | **GONE if and only if MFE/MAE and fill-price thresholds are not used to classify.** ⚠️ **It returns the instant anyone classifies by proximity of `fill_price` to a declared threshold** ("exit ≈ 0.5 × credit ⇒ PT50") — the identical defect in new clothes. Any authorization must forbid price-threshold classification in the schema note itself |
| *"The ITM limb is unimplementable"* | ⛔ **UNCHANGED, AND NOW PERMANENT.** U-1 removed both discriminators from the surface they were to be read from. There is no route to labelling an ITM-action row |

⭐ **What makes time-based assignment stronger here than the spec's general argument implies:** under
Option A each arm holds **exactly one** exit mechanic, so the problem per arm is three-way —
*{the arm's own mechanic, the 15:50 Expiration exit, the 15:52 backstop}* — plus the unlabellable ITM
action. Every arm's own mechanic except PR-22's fires **intraday**, minutes to hours before 15:50.

⛔ **The strongest argument against, stated at full strength.** `comparative-machinery-spec.md` §2.3,
verbatim, on the FIRED subpopulation:

> It is **not** inferred from close time, from MFE/MAE, or from anything in I-1 (§1.4).

**A degraded capture assigns `row_type` from close time. It does the thing the spec forbade.** The
table above argues the specific defects behind that prohibition are mostly absent in the specific
per-arm form proposed — but the prohibition is in the spec's declared text, and overriding it is a
decision, not a reading.

⛔ **A hazard the degraded route introduces that the full schema did not.** Hand-assignment puts a
human at the classification step, and that human sees the position's P/L — an analyst decision on the
outcome variable, the same defect class as conditioning on MFE/MAE. **If AUTHORIZE-DEGRADED is
chosen, `row_type` must not be hand-assigned.** Capture `(exit_ts, fill_price, bid, description)`
mechanically; assign `row_type` by a **deterministic rule declared in writing before Day-0 and
executed by code**. That converts the capture from a judgement into an instrument, and costs one
paragraph.

## 4.4 Which blocked criteria it unlocks, and which stay dead

A1's "Unblocks" list, re-adjudicated. `n` here counts **criteria**, not positions.

| Blocked item | FULL schema | DEGRADED schema |
|---|---|---|
| **GATE-CM conjunct (c)** — sign test on the FIRED subpopulation | ✅ | ⚠️ **PARTIAL** for PR-15/16/17/18 (intraday mechanic vs 15:50/15:52 is a wide separation). ⛔ Contaminated by unlabellable ITM rows at an **arm-dependent** rate (CF-1). ⬛ Moot for PR-19 — **G-5 disapplied (c)**. Also needs restating under G-10, which retired the `α′ = 0.05/K` basis of `sign_test_capable` |
| **PR-14 Ride inverted liveness** — *any PT/trail/touch/stop row → RED, **except** ITM-action rows* | ✅ | ⛔ **STAYS ADVISORY.** Detection works (Ride has no early mechanic, so any non-15:50/15:52 exit is anomalous). **The ITM exception cannot be implemented**, and §9 is explicit: without it *"a mislabelled ITM close kills the control on day one and every comparison in the family loses its referent"* |
| **PR-18 SL100 stop-row liveness** | ✅ | ⚠️ **MOSTLY.** SL100's only early mechanic is the stop, so an early row is a stop row modulo ITM. The *threshold-breached* limb reads `mae_pct` from the ledger — already ⚠️ on a credit-basis question, unchanged |
| **PR-19 SL200 liveness / degeneracy** | ✅ | ⬛ **LARGELY MOOT.** Liveness disapplied by design (CF-11); the degeneracy criterion that needed the stop-row count was replaced by **G-13 (REPLACE-EQUIV, TOST ±0.015R)**, Layer 1 only |
| **PR-20 Canary PT-fill detector** — *"the fleet's only forward exit-engine detector"* | ✅ | ⭐ **UNBLOCKED — the strongest argument for AUTHORIZE-DEGRADED.** The spec's objection was that *"any price-based proxy is indistinguishable from a one-cent early close"* — but on the Canary there **is no other mechanic that produces an early close**. Its 5 % target is sub-tick, so the signature is a fill minutes after open, hours from 15:50. ⚠️ §4.2 cuts the other way: the ledger's own `close_date` already detects a same-morning close, so the marginal value of a *Trades-list* capture here specifically is small |
| **PR-22 K2** — *zero `speedy` close rows at ~15:45 across 10 consecutive matched days* | ✅ | ⛔ **DEAD AS WRITTEN.** `pricing_mode == speedy` is unreadable — and now vacuous, since under G-1-HOLD all arms are stamped uniform `{"smart":"normal"}`. Making K2 fireable needs a respec of signed PR text: a separate gated decision. (PR-21/PR-22 are unsigned; neither arm is buildable today) |
| **CF-1's publication precondition** | ✅ | ⛔ **DEAD.** The Market-priced count is partly time-identifiable (the 15:52 backstop is the family's only Market close by design); the **ITM-action count is not identifiable at all** without a label. **§3's cap stands** |

**Tally, in criteria:** of **6** blocked items plus CF-1 — **1** unlocks cleanly (PR-20's detector,
itself approximable from the ledger), **2** partially and with arm-dependent contamination, **1**
stays advisory, **1** is mooted by other rulings, **2** stay dead.

## 4.5 The realistic daily capture cost

Assumptions labelled, because A1's *"one capture step per trading day"* was priced against the full
schema.

- **Positions per trading day at Day-0: 7** — PR-14…PR-20, one condor each (§1.5's exactly-one rule).
  **14 spread exits.** With Track B later: 9 positions / 18 spread exits.
- **Surface:** one Trades-list page **per position**. No bulk export exists — the 26-column OA export
  carries no exit-reason field (`oa-export-schema.md` §1), and the `/bots` bookmarklet reads bot
  configuration, not position trade rows.
- **Who pays it:** under the **2026-08-04 OA automation amendment** (`CLAUDE.md` §5) Claude drives
  Chrome directly, so this is **Claude session time appended to the existing ~17:30 ET daily loop**,
  not Andy's clicking. A genuine reduction against A1's framing.
- **Estimate:** ~7 page reads + parse + append ≈ **10–20 minutes per trading day**, every trading
  day. Over Day-0 + 6 months (**≈126** NYSE trading days) ≈ **21–42 hours**; over the re-arm horizon
  of Day-0 + 9 months (**≈189** trading days) ≈ 32–63 hours.
- ⛔ **Not reconstructible retroactively.** A1's DEFER text is unchanged by U-1: *"the arms accrue
  days with no attribution record, and the record cannot be reconstructed retroactively."*
- **It adds a daily failure mode.** A surface that must run every trading day can silently stop
  running — the shape of the v1 failure this program exists to prevent. Any authorization should
  carry its own liveness assert: rows appear every trading day, or the brief goes RED.

## 4.6 Options and recommendation

**1 · AUTHORIZE-DEGRADED.** Build `data/exit_rows.csv` with the schema reduced to
`bot,open_date,short_put,short_call,exit_ts,row_type,fill_price,bid_price,description,quantity,capture_file,capture_sha`
— `pricing_mode` and `memo` dropped; `row_type` assigned by a **pre-declared deterministic rule
executed by code**, never by hand (§4.3); `UNATTRIBUTED` kept as a first-class value; price-threshold
classification explicitly forbidden.

**2 · DECLINE.** Layer 2 stays `BLOCKED` permanently; `pre-registration-ledger.md` §7 item 3 closes
for Layer 1 only; refusal **R-9** (`BLOCKED`, never `PASS`) becomes the standing state for every
Layer-2 criterion.

**3 · DEFER.** Identical in effect to DECLINE, with the interim days unrecoverable. Given §4.5's
non-reconstructibility, **DEFER is the strictly worse form of DECLINE**, included for completeness.

### ⭐ RECOMMENDATION — **DECLINE, and re-spend the budget on the two checks that actually block.**

1. **The authorization's stated basis is gone.** A1 recommended AUTHORIZE because I-5 would make five
   declared criteria fireable. §4.4 re-adjudicates that to **one clean unlock, two partial, two
   dead** — and the clean unlock is approximable from `close_date`, already in the ledger.
2. **§4.2 is decisive.** The degraded schema's headline content is **already written by
   `build_ledger.py`** — second resolution, 100 % of closed rows, per-side independence realised on
   83.9 % of v1 condor groups. Authorizing a daily manual capture to obtain data the ledger already
   carries is the expensive half of the decision buying the cheap half of the information.
3. **What would have justified it is exactly what U-1 removed.** Attribution needed a *label*. There
   is none. Everything else is inference from time, which §2.3 prohibits, and which cannot resolve
   the ITM rows CF-1 says are the confound.
4. **The blocking items are cheaper elsewhere.** Two ~5-minute Day-0 checks are worth more than 126
   days of capture: **D3** (resolvable from the 15:52 backstop's own `close_date` on day 1) and **the
   Automation Log link's target** (§4.1) — which, if it names the closing object, returns a large part
   of attribution for free and reopens this ruling on much better terms. **It has not been looked at.**
5. ⚠️ **What DECLINE costs, so it is chosen and not discovered.** PR-14's inverted liveness stays
   ADVISORY forever; PR-22's K2 stays dead; and **CF-1's publication precondition is never met** —
   which is §3's standing cap, and it applies to T1. **That is not a footnote.**

⚠️ **The honest counter-case for AUTHORIZE-DEGRADED**, so the recommendation is not the only thing
read: the bid→fill pair is the only direct slippage instrument this program would have, CF-1 is
fundamentally an execution-class confound, and slippage is the quantity CF-1 is about. A capture
scoped **only** to that — bid, fill, timestamp, no `row_type`, no attribution claim at all — would be
a smaller, cleaner object than either option, and would sidestep §2.3's prohibition entirely because
it would classify nothing. It is not offered as a formal option because it is a different instrument
with a different purpose, and it should be scoped on its own rather than smuggled in under G-1.

---

# Close-out

**Files written this session: this one only.** No existing document edited. No OA object touched. No
git operation run. `docs/state.md` and `docs/session-log.md` **not** written — concurrent sessions
own those, per the instruction this session ran under.

**Flagged for a later session, not applied here:**

1. `greenfield-family-spec.md` §6.2 **Rule 1** — its discriminator (`pricing_mode`) is unreadable
   per U-1.
2. `greenfield-family-spec.md` §6.2 **Rule 2** — its discriminator (the memo) was *"provisional until
   it is read"*; it has been read and is not there. Open check **D-2/D4** should close NEGATIVE.
3. `comparative-machinery-spec.md` §1.4 — the I-5 schema's `pricing_mode` and `memo` columns are
   unsourceable; the section needs a dated U-1 banner.
4. **§2's two constraints** — for the G-10 max-T restatement (Claude Code, post-downgrade). Not a
   doc edit tonight; a build constraint.

**Verification.** `sha256` of this file, read directly on the device with `device_bash` — not a
tool-success message, not a stage-back read (`CLAUDE.md` §9.1a) — is recorded in the session summary
accompanying it.

**Ready to commit:** `docs/post-u1-package-2026-08-07.md` (new file, no other change).
