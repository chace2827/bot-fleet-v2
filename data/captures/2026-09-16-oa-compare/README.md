# Capture bundle — 2026-09-16 OA Compare & Combine surface reconnaissance

Purpose: **Phase 0b of `docs/dispatch-oa-capture-2026-09-16.md`** — answer, by
looking at the live UI, what two backtests do together on
`/backtests/compare/<ids>`: procedure, granularity, conditionality, size ratio,
duplicate fidelity, ceiling. Read-mostly CDP/UI session against Andy's
authenticated Chrome (paper account). No backtest run, no save, no live-fleet
surface touched.

Captured **2026-09-16 ~23:40–23:55-04:00** (ET).

## Files

| file | sha256 | what it is |
|---|---|---|
| `01-compare-combine-surface-2026-09-16-2355.txt` | see `SHA256SUMS.txt` | RAW capture, unmodified. All rendered surfaces in order: list-page compare cells + selection menu (2/7/8-selected states incl. disabled items), compare view innerText, Combine Results drawer + serialized inputs, a Combo Rule row's verbatim structure, combined view innerText + `=` column, Combined Monthly P/L table, 126-positions drawer, Add Backtest / Edit Settings / Add Variation drawers, 7-way compare+combine, and the not-exercised list. |
| `02-compare-combine-answers-2026-09-16.md` | see `SHA256SUMS.txt` | DERIVED. The six answers + export finding, each with verbatim-label evidence; header names the raw sources. |
| `03-combined-positions-copycsv-2026-09-16-2347.csv` | see `SHA256SUMS.txt` | RAW OA export, unmodified. Clipboard content produced by the positions drawer's own `Copy CSV` button on the 126-position combined list. 126 data rows (63 A + 63 B), 24 columns; P/L sums to -18 = the combined `=` column's `-$18`. |
| `screenshots/` | per file in `SHA256SUMS.txt` | 16 PNGs named by section (see below). |

## The six answers

1. **Procedure — YES, captured.** List path: row `cell.compare` check cells →
   `2 backtests selected` → menu `Compare` → `/backtests/compare/<id1>,<id2>`.
   In-compare path: `+ Add Backtest` (new-build drawer) or card ⋮ `Add Variation`/
   `Replace Variation`, Stats `+` column. Combine invoked by `Combine Results`
   toggle → drawer (`Daily Positions`, `Position Limit`, `Combo Rules`) →
   `View Results` → `Combine Backtests` with `?crules=…&combine=1` in the URL.
   Evidence: `01-…txt` §1–§3, §5; `screenshots/01,02,03,04,05,06`.
2. **Granularity — YES, per-day rows.** Positions drawer (`126 positions`,
   headers `TEST | DESCRIPTION | LEGS | DATE | STATUS | RISK | P/L`, `Load more`)
   gives per-position rows for the combined portfolio with a test-of-origin
   column; every Stats `Count`/`Exits`/monthly/`N positions` cell opens it
   filtered. Aggregate granularity bottoms out at `Combined Monthly P/L`
   (`MONTH | P/L | TRADES | WIN RATE | AVG ROR | AVG P/L | AVG RISK | BEST |
   WORST`). Evidence: `01-…txt` §6–§7; `03-…csv`; `screenshots/07*,08*`.
3. **Conditionality — NOT purely additive.** `Combo Rules` renders
   `Only open [Test B ▾] if [Test A ▾] is [open ▾]` — a cross-test entry gate.
   Vocabulary is exactly open/not-open (no P/L, delta, or time predicates);
   whether `open` gates intraday or across days is NOT DETERMINABLE without
   running a combine (prohibited). Evidence: `01-…txt` §4; `screenshots/05`.
4. **Size ratio — NO.** No relative-sizing control on any surface; each test
   keeps its own `Position Size`. Combine-level controls are caps only
   (`Daily Positions`, `Position Limit`, 1–10 pickers). Evidence: `01-…txt`
   §3, §5, §9; `screenshots/05,11`.
5. **Duplicate fidelity — YES.** `Add Variation` pre-fills all 51 serialized
   inputs identically to the parent — name, dates, leg JSON, slippage included;
   only the differ changes. Persists via `Run Backtest` (not run).
   Evidence: `01-…txt` §8; `screenshots/09`.
6. **Ceiling — 7, not 4.** Menu header verbatim `FOR UP TO 7 BACKTESTS:`; 5th–7th
   select fine, 7-way compare+combine renders (Stats `A B C D E F G =`);
   an 8th selection greys `Compare`/`Rerun Backtests` (`mi disabled` — the
   disabled item is the refusal, no error text). Cap binds at the shared
   selection menu — same for Compare and Combine. Evidence: `01-…txt` §1, §9;
   `screenshots/12,13,10`.

## Export finding

`Copy CSV` and `Download CSV` controls render on every positions drawer
(combined, per-test, and every filtered variant). `Copy CSV` exercised once —
real CSV captured (`03-…csv`), internally consistent with the rendered stats.
`Download CSV` declined (writes outside the bundle). No export control exists on
the Stats table, equity chart, or Monthly P/L panel — export is position-level.
The `docs/AI Agent Stack.md`:256 "not exportable" expectation is **falsified for
position-level data**. Evidence: `01-…txt` §7, §10; `screenshots/08*`;
`03-…csv`.

## Docs-vs-render deltas

| fact ID | verbatim doc quote | verbatim rendered label | evidence |
|---|---|---|---|
| OA-1089 | "Traders can use a test period of up to three years," | `Test Period` options `1 year · 2 years · 3 years · 5 years · Custom` | sibling bundle `2026-09-16-oa-backtester/01-…txt` L77-82 (sha 02376a44…); today's serialized `period="custom"` + `startDate`/`endDate` inputs (`01-…txt` §8) |
| OA-1090 | "and compare up to four backtests simultaneously," | `FOR UP TO 7 BACKTESTS:`; 7-way renders; 8th disables `Compare`/`Rerun Backtests` | `screenshots/12,13,10`; `01-…txt` §1, §9 — **falsified** |
| OA-1141/OA-1142 | `{% embed url=" " %}` (the docs page for compare/combine is an empty embed) | a full working procedure exists on the surface (§1) | `screenshots/01,02` — docs gap confirmed, not a contradiction |
| OA-1077/OA-1091 | "combine the results of multiple strategies into one portfolio curve" | `=` column + combined curve render exactly this; **additionally** `Combo Rules` renders, which docs never mention | `screenshots/05,06` — docs agree but are incomplete |
| OA-1079 | "Every backtest includes detailed trade logs…" | holds for the *combined* view too: `126 positions` drawer, `TEST` column | `screenshots/08*`; `03-…csv` — agreed |
| OA-1109 | "View all filtered not included in the backtest…" | `Filtered` stat row renders in compare/combined Stats (`-`/`2`/`455` at 7-way) | `01-…txt` §5, §9 — agreed |

## Boundary notes (per dispatch "REPORT")

- Read-mostly: navigated, clicked, opened drawers/menus, toggled `Combine
  Results`, added+deleted one probe Combo Rule (deleted before `View Results`;
  serialized URL shows `"rules":[]`), exercised `Copy CSV` once. **No** backtest
  run, save, rename, delete, create-bot, or saved comparison.
- `Save` on the compare bar and `Create Bot` were never clicked — saving a
  comparison was prohibited; Create Bot is a live-fleet surface.
- `Download CSV` declined — Copy CSV already proved export; a browser download
  writes outside the bundle dir.
- Stop conditions never triggered: no `/login`, no 401/403/429, no terms or
  payment prompt, no live-account indicator (PAPER verified verbatim on `/home`).
- One incidental note: the "Combine Results" checkbox state was left ON for the
  2-test comparison URL in the tab at close; nothing was saved — URL state only.
