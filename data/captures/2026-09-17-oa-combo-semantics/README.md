# Phase 0c — OA backtest Combo Rules semantics

**Purpose:** resolve four unknowns left by Phase 0b's discovery of `Combo Rules`:
1. Does `Only open [overlay] if [primary] is open` gate on **concurrent presence** (primary open
   at the overlay's entry moment) or **day-level presence** (primary opened at any point that day)?
2. Does a populated `crules` JSON round-trip through a hand-constructed URL?
3. Is the combined positions export a **census** of both tests or a **filtered result**?
4. What do `Daily Positions`/`Position Limit` default to across pass sizes, are they editable,
   and do they change the combined result?

**Captured:** 2026-09-17 ~00:05–00:45 America/New_York (UTC-4; UI clock 12:xxAM).
Host `app.optionalpha.com`, PAPER verified on `/home`. No `/login`, no 401/403/429,
no payment/terms prompt, no non-PAPER indication. CDP attach; DOM reads + trusted input only.

**Fixture (agent-created, run-authorized):**
| name | id | entry | structure |
|---|---|---|---|
| ZZ-AGENT-2026-09-17-primary | ZT41789618576434486115 | 09:35 | QQQ 0DTE short put spread, 1ct, PT 2.5% |
| ZZ-AGENT-2026-09-17-overlay | ZT41789619101486375116 | 15:00 | identical |

**Rendered test period:** Sep 2025 → Sep 2026 (1y; Monthly P/L shows partial Septembers at both ends).
Each test: 249 positions.

## Answers (evidence in `02-…md`, raw verbatim in `01-…txt`)

1. **`open` = CONCURRENT.** On all 240 days the primary closed before 15:00, the `is open` run
   admits **zero** overlay rows; the `is not open` run admits all 240. Disjoint, exhaustive,
   mirrored. The gate evaluates live presence at 15:00, not "traded today."
2. **`crules` round-trips: YES.** Populated rules array re-renders in the drawer from a hand-built
   URL and the combined view honors it. Two rules accepted in array order (`rule0`,`rule1`).
   Malformed rules/JSON silently ignored (unruled fallback, no error). Caveat: drawer form state
   is SPA-sticky and can disagree with the URL — the URL is the record of what ran.
3. **Combined export = RESULT, not census.** Control run: 497 rows vs 498 standalone position-rows —
   the overlay's Nov 3, 2025 row was dropped by combine caps despite nominal headroom. Rule runs
   filter further (257 / 489). Diff combined exports against standalone exports before assuming
   coverage.
4. **Caps default to exactly N and change the result.** `2/2` at two tests, `4/4` at four, `7/7`
   at seven — editable, `1–10` both pickers. `posLimitDay=1` on the same pair → 249 rows (overlay
   entirely gated out); `posLimit=1` → 489 rows, dropping exactly the open-at-15:00 days (B-day
   set identical to the `is not open` run — the cap evaluates concurrent presence too).
   **Combined results are not comparable across pass sizes under default caps** — pin `crules`
   caps explicitly or hold test count fixed. Compare columns A…G impose no shared caps.

## Files

| file | sha256 (first 16) | what |
|---|---|---|
| `01-combo-semantics-2026-09-17-0030.txt` | `a24c99275a984e8b` | raw capture: verbatim form values, drawer text, URLs, stats, run outputs |
| `02-combo-semantics-answers-2026-09-17.md` | *(see SHA256SUMS)* | derived answers + partition analysis + docs-vs-render deltas |
| `standalone-primary-249.csv` | `b234578248266f7a` | primary positions export (Copy CSV) |
| `standalone-overlay-249.csv` | `157deb2df4071cae` | overlay positions export |
| `combined-control-497.csv` | `aeeb327e300afe9f` | combined export, no rule (A=249,B=248) |
| `combined-open-257.csv` | `e390d47d8bc9463f` | combined export, `Only open B if A is open` (A=249,B=8) |
| `combined-notopen-489.csv` | `01af5d4bb645a6c8` | combined export, `Only open B if A is not open` (A=249,B=240) |
| `combined-cap-day1-249.csv` | *(see SHA256SUMS)* | combined export, `posLimitDay=1` cap — A only, overlay fully gated |
| `combined-cap-pos1-489.csv` | *(see SHA256SUMS)* | combined export, `posLimit=1` cap — B-day set identical to `is not open` run |
| `screenshots/01-primary-config.png` | | primary form pre-run |
| `screenshots/02-primary-running.png` | | `Backtest running.` state verbatim |
| `screenshots/03-overlay-config.png` | | overlay form pre-run |
| `screenshots/04-combined-open-rule-view.png` | | combined view honoring open-rule (257) |
| `screenshots/05-combo-rule-drawer-open.png` | | drawer with `Only open Test B if Test A is open` |
| `screenshots/06-combo-rule-drawer-first-add.png` | | drawer after first addRule (state pickers visible) |
| `screenshots/07-backtest-running-state.png` | | running-state duplicate of 02 (kept: capture of the verbatim state) |
| `SHA256SUMS.txt` | | hashes over everything above |

## Refusals

- `Create Bot` — offered on single-test and combined views; never clicked (live-fleet surface).
- `Save` (compare/combined bar) — saving a comparison prohibited; declined.
- `Download CSV` — declined throughout; `Copy CSV`+`pbpaste` used so bytes land only in the bundle.
- `Rerun Backtests`, `Delete Test`, `Replace Variation`, `Edit Description` — write actions outside
  the two authorized builds; declined.
- No `git` mutations; `git restore` was used once to repair 8 screenshot files in the verified
  0a bundle that `/tmp/oa_shots.mjs` overwrote when invoked as a generic screenshot tool
  (lesson recorded in `data/lessons.csv`).
- Wire protocol never touched: no fetch/XHR, no `POST /api/request`, no `zdte.*`, no network reads.
- Stop conditions never triggered.

## Docs-vs-render deltas

See `02-…md` §Docs-vs-render deltas — OA-1090 (4-vs-7 cap, re-confirmed), OA-1076/1077/1091
(aggregation-only docs vs rendered conditionality), `AI Agent Stack.md`:256 exportability.
