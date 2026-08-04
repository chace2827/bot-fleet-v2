# Track B — first arms spec

*Written 2026-08-04. Designs the first **Track B** arms under `docs/research-loop-spec.md` §4
and §10: real paper bots, one differing input, pre-registered. Nothing here was built. No OA
surface was touched. `research-loop-spec.md`, `research_loop.py`, `greenfield-family-spec.md`
and `daily.sh` are **unmodified** by this session.*

> ### Date note, once
> The commissioning task states "Today is 2026-08-06". The device clock and the session
> environment both read **2026-08-04**. Every date stamped in this file is the verifiable one.
> `greenfield-family-spec.md` carries the identical note and the identical resolution.

> ### ✅ RULING GATE — CLEARED
> The task says: *if unruled, STOP.* `docs/research-loop-review-2026-08-04.md` §0 records
> **all seven rulings, signed 2026-08-04**: R-1 SIGN · R-2 SIGN · R-3 SIGN · R-4 SIGN · R-5 SIGN ·
> R-6 RULE position · R-7 SIGN. R-1 and R-2 are applied to `research-loop-spec.md` §3 as dated
> amendments and are legible there. **This spec proceeds.**
>
> The two rulings the task names as slot-determining both landed, and both landed *against* the
> shape the task anticipated:
> - **The "RISK-basis rung ruling" went the other way.** The task's phrasing anticipates a
>   RISK-basis rung. R-1 **REJECTED** the RISK basis — `0.50×risk` lands at ~720% of credit at
>   the fleet's median credit/risk of 0.070 (n=1,254), past the no-stop boundary. The signed rung
>   basis is **1.00× and 1.50× the bot's trailing-90-day MEDIAN CREDIT, in dollars**.
> - **`TIME_*` was not merely dropped — it was moved into this document's budget.** R-2 retires
>   both `TIME_*` slots from Track A and funds the question *"instead from the Track B allocation
>   in §10"*. §7 below answers the task's direct question about this.

---

## 0. What this document is, in five lines

Two first arms, both on the **loss side**, both matched to controls that already exist on paper
in `greenfield-family-spec.md`, both inside the signed §3 variant set or added to Track B by a
signed ruling.

The hard part of this task turned out not to be designing arms. It was **discovering that the
slots are already spent** — `greenfield-family-spec.md` §12 item 11 states that its seven bots
consume **7 of the 8** signed Track B slots. §3 below is therefore the load-bearing section, and
its answer is a ruling request, not a design.

---

## 1. The rulings, and exactly what each one does to the slot question

| Ruling | What it does to Track B |
|---|---|
| **R-1** | Puts `DSTOP_100` / `DSTOP_150` into the signed §3 set on a **credit-dollar** basis. `greenfield-family-spec.md` §3.1 and §12 item 9 explicitly **exclude** fixed-$ rungs from that family and assign them to Track B. ⇒ **a live, ruled, unfunded loss-side arm.** This is ARM-B1. |
| **R-2** | Removes both time slots from Track A **and names Track B as their funding source**, with the exact values: `Expiration` **0.015** and **0.005** against the **0.01** incumbent. ⇒ **a live, ruled, unfunded arm.** This is ARM-B2 — and §6.4 finds the `0.005` half **not buildable in this family**. |
| **R-3** | Lowers the graduation margin from `≥0.10R` to **mean ΔR ≥ +0.015R**, withdraws the median test, adds a bootstrap CI and a fired-subpopulation sign test. ⇒ **materially resolves `greenfield-family-spec.md` §12 item 10**, which is written against the superseded 0.10R and is now stale. See §11 item 3. |
| **R-4** | `n` is **closed POSITIONS**, `expired` excluded, and — in the signed-but-unapplied §5 companion line — **per (bot, variant) pair**. For an arm, the pair *is* the bot. ⇒ sets every SAMPLE TARGET below. |
| **R-5** | New §10a: family = the 9 computable variants × every bot under test; **gate evaluated ONCE at a pre-declared date**; permutation max-T, no Bonferroni term. ⇒ every entry below carries a **GATE EVALUATION DATE**, which the `pre-registration-ledger.md` §2 template does not have a field for. See §11 item 5. |
| **R-6** | Unit = the POSITION (`trade_id` group, risk = larger side), and **combined MFE for a paired condor is a Track B question**. ⇒ a *third* ruled Track B question. §8 finds it **not expressible as an arm of this family** and defers it with the reason. |
| **R-7** | `expired` stratified — excluded from counts and from the PT comparison, retained as a stratum. ⇒ affects Track A bookkeeping only; no arm consequence. |

**Net: the rulings created three new Track B obligations (R-1, R-2, R-6) at the same moment the
greenfield spec spent 7 of the 8 slots.** That is the whole tension in this document.

---

## 2. The candidate space — what survives the rules

The task's binding rule: *no arm may test a variant outside the signed §3 set unless Andy's
review ruling added it.*

**The signed §3 set (12, frozen):** `CONTROL` · `PT40` · `PT60` · `PT70` · `SL100` · `SL150` ·
`SL200` · `DSTOP_100` · `DSTOP_150` · `COND_100_1300` · `COND_100_1400` · `COND_200_1400`.
**Added to Track B by ruling:** time exits at `expdays` 0.015 / 0.005 (R-2); combined-MFE
condor questions (R-6).

Filtered in four passes:

| Candidate | Loss side? | In signed set / ruled? | Expressible? | Already covered? | Verdict |
|---|---|---|---|---|---|
| `SL100` | ✓ | ✓ §3 | ✓ `stoploss` | **YES** — `GF-QQQ-IC-SL100` | drop, duplicate |
| `SL200` | ✓ | ✓ §3 | ✓ `stoploss` | **YES** — `GF-QQQ-IC-SL200` | drop, duplicate |
| `SL150` | ✓ | ✓ §3 | ✓ `stoploss` | no | **drop — low information, §8.1** |
| `DSTOP_100` | ✓ | ✓ §3 (R-1 basis) | ✓ `dstop`, confirmed §6.1a | **no** — excluded by greenfield §3.1 | ⭐ **ARM-B1** |
| `DSTOP_150` | ✓ | ✓ §3 (R-1 basis) | ✓ `dstop` | no | **hold for wave 2, §8.2** |
| `COND_*` (trough-timing) | ✓ | ✓ §3 | ⛔ **NO** | — | **drop — §8.3, platform limit** |
| Time `expdays` 0.015 | ✓ (see §7) | ✓ ruled R-2 | ✓ enumerated first-hand | **no** — all 7 greenfield arms hold 0.01 | ⭐ **ARM-B2** |
| Time `expdays` 0.005 | ✓ | ✓ ruled R-2 | ⛔ **NO in this family** | — | **drop — §6.4, backstop preempts it** |
| Combined-MFE condor (R-6) | profit side | ✓ ruled R-6 | ⛔ not as an arm of this family | — | **defer — §8.4** |
| `PT40` / `PT60` / `PT70` | ✗ profit side | ✓ §3 | ✓ | partly (`GF-PT50`) | **defer — §4 says loss side first** |
| `Touch $0` | ✓ | ✗ **not in §3** | ✓ | **YES** — `GF-QQQ-IC-Touch0` | drop, duplicate |
| `SL50` / `SL75` | ✓ | ⛔ **not in §3** | ✓ | no | ⛔ **forbidden — §8.5, and this is a loss** |

**Two arms survive.** That is the count this document proposes, and §8 states the reason for
every rejection rather than leaving the reader to infer it.

---

## 3. ⭐ SLOT BUDGET ACCOUNTING — and the collision that needs a ruling

### 3.1 The disposition table, and the n for "used"

From `build-plan.md` §2, **confirmed against the 2026-07-30 capture, no remainder**:

> `**Accounting: 35 on the roster = 20 archived + 2 deleted + 4 cloned (originals archived) + 9 untouched.**`

Post-cutover **active** fleet, the number the task asks me to state:

| Group | n | Source |
|---|--:|---|
| B — clone-to-spec (originals archived) | 4 | `build-plan.md` §2B |
| C — untouched | 9 | `build-plan.md` §2C |
| D — fresh builds (greenfield family) | 7 | `greenfield-family-spec.md` §3, at §2D's ceiling |
| **n_used (active)** | **20** | |

⚠️ **n_used = 20 only if the greenfield count lands at 7.** `build-plan.md` §2D authorises
**5–7**, and `greenfield-family-spec.md` §12 item 3 records that its own reading of §2D
(4–6 IC bots *plus* hedge arms *plus* canary vs 5–7 total) is unresolved and Andy's. At §2D's
floor, n_used = **18**. Both figures are quoted below where they matter.

**Roster today is 36**, not 35 — `state.md` records the pilot clone as a 36th bot. The 20 Group-A
archivals have not run yet.

### 3.2 The 50-bot cap — and an unrecorded assumption inside it

`research-loop-spec.md` §4 and §10:

> `**Track B is strictly better evidence and you can afford it.** The Pro plan allows 50 bots; the`
> `- [x] **Track B may consume ≤ 8 bot slots**, leaving headroom under the 50-bot plan cap.`

⚠️ **Nothing in this repository records whether ARCHIVED bots count against the 50.** I searched
`docs/` and `CLAUDE.md`; the only cap statements are the two above and
`oa-mirror-reference.md`'s *"up to 50 bot slots"*. If archived bots **do** count, the live
arithmetic at Day-0 is 36 on the roster + 7 fresh = **43**, and the ≤8 Track B allocation
**does not fit** — 43 + 8 = 51. If they do not count, it is 20 + 8 = 28 and there is ample room.

**This is a one-screen read on the OA membership page and it has never been done.** It is
promoted to a blocking check (**C12**, §10) because it can invalidate the ≤8 allocation outright,
and because "we can afford it" is currently a **[FIRST-HAND, UNCORROBORATED]** inference from a
plan tier rather than an observed slot count.

### 3.3 ⛔ The collision — the greenfield family may already be Track B

`greenfield-family-spec.md` §12 item 11, verbatim:

> `**Slot budget and double-testing.** These seven bots meet `research-loop-spec.md` §4's definition of Track B arms, so the family consumes **7 of the 8 signed Track B slots**; and `GF-SL200` duplicates a variant already in the signed Track A §3 set, pooling error rates nowhere`

and it names the consequence in the same row: *"**Andy's**, and it directly constrains Task 7's
Track B arms."* It does. Two readings, both defensible, and I am not entitled to pick:

| | **Reading A — greenfield IS Track B** | **Reading B — greenfield is §2D, Track B is separate** |
|---|---|---|
| Basis | §4's definition is behavioural: *"Run the variant as its own paper bot. Same underlying, same entry logic, exactly one variable changed, pre-registered."* All seven satisfy it exactly. | The seven are authorised by `build-plan.md` §2D as **fresh builds** of the cutover disposition, signed before the research loop existed. Track B's ≤8 is a separate §10 allocation. |
| Supporting evidence | The greenfield spec says so about itself. | The greenfield spec **also** says so about itself: §3.1 and §12 item 9 defer the fixed-$ rungs *"to Track B"* — i.e. its author treats Track B as a **different** allocation from the family. |
| Slots free after greenfield | **1** | **8** |
| Wave-1 arms buildable | **1** (ARM-B2 only) | **2** (both) |
| Active fleet | 20 + 1 = **21** | 20 + 2 = **22** (ceiling 28) |

**The greenfield spec contradicts itself on this point** — §12-11 counts itself inside Track B
while §3.1 and §12-9 hand work *out* to Track B as somewhere else. That is not a defect in either
document; it is an unruled boundary between two signed ones.

### 3.4 What breaks under **both** readings, and needs saying plainly

`build-plan.md` §2D and `pre-registration-ledger.md` §3 both declare the end state as
**≈18–20 active bots**. Under Reading A the fleet is **21**; under Reading B, **22** at wave 1 and
up to **28** if Track B is fully spent.

⛔ **Every reading of the slot budget puts the fleet outside `build-plan.md` §2D's stated end
state, and `build-plan.md` is 🔒 frozen** (`CLAUDE.md` §3 item 6: changing any of it requires an
explicit "amend the plan"). **Therefore: no Track B arm — not one — can be built without either
an "amend the plan" on §2D's count, or a ruling that Track B slots sit outside §2D's disposition
arithmetic entirely.** This is not a technicality invented here; it is the direct arithmetic of
two signed documents, and it was not visible until both existed.

### 3.5 The recommendation

**Recommended: Reading B, with an explicit amendment, and a wave-1 spend of 2.**

Reason: the seven greenfield bots exist to answer `build-plan.md` §2D's tournament question
(hard-PT vs trailing vs ride vs hedge arms), which predates the research loop. Charging them to
Track B's research budget would leave **one** slot to fund **three** questions the rulings just
created (R-1's dollar rungs, R-2's time exits, R-6's combined-MFE condor) — and would mean the
research loop's own signed allocation was fully consumed before the loop produced a single
observation. That is not what §10's "≤8" was reserving.

**Budget under the recommendation:**

| | slots |
|---|--:|
| Signed Track B cap (§10) | 8 |
| ARM-B1 `GF-QQQ-IC-DStop100` | −1 |
| ARM-B2 `GF-QQQ-IC-Exp1545` | −1 |
| **Held for wave 2** (DSTOP_150, R-6 native-IC pair, SL130 per greenfield §12-9) | **6** |
| Active fleet at wave 1 | 22 (or 20 at §2D's greenfield floor + 2 = 20) |
| Against the 50 cap | 22 of 50 — **subject to C12** |

**Under Reading A, build ARM-B2 only** and hold ARM-B1 until a slot frees or the cap is raised.
§7 explains why B2 is the one that survives a 1-slot budget, and it is not the ordering §4 of the
spec would predict.

---

## 4. What these arms answer that Track A cannot

Three distinct failures, not one. The task names the first; the review found the other two, and
the second is larger than the first and runs opposite to it.

**(1) Marks, not fills — one-sided toward tighter targets.** `research-loop-spec.md` §6.2:
*"A PT that 'would have filled' at MFE might not have. The error is one-sided: it **biases toward
optimism on tighter targets.**"* On the **loss** side the same defect inverts and gets worse: MAE
proves the mark **touched** the stop level; the fill on a 0DTE QQQ spread in the minute a stop
level is crossed is **through** it, not at it. Track A therefore reports a stop's cost as the
level and the arm reports it as the fill. **Every number in this program that would justify a
stop is a number Track A systematically flatters.**

**(2) Censoring by the incumbent exit (D-8) — the larger bias.** MFE/MAE accumulate only until
the position closed, so *Track A can only evaluate variants **tighter** than the incumbent exit on
the same side.* Measured on the v1 capture, demonstration only: MFE ≥ 0.70 on
**65/80 (81.2%, median MFE 1.000)** for the unstopped `QQQ-IC-0DTE-Raw-HoldToExp`, on
**39/364 (10.7%, median 0.286)** for PT25 `IC-SPX-FastPT25-S2`, and on **0/70 (0.0%, median
0.250)** for its `-130PM` clone. An 81% → 0% collapse is the exit erasing the evidence.
⚠️ The §6 limit that states this rule is **drafted but unsigned** (review §9 item 3) — R-2's
applied §3 text already references it as `(§6.5)` and **that reference currently dangles**.

**(3) Structural undecidability.** Time exits produce `UNDECIDABLE` on **1,254 of 1,254**
same-day rows. Not a bias — an absence. No engine fix reaches it. This is §7's subject.

**And the arms carry a bias Track A does not**, which must be said in the same breath: an arm is
`n=1 bot` and its result is confounded with everything the shared objects do. The defence is not
that arms are unbiased; it is that a shared entry automation plus one differing input makes the
confound *the same on both sides of the comparison*. That is the whole of `greenfield-family-spec.md`
§1.1, and these arms inherit it by attaching to the same objects.

### 4.1 The loss-tail rationale, with its n

`data/mirror_baseline.csv` — **n=174 positions across 10 mirrors**, frozen, an anchor and not a
metric. **Four of the ten have a positive median R and a negative mean R:**

| mirror | n | win rate | mean R | median R | sum P/L |
|---|--:|--:|--:|--:|--:|
| `60min-ORB-10W-Paper-v1` | 12 | 83.3% | **−0.0328** | +0.0786 | −$448 |
| `Opening Range Breakout 60m` | 19 | 68.4% | **−0.1107** | +0.0676 | −$2,602 |
| `Trendy-Paper-v1` | 15 | 80.0% | **−0.0365** | +0.0405 | −$119 |
| `Weekly-IB-SPY-Paper-v1` | 18 | 50.0% | **−0.0770** | +0.0217 | −$1,246 |
| **combined** | **64** | — | — | — | **−$4,415** |

They win most of their trades and lose money. **n=64 of 174 positions**; the full 10-mirror set
nets **+$6,284 on n=174**. The entire mean–median gap is the loss tail, which is what §4's
*"loss-tail behaviour is where a 0DTE premium seller lives or dies"* asserts and what these arms
are pointed at.

⚠️ **Discipline, stated rather than assumed:** the mirrors are the **OA-Mirror pillar** —
multi-day, watch-only, other people's bots, other structures. The rationale is **directional and
analogical, not a prior**. No figure in this table is transferable to a QQQ 0DTE condor, and none
is offered as one.

---

## 5. ⭐ ARM-B1 — `GF-QQQ-IC-DStop100`

**The variant:** `DSTOP_100` from the signed §3 set, on R-1's ruled basis — a fixed dollar stop
pinned to **1.00× the bot's trailing-90-day median credit**, held constant across positions.

### 5.1 The question it answers that Track A cannot

R-1's contrast is **not a level contrast — it is an anchoring contrast.** A percent stop
re-evaluates against each position's own credit; a dollar stop is typed once and holds. They
differ **only on positions whose credit departs from the bot's median**, and that is the entire
signal. Measured credit\$/risk\$ over **n=1,254** same-day v1 rows (demonstration only):
**p10 0.036 · median 0.0695 · p90 0.156** — a **4.3× spread p10→p90**. The effect lives in the
tails of that distribution.

Track A cannot decide it, for three compounding reasons:

1. **The signal is in the tail of the credit distribution, which is where n is smallest and where
   MAE is least reliable.** With units corrected, the rejected RISK-basis rungs fired on
   **42/1,254 (3.3%)** and **26/1,254 (2.1%)**; as coded they fired **0/1,254**. A comparison whose
   entire content is a few dozen atypical-credit positions is precisely where a mark-vs-fill error
   dominates the effect.
2. **Stop fills are through the level, not at it** (§4 failure 1). Track A prices the stop at the
   level; the arm prices it at the fill. On the loss side this is the difference between a
   measured cost and a fabricated one.
3. **Censoring** (§4 failure 2): whether the dollar rung is decidable at all depends on the
   incumbent's stop, which is what `bots_config_v2.csv` would tell us — and that file is
   **blocked**, not neglected (`state.md`), so Track A's own honesty flag for this variant cannot
   be computed today.

### 5.2 The control it pairs with, and the ONE differing input

**PRIMARY control: `GF-QQQ-IC-Ride`** (greenfield PR-14) — the family's declared control.

**ONE differing input:** the exit bundle carried by Bot Inputs `GF_EXITS_PUT` / `GF_EXITS_CALL`
= **Ride's base bundle + exactly one mechanic**, `Stop Loss $` (`dstop`) and its pricing
sub-field. This is the identical shape as `GF-SL100`-vs-`Ride` and satisfies
`greenfield-family-spec.md` §8.1's bundle granularity — **one trigger, two fields.**

⚠️ **SECONDARY comparison, pre-declared here and caveated:** the R-1 dollar-vs-percent contrast is
`(DStop100 − Ride) − (SL100 − Ride)` — a **difference-in-differences** against `GF-QQQ-IC-SL100`.
It is **not** a one-parameter comparison. Under §8.1, `DStop100` vs `SL100` differs in
`stoploss` **and** `dstop` **and** both pricing sub-fields — up to four fields — which makes it a
comparison of *policies*, in exactly the class §8.1 says *"must be caveated as such wherever it is
published."* **Naming `SL100` as this arm's control would have been the wrong answer** and would
have quietly restated a four-field policy contrast as a single-variable experiment.

### 5.3 Full bot configuration — confirmed controls only

All fields below are from `oa-platform-reference.md` §6.1a, **[FIRST-HAND 2026-08-04]**, read as
`input.value` on named hidden fields. No field is asserted that was not read there.

**Shared objects — attached, not copied** (`greenfield-family-spec.md` §4):
`GF-ScannerA-PutSpread` · `GF-ScannerB-CallSpread` · `GF-Backstop-1552-FlatClose` ·
`GF-SiblingClose`. Entry SmartPricing **`normal`**, `pct` = 100. Sizing per Phase-0 **C4** —
1 contract if a contract-count primitive exists, else `Up to $250 risk`; **record which**.

**Exit bundle** (put and call, asserted equal by nightly A8):

| # | UI label | Field | Value |
|---|---|---|---|
| 1 | Profit Taking % | `profits` | empty |
| 1b | ↳ PRICING | `smprofits` | — |
| 2 | Profit Taking $ | `dprofit` | empty |
| 3 | Price Target | *(read blocked)* | empty |
| 4 | Stop Loss % | `stoploss` | **empty** |
| **5** | **Stop Loss $** | **`dstop`** | **`<D100>`** — see §5.4 |
| 5b | ↳ PRICING | *(field name unknown)* | ⚠️ **C11** — must be non-Market |
| 6 | Trailing Stop | `tstop` | empty |
| 7 | Touch | `touch` | empty |
| 8 | Expiration | `expdays` | `0.01` (= 10 min before close = 15:50) |
| 8b | ↳ PRICING | `smexpdays` | **`speedy`** — ⛔ not `market` (Decision 6) |
| 9 | Avoid Events | — | **None** |
| 10 | Earnings | `epsdays` | empty |
| 11 | ☐ Wait at least 1 day (PDT) | `chposLimitDay` | **unchecked** |
| 12 | ☐ Disable exit options if bid/ask exceeds $ | `chbidask` / `bidask` | **unchecked / empty** |
| 13 | ☐ Save as presets | `pretext` | `GF-DSTOP100-EXITS` |

Sentinel Default Value on the automation input: `SENTINEL-SL1`, subject to C6.
Bid-Ask Guard **OFF**, identically to all seven greenfield arms (§4.4) — it disables Exit Options
with no error while a spread is wide, which on a stop arm is the worst-timed possible failure.

### 5.4 ⛔ `<D100>` — the value cannot be stamped at Day-0, and this is the arm's real blocker

R-1's basis is *"the bot's trailing-90-day MEDIAN credit, in dollars"*. A fresh bot has no
trailing 90 days, and **`data/trades.csv` holds n=0** (`CLAUDE.md` §3: the v1 ledger is *never a
reporting input*, and an absent number is not a zero). So:

- ⛔ **Stamping `<D100>` from the v1 capture is forbidden.** The credit/risk figures in §5.1 are
  demonstration-only and are quoted here as *rationale*, never as a value.
- ✅ **Resolution, and it falls out of Architecture E.** The arm shares the entry automation with
  its control, so **the control's realised credit distribution IS the arm's**. Declare:
  > `<D100>` = the **median of `credit × 100 × quantity`, in dollars, over `GF-QQQ-IC-Ride`'s
  > closed condors in the first 90 post-cutover trading days**, `expired` excluded (R-7),
  > position = `trade_id` group (R-6). Computed once by `build_ledger.py` output, stamped once,
  > **held constant for the life of the pre-registration.**
- **Consequence, stated rather than absorbed:** the arm is **built at Day-0 and left OFF**, its
  value stamped at **Day-0+90**, and switched on then. It forfeits 90 days of matched-day pairing
  with its control and its review date moves out accordingly. That cost is real and it is the
  price of not stamping a live parameter from frozen v1 data.

⚠️ **An ambiguity in R-1's signed text that needs one word from Andy.** *"trailing-90-day median"*
reads either as **(a)** a one-time calibration recipe, or **(b)** a rolling parameter. R-1's own
prose says *"OA's `dstop` is a fixed dollar typed once and held constant"*, which points at (a).
Under (b) the value would be re-typed periodically — a **mid-trial config change**, which under
§10a item 2 makes every re-stamp a **new pre-registration**. This spec assumes **(a)** and says so.
If Andy means (b), this arm's design changes and PR-21 must be re-drafted before signing.

### 5.5 What this arm cannot conclude

⛔ **CF-4 applies unchanged.** `GF-SiblingClose` force-closes the untested side the instant the
tested side stops, so this arm is **"DStop100-close-both"**, an S2-shaped mechanic. Like `GF-SL100`
and `GF-SL200` it forfeits the untested side's decay and is biased **downward** against any
published dollar-stop comparable. It must never be published under a bare "fixed-$ stop" name.
This is carried, not fixed — removing sibling-close from this arm alone would break matching,
which is worse.

⚠️ **The secondary DiD is gated on C1.** If `stoploss` turns out to be a percent of **RISK** rather
than of **CREDIT**, then `GF-SL100` is not "100% of credit" and R-1's *"pinned to the SAME AVERAGE
LEVEL"* premise does not hold — the DiD then compares a dollar-credit anchor against a
percent-risk anchor and measures two changes at once. **The primary arm-vs-Ride comparison is
unaffected.** C1 is already a blocking Phase-0 check for `GF-SL100`/`GF-SL200`; this arm inherits
it for its secondary reading only.

---

## 6. ⭐ ARM-B2 — `GF-QQQ-IC-Exp1545`

**The variant:** the time exit, **added to Track B by ruling R-2** — `Expiration` **`0.015`**
(15 minutes before close = **15:45**) against the family's **`0.01`** (15:50) incumbent.

### 6.1 The question it answers that Track A cannot — and this one is absolute

Not a bias. An **absence**. Both `TIME_*` slots returned `UNDECIDABLE` on **1,254 of 1,254**
same-day rows. MFE/MAE give extremes and their timestamps; they do not give the position's mark at
an arbitrary clock time, so no engine change reaches this. R-2 ruled the question out of Track A
**by signature**. If no arm funds it, **the question is tested nowhere in the program.**

And it is a loss-side question, not a scheduling one. On `GF-QQQ-IC-Ride` the time exit is the
**only** exit — the arm's entire loss control is *when* it flattens. The nearest measurable proxy
in the export says the last hour is where the outcome is decided: over **n=394** same-day losers,
a trough **before 14:00** recovered **56/326 (17.2%)** while a trough **at or after 14:00**
recovered **45/68 (66.2%)**; on deep losers (MAE ≤ −200%, **n=101**), **15/56 (27%)** early vs
**30/45 (67%)** late. ⚠️ **Demonstration only, v1, and it is a trough-timing statistic, not an
exit-timing one.** It establishes that late-session path matters. It does not price five minutes.

### 6.2 The control it pairs with, and the ONE differing input

**Control: `GF-QQQ-IC-Ride`** (greenfield PR-14).

**ONE differing input — and this is the cleanest comparison in the entire program:**

| Field | `GF-QQQ-IC-Ride` | `GF-QQQ-IC-Exp1545` |
|---|---|---|
| `expdays` | `0.01` | **`0.015`** |
| `smexpdays` | `speedy` | `speedy` — **identical** |
| every other field | empty / base | empty / base — **identical** |

**Exactly one field differs, and its pricing sub-field does not.** `greenfield-family-spec.md`
§8.1 concedes that every arm-vs-control comparison in that family is a **two-field** delta
(*"each trigger comes with its own pricing sub-field"*) and names `SL100` vs `SL200` — a
value-only change — as *"the cleanest comparison in the family."* **ARM-B2 is that shape against
the control itself.** No other proposed or existing arm in this program achieves it.

### 6.3 ⭐ It is the only proposed arm that does not double-test a signed Track A variant

`greenfield-family-spec.md` §12-11's second clause — *"`GF-SL200` duplicates a variant already in
the signed Track A §3 set, pooling error rates nowhere"* — applies to `GF-SL100`, `GF-SL200` and,
honestly, to **ARM-B1** (`DSTOP_100` is in the §3 set). §10a item 1 sets the multiplicity family
as *"the 9 computable variants × every bot under test"*, and an arm is a bot under test, so an
arm's own ledger re-enters Track A's family carrying the same variant. **`TIME_*` was retired
from §3 by R-2, so ARM-B2 alone is tested in exactly one place.** Under a 1-slot budget that is
decisive, and it is §7's answer.

### 6.4 ⛔ The `0.005` (15:55) half of R-2 is NOT buildable in this family

R-2 names two values: `0.015` and `0.005`. Only one is expressible here.

`GF-Backstop-1552-FlatClose` is a **Repeating Events-class** automation firing at **15:52**,
Positions loop (unrestricted) → Close Position, `Market`, memo `1552 backstop flat close`. A
`0.005` Exit Option fires at **15:55** — **three minutes after the backstop has already closed
both legs flat.** The arm's distinguishing variable would be **erased on every day the backstop
works**, and on the days it did not work the arm would be measuring a backstop failure rather
than a later exit.

The mechanism is not marginal and does not depend on jitter: the backstop is a different execution
class, runs whether or not Exit Options run (§6: *"Exit Options always run, even if your
automations inside a bot are turned off"* — the inverse being the backstop's whole reason to
exist), and closes 100% at market.

⛔ **Do not "fix" this by moving or removing the backstop for one arm.** The backstop is a shared
object; changing it changes all seven greenfield arms, and exempting one arm breaks matching.
**The 15:55 rung is therefore deferred with a stated reason: it requires a family whose backstop
is later than 15:55, which this family is not and should not become.** R-2's time question is
funded here in its **earlier** direction only — which is the loss-side direction, and the one §4
asks for first.

### 6.5 Full bot configuration — confirmed controls only

Identical to §5.3 in every respect **except** rows 5 and 8, and the preset name:

| # | UI label | Field | Value |
|---|---|---|---|
| 4 / 5 | Stop Loss % / **Stop Loss $** | `stoploss` / `dstop` | **empty / empty** |
| 1 / 2 / 6 / 7 / 10 | `profits` / `dprofit` / `tstop` / `touch` / `epsdays` | | **all empty** |
| **8** | **Expiration** | **`expdays`** | **`0.015`** = 15 minutes before close |
| 8b | ↳ PRICING | `smexpdays` | **`speedy`** |
| 9 | Avoid Events | — | None |
| 11 | ☐ PDT | `chposLimitDay` | unchecked |
| 12 | ☐ Bid/ask guard | `chbidask` / `bidask` | unchecked / empty |
| 13 | ☐ Save as presets | `pretext` | `GF-EXP1545-EXITS` |

`0.015` is **confirmed to exist and confirmed in its meaning** — `oa-platform-reference.md` §6.1a
enumerates the Expiration dropdown first-hand, 2026-08-04: *"`0.011`–`0.015` 11–15"* minutes
before close. Nothing here is inferred from a grid or a label.

⚠️ **"15:45" assumes a 16:00 close.** On an early-close session `0.015` is 15 minutes before
**that** close (e.g. 12:45 on a 13:00 half day) — as is the control's `0.01`, so the **arm
variable is preserved** and only the absolute clock time moves. Half days are flagged for
exclusion from matched-day pairing rather than silently pooled.

### 6.6 ⛔ A defect this arm introduces, with its fix — the sibling-close race

**Found while specifying this arm; it is not in any existing document.**

`GF-SiblingClose` is gated `Current market time is before 3:50pm`, and
`greenfield-family-spec.md` §4.3(c) states the gate's purpose exactly: it *"de-races the
backstop"*, because otherwise one leg's close fires `Position closed`, sibling-close issues a
**SmartPricing** close on leg 2 while another mechanic issues a close on the same leg. §4.3 calls
sibling-close *"the highest-risk shared object in the family."*

**On `GF-QQQ-IC-Ride` the gate works:** both legs hold `expdays` `0.01`, both close at ~15:50,
and 15:50 is **not** before 15:50, so sibling-close is excluded.

**On `GF-QQQ-IC-Exp1545` it does not.** Both legs close at ~15:45, which **is** before 15:50. Leg 1
fills → `Position closed` fires → sibling-close loops, finds leg 2 open with a differing side tag,
opened today, time < 15:50 → issues a `patient` close on leg 2 **while leg 2's own `speedy`
Expiration order is still working** (memo finding N-6: an exit-option order stays live **two
minutes**). That is the 7/01 orphan-loop shape, reintroduced at 15:45, **on this arm alone** —
which makes it not merely an operational risk but a **mechanic difference between arm and
control**, i.e. a confound in the one comparison the arm exists to make.

**Named fix, recommended, NOT applied here** (it edits a shared object in a spec this task may not
edit):

> Move `GF-SiblingClose`'s gate from `before 3:50pm` to **`before 3:44pm`**, in Phase A, **before
> any greenfield arm is switched on** — not as a later edit.

**Cost, stated:** on the five triggered greenfield arms, a trigger firing in [15:44, 15:50) leaves
the sibling open until its own 15:50 Expiration exit closes it — the condor still closes, at worst
six minutes later, with no orphan. **Benefit:** the gate keeps doing exactly what §4.3(c) built it
to do, for both the 15:52 backstop and the 15:45 exit, and all seven greenfield arms plus both new
arms share one unchanged object. ⚠️ Because it changes a shared object, it requires re-verification
of every attached arm (assert **A7**, payload-hash baseline) and is **Andy's**, since
`greenfield-family-spec.md` is not this session's to amend.

### 6.7 One asymmetry this arm gains, recorded rather than claimed as a win

`greenfield-family-spec.md` §6.2 records **four** mechanics that can close a position between
15:50 and 15:52, and Rule 3 buckets ambiguous fills there as **`UNATTRIBUTED`**. A 15:45 exit sits
**outside that window entirely**, so ARM-B2's own closes are cleanly attributable and its control's
are not. **That is an asymmetry in measurement quality between arm and control, not a virtue of the
arm** — the arm will look tidier in the Trades list for reasons that have nothing to do with the
hypothesis. It is recorded here so nobody later reads a lower `UNATTRIBUTED` count as a result.

---

## 7. ⭐ SHOULD ONE OF THE FIRST ARMS BE A TIME ARM? — **YES, and it should be the first one built**

The task asks this directly. The answer has two halves, and they point in opposite directions.

**On priority, `research-loop-spec.md` §4 nominates the dollar stop.** §4's own words:
*"Priority for the first arms, given §1a: the **loss side**. `Stop Loss $` and `Touch` are both now
confirmed to exist…"*. `Touch` is already funded (`GF-QQQ-IC-Touch0`, PR-17). `Stop Loss $` is
ARM-B1. **By §4's literal nomination, ARM-B1 ranks first.**

**On build readiness, it inverts — and readiness decides what gets built at Day-0.**

| | ARM-B1 `DStop100` | ARM-B2 `Exp1545` |
|---|---|---|
| Variant authority | signed §3 (R-1 basis) | ruled into Track B (R-2) |
| Answerable in Track A? | biased and censored — but **not** structurally blocked | ⛔ **`UNDECIDABLE` 1,254/1,254 — nowhere else** |
| Value stampable at Day-0? | ⛔ **no** — needs 90 days of post-cutover credit (§5.4) | ✅ **yes** — `0.015`, enumerated first-hand |
| Primitive confirmed? | ⚠️ `dstop` exists; **unit and pricing sub-field unobserved** (C10, C11) | ✅ `expdays` exists **and its values are enumerated** |
| Fields differing vs control | 2 (trigger + pricing) | **1** |
| Double-tests a §3 variant? | yes (`DSTOP_100`) | **no** — retired from §3 by R-2 |
| Blocking checks it adds | C10, C11 | the C8-adjacent sibling-close gate change (§6.6) |
| Earliest first observation | **Day-0 + 90** | **Day-0** |

**Therefore:**

1. **Yes — one of the first arms must be a time arm.** R-2 removed the question from Track A by
   signature and named Track B as its funder. Leaving it unfunded would reproduce, in Track B, the
   exact misallocation the review called *"the worst allocation on the board"* — the one question
   Track A provably cannot answer, unfunded in the track that answers it in one field.
2. **It should be `Expiration 0.015` (15:45), not `0.005`** — §6.4: the 15:52 backstop preempts a
   15:55 exit structurally.
3. **Build order is B2 then B1**, and this is a **readiness ordering, not a priority reversal**.
   B1 remains §4's nominated first arm on the merits; it is simply not stampable until Day-0+90 and
   carries two unobserved primitives. Building B2 at Day-0 and B1 at Day-0+90 spends nothing extra
   — B1's calibration window runs while B2 collects.
4. **Under Reading A's 1-slot budget, build B2 and hold B1.** It is the only proposed arm that is
   simultaneously ruled-in, buildable today, a true one-field delta, and not double-tested in
   Track A.

**And the time exit is a loss-side arm, not an exception to §4.** On the ride control the time
exit is the only loss control there is. Moving it earlier truncates the last 5 minutes of 0DTE
gamma exposure — the same tail §4 sends the first arms after.

---

## 8. Rejected candidates — every one, with its reason

**8.1 `SL150` — rejected on information, not on rules.** In the signed §3 set, expressible, not
covered by greenfield, one-field-value change from `GF-SL100`. Rejected because the review's own
design finding measures the value elsewhere: *"the loss rungs cluster where marginal separation is
6–28 positions while the **159-position gap between SL50 and SL75** is unsampled."* Fire counts on
n=1,254: `SL100` 279 (22.2%), `SL150` 200 (15.9%), `SL200` 172 (13.7%) — inserting `SL150` between
two arms that already exist buys **~28–79 positions** of separation for a whole slot.

**8.2 `DSTOP_150` — held for wave 2.** R-1 pins it to `SL150`, which does not exist, so the paired
contrast would cost **two** slots. R-1's argument is about **anchoring**, not level; one rung tests
anchoring. Reopen when ARM-B1 returns a signed result.

**8.3 `COND_100_1300` / `COND_100_1400` / `COND_200_1400` — not expressible.** In the signed §3
set, and they are the export's strongest discriminator — and they cannot be arms.
`oa-platform-reference.md` §11: *"Regime-conditional branching at a breach — **NOT NATIVE.** No
mid-trade branching"* and *"Any condition referencing its own past — **NOT NATIVE**"*. A stop whose
level depends on whether the trough already happened is a mid-trade state change.
`greenfield-family-spec.md` §3.1 excludes the same shape twice on the same rows.
⚠️ **These three are Track-A-only by construction** — the one place in the program where Track A is
the *only* instrument. That is worth recording, because it inverts the usual direction and because
Track A's censoring bias applies to them in full.

**8.4 R-6's combined-MFE condor question — deferred, with the reason.** R-6 ruled it a Track B
question. It is **not expressible as an arm of this family**: §3 of the platform reference models
*"each spread as a separate position"*, the condor pairing is a **project** construct (`trade_id`),
and OA applies Exit Options **per position**. A combined-credit stop or PT is therefore not a field
on this family's bundle. Answering R-6 needs a bot whose entry opens a **native `ironcondor`** —
one position, not two spreads — which **cannot share `GF-ScannerA`/`GF-ScannerB`**, so it needs its
own matched control too: **2 slots, and a second entry automation.** Wave 2, on the held budget.
*(Context, v1 capture, n=1,386 export rows: only **102** are native `ironcondor` and **1,246** are
single-sided legs — so this is the majority case, not an edge one.)*

**8.5 ⛔ `SL50` / `SL75` — forbidden, and the program pays for it.** By the review's own
measurement the **SL50→SL75 gap (159 positions unsampled, n=1,254)** is the highest-information
loss rung available, and `hedge-research.md` §9's **#1 ordered sweep item** is
*"SL100 + SL150 on the Range075-filtered base, controls **SL50** / current / Unstopped."* Neither
`SL50` nor `SL75` is in the signed §3 set, and **no ruling added them**. The task's rule is
explicit, so they are excluded. **Recorded as a cost of the freeze, not as a design choice:**
reaching them requires a new §3 signature, which §10 deliberately makes expensive. Andy's, if he
wants it.

**8.6 `PT40` / `PT60` / `PT70` — deferred by §4's own ordering.** Profit side. `GF-PT50` covers the
incumbent level. Wave 2.

**8.7 `Touch`, `Trail`, `PT50`, `SL100`, `SL200` — already funded** as greenfield PR-15…PR-19.
Re-specifying any of them would spend a slot to duplicate a bot.

---

## 9. DRAFT pre-registration entries

*Format per `pre-registration-ledger.md` §2. **Both entries are DRAFT — unsigned.** Signing is
Andy's, at Day-0, per §7 of that ledger: config hash filled from the bot's own capture, every
placeholder resolved, kill criterion re-read against the daily loop, max loss filled, then signed —
and only then may the bot be switched ON. **Signed ≠ verified**: the Trades-list artifact is read
before it may take a position.*

**Conventions applying to both, stated once** (inherited verbatim from
`greenfield-family-spec.md` §9 so the two families read against each other):

- **Unit: the POSITION = the CONDOR** (`trade_id` group), **risk = the larger side** (R-6,
  `CLAUDE.md` §4). Every `Exp(R)` is **per condor, ex-artifact**. `R` basis is **`ror`** (return on
  risk), never `returnPct`. `expired` rows are **excluded from every count** (R-7).
- **Analysis is PAIRED BY DAY, on matched days only.**
- **Comparative criterion — the §10 gate as amended by R-3:** the arm beats its control only if
  **(a)** mean ΔR **≥ +0.015R per condor**; **(b)** a paired bootstrap **95% CI excludes zero**
  under §10a's stratified sign-flip permutation procedure (10,000 flips, max-T, **no Bonferroni
  term**); **and (c)** on the subpopulation where the arm's trigger actually fires, a paired sign
  test against the control is significant at the same level. **The median-ΔR test is WITHDRAWN.**
- **SIZING TIER** 1 lot — experiment, **identical to the greenfield arms by construction** (shared
  Open Position action), subject to C4 and the nightly **A6** one-contract assert.
- **CONFIG HASH** `<capture> @ <sha256>` — filled at signing from the arm's **own capture**, not
  from a template (template rows carry the bot's live `rid`; the capture is the snapshot).
- **Family-level, liveness and sentinel kill criteria** are carried identically from
  `greenfield-family-spec.md` §9, including the field-granularity correction to the family rule.
- **⭐ GATE EVALUATION DATE** — required by §10a item 2 (*"The gate is evaluated ONCE, at the
  pre-declared n=100 … on a date written into `pre-registration-ledger.md` BEFORE n reaches 100"*).
  ⚠️ `pre-registration-ledger.md` §2's template has **no field for this**; see §11 item 5.

---

```
### GF-QQQ-IC-Exp1545
ID               PR-22  (proposed — see §11 item 4)
DISPOSITION      fresh build — Track B arm (research-loop-spec.md §10, ≤8 allocation)
PILLAR / ROLE    IC · experiment
STATUS           DRAFT — unsigned

HYPOTHESIS       Flattening an unmanaged QQQ 0DTE iron condor at 15:45 rather than 15:50 raises
                 Exp(R) per condor above the GF-QQQ-IC-Ride control, on matched days, by
                 truncating the final five minutes of 0DTE gamma exposure. Falsifiable in both
                 directions: if the last five minutes are net decay rather than net gamma, the
                 paired ΔR is negative and the arm dies on its own kill criterion.
MECHANISM        The arm buys removal of terminal gamma exposure at the price of five minutes of
                 theta. Which dominates is not derivable — it is the whole question, and it is
                 structurally UNDECIDABLE from MFE/MAE (1,254/1,254 UNDECIDABLE on the v1
                 capture), which is why ruling R-2 retired it from Track A §3 and funded it here.
                 PRIMITIVES, named so a substitution has something to contradict:
                 shared Library entry automations GF-ScannerA-PutSpread / GF-ScannerB-CallSpread
                 (Loop -> after 1:30pm -> before 2:00pm -> Range075 two-sided symbol decisions ->
                 position-tag re-entry gate -> Open Short Put/Call Spread, SmartPricing `normal`)
                 + bundle-typed Bot Inputs GF_EXITS_PUT / GF_EXITS_CALL holding
                 {Expiration `expdays`=0.015, `smexpdays`=speedy} AND NOTHING ELSE
                 + the shared Events-class 15:52 Market flat close
                 + the shared GF-SiblingClose (⚠️ gate to be moved 15:50 -> 15:44, §6.6)
                 Size primitive per C4 — RECORD WHICH ONE WAS USED BEFORE BUILD.
                 ⚠️ This is a close-both (S2-shaped) mechanic; sibling-close is on. Do not
                 publish it as a bare "earlier time exit" result.
KILL CRITERION   R-based, computable from the daily loop, fires with no human in the loop:
                 (K1) paired per-condor mean ΔR vs GF-QQQ-IC-Ride < 0 with the bootstrap 95% CI
                      entirely below 0 at n >= 60 matched condors -> RED, bot off.
                 (K2) LIVENESS — zero close rows at ~15:45 priced `speedy` across 10 consecutive
                      matched days -> RED, pending investigation. (Not conditioned on a threshold
                      breach: unlike a stop, a time exit must fire every single day, which makes
                      this arm's liveness test the strongest in the program.)
                 (K3) FAMILY — a capture-diff showing this arm differs from GF-QQQ-IC-Ride in more
                      than one mechanic (trigger field + its pricing sub-field), or any of A1, A2,
                      A3, A7, A8 firing -> the comparison is VOID and both arms are re-based.
                 (K4) SENTINEL — stored bundle == SENTINEL-SL1 -> RED (A4); plus the behavioural
                      form, positions closing within 5 minutes of open on >=2 consecutive days
                      while the stored config carries no stop (A4b).
                 (K5) A fired trigger not executed within 48 hours is itself a kill condition
                      (pre-registration-ledger.md §2 rule 3).
SAMPLE TARGET    n = 100 closed CONDORS for this (bot, variant) pair, `expired` excluded
                 (R-4's signed §5 companion line — ⚠️ NOT YET APPLIED to §5, review §9 item 1).
                 ⚠️ DECLARED WITH ITS POWER, NOT WITHOUT IT. At SD(R) ~ 0.30 with day-pairing at
                 rho ~ 0.90, n=100 gives a 95% CI half-width on paired ΔR of ±0.026R, against a
                 required margin of +0.015R and a largest-ever-measured effect in this program of
                 +0.0150R (SL75, n=1,254). Reaching ±0.015R needs ~307 matched condors.
                 n=100 is therefore a FIRST-READ target, not a decision target.
                 ⛔ THE §5 GATE IS CONJUNCTIVE AND ITS THIRD CONJUNCT IS UNDEFINED: n>=100 AND
                 >=6 months AND "the window spans a regime change" AND a pre-declared margin.
                 No definition of "regime change" exists anywhere in this repository. This arm
                 CANNOT GRADUATE until one is written and signed, regardless of n. Not invented
                 here (greenfield-family-spec.md §12 item 12).
REVIEW DATE      Day-0 + 6 months; interim read at n = 60 matched condors.
GATE EVAL DATE   <Day-0 + N days>  ← stamped at signing, BEFORE n reaches 100 (§10a item 2).
                 Evaluated ONCE. If n < 100 on that date the gate does not fire; re-declaring it
                 is a NEW pre-registration, not an extension.
MAX LOSS         ~$185 net risk per condor ($200 gross per side less credit, $2-wide QQQ);
                 daily aggregate per bot = one condor.
SIZING TIER      1 lot — experiment. IDENTICAL to all greenfield arms (shared entry action).
CONFIG HASH      <capture> @ <sha256>            ← filled at signing, from this bot's own capture
VERIFICATION     Trades list, never the Exit Options panel (CLAUDE.md §3 item 3):
                 (V1) a close row at ~15:45 priced `speedy`, on the FIRST new position;
                 (V2) NO profit-taking, trail, touch or stop row;
                 (V3) the pairwise capture-diff of greenfield §8.2 against GF-QQQ-IC-Ride,
                      decoding the BOT INPUT object's value — never the action's reference,
                      never `oldValue`, never a rendered label (G2 rider);
                 (V4) no duplicate/racing close on the second leg at ~15:45 (§6.6 must be fixed
                      first — this is the observation that proves it was).
SIGNED           ..............................
```

```
### GF-QQQ-IC-DStop100
ID               PR-21  (proposed — see §11 item 4)
DISPOSITION      fresh build — Track B arm (research-loop-spec.md §10, ≤8 allocation)
PILLAR / ROLE    IC · experiment
STATUS           DRAFT — unsigned

HYPOTHESIS       A stop anchored in DOLLARS at 1.00x the bot's median credit, held constant
                 across positions, raises Exp(R) per condor above the GF-QQQ-IC-Ride control on
                 matched days — and, in the pre-declared secondary reading, differs from a
                 percent-of-own-credit stop set to the same average level (GF-QQQ-IC-SL100).
                 The secondary is the real question: the two rules are identical at the median
                 and diverge only on positions whose credit departs from it, which on the v1
                 capture spans p10 0.036 to p90 0.156 credit$/risk$ (n=1,254, demonstration
                 only) — a 4.3x spread. If credit dispersion carries no information about
                 outcome, the difference-in-differences is zero and the hypothesis is dead.
MECHANISM        hedge-research.md §9 item 6 ("Fixed-$ SL variants alongside the % rungs, now
                 that OA supports them"). A dollar anchor stops high-credit positions EARLIER in
                 percentage terms and low-credit positions LATER; if adverse excursion scales
                 with dollars at risk rather than with credit collected, the dollar anchor is the
                 better-matched rule. Track A cannot settle it: the signal lives in the tail of
                 the credit distribution where n is smallest, and stop fills are THROUGH the
                 level while MAE only proves the mark touched it.
                 PRIMITIVES: the same four shared Library objects as PR-22, plus bundle-typed Bot
                 Inputs GF_EXITS_PUT / GF_EXITS_CALL holding
                 {Expiration `expdays`=0.01, `smexpdays`=speedy, Stop Loss $ `dstop`=<D100>,
                  <dstop pricing sub-field per C11 — non-Market>} AND NOTHING ELSE.
                 ⚠️ `dstop` (Stop Loss $) is CONFIRMED TO EXIST, first-hand on the live modal
                 2026-08-04 (oa-platform-reference.md §6.1a), and was read EMPTY. Its UNIT
                 (per contract / per position / per leg) and its pricing sub-field are
                 UNOBSERVED — checks C10 and C11. Per hedge-research.md §5.2 this is NOT AN ARM
                 until both close.
                 ⚠️ Close-both (S2-shaped): sibling-close force-closes the untested side the
                 instant the tested side stops, forfeiting its decay. Biased DOWNWARD against any
                 published fixed-$ comparable (CF-4). Never publish under a bare "fixed-$ stop"
                 name. Size primitive per C4 — RECORD WHICH ONE WAS USED BEFORE BUILD.
KILL CRITERION   (K1) paired per-condor mean ΔR vs GF-QQQ-IC-Ride < 0 with the bootstrap 95% CI
                      entirely below 0 at n >= 60 matched condors -> RED, bot off.
                 (K2) LIVENESS, conditioned so it cannot fire on a calm regime: zero stop rows
                      across 10 consecutive matched days ON WHICH THE LEDGER SHOWS <D100> WAS
                      BREACHED (from MFE/MAE) -> RED, pending investigation.
                 (K3) FAMILY — as PR-22 K3, against GF-QQQ-IC-Ride.
                 (K4) SENTINEL — as PR-22 K4 (A4 and A4b).
                 (K5) 48-hour execution rule, as PR-22 K5.
SAMPLE TARGET    n = 100 closed CONDORS for this (bot, variant) pair, `expired` excluded.
                 Same power statement as PR-22: ±0.026R at n=100 against a +0.015R margin;
                 ~307 matched condors for ±0.015R. FIRST-READ target, not a decision target.
                 ⛔ Same undefined "regime change" conjunct — cannot graduate until it is defined.
                 ⚠️ The SECONDARY difference-in-differences against GF-QQQ-IC-SL100 is a
                 DIFFERENCE OF TWO NOISY ESTIMATES and its CI is materially wider than either
                 arm-vs-control CI. It is NOT powered at n=100 and is declared as descriptive
                 at this n. It is also gated on C1 (§5.5).
REVIEW DATE      Day-0 + 90 + 6 months.  ⚠️ NOT Day-0 + 6 months — see CALIBRATION.
                 Interim read at n = 60 matched condors.
GATE EVAL DATE   <Day-0 + 90 + N days>  ← stamped at signing, BEFORE n reaches 100 (§10a item 2).
CALIBRATION      ⛔ <D100> CANNOT BE STAMPED AT DAY-0 and this is the arm's binding constraint.
                 <D100> := median of (credit x 100 x quantity), in dollars, over
                 GF-QQQ-IC-Ride's closed condors in the first 90 post-cutover trading days;
                 `expired` excluded; position = trade_id group. Legitimate because the arm and
                 the control SHARE the entry automation, so the control's realised credit
                 distribution IS the arm's.
                 Stamped ONCE at Day-0+90 and HELD CONSTANT for the life of this
                 pre-registration. A re-stamp is a NEW pre-registration (§10a item 2).
                 ⛔ NOT from data/captures/oa_export_positions_2026-07-30.csv — v1 is frozen and
                 is never a reporting input (CLAUDE.md §3). The credit/risk figures quoted in
                 the HYPOTHESIS are rationale, never a value.
                 The bot is BUILT at Day-0 and left OFF; it is switched ON at Day-0+90 once
                 <D100> is stamped. It forfeits 90 days of matched-day pairing. That cost is
                 accepted rather than hidden.
                 ⚠️ Depends on Andy resolving R-1's "trailing-90-day median" as a ONE-TIME
                 calibration (assumed here) vs a ROLLING parameter (§5.4). If rolling, re-draft.
MAX LOSS         ~$185 net risk per condor; daily aggregate per bot = one condor.
                 ⚠️ If C10 returns a PER-CONTRACT `dstop` unit, this line and <D100> both change.
SIZING TIER      1 lot — experiment. IDENTICAL to all greenfield arms.
CONFIG HASH      <capture> @ <sha256>            ← filled at signing, from this bot's own capture
VERIFICATION     Trades list, never the Exit Options panel:
                 (V1) a stop-loss row on the first position at which the ledger shows <D100> was
                      breached — with the fill price recorded, because the gap between <D100> and
                      the fill IS the quantity this arm exists to measure that Track A cannot;
                 (V2) NO profit-taking, trail or touch row; NO `stoploss` value in the decoded
                      bundle (a percent stop here would silently answer a different question);
                 (V3) the pairwise capture-diff of greenfield §8.2 against BOTH GF-QQQ-IC-Ride
                      (primary) and GF-QQQ-IC-SL100 (secondary), decoding the BOT INPUT value;
                 (V4) a `sibling close` memo row on the second leg priced `patient`.
SIGNED           ..............................
```

---

## 10. Blocking checks this spec adds

Same discipline as `greenfield-family-spec.md` §10 Phase 0: each is a **read**, not a write; each
has a named outcome and a named fallback; **if a check cannot be answered, STOP and report — do
not improvise a spec on the fly.** Each answer is filed to
`data/captures/edit-verify/<date>/phase0_C<n>.png|.txt` with the read value written into the
session log. Nothing is answered from memory or from this document.

| # | Check | If it fails |
|---|---|---|
| **⛔ C10** | **The UNIT of Exit Options `dstop` (Stop Loss $)** — per **contract**, per **position**, or per **leg**? Read the live modal's own label and any suffix, plus any helper text. §6.1a read the field as *empty*; **its semantics were never observed.** | R-1's rung is specified *"in dollars"*. A per-contract unit puts `<D100>` off by the contract count and the arm silently tests a different level. **Re-derive `<D100>` on the actual basis and re-stamp PR-21 before build.** This is the D-6 units failure one layer up — the same class that made every Track A counterfactual wrong by 100 × quantity. |
| **⛔ C11** | **Does `dstop` carry its own SmartPricing sub-field** (as `profits`→`smprofits` and `expdays`→`smexpdays` do), or inherit a default — and **what is that default**? C3 covers `tstop`, `touch` and `stoploss`; **it does not cover `dstop`.** | ⛔ If it inherits **`market`**, ARM-B1 violates §7's Market ban and Decision 5, **and** confounds the comparison with a pricing difference its control does not have. **Stop. Report. Do not build the arm.** |
| **⛔ C12** | **Do ARCHIVED bots count against the Pro plan's 50-bot cap?** One read of the membership/bots page after the Group-A sweep, comparing the visible slot count against 36 roster bots. | If they do: 36 + 7 fresh = 43, and **≤8 Track B does not fit** (43 + 8 = 51). The ≤8 allocation in §10 would need re-declaring against an observed count rather than a plan tier. **This is currently an unverified inference and §3.2 says so.** |
| **⛔ C13** | **The `GF-SiblingClose` gate move, 15:50 → 15:44** (§6.6). Not a question — a required change to a shared object, before any arm is switched on. Verify as a real decision node (C8 discipline), then re-baseline every attached arm's shared-object payload hash (assert **A7**). | Without it ARM-B2 races its own second leg at 15:45 on every trading day, and the race is **arm-specific**, i.e. a confound in the only comparison the arm makes. ⚠️ Touches `greenfield-family-spec.md`'s shared object — **Andy's**, not this spec's to apply. |

**Inherited unchanged from `greenfield-family-spec.md` §10 Phase 0** — both arms attach to the same
shared objects, so **C0a, C0b, C0c, C4, C5, C6, C7, C8, C9 gate these arms exactly as they gate the
seven.** In particular ⛔ **C0a can stop this architecture outright**, and if it does, these two arms
return to Andy with the tournament. **C1** gates ARM-B1's secondary reading only (§5.5).

---

## 11. Open items this spec does not close

| # | Item | Why it is not closed here |
|---|---|---|
| **1** | ⭐ **The Reading A / Reading B slot collision** (§3.3), and the fact that **every** reading puts the fleet outside `build-plan.md` §2D's frozen "≈18–20 active" (§3.4) | **Andy's.** Binds two signed documents plus a frozen one. Reading B recommended; **no arm may be built until this is ruled and §2D is amended or scoped.** |
| **2** | ⛔ **The four consequential edits still NOT applied to `research-loop-spec.md`** (review §9): §5's `n ≥ 100 positions` line · §5's `**adjusted for the 12-variant count**` phrase, now contradicted by §10a · **§6 limit 5, the censoring block — R-2's applied §3 text already references it as `(§6.5)` and that reference dangles** · §1a's `74 (19%)`, correctly **101/394 = 25.6%** | Outside the §3/§10 authorisation. **Both SAMPLE TARGETs above are written against the signed-but-unapplied §5 wording**, so until item 1 of that list is applied, this spec's targets and §5's text disagree on their face. Review §9 recommends ruling 1–3 together. |
| **3** | ⭐ **`greenfield-family-spec.md` §12 item 10 is STALE** — it is written against the superseded `≥0.10R` margin and concludes *"nothing here can ever graduate"*. **R-3 lowered the margin to +0.015R**, which that family's theoretical range (+0.083R to +0.162R) clears comfortably. The item should be re-scoped: the **effect-size** objection is resolved; the **power** objection is not (n=100 → ±0.026R; ~307 matched condors for ±0.015R; ~560 with Bonferroni) | Not this spec's file to edit. Flagged so the greenfield build does not carry a resolved blocker as if it were live — and so the surviving half is not lost with it. |
| **4** | **PR-21 / PR-22 ID literals are PROPOSED.** `pre-registration-ledger.md` §8 item 1: PR-01…PR-13 are stamped and final; §6's are ranges until the fresh-build counts are fixed. Greenfield proposes PR-14…PR-20 | These follow greenfield's block and become final when Andy fixes both counts. **If the greenfield count lands below 7, these shift down.** |
| **5** | **`pre-registration-ledger.md` §2's template has no GATE EVALUATION DATE field**, which §10a item 2 now requires *before* n reaches 100 | Editing that template is a change to a signed document. Both entries above carry the field anyway, marked ⭐, so nothing is lost if the template is amended later. |
| **6** | ⭐ **"Regime change" is undefined everywhere.** `research-loop-spec.md` §5 and `build-plan.md` §5 are **conjunctive** gates whose third conjunct has no definition and no detector in `scripts/` | **No arm and no variant can graduate until it is written and signed**, regardless of n or elapsed time. Not invented here. Same finding as greenfield §12 item 12 — recorded twice, from two directions, which is itself the argument for closing it. |
| **7** | ⭐ **The comparative machinery does not exist.** Nothing produces a cross-bot **paired ΔR with a bootstrap CI**; `research_loop.py` is `0.1.0-DRAFT`, advisory-only, carries **three fatal defects** and **must not be wired in**; §10a's stratified sign-flip permutation test is unimplemented; and the liveness criteria need an **exit-reason field the export may not carry** | Every comparative criterion in §9 is currently uncomputable. `pre-registration-ledger.md` §7 item 3 makes it a **signing gate**, so this blocks signing, not just analysis. Largest unbuilt dependency these arms imply. |
| **8** | **R-1's "trailing-90-day median": one-time calibration or rolling?** (§5.4) | One word from Andy. This spec assumes one-time; rolling makes every re-stamp a new pre-registration under §10a. |
| **9** | **`bots_config_v2.csv` is BLOCKED, not neglected** — written per-bot as each bot is built. It is what the capture-diff, the drift detector and Track A's `censored` flag all read | Not a task; a consequence of build order. Both arms write their rows when they are built. |
| **10** | **The 15:55 rung of R-2 is unfunded** (§6.4) and the **SL50/SL75 gap is unreachable** (§8.5) | Both are recorded as costs, not as oversights. Each needs a decision Andy has not been asked for: a later-backstop family, and a new §3 signature. |

---

## 12. Verification record

- Every source file read **directly from the device** via `device_bash`, not from a staged copy.
  `state.md` records that **a staged read once returned text that is not in the file**; the
  standing mitigation is to derive anchors from the device file itself, and that is what was done.
- **Every quoted phrase in this document was taken from the device file and re-read in place
  before use.** No claim is sourced from a screen that was not opened, and no OA surface was
  opened at all in this session.
- **Every empirical figure carries its n**, and every capture-derived figure is labelled
  **v1 pre-cutover, demonstration only** per spec §1a and `CLAUDE.md` §3. `data/trades.csv` holds
  **n=0**. Absent is not zero.
- `data/mirror_baseline.csv` figures in §4.1 are read from the CSV, not from a narrative doc
  (`CLAUDE.md` §3 item 5: *narrative docs never carry numbers; if a `.md` states a figure, the CSV
  wins*). The four-mirror subset (n=64 of 174) and the −$4,415 / +$6,284 sums were computed from
  its rows.
- **Three arms' worth of primitives are marked UNCONFIRMED rather than assumed** — `dstop`'s unit
  (C10), `dstop`'s pricing sub-field (C11), and the inherited C1/C3 set. Per
  `hedge-research.md` §5.2's closing sentence, **ARM-B1 is not an arm until C10 and C11 close.**
  That is the HedgeD rule applied to this spec's own drafting: the bot that lost **−$15,376**
  did so because a substitution was made at a platform limit and never recorded.
- **Nothing was built.** No OA surface touched, no bot created, no config written.
  `research-loop-spec.md`, `research_loop.py`, `greenfield-family-spec.md`, `daily.sh` and
  `pre-registration-ledger.md` are **unmodified**. `research_loop.py` is **not** wired into
  `daily.sh`. No `git` command was run.
- The written file is verified by **direct on-device `shasum -a 256`**, recorded in the session
  log alongside the container-side hash, per `CLAUDE.md` §9.1a.

**Changed files for Andy's commit:**

- `docs/track-b-arms-spec.md` *(new)*
- `docs/session-log.md` *(appended)*
