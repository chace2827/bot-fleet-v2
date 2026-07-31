# Daily Review — Design

*Written 2026-07-29 · design only, nothing built yet · depends on `docs/oa-capture-coverage-2026-07-29.md` for what the input files can and cannot carry*

**Status: PROPOSED.** No code, no schedule, no commitment. Tier 0 is testable today with zero infrastructure.

---

## The framing that makes this worth doing

The daily review is **a data collection ritual that produces a report as a byproduct** — not a report.

`approach-reset-2026-07-29.md` §4.3 already makes this argument about the forensic audit: *"a one-shot forensic decays the moment it's written. A nightly script keeps paying."* The same trap applies here. A daily review that produces 250 beautiful standalone analyses and accumulates nothing is the audit's mistake repeated at higher frequency.

So every design decision below is subordinate to one rule: **each day must append machine-readable rows to a ledger.** Today's report is the receipt. The ledger is the asset.

---

## 1. Split "did the bot do its job" into three questions

These get conflated constantly, and separating them is most of the value.

| Question | What it asks | Answerable from |
|---|---|---|
| **Did it fire?** | Should it have entered, and did it, at the right time? | Tag capture + C1 regime inputs |
| **Did its mechanics execute?** | Did every declared exit actually generate an order? | Tag capture (status, exit times) |
| **Was the strategy right for the tape?** | Given it ran correctly, was the bet good? | Counterfactual replay |

A bot can lose money with all three clean. A bot can make money with all three broken — that is `IC-SPX-FastPT25-S2`'s entire story. Every daily review answers these **separately** and must refuse to blend them into a single verdict.

---

## 2. The counterfactual engine

For each position the tag capture gives entry time, strikes, width, exit time, P/L, ROR. Against that, replay a **fixed** policy panel every day:

- Hold to expiry
- PT at 25 / 50 / 75% of credit
- Time exit at 14:00 / 15:00 / 15:50
- Stop at 1x / 2x credit
- Breach response: immediate / $1 ITM / sustained 10 min
- No hedge at all

The panel must not change day to day, or the accumulated ledger becomes uncomparable.

### Cost tiers — these are not equal

**Exact, from data already held**
- *Hold-to-expiry* is fully determined by settle vs. strikes. No model.
- *"Would PT50 have fired?"* is answerable from `mfe_pct >= 0.50` in the ledger. No model.

These two alone cover Patterns A and B. **Start here.**

**Approximate, needs modelling**
- Time-exit and stop counterfactuals need an option price at an arbitrary minute. For 0DTE this is reconstructable from underlying + IV, but label it approximate and **never let an approximate counterfactual drive a config decision on its own.**

### The output that matters is not today's

Each day appends one row per policy to `data/counterfactual_ledger.csv`. After 30 days: *"PT50 beat actual on 22 of 30 days, median +$340."* A real finding, built by accumulation, at zero marginal effort per day.

---

## 3. The chart

Two stacked panels, per bot per day.

**Top — the tape.** Underlying 1-min line (Tradier). Short put and short call strikes as horizontal bands, profit zone between them shaded. Entry marker, exit marker. A vertical rule at each counterfactual exit time, so the reader literally sees *"here is where PT50 would have closed it, here is where it actually closed."* Annotate the MFE point: *peak +87% at 13:42*.

**Bottom — position value over time.** Actual P/L path with counterfactual exit points marked on it. **The gap between the actual exit and the best counterfactual exit is the day's recoverable value, drawn to scale.**

Fleet-specific: add a marker at 11:01. When entry deviates from it, that should be visually obvious rather than buried in a table.

---

## 4. Two sections that keep the review honest

**A prosecution section, every day.** The failure mode of daily review is attachment — look at a bot 40 days running and you start rationalising. Every report ends with a fixed section arguing the bot should be switched off, restating the pre-registered kill criterion and where the bot stands against it. Not optional. Not skipped on good days. This operationalises `approach-reset-2026-07-29.md` §3.3 Rule 2.

**Permission to be boring.** Most days should conclude *"bot fired at 11:01, PT50 executed both sides, exited as designed, nothing to do."* If every daily review surfaces something interesting, it is generating false positives and will stop being trusted within two weeks. Build in an explicit `NO FINDINGS` verdict and let it be the common case.

---

## 5. What each day should accumulate regardless

Free riders on a process that is running anyway:

- **Morning ATM IV vs. realised range** — builds live evidence for the C1 gate already validated on 956 days, one row per day
- **Duplicate-arm check** — flag any two positions with identical P/L *and* identical entry minute. This is how `HedgeA-S1` ≈ `HedgeD` would have surfaced on day one
- **Expired vs. Closed ratio per bot** — a bot whose positions start expiring instead of closing is a mechanic that stopped firing. This is the `QQQ-IC-0DTE-Fortress` regression signature, and it is a one-line check

---

## 6. Automation path

The analysis automates cleanly. **The capture is the bottleneck.**

| Tier | What runs | Effort |
|---|---|---|
| **0 — today** | Upload tag files to a chat, Claude produces chart + three verdicts | Zero infrastructure. Works now. |
| **1** | Scheduled task weekdays ~17:30 ET: read captures from the repo, pull Tradier bars, write report, append ledger | Everything after the capture is unattended |
| **2** | Remove the manual capture step | See below |

**Three routes past the capture bottleneck:**
1. Keep clicking the bookmarklet — ~2 min/day, and honestly fine
2. `Export Data` CSV, *if* it carries a bot column (see `oa-capture-coverage-2026-07-29.md` §4 — this check has not been done and removes the tag-filtering requirement entirely)
3. Drive it with Claude-in-Chrome for genuinely zero-touch

---

## 7. Output form

**One persisted artifact that updates daily**, not 250 separate files. A day selector, the chart, the three verdicts, and a cumulative counterfactual scoreboard that gets more valuable every day.

The thing opened each evening is then the same object, and its top section is always *"what the last 30 days say"* — not *"what happened yesterday."*

---

## Open items

1. Does `Export Data` include a bot-name column? (10 min, unblocks Tier 2 route 2)
2. Which tag scheme maps 1:1 to bots? The tag capture's usefulness depends entirely on this
3. Where does intraday underlying data come from — Tradier live pull, or the VPS recorder at 149.28.47.235 once re-set-up?
4. Counterfactual option pricing: accept Black-Scholes reconstruction, or restrict permanently to the two exact counterfactuals?
