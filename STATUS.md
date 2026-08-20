# Bot Fleet — STATUS  ·  generated 2026-08-19

> **Numeric source of truth.** Auto-generated from `data/trades.csv` by `scripts/report.py`. Do not edit by hand. All figures are PAPER. Task backlog: `docs/backlog.md` (also in `dashboard.html`).

> **POST-CUTOVER LEDGER — `LEDGER_START = 2026-08-10`.** Every figure below is drawn from positions **opened on or after** that date. The v1 era is frozen in `data/archive/` and is never an input here.


## ⚠️ UNSIGNED PRE-REGISTRATION BOTS — DO NOT SWITCH ON

> The following bots have a pre-registration ledger entry with a blank, missing, or `NOT SIGNED` `SIGNED` line. No bot may be switched ON until the entry is signed and dated.

- QQQ long call
- QQQ-IC-0DTE-Fortress
- QQQ-IC-0DTE-Fortress-NoPT50
- Tasty Condor


## Should-have-fired verdict — 2026-08-19

> SUSPECT rows split by `data/bot_gates.csv` `gate_type`. **1 structural** (no declared market gate) · **0 evidenced** (signed gate evaluated against tape). The split keeps the evidenced count meaningful without hiding anything.

| Bot | PR | Class | Verdict | Reason |
|---|---|---|---|---|
| IC-SPX-Fortress-Unstopped | INC-01 | STRUCTURAL | SUSPECT | no market gate and no fill_precondition declared; silence is suspect |

## Headline
- **Total closed P/L:** $4,706  ·  71 legs  ·  15 bots
  - Directional: $-255  (SPX $-255)
  - IC: $4,681  (QQQ $181  ·  SPX $4,500)
  - OA-Mirror: $280  (SPX $120)

## Champion — IC-SPX-FastPT25-S2
- P/L **$100**  ·  7 positions (0 condors, 7 single-sided) · 7 legs  ·  7 trading days (2 green / 0 red)
- Max drawdown (daily cumulative): $0

## Focus roster — the bots you're actively perfecting  (OA: `*-Focus` groups)
> Close-to-live per pillar; for an A/B only the leading side. Select one group = per-pillar, all three = combined. Read per-bot R (readiness board), not the subtotal.

| Pillar | Bot | Status | Trades | P/L | WR |
|---|---|---|--:|--:|--:|
| IC | IC-SPX-FastPT25-S2 | ON | 7 | $100 | 29% |
| Directional | DIR-SPX-CallVIXdrop | ON | 2 | $-255 | 50% |
| OA-Mirror | 3DTE $140-$350 | ON | 2 | $70 | 100% |
| OA-Mirror | Nigiri-Paper-v1 | ON | 4 | $120 | 75% |
| **Total** | | | | **$35** | |

## Monitor — live but not focus  (OA: `Monitor` group)
> Running and watched — A/B laggards, controls, other active mirrors, the pending-decision QQQ-Fortress pair. Not promotion candidates yet.

| Pillar | Bot | Status | Trades | P/L | WR |
|---|---|---|--:|--:|--:|
| IC | GF-QQQ-IC-Canary | ON | 4 | $5 | 100% |
| IC | GF-QQQ-IC-Trail | ON | 4 | $10 | 100% |
| IC | GF-QQQ-IC-PT50 | ON | 4 | $17 | 100% |
| IC | GF-QQQ-IC-SL200 | ON | 4 | $27 | 100% |
| IC | GF-QQQ-IC-Touch0 | ON | 4 | $27 | 100% |
| IC | GF-QQQ-IC-Ride | ON | 4 | $27 | 100% |
| IC | GF-QQQ-IC-SL100 | ON | 4 | $27 | 100% |
| IC | GF-QQQ-IC-Ride-Delta | ON | 6 | $41 | 100% |
| IC | IC-SPX-FastPT25-S2-130PM | ON | 8 | $4,400 | 100% |
| OA-Mirror | Trendy-Paper-v1 | ON | 1 | $40 | 100% |
| OA-Mirror | 60min-ORB-10W-Paper-v1 | ON | 5 | $50 | 80% |
| **Total** | | | | **$4,671** | |

## Allocation audit — sizing realism  (ON bots, per-position)
> R (pnl÷risk) already cancels size, so this changes **no ranking** — it flags whether the paper sizing is realistic to carry live. Hold class sets the rule: **0DTE** recycles risk daily; **swing/multi-week** ties capital up for the whole hold (max-risk/day = concurrent open risk, not daily deploy). **1-lot bots are fill-untested at scale** — their edge won't survive the slippage of a real order size (ties to the v5-slippage task).

| Bot | Pillar | Hold | Pos | med Qty | med Risk$ | max Risk$ | Realism |
|---|---|---|--:|--:|--:|--:|:--|
| IC-SPX-FastPT25-S2 | IC | 0DTE | 7 | 10 | $4,900 | $4,900 | sized ✓ |
| IC-SPX-FastPT25-S2-130PM | IC | 0DTE | 8 | 10 | $4,750 | $4,800 | sized ✓ |
| GF-QQQ-IC-Canary | IC | 0DTE | 4 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-Trail | IC | 0DTE | 4 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-PT50 | IC | 0DTE | 4 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-SL200 | IC | 0DTE | 4 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-Touch0 | IC | 0DTE | 4 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-Ride | IC | 0DTE | 4 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-SL100 | IC | 0DTE | 4 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-Ride-Delta | IC | 0DTE | 6 | 1 | $193 | $193 | **1-lot — fill-untested** |
| DIR-SPX-CallVIXdrop | Directional | 0DTE | 2 | 1 | $640 | $640 | **1-lot — fill-untested** |
| Nigiri-Paper-v1 | OA-Mirror | 4d swing | 4 | 10 | $4,920 | $4,930 | sized ✓ |
| 3DTE $140-$350 | OA-Mirror | 5d swing | 2 | 1 | $975 | $975 | **1-lot — fill-untested** |
| Trendy-Paper-v1 | OA-Mirror | 10d multi-wk | 1 | 1 | $929 | $929 | **1-lot — fill-untested** |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 0DTE | 5 | 1 | $910 | $920 | **1-lot — fill-untested** |

> **Read:** SPX-IC + Nigiri run ~10-lot (~$4.8k/position, comparable to the champion). Every other mirror + both directional bots run **1 lot** ($0.5k–$2.9k) — realistic for tracking W/L, not for reading a live-scale edge. Sizing rule is per-bot by hold class (see backlog COCKPIT LANE step 1); the go-live target is ~$10k max risk/day with a hedge reserve carved out first.

## Hedge tournament (live-data counterfactual)
> **The productized loss autopsy.** Every real, settled (status=expired) leg replayed through the v1 hedge library — Ride/no-stop, PT+X%/SL-X% return-threshold rules, and an S2 strike-touch cut (tape-gated, 5-min grain). **Optimistic bound, not a live estimate** — every non-Ride arm assumes a fill exactly at the threshold; real fills slip. Compare rules by **R** (pnl÷risk), never $. Basis: PT/SL % are of the credit collected (`|premium|`), per `mfe_pct`/`mae_pct` already carrying that unit (verified against the ledger — see `scripts/hedge_tournament.py` docstring). **Defang: deferred v1** (17 legs marked, not modeled — needs an intraday premium-decay path not yet in the ledger).

| Rule | N | Exp(R) | Tot R | WR | maxDD-R | worst-R |
|---|--:|--:|--:|--:|--:|--:|
| ride | 17 | +5.8% | +0.98 | 100% | 0.00 | +4.2% |
| pt25 | 17 | +1.4% | +0.25 | 100% | 0.00 | +1.0% |
| pt50 | 17 | +2.9% | +0.49 | 100% | 0.00 | +2.1% |
| pt100 | 17 | +5.8% | +0.98 | 100% | 0.00 | +4.2% |
| sl50 | 17 | +1.4% | +0.24 | 47% | -0.08 | -3.2% |
| sl75 | 17 | +3.5% | +0.59 | 76% | -0.09 | -4.8% |
| sl100 | 17 | +3.8% | +0.64 | 82% | -0.06 | -6.4% |
| sl130 | 17 | +4.2% | +0.71 | 88% | -0.08 | -8.3% |
| s2 | 12 | +5.9% | +0.71 | 100% | 0.00 | +4.2% |

#### Per-bot cut  (Ride vs SL75 — the mid-spectrum published rung)
| Bot | N | Ride Exp(R) | SL75 Exp(R) | Δ |
|---|--:|--:|--:|--:|
| IC-SPX-FastPT25-S2-130PM | 16 | +5.8% | +3.4% | -2.4pp |
| 3DTE $140-$350 | 1 | +4.7% | +4.7% | +0.0pp |

#### Regime cut  (Ride vs SL75, by tape-derived regime label)
| Regime | N | Ride Exp(R) | SL75 Exp(R) |
|---|--:|--:|--:|
| Chop | 13 | +5.8% | +4.4% |
| n/a | 4 | +5.5% | +0.4% |

> N is small and concentrated in the last few tape-covered trading days (tape.py is new); the S2 arm and the regime cut will thicken as more days accrue. Read this as an early ranking to cross-check the LEAN/OA backtest tournament, not a standalone verdict.

## Trade-window heat map — when do shorts actually get touched (hour x regime)
> **The 11am-vs-1:30 question, generalized.** Every ledger position's worst-adverse-excursion (MAE) timestamp, bucketed by hour-of-day x tape-derived regime (Drift/Trend/Chop/n-a). `touch %` = short-strike touch rate, scored only on positions with same-day tape coverage (a small, recent subset — most history predates `tape.py`); `MAE` = mean adverse excursion as % of credit, computed on ALL positions in the bucket regardless of tape coverage. Cells are `n=… · touch …% · MAE …%`; blank touch% = no tape-covered position fell in that cell. **Small-n cells are directional, not conclusive** — read the n before the rate.

| Hour | Chop | Drift | n/a |
|---|---|---|---|
| 09:30-10 | n=1 · MAE -2.1% | — | — |
| 10-11 | n=2 · touch 0% · MAE -0.1% | — | n=1 · MAE -0.3% |
| 11-12 | n=10 · touch 0% · MAE -0.1% | — | n=1 · MAE -0.2% |
| 12-13 | n=3 · touch 50% · MAE -0.8% | — | n=1 · MAE -0.4% |
| 13-14 | n=16 · touch 0% · MAE -0.3% | n=12 · touch 0% · MAE -0.1% | — |
| 14-15 | n=1 · touch 0% · MAE -0.8% | n=13 · touch 0% · MAE -0.7% | n=2 · MAE -0.6% |

> **Read:** touches cluster at **12-13 (Chop)** — 1 of 2 tape-covered position(s) scored there touched (touch rate 50%). Tape coverage is thin (5 days) — treat as an early signal, not a verdict.

## Lessons index — tagged, searchable  (data/lessons.csv)
> Every graded bot-day's "day's lesson" (from the brief JSON's Verdict row; session-log fallback only for dates the brief never covered), tagged from a fixed vocabulary (`entry-timing · hedge · filter · regime · sizing · other`) by simple keyword rules (see `scripts/lessons.py` docstring) — not an ML classifier. Grouped by tag, most recent first.

**Tag counts:** 

## Per-bot (sorted by P/L)
| Bot | Pillar | Und | Role | Status | Trades | Legs | P/L | WR | Fix? |
|---|---|---|---|---|--:|--:|--:|--:|:--:|
| DIR-SPX-CallVIXdrop | Directional | SPX | experiment | ON | 2 | 2 | $-255 | 50% | - |
| GF-QQQ-IC-Canary | IC | QQQ | instrument | ON | 4 | 4 | $5 | 100% | - |
| GF-QQQ-IC-Trail | IC | QQQ | experiment | ON | 4 | 4 | $10 | 100% | - |
| GF-QQQ-IC-PT50 | IC | QQQ | experiment | ON | 4 | 4 | $17 | 100% | - |
| GF-QQQ-IC-SL200 | IC | QQQ | experiment | ON | 4 | 4 | $27 | 100% | - |
| GF-QQQ-IC-Touch0 | IC | QQQ | experiment | ON | 4 | 4 | $27 | 100% | - |
| GF-QQQ-IC-Ride | IC | QQQ | control | ON | 4 | 4 | $27 | 100% | - |
| GF-QQQ-IC-SL100 | IC | QQQ | experiment | ON | 4 | 4 | $27 | 100% | - |
| Trendy-Paper-v1 | OA-Mirror | — | mirror-watch | ON | 1 | 1 | $40 | 100% | - |
| GF-QQQ-IC-Ride-Delta | IC | QQQ | experiment | ON | 6 | 6 | $41 | 100% | - |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | SPX | mirror-watch | ON | 5 | 5 | $50 | 80% | - |
| 3DTE $140-$350 | OA-Mirror | SPX | mirror-watch | ON | 2 | 2 | $70 | 100% | - |
| IC-SPX-FastPT25-S2 | IC | SPX | live-candidate | ON | 7 | 7 | $100 | 29% | - |
| Nigiri-Paper-v1 | OA-Mirror | — | mirror-watch | ON | 4 | 4 | $120 | 75% | - |
| IC-SPX-FastPT25-S2-130PM | IC | SPX | experiment | ON | 8 | 16 | $4,400 | 100% | - |

## Readiness board — per-condor, gated (the graduation view)
> **Grain = condor** (legs summed), not leg. Six ordered gates; the **first red (○) gate is the named blocker**. `●`=pass `○`=fail `·`=pending. Exp(R) shows the **bootstrap 95% CI** (replaces the t-stat). Stage: INCUBATE→VALIDATE→CANDIDATE→LIVE-READY (LIVE = real capital). Controls & mirror-watch are listed separately — they can't graduate by design.
> **Gates:** G1 clean data (no strike-bug, single-sided excluded) · G2 ≥20 clean condors · G3 Exp(R)>0 w/ 95% CI above 0 · G4 maxDD-R within cap (RoE $ cap still a `<FILL>` blank) · G5 instruction-mirror ≥90% (from the daily brief / `data/compliance.csv`; pending until ≥5 graded days) · G6 OOS/regime robustness.

| Bot | Role | Stage | Gates | n | Exp(R) [95% CI] | Blocker |
|---|---|---|:--:|--:|--:|---|
| IC-SPX-FastPT25-S2-130PM | experiment | CANDIDATE | ●○●●·· | 8 | +11.6% [+11.1, +12.1] | G2: 8 clean condors (need 20) |
| GF-QQQ-IC-Ride-Delta | experiment | CANDIDATE | ●○●●·· | 6 | +3.6% [+3.1, +4.1] | G2: 6 clean condors (need 20) |
| GF-QQQ-IC-SL200 | experiment | CANDIDATE | ●○●●·· | 4 | +3.5% [+3.1, +4.3] | G2: 4 clean condors (need 20) |
| GF-QQQ-IC-Touch0 | experiment | CANDIDATE | ●○●●·· | 4 | +3.5% [+3.1, +4.3] | G2: 4 clean condors (need 20) |
| GF-QQQ-IC-SL100 | experiment | CANDIDATE | ●○●●·· | 4 | +3.5% [+3.1, +4.3] | G2: 4 clean condors (need 20) |
| GF-QQQ-IC-PT50 | experiment | CANDIDATE | ●○●●·· | 4 | +2.2% [+2.1, +2.5] | G2: 4 clean condors (need 20) |
| GF-QQQ-IC-Trail | experiment | CANDIDATE | ●○●●·· | 4 | +1.3% [+0.5, +2.5] | G2: 4 clean condors (need 20) |
| GF-QQQ-IC-Canary | instrument | CANDIDATE | ●○●●·· | 4 | +0.6% [+0.5, +0.9] | G2: 4 clean condors (need 20) |
| IC-SPX-FastPT25-S2 | live-candidate | VALIDATE | ●○○●·· | 7 | +0.3% [+0.0, +0.6] | G2: 7 clean condors (need 20) |
| DIR-SPX-CallVIXdrop | experiment | VALIDATE | ●○○●·· | 2 | -19.6% [-50.0, +10.7] | G2: 2 clean condors (need 20) |

#### Non-graduating (controls / mirror-watch — tracked, can't go live)
| Bot | Role | Gates | n | Exp(R) [95% CI] | Note |
|---|---|:--:|--:|--:|---|
| 3DTE $140-$350 | mirror-watch | ●○●●·· | 2 | +3.6% [+2.6, +4.7] | G2: 2 clean condors (need 20) |
| GF-QQQ-IC-Ride | control | ●○●●·· | 4 | +3.5% [+3.1, +4.3] | G2: 4 clean condors (need 20) |
| Nigiri-Paper-v1 | mirror-watch | ●○●●·· | 4 | +0.6% [+0.2, +1.2] | G2: 4 clean condors (need 20) |
| Trendy-Paper-v1 | mirror-watch | ●○○●·· | 1 | +4.3% — | G2: 1 clean condors (need 20) |
| 60min-ORB-10W-Paper-v1 | mirror-watch | ●○○●·· | 5 | +1.2% [-7.7, +5.8] | G2: 5 clean condors (need 20) |

## Scorecard — normalized (Return on Risk) · legacy per-LEG view
> ⚠️ **Per-LEG grain** (kept for continuity) — for the graduation decision use the **Readiness board** above (per-condor, gated). Each trade = **pnl ÷ capital-at-risk** ("R"), so allocation and contract size cancel out. Sorted by expectancy. t-stat blows up for low-variance grinders (e.g. 3DTE) — don't rank on it alone.

### Ranked (n ≥ 20)
| Bot | Pillar | n | Exp(R) | t | Tot R | maxDD-R | WR |
|---|---|--:|--:|--:|--:|--:|--:|

### Provisional (n < 20 — tracked, not ranked; samples too small to trust)
| Bot | Pillar | n | Exp(R) | Tot R | raw P/L |
|---|---|--:|--:|--:|--:|
| IC-SPX-FastPT25-S2-130PM | IC | 16 | +0.058 | +0.9 | $4,400 |
| Trendy-Paper-v1 | OA-Mirror | 1 | +0.043 | +0.0 | $40 |
| 3DTE $140-$350 | OA-Mirror | 2 | +0.036 | +0.1 | $70 |
| GF-QQQ-IC-Ride-Delta | IC | 6 | +0.036 | +0.2 | $41 |
| GF-QQQ-IC-SL200 | IC | 4 | +0.035 | +0.1 | $27 |
| GF-QQQ-IC-Touch0 | IC | 4 | +0.035 | +0.1 | $27 |
| GF-QQQ-IC-Ride | IC | 4 | +0.035 | +0.1 | $27 |
| GF-QQQ-IC-SL100 | IC | 4 | +0.035 | +0.1 | $27 |
| GF-QQQ-IC-PT50 | IC | 4 | +0.022 | +0.1 | $17 |
| GF-QQQ-IC-Trail | IC | 4 | +0.013 | +0.1 | $10 |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 5 | +0.012 | +0.1 | $50 |
| GF-QQQ-IC-Canary | IC | 4 | +0.006 | +0.0 | $5 |
| Nigiri-Paper-v1 | OA-Mirror | 4 | +0.006 | +0.0 | $120 |
| IC-SPX-FastPT25-S2 | IC | 7 | +0.003 | +0.0 | $100 |
| DIR-SPX-CallVIXdrop | Directional | 2 | -0.196 | -0.4 | $-255 |

### Decision rules (read against the right column)
- **Kill** — Exp(R) < 0 held with conviction (|t| ≳ 2, or n large). Raw P/L size is irrelevant.
- **Graduate** — Exp(R) > 0 **and** |t| ≳ 2 **and** n ≥ threshold (edge is real, not noise).
- **Size live capital** — among graduates, weight by Tot R + low maxDD-R (consistency); never size on raw P/L.
- **Exp(R)** = avg return per $1 risked. **Tot R** = size-free analog of total P/L. **maxDD-R** = worst cumulative-R drawdown (risk shape). **t** = evidence the edge is real.

---

## Decidability countdown — per armed arm (PROJECTION, not evidence)
> **This is a forward projection, not a result.** It extrapolates the recent fire rate and assumes that rate holds. Calendar projection skips weekends and does **not** model market holidays, so the date is approximate. The unit of account is the **POSITION** (a two-sided condor = two spread rows paired by `trade_id`); *n* = 100 means **100 condors**, not 100 legs. One-sided spreads are listed separately and do **not** count toward the 100-condor target. The recent window is the last **20 trading days**; the post-cutover ledger currently contributes **8 trading days** to this window.

| Arm | Pillar | Current condors, positions | One-sided positions, spreads | Closes in 20-trading-day window | Fire rate (closes/trading-day, condors) | Projected 100-condor date |
|---|---|--:|--:|--:|--:|---|
| 3DTE $140-$350 | OA-Mirror | 2 | 0 | 2 | insufficient data | insufficient data |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 0 | 5 | 0 | insufficient data | insufficient data |
| DIR-SPX-CallVIXdrop | Directional | 2 | 0 | 2 | insufficient data | insufficient data |
| DIR-SPX-PutVIX22-SL75 | Directional | 0 | 0 | 0 | insufficient data | insufficient data |
| Friday 14 DTE Broken Wing IB (B-70) | OA-Mirror | 0 | 0 | 0 | insufficient data | insufficient data |
| GF-QQQ-IC-Canary | IC | 0 | 4 | 0 | insufficient data | insufficient data |
| GF-QQQ-IC-PT50 | IC | 0 | 4 | 0 | insufficient data | insufficient data |
| GF-QQQ-IC-Ride | IC | 0 | 4 | 0 | insufficient data | insufficient data |
| GF-QQQ-IC-Ride-Delta | IC | 0 | 6 | 0 | insufficient data | insufficient data |
| GF-QQQ-IC-SL100 | IC | 0 | 4 | 0 | insufficient data | insufficient data |
| GF-QQQ-IC-SL200 | IC | 0 | 4 | 0 | insufficient data | insufficient data |
| GF-QQQ-IC-Touch0 | IC | 0 | 4 | 0 | insufficient data | insufficient data |
| GF-QQQ-IC-Trail | IC | 0 | 4 | 0 | insufficient data | insufficient data |
| IC-SPX-FastPT25-S2 | IC | 0 | 7 | 0 | insufficient data | insufficient data |
| IC-SPX-FastPT25-S2-130PM | IC | 8 | 0 | 8 | 1.00 | 2026-12-25 |
| IC-SPX-Fortress-Unstopped | IC | 0 | 0 | 0 | insufficient data | insufficient data |
| Nigiri-Paper-v1 | OA-Mirror | 0 | 4 | 0 | insufficient data | insufficient data |
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | 0 | 0 | 0 | insufficient data | insufficient data |
| Trendy-Paper-v1 | OA-Mirror | 0 | 1 | 0 | insufficient data | insufficient data |

## Caveats
- **Positions:** 63 total (8 condors, 55 single-sided)  ·  71 legs.
- A condor has two spread rows paired by `trade_id` with `single_sided=False`; a single-sided position is any position that is not a condor (one spread row or `single_sided=True`). **Legs = OA position rows** (matches OA's "Positions" count). Win rate shown is per-position.
- A combined-`ironcondor` bot logs 1 leg per condor; a legged bot logs 2 — so Legs ≈ 2× condors only for legged bots. That's why they were confusing before.
- `Fix? = Y`: QQQ-IC bot carrying the call-side strike-resolution bug; data contaminated until fixed.
- Single-sided positions (not condors): 55 positions.
- Tiny-N bots are tracked but **not** evidence; read Trades before P/L.
