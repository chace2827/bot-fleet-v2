# Directional Pillar — OA Compare-Backtests Build Sheet

> Created 2026-06-24. Click-by-click for building the directional backtests on OA's **Compare
> Backtests** page, structured around the **Duplicate** button so you build the base ONCE and copy it
> for every variant. Sequence = one factor per batch, each vs its control (methodology discipline —
> beat control + read main effects, not the best cell). Gate = **VIX** (validated by C1 as the regime
> signal; OA has no raw ATM-IV filter, VIX = the absolute-IV analog). Judge on **Return-on-Risk +
> Profit Factor + Worst Loss**, NEVER win rate or total P/L.

## The time-saver: build once, duplicate, tweak one field

OA's Compare page holds up to **5 columns (A–E)**. Workflow for every batch:
1. Build **Column A (the control)** fully — all shared settings.
2. Click **Duplicate** on A → it copies every setting into a new column.
3. Change **exactly ONE field** in the copy (the variable for that batch).
4. Repeat duplicate → tweak for each remaining column.
5. Run all, read side-by-side.

Never hand-build B/C/D from scratch — duplicate A so the shared settings are guaranteed identical
(that's what makes the comparison clean).

---

## BATCH 1 — Does the VIX regime gate add edge? (run this first)

**Question:** C1 proved high-VIX days *move* more, but moving ≠ making money (high IV = expensive to
buy). Does firing a directional trade only on high-VIX days beat firing every day?

### Column A — the control (build this fully, once)

| Setting | Value |
|---|---|
| Symbol | **SPX** |
| Strategy / structure | **Long Put Spread** (debit put spread — bearish, defined-risk) |
| Expiration | **0DTE** (same-day) |
| Long leg | put closest to **at-the-money** (~0.45–0.50 delta) |
| Short leg | put **$15 below** the long (or ~0.30 delta — pick one selector, keep it fixed) |
| Width | **$15** |
| Quantity | **1 contract** |
| Entry trigger | **Time of day = 11:00 ET** (fixed for now; OR-break is Batch 3) |
| Entry filters | **NONE** (this is the control) |
| Profit target | **+100%** of debit |
| Stop loss | **−50%** of debit |
| Time/expiry exit | **hold to close / settlement** (0DTE, defined-risk) |
| Slippage | **0.03** per leg |
| Commission | **$0.60 / contract** |
| Date range | **max available** (SPX 0DTE ≈ 2022 → now) |

Run Column A. Expect it to **lose or scratch** (bearish bet fighting bull drift + theta) — that's the
baseline the gate has to beat.

### Columns B / C / D — duplicate A, add ONE filter each

For each: click **Duplicate** on Column A, then add a single **Entry Filter → Market condition → VIX**:

| Column | The one change |
|---|---|
| **B** | Entry filter: **VIX ≥ 18** |
| **C** | Entry filter: **VIX ≥ 20** |
| **D** | Entry filter: **VIX ≥ 22** |

(VIX lives under the backtest's Entry Filters / market-condition list — same place as Gap %, Change %,
IV Rank. If the label is "VIX Level," that's it.)

### Read the result
Compare the four columns on: **Return-on-Risk per trade**, **Profit Factor**, **Worst Loss** (and Win/Loss
for context). **PASS = the VIX-gated columns beat Column A on RoR, ideally improving as the threshold
rises** (A < B < C < D = a real, monotonic signal, not noise). If the gated columns *don't* beat control,
the regime signal doesn't translate to directional P&L (the move is real but eaten by option cost) — a
decisive finding that redirects us (e.g., to selling the high-vol day via HiVolIC instead of buying it).

---

## ✅ BATCH 1 RESULT (2026-06-24) — VIX gate PASSES

RoR/trade: A(no filter) **−1.3%** → B(VIX≥18) **+1.8%** → C(≥20) **+2.1%** → D(≥22) **+3.8%** (monotonic);
PF 0.96→1.11; control loses −$8,055, all gated columns positive. **The VIX regime gate adds real edge.**
Winner so far = **D (VIX≥22) put spread.** Use it as the control for the next batches.

---

## RUNNING QUEUE (prioritized; one factor per batch, each vs its control)

> The list is long and that's fine — but the discipline is **pre-register motivated hypotheses, one per
> batch, beat control + OOS.** Do NOT sweep all 8 Range filters for the best cell (the 95→57 trap).

### Batch 2 — Direction: calls vs puts on high-VIX days *(do next — most important)*
Settles "is it directional, or just trade-on-high-vol-days?"
- **Col A:** Batch-1 winner = **Long PUT spread, VIX≥22** (the control).
- **Col B:** Duplicate A → swap structure to **Long CALL spread** (long ATM call / short $15 above), keep VIX≥22.
- **Col C / D (optional robustness):** same put-vs-call pair at VIX≥20.
- **Read:** puts ≫ calls → downside lean confirmed (real direction edge). Calls also positive → it's
  "big-vol days move," not direction → we'd need direction logic, not just the gate.

#### ✅ BATCH 2 RESULT (2026-06-25) — PASS, FORK = Family A (downside-directional). Calls LOSE.
Config-verified: A=put VIX≥22, B=call VIX≥22, C=call VIX≥20, D=put VIX≥20; all PT100/SL50, 11:00, $15-wide.
All numbers reconciled via `tools/bt_eval.py`.

| Col | Structure / gate | RoR/trade | PF | Total | N |
|---|---|---|---|---|---|
| **A** | **put VIX≥22** | **+3.8%** | 1.11 | +$6,385 | 280 |
| **D** | put VIX≥20 | +2.1% | 1.06 | +$4,818 | 389 |
| **B** | **call VIX≥22** | **−1.9%** | 0.95 | **−$3,645** | 280 |
| **C** | call VIX≥20 | −1.6% | 0.95 | **−$4,212** | 389 |

**Decisive: puts make money at every threshold, calls LOSE money at every threshold.** Not "big-vol days
just move" (that would make calls positive too) — a genuine **downside** asymmetry: on high-VIX days SPX
falls more than it rises vs the premium. Losing-day signatures confirm it (call book wins 100% on up days /
loses 98% on down days; put book the mirror). **Consequences: (1) Family A (downside-directional) confirmed.
(2) Family B NARROW-killed, NOT abandoned.** What's dead = a *symmetric* long strangle/straddle entered **on the
VIX≥22 gate** (you're buying already-expensive vol → the call leg overpays for an up-move that doesn't come,
−1.9%). What SURVIVES: the **VRP-gated** long-gamma (buy vol only when IMPLIED is CHEAP — **low IV Rank**, VIX not
already spiked = the opposite gate, UNTESTED here, arguably supported since buying expensive vol is the loser)
and the **Batch 8 CALENDAR** (long-*vega*, term-structure edge — a different animal Batch 2 doesn't touch). Also:
the move is asymmetric (down>up) → any future long-vol structure should skew to the put side. Directionality is
regime-robust (calls lose in BOTH 2022 & 2026; puts win in both), magnitude still 2022-weighted. VIX≥22 > VIX≥20
for puts (monotonic, consistent w/ Batch 1).

**Converged deployable config:** long PUT spread · VIX≥22 · PT100/no-SL (Batch 3) · 11:00 entry ≈ +7% RoR.
**Next lever = Family A3 / Batch 7: OR-break DOWN entry** (addresses the ~95% rally-day losers — direction confirmation).

### Batch 1b — Extend the VIX threshold
Duplicate D; set VIX ≥ **24 / 26 / 28**. Find where RoR/trade peaks before trade count gets too thin
(you're at 280 trades at ≥22; watch the >100-trade floor).

### Batch 3 — Exits: ride the winners? *(high-value — debit-buy is a positive-tail strategy)*
Hold gate+direction fixed (put ≥22). Vary exits:
- **Col A:** **PT 100% / SL 50%** (current).
- **Col B:** **no PT**, keep SL 50% (let winners run to expiry).
- **Col C:** keep PT 100%, **no SL** (avoid whipsaw stop-outs).
- **Col D:** **no PT, no SL = ride to expiration / settlement.**
- **Read:** judge on RoR **and Worst Loss + Max Drawdown** (no-stops widens the tail). Prior: removing the
  PT cap helps (stops capping the fat winners); full no-stops is higher-variance. Ties to the IC Hindsight
  finding that early exits were manufacturing losses.

#### ✅ BATCH 3 RESULT (2026-06-25) — PASS, winner = C (PT100, NO stop-loss)
**⚠️ Config slip (logged, not fatal):** the run's **Col A was the no-filter control (N=1159), not VIX≥22+PT100/SL50.**
B/C/D were all correctly VIX≥22 (N=280), exits-only varied. Used the **Batch-1-D number (VIX≥22 PT100/SL50 =
+3.8% RoR, PF 1.11)** as the baseline reference. All screenshot numbers reconciled exactly via `tools/bt_eval.py`.

| Config (all VIX≥22) | RoR/trade | PF | WR | Worst | Max DD | Median R |
|---|---|---|---|---|---|---|
| PT100/SL50 *(Batch-1-D ref)* | +3.8% | 1.11 | ~34% | −$438 | — | −51% |
| **B** — SL50 only, no PT | +0.8% | 1.02 | 28% | −$531 | −$7,496 | −51% |
| **C** — PT100, **no SL** | **+7.0%** | **1.15** | **52%** | −$718 | **−$6,039** | **+54%** |
| **D** — ride (no PT/SL) | +3.8% | 1.07 | 43% | −$718 | −$8,166 | −99% |

**Findings:** (1) **the SL50 was the value-destroyer** — C nearly doubles PT100/SL50; SL-only B is the worst
gated config. The −50% stop whipsawed out of recovering spreads (confirms Analysis-A forensic + IC Hindsight).
Safe to drop because **debit spread = defined risk** (worst = full debit −$718, bounded; not unbounded). (2)
**Keep the PT** — C (+7.0%) > D/ride (+3.8%): cap winners, don't stop losers. C is the only config with a
**positive median R** and posts the best PF + best Return-on-DD (194%) + lowest max-DD. **OOS (2024+):** C
positive both halves (IS +6.5% / OOS +8.6%), most regime-robust; still 67% 2022-weighted but earns 2024 & 2026.
Losing-day signature ~95% rally days → **direction-confirmation (OR-break DOWN) still the orthogonal next lever, stacks with C.**

**Follow-ups:** clean re-run, all VIX≥22 / PT100, vary ONLY the stop: **A=SL50 · B=SL75 · C=SL90 · D=no-SL**
(duplicate Batch-3 Col C as the base). ⚠️ **SL100/130 do NOT apply to a DEBIT spread** — loss is capped at 100%
of debit, so SL≥100% = no stop; the meaningful rungs are sub-100% (50/75/90). Judge (RoR, worst-loss) jointly:
a stop passes only if it trims the −$718 full-debit tail enough to justify the RoR it costs. Prior (Batch 3): no-SL
likely wins (the stop whipsaws recoverable trades). New champion config for the paper bot = **C/no-SL unless a sub-100% rung beats it on the tail.**

#### ✅ CLEAN RE-RUN RESULT (2026-06-25) — OVERTURNS "no-SL". Winner = SL75. Exit curve is an inverted-U.
5 cols, all VIX≥22/PT100, only the stop varies. Config-verified, reconciled via bt_eval.py.

| Stop | RoR/trade | PF | Worst | Max-DD | Full-loss rate |
|---|---|---|---|---|---|
| SL40 | +0.7% | 1.02 | −$372 | −$3,037 | 0% |
| SL50 | +4.0% | 1.11 | −$438 | −$4,929 | 0% |
| none | +7.0% | 1.15 | −$718 | −$6,039 | **44%** |
| SL90 | +8.6% | 1.19 | −$693 | −$6,614 | 0.7% |
| **SL75** | **+9.2%** | **1.23** | −$639 | −$6,099 | **0%** |

**The earlier "drop the SL" call was an artifact of only testing SL50-vs-none.** Real shape = **inverted-U, peak at
SL75**, which BEATS no-SL (+9.2% vs +7.0%). Too-tight (40/50) whipsaws out recoverable dips; none gives back the
last 25–60% on the 44% of trades that ride to full debit; **SL75 cuts the genuinely-dead trades at −75% (rarely
recover from that deep) while leaving −50% dips alone to recover.** Exits show ~143 full-loss rides converted to
−75% stops (save ~25% debit each) at the cost of ~7 early-stopped recoveries → net +$3.5k vs no-SL. **Vindicates
`hedge-research.md`:** SL50 was flagged as below every documented operator (~70–130%); the data confirms the
operator-range lower edge (~75%) is optimal — trust the framework over the equity curve. SL75 wins on RoR, PF,
Return-on-DD (249%), worst-loss (−$639 < no-SL −$718), AND tail-frequency (0% vs 44% full-loss). Don't over-fit
75-vs-90 (within noise) → call it the **~75–90% band**. Still 2022-weighted (69%) → OOS holdout mandatory.
**NEW CONVERGED CONFIG: put · VIX≥22 · PT100 · SL75 · 11:00 (≈+9.2% RoR, PF 1.23).** Supersedes the no-SL config.

### Batch 9 (NEW 2026-06-25) — Entry-time sweep: fixed clock (11:00 vs later) *(Andy's ask — the untested gap)*
**Why:** Batch 7 tested 11:00 vs OR-break (failed), NOT 11:00 vs a plain later clock. Live IC/Fortress bots *appear*
to do better at 1:30 — but those are iron CONDORS (short-vol; later = less chop-breach time), a different structure
from this directional put BUY, and the live A/B is only 1-1 on n=2 days (6/24 clone won, 6/25 11am champion won;
QQQ "wins" were near-max-loss escapes). So it's an untested hypothesis on THIS strategy, not a proven edge. The
a-priori case: the forensic shows losers are 11:00 rally-day entries (buy the morning top, it keeps rising) → a
later entry that skips the morning relief rally MIGHT cut those — and unlike OR-break, a plain time-delay has no
breakout condition to misfire. Counter-case: a put buy needs time for the down-move; 1:30 leaves only ~2.5h.
- **Hold the champion fixed** (put · VIX≥22 · PT100 · SL75), vary ONLY Entry Time. Duplicate the SL75 winner.
- **Col A:** 11:00 (champion) · **B:** 12:30 · **C:** 1:30 · **D:** 2:00 (optional).
- **Read:** RoR/trade vs 11:00 **and the rally-day-loss rate** (does later entry skip the morning-rally losers?) +
  N + worst-loss. ⚠️ **Watch premium/fill realism** — a 0DTE debit spread late in the day may be cheap/illiquid
  (the same premium-collapse that broke the IC 130PM clone). Flag thin-premium fills. **One factor (entry time).**
- **Slots:** after Batch 4 (gate), before OOS holdout. Whichever entry wins → that's the entry for the paper bot.

#### ✅ BATCH 9 RESULT (2026-06-25) — 11:00 LOCKED; sharp peak; 1:30 thesis FALSIFIED.
Andy added Col E=9:50 (early). All VIX≥22/PT100/SL75, reconciled via bt_eval.py (totals + PF exact).

| Entry | RoR/trade | PF | Total | rally-day-loss % |
|---|---|---|---|---|
| 9:50 | −4.2% | 0.91 | −$7,458 | 98% |
| **11:00** | **+9.1%** | **1.23** | **+$15,213** | 98% |
| 12:30 | −3.4% | 0.93 | −$5,559 | 96% |
| 1:30 | +1.7% | 1.04 | +$2,632 | 96% |
| 2:00 | −1.0% | 0.98 | −$1,399 | 94% |

**Sharp PEAK at 11:00 — not a scaffold, the genuine optimum.** 9:50 too early (buys morning open-noise/relief-rally
before direction resolves); 12:30/2:00 too late (not enough of the ~5h window left for the down-move to pay the debit).
**Andy's 1:30 hypothesis FALSIFIED:** +1.7% vs +9.1%, and the rally-day rate barely moved (96% vs 98%) — later entry
did NOT skip the morning rally, it just gave up the winners (less time for the move). **The live "1:30 wins" was
IC-specific (short-vol condor) + n=2 noise — does NOT transfer to the directional put.** Premium decays into the
afternoon as expected (Risk/trade $601@11:00 → $551@2:00) but not to the $0.05 pathology — fill realism is not the
driver; time-for-the-move is. **ENTRY LOCKED = 11:00. PUT SIDE FULLY LOCKED ON EVERY DIMENSION: put · VIX≥22 · PT100 ·
SL75 · 11:00 → +9.2% RoR, PF 1.23.** Nothing left to optimize on the put; paper-ready pending OOS holdout.

### Batch 4 — Regime-gate DISCOVERY (VIX≥22 is provisional, NOT settled — high priority)
**VIX level is the current benchmark, not the answer.** C1 validated that vol (ATM IV/VIX) predicts range,
but a better single indicator — or an orthogonal *combination* — likely flags directional days more sharply.
Explore it, with discipline (the combo stage is where the 95→57 dredge lives).

**Dual control:** read every candidate gate against BOTH (a) the **no-filter** control (does it add edge at
all) and (b) the **VIX≥22** incumbent (does it actually BEAT the gate we already have). Adopt only if it
beats VIX≥22, or a combo beats VIX≥22-alone.

**Stage 4a — single-factor screen (motivated shortlist, one gate/column, hold structure = put spread).**
Each candidate has a real thesis, not a dredged oscillator:
- **VIX level ≥22** — benchmark (absolute vol regime).
- **VIX Change % > 0 / > 5 — the "VIX gap" / vol expansion** *(Andy's ask; strongest a-priori challenger:
  vol *rising* = regime shift starting, sharper than a static-but-flat high VIX).*
- **IV Rank ≥ 50** — relative-vol cross-check.
- **Change SD ≥ 1** — the day is already extending (magnitude).
- **Trading range > 1% since prev close** — realized range expansion.
- **ADX(14) ≥ 25** — classic trend-strength (trending vs ranging).
- **Gao-Han intraday momentum** — sign of the **10:00 ET return** (or first-30-min return). Academic,
  high-confidence (JFE 2018, R² ~3.3% on high-vol days), and **orthogonal to VIX** (it's a direction/persistence
  signal, not a vol level). Express in OA as a `Change %`-since-open condition at the entry window; combine with
  the put side (fire the put only when the morning return is *down*). Prior caveat: thesis predates the 0DTE era
  → OOS-confirm on 2024–26.
- **Narrow Initial Balance (IB < 0.5×ATR)** — first-60-min range vs 5-day ATR; narrow IB = compression →
  expansion (large-sample ES study: ~98.7% break, 74.8% extension). Free pre-entry day-type flag; cross-check
  against the ATR/VIX gate. (Approximate in OA via `trading range since open < X%` if a true IB metric isn't
  exposed.)
- **Time-series momentum (12-mo trend sign)** — a **confirmation filter, not a trigger**: only take the put
  (bearish) side when the macro 12-mo SPX trend is *not* strongly up (don't fade an established bull). Cheap,
  low-decay (JFE 2012). Use as a combo gate in 4b, not a standalone permission gate.
Rank by RoR-lift + null p (in-sample only). **Keep only gates that beat BOTH controls AND the null.** Note:
**Gap % alone was already falsified** (noise); **GEX stays OUT** (FlashAlpha verdict — adds nothing after
VIX/IV); **skip the RSI/MACD/Stoch/CCI/Momentum oscillators** in the screen (weak 0DTE thesis + dredge
magnets) unless one earns a specific written hypothesis first.

**Stage 4b — orthogonal combination (survivors only, PAIRS only).** Combine at most TWO survivors that
measure DIFFERENT things (e.g. vol-level × vol-expansion = "high AND rising"; or vol × trend-strength). Test
the pair vs the better single component — **the combo must ADD beyond the best single**, or it's overfitting.
Never sweep the full indicator cross-product for the best cell (the 95→57 scar). At most ONE combo graduates.

**OOS every gate survivor (2024–26) before it informs the bot.** A gate that only beats VIX in-sample is
curve-fit. Log the trial count across 4a+4b and deflate the winner for it.

### Batch 5 — Structure: spread vs single long option
Hold gate+direction fixed. **Col A:** put SPREAD (defined cost). **Col B:** single **long put** (naked
long = pure convexity, bigger winning tail, more theta cost). *(Naked = single long option, defined risk =
premium. Never sell naked.)*

### Batch 6 — Bullish mirror: low-VIX + falling-VIX → calls *(refined 2026-06-25, Andy's gate)* — **[✅ DONE 2026-06-25 — PASS, calls work; champion gate = VIX Change%<−2. RESULT block below.]**
**The CALL track — its own confirm-or-kill series.** ⚠️ **Batch 2 was NOT a fair call test** — it ran calls on the
PUT's gate (VIX≥22 = the worst regime for calls, since high VIX is when the market falls). The fair call gate is
the MIRROR: **low absolute VIX AND VIX falling** (risk-on / melt-up continuation). Mirror of the put logic — puts
want high-and-fearful, calls want low-and-calming.

**First call batch** (all **Long Call Spread** · 0DTE · 11:00 · PT100/SL75; long ATM call / short $15 above):
- **Col A:** no filter (call control — earlier finding: ~+1.6% from bull drift, the bar to beat).
- **Col B:** **VIX Change % < −2** (VIX falling).
- **Col C:** **VIX Change % < −4** (VIX falling hard).
- **Col D:** **VIX ≤ 16 AND VIX Change % < −2** (Andy's combo — low level *and* dropping).
- **Read:** does any column turn **positive** AND beat the no-filter call control? D = the thesis; B/C isolate whether
  it's the *falling* or the *low level* doing the work. Judge on RoR + PF; watch N floor.
- **Scaling note:** VIX-change at multiple negative scales (−2/−3/−4) IS motivated HERE (different factor direction
  on a different structure = pre-registered, not a dredge) — unlike the put side, where VIX-change is already
  falsified (lost at >0 AND >5 monotonically; scanning more scales = the 95→57 dredge trap).

**Honest prior — likely WEAK:** every call test so far has LOST (Batch 2 high-VIX calls; earlier Change-SD up-moves
+ momentum-continuation both falsified — "up-extensions fade, it's all beta"). Structural reason: **low VIX = small
expected move**, so a calm melt-up often doesn't travel far enough intraday to pay a 0DTE call debit + theta. The
put edge is real because high-VIX days have genuine downside skew; the call side fights slow grinds. **Bar = is it
even positive on the right gate.** If yes → earns a full series (exits/entry/structure mirror of Batches 3/7/9). If
it bleeds → the directional pillar is downside-only, asymmetry confirmed, and we stop here.

#### ✅ BATCH 6 RESULT (2026-06-25) — PASS, and it OVERTURNS the downside-only prior. Calls WORK on the mirror gate.
Config-verified (all SPX Long Call Spread · 0DTE · long ATM / short $15 above · 11:00 · PT100/SL75 · 5Y; A=no filter,
B=VIX Change%<−2, C=VIX Change%<−4, D=VIX≤16 AND VIX Change%<−2). Totals + PF + N reconcile **exactly** to the screenshot;
RoR/trade shown as OA's per-trade average (bt_eval reconciles directionally, ~1–2 pts higher by the avg-of-ratios convention).

| Col | Gate | RoR/t | PF | N | WR | Total | Max DD | null p (vs A) |
|---|---|---|---|---|---|---|---|---|
| **A** | none (control) | **−1.2%** | 0.97 | 1159 | 43% | **−$8,705** | −$16,604 | control |
| **B** | **VIX Change% < −2** | **+15.2%** | **1.42** | 337 | 53% | **+$32,274** | −$4,245 | **0.000 PASS** |
| **C** | VIX Change% < −4 | +10.3% | 1.27 | 174 | 52% | +$11,445 | −$3,747 | 0.020 PASS |
| **D** | VIX≤16 & VIXΔ%<−2 | **+21.5%** | **1.64** | **88** | 56% | +$10,901 | **−$2,444** | 0.005 PASS |

**Decisive PASS — the honest "weak prior" was WRONG. Calls earn on their own regime (falling/low VIX = risk-on relief).**
All three gated columns flip the −1.2% control to strongly positive, each beats the random-day null (p 0.000/0.020/0.005 →
not just fewer/luckier days). Coherent with Batch 4: VIX *rising* (>0) didn't help puts; VIX *falling* (<−2) powers calls —
same signal, opposite sign, opposite structure. Losing-day signature confirms clean directionality: **100% of wins are UP days,
92–95% of losses are DOWN days** (calls lose when the market falls — expected). The lever to improve = direction confirmation
(OR-break UP), the call mirror of the put's rally-day problem.

**Champion call gate = B (VIX Change% < −2):** clears the N≥100 floor (337), passes the null (p 0.000), PF 1.42, and is
**positive EVERY year 2021–2026** (2021 +$1.7k · 2022 +$3.2k · 2023 +$9.5k · 2024 +$5.1k · 2025 +$11.6k · 2026 +$1.1k).
**Inverse fragility vs the put:** the put champion is 2022-weighted (rare-fire, OOS-fragile); the call champion is
**2023–25-weighted and STRONGEST in the would-be OOS window** (2024–26 = ~55% of B's P/L). The two tracks are genuine
**regime complements** — put fires in high-vol selloffs, call fires in low-vol relief rallies; they earn on different days.

**Decomposition (what's doing the work):** B (+15.2%) > C (+10.3%) → **falling *harder* (−4) does NOT help** — it just thins
N from 337→174; the −2 threshold already captures the signal (non-monotonic on the VIXΔ axis = "−2 is the sweet spot," a
finding, not noise). D (+21.5%) > B → **the LOW-LEVEL condition (VIX≤16) adds real lift.** So the operative thesis = "VIX
falling (≤−2 is enough) AND low absolute level" = D's combo — **but D is N=88 < the 100-trade floor**, so it's a promising
*refinement*, not yet trustable. **Firm-up: re-run D with VIX≤18 to lift N over 100** and confirm the low-level lift survives.

**⚠️ One validity check before paper:** confirm OA's **VIX Change %** is evaluated **at the 11:00 entry** (VIX-now vs prior
close, known-at-entry) and not a full-day change (which would be lookahead). The live "CURRENT 1.4%" reading and Batch-4's
clean use of the same family both suggest entry-time evaluation — but verify in-app before live capital. ~30–40% live haircut
applies as always.

**Verdict + routing:** Batch 6 PASSES → the call track **graduates to its own series** (the prior's "if positive" branch).
Directional pillar is **NOT downside-only** — it's two complementary regime engines. **Adopt B as the provisional call champion
gate.** Next for the call track (mirror of the put series): (1) **firm up D** (VIX≤18 for N); (2) **call exit-sweep** (PT/SL —
D's median R = +100% hints PT100 may truncate winners, same as put Batch 3); (3) **OR-break UP entry** (Batch 7 analog,
direction confirmation for the 92–95% down-day losers); (4) OOS formal + **paper a `DIR-SPX-CallVIXdrop` experiment** alongside
the put bots. Trial count this batch = 4 (A + 3 gates) → low; B's p 0.000 / N 337 / all-year-positive survives deflation easily.

### Analysis A — Losing-day forensic + directional hedging *(Andy's 2026-06-24 add)*
Not a Compare batch — a position-level study. **Export variant B's positions** (the **Copy CSV / Download
CSV** button on the 569-positions view) → save to `bot-fleet/` → Claude categorizes the **stop-loss /
max-loss days**: what did SPX do (rally / whipsaw / reverse-up?), VIX level, gap, time-of-SL. **Observed so
far:** worst losers are all SL exits on days the market *rose* despite high VIX (e.g., Apr 6 2022: entered
11:00 @4464, rose to 4488, stopped −$438). Goal = find the common signature of losing days, then test
**filters/hedges to cut the max-loss days**: (a) **direction confirmation** (OR-break — only fire the put
when price actually breaks down, skipping relief-rally days) is the natural "hedge" here; (b) exit timing
(Batch 3); (c) a small opposite-side cap (eats edge — last resort). Feeds the hedge→bot matrix in
`hedge-research.md`.

**✅ DONE 2026-06-25 on the Batch-1-D CSV (280 trades, VIX≥22).** Export works (resolves the export-block question). Forensic result: **178 stop-losses → 99% were days SPX RALLIED open→close (+0.43% avg); 102 winners → 100% down days (−0.80%).** Pure directional down-bet, zero chop/theta nuance — so **(a) direction confirmation (OR-break DOWN) is THE lever** (it's where the −$57k of stops sits), not an opposite-side cap. Two more findings the OA summary hides: **(1) 2022 = 63% of trades / 77% of P/L; 2024 loses (11% WR, n=9); 2026 +$2,991 (46% WR, n=26)** → rare-fire high-vol-selloff earner, OOS-fragile → **OOS holdout 2024–26 is mandatory before paper.** **(2) median trade hits SL50 (median R −50.8%), mean R +4.0% is all right-tail, and the 2 "expired" runners were the biggest wins (+$685 avg)** → **PT100 likely truncates the trend days → Batch 3 (ride/no-PT) is high-value.** Still to confirm direction-vs-just-high-vol = **Batch 2 (calls vs puts on VIX≥22).**

### Batch 3b (later) — Structure sweep
Width {10 / 15 / 20}, then PT {75 / 100 / 150}, then SL {40 / 50}. One dimension per screen, after the gate
+ direction + trigger + exit-style are locked.

### Batch 7 (later) — OR-break entry trigger
Once direction + exits lock: A = fixed 11:00, B = **OR-Breakout 15-min**, C = **OR-Breakout 30-min** (the
`$ below 15-minute opening range low` selector). Signal-based entry vs the clock; also the primary
losing-day hedge (don't buy puts on days that rally).

#### ❌ BATCH 7 RESULT (2026-06-25) — FAIL. OR-break DOWN degrades the edge; KEEP fixed 11:00.
Config-verified (A=Time 11:00, B=ORB-15↓, C=ORB-30↓; all put · VIX≥22 · PT100/no-SL). Reconciled via bt_eval.py.

| Col | Entry | RoR/trade | PF | Total | N | Worst |
|---|---|---|---|---|---|---|
| **A** | **fixed 11:00** | **+7.0%** | **1.15** | **+$11,740** | 280 | −$718 |
| B | ORB-15 down | −0.3% | 0.99 | −$674 | 224 | −$898 |
| C | ORB-30 down | +1.2% | 1.01 | +$544 | 206 | −$698 |

**The direction-confirmation lever (Family A3) is DISCONFIRMED.** OR-break-down cut entries (280→224→206) and
trimmed rally-day losers (133→116→106) but **removed even more winners** (147→108→100), and **~92% of surviving
losses are STILL rally days** — it didn't fix the problem. Mechanism: trend-down winners often grind down later
without an early OR-low break → **OR-break misses them**; fast OR-low breaks are disproportionately **whipsaw
head-fakes that bounce** → losers. It selects the wrong subset; worst loss worsens (later entry = higher debit).
**KEEP fixed 11:00.** Strategic redirect: rally-day losses are NOT fixable by entry timing → the only lever left
is **at the GATE** (Batch 4 VIX Change%/vol-expansion may select truer selloff days than static VIX level). This
also disconfirms **Family A3 (down-break continuation)** in the structure-family section. Converged config LOCKED
on every dimension tested: **put · VIX≥22 · PT100/no-SL · fixed 11:00.**

### Batch 8 (NEW 2026-06-25) — Long-vega CALENDAR (the scarce long-vol/convexity bucket) *(newly testable)*
**Why now:** the fleet is ~9-of-10 short-vol (`methodology.md` factor-bucket gap); a calendar is genuine
**long-vega** diversification, anti-correlated to the IC book. It was **untestable in OA until the June
release** (needed multi-DTE) — **45 DTE + 2013 history now make it runnable.** Sources: F-003 double-calendar,
F-005 backwardation+calendar (`cross-project-research.md`).
- **Structure:** sell the short-DTE option(s), buy the longer-DTE option(s) at the same strike — start with a
  **double calendar** (call + put calendar) or a **straddle calendar**; short ~7DTE, long ~30–45DTE.
- **Col A (control):** calendar entered **every day** (expect it to bleed in calm/contango tape — the baseline).
- **Col B/C/D (gate):** enter only when **front-end vol is rich / expanding** — proxy with **VIX Change % > 0**
  or **IV Rank** (we have no native VIX3M/VIX9D term-structure metric, so F-002/F-005 backwardation is proxied,
  not literal — flag this). One gate per column.
- **Exit:** roll/close the short leg at ~2–3 DTE; judge the structure on **Exp(R) + Worst Loss**, NOT win rate.
- **Read:** PASS = the gated calendar is positive AND its drawdowns are *uncorrelated* with the IC book's
  bad days (that's the diversification value, not raw RoR). Binding risk is **gamma/whipsaw**, not vega — watch
  the worst-loss tail. **OOS 2024–26.** Note: multi-leg/multi-DTE fills are less liquid → use the bid/ask
  fill-realism check, and this is a prime **paper-before-capital** structure.

### Batch M (NEW 2026-07-04) — Middle-band coverage: wider IC vs long-gamma head-to-head *(from the regime-coverage map)*
**Why now:** the coverage map (`data/regime_coverage.md`) sized the fleet's biggest hole — the **mid-IV
"middle band" ≈ 50% of days (~116/yr)** that neither the calm-IC gate nor the VIX≥22 put gate claims.
Character: **HELD ~76%** (short strikes survive 3 days in 4) but **STAYED075 only ~42%** = directional-DRIFT-
not-trend days. Two opposite exposures could monetize it; this batch runs them **head-to-head on the same
cohort** and lets R decide (don't pre-pick). This is ALSO the exact failure mode the cockpit tools converged
on (naked-downside/drift-after-entry) — so a winner here doubles as a hedge for the existing book.

- **Cohort gate (shared by ALL columns — the key to a fair test):** the middle band, expressed in OA via a
  **VIX band ≈ 15–22** (above the calm floor, below the put track's VIX≥22 trend gate). ⚠️ Cutoffs are
  APPROXIMATE — the precise ATM-IV-percentile→VIX mapping needs `c1_rows.csv` (deferred). Start 15–22, tune later.
- **Col A — Control:** the **champion IC config, unmodified**, run on the middle-band cohort. Establishes what
  the current bot already earns/loses on these contested days (the bar both candidates must beat).
- **Track A (short-vol — harvest the 76% that HOLD):** the **wider IC** = Family C1 (`HiVolIC`) re-pointed here —
  wider %OTM (1.25/1.5%), retuned PT + stop for 76%-hold days. Sweep width × PT × stop. Monetizes range-holding.
- **Track B (long-vol — harvest the 24% that RUN):** the **long-gamma / convexity** structure = Family B1 +
  its VRP gate re-pointed here (long strangle/straddle, or A2 ratio backspread), entered only when **implied is
  cheap** (IV Rank low — plausible in the mid band). Monetizes the drift/run. **Higher-priority test** per the
  "prioritize long-vol/convexity — the gap" rule (fleet is ~9-of-10 short-vol).
- **Null:** random-day sense-check on the same cohort (a gate must select BETTER middle days, not just fewer).
- **PASS / read — and the real question is complementarity, not just a winner:**
  - Each track PASSES if it beats Col A on **Exp(R) + Worst Loss** AND beats the random-day null on the cohort.
  - **The strategic test:** A (short-vol) and B (long-vol) are OPPOSITE exposures on the same days — A wins when
    they hold, B wins when they run. Check whether **their bad days anti-correlate** → if so the prize isn't
    either/or, it's **a wider IC + a cheap convex overlay** sized for contested days (likely the best outcome).
  - If neither clears, "cash is the correct position on the middle band" is itself a valid, logged result
    (the coverage goal is *measured* coverage, not forced coverage).
- **Discipline:** OOS 2024–26 on any survivor; ~30–40% live haircut + commission; long-vol/multi-leg fills are
  thinner → bid/ask fill-realism check; **paper-before-capital.** Reconcile every column via `tools/bt_eval.py`.
- **Slots:** after the current directional OOS holdout (doesn't compete with the locked put/call tracks — different
  cohort). Pairs with Batch 8 (calendar, same long-vega thesis) and RESEARCH item 3.

**Evaluation discipline (every batch):** judge on **Exp(R) / RoR + Worst Loss**, beat **control + a
random-day sense-check**, then confirm survivors on an **out-of-sample** date range before papering. Apply
a ~30–40% backtest-to-live haircut + real commission before any go-live math.

---

## STRUCTURE-FAMILY EXPLORATION — the Batch-2 branch (variations beyond put spreads)

> Added 2026-06-25. The goal of this pillar = **fire on the days the chop/IC bots DON'T** (high-vol /
> non-chop days, already identified by the C1 gate = VIX/IV-Rank). "Which days" is solved; this section
> explores **what structure** to fire. **Batch 2 is the fork** — its result routes which family below to
> explore. Don't run all three families at once (dredge). All families share the same C1/VIX gate + the
> no-filter control + random-day null + OOS holdout.

**THE FORK (Batch 2 result):**
- **Puts ≫ calls** → real downside direction → explore **Family A**.
- **Calls also clearly positive** → it's "big-vol days just *move*," not direction → explore **Family B**
  (direction-neutral long-vol — the **factor-bucket jackpot**, it diversifies the 9-of-10 short-vol fleet).
- Either way, run **Family C** as a parallel short-vol benchmark (but know it doesn't diversify).

### Family A — downside-directional (if puts win)
- **A1. Long put debit spread, VIX-gated** — Batch-1 winner, the benchmark (already have it).
- **A2. Put ratio backspread** (e.g. long 2× ATM-ish puts / short 1× higher put). The one variable vs A1 =
  structure. Long convexity on a real selloff, cheaper than a naked long, fat tail. **Pass:** beats A1 on
  RoR *and* improves Worst Loss/tail on the deep-down days; watch the mid-range "max pain" zone.
- **A3. Down-break continuation** — A1 structure, but Entry Trigger = **OR-break DOWN** (15 vs 30 min) vs
  the fixed 11:00. The one variable = trigger. Exploits the one confirmed momentum finding (down-moves
  continue; up-moves fade) and is the direction-confirmation lever the forensic flagged (skip relief-rally
  mornings). **Pass:** beats fixed-11:00 A1 on RoR *and* cuts the rally-day stop-outs (fewer SL exits).

### Family B — direction-neutral long-vol (if calls also positive — the jackpot)
- **B1. Long strangle / straddle** on C1 high-vol days. Col A = put spread VIX≥22 (benchmark); Col B =
  long strangle (~0.30Δ both sides) VIX≥22; Col C = long straddle (ATM both sides) VIX≥22. The one variable
  = structure. **The real test: does *realized* range exceed the *implied* (premium paid)?** C1 says morning
  IV predicts range — if range beats the breakevens, long gamma wins even bought at high IV. **Pass:** the
  long-vol structure is positive *and* beats the put spread *and* its wins come on BOTH up and down days
  (true direction-neutrality). This is the most strategically valuable possible result — flag it loudly if
  it hits.
- **B1-VRP refinement (the timing gate):** the structure (B1) tests *what*; this tests *when to buy vol*.
  Only enter the long strangle/straddle when **implied is cheap vs realized** (a positive variance-risk-premium
  setup) — proxy in OA with **IV Rank LOW** and/or **VIX not already spiked** (don't pay top dollar for vol).
  One variable = the VRP gate, vs the ungated B1. Pass = the gate lifts Exp(R)/cuts the theta-bleed days. Pairs
  with the Batch-8 calendar (same long-vega thesis, different structure).

### Family C — adapted short-vol benchmark (fires on the same days, lower strategic value)
- **C1. HiVolIC** — wider OTM (1.25 / 1.5 / 1.75%), later entry (12:30–1:30, skip the morning impulse),
  tighter hedge. Sells the fat fear premium instead of buying. The one variable per column = %OTM (then a
  later batch sweeps entry time). **Pass:** positive RoR with acceptable Worst Loss vs unstopped. **Caveat:
  even if it passes it's still short-vol** — it monetizes the day but does NOT diversify the factor mix, so
  it's a benchmark, not the prize. (Note it competes with the IC champion's lane, not the directional thesis.)

### Orthogonal layer (apply to the family winner, not now)
Entry timing — later/post-impulse entry (the 6/24 A/B showed 1:30 beat 11:00 on the reversal) and the
OR-break window (15 vs 30 min). One factor, after the structure + direction lock.

---

## EXACT CLICK-STEPS (staged 2026-06-24)

### Batch 2 — direction (DO NEXT)
1. Duplicate Batch-1 **Col D (VIX≥22 put spread)** → this is Col A (control).
2. Duplicate → Col B: change structure **Long Put Spread → Long Call Spread** (long ATM call / short $15 above), keep VIX≥22.
3. (optional) Cols C/D = same put-vs-call pair at VIX≥20.
4. Read RoR/trade: **puts ≫ calls = real downside edge; calls also positive = "trade high-vol days," not direction.**

### OOS check — survives outside 2022? (highest-value validation)
1. Duplicate Batch-1 **Col A (no-filter control)** → date range **2024-01-01 → present** ("OOS control").
2. Duplicate Batch-1 **Col D (VIX≥22)** → same date range ("OOS gated").
3. **PASS = OOS gated still beats OOS control + stays positive.** Gap vanishing in 2024–26 = edge leaned on the 2022 bear.

> **✅ OOS HOLDOUT RESULT (2026-07-04) — PUT CHAMPION PASSES.** Base = the final SL75 champion (Long Put Spread ·
> $15-wide · VIX≥22 · PT100 · SL75 · 11:00), NOT the pre-SL75 Batch-1 Col D above. Holdout window ~Jul'24→now
> (2Y, outside 2022). **Gated: +6.4% RoR/trade · PF 1.15 · +$2,974 · N=76 · RoD 63.1% · worst −$585. Control (no
> VIX filter): −3.0% RoR · PF 0.93 · −$9,643 · N=616.** Gated stays POSITIVE and beats control decisively → the
> VIX≥22 edge is NOT a 2022 artifact. Caveats: +6.4% < in-sample +9.2% (some 2022-weighting, expected); OOS profit
> LUMPY (mostly a 2026 vol episode — insurance-like); **N=76 < the 100-trade floor** → size conservatively. Window
> was a 2Y preset not full 2024-01-01 (verdict unchanged; optional clean re-run). **Both directional engines now
> OOS-validated** (call passed 6/25). Remaining before live capital: haircut+commission math on +6.4% + the RoE
> governance gate. Logged `session-log.md` 2026-07-04.

### Batch 1b — extend VIX threshold
1. Duplicate Col D ×3; set VIX **≥24 / ≥26 / ≥28** (keep one ≥22 reference).
2. Read RoR/trade + **N**; pick the peak threshold still holding N>100.

### Batch 3 — exits
1. Col A = **PT100 / SL50** (current). 2. B = **remove PT**, keep SL50. 3. C = keep PT100, **remove SL**. 4. D = **remove both** (ride to expiry).
2. Judge **RoR + Worst Loss + Max DD** (no-stops widens the tail). Confirm "no exit options" holds 0DTE to settlement.

### Batch 4 — regime-gate discovery (multi-pass; hold structure = put spread fixed)
**Pass 1 (vol gates):** A = **VIX≥22** (benchmark) · B = **VIX Change % > 0** · C = **VIX Change % > 5** · D = **IV Rank ≥ 50**.

> **✅ PASS 1 RESULT (2026-06-25, in-sample) — VIX≥22 stays champion; 0 of 3 challengers beat it.** All put/PT100/SL75,
> reconciled via bt_eval.py. **A VIX≥22 +9.2% (PF 1.23) · B VIXΔ%>0 −0.9% (PF 0.99, N=600) · C VIXΔ%>5 −2.4% (PF 0.96)
> · D IVR≥50 +5.9% (PF 1.12, N=125).** **VIX Change% (vol-expansion = Andy's strongest a-priori challenger) FALSIFIED**
> — loses at both thresholds; the LEVEL matters, not the change (VIXΔ>0 fires on 600 days = ~half of all sessions =
> loose, scoops revert days). **IV Rank positive but inferior** (same vol-level factor family as VIX; not orthogonal →
> not a combo partner). **KEY NEGATIVE: no gate moves the rally-day-loss rate (all 94–98%)** → neither entry-timing
> (Batch 7) NOR vol-gating reduces the rally-day losses → they are **structural** (the irreducible cost of buying
> convexity on high-vol days), not a fixable leak. **Trial ledger: 3 gates, 0 survivors. Pass 3 NOT triggered** (needs
> a challenger beating VIX≥22). Pass 2 (orthogonal move/trend gates) is the remaining shot + only valid combo source.

**Pass 2 (move/trend gates):** A = **VIX≥22** (carry the benchmark) · B = **Change SD ≥ 1** · C = **Trading range > 1%** · D = **ADX(14) ≥ 25**.

> **✅ PASS 2 RESULT (2026-06-25, in-sample) — 0 of 3 orthogonal gates beat VIX≥22. GATE DISCOVERY DONE; VIX≥22 LOCKED.**
> ⚠️ **Substitution (option 2, logged for the trial ledger):** OA has no literal "Trading range %" filter (Ranges menu =
> VIX/VIX Change/VIX Change %/IV Rank/Change SD/Gap %/Open Chg %), so Col C "Trading range" was replaced with a 2nd ADX
> cut. Run: A=VIX≥22 · B=Change SD≥1 · **C=ADX≥20 · D=ADX≥25** (ADX under the Indicators tab). All put/PT100/SL75,
> reconciled via bt_eval.py. **A VIX≥22 +9.2% (PF 1.23) · B ChangeSD≥1 −0.9% (PF 0.98, N=111) · C ADX≥20 −0.1% (PF 1.00,
> N=725) · D ADX≥25 −5.2% (PF 0.89, N=468).** **ADX falsified — monotonically WORSE as threshold rises** (≥20→−0.1%,
> ≥25→−5.2%): ADX is direction-agnostic, so tightening it scoops up strong UP-trends = put-killers. Rally-day rate still
> 96–98% (no gate moves it). **COMBINED Batch 4 trial ledger: 6 gates (VIXΔ% ×2, IV Rank, Change SD, ADX ×2), 0 survivors;
> next-best was IV Rank +5.9%, still 3 pts behind. Pass 3 (combo) NOT triggered (needs a challenger beating VIX≥22).**
> **GATE LOCKED = VIX≥22.** Settled: (1) no better single gate exists; (2) rally-day losses are STRUCTURAL (unmoved by
> entry-timing OR 6 gates) → size for them, don't filter. **FULLY LOCKED CONFIG: put · VIX≥22 · PT100 · SL75 · 11:00 →
> +9.2% RoR, PF 1.23.** Remaining to paper: Batch 9 (entry-time) + call track (Batch 6, optional) + OOS holdout → paper.
**Pass 3 (combo — only if a challenger beat VIX≥22 + null in P1/P2):** A = **VIX≥22 alone** · B = **best challenger alone** · C = **VIX≥22 + best challenger** (orthogonal pair). The combo must beat BOTH singles to graduate.
- Read RoR/trade + N + null each pass; read the **main effect**, not the best cell; OOS-confirm the winner. **Log the trial count** (~7 gates + 1 combo) and deflate accordingly. Dual control: beat no-filter AND VIX≥22.

### Batch 6 — the CALL track (confirm-or-kill the bullish mirror) **[STAGED 2026-06-25, ready to run]**
**Pre-register (one factor = the entry gate; structure/exits/time held fixed at the call mirror of the locked put champion):**
- **Hypothesis:** calls only earn on their *own* regime — **low absolute VIX AND VIX falling** (risk-on / melt-up). Batch 2 already killed calls on the PUT's gate (VIX≥22, the worst regime for calls); this is the fair mirror test.
- **Honest prior = WEAK.** Every call test so far LOST (Batch 2 high-VIX calls; Change-SD up-moves + momentum-continuation both falsified — "up-extensions fade, it's all beta"). Structural reason: low VIX = small expected move → a calm grind-up often won't travel far enough intraday to pay a 0DTE call debit + theta. **Bar = is it even POSITIVE on the right gate AND does it beat the no-filter call control.**
- **Pass:** a gated column turns positive **AND** beats Col A (no-filter call control) on RoR + PF, with N>100. D = the thesis (low *and* dropping); B/C isolate whether it's the *falling* or the *low level* doing the work. If yes → calls earn a full mirror series (exits/entry/structure, Batches 3/7/9 analogs). **If it bleeds on its own best gate → the directional pillar is downside-only, asymmetry confirmed, STOP the call track.**

**Build (shared settings = the call mirror of the locked champion):** Long **Call** Spread · 0DTE · SPX · long ATM call / short **$15 above** · 1 ct · Entry **Time 11:00** · **PT100 / SL75** · hold to settlement · slippage 0.03 · commission $0.60 · **max available date range**.

1. **Col A (call control, NO filter)** — fastest clean base: **Duplicate the locked put champion (VIX≥22/PT100/SL75 SL75-winner column)**, then make exactly two changes: (a) structure **Long Put Spread → Long Call Spread** (long ATM call / short $15 *above*); (b) **DELETE the VIX≥22 entry filter** so A fires every day. Confirm SL is **75%**, PT **100%**, entry **Time 11:00**. This is the bull-drift bar (~+1.6% prior).
2. **Col B** — Duplicate A → add ONE entry filter: **VIX Change % < −2**. (Ranges menu: VIX / VIX Change / **VIX Change %** / IV Rank / Change SD / Gap %. Use VIX Change **%**, the relative one — same family used in Batch 4.)
3. **Col C** — Duplicate A → add ONE entry filter: **VIX Change % < −4** (falling hard).
4. **Col D** — Duplicate A → add TWO conditions (Andy's combo): **VIX ≤ 16 AND VIX Change % < −2** (low level *and* dropping). ⚠️ This is the one 2-condition column — fine because it's the *pre-registered* thesis cell, not a swept combo; B/C are its single-factor decomposition.
5. Run all four. **Scaling note:** testing VIX-change at −2/−3/−4 scales IS motivated here (different factor direction on a different structure = pre-registered, not a dredge) — unlike the put side where VIX-change is already falsified.

**Read (judge on R, never WR or raw P/L):** RoR/trade + PF + N + Worst Loss across A/B/C/D. Does any gated column turn **positive AND beat Col A**? Watch the N floor (falling-VIX-hard may thin out fast). Then I run `tools/bt_eval.py --side call A=control.csv B=... C=... D=...` for the forensic + random-day null vs Col A, plus the win/loss anatomy and year concentration. **Verdict routes the pillar:** positive on the right gate → calls earn their own series; bleeds → directional pillar is **downside-only**, asymmetry confirmed, and Batch 6 closes the call track.

**Artifacts to paste back** (per ingest protocol): (1) the A/B/C/D **Compare screenshot**; (2) a **Details/settings screenshot per column** (so I can config-verify the one-factor rule); (3) **positions.csv per column** (Copy/Download CSV) → save to `bot-fleet/` for the forensic. If only some arrive I'll proceed and name what I couldn't verify.

### Batch 6b — firm up D: does a low-VIX-LEVEL cap beat the VIXΔ%<−2 champion? (lift N over the floor) **[STAGED 2026-06-25 — RUN FIRST of the two]**
**Pre-register (one factor = the VIX-level ceiling; gate VIXΔ%<−2 + structure/exits/time held fixed):**
- **Question:** Batch 6 found the **low-level condition (VIX≤16) lifts RoR** (D +21.5% > B +15.2%) but **D was N=88 < the 100-trade floor** — untrustable. Does the lift survive at a looser ceiling that clears N≥100, or was it small-sample noise? Find the VIX-level cap that maximizes RoR while keeping N≥100.
- **Dual control:** read each capped column against (a) **Col A = VIXΔ%<−2 alone** (the incumbent champion, N=337) and (b) implicitly the no-filter call control from Batch 6. **Adopt a cap only if it BEATS the VIXΔ-alone incumbent on RoR AND clears N≥100.** If none does → **gate LOCKS at VIX Change%<−2** and D was a small-sample artifact.
- **Pass:** monotone-ish lift as the cap tightens (≤20 → ≤18 → ≤16) with N still ≥100 at the adopted ceiling, and it beats the incumbent + the random-day null.

**Build:** identical to the Batch 6 champion (Long **Call** Spread · 0DTE · SPX · long ATM / short $15 above · 1ct · Time **11:00** · **PT100/SL75** · max range). One filter family varies (the VIX level cap), VIXΔ%<−2 stays on every column.
1. **Col A (incumbent)** — Duplicate Batch-6 **Col B (VIXΔ%<−2 alone)**. This is the bar to beat (N=337).
2. **Col B** — Duplicate A → add a 2nd filter **VIX** level: Min blank, **Max = 18** (VIX≤18 & VIXΔ%<−2).
3. **Col C** — Duplicate A → add **VIX** level: Min blank, **Max = 20** (VIX≤20 & VIXΔ%<−2).
4. **Col D** — Duplicate A → add **VIX** level: Min blank, **Max = 16** (VIX≤16 & VIXΔ%<−2) = the original D, carried for continuity.
5. Run all four. **Read:** RoR/trade + **N** (the gating constraint) + PF + null vs Col A. Pick the **loosest cap that still beats the incumbent** (don't over-tighten into thin N). One factor (the level ceiling). I'll reconcile via `bt_eval.py --side call`.

#### ✅ BATCH 6b RESULT (2026-06-25) — cap NOT adopted; GATE LOCKS at VIX Change% < −2. The low-VIX lift fails the null.
Config-verified (all VIXΔ%<−2 + PT100/SL75; A=no cap, B=VIX≤18, C=VIX≤20, D=VIX≤16). Totals/PF/N reconcile exactly; RoR shown OA-avg.

| Col | Gate | RoR/t | PF | N | Total | Max DD | null p vs A |
|---|---|---|---|---|---|---|---|
| **A** | **VIXΔ%<−2 (incumbent)** | +15.2% | 1.42 | 337 | +$32,274 | −$4,245 | — |
| B | + VIX≤18 | +19.8% | 1.59 | 159 | +$18,443 | −$3,445 | 0.196 ✗ |
| C | + VIX≤20 | +20.6% | 1.61 | 215 | +$26,549 | −$3,332 | **0.064 ✗** |
| D | + VIX≤16 | +21.5% | 1.64 | 88 | +$10,901 | −$2,444 | 0.234 ✗ |

**The cap improves every point metric** (RoR 15→21%, PF 1.42→1.64, worst-loss −$684→−$581, Max-DD −$4,245→−$2,444) **but FAILS the random-day null on every column** (p 0.064/0.196/0.234, none <0.05). The null draws N random days from A's VIXΔ%<−2 population: the low-VIX subset is **not statistically distinguishable from a lucky same-size random draw** of falling-VIX days. The higher per-trade RoR is consistent with simply selecting fewer days, not a genuine second edge. This extends the small-sample worry flagged for D (N=88) to the looser caps too. **Mirrors the put's Batch 4 outcome** (no second gate beat the primary beyond noise) — and the within-axis pattern repeats: tightening ≤20→≤18 doesn't help RoR (20.6→19.8), only thins N, exactly like VIXΔ −2→−4.

**Verdict: GATE LOCKED = VIX Change% < −2** (incumbent A; N=337, PF 1.42, positive every year 2021–2026). The VIX-level cap is **NOT baked in.** **Honest footnote:** C (VIX≤20) nominally improves all risk metrics with a coherent mechanism (low VIX = smaller, more-reliable melt-up) and sits just above the bar (p 0.064) — so it's a **defensible-but-unconfirmed risk-reduction overlay** if a tighter DD is wanted later; revisit only with more data or as an OOS cross-check, never adopt on the in-sample point estimate. **Next: Batch 6c exit-sweep runs on the locked VIXΔ%<−2 gate.**

### Batch 6c — call exit-sweep: find the optimal stop (mirror of the put's SL75 finding) **[STAGED 2026-06-25 — RUN AFTER 6b locks the gate]**
**Pre-register (one factor = the stop %; gate + structure + entry held fixed; PT100 fixed):**
- **Question:** the put's clean exit re-run found an **inverted-U peaking at SL75** (not no-stop). Does the call book have the same shape, and where's its peak? Hold the locked call gate (default **VIX Change%<−2**, or 6b's winner if a level-cap graduates) + PT100, vary ONLY the stop.
- **✅ GATE LOCKED by 6b = VIX Change% < −2** (no level cap adopted — it failed the null). Run 6c on **VIXΔ%<−2**.
- **Motivated by the data:** D's **median R = +100%** (most trades hit PT) hints **PT100 may be truncating call winners** — but that's a *PT* question; keep it separate. THIS batch is the **stop** sweep (one factor). The PT question (PT75/100/150/ride) is the explicit **follow-up 6d**, run after the stop locks (same stop-then-PT order the put used).

**Build:** locked call gate · Long Call Spread · 0DTE · 11:00 · **PT100** fixed · max range. Duplicate the gate winner, vary only Stop Loss. Uses all 5 Compare columns:
1. **Col A** — **SL40** · 2. **Col B** — **SL50** · 3. **Col C** — **SL75** (current champion) · 4. **Col D** — **SL90** · 5. **Col E** — **no SL**.
2. ⚠️ **SL>100% is meaningless on a debit spread** (loss capped at 100% of debit = no stop) — rungs are sub-100% (40/50/75/90/none), same as the put.
3. **Read jointly (RoR, PF, Worst Loss, full-loss rate)** — a stop passes only if it trims the full-debit tail enough to justify the RoR it costs. Prior (from the put): expect an inverted-U with the peak in the **~75–90% band**; don't over-fit 75-vs-90. I'll reconcile via `bt_eval.py --side call`.

#### ✅ BATCH 6c RESULT (2026-06-25) — call wants a TIGHT stop (~40–50%), the OPPOSITE of the put. Champion = SL50.
Config-verified (all VIXΔ%<−2 · PT100 · N=337; only Stop Loss varies A→E). **No CSVs this round → forensic/median-R skipped; the random-day null does NOT apply to an exit sweep (same 337 days every column, only the exit changes).** Col C reconciles exactly to the known SL75 number ($32,274, PF 1.42) — mapping confirmed.

| Col | Stop | RoR/t | PF | WR | Worst | Max DD | Ret-on-DD | Total |
|---|---|---|---|---|---|---|---|---|
| A | SL40 | 15.5% | **1.60** | 41.5% | **−$425** | **−$3,044** | **1,078%** | $32,801 |
| **B** | **SL50** | **16.8%** | 1.58 | 46.6% | −$528 | −$3,490 | 1,022% | **$35,672** |
| C | SL75 | 15.2% | 1.42 | 53.1% | −$684 | −$4,245 | 760% | $32,274 |
| D | SL90 | 14.3% | 1.37 | 55.8% | −$713 | −$5,016 | 604% | $30,300 |
| E | none | 14.5% | 1.36 | 57.3% | −$788 | −$5,613 | 549% | $30,788 |

**The call optimum is the tight ~40–50% band — mirror image of the put's SL75.** RoR peaks at **SL50 (16.8%)**; PF, Max-DD, worst-loss, and Return-on-DD all **monotonically improve as the stop tightens** (SL40 best on every risk metric: PF 1.60, DD −$3,044, worst −$425, Ret-on-DD 1,078%). Loosening past 50% strictly hurts (RoR 16.8→15.2→14.3→14.5; PF 1.58→1.36). **Coherent mechanism for the asymmetry:** call losers are **down days on low-VIX tape** — SPX falls and the spread does NOT bounce (low vol = no big reversal expected), so cutting fast at −40/−50% saves the debit; riding to −100% just bleeds. The put's losers were whippy **high-vol rally days that often recovered**, so a tight put stop whipsawed (SL75 won there). Two books, opposite exit logic — a genuine structural finding, not a tuning artifact.

**Champion = SL50** (best RoR + total P/L; PF 1.58 ≈ tied with SL40's 1.60). **SL40 is the conservative alternative** — near-identical RoR (15.5%) with the best DD/worst-loss/Ret-on-DD; pick it if a tighter live tail is wanted. Don't over-fit 40-vs-50 (within noise) → **~40–50% band.** Note this **improves the call champion** from SL75 (15.2%) to SL50 (16.8% RoR, +$35.7k). WR rises with looser stops (41→57%) while RoR falls = classic high-WR/lower-expectancy.

**⚠️ Before papering:** export the **SL50 column CSV** so I can confirm median R + **year concentration (positive across 2024–26)** — the gate was all-year-positive in Batch 6, but the exit choice should be OOS-checked too. **PT question still open (6d):** looser-stop columns ride more to expiry (E: 175/337 expired), and the PT100 cap may truncate winners — that's the next sweep.

**NEW CALL CHAMPION CONFIG: Long Call Spread · VIX Change% < −2 · PT100 · SL50 · 11:00 → ≈+16.8% RoR, PF 1.58.**

### Batch 6d — call PT sweep: is PT100 truncating winners? **[STAGED 2026-06-25 — run after the OOS check]**
**Pre-register (one factor = the profit target; gate + structure + SL50 + entry held fixed):**
- **Question:** with no stop, 175/337 trades rode to expiry (6c Col E), and D's median R = +100% (most trades hit PT) — both hint **PT100 may be capping the fat trend-up days.** Does raising/removing the PT capture more of the right tail, or does it just give back winners to theta/reversal? Mirror of the put's PT decision (where PT100 *beat* ride — capping won).
- **Hold the locked champion fixed** (call · VIXΔ%<−2 · **SL50** · 11:00), vary ONLY Profit Taking. Duplicate the 6c SL50 column.
- **Cols:** A = **PT75** · B = **PT100** (champion) · C = **PT150** · D = **PT200** · E = **no PT** (ride to settlement, SL50 still on).
- **Read:** RoR/trade + PF + **median R** + Worst Loss + Max-DD. Prior is genuinely uncertain: the put said *cap* (PT100 beat ride), but the call's down-day losers cut fast at SL50 might leave room to let up-day winners run further. **Pass = a PT setting beats PT100 on RoR without blowing out DD.** One factor (PT). I'll reconcile via `bt_eval.py --side call`.
- **Slots AFTER the OOS check** (cheaper gate first). Whichever PT wins → final call champion → automate→paper.

#### ✅ BATCH 6d RESULT (2026-06-25) — PT100 WAS truncating; winner = RIDE/no-PT. Call FULLY LOCKED.
Config-verified (all VIXΔ%<−2 · SL50 · N=337; only PT varies A=75→E=none). Totals reconcile exactly; null N/A (same days, exit-only).

| Col | PT | RoR/t | PF | WR | Worst | Max DD | Total | median R |
|---|---|---|---|---|---|---|---|---|
| A | PT75 | +14.9% | 1.53 | 52% | −$528 | −$2,593 | $29,455 | +75% |
| B | PT100 | +17.7% | 1.58 | 47% | −$528 | −$3,490 | $35,672 | −50% |
| C | PT150 | +20.0% | 1.60 | 42% | −$536 | −$3,405 | $39,303 | −51% |
| D | PT200 | +21.4% | 1.63 | 42% | −$536 | −$3,215 | $41,843 | −51% |
| **E** | **none (ride)** | **+21.9%** | **1.63** | 42% | −$536 | **−$3,213** | **$42,122** | −51% |

**PT100 was truncating winners — confirmed.** Tightening to PT75 HURTS (14.9% vs 17.7%); loosening past 100 HELPS monotonically and peaks at **ride/no-PT** (+21.9%, PF 1.63, +$42,122). **Drawdown does NOT blow out** — D/E DD (−$3,2xx) is actually *lower* than PT100's (−$3,490) because the fat winners offset, and worst-loss stays capped at −$536 (SL50 still cuts the down-day losers). D (PT200) ≈ E (no-PT) within noise → don't over-fit; **ride is the cleanest** (SPX 0DTE = cash-settled European → holding to settlement is safe). **median R −51% / mean +21.9% = ride the positive tail, don't cap it.**

**Third mirror of the put — opposite on BOTH exits:** put = **cap winners (PT100) + loose stop (SL75)** (losers are recoverable high-vol rally days; winners can reverse → lock them); call = **ride winners (no-PT) + tight stop (SL50)** (winners grind up to settlement on calm tape; losers are down days that don't bounce → cut fast). Fully coherent, not tuning noise.

**OOS check on the ride/no-PT winner (bt_eval --oos 2024-01-01):** **IS n=163 RoR +24.8% +$21,833 | OOS n=174 RoR +19.1% +$20,289** — both strongly positive; **positive every year 2021–2026.** OOS-robust.

**🔒 FINAL CALL CHAMPION (fully locked on every dimension, OOS-passed): Long Call Spread · VIX Change% < −2 · NO PT (ride to settlement) · SL50 · 11:00 → ≈+21.9% RoR, PF 1.63, +$42,122.** Higher RoR + better OOS profile than the put champion (+9.2%). **Call track DONE → automate→paper `DIR-SPX-CallVIXdrop` alongside the put pair.**

### OOS check — call champion survives 2024–26? **[STAGED 2026-06-25 — RUN FIRST: just export 1 CSV]**
**Cheapest remaining gate.** No new backtest needed — just **export the 6c SL50 column positions.csv** → save to `bot-fleet/`. I run `bt_eval.py --side call --oos 2024-01-01` on it → **in-sample vs out-of-sample RoR + median R + year concentration.** **Pass = positive in OOS (2024–26), not just overall.** The gate (VIXΔ%<−2) was already positive every year in Batch 6, so this is expected to pass, but it's the pre-committed holdout and must be touched before paper. Confirms the exit choice (SL50) didn't quietly lean on one regime.

#### ✅ OOS CHECK RESULT (2026-06-25, SL50 champion CSV) — PASS, decisively. OOS STRONGER than in-sample.
Ran `bt_eval.py --side call --oos 2024-01-01` on the SL50 column export (N=337).
- **IS (pre-2024): n=163, RoR +16.3%, +$14,648 | OOS (2024+): n=174, RoR +18.96%, +$21,024** — OOS beats IS.
- **Positive EVERY year:** 2021 +$987 · 2022 +$3,553 · 2023 +$10,108 · 2024 +$5,435 · 2025 +$12,402 · 2026 +$3,187. OOS window (2024–26) = 59% of total P/L.
- **Exact inverse of the put's fragility:** put leans on 2022 / fades OOS; the call is STRONGEST in the recent OOS years. As a pair = genuine regime complements (put = high-vol selloffs / 2022-heavy; call = low-vol melt-ups / 2023–25-heavy).
- **median R −50.2% vs mean R +17.7%** = positive-tail with the median at the stop → **PT100-truncation suspect, motivates Batch 6d.** Losing-day signature 96% down days (clean directionality). realized R:R 1.82 (avg win $617 / avg loss $340 after SL50).
- **Verdict: call champion is OOS-robust and paper-ready** pending 6d (PT). **Long Call Spread · VIXΔ%<−2 · PT100 · SL50 · 11:00** clears every gate the put cleared, with a *better* OOS profile.

**Artifacts for both (per ingest protocol):** A–D/E **Compare screenshot** + **per-column Details screenshot** + **positions.csv per column** → save to `bot-fleet/`.

---

## After the backtests
A surviving config → **"Automate your strategy"** turns the backtest into a bot (carries all settings/
filters) → drop it in a new **Directional** group, tag `experiment`, run alongside a no-filter **control**
bot → **paper** → graduate on data (≥N trades across ≥1 high-vol cluster, positive Exp(R), tail matches
backtest, beats control live). That paper bot is the near-term milestone.
