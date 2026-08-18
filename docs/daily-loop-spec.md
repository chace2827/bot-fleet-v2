# Daily loop — the contract

*Written 2026-07-31 for Bot Fleet v2. **MERGE** of the archive's `daily-brief-spec.md` (the
render conventions) and `daily-review-design-2026-07-29.md` (the accumulation discipline and
the three-verdict split). Supersedes both. Neither archive file is a v2 input.*

> **What survived the merge:** the tape chart, the marker convention, the regime read, the
> instruction-mirror card, the hedge clinic, the cumulative threads, the daily-ops conventions.
> **What did not:** the single blended green/amber/red grade, and the whole compliance-scoring
> layer. Both are replaced — by the three-verdict split (§2) and the drift detector (§5).
> **Why:** G5 scored 100% instruction-compliance on five consecutive days while the champion's
> profit target had been dead for a month. It was scoring fidelity to a record, and the record
> was false. A grading scheme that can do that is not a weak grading scheme; it is a hazard.

---

## 0. The framing that makes this worth doing

**The daily loop is a data-collection ritual that produces a report as a byproduct — not a
report.**

A one-shot forensic decays the moment it is written; a nightly script keeps paying. The same
trap applies at higher frequency: a loop that produces 250 beautiful standalone analyses and
accumulates nothing is the audit's mistake, repeated daily.

Every design decision below is subordinate to one rule:

> **Each day must append machine-readable rows to a ledger. Today's report is the receipt. The
> ledger is the asset.**

Three consequences, all load-bearing:

- **The fixed panel never changes.** Counterfactual policies, detector rules and their
  thresholds are frozen inputs. Change one and the accumulated ledger becomes uncomparable —
  which silently destroys every day already banked. Version and re-baseline instead
  (`execution_audit.py` is frozen at v1.0.0, sha `fdc43d0dcb7275560069048e62d897f528d9620b5a6be87de7a410fae1851e2d`, precisely for this).
- **NO FINDINGS is the goal, not a failure.** If every review surfaces something interesting it
  is generating false positives and will stop being read inside two weeks.
- **The loop is worthless if the fleet is off.** Its entire value is making the next stretch
  trustworthy.

---

## 1. Trigger, inputs, and the two modes

### 1.1 LIVE mode — each trading day, ~17:30 ET

Andy provides two things and one line of context:

1. **OA Export Data CSV**, all bot groups selected → `data/raw/YYYY-MM-DD.csv`.
2. **Bookmarklet capture** of `/bots`, plus **toggle screenshots** (`AUTOMATIONS` and
   `EXIT OPTIONS`) for anything that changed.
3. One line: the trading date, and anything unusual — outage, manual override, skipped day.

> ⚠️ **THE EXPORT RESPECTS THE BOT-GROUP FILTER.** An export taken with any group deselected is
> a subset, and rebuilding from it would erase the excluded bots' history. `build_ledger.py`
> carries a filtered-export guard that compares against the prior ledger and warns loudly — but
> the guard only catches bots that already existed. **Select all groups.**

Then `scripts/daily.sh` runs the nine stages (§4), and Claude renders §6 from the brief JSON.

### 1.2 CONFIG-DRIFT mode — weekly, while the account is inactive

No positions, so no tape, no counterfactuals, no verdicts. The loop still runs weekly on the
**capture** alone: diff this week's `/bots` capture against the last one and report field-level
changes. That is the only thing that can drift while nothing trades — and edits made while
inactive **do persist** (verified 7/29→7/30), so drift is real in this mode.

**This is the mode the fleet is in today.** It stays here until Day-0.

---

## 2. Three verdicts, never blended

This is the spine of the whole document. The three questions get conflated constantly and
separating them is most of the value.

| Verdict | The question | Answerable from |
|---|---|---|
| **FIRE** | Should it have entered, and did it, at the right time? | Capture + regime inputs + bot logs |
| **MECHANICS** | Did every declared exit actually generate an order? | **The position's Trades list** |
| **STRATEGY** | Given it ran correctly, was the bet good? | Counterfactual replay (§7) |

**A bot can lose money with all three clean. A bot can make money with all three broken** — that
is `IC-SPX-FastPT25-S2`'s entire story. Every review answers these **separately** and must
refuse to collapse them into one grade.

**Each verdict carries its own status,** and they do not average:

- 🟢 **GREEN** — behaved as designed on that axis.
- 🟡 **AMBER** — correct process, bad outcome (a "good loss"), or a borderline call.
- 🔴 **RED** — a deviation on that axis. Emits an instruction card (§8).
- ⬜ **NOT EVALUABLE** — the evidence to judge it does not exist. **Never a pass.** Say which
  artifact is missing.

> ### ⛔ THE EXIT OPTIONS PANEL IS NOT EVIDENCE
> Exit Options are copied onto a position **at open**; the panel renders the automation's
> *current* settings, which can diverge from every live position silently and indefinitely.
> **MECHANICS is answered by the Trades list or it is NOT EVALUABLE.** There is no third option
> and no exception. See `oa-platform-reference.md` §0.3.

---

## 3. Post-cutover only, and n=0 for a while

Everything the loop reads comes from the **post-cutover working ledger**. The v1 era is frozen
in `data/archive/` and is never an input (`build-plan.md` §3).

Practical consequences to state in the brief rather than let a reader discover:

- **Every bot restarts at n=0 on Day-0.** For the first weeks the standings tables are empty by
  construction. An absent number is not a zero, and a blank expectancy is not a flat one.
- **No cross-era pooling, ever** — not for a bot, not for the fleet, not "just for context."
- **Straddlers** (opened pre-cutover, closing after) resolve to `data/straddlers.csv` and the
  mirror baseline layer. They appear in **no** report. If someone wants them they must look
  deliberately, which is the point.
- **The one exception is mirror funding**, which reads `data/mirror_baseline.csv` — a one-time
  frozen snapshot, nine rows, written once, never recomputed.

---

## 4. The pipeline — nine stages, order matters

`scripts/daily.sh [YYYY-MM-DD]`

| # | Stage | Produces |
|---|---|---|
| 1 | `build_ledger.py` | `trades.csv` · `bots.csv` · `straddlers.csv` · `ledger_meta.json` |
| 2 | `tape.py` | `data/brief/<date>_tape.json` |
| 3 | **`execution_audit.py`** | `data/execution_audit_findings.csv` + `_meta.json` |
| 4 | `daily_brief.py` | `data/brief/<date>_brief.json` · `compliance.csv` |
| 5 | `should_have_fired.py` | `data/brief/<date>_p3_verdicts.tsv` |
| 6 | `hedge_tournament.py` | `data/hedge_tournament.csv` |
| 7 | `trade_window.py` | `data/trade_window.csv` |
| 8 | `lessons.py` | `data/lessons.csv` |
| 9 | `report.py` | `STATUS.md` · `dashboard.html` |

**The drift audit runs at stage 3 — before the brief, not after.** The brief's job is to render
verdicts; the detector's job is to find the facts those verdicts rest on. Reversed, the brief
would render a clean day and the detector would contradict it afterwards.

**Every stage degrades gracefully at n=0.** Verified 2026-07-30; four defects were found and
fixed getting there, two of them destructive. That property is a test, not an accident —
re-check it if any stage changes.

**Stage 1 refuses to run without `LEDGER_START`.** This is deliberate: a ledger with no cutover
is a contaminated ledger, and the whole run stops rather than produce one.

---

## 5. The drift detector — what stage 3 contributes

`execution_audit.py` v1.0.0 (frozen; sha `fdc43d0dcb7275560069048e62d897f528d9620b5a6be87de7a410fae1851e2d`). It is a **detector, not a judge**:
it never assigns a cause, and every finding carries a **`verify_by`** field naming the artifact
that closes it.

**Its findings map straight onto the verdicts.** Each rule declares its axis — FIRE or
MECHANICS — and **no rule is on the STRATEGY axis**. Strategy belongs to the counterfactual
engine (§7). Mixing them is the failure this document exists to prevent.

**Tier S (structural, config-free — always runs):** `IMPOSSIBLE_FILL` · `RISK_INTEGRITY` ·
`RISK_MISMATCH` / `RISK_UNWITNESSED` · `FILL_WORSE_THAN_MAE` · `NEVER_IN_PROFIT` ·
`CLOSED_AT_MAE` · `EXPIRY_RATIO_FLIP` · `DUPLICATE_ARM` · `SILENT_BOT`.

**Tier C (needs `data/bots_config_v2.csv`):** `PT_DECLARED_NOT_TAKEN` · `PT_NEVER_FIRES` ·
`TIME_EXIT_MISSED` · `REMOVED_EXIT_FIRED` · `BACKSTOP_CAUGHT_IT`.

**Without that config, Tier C reports SKIPPED with a reason — never silence.** A detector that
answers "no findings" while structurally blind is worse than no detector, and the brief must
carry the SKIPPED list into §6 so the blind spot is visible on the page.

Three rules worth naming because they encode expensive lessons:

- **`SILENT_BOT` can never be RED.** A correctly-gated bot and a switched-off bot are
  indistinguishable from position data. `DIR-SPX-PutVIX22-SL75` is the standing proof — 0
  positions in 22 days because its VIX≥22 gate correctly never fired. **Only the bot logs close
  it:** a scanner run with no entry is GREEN; zero log rows is RED.
- **`EXPIRY_RATIO_FLIP`** catches an exit engine that stopped generating orders. Run over the
  archive it independently dates the champion's death to **2026-06-01** and both Fortress bots
  to **2026-06-12**, and names the trade_id whose Trades list settles it.
- **`BACKSTOP_CAUGHT_IT`** fires when a position closes between the Exit-Options time exit and
  the AUTOMATIONS backstop. **Nothing is lost that day** — which is exactly why it would
  otherwise go unnoticed for six sessions, as it did.

---

## 6. The brief — fixed running order

Same skeleton every day, so days are comparable. Sections that have nothing to say say so in
one line rather than being dropped.

### §0 · Since yesterday
Fleet P/L delta, gate progress, standings moves — **and grade yesterday's "tomorrow's watch."**
Did the forecast play out? This makes the brief a chain rather than a snapshot, and it builds
forecasting discipline by scoring it.

### §1 · The tape — one chart per traded underlying
- One intraday chart per underlying with ON 0DTE bots.
- **Y axis = % change from prior close**, gridlines every 0.25%, range ~±1.0%. This is the axis
  that matters: it makes the **Range075 ±0.75% GO zone a shaded band**, so whether price — and
  each entry — sat inside the filter is visible at a glance.
- **Marker convention: colour = the bot, shape = what fired.** One categorical hue per bot
  (coral / teal / purple / amber — never green/red, never the price line's blue).
  **● entry** · **◆ defensive exit** (hedge / stop / defang) · **▪ profit-target exit**
  (collapse a swarm to one marker with `×N`) · **no exit mark = held to expiry**.
  > The teaching payoff is in the **absent** mark: a losing bot with no diamond is a missing
  > hedge made visible; a winning bot with no mark was never threatened.
- **Legend = one descriptive row per bot:** swatch · name · WIN/LOSS + P/L · one sentence on
  *why* — where it entered relative to the zone, what the hedge did.
- **Never mix underlyings.** Only that underlying's bots route onto its chart.
- **Intraday tape is for 0DTE bots only.** Multi-day positions are tracked by lifecycle (days
  held, MTM trend, distance to profit/stop), not charted 9:30–4:00.
- **SPX-vs-QQQ divergence line** — when one trends while the other ranges, flag which sleeve is
  about to get stressed.

### §2 · The read — quantified regime
Numbers with a teaching tag, not vibes: % move today · gap % · realized range % · net move % ·
**directionality ratio** (|net move| ÷ path length; low = chop, high = trend) · direction
changes · % of session above/below open → **regime label** `Chop` / `Drift` / `Trend`, with the
number behind it and one line on what it means for IC vs Directional.

Tape source is stated every day: `tradier` or `reconstructed`. Reconstructed high/low is an
approximation and any breach flag resting on it is labelled `approx`.

### §3 · Expected behaviour — who *should* have fired
For each ON bot, derived from today's regime and its **declared** config: GO / NO-GO per its
filter · which side should be stressed · should its hedge have triggered. This makes each bot's
purpose explicit daily, which is the core learning mechanic — and it is the baseline the FIRE
verdict is scored against.

### §4 · Per-bot review — the instruction-mirror card
One card per ON bot, built on the skeleton of **its own config**, one row per instruction:

**Filter → Entry → Profit target → Hedge → Re-entry → Verdict**

Each row shows **declared vs actual**, flagged ✓ or ⚠. Same skeleton for every bot so cards are
directly comparable. **A missing capability gets its own row** — an unstopped bot shows
"Hedge: none → no cut → rode to expiry", and the absent row *is* the lesson.

**The Verdict row carries all three verdicts separately** (§2), never one blended grade, plus
the day's single lesson. Pair each card with the per-leg breach lines from §1 — short/long
strike · BREACH / NO BREACH · hedge applied.

> **Card rows are built from `data/bots_config_v2.csv`, which is written from capture — never
> from memory, and never from the archived `bots_config.csv`.** Without v2 config,
> `daily_brief.py` runs **CONFIG-BLIND and grades nothing**, and says so on the page. That is
> correct behaviour: grading against a record that does not exist is what produced the false
> 100%.

### §5 · Hedge clinic
For every breach or touch: did a hedge exist · did it fire · did it **help** (capped a loss) or
**hurt** (locked a loss that would have recovered)? Flag naked / uncapped losses as candidate
hedge sites and map them to the library in `hedge-research.md`.

**Convexity watch:** long-vol is the acknowledged gap. Each day a cheap long-put or long-vol
overlay would have paid, log it — the empirical case gets built by accumulation.

### §6 · Educational layer
**What you learned** — one durable lesson, pattern-detected from full post-cutover history.
**Counterfactual** — the exact arms only (§7), plus any live A/B.
**Micro-concept** — one rotating idea in two lines, so knowledge compounds.

### §7 · Cumulative threads
Story-so-far · open-questions ledger (open / advanced / answered-today) · rolling windows
(5-day regime mix, last-10 WR, gap trend, streaks) · **kill-trigger proximity** (§9).

### §8 · The prosecution section — every day, no exceptions
A fixed section arguing the bot should be switched off: restate its **pre-registered kill
criterion** and where it stands against it.

> Not optional. **Not skipped on good days.** The failure mode of daily review is attachment —
> look at a bot for 40 days and you start rationalising. This is the countermeasure and it only
> works if it is unconditional.

### §9 · Tomorrow's watch
What to look for next session — FOMC, day-of-week effects, a likely NO-GO. Graded in §0
tomorrow, closing the chain.

---

## 7. The counterfactual engine — and its cost tiers

A **fixed** policy panel replayed against every position, every day: hold-to-expiry · PT at
25 / 50 / 75% of credit · time exit at 14:00 / 15:00 / 15:50 · stop at 1× / 2× credit · breach
response · no hedge at all.

**The panel must not change day to day**, or the accumulated ledger becomes uncomparable.

### Two tiers, and they are not equal

**EXACT — from data already held. Start and stay here.**
- *Hold-to-expiry* is fully determined by settle vs strikes. No model.
- *"Would PT50 have fired?"* is answerable from `mfe_pct >= 0.50`. No model.

**APPROXIMATE — needs modelling.** Time-exit and stop counterfactuals need an option price at
an arbitrary minute. For 0DTE that is reconstructable, but **label it `approx` and never let an
approximate counterfactual drive a config decision on its own.**

### Correctness rules, non-negotiable

- **MFE/MAE are path extremes, not fill guarantees.** "Would have booked ±X%" assumes the
  threshold *filled* at the threshold. **The whole engine is an optimistic bound, never a live
  estimate.** Do not present its numbers as achievable P/L.
- **Order resolution:** if a position breached both a PT and an SL intraday, use the MFE/MAE
  **timestamps** to decide which fired first. That is why the ledger carries them. Do not assume.
- **Compare by R, never $, never win rate.**
- **Real positions only** — counterfactual on *exits*, never entries. No lookahead, no invented
  trades.
- **Unit test:** the ride arm reconciles against the ledger's expired-position P/L **to the
  dollar**, every run.

**The output that matters is not today's.** Each day appends one row per policy. After 30 days:
*"PT50 beat actual on 22 of 30 days, median +$340."* A real finding, built by accumulation, at
zero marginal daily effort.

---

## 8. Instruction cards — how a RED becomes an action

**Claude detects, instructs, and executes: Claude makes every OA edit directly, self-verified
before being marked done** — a fresh screenshot/capture re-observation of the changed value, plus
the Trades-list behavioral check (`CLAUDE.md` §5, `oa-ops-runbook.md` §4). *Amended 2026-08-04, at
Andy's explicit instruction — supersedes "Andy makes every OA edit."* No exceptions, no edit
reported done without both proofs.

Every RED emits one card:

```
RED · <VERDICT AXIS> · <bot>            <date> · <trade_id>
WHAT           one sentence, mechanical, no cause attributed
OBSERVED       the number, with its threshold
VERIFY BY      the exact artifact that settles it (almost always the Trades list)
IF CONFIRMED   the specific OA edit Claude executes, and how it self-verifies
IF NOT         what that would mean instead
```

**The card is a question with an address, not a verdict.** `IF CONFIRMED` and `IF NOT` are both
required — a card with only one branch has assumed its own conclusion.

**Cards repeat at the top of every brief until closed**, and a card closes only when the naming
artifact has been read. Closing it by assertion is how the fleet spent four months believing
PT25 was alive.

---

## 9. Daily-ops conventions

**CSV naming.** `data/raw/YYYY-MM-DD.csv`; newest file wins; the export is full history, so the
newest reconstructs the whole ledger.

**No pooling across config changes.** When a bot's config materially changes, snapshot and start
a fresh window. The `epoch_boundary` cell in `bots_meta.csv` encodes this and `build_ledger.py`
applies it. Under the cutover this is a *within-era* rule — cross-era pooling is already
forbidden outright (§3).

**Entry-timing check.** Verify entries land in their declared window, every day. The bell-entry
drift cost −$3,400 over two sessions and ran 20+ sessions before anyone noticed, because nothing
checked.

**Kill-trigger proximity — flagged daily:**
- Any single-day loss > 3× average daily credit.
- A declared hedge failed to fire on a strike touch.
- An OA automation toggled off silently 3× in a week.
- ~~Rolling-30 win rate < 75%~~ — **RETIRED 2026-07-31 (Andy).** A 0DTE PT scalper wins small
  often and loses bigger rarely, so raw win rate was never the right bar; the champion sat at
  ~43% over 221 positions with no kill review ever recorded, and the rule's only effect was to
  fire and be argued with. **Replaced by per-bot, R-based kill criteria, pre-registered at
  Phase 4** — one criterion per bot, written before it restarts, fired in code. See
  `docs/evidence-standards.md` §7 and `docs/pre-registration-ledger.md`.
  A fleet-wide win-rate bar is not reinstated in any form.

---

## 10. Output and persistence

- **`STATUS.md`** is the numeric source of truth, generated by `report.py`. **Never hand-edited.**
  It carries the cutover date in a header banner and an explicit n=0 section when empty.
- **One persisted artifact that updates daily**, not 250 separate files — a day selector, the
  chart, the three verdicts, and a cumulative counterfactual scoreboard that gets more valuable
  every day. The thing Andy opens each evening is then the same object, and its top section is
  always *"what the last 30 days say"*, not *"what happened yesterday."*
- **Every day appends** to `hedge_tournament.csv`, `trade_window.csv`, `lessons.csv`,
  `execution_audit_findings.csv`, and the counterfactual ledger. Those files are the asset.
- Session-log note on any state change, per `CLAUDE.md` §9.

> ⚠️ **`lessons.py` is a full rebuild and will truncate a populated index if its sources are
> empty.** A shrink guard now refuses that (`LESSONS_ALLOW_TRUNCATE=1` to override
> deliberately). Do not remove the guard; it caught a real Day-1 data-loss path.

---

## 11. Build tiers — so this grows rather than boiling the ocean

| Tier | What runs | Effort |
|---|---|---|
| **0 — works today** | Andy provides the capture; Claude produces the chart + three verdicts + cards | Zero infrastructure |
| **1** | Scheduled task weekdays ~17:30 ET: read captures, pull tape, write report, append ledgers | Everything after the capture is unattended |
| **2** | Remove the manual capture step | See below |

**The capture is the bottleneck, and it is a ~2-minute manual step.** Three routes past it:
keep clicking the bookmarklet (honestly fine); drive the Export Data CSV, which **is** confirmed
to carry `botName` as column 1 and works while the subscription is lapsed; or drive OA with
Claude-in-Chrome — noting OA has historically been blocklisted to the extension, so re-verify
before depending on it.

**Honest constraint:** OA has no API. Everything around the capture automates; the capture
itself does not.

---

## 12. Open items

1. ~~The rolling-30 WR kill criterion~~ — **CLOSED 2026-07-31: retired**, replaced by per-bot
   R-based pre-registered criteria at Phase 4 (§9). Automatic kill-flagging is unblocked but
   cannot be wired until those criteria exist, one per bot.
2. **`data/bots_config_v2.csv` does not exist yet.** Until it does, Tier C of the detector is
   SKIPPED and §4's cards run config-blind. This is the single largest gap in the loop.
3. **Counterfactual option pricing** — accept a Black-Scholes reconstruction for the approximate
   arms, or restrict the panel permanently to the two exact ones? Restricting is the honest
   default until someone needs otherwise.
4. **Intraday underlying data** — Tradier live pull is working; reconstruction is the labelled
   fallback. No third source is needed unless sub-minute resolution becomes load-bearing.
5. **48 cached symbol-days of 5-min tape (5/29→7/02) were never committed** and Tradier's window
   is rolling — the early days are already unrecoverable. Post-cutover this stops mattering, but
   the archive's S2 counterfactual arm is permanently thinner for it.
