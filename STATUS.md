# Bot Fleet — STATUS  ·  generated 2026-09-16

> **Numeric source of truth.** Auto-generated from `data/trades.csv` by `scripts/report.py`. Do not edit by hand. All figures are PAPER. Task backlog: `docs/backlog.md` (also in `dashboard.html`).

> **POST-CUTOVER LEDGER — `LEDGER_START = 2026-08-10`.** Every figure below is drawn from positions **opened on or after** that date. The v1 era is frozen in `data/archive/` and is never an input here.


## ⚠️ UNSIGNED PRE-REGISTRATION BOTS — DO NOT SWITCH ON

> The following bots have a pre-registration ledger entry with a blank, missing, or `NOT SIGNED` `SIGNED` line. No bot may be switched ON until the entry is signed and dated.

- QQQ long call
- QQQ-IC-0DTE-Fortress
- Tasty Condor


## Should-have-fired verdict — 2026-09-16

> SUSPECT rows split by `data/bot_gates.csv` `gate_type`. **1 structural** (no declared market gate) · **3 evidenced** (signed gate evaluated against tape). The split keeps the evidenced count meaningful without hiding anything.

| Bot | PR | Class | Verdict | Reason |
|---|---|---|---|---|
| IC-SPX-Fortress-Unstopped | INC-01 | STRUCTURAL | SUSPECT | no market gate and no fill_precondition declared; silence is suspect |
| 60min-ORB-10W-Paper-v1 | PR-12 | EVIDENCED | SUSPECT | SPX p=7616.17 at 11:00 breaks ORB range 7597.61-7614.97 (prior_close 7585.73) |
| IC-SPX-FastPT25-S2 | PR-01 | EVIDENCED | SUSPECT | SPX p=7616.17 at 11:00, Δ%=0.4, \|Δ%\|=0.4 < threshold 0.75 |
| IC-SPX-FastPT25-S2-130PM | PR-02 | EVIDENCED | SUSPECT | SPX p=7609.19 at 13:30, Δ%=0.31, \|Δ%\|=0.31 < threshold 0.75 |

## Headline
- **Total closed P/L:** $11,945  ·  333 legs  ·  18 bots
  - Directional: $-1,220  (SPX $-1,220)
  - IC: $11,204  (QQQ $3,954  ·  SPX $7,250)
  - OA-Mirror: $1,961  (SPX $555)

## Champion — IC-SPX-FastPT25-S2
- P/L **$850**  ·  26 positions (3 condors, 23 single-sided) · 29 legs  ·  23 trading days (10 green / 3 red)
- Max drawdown (daily cumulative): $-100

## Focus roster — the bots you're actively perfecting  (OA: `*-Focus` groups)
> Close-to-live per pillar; for an A/B only the leading side. Select one group = per-pillar, all three = combined. Read per-bot R (readiness board), not the subtotal.

| Pillar | Bot | Status | Trades | P/L | WR |
|---|---|---|--:|--:|--:|
| IC | IC-SPX-FastPT25-S2 | ON | 26 | $850 | 42% |
| Directional | DIR-SPX-CallVIXdrop | ON | 8 | $-1,220 | 38% |
| OA-Mirror | 3DTE $140-$350 | ON | 8 | $345 | 100% |
| OA-Mirror | Nigiri-Paper-v1 | ON | 14 | $550 | 93% |
| OA-Mirror | Friday 14 DTE Broken Wing IB (B-70) | ON | 4 | $675 | 100% |
| **Total** | | | | **$1,200** | |

## Monitor — live but not focus  (OA: `Monitor` group)
> Running and watched — A/B laggards, controls, other active mirrors, the pending-decision QQQ-Fortress pair. Not promotion candidates yet.

| Pillar | Bot | Status | Trades | P/L | WR |
|---|---|---|--:|--:|--:|
| IC | GF-QQQ-IC-SL200 | ON | 18 | $-584 | 78% |
| IC | GF-QQQ-IC-SL100 | ON | 19 | $-173 | 68% |
| IC | QQQ-IC-0DTE-Fortress-NoPT50 | ON | 2 | $-77 | 50% |
| IC | GF-QQQ-IC-Canary | ON | 18 | $24 | 94% |
| IC | IC-SPX-Fortress-Unstopped | ON | 1 | $100 | 100% |
| IC | GF-QQQ-IC-Trail | ON | 18 | $589 | 78% |
| IC | GF-QQQ-IC-PT50 | ON | 18 | $878 | 89% |
| IC | GF-QQQ-IC-Touch0 | ON | 18 | $1,603 | 89% |
| IC | GF-QQQ-IC-Ride | ON | 18 | $1,603 | 89% |
| IC | IC-SPX-FastPT25-S2-130PM | ON | 24 | $6,300 | 88% |
| OA-Mirror | Trendy-Paper-v1 | ON | 5 | $181 | 100% |
| OA-Mirror | 60min-ORB-10W-Paper-v1 | ON | 12 | $210 | 83% |
| **Total** | | | | **$10,654** | |

**Archive (OA: `Archive` group):** 1 off/dead bots · $91 closed — excluded from the working view (still exported for the ledger).

## Allocation audit — sizing realism  (ON bots, per-position)
> R (pnl÷risk) already cancels size, so this changes **no ranking** — it flags whether the paper sizing is realistic to carry live. Hold class sets the rule: **0DTE** recycles risk daily; **swing/multi-week** ties capital up for the whole hold (max-risk/day = concurrent open risk, not daily deploy). **1-lot bots are fill-untested at scale** — their edge won't survive the slippage of a real order size (ties to the v5-slippage task).

| Bot | Pillar | Hold | Pos | med Qty | med Risk$ | max Risk$ | Realism |
|---|---|---|--:|--:|--:|--:|:--|
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | 0DTE | 2 | 29 | $4,940 | $4,940 | sized ✓ |
| IC-SPX-Fortress-Unstopped | IC | 0DTE | 1 | 10 | $4,900 | $4,900 | sized ✓ |
| IC-SPX-FastPT25-S2 | IC | 0DTE | 26 | 10 | $4,900 | $4,900 | sized ✓ |
| IC-SPX-FastPT25-S2-130PM | IC | 0DTE | 24 | 10 | $4,750 | $4,900 | sized ✓ |
| GF-QQQ-IC-SL200 | IC | 0DTE | 18 | 1 | $193 | $5,018 | **1-lot — fill-untested** |
| GF-QQQ-IC-SL100 | IC | 0DTE | 19 | 1 | $193 | $5,018 | **1-lot — fill-untested** |
| GF-QQQ-IC-Canary | IC | 0DTE | 18 | 1 | $193 | $193 | **1-lot — fill-untested** |
| GF-QQQ-IC-Trail | IC | 0DTE | 18 | 1 | $193 | $5,018 | **1-lot — fill-untested** |
| GF-QQQ-IC-PT50 | IC | 0DTE | 18 | 1 | $193 | $5,018 | **1-lot — fill-untested** |
| GF-QQQ-IC-Touch0 | IC | 0DTE | 18 | 1 | $193 | $5,018 | **1-lot — fill-untested** |
| GF-QQQ-IC-Ride | IC | 0DTE | 18 | 1 | $193 | $5,018 | **1-lot — fill-untested** |
| DIR-SPX-CallVIXdrop | Directional | 0DTE | 8 | 1 | $630 | $725 | **1-lot — fill-untested** |
| Nigiri-Paper-v1 | OA-Mirror | 7d swing | 14 | 10 | $4,910 | $4,930 | sized ✓ |
| Friday 14 DTE Broken Wing IB (B-70) | OA-Mirror | 14d multi-wk | 4 | 1 | $1,960 | $1,995 | **1-lot — fill-untested** |
| 3DTE $140-$350 | OA-Mirror | 5d swing | 8 | 1 | $965 | $1,910 | **1-lot — fill-untested** |
| Trendy-Paper-v1 | OA-Mirror | 10d multi-wk | 5 | 1 | $933 | $943 | **1-lot — fill-untested** |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 0DTE | 12 | 1 | $920 | $930 | **1-lot — fill-untested** |

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

| Hour | Chop | Drift | Trend | n/a |
|---|---|---|---|---|
| 09:30-10 | n=1 · MAE -2.1% | — | — | n=3 · MAE -0.4% |
| 10-11 | n=2 · touch 0% · MAE -0.1% | — | — | n=13 · MAE -0.8% |
| 11-12 | n=12 · touch 0% · MAE -0.1% | — | — | n=23 · MAE -0.3% |
| 12-13 | n=3 · touch 50% · MAE -0.8% | — | — | n=5 · MAE -0.5% |
| 13-14 | n=32 · touch 25% · MAE -0.7% | n=12 · touch 0% · MAE -0.1% | n=7 · touch 0% · MAE -1.0% | n=97 · MAE -0.8% |
| 14-15 | n=3 · touch 0% · MAE -0.9% | n=13 · touch 0% · MAE -0.7% | n=2 · touch 100% · MAE -1.4% | n=14 · MAE -2.3% |
| 15-16 | — | — | n=1 · touch 0% · MAE -1.1% | n=3 · MAE -1.1% |

> **Read:** touches cluster at **14-15 (Trend)** — 1 of 1 tape-covered position(s) scored there touched (touch rate 100%). Tape coverage is thin (5 days) — treat as an early signal, not a verdict.

## Lessons index — tagged, searchable  (data/lessons.csv)
> Every graded bot-day's "day's lesson" (from the brief JSON's Verdict row; session-log fallback only for dates the brief never covered), tagged from a fixed vocabulary (`entry-timing · hedge · filter · regime · sizing · other`) by simple keyword rules (see `scripts/lessons.py` docstring) — not an ML classifier. Grouped by tag, most recent first.

**Tag counts:** 

## Per-bot (sorted by P/L)
| Bot | Pillar | Und | Role | Status | Trades | Legs | P/L | WR | Fix? |
|---|---|---|---|---|--:|--:|--:|--:|:--:|
| DIR-SPX-CallVIXdrop | Directional | SPX | experiment | ON | 8 | 8 | $-1,220 | 38% | - |
| GF-QQQ-IC-SL200 | IC | QQQ | experiment | ON | 18 | 24 | $-584 | 78% | - |
| GF-QQQ-IC-SL100 | IC | QQQ | experiment | ON | 19 | 24 | $-173 | 68% | - |
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | QQQ | experiment | ON | 2 | 4 | $-77 | 50% | Y |
| GF-QQQ-IC-Canary | IC | QQQ | instrument | ON | 18 | 27 | $24 | 94% | - |
| GF-QQQ-IC-Ride-Delta | IC | QQQ | experiment | OFF | 15 | 18 | $91 | 93% | - |
| IC-SPX-Fortress-Unstopped | IC | SPX | control | ON | 1 | 1 | $100 | 100% | - |
| Trendy-Paper-v1 | OA-Mirror | — | mirror-watch | ON | 5 | 5 | $181 | 100% | - |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | SPX | mirror-watch | ON | 12 | 12 | $210 | 83% | - |
| 3DTE $140-$350 | OA-Mirror | SPX | mirror-watch | ON | 8 | 8 | $345 | 100% | - |
| Nigiri-Paper-v1 | OA-Mirror | — | mirror-watch | ON | 14 | 14 | $550 | 93% | - |
| GF-QQQ-IC-Trail | IC | QQQ | experiment | ON | 18 | 27 | $589 | 78% | - |
| Friday 14 DTE Broken Wing IB (B-70) | OA-Mirror | — | mirror-watch | ON | 4 | 4 | $675 | 100% | - |
| IC-SPX-FastPT25-S2 | IC | SPX | live-candidate | ON | 26 | 29 | $850 | 42% | - |
| GF-QQQ-IC-PT50 | IC | QQQ | experiment | ON | 18 | 26 | $878 | 89% | - |
| GF-QQQ-IC-Touch0 | IC | QQQ | experiment | ON | 18 | 27 | $1,603 | 89% | - |
| GF-QQQ-IC-Ride | IC | QQQ | control | ON | 18 | 27 | $1,603 | 89% | - |
| IC-SPX-FastPT25-S2-130PM | IC | SPX | experiment | ON | 24 | 48 | $6,300 | 88% | - |

## Readiness board — per-condor, gated (the graduation view)
> **Grain = condor** (legs summed), not leg. Six ordered gates; the **first red (○) gate is the named blocker**. `●`=pass `○`=fail `·`=pending. Exp(R) shows the **bootstrap 95% CI** (replaces the t-stat). Stage: INCUBATE→VALIDATE→CANDIDATE→LIVE-READY (LIVE = real capital). Controls & mirror-watch are listed separately — they can't graduate by design.
> **Gates:** G1 clean data (no strike-bug, single-sided excluded) · G2 ≥20 clean condors · G3 Exp(R)>0 w/ 95% CI above 0 · G4 maxDD-R within cap (RoE $ cap still a `<FILL>` blank) · G5 instruction-mirror ≥90% (from the daily brief / `data/compliance.csv`; pending until ≥5 graded days) · G6 OOS/regime robustness.

| Bot | Role | Stage | Gates | n | Exp(R) [95% CI] | Blocker |
|---|---|---|:--:|--:|--:|---|
| IC-SPX-FastPT25-S2-130PM | experiment | CANDIDATE | ●●○●·● | 24 | +5.5% [-1.5, +11.1] | G3: CI includes 0 (~5 more trades) |
| GF-QQQ-IC-Touch0 | experiment | CANDIDATE | ●○●●·· | 9 | +4.8% [+1.5, +7.3] | G2: 9 clean condors (need 20) |
| IC-SPX-FastPT25-S2 | live-candidate | CANDIDATE | ●○●●·· | 3 | +4.8% [+4.1, +5.1] | G2: 3 clean condors (need 20) |
| GF-QQQ-IC-PT50 | experiment | CANDIDATE | ●○●●·· | 8 | +3.2% [+0.3, +5.2] | G2: 8 clean condors (need 20) |
| GF-QQQ-IC-Ride-Delta | experiment | VALIDATE | ●○○●·· | 3 | +2.4% [-6.3, +7.3] | G2: 3 clean condors (need 20) |
| GF-QQQ-IC-Trail | experiment | VALIDATE | ●○○●·· | 9 | +0.8% [-1.2, +2.3] | G2: 9 clean condors (need 20) |
| GF-QQQ-IC-Canary | instrument | VALIDATE | ●○○●·· | 9 | +0.7% [-1.6, +2.2] | G2: 9 clean condors (need 20) |
| GF-QQQ-IC-SL100 | experiment | VALIDATE | ●○○●·· | 5 | +0.3% [-2.6, +3.5] | G2: 5 clean condors (need 20) |
| GF-QQQ-IC-SL200 | experiment | VALIDATE | ●○○●·· | 6 | -1.8% [-6.3, +2.9] | G2: 6 clean condors (need 20) |
| DIR-SPX-CallVIXdrop | experiment | VALIDATE | ●○○●·· | 8 | -21.7% [-51.6, +11.0] | G2: 8 clean condors (need 20) |
| QQQ-IC-0DTE-Fortress-NoPT50 | experiment | VALIDATE | ○○○●·· | 2 | -0.8% [-6.8, +5.3] | G1: strike-bug contamination |

#### Non-graduating (controls / mirror-watch — tracked, can't go live)
| Bot | Role | Gates | n | Exp(R) [95% CI] | Note |
|---|---|:--:|--:|--:|---|
| Friday 14 DTE Broken Wing IB (B-70) | mirror-watch | ●○●●·· | 4 | +8.7% [+6.3, +11.1] | G2: 4 clean condors (need 20) |
| GF-QQQ-IC-Ride | control | ●○●●·· | 9 | +4.8% [+1.5, +7.4] | G2: 9 clean condors (need 20) |
| 3DTE $140-$350 | mirror-watch | ●○●●·· | 8 | +3.9% [+3.4, +4.3] | G2: 8 clean condors (need 20) |
| Trendy-Paper-v1 | mirror-watch | ●○●●·· | 5 | +3.9% [+2.6, +5.3] | G2: 5 clean condors (need 20) |
| Nigiri-Paper-v1 | mirror-watch | ●○●●·· | 14 | +0.8% [+0.6, +1.0] | G2: 14 clean condors (need 20) |
| IC-SPX-Fortress-Unstopped | control | ●○○●·· | 1 | +2.0% — | G2: 1 clean condors (need 20) |
| 60min-ORB-10W-Paper-v1 | mirror-watch | ●○○●·· | 12 | +1.8% [-3.8, +5.5] | G2: 12 clean condors (need 20) |

## Scorecard — normalized (Return on Risk) · legacy per-LEG view
> ⚠️ **Per-LEG grain** (kept for continuity) — for the graduation decision use the **Readiness board** above (per-condor, gated). Each trade = **pnl ÷ capital-at-risk** ("R"), so allocation and contract size cancel out. Sorted by expectancy. t-stat blows up for low-variance grinders (e.g. 3DTE) — don't rank on it alone.

### Ranked (n ≥ 20)
| Bot | Pillar | n | Exp(R) | t | Tot R | maxDD-R | WR |
|---|---|--:|--:|--:|--:|--:|--:|
| IC-SPX-FastPT25-S2-130PM | IC | 48 | +0.028 | 1.8 | +1.3 | -0.8 | 94% |
| GF-QQQ-IC-Touch0 | IC | 27 | +0.025 | 4.3 | +0.7 | -0.1 | 85% |
| GF-QQQ-IC-Ride | IC | 27 | +0.025 | 4.3 | +0.7 | -0.1 | 85% |
| GF-QQQ-IC-PT50 | IC | 26 | +0.016 | 3.1 | +0.4 | -0.1 | 88% |
| GF-QQQ-IC-Trail | IC | 27 | +0.008 | 1.8 | +0.2 | -0.1 | 78% |
| IC-SPX-FastPT25-S2 | IC | 29 | +0.006 | 2.7 | +0.2 | -0.0 | 48% |
| GF-QQQ-IC-SL100 | IC | 24 | +0.006 | 0.5 | +0.1 | -0.2 | 71% |
| GF-QQQ-IC-Canary | IC | 27 | +0.005 | 1.3 | +0.1 | -0.1 | 96% |
| GF-QQQ-IC-SL200 | IC | 24 | +0.003 | 0.3 | +0.1 | -0.2 | 75% |

### Provisional (n < 20 — tracked, not ranked; samples too small to trust)
| Bot | Pillar | n | Exp(R) | Tot R | raw P/L |
|---|---|--:|--:|--:|--:|
| Friday 14 DTE Broken Wing IB (B-70) | OA-Mirror | 4 | +0.087 | +0.3 | $675 |
| 3DTE $140-$350 | OA-Mirror | 8 | +0.039 | +0.3 | $345 |
| Trendy-Paper-v1 | OA-Mirror | 5 | +0.039 | +0.2 | $181 |
| GF-QQQ-IC-Ride-Delta | IC | 18 | +0.026 | +0.5 | $91 |
| IC-SPX-Fortress-Unstopped | IC | 1 | +0.020 | +0.0 | $100 |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 12 | +0.018 | +0.2 | $210 |
| Nigiri-Paper-v1 | OA-Mirror | 14 | +0.008 | +0.1 | $550 |
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | 4 | -0.003 | -0.0 | $-77 |
| DIR-SPX-CallVIXdrop | Directional | 8 | -0.217 | -1.7 | $-1,220 |

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
| 3DTE $140-$350 | OA-Mirror | 8 | 0 | 7 | 0.35 | 2027-10-04 |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 0 | 12 | 0 | insufficient data | insufficient data |
| DIR-SPX-CallVIXdrop | Directional | 8 | 0 | 7 | 0.35 | 2027-10-04 |
| DIR-SPX-PutVIX22-SL75 | Directional | 0 | 0 | 0 | insufficient data | insufficient data |
| Friday 14 DTE Broken Wing IB (B-70) | OA-Mirror | 4 | 0 | 4 | 0.20 | 2028-08-15 |
| GF-QQQ-IC-Canary | IC | 9 | 9 | 9 | 0.45 | 2027-07-09 |
| GF-QQQ-IC-PT50 | IC | 8 | 10 | 8 | 0.40 | 2027-08-17 |
| GF-QQQ-IC-Ride | IC | 9 | 9 | 9 | 0.45 | 2027-07-09 |
| GF-QQQ-IC-SL100 | IC | 5 | 14 | 5 | 0.25 | 2028-03-22 |
| GF-QQQ-IC-SL200 | IC | 6 | 12 | 6 | 0.30 | 2027-12-15 |
| GF-QQQ-IC-Touch0 | IC | 9 | 9 | 9 | 0.45 | 2027-07-09 |
| GF-QQQ-IC-Trail | IC | 9 | 9 | 9 | 0.45 | 2027-07-09 |
| IC-SPX-FastPT25-S2 | IC | 3 | 23 | 3 | 0.15 | 2029-04-16 |
| IC-SPX-FastPT25-S2-130PM | IC | 24 | 0 | 17 | 0.85 | 2027-01-26 |
| IC-SPX-Fortress-Unstopped | IC | 0 | 1 | 0 | insufficient data | insufficient data |
| Nigiri-Paper-v1 | OA-Mirror | 0 | 14 | 0 | insufficient data | insufficient data |
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | 2 | 0 | 2 | insufficient data | insufficient data |
| Trendy-Paper-v1 | OA-Mirror | 0 | 5 | 0 | insufficient data | insufficient data |

## Caveats
- **Positions:** 246 total (87 condors, 159 single-sided)  ·  333 legs.
- A condor has two spread rows paired by `trade_id` with `single_sided=False`; a single-sided position is any position that is not a condor (one spread row or `single_sided=True`). **Legs = OA position rows** (matches OA's "Positions" count). Win rate shown is per-position.
- A combined-`ironcondor` bot logs 1 leg per condor; a legged bot logs 2 — so Legs ≈ 2× condors only for legged bots. That's why they were confusing before.
- `Fix? = Y`: QQQ-IC bot carrying the call-side strike-resolution bug; data contaminated until fixed.
- Single-sided positions (not condors): 159 positions.
- Tiny-N bots are tracked but **not** evidence; read Trades before P/L.
