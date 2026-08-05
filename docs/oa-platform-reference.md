# Option Alpha platform reference — v2

*REWRITTEN FROM SCRATCH 2026-07-31 for Bot Fleet v2. Supersedes the v1 file at
`~/bot-fleet/docs/oa-platform-reference.md` entirely — do not read the old one.*

> **This file GATES the greenfield builds and the four clone specs.** Six carried docs cite it.
> The v1 version had two defects serious enough to require a rewrite rather than a patch:
> its §14 defined a hedge mechanic that **cannot be built on this platform**, and
> Exit-Options-panel-as-evidence was implicit throughout — the exact reasoning that let a
> dead profit target look alive for four months.

> ### 📌 AMENDED 2026-08-03 — this file is no longer frozen. Read §0.2 before adding to it.
> Twelve marked blocks were added the same day: **4 × `⛔ CONTESTED`** (§2 clone trap, §4.1
> market-open/close, §6.4 order-lifetime tag, §8.2 the 15:52 premise), **3 × `✅ RESOLVED`**
> (§6.2 Touch, §7 SmartPricing table, §7 final-price conflict), and **5 × `📝` appends**.
> **Nothing was deleted** — every contested claim stands with its original text beneath the banner.
> **§8's build instructions were marked but not rewritten** and remain gated.
> `§9` rows 1, 2 and 6 are now answered; row 4 is narrowed.

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

> ### ⛔ PROVENANCE RULE — added 2026-08-03
> **A tier tag must name what was observed and when. Citing another project document is NOT
> provenance.** §2's clone trap carried `[FIRST-HAND — runbook §2 step 2]`; the runbook asserted
> the same claim with no observation behind it. Two documents vouching for each other is a
> citation loop, and it survived because the tag *looked* like evidence.
>
> **`[FIRST-HAND]` requires a value that was read** — a DOM field, a hidden-input payload, a
> screenshot. **Inference from absence is not observation.** "I did not see a control" is not a
> finding; it is a screen that was not opened. (Written the same day it would have caught a wrong
> claim about Exit Option presets — see §6.1.)
>
> ⚠️ **Do not quote this file, or any file, from a stage-back or a cached read.** On 2026-08-03 a
> read of this file returned a paraphrase of §2's clone-trap paragraph — same meaning, different
> sentences — while the bytes on disk were unchanged (hash identical). **Verify a quotation against
> the file itself before relying on it.**

> ### 📝 THE `⛔ CONTESTED` CONVENTION — added 2026-08-03
> When an observation falsifies a claim in this file, the claim is **marked in place, dated, and
> left standing** — not deleted. The banner names the contradicting evidence so no session reads
> the old claim as authority; the original text survives so the record can be audited.
> **Rewriting a contested section requires Andy's authorization. Marking it does not.**
>
> Appends backed by a value that was read or a sentence that can be quoted need no authorization.
> **§8 stays gated** — it is build-plan-adjacent. §8.2 below is *marked* but not rewritten.

> ### 📝 AMENDED 2026-08-05 — the authorization split, at Andy's explicit instruction
> **The gate is on decisions, not on corrections.**
>
> - **Correcting a claim in this file that has been falsified needs no authorization** — provided it
>   is a **dated banner** citing a **quotable sentence** (an `oa_facts.csv` fact ID with its
>   verbatim quote) or **a value that was read first-hand on a stated date**, and the original text
>   is **left standing beneath it** per the convention above. This makes explicit what every
>   2026-08-03 `⛔ CONTESTED` block already did: the banner that says *"the claim above is false,
>   and here is the quote"* is an append, and appends backed by a quotable sentence were already
>   free.
> - **Replacing or deleting the original text still requires Andy's authorization.** Marking is
>   free; overwriting is not. The record must stay auditable.
> - **§8 stays gated**, unchanged — it is build-plan-adjacent, and `build-plan.md` changes require
>   an explicit "amend the plan".
> - **Inference from absence is never a correction.** The provenance rule above is unaffected and
>   is not relaxed by anything in this block.
> - **Verification is unchanged and not optional:** a direct `device_bash` sha256 plus a
>   single-match grep of the new text. A tool success message is not verification (`CLAUDE.md`
>   §9.1a). Every directly-applied correction is listed at commit review, where Andy may veto it.
>
> Full regime: `CLAUDE.md` §5, *"Doc-edit authority"*. Worked example of the split applied to
> sixteen concrete edits: `docs/r-edit-authorization-2026-08-05.md`.

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

> ### ⛔ CONTESTED 2026-08-03 — THIS CLAIM IS FALSE. Do not act on it.
> **Cloned bots do NOT share automations by reference.** Direct test: the CLONE's ScannerA was
> renamed, saved, hard-reloaded, and the ORIGINAL read back **unchanged** in both name and
> allocation. A shared object would have propagated. Corroborated structurally — OA's Automation
> Library is **opt-in** ("Add to My Library"), reports per-automation usage, and contained exactly
> **one** shared automation fleet-wide (`Defang-Mon-S2-StrikeTouch` → 2 bots, both §2A
> archive-directly bots). **Sharing is opt-in via the Library. Cloning copies.**
>
> The `[FIRST-HAND]` tag below cites `runbook §2 step 2` — the other document asserting the same
> claim. That is a citation loop with no observation behind it, and it is why §0.2's provenance
> rule now exists. **Consequence: the fork step is a no-op** and can come out of the clone ritual
> for all four clones, removing a `Delete` from the procedure.
> **Original preserved below for audit; rewrite pending authorization.**

> ⚠️ **THE CLONE TRAP.** A cloned bot shares its parent's automations by reference. Edit the
> clone and you have edited the original; edit the original later and you silently change the
> clone. Fork every automation via **Copy** immediately after cloning, then confirm the clone's
> list points at the copies. [FIRST-HAND — runbook §2 step 2]

> ⚠️ **SYMBOLS DROP SILENTLY ON CLONE.** The Symbols panel is not carried over. A bot with no
> Symbols looks fully configured and simply never scans. Re-add them. [FIRST-HAND]

> **📝 Observed 2026-08-03 — INAPPLICABLE on the Fortress pair, for a reason worth knowing.**
> The Symbols panel reads `No symbols yet` on **both** original and clone. The symbol is not in the
> watchlist at all — it lives **inside the automation** (`Loop QQQ` + action `Symbol: QQQ`) and
> carried across the clone correctly. **This trap does not bite a bot whose symbol is
> automation-resident.** It still bites one using the Bot Symbols loop.
>
> ⚠️ **Three clone traps that ARE real and appear in NO document** (first-hand, 2026-08-03):
> **Allocation resets to a flat `1000`** in the Clone dialog (original `$100,000` — a silent 100×
> sizing error on a bot that looks fine on the dashboard), **Bot Group drops to `None`**, and
> **Tags drop to empty**. Of the two traps this file *does* document, one is false (above) and one
> is inapplicable here — while the three that bite were undocumented.

> ### 📝 SHARPENED 2026-08-05 — it is worse than silence. The docs address cloning and get it wrong.
> **OA-0845** [DOCUMENTED], `tools/clone-bot-templates`:
> > *"With a single click, you can add a cloned bot to your portfolio, complete with all the
> > settings and strategies of the original bot."*
>
> Allocation reset to a flat `1000`, Bot Group dropped to `None` and Tags dropped to empty are
> **not** "all the settings and strategies". Per §0.2 the screenshot beats the doc and the three
> traps stand **[FIRST-HAND 2026-08-03]** — but record this as a **documented claim contradicted by
> observation**, which is stronger ammunition than "appears in NO document". Doc-side corroboration
> that clone drift is a known problem: **OA-0721** — users are told to confirm Automation and Bot
> Input values after upgrading or cloning a bot, *"not only can this result in subpar performance
> for you, but it can also misrepresent the bot template's performance on the Top Bots page."*
> `oa-reconciliation-report.md` R-07.

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

> ### 📝 APPENDED 2026-08-04 (Tier 1 audit) — the trip condition is broader than stated below.
> > *"If a bot has reached an **allocation or position limit**, the scanner turns off **and a
> > warning is displayed**."* — `tools/bots/safeguards` [DOCUMENTED]
>
> Two additions: **the allocation limit trips scanners too**, not only the position limits; and
> **a warning is displayed** — a detectable signal, which matters for the liveness work in §4.4,
> since it distinguishes "scanner off because it hit a limit" from "scanner off because the bot is
> dead". Also verbatim: *"Position limits are for opening positions only; there is no limit on the
> amount of closing positions."*

**Defaults allow 10 daily / 10 total, both editable. There is no limit on closing.** When a
limit trips, **scanners are automatically turned off** until there is room [DOCUMENTED,
`§ safeguards`] — which makes the daily limit a usable interlock (§5.4).

> ### ⛔ IC = 2 POSITIONS [PROJECT-RULE]
> OA models **each spread as a separate position**. A full iron condor is **two** positions —
> the call spread and the put spread. A one-IC-per-day bot needs limits of **2, not 1**, or one
> side never opens. Ten re-entries of a single IC is a daily limit of **20**, not 10.
> Docs are silent on this; the project rule stands and is load-bearing everywhere.

> ### ✅ §9 CHECK #9 ANSWERED 2026-08-04 — **limits CANNOT exceed 10.**
> **[FIRST-HAND — Bot Safeguards panel on `QQQ-IC-0DTE-Fortress Clone`, 2026-08-04.]**
> Both limits are **hidden inputs behind pickers**, not number fields — so there is no `max`
> attribute to read and nothing to type a larger value into:
>
> - `posLimitDay` (Daily Positions) — picker offers **`1` … `10` only**. Read `2`.
> - `posLimit` (Position Limit) — picker offers **`1` … `10` only**. Read `2`.
> - `seed` (Allocation) — `type=number` **`min="250" max="100000"`**. Read `100000`. The ceiling
>   is the Pro plan's per-bot cap (`Settings → Membership: PER BOT $100k`), enforced client-side.
> - Day Trading — two-item picker, `0` **Allowed** / `1` **Blocked**. Read `Allowed`.
>
> ⛔ **This bites the §3 [PROJECT-RULE] box directly above.** "Ten re-entries of a single IC is a
> daily limit of **20**, not 10" is arithmetically right and **not expressible**. The product caps
> the field at 10, so an IC bot's real ceiling is **five** re-entries per day, not ten. Any
> re-entry spec above 5 ICs/day must be redesigned or split across bots — it cannot be configured.
>
> Verified by hard reload: Safeguards still read $100,000 / 2 per day / 2 at once / Allowed.
> Nothing was saved.

**Allocation caveat.** Max risk is an *at-expiration* concept. Exit-side risk can exceed entry
allocation when spreads blow out. With percentage allocation above 50%, OA deliberately shrinks
later positions to avoid exceeding 100%.

> ⚠️ **[UNVERIFIED] — flagged 2026-08-04 (Tier 1 audit).** The percentage-allocation-shrinking
> claim is **not on the safeguards page** and carries no source anywhere in this file. It sits in a
> section whose other claims are all [DOCUMENTED], which makes it read as documented. **Treat as
> unsourced until someone finds the page or observes it.** Sizing decisions must not rest on it.

> ### ✅ RESOLVED 2026-08-05 — the claim IS sourced. The audit looked on the wrong page.
> It is not on `tools/bots/safeguards`. It is on
> `technical-documentation/platform/automation-behavior`, verbatim:
> > *"If you attempt to open multiple positions using a percentage-based allocation greater than
> > 50%, the contract/share amount of a subsequent position is intentionally reduced to avoid
> > allocating more than 100% of bot capital."* — **OA-0083** [DOCUMENTED]
>
> **Retag [DOCUMENTED]. The [UNVERIFIED] flag above is lifted** — sizing may rest on this again, as
> documented platform behavior rather than folklore. The flag's own release condition ("until
> someone finds the page") is met. `oa-reconciliation-report.md` R-05. `docs/state.md`'s Tier-1
> list is updated in the same pass.

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

> ### ⛔ CONTESTED 2026-08-03 — "neither is adjustable" is contradicted on two independent lines.
> **(i) The running product.** The live `Add Automation` → Schedule menu renders these two entries
> as **`Market open — At scheduled time in settings`** and **`Market close — At scheduled time in
> settings`** — not as fixed 9:40/3:50 times.
> **(ii) OA's own current documentation.** The Exit Options page states the 9:31am→1-minute-before-
> close window is **customizable via Settings** (§6). Both point at the same Settings surface.
>
> ### ⛔⛔ UPGRADED TO **CONFIRMED FALSE** 2026-08-04 (Tier 1 audit) — third line of evidence,
> ### and it was on the file's OWN cited page all along.
> `tools/bots/automations.md` — the page the quotation above is taken from — also says:
> > *"In your settings, you can customize when automations run, from as early as 9:31 am EST until
> > **5 minutes before the market close**."* [DOCUMENTED]
> and *"Market open automations run first **at the time you specify** automations to begin."*
>
> **"Neither is adjustable" is not merely contested — it is false, and it was falsifiable from the
> source this section already cites.** The 9:40am/3:50pm figures are DEFAULTS, not fixed times.
> **§8.2's premise collapses entirely.**
>
> ⚠️ **And it hands us the platform-wide cap:** automations may run until **5 minutes before the
> close = 15:55** — exactly the `max="15:55"` observed on the Custom time input. Two independent
> sources agreeing. **15:52 sits inside the cap**, which is why the backstop built on 2026-08-03 is
> legal rather than lucky.
>
> *Original 2026-08-03 note, superseded: "not yet verified in Settings directly… the conclusion
> drawn from it is contested."*

> **📝 Observed 2026-08-03 — the live trigger vocabulary, with undocumented per-bot SLOT LIMITS.**
> `Scanner` — Every scan to find new positions — **2/5** · `Monitor` — Every scan to monitor open
> positions — 0/5 · `Date` — At a specific date and time — 0/10 · `Repeating` — On a recurring
> schedule — 0/10 · `Market open` — 0/5 · `Market close` — 0/5 · `Position opened` — 0/5 ·
> `Position closed` — 0/5 · `Webhook` — 0/10 · **`Button` — Add a button to bot dashboard — 0/10**
> (a tenth type absent from the documented list quoted above).
> **Each bot has a bounded budget per trigger class.** The 15:52 backstop spends 1 of 10 Repeating
> slots. Nothing in OA's docs states these limits.
> ### ✅ RESOLVED IN THE PRODUCT 2026-08-04 — the Settings surface is real, it is called
> ### **Bot Schedule**, and it carries TWO INDEPENDENT WINDOWS, not one.
> **[FIRST-HAND — DOM read of `app.optionalpha.com/settings`, 2026-08-04.]** Values are the
> `input.value` of each named field, not label text:
>
> | Control | Field | Value read | Bounds read |
> |---|---|---|---|
> | Automations — start | `scanstart` | `09:31` | `type=time min="09:31" max="15:30"` |
> | Automations — end | `scanend` | `5` (“5 minutes before market close”) | picker floor **5** → **15:55** |
> | Exit Options — start | `exitstart` | `09:31` | `type=time min="09:31" max="15:30"` |
> | Exit Options — end | `exitend` | `1` (“1 minute before market close”) | picker floor **1** → **15:59** |
>
> Both end-pickers offer `5,6,7,8,9,10,15,20,25,30,45,60` minutes before the close (the Exit
> Options one also offers `1,2,3,4`). **9:40 / 3:50 are neither fixed nor even the current
> setting** — this account runs 09:31. The claim struck above is closed on a third line of
> evidence, this one first-hand.
>
> ⚠️ **This file has been treating one window where the product has two.** The automation
> window and the Exit Options window are configured separately and currently differ by four
> minutes at the close. §6's “9:31am to 1 minute before market close” and §4.1's automation cap
> are **not the same setting**.
>
> ⚠️ **And a footnote nobody had read**, verbatim from the same card:
> > *"Repeating and date/time scheduled automations are not affected by this schedule and run at
> > the selected date and time even if it's outside the range defined above"*
>
> The 15:52 backstop is a **Repeating** trigger, so the Bot Schedule does not bind it at all.
> (The `max="15:55"` on the Custom time input still does. Two different limits — do not merge them.)
>
> Verified by hard reload: all seven fields unchanged afterwards. Nothing was saved.

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

> ### ⚠️ APPENDED 2026-08-04 (Tier 1 audit) — TIMING IS NOT GUARANTEED. This was missing entirely.
> > *"All user automations are pushed into a **distributed work queue and executed in parallel by
> > worker processes. There is no guarantee an automation will run exactly on the 15-minute
> > marks**."*
> > — `technical-documentation/platform/automation-behavior.md` [DOCUMENTED]
>
> **A scheduled automation is not promised to fire at its stamped minute.** Consequences:
> - **The 15:52 flat-close backstop has an 8-minute buffer to the bell, not a guaranteed slot.**
>   That is probably ample, but it is a buffer, and it compounds with the unresolved DST question
>   (§8.2). Do not design a backstop whose margin is smaller than the scheduling jitter.
> - Any attribution rule keyed on an exact timestamp — including the `:00`/`:00` vs `:01–:02`
>   sibling-close test in §8.3 — is reading a **jittered** clock. The test is still sound (the gap
>   is what matters, not the absolute minute) but it is not a precision instrument.
>
> Same page, also missing here: the default scan interval runs *"beginning approximately 15 minutes
> after the market opens, and ending at 15 minutes before the market close"*, with the last interval
> at **3:45 ET**. ⚠️ **Three different windows now exist in this document and they are not the
> same:** default scan cadence ends **15:45**; automations are customizable until **15:55**;
> Exit Options run until **1 minute before close (~15:59)**. Do not conflate them.

### 4.3 Loops

**Position loop** (oldest → newest, always), **Symbol loop**, and **Bot Symbol Loop** over a
dynamic watchlist. Loops inside a synchronous group run sequentially — one item fully through
the tree before the next.

### 4.4 Bot logs record NON-actions [DOCUMENTED]

> *"Bot logs offer a detailed automation history, allowing you to see exactly **what actions
> your bot has taken—or not taken—during each automation run**."* Filterable by **date**, by type
> (Scanner / Monitor / Event / Button) and by errors or warnings. — `tools/bots/automation-logs.md`

This is the **only** way to distinguish a correctly-gated bot from a switched-off one.
`DIR-SPX-PutVIX22-SL75` took zero positions in 22 days because its VIX≥22 gate correctly never
fired — from position data alone that is indistinguishable from a dead bot. The log closes it:
**a scanner run with no entry = healthy. Zero log rows = presumed OFF or failsafe-tripped.**

⚠️ **Log retention window is [DOCS-SILENT].** Any monitoring design that depends on looking
back more than a few days is unproven.

> ### ✅ §9 CHECK #7 ANSWERED 2026-08-04 — and the answer is **two different numbers.**
> **[FIRST-HAND — bot Log tab, `QQQ-IC-0DTE-Fortress`, 2026-08-04.]**
>
> - **The date FILTER reaches back exactly 3 weeks of weekdays.** It offers `Today`, then
>   `LAST WEEK` (Fri Jul 31 → Mon Jul 27), `2 WEEKS AGO` (Fri Jul 24 → Mon Jul 20), `3 WEEKS AGO`
>   (Fri Jul 17 → **Mon Jul 13**). `scrollHeight === clientHeight`, so nothing is hidden below.
>   Note **Mon Aug 3 — the immediately preceding weekday — is NOT offered**: the grouping starts at
>   "last week", so the current week's earlier days fall through the gap.
> - **The stored data goes back at least 141 days.** The unfiltered stream still serves Jul 2 in
>   full, and the error stream reaches **`Mar 16, 2026`**.
>
> **Retention is not the constraint — the filter is.** Anything looking back more than 3 weeks
> must page the raw stream via a `Load more` button, which is slow and, at ~229 rows in, stopped
> yielding while still displaying the button. Treat "reachable by filter" and "still stored" as
> two separate budgets in any liveness design.
>
> 📝 **Capture handle:** every log row carries a `title` attribute holding a **year-bearing
> timestamp** (e.g. `Apr 16, 2026 3:55PM`). Use it. The visible date *group header* is unreliable —
> on one bot it did not render at all, on another it re-rendered mid-scroll and changed value.
>
> 📝 **Third `innerText` trap, same family as the two already recorded.** The `Date`, `Time` and
> `Type` filter chips render their labels via CSS, so `innerText` on them is the **empty string**.
> They are `div.input-ct.filterbtn-ct` wrappers around hidden inputs named `date`, `time`,
> `autotypes`. A reader trusting `innerText` concludes the filters do not exist.

### 4.5 The Excessive Errors Failsafe [DOCUMENTED]

> *"The 'excessive errors failsafe' is an automatic protection mechanism that **disables all
> automations when a bot experiences 10 errors within a single day**."*
> — `technical-documentation/troubleshooting/excessive-errors-failsafe.md`

Ten errors in one day, on one bot, disables **all** its automations. **Re-enabling is manual.**

> ### 📝 APPENDED 2026-08-04 (Tier 1 audit) — three facts from the same page, none of them here.
> - **Re-enabling does not make it safe: it re-trips.** You *"can always turn automations on
>   again"*, but **if another error occurs that same day the automations turn off again.** A bot
>   switched back on can die a second time the same session, silently.
> - **The error count resets *"the next trading day."*** So the counter is per-day, not cumulative.
> - **Where to look:** errors surface **on the homepage** and via **"errors" in the bot dashboard's
>   activity summary**, with detail in the bot log and automation log. ⚠️ **This is the surface for
>   §9 check #8** (did the Fortress bots show ≥10 errors in June) — that check was never actionable
>   before because nobody had recorded where the counter lives.
> - The page refers specifically to *"automation error"*, which suggests **not all error types count
>   toward the threshold**; which are excluded is [DOCS-SILENT].

This is a documented mechanism by which a working bot silently stops firing, and it was unknown
to this project until 2026-07-29 — including to the OA support rep consulted about the lapse.

> **Carry the uncertainty:** it is a **hypothesis** for the 2026-06-12 Fortress regression, not
> the answer. Fortress kept emitting *entry* orders through 6/26 while emitting no exit orders,
> which is not a whole-bot shutdown. State it as a hypothesis in pre-registration and check the
> June error counter before claiming it.

> ### ⛔ §9 CHECK #8 ANSWERED 2026-08-04 — **the hypothesis is DEAD. No June errors, on either bot.**
> **[FIRST-HAND — bot Log → `Errors` filter (`?status=,error`), 2026-08-04.]** The list is
> newest-first, and every row's `title` attribute carries the year.
>
> | Bot | Error days found | Count | Window |
> |---|---|---|---|
> | `QQQ-IC-0DTE-Fortress` | **Apr 16, 2026** | 91 | 1:31PM – 3:55PM |
> | `QQQ-IC-0DTE-Fortress` | **Mar 16, 2026** | 138 (+ more unloaded) | 1:31PM – 2:40PM |
> | `QQQ-IC-0DTE-Fortress-NoPT50` | **Apr 16, 2026** | 91 | 1:31PM – 3:55PM |
>
> **The newest error on either bot is `Apr 16, 2026 3:55PM`.** Because the list is newest-first, a
> June error would have to sit above these rows. There are none. **Neither Fortress bot logged a
> single error in June 2026.**
>
> → The Excessive Errors Failsafe is **not** the explanation for the 2026-06-12 exit-order
> regression. The caveat directly above — that entry orders kept flowing while exits stopped,
> which is not a whole-bot shutdown — was the right instinct, and the counter now confirms it.
> **Do not carry this into pre-registration as a live hypothesis; carry it as a closed one.**
>
> ⚠️ **What the counter DOES show is still worth keeping.** Both March and April days are far
> above the 10-error threshold, so the failsafe plausibly *did* fire on those days — on the **entry
> scanners** (`Fortress-ScannerB-CallSpread`, `FortNoPT-Scan-Call`), months before the lapse. The
> mechanism is real and this fleet has tripped it. It just did not trip it in June.

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

> **📝 Appended 2026-08-04 (Tier 1 audit):** the documented *consequence* is that a looping bot
> *"reach[es] its daily and/or total position limit"*, and the docs name **position limits and
> capital allocation limits** as the designed safeguard against exactly this. **That corroborates
> §5.4's interlock** — keeping the daily limit at 2 is not a project invention, it is the
> platform's own stated defence. The docs' other advice is procedural: test automations and paper
> trade first.

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
> frame."* The "intraday" toggle **shifts all indicator bars forward** and substitutes the current
> market price for the most recent close as the final daily bar *(mechanic corrected 2026-08-04 —
> the previous wording omitted the forward shift)*; a true
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
~~The greenfield spec ("PT% as a Bot Input") **depends on this and it has not been checked.**~~
See §9.

> ### 📝 CORRECTED 2026-08-05 — the LAST SENTENCE only. **Read the split carefully.**
> *Struck text left standing per §0.2. This correction narrows a status claim; it decides nothing
> and it does NOT lift the [DOCS-SILENT] tag above, which is load-bearing for greenfield check
> **C0a**.*
>
> **✅ CHECKED, at the AUTOMATION-Input tier — [FIRST-HAND 2026-08-04, Exit Options editor on
> `QQQ-IC-0DTE-Fortress Clone`; §9 row 3].** Exit Options **can** be linked: the 🔗 on the Exit
> Options row (`a.btn.gray.opts-btn.param-opts` → `i.fa-link`) opens `Add Input / Exit Options`.
> ⛔ **But the input's TYPE is the WHOLE exit bundle** — inside the Default Value editor
> `i.fa-link` count is **0**, so there is no 🔗 on Profit Taking % or on any individual field.
> **The "PT% as a Bot Input" design is therefore NOT EXPRESSIBLE.** What is expressible is
> **"Exit-Options-SET as a Bot Input"**, one variable holding a whole exit configuration swapped
> as a unit — a materially different mechanic, **ruled 2026-08-04 as D-1 Option A**.
>
> ⛔ **STILL UNVERIFIED, and the sentence above must not be read as closing it: the BOT-INPUT
> tier has never been observed.** G1/G2/G3 and §9 row 3 all exercised the **Automation** Input.
> Whether an Exit-Options input can be promoted to a **Bot** Input is greenfield check **C0a**,
> and **C0a can stop that architecture outright.** The [DOCS-SILENT] tag above stays as written.

### 5.3 Tags — the only writable state on the platform [DOCUMENTED]

> *"Bot Tags: Tags that are applied to your bot. **They do not change state and remain applied
> to the bot unless reset or untagged by the user.**"* · *"The tagging system… can be used to
> track information, categorize items, and **make decisions within your automations**."*
> — `tools/bots/tags.md`

Tag / Untag / Reset × Bot / Position / Symbol = **9 tag actions** [DOCUMENTED].

**This is the entire memory of the platform.** It is also the one build path for a sustain
condition — see §6.2.

> ⚠️ **[PROJECT-RULE] — retagged 2026-08-04 (Tier 1 audit).** "The entire memory of the platform"
> is **this project's inference, not a documented statement.** The tags page does not claim tags are
> the sole writable state; it says only that bot tags persist and can be used in decisions. The
> inference is well-supported by §0.1's keyword sweep and is probably right — but it sits inside a
> `[DOCUMENTED]` section and reads as quoted fact. **§0.1 and §11 both rest on it**, so its tier
> matters. Also unverified on the same page: tag limits, expiry, and **whether tags persist across
> a clone** — the last is directly relevant to the clone ritual and is [DOCS-SILENT].
>
> ⚠️ The **second** quotation above (*"The tagging system… can be used to track information,
> categorize items, and make decisions within your automations"*) **could not be located** in the
> 2026-08-04 re-read, which returned *"Tags can be used in conjunction with decisions to create
> powerful and flexible automations."* Same meaning, different sentence. **Re-verify or drop the
> quotation marks.**

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

> ### 📝 [CONFLICT] 2026-08-05 — the START time is docs-internal-contradictory. The product settles it.
> Two DOCUMENTED pages disagree on the start:
> > *"Exit Options can run from 9:31 am ET until 1 minute before the market close. You can
> > customize the Exit Options schedule in your Settings."*
> > — `tools/managing-positions/exit-options` — **OA-0870**
> > *"The user-defined parameters are checked every one market minute between 9:40 AM and 3:59 PM
> > Eastern."*
> > — `technical-documentation/platform/automation-behavior` — **OA-0085**
>
> The **end** (~15:59 / 3:59 PM) agrees. The **start** is 9:31 on one page and 9:40 on the other.
> Retag the START **[CONFLICT]**; the sentence above may no longer be read as a single documented
> window. The §4.2 "three windows" append gains a fourth number.
>
> ✅ **For THIS account the product has already settled it, first-hand.** §4.1's
> `✅ RESOLVED IN THE PRODUCT 2026-08-04` block reads `exitstart` = `09:31`
> (`type=time min="09:31" max="15:30"`) and `exitend` = `1` → 15:59; §6.1a confirms the modal
> header renders `9:31am to 1 minute before market close` **live from that same Bot Schedule**.
> **09:31 is the operative value here — read, not inferred.** The conflict is a docs defect to
> carry, not an open question about this account. No project design depends on the start minute.
> `oa-reconciliation-report.md` R-06. Applied as narrowed, at Andy's explicit ruling 2026-08-05.

> **📝 Appended 2026-08-03 — TWO documented facts this section was missing.**
>
> **1. THE WINDOW IS CUSTOMIZABLE.** The docs give the window and then state it is **customizable
> via Settings**. This file recorded it as fixed. ⚠️ The Exit Options modal renders the phrase
> *"9:31am to 1 minute before market close"* **as a hyperlink** — present in the 2026-08-03
> capture, read as plain text and not followed. Same Settings surface as §4.1's contested claim.
>
> **2. ⛔ EXIT OPTIONS RUN EVEN WHEN AUTOMATIONS ARE OFF.**
> > *"Exit Options always run, even if your automations inside a bot are turned off."*
> > — `tools/managing-positions/exit-options.md` [DOCUMENTED]
>
> Two load-bearing consequences:
> - **A bot with `AUTOMATIONS` OFF is NOT inert if it holds positions** — its Exit Options still
>   fire. Any "is this bot parked / is it safe" judgement must read **both** toggles, not one.
> - **This is the documented reason a flat-close backstop belongs on the AUTOMATIONS side**
>   (§8.2). v1's failure was Exit Options dead while automations ran; a backstop living *inside*
>   Exit Options would have died with them. The architecture was right for a reason this file
>   never stated.

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

> **📝 Appended 2026-08-03 — the quote above stops ONE SENTENCE SHORT of the answer.**
> The docs continue: *"**You can name your presets for easy identification.**"* [DOCUMENTED]
> **Presets ARE nameable, so `build-plan.md` §2B/§8.1's "NAMED Exit Option Preset" is expressible
> exactly as written.**
>
> ⛔ **A retracted claim, recorded because the error class matters more than the claim.** A
> 2026-08-03 session opened the Exit Options modal, saw a `Presets` picker and a `Save as presets
> for short option positions` checkbox, saw no name field, and concluded "NAMED preset" might not
> be expressible. **That was wrong.** The checkbox was never ticked, so the naming step was never
> reached — **absence inferred from a screen that was never opened.** This is precisely the error
> §0.2's provenance rule now forbids.
>
> **Observed first-hand 2026-08-03:** the control exists, and the account holds **zero** presets —
> the picker returns the exact string `"No presets found for short option positions"`. It is scoped
> by **position type**, which is suggestive for the cross-automation question (both an IC's put and
> call spreads are short option positions) **but is not observation. §9 check #4 stands.**

> ### ✅ §9 CHECK #4 ANSWERED 2026-08-04 — **YES, and wider than the check asked.**
> **[FIRST-HAND — direct test on `QQQ-IC-0DTE-Fortress Clone`, 2026-08-04.]**
>
> 1. Baseline re-confirmed on the put side: `"No presets found for short option positions"`.
> 2. Ticked `Save as presets for short option positions`. **A name field appeared** — `name="pretext"`,
>    pre-filled `Profit: 50%, Expiration: 10 minutes`. Set to `TIER2-CHECK4-PUTSIDE`. Saved the
>    modal → the action → the automation.
> 3. Hard-reloaded. Opened the **call side** — a **different automation**
>    (`Fortress-ScannerB-CallSpread` → `Open Short Call Spread`) — and opened its `Presets` picker.
>
> The picker returned `{"data-value": "UIfw5TkkCRF1517858152565216101", "text": "TIER2-CHECK4-PUTSIDE"}`.
>
> **One preset serves both Open Position actions, across two separate automations.** Note the id
> namespace: **`UI…`**, not `BOT…` or `RT…` — presets are **account-scoped user objects**, not
> bot- or automation-scoped. §6.1's cross-automation [DOCS-SILENT] is closed and the greenfield
> spec's assumption holds. The naming step also confirms the 2026-08-03 retraction was correct.
>
> 📝 **Residue from this test, recorded rather than tidied away:** the account now holds preset
> `TIER2-CHECK4-PUTSIDE`; `Fortress-ScannerA-PutSpread-CLONE` was saved and its Open Position
> `exits` blob **re-serialized** — numeric payload byte-identical (`^^0.5|0.01^$0` before and
> after), but the `text` label changed `"Profits: 50%, …"` → `"Profit: 50%, …"` and the sig gained
> an `xevents` key. Cosmetic on inspection, persisted through a hard reload, **and it is still a
> diff on a pilot bot.** `Fortress-ScannerB-CallSpread` was closed without saving.

> **A preset makes the VALUES consistent, not the ATTACHMENT.** A preset can still be attached
> to one Open action and omitted from the other. It converts a silent asymmetry into a visible
> one — a smaller failure class, not none. The per-side fire-rate assertion still has to run.

### 6.1a The complete Exit Options panel, field by field — [FIRST-HAND 2026-08-04]

*Read from the live modal on `QQQ-IC-0DTE-Fortress Clone` → `Open Short Put Spread`, 2026-08-04.
Values are `input.value` on the named hidden fields, not label text. This closes §9 check #10.*

The modal's own header, verbatim:

> *"Your bot checks your position every 1 minute from 9:31am to 1 minute before market close and
> automatically attempts to close it if any of these criteria are met."*

— and `9:31am to 1 minute before market close` **is a hyperlink**, not prose. It renders live from
the Bot Schedule (§4.1's resolution block): `exitstart` = `09:31`, `exitend` = `1`. The two
surfaces agree. This was §6 defect (d), predicted 2026-08-03 and now confirmed.

| # | UI label | Field | Value on the put side |
|---|---|---|---|
| 1 | Profit Taking % | `profits` | `0.5` |
| 1b | ↳ PRICING | `smprofits` | `normal` |
| 2 | **Profit Taking $** | `dprofit` | empty |
| 3 | Price Target | *(read blocked)* | empty |
| 4 | Stop Loss % | `stoploss` | empty |
| 5 | **Stop Loss $** | `dstop` | empty |
| 6 | Trailing Stop | `tstop` | empty |
| 7 | Touch | `touch` | empty |
| 8 | Expiration | `expdays` | `0.01` |
| 8b | ↳ PRICING | `smexpdays` | `{"text":"Market","smart":"market"}` |
| 9 | **Avoid Events** | — | None |
| 10 | Earnings | `epsdays` | empty |
| 11 | ☐ Wait at least 1 day to avoid pattern day trading | `chposLimitDay` | unchecked |
| 12 | ☐ Disable exit options if bid/ask exceeds $ | `chbidask` / `bidask` | unchecked / empty |
| 13 | ☐ Save as presets for short option positions | → reveals `pretext` | unchecked |

**`Profit Taking $` and `Stop Loss $` both exist.** They were absent from the 100-page docs corpus
(Phase 6, R-13) and are now first-hand confirmed — `hedge-research.md` §9's fixed-$ stop rungs are
buildable. **`Avoid Events` exists** and opens a sub-modal: *"Close positions on the day before an
important event. Select the event(s) below and a time to close the position."* with a multi-select
— `FOMC Meeting`, `CPI Release`, `PPI Release`, `PCE Release`, `Nonfarm Payrolls`, `Triple
Witching`, `Monthly Expiration`, `End of Month`, `End of Quarter`, `First Weekly`, `Full Moon` —
and a separate "Time … before market close" picker (default `1 hour`).

⚠️ **Item 11 is the PDT checkbox** (Phase 6 / OA-0890). It is **unchecked** on the pilot clone,
which is what a 0DTE program wants; on any bot where it *is* checked it delays closes by ≥1 day.
Add it to the §8.3 per-bot verification read.

> ### 📝 The Expiration dropdown, finally enumerated — [FIRST-HAND 2026-08-04]
> §8.2 notes this control's options *"were NOT read"*. They are, near expiry, 1-minute granular:
> `0.005` **5 minutes before** · `0.006` 6 · `0.007` 7 · **`0.008` 8 minutes before** · `0.009` 9 ·
> `0.01` **10** (the current value) · `0.011`–`0.015` 11–15 · then `0.02` 20 · `0.025` 25 · `0.03` 30 ·
> `0.035` 35 · `0.04` 40 · `0.045` 45 · `0.1` 1 hour · … · `0.6` 6 hours · `1`–`15`+ days.
>
> **`8 minutes before` exists**, so an Exit Option firing at 15:52 was expressible all along.
> §8.2's stated objection — that such an exit "does not exist" — is falsified **by the control
> itself**, not merely by inference from the window bounds. §8 is gated, so it is not edited here;
> this note records the observation against it. The architectural objection (we do not *want* the
> backstop in the Exit Options execution class) is untouched and remains the real reason.

### 6.2 THE TOUCH TRIGGER — the highest-value open question in this document

A `Touch` Exit Option is documented to exist. **What it references is not.**

> ### ✅ RESOLVED 2026-08-03 — TOUCH REFERENCES THE UNDERLYING, RELATIVE TO THE STRIKE.
> > *"The new 'Touch' Exit Option references the underlying price relative to a position's strike
> > price(s)."* — `optionalpha.com/blog/new-exit-option-for-itm-price-touches` [DOCUMENTED]
>
> It fires when the underlying is **`$X` or `X%` from in-the-money, or less**. Takes dollars or
> percent: **`$0`** exits the moment the position goes ITM; **negative** values (`-$0.50`, `-5%`)
> allow ITM penetration first; **positive** values exit *before* ITM. Documented to work on credit
> spreads **and** on long options and debit spreads.
>
> **This is the underlying-touches-strike reading — so everything in the paragraph below now HOLDS**
> rather than being conditional. `build-plan.md` §2D/§8.1's "Touch $0 on the challenged side" has a
> precise meaning: close the moment the position goes ITM.
>
> ⚠️ **Still unresolved: whether a Touch on one spread can close its SIBLING.** The source describes
> "closing iron condors", but OA models an IC as **two positions** (§3). Treat as loose phrasing,
> keep §5.4's mechanism, do not assume.
>
> ⚠️ **Process note.** This section called it "a two-minute UI check" and §9 ranked it #1 of 8. It
> was answerable from OA's own published material the whole time — one link from a page already in
> the swept docs corpus — and a 2026-08-03 session spent two failed clicks on the dropdown before
> stopping. **Read the product's own material before instrumenting it.**

> **Superseded — the original open question, preserved for audit:**
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

> **📝 Re-confirmed 2026-08-03 [FIRST-HAND]** on `QQQ-IC-0DTE-Fortress Clone`: the control renders
> as `Disable exit options if bid/ask exceeds $ ___` at the foot of the Exit Options modal, and is
> **unchecked with the dollar field empty**. The guard is OFF on the Fortress line too.

### 6.4 Mid-price, two-minute orders — carry the caveat

Exit Options evaluate the position's **mid-price**; a triggered order stays active **two
minutes**, then cancels and re-checks at the next minute. Fills are never guaranteed. For a
profit target, SmartPricing's final price is auto-set to the price that locks in the target.

⚠️ **[PROJECT-RULE, not doc-verified.]** The 2-minute lifetime and mid-price evaluation appear
in project files only; the docs do not address either. They explain the observed ~11% PT-miss
rate on thin credits, so they are probably right — but they are not documented.

> ### ⛔ CONTESTED 2026-08-03 — THE TAG ABOVE IS WRONG. The 2-minute lifetime IS documented.
> > *"Orders triggered by an exit option will remain active for two minutes; during that time,
> > **no additional orders will be sent to your broker**."*
> > — `tools/managing-positions/exit-options.md` [DOCUMENTED]
>
> **Promote the 2-minute lifetime to [DOCUMENTED].** The emphasised clause appears **nowhere in
> this folder** and is operationally significant: for those two minutes the position is
> **uncoverable by any further exit order**, so no stacked-exit design may assume a second attempt
> inside that window.
>
> The **mid-price** half remains unquoted; it is only implied, by the docs' Stop Loss definition
> ("closes position when mid-price reaches specified loss threshold"). **Leave that half as
> [PROJECT-RULE] until it can be quoted directly** — half a claim being documented does not
> document the other half.

> ### ✅ RESOLVED 2026-08-05 — the mid-price half CAN now be quoted directly. Promote it.
> The condition the block above sets is met, verbatim from `tools/managing-positions/exit-options`:
> > *"Exit Options use a position's mid-price when evaluating returns."* — **OA-0872** [DOCUMENTED]
>
> **Both halves of §6.4 are now [DOCUMENTED]**: the 2-minute order lifetime (OA-0877 / OA-0883 /
> OA-0878, quoted in the ⛔ block above) and mid-price evaluation (OA-0872). The
> ⚠️ **[PROJECT-RULE, not doc-verified.]** tag at the head of this section is therefore wrong on
> **both** counts and is superseded by this block together with the ⛔ block above it.
> `oa-reconciliation-report.md` R-04.

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

✅ **[DOCUMENTED + FIRST-HAND].** Every cell above is stated verbatim on `tools/bots/smartpricing`:
**OA-0785** *"Normal will try up to 4 prices, 10 seconds each."* · **OA-0786** *"Fast will try up
to 3 prices, 5 seconds each."* · **OA-0787** *"Patient will try up to 5 prices, 20 seconds each."*
· **OA-0784** *"…turn SmartPricing off and use a single limit, or send a market order."*
Independently confirmed cell-for-cell by the first-hand read recorded immediately below — docs and
product agree, which is rare enough in this file to be worth stating.

*(⛔ Corrected 2026-08-05, authorized by Andy. This line previously read:* ⚠️ *"**[PROJECT-RULE, not
doc-verified.]** These mode names, price counts and timings come from project files. The docs do not
state them." That was wrong on both counts —* `oa-reconciliation-report.md` *R-03. The `speedy`
internal value remains **[FIRST-HAND]** only; the docs do not give internal values.)*

> ### ✅ VERIFIED FIRST-HAND 2026-08-03 — the table above is correct in every cell.
> Read verbatim off the live SmartPricing selector on `QQQ-IC-0DTE-Fortress Clone`, with each
> option's internal value: `Normal` (**`normal`**) up to 4 prices / 10s each · `Fast`
> (**internal value `speedy`, not "fast"**) up to 3 / 5s · `Patient` (**`patient`**) up to 5 / 20s ·
> `Off` (**`off`**) 1 limit price · `Market` (**`market`**) send a market order.
> **Promote off [PROJECT-RULE] to [FIRST-HAND].**
> ⚠️ **`speedy`** — any capture-diff or config parser keying on the string "fast" will silently
> miss it.
> Also observed: selecting `Market` **collapses the Final Price ladder entirely** — a market order
> takes no limit, consistent with §7's "do not cap the flat exit's slippage".

> ### ✅ [CONFLICT] RESOLVED 2026-08-03 — the v1 file was right; the docs are wrong.
> The Final Price control is, first-hand:
> `<input name="pct" type="number" min="50" max="150" step="1" value="100">`
> **The range is 50–150.** The v1 file's **150%** claim is correct and may now be quoted as fact;
> the docs' *"0% (bid) through 50% (mid) to 100% (ask)"* is wrong for this control.
> ⚠️ **Note the FLOOR: 50, not 0.** A final price better than the mid is **not settable**, so any
> design assuming a bid-side final price is not expressible. **Closes §9 check #6.**
> The other four Final Price options observed alongside it: `Up to $X slippage from the mid price`,
> `X% of typical slippage from the mid price for symbol`, a fixed `$` price, and
> `Position trade price ×`. The docs' note that "when multiple final price options are selected,
> the best price is used" is confirmed on screen.

> **Superseded — the original conflict, preserved for audit:**
> **[CONFLICT] — FINAL PRICE CEILING.** The v1 file said SmartPricing may reach **150%** of the
> bid/ask spread. The docs describe the control as *"0% (bid) through 50% (mid) to 100% (ask)"*.
> These disagree and the conflict is unresolved. Check the Final Price control's actual maximum
> in the UI before relying on either. Do not quote 150% as fact.

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

> ### ⛔ CONTESTED 2026-08-03 — 15:52 IS BUILDABLE. It was built. The premise below is falsified.
> *Marked, not rewritten — §8 is build-plan-adjacent and stays gated. **Nothing about what to build
> has been changed here.***
>
> **15:52 is reachable.** `Add Automation` → Schedule = **Repeating** → Pattern →
> `Market Time (EST)` → **`Custom`** — a selectable option, `data-value="0"`, first in the list,
> **not** a heading — opens a modal *"Select a time from 9:31AM to 3:55PM EST:"* backed by a native
> `<input type="time" min="09:31" max="15:55">` at 1-minute step. `15:52` validates
> (`checkValidity() true`, no range error) and commits as `ntime=1552`. The visible **77-entry
> 5-minute grid is a convenience list, not the constraint.**
> Built and reload-verified on the pilot clone as `Fortress-Backstop-1552-FlatClose`:
> `Every week on Mon-Fri, 3:52pm EST`, `holidays=skip`.
>
> **⛔ The second bullet below is not merely outdated — it is UNSOUND.** It reasons that Exit
> Options run *"until 1 minute before the market close"*, therefore a 15:52 **Exit Option** cannot
> exist. **15:52 is INSIDE a window that runs to roughly 15:59.** An `Expiration: 8 minutes before`
> would plausibly reach it (⚠️ that dropdown's options were **not** read).
> **The correct objection was never impossibility — it is architectural:** the backstop's whole
> value is living in the **Events** execution class, which survives an Exit Options failure. That
> is now documented rather than inferred — see §6, *"Exit Options always run, even if your
> automations inside a bot are turned off."* **Right build, wrong stated reason.**
>
> ⚠️ **NEW, UNRESOLVED — a DST ambiguity this section does not anticipate.** The saved trigger
> serialises `startDate` as `2026-08-03T20:52:00.000Z`. 20:52 UTC is 15:52 at **UTC−5 (EST)** — but
> August is **EDT (UTC−4)**, where that is **16:52 ET, after the close.** The control is labelled
> "Market Time (**EST**)" and the summary reads "3:52pm EST". Either OA means market time loosely
> and `ntime=1552` fires at 15:52 ET year-round, or it means EST literally and the trigger drifts
> an hour under daylight saving. **`ntime` is the operative field; `startDate`'s time component may
> be a stamp only. Requires a Day-0 observation — do not assume.**

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

> ### 📝 CORRECTED 2026-08-05 — **AUTHORIZED §8 EDIT, Andy's explicit release, step 1 only.**
> *§8 is otherwise gated and nothing else in it was touched. Original struck in place per §0.2.*
> **Step 1 restated a claim falsified 2026-08-03 and corrected everywhere else in this folder** —
> it was the last surviving instance in the tree, and it sat in the build instructions.
>
> **Evidence — [FIRST-HAND 2026-08-03, direct test]:** the CLONE's ScannerA was renamed, saved and
> hard-reloaded, and the ORIGINAL read back **unchanged** in both name and allocation. A shared
> object would have propagated. Corroborated structurally: the Automation Library is **opt-in**
> ("Add to My Library"), reports per-automation usage, and contained exactly **one** shared
> automation fleet-wide (`Defang-Mon-S2-StrikeTouch` → 2 bots). **[DOCUMENTED]** corroboration
> that Library-shared automations *do* propagate: **OA-0682**. **No fact in the 1,548-fact corpus
> states that a clone shares by reference.**
>
> ⚠️ **The fork step was a NO-OP RITUAL, and removing it removes a `Delete` from the procedure** —
> the fork produced copies that then had to be cleaned up. **The real risk is narrower and still
> real:** editing an automation you have **added to the Library** changes it in **every** bot that
> uses it. That is the check that replaces the fork.
> ⭐ **This is also where the citation-loop rule came from:** §2's `[FIRST-HAND]` tag on the same
> claim cited `runbook §2 step 2` — the other document asserting it — with no observation behind
> either. See §0.2's provenance rule. **Steps 2–5 below are unchanged and all still stand.**

1. ~~**Fork ALL automations via Copy** (§2 — shared by reference).~~
   **⛔ FALSE — corrected 2026-08-05. Cloning COPIES; sharing is opt-in via the Automation
   Library.** Replace this step with: **before editing any automation, check whether it is in the
   Library.** In-Library → **Copy to fork**. Not in the Library (the default for a clone) → **edit
   it directly; no fork is needed.** Verify by `oa-ops-runbook.md` §4's two-layer check.
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
| ~~**1**~~ | ✅ **ANSWERED 2026-08-03 — `Touch` references the UNDERLYING relative to the position's strike(s).** Not a UI check; it was in OA's own docs. | **Resolved in favour of the tournament.** S1/S2 stop needing monitors, become 1-minute Exit Options running first in the cycle, and the execution-class confound dissolves (§6.2). Sibling-close via Touch still unresolved. |
| ~~**2**~~ | ✅ **ANSWERED 2026-08-03 — YES**, via `Repeating` → `Market Time (EST)` → `Custom` → native time input, `min=09:31 max=15:55`, 1-minute step. Built as `Fortress-Backstop-1552-FlatClose`. | **Both clone specs unblocked** (§8.2). ⚠️ **Replaced by a new check: is the Market open/close time configurable in Settings?** (§4.1 contested) — and **does "Market Time (EST)" mean 15:52 ET year-round, or drift under DST?** |
| ~~**3**~~ | ✅ **ANSWERED 2026-08-04 — YES, but the input's TYPE is the whole Exit-Options bundle, not a scalar.** The 🔗 on the Exit Options row (`a.btn.gray.opts-btn.param-opts` → `i.fa-link`) opens `Inputs` → `Add Input`, headed **`Add Input / Exit Options`**, with Label · Default Value · Description. Inside the Default Value editor, **`i.fa-link` count is 0** — there is no 🔗 on Profit Taking % or any individual field. | ⛔ **The greenfield "PT% as a Bot Input" spec (§5.2) is NOT expressible.** What IS expressible is "Exit-Options-SET as a Bot Input" — one variable holding a whole exit configuration, swapped as a unit. **Different design; needs an explicit decision before it is written into the spec.** |
| ~~**4**~~ | ✅ **ANSWERED 2026-08-04 — YES, and across two different AUTOMATIONS, not just two actions.** Preset `TIER2-CHECK4-PUTSIDE` saved on the put side appeared in the call side's picker as `UIfw5TkkCRF1517858152565216101`. The `UI…` namespace means presets are **account-scoped**. | **§6.1's preset-as-unit-of-attachment design is confirmed.** Its cross-automation [DOCS-SILENT] is closed. |
| **5** | **Is re-applying Update Position Exit Options side-effect-free?** | Any re-assertion watchdog (§6.5). |
| ~~**6**~~ | ✅ **ANSWERED 2026-08-03 — `min="50" max="150"`.** The v1 file's 150% was right; the docs are wrong. **Floor is 50 (mid)**, so a better-than-mid final price is not settable. | **§7 conflict RESOLVED.** |
| ~~**7**~~ | ✅ **ANSWERED 2026-08-04 — TWO numbers, not one.** Date **filter** reaches 3 weeks of weekdays (oldest `Mon Jul 13`, and yesterday `Mon Aug 3` is not offered). Stored **data** reaches `Mar 16, 2026` — ≥141 days. | **§4.4 answered.** The filter, not retention, is the constraint. Beyond 3 weeks you must page `Load more`, which stalls. |
| ~~**8**~~ | ⛔ **ANSWERED 2026-08-04 — NO. Zero June errors on either Fortress bot.** Newest error on either is `Apr 16, 2026 3:55PM`. Error days found: Apr 16 (91) and Mar 16 (138+) on `QQQ-IC-0DTE-Fortress`; Apr 16 (91) on `-NoPT50`. | **KILLS the Excessive Errors Failsafe hypothesis for the 2026-06-12 lapse (§4.5).** The mechanism is real and this fleet has tripped it — in March and April, on entry scanners, not in June. |
| ~~**9**~~ | ⛔ **ANSWERED 2026-08-04 — NO. Daily and total position limits are pickers capped at `10`.** `posLimitDay` / `posLimit` are hidden inputs behind 1–10 pickers; there is no free-text path. `seed` (Allocation) is `min="250" max="100000"`. | **Kills any daily-limit-20 re-entry spec (R-11).** §3's [PROJECT-RULE] "ten IC re-entries = a daily limit of 20" is correct arithmetic and **unconfigurable** — the real ceiling is **5 ICs/day per bot**. |
| ~~**10**~~ | ✅ **ANSWERED 2026-08-04 — all three EXIST.** `Profit Taking $` (`dprofit`), `Stop Loss $` (`dstop`) and `Avoid Events` are live controls in the Exit Options panel. Full field roster in §6.1a. | **`hedge-research.md` §9's fixed-$ stop rungs are buildable.** Corpus-absence (R-13) was a docs gap, not a product gap. |
| ~~**11**~~ | ⛔ **ANSWERED 2026-08-04 — the account is on the setting that sends NO closing order.** `itmpaper` = `itmlive` = **`auto`** = *"Calculate estimated P/L from underlying close price"*. See §13. | **Confirms the Phase 6 §13 risk class first-hand.** A QQQ position that outlives its exits rides into settlement. **Day-0 must decide this setting before capital is live.** |

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

> ### ⛔ CONTESTED 2026-08-05 — THE PARAGRAPH ABOVE IS FALSE. The toggle IS documented.
> The 2026-07-31 sweep missed `tools/managing-positions/exit-options`. Verbatim:
> > *"Exit Options always run, even if your automations inside a bot are turned off… **unless you
> > turn off Exit Options in your bot**"* — **OA-0871** [DOCUMENTED]
> > *"Additionally, you can enable and disable Exit Options from **the main Bots page, inside of
> > the bot** as shown below, or individually within each position"* — **OA-0896** [DOCUMENTED]
>
> **Existence retags to [DOCUMENTED + FIRST-HAND ×2]** — the strongest tier any claim in this file
> holds. Three documented control surfaces: the main Bots page, inside the bot, per position.
>
> ⚠️ **The section heading still stands, unchanged.** *"MECHANISM still unverified"* is untouched:
> the docs establish the toggle's existence and its surfaces and say **nothing** about subscription
> lapse, deactivation, or what resubscription restores (R-10 — zero corpus facts; the only adjacent
> row, OA-0423, is DOCS-SILENT and about broker authorization). The ⚠️ CAUSAL block below is
> unmodified, and **§8.3's Day-0 Trades-list check remains the only test that settles it.**
> `oa-reconciliation-report.md` R-01 · `data/oa_facts.csv` sha256 `435abe0d…3527b`.

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

## 13. Account-level settings — the surface this file never had [FIRST-HAND 2026-08-04]

*Everything below is an `input.value` read from `app.optionalpha.com/settings` on 2026-08-04,
re-read after a hard reload. Nothing was changed. This page is account-wide: it overrides nothing
per-bot, and no bot setting overrides it.*

### 13.1 ⛔ In-the-money Position Action — the assignment-risk setting

The page's own description:

> *"Positions expiring in-the-money are subject to assignment and/or broker intervention based on
> the contract type and your account balance. Use this setting to auto-close ITM positions 10
> minutes before the close on expiration day OR estimate P/L from the underlying closing price on
> expiration day OR auto-override and manually enter the position results later."*

**Two independent controls, one for paper and one for live**, each with the same three options:

| Internal value | Label | Sends a closing order? |
|---|---|---|
| **`auto`** | Calculate estimated P/L from underlying close price | **NO** |
| `release` | Override position and manually enter results | **NO** |
| `market` | Close position with a market order | **YES** — 10 min before the close on expiration day |

~~**Read 2026-08-04: `itmpaper` = `auto`, `itmlive` = `auto`.**~~

⚠️ **SUPERSEDED THE SAME DAY — corrected 2026-08-05.** **[FIRST-HAND 2026-08-04: `itmpaper` SET
to `market`, verified by hard reload + `input.value` re-read, before/after screenshots on file in
`data/captures/2026-08-03-pilot/06-clone-final/`.]**
**Current: `itmpaper` = `market` · `itmlive` = `auto`.** The struck line was true at the moment of
the first read and false by the end of the same session.

⛔ **`itmlive` remains at `auto` deliberately — it is the hard Day-0 gate, and it is unchanged by
this correction.**
⚠️ **`itmpaper` = `market` is what created the 15:50 race** (this ITM action vs the bot's own
Expiration exit, both Market). That race exists *because* of this correction, not despite it.

⛔ **The account is on the option that sends no closing order.** Only `market` closes an expiring
ITM position. This is the first-hand confirmation of the Phase 6 risk class (OA-0157 / OA-0231,
draft §13): a QQQ iron condor whose exits fail to fire rides into **physical settlement** with the
bot blind to the assignment (OA-0245 / OA-0246). On QQQ — an ETF, physically settled — that is
real stock delivered, not a cash adjustment.

**This is a Day-0 decision, not a preference.** §8.3-class verification must read `itmlive`
before any capital is live, and `build-plan.md`'s exit stack should state which of the three the
program intends. Note also that `market` fires at **10 minutes before the close = 15:50**, which is
the same instant as the clone's existing Expiration exit — the two would race.

### 13.2 Maximum Exit Options Close Attempts — undocumented anywhere in this folder

> *"Limit the number of times a bot will attempt to close a position in a single day. This setting
> can be useful to avoid hitting the 390 rule if you're a very active trader."*

`maxexits` — read **`0`** = `Unlimited`. Picker offers `0` Unlimited · `1`–`10` per day · `15` ·
`20` · `25` per day.

**This is an account-wide throttle on exit attempts and it appears in no other document here.**
At `Unlimited` it is currently inert, but it is a single switch that can silently cap every bot's
ability to close — exactly the failure shape §0.3 and §10 are about. Add it to the capture set.

### 13.3 Bot Schedule

Recorded in full in §4.1's `✅ RESOLVED IN THE PRODUCT 2026-08-04` block — `scanstart` / `scanend`
/ `exitstart` / `exitend`, two independent windows, and the Repeating-trigger carve-out.

### 13.4 Also read, lower stakes

`openclose` (email on position open/close) = **checked** · `botalert` (custom automation
notifications) = unchecked · `paper` (notifications for paper trading) = **unchecked** — note the
fleet is entirely paper right now, so **position-open/close emails are not reaching Andy for the
bots that actually exist.** Membership reads `Pro (Monthly Plan)` · `BOTS 50` · `PER BOT $100k`,
which is where §3's `seed max="100000"` comes from.

---

## 14. 📎 Documented facts this file was missing — PHASE 6 corpus, added 2026-08-05

*Cherry-picked from `oa-platform-reference-v3-DRAFT.md` §13 at Andy's ruling 2026-08-05 (**ALT: NO**
— the draft is a stale branch off base sha `1330dc59…7386` and adopting it wholesale would have
deleted §6.1a, §13 and eleven `ANSWERED 2026-08-04` §9 rows; only its unique content is carried
here). Every claim below is [DOCUMENTED] with a `data/oa_facts.csv` fact ID. Full register:
`docs/oa-reconciliation-report.md` §5. **Nothing here is an inference from absence.***

### 14.1 ⛔ Bots are blind to assignment

Bots *"do not support"* and are *"unaware of"* assignment [**OA-0245**, **OA-0246**]; the broker
API does not report assignment events to OA [**OA-0145**]. Assignment can occur on OTM legs, before
or after the close [**OA-0097**, **OA-0239**]. After an assignment the bot keeps tracking the
pre-assignment position, still attempts exits against it, and errors [**OA-0146**, **OA-0147**,
**OA-0251**]. OA tracks positions independently of the broker [**OA-0247**] — **OA-side position
state can silently diverge from broker truth**, and only a broker-side check detects it. The daily
loop's drift audit reads OA exports; **it cannot see this class.** Recorded as a known blind spot,
not a fixable one.

### 14.2 The expiration protocol — the documented half

§13.1 records this account's setting first-hand (`itmpaper` = `itmlive` = `auto`). The corpus adds
the surrounding facts: three Settings options [**OA-0233**]; the **default sends no closing order**
and reports a synthetic estimated P/L [**OA-0157**, **OA-0230**, **OA-0231**]; OTM positions are
never closed [**OA-0236**]; last moneyness check 10 minutes before the close [**OA-0238**]; which
price decides ITM is DOCS-SILENT [**OA-0252**], as is what happens if the market-order variant
fails to fill [**OA-0161**].

⚠️ **[CONFLICT] worth carrying:** `automation-behavior` says bots *"attempt to close the entire
position"* when a leg is ITM on expiration day [**OA-0097**] — presumably describing the
non-default setting, but as written the two pages disagree [vs **OA-0231**].

### 14.3 The rest, briefly

- **Partial fills.** Opening-order partials reset a 2-minute timeout; at expiry the remainder is
  **canceled** and the position flips to "open" **with the partial quantity** [**OA-0140**–**OA-0142**].
  Closing-order partial behavior is DOCS-SILENT [**OA-0144**]. A half-filled condor leg is a live
  lopsided-risk event **no detector rule currently names**.
- **Quote staleness.** Contract data updates at most every 500ms **unless no new market update
  arrived** — thin, far-OTM contracts (this fleet's short strikes on quiet days) can sit stale
  [**OA-0105**–**OA-0107**]; bot-vs-broker display mismatch is expected by design [**OA-0108**].
  Relevant to every *"the mark was X at the trigger minute"* forensic.
- **Externally-closed positions.** The bot keeps honoring close instructions and ITM handling as if
  the position were open, errors at the broker, and needs a manual override to stop
  [**OA-0131**–**OA-0133**]. Relevant to any manual intervention mid-pilot or during Day-0.
- **In-flight invisibility.** A position released to the broker service is temporarily unknown to
  the bot, and other automations do not see it as Open [**OA-0136**–**OA-0138**] — the documented
  mechanism behind the 7/01 orphan-loop shape, sharper than §4.2's "redundant position check".
- **Manual override frees limits.** An overridden position stops counting against position and
  allocation limits [**OA-0130**, **OA-0759**] — overriding a runaway position *raises* the bot's
  capacity to open more.
- **The 10-symbol daily limit counts everything** — opening, analyzing, monitoring and custom
  inputs alike [**OA-0347**]; at 10 assigned, symbol swaps must wait for after-hours [**OA-0351**].
- **Scheduled events are UTC-anchored.** *"A UTC offset is employed for all Scheduled events"* — a
  next-day automation must exist before UTC 00:00 [**OA-0059**]. This is the closest documented
  evidence bearing on §8.2's DST question and **does not resolve** whether `ntime=1552` tracks
  market time across the boundary. The Day-0 observation stands.
- **SPX pricing granularity.** Legs fill in nickels; the "mid" of an SPX leg with a $0.10–$0.15
  spread is $0.15 buying / $0.10 selling — not the arithmetic mid [**OA-0801**–**OA-0806**].
- **Silent-by-design paths.** The 'Opportunity is available' check fails without alerting
  [**OA-0382**]; the four named Warnings never count toward the failsafe [**OA-0324**].
- **Calendar-day exits.** Before Expiration / Before Earnings compute in **calendar days**
  [**OA-0886**] — matters for any DTE-specified time exit on a Friday-weekend boundary.
- **Empty core pages.** The "Automated Trading" concept page has zero body content [**OA-0632**],
  as do Screener, Trade Grid, Top Strategies and both Guides pages. **No canonical first-party
  definition of a bot exists** — this file is the substitute, which is why it carries fact IDs.

---

*Sources: `docs.optionalpha.com` (swept 2026-07-29, `oa-docs-research-2026-07-29.md`), the
project's own OA capability inventory (`oa-setup-exploration-2026-07-29.md`), first-hand
captures in `data/captures/`, the Fortress and champion execution forensics, and one OA
support conversation of 2026-07-30 (§10). Platform features change and the docs demonstrably
lag the product — re-verify §9 against the running account before relying on any of it.*
