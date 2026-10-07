# Edge Funnel — prior art (handoff §4), 2026-10-06

**Scope.** What earlier work already says about whether this program has an edge. One row per finding in
`data/backtest_findings.csv` (54 rows, `BF-001`…`BF-054`); every figure below cites its row, and each row
cites its source file. Search scope (§5) is **not** drafted here.
**Units.** "R" means P/L ÷ risk. Condors are R per condor, debit spreads are R per position.
"Net" uses OA's rendered fee estimate of **$3.16 per 1-lot SPX IC transaction** (BF-008).
**Deferred, not captured.** The OA `/backtests` leads (the long call spread listed at $42.1K, the
.05/.30/.82Δ long calls, `PUT-OOS-control` vs `-gated`) are deferred by Andy. BF-043 and BF-041 record what
the *docs* say about the first and the last of those leads, nothing more.

## 1. Bottom line
- **No finding on file is a net-of-fee edge confirmed on a sealed holdout.** Not one.
- **Short premium (0DTE IC) shows about zero gross, negative net, and a regime flip.** All four SPX 13:30 ride
  arms are net-negative over 2021-10→2024-12 and positive over 2025-01→present; the Touch $10 arms do the
  reverse, positive before 2025 and flat or negative after (BF-002, BF-004, BF-006, BF-007). The QQQ
  primary shows the same flip: +0.0018 R before 2025, +0.1045 after (BF-012). The sealed holdout window
  `R-2026-10-06-TAIL-HOLDOUT` uses is a *favourable short-vol regime*. **For short premium, passing that
  holdout is not evidence of edge.**
- **Exits don't create edge.** Across five mechanics the paired spread is 0.0215 R, and no CI excludes
  zero (BF-013). Touch exits fix the tail, but net of fees only A3 and A6 end positive (BF-003), and A3
  loses net in the holdout (BF-004).
- **The only leads with real signal are long-premium and gated, and both are unverified** (§2).

## 2. The three strongest leads, with evidence

| # | Lead | Evidence | Why it is not yet a finding |
|---|---|---|---|
| 1 | **SPX 0DTE long call spread, VIX Change% < −2, 11:00, SL50, ride** (v1 call track) | +21.9% R/position, PF 1.63, n 337, positive every year 2021–26 per doc; random-day null p 0.000 at the gate step (BF-042, BF-043) | (a) The 2024+ "OOS" was split *after* exits were chosen on the full window, so it was never sealed. (b) ~25 arms were tried across the two tracks. (c) **Lookahead risk:** OA documents Change% as prior close→entry time for the *underlying* (OA-1111); for VIX Change% the docs say nothing, and the doc's own "100% of wins are up days" fits lookahead as well as edge. (d) No CSV survives in either repo. (e) Live PR-06: n 11, −0.139 R/position, 95% CI [−0.56, +0.28]. That is not a falsification, but it is not support either. |
| 2 | **SPX 0DTE long put spread, VIX ≥ 22, 11:00, PT100/SL75** (v1 put track) | +9.2% R/position in-sample, n 280 (BF-038); "OOS" +6.4%, n 76, vs control −3.0% (BF-041) | The holdout overlapped every earlier batch's 5Y window, so it is not sealed. No significance test. n < 100. 2022 carries 77% of P/L (BF-037). The entry-time surface is a single sharp peak, an overfit signature (BF-040). No live fills. |
| 3 | **IV/VIX-level-gated short premium** | Calmest 20% of mornings by ATM IV held 0.75%-OTM strikes 96% vs 69% base, p 0.000 vs null, 956 days (BF-033). ATR5 adds the same signal (BF-034). The regime flip in §1 is consistent with it. | It was a price-vs-strike study and has never been run as a P&L gate on an IC. In-sample only. The middle-band numbers are interpolated. |

## 3. Dead or stale, and why
- **The base SPX IC shapes.** 13:30 ride: +0.0022 R gross, −0.0050 net (BF-001). 11:00: every arm fails
  (BF-005). Strike distance: .05/.07 are net-negative; .15 nets ~0 in holdout (BF-006, BF-007).
- **Exit mechanics as an income lever:** BF-013. Canary's gross t = +4.85 disappears once fees apply
  (BF-014).
- **Unconditional long premium:** the afternoon QQQ put overlay ran −0.2047 R (BF-015); the combine adds
  nothing (BF-016).
- **v1 headline backtests:** the champion's "95.3% WR / walk-forward PASSED" has no unit, window or cost
  (BF-027). Fortress went OOS-negative (BF-028). The "arsenal Sharpe 1.4" (BF-029) and "S2 964 trades"
  (BF-030) have no artifact.
- **v1 tournaments and Hindsight:** invalidated arms, pre-2026-07-31 denominator (flattered), contaminated
  cohort (BF-047, BF-048).
- **Gates already falsified:** gap % for IC (BF-031); call momentum and dip-buying (BF-036); six put gates
  that lost to VIX ≥ 22 (BF-039); OR-break (BF-040); pivots and newsletter levels (BF-035); GEX and intraday
  momentum (BF-051); candle-run reversal (BF-050).
- **Stale or falsified claims:** "Touch0 is not firing" was superseded when it fired on 09-18 (BF-018).
  "Nothing held to settlement lost" fails: 53 of 353 positions lost (BF-017). `ic-trailing-stop-backtest`
  rests on a falsified premise and an exit the backtester can't express (BF-025). The OO trials never ran
  (BF-026). Mirror leaderboard numbers carry no unit and are external (BF-046).

## 4. Data-quality flags the search must carry
- **Missing units:** BF-027, BF-028, BF-046, BF-047 (Exp(R) with no per-leg/condor label).
- **Pre-2026-07-31 denominator:** BF-025, BF-047, BF-048. Restate or drop them; none is used here.
- **Narrative numbers with no CSV:** the whole v1 directional series (BF-037…BF-044). Neither repo holds
  the positions CSVs, and the docs don't record test ids. CSV wins; here there is no CSV.
- **No sealed holdout:** every v1 lead (BF-041, BF-043) and every v2 run before 10-06.
- **Gross-only:** QQQ fees were never rendered in a capture. Breakeven for S1-0 is ≈$5.75 per transaction
  (BF-012).
- **Backtester fidelity:**
  - Entries are one-shot; live scanners retry every minute (BF-010).
  - Exits end around 15:45 on SPX (BF-003), but QQQ touches have closed at 15:54–15:58 (BF-021). Unresolved.
  - Before 2022-05 the window has MWF expiries only (BF-009, BF-052).
  - Strikes replicate live exactly (BF-011).
  - External backtests degrade ~50% live (BF-045).

## 5. What this implies for §5 (inputs only, not the scope)
1. Score edge **net**. A fee ruling is needed before any arm runs (BF-008).
2. Require **per-year stability or regime-split reporting**, not only a pass on the 2025+ holdout (BF-002, BF-012).
3. Verify **VIX Change% entry-time evaluation** before lead 1 is re-tested. If it reads end-of-day, the
   whole call track is lookahead.
4. Spend the arm budget on entry gates, structure and regime (leads 1–3). Exits are a measured dead end (BF-013).
5. Handoff §5b (queued "touch decision" study) inherits BF-053/BF-054: fixed touch exits trade winners for
   tail, and live touches split reverted/continued 2–2. Its step 1 also inherits the open exit-cutoff conflict
   (BF-003 vs BF-021) and the ~20-day 1-min Tradier retention, which is why it needs purchased data.
