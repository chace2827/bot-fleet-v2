# DIR-SPX-PutVIX22-SL75 — Execution Forensic

*Audit date 2026-07-27 · ledger current to 2026-07-02 · VIX verified through 2026-07-27*

**Declared:** exit = PT100 | hedge = SL75 | entry = 11:00, **VIX ≥ 22**, long put debit spread, long ~ATM / short $15 below, $15 wide, 1 contract/day, no re-entry | sizing = paper $10k, 1 ct

**Ledger:** **0 positions**, 0 losses, P/L $0, Exp(R) n/a. Live on paper since 2026-06-25 → 6 trading days in the ledger, **22 trading days as of today**.

**Verdict:** **Execution-clean by the only test available — and that test proved nothing.** [Non-trading fully explained: `filter gating`, CONFIRMED. Bot health: **UNVERIFIED and currently unverifiable**.] The bot has not fired because its entry condition has not once been true. It has also not been tested.

---

## Why no entries fired — CONFIRMED

The gate is `VIX ≥ 22`. VIX daily bars from Tradier, every trading day since the bot went live:

| Window | Days | Max VIX **high** | Days with high ≥ 22 |
|---|---|---|---|
| Ledger window 6/25 → 7/02 | 6 | **20.72** (6/26) | **0** |
| Post-ledger 7/06 → 7/27 | 16 | **20.31** (7/23) | **0** |
| **Total since going live** | **22** | **20.72** | **0** |

The **daily high** is a strict upper bound on the VIX level at any 11:00 scan. It never reached 22 on any of the 22 days — the closest approach was 20.72, a full 1.28 points short. The gate could not have passed. **Zero positions is the correct and only possible output.**

**Cause: `filter gating` [CONFIRMED].** Benign explanations ruled out:
- *by_design* — yes, precisely: this is the design working.
- *cash settlement* — n/a, no position existed.
- *market_unfillable* — n/a, no order was ever generated to fill.
- *config-record staleness* — `bots_meta` and `bots_config` agree on VIX ≥ 22, and the sibling `DIR-SPX-Put-Control` is documented as *"only diff = VIX condition removed"* and traded on 5 of the 6 ledger days. The gate is the sole difference and it is the sole explanation.
- *oa_execution* — no platform failure is needed to explain the observation, and none may be inferred from it.

No probability model is required here. The observation is direct: the condition was never met.

---

## The finding that actually matters

### The forward test has produced zero information about this bot
`current-state.md` states the paper deployment is *"forward-mechanics only"* and that the *"OOS holdout still gates LIVE CAPITAL."* After 22 trading days, the forward-mechanics test **has not run a single time**. Not the entry, not PT100, not SL75, not the 1-contract sizing, not the exit pricing.

Worse — and this is the part to be adversarial about:

> **A correctly-gated bot and a switched-off bot emit identical evidence when the gate never passes.**

Both produce zero positions. I therefore **cannot confirm this bot is operational.** The `bots_meta` note for its sibling `CallVIXdrop` carries the warning *"⚠️ Confirm AUTOMATIONS toggled ON (was OFF at creation)"* — the same failure mode is live and unfalsified here. `DIR-SPX-Put-Control` firing proves nothing about this bot; it is a **separate bot object** with its own automation toggles.

**Evidence that would change this verdict:** the bot's OA page showing its automations toggled ON, or any log entry showing `Scalp`-equivalent scan cycles executing and exiting the tree at the VIX node. A scanner that runs and correctly answers "No" leaves a trace; a scanner that never runs does not.

### How long should you expect to wait?
| Base-rate window | Trading days | VIX open ≥ 22 | Rate |
|---|---|---|---|
| 2024-01 → now | 643 | 79 | 12.3% |
| 2025-01 → now | 391 | 69 | 17.6% |
| 2026-01 → now | 141 | 25 | 17.7% |

At an unconditional 17.6%, a 22-day drought is a **1.4%** event — which looks alarming until you remember volatility is strongly autocorrelated. The market has sat in a 15–21 VIX regime for two straight months; *conditional* on that regime, 22 quiet days is entirely ordinary. **The unconditional base rate is the wrong model here** and I flag it only to head off the reading that 1.4% implies something is broken. The direct observation (max high 20.72) is dispositive and needs no model.

Practical consequence: at ~17% of days, expect roughly **one fire every 6 trading days** once a normal-vol regime returns — but the strategy is explicitly a high-vol engine, so its fires will arrive in clusters, not on a schedule. Accumulating a meaningful forward sample will take months, not weeks.

### The A/B is accumulating evidence only on the arm you don't care about
`DIR-SPX-Put-Control` — the arm documented as *"MEANT to lose"* — has 5 trades and −$1,045. The champion arm has 0. The pair was deployed to compare them; so far only the loser is generating data. That is expected given the gate, but it means the comparison cannot begin until vol returns.

### One genuinely useful cross-bot inference — with an explicit caveat
The control bot shares the champion's **PT100 / SL75** exit configuration. Its exits reconcile to those rules almost exactly:

| Date | Entry debit | SL75 → exit at 25% of debit | PT100 → exit at 2× debit | Actual exit | Reads as |
|---|---|---|---|---|---|
| 6/26 | $5.20 | $1.30 | — | $1.05 | SL75 + slippage |
| 6/29 | $5.65 | $1.41 | — | $1.30 | SL75 + slippage |
| 6/30 | $5.25 | $1.31 | — | $1.25 | SL75 |
| 7/01 | $4.60 | $1.15 | — | $1.10 | SL75 |
| **7/02** | **$5.55** | $1.39 | **$11.10** | **$11.10** | **PT100 — exact** |

The 7/02 exit is $11.10 against a modelled PT100 of exactly $11.10. **Both declared exit mechanics are demonstrably expressible and executing in this bot family** — a direct contrast with Bot 1, where PT25 was attached and generated no orders at all.

**Caveat, stated plainly:** this is the *control* bot. It is evidence that the PT100/SL75 configuration works when built this way; it is **not** evidence that `DIR-SPX-PutVIX22-SL75`'s own copy is attached, armed, or toggled on. Do not let it stand in for the verification the champion arm still needs.

---

## Position log
**None.** Zero positions exist, so the A–E per-position schema has no subject. No rows are appended to `data/execution_audit.csv` for this bot.

---

## Open evidence requests
1. **The bot's OA page showing automations toggled ON.** The only thing standing between "correctly gated" and "silently off." Cheap to check, and it is the difference between a bot that will fire when vol returns and one that will not.
2. **Any scan-cycle log entry** showing the automation running and exiting at the VIX decision node with `No`. Positive proof of life.
3. Whether a **VIX-based paper drill** is worth running — e.g. temporarily cloning the bot with a VIX ≥ 16 gate purely to exercise entry → PT100 → SL75 once, then discarding it. **I am not recommending this**; it is a config change and belongs in a pre-registered test, not a forensic. Flagging it because "wait for vol" may mean waiting a quarter to learn whether the bot works at all.

---

## Fleet-level running table

| Bot | Verdict | Confirmed execution failures | $ recoverable | $ explained by strategy |
|---|---|---|---|---|
| **IC-SPX-FastPT25-S2** (post-fix) | **Execution-broken** — PT25 dead; entry, S2 firing + scanner gates clean | PT25 non-firing (CONFIRMED, bot-wide) · orphan-loop race (CONFIRMED) · Market-pricing on Cleanup (CONFIRMED, unremediated) · 1 structural artifact | $3,000 artifact (not a real loss) · +$11,922 net if PT25 executed *(optimistic bound)* · $305 orphan-loop churn | −$3,285 S2 whipsaw cost |
| **DIR-SPX-PutVIX22-SL75** | **Clean but untested** — non-trading fully explained; bot health unverified | **0** | **$0** | **$0** — nothing traded, nothing lost, nothing learned |
| QQQ-IC-0DTE-Range075-PT50-Wide2-1230PM | *not started* | — | — | — |
| QQQ-IC-0DTE-HedgeD-Conditional | *blocked — declared exit is blank in config* | — | — | — |

---

### Data provenance
VIX daily OHLC 2024-01-01 → 2026-07-27 via Tradier `/v1/markets/history` (plain ticker `VIX`). Ledger `data/trades.csv` (2026-07-02). Config from `data/bots_config.csv` + `data/bots_meta.csv`. Control-bot exit reconciliation computed from ledger entry debits against declared PT100/SL75 thresholds.
