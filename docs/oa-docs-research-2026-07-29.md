# OA Platform Capability Research — Documentation-Grounded

*Written 2026-07-29 · companion to `docs/oa-setup-exploration-2026-07-29.md`, which was written under an explicit no-research constraint*
*Source: docs.optionalpha.com only. Five parallel sweeps: automations/triggers/logging · decisions/indicators · actions/inputs/tags/loops · exits/pricing/safeguards · backtester/templates/integrations*

> **What this document is for.** The exploration doc carried 9 SPECULATIVE and ~20 EXPECTED claims with a verification appendix of UI checks. This resolves as many as the public docs can, and — more importantly — surfaces **eight primitives the first document did not know existed**, two of which change its top-ranked recommendations.

**Labels used here:**
**DOCUMENTED** — verbatim quote + URL · **DOCS-SILENT** — the docs do not address it, which is itself a finding · **DOCS-CONFLICT** — the docs contradict `oa-platform-reference.md` or the approach-reset doc

---

## 1. The load-bearing question, answered: NO

The exploration's Open Question 1 was whether OA can express "condition sustained for N minutes." **It cannot, and the docs say so affirmatively rather than by omission.**

> "If a price, indicator, etc. exceeds a threshold between intervals, the bot does not know about it. The one major exception is tracking Smart Stops, where the position gain and high gain are tracked every minute. Regardless, even if a bot is logging information or position data between intervals, it will not act upon it until automation execution at the next interval."
> — `technical-documentation/platform/automation-behavior.md` · **DOCUMENTED**

Keyword sweep across `llms-full.txt` for *sustained, persisted, consecutive, for at least, has been, duration, elapsed, minutes or more, in a row, streak*: **zero hits** in any decision context. The only "since" hit is a point-in-time comparator (`[Symbol] price [increased] [2 std devs] since [1 day ago]`), not persistence.

**This reclassifies Pattern C.** The approach-reset doc treats `open 30 minutes or more` as a copy-paste error that replaced a sustain condition. The docs say there was never a sustain condition available to copy. Whoever built HedgeD hit a platform wall and substituted the nearest expressible thing — position age — without recording that substitution. That is a **sixth failure pattern the reset doc does not name: an undocumented substitution made at a platform limit.** It is more dangerous than Pattern C as described, because no amount of config-vs-reality diffing catches it — the config record and the automation tree would agree with each other and both be wrong about the intent.

### 1.1 But there IS a build path, via tags

The docs also establish that **tags are writable state that persists across scans** — the only such mechanism on the platform.

> "Tag Bot: Add tags to your bot. Untag Bot: Remove tags from your bot. Reset Bot Tags: Replace all tags for your bot. Tag Position: Add tags to a position. Untag Position: Remove tags from a position. Reset Position Tags: Replace all tags for a position. Tag Symbol… Untag Symbol… Reset Symbol Tags…"
> — `tools/bots/tags.md` · **DOCUMENTED**

> "Bot Tags: Tags that are applied to your bot. **They do not change state and remain applied to the bot unless reset or untagged by the user.**"
> — `tools/bots/tags.md` · **DOCUMENTED**

> "The tagging system is a powerful tool that allows you to add data to your bots, positions, and symbols. This data can be used to track information, categorize items, and **make decisions within your automations**."
> — `tools/bots/tags.md` · **DOCUMENTED**

A tag survives between scan cycles. That makes a **tag ladder** a genuine persistence counter: at 1-minute scan speed, a monitor that tags `brch1` on first breach, `brch2` when `brch1` is present and the breach still holds, and so on, reaches `brch10` only if the breach held across ten consecutive scans. Untag-all on any non-breach scan resets it. That is a real 10-minute sustain condition, built from documented primitives.

**Cost:** ~10 decision/action node pairs, and it consumes the bot's 1-minute scan budget. **Risk:** every rung is a place the ladder can silently break, and a broken rung fails *safe-looking* (no close). This is a Pattern-A generator by construction and needs the shadow-monitor guard (option C2 in the exploration doc).

---

## 2. Primitives the exploration document did not know about

These are the substantive finds. Each changes at least one option.

| # | Primitive | Verbatim | Why it matters |
|---|---|---|---|
| **N1** | **Trigger list is far richer than "scheduled time"** | "**Date** – At a specific date and time · **Repeating** – On a recurring schedule · **Market open** – 10 minutes after the market opens (9:40 am EST) · **Market close** – 10 minutes before the market closes (3:50 pm EST) · **Position opened** – After the bot opens a position · **Position closed** – After the bot closes a position · **Webhook** – When a webhook is called" (`tools/bots/automations.md`) | Position-opened / position-closed triggers are a designed replacement for the emergent Cleanup behaviour (Pattern E). See K1. |
| **N2** | **Exit Options include a "Touch" trigger** | "You can customize each position's Exit Options for specific management using six triggers: Profit Taking, Profit Target, Price Target, Stop Loss, Trailing Stop, **Touch**, Expiration, Earnings" (`tools/managing-positions/exit-options.md`) | **S1/S2 may not need monitors at all.** A Touch Exit Option runs first in the cycle at 1-min cadence instead of third at scan speed. This is the biggest single find. See K2. |
| **N3** | **Exit Options are attached per-position at open, not re-read from the automation** | "When using Exit Options in an Open Position action, all positions opened in the automation will have the same entry criteria. **Once opened, Exit Options are specific to each position.** You can always edit each position's Exit Options at any time after it is opened." (`tools/managing-positions/exit-options.md`) | Independently confirms the Fortress forensic's central claim that the panel is not evidence — and makes C1 (re-assertion watchdog) the architecturally correct fix, not a workaround. |
| **N4** | **Excessive Errors Failsafe — 10 errors in a day disables ALL automations** | "The 'excessive errors failsafe' is an automatic protection mechanism that **disables all automations when a bot experiences 10 errors within a single day**." (`technical-documentation/troubleshooting/excessive-errors-failsafe.md`) | A **documented mechanism by which a working bot silently stops firing**. This is a live candidate explanation for the QQQ-Fortress 2026-06-12 regression and it is monitorable. See K3. |
| **N5** | **Instant Exit Options are live-bots-only** | "**Live bots** can enable Instant Exit Options, which continuously monitor and update position returns and respond to changes in the leg and underlying pricing." (`tools/managing-positions/exit-options.md`) | Paper and live bots run different exit execution classes. Every paper→live graduation in the fleet carries an unmeasured confound. |
| **N6** | **Inputs are a 3-tier link chain that silently falls back on break** | "the decision input is linked to the Automation Input, which is linked to the Bot Input – and the Bot Input value takes priority. **The Default Values are not used UNLESS the Automation/Bot Input link is broken.**" (`tools/bots/inputs.md`) | The reset doc's Change 2 (parameterise with inputs) has its own silent-failure mode built in: a broken link reverts to a stale Default without stopping the bot. See §4. |
| **N7** | **Bot logs record non-actions** | "Bot logs offer a detailed automation history, allowing you to see exactly **what actions your bot has taken—or not taken—during each automation run**." Filterable "By Type: Scanner, Monitor, Event, and Button" and "By Errors or Warnings." (`tools/bots/automation-logs.md`) | The heartbeat option (B2) is viable and cheaper than proposed — the log already records no-action runs. |
| **N8** | **Bot event loops are a documented failure class** | "an event could automatically open a position when another is closed. Closing the position could trigger another event that immediately opens a new position, thereby causing the bot to enter and exit positions in an **endless loop**." (`technical-documentation/troubleshooting/bot-event-loops.md`) | OA documents the 7/01 orphan-loop class directly — and it is a caution against N1-based designs, which are exactly the shape it warns about. |

Secondary finds: **standard-deviation strike selection** and `exactly / or-higher / or-lower` rounding control (`technical-documentation/calculations/parameter-selection.md`); a webhook "can trigger up to 10 automations in a single bot… and automations in multiple bots" and **persists across bot clones** (`tools/bots/webhooks.md`); **three loop types** including Bot Symbol Loop over dynamic watchlists (`tools/bots/loops.md`); **conditional actions** as a nesting construct distinct from Yes/No branching (`tools/bots/decision-actions.md`).

---

## 3. Verification appendix, resolved

| # | Claim (from the exploration doc) | Verdict | Evidence |
|---|---|---|---|
| V1 | Inputs accept a string/text type | **DOCS-SILENT** — no type system documented. Still a UI check | `tools/bots/inputs.md` documents only the link hierarchy |
| V2 | Missing required input produces a visible warning | **PARTLY DOCUMENTED** — "an error alerts you that this input has an invalid, or missing, value." Whether the run is *blocked* is DOCS-SILENT | `troubleshooting/missing-or-invalid-input.md`, `tools/bots/safeguards.md` |
| V3 | A no-action automation writes a log row | **DOCUMENTED — YES.** "actions your bot has taken—or not taken" | `tools/bots/automation-logs.md` |
| V4 | An Event's No-path can carry actions | **DOCUMENTED — YES**, resultant automations take actions (that is the documented loop hazard) | `troubleshooting/bot-event-loops.md` |
| V5 | Events can gate on market state, not just clock | **DOCS-SILENT.** Trigger types are date/schedule/market-open/close/position-opened/closed/webhook. Conditions live in the tree *after* the trigger | `tools/bots/automations.md` |
| V6 | Exit Option Presets exist | **DOCUMENTED — YES.** "Save your Exit Option criteria as a Preset to be reused for similar position types." Cross-automation scope is DOCS-SILENT | `tools/managing-positions/exit-options.md` |
| V7 | Update Position Exit Options is repeatable without side effects | **DOCS-SILENT.** Only "set (and re-set) Exit Options whenever and however you want" — no statement on repeat application or spurious orders. **Still the highest-value UI check** | `tools/managing-positions/exit-options.md` |
| V8 | A tag-setting *action* exists | **DOCUMENTED — YES.** Tag/Untag/Reset × Bot/Position/Symbol = 9 actions | `tools/bots/tags.md` |
| V9 | Tags appear in the position record and exports | **DOCS-SILENT.** Tags are stated to support "custom reports and analytics" but export visibility is unaddressed. Still a UI check | `tools/bots/tags.md` |
| V10 | Backtest positions download as CSV | **DOCS-SILENT — entirely.** The docs never mention export. This does **not** resolve the licensing-block conflict either way | backtesting section, all pages |
| V11 | Backtest settings copy as text | **DOCS-SILENT** | as above |
| V12 | Compare Backtests holds 5 arms | **DOCS-CONFLICT — docs say FOUR.** "compare up to **four** backtests simultaneously" | `tools/backtesting/backtesting-metrics.md` |
| V13 | "Update a bot from a backtest" preserves positions/stats | **DOCS-SILENT.** The page is a bare Vimeo embed. Only "instantly turn that backtest into an automated bot" exists | `tools/backtesting/automate-your-strategy.md` |
| V14 | **OA can express time-persistence** | **DOCUMENTED — NO.** See §1 | `platform/automation-behavior.md` |
| V15 | Saving a template from a live bot doesn't disturb it | **DOCS-SILENT** | `tools/clone-bot-templates.md` |
| V16 | Template VERSION counter + History + restore | **DOCS-CONFLICT.** Docs describe templates with **no versioning at all**. The approach-reset doc's §2.3 is a first-hand screenshot observation and beats the docs' silence — the docs are behind the product | `tools/clone-bot-templates.md` |
| V17 | Scan Speed settable to 1 minute | **DOCUMENTED — YES.** 15 (default) / 5 / 1, **bot-level**, scoped to Scanners and Monitors only | `tools/bots/automations.md` |
| V18 | Opportunity filters inside the Open action don't log rejections | **DOCS-SILENT**, but the Open action's own "entry criteria" and "position criteria" min/max filters are confirmed to exist inside the action. Still a UI check | `tools/finding-trades/scanners.md` |
| V19 | Slippage-from-mid cap is independent of final price | **DOCUMENTED — YES.** "slippage from the mid-price setting to protect against price fluctuations"; "when multiple final price options are selected, the best price is used" | `tools/bots/smartpricing.md` |
| V20 | Buttons fire an automation manually and are logged | **DOCUMENTED — YES** on both. "One button click results in one execution"; Button is a bot-log filter type | `platform/automations.md`, `tools/bots/automation-logs.md` |
| V21 | "Only 1 position per expiration" exists on live bots | **DOCS-SILENT** — not documented as a named safeguard anywhere | `tools/bots/safeguards.md` |
| V22 | Webhooks carry parameters into an automation | **DOCS-SILENT on payload.** Confirmed: one webhook triggers ≤10 automations in a bot, works across bots, survives cloning | `tools/bots/webhooks.md` |
| V23 | Tradier OTOCO on multi-leg spreads | **OUT OF SCOPE for OA docs** — broker-side check, unchanged | — |
| V24 | Automation log retention window | **DOCS-SILENT.** Material, because B2's heartbeat depends on it | `tools/bots/automation-logs.md` |

**Net: 10 resolved from documentation, 2 conflicts found, 12 still require a UI check.** The remaining 12 are dominated by V7, V9, V10 and V24 — those four gate four different options.

---

## 4. What changes in the exploration document

### Options that get stronger

| Option | Change |
|---|---|
| **B2 heartbeat** (was rank 9, SPECULATIVE on its core premise) | Premise **DOCUMENTED** (N7). Also gets cheaper: no marker trade needed. And N4 gives it a specific thing to watch for — the failsafe. **Promote.** |
| **C1 re-assertion watchdog** (was rank 11) | N3 confirms Exit Options are per-position copies made at open. Re-assertion is now the architecturally correct answer to the Fortress class, not a hack. **Promote.** |
| **D1 Exit Option Presets** (was EXPECTED) | **DOCUMENTED.** Unchanged in rank but no longer speculative. |
| **G1 position tags** (was SPECULATIVE on the write side) | **DOCUMENTED** — nine tag actions exist. Plus tags turn out to be the platform's only persistent state, which makes G1 the foundation for K4 as well as attribution. **Promote.** |

### Options that get weaker or need rework

| Option | Change |
|---|---|
| **A2 required-input tripwire** | Weakened. The docs confirm an *alert*, not a *refusal to run*. Worse, N6 means a broken input link **silently falls back to the Default Value** rather than erroring — the opposite of fail-loud. **Rework: the tripwire must be a distinctive sentinel Default Value** (e.g. `-999`) that a decision explicitly tests for, so a broken link produces an observable, non-trading branch instead of a stale-but-plausible number. |
| **A1 / Change 2 generally (parameterise with inputs)** | Carries N6 as an intrinsic new failure mode. The reset doc's Change 2 is still right, but "behaviour-neutral" is only true while the links hold. **Add to the nightly script: assert each bot's live input values against the pre-registered values, not just their presence.** |
| **A3 shared hedge automation** | The `SUSTAIN_MIN` input has no native implementation (§1). Either build the tag ladder (§1.1) or drop the Conditional arm from the live tournament. Also: shared-by-reference is now **DOCUMENTED** — "Any changes made to an automation will flow through anywhere the automation is used, including other bots" — so the fleet-wide-blast-radius warning on this option is confirmed, not suspected. |
| **I2 tournament in Compare Backtests** | Capacity is **four**, not five (V12). With a no-hedge control that leaves three hedge arms per comparison. Run two overlapping batches sharing the control. |
| **B3 15:52 hard-flat Event** | Constrained: the Market-close trigger is fixed at **3:50 pm**, and Exit Options run only "until 1 minute before the market close." A 15:52 Event is not obviously available — use the 3:50 Market-close trigger or a Repeating trigger at a custom time. **Needs a UI check.** |
| **J1 webhook entry** | No payload is documented, so the VPS can trigger but cannot *parameterise*. The Conditional-via-webhook idea still works (the VPS holds the sustain logic and only calls when satisfied), but the webhook cannot pass the breach depth in. |
| **J2 Tradier OTOCO** | Unchanged, and §10 of the exits sweep found **nothing** in the docs about what happens to a running bot's exit conditions if account state or billing changes. That silence keeps the Fortress cause open. |

### Options that should be killed

**None outright** — but the *indicator-based* framing of anything intraday is dead on arrival:

> "All historical daily indicators in the auto trading platform are cached pre-market based on yesterday's close… The autotrading platform's indicators are based on a Daily (D) time frame." The "intraday" toggle only "uses the current market price" as the final bar; "a true intraday indicator would be plotted using an aggregation period… of less than 1 day" — described explicitly as *not* what the platform does.
> — `technical-documentation/indicators.md` · **DOCUMENTED**

This kills any pivot/VWAP or intraday-regime mechanic expressed as an OA indicator. It has to be webhook-fed from the VPS or it does not exist. (Consistent with the P3 adjudication already on file, but the reason is now a hard platform limit rather than a priority call.)

---

## 5. Four new options the docs unlock

Continuing the exploration doc's numbering. Same fields, same weighting (Score = 1.5·Detection + 1.0·Velocity − 0.25·Hours − BlastPenalty).

### K1 — Position-closed trigger replaces the Cleanup automation
**Primitives:** Trigger → "Position closed" (N1); position loop; Close Position.
**APPLIES TO:** HedgeD first (harmless, it is off). Then `IC-SPX-FastPT25-S2-130PM`, then `IC-SPX-FastPT25-S2`.
**What changes:** S2's whole-IC close stops being an emergent side effect of a 2-minute cleanup monitor. A "Position closed" trigger fires an automation that checks whether the closed position's sibling spread is still open, and closes it. One designed mechanism, one name, one place to read.
**Solves:** Pattern E — and it disarms the trap the reset doc names, because the sibling-close no longer depends on the Cleanup automation existing at all.
**NEW-FAILURE CHECK:** Yes, and OA documents it by name (N8): a position-closed trigger that closes a position can re-trigger itself. **Guard:** the automation must gate on "sibling still open AND opened today," and the bot's daily position limit stays at 2. Test on HedgeD with the daily limit at 2 before anything else.
**Detection 4 · Velocity 1 · Build 3 hrs · Blast: one dead bot (rollout: two live SPX bots) · Behaviour-neutral in intent · Score 6.25**

### K2 — Touch as an Exit Option, not a monitor
**Primitives:** Exit Options → "Touch" trigger (N2).
**APPLIES TO:** HedgeD first. Then the whole hedge tournament — `HedgeA-S1`, `HedgeB-S2`, `HedgeC-S3` — and `QQQ-IC-0DTE-Fortress` (where S2 is currently off).
**What changes:** the fleet builds strike-touch hedges as monitors because `oa-platform-reference.md` §14 says cross-leg state cannot live in Exit Options. If a Touch trigger exists as documented, S1 becomes an Exit Option: 1-minute cadence, runs **first** in the cycle, no scan-speed dependency.
**Solves:** the tournament's "arms differ in execution class" structural failure — S3's win is confounded with being the only Exit-Option arm. Move S1 (and possibly S2, if Touch can close both spreads) onto Exit Options and the confound disappears rather than being controlled for.
**NEW-FAILURE CHECK:** Yes — Exit Options are subject to the Bid-Ask Guard, which "will disable Exit Options from closing a position or tracking the high % or low %" while the spread is wide. A touch hedge that silently stops working exactly when the market is fast is a Pattern-A failure with the worst possible timing. **Guard:** leave the guard OFF on touch hedges (matching current champion config), and keep a shadow monitor (C2) as the divergence detector.
**Open:** whether Touch means *underlying touches the short strike* or *position price touches a level* is not documented. This changes everything about the option and is a two-minute UI check.
**Detection 3 · Velocity 4 · Build 2 hrs · Blast: one dead bot · Behaviour-changing (execution class changes; expect earlier fires) · Score 8.0**

### K3 — Monitor the Excessive Errors Failsafe
**Primitives:** bot logs, error/warning filter (N4, N7).
**APPLIES TO:** every in-scope bot. No HedgeD-first version needed — this is read-only.
**What changes:** a documented mechanism disables **all** automations on a bot after 10 errors in a day, and re-enabling is manual. The nightly script gains two checks: (a) any bot with a nonzero error count, escalating on approach to 10; (b) any bot whose automations are ON in the record but produced no scanner/monitor log rows that day.
**Solves:** the first-class requirement — a mechanic that worked and then stopped. This is the only *named, documented* pathway by which that happens, and the QQQ-Fortress bots stopped entering entirely after 6/26, which is the failsafe's signature.
**NEW-FAILURE CHECK:** Yes, a scoping one — this detects the failsafe, not the Fortress failure. Fortress emitted **entry orders** through 6/26 while emitting no exit orders, which is not a whole-bot shutdown. The failsafe is a hypothesis to test, not the answer. **Guard:** state it as a hypothesis in the pre-registration and check the June logs for the error counter before claiming it.
**Detection 5 · Velocity 1 · Build 2 hrs · Blast: none · Behaviour-neutral · Score 8.0**

### K4 — Tag ladder as a real sustain condition
**Primitives:** Tag/Untag/Reset Position actions; 1-minute scan speed; position loop (§1.1).
**APPLIES TO:** `QQQ-IC-0DTE-HedgeD-Conditional` only, at least initially. This is the pilot's whole point — the Conditional arm has never run as specified and is the reason the tournament cannot select a hedge.
**What changes:** ten rungs. Scan N: if breach and no tag → `brch1`. If `brchK` and breach → `brch(K+1)`. If `brch10` and breach → close. Any non-breach scan → Reset Position Tags. Bot scan speed to 1 minute.
**Solves:** Pattern C, at the level the reset doc could not — it makes the mechanic the tournament was supposed to test actually buildable.
**NEW-FAILURE CHECK:** Yes, badly. Ten rungs is ten places to fail, and every failure mode is silent and fails *closed* (no exit). It is also two automations interacting with shared state, which is the Pattern-E shape. **Guard:** (a) log the max rung reached per position as a tag that is never reset, so the ladder's depth is visible in the position record even when it does not fire; (b) run it in paper against a shadow monitor implementing the naive immediate-$1 stop, and compare; (c) do not roll this beyond HedgeD until it has fired correctly on at least five breaches.
**Detection 2 · Velocity 3 · Build 6 hrs · Blast: one dead bot · Behaviour-changing — this is a mechanic that has never run · Score 4.5**

---

## 6. Docs vs. the project's own reference file

`oa-platform-reference.md` is now demonstrably ahead of the public docs in places and wrong in others. Neither wins automatically — first-hand screenshots beat stale docs, and docs beat memory.

| Claim | `oa-platform-reference.md` | Docs | Read |
|---|---|---|---|
| Backtest history | "back to 2013 (all symbols; XSP from 2015)" §16 | "test period of up to **three years**" | **CONFLICT.** Project source is the Jun-2026 release email; docs may be stale. Check the backtester's own date picker |
| Compare Backtests capacity | ≤5 (project memory) | "up to **four**" | **CONFLICT.** Affects I2's design. Check the UI |
| SmartPricing final price | "up to **150%** of the bid/ask spread" §9 | "0% (bid) through 50% (mid) to 100% (ask)" | **CONFLICT.** Check the Final Price control's max |
| Exit Options window | "roughly 9:40 AM–3:58 PM ET" §8 | "**9:31 am** ET until **1 minute before** the market close" | Docs are more precise; adopt |
| Position limits | "Default caps allow up to 10 daily / 10 total" §11 | Same — and "**Scanners are automatically turned off** if a bot reaches either limit" | Consistent; the auto-off detail is new and matters for the orphan loop |
| Template versioning | Reset doc §2.3, first-hand screenshot: VERSION, History, Clone version N | **No versioning documented at all** | **Trust the screenshot.** Docs lag |
| Bot Groups | In use (#1 SPX-IC, #8 OA-Mirror) | **Not documented anywhere** | Trust the account. Docs lag |
| Cycle order | Exit Options → Events → Monitors → Scanners §4 | Identical, stated twice | **Confirmed** |
| Intra-class order | "not guaranteed" §4 | "Execution order is never guaranteed" — *and* "The automation on top runs first" | **Docs contradict themselves.** Do not build anything that depends on within-class order |
| IC = 2 positions | §10, project rule | Not stated | Docs silent; project rule stands |

---

## 7. Revised shortlist (deltas only)

| Option | Was | Now | Why |
|---|---|---|---|
| A1 Parameter surface + BUILD_ID | 10.75 | **10.75** | Unchanged rank, but N6 adds a required guard: assert live input *values*, not just presence |
| I1 Backtest fingerprint diff | 10.00 | **10.00** | Unchanged, but V10 is still unresolved and gates the whole option |
| G1 Tag attribution | 9.75 | **10.25** | Write side now DOCUMENTED (was SPECULATIVE); build cost drops ~1 hr |
| C2 Shadow PT detector | 9.00 | **9.00** | Unchanged; now the required guard on K2 and K4 as well |
| B2 Heartbeat | 8.00 | **9.00** | Premise DOCUMENTED, cheaper build, and N4 gives it a named target |
| K3 Failsafe monitor | — | **8.00** | New |
| K2 Touch as Exit Option | — | **8.00** | New; contingent on what "Touch" means |
| C1 Re-assertion watchdog | 7.25 | **8.25** | N3 makes it the correct architecture; V7 still gates it |
| I2 Compare Backtests tournament | 8.50 | **8.25** | Four arms, not five — needs two overlapping batches |
| A2 Required-input tripwire | 8.25 | **6.75** | Docs confirm alert, not refusal; N6 fallback is the opposite of fail-loud. Needs the sentinel-value rework |
| K1 Position-closed trigger | — | **6.25** | New |
| K4 Tag ladder sustain | — | **4.50** | New; low score, high strategic value — it is the only path to a real Conditional arm |
| B3 15:52 hard-flat Event | 5.25 | **4.75** | Trigger is fixed at 3:50; custom time needs verification |

Everything not listed is unchanged.

---

## 8. What still needs the UI, ranked by how much it gates

| Check | Gates | Why it matters most |
|---|---|---|
| **What does the Exit Option "Touch" trigger reference** — underlying vs short strike vs position price | K2, the whole tournament rebuild | If it means underlying-touches-strike, S1 and S2 stop needing monitors and the execution-class confound dissolves |
| **Does re-applying Update Position Exit Options generate orders** (V7) | C1 | The watchdog is either free or actively harmful; the docs do not say which |
| **Backtest CSV export exists** (V10) | I1, I2 — ranks 2 and 9 | Docs are silent, so the project's own licensing-block note is neither confirmed nor refuted |
| **Automation log retention window** (V24) | B2, K3 | A 30-day window makes the heartbeat a live alarm; a 7-day window makes it useless for monthly sweeps |
| **Do position tags appear in any export** (V9) | G1 (rank 1–3) | If tags are UI-only, attribution stays a forensic exercise |
| **Compare Backtests: four or five** (V12) | I2 batch design | Two overlapping batches vs one |
| **Backtest history: 3 years or 2013** | I1's window, evidence-bar claims | Determines whether the ≥6-month / ≥100-trade bar clears honestly |
| **Can a Repeating trigger fire at a custom time like 15:52** | B3 | Market-close trigger is hard-coded to 3:50 |
| **Input type list** (V1) | A1's BUILD_ID canary | If inputs are numeric-only, BUILD_ID becomes a number |

---

## 9. Two things worth saying plainly

**The docs describe a platform with no memory.** No counters, no variables an automation can write, no persistence between scans except tags and SmartStops' high-water mark, and no condition that can reference its own past. Every mechanic the fleet has described as "sustained," "confirmed," or "after N minutes of" is either a tag ladder nobody built or a substitution nobody recorded. That is a structural property of the platform, and it should be written into `oa-platform-reference.md` as a constraint at the top, not discovered per-project.

**The docs are behind the product in at least three places** — template versioning, Bot Groups, and probably the June 2026 backtester release. That means documentation research and UI verification are not substitutes for each other, and an "EXPECTED" label based on docs alone is not stronger than one based on a screenshot of the running account. The verification appendix in the exploration document does not go away because this research happened; twelve of its rows survive intact.

---

**Sources:** `docs.optionalpha.com` — `tools/bots/automations.md` · `tools/bots/automation-logs.md` · `tools/bots/inputs.md` · `tools/bots/tags.md` · `tools/bots/loops.md` · `tools/bots/decision-actions.md` · `tools/bots/safeguards.md` · `tools/bots/smartpricing.md` · `tools/bots/webhooks.md` · `tools/bots/clone-bot-templates.md` · `tools/finding-trades/scanners.md` · `tools/managing-positions/exit-options.md` · `tools/backtesting.md` · `tools/backtesting/backtesting-metrics.md` · `technical-documentation/platform/automations.md` · `technical-documentation/platform/automation-behavior.md` · `technical-documentation/platform/data-feeds.md` · `technical-documentation/platform/order-handling.md` · `technical-documentation/platform/bot-limitations.md` · `technical-documentation/indicators.md` · `technical-documentation/calculations/decision-properties.md` · `technical-documentation/calculations/decision-calculations.md` · `technical-documentation/calculations/parameter-selection.md` · `technical-documentation/calculations/probability.md` · `technical-documentation/troubleshooting/excessive-errors-failsafe.md` · `technical-documentation/troubleshooting/bot-event-loops.md` · `technical-documentation/troubleshooting/missing-or-invalid-input.md` · `technical-documentation/troubleshooting/position-limit-warnings.md` · `technical-documentation/troubleshooting/trade-enforcements.md` · `technical-documentation/troubleshooting/testing-automations.md`
