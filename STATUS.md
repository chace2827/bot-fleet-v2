# Bot Fleet — STATUS  ·  generated 2026-09-04

> **Numeric source of truth.** Auto-generated from `data/trades.csv` by `scripts/report.py`. Do not edit by hand. All figures are PAPER. Task backlog: `docs/backlog.md` (also in `dashboard.html`).

> **POST-CUTOVER LEDGER — `LEDGER_START = 2026-08-10`.** Every figure below is drawn from positions **opened on or after** that date. The v1 era is frozen in `data/archive/` and is never an input here.


## ⚠️ UNSIGNED PRE-REGISTRATION BOTS — DO NOT SWITCH ON

> The following bots have a pre-registration ledger entry with a blank, missing, or `NOT SIGNED` `SIGNED` line. No bot may be switched ON until the entry is signed and dated.

- QQQ long call
- QQQ-IC-0DTE-Fortress
- Tasty Condor


## Should-have-fired verdict — 2026-09-04

> SUSPECT rows split by `data/bot_gates.csv` `gate_type`. **1 structural** (no declared market gate) · **2 evidenced** (signed gate evaluated against tape). The split keeps the evidenced count meaningful without hiding anything.

| Bot | PR | Class | Verdict | Reason |
|---|---|---|---|---|
| IC-SPX-Fortress-Unstopped | INC-01 | STRUCTURAL | SUSPECT | no market gate and no fill_precondition declared; silence is suspect |
| 60min-ORB-10W-Paper-v1 | PR-12 | EVIDENCED | SUSPECT | SPX p=7718.89 at 10:40 breaks ORB range 7723.78-7750.19 (prior_close 7747.71) |
| Friday 14 DTE Broken Wing IB (B-70) | PR-10 | EVIDENCED | SUSPECT | date is Fri, gate requires Fri |

## Headline
- **Total closed P/L:** $8,160  ·  246 legs  ·  18 bots
  - Directional: $-840  (SPX $-840)
  - IC: $7,813  (QQQ $1,363  ·  SPX $6,450)
  - OA-Mirror: $1,187  (SPX $295)

## Champion — IC-SPX-FastPT25-S2
- P/L **$450**  ·  20 positions (1 condor, 19 single-sided) · 21 legs  ·  18 trading days (7 green / 1 red)
- Max drawdown (daily cumulative): $-50

## Focus roster — the bots you're actively perfecting  (OA: `*-Focus` groups)
> Close-to-live per pillar; for an A/B only the leading side. Select one group = per-pillar, all three = combined. Read per-bot R (readiness board), not the subtotal.

| Pillar | Bot | Status | Trades | P/L | WR |
|---|---|---|--:|--:|--:|
| IC | IC-SPX-FastPT25-S2 | ON | 20 | $450 | 40% |
| Directional | DIR-SPX-CallVIXdrop | ON | 6 | $-840 | 33% |
| OA-Mirror | 3DTE $140-$350 | ON | 5 | $185 | 100% |
| OA-Mirror | Friday 14 DTE Broken Wing IB (B-70) | ON | 2 | $250 | 100% |
| OA-Mirror | Nigiri-Paper-v1 | ON | 13 | $480 | 92% |
| **Total** | | | | **$525** | |

## Monitor — live but not focus  (OA: `Monitor` group)
> Running and watched — A/B laggards, controls, other active mirrors, the pending-decision QQQ-Fortress pair. Not promotion candidates yet.

| Pillar | Bot | Status | Trades | P/L | WR |
|---|---|---|--:|--:|--:|
| IC | QQQ-IC-0DTE-Fortress-NoPT50 | ON | 1 | $-338 | 0% |
| IC | GF-QQQ-IC-Canary | ON | 13 | $8 | 92% |
| IC | IC-SPX-Fortress-Unstopped | ON | 1 | $100 | 100% |
| IC | GF-QQQ-IC-PT50 | ON | 13 | $202 | 92% |
| IC | GF-QQQ-IC-Trail | ON | 13 | $251 | 77% |
| IC | GF-QQQ-IC-SL100 | ON | 13 | $269 | 69% |
| IC | GF-QQQ-IC-SL200 | ON | 13 | $274 | 85% |
| IC | GF-QQQ-IC-Ride | ON | 13 | $303 | 92% |
| IC | GF-QQQ-IC-Touch0 | ON | 13 | $303 | 92% |
| IC | IC-SPX-FastPT25-S2-130PM | ON | 19 | $5,900 | 89% |
| OA-Mirror | 60min-ORB-10W-Paper-v1 | ON | 10 | $110 | 80% |
| OA-Mirror | Trendy-Paper-v1 | ON | 4 | $162 | 100% |
| **Total** | | | | **$7,544** | |

**Archive (OA: `Archive` group):** 1 off/dead bots · $91 closed — excluded from the working view (still exported for the ledger).

## Allocation audit — sizing realism  (ON bots, per-position)
> R (pnl÷risk) already cancels size, so this changes **no ranking** — it flags whether the paper sizing is realistic to carry live. Hold class sets the rule: **0DTE** recycles risk daily; **swing/multi-week** ties capital up for the whole hold (max-risk/day = concurrent open risk, not daily deploy). **1-lot bots are fill-untested at scale** — their edge won't survive the slippage of a real order size (ties to the v5-slippage task).

| Bot | Pillar | Hold | Pos | med Qty | med Risk$ | max Risk$ | Realism |
|---|---|---|--:|--:|--:|--:|:--|
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | 0DTE | 1 | 26 | $4,940 | $4,940 | sized ✓ |
| IC-SPX-Fortress-Unstopped | IC | 0DTE | 1 | 10 | $4,900 | $4,900 | sized ✓ |
| IC-SPX-FastPT25-S2 | IC | 0DTE | 20 | 10 | $4,900 | $4,900 | sized ✓ |
| IC-SPX-FastPT25-S2-130PM | IC | 0DTE | 19 | 10 | $4,750 | $4,900 | sized ✓ |
| GF-QQQ-IC-Canary | IC | 0DTE | 13 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-PT50 | IC | 0DTE | 13 | 1 | $193 | $4,940 | **1-lot — fill-untested** |
| GF-QQQ-IC-Trail | IC | 0DTE | 13 | 1 | $193 | $4,940 | **1-lot — fill-untested** |
| GF-QQQ-IC-SL100 | IC | 0DTE | 13 | 1 | $193 | $4,940 | **1-lot — fill-untested** |
| GF-QQQ-IC-SL200 | IC | 0DTE | 13 | 1 | $193 | $4,940 | **1-lot — fill-untested** |
| GF-QQQ-IC-Ride | IC | 0DTE | 13 | 1 | $193 | $4,940 | **1-lot — fill-untested** |
| GF-QQQ-IC-Touch0 | IC | 0DTE | 13 | 1 | $193 | $4,940 | **1-lot — fill-untested** |
| DIR-SPX-CallVIXdrop | Directional | 0DTE | 6 | 1 | $630 | $675 | **1-lot — fill-untested** |
| Nigiri-Paper-v1 | OA-Mirror | 4d swing | 13 | 10 | $4,910 | $4,930 | sized ✓ |
| Friday 14 DTE Broken Wing IB (B-70) | OA-Mirror | 14d multi-wk | 2 | 1 | $1,995 | $1,995 | **1-lot — fill-untested** |
| 3DTE $140-$350 | OA-Mirror | 5d swing | 5 | 1 | $955 | $975 | **1-lot — fill-untested** |
| Trendy-Paper-v1 | OA-Mirror | 11d multi-wk | 4 | 1 | $933 | $943 | **1-lot — fill-untested** |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 0DTE | 10 | 1 | $920 | $930 | **1-lot — fill-untested** |

> **Read:** SPX-IC + Nigiri run ~10-lot (~$4.8k/position, comparable to the champion). Every other mirror + both directional bots run **1 lot** ($0.5k–$2.9k) — realistic for tracking W/L, not for reading a live-scale edge. Sizing rule is per-bot by hold class (see backlog COCKPIT LANE step 1); the go-live target is ~$10k max risk/day with a hedge reserve carved out first.

## Hedge tournament (live-data counterfactual)
> **The productized loss autopsy.** Every real, settled (status=expired) leg replayed through the v1 hedge library — Ride/no-stop, PT+X%/SL-X% return-threshold rules, and an S2 strike-touch cut (tape-gated, 5-min grain). **Optimistic bound, not a live estimate** — every non-Ride arm assumes a fill exactly at the threshold; real fills slip. Compare rules by **R** (pnl÷risk), never $. Basis: PT/SL % are of the credit collected (`|premium|`), per `mfe_pct`/`mae_pct` already carrying that unit (verified against the ledger — see `scripts/hedge_tournament.py` docstring). **Defang: deferred v1** (23 legs marked, not modeled — needs an intraday premium-decay path not yet in the ledger).

| Rule | N | Exp(R) | Tot R | WR | maxDD-R | worst-R |
|---|--:|--:|--:|--:|--:|--:|
| ride | 23 | +5.6% | +1.28 | 100% | 0.00 | +2.0% |
| pt25 | 23 | +1.4% | +0.32 | 100% | 0.00 | +0.5% |
| pt50 | 23 | +2.8% | +0.65 | 100% | 0.00 | +1.0% |
| pt100 | 23 | +5.6% | +1.28 | 100% | 0.00 | +2.0% |
| sl50 | 23 | +2.0% | +0.46 | 52% | -0.08 | -3.2% |
| sl75 | 23 | +3.6% | +0.84 | 78% | -0.09 | -4.8% |
| sl100 | 23 | +3.8% | +0.88 | 83% | -0.06 | -6.4% |
| sl130 | 23 | +4.1% | +0.94 | 87% | -0.08 | -8.3% |
| s2 | 18 | +4.1% | +0.74 | 94% | -0.24 | -24.1% |

#### Per-bot cut  (Ride vs SL75 — the mid-spectrum published rung)
| Bot | N | Ride Exp(R) | SL75 Exp(R) | Δ |
|---|--:|--:|--:|--:|
| IC-SPX-FastPT25-S2-130PM | 20 | +6.0% | +3.7% | -2.2pp |
| 3DTE $140-$350 | 1 | +4.7% | +4.7% | +0.0pp |
| IC-SPX-FastPT25-S2 | 2 | +2.0% | +2.0% | +0.0pp |

#### Regime cut  (Ride vs SL75, by tape-derived regime label)
| Regime | N | Ride Exp(R) | SL75 Exp(R) |
|---|--:|--:|--:|
| Chop | 19 | +5.6% | +4.3% |
| n/a | 4 | +5.5% | +0.4% |

> N is small and concentrated in the last few tape-covered trading days (tape.py is new); the S2 arm and the regime cut will thicken as more days accrue. Read this as an early ranking to cross-check the LEAN/OA backtest tournament, not a standalone verdict.

## Trade-window heat map — when do shorts actually get touched (hour x regime)
> **The 11am-vs-1:30 question, generalized.** Every ledger position's worst-adverse-excursion (MAE) timestamp, bucketed by hour-of-day x tape-derived regime (Drift/Trend/Chop/n-a). `touch %` = short-strike touch rate, scored only on positions with same-day tape coverage (a small, recent subset — most history predates `tape.py`); `MAE` = mean adverse excursion as % of credit, computed on ALL positions in the bucket regardless of tape coverage. Cells are `n=… · touch …% · MAE …%`; blank touch% = no tape-covered position fell in that cell. **Small-n cells are directional, not conclusive** — read the n before the rate.

| Hour | Chop | Drift | n/a |
|---|---|---|---|
| 09:30-10 | n=1 · MAE -2.1% | — | n=2 · MAE -0.5% |
| 10-11 | n=2 · touch 0% · MAE -0.1% | — | n=7 · MAE -0.3% |
| 11-12 | n=12 · touch 0% · MAE -0.1% | — | n=15 · MAE -0.3% |
| 12-13 | n=3 · touch 50% · MAE -0.8% | — | n=5 · MAE -0.5% |
| 13-14 | n=32 · touch 25% · MAE -0.7% | n=12 · touch 0% · MAE -0.1% | n=68 · MAE -0.9% |
| 14-15 | n=3 · touch 0% · MAE -0.9% | n=13 · touch 0% · MAE -0.7% | n=9 · MAE -0.9% |
| 15-16 | — | — | n=3 · MAE -1.1% |

> **Read:** touches cluster at **12-13 (Chop)** — 1 of 2 tape-covered position(s) scored there touched (touch rate 50%). Tape coverage is thin (5 days) — treat as an early signal, not a verdict.

## Lessons index — tagged, searchable  (data/lessons.csv)
> Every graded bot-day's "day's lesson" (from the brief JSON's Verdict row; session-log fallback only for dates the brief never covered), tagged from a fixed vocabulary (`entry-timing · hedge · filter · regime · sizing · other`) by simple keyword rules (see `scripts/lessons.py` docstring) — not an ML classifier. Grouped by tag, most recent first.

**Tag counts:** 

## Per-bot (sorted by P/L)
| Bot | Pillar | Und | Role | Status | Trades | Legs | P/L | WR | Fix? |
|---|---|---|---|---|--:|--:|--:|--:|:--:|
| DIR-SPX-CallVIXdrop | Directional | SPX | experiment | ON | 6 | 6 | $-840 | 33% | - |
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | QQQ | experiment | ON | 1 | 2 | $-338 | 0% | Y |
| GF-QQQ-IC-Canary | IC | QQQ | instrument | ON | 13 | 18 | $8 | 92% | - |
| GF-QQQ-IC-Ride-Delta | IC | QQQ | experiment | OFF | 15 | 18 | $91 | 93% | - |
| IC-SPX-Fortress-Unstopped | IC | SPX | control | ON | 1 | 1 | $100 | 100% | - |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | SPX | mirror-watch | ON | 10 | 10 | $110 | 80% | - |
| Trendy-Paper-v1 | OA-Mirror | — | mirror-watch | ON | 4 | 4 | $162 | 100% | - |
| 3DTE $140-$350 | OA-Mirror | SPX | mirror-watch | ON | 5 | 5 | $185 | 100% | - |
| GF-QQQ-IC-PT50 | IC | QQQ | experiment | ON | 13 | 18 | $202 | 92% | - |
| Friday 14 DTE Broken Wing IB (B-70) | OA-Mirror | — | mirror-watch | ON | 2 | 2 | $250 | 100% | - |
| GF-QQQ-IC-Trail | IC | QQQ | experiment | ON | 13 | 18 | $251 | 77% | - |
| GF-QQQ-IC-SL100 | IC | QQQ | experiment | ON | 13 | 18 | $269 | 69% | - |
| GF-QQQ-IC-SL200 | IC | QQQ | experiment | ON | 13 | 18 | $274 | 85% | - |
| GF-QQQ-IC-Ride | IC | QQQ | control | ON | 13 | 18 | $303 | 92% | - |
| GF-QQQ-IC-Touch0 | IC | QQQ | experiment | ON | 13 | 18 | $303 | 92% | - |
| IC-SPX-FastPT25-S2 | IC | SPX | live-candidate | ON | 20 | 21 | $450 | 40% | - |
| Nigiri-Paper-v1 | OA-Mirror | — | mirror-watch | ON | 13 | 13 | $480 | 92% | - |
| IC-SPX-FastPT25-S2-130PM | IC | SPX | experiment | ON | 19 | 38 | $5,900 | 89% | - |

## Readiness board — per-condor, gated (the graduation view)
> **Grain = condor** (legs summed), not leg. Six ordered gates; the **first red (○) gate is the named blocker**. `●`=pass `○`=fail `·`=pending. Exp(R) shows the **bootstrap 95% CI** (replaces the t-stat). Stage: INCUBATE→VALIDATE→CANDIDATE→LIVE-READY (LIVE = real capital). Controls & mirror-watch are listed separately — they can't graduate by design.
> **Gates:** G1 clean data (no strike-bug, single-sided excluded) · G2 ≥20 clean condors · G3 Exp(R)>0 w/ 95% CI above 0 · G4 maxDD-R within cap (RoE $ cap still a `<FILL>` blank) · G5 instruction-mirror ≥90% (from the daily brief / `data/compliance.csv`; pending until ≥5 graded days) · G6 OOS/regime robustness.

| Bot | Role | Stage | Gates | n | Exp(R) [95% CI] | Blocker |
|---|---|---|:--:|--:|--:|---|
| IC-SPX-FastPT25-S2-130PM | experiment | VALIDATE | ●○○●·· | 19 | +6.6% [-0.6, +11.7] | G2: 19 clean condors (need 20) |
| IC-SPX-FastPT25-S2 | live-candidate | VALIDATE | ●○○●·· | 1 | +4.1% — | G2: 1 clean condors (need 20) |
| GF-QQQ-IC-Ride-Delta | experiment | VALIDATE | ●○○●·· | 3 | +2.4% [-6.3, +7.3] | G2: 3 clean condors (need 20) |
| GF-QQQ-IC-Touch0 | experiment | VALIDATE | ●○○●·· | 5 | +2.4% [-2.0, +5.6] | G2: 5 clean condors (need 20) |
| GF-QQQ-IC-PT50 | experiment | VALIDATE | ●○○●·· | 5 | +1.7% [-2.2, +4.4] | G2: 5 clean condors (need 20) |
| GF-QQQ-IC-SL100 | experiment | VALIDATE | ●○○●·· | 5 | +0.3% [-2.6, +3.5] | G2: 5 clean condors (need 20) |
| GF-QQQ-IC-Trail | experiment | VALIDATE | ●○○●·· | 5 | +0.1% [-3.2, +2.6] | G2: 5 clean condors (need 20) |
| GF-QQQ-IC-Canary | instrument | VALIDATE | ●○○●·· | 5 | -0.2% [-4.1, +2.2] | G2: 5 clean condors (need 20) |
| GF-QQQ-IC-SL200 | experiment | VALIDATE | ●○○●·· | 5 | -0.7% [-6.0, +4.2] | G2: 5 clean condors (need 20) |
| DIR-SPX-CallVIXdrop | experiment | VALIDATE | ●○○●·· | 6 | -20.4% [-52.4, +22.2] | G2: 6 clean condors (need 20) |
| QQQ-IC-0DTE-Fortress-NoPT50 | experiment | VALIDATE | ○○○●·· | 1 | -6.8% — | G1: strike-bug contamination |

#### Non-graduating (controls / mirror-watch — tracked, can't go live)
| Bot | Role | Gates | n | Exp(R) [95% CI] | Note |
|---|---|:--:|--:|--:|---|
| Friday 14 DTE Broken Wing IB (B-70) | mirror-watch | ●○●●·· | 2 | +6.3% [+5.5, +7.1] | G2: 2 clean condors (need 20) |
| Trendy-Paper-v1 | mirror-watch | ●○●●·· | 4 | +4.3% [+3.0, +6.0] | G2: 4 clean condors (need 20) |
| 3DTE $140-$350 | mirror-watch | ●○●●·· | 5 | +3.9% [+3.2, +4.5] | G2: 5 clean condors (need 20) |
| Nigiri-Paper-v1 | mirror-watch | ●○●●·· | 13 | +0.8% [+0.5, +1.0] | G2: 13 clean condors (need 20) |
| GF-QQQ-IC-Ride | control | ●○○●·· | 5 | +2.4% [-2.0, +5.6] | G2: 5 clean condors (need 20) |
| IC-SPX-Fortress-Unstopped | control | ●○○●·· | 1 | +2.0% — | G2: 1 clean condors (need 20) |
| 60min-ORB-10W-Paper-v1 | mirror-watch | ●○○●·· | 10 | +1.0% [-5.7, +5.6] | G2: 10 clean condors (need 20) |

## Scorecard — normalized (Return on Risk) · legacy per-LEG view
> ⚠️ **Per-LEG grain** (kept for continuity) — for the graduation decision use the **Readiness board** above (per-condor, gated). Each trade = **pnl ÷ capital-at-risk** ("R"), so allocation and contract size cancel out. Sorted by expectancy. t-stat blows up for low-variance grinders (e.g. 3DTE) — don't rank on it alone.

### Ranked (n ≥ 20)
| Bot | Pillar | n | Exp(R) | t | Tot R | maxDD-R | WR |
|---|---|--:|--:|--:|--:|--:|--:|
| IC-SPX-FastPT25-S2-130PM | IC | 38 | +0.033 | 2.0 | +1.2 | -0.8 | 95% |
| IC-SPX-FastPT25-S2 | IC | 21 | +0.004 | 2.5 | +0.1 | -0.0 | 43% |

### Provisional (n < 20 — tracked, not ranked; samples too small to trust)
| Bot | Pillar | n | Exp(R) | Tot R | raw P/L |
|---|---|--:|--:|--:|--:|
| Friday 14 DTE Broken Wing IB (B-70) | OA-Mirror | 2 | +0.063 | +0.1 | $250 |
| Trendy-Paper-v1 | OA-Mirror | 4 | +0.043 | +0.2 | $162 |
| 3DTE $140-$350 | OA-Mirror | 5 | +0.039 | +0.2 | $185 |
| GF-QQQ-IC-Ride-Delta | IC | 18 | +0.026 | +0.5 | $91 |
| GF-QQQ-IC-Ride | IC | 18 | +0.022 | +0.4 | $303 |
| GF-QQQ-IC-Touch0 | IC | 18 | +0.022 | +0.4 | $303 |
| IC-SPX-Fortress-Unstopped | IC | 1 | +0.020 | +0.0 | $100 |
| GF-QQQ-IC-PT50 | IC | 18 | +0.015 | +0.3 | $202 |
| GF-QQQ-IC-SL200 | IC | 18 | +0.014 | +0.3 | $274 |
| GF-QQQ-IC-SL100 | IC | 18 | +0.013 | +0.2 | $269 |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 10 | +0.010 | +0.1 | $110 |
| Nigiri-Paper-v1 | OA-Mirror | 13 | +0.008 | +0.1 | $480 |
| GF-QQQ-IC-Trail | IC | 18 | +0.008 | +0.1 | $251 |
| GF-QQQ-IC-Canary | IC | 18 | +0.002 | +0.0 | $8 |
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | 2 | -0.034 | -0.1 | $-338 |
| DIR-SPX-CallVIXdrop | Directional | 6 | -0.204 | -1.2 | $-840 |

### Decision rules (read against the right column)
- **Kill** — Exp(R) < 0 held with conviction (|t| ≳ 2, or n large). Raw P/L size is irrelevant.
- **Graduate** — Exp(R) > 0 **and** |t| ≳ 2 **and** n ≥ threshold (edge is real, not noise).
- **Size live capital** — among graduates, weight by Tot R + low maxDD-R (consistency); never size on raw P/L.
- **Exp(R)** = avg return per $1 risked. **Tot R** = size-free analog of total P/L. **maxDD-R** = worst cumulative-R drawdown (risk shape). **t** = evidence the edge is real.

---

## Decidability countdown — per armed arm (PROJECTION, not evidence)
> **This is a forward projection, not a result.** It extrapolates the recent fire rate and assumes that rate holds. Calendar projection skips weekends and US market holidays (rule-derived), so the date is approximate. The unit of account is the **POSITION** (a two-sided condor = two spread rows paired by `trade_id`); *n* = 100 means **100 condors**, not 100 legs. One-sided spreads are listed separately and do **not** count toward the 100-condor target. The recent window is the last **20 trading days**; the post-cutover ledger currently contributes **20 trading days** to this window.

| Arm | Pillar | Current condors, positions | One-sided positions, spreads | Closes in 20-trading-day window | Fire rate (closes/trading-day, condors) | Projected 100-condor date |
|---|---|--:|--:|--:|--:|---|
| 3DTE $140-$350 | OA-Mirror | 5 | 0 | 5 | 0.25 | 2028-03-13 |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 0 | 10 | 0 | insufficient data | insufficient data |
| DIR-SPX-CallVIXdrop | Directional | 6 | 0 | 6 | 0.30 | 2027-12-06 |
| DIR-SPX-PutVIX22-SL75 | Directional | 0 | 0 | 0 | insufficient data | insufficient data |
| Friday 14 DTE Broken Wing IB (B-70) | OA-Mirror | 2 | 0 | 2 | insufficient data | insufficient data |
| GF-QQQ-IC-Canary | IC | 5 | 8 | 5 | 0.25 | 2028-03-13 |
| GF-QQQ-IC-PT50 | IC | 5 | 8 | 5 | 0.25 | 2028-03-13 |
| GF-QQQ-IC-Ride | IC | 5 | 8 | 5 | 0.25 | 2028-03-13 |
| GF-QQQ-IC-SL100 | IC | 5 | 8 | 5 | 0.25 | 2028-03-13 |
| GF-QQQ-IC-SL200 | IC | 5 | 8 | 5 | 0.25 | 2028-03-13 |
| GF-QQQ-IC-Touch0 | IC | 5 | 8 | 5 | 0.25 | 2028-03-13 |
| GF-QQQ-IC-Trail | IC | 5 | 8 | 5 | 0.25 | 2028-03-13 |
| IC-SPX-FastPT25-S2 | IC | 1 | 19 | 1 | insufficient data | insufficient data |
| IC-SPX-FastPT25-S2-130PM | IC | 19 | 0 | 19 | 0.95 | 2027-01-08 |
| IC-SPX-Fortress-Unstopped | IC | 0 | 1 | 0 | insufficient data | insufficient data |
| Nigiri-Paper-v1 | OA-Mirror | 0 | 13 | 0 | insufficient data | insufficient data |
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | 1 | 0 | 1 | insufficient data | insufficient data |
| Trendy-Paper-v1 | OA-Mirror | 0 | 4 | 0 | insufficient data | insufficient data |

## Caveats
- **Positions:** 187 total (59 condors, 128 single-sided)  ·  246 legs.
- A condor has two spread rows paired by `trade_id` with `single_sided=False`; a single-sided position is any position that is not a condor (one spread row or `single_sided=True`). **Legs = OA position rows** (matches OA's "Positions" count). Win rate shown is per-position.
- A combined-`ironcondor` bot logs 1 leg per condor; a legged bot logs 2 — so Legs ≈ 2× condors only for legged bots. That's why they were confusing before.
- `Fix? = Y`: QQQ-IC bot carrying the call-side strike-resolution bug; data contaminated until fixed.
- Single-sided positions (not condors): 128 positions.
- Tiny-N bots are tracked but **not** evidence; read Trades before P/L.
