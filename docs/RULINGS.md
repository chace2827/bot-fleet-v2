# RULINGS — canonical, append-only register

*Consolidated 2026-08-12 from the sources named in every record's `source` field:
`docs/decision-card-2026-08-08.md` · `docs/decision-card-2026-08-06.md` ·
`docs/g-rulings-card-2026-08-07.md` · the ruling sections of `docs/session-log.md` and
`docs/state.md`. **Nothing here is new.** No ruling was invented, none was merged, none was
re-derived, and no source file was edited. Where a ruling's own wording is quotable it is quoted
verbatim in `verbatim`; where the source records only the applied disposition, `verbatim` carries
that disposition's own words and `unclear` says so.*

## How to use this file

- **APPEND-ONLY.** Never edit or delete an existing record. A ruling that changes is expressed by
  **appending a new record** and setting the old record's `status: Superseded` +
  `superseded_by: <new id>` — those two fields are the only mutation this file permits.
- **This file does not rule anything.** It is a register. The authority for every entry is the
  source named in its `source` field; on any disagreement the source wins and the divergence is
  recorded here as a new record, not fixed silently.
- **Machine-readable.** Every record is one fenced ` ```yaml ` block containing exactly one YAML
  mapping. A parser extracts all `yaml` blocks in file order and `safe_load`s each one.

## Schema

| field | meaning |
|---|---|
| `ruling_id` | `R-<ruling date>-<the source's own item label>`. Unique, stable, never reused. |
| `date` | The date the ruling was made, as recorded in the source (ISO). |
| `scope` | One line: what the ruling is about. |
| `verbatim` | The ruling text, verbatim from the source. `verbatim_of` names what was quoted. |
| `verbatim_of` | `andy` (Andy's own words) · `ruling_text` (the source's recorded ruling/disposition wording). |
| `owner` | `Andy` for every record — the owner of every ruling in this project. |
| `status` | `Active` · `Superseded` · `Gated` (ruled but not in force / still needs a further gate). |
| `applies_to` | Files, bots, PR entries or specs the source names as the ruling's surface. |
| `superseded_by` | Ruling id, or `none`. |
| `source` | Repo-relative file + section the record was taken from. |
| `unclear` | `false`, or a `[UNCLEAR] …` string naming exactly what is ambiguous and in which source. |

## Counts at consolidation (2026-08-12)

- Records: **114**
- `[UNCLEAR]`: **9**

---

## RULINGS

```yaml
ruling_id: R-2026-07-31-RULING-1-R-DENOMINATOR
date: 2026-07-31
scope: The R denominator for a condor — risk is the larger side, not the sum of both sides.
verbatim: >-
  Ruling 1 — R denominator FIXED. `scripts/report.py` condor aggregation now uses
  `c["risk"] = max(c["risk"], fl(t["risk"]))` instead of `+=`. Anything quoting a
  pre-2026-07-31 condor Exp(R) is quoting the flattered number.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: scripts/report.py; every condor Exp(R) quoted anywhere; data/receipts/r-denominator-fix.txt
superseded_by: none
source: docs/session-log.md — "2026-07-31 — Three rulings executed + Block 2", Ruling 1
unclear: "[UNCLEAR] the source records the ruling as executed but does not name who ruled it; owner Andy is the project-wide owner, not a quoted attribution (docs/session-log.md 2026-07-31)."
```

```yaml
ruling_id: R-2026-07-31-RULING-2-GATE-T3
date: 2026-07-31
scope: Gate T3 defined — the ledger's previously undefined "separate, weaker gate".
verbatim: >-
  Ruling 2 — gate T3 DEFINED. parameters frozen before the window · window untouched during
  design · n>=100 backtest trades over >=2 years incl. a regime change · positive after a 30-40%
  haircut + commissions · beats its control · clears the F1 multiple-comparisons haircut.
  Scope is the important half: a T3 pass authorises BUILDING and PAPER-RUNNING an experiment and
  setting its sizing tier. It never authorises live capital, and B1 is unchanged.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/evidence-standards.md; docs/pre-registration-ledger.md; every experiment build/paper-run authorization
superseded_by: none
source: docs/session-log.md — "2026-07-31 — Three rulings executed + Block 2", Ruling 2
unclear: "[UNCLEAR] the 30-40% haircut is a range, not a number — flagged for the redesign session by the source itself (docs/session-log.md 2026-07-31)."
```

```yaml
ruling_id: R-2026-07-31-RULING-3-THIRD-PARTY-SWITCH
date: 2026-07-31
scope: The garbled "switch to a third-party platform" record; what the 7/27 audit actually had declined.
verbatim: >-
  Ruling 3 — the record corrected. "Switch to a third-party platform" was a garbled transcription
  of "the go-live SWITCH held by a THIRD PARTY." No platform-migration recommendation exists
  anywhere in the audit. What was actually declined is audit §5.5 items 6-7: custody separation and
  independent go-live authority. Reason recorded: go-live authority stays with Andy.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: CLAUDE.md §4; docs/evidence-standards.md §1 and §9.2; the audit banner; the pre-commitment ledger banner. NOT applied to build-plan.md §5 (frozen; needs an explicit "amend the plan")
superseded_by: none
source: docs/session-log.md — "2026-07-31 — Three rulings executed + Block 2", Ruling 3
unclear: false
```

```yaml
ruling_id: R-2026-08-04-D-1
date: 2026-08-04
scope: How an exit mechanic is expressed as a bot input — Option A, the Exit-Options SET as a Bot Input.
verbatim: >-
  DECIDED 2026-08-04: Option A — Exit-Options-SET as a Bot Input. Gates closed first: G1 YES
  (empty bundle saves, server-confirmed — the `ride` arm IS expressible), G3 compatible, G4 no
  propagation. RIDER, forced by G2 (REFERENCE not values): every capture surface —
  `bots_config_v2.csv`, the capture-diff and the drift detector — must read the INPUT OBJECT, not
  just the action, or every arm diffs as identical; and `oldValue` must never be read as current
  config (stale pre-link snapshot).
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: data/bots_config_v2.csv; the capture-diff; the drift detector; docs/reactivation-runbook.md Step C; docs/pre-registration-ledger.md §6
superseded_by: none
source: docs/state.md — "FOUR DECISIONS — ALL DECIDED 2026-08-04", D-1 row
unclear: false
```

```yaml
ruling_id: R-2026-08-04-D-2
date: 2026-08-04
scope: The IC-per-day ceiling and whether to split a strategy across bots to exceed it.
verbatim: >-
  DECIDED 2026-08-04: cap at 5 ICs/day, ONE bot. Accept the platform ceiling; do not split a
  strategy across two bots to reach 10. Rationale: one bot = one config row = one pre-registration
  entry = one ledger identity. Revisit only if a spec genuinely needs >5 entries in a session.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: every re-entry spec; posLimitDay / posLimit on every IC bot; docs/oa-reconciliation-report.md R-11
superseded_by: none
source: docs/state.md — "FOUR DECISIONS — ALL DECIDED 2026-08-04", D-2 row
unclear: false
```

```yaml
ruling_id: R-2026-08-04-D-3
date: 2026-08-04
scope: The ITM-action setting — itmpaper and itmlive.
verbatim: >-
  DECIDED AND PART-EXECUTED 2026-08-04: `itmpaper` = `market` (done, hard-reload + `input.value`
  verified, before/after screenshots on file). `itmlive` = `market` is a HARD DAY-0 GATE —
  deliberately left at `auto`; it must be set before any capital is live.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: OA account settings (itmpaper, itmlive); docs/reactivation-runbook.md Step 0a; docs/oa-platform-reference.md §13.1
superseded_by: none
source: docs/state.md — "FOUR DECISIONS — ALL DECIDED 2026-08-04", D-3 row
unclear: false
```

```yaml
ruling_id: R-2026-08-04-D-4
date: 2026-08-04
scope: The Excessive-Errors failsafe as the cause of the 2026-06-12 lapse.
verbatim: >-
  DECIDED 2026-08-04: RETIRED as the 2026-06-12 lapse cause. KEPT as a real, documented mechanism
  this fleet has tripped — March/April, on entry scanners. June cause: UNKNOWN.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/oa-platform-reference.md §4.5 and §10; docs/oa-ops-runbook.md §7 and §9 row 8; docs/reactivation-runbook.md §1; PR-05's liveness kill criterion (stays)
superseded_by: none
source: docs/state.md — "FOUR DECISIONS — ALL DECIDED 2026-08-04", D-4 row
unclear: false
```

```yaml
ruling_id: R-2026-08-04-DECISION-4-ARCHITECTURE-E
date: 2026-08-04
scope: Family architecture — how arms differ from one another.
verbatim: >-
  Decision 4 -> Architecture E, share the entry automation and differ on exits; consistent with
  D-1 as the coupling required.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/greenfield-family-spec.md; docs/build-plan.md §2D; docs/oa-ops-runbook.md §3
superseded_by: none
source: docs/state.md — "DECISION MEMO RULED 2026-08-04" banner
unclear: false
```

```yaml
ruling_id: R-2026-08-04-DECISION-5-MARKET-BAN-ENTRIES
date: 2026-08-04
scope: Whether the Market-pricing ban covers entries as well as exits.
verbatim: >-
  Decision 5 -> the Market-pricing ban extends to ENTRIES, recorded as a MECHANISM decision, not
  evidence (n=1 position, n=2 fixture — below the T2 gate).
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/oa-platform-reference.md §7; docs/oa-ops-runbook.md §5 trap 6; docs/hedge-research.md §10
superseded_by: none
source: docs/state.md — "DECISION MEMO RULED 2026-08-04" banner
unclear: false
```

```yaml
ruling_id: R-2026-08-04-DECISION-6-1550-REPRICE
date: 2026-08-04
scope: Re-pricing the 15:50 Expiration exit off Market.
verbatim: >-
  Decision 6 -> re-price the 15:50 Expiration exit off Market, backstop keeps Market — EXECUTION
  DEFERRED: Template V1 / PR-03's config hash is frozen, so it lands as Template V2 with an amended
  pre-registration before Day-0, not as a quiet edit.
verbatim_of: ruling_text
owner: Andy
status: Gated
applies_to: Template V2; PR-03's pre-registration entry; docs/oa-platform-reference.md §8.2; docs/reactivation-runbook.md §2 step 6a
superseded_by: none
source: docs/state.md — "DECISION MEMO RULED 2026-08-04" banner
unclear: false
```

```yaml
ruling_id: R-2026-08-04-DECISION-7-SCANNERA-REVERT
date: 2026-08-04
scope: "Disposition of the writes left on the pilot clone by Tier-2 check #4."
verbatim: >-
  Decision 7 -> RULED AND EXECUTED: ScannerA name and tag reverted, preset `TIER2-CHECK4-PUTSIDE`
  kept, Bot Group stays unset until the Phase 4 sweep.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: Fortress-ScannerA-PutSpread-CLONE; preset TIER2-CHECK4-PUTSIDE; the Phase 4 group sweep
superseded_by: none
source: docs/state.md — "DECISION MEMO RULED 2026-08-04" banner
unclear: false
```

```yaml
ruling_id: R-2026-08-04-RL-R-1
date: 2026-08-04
scope: Research loop — the fixed-dollar stop rungs.
verbatim: >-
  R-1 fixed-$ rungs -> dollar stop at 1.00x/1.50x the bot's trailing-90-day median credit (the
  unsigned 0.50x/0.75x RISK substitution is REJECTED).
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/research-loop-spec.md §3/§10; scripts/research_loop.py (spec only — the engine is not wired in)
superseded_by: none
source: docs/state.md — "Research loop — ALL 7 RULINGS SIGNED 2026-08-04"
unclear: false
```

```yaml
ruling_id: R-2026-08-04-RL-R-2
date: 2026-08-04
scope: Research loop — the TIME_* variant set.
verbatim: >-
  R-2 `TIME_*` replaced by trough-timing rungs, time question retired to Track B.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/research-loop-spec.md §3/§10; docs/oa-export-schema.md (TIME_* set); docs/track-b-arms-spec.md
superseded_by: none
source: docs/state.md — "Research loop — ALL 7 RULINGS SIGNED 2026-08-04"
unclear: false
```

```yaml
ruling_id: R-2026-08-04-RL-R-3
date: 2026-08-04
scope: Research loop — the minimum-effect margin.
verbatim: >-
  R-3 margin -> mean deltaR >= +0.015R, median test withdrawn.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/research-loop-spec.md §3/§10; the greenfield family's equivalence band (see R-2026-08-06-G-13)
superseded_by: none
source: docs/state.md — "Research loop — ALL 7 RULINGS SIGNED 2026-08-04"
unclear: false
```

```yaml
ruling_id: R-2026-08-04-RL-R-4
date: 2026-08-04
scope: Research loop — the start condition.
verbatim: >-
  R-4 start condition -> n >= 30 closed POSITIONS fleet-wide.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/research-loop-spec.md §5 (per bot, variant); scripts/research_loop.py silence floor
superseded_by: none
source: docs/state.md — "Research loop — ALL 7 RULINGS SIGNED 2026-08-04"
unclear: false
```

```yaml
ruling_id: R-2026-08-04-RL-R-5
date: 2026-08-04
scope: Research loop — multiplicity correction.
verbatim: >-
  R-5 -> new §10a, permutation max-T, no Bonferroni term.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/research-loop-spec.md §10a
superseded_by: none
source: docs/state.md — "Research loop — ALL 7 RULINGS SIGNED 2026-08-04"
unclear: false
```

```yaml
ruling_id: R-2026-08-04-RL-R-6
date: 2026-08-04
scope: Research loop — unit of account and combined MFE.
verbatim: >-
  R-6 unit of account is the POSITION and combined MFE for a paired condor is a Track B question.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/research-loop-spec.md §3/§10; docs/track-b-arms-spec.md; CLAUDE.md §4 unit convention
superseded_by: none
source: docs/state.md — "Research loop — ALL 7 RULINGS SIGNED 2026-08-04"
unclear: false
```

```yaml
ruling_id: R-2026-08-04-RL-R-7
date: 2026-08-04
scope: Research loop — treatment of expired positions.
verbatim: >-
  R-7 `expired` stratified. The §3 set remains 12, so the freeze holds without a count change.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/research-loop-spec.md §3; the X-1 group reading (see R-2026-08-06-G-4)
superseded_by: none
source: docs/state.md — "Research loop — ALL 7 RULINGS SIGNED 2026-08-04"
unclear: false
```

```yaml
ruling_id: R-2026-08-05-D0-OBSERVE-FIRST
date: 2026-08-05
scope: Day-0 release sheet D0 / audit finding F-36 — the no-touch observation.
verbatim: >-
  D0 — the no-touch observation: OBSERVE FIRST. The `NOT RULED` slot is now ruled. New Step 2c,
  placed before any toggle moves, with all three branches. Account settings are explicitly carved
  out as *not* toggle intervention, so Step 0a does not spoil it.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/reactivation-runbook.md §4 Step 2c
superseded_by: none
source: docs/state.md — "RELEASE SHEET RULED IN FULL 2026-08-05" banner (D0; audit F-36)
unclear: false
```

```yaml
ruling_id: R-2026-08-05-D1-PROPAGATION
date: 2026-08-05
scope: Day-0 release sheet D1 — the three propagation items.
verbatim: >-
  D1 — propagation, all three. `itmlive` = `market` is now Step 0a, a hard gate before capital is
  live · Template V2 is §2 step 6a and a checklist box · the fleet count is ~18-20 plan bots plus
  <=8 Track B arms, ceiling 28.
verbatim_of: ruling_text
owner: Andy
status: Superseded
applies_to: docs/reactivation-runbook.md Step 0a and §2 step 6a; the fleet-count surfaces
superseded_by: R-2026-08-07-E-1-LAB-SLOTS
source: docs/state.md — "RELEASE SHEET RULED IN FULL 2026-08-05" banner (D1)
unclear: "[UNCLEAR] only the ceiling-28 limb is superseded (E-1 moves it to 30); the itmlive and Template V2 limbs stand. The sources record no per-limb status (docs/state.md D1 banner vs the E-1 block)."
```

```yaml
ruling_id: R-2026-08-05-D2-FAILURE-BRANCHES
date: 2026-08-05
scope: Day-0 release sheet D2 — the failure-branch set and fleet-halt branches.
verbatim: >-
  D2 — the failure-branch set, FULL version with fleet-halt branches. §4 opens with a how-to-read
  block defining *bot stays OFF* vs *fleet stays OFF* and "a check you could not run is NOT a
  pass." §1's heading corrected from "ANSWERED" to EXISTENCE ESTABLISHED, CAUSE STILL UNVERIFIED,
  with Step 6a added to settle it and a full REFUTED branch.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/reactivation-runbook.md §1 and §4 (F-3…F-10)
superseded_by: none
source: docs/state.md — "RELEASE SHEET RULED IN FULL 2026-08-05" banner (D2)
unclear: false
```

```yaml
ruling_id: R-2026-08-05-D3-STEP-3-7-SWAP
date: 2026-08-05
scope: Day-0 release sheet D3 — Step 3 / Step 7 swap and the nine leave-in-place bots.
verbatim: >-
  D3 — the swap, and the nine are NOT exempt from Step 6. Step 3 arms `EXIT OPTIONS` only;
  `AUTOMATIONS` -> ON moved to Step 7, per bot, only for bots that passed. The exemption question
  is now answered in the document: "a pre-existing bot is not a proven bot."
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/reactivation-runbook.md §4 Steps 3, 6, 7; the nine leave-in-place bots
superseded_by: none
source: docs/state.md — "RELEASE SHEET RULED IN FULL 2026-08-05" banner (D3; audit F-2)
unclear: false
```

```yaml
ruling_id: R-2026-08-05-D4-FOUR-OBSERVATIONS
date: 2026-08-05
scope: Day-0 release sheet D4 — DST, the /settings capture set, C10's dstop read, Phase 0 + A7 in the Step 4 gate.
verbatim: >-
  D4 — all four observations. DST (Step 5a) · the `/settings` capture set incl. `maxexits` · C10's
  `dstop` read (Step 6b) · Phase 0 + A7 in the Step 4 gate.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/reactivation-runbook.md Steps 4, 5a, 6b; the /settings capture set
superseded_by: none
source: docs/state.md — "RELEASE SHEET RULED IN FULL 2026-08-05" banner (D4; audit F-7/F-13/F-16/F-18)
unclear: false
```

```yaml
ruling_id: R-2026-08-05-D5-SCRATCH-DELETE
date: 2026-08-05
scope: Day-0 release sheet D5 — deletion of the shared scratch automation.
verbatim: >-
  D5 — the sweep deletes `CLAUDE-C5-SHARED-SCRATCH` after both scratch bots, in that order, with a
  verify-back to exactly one shared automation and a do-not-force branch.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: the mechanical sweep; the OA Automation Library
superseded_by: none
source: docs/state.md — "RELEASE SHEET RULED IN FULL 2026-08-05" banner (D5; audit F-15)
unclear: false
```

```yaml
ruling_id: R-2026-08-05-D6-REMAINDER
date: 2026-08-05
scope: Day-0 release sheet D6 — the remaining nine audit items.
verbatim: >-
  D6 — the remainder, all nine.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/reactivation-runbook.md (audit items F-17, F-24…F-28, F-33…F-35)
superseded_by: none
source: docs/state.md — "RELEASE SHEET RULED IN FULL 2026-08-05" banner (D6)
unclear: "[UNCLEAR] the source states 'all nine' and lists the finding ids only by range; the individual dispositions are not restated in any of the five sources."
```

```yaml
ruling_id: R-2026-08-05-TIER-M-DRAFT
date: 2026-08-05
scope: A cadence-scaled graduation bar (Tier M) for the mirror class.
verbatim: >-
  One new DRAFT, ruled 2026-08-05 and NOT in force: a cadence-scaled graduation bar (Tier M) for
  the mirror class, drafted as §7a of `docs/mirror-funding-memo-2026-08-05.md`.
  `docs/evidence-standards.md` is UNTOUCHED — and the n>=100 bar remains in force as written. Andy
  signs Tier M separately.
verbatim_of: ruling_text
owner: Andy
status: Gated
applies_to: docs/mirror-funding-memo-2026-08-05.md §7a; the mirror class; docs/evidence-standards.md (untouched)
superseded_by: none
source: docs/state.md — "RELEASE SHEET RULED IN FULL 2026-08-05" banner, closing note
unclear: false
```

```yaml
ruling_id: R-2026-08-05-GATED-BATCH-RELEASE
date: 2026-08-05
scope: Release of the four gated propagation items (S-2 count scoping, D-1 propagation, six research-loop-spec corrections, oa-platform-reference §8.4 step 1).
verbatim: >-
  THE GATED BATCH BELOW WAS RELEASED BY ANDY AND APPLIED, 2026-08-05, SAME DAY. All four items
  authorized in one release; all four applied and device-verified.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/pre-registration-ledger.md §1/§3/§7 and §6; docs/reactivation-runbook.md Step C; docs/research-loop-spec.md (six corrections); docs/oa-platform-reference.md §8.4 step 1
superseded_by: none
source: docs/state.md — "PROPAGATION SWEEP — 2026-08-05", released-gated-batch banner
unclear: false
```

```yaml
ruling_id: R-2026-08-05-S-5-KILL-CRITERION
date: 2026-08-05
scope: The PR-14…PR-17 family-level kill criterion, replaced because it was vacuously unfireable.
verbatim: >-
  The vacuously-unfireable criterion ("more than one differing input") was replaced 2026-08-05
  under row S-5 … now fires on MORE THAN ONE MECHANIC — field granularity, a trigger field plus
  its own pricing sub-field — plus §8.3's assert rules A1/A2/A3/A7/A8.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/pre-registration-ledger.md PR-14…PR-17 entry; docs/greenfield-family-spec.md §8.3, §9
superseded_by: none
source: docs/decision-card-2026-08-06.md §3 (slot 3's device check of the 2026-08-05 S-5 replacement)
unclear: false
```

```yaml
ruling_id: R-2026-08-06-SLOT-01-PROPAGATION-GRANT
date: 2026-08-06
scope: Amend-the-plan grant — propagate the four ruled 08-04 decisions into the six carrier docs.
verbatim: >-
  RULED 2026-08-06: YES, in full (no items struck).
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/oa-platform-reference.md §8.1/§8.2/§7/§10/§4.5; docs/build-plan.md §2D; docs/hedge-research.md §5.2 and §10; docs/oa-ops-runbook.md §3 and §5 trap 6; docs/reactivation-runbook.md §1; docs/state.md (U-4 hash refresh)
superseded_by: none
source: docs/decision-card-2026-08-06.md — RULING SHEET slot 1; docs/state.md "DECISION CARD 2026-08-06" block
unclear: false
```

```yaml
ruling_id: R-2026-08-06-SLOT-01A-RANGE075
date: 2026-08-06
scope: Timing of the build-plan §2D Range075 wording amendment.
verbatim: >-
  1a. build-plan §2D Range075 wording now vs hold: RULED 2026-08-06: APPLY NOW.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/build-plan.md §2D (dated amendment block, original left standing); reopens only if the preset-picker UI check contradicts
superseded_by: none
source: docs/decision-card-2026-08-06.md — RULING SHEET slot 1a
unclear: false
```

```yaml
ruling_id: R-2026-08-06-SLOT-02-LEDGER-COUNT-SCOPING
date: 2026-08-06
scope: Pre-registration-ledger §1/§3/§7 bot-count scoping.
verbatim: >-
  2. Ledger §1/§3/§7 count scoping: RULED 2026-08-06: CONFIRM. (NO ACTION NEEDED)
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/pre-registration-ledger.md §1, §3, §7; docs/track-b-arms-spec.md §11-1f item (iv)
superseded_by: none
source: docs/decision-card-2026-08-06.md — RULING SHEET slot 2
unclear: false
```

```yaml
ruling_id: R-2026-08-06-SLOT-03-PR14-17-KILL-CRITERION
date: 2026-08-06
scope: The PR-14…PR-17 family kill criterion after its 2026-08-05 replacement.
verbatim: >-
  3. PR-14…17 family kill criterion: RULED 2026-08-06: CONFIRM. (NO ACTION NEEDED)
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/pre-registration-ledger.md PR-14…PR-17 entry (DRAFT — UNSIGNED at the time of ruling)
superseded_by: none
source: docs/decision-card-2026-08-06.md — RULING SHEET slot 3
unclear: false
```

```yaml
ruling_id: R-2026-08-06-SLOT-04-GREENFIELD-BUILD
date: 2026-08-06
scope: Authorization of the greenfield build session (7-bot family + shared automations, pre-Day-0, toggles OFF).
verbatim: >-
  RULED 2026-08-06: AUTHORIZE, package items 1-8. Amended, two parts from Andy: (i) the OA build
  itself (Phase 0 probes onward) runs in a SEPARATE session — this session applied doc edits only,
  touched no OA surface, ran no browser tool; (ii) sequencing per slot 7 — C0b look, 2 deletions,
  and the C5 Library delete + exactly-one verify-back run tonight, before Phase A, in that separate
  session.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/greenfield-family-spec.md (Phase 0 -> Phase A -> Phase B); the 7 greenfield arms PR-14…PR-20; underlying QQQ; ride arm = time-exit-only
superseded_by: none
source: docs/decision-card-2026-08-06.md — RULING SHEET slot 4 and §4 package items 1-8
unclear: false
```

```yaml
ruling_id: R-2026-08-06-SLOT-04A-PILOT-CLEAN
date: 2026-08-06
scope: The runbook §3 Step A gate — is the pilot clone declared clean.
verbatim: >-
  RULED 2026-08-06: YES, CLEAN — on the ritual-complete record and the FINISH capture-diff
  no-unintended-edits verdict (reactivation-runbook.md §3 Step A gate).
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/reactivation-runbook.md §3 Step A; docs/pilot-clone-card-qqq-fortress.md; any fresh build
superseded_by: none
source: docs/decision-card-2026-08-06.md — RULING SHEET slot 4a
unclear: false
```

```yaml
ruling_id: R-2026-08-06-SLOT-05-DOUBLE-TESTING
date: 2026-08-06
scope: Double-testing of GF-SL100 / GF-SL200 / ARM-B1 against the signed Track A §3 set.
verbatim: >-
  5. Double-testing: RULED 2026-08-06: RETIRE-SCOPED, package parts 1-4
  (research-loop-spec.md §10a).
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/research-loop-spec.md §10a; docs/greenfield-family-spec.md §9 and §12 row 11; docs/track-b-arms-spec.md §5.5 and §6.3; PR-14…PR-20, PR-21, PR-22 (the no-influence rule applies at signing)
superseded_by: none
source: docs/decision-card-2026-08-06.md — RULING SHEET slot 5; docs/state.md "DECISION CARD 2026-08-06" block
unclear: false
```

```yaml
ruling_id: R-2026-08-06-SLOT-06-REGIME-CHANGE-DEFER
date: 2026-08-06
scope: The regime-change criterion — first ruling of the evening.
verbatim: >-
  RULED 2026-08-06: DEFER W/ TRIGGER as drafted — then SUPERSEDED same session when the card's
  "undefined everywhere" premise was found false (evidence-standards.md §4 gate B3 already defines
  regime change).
verbatim_of: ruling_text
owner: Andy
status: Superseded
applies_to: docs/evidence-standards.md §4; docs/build-plan.md §5; CLAUDE.md §4
superseded_by: R-2026-08-06-SLOT-06-B3-RATIFIED
source: docs/decision-card-2026-08-06.md — RULING SHEET slot 6
unclear: false
```

```yaml
ruling_id: R-2026-08-06-SLOT-06-B3-RATIFIED
date: 2026-08-06
scope: The regime-change conjunct's definition, ruled fresh after the card's premise was falsified.
verbatim: >-
  Andy's fresh ruling, 2026-08-06: RATIFY B3 as the regime-change conjunct's definition for
  `build-plan.md` §5 / `CLAUDE.md` §4's gate — no new definition authored. The deferral trigger
  survives, narrowed to the detector question: B3 must be wired to a `scripts/` detector — or a
  recorded manual-evaluation protocol run at each review date — before the earlier of (i) any
  arm's/variant's first n=60 interim read, or (ii) 2026-11-30. Until then, B3 is evaluated manually
  and every evaluation is logged.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/evidence-standards.md §4 gate B3 (operative gate text); docs/greenfield-family-spec.md §12 row 12; docs/track-b-arms-spec.md §11 item 6; docs/session-log.md (each manual evaluation)
superseded_by: none
source: docs/state.md — "DECISION CARD 2026-08-06" block, slot 6 fresh-ruling banner
unclear: false
```

```yaml
ruling_id: R-2026-08-06-SLOT-07-MECHANICAL-SWEEP
date: 2026-08-06
scope: The tomorrow-morning mechanical sweep.
verbatim: >-
  7. Tomorrow-morning mechanical sweep: RULED 2026-08-06: GO, re-ordered — see slot 4
  amendment (ii).
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: the C0b look; the 2 deletions; the C5 Library delete + verify-back; the three clones and the ~23 manual archives
superseded_by: none
source: docs/decision-card-2026-08-06.md — RULING SHEET slot 7
unclear: false
```

```yaml
ruling_id: R-2026-08-06-C8-SIBLING-CLOSE
date: 2026-08-06
scope: Whether sibling-close is built; the unit for early exits.
verbatim: >-
  RULED (Andy): build without sibling-close; the spread is the unit for early exits.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/greenfield-family-spec.md §4.3; GF-SiblingClose (not built); PR-14's MECHANISM block; the 15:44 constant
superseded_by: none
source: "docs/session-log.md — \"2026-08-06 — part 2: Phase 0 CLOSED\", finding 1; docs/decision-card-2026-08-06.md same-night rulings"
unclear: false
```

```yaml
ruling_id: R-2026-08-06-PR-16-ARMED-TRAIL
date: 2026-08-06
scope: PR-16's trail mechanic after C2 falsified the review's "fix".
verbatim: >-
  RULED (Andy): PR-16 re-scoped to the armed trail, `target`=40 / `trail`=15.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: PR-16 (GF-QQQ-IC-Trail); docs/greenfield-family-spec.md; docs/pre-registration-ledger.md PR-16 entry
superseded_by: none
source: "docs/session-log.md — \"2026-08-06 — part 2: Phase 0 CLOSED\", finding 2; docs/decision-card-2026-08-06.md same-night rulings"
unclear: false
```

```yaml
ruling_id: R-2026-08-06-F-4-SENTINEL-SL1
date: 2026-08-06
scope: The SENTINEL-SL1 stop-loss sentinel value.
verbatim: >-
  F-4 — probe-first, then RULED 2026-08-06 (Andy, final), same night as this card: `SENTINEL-SL1`
  struck as inexpressible; Default Value stays NONE; detection moved to a new config-level assert
  (`greenfield-family-spec.md` §1.3a, §8.3 A9). Closed.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/greenfield-family-spec.md §1.3, §1.3a, §8.3 A9; the seven GF exit presets (Default Value = None)
superseded_by: none
source: docs/decision-card-2026-08-06.md — same-night rulings outside the seven slots
unclear: false
```

```yaml
ruling_id: R-2026-08-06-G-1
date: 2026-08-06
scope: Authorize data/exit_rows.csv, the exit-attribution capture surface.
verbatim: >-
  G-1 exit_rows.csv capture surface — AUTHORIZE, conditional on U-1 positive (Trades list renders
  per-row pricing mode + memo); reverts to HOLD if U-1 negative. Ruled Andy 2026-08-06.
verbatim_of: ruling_text
owner: Andy
status: Gated
applies_to: data/exit_rows.csv (Layer 2); GATE-CM conjunct (c); PR-14 inverted liveness; PR-18/PR-19 stop-row liveness; PR-20's PT-fill detector; PR-22's K2; CF-1's publication precondition
superseded_by: R-2026-08-07-G-1-PRIME
source: docs/g-rulings-card-2026-08-07.md — RULING SHEET group A, G-1; §A1
unclear: "[UNCLEAR] the authorization is conditional and the condition failed — docs/session-log.md 2026-08-07 records U-1 NEGATIVE, so the ruling's own terms revert it to HOLD; the degraded-schema variant was then DECLINED as G-1'. No source states G-1's final status in one place."
```

```yaml
ruling_id: R-2026-08-06-G-2
date: 2026-08-06
scope: The matched-day predicate — M7 or M6.
verbatim: >-
  G-2 Matched-day predicate — M6 — gate reads the six comparative arms; |M7| still printed
  alongside. Ruled Andy 2026-08-06.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/comparative-machinery-spec.md §8; scripts/comparative_machinery.py; the six comparative arms
superseded_by: none
source: docs/g-rulings-card-2026-08-07.md — RULING SHEET group C, G-2
unclear: false
```

```yaml
ruling_id: R-2026-08-06-G-3
date: 2026-08-06
scope: The "exactly one condor per arm per day" reading.
verbatim: >-
  G-3 "exactly one condor per arm per day" — CONFIRM. Ruled Andy 2026-08-06.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/comparative-machinery-spec.md §8; the seven greenfield arms' 2/2 limits
superseded_by: none
source: docs/g-rulings-card-2026-08-07.md — RULING SHEET group C, G-3
unclear: false
```

```yaml
ruling_id: R-2026-08-06-G-4
date: 2026-08-06
scope: The X-1 group reading of refusal R-7 (expired groups).
verbatim: >-
  G-4 X-1 group reading of R-7 — CONFIRM (exclude only all-expired groups). Ruled Andy 2026-08-06.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/comparative-machinery-spec.md §8; scripts/comparative_machinery.py refusal R-7
superseded_by: none
source: docs/g-rulings-card-2026-08-07.md — RULING SHEET group C, G-4
unclear: false
```

```yaml
ruling_id: R-2026-08-06-G-5
date: 2026-08-06
scope: PR-19 / SL200 — GATE-CM conjunct (c).
verbatim: >-
  G-5 PR-19 (SL200): gate conjunct (c) — DISAPPLY — the deliberate parallel to CF-11; with (a)
  inert (G-6), PR-19's gate reduces to conjunct (b) alone — chosen, not arrived at. Ruled Andy
  2026-08-06.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: PR-19 (GF-QQQ-IC-SL200); GATE-CM; docs/greenfield-family-spec.md §9; docs/comparative-machinery-spec.md §2.5
superseded_by: none
source: docs/g-rulings-card-2026-08-07.md — RULING SHEET group A, G-5; §A2
unclear: false
```

```yaml
ruling_id: R-2026-08-06-G-6
date: 2026-08-06
scope: The +0.015R margin read on a fire-rate-diluted mean.
verbatim: >-
  G-6 +0.015R on a fire-rate-diluted mean — STANDS — fire_rate published beside it always;
  currently inert under (b). Ruled Andy 2026-08-06.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/comparative-machinery-spec.md §2.5 conjunct (a); every published deltaR line (fire_rate beside it)
superseded_by: none
source: docs/g-rulings-card-2026-08-07.md — RULING SHEET group C, G-6
unclear: false
```

```yaml
ruling_id: R-2026-08-06-G-7
date: 2026-08-06
scope: Stamping a GATE EVAL DATE for PR-14…PR-20.
verbatim: >-
  G-7 GATE EVAL DATE, PR-14…PR-20 — STAMP = Day-0 + 6 months (relational; resolves to calendar at
  Day-0); interim look at n=60. STAMP. Ruled Andy 2026-08-06.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: PR-14…PR-20 entries; docs/pre-registration-ledger.md §2 template; docs/research-loop-spec.md §10a item 2; resolved to 2027-02-10 at S2 (2026-08-09)
superseded_by: none
source: docs/g-rulings-card-2026-08-07.md — RULING SHEET group A, G-7; §A4
unclear: false
```

```yaml
ruling_id: R-2026-08-06-G-7-TEMPLATE-FIELD
date: 2026-08-06
scope: Whether the GATE EVALUATION DATE field is added to the pre-registration template.
verbatim: >-
  and add the field to pre-registration-ledger.md §2 template? YES. Ruled Andy 2026-08-06.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/pre-registration-ledger.md §2 template; docs/track-b-arms-spec.md §11 item 5
superseded_by: none
source: docs/g-rulings-card-2026-08-07.md — RULING SHEET group A, G-7 sub-item
unclear: false
```

```yaml
ruling_id: R-2026-08-06-G-8
date: 2026-08-06
scope: The n>=60 absolute kill versus the stamped gate.
verbatim: >-
  G-8 n>=60 absolute kill vs the gate — SEQUENCE+CS — n>=60 read emitted as an always-valid
  confidence sequence; absolute kill cannot retire an arm before its stamped gate-eval date. Ruled
  Andy 2026-08-06.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/comparative-machinery-spec.md §8; scripts/comparative_machinery.py; PR-14…PR-20, PR-21, PR-22
superseded_by: none
source: docs/g-rulings-card-2026-08-07.md — RULING SHEET group B, G-8
unclear: false
```

```yaml
ruling_id: R-2026-08-06-G-9
date: 2026-08-06
scope: The BONFERRONI_K value (6, 5, 9 or a census).
verbatim: >-
  G-9 BONFERRONI_K — MOOT under G-10 — max-T needs no hand-set K; the 6-vs-5-vs-9 question
  dissolves. Ruled Andy 2026-08-06.
verbatim_of: ruling_text
owner: Andy
status: Superseded
applies_to: docs/comparative-machinery-spec.md §2.5; the family_census block
superseded_by: R-2026-08-06-G-10
source: docs/g-rulings-card-2026-08-07.md — RULING SHEET group B, G-9; §B3
unclear: false
```

```yaml
ruling_id: R-2026-08-06-G-10
date: 2026-08-06
scope: Replacing Bonferroni-across-6 with a joint day-bootstrap max-T.
verbatim: >-
  G-10 Bonferroni -> joint day-bootstrap max-T? SWITCH — joint day-bootstrap max-T across arms,
  declared before any data exists. Ruled Andy 2026-08-06.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/comparative-machinery-spec.md §2.5 and §8; scripts/comparative_machinery.py; PR-15…PR-19, PR-21, PR-22
superseded_by: none
source: docs/g-rulings-card-2026-08-07.md — RULING SHEET group B, G-10
unclear: false
```

```yaml
ruling_id: R-2026-08-06-G-11
date: 2026-08-06
scope: Whether PR-21/PR-22 sit statistically inside the greenfield family.
verbatim: >-
  G-11 PR-21/PR-22 in the greenfield family? IN — one family, one correction; S-1 governs slots
  only, not error rates. Ruled Andy 2026-08-06.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: PR-21, PR-22 (Track B arms); docs/track-b-arms-spec.md §3.3; the greenfield family correction
superseded_by: none
source: docs/g-rulings-card-2026-08-07.md — RULING SHEET group B, G-11; §B2
unclear: false
```

```yaml
ruling_id: R-2026-08-06-G-12
date: 2026-08-06
scope: PR-16's worst-condor test.
verbatim: >-
  G-12 PR-16 worst-condor test — RESPEC — old wording struck; exact tail-quantile/CI method is a
  follow-up decision, not fabricated here. Ruled Andy 2026-08-06.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: PR-16 (GF-QQQ-IC-Trail); docs/greenfield-family-spec.md §9; docs/pre-registration-ledger.md PR-14…PR-17 entry
superseded_by: none
source: docs/g-rulings-card-2026-08-07.md — RULING SHEET group C, G-12
unclear: "[UNCLEAR] RESPEC strikes the old wording but the replacement method is explicitly left as a follow-up decision; the follow-on signature is R-2026-08-07-G-12B, which the sources do not label as G-12's replacement."
```

```yaml
ruling_id: R-2026-08-06-G-13
date: 2026-08-06
scope: PR-19 / SL200's degeneracy criterion, which could not fire.
verbatim: >-
  G-13 PR-19 (SL200): degeneracy criterion — REPLACE-EQUIV — TOST equivalence test on mean paired
  deltaR vs Ride, band +-0.015R (Andy-signed 2026-08-06 as the R-3 minimum-effect margin),
  evaluated once at the stamped gate-eval date; strikes the 40-day-window rule as unfireable
  (~1.2 expected hits vs 20 required). Ruled Andy 2026-08-06.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: PR-19 (GF-QQQ-IC-SL200); docs/greenfield-family-spec.md §9; docs/research-loop-spec.md §10a item 2
superseded_by: none
source: docs/g-rulings-card-2026-08-07.md — RULING SHEET group A, G-13; §A3
unclear: false
```

```yaml
ruling_id: R-2026-08-06-G-14
date: 2026-08-06
scope: The <D100> calendar / unit / C10 question.
verbatim: >-
  G-14 <D100> calendar / unit / C10 — DEFER-TO-DAY-0. Ruled Andy 2026-08-06.
verbatim_of: ruling_text
owner: Andy
status: Gated
applies_to: docs/comparative-machinery-spec.md §8; C10; Day-0
superseded_by: none
source: docs/g-rulings-card-2026-08-07.md — RULING SHEET group C, G-14
unclear: "[UNCLEAR] the item bundles three questions (calendar, unit, C10) under one DEFER; no source records which of the three was later closed, and C10 is separately recorded OPEN by R-2026-08-08-A-12."
```

```yaml
ruling_id: R-2026-08-06-G-15
date: 2026-08-06
scope: The put-breached / call-not-breached reading.
verbatim: >-
  G-15 put-breached / call-not-breached — PER-SIDE — still gated on G-1 (exit_rows.csv) for a
  fireable input. Ruled Andy 2026-08-06.
verbatim_of: ruling_text
owner: Andy
status: Gated
applies_to: docs/comparative-machinery-spec.md §8; data/exit_rows.csv (Layer 2, on HOLD per G-1 / G-1')
superseded_by: none
source: docs/g-rulings-card-2026-08-07.md — RULING SHEET group C, G-15
unclear: false
```

```yaml
ruling_id: R-2026-08-06-G-16
date: 2026-08-06
scope: The n_matched_days emission floor.
verbatim: >-
  G-16 n_matched_days >= 20 emission floor — Confirm 20. Ruled Andy 2026-08-06.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/comparative-machinery-spec.md §8; scripts/comparative_machinery.py emission floor
superseded_by: none
source: docs/g-rulings-card-2026-08-07.md — RULING SHEET group C, G-16
unclear: false
```

```yaml
ruling_id: R-2026-08-07-LEDGER-START
date: 2026-08-07
scope: When the post-cutover era begins (LEDGER_START).
verbatim: >-
  Andy's ruling (2026-08-07, S0a): the post-cutover era begins at the FIRST DAY A BOT'S
  `AUTOMATIONS` ACTUALLY GOES ON — not at the 2026-08-07 ~12:06 ET payment timestamp. AUTOMATIONS
  is OFF on all 41 bots, verified fleet-wide this session. THAT DATE DOES NOT YET EXIST. The
  `2099-01-01` sentinel is therefore CORRECT and STAYS.
verbatim_of: ruling_text
owner: Andy
status: Superseded
applies_to: scripts/build_ledger.py LEDGER_START; data/ledger_meta.json; docs/reactivation-runbook.md §4 Step 1
superseded_by: R-2026-08-08-A-02
source: docs/session-log.md — 2026-08-07 S0a, "LEDGER_START — RULED, AND DELIBERATELY NOT SET"; docs/state.md S0a/S0b blocks
unclear: false
```

```yaml
ruling_id: R-2026-08-07-F-C1-PT25-REMOVE
date: 2026-08-07
scope: PT25 living on the "Exit-Option-free" controls.
verbatim: >-
  RULED 2026-08-07 (Andy, first-hand): REMOVE. `exits.profits` (`PT25`) comes out of both Open
  Position actions per `build-plan.md` §2B as written; §2B not amended. Originals untouched;
  applies to the PR-01 clone at reactivation and to PR-02 at build.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: PR-01 clone (IC-SPX-FastPT25-S2) and PR-02 (…-130PM), both Open Position actions; docs/reactivation-runbook.md §2 step 7; docs/build-plan.md §2B (not amended)
superseded_by: none
source: docs/session-log.md — 2026-08-07 doc-only session, item 2; finding F-C1
unclear: false
```

```yaml
ruling_id: R-2026-08-07-F-C2-TRAP-10
date: 2026-08-07
scope: A fourth clone trap — disableExits resets 1 -> 0 on clone.
verbatim: >-
  RULED 2026-08-07 (Andy, first-hand): AUTHORIZED AS TRAP 10. `disableExits` resets 1->0 on clone —
  a config-present/toggle-off exit arms itself silently on every clone; check and restore
  immediately after cloning.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/oa-ops-runbook.md §5 Trap 10; every clone operation
superseded_by: none
source: docs/session-log.md — 2026-08-07 doc-only session, item 3; finding F-C2
unclear: false
```

```yaml
ruling_id: R-2026-08-07-G-12B
date: 2026-08-07
scope: PR-16's tail retirement criterion.
verbatim: >-
  G-12b — SIGNED AS DRAFTED. PR-16's (`GF-QQQ-IC-Trail`) tail retirement criterion is signed:
  delta=0.10R, p=0.20, floor n_matched_days>=100 + one re-arm at Day-0+9mo, INSIDE the family
  correction, publication cap acknowledged. Whatever fires still carries
  `CF1_PUBLICATION_PRECONDITION: UNMET` while G-1 is on HOLD.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: PR-16; docs/pre-registration-ledger.md PR-14…PR-17 entry; docs/post-u1-package-2026-08-07.md RULING SLOTS; docs/greenfield-family-spec.md §9 PR-16 entry (struck clause left standing)
superseded_by: none
source: docs/state.md — "RULED 2026-08-07 (Andy) — four open items closed"; docs/session-log.md 2026-08-07 four-slot entry
unclear: false
```

```yaml
ruling_id: R-2026-08-07-G-1-PRIME
date: 2026-08-07
scope: exit_rows.csv under the degraded schema.
verbatim: >-
  G-1' — DECLINED. `exit_rows.csv` under the degraded schema is not authorized; Layer 2 stays
  `BLOCKED`, refusal R-9 stands. Two ~5-minute Day-0 checks kept as ruling-reopeners — D3 (export
  timezone, Step 5a) and the Automation Log link's target for an Exit-Option close (unobserved).
  The CF-1 publication-cap acknowledgment is part of this ruling: no option here makes CF-1's
  precondition meetable.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: data/exit_rows.csv; Layer 2 (BLOCKED, refusal R-9); docs/day0-session-pack-2026-08-07.md S2 close-out item 4; CF-1
superseded_by: none
source: docs/state.md — "RULED 2026-08-07 (Andy) — four open items closed"; docs/session-log.md 2026-08-07 four-slot entry
unclear: false
```

```yaml
ruling_id: R-2026-08-07-M-BOT-CALIBRATION
date: 2026-08-07
scope: Calibration of M_bot_$ (fix-spec OPEN-1 / OPEN-2).
verbatim: >-
  `M_bot_$` calibration — RULED (fix-spec OPEN-1/OPEN-2). ONE-TIME, not rolling; median over
  POSITIONS, computed at the stamp date over the trailing 90 days as of that date; SKIPPED (never a
  zero, never a proxy) before 90 days of history exist.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/research-loop-spec.md §5a item 1; docs/research-loop-fix-spec-2026-08-07.md §10; scripts/research_loop.py (unwired)
superseded_by: none
source: docs/state.md — "RULED 2026-08-07 (Andy) — four open items closed"
unclear: false
```

```yaml
ruling_id: R-2026-08-07-PT-FAMILY-REPORTING
date: 2026-08-07
scope: How the PT family is reported (fix-spec OPEN-3).
verbatim: >-
  PT family — RULED (fix-spec OPEN-3). REPORTED WITH MANDATORY SPLIT: every PT line prints its
  decidable/undecidable position counts and `single_sided` share. Descriptive only — no graduation
  read is taken from a Track A PT line. The live test of the PT mechanic is the greenfield PT50 arm
  (PR-15), judged on its own matched-day family under G-10, not against this bucket.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/research-loop-fix-spec-2026-08-07.md §10; every Track A PT line; PR-15 (GF-QQQ-IC-PT50)
superseded_by: none
source: docs/state.md — "RULED 2026-08-07 (Andy) — four open items closed"
unclear: false
```

```yaml
ruling_id: R-2026-08-07-E-1-LAB-SLOTS
date: 2026-08-07
scope: Slot budget for exploratory/Lab ops bots.
verbatim: >-
  E-1 (SLOT A, slot budget) — RULED & APPLIED. Third named allocation, `<=2 Lab ops slots`,
  separate from plan bots and Track B. Ceiling 28 -> 30. Wave 1 becomes 24 of 50; full spend 30 of
  50.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/build-plan.md §2D (AMENDMENT 2026-08-07); docs/pre-registration-ledger.md §1/§3/§7; docs/exploratory-bots-design-2026-08-07.md §3
superseded_by: none
source: docs/state.md — "E-1 / E-2 / E-3 APPLIED — 2026-08-07"
unclear: false
```

```yaml
ruling_id: R-2026-08-07-E-2-OPS-PREREGISTRATION
date: 2026-08-07
scope: Pre-registration for the ops/Lab class.
verbatim: >-
  E-2 (SLOT B, pre-registration) — RULED & APPLIED. `pre-registration-ledger.md` gains new §2a
  (ops-class template … plus a new `PHASE LOG` field) and guardrails G1-G10 (publication interdict,
  never an arm/control, no shared Library object, paper only, etc.), a new §3 roster row (Group E,
  <=2, entries at new placeholder §6a — no bot named yet), and the ceiling propagated to §1/§3/§7.
  No entry, no restart applies to this class exactly as to every other.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/pre-registration-ledger.md §2a, §3 (Group E), §6a; every Lab/ops bot
superseded_by: none
source: docs/state.md — "E-1 / E-2 / E-3 APPLIED — 2026-08-07"
unclear: false
```

```yaml
ruling_id: R-2026-08-07-E-3-LEDGER-EXCLUSION
date: 2026-08-07
scope: Ledger contamination by ops/Lab bots — the hard precondition.
verbatim: >-
  E-3 (SLOT C, ledger contamination) — RULED … the HARD PRECONDITION: `build_ledger.py` exclusion +
  `a_series` scoping (`_a4b`/`_a6`) + Lab group/tag fencing, all implemented and verified, before
  any Lab bot's `AUTOMATIONS` goes ON. No exception, no partial credit.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: scripts/build_ledger.py; scripts/a_series.py (_a4b/_a6); Lab group/tag fencing; docs/exploratory-bots-design-2026-08-07.md §3.3
superseded_by: none
source: docs/state.md — "E-1 / E-2 / E-3 APPLIED — 2026-08-07" (implemented and verified 2026-08-08)
unclear: false
```

```yaml
ruling_id: R-2026-08-07-A7-DRIFT-1
date: 2026-08-07
scope: ScannerA's stale recorded A7 baseline.
verbatim: >-
  Ruling: ADOPT the new ScannerA baseline. … Cause, as ruled: own-session materialization of the
  F-4 `Default Value = None` setting on input `IN178605447966781`; tree and Open-Position payload
  diffed unchanged. A7 detected it as designed — that is the mechanism passing, not failing.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: data/bots_config_v2.csv (GF-ScannerA-PutSpread row, version 9, a7_hash 3308ce8b…); data/captures/2026-08-06-gfam/GF-ScannerA-PutSpread.txt; docs/state.md
superseded_by: none
source: docs/session-log.md — 2026-08-07 six-arm session, item 1; 2026-08-07 housekeeping entry (assigned to the arms-build session)
unclear: false
```

```yaml
ruling_id: R-2026-08-07-A2-EXITRATE-1
date: 2026-08-07
scope: The absent exitrate field on GF-QQQ-IC-Ride (assert A2).
verbatim: >-
  RULING 1 — A2-EXITRATE-1: TAKE THE CLICK. Applied. A2 = PASS 7/7. `exitrate` is now STORED = 1 on
  `GF-QQQ-IC-Ride`, verified after a hard reload.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: GF-QQQ-IC-Ride (exitrate = 1); data/captures/2026-08-07-greenfield/GF-QQQ-IC-Ride/GF-QQQ-IC-Ride.txt; data/bots_config_v2.csv (banner + schema note)
superseded_by: none
source: docs/session-log.md — "2026-08-07 (rulings)", RULING 1
unclear: false
```

```yaml
ruling_id: R-2026-08-07-A1-SPEC-1
date: 2026-08-07
scope: Assert A1's expected mechanic-difference count (arm-vs-control vs arm-vs-arm).
verbatim: >-
  RULING 2 — A1-SPEC-1: AMEND. Applied to `greenfield-family-spec.md` §8.3. A1 = PASS 21/21.
  Amended text: pair type decides the expected count. (a) arm-vs-CONTROL -> differ in exactly ONE
  mechanic. (b) arm-vs-arm -> differ in exactly TWO, and those two must be precisely each arm's own
  declared mechanic, with nothing else differing. Two arms sharing a mechanic FIELD at different
  VALUES differ in exactly ONE and are checked under (a).
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/greenfield-family-spec.md §8.3 assert A1; scripts/a_series.py; the 21 arm pairs
superseded_by: none
source: docs/session-log.md — "2026-08-07 (rulings)", RULING 2
unclear: false
```

```yaml
ruling_id: R-2026-08-07-GF-EXIT-OPTIONS-RESTORE
date: 2026-08-07
scope: EXIT OPTIONS reading OFF on all seven GF bots after the OA restore.
verbatim: >-
  Andy's ruling: expected — OA resets Exit Options OFF on restore; not a config loss. Flip it back
  to ON for all seven and re-verify.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: GF-QQQ-IC-Ride, -PT50, -Trail, -Touch0, -SL100, -SL200, -Canary (disableExits 0); data/bots_config_v2.csv
superseded_by: none
source: docs/session-log.md — 2026-08-07 S0b-RESUME, "NEW FINDING, ESCALATED, RULED BY ANDY, FIXED AND VERIFIED"
unclear: false
```

```yaml
ruling_id: R-2026-08-07-PR-05-PR-06-GATE-EVAL-DATE
date: 2026-08-07
scope: GATE EVAL DATE for PR-05 / PR-06.
verbatim: >-
  `pre-registration-ledger.md` — PR-05/PR-06 `GATE EVAL DATE` stamped (open item 7; Andy's ruling:
  stamp both). Both now carry the field, dated 2026-08-07, marked a standalone R kill (Exp(R) <
  -0.10, n>=50) — not a comparative gate under `research-loop-spec.md` §10a, so no interim look at
  n=60 applies.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/pre-registration-ledger.md PR-05 and PR-06 entries
superseded_by: none
source: "docs/session-log.md — \"2026-08-07 — Housekeeping: five doc corrections (Andy's ruling)\", item 1"
unclear: false
```

```yaml
ruling_id: R-2026-08-07-IC-GROUPS-BOTH-STAY
date: 2026-08-07
scope: Whether the IC and IC-Focus bot groups both stay.
verbatim: >-
  `IC`/`IC-Focus` — both groups stay; correcting the stale runbook §3 line is this session's
  item 3.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: OA bot groups IC and IC-Focus; docs/oa-ops-runbook.md §3 (dated correction banner)
superseded_by: none
source: "docs/session-log.md — \"2026-08-07 — Housekeeping: five doc corrections (Andy's ruling)\""
unclear: false
```

```yaml
ruling_id: R-2026-08-07-R-06-NARROWED
date: 2026-08-07
scope: The reconciliation report's R-06 retag request on the Exit Options start time.
verbatim: >-
  Andy ruled "YES as narrowed". … It is settled for this account: §4.1's first-hand DOM read has
  `exitstart` = `09:31` … Applied as a docs-defect note, not an open question.
verbatim_of: andy
owner: Andy
status: Active
applies_to: docs/oa-platform-reference.md §4.1 / §6.1a; docs/oa-reconciliation-report.md R-06
superseded_by: none
source: docs/session-log.md — 2026-08-07 package session, item 3 (R-06)
unclear: false
```

```yaml
ruling_id: R-2026-08-08-A-02
date: 2026-08-08
scope: LEDGER_START semantics — which day the post-cutover era begins.
verbatim: >-
  "We are turning them on today or tomorrrow to start recofrding data starting monday open. so Aug
  10 should be day=o" — THE RULING: `LEDGER_START` = `2026-08-10`. The post-cutover era begins at
  Monday 2026-08-10's open — the first market session on or after switch-on. Not the 2026-08-07
  payment timestamp, and not a non-trading day on which a toggle happens to be flipped.
  Slip condition — FIXED DATE: `LEDGER_START` stays `2026-08-10` even if switch-on slips past
  Monday's open.
verbatim_of: andy
owner: Andy
status: Active
applies_to: scripts/build_ledger.py (line 108, set at Day-0); docs/build-plan.md §1 and §3 (CA-1, amend-the-plan); docs/state.md S0a/S0b blocks; docs/reactivation-runbook.md §4 Step 1
superseded_by: none
source: docs/decision-card-2026-08-08.md — SLOT 1 (RULINGS section)
unclear: false
```

```yaml
ruling_id: R-2026-08-08-A-11
date: 2026-08-08
scope: The first-position control — what caps a bot at one position for Step 6.
verbatim: >-
  THE RULING: A THEN B, WITH 2a = NO. 1. Attempt the button test-fire first, one bot, record
  verbatim whether the control exists. 2. If it does not exist, `posLimitDay` = 1 is AUTHORIZED
  (and `posLimit` = 1 where separately settable): one bot at a time, never a batch; screenshot
  before and after; read the Trades list the moment the position opens; revert immediately after
  the read. 3. 2a = NO — a temporary limit does not fork the Step-2b signature. … the revert is
  PROVEN, not asserted. 5. Option C DECLINED. Option D is the per-bot fallback.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/day0-session-pack-2026-08-07.md §0.0 A-11 and S2 Step 6; docs/reactivation-runbook.md §4 Step 6; each bot's pre-registration entry
superseded_by: none
source: docs/decision-card-2026-08-08.md — SLOT 2 (RULINGS section)
unclear: "[UNCLEAR] R-2026-08-09-S2-R5 finds posLimitDay=1 would break the condor on the seven arms and rules they stay 2/2, and docs/state.md records 'the ruled limits ARE the first-position control'; no source states whether A-11 limb 2 is thereby retired or merely unused."
```

```yaml
ruling_id: R-2026-08-08-A-12
date: 2026-08-08
scope: The C10 dstop instrument for Day-0.
verbatim: >-
  "C for Day-0, A as the queued path" — THE RULING. C10 STAYS OPEN for Day-0. No instrument runs it
  on the day. PR-20 is not edited (A-12(a)) and candidate B, the pilot, is DECLINED. … The queued
  path is `TESTOPS-LAB-DSTOP` … This ruling does NOT authorize building it. ARM-B1 stays blocked and
  PR-21 stays unstamped.
verbatim_of: andy
owner: Andy
status: Active
applies_to: C10 (open); PR-20 (not edited); TESTOPS-LAB-DSTOP (queued, gated on E-3 verified + signed PHASE LOG + a Lab slot); ARM-B1; PR-21; docs/day0-session-pack-2026-08-07.md; docs/state.md
superseded_by: none
source: docs/decision-card-2026-08-08.md — SLOT 3 (RULINGS section)
unclear: false
```

```yaml
ruling_id: R-2026-08-08-A-24-I
date: 2026-08-08
scope: Template V2 on the pilot at S2 Step 0.
verbatim: >-
  (i) Template V2 on the pilot — NOT finished at Step 0; THE PILOT STAYS OFF. Finishing V2 is a
  spec change plus a signature … V2 lands in a build window with its amended PR-03. The 15:50 exit
  is not re-priced on Day-0.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: the pilot clone (stays OFF); Template V2; PR-03 (amended pre-registration); docs/day0-session-pack-2026-08-07.md S2 Step 0
superseded_by: none
source: docs/decision-card-2026-08-08.md — SLOT 4 (i)
unclear: false
```

```yaml
ruling_id: R-2026-08-08-A-24-II
date: 2026-08-08
scope: C9 at S2 Step 0.
verbatim: >-
  (ii) C9 — RUN AS A READ AT STEP 0. The family does not stay off. Read only, never a write, never
  an improvised spec.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: C9; the seven greenfield arms; docs/day0-session-pack-2026-08-07.md S2 Step 0
superseded_by: none
source: docs/decision-card-2026-08-08.md — SLOT 4 (ii)
unclear: false
```

```yaml
ruling_id: R-2026-08-08-A-24-III
date: 2026-08-08
scope: A7 not being wired into daily.sh.
verbatim: >-
  (iii) A7 unwired — THE FAMILY TRADES, with a hand-run detector. `scripts/a_series.py --validate`
  and `--json`, by hand, at every close-out, from Day-0 on. … The 4th object,
  `Defang-Mon-S2-StrikeTouch` (A-13), is named as an open gap at every close-out — its 2026-08-08
  sweep entry is a FIRST BASELINE, not a pass, so A7 reports 3/4 VERIFIED + 1 FIRST BASELINE, never
  4/4. Wiring into `daily.sh` stays a queued Claude Code task, not a Day-0 action.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: scripts/a_series.py (hand-run at every close-out); scripts/daily.sh (wiring queued); Defang-Mon-S2-StrikeTouch (A-13)
superseded_by: none
source: docs/decision-card-2026-08-08.md — SLOT 4 (iii)
unclear: false
```

```yaml
ruling_id: R-2026-08-08-A-24-IV-GATE-A9
date: 2026-08-08
scope: Gate A9 — Andy's own clean end-to-end daily.sh n=0 run.
verbatim: >-
  (iv) Gate A9 — CONFIRMED as a rule, and ALREADY SATISFIED. §4 does not start until Andy's own
  clean end-to-end `daily.sh` n=0 run is on file, and a session's report of its own run is not that
  check. It is on file — gate A9 CLOSED 2026-08-08 on Andy's own 8/8 run. The box is TICKED. Split
  (ii), the Tier-C contract reconciliation, stays open and does not gate Day-0.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: gate A9 (CLOSED); scripts/daily.sh; scripts/execution_audit.py v1.1.0; scripts/daily_brief.py; Tier C (SKIPPED BY NAME, split (ii) open)
superseded_by: none
source: docs/decision-card-2026-08-08.md — SLOT 4 (iv)
unclear: false
```

```yaml
ruling_id: R-2026-08-08-GATE-A8-PR-18-NAME
date: 2026-08-08
scope: PR-18's name — "Breakeven" versus the mechanical SL100 label.
verbatim: >-
  "Card's RECOMMENDATION: C" — THE RULING — OPTION C, THE SPLIT. "Breakeven" is the LEDGER /
  INTERNAL label for PR-18. … The MECHANICAL name — `SL100` / "stop at 100% of credit" — is used in
  anything PUBLISHED or COMPARED EXTERNALLY, and the CF-1 caveat is attached at that surface. …
  The OA bot name `GF-QQQ-IC-SL100` is unchanged — nothing renames anywhere. PR-19 (`SL200`)
  follows the same convention by construction.
verbatim_of: andy
owner: Andy
status: Active
applies_to: PR-18 (GF-QQQ-IC-SL100) and PR-19 (SL200); docs/greenfield-family-spec.md PR-18 naming block; docs/pre-registration-ledger.md NAMING field; docs/day0-session-pack-2026-08-07.md; docs/state.md CF-4 bullet
superseded_by: none
source: docs/decision-card-2026-08-08.md — SLOT 5 (RULINGS section); gate A8 CLOSED IN FULL
unclear: false
```

```yaml
ruling_id: R-2026-08-08-GATE-A8-5A-CF-4
date: 2026-08-08
scope: Correcting state.md's CF-4 bullet to match the PR-18 naming ruling.
verbatim: >-
  "YES and for the remainging items, lets go with your suggestions" — 5a / CA-2 — RULED YES.
  `state.md`'s CF-4 bullet carried the pre-discharge finding as a live fact. Corrected: original
  left standing, dated banner records CF-4's 2026-08-06 discharge and this ruling. The old
  instruction "do not publish it under the anchor's name" survives for publication and is
  superseded for the ledger — it was incomplete, not wrong.
verbatim_of: andy
owner: Andy
status: Active
applies_to: docs/state.md CF-4 bullet; PR-18's publication surfaces
superseded_by: none
source: docs/decision-card-2026-08-08.md — SLOT 5, sub-choice 5a
unclear: false
```

```yaml
ruling_id: R-2026-08-08-A-27C
date: 2026-08-08
scope: Step-4b's config-capture precondition (A-07's ESTABLISHED-hash scope).
verbatim: >-
  THE RULING — OPTION 2, AMEND A-07's SCOPE. An ESTABLISHED config-capture hash is required only
  where a pre-restore baseline exists. The bots without one are carried explicitly NOT EVALUABLE,
  not as blockers … Riders, all applied: 1. In the field, never a footnote … 2. A capture is taken
  on the first day each bot trades … This is a worklist, not a precondition on S2.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/pre-registration-ledger.md CONFIG HASH fields on PR-05…PR-13 (nine); docs/day0-session-pack-2026-08-07.md §0.0 A-27(c) and the S2 opening precondition
superseded_by: none
source: docs/decision-card-2026-08-08.md — SLOT 6 (RULINGS section)
unclear: false
```

```yaml
ruling_id: R-2026-08-08-A-27C-6A-PURE-READ
date: 2026-08-08
scope: Whether opening one of the nine leave-in-place bots for a capture spends Step 2c.
verbatim: >-
  6a — PURE READ, ruled explicitly. Opening any of the nine for a capture does not spend Step 2c …
  Pure read means read — no edit, no toggle, no rename, no save, no archive, no template. S0b's
  narrower "do not touch… in any way" is superseded for reads only.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: the nine leave-in-place bots; Step 2c; gate A0 Branch 1 (A-09b)
superseded_by: none
source: docs/decision-card-2026-08-08.md — SLOT 6, sub-item 6a
unclear: false
```

```yaml
ruling_id: R-2026-08-08-A-27C-6B-GROUP-A
date: 2026-08-08
scope: The 20 Group-A bots' absence from any post-restore config check.
verbatim: >-
  6b — ACCEPT AND RECORD. The 20 Group-A bots are in no post-restore config check anywhere; that
  is now written down. Not brought into scope, not archived by this ruling; still covered by the
  ~23 archives queued for Andy's hand.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: the 20 Group-A bots; the ~23 queued archives
superseded_by: none
source: docs/decision-card-2026-08-08.md — SLOT 6, sub-item 6b
unclear: false
```

```yaml
ruling_id: R-2026-08-08-PR02-R2
date: 2026-08-08
scope: The pack's "the Symbols panel is NOT empty" checklist line.
verbatim: >-
  THE RULING — option (a): APPLY AS AN EVIDENCE-BACKED CORRECTION … The check is NOT skipped — it
  is BRANCHED. Bot-Symbols-loop bot -> the panel must be non-empty and match
  character-for-character … Automation-resident-symbol bot (`Loop <SYM>` + action `symbol: <SYM>`)
  -> "No symbols yet" is the correct and expected state on both sides … Do not "restore" symbols
  into such a bot's panel — that is an unrequested config change.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/day0-session-pack-2026-08-07.md §S1 step 4; docs/reactivation-runbook.md §2 step 3 and the WHAT-"CLEAN"-MEANS block (routed to slot 8); PR-01 and PR-02
superseded_by: none
source: docs/decision-card-2026-08-08.md — SLOT 7 (RULINGS section)
unclear: false
```

```yaml
ruling_id: R-2026-08-08-SLOT-08-DOC-BATCH
date: 2026-08-08
scope: The five-item doc-correction batch (an explicit "amend the plan" for the runbook items).
verbatim: >-
  RULED 2026-08-08. AMEND ALL FIVE. (1) PR02-R3 / A-16b — the pre-F-C1 "do not remove PT25
  yourself · bot stays OFF" branch is struck and replaced: F-C1 is RULED: REMOVE … (2) PR04-R1 —
  "hash all four of its automations" is a PR-02 inheritance, not a constant … (3) FS-3 — The
  Automation Library is at `/bots/automations` … (4) from slot 1 — "This date is `LEDGER_START`"
  struck … (5) from slots 2 and 7 — Step 6's first-position exception now names its control …
  Both symbols echoes branched rather than deleted.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/reactivation-runbook.md (§2 step 3, §2 step 7, §4 Step 1, §4 Step 6, WHAT-"CLEAN"-MEANS); docs/day0-session-pack-2026-08-07.md §S1 steps 0 and 7; docs/state.md PR04-R2 note; docs/oa-ops-runbook.md §5 trap 1
superseded_by: none
source: docs/decision-card-2026-08-08.md — SLOT 8 (RULINGS section)
unclear: false
```

```yaml
ruling_id: R-2026-08-08-OPS-TRADE-ID
date: 2026-08-08
scope: The ops trade_id namespace in data/ops_rows.csv.
verbatim: >-
  THE RULING — (c) DEFER, WITH (a) PRE-REGISTERED AS THE SCHEME. `trade_id` stays blank in
  `data/ops_rows.csv`. … The scheme, on the record before any row exists: when the first Lab bot is
  built, `ops_rows.csv` rows carry `OPS-<bot>-<date>-<n>` … REOPEN CONDITION: the first Lab bot's
  build. … E-3 §3.3 item 8 … stays NOT USABLE until ids exist.
verbatim_of: ruling_text
owner: Andy
status: Gated
applies_to: data/ops_rows.csv (trade_id stays empty); docs/exploratory-bots-design-2026-08-07.md §3.3; docs/state.md three-gated-items paragraph
superseded_by: none
source: docs/decision-card-2026-08-08.md — SLOT 9 (RULINGS section)
unclear: false
```

```yaml
ruling_id: R-2026-08-08-DA-3
date: 2026-08-08
scope: The retired >=15-condor go-live bar still printing on the reporting surfaces.
verbatim: >-
  THE RULING — YES, RETIRED IN PRINT. … The line is DROPPED from both surfaces. G2's >=20 is the
  only go-live bar. Rider: do NOT replace it with a ">=20" line. … ACCEPTANCE CRITERIA:
  `grep -c "Go-live gate" scripts/report.py` = 0, and the next generated `STATUS.md` contains no
  `Go-live gate` line.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: scripts/report.py (line 141, queued Claude Code task); STATUS.md (generated); docs/evidence-standards.md §5
superseded_by: none
source: docs/decision-card-2026-08-08.md — SLOT 10 (RULINGS section); applied 2026-08-09 per docs/session-log.md orchestrator entry
unclear: false
```

```yaml
ruling_id: R-2026-08-08-PR02-R1-ALLOCATION
date: 2026-08-08
scope: PR-02's allocation.
verbatim: >-
  PR02-R1 RULED — 2026-08-08, by Andy (orchestrator chat): ALLOCATION $50,000 STANDS. Zero OA edit.
  The clone keeps $50,000 as found.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: PR-02 (IC-SPX-FastPT25-S2-130PM); docs/pre-registration-ledger.md §4 PR-02; rename_map.csv row 4
superseded_by: none
source: docs/session-log.md — "PR02-R1 RULED — 2026-08-08"; docs/state.md 2026-08-08 evening block
unclear: false
```

```yaml
ruling_id: R-2026-08-08-E-3-ITEM-1-ADDITIVE
date: 2026-08-08
scope: The E-3 §3.3 receipt clause.
verbatim: >-
  (1) "ADDITIVE OK" — the §3.3 receipt clause is read as: pre-existing `ledger_meta.json` keys
  byte-identical (verified by Worker B, every key), NEW keys permitted for items 2/4. The
  contradiction in the ruled text is resolved additively; 4 additions / 0 changed values stands as
  built.
verbatim_of: andy
owner: Andy
status: Active
applies_to: docs/exploratory-bots-design-2026-08-07.md §3.3; data/ledger_meta.json
superseded_by: none
source: docs/session-log.md — "E-3 GATED ITEMS (1)+(3) RULED — 2026-08-08"
unclear: false
```

```yaml
ruling_id: R-2026-08-08-E-3-ITEM-3-FIX-O4
date: 2026-08-08
scope: The pre-existing _a4b blind-detector defect (self-test O4).
verbatim: >-
  (3) "FIX O4" — the pre-existing `_a4b` blind-detector defect (timedelta<=int, TypeError
  swallowed) is authorized for repair by the orchestrator session, mechanical scope only: correct
  the comparison, make the failure path loud, flip self-test O4 from defect-recording to firing,
  `--validate` must remain reproduction-exact.
verbatim_of: andy
owner: Andy
status: Active
applies_to: scripts/a_series.py::_a4b; self-test O4
superseded_by: none
source: docs/session-log.md — "E-3 GATED ITEMS (1)+(3) RULED — 2026-08-08"; "O4 FIXED — 2026-08-08"
unclear: false
```

```yaml
ruling_id: R-2026-08-08-BASELINE-ADDENDUM-OPTION-B
date: 2026-08-08
scope: How the QQQ-IC-0DTE-Baseline forensic carries its Monday-tracking material.
verbatim: >-
  Andy ruled (orchestrator chat): option B — a short Monday-tracking addendum appended to the
  existing file under a dated banner, not a new forensic. … Gates nothing, amends nothing.
  `data/lessons.csv` NOT written.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: docs/baseline-forensic-2026-08-07.md §A.1-A.6; data/lessons.csv (not written)
superseded_by: none
source: "docs/session-log.md — \"2026-08-08 — QQQ-IC-0DTE-Baseline forensic: REPLICATED, NOT REWRITTEN\""
unclear: false
```

```yaml
ruling_id: R-2026-08-09-S2-GATE-A6-RIDE
date: 2026-08-09
scope: Gate A6 — disposition of the five open mirror positions.
verbatim: >-
  Gate A6 — "Ride: leave both bots' EXIT OPTIONS OFF". RIDE on all five. `QQQ long call` and `Tasty
  Condor` excluded from Step 3, unsigned, OFF. Cost accepted and named: Step 6a can now reach at
  most 7 of the 9 subjects.
verbatim_of: andy
owner: Andy
status: Active
applies_to: the five open mirror positions; QQQ long call and Tasty Condor (EXIT OPTIONS OFF, PR-09 and PR-13 UNSIGNED); docs/pre-registration-ledger.md §5a PR-RC-01
superseded_by: none
source: docs/session-log.md — 2026-08-09 S2, "ANDY'S SIX RULINGS", 1; docs/state.md S2 block
unclear: false
```

```yaml
ruling_id: R-2026-08-09-S2-STEP-6-7-ORDERING
date: 2026-08-09
scope: Step 6/7 ordering on a closed market.
verbatim: >-
  Step 6/7 ordering — "Switch on today at Step 7 with posLimitDay=1", treating the closed market as
  "test-fire cannot execute".
verbatim_of: andy
owner: Andy
status: Superseded
applies_to: the seven greenfield arms at Step 7; docs/reactivation-runbook.md §4 Steps 6 and 7
superseded_by: R-2026-08-09-S2-R5-LIMITS
source: docs/session-log.md — 2026-08-09 S2, "ANDY'S SIX RULINGS", 2
unclear: false
```

```yaml
ruling_id: R-2026-08-09-S2-SIGN-THE-SEVEN
date: 2026-08-09
scope: Which of the nine leave-in-place bots get signed.
verbatim: >-
  The nine — "Sign the seven that can trade (ledger reading)", following the ledger's own CONFIG
  HASH text ("does NOT block this signature") over the prompt's stricter line.
verbatim_of: andy
owner: Andy
status: Active
applies_to: PR-01, PR-05, PR-06, PR-07, PR-08, PR-10, PR-11, PR-12 signed; PR-09 and PR-13 NOT SIGNED
superseded_by: none
source: docs/session-log.md — 2026-08-09 S2, "ANDY'S SIX RULINGS", 3
unclear: false
```

```yaml
ruling_id: R-2026-08-09-S2-CONFIG-HASH-CONVENTION
date: 2026-08-09
scope: What the CONFIG HASH field records.
verbatim: >-
  CONFIG HASH convention — "Both: capture path @ file sha256, plus the three A7 hashes".
verbatim_of: andy
owner: Andy
status: Active
applies_to: docs/pre-registration-ledger.md CONFIG HASH on the seven arms and PR-01; docs/greenfield-family-spec.md §9
superseded_by: none
source: docs/session-log.md — 2026-08-09 S2, "ANDY'S SIX RULINGS", 4
unclear: false
```

```yaml
ruling_id: R-2026-08-09-S2-ENTRY-FIELDS-AMEND
date: 2026-08-09
scope: The three Step-2b entry-field classes.
verbatim: >-
  Entry fields — "Amend the plan: resolve all three classes" (CONFIG HASH · the relational dates ·
  PR-14's MECHANISM).
verbatim_of: andy
owner: Andy
status: Active
applies_to: docs/greenfield-family-spec.md §9 (GATE EVAL DATE 2027-02-10 on all seven; REVIEW DATE PR-14 2027-02-10, PR-20 2026-11-10); PR-14's MECHANISM block (corrected in place)
superseded_by: none
source: docs/session-log.md — 2026-08-09 S2, "ANDY'S SIX RULINGS", 5; docs/state.md S2 block
unclear: false
```

```yaml
ruling_id: R-2026-08-09-S2-GATE-A7-SIGN-ALL-SEVEN
date: 2026-08-09
scope: Gate A7 — signing the seven greenfield arms and PR-01.
verbatim: >-
  Gate A7 — "Sign all seven" (PR-14…PR-20) and "Fill its CONFIG HASH and sign it" (PR-01).
verbatim_of: andy
owner: Andy
status: Active
applies_to: PR-14…PR-20 and PR-01 (signed, each carrying SIGNED != VERIFIED and the owed first-trading-day capture)
superseded_by: none
source: docs/session-log.md — 2026-08-09 S2, "ANDY'S SIX RULINGS", 6
unclear: false
```

```yaml
ruling_id: R-2026-08-09-S2-R5-LIMITS
date: 2026-08-09
scope: Position limits after posLimitDay=1 was found to break the condor.
verbatim: >-
  S2-R5 — "Condor-aware: arms stay 2/2, PR-01 -> 2/2, mirrors -> 1/1". Arms untouched — no edit, no
  hash fork, nothing to revert.
verbatim_of: andy
owner: Andy
status: Active
applies_to: the seven GF arms (2/2); PR-01 (10/10 -> 2/2); the mirrors (1/1); docs/reactivation-runbook.md §3 Step A criterion 4
superseded_by: none
source: docs/session-log.md — 2026-08-09 S2, "ANDY'S SIX RULINGS", 6 (S2-R5); docs/state.md S2 findings table
unclear: false
```

```yaml
ruling_id: R-2026-08-09-S2-R3-RECORDED-NOTE-LEN
date: 2026-08-09
scope: The a_series.py --validate 1-divergence spot check caused by the Day-0 signing edits.
verbatim: >-
  S2-R3 was in fact RULED BY ANDY — OPTION A — in the orchestrator chat BEFORE S2b opened, and
  applied there: `scripts/a_series.py` `RECORDED_NOTE_LEN` re-baselined to the signed §9 lengths
  (build-time values kept in a dated comment) … `--validate` = REPRODUCED THE REFERENCE EXACTLY,
  `--json` clean. S2-R3 is CLOSED.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: scripts/a_series.py RECORDED_NOTE_LEN; the seven signed bots' Notes (NOT rewritten — S0b-2 stands)
superseded_by: none
source: docs/state.md — 2026-08-09 S2b block, "CORRECTED 2026-08-09" banner; docs/session-log.md 2026-08-09 orchestrator entry
unclear: "[UNCLEAR] the S2b worker's own record says S2-R3 was DEFERRED by Andy at S2b and the orchestrator banner says it was ruled OPTION A before S2b opened; the sources keep both, attributing the conflict to a prompt gap."
```

```yaml
ruling_id: R-2026-08-09-S2B-PR02-PR04-LIMITS
date: 2026-08-09
scope: Position limits for PR-02 and PR-04, which S2-R5 never named.
verbatim: >-
  PR-02 / PR-04 position limits — S2-R5 never named them. Gated. "2 per day / 2 at once", the
  condor-aware reading, identical to PR-01 and the seven arms.
verbatim_of: andy
owner: Andy
status: Active
applies_to: PR-02 (10/10 -> 2/2); PR-04 (already stored 2/2, recorded and skipped)
superseded_by: none
source: docs/session-log.md — 2026-08-09 S2b, "ANDY'S FIVE RULINGS", 1
unclear: false
```

```yaml
ruling_id: R-2026-08-09-S2B-R3-ARM-THEN-ON
date: 2026-08-09
scope: PR-04's EXIT OPTIONS reading OFF before switch-on.
verbatim: >-
  S2b-R3 — "Arm EXIT OPTIONS, then switch ON" for PR-04; then the self-challenge above; then
  "Go — flip AUTOMATIONS ON" once the empty `profits` was proven.
verbatim_of: andy
owner: Andy
status: Active
applies_to: PR-04 (QQQ-IC-0DTE-Fortress-NoPT50) — ARMED + ON; its two Open Position actions (profits "" both sides, expdays 0.01 the only live rung)
superseded_by: none
source: docs/session-log.md — 2026-08-09 S2b, "ANDY'S FIVE RULINGS", 2; docs/state.md S2b findings table
unclear: false
```

```yaml
ruling_id: R-2026-08-09-S2B-R4-RECORD-ONLY
date: 2026-08-09
scope: The "15:50 exit" label versus the stored expdays = 0.01.
verbatim: >-
  S2b-R4 — "Record only, correct after Monday." No doc edit made … Monday check owed: record the
  OBSERVED close time and reconcile it against `expdays 0.01` and the label.
verbatim_of: andy
owner: Andy
status: Active
applies_to: PR-04's two scanners (expdays 0.01); the "15:50 exit" label on at least three folder surfaces
superseded_by: none
source: docs/session-log.md — 2026-08-09 S2b, "ANDY'S FIVE RULINGS", 3; docs/state.md S2b findings table
unclear: false
```

```yaml
ruling_id: R-2026-08-09-S2B-GATE-A12
date: 2026-08-09
scope: Gate A12 — the bots_config_v2.csv roster capture sweep.
verbatim: >-
  Gate A12 / `bots_config_v2.csv` — "comment banner today, sweep at your convenience."
verbatim_of: andy
owner: Andy
status: Active
applies_to: data/bots_config_v2.csv (dated staleness banner, comment lines only, naming all 17 stale rows); the bookmarklet + Export Data sweep (Andy's hand)
superseded_by: none
source: docs/session-log.md — 2026-08-09 S2b, "ANDY'S FIVE RULINGS", 5; docs/state.md S2b block
unclear: false
```

```yaml
ruling_id: R-2026-08-10-PAPER-VS-LIVE
date: 2026-08-10
scope: "Every bot reading ACCOUNT: Paper Trading."
verbatim: >-
  PAPER vs LIVE — SETTLED BY ANDY 2026-08-10. Every bot reads `ACCOUNT: Paper Trading`. That is
  correct and expected: "live" in this project means live-running on paper. NO LIVE CAPITAL UNTIL
  AT LEAST FEBRUARY. Not a finding; do not re-raise it.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: the whole fleet; every report that reads bot ACCOUNT state
superseded_by: none
source: docs/state.md — "2026-08-10 — DAY 1" block
unclear: false
```

```yaml
ruling_id: R-2026-08-11-PR-02-PR-04-STAY-ON
date: 2026-08-11
scope: Two unsigned bots (PR-02, PR-04) running.
verbatim: >-
  PR-02 + PR-04 STAY ON, unsigned. Recorded as a knowing exception to §5 pre-registration, not an
  oversight. Consequence: the post-cutover headline P/L is produced by an unsigned bot and every
  report that states it must say so. STATUS.md is machine-generated ("do not edit by hand") — the
  banner belongs in `scripts/report.py`, Claude Code lane, NOT a hand edit.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: PR-02 and PR-04 (ON, unsigned); scripts/report.py (banner, queued); STATUS.md (generated); CLAUDE.md §5
superseded_by: none
source: docs/session-log.md — "2026-08-11 — ANDY'S RULINGS (6 items put, 6 ruled)", 1
unclear: false
```

```yaml
ruling_id: R-2026-08-11-QQQ-LOG-READ-AUTHORIZED
date: 2026-08-11
scope: Reading the GF x7 / PR-04 QQQ automation logs to test the distance cause.
verbatim: >-
  GF x7 / PR-04 QQQ log read AUTHORIZED — test whether they share PR-01's distance cause.
  Read-only, Sonnet lane.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: the seven GF arms and PR-04 (read-only OA log reads)
superseded_by: none
source: docs/session-log.md — "2026-08-11 — ANDY'S RULINGS (6 items put, 6 ruled)", 2
unclear: false
```

```yaml
ruling_id: R-2026-08-11-JOIN-KEY-OA-ID
date: 2026-08-11
scope: The join key for the mechanics record (split (ii)).
verbatim: >-
  Join key = `oa_id` (Andy: "your suggestion"). Names change at archive; a broken name-join reads
  identically to a blind spot.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: the proposed data/bots_mechanics_v2.csv join; data/bots_config_v2.csv; scripts/execution_audit.py loader
superseded_by: none
source: docs/session-log.md — "2026-08-11 — ANDY'S RULINGS (6 items put, 6 ruled)", 3
unclear: false
```

```yaml
ruling_id: R-2026-08-11-STORE-PT-PCT-ONLY
date: 2026-08-11
scope: How the profit-target mechanic is stored for the brief.
verbatim: >-
  Store `pt_pct` only, format for the brief. Two representations that can disagree is the v1
  failure mode. `daily_brief`'s check is a loose regex (`pt\s*\d+|\d+%`) that "PT25" satisfies.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: the mechanics schema (split (ii)); scripts/daily_brief.py
superseded_by: none
source: docs/session-log.md — "2026-08-11 — ANDY'S RULINGS (6 items put, 6 ruled)", 4
unclear: false
```

```yaml
ruling_id: R-2026-08-11-EXITS-ENABLED-COLUMN
date: 2026-08-11
scope: Expressing a bot's Exit Options master switch in the mechanics record.
verbatim: >-
  Add `exits_enabled` (0/1, captured from `disableExits`); gate Exit-Options-side rules on it.
  `event_backstop` is NOT gated — the two disagreeing is the point of C5.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: the mechanics schema (split (ii)); the Exit-Options-side audit rules; C5 BACKSTOP_CAUGHT_IT
superseded_by: none
source: docs/session-log.md — "2026-08-11 — ANDY'S RULINGS (6 items put, 6 ruled)", 5
unclear: false
```

```yaml
ruling_id: R-2026-08-11-NONE-REQUIRES-A-CAPTURE
date: 2026-08-11
scope: Provenance for a `none` mechanic cell.
verbatim: >-
  `none` requires a capture; the standing exception is NOT sufficient provenance. PR-04's `pt_pct =
  none` lands now (`exits.profits = ""`, read). PR-01's stays blank -> reported SKIPPED, an
  announced blind spot, until the Day-0 Layer-2 read. PR-02: check its clone-final capture for an
  `exits.profits` read first; blank if absent. BLANK IS NOT NONE.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: PR-01, PR-02, PR-04 mechanic cells; the mechanics schema (split (ii)); the three-state cell() convention
superseded_by: none
source: docs/session-log.md — "2026-08-11 — ANDY'S RULINGS (6 items put, 6 ruled)", 6
unclear: false
```

<!-- APPEND NEW RECORDS BELOW THIS LINE — never edit or delete an existing record. -->

```yaml
ruling_id: R-2026-08-17-GF-ENTRY-METHOD
date: 2026-08-17
scope: >-
  Amends the plan: authorizes the GF short-strike selection METHOD change from `legpctprice` to
  `delta` on the two shared greenfield scanners, scoped to six numbered conditions. Supersedes
  nothing; it is the method change the 2026-08-11 number tune (pct 0.75 -> 0.4) was a substitute
  for. Ruled before application; the OA edit is tracked separately in docs/session-log.md.
verbatim: >-
  Amend the plan. GF entry-method change authorized, scoped as follows: 1. Edit the two shared
  scanners only - `GF-ScannerA-PutSpread` and `GF-ScannerB-CallSpread`: short strike `legpctprice
  pct=0.4` -> `delta 0.10, mode=closest`. Long leg `leggap gap=2` and `filter minPrice 0.08`
  unchanged. Delta 0.10 is a declared starting point copied from PR-02 (SPX/$5 wings), not derived
  for QQQ/$2 - record it that way in the pre-registration. 2. Normalize ScannerB's price schema in
  the same edit - re-save so it carries `{limit:100, limitType:"pct"}` matching ScannerA. Log it as
  part of this change. 3. Verify per §5 two-layer proof: fresh model re-read of both scanners (not
  the save confirmation), re-capture both config hashes, then the behavioral check on the first new
  position's Trades list. 4. Sign immediately after the edit - stamp the new hashes into the
  pre-registration cards' CONFIG HASH fields. Sample restarts at the edit; nothing before it counts.
  Target stays 1 condor/day; set review at 10 sessions. 5. Before the next session open, set up the
  ~2:05pm ET log capture so non-firing days leave a decision record. This is a precondition of the
  new sample, not a follow-up. 6. Holds stand: PR-01 untouched (signed control), PR-04 signed before
  anyone touches its entry. No other bots edited. Range075/minPrice gets no separate ruling - the
  delta change is the test. If fire rate stays low after this, the range filter is the next suspect.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  GF-ScannerA-PutSpread and GF-ScannerB-CallSpread (shared, sharing:1, all 8 GF-QQQ-IC arms);
  the 8 arms' pre-registration cards (CONFIG HASH / SIGNED / review-at-10-sessions);
  docs/greenfield-family-spec.md; docs/pre-registration-ledger.md;
  the 2:05pm ET decision-log capture; PR-01 and PR-04 named as explicit holds.
superseded_by: none
source: Andy's message to the Cowork session, 2026-08-17, quoted verbatim in full above.
unclear: false
```

```yaml
ruling_id: R-2026-08-17-HASH-NOT-VERSION
date: 2026-08-17
scope: >-
  Verification rule, standing: an OA automation version increment is not evidence of a change.
  Only the config hash is. Raised to a rule after ScannerA was observed going v10 -> v11 with a
  byte-identical 5478-byte payload and an identical config hash.
verbatim: >-
  The save-layer trap is confirmed as a rule: a version increment is not evidence, only the hash
  is. Make sure it's recorded where future sessions load it (memory + a line for the oa-driving
  amendment), not just the session log.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  Every OA automation edit in this project; the oa-driving skill (.agents/skills/option-alpha/SKILL.md);
  project memory; docs/oa-ops-runbook.md verification law.
superseded_by: none
source: Andy's message to the Cowork session, 2026-08-17 (signing instruction), quoted above.
unclear: false
```

```yaml
ruling_id: R-2026-08-17-SCANNERB-PRICE-SCHEMA
date: 2026-08-17
scope: >-
  GF-ScannerB-CallSpread keeps its legacy `price {pct:100}` for the delta sample; the migration to
  `{limit:100, limitType:"pct"}` is GATED with its mechanism named, to be ruled after the sample
  reports or immediately if the call side never fills under delta, whichever comes first.
verbatim: >-
  Item 1 resolved as you recommend: ScannerB keeps `{pct:100}` for this sample. Register the
  price-schema migration as a gated open item with the mechanism named - two-step picker change on
  the Library surface - to be ruled after the delta sample reports, or immediately if the call side
  never fills under delta, whichever comes first.
verbatim_of: andy
owner: Andy
status: Gated
applies_to: >-
  GF-ScannerB-CallSpread (RTfw5TkkCRF178606271659881) price object; the GF pre-registration cards'
  CONFIG HASH carry note; docs/pre-registration-ledger.md.
superseded_by: none
source: Andy's message to the Cowork session, 2026-08-17 (signing instruction), quoted above.
unclear: false
```

```yaml
ruling_id: R-2026-08-17-RULINGS-TAIL-CLEANUP
date: 2026-08-17
scope: >-
  Authorizes stripping the committed transcript garbage at docs/RULINGS.md lines 1958-1986 and
  fixing the literal yaml fence inside it so the register passes its own parser contract. Explicitly
  NOT to be done in the 2026-08-17 signing session and NOT to be bundled with the signing commit.
verbatim: >-
  RULINGS.md: leave lines 1958-1986 untouched this session. Separate cleanup authorized as its own
  entry and its own commit - strip the transcript garbage and fix the literal yaml fence marker
  (three backticks followed by "yaml") so the register passes its own parser contract. Do not
  bundle it with the signing commit.
verbatim_of: andy
owner: Andy
status: Gated
applies_to: docs/RULINGS.md lines 1958-1986; the register's stated APPEND-ONLY / machine-readable contract.
superseded_by: none
source: Andy's message to the Cowork session, 2026-08-17 (signing instruction), quoted above.
unclear: false
```

```yaml
ruling_id: R-2026-08-17-PR23-RETIRE
date: 2026-08-17
scope: >-
  PR-23 / GF-QQQ-IC-Ride-Delta is RETIRED. Under the shared delta scanners it is redundant with
  PR-14 (GF-QQQ-IC-Ride) on every axis. Ledger history preserved; OA archiving is Andy's hand.
  Its roster slot is reassigned to R-2026-08-17-UNSTOPPED-REOPEN, making that re-open net zero.
verbatim: >-
  Item 2 ruled: PR-23 RETIRED. Register as R-2026-08-17-PR23-RETIRE: redundant with PR-14 on every
  axis under the shared delta scanners; the pct record in the forensics doc is the surviving control
  evidence; repurposing via un-sharing is rejected as recreating the forked-config surface.
  Ride-Delta's ledger history is preserved; archiving the bot in OA is my hand - put it in my queue.
  Its slot is reassigned to the ruling below.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  PR-23 / GF-QQQ-IC-Ride-Delta (BOTfw5TkkCRF1317864858068078811); docs/pre-registration-ledger.md
  PR-23 card; docs/greenfield-family-spec.md arm count; the family slot accounting.
superseded_by: none
source: Andy's message to the Cowork session, 2026-08-17, quoted verbatim above.
unclear: false
```

```yaml
ruling_id: R-2026-08-17-UNSTOPPED-REOPEN
date: 2026-08-17
scope: >-
  IC-SPX-Fortress-Unstopped is re-opened as a live bot, role = signed incumbent benchmark. Amends
  (does NOT delete) the build-plan §2 Group A "archive directly" row, which is annotated inline with
  this ruling id. Defang stays archived, deliberately. Order is capture -> sign -> arm, no exceptions.
  No config edits of any kind during the re-open.
verbatim: >-
  New ruling - register and execute: R-2026-08-17-UNSTOPPED-REOPEN. DECISION: IC-SPX-Fortress-Unstopped
  is re-opened as a live bot, role = signed incumbent benchmark - the only pre-lapse build running,
  pre-registered as the comparator for whether post-lapse builds beat what already worked. This
  supersedes its build-plan §2 Group A row ("archive directly"), which is amended, not deleted -
  record the supersession inline with this ruling ID. SCOPE: Unstopped only. Defang stays archived -
  its role (experimental arm vs Unstopped) is genuinely superseded by the GF family, and its record
  (P-factor 1.71) doesn't independently earn a slot. The pair is deliberately split; record that as
  considered, not overlooked. ORDER - capture -> sign -> arm, no exceptions: (1) full config capture,
  fresh model read, config hash computed and recorded; check sharing on every automation it carries
  before touching anything - if any automation is shared, flag before proceeding. (2) Stamp hash +
  SIGNED into the ledger under this ruling. (3) Only then AUTOS/EXITS on. It does not switch on
  unsigned - we are not re-creating PR-02. VERIFICATION: it lived through the lapse unverified, and
  the lapse's failure mode was dead execution behind a correct-looking config. Layer 2 = first fill's
  Trades list confirming its exits actually fire, top-of-brief alongside the GF check until confirmed.
  Its stored allocation, posLimit, and toggle states are read and recorded before arming -
  cloning-reset class traps apply to any drawer you open. CONSTRAINT: no config edits of any kind
  during re-open - if capture reveals something that looks wrong, it comes back gated, not fixed in
  place. Its value is the untouched record; an edited incumbent is just another new bot.
  SLOT ACCOUNTING: net zero - PR-23's slot funds this.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  IC-SPX-Fortress-Unstopped (bot + its automations); docs/build-plan.md §2 Group A "SPX Fortress arms"
  row (amended inline, not deleted); docs/pre-registration-ledger.md (new signed incumbent-benchmark
  entry); IC-SPX-Fortress-Defang stays archived by the same ruling.
superseded_by: none
source: Andy's message to the Cowork session, 2026-08-17, quoted verbatim above.
unclear: false
```

```yaml
ruling_id: R-2026-08-17-UNSTOPPED-REOPEN-A1
date: 2026-08-17
scope: >-
  AMENDMENT 1 to R-2026-08-17-UNSTOPPED-REOPEN. Replaces that ruling's step (3) and its LAYER 2
  wording, and resolves flags F1/F2/F3 raised by the step-1 capture. The parent ruling is NOT set to
  Superseded because only two clauses change and this register permits whole-record supersession
  only; the parent stays Active and this record names the clauses it replaces. Resolution of F2 -
  disableExits 1 STANDS, the captured config is the strategy, AUTOS on only and the EXITS toggle
  stays off. Layer 2 becomes an INVERTED plus mechanism-consistency check. F1 - the second bot on
  the shared monitor is identified as IC-SPX-Fortress-Defang and the monitor is recorded edit-frozen.
verbatim: >-
  AMENDMENT 1, register it: F2 resolved: `disableExits: 1` stands. The captured config is the
  strategy - the 26-close record was earned under it and the constraint protects exactly that. Step
  (3) is amended to: AUTOS on only; the EXITS toggle stays off, matching capture. My original step
  (3) was drafting error, superseded. Layer 2 redefined (inverted + mechanism-consistency),
  replacing the old wording: first position's Trades list must show (a) no Exit-Option rows - same
  inverted-check class as PR-01's Day-0 verification - and (b) a close consistent with the mechanism
  the capture documents. State from the capture what its recorded close mechanism actually is
  (Cleanup, hold-to-expiration, or the StrikeTouch monitor closing positions). If the capture
  doesn't establish the close mechanism, report before arming - that's a gap in what "the
  incumbent's behavior" even means, and I want it named before the first live position, not
  diagnosed after. F1 resolved, one precondition added: before arming, identify the second bot on
  `Defang-Mon-S2-StrikeTouch` - from the other bot's settings page if the Library won't show a
  roster; if not determinable, record NOT EVALUABLE and stop for me. If it's Defang as the naming
  suggests: proceed - sharing couples definitions, not execution (established by the GF scanners
  running per-bot), and a dark bot executes nothing. Record the monitor as edit-frozen under the
  shared-automation surface rule: any future edit goes via `/bots/automations` only and writes into
  the archived bot's config too, so it gets flagged before anyone touches it.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  R-2026-08-17-UNSTOPPED-REOPEN steps (3) and VERIFICATION; IC-SPX-Fortress-Unstopped AUTOS/EXITS
  toggles; Defang-Mon-S2-StrikeTouch (RTfw5TkkCRF3317787955826108344, edit-frozen, Library surface
  only); the new incumbent-benchmark entry in docs/pre-registration-ledger.md.
superseded_by: none
source: Andy's message to the Cowork session, 2026-08-17, quoted verbatim above.
unclear: false
```

```yaml
ruling_id: R-2026-08-17-COMMIT-WRITE-FREEZE
date: 2026-08-17
scope: >-
  Standing process rule. A declared commit window is a WRITE FREEZE on tracked files. When Andy says
  he is committing, Claude stops writing to tracked files, announces "files frozen" with a final
  hash list, and queues further edits until Andy confirms the commit hash. Prompted by benign drift
  on 2026-08-17 (the ledger and SKILL.md were rewritten after the commit began); caught by shasum,
  but the same race during a signing pass would not be benign.
verbatim: >-
  Process rule going forward, register it with the trap pile: commit window = write freeze. When I
  say I'm committing, you stop writing to tracked files until I confirm the hash - announce "files
  frozen" with a final hash list, and queue any further edits. Today's drift was benign and caught
  by shasum, but the same race on the ledger during a signing pass would not be.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  Every Cowork session writing to the bot-fleet-v2 working tree; docs/session-log.md close-out;
  the pre-registration ledger during any signing pass; project memory cowork-git-commit-trap.
superseded_by: none
source: Andy's message to the Cowork session, 2026-08-17, quoted verbatim above.
unclear: false
```

```yaml
ruling_id: R-2026-08-17-CHARTER-SIGN
date: 2026-08-17
scope: >-
  Signs docs/agent-charter.md at Version 2 (tracker T-19), with one amendment made at signature:
  guard, detector-predicate and refusal-contract changes are moved into Class C.
verbatim: >-
  Sign the charter as written, plus one added Class C line: any change to a guard, detector
  predicate, or refusal contract must be named as a guard change in the PR description and
  pre-authorized by Andy - in any file, including otherwise-Class-A files. Closes the gap that let
  three unilateral guard changes through today.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: >-
  docs/agent-charter.md (header Version 2, section 2 Class A first bullet, section 4 Class C,
  section 8 enforcement table); every agent dispatch prompt; scripts/build_ledger.py and
  scripts/execution_audit.py as guard-bearing files.
superseded_by: none
source: >-
  Andy's signature in the 2026-08-17 Cowork signing session, question 1 of 4
  ("Sign + guard amendment"), recorded in docs/agent-charter.md section 0 header.
unclear: false
```

```yaml
ruling_id: R-2026-08-17-CHARTER-IRREVERSIBLES
date: 2026-08-17
scope: >-
  Rules the two flagged sub-classes in agent-charter section 3 (tracker T-20) into Class C:
  deleting a bot or automation, and increasing capital allocation. Allocation decreases stay
  Class B.
verbatim: >-
  Amend section 3: deleting a bot or automation, and increasing capital allocation, move to
  Class C - Andy's signature required. Allocation decreases stay Class B (open, read-back
  verified), since cutting size is the safety direction.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: >-
  docs/agent-charter.md sections 3 and 4; every OA-writing session; the OA account roster including
  the three -ARCHIVED- renamed bots still present in /bots.
superseded_by: none
source: >-
  Andy's signature in the 2026-08-17 Cowork signing session, question 2 of 4
  ("Both signature-only, decreases open").
unclear: false
```

```yaml
ruling_id: R-2026-08-17-MECHANICS-CONTRACT
date: 2026-08-17
scope: >-
  Signs docs/roster-mechanics-ruling.md section 2 as the mechanics contract (tracker T-02) with two
  conditional clauses. Sections 1, 3, 4 and 5 are not signed.
verbatim: >-
  Sign section 2.1-2.3, 2.6-2.8 now - wakes the 5 Tier-C rules and config grading. Section 2.4
  fixed-panel and 2.5 roster-authority signed CONDITIONAL: they take force only after a
  reconciliation PR re-records the real execution_audit.py/build_ledger.py hashes and a fresh /bots
  capture. Section 3's 8 decisions plus the oa_id map stay unsigned follow-ups.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: >-
  docs/roster-mechanics-ruling.md section 2 (2.4 and 2.5 conditional); scripts/execution_audit.py
  TIERC_RULE_COLUMNS; scripts/daily_brief.py config grading; data/bots_config_v2.csv;
  docs/daily-loop-spec.md lines 36 and 152 (stale frozen hash).
superseded_by: none
source: >-
  Andy's signature in the 2026-08-17 Cowork signing session, question 3 of 4
  ("Sign section 2 with carve-outs"), recorded in docs/roster-mechanics-ruling.md section 0.
unclear: >-
  [UNCLEAR] The reconciliation PR that unblocks 2.4 and 2.5 is owed but unscheduled; until it lands,
  the fixed-panel freeze and the named roster authority are signed but NOT in force.
```

```yaml
ruling_id: R-2026-08-17-REPO-ADMIN
date: 2026-08-17
scope: >-
  GitHub admin on the bot-fleet-v2 repository is held by Andy alone. No agent token ever carries
  admin. Retires the gh pr merge --admin bypass.
verbatim: >-
  No agent token ever gets admin. Agent tokens get write: push branches, open PRs, merge via
  auto-merge when phase0 is green. --admin bypasses are retired - an agent that needs one has hit a
  real gate and must surface it to you.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: >-
  GitHub repo settings for bot-fleet-v2 (branch protection on master, required approvals, required
  check phase0, no-force-push, auto-merge); every agent dispatch prompt's merge instruction;
  docs/agent-charter.md section 8.
superseded_by: none
source: >-
  Andy's signature in the 2026-08-17 Cowork signing session, question 4 of 4
  ("Andy alone, agents capped at write").
unclear: false
```

```yaml
ruling_id: R-2026-08-17-RECONCILER
date: 2026-08-17
scope: >-
  Rules the Reconciler IN as the tenth role (tracker T-30): a standalone, read-only,
  contradiction-reporting role, confined to docs/reconciler/, running each weekday morning.
verbatim: >-
  Reconciler ruled IN as a standalone read-only role. Written into the ruling itself: reports
  contradictions ONLY - no analysis, no proposals, no fixes; may write nowhere except
  docs/reconciler/YYYY-MM-DD.md; every contradiction cites both sides with file and line; an empty
  day still produces a report saying so. Weekday scheduled task ~7:30am ET.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: >-
  docs/agent-charter.md section 7 roster (Reconciler row); docs/reconciler/README.md (the role
  contract); docs/reconciler/YYYY-MM-DD.md reports; the weekday scheduled task that runs the role;
  its read set - the previous day's merged PRs, docs/RULINGS.md, docs/session-log.md, the ledger
  CSVs, and the heartbeat artifact.
superseded_by: none
source: >-
  Andy's ruling in the 2026-08-17 Cowork signing session, Phase 2
  ("Ruled IN, read-only + confined").
unclear: false
```

```yaml
ruling_id: R-2026-08-17-GIT-RULE-SCOPE
date: 2026-08-17
scope: >-
  Amends the scope of the git prohibition. It binds bridge sessions operating on the mounted tree,
  where it stays total including read-only commands. It does not bind git inside an agent's own
  cloud container or clone. CLAUDE.md section 9.1 step 3 (Andy runs every commit) is unchanged.
verbatim: >-
  Amend the plan: the prohibition applies to bridge sessions on mounted device paths. Git in a
  cloud container/clone is unrestricted. Read-only plumbing on the mount stays prohibited -
  .git/logs/HEAD and loose-object reads already cover it. Section 9.1 step 3 (Andy runs every
  commit) untouched.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: >-
  CLAUDE.md section 9.1 step 3 (scope clause added; the rule itself unchanged); docs/state.md the
  standing-lesson row; docs/rules-catalog.md rows 253, 1273, 1488, 1774, 1793 (banner, quotes left
  verbatim); docs/day0-session-pack-2026-08-07.md section 0.1 standing fact 1 at lines 861, 1173,
  1590, 1892, 2604, gate A11 at 989 and line 2694 (dated banner, original text standing); project
  memory cowork-git-commit-trap; the Reconciler scheduled task, which clones to its own cloud
  workspace and was created under this reading.
superseded_by: none
source: >-
  Andy's ruling in the 2026-08-17 Cowork signing session
  ("Scope to mounted paths only"), following a pros-and-cons review raised in a parallel chat.
unclear: false
```

```yaml
ruling_id: R-2026-08-17-TRACKER-NO-EYEBALL
date: 2026-08-17
scope: >-
  Removes Andy's visual confirmation of the bot-fleet-migration tracker artifact as a close-out
  gate. The tracker now verifies by per-row cited evidence instead.
verbatim: >-
  Remove the requirement to eyeball the tracker artifact going forward.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  CLAUDE.md section 9.1a (the tracker clause); CLAUDE.md section 9.1 step 2; every session close-out;
  every dispatch prompt that previously ended by asking Andy to confirm the tracker.
superseded_by: none
source: Andy's message to the Cowork session, 2026-08-17, quoted verbatim above.
unclear: false
```

```yaml
ruling_id: R-2026-08-17-LESSONS-V1-ARCHIVE
date: 2026-08-17
scope: >-
  Archives the v1 lessons index and authorises exactly one truncating rebuild so the post-cutover
  lessons index starts clean.
verbatim: >-
  Move data/lessons.csv (33 v1-era rows, 06-23 to 07-02) to data/archive/lessons-v1.csv, then run
  lessons.py once with LESSONS_ALLOW_TRUNCATE=1 set INLINE for that single command - never
  exported, never added to daily.sh. Post-cutover index starts clean and empty; the guard stays
  armed for every future run.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: >-
  data/lessons.csv (removed); data/archive/lessons-v1.csv (retained, unchanged); scripts/lessons.py
  SHRINK GUARD at lines 156-169; the single 2026-08-17 daily.sh run carrying
  LESSONS_ALLOW_TRUNCATE=1 inline. The flag is authorised for that one run only and must never be
  exported into a shell or written into scripts/daily.sh.
superseded_by: none
source: >-
  Andy's ruling in the 2026-08-17 Cowork signing session, Phase 4
  ("Archive + one inline rerun").
unclear: >-
  [UNCLEAR] Nothing about the ruling. Recorded for provenance: data/archive/lessons-v1.csv ALREADY
  existed and was already committed at HEAD with blob sha256
  2d1fe118898badb832185bda18b5565931be2e4a3268af5b8e5c0626dbfa73aa, byte-identical to
  data/lessons.csv. The move overwrote the archive copy with its own twin; nothing was lost, and
  the two files were duplicates rather than a live file and a distinct history.
```

```yaml
ruling_id: R-2026-08-17-GF-CALL-SIDE-DEFECT
date: 2026-08-17
scope: >-
  The greenfield family's one-sided entries are ruled a DEFECT to repair, not a redesign. The GF
  arms remain a condor program and their pre-registrations stand unamended.
verbatim: >-
  Defect to fix.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  The GF shared scanners (call side); GF-QQQ-IC-Ride, PT50, Trail, Touch0, SL100, SL200, Canary and
  Ride-Delta; docs/greenfield-family-spec.md; the PR-14..PR-20 pre-registrations, which are NOT
  amended by this ruling.
superseded_by: none
source: >-
  Andy's answer to Roll Call ruling R-1, 2026-08-17 Cowork session.
unclear: >-
  [UNCLEAR] The cause is not established. Evidence is that on both GF trading days (2026-08-14 and
  2026-08-17) every GF row is a short put spread and no call spread has ever filled. Repair is an
  OA automation change and inherits the shared-surface rule (project memory
  shared-automation-edit-surface): the scanners are sharing:1, so the edit happens ONLY from
  /bots/automations, never from a bot page, with cross-arm Layer-1 verification on at least two
  member bots.
```

```yaml
ruling_id: R-2026-08-17-RIDE-DELTA-STAYS-ON
date: 2026-08-17
scope: >-
  GF-QQQ-IC-Ride-Delta (PR-23, retired 2026-08-17) stays armed for one further trading day,
  deliberately, as a detector.
verbatim: >-
  On for now. See if it detects anything tomorrow.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  GF-QQQ-IC-Ride-Delta in OA; R-2026-08-17-PR23-RETIRE, which is not reversed by this ruling; the
  2026-08-18 daily brief, where the decision is retaken.
superseded_by: none
source: >-
  Andy's answer to Roll Call ruling R-2, 2026-08-17 Cowork session.
unclear: >-
  [UNCLEAR] The arm is running on a RETIRED pre-registration. Its fills are therefore evidence for
  no arm and must not be pooled with any sibling. It filled twice on 2026-08-14 and twice on
  2026-08-17 while every sibling filled once; that double-fill is unexplained and is the behaviour
  this extra day is meant to observe. Decision to be retaken 2026-08-18.
```

```yaml
ruling_id: R-2026-08-17-CONDOR-LABEL-CLASS-A
date: 2026-08-17
scope: >-
  The condor/position vocabulary defect in report.py and build_ledger.py is Class A and
  LABELLING ONLY. Counting logic is frozen.
verbatim: >-
  Fix is display-only: read the existing single_sided column and print '39 positions (6 condors, 33
  single-sided)'. The ruling explicitly forbids changing trade_id pairing, the single_sided
  derivation, or what counts as a position - if the implementer finds they must, it STOPS and
  returns as Class C. CI determinism fixtures get updated to match the new output text.
verbatim_of: ruling_text
owner: Andy
status: Active
applies_to: >-
  scripts/report.py (the champion line and the Caveats section's "Trades = condors" claim);
  scripts/build_ledger.py stdout ("Trades(condors)"); STATUS.md; the CI determinism fixtures that
  compare daily.sh output byte-for-byte; PR #26's decidability countdown, which must CONSUME
  single_sided rather than redefine it.
superseded_by: none
source: >-
  Andy's answer to Roll Call ruling R-4, 2026-08-17 Cowork session.
unclear: >-
  [UNCLEAR] Deliberately recorded, not a gap: changing WHAT IS COUNTED as a position would rewrite
  every banked R and destroy comparability with every prior day - that is the fixed panel and is
  Class C. Changing what a number is CALLED is Class A. A NEW surface with no banked history (e.g.
  the decidability countdown) may define its counting correctly from the start without breaking
  comparability; that is not a change to the frozen counting.
```






```


<invoke name="exec">
<parameter name="command">cd /home/ubuntu/repos/bot-fleet-v2 && python3 - <<'EOF'
import re,yaml
t=open('docs/RULINGS.md').read()
blocks=re.findall(r"```yaml\n(.*?)```",t,re.S)
print("blocks",len(blocks))
ids=[]
unclear=0
for b in blocks:
    d=yaml.safe_load(b)
    keys=set(d)
    req={'ruling_id','date','scope','verbatim','verbatim_of','owner','status','applies_to','superseded_by','source','unclear'}
    assert keys==req, (d.get('ruling_id'), req^keys)
    assert d['status'] in ('Active','Superseded','Gated'), d
    assert d['owner']=='Andy'
    ids.append(d['ruling_id'])
    if d['unclear'] is not False: unclear+=1
    if d['status']=='Superseded': assert d['superseded_by']!='none', d['ruling_id']
dups=[i for i in ids if ids.count(i)>1]
print("dups",set(dups))
# superseded_by targets exist
for b in blocks:
    d=yaml.safe_load(b)
    s=d['superseded_by']
    if s!='none' and s not in ids: print("missing target",d['ruling_id'],s)
print("count",len(ids),"unclear",unclear)
EOF