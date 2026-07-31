# Option Alpha platform reference — v2

*REWRITTEN FROM SCRATCH 2026-07-31 for Bot Fleet v2. Supersedes the v1 file at
`~/bot-fleet/docs/oa-platform-reference.md` entirely — do not read the old one.*

> **This file GATES the greenfield builds and the four clone specs.** Six carried docs cite it.
> The v1 version had two defects serious enough to require a rewrite rather than a patch:
> its §14 defined a hedge mechanic that **cannot be built on this platform**, and
> Exit-Options-panel-as-evidence was implicit throughout — the exact reasoning that let a
> dead profit target look alive for four months.

---

## 0. Read this first — three structural facts

### 0.1 The platform has no memory

No counters. No variables an automation can write. No persistence between scans except
**tags** and SmartStops' high-water mark. **No condition can reference its own past.**

> *"If a price, indicator, etc. exceeds a threshold between intervals, the bot does not know
> about it. The one major exception is tracking Smart Stops… Regardless, even if a bot is
> logging information or position data between intervals, it will not act upon it until
> automation execution at the next interval."*
> — `technical-documentation/platform/automation-behavior.md` [DOCUMENTED]

A keyword sweep of the full docs corpus for *sustained · persisted · consecutive · for at
least · duration · elapsed · minutes or more · in a row · streak* returns **zero hits in any
decision context**. The only *"since"* comparator is point-in-time
(`[Symbol] price [increased] [2 std devs] since [1 day ago]`), not persistence.

**Every mechanic this project has described as "sustained", "confirmed", or "after N minutes
of" is either a tag ladder nobody built, or a substitution nobody recorded.** Treat this as
the platform's defining constraint, not a footnote. §5.3 gives the one build path that exists.

### 0.2 Evidence tiers — every claim below carries one

The docs are **behind the product** in at least three confirmed places (template versioning,
Bot Groups, and probably the June 2026 backtester release). So documentation research and UI
verification are not substitutes for each other, and a doc-sourced claim is **not**
automatically stronger than a screenshot of the running account.

| Tag | Means |
|---|---|
| **[DOCUMENTED]** | verbatim quote + path in `docs.optionalpha.com` |
| **[FIRST-HAND]** | observed in Andy's account — screenshot or bookmarklet capture |
| **[PROJECT-RULE]** | established by this project's own data; docs silent |
| **[SINGLE-SOURCE]** | one uncorroborated source. **Never build a one-way door on these.** |
| **[DOCS-SILENT]** | the docs do not address it — itself a finding |
| **[CONFLICT]** | two sources disagree; both stated, neither laundered |

Where a first-hand screenshot and a stale doc disagree, **the screenshot wins**. Where memory
and a doc disagree, **the doc wins**.

### 0.3 The Exit Options panel is NOT evidence

> *"When using Exit Options in an Open Position action, all positions opened in the automation
> will have the same entry criteria. **Once opened, Exit Options are specific to each
> position.** You can always edit each position's Exit Options at any time after it is
> opened."* — `tools/managing-positions/exit-options.md` [DOCUMENTED]

Exit Options are **copied onto the position at open**. The panel renders the *automation's
current settings* — not what is live on any position. The two can diverge silently and
indefinitely, and in this fleet they did: Fortress positions generated **no exit orders at
all** — not sent-and-unfilled, never sent — while the panel still displayed `PROFIT % 50%`.

**The only order-level ground truth is the position's Trades list.** Everywhere this document
says "verify", it means the Trades list. This rule is absolute and has no exception.

---

## 1. What Option Alpha is

A no-code autotrading platform. Bots are built from automations; automations are decision
trees plus actions. Bots run in OA's cloud regardless of whether your machine is on.

- Brokers: **Tradier** and **TradeStation**. Connecting one makes the platform free.
- Two run modes: **paper** (live data, no real fills) and **live**. A bot is bound to one
  account at creation and cannot be flipped later.
- ⚠️ **Paper and live are different exit execution classes** — see §4.6. Every paper→live
  graduation in this fleet carries an unmeasured confound.

---

## 2. Object hierarchy

```
Portfolio
  └─ Bot                  (strategy container: account, allocation, safeguards, symbols)
       └─ Automation      (Scanner / Monitor / Event / Button — a decision tree + actions)
            ├─ Decisions  (yes/no logic blocks)
            └─ Actions    (open / close / update / tag / loop)
                 └─ Position(s)
```

**Automations are shared by reference.** They live in the Library and can be added to many
bots. Editing a shared automation changes it in **every** bot that uses it. **Copy** to fork.

> ⚠️ **THE CLONE TRAP.** A cloned bot shares its parent's automations by reference. Edit the
> clone and you have edited the original; edit the original later and you silently change the
> clone. Fork every automation via **Copy** immediately after cloning, then confirm the clone's
> list points at the copies. [FIRST-HAND — runbook §2 step 2]

> ⚠️ **SYMBOLS DROP SILENTLY ON CLONE.** The Symbols panel is not carried over. A bot with no
> Symbols looks fully configured and simply never scans. Re-add them. [FIRST-HAND]

---

## 3. Bot settings and safeguards

| Setting | What it does |
|---|---|
| Name / Icon | Cosmetic. |
| Account | Paper or a connected live account. Fixed at creation. |
| Allocation | Max capital for opening positions. % or $. Calculated **at entry**, on entry max risk. |
| Daily Position Limit | Max new positions opened in one trading day. |
| Total Position Limit | Max simultaneously open positions. |
| Scan Speed | Bot-level interval for Scanners and Monitors. Default **15 min**, down to **1 min**. |
| Symbols | Tickers the bot may trade. |

**Defaults allow 10 daily / 10 total, both editable. There is no limit on closing.** When a
limit trips, **scanners are automatically turned off** until there is room [DOCUMENTED,
`§ safeguards`] — which makes the daily limit a usable interlock (§5.4).

> ### ⛔ IC = 2 POSITIONS [PROJECT-RULE]
> OA models **each spread as a separate position**. A full iron condor is **two** positions —
> the call spread and the put spread. A one-IC-per-day bot needs limits of **2, not 1**, or one
> side never opens. Ten re-entries of a single IC is a daily limit of **20**, not 10.
> Docs are silent on this; the project rule stands and is load-bearing everywhere.

**Allocation caveat.** Max risk is an *at-expiration* concept. Exit-side risk can exceed entry
allocation when spreads blow out. With percentage allocation above 50%, OA deliberately shrinks
later positions to avoid exceeding 100%.

---

## 4. Automations, triggers, and execution order

Scanner and Monitor are **organisational labels, not different objects**. A Scanner can close;
a Monitor can open. This is the mechanism behind the "a scan node opened an extra leg" class of
bug — and behind the 7/01 orphan loop.

### 4.1 The full trigger vocabulary [DOCUMENTED]

> *"**Date** – At a specific date and time · **Repeating** – On a recurring schedule ·
> **Market open** – 10 minutes after the market opens (9:40 am EST) · **Market close** –
> 10 minutes before the market closes (3:50 pm EST) · **Position opened** – After the bot
> opens a position · **Position closed** – After the bot closes a position · **Webhook** –
> When a webhook is called"* — `tools/bots/automations.md`

Two of these are richer than this project previously assumed:

- **Market open is hard-coded 9:40 am; Market close is hard-coded 3:50 pm.** Neither is
  adjustable. See §8.2 — this constrains the clone specs.
- **Position opened / Position closed** are native triggers. They are the designed replacement
  for the emergent Cleanup-monitor behaviour, and are how a sibling-spread close should be
  built (§5.4).

### 4.2 Execution order — fixed between classes, undefined within

**Exit Options → Scheduled Events → Monitors → Scanners.** Stated twice in the docs; confirmed.

**Order *within* a class is not guaranteed.** The docs contradict themselves here — one page
says *"Execution order is never guaranteed"*, another says *"The automation on top runs
first"* [CONFLICT]. **Build nothing that depends on within-class order.**

This ordering is architecturally important: it is why an Exit Option and a Scheduled Event are
in genuinely different execution classes, and why a backstop in the Events class survives an
Exit Options failure (§8.2).

Before each execution OA runs a **redundant position check** and blocks an action already in
flight. Note this did **not** prevent the 7/01 orphan loop — close and open are not identical
actions.

### 4.3 Loops

**Position loop** (oldest → newest, always), **Symbol loop**, and **Bot Symbol Loop** over a
dynamic watchlist. Loops inside a synchronous group run sequentially — one item fully through
the tree before the next.

### 4.4 Bot logs record NON-actions [DOCUMENTED]

> *"Bot logs offer a detailed automation history, allowing you to see exactly **what actions
> your bot has taken—or not taken—during each automation run**."* Filterable by type
> (Scanner / Monitor / Event / Button) and by errors or warnings. — `tools/bots/automation-logs.md`

This is the **only** way to distinguish a correctly-gated bot from a switched-off one.
`DIR-SPX-PutVIX22-SL75` took zero positions in 22 days because its VIX≥22 gate correctly never
fired — from position data alone that is indistinguishable from a dead bot. The log closes it:
**a scanner run with no entry = healthy. Zero log rows = presumed OFF or failsafe-tripped.**

⚠️ **Log retention window is [DOCS-SILENT].** Any monitoring design that depends on looking
back more than a few days is unproven.

### 4.5 The Excessive Errors Failsafe [DOCUMENTED]

> *"The 'excessive errors failsafe' is an automatic protection mechanism that **disables all
> automations when a bot experiences 10 errors within a single day**."*
> — `technical-documentation/troubleshooting/excessive-errors-failsafe.md`

Ten errors in one day, on one bot, disables **all** its automations. **Re-enabling is manual.**

This is a documented mechanism by which a working bot silently stops firing, and it was unknown
to this project until 2026-07-29 — including to the OA support rep consulted about the lapse.

> **Carry the uncertainty:** it is a **hypothesis** for the 2026-06-12 Fortress regression, not
> the answer. Fortress kept emitting *entry* orders through 6/26 while emitting no exit orders,
> which is not a whole-bot shutdown. State it as a hypothesis in pre-registration and check the
> June error counter before claiming it.

### 4.6 Instant Exit Options are live-bots-only [DOCUMENTED]

> *"**Live bots** can enable Instant Exit Options, which continuously monitor and update
> position returns and respond to changes in the leg and underlying pricing."*
> — `tools/managing-positions/exit-options.md`

Paper and live run different exit execution classes. Any paper result carrying an exit-timing
claim does not transfer cleanly to live.

### 4.7 Bot event loops are a documented failure class [DOCUMENTED]

> *"an event could automatically open a position when another is closed. Closing the position
> could trigger another event that immediately opens a new position, thereby causing the bot to
> enter and exit positions in an **endless loop**."*
> — `technical-documentation/troubleshooting/bot-event-loops.md`

OA documents this fleet's 7/01 orphan-loop class directly. It is a standing caution against
position-opened/closed trigger designs — which is exactly the shape §5.4 recommends. Build the
interlock with it, not after it.

---

## 5. Decisions, actions, and state

### 5.1 Decision families

Symbol-based · Indicator-based · Bot-based · Opportunity-based (a *candidate* trade) · General
(time, day, events) · Position-based (an *existing* position). Groupable and nestable;
copy/paste as groups. **Conditional actions** exist as a nesting construct distinct from Yes/No
branching.

Strike selection supports **standard deviations** as well as delta / %OTM / absolute / premium,
with `exactly · or-higher · or-lower` rounding control.

> ### ⛔ ALL INDICATORS ARE DAILY, CACHED PRE-MARKET [DOCUMENTED]
> *"All historical daily indicators in the auto trading platform are cached pre-market based on
> yesterday's close… The autotrading platform's indicators are based on a Daily (D) time
> frame."* The "intraday" toggle only substitutes the current price as the final bar; a true
> intraday indicator *"would be plotted using an aggregation period of less than 1 day"*, which
> is explicitly not what the platform does. — `technical-documentation/indicators.md`
>
> **This kills any pivot / VWAP / intraday-regime mechanic expressed as an OA indicator.** It
> has to arrive by webhook from outside, or it does not exist.

### 5.2 Inputs — a three-tier chain that fails silently [DOCUMENTED]

> *"the decision input is linked to the Automation Input, which is linked to the Bot Input – and
> the Bot Input value takes priority. **The Default Values are not used UNLESS the
> Automation/Bot Input link is broken.**"* — `tools/bots/inputs.md`

**A broken link does not error. It silently reverts to a stale Default and keeps trading.**
This is the opposite of fail-loud, and it is built into the mechanism the v2 tournament depends
on for matched arms.

**Mitigation, required on every input-parameterised arm:** make each Default Value a
distinctive sentinel (`-999`) that a decision explicitly tests for and refuses to trade on.
A missing input produces *"an error alerts you that this input has an invalid, or missing,
value"* — but whether the run is **blocked** is [DOCS-SILENT]. Do not rely on it.

⚠️ **Whether Exit Options can reference Bot Inputs is [DOCS-SILENT] and unverified.** The
documented chain terminates at a *decision* input; Exit Options are never named as a consumer.
The greenfield spec ("PT% as a Bot Input") **depends on this and it has not been checked.**
See §9.

### 5.3 Tags — the only writable state on the platform [DOCUMENTED]

> *"Bot Tags: Tags that are applied to your bot. **They do not change state and remain applied
> to the bot unless reset or untagged by the user.**"* · *"The tagging system… can be used to
> track information, categorize items, and **make decisions within your automations**."*
> — `tools/bots/tags.md`

Tag / Untag / Reset × Bot / Position / Symbol = **9 tag actions** [DOCUMENTED].

**This is the entire memory of the platform.** It is also the one build path for a sustain
condition — see §6.2.

### 5.4 Closing a sibling spread — use the Position-closed trigger

An IC is two positions (§3). Closing "the whole condor" therefore requires an explicit
mechanism. In v1 this was an *emergent side effect* of a 2-minute Cleanup monitor — unnamed,
undocumented, and load-bearing for S2.

**The designed replacement:** a **Position closed** trigger (§4.1) fires an automation that
checks whether the closed position's sibling is still open, and closes it. One mechanism, one
name, one place to read.

> ⚠️ **This is exactly the shape §4.7 warns about.** A position-closed trigger that closes a
> position can re-trigger itself.
> **Required interlocks, all three:** gate on *"sibling still open AND opened today"*; keep the
> bot's daily position limit at **2**; and test on a dead bot first.

---

## 6. Exit Options — what they are and what they are not

Per-position rules, evaluated every **1 market minute**, running **first** in the cycle.

**Operating window: 9:31 am ET until 1 minute before the market close** [DOCUMENTED].
*(The v1 file said "roughly 9:40 AM–3:58 PM ET". The docs are more precise; adopt them. This
change matters — see §8.2.)*

### 6.1 The triggers [DOCUMENTED]

> *"You can customize each position's Exit Options for specific management using six triggers:
> Profit Taking, Profit Target, Price Target, Stop Loss, Trailing Stop, **Touch**, Expiration,
> Earnings"* — `tools/managing-positions/exit-options.md`

*(The docs say "six" and then list eight. Reproduced verbatim rather than corrected, because
which reading is right is unknown.)*

Also available: **Profit Taking $ / Stop Loss $** (absolute dollars, June 2026 release) and
**Avoid Events** (close the day before FOMC / CPI at a chosen time).

**Presets exist** [DOCUMENTED]: *"Save your Exit Option criteria as a Preset to be reused for
similar position types."* ⚠️ **Cross-automation scope is [DOCS-SILENT]** — whether one preset
object can be referenced from both the call-side and the put-side Open Position action is
unverified, and the greenfield spec assumes it can.

> **A preset makes the VALUES consistent, not the ATTACHMENT.** A preset can still be attached
> to one Open action and omitted from the other. It converts a silent asymmetry into a visible
> one — a smaller failure class, not none. The per-side fire-rate assertion still has to run.

### 6.2 THE TOUCH TRIGGER — the highest-value open question in this document

A `Touch` Exit Option is documented to exist. **What it references is not.**

> **Open, and gating:** does Touch mean *the underlying touches the short strike*, or *the
> position price touches a level*? This is a two-minute UI check and it changes the entire
> tournament architecture.

**If Touch means underlying-touches-strike:** S1 and S2 stop needing monitors entirely. They
become Exit Options — 1-minute cadence, running *first* in the cycle instead of third at scan
speed. The v1 file's §14 claim that cross-leg strike-touch logic *cannot* live in Exit Options
would be **wrong**, and the tournament's worst confound — that S3 was the only Exit-Option arm,
so its win was inseparable from its execution class — **dissolves**.

**Its own new failure mode:** Exit Options are subject to the **Bid-Ask Guard**, which
*"will disable Exit Options from closing a position or tracking the high % or low %"* while the
spread is wide [DOCUMENTED]. A touch hedge that silently stops working exactly when the market
is fast is the worst-timed possible failure. **Guard: leave the Bid-Ask Guard OFF on touch
hedges, and keep a shadow monitor as the divergence detector.**

⚠️ Whether a Touch on one spread can close its **sibling** is unresolved. Assume not; use §5.4.

### 6.3 The Bid-Ask Guard suppresses exits silently

While the position's spread exceeds the configured width, Exit Options are **disabled** and
high%/low% tracking **pauses**. It exists to stop the platform acting on garbage mid-prices.

**It is currently OFF on the champion and on HedgeD** [FIRST-HAND]. Turning it on is a
silent-suppression generator. Decide per bot, deliberately, and record the decision.

### 6.4 Mid-price, two-minute orders — carry the caveat

Exit Options evaluate the position's **mid-price**; a triggered order stays active **two
minutes**, then cancels and re-checks at the next minute. Fills are never guaranteed. For a
profit target, SmartPricing's final price is auto-set to the price that locks in the target.

⚠️ **[PROJECT-RULE, not doc-verified.]** The 2-minute lifetime and mid-price evaluation appear
in project files only; the docs do not address either. They explain the observed ~11% PT-miss
rate on thin credits, so they are probably right — but they are not documented.

### 6.5 Re-applying Exit Options — the highest-value unverified operation

Whether **Update Position Exit Options** can be re-applied repeatedly without generating
spurious orders is **[DOCS-SILENT]**. The docs say only *"set (and re-set) Exit Options
whenever and however you want"*.

This gates any re-assertion watchdog — the architecturally correct fix for §0.3, since Exit
Options are per-position copies. **Check it in the UI before building on it.**

---

## 7. SmartPricing

Timed limit orders that walk from the mid toward your worst acceptable ("final") price,
cancelling and re-sending until filled or exhausted.

| Mode | Prices tried | Time per price |
|---|---|---|
| Fast | up to 3 | 5 s each |
| Normal (default) | up to 4 | 10 s each |
| Patient | up to 5 | 20 s each |
| Off | single limit order | — |
| **Market** | immediate market order | — |

⚠️ **[PROJECT-RULE, not doc-verified.]** These mode names, price counts and timings come from
project files. The docs do not state them.

> ### ⛔ [CONFLICT] — FINAL PRICE CEILING
> The v1 file said SmartPricing may reach **150%** of the bid/ask spread. The docs describe the
> control as *"0% (bid) through 50% (mid) to 100% (ask)"*. **These disagree and the conflict is
> unresolved.** Check the Final Price control's actual maximum in the UI before relying on
> either. Do not quote 150% as fact.

**Confirmed** [DOCUMENTED]: a *"slippage from the mid-price setting to protect against price
fluctuations"* exists independently of final price, and *"when multiple final price options are
selected, the best price is used."*

> ### ⛔ MARKET ORDERS FILL OUTSIDE THE SPREAD
> This is not theoretical. The 6/11 Cleanup fill on a $5-wide spread came in at **$7.50** —
> **$5.05/contract beyond the worst price the position was ever marked at** — producing a
> −$7,740 loss on $4,740 of risk (R −1.63), structurally impossible for a defined-risk spread.
> The detector reproduces this from two independent rules (`execution_audit.py` v1.0.0,
> `IMPOSSIBLE_FILL` + `FILL_WORSE_THAN_MAE`).
>
> **Rule: Market pricing is banned on every exit in the v2 fleet, with one exception** — a
> hard end-of-day flat close, where fill certainty beats fill quality. Do not cap the flat
> exit's slippage; cap profit-taking and hedge closes.

Guidance: **Fast** for 0DTE exits where fill certainty matters; **Patient** in calm markets.

---

## 8. Building the v2 fleet — what the platform supports

### 8.1 The greenfield exit stack

Per `build-plan.md` §2B and runbook §3 Step C, each greenfield bot carries:

1. **A named Exit Option Preset in the Open Position action** — PT% · Touch on the challenged
   side · time exit. ⚠️ Depends on two unverified things: preset cross-automation scope (§6.1)
   and whether Exit Options accept Bot Inputs (§5.2).
2. **A flat-close Scheduled Event backstop** in the Events class — see §8.2.
3. **A position-closed-trigger automation** to close the sibling spread — §5.4, with all three
   interlocks.

### 8.2 ⚠️ THE 15:52 BACKSTOP MAY NOT BE BUILDABLE AS SPECIFIED

`build-plan.md` §2B specifies a **"15:52 flat-close Scheduled Event backstop"** on two of the
four clones. Two documented facts sit against it:

- The **Market close trigger is hard-coded to 3:50 pm** (§4.1). There is no 15:52 variant of it.
- Exit Options run *"until 1 minute before the market close"* (§6) — so a 15:52 Exit Option
  does not exist either.

A **Repeating trigger at a custom time** may still reach 15:52; the docs do not say.
**This is a UI check, and it gates two clone specs.**

> **The plan is under decision freeze and I have not edited it.** This is raised as a finding,
> per the freeze's own instruction. If the Repeating trigger cannot hit 15:52, the spec needs
> an explicit amendment from Andy — either move the backstop to the 3:50 pm Market-close
> trigger, or pick a reachable custom time. **Do not improvise this on build day.**

The *architecture* is sound regardless of the minute: the backstop's whole value is living in
the **Events** execution class, which survives an Exit Options failure. Only the timestamp is
in question.

**Attribution guard.** Two exit mechanics targeting one position means you cannot tell from P/L
which fired. Give the Event a **distinct SmartPricing setting** from the Exit Option so the
Trades list distinguishes them, and have the nightly detector count fires per mechanic. This is
what `execution_audit.py`'s `BACKSTOP_CAUGHT_IT` rule reads — and it needs `time_exit` and
`event_backstop` as separate config columns for exactly this reason.

### 8.3 Verification standard — every bot, before it may trade

Two acceptable proofs, in order of preference:

1. **Button test-fire**, then read the resulting **Trades list**; or
2. open the **first new position** and confirm the Trades list contains the PT row and the
   exit-trigger row.

**The Exit Options panel is not evidence** (§0.3). For the two control clones the check is
**inverted**: confirm the Trades list shows **no** PT or exit-trigger rows, and that the S2
monitor is firing.

For a sibling-close mechanism, the **timestamp gap is the test**: a designed close-both shows
`:00`/`:00`; an emergent Cleanup-driven one shows `:00`/`:01–:02`.

### 8.4 Clone checklist — the platform-level traps

1. **Fork ALL automations via Copy** (§2 — shared by reference).
2. **Re-add Symbols** (§2 — they drop silently).
3. Set **Daily / Total limits with 2 positions per IC** in mind (§3).
4. Confirm every time gate is a **real decision node**, not assumed. *(The 11 AM gate on the
   original Scalp-SPX bot was never implemented — 20+ sessions of entry drift.)*
5. Verify the scan position-count node gates on the **correct side**, or the scanner re-fires
   and opens a single leg.
6. Choose SmartPricing speed and a sane final price. **No Market on any exit but the flat close.**
7. Attach exits as a **named Preset**, and record the preset name per Open action in the capture.
8. Save as **template V1** with the pre-registration note attached.

---

## 9. Open UI checks — ranked, and what each one gates

Nothing below is answerable from documentation. Each is a few minutes in the account.

| # | Check | Gates |
|---|---|---|
| **1** | **What does the Exit Option `Touch` trigger reference** — underlying vs short strike vs position price? | The entire tournament architecture (§6.2). If it means underlying-touches-strike, S1/S2 stop needing monitors and the execution-class confound dissolves. |
| **2** | **Can a Repeating trigger fire at a custom time like 15:52?** | Two clone specs (§8.2). Market-close is hard-coded 3:50. |
| **3** | **Can Exit Options reference a Bot Input?** | The greenfield "PT% as a Bot Input" spec (§5.2). Nowhere documented. |
| **4** | **Can one Exit Option Preset be referenced from two different Open Position actions?** | The preset-as-unit-of-attachment design (§6.1). |
| **5** | **Is re-applying Update Position Exit Options side-effect-free?** | Any re-assertion watchdog (§6.5). |
| **6** | **What is the Final Price control's actual maximum** — 100% or 150%? | Resolves the §7 conflict. |
| **7** | **What is the automation-log retention window?** | Any liveness monitoring that looks back more than a day (§4.4). |
| **8** | **Does the June error counter show ≥10 on the Fortress bots in June?** | Confirms or kills the Excessive Errors Failsafe hypothesis (§4.5). |

---

## 10. The `EXIT OPTIONS` toggle — existence established, MECHANISM still unverified

*Corrected 2026-07-31. This section previously called the toggle `[SINGLE-SOURCE]` and said its
sole source was one support rep. **That was wrong** — there are two independent observations of
its existence. The distinction that actually matters is between the toggle EXISTING and the
toggle DOING what the lapse explanation says it does.*

**Existence: [FIRST-HAND ×2].**

A per-bot `EXIT OPTIONS` ON/OFF toggle sits beside `AUTOMATIONS` at the top right of each bot's
dashboard, visible only there and never in the editor. **Two independent observations:**

1. **The OA support rep's screenshot** showing both toggles on a bot dashboard (2026-07-30).
2. **Andy's own fleet-wide observation** — both toggles read OFF on **all 35 bots**.

**It still appears nowhere in OA's documentation** — a full sweep returns nothing. That is a
docs gap, not an evidence gap: the docs demonstrably lag the product in at least three other
confirmed places (§0.2), and a first-hand observation beats a stale doc.

> ### ⚠️ WHAT REMAINS UNVERIFIED IS THE CAUSAL CLAIM
> That **flipping the toggle back ON re-arms exit-order generation** is the explanation for the
> lapse, and it is **not established.** A toggle can exist, read ON, and still produce no orders
> — that is the precise shape of the v1 failure, where the Exit Options *editor* displayed every
> setting correctly while the engine emitted nothing.
>
> The rep who supplied the mechanism also **did not know about the documented Excessive Errors
> Failsafe** (§4.5), which is an independent candidate explanation for a bot that silently stops
> firing. Neither has been tested.
>
> **Only the Day-0 order-level check settles it** — first new position, Trades list, PT row
> present. §8.3.

What the evidence set *does* contain:

- **Bot-level ON/OFF and per-automation `AUTOMATIONS` ON/OFF toggles** — [FIRST-HAND], and
  noted as *"the one config state that does not survive text capture"*. Per-**automation**,
  not per-bot, and not exit-specific.
- The **Bid-Ask Guard**, which disables Exit Options conditionally on spread width (§6.3).
- The **Excessive Errors Failsafe**, which disables all automations (§4.5).

None of these is the claimed toggle, and none refutes it — they are separate mechanisms that
could produce a similar-looking outcome, which is why the Day-0 check has to discriminate.

> **How to hold this.** The *observed failure* is not in doubt: automations resumed, every Exit
> Option stayed dead, and the editor kept displaying settings as configured. The *toggle* is not
> in doubt either. What is in doubt is that **one causes the other.**
>
> The Day-0 runbook is right to act on it — re-arm the nine leave-in-place bots, screenshot both
> toggles — because acting on it is cheap and reversible. But **a toggle screenshot is necessary
> and not sufficient**, and the runbook already says so.
>
> **If the toggles read ON at Day-0 and the Trades lists still show no PT rows, the lapse
> mechanism is refuted, not confirmed** — and §4.5 plus the docs' total silence on what happens
> to a running bot's exit conditions when billing state changes both move back into contention.
> That is the outcome to watch for, and it is why §8.3 is a hard gate rather than a formality.

---

## 11. What is NOT expressible on this platform

Recorded so nobody spends a build day rediscovering it.

| Wanted | Status |
|---|---|
| **"Condition sustained for N minutes"** | **NOT NATIVE** (§0.1). Affirmatively ruled out by the docs, not merely undocumented. Build path: the tag ladder, §6.2 / §5.3 — ~10 decision/action node pairs, consuming the 1-minute scan budget, where every rung fails *safe-looking*. |
| Intraday indicators (pivots, VWAP, intraday regime) | **NOT NATIVE** (§5.1). Daily bars cached pre-market. Webhook-fed or nonexistent. |
| Sub-second strike-touch with a latch | **NOT NATIVE.** 1-minute cadence at best. |
| Regime-conditional branching at a breach | **NOT NATIVE.** No mid-trade branching. |
| True "defang" as a single action (buy back the short, ride the long) | **NOT NATIVE.** Multi-leg workaround required. |
| Any condition referencing its own past | **NOT NATIVE** (§0.1). |

> ### ⛔ CORRECTION OF RECORD — the "Conditional" hedge was never buildable
> The v1 file's §14 defined the `Conditional` mechanic as *"close the tested spread only after
> price is sustained ~$1 past the strike for ~10 minutes."* **The platform cannot express time
> persistence at all.** Whoever built `QQQ-IC-0DTE-HedgeD-Conditional` hit that wall and
> substituted the nearest expressible thing — **position age** (`open 30 minutes or more`) —
> without recording the substitution.
>
> The bot lost **−$15,376** testing an immediate $1-ITM stop while its documentation, its
> config record and its automation tree all agreed it was testing a 10-minute sustained
> breach. **No amount of config-vs-reality diffing catches this**, because the config record
> and the tree agreed with each other and both were wrong about the intent.
>
> **This is a distinct failure pattern: an undocumented substitution made at a platform limit.**
> The defence is not better diffing — it is pre-registration that names the mechanic *and* the
> primitive it will be built from, so a substitution has something to contradict.

---

## 12. Integrations

- **Broker:** Tradier (margin, options level 3).
- **Webhooks:** a single webhook *"can trigger up to 10 automations in a single bot… and
  automations in multiple bots"*, and **persists across bot clones** [DOCUMENTED]. Payload
  parameters are [DOCS-SILENT]. This is the only route for externally-computed signals
  (§5.1) — and the clone persistence is a trap worth knowing before cloning.
- **OA outage = no execution and no broker-side protection** unless a broker-level bracket
  (Tradier OTOCO) sits behind the bot. OTOCO behaviour on multi-leg spreads is unverified and
  is a broker-side question, not an OA one.

---

*Sources: `docs.optionalpha.com` (swept 2026-07-29, `oa-docs-research-2026-07-29.md`), the
project's own OA capability inventory (`oa-setup-exploration-2026-07-29.md`), first-hand
captures in `data/captures/`, the Fortress and champion execution forensics, and one OA
support conversation of 2026-07-30 (§10). Platform features change and the docs demonstrably
lag the product — re-verify §9 against the running account before relying on any of it.*
