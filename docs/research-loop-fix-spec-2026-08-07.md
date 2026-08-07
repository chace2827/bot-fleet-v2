# Research loop — fix specification for the three fatal defects

*Written 2026-08-07. **This document is a SPECIFICATION, not code, and not a decision.** It edits
nothing. `scripts/research_loop.py` is untouched and remains `0.1.0-DRAFT` under the standing
DO-NOT-WIRE order (`research-loop-review-2026-08-04.md` §1; `research-loop-spec.md` §6.5). Its
product is the instruction set Andy hands to Claude Code.*

**Scope.** The three fatal defects of `research-loop-review-2026-08-04.md` §5 — **D-6** (units),
**D-7** (the `CONTROL` tautology), **D-8** (censoring by the incumbent exit). Per defect: the faulty
code cited byte-exact, the corrected computation with a unit named at every term, the validation
fixture that would have caught it, and the re-run expectation. D-8 gets a documentation fix, because
it is not fixable in code.

⛔ **Nothing here amends a signed document.** Where the correct implementation depends on a choice
Andy has not made, it is listed in **§10 OPEN — GATED** and the fixture is specified so that it does
**not** certify the unsigned choice. Under `CLAUDE.md` §5 (doc-edit authority) this file is a new
document that changes no decision; the items in §10 are decisions and stay gated.

---

## 0. Verdict in one paragraph

The units fix is correct and sufficient for D-6, and a fixture built on four verbatim real ledger
rows kills every units mutation I could construct. The `CONTROL` fix is correct but **does not**
catch the D-6 class, contrary to the review's §7 step 2 — the two branches share no operand, so the
D-6 regression test has to be a numeric assertion inside the PT and DSTOP branches themselves.
D-8 cannot be tested at all from historical data and must be converted from a silent gap into a
**loud, asserted absence**. Three further defects surfaced during adversarial review that are the
same severity as the three named ones and are specified here as **D-15 / D-16 / D-17**: `delta_R` is
emitted per leg while the §10 margin is per position; the loss-side `cf_$` is unclamped and can
posit a loss larger than the position's risk; and MFE/MAE fail to bracket the realised outcome on
**291 of 1,380** ledger rows (21.1%), which the specified guard did not check.

---

## 1. Verification base

Read fresh from the device this session, in full, before anything below was written:
`docs/research-loop-review-2026-08-04.md` · `scripts/research_loop.py` · `docs/research-loop-spec.md`
(as amended: R-1…R-7, the 2026-08-05 releases, §6.5, §10a and its 2026-08-06 scoped-retirement
append) · `docs/oa-export-schema.md` · `docs/comparative-machinery-spec.md` §0–§1.4 ·
`docs/post-u1-package-2026-08-07.md` §2 · `docs/g-rulings-card-2026-08-07.md` (G-8/G-9/G-10/G-11) ·
`scripts/daily.sh`.

**Every number in this file was recomputed this session, read-only**, from one of two frozen v1
sources, and each is labelled with its source and its `n`:

| tag | file | n | note |
|---|---|---|---|
| `[EXPORT]` | `data/captures/oa_export_positions_2026-07-30.csv` | 1,386 rows; **1,254 same-day**; 1,136 same-day+closed; 118 same-day+expired | the review's own base |
| `[LEDGER]` | `data/archive/trades.csv` | 1,380 rows → **934 `trade_id` groups** (488 size-1, 446 size-2, 0 size>2) | the frozen v1 ledger |

⛔ **Both are frozen v1 pre-cutover data** (`CLAUDE.md` §3). They are used here exactly as
`research-loop-spec.md` §1a uses them — to establish **arithmetic feasibility**, a property of the
instrument and the export, not of the regime. **No figure in this document supports a live-capital
decision and none is offered as one.** `data/trades.csv` is header-only: **n=0**; `data/ledger_meta.json`
still carries the pre-Day-0 sentinel `"ledger_start": "2099-01-01"` and `"export_rows": 0`.
An absent number is not a zero.

**Reproduction of the review's figures.** Recomputed independently and matched exactly: same-day
n=1,254 / closed 1,136 / expired 118; dollar-credit-to-risk median **0.06952**, p10 0.03627, p90
0.15607 `[EXPORT]`; SL100/SL150/SL200 fire 279 / 200 / 172 of 1,254; PT40/PT60/PT70 fire 749 / 461 /
299 of 1,254; the rejected `DSTOP_50R` / `DSTOP_75R` rungs fire **42** and **26** of 1,254 once units
are corrected. The censoring signature of §6.5 also reproduces on `[LEDGER]`:
`QQQ-IC-0DTE-Raw-HoldToExp` MFE≥0.70 on **65/80 (81.2%)**, median MFE 1.000; `IC-SPX-FastPT25-S2`
**39/364 (10.7%)**, median 0.286; `IC-SPX-FastPT25-S2-130PM` **0/70 (0.0%)**, median 0.250.

⭐ **One figure in the review needs its basis named.** R-1's *"median credit\$/risk\$ … 0.0695"* is on
the **dollar** credit basis (`openPrice × 100 × quantity`). The per-contract ratio
(`openPrice / risk`) is **4.41×10⁻⁵** `[EXPORT], n=1,254`. The review's number is right; a reader who
takes "credit" to mean the price column will be off by 100 × quantity — which is the same confusion
that produced D-6. Stated here, not corrected there.

---

## 2. DEFECT 1 — D-6 · UNITS

### 2.1 The faulty code, byte-exact

`scripts/research_loop.py`, quoted verbatim with its own indentation. Each line was confirmed
**single-match** in the file by substring count.

Line 115 — the profit-target counterfactual:

```
                cf = param * credit
```

Line 124 — the stop-loss counterfactual:

```
                cf = -param * credit
```

Lines 133–134 — the fixed-dollar stop:

```
                thresh = param * risk
                if (mae * credit) <= -thresh:
```

Line 154 — the conditional rung:

```
                cf = -lvl * credit
```

And the source of `credit`, lines 91–94:

```
    _prem  = _f(row.get("credit"))
    if _prem is None:
        _prem = _f(row.get("premium"))
    credit = abs(_prem) if _prem is not None else None
```

**Why it is wrong.** `credit` here is the ledger's `credit` column, which `build_ledger.py` writes
from the export's `openPrice` — a **per-contract price in $/contract**. `pnl` and `risk` are
**dollars**. `cf` is subtracted from `pnl` at lines 116/125/136/155 (`cf - pnl`), so a price is
subtracted from a dollar amount. The missing factor is `100 [$ per contract per $1.00 of price] ×
quantity [contracts]`.

**`quantity` is never read anywhere in the file.** Verified: `grep -c quantity scripts/research_loop.py`
→ 0.

**The magnitude of the error is not 100×.** `[EXPORT], n=1,254 same-day rows`: quantity is **>1 on
1,066 rows (85.0%)**, median **11**, max **192**. The error factor is `100 × quantity`, so the
**median** error factor is **1,100×** and the maximum is **19,200×**. On `[LEDGER]` the largest
single-position factor is also 19,200× (`T00554`, quantity 192).

**The consequence the review names, reproduced.** Because `cf` is two to four orders of magnitude
smaller than `pnl` on every FILLED row, `delta = cf - pnl ≈ -pnl`. The `delta` column is not a
counterfactual; it is the negated realised P/L of whichever subset the variant selects. Worked on
`T00034` (§5 F-1): the buggy engine reports PT70 `cf=0.35, delta=-34.65` for a position that closed
at **exactly** 70% of credit, whose true delta is **$0.00**.

### 2.2 The corrected computation

Units are named at every term. `[$]` = US dollars. `[$/ct]` = dollars per contract (a price).
`[ct]` = contracts. `[1]` = dimensionless.

**Constants**

```
MULT = 100          [$ per ct per $1.00 of price]     the options contract multiplier
```

⛔ Do **not** hard-code `MULT` without checking it. Derive and assert per row:
`abs(premium) / (credit × quantity) == MULT`. `[EXPORT], n=1,386`: this evaluates to exactly
**100.000000 on 1,386/1,386 rows**, identically for SPY, SPX and QQQ, with 0 rows at `openPrice == 0`.
That makes `MULT = 100` safe **for this file**, and asserting it costs one division.

**Per ledger row (one leg)**

```
credit_$   = credit [$/ct] × MULT [$/ct/$] × quantity [ct]                    -> [$]
MFE_$      = mfe_pct [1] × credit_$ [$]                                       -> [$]
MAE_$      = mae_pct [1] × credit_$ [$]                                       -> [$]
```

`mfe_pct` / `mae_pct` are fractions of `abs(premium)` (`oa-export-schema.md` §4), and
`abs(premium) == credit × MULT × quantity` with **0 mismatches on `[LEDGER]` n=1,380 and `[EXPORT]`
n=1,386**. So `MFE_$` and `MAE_$` above are exact, for credit and debit structures alike.

**Per-structure sign classes** — enumerate explicitly and **refuse on anything else**:

```
CREDIT_STRUCTURES = {ironcondor, ironbutterfly, shortputspread, shortcallspread}
DEBIT_STRUCTURES  = {longcallspread, longputspread}
anything else -> REFUSE the position, count the refusal, never a verdict
```

`[LEDGER], n=1,380`: shortputspread 685 · shortcallspread 559 · ironcondor 98 · ironbutterfly 25 ·
longcallspread 8 · longputspread 5. OA emits structures outside this set (calendars, diagonals,
naked); today they hit no branch and the behaviour is undefined.

**The counterfactual P/L, all in dollars**

```
PT{p}     FILLED iff mfe_pct >= p ;  cf_$ = + p × credit_$
SL{p}     FILLED iff mae_pct <= -p ; cf_$ = max( -p × credit_$ , -risk_$ )        <- see D-16
DSTOP_{k} D_$ = k × M_bot_$  (M_bot_$ per §10 OPEN-2) ;
          FILLED iff MAE_$ <= -D_$ ;  cf_$ = max( -D_$ , -risk_$ )
COND{p}_{t} FILLED iff mae_pct <= -p AND mae_time < t ; cf_$ = max( -p × credit_$ , -risk_$ )
not FILLED and not censored and not undecidable -> NEVER_REACHED, cf_$ = pnl_$, delta_$ = 0
```

**The delta, and the only unit the gate reads**

```
delta_$        = cf_$ [$] - pnl_$ [$]                                          -> [$]
delta_R        = delta_pos_$ [$] / risk_pos_$ [$]                              -> [1]
```

⛔ **`delta_R` is defined ONLY at the position.** See **D-15** (§2.5) — this is the single most
consequential correction in this document after the units themselves.

**Position construction (ruling R-6; `CLAUDE.md` §4; `comparative-machinery-spec.md` §1.3)**

```
group          := all ledger rows sharing trade_id
credit_pos_$   := SUM( credit_$ over group )        [$]
pnl_pos_$      := SUM( pnl over group )             [$]
risk_pos_$     := MAX( risk over group )            [$]   <- the LARGER side, never the sum
delta_pos_$    := SUM( delta_$ over the legs of the group )   [$]
R              := pnl_pos_$ / risk_pos_$            [1]
```

**PT family on a multi-row group -> `UNDECIDABLE`.** Ruling R-6: combined MFE for a paired condor is
a Track B question. `[LEDGER]`: **446 of 934 groups (47.8%)** are size-2, so this is not a corner case
— see §9 objection U-10 for what it does to the PT sample.
**SL / DSTOP / COND on a multi-row group are computed PER-SPREAD and summed to the position**
(`greenfield-family-spec.md` §11 CF-4 establishes that Track A's `SL100`/`SL200` are per-spread
counterfactuals while the greenfield arms are close-both mechanics — non-equivalent estimands,
carried, not solved). The output row must carry `estimand = per_spread_summed`.

**CONTROL — the engine's self-test**

```
CREDIT: cf_$ = (credit [$/ct] - exit_price [$/ct]) × MULT × quantity      -> [$]
DEBIT:  cf_$ = (exit_price [$/ct] - credit [$/ct]) × MULT × quantity      -> [$]
CONTROL_OK iff |cf_$ - pnl| <= $0.01
```

Verified `[LEDGER], n=1,380`: **0 mismatches**, worst residual **4.55×10⁻¹³ $**, with the debit sign
class handled separately. Handling only the credit identity produces **12 false CONTROL_MISMATCHes
among the 1,232 closed rows** — see §3.

### 2.3 Guards that must be part of the fix

**G-1 · MULT assertion.** `abs(premium) == credit × MULT × quantity`, tolerance $0.01. Refuses
0/1,380 `[LEDGER]` today. ⚠️ **This is a sanity assert on the multiplier, NOT a second witness** —
`build_ledger.py` writes `credit` from `openPrice` and `premium` as a raw passthrough, two different
export columns, so it is not code-circular; but both come from the same vendor with no independent
derivation, and it cannot vary. Label it as what it is (§9, objection U-4).

**G-2 · `risk` gets a real second witness.** `oa-export-schema.md` §6 forbids trusting the `risk`
column alone, and this engine puts `risk` in the denominator of every number the gate reads. Derived
this session `[LEDGER]`:

```
CREDIT structures:  risk_$ == width [$] × MULT × quantity - credit_$      1,367 / 1,367 exact
DEBIT structures:   risk_$ == credit_$                                       13 /    13 exact
where width = max( |short_put - long_put| , |short_call - long_call| )
```

⚠️ **`comparative-machinery-spec.md` §1.3 guard 1 specifies this re-derivation as
`short_put/long_put/short_call/long_call × 100 × quantity` and omits the `- credit_$` term, and has
no debit form.** As written, that guard refuses **1,380 of 1,380 positions**. Recorded here as a
finding against that spec; **not corrected there** — that file is a build specification and the
change is Andy's. See §10 OPEN-5.

**G-3 · Bracketing.** `MAE_$ - $0.51 <= pnl <= MFE_$ + $0.51`. This is the invariant the whole
counterfactual rests on, and it **fails on 291 of 1,380 `[LEDGER]` rows (21.1%)** — see **D-17**
(§2.6). Rows that fail go to a named `BRACKET_VIOLATION` stratum whose size is printed beside every
aggregate; they are **not** silently scored.

**G-4 · Refusal is at the `trade_id` GROUP, never the row.** `[LEDGER]`: 446 groups have two legs.
Refusing one leg leaves `pnl_pos_$` and `credit_pos_$` computed over the survivor — a half-condor
whose R has no referent. `comparative-machinery-spec.md` §1.3 gets this right ("refuses the
position on mismatch, counting refusals"); the engine must match it.

**G-5 · Same-day filter (D-12, still open).** `open_date[:10] == close_date[:10]`, applied at the
group. `[LEDGER]`: **126 of 934 groups are multi-day**, and OA-Mirror positions are multi-day by
construction — pooling them into a per-variant mean blends pillars, which the three-verdict contract
forbids. `_hhmm()` discards the date entirely, so every `COND` comparison on a multi-day position is
a clock-time comparison across different calendar days.

**G-6 · Mixed-status and mixed-quantity groups need a stated rule.** `[LEDGER]`: **3 groups have one
`closed` leg and one `expired` leg** (`T00777`, `T00861`, `T00923`); R-7 stratifies `expired` and
gives no rule for a mixed group. **128 of 446 size-2 groups have different `quantity` between legs**,
so `credit_pos_$ = SUM` carries both quantities while `risk_pos_$ = MAX` carries one. Both need a
declared rule before the engine runs. See §10 OPEN-4.

**G-7 · Domain assertions must match the data.** `mae_pct <= 0` is **false on 89 of 1,380**
`[LEDGER]` rows; `mfe_pct >= 0` is false on **30**. Neither breaks the arithmetic, but an assert
written against the stated domain will fire on real data.

### 2.4 The fixture that would have caught D-6

Full row-by-row fixture in **§5**. What matters here is *why* the old one failed and what makes the
new one different.

**Why the old fixture was green while the engine was wrong.** Of its 23 checks, **21 assert only a
verdict string**, and verdicts depend on dimensionless ratios (`mfe_pct >= param`), which no units
error can perturb. The one numeric check is line 271:

```
    check("V17 ...and uses |premium|, so PT40 = +40 not -40", cf16, 40.0)
```

Its row sets `credit="100"`, implicitly dollars. **V17 is a regression test *for* D-6** — it asserts
the buggy identity and would *fail* against a correct engine. And the `dstop` family, the one family
whose verdict depends on units, has **no real-row check at all**.

**What the new fixture does instead.** Four verbatim single-match rows from `data/archive/trades.csv`
carrying **assertions on VALUES in dollars and in R**, with quantity spanning 1 → 192 so that "× 100"
and "× 100 × quantity" are separable, plus a real-row `dstop` check that **fires under the corrected
units and is silent under the bug**.

⚠️ **`F-1` alone cannot do this job.** Its quantity is 1, so it cannot distinguish `× MULT` from
`× MULT × quantity` — verified by mutation: dropping the quantity term fails **zero** F-1
assertions. **F-3/F-4 (quantity 10) do that work on the `cf` path; F-2/F-2b (quantity 144–192) do it
on the `credit_$` / `MAE_$` path.** All four are required.

**Mutation-test result (§9(b)).** Every units mutation — drop `× quantity`, drop `× MULT`, the
original bug, `MULT = 1000`, `delta = pnl - cf`, `delta_R ÷ credit_$`, `risk = SUM` instead of `MAX`,
`mae >= ` instead of `<=`, `DSTOP` on `mae_pct` instead of `MAE_$` — fails between 2 and 17
assertions. **I could not construct a units error that survives the set.**

### 2.5 ⛔ D-15 — `delta_R` is emitted per LEG; the §10 margin is per POSITION

**New, and the same severity as D-6.** The corrected per-row formula produces one `delta_R` per
ledger row. §10's margin is `+0.015R per position` and §10a's permutation test runs on *the
per-position ΔR vector*. Worked on `[LEDGER]` group **`T00002`** (`IC-SPX-FastPT25-S2`, both legs
`closed`, same-day 2026-07-02), variant SL150:

| leg | quantity | credit_$ | risk_$ | pnl_$ | cf_$ | delta_$ | delta_R on leg risk |
|---|---|---|---|---|---|---|---|
| shortputspread | 10 | 350.00 | **4,650** | −1,950 | −525.00 | **+1,425.00** | +0.306452 |
| shortcallspread | 10 | 150.00 | **4,850** | +100 | — (mae 0) | 0.00 | 0.000000 |

`risk_pos_$ = MAX(4,650 , 4,850) = **4,850**` — the larger side, `CLAUDE.md` §4.
`delta_pos_$ = +1,425.00`, so the position's **ΔR = 1,425 / 4,850 = +0.293814**, not +0.306452.
The per-leg number is **4.3% flattered**, and it is flattered in exactly the direction the
2026-07-31 denominator fix already corrected once.

Emitting per leg also doubles `n`: `[LEDGER]` has **1,380 legs against 934 positions**, so a
permutation null built on legs is drawn from a sample ~1.48× too large and its SD is understated
accordingly. §10's `n ≥ 100` and §10a's family are both stated in positions.

**THE RULE.** `counterfactuals.csv` writes **one row per (position, variant)**, carrying
`delta_pos_$`, `risk_pos_$`, `delta_R`, the per-leg `delta_$` values as a diagnostic column, and
`estimand`. **The per-leg number never enters the gate vector.**

### 2.6 ⛔ D-16 — the loss-side `cf_$` is unclamped and can posit a loss larger than the risk

`cf_$ = -p × credit_$` is unbounded above `p`. `[LEDGER], n=1,380`: `p × credit_$ > risk_$` on
**16 rows at SL100, 48 at SL150, 52 at SL200**. On those rows the engine asserts a counterfactual
loss exceeding the position's entire defined risk, which is not a thing a defined-risk spread can do.
**Clamp: `cf_$ = max(-p × credit_$, -risk_$)`**, and count the clamped rows.

Related and worse for debit structures: `[LEDGER]`, the 13 `long*spread` rows satisfy
`risk_$ == credit_$` on **13/13**, so (a) `delta_R = delta_$ / risk_$` silently becomes the **credit
basis**, which `comparative-machinery-spec.md` §0 forbids, and (b) `min(mae_pct) = −0.804` across all
13 with a structural floor of −1.0, so **SL100/SL150/SL200 fire 0 of 13** by construction. Those 39
cells are fabricated zeros. **Rule: the SL and DSTOP families report `N/A — structure` on debit
structures, never `NEVER_REACHED`.**

### 2.7 ⛔ D-17 — MFE/MAE do not bracket the realised outcome on 21.1% of rows

The counterfactual assumes the realised outcome lies inside the excursion envelope. `[LEDGER],
n=1,380`: **`MAE_$ > pnl` on 278 rows** and **`MFE_$ < pnl` on 13** — union **291 (21.1%)**. The
consequence is not cosmetic: a position whose realised return breached −100% but whose recorded
`mae_pct` did not is scored `NEVER_REACHED, delta 0` by SL100 — a fabricated zero of the same class
D-8 produces, arriving by a different route. **Rule:** G-3 above; the violating rows form a named
stratum, counted and printed, never scored silently. The likely cause is the scan-rate sampling of
`oa-export-schema.md` §4 ("max *observed*, not the true intraday max"), which is disclosed for MFE
and never quantified against realised P/L anywhere in the folder.

### 2.8 Re-run expectation for D-6

After the units fix, run the engine read-only over the frozen capture (**never** as a reporting
input — `CLAUDE.md` §3 — purely as a regression harness) and check all five:

**(a) The `dstop` family must fire, and the count is pinned.** On the **rejected** `0.50×risk` /
`0.75×risk` rungs — kept only as the units regression probe, since R-1 rejected the basis — the
expected counts are **exactly 42 and 26 of 1,254** `[EXPORT]` same-day rows (3.3% and 2.1%), against
**0 and 0** under the bug. These are exact integers, not orders of magnitude: any other value means
the fix is not the fix that was measured.

**(b) The SIGNED rungs land in the same order of magnitude as their percentage twins.** `DSTOP_100`
and `DSTOP_150` (`k` × the bot's median dollar credit) fire on the order of **10²** rows, i.e.
**15–25% of the population**, not 0 and not ~all. Measured `[LEDGER], n=1,380`: on the leg-median
basis **340 (24.6%)** and **249 (18.0%)**; on the position-median basis **266 (19.3%)** and
**216 (15.7%)**. The two bases differ by **27.8% relative** at `DSTOP_100` — that spread is §10
OPEN-2, and the fixture must not certify either.

**(c) The R-1 calibration check, which is the real sanity test.** R-1's signed §3 text says the
dollar rungs *"are not a looser stop, they are the same stop anchored in dollars instead of
percent."* So `DSTOP_100`'s fire rate must sit **near `SL100`'s**. Measured: `SL100` fires
**279/1,254 (22.2%)** `[EXPORT]` and **316/1,380 (22.9%)** `[LEDGER]`; `DSTOP_100` on the leg-median
basis fires **24.6%** `[LEDGER]`. Within three points — the calibration holds.
⛔ **If `DSTOP_100` comes back below ~10% or above ~40%, the median-credit calibration is wrong and
the rung is a no-stop control or a position-size filter, which is precisely what R-1 rejected the
RISK basis for.**

**(d) No mean ΔR may approach the gate margin.** R-3 measured the largest mean effect on the whole
capture at **+0.0150R per position**, and computed the arithmetic ceiling on a PT50→PT70 move at
**0.014R per fired position** at a median credit/risk of 0.0695. Expect every variant's mean ΔR to
land in **|ΔR| ≲ 0.05R**. ⛔ **Anything at or above 0.10R is a units bug, not a discovery** — R-3's
own words, and the reason the 0.10R margin was withdrawn: *"the first thing that ever crosses 0.10R
will be a units bug."*

**(e) Bounds hold row-wise.** For every FILLED cell: `-risk_$ <= cf_$ <= credit_$`, and
`|delta_$| <= risk_$ + credit_$`. Print the count of clamped cells (expected 16 / 48 / 52 at
SL100 / SL150 / SL200 on `[LEDGER]`).

**How to sanity-check by hand, in one line.** For any single FILLED PT cell, `cf_$ / pnl_$` must be
a ratio of order 1 (both are dollars). Under the bug it is of order `10⁻²` to `10⁻⁴`. Print
`cf_$`, `pnl_$` and `credit_$` side by side for the first ten FILLED cells and read them: on
`T00034` the corrected engine prints `PT70 cf_$ 35.00 · pnl 35 · credit_$ 50.00`; the buggy one
prints `0.35`.

---

## 3. DEFECT 2 — D-7 · THE `CONTROL` TAUTOLOGY

### 3.1 The faulty code, byte-exact

`scripts/research_loop.py` line 108, verbatim, single-match:

```
            ok = abs(pnl - pnl) < 1e-9
```

in context, lines 106–109:

```
        if fam == "control":
            # the engine claims it can reproduce reality; check it
            ok = abs(pnl - pnl) < 1e-9
            yield (name, "CONTROL_OK" if ok else "CONTROL_MISMATCH", pnl, 0.0, note)
```

`pnl - pnl` is `0.0` for every finite float, so `ok` is unconditionally `True`, `CONTROL_MISMATCH` is
unreachable, and the `THE ENGINE IS WRONG` abort at lines 192–196 is dead code. Fixture checks V4 and
V21 assert `"CONTROL_OK" == "CONTROL_OK"` by construction.

The docstring at lines 18–20 states the contract this code does not implement:

```
  CONTROL_OK / CONTROL_MISMATCH
                the control variant must reproduce the realised P/L. A mismatch
                means THIS ENGINE IS WRONG, not that the strategy underperformed.
```

### 3.2 The corrected computation

```
CREDIT structures:  cf_$ = (credit [$/ct] - exit_price [$/ct]) × MULT [$/ct/$] × quantity [ct]
DEBIT  structures:  cf_$ = (exit_price [$/ct] - credit [$/ct]) × MULT [$/ct/$] × quantity [ct]
verdict = CONTROL_OK  iff  |cf_$ - pnl [$]| <= TOL,  TOL = $0.01
          CONTROL_MISMATCH otherwise -> print, abort, exit non-zero
```

`credit` is `openPrice`; `exit_price` is `closePrice` — confirmed from `build_ledger.py`, not from
prose. The identity is `oa-export-schema.md` §3, and it holds on `[LEDGER] n=1,380` with **0
mismatches** and a worst residual of **4.55×10⁻¹³ $**.

**On the tolerance.** `openPrice`/`closePrice` carry at most two decimals and `pnl` is integral on
1,386/1,386 export rows, so `(credit − exit_price) × 100 × quantity` is exactly integral in real
arithmetic and the only residual is float representation. **`$0.01` is right**, and it is *required*:
on `T00554` the computation returns `192.00000000000017`, so `== 192.0` is `False`. Tightening to
$1×10⁻⁶ still produces 0 mismatches; loosening finds nothing masked. A **relative** limb
(`1e-9 × |pnl|`) is dead code — `max |pnl| = 9,975` `[LEDGER]`, so it maxes out at $9.98×10⁻⁶ and
never binds. Omit it or mark it reserved.

⛔ **The debit branch is not optional.** `[LEDGER]` carries 13 `long*spread` rows, **12 of them
`closed`**, and the two earliest sit at **lines 20 and 21** of the file (`T00011`
`DIR-SPX-Put-Control` and `T00012` `DIR-SPX-CallVIXdrop`). A `CONTROL` written on the credit
identity alone therefore reports `CONTROL_MISMATCH` on any "first 30 rows" end-to-end harness, a
**correct** engine exits 1, and the obvious fix under time pressure is to weaken the abort — which
re-kills D-7. Specify the debit branch and the fixture row together.

### 3.3 ⚠️ The correction the review's own §7 gets wrong

`research-loop-review-2026-08-04.md` §7 step 2 states: *"A real CONTROL that recomputes P/L from
`(openPrice − closePrice) × 100 × quantity` catches the whole D-6 class."*

**It does not.** `CONTROL` reads `credit`, `exit_price`, `quantity`. The PT branch reads `mfe_pct`,
`credit`, `quantity`. They share **no code path and no operand beyond the raw columns**. Verified by
mutation: drop `× MULT × quantity` from the PT branch **only**, and `CONTROL_OK` still returns
1,380/1,380. `CONTROL` verifies OA's arithmetic — which was never in doubt (0 mismatches) — not the
engine's counterfactual scale.

**Consequence for the build order.** `CONTROL` is necessary and must be fixed, but the **D-6
regression test is the numeric real-row assertion inside the PT and DSTOP branches** (§5 F-1/F-2b/F-3),
not `CONTROL`. Recorded here rather than corrected in the review, which is a ruling sheet and not
this session's to amend.

### 3.4 The fixture that would have caught D-7

The mutation test is unambiguous and it is the most important single result in this document:

- **M4** — `CONTROL` reverted to `abs(pnl - pnl) < 1e-9` — fails **zero** of the twenty value
  assertions on the four fixture rows. It is caught **only** by the corrupt-input negative control.
- **M5** — `CONTROL` compares against `abs(pnl)` instead of `pnl` — fails **zero** row assertions
  **and passes the corrupt-`pnl` negative control**, because all the CONTROL-asserted rows are
  winners where `abs(pnl) == pnl`.

So the D-7 defence cannot be a single negative control. **Four checks are required** (§5 N-1…N-4):

1. `F-3 CONTROL cf_$ == -1,950.00` and `CONTROL_OK` — a **loser**. This one line kills M5.
2. `F-1` with `pnl` corrupted to `"9999"` -> `CONTROL_MISMATCH` and `run()` exits non-zero.
3. `F-1` with `exit_price` corrupted to `"99"` -> `CONTROL_MISMATCH`. Corrupts an **input to the
   recompute**, which a tautology is structurally blind to.
4. `F-1` with `quantity` corrupted to `"100"` -> `CONTROL_MISMATCH`. Re-checks the `× quantity` term
   *inside* `CONTROL`, which nothing else does.

### 3.5 Re-run expectation for D-7

- On the frozen capture, `CONTROL_MISMATCH` count must be **exactly 0** across **1,380/1,380**
  `[LEDGER]` rows and **1,386/1,386** `[EXPORT]` rows, with the debit branch present. **Any non-zero
  count is the engine, not the strategy** — and the run must abort with a non-zero exit, printing the
  offending `trade_id`, `structure`, `quantity`, `credit`, `exit_price`, recomputed `cf_$` and
  recorded `pnl`.
- The worst absolute residual over all rows must be **< $1×10⁻⁹**. Print it. A residual in the
  dollars is a units error; a residual in the cents is a rounding error; today's engine reports
  neither because it compares a variable to itself.
- ⛔ **`CONTROL` is not a comparison and does not enter the multiplicity family** (§10a item 1). Its
  `delta` is 0 by construction and must be excluded from every aggregate — the current code does this
  correctly at line 199 and that behaviour must survive the fix.

---

## 4. DEFECT 3 — D-8 · CENSORING BY THE INCUMBENT EXIT — the DOCUMENTATION fix

### 4.1 Why there is no code fix, restated precisely

MFE/MAE accumulate only until the position closed. A position the incumbent PT closed at +50% has
`mfe_pct ≈ 0.50` and **can never evidence 0.70**. From a closed row alone, "the mark never reached
0.70" and "the incumbent exit closed it before it could" are **observationally identical**. The
discriminator is the bot's incumbent exit, which lives only in `data/bots_config_v2.csv`.

That file is **not usable today**. Read directly this session: its header is
`object_kind,name,oa_id,version,attached_to,input_id,input_type,input_label,input_default,a7_hash,captured,layer2_status`
and it holds **one row**, `shared_automation,GF-ScannerA-PutSpread,…`, whose `input_default` reads
`NOT SET — see FINDING F-4` (`comparative-machinery-spec.md` §1.1a, confirmed independently).
So Track A's honesty is gated on Phase-2 config capture, exactly as `research-loop-spec.md` §6.5
states.

**The signature is distributional and per bot, never per row.** `[LEDGER]`, MFE≥0.70 share and median
MFE: `QQQ-IC-0DTE-Raw-HoldToExp` (no PT) **81.2%**, median **1.000**; `IC-SPX-Fortress-Defang`
**57.7%**, median **1.000**; `IC-SPX-FastPT25-S2` (PT25) **10.7%**, median **0.286**; its `-130PM`
clone **0.0%**, median **0.250**. No fixture over four rows can express an 81%→0% collapse across
bots. **This is the honest answer to "would the fixture catch it": no fixture can.**

### 4.2 The documentation fix — what the engine must WRITE

**(1) The output-header censoring limit.** `data/counterfactuals.csv` gets a header block, and the
same text opens `data/research_log.md` every night, verbatim:

```
# CENSORING LIMIT — READ BEFORE ANY NUMBER BELOW
# MFE/MAE accumulate only until the position closed. Track A can therefore evaluate ONLY
# variants TIGHTER than the incumbent exit on the same side. Every LOOSER-side variant is
# right-censored: its NEVER_REACHED is a FALSE NEGATIVE, not a null result, and its delta of
# 0.0 is a FABRICATED ZERO (CLAUDE.md §3, research-loop-spec.md §6.5).
# Looser-side questions are TRACK B questions and are not answerable from this file.
# incumbent-exit source : data/bots_config_v2.csv   status: <PRESENT n=<k> rows | ABSENT>
# censored cells        : <n> of <N>   (<pct>%)   blocked cells: <n>
# censoring UNKNOWN for : <list of bots with no config row>   -> every same-side cell BLOCKED
```

**(2) The per-variant censored flag — three states, never two.** Per (position, variant):

```
censored = FALSE    incumbent exit on that side is KNOWN and the variant is TIGHTER
                    -> verdict may be FILLED or NEVER_REACHED
censored = TRUE     incumbent exit on that side is KNOWN and the variant is LOOSER or EQUAL
                    -> verdict MUST be CENSORED ; cf_$ and delta_$ are EMPTY, never 0
censored = UNKNOWN  no config row for this bot
                    -> verdict MUST be BLOCKED ; cf_$ and delta_$ are EMPTY, never 0
```

⛔ **`UNKNOWN` is the state the engine is in today for every bot**, and it is the state the current
code does not have. `research-loop-spec.md` §6.5's rule names `CENSORED`; the third state is the
consequence of `bots_config_v2.csv` being empty, and without it the engine's default on Day-0 is to
report every looser-side cell as a clean `NEVER_REACHED` with a fabricated zero.

**(3) The columns.** `counterfactuals.csv` carries, per (position, variant):
`censored` · `incumbent_exit_side` · `incumbent_exit_value` · `incumbent_exit_source` (fact ID or
config row) · `variant_is_tighter` (TRUE/FALSE/UNKNOWN). An empty `incumbent_exit_source` forces
`censored = UNKNOWN`.

**(4) The nightly line states the blocked count, and never the mean over blocked cells.**

```
RESEARCH: <n> positions x 12 variants.  <u>/<N> cells UNDECIDABLE, <c> CENSORED, <b> BLOCKED.
          CENSORING: <b> cells blocked (no incumbent-exit config) — Track A is BLIND on the
          loose side for <k> of <m> bots.  NO GRADUATIONS (gate: n>=100 positions + 6mo +
          regime change, §5).
```

**(5) The fixture asserts the absence of coverage rather than staying silent.** `validate()` must
print, and assert, a `SKIP` line:

```
  SKIP  D-8 CENSORING: NOT COVERED BY ANY FIXTURE — unobservable from historical rows.
        Blocked on data/bots_config_v2.csv (currently 1 scaffolding row, input_default NOT SET).
```

so that a green fixture line can never be read as full coverage. **Plus a hard tripwire that IS
testable:** call `evaluate()` with **no** incumbent-exit config and assert that every PT and SL cell
comes back `BLOCKED` — **not** `FILLED`, **not** `NEVER_REACHED`. That check fails against today's
engine, which is the point.

**(6) One more thing the fixture must assert, and it costs one line:** that
`scripts/research_loop.py` is still **absent from `scripts/daily.sh`**. It is the only mechanical
guard on the DO-NOT-WIRE order, and it is cheap.

### 4.3 D-11 made concrete — the order conflict, which the censoring header must also carry

`mfe_date` is never read; the only timestamp loaded is line 99: `    mae_t  = _hhmm(row.get("mae_date"))`.
`research-loop-spec.md` §1's headline claim — that timestamps let a counterfactual test *"whether it
was there **before the exit**"* — is unimplemented, and what ships is the form the spec itself calls
worthless.

**Worked on a real row, this session.** On `[LEDGER]` `T00034`: `SL100` fires (mae −1.1 ≤ −1.0) at
`mae_date 2026-06-29 10:17:00`, and `PT70` fires (mfe 0.84 ≥ 0.70) at `mfe_date 2026-07-01 09:31:00`
— **the stop precedes the peak by two days.** Both cannot happen: under SL100 the position is closed
before the peak exists. The engine reports both, unflagged.

**Rule:** where a same-position PT cell and SL/DSTOP/COND cell would both report `FILLED` and
`mae_date < mfe_date`, the **PT cell is downgraded to `UNDECIDABLE`** with note
`ORDER_CONFLICT — stop precedes peak`, and the conflict count is printed. This is D-11 and D-10 in
one rule and it is not the same defect as D-8, but it is the same failure mode: a number that reads
as evidence and is an artefact of what was never checked.

### 4.4 D-10 quantified — trough time is not breach time

`lowReturnPctDate` is when the extreme occurred, at or **after** the first crossing of the stop
level. `COND` therefore **systematically under-counts fills and never over-counts**. The engine must
carry this as a stated one-sided limit in the output header, with the note text corrected — the
variant's own note silently rewrote "breached" to "trough", and unlike the `dstop` change that
substitution is recorded nowhere.

### 4.5 Re-run expectation for D-8

There is no numeric re-run expectation, because there is no code fix. The expectation is
**structural** and it is checkable in one grep of the output:

- With `bots_config_v2.csv` in its current state, **every PT and SL cell in `counterfactuals.csv`
  must read `BLOCKED`**, and `delta` must be **empty on every row**. Cell count with a numeric
  `delta`: **0**. If any cell carries a number, the engine is fabricating zeros.
- `research_log.md` must exist and must open with the censoring block. It is **never written today**
  (D-13), and the literal `NO CANDIDATES` that §2 declares as the expected nightly output is never
  printed.
- After Phase-2 config capture lands per-bot rows, the blocked count must fall and the **censored**
  count must rise, and the two must sum to the same cells. On a PT25 bot every `PT40/PT60/PT70` cell
  is `CENSORED`; on `QQQ-IC-0DTE-Raw-HoldToExp` (no PT) none of them is.

---

## 5. THE FIXTURE SET

Six real rows plus four negative controls plus three boundary cases. Every real row was verified this
session **byte-exact and single-match** in `data/archive/trades.csv` by `grep -Fxc` = 1, and the
line number is given. **Copy the rows; do not transcribe them** (`oa-export-schema.md` §5 fix 2) —
and carry a `sha256` of each raw line in the fixture so drift between fixture and archive is loud.

Ledger header, for field order:

```
bot,pillar,underlying,role,epoch,trade_id,symbol,structure,status,quantity,credit,exit_price,pnl,risk,open_date,close_date,expiration,tags,single_sided,short_put,long_put,short_call,long_call,premium,underlying_open,underlying_close,mfe_pct,mae_pct,mfe_date,mae_date
```

### F-1 — line 48 · `T00034` · the review's own D-6 worked example

```
3DTE $140-$350,OA-Mirror,SPX,mirror-watch,baseline,T00034,SPX,ironcondor,closed,1,0.5,0.15,35,950,2026-06-29 10:00:03,2026-07-01 09:45:02,2026-07-02 16:00:00,"220,60percent",False,7175,7165,7620,7630,-50,7398.48,7457.91,0.84,-1.1,2026-07-01 09:31:00,2026-06-29 10:17:00
```

⚠️ **This row is multi-day (2026-06-29 → 2026-07-01) and `pillar == OA-Mirror`.** It is retained
because it is the one row in the folder where the corrected delta is exactly zero, but it has **three
jobs and the first is a rejection**:

| id | assertion | value | catches |
|---|---|---|---|
| F1-a | the same-day filter **rejects** this position | `open_date[:10] != close_date[:10]` -> excluded from the population | D-12, pillar blending |
| F1-b | `credit_$` | `0.5 × 100 × 1 = ` **50.00** | D-6 scale |
| F1-c | `PT70` verdict | **FILLED** | branch (see below) |
| F1-d | `PT70 cf_$` | **+35.00** (buggy: 0.35) | D-6 |
| F1-e | `PT70 delta_$` | **0.00 exactly** | D-6 — the review's worked case |
| F1-f | `PT60 cf_$ / delta_$` | **+30.00 / −5.00** | D-6, non-degenerate |
| F1-g | `PT40 delta_$` | **−15.00** | D-6, PT comparison direction |
| F1-h | `MAE_$` | `−1.1 × 50.00 = ` **−55.00** (buggy: −0.55) | D-6 on the dstop path |
| F1-i | `SL150` verdict | **NEVER_REACHED** (−1.1 > −1.5) | SL comparison direction |
| F1-j | `SL100` **and** `PT70` both FILLED with `mae_date < mfe_date` -> `PT70` downgraded to **UNDECIDABLE / ORDER_CONFLICT** | flag present | D-11 (§4.3) |

⚠️ **F1-e is degenerate on its own** and must be paired with F1-c and F1-f. The `NEVER_REACHED`
branch emits `(cf_$ = pnl, delta_$ = 0)`, and this row's `pnl` is 35 — the same number F1-d asserts.
So inverting the PT comparison leaves F1-d and F1-e both green; only F1-c, F1-f and F1-g catch it.
The flagship anti-D-6 assertion is the least informative one in the set, because the row was chosen
precisely so the counterfactual equals reality.

⭐ **F1-e is not a float-equality trap.** `35.0` is computed bit-identically in five association
orders (hex `0x1.1800000000000p+5`); 0.5 and 100 are dyadic and the 0.7 rounding error is absorbed.
The subtraction is exactly `0.0`. Assert exact equality here and tolerance everywhere else.

⚠️ **F-1 cannot separate `× MULT` from `× MULT × quantity`** — its quantity is 1. Verified: dropping
the quantity term fails **zero** F-1 assertions. F-2, F-2b, F-3 and F-4 do that work.

### F-2 — line 791 · `T00554` · the quantity witness, same-day

```
QQQ-IC-0DTE-Baseline,IC,QQQ,control,baseline,T00554,QQQ,ironcondor,closed,192,0.5,0.49,192,9600,2026-04-29 13:30:12,2026-04-29 15:50:11,2026-04-29 16:00:00,,False,654,653,662,663,-9600,658.82,660.14,0.06,-0.1,2026-04-29 15:06:00,2026-04-29 13:31:00
```

Same-day, `status closed`, native `ironcondor` (so its `trade_id` group is size 1 and the position IS
the leg), **quantity 192 — the largest in the file. Error factor here is 19,200×.**

| id | assertion | value |
|---|---|---|
| F2-a | `credit_$` | `0.5 × 100 × 192 = ` **9,600.00** |
| F2-b | `CONTROL cf_$` | **192.00 ± $0.01** — the raw computation returns `192.00000000000017`, so `== 192.0` is **False** and the tolerance is load-bearing |
| F2-c | `MAE_$` | `−0.1 × 9,600.00 = ` **−960.00** (buggy: −0.05) |
| F2-d | position group size | **1** — `risk_pos_$ == 9,600.00`, `pnl_pos_$ == +192.00` |

### F-2b — `T00626` · a large-quantity row where a PT actually FIRES

```
QQQ-IC-0DTE-Baseline,IC,QQQ,control,baseline,T00626,QQQ,ironcondor,closed,144,0.31,0.15,2304,9936,2026-04-23 13:30:34,2026-04-23 15:13:32,2026-04-23 16:00:00,,False,645,644,653,654,-4464,650.05,650.53,0.58064516,-0.4516129,2026-04-23 15:13:00,2026-04-23 13:46:00
```

**New in this spec, and it is the row F-2 could not be.** F-2's MFE is 0.06, so no PT fires on it and
the PT `cf_$` path is untested at large quantity. F-2b fires PT40 at quantity 144, same-day, size-1
group.

| id | assertion | value |
|---|---|---|
| F2b-a | `credit_$` | `0.31 × 100 × 144 = ` **4,464.00** |
| F2b-b | `CONTROL cf_$` | `(0.31 − 0.15) × 100 × 144 = ` **2,304.00 ± $0.01** = `pnl` |
| F2b-c | `PT40` verdict | **FILLED** (0.5806 ≥ 0.40) |
| F2b-d | `PT40 cf_$` | **+1,785.60** (buggy: **0.1240**) |
| F2b-e | `PT40 delta_$` | **−518.40** (buggy: −2,303.876) |
| F2b-f | `PT40 delta_R` | `−518.40 / 9,936 = ` **−0.0521739** |
| F2b-g | `PT60` verdict | **NEVER_REACHED** (0.5806 < 0.60) — brackets PT40 from above |

### F-3 — line 19 · `T00002` (both legs) · the position-aggregation and dstop witness

```
IC-SPX-FastPT25-S2,IC,SPX,live-candidate,post-fix,T00002,SPX,shortputspread,closed,10,0.35,2.3,-1950,4650,2026-07-02 11:01:00,2026-07-02 13:02:00,2026-07-02 16:00:00,put side,False,7445,7440,,,-350,7502.99,7442.66,0,-5.57142857,2026-07-02 11:01:00,2026-07-02 13:02:00
```

⛔ **The fixture must load BOTH legs of `T00002`.** The sibling is the `shortcallspread`:
`risk 4850 · pnl +100 · credit 0.15 · quantity 10 · mae_pct 0`. Loading only the put leg is how the
flattered denominator gets back in — see D-15 (§2.5).

| id | assertion | value | catches |
|---|---|---|---|
| F3-a | leg `credit_$` (put) | `0.35 × 100 × 10 = ` **350.00** | D-6 |
| F3-b | `CONTROL cf_$` (put) | **−1,950.00 ± $0.01**, `CONTROL_OK` | **D-7 · the only CONTROL assertion on a LOSER — this line alone kills the `abs(pnl)` mutation** |
| F3-c | `risk_pos_$` | **4,850.00** — `MAX(4,650 , 4,850)`, **not** 4,650 and **not** 9,500 | R-6, `CLAUDE.md` §4 |
| F3-d | `pnl_pos_$` | **−1,850.00** (`−1,950 + 100`) | R-6 |
| F3-e | `credit_pos_$` | **500.00** (`350 + 150`) | R-6 |
| F3-f | `SL150` leg `cf_$` / `delta_$` | **−525.00 / +1,425.00** | D-6 |
| F3-g | `SL150` position `delta_R` | **+0.293814** (`1,425 / 4,850`) — **NOT +0.306452** | **D-15** |
| F3-h | `SL100` position `delta_R` | **+0.329897** (`1,600 / 4,850`) | D-15 |
| F3-i | `DSTOP` with `D_$` injected as **$350.00** | **FILLED**, `cf_$ = ` **−350.00**, leg `delta_$ = ` **+1,600.00** | **the real-row `dstop` check the old fixture never had** |
| F3-j | the same `DSTOP` under the D-6 bug | **SILENT** — `MAE_$` computes as **−1.95** instead of **−1,950.00**, and −1.95 > −350 | D-6, the family whose *verdict* depends on units |

⛔ **F3-i injects the threshold; it does not derive it.** The signed rungs are `DSTOP_100`/`DSTOP_150`
at 1.00×/1.50× the bot's trailing-90-day **median credit in dollars** (R-1), and the leg-vs-position
basis for that median is **unsigned** (§10 OPEN-2). Measured for `IC-SPX-FastPT25-S2` `[LEDGER]`:
leg-median **$300.00** (n=364 legs) vs position-median **$500.00** (n=221 positions). The fixture
therefore asserts the *arithmetic* against an injected threshold and asserts the *derivation
function* separately, under whichever basis Andy signs. **A green fixture must not certify an
unsigned choice.**

### F-4 — line 114 · `T00083` (both legs) · the stop that HURTS, and the COND negative

```
IC-SPX-Fortress-Defang,IC,SPX,experiment,baseline,T00083,SPX,shortcallspread,closed,10,0.1,0.05,50,4900,2026-06-25 13:31:03,2026-06-25 15:26:03,2026-06-25 16:00:00,call side,False,,,7420,7425,-100,7362.41,7354.6,1,-2.7,2026-06-25 13:50:00,2026-06-25 14:30:00
```

Sibling leg: `shortputspread · risk 4800 · pnl +100 · credit 0.2 · quantity 10 · mae_pct −1.65`.

| id | assertion | value | catches |
|---|---|---|---|
| F4-a | `CONTROL cf_$` | **+50.00**, `CONTROL_OK` | D-7 |
| F4-b | `SL200` leg `cf_$` / `delta_$` | **−200.00 / −250.00** — the stop **hurts** a recovered loser | D-6, §1a's "one loser in four recovers" |
| F4-c | `risk_pos_$` | **4,900.00** = `MAX(4,800 , 4,900)` | R-6 |
| F4-d | `SL200` position `delta_R` | **−0.0510204** — ⚠️ equal to the leg value **by coincidence**, because the only firing leg happens to be the larger-risk side. Assert F4-c explicitly or this row silently tolerates the D-15 bug | D-15 |
| F4-e | `SL150` position `delta_$` / `delta_R` | **−600.00 / −0.1224490** — **both** legs fire here, so this is the genuine two-leg aggregation test | **D-15** |
| F4-f | `COND_200_1400` | **NEVER_REACHED** — mae −2.7 ≤ −2.0 **but** trough 14:30 is **not** before 14:00 | COND conjunct |

### F-5 — line 21 · `T00012` · the debit-structure `CONTROL` branch

```
DIR-SPX-CallVIXdrop,Directional,SPX,experiment,post-fix,T00012,SPX,longcallspread,closed,1,6.9,2.9,-400,690,2026-07-02 11:00:03,2026-07-02 11:08:01,2026-07-02 16:00:00,,False,,,7520,7505,690,7504.33,7470.23,0.03623188,-0.58405797,2026-07-02 11:00:03,2026-07-02 11:08:00
```

Note `premium` is **positive** (`+690`) here, as `oa-export-schema.md` §2 requires for a debit
structure, and `abs(premium) == credit_$ == risk_$ == 690.00`.

| id | assertion | value | catches |
|---|---|---|---|
| F5-a | `CONTROL cf_$` | `(2.9 − 6.9) × 100 × 1 = ` **−400.00**, `CONTROL_OK` | the debit sign class |
| F5-b | the credit identity applied here | would yield **+400.00** -> `CONTROL_MISMATCH` | the false-alarm that breaks E-1 |
| F5-c | `risk_$` | **690.00** `== credit_$` (`6.9 × 100 × 1`) | D-16 — the R basis collapses to the credit basis |
| F5-d | `SL100` / `SL150` / `SL200` verdict | **`N/A — structure`**, never `NEVER_REACHED` | D-16 — `min(mae_pct)` over all 13 debit rows is **−0.804**, floor −1.0, so these fire **0 of 13** by construction |

### N-1 … N-4 — negative controls (§3.4)

| id | mutation of F-1 | required result |
|---|---|---|
| N-1 | `pnl` -> `"9999"` | `CONTROL_MISMATCH`, `run()` exits non-zero |
| N-2 | `exit_price` -> `"99"` | `CONTROL_MISMATCH` — corrupts an **input to the recompute** |
| N-3 | `quantity` -> `"100"` | `CONTROL_MISMATCH` — the only check on `× quantity` **inside** `CONTROL` |
| N-4 | `structure` -> `"calendar"` | **REFUSED**, counted, no verdict emitted |

### E-1 … E-4 — end-to-end and boundary

| id | check | required result |
|---|---|---|
| E-1 | `run()` over a temp ledger of **30 verbatim consecutive real rows** that includes ≥1 debit structure, ≥1 loser, ≥1 `quantity > 1` | completes, 0 `CONTROL_MISMATCH`, writes both `counterfactuals.csv` and `research_log.md` |
| E-2 | **29** closed positions (`trade_id` groups) | prints the suppressed line, emits nothing |
| E-3 | **30** closed positions | emits |
| E-4 | **29** closed + **5** expired positions | prints the **suppressed** line — not 34 |

⛔ **E-2/E-3/E-4 all fail against today's code**, which counts *rows* and includes `expired`
(line 169: `            if (r.get("status") or "").lower() in ("closed", "expired")]`). That is the
point of specifying them. `[LEDGER]` illustrates the gap: **1,380 rows** with status in
(closed, expired) against **819 all-closed positions**, 112 all-expired, 3 mixed.

### V-0 — the variant-list assertion

⛔ **The code's variant list is not the signed one.** Read directly this session,
`scripts/research_loop.py` lines 42–56 declares:
`CONTROL · PT40 · PT60 · PT70 · SL150 · SL200 · SL250 · DSTOP_50R · DSTOP_75R · TIME_1545 ·
TIME_1555 · COND_MAE_1400`.
The signed §3 set is:
`CONTROL · PT40 · PT60 · PT70 · SL100 · SL150 · SL200 · DSTOP_100 · DSTOP_150 · COND_100_1300 ·
COND_100_1400 · COND_200_1400`.
**Five signed variants do not exist in the code** (`SL100`, `DSTOP_100`, `DSTOP_150`,
`COND_100_1300`, `COND_100_1400`) and **six retired ones are still in it** (`SL250`, `DSTOP_50R`,
`DSTOP_75R`, `TIME_1545`, `TIME_1555`, `COND_MAE_1400`). Line 57's
`assert len(VARIANTS) == 12, "the signed count is 12 including CONTROL"` passes on the **wrong**
twelve.

**V-0:** assert `[name for name, _, _, _ in VARIANTS]` equals the signed twelve **verbatim and in
order**. One line; it catches the drift the count assert is blind to.

---

## 6. Build order and acceptance

Ordered so that each step's fixture can run before the next is written. Steps 1–3 are the fatal
three; 4–7 are the material defects the same rewrite has to carry, because they share the same code
paths and re-touching them later re-opens the freeze.

| # | Step | Acceptance |
|---|---|---|
| 1 | **`CONTROL`** — recompute from `(credit − exit_price) × MULT × quantity`, both sign classes, `$0.01` tolerance, abort non-zero on mismatch | F3-b, F4-a, F5-a/b, N-1…N-4 green; 0 mismatches on `[LEDGER]` n=1,380 and `[EXPORT]` n=1,386; worst residual printed and `< $1e-9` |
| 2 | **Units (D-6)** — `credit_$ = credit × MULT × quantity`, `MFE_$`/`MAE_$` from it, `MULT` derived and asserted, all four counterfactual families | F1-b…F1-i, F2-a…F2-c, F2b-a…F2b-g, F3-a/f/i/j, F4-b green; §2.8 (a)–(e) all hold |
| 3 | **Position unit (D-15)** — one output row per (position, variant); `risk_pos_$ = MAX`; `delta_R` position-only; PT `UNDECIDABLE` on multi-row groups | F3-c…F3-h, F4-c…F4-e, F2-d green; output row count == positions × 12, **not** legs × 12 |
| 4 | **Censoring surface (D-8)** — `censored ∈ {FALSE, TRUE, UNKNOWN}`, `CENSORED`/`BLOCKED` verdicts, header block, `research_log.md` | §4.5: every PT/SL cell `BLOCKED` today; **0** cells with a numeric `delta`; the `SKIP` line prints |
| 5 | **Clamp + structure classes (D-16)** · **bracketing stratum (D-17)** · **refuse at the group (G-4)** · **same-day filter (D-12)** | clamp counts 16/48/52 at SL100/150/200 `[LEDGER]`; `BRACKET_VIOLATION` stratum = **291** rows; 126 multi-day groups excluded; F5-c/d green |
| 6 | **Order-conflict + trough-vs-breach (D-11, D-10)** — read `mfe_date`, downgrade conflicting PT cells | F1-j green; conflict count printed |
| 7 | **`execution_audit.py` pattern** — `ROOT` anchoring, version banner in `run()`, `_meta.json` receipt, `self_hash()` computed **once** (today it is recomputed per output record: **15,048 file reads per run** at capture scale), append-not-clobber (D-13), variant list V-0, drop the ranked top-4 leaderboard (D-9) | V-0 green; `counterfactuals.csv` no longer truncated per run; no descending-sorted podium in the nightly line |

⛔ **`FROZEN_ON = None` stays `None` until every acceptance box above is green and Andy signs.**
Freezing is a signature, not a code change.

---

## 7. Wiring checklist — for when Andy wires it into `daily.sh`

**Not now.** `research-loop-spec.md` §6.5 and §5a both carry the standing order: *"It is not wired
into `daily.sh` and must not be."* This is the checklist for the day that changes. Every box is a
precondition; **none of them is a tool's success message** (`CLAUDE.md` §9.1a).

**Gate A — the fixes pass their own fixtures**

- [ ] `python3 scripts/research_loop.py --validate` exits 0 with **every** check in §5 green:
      F-1 (10) · F-2 (4) · F-2b (7) · F-3 (10) · F-4 (6) · F-5 (4) · N-1…N-4 · E-1…E-4 · V-0.
- [ ] The `SKIP  D-8 CENSORING: NOT COVERED` line is **present in the output**. A fixture that
      does not print it is reporting coverage it does not have.
- [ ] The count of **verdict-string-only** assertions is stated in the fixture's own summary and is
      **under 15%** of checks. The old fixture was 21 of 23 (91%); the set above is 2 of 20 (10%).
- [ ] The mutation table of §9(b) is re-run against the finished code and **every** mutation is
      CAUGHT, with the failing check ids printed.

**Gate B — a fresh 23-check run over the frozen capture**

- [ ] Read-only pass over `data/captures/oa_export_positions_2026-07-30.csv`, **explicitly labelled
      `v1 pre-cutover · demonstration only · not a reporting input`** in its own output header
      (`CLAUDE.md` §3). Its numbers may not enter `STATUS.md`, the brief, or any instruction card.
- [ ] All of §2.8 (a)–(e) hold: `dstop` regression counts **42 / 26** of 1,254 on the rejected risk
      rungs; signed `DSTOP_100` within ~3 points of `SL100`; no `|mean ΔR| ≥ 0.10R`; row-wise bounds
      hold; clamp counts printed.
- [ ] `CONTROL_MISMATCH` count **0**; worst residual printed and `< $1e-9`.
- [ ] Output row count equals **positions × 12**, and the printed `n` carries the word **positions**
      (`CLAUDE.md` §4: never a bare count).

**Gate C — the spec's own preconditions, none of which is code**

- [ ] `data/bots_config_v2.csv` carries a **per-bot** row with the incumbent exit for every bot under
      test, or the censoring surface reports `BLOCKED` and the brief says so out loud. Today it holds
      **one scaffolding row** with `input_default = NOT SET — see FINDING F-4`.
- [ ] §10's start condition is measured on the right population: **n ≥ 30 post-cutover CLOSED
      POSITIONS fleet-wide**, `trade_id` groups, `expired` excluded (R-4/R-6/R-7).
- [ ] §5's per-pair gate `n ≥ 100` is understood as a **different population** from §10's fleet-wide
      30 (`research-loop-spec.md` §5, 2026-08-05 applied note: *"Do not conflate them."*).
- [ ] The **regime-change conjunct is still undefined in every document** (`build-plan.md` §5,
      `greenfield-family-spec.md` §12-12, `track-b-arms-spec.md` §11-6). ⛔ **The §5 gate cannot fire
      until it is written and signed** — wiring the generator is fine; the gate is not reachable.
- [ ] Every §10 OPEN item below is ruled, or the affected variant is emitted as `SKIPPED`.

**Gate D — the wiring itself**

- [ ] Inserted as **stage 9 of 9** in `scripts/daily.sh`, **after** `report.py` — Track A is
      advisory-only (§10 bullet 4) and must never be an input to `STATUS.md` or the three verdicts.
      Update the `== N/8 ==` banners to `/9` and the header comment block (it says "eight stages" at
      line 4).
- [ ] `set -euo pipefail` is active, so **stage 9 must exit 0 on an empty ledger**. Verify the n=0
      path by running `scripts/daily.sh` against the current header-only `data/trades.csv` and
      confirming the whole pipeline still completes.
- [ ] The `pre-Day-0` branch is fixed: `build_ledger.py` **always** writes `data/trades.csv`, even at
      n=0, so `if not os.path.exists(ledger)` never means pre-Day-0 — it means the working directory
      is wrong. Today that prints a cheerful false green.
- [ ] `os.makedirs(os.path.dirname(out), exist_ok=True)` raises on a bare filename. Guard it.
- [ ] One line to the brief, `NO CANDIDATES` as the expected nightly output (§2), **no leaderboard**.
- [ ] Andy runs the commit. Claude does not (`CLAUDE.md` §9.1).

---

## 8. ⛔ G-10's max-T constraints bind ANY shared statistical machinery

**This applies to `research_loop.py` too, and it is easy to miss because G-10 was ruled about the
greenfield family.** §10a item 3 already specifies Track A's gate as *"a stratified paired sign-flip
permutation test … with max-T across all variants and bots … so no Bonferroni term is applied."*
That is the same family object G-10 switched the comparative machinery to
(`g-rulings-card-2026-08-07.md` B4: **SWITCH — joint day-bootstrap max-T across arms, declared before
any data exists**, ruled Andy 2026-08-06). Two constraints measured in
`post-u1-package-2026-08-07.md` §2 therefore bind Track A's implementation as well:

**CONSTRAINT A — no bootstrap-t studentization unless the realised `c` is demonstrated ≤ 2.638.**
On a ≈90%-degenerate, ≈10%-at-±0.9 leptokurtic `d`, a studentized max-T critical value was measured
at **`c` = 2.92** (within-day dispersion 0.05) and **4.69** (0.02), against Bonferroni K=6 two-sided
= **2.638** — the value G-10 was ruled in order to improve on. The implementation must either
**(i)** avoid bootstrap-t studentization for the family region, or **(ii)** demonstrate on real data,
and **publish the number**, that its realised `c` does not exceed 2.638. *"A max-T implementation
whose `c` exceeds 2.638 has not implemented G-10; it has silently reversed it while carrying G-10's
name."* **`c` is a mandatory published field on every verdict object.**

⚠️ Track A's ΔR vector is **more** zero-inflated than the family's `d`, not less: `[LEDGER]`,
`DSTOP_100` fires on 24.6% of rows and `SL200` on 13.9%, so 75–86% of the vector is exact zeros. If
studentization inflates `c` on a 90%-degenerate vector, it will inflate it here too. Measure it
before adopting it.

**CONSTRAINT B — the family region needs a per-member direction vector, declared before any data
exists.** Track A's members do not all point the same way: the variant-beats-control tests are
**LOWER**-bound (`ci_fam_lo > 0`), while any equivalence or no-harm member is two-sided or upper.
*"A signed max over statistics whose pivots enter with opposite signs is not the right object, and
one `c` cannot simultaneously calibrate a one-sided upper region, a one-sided lower region, and a
two-sided equivalence band."* The object must be either **(a)** an explicitly **signed** simultaneous
region with each member's direction declared in advance, or **(b)** two-sided using `max_j |T_j*|`.

⚠️ **And it must be declared BEFORE any data exists — which is still true today**
(`data/ledger_meta.json`: `"export_rows": 0`). A direction vector chosen after the data exist is a
post-hoc analysis change.

**Two more, already signed, that a shared implementation must not lose:**
- §10a item 2 — **no nightly gate evaluation.** The gate is evaluated **once**, at a date written
  into `pre-registration-ledger.md` **before** n reaches 100. Nightly output is descriptive only.
- **G-8** (ruled Andy 2026-08-06, SEQUENCE+CS) — an interim `n ≥ 60` read is emitted as an
  **always-valid confidence sequence**, and an absolute kill cannot retire an arm before its stamped
  gate-eval date. §10a item 4 says the same thing for Track A: nightly monitoring uses a confidence
  sequence, **never a fixed-n CI**.
- **G-11** (ruled Andy 2026-08-06, IN) — PR-21/PR-22 are inside the greenfield family for error-rate
  purposes. And §10a's 2026-08-06 scoped retirement excludes dual-tested (bot, variant) pairs from
  Track A's family: at this signature `SL100`, `SL200` and `DSTOP_100` on the seven greenfield
  ledgers and on ARM-B1. **The engine must implement that exclusion**, or Track A will test whether
  an arm differs from itself — the tautological-`CONTROL` defect class, in a new place.

⚠️ **No pooled alpha exists across the two engines**, and this spec does not create one. Within-family
multiplicity for the greenfield arms stays with Phase C step C4's Bonferroni-across-6; Track A's stays
with §10a's max-T. Carried limitation, not a solved one.

---

## 9. Adversarial record

Two subagents were spawned against the draft with instructions to **refute**, defaulting to "this is
wrong." **Both succeeded.** Reviewer **U** attacked the corrected units formula against the export
schema and the ledger; reviewer **X** attacked the fixtures by mutation-testing a correct engine.
Between them: **8 FATAL and 17 MATERIAL** objections. The text above is the post-review text.

⛔ **Every figure below was recomputed independently by me this session before being recorded.** Two
reviewer figures did not survive that check and are corrected in place, with a note.

### (a) Surviving objections — INCORPORATED above

| id | sev | objection | where it landed |
|---|---|---|---|
| **U-1** | FATAL | The formula omits `CENSORED` entirely, so a units fix converts a wrong non-zero into a **correct-looking zero** that now survives `CONTROL` and enters the §10a vector as a genuine observation. | §4.2 — three-state flag, `BLOCKED` as today's default |
| **U-2 / X-1** | FATAL | `delta_R` is per leg; the §10 margin is per position. On `T00002` the per-leg number is **+0.306452** and the position's is **+0.293814** — 4.3% flattered, and it doubles `n` (1,380 legs vs 934 positions). **My draft asserted the flattered number.** | **D-15, §2.5**; fixture F3-c/F3-g |
| **U-3** | FATAL | `DSTOP`'s threshold is a **position**-level median compared against a **leg**-level `MAE_$` — mixed units. Fire rates: 266 vs 340 at `DSTOP_100`, 216 vs 249 at `DSTOP_150` (`[LEDGER]`, 27.8% relative swing at DSTOP_100) | §2.8(b), §10 OPEN-2, fixture F3-i note |
| **U-4** | FATAL | The `abs(premium)` second-witness guard refuses **0 of 1,380** and cannot vary; meanwhile the invariant the counterfactual actually rests on — MFE/MAE bracketing the realised outcome — **fails on 291 of 1,380 (21.1%)** and was unchecked | **D-17, §2.7**; guards G-1 (demoted to a sanity assert) and G-3 |
| **U-5 / X-2** | MATERIAL→FATAL | `CONTROL` does **not** catch the D-6 class: the branches share no operand. Drop `× MULT × quantity` from the PT branch only and `CONTROL_OK` is still 1,380/1,380. The review's §7 step 2 is wrong on this. | §3.3 |
| **U-6** | MATERIAL | Debit structures: `risk_$ == credit_$` on **13/13**, so `delta_R` silently becomes the credit basis; `min(mae_pct) = −0.804` with a −1.0 floor, so SL fires **0 of 13** by construction; and `cf_$` is unclamped | **D-16, §2.6**; fixture F-5 |
| **X-3** | FATAL | No `CONTROL` assertion sits on a **loser**, so the `abs(pnl)` mutation (M5) survives every row assertion **and** the corrupt-`pnl` negative control | fixture F3-b, N-2, N-3 |
| **X-4** | FATAL | The debit rows sit at ledger **lines 20–21**, so a "first 30 rows" end-to-end harness makes a **correct** engine exit 1 — and the obvious fix re-kills D-7 | §3.2 note, fixture F-5, E-1 |
| **U-7 / X-9** | MATERIAL | `COND` uses trough time as breach time (D-10) and compares clock times across calendar days on the **126 multi-day groups**; the export's timezone is an open pre-switch-on check (`comparative-machinery-spec.md` §1.4, D3) | §4.4, guard G-5 |
| **U-8** | MATERIAL | "Refuse the row" corrupts position aggregation on the 446 two-leg groups | guard G-4 |
| **U-9** | MATERIAL | `risk` is in every denominator with no real second witness — and the re-derivation specified in `comparative-machinery-spec.md` §1.3 **omits the `− credit_$` term and has no debit form**, so as written it refuses **1,380 of 1,380** | guard G-2, §10 OPEN-5 |
| **U-10** | MATERIAL | The PT family is `UNDECIDABLE` on **446 of 934 groups (47.8%)**, and the decidable remainder is a **selected** subpopulation: median R **+0.02073** (n=488) vs **+0.00376** (n=446) — a gap of **+0.01696R**, **larger than §10's entire pre-declared margin of +0.015R**. 72.1% of the decidable set is `single_sided`. Feasibility: **no bot reaches n=100 PT-decidable positions** on the whole capture; the max is **78** (`IC-SPX-FastPT25-S2`) | §10 OPEN-3 — this is a decision, not a formula |
| **U-11** | MATERIAL | `M_bot_$` takes a position on a question `research-loop-spec.md` §5a item 1 marks *"Open, one word from Andy"* (rolling vs one-time), does not say **as of when** (whole-ledger median is look-ahead), and is undefined for early positions because §10 starts the engine at n≥30 fleet-wide, long before 90 days exist | §10 OPEN-2 |
| **U-12** | MATERIAL | `dstop` dispersion within a bot is driven by **quantity**, not credit: `QQQ-IC-0DTE-Baseline` spans **$101 → $9,600 (95.0×)** on quantity 54→192; `IC-SPX-FastPT25-S2` spans 13.8×. At a 95× spread a single dollar `dstop` is a **position-size filter wearing a stop's name** | §10 OPEN-2, §2.8(c) |
| **X-5** | MATERIAL | F1-d/F1-e have **zero branch-discriminating power** — the `NEVER_REACHED` branch emits `(cf_$ = pnl, delta_$ = 0)` and this row's `pnl` is 35, the same number F1-d asserts | fixture F1-c, F1-f, F1-g added |
| **X-6** | MATERIAL | No fixture can catch D-8; the fixture must therefore **assert the absence of coverage** | §4.2 items 5–6 |
| **X-7** | MATERIAL | F3's injected `$350` threshold bypasses the only part of `DSTOP` that is signed, and is not even the measured median (`IC-SPX-FastPT25-S2` leg-median is **$300.00**) | fixture F3-i note |
| **X-8** | MATERIAL | Five signed variants are missing from the code and six retired ones are still in it; `assert len(VARIANTS) == 12` passes on the wrong twelve | fixture V-0 |
| **X-10** | MATERIAL | F-1 is a **3DTE multi-day OA-Mirror** row being used to validate a 0DTE Track-A engine | fixture F1-a; F-2b added as the same-day large-quantity witness |
| **X-11** | MATERIAL | E-1 as drafted tests only that `run()` executes — none of R-4/R-6/R-7 | E-2, E-3, E-4 |
| **U-13** | MINOR | `MULT = 100` is asserted where it can be derived for free; the relative limb of the CONTROL tolerance is dead code (`max |pnl| = 9,975`, so it maxes at $9.98×10⁻⁶) | §2.2, §3.2 |
| **U-14** | MINOR | `mae_pct ≤ 0` is false on **89 of 1,380**; `mfe_pct ≥ 0` false on **30**; the structure enumeration has no `else`; **3 groups have mixed status** and **128 of 446 have mixed quantity** between legs | guards G-6, G-7; N-4 |
| **X-12** | MINOR | Verbatim-ness: transcription drift between fixture and archive is silent | §5 preamble — sha256 per raw line |

### (b) The mutation table — reviewer X, re-derived

A correct `evaluate()` and each mutation were implemented and **run**, not reasoned about. Detection
channels: fixture value assertions · N-1…N-4 · E-1.

| mutation | assertions that fail | verdict |
|---|---|---|
| M1 drop `× quantity` (variant line only) | F3-f, F3-g, F3-h, F4-b, F4-d, F4-e | CAUGHT |
| M1 drop `× quantity` (shared helper) | + F2-a, F2-c, F2b-a, F3-a, F3-i | CAUGHT |
| M2 drop `× MULT` | F1-d…F1-h, F3-f…F3-i, F4-b…F4-e (9–17 depending on scope) | CAUGHT |
| M3 the original D-6 bug | same as M2, plus F3-j | CAUGHT |
| **M4 `CONTROL = abs(pnl − pnl)`** | **none** | **CAUGHT BY N-1…N-3 ONLY — survives all four real rows** |
| **M5 `CONTROL` vs `abs(pnl)`** | **none**, and it **passes N-1** | **CAUGHT ONLY BY F3-b** (the loser row) |
| M6 `delta = pnl − cf` | F1-e, F1-f, F1-g, F2b-e, F3-f…F3-h, F4-b, F4-e | CAUGHT |
| M7 `delta_R ÷ credit_$` | F2b-f, F3-g, F3-h, F4-d, F4-e | CAUGHT |
| M8 `risk = SUM` over the group | F3-c, F3-g, F3-h, F4-c…F4-e | CAUGHT |
| M9 `MULT = 1000` | 15+ across all rows; E-1 aborts | CAUGHT |
| M10 `mae >=` instead of `<=` | F1-i, F3-f…F3-h, F4-b, F4-d…F4-f | CAUGHT |
| M11 PT comparison inverted | F1-c, F1-f, F1-g, F2b-c, F2b-g | CAUGHT |
| M12 `DSTOP` on `mae_pct` not `MAE_$` | F3-i, F3-j | CAUGHT |
| M13 emit per leg instead of per position | F3-g, F3-h, F4-e; output row count ≠ positions × 12 | CAUGHT |

**D-6 is dead: every units mutation dies on ≥5 assertions.** **D-7 is alive on the rows alone** —
M4 and M5 fail zero of them — and is killed only by F3-b plus N-1…N-3. That asymmetry is the single
most important result of the adversarial pass and is why §3.4 specifies four checks, not one.

### (c) Objections raised and NOT sustained

- **"`credit` may not be `openPrice`; `exit_price` may not be `closePrice`."** Sustained as a
  question, refuted as a defect: `build_ledger.py` writes `r["openPrice"]` and `r["closePrice"]` into
  the `credit` and `exit_price` columns, and `mfe_pct`/`mae_pct` from `highReturnPct`/`lowReturnPct`.
  Read from the code, not from prose.
- **"`risk` needs its own `× quantity` term."** **False**, and it was my highest-prior worry. On the
  1,103 credit rows with quantity > 1, `risk == width × 100 × quantity − credit_$` matches
  **1,103/1,103** and the per-contract form matches **0/1,103**. `risk` already carries quantity, so
  `delta_R` is dimensionally sound. What the check *did* find is that `risk` is **net of credit** and
  that the debit form differs — objections U-6 and U-9.
- **"`MULT = 100` is unsafe across symbols."** Derived per row: exactly **100.000000 on 1,386/1,386**,
  identical for SPY (75 rows), SPX (586), QQQ (725). Safe for this file; still asserted, not assumed.
- **"`MFE_$ = mfe_pct × credit_$` is the wrong basis for `ironbutterfly` or for debit structures."**
  Refuted: `returnPct == pnl / abs(premium)` holds to 5.04×10⁻⁷ on n=1,386; butterflies 25/25 exact;
  the debit sign convention is identical (favourable is positive). The **basis** survives; only the
  downstream **semantics** break, which is U-6.
- **"The `$0.01` CONTROL tolerance is wrong."** Refuted both ways: no false `CONTROL_MISMATCH` and no
  false `CONTROL_OK` at $0.01; tightening to $1e-6 still gives 0 mismatches; loosening masks nothing.
- **"`PT70 delta == 0.00 exactly` is a float-equality trap."** Refuted: bit-identical `35.0` in five
  association orders. The objection to F1-e is degeneracy (X-5), not floating point.
- **"The premium guard is code-circular."** Refuted: `build_ledger.py` writes `credit` and `premium`
  from two different export columns and derives neither from the other. It reduces to "same vendor,
  not independent" — which is U-4, and is why G-1 is demoted to a sanity assert.

### (d) ⚠️ Two reviewer figures that did NOT survive my recheck, corrected

- Reviewer U reported `IC-SPX-FastPT25-S2` within-bot dollar-credit spread as **25.2×** over n=221
  and `QQQ-IC-0DTE-Baseline` as 95.0× over n=43. Recomputed `[LEDGER]`: `IC-SPX-FastPT25-S2` is
  **13.8×** ($100 → $1,375, n=364 legs, quantity 10–12); `QQQ-IC-0DTE-Baseline` is **95.0×**
  ($101 → $9,600, n=43, quantity 54–192). U's second figure stands; the first does not, and the
  version above is mine. The objection (U-12) survives on the second figure alone.
- Reviewer X gave `T00012` as *"credit 4.0, exit_price 0.0, pnl −400."* The actual line 21 is
  **credit 6.9, exit_price 2.9, pnl −400, risk 690**. The row is right; the values were wrong. §5 F-5
  carries the verbatim line.

---

## 10. ⛔ OPEN — GATED. Decisions the build must not make for itself

Each of these changes what gets built, so under `CLAUDE.md` §5 it needs an explicit **"amend the
plan"** from Andy. **Where an item is unruled, the affected variant is emitted `SKIPPED`, never
`PASS` and never a number** (`execution_audit.py` precedent, `daily.sh` stage 3).

| # | Open question | Why it is gated | Consequence of leaving it |
|---|---|---|---|
| **OPEN-1** | `M_bot_$`: **rolling** or **one-time** calibration? | Already flagged `research-loop-spec.md` §5a item 1 (*"Open, one word from Andy"*); rolling makes every re-stamp a new pre-registration under §10a | `DSTOP_100`/`DSTOP_150` emit `SKIPPED` |
| **OPEN-2** | `M_bot_$`: median over **positions** or over **legs**? And **as of when** (a whole-ledger median is look-ahead), and what happens before 90 days of history exist? | Changes `DSTOP_100`'s fire rate by **27.8% relative** (`[LEDGER]`: 266 vs 340). The signed §3 text says only *"the bot's trailing-90-day MEDIAN credit, in dollars"* | as OPEN-1 |
| **OPEN-3** | Is the PT family reported at all, given it is `UNDECIDABLE` on **47.8%** of positions and the decidable remainder's median R differs by **+0.01696R** — more than the whole §10 margin? And **no bot reaches n=100 PT-decidable positions** on the v1 capture (max 78) | R-6 ruled the unit and named the cost (*"a real reduction in scope"*) but not this selection effect, which was not measured at the time | PT lines print the decidable/undecidable split and the `single_sided` share on every line, or the family is retired to Track B |
| **OPEN-4** | Mixed-status groups (**3** on `[LEDGER]`) and mixed-quantity groups (**128 of 446**) — which stratum, which quantity? | R-7 stratifies `expired` at the row and is silent on a group with one leg of each | those groups are REFUSED and counted |
| **OPEN-5** | `comparative-machinery-spec.md` §1.3 guard 1's risk re-derivation **omits `− credit_$` and has no debit form**, so as written it refuses **1,380 of 1,380** | That is a build specification and the correction is a decision about what gets built, not an evidence-backed correction of a falsified claim within this session's authority | recorded here; **that file is untouched** |
| **OPEN-6** | The **regime-change conjunct** is undefined in every document | `research-loop-spec.md` §5's own applied note: *"The gate cannot fire until it is written and signed"* | the §5 gate is unreachable; the generator may still run |
| **OPEN-7** | G-10's **per-member direction vector** for Track A's max-T region (§8 Constraint B), which must be declared **before any data exists** — still true today | A direction vector chosen after Day-0 is a post-hoc analysis change | §10a item 3's test is not implementable |

### 📝 RULED 2026-08-07 (Andy) — OPEN-1, OPEN-2, OPEN-3 signed; OPEN-4 through OPEN-7 remain gated

**OPEN-1 + OPEN-2 — `M_bot_$` calibration, RULED.** ONE-TIME calibration (not rolling — answers
`research-loop-spec.md` §5a item 1's "one word from Andy," recorded there with its own dated
banner). Median over **POSITIONS**, not legs. Computed **at the stamp date**, over the **trailing
90 days as of that date** (not a whole-ledger, look-ahead median). **SKIPPED, never a fabricated
value, for any bot with fewer than 90 days of history** at the stamp date — the engine emits
`SKIPPED`, not a proxy computed from a shorter window. `DSTOP_100`/`DSTOP_150` may emit `PASS`/
`FAIL` once `M_bot_$` is implemented to this spec **and** the engine's three fatal defects (§9
above) are fixed — `research_loop.py` is still `0.1.0-DRAFT` and still not wired into `daily.sh`.

**OPEN-3 — PT family, RULED.** REPORTED, WITH A MANDATORY SPLIT: every PT line prints the
**decidable / undecidable position counts** and the **`single_sided` share**, on every line, no
exceptions. The report is **descriptive only** — no graduation read, no kill/pass verdict, is
taken from a Track A PT line while this ruling stands. The **live test of the PT mechanic is the
greenfield PT50 arm** (`greenfield-family-spec.md` §9, PR-15), which is exempt from the
47.8%-undecidable / +0.01696R selection-effect problem OPEN-3 measured, because it is judged on
its own matched-day family under G-10, not against the v1-style PT bucket.

**OPEN-4 through OPEN-7 are UNCHANGED — still GATED, still unruled.** Nothing above touches them.

---

## 11. Verification record

- **Every code and document quotation in this file was asserted byte-exact and single-match** against
  its source by substring count on the device: `research_loop.py` lines 91–94, 106–109, 115, 124,
  133–134, 154, 169, 271, and the docstring at 18–20; the four fixture rows at
  `data/archive/trades.csv` lines **19, 21, 48, 114, 791** (`grep -Fxc` = 1 each).
- **Every empirical figure was recomputed by me this session, read-only**, from
  `data/archive/trades.csv` (n=1,380) or `data/captures/oa_export_positions_2026-07-30.csv`
  (n=1,386), never taken from a reviewer. Where a reviewer figure disagreed, §9(d) records the
  disagreement and the version printed is mine.
- **The review's own figures reproduce exactly** — 1,254 / 1,136 / 118; 0.06952 / 0.03627 / 0.15607;
  279 / 200 / 172; 749 / 461 / 299; 42 / 26; and §6.5's 81.2% / 10.7% / 0.0% censoring signature.
- **All capture- and archive-derived figures are v1 pre-cutover, demonstration only** (`CLAUDE.md`
  §3, `research-loop-spec.md` §1a). `data/trades.csv` holds **n=0**; `data/ledger_meta.json` carries
  the pre-Day-0 sentinel. An absent number is not a zero.
- **No file in the repo was modified by this session except this one.** `scripts/research_loop.py`,
  `scripts/daily.sh`, `docs/research-loop-spec.md`, `docs/research-loop-review-2026-08-04.md`,
  `docs/oa-export-schema.md` and `docs/comparative-machinery-spec.md` are **untouched**. No OA edit,
  no git operation, no `state.md` or `session-log.md` edit (concurrent sessions own those).
- This file's own sha256 is recorded in the session hand-off.

**Changed files for Andy's commit:** `docs/research-loop-fix-spec-2026-08-07.md` (new).
