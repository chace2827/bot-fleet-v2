# LEAN / QuantConnect Backtesting Reference (Bot Fleet)

> Created 2026-06-23. **Verified patterns** for backtesting SPX 0DTE options strategies in
> QuantConnect/LEAN for Bot Fleet — built from code that *actually ran and was cross-checked against
> OA*, not from web docs (LEAN's API drifts; docs mislead on specifics). Read this before writing any
> LEAN algorithm here. Pipeline context: LEAN sweeps → OA backtester validates structural survivors →
> OA paper is the live gate (`backtest-tooling-roi.md`).

## Calibration protocol (do this before trusting any new sweep)

**Always reproduce a known OA number first.** New engine, new code, my (Claude's) LEAN API knowledge is
~90% — calibration is what closes the last 10%. Confirm the engine matches OA on a known config before
believing any *new* result it produces.

**CALIBRATION LOCKED — 2026-06-24 (v5 Control, full window).**
- Config: SPX 0DTE IC, enter 9:45, shorts 1.5% OTM, $25 wings, 1 qty, hold to settlement, no gap filter
  (= OA Batch 1 Control). Window **2022-05-02 → 2026-06-18** (full).
- Result: **707 ICs, per-condor win rate 92.1%, avg RoR/IC +1.31%, Total Fees $1,699** (Tradier Pro Plus
  $0.60/contract custom model now applying — fees ≠ $0 confirmed).
- **Win-rate match: 92.1% (LEAN) ≈ 92.6% (OA 5Y control) ✓** — engine validated on win rate. Per-condor
  metric is the in-algo one; ignore LEAN's built-in leg-level "Win Rate" (~49%).

**⚠️ Carry these two calibration findings into every LEAN result:**

1. **LEAN RoR runs ~4× HOTTER than OA (+1.31% vs +0.3% RoR/IC) — fill optimism.** LEAN fills at
   mid/market; OA models SmartPricing + 0.03/leg slippage. So: **trust LEAN for win rate + RELATIVE
   rankings only.** Always compare a config to the **LEAN control** (the +1.31% baseline), never read
   LEAN's absolute RoR as live economics. **OA/paper validates absolute economics.** TODO to tighten:
   add a slippage model to LEAN (≈0.03/leg) so the absolute match improves — until then, relative-only.
2. **Quote-filter coverage gap: v5 traded 707 ICs vs OA's ~920 (skips ~24% of days with no clean 9:45
   bid/ask).** **MUST verify this filter doesn't bias toward calmer days before trusting any gap or
   directional result** — if "no clean quote" correlates with fast/volatile opens, every sweep silently
   drops the exact days directional/gap strategies live on. Check: compare the VIX/gap/ATR distribution
   of SKIPPED vs TRADED days; if skipped days skew high-vol, the sample is biased and results understate
   tail risk. (C1 inherits the same filter at 11:00 — `c1_regime.py` now skip-logs days for exactly this
   check; see C1 build note in `current-state.md`.)

**Earlier 1yr run (2026-06-23), superseded by the lock above:** May'22–May'23, 247 ICs, 87.9% WR,
+1.05% RoR/IC, +$6,476 — the WR gap to OA was the harsher 1yr window; full-window lock closes it.

## Verified working pattern (SPX 0DTE iron condor)

What ran successfully (LEAN Engine v2.5.0.0.17868):
- `idx = self.add_index("SPX", Resolution.MINUTE)` → `self.spx = idx.symbol`
- `opt = self.add_index_option(self.spx, "SPXW")` (SPX weekly/daily series; **SPXW**, not SPX monthlies)
- `opt.set_filter(lambda u: u.include_weeklys().expiration(0, 0).strikes(-35, 35))` — `expiration(0,0)` =
  0DTE; `strikes(-35,35)` covers 1.5% short + $25 wing with room. **Narrow strikes = the #1 speed lever.**
- Entry via `self.schedule.on(date_rules.every_day, time_rules.after_market_open(spx, 15), ...)` for 9:45.
- Read chain in the scheduled method via `self.current_slice.option_chains.get(self.opt_symbol)`.
- Build IC with `Leg.create(symbol, signed_qty)` ×4 then `self.combo_market_order(legs, 1)`.
- Hold to expiry = do nothing; SPX index options are **European, cash-settled (no assignment)** — they
  settle automatically at 4pm. Matches OA hold-to-settlement.

## Gotchas (verified the hard way)

1. **Built-in "Win Rate" is LEG-level, not position-level.** A 4-leg IC shows ~48% because ~2 legs win
   (shorts) and ~2 lose (longs). **Always compute per-condor win rate yourself** (track portfolio value
   day-over-day on traded days; 1 IC/day → daily realized P&L = that IC's result; log in
   `on_end_of_algorithm`). The `profitLoss` export is also per-leg (988 entries = 247 ICs × 4).
2. **Free B-MICRO node is slow on minute option data** (full 5Y ground for many minutes / can stall).
   Levers: narrow strikes, short window for calibration, and **local LEAN CLI for scale** (runs on your
   machine, no node queue / 200-runs-day cap, `lean optimize` parallelizes sweeps — free).
3. **Right-size data per test.** Hold-to-expiry *structural* tests only need the chain at entry +
   settlement → can use coarser resolution / entry-snapshot (10–60× faster). Minute (or finer) only for
   **hedge/intraday** tests that react during the day.
4. **SPX daily 0DTE expirations began ~May 2022** — earlier dates simply find no 0DTE; usable sample is
   ~2022→ regardless of window.
5. **Model fees + slippage explicitly** to match OA (default fills are mid; OA uses 0.03/leg slippage +
   real commissions). Verify Total Fees ≠ $0 after adding a fee model.
6. **Match OA's reaction granularity for hedges:** OA Monitors poll ~1 min. Backtesting a touch hedge at
   per-second granularity flatters it. Model hedge reactions at 1-min to stay honest.

## Speed & cost (verified 2026-06-23)

- **Free B-MICRO cloud node:** ~190–210s for a 1yr minute-options run; full 5Y ~12–15 min. 200
  backtests/day cap, 20s launch delay, single node (queues).
- **Local LEAN CLI is NOT free for our data.** It needs data on-machine; QC's auto-downloader charges
  **QuantConnect Credits (real money) per options data file**. Free data is cloud-only. So local CLI
  removes the node queue but adds a per-download data cost for SPX options. Don't assume "local = free."
- **QC options data is MINUTE-ONLY** (no hourly/daily option bars). So the "coarser resolution to go
  faster" lever does NOT exist here — minute is forced. Free speed levers are limited to: narrower
  strikes (±20 covers 1.5%+$25 wing), shorter windows, fewer disciplined runs. A full-window minute run
  stays ~10–15 min on B-MICRO regardless.
- Paid speed (verified prices, newtrading review 2026): **QC Researcher $60/mo** = off the throttled
  B-MICRO onto real node(s), up to 2 concurrent, no 200/day cap (this is the entry to faster cloud
  backtesting; live not needed for us). Beefier add-on nodes $24/mo (L1-1) → $1,000/mo (GPU); a
  mid-node for heavy minute-options ≈ $24–60/mo more. So **~$60–120/mo** for comfortably fast cloud.
  Alternative: **local CLI + Polygon (~$29/mo)** = free compute on your Mac, but Docker + data-format
  conversion work. Decide at the hedge-tournament stage.
- **Fee model fix:** set fees on each *contract* via `set_security_initializer`, NOT on the canonical
  option (that's why Total Fees showed $0). Verify `portfolio.total_fees > 0` after.
- **Confirmed fee basis — Tradier Pro Plus: ~$0.60/contract all-in** ($0.10 commission + ~$0.50 CBOE
  index/ORF/OCC pass-throughs). Use the custom per-contract `TradierSpxFeeModel` (scales with size);
  set OA's commission to the same $0.60 so LEAN/OA/live agree. (Lite/Pro would be ~$0.85/contract.)

## Faster calibration lock — shrink OA, don't grow LEAN

To compare apples-to-apples without a slow full-window LEAN run: **re-run the OA backtest on LEAN's
window** (cheap in OA) rather than running LEAN on OA's 5Y. E.g. set OA Batch 1 Control to
May'22–May'23 and compare its per-IC win rate to LEAN's 87.9%. Match = calibration locked.

## Metric mapping (LEAN → OA)

- OA "Win Rate" (per IC) ↔ LEAN: compute per-condor (NOT the built-in leg-level stat).
- OA "Return on Risk / trade" ↔ LEAN: `net_pl_per_IC / (wing × 100 × qty)`; report this, not Total P/L.
- Judge on RoR + Worst Loss + per-condor win rate; ignore LEAN's Sharpe/Total-P&L for ranking ICs.
