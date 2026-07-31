# OA Grab Bookmarklet — Page-by-Page Coverage

*Written 2026-07-29 · companion to `docs/oa-capture-bookmarklet-2026-07-28.md` (which covers HOW to capture automation trees). This document covers HOW WELL the bookmarklet captures the DATA pages, which is a different question with a different answer per page.*

Tested against three live captures with matching screenshots taken 2026-07-28 22:17–22:23.

---

## Summary

| Page | Verdict | Use it for |
|---|---|---|
| `/bots` | **Strong** — 35/35 bots, 18 fields each, fixed schema | Nightly per-bot drift diff |
| `/positions/analyze` | **Weak** — scalars only, every chart lost | Nothing. Use `Export Data`. |
| Day drill-down modal | **Strong but anonymous** — 27/27 rows, no bot ID | Intraday sequence forensics, single-bot-filtered only |

---

## 1. `/bots` — the bot list

All **35 of 35** bots captured. Value runs are **perfectly consistent at 18 fields per bot**, verified across bots with full data (Tasty Condor), partial data (Nigiri-Paper-v1), and zero data (DIR-SPX-PutVIX22-SL75, which emits 8 dashes then `$10K` then 9 dashes). Parses with a fixed schema, no heuristics:

```
name, TOTAL_PL, RETURN_PCT, CLOSED_PL, CLOSED_PCT, CHANGE, CHANGE_PCT,
POS, RISK, ALLOCATION, WIN_RATE, BETA_WEIGHT, BETA_EXPOSURE,
AVG_PL, AVG_WIN, AVG_LOSS, P_FACTOR, STREAK, CLOSED
```

The header row lists 23 columns. Three never emit text (`30D` sparkline, `AUTOS`, `EXITS`) and `ICON` is decorative — so the capture yields 18 of 21 real data columns, **86%**, deterministically.

### What is lost

| Lost | Consequence |
|---|---|
| `AUTOS` / `EXITS` counts | **Highest-value miss.** This is the column that would have flagged `QQQ-IC-0DTE-HedgeC-S3` having zero monitors. |
| ON/OFF toggle state | Confirms the known limitation in `approach-reset-2026-07-29.md` §3.4. `DIR-SPX-PutVIX22-SL75` shows all dashes — **the capture cannot resolve Open Question #2** (is that bot switched on?). |
| Live/Paper per bot | Only inferable from the global "Paper Trading" filter chip |
| Bot Group membership | No trace |
| Precision above $10K | `-$11.2K`, `-$31.6K` — rounded to 3 significant figures. A move from -$11,200 to -$11,249 will not diff. Sub-$10K values are exact. |

### Normalisation additions

Beyond the items already listed in `approach-reset-2026-07-29.md` §3.4 (`captured:` line, sidebar clock, `Opportunities N` counter), strip:

- the two-line `Account inactive, no changes will be saved… / See plans` banner
- the footer `35 active bots • 15 left in your plan • Upgrade` — changes on every bot add/delete

### Why this matters

A nightly `/bots` capture is **a drift-detection surface the approach-reset plan does not currently account for**, and it needs no ledger and no OA API. `AVG LOSS`, `P FACTOR`, `WIN RATE` and `CLOSED` per bot, diffed daily, catch a Fortress-style regression directly: when `QQQ-IC-0DTE-Fortress` stopped executing PT50 on 2026-06-12, `AVG LOSS` would have blown out and `P FACTOR` dropped within a day or two. Worth adding to `scripts/execution_audit.py` as a second input alongside the ledger.

---

## 2. `/positions/analyze` — the Analyze page

Scalars survive. **Every chart dies.**

Captured cleanly: the four KPI tiles, the Metrics block (1,386 positions, Sharpe -2.32, Sortino -1.37), all eight Averages, and the Range label.

Lost entirely — `Closed P/L`, `Day of Week`, `Hour of Day`, `By Strategy`, `By Symbol` come through as bare headings with zero data. From the matching screenshot that silently discards:

- **By Symbol:** QQQ -$74,030 · SPX ~-$8K · SPY +$2,025
- **By Strategy:** Short Put Spread -$43,775 · Iron Condor ~-$30K
- **Hour of Day:** 11AM -$54.5K · 1PM ~-$40K — the entry-time signal for the 11am-vs-1:30 A/B

### Two additional defects

**Filter state is not captured.** The page carries eight filter dropdowns (Symbols, Tags, Strategy, DTE, Bot, Bot Group, Day, Hour); the text got only `Tags` and `Strategy`. The file therefore records numbers without recording what produced them. Numbers whose scope cannot be reconstructed are exactly the failure class this project is trying to eliminate.

**A hover tooltip leaks in.** A chart tooltip that happened to be in the DOM at capture time appears as a trailing block. Non-deterministic — strip it or it generates false diffs.

**Verdict: do not use the bookmarklet here.** The page has an `Export Data` button (up to 10,000 positions). That is the correct instrument for anything chart-shaped.

---

## 3. Day drill-down modal (click a bar in Closed P/L)

Best granular capture of the three, with one fatal gap.

All **27 of 27** positions captured, 6 of 7 columns: DESCRIPTION (symbol + strategy), LEGS, DURATION, STATUS, P/L, ROR. Row order preserved (sorted by DURATION ascending).

Record shape is variable-length but deterministically parseable — leg count implied by strategy name (`Short X Spread` -> 4 tokens, `Iron Condor` -> 8), and DURATION is always exactly 2 lines whether single-day or multi-day:

```
symbol, strategy, [strike,type x 2 or 4], date_range, time_range, status, pl, ror
```

**Spread width is recoverable** because strike and type come through as separate tokens: SPX 7330P/7325P = $5 wide, QQQ 698/696 = $2 wide, and the -$9,234 Iron Condor is 705/704 + 695/694, a **$1-wide** QQQ IC at -93.1%. This means Pattern C's exit-price clustering test can partly run off this capture.

### The fatal gap: the BOT column is an icon

The BOT column renders a coloured avatar per bot. It emits **zero text**. What appears in the .txt as `SPX` / `QQQ` / `SPY` is the DESCRIPTION cell's first line, not the bot.

On 2026-05-12, six QQQ short put spreads all opened at 11:01am at identical strikes 698/696. **Which bot is which cannot be determined from the file.** Sitting in that capture, unattributable:

| Signature | Evidence in the capture | Doc reference |
|---|---|---|
| Tournament arms entering in lockstep | 6 QQQ SPS + 6 QQQ SCS, all `11:01am`, all 698/696 and 710/708 | "11:01 x 45/45" |
| **Duplicate arms** | `-$1,674` twice (both 11:01->12:42); `$243` four times (all 11:01->11:22) | HedgeA-S1 ≈ HedgeD, identical P/L 73/86 |
| **Re-entry churn** | SPX closes 9:49 -> opens 9:49; closes 9:55 -> opens 9:55; closes 9:58 -> opens 9:58 | The 7/01 orphan loop |

Every one of those is a finding the execution audit spent hours establishing, visible at a glance — and none of it can be pinned to a bot from this file.

### Two smaller notes

**The tooltip reconciles.** `14 wins, 12 losses` against `27 positions` — the missing one is a SPY Short Put Spread with `--` for both P/L and ROR. Neither win nor loss. Not a bug; an unpriced position.

**Time resolution is minutes, not seconds.** The orphan-loop fingerprint in the audit ("every close followed by an open one second later") came from order-level Trade Log data. Here a 1-second and a 45-second re-entry both render as the same minute. Same-minute close->open is still a strong detector; the ability to distinguish a race from a fast legitimate re-entry is lost.

---

## 4. Recommended next check (10 minutes, not yet done)

Click `Export Data` on `/positions/analyze` and inspect the CSV header row for a **bot name column**. If present, the bookmarklet stops being the primary instrument for position data and becomes the fast visual check, because every signature in §3 becomes computable rather than merely visible.

Until then, attribution requires filtering to one bot before capturing — and since filter state is not captured either, the bot name has to be recorded out-of-band in the filename.
