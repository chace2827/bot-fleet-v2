# Compare & Combine — the six answers (DERIVED)

Source: `01-compare-combine-surface-2026-09-16-2355.txt` (raw,
sha256 `00c9dd4b5aaa1ef6a655a466fedd5fdd5756195ae852931f4c403b5462c3626d`)
plus `03-combined-positions-copycsv-2026-09-16-2347.csv` (raw Copy CSV output,
sha256 `6aeac96d9e6bcc6eebb9021050d6ace8c13db491fa30b271a0be6ab93acdaea4`) and
`screenshots/` — every label below is verbatim rendered text from the live surface.
Captured 2026-09-16 ~23:4x–23:5x ET, paper account, read-mostly.

| # | Question | Answer |
|---|---|---|
| 1 | Procedure | YES — documented below, both paths |
| 2 | Granularity | YES — per-position per-day rows exist for the combined portfolio |
| 3 | Conditionality | NOT purely additive — `Combo Rules` gates one test's opens on another's state |
| 4 | Size ratio | NO — no relative-sizing control anywhere on the surface |
| 5 | Duplicate fidelity | YES — `Add Variation` pre-fills all 51 serialized inputs identically |
| 6 | Ceiling | 7, not 4 — `OA-1090` falsified by the live surface |

---

## 1. Procedure — YES

**Adding backtests to a comparison.** Two paths observed:

- **List page:** `/backtests` grid rows each carry a `div.cell.compare` cell with
  `<a class="cmpcheck" data-click="onCheck" data-id="<testid>">`. Clicking two rows'
  check cells renders **`2 backtests selected`** (a.btn.gray.selbtn) in the header bar.
  Clicking it opens a menu verbatim:
  `Clear Selections · Delete Backtests · FOR UP TO 7 BACKTESTS: · Compare · Rerun Backtests`.
  `Compare` navigates to `/backtests/compare/<id1>,<id2>` (comma-separated ids).
  Evidence: `01-…txt` §1, `screenshots/01-list-compare-cells-2-selected.png`,
  `02-selected-menu-compare.png`.
- **Inside a comparison:** `+ Add Backtest` (a.btn.gray, top-right) opens the
  `Backtest Settings` drawer — a NEW backtest builder, not a picker of existing tests.
  Its only action button is `Run Backtest`. Also: each Settings card's ⋮ menu carries
  `Add Variation` / `Replace Variation`, and the Stats table has a `+` column.
  Evidence: `01-…txt` §2, §8, `screenshots/09-add-backtest-editor.png`,
  `04-card-ellipsis-menu.png`.

**Invoking `Combine Results`.** A verbatim `Combine Results` toggle (a.btn.gray.sm.trans)
sits at the top-right of the Results panel. Activating it opens a right-side drawer
verbatim `Combine Results` containing `Daily Positions`, `Position Limit`, `Combo Rules`,
and a green `View Results` button. `View Results` re-renders the page as
`Combine Backtests` with the combine config serialized into the URL
(`?crules={"posLimit":2,"posLimitDay":2,"rules":[]}&combine=1`).
Evidence: `01-…txt` §3, §5, `screenshots/05-combo-rule.png`, `06-combined-view-top.png`.

## 2. Granularity — YES, per-day rows exist

The combined view exposes **per-position rows** — which for these 0DTE tests are
per-day rows — plus a monthly rollup:

- Stats `Count` cells are `<a data-click="showPositions">` links; the `=` column's `126`
  opens a positions drawer titled verbatim **`126 positions`** with headers verbatim
  **`TEST | DESCRIPTION | LEGS | DATE | STATUS | RISK | P/L`** — a `TEST` column
  identifies which backtest each row came from, dates are per-day
  (`Sep 14, 2026 1:30pm → 3:56pm`), and a `Load more` pager covers the tail.
  Evidence: `01-…txt` §7, `screenshots/08-positions-drawer-csv.png`.
- Filtered variants: `Exits` cells (`54`, `48`, `9`, `57`, `15`), monthly rows, and
  Insights `N position(s)` links all open the same drawer pre-filtered.
- The **`Combined Monthly P/L`** section (collapsed by default) renders monthly rows:
  headers verbatim `MONTH | P/L | TRADES | WIN RATE | AVG ROR | AVG P/L | AVG RISK |
  BEST | WORST` — June/July/August/September rows plus a `2026` total row.
  Evidence: `01-…txt` §6, `screenshots/07-combined-monthly.png`,
  `07b-monthly-expanded.png`.
- The `Copy CSV` export (see Export) carries per-day/per-position granularity with
  `Opened`/`Closed` timestamps to the minute.
- No intraday/daily-P/L table exists — the finest *aggregate* granularity is monthly;
  the finest *row* granularity is per position. Day-level P/L is derivable from the
  position rows or the CSV.

## 3. Conditionality — NOT purely additive

`Combo Rules` in the Combine Results drawer is a cross-test entry gate. Clicking `+`
(data-click="addRule") renders a rule row verbatim:

**`Only open [Test B ▾] if [Test A ▾] is [open ▾]  ✕`**

- Picker `rule0-test1`: `Test A · Test B` — the gated test.
- Picker `rule0-test2`: `Test A · Test B` — the condition test.
- Picker `rule0-state`: verbatim options **`open` · `not open`** — the only two states.
- `Only open`, `if`, `is` are fixed literals; `+` allows multiple rules; each row has a
  `✕` (data-click="deleteRule"). No other rule shape exists in the DOM.

So a combined run CAN condition one backtest's entries on another backtest's
position-open state — exactly the hedge trigger shape ("only open the overlay if the
condor is open"). The vocabulary is narrower than a reactive hedge needs — open/not-open
only, no P/L, delta, or time-since-open predicates — but it is **not additive-only**.
Evidence: `01-…txt` §4, `screenshots/05-combo-rule.png`. The probe rule was added, read,
and deleted before `View Results`; the serialized URL shows `"rules":[]`.

Caveat recorded, not tested: whether the rule gates intra-day (B opens only while A's
position is open that day) or inter-day. The vocabulary renders `open`/`not open` only;
the evaluation timing is not stated anywhere on the surface. NOT DETERMINABLE without
running a combine — which was prohibited.

## 4. Size ratio — NO

No control bearing on relative sizing between combined backtests is rendered anywhere:
not in the Combine Results drawer (only `Daily Positions`, `Position Limit`,
`Combo Rules`, `View Results`), not in either card's ⋮ menu, not in the combined card's
menu (`Edit Settings · Create Bot · Remove`), not in the Stats header. Each test keeps
whatever `Position Size` its own backtest config carries (here `1 contract` each); the
combine layer adds only portfolio-level caps (`Daily Positions` — "Max positions opened
in one day."; `Position Limit` — "Max open positions at once.", both `1–10` pickers).
Evidence: `01-…txt` §3, §5, §9, `screenshots/05-combo-rule.png`,
`11-combined-card-menu.png`.

## 5. Duplicate fidelity — YES

Card ⋮ → `Add Variation` opens the `Backtest Settings` drawer with **all 51 serialized
inputs identical to the parent test** — including `name="RPCTEST-TOUCH"` verbatim,
`startDate=2026-06-15`/`endDate=2026-09-15`, the leg JSON payloads
(`longPut {"$2.00 below short put leg"}`, `shortPut {"-.20 delta"}`), `touch {"$0"}`,
and the exit-slippage checkbox (`chxslip` checked, `xslip=0.05`). Field-for-field it
matches the same test's `Edit Settings` dump; only the differ would change. The
variation persists only via `Run Backtest` (not run). Evidence: `01-…txt` §8,
`screenshots/09-add-backtest-editor.png` (same drawer shape).

## 6. Ceiling — 7, not 4

- `OA-1090` claims "up to four backtests simultaneously." The live selection menu's
  section header renders verbatim **`FOR UP TO 7 BACKTESTS:`**.
- A 5th, 6th and 7th selection all keep `Compare` enabled; a 7-id URL renders a
  7-column Stats table (`A B C D E F G`) and a working combined view
  (`= Combined Results / 7 backtests`, combined Total P/L `-$25,651`).
- Selecting an 8th renders `Compare` and `Rerun Backtests` with class
  `mi disabled` — greyed, no error text. The refusal IS the disabled item.
- The cap is applied at the selection menu that feeds both surfaces; a 7-way combine
  rendered without refusal, so the cap binds `Combine Results` the same way
  (no separate combine cap observed).
Evidence: `01-…txt` §1, §9, `screenshots/12-seven-selected-menu.png`,
`13-eight-selected-disabled.png`, `10-seven-way-combined.png`.

## Export — YES, at the positions level

The `docs/AI Agent Stack.md`:256 expectation ("backtest data is not exportable") is
**falsified for position-level data**: the positions drawer carries verbatim
`Copy CSV` and `Download CSV` controls on every positions list — combined (126), per-test,
exit-filtered, month-filtered, insight-filtered. `Copy CSV` was exercised once and
produced a real CSV (see `03-…csv`: 24 columns incl. `Opened`,`Closed`,`Status`,`P/L`,
`Risk`,`ROR`, leg detail, `Test`; 63 A + 63 B; P/L sums to -18 = the combined `=`
column's `-$18`). `Download CSV` was not exercised (would write outside the bundle dir).
No export control was found on the Stats table, equity chart, or Monthly P/L panel —
export exists at the position-row level only. Evidence: `01-…txt` §7, §10,
`screenshots/08-positions-drawer-csv.png`, `03-…csv` itself.

## Docs-vs-render deltas

See README.md `## Docs-vs-render deltas` — OA-1089 (test period), OA-1090 (cap),
OA-1143/1144 (empty docs page — no rendered procedure anywhere to check against).
