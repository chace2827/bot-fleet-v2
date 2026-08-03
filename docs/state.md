# State — Bot Fleet v2

*The live facts. Updated whenever a stated fact changes (CLAUDE.md §9.1). Numbers live in
`STATUS.md`; the plan in `docs/build-plan.md`; progress in the `bot-fleet-migration` tracker.
Last updated 2026-08-03 (pilot session, part 1).*

## Account
- OA subscription **INACTIVE**. Andy reactivates **~mid-Aug**. The reactivation date is
  **Day-0 = `LEDGER_START`**.
- No new entries since 7/02. **5 multi-day mirror positions were still open** at the 7/30
  capture (`QQQ long call` ×4, `Tasty Condor` ×1) — ride-or-close is an explicit Day-0
  decision (`reactivation-runbook.md` §4 Step 2). Per the straddle rule they resolve into the
  mirror baseline layer, never the working ledger.
- **Edits made while inactive persist** (verified empirically 7/29→7/30) — building ahead is
  safe. **Extended 2026-08-03: bot CREATION persists too** (roster 35→36 across a full
  navigation), and so do automation renames. OA's "no changes will be saved" banner is false.
- Andy has confirmed **both dashboard toggles (`AUTOMATIONS`, `EXIT OPTIONS`) are OFF on all
  35 bots.** The lapse mechanism and its Day-0 consequences: `reactivation-runbook.md` §1,
  `oa-platform-reference.md` §10.

## What is built
- **The ledger stack is code.** `build_ledger.py` refuses to run without `LEDGER_START`,
  filters on `open_date`, routes straddlers to `data/straddlers.csv`, writes run receipts.
  `scripts/execution_audit.py` passes its 12/12 validation matrix. `daily.sh` is 8 stages
  (drift audit at stage 3) and degrades cleanly at n=0. `STATUS.md` and `dashboard.html`
  generate at n=0 — **empty by construction, not by failure.**
- **Phase 3's document set is complete.** The pilot-clone card
  (`pilot-clone-card-qqq-fortress.md`) is written and was **partly executed 2026-08-03** — see
  Open items.
- **The pilot clone EXISTS in OA**: `QQQ-IC-0DTE-Fortress Clone`,
  bot_id `BOTfw5TkkCRF2717857919585029021`, allocation $100,000, limits 2/2, `AUTOMATIONS` OFF,
  `EXIT OPTIONS` ON. It cannot trade. The original `QQQ-IC-0DTE-Fortress`
  (`BOTfw5TkkCRF817734373392552121`) is **untouched and verified so**. Roster is now **36 bots**.
- **Folder cleanup in progress** (approved 2026-08-03): Block 1 done — 16 v1-history docs
  removed, `docs/history-index.md` added. Block 2 = this page + the CLAUDE.md rewrite.
  Blocks 3–4 (ops-doc trims, reference merges) deferred until after the pilot / Day-0.

## Not built yet — do not go looking for them
- `data/bots_config_v2.csv` (Phase 2 — written from capture, never by hand) and
  `data/mirror_baseline.csv` (one-time frozen mirror snapshot, built from
  `data/captures/oa_export_positions_2026-07-30.csv`, **not** from the archived ledger).
- The liveness check is half-done: the `SILENT_BOT` rule ships, but the bot-log side needs a
  log source the detector does not have.

## Day-0 first action
**Set `LEDGER_START` in `build_ledger.py` before anything else.** Then
`reactivation-runbook.md` top to bottom.

## Open items
- **Pilot clone — PART 1 DONE, PAUSED MID-RITUAL** (2026-08-03). Steps 0–1 complete and
  verified; **Step 2 is VOID** (see below); Steps 3–4 verified in passing; **Steps 5–9 and FINISH
  not started**. **Both platform answers are still UNANSWERED** — does an Exit Option Preset save
  control exist, and can a Scheduled Event reach 15:52. B's location is known: automation
  `Edit Settings` → `Schedule` → `Market Time (EST)`.
  **Three loose ends on the clone:** ScannerA is still named `Fortress-ScannerA-PutSpread-CLONE`
  (revert pending), Bot Group is `None` (was `Monitor`), Tags are empty (were `experiment`).
- **⛔ TRAP 1 IS FALSE — cloned bots do NOT share automations by reference** (direct test,
  2026-08-03). Sharing is opt-in via the Automation Library only. This falsifies
  `oa-platform-reference.md` §2, `oa-ops-runbook.md` §5 Trap 1, and voids the card's Step 2 —
  removing a `Delete` from the ritual for all four clones. **Corrections pending Andy's
  authorization; nothing edited.**
- **The clone's exits already existed.** Both Open Position actions carry PT50 + a 15:50 time
  exit. `build-plan.md` §2B's "restored exits" is a no-op; only the 15:52 backstop is new work.
  The §2B justification wording is now inaccurate — flagged, frozen, not edited.
- **Three undocumented clone traps**: Allocation resets to `1000`, Bot Group drops to `None`,
  Tags drop. None are in any doc.
- **`oa-platform-reference.md` tag-provenance audit needed.** Its `[FIRST-HAND]` tag on the clone
  trap cites the runbook, which asserts the same claim — a citation loop with no observation
  behind it. That file gates the greenfield builds and all four clone specs.
- **Tournament doc conflict**: `oa-ops-runbook.md` §3 (fork so arms are NOT shared) vs
  `build-plan.md` §2D + `hedge-research.md` §5.2 (shared automation required). Incompatible now
  that the mechanism is understood. Unresolved; build-plan frozen.
- **Entry pricing open question**: `oa-platform-reference.md` §7 bans Market pricing "on every
  exit"; the Fortress enters at Market on both sides. No literal conflict — the ban is
  exit-scoped — but the cited failure mechanism is order-type-specific, not side-specific.
  Entry Market → SmartPricing would be a future pre-registered decision.
- **CHROME-DIRECT OA EDITS — TRIAL, authorized 2026-08-03.** Claude executed OA edits directly
  via Claude-in-Chrome under five hard stops, as a sanctioned trial of amending `build-plan.md`
  §5 / `CLAUDE.md` §5. **Neither frozen doc was edited; the standing rule "Andy makes all OA
  edits" remains textually in force.** Trial verdict (session log, 2026-08-03): **qualified pass
  — Claude reads and detects, Andy clicks.** Reading/capture was a clear gain; self-verified
  mutation produced a false claim in a capture file. Doc amendment pending Andy's decision.
- **Fortress strike check — optional research, non-gating.** Both Fortress bots still carry
  `strike_fix=Y` in `bots_meta.csv` while `build-plan.md` §2B rests on their positive
  pre-regression record; nobody has checked their strikes against the tape. `build-plan.md`
  §3 rules this adjudication **dead as a blocker** — it concerns archived bots and
  pre-cutover data, and the clone starts at n=0 judged on its own gate evidence
  (`build-plan.md` §4). Re-filed 2026-08-03 from "queued as a Phase 2 verification";
  parallel to the Baseline forensic in `build-plan.md` §6. It affects only how the frozen
  v1 record is read — not the pilot, not Day-0, not any live decision.
- 48 cached symbol-days of 5-min SPX/QQQ tape (5/29→7/02) were never committed; Tradier's
  window is rolling and the early days are unrecoverable. Noted, closed as a loss.
- RoE `$` blanks stand by decision (an active audit-gate H3 failure — `evidence-standards.md`
  §10 item 4). Notion's role in v2 is undecided.
- **⚠️ `bot-fleet-v2` HAS NO GIT REMOTE — the folder exists on one disk only.**
  Discovered 2026-08-03 when `git push` failed: `.git/config` carries only `[core]` and
  `[user]`, no `[remote]`. Every v2 commit since the 7/30 rebuild (`298d7a3`, `e7f3b36`,
  `6a39373`, `83af63b`) is unbacked. `CLAUDE.md` §8's remote (`chace2827/bot-fleet`) belongs to
  the **archive**, not to v2 — it has been standing in for a backup that does not exist.
  Fix: create a private repo, then `git remote add origin <url>` + `git push -u origin master`.
  ⚠️ Confirm `.gitignore` covers `.env` before the first push (§8 records `.env` is
  deliberately absent from the archive backup).
- **HOLD in force on the builder chat** — no writes there until Andy returns with the pilot
  captures and the two open answers.
