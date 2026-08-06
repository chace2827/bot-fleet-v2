# Decision card — 2026-08-06

*One card, seven ruling slots, ruled once tonight so the remaining Max-capacity window
(downgrade **2026-08-07 14:52 ET**) runs unblocked. Written against fresh device reads of every
cited file — no memory, no staged-copy quotes. Every quoted phrase below was asserted byte-exact
against the device file by a `device_bash` grep with a match count of exactly **1** unless a
different count is stated; the assert table and per-file sha256 set are in the Verification
appendix. Two slots (4 and 5) were attacked by adversarial subagents before this card was
finalized; both original recommendations were **refuted as drafted** and appear here in their
post-review form, with the surviving objections recorded in-slot.*

**How to rule:** one line per slot. The Ruling Sheet below is copy-paste ready. Nothing in this
card edits anything; every edit happens only after — and exactly as far as — the corresponding
ruling authorizes. Gated surfaces move only under an explicit **"amend the plan"** (`CLAUDE.md`
§5).

---

## RULING SHEET — copy, fill, send

```
1. Propagation grant (memo → 6 docs, list §1):        AMEND THE PLAN: YES / NO / strike items: ___
   → RULED 2026-08-06: YES, in full (no items struck).
   1a. build-plan §2D Range075 wording now vs hold:    APPLY NOW / HOLD for the UI check
   → RULED 2026-08-06: APPLY NOW.
2. Ledger §1/§3/§7 count scoping:                      NO ACTION NEEDED — CONFIRM / reopen: ___
   → RULED 2026-08-06: CONFIRM.
3. PR-14…17 family kill criterion:                     NO ACTION NEEDED — CONFIRM / reopen: ___
   → RULED 2026-08-06: CONFIRM.
4. Greenfield build session (package §4):              AUTHORIZE / PROBE-ONLY / DEFER
   → RULED 2026-08-06: AUTHORIZE, package items 1–8. Amended, two parts from Andy: (i) the OA
     build itself (Phase 0 probes onward) runs in a SEPARATE session — this session applied doc
     edits only, touched no OA surface, ran no browser tool; (ii) sequencing per slot 7 —
     C0b look, 2 deletions, and the C5 Library delete + exactly-one verify-back run tonight,
     before Phase A, in that separate session.
   4a. Pilot declared clean (runbook §3 Step A):       YES, CLEAN / NOT YET
   → RULED 2026-08-06: YES, CLEAN — on the ritual-complete record and the FINISH capture-diff
     no-unintended-edits verdict (reactivation-runbook.md §3 Step A gate).
5. Double-testing:                                     RETIRE FROM TRACK A (rec) / PRECEDENCE ONLY /
                                                       DROP AN ARM / ACCEPT+DOCUMENT
   → RULED 2026-08-06: RETIRE-SCOPED, package parts 1–4 (research-loop-spec.md §10a).
6. Regime-change criterion:                            DEFER W/ TRIGGER (rec) / DEFINE NOW / other
   → RULED 2026-08-06: DEFER W/ TRIGGER as drafted — then SUPERSEDED same session when the
     card's "undefined everywhere" premise was found false (evidence-standards.md §4 gate B3
     already defines regime change). Andy's fresh ruling: B3 RATIFIED as the regime-change
     conjunct's definition; the deferral narrows to a detector question — wire B3 to a scripts/
     detector, or a recorded manual-evaluation protocol run at each review date, before the
     earlier of any arm's/variant's first n=60 interim read or 2026-11-30.
7. Tomorrow-morning mechanical sweep:                  GO / NO-GO / GO minus: ___
   → RULED 2026-08-06: GO, re-ordered — see slot 4 amendment (ii).
```

**Same-night rulings outside this card's seven slots — 2026-08-06.** Made by Andy during
tonight's Phase A OA build session (a separate session from this card), recorded in
`docs/state.md` and `docs/session-log.md`'s 2026-08-06 (late) entry, noted here so this card
and the live-facts page do not diverge:
- **C8** — build without sibling-close; the spread, not the condor, is the unit for early exits
  (`greenfield-family-spec.md` §4.3).
- **PR-16** — re-scoped to the armed trail, target=40 / trail=15.
- **F-4** — probe-first: `SENTINEL-SL1` left unimplemented, Default Value = NONE, flagged as an
  open Day-0 blocker — not yet decided, must be ruled before any arm's `AUTOMATIONS` goes ON.

---

## 1. "Amend the plan" grant — propagate the four ruled 08-04 decisions into the six carrier docs

### Forcing fact

`docs/state.md`, decision-memo block (grep: `NOT YET PROPAGATED` = 1 match):

> ⚠️ **NOT YET PROPAGATED — the rulings are recorded, the docs are not yet amended.** D-1, D-4,
> Decision 4 and Decision 5 all imply edits to `build-plan.md`, `oa-platform-reference.md`,
> `hedge-research.md`, `oa-ops-runbook.md`, `pre-registration-ledger.md` and
> `reactivation-runbook.md` that have **not** been made.

and, same block: `The memo carries the ready-to-paste text` (grep: 1). The memo is
`docs/decision-memo-2026-08-04.md`; **no text is redrafted here — every amendment below points at
the memo's own draft block.**

### Status on device, checked target-by-target tonight

**Already applied (no action, recorded so nothing is done twice):** D-1(a) ledger PR-14…17
MECHANISM + banner and D-1(b) runbook Step C (`the Exit-Options SET as a Bot Input` in
`reactivation-runbook.md`, grep: 1) — applied 2026-08-05 on the gated-batch release · D-4
carriers 1/2 (opr §4.5 banner, §9 row 8) · carrier 5 (`oa-ops-runbook.md` §7 row struck, ruled
D-4, applied 2026-08-05) · carrier 7 (PR-05 — memo says KEEP UNCHANGED) · D-3's runbook Step 0a +
`/settings` capture set incl. `maxexits` (in `reactivation-runbook.md`, grep `maxexits` = 3) —
applied via the Day-0 release D1/D4 · D-1(d): under Option A **no `build-plan.md` §2D amendment
is required** (memo, verbatim).

**Still pending — the grant covers exactly these.** Six gated items (G) + three ungated riders
(U) that travel in the same batch so nothing is silent:

| # | Target | Source text | Device evidence it is pending |
|---|---|---|---|
| G-1 | `oa-platform-reference.md` §8.1 | memo **D-1 draft (c)** — the 📝 append | grep `D-1 ruled. The item-1 dependency resolves` = **0**. §8 is gated |
| G-2 | `oa-platform-reference.md` §8.2 | memo **Decision 6** draft append (attribution restored by re-pricing the 15:50 exit; Template V2 half already landed in the runbook) | grep `attribution restored` = **0**. §8 is gated |
| G-3 | `build-plan.md` §2D | memo **Decision 4 draft (c)** — `"Range075 as a preset"` → `"Range075 in the shared entry automation"` | grep `Range075 as a` = **1** — the frozen sentence still names the preset primitive. See sub-choice 1a below |
| G-4 | `hedge-research.md` §5.2 rule 3 | memo **Decision 4 draft (b)** — the FLAGGED banner | grep `carried as a preset` = 1 (still unflagged); file untouched since 07-31 |
| G-5 | `oa-ops-runbook.md` §3 | memo **Decision 4 draft (a)** — the DESIGNED-sharing replacement sentence | grep `Fork via **Copy**` = **1** — the fork instruction still stands; the 2026-08-05 NARROWED banner fixed the trap-1 cite, not the design. `state.md` still lists the §3-vs-§2D tournament conflict as open |
| G-6 | Decision-5 set, three surfaces that quote one rule and change together: `oa-platform-reference.md` §7 append + `oa-ops-runbook.md` §5 trap 6 cell + one clause in `hedge-research.md` §10's restatement | memo **Decision 5** draft | grep `banned on every entry` = **0** in all three files; the exit-scoped originals each assert cleanly (`banned on every exit in the v2 fleet` = 1 · trap-6 cell = 1 · `banned on every v2 exit` = 1) |
| U-1 | `oa-platform-reference.md` §10 | memo D-4 carrier 4 — dated append beneath `Neither has been tested.` (grep: 1, still standing) using the memo's **standard replacement sentence** | ungated §0.2 append, evidence = the 2026-08-04 log read |
| U-2 | `oa-platform-reference.md` §4.5 "Carry the uncertainty" block | carrier 3 — one-line dated pointer. *Materially covered already*: the ⛔ ANSWERED banner sits directly beneath it (device-read tonight); this is a cross-reference line, not new content | ungated |
| U-3 | `reactivation-runbook.md` §1 | carrier 6 — "Keep, add one clause" to the `one rep` caveat (grep: 1). Draft clause: *"(and the failsafe is excluded as the June cause — zero June errors on either Fortress bot, newest error Apr 16, 2026; `oa-platform-reference.md` §4.5, ruled D-4 2026-08-04. The mechanism itself is real — tripped March/April, entry scanners.)"* | ungated correction, first-hand evidence |
| U-4 | `state.md` | refresh the embedded greenfield-spec hash: the page records `99abab8f…` "on-device verified 2026-08-05 at close-out"; the device file tonight reads **`0797de38…`** — the C0a-probe annotations moved it again after that close-out. Third instance of the flagged hash-goes-stale class | ungated; first-hand `shasum` tonight |

### Sub-choice 1a — G-3 timing

The memo conditions the Range075 amendment on a UI check not yet run (*does the preset picker
accept anything that is not an Exit Option criterion — presumed no, not observed*). Against
holding: the category fact is documented affirmatively — `Save your Exit Option criteria as a
Preset` (opr §6.1, grep: 1) — and Range075 is an entry decision by `hedge-research.md` §8's own
words (`gap filter, not an intraday-range filter`, grep: 1); the greenfield spec already
implements the correct substance (two Symbol-change-% nodes in the shared scanner, §12 row 2
points at this exact amendment); and if slot 4 is authorized, the build runs *through* a frozen
sentence that names a primitive that cannot express the mechanic — the HedgeD defect class.
**Recommend APPLY NOW**, with the memo's stated reopen if the UI check ever contradicts.

### Recommendation

**Grant the batch.** Every item is a ruled 08-04 decision whose text Andy has already seen in the
memo; the alternative is a third consecutive session discovering the same seven gaps. One
paragraph of rationale: the propagation-sweep record on `state.md` exists because *"a ruling that
reached the document it was recorded in and no further"* is this project's most-reproduced defect
class (7 instances); the gated remainder above is precisely the tail of that class, each item
already drafted, each verified pending on the device tonight.

**RULING SLOT 1:** Amend the plan — apply G-1…G-6 (+U-1…U-4) from the memo's draft blocks: YES / NO / strike list.
**RULING SLOT 1a:** G-3 Range075 wording: APPLY NOW / HOLD.

---

## 2. Ledger §1/§3/§7 count scoping — ⭐ ALREADY APPLIED; no ruling needed

This slot was queued on the expectation that `pre-registration-ledger.md` §1/§3/§7 still read
`≈18–20 active bots`. **Device-checked tonight: the S-2 scoping landed 2026-08-05 on the
gated-batch release and is verified in place.**

- Preamble: the original is struck in place and replaced — `≈18–20 plan bots plus up to 8
  pre-registered Track B arms` (grep: 1); the only surviving `18–20 active bots` string on the
  file is the struck original inside that banner (grep: 1, line 14).
- §3 heading now reads `## 3. The roster — ≈18–20 plan bots, plus ≤8 Track B arms. Ceiling 28.`
  with the 📝 SCOPED 2026-08-05 release banner citing `build-plan.md` §2D's 🔓 amendment, S-1,
  and the C12 discharge with its `[FIRST-HAND, UNCORROBORATED]` residual and reopen condition.
- §7's checklist line carries the same strike-and-replace. `ceiling 28` appears 5× across the
  three surfaces.
- Independent record: `track-b-arms-spec.md` §11-1f item (iv) is closed with the same evidence,
  and `state.md`'s gated-batch banner lists it as released by Andy.

**RULING SLOT 2:** NO ACTION NEEDED — confirm, or name anything to reopen.

---

## 3. PR-14…17 family-level kill criterion — ⭐ ALREADY REPLACED; no ruling needed

Same situation as slot 2. The vacuously-unfireable criterion (*"more than one differing input"*
— unreachable under D-1 Option A, each arm holding exactly one exit input; the identical defect
the memo used to reject Options B and C) **was replaced 2026-08-05 under row S-5** and is
verified in place tonight:

- The operative entry reads `FAMILY-LEVEL (REPLACED 2026-08-05 — see the banner below this
  entry)` (grep: 1) and now fires on `MORE THAN ONE MECHANIC` — field granularity, a trigger
  field plus its own pricing sub-field — plus §8.3's assert rules A1/A2/A3/A7/A8, matching the
  spec's §9 comparative form exactly.
- The original wording survives only inside the REPLACED banner's quote (grep `more than one
  differing input` = 2, both inside record-of-original context). `vacuously unfireable` banner
  present (grep: 1).
- Status is unchanged where it must be: **DRAFT — UNSIGNED.** Signing remains a Day-0 act under
  §7, including item 3's gate (does the loop actually produce the number the criterion needs —
  see slot 6 and greenfield §12 row 13).

**RULING SLOT 3:** NO ACTION NEEDED — confirm, or name anything to reopen.

---

## 4. Build-start authorization — the 7-bot family + 4 shared automations, pre-Day-0, toggles OFF

### Forcing facts

- `docs/state.md` greenfield block header: `DO NOT START THE BUILD` (grep: 1) — written when six
  Phase-0 checks blocked; superseded **in part** 2026-08-05: **C0a passed both clauses**
  (Architecture E buildable), C3/C4/C5/C6/C11 answered; still open per the spec's Phase-0 table:
  `untouched: C0c · C2 · C7 · C8 · C9` (grep: 1) plus **C1 PARTIAL** (`stoploss` unit unread —
  SL100/SL200 rungs underived). C10 is open but gates **ARM-B1 only**, not this family.
- `docs/greenfield-family-spec.md` §10: `Layer 2 is DEFERRED to Day-0 for every step in this
  build` (grep: 1) — the spec is *written* for a pre-Day-0 build on the inactive account.
- `docs/state.md`: `Edits made while inactive persist` (grep: 1) and `bot CREATION persists`
  (grep: 1) — the platform holds the work.
- `docs/reactivation-runbook.md` §3 Step A: `any fresh build until this pilot is clean` (grep: 1)
  and `Claude does not self-certify` (grep: 1) — **a hard gate this card cannot close; slot 4a
  puts it to Andy explicitly.**
- The Max-capacity downgrade lands 2026-08-07 14:52 ET; Chrome-driving OA builds are the
  heaviest work this project does.

### Options

**A — AUTHORIZE the staged session (recommended):** Phase-0 remaining checks → cleanup sweep
(slot 7) → Phase A → Phase B per arm, atomic, in spec order — under the pre-ruled package below.
**B — PROBE-ONLY now:** run only the remaining Phase-0 checks in the Max window (the 08-05 probe
is the proven template); build later at standard capacity. The adversarial reviewer's preferred
option: the runbook's real deadline is Day-0 (*"the entire build happens before you pay"*), not
14:52 tomorrow, and capacity is a cost gradient, not a cliff.
**C — DEFER everything** to the Day-0 build window.

### Recommendation — A, as a staged session whose STOPs are binding, under this package

A degrades gracefully into B by construction: the session opens with the probe, and if Phase 0
stops, the session stops — nothing is bought by choosing B in advance except forfeiting the
window on the branch where the checks pass. The package (every item below is part of the YES):

1. **Pilot-clean declaration (slot 4a).** No fresh build starts without Andy's explicit
   declaration per runbook §3 Step A. The ritual is recorded complete with a no-unintended-edits
   capture-diff; the declaration itself is Andy's and is not on file.
2. **Phase 0 first, STOPs binding, no substitutions.** C0b direct look (needs a scratch bot —
   ordered BEFORE the slot-7 deletions), C0c, C1-`stoploss`, C2, C7, C8, C9. C7/C8 STOP outright
   per spec. **C2 fail → Trail arm returns to Andy (re-stamp PR-16), no in-session substitute.
   C1 resolving to anything but %-of-credit → SL100/SL200 return to Andy; no in-session
   re-stamp** (re-stamping pre-registration text is gated).
3. **C9 pre-ruled re-scope** (reviewer FATAL: C9 — does `Position closed` fire on Events-class
   and ITM-action closes — is a *firing-semantics* question an inactive account cannot answer;
   left as-written it lawfully stops the whole build at the Phase-0 header). Re-scope: C9 moves
   to a **Day-0 behavioural read before any arm's AUTOMATIONS goes ON**, and the build proceeds
   on the conservative branch the spec already builds — the 15:44 sibling-close gate stands
   regardless of C9's answer. This is a spec-text change and is inside this ruling.
4. **This YES finalizes four reserved decisions, named so they are not smuggled:** arm count =
   **7** and PR literals **PR-14…PR-20** · the **one-family** reading of §2D's arithmetic
   (spec §12 row 3) · underlying **QQQ** (row 4) · **ride arm = time-exit-only**, not empty
   bundle (row 5).
5. **Partial-build protocol, pre-stated:** each arm is atomic through B8; arms whose primitives
   confirmed build; unconfirmed arms return to Andy; **the family trades only after full Phase C
   on the final roster** — no ranking, no signing, of a subset.
6. **A4 contradiction resolved:** the spec asks for a dead-bot test-fire of `GF-SiblingClose` in
   the same section that forbids test-fires. Resolution inside this ruling: build + config-read
   verification now; the **fire test executes at Day-0, on a designated bot, before any arm's
   AUTOMATIONS goes ON** — queued and tracked with the other Layer-2 deferrals.
7. **Phase C1–C3 (21-pair capture-diff · §8.3 nightly assert A1–A8 · A7 baseline wired into
   `daily.sh`) is scheduled as a tracked pre-Day-0 deliverable** — code-lane work that does not
   need the Max window and without which the family has no drift detector.
8. **Hard stop 14:30 ET 2026-08-07.** Whatever is unbuilt continues at standard capacity; the
   deadline that binds is Day-0.

**Explicitly NOT authorized by a YES:** any `AUTOMATIONS` toggle → ON, anywhere · signing any
PR entry (Day-0, per the ledger: *"Day-0 is signing, not authoring"* — build → capture → sign →
switch-on is the designed order) · Track B arms B1/B2 (separate allocation; PR-21/22 DRAFT
unsigned; ARM-B1 not an arm until C10 closes) · any capital · `itmlive` (stays `auto`; hard
Day-0 gate Step 0a) · any toggle move on the nine leave-in-place bots (Step 2c's no-touch
observation stays unspoiled — this build creates new bots and flips nothing on the lapsed nine).
Per spec step B5 the new bots stand `EXIT OPTIONS` ON / `AUTOMATIONS` OFF: with no positions
possible on an inactive account this is inert, and the reverse arrangement is the v1 killer
(config present, exit toggle OFF).

### Adversarial record — slot 4

Original recommendation **REFUTED as drafted** (subagent verdict), on: C9 is not a UI read and
lawfully stops the build (→ package item 3) · the pilot-clean gate was unsatisfied and unnamed
(→ item 1 / slot 4a) · four reserved decisions were being finalized silently (→ item 4) · the C1
fallback routed a gated re-stamp into the session (→ item 2) · no partial-build protocol (→
item 5) · A4's test-fire contradiction (→ item 6) · Phase C silently out of scope (→ item 7) ·
checks/cleanup ordering entangled with C0b's scratch-bot need (→ item 2 + slot 7 sequencing).
**Surviving objection, carried not cured:** *deadline pressure is this repo's documented
defect-generator* (§9.1a has failed twice; the byte-exact Notes compare exists because the pilot
silently lost content) and the compressed workload is roughly an order of magnitude beyond
demonstrated single-session throughput. Mitigations are the hard stop, atomic per-arm
checkpoints, and the standing verification discipline — the pressure itself is not curable by
wording, and Option B exists for exactly this reason. Two attacks failed and are recorded as
support: pre-signing build does not invert "no entry, no restart" (signing needs the build's own
capture hash), and EXIT-OPTIONS-ON pre-Day-0 is the safe arrangement, not the risky one.

**RULING SLOT 4:** AUTHORIZE (package 1–8) / PROBE-ONLY / DEFER.
**RULING SLOT 4a:** Pilot declared clean: YES / NOT YET.

---

## 5. Double-testing — GF-SL100 / GF-SL200 / ARM-B1 vs the signed Track A §3 set

### Forcing facts

- `greenfield-family-spec.md` §12 row 11, second clause (standing, post-S-1): GF-SL100/GF-SL200
  duplicate signed Track A §3 variants and `pool error rates nowhere` (grep, normalized: 2 —
  row 11 and its §11 echo); *"one hypothesis, two engines, no shared multiplicity accounting"*;
  ARM-B1 (`DSTOP_100`) has the identical defect.
- `track-b-arms-spec.md` §6.3 (heading grep `does not double-test a signed Track A variant` = 1):
  §10a's family is the 9 computable variants × every bot under test, and `an arm is a bot under
  test` (grep: 1) — so an arm's own ledger re-enters Track A's family carrying the same variant.
  Only ARM-B2 is tested in exactly one place.
- `research-loop-spec.md` §3 (device-read tonight): the signed 12-variant set includes SL100 ·
  SL200 · DSTOP_100; §10a item 1: `The family is the 9 computable variants` (grep: 1) × every
  bot under test. **Precedent in the same section:** `slots are retired to Track B` (grep: 1) —
  R-2 retired `TIME_*` from §3 when the question moved to a live arm, which is why ARM-B2 is
  clean. The program has already solved this defect once, by retirement.
- `greenfield-family-spec.md` §11 CF-4: sibling-close makes the SL arms **close-both** mechanics
  — PR-18/PR-19 are renamed in substance `SL100/SL200-close-both` with an instruction not to
  publish under the anchor's name. **The arm and the Track A variant are therefore not the same
  estimand**: Track A's counterfactual on the Ride ledger tests the per-spread stop; the arm
  tests the close-both stop.

### Options

**(a) Precedence rule** — Track A advisory-only for dual-tested variants; graduation only from
the arm. *(The original recommendation. Refuted: it does zero statistical work — "one family"
with no correction over it; it leaves Track A's kill/peeking channel open; it doesn't touch the
reverse direction, the arm's ledger re-entering §10a's family; and its "one hypothesis" clause
writes a claim CF-4 has already falsified into a signed spec.)*
**(b) R-2-shaped scoped retirement (recommended)** — exclude the dual-tested (bot, variant)
pairs from Track A's computed family, document CF-4 non-equivalence, bar advisory influence.
**(c) Drop an arm** — costs the only live test of the loss-side mechanic; Track A's evaluation
of these rungs is additionally flattered by marks-vs-fills and its engine is 0.1.0-DRAFT with
three fatal defects, not wired in.
**(d) Accept and document** — leaves two graduation paths open for one variant name; the exact
hole the ledger exists to close.

### Recommendation — (b), as a four-part package

1. **Scoped retirement, R-2 precedent, one paragraph appended to `research-loop-spec.md` §10a
   (gated — this signature covers it).** Draft: *"§10a item 1 is scoped 2026-08-06: the family
   excludes any (bot, variant) pair where the bot belongs to a pre-registered live-arm family
   that runs that same variant as an arm — at signing: SL100, SL200 and DSTOP_100 on the seven
   greenfield-family ledgers and on any Track B arm ledger. Rationale: a live arm re-entering
   the counterfactual family carries its own variant, degenerating to the CONTROL tautology;
   and R-2's precedent — a question moved to a live arm is retired from §3's computed set, not
   run twice. The variants remain in §3 and continue to compute on all non-family ledgers. The
   set remains 12; the §10 freeze holds without a count change."*
2. **Non-equivalence documented (CF-4):** one dated note in `greenfield-family-spec.md` §9
   (PR-18/PR-19) and `track-b-arms-spec.md` §6.3/§5.5 — the arms are **close-both** mechanics,
   Track A's SL100/SL200/DSTOP_100 are **per-spread**; neither result may be published under the
   other's name, and neither is a replication of the other.
3. **No-influence rule, carried into PR-14…20 and PR-21/22 at signing:** a Track A advisory
   read on a dual-named variant may not trigger, accelerate, or veto any arm disposition before
   the arm's own pre-declared gate date; kill authority for these variants rests solely with the
   arm's pre-registered criteria. (Closes the peeking channel the precedence rule left open.)
4. **Honesty line, §12-row style:** no cross-engine multiplicity accounting exists or is created
   by this ruling; within-family multiplicity stays with Phase C4's declared Bonferroni-across-6;
   Track A's stays with §10a's max-T. Recorded as a carried limitation, not solved.

### Adversarial record — slot 5

Original recommendation (option (a)) **REFUTED** (subagent verdict). Objections that forced the
change, all folded in above: the omitted dominant remedy — the program's own R-2 retirement
precedent (→ part 1) · CF-4 falsifies the "one hypothesis" premise, so the precedence paragraph
would have written a known-false equivalence into a signed spec (→ part 2) · the censoring
rationale used to reject drop-an-arm was wrong for these specific variants — against the Ride
control every stop is *tighter* than the incumbent, so the real Track A defect here is
marks-vs-fills flattery, not censoring (rejection restated above) · advisory/kill asymmetry and
peeking uncontrolled (→ part 3) · "cheap form of (a)" mislabeled — no statistical work done
(→ part 4) · the arm-ledger→§10a re-entry direction unaddressed (→ part 1's exclusion clause) ·
§10a was quoted second-hand (cured: §3/§10a device-read tonight, quotes asserted). **Surviving
demotion, carried:** at declared samples neither engine can resolve the +0.015R margin
(±0.026R half-width at n=100; ~307 paired days, ~560 with Bonferroni — §12 row 16), so this slot
is pre-declaration hygiene, not a live graduation dispute; and the package binds little for
ARM-B1 until C10 closes and `bots_config_v2.csv` exists. Recorded as such.

**RULING SLOT 5:** RETIRE-SCOPED package 1–4 (rec) / PRECEDENCE ONLY / DROP AN ARM / ACCEPT+DOCUMENT.

---

## 6. The regime-change conjunct — define now, or defer by recorded decision

### Forcing facts

- `build-plan.md` §5 (frozen): `n≥100 / 6 months / a regime change` (grep: 1) — the evidence
  gate is conjunctive.
- `greenfield-family-spec.md` §12 row 12: the third conjunct is `undefined in every document`
  (grep: 1). `track-b-arms-spec.md` §11 item 6: `undefined everywhere` (grep: 1) — found twice,
  from two directions, and per that row *"no arm and no variant can graduate until it is written
  and signed, regardless of n or elapsed time."*
- Constraint from the ledger's own law (§2 rule 2): a criterion needing evidence nobody collects
  is not a criterion — any mechanical definition needs a daily vol series the loop does not
  currently ingest.

### Options

**Define now** — sign the draft below tonight. **Defer with a recorded trigger (recommended)** —
deferral as a dated decision, not silence.

### Recommendation — DEFER, with this recorded trigger

Nothing can graduate before roughly six months post-Day-0 (mid-Feb 2027 at earliest), the
evidence-standards redesign Andy already wants is the natural home for the definition, and a
load-bearing statistical definition drafted against a capacity deadline is how this repo's worst
text got written. **Trigger, recorded as a dated decision in `evidence-standards.md` §4 (gated —
this ruling covers the note) and `state.md`:** *"The regime-change conjunct is undefined by
recorded decision 2026-08-06, not by omission. It must be defined and signed before the earlier
of (i) any arm's or variant's first interim read at n=60, or (ii) 2026-11-30. Defining it
requires naming its data source; the daily loop currently ingests none. Until defined, the third
conjunct cannot be satisfied and nothing graduates — the gate fails closed, not open."*

**Draft definition, included so DEFINE NOW is signable tonight if preferred:** *a regime change
is recorded when, relative to the regime prevailing at the sample's start, either (i) the
21-session median VIX close crosses a fixed band boundary (<15 / 15–25 / >25) and holds the new
band ≥10 consecutive sessions, or (ii) 21-session realized volatility of the underlying doubles
or halves and holds ≥10 sessions. A sample satisfies the conjunct only if it spans ≥1 recorded
change. Detector: nightly in `daily.sh` from an ingested daily close series; until the detector
exists, evaluated manually at review dates, each evaluation logged.*

**RULING SLOT 6:** DEFER W/ TRIGGER (rec) / DEFINE NOW (sign the draft) / other.

---

## 7. Tomorrow-morning mechanical pull-forward — go/no-go

### What it is

Runbook §3 Step B ("Capture the roster, then sweep") plus the three remaining clones of Step C —
already pre-Day-0 work by the runbook's own structure; the pull-forward is executing it in the
last Max-window morning. Contents: the 20-bot Group-A archive · the 2 deletions
(`TEST QQQ-IC-0DTE-HedgeC-S3 Clone`, `QQQ-IC-0DTE-InvFilter-Wide150`) · the ruled third delete —
the Library object `CLAUDE-C5-SHARED-SCRATCH` (state.md: `must DELETE IT EXPLICITLY`, grep: 1;
ruled D5 2026-08-05) · clones PR-01 `IC-SPX-FastPT25-S2`, PR-02 `-130PM`, PR-04
`-NoPT50` per §2's checklist.

### Forcing facts

- `build-plan.md` §2: `Positions → archive. Empty → delete.` (grep: 1) and `The capture must be
  taken before any deletion` (grep: 1). Delete rule: only bots BOTH zero-trade AND absent from
  the disposition table; `DIR-SPX-PutVIX22-SL75` is the zero-trade bot that must NOT be deleted;
  full-name check (`Opening Range Breakout 60m` archived vs `60min-ORB-10W-Paper-v1` stays).
- `reactivation-runbook.md` Step B (D5, ruled): bots first, object second; verify-back =
  `My Automations` returns to exactly **one** shared automation (`Defang-Mon-S2-StrikeTouch`);
  if it will not delete or the count is wrong — do not force, record, escalate.
- `state.md`: `would not fire from Claude` (grep: 1) — `archiveBot` resisted three distinct
  mechanisms on 2026-08-04; Andy archived manually; the coordinate fallback is refused by
  standing rule (`Delete` sits ~29px below `Archive`).
- Clone gate: the same pilot-clean declaration as slot 4a (`any fresh build until this pilot is
  clean` covers "the other three clones" in the same sentence).

### Recommendation — GO, in this order, with these constraints

1. **Fresh bookmarklet `/bots` capture first** (expected count written down first: **35**); the
   7/30 capture predates the pilot renames and the 36→35 archive.
2. **C0b's direct look (slot 4, package item 2) runs BEFORE the deletions** — it needs a scratch
   bot, and the deletions destroy both.
3. **Delete exactly two bots, then the C5 Library object, then the verify-back to exactly one
   shared automation.** Escalate branch as ruled — no forcing. These are the only irreversible
   acts in the morning; everything else is rename/clone/config.
4. **Cleanup completes BEFORE greenfield Phase A** (slot 4), or the verify-back's
   "exactly one" is unmeasurable — after Phase A the correct count becomes five (1 + the 4 GF
   shared objects).
5. **The archive halves are queued for Andy's hand, not burned against.** 20 Group-A archives +
   3 clone-original archives are ~23 operations of the exact class that failed 3-for-3 on
   08-04. Claude attempts the first via the dispatched-event sequence; on three failures the
   whole archive half goes to Andy's queue. Nothing blocks on it: originals are **renamed
   first** (`-ARCHIVED-2026-08-06` style — rename is proven to work), so every production name
   is free and the archive is hygiene, per the pilot precedent.
6. **The three clones per §2's checklist, pilot-clean gate permitting (slot 4a):** PR-01/PR-02
   get **only** the two safety fixes (re-entry gate → `opened this side today`; Cleanup pricing
   Market → SmartPricing) — they are the deliberately Exit-Option-free ride+S2 controls;
   standing exception says do not "fix" them further. PR-04: 15:50 time exit + 15:52 backstop,
   NO PT50 (removed from the action, not toggled off). Every step two-layer verified, Layer 2
   deferred and queued.
7. **No toggle moves on the nine leave-in-place bots** — Step 2c's no-touch observation stays
   intact. Hard stop 14:30 ET.

**RULING SLOT 7:** GO / NO-GO / GO minus named items.

---

## Verification appendix

**Method.** Every quote above was asserted against the **device file** via `device_bash`
(`grep -cF`, or whitespace-normalized count where the phrase wraps a line), match count exactly
1 unless stated. No quote was taken from a staged copy (`CLAUDE.md` §9.1a; the 2026-08-03
altered-staged-read incident). The two adversarial subagents ran against staged copies for
speed; every claim of theirs that this card relies on was re-verified on the device.

**Files read in full or in cited sections tonight, sha256 at read time:**

```
a95e6c6e2d368f2c…  CLAUDE.md
158b1492c50e0b10…  docs/state.md
cd39b97230a5ab99…  docs/decision-memo-2026-08-04.md
0797de386a112272…  docs/greenfield-family-spec.md   ← state.md still cites 99abab8f…; see slot 1 U-4
e2753227556ecb93…  docs/track-b-arms-spec.md
e16bd23ca61f6ab5…  docs/pre-registration-ledger.md
289b701a74b29a3f…  docs/build-plan.md
800ccc6a1ed3ae1d…  docs/oa-platform-reference.md
7d3e751f8993d37e…  docs/hedge-research.md
489501882c99fa8e…  docs/oa-ops-runbook.md
919349b6bc5f1e46…  docs/reactivation-runbook.md
3fe3369ada262ac7…  docs/research-loop-spec.md
```

**Key single-match asserts (file | pattern | count):** state.md `NOT YET PROPAGATED` 1 ·
opr `D-1 ruled. The item-1 dependency resolves` 0 · opr `attribution restored` 0 ·
opr `banned on every entry` 0 · oor `banned on every entry` 0 · oor `Fork via **Copy**` 1 ·
hedge `may be a category error` 0 · hedge `carried as a preset` 1 · build-plan `Range075 as a` 1 ·
ledger `≈18–20 plan bots plus up to 8 pre-registered Track B arms` 1 · ledger
`FAMILY-LEVEL (REPLACED 2026-08-05` 1 · ledger `vacuously unfireable` 1 · greenfield
`untouched: C0c · C2 · C7 · C8 · C9` 1 · greenfield `Layer 2 is DEFERRED to Day-0 for every step
in this build` 1 · track-b `does not double-test a signed Track A variant` 1 · track-b `an arm is
a bot under test` 1 · rls `The family is the 9 computable variants` 1 · rls `slots are retired to
Track B` 1 · build-plan `n≥100 / 6 months / a regime change` 1 · greenfield `undefined in every
document` 1 · track-b `undefined everywhere` 1 · state `must DELETE IT EXPLICITLY` 1 · state
`would not fire from Claude` 1 · build-plan `The capture must be taken before any deletion` 1 ·
runbook `any fresh build until this pilot is clean` 1 · runbook `Claude does not self-certify` 1 ·
runbook `the Exit-Options SET as a Bot Input` 1 · opr `Neither has been tested.` 1 · opr
`State it as a hypothesis in pre-registration` 1 (normalized) · opr `Save your Exit Option
criteria as a Preset` 1 · hedge `gap filter, not an intraday-range filter` 1.

*Card written 2026-08-06. Nothing was edited, no OA surface touched, no git run. Post-ruling
work applies exactly what each ruling authorizes, with per-file dated amendment conventions,
originals left standing where required, and every edited file verified by direct `device_bash`
sha256 + single-match grep of the inserted text.*
