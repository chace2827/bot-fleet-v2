> **⚠️ PREMISE FALSIFIED — read this first (banner added 2026-07-30, Phase 1).**
> This document frames the champion as running a hard 25% profit target and sources its constants from
> `data/bots_config.csv`. Both are wrong: PT25 generated **zero** exit orders across 47 post-fix positions
> (`docs/config-vs-reality-2026-07-28.md`), and `bots_config.csv` is the discredited hand-written record.
> It also cites `STATUS.md` and `backlog.md`, neither of which exists in v2.
> **The champion's PT25 was formally removed on 2026-07-30** — it is no longer the subject of this test.
> What survives and is still wanted: the **batch design** (PT25 vs PT50 vs trailing vs ride, judged on R via
> OA Compare). That batch moves to the **greenfield IC arms**, pre-registered, per `docs/build-plan.md`.

# IC Exit-Mechanic Backtest — Hard PT25 vs Trailing SmartStop

> **Status: QUEUED (spec'd 2026-07-07).** The IC analog of `oo-trial-backtests.md` /
> `directional-oa-build-sheet.md` — copy-pasteable OA backtest settings, pre-registered
> arms, success criteria, and what it does NOT verify. Runs in the OA backtester (June-2026
> upgrade: 2013→now history + trailing/SmartStop + $ SL/PT). **Compare by R, never raw P/L
> or win rate.** Do NOT touch the live champion while it clears G2 — this is a parallel test.

## 1. Hypothesis (why we're running this)
The champion (`IC-SPX-FastPT25-S2`) exits winners at a **hard 25% profit target**. Two
independent findings say that cut is **too tight** on this structure:
- **Hedge tournament** (`STATUS.md`): champion IC **Ride +7.3% Exp(R)** vs the tight-cut arm
  ~**+2.0%** — riding the winner beats cutting it.
- **OA Hindsight** (`backlog.md` COCKPIT LANE): **82.77% of closes were worse than holding**
  (−$312 avg); PT25 caps the many small winners. Held +$12.8K vs actual −$7.7K counterfactual.

**Thesis:** replacing the hard PT25 with a **trailing stop that arms at ~25% profit and then
trails** lets winners keep decaying in our favor while still locking a floor — capturing the
ride edge without the naked-hold tail risk. **This is the profit-side (winner) exit only; the
loss-side hedge (S2) is held constant across all arms** so the comparison is clean.

**Direction of expected result:** win rate will likely *fall* (some trails give back a bit before
closing) but **Exp(R) and Tot R should rise** if the thesis holds. Judge on R, not WR.

## 2. Constant config (identical across ALL arms — the champion baseline)
Verified against `data/bots_config.csv` (champion row):

| Field | Value |
|---|---|
| Underlying | **SPX**, 0DTE |
| Structure | Iron condor, **$5-wide** wings both sides |
| Entry | **11:00 AM ET** |
| Strike selection | **0.75% OTM** short strikes (NOT the −10Δ the 130PM clone uses — match the champion) |
| Entry filter | **Range075** — skip if `abs(SPX %chg from prior close) > 0.75%` |
| Calendar | **Skip FOMC days** |
| Re-entries | up to **10/day** (OA: 20 position-slots, since IC = 2 positions) |
| Backtest window | **2013 → present** (full history; regime coverage clears the ≥100-trade / ≥6-mo flag) |
| Exit pricing | SmartPricing Fast, 100% bid/ask (0DTE) |

**Only ONE thing changes between arms: the winner-exit rule.** Hold everything above frozen.

## 3. The arms — Batch T1 (fits OA Compare's ≤5-side-by-side)
Build arm 1, then **duplicate → tweak only the exit** for 2–5 (per the OA Compare workflow).

| Arm | Winner exit | Loss-side | Role |
|---|---|---|---|
| **T1-Control** | **Hard PT25** (close at +25% of credit) | constant SL* | Reproduces the champion — the number to beat |
| **T1-Ride** | **None** (ride to 3:50 time-exit) | constant SL* | Upper bracket; the tournament's +7.3% ride arm |
| **T1-Trail-A** | SmartStop: **arm @ 25%**, trail **15%** | constant SL* | Andy's exact idea — trail from the current PT mark |
| **T1-Trail-B** | SmartStop: **arm @ 40%**, trail **15%** | constant SL* | Let it build more before arming |
| **T1-Trail-C** | SmartStop: **arm @ 50%**, trail **20%** | constant SL* | Ride further, wider give-back |

\* **Loss-side control (read §6 first):** the live S2 (whole-IC strike-touch close) is a *monitor*
mechanic the backtester can't express natively. To keep the loss-side identical across arms, set a
**constant per-position stop-loss %** on every arm (start **SL200%** of credit as a loose proxy so
the winner-exit differences dominate). If you'd rather isolate the winner mechanic completely, run
**stopless** on all five instead — just keep it the *same* on all five. Do not vary the stop and the
PT in the same batch.

**Arm/trail semantics:** "arm @ 25%" = the trail activates once the position has captured 25% of the
collected credit as profit; "trail 15%" = if it then gives back 15% of credit from its best, close.
⚠️ **Confirm OA's exact field meaning when you build it** (% of credit vs % of max-profit vs $) — the
platform reference flags SmartStop config as a re-verify item. Whatever the unit, keep it consistent
across arms.

## 4. Build steps (OA)
1. Build **T1-Control** first: full champion config (§2) + PT25 exit option + the constant SL proxy.
2. Run it; **sanity-check it reproduces the champion's shape** (WR ~43%, expectancy sign) before trusting the batch.
3. On the **Compare Backtests** page: **duplicate** T1-Control four times; on each copy change **only** the winner-exit to the T1-Ride / A / B / C setting. Leave entry, strikes, width, filter, SL untouched.
4. Run all five over 2013→present. Screenshot the Compare view.
5. **Copy/Download positions as CSV** for each arm (June-2026 export) — we score off the CSV, not OA's win-rate-sorted view.

## 5. Success criteria (compare by R)
For each arm pull from the positions CSV (our own analysis, not OA's WR view):
- **Exp(R)** = avg pnl ÷ risk per trade — the primary metric.
- **Tot R** (size-free total), **maxDD-R** (risk shape), **longest losing streak**.
- **Instance-profitability** (% of trades green) and **avg win vs avg loss in R**.
- Run the **expectancy sanity check** (Exp(R) ≈ WR·avgWinR − (1−WR)·avgLossR).

**PASS = a trail arm beats T1-Control on Exp(R) AND Tot R, without a materially worse maxDD-R.**
A trail arm that merely matches Control on R but with lower drawdown is also interesting (smoother).
If **T1-Ride** wins outright and no trail beats it, that's a real result too → the champion should
simply drop the PT and ride (with S2 doing the loss-side work live).

## 6. What this does NOT verify (limitations — read before acting)
- **S2 fidelity.** The backtester's constant SL proxy is **not** the live whole-IC strike-touch S2.
  So this batch ranks **winner-exit mechanics**, not the true live loss-side. Cross-reference the
  live **hedge tournament** (`STATUS.md`) for the S2 side; the two together give the full picture.
  A trail arm that wins here still needs the live S2 running in paper before capital.
- **Slippage / fills.** OA backtest fills are optimistic. Apply the standard **30–40% haircut +
  commission** before believing any edge (ties to the unlogged v5-slippage task). Trailing exits fire
  more often than a one-shot PT → **more commission events** — account for that explicitly.
- **Trial count.** Five arms is small, but still pre-register and resist mining trail widths post-hoc.
  If a winner emerges, confirm it on a **held-out window** (e.g. exclude 2022, or OOS the last ~12mo)
  before promoting — same discipline as the directional OOS gate.
- **Whole-IC vs per-spread trail.** OA trails each **spread** (IC = 2 positions) independently. This
  batch tests per-spread trailing (usually what you want). Whole-condor trailing = monitor logic, a
  separate test.

## 7. Next batch (only if a trail arm passes)
**Batch T2** = refine the trail *width* around the T1 winner (e.g. arm @ 25%, trail 8% / 12% / 18% /
25%) to find the give-back sweet spot; hold the arm level at the T1 winner. Then OOS-confirm.

## 8. Graduation → paper bot (post-PASS)
If a trail arm clears §5 + the OOS confirm, build it as a **parallel experiment bot**, NOT a change
to the champion:
- **Name:** `IC-SPX-FastPT25-Trail`
- **Config:** champion §2 exactly, but winner-exit = the winning SmartStop arm; **live S2 monitor ON**
  (the real hedge, restored for live).
- **Run head-to-head vs the champion** on R, regime-matched, until it clears the readiness board.
  Keeps the champion's G2 clock clean while the ride-vs-cut question resolves on live paper.
