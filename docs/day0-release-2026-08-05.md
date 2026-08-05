# Day-0 release sheet — 2026-08-05

*Every gated finding from `docs/day0-audit-2026-08-05.md`, as a tick-box. **28 items, 6 decisions.***
*Full evidence and rationale live in the audit; this sheet is for deciding, not for re-reading.*

**How to use:** tick `[x] RELEASE` or write `NO —` + one line. A `NO` is a real answer and I will
record it as a ruling, not as an omission. Anything left blank stays gated and Day-0 executes
without it.

**Nothing on this sheet touches `docs/build-plan.md`.** Where an item would, it is marked
⛔ **PLAN AMENDMENT** and needs your explicit *"amend the plan"*, not a tick.

---

## DECISION 0 — decide this one first. It is the only one where waiting destroys information.

### ⏳ F-36 · The no-touch observation before the re-arm sweep

**Status:** `NOT RULED as of 2026-08-04` (`decision-memo-2026-08-04.md:393`). Not a release — an
open slot. **Step 3 as written resolves it by acting.**

**The question.** Day-0 is itself an inactive→active transition. If exits resume at reactivation
**with no toggle intervention**, billing state is implicated as the June cause. Flip a toggle first
and re-arm is confounded with reactivation — candidate 1 (the `EXIT OPTIONS` toggle) and candidate 6
(billing) become **permanently indistinguishable.** The memo calls the fix *"free"*: it is one
screenshot, before Step 3.

**Cost of YES:** ~2 minutes on Day-0. **Cost of NO:** the §1 causal story stays unfalsifiable
forever, and D-4 ("the June cause is UNKNOWN") can never be closed.

- [ ] **RELEASE — observe first.** Before any toggle: read both dashboard toggles on one mirror and
      one directional bot, screenshot, log. If either reads ON without intervention, report before
      proceeding.
- [ ] **NO — flip straight through.** I record the slot as ruled-against and strike the
      discriminator from the memo so nobody re-raises it.

---

## DECISION 1 — pure propagation. Not new decisions; you already ruled all three.

*These are gated only because `CLAUDE.md` §5 condition 3 forbids me citing another project document
as the falsifying evidence. **One tick releases all three.***

- [ ] **RELEASE ALL THREE** ⟶ F-1, F-12, F-32

### F-1 · `itmlive` = `market` — inserted as §4 Step 0a
*Your ruling: `decision-memo-2026-08-04.md:278` — ✅ RULED, hard Day-0 gate.*
**The single most dangerous omission in the runbook.** Zero matches for `itmlive` in 223 lines.

> ### Step 0a — ⛔ Set `itmlive` = `market`. HARD GATE, before any capital is live.
>
> `itmlive` is deliberately still `auto` — *"Calculate estimated P/L from underlying close price"* —
> which **sends no closing order at all.** `market` is the only option that closes. A QQQ condor
> outliving its exits under `auto` rides into **physical settlement**: real stock delivered, with
> the bot blind to the assignment.
>
> **DO:** `/settings` → set `itmlive` = `market` → hard reload → re-read `input.value` → screenshot
> before and after. **A save banner is not verification** (`CLAUDE.md` §9.1a).
>
> ⚠️ **`itmpaper` is ALREADY `market`** — set and verified 2026-08-04. **Do not re-set it.** Read it
> back as part of the same self-check. `itmlive` is the only half still outstanding.
>
> ⛔ **IF the value will not persist through a hard reload → NO capital goes live. Fleet stays OFF.
> Escalate to Andy: YES.**
>
> ⚠️ **`market` is not a substitute for the 15:52 flat-close backstop.** It reaches only *expiring
> ITM* positions on expiration day.

### F-12 · Template V2 lands before Day-0 — new §2 step 6a
*Your ruling: `decision-memo-2026-08-04.md:728-732` — ✅ RULED, execution deferred as part of the
ruling, lands as V2 with an amended pre-registration.* The runbook currently sequences only V1, and
its Day-0 completeness gate **accepts V1** — so the pilot passes Step 4 with the attribution guard
unsatisfied.

> 6a. **⏸ Template V2 — the pilot only, and it lands BEFORE Day-0.** Decision 6 ruled 2026-08-04:
>     re-price the 15:50 Expiration exit **OFF Market** (SmartPricing — internal value `speedy`,
>     **NOT** `fast`; a capture parser keying on "fast" silently misses it). **The 15:52 backstop
>     KEEPS Market.** ⛔ Execution was deferred as part of the ruling: PR-03's config hash is frozen,
>     so this is a **spec change.** It lands as **Template V2 with an AMENDED pre-registration**,
>     before Day-0 — never as a quiet edit. PR-03 is still unsigned; the amendment and the signature
>     happen together.

*Plus one line in §4 Step 4: the completeness gate reads "a saved template at its **current ruled
version** (the pilot requires **V2**)".*

### F-32 · The fleet count — `≈18` → ≈18–20 plan bots plus ≤8 Track B arms, ceiling 28
*Your amendment: `build-plan.md:128` — 🔓 SCOPING AMENDMENT 2026-08-05.* Two spots (§3 Step D, the
Pre-Day-0 checklist) still say `≈18`. ⚠️ The amendment scopes a **count**; it authorizes no build,
and every Track B arm still needs its own signed entry.

---

## DECISION 2 — failure branches. One decision about shape, not ten.

**The problem in one number: 41 of 44 checks (93%) have no usable branch, and `STOP` appears zero
times in 223 lines.** Day-0 runs on a weaker model with no judgment budget.

**Every branch is drafted in one of two shapes — read three of them and you have read all ten:**
> **IF** ‹fail condition› **→** ‹action› **·** bot stays OFF / fleet stays OFF **·** escalate to
> Andy: yes/no

- [ ] **RELEASE THE SET** ⟶ F-3, F-4, F-5, F-6, F-8, F-9, F-10, F-23, F-29
- [ ] **RELEASE, but per-bot only** — no branch may halt the whole fleet; I downgrade every
      *fleet stays OFF* to *bot stays OFF* and flag the three where I think that is wrong.

| # | Check | Branch, in one line |
|---|---|---|
| **F-4** | Inverted control-clone check | PT row present ⟶ control **contaminated**, comparison void. **Do NOT remove it** (`CLAUDE.md` §5 standing exception). Bot OFF · fleet proceeds · escalate YES |
| **F-5** | Step 6 order-level verification | No PT row ⟶ MECHANICS 🔴 RED, re-observe toggles, re-read values, re-drive once. Bot OFF · fleet proceeds · escalate on 2nd failure. **No position opened = NOT EVALUABLE, never a pass** |
| **F-6** | Re-arm sweep toggles | Toggle absent ⟶ try all 3 documented surfaces first. Won't hold ON after 2 tries ⟶ bot OFF. **3+ of 9 won't hold ⟶ fleet stays OFF** ⚠️ *the revert half is invented, not corpus-cited — audit §C-3* |
| **F-8** | Mechanism verdict (new Step 6a) | Toggles ON + no PT rows ⟶ **§1 REFUTED, full stop.** All nine `AUTOMATIONS` OFF, clones blocked too, check the 4 competing mechanisms in order, card `LAPSE-MECHANISM-REFUTED`. **Do not diagnose past that point** |
| **F-9** | Step 6/7 circularity | Test-fire unavailable ⟶ **first-position exception:** exactly one position, 1 lot, read on open. Matches greenfield D6 (*"Signed ≠ verified"*) |
| **F-10** | Signing (new Step 2b) | No signed entry ⟶ **bot stays OFF for all of Day-0**, including the nine untouched. §4 currently has **no signing step at all** |
| **F-23** | Day-1 RED | A card is a notification, not a disposition. Zero log entries ⟶ **bot switched off pending investigation**. `mfe_pct` ≥ PT with no PT order ⟶ bot OFF next session, escalate YES |
| **F-29** | Six more (D7–D13) | Symbols still empty · script crash at n=0 (**fix the script, never seed a row**) · short capture · what "clean" means (**Andy declares it**) · ORIGINAL's list changed · toggle reads OFF |
| **F-3** | Structural | One header at the top of §4 defining *bot stays OFF* vs *fleet stays OFF*, and **"a check you could not run is not a pass"** |

---

## DECISION 3 — the one real disposition change.

### F-2 · Step 3 arms nine bots 24 lines before the gate that authorizes them

**`AUTOMATIONS` ON *is* the entry authorization.** By the time the executor reaches Step 6, "the
first new position" already exists and was taken unproven — the v1 failure (−$9,618 over six June
days) reproduced on Day-0, with Step 7 gating nothing.

**The fix is one swap:**

> **Step 3** arms **`EXIT OPTIONS` only**; `AUTOMATIONS` stays **OFF** on all nine.
> **Step 7** turns `AUTOMATIONS` ON, per bot, only for bots that passed Step 6.

Plus one clarifying line, because the runbook is currently ambiguous about it: *"These nine are NOT
exempt from Step 6. Line 173's 'nothing else needs re-arming' scopes re-arming, not verification."*

- [ ] **RELEASE — swap them.**
- [ ] **RELEASE the swap, but the nine ARE exempt from Step 6** — they are pre-existing bots, not
      new builds, and you want them trading Day-0 without waiting on a Trades list.
- [ ] **NO — leave Step 3 as written**, and I add a note saying the ordering is deliberate so nobody
      re-raises it.

*(Roster verified correct either way: **n=9 named, n=9 expected**, name-for-name against
`build-plan.md:109` / `:112–113`, set difference empty both directions.)*

---

## DECISION 4 — new Day-0 observations. Decide as a set: how long may Day-0 be?

*Each adds a step. Individually cheap; together they lengthen Day-0 materially. F-7 is the one I
would not drop.*

- [ ] **RELEASE ALL FOUR** ⟶ F-7, F-13, F-16, F-18
- [ ] **RELEASE F-7 and F-18 only** — the two that can invalidate the whole sample
- [ ] **NO** — Day-0 stays short; these become Day-1/Day-2 items and I say so explicitly in the
      runbook rather than leaving them unscheduled

| # | Observation | Why it is on Day-0 | Cost if skipped |
|---|---|---|---|
| **F-7** | **DST** — does `ntime=1552` fire at 15:52 ET in August? | Day-0 is EDT; the trigger serialised as `20:52Z` = **16:52 ET** under a literal-EST reading | **The backstop never fires, on every bot at once — and the absence looks exactly like "nothing needed closing."** Needs a decision tree for fires-late / no-row / unreadable |
| **F-13** | `/settings` capture set: `itmlive` `itmpaper` **`maxexits`** `scanstart` `scanend` `exitstart` `exitend` | Account-wide, override every bot, in **no** capture today | `maxexits` is a single switch that caps **every bot's** ability to close. Read `0`/Unlimited 2026-08-04, so inert — and invisible to the drift detector if it ever changes |
| **F-16** | **C10** — is `dstop` per-contract or per-position? | Needs a live position with a **known contract count.** That moment exists once. The 1-lot canary is the instrument — currently marked *"Optional"* | ARM-B1 stays blocked, `<D100>` underived, PR-21 unstampable. **Do not infer it from the negative sign** |
| **F-18** | Phase 0 (`C0c · C2 · C7 · C8 · C9` untouched, C10 open) + **A7 payload-hash baselines** in the Step 4 gate | Shared automations across 7 bots: a mis-built gate fails identically on all seven, which the arms cannot detect by diffing each other | **A7 is the only detector.** No baseline before Day-0 = no detector for the whole sample |

---

## DECISION 5 — one irreversible action.

### F-15 · Does the Phase 4 sweep delete `CLAUDE-C5-SHARED-SCRATCH`?

`rid RTfw5TkkCRF178589028977611`, carrying automation input `C5_EXITS` (`IN178589048006251`).
**Account-level. Does not die with the two scratch bots.** Left in place it orphans in
`My Automations`, where the account previously held exactly **one** shared automation — so an
orphan is conspicuous and will be mistaken for a real object, and a Library edit propagates to every
bot using it.

*The **fact** is already applied to the runbook (audit F-22). Only the delete instruction is gated.*

- [ ] **RELEASE — sweep deletes it**, after both scratch bots are deleted.
- [ ] **NO — leave it**, and I add a line naming it as known, deliberate residue so a future session
      doesn't "discover" it.

---

## DECISION 6 — the remainder. Low individual value; one tick clears them.

- [ ] **RELEASE ALL** ⟶ F-17, F-24, F-25, F-26, F-27, F-28, F-33, F-34, F-35

| # | One line |
|---|---|
| **F-17** | The 15:50 race: `itmpaper=market` fires at the same instant as the Expiration exit. Record **both** rows, attribute by the **gap**, not the absolute minute. Pricing only discriminates **after** Template V2 |
| **F-24** | Classify all 12 Pre-Day-0 boxes ⛔ HARD BLOCKER / ⚠️ PER-BOT / 📝 ADVISORY. Today none is marked, so all twelve can be unticked on the day |
| **F-25** | §4 never re-asserts five checklist preconditions it depends on. **Sizing** in particular — *"set once at restart, never ad hoc"* — will otherwise be set mid-sample |
| **F-26** | Step 5 claims a `/bots` sweep **is** `bots_config_v2.csv`. It cannot be: no Exit Options values, and the file is written **per-bot as each bot is built** |
| **F-27** | The G2 rider is stated in §3 and never re-asserted in §4. If the input value can't be read, the capture is **not a baseline** — hash `NOT ESTABLISHED`, entry unsignable, bot OFF. **Never fall back to `oldValue`** |
| **F-28** | **D4** — whether the ITM action appears in a Trades list and under what label is **unobserved**, which makes every inverted check **advisory, not fireable**. Compounds F-4: a mislabelled ITM close reads as a PT row and kills a control on day one |
| **F-33** | After setting `LEDGER_START`, run `build_ledger.py` once and confirm row count **0**. Any row ⟶ a pre-cutover row has entered ⟶ STOP |
| **F-34** | The ride-or-close decision has **nowhere to be written** — its ledger entry is not drafted. And Step 2 requires it *logged*, never *executed*, while Step 3 then arms the two bots holding those five positions |
| **F-35** | The Exit Options toggle has **three** documented surfaces; Step 3 touches one. On positions open **through** the lapse, read the position's own state. ⚠️ Never observed on those five — an unopened screen, not a known-good one |

---

## Tally

| | Items | Ticks needed |
|---|---|---|
| Decision 0 — F-36 | 1 | 1 |
| Decision 1 — propagation | 3 | 1 |
| Decision 2 — failure branches | 9 | 1 |
| Decision 3 — the swap | 1 | 1 |
| Decision 4 — observations | 4 | 1 |
| Decision 5 — the delete | 1 | 1 |
| Decision 6 — remainder | 9 | 1 |
| **Total** | **28** | **7** |

**Already applied and awaiting only your commit review** (audit §D): F-11 · F-14 · F-19 · F-20 ·
F-21 · F-22 · F-30 · F-31.

**Files to commit:** `docs/day0-audit-2026-08-05.md` (new) · `docs/day0-release-2026-08-05.md`
(new) · `docs/reactivation-runbook.md` · `docs/oa-platform-reference.md` · `docs/state.md` ·
`docs/session-log.md`.
