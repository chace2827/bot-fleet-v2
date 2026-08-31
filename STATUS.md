# Bot Fleet — STATUS  ·  generated 2026-08-31

> **Numeric source of truth.** Auto-generated from `data/trades.csv` by `scripts/report.py`. Do not edit by hand. All figures are PAPER. Task backlog: `docs/backlog.md` (also in `dashboard.html`).

> **POST-CUTOVER LEDGER — `LEDGER_START = 2026-08-10`.** Every figure below is drawn from positions **opened on or after** that date. The v1 era is frozen in `data/archive/` and is never an input here.


## ⚠️ UNSIGNED PRE-REGISTRATION BOTS — DO NOT SWITCH ON

> The following bots have a pre-registration ledger entry with a blank, missing, or `NOT SIGNED` `SIGNED` line. No bot may be switched ON until the entry is signed and dated.

- QQQ long call
- QQQ-IC-0DTE-Fortress
- Tasty Condor


## Should-have-fired verdict — 2026-08-31

> SUSPECT rows split by `data/bot_gates.csv` `gate_type`. **1 structural** (no declared market gate) · **0 evidenced** (signed gate evaluated against tape). The split keeps the evidenced count meaningful without hiding anything.

| Bot | PR | Class | Verdict | Reason |
|---|---|---|---|---|
| IC-SPX-Fortress-Unstopped | INC-01 | STRUCTURAL | SUSPECT | no market gate and no fill_precondition declared; silence is suspect |

## Headline
- **Total closed P/L:** $4,557  ·  205 legs  ·  18 bots
  - Directional: $-955  (SPX $-955)
  - IC: $4,710  (QQQ $10  ·  SPX $4,700)
  - OA-Mirror: $802  (SPX $210)

## Champion — IC-SPX-FastPT25-S2
- P/L **$400**  ·  16 positions (1 condor, 15 single-sided) · 17 legs  ·  14 trading days (6 green / 1 red)
- Max drawdown (daily cumulative): $-50

## Focus roster — the bots you're actively perfecting  (OA: `*-Focus` groups)
> Close-to-live per pillar; for an A/B only the leading side. Select one group = per-pillar, all three = combined. Read per-bot R (readiness board), not the subtotal.

| Pillar | Bot | Status | Trades | P/L | WR |
|---|---|---|--:|--:|--:|
| IC | IC-SPX-FastPT25-S2 | ON | 16 | $400 | 44% |
| Directional | DIR-SPX-CallVIXdrop | ON | 4 | $-955 | 25% |
| OA-Mirror | Friday 14 DTE Broken Wing IB (B-70) | ON | 1 | $140 | 100% |
| OA-Mirror | 3DTE $140-$350 | ON | 4 | $150 | 100% |
| OA-Mirror | Nigiri-Paper-v1 | ON | 10 | $350 | 90% |
| **Total** | | | | **$85** | |

## Monitor — live but not focus  (OA: `Monitor` group)
> Running and watched — A/B laggards, controls, other active mirrors, the pending-decision QQQ-Fortress pair. Not promotion candidates yet.

| Pillar | Bot | Status | Trades | P/L | WR |
|---|---|---|--:|--:|--:|
| IC | QQQ-IC-0DTE-Fortress-NoPT50 | ON | 1 | $-338 | 0% |
| IC | GF-QQQ-IC-Canary | ON | 11 | $5 | 91% |
| IC | GF-QQQ-IC-Trail | ON | 11 | $16 | 73% |
| IC | GF-QQQ-IC-SL100 | ON | 11 | $30 | 64% |
| IC | GF-QQQ-IC-SL200 | ON | 11 | $35 | 82% |
| IC | GF-QQQ-IC-PT50 | ON | 11 | $43 | 91% |
| IC | GF-QQQ-IC-Ride | ON | 11 | $64 | 91% |
| IC | GF-QQQ-IC-Touch0 | ON | 11 | $64 | 91% |
| IC | IC-SPX-Fortress-Unstopped | ON | 1 | $100 | 100% |
| IC | IC-SPX-FastPT25-S2-130PM | ON | 16 | $4,200 | 88% |
| OA-Mirror | 60min-ORB-10W-Paper-v1 | ON | 9 | $60 | 78% |
| OA-Mirror | Trendy-Paper-v1 | ON | 2 | $102 | 100% |
| **Total** | | | | **$4,381** | |

**Archive (OA: `Archive` group):** 1 off/dead bots · $91 closed — excluded from the working view (still exported for the ledger).

## Allocation audit — sizing realism  (ON bots, per-position)
> R (pnl÷risk) already cancels size, so this changes **no ranking** — it flags whether the paper sizing is realistic to carry live. Hold class sets the rule: **0DTE** recycles risk daily; **swing/multi-week** ties capital up for the whole hold (max-risk/day = concurrent open risk, not daily deploy). **1-lot bots are fill-untested at scale** — their edge won't survive the slippage of a real order size (ties to the v5-slippage task).

| Bot | Pillar | Hold | Pos | med Qty | med Risk$ | max Risk$ | Realism |
|---|---|---|--:|--:|--:|--:|:--|
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | 0DTE | 1 | 26 | $4,940 | $4,940 | sized ✓ |
| IC-SPX-Fortress-Unstopped | IC | 0DTE | 1 | 10 | $4,900 | $4,900 | sized ✓ |
| IC-SPX-FastPT25-S2 | IC | 0DTE | 16 | 10 | $4,900 | $4,900 | sized ✓ |
| IC-SPX-FastPT25-S2-130PM | IC | 0DTE | 16 | 10 | $4,750 | $4,900 | sized ✓ |
| GF-QQQ-IC-Canary | IC | 0DTE | 11 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-Trail | IC | 0DTE | 11 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-SL100 | IC | 0DTE | 11 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-SL200 | IC | 0DTE | 11 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-PT50 | IC | 0DTE | 11 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-Ride | IC | 0DTE | 11 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-Touch0 | IC | 0DTE | 11 | 1 | $193 | $193 | **1-lot — fill-untested** |
| DIR-SPX-CallVIXdrop | Directional | 0DTE | 4 | 1 | $640 | $675 | **1-lot — fill-untested** |
| Nigiri-Paper-v1 | OA-Mirror | 4d swing | 10 | 10 | $4,910 | $4,930 | sized ✓ |
| Friday 14 DTE Broken Wing IB (B-70) | OA-Mirror | 14d multi-wk | 1 | 1 | $1,960 | $1,960 | **1-lot — fill-untested** |
| 3DTE $140-$350 | OA-Mirror | 5d swing | 4 | 1 | $955 | $975 | **1-lot — fill-untested** |
| Trendy-Paper-v1 | OA-Mirror | 10d multi-wk | 2 | 1 | $932 | $932 | **1-lot — fill-untested** |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 0DTE | 9 | 1 | $915 | $930 | **1-lot — fill-untested** |

> **Read:** SPX-IC + Nigiri run ~10-lot (~$4.8k/position, comparable to the champion). Every other mirror + both directional bots run **1 lot** ($0.5k–$2.9k) — realistic for tracking W/L, not for reading a live-scale edge. Sizing rule is per-bot by hold class (see backlog COCKPIT LANE step 1); the go-live target is ~$10k max risk/day with a hedge reserve carved out first.

## Hedge tournament (live-data counterfactual)
> **The productized loss autopsy.** Every real, settled (status=expired) leg replayed through the v1 hedge library — Ride/no-stop, PT+X%/SL-X% return-threshold rules, and an S2 strike-touch cut (tape-gated, 5-min grain). **Optimistic bound, not a live estimate** — every non-Ride arm assumes a fill exactly at the threshold; real fills slip. Compare rules by **R** (pnl÷risk), never $. Basis: PT/SL % are of the credit collected (`|premium|`), per `mfe_pct`/`mae_pct` already carrying that unit (verified against the ledger — see `scripts/hedge_tournament.py` docstring). **Defang: deferred v1** (21 legs marked, not modeled — needs an intraday premium-decay path not yet in the ledger).

| Rule | N | Exp(R) | Tot R | WR | maxDD-R | worst-R |
|---|--:|--:|--:|--:|--:|--:|
| ride | 21 | +5.5% | +1.15 | 100% | 0.00 | +2.0% |
| pt25 | 21 | +1.4% | +0.29 | 100% | 0.00 | +0.5% |
| pt50 | 21 | +2.8% | +0.59 | 100% | 0.00 | +1.0% |
| pt100 | 21 | +5.5% | +1.15 | 100% | 0.00 | +2.0% |
| sl50 | 21 | +1.6% | +0.33 | 48% | -0.08 | -3.2% |
| sl75 | 21 | +3.4% | +0.71 | 76% | -0.09 | -4.8% |
| sl100 | 21 | +3.6% | +0.75 | 81% | -0.06 | -6.4% |
| sl130 | 21 | +3.9% | +0.81 | 86% | -0.08 | -8.3% |
| s2 | 16 | +3.8% | +0.61 | 94% | -0.24 | -24.1% |

#### Per-bot cut  (Ride vs SL75 — the mid-spectrum published rung)
| Bot | N | Ride Exp(R) | SL75 Exp(R) | Δ |
|---|--:|--:|--:|--:|
| IC-SPX-FastPT25-S2-130PM | 18 | +5.9% | +3.4% | -2.5pp |
| 3DTE $140-$350 | 1 | +4.7% | +4.7% | +0.0pp |
| IC-SPX-FastPT25-S2 | 2 | +2.0% | +2.0% | +0.0pp |

#### Regime cut  (Ride vs SL75, by tape-derived regime label)
| Regime | N | Ride Exp(R) | SL75 Exp(R) |
|---|--:|--:|--:|
| Chop | 17 | +5.5% | +4.1% |
| n/a | 4 | +5.5% | +0.4% |

> N is small and concentrated in the last few tape-covered trading days (tape.py is new); the S2 arm and the regime cut will thicken as more days accrue. Read this as an early ranking to cross-check the LEAN/OA backtest tournament, not a standalone verdict.

## Trade-window heat map — when do shorts actually get touched (hour x regime)
> **The 11am-vs-1:30 question, generalized.** Every ledger position's worst-adverse-excursion (MAE) timestamp, bucketed by hour-of-day x tape-derived regime (Drift/Trend/Chop/n-a). `touch %` = short-strike touch rate, scored only on positions with same-day tape coverage (a small, recent subset — most history predates `tape.py`); `MAE` = mean adverse excursion as % of credit, computed on ALL positions in the bucket regardless of tape coverage. Cells are `n=… · touch …% · MAE …%`; blank touch% = no tape-covered position fell in that cell. **Small-n cells are directional, not conclusive** — read the n before the rate.

| Hour | Chop | Drift | n/a |
|---|---|---|---|
| 09:30-10 | n=1 · MAE -2.1% | — | n=2 · MAE -0.5% |
| 10-11 | n=2 · touch 0% · MAE -0.1% | — | n=4 · MAE -0.4% |
| 11-12 | n=11 · touch 0% · MAE -0.1% | — | n=10 · MAE -0.3% |
| 12-13 | n=3 · touch 50% · MAE -0.8% | — | n=5 · MAE -0.5% |
| 13-14 | n=24 · touch 33% · MAE -0.6% | n=12 · touch 0% · MAE -0.1% | n=57 · MAE -0.9% |
| 14-15 | n=3 · touch 0% · MAE -0.9% | n=13 · touch 0% · MAE -0.7% | n=6 · MAE -0.7% |
| 15-16 | — | — | n=3 · MAE -1.1% |

> **Read:** touches cluster at **12-13 (Chop)** — 1 of 2 tape-covered position(s) scored there touched (touch rate 50%). Tape coverage is thin (5 days) — treat as an early signal, not a verdict.

## Lessons index — tagged, searchable  (data/lessons.csv)
> Every graded bot-day's "day's lesson" (from the brief JSON's Verdict row; session-log fallback only for dates the brief never covered), tagged from a fixed vocabulary (`entry-timing · hedge · filter · regime · sizing · other`) by simple keyword rules (see `scripts/lessons.py` docstring) — not an ML classifier. Grouped by tag, most recent first.

**Tag counts:** 

## Per-bot (sorted by P/L)
| Bot | Pillar | Und | Role | Status | Trades | Legs | P/L | WR | Fix? |
|---|---|---|---|---|--:|--:|--:|--:|:--:|
| DIR-SPX-CallVIXdrop | Directional | SPX | experiment | ON | 4 | 4 | $-955 | 25% | - |
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | QQQ | experiment | ON | 1 | 2 | $-338 | 0% | Y |
| GF-QQQ-IC-Canary | IC | QQQ | instrument | ON | 11 | 15 | $5 | 91% | - |
| GF-QQQ-IC-Trail | IC | QQQ | experiment | ON | 11 | 15 | $16 | 73% | - |
| GF-QQQ-IC-SL100 | IC | QQQ | experiment | ON | 11 | 15 | $30 | 64% | - |
| GF-QQQ-IC-SL200 | IC | QQQ | experiment | ON | 11 | 15 | $35 | 82% | - |
| GF-QQQ-IC-PT50 | IC | QQQ | experiment | ON | 11 | 15 | $43 | 91% | - |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | SPX | mirror-watch | ON | 9 | 9 | $60 | 78% | - |
| GF-QQQ-IC-Ride | IC | QQQ | control | ON | 11 | 15 | $64 | 91% | - |
| GF-QQQ-IC-Touch0 | IC | QQQ | experiment | ON | 11 | 15 | $64 | 91% | - |
| GF-QQQ-IC-Ride-Delta | IC | QQQ | experiment | OFF | 15 | 18 | $91 | 93% | - |
| IC-SPX-Fortress-Unstopped | IC | SPX | control | ON | 1 | 1 | $100 | 100% | - |
| Trendy-Paper-v1 | OA-Mirror | — | mirror-watch | ON | 2 | 2 | $102 | 100% | - |
| Friday 14 DTE Broken Wing IB (B-70) | OA-Mirror | — | mirror-watch | ON | 1 | 1 | $140 | 100% | - |
| 3DTE $140-$350 | OA-Mirror | SPX | mirror-watch | ON | 4 | 4 | $150 | 100% | - |
| Nigiri-Paper-v1 | OA-Mirror | — | mirror-watch | ON | 10 | 10 | $350 | 90% | - |
| IC-SPX-FastPT25-S2 | IC | SPX | live-candidate | ON | 16 | 17 | $400 | 44% | - |
| IC-SPX-FastPT25-S2-130PM | IC | SPX | experiment | ON | 16 | 32 | $4,200 | 88% | - |

## Readiness board — per-condor, gated (the graduation view)
> **Grain = condor** (legs summed), not leg. Six ordered gates; the **first red (○) gate is the named blocker**. `●`=pass `○`=fail `·`=pending. Exp(R) shows the **bootstrap 95% CI** (replaces the t-stat). Stage: INCUBATE→VALIDATE→CANDIDATE→LIVE-READY (LIVE = real capital). Controls & mirror-watch are listed separately — they can't graduate by design.
> **Gates:** G1 clean data (no strike-bug, single-sided excluded) · G2 ≥20 clean condors · G3 Exp(R)>0 w/ 95% CI above 0 · G4 maxDD-R within cap (RoE $ cap still a `<FILL>` blank) · G5 instruction-mirror ≥90% (from the daily brief / `data/compliance.csv`; pending until ≥5 graded days) · G6 OOS/regime robustness.

| Bot | Role | Stage | Gates | n | Exp(R) [95% CI] | Blocker |
|---|---|---|:--:|--:|--:|---|
| IC-SPX-FastPT25-S2-130PM | experiment | VALIDATE | ●○○●·· | 16 | +5.5% [-2.9, +11.6] | G2: 16 clean condors (need 20) |
| IC-SPX-FastPT25-S2 | live-candidate | VALIDATE | ●○○●·· | 1 | +4.1% — | G2: 1 clean condors (need 20) |
| GF-QQQ-IC-Ride-Delta | experiment | VALIDATE | ●○○●·· | 3 | +2.4% [-6.3, +7.3] | G2: 3 clean condors (need 20) |
| GF-QQQ-IC-Touch0 | experiment | VALIDATE | ●○○●·· | 4 | +2.3% [-3.2, +6.2] | G2: 4 clean condors (need 20) |
| GF-QQQ-IC-PT50 | experiment | VALIDATE | ●○○●·· | 4 | +1.8% [-3.3, +4.5] | G2: 4 clean condors (need 20) |
| GF-QQQ-IC-Trail | experiment | VALIDATE | ●○○●·· | 4 | -0.0% [-4.1, +3.1] | G2: 4 clean condors (need 20) |
| GF-QQQ-IC-SL100 | experiment | VALIDATE | ●○○●·· | 4 | -0.3% [-3.1, +4.0] | G2: 4 clean condors (need 20) |
| GF-QQQ-IC-Canary | instrument | VALIDATE | ●○○●·· | 4 | -0.5% [-5.4, +2.3] | G2: 4 clean condors (need 20) |
| GF-QQQ-IC-SL200 | experiment | VALIDATE | ●○○●·· | 4 | -1.5% [-7.6, +4.7] | G2: 4 clean condors (need 20) |
| DIR-SPX-CallVIXdrop | experiment | VALIDATE | ●○○●·· | 4 | -36.6% [-53.6, -5.2] | G2: 4 clean condors (need 20) |
| QQQ-IC-0DTE-Fortress-NoPT50 | experiment | VALIDATE | ○○○●·· | 1 | -6.8% — | G1: strike-bug contamination |

#### Non-graduating (controls / mirror-watch — tracked, can't go live)
| Bot | Role | Gates | n | Exp(R) [95% CI] | Note |
|---|---|:--:|--:|--:|---|
| Trendy-Paper-v1 | mirror-watch | ●○●●·· | 2 | +5.5% [+4.3, +6.7] | G2: 2 clean condors (need 20) |
| 3DTE $140-$350 | mirror-watch | ●○●●·· | 4 | +3.9% [+3.1, +4.7] | G2: 4 clean condors (need 20) |
| Nigiri-Paper-v1 | mirror-watch | ●○●●·· | 10 | +0.7% [+0.4, +1.0] | G2: 10 clean condors (need 20) |
| Friday 14 DTE Broken Wing IB (B-70) | mirror-watch | ●○○●·· | 1 | +7.1% — | G2: 1 clean condors (need 20) |
| GF-QQQ-IC-Ride | control | ●○○●·· | 4 | +2.3% [-3.2, +6.2] | G2: 4 clean condors (need 20) |
| IC-SPX-Fortress-Unstopped | control | ●○○●·· | 1 | +2.0% — | G2: 1 clean condors (need 20) |
| 60min-ORB-10W-Paper-v1 | mirror-watch | ●○○●·· | 9 | +0.5% [-6.9, +5.6] | G2: 9 clean condors (need 20) |

## Scorecard — normalized (Return on Risk) · legacy per-LEG view
> ⚠️ **Per-LEG grain** (kept for continuity) — for the graduation decision use the **Readiness board** above (per-condor, gated). Each trade = **pnl ÷ capital-at-risk** ("R"), so allocation and contract size cancel out. Sorted by expectancy. t-stat blows up for low-variance grinders (e.g. 3DTE) — don't rank on it alone.

### Ranked (n ≥ 20)
| Bot | Pillar | n | Exp(R) | t | Tot R | maxDD-R | WR |
|---|---|--:|--:|--:|--:|--:|--:|
| IC-SPX-FastPT25-S2-130PM | IC | 32 | +0.028 | 1.5 | +0.9 | -0.8 | 94% |

### Provisional (n < 20 — tracked, not ranked; samples too small to trust)
| Bot | Pillar | n | Exp(R) | Tot R | raw P/L |
|---|---|--:|--:|--:|--:|
| Friday 14 DTE Broken Wing IB (B-70) | OA-Mirror | 1 | +0.071 | +0.1 | $140 |
| Trendy-Paper-v1 | OA-Mirror | 2 | +0.055 | +0.1 | $102 |
| 3DTE $140-$350 | OA-Mirror | 4 | +0.039 | +0.2 | $150 |
| GF-QQQ-IC-Ride-Delta | IC | 18 | +0.026 | +0.5 | $91 |
| GF-QQQ-IC-Ride | IC | 15 | +0.022 | +0.3 | $64 |
| GF-QQQ-IC-Touch0 | IC | 15 | +0.022 | +0.3 | $64 |
| IC-SPX-Fortress-Unstopped | IC | 1 | +0.020 | +0.0 | $100 |
| GF-QQQ-IC-PT50 | IC | 15 | +0.015 | +0.2 | $43 |
| GF-QQQ-IC-SL200 | IC | 15 | +0.012 | +0.2 | $35 |
| GF-QQQ-IC-SL100 | IC | 15 | +0.010 | +0.2 | $30 |
| Nigiri-Paper-v1 | OA-Mirror | 10 | +0.007 | +0.1 | $350 |
| GF-QQQ-IC-Trail | IC | 15 | +0.005 | +0.1 | $16 |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 9 | +0.005 | +0.0 | $60 |
| IC-SPX-FastPT25-S2 | IC | 17 | +0.005 | +0.1 | $400 |
| GF-QQQ-IC-Canary | IC | 15 | +0.002 | +0.0 | $5 |
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | 2 | -0.034 | -0.1 | $-338 |
| DIR-SPX-CallVIXdrop | Directional | 4 | -0.366 | -1.5 | $-955 |

### Decision rules (read against the right column)
- **Kill** — Exp(R) < 0 held with conviction (|t| ≳ 2, or n large). Raw P/L size is irrelevant.
- **Graduate** — Exp(R) > 0 **and** |t| ≳ 2 **and** n ≥ threshold (edge is real, not noise).
- **Size live capital** — among graduates, weight by Tot R + low maxDD-R (consistency); never size on raw P/L.
- **Exp(R)** = avg return per $1 risked. **Tot R** = size-free analog of total P/L. **maxDD-R** = worst cumulative-R drawdown (risk shape). **t** = evidence the edge is real.

---

## Decidability countdown — per armed arm (PROJECTION, not evidence)
> **This is a forward projection, not a result.** It extrapolates the recent fire rate and assumes that rate holds. Calendar projection skips weekends and does **not** model market holidays, so the date is approximate. The unit of account is the **POSITION** (a two-sided condor = two spread rows paired by `trade_id`); *n* = 100 means **100 condors**, not 100 legs. One-sided spreads are listed separately and do **not** count toward the 100-condor target. The recent window is the last **20 trading days**; the post-cutover ledger currently contributes **16 trading days** to this window.

| Arm | Pillar | Current condors, positions | One-sided positions, spreads | Closes in 20-trading-day window | Fire rate (closes/trading-day, condors) | Projected 100-condor date |
|---|---|--:|--:|--:|--:|---|
| 3DTE $140-$350 | OA-Mirror | 4 | 0 | 4 | 0.25 | 2028-02-18 |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 0 | 9 | 0 | insufficient data | insufficient data |
| DIR-SPX-CallVIXdrop | Directional | 4 | 0 | 4 | 0.25 | 2028-02-18 |
| DIR-SPX-PutVIX22-SL75 | Directional | 0 | 0 | 0 | insufficient data | insufficient data |
| Friday 14 DTE Broken Wing IB (B-70) | OA-Mirror | 1 | 0 | 1 | insufficient data | insufficient data |
| GF-QQQ-IC-Canary | IC | 4 | 7 | 4 | 0.25 | 2028-02-18 |
| GF-QQQ-IC-PT50 | IC | 4 | 7 | 4 | 0.25 | 2028-02-18 |
| GF-QQQ-IC-Ride | IC | 4 | 7 | 4 | 0.25 | 2028-02-18 |
| GF-QQQ-IC-SL100 | IC | 4 | 7 | 4 | 0.25 | 2028-02-18 |
| GF-QQQ-IC-SL200 | IC | 4 | 7 | 4 | 0.25 | 2028-02-18 |
| GF-QQQ-IC-Touch0 | IC | 4 | 7 | 4 | 0.25 | 2028-02-18 |
| GF-QQQ-IC-Trail | IC | 4 | 7 | 4 | 0.25 | 2028-02-18 |
| IC-SPX-FastPT25-S2 | IC | 1 | 15 | 1 | insufficient data | insufficient data |
| IC-SPX-FastPT25-S2-130PM | IC | 16 | 0 | 16 | 1.00 | 2026-12-25 |
| IC-SPX-Fortress-Unstopped | IC | 0 | 1 | 0 | insufficient data | insufficient data |
| Nigiri-Paper-v1 | OA-Mirror | 0 | 10 | 0 | insufficient data | insufficient data |
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | 1 | 0 | 1 | insufficient data | insufficient data |
| Trendy-Paper-v1 | OA-Mirror | 0 | 2 | 0 | insufficient data | insufficient data |

## Caveats
- **Positions:** 156 total (49 condors, 107 single-sided)  ·  205 legs.
- A condor has two spread rows paired by `trade_id` with `single_sided=False`; a single-sided position is any position that is not a condor (one spread row or `single_sided=True`). **Legs = OA position rows** (matches OA's "Positions" count). Win rate shown is per-position.
- A combined-`ironcondor` bot logs 1 leg per condor; a legged bot logs 2 — so Legs ≈ 2× condors only for legged bots. That's why they were confusing before.
- `Fix? = Y`: QQQ-IC bot carrying the call-side strike-resolution bug; data contaminated until fixed.
- Single-sided positions (not condors): 107 positions.
- Tiny-N bots are tracked but **not** evidence; read Trades before P/L.
