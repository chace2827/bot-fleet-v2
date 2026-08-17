# Bot Fleet — STATUS  ·  generated 2026-08-10

> **Numeric source of truth.** Auto-generated from `data/trades.csv` by `scripts/report.py`. Do not edit by hand. All figures are PAPER. Task backlog: `docs/backlog.md` (also in `dashboard.html`).

> **POST-CUTOVER LEDGER — `LEDGER_START = 2026-08-10`.** Every figure below is drawn from positions **opened on or after** that date. The v1 era is frozen in `data/archive/` and is never an input here.


## ⚠️ UNSIGNED PRE-REGISTRATION BOTS — DO NOT SWITCH ON

> The following bots have a pre-registration ledger entry with a blank, missing, or `NOT SIGNED` `SIGNED` line. No bot may be switched ON until the entry is signed and dated.

- IC-SPX-FastPT25-S2-130PM
- QQQ long call
- QQQ-IC-0DTE-Fortress
- QQQ-IC-0DTE-Fortress-NoPT50
- Tasty Condor

## Headline
- **Total closed P/L:** $500  ·  4 legs  ·  3 bots
  - IC: $650  (SPX $650)
  - OA-Mirror: $-150  (SPX $-150)

## Champion — IC-SPX-FastPT25-S2
- P/L **$50**  ·  1 condors (1 legs)  ·  1 trading days (1 green / 0 red)
- Max drawdown (daily cumulative): $0

## Focus roster — the bots you're actively perfecting  (OA: `*-Focus` groups)
> Close-to-live per pillar; for an A/B only the leading side. Select one group = per-pillar, all three = combined. Read per-bot R (readiness board), not the subtotal.

| Pillar | Bot | Status | Trades | P/L | WR |
|---|---|---|--:|--:|--:|
| IC | IC-SPX-FastPT25-S2 | ON | 1 | $50 | 100% |
| **Total** | | | | **$50** | |

## Monitor — live but not focus  (OA: `Monitor` group)
> Running and watched — A/B laggards, controls, other active mirrors, the pending-decision QQQ-Fortress pair. Not promotion candidates yet.

| Pillar | Bot | Status | Trades | P/L | WR |
|---|---|---|--:|--:|--:|
| IC | IC-SPX-FastPT25-S2-130PM | ON | 1 | $600 | 100% |
| OA-Mirror | 60min-ORB-10W-Paper-v1 | ON | 1 | $-150 | 0% |
| **Total** | | | | **$450** | |

## Allocation audit — sizing realism  (ON bots, per-position)
> R (pnl÷risk) already cancels size, so this changes **no ranking** — it flags whether the paper sizing is realistic to carry live. Hold class sets the rule: **0DTE** recycles risk daily; **swing/multi-week** ties capital up for the whole hold (max-risk/day = concurrent open risk, not daily deploy). **1-lot bots are fill-untested at scale** — their edge won't survive the slippage of a real order size (ties to the v5-slippage task).

| Bot | Pillar | Hold | Pos | med Qty | med Risk$ | max Risk$ | Realism |
|---|---|---|--:|--:|--:|--:|:--|
| IC-SPX-FastPT25-S2 | IC | 0DTE | 1 | 10 | $4,850 | $4,850 | sized ✓ |
| IC-SPX-FastPT25-S2-130PM | IC | 0DTE | 1 | 10 | $4,800 | $4,800 | sized ✓ |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 0DTE | 1 | 1 | $910 | $910 | **1-lot — fill-untested** |

> **Read:** SPX-IC + Nigiri run ~10-lot (~$4.8k/position, comparable to the champion). Every other mirror + both directional bots run **1 lot** ($0.5k–$2.9k) — realistic for tracking W/L, not for reading a live-scale edge. Sizing rule is per-bot by hold class (see backlog COCKPIT LANE step 1); the go-live target is ~$10k max risk/day with a hedge reserve carved out first.

## Hedge tournament (live-data counterfactual)
> **The productized loss autopsy.** Every real, settled (status=expired) leg replayed through the v1 hedge library — Ride/no-stop, PT+X%/SL-X% return-threshold rules, and an S2 strike-touch cut (tape-gated, 5-min grain). **Optimistic bound, not a live estimate** — every non-Ride arm assumes a fill exactly at the threshold; real fills slip. Compare rules by **R** (pnl÷risk), never $. Basis: PT/SL % are of the credit collected (`|premium|`), per `mfe_pct`/`mae_pct` already carrying that unit (verified against the ledger — see `scripts/hedge_tournament.py` docstring). **Defang: deferred v1** (4 legs marked, not modeled — needs an intraday premium-decay path not yet in the ledger).

| Rule | N | Exp(R) | Tot R | WR | maxDD-R | worst-R |
|---|--:|--:|--:|--:|--:|--:|
| ride | 4 | +6.4% | +0.26 | 100% | 0.00 | +4.2% |
| pt25 | 4 | +1.6% | +0.06 | 100% | 0.00 | +1.0% |
| pt50 | 4 | +3.2% | +0.13 | 100% | 0.00 | +2.1% |
| pt100 | 4 | +6.4% | +0.26 | 100% | 0.00 | +4.2% |
| sl50 | 4 | +2.9% | +0.12 | 50% | -0.03 | -2.6% |
| sl75 | 4 | +4.1% | +0.16 | 75% | -0.04 | -4.0% |
| sl100 | 4 | +3.8% | +0.15 | 75% | -0.05 | -5.3% |
| sl130 | 4 | +3.4% | +0.14 | 75% | -0.07 | -6.8% |
| s2 | 4 | +6.4% | +0.26 | 100% | 0.00 | +4.2% |

#### Per-bot cut  (Ride vs SL75 — the mid-spectrum published rung)
| Bot | N | Ride Exp(R) | SL75 Exp(R) | Δ |
|---|--:|--:|--:|--:|
| IC-SPX-FastPT25-S2-130PM | 4 | +6.4% | +4.1% | -2.3pp |

#### Regime cut  (Ride vs SL75, by tape-derived regime label)
| Regime | N | Ride Exp(R) | SL75 Exp(R) |
|---|--:|--:|--:|
| Chop | 4 | +6.4% | +4.1% |

> N is small and concentrated in the last few tape-covered trading days (tape.py is new); the S2 arm and the regime cut will thicken as more days accrue. Read this as an early ranking to cross-check the LEAN/OA backtest tournament, not a standalone verdict.

## Trade-window heat map — when do shorts actually get touched (hour x regime)
> **The 11am-vs-1:30 question, generalized.** Every ledger position's worst-adverse-excursion (MAE) timestamp, bucketed by hour-of-day x tape-derived regime (Drift/Trend/Chop/n-a). `touch %` = short-strike touch rate, scored only on positions with same-day tape coverage (a small, recent subset — most history predates `tape.py`); `MAE` = mean adverse excursion as % of credit, computed on ALL positions in the bucket regardless of tape coverage. Cells are `n=… · touch …% · MAE …%`; blank touch% = no tape-covered position fell in that cell. **Small-n cells are directional, not conclusive** — read the n before the rate.

| Hour | Chop |
|---|---|
| 11-12 | n=1 · touch 0% · MAE +0.0% |
| 12-13 | n=1 · touch 0% · MAE -1.7% |
| 13-14 | n=1 · touch 0% · MAE -0.2% |

> **Read:** touches cluster at **11-12 (Chop)** — 0 of 0 tape-covered position(s) scored there touched (touch rate 0%). Tape coverage is thin (5 days) — treat as an early signal, not a verdict.

## Lessons index — tagged, searchable  (data/lessons.csv)
> Every graded bot-day's "day's lesson" (from the brief JSON's Verdict row; session-log fallback only for dates the brief never covered), tagged from a fixed vocabulary (`entry-timing · hedge · filter · regime · sizing · other`) by simple keyword rules (see `scripts/lessons.py` docstring) — not an ML classifier. Grouped by tag, most recent first.

**Tag counts:** entry-timing 1  ·  hedge 2  ·  regime 12  ·  other 18

#### other (18)
- **2026-07-02** · DIR-SPX-Put-Control — borderline; watch
- **2026-07-02** · IC-SPX-FastPT25-S2-130PM — borderline; watch
- **2026-07-02** · IC-SPX-Fortress-Defang — clean win
- **2026-07-02** · IC-SPX-Fortress-Unstopped — clean win
- **2026-07-01** · IC-SPX-FastPT25-S2-130PM — borderline; watch
- **2026-07-01** · IC-SPX-Fortress-Defang — clean win
- **2026-07-01** · IC-SPX-Fortress-Unstopped — clean win
- **2026-07-01** · Nigiri-Paper-v1 — borderline; watch
- **2026-06-30** · 60min-ORB-10W-Paper-v1 — clean win
- **2026-06-30** · DIR-SPX-CallVIXdrop — borderline; watch
- **2026-06-30** · IC-SPX-FastPT25-S2 — clean win
- **2026-06-30** · IC-SPX-FastPT25-S2-130PM — borderline; watch
- **2026-06-30** · Nigiri-Paper-v1 — clean win
- **2026-06-30** · Trendy-Paper-v1 — clean win
- **2026-06-29** · 3DTE $140-$350 — clean win
- **2026-06-29** · IC-SPX-FastPT25-S2 — clean win
- **2026-06-29** · Nigiri-Paper-v1 — clean win
- **2026-06-26** · IC-SPX-FastPT25-S2 — clean win

#### regime (12)
- **2026-07-02** · DIR-SPX-CallVIXdrop — good loss — design held, tape unlucky
- **2026-07-02** · IC-SPX-FastPT25-S2 — good loss — design held, tape unlucky
- **2026-07-01** · DIR-SPX-Put-Control — good loss — design held, tape unlucky
- **2026-07-01** · IC-SPX-FastPT25-S2 — good loss — design held, tape unlucky
- **2026-06-30** · DIR-SPX-Put-Control — good loss — design held, tape unlucky
- **2026-06-30** · IC-SPX-Fortress-Defang — good loss — design held, tape unlucky
- **2026-06-30** · IC-SPX-Fortress-Unstopped — good loss — design held, tape unlucky
- **2026-06-29** · DIR-SPX-Put-Control — good loss — design held, tape unlucky
- **2026-06-26** · DIR-SPX-Put-Control — good loss — design held, tape unlucky
- **2026-06-26** · IC-SPX-FastPT25-S2-130PM — good loss — design held, tape unlucky
- **2026-06-26** · IC-SPX-Fortress-Defang — good loss — design held, tape unlucky
- **2026-06-26** · IC-SPX-Fortress-Unstopped — good loss — design held, tape unlucky

#### hedge (2)
- **2026-06-26** · QQQ-IC-0DTE-Fortress — naked breach rode to expiry — log a convexity/hedge candidate here
- **2026-06-26** · QQQ-IC-0DTE-Fortress-NoPT50 — naked breach rode to expiry — log a convexity/hedge candidate here

#### entry-timing (1)
- **2026-06-23** · (session-log) — **Key lesson surfaced (6/17 vs 6/23):** Range075 protects against gap days (move visible at entry) but NOT against an intraday trend after entry — 6/17 opened +0.7%, passed filter, Fortress entered 1:31 and ate −$7,530; 6/23 gapped −3% pre-open so filter blocked. Naked-downside risk = "quiet open, trend after 11am," the exact hole a stop-loss / long-vol overlay plugs.

## Per-bot (sorted by P/L)
| Bot | Pillar | Und | Role | Status | Trades | Legs | P/L | WR | Fix? |
|---|---|---|---|---|--:|--:|--:|--:|:--:|
| 60min-ORB-10W-Paper-v1 | OA-Mirror | SPX | mirror-watch | ON | 1 | 1 | $-150 | 0% | - |
| IC-SPX-FastPT25-S2 | IC | SPX | live-candidate | ON | 1 | 1 | $50 | 100% | - |
| IC-SPX-FastPT25-S2-130PM | IC | SPX | experiment | ON | 1 | 2 | $600 | 100% | - |

## Readiness board — per-condor, gated (the graduation view)
> **Grain = condor** (legs summed), not leg. Six ordered gates; the **first red (○) gate is the named blocker**. `●`=pass `○`=fail `·`=pending. Exp(R) shows the **bootstrap 95% CI** (replaces the t-stat). Stage: INCUBATE→VALIDATE→CANDIDATE→LIVE-READY (LIVE = real capital). Controls & mirror-watch are listed separately — they can't graduate by design.
> **Gates:** G1 clean data (no strike-bug, single-sided excluded) · G2 ≥20 clean condors · G3 Exp(R)>0 w/ 95% CI above 0 · G4 maxDD-R within cap (RoE $ cap still a `<FILL>` blank) · G5 instruction-mirror ≥90% (from the daily brief / `data/compliance.csv`; pending until ≥5 graded days) · G6 OOS/regime robustness.

| Bot | Role | Stage | Gates | n | Exp(R) [95% CI] | Blocker |
|---|---|---|:--:|--:|--:|---|
| IC-SPX-FastPT25-S2-130PM | experiment | VALIDATE | ●○○●·· | 1 | +12.5% — | G2: 1 clean condors (need 20) |
| IC-SPX-FastPT25-S2 | live-candidate | VALIDATE | ●○○●·· | 1 | +1.0% — | G2: 1 clean condors (need 20) |

#### Non-graduating (controls / mirror-watch — tracked, can't go live)
| Bot | Role | Gates | n | Exp(R) [95% CI] | Note |
|---|---|:--:|--:|--:|---|
| 60min-ORB-10W-Paper-v1 | mirror-watch | ●○○●·· | 1 | -16.5% — | G2: 1 clean condors (need 20) |

## Scorecard — normalized (Return on Risk) · legacy per-LEG view
> ⚠️ **Per-LEG grain** (kept for continuity) — for the graduation decision use the **Readiness board** above (per-condor, gated). Each trade = **pnl ÷ capital-at-risk** ("R"), so allocation and contract size cancel out. Sorted by expectancy. t-stat blows up for low-variance grinders (e.g. 3DTE) — don't rank on it alone.

### Ranked (n ≥ 20)
| Bot | Pillar | n | Exp(R) | t | Tot R | maxDD-R | WR |
|---|---|--:|--:|--:|--:|--:|--:|

### Provisional (n < 20 — tracked, not ranked; samples too small to trust)
| Bot | Pillar | n | Exp(R) | Tot R | raw P/L |
|---|---|--:|--:|--:|--:|
| IC-SPX-FastPT25-S2-130PM | IC | 2 | +0.064 | +0.1 | $600 |
| IC-SPX-FastPT25-S2 | IC | 1 | +0.010 | +0.0 | $50 |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 1 | -0.165 | -0.2 | $-150 |

### Decision rules (read against the right column)
- **Kill** — Exp(R) < 0 held with conviction (|t| ≳ 2, or n large). Raw P/L size is irrelevant.
- **Graduate** — Exp(R) > 0 **and** |t| ≳ 2 **and** n ≥ threshold (edge is real, not noise).
- **Size live capital** — among graduates, weight by Tot R + low maxDD-R (consistency); never size on raw P/L.
- **Exp(R)** = avg return per $1 risked. **Tot R** = size-free analog of total P/L. **maxDD-R** = worst cumulative-R drawdown (risk shape). **t** = evidence the edge is real.

## Caveats
- **Trades = condors** (the two legs of one entry paired); **Legs = OA position rows** (matches OA's "Positions" count). Win rate shown is per-condor.
- A combined-`ironcondor` bot logs 1 leg per condor; a legged bot logs 2 — so Legs ≈ 2× Trades only for legged bots. That's why they were confusing before.
- `Fix? = Y`: QQQ-IC bot carrying the call-side strike-resolution bug; data contaminated until fixed.
- Single-sided condors (only one leg opened): 2 legs flagged.
- Tiny-N bots are tracked but **not** evidence; read Trades before P/L.
