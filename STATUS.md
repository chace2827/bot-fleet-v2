# Bot Fleet — STATUS  ·  generated 2026-10-06

> **Numeric source of truth.** Auto-generated from `data/trades.csv` by `scripts/report.py`. Do not edit by hand. All figures are PAPER. Task backlog: `docs/backlog.md` (also in `dashboard.html`).

> **POST-CUTOVER LEDGER — `LEDGER_START = 2026-08-10`.** Every figure below is drawn from positions **opened on or after** that date. The v1 era is frozen in `data/archive/` and is never an input here.


## ⚠️ UNSIGNED PRE-REGISTRATION BOTS — DO NOT SWITCH ON

> The following bots have a pre-registration ledger entry with a blank, missing, or `NOT SIGNED` `SIGNED` line. No bot may be switched ON until the entry is signed and dated.

- QQQ long call
- QQQ-IC-0DTE-Fortress
- Tasty Condor


## Should-have-fired verdict — 2026-10-06

> SUSPECT rows split by `data/bot_gates.csv` `gate_type`. **1 structural** (no declared market gate) · **1 evidenced** (signed gate evaluated against tape). The split keeps the evidenced count meaningful without hiding anything.

| Bot | PR | Class | Verdict | Reason |
|---|---|---|---|---|
| IC-SPX-Fortress-Unstopped | INC-01 | STRUCTURAL | SUSPECT | no market gate and no fill_precondition declared; silence is suspect |
| 60min-ORB-10W-Paper-v1 | PR-12 | EVIDENCED | SUSPECT | SPX p=7836.17 at 11:05 breaks ORB range 7805.96-7835.09 (prior_close 7773.95) |

## Headline
- **Total closed P/L:** $5,063  ·  508 legs  ·  18 bots
  - Directional: $-1,055  (SPX $-1,055)
  - IC: $2,404  (QQQ $-901  ·  SPX $3,305)
  - OA-Mirror: $3,714  (SPX $990)

## Champion — IC-SPX-FastPT25-S2
- P/L **$-1,310**  ·  38 positions (10 condors, 28 single-sided) · 48 legs  ·  34 trading days (15 green / 7 red)
- Max drawdown (daily cumulative): $-3,210

## Focus roster — the bots you're actively perfecting  (OA: `*-Focus` groups)
> Close-to-live per pillar; for an A/B only the leading side. Select one group = per-pillar, all three = combined. Read per-bot R (readiness board), not the subtotal.

| Pillar | Bot | Status | Trades | P/L | WR |
|---|---|---|--:|--:|--:|
| IC | IC-SPX-FastPT25-S2 | ON | 38 | $-1,310 | 42% |
| Directional | DIR-SPX-CallVIXdrop | ON | 11 | $-1,055 | 36% |
| OA-Mirror | 3DTE $140-$350 | ON | 15 | $630 | 100% |
| OA-Mirror | Nigiri-Paper-v1 | ON | 26 | $1,020 | 92% |
| OA-Mirror | Friday 14 DTE Broken Wing IB (B-70) | ON | 7 | $1,360 | 100% |
| **Total** | | | | **$645** | |

## Monitor — live but not focus  (OA: `Monitor` group)
> Running and watched — A/B laggards, controls, other active mirrors, the pending-decision QQQ-Fortress pair. Not promotion candidates yet.

| Pillar | Bot | Status | Trades | P/L | WR |
|---|---|---|--:|--:|--:|
| IC | GF-QQQ-IC-Trail | ON | 29 | $-1,101 | 83% |
| IC | GF-QQQ-IC-SL200 | ON | 27 | $-818 | 70% |
| IC | GF-QQQ-IC-PT50 | ON | 28 | $-708 | 86% |
| IC | GF-QQQ-IC-SL100 | ON | 30 | $-277 | 63% |
| IC | GF-QQQ-IC-Canary | ON | 30 | $-150 | 87% |
| IC | QQQ-IC-0DTE-Fortress-NoPT50 | ON | 6 | $78 | 67% |
| IC | GF-QQQ-IC-Ride | ON | 29 | $641 | 86% |
| IC | IC-SPX-Fortress-Unstopped | ON | 5 | $800 | 100% |
| IC | GF-QQQ-IC-Touch0 | ON | 30 | $1,343 | 83% |
| IC | IC-SPX-FastPT25-S2-130PM | ON | 36 | $3,815 | 83% |
| OA-Mirror | Trendy-Paper-v1 | ON | 8 | $344 | 100% |
| OA-Mirror | 60min-ORB-10W-Paper-v1 | ON | 15 | $360 | 87% |
| **Total** | | | | **$4,327** | |

**Archive (OA: `Archive` group):** 1 off/dead bots · $91 closed — excluded from the working view (still exported for the ledger).

## Allocation audit — sizing realism  (ON bots, per-position)
> R (pnl÷risk) already cancels size, so this changes **no ranking** — it flags whether the paper sizing is realistic to carry live. Hold class sets the rule: **0DTE** recycles risk daily; **swing/multi-week** ties capital up for the whole hold (max-risk/day = concurrent open risk, not daily deploy). **1-lot bots are fill-untested at scale** — their edge won't survive the slippage of a real order size (ties to the v5-slippage task).

| Bot | Pillar | Hold | Pos | med Qty | med Risk$ | max Risk$ | Realism |
|---|---|---|--:|--:|--:|--:|:--|
| GF-QQQ-IC-Touch0 | IC | 0DTE | 30 | 26 | $4,992 | $5,018 | sized ✓ |
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | 0DTE | 6 | 26 | $4,940 | $4,992 | sized ✓ |
| GF-QQQ-IC-Trail | IC | 0DTE | 29 | 26 | $4,914 | $5,018 | sized ✓ |
| GF-QQQ-IC-SL200 | IC | 0DTE | 27 | 26 | $4,914 | $5,018 | sized ✓ |
| GF-QQQ-IC-PT50 | IC | 0DTE | 28 | 26 | $4,914 | $5,018 | sized ✓ |
| GF-QQQ-IC-SL100 | IC | 0DTE | 30 | 26 | $4,914 | $5,018 | sized ✓ |
| GF-QQQ-IC-Ride | IC | 0DTE | 29 | 26 | $4,914 | $5,018 | sized ✓ |
| IC-SPX-FastPT25-S2 | IC | 0DTE | 38 | 10 | $4,900 | $4,900 | sized ✓ |
| IC-SPX-Fortress-Unstopped | IC | 0DTE | 5 | 10 | $4,900 | $4,900 | sized ✓ |
| IC-SPX-FastPT25-S2-130PM | IC | 0DTE | 36 | 10 | $4,750 | $4,900 | sized ✓ |
| GF-QQQ-IC-Canary | IC | 0DTE | 30 | 1 | $193 | $193 | **1-lot — fill-untested** |
| DIR-SPX-CallVIXdrop | Directional | 0DTE | 11 | 1 | $615 | $725 | **1-lot — fill-untested** |
| Nigiri-Paper-v1 | OA-Mirror | 7d swing | 26 | 10 | $4,910 | $4,960 | sized ✓ |
| Friday 14 DTE Broken Wing IB (B-70) | OA-Mirror | 14d multi-wk | 7 | 1 | $1,910 | $1,995 | **1-lot — fill-untested** |
| 3DTE $140-$350 | OA-Mirror | 5d swing | 15 | 1 | $950 | $1,910 | **1-lot — fill-untested** |
| Trendy-Paper-v1 | OA-Mirror | 10d multi-wk | 8 | 1 | $933 | $943 | **1-lot — fill-untested** |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 0DTE | 15 | 1 | $910 | $930 | **1-lot — fill-untested** |

> **Read:** SPX-IC + Nigiri run ~10-lot (~$4.8k/position, comparable to the champion). Every other mirror + both directional bots run **1 lot** ($0.5k–$2.9k) — realistic for tracking W/L, not for reading a live-scale edge. Sizing rule is per-bot by hold class (see backlog COCKPIT LANE step 1); the go-live target is ~$10k max risk/day with a hedge reserve carved out first.

## Hedge tournament (live-data counterfactual)
> **The productized loss autopsy.** Every ledger leg with risk > 0 replayed through the v1 hedge library — Actual (the recorded outcome), PT+X%/SL-X% return-threshold rules, and an S2 strike-touch cut (tape-gated, 5-min grain, bounded at the position's actual close). **The two populations are reported separately and never pooled** — `status=expired` scores against settlement, `status=closed` against the exit that actually happened. **Optimistic bound, not a live estimate** — every non-Actual arm assumes a fill exactly at the threshold; real fills slip. Compare rules by **R** (pnl÷risk), never $. Basis: PT/SL % are of the credit collected (`|premium|`), per `mfe_pct`/`mae_pct` already carrying that unit (verified against the ledger — see `scripts/hedge_tournament.py` docstring). **Defang: deferred v1** (345 legs marked, not modeled — needs an intraday premium-decay path not yet in the ledger).

> **`settle` = NOT EVALUABLE** (287 closed legs marked, never modeled — what a closed leg would have returned held to settlement needs post-exit path data that does not exist).

### Settled at expiry (`status=expired`) — `actual` = settlement pnl

| Rule | N | Exp(R) | Tot R | WR | maxDD-R | worst-R |
|---|--:|--:|--:|--:|--:|--:|
| actual | 58 | +5.1% | +2.94 | 100% | 0.00 | +2.0% |
| pt25 | 58 | +1.3% | +0.74 | 100% | 0.00 | +0.5% |
| pt50 | 58 | +2.6% | +1.48 | 100% | 0.00 | +1.0% |
| pt100 | 58 | +5.1% | +2.94 | 100% | 0.00 | +2.0% |
| sl50 | 58 | +1.3% | +0.78 | 48% | -0.11 | -4.3% |
| sl75 | 58 | +2.7% | +1.54 | 71% | -0.11 | -4.8% |
| sl100 | 58 | +3.0% | +1.73 | 78% | -0.11 | -6.4% |
| sl130 | 58 | +3.4% | +1.98 | 84% | -0.12 | -8.3% |
| s2 | 24 | +4.4% | +1.06 | 96% | -0.24 | -24.1% |

#### Per-bot cut — expired  (Actual vs SL75 — the mid-spectrum published rung)
| Bot | N | Actual Exp(R) | SL75 Exp(R) | Δ |
|---|--:|--:|--:|--:|
| IC-SPX-FastPT25-S2-130PM | 45 | +5.6% | +2.9% | -2.7pp |
| 3DTE $140-$350 | 6 | +4.0% | +1.9% | -2.1pp |
| IC-SPX-FastPT25-S2 | 6 | +2.4% | +1.5% | -0.9pp |
| IC-SPX-Fortress-Unstopped | 1 | +2.0% | +2.0% | +0.0pp |

#### Regime cut — expired  (Actual vs SL75, by tape-derived regime label)
| Regime | N | Actual Exp(R) | SL75 Exp(R) |
|---|--:|--:|--:|
| Chop | 26 | +5.4% | +3.3% |
| n/a | 32 | +4.8% | +2.2% |

### Closed early (`status=closed`) — `actual` = the recorded exit fill, not settlement

| Rule | N | Exp(R) | Tot R | WR | maxDD-R | worst-R |
|---|--:|--:|--:|--:|--:|--:|
| actual | 287 | +0.4% | +1.13 | 79% | -1.97 | -58.6% |
| pt25 | 287 | +0.7% | +2.01 | 91% | -1.03 | -58.6% |
| pt50 | 287 | +1.4% | +3.90 | 86% | -0.89 | -58.6% |
| pt100 | 287 | +1.0% | +2.78 | 79% | -1.92 | -58.6% |
| sl50 | 287 | -0.0% | -0.08 | 53% | -2.23 | -50.0% |
| sl75 | 287 | -0.2% | -0.59 | 57% | -2.67 | -58.6% |
| sl100 | 287 | +0.3% | +0.91 | 70% | -1.77 | -58.6% |
| sl130 | 287 | +0.4% | +1.19 | 74% | -1.63 | -58.6% |
| s2 | 96 | +1.4% | +1.33 | 85% | -0.82 | -75.3% |

#### Per-bot cut — closed  (Actual vs SL75 — the mid-spectrum published rung)
| Bot | N | Actual Exp(R) | SL75 Exp(R) | Δ |
|---|--:|--:|--:|--:|
| GF-QQQ-IC-Ride | 29 | +2.5% | +0.5% | -1.9pp |
| GF-QQQ-IC-Touch0 | 29 | +2.5% | +0.5% | -1.9pp |
| GF-QQQ-IC-Ride-Delta | 18 | +2.6% | +0.9% | -1.7pp |
| GF-QQQ-IC-PT50 | 27 | +1.6% | +0.6% | -1.0pp |
| Friday 14 DTE Broken Wing IB (B-70) | 4 | +8.7% | +8.7% | +0.0pp |
| GF-QQQ-IC-Trail | 28 | +0.9% | -0.1% | -1.0pp |
| 60min-ORB-10W-Paper-v1 | 12 | +1.8% | +1.6% | -0.2pp |
| Trendy-Paper-v1 | 5 | +3.9% | -1.8% | -5.7pp |
| GF-QQQ-IC-SL100 | 25 | +0.7% | +0.4% | -0.3pp |
| GF-QQQ-IC-Canary | 29 | +0.5% | -0.2% | -0.7pp |
| GF-QQQ-IC-SL200 | 25 | +0.5% | +0.3% | -0.2pp |
| Nigiri-Paper-v1 | 14 | +0.8% | -0.1% | -0.9pp |
| 3DTE $140-$350 | 2 | +3.7% | -0.1% | -3.8pp |
| IC-SPX-FastPT25-S2 | 23 | +0.1% | +0.2% | +0.0pp |
| QQQ-IC-0DTE-Fortress-NoPT50 | 4 | -0.3% | +1.0% | +1.3pp |
| IC-SPX-FastPT25-S2-130PM | 5 | -21.9% | -1.8% | +20.1pp |
| DIR-SPX-CallVIXdrop | 8 | -21.7% | -21.7% | +0.0pp |

#### Regime cut — closed  (Actual vs SL75, by tape-derived regime label)
| Regime | N | Actual Exp(R) | SL75 Exp(R) |
|---|--:|--:|--:|
| Chop | 57 | +1.3% | -0.6% |
| Drift | 25 | +2.5% | +1.1% |
| Trend | 17 | -1.3% | -1.7% |
| n/a | 188 | -0.0% | -0.1% |

> N is small and concentrated in the last few tape-covered trading days (tape.py is new); the S2 arm and the regime cut will thicken as more days accrue. Read this as an early ranking to cross-check the LEAN/OA backtest tournament, not a standalone verdict.

## Trade-window heat map — when do shorts actually get touched (hour x regime)
> **The 11am-vs-1:30 question, generalized.** Every ledger position's worst-adverse-excursion (MAE) timestamp, bucketed by hour-of-day x tape-derived regime (Drift/Trend/Chop/n-a). `touch %` = short-strike touch rate, scored only on positions with same-day tape coverage (a small, recent subset — most history predates `tape.py`); `MAE` = mean adverse excursion as % of credit, computed on ALL positions in the bucket regardless of tape coverage. Cells are `n=… · touch …% · MAE …%`; blank touch% = no tape-covered position fell in that cell. **Small-n cells are directional, not conclusive** — read the n before the rate.

| Hour | Chop | Drift | Trend | n/a |
|---|---|---|---|---|
| 09:30-10 | n=1 · MAE -2.1% | — | — | n=6 · MAE -0.4% |
| 10-11 | n=2 · touch 0% · MAE -0.1% | — | — | n=20 · MAE -0.7% |
| 11-12 | n=12 · touch 0% · MAE -0.1% | — | — | n=46 · MAE -0.7% |
| 12-13 | n=3 · touch 50% · MAE -0.8% | — | — | n=9 · MAE -0.6% |
| 13-14 | n=37 · touch 22% · MAE -0.6% | n=12 · touch 0% · MAE -0.1% | n=7 · touch 0% · MAE -1.0% | n=153 · MAE -0.8% |
| 14-15 | n=9 · touch 0% · MAE -0.7% | n=13 · touch 0% · MAE -0.7% | n=2 · touch 100% · MAE -1.4% | n=32 · MAE -2.3% |
| 15-16 | — | — | n=1 · touch 0% · MAE -1.1% | n=20 · MAE -4.7% |

> **Read:** touches cluster at **14-15 (Trend)** — 1 of 1 tape-covered position(s) scored there touched (touch rate 100%). Tape coverage is thin (5 days) — treat as an early signal, not a verdict.

## Lessons index — tagged, searchable  (data/lessons.csv)
> Every graded bot-day's "day's lesson" (from the brief JSON's Verdict row; session-log fallback only for dates the brief never covered), tagged from a fixed vocabulary (`entry-timing · hedge · filter · regime · sizing · other`) by simple keyword rules (see `scripts/lessons.py` docstring) — not an ML classifier. Grouped by tag, most recent first.

**Tag counts:** 

#### oa-drive (4)
- **2026-09-17** · - — In the OA drawer Escape closes the ENTIRE drawer (discarding an unsaved New Backtest form) — close inner pickers via their back arrow or X, never Escape; also re-locate buttons right before clicking because the drawer scroll position changes
- **2026-09-17** · - — A malformed crules rule or invalid JSON does NOT error — the page silently falls back to the UNRULED control and renders a complete-looking result, while the SPA-sticky drawer can still show the rule. Verify what ran from the URL and the row count, never the drawer; a combined run whose row count equals the control is presumed unruled
- **2026-09-17** · - — A combined positions export is a RESULT, not a census — 249+249=498 standalone vs an unruled control of 497, one row dropped with caps permitting it and no error. Reconcile every combine row-for-row against standalone exports before ranking
- **2026-09-16** · - — Trusted-click misses on small icon buttons (drawer X, deleteRule X) land on padding and silently do nothing — click the icon element's own center, then re-read state

#### capture (2)
- **2026-09-17** · - — wc -l undercounts these OA CSV exports by one — they carry no trailing newline. Count rows with a CSV reader, never a line count
- **2026-09-16** · - — Clipboard captures are volatile: run the Copy click and pbpaste > file in the SAME exec call, then verify the file header before moving on

#### tooling (2)
- **2026-09-17** · - — oa_shots.mjs is a fixed capture script not a generic screenshot tool — invoking its `shot` arg re-ran its built-in sequence and overwrote 8 verified PNGs in data/captures/2026-09-16-oa-backtester/ (restored via git restore). Put a generic `shot` in oa_cdp.mjs instead; never run oa_shots.mjs except as its original one-shot capture
- **2026-09-16** · - — CDP helper scripts print then hang on WebSocket teardown — add explicit setTimeout(process.exit) after close

## Per-bot (sorted by P/L)
| Bot | Pillar | Und | Role | Status | Trades | Legs | P/L | WR | Fix? |
|---|---|---|---|---|--:|--:|--:|--:|:--:|
| IC-SPX-FastPT25-S2 | IC | SPX | live-candidate | ON | 38 | 48 | $-1,310 | 42% | - |
| GF-QQQ-IC-Trail | IC | QQQ | experiment | ON | 29 | 38 | $-1,101 | 83% | - |
| DIR-SPX-CallVIXdrop | Directional | SPX | experiment | ON | 11 | 11 | $-1,055 | 36% | - |
| GF-QQQ-IC-SL200 | IC | QQQ | experiment | ON | 27 | 34 | $-818 | 70% | - |
| GF-QQQ-IC-PT50 | IC | QQQ | experiment | ON | 28 | 36 | $-708 | 86% | - |
| GF-QQQ-IC-SL100 | IC | QQQ | experiment | ON | 30 | 36 | $-277 | 63% | - |
| GF-QQQ-IC-Canary | IC | QQQ | instrument | ON | 30 | 44 | $-150 | 87% | - |
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | QQQ | experiment | ON | 6 | 9 | $78 | 67% | Y |
| GF-QQQ-IC-Ride-Delta | IC | QQQ | experiment | OFF | 15 | 18 | $91 | 93% | - |
| Trendy-Paper-v1 | OA-Mirror | — | mirror-watch | ON | 8 | 8 | $344 | 100% | - |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | SPX | mirror-watch | ON | 15 | 15 | $360 | 87% | - |
| 3DTE $140-$350 | OA-Mirror | SPX | mirror-watch | ON | 15 | 15 | $630 | 100% | - |
| GF-QQQ-IC-Ride | IC | QQQ | control | ON | 29 | 40 | $641 | 86% | - |
| IC-SPX-Fortress-Unstopped | IC | SPX | control | ON | 5 | 8 | $800 | 100% | - |
| Nigiri-Paper-v1 | OA-Mirror | — | mirror-watch | ON | 26 | 26 | $1,020 | 92% | - |
| GF-QQQ-IC-Touch0 | IC | QQQ | experiment | ON | 30 | 43 | $1,343 | 83% | - |
| Friday 14 DTE Broken Wing IB (B-70) | OA-Mirror | — | mirror-watch | ON | 7 | 7 | $1,360 | 100% | - |
| IC-SPX-FastPT25-S2-130PM | IC | SPX | experiment | ON | 36 | 72 | $3,815 | 83% | - |

## Readiness board — per-condor, gated (the graduation view)
> **Grain = condor** (legs summed), not leg. Six ordered gates; the **first red (○) gate is the named blocker**. `●`=pass `○`=fail `·`=pending. Exp(R) shows the **bootstrap 95% CI** (replaces the t-stat). Stage: INCUBATE→VALIDATE→CANDIDATE→LIVE-READY (LIVE = real capital). Controls & mirror-watch are listed separately — they can't graduate by design.
> **Gates:** G1 clean data (no strike-bug, single-sided excluded) · G2 ≥20 clean condors · G3 Exp(R)>0 w/ 95% CI above 0 · G4 maxDD-R within cap (RoE $ cap still a `<FILL>` blank) · G5 instruction-mirror ≥90% (from the daily brief / `data/compliance.csv`; pending until ≥5 graded days) · G6 OOS/regime robustness.

| Bot | Role | Stage | Gates | n | Exp(R) [95% CI] | Blocker |
|---|---|---|:--:|--:|--:|---|
| GF-QQQ-IC-Touch0 | experiment | CANDIDATE | ●○●●·· | 13 | +5.0% [+1.8, +7.9] | G2: 13 clean condors (need 20) |
| GF-QQQ-IC-PT50 | experiment | CANDIDATE | ●○●●·· | 8 | +3.2% [+0.3, +5.2] | G2: 8 clean condors (need 20) |
| IC-SPX-FastPT25-S2-130PM | experiment | CANDIDATE | ●●○●·○ | 36 | +2.2% [-6.2, +9.1] | G3: CI includes 0 (~371 more trades) |
| GF-QQQ-IC-Ride-Delta | experiment | VALIDATE | ●○○●·· | 3 | +2.4% [-6.3, +7.3] | G2: 3 clean condors (need 20) |
| GF-QQQ-IC-SL100 | experiment | VALIDATE | ●○○●·· | 6 | +1.0% [-1.9, +3.9] | G2: 6 clean condors (need 20) |
| GF-QQQ-IC-Trail | experiment | VALIDATE | ●○○●·· | 9 | +0.8% [-1.2, +2.3] | G2: 9 clean condors (need 20) |
| GF-QQQ-IC-Canary | instrument | VALIDATE | ●○○●·· | 14 | +0.6% [-1.1, +1.9] | G2: 14 clean condors (need 20) |
| GF-QQQ-IC-SL200 | experiment | VALIDATE | ●○○●·· | 7 | -2.0% [-6.3, +2.4] | G2: 7 clean condors (need 20) |
| IC-SPX-FastPT25-S2 | live-candidate | VALIDATE | ●○○●·· | 10 | -2.4% [-17.3, +6.2] | G2: 10 clean condors (need 20) |
| DIR-SPX-CallVIXdrop | experiment | VALIDATE | ●○○●·· | 11 | -13.9% [-46.5, +25.3] | G2: 11 clean condors (need 20) |
| QQQ-IC-0DTE-Fortress-NoPT50 | experiment | VALIDATE | ○○○●·· | 3 | -2.5% [-6.8, +5.3] | G1: strike-bug contamination |

#### Non-graduating (controls / mirror-watch — tracked, can't go live)
| Bot | Role | Gates | n | Exp(R) [95% CI] | Note |
|---|---|:--:|--:|--:|---|
| Nigiri-Paper-v1 | mirror-watch | ●●●●·● | 26 | +0.8% [+0.6, +1.0] | G5: compliance 0/5 graded days (daily brief) |
| Friday 14 DTE Broken Wing IB (B-70) | mirror-watch | ●○●●·· | 7 | +10.1% [+7.7, +12.9] | G2: 7 clean condors (need 20) |
| GF-QQQ-IC-Ride | control | ●○●●·· | 11 | +4.7% [+0.8, +8.4] | G2: 11 clean condors (need 20) |
| Trendy-Paper-v1 | mirror-watch | ●○●●·· | 8 | +4.6% [+3.4, +5.8] | G2: 8 clean condors (need 20) |
| IC-SPX-Fortress-Unstopped | control | ●○●●·· | 3 | +4.1% [+4.1, +4.1] | G2: 3 clean condors (need 20) |
| 3DTE $140-$350 | mirror-watch | ●○●●·· | 15 | +4.0% [+3.7, +4.3] | G2: 15 clean condors (need 20) |
| 60min-ORB-10W-Paper-v1 | mirror-watch | ●○○●·· | 15 | +2.6% [-1.9, +5.6] | G2: 15 clean condors (need 20) |

## Scorecard — normalized (Return on Risk) · legacy per-LEG view
> ⚠️ **Per-LEG grain** (kept for continuity) — for the graduation decision use the **Readiness board** above (per-condor, gated). Each trade = **pnl ÷ capital-at-risk** ("R"), so allocation and contract size cancel out. Sorted by expectancy. t-stat blows up for low-variance grinders (e.g. 3DTE) — don't rank on it alone.

### Ranked (n ≥ 20)
| Bot | Pillar | n | Exp(R) | t | Tot R | maxDD-R | WR |
|---|---|--:|--:|--:|--:|--:|--:|
| GF-QQQ-IC-Touch0 | IC | 43 | +0.014 | 1.6 | +0.6 | -0.4 | 81% |
| GF-QQQ-IC-Ride | IC | 40 | +0.012 | 0.9 | +0.5 | -0.5 | 82% |
| IC-SPX-FastPT25-S2-130PM | IC | 72 | +0.011 | 0.6 | +0.8 | -1.0 | 92% |
| Nigiri-Paper-v1 | OA-Mirror | 26 | +0.008 | 8.7 | +0.2 | 0.0 | 92% |
| GF-QQQ-IC-SL100 | IC | 36 | +0.004 | 0.4 | +0.1 | -0.2 | 64% |
| GF-QQQ-IC-PT50 | IC | 36 | +0.003 | 0.2 | +0.1 | -0.5 | 86% |
| GF-QQQ-IC-SL200 | IC | 34 | +0.001 | 0.1 | +0.0 | -0.2 | 71% |
| GF-QQQ-IC-Trail | IC | 38 | -0.004 | -0.3 | -0.1 | -0.5 | 82% |
| IC-SPX-FastPT25-S2 | IC | 48 | -0.006 | -0.4 | -0.3 | -0.7 | 52% |
| GF-QQQ-IC-Canary | IC | 44 | -0.018 | -1.1 | -0.8 | -0.9 | 91% |

### Provisional (n < 20 — tracked, not ranked; samples too small to trust)
| Bot | Pillar | n | Exp(R) | Tot R | raw P/L |
|---|---|--:|--:|--:|--:|
| Friday 14 DTE Broken Wing IB (B-70) | OA-Mirror | 7 | +0.101 | +0.7 | $1,360 |
| Trendy-Paper-v1 | OA-Mirror | 8 | +0.046 | +0.4 | $344 |
| 3DTE $140-$350 | OA-Mirror | 15 | +0.040 | +0.6 | $630 |
| GF-QQQ-IC-Ride-Delta | IC | 18 | +0.026 | +0.5 | $91 |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 15 | +0.026 | +0.4 | $360 |
| IC-SPX-Fortress-Unstopped | IC | 8 | +0.020 | +0.2 | $800 |
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | 9 | +0.002 | +0.0 | $78 |
| DIR-SPX-CallVIXdrop | Directional | 11 | -0.139 | -1.5 | $-1,055 |

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
| 3DTE $140-$350 | OA-Mirror | 15 | 0 | 9 | 0.45 | 2027-07-09 |
| 60min-ORB-10W-Paper-v1 | OA-Mirror | 0 | 15 | 0 | insufficient data | insufficient data |
| DIR-SPX-CallVIXdrop | Directional | 11 | 0 | 5 | 0.25 | 2028-03-08 |
| DIR-SPX-PutVIX22-SL75 | Directional | 0 | 0 | 0 | insufficient data | insufficient data |
| Friday 14 DTE Broken Wing IB (B-70) | OA-Mirror | 7 | 0 | 5 | 0.25 | 2028-03-30 |
| GF-QQQ-IC-Canary | IC | 14 | 16 | 9 | 0.45 | 2027-07-14 |
| GF-QQQ-IC-PT50 | IC | 8 | 20 | 3 | 0.15 | 2029-03-19 |
| GF-QQQ-IC-Ride | IC | 11 | 18 | 6 | 0.30 | 2027-12-10 |
| GF-QQQ-IC-SL100 | IC | 6 | 24 | 1 | insufficient data | insufficient data |
| GF-QQQ-IC-SL200 | IC | 7 | 20 | 2 | insufficient data | insufficient data |
| GF-QQQ-IC-Touch0 | IC | 13 | 17 | 8 | 0.40 | 2027-08-19 |
| GF-QQQ-IC-Trail | IC | 9 | 20 | 4 | 0.20 | 2028-07-31 |
| IC-SPX-FastPT25-S2 | IC | 10 | 28 | 9 | 0.45 | 2027-07-26 |
| IC-SPX-FastPT25-S2-130PM | IC | 36 | 0 | 16 | 0.80 | 2027-02-01 |
| IC-SPX-Fortress-Unstopped | IC | 3 | 2 | 3 | 0.15 | 2029-05-04 |
| Nigiri-Paper-v1 | OA-Mirror | 0 | 26 | 0 | insufficient data | insufficient data |
| QQQ-IC-0DTE-Fortress-NoPT50 | IC | 3 | 3 | 2 | insufficient data | insufficient data |
| Trendy-Paper-v1 | OA-Mirror | 0 | 8 | 0 | insufficient data | insufficient data |

## Caveats
- **Positions:** 385 total (123 condors, 262 single-sided)  ·  508 legs.
- A condor has two spread rows paired by `trade_id` with `single_sided=False`; a single-sided position is any position that is not a condor (one spread row or `single_sided=True`). **Legs = OA position rows** (matches OA's "Positions" count). Win rate shown is per-position.
- A combined-`ironcondor` bot logs 1 leg per condor; a legged bot logs 2 — so Legs ≈ 2× condors only for legged bots. That's why they were confusing before.
- `Fix? = Y`: QQQ-IC bot carrying the call-side strike-resolution bug; data contaminated until fixed.
- Single-sided positions (not condors): 262 positions.
- Tiny-N bots are tracked but **not** evidence; read Trades before P/L.
