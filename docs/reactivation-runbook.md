# Day-0 reactivation runbook

*Rewritten from scratch 2026-07-30 after the consolidation pass. Supersedes all earlier versions.
Account inactive; reactivation ~mid-Aug 2026. **Not blocked** — the re-arm ~~mechanism is known~~
**procedure is known; the CAUSE is not** (§1, corrected 2026-08-05).*

> **Read `docs/build-plan.md` first.** It is under decision freeze and defines the fleet disposition this
> runbook executes. Do not improvise a change here on the day.

---

## 0. What is different this time

Day-0 used to mean re-arming ~35 lapsed bots and hoping. It doesn't any more.

**Every active bot on Day-0 is fresh-built, cloned-to-spec, or untouched-validated.** The clones and fresh
builds are constructed *after* reactivation with their exits correct from birth, so they were never lapsed
and have nothing to re-arm. **The re-arm sweep applies to nine bots only** — the two directional bots and
the seven live mirrors, the only ones that lived through the lapse.

Most of the build work happens **before** you pay. Edits made while the account is inactive **do persist**
(verified empirically 7/29→7/30). Do as much of §3 as OA allows before Day-0, and log every inactive-era
edit.

> ### ⛔ ADDED 2026-08-07 — THE ACCOUNT IS FULLY DISABLED. DAY-0 NOW BEGINS FROM A LOGGED-OUT STATE.
> **[FIRST-HAND, Andy's screenshot, 04:24 ET 2026-08-07]**: OA login itself is blocked (“Account
> disabled, please purchase a plan”), a step beyond the inactive-but-reachable account this
> section was written against. **Step 0 now includes, before anything else in §4: log in, verify
> the 41-bot roster, and re-run the A-series against fresh captures** (per
> `day0-session-pack-2026-08-07.md` §S0). See `state.md`'s dated lockout block (end of file,
> 2026-08-07) for the full first-hand record. The Step 0a/Step 1 ordering question this creates is
> already recorded there as gate A2 in the pack — unchanged by this note.

---

## 1. The lapse mechanism — EXISTENCE ESTABLISHED, CAUSE STILL UNVERIFIED (OA support / Zack, 2026-07-30)

> ### ⛔ CORRECTED 2026-08-05 on Andy's release (D2) — this heading previously read *"ANSWERED"*.
> The toggle's **existence** is `[DOCUMENTED + FIRST-HAND ×2]` (OA-0871, OA-0896, plus Andy's
> fleet-wide read). The **causal** claim — that flipping it back ON re-arms exit-order generation,
> and that its being OFF is what killed the June exits — is **NOT established.** The independently
> ruled position on the June regression is **D-4: the June cause is UNKNOWN.**
> **Everything in this section is what to DO, not what is proven. §4 Step 6a settles it, either
> way — and it has a branch for the refuted outcome.**

**Each bot's dashboard carries a per-bot `EXIT OPTIONS` ON/OFF toggle at the top right, beside the
`AUTOMATIONS` toggle. That toggle is the hidden state.**

Deactivation turns both off. Resubscription restores **only `AUTOMATIONS`** — which is why the monitors
fired while every PT and time exit stayed dead. The failure is **visible only on that dashboard toggle,
never in the editor**: the Exit Options editor keeps displaying every setting exactly as configured.

**Andy has confirmed both toggles are currently OFF on every bot.** That is the state Day-0 starts from.

What this cost in v1: **−$9,618** net across the Fortress pair over six June days — concentrated enough
that two put legs alone lost −$9,734 across two of those days, with call-side wins offsetting the rest.
It was invisible for six sessions. The champion's PT25 died on June 1, the first session back, while its
6/14 clone worked 70/0.

Two design consequences, already built in:
- **One toggle kills every Exit Option on a bot at once** — PT, Touch and time exit together. No partial
  failure mode, no redundancy inside Exit Options. This is why the **15:52 flat-close backstop lives on the
  `AUTOMATIONS` side**, a different execution class.
  > ### 📝 SHARPENED 2026-08-05 — the execution-class claim is right; its stated bound was wrong.
  > **[FIRST-HAND 2026-08-04, DOM read of `app.optionalpha.com/settings`.]** The Settings surface is
  > called **Bot Schedule** and it carries **TWO INDEPENDENT WINDOWS**, not one: Automations
  > `scanstart 09:31` → `scanend 5` (**15:55**) · Exit Options `exitstart 09:31` → `exitend 1`
  > (**15:59**). This project had been treating one window where the product has two.
  >
  > ⚠️ **Neither window binds the backstop.** OA's footnote, verbatim: *"Repeating and date/time
  > scheduled automations are not affected by this schedule and run at the selected date and time
  > even if it's outside the range defined above"*. The backstop is a **Repeating** trigger. Its
  > actual bound is the `max="15:55"` on the Custom time input — **a different limit; do not merge
  > the two.**
  >
  > ⚠️ **The 15:59 edge has a Day-0 consequence** the sequence does not yet handle: the Exit
  > Options window is still open nine minutes after a 15:50 exit, and an exit-option order stays
  > live two minutes — so a 15:50 order is still working when the backstop fires at 15:52.
  > Attribution cannot rest on the timestamp gap alone: `docs/day0-audit-2026-08-05.md` F-17.
- **On the two control clones, PT25 is removed from the Open Position action explicitly** rather than left
  dead behind an off toggle. A toggle can be flipped by accident; a removed action cannot.

Caveat that still stands: this came from **one rep**, who did not know the documented Excessive Errors
Failsafe (and the failsafe is excluded as the June cause — zero June errors on either Fortress bot,
newest error `Apr 16, 2026 3:55PM`; `oa-platform-reference.md` §4.5, ruled D-4 2026-08-04. The
mechanism itself is real — tripped March/April, entry scanners. Applied 2026-08-06,
`decision-card-2026-08-06.md` ruling 1). Verify capabilities in the UI. And **the toggle being ON
was never the failure we observed being detected** — a toggle screenshot is necessary but not
sufficient. Keep the order-level verification.

---

## 2. The per-clone checklist — run this for each of the 4 clones

Order matters. One of these steps exists because of a trap that will silently produce a broken bot.
*(Was "Two of these steps" — amended 2026-08-05 with step 2's correction below; the shared-automations
trap was falsified 2026-08-03 and step 2 is now a Library check, not a fork ritual.)*

1. **Clone** the original bot.
2. **Check the Automation Library before editing anything.** ⚠️ **Corrected 2026-08-05, at Andy's
   authorization — the old step here said "clones share automations by reference." That is FALSE**
   (direct test 2026-08-03; OA-0681 / OA-0682 / OA-0683 / OA-0845; `oa-ops-runbook.md` §5 Trap 1 as
   corrected). **Cloning copies.** Sharing is opt-in via the Library only. For each automation on the
   clone: if it is **in the Library**, use **Copy** to fork it before editing — a Library edit
   propagates to every bot using it (OA-0682). If it is **not** in the Library — the default for a
   clone — **edit it directly; no fork is needed.** Then confirm the ORIGINAL's automation list is
   unchanged. That confirmation is now a sanity check, not a trap counter, and it costs one page load.
   > ⛔ **IF the ORIGINAL's list changed** → the automation was in the Library and the Copy was
   > skipped. You are editing a shared object and **the edit has already propagated** (OA-0682:
   > *"Any changes made to an automation will flow through anywhere the automation is used,
   > including other bots."*). **STOP this clone. Do not proceed to step 4.** Record which
   > automation and what changed. **Bot stays OFF. The other clones stay unstarted until the blast
   > radius is known** — check every bot the Library page reports as using that automation.
   > **Escalate to Andy: YES.**
3. **Re-add Symbols — and check the three traps that actually bite.** ⚠️ **Amended 2026-08-05
   [FIRST-HAND 2026-08-03, Clone dialog values read on the Fortress pair].**
   Symbols drop silently on clone. A bot with no Symbols looks configured and simply
   never scans.
   ⚠️ **But this trap did NOT bite the Fortress pair** — its symbol is *automation-resident*
   (`Loop QQQ` + action `Symbol: QQQ`) and carried across the clone correctly. It still bites any
   bot using the Bot Symbols loop. **Check which kind you have; do not assume either way.**
   ⛔ **Three traps that DID bite, undocumented by OA — whose own docs claim a clone arrives
   "complete with all the settings and strategies of the original":**
   - **Allocation resets to a flat `1000`** in the Clone dialog (original `$100,000`) — **a silent
     100× sizing error on a bot that looks fine on the dashboard.** Re-set it to the
     pre-registered value and **read it back**; a save confirmation is not this check.
   - **Bot Group drops to `None`.** Restore it — and note the export respects the bot-group filter.
   - **Tags drop to empty.** Restore them.
   > ⛔ **Then read the Symbols panel back, character by character, against the original's list.**
   > *"Verify, don't assume"* — and *"It is **not empty**. Look at it again. This is the single most
   > common silent clone failure in this fleet."*
   > **IF the panel is empty or does not match after re-adding** → re-add once via the form control,
   > then re-read `.value` (typed input lands intermittently). **IF it is still wrong** → **stop
   > this clone; the bot stays OFF. The other clones proceed. Escalate to Andy: YES.** Do not
   > proceed to step 4 — every later step would be built on a bot that never scans.
4. **Apply the spec** from `build-plan.md` §2B. Nothing beyond the spec.
5. **Capture the automation tree** (bookmarklet) — this is what `bots_config_v2.csv` will cite.
6. **Save as template V1** with the pre-registration note attached, so the config has a versioned identity
   from birth.
6a. **⏸ Template V2 — the pilot only, and it lands BEFORE Day-0.** ⚠️ **Added 2026-08-05 on Andy's
    release (D1).** **Decision 6 ruled 2026-08-04: re-price the 15:50 Expiration exit OFF Market**
    (SmartPricing — internal value `speedy`, **NOT** `fast`; a capture parser keying on "fast"
    silently misses it). **The 15:52 backstop KEEPS Market.**
    ⛔ **Execution was deferred as part of the ruling:** the pilot's Template V1 / PR-03 config hash
    is **frozen**, so this is a **spec change, not a config tweak.** It lands as **Template V2 with
    an AMENDED pre-registration**, before Day-0 — **never as a quiet edit.** PR-03 is still
    unsigned; the amendment and the signature happen together.
    ⚠️ **This is what makes the three 15:50-15:52 mechanics distinguishable** in a Trades list —
    see §4 Step 6. Without V2 they are three Market orders in two minutes with only memo strings
    between them.
7. **Verify both dashboard toggles** — `AUTOMATIONS` and `EXIT OPTIONS` — and screenshot them.
   Toggle state does not survive text capture. *(For the two control clones, `EXIT OPTIONS` stays OFF by
   design and PT25 is already removed from the action — verify the removal, not the toggle.)*
   > ⛔ **IF either toggle reads OFF on the post-save screenshot** → drive it ON and re-screenshot.
   > **IF it reverts** → **bot stays OFF · other clones proceed · escalate to Andy: YES.**
   > A save confirmation is never this check.
   > ⛔ **IF PT25 is still present on a control clone's Open Position action** → **do not remove it
   > yourself.** The removal is spec, and the spec is frozen (`build-plan.md` §4). **Bot stays OFF ·
   > escalate to Andy: YES.**
   > ⚠️ **A toggle screenshot is necessary and not sufficient** (§1). §4 Step 6's Trades-list check
   > is still required before this bot may trade.
8. **Rename the original** with an `-ARCHIVED-<date>` suffix, **then archive it.** Renaming first frees the
   production name for the clone and keeps the archived record self-labelling.
   ⛔ **The archive click is Andy's — added 2026-08-05. [FIRST-HAND 2026-08-04, pilot original.]**
   `archiveBot` **fired from none of the three working click mechanisms** — dispatched event
   sequence on the item, the same on the hit-tested target, and click by element ref. No error, no
   dialog, `/bots` unchanged. **Stop at three attempts and hand it to Andy. Do NOT fall back to
   coordinates:** on that `…` menu `Delete` sits **~29px below `Archive`**, and a mis-landed click
   is unrecoverable — on the pilot's original it would have destroyed **41 positions** of history.
   ✅ The **rename** is what frees the production name, and the rename does commit, so the archive
   is hygiene, not a blocker. Verify it afterwards **read-only** from `/bots`: active-bot footer
   count decremented by one, exactly one bot under the production name, and the `-ARCHIVED-` name
   no longer listed.
9. **Log it** — clone date, spec applied, template version, capture filename, and the archived original's
   new name. **Append the row to `data/archive/rename_map.csv`** (`original_name`, `archived_as`,
   `clone_name`, `date`, `disposition`) as you go, not afterwards from memory. This is the only thing that
   will later connect a name in the frozen ledger to a bot running today.

---

## 3. Before Day-0 — the build window

**Edits made while the account is inactive persist** (verified 7/29→7/30), so the entire build happens
*before* you pay. Day-0 itself should be a short, boring checklist — not a build day.

### Step A — Pilot the clone ritual on ONE bot first

> ### ✅ DONE 2026-08-04 — THE PILOT RITUAL IS COMPLETE END TO END. Do not re-run it.
> **[FIRST-HAND 2026-08-04: `/bots` read read-only — footer `35 active bots`, exactly one bot under
> the production name, resolving to the clone; `data/archive/rename_map.csv` row written.]** Steps
> 5c, 6, 7, 8, 9 and FINISH are all done. The clone holds the production name
> `QQQ-IC-0DTE-Fortress` (`BOTfw5TkkCRF2717857919585029021`); the original is
> `QQQ-IC-0DTE-Fortress-ARCHIVED-2026-08-03` and archived.
>
> ⚠️ **Two things remain outstanding on the pilot, and neither is a re-run:** Template **V2**
> (ruled 2026-08-04, execution deferred) and **Bot Group**. See `docs/day0-audit-2026-08-05.md`
> F-12 and F-21.
>
> ⛔ **If the card is ever re-run on a different day, all 11 date literals in
> `pilot-clone-card-qqq-fortress.md` are stale again** — the `-ARCHIVED-` suffix and the
> `rename_map.csv` row are lineage records, and a wrong date in them is a record that lies.
>
> *The text below is the original instruction, left standing as the record of what was run.*

Run the full 9-step checklist on **`QQQ-IC-0DTE-Fortress`** and nothing else. Find out where the automation
Copy-vs-reference trap and the Symbols drop actually bite, on a bot whose spec is simple and whose original
is already superseded. **Do not start the other three clones or any fresh build until this pilot is clean.**
A mistake made once is a lesson; the same mistake made across nine bots is a rebuild.

> ### ⛔ WHAT "CLEAN" MEANS — added 2026-08-05 on Andy's release (D2). It was undefined.
> The pilot is **clean** when all six hold **and Andy has said so**:
> 1. Every ✅ CONFIRM block in `pilot-clone-card-qqq-fortress.md` is ticked — none from memory.
> 2. The original's automation list is unchanged from its Step 0 capture.
> 3. The clone's Symbols panel is non-empty and matches Step 0 character-for-character.
> 4. Daily and Total position limits are even numbers (an IC = 2 positions).
> 5. Both capture sets and both toggle screenshots are on file under `data/captures/`.
> 6. Both open questions are answered in writing: Preset control yes/no; 15:52 reachable yes/no.
>
> ⚠️ **The 15:52 backstop being NOT buildable does NOT make the pilot unclean** — that is a known
> unknown with its own branch: leave it unbuilt, flag it, finish the card, **do not substitute a
> different time.**
>
> ⛔ **IF any of 1–6 fails** → **no other clone and no fresh build starts. Fleet stays OFF.**
> **Escalate to Andy: YES — Andy declares the pilot clean. Claude does not self-certify it.**

### Step B — Capture the roster, then sweep
Bookmarklet capture of `/bots` **first** — it is the roster authority and the only record the zero-trade
bots will ever have. *(Done 2026-07-30: `data/captures/oa_bots_capture_2026-07-30.txt`, 35 bots.)*
Then: **positions → archive, empty → delete** (`build-plan.md` §2).

> ⛔ **CAPTURE FAILURE BRANCHES — added 2026-08-05 on Andy's release (D2).**
> **Write the expected bot count down BEFORE capturing.** **IF the capture's count does not match**
> → recapture once. **IF it still disagrees** → **fleet stays OFF · escalate to Andy: YES.** A short
> roster silently drops bots from every future drift diff, and the drift diff is the whole detector.
> **IF a per-bot capture shows only automation names and no decision text** → the carets were not
> expanded and the branch is not in the DOM. **Re-expand and re-grab. That bot stays OFF until its
> tree captures; the fleet proceeds.**
> ⛔ **IF `Export Data` was taken with any bot group deselected** → **discard it.** The export
> respects the bot-group filter and a subset export rebuilds the ledger as a subset. Re-export with
> **all groups selected.**

Two traps in this step, both of which destroy something if you move fast:
- ⛔ **Delete exactly two bots**: `TEST QQQ-IC-0DTE-HedgeC-S3 Clone` and `QQQ-IC-0DTE-InvFilter-Wide150`.
  **`DIR-SPX-PutVIX22-SL75` is also zero-trade and must NOT be deleted** — it is an OOS-validated build
  whose VIX≥22 gate correctly never fired. Empty ≠ worthless.
  ⚠️ **Those are still the right two — and they are no longer the whole residue picture. Added
  2026-08-05. [FIRST-HAND 2026-08-05, `My Automations` / Library read: `CLAUDE-C5-SHARED-SCRATCH`,
  `rid RTfw5TkkCRF178589028977611`, carrying automation input `C5_EXITS` (`IN178589048006251`).]**
  That object is **account-level** and **does NOT die with the two scratch bots.** Left in place it
  orphans in `My Automations`, where the account previously held exactly **one** shared automation
  — so an orphan is conspicuous and will be mistaken for a real object.
  ✅ The two bots' **own** bindings — bot inputs `CLAUDE-C0A-BOT-EXITS`, `C5_BOTVAL_TESTCLONE`,
  `C5_BOTVAL_INVFILTER`, their instances, and the 2026-08-04 `CLAUDE-G1-EMPTY-EXITS` residue —
  **all die with their bots. No sweep action for these.**
  ⛔ **RULED 2026-08-05 (D5) — THE SWEEP DELETES IT. This is a third delete, not a third bot.**
  **After `TEST QQQ-IC-0DTE-HedgeC-S3 Clone` and `QQQ-IC-0DTE-InvFilter-Wide150` are deleted,
  delete the Library object `CLAUDE-C5-SHARED-SCRATCH` (`rid RTfw5TkkCRF178589028977611`)
  EXPLICITLY**, from `My Automations`. Verify by re-reading `My Automations` and confirming the
  account is back to exactly **one** shared automation (`Defang-Mon-S2-StrikeTouch`).
  ⛔ **Order matters: bots first, object second.** Deleting the shared object while a bot still
  references it is an edit to a live binding, and a Library edit propagates to every bot using it
  (OA-0682).
  ⛔ **IF the object will not delete, or `My Automations` does not return to exactly one entry** →
  **do not force it and do not delete anything else. Record what is there and escalate to Andy: YES.**
  An orphan left in the Library is conspicuous but harmless; a wrong delete in a shared-object list
  is not recoverable.
- ⚠️ **Read full names before archiving**: `Opening Range Breakout 60m` is archived,
  `60min-ORB-10W-Paper-v1` stays live.

### Step C — Build the rest
The remaining 3 clones per §2, then the 5–7 fresh builds. Greenfield exits are a named **Exit Option Preset
in the Open Position action** (~~PT% as a Bot Input~~ **the Exit-Options SET as a Bot Input** · Touch $0 on
the challenged side · time exit), plus the
**15:52 flat-close Scheduled Event backstop**, plus a **position-closed-trigger automation** to close the
sibling spread. Optional 1-lot canary.

> ### 📝 D-1 PROPAGATED 2026-08-05 — substring replaced on Andy's explicit release
> *From `docs/decision-memo-2026-08-04.md`'s draft amendment (b), one occurrence. Original struck
> in place. **The Day-0 sequence is otherwise unchanged.***
>
> **D-1 ruled 2026-08-04 → Option A.** *"PT% as a Bot Input"* is **not expressible** — **[FIRST-HAND
> 2026-08-04, Exit Options editor on `QQQ-IC-0DTE-Fortress Clone`]**: the 🔗 sits on the Exit
> Options **row**, and inside the Default Value editor `i.fa-link` count is **0**. There is no 🔗 on
> Profit Taking % or any individual field, so the linkable unit is the **whole exit bundle**.
>
> ⛔ **G2 rider, and it changes what Day-0 must capture.** The saved action stores a **REFERENCE,
> not values** — `{"type":"input","input":"IN…","text":"<label>","oldValue":{…}}`. **A capture that
> reads only the action records the input's NAME, so every arm diffs as identical.** Any Day-0
> capture, capture-diff or drift-audit run against these bots must **also read the input object's
> value**. ⚠️ **Never read `oldValue` as current config** — it is a pre-link snapshot and goes
> stale.
>
> ⛔ ~~**Build gate unchanged and still binding: greenfield check C0a — the BOT-INPUT tier has never
> been observed.** The finding above is at the *Automation* Input tier. If C0a fails, Architecture E
> is not buildable and Step C's fresh builds return to Andy (`greenfield-family-spec.md` §10).~~
>
> ✅ **SUPERSEDED 2026-08-05 — C0a PASSES ON BOTH CLAUSES.** The BOT-INPUT tier **was** observed
> — **[FIRST-HAND 2026-08-05, probe on two scratch bots: the control lives on the bot's automation
> row → ⚙ Edit Settings → 🔗 → `Bot Inputs`, and the bound value was read back]**. Architecture E
> **is buildable** and Step C's fresh builds do **not** return to Andy on C0a.
>
> ⛔ **This closes C0a ONLY — it does not open the build.** `C0c · C2 · C7 · C8 · C9` remain
> **untouched**, and **C10 is open and blocks ARM-B1**. See `docs/day0-audit-2026-08-05.md` F-18.
> ✅ **The G2 rider above is unaffected and still binding.**

### Step D — Pre-register everything
Draft a pre-registration entry for ~~all ≈18 active bots~~ **≈18–20 plan bots — and, separately, up to
8 pre-registered Track B arms, ceiling 28** *(📝 corrected 2026-08-05 on Andy's release (D1), per
`build-plan.md` §2D's `🔓 SCOPING AMENDMENT 2026-08-05`)* during this window, so **Day-0 is signing, not
authoring**. Hypothesis · kill criterion · sample target · review date · config-capture hash.
⚠️ **The amendment scopes a COUNT. It authorizes no build**, and **every Track B arm still needs its
own signed entry** before it may be switched on.

### Step E — Dry-run the pipeline at n=0
Run `daily.sh` end-to-end against an empty post-cutover ledger. Every script must **degrade gracefully at
n=0** — no divide-by-zero, no empty-frame crash, no misleading 0.0% expectancy rendered as a finding.
Day-1 is the worst possible time to discover the reporting stack cannot handle having no data yet.

> ### ⛔ FAILURE BRANCHES — n=0 DRY RUN. Added 2026-08-05 on Andy's release (D2).
> **IF any script raises** → **fix the script, do not fix the data.** ⛔ **Never seed a synthetic row
> to make the run pass** — a seeded row is a pre-cutover row entering the working ledger, which
> `LEDGER_START` exists to refuse. **Re-run the full `daily.sh` after the fix, not the single
> stage. Day-0 does not start until a clean end-to-end n=0 run is on file — this is a ⛔ HARD
> BLOCKER.** Escalate to Andy: NO for a fix · YES if the fix requires a spec change.
>
> **IF a script emits `0.0%` expectancy, a flat R, or a populated-looking table at n=0** → that is a
> **failure, not a pass. An absent number is not a zero.** Fix and re-run.
>
> **IF `lessons.py` shrinks a populated index** → the shrink guard caught a real Day-1 data-loss
> path. ⛔ **Do not set `LESSONS_ALLOW_TRUNCATE=1` to make the dry run pass.**
>
> **IF Tier C rules report SKIPPED** because `bots_config_v2.csv` does not exist yet → **that is
> correct behaviour, not a failure.** Confirm the SKIPPED list reaches the brief. **Silence in its
> place is the failure.**

---

## 4. Day-0 sequence

> ### ⛔ HOW TO READ THIS SECTION — added 2026-08-05 on Andy's release (D2).
> **Every check below carries an explicit branch. There is no step here that requires judgment.**
> - **"bot stays OFF"** → that bot does not trade today. **The rest of the fleet proceeds.**
> - **"fleet stays OFF"** → **nothing else is switched on today.** Stop the sequence and escalate.
> - ⬜ **A check you could not run is NOT a pass.** It is **NOT EVALUABLE**, it is written down as
>   such by name, and the bot stays OFF. Never record an unrun check as clean.
> - ⛔ **Do not improvise a remedy.** `build-plan.md` is under decision freeze and **Day-0 is not a
>   build day.** Where a branch says escalate, escalate to Andy and stop that thread.
> - ⚠️ **The steps are in dependency order. Do not reorder them.** Several exist only because
>   something later cannot be read until they have run.

### Step 0 — Close the Pre-Day-0 checklist. Nothing in §4 starts until it is closed.

> ⛔ **STOP — §4 is not self-contained.** The checklist at the foot of this file is a set of
> **preconditions** for the steps below, and Step 4 does not re-assert them. Confirm each **by
> reading the artifact itself**, never from a memory of a prior session.
> **IF any ⛔ HARD BLOCKER box is unticked → do not pay, do not re-arm. Escalate to Andy: YES.**

### Step 0a — ⛔ Set `itmlive` = `market`. HARD GATE, before any capital is live.
*Added 2026-08-05 on Andy's release (D1). Ruled D-3, 2026-08-04.*

`itmlive` is deliberately still `auto` — *"Calculate estimated P/L from underlying close price"* —
which **sends no closing order at all.** `market` is the only option that closes. A QQQ condor
outliving its exits under `auto` rides into **physical settlement**: real stock delivered, with the
bot blind to the assignment. Separately, every ITM expiry under `auto` enters the export as a
**modelled** P/L rather than a fill, so the loss tail is synthetic and the arm ranking measures a
model rather than the arms.

**DO:** `/settings` → set `itmlive` = `market` → **hard reload** → re-read `input.value` →
screenshot before and after. **A save banner is not verification.**

⚠️ **`itmpaper` is ALREADY `market`** — set and verified 2026-08-04 by hard reload + `input.value`
re-read, before/after screenshots on file. **Do not re-set it.** Read it back as part of the same
self-check. `itmlive` is the only half still outstanding.

⛔ **IF the value will not persist through a hard reload → NO capital goes live. FLEET STAYS OFF.
Escalate to Andy: YES.**

⚠️ **`market` is not a substitute for the 15:52 flat-close backstop.** It reaches only *expiring
ITM* positions on expiration day.

### Step 1 — Pay / reactivate
Note the exact timestamp. **This date is `LEDGER_START`.** Set it in `build_ledger.py` before anything
else, so no pre-cutover row can enter the working ledger.

> ⛔ **VERIFY IT, do not assume it. Added 2026-08-05 (D6/F-33).** After setting it, run
> `build_ledger.py` once and confirm the row count is **0** and the status reads **EMPTY LEDGER,
> n=0**.
> **IF the ledger returns ANY row** → a pre-cutover row has entered. ⛔ **STOP. Nothing is re-armed.
> FLEET STAYS OFF. Escalate to Andy: YES.** Every downstream number would be cross-era.

### Step 2 — Decide the open mirror positions: ride or close
Five positions were open at the 2026-07-30 capture and will still be open at reactivation:
**`QQQ long call` ×4** — ~$13K risk, ~**−$10.8K unrealized** — and **`Tasty Condor` ×1** (~+$328).

Make an explicit, logged **ride-or-close** call on each before anything else trades.
This must not be the one undecided thing on the account: an unmanaged legacy position is exactly the kind
of quiet exposure that survives a clean-slate rebuild and then surprises someone. Whichever way it goes,
write the reason into the pre-registration ledger — these are pre-cutover positions, so under the straddle
rule their P/L resolves into the **mirror baseline layer**, never the working ledger, and they will not
appear in any post-cutover report unless someone deliberately looks.

> ### ⛔ THE DECISION IS NOT COMPLETE UNTIL IT IS EXECUTED AND RE-OBSERVED. Added 2026-08-05 (D6/F-34).
> **A logged call is not a disposition.** Before Step 3 touches any toggle:
> 1. ⚠️ **Draft and sign the ledger entry FIRST.** `pre-registration-ledger.md` records that this
>    entry *"is not yet drafted"* — **there is no place to write the reason until it exists.**
> 2. **CLOSE → close the positions now**, then re-read the **Trades list** and confirm the closing
>    rows are there. A save confirmation is not evidence.
> 3. **RIDE → the ride must survive Step 3.** Turning `EXIT OPTIONS` ON for `QQQ long call` or
>    `Tasty Condor` re-arms every exit on that bot at once (§1) and **can close a ridden position
>    within minutes of reactivation.** Before flipping either toggle, read that bot's Exit Options
>    and record what would fire. **If anything would act on the five open positions against the
>    decision, leave that bot's `EXIT OPTIONS` OFF** until the positions are closed or the exits
>    are removed.
> 4. ⚠️ **Mirror funding does NOT gate this and is not decided today.** `docs/mirror-funding-memo-2026-08-05.md`:
>    **zero of ten mirrors clears the evidence bar, and none can before late Oct 2026.** The Day-0
>    mirror action is **re-arm, watch-only, size nothing.** ⛔ **Do not read "insufficient evidence"
>    as "do nothing" — for a running bot that means CONTINUE, which is a capital decision made by
>    default.** Say the verdict out loud in the log.
> ⛔ **IF the ride-or-close call has not been made, signed AND executed for all five** → **do not
> proceed to Step 3. No bot is re-armed. Escalate to Andy: YES** — this is a capital decision and
> go-live authority is Andy's.

### Step 2b — Sign the pre-registration entries. Nothing is switched on before this.
*Added 2026-08-05 on Andy's release (D2/F-10).*

> ⛔ **STOP — no toggle is touched until this step is complete.** *"Andy signs and dates. Only then
> may the bot be switched ON."*

Run `pre-registration-ledger.md` §7's six-item checklist for **every bot that will be ON today** —
the nine untouched (PR-05…PR-13), the four clones, the fresh builds, **and every Track B arm.**
Config hash from the bot's own capture file, every `<placeholder>` resolved, max-loss line filled,
Andy signs and dates.

**A bot whose entry is unsigned stays OFF for the whole of Day-0. No exceptions, including the
nine** — the ledger names them explicitly because they are the group most likely to be waved
through as "untouched". ⚠️ **Signed ≠ verified.** Signing does not satisfy Step 6.

### Step 2c — ⭐ THE NO-TOUCH OBSERVATION. Do this BEFORE any toggle is moved.
*Added 2026-08-05 — **Andy ruled the open slot: OBSERVE FIRST** (D0). Previously `NOT RULED`, and
Step 3 as written resolved it by acting.*

**Why it must be here and nowhere later.** Day-0 is itself an inactive→active transition. **If exits
resume at reactivation with NO toggle intervention, billing state is implicated as the June cause.**
Flip a toggle first and re-arm is confounded with reactivation — the toggle candidate and the
billing candidate become **permanently indistinguishable**, and §1's causal story stays
unfalsifiable forever. The observation is free; the information is not recoverable afterwards.

**OBSERVE — before Step 3, before any toggle is moved:** read both dashboard toggles on **one live
mirror and one directional bot**, and **screenshot both**. Andy's pre-Day-0 state is *both toggles
OFF on every bot* (§1), so the question is whether either now reads ON without anyone touching it.

- **IF either toggle reads ON without intervention** → ⭐ **BILLING STATE IS IMPLICATED.** Log it as
  a first-hand observation with the screenshot filename and the timestamp, **report to Andy before
  proceeding**, and carry it into the Step 6a verdict. Do not re-flip anything first.
- **IF both read OFF on both bots** → the toggle candidate survives. Record it verbatim and proceed
  to Step 3. This is the expected result; **record it anyway — a confirmed expectation is evidence
  and an unrecorded one is not.**
- **IF the toggles cannot be read** → ⚠️ **an unread toggle is not an OFF toggle.** Re-screenshot.
  If still unreadable, record `NO-TOUCH OBSERVATION UNREAD` and say so at close-out. **Proceed —
  this observation does not gate the sequence**, but a missing answer is never reported as a
  negative one.

⚠️ **Account settings are not bot toggles.** Step 0a set `itmlive` at the account level and does
**not** count as toggle intervention. Nothing else may touch a bot before this observation.

### Step 3 — Re-arm sweep: `EXIT OPTIONS` ONLY. The nine leave-in-place bots.
*⛔ **Amended 2026-08-05 on Andy's release (D3) — the swap.** This step previously turned
`AUTOMATIONS` ON as well, **24 lines before the gate that authorizes entries.***

> ⛔ **DO NOT TURN `AUTOMATIONS` ON IN THIS STEP.** Re-arming and authorizing entries are two
> different acts and Step 7 is the gate between them. **`AUTOMATIONS` ON *is* the entry
> authorization:** a bot switched on here takes a position before Step 6 can prove it — which is
> the v1 failure (§1, **−$9,618**) reproduced on Day-0, with Step 7 gating nothing.

`DIR-SPX-PutVIX22-SL75`, `DIR-SPX-CallVIXdrop`, and the seven live mirrors
(`3DTE $140-$350`, `Nigiri-Paper-v1`, `QQQ long call`, `Friday 14 DTE Broken Wing IB (B-70)`,
`Trendy-Paper-v1`, `60min-ORB-10W-Paper-v1`, `Tasty Condor`).

For each: **`EXIT OPTIONS` → ON**, **`AUTOMATIONS` LEFT OFF**, then screenshot **both** toggles.
`AUTOMATIONS` → ON happens once, per bot, in **Step 7** — never here.

⛔ **THE NINE ARE NOT EXEMPT FROM STEP 6** *(ruled explicitly 2026-08-05, D3)*. The line below scopes
**re-arming**, not **verification**. Each of the nine passes the order-level Trades-list check before
it may trade, **exactly as a clone does.** A pre-existing bot is not a proven bot — these nine are
the only bots that lived through the lapse, which makes them the *most* in need of the check, not
the least.

Nothing else on the fleet needs re-arming. Clones and fresh builds are born correct; the ~20 archived bots
are gone.

> ### ⛔ FAILURE BRANCHES — RE-ARM SWEEP. Added 2026-08-05 (D2/F-6).
> **IF the `EXIT OPTIONS` toggle is not present on a bot's dashboard** → try the **two other
> documented surfaces** before concluding absence: **inside the bot**, and **individually within
> each position** (OA-0896). ⚠️ **A surface you did not open is not an absent control.**
> **IF all three are absent** → the lapse mechanism is **unexplained, not solved**. **Bot stays OFF ·
> the other eight proceed · escalate to Andy: YES.**
>
> **IF a toggle reverts to OFF, or the post-save screenshot reads OFF** → re-drive it once via the
> full pointer sequence (element refs alone silently no-op). **IF it reverts a second time** →
> **bot stays OFF · fleet proceeds · escalate to Andy: YES.** ⛔ **Do not fall back to coordinate
> clicks.** ⚠️ *This revert branch is a drafted remedy, not a corpus-cited one — no observation of a
> reverting toggle exists. Record what actually happens.*
>
> **IF three or more of the nine will not hold ON** → ⛔ **STOP the sweep. FLEET STAYS OFF.
> Escalate to Andy: YES** — §1's mechanism is falsified and Day-0 is not a checklist day.
>
> ⚠️ **The toggle has THREE documented surfaces and this step touches one** (D6/F-35). On any
> position that was already open **through** the lapse — the five in Step 2 — **read that
> position's OWN Exit Options state** before acting on it. **This has never been observed on those
> five positions: it is an unopened screen, not a known-good one.**

### Step 4 — Confirm the build window is complete
Every clone and fresh build has: a capture on file, a saved template at its **current ruled version**
(⚠️ **the pilot requires V2, not V1** — §2 step 6a), a signed pre-registration entry,
and a `rename_map.csv` row. Anything missing is finished now or its bot stays OFF.

> ### ⛔ TWO ADDITIONAL GATES FOR THE 7-BOT FAMILY AND THE TRACK B ARMS. Added 2026-08-05 (D4/F-18).
> Neither is satisfied by the four artifacts above.
>
> **(a) Phase 0 blocking checks CLOSED.** `C0c · C2 · C7 · C8 · C9` are recorded as **untouched**
> and **C10 as OPEN** as of 2026-08-05. **C7 and C8 carry their own ⛔ STOP** — C8's verbatim:
> *"Do NOT substitute position age — that is the literal substitution that cost −$15,376."*
> ⛔ **IF any of the five is still unanswered, the family does not trade today** — those bots stay
> OFF and the checks are run **as reads, never writes**, before switch-on. **Do not improvise a spec
> on the fly.** Fleet proceeds. Escalate to Andy: YES.
>
> **(b) A7 payload-hash baselines RECORDED** — the payload hash of each of the four shared
> automations, written to `bots_config_v2.csv`'s shared-object rows, **re-read and re-hashed after a
> hard reload**, and A7 wired into `daily.sh`. Under Architecture E the automations are **shared
> across seven bots**, so a later edit changes all seven at once with no template version bump, and
> a mis-built gate fails **identically on all seven** — which the arms cannot detect by diffing each
> other. **A7 is the only detector.** ⛔ **No baseline before Day-0 = no detector for the whole
> sample. Those bots stay OFF.**

### Step 5 — Capture everything, and RESOLVE THE INPUT CHAIN
Full bookmarklet sweep of `/bots` across the whole new roster, plus toggle screenshots.

> ⚠️ **A `/bots` sweep is NOT `bots_config_v2.csv`. Corrected 2026-08-05 (D6/F-26).** It carries
> names and P/L and **no Exit Options values**, and that file describes the *post-Phase-4* fleet.
> It is written **per-bot as each bot is built** — not as a big-bang Day-0 extraction. **Step 5
> VERIFIES those rows are present and current; it does not create them.**
>
> ⛔ **THE D-1 G2 RIDER APPLIES HERE, TWO HOPS DEEP** (§3 Step C states it; this is where it bites).
> The saved action stores a **REFERENCE, not values.** Every capture, capture-diff and drift
> baseline must resolve **action → automation input → bot input** and read the **input object's
> value**. **A capture that reads only the action records the input's NAME, so every arm diffs as
> identical and the tournament is undetectably void.**
> ⚠️ **Never read `oldValue` as current config** — it is a stale pre-link snapshot.
> ⛔ **IF the input object's value cannot be read** → **the capture is not a baseline. Do NOT record
> it as one, and do NOT fall back to `oldValue`.** Mark those bots' config-capture hash **NOT
> ESTABLISHED**; their pre-registration entries **cannot be signed** (the entry requires a
> config-capture hash). **Those bots stay OFF · the rest of the fleet proceeds · escalate: YES.**
> The control lives on the **bot's** automation row → ⚙ Edit Settings → 🔗 → `Bot Inputs`.

> ### ⛔ SEVEN ACCOUNT-LEVEL FIELDS THAT ARE IN NO CAPTURE AND OVERRIDE EVERY BOT. Added 2026-08-05 (D4/F-13).
> **`/settings` is a SEPARATE capture from `/bots` and it is not optional.** Record, every sweep:
> `itmlive` · `itmpaper` · **`maxexits`** · `scanstart` · `scanend` · `exitstart` · `exitend`.
> These are account-wide: they override nothing per-bot and are overridden by nothing per-bot.
>
> ⛔ **`maxexits` ("Maximum Exit Options Close Attempts") is the dangerous one** — a single switch
> that can cap **every bot's** ability to close. Read **`0` = `Unlimited`** on 2026-08-04, so it is
> **inert today**; the picker also offers `1`–`10` · `15` · `20` · `25` per day. **A non-zero value
> reproduces the exact failure shape of the June lapse with nothing per-bot to show for it.**
> **Record the value, and make it a drift-audit row.**

**Then confirm the comparator is real:** open one arm's row and one shared-object row and read the
decoded bundle and the A7 hash back. **IF either is missing**, the drift detector's Tier C is
**SKIPPED** and the daily loop runs config-blind. **Say so in the brief rather than reporting a green
baseline.**

### Step 5a — ⛔ DST CHECK: does `ntime=1552` actually fire at 15:52 ET in August?
*Added 2026-08-05 on Andy's release (D4/F-7).*

**Why this is a hard gate.** §1 says one toggle kills every Exit Option on a bot at once — which is
exactly why the flat close lives in the Events class. **If it fires at 16:52 ET, the fleet has no
last-resort flat close at all**, which is the single point of failure §1 was designed to remove. The
saved trigger serialised `startDate 2026-08-03T20:52:00.000Z` — **15:52 at UTC−5 (EST), but 16:52 ET
in August (EDT).** Day-0 is mid-August. `ntime` is the operative field and `startDate`'s time
component may be a stamp only. **Nobody has observed which. Do not assume.**

**OBSERVE — on the pilot's backstop automation, on the FIRST trading day the bot is ON:** bot **Log**
tab → filter Type = `Event` → find the backstop's run row → read that row's **`title` attribute**,
**not** the visible group header (the group header is unreliable; the `title` carries a year-bearing
timestamp).

- **IF the `title` reads between `3:52PM` and `3:56PM`** → `ntime` is operative. ✅ **DST CLOSED.**
  Record the verbatim `title` string and the date. Proceed. *(A minute or two of drift is expected —
  automations run on a distributed queue with no guaranteed slot.)*
- **IF the `title` reads `4:5xPM`, or there is NO Event row for the backstop that day** → ⛔ **THE
  BACKSTOP IS DEAD UNDER DST. STOP.** Every bot carrying it is now single-layer. **Do not re-time
  the trigger yourself** — the minute is in `build-plan.md` §2B and §0 says do not improvise a
  change here on the day. Then: (1) set every affected bot's toggles **OFF** and record it;
  (2) emit an instruction card headed **`DST-BACKSTOP-DEAD`** naming every affected bot; (3) hand to
  Andy for an explicit *"amend the plan"*. **Entries stay blocked for those bots until Andy rules.**
- **IF the Log filter returns nothing readable** (chips render labels via CSS, so `innerText` on the
  filters is the empty string) → ⚠️ **do not conclude "no rows".** Read the hidden inputs named
  `date`, `time`, `autotypes` directly, or take it to Andy as UNREAD. ⛔ **An unread DST check is
  treated as the FAILURE branch — those bots stay OFF.**

⚠️ **Re-run this exact check on the first trading day after the November EST transition**, whichever
way it resolves this time.

### Step 6 — Order-level verification, per bot, before it may trade
Two acceptable proofs, in order of preference:
- **Button test-fire**, then read the resulting **Trades list**; or
- allow the bot **one** position — the first-position exception below — and read it the moment it opens.

> ⚠️ **THE FIRST-POSITION EXCEPTION, stated plainly, because Steps 6 and 7 are otherwise circular.**
> *Added 2026-08-05 (D2/F-9).* The Trades list is the only order-level ground truth **and it does not
> exist until a position does.** So: if the test-fire is unavailable, the bot is allowed **exactly
> one** position at **1 lot**, read the moment it opens. `greenfield-family-spec.md` D6 makes the
> same concession — *"Signed ≠ verified."* The test-fire prohibition elsewhere is scoped to the
> **inactive-account build window**, not to Day-0.

**The Exit Options panel is NOT evidence.** Exit Options are copied per-position at open; the panel shows
intent, the Trades list shows what was attached.

For the two control clones the verification is **inverted**: confirm their Trades lists show **no** PT or
exit-trigger rows — the ride behavior is intact and their S2 monitor is firing.

> ⚠️ **THE INVERTED CHECK IS ADVISORY UNTIL D4 IS ANSWERED** *(D6/F-28)*. Whether the account-level
> ITM action appears in a Trades list, **and under what label, is UNOBSERVED.** Until it is read, a
> mislabelled ITM close **reads as a PT row** and would kill a ride control on day one — taking the
> referent of every comparison in the family with it. **Read the label first; fire the rule second.**

> ### ⛔ FAILURE BRANCHES — ORDER-LEVEL VERIFICATION. Added 2026-08-05 (D2/F-5, F-4).
> **IF the Trades list shows no PT row and/or no exit-trigger row** → **bot stays OFF.** Record as
> MECHANICS 🔴 RED with the trade_id. Then, in order: (a) re-observe both dashboard toggles by a
> **fresh** screenshot; (b) re-read the Open Position action's Exit Options **values, not presence**;
> (c) re-drive the toggle once. **Fleet proceeds. Escalate to Andy: YES if it fails a second
> position.**
>
> **IF no position opens at all** → ⬜ **NOT EVALUABLE, which is never a pass. Bot stays OFF.**
> Carry the open card forward.
>
> **IF three or more bots show the same missing row** → ⛔ **STOP. FLEET STAYS OFF. Escalate to
> Andy: YES.** This is the v1 failure repeating, not a per-bot defect.
>
> **IF the button test-fire is unavailable or its result cannot be read** → fall back to the
> first-position exception. ⛔ **Never substitute the Exit Options panel. No exception.**
>
> ### ⛔ THE INVERTED CHECK'S OWN BRANCH — and the generic one is the WRONG action here.
> **IF either control clone's Trades list shows a PT row or an exit-trigger row** → the ride+S2
> control is **CONTAMINATED**; the arm's comparison is **void, not delayed.** ⛔ **Do NOT edit the
> bot to remove it** — `CLAUDE.md` §5 standing exception: *"Do not 'fix' them, do not re-arm them."*
> Capture the Trades list, screenshot the Open Position action. **Bot stays OFF · fleet proceeds ·
> escalate to Andy: YES** (a spec question under decision freeze).
> **IF the S2 monitor shows no firing** → **bot stays OFF · fleet proceeds · escalate: YES.** Zero
> log rows is the liveness RED of Step 8. **Do not read monitor silence as "ride behavior intact."**

> ### ⚠️ THREE MECHANICS NOW AIM AT THE SAME TWO MINUTES — attribute before you conclude. (D6/F-17.)
> Since 2026-08-04 the account runs **`itmpaper` = `market`**, which closes expiring ITM positions
> **10 minutes before the close = 15:50** — the same instant as the bot's own Expiration exit, and
> two minutes before the 15:52 backstop. **An exit-option order stays live two minutes**, so the
> 15:50 order is still working when the backstop fires.
> **Record BOTH rows' timestamps and attribute by the GAP, not the absolute minute** — automations
> run on a distributed queue and the clock is jittered. Feed `time_exit` and `itm_action` to the
> detector as **separate config columns**.
> ⚠️ **After Template V2 lands (§2 step 6a) the three are distinguishable by pricing** — 15:50
> Expiration exit on SmartPricing (`speedy`), ITM action Market, backstop Market-with-memo.
> **Without V2 they are three Market orders in two minutes with only memo strings between them.**

### Step 6a — ⛔ MECHANISM VERDICT: is the toggle actually the cause?
*Added 2026-08-05 on Andy's release (D2/F-8). This is the step that settles §1.*

Run **once**, on the **nine** leave-in-place bots only — the clones and fresh builds were never
lapsed and cannot test it.
**PRECONDITION:** Step 3 done **and** the bot has opened its first new position. Do not run it
earlier.

- **IF toggles read ON *and* the Trades list contains the PT row and the exit-trigger row** →
  ✅ **MECHANISM CONFIRMED.** Record per bot: name, screenshot filename, verbatim PT row text, date.
  Write the verdict into `docs/state.md` and retire the CAUSAL caveat by citing this observation.
- **IF toggles read ON *and* the Trades list shows NO PT row** → ⛔ **MECHANISM REFUTED. FULL STOP —
  this is not a per-bot problem.** §4.5 moves back into contention and the June cause is again
  UNKNOWN. Do all of the following before anything else:
  1. **`AUTOMATIONS` OFF on all nine**, screenshotted. Do not leave a bot opening positions it
     cannot exit.
  2. ⛔ **Do not allow entries on the clones or fresh builds either.** They were built on the premise
     that a correct-from-birth exit stack cannot suffer this failure. **That premise is now
     unproven. FLEET STAYS OFF.**
  3. **Check the competing mechanisms, in order, recording each answer verbatim:** (a) bot Log →
     `Errors` filter, read each row's `title` — any day at or above **10 errors** since re-arm?
     (b) `/settings` → `maxexits` still `0`/Unlimited? (c) `/settings` → Bot Schedule
     `exitstart`/`exitend` — do the window bounds still admit the exit's stamped minute?
     (d) Bid-Ask Guard — was the spread wide at the stamped minute?
  4. **Emit an instruction card headed `LAPSE-MECHANISM-REFUTED`**, repeated at the top of every
     brief until closed, and hand to Andy. ⛔ **Do not diagnose past this point and do not re-arm
     anything.** The cause is a research question, not a Day-0 step.
- **IF no position has opened yet on a bot** → that bot is **UNTESTED, not passing.** ⬜ Do not count
  an untested bot as a confirmation.
- **IF the toggle state is unreadable** → ⚠️ absence of a readable toggle is not an observation.
  Re-screenshot; if still unreadable that bot is **UNTESTED and stays OFF.**

⚠️ **Feed Step 2c's result into this verdict.** If a toggle read ON without intervention at Step 2c,
then re-arm and reactivation were **never** cleanly separated for that bot, and a CONFIRMED verdict
on it is weaker than it looks. Say so.

### Step 6b — 📝 C10 OBSERVATION: the unit of `dstop` (Stop Loss $)
*Added 2026-08-05 on Andy's release (D4/F-16).*

**An observation, not a build. Nothing is re-stamped on Day-0 either way** — Andy re-stamps PR-21.

⛔ **Why it needs its own step.** C10 cannot be read off the modal: it is headed `Stop Loss Amount`,
the only unit marker is a bare `$`, `step=1`, and there is **no per-contract / per-position / per-leg
qualifier anywhere on it.** It needs a **live position whose contract count you wrote down before it
opened.** **That moment exists exactly once. Do not let it pass unrecorded.**

**SET UP:** the 1-lot canary in §3 Step C **is the C10 instrument — run it, and run it at exactly 1
contract.** On the canary only, set `dstop` to a round, unmistakable value (e.g. `-100`) and
**record, before the position opens:** bot name, `dstop` as typed, and **contract count per leg**.

- **IF the stop fired at ≈ −$100 total on the position** → **PER POSITION.** `<D100>` as specified
  by R-1 *"in dollars"* is on the correct basis; the PR-21 re-stamp is a formality. ✅ **C10 CLOSED.**
- **IF it fired at ≈ −$100 × (contract count)** → **PER CONTRACT.** ⛔ **This is the D-6 units
  failure one layer up.** (1) Emit a card headed **`C10-PER-CONTRACT`**; (2) state plainly that
  `<D100>` is off by the contract count and **ARM-B1 must not be built** until Andy re-derives the
  rung and re-stamps PR-21; (3) ⛔ **do not re-derive `<D100>` yourself** — the rung basis is signed
  ruling R-1 and changing it is a plan amendment. **C10 CLOSED, ARM-B1 STILL BLOCKED.**
- **IF it fired at neither figure** → record realised P/L, contract count and leg count; report
  **`C10-UNRESOLVED`**. **ARM-B1 stays blocked. Do not fit a basis to one data point.**
- **IF the canary is not run, or the stop never fires, or the count was not recorded first** →
  ⚠️ **C10 stays OPEN. Say so** in `docs/state.md` and at close-out. ⛔ **Do not infer the unit from
  `dstop` persisting as a negative number** — that is a sign convention, and it is **inadmissible as
  the answer.**

### Step 7 — Only now allow entries: `AUTOMATIONS` → ON, per bot
*⛔ **Amended 2026-08-05 on Andy's release (D3).** This is where `AUTOMATIONS` is switched on — not
Step 3.*

Hard gate, not a preference. A bot that cannot be proven stays OFF until it can.

**For each bot that passed Step 6** — and **only** those — set **`AUTOMATIONS` → ON** and screenshot.
**A bot that did not pass Step 6 does not get this step**, including any of the nine.

> ### ⛔ AMENDED 2026-08-07 ON ANDY'S EXPLICIT "AMEND THE PLAN" — RE-READ THE TOGGLE BEFORE EVERY SWITCH-ON.
> *Authorization is scoped to **this line only**; nothing else in this runbook was touched.
> Cross-reference: `day0-session-pack-2026-08-07.md` §0.0 **A-27a**.*
>
> **Before any bot's `AUTOMATIONS` goes ON, re-read that bot's `EXIT OPTIONS` toggle state
> FIRST-HAND. Never inherit it from an earlier session** — not from a close-out, not from
> `data/bots_config_v2.csv`, not from the session pack. **A re-read that returns OFF is a NEW
> FINDING, not a silent re-arm:** record it, escalate to Andy, and do not switch that bot on.
>
> **[Forcing evidence, dated first-hand 2026-08-07 (S0b-RESUME):** the pilot
> `QQQ-IC-0DTE-Fortress` read `disableExits: 1` (EXIT OPTIONS **OFF**) against its own 2026-08-04
> capture, which records `EXIT OPTIONS ON (input[name=onoff].value="true")` verbatim. That is the
> **eighth of eight** bots examined to show the same reset, after the seven greenfield arms S0a
> found and re-armed.**]** ⛔ **The inference that matters: a state that was reset once can be
> reset again.** The seven bots S0a armed cannot be assumed still armed at Step 7. A recorded ON
> is a fact about the moment it was read, not a property of the bot.
>
> ⚠️ **Re-reading is NOT re-doing Step 3.** Step 3 arms `EXIT OPTIONS`; this is a verification
> immediately before the switch-on, and it does not license a second pass over the seven.
> ⚠️ Cheapest instrument, first-hand 2026-08-07: the `/bots` list carries **both** toggles per row
> on `i.sticon`'s **`title`** attribute — all 41 bots in one page read, no bot page opened.
> (Text capture misses this; §1.5/§1.6 of `oa-ops-runbook.md` explain why. A-27d.)

⛔ **IF Step 6a returned MECHANISM REFUTED, no bot gets this step. FLEET STAYS OFF.**

### Step 8 — Day-1 monitoring
Liveness check: every ON bot must show a position **or** a scanner run in the capture window. OA bot logs
record non-actions, so **zero log entries = presumed OFF or Failsafe-tripped → RED.**
Same-day engine-death checks: the expired:closed ratio flip, and any position with `mfe_pct` ≥ its declared
PT and no PT order. Any RED emits an instruction card, repeated at the top of every brief until closed.

> ### ⛔ WHAT RED DOES — a card is a question, not an action. Added 2026-08-05 (D2/F-23).
> An instruction card is a **notification with an address.** It is **not a disposition.** On Day-1
> each RED also carries one:
>
> **IF zero log entries for an ON bot in the capture window** → **the bot is switched off pending
> investigation** (PR-05's liveness kill). **Fleet proceeds. Escalate to Andy: NO on day 1; YES if
> unresolved after two sessions.**
> ⚠️ **Distinguish the windows:** PR-05's *kill* criterion is a **10-session** window; this Day-1
> check is **one** capture window and switches the bot off to be re-armed — **it does not retire the
> bot.**
> ⚠️ **`SILENT_BOT` can never be RED from position data alone** — only the bot log closes it. If the
> log cannot be read the verdict is ⬜ **NOT EVALUABLE, never GREEN.**
>
> **IF `mfe_pct` ≥ declared PT with no PT order, or the expired:closed ratio flips** → **bot stays
> OFF from the next session** until a Trades list proves the PT row exists. **Fleet proceeds.
> Escalate to Andy: YES** — this is the exact 2026-06 signature.
>
> **IF `BACKSTOP_CAUGHT_IT` fires** → **the Exit-Options side is dead even though nothing was lost
> that day.** **Bot stays OFF. Escalate to Andy: YES.**

---

## Pre-Day-0 checklist

> ### ⛔ BLOCKER CLASSIFICATION — added 2026-08-05 on Andy's release (D6/F-24). Read before ticking.
> Until now no box carried a marker, so all of them could be unticked on the morning of Day-0 with
> nothing to say whether that mattered.
> - ⛔ **HARD BLOCKER** — **§4 does not start until this is ticked.** No exceptions, no partial credit.
> - ⚠️ **PER-BOT BLOCKER** — an unticked box blocks only the bots it names; the fleet proceeds.
> - 📝 **ADVISORY** — Day-0 proceeds; the gap is logged and carried as an open card.
>
> **IF any ⛔ box is unticked on the morning of Day-0 → do not pay, do not re-arm. Escalate to
> Andy: YES.**

- [x] ~~Support's re-arm procedure~~ — **ANSWERED, see §1** *(⚠️ the **procedure**; the **cause** is
      not — §1 as corrected 2026-08-05, and §4 Step 6a settles it)*
- [ ] ⛔ `LEDGER_START` implemented in `build_ledger.py` and defaulted to refuse pre-cutover rows
- [ ] ⛔ **`itmlive` = `market` set, hard-reload verified, before/after screenshots on file** — §4
      Step 0a. *(Added 2026-08-05, D1. `itmpaper` is already `market`; do not re-set it.)*
- [x] ~~`data/mirror_baseline.csv` written — the one-time frozen pre-lapse snapshot for the 7 mirrors~~
      — ✅ **WRITTEN 2026-08-04** (174 positions, 10 mirrors, zero excluded). ⛔ **It is an anchor —
      do not recompute it and do not pass `--force`.**
- [x] ~~⛔ `data/raw/` + `data/brief/` pre-cutover files resolved (filtered or moved to `data/archive/`)~~
      ⛔ **AMENDED 2026-08-07 ON ANDY'S EXPLICIT "AMEND THE PLAN" — THIS BOX ONLY. Original struck,
      left standing.** The parenthetical prescribed **moving or deleting files, and that is now the
      wrong action.** ⭐ **THE BOX'S PURPOSE IS THAT NO PRE-CUTOVER ROW REACHES THE WORKING
      LEDGER.** It is satisfied by `build_ledger.py`'s own counts in `data/ledger_meta.json` —
      `export_rows` / `post_cutover` / `straddler` / `pre_cutover` discarded — and **NEVER by a
      directory listing, a file move, or a deletion.** An empty `data/raw/` proves nothing; a
      1,386 → 0 filter proves the cutover works under load.
      ✅ **SATISFIED 2026-08-07, first-hand, under real load:** `export_rows 1386 · post_cutover 0
      · straddler 0 · pre_cutover 1386 discarded · WORKING LEDGER n=0`, `ledger_start 2099-01-01`,
      `source_export 2026-08-07.csv`. That is the cutover **working**, not a null result.
      ⛔ **`data/raw/2026-08-07.csv` IS THE LIVE EXPORT AND IS DO-NOT-DELETE.** It is filed exactly
      where `oa-ops-runbook.md` §1.7 and `daily.sh`'s own header ("drop the OA positions CSV in
      `data/raw/` named `YYYY-MM-DD.csv` first") say the export belongs. It is stage 1's input, not
      contamination. Removing it breaks the ledger build.
      ⛔ **THIS BOX COVERS `data/brief/` TOO, AND `data/brief/` IS ALSO NO LONGER EMPTY.** Same
      rule, no exception: **a populated `data/brief/` is WORKING OUTPUT, not contamination.** It
      holds `2026-08-08_tape.json`, a **gate-A9 test artifact** written on a **Saturday** with an
      empty payload — correct degradation, labelled in place, and **not to be read as a real
      brief.** Neither directory is expected to be empty from Day-0 onward.
      *Wording matches the three corrected surfaces in `day0-session-pack-2026-08-07.md` (S0
      Step 8, the §1 pre-flight list, and the S1 hand-off checklist) so the two documents agree.*
- [ ] ⚠️ `execution_audit.py` passing its validation matrix against the frozen 35-row fixture, surfacing
      **both** T00147 and T00845 and staying silent on the R>1 winners — an unpassed matrix means Tier C
      **reports SKIPPED with a reason, never silence**; Day-0 proceeds with the blind spot on the page
- [ ] ⛔ A **pre-registration entry, SIGNED,** for every one of the ≈18–20 active bots — including the
      untouched nine — dated before its restart. **Per bot: no entry, no restart.** §4 Step 2b.
- [ ] 📝 `oa-platform-reference.md` and `hedge-research.md` rewritten from the archive (they gate the
      greenfield and tournament builds)
- [ ] ⛔ Sizing decided and written down: 1 lot for experiments, ≈$5K risk/position for CANDIDATE+,
      identical allocation across tournament arms. **Set once, here — never ad hoc later**
      (`CLAUDE.md` §5). If it is not written down before Step 3, it will be set mid-sample.
- [x] ~~Clone ritual **piloted on `QQQ-IC-0DTE-Fortress`** and clean before any other clone or build~~
      — **DONE 2026-08-04, end to end, archive confirmed** (§3 Step A). Remaining on the pilot:
      Template V2 and Bot Group — neither is a re-run.
- [x] ~~`data/archive/rename_map.csv` started~~ — **row written 2026-08-04**
- [ ] ⛔ **Template V2 saved on the pilot, with its AMENDED pre-registration signed** — §2 step 6a.
      *(Added 2026-08-05, D1. Ruled 2026-08-04; execution was deferred as part of the ruling.)*
- [ ] ⛔ `daily.sh` dry-run at n=0 passes — every script degrades gracefully on an empty ledger
- [ ] ⚠️ All ≈18–20 pre-registration entries **drafted** during the build window — **plus up to 8
      Track B arms, ceiling 28** *(corrected 2026-08-05, D1)*
- [ ] ⛔ Ride-or-close decision prepared, **signed, and ready to EXECUTE** for the 5 open mirror
      positions (`QQQ long call` ×4, `Tasty Condor` ×1) — §4 Step 2. **A logged call is not a
      disposition.**
- [ ] ⛔ **Phase 0 checks `C0c · C2 · C7 · C8 · C9` answered, and the A7 payload-hash baselines
      recorded** — §4 Step 4. *(Added 2026-08-05, D4.)* ⚠️ **C10 is open and blocks ARM-B1**; it is
      observed on Day-0 at Step 6b, not before.
- [ ] 📝 **Deferred Day-0 observations queued with their decision trees:** no-touch (Step 2c) · DST
      (Step 5a) · mechanism verdict (Step 6a) · C10 `dstop` (Step 6b) · the 15:50 attribution
      (Step 6). **Any one left unread at close-out is reported as OPEN, never as passed.**
