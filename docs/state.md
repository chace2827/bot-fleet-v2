# State — Bot Fleet v2

*The live facts. Updated whenever a stated fact changes (CLAUDE.md §9.1). Numbers live in
`STATUS.md`; the plan in `docs/build-plan.md`; progress in the `bot-fleet-migration` tracker.
Last updated 2026-08-03.*

## Account
- OA subscription **INACTIVE**. Andy reactivates **~mid-Aug**. The reactivation date is
  **Day-0 = `LEDGER_START`**.
- No new entries since 7/02. **5 multi-day mirror positions were still open** at the 7/30
  capture (`QQQ long call` ×4, `Tasty Condor` ×1) — ride-or-close is an explicit Day-0
  decision (`reactivation-runbook.md` §4 Step 2). Per the straddle rule they resolve into the
  mirror baseline layer, never the working ledger.
- **Edits made while inactive persist** (verified empirically 7/29→7/30) — building ahead is
  safe.
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
  (`pilot-clone-card-qqq-fortress.md`) is written and **HELD** for Andy's next OA session.
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
- **Pilot clone** (`QQQ-IC-0DTE-Fortress`) — first thing in Andy's next OA session. Two open
  platform answers ride on it: does an Exit Option Preset save control exist, and can a
  Scheduled Event reach 15:52.
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
- **HOLD in force on the builder chat** — no writes there until Andy returns with the pilot
  captures and the two open answers.
