---
name: option-alpha
description: Operating knowledge for the Option Alpha platform — evidence rules, liveness checks, log reading, capture ritual, and the traps that have bitten this fleet. Use whenever a task touches OA bots, automations, exits, positions, captures, or the question "did this bot actually do what we think it did?"
---

# Option Alpha — operator's skill

This is an **index and a set of laws**, not a copy of the research. The canonical documents
live in `docs/` and win over this file in every case of disagreement. Nothing here is
restated for its own sake; each entry exists because getting it wrong has cost this project
money or a wasted session.

## 0. Reading order

Before doing anything that touches OA, in this order:

| # | File | What it is |
|---|---|---|
| 1 | `docs/state.md` | Where the project is right now. `CLAUDE.md` requires this first. |
| 2 | `docs/oa-platform-reference.md` | **The bible.** Platform semantics, limits, evidence tiers. 1,431 lines. |
| 3 | `docs/oa-ops-runbook.md` | How to *operate*: capture ritual, edit verification, the traps. |
| 4 | `data/oa_facts.csv` | 1,770 rows of quotable OA documentation facts, with IDs (`OA-0785` etc.). Grep it before asserting anything about the platform. |
| 5 | `docs/capture-architecture-2026-07-30.md` | Why captures exist and what a capture must contain. |
| 6 | `docs/oa-mirror-reference.md` | The mirrored-strategy pillar and its funding bar. |
| 7 | `docs/oa-export-schema.md` | Column semantics of OA's Export Data — the ledger source. |

Supporting: `docs/oa-reconciliation-report.md` (doc-vs-fact-corpus reconciliation),
`docs/oa-platform-reference-v3-DRAFT.md` (**draft — never cite as authority**).

## 1. The five laws

These are not guidelines. Each was learned from a specific failure.

1. **The Trades list is the only order-level evidence.** Exit Options are *copied onto a
   position at open*; the panel renders the automation's current settings, not what is live on
   any position. They diverge silently. Fortress positions generated **no exit orders at all**
   while the panel displayed `PROFIT % 50%`. When any doc here says "verify", it means the
   position's Trades list. No exceptions. (`oa-platform-reference.md` §0.3, `oa-ops-runbook.md` §4.2)

2. **The platform has no memory.** No counters, no writable variables, no persistence between
   scans except tags and SmartStops' high-water mark. **No condition can reference its own
   past.** Any mechanic described as "sustained", "confirmed", or "after N minutes" is either an
   unbuilt tag ladder or an undocumented substitution. `QQQ-IC-0DTE-HedgeD-Conditional` lost
   **−$15,376** testing an immediate $1-ITM stop while its docs, its config record and its
   automation tree all agreed it was testing a 10-minute sustained breach. Config-vs-reality
   diffing cannot catch that class of failure. (§0.1, §11)

3. **Provenance or it did not happen.** Every claim carries a tier: `[DOCUMENTED]`
   (verbatim quote + docs path), `[FIRST-HAND]` (a value read from the account, dated),
   `[PROJECT-RULE]`, `[SINGLE-SOURCE]`, `[DOCS-SILENT]`, `[CONFLICT]`. **Citing another project
   document is not provenance** — two documents vouching for each other is a citation loop, and
   one survived here for weeks. **Inference from absence is not observation:** "I did not see a
   control" is a screen that was not opened. Screenshot beats stale doc; doc beats memory. (§0.2)

4. **Contested claims are marked in place, dated, never deleted.** Appending a dated banner that
   cites a quotable fact ID or a first-hand value needs no authorization. Replacing or deleting
   the original text does. `§8` of the platform reference is build-plan-adjacent and stays
   gated. (§0.2, `CLAUDE.md` §5)

5. **A tool's success message is not verification.** Re-read the value from OA after the write.
   (`CLAUDE.md` §9.1a)

## 2. Liveness — "should this bot have fired?"

The highest-value routine OA question, and it works at n=1. Position data alone **cannot**
distinguish a correctly-gated bot from a dead one: `DIR-SPX-PutVIX22-SL75` took zero positions
in 22 days because its VIX≥22 gate correctly never fired. `execution_audit.py` therefore raises
`SILENT_BOT` as unverifiable rather than as a failure, and names the log as the resolver.

**The resolution rule** (`oa-platform-reference.md` §4.4, [DOCUMENTED]):

> a **scanner run recorded with no entry = healthy**. **Zero log rows = presumed OFF or
> failsafe-tripped.**

Four inputs, in increasing cost:

| Input | Answers |
|---|---|
| `data/bots_meta.csv` `status` | Is it even supposed to be ON? Must be a first-hand OA read, not memory. |
| OA bot log (`/bots/bot/<id>` → Log tab) | Did the scanner run? Did it error? |
| Tradier intraday option prices (`scripts/tape.py`, `scripts/intraday_read.py`) | Were the entry conditions actually present? |
| The position's Trades list | What was actually sent, at what price. |

### 2.1 Reading the logs without being lied to

- Filterable by **date**, **type** (Scanner / Monitor / Event / Button), and errors/warnings.
- **The date filter reaches 3 weeks of weekdays; the stored data reaches ≥141 days.** Retention
  is not the constraint, the filter is. Beyond 3 weeks you must page `Load more`, which is slow
  and stopped yielding at ~229 rows while still displaying the button. Treat "reachable by
  filter" and "still stored" as two separate budgets. **The immediately preceding weekday may not
  be offered by the filter at all** — grouping starts at "last week".
- **Every log row carries a `title` attribute holding a year-bearing timestamp**
  (`Apr 16, 2026 3:55PM`). Use it. **The visible date group header is unreliable** — on one bot it
  did not render, on another it re-rendered mid-scroll and changed value.
- The `Date`/`Time`/`Type` filter chips render their labels via CSS, so `innerText` on them is
  the **empty string**. They are `div.input-ct.filterbtn-ct` wrappers around hidden inputs named
  `date`, `time`, `autotypes`. A reader trusting `innerText` concludes the filters do not exist.

### 2.2 The failsafe that kills a healthy bot

**10 automation errors in one day disables ALL automations on that bot** [DOCUMENTED,
`troubleshooting/excessive-errors-failsafe.md`]. Re-enabling is manual, and **if another error
occurs the same day it trips again** — a bot switched back on can die a second time silently.
The counter resets the next trading day. Errors surface on the homepage and in the bot
dashboard's activity summary; detail is in the bot log and automation log. Which error types
count toward the threshold is [DOCS-SILENT]. This mechanism was unknown to this project until
2026-07-29, including to the OA support rep consulted about the lapse.

**So: zero positions + zero log rows + `status=ON` is not a quiet day. It is a dead bot until
proven otherwise.**

## 3. Capture — how OA state gets into the repo

`Ctrl+S` does not work; image screenshot tools are banned for config (they cannot be diffed).
The primary instrument is the **bookmarklet** ("OA Grab"), with three fallbacks. Full ritual:
`oa-ops-runbook.md` §1. Non-obvious parts:

- **Expand every caret before grabbing** — collapsed nodes may not be in the DOM, so a missing
  branch looks like a clean capture (§5 trap 3).
- **Select all groups before Export Data** — the export respects the group filter, and a subset
  export rebuilds the ledger and erases history (trap 4).
- **Toggle state is the one place images are mandatory** (§1.6) — toggles are invisible to text
  capture by construction.
- Captures land in `data/captures/<date>-<session>/` and are the *only* legitimate source for
  `data/bots_config_v2.csv`. That file is **built only from capture, never hand-written.**

## 4. Editing OA — the two-layer verification

Never optional. `oa-ops-runbook.md` §4.

- **Layer 1, immediate:** hard reload, re-read the field's `input.value` (not the rendered
  label), confirm the value you intended. Verify **values, not presence** (§4.5).
- ⭐ **A VERSION INCREMENT IS NOT EVIDENCE — ONLY THE HASH IS** (ruling
  `R-2026-08-17-HASH-NOT-VERSION`). Verify an automation edit by
  `sha256(JSON.stringify({name, inputs, root}))` on `a5.bots.acedit.routine` **and** the payload
  byte count, never by the version number or the save confirmation. Observed 2026-08-17:
  `GF-ScannerA-PutSpread` advanced **v10 → v11 with a byte-identical 5478-byte payload and an
  identical hash** — the save "succeeded" and nothing changed.
- **Layer 2, behavioral:** the **next new position's Trades list** shows the expected order.
  Until Layer 2 runs, an edit is *applied*, not *proven*.
- **Two control clones** give inverted verification (§4.3); sibling closes give the timestamp
  gap test (§4.4).

**Standing rules:** refactor behaviour-neutral first, then change values; pilot on a dead bot,
champion last; no changes during streaks; log every inactive-era edit (edits made while the
account is inactive **do persist**); never clone to escape a bad record — cloning to a written
spec with the original renamed `-ARCHIVED-<date>` is the sanctioned path; append to
`data/archive/rename_map.csv` **as the sweep runs**, not from memory afterwards.

## 5. Traps — the short list

Full table with evidence: `oa-ops-runbook.md` §5. The ones that cost the most:

| Trap | Counter |
|---|---|
| **Symbols drop silently on clone** — the bot looks configured and simply never scans | Re-add Symbols; verify |
| **`disableExits` resets 1→0 on clone** — a config-present/toggle-off exit re-arms itself with no field edited | Check the toggle immediately after cloning, before any other edit. Invisible to text capture |
| **Cloning COPIES, it does not share** (the opposite was believed for weeks) | Sharing is opt-in via the Automation Library at `/bots/automations` (`/automations` 404s). In-Library → Copy to fork. Not in Library → edit directly |
| **Market orders fill outside the spread** — one fill came in $5.05/contract beyond the worst mark the position ever traded | Market pricing is **banned on every entry and every exit** except a hard end-of-day flat close |
| **IC = 2 positions** | Position limits × 2 per iron condor |
| **A time gate that was never implemented** | Confirm the gate is a real decision node, then check the first five entry timestamps |
| **Name collision on archive** | Read the *full* name. `Opening Range Breakout 60m` is archived; `60min-ORB-10W-Paper-v1` is live |
| **Zero-trade ≠ worthless** | See §2. Delete only if zero-trade **and** absent from the disposition table |
| **THREE save layers, not two** — recipe `a.btn.green.save` → the action drawer's OWN Save (a `button.btn.green` at the BOTTOM of the drawer's scroll region, OFF-SCREEN) → `a.saveclose`. Only the drawer Save writes into `a5.bots.acedit.routine` | `scrollIntoView({block:'center'})` the drawer Save before clicking. Enumerate every `Save` candidate's `{tag,class,x,y,w}` first — a naive text match hits an off-screen button |
| **Closing the action drawer with its ✕ DISCARDS staged edits** — and the following `a.saveclose` then commits an UNCHANGED routine with a BUMPED VERSION | Never close the drawer to "apply". Compare the config hash before and after; equal hash = nothing changed, whatever the version says |
| **`a.saveclose` sits UNDER the drawer overlay** — `elementFromPoint` at its centre returns the drawer, so the dispatch silently goes nowhere | Close the drawer first (`i.fa-times`, drawer top-right), then re-check what occupies the point before clicking |
| **A 45s `Runtime.evaluate` timeout may be a LOGOUT, not a freeze** | Check for `/login` in the URL before re-trying anything. Never re-fire a save on a timeout |
| **Flipping the AUTOMATIONS / EXIT OPTIONS master toggle NAVIGATES the page** — the call returns `Inspected target navigated or closed` mid-evaluation and looks like a failure | Same class as the 45s timeout: **the work has usually COMMITTED. Re-read state, never re-fire.** Re-firing a toggle silently flips it back. Verify from `a5.bots.bot.status` + the switch's `input-ct onoff on\|off` class after the reload |
| **The two master switches sit side by side** — a coordinate-based click can hit EXIT OPTIONS instead of AUTOMATIONS | Scope by DOM container (`div.autoswitch.hdbox` whose `innerText` matches `AUTOMATIONS`), then guard on the target's x against the other box's left edge before dispatching |

## 6. Numbers that get quoted wrong

- **SmartPricing:** Fast (internal value **`speedy`**, not `"fast"` — any parser keying on
  "fast" silently misses it) 3 prices × 5s · Normal `normal` 4 × 10s · Patient `patient` 5 × 20s ·
  `off` single limit · `market` immediate. Selecting Market collapses the Final Price ladder.
- **Final Price range is 50–150**, floor 50, not 0. A final price better than the mid is **not
  settable**. The docs' "0% (bid) through 100% (ask)" is wrong for this control.
- **Exit Options evaluate every 1 market minute.** There is no sub-second anything; Touch `$0`
  exits on the first 1-minute evaluation at which the position is ITM.
- **Account-level, overrides nothing and is overridden by nothing** (`/settings`): `itmpaper` =
  `market`, `itmlive` = `auto`. Only `market` sends a closing order (10 min before the close on
  expiration day = 15:50). **`itmlive` = `auto` sends no closing order** and is the hard Day-0
  gate. `maxexits` = `0` (unlimited) throttles exit attempts account-wide.

## 7. Not expressible — do not spend a day rediscovering

Time persistence · intraday indicators (pivots, VWAP — daily bars are cached pre-market) ·
sub-second strike touch with a latch · mid-trade branching on a breach · single-action "defang" ·
any condition referencing its own past. Webhooks are the **only** route for an externally
computed signal — and a webhook **persists across bot clones**. (`oa-platform-reference.md` §11, §12)

## 8. Rules of engagement for an agent

- **Never change anything in OA without explicit authorization for that change.** Reads are free;
  writes are not. `CLAUDE.md` governs.
- **Never put credentials in this repo, in a capture, or in a message.** OA and Tradier
  credentials come from the environment.
- **Never use v1 archive data as a reporting input.** `LEDGER_START = 2026-08-10`.
- **Never use a narrative doc to override a CSV.** Numbers come from the post-cutover ledger and
  generated `STATUS.md`; config facts come from capture files.
- When this file and a `docs/` file disagree, **the `docs/` file wins** — and fix this file.
