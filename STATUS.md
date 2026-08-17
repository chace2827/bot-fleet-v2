# Bot Fleet — STATUS  ·  generated 2026-08-17

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
- **Total closed P/L:** $3,777  ·  45 legs  ·  15 bots
  - Directional: $65  (SPX $65)
  - IC: $3,557  (QQQ $107  ·  SPX $3,450)
  - OA-Mirror: $155  (SPX $-5)

## Champion — IC-SPX-FastPT25-S2
- P/L **$100**  ·  5 condors (5 legs)  ·  5 trading days (2 green / 0 red)
- Max drawdown (daily cumulative): $0

## Focus roster — the bots you're actively perfecting  (OA: `*-Focus` groups)
> Close-to-live per pillar; for an A/B only the leading side. Select one group = per-pillar, all three = combined. Read per-bot R (readiness board), not the subtotal.

| Pillar | Bot | Status | Trades | P/L | WR |
|---|---|---|--:|--:|--:|
| IC | IC-SPX-FastPT25-S2 | ON | 5 | $100 | 40% |
| Directional | DIR-SPX-CallVIXdrop | ON | 1 | $65 | 100% |
| OA-Mirror | 3DTE $140-$350 | ON | 1 | $45 | 100% |
| OA-Mirror | Nigiri-Paper-v1 | ON | 4 | $120 | 75% |
| **Total** | | | | **$330** | |

## Monitor — live but not focus  (OA: `Monitor` group)
> Running and watched — A/B laggards, controls, other active mirrors, the pending-decision QQQ-Fortress pair. Not promotion candidates yet.

| Pillar | Bot | Status | Trades | P/L | WR |
|---|---|---|--:|--:|--:|
| IC | GF-QQQ-IC-Canary | ON | 2 | $2 | 100% |
| IC | GF-QQQ-IC-Trail | ON | 2 | $7 | 100% |
| IC | GF-QQQ-IC-PT50 | ON | 2 | $9 | 100% |
| IC | GF-QQQ-IC-Touch0 | ON | 2 | $15 | 100% |
| IC | GF-QQQ-IC-SL100 | ON | 2 | $15 | 100% |
| IC | GF-QQQ-IC-SL200 | ON | 2 | $15 | 100% |
| IC | GF-QQQ-IC-Ride | ON | 2 | $15 | 100% |
| IC | GF-QQQ-IC-Ride-Delta | ON | 4 | $29 | 100% |
| IC | IC-SPX-FastPT25-S2-130PM | ON | 6 | $3,350 | 100% |
| OA-Mirror | 60min-ORB-10W-Paper-v1 | ON | 3 | $-50 | 67% |
| OA-Mirror | Trendy-Paper-v1 | ON | 1 | $40 | 100% |
| **Total** | | | | **$3,447** | |

## Allocation audit — sizing realism  (ON bots, per-position)
> R (pnl÷risk) already cancels size, so this changes **no ranking** — it flags whether the paper sizing is realistic to carry live. Hold class sets the rule: **0DTE** recycles risk daily; **swing/multi-week** ties capital up for the whole hold (max-risk/day = concurrent open risk, not daily deploy). **1-lot bots are fill-untested at scale** — their edge won't survive the slippage of a real order size (ties to the v5-slippage task).

| Bot | Pillar | Hold | Pos | med Qty | med Risk$ | max Risk$ | Realism |
|---|---|---|--:|--:|--:|--:|:--|
| IC-SPX-FastPT25-S2 | IC | 0DTE | 5 | 10 | $4,900 | $4,900 | sized ✓ |
| IC-SPX-FastPT25-S2-130PM | IC | 0DTE | 6 | 10 | $4,750 | $4,800 | sized ✓ |
| GF-QQQ-IC-Canary | IC | 0DTE | 2 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-Trail | IC | 0DTE | 2 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-PT50 | IC | 0DTE | 2 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-Touch0 | IC | 0DTE | 2 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-SL100 | IC | 0DTE | 2 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-SL200 | IC | 0DTE | 2 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-Ride | IC | 0DTE | 2 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-Ride-Delta | IC | 0DTE | 4 | 1 | $193 | $193 | **1-lot — fill-untested** |
| DIR-SPX-CallVIXdrop | Directional | 0DTE | 1 | 1 | $605 | $605 | **1-lot — fill-untested** |
| Nigiri-Paper-v1 | OA-Mirror | 4d swing | 4 | 10 | $4,920 | $4,930 | sized ✓ |
| 3DTE $140-$350 | OA-Mirror | 3d swing | 1 | 1 | $955 | $955 | **1-lot — fill-untested** |
| Trendy-Paper-v1 | OA-Mirror | 10d multi-wk | 1 | 1 | $929 | $929 | **1-lot — fill-untested** |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 0DTE | 3 | 1 | $910 | $920 | **1-lot — fill-untested** |

> **Read:** SPX-IC + Nigiri run ~10-lot (~$4.8k/position, comparable to the champion). Every other mirror + both directional bots run **1 lot** ($0.5k–$2.9k) — realistic for tracking W/L, not for reading a live-scale edge. Sizing rule is per-bot by hold class (see backlog COCKPIT LANE step 1); the go-live target is ~$10k max risk/day with a hedge reserve carved out first.

## Hedge tournament (live-data counterfactual)
> **The productized loss autopsy.** Every real, settled (status=expired) leg replayed through the v1 hedge library — Ride/no-stop, PT+X%/SL-X% return-threshold rules, and an S2 strike-touch cut (tape-gated, 5-min grain). **Optimistic bound, not a live estimate** — every non-Ride arm assumes a fill exactly at the threshold; real fills slip. Compare rules by **R** (pnl÷risk), never $. Basis: PT/SL % are of the credit collected (`|premium|`), per `mfe_pct`/`mae_pct` already carrying that unit (verified against the ledger — see `scripts/hedge_tournament.py` docstring). **Defang: deferred v1** (13 legs marked, not modeled — needs an intraday premium-decay path not yet in the ledger).

| Rule | N | Exp(R) | Tot R | WR | maxDD-R | worst-R |
|---|--:|--:|--:|--:|--:|--:|
| ride | 13 | +5.8% | +0.76 | 100% | 0.00 | +4.2% |
| pt25 | 13 | +1.5% | +0.19 | 100% | 0.00 | +1.0% |
| pt50 | 13 | +2.9% | +0.38 | 100% | 0.00 | +2.1% |
| pt100 | 13 | +5.8% | +0.76 | 100% | 0.00 | +4.2% |
| sl50 | 13 | +2.1% | +0.27 | 54% | -0.08 | -3.2% |
| sl75 | 13 | +3.6% | +0.46 | 77% | -0.09 | -4.8% |
| sl100 | 13 | +4.0% | +0.53 | 85% | -0.06 | -6.4% |
| sl130 | 13 | +3.8% | +0.49 | 85% | -0.08 | -8.3% |
| s2 | 8 | +6.1% | +0.49 | 100% | 0.00 | +4.2% |

#### Per-bot cut  (Ride vs SL75 — the mid-spectrum published rung)
| Bot | N | Ride Exp(R) | SL75 Exp(R) | Δ |
|---|--:|--:|--:|--:|
| IC-SPX-FastPT25-S2-130PM | 12 | +5.9% | +3.5% | -2.5pp |
| 3DTE $140-$350 | 1 | +4.7% | +4.7% | +0.0pp |

#### Regime cut  (Ride vs SL75, by tape-derived regime label)
| Regime | N | Ride Exp(R) | SL75 Exp(R) |
|---|--:|--:|--:|
| Chop | 9 | +6.0% | +4.9% |
| n/a | 4 | +5.5% | +0.4% |

> N is small and concentrated in the last few tape-covered trading days (tape.py is new); the S2 arm and the regime cut will thicken as more days accrue. Read this as an early ranking to cross-check the LEAN/OA backtest tournament, not a standalone verdict.

## Trade-window heat map — when do shorts actually get touched (hour x regime)
> **The 11am-vs-1:30 question, generalized.** Every ledger position's worst-adverse-excursion (MAE) timestamp, bucketed by hour-of-day x tape-derived regime (Drift/Trend/Chop/n-a). `touch %` = short-strike touch rate, scored only on positions with same-day tape coverage (a small, recent subset — most history predates `tape.py`); `MAE` = mean adverse excursion as % of credit, computed on ALL positions in the bucket regardless of tape coverage. Cells are `n=… · touch …% · MAE …%`; blank touch% = no tape-covered position fell in that cell. **Small-n cells are directional, not conclusive** — read the n before the rate.

| Hour | Chop | Drift | n/a |
|---|---|---|---|
| 10-11 | n=1 · touch 0% · MAE -0.1% | — | n=1 · MAE -0.3% |
| 11-12 | n=4 · touch 0% · MAE +0.0% | — | n=4 · MAE -0.1% |
| 12-13 | n=2 · touch 0% · MAE -0.9% | — | n=1 · MAE -0.4% |
| 13-14 | n=13 · touch 0% · MAE -0.2% | n=9 · touch 0% · MAE -0.1% | n=2 · MAE -1.1% |
| 14-15 | — | — | n=2 · MAE -0.6% |

> **Read:** touches cluster at **10-11 (Chop)** — 0 of 0 tape-covered position(s) scored there touched (touch rate 0%). Tape coverage is thin (5 days) — treat as an early signal, not a verdict.

## Lessons index — tagged, searchable  (data/lessons.csv)
> Every graded bot-day's "day's lesson" (from the brief JSON's Verdict row; session-log fallback only for dates the brief never covered), tagged from a fixed vocabulary (`entry-timing · hedge · filter · regime · sizing · other`) by simple keyword rules (see `scripts/lessons.py` docstring) — not an ML classifier. Grouped by tag, most recent first.

**Tag counts:** 

## Per-bot (sorted by P/L)
| Bot | Pillar | Und | Role | Status | Trades | Legs | P/L | WR | Fix? |
|---|---|---|---|---|--:|--:|--:|--:|:--:|
| 60min-ORB-10W-Paper-v1 | OA-Mirror | SPX | mirror-watch | ON | 3 | 3 | $-50 | 67% | - |
| GF-QQQ-IC-Canary | IC | QQQ | instrument | ON | 2 | 2 | $2 | 100% | - |
| GF-QQQ-IC-Trail | IC | QQQ | experiment | ON | 2 | 2 | $7 | 100% | - |
| GF-QQQ-IC-PT50 | IC | QQQ | experiment | ON | 2 | 2 | $9 | 100% | - |
| GF-QQQ-IC-Touch0 | IC | QQQ | experiment | ON | 2 | 2 | $15 | 100% | - |
| GF-QQQ-IC-SL100 | IC | QQQ | experiment | ON | 2 | 2 | $15 | 100% | - |
| GF-QQQ-IC-SL200 | IC | QQQ | experiment | ON | 2 | 2 | $15 | 100% | - |
| GF-QQQ-IC-Ride | IC | QQQ | control | ON | 2 | 2 | $15 | 100% | - |
| GF-QQQ-IC-Ride-Delta | IC | QQQ | experiment | ON | 4 | 4 | $29 | 100% | - |
| Trendy-Paper-v1 | OA-Mirror | — | mirror-watch | ON | 1 | 1 | $40 | 100% | - |
| 3DTE $140-$350 | OA-Mirror | SPX | mirror-watch | ON | 1 | 1 | $45 | 100% | - |
| DIR-SPX-CallVIXdrop | Directional | SPX | experiment | ON | 1 | 1 | $65 | 100% | - |
| IC-SPX-FastPT25-S2 | IC | SPX | live-candidate | ON | 5 | 5 | $100 | 40% | - |
| Nigiri-Paper-v1 | OA-Mirror | — | mirror-watch | ON | 4 | 4 | $120 | 75% | - |
| IC-SPX-FastPT25-S2-130PM | IC | SPX | experiment | ON | 6 | 12 | $3,350 | 100% | - |

## Readiness board — per-condor, gated (the graduation view)
> **Grain = condor** (legs summed), not leg. Six ordered gates; the **first red (○) gate is the named blocker**. `●`=pass `○`=fail `·`=pending. Exp(R) shows the **bootstrap 95% CI** (replaces the t-stat). Stage: INCUBATE→VALIDATE→CANDIDATE→LIVE-READY (LIVE = real capital). Controls & mirror-watch are listed separately — they can't graduate by design.
> **Gates:** G1 clean data (no strike-bug, single-sided excluded) · G2 ≥20 clean condors · G3 Exp(R)>0 w/ 95% CI above 0 · G4 maxDD-R within cap (RoE $ cap still a `<FILL>` blank) · G5 instruction-mirror ≥90% (from the daily brief / `data/compliance.csv`; pending until ≥5 graded days) · G6 OOS/regime robustness.

| Bot | Role | Stage | Gates | n | Exp(R) [95% CI] | Blocker |
|---|---|---|:--:|--:|--:|---|
| IC-SPX-FastPT25-S2-130PM | experiment | CANDIDATE | ●○●●·· | 6 | +11.7% [+11.2, +12.3] | G2: 6 clean condors (need 20) |
| GF-QQQ-IC-Touch0 | experiment | CANDIDATE | ●○●●·· | 2 | +3.9% [+3.1, +4.7] | G2: 2 clean condors (need 20) |
| GF-QQQ-IC-SL100 | experiment | CANDIDATE | ●○●●·· | 2 | +3.9% [+3.1, +4.7] | G2: 2 clean condors (need 20) |
| GF-QQQ-IC-SL200 | experiment | CANDIDATE | ●○●●·· | 2 | +3.9% [+3.1, +4.7] | G2: 2 clean condors (need 20) |
| GF-QQQ-IC-Ride-Delta | experiment | CANDIDATE | ●○●●·· | 4 | +3.8% [+3.1, +4.5] | G2: 4 clean condors (need 20) |
| GF-QQQ-IC-PT50 | experiment | CANDIDATE | ●○●●·· | 2 | +2.4% [+2.1, +2.6] | G2: 2 clean condors (need 20) |
| GF-QQQ-IC-Trail | experiment | CANDIDATE | ●○●●·· | 2 | +1.8% [+0.5, +3.1] | G2: 2 clean condors (need 20) |
| GF-QQQ-IC-Canary | instrument | CANDIDATE | ●○●●·· | 2 | +0.5% [+0.5, +0.5] | G2: 2 clean condors (need 20) |
| DIR-SPX-CallVIXdrop | experiment | VALIDATE | ●○○●·· | 1 | +10.7% — | G2: 1 clean condors (need 20) |
| IC-SPX-FastPT25-S2 | live-candidate | VALIDATE | ●○○●·· | 5 | +0.4% [+0.0, +0.8] | G2: 5 clean condors (need 20) |

#### Non-graduating (controls / mirror-watch — tracked, can't go live)
| Bot | Role | Gates | n | Exp(R) [95% CI] | Note |
|---|---|:--:|--:|--:|---|
| GF-QQQ-IC-Ride | control | ●○●●·· | 2 | +3.9% [+3.1, +4.7] | G2: 2 clean condors (need 20) |
| Nigiri-Paper-v1 | mirror-watch | ●○●●·· | 4 | +0.6% [+0.2, +1.2] | G2: 4 clean condors (need 20) |
| 3DTE $140-$350 | mirror-watch | ●○○●·· | 1 | +4.7% — | G2: 1 clean condors (need 20) |
| Trendy-Paper-v1 | mirror-watch | ●○○●·· | 1 | +4.3% — | G2: 1 clean condors (need 20) |
| 60min-ORB-10W-Paper-v1 | mirror-watch | ●○○●·· | 3 | -1.8% [-16.5, +5.5] | G2: 3 clean condors (need 20) |

## Scorecard — normalized (Return on Risk) · legacy per-LEG view
> ⚠️ **Per-LEG grain** (kept for continuity) — for the graduation decision use the **Readiness board** above (per-condor, gated). Each trade = **pnl ÷ capital-at-risk** ("R"), so allocation and contract size cancel out. Sorted by expectancy. t-stat blows up for low-variance grinders (e.g. 3DTE) — don't rank on it alone.

### Ranked (n ≥ 20)
| Bot | Pillar | n | Exp(R) | t | Tot R | maxDD-R | WR |
|---|---|--:|--:|--:|--:|--:|--:|

### Provisional (n < 20 — tracked, not ranked; samples too small to trust)
| Bot | Pillar | n | Exp(R) | Tot R | raw P/L |
|---|---|--:|--:|--:|--:|
| DIR-SPX-CallVIXdrop | Directional | 1 | +0.107 | +0.1 | $65 |
| IC-SPX-FastPT25-S2-130PM | IC | 12 | +0.059 | +0.7 | $3,350 |
| 3DTE $140-$350 | OA-Mirror | 1 | +0.047 | +0.0 | $45 |
| Trendy-Paper-v1 | OA-Mirror | 1 | +0.043 | +0.0 | $40 |
| GF-QQQ-IC-Touch0 | IC | 2 | +0.039 | +0.1 | $15 |
| GF-QQQ-IC-SL100 | IC | 2 | +0.039 | +0.1 | $15 |
| GF-QQQ-IC-SL200 | IC | 2 | +0.039 | +0.1 | $15 |
| GF-QQQ-IC-Ride | IC | 2 | +0.039 | +0.1 | $15 |
| GF-QQQ-IC-Ride-Delta | IC | 4 | +0.038 | +0.2 | $29 |
| GF-QQQ-IC-PT50 | IC | 2 | +0.024 | +0.0 | $9 |
| GF-QQQ-IC-Trail | IC | 2 | +0.018 | +0.0 | $7 |
| Nigiri-Paper-v1 | OA-Mirror | 4 | +0.006 | +0.0 | $120 |
| GF-QQQ-IC-Canary | IC | 2 | +0.005 | +0.0 | $2 |
| IC-SPX-FastPT25-S2 | IC | 5 | +0.004 | +0.0 | $100 |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 3 | -0.018 | -0.1 | $-50 |

### Decision rules (read against the right column)
- **Kill** — Exp(R) < 0 held with conviction (|t| ≳ 2, or n large). Raw P/L size is irrelevant.
- **Graduate** — Exp(R) > 0 **and** |t| ≳ 2 **and** n ≥ threshold (edge is real, not noise).
- **Size live capital** — among graduates, weight by Tot R + low maxDD-R (consistency); never size on raw P/L.
- **Exp(R)** = avg return per $1 risked. **Tot R** = size-free analog of total P/L. **maxDD-R** = worst cumulative-R drawdown (risk shape). **t** = evidence the edge is real.

## Caveats
- **Trades = condors** (the two legs of one entry paired); **Legs = OA position rows** (matches OA's "Positions" count). Win rate shown is per-condor.
- A combined-`ironcondor` bot logs 1 leg per condor; a legged bot logs 2 — so Legs ≈ 2× Trades only for legged bots. That's why they were confusing before.
- `Fix? = Y`: QQQ-IC bot carrying the call-side strike-resolution bug; data contaminated until fixed.
- Single-sided condors (only one leg opened): 31 legs flagged.
- Tiny-N bots are tracked but **not** evidence; read Trades before P/L.
