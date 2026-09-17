# DERIVED — can the OA backtester express a SECOND, separate protective position?

# Source of every field below: `01-backtest-settings-form-2026-09-16-223758.txt`
# (sha256 02376a44a3b60afdaf069974ae50292f4cdc93e2bfe10003413ae6fcfebe9973) —
# the New Backtest "Backtest Settings" drawer captured 2026-09-16 22:37:58 ET with
# all 7 sections expanded, plus per-menu verbatim lists read from the live UI in
# the same session. Nothing here is typed from memory.
# Screenshots: `screenshots/` (one per section + the Entry Filters "More" drawer
# + the OA Portfolio tab).

## The question (Phase 0, dispatch-oa-capture-2026-09-16)

> Can OA's backtester express a SECOND, separate protective position — one opened
> after the primary position is already on — or is it single-structure only?

Under `R-2026-09-16-HEDGE-DEFINITION` a hedge is a separate protective position;
an exit strategy is not a hedge.

## Answer: NO

Single-structure only. Every control on the surface configures the ONE primary
position (its structure, when it opens, when it closes). No control adds a second
structure/leg-group/position distinct from the primary, and no control opens any
position conditionally mid-trade.

## Control-by-control basis (verbatim labels)

| Section | Controls (verbatim) | Second position? | Conditional mid-trade open? |
|---|---|---|---|
| Position Details | `Symbol` pills (SPX SPY QQQ XSP IWM GLD TLT) · `Expiration` "exactly 0 days" · `Strategy` mpick: **Long Call / Long Call Spread / Short Call Spread / Long Put / Long Put Spread / Short Put Spread / Iron Condor / Iron Butterfly** · leg pickers `Long put`/`Short put` "Select..." | No — strategy fixes ONE structure's legs; no add-structure control exists | No |
| Capital | `Allocation` "Max total capital to open positions" · `Position Size` "1 contract" | No — sizing of the one structure | No |
| Position Entry | `Entry Trigger` checkboxes "Time of day" / "Opening range breakout" · `Entry Time` · `Trading Days` "Mon-Fri" · `Skip Events` "None" · `Position Limit` mpick: **1 position … 10 positions** · "At least N market day from last opened position" · "Include slippage from the mid price on opening trades" | No — Position Limit 1–10 repeats the SAME structure; there is no second-structure config anywhere for it to bind to | No — triggers gate the primary's open only |
| Position Criteria (optional) | "Mid price between _ - _" · "Reward/risk ratio is _% or more" · "Bid/ask spread is $_ or less" · "Only 1 position open in an expiration at a time" | No — filters on the primary entry | No |
| Entry Filters (optional) | Menus: `Ranges` (VIX, VIX Change, VIX Change %, IV Rank, Change %, Change SD, Gap %, Open Chg %) · `Indicators` (ADX(14), CCI(20), CMO(9), MACD(12,26,9), Momentum(10), RSI(14), Stoch(14,3,3), Stoch RSI(14,14,3,3)) · `Moving averages` (SMA/EMA 10-200) · `More ...` drawer: Stocks + Gamma Exposure templates (full list in raw file) | No — every template predicates on the UNDERLYING/market; none reference an existing position's state | No |
| Exit Options (optional) | `Profit Taking %` · `Profit Taking $` · `Stop Loss %` · `Stop Loss $` · `Expiration` · `Avoid Events` · `Touch` · "Include slippage … on closing trades" · "Automatically detect and ignore unrealistic exit prices" (checked) | No — all are exits: they CLOSE the position. An exit is not a hedge (ruling above) | No |
| Backtest Options (optional) | `Test Period` (1 year / 2 years / 3 years / 5 years / Custom) · `Description` · `Excluded Dates` | No | No |

## Other surfaces checked

- **`OA Portfolio` tab** (`/backtests/portfolio`): published backtest library
  ("Flat Fly", "1:45pm Sandwich", "Afternoon Paycheck", …). Each variant row is
  still one single-structure backtest.
- **`Compare`** (`/backtests/compare/<ids>`): aggregates equity curves of
  independent single-structure backtests ("Combine Results"). It combines
  *results*, not positions inside one test.
- The form's only action buttons are `Run Backtest` and the drawer ✕ (discard).
  No "add position", "add structure", "add leg group", or second-entry block
  exists anywhere in the serialized form (51 inputs, all listed in the raw file).

## Corollary for Phase 1

The conditional-hedge arms (H-A, H-B) are not expressible here. H-0 (ride to
settlement) and H-C (Stop Loss % = SL100/SL200) are expressible — they are
exit/single-structure configurations.
