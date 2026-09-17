# Capture bundle — 2026-09-16 OA backtester surface reconnaissance

Purpose: **Phase 0 of `docs/dispatch-oa-capture-2026-09-16.md`** — answer, by
looking at the UI: *can OA's backtester express a SECOND, separate protective
position opened after the primary is already on, or is it single-structure only?*
Read-only UI capture over CDP against Andy's authenticated Chrome (paper
account). No edits, no saves, no backtest runs.

Captured **2026-09-16 22:37:58-04:00** (ET).

## Files

| file | sha256 | what it is |
|---|---|---|
| `01-backtest-settings-form-2026-09-16-223758.txt` | `02376a44a3b60afdaf069974ae50292f4cdc93e2bfe10003413ae6fcfebe9973` | RAW capture, unmodified. New Backtest "Backtest Settings" drawer, all 7 sections expanded: rendered innerText + all 51 serialized form inputs + verbatim menu option lists (Strategy, Position Limit, Entry Filters submenus, More-drawer templates, OA Portfolio tab notes). |
| `02-second-position-expressivity-2026-09-16.md` | `123da5a08846dc1538716ec195ba983dc0439d2d594695212450d7224075ac8b` | DERIVED. Control-by-control expressivity table answering the Phase 0 question; header names the raw file + sha as the source of every field. |
| `screenshots/` | per file in `SHA256SUMS.txt` | One PNG per configuration section + Entry Filters "More" drawer + OA Portfolio tab + the Run Backtest footer. |

## Findings

- **Answer: NO.** The New Backtest surface is single-structure. No control adds a
  second structure/leg-group/position distinct from the primary; no control opens
  a position conditionally mid-trade.
- Strategy picker is exactly 8 single structures, verbatim:
  `Long Call · Long Call Spread · Short Call Spread · Long Put · Long Put Spread ·
  Short Put Spread · Iron Condor · Iron Butterfly` — no custom/multi option.
- `Position Limit` offers `1 position` through `10 positions` — repeat entries of
  the SAME structure only; Position Criteria adds verbatim
  `Only 1 position open in an expiration at a time`.
- Entry-side conditionality exists but predicates only on the underlying/market:
  verbatim menus `Ranges` (VIX, IV Rank, Gap % …), `Indicators` (ADX, MACD, RSI …),
  `Moving averages` (SMA/EMA 10–200), `More ...` drawer (`Stocks`, `Gamma Exposure`
  templates). None reference an existing position's state.
- Everything post-entry is an exit (`Profit Taking %/$`, `Stop Loss %/$`,
  `Expiration`, `Avoid Events`, `Touch`) — closes the position, never opens one.
  Under `R-2026-09-16-HEDGE-DEFINITION` none of these is a hedge.
- `OA Portfolio` tab is a published-backtest library; `Compare`
  (`/backtests/compare/<ids>`) aggregates independent single-structure results —
  it combines results, not positions inside one test.

Verbatim labels relied on (drawer + controls), quoted from the raw file:
`Backtest Settings` · `Position Details` · `Strategy` · `Position Limit` ·
`Only 1 position open in an expiration at a time` · `Entry Filters(optional)` ·
`Exit Options(optional)` · `Run Backtest`.

Cross-check path: none within OA (single surface). Corroborating doc context:
`docs/oa-platform-reference.md` (platform expressivity limits) and the dispatch's
Phase-1 branch for a NO answer.

## Boundary notes (per dispatch "REPORT")

- Read-only throughout: no fields set, no backtest run, nothing saved. The editor
  was opened, read, and closed with its ✕ (discard).
- Menus were opened to enumerate options and closed without selecting; the
  `strategy` hidden input read `shortputspread` before and after.
- Stop conditions never triggered: no `/login`, no 401/403/429, no live-account
  indicator (paper account per Andy, confirmed in-session).
