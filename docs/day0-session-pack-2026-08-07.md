# Day-0 session pack — written 2026-08-07

**What this is.** Four ready-to-paste session prompts covering reactivation day end to end, written
while the OA account is locked so that Day-0 runs on **Pro-tier models with zero re-derivation**.
Each prompt is self-contained: paste it into a fresh chat, and that session knows what it needs
without reading this file first.

**What this is NOT.** It is not a plan. `docs/reactivation-runbook.md` (801 lines) is the plan and it
governs. **These prompts EXECUTE it. Nothing here re-plans, re-orders or re-scopes a runbook step**,
and where the lockout forced a sequencing question it is raised as an Andy gate (S0 gate A2), never
resolved silently.

**This session wrote exactly one file — this one.** No existing doc was edited. No OA action was
attempted (impossible — the account is disabled). No git command in any form.

---

# §0.0 · ⛔ AMENDMENTS — ADDED 2026-08-07 (evening), AFTER AN ADVERSARIAL REVIEW. READ BEFORE §0.

> **How to read this section.** The body of this pack below is **left standing exactly as written**
> — nothing in §0–§4 was deleted or rewritten. Every correction lives here, dated, with the
> evidence that forced it. **Where an amendment and the original body text conflict, the amendment
> wins.** Each amendment names the location it governs. Short pointers were also inserted inside
> the four prompt blocks, because a prompt pasted into a fresh chat never sees this section unless
> it is read — **every prompt's READ FIRST list now names `§0.0` explicitly.**
>
> Two things happened between the pack being written and this review: (1) the account was paid and
> came back **empty**; (2) four items the pack records as open were ruled and recorded in the
> folder. Neither was known to the authoring session. **This section is the delta.**
>
> ⚠️ **These are corrections and gates. Not one of them rules a decision.** Where the review found
> a decision that needed making, the amendment routes it to Andy rather than resolving it.
> **Andy may reject any amendment at commit review** (`CLAUDE.md` §5).
>
> ⛔ **UPDATED 2026-08-07 (post-S0b): 27 amendments, A-01…A-27. A-27 IS FILED LAST AND IT IS THE
> ONE THAT GATES S2's OPENING** — it carries Andy's four S0b rulings, including a hard
> carry-forward that **the seven greenfield bots' EXIT OPTIONS state must be re-read first-hand
> immediately before Step 7 and never inherited.** Read A-27 before starting S2.
>
> **26 amendments, A-01…A-26.** ⭐ **A-26 is filed OUT OF NUMERIC ORDER — it sits immediately after
> A-15 because it supersedes A-15's hand-derivation fallback.** It is the one amendment that adds a
> tool rather than a gate: **the A-series now executes via `python3 scripts/a_series.py`.**

---

## ⛔ A-01 — THE ROSTER WAS LOST. GATE A0 COMES BEFORE EVERYTHING, INCLUDING S0 STEP 1.
**Governs: §1.1, §1.2, S0 Step 3, and the opening line of S1, S2 and S3.**

**[Evidence: dated first-hand block, `docs/state.md` (read directly 2026-08-07), "⛔ OA REACTIVATED
BUT ROSTER LOST — 2026-08-07, ~12:06–12:30 ET": `/bots` with all filters cleared read **"0 active
bots • 50 left in your plan"**. SURVIVED: the Automation Library (all 4 objects, each reading
"Unused"), all 9 Bot Templates, and the Bot Archive (1 bot). LOST: every active bot. OA support
(Zack), ~12:30 ET, in writing: *"We will restore the bots promptly… operational again by
Monday."*]**

**§1.1's "Expected roster at reactivation: 41 active bots" is superseded-in-part.** It is the right
arithmetic for a **restored** account and the wrong one for a rebuilt or partially restored one.

### GATE A0 — run this before S0 Step 1, and before starting S1, S2 or S3.
1. Read `docs/state.md`'s incident block (tail of file) **and** `docs/rebuild-contingency-2026-08-07.md`.
2. Open `/bots` with **all filters cleared** and read the footer.
3. Take **one** of the three branches below. ⛔ **There are three, not two.** `state.md`'s branch is
   binary; the third is the state this review found it does not cover.

**BRANCH 1 — CLEAN RESTORE.** Footer reads **41 active · 9 left**, AND every name in S0 Step 3's
list (as corrected by A-05) is present as written, AND every bot ID and automation `rid` matches
its recorded value (A-01c below). → Run the pack as written, with every amendment in this section
applied.

**BRANCH 2 — NO RESTORE.** Footer reads 0, or nothing recognisable came back. → ⛔ **DO NOT run S0
Step 3 cold. DO NOT run S1, S2 or S3 at all** — they operate on bots that do not exist, and
`rebuild-contingency-2026-08-07.md` §2 records that PR-02's and PR-04's originals were themselves
lost with no template, so there is nothing left to clone from. Read the contingency doc, honour its
§4 DO-NOT-START gate, and hand to Andy. **No OA write of any kind.**

**BRANCH 3 — ⛔ PARTIAL, ALTERED, OR STILL-MOVING RESTORE. THIS IS THE BRANCH THE FOLDER DID NOT
HAVE, AND IT IS THE MOST LIKELY ONE.** Anything that is not Branch 1 and not Branch 2 is Branch 3.
**Default disposition: STOP. NO OA WRITE. FLEET STAYS OFF. ESCALATE TO ANDY: YES.** Record which
sub-state you are in, by name, with first-hand evidence:

| Sub-state | How you detect it | What you do |
|---|---|---|
| **a. Count ≠ 41** (short **or** long) | `/bots` footer | STOP. A long count may be the two 08-06 deletes or an archived original coming back — that is a finding, not a tidy-up. ⛔ **DELETE NOTHING. ARCHIVE NOTHING.** |
| **b. Roster still moving** | two captures disagree | ⛔ **A second capture that agrees is NOT a capture defect resolved — it is a restore still landing.** See A-08. |
| **c. Names match but IDs / `rid`s changed** | read `a5.bots.bot`'s id per bot against `data/bots_config_v2.csv`; read each shared automation's `rid` against `RTfw5TkkCRF178605283747821` (ScannerA) · `RTfw5TkkCRF178606271659881` (ScannerB) · `RTfw5TkkCRF178606373201751` (Backstop) | STOP. The objects were **re-created, not preserved**. Every capture file, CSV row, doc citation and signed config hash is keyed to a dead identifier. ⛔ **The A-series cannot see this — every assert in it is relational and passes on a faithful re-creation.** Not repairable by a session. |
| **d. Config rolled back to an older snapshot** | S0 Step 4b (A-07) — field-by-field diff against each bot's own capture file | STOP for the affected bots. Watch specifically for: `disableExits` back to 0, PT25 back in the champion clone's Open actions, the re-entry gate absent, Cleanup back on Market, `itmpaper` back to `auto`, exits bundles unlinked. ⛔ **A bot that "already looks correct" after a rollback past its own creation is not a pass** — without the diff you cannot tell a restored-correct bot from a never-edited one. |
| **e. Automations restored but detached or re-created** | `My Automations` bot-counts ≠ 7/7/7/2, or a `rid` changed | STOP. Re-attaching a re-created object creates a new object, not the shared one. ⛔ Do not re-attach to make the count look right. |
| **f. Archive / rename state lost → name collisions** | two bots under one production name, or an `-ARCHIVED-` name back on `/bots` | STOP. ⛔ **Do not rename and do not archive to resolve it** — renames commit and are not reversible from this side. |
| **g. Positions did not come back, or came back different** | the five open mirror positions (S2 Step 2) | See A-10. The ride-or-close decision is **mooted, not preserved** — a forced outcome recorded as a decision is a record that lies. |
| **h. Restore lands MID-SESSION** | anything appears that was not there at gate A0 | ⛔ STOP at the current per-bot boundary, write the close-out, and **re-run gate A0 in a fresh chat.** Do not absorb a changing account into a session already in flight. |

⛔ **Branch 3 is never resolved by a session's own judgment, and never by re-capturing until the
numbers agree.** The contingency doc's §4 DO-NOT-START gate governs everything downstream of it.

---

## ⛔ A-02 — GATE A1 IS ALREADY SATISFIED. DO NOT ASK ANDY TO PURCHASE AGAIN.
**Governs: §0.3 gate A1, S0 Step 1, S2 Step 1.**

**[Evidence: `docs/state.md` incident block, dated ~12:06–12:10 ET 2026-08-07, first-hand from
Andy's screenshots: "plan purchased, login works."]**

S0 Step 1 as written (*"Wait for gate A1… Do not attempt to log in or pay"*) would have a Sonnet
ask Andy to buy a plan he already owns. **Replace it with: read the payment timestamp from
`state.md`'s incident block and have Andy confirm it in one line.**

⛔ **AND `LEDGER_START` IS NOW A GATED QUESTION, NOT A COPY.** The runbook says *"This date is
`LEDGER_START`"* on the assumption that payment and Day-0 are the same day. They are not: payment
was 2026-08-07 and the roster does not exist until the restore lands. **A `LEDGER_START` of
2026-08-07 claims an era in which the account held zero bots.** S2 Step 1 must **ask Andy** whether
the era starts at the payment timestamp or at the first day a bot is actually switched ON, record
the answer verbatim, and only then set it. ⛔ Do not choose. The rest of Step 1 — set it, run
`build_ledger.py`, require row count 0 / EMPTY LEDGER n=0 — is unchanged and still binding.

---

## ⛔ A-03 — §1.3(a) AND §1.3(b) ARE FALSIFIED. GATE A3 BECOMES *VERIFY*, NOT *RE-ASK*.
**Governs: §1.3(a), §1.3(b), §0.3 gate A3, S0's gate A3 block, S0 Step 7(a) and 7(b).**

**[Evidence: direct read of the files, 2026-08-07. `docs/state.md` carries — verbatim —
"⛔ **OA ACCOUNT FULLY DISABLED — 2026-08-07, ~04:24 ET. LOGIN ITSELF NOW BLOCKED.**" with the
first-hand screenshot record; and "⛔ ~~**F-C1 — GATED, NEEDS ANDY.**~~ ✅ **F-C1 — RULED
2026-08-07 (Andy, first-hand): REMOVE.**" and "✅ **F-C2 — RULED 2026-08-07 (Andy, first-hand):
AUTHORIZED AS TRAP 10.**". `docs/session-log.md` carries the same banner: "### ⛔ FINDING F-C1 …
~~GATED, NOT ACTED ON.~~ ✅ RULED 2026-08-07 — REMOVE."]**

§1.3 says all three divergences are missing from the folder. **Two of the three are in the folder
and were already in it when the pack was written.** Only §1.3(c) (uncommitted work) survives as
stated.

- **Gate A3 is DISCHARGED as a ruling.** Do **not** ask Andy to re-confirm F-C1 or F-C2. Read the
  two `state.md` blocks and confirm they say REMOVE and AUTHORIZED AS TRAP 10. ⛔ **A ruling
  recorded first-hand in the folder is never retracted by a session's failure to get it re-said** —
  A3's decline branch as written would do exactly that.
- ⚠️ **What is still outstanding is the APPLICATION, not the ruling.** `state.md` says of F-C1:
  *"Not yet applied to either bot"*. **S0 Step 5 and S1 step 6 stand unchanged** — they are the
  application.
- **S0 Step 7(a) and 7(b) become VERIFY-AND-REPORT.** Read the blocks, confirm they are there,
  report "already recorded". ⛔ **Do not write a second dated banner for either** — a duplicate
  ruling banner in the project's single source of facts is worse than a missing one.
- What S0 must still record is what gate A0 found: the restore state, first-hand.

---

## ⛔ A-04 — GATE A8 IS **ONE** OPEN ITEM, NOT THREE.
**Governs: §0.3 gate A8, S2 Step 2b's "THREE OPEN SIGNATURE ITEMS".**

**[Evidence: `docs/state.md`, dated block "📝 RULED 2026-08-07 (Andy) — four open items closed":
"**G-12b — SIGNED AS DRAFTED.** … δ=0.10R, p=0.20, floor n_matched_days≥100 + one re-arm at
Day-0+9mo, INSIDE the family correction, publication cap acknowledged… exact ledger text pasted
into `pre-registration-ledger.md`" and "**G-1′ — DECLINED.**" The same block: "PR-18's 'Breakeven'
naming, remain open and gated."]**

- **(i) G-12b — SIGNED. ⛔ DO NOT RE-PRESENT `[ 0.10 | other ]` TO ANDY.** Any answer that is not a
  verbatim repeat silently forks a signed pre-registration. **Verify the pasted text is in the
  ledger's PR-14…PR-17 entry, scoped to PR-16, and move on.**
- **(iii) G-1′ — DECLINED.** Do not re-open it. Its two ruling-reopeners are already carried
  correctly at S2 close-out item 4 — that part of the pack is right and the Step 2b text is stale.
- **(ii) PR-18's "Breakeven" naming — STILL OPEN AND STILL ANDY'S.** Ask; do not choose. This is
  the whole of gate A8.

---

## ⛔ A-05 — S0 STEP 3'S NAME LIST CONTAINS AN ARCHIVED BOT. AS WRITTEN IT FIRES A FALSE FLEET-STOP.
**Governs: S0 Step 3's "Confirm by name" list.**

**[Evidence: `reactivation-runbook.md` §3 Step A, first-hand 2026-08-04: *"the original is
`QQQ-IC-0DTE-Fortress-ARCHIVED-2026-08-03` and archived."* `docs/state.md` incident block: the Bot
Archive holds *"exactly the 1 expected bot, `Fortress-ARCHIVED-2026-08-03`"*. And §1.1's own
arithmetic — the pilot clone replaced its original one-for-one inside the 35.]**

`QQQ-IC-0DTE-Fortress-ARCHIVED-2026-08-03` **is not one of the 41 and must NOT appear on `/bots`.**
Step 3's branch (*"IF A BOT IS MISSING… same STOP"*) is unconditional, so a session that cannot
find it halts the entire fleet over a bot that is exactly where it belongs.

**Corrected clause:** confirm `QQQ-IC-0DTE-Fortress` (the pilot clone, holding the production name)
on `/bots`. ⚠️ **Its original `-ARCHIVED-2026-08-03` lives in the Bot Archive. If it IS on `/bots`,
THAT is the finding** — A-01 branch 3f.
⚠️ Contrast, and the pack is right about this one: `IC-SPX-FastPT25-S2-ARCHIVED-2026-08-07` **was
renamed, not archived**, so it *is* expected on `/bots` and it *does* count toward 41.

---

## ⛔ A-06 — A STOP DOES NOT PROPAGATE ACROSS THE SESSION BOUNDARY. IT MUST.
**Governs: the opening line of S1, S2 and S3.**

S1 opens *"S0 has run"*, S2 *"S0 and S1 have run"*, S3 *"Day-0's sequence has run"* — none branches
on what the previous close-out actually **says**. The STOP ladder's *"fleet stays OFF → stop the
sequence"* is unenforceable across four separate chats with no shared memory, and S1 is explicitly
cleared to run **unattended**.

**Insert as the first instruction of S1, S2 and S3, before any work:**
> ⛔ **PRECONDITION — READ THE PREVIOUS SESSION'S CLOSE-OUT FIRST, IN THE FOLDER, NOT FROM MEMORY.
> IF it records a `FLEET STAYS OFF` verdict, OR gate A0 landed on branch 2 or branch 3, OR no
> close-out exists, OR its hand-off block is absent or incomplete → DO NOT START. Record
> `BLOCKED ON <session> — <verbatim branch>` and hand to Andy. A hand-off you had to reconstruct is
> a hand-off that did not happen.**

---

## ⛔ A-07 — NEW S0 STEP 4b: THE THIRTEEN NON-GREENFIELD BOTS GET NO POST-RESTORE CONFIG CHECK.
**Governs: S0, between Step 4 and Step 5. Runs on gate-A0 branch 1 only.**

Every post-restore config check in the pack is scoped to the seven greenfield arms (A1/A2/A3/A8/A9
are all n=7). The PR-01 clone, the pilot, the two un-started clone originals and **the nine** go
from "lost" to "signed at Step 2b and switched on at Step 7" without their configuration ever being
re-read. S0 Step 5's F-C1 verification is a **post-edit self-check**, not a pre-edit baseline: a
session that finds `profits` already absent because the restore rolled the bot back past its own
creation reads that as success.

> **STEP 4b — RE-CAPTURE AND DIFF EVERY NON-GREENFIELD BOT.** For `IC-SPX-FastPT25-S2` (the clone),
> `IC-SPX-FastPT25-S2-ARCHIVED-2026-08-07`, `QQQ-IC-0DTE-Fortress`, `IC-SPX-FastPT25-S2-130PM`,
> `QQQ-IC-0DTE-Fortress-NoPT50`, and each of the nine: fresh capture after a hard reload, resolve
> the input chain two hops where one exists, and diff **field-by-field against that bot's own
> capture file on disk**. ⛔ **ANY DIFF → that bot's config-capture hash is NOT ESTABLISHED, its
> entry CANNOT be signed at Step 2b, the bot STAYS OFF, the fleet proceeds, ESCALATE: YES.**
> ⛔ **A capture file written before the roster was lost is a record of a bot that no longer
> demonstrably exists.** Do not sign against one without this diff.

---

## ⛔ A-08 — "RECAPTURE ONCE" MUST NOT CONVERT A LANDING RESTORE INTO A PASS.
**Governs: S0 Step 3's `IF THE COUNT DISAGREES -> recapture ONCE` branch.**

That branch was inherited from `reactivation-runbook.md` §3 Step B, which was written for a
bookmarklet that mis-scrapes — not for a roster being repopulated by OA support. As written, first
capture 37 → second capture 41 reads as *"the first capture was bad, proceed"*, and the A-series
then baselines a roster that is still acquiring objects.

> ⛔ **IF THE FIRST AND SECOND CAPTURES DISAGREE, THAT IS A-01 BRANCH 3b — A MOVING ROSTER — UNTIL
> PROVEN OTHERWISE. Record both counts with their timestamps, wait 30 minutes, capture a THIRD
> time, and require TWO CONSECUTIVE IDENTICAL captures before proceeding. IF THE THIRD DIFFERS FROM
> THE SECOND → STOP. FLEET STAYS OFF. ESCALATE: YES.** Carry both timestamps and the
> two-consecutive-match confirmation into the close-out.

---

## ⛔ A-09 — STEP 2c IS SPENT BY THE TRANSITION, NOT BY THE SESSION THAT REACHES IT.
**Governs: S0 (new read, before Step 2) and S2 Step 2c.**

Step 2c is the one irreversible observation in the plan, and the pack schedules it **two sessions
after** the inactive→active transition it measures. Worse: that transition **already happened** at
~12:06 ET 2026-08-07, and the roster was wiped and is being restored across it.

**(a) S0 takes the reading, as a READ, before anything else.** Insert before S0 Step 2:
> ⭐ **BEFORE ANY OTHER OA ACTION: screenshot BOTH dashboard toggles on ONE live mirror and ONE
> directional bot. READING AND SCREENSHOTTING IS NOT TOUCHING** — you flip nothing, you open no
> editor, you change no value. Record the filenames and the timestamp in the close-out under
> `2c PRE-OBSERVATION`. ⛔ **This does NOT replace S2 Step 2c and licenses no other contact with
> the nine** — it preserves information that Step 2c would otherwise find already spent.

**(b) S2 Step 2c gains a confounding branch:**
> ⛔ **IF THE ROSTER WAS RESTORED BY OA RATHER THAN SURVIVING INTACT, THIS OBSERVATION IS CONFOUNDED
> BY THE RESTORE.** A restored bot's toggle state is whatever the snapshot or OA's restore default
> carries; it cannot separate billing-state from hand-set. Record `NO-TOUCH OBSERVATION CONFOUNDED —
> RESTORE`, treat it as ⬜ NOT EVALUABLE, and say so **inside the Step 6a verdict** — a CONFIRMED
> verdict resting on it is weaker than it looks, and `rebuild-contingency-2026-08-07.md` §2 already
> records the rebuild case as **foreclosed, not delayed**.

---

## ⛔ A-10 — GATE A6: RE-READ THE FIVE POSITIONS FIRST-HAND, AND BRANCH FOR "GONE OR CHANGED".
**Governs: S2 Step 2.**

Step 2 quotes *"~$13K risk, ~−$10.8K unrealized"* from the **2026-07-30** capture and puts it in
front of Andy at the one gate the pack itself labels a capital decision. It also has no branch for
the positions not surviving the wipe — and its completion condition (*"EXECUTED FOR ALL FIVE"*) is
then unsatisfiable, deadlocking the sequence at `DO NOT PROCEED TO STEP 3`.

> ⛔ **FIRST, BEFORE EITHER BRANCH: re-read all five positions first-hand — quantity, open date,
> current mark, unrealized P/L — and open EACH POSITION'S OWN EXIT OPTIONS SCREEN AND SCREENSHOT
> IT.** That per-position screen is the third toggle surface, it has never been observed on a
> lapse-surviving position (Step 3's own rider says so), and **a CLOSE destroys it permanently.**
> Reading and screenshotting a position is not toggle intervention.
> **BRANCH: all five present → proceed as written, using the FRESH numbers. Do not present a stale
> number to Andy at a capital gate.**
> ⛔ **FEWER THAN FIVE, OR ANY POSITION MATERIALLY CHANGED → the outcome was FORCED BY THE INCIDENT,
> NOT CHOSEN BY ANDY.** Record `RIDE-OR-CLOSE MOOTED BY THE 2026-08-07 ROSTER LOSS` in the ledger
> entry and in `state.md`, naming which survived and which did not, get Andy's explicit
> acknowledgment of that record, and only then proceed to Step 2b. **A forced outcome recorded as a
> decision is a record that lies** (`rebuild-contingency-2026-08-07.md` §2).

---

## ⛔ A-11 — THE FIRST-POSITION EXCEPTION HAS NO MECHANISM. DO NOT INVENT ONE.
**Governs: S2 Step 6. ⚠️ RUNBOOK-LEVEL in origin — `reactivation-runbook.md` §4 Step 6 has the
same hole and is not this session's to edit.**

*"The bot is allowed EXACTLY ONE position at 1 LOT"* names no control. The only way to make a
position exist is `AUTOMATIONS` → ON, which Step 3 forbids and Step 7 gates — and nothing caps the
bot at one (the greenfield arms carry `limits 2/2`, the PR-01 clone `10/10`). A session that
improvises here reproduces the v1 failure the pack quotes at −$9,618, with Step 7 gating nothing.

> ⛔ **DO NOT IMPROVISE THE MECHANISM AND DO NOT BATCH IT.** Attempt the button test-fire first and
> record verbatim whether the control exists. If it does not: **STOP and put the mechanism to Andy
> as a gated question** — changing a signed bot's position limit is a config change on a signed
> entry, and turning `AUTOMATIONS` ON early is the act Step 3 forbids. Whatever he authorizes:
> **ONE BOT AT A TIME, never a batch; screenshot every transition; read the Trades list the moment
> the position opens.** ⛔ **IF ANDY IS NOT AVAILABLE TO RULE IT → that bot's Step 6 is ⬜ NOT
> EVALUABLE and IT STAYS OFF.** Never spend a live position to route around an unanswered question.
> ⚠️ **AND "TEST-FIRE UNAVAILABLE" IS NOT DECIDABLE FROM ONE SCREEN.** Step 3's own rule applies
> here: **a surface you did not open is not an absent control.** If no doc names where the
> test-fire lives, that is ⬜ NOT EVALUABLE — not "unavailable".

---

## ⛔ A-12 — STEP 6b: DO NOT EDIT A SIGNED ARM, AND THE READ IS AMBIGUOUS AS SPECIFIED.
**Governs: S2 Step 6b's SET UP and its first two branches.**

**Two independent defects.**

**(a) PR-20 is a SIGNED tournament arm.** Its whole mechanic is `profits 0.05` + `smprofits speedy`
(§1.1). Adding `dstop` to it after Step 2b has signed its config: falsifies **A1** (it now differs
from the control in two mechanics), falsifies **A3** — *"the load-bearing one"* — and voids the
config hash its signature cites. A later A-series run then reports a red that the pack's own Step 4
branch escalates as `FLEET STAYS OFF for the family`, over an edit this pack ordered. And
`profits 0.05` will usually close the position before any `dstop` can fire.
> ⛔ **DO NOT EDIT A SIGNED ARM TO CLOSE AN OBSERVATION, AND DAY-0 IS NOT A BUILD DAY. Put it to
> Andy: run C10 on an instrument OUTSIDE the tournament, or leave C10 OPEN.** If no such instrument
> exists on the day, **C10 STAYS OPEN** — say so by name in `state.md` and at close-out; ARM-B1
> stays blocked, which is where it already is. Standing up a separate canary is a plan question.

**(b) "CONTRACT COUNT" IS UNDEFINED AND THE TWO BRANCHES CAN COLLAPSE.** The step says record
*"CONTRACT COUNT PER LEG"* and then branches on `−$100 × (CONTRACT COUNT)`. **At 1 contract per
leg, per-leg count = 1, so `−$100` and `−$100 × 1` are the same number** — the two primary branches
become indistinguishable and `FIRED AT NEITHER FIGURE` is unreachable.
> ⛔ **IF C10 IS RUN AT ALL: the discriminating quantity is TOTAL CONTRACTS ON THE POSITION (a
> 1-lot iron condor = 4), not contracts per leg. Record BOTH numbers — per leg and total — before
> the position opens, and state which one each branch is read against. IF THE TWO CANDIDATE FIGURES
> ARE EQUAL FOR THE INSTRUMENT YOU ACTUALLY HAVE → the read cannot discriminate: report
> `C10-UNRESOLVED`, do NOT report C10 CLOSED, and do not fit a basis to one data point.**

---

## ⛔ A-13 — A7 COVERS **3** SHARED AUTOMATIONS. THE RUNBOOK REQUIRES **4**.
**Governs: S0 Step 4's A7, S2 Step 0 and Step 4(b).**

**[Evidence: `reactivation-runbook.md` §4 Step 4, verbatim: *"the payload hash of each of the four
shared automations, written to `bots_config_v2.csv`'s shared-object rows"*. Against §1.1: the
Library holds four objects — the three GF objects **plus `Defang-Mon-S2-StrikeTouch` (2 bots)** —
and the pack supplies baselines for three.]**

`Defang-Mon-S2-StrikeTouch` is shared by 2 bots, so an edit to it propagates to both with no
template bump — exactly the blast radius A7 exists to detect, and the pack calls A7 *"THE ONLY
DETECTOR"*. It is also the object the two control clones' S2 monitor depends on.
> ⛔ **Report A7 as `3/4`, with `Defang-Mon-S2-StrikeTouch` named as ⬜ NOT EVALUABLE — no recorded
> baseline. DO NOT REPORT 3/3 AS COMPLETE and do not tick the runbook's Step 4(b) box on it.**
> Recording the fourth baseline is a read-and-record, not an edit, and is allowed: read it after a
> hard reload, hash it, write the row to `bots_config_v2.csv`, and say plainly that it is a
> **first** baseline, not a re-verification.

---

## ⛔ A-14 — "NO COORDINATE FALLBACK" DOES NOT BAN THE ONLY CLICK METHOD THAT WORKS.
**Governs: §0.2 and the inline STOP ladder in all four prompts.**

§0.2 says *"Do NOT fall back to raw coordinates"* — correct. The inline copies dropped the word
**raw**: S0 *"do not fall back to coordinates"*, S1 and S3 *"no coordinate fallback"*. Standing
fact 6 makes DOM-computed coordinates **the documented method**, not a fallback. A literal session
hits its first silent ref no-op, reads the ladder, and concludes it has no method left.
> **Read every ladder as: do not fall back to RAW / EYEBALLED coordinates. DOM-COMPUTED coordinates
> (`scale = screenshotWidth / window.innerWidth`, click at `rect.centre × scale`, re-derived after
> any resize) ARE the documented method — use them freely. The ONE documented alternative for a
> failed click is: fresh screenshot → re-derive the scale → re-click once. ⛔ The raw-coordinate ban
> is absolute on the bot `…` menu (fact 8) and there it means exactly what it says.**

---

## ⛔ A-15 — S0 IS TOLD TO RUN THE A-SERIES AND TO WRITE NOTES WITHOUT THE SOURCE TEXT FOR EITHER.
**Governs: S0's READ FIRST list, S0 Step 4, S0 Step 6; S1's READ FIRST list and step 8.**

S0 must *"Build against the AMENDED text, not the struck one"* for A1, and compare each arm's
decoded set to *"its pre-registered set"* for A3 — but `docs/greenfield-family-spec.md` **is not on
S0's read list** (it appears only on S2's). Separately, S0 Step 6b and S1 step 8 require the PR-01
and PR-02 **Notes / pre-registration note text**, and `docs/pre-registration-ledger.md` is on
neither list. A session that composes a Notes block and then "verifies byte-exact against the
source" is verifying its own invention.
> **ADD to S0's and S1's READ FIRST lists:**
> `docs/greenfield-family-spec.md` — **§8.3** (the A-series; A1's AMENDED text is authoritative and
> the struck version is marked in place — do not run A1 from this pack's one-line summary) and
> **§9** (the seven DRAFT entries — each arm's pre-registered set is **A3's comparand**).
> `docs/pre-registration-ledger.md` **§4** — the PR-01 / PR-02 entries. **This is the source text
> for the Notes block and for the template's attached note; there is no other.**
> ⛔ **IF YOU CANNOT LOCATE THE EXACT NOTE TEXT → STOP. DO NOT COMPOSE ONE.** These are record
> artifacts and nothing in the Day-0 sequence reads them: record NOT DONE and carry forward, per
> Step 6's own branch.
> ⚠️ **AND THE HASH PROCEDURE IS IN NO PROMPT.** ⭐ **SUPERSEDED 2026-08-07 (evening) by A-26 —
> THE A-SERIES NOW HAS A RUNNER: `python3 scripts/a_series.py`. RUN IT; DO NOT HAND-DERIVE THE
> ASSERTS OR THE HASHES.** The fallback below stands only if the script is absent or will not run:
> use exactly the procedure recorded in
> `data/captures/2026-08-07-greenfield/ASSERTS-A1-A9-and-capture-diff.txt`, which produced the
> baselines you are comparing to. **IF THAT FILE DOES NOT STATE THE SERIALIZATION → A7 IS ⬜ NOT
> EVALUABLE. Do not invent a hash input, and never compare a recorded baseline to itself.**

---

## ⭐ A-26 — THE A-SERIES EXECUTES VIA `scripts/a_series.py`. SESSIONS RUN IT; THEY DO NOT HAND-DERIVE IT.
**Governs: A-13, A-15, S0 Step 4, S2 Step 0 and Step 4(b). Added 2026-08-07 (evening), at Andy's
instruction.**

**[Evidence: Andy, first-hand 2026-08-07 — built and verified: reproduces the hand-run reference
exactly, name-keyed so it survives an id-rekeying restore, RED paths negative-tested. Corroborated
by a direct read of the file the same evening: `scripts/a_series.py`, 33,345 bytes, module
docstring — *"`--validate` asserts this tool reproduces it EXACTLY: A1 21/21 · A2 7/7 · A3 7/7 ·
A7 3/3 · A8 7/7 · A9 7/7; A4 MOOT; A4b/A6 NOT-RUNNABLE pre-Day-0; A5 NOT-RUN"* and *"NEVER
HARDCODE OA OBJECT IDS… family membership keys on the STABLE bot NAME (GF-QQQ-IC-<Arm>), never on
an id."*]**

**HOW TO RUN IT.** `python3 scripts/a_series.py` — defaults resolve `data/captures/`,
`data/bots_config_v2.csv` and `docs/greenfield-family-spec.md` on their own; override with
`--captures` / `--config` / `--spec` if the session is pointed elsewhere. Useful flags:
`--validate` (assert it still reproduces the 2026-08-07 hand-run reference — **run this FIRST on
Day-0, before trusting any verdict it gives**), `--json` (machine-readable output for the
close-out), `--emit-wiring` (prints the `daily.sh` snippet as a COMMENT; it does not edit
`daily.sh`).

**WHAT IT DISCHARGES.** The serialization/hash question in A-15 · A3's comparand (the §9
pre-registration mechanics are encoded in the tool, so A3 is config-independent and catches
all-arms-mistyped-identically) · the G2 rider two hops deep (it reads the **bot input object's**
decoded value and ignores both the action reference and `oldValue`) · the arithmetic of A1's
amended 21-pair rule. ⛔ **A hand-derived assert is now the fallback, not the method — a session
that hand-runs the A-series when the script is available is inventing a second procedure.**

⛔ **WHAT IT DOES *NOT* DISCHARGE — read this before reporting anything green:**
1. ⛔ **A-01c STILL APPLIES, AND THE SCRIPT'S OWN DESIGN IS WHY.** It is **name-keyed by
   construction** and never reads an OA id — which is exactly what makes it survive a rekeying
   restore, and exactly why **it cannot detect one**. A restore that re-creates every object under
   the same names produces a **fully green A-series** over dead identifiers. **The bot ID and
   `rid` comparison at gate A0 / Step 3 is a separate, manual, still-mandatory check.**
2. ⛔ **A-13 IS UNCHANGED: the script's `SHARED_AUTOMATIONS` list carries the same THREE objects.**
   `Defang-Mon-S2-StrikeTouch` is not in it. A green `A7 3/3` from the tool is still **3 of the 4**
   the runbook requires — report it as **3/4** with the fourth named ⬜ NOT EVALUABLE.
3. ⛔ **THE `daily.sh` WIRING GATE IS STILL OPEN.** The file's own header, read first-hand:
   *"⛔ STANDALONE. NOT wired into `scripts/daily.sh`… wiring is a Day-0-adjacent decision
   (`reactivation-runbook.md` §4 Step 4(b)) and this tool does not edit daily.sh."* A runner
   existing is not a nightly detector existing. **S0 and S2 still report Step 4(b) as an OPEN
   gate**, and it stays Andy's call whether the family trades today without a nightly A7 (A-24).
4. **A5 is still fed by hand** from the `/settings` read (S0 Step 2), and **A4b and A6 remain
   not-runnable until positions exist** (Day-1, S2 Step 8). The tool reports them as such; do not
   read `NOT-RUNNABLE` as a pass.
5. ⚠️ **Its `VERSION` string still reads `0.1.0-DRAFT`** (direct read, same evening). Stated as an
   observation, not an objection — Andy's verification is the authority on its fitness. **If
   `--validate` fails on Day-0, that is a defect in the tool, not in the record: STOP, report it,
   fall back to the A-15 hand procedure, and do not silently re-baseline.**
6. ⛔ **Its `PRE_REGISTRATION` table is a spec surface.** Changing an arm's entry there is an
   *"amend the plan"* edit, not a fix. ⛔ **A session never edits this script to make an assert
   pass.** `scripts/` is Claude Code's lane (`CLAUDE.md` §7); Day-0 sessions **run** it.

---

## ⛔ A-16 — TWO PLACES WHERE THE RUNBOOK AND THIS PACK GIVE OPPOSITE INSTRUCTIONS.
**Governs: S1's "Run runbook §2's nine steps in order". ⚠️ Both are RUNBOOK-LEVEL findings —
flagged, not fixed. `reactivation-runbook.md` is not this session's to edit.**

**(a) ORDER.** Runbook §2 is *"1. Clone the original bot … 8. Rename the original"*. S1's list is
`0. baseline capture … 1. RENAME THE ORIGINAL FIRST … 2. CLONE`. A literal session obeying the
sentence *"Run runbook §2's nine steps in order"* clones first, and the Clone Settings drawer then
cannot take the production name because the original still holds it.
> **THE PACK'S ORDER SUPERSEDES §2's NUMBERING AND IT IS THE ONLY ORDER YOU FOLLOW.** Read §2 for
> its **branches and trap text**, not its sequence. Two deliberate changes, both learned on PR-01:
> a Step-0 baseline capture is ADDED before anything; the RENAME moves before the clone. **Where
> they disagree on ORDER, the pack wins. Where they disagree on a BRANCH, stop and gate it.**

**(b) PT25.** `reactivation-runbook.md` §2 step 7 still carries, verbatim: *"⛔ **IF PT25 is still
present on a control clone's Open Position action** → **do not remove it yourself.** … **Bot stays
OFF · escalate to Andy: YES.**"* — the pre-ruling text. It was never amended for F-C1.
> **THAT TEXT IS SUPERSEDED** by F-C1 RULED: REMOVE (Andy, first-hand, 2026-08-07, recorded in
> `docs/state.md` and `docs/session-log.md`). **Do not treat the conflict as ambiguity and do not
> stop on it.** ⛔ **Report the un-amended runbook line at close-out as a doc-correction item for
> Andy** — the runbook is a decision surface and amending it is his.

---

## ⛔ A-17 — F-C2 IS APPLIED UNCONDITIONALLY IN S1 WHILE F-C1 CARRIES A GATE; AND THE CONTROL CLONES HAVE NO DISPOSITION IF F-C1 IS NOT APPLIED.
**Governs: S1 clone step 4 (Trap 10), S1 step 6, S2 Step 6's inverted branch, S2 Step 7.**

- **Trap 10 gets the same precondition as F-C1** — same ruling class, same date. Under A-03 both
  read RULED in the folder, so both proceed; but if a session finds either **not** recorded, ⛔ **do
  not restore `disableExits` on your own reading. Leave it, record it, ESCALATE: YES — a clone with
  EXIT OPTIONS ON and PT25 present is a live hazard, not a tidy-up.**
- **The bigger hole:** if F-C1 is not applied, S2 Step 6 calls the failed inverted check *"a known
  state, not a finding"* — which disclaims the generic `BOT STAYS OFF` branch and supplies no
  replacement, while Step 7 describes those same bots as *"deliberately Exit-Option-free"*, which
  they would not be.
  > ⛔ **IF F-C1 WAS NOT APPLIED, BOTH CONTROL CLONES STAY OFF. "Fails by construction" is not a
  > pass and it is not an exemption — the arm has no valid control until the removal lands.**

---

## ⛔ A-18 — S0 AND S1 MUST ATTEST ABOUT THE NINE. STEP 2c'S PRECONDITION IS OTHERWISE UNDECIDABLE.
**Governs: S0 and S1 close-out blocks; S2 Step 2c.**

Step 2c says *"confirm from their close-outs that they did"* — and neither close-out template has a
field for it, leaving S2 to choose between inferring compliance from silence (forbidden: inference
from absence is never evidence) and treating its own precondition as unverified.
> **ADD to S0's and S1's close-out hand-off:** ⛔ **ATTESTATION — state explicitly whether any of
> the nine leave-in-place bots was opened, edited, or had a toggle touched this session, BY NAME.
> "None" must be written; silence is not an attestation.** (The A-09 pre-observation screenshots
> are a read, and are declared here as such.)
> **ADD to S2 Step 2c:** ⛔ **IF EITHER CLOSE-OUT LACKS THE ATTESTATION → record
> `2c PRECONDITION UNVERIFIED`, run the observation anyway, and label the result NOT EVALUABLE in
> the Step 6a verdict.**

---

## ⛔ A-19 — S2 NEVER READS `state.md`, AND WRITES TO IT AT CLOSE-OUT.
**Governs: S2's READ FIRST list — and every prompt's.**

The one Opus session — the one that settles §1, rules the mechanism verdict, and appends that
verdict to `state.md` — does not have `state.md` on its read list. `CLAUDE.md` §6: *"`docs/state.md`
— the live facts. **Read first.**"* Without it S2 never sees the incident block and its branch, the
lockout block, the F-C1/F-C2 rulings, or the four-rulings block that closes two of the three items
its own gate A8 presents as open.
> **INSERT FIRST in S2's read list:** `docs/state.md` — **IN FULL**, and specifically the dated tail
> blocks: the 04:24 ET lockout, the F-C1/F-C2 rulings, the "four open items closed" ruling block,
> and the `OA REACTIVATED BUT ROSTER LOST` incident block with its branch. ⛔ **You do not write to
> a file you have not read.**
> **AND ADD `docs/rebuild-contingency-2026-08-07.md` TO ALL FOUR READ LISTS** — gate A0 needs it.

---

## ⛔ A-20 — GATE A4 SITS BETWEEN STEP 4 AND STEP 5, NOT AT THE CLOSE-OUT.
**Governs: §0.3 gate A4, S0's header line, S0's gate A4 block.**

S0's header says *"Everything after gate A4 is unattended-safe"*, but A4 is written as *"before you
write the close-out"* — which puts Step 5's destructive, spec-level `exits.profits` removal on a
live bot **before** Andy has accepted the roster the edit is being made against. In a
restored-account scenario that acceptance is the entire point.
> **A4 LANDS AT THE END OF STEP 4 (after Step 4b, A-07). No OA edit is made until it does. IF ANDY
> IS UNAVAILABLE, S0 STOPS AFTER STEP 4b with its roster and A-series report, and Steps 5–8 move to
> a follow-up session.** The header reads: *everything after gate A4 — which is reached at the end
> of Step 4b — is unattended-safe.*

---

## ⛔ A-21 — ESCALATION GOES TO ANDY, NOT TO A MODEL; AND "DIVERGES" NEEDS A DEFINITION.
**Governs: S0's header line, S0 Step 4's branches.**

S0's header (*"Escalate to Opus only if §1's roster or the A-series diverges"*), Step 4's generic
branch (*"ESCALATE TO ANDY: YES"*) and Step 4's A7 carve-out (*"report what you find, and GATE
it"*) give three destinations for one event.
> ⛔ **EVERY ESCALATION IN THIS SESSION GOES TO ANDY. You never request a model and never reason
> past a gate; Andy decides whether to re-open a thread on Opus (§0.2 step 6).**
> **"DIVERGES" MEANS, EXACTLY:** the `/bots` active count ≠ 41; **or** any name in Step 3's
> corrected list is absent, altered, or unexpectedly present; **or** any shared automation's
> bot-count ≠ its expected value; **or** any bot ID or `rid` ≠ its recorded value (A-01c); **or**
> any assert other than A7 fails. **A7 drift ALONE is not a divergence** — diff the tree and the
> payload field-by-field, report, and GATE it, per Step 4's own carve-out.

---

## ⛔ A-22 — THE BOOKMARKLET CAPTURE AND `Export Data` ARE ANDY'S HAND. NEW GATE A12.
**Governs: §0.3, S0 Step 3, S2 Step 5, S3.**

`CLAUDE.md` §2 assigns capture to Andy (*"Andy captures (bookmarklet on `/bots` + OA Export Data,
all groups)"*), no prompt says where the bookmarklet lives or what it emits, and standing fact 6
says JS dispatch is harness-blocked on this app. A session left to resolve that substitutes a page
scrape — which the same prompts rule inferior evidence, and which cannot satisfy the two-hop input
chain.
> **GATE A12 — ANDY RUNS THE BOOKMARKLET CAPTURE AND THE `Export Data` PULL** (⛔ **ALL GROUPS
> SELECTED**) and says where the file landed. Procedure: `oa-ops-runbook.md` §1.
> ⛔ **A `get_page_text` scrape is NOT a capture and must never be recorded as one.** If no capture
> file arrives, the roster check is ⬜ NOT EVALUABLE and the fleet stays OFF.
> ⚠️ Reading `a5.bots.bot` per bot is a different thing and remains yours — it is the hydrated
> client model, and it is what Step 4's asserts run against.

---

## ⛔ A-23 — S0 IS TOO LARGE FOR ONE CHAT, ON THE MODEL LEAST ABLE TO ABSORB IT.
**Governs: S0 as a whole; §3's model table.**

S0 as written is `/settings` + a 41-bot roster read + ~22 by-name confirmations + a 7-bot A-series
whose two-hop input-chain resolution alone is ~50 navigations + (now) Step 4b + a live two-action
edit + template / Notes / tag + four folder writes + close-out. **[Evidence: `docs/state.md`,
first-hand 2026-08-07 — *"The bot `…` menu (`showBotMenu`) stopped responding after ~40 good
clicks"*.]** The pack's own §0.1 item 12 warns that long OA chats saturate and start dropping
reads — and saturation here presents as **reads that return stale content while reporting
success**, which on S0 means a green `A2 7/7` on a bot whose page never loaded.
> ⛔ **S0 IS TWO CHATS. S0a = gate A0, Steps 1–4b, gate A4, close-out and hand-off. S0b = Steps 5–8
> in a FRESH chat against that close-out.** ⛔ **IF YOU HAVE PASSED ~40 CLICKS AND A READ LOOKS
> WRONG, STOP AT THE CURRENT PER-BOT BOUNDARY AND HAND OFF** — do not push to finish the arm.

---

## ⛔ A-24 — S2 STEP 0's "DO NOT PAY" CLAUSE IS SPENT, AND THE STEP AS WRITTEN DEADLOCKS.
**Governs: S2 Step 0.**

Step 0 says *"IF ANY ⛔ HARD BLOCKER BOX IS UNTICKED -> DO NOT PAY, DO NOT RE-ARM"* and then, in
the same block, lists three ⛔ boxes as known-unticked: **Template V2 on the pilot**, **C9**, and
**A7 wired into `daily.sh`**. Read literally, the session must halt before Step 0a — and one of the
two required actions refers to a payment gate A1 completed on 2026-08-07.
> ⚠️ **THE "DO NOT PAY" HALF IS SPENT — payment already happened. It is not an instruction.**
> ⛔ **THE THREE KNOWN-UNTICKED BOXES ARE ANDY'S RULING AT STEP 0, ONE AT A TIME, ASKED EXPLICITLY —
> not a silent proceed and not an automatic halt:** Template V2 is finished here **or the pilot
> stays OFF**; C9 is run **as a read** before switch-on **or the family stays OFF**; A7-unwired is
> reported and **Andy rules whether the family trades today with no nightly detector** (wiring it
> is Claude Code's lane). ⛔ **ANY OTHER unticked ⛔ box is an unqualified STOP.** ⛔ **Do not
> resolve any of them yourself.**

---

## ⛔ A-25 — PROJECT MEMORY IS CORROBORATION, NOT A PRECONDITION.
**Governs: all four READ FIRST lists.**

Every prompt lists project-memory keys under an absolute *"READ FIRST"*, and the STOP ladder makes
an unrun read `NOT EVALUABLE, never a pass` — so a fresh chat without project-memory access has an
unsatisfiable precondition on line one.
> ⚠️ **THE project-memory ENTRIES ARE CORROBORATION. Every fact they carry is restated inline in
> the prompt or is now recorded in `docs/state.md` (A-03). IF PROJECT MEMORY IS UNAVAILABLE: note
> it once and PROCEED on the folder plus the prompt.** ⛔ **IF A *FILE* ON THE LIST CANNOT BE READ,
> that is different — name it and STOP.**

---

## ⛔ A-27 — S0b's FOUR FINDINGS, RULED BY ANDY 2026-08-07. **THREE OF THEM GATE S2's OPENING.**
**Governs: S2's opening precondition, S2 Step 3, S2 Step 7, S2 Step 2b; and S0/S1's Step 6b.**
**Added 2026-08-07 at Andy's explicit ruling, after the S0b-RESUME session. Not a session's own
judgment — the four dispositions below are Andy's, verbatim in intent. Full evidence:
`session-log.md` "2026-08-07 (S0b-RESUME)" and `data/captures/2026-08-07-s0b/`.**

### (a) ⛔ S0b-1 — DO NOT FIX THE PILOT. AND THE CARRY-FORWARD IS THE IMPORTANT HALF.
**[Evidence: dated first-hand read 2026-08-07, `a5.bots.bot.disableExits` = 1 on
`QQQ-IC-0DTE-Fortress` (`BOTfw5TkkCRF2717857919585029021`), against that bot's own
`data/captures/2026-08-03-pilot/06-clone-final/oa_bot-settings_QQQ-IC-0DTE-Fortress-Clone_2026-08-04.txt`
which records verbatim: `EXIT OPTIONS ON (input[name=onoff].value="true")`.]**

**RULING: the pilot STAYS AS FOUND, EXIT OPTIONS OFF.** Arming it is **Day-0 Step 3** and it
belongs to **S2**. It is recorded as a **second witness** on the `disableExits`-reset question —
**8 of 8 bots examined** now point the same way. **PR-03 stays UNSIGNABLE; that is expected and
blocks nothing on the current path.**

> ### ⛔⛔ CARRY FORWARD, PROMINENTLY — THIS IS THE ONE THAT CAN COST A DAY-0.
> **IF THE RESTORE RESET `disableExits`, IT MAY RESET AGAIN.** Therefore **the seven greenfield
> bots S0a armed CANNOT BE ASSUMED STILL ARMED.**
> ⛔ **TOGGLE STATE MUST BE RE-READ FIRST-HAND IMMEDIATELY BEFORE STEP 7, ON EVERY BOT, AND NEVER
> INHERITED** — not from S0a's close-out, not from S0b's, not from `bots_config_v2.csv`, not from
> this pack. A recorded ON is a historical fact about the moment it was read, not a property of
> the bot. Re-read it, then switch AUTOMATIONS on.
> ⚠️ **AND S2 STILL DOES NOT RE-DO STEP 3 ON THE SEVEN** (the S0a correction in `state.md`
> stands). **Re-reading is not re-doing.** If the re-read comes back OFF, that is a NEW finding —
> record it, escalate, and do not silently re-arm inside Step 7.
> Cheapest instrument, first-hand 2026-08-07: the `/bots` list carries both toggles per row on
> `i.sticon`'s `title` attribute — one page read covers all 41 bots. See (d).

### (b) ⛔ S0b-2 — STEP 6b CANNOT PASS AS WRITTEN. RECORD IT OPEN; **DO NOT RETRY IT.**
**RULING: OPEN.** The PR-01 Notes on the clone are **NOT byte-exact** to
`pre-registration-ledger.md` §4, because the **bot-page** Notes editor does **not** perform the
decode pass the **template** Notes editor does — so §4.0 item 2's double-escape counter backfires
there, and the writing session worked around it by dropping the angle-bracketed placeholders.
**Two editors, two behaviours; the §4.0 trap text is CORRECT for templates and is NOT amended.**
⛔ **DO NOT RETRY THE BYTE-EXACT WRITE.** The Notes are a **record artifact** and **nothing in the
Day-0 sequence reads them.** Step 6b's byte-exact clause is unsatisfiable on this surface; record
NOT-BYTE-EXACT-BY-KNOWN-CAUSE and move on. Settling the mechanism needs a deliberate write test on
a throwaway bot — a decision, not a Day-0 action.

### (c) ⛔ S0b / STEP 4b — **GATED AND DEFERRED. IT BLOCKS S2's OPENING, NOT S0b's CLOSE.**
**RULING: this is a NAMED PRECONDITION ON S2 OPENING, and NO OPTION IS CHOSEN.**

⛔ **S2 DOES NOT START UNTIL ANDY HAS RULED THIS.** A-07 makes an **ESTABLISHED** config-capture
hash a precondition for signing at **Step 2b**. First-hand inventory of `data/captures/`,
2026-08-07: **for 12 of the 14 bots in A-07's scope there is NO per-bot capture file on disk at
all** — `IC-SPX-FastPT25-S2-130PM`, `QQQ-IC-0DTE-Fortress-NoPT50` and **all nine leave-in-place
bots** have never been captured per bot. **This is a structural gap in the repository, not a task
a longer session closes.** Current dispositions: PR-01 clone **ESTABLISHED** · its archived
original **ESTABLISHED** · the pilot **NOT ESTABLISHED** (a) · **the other twelve ⬜ NOT
EVALUABLE — never a pass.**

**THE THREE OPTIONS, STATED, NONE CHOSEN — ANDY PICKS:**
1. **CAPTURE-NOW-AS-BASELINE.** Take a fresh per-bot capture of the twelve and treat it as the
   baseline. ⚠️ Honest cost: this **establishes nothing about the past.** A first capture taken
   after the restore cannot distinguish a faithfully restored bot from a rolled-back one — it
   only makes future drift detectable. It buys forward coverage, not retrospective assurance.
   ⛔ It also requires opening the nine, which **spends Step 2c** unless taken as a pure read.
2. **AMEND A-07's SCOPE** so an ESTABLISHED hash is required only where a pre-restore baseline
   exists, with the twelve carried explicitly as ⬜ NOT EVALUABLE rather than blocking.
3. **LEAVE THEM OFF PERMANENTLY.** The literal reading of A-07 as written: no ESTABLISHED hash,
   no signature at Step 2b, bot stays OFF. Applies to all nine leave-in-place bots.

**TWO CORRECTIONS THAT TRAVEL WITH THIS RULING, BOTH RECORDED:**
- ⛔ **A-07's scope is FOURTEEN bots, not thirteen.** The pack and S0a's close-out both say
  "13 non-greenfield bots". The arithmetic: **41 active = 7 greenfield + 5 named +
  9 leave-in-place + 20 Group-A**, and A-07's named list is 5 + 9 = **14**.
- ⛔ **THE 20 GROUP-A BOTS ARE IN NO POST-RESTORE CONFIG CHECK ANYWHERE IN THIS PACK.** They are
  still active only because the ~23 archives remain queued for Andy's hand. Named here so the
  gap is on the record rather than discovered later.

### (d) 📝 S0b-3 — A BOOKMARKLET DEFECT, WITH THE FIX IDENTIFIED. **CLAUDE CODE'S LANE.**
**RULING: recorded as a defect in the capture instrument, not in the page.**
`oa-ops-runbook.md` §1.5 calls the missing `AUTOS`/`EXITS` columns "the highest-value miss" and
§1.6 concludes toggle state "does not survive text capture". **Both are CORRECT and NEITHER is
amended.** The cause, first-hand 2026-08-07: the `/bots` rows emit **18** values, not 20, because
the two toggle cells are **icons with no text node** — but the state **is** in the DOM, on
`i.sticon`'s **`title`** attribute ("Scheduled automations are off" / "Exit Options for positions
managed by this bot are on").
**FIX, IDENTIFIED: the bookmarklet must read the icon `title` attribute, not `innerText`.**
⛔ **Implementing it is Claude Code's lane** (`CLAUDE.md` §7), not a Day-0 session's. Until it
lands, toggle state comes from a separate DOM read — the method and a full 41-bot table are in
`data/captures/2026-08-07-s0b/toggle-state-all-41-2026-08-07.tsv`.

---

*Amendments A-01…A-25 written 2026-08-07 (evening) under `CLAUDE.md` §5's
evidence-backed-correction rule: each one either corrects a claim falsified by a dated first-hand
read of the folder, or adds a gate/branch where the review found none. **A-26 added the same
evening at Andy's instruction** (the `a_series.py` runner). **No decision was ruled here** — A-02,
A-11, A-12, A-24 and gate A8's surviving item are routed to Andy. **Andy may reject any of them at
commit review.***

---

# §0 · THE STANDING PREAMBLE

Every prompt below already embeds this block. It is repeated here once so it can be maintained in
one place; if you edit it, edit it in all four prompts too.

## 0.1 Standing facts — true in every Day-0 session

1. ⛔ **NEVER RUN GIT. In any form, including `git status`.** The device bridge cannot unlink files,
   so a git run from this side strands `.git/index.lock` and Andy has to remove it by hand
   (established 2026-07-31; two slips in one night 2026-08-06, different sessions). File
   verification is **`device_bash` sha256 plus a single-match grep of the new text** — never the
   write tool's response, never a stage-back read (`CLAUDE.md` §9.1a; stage-backs serve stale
   content under fresh metadata, reproduced 2026-07-31). **Andy runs every commit.**

2. ⛔ **SESSIONS START LOGGED OUT.** The OA login page read **"Account disabled, please purchase a
   plan"** at ~04:20 ET 2026-08-07. This **SUPERSEDES** the standing "the account-inactive banner is
   cosmetic, not a save-blocker" finding — that finding was TRUE through ~04:00 08-07 (every write
   server-verified through hard reloads) and then OA escalated from *inactive* to *fully disabled*.
   Do not expect a live session. Do not log in and poke. **Purchasing IS Day-0.**

3. ⛔ **NOTES: DOUBLE-ESCAPE FROM THE FIRST WRITE.** OA's sanitizer **decodes entities, then strips
   unknown tags** — `&lt;capture&gt;` becomes `<capture>` and is then removed as markup, and the
   rendered panel looks correct. Write `&amp;lt;` so one decode pass leaves `&lt;` intact. **Verify
   by byte-exact length-and-content compare against the source, never by reading the panel.**
   Reproduced and defeated on PR-14 (two lost writes, 2324/2339 both times).

4. ⛔ **DECISION-NODE INNER-ATTACH: use `NOT`, never a rebuild.** OA's decision editor has **no
   move-node control** (its menu is Settings / Precede with / Copy Action / Edit Caption / Edit
   Notes / Delete). To move an action onto the other branch you would have to delete and rebuild the
   whole action *including its `exits` bundle*. **Do not.** `NOT` is first-class on the criterion
   toolbar (`Create Group | NOT | 🗑`) and stores as `not:true` on the criterion — logically
   identical, action node left byte-untouched. This is how PR-01's re-entry gate was built
   (`postagtoday{oc:opened, not:true, tag:"put|call side"}`, action left on YES).

5. ⛔ **PICKER NO-OP — force with a two-step.** Clicking a picker's already-displayed value is a
   **no-op**; the field never materializes. Force it with a two-step through a different value and
   back (e.g. `exitrate`: Instant `0` → save → Every 1m `1` → save). **Verify the STORED model
   field, not the rendering.** Record the intermediate state rather than hiding it, and only do this
   while the bot is inert (AUTOMATIONS OFF, no positions).

6. **Clicking, on this app.** Element-**ref** clicks silently no-op and the tool still reports
   success. JS event dispatch (`pointerdown→…→click`) is blocked by the Cowork harness classifier on
   this app. **The path that works from Cowork: compute the target from the DOM.**
   `scale = screenshotWidth / window.innerWidth`; click at `rect.centre × scale`.
   ⚠️ **Never carry a coordinate across a window resize** — the ratio changed mid-session on
   2026-08-07 (2560×1314/1548×795 → 3456×1314/1568×596) and silently invalidated every in-flight
   coordinate. Re-derive the scale after any resize.

7. **Other app traps, all first-hand.** `overlay.innerText` goes stale while a drawer animates —
   screenshot before concluding a click failed. The title editor commits on **blur**, not Enter.
   `Runtime.evaluate` times out at ~45s **with the work COMMITTED** — re-read state, **never re-fire
   the action**. `form_input` over `computer.type`; re-read `.value` after every text entry. Tag
   widgets need per-character `input` events — click the suggestion item. OA lowercases tags and
   maps non-alphanumerics to spaces: `PR-01` stores as `pr 01`. Tags live on the bot's **Dashboard**
   tab, not Settings. `a5.bots.bot` is the hydrated client model and is better Layer-1 evidence than
   any DOM scrape.

8. ⛔ **`archiveBot` IS ANDY'S HAND. 3-for-3 failed from this side** (2026-08-04, and again
   2026-08-07 as `showBotMenu`). **Three attempts, then stop.** ⛔ **Never fall back to raw
   coordinates on that menu** — `Delete` sits ~29px below `Archive` and a mis-landed click is
   unrecoverable. Renames DO commit; the rename is what frees the production name, so the archive is
   hygiene, not a blocker.

9. **Two-layer OA edit proof, every edit, no substitutions** (`CLAUDE.md` §5, `oa-ops-runbook.md`
   §4). **Layer 1** — re-observe the changed value from OA itself after a hard reload (screenshot for
   toggle/UI state, fresh capture/model read for text-capturable fields). **Layer 2** — the first NEW
   position's **Trades list**. ⛔ **The Exit Options panel is NEVER evidence.** A save confirmation,
   a toast, or a tool-success message is never either layer.

10. **Decisions stay gated; evidence-backed corrections of falsified claims may be applied
    directly** — the five-condition test in `CLAUDE.md` §5. **When it is ambiguous, it is gated.**
    Inference from absence is never an evidence-backed correction.

11. **Close out after each piece of work, not once at the end** (`CLAUDE.md` §9.1): append
    `session-log.md` (+ `state.md` if a stated fact changed) → update the `bot-fleet-migration`
    tracker via `update_artifact` → say "ready to commit" with the changed-files list. **The tracker
    verifies by Andy's visual confirmation and the close-out is not complete without it.**

12. **Close the chat at a clean boundary.** Long OA build chats saturate and start dropping reads.
    Stop at a per-bot / per-step boundary and hand to the next session against a written close-out.

## 0.2 The STOP ladder

Applies to every action in every session. It is what makes a Sonnet session safe.

```
1. Do it the documented way.
2. Failed? Try the ONE documented alternative. (Never a third invented method.)
3. Failed again? THIRD attempt maximum — then STOP.
     - Do NOT force it.
     - Do NOT fall back to raw coordinates.
     - Do NOT improvise a remedy. build-plan.md is under decision freeze
       and Day-0 is not a build day.
4. Record what was attempted, verbatim, and take the runbook's own branch:
     "bot stays OFF"   -> that bot does not trade today; the fleet proceeds.
     "fleet stays OFF" -> nothing else is switched on today; stop the sequence.
     unrun check       -> NOT EVALUABLE. Written down by name. NEVER a pass.
5. Ambiguous / two frozen decisions conflict / it would change a decision
   -> GATED. Escalate to Andy. Stop that thread; the others proceed.
6. MODEL ESCALATION: a Sonnet session that reaches step 5, or that finds a
   documented branch does not fit what it is actually seeing, STOPS and hands
   to Andy. Andy re-opens it in an Opus session. A Sonnet session never
   reasons its way past a gate.
```

> ⛔ **AMENDED 2026-08-07 (A-14) — "no coordinate fallback" does NOT ban the only click method that
> works.** Step 3 above says *raw* coordinates, and it means it. The inline copies of this ladder in
> S0, S1 and S3 dropped the word. **DOM-COMPUTED coordinates (`scale = screenshotWidth /
> window.innerWidth`, click at `rect.centre × scale`, re-derived after any resize) ARE the
> documented method (standing fact 6), not a fallback — use them freely.** The ONE documented
> alternative for a failed click is: fresh screenshot → re-derive the scale → re-click once.
> ⛔ **The RAW/eyeballed-coordinate ban is absolute on the bot `…` menu** (fact 8).
>
> ⛔ **AMENDED 2026-08-07 (A-21) — every escalation goes to ANDY, not to a model.** A session never
> requests Opus; it stops and hands to Andy, and Andy decides whether to re-open on Opus.

## 0.3 Andy's steps — the gates that are HIS hands, in order

> ⛔ **AMENDED 2026-08-07 — two gates added and two corrected. A0 and A12 are new; A1 is spent; A3,
> A4 and A8 changed. See §0.0.**

| # | Gate | Session | Why it cannot be Claude's |
|---|---|---|---|
| **A0** | ⛔ **RULE THE RESTORE STATE** — 0 of 41 bots survived reactivation (A-01). Andy confirms which of the three branches the account is in. | **before S0 Step 1, and before S1/S2/S3** | The roster is the premise of the whole pack; branch 3 (partial/altered/moving) is never a session's call. |
| A1 | ~~**Log in and purchase the plan**~~ ✅ **SPENT — DONE 2026-08-07 ~12:06 ET.** Andy confirms the timestamp in one line; **`LEDGER_START` becomes a separate gated question** (A-02). | S0 | Payment. Also the only way in — the account is disabled. |
| **A12** | **Run the bookmarklet capture and the `Export Data` pull, ALL GROUPS SELECTED** (A-22) | S0, S2, S3 | `CLAUDE.md` §2 assigns capture to Andy; JS dispatch is harness-blocked on this app, and a page scrape is not a capture. |
| A2 | **Acknowledge the pay-before-`itmlive` order** (S0 §2) | S0 | Runbook §4 says do not reorder; the lockout forced it. One line. |
| A3 | **Rule / re-confirm F-C1 and F-C2** if not already recorded in the folder | S0 | The rulings exist only in project memory (see §1.3). |
| A4 | **Declare the roster and A-series verdict accepted** | S0 | Same class as "Andy declares the pilot clean" (runbook §3 Step A). |
| A5 | **The ~23 archive clicks** (20 Group-A + 3 clone originals) | S3 | `archiveBot` 3-for-3 failed from this side. |
| A6 | **Ride-or-close decision on the 5 open mirror positions — drafted, SIGNED, and EXECUTED** | S2 Step 2 | Capital decision. Go-live authority is Andy's. |
| A7 | **Sign every pre-registration entry** (20 plan bots + the ride-or-close entry) | S2 Step 2b | "Andy signs and dates. Only then may the bot be switched ON." |
| A8 | **Rule the three open signature items**: PR-16 T1 δ/p/floor (G-12b), PR-18 "Breakeven" naming, G-1′ | S2 Step 2b | Unfilled field ⇒ unsigned entry (ledger §7 item 2). |
| A9 | **Run `bash scripts/daily.sh` at n=0 from his own terminal** | S0 pre-flight | `tape.py` needs network; `device_bash` has none. |
| A10 | **Visually confirm the tracker artifact** | every close-out | §9.1a — the tracker is the one dashboard Andy reads. |
| A11 | **Run every commit** | every close-out | The bridge cannot unlink; git from this side strands lock files. |

---

# §1 · PRE-FLIGHT STATE — what is true as of 2026-08-07

Read fresh from the folder this session. Every prompt below repeats the parts it needs.

## 1.1 The fleet, as built

> ⛔ **SUPERSEDED-IN-PART 2026-08-07 ~12:06 ET — READ §0.0 A-01 BEFORE USING ANY NUMBER BELOW.**
> `/bots` read **"0 active bots • 50 left in your plan"** after the plan was purchased. Templates,
> the Automation Library and the Bot Archive survived; every active bot did not. Restore was
> promised by OA for Monday. **The arithmetic below is correct for a RESTORED account and wrong for
> a rebuilt or partially restored one.** Gate A0 decides which world you are in.

**Expected roster at reactivation: 41 active bots · 9 slots left of the Pro 50.**
Arithmetic: 35 (2026-07-30 capture) − 2 deleted (sweep, 08-06 night) = 33; + 7 greenfield = 40;
+ 1 PR-01 clone = **41**. The `/bots` footer read `40 active bots • 10 left` immediately before the
PR-01 clone. The PR-01 original was **renamed, not archived** — it still counts.

**The greenfield family — COMPLETE, 7 of 7, server-verified, nothing ON.**
All seven: Paper · `seed 2500` · limits 2/2 · scan 1m/1m · Day Trading Allowed · Group `IC` ·
`status "off"` (AUTOMATIONS OFF) · `disableExits 0` (EXIT OPTIONS ON) · symbols empty · both bot
inputs bound, non-empty and EQUAL · three shared automations attached by `rid` (**attach, not
copy** — the Library reads "7 bots" on each) · Notes byte-exact · Template V1 each.

| Arm | PR | Bot ID | Mechanic |
|---|---|---|---|
| `GF-QQQ-IC-Ride` | PR-14 | `BOTfw5TkkCRF4417860701930934951` | control, base only, `mechanics = {}` |
| `-PT50` | PR-15 | `…4417860738688735152` | `profits 0.5` + `smprofits speedy` |
| `-Trail` | PR-16 | `…4417860754672239833` | `tstop {target:40, trail:15}` + `smtstop normal` |
| `-Touch0` | PR-17 | `…4417860760818962144` | `touch {usd, 0}` + `smtouch normal` |
| `-SL100` | PR-18 | `…4417860767788927225` | `stoploss 1` + `smstoploss normal` |
| `-SL200` | PR-19 | `…4417860785000861357` | `stoploss 2` + `smstoploss normal` |
| `-Canary` | PR-20 | `…4417860774419022836` | `profits 0.05` + `smprofits speedy` |

Shared objects and A7 baselines (in `data/bots_config_v2.csv`):
`GF-ScannerA-PutSpread` **`3308ce8b476d2bd090d9519b445748fc4c0d0fdbe71861c83a249729b1a5a30a`** @ v9
(A7-DRIFT-1 ruled ADOPT 2026-08-07, applied) · `GF-ScannerB-CallSpread`
`bb4ba866a13e7ecd682f7bda9a19011003e9e3ef73fffd0fb64a80a4cd0eb32e` @ v2 ·
`GF-Backstop-1552-FlatClose` `116069bddf8b8c9e58bd8f28313c2ad95726fa3f7205df4dfde82de7a3e2e5b5` @ v1.
Library holds exactly **4** objects: those three (7 bots each) + `Defang-Mon-S2-StrikeTouch` (2 bots).

**Asserts at n=7, all runnable ones green** —
`data/captures/2026-08-07-greenfield/ASSERTS-A1-A9-and-capture-diff.txt`:
**A1 21/21** (amended rule) · **A2 7/7** (12 of 12 non-bundle fields equal) · **A3 7/7** ·
**A7 3/3** · **A8 7/7** · **A9 7/7**. A4 struck moot · **A5 · A4b · A6 not runnable pre-Day-0**
(A5 needs the account fields re-read; A4b and A6 need positions).

**Clones — 2 of 4 done.** Pilot `QQQ-IC-0DTE-Fortress` (PR-03, 08-03/04, declared clean by Andy
2026-08-06). `IC-SPX-FastPT25-S2` (PR-01, 08-07) — clone `BOTfw5TkkCRF4417860821948715488`, n=0,
AUTOMATIONS OFF, EXIT OPTIONS OFF, group `IC-Focus`, tags `live candidate,focus ic`, allocation
$50,000, limits 10/10; original renamed `IC-SPX-FastPT25-S2-ARCHIVED-2026-08-07`
(`BOTfw5TkkCRF1217757048550308561`) and verified byte-identical to its Step-0 baseline.
**PR-02 (`-130PM`) and PR-04 (`-NoPT50`) were never started — both originals untouched and
un-renamed.**

## 1.2 What is NOT done — the Day-0 work list

**⛔ HARD BLOCKERS still unticked on the runbook's Pre-Day-0 checklist:**

- `itmlive` = `market` (runbook §4 Step 0a). `itmpaper` is already `market` — **do not re-set it**.
- `LEDGER_START` set in `build_ledger.py` and verified by an n=0 run. Currently
  `data/ledger_meta.json` reads `"ledger_start": "2099-01-01"` — a refuse-everything sentinel, which
  is correct pre-Day-0, not a value to keep.
- **Template V2 on the pilot** (15:50 Expiration exit re-priced OFF Market → SmartPricing internal
  value `speedy`, **NOT `fast`**; the 15:52 backstop KEEPS Market) **with its AMENDED PR-03 signed.**
  ⚠️ Without V2 the three 15:50–15:52 mechanics are three Market orders in two minutes with only
  memo strings between them.
- `daily.sh` n=0 dry run passing end to end.
- Sizing written down: 1 lot experiments, ≈$5K risk/position CANDIDATE+, identical across arms.
- Ride-or-close prepared, **signed, and ready to EXECUTE** on the 5 open mirror positions.
- Every pre-registration entry SIGNED, including the nine untouched.
- Phase 0 `C9` (firing semantics — re-scoped to a Day-0 pre-switch-on read) and the **A7 baselines
  wired into `daily.sh`**. ⚠️ The baselines ARE recorded in `bots_config_v2.csv`; **A7 is not wired
  into `daily.sh`** — `daily.sh`'s eight stages carry `execution_audit.py` as the detector and no
  A-series runner. The A-series is currently run by hand. That is an open Step-4(b) gate.
  `C0c · C2 · C7 · C8` are **CLOSED** (decision card 2026-08-06 late-night Phase 0 closure).
- ✅ `data/raw/` and `data/brief/` are **empty** — the pre-cutover-files box is satisfiable by a read.
  ⛔ **CORRECTED 2026-08-07/08 (Andy's rulings). Original left standing.** **NEITHER DIRECTORY IS
  EMPTY ANY MORE, AND NEITHER SHOULD BE.** `data/raw/` holds the filed Export Data pull
  `2026-08-07.csv` (⛔ **DO-NOT-DELETE** — it is stage 1's input); `data/brief/` holds
  `2026-08-08_tape.json`, a **gate-A9 test artifact** written on a **Saturday** with an empty
  payload — correct degradation, labelled in place, **not a real brief**. **A populated
  `data/brief/` is working output, not contamination.**
  **The box is NOT satisfiable by a directory listing, a file move, or a deletion.** It is
  satisfied by `build_ledger.py`'s own counts: **`export_rows` 1,386 → `post_cutover` 0 ·
  `straddler` 0 · `pre_cutover` 1,386 discarded · n=0**, verified first-hand 2026-08-07.
  Matching amendment: `reactivation-runbook.md` §4 checklist. See S0's Step 8.
- ✅ `data/mirror_baseline.csv` written 2026-08-04, 10 rows / 174 positions. **It is an anchor — do
  not recompute it, do not pass `--force`.**

**Build-side leftovers:**

- PR-01 clone: **Template V1 + PR-01 Notes + `pr 01` tag** (record artifacts; nothing depends on
  them) — not done, `showBotMenu` went dead.
- **PR-02 (`-130PM`) and PR-04 (`-NoPT50`) clones** — never started.
- **The ~23 archives** (20 Group-A + 3 clone originals) — **Andy's hand.**
- The pilot's **Bot Group** (runbook §3 Step A, audit F-21).

**Open observations queued to Day-0, each with a decision tree already written:**
Step 2c no-touch · Step 5a **D3 DST** (`ntime=1552` vs 16:52 ET under EDT — reproduces on all six
arms, `startDate 2026-08-07T20:52:00.000Z`) · Step 6 the 15:50 attribution · Step 6a **D4 mechanism
verdict** · Step 6b **C10 `dstop` unit** (blocks ARM-B1) · Tier-2 **§9 #5**.
**Any one left unread at close-out is reported OPEN, never passed.**

## 1.3 ⛔ THREE DIVERGENCES THIS SESSION FOUND — read before S0

> ⛔ **CORRECTED 2026-08-07 (evening) — A-03. TWO OF THE THREE ARE FALSIFIED. Original text left
> standing below.** `docs/state.md` carries the 04:24 ET lockout block, and both
> **"F-C1 — RULED 2026-08-07 (Andy, first-hand): REMOVE"** and **"F-C2 — RULED 2026-08-07 (Andy,
> first-hand): AUTHORIZED AS TRAP 10"**; `docs/session-log.md` carries the same F-C1 banner. They
> were already in the folder when this pack was written. **(a) and (b) are wrong as stated. Only
> (c) survives.** Gate A3 becomes VERIFY, not re-ask; S0 Step 7(a)/(b) become verify-and-report and
> must NOT write a second dated banner. ⚠️ **What IS still outstanding is the APPLICATION of F-C1 —
> `state.md`: *"Not yet applied to either bot"* — so S0 Step 5 and S1 step 6 stand unchanged.**

**(a) The lockout is NOT in `docs/state.md` or `docs/session-log.md`.** It exists only in project
memory (`greenfield-build-status`). The last `state.md` block is the 08-07 morning clone sweep and
the last `session-log.md` entry is the same session — both written ~06:20, both silent on the
~04:20 disable. **S0 records it.**

**(b) The F-C1 and F-C2 rulings are NOT in the folder either.** `state.md` line 1495 and
`session-log.md` line 5198 both still read **GATED**. Project memory `greenfield-build-status`
records them as ruled — **F-C1: REMOVE PT25 from the clones' Open actions** (the controls are
genuinely Exit-Option-free) and **F-C2: Trap 10 authorized** — but a memory note is not the folder.
⛔ **S0 opens with Andy re-confirming both in one line before any edit is made** (gate A3), then
records them in `state.md` + `session-log.md` as ruled-and-applied. Two documents vouching for each
other is a citation loop; a ruling that lives only in memory is worse.

**(c) Uncommitted work is sitting in the tree.** `docs/decision-card-2026-08-06.md` is modified and
`data/captures/2026-08-06-gfam/GF-Backstop-1552-FlatClose.txt` is untracked. **Andy commits before
Day-0 starts** — an untracked folder cannot be diffed or reverted, and Day-0 is the worst day to
discover that.

---

# §2 · SESSION PROMPTS

Run in order. **S0 → S1 → S2 → S3.** Each hands off to the next in writing.

---

## S0 — REACTIVATION OPENING

**Model: Sonnet.** Escalate to Opus only if §1's roster or the A-series diverges — that is a STOP,
not a judgment call, and the judgment about what to do next is Andy's.
**Andy attended: yes, for gates A1–A4.** Everything after gate A4 is unattended-safe.

```text
You are working in bot-fleet-v2 (~/bot-fleet-v2 via the device bridge). TODAY IS DAY-0: the OA
account is being reactivated. This is the OPENING session. Its job is to establish that the fleet
came out of the lockout exactly as it went in, then finish the two record artifacts the lockout
interrupted. It does NOT run the Day-0 sequence — that is a later session.

⛔ AMENDED 2026-08-07 (evening). READ `docs/day0-session-pack-2026-08-07.md` §0.0 — THE AMENDMENTS —
BEFORE ANYTHING ELSE IN THIS PROMPT. Where §0.0 and the text below conflict, §0.0 WINS. The ones
that change this session: A-01 (gate A0 — THE ROSTER WAS LOST; three branches, not two) · A-02
(the plan is ALREADY PAID — do not ask) · A-03 (F-C1/F-C2 are RULED IN THE FOLDER — verify, do not
re-ask) · A-05 (one name in Step 3's list is archived and will fire a false STOP) · A-07 (new Step
4b) · A-09 (take the 2c toggle screenshots FIRST) · A-13 · A-15 · A-20 · A-21 · A-22 · A-23.

READ FIRST, FRESH, IN THIS ORDER (never from memory of a prior session):
  docs/day0-session-pack-2026-08-07.md  ⛔ §0.0 FIRST, then §0, §1  (standing facts and pre-flight)
  docs/state.md                          ⛔ IN FULL. The dated tail blocks are load-bearing: the
                                         04:24 ET lockout · the F-C1/F-C2 RULINGS · the "four open
                                         items closed" block · ⛔ the `OA REACTIVATED BUT ROSTER
                                         LOST` incident block and its branch (gate A0)
  docs/rebuild-contingency-2026-08-07.md ⛔ gate A0 branch 2/3 routes here; it has its own
                                         DO-NOT-START gate (§4)
  docs/greenfield-family-spec.md         §8.3 (the A-series — A1's AMENDED text is authoritative)
                                         and §9 (each arm's pre-registered set — A3's comparand)
  docs/pre-registration-ledger.md        §4 — the PR-01 entry. ⛔ The Notes-block SOURCE TEXT for
                                         Step 6. There is no other; do not compose one.
  docs/session-log.md                    the last two entries
  docs/reactivation-runbook.md           §2 (the per-clone checklist), §3 Step B, §4 Steps 0, 0a, 1
  docs/oa-ops-runbook.md                 §1 (capture ritual), §4 (edit verification), §5 (traps)
  docs/build-plan.md                     §2B (the four clones' specs — FROZEN)
  data/bots_config_v2.csv                the config record — 3 shared automations + 8 bots
  data/captures/2026-08-07-greenfield/ASSERTS-A1-A9-and-capture-diff.txt
  project memory: greenfield-build-status, clone-sweep-status

=== STANDING FACTS — TRUE ALL SESSION ===
1. NEVER RUN GIT, in any form, INCLUDING `git status`. The bridge cannot unlink, so git from this
   side strands .git/index.lock and Andy removes it by hand. Verify files by direct `device_bash`
   sha256 + a single-match grep of the new text. Never the write tool's response, never a
   stage-back read (stage-backs serve stale content under fresh metadata). ANDY RUNS EVERY COMMIT.
2. YOU START LOGGED OUT. At ~04:20 ET 2026-08-07 the OA login page read "Account disabled, please
   purchase a plan". This SUPERSEDES the old "the inactive banner is cosmetic" finding — that was
   true through ~04:00 08-07, then OA escalated from inactive to fully disabled.
3. NOTES: DOUBLE-ESCAPE FROM THE FIRST WRITE. OA's sanitizer decodes entities THEN strips unknown
   tags, so `&lt;capture&gt;` silently vanishes and the rendered panel still looks right. Write
   `&amp;lt;`. Verify by byte-exact length-and-content compare against the source, never by
   reading the panel.
4. DECISION NODES: use the `NOT` operator, never a rebuild. OA has no move-node control; moving an
   action to the other branch means deleting and rebuilding it including its `exits` bundle. `NOT`
   is first-class on the criterion toolbar and stores as `not:true`.
5. PICKERS NO-OP on the already-displayed value. Force with a two-step through another value and
   back. Verify the STORED model field, not the rendering. Only while the bot is inert.
6. CLICKING: element-ref clicks silently no-op and the tool still reports success; JS event
   dispatch is blocked by the harness on this app. Compute from the DOM:
   scale = screenshotWidth / window.innerWidth, click at rect.centre × scale.
   NEVER carry a coordinate across a window resize — re-derive the scale.
7. `Runtime.evaluate` times out at ~45s WITH THE WORK COMMITTED — re-read state, never re-fire.
   Title fields commit on BLUR, not Enter. `overlay.innerText` goes stale mid-animation —
   screenshot before concluding a click failed. Prefer `form_input` and re-read `.value`.
   Tags: click the suggestion item; OA stores `PR-01` as `pr 01`; tags live on the DASHBOARD tab.
   `a5.bots.bot` is the hydrated client model and beats any DOM scrape as Layer-1 evidence.
8. `archiveBot` / `showBotMenu` are ANDY'S HAND — 3-for-3 failed from this side. Three attempts,
   then STOP. NEVER fall back to raw coordinates on that menu: `Delete` sits ~29px below `Archive`.
9. TWO-LAYER EDIT PROOF, no substitutions. Layer 1 = re-observe the changed value from OA after a
   HARD RELOAD. Layer 2 = the first NEW position's Trades list. The Exit Options panel is NEVER
   evidence. A save confirmation proves nothing.
10. Decisions stay gated; evidence-backed corrections of falsified claims may be applied directly
    (CLAUDE.md §5's five conditions). WHEN IT IS AMBIGUOUS, IT IS GATED.

=== THE STOP LADDER ===
Documented method -> ONE documented alternative -> third attempt max -> STOP. Do not force, do not
fall back to coordinates, do not improvise a remedy. Record verbatim what was attempted and take
the runbook's own branch: "bot stays OFF" (fleet proceeds) / "fleet stays OFF" (stop the sequence)
/ an unrun check is NOT EVALUABLE and is never a pass. Ambiguous or decision-touching -> GATED,
escalate to Andy, stop that thread. You do not reason past a gate; you stop and hand it to Andy.

=== ⛔ ANDY'S STEPS — HIS HANDS, NOT YOURS ===
A1. ANDY LOGS IN AND PURCHASES THE PLAN. Ask for it, then WAIT. Record the exact payment timestamp
    he reports (date + time + timezone) — that timestamp is LEDGER_START and a later session sets
    it. Do not attempt to log in or pay.
A2. ANDY ACKNOWLEDGES A SEQUENCING NOTE, in one line. The runbook puts Step 0a (`itmlive` =
    `market`, "HARD GATE, before any capital is live") BEFORE Step 1 (pay), and §4 says do not
    reorder the steps. THE LOCKOUT MAKES THAT ORDER IMPOSSIBLE — `/settings` is unreachable until
    the plan is purchased. The gate's INTENT is preserved: no capital is live until Step 7 turns
    AUTOMATIONS on, and nothing is switched on in this session or the next. State this to Andy
    plainly and get an explicit acknowledgment before you set `itmlive`. DO NOT proceed on your own
    reading of it. If he declines, `itmlive` stays `auto`, you record it, and FLEET STAYS OFF.
A3. ANDY RE-CONFIRMS F-C1 AND F-C2 IN ONE LINE. Project memory records them as ruled — F-C1: REMOVE
    `exits.profits` (PT25) from BOTH Open Position actions of the champion pair, per build-plan.md
    §2B; F-C2: authorize `disableExits` resets 1→0 on clone as oa-ops-runbook.md §5 Trap 10 — but
    docs/state.md and docs/session-log.md BOTH STILL READ "GATED". A ruling that lives only in
    memory is not a ruling in the folder. Get the one-line re-confirmation, then apply and record.
    IF HE DOES NOT RE-CONFIRM: change nothing, record it as still GATED, and PR-01 and PR-02 keep
    their INVERTED-check failure-by-construction. Their Day-0 verification stays blocked.
A4. ANDY DECLARES THE ROSTER + A-SERIES VERDICT ACCEPTED, before you write the close-out. Same
    class as "Andy declares the pilot clean" — you do not self-certify it.

=== YOUR WORK, IN ORDER ===

⛔ STEP 0 — GATE A0 (AMENDMENT A-01). BEFORE STEP 1. Read state.md's incident block and
rebuild-contingency; open /bots with ALL FILTERS CLEARED and read the footer. BRANCH 1 clean
restore (41 · 9 left · names match · IDs and rids match) -> continue. BRANCH 2 nothing came back ->
STOP, no OA write, hand to Andy. ⛔ BRANCH 3 — ANYTHING ELSE, including a count that is short OR
long, names right but IDs/rids changed, configs rolled back, automations detached, an -ARCHIVED-
name back on /bots, or a roster that moves between two captures -> STOP. NO OA WRITE. FLEET STAYS
OFF. ESCALATE: YES. Record the sub-state by name per A-01's table. You do not resolve branch 3.

STEP 1 — ⛔ AMENDED (A-02): THE PLAN IS ALREADY PURCHASED — state.md's incident block, first-hand
~12:06 ET 2026-08-07, "plan purchased, login works". DO NOT ASK ANDY TO PURCHASE ANYTHING. Read the
payment timestamp from that block and have him confirm it in one line. ⛔ AND LEDGER_START IS NOW A
GATED QUESTION, NOT A COPY — payment and Day-0 are different days, so ask Andy whether the era
starts at payment or at the first day a bot is ON, and carry his verbatim answer forward. Do not
set LEDGER_START (that is the next session's Step 1); carry it into the close-out under a heading a
later session cannot miss.
[Original Step 1 text, left standing: "Wait for gate A1. Record the payment timestamp verbatim."]

STEP 1b — ⭐ AMENDMENT A-09(a). BEFORE ANY OTHER OA ACTION: screenshot BOTH dashboard toggles on ONE
live mirror and ONE directional bot. READING AND SCREENSHOTTING IS NOT TOUCHING — you flip nothing,
open no editor, change no value. Record the filenames + timestamp in the close-out under
`2c PRE-OBSERVATION`. Step 2c's information is spent by the TRANSITION, not by the session that
reaches it, and the transition already happened. ⛔ This does NOT replace S2 Step 2c and licenses
no other contact with the nine.

STEP 2 — Gate A2, then runbook §4 Step 0a: /settings -> set `itmlive` = `market` -> HARD RELOAD ->
re-read `input.value` -> screenshot before and after. A save banner is not verification.
  ⚠️ `itmpaper` is ALREADY `market` (set + verified 2026-08-04). DO NOT RE-SET IT. Read it back as
     part of the same self-check.
  ⛔ IF the value will not persist through a hard reload -> NO CAPITAL GOES LIVE. FLEET STAYS OFF.
     Escalate to Andy: YES.
  While you are on /settings, record all seven account-level fields — they are in no /bots capture
  and they override every bot: itmlive · itmpaper · maxexits · scanstart · scanend · exitstart ·
  exitend. Expected from 2026-08-04: maxexits = 0 (Unlimited) · Bot Schedule 09:31/5 and 09:31/1.
  ⛔ `maxexits` is the dangerous one — a non-zero value reproduces the June failure shape fleet-wide
  with nothing per-bot to show for it. This closes assert A5. Record the values verbatim.

STEP 3 — VERIFY THE ROSTER.
⛔ AMENDED (A-22): THE BOOKMARKLET CAPTURE AND `Export Data` (ALL GROUPS SELECTED) ARE ANDY'S HAND —
gate A12, CLAUDE.md §2. Ask him to run them and say where the file landed; procedure
oa-ops-runbook.md §1. A get_page_text scrape is NOT a capture and is never recorded as one; if no
capture file arrives the roster check is ⬜ NOT EVALUABLE and the fleet stays OFF. Reading
`a5.bots.bot` per bot is a different thing and remains yours.
⛔ AMENDED (A-05): `QQQ-IC-0DTE-Fortress-ARCHIVED-2026-08-03` was ARCHIVED 2026-08-04 and is in the
Bot Archive. It is NOT one of the 41 and MUST NOT appear on /bots — as written, the list below
fires a false FLEET-STOP on it. Confirm `QQQ-IC-0DTE-Fortress` (the pilot clone) only; if the
-ARCHIVED- name IS on /bots, THAT is the finding (A-01 branch 3f). Contrast:
`IC-SPX-FastPT25-S2-ARCHIVED-2026-08-07` was RENAMED, not archived — it IS expected and DOES count.
⛔ AMENDED (A-08): if the first and second captures DISAGREE, that is a MOVING ROSTER until proven
otherwise, not a capture defect resolved. Record both counts with timestamps, wait 30 minutes,
capture a THIRD time, and require TWO CONSECUTIVE IDENTICAL captures. Third differs -> STOP.
⛔ AMENDED (A-01c): ALSO READ THE IDENTIFIERS, NOT JUST THE NAMES — each built bot's id from
`a5.bots.bot` against data/bots_config_v2.csv, and each shared automation's `rid` against
RTfw5TkkCRF178605283747821 / RTfw5TkkCRF178606271659881 / RTfw5TkkCRF178606373201751. Any mismatch
-> the objects were RE-CREATED, not preserved; every capture file, CSV row and signed hash is keyed
to a dead identifier, and the A-series CANNOT SEE THIS because every assert in it is relational.
STOP. FLEET STAYS OFF. ESCALATE: YES.
[Original Step 3 text follows, left standing.]
Bookmarklet capture of /bots FIRST — write the expected count down
before you capture. EXPECTED: 41 active bots, 9 left of the Pro 50.
  Arithmetic: 35 (2026-07-30) − 2 deleted = 33; + 7 greenfield = 40; + 1 PR-01 clone = 41. The
  PR-01 original was RENAMED, not archived, so it still counts.
  Confirm by name: the seven greenfield arms; `IC-SPX-FastPT25-S2` (the clone, holding the
  production name) and `IC-SPX-FastPT25-S2-ARCHIVED-2026-08-07`; `QQQ-IC-0DTE-Fortress` (pilot
  clone) and `QQQ-IC-0DTE-Fortress-ARCHIVED-2026-08-03`; the nine leave-in-place bots
  (DIR-SPX-PutVIX22-SL75, DIR-SPX-CallVIXdrop, 3DTE $140-$350, Nigiri-Paper-v1, QQQ long call,
  Friday 14 DTE Broken Wing IB (B-70), Trendy-Paper-v1, 60min-ORB-10W-Paper-v1, Tasty Condor);
  the two un-started clone originals `IC-SPX-FastPT25-S2-130PM` and `QQQ-IC-0DTE-Fortress-NoPT50`,
  both expected UNTOUCHED and UN-RENAMED.
  Also read `My Automations`: EXACTLY 4 objects — GF-ScannerA-PutSpread, GF-ScannerB-CallSpread,
  GF-Backstop-1552-FlatClose (7 bots each) and Defang-Mon-S2-StrikeTouch (2 bots).
  ⛔ IF THE COUNT DISAGREES -> recapture ONCE. IF IT STILL DISAGREES -> ⛔ STOP. FLEET STAYS OFF.
     ESCALATE TO ANDY: YES. A short roster silently drops bots from every future drift diff, and
     the drift diff is the whole detector. Do not reconcile it yourself.
  ⛔ IF A BOT IS MISSING, RENAMED, OR AN AUTOMATION'S BOT-COUNT HAS MOVED -> same STOP. The disable
     was supposed to block access, not delete anything; a deletion is a different event entirely
     and it is Andy's call, not yours.

STEP 4 — RE-RUN THE A-SERIES AGAINST FRESH CAPTURES.
⭐ AMENDED (A-26) — RUN THE SCRIPT, DO NOT HAND-DERIVE THE ASSERTS:
  `python3 scripts/a_series.py --validate`   FIRST — it asserts the tool still reproduces the
  2026-08-07 hand-run reference exactly (A1 21/21 · A2 7/7 · A3 7/7 · A7 3/3 · A8 7/7 · A9 7/7;
  A4 MOOT; A4b/A6 NOT-RUNNABLE; A5 NOT-RUN). Then `python3 scripts/a_series.py --json` for the
  close-out. Defaults resolve data/captures/, data/bots_config_v2.csv and
  docs/greenfield-family-spec.md on their own. It encodes the §9 pre-registration mechanics, the
  hash procedure and the G2 two-hop read (bot INPUT OBJECT, never the action, never oldValue).
  ⛔ IF `--validate` FAILS -> that is a defect in the TOOL, not in the record. STOP, report it, and
  fall back to the hand procedure below. DO NOT silently re-baseline and DO NOT EDIT THE SCRIPT to
  make an assert pass — scripts/ is Claude Code's lane and its PRE_REGISTRATION table is a spec
  surface (amending it is an "amend the plan" edit).
  ⛔ THE SCRIPT IS NAME-KEYED BY CONSTRUCTION AND READS NO OA ID — which is why it survives a
  rekeying restore and why IT CANNOT DETECT ONE. A restore that re-creates every object under the
  same names gives you a FULLY GREEN A-SERIES OVER DEAD IDENTIFIERS. A-01c's manual bot-ID and rid
  comparison is a SEPARATE, STILL-MANDATORY check. A green run does not close it.
⛔ AMENDED (A-15) — FALLBACK ONLY, if the script is absent or will not run: A1's AMENDED text and
A3's comparand are NOT in this prompt — they are in greenfield-family-spec.md §8.3 and §9. Read
them; do not run A1 from the one-line summary below. The HASH PROCEDURE is in no prompt either: use
exactly the procedure recorded in
data/captures/2026-08-07-greenfield/ASSERTS-A1-A9-and-capture-diff.txt, which produced the baselines
you are comparing to. If that file does not state the serialization -> A7 IS ⬜ NOT EVALUABLE. Do
not invent a hash input and NEVER compare a recorded baseline to itself.
⛔ AMENDED (A-13): A7 IS 3 OF THE FOUR SHARED AUTOMATIONS THE RUNBOOK REQUIRES — AND THE SCRIPT
DOES NOT CHANGE THIS: its SHARED_AUTOMATIONS list carries the same three, so a green `A7 3/3` from
the tool is still 3 of 4.
`Defang-Mon-S2-StrikeTouch` (2 bots) has NO recorded baseline. Report A7 as 3/4 with it named ⬜ NOT
EVALUABLE — do NOT report 3/3 as complete. Recording its FIRST baseline (read after hard reload,
hash, write the row) is a read-and-record and is allowed; say plainly it is a first baseline.
⛔ AMENDED (A-21): EVERY ESCALATION GOES TO ANDY, NOT TO A MODEL. "DIVERGES" MEANS EXACTLY: active
count ≠ 41; or any name in Step 3's CORRECTED list absent, altered or unexpectedly present; or any
shared automation's bot-count ≠ expected; or any bot ID / rid ≠ recorded; or any assert other than
A7 fails. A7 drift ALONE is not a divergence — diff, report, GATE.
[Original Step 4 text follows, left standing.]
Not against the 08-07 file — that file is the
reference you compare TO. One page load per bot, after a hard reload, read from `a5.bots.bot` (and
`a5.bots.acedit.routine` for the three Library objects). Never innerText, never a save banner.
  RUN: A1 (21/21 under the AMENDED rule — arm-vs-control differ in exactly ONE mechanic;
       arm-vs-arm in exactly TWO, precisely each arm's own; PT50/Canary and SL100/SL200 share a
       field and differ in ONE, so they are checked under the arm-vs-control rule. ⛔ Build against
       the AMENDED text, not the struck one.)
       A2 (7/7 — every non-bundle field equal INCLUDING trigger config and scan speeds; `exitrate`
       is stored = 1 on all seven since the 08-07 two-step fix)
       A3 (7/7 — each arm's decoded set == its pre-registered set. A3 is the load-bearing one.)
       A5 (from Step 2's /settings read)
       A7 (3/3 — payload hash of each shared automation vs its recorded baseline:
           ScannerA 3308ce8b476d2bd090d9519b445748fc4c0d0fdbe71861c83a249729b1a5a30a @ v9
           ScannerB bb4ba866a13e7ecd682f7bda9a19011003e9e3ef73fffd0fb64a80a4cd0eb32e @ v2
           Backstop 116069bddf8b8c9e58bd8f28313c2ad95726fa3f7205df4dfde82de7a3e2e5b5 @ v1)
       A8 (7/7 — decoded(GF_EXITS_PUT) == decoded(GF_EXITS_CALL) per arm)
       A9 (7/7 — both bot inputs BOUND and NON-EMPTY on every arm)
  ⛔ THE G2 RIDER APPLIES, TWO HOPS DEEP. The saved action stores a REFERENCE, not values. Resolve
     action -> automation input -> BOT input and read the INPUT OBJECT'S VALUE. A capture that
     reads only the action records the input's NAME and every arm diffs as identical — the
     tournament is then undetectably void. ⚠️ NEVER read `oldValue` as current config: it is a
     stale pre-link snapshot. The control is at: bot settings page -> the automation row's ⚙ Edit
     Settings -> 🔗 -> `Bot Inputs`.
  NOT RUNNABLE YET, and say so by name rather than omitting them: A4 (struck moot),
  A4b and A6 (both need positions — they belong to Day-1).
  ⛔ IF ANY ASSERT FAILS -> record the failure verbatim with the bot and the field. DO NOT FIX IT.
     FLEET STAYS OFF for the family. ESCALATE TO ANDY: YES. The family was green on 2026-08-07
     with AUTOMATIONS OFF; a fail now means something changed during a lockout that was supposed
     to block access, and that is a finding, not a repair job.
  ⚠️ A7 drift is NOT automatically a failure — A7-DRIFT-1 (2026-08-07) was ruled ADOPT because the
     tree and the full Open-Position payload diffed field-by-field UNCHANGED. But that ruling was
     Andy's, on evidence. If A7 drifts again: diff the tree and payload field-by-field, report what
     you find, and GATE it. Do not re-baseline on your own.

⛔ STEP 4b — ADDED 2026-08-07 (AMENDMENT A-07). RE-CAPTURE AND DIFF EVERY NON-GREENFIELD BOT.
The A-series is n=7 and covers the greenfield family only. Thirteen bots would otherwise go from
"lost" to "signed and switched ON" with their config never re-read. For `IC-SPX-FastPT25-S2` (the
clone), `IC-SPX-FastPT25-S2-ARCHIVED-2026-08-07`, `QQQ-IC-0DTE-Fortress`,
`IC-SPX-FastPT25-S2-130PM`, `QQQ-IC-0DTE-Fortress-NoPT50` and EACH OF THE NINE: fresh capture after
a hard reload, resolve the input chain two hops where one exists, diff FIELD-BY-FIELD against that
bot's own capture file on disk. ⛔ ANY DIFF -> that bot's config-capture hash is NOT ESTABLISHED,
its entry CANNOT BE SIGNED at Step 2b, BOT STAYS OFF, fleet proceeds, ESCALATE: YES.
⛔ A capture file written before the roster was lost is a record of a bot that no longer
demonstrably exists. Do not sign against one without this diff.
⚠️ This is a READ on the nine — it is not toggle intervention and does not spend Step 2c. Declare
it in the close-out attestation (A-18).

⛔ GATE A4 LANDS HERE (AMENDMENT A-20), NOT AT THE CLOSE-OUT. Andy declares the roster + A-series
verdict ACCEPTED before any OA EDIT is made. IF ANDY IS UNAVAILABLE, STOP AFTER STEP 4b with the
roster and A-series report; Steps 5–8 move to a follow-up session. ⚠️ A-23: S0 is two chats — this
is the boundary. S0a = gate A0 → Step 4b → A4 → close-out. S0b = Steps 5–8, fresh chat.

STEP 5 — APPLY THE RULED F-C1 REMOVAL TO THE PR-01 CLONE (only after gate A3).
⛔ AMENDED (A-03): GATE A3 IS DISCHARGED AS A RULING — F-C1 (REMOVE) and F-C2 (Trap 10 authorized)
ARE RECORDED IN docs/state.md AND docs/session-log.md, dated 2026-08-07, first-hand. VERIFY THEM BY
READING; DO NOT ASK ANDY TO RE-CONFIRM, and ⛔ never let a failure to get a ruling re-said retract a
ruling already in the folder. What is outstanding is the APPLICATION, which is this step.
⚠️ A-01 branch 3d applies first: if the restore rolled this bot back, `profits` may be absent for
the WRONG reason. Step 4b's diff is what tells you which; a post-edit self-check cannot.
  TARGET: `IC-SPX-FastPT25-S2`, the CLONE `BOTfw5TkkCRF4417860821948715488`. NOT the archived
  original — that is a lineage record and stays byte-identical to its Step-0 baseline.
  DO: remove `exits.profits` (0.25) from BOTH Open Position actions — put side and call side.
  Read first-hand 2026-08-07: `exits.profits = 0.25`, `smprofits "normal"`, text "Profits: 25%".
  build-plan.md §2B, verbatim: "PT25 removed from the Open Position action explicitly — not left
  dead behind an off toggle."
  ⛔ REMOVE ONLY `profits`/`smprofits`. Touch nothing else in the bundle, nothing else in the
     action, and nothing in `Scalp-Mon-S2-Cleanup` — S2 depends on Cleanup (build-plan §2B).
  ⛔ DO NOT rebuild the action to do it. If `profits` cannot be cleared in place, STOP —
     rebuilding the action would destroy the exits bundle and the re-entry-gate work.
  VERIFY: hard reload -> re-read `node.input.exits` on both actions -> confirm `profits` is absent
  -> confirm `disableExits` is still 1 (EXIT OPTIONS OFF) -> screenshot the toggle. Re-hash all
  four of the clone's automations and confirm only the two scanners' Open actions moved.
  ⛔ ALSO CONFIRM the ORIGINAL `…-ARCHIVED-2026-08-07` is untouched: `Scalp-Scan-Put` must still
     hash `91da84fd2b7aafbb…`, 5027 bytes, version 2.
  Layer 2 is DEFERRED to Day-0's Step 6 and it is INVERTED for this bot — the Trades list must show
  NO PT row and NO exit-trigger row, and the S2 monitor MUST be firing. Say so in the close-out.

STEP 6 — FINISH PR-01's RECORD ARTIFACTS (interrupted when `showBotMenu` went dead).
  a. Save Template V1 with the PR-01 pre-registration note attached.
  b. Write the PR-01 Notes block. ⛔ DOUBLE-ESCAPE FROM THE FIRST WRITE and verify byte-exact
     length-and-content against the source. The pilot's defect reproduced twice on PR-14 before it
     was defeated this way.
  c. Add the tag. It will store as `pr 01` — that is correct, not a failure. Tags are on the
     DASHBOARD tab. Click the suggestion item; re-read the input's value per add (the tag menu
     serves stale lists after a timeout).
  ⛔ IF `showBotMenu` GOES DEAD AGAIN -> three attempts, then STOP. These are RECORD ARTIFACTS;
     nothing in the Day-0 sequence reads them. Record them as NOT DONE and carry them forward.
     Do not let this block anything.

STEP 7 — RECORD WHAT THE FOLDER IS MISSING.
⛔ AMENDED (A-03): (a) AND (b) BELOW ARE FALSIFIED — BOTH ARE ALREADY IN THE FOLDER. state.md
carries the 04:24 ET lockout block, and both "F-C1 — RULED 2026-08-07 … REMOVE" and "F-C2 — RULED
2026-08-07 … AUTHORIZED AS TRAP 10"; session-log.md carries the same F-C1 banner. (a) and (b)
become VERIFY-AND-REPORT: read the blocks, confirm they are there, report "already recorded".
⛔ DO NOT WRITE A SECOND DATED BANNER FOR EITHER — a duplicate ruling banner in the project's single
source of facts is worse than a missing one. (c) stands as written.
⛔ WHAT S0 MUST ACTUALLY RECORD INSTEAD: gate A0's finding — the restore state, first-hand, with the
footer read verbatim, the capture timestamps, and the branch taken.
[Original Step 7 text follows, left standing.] Three items, found 2026-08-07:
  (a) The ~04:20 ET 2026-08-07 lockout ("Account disabled, please purchase a plan") is in project
      memory only — NOT in docs/state.md and NOT in docs/session-log.md. Write it into both, as a
      dated first-hand record, noting that it SUPERSEDED the "inactive banner is cosmetic" finding.
  (b) The F-C1 and F-C2 rulings are in project memory only; state.md line ~1495 and session-log.md
      line ~5198 both still read GATED. Once gate A3 lands, record both as ruled-and-applied with
      the date and Andy's re-confirmation. Leave the original GATED text standing per the doc's
      correction convention.
  (c) `docs/decision-card-2026-08-06.md` was modified and
      `data/captures/2026-08-06-gfam/GF-Backstop-1552-FlatClose.txt` untracked as of 2026-08-07.
      Tell Andy at close-out so the tree is committed before the Day-0 sequence starts.

STEP 8 — PRE-FLIGHT FOR THE NEXT SESSIONS. Read and REPORT, do not fix:
  - `data/raw/` and `data/brief/` — expected EMPTY (they were on 2026-08-07). If not, the
    pre-cutover-files box is unticked and the runbook says resolve before §4 starts.
    ⛔ CORRECTED 2026-08-07 ON ANDY'S RULING — THE "EXPECTED EMPTY" CLAUSE ABOVE IS SUPERSEDED.
    ORIGINAL LEFT STANDING; READ THIS WITH IT. `data/brief/` IS empty ✅. `data/raw/` IS **NOT**
    EMPTY AND MUST NOT BE MADE EMPTY: it holds `data/raw/2026-08-07.csv` (428KB, 1,386 rows), the
    Export Data pull Andy filed. ⛔ DO NOT DELETE IT. It is filed exactly where
    `oa-ops-runbook.md` §1.7 and `daily.sh`'s own header ("drop the OA positions CSV in data/raw/
    named YYYY-MM-DD.csv first") say the export belongs. The clause was written BEFORE the capture
    ritual had run and it mistakes the instrument for the hazard.
    ⭐ RE-READ THE BOX TO WHAT IT ACTUALLY PROTECTS AGAINST: **pre-cutover rows reaching the
    WORKING LEDGER.** That is the test, and it PASSED first-hand on 2026-08-07 — stage 1 took
    1,386 export rows to **0 post-cutover / 1,386 discarded pre-cutover / WORKING LEDGER n=0**.
    ⛔ SO THE BOX IS SATISFIED BY THE LEDGER COUNTS, NOT BY AN EMPTY DIRECTORY. An empty
    `data/raw/` proves nothing; a 1,386 → 0 filter proves the cutover works under real load.
    ⛔ UPDATED AGAIN 2026-08-08 — `data/brief/` IS NO LONGER EMPTY EITHER, AND THAT IS ALSO FINE.
    SAME RULE, NO EXCEPTION: **a populated `data/brief/` is WORKING OUTPUT, not contamination.**
    It holds `2026-08-08_tape.json` — a **GATE-A9 TEST ARTIFACT**, generated 2026-08-08T09:34:30
    by the `daily.sh` test run on a **SATURDAY**, empty payload (`underlyings {}`,
    `any_reconstructed false`, `divergence null`). That is **correct degradation on a non-trading
    day**, not a data failure and not a flat tape. It is labelled in place with a `_note` key
    (inert — every consumer reads only `underlyings` via `.get()`). ⛔ **NO LATER SESSION MAY READ
    IT AS A REAL BRIEF** or treat the absent underlyings as zeros.
    ⛔ **NEITHER DIRECTORY IS EXPECTED TO BE EMPTY FROM DAY-0 ONWARD.** Matching amendment:
    `reactivation-runbook.md` §4's checklist box, amended 2026-08-07 on Andy's authorization.
  - `data/ledger_meta.json` — expected `"ledger_start": "2099-01-01"` (the refuse-everything
    sentinel). It is CORRECT pre-Day-0 and it is NOT the value to keep.
  - ⛔ ANDY'S GATE A9: `daily.sh` at n=0 has NOT been run and is a HARD BLOCKER. You cannot run it
    — `tape.py` needs network and `device_bash` has none. Ask Andy to run `bash scripts/daily.sh`
    from his own terminal and paste the output. Read it against the runbook §3 Step E branches:
    a script that raises -> fix the script, NEVER the data, NEVER seed a synthetic row; `0.0%`
    expectancy or a populated-looking table at n=0 is a FAILURE, not a pass; Tier C rules
    reporting SKIPPED because bots_config_v2.csv is incomplete is CORRECT behaviour — silence in
    its place is the failure. ⛔ Day-0's §4 does not start until a clean end-to-end n=0 run is on
    file.
  - `daily.sh`'s eight stages carry NO A-series runner. The A7 baselines are recorded in
    bots_config_v2.csv but A7 IS NOT WIRED INTO daily.sh, which runbook Step 4(b) requires. Report
    it as an OPEN Step-4(b) gate. Wiring it is Claude Code's lane, not yours.

=== ⛔ WHAT THIS SESSION MUST NOT DO ===
- DO NOT TOUCH ANY OF THE NINE LEAVE-IN-PLACE BOTS, in any way, for any reason. Runbook Step 2c
  requires a NO-TOUCH OBSERVATION of their dashboard toggles before anything is moved, and the
  information it captures is NOT RECOVERABLE afterwards: if exits resume at reactivation with no
  toggle intervention, billing state is implicated as the June cause; touch a toggle first and the
  toggle candidate and the billing candidate become permanently indistinguishable.
  ⚠️ Step 2's ACCOUNT-LEVEL `itmlive` is explicitly NOT toggle intervention. Nothing else may
  touch a bot before Step 2c runs.
- DO NOT switch AUTOMATIONS ON on anything. Not one bot. That is Step 7 of the sequence, two
  sessions from now, and only for bots that passed Step 6.
- DO NOT flip any EXIT OPTIONS toggle on the nine. That is Step 3, in S2.
- DO NOT start the PR-02 or PR-04 clones. That is S1.
- DO NOT archive anything. Andy's hand.
- DO NOT sign a pre-registration entry, or fill a SIGNED line. Andy's, at Step 2b.
- DO NOT run the Day-0 sequence. This session is the opening, not the sequence.

=== CLOSE-OUT (CLAUDE.md §9.1 — mandatory, in this order) ===
1. Append docs/session-log.md; update docs/state.md for every fact that changed (the lockout
   record, the F-C1/F-C2 rulings, the roster verification, the A-series re-run verdict, `itmlive`).
   Verify EVERY edited file by direct `device_bash` sha256 + a single-match grep of the new text.
2. Update the `bot-fleet-migration` tracker artifact via `update_artifact`, and ASK ANDY TO
   VISUALLY CONFIRM IT. The close-out is not complete without his confirmation.
3. Say "ready to commit" with a one-line summary of the changed files. DO NOT COMMIT.
4. HAND-OFF BLOCK for S1, written so the next session needs nothing else:
   - the payment timestamp, verbatim, labelled LEDGER_START CANDIDATE
   - roster verdict: count, and every by-name confirmation or divergence
   - A-series verdict, per assert, including the ones not run and why
   - the seven /settings values, verbatim
   - F-C1 / F-C2: ruled or still gated, and what was applied
   - PR-01: what landed, what did not
   - everything still OPEN, by name — an unrun check is NOT EVALUABLE, never a pass
   ⛔ ADDED 2026-08-07 (evening):
   - GATE A0's VERDICT: the /bots footer verbatim, both/all capture counts with timestamps, the
     two-consecutive-match confirmation, and WHICH BRANCH (1 / 2 / 3+sub-state) you took
   - the ID and rid comparison result (A-01c), per bot and per shared automation
   - STEP 4b's per-bot diff result for all thirteen non-greenfield bots — and, for each, whether
     its config-capture hash is ESTABLISHED or NOT ESTABLISHED
   - A7 reported as 3/4, with Defang-Mon-S2-StrikeTouch named ⬜ NOT EVALUABLE or newly baselined
   - the `2c PRE-OBSERVATION` screenshot filenames + timestamp (A-09a)
   - ⛔ ATTESTATION (A-18): state explicitly whether ANY of the nine leave-in-place bots was
     opened, edited, or had a toggle touched this session, BY NAME. "None" must be WRITTEN.
     Silence is not an attestation. Declare the A-09a screenshots and the Step 4b captures here as
     READS.
   - ⛔ A FLEET STAYS OFF verdict, if one fired, stated in those words at the top of the hand-off —
     S1 is instructed to refuse to start on it (A-06)
```

---

## S1 — THE TWO REMAINING CLONES

**Model: Sonnet.** The clone ritual is a nine-step checklist with an explicit branch at every step
and no judgment left in it. Every branch here says either "bot stays OFF, fleet proceeds" or
"escalate" — both are mechanical.
**Andy attended: not required**, except if a branch fires. S1 can run unattended.

```text
You are working in bot-fleet-v2 (~/bot-fleet-v2 via the device bridge). Day-0 is in progress. S0
has run (read its close-out first). Your job: build the last two clones — PR-02 and PR-04 — per the
ruled pattern, and NOTHING else.

⛔ PRECONDITION, ADDED 2026-08-07 (AMENDMENT A-06). READ S0's CLOSE-OUT IN THE FOLDER FIRST, NOT
FROM MEMORY. IF it records a `FLEET STAYS OFF` verdict, OR gate A0 landed on branch 2 or branch 3,
OR no close-out exists, OR its hand-off block is absent or incomplete -> ⛔ DO NOT START. Record
`BLOCKED ON S0 — <verbatim branch>` and hand to Andy. A hand-off you had to reconstruct is a
hand-off that did not happen. ⛔ AND IF GATE A0 LANDED ON BRANCH 2 (no restore), PR-02's AND PR-04's
ORIGINALS DO NOT EXIST — rebuild-contingency-2026-08-07.md §2: there is nothing left to clone from,
template or otherwise. This session is unexecutable; say so and stop.

⛔ READ `docs/day0-session-pack-2026-08-07.md` §0.0 — THE AMENDMENTS — BEFORE ANYTHING ELSE. Where
§0.0 and the text below conflict, §0.0 WINS. The ones that change this session: A-06 (above) ·
A-14 (the coordinate ban) · A-15 (the Notes source text) · A-16 (the pack's step ORDER supersedes
runbook §2's, and runbook §2 step 7's "do not remove PT25" is superseded) · A-17 (Trap 10's
precondition; and the control clones stay OFF if F-C1 was not applied) · A-18 (the attestation) ·
A-22 (captures are Andy's hand) · A-25 (project memory is corroboration, not a precondition).

READ FIRST, FRESH:
  docs/day0-session-pack-2026-08-07.md   ⛔ §0.0 FIRST, then §0, §1, and S0's hand-off block
  docs/state.md                          ⛔ the dated tail blocks — F-C1/F-C2 RULED, and the
                                         `OA REACTIVATED BUT ROSTER LOST` incident block
  docs/rebuild-contingency-2026-08-07.md ⛔ read before assuming an original exists to clone
  docs/pre-registration-ledger.md        §4 — the PR-02 and PR-04 entries. ⛔ The SOURCE TEXT for
                                         step 8's Notes / template note. Do not compose one.
  docs/session-log.md                     S0's entry, in full
  docs/reactivation-runbook.md            §2 — the nine-step per-clone checklist, IN FULL
  docs/build-plan.md                      §2B — the two clone specs. FROZEN. Nothing beyond spec.
  docs/pilot-clone-card-qqq-fortress.md   the live-follow card; every clone reuses this shape
  docs/oa-ops-runbook.md                  §4 (edit verification), §5 (the traps)
  data/archive/rename_map.csv             the lineage record you append to as you go
  project memory: clone-sweep-status      (⚠️ its "F-C1/F-C2 GATED" lines are superseded if S0
                                           landed gate A3 — S0's close-out is authoritative)

=== STANDING FACTS — TRUE ALL SESSION ===
[Identical to S0's block. Reproduced verbatim so this prompt is self-contained.]
1. NEVER RUN GIT, in any form, INCLUDING `git status`. The bridge cannot unlink, so git from this
   side strands .git/index.lock and Andy removes it by hand. Verify files by direct `device_bash`
   sha256 + a single-match grep. Never the write tool's response, never a stage-back read.
   ANDY RUNS EVERY COMMIT.
2. THE LOCKOUT SUPERSEDED THE OLD BANNER FINDING — sessions start LOGGED OUT unless S0 has already
   reactivated the account. Confirm from S0's close-out; do not assume a live session.
3. NOTES: DOUBLE-ESCAPE FROM THE FIRST WRITE (`&amp;lt;`). OA's sanitizer decodes entities THEN
   strips unknown tags, and the rendered panel still looks correct. Verify byte-exact.
4. DECISION NODES: use `NOT`, never a rebuild. OA has no move-node control; rebuilding an action
   destroys its `exits` bundle.
5. PICKERS NO-OP on the already-displayed value. Force with a two-step. Verify the STORED field.
6. CLICKING: refs silently no-op; JS dispatch is harness-blocked on this app. Compute from the DOM:
   scale = screenshotWidth / window.innerWidth, click at rect.centre × scale. NEVER carry a
   coordinate across a window resize.
7. `Runtime.evaluate` times out at ~45s WITH THE WORK COMMITTED — re-read, never re-fire. Titles
   commit on BLUR. `overlay.innerText` goes stale mid-animation — screenshot first. Prefer
   `form_input`, re-read `.value`. Tags: click the suggestion; `PR-02` stores as `pr 02`; tags are
   on the DASHBOARD tab. `a5.bots.bot` is the hydrated client model.
8. `archiveBot` / `showBotMenu` are ANDY'S HAND. Three attempts, then STOP. NEVER coordinates on
   that menu — `Delete` sits ~29px below `Archive`.
9. TWO-LAYER EDIT PROOF. Layer 1 = re-observe after a HARD RELOAD. Layer 2 = the first NEW
   position's Trades list. The Exit Options panel is NEVER evidence.
10. WHEN IT IS AMBIGUOUS, IT IS GATED.

=== THE STOP LADDER ===
Documented method -> ONE documented alternative -> third attempt max -> STOP. No forcing, no
coordinate fallback, no improvised remedy. Record verbatim and take the runbook's own branch. An
unrun check is NOT EVALUABLE and is never a pass. Ambiguous -> GATED, escalate, stop that thread.
⚠️ ON THIS SESSION SPECIFICALLY: a failed clone stops THAT CLONE. The other one proceeds. Only a
Library-propagation event (step 2's branch) stops both.

=== ⛔ WHAT THIS SESSION MUST NOT DO ===
- DO NOT TOUCH ANY OF THE NINE LEAVE-IN-PLACE BOTS. Step 2c's no-touch observation has not run yet
  and its information is not recoverable afterwards. Clones only.
- DO NOT switch AUTOMATIONS ON. Both clones end this session with AUTOMATIONS OFF.
- DO NOT archive anything — not the originals you rename. Renames commit; archives are Andy's hand
  and they are hygiene, not a blocker.
- DO NOT sign anything.
- DO NOT touch the pilot (`QQQ-IC-0DTE-Fortress`) or the PR-01 clone. Both are finished.
- DO NOT run the Day-0 sequence.

=== ORDER OF WORK: PR-02 FIRST, THEN PR-04. PER-CLONE ATOMIC. ===
Finish and verify one completely before starting the other. A mistake made once is a lesson; the
same mistake across two bots is a rebuild.

────────────────────────────────────────────────────────────────
CLONE 1 — PR-02 · `IC-SPX-FastPT25-S2-130PM`
────────────────────────────────────────────────────────────────
SPEC (build-plan.md §2B, frozen): identical to PR-01 with a 1:30 PM entry. Ride + S2. The entry-time
A/B partner. Same two safety fixes, same Exit-Option-free spec. NO NEW EXIT ARCHITECTURE — it is a
control. ⛔ DO NOT TOUCH `Cleanup` ITSELF — S2 depends on it.

⛔ AMENDED 2026-08-07 (A-16a): THE ORDER BELOW SUPERSEDES runbook §2's NUMBERING AND IT IS THE ONLY
ORDER YOU FOLLOW. §2 is read for its BRANCHES and its trap text, not its sequence — §2 clones at
step 1 and renames at step 8; this list captures a Step-0 baseline first and RENAMES BEFORE THE
CLONE, because the Clone Settings drawer sets the production name at creation and the original must
have released it. Where they disagree on ORDER, this list wins. Where they disagree on a BRANCH,
stop and gate it.
[Original sentence, left standing:] Run runbook §2's nine steps in order.
The clone-specific points that cost real time on PR-01:

0. STEP-0 BASELINE CAPTURE OF THE ORIGINAL FIRST, and hash all four of its automations. That
   baseline is what proves later that the original was never touched.
1. RENAME THE ORIGINAL FIRST — `IC-SPX-FastPT25-S2-130PM-ARCHIVED-<today>`. It frees the production
   name and keeps the archived record self-labelling. Titles commit on BLUR.
2. CLONE. ⭐ The Clone Settings drawer exposes Name + Account + Allocation BEFORE creation — set
   the production name and the real allocation THERE. This pre-empts the allocation trap and
   retires the pilot card's temporary-name step entirely.
3. CHECK THE AUTOMATION LIBRARY BEFORE EDITING ANYTHING. ⚠️ CLONING COPIES — the old "clones share
   automations by reference" text is FALSE and corrected. Clone-owned automations read `sharing=0`
   and get NEW rids. Sharing is opt-in via the Library only, and this bot's automations are not in
   it (the Library holds exactly 4 objects: the three GF objects at 7 bots each, and
   `Defang-Mon-S2-StrikeTouch` at 2). So: EDIT DIRECTLY, no fork needed. Then confirm the
   ORIGINAL's automation list is unchanged — a sanity check, one page load.
   ⛔ IF THE ORIGINAL'S LIST CHANGED -> you are editing a shared object and the edit HAS ALREADY
      PROPAGATED. STOP THIS CLONE. Do not proceed. Record which automation and what changed. BOTH
      CLONES STOP until the blast radius is known — check every bot the Library reports as using
      it. ESCALATE TO ANDY: YES.
4. THE FOUR CLONE TRAPS. All four bit on PR-01; check every one, by reading the value back:
   - Allocation resets to a flat `1000` (original $50,000) — a silent 100× sizing error on a bot
     that looks fine on the dashboard. Pre-empt it in the Clone Settings drawer; read it back.
   - Bot Group drops to `None`. PR-01's clone is `IC-Focus` — match it.
   - Tags drop to empty. PR-01's clone carries `live candidate,focus ic`.
   - ⛔ AMENDED 2026-08-07 (A-17): TRAP 10 CARRIES THE SAME PRECONDITION AS F-C1 — same ruling
     class, same date. Verify F-C2 reads RULED / AUTHORIZED in state.md (it does, first-hand
     2026-08-07). IF A SESSION EVER FINDS IT NOT RECORDED -> do NOT restore `disableExits` on your
     own reading: leave it, record it, ESCALATE: YES. A clone with EXIT OPTIONS ON and PT25 still
     present is a live hazard, not a tidy-up.
   - ⛔ TRAP 10 (F-C2, found 2026-08-07, authorized by Andy): `disableExits` RESETS 1 -> 0 ON
     CLONE. EXIT OPTIONS turns ON. Unlike the other three this makes the clone DO SOMETHING —
     composed with F-C1 it would arm PT25 on a ride benchmark and trip its own REMOVED_EXIT_FIRED
     kill criterion on day one. It is INVISIBLE TO TEXT CAPTURE by construction. RESTORE
     `disableExits` TO 1 AND VERIFY IT — screenshot the toggle, it does not survive text capture.
   Then READ THE SYMBOLS PANEL BACK, character by character, against the original's list. It is
   NOT empty — look at it again; this is the single most common silent clone failure in this fleet.
   ⛔ IF IT IS EMPTY OR DOES NOT MATCH -> re-add ONCE via the form control, re-read `.value`
      (typed input lands intermittently). STILL WRONG -> STOP THIS CLONE, BOT STAYS OFF, the other
      clone proceeds, ESCALATE TO ANDY: YES. Every later step would sit on a bot that never scans.
5. THE TWO SAFETY FIXES, both per the PR-01 pattern, both Layer-1 verified after a hard reload:
   a. RE-ENTRY GATE, on BOTH scanners:
      `countpostag{cop:eq, tags:"…side", count:0, status:"open"}`
        -> `postagtoday{"oc":"opened", "not":true, "tag":"put|call side"}`, ACTION LEFT ON YES.
      ⚠️ This diverges in FORM from the greenfield scanners (plain `postagtoday`, action on NO) and
      the divergence is DELIBERATE and recorded, not smuggled: OA has no move-node control, so the
      NO form requires deleting and rebuilding the Open Position action IN FULL — including its
      `exits` bundle. `NOT` is a first-class criterion operator (`Create Group | NOT | 🗑`) and
      `oc` offers only opened/closed, so there is no negated recipe variant. Logically identical;
      the action node stays byte-untouched. USE THE SAME FORM PR-01 USES.
   b. CLEANUP PRICING: `{"text":"Market","smart":"market"}` -> `{"pct":100, "smart":"speedy"}`.
      ⚠️ §2B says only "Market -> SmartPricing" and does not name a tier. PR-01 chose `speedy`
      (= Fast) as byte-identical to this same bot's own StrikeTouch closes — least-invention.
      USE `speedy`. Do not re-open the choice. ⛔ Nothing else in Cleanup is touched.
6. ⛔ AMENDED 2026-08-07 (A-16b): runbook §2 step 7 STILL CARRIES THE PRE-RULING BRANCH — "IF PT25
   is still present on a control clone's Open Position action -> do not remove it yourself … Bot
   stays OFF · escalate to Andy: YES". IT WAS NEVER AMENDED FOR F-C1 AND IT IS SUPERSEDED by
   F-C1 RULED: REMOVE (Andy, first-hand, 2026-08-07, recorded in state.md and session-log.md).
   DO NOT TREAT THE CONFLICT AS AMBIGUITY AND DO NOT STOP ON IT. ⛔ Report the un-amended runbook
   line at close-out as a doc-correction item for Andy — the runbook is his to amend.
   ⛔ AMENDED (A-03): the PRECONDITION below reads "S0's gate A3 landed". A3 is DISCHARGED AS A
   RULING — F-C1 is recorded RULED: REMOVE in the folder. Verify by reading state.md; do not treat
   a missing re-confirmation as a retraction.
   ⛔ AMENDED (A-17): IF F-C1 SOMEHOW READS NOT-APPLIED AT THE END OF THIS SESSION, BOTH CONTROL
   CLONES STAY OFF. "Fails by construction" is NOT a pass and NOT an exemption — the arm has no
   valid control until the removal lands.
   [Original step 6 follows, left standing.]
   ⛔ F-C1 — APPLY THE RULED PT25 REMOVAL, on the CLONE only. Remove `exits.profits` (0.25) and
   `smprofits` from BOTH Open Position actions, put side and call side. build-plan.md §2B: "PT25
   removed from the Open Position action explicitly — not left dead behind an off toggle."
   ⛔ PRECONDITION: S0's gate A3 landed and F-C1 reads RULED: REMOVE in S0's close-out. IF IT IS
      STILL GATED -> DO NOT REMOVE IT. Build the clone with PT25 in place, record that PR-02's Day-0
      INVERTED check fails by construction exactly as PR-01's does, and ESCALATE TO ANDY: YES.
   ⛔ Remove ONLY `profits`/`smprofits`. Do not rebuild the action to do it — that destroys the
      exits bundle and the re-entry-gate work. If it cannot be cleared in place, STOP.
7. NO-UNINTENDED-EDITS PROOF, BY HASH, NOT BY EYE. Re-hash the ORIGINAL's automations after every
   clone edit and confirm they are byte-identical to the Step-0 baseline. Confirm all four of the
   clone's automations carry DIFFERENT rids from the original's. (On PR-01: the original's
   `Scalp-Scan-Put` still hashed `91da84fd2b7aafbb…`, 5027 bytes, v2, after every edit.)
8. CAPTURE the automation tree -> `data/captures/<date>-clones/`. Save Template V1 with the PR-02
   pre-registration note attached (⛔ DOUBLE-ESCAPE, verify byte-exact). Add the tag — it stores as
   `pr 02`, which is correct.
9. VERIFY BOTH DASHBOARD TOGGLES AND SCREENSHOT THEM. For this bot EXIT OPTIONS stays OFF BY DESIGN
   and PT25 is removed from the action — VERIFY THE REMOVAL, not the toggle.
   ⛔ IF PT25 IS STILL PRESENT after step 6 and F-C1 was ruled -> BOT STAYS OFF, ESCALATE: YES.
   Layer 2 is DEFERRED TO DAY-0 AND IT IS INVERTED: the Trades list must show NO PT row and NO
   exit-trigger row, and the S2 monitor MUST be firing. ⚠️ Monitor silence is NOT "ride behavior
   intact" — zero log rows is a liveness RED.
10. APPEND `data/archive/rename_map.csv` AS YOU GO, not afterwards from memory:
    original_name, archived_as, clone_name, date, disposition. It is the only thing that will later
    connect a name in the frozen ledger to a bot running today. Append the row to
    `data/bots_config_v2.csv` too, with the config-capture hash.

────────────────────────────────────────────────────────────────
CLONE 2 — PR-04 · `QQQ-IC-0DTE-Fortress-NoPT50`
────────────────────────────────────────────────────────────────
Same nine steps, same four traps, same hash proof, same rename_map row.
SPEC (build-plan.md §2B, frozen): 15:50 time exit + 15:52 flat-close Scheduled Event backstop.
**NO PT50.** This restores the bot's declared no-PT design and preserves the real A/B — PT50 vs
none, against the pilot clone, everything else matched. The name stays; it is now accurate.

DIFFERENCES FROM PR-02, and they matter:
- ⚠️ THE SYMBOLS TRAP DOES NOT BITE THIS FAMILY. The Fortress pair's symbol is AUTOMATION-RESIDENT
  (`Loop QQQ` + action `Symbol: QQQ`) and carried across the clone correctly on the pilot. It still
  bites any bot using the Bot Symbols loop. CHECK WHICH KIND YOU HAVE — do not assume either way.
- F-C1 DOES NOT APPLY. F-C1 is about the champion pair's PT25. This bot's spec is "no PT50", which
  is a different clause. Read the action and confirm no `profits` is present; if one IS present,
  that is a NEW finding — record it and GATE it. Do not treat it as F-C1 by analogy.
- THE 15:52 BACKSTOP. ⛔ IF IT IS NOT BUILDABLE, that does NOT make the clone unclean — it is a
  known unknown with its own branch: LEAVE IT UNBUILT, FLAG IT, FINISH THE CARD. ⛔ DO NOT
  SUBSTITUTE A DIFFERENT TIME. The minute is in build-plan.md §2B and §0 says do not improvise a
  change here on the day.
- ⚠️ D3 IS OPEN AND IT BEARS ON THIS BOT. The 15:52 trigger serialises `startDate
  …T20:52:00.000Z` = 15:52 at UTC−5 but **16:52 ET in August (EDT)**. `ntime=1552` is the operative
  field and nobody has observed which one wins. It is UNRESOLVED and it is READ AT STEP 5a OF THE
  SEQUENCE, not here. Build to spec; do not re-time anything; note in the close-out that this bot
  is affected.

=== CLOSE-OUT (CLAUDE.md §9.1 — mandatory, after EACH clone, not once at the end) ===
1. Append docs/session-log.md; update docs/state.md. Verify every edited file by direct
   `device_bash` sha256 + a single-match grep. Rows in rename_map.csv and bots_config_v2.csv.
2. Update the `bot-fleet-migration` tracker via `update_artifact`; ASK ANDY TO VISUALLY CONFIRM.
3. "Ready to commit" + the changed-files list. DO NOT COMMIT.
4. HAND-OFF FOR S2: per clone — built / partial / stopped and why; F-C1 applied or still gated;
   every toggle state with its screenshot filename; the capture hash; the rename_map row; the
   Layer-2 INVERTED check queued for Step 6; and every branch that fired, verbatim.
   ⛔ State plainly which of the four clones now have a signable config-capture hash. A bot whose
   hash is NOT ESTABLISHED cannot be signed at Step 2b, and a bot that is not signed stays OFF for
   the whole of Day-0.
   ⛔ ADDED 2026-08-07 (evening):
   - ⛔ ATTESTATION (A-18): state explicitly whether ANY of the nine leave-in-place bots was
     opened, edited, or had a toggle touched this session, BY NAME. "None" must be WRITTEN.
     Silence is not an attestation — S2 Step 2c's precondition is decided from this line.
   - the un-amended runbook §2 step 7 PT25 line (A-16b), listed as a doc-correction item for Andy
   - a `FLEET STAYS OFF` verdict, if one fired, in those words at the top of the hand-off (A-06)
```

---

## S2 — THE DAY-0 SEQUENCE, STEPS 0 → 8

**Model: Opus.** This is where judgment is real: the mechanism verdict that settles §1 either way,
the C10 unit read that exists exactly once, the DST verdict, and the three-mechanics-in-two-minutes
attribution. Each has a written decision tree, but reading which branch you are actually in is not
mechanical.
**Andy attended: YES, throughout.** Gates A6, A7, A8 are his and they sit in the middle of the
sequence.

```text
You are working in bot-fleet-v2 (~/bot-fleet-v2 via the device bridge). This is DAY-0's MAIN
SEQUENCE. S0 and S1 have run. Your job is to execute docs/reactivation-runbook.md §4, Steps 0
through 8, in order, and NOTHING ELSE.

⛔ PRECONDITION, ADDED 2026-08-07 (AMENDMENT A-06). READ S0's AND S1's CLOSE-OUTS IN THE FOLDER
FIRST. IF either records a `FLEET STAYS OFF` verdict, OR gate A0 landed on branch 2 or branch 3, OR
a close-out is missing or its hand-off block incomplete -> ⛔ DO NOT START. Record
`BLOCKED ON <session> — <verbatim branch>` and hand to Andy.

⛔⛔ SECOND PRECONDITION, ADDED 2026-08-07 AT ANDY'S RULING (AMENDMENT A-27c). **STEP 4b IS A NAMED
BLOCKER ON THIS SESSION'S OPENING AND IT IS UNRULED.** For 12 of the 14 bots in A-07's scope there
is NO per-bot capture file on disk, so an ESTABLISHED config-capture hash — which A-07 makes a
precondition for signing at STEP 2b — is unobtainable for them from the repository as it stands.
Three options are written out in A-27c and ANDY HAS CHOSEN NONE. ⛔ IF ANDY HAS NOT RULED IT BY
THE TIME YOU OPEN, DO NOT START: record `BLOCKED ON STEP 4b — A-27c UNRULED` and hand to him.
⛔ AND READ A-27a's CARRY-FORWARD BEFORE STEP 7: **the seven greenfield bots' EXIT OPTIONS state
MUST be re-read first-hand immediately before you switch AUTOMATIONS on, and NEVER inherited from
any close-out, CSV or this pack** — if a restore reset `disableExits` once it can reset again.
Re-reading is NOT re-doing Step 3. Cheapest instrument: the `/bots` list carries both toggles per
row on `i.sticon`'s `title` attribute, all 41 bots in one page read (A-27d).

⛔ READ `docs/day0-session-pack-2026-08-07.md` §0.0 — THE AMENDMENTS — BEFORE ANYTHING ELSE. Where
§0.0 and the text below conflict, §0.0 WINS. The ones that change this session: A-01 (gate A0) ·
A-02 (LEDGER_START is a GATED question at Step 1, not a copy) · A-04 (gate A8 is ONE item, not
three — G-12b is SIGNED and G-1′ is DECLINED) · A-09b (Step 2c is confounded by a restore) · A-10
(re-read the five positions; branch for gone-or-changed) · A-11 (the first-position exception has
no mechanism — do not invent one) · A-12 (do NOT put `dstop` on PR-20; and "contract count" is
undefined) · A-13 (A7 is 3/4) · A-17 · A-18 · A-19 · A-24 (Step 0's "do not pay" is spent).

⛔ YOU DO NOT RE-PLAN THIS. The runbook is 801 lines and it governs. Every check below carries an
explicit branch and there is no step that requires you to invent a remedy. Where a branch says
escalate, escalate and stop that thread. build-plan.md is under decision freeze and DAY-0 IS NOT A
BUILD DAY.

READ FIRST, FRESH, IN FULL:
  docs/state.md                           ⛔ IN FULL, AND FIRST (A-19 — it was missing from this
                                          list and you WRITE TO IT at close-out). The dated tail
                                          blocks: the 04:24 ET lockout · the F-C1/F-C2 rulings ·
                                          the "four open items closed" block (G-12b SIGNED, G-1′
                                          DECLINED) · the `OA REACTIVATED BUT ROSTER LOST`
                                          incident block and its branch.
  docs/rebuild-contingency-2026-08-07.md  ⛔ gate A0 routes here on branch 2/3; §4 DO-NOT-START.
  docs/reactivation-runbook.md            THE WHOLE FILE. §4 is not self-contained — the Pre-Day-0
                                          checklist at the foot is a set of PRECONDITIONS for it,
                                          and Step 4 does not re-assert them.
  docs/day0-session-pack-2026-08-07.md    §0, §1, and S0's + S1's hand-off blocks
  docs/session-log.md                     the S0 and S1 entries, in full
  docs/pre-registration-ledger.md         §2 (template), §4–§6 (entries), §7 (signing checklist),
                                          §8 (open items)
  docs/greenfield-family-spec.md          §8.3 (the A-series, A1 AMENDED), §9 (the seven DRAFT
                                          entries PR-14…PR-20 — this is where they live, NOT in
                                          the ledger), §12 (open items)
  docs/post-u1-package-2026-08-07.md      the two ruling slots, and §1.7's ready-to-paste PR-16 text
  docs/oa-ops-runbook.md                  §4 (edit verification), §4.3 (the inverted check)
  docs/decision-card-2026-08-06.md · docs/g-rulings-card-2026-08-07.md   the ruled sheets
  docs/mirror-funding-memo-2026-08-05.md  §1, §9 — for Step 2's mirror verdict
  docs/build-plan.md                      §2 — FROZEN
  project memory: greenfield-build-status, decision-card-2026-08-06, mirror-funding

=== STANDING FACTS — TRUE ALL SESSION ===
[Identical to S0's block. Reproduced verbatim so this prompt is self-contained.]
1. NEVER RUN GIT, in any form, INCLUDING `git status`. The bridge cannot unlink; git from this side
   strands .git/index.lock. Verify by direct `device_bash` sha256 + single-match grep. Never the
   write tool's response, never a stage-back read. ANDY RUNS EVERY COMMIT.
2. The ~04:20 ET 2026-08-07 lockout SUPERSEDED the old "inactive banner is cosmetic" finding.
   Sessions start LOGGED OUT; S0 reactivated the account — confirm from its close-out.
3. NOTES: DOUBLE-ESCAPE FROM THE FIRST WRITE (`&amp;lt;`); verify byte-exact, never the panel.
4. DECISION NODES: use `NOT`, never a rebuild. No move-node control exists.
5. PICKERS NO-OP on the already-displayed value. Force with a two-step; verify the STORED field.
6. CLICKING: refs silently no-op; JS dispatch is harness-blocked. Compute from the DOM:
   scale = screenshotWidth / window.innerWidth, click at rect.centre × scale. Never carry a
   coordinate across a resize.
7. `Runtime.evaluate` times out at ~45s WITH THE WORK COMMITTED — re-read, never re-fire. Titles
   commit on BLUR. `overlay.innerText` goes stale mid-animation. Prefer `form_input`; re-read
   `.value`. Tags store lowercased with non-alphanumerics as spaces. `a5.bots.bot` is the hydrated
   client model.
8. `archiveBot` / `showBotMenu` are ANDY'S HAND. Three attempts, then STOP. Never coordinates.
9. TWO-LAYER EDIT PROOF. Layer 1 = re-observe after a HARD RELOAD. Layer 2 = the first NEW
   position's Trades list. ⛔ THE EXIT OPTIONS PANEL IS NEVER EVIDENCE — exits are copied onto the
   position at open, so the panel shows intent and the Trades list shows what was attached. In v1
   the panel displayed `PROFIT % 50%` while the bot generated NO exit orders at all for four
   months. This has no exception.
10. WHEN IT IS AMBIGUOUS, IT IS GATED.

=== THE STOP LADDER + HOW TO READ §4 ===
Documented method -> ONE documented alternative -> third attempt max -> STOP. No forcing, no
coordinate fallback, no improvised remedy.
  "bot stays OFF"   -> that bot does not trade today. THE REST OF THE FLEET PROCEEDS.
  "fleet stays OFF" -> NOTHING ELSE IS SWITCHED ON TODAY. Stop the sequence and escalate.
  a check you could not run -> ⬜ NOT EVALUABLE. Write it down BY NAME. It is never a pass, and it
  is never reported as a negative result.
⚠️ THE STEPS ARE IN DEPENDENCY ORDER. DO NOT REORDER THEM. Several exist only because something
later cannot be read until they have run.

=== ⛔ ANDY'S GATES INSIDE THIS SEQUENCE ===
A6 (Step 2)  — the ride-or-close call on the 5 open mirror positions: DRAFTED, SIGNED, AND EXECUTED.
               A logged call is not a disposition. Capital decision; go-live authority is Andy's.
A7 (Step 2b) — every pre-registration signature. "Andy signs and dates. Only then may the bot be
               switched ON."
A8 (Step 2b) — the three open signature items (see Step 2b below).
Ask for each explicitly and WAIT. Do not proceed past a gate on your own reading of it.

────────────────────────────────────────────────────────────────
STEP 0 — CLOSE THE PRE-DAY-0 CHECKLIST. NOTHING IN §4 STARTS UNTIL IT IS CLOSED.
────────────────────────────────────────────────────────────────
⛔ AMENDED 2026-08-07 (A-24): AS WRITTEN THIS STEP DEADLOCKS. It says "IF ANY ⛔ HARD BLOCKER BOX IS
UNTICKED -> DO NOT PAY, DO NOT RE-ARM" and then lists THREE ⛔ boxes as known-unticked (Template V2
on the pilot · C9 · A7 wired into daily.sh). AND THE "DO NOT PAY" HALF IS SPENT — payment happened
2026-08-07 (gate A1, A-02). IT IS NOT AN INSTRUCTION.
⛔ THE THREE KNOWN-UNTICKED BOXES ARE ANDY'S RULING HERE, ONE AT A TIME, ASKED EXPLICITLY — not a
silent proceed and not an automatic halt: Template V2 is finished here OR THE PILOT STAYS OFF; C9
is run AS A READ before switch-on OR THE FAMILY STAYS OFF; A7-unwired is reported and ANDY RULES
whether the family trades today with no nightly detector (wiring it is Claude Code's lane).
⛔ ANY OTHER unticked ⛔ box is an unqualified STOP. ⛔ Do not resolve any of them yourself.
[Original Step 0 text follows, left standing.]
The checklist is at the foot of the runbook. Confirm EACH BOX BY READING THE ARTIFACT ITSELF, never
from a memory of a prior session and never from another document's claim about it.
⛔ IF ANY ⛔ HARD BLOCKER BOX IS UNTICKED -> DO NOT PAY, DO NOT RE-ARM. ESCALATE TO ANDY: YES.
Blocker classes: ⛔ HARD (§4 does not start) · ⚠️ PER-BOT (blocks only the bots it names) ·
📝 ADVISORY (proceed; log and carry as an open card).

Known state entering this session — VERIFY each, do not assume:
  ✅ `itmlive` = `market` — S0 Step 2. `itmpaper` was already `market`; do not re-set it.
  ✅ `data/mirror_baseline.csv` — written 2026-08-04, 10 rows / 174 positions. An ANCHOR: do not
     recompute it, do not pass `--force`.
  ✅ Pilot ritual complete + declared clean by Andy 2026-08-06; `rename_map.csv` started.
  ❓ `LEDGER_START` — Step 1 below.
  ❓ `data/raw/` + `data/brief/` pre-cutover files resolved — S0 reported them empty.
  ✅ RESOLVED 2026-08-07 (Andy's ruling), AND NOT BY THEM BEING EMPTY. `data/brief/` is empty;
     `data/raw/` holds the filed export `2026-08-07.csv` and ⛔ STAYS. The box is satisfied by the
     LEDGER COUNTS — 1,386 export rows -> 0 post-cutover, 1,386 discarded, n=0, first-hand.
  ❌ `daily.sh` n=0 dry run — RUN BY ANDY 2026-08-07. **GATE A9 FAILED AT STAGE 3.**
     Stages 1 and 2 PASSED; `execution_audit.py` raises `KeyError: 'bot'` on
     `data/bots_config_v2.csv`. ⛔ IT IS A SCRIPT DEFECT AND IT IS QUEUED TO CLAUDE CODE —
     ⛔ DO NOT RESHAPE THE CSV. Full diagnosis and the fix constraints: `state.md` and
     `session-log.md`, 2026-08-07. **Day-0's §4 does not start until a clean end-to-end n=0 run
     is on file, so this blocker is still OPEN.**
     [Original line left standing:] ⛔ HARD BLOCKER. Read the output against
     runbook §3 Step E's branches: a script that raises -> FIX THE SCRIPT, NEVER THE DATA, and
     NEVER seed a synthetic row to make it pass. `0.0%` expectancy / a flat R / a populated-looking
     table at n=0 is a FAILURE, not a pass — an absent number is not a zero. Tier C reporting
     SKIPPED because bots_config_v2.csv is incomplete is CORRECT — silence in its place is the
     failure. Do not set LESSONS_ALLOW_TRUNCATE=1 to make a shrink guard pass.
  ❓ ⛔ TEMPLATE V2 ON THE PILOT, with its AMENDED PR-03 signed. Ruled 2026-08-04, execution
     deferred as part of the ruling. Re-price the 15:50 Expiration exit OFF Market -> SmartPricing,
     internal value `speedy`, ⛔ NOT `fast` (a capture parser keying on "fast" silently misses it).
     THE 15:52 BACKSTOP KEEPS MARKET. This is a SPEC CHANGE, not a config tweak: it lands as
     Template V2 with an amended pre-registration, never as a quiet edit, and the amendment and the
     signature happen together. ⚠️ WITHOUT V2 THE THREE 15:50–15:52 MECHANICS ARE INDISTINGUISHABLE
     — three Market orders in two minutes with only memo strings between them (see Step 6).
  ❓ Sizing written down: 1 lot experiments · ≈$5K risk/position CANDIDATE+ · IDENTICAL allocation
     across tournament arms. SET ONCE, HERE. If it is not written down before Step 3 it will be set
     mid-sample.
  ❓ Ride-or-close prepared, signed, ready to EXECUTE — Step 2.
  ❓ Every pre-registration entry SIGNED — Step 2b.
  ❓ Phase 0: `C0c · C2 · C7 · C8` are CLOSED (decision card 2026-08-06). ⛔ `C9` is RE-SCOPED TO A
     DAY-0 PRE-SWITCH-ON READ and is still open. `C10` is open and blocks ARM-B1 — observed at
     Step 6b, not before. ⛔ C7 and C8 carry their own STOP; C8's verbatim: "Do NOT substitute
     position age — that is the literal substitution that cost −$15,376."
  ⭐ A-26: run `python3 scripts/a_series.py --validate` before you read any A-series verdict this
     session, and `--json` for the close-out. ⛔ It is STANDALONE and does NOT wire itself into
     daily.sh — the gate below is unchanged.
  ❓ ⛔ A7 BASELINES + A7 WIRED INTO `daily.sh`. The baselines ARE recorded in bots_config_v2.csv;
     A7 IS NOT WIRED INTO daily.sh (its eight stages carry execution_audit.py and no A-series
     runner). Under Architecture E the three automations are shared across seven bots, so one edit
     changes all seven at once with no template version bump and a mis-built gate fails IDENTICALLY
     on all seven — which the arms cannot detect by diffing each other. A7 IS THE ONLY DETECTOR.
     ⛔ No baseline and no detector before Day-0 = no detector for the whole sample. Report the
     gate state plainly to Andy; wiring it is Claude Code's lane, not yours.

────────────────────────────────────────────────────────────────
STEP 0a — `itmlive` = `market`. Already done in S0. VERIFY, do not re-do.
────────────────────────────────────────────────────────────────
Re-read `input.value` after a hard reload and confirm S0's screenshots are on file.
⛔ IF IT DID NOT PERSIST -> NO CAPITAL GOES LIVE. FLEET STAYS OFF. ESCALATE: YES.
⚠️ `market` is NOT a substitute for the 15:52 flat-close backstop — it reaches only EXPIRING ITM
positions on expiration day. Do not let the two be conflated later.

────────────────────────────────────────────────────────────────
STEP 1 — LEDGER_START
────────────────────────────────────────────────────────────────
⛔ AMENDED 2026-08-07 (A-02): `LEDGER_START` IS A GATED QUESTION, NOT A COPY. Payment was
2026-08-07 and the roster did not exist that day — a LEDGER_START of the payment date claims an era
in which the account held zero bots. ASK ANDY whether the era starts at the payment timestamp or at
the first day a bot is actually switched ON, record his answer VERBATIM, and only then set it.
⛔ DO NOT CHOOSE. Everything else in this step — set it, run build_ledger.py, require row count 0
and EMPTY LEDGER n=0 — is unchanged and still binding.
[Original Step 1 text follows, left standing.]
S0 recorded the exact payment timestamp. THAT DATE IS `LEDGER_START`. Set it in
`scripts/build_ledger.py` before anything else, so no pre-cutover row can enter the working ledger.
⛔ VERIFY IT, DO NOT ASSUME IT. Run `build_ledger.py` once and confirm the row count is 0 and the
status reads EMPTY LEDGER, n=0. (`data/ledger_meta.json` currently reads
`"ledger_start": "2099-01-01"` — the refuse-everything sentinel, correct pre-Day-0 and NOT the
value to keep.)
⛔ IF THE LEDGER RETURNS ANY ROW -> a pre-cutover row has entered. STOP. NOTHING IS RE-ARMED. FLEET
STAYS OFF. ESCALATE: YES. Every downstream number would be cross-era.
⚠️ THE STRADDLE RULE: a position's era is its OPEN date. Pre-cutover positions resolve into the
MIRROR BASELINE layer, never the working ledger.

────────────────────────────────────────────────────────────────
STEP 2 — RIDE OR CLOSE, on the 5 open mirror positions. ⛔ ANDY'S GATE A6.
────────────────────────────────────────────────────────────────
⛔ AMENDED 2026-08-07 (A-10). BEFORE EITHER BRANCH, TWO THINGS THE STEP AS WRITTEN DOES NOT DO:
(1) RE-READ ALL FIVE POSITIONS FIRST-HAND — quantity, open date, current mark, unrealized P/L. The
numbers below are from the 2026-07-30 capture and are NOT current; do not put a stale number in
front of Andy at a capital gate.
(2) OPEN EACH POSITION'S OWN EXIT OPTIONS SCREEN AND SCREENSHOT IT. That per-position screen is the
THIRD toggle surface, it has never been observed on a lapse-surviving position (Step 3's own rider
says so), and A CLOSE DESTROYS IT PERMANENTLY. Reading and screenshotting a position is not toggle
intervention.
⛔ BRANCH — FEWER THAN FIVE SURVIVED THE 2026-08-07 ROSTER LOSS, OR ANY POSITION MATERIALLY CHANGED
-> the outcome was FORCED BY THE INCIDENT, NOT CHOSEN BY ANDY, and the step's completion condition
("EXECUTED FOR ALL FIVE") is otherwise unsatisfiable and deadlocks the sequence. Record
`RIDE-OR-CLOSE MOOTED BY THE 2026-08-07 ROSTER LOSS` in the ledger entry AND in state.md, naming
which survived and which did not, get Andy's explicit acknowledgment of that record, and only then
proceed to Step 2b. A forced outcome recorded as a decision is a record that lies.
[Original Step 2 text follows, left standing.]
`QQQ long call` ×4 (~$13K risk, ~−$10.8K unrealized) and `Tasty Condor` ×1 (~+$328), open at the
2026-07-30 capture and still open. An unmanaged legacy position is exactly the quiet exposure that
survives a clean-slate rebuild and then surprises someone.
⛔ THE DECISION IS NOT COMPLETE UNTIL IT IS EXECUTED AND RE-OBSERVED. A logged call is not a
disposition. Before Step 3 touches any toggle:
1. ⚠️ DRAFT AND SIGN THE LEDGER ENTRY FIRST. `pre-registration-ledger.md` §8 item 5 records that
   this entry "is not yet drafted" — THERE IS NO PLACE TO WRITE THE REASON UNTIL IT EXISTS.
2. CLOSE -> close the positions now, then re-read the TRADES LIST and confirm the closing rows are
   there. A save confirmation is not evidence.
3. RIDE -> the ride must survive Step 3. Turning EXIT OPTIONS ON for `QQQ long call` or
   `Tasty Condor` re-arms EVERY exit on that bot at once and CAN CLOSE A RIDDEN POSITION WITHIN
   MINUTES OF REACTIVATION. Before flipping either toggle, read that bot's Exit Options and record
   what would fire. If anything would act on the five positions against the decision, LEAVE THAT
   BOT'S EXIT OPTIONS OFF until the positions are closed or the exits are removed.
4. ⚠️ MIRROR FUNDING DOES NOT GATE THIS AND IS NOT DECIDED TODAY. ZERO OF TEN MIRRORS CLEARS THE
   EVIDENCE BAR AND NONE CAN BEFORE LATE OCT 2026. The Day-0 mirror action is RE-ARM, WATCH-ONLY,
   SIZE NOTHING. ⛔ Do not read "insufficient evidence" as "do nothing" — for a RUNNING bot that
   means CONTINUE, which is a capital decision made by default. SAY THE VERDICT OUT LOUD IN THE LOG.
⛔ IF THE CALL HAS NOT BEEN MADE, SIGNED AND EXECUTED FOR ALL FIVE -> DO NOT PROCEED TO STEP 3. NO
BOT IS RE-ARMED. ESCALATE: YES.

────────────────────────────────────────────────────────────────
STEP 2b — SIGNING. ⛔ ANDY'S GATES A7 + A8. NO TOGGLE IS TOUCHED UNTIL THIS IS COMPLETE.
────────────────────────────────────────────────────────────────
Run `pre-registration-ledger.md` §7's six-item checklist for EVERY BOT THAT WILL BE ON TODAY:
config hash from the bot's OWN capture file · every `<placeholder>` and `TBD` resolved · kill
criterion re-read against the daily loop (does the loop actually produce that number?) · max-loss
line filled · ANDY SIGNS AND DATES · verification artifact identified.

THE SIGNING SET — 20 plan bots plus the ride-or-close entry:
  Group B, 4 clones — ledger §4:
    PR-01 `IC-SPX-FastPT25-S2` · PR-02 `-130PM` · PR-03 `QQQ-IC-0DTE-Fortress` (pilot — ⛔ ITS
    AMENDED ENTRY AND ITS SIGNATURE HAPPEN TOGETHER, with Template V2) · PR-04 `-NoPT50`
  Group C, 9 untouched — ledger §5:
    PR-05 `DIR-SPX-PutVIX22-SL75` · PR-06 `DIR-SPX-CallVIXdrop` · PR-07…PR-13, the seven mirrors
    (3DTE $140-$350 · Nigiri-Paper-v1 · QQQ long call · Friday 14 DTE Broken Wing IB (B-70) ·
    Trendy-Paper-v1 · 60min-ORB-10W-Paper-v1 · Tasty Condor)
    ⛔ THE LEDGER NAMES THE NINE EXPLICITLY BECAUSE THEY ARE THE GROUP MOST LIKELY TO BE WAVED
    THROUGH AS "UNTOUCHED". A bot whose entry is unsigned stays OFF for the whole of Day-0. No
    exceptions, including the nine.
  Group D, 7 fresh — ⚠️ THEIR ENTRIES LIVE IN `greenfield-family-spec.md` §9, NOT in the ledger:
    PR-14 Ride (control) · PR-15 PT50 · PR-16 Trail · PR-17 Touch0 · PR-18 SL100 · PR-19 SL200 ·
    PR-20 Canary
  Plus the ride-or-close entry from Step 2.
  ⛔ NOT IN THE SIGNING SET: PR-21 / PR-22 (Track B) are DRAFT and unsigned, and ARM-B1 is not an
  arm until C10/C11 close. They are not switched on today. Do not sign them to be tidy.

⛔ AMENDED 2026-08-07 (A-04): GATE A8 IS **ONE** OPEN ITEM, NOT THREE. state.md's dated block
"📝 RULED 2026-08-07 (Andy) — four open items closed" records: **G-12b — SIGNED AS DRAFTED**
(δ=0.10R, p=0.20, floor n_matched_days≥100 + one re-arm at Day-0+9mo, INSIDE the family correction,
publication cap acknowledged; exact ledger text already pasted into pre-registration-ledger.md's
PR-14…PR-17 entry, scoped to PR-16) and **G-1′ — DECLINED**.
⛔ ITEM (i) IS SIGNED — DO NOT RE-PRESENT `[ 0.10 | other ]` TO ANDY. Any answer that is not a
verbatim repeat silently forks a signed pre-registration. VERIFY the pasted text is in the ledger
and move on.
⛔ ITEM (iii) IS DECLINED — do not re-open it. Its two ruling-reopeners are already carried
correctly at this session's close-out item 4.
✅ ITEM (ii), PR-18's "Breakeven" naming, IS STILL OPEN AND STILL ANDY'S — it is the WHOLE of gate
A8. Ask; do not choose.
[Original text follows, left standing.]
⛔ THREE OPEN SIGNATURE ITEMS — ANDY'S GATE A8. Under §7 item 2 an entry with an unresolved field
is UNSIGNED, so each of these blocks a signature until it is ruled:

  (i) PR-16's TAIL RETIREMENT CRITERION — ruling slot G-12b.
      G-12 was ruled RESPEC (Andy, 2026-08-06): the worst-condor coin-flip test is STRUCK and the
      replacement was deliberately NOT invented by the applying session. ⛔ DO NOT INVENT ONE.
      `docs/post-u1-package-2026-08-07.md` §1 drafts it and §1.7 carries the EXACT ledger text
      ready to paste. Three constants need Andy's signature:
        S1  delta = 0.10 R per condor, on the tail set T   [ 0.10 | other ]
            ⚠️ A NEW MARGIN. The transport-from-R-3 argument was REFUTED in adversarial review and
            WITHDRAWN — delta carries no inherited authority and stands only on this signature.
        S2  p = 0.20 (tail fraction; m = ceil(p·n))         [ 0.20 | other ]
        S3  floor = n_matched_days >= 100, plus ONE re-arm at Day-0 + 9 months   [ as stated | other ]
      Plus: family membership [ INSIDE the family correction (recommended) | uncorrected one-sided
      5% ] and an acknowledgment of the standing publication cap.
      ⚠️ Until this is signed, the engine keeps emitting `worst_r_*` annotated `no_inference`.
      ⚠️ Whatever is ruled, the verdict carries `CF1_PUBLICATION_PRECONDITION: UNMET` while G-1 is
      on HOLD, and Refusal R-6 stands: no verdict while `pnl_may_be_modelled == true`.

  (ii) PR-18's NAME — "Breakeven", or not. Sandvand's rung is called Breakeven because stopping the
      tested spread at 100% of credit leaves the UNTESTED side to decay to zero, netting ≈$0 on the
      condor. The C8 ruling removed sibling-close, so the untested side IS left to decay and the
      construction objection is GONE — CF-4 is discharged and the arm CAN now reach Breakeven. The
      name is withheld PENDING ANDY'S READ OF HOW IT SHOULD BE PUBLISHED. The decision card records
      it explicitly as ANDY'S CALL AT DAY-0 SIGNING, not before. Ask; do not choose.

  (iii) G-1′ — `exit_rows.csv` under the degraded schema. U-1 came back NEGATIVE (Trades-list rows
      carry no per-row pricing-mode label and no memo field), so G-1 reverted to HOLD and the
      question re-presents. `post-u1-package-2026-08-07.md` §4: [ AUTHORIZE-DEGRADED | DECLINE |
      DEFER ], recommendation DECLINE plus two ~5-minute Day-0 checks — D3 (export timezone) and
      the Automation Log link's target. ⚠️ NO OPTION HERE MAKES CF-1's PUBLICATION PRECONDITION
      MEETABLE; the acknowledgment is part of the ruling.

⚠️ SIGNED ≠ VERIFIED. Signing does not satisfy Step 6.

────────────────────────────────────────────────────────────────
STEP 2c — ⭐ THE NO-TOUCH OBSERVATION. BEFORE ANY TOGGLE IS MOVED.
────────────────────────────────────────────────────────────────
⛔ AMENDED 2026-08-07 (A-09b): IF THE ROSTER WAS RESTORED BY OA RATHER THAN SURVIVING INTACT, THIS
OBSERVATION IS CONFOUNDED BY THE RESTORE. A restored bot's toggle state is whatever the snapshot or
OA's restore default carries; it cannot separate billing-state from hand-set. Record
`NO-TOUCH OBSERVATION CONFOUNDED — RESTORE`, treat it as ⬜ NOT EVALUABLE, and say so INSIDE the
Step 6a verdict — a CONFIRMED verdict resting on it is weaker than it looks
(rebuild-contingency-2026-08-07.md §2 records the rebuild case as FORECLOSED, not delayed).
⚠️ S0 was amended (A-09a) to take READ-ONLY toggle screenshots on one live mirror and one
directional bot before anything else, because this information is spent by the TRANSITION, not by
the session that reaches it. Read those screenshots from S0's close-out and report both readings.
⛔ AMENDED (A-18): the precondition below — "confirm from their close-outs that they did" — is
decided from S0's and S1's ATTESTATION line. IF EITHER CLOSE-OUT LACKS IT -> record
`2c PRECONDITION UNVERIFIED`, run the observation anyway, and label the result NOT EVALUABLE in the
Step 6a verdict. ⛔ Never infer compliance from silence.
[Original Step 2c text follows, left standing.]
⛔ THIS IS FREE AND THE INFORMATION IS NOT RECOVERABLE AFTERWARDS. Day-0 is itself an
inactive→active transition. If exits resume at reactivation with NO toggle intervention, BILLING
STATE IS IMPLICATED as the June cause. Flip a toggle first and re-arm is confounded with
reactivation — the toggle candidate and the billing candidate become PERMANENTLY
INDISTINGUISHABLE, and §1's causal story stays unfalsifiable forever.

OBSERVE: read BOTH dashboard toggles on ONE live mirror and ONE directional bot, and SCREENSHOT
BOTH. Andy's pre-Day-0 state is both toggles OFF on every bot, so the question is whether either
now reads ON without anyone touching it.
- EITHER READS ON WITHOUT INTERVENTION -> ⭐ BILLING STATE IS IMPLICATED. Log it as a first-hand
  observation with the screenshot filename and the timestamp, REPORT TO ANDY BEFORE PROCEEDING, and
  carry it into the Step 6a verdict. Do not re-flip anything first.
- BOTH READ OFF ON BOTH BOTS -> the toggle candidate survives. RECORD IT VERBATIM ANYWAY — a
  confirmed expectation is evidence and an unrecorded one is not. Proceed.
- UNREADABLE -> ⚠️ an unread toggle is not an OFF toggle. Re-screenshot. Still unreadable -> record
  `NO-TOUCH OBSERVATION UNREAD` and say so at close-out. PROCEED — this does not gate the sequence,
  but a missing answer is never reported as a negative one.
⚠️ Step 0a's ACCOUNT-LEVEL `itmlive` is NOT toggle intervention. Nothing else may touch a bot before
this observation. S0 and S1 were both instructed to leave the nine alone for exactly this reason —
confirm from their close-outs that they did.

────────────────────────────────────────────────────────────────
STEP 3 — RE-ARM SWEEP: `EXIT OPTIONS` ONLY. The nine leave-in-place bots.
────────────────────────────────────────────────────────────────
⛔ DO NOT TURN `AUTOMATIONS` ON IN THIS STEP. Re-arming and authorizing entries are two different
acts and Step 7 is the gate between them. `AUTOMATIONS` ON *IS* THE ENTRY AUTHORIZATION: a bot
switched on here takes a position before Step 6 can prove it — which is the v1 failure (−$9,618)
reproduced on Day-0, with Step 7 gating nothing.

THE NINE: `DIR-SPX-PutVIX22-SL75` · `DIR-SPX-CallVIXdrop` · `3DTE $140-$350` · `Nigiri-Paper-v1` ·
`QQQ long call` · `Friday 14 DTE Broken Wing IB (B-70)` · `Trendy-Paper-v1` ·
`60min-ORB-10W-Paper-v1` · `Tasty Condor`.
For each: EXIT OPTIONS -> ON · AUTOMATIONS LEFT OFF · then screenshot BOTH toggles.
Nothing else needs re-arming — clones and fresh builds were born correct and the ~20 Group-A bots
are being archived.

⛔ THE NINE ARE NOT EXEMPT FROM STEP 6. This step scopes RE-ARMING, not VERIFICATION. A pre-existing
bot is not a proven bot — these nine are the ONLY bots that lived through the lapse, which makes
them the MOST in need of the check, not the least.

BRANCHES:
- TOGGLE NOT PRESENT ON THE DASHBOARD -> try the TWO OTHER DOCUMENTED SURFACES first: inside the
  bot, and individually within each position. ⚠️ A SURFACE YOU DID NOT OPEN IS NOT AN ABSENT
  CONTROL. All three absent -> the lapse mechanism is UNEXPLAINED, not solved. BOT STAYS OFF · the
  other eight proceed · ESCALATE: YES.
- TOGGLE REVERTS TO OFF, or the post-save screenshot reads OFF -> re-drive it ONCE via the full
  pointer sequence. Reverts a second time -> BOT STAYS OFF · fleet proceeds · ESCALATE: YES.
  ⛔ No coordinate fallback. ⚠️ This revert branch is a DRAFTED remedy, not a corpus-cited one — no
  observation of a reverting toggle exists. RECORD WHAT ACTUALLY HAPPENS.
- THREE OR MORE OF THE NINE WILL NOT HOLD ON -> ⛔ STOP THE SWEEP. FLEET STAYS OFF. ESCALATE: YES.
  §1's mechanism is falsified and Day-0 is not a checklist day.
⚠️ THE TOGGLE HAS THREE DOCUMENTED SURFACES AND THIS STEP TOUCHES ONE. On any position that was
open THROUGH the lapse — the five from Step 2 — READ THAT POSITION'S OWN EXIT OPTIONS STATE before
acting on it. This has never been observed on those five: it is an UNOPENED SCREEN, not a
known-good one.

────────────────────────────────────────────────────────────────
STEP 4 — CONFIRM THE BUILD WINDOW IS COMPLETE
────────────────────────────────────────────────────────────────
Every clone and fresh build has: a capture on file · a saved template AT ITS CURRENT RULED VERSION
(⚠️ THE PILOT REQUIRES V2, NOT V1) · a signed pre-registration entry · a `rename_map.csv` row.
Anything missing is finished now or ITS BOT STAYS OFF.
PLUS the two gates the four artifacts do not satisfy:
  (a) Phase 0 blocking checks CLOSED. C0c · C2 · C7 · C8 are closed; ⛔ C9 is still open as a Day-0
      pre-switch-on read. ⛔ IF ANY IS STILL UNANSWERED, THE FAMILY DOES NOT TRADE TODAY — those
      bots stay OFF and the checks are run AS READS, NEVER WRITES, before switch-on. DO NOT
      IMPROVISE A SPEC ON THE FLY. Fleet proceeds. Escalate: YES.
  ⭐ AMENDED (A-26): THE A-SERIES HAS A RUNNER — `python3 scripts/a_series.py` (`--validate` first,
      then `--json`). RUN IT; do not hand-derive the asserts or the hashes. ⛔ IT DOES NOT CLOSE
      THIS GATE: its own header reads "STANDALONE. NOT wired into scripts/daily.sh… this tool does
      not edit daily.sh" (`--emit-wiring` prints the snippet as a COMMENT). A RUNNER EXISTING IS
      NOT A NIGHTLY DETECTOR EXISTING — (b) below stays OPEN and stays Andy's call.
      ⛔ AND IT IS NAME-KEYED AND READS NO OA ID, so a green run CANNOT detect a rekeying restore —
      A-01c's manual ID/rid comparison is separate and still mandatory. A7 from the tool is 3/4
      (A-13): `Defang-Mon-S2-StrikeTouch` is not in its SHARED_AUTOMATIONS list.
  (b) A7 payload-hash baselines RECORDED and A7 WIRED INTO `daily.sh`. Baselines: recorded. Wiring:
      NOT DONE (see Step 0). ⛔ No detector before Day-0 = no detector for the whole sample.
      Report the state; the wiring is Claude Code's lane. Andy rules whether the family trades
      today without a nightly A7.

────────────────────────────────────────────────────────────────
STEP 5 — CAPTURE EVERYTHING, AND RESOLVE THE INPUT CHAIN
────────────────────────────────────────────────────────────────
Full bookmarklet sweep of /bots across the whole new roster, plus toggle screenshots.
⚠️ A /bots SWEEP IS NOT `bots_config_v2.csv`. It carries names and P/L and NO Exit Options values.
That file is written PER-BOT AS EACH BOT IS BUILT. Step 5 VERIFIES its rows are present and
current; it does not create them.
⛔ THE D-1 G2 RIDER APPLIES HERE, TWO HOPS DEEP. The saved action stores a REFERENCE, NOT VALUES:
`{"type":"input","input":"IN…","text":"<label>","oldValue":{…}}`. Every capture, capture-diff and
drift baseline must resolve action -> automation input -> BOT input and read THE INPUT OBJECT'S
VALUE. A CAPTURE THAT READS ONLY THE ACTION RECORDS THE INPUT'S NAME, SO EVERY ARM DIFFS AS
IDENTICAL AND THE TOURNAMENT IS UNDETECTABLY VOID. ⚠️ NEVER read `oldValue` as current config — it
is a stale pre-link snapshot. The control lives at: bot settings page -> the automation row's ⚙ Edit
Settings -> 🔗 -> `Bot Inputs`.
⛔ IF THE INPUT OBJECT'S VALUE CANNOT BE READ -> THE CAPTURE IS NOT A BASELINE. Do NOT record it as
one and do NOT fall back to `oldValue`. Mark those bots' config-capture hash NOT ESTABLISHED; their
entries CANNOT BE SIGNED. Those bots stay OFF · the rest of the fleet proceeds · escalate: YES.
⛔ ALSO CAPTURE /settings SEPARATELY — SEVEN ACCOUNT-LEVEL FIELDS THAT ARE IN NO /bots CAPTURE AND
OVERRIDE EVERY BOT: `itmlive` · `itmpaper` · `maxexits` · `scanstart` · `scanend` · `exitstart` ·
`exitend`. ⛔ `maxexits` is the dangerous one — a single switch that can cap EVERY bot's ability to
close, and a non-zero value reproduces the exact failure shape of the June lapse with nothing
per-bot to show for it. It read `0` = Unlimited on 2026-08-04 and again in S0. RECORD THE VALUE AND
MAKE IT A DRIFT-AUDIT ROW.
⛔ IF `Export Data` IS TAKEN WITH ANY BOT GROUP DESELECTED -> DISCARD IT. The export respects the
bot-group filter and a subset export rebuilds the ledger as a subset. Re-export with ALL GROUPS
SELECTED.
THEN CONFIRM THE COMPARATOR IS REAL: open one arm's row and one shared-object row and read the
DECODED BUNDLE and the A7 hash back. IF EITHER IS MISSING, the drift detector's Tier C is SKIPPED
and the daily loop runs config-blind — SAY SO IN THE BRIEF rather than reporting a green baseline.

────────────────────────────────────────────────────────────────
STEP 5a — ⛔ DST CHECK: does `ntime=1552` actually fire at 15:52 ET? (D3)
────────────────────────────────────────────────────────────────
WHY THIS IS A HARD GATE: one toggle kills every Exit Option on a bot at once, which is exactly why
the flat close lives in the Events class. IF IT FIRES AT 16:52 ET, THE FLEET HAS NO LAST-RESORT FLAT
CLOSE AT ALL — the single point of failure the design was built to remove.
The saved trigger serialises `startDate …T20:52:00.000Z` — 15:52 at UTC−5 (EST) but 16:52 ET in
August (EDT). It reproduces on ALL SIX arms (`2026-08-07T20:52:00.000Z`) and on PR-14. `ntime` is
the operative field and `startDate`'s time component may be a stamp only. NOBODY HAS OBSERVED WHICH.
DO NOT ASSUME.
OBSERVE, on the pilot's backstop automation, on the FIRST TRADING DAY THE BOT IS ON: bot Log tab ->
filter Type = `Event` -> find the backstop's run row -> read THAT ROW'S `title` ATTRIBUTE, NOT the
visible group header (the group header is unreliable; the `title` carries a year-bearing timestamp).
- `title` reads between 3:52PM and 3:56PM -> `ntime` is operative. ✅ DST CLOSED. Record the verbatim
  `title` string and the date. Proceed. (A minute or two of drift is expected — automations run on a
  distributed queue with no guaranteed slot.)
- `title` reads `4:5xPM`, OR THERE IS NO EVENT ROW FOR THE BACKSTOP THAT DAY -> ⛔ THE BACKSTOP IS
  DEAD UNDER DST. STOP. Every bot carrying it is now single-layer. ⛔ DO NOT RE-TIME THE TRIGGER
  YOURSELF — the minute is in build-plan.md §2B and §0 says do not improvise a change here on the
  day. Then: (1) set every affected bot's toggles OFF and record it; (2) emit an instruction card
  headed `DST-BACKSTOP-DEAD` naming every affected bot; (3) hand to Andy for an explicit "amend the
  plan". ENTRIES STAY BLOCKED FOR THOSE BOTS UNTIL ANDY RULES.
- LOG FILTER RETURNS NOTHING READABLE (chips render labels via CSS, so `innerText` on the filters is
  the empty string) -> ⚠️ DO NOT CONCLUDE "NO ROWS". Read the hidden inputs named `date`, `time`,
  `autotypes` directly, or take it to Andy as UNREAD. ⛔ AN UNREAD DST CHECK IS TREATED AS THE
  FAILURE BRANCH — those bots stay OFF.
⚠️ RE-RUN THIS EXACT CHECK on the first trading day after the November EST transition, whichever way
it resolves now.

────────────────────────────────────────────────────────────────
STEP 6 — ORDER-LEVEL VERIFICATION, PER BOT, BEFORE IT MAY TRADE
────────────────────────────────────────────────────────────────
⛔ AMENDED 2026-08-07 (A-11): THE FIRST-POSITION EXCEPTION HAS NO MECHANISM ANYWHERE IN THIS PACK
OR IN THE RUNBOOK. "Allowed exactly ONE position at 1 LOT" names no control: the only way to make a
position exist is AUTOMATIONS -> ON, which Step 3 forbids and Step 7 gates, and nothing caps the
bot at one (greenfield arms carry limits 2/2, the PR-01 clone 10/10).
⛔ DO NOT IMPROVISE IT AND DO NOT BATCH IT. Attempt the button test-fire first and record VERBATIM
whether the control exists. If it does not: STOP and put the mechanism to Andy as a GATED question
— changing a signed bot's position limit is a config change on a signed entry, and turning
AUTOMATIONS ON early is the exact act Step 3 forbids (the v1 −$9,618 failure, with Step 7 gating
nothing). Whatever he authorizes: ONE BOT AT A TIME, never a batch; screenshot every transition;
read the Trades list the moment the position opens.
⛔ IF ANDY IS NOT AVAILABLE TO RULE IT -> that bot's Step 6 is ⬜ NOT EVALUABLE and IT STAYS OFF.
Never spend a live position to route around an unanswered question.
⚠️ AND "TEST-FIRE UNAVAILABLE" IS NOT DECIDABLE FROM ONE SCREEN — Step 3's own rule applies here:
A SURFACE YOU DID NOT OPEN IS NOT AN ABSENT CONTROL. If no doc names where the test-fire lives,
that is ⬜ NOT EVALUABLE, not "unavailable".
[Original Step 6 text follows, left standing.]
Two acceptable proofs, in order of preference: BUTTON TEST-FIRE then read the resulting TRADES LIST;
or allow the bot ONE position — the first-position exception — and read it the moment it opens.
⚠️ THE FIRST-POSITION EXCEPTION, stated plainly because Steps 6 and 7 are otherwise circular: the
Trades list is the only order-level ground truth AND IT DOES NOT EXIST UNTIL A POSITION DOES. If the
test-fire is unavailable, the bot is allowed EXACTLY ONE position at 1 LOT, read the moment it opens.
The test-fire prohibition elsewhere is scoped to the INACTIVE-ACCOUNT BUILD WINDOW, not to Day-0.
⛔ THE EXIT OPTIONS PANEL IS NOT EVIDENCE. Exit Options are copied per-position at open; the panel
shows intent, the Trades list shows what was attached.

FOR THE TWO CONTROL CLONES (PR-01 `IC-SPX-FastPT25-S2`, PR-02 `-130PM`) THE CHECK IS INVERTED:
confirm their Trades lists show NO PT row and NO exit-trigger row, and that their S2 monitor IS
firing.
⚠️ THE INVERTED CHECK IS ADVISORY UNTIL D4 IS ANSWERED. Whether the account-level ITM action appears
in a Trades list, AND UNDER WHAT LABEL, IS UNOBSERVED. Until it is read, a mislabelled ITM close
READS AS A PT ROW and would kill a ride control on day one — taking the referent of every comparison
in the family with it. READ THE LABEL FIRST; FIRE THE RULE SECOND.
⚠️ AND: the inverted check only means anything if F-C1 was applied. If PT25 is still in either
control's Open actions, THE CHECK FAILS BY CONSTRUCTION — that is a known state, not a finding.
Confirm from S0's and S1's close-outs which applies.

BRANCHES:
- NO PT ROW AND/OR NO EXIT-TRIGGER ROW -> BOT STAYS OFF. Record as MECHANICS 🔴 RED with the
  trade_id. Then, in order: (a) re-observe both dashboard toggles by a FRESH screenshot; (b) re-read
  the Open Position action's Exit Options VALUES, NOT PRESENCE; (c) re-drive the toggle once. Fleet
  proceeds. Escalate: YES if it fails a second position.
- NO POSITION OPENS AT ALL -> ⬜ NOT EVALUABLE, WHICH IS NEVER A PASS. Bot stays OFF. Carry the open
  card forward.
- THREE OR MORE BOTS SHOW THE SAME MISSING ROW -> ⛔ STOP. FLEET STAYS OFF. ESCALATE: YES. This is
  the v1 failure repeating, not a per-bot defect.
- TEST-FIRE UNAVAILABLE OR UNREADABLE -> fall back to the first-position exception. ⛔ NEVER
  SUBSTITUTE THE EXIT OPTIONS PANEL. NO EXCEPTION.
- ⛔ THE INVERTED CHECK'S OWN BRANCH — AND THE GENERIC ONE IS THE WRONG ACTION HERE. If either
  control clone's Trades list shows a PT row or an exit-trigger row, THE RIDE+S2 CONTROL IS
  CONTAMINATED and the arm's comparison is VOID, NOT DELAYED. ⛔ DO NOT EDIT THE BOT TO REMOVE IT —
  CLAUDE.md §5 standing exception: "Do not 'fix' them, do not re-arm them." Capture the Trades list,
  screenshot the Open Position action. BOT STAYS OFF · fleet proceeds · ESCALATE: YES.
  If the S2 monitor shows NO firing -> BOT STAYS OFF · fleet proceeds · escalate: YES. Zero log rows
  is the liveness RED of Step 8. ⛔ DO NOT READ MONITOR SILENCE AS "RIDE BEHAVIOR INTACT."

⚠️ THREE MECHANICS NOW AIM AT THE SAME TWO MINUTES — ATTRIBUTE BEFORE YOU CONCLUDE. `itmpaper` =
`market` closes expiring ITM positions 10 minutes before the close = 15:50, THE SAME INSTANT as the
bot's own Expiration exit and two minutes before the 15:52 backstop. AN EXIT-OPTION ORDER STAYS LIVE
TWO MINUTES, so the 15:50 order is still working when the backstop fires. RECORD BOTH ROWS'
TIMESTAMPS AND ATTRIBUTE BY THE GAP, NOT THE ABSOLUTE MINUTE — automations run on a distributed
queue and the clock is jittered. Feed `time_exit` and `itm_action` to the detector as SEPARATE
config columns. ⚠️ After Template V2 lands the three are distinguishable BY PRICING — 15:50
Expiration on SmartPricing (`speedy`), ITM action Market, backstop Market-with-memo. WITHOUT V2 THEY
ARE THREE MARKET ORDERS IN TWO MINUTES WITH ONLY MEMO STRINGS BETWEEN THEM.

────────────────────────────────────────────────────────────────
STEP 6a — ⛔ MECHANISM VERDICT (D4). THIS IS THE STEP THAT SETTLES §1.
────────────────────────────────────────────────────────────────
Run ONCE, on THE NINE leave-in-place bots ONLY — the clones and fresh builds were never lapsed and
cannot test it. PRECONDITION: Step 3 done AND the bot has opened its first new position. Do not run
it earlier.
⚠️ WHAT IS AND IS NOT ESTABLISHED, going in: the toggle's EXISTENCE is documented + first-hand ×2.
The CAUSAL claim — that flipping it back ON re-arms exit-order generation, and that its being OFF is
what killed the June exits — is NOT ESTABLISHED. The independently ruled position is D-4: THE JUNE
CAUSE IS UNKNOWN. The Excessive Errors Failsafe is excluded as the June cause (zero June errors on
either Fortress bot; newest error Apr 16 2026 3:55PM) but the mechanism itself is real.

- TOGGLES READ ON *AND* THE TRADES LIST CONTAINS THE PT ROW AND THE EXIT-TRIGGER ROW ->
  ✅ MECHANISM CONFIRMED. Record per bot: name, screenshot filename, VERBATIM PT row text, date.
  Write the verdict into docs/state.md and retire the CAUSAL caveat BY CITING THIS OBSERVATION.
- TOGGLES READ ON *AND* THE TRADES LIST SHOWS NO PT ROW -> ⛔ MECHANISM REFUTED. FULL STOP — THIS IS
  NOT A PER-BOT PROBLEM. The Failsafe moves back into contention and the June cause is again UNKNOWN.
  Do ALL of the following before anything else:
    1. AUTOMATIONS OFF ON ALL NINE, screenshotted. Do not leave a bot opening positions it cannot
       exit.
    2. ⛔ DO NOT ALLOW ENTRIES ON THE CLONES OR FRESH BUILDS EITHER. They were built on the premise
       that a correct-from-birth exit stack cannot suffer this failure. THAT PREMISE IS NOW
       UNPROVEN. FLEET STAYS OFF.
    3. Check the competing mechanisms, IN ORDER, recording each answer verbatim: (a) bot Log ->
       `Errors` filter, read each row's `title` — any day at or above 10 ERRORS since re-arm?
       (b) /settings -> `maxexits` still 0/Unlimited? (c) /settings -> Bot Schedule
       `exitstart`/`exitend` — do the window bounds still admit the exit's stamped minute?
       (d) Bid-Ask Guard — was the spread wide at the stamped minute?
    4. Emit an instruction card headed `LAPSE-MECHANISM-REFUTED`, repeated at the top of every brief
       until closed, and hand to Andy. ⛔ DO NOT DIAGNOSE PAST THIS POINT AND DO NOT RE-ARM ANYTHING.
       The cause is a research question, not a Day-0 step.
- NO POSITION HAS OPENED YET ON A BOT -> that bot is UNTESTED, NOT PASSING. ⬜ Do not count an
  untested bot as a confirmation.
- TOGGLE STATE UNREADABLE -> ⚠️ absence of a readable toggle is not an observation. Re-screenshot;
  still unreadable -> that bot is UNTESTED and STAYS OFF.
⚠️ FEED STEP 2c's RESULT INTO THIS VERDICT. If a toggle read ON without intervention at Step 2c, then
re-arm and reactivation were NEVER CLEANLY SEPARATED for that bot, and a CONFIRMED verdict on it is
WEAKER THAN IT LOOKS. SAY SO.

────────────────────────────────────────────────────────────────
STEP 6b — 📝 C10 OBSERVATION: the unit of `dstop` (Stop Loss $)
────────────────────────────────────────────────────────────────
AN OBSERVATION, NOT A BUILD. Nothing is re-stamped on Day-0 either way — Andy re-stamps PR-21.
⛔ WHY IT NEEDS ITS OWN STEP: C10 cannot be read off the modal. It is headed `Stop Loss Amount`, the
only unit marker is a bare `$`, `step=1`, and there is NO per-contract / per-position / per-leg
qualifier anywhere on it. It needs a LIVE POSITION WHOSE CONTRACT COUNT YOU WROTE DOWN BEFORE IT
OPENED. THAT MOMENT EXISTS EXACTLY ONCE. DO NOT LET IT PASS UNRECORDED.
⛔ AMENDED 2026-08-07 (A-12) — TWO DEFECTS IN THE SET-UP BELOW.
(a) PR-20 IS A SIGNED TOURNAMENT ARM. Its whole mechanic is `profits 0.05` + `smprofits speedy`.
Adding `dstop` to it after Step 2b signs its config falsifies A1 (two mechanics vs the control),
falsifies A3 — "the load-bearing one" — and voids the config hash its signature cites; a later
A-series run then reports a red that Step 4's branch escalates as FLEET STAYS OFF for the family,
over an edit this pack ordered. And `profits 0.05` will usually close the position before any
`dstop` can fire. ⛔ DO NOT EDIT A SIGNED ARM TO CLOSE AN OBSERVATION, AND DAY-0 IS NOT A BUILD
DAY. PUT IT TO ANDY: run C10 on an instrument OUTSIDE the tournament, or leave C10 OPEN. If no such
instrument exists today, C10 STAYS OPEN — say so by name in state.md and at close-out; ARM-B1 stays
blocked, which is where it already is.
(b) "CONTRACT COUNT" IS UNDEFINED AND THE FIRST TWO BRANCHES CAN COLLAPSE. The step says record
CONTRACT COUNT PER LEG and then branches on −$100 × (CONTRACT COUNT): at 1 contract per leg those
are the same number and `FIRED AT NEITHER FIGURE` becomes unreachable. ⛔ IF C10 IS RUN AT ALL, the
discriminating quantity is TOTAL CONTRACTS ON THE POSITION (a 1-lot iron condor = 4), not per leg.
Record BOTH numbers before the position opens and state which one each branch is read against.
IF THE TWO CANDIDATE FIGURES ARE EQUAL FOR THE INSTRUMENT YOU ACTUALLY HAVE -> the read cannot
discriminate: report C10-UNRESOLVED, do NOT report C10 CLOSED, and do not fit a basis to one point.
[Original SET UP follows, left standing.]
SET UP: the 1-lot canary (PR-20) IS THE C10 INSTRUMENT — run it, and run it at EXACTLY 1 CONTRACT.
On the canary ONLY, set `dstop` to a round, unmistakable value (e.g. −100) and RECORD, BEFORE THE
POSITION OPENS: bot name, `dstop` as typed, and CONTRACT COUNT PER LEG.
- FIRED AT ≈ −$100 TOTAL ON THE POSITION -> PER POSITION. `<D100>` as specified by R-1 "in dollars"
  is on the correct basis; the PR-21 re-stamp is a formality. ✅ C10 CLOSED.
- FIRED AT ≈ −$100 × (CONTRACT COUNT) -> PER CONTRACT. ⛔ This is the D-6 units failure one layer up.
  (1) Emit a card headed `C10-PER-CONTRACT`; (2) state plainly that `<D100>` is off by the contract
  count and ARM-B1 MUST NOT BE BUILT until Andy re-derives the rung and re-stamps PR-21;
  (3) ⛔ DO NOT RE-DERIVE `<D100>` YOURSELF — the rung basis is signed ruling R-1 and changing it is
  a plan amendment. C10 CLOSED, ARM-B1 STILL BLOCKED.
- FIRED AT NEITHER FIGURE -> record realised P/L, contract count and leg count; report
  `C10-UNRESOLVED`. ARM-B1 stays blocked. DO NOT FIT A BASIS TO ONE DATA POINT.
- CANARY NOT RUN / STOP NEVER FIRES / COUNT NOT RECORDED FIRST -> ⚠️ C10 STAYS OPEN. SAY SO in
  docs/state.md and at close-out. ⛔ DO NOT INFER THE UNIT FROM `dstop` PERSISTING AS A NEGATIVE
  NUMBER — that is a sign convention and it is INADMISSIBLE as the answer.

⛔ ALSO DUE HERE, and it is easy to lose: TIER-2 CHECK §9 #5 is the last open item from the
2026-08-04 Tier-2 pass (seven of eight answered). Read it, record the answer verbatim, and if it
cannot be run say NOT EVALUABLE by name.

────────────────────────────────────────────────────────────────
STEP 7 — ONLY NOW ALLOW ENTRIES: `AUTOMATIONS` -> ON, PER BOT
────────────────────────────────────────────────────────────────
HARD GATE, NOT A PREFERENCE. A bot that cannot be proven stays OFF until it can.
FOR EACH BOT THAT PASSED STEP 6 — AND ONLY THOSE — set AUTOMATIONS -> ON and SCREENSHOT.
A BOT THAT DID NOT PASS STEP 6 DOES NOT GET THIS STEP, INCLUDING ANY OF THE NINE.
⛔ IF STEP 6a RETURNED MECHANISM REFUTED, NO BOT GETS THIS STEP. FLEET STAYS OFF.
⛔ A BOT WHOSE PRE-REGISTRATION IS UNSIGNED DOES NOT GET THIS STEP EITHER.
⚠️ THE STANDING EXCEPTION: the legacy champion (`IC-SPX-FastPT25-S2`) and its `-130PM` clone are
deliberately Exit-Option-free ride+S2 controls. Do not "fix" them and do not re-arm them.

────────────────────────────────────────────────────────────────
STEP 8 — DAY-1 MONITORING
────────────────────────────────────────────────────────────────
LIVENESS: every ON bot must show a position OR a scanner run in the capture window. OA bot logs
record NON-ACTIONS, so ZERO LOG ENTRIES = presumed OFF or Failsafe-tripped -> RED.
SAME-DAY ENGINE-DEATH CHECKS: the expired:closed ratio flip, and any position with `mfe_pct` ≥ its
declared PT and NO PT order.
⛔ WHAT RED DOES — A CARD IS A QUESTION, NOT AN ACTION. An instruction card is a notification with an
address. It is NOT a disposition. Each RED also carries one:
- ZERO LOG ENTRIES FOR AN ON BOT IN THE CAPTURE WINDOW -> the bot is SWITCHED OFF pending
  investigation (PR-05's liveness kill). Fleet proceeds. Escalate: NO on day 1; YES if unresolved
  after two sessions. ⚠️ DISTINGUISH THE WINDOWS: PR-05's KILL criterion is a 10-SESSION window;
  this Day-1 check is ONE capture window and switches the bot off TO BE RE-ARMED — it does not
  retire the bot. ⚠️ `SILENT_BOT` CAN NEVER BE RED FROM POSITION DATA ALONE — only the bot log
  closes it. If the log cannot be read the verdict is ⬜ NOT EVALUABLE, NEVER GREEN.
- `mfe_pct` ≥ DECLARED PT WITH NO PT ORDER, or the expired:closed ratio flips -> BOT STAYS OFF FROM
  THE NEXT SESSION until a Trades list proves the PT row exists. Fleet proceeds. Escalate: YES —
  this is the exact 2026-06 signature.
- `BACKSTOP_CAUGHT_IT` FIRES -> the Exit-Options side is dead even though nothing was lost that day.
  BOT STAYS OFF. Escalate: YES.
Any RED emits an instruction card, repeated at the top of every brief until closed.
⚠️ ASSERTS A4b AND A6 BECOME RUNNABLE TODAY and belong here: A4b (no arm shows a ledger day of
stop-outs within minutes of open with no `stoploss` in its config — the broken-input-link signature)
and A6 (every arm opened EXACTLY 1 contract per leg today — the $-risk sizing fallback silently
sizing 2 lots, and doing it on SOME arms only). Run both. Report the result.

=== CLOSE-OUT (CLAUDE.md §9.1 — mandatory, AFTER EACH STEP GROUP, not once at the end) ===
1. Append docs/session-log.md; update docs/state.md for every fact that changed — and the Step 6a
   verdict goes into state.md BY NAME whichever way it lands. Verify every edited file by direct
   `device_bash` sha256 + a single-match grep.
2. Update the `bot-fleet-migration` tracker via `update_artifact`; ASK ANDY TO VISUALLY CONFIRM.
3. "Ready to commit" + the changed-files list. DO NOT COMMIT.
4. ⛔ THE FIVE DEFERRED OBSERVATIONS, EACH REPORTED BY NAME WITH ITS ANSWER OR AS OPEN:
   no-touch (2c) · DST (5a) · the 15:50 attribution (6) · mechanism verdict (6a) · C10 `dstop` (6b).
   Plus Tier-2 §9 #5. ANY ONE LEFT UNREAD IS REPORTED AS OPEN, NEVER AS PASSED.
   📝 ADDED 2026-08-07 (G-1′ DECLINED, Andy) — two of the above are also RULING-REOPENERS
   for G-1′ (`post-u1-package-2026-08-07.md` §4.1, §4.6): if either resolves favorably it
   reopens the DECLINE on materially better terms and must be flagged back to Andy, not just
   logged.
     - DST (5a), export timezone — the SAME read as D3 above; no separate step. RULING-REOPENER:
       if the 15:52 backstop's own `close_date` confirms the export clock on day 1, that same
       reading also supports per-arm time-based exit attribution (§4.3).
     - THE AUTOMATION LOG LINK'S TARGET, for an Exit-Option close (~5 min, NOT a numbered step —
       run it opportunistically during Step 6 while a Trades-list row is open). Read one exit
       row's Automation Log link and record whether its target names the closing object (the
       Exit-Options bundle) or the automation that fired it. UNOBSERVED as of this ruling
       (§4.1: "It is not assumed anywhere below"). RULING-REOPENER: if it names the closing
       object, most of the `pricing_mode`/attribution loss in §4.1 reopens.
5. A per-bot ON/OFF table: every bot, its Step 6 verdict, its signature status, and — for every bot
   that is OFF — the named reason and what would close it.
```

---

## S3 — CLOSE-DOWN

**Model: Sonnet.** Records, tracker, hand-off. The one judgment call — whether an archive is safe —
is resolved by handing every archive click to Andy.
**Andy attended: yes, for gate A5** (the ~23 archive clicks) **and A10/A11.**

```text
You are working in bot-fleet-v2 (~/bot-fleet-v2 via the device bridge). Day-0's sequence has run
(S0, S1, S2). This is the CLOSE-DOWN session. Its job is to leave the folder in a state Andy can
commit in one command, get the ~23 archives done under Andy's hand, and hand Day-1 forward.

⛔ PRECONDITION, ADDED 2026-08-07 (AMENDMENT A-06). READ S0's, S1's AND S2's CLOSE-OUTS IN THE
FOLDER FIRST. IF any records a `FLEET STAYS OFF` verdict, OR gate A0 landed on branch 2 or branch
3, OR a close-out is missing -> ⛔ DO NOT RUN TASK 1 (the archive sweep). Archiving against an
unexplained roster is irreversible from this side. Do Tasks 2–5 (the records, the tracker, the
commit hand-off, the Day-1 note) so the tree is committable, name the block, and hand to Andy.
⛔ READ `docs/day0-session-pack-2026-08-07.md` §0.0 — THE AMENDMENTS — BEFORE ANYTHING ELSE. Where
§0.0 and the text below conflict, §0.0 WINS. Relevant here: A-01 (gate A0; ⛔ branch 3f — a name
collision or an -ARCHIVED- name back on /bots is a FINDING, never resolved by archiving) · A-06 ·
A-14 (DOM-computed clicks are the documented method; the RAW-coordinate ban is absolute on the
`…` menu) · A-22 (the capture is Andy's hand) · A-25.
⛔ ADD TO THE READ LIST: `docs/state.md` (the dated tail blocks, incl. the incident block) and
`docs/rebuild-contingency-2026-08-07.md`.

⛔ THIS SESSION MAKES NO SPEC DECISION AND NO OA CONFIG EDIT. If you find something that wants
changing, record it and gate it.

READ FIRST, FRESH:
  docs/day0-session-pack-2026-08-07.md   §0, §1
  docs/session-log.md                     the S0, S1 and S2 entries, in full
  docs/state.md                           the Day-0 blocks S2 wrote
  docs/reactivation-runbook.md            §3 Step B (the sweep + its name-collision warning), §4
                                          Step 8, and the Pre-Day-0 checklist
  docs/build-plan.md                      §2 group A (the 20) and §2B (the 4 clone originals)
  docs/daily-loop-spec.md                 the three-verdict contract — Day-1 runs on it
  data/archive/rename_map.csv             every lineage row written so far

=== STANDING FACTS — TRUE ALL SESSION ===
[Identical to S0's block. Reproduced verbatim so this prompt is self-contained.]
1. NEVER RUN GIT, in any form, INCLUDING `git status`. The bridge cannot unlink; git from this side
   strands .git/index.lock and Andy removes it by hand. Verify files by direct `device_bash` sha256
   + a single-match grep. Never the write tool's response, never a stage-back read. ANDY RUNS EVERY
   COMMIT — and on this session that is the whole deliverable.
2. The ~04:20 ET 2026-08-07 lockout superseded the old banner finding; sessions start LOGGED OUT.
3. NOTES: DOUBLE-ESCAPE FROM THE FIRST WRITE; verify byte-exact, never the panel.
4. DECISION NODES: use `NOT`, never a rebuild.
5. PICKERS NO-OP on the already-displayed value; force with a two-step; verify the STORED field.
6. CLICKING: refs no-op; JS dispatch is harness-blocked. scale = screenshotWidth / innerWidth,
   click at rect.centre × scale. Never carry a coordinate across a resize.
7. `Runtime.evaluate` times out at ~45s WITH THE WORK COMMITTED — re-read, never re-fire.
8. ⛔ `archiveBot` IS ANDY'S HAND — 3-for-3 failed from this side, and this session is where that
   bites hardest. Three attempts, then STOP. ⛔ NEVER FALL BACK TO COORDINATES: `Delete` sits ~29px
   below `Archive`, and on the pilot's original a mis-landed click would have destroyed 41
   POSITIONS OF HISTORY.
9. TWO-LAYER EDIT PROOF; the Exit Options panel is never evidence.
10. WHEN IT IS AMBIGUOUS, IT IS GATED.

=== THE STOP LADDER ===
Documented method -> ONE documented alternative -> third attempt max -> STOP. No forcing, no
coordinate fallback, no improvised remedy. Record verbatim and escalate.

────────────────────────────────────────────────────────────────
TASK 1 — SUPPORT THE ARCHIVE SWEEP. ⛔ ANDY'S GATE A5. EVERY CLICK IS HIS.
────────────────────────────────────────────────────────────────
~23 archives: the 20 Group-A bots plus the 3 clone originals whose clones now hold the production
names (the pilot's original was archived 2026-08-04 and is already done).
YOUR JOB IS TO MAKE HIS CLICKS SAFE, NOT TO CLICK. For each, present: the EXACT full name, its bot
ID, and a one-line confirmation of what it is. Then read `/bots` back after each batch and confirm
the active-bot footer decremented by exactly the number archived.

THE 20 (build-plan.md §2A): `IC-SPX-Fortress-Unstopped` · `IC-SPX-Fortress-Defang` ·
`QQQ-IC-0DTE-Fortress-NoFilter` · `QQQ-IC-0DTE-Fortress-S2` · `QQQ-IC-0DTE-HedgeA-S1` ·
`-HedgeB-S2` · `-HedgeC-S3` · `-HedgeD-Conditional` · `-HedgeTest` · `QQQ-IC-0DTE-Baseline` ·
`-Raw-HoldToExp` · `-InverseFilter-HoldToExp` · `-VIX25-Range075-PT50` · `-Range075-PT50` ·
`-Range075-PT50-Wide2-155PM` · `-Range075-PT50-Wide2-1230PM` · `Weekly-IB-SPY-Paper-v1` ·
`1-45pm-Sandwich-Paper-v1` · `Opening Range Breakout 60m` · `DIR-SPX-Put-Control`.
THE 3 CLONE ORIGINALS: `IC-SPX-FastPT25-S2-ARCHIVED-2026-08-07` and the two S1 renamed this Day-0.

⛔ NAME-COLLISION WARNING — READ FULL NAMES BEFORE ANY ARCHIVE. `Opening Range Breakout 60m` IS
ARCHIVED. `60min-ORB-10W-Paper-v1` IS A DIFFERENT BOT AND STAYS LIVE — it is one of the nine.
⛔ `DIR-SPX-PutVIX22-SL75` IS ZERO-TRADE AND MUST NOT BE TOUCHED. Its VIX≥22 gate correctly never
fired in 22 days. EMPTY ≠ WORTHLESS, and it is in the leave-in-place group.
⛔ DELETE NOTHING. The two deletes (`TEST QQQ-IC-0DTE-HedgeC-S3 Clone`,
`QQQ-IC-0DTE-InvFilter-Wide150`) and the Library object `CLAUDE-C5-SHARED-SCRATCH` were all
executed 2026-08-06. There is nothing left to delete. If something looks like it needs deleting,
that is a finding, not a task.
VERIFY READ-ONLY afterwards, per bot: active-bot footer decremented by one · exactly one bot under
the production name · the `-ARCHIVED-` name no longer listed.
APPEND `data/archive/rename_map.csv` as you go — original_name, archived_as, clone_name, date,
disposition. It is the ONLY thing that will later connect a name in the frozen ledger to a bot
running today.
⛔ IF ANY ARCHIVE WILL NOT FIRE FROM ANDY'S CLICKS EITHER -> record it, leave the bot renamed, and
carry it forward. An un-archived renamed original is untidy; it is not a blocker. Renames are what
free the production names and they already committed.

────────────────────────────────────────────────────────────────
TASK 2 — THE RECORDS
────────────────────────────────────────────────────────────────
a. `data/bots_config_v2.csv` — one row per bot and per shared object, each citing its own capture
   file and hash. ⚠️ It is written PER-BOT AS EACH BOT IS BUILT, not as a big-bang extraction; this
   task VERIFIES completeness and currency. ⛔ Every row's config-capture hash must resolve the
   input chain two hops (action -> automation input -> BOT input, reading the INPUT OBJECT'S VALUE).
   A row whose hash is NOT ESTABLISHED must say so — its bot could not have been signed.
b. `data/archive/rename_map.csv` — complete for all four clones plus every Group-A archive.
c. `docs/state.md` — the Day-0 facts, current. Specifically: the roster after archiving, the Step 6a
   mechanism verdict, the DST verdict, the C10 verdict, `LEDGER_START`, `itmlive`, the seven
   account-level fields, and which bots are ON.
d. `docs/session-log.md` — a Day-0 entry per session, already appended by S0/S1/S2. Add the
   close-down entry.
e. ⛔ THE OPEN-ITEMS LIST, BY NAME. Everything still open at the end of Day-0: every bot that is OFF
   and why · every ⬜ NOT EVALUABLE check · the five deferred observations and Tier-2 §9 #5 with
   their verdicts or OPEN · the A7-not-wired-into-daily.sh gate · G-12b / PR-18 naming / G-1′ if
   any went unruled · Track B (PR-21/22 unsigned, ARM-B1 blocked on C10) · the post-downgrade
   backlog. ⛔ AN ABSENT NUMBER IS NOT A ZERO AND AN UNRUN CHECK IS NOT A PASS.
VERIFY EVERY EDITED FILE by direct `device_bash` sha256 + a single-match grep of the new text.

────────────────────────────────────────────────────────────────
TASK 3 — THE TRACKER. ⛔ ANDY'S GATE A10.
────────────────────────────────────────────────────────────────
Update the `bot-fleet-migration` tracker artifact via `update_artifact` so it matches the folder,
then ASK ANDY TO VISUALLY CONFIRM IT. ⛔ THE CLOSE-OUT IS NOT COMPLETE WITHOUT HIS CONFIRMATION —
`update_artifact` returning success is a claim, not evidence (CLAUDE.md §9.1a). This rule has failed
twice (7/29, 7/31). THE TRACKER IS THE ONE DASHBOARD ANDY READS; when it lags the folder it reports
finished work as missing and invites it to be done twice.

────────────────────────────────────────────────────────────────
TASK 4 — THE COMMIT HAND-OFF. ⛔ ANDY'S GATE A11.
────────────────────────────────────────────────────────────────
Say "READY TO COMMIT" with a one-line summary of every changed file. ⛔ DO NOT COMMIT — the bridge
cannot unlink files and git from this side strands lock files in `.git/`.
UNCOMMITTED WORK AT SESSION END IS UNFINISHED WORK. The folder is the only memory this project has;
an untracked folder cannot be diffed, reverted or trusted. Leave the tree in a state Andy can commit
in ONE command, and say so plainly.
⚠️ CHECK FOR THE PRE-DAY-0 STRAGGLERS TOO: as of 2026-08-07,
`docs/decision-card-2026-08-06.md` was modified and
`data/captures/2026-08-06-gfam/GF-Backstop-1552-FlatClose.txt` untracked. If they are still
uncommitted, name them.

────────────────────────────────────────────────────────────────
TASK 5 — HAND DAY-1 FORWARD
────────────────────────────────────────────────────────────────
Write the Day-1 opening note into the session log:
- WHICH BOTS ARE ON, by name, with each one's Step 6 verdict.
- THE DAILY LOOP resumes per `docs/daily-loop-spec.md`: capture (bookmarklet on /bots + Export Data,
  ⛔ ALL GROUPS SELECTED) -> `daily.sh` -> ledger -> tape -> DRIFT AUDIT -> the three verdicts,
  NEVER BLENDED -> an instruction card for any RED. NO FINDINGS is the expected common case.
- EVERY OPEN INSTRUCTION CARD, repeated at the top of every brief until closed.
- THE STEP 8 CHECKS that run tomorrow: liveness · expired:closed ratio flip · `mfe_pct` ≥ declared
  PT with no PT order · asserts A4b and A6.
- ⚠️ RE-RUN THE STEP 5a DST CHECK on the first trading day after the November EST transition,
  whichever way it resolved today.
- ⚠️ THE FIRST POST-CUTOVER TRADING DAY is when `STATUS.md` stops reading EMPTY LEDGER — n=0. Until
  then, an absent number is not a zero.

=== CLOSE-OUT ===
Same §9.1 sequence: session-log + state.md (sha-verified) -> tracker + Andy's visual confirmation ->
"ready to commit" + changed-files list. DO NOT COMMIT.
```

---

# §3 · SEQUENCING AND MODEL SUMMARY

| Session | Model | Andy attended | Runbook coverage | Ends when |
|---|---|---|---|---|
| **S0** Reactivation opening ⛔ **AMENDED — SPLIT IN TWO (A-23): S0a = gate A0 → Steps 1–4b → gate A4 → close-out; S0b = Steps 5–8, fresh chat** | **Sonnet** | Yes — **A0**, ~~A1~~ (spent), A2, ~~A3~~ (now verify-only), A4, A9, **A12** | gate A0; Step 0a; Step 1's timestamp; §3 Step B roster; the A-series; **new Step 4b** | Roster + A-series accepted, F-C1 applied, PR-01 finished |
| **S1** Clones | **Sonnet** | No, unless a branch fires | §2's nine steps ×2 (PR-02, PR-04) | Both clones built and verified, or stopped with a named branch |
| **S2** The sequence | **Opus** | **Yes, throughout** — A6, A7, A8 | §4 Steps 0 → 8, in order | Step 7 done per bot, Step 8 queued for Day-1 |
| **S3** Close-down | **Sonnet** | Yes — A5, A10, A11 | §3 Step B's archives; §4 Step 8's hand-off | Tree committable in one command, Day-1 handed forward |

**Why Opus only on S2.** S0, S1 and S3 execute checklists whose every branch is written. S2 carries
four reads where the branch you are in is not obvious from the surface: the mechanism verdict
(CONFIRMED vs REFUTED changes what the entire fleet is allowed to do), the C10 unit read (a moment
that exists exactly once and cannot be re-created), the DST verdict (an unread check is treated as
the failure branch, so "I couldn't read it" and "it failed" have to be distinguished carefully), and
the three-mechanics-in-two-minutes attribution. A Sonnet session at a STOP hands to Andy; Andy
re-opens it on Opus. That ladder is in §0.2 of every prompt.

**Close the chat between sessions.** Long OA sessions saturate and start dropping reads — every
2026-08 build session that ran past a natural boundary paid for it. Each prompt is written to be
pasted into a fresh chat against the previous session's written close-out.

---

# §4 · WHAT THIS PACK DOES NOT COVER

Named so nothing is assumed handled:

- **`daily.sh` at n=0** — Andy's terminal (gate A9). `tape.py` needs network; `device_bash` has none.
- **Wiring A7 into `daily.sh`** — Claude Code's lane (`CLAUDE.md` §7). Runbook Step 4(b) requires
  it; it is not done, and S0/S2 report it as an open gate rather than closing it.
  ⭐ **UPDATED 2026-08-07 (evening), A-26: the A-series RUNNER now exists —
  `python3 scripts/a_series.py`, and Day-0 sessions run it instead of hand-deriving the asserts.
  ⛔ IT IS STILL STANDALONE AND STILL NOT WIRED INTO `daily.sh`** (its own header says so;
  `--emit-wiring` prints the snippet as a comment and edits nothing). **A runner existing is not a
  nightly detector existing — this row stays open.**
- **The comparative machinery implementation** and `research_loop.py`'s D-1…D-17 fixes — Claude
  Code, post-downgrade, with the two G-10 constraints from `post-u1-package-2026-08-07.md` §2
  (the max-T restatement must not silently undo G-10; the family region needs a per-member
  direction vector declared pre-data). ⛔ `research_loop.py` is 0.1.0-DRAFT with three fatal
  defects — DO NOT WIRE IN until its fixtures pass.
- **Track B** — PR-21/PR-22 unsigned, ARM-B1 blocked on C10. Nothing is switched on for Track B on
  Day-0. Wave 1 is 22 of 50; ceiling 28.
- **`post-u1-package-2026-08-07.md` §10's seven gated items** and the post-downgrade backlog
  generally.
- **The pilot's Bot Group** (runbook §3 Step A / audit F-21) — small, and it belongs to whichever
  session is on the pilot when Template V2 lands.
- **Mirror funding.** Zero of ten mirrors clears the bar and none can before late Oct 2026. The
  Day-0 action is re-arm, watch-only, size nothing. It is not a Day-0 decision and this pack does
  not open it.

---

# §5 · ⛔ RUNBOOK-LEVEL FINDINGS — FLAGGED, NOT FIXED (added 2026-08-07 evening)

`docs/reactivation-runbook.md` is a decision surface and amending it needs Andy's explicit *"amend
the plan"*. The adversarial review found four defects that live **in the runbook**, not here. Each
is carried with a pack-side guard (named), and each needs Andy's ruling to close properly.

| # | Runbook location | Defect | Pack-side guard |
|---|---|---|---|
| **R-1** | §2 step 7 | Still carries the pre-ruling branch *"IF PT25 is still present on a control clone's Open Position action → do not remove it yourself … escalate"*. Never amended for **F-C1 RULED: REMOVE** (2026-08-07). A session told to read §2 "IN FULL" hits a direct countermand mid-clone. | A-16b |
| **R-2** | §2's numbering | §2 clones at step 1 and renames at step 8; the learned order (baseline → rename → clone) is the opposite, and the pack asserts it "re-orders nothing". Also: §2 step 3 documents **three** clone traps; Trap 10 (F-C2) makes four. | A-16a, A-17 |
| **R-3** | §4 Step 6 | The **first-position exception** names no mechanism. The only way to open a position is `AUTOMATIONS` → ON, which Step 3 forbids and Step 7 gates, and nothing caps the bot at one. | A-11 |
| **R-4** | §4 Step 6b | *"run it at exactly 1 contract"* with branches on `−$100` vs `−$100 × (contract count)` — at 1 contract **per leg** those are the same number, so the read cannot discriminate as specified. And the runbook's instrument is §3 Step C's *optional* canary; treating a signed tournament arm as that instrument breaks A1/A3. | A-12 |

⚠️ **Also runbook-level and unresolved by either document:** the Pre-Day-0 checklist says *"do not
pay while any ⛔ box is unticked"*, and payment has already happened with at least three ⛔ boxes
open (A-24). That ordering question is Andy's, not a session's.

---

*Written 2026-08-07. This file is the pack; it edits nothing else. Every number in it was read from
the folder this session. Where the folder and project memory disagree — the lockout record and the
F-C1/F-C2 rulings — the divergence is stated in §1.3 rather than resolved, and S0 closes it under
Andy's gate A3.*
