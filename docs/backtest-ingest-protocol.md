# Backtest Ingest Protocol

**What this is:** the standard routine Claude runs every time Andy pastes OA backtest
results. It exists so the analysis is *deterministic across sessions* — Claude does NOT
reliably reproduce a routine from memory; this doc is the contract. Pairs with
`daily-results-process.md` (daily live-results plumbing) and `daily-brief-spec.md` (the
cockpit). This one is for **backtest / Compare-page results**, not live daily P&L.

Apply the `oa-mirror-reference.md` §3 evidence standards and the `methodology.md`
factor-bucket lens throughout. Compare by **R**, never raw P/L.

---

## What Andy pastes (per batch)
Three artifacts. All three are wanted; none is redundant.
1. **Compare-page screenshot** — the A/B/C/D column grid (the headline numbers).
2. **Settings / Position Details screenshot for each column** — so Claude can verify the
   config actually matches the pre-registered hypothesis (catches setting slips).
3. **`positions.csv` for each column** — Copy/Download CSV from the backtest's positions
   list. The only artifact that exposes what the summary screen hides.

If only some arrive, Claude proceeds with what's present and **names what it could not
verify** (e.g. "no Details screenshot → config unverified" or "no CSV → forensic skipped").

---

## Two speeds: DISCOVERY (broad) vs CONFIRMATION (strict)

Discovery and confirmation need different rules. The mistake is applying one phase's rules to the
other — strict rules on discovery kill good leads before you see them; loose rules on confirmation
ship a curve-fit (the 95.3%→57% scar). So run two speeds, and **never let a discovery finding skip
to deployment.**

### DISCOVERY mode (default for screening / "explore the space" nights) — be BROAD
Cast a wide net. **Pre-registration NOT required. Per-cell null NOT required.** Screen many single
indicators and thresholds, eyeball combos, look at the whole grid — including indicators with no
strong a-priori thesis (oscillators are fine to *look* at; just don't *believe* them yet). The only
four rules that stay on, because they cost ~nothing and are the actual protection:

1. **OOS quarantine (the firewall).** Explore **in-sample only**; do NOT touch the OOS holdout
   (default 2024–26) during discovery. This is what makes broad dredging *safe* — an untouched
   holdout still tells the truth no matter how much you searched. Never "just peek" at OOS.
2. **Trial ledger.** Tally every variant run in the session. Costs nothing; it's the only way to
   deflate a winner later (best-of-3 needs a small margin; best-of-40 a large one).
3. **Exploratory tag.** Everything found in discovery is tagged **exploratory** — a hypothesis for a
   fresh test, NEVER a verdict, no matter how good it looks.
4. **Compare by R, never win rate.** Free; prevents the dumbest error.

### CONFIRMATION mode — be STRICT (this is the gate to paper/capital)
Take the handful of survivors discovery surfaced and NOW apply full rigor: **pre-register** each as a
specific hypothesis (factor, expected direction, pass threshold) *before* re-running; **beat the
no-filter control AND the random-day null**; for combos, **the combo must beat the best single
component**; then the **OOS holdout**; then paper. Only confirmation survivors earn capital. State the
trial count and deflate for it.

**The rule that bridges them:** an exploratory winner is never deployed — it must be re-run as a
pre-registered confirmation test (fresh, on quarantined OOS) before it papers. Discovery proposes;
confirmation disposes.

---

## Window policy (which years to backtest)

- **In-sample = the FULL available window, including 2022.** 2022 is NOT an outlier "bad year" to
  remove — for the high-vol directional strategies it's the **best year and the target regime**
  (63% of trades / 77% of P/L in Batch 1-D). Cutting it deletes the signal, not noise. Max regime
  coverage = better discovery.
- **A true 5yr 0DTE backtest does not exist** — SPX daily 0DTE began ~May 2022, so the full 0DTE
  window is only ~2022→now (~4yr). "3yr vs 5yr" for 0DTE really just means "include 2022 or not" —
  and you include it. The new **2013 history only helps for longer-dated / 45-DTE** directional
  variants (then it adds 2015, Volmageddon '18, COVID '20 — use it there).
- **OOS holdout = a pre-committed recent slice (default 2024–26), quarantined** until confirmation.
  This is where you learn forward expectancy when 2022 isn't repeating (Batch 1-D ex-2022 ≈ +$1,486
  / 105 trades, rare-fire). Report per-regime; size for a rare-fire strategy, not all-weather.
- **Window choice is NOT a knob to tune for pretty numbers** (period-shopping is overfitting too,
  whether you cut 2022 to hide it or keep it to inflate the mean). In-sample = all of it; OOS = the
  pre-committed slice; don't shop.

---

## What Claude does, in order

### Step 1 — Config verification (from the Details screenshot)
Before trusting any number, check each column's settings against the stated hypothesis and
flag mismatches. Checklist: **symbol, DTE, strategy/structure, strike selection (%OTM/Δ/$),
width, entry trigger + time, trading days, position limit, slippage, PT, SL, and the ONE
entry filter under test.** Confirm only one factor varies across columns (the pre-register
rule). **If a setting is off-spec, say so first and treat that column's result as suspect.**

### Step 2 — Headline grid (from the Compare screenshot)
Build the compare table in **R terms**: RoR/trade (or Exp(R)), Profit Factor, Worst Loss,
N (trades), and total P/L as secondary. Check the gate the batch is testing:
- Is the effect **monotonic** across the swept factor (not a zigzag = noise)?
- Does every gated column **beat the control**? (Necessary but NOT sufficient — must also beat
  the random-day null in Step 3; beating control can just mean fewer/luckier days.)
- **N ≥ 100** and **span ≥ 6 mo**? Flag any column that fails.
- Win rate is context only — **never the verdict** (high-WR/negative-expectancy is the trap).
- **For HEDGE batches, worst-loss and tail are first-class, not secondary.** A hedge is judged
  on **tail/worst-loss reduction vs the RoR it gives up**, always against **unstopped** as
  control. Add a **tail count** (trades worse than 3× avg credit) per column. The verdict is
  the (RoR, worst-loss) pair *jointly* — a hedge wins only if it cuts the tail enough to
  justify the premium it costs.

### Step 3 — CSV forensic (per column, the part the summary can't show)
Run the standard battery on each positions.csv:
- **IC FIRST STEP — group legs/spreads into condors.** OA logs each spread/scanner as its own
  position (confirmed in the QQQ Fortress data: separate scanners → separate rows). For any IC
  tournament, pair the two spreads into one condor by (day, entry window) BEFORE computing WR/R,
  or you'll read the leg-level ~48% WR trap. Per-condor only. (Single-leg directional spreads:
  one position = one trade, skip this step.)
- **Random-day null** (when a gate claims edge): bootstrap from the control's trade population —
  does the gate select genuinely better days than randomly drawing the same number of days?
  Report the p-value; pass bar = gated RoR > control RoR **AND** null p < 0.05 (the `c1_analyze.py`
  method). Beating control alone is not a pass.
- **Expectancy in R:** mean R and **median R** (median hitting the stop while mean is
  positive = positive-tail structure → exit-cap questions).
- **Fill realism (uses Open/Close Bid/Ask):** flag trades filled at mid inside a wide spread —
  the cheap-0DTE $0.05-fill pathology (5/15, 6/16). Serves the "real returns run below backtest,
  slippage is material" rule; it's free now that bid/ask is in the export.
- **Win/loss anatomy:** avg win, avg loss, worst, reward/risk realized.
- **Exit distribution:** profits / stoploss / expired counts + P/L each. (Expired or
  ride-to-end being the biggest wins ⇒ the PT cap may be truncating the tail.)
- **Losing-day signature** (uses **Price at Open / Price at Close** in the CSV): on the
  losing trades, did the underlying move *with* or *against* the position? (For the put
  variant: did SPX rally? If ~all losses are rally-days ⇒ the lever is **direction
  confirmation**, not a hedge.)
- **Regime / year concentration:** P/L and WR by calendar year. Flag if one regime (e.g.
  2022) carries most of the edge ⇒ **OOS holdout required**.
- **OOS holdout (pre-committed, not "when asked"):** the IS/OOS split is fixed at session start
  (default holdout 2024–26). Sweeping happens in-sample only; OOS is touched only for the final
  1–2 survivors. Require the edge to survive in **≥2 distinct regimes**, not just be positive
  overall (the all-2022, rare-fire earner is not an everyday strategy).

### Step 4 — Verdict + write-back
- State **PASS / FAIL vs control + null/OOS**, the main effect (not the best cell), and the
  honest caveats (apply the live haircut reminder). Tag the read **confirmatory** (matched a
  pre-registration) or **exploratory** (post-hoc → needs a fresh test). **State the trial count**
  and deflate the verdict for it (best-of-N needs a margin that grows with N).
- Name the **next batch in the queue** (`directional-oa-build-sheet.md` RUNNING QUEUE is
  authoritative for Directional).
- **Update `current-state.md`** (the relevant pillar §) and **append `session-log.md`**.
- Discipline gate: pre-registered hypothesis, one factor/batch, beat control + OOS, main
  effect — flag the 95→57 over-fit trap if a batch sweeps too many filters at once.

---

## Output shape (what Andy gets back)
1. **Config check** — ✅/⚠️ per column (mismatches first).
2. **R-grid** — the compare table + the gate verdict (monotonic? beats control? N/span ok?).
3. **Forensic** — the 2–4 things the summary hid, per the Step-3 battery.
4. **Verdict + next step** — PASS/FAIL, caveats, the next queued batch.

Keep it tight; Andy wants the read, not a recap of the routine.

---

## Notes / gotchas
- **CSV export confirmed working 2026-06-25** (resolved the old "export-blocked" premise).
  Schema: `Opened, Closed, Symbol, Exp, Type, Legs, Quantity, Status, P/L, Risk, ROR,
  Premium, Reward/Risk, Open/Close (Bid/Ask) Price, Max Loss, Max Profit, Price at Open,
  Price at Close`. `Max Loss/Max Profit` are the **structural** spread bounds (= Risk /
  reward), **not** intraday excursion — the CSV does NOT contain the intraday P/L path, so
  touch/excursion-dependent hedge questions still need LEAN/OO.
- `Status` values seen: `profits`, `stoploss`, `expired`. `Price at Open/Close` = underlying
  at entry/exit (enables the losing-day forensic without minute data).
- LEAN fills run ~4× hot; OA backtest ≈ live-predictive but still apply a ~30–40% haircut to
  absolute economics. Use R and relative rankings for the decision; OA-paper is the gate.
