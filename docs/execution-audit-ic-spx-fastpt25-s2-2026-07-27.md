# IC-SPX-FastPT25-S2 — Execution Forensic

*Audit date 2026-07-27 · ledger current to 2026-07-02 · scope = **post-fix epoch only** (see Scope note)*

**Declared:** exit = PT25 | hedge = S2 (close whole IC on short-strike touch) | entry = 11:00, Range075 filter, 0.75% OTM, $5 wide | sizing = 10–12 contracts, ~$4.6–4.9K risk/leg, ≤10 re-entries

**Ledger (post-fix, 2026-06-08 → 2026-07-02):** 47 positions, 13 losses, P/L −$5,455, Exp(R) −0.0250, 15 trading days

**Verdict:** **EXECUTION-BROKEN on the profit target; execution-clean on the hedge and the entry.** [PT25 failure **CONFIRMED** — the exit option is verified attached, the Bid-Ask Guard is verified off, and no order was generated on 3 order-level instances or across 24 ride-to-expiry positions. S2 firing CONFIRMED correct and prompt. Orphan-loop CONFIRMED and named.] The bot has not been running its declared strategy. It has been running *ride-to-expiry with an S2 strike-touch monitor and an orphan-leg cleanup*.

> **Scope note.** 317 of the bot's 364 ledger positions are `epoch=pre-fix` and opened at 09:xx, not the declared 11:00 (270 of 317 at the bell). Auditing those against a spec the bot demonstrably was not running is a category error, so they are excluded. This audit covers the 47 post-fix positions. **Flag: 47 positions over 15 trading days is far below the ≥100-trade / ≥6-month evidence bar.** Every conclusion below is directional, not decision-grade.

---

## Findings, most severe first

### F1 — Structural impossibility: $3,000 of the 6/11 loss could not have happened in a market
`2026-06-11 | T00147 | shortcallspread | 7315/7320 | q12 | credit $1.05 | **−$7,740** | R **−1.633**`

Max structural loss = ($5 × 12 × 100) − $1,260 = **$4,740** — which is exactly what OA itself reports as *Capital at Risk*. The realised loss exceeds it by **$3,000**.

Cause is now settled by order-level evidence, and it is **not** an OA exit failure:

- **Trade Details:** SmartPricing **Market**, BID/ASK **0 – 7.5**, Order 403634334, LIMIT PRICE `Market`, **filled at $7.50**.
- A $5-wide vertical cannot be worth more than $5.00. The bot paid **$7.50** — 150% of the structural maximum — because a market order took the ask of a garbage 0×7.50 quote.
- **OA's own high-water tracker on this position says the spread's worst mid all day was −$1,680 (−133.3%), i.e. a value of ~$2.45.** The fill was $5.05 above the worst price the position ever actually reached.

**This was a settings choice, and it has already been fixed.** `bots_config.csv` records: *"S2 close switched Market→SmartPricing 2026-06-14."* 6/11 predates that change. Both later positions I have evidence for (6/24, 7/02) show SmartPricing **Fast** with a proper price ladder — 6/24: `$2.20 ✓ → $2.30 → $2.40`; 7/02: `$2.30 ✓ → $2.35 → $2.40`. The remediation is confirmed working.

Two layers, both real: **(i)** `settings` — Market pricing on the S2 close; **(ii)** an OA **paper-engine artifact** that permitted a fill above the structural cap at all (`oa-platform-reference.md` §16.1 records a paper-engine fix for *"the class of impossible-fill artifact we hit on 6/11"* — same date). Layer (ii) means **$3,000 of this loss is not a real trading loss and should be excluded from the bot's performance record.**

### F2 — PT25 generated ZERO exit orders across all 47 post-fix positions
This is the central finding, and it does not depend on any model.

**Order-level evidence (meets the CONFIRMED bar):**

| Position | OA's own high-water tracker | PT25 threshold | Profit-taking order in Trades list |
|---|---|---|---|
| 6/24 T00095 put | **40.0% high · $100 high** | 25% | **None.** Only `Open 11:08AM` + `Close 1:25PM` |
| 6/11 T00147 call | **45.7% high · $576 high** | 25% | **None.** Only `Open 11:01AM` + `Close 1:29PM` |
| 7/01 T00029 put | **33.3% high · $50 high** | 25% | **None.** Only `Open 11:09AM` + `Close 11:12AM` |

Both positions cleared the profit target by a wide margin, on OA's own accounting, and **no order was ever generated.** Per the Fortress precedent, a healthy position shows a profit-taking row (sent, possibly cancelled). These show two rows.

**Corroboration across the full post-fix set:** **24 of 47 positions rode to expiry** (`status=expired`, `close 16:15`, `exit_price 0`, `mfe_pct 1.00`) — i.e. their premium decayed to zero and PT25 never closed them at 25%. A live PT25 evaluating mid every minute cannot miss 24 consecutive positions whose mid went to $0.00.

**The Exit Options editor (operator-supplied 2026-07-27) settles the `settings` alternative — PT25 IS attached:**

| Field | Value |
|---|---|
| **Profit Taking %** | **25% of credit** — attached, with `PRICING: Normal` |
| Profit Taking $ / Price Target / Stop Loss % / Stop Loss $ / Trailing Stop | None |
| **Touch** | **None** — see F7 |
| Expiration / Avoid Events / Earnings | None |
| **"Disable exit options if bid/ask exceeds $"** | **UNCHECKED, blank — the Bid-Ask Guard is OFF** |
| Header | *"Your bot checks your position every **1 minute** from 9:31am to 1 minute before market close"* |

So the rule is attached, live every minute from 9:31 to ~15:59, with **no guard that could disable it**. That eliminates the single benign explanation that mattered.

**Benign explanations ruled out, one line each:**
- *by_design* — no. PT25 is attached in the automation and named in `bots_config`.
- *cash settlement* — irrelevant; PT25 is an intraday mid-price rule, not an expiry mechanic.
- *market_unfillable* — no. An unfilled order still appears in the Trades list. And a position at mid $0.00–0.05 against a $0.26–0.79 target is trivially fillable — that is the 24 expiries.
- *Bid-Ask Guard* — **ruled out by direct evidence.** The checkbox is unchecked and the dollar field is empty. There is no guard configured on this bot.
- *filter gating* — n/a, this is an exit not an entry.
- *config-record staleness* — **now ruled out.** The automation itself, not just the position panel, shows `25% of credit`. Residual caveat below.

**Cause: `oa_execution` [CONFIRMED].** The exit option was attached, evaluated every minute, unguarded — and generated no order on three order-level instances and across 24 positions whose premium decayed to zero. This is the Fortress precedent reproduced on the champion.

**Residual caveat, stated plainly:** the editor shows the automation's configuration *today*. There is no dated change-log proving `25% of credit` was set on 2026-06-24 rather than added since. I judge this remote — `bots_config` records the 6/14 pricing change but no PT change, and all four Position Details panels show `PROFIT % 25%` — but it is the one gap that remains. **Evidence that would fully close it:** OA's bot/automation change history for `Scalp-Scan-Put`.

**Secondary friction worth recording (it cuts against my own counterfactual):** SPX spreads quote in $0.05 increments, and PT25 targets land off-tick on 13 of 17 distinct post-fix credits — $0.35 → $0.2625, $0.55 → $0.4125, $1.05 → $0.7875. OA sets the SmartPricing final price *at* the target, so a fill requires the next better tick. This makes PT25 fills harder than the model assumes and means **the recovery figures below are optimistic even by their own optimistic standard.** It does **not** explain the 24 expiries, where the spread decayed to $0.00 against targets of $0.26–$0.64.

### F3 — 2026-07-01: ten open→close round-trips in 29 minutes with no touch, no target, and no stop
| Open→Close | Short put | SPX range in window | Touch? | Credit → exit | P/L |
|---|---|---|---|---|---|
| 11:01→11:03 | 7440 | 7496.36 – 7506.68 | **No** | 0.20 → 0.15 | +$50 |
| 11:03→11:06 | 7445 | 7496.36 – 7507.76 | **No** | 0.20 → 0.20 | $0 |
| 11:06→11:09 | 7450 | 7500.60 – 7507.76 | **No** | 0.15 → 0.25 | −$100 |
| 11:09→11:12 | 7445 | 7500.60 – 7508.42 | **No** | 0.15 → 0.20 | −$50 |
| 11:12→11:15 | 7450 | 7501.86 – 7513.16 | **No** | 0.20 → 0.15 | +$50 |
| 11:15→11:18 | 7455 | 7507.81 – 7513.16 | **No** | 0.15 → 0.20 | −$50 |
| 11:18→11:21 | 7455 | 7507.81 – 7518.19 | **No** | 0.15 → 0.15 | $0 |
| 11:21→11:24 | 7460 | 7512.30 – 7518.19 | **No** | 0.15 → 0.20 | −$50 |
| 11:24→11:27 | 7460 | 7512.30 – 7521.11 | **No** | 0.10 → 0.15 | −$50 |
| 11:27→11:30 | 7460 | 7513.98 – 7521.11 | **No** | 0.10 → 0.15 | −$50 |

SPX traded **7496–7521 all window — 40 to 60 points above every short strike.** Nothing was ever tested. So:
- **S2 did not fire** (no touch — verified against 5-min tape).
- **PT25 did not fire** (five of the ten closed at a *loss*; three had `mfe_pct 0.00`).
- **No stop is configured** on this bot.
- **Range075 did not stop it** — SPX ran +0.078% → +0.284% from the prior close, passing the gate on all ten re-entries. The filter is not designed to catch this.

**The mechanism is now CONFIRMED and the closing agent is named: `Scalp-Mon-S2-Cleanup`.** Two operator-supplied Automation Logs (Jul 1, 11:12AM and 11:27AM, both triggered by Monitor) show identical trees:

> `Repeat for each position` → `Position: SPX −7,445 put / +7,440 put` → **"Position has been open 2 minutes or more" → Yes** → **"Bot has exactly 1 position with any type and open status" → Yes** → **Close Position**

This is an **orphan-leg cleanup**: if a position has sat unpaired for 2 minutes, kill it. The intent is sound — don't leave a naked single-sided leg on a 0DTE book.

**I must correct my previous attribution.** I earlier read this as the §13 *"scan node checks the wrong side"* bug. **It is not.** The `Scalp-Scan-Call` editor (operator-supplied) shows it gates on `Bot has exactly 0 positions with **call** side and open status` — correctly mirrored against `Scalp-Scan-Put`'s put-side gate. Both scanners are correct in isolation.

**The real defect is a race with no interlock.** The two scanners each gate only on *their own* side; the Cleanup monitor gates on the *total* position count. So:

1. `Scalp-Scan-Put` sees 0 put positions → opens a put spread. Total = 1.
2. `Scalp-Scan-Call` should open the call side in the same cycle → total = 2, Cleanup's "exactly 1" is false, nothing happens. **On 7/01 it never fired** — no call spread opened all day.
3. Two minutes later, Cleanup sees exactly 1 open position → closes the put.
4. Same cycle, **Scanners run after Monitors** → the put scanner sees 0 put positions → re-opens.
5. Loop until the daily position cap.

Nothing in the system remembers that this already happened. There is no "the other side already failed today" condition on Cleanup and no "don't re-open what Cleanup just killed" condition on the scanner. **The 2-minute gate plus the 1-minute monitor cadence produces exactly the observed 2–3 minute round-trips**, and the ledger timestamps show the handoff — **every close is followed by an open one second later**:

`11:03:02 close → 11:03:03 open` · `11:06:02 → 11:06:03` · `11:09:02 → 11:09:03` · `11:12:01 → 11:12:03` · `11:15:05 → 11:15:08` · `11:18:02 → 11:18:03` · `11:21:03 → 11:21:04` · `11:24:03 → 11:24:04` · `11:27:01 → 11:27:02`

Monitor closes the orphan put; Scanner, in the same cycle, sees zero put positions and re-opens. 7/01 was a **put-only day — 10 put spreads, zero call spreads, all flagged `single_sided`.**

**The 6/08 natural experiment confirms it.** T00161 opened 11:31:01 and was closed 11:33:02 with no touch — same signature. Then at **11:33:03 a call spread opened**, at 11:34:03 the paired put opened, **and the churn stopped instantly**; that pair rode to expiry for +$850. The loop terminated the moment the call side filled. That is a causal signature, not a coincidence.

**Cause: `settings` [CONFIRMED].** Both halves of the loop are now evidenced: the scanner's own-side gate (editor + log) and the Cleanup monitor's 2-minute / count==1 close (two logs). *Ruled out:* by_design (nothing declares a 3-minute round-trip); cash settlement; market_unfillable (all filled); filter gating (Range075 passed on all ten, +0.078% → +0.284%); oa_execution (every automation did exactly what it was configured to do — this is a design race, not a platform failure).

**Open sub-question: why did `Scalp-Scan-Call` never fire on 7/01?** Its decision tree passes the same four gates the put scanner passed. The likely blocker is inside the `Open SPX Short Call Spread` action's opportunity filters — SPX rallied 7496→7521 that morning, so 0.75%-OTM calls near 7560 would have been very cheap and may have failed a minimum-credit or delta filter. **That is a hypothesis, not a finding.** Evidence: the `Open SPX Short Call Spread` action's opportunity settings, or a `Scalp-Scan-Call` log from 7/01 showing where it exited the tree.

Direct cost was small (−$250 on 7/01) but it **burned the entire 10-re-entry daily cap in 29 minutes** — that is the real damage, and on a day with a genuine setup it would have left the bot with no ammunition.

**Scale of the signature.** Positions closing 2–4.5 minutes after open, post-fix: **11 of 47, −$305** (10 of them 7/01, plus 6/08 T00161). Across the bot's full history including pre-fix: **122 of 364 positions, −$2,345**, clustered on 7/01, 5/18, 5/07, 5/05, 5/01, 4/09. I am **not** claiming all 122 are Cleanup fires — 78 of them carry `single_sided=False` and the pre-fix epoch ran a different entry regime. It is a same-signature population that warrants its own pass, not a conclusion.

### F3b — Entry logic is CONFIRMED correct (the one clean result in this audit)
The `Scalp-Scan-Put` Automation Log (Jun 24, 11:08AM, triggered by Scanner) shows the full entry tree executing as specified:

| Node | Result | Verdict |
|---|---|---|
| `Symbol change % is greater than -0.75 since previous close` | Yes | **Range075 implemented correctly** — as a two-sided %-change-since-prior-close gate, exactly as `oa-platform-reference.md` §13 requires (a gap filter, not a high-low range check) |
| `Symbol change % is less than 0.75 since previous close` | Yes | ↑ |
| `FOMC Meeting today` | No | **FOMC skip present and real** |
| `Current market time is after 11:00am` | Yes | **The 11:00 gate is a real decision node**, not assumed — this is the 6/07 fix, verified from primary evidence. It also independently validates the pre-fix/post-fix epoch split used to scope this audit. |
| `Bot has exactly 0 positions with put side and open status` | Yes | **DEFECTIVE — see F3** |

Reconciles to market data: SPX prior close 6/23 = 7365.46, SPX at 11:08 = 7413.21 → +0.648%, inside the ±0.75% band. The gate passed for the right reason.

### F4 — S2 fired correctly and promptly every time it fired — and cost money
Execution is clean. On 7/02 SPX first traded below the 7445 short put in the **13:00** bar; S2 closed **both** legs at **13:02** — a 2-minute response. The 6/11 Automation Log shows the exact decision path (`Scalp-Mon-S2-StrikeTouch`, triggered by Monitor, `Repeat for each position 2/2`, tag check → `No` → `underlying above short call strike` → `Yes` → Close Position). The mechanic works as designed.

The problem is not execution. It is that **the mechanic lost money over the window:**

| | Post-fix total |
|---|---|
| Actual | **−$5,455** |
| Ride to settlement (no S2, no PT) | **+$830** |
| **S2's contribution** | **−$6,285** |
| S2's contribution excluding the F1 artifact | **−$3,285** |

Leave-one-day-out on the raw −$6,285: range −$3,150 (drop 6/09) to −$9,465 (drop 6/10); **sign never flips**. But after removing the F1 artifact, dropping 6/09 leaves −$150 — effectively zero. **So: directionally negative, not robust enough to act on.** 15 days is not a sample.

**This contradicts `docs/current-state.md`**, which states *"S2 mechanic is healthy in production."* Healthy ≠ profitable — it is executing correctly and still costing R.

### F6 — The 6/14 Market→SmartPricing remediation was applied to only ONE of the two closing automations
The 7/01 Position Details Trades list shows the Cleanup close tagged **`Market`**, filled at $0.20.

Three closing mechanisms, three different pricing settings:

| Mechanism | Pricing | Evidence |
|---|---|---|
| PT25 (Exit Option) | **Normal** | Exit Options editor, `PRICING: Normal` |
| `Scalp-Mon-S2-StrikeTouch` | **Fast** | Trade Details 6/24 (`$2.20 ✓ → $2.30 → $2.40`) and 7/02 (`$2.30 ✓ → $2.35 → $2.40`) |
| `Scalp-Mon-S2-Cleanup` | **Market** | Position Details 7/01, `Market` tag on the 11:12AM close |

`bots_config.csv` records *"S2 close switched Market→SmartPricing 2026-06-14."* That change reached the StrikeTouch monitor. **It did not reach Cleanup, which still sends Market orders.** This is the exact mechanism that produced the $3,000 impossible fill in F1, still live and unremediated.

On 7/01 it was harmless — the quote was tight and the fill was $0.20. The exposure is a Cleanup fire into a wide 0DTE quote, which is precisely the condition under which orphan legs occur. I am recording this as a finding; per the audit's terms I am not authorising a config change, and any fix should go to a pre-registered test.

Secondary: `bots_config` lists `exit_pricing: Fast/100% bid-ask`, but the PT25 Exit Option is set to **Normal**. Not a defect — different mechanism — but the config record is incomplete on this point.

### F7 — The native `Touch` Exit Option is available and set to `None`
S2 is a strike-touch hedge, and OA exposes **Touch** as a native Exit Option — evaluated every 1 minute in the Exit Options class, which runs *first* in the platform's cycle order. The bot has `Touch: None` and implements S2 entirely as monitor logic, which runs third.

In practice the monitor has been fast (2 minutes from the 13:00 touch bar to the 13:02 close on 7/02), so this has not visibly cost anything. Recording it as an unexploited platform capability, **not** as a recommendation — F4 shows S2 lost money over the window, so making it fire *faster* is not obviously an improvement. Route to a pre-registered test if it is worth asking.

### F5 — A documented claim in `current-state.md` is factually wrong
The doc says of 7/02: *"a genuine put breach where **S2 fired and cut early (helped** — hold-to-expiry ≈ max loss)."*

Hold-to-expiry was a **full winner**. SPX settled at **7483.24**, 38 points *above* the 7445 short put. Tradier confirms the legs settled at $0.05 / $0.03 — worthless. `PRICE AT CLOSE 7,442.66` on the OA screenshot is SPX at the 13:02 exit, **not** the 4:00 close; the doc read it as settlement.

| | 7/02 T00002 put |
|---|---|
| Actual (S2 at 13:02 @ $2.30) | −$1,950 |
| Hold to settlement | **+$350** |
| **S2 cost** | **−$2,300** |

S2 exited into a 13:00 dip; SPX bottomed at 7427.55 at 14:00 and rallied 55 points into the close. This is a textbook S2 whipsaw, recorded in the project's narrative as an S2 success.

---

## The counterfactual that matters — and its honest cost

If PT25 had actually executed across the post-fix window (gated on OA's own `mfe_pct` ≥ 0.25, so no position is credited with a profit it never reached):

| | Actual | PT25 executes | Delta |
|---|---|---|---|
| **13 losers** | −$17,625 | +$3,064 | **+$20,689** |
| **32 winners** | +$12,170 | +$3,316 | **−$8,854** |
| **Net (47)** | **−$5,455** | **+$6,468** | **+$11,922** |

**Preemption warning — read this before quoting the +$11,922.** The winners' give-back is not optional; it is the same rule. PT25 caps every one of the 24 ride-to-expiry winners at 25% of credit. The headline number is only valid if both sides are taken together. Quoting +$20,689 alone would be dishonest.

**All figures except actual settled P/L are OPTIMISTIC BOUNDS** — they assume a fill at the modeled price with zero slippage and zero commission. Real fills run below this, and commission on 10–12 lots is material.

**Model-quality disclosure:** my first pass solved IV from entry credit and repriced on the 5-min tape. It disagreed with OA's own high-water tracking — it claimed PT25 was reachable on 7/02 T00002 (OA: `mfe 0.00`) and on 6/09 T00152 (OA: `mfe 0.23`, just short of the 0.25 threshold). Flat-IV BS decays a 0DTE wing faster than the real market. **Every counterfactual above is therefore gated on OA's observed `mfe_pct`/`mae_pct`, not on the model.** The model is used only for shape and timing.

---

## Position log

### `2026-06-11 | shortcallspread | 7315/7320 | q12 | cr $1.05 | −$7,740 | R −1.633`
- **A) Exit:** PT25 → **NOT FIRED** — OA tracker recorded `45.7% high / $576 high`; Trades list has only `Open 11:01AM` + `Close 1:29PM`. No profit-taking order.
- **B) Hedge:** S2 → **FIRED** — Automation Log `Scalp-Mon-S2-StrikeTouch` @ 1:29PM, decision path confirmed, both legs closed 13:29.
- **C) Cause:** `settings` **[CONFIRMED]** — SmartPricing Market on the S2 close, filled $7.50 into a 0–7.5 quote on a $5-wide spread. *Ruled out:* by_design (not an unstopped control); cash settlement (loss came from the fill, not settlement); market_unfillable (it filled — that's the problem); filter gating (n/a); config staleness (config records the 6/14 Market→SmartPricing fix, so the record is right and 6/11 predates it). **Evidence that would change this verdict:** a broker-side confirm showing $7.50 was a real executable ask, which would move the excess from artifact to genuine slippage.
- **D) If declared logic worked:** S2 at a fair fill capped by structure = **−$4,740** (R −1.000), delta **+$3,000** — S2 fired on time; only the pricing was broken.
- **E) Best alternative:** **SL50 −$630** (R −0.133); runner-up SL75 −$945. *Preemption:* PT25 (+$315) is **excluded** — `mae_date 12:16` precedes `mfe_date 13:23`, so every SL fires before PT25 gets its chance. Naming PT25 here would be a preemption error.

### `2026-07-02 | shortputspread | 7445/7440 | q10 | cr $0.35 | −$1,950 | R −0.419`
- **A) Exit:** PT25 → **N/A** — `mfe_pct 0.00`; the position was never profitable for one minute. Correct non-fire. OA panel shows no profit high row, consistent.
- **B) Hedge:** S2 → **FIRED, correctly and fast** — first sub-7445 print in the 13:00 bar, both legs closed 13:02. Trade Details: SmartPricing Fast, bid/ask 2.2–2.4, ladder `$2.30 ✓ → $2.35 → $2.40`, order 021847315 filled $2.30. Textbook.
- **C) Cause:** `by_design` **[CONFIRMED]** — every declared rule did exactly what it was told. *Ruled out:* oa_execution (order generated and filled at the top of the ladder); market_unfillable (filled); settings (Fast pricing, as remediated); data_error (screenshot reconciles to the ledger to the dollar).
- **D) If declared logic worked:** **−$1,950** — it did work. Delta $0.
- **E) Best alternative:** **ride +$350** (R +0.075); runner-up SL50 −$175. *Preemption:* none — ride has no fire time to preempt. **This is the clean example of the S2 whipsaw: perfect execution, −$2,300 of value destroyed.**

### `2026-06-24 | shortputspread | 7360/7355 | q10 | cr $0.25 | −$1,950 | R −0.411`
- **A) Exit:** PT25 → **NOT FIRED** — OA tracker `40.0% high / $100 high` on Jun 24, threshold 25%, and the Trades list contains only `Open 11:08AM` + `Close 1:25PM`. **The single cleanest instance of the F2 failure.**
- **B) Hedge:** S2 → **FIRED** — both legs closed 13:25; Trade Details SmartPricing Fast, ladder `$2.20 ✓ → $2.30 → $2.40`, order 003138628 filled $2.20.
- **C) Cause:** `oa_execution` **[CONFIRMED no order generated; INFERRED vs `settings`]**. *Ruled out:* by_design (PT25 is the declared exit); cash settlement (intraday mid rule); market_unfillable (no order to fill, and at 40% profit the target was inside the market); filter gating (n/a); **config staleness NOT ruled out** — the panel is current settings. **Evidence that would change this verdict:** Automation Log on the `Open 10 contracts` row.
- **D) If declared logic worked:** **+$62** (R +0.013) — PT25 fill at $0.1875 around `mfe_date 11:30`. Delta **+$2,012**. *Optimistic bound.*
- **E) Best alternative:** **PT25 +$62**; runner-up ride −$1,530. *Preemption:* all four SL levels are **excluded** — `mfe_date 11:30` precedes `mae_date 13:25`, so PT25 fires first and no stop gets the chance.

### `2026-06-11 | shortcallspread | 7365/7370 | q11 | cr $1.25 | −$1,705 | R −0.413`
- **A) Exit:** PT25 → **NOT FIRED** — `mfe_pct 0.82` (82% of credit). Grossly past threshold.
- **B) Hedge:** S2 → **FIRED** — closed 13:43 with the paired put leg.
- **C) Cause:** `oa_execution` **[INFERRED]** — no Trades list supplied for this position, so the "no order generated" observation is extrapolated from the same-day sibling. *Ruled out:* by_design; market_unfillable (at 82% profit the target sat deep inside the market). **Evidence that would change this verdict:** Trades list for T00146.
- **D) If declared logic worked:** **+$344** (R +0.083), delta +$2,049. *Optimistic bound.*
- **E) Best alternative:** **PT50 +$688** (R +0.167); runner-up PT25 +$344. *Preemption:* SL50/75/100 excluded — `mfe_date 13:29` precedes `mae_date 13:42`. **Note S2 SAVED $2,420 here** (ride = −$4,125 max loss): 6/11 is a day where S2 earned its keep on one leg and the Market-order artifact destroyed the other.

### `2026-06-10 | shortputspread | 7280/7275 | q12 | cr $0.95 | −$1,620 | R −0.333`
- **A) Exit:** PT25 → **NOT FIRED** — `mfe_pct 0.58`.
- **B) Hedge:** S2 → **FIRED** — closed 15:16.
- **C) Cause:** `oa_execution` **[INFERRED]** — same basis as T00146. **Evidence that would change this verdict:** Trades list for T00149.
- **D) If declared logic worked:** **+$285** (R +0.059), delta +$1,905. *Optimistic bound.*
- **E) Best alternative:** **PT50 +$570** (R +0.117); runner-up PT25 +$285. *Preemption:* SL50/75/100 excluded (`mfe_date 14:05` before `mae_date 15:16`). **S2 saved $3,240 here** — ride was max loss.

### `2026-06-09 | shortputspread | 7335/7330 | q11 | cr $0.65 | −$2,255 | R −0.471`
- **A) Exit:** PT25 → **N/A** — `mfe_pct 0.23`, genuinely short of the 0.25 threshold. Correct non-fire. *(My BS model wrongly claimed this one fired; OA's tracker overrules it.)*
- **B) Hedge:** S2 → **FIRED** — closed 11:29 on a touch of 7335 (SPX day low 7237.85).
- **C) Cause:** `by_design` **[INFERRED]** — all rules behaved. *Ruled out:* oa_execution (nothing was due to fire); market_unfillable. **Evidence that would change this verdict:** Trades list for the 11:29 close showing an unfilled PT order, which would move `mfe` interpretation.
- **D) If declared logic worked:** **−$2,255** — it did. Delta $0.
- **E) Best alternative:** **ride +$715** (R +0.149); runner-up SL50 −$358. Second clean S2 whipsaw: SPX closed 7386.65, well above the 7335 short put.

### `2026-06-08 | shortputspread | 7385/7380 | q11 | cr $0.55 | −$55 | R −0.011`
- **A) Exit:** PT25 → **N/A** — `mfe_pct 0.15`, below threshold.
- **B) Hedge:** S2 → **NOT FIRED** — no touch; SPX low that window well above 7385.
- **C) Cause:** `settings` **[CONFIRMED]** — `Scalp-Mon-S2-Cleanup` (open ≥2 min + exactly 1 open position → close). Opened 11:31:01, closed 11:33:02 — exactly 2 minutes, matching the gate. A call spread opened 11:33:03, total went to 2, and the churn stopped immediately. **This position is the natural experiment that identifies the mechanism.**
- **D) If declared logic worked:** no declared rule was due to fire; **−$55** stands.
- **E) Best alternative:** **ride +$605** (R +0.124). No preemption.

### `2026-07-01 chain | shortputspread ×6 losers | q10 | −$350 combined`
`T00030 −$100 (R −0.021) · T00023 −$50 · T00024 −$50 · T00025 −$50 · T00027 −$50 · T00029 −$50 (each R −0.010)`
- **A) Exit:** PT25 → **NOT FIRED** — three have `mfe_pct 0.00`; five closed at a loss.
- **B) Hedge:** S2 → **NOT FIRED** — no strike was within 40 points of SPX at any point (5-min tape verified, see F3).
- **C) Cause:** `settings` **[CONFIRMED]** — `Scalp-Mon-S2-Cleanup` closing unpaired legs (logs at 11:12AM and 11:27AM) racing `Scalp-Scan-Put`'s own-side re-entry gate, with no interlock. Closes are tagged **Market** (F6). *Ruled out:* by_design; cash settlement; market_unfillable (all filled); filter gating (Range075 passed on all ten); oa_execution (every automation behaved as configured). **Note T00029 also carries a 33.3% profit high with no PT order — it is simultaneously an F2 instance.**
- **D) If declared logic worked:** no declared rule was due to fire on any of them.
- **E) Best alternative:** **ride** — +$100 to +$150 each, **+$800 for the chain** vs −$250 actual. No preemption (nothing else fires).

---

## Open evidence requests

**Resolved 2026-07-27** — Exit Options editor (F2 → CONFIRMED) · `Scalp-Mon-S2-Cleanup` logs ×2 (F3 → CONFIRMED) · `Scalp-Scan-Call` editor (corrected the F3 attribution) · `Scalp-Scan-Put` log (F3b). **Bot 1 no longer has a blocking evidence gap.**

Remaining, in priority order — none of these block the verdict:

1. **Why `Scalp-Scan-Call` never fired on 7/01.** The `Open SPX Short Call Spread` action's opportunity filters (min credit / delta / bid-ask), or a `Scalp-Scan-Call` log from 7/01 showing where it exited the tree. Determines whether the orphan loop is a rare tape accident or a recurring thin-credit failure mode.
2. **Trades lists for `2026-06-10 T00149` (`mfe 0.58`) and `2026-06-11 T00146` (`mfe 0.82`).** These two remain INFERRED rather than CONFIRMED purely because I have not seen their order rows. The bot-wide mechanism is confirmed; these would close the last two individual cases.
3. **OA's automation change-history for `Scalp-Scan-Put`.** Closes the one residual caveat on F2 — that the Exit Options editor shows today's config, not 6/24's.
4. **Trades list for any one of the 24 ride-to-expiry winners** (e.g. 6/12, credit $0.85). Would convert the strongest corroboration from ledger inference to order-level evidence.

## Fleet-level running table

| Bot | Verdict | Confirmed execution failures | $ recoverable | $ explained by strategy |
|---|---|---|---|---|
| **IC-SPX-FastPT25-S2** (post-fix) | **Execution-broken** — PT25 dead; entry, S2 firing + scanner gates clean | **PT25 non-firing (CONFIRMED, bot-wide)** · orphan-loop race (CONFIRMED) · Market-pricing on Cleanup (CONFIRMED, unremediated) · 1 structural artifact | **$3,000** artifact (not a real loss) · **+$11,922** net if PT25 executed *(optimistic bound; includes −$8,854 winner give-back, and off-tick targets make it optimistic again)* · **$305** orphan-loop churn | **−$3,285** S2 whipsaw cost — a real strategy result, not an execution failure |
| QQQ-IC-0DTE-Range075-PT50-Wide2-1230PM | *not started* | — | — | — |
| QQQ-IC-0DTE-HedgeD-Conditional | *not started* | — | — | — |
| DIR-SPX-PutVIX22-SL75 | *not started* | — | — | — |

---

### Data provenance
Ledger `data/trades.csv` (2026-07-02). SPX 5-min tape and daily OHLC via Tradier `/v1/markets/timesales` + `/v1/markets/history`; expired-option daily OHLC via `/v1/markets/history` on OCC symbols (7445P settled $0.05, 7440P $0.03 on 7/02 — confirms the F5 correction). OA screenshots supplied by operator 2026-07-27: Position Details + Trade Details for T00002, T00095, T00147; `Scalp-Mon-S2-StrikeTouch` close log (Jun 11); `Scalp-Scan-Put` open log (Jun 24 11:08AM); **Exit Options editor**; **`Scalp-Mon-S2-Cleanup` logs (Jul 1 11:12AM, 11:27AM)**; **`Scalp-Scan-Call` automation editor**; Position Details 7/01 T00029. `data/hedge_tournament.csv` contributed **nothing** — its 278 rows for this bot cover 15 winning condor-ids only, because the tournament ran on the expired-leg subset.
