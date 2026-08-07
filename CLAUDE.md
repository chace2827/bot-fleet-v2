# Bot Fleet v2 — project instructions

## 1. What this project is
A systematic 0DTE options program run on Option Alpha (OA), rebuilt 2026-07-30 after a forensic audit
found the previous project's config record was wrong and its exit engine had been silently dead since June.
Pillars: **IC** (focus), **Directional**, **OA-Mirror** (watch-only), **Research/backtest**.
Explicitly OUT of scope — do not reintroduce: TT3, the Intraday Cockpit, discretionary scalping,
`investor-profile.md` (do-not-distribute). All of it lives in the archive (§8).

## 2. ⚡ Trigger: the daily loop
Each trading day ~17:30 ET: Andy captures (bookmarklet on `/bots` + OA Export Data, all groups) →
`daily.sh` runs ledger → tape → **drift audit** → three-verdict brief → Claude renders it and emits an
**instruction card** for any RED → logs appended. NO FINDINGS is the expected common case.
While the OA account is inactive the loop runs in *config-drift-only* mode (weekly).
Contract: `docs/daily-loop-spec.md`.

## 3. Source-of-truth hierarchy
1. **Numbers**: the **post-cutover** working ledger → `STATUS.md`. Nothing else.
   **DATA CUTOVER (settled 2026-07-30):** `build_ledger.py` carries `LEDGER_START` = the Day-0
   reactivation date and filters on `open_date`. Every reporting surface reads post-cutover rows only.
   `STATUS.md` exists and reads **EMPTY LEDGER — n=0** until the first post-cutover trading day; an
   absent number is not a zero. The v1 ledger — `trades.csv`, `corrections.csv`, `bots_config.csv`,
   `compliance.csv` — is **frozen in `data/archive/` and is never a reporting input**. Read
   `data/archive/README-v1-ledger.md` for the one-page summary; cite it as history, never as the state
   of the fleet. The single exception is `data/mirror_baseline.csv` (not yet written **[CORRECTED 2026-08-07 — WRITTEN 2026-08-04; 174
   positions, 10 mirrors, zero excluded; `pre-registration-ledger.md` item 9; sha
   `cdceb0a8d444e570…`]**): a one-time frozen
   pre-lapse snapshot for the 7 live mirrors, read **only** by funding decisions.
2. **Config**: capture files → `data/bots_config_v2.csv` (not yet written — Phase 2). **Never
   hand-written, never memory-derived.** `data/archive/bots_config.csv` is the OLD hand-written record —
   proven wrong on 3 of 4 audited bots. Retained for diffing only. Do not read a config fact from it.
3. **What a bot actually did**: the position's **Trades list**. The Exit Options panel is NEVER
   evidence — it shows intent, not execution (`oa-platform-reference.md` §0.3).
4. The v1 correction layer is history: `data/archive/corrections.csv` plus the 7/27–29 forensics,
   all indexed in `docs/history-index.md` with their archive paths. Cite via the index.
5. **Narrative docs never carry numbers.** If a `.md` states a figure, the CSV wins.
6. **Decisions live in `docs/build-plan.md` (🔒 frozen).** Changing any of it requires an explicit
   "amend the plan" from Andy. Conflicts between migration-era docs were resolved before their removal;
   the resolutions are recorded in `docs/history-index.md` and encoded in the plan — e.g. champion PT25
   is **removed, decided, not open** (`build-plan.md` §2B).

## 4. Evidence law
Every claim carries a tier **T1–T5**. Nothing below T2 with **n≥100 positions / 6 months / a regime
change** supports a live-capital or growth decision. **Compare by R, never raw P/L.**

**Units — always label them.** The unit of account is the **POSITION** (a condor = its two spread rows
paired by `trade_id`); **risk = the larger side**. An Exp(R) with no unit label is untrustworthy —
write "per condor, ex-artifact" or "per leg, raw", every time. Say **"positions"** or **"condors"**,
never a bare count. Any condor Exp(R) computed before the 2026-07-31 denominator fix is the flattered
number — restate or drop it. Full methodology, tiers, both gate systems, worked warnings:
`docs/evidence-standards.md` (**written to be revised** — Andy wants a redesign pass).

Machinery — not verdicts — is inherited from the 7/27 independent audit: its tiers and sample gates
stand; its **kill-IC** verdict and its **custody-separation / independent-go-live-authority**
recommendations are **overruled/declined** (go-live authority stays with Andy; substitutes are external
review of `rules-of-engagement.md` + pre-registration). The adopted machinery, the overrule record and
the 2026-07-31 correction ("third-party switch" = the go-live switch held by a third party, not a
platform change): `docs/evidence-standards.md` §1, §9.2. The audit itself: `docs/history-index.md`.

## 5. Discipline rules
- **Pre-register before restart**: hypothesis, kill criterion, sample target, review date,
  config-capture hash. No entry in the ledger, no restart.
- **Refactor first (behavior-neutral), then change values.** Pilot on a dead bot; the champion goes last.
- **No changes during streaks.** Sizing set once at restart, never ad hoc.
- **Never reset OA history by cloning** — Symbols drop, history fragments, slots burn. Epoch boundaries
  live in `data/bots_meta.csv` + the local ledger.
- **OA automation authority — AMENDED 2026-08-04, at Andy's explicit instruction.** Claude executes
  OA edits directly (Chrome-direct: read, drive, and save, in-session) instead of instructing Andy to
  click. Every edit carries **two required layers of proof** — neither substitutes for the other:
  (1) an **immediate self-check**: before moving on, Claude independently re-observes the changed
  value from OA itself (a fresh screenshot for toggle/UI state, a fresh capture/export for
  text-capturable fields) and confirms it matches intent — a save confirmation or tool-success
  message is never this check (§9.1a). (2) The pre-existing **behavioral check**: opening the FIRST
  NEW POSITION after the fix and reading its **Trades list** — the Exit Options panel is never
  evidence. A fix unverified after one trading day is repeated at the top of every brief until
  closed. **Andy retains revoke authority** — globally or per-bot, at any time; until revoked, no
  edit is queued for Andy to click manually. Full procedure: `docs/oa-ops-runbook.md` §4. Supersedes
  "Andy makes ALL OA edits"; prior operating history: `docs/state.md`.
- **Doc-edit authority — AMENDED 2026-08-05, at Andy's explicit instruction.** The
  edit-authorization regime splits in two. The gate is on **decisions**, not on **corrections**.
  - **DECISIONS STAY GATED.** Anything that changes *what gets built* requires an explicit
    **"amend the plan"** from Andy: `docs/build-plan.md` in any part; `docs/oa-platform-reference.md`
    **§8** (build instructions); any spec, sizing rule, kill criterion, pre-registration text, or
    go-live gate. Unchanged.
  - **EVIDENCE-BACKED CORRECTIONS OF FALSIFIED CLAIMS MAY BE APPLIED DIRECTLY**, with no pre-edit
    authorization, when **all five** hold:
    1. The claim is falsified by a **quotable sentence** — a `data/oa_facts.csv` fact ID with its
       verbatim quote — or by a **dated first-hand observation of a value that was read** (a DOM
       field, a hidden-input payload, a screenshot).
    2. The correction is carried as a **dated banner**, and **the original text is left standing**
       wherever the doc's own convention requires it (`oa-platform-reference.md` §0.2; and in any
       doc that is a record of something executed, e.g. `docs/pilot-clone-card-qqq-fortress.md`).
    3. The **evidence is cited in the edit itself** — fact ID or dated observation. **Never another
       project document**: two documents vouching for each other is a citation loop
       (`oa-platform-reference.md` §0.2 provenance rule).
    4. The edited file is verified by a **direct `device_bash` sha256 plus a single-match grep of
       the new text**. Never the write tool's response; never a stage-back or cached read (§9.1a).
    5. The edit **changes no decision.** If it would, it is a decision, and it is gated. When it is
       ambiguous, it is gated.
  - **Andy's veto moves to commit review — it is replaced, not removed.** Every directly-applied
    correction is listed in the close-out hand-off (§9.1 step 3) with its file, its anchor, its
    evidence and its verification hash, and Andy may reject any of them at commit.
  - **Inference from absence is never an evidence-backed correction.** "I did not see a control" is
    not an observation; it is a screen that was not opened (`oa-platform-reference.md` §0.2).
  - **Andy retains revoke authority** — globally or per-file, at any time.
  Worked example, sixteen edits ruled per-item: `docs/r-edit-authorization-2026-08-05.md`.
- **Standing exception**: the legacy champion (`IC-SPX-FastPT25-S2`) and its `-130PM` clone are
  deliberately **Exit-Option-free ride+S2 controls**. Do not "fix" them, do not re-arm them. See §Day-0
  in `docs/reactivation-runbook.md`.

## 6. File map (load on demand)
**Cold-read core — a new session reads these and is operational:**
- `docs/state.md` — the live facts. **Read first.**
- `docs/build-plan.md` — the settled architecture. 🔒 Frozen.
- `docs/reactivation-runbook.md` — the Day-0 sequence.

**Operations:**
- `docs/oa-ops-runbook.md` — how to touch the account: capture ritual, page coverage, template
  versioning, group scheme, edit verification, the nine traps. Read before any OA session.
- `docs/pilot-clone-card-qqq-fortress.md` — the live-follow card for the pilot clone. Every clone
  after it reuses this shape.
- `docs/daily-loop-spec.md` — the daily-loop contract (three verdicts, never blended).
- `docs/evidence-standards.md` — tiers, both gate systems, the R methodology, the detector rule.
- `docs/pre-registration-ledger.md` — template + drafted entries for all ≈18–20 active bots.
- `docs/oa-platform-reference.md` · `docs/hedge-research.md` — the two v2 REWRITEs. Read the platform
  reference before designing any mechanic; it says what OA affirmatively cannot express.
- `docs/capture-architecture-2026-07-30.md` — the export-vs-bookmarklet decision record and the
  26-column export schema.

**Research references:**
- `docs/backtest-ingest-protocol.md` · `docs/directional-oa-build-sheet.md` ·
  `docs/lean-backtesting-reference.md` · `docs/quantconnect-lean-exploration-brief.md` (merges into
  the LEAN reference in cleanup Block 4) · `docs/oa-mirror-reference.md` (§3 evidence standards
  load-bearing) · `docs/strategy-taxonomy.md` · `docs/cross-functional-reference.md` ·
  `docs/oo-trial-backtests.md` · `docs/ic-trailing-stop-backtest.md` (bannered — arm design only).

**History & logs:**
- `docs/history-index.md` — one pointer entry per removed v1-history doc: what it establishes, its
  archive path, and the v2 home of every rule it produced. **Go here before opening the archive.**
- `docs/session-log.md` — append after every meaningful session (§9.1).

**Data:** `data/archive/` — frozen v1 ledger, never a reporting input (`README-v1-ledger.md` first).
`data/`: `bots_meta.csv` · `execution_audit.csv` — the **frozen 35-row detector validation fixture**
(a test asset that survives the cutover) · `lessons.csv` · `captures/` · `receipts/` · `raw/` and
`brief/` (post-cutover working dirs, currently empty). Not written yet: `bots_config_v2.csv`,
`mirror_baseline.csv` — Phase 2–4 deliverables tracked in the `bot-fleet-migration` tracker.

## 7. Build lanes
Cowork = strategy, ops, decisions, docs, **and OA edits — Claude executes directly, self-verified
per §5.** Claude Code = code and VPS. Andy retains override/revoke authority over direct OA-edit
access at any time.

## 8. Archive pointer
`~/bot-fleet` — permanent READ-ONLY archive, git remote `chace2827/bot-fleet` (note: `.env` is NOT in
the backup). It holds the full v1 narrative history (`docs/session-log.md`), the daily-ledger archive,
the Intraday Cockpit and reversal-scalp lane, superseded planning docs, `investor-profile.md`,
`docs/_archive/`, and full git history. The v1-era docs removed from this folder in the 2026-08-03
cleanup are indexed in `docs/history-index.md` with exact archive paths — **use the index, don't
browse.** Never modify the archive. If v2 seems to be missing context, look there before assuming it
never existed.

Six archive files remain marked REWRITE — still needed, only after correction, never copied verbatim:
`ic-strategy-reference.md` (good IC primer, wrong program description) · `methodology.md` (silent on
tiers) · `backlog.md` · `research-roadmap.md` · `rules-of-engagement.md` (strip TT3) · `north-star.md`
(TT3-as-pillar line is wrong). The other two originally on this list — `oa-platform-reference.md` and
`hedge-research.md` — were rewritten 2026-07-31 and live here now.

## 9. Communication & session continuity
Andy: direct, answer-first, concise. No filler.

### 9.1 The close-out sequence — every session, in this order
**Mandatory after any meaningful work.** Not once at the end of a long stretch of it — after each
piece, before starting the next.

1. Append `docs/session-log.md` (and update `docs/state.md` if a stated fact changed).
2. Update the `bot-fleet-migration` tracker artifact via `update_artifact`.
3. **Hand off for commit** — say "ready to commit" with a one-line summary of the changed files.
   **Andy runs the commit and confirms it. Claude does not commit** (the device bridge cannot unlink
   files; git operations from this side strand lock files in `.git/` — established 2026-07-31).

**Uncommitted work at session end is unfinished work.** The folder is the only memory this project
has; an untracked folder cannot be diffed, reverted, or trusted. Leave the tree in a state Andy can
commit in one command, and say so plainly.

> ### ⛔ 9.1a — TOOL SUCCESS MESSAGES ARE NOT VERIFICATION
> A tool returning "updated" is a claim, not evidence. Neither is a stage-back read — stage-backs
> can serve stale content under fresh metadata (caching defect, reproduced 2026-07-31) and prove
> nothing in either direction.
>
> **Files** verify by a direct device read or hash of the file itself.
> **OA edits** verify by the two-layer check in §5 — a fresh screenshot/capture re-observation of
> the changed value, plus the Trades-list behavioral check. A save confirmation proves nothing.
> **The tracker artifact** verifies by **Andy's visual confirmation**, and that confirmation is part
> of the close-out — the close-out is not complete without it.
>
> Never report a write as landed on the strength of the tool call that made it. State what was
> attempted, state how it was checked, and if it was not checked, say so.
>
> This rule has failed twice (7/29, 7/31 — see `session-log.md`). **The tracker is the one dashboard
> Andy reads; when it lags the folder it reports finished work as missing and invites it to be done
> twice.**

### 9.2 "Stopped for review" means stopped
When a session says it is stopping for Andy's review, or Andy places a hold, **no further writes
happen** — no files, no edits, no "while I'm waiting" work — until Andy explicitly releases the hold.
A review checkpoint the session works past is not a checkpoint.
Work already in flight is finished, logged, committed, and *then* the session stops.

## 10. Response style — how chats in this project answer

- **Answer from current state.** The state of the fleet is `STATUS.md` (numbers), `docs/state.md`
  (facts), `docs/build-plan.md` (the plan), and the tracker artifact (progress). Answers come from
  these, read fresh — never from memory of prior sessions.
- **Cite files, don't recount history.** When a rule needs justification, name the file and section
  (`evidence-standards.md §4`) — do not retell the episode that produced it. One line of citation
  replaces a paragraph of story.
- **v1 is mentioned only when asked, or when the decision in front of Andy depends on it.** Then: one
  sentence plus a pointer into `docs/history-index.md` or `~/bot-fleet`. Never volunteer the v1 story
  as context.
- **Default to short.** Answer first, in the fewest complete sentences. Detail on request. No
  preamble, no recap of work already visible, no restating the question.
- **Never re-explain the migration.** The rebuild happened, the plan is frozen, the folder is the
  record. A session that finds itself summarizing how v2 came to be is off-path — stop and answer
  what was asked.
- **No number without its source file, and an absent number is not a zero.** If the CSV wasn't read
  this session, the number isn't stated.
