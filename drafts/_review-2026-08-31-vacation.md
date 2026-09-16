# Vacation-period position review — 2026-08-20 → 2026-08-31
Source: OA closed-position export (Analyze range since 08/01), 207 rows, captured 2026-08-31.
Cross-check: rows closing before 08-20 sum to **$4,706 / 71 legs — exact match** to the committed
08-19 STATUS.md. The export is the complete August record on a second surface.

## Headline
- **Vacation closed P/L: -$2,702 over 136 legs** (OA-Analyze basis, close-date, incl. legacy).
- Decomposition: **QQQ long call legacy expiry -$2,971** (opened 06-01, expired 08-31, -100% RoR)
  + Tasty Condor legacy expiry +$418 (opened 06-22, expired 08-21) = -$2,553 from PRE-CUTOVER
  legacy positions. **Ex-legacy vacation P/L: -$149** — the armed fleet was flat.
- Ledger-eligible (opened ≥ 08-10): vacation contributes **-$149**, so post-backfill cumulative
  ≈ **$4,557** (from $4,706).
- Red days: 08-26 -$1,899 · 08-27 -$2,038 · 08-31 -$2,127 (the last is 84% the legacy expiry).

## F-1 · 130PM champion — the tail arrived, and it survived
16/16 two-sided condors Aug 10–31. Cum $6,200 by 08-25, then **-$1,500 (08-26, call side -1650)**
and **-$1,800 (08-27, put side -1900)**, recovered to **+$4,200**. Per-condor: Exp(R) **+0.055**,
TotR +0.89, maxDD-R **-0.68**, wins ≈ +0.11R, losses -0.31/-0.37R (NOT full -1.0R max loss —
exits fired mid-move). W30/L2 by leg. The "10-for-10 hides the tail" warning materialized at
~⅓ max-loss size, twice, and the strategy is still net strongly positive. n=16 of G2's 20.
**CORRECTION: PR-02 is SIGNED (2026-08-09) and its verification rider was DISCHARGED BY
SUBSTITUTE 2026-08-18** — earlier "unsigned champion" memory notes are stale.

## F-2 · I-06 resolves differently than expected — PR-04 is SIGNED, verification was OWED
QQQ-IC-0DTE-Fortress-NoPT50 entered a fresh condor **08-26 13:31** (put +104 / call -442 =
**-$338**, both legs closed 15:50 = the time exit). The ledger shows PR-04 **SIGNED 2026-08-09**;
the banner lists it unsigned only because the parser (by design) treats
`SIGNED != VERIFIED` + `FIRST-TRADING-DAY CAPTURE OWED` as unsigned. The 08-26 fill IS its first
trading day — the owed Step-6 evidence now exists in OA. **Discharge path: capture the 08-26
position's Trades list (time-exit row present, NO PT row) + BACKSTOP_CAUGHT_IT negative, next OA
session** — precedent: R-2026-08-18 SUBSTITUTE-VERIFY (5a). CSV evidence is consistent
(15:50 closes) but is not the capture the entry demands.

## F-3 · Ride-Delta double-fire is SYSTEMIC, its sample is contaminated
Duplicate same-side entries seconds apart on **6 of 9 vacation trading days** (08-14, 08-17,
08-19, 08-21, 08-25 ×2 CALL spreads, 08-31). It "leads" the GF family (+$91) because winners are
mechanically doubled — an artifact, not edge. n=18 rows ≈ 9 true bot-days.

## F-4 · GF family: the delta-0.10 fix WORKS — condors now form
Call sides fired on 5 of 6 vacation entry days (vs zero pre-fix). PT50: 6/9 days two-sided. The
family survived its first losing day (08-26, ~-0.06R each) as designed. Exp(R)/day +0.01…+0.05.

## F-5 · DIR-SPX-CallVIXdrop: three consecutive ~-0.5R losses
08-19 -320, 08-21 -335, 08-27 -365 (SL50 each time). Full Aug: W1/L3, Exp(R) **-0.366/trade**,
TotR -1.47. n=4 — below kill conviction, but the worst live line on the fleet.

## F-6 · 11AM S2 defect persists (with one anomaly)
Puts-only 2-minute scratch exits continue through vacation (11:01→11:03 pattern, 9 more
instances). Anomaly: **08-31 both sides EXPIRED** at full profit (+$200) — first held-to-close
day ever. 3/14 bot-days two-sided. Still not running its intended strategy.

## F-7 · "Friday 14 DTE Broken Wing IB (B-70)" — ✗ FALSIFIED by the 08-31 OA sweep
SPX iron butterfly, 08-14→08-25, +$140. It was ALREADY in `bots_meta.csv` (line 24, OA-Mirror /
mirror-watch), already matched by roster.py's Live-mirrors rule, already in the 08-19 capture and
the OA-Mirror-Focus group. The review's "unknown bot / backfill blocker" claim was wrong — an
inference from stale memory, never checked against the file. Backfill was never blocked.

## F-8 · Legacy open-position exposure was invisible
Both legacy expiries (QQQ long call -2,971; Tasty +418) rode positions opened in June while the
bots' toggles were OFF — toggles stop NEW entries, not existing exposure. Neither appears in the
post-cutover ledger (open-date < 08-10). Action: enumerate any REMAINING legacy open positions.

## Provisional R-sheet (per-condor where derivable; provisional until backfill regenerates STATUS.md)
| Bot | condor-days | Exp(R) | TotR | maxDD-R | Note |
|---|--:|--:|--:|--:|---|
| IC-SPX-FastPT25-S2-130PM | 16 | +0.055 | +0.89 | -0.68 | 4 days from G2 n=20 |
| GF-QQQ-IC-PT50 | 9 | +0.025 | +0.22 | -0.06 | family-representative |
| GF-QQQ-IC-Ride-Delta | 9* | +0.052 | +0.47 | -0.06 | *contaminated (F-3) |
| IC-SPX-FastPT25-S2 (11AM) | 14 | +0.006 | +0.08 | -0.01 | defective mechanism (F-6) |
| QQQ-IC-0DTE-Fortress-NoPT50 | 1 | -0.068 | -0.07 | -0.07 | unsigned, armed (F-2) |
| DIR-SPX-CallVIXdrop | 4 | -0.366 | -1.47 | -1.57 | kill-watch (F-5) |

Full-Aug per-leg table for all 20 bots with fills: see chat / regenerate at backfill.

## Allocation read (from position risk)
Already internally consistent: GF family (~$190-193/leg, all 8), FastPT25 siblings (~$4,700-4,900).
Known misalignment: DIR-SPX-CallVIXdrop alloc $50k vs put pair $10k (risk-per-trade is fine at
1ct; nominal alloc only). NoPT50 risks $4,940/side — QQQ Fortress line reportedly at $100k alloc.
Final edit list needs current alloc values read from OA (next OA session).

## 08-31 OA-sweep addenda (corrections + new facts)
- **F-6 RESTATED**: 11AM S2's exit logic is NOT broken. `Scalp-Mon-S2-Cleanup` = "open ≥2min AND
  exactly 1 open position → close 100%" — the 2-minute scratches are the designed one-leg guard.
  The real defect is ENTRY-side: the call side fills on only 3 of 14 bot-days. 08-31 both sides
  filled → condor rode to expiry, +$200, as designed. 4/4 automation hashes byte-identical to the
  08-07 baseline.
- **Ride-Delta root cause**: FOUR scanners on (shared GF pair + bot-local Ride-Delta pair),
  functionally identical since the 08-17 family-wide delta change; same-tick race double-fires one
  side, and the 2-positions/day safeguard then BLOCKS the other side → one-sided trades, not
  doubled condors. Pre-fix sample = a different strategy; EXCLUDE, don't discount. Post-fix the
  bot would be config-identical to GF-QQQ-IC-Ride — PR-23's delta-vs-fixed hypothesis was MOOTED
  when R-2026-08-17-GF-ENTRY-METHOD made the whole family delta-based. Disposition = Andy.
- **Allocations (07-…tsv)**: families already aligned — DIR trio $10K each (the $50K note was
  stale), Fortress $100K, GF $2.5K, FastPT25 live pair $50K. Only gaps: mirror family — 8 @ $10K,
  `3DTE $140-$350` @ $5K, `QQQ long call` @ $30K. `QQQ-IC-0DTE-Fortress` is in no OA group.
- **Legacy opens (F-8 quantified)**: THREE remaining, all `QQQ long call` (toggles OFF) — opened
  Jun 15 / 22 / 29, risk $10,065 total, unrealised **-$8,691**. Salvage-vs-ride is Andy's call.
- PR-04 discharge evidence captured 3/3 PASS (`04-pr04-discharge-trades-2026-08-31.txt`).
  Roster capture #3: 44 bots, ZERO toggle drift vs 08-19.
