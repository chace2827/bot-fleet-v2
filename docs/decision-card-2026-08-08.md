# Decision card — 2026-08-08

*One card, six ruling slots: the remaining Day-0 batch, prepared so it can be ruled in one
sitting. Slots 1–5 are the five items the 2026-08-07 amendment pass routed to Andy and did not
rule — **A-02** (`LEDGER_START` semantics), **A-11** (the first-position control), **A-12** (the
`dstop`-read instrument), **A-24** (S2 Step-0's residue) and **gate A8**'s one surviving signature
item (**PR-18**'s naming, per **A-04**). Slot 6 is **A-27(c)**'s Step-4b precondition, with the
capture worklist attached so the ruling and the work to discharge it arrive together.*

*Written against fresh device reads of every cited file — no memory, no staged-copy quotes, no OA
surface touched, no browser tool run, no git command run (including `status`). Every quoted phrase
was asserted byte-exact against the device file by a `device_bash` `grep -cF` with the match count
stated; the sha256 set and the assert table are in the Verification appendix. **No OA fact in this
card comes from memory. Where a fact could not be read from the folder it is written `UNVERIFIED`.***

**⛔ THIS CARD DECIDES NOTHING.** Every "RECOMMENDATION" below is a recommendation and is labelled
as one. Nothing here is a ruling, nothing here was applied, and no file in the folder was edited by
the session that wrote it except `docs/session-log.md`, `docs/state.md` and this file.

**How to rule:** one line per slot. The Ruling Sheet below is copy-paste ready. Gated surfaces move
only under an explicit **"amend the plan"** (`CLAUDE.md` §5). Three slots carry a **consequential
amendment** — an edit that becomes necessary *whichever way* the slot is ruled; each is flagged
in-slot and listed again at the end of the Ruling Sheet so none is discovered later.

---

## RULING SHEET — copy, fill, send

```
1. A-02 · LEDGER_START semantics            >>> RULED 2026-08-08: LEDGER_START = 2026-08-10 <<<
   The post-cutover era begins at:      MONDAY 2026-08-10 OPEN — the first market session on or
                                        after switch-on. NOT the 2026-08-07 payment date.
   1a. build-plan.md §3 amend:          AMEND THE PLAN: YES (delegated) — APPLIED
   Slip: FIXED at 2026-08-10 (delegated). See RULINGS section for the verbatim text.

2. A-11 · the first-position control        >>> RULED 2026-08-08: A THEN B; 2a = NO <<<
   Mechanism for Step 6's one-position read:
                                        TEST-FIRE FIRST (mandatory), THEN posLimitDay=1
                                        AUTHORIZED one bot at a time, screenshotted, REVERTED
                                        and the revert HASH-PROVEN. C DECLINED. D is the
                                        per-bot fallback.
   2a. RULED NO — verification action, not a spec change; logged in the entry.

3. A-12 · the C10 `dstop` instrument        >>> RULED 2026-08-08: "C for Day-0, A as the queued path" <<<
                                        C10 STAYS OPEN for Day-0. PR-20 not edited, pilot
                                        declined. TESTOPS-LAB-DSTOP is the queued instrument,
                                        gated on E-3 verified + signed PHASE LOG + a Lab slot.

4. A-24 · S2 Step-0's residue              >>> ALL FOUR RULED 2026-08-08 <<<
   (i)   Template V2 on the pilot:      PILOT STAYS OFF — V2 to a build window w/ amended PR-03
   (ii)  C9 as a pre-switch-on read:    RUN AS A READ AT STEP 0 (read only, never a write)
   (iii) A7 not wired into daily.sh:    TRADE, with hand-run a_series.py --validate + --json at
                                        EVERY close-out; 4th object named as an OPEN GAP; A7
                                        reports 3/4 VERIFIED + 1 FIRST BASELINE, never 4/4
   (iv)  gate A9:                       CONFIRMED as a rule AND ALREADY SATISFIED — CLOSED
                                        2026-08-08 on Andy's own 8/8 n=0 run. BOX TICKED.

5. Gate A8 · PR-18's name                  >>> RULED 2026-08-08: OPTION C, THE SPLIT <<<
                                        "Breakeven" = LEDGER / INTERNAL label.
                                        MECHANICAL name (SL100 / stop at 100% of credit) in
                                        anything PUBLISHED or EXTERNALLY COMPARED, CF-1 caveat
                                        attached at that surface. CF-1 NOT discharged.
                                        OA bot name GF-QQQ-IC-SL100 unchanged. FIELD FILLED.
   5a. RULED YES — state.md's CF-4 bullet amended to match. GATE A8 IS CLOSED.

6. A-27(c) · Step-4b                       >>> RULED 2026-08-08: OPTION 2. S2 MAY OPEN. <<<
                                        2. AMEND A-07's SCOPE — ESTABLISHED hash required only
                                           where a pre-restore baseline exists; the rest carried
                                           ⬜ NOT EVALUABLE **in the CONFIG HASH field itself**.
                                           Capture on the first day each bot trades.
                                           Options 1 and 3 DECLINED, on the record.
   6a. RULED YES, PURE READ — does NOT spend Step 2c. Read only; no write of any kind.
   6b. RULED ACCEPT AND RECORD — 20 Group-A bots named, not brought into scope, not archived
       by this ruling; still covered by the ~23 archives queued for Andy's hand.
```

**Consequential amendments — required whichever way the slot goes.** Listed so they are ruled
here rather than discovered inside Day-0. Each is a **gated** edit (`CLAUDE.md` §5: it changes what
gets built, or it is ambiguous, so it is gated):

| # | Slot | Surface | Why it is needed either way |
|---|---|---|---|
| CA-1 | 1 | `build-plan.md` §3 · `scripts/build_ledger.py` line 68 | The constant currently reads `"UNSET"` and §3 defines `LEDGER_START` as *"the Day-0 reactivation date"* — a phrase that now names two different days |
| CA-2 | 5 | `docs/state.md` CF-4 bullet | It still carries the pre-2026-08-06 text; the spec discharged CF-4. The two documents disagree today |
| CA-3 | 6 | `day0-session-pack` §0.0 A-27(c) | Its "12 of the 14" count and its own named list disagree by one — see slot 6, §A |

---

# ✅ RULINGS — 2026-08-08 SITTING (Andy attending, ruled live)

*Recorded verbatim as ruled, in slot order. Each entry: Andy's words, then what the ruling
authorized and where it was applied. Applied same session; every edited file verified by direct
`device_bash` sha256 + single-match grep (`CLAUDE.md` §9.1a) — never a stage-back read. No OA
surface touched, no browser tool loaded, no git command run, including `status`.*

## SLOT 1 — A-02 · `LEDGER_START` semantics — ✅ **RULED 2026-08-08**

**Andy, verbatim:** *"We are turning them on today or tomorrrow to start recofrding data starting
monday open. so Aug 10 should be day=o"*
On sub-choice **1a** and the slip condition, verbatim: *"WHatever you suggest"* — recorded as an
**explicit delegation** of the two sub-choices, not as a session choice; the date itself is Andy's.

**THE RULING.** **`LEDGER_START` = `2026-08-10`.** The post-cutover era begins at **Monday
2026-08-10's open** — the first market session on or after switch-on. Not the 2026-08-07 payment
timestamp, and not a non-trading day on which a toggle happens to be flipped. Switch-on is
expected 2026-08-08 or 2026-08-09 (both non-trading days), so the first `AUTOMATIONS`-ON day and
the first tradeable session are the same day: 2026-08-10.

**1a — CA-1: AMEND THE PLAN — YES** (delegated, applied). `build-plan.md` §3's *"the Day-0
reactivation date"* named two different days once payment and Day-0 separated; §1's echo carried
the same phrase. Both now carry the ruled date behind a dated amendment banner, originals standing.

**Slip condition — FIXED DATE** (delegated, applied). `LEDGER_START` stays `2026-08-10` even if
switch-on slips past Monday's open. A bot that is OFF opens nothing, so a floor of 2026-08-10
admits no row it should not; a moving date buys nothing and costs a second amendment. The
`n=0` verification is still run at Day-0 Step 1 and again at close-out.

**⚠️ SUPERSEDES a prior Andy ruling, on its face.** `state.md` (S0a 2026-08-07 and S0b 2026-08-07)
carries: *"the day you switch the first bot on IS `LEDGER_START`"*. With switch-on on a Saturday
or Sunday that text yields 2026-08-08/09. Today's ruling resolves the weekend case the 08-07
ruling did not anticipate. Both blocks corrected in place with dated banners, originals standing.

**Applied to:** `docs/build-plan.md` §1 + §3 (CA-1, amend-the-plan) · `docs/state.md` S0a and S0b
blocks (superseded-ruling banners) · this card.
**Queued, NOT done here:** `scripts/build_ledger.py` line 108 — `LEDGER_START = "2026-08-10"`,
set **at Day-0**, per that script's own line-151 instruction. Acceptance: `bash scripts/daily.sh`
runs stage 1 without the refusal path and reports `n=0` on 2026-08-10 pre-open, and again at
close-out.
**Residuals, named not silently carried:** (a) `reactivation-runbook.md` §4 Step 1 line 382 —
*"Note the exact timestamp. **This date is `LEDGER_START`.**"* — still assumes payment == Day-0;
it is a decision surface and is **not** in CA-1's named scope → folded into the slot-8 doc batch.
(b) `state.md` "Account" section (*"OA subscription **INACTIVE**… The reactivation date is
**Day-0 = `LEDGER_START`**"*) is stale on a larger fact than this ruling → left standing, named
here.

## SLOT 2 — A-11 · the first-position control — ✅ **RULED 2026-08-08**

**Andy, verbatim:** *"Your reccomendation"* — an explicit delegation to the card's recommendation
for this slot, recorded as a delegation.

**THE RULING: A THEN B, WITH 2a = NO.**
1. **Attempt the button test-fire first**, one bot, record verbatim whether the control exists.
   Mandatory and unchanged; absence is concluded only after the surfaces are opened.
2. **If it does not exist, `posLimitDay` = 1 is AUTHORIZED** (and `posLimit` = 1 where separately
   settable): **one bot at a time, never a batch**; screenshot before and after; read the Trades
   list the moment the position opens; **revert immediately after the read**.
3. **2a = NO** — a temporary limit does not fork the Step-2b signature. Declared, dated, reverted;
   alters no mechanic, no exit bundle, no matched field. ⛔ **Rider added at the sitting: the
   revert is PROVEN, not asserted** — re-capture and re-hash after reverting; the hash must return
   to its pre-change value, and **if it does not, that IS a fork** and the entry stops for a fresh
   signature.
4. The change, the read and the revert are **logged in that bot's pre-registration entry**, dated,
   citing this ruling.
5. **Option C DECLINED** (switch on at 2/2 or 10/10 and read whatever opens — uncapped exposure).
   **Option D is the per-bot fallback** where step 2 cannot be executed: Step 6 ⬜ NOT EVALUABLE,
   bot stays OFF.

⚠️ **Ordering, restated because it is now live:** the mechanism only does work if `AUTOMATIONS`
goes ON **at Step 7 and not before**. A bot switched on ahead of S2 opens at its stored limit
(`10/10` on the champion clone) with Step 7 gating nothing.

**Applied to:** `docs/day0-session-pack-2026-08-07.md` — **both** A-11 surfaces (§0.0 amendment
block and the S2 Step 6 restatement) · this card.
**Residual, named not silently carried:** `reactivation-runbook.md` §4 Step 6 carries the
identical hole, is a decision surface, and A-11 itself says it *"is not this session's to edit"* →
**routed to the slot-8 doc batch** for an explicit scoped "amend the plan".
**Queued, NOT done here:** the per-bot pre-registration log lines are written at Day-0, as the
edits happen.

## SLOT 3 — A-12 · the C10 `dstop` instrument — ✅ **RULED 2026-08-08**

**Andy, verbatim:** *"C for Day-0, A as the queued path"* — the card's recommendation, ruled as
stated.

**THE RULING.** ⛔ **C10 STAYS OPEN for Day-0.** No instrument runs it on the day. **PR-20 is not
edited** (A-12(a)) and **candidate B, the pilot, is DECLINED** — its capture hash is NOT
ESTABLISHED (S0b-1) so it opens nothing, and at 1 lot it could not discriminate even if it did.
C10 is **named OPEN by name in `state.md` and again at Day-0 close-out**, per A-12's own
requirement. **ARM-B1 stays blocked** — where it already is — and **PR-21 stays unstamped**.

**The queued path is `TESTOPS-LAB-DSTOP`** (`exploratory-bots-design-2026-08-07.md` §2.2): the only
candidate that can discriminate, 3 contracts being the minimum count separating all four candidate
bases on a 2-leg vertical, with ≥3 firings required before it may report. ⛔ **This ruling does NOT
authorize building it.** Unchanged preconditions, all of which must hold first: E-3's three
exclusion surfaces implemented **and verified** (implementation landed 2026-08-08; the toggle gate
still needs Andy's go), a **signed `PHASE LOG`** (guardrail G8), and one of the **≤2 Lab ops slots**
(E-1). Build-window decision, not a Day-0 one.

**Applied to:** `docs/day0-session-pack-2026-08-07.md` — **both** A-12 surfaces (§0.0 A-12(a) and
the S2 Step 6b restatement) · this card · `docs/state.md` (C10 named OPEN, in the sitting block at
close-out).
**Residuals, named:** no `pre-registration-ledger.md` §6a entry is created for `TESTOPS-LAB-DSTOP`
— naming a Lab bot is a pre-registration act and is **not** authorized by this ruling. A-12(b)'s
contract-count rule (total contracts, not per leg; report `C10-UNRESOLVED` if the two figures are
equal) stands unchanged and applies whenever C10 is eventually run.

## SLOT 4 — A-24 · S2 Step-0's residue — ✅ **ALL FOUR RULED 2026-08-08**

**Andy, verbatim:** *"your reccomendation"* — delegation to the card's recommendation on all four
items, ruled one at a time as A-24 requires.

**(i) Template V2 on the pilot — NOT finished at Step 0; THE PILOT STAYS OFF.** Finishing V2 is a
spec change plus a signature, and the pilot already stays OFF independently on S0b-1's
NOT-ESTABLISHED hash — so doing it inside Step 0 buys nothing for Day-0. V2 lands in a build window
with its amended PR-03. ⛔ The 15:50 exit is not re-priced on Day-0.

**(ii) C9 — RUN AS A READ AT STEP 0.** The family does **not** stay off. ⛔ Read only, never a
write, never an improvised spec.

**(iii) A7 unwired — THE FAMILY TRADES, with a hand-run detector.** `scripts/a_series.py
--validate` **and** `--json`, by hand, **at every close-out**, from Day-0 on. The honest state goes
on the page: a hand-run tool at **3 of 4** shared objects, not a nightly. ⛔ The 4th object,
`Defang-Mon-S2-StrikeTouch` (A-13), is **named as an open gap at every close-out** — its 2026-08-08
sweep entry is a **FIRST BASELINE, not a pass**, so A7 reports **3/4 VERIFIED + 1 FIRST BASELINE,
never 4/4**. Wiring into `daily.sh` stays a queued Claude Code task, not a Day-0 action.

**(iv) Gate A9 — CONFIRMED as a rule, and ALREADY SATISFIED.** §4 does not start until Andy's own
clean end-to-end `daily.sh` n=0 run is on file, and a session's report of its own run is not that
check (`CLAUDE.md` §9.1a). ⛔ **It is on file — gate A9 CLOSED 2026-08-08** on Andy's own 8/8 run
(`execution_audit.py` v1.1.0 + `daily_brief.py` loader fixes; matrix 21/21 unchanged; Tier C
SKIPPED BY NAME). **The box is TICKED.** Split (ii), the Tier-C contract reconciliation, stays open
and does **not** gate Day-0.

**Applied to:** `docs/day0-session-pack-2026-08-07.md` — **both** A-24 surfaces (§0.0 amendment and
the S2 Step 0 restatement) · this card · `docs/state.md` (ruled facts, at close-out).
**Residuals, named:** the Template-V2 build-window task and the `daily.sh` A7 wiring are **queued,
not scheduled** — neither has a date attached by this ruling. A-13's 3-of-4 gap is now a standing
close-out line rather than a closed item.

## SLOT 5 — Gate A8 · PR-18's name — ✅ **RULED 2026-08-08. GATE A8 IS CLOSED.**

**Andy, verbatim:** *"Card's RECOMMENDATION: C"*. On sub-choice **5a**, verbatim: *"YES and for the
remainging items, lets go with your suggestions"* — 5a ruled **YES**, and slots 6–10 delegated to
the card's recommendations (recorded at each of those slots).

**THE RULING — OPTION C, THE SPLIT.** **"Breakeven" is the LEDGER / INTERNAL label** for PR-18.
CF-4 was discharged 2026-08-06 by the C8 ruling — sibling-close is not built, the untested side is
left to decay exactly as the anchor assumes, so the arm can reach the shape its anchor describes
and is entitled to the name on the merits. **The MECHANICAL name — `SL100` / "stop at 100% of
credit" — is used in anything PUBLISHED or COMPARED EXTERNALLY**, and ⛔ **the CF-1 caveat is
attached at that surface**: the exit-pricing / ITM-exposure confound is **NOT** discharged, is
unrelated to sibling-close, and bounds what the family can conclude against a public anchor. The OA
bot name `GF-QQQ-IC-SL100` is unchanged — nothing renames anywhere. **PR-19 (`SL200`) follows the
same convention by construction.**
⚠️ **Cost accepted with the ruling:** two labels for one arm, and the wrong one leaking into a
brief is the standing risk.

**5a / CA-2 — RULED YES.** `state.md`'s CF-4 bullet carried the **pre-discharge** finding as a live
fact. Corrected: original left standing, dated banner records CF-4's 2026-08-06 discharge and this
ruling. The old instruction *"do not publish it under the anchor's name"* **survives for
publication** and is **superseded for the ledger** — it was incomplete, not wrong.

**⭐ GATE A8 IS NOW CLOSED IN FULL:** (i) G-12b **SIGNED** · (ii) PR-18's name **RULED 2026-08-08**
· (iii) G-1′ **DECLINED**. ⛔ None of the three is re-presented.

**Applied to:** `docs/day0-session-pack-2026-08-07.md` (§0.0 A-04 item (ii) **and** the S2 Step 2b
restatement) · `docs/greenfield-family-spec.md` (PR-18 naming block, original struck text standing)
· `docs/pre-registration-ledger.md` (new **`NAMING`** field on the hedge-arms entry — the field
that held it UNSIGNED under §7 item 2 is now resolved) · `docs/state.md` (CF-4 bullet, 5a) · this
card.
**Residuals, named:** the entry is still **UNSIGNED** for the ordinary reasons — `CONFIG HASH` is
`<capture> @ <hash> per arm` and `SIGNED` is blank. Gate A8 no longer blocks it; Day-0 signing does
the rest. CF-1's publication bound is now carried in four places and must travel with any external
comparison.

## SLOT 6 — A-27(c) · Step-4b — ✅ **RULED 2026-08-08. THE S2 PRECONDITION IS DISCHARGED.**

**Andy, verbatim:** *"YES and for the remainging items, lets go with your suggestions"* — a blanket
delegation to the card's recommendations for slots 6–10, given after slot 5. Recorded as a
delegation; the honest cost of the declined branches is restated below rather than assumed away.

**THE RULING — OPTION 2, AMEND A-07's SCOPE.** An **ESTABLISHED** config-capture hash is required
**only where a pre-restore baseline exists**. The bots without one are carried explicitly **⬜ NOT
EVALUABLE**, **not** as blockers — Day-0 proceeds with the blind spot **named on the page**, which
is how this folder already handles unrunnable checks (`reactivation-runbook.md` §4).

**Declined, on the record.** **Option 1** *"establishes nothing about the past"* by A-27(c)'s own
words — a first capture taken after the restore cannot distinguish a faithfully restored bot from a
rolled-back one — and it costs eleven hand captures before S2 opens for zero retrospective
assurance. **Option 3** permanently forecloses **Step 6a**, the step the runbook calls *"the step
that settles §1"* (the verdict runs on the nine leave-in-place bots ONLY), and strands the five open
mirror positions.

**Riders, all applied:**
1. ⛔ **In the field, never a footnote.** Each affected pre-registration entry now carries the
   ⬜ NOT EVALUABLE carry **inside its `CONFIG HASH` field**, citing this ruling by date.
2. **A capture is taken on the first day each bot trades.** Forward drift detection starts one day
   late instead of never. This is a **worklist, not a precondition on S2**.
3. **6b — ACCEPT AND RECORD.** The **20 Group-A bots** are in no post-restore config check
   anywhere; that is now written down. Not brought into scope, not archived by this ruling; still
   covered by the ~23 archives queued for Andy's hand.

**6a — PURE READ, ruled explicitly.** Opening any of the nine for a capture **does not spend Step
2c**: A-09b already ruled that observation ⬜ NOT EVALUABLE (`NO-TOUCH OBSERVATION CONFOUNDED —
RESTORE`, gate A0 Branch 1), and the 2026-08-08 sweep attested by name that the nine were not
opened and Step 2c is unspent. ⛔ **Pure read means read** — no edit, no toggle, no rename, no save,
no archive, no template. S0b's narrower *"do not touch… in any way"* is superseded **for reads
only**.

**⭐ WORKLIST CORRECTED 11 → 9, on this card's own §B condition.** §B said to check S1's close-out
before capturing bots 10 and 11. **S1 has closed.** A direct listing of
`data/captures/2026-08-08-clones/` this session shows both un-started clone originals now hold
post-restore step-0 baselines (`PR-02-step0-baseline-…-130PM.txt`,
`PR-04-step0-baseline-…-NoPT50.txt`, the latter with an original-side toggle screenshot), and both
are renamed `-ARCHIVED-2026-08-08` and **will not trade** — so rider 2 cannot apply to them.
**Live capture worklist = the NINE leave-in-place bots.** NOT-ESTABLISHED total is still **12 of
14**; this corrects the worklist, not the disposition arithmetic.

**Applied to:** `docs/day0-session-pack-2026-08-07.md` (§0.0 A-27(c) ruling block, the S2
opening-precondition restatement, and a dated worklist correction on the CA-3 banner) ·
`docs/pre-registration-ledger.md` — the carry written into **nine** `CONFIG HASH` fields: **PR-05,
PR-06, PR-07, PR-08, PR-09, PR-10, PR-11, PR-12, PR-13** · this card · `docs/state.md` at close-out.
**Residuals, named:** eleven bots trade or sit with **no pre-restore config baseline of any kind** —
that is the state of the repository, named rather than papered over. The two archived originals'
capture sets remain incomplete (no Exit-Options PDF; `-130PM` has no original-side toggle
screenshot and no input-chain resolution) and, since neither will trade, **are not being completed**.

## SLOT 7 — PR02-R2 · the "Symbols panel is NOT empty" line — ✅ **RULED 2026-08-08**

**Andy:** covered by the blanket delegation recorded at slot 5 (*"for the remainging items, lets go
with your suggestions"*).

**THE RULING — option (a): APPLY AS AN EVIDENCE-BACKED CORRECTION** (`CLAUDE.md` §5, CA-3 class:
dated banner, original left standing, dated first-hand observation cited, verified by device
sha256 + single-match grep). The blanket assertion *"It is NOT empty — look at it again"* is
**false for automation-resident-symbol families**, observed first-hand 2026-08-08 on **both** PR-02
sides — clone and original both read *"No symbols yet"*, symbol resident as `Loop SPX` + action
`symbol: SPX`; same recorded for PR-01.

**⛔ The check is NOT skipped — it is BRANCHED.** First determine which kind of bot you have:
- **Bot-Symbols-loop bot** → the panel must be non-empty and match character-for-character; the
  existing STOP branch applies in full. **This is the real trap.**
- **Automation-resident-symbol bot** (`Loop <SYM>` + action `symbol: <SYM>`) → *"No symbols yet"* is
  the **correct and expected** state on both sides. Verify the original reads the same and that the
  automation carries the symbol. ⛔ Do **not** "restore" symbols into such a bot's panel — that is
  an unrequested config change.

**Rationale, kept on the page:** a checklist line that cries wolf on every automation-resident bot
trains sessions to wave the check through — which is exactly when the real Bot-Symbols-loop trap
gets missed.

**Applied to:** `docs/day0-session-pack-2026-08-07.md` §S1 step 4 · this card.
**Residual, named and routed:** `reactivation-runbook.md` carries **two** echoes of the same
falsified assertion — §2 step 3's *"It is **not empty**. Look at it again…"* (line ~130) and the
WHAT-"CLEAN"-MEANS item 3, *"The clone's Symbols panel is non-empty and matches Step 0
character-for-character"* (line ~214). The runbook is a **decision surface** → **routed into the
slot-8 doc batch**, not corrected here.

## SLOT 8 — the doc-correction batch — ✅ **RULED 2026-08-08. AMEND ALL FIVE.**

**Andy:** covered by the blanket delegation recorded at slot 5. `reactivation-runbook.md` is a
decision surface, so this is the explicit **"amend the plan"** for every runbook item below.
**The batch grew from three to five** — slots 1, 2 and 7 each produced a runbook residual that was
routed here rather than left dangling.

| # | Item | Surface | What changed |
|---|---|---|---|
| 1 | **PR02-R3 / A-16b** | `reactivation-runbook.md` §2 step 7 | The pre-F-C1 *"do not remove PT25 yourself · bot stays OFF"* branch is **struck and replaced**: **F-C1 is RULED: REMOVE** (Andy, first-hand 2026-08-07). Remove only `profits`/`smprofits`, in place; do not rebuild the action; STOP if it cannot be cleared in place. Ends the pack-vs-runbook contradiction A-16b told sessions to work past. |
| 2 | **PR04-R1** | pack §S1 clone prompt, steps 0 and 7 | *"hash all four of its automations"* is a **PR-02 inheritance, not a constant**. Read as **all of them, whatever the count** — `-130PM` has 4, `-NoPT50` has **2**, so its proof is 2 of 2, complete not partial. ⛔ A count of 2 is not a missed capture. |
| 3 | **FS-3** | `docs/state.md` PR04-R2 note · `oa-ops-runbook.md` §5 trap 1 | **The Automation Library is at `/bots/automations`.** `/automations` does 404 but was never its path. Evidence: the `/bots` Library button's own `data-ui` menu JSON, read first-hand 2026-08-08; the Library was then enumerated there (1 folder, 4 objects, 7/7/7/2). PR04-R2's reasoning is unaffected — only the "unreachable" cause is corrected. |
| 4 | **from slot 1** | `reactivation-runbook.md` §4 Step 1 | *"This date is `LEDGER_START`"* struck: the payment timestamp is **not** `LEDGER_START`. **`LEDGER_START` = `2026-08-10`**, fixed. The "set it before anything else" and the n=0 verification requirements are unchanged. |
| 5 | **from slots 2 and 7** | `reactivation-runbook.md` §4 Step 6 · §2 step 3 · WHAT-"CLEAN"-MEANS item 3 | Step 6's first-position exception **now names its control** (test-fire first → `posLimitDay`=1, one bot at a time, reverted, revert hash-proven; accept-the-stored-limit declined; ⬜ NOT EVALUABLE + OFF as fallback). Both symbols echoes **branched** rather than deleted: Bot-Symbols-loop → must be non-empty; automation-resident-symbol → *"No symbols yet"* on both sides is correct, and ⛔ do not "restore" symbols into such a bot. |

**Convention on every one:** dated banner, **original struck but left standing**, evidence cited as
a dated first-hand observation or as the ruling that authorizes it — never another project document
vouching for one.

**Applied to:** `docs/reactivation-runbook.md` (4 amendments across §2 step 3, §2 step 7, §4 Step 1,
§4 Step 6, and the WHAT-"CLEAN"-MEANS block) · `docs/day0-session-pack-2026-08-07.md` (§S1 steps 0
and 7) · `docs/state.md` (PR04-R2 note) · `docs/oa-ops-runbook.md` (trap 1 row) · this card.
**Residuals, named:** `docs/session-log.md`'s 2026-08-07/08 entries also record *"`/automations`
404s"* — **left standing untouched**: the log is a record of what a session observed at the time,
not a live-facts surface. The `oa-driving` **skill** is a v1.2 candidate for the `/bots/automations`
path and the symbols branch; a skill is not a folder file and is **not** edited by this ruling.

## SLOT 9 — ops `trade_id` namespace — ✅ **RULED 2026-08-08**

**Andy:** covered by the blanket delegation recorded at slot 5.

**THE RULING — (c) DEFER, WITH (a) PRE-REGISTERED AS THE SCHEME.** `trade_id` **stays blank** in
`data/ops_rows.csv`. Nothing consumes the column, because **no Lab bot exists** — `pre-registration-
ledger.md` §6a records that no Lab bot is named or entered yet. ⛔ **No id is invented and no row is
backfilled** (Worker B was right to leave it blank).

**The scheme, on the record before any row exists:** when the first Lab bot is built, `ops_rows.csv`
rows carry **`OPS-<bot>-<date>-<n>`** — collision-proof against the working ledger's global pairing
counter **by prefix**, and structurally unable to reach the working ledger because the ops-class
partition runs **upstream of pairing**.

**REOPEN CONDITION:** the first Lab bot's build. Implement as written then, or amend by explicit
ruling before any row is emitted.

⚠️ **Carried, not fixed:** E-3 §3.3 **item 8** — pointing the frozen `execution_audit.py` at
`ops_rows.csv` as a fixture — stays **NOT USABLE** until ids exist. That is a carried state with a
named reopen condition, not a defect.
⛔ **The other two E-3 gated items are closed and were not re-opened:** the receipt clause ruled
**ADDITIVE**, and **O4 FIXED** (both 2026-08-08).

**Applied to:** `docs/exploratory-bots-design-2026-08-07.md` §3.3 (gated-item block) ·
`docs/state.md` (the three-gated-items paragraph, item 2) · this card.
**Residuals, named:** `data/ops_rows.csv` itself is **not touched** — its header already carries the
`trade_id` column and the column stays empty by ruling. No script change is authorized by this slot.

## SLOT 10 — DA-3 · the retired ≥15-condor go-live bar — ✅ **RULED 2026-08-08**

**Andy:** covered by the blanket delegation recorded at slot 5.

**THE RULING — YES, RETIRED IN PRINT.** `evidence-standards.md` §5 already retires the legacy
*"≥15 clean post-fix condors"* gate — *"G2's ≥20 supersedes it. Do not reinstate a 15-condor bar."*
That retirement **governs the reporting surfaces, not just the doctrine**. Verified first-hand
2026-08-08: `scripts/report.py:141` still emits `- Go-live gate (≥15 clean post-fix condor trades):
**{post_trades} / 15**`, and `STATUS.md` line 17 carries the rendered form — so a retired bar would
print on the dashboard **every trading day from 2026-08-10 on**. ⛔ **The line is DROPPED from both
surfaces. G2's ≥20 is the only go-live bar.**
⛔ **Rider: do NOT replace it with a "≥20" line.** G2 is not a single-count gate; rendering it as
one reproduces the exact defect §5 describes ("18/15" silently dropping 11 positions).

**Implementation — QUEUED, NOT DONE HERE.** The `report.py` edit is a **Claude Code task**
(`CLAUDE.md` §7); this session touches no file under `scripts/`. `STATUS.md` is **generated
output** and clears on the next `daily.sh` run once the emitter is fixed — it is not hand-edited.
**ACCEPTANCE CRITERIA:** `grep -c "Go-live gate" scripts/report.py` = **0**, and the next generated
`STATUS.md` contains no `Go-live gate` line.
⚠️ **Timing:** if the edit does not land before Monday's first `daily.sh`, the retired line prints
at least once. It is cosmetic, not a gate — nothing reads it — but it is named here rather than
discovered on the dashboard.

**Applied to:** `docs/evidence-standards.md` §5 (retired-in-print banner with the acceptance
criteria) · this card.
**Residuals, named:** `scripts/report.py` and `STATUS.md` are **unchanged this session** — both are
in the queued-implementation list. DA-1 … DA-10, the wider evidence-standards redesign proposal, is
**deliberately not on this sitting** and stays PREPARED, unruled.

<!-- RULINGS-END -->

---

## 1. A-02 — `LEDGER_START` semantics: the payment date, or the first `AUTOMATIONS`-ON day?

### The question

The post-cutover era's start date. `LEDGER_START` filters `open_date`; every reporting surface in
v2 reads post-cutover rows only. Andy sets it once, at S2 Step 1, and it is not revisited.

### Forcing facts, verbatim

`docs/day0-session-pack-2026-08-07.md` §0.0 **A-02** (grep `IS NOW A GATED QUESTION, NOT A COPY` = 1):

> ⛔ **AND `LEDGER_START` IS NOW A GATED QUESTION, NOT A COPY.** The runbook says *"This date is
> `LEDGER_START`"* on the assumption that payment and Day-0 are the same day. They are not: payment
> was 2026-08-07 and the roster does not exist until the restore lands. **A `LEDGER_START` of
> 2026-08-07 claims an era in which the account held zero bots.** S2 Step 1 must **ask Andy**
> whether the era starts at the payment timestamp or at the first day a bot is actually switched
> ON, record the answer verbatim, and only then set it. ⛔ Do not choose.

`docs/reactivation-runbook.md` §4 Step 1 (grep ``This date is `LEDGER_START`.`` = 1):

> Note the exact timestamp. **This date is `LEDGER_START`.** Set it in `build_ledger.py` before
> anything else, so no pre-cutover row can enter the working ledger.

`docs/build-plan.md` §3 (grep ``` `LEDGER_START` = the Day-0 reactivation date. ``` = 1) — 🔒 frozen:

> **`LEDGER_START` = the Day-0 reactivation date.** Everything downstream reads post-cutover only.

and, same section, the straddle rule: **`LEDGER_START` filters on `open_date`, never `close_date`.**

### The evidence, as it stands on device today

| Fact | Source, read this session |
|---|---|
| `ledger_start` currently `2099-01-01` — the refuse-everything sentinel | `data/ledger_meta.json` |
| `export_rows 1386 · post_cutover 0 · straddler 0 · pre_cutover 1386 · n_trades_condors 0` | `data/ledger_meta.json` |
| `LEDGER_START = "UNSET"` in the script; resolution order `--ledger-start` > `$LEDGER_START` > the constant; **refusal is the default** | `scripts/build_ledger.py` |
| **AUTOMATIONS ON: 0 of 41.** *"The fleet is entirely OFF. Nothing can open a position."* (grep `AUTOMATIONS ON : 0 of 41` = 1) | `data/captures/2026-08-07-s0b/toggle-state-all-41-2026-08-07.tsv` |
| Payment timestamp: ~12:06–12:10 ET 2026-08-07, *"plan purchased, login works"* | `docs/state.md` incident block |

⭐ **The choice is not currently observable in the data, and that is the point.** With 0 of 41 bots
switched on, no position can have opened on or after 2026-08-07, so the working ledger reads `n=0`
under *either* option today. What the ruling fixes is **which future dates are admissible**, not
which rows exist now. It is cheap to rule today and expensive to rule wrong.

### Options

**A — PAYMENT DATE, 2026-08-07.**
*Cost:* it is exactly the reading A-02 objects to — it claims an era in which the account held zero
bots, and it makes admissible any position opened by a bot switched on for a reason other than
Step 7 (a Lab/ops bot, a test, a hand-flip). `pre-registration-ledger.md` §2a guardrail **G2** notes
that the ledger exclusion for ops bots is *"implementation queued"* — so today there is no code
preventing exactly that class of row. *Benefit:* it is a first-hand recorded fact needing no later
amendment, and it is the literal text of runbook §4 Step 1.

**B — FIRST `AUTOMATIONS`-ON DATE (the day Step 7 first flips a bot).**
*Cost:* a real ordering conflict — Step 1 runs *before* Step 7 in dependency order and the runbook
says set it *"before anything else"*, so the step that sets the value runs before the fact it names
exists. *Mitigation, and it is cheap:* Step 1's binding requirement is the **n=0 verification**, and
that passes identically under any future-dated value — the current `2099-01-01` sentinel already
demonstrates it under real load (`1,386 → 0`). Set the expected Step-7 date at Step 1, re-run
`build_ledger.py` at close-out against the actual date, require `n=0` both times, record both runs.
*Benefit:* every row in the working ledger is then, by construction, from a bot that passed Step 6
and was authorized at Step 7.

**C — FIRST FULL TRADING DAY AFTER SWITCH-ON.**
*Cost:* adds a definition the folder does not currently carry, and if Step 7 completes intraday it
discards that day's positions from the working ledger — positions that *were* authorized. *Benefit:*
no partial trading day enters the record.

### RECOMMENDATION — **B**, with the ordering fix stated in the ruling *(RECOMMENDATION, NOT A RULING)*

The cutover exists so that no row can be read as evidence about a fleet state that did not exist.
Option A admits precisely that class of row; option C discards rows that are legitimately in-era.
B's only defect is an ordering awkwardness with a demonstrated, already-exercised workaround.

⚠️ **If B or C is ruled, CA-1 follows:** `build-plan.md` §3's *"the Day-0 reactivation date"* now
names a different day from the payment date, and `build_ledger.py`'s `LEDGER_START` constant
(currently `"UNSET"`) takes the ruled value. §3 is a frozen surface — this needs an explicit
"amend the plan", which is sub-choice **1a**.

⛔ **A-02 forbids a session choosing this.** The above is a recommendation to be accepted, rejected
or replaced by Andy, recorded verbatim, and only then set.

---

## 2. A-11 — the first-position control: what actually caps a bot at one position?

### The question

Step 6 needs a Trades list, a Trades list needs a position, and the only documented way to make a
position exist is `AUTOMATIONS` → ON — which Step 3 forbids and Step 7 gates. A-11 says the
exception names no control and forbids a session inventing one. What does Andy authorize?

### Forcing facts, verbatim

`day0-session-pack-2026-08-07.md` §0.0 **A-11** and its S2 Step 6 restatement
(grep `THE FIRST-POSITION EXCEPTION HAS NO MECHANISM` = 2, one per surface):

> *"The bot is allowed EXACTLY ONE position at 1 LOT"* names no control. The only way to make a
> position exist is `AUTOMATIONS` → ON, which Step 3 forbids and Step 7 gates — and nothing caps the
> bot at one (the greenfield arms carry `limits 2/2`, the PR-01 clone `10/10`). A session that
> improvises here reproduces the v1 failure the pack quotes at −$9,618, with Step 7 gating nothing.
>
> ⛔ **DO NOT IMPROVISE THE MECHANISM AND DO NOT BATCH IT.** Attempt the button test-fire first and
> record verbatim whether the control exists. If it does not: **STOP and put the mechanism to Andy
> as a gated question** … ⛔ **IF ANDY IS NOT AVAILABLE TO RULE IT → that bot's Step 6 is ⬜ NOT
> EVALUABLE and IT STAYS OFF.** … ⚠️ **AND "TEST-FIRE UNAVAILABLE" IS NOT DECIDABLE FROM ONE
> SCREEN.** … **a surface you did not open is not an absent control.**

`reactivation-runbook.md` §4 Step 6 carries the same hole — A-11 notes it is *"RUNBOOK-LEVEL in
origin … and is not this session's to edit."*

### The evidence

| Bot / group | `posLimit` / `posLimitDay` | Source |
|---|---|---|
| The 7 greenfield arms | **2 / 2** | pack §1.1 |
| PR-01 clone `IC-SPX-FastPT25-S2` | **10 / 10** | pack §1.1 |
| `IC-SPX-FastPT25-S2-130PM` | **10 / 10** | `data/captures/2026-08-08-clones/PR-02-step0-baseline-…txt` (read this session) |
| `QQQ-IC-0DTE-Fortress-NoPT50` | **2 / 2** | `2026-08-07-s0b/STEP-4b-capture-diff…txt` §5 |
| The nine leave-in-place | **UNVERIFIED** — no per-bot capture exists (slot 6) | — |

⛔ **The existence and location of a button test-fire is `UNVERIFIED`.** No document in this folder
names where it lives. Per A-11's own rule that is **⬜ NOT EVALUABLE, not "unavailable"** — so the
first act on Day-0 is still to look, and to record what is seen verbatim.

### Options

**A — TEST-FIRE FIRST, THEN RE-ASK.** Attempt it on one bot, record verbatim whether the control
exists, and only escalate the mechanism if it demonstrably does not. *Cost:* if it does not exist,
Day-0 stalls on a round trip to Andy — which is what ruling this slot in advance is meant to avoid.
*Benefit:* no config change at all on the branch where the test-fire exists. **This is not really an
alternative to B — it is the step that precedes it.** A-11 mandates the attempt regardless.

**B — AUTHORIZE A TEMPORARY `posLimitDay` = 1**, one bot at a time, screenshot before and after,
revert immediately after the Trades-list read, log the change and the revert in that bot's
pre-registration entry. *Cost:* it is a configuration change on an entry signed at Step 2b, and the
signature cites a config hash. Whether that forks the signature is itself a question — sub-choice
**2a**. It is the same class of objection A-12(a) raises against editing PR-20, though weaker: a
position limit is not a *mechanic*, and the A-series asserts that compare arms (A1/A2/A3) compare
mechanics and non-bundle fields. *Benefit:* it is the only mechanism on the table that actually caps
the bot at one, which is what the runbook's "exactly one position at 1 LOT" already promises.

**C — ACCEPT THE EXISTING LIMITS AS-IS.** Switch on at Step 7 with `2/2` or `10/10`, read the first
position's Trades list the moment it opens. *Cost:* the greenfield arms may open two; the PR-01
clone may open ten before anything is read. **This is the shape of the v1 −$9,618 failure A-11
names**, with Step 7's gate doing no work. *Benefit:* zero config change.

**D — DECLARE STEP 6 ⬜ NOT EVALUABLE** wherever the test-fire cannot be read; those bots stay OFF.
*Cost:* on the branch where no test-fire exists, this is the whole fleet staying OFF on Day-0.
*Benefit:* it is A-11's own default and it is unimpeachable. It is also what happens by default if
this slot is left unruled.

### RECOMMENDATION — **A, then B, with 2a answered NO** *(RECOMMENDATION, NOT A RULING)*

Attempt the test-fire and record it verbatim (A is mandatory anyway). If it is absent, B is the only
option that keeps the runbook's own promise. Rule 2a **NO** — a `posLimit` change made as a declared,
dated, reverted Day-0 verification step, logged in the entry, is a **verification action, not a spec
change**: it alters no mechanic, no exit bundle and no matched field, and it is reverted before the
sample starts. If Andy rules 2a **YES**, B collapses and D is the honest fallback — C should be
declined either way, because it converts a verification step into an uncapped live exposure.

⚠️ **Scope note.** A-11 governs the pack; `reactivation-runbook.md` §4 Step 6 carries the identical
hole and is a decision surface. If B is authorized, the runbook line should get the same treatment
Step 7 got on 2026-08-07 — an explicit, scoped "amend the plan" — so the mechanism survives a session
working from the runbook rather than the pack. **Not applied; flagged.**

---

## 3. A-12 — the C10 `dstop` read: which instrument, or none?

### The question

C10 (the unit of `dstop`, `Stop Loss $`) blocks **ARM-B1**. A-12 forbids closing it by editing
PR-20. Which instrument runs it — or does C10 stay open?

### Forcing facts, verbatim

`day0-session-pack-2026-08-07.md` §0.0 **A-12(a)** and its S2 Step 6b restatement
(grep `DO NOT EDIT A SIGNED ARM TO CLOSE AN OBSERVATION` = 2):

> **PR-20 is a SIGNED tournament arm.** Its whole mechanic is `profits 0.05` + `smprofits speedy`
> (§1.1). Adding `dstop` to it after Step 2b has signed its config: falsifies **A1** …, falsifies
> **A3** … and voids the config hash its signature cites. … And `profits 0.05` will usually close
> the position before any `dstop` can fire.
> ⛔ **DO NOT EDIT A SIGNED ARM TO CLOSE AN OBSERVATION, AND DAY-0 IS NOT A BUILD DAY. Put it to
> Andy: run C10 on an instrument OUTSIDE the tournament, or leave C10 OPEN.** … **Standing up a
> separate canary is a plan question.** *(last phrase, grep = 1)*

**A-12(b)** — the discrimination defect:

> **At 1 contract per leg, per-leg count = 1, so `−$100` and `−$100 × 1` are the same number** — the
> two primary branches become indistinguishable and `FIRED AT NEITHER FIGURE` is unreachable.

### Candidate A — `TESTOPS-LAB-DSTOP`, the Lab instrument

Fully specified already: `docs/exploratory-bots-design-2026-08-07.md` §2.2 — short put 1.50% below
underlying, long put $2.00 below, **3 contracts**, `posLimit`/`posLimitDay` 1/1, phase D1
`dstop = −60` + `smdstop speedy` with no PT, no time exit, no backstop.

⭐ **It is the only candidate that can actually discriminate.** §2.2's derivation (grep
`is the minimum count that separates all four candidate bases` = 1) enumerates four bases —
per position, per leg, per contract-per-leg, per total contract — and shows that at `n = 1` two of
the four collapse onto each of two values, at `n = 2` two collapse, and **`n = 3` is the minimum
count that separates all four on a 2-leg vertical.** Its reporting rule (grep
``C10-UNRESOLVED` unless the same basis is reproduced on`` = 1) requires **≥3 separate firings**,
which is A-12's own *"do not fit a basis to one data point"* made operational. It also answers **R3**
(`dprofit`) in phase D2.

**Costs, all four independent:**

1. ⛔ **Blocked by E-3's hard precondition.** `pre-registration-ledger.md` §2a (grep
   `E-3 hard precondition` = 1): *"no Lab bot's `AUTOMATIONS` may go ON until the `build_ledger.py`
   exclusion, the `a_series` scoping (`_a4b`/`_a6`), and the Lab group/tag fencing are **all
   implemented and verified**."* `docs/state.md` records E-3 as **RULED, NOT IMPLEMENTED** (grep
   `RULED, NOT IMPLEMENTED` = 1). None of the three can be built by a Day-0 session — they are
   Claude Code's lane.
2. **The bot does not exist.** Building it is a build; **Day-0 is not a build day** (A-12's words).
3. It consumes **1 of the ≤2 Lab ops slots** (E-1, ceiling 30).
4. It needs a signed `PHASE LOG` before its first phase (guardrail **G8**), and
   `pre-registration-ledger.md` §6a records that **no Lab bot is named or entered yet**.

⭐ One genuine argument in its favour beyond discrimination: §2.2 notes paper is the *better*
instrument here, not a compromise — Exit Options evaluate mid-price and paper fills near mid, so the
realised fill sits close to the band that fired it.

### Candidate B — the pilot, `QQQ-IC-0DTE-Fortress` (`BOTfw5TkkCRF2717857919585029021`)

**Costs, and two of them are independently fatal to a Day-0 read:**

1. ⛔ **It cannot open a position.** `data/captures/2026-08-07-s0b/STEP-4b-capture-diff…txt` §4
   (grep `NOT ESTABLISHED** — FINDING S0b-1 above` = 1): its config-capture hash is **NOT
   ESTABLISHED**, PR-03 **cannot be signed at Step 2b**, and the **bot stays OFF**. A bot that stays
   off produces no position and therefore no `dstop` firing. *Fatal on its own.*
2. ⛔ **At 1 lot it cannot discriminate** — §2.2's `n = 1` row: B1 = B3 and B2 = B4, four bases and
   two values. The best available outcome is `C10-UNRESOLVED`; the worst is a false CLOSED.
   *Fatal on its own.*
3. Its spec is frozen in `build-plan.md` §2B (grep `Restored exits: PT50 + 15:50 time exit + 15:52
   flat-close Scheduled Event backstop` = 1). Adding `dstop` is a spec change → an amend-the-plan.
4. **PT50 will usually close the position before `dstop` can fire** — the identical objection A-12
   raises against the Canary, and it applies here with the same force.
5. It is also the Template-V2 blocker bot (slot 4, item i).

*Benefits, stated fairly:* it exists, it is outside the tournament, and it is not a matched arm — so
editing it falsifies no A1/A3 assert.

### Candidate C — **LEAVE C10 OPEN**

A-12's own second branch, verbatim: *"If no such instrument exists on the day, **C10 STAYS OPEN** —
say so by name in `state.md` and at close-out; **ARM-B1 stays blocked, which is where it already
is.**"* *Cost:* PR-21 stays unstamped and ARM-B1 stays blocked — a cost already being paid.
*Benefit:* nothing is edited, nothing is built, no false close enters the record.

### RECOMMENDATION — **C for Day-0; A as the queued path** *(RECOMMENDATION, NOT A RULING)*

C10 stays OPEN by name in `state.md` and at close-out. `TESTOPS-LAB-DSTOP` is the instrument that
closes it, once E-3's three implementations land and Andy signs its `PHASE LOG` — which is a
build-window decision, not a Day-0 one. **Candidate B should be declined on cost 2 alone:** even if
the pilot's hash were ESTABLISHED and its spec amended, a 1-lot read cannot distinguish per-position
from per-contract-per-leg, so it spends a live position and an amendment to buy an unresolvable
reading. That is the shape of decision A-12 was written to prevent.

---

## 4. A-24 — S2 Step 0's residue: three known-unticked ⛔ boxes, plus one A-24 did not know about

### Forcing facts, verbatim

`day0-session-pack-2026-08-07.md` §0.0 **A-24** and its S2 Step 0 restatement (grep
`THE THREE KNOWN-UNTICKED BOXES ARE ANDY'S RULING` = 2):

> ⚠️ **THE "DO NOT PAY" HALF IS SPENT — payment already happened. It is not an instruction.**
> ⛔ **THE THREE KNOWN-UNTICKED BOXES ARE ANDY'S RULING AT STEP 0, ONE AT A TIME, ASKED EXPLICITLY —
> not a silent proceed and not an automatic halt:** Template V2 is finished here **or the pilot
> stays OFF**; C9 is run **as a read** before switch-on **or the family stays OFF**; A7-unwired is
> reported and **Andy rules whether the family trades today with no nightly detector** (wiring it is
> Claude Code's lane). ⛔ **ANY OTHER unticked ⛔ box is an unqualified STOP.** ⛔ **Do not resolve
> any of them yourself.**

### (i) Template V2 on the pilot, with its amended PR-03 signed

*State:* not done. Re-price the 15:50 Expiration exit off Market → SmartPricing internal value
`speedy` (⛔ **not** `fast`); the 15:52 backstop keeps Market. Without V2 the three 15:50–15:52
mechanics are three Market orders in two minutes with only memo strings between them.

⚠️ **Interaction that changes this item's weight.** The pilot **already stays OFF** on an
independent ground — S0b-1's NOT ESTABLISHED finding (slot 3, candidate B, cost 1). So ruling
"finish V2 at Step 0" buys nothing for Day-0 unless S0b-1 is *also* released, and finishing V2 is a
spec change plus a signature — which A-24 itself calls out as *"a SPEC CHANGE, not a config tweak."*

**RECOMMENDATION — PILOT STAYS OFF.** *(RECOMMENDATION, NOT A RULING.)* V2 lands in a build window
with its amended PR-03, not inside Step 0 of a Day-0 sequence.

### (ii) C9 — firing semantics, re-scoped to a Day-0 pre-switch-on read

*State:* `C0c · C2 · C7 · C8` are **CLOSED** (decision card 2026-08-06). **C9 is re-scoped to a
Day-0 pre-switch-on read and still open.** A-24's branch: run it as a read, or the family stays OFF.

**RECOMMENDATION — RUN AS A READ AT STEP 0.** *(RECOMMENDATION, NOT A RULING.)* It is a read, it is
cheap, and the alternative forfeits the family's Day-0 for an observation that takes minutes. ⛔ Read
only — never a write, never an improvised spec.

### (iii) A7 not wired into `daily.sh`

*State, precisely:* the A7 **baselines are recorded** in `data/bots_config_v2.csv` (3 of 3 shared
objects, ScannerA at v9 / `3308ce8b…` after the A7-DRIFT-1 ADOPT ruling). **A7 is not wired into
`daily.sh`** — its eight stages carry `execution_audit.py` and no A-series runner. **A-26** adds
`scripts/a_series.py`, which runs **standalone and does not wire itself in**. ⚠️ **A-13** separately
records that A7 covers **3** shared automations where the runbook requires **4** — the fourth being
`Defang-Mon-S2-StrikeTouch`.

So the honest state is: *the detector exists as a hand-run tool at 3 of 4 objects, not as a nightly.*

**RECOMMENDATION — TRADE, WITH A HAND-RUN `a_series.py --validate` + `--json` AT EVERY CLOSE-OUT,
AND THE 4th OBJECT NAMED AS AN OPEN GAP.** *(RECOMMENDATION, NOT A RULING.)* Under Architecture E one
edit changes all seven arms at once with no template version bump, so A7 is the only detector — but
a detector run by hand every day is a detector, and the pack's own standard is that a gap is
reported on the page rather than papered over. If Andy prefers the stricter reading, the family
stays OFF until wiring lands, which is Claude Code's lane and not a Day-0 action either way.

### (iv) ⛔ NOT IN A-24 — gate A9 is an unticked ⛔ HARD box, and it is currently the binding one

`docs/state.md`, gate-A9 block, verbatim (grep `run is on file` = 1):

> ⛔ **Day-0's §4 does not start until a clean end-to-end n=0 run is on file. THIS BLOCKER IS
> OPEN.** … **❌ STAGE 3 `execution_audit.py` — RAISES `KeyError: 'bot'`.**

A-24 was written before this failure and does not enumerate it, so A-24's own catch-all applies:
*"⛔ ANY OTHER unticked ⛔ box is an unqualified STOP."*

⚠️ **A fix has been written but the box is not closed.** `CLAUDE.md` §9.1a: a tool-success message
is not verification, and neither is a session's report of its own run. **The box closes on Andy's
own clean end-to-end `daily.sh` n=0 run, on file, and on nothing else.** The queued task is split —
**(i)** the minimum loader fix clears gate A9 on its own; **(ii)** the Tier-C contract
reconciliation is separate and does **not** gate Day-0. ⛔ Do not reshape `data/bots_config_v2.csv`.

**RECOMMENDATION — CONFIRM (iv) as stated, and rule (i)–(iii) now anyway.** *(RECOMMENDATION, NOT A
RULING.)* (iv) is a calendar gate: §4 does not start until it clears, regardless of how (i)–(iii)
go. Ruling (i)–(iii) today costs nothing and removes three stalls from inside Step 0.

---

## 5. Gate A8 — PR-18's name. This is the whole of gate A8.

### Forcing facts, verbatim

`day0-session-pack-2026-08-07.md` §0.0 **A-04** and S2 Step 2b (grep
`IS STILL OPEN AND STILL ANDY'S — it is the WHOLE of gate` = 1):

> ✅ **ITEM (ii), PR-18's "Breakeven" naming, IS STILL OPEN AND STILL ANDY'S — it is the WHOLE of
> gate A8. Ask; do not choose.**

⛔ **The other two A8 items are closed and must not be re-presented.** **G-12b — SIGNED**
(δ=0.10R, p=0.20, floor n_matched_days ≥ 100 + one re-arm at Day-0+9mo, inside the family
correction): *"⛔ DO NOT RE-PRESENT `[ 0.10 | other ]` TO ANDY. Any answer that is not a verbatim
repeat silently forks a signed pre-registration."* **G-1′ — DECLINED**; do not re-open.

The substance, from S2 Step 2b:

> Sandvand's rung is called Breakeven because stopping the tested spread at 100% of credit leaves
> the UNTESTED side to decay to zero, netting ≈$0 on the condor. The C8 ruling removed
> sibling-close, so the untested side IS left to decay and the construction objection is GONE —
> CF-4 is discharged and the arm CAN now reach Breakeven. **The name is withheld PENDING ANDY'S
> READ OF HOW IT SHOULD BE PUBLISHED.**

`docs/greenfield-family-spec.md` (grep `NOW REACH BREAKEVEN` = 1; `CF-4 is DISCHARGED` = 2):

> ⭐ **RESOLVED 2026-08-06 BY THE C8 RULING:** sibling-close is NOT BUILT, so the untested side IS
> left to decay exactly as the anchor assumes. **THIS ARM CAN NOW REACH BREAKEVEN**, the downward
> bias is removed, and **CF-4 is DISCHARGED**. The arm may be read against Sandvand's rung on its
> own terms.

### ⚠️ A propagation gap this card found, and did NOT fix

`docs/state.md` still carries the **pre-discharge** CF-4 text (grep
`CF-4 — sibling-close destroys the anchor PR-18 imports` = 1; `publish it under the anchor's name` = 1):

> **CF-4 — sibling-close destroys the anchor PR-18 imports.** … Renamed in substance to
> "SL100-close-both"; **do not publish it under the anchor's name.**

The spec discharged CF-4 on 2026-08-06; `state.md` — the live-facts page — still says the opposite.
⛔ **Not corrected here.** The falsified sentence *is* the decision in front of Andy in this slot, so
under `CLAUDE.md` §5 it is ambiguous and therefore **gated**, not an evidence-backed correction.
It is sub-choice **5a** / consequential amendment **CA-2**.

⚠️ **What is NOT discharged: CF-1.** The exit-pricing / ITM-exposure confound stands, is unrelated to
sibling-close, and *"bounds what the family can conclude."* Any publication under a public anchor's
name inherits that bound.

### Options

**A — "Breakeven" everywhere.** *Cost:* imports a public anchor's name onto an arm whose comparison
to that anchor is bounded by CF-1. *Benefit:* the name *is* the mechanic (`stoploss = 1` =
−100% of credit, unit confirmed % of credit by C1), and CF-4 is discharged, so the arm is entitled
to it on the merits.

**B — MECHANICAL NAME ONLY** (`SL100`, "stop at 100% of credit"). *Cost:* forfeits the anchor's
interpretive value in briefs and reviews. *Benefit:* no publication claim CF-1 could undercut; the
OA bot name is already `GF-QQQ-IC-SL100`, so nothing renames anywhere.

**C — SPLIT.** "Breakeven" as the ledger/internal label; the mechanical name in anything published
or compared externally, with the CF-1 caveat attached at that surface. *Cost:* two labels for one
arm — a small standing risk of the wrong one leaking into a brief. *Benefit:* takes CF-4's discharge
at face value where it is true, and keeps CF-1's constraint attached where it actually bites.

### RECOMMENDATION — **C** *(RECOMMENDATION, NOT A RULING)*

C is the only option that honours both findings rather than one. Whichever is ruled, the field must
be **filled** — `pre-registration-ledger.md` §7 item 2: an entry with an unresolved field is
**UNSIGNED**, and that is the whole of gate A8.

---

## 6. A-27(c) — Step-4b: the A-07 precondition on S2's opening, and the capture worklist

### The gate, verbatim

`day0-session-pack-2026-08-07.md` §0.0 **A-27(c)** (grep `S2 DOES NOT START UNTIL ANDY HAS RULED
THIS` = 1):

> **RULING: this is a NAMED PRECONDITION ON S2 OPENING, and NO OPTION IS CHOSEN.**
> ⛔ **S2 DOES NOT START UNTIL ANDY HAS RULED THIS.**

The three options, verbatim from A-27(c): **1. CAPTURE-NOW-AS-BASELINE** (*"Honest cost: this
establishes nothing about the past… It buys forward coverage, not retrospective assurance."*
⛔ *"It also requires opening the nine, which spends Step 2c unless taken as a pure read."*) ·
**2. AMEND A-07's SCOPE** so an ESTABLISHED hash is required only where a pre-restore baseline
exists, the rest carried explicitly ⬜ NOT EVALUABLE rather than blocking · **3. LEAVE THEM OFF
PERMANENTLY.**

### §A — ⛔ A count correction, found by re-running the inventory this session

A-27(c) says *"for **12** of the 14 bots in A-07's scope there is NO per-bot capture file on disk at
all"* and then names its list: *"`IC-SPX-FastPT25-S2-130PM`, `QQQ-IC-0DTE-Fortress-NoPT50` and all
nine leave-in-place bots"* — **which is eleven, not twelve.**

Re-inventoried `data/captures/` directly this session. Both numbers are defensible; they count
different things, and the pack conflates them:

- **11** bots had **no per-bot capture file on disk** as of 2026-08-07.
- **12** bots **cannot have their config-capture hash ESTABLISHED** — those 11, **plus the pilot**,
  which *has* a baseline and **diverges from it** (S0b-1).

The step4b file's own §4 disposition table is internally correct (2 ESTABLISHED + 1 NOT ESTABLISHED
+ 11 ⬜ NOT EVALUABLE = 14) and its §0 headline is the loose one; A-27(c) inherited §0's wording.
⛔ **Not corrected in the pack** — it is one number inside an amendment whose ruling is live in front
of Andy, so it is gated (**CA-3**), not applied.

### §B — the worklist, as of a device read on 2026-08-08

⚠️ **Everything in the "on disk" column is POST-restore.** Under A-27(c)'s own honest cost, none of
it establishes anything about the pre-restore past; it buys forward drift detection only.

**Group 1 — the nine leave-in-place bots. Nothing on disk at bot or automation level.**
List-view 18 fields + toggle state (AUTOS OFF / EXITS OFF) only, and A-27(c) records that no bot
page was opened for any of them.

| # | Bot | Bot ID | Note |
|---|---|---|---|
| 1 | `DIR-SPX-PutVIX22-SL75` | `BOTfw5TkkCRF217824306963282811` | |
| 2 | `DIR-SPX-CallVIXdrop` | `BOTfw5TkkCRF217824370390678863` | |
| 3 | `3DTE $140-$350` | `BOTfw5TkkCRF2217765235512870291` | mirror |
| 4 | `Nigiri-Paper-v1` | `BOTfw5TkkCRF1017766118057607741` | mirror |
| 5 | `QQQ long call` | `BOTfw5TkkCRF1017766424258604555` | mirror · **POS 4, RISK $13K** — 4 of the 5 open positions; A-10 requires a first-hand re-read at Step 2 |
| 6 | `Friday 14 DTE Broken Wing IB (B-70)` | `BOTfw5TkkCRF1017766446781407596` | mirror |
| 7 | `Trendy-Paper-v1` | `BOTfw5TkkCRF1017766118431160782` | mirror |
| 8 | `60min-ORB-10W-Paper-v1` | `BOTfw5TkkCRF3317782759988647731` | mirror |
| 9 | `Tasty Condor` | `BOTfw5TkkCRF1017766126336204213` | mirror · **POS 1, RISK $1,082** — the 5th open position |

**Group 2 — the two un-started clone originals. Partial records exist; both post-restore.**

| # | Bot | Bot ID | What is on disk today | Still missing |
|---|---|---|---|---|
| 10 | `IC-SPX-FastPT25-S2-130PM` | `BOTfw5TkkCRF3717814485128334371` | bot-level fields (step4b §5, 08-07) **+ automation-level `a7_hash` for all 4 automations** (`data/captures/2026-08-08-clones/PR-02-step0-baseline-…txt`, 08-08) | Exit-Options PDF · both toggle screenshots · input-chain resolution |
| 11 | `QQQ-IC-0DTE-Fortress-NoPT50` | `BOTfw5TkkCRF2617743681996538301` | bot-level fields only (step4b §5, 08-07) | **automation hashes** (2 automations: `FortNoPT-Scan-Put`, `FortNoPT-Scan-Call`) · Exit-Options PDF · toggle screenshots |

⚠️ **Check S1's close-out before capturing 10 and 11.** S1 (the PR-02/PR-04 clone build) was running
today; as of this card's device read it has written one step-0 baseline
(`PR-02-step0-baseline-IC-SPX-FastPT25-S2-130PM.txt`, 2026-08-08) and **no close-out entry exists in
`docs/session-log.md`**. If S1 completes, both bots acquire full clone capture sets and their rows
here are discharged.

**Out of scope but on the record — A-27(c)'s second correction:** *"⛔ **THE 20 GROUP-A BOTS ARE IN
NO POST-RESTORE CONFIG CHECK ANYWHERE IN THIS PACK.**"* They are still active only because the ~23
archives remain queued for Andy's hand. Sub-choice **6b**.

### §C — the exact pages, per bot, for option 1

Per `oa-ops-runbook.md` §1.8 (the sweep, end to end) plus A-07's two additional requirements:

**Once, for the whole pass:**

1. **`/bots` bookmarklet capture first** — roster authority, 18 fields × 41 bots, one page.
   ⚠️ It **misses `AUTOS`/`EXITS`** (§1.5, *"the highest-value miss"*): the rows emit 18 values, not
   20, because the toggle cells are icons with no text node. Toggle state comes from the separate
   `i.sticon[title]` DOM read (**A-27d**) or from per-bot screenshots — never from the bookmarklet.
2. **`Export Data`, ALL bot groups selected → `data/raw/YYYY-MM-DD.csv`.**
   ⛔ §1.7, grep `THE EXPORT RESPECTS THE BOT-GROUP FILTER` = 1: an export taken with any group
   deselected is a **subset**.

**Per bot, for each of the 11:**

3. Open **each automation**, **expand every node**, click **OA Grab**. ⛔ After a **hard reload**
   (A-07), and **resolve the input chain two hops** where one exists.
4. **Open Position action → Exit Options → `⌘P` → Save as PDF.**
5. **Both toggle screenshots** (grep `**Both toggle screenshots per bot.**` = 1) → filed as
   `data/captures/toggles/<date>/<bot>.png`. §1.6: toggle state *"does not survive text capture"*.
6. Drop everything into `data/captures/<date>/`.
7. **Hand off for commit.** ⛔ Claude does not commit (`CLAUDE.md` §9.1).

Rough shape of the ask: **11 bots × (automations + 1 Exit-Options PDF + 2 screenshots)**, plus 2
account-level pulls. Automation counts are known for 2 of the 11 — `-130PM` has 4, `-NoPT50` has 2 —
and are **UNVERIFIED for the nine**, because no bot page has ever been opened on them.

### §D — the Step-2c collision, and why it is cheaper than it looks

A-27(c) warns option 1 *"requires opening the nine, which **spends Step 2c** unless taken as a pure
read"* (grep `requires opening the nine, which` = 1). ⚠️ **But Step 2c is already forfeit.**
Amendment **A-09b** (grep `NO-TOUCH OBSERVATION CONFOUNDED` = 2):

> IF THE ROSTER WAS RESTORED BY OA RATHER THAN SURVIVING INTACT, THIS OBSERVATION IS CONFOUNDED BY
> THE RESTORE. … Record `NO-TOUCH OBSERVATION CONFOUNDED — RESTORE`, treat it as ⬜ NOT EVALUABLE.

Gate A0 landed on **Branch 1** (restore, 41·9 verified), so A-09b fires. **The observation option 1
would spend is one A-09b has already ruled NOT EVALUABLE.** That materially lowers option 1's cost —
but it does **not** make the capture pass automatically permissible, because the S0b session was
told *"DO NOT touch any of the nine leave-in-place bots, in any way"*, which is narrower than A-07's
pure-read allowance. Sub-choice **6a** settles it explicitly.

### Options and costs

**1 — CAPTURE-NOW-AS-BASELINE.** *Cost:* the whole §C worklist, by hand, before S2 opens; and it
**establishes nothing about the past** — a first capture taken after the restore cannot distinguish a
faithfully restored bot from a rolled-back one. Needs 6a answered. *Benefit:* every one of the 11
becomes drift-detectable from that day forward, and the repository stops carrying a structural hole.

**2 — AMEND A-07's SCOPE.** Require an ESTABLISHED hash only where a pre-restore baseline exists;
carry the rest explicitly as ⬜ NOT EVALUABLE rather than as blockers, so Day-0 proceeds with the
blind spot **named on the page**. *Cost:* eleven bots trade with no config baseline of any kind, and
"⬜ carried" is one step from "⬜ forgotten" unless the carry is written into the entries themselves.
*Benefit:* it is the reading consistent with how this folder already handles unrunnable checks
(`reactivation-runbook.md` §4: *"Day-0 proceeds with the blind spot on the page"*), it costs no
Day-0 time, and it does not manufacture false assurance.

**3 — LEAVE THEM OFF PERMANENTLY.** The literal reading of A-07: no ESTABLISHED hash, no signature,
bot stays OFF. *Cost:* all nine leave-in-place bots stay off — including the two holding the five
open mirror positions, and both directional bots. It also makes **Step 6a undecidable forever**: the
mechanism verdict runs *"on the nine leave-in-place bots ONLY — the clones and fresh builds were
never lapsed and cannot test it."* Nine bots off = §1's lapse mechanism can never be settled.
*Benefit:* maximal evidential conservatism.

### RECOMMENDATION — **2, with the carry written into the entries; 6a = PURE READ** *(RECOMMENDATION, NOT A RULING)*

Option 3 has a consequence A-27(c) does not state and that is worth surfacing: it permanently
forecloses **Step 6a**, the step the runbook calls *"the step that settles §1."* Option 1 buys real
forward coverage but spends Day-0 hours on eleven hand captures for zero retrospective assurance, by
its own admission. Option 2 is the honest description of where the repository actually is.

**If 2 is ruled, three riders make it safe:** (a) each of the 11 pre-registration entries carries
`CONFIG HASH: ⬜ NOT EVALUABLE — no pre-restore baseline (A-27c ruling <date>)` in the field itself,
never as a footnote; (b) a capture is taken **on the first day each bot trades**, so forward drift
detection starts one day late instead of never; (c) 6b is answered so the 20 Group-A bots are not
silently in the same position with nobody having said so.

⛔ **A-27(c) chose no option and neither does this card.**

---

## Verification appendix

**Method.** Every quote above was asserted against the **device file** via `device_bash`
`grep -cF`, with the match count stated inline. No quote was taken from a staged copy
(`CLAUDE.md` §9.1a; the device-bridge caching defect reproduced 2026-07-31). No git command was run,
including `status`. No OA surface was touched and no browser tool was loaded. Where a fact could not
be read from the folder it is written **UNVERIFIED** in place.

**Files read in full or in cited sections, sha256 at read time (2026-08-08):**

```
cf041a456c13776f…  CLAUDE.md
8caecfd4cc6e3df6…  docs/day0-session-pack-2026-08-07.md
ba03487967efb450…  docs/state.md
12123d0c7744956d…  docs/reactivation-runbook.md
5f21c134dbc1ed63…  docs/evidence-standards.md
78bdf5e3d26f7097…  docs/build-plan.md
3b37fa3cb91767fc…  docs/pre-registration-ledger.md
0e84e86278d74169…  docs/greenfield-family-spec.md
386ec1dbe9b63aab…  docs/oa-ops-runbook.md
9ec56ba972cd03ab…  docs/exploratory-bots-design-2026-08-07.md
5c6e8d8cb6ebe3e8…  docs/decision-card-2026-08-06.md
676b295fa1894d2f…  data/captures/2026-08-07-s0b/STEP-4b-capture-diff-2026-08-06-vs-2026-08-07.txt
f45817aed7cd03ea…  data/captures/2026-08-07-s0b/toggle-state-all-41-2026-08-07.tsv
cf3866027b89895a…  data/bots_config_v2.csv
83761b3b3f8016b5…  data/ledger_meta.json
```

Also read: `scripts/build_ledger.py` (header + `LEDGER_START` resolution block),
`data/captures/2026-08-08-clones/PR-02-step0-baseline-IC-SPX-FastPT25-S2-130PM.txt`,
`docs/session-log.md` (tail), and a full recursive listing of `data/captures/`.

**Assert table (file | pattern | count).** Counts are `grep -cF` on the device file. A count of 2
means the phrase appears on two surfaces (§0.0 amendment + its S2 prompt restatement) and both were
read.

| Pattern | n | File |
|---|---|---|
| `IS NOW A GATED QUESTION, NOT A COPY` | 1 | day0-session-pack |
| ``This date is `LEDGER_START`.`` | 1 | reactivation-runbook |
| ``` `LEDGER_START` = the Day-0 reactivation date. ``` | 1 | build-plan |
| `THE FIRST-POSITION EXCEPTION HAS NO MECHANISM` | 2 | day0-session-pack |
| `DO NOT EDIT A SIGNED ARM TO CLOSE AN OBSERVATION` | 2 | day0-session-pack |
| `Standing up a separate canary is a plan question` | 1 | day0-session-pack |
| `is the minimum count that separates all four candidate bases` | 1 | exploratory-bots-design |
| ``C10-UNRESOLVED` unless the same basis is reproduced on`` | 1 | exploratory-bots-design |
| `E-3 hard precondition` | 1 | pre-registration-ledger |
| `RULED, NOT IMPLEMENTED` | 1 | state.md |
| `THE THREE KNOWN-UNTICKED BOXES ARE ANDY'S RULING` | 2 | day0-session-pack |
| `run is on file` | 1 | state.md |
| `IS STILL OPEN AND STILL ANDY'S — it is the WHOLE of gate` | 1 | day0-session-pack |
| `NOW REACH BREAKEVEN` | 1 | greenfield-family-spec |
| `CF-4 is DISCHARGED` | 2 | greenfield-family-spec |
| `CF-4 — sibling-close destroys the anchor PR-18 imports` | 1 | state.md |
| `publish it under the anchor's name` | 1 | state.md |
| `S2 DOES NOT START UNTIL ANDY HAS RULED THIS` | 1 | day0-session-pack |
| `A-07's scope is FOURTEEN bots, not thirteen` | 1 | day0-session-pack |
| `capture file on disk to diff against` | 1 | STEP-4b-capture-diff |
| `NOT ESTABLISHED** — FINDING S0b-1 above` | 1 | STEP-4b-capture-diff |
| `AUTOMATIONS ON : 0 of 41` | 1 | toggle-state-all-41 |
| `NO-TOUCH OBSERVATION CONFOUNDED` | 2 | day0-session-pack |
| `requires opening the nine, which` | 1 | day0-session-pack |
| `**Both toggle screenshots per bot.**` | 1 | oa-ops-runbook |
| `THE EXPORT RESPECTS THE BOT-GROUP FILTER` | 1 | oa-ops-runbook |
| `Restored exits: PT50 + 15:50 time exit + 15:52 flat-close Scheduled Event backstop` | 1 | build-plan |
| `Nothing is re-stamped on Day-0 either way` | 1 | reactivation-runbook |
| `Optional 1-lot canary` | 1 | pre-registration-ledger |

**Open evidence gaps carried by this card, stated rather than papered over:**

1. **The button test-fire** — its existence and location are **UNVERIFIED**. No document in this
   folder names it. Per A-11 that is ⬜ NOT EVALUABLE, never "unavailable". Slot 2 depends on it.
2. **The nine leave-in-place bots' automation trees, `posLimit`s, tags and groups** — **UNVERIFIED**.
   No bot page has ever been opened on any of them. Slot 6 is the whole of this gap.
3. **The 20 Group-A bots** — in no post-restore config check anywhere. Sub-choice 6b.
4. **A7's 4th shared object** (`Defang-Mon-S2-StrikeTouch`) — A-13's 3-of-4 gap. Slot 4(iii).
5. **Gate A9** — closes only on Andy's own clean end-to-end n=0 run. A session's report of a fix is
   not the check (`CLAUDE.md` §9.1a). Slot 4(iv).
6. **S1's outcome** — running at the time of this read; one step-0 baseline on disk, no close-out in
   `session-log.md`. Slots 2 and 6 both reference bots S1 may have changed.

*Card written 2026-08-08. Nothing was edited beyond this file, `docs/session-log.md` and
`docs/state.md`; no OA surface touched; no browser tool loaded; no git run. Post-ruling work applies
exactly what each ruling authorizes, with per-file dated amendment conventions, originals left
standing where required, and every edited file verified by direct `device_bash` sha256 +
single-match grep of the inserted text.*

---

# ADDENDUM — 2026-08-08 evening. Three slots added by the day's work; S2-precondition status. PREPARED, NOTHING RULED.

*Appended by the orchestrator session so tonight's sitting is ONE document. Same rules as the
card: every recommendation is a RECOMMENDATION, not a ruling.*

## SLOT 7 — ✅ RULED 2026-08-08 (a): PR02-R2, the §S1 "Symbols panel is NOT empty" line is FALSE for this family
**Question:** amend the pack's §S1 step-4 symbols text (and the runbook §2 echo if present)?
**Evidence:** first-hand on BOTH PR-02 sides 2026-08-08 — clone AND original read "No symbols
yet"; the symbol is automation-resident (`Loop SPX` / action `symbol: SPX`). Same finding
recorded for PR-01. **Options:** (a) apply as evidence-backed correction (CA-3 class, dated
banner, original standing) — the sentence is guidance falsified twice first-hand; (b) leave for
a pack rewrite. **RECOMMENDATION: (a)** — a checklist line that cries wolf on every
automation-resident-symbol bot trains sessions to skip the one check that catches the REAL
symbols trap on Bot-Symbols-loop bots.

## SLOT 8 — ✅ RULED 2026-08-08: AMEND ALL FIVE. PR02-R3: runbook §2 step 7 still carries the pre-F-C1 "do not remove PT25" branch
**Question:** amend `reactivation-runbook.md` §2 step 7 to the F-C1 RULED: REMOVE state?
**Status:** flagged at S0b close-out AND by A-16b (pack already supersedes it; sessions are
instructed not to stop on the conflict). Runbook is a decision surface — **amend-the-plan, yours
only.** **RECOMMENDATION: amend at the sitting** — the pack-vs-runbook contradiction is exactly
the A-16 class that cost an adversarial-review pass to find.

## SLOT 9 — ✅ RULED 2026-08-08 (c)+(a): ops `trade_id` namespace (E-3 gated item (2))
**Question:** what `trade_id` scheme do `data/ops_rows.csv` rows carry?
**Status:** blank today — Worker B correctly invented nothing; blank blocks E-3 item 8's fixture
use. **Options:** (a) `OPS-<bot>-<date>-<n>` synthetic namespace, collision-proof by prefix,
never enters the working ledger (partition is upstream); (b) carry OA's native ids when the Lab
bots exist and backfill nothing; (c) defer until the first Lab bot is built (nothing consumes
the column today). **RECOMMENDATION: (c) defer with (a) pre-registered as the scheme** — zero
cost now, no invented ids, and the namespace is on record before any row exists.

## S2-PRECONDITION STATUS — as of this addendum, from the folder
| Precondition | Status |
|---|---|
| Gate A9 clean end-to-end n=0 run on Andy's machine, on file | ✅ CLOSED 2026-08-08 |
| A-27c / Step-4b capture disposition | ⛔ UNRULED — slot 6 (worklist = 11, per CA-3) |
| Slots 1–5 (A-02 · A-11 · A-12 · A-24 · gate A8/PR-18) | ⛔ UNRULED |
| PR-02 clone | ✅ built + verified; R1 RULED $50k; Template V1 = Andy's hand at Day-0 |
| PR-04 clone | 🔄 in progress (S1 continuation session) |
| Fleet sweep (read-only audit) + master audit report | queued behind PR-04 |
| FLEET-STAYS-OFF / A-06 | no such verdict fired today; nothing switched ON |

## SLOT 10 — ✅ RULED 2026-08-08 YES (retired-in-print): DA-3, the retired ≥15-condor go-live bar still prints (added post-sweep)
**Question:** does evidence-standards §5's retirement of the ≥15-condor bar govern, so
`report.py:141` / STATUS.md line 17 drop that line? **Evidence:** both verified first-hand
2026-08-08; the line will print on the dashboard every trading day from Monday.
**RECOMMENDATION: yes — rule it retired-in-print; the one-line report.py edit is Claude Code's
lane after the ruling.**

## SLOT 8 SCOPE NOTE (added post-sweep): the doc-correction batch now carries THREE items —
runbook §2 step 7 pre-F-C1 line (PR02-R3) · pack §S1 clone-2 "four automations/traps" is two
for the Fortress family (PR04-R1) · Library path is /bots/automations, not unreachable (FS-3,
proven from the /bots Library button's own menu JSON).
