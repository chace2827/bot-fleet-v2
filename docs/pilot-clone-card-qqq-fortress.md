# PILOT CLONE — `QQQ-IC-0DTE-Fortress`

**Instruction card. Follow live, top to bottom, with Claude open beside you.**

*Written 2026-07-31. This is the first clone of the v2 rebuild and the pilot for the 9-step
ritual (`reactivation-runbook.md` §3 Step A). **Nothing else in Phase 4 starts until this one is
clean.***

---

## READ THIS FIRST — three things that shape the whole session

> ### ✍️ BEFORE STARTING — fill the date placeholders
> This card is written with `<session-date>` placeholders. **Replace every one with today's
> date (`YYYY-MM-DD`) before Step 0** — including the name of the capture folder on disk,
> which ships as a literal `<session-date>-pilot` directory.
>
> **11 occurrences, three kinds:** the capture path (6), the archive suffix
> (4), and the `rename_map.csv` row's `date` field (1).
>
> A stale literal date on an `-ARCHIVED-` suffix or a `rename_map` row is a lineage record
> that lies — which is the one thing that file exists to prevent.

**1. The account is INACTIVE. That is fine and it is deliberate.**
Edits made while inactive **do persist** (verified 7/29→7/30). Nothing will trade today. This
means **order-level verification is impossible today** and is deferred to Day-0 — see §FINISH.
Today's finish line is a structural one, not a behavioural one. Do not try to test-fire.

**2. Why this bot was chosen as the pilot.** Simple spec, and its original is already superseded
— so if the ritual goes wrong, the blast radius is a bot that was being archived anyway.
**A mistake made once is a lesson; the same mistake made across nine bots is a rebuild.**

**3. You will hit at least one unknown.** Two specification questions are genuinely unresolved
and one of them lands mid-ritual at Step 5. They are flagged inline with a **⚠️ DECISION POINT**
box. **When you hit one, stop and tell me what you see** — do not improvise a spec on the fly.
That is exactly how the v1 `Conditional` bot ended up testing something nobody chose.

### The target spec (from `build-plan.md` §2B — frozen, do not improvise)

```
CLONE NAME       QQQ-IC-0DTE-Fortress          (takes the production name at Step 8)
ORIGINAL         QQQ-IC-0DTE-Fortress-ARCHIVED-<session-date>   → then archived
EXITS            PT50  +  15:50 time exit  +  15:52 flat-close Scheduled Event backstop
NOT IN SCOPE     any new exit architecture, any filter change, any sizing change
```

### Have these open before you start

- OA `/bots`
- The `OA Grab` bookmarklet installed (`oa-ops-runbook.md` §1.2)
- A folder ready: `data/captures/<session-date>-pilot/`
- This card
- Me

---

## STEP 0 — Baseline capture of the ORIGINAL

**You cannot verify a clone against an original you did not record.** This step is not optional
and it is the one people skip.

**DO**
1. Open `QQQ-IC-0DTE-Fortress` (the original).
2. Settings → Automations. For **each** automation: open it → **expand every `^` caret** →
   click **OA Grab**.
3. Open Position action → Exit Options → `⌘P` → Save as PDF.
4. Screenshot **both** dashboard toggles (`AUTOMATIONS`, `EXIT OPTIONS`) top-right.
5. Note the **Symbols** panel contents and the **Daily / Total position limits**. Write them
   here before you touch anything:

```
SYMBOLS      ______________________
DAILY LIMIT  ______   TOTAL LIMIT  ______
AUTOMATIONS  ON / OFF        EXIT OPTIONS  ON / OFF
AUTOMATION LIST (names, in order):
  1. ______________________
  2. ______________________
  3. ______________________
  4. ______________________
```

**CAPTURE →** `data/captures/<session-date>-pilot/00-original/`

> ### ✅ CONFIRM BEFORE PROCEEDING
> - [ ] One `.txt` file exists **per automation** — count them against the list above.
> - [ ] Open one `.txt` and confirm you can see **actual decision text**, not just names.
>       You should see things like `Profit Taking % 50% of credit`. **If you only see
>       automation names, the tree was not expanded — redo it.**
> - [ ] The Exit Options PDF shows the panel contents.
> - [ ] Both toggle screenshots exist.
> - [ ] Symbols and limits written down above.
>
> **If any box is unticked, do not clone yet.** Tell me what is missing.

---

## STEP 1 — Clone the bot

**DO** — On `/bots`, find `QQQ-IC-0DTE-Fortress` → clone it.

OA will give the clone an automatic name (something like `QQQ-IC-0DTE-Fortress Copy` or
`... (1)`). **Leave that name alone for now.** It gets the production name at Step 8, after the
original has been renamed out of the way. Write down exactly what OA called it:

```
CLONE'S TEMPORARY NAME: ______________________________
```

> ### ✅ CONFIRM BEFORE PROCEEDING
> - [ ] Two bots now exist with similar names.
> - [ ] You can tell which is which. **Say the clone's temporary name out loud once.**
>       Every remaining step happens on the CLONE. If you edit the original by mistake, you
>       have edited the bot you were about to archive — recoverable, but tell me.

---

## STEP 2 — ⚠️ TRAP 1: fork EVERY automation via Copy

> ### ⛔ THE TRAP
> **Clones share automations BY REFERENCE.** Right now, the clone and the original point at the
> *same* automation objects. Edit the clone's automation and **you have edited the original
> too** — and worse, any later edit to the original silently changes your clone.
>
> **This is the trap most likely to produce a bot that looks right and is not.** It leaves no
> error and no visible sign.

**DO** — On the **CLONE**, for **every automation in the list from Step 0**:
1. Open the automation.
2. Use **Copy** to fork it into a new, clone-owned automation.
3. Attach the **copy** to the clone; detach the shared original.
4. Repeat until every automation in the clone's list is a copy.

**CAPTURE →** clone's automation list (bookmarklet on the Automations page)
→ `data/captures/<session-date>-pilot/02-clone-automations-forked.txt`

> ### ✅ CONFIRM BEFORE PROCEEDING — do this test, do not skip it
> - [ ] The clone's automation list has the **same number** of automations as Step 0.
> - [ ] **Each name is visibly distinct from the original's** (a copy suffix, or you renamed it).
>       **If any name is identical to the original's, it is probably still shared.**
> - [ ] **THE REAL TEST:** open the **ORIGINAL** bot's automation list. It must be **unchanged**
>       from Step 0 — same names, same count.
>
> **If the original's list changed, the fork did not take.** Stop and tell me. Do not continue —
> everything after this point would be built on a shared object.

---

## STEP 3 — ⚠️ TRAP 2: re-add Symbols

> ### ⛔ THE TRAP
> **The Symbols panel is not carried on clone.** A bot with no Symbols **looks completely
> configured and simply never scans.** No error, no warning, no positions — indistinguishable at
> a glance from a bot whose filter never passed.

**DO** — Clone → Settings → **Symbols** → add the exact tickers from Step 0.

**CAPTURE →** Settings page → `03-clone-symbols.txt`

> ### ✅ CONFIRM BEFORE PROCEEDING
> - [ ] The Symbols panel lists **exactly** what you wrote in Step 0. Read them character by
>       character against your note.
> - [ ] It is **not empty**. Look at it again. This is the single most common silent clone
>       failure in this fleet.

---

## STEP 4 — Position limits: **IC = 2 POSITIONS**

> ### ⛔ OA models each spread as a SEPARATE POSITION.
> A full iron condor is **two** positions — the call spread and the put spread. A limit of 1
> means **one side never opens**, and you get a half-condor that looks like a strategy.

**DO** — Clone → Settings → confirm **Daily** and **Total** position limits match Step 0's
values, and that they are sized in multiples of **2 per IC**.

> ### ✅ CONFIRM BEFORE PROCEEDING
> - [ ] Daily limit is an **even number** and matches the original's intent.
> - [ ] Total limit likewise.
> - [ ] If either is odd, stop — tell me the number and what the original had.

---

## STEP 5 — Apply the spec. **Nothing beyond the spec.**

The spec is **PT50 + 15:50 time exit + 15:52 flat-close Scheduled Event backstop.** No new exit
architecture, no filter changes, no sizing changes.

**DO — 5a: the Exit Options (PT50 + 15:50 time exit)**
Clone → the **Open Position action** → Exit Options → set **Profit Target 50%** and a
**time exit at 15:50**.

> ### ⚠️ DECISION POINT A — save this as a named Preset, or set values by hand?
> `build-plan.md` specifies a **named Exit Option Preset** for the greenfield family. For this
> pilot, either is acceptable — **but if a "save as Preset" control exists, use it and tell me
> the name you gave it.** Whether one Preset can be referenced from two different Open Position
> actions is undocumented, and this pilot is the cheapest place to find out.
>
> **Report to me: does a Preset save/dropdown control exist in this panel? Yes / No.**

**DO — 5b: the 15:52 Scheduled Event backstop**
Clone → Automations → create a **Scheduled Event** that closes all open positions at **15:52**.

> ### ⚠️ DECISION POINT B — THIS ONE MAY NOT BE BUILDABLE. STOP HERE IF SO.
> Two documented facts sit against a 15:52 Event (`oa-platform-reference.md` §8.2):
> - The **Market close** trigger is **hard-coded to 3:50 pm**. There is no 15:52 variant.
> - Exit Options run only *"until 1 minute before the market close"*, so a 15:52 **Exit Option**
>   does not exist either.
>
> A **Repeating** trigger *may* reach a custom time like 15:52. **Nobody has checked.**
>
> **What to do:** open the Scheduled Event trigger dropdown and tell me **exactly what options
> you see**, and whether a Repeating trigger lets you type an arbitrary time.
>
> - **If 15:52 is reachable** → build it, and we have resolved a blocker that gates two clone
>   specs.
> - **If it is NOT reachable** → **STOP. Do not substitute a different time.** The spec is under
>   decision freeze and changing it needs an explicit "amend the plan" from you. Leave the
>   backstop unbuilt, finish the rest of the card, and flag it. **A substitution made silently
>   at a platform limit is exactly what produced the −$15,376 HedgeD bot.**

**DO — 5c: pricing**
Confirm no exit on this bot uses **Market** pricing, with one permitted exception — the
end-of-day flat close, where fill certainty beats fill quality.

> ### ✅ CONFIRM BEFORE PROCEEDING
> - [ ] PT50 is set on the Open Position action.
> - [ ] 15:50 time exit is set.
> - [ ] Backstop: **built at 15:52** ☐ / **NOT buildable — flagged, left unbuilt** ☐
> - [ ] No Market pricing on any exit except the flat close.
> - [ ] **Nothing else was changed.** No filter edits, no sizing edits, no "while I'm in here"
>       improvements. If you changed anything else, say so now.

---

## STEP 6 — Capture the finished automation tree

**DO** — For every automation on the clone: open → **expand every caret** → **OA Grab**.
Plus Open Position action → Exit Options → `⌘P` → PDF.

**CAPTURE →** `data/captures/<session-date>-pilot/06-clone-final/`

> ### ✅ CONFIRM BEFORE PROCEEDING
> - [ ] One `.txt` per automation, same count as Step 2.
> - [ ] Open one and confirm **decision text is present, not just names.**
> - [ ] Grep the capture set for `50` and confirm the PT50 setting appears in text.
>
> **This capture is what `bots_config_v2.csv` will cite for this bot.** If it is thin, the
> config row is unfounded.

---

## STEP 7 — Save as Template V1, with the pre-registration in Notes

**DO**
1. Clone → save as **Template**, version **V1**.
2. In the template **Notes**, paste the bot's pre-registration entry from
   `docs/pre-registration-ledger.md` §4 (`QQQ-IC-0DTE-Fortress`).
3. Add a **Tag** carrying the pre-registration ID: **`PR-03`**
   (`pre-registration-ledger.md` §4 — scheme is `PR-NN`, ledger entry order).

> ### ⚠️ PASTE THE MECHANISM VERBATIM — even if Decision Point A came back "no Preset"
> The entry's MECHANISM line names **"PT50 + 15:50 time exit as a NAMED EXIT OPTION PRESET"**.
> If Step 5a found no Preset control and you set the values by hand, that line now describes a
> build this bot does not have. **Paste it anyway, unedited.**
>
> The entry is `STATUS DRAFT — unsigned`; signing is a **Day-0** act, and the ledger is
> corrected from the pilot's findings *before* it is signed. Editing pre-registration text live,
> mid-ritual, to match what you just built is how a pre-registration stops being one.
> Report what you found; I amend the ledger with the reason recorded.

> ⚠️ Whether saving a template from a live bot disturbs the bot (position count, automation
> states) is **expected but unverified**. The account is inactive and this bot has no open
> positions, so this is the safest possible moment to find out.

> ### ✅ CONFIRM BEFORE PROCEEDING
> - [ ] Template shows **VERSION 1**.
> - [ ] Notes contain the pre-registration text.
> - [ ] **Re-open the clone**: automation count and Symbols are **unchanged** from Steps 2–3.
> - [ ] Tell me whether saving the template changed anything on the bot. **Either answer is a
>       useful finding** — it closes an open UI check.

---

## STEP 8 — Rename the original, THEN rename the clone. Order matters.

> The production name is currently **occupied by the original**. It has to be freed first.

**DO — in this exact order**
1. **Original** → rename to `QQQ-IC-0DTE-Fortress-ARCHIVED-<session-date>`.
2. **Confirm the rename took** (refresh `/bots`).
3. **Clone** → rename from its temporary name to **`QQQ-IC-0DTE-Fortress`**.
4. **Now archive the original.**

> ### ✅ CONFIRM BEFORE PROCEEDING
> - [ ] `/bots` shows **exactly one** bot named `QQQ-IC-0DTE-Fortress` — the clone.
> - [ ] The archived one reads `QQQ-IC-0DTE-Fortress-ARCHIVED-<session-date>`.
> - [ ] **You archived the ARCHIVED-suffixed one, not the clone.** Read the full name before
>       clicking. Check again.
> - [ ] ⚠️ **Name-collision guard:** you did not touch `60min-ORB-10W-Paper-v1`. (Different bot,
>       stays live. `Opening Range Breakout 60m` is the one that gets archived — later, not now.)

**DO — append the `rename_map.csv` row now, not later from memory:**

`data/archive/rename_map.csv`
```
original_name,archived_as,clone_name,date,disposition
QQQ-IC-0DTE-Fortress,QQQ-IC-0DTE-Fortress-ARCHIVED-<session-date>,QQQ-IC-0DTE-Fortress,<session-date>,clone-to-spec
```

> ### ✅ CONFIRM
> - [ ] The row is written. **This is the only thing that will later connect a name in the
>       frozen ledger to a bot running today.** Without it, every lineage question becomes
>       archaeology.

---

## STEP 9 — Both toggles, screenshotted

**DO** — Clone dashboard, top right: check **`AUTOMATIONS`** and **`EXIT OPTIONS`**. Screenshot
both.

**CAPTURE →** `09-clone-toggles.png`

> ### ✅ CONFIRM BEFORE PROCEEDING
> - [ ] Both toggle states are visible in the screenshot and you can read them.
> - [ ] Record them here: `AUTOMATIONS ___ / EXIT OPTIONS ___`
>
> **Leave them as they are.** Turning this bot ON is a **Day-0** action, not a today action.
>
> The `EXIT OPTIONS` toggle's **existence is established** — the support rep's screenshot of both
> toggles on a bot dashboard, plus your own fleet-wide observation of both toggles OFF on all 35
> bots. Two independent observations. Nothing to report here.
>
> ⚠️ **What is still unverified is the CAUSAL claim** — that flipping `EXIT OPTIONS` back ON
> actually re-arms exit-order generation. A toggle can exist, read ON, and still not produce
> orders; that is the exact shape of the v1 failure. **Only the Day-0 Trades-list check settles
> it**, which is why §FINISH keeps that check rather than treating a toggle screenshot as proof.

---

## FINISH — what "clean" means today, and what waits for Day-0

### ✅ TODAY'S FINISH LINE — structural verification

- [ ] **Capture-diff:** the Step 6 clone capture vs the Step 0 original capture differs **only**
      in the exit block (PT50 / 15:50 / backstop). Send me both and I will diff them. **Any
      other difference is an unintended edit** and we find it now, not in six months.
- [ ] Symbols present and correct.
- [ ] Position limits even, IC = 2.
- [ ] Automations forked — original's list unchanged.
- [ ] Template V1 saved with the pre-registration in Notes.
- [ ] Rename done in the right order; `rename_map.csv` row written.
- [ ] Both toggles screenshotted.
- [ ] `data/captures/<session-date>-pilot/` committed.

### ⏳ DEFERRED TO DAY-0 — order-level verification

**Cannot be done today. The account is inactive and nothing will trade.**

On Day-0, before this bot may take a position:

- [ ] Open the **first new position** and read its **Trades list**.
- [ ] It must contain **a PT row** and **a time-exit row**.
- [ ] If the backstop was built: check it is **not** the thing closing positions
      (`BACKSTOP_CAUGHT_IT`). A backstop doing the work means the Exit Options side is dead.

> ### ⛔ THE EXIT OPTIONS PANEL IS NOT EVIDENCE.
> Exit Options are copied onto a position **at open**. The panel shows the automation's current
> settings, which can diverge from every live position silently and indefinitely. In v1 the
> Fortress positions generated **no exit orders at all — never sent** — while the panel
> displayed `PROFIT % 50%` the whole time.
>
> **The Trades list is the only order-level ground truth. This has no exception, and it is the
> reason this bot is being rebuilt.**

---

## IF SOMETHING GOES WRONG

**You cannot break anything unrecoverable today** — the original is intact until Step 8, and
nothing trades.

| Symptom | What it means | Do this |
|---|---|---|
| Original's automation list changed at Step 2 | The fork did not take; you are editing shared objects | **Stop.** Tell me. Do not proceed to Step 5. |
| Capture `.txt` shows only automation names | Tree was not expanded — the branch is missing from the DOM | Re-expand every caret and re-grab |
| Symbols panel empty after Step 3 | Trap 2 | Re-add. Verify by reading, not by remembering |
| You edited the original by mistake | Recoverable — it is being archived anyway | Tell me exactly what changed so the record is accurate |
| 15:52 not reachable | Known unknown, Decision Point B | **Do not substitute a time.** Leave unbuilt, flag it, finish the card |
| Anything else surprising | — | **Stop and describe what you see.** Do not improvise a spec. |

---

## WHAT I NEED FROM YOU AT THE END

Paste or upload:

1. `data/captures/<session-date>-pilot/` — both capture sets and the screenshots
2. Answers to the two open questions:
   - **Preset control exists in the Exit Options panel?** yes / no
   - **Can a Scheduled Event reach 15:52?** yes / no / what the trigger options actually are

   *(The `EXIT OPTIONS` toggle question is closed — its existence is established by the rep's
   screenshot and your fleet-wide observation. Only whether flipping it ON re-arms exit-order
   generation is open, and that is a Day-0 Trades-list question, not a today question.)*
3. Anything that surprised you, however small

Then I run the capture-diff, write up what the pilot found, and we decide whether the ritual is
clean enough to run on the remaining three clones.

> **The pilot's job is not to produce one good bot. It is to find out where the ritual breaks
> before it runs nine times.** A step that felt awkward is a finding. Tell me about it.
