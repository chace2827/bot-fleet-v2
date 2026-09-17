# Phase 0c — derived answers: what `open` MEANS

Derived from raw capture `01-combo-semantics-2026-09-17-0030.txt`
(sha256 `092135f7f677c0aaaa42f1420652311fbff091e87befd4d33934d076c73f0d4f`)
and the five exported CSVs (sha256s in SHA256SUMS.txt). All analysis below is computed
from the exported CSVs, not from charts. Test period as rendered by OA: **Sep 2025 → Sep 2026**
(1y; partial Septembers at both ends — Monthly P/L verbatim in raw §2).

Fixture: two identical QQQ 0DTE short put spreads, 1 contract, PT 2.5% of credit —
- PRIMARY `ZT41789618576434486115` entry 09:35 → 249 positions; 240 closed before 15:00, 9 still open at 15:00.
- OVERLAY `ZT41789619101486375116` entry 15:00 → 249 positions.

## ANSWER 1 — `open` is CONCURRENT (presence at the gated test's entry moment), NOT day-level

Partition (standalone CSVs):

| primary day-class | days |
|---|---|
| closed before 15:00 | 240 |
| still open at 15:00 | 9 |
| total | 249 |

Combined-run B-rows (overlay positions admitted), matched by day:

| run | rule | B-rows | B-days ⊆ before-15:00? | B-days ⊆ open-at-15:00? |
|---|---|---|---|---|
| control | none | 248 | 240 of them | 8 of them |
| (b) | `Only open B if A is open` | **8** | **0** | 8 (of 9) |
| (c) | `Only open B if A is not open` | **240** | 240 (all) | **0** |

- On the **240 days the primary closed before 15:00**, run (b) contains **ZERO** overlay rows.
  If `open` meant "primary opened at any point that day," all ~248 would be present. It does not.
- On the **9 days the primary was still open at 15:00**, run (b) admits 8 overlay rows
  (the 9th, Nov 3 2025, is cap-dropped in all three runs — see Answer 3).
- Run (c) is the exact mirror: B-days ∩ B-days(b) = ∅; B-days(b) ∪ B-days(c) = control B-days exactly.
  `open` and `not open` partition the sample with no overlap and no residue — the predicate is
  evaluated at the gated test's entry moment (15:00), against the predicate test's live presence.

**VERDICT: CONCURRENT.** `Only open [overlay] if [primary] is open` = "the primary holds a live
position at the moment the overlay would enter." It is a presence gate, closer to H-B (fixed-time
overlay, conditioned to fire only when the primary is actually on), NOT H-A (loss-conditioned).
It is not a hedge trigger and does not read P/L.

Sample: 240 vs 9 day partition — well above the NOT-DETERMINABLE threshold.

## ANSWER 2 — `crules` round-trips through a hand-constructed URL: YES

- Populated rule travels as URL JSON verbatim:
  `rules:[{"type":"state","test1":"<id>","test2":"<id>","state":"open","text":"Only open Test B if Test A is open"}]`
- Hand-constructed URL → combined view honors it (Count=257, identical to drawer-built run) AND
  the Combine Results drawer re-renders the rule row verbatim with `rule0-test1/test2/state` populated.
- Two rules: accepted; array order → `rule0`, `rule1` rendered top-down in that order; both applied.
- Malformed input: `[{"bogus":1,"foo":"bar"}]` and outright invalid JSON both produce **no error**;
  the combine silently falls back to unruled behavior (Count=497 = control).
- ⚠️ Drawer is not a reliable URL mirror: under the malformed-rule URL the drawer still displayed
  the prior session's rule; under a bare URL the `Combine Results` toggle stayed checked while no
  `=` column rendered. URL state and SPA form state can diverge — read the URL for what ran,
  not the drawer.

## ANSWER 3 — combined positions export is a RESULT, not a census: CONFIRMED

- Standalone counts: 249 + 249 = 498 position-rows exist across the two tests.
- Control combined export (no rules): **497 rows** — the overlay's `Nov 3, 2025 3:00pm` row is
  absent even though `posLimitDay=2`/`posLimit=2` nominally allow it. One row was dropped by the
  combine's own caps/ordering.
- Rule runs filter further by design: 257 (open) and 489 (not open).
- Consequence: the combined positions CSV reflects what the combine *simulated*, not the union of
  the two tests' standalone positions. Any downstream analysis must treat it as a result set
  with rows possibly missing — diff against standalone exports before assuming coverage.

## ANSWER 4 — caps default to exactly N; they are editable 1–10; and they change the result — CONFIRMED, the capital frame is not comparable across pass sizes

**(a) Defaults = exactly N.** Verbatim at first drawer open: 2 tests → `2 per day`/`2 positions`;
4 tests → `4 per day`/`4 positions`; 7 tests → `7 per day`/`7 positions` (0b observation,
unchanged). Scaling is exactly N at every pass size observed.

**(b) Editable: YES.** `Daily Positions` offers `1 per day` … `10 per day`; `Position Limit`
offers `1 position` … `10 positions` (verbatim in raw §8b). Values persist in the drawer across
toggle off/on.

**(c) Caps change the result — same pair, two settings:**

| run | caps | combined rows | vs control (497) |
|---|---|---|---|
| D1 | `posLimitDay=1, posLimit=2` | **249 — all Test A** | all 248 overlay rows absent (the 15:00 open is always the day's second open) |
| D2 | `posLimit=1, posLimitDay=2` | **489 — A249 + B240** | 8 overlay rows absent — exactly the open-at-15:00 days |

Positions present in one run and absent in the other: **yes** — D1 drops every overlay row,
D2 drops exactly the 9-day open15 set. And the D2 B-day set is **identical** to the
`is not open` rule run's: the concurrent-position cap evaluates live presence the same way
the rule does, independently corroborating Answer 1.

**The concern is confirmed:** a 7-way combine runs under `7/day + 7 concurrent` while a 2-way
runs under `2/day + 2 concurrent` — different capital frames by default. Combined results are
**not comparable across pass sizes under default caps.** The arm grid must either pin both
caps explicitly (they travel in `crules` — addressable, see Answer 2) or hold test count fixed.

**Compare is unaffected:** per-test columns A…G render standalone Counts under every `crules`
variant — caps live only in the Combine Results drawer and the `=` column. No evidence Compare
imposes shared caps.

## Docs-vs-render deltas

Checked `data/oa_facts.csv` backtest rows against this surface:

- **OA-1090** — doc: "compare up to four backtests simultaneously." Rendered (Phase 0b, this session
  unchanged): `FOR UP TO 7 BACKTESTS:` — 7-way compare+combine verified. Delta stands (re-confirmed).
- **OA-1091 / OA-1076 / OA-1077** — docs describe combining only as result aggregation
  ("single portfolio P/L curve"). Rendered: cross-test entry gating exists (`Combo Rules`,
  presence predicate `open`/`not open`, evaluated concurrently). The docs' silence on
  conditionality is itself the delta — no doc mentions it.
- **`docs/AI Agent Stack.md`:256** ("backtest data is not exportable") — falsified at position level
  in 0b; re-confirmed here: every positions drawer exports via `Copy CSV`/`Download CSV`,
  including the combined view (Test column present in combined exports only).
- No doc covers `open` semantics — the CONCURRENT finding is first-hand only.
