> **⚠️ DEMOTED — read this first (banner added 2026-07-30, Phase 1).**
> This document is **authoritative as diagnosis** and **superseded as a plan**.
> Its **Part 3 and Part 5 are replaced by `docs/build-plan.md`**. Where it conflicts with
> `docs/phase1-kickoff-2026-07-30.md` or `docs/rebuild-audit-2026-07-29.md`, those two win.
> Do not execute a plan from this file.

# Approach Reset — Why the Current Method Is Failing and What Replaces It

*Written 2026-07-29 · derived from the four-bot execution forensic of 2026-07-27/28*
*Companion docs: `docs/config-vs-reality-2026-07-28.md` · `docs/execution-audit-*.md` · `data/execution_audit.csv`*

> **How to use this document.** It is self-contained — a future chat can read only this file and understand the situation. Every claim names the bot it came from. Confidence labels are explicit: **CONFIRMED** means order-level or automation-tree evidence; **INFERRED** means derived from ledger behaviour.

---

## The one-paragraph version

Bots were built. What they did was written down. Over four months the two drifted apart and nothing detected it. A forensic audit of four bots found that **three of the four were running something materially different from what `bots_config.csv` describes** — a profit target that never fired once, a hedge with no conditional in it, and an entry filter that does not exist. Across 35 losing positions the cause split was **66% our configuration, 26% deliberate design, 9% platform**. The strategy was never disproven. It was never *tested*. The fix is not a new strategy — it is instrumentation, parameterisation, and a drift detector.

---

# PART 1 — Why the current approach is failing

## 1.1 The root cause

**There is no mechanism that compares what a bot does to what we believe it does.**

`bots_config.csv` is written by hand, from memory, after the fact. Nothing validates it. A bot can be edited — or built wrong from the start — and the record stays confidently wrong indefinitely. Every downstream artifact (STATUS.md, the readiness board, the hedge tournament, the daily brief) inherits that error and compounds it.

Four months is not how long the drift took. **Four months is how long it took to notice.**

## 1.2 The five failure patterns, with bots as evidence

### Pattern A — A declared mechanic that never executes
**`IC-SPX-FastPT25-S2` (the champion).** PT25 is verifiably attached — the Exit Options editor shows `Profit Taking %: 25% of credit`, pricing Normal, Bid-Ask Guard unchecked. It generated **zero exit orders across all 47 post-fix positions.**

- **24 positions rode to expiry at `mfe_pct 1.00`** — premium decayed to zero and the target never closed them
- Three order-level instances: 6/24 (40.0% profit high), 6/11 (45.7%), 7/01 (33.3%) — Trades lists show only an Open row and the hedge close. No profit-taking order
- Not a platform defect: `QQQ-IC-0DTE-Range075-PT50` fires the same OA mechanic **21/21** on its put side

**Consequence:** the champion has been running *ride-to-expiry + S2*, not *PT25 + S2*. Its go-live gate (18/15 clean condors) certifies a strategy that never ran. **CONFIRMED** that no order was generated; **INFERRED** between platform failure and recent attachment.

### Pattern B — A mechanic attached to one side only
**`QQQ-IC-0DTE-Range075-PT50-Wide2-1230PM`.** PT50 fires **21 of 21** on the put side — `mfe_date == close_date` on every one, the profit-target fingerprint. On the call side it fires **0 of 15** reachable opportunities. Fifteen call spreads reached 50%+ profit, nine of them before 15:00, and all seventeen rode to the 15:50 time exit.

Worst case: **2026-04-07**, a call spread at **100% profit at 14:51**, closed at 15:50 for **−$5**.

**Consequence:** a bot that looks like it has a profit target and half-does. **INFERRED (strong)** from population evidence.

### Pattern C — A mechanic that does not implement what it is named
**`QQQ-IC-0DTE-HedgeD-Conditional`.** Both monitors read:

> `Position is more than $1 in the money` → `Position has been open 30 minutes or more` → `Close Position`

The second gate is **position age**, not breach persistence. Entry is 11:00, so it is permanently true after 11:30. `oa-platform-reference.md` §14 defines Conditional as *"sustained ~$1 past the strike for ~10 minutes."* **There is no time-persistence condition anywhere in either tree.** It is an immediate $1-ITM stop.

Confirmed by the fills: 13 of 16 losses exited **$0.91–$1.07, mean $1.012, sd $0.054** — exactly $1.00 of intrinsic value on a $2-wide spread.

**Consequence:** the hedge tournament's Conditional arm never tested the conditional mechanic. **CONFIRMED** from the automation trees.

### Pattern D — A declared filter that does not exist
**`QQQ-IC-0DTE-HedgeD-Conditional`** again, and **all three siblings**. `bots_config.csv` records `filter: <verify: Range075>`. The scanner is four nodes:

> `Loop QQQ` → `FOMC Meeting today` No → `Current market time is after 11:00am` Yes → `Bot opened a position with [side] today` No → `Open`

**No percent-change nodes at all.** `HedgeA-S1`, `HedgeB-S2` and `HedgeC-S3` carry the identical filter-free scanner.

**Consequence:** **16 of 45 entry days (36%) opened outside the ±0.75% band** — including 2026-03-23 at +1.45%. The tournament *is* matched on entries (a relief), but none of the four is the Range075 bot the config claims. **CONFIRMED.**

### Pattern E — Behaviour that emerges from two automations, unplanned
**`IC-SPX-FastPT25-S2`.** `Scalp-Mon-S2-StrikeTouch` loops position-by-position and closes **only the leg whose own strike is breached.** There is no instruction anywhere to close the other side. Yet the whole IC closes — because `Scalp-Mon-S2-Cleanup` (open ≥2 min + exactly 1 open position → close) kills the orphaned survivor 1–2 seconds later.

| Date | Closes at `:00` | Closes at `:01–:02` |
|---|---|---|
| 6/09 | put K7335, **breached** | call K7445, untouched |
| 6/11 | call K7315, **breached** | put K7210, untouched |
| 6/11 | call K7365, **breached** | put K7255, untouched |
| 6/24 | put K7360, **breached** | call K7475, untouched |
| 7/02 | put K7445, **breached** | call K7560, untouched |

Five for five. **S2 is not a designed hedge — it is a side effect of the cleanup automation.**

**Consequence, and this is a live trap:** the obvious fix for the 7/01 orphan loop is to disable Cleanup. **Doing that silently breaks S2's whole-IC behaviour**, leaving a naked leg. The correct fix is to change the *scanner's* gate instead. **CONFIRMED** (trees + five timestamp sequences).

## 1.3 The two structural failures behind all five

### The 7/01 orphan loop — a race with no interlock
`Scalp-Scan-Put` gates on `Bot has exactly 0 positions with put side and open status` — **currently open**, not *opened today*. Platform cycle order is Exit Options → Scheduled Events → **Monitors → Scanners**. So:

1. Scanner opens a put spread (total = 1)
2. Call side fails to open — reason still unknown
3. Two minutes later Cleanup sees exactly 1 position and closes it
4. Same cycle, Scanner sees 0 put positions and re-opens
5. Repeat until the daily cap

On 2026-07-01 this ran **ten times in 29 minutes** — every close followed by an open **one second later** — burning the entire 10-re-entry budget for −$250. Confirmed by the 6/08 natural experiment: the churn stopped the instant a call spread finally opened.

**`IC-SPX-FastPT25-S2-130PM` carries the identical gate and the identical Cleanup monitor.** It has not looped yet only because it enters at 1:30pm with less runway.

**The QQQ bots cannot loop** — their scanners gate on `Bot opened a position with [side] today`, a per-day flag. `HedgeB-S2` carries the same Cleanup family and never loops. **The QQQ pattern is correct; the SPX champion's is not.**

### The tournament cannot select a hedge
`QQQ-IC-0DTE-Hedge{A,B,C,D}` were built to answer *which hedge*. They can't:

| Problem | Detail |
|---|---|
| Two arms are the same arm | `HedgeA-S1` and `HedgeD` share **identical P/L on 73 of 86 positions (85%)** |
| S3 is mis-implemented | `HedgeC-S3` has **no monitors at all** — S3 is a `Stop Loss %` Exit Option. Its 44 losses show exit/credit median **1.67**, i.e. a **%-of-credit stop**, not the documented "50% max-loss stop" (which would exit near $1.07, not $0.24). **INFERRED (strong)** |
| Arms differ in execution class | S3 = Exit Option (1-min, runs **first** in the cycle). S1/S2/D = Monitors (runs **third**). **S3's win is confounded with being the fastest implementation** |
| No arm has the declared filter | See Pattern D |

Matched-day standing (42 days, identical sizing, by Exp(R)): **S3 −0.0029 · S2 −0.0095 · Raw/no-hedge −0.0211 · S1 −0.0260 · Conditional −0.0308.**

Conditional is worse than not hedging at all. But the ranking cannot be trusted to select a mechanic, because at least two arms are testing something other than their name.

## 1.4 The scoreboard

**35 losing positions across four bots:**

| Cause | Count | Share |
|---|---|---|
| `settings` — our configuration | **23** | **66%** |
| `by_design` — bot did what it was told | 9 | 26% |
| `oa_execution` — platform | 3 | 9% |

**Option Alpha is not the problem.** 84% of audited losses trace to configuration and design choices.

**Coverage caveat:** the audit examined 173 positions — **12.5% of the ledger, 25% of absolute P/L.** The largest untouched pool is `QQQ-IC-0DTE-Baseline` at **−$31,580 across 43 positions** (38% of the fleet's total loss, three full max-loss events, worst Exp(R) in the fleet). It has never been audited.

---

# PART 2 — What is architecturally missing

Three Option Alpha primitives are not being used. One of them is already documented in our own reference file.

## 2.1 Bot Inputs — parameters live inside the logic

Every threshold is hardcoded into a decision node. Every automation reports **"Inputs: No inputs."**

`oa-platform-reference.md` §2 already says: *"Custom Inputs are named variables… so one automation can be re-pointed across bots/symbols without rebuilding logic."* It was documented and not used.

**Reference implementation: the `3DTE $140-$350` mirror bot.** Its Settings page shows a clean Bot Inputs panel — `EXPIRATION: 3 market days` · `POSITION SIZE: 26% of net liquid` · `< RETURN %: 6%` — and its scanner reports "with 3 inputs."

Costs of not using them:
- **Duplicated automations.** `HedgeA-Mon-S1-PutBreach` and `HedgeD-Mon-Cond-PutBreach` are separate near-identical automations maintained twice — and produce identical P/L 85% of the time
- **Every parameter change is a logic edit**, which is how a copy-paste turned a sustain condition into `open 30 minutes or more`
- **Experiments vary more than one thing** — the tournament's core flaw
- **Parameters are invisible.** They live inside four automation trees instead of on one panel, which is why config capture takes 16 clicks per bot instead of one

## 2.2 Triggers — timed entry done with the wrong tool

Timed entry uses a Scanner plus a `Current market time is after 11:00am` decision. A scanner fires at **the first scan cycle where every gate passes** — not at a fixed time. `3DTE $140-$350` uses a **TRIGGERS** section: *"Every day, 10:05am EST."*

Observable effect — first entry across all days:

| Bot | Distribution |
|---|---|
| `HedgeD` | **11:01 × 45/45** |
| `HedgeA-S1` | **11:01 × 45/45** |
| **`IC-SPX-FastPT25-S2`** | 11:01 ×12, **11:08, 11:31, 11:39** — a 38-minute spread |

The champion's scatter has a benign explanation (Range075 failing at 11:01, passing later). But it means the bot silently implements *"trade the first moment after 11:00 when conditions allow, retrying all day"* rather than *"check at 11:00, trade or skip."* **That is a strategy choice nobody made.** It also injects noise into the 11am-vs-1:30 A/B, where entry time is the variable under test.

## 2.3 Version history — being hand-built when it already exists

A clone-and-archive versioning scheme was being designed. Option Alpha already has it: template pages carry a native **VERSION** counter, **LAST UPDATE**, **Tags**, free-text **Notes**, and a **History** section with per-version **"Clone version N"** restore buttons. A cloned bot records `BOT VERSION 11, Jan 23, 2026` — provenance included.

It beats clone-and-archive on the three things that matter: **no bot slot consumed, no position history fragmented, no dependency on the unrun archive-vs-export probe.**

## 2.4 Drift detection — nothing exists

There is no check that compares declared config to actual behaviour. Everything above went unnoticed for four months for this single reason.

---

# PART 3 — The new approach

## 3.1 Four changes

### Change 1 — A nightly behavioural drift detector *(highest priority)*
`scripts/execution_audit.py`, wired into `daily.sh`. Detects from the ledger alone, no OA access required:

| Check | Catches |
|---|---|
| `mfe_pct` ≥ declared PT threshold but no PT-consistent exit | Pattern A, Pattern B |
| `mfe_date == close_date` fingerprint present/absent per side | Pattern B |
| Close followed by open within N seconds | The orphan loop |
| Exit-price clustering | Pattern C — the $1-ITM signature |
| `|loss|` > max structural loss | The 6/11 impossible fill |
| Entry-day gap vs declared filter | Pattern D |

**Validated against the audit as a labelled test set** — roughly 20 of the 35 rows in `data/execution_audit.csv` are ledger-detectable, and the script must reproduce those detections while staying silent on the known-clean cases (champion entry logic, HedgeD's working PT50, Bot 4's correct filter gating, S2 firing on 7/02).

**Build the checks from first principles, not by fitting them to the 35 known cases.** The known cases are validation, not specification — they're all fixed already.

### Change 2 — Parameterise with Bot Inputs
Every threshold that defines a strategy becomes a named Bot Input. **Behaviour-neutral: same numbers, different storage.**

### Change 3 — Template-based versioning
Each meaningful config state saved as a template version, with the hypothesis and kill criteria in the Notes field. The live bot is never cloned, so its position history keeps accumulating.

### Change 4 — Config capture at edit time
A bookmarklet extracts the rendered automation tree as **plain text** (verified working on `Scalp-Scan-Put` and `Scalp-Mon-S2-StrikeTouch`). Captured on every edit plus a monthly sweep, committed to the repo, diffed. Requires a normalisation step — strip the `captured:` line, the sidebar clock, and the `Opportunities N` counter, or every diff produces false alerts.

**Known limitation:** toggle states (`AUTOMATIONS ON/OFF`) do not survive text capture — the control renders both labels. Those need a screenshot.

## 3.2 What is explicitly NOT changing

- **No strategy changes.** No new mechanics, no threshold changes, no hedge selection. The audit identifies causes; it does not authorise config changes
- **The 7 OA-Mirror bots are never refactored** — they are faithful copies by definition
- **The 17 OFF bots stay off** until there is a reason
- **`bots_config.csv` gets corrected, not redesigned**

## 3.3 The three discipline rules

**Rule 1 — Refactor first, re-parameterise later.** Hardcoded `$1` becomes an input holding `$1`. Same value. Let it run a week, confirm the ledger is unchanged, *then* start changing numbers. If both happen at once you cannot attribute any change in results — which is exactly the mistake that produced this audit.

**Rule 2 — Pre-register before restarting.** Hypothesis, kill criterion, sample-size target, review date — written down *before* the bot runs, while there is no stake in the answer. This is what makes the G2 gate problem structurally impossible: a gate cannot be cleared by data from a strategy that wasn't running, because the pre-registration pins which strategy the data must come from.

**Rule 3 — Pilot on a dead bot first.** `QQQ-IC-0DTE-HedgeD-Conditional` is off, understood, and worthless. Learn the pattern there. The champion goes last.

---

# PART 4 — Why this benefits the project

## 4.1 Immediate

**Results become trustworthy.** Every number in the project currently carries an asterisk. That asterisk is what blocks every other decision.

**The known traps get disarmed.** Specifically: the Cleanup fix that would have broken S2, the 130PM arm carrying the same loop, and the Market-pricing on Cleanup that produced a $3,000 structurally-impossible fill on 6/11.

**Recoverable value on the audited slice is roughly +$11,944** if declared logic had executed — an optimistic bound, already net of an $8,854 winner give-back, and before commissions (~$286–372 on the champion's 13 losses). *Fill quality is better than assumed: 21 of 21 observed PT50 fills landed at or better than target, mean advantage 4.6% of credit.*

## 4.2 Structural

**Experiment velocity.** Testing a threshold today means duplicating an automation, editing a node, attaching a bot, and hoping nothing else was touched. With inputs it is typing a number. That is the difference between one experiment every few weeks and several a week — and experiment rate is the only variable that determines how fast anything gets learned.

**Experiments become controlled by construction.** One shared automation plus inputs means the only thing that *can* differ between arms is the value. Clean because it cannot be dirty, not because someone was careful.

**Detection latency collapses.** Four months → one day. PT25's failure would have been caught on the first position.

**Config capture becomes one screenshot.** Parameters surfaced on the Bot Inputs panel instead of buried in four trees.

## 4.3 Doors this opens

**The hedge question becomes answerable.** Open since March. With matched arms, shared automations, and inputs, the tournament can finally select a mechanic — including re-testing the *real* Conditional, which has never run.

**Live capital becomes a defensible decision.** Not "I think it works" but "here are 100+ positions of a strategy I can prove was running, against a kill criterion I wrote before I saw the data."

**The audit becomes an instrument rather than an event.** A one-shot forensic decays the moment it's written. A nightly script keeps paying.

**Prior work stops being wasted.** Four months of runtime produced almost no decision-grade evidence. The only way that time becomes worth something is if the next stretch produces a real answer — and it cannot, on the current setup.

## 4.4 The honest limits

- **This does not make a losing strategy win.** It makes the answer legible when it arrives. Whether the edge exists is still unknown
- **Confidence that fixing everything yields a higher forward score: ~25%.** The one correctly-functioning mechanic that could be measured — S2 — *lost money* (−$3,285 over the champion's post-fix window)
- **Every recovery figure is an optimistic bound**
- **Sample sizes remain below the bar.** Champion post-fix: 47 positions / 15 days. HedgeD: 86 / 45 days. Both fail ≥100 trades and ≥6 months
- **Some evidence is permanently gone.** The March–May 5-minute tape expired before it was archived, so the real Conditional mechanic can never be modelled on this data
- **The whole thing is wasted if the fleet stays off.** Its entire value is making the *next* 100 positions trustworthy

---

# PART 5 — Sequencing

| Phase | Work | Time | Blocked by |
|---|---|---|---|
| **0** | `scripts/execution_audit.py` + test fixture | 3–4 hrs | Nothing |
| **0** | Scope decision + pre-registration template | 1 hr | Nothing |
| **1** | Pilot: Bot Inputs on `HedgeD` (dead bot) | ~30 min | Verify edits persist |
| **2** | Roll out to ~9 in-scope bots | ~30–45 min each | Phase 1 |
| **3** | Capture ritual + V1 templates | 2 hrs | Phase 2 |

**Total ≈ 10–12 hours across 2–3 weeks.** Ordering matters more than speed: **script first, pilot second, champion last.**

**Recommended commitment: Phase 0 + Phase 1 only (~5 hrs), then reassess.** Small enough that being wrong costs almost nothing, and it produces the one irreplaceable thing — a nightly check that says when a bot stops doing what it's believed to do.

---

# PART 6 — Open questions

1. **Do edits persist while the account is inactive?** The banner says no; a clone and a template save both appeared to succeed. **Verify with DevTools Network tab (200 vs 402/403) before investing hours.**
2. **Is `DIR-SPX-PutVIX22-SL75` actually switched on?** Zero positions in 22 trading days is fully explained by VIX never reaching 22 (max high 20.72) — but a correctly-gated bot and a switched-off bot emit identical evidence
3. **Why did `Scalp-Scan-Call` never fire on 2026-07-01?** Determines whether the orphan loop is a rare tape accident or a recurring thin-credit failure mode. Likely inside the Open Position action's opportunity filters
4. **`QQQ-IC-0DTE-Baseline` has never been audited** — −$31,580, 43 positions, three max-loss events, 38% of total fleet loss
5. **Continue vs shelve is unresolved.** The audit could not answer it, and that *is* the finding: no evidence for the strategy and none against it. **"Continue unchanged" is the one clearly wrong option**

---

## Appendix — Evidence index

| Bot | Finding | Confidence |
|---|---|---|
| `IC-SPX-FastPT25-S2` | PT25 attached, 0 orders / 47 positions | CONFIRMED (editor + 3 Trades lists + 24 expiries) |
| `IC-SPX-FastPT25-S2` | Orphan loop, 10 round-trips 7/01 | CONFIRMED (2 Cleanup logs + 6/08 natural experiment) |
| `IC-SPX-FastPT25-S2` | S2 = StrikeTouch + Cleanup emergent | CONFIRMED (tree + 5 timestamp sequences) |
| `IC-SPX-FastPT25-S2` | $3,000 of 6/11 exceeds structural max | CONFIRMED (Trade Details: Market, 0–7.5 quote, filled $7.50) |
| `IC-SPX-FastPT25-S2-130PM` | Same scanner gate + Cleanup | CONFIRMED (bookmarklet capture) |
| `QQQ-Range075-PT50-1230PM` | PT50 puts 21/21, calls 0/15 | INFERRED (strong) |
| `QQQ-HedgeD-Conditional` | No sustain condition | CONFIRMED (both monitor trees) |
| `QQQ-HedgeD-Conditional` | No Range075 filter | CONFIRMED (both scanner trees) |
| `QQQ-Hedge{A,B,C}` | Identical filter-free scanners | CONFIRMED (all six trees) |
| `QQQ-HedgeC-S3` | No monitors → S3 is an Exit Option | CONFIRMED (Automations panel) |
| `QQQ-HedgeC-S3` | %-of-credit stop, not 50% max loss | INFERRED (44/44 MAE fingerprint, ratio med 1.67) |
| `QQQ-HedgeA-S1` ≈ `HedgeD` | Identical P/L 73/86 | CONFIRMED (ledger) |
| `DIR-SPX-PutVIX22-SL75` | 0 positions, VIX never ≥22 in 22 days | CONFIRMED (Tradier daily) |
| `DIR-SPX-Put-Control` | PT100 fired at exactly 2× debit | CONFIRMED (ledger) |
| `3DTE $140-$350` | Reference architecture — Inputs, Triggers, versions | CONFIRMED (Settings + template page) |
