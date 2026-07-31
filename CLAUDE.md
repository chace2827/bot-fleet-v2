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
Contract: `docs/daily-loop-spec.md` (written in Phase 3).

## 3. Source-of-truth hierarchy
1. **Numbers**: the **post-cutover** working ledger → `STATUS.md`. Nothing else.
   **DATA CUTOVER (settled 2026-07-30):** `build_ledger.py` carries `LEDGER_START` = the Day-0 reactivation
   date. Every reporting surface reads post-cutover rows only. The v1 ledger — `trades.csv`,
   `corrections.csv`, `bots_config.csv`, `compliance.csv` — is **frozen in `data/archive/` and is never a
   reporting input**. Read `data/archive/README-v1-ledger.md` for the one-page summary of what it
   established; cite it as history, never as the state of the fleet.
   The single exception is `data/mirror_baseline.csv`: a one-time frozen pre-lapse snapshot for the 7 live
   mirrors, read **only** by funding decisions.
   ⚠️ **`STATUS.md` does not exist yet** — regenerated in Phase 3. Until then `docs/current-state.md`
   carries the headline figures, and any `STATUS.md` line reference in a carried doc points into the old
   **archive folder**, not this one.
2. **Config**: capture files → `data/bots_config_v2.csv`. **Never hand-written, never memory-derived.**
   `data/bots_config.csv` (copied from v1) is the OLD hand-written record — proven wrong on 3 of 4 audited
   bots. It is retained for diffing only. Do not read a config fact from it.
3. **What a bot actually did**: the position's **Trades list**. The Exit Options panel is NEVER evidence —
   Exit Options are copied per-position at open; the panel shows intent, not execution.
4. The 7/27–29 forensics are the sanctioned correction layer.
5. **Narrative docs never carry numbers.** If a `.md` states a figure, the CSV wins.
6. On conflict between docs: `docs/phase1-kickoff-2026-07-30.md` and `docs/rebuild-audit-2026-07-29.md`
   govern — and **where those two disagree with each other, the kickoff wins** (it is later and records
   decisions Andy confirmed after the memo). Known instance: the memo's per-bot table lists champion PT25 as
   "attach-for-real vs drop — decide by test" (P1); the kickoff supersedes that — **PT25 is removed, decided,
   not open.** `docs/approach-reset-2026-07-29.md` is **DEMOTED** — authoritative diagnosis, superseded plan;
   its Part 3/5 is replaced by `docs/build-plan.md`.

## 4. Evidence law
Every claim carries a tier **T1–T5**. Nothing below T2 with **n≥100 positions / 6 months / a regime change**
supports a live-capital or growth decision. **Compare by R, never raw P/L.**

**Units — always label them; three different Exp(R) values for the same window otherwise circulate.**
`trades.csv` has **1,380 rows = 934 positions**. A row is a *leg* for two-legged spreads and a *whole
position* for `ironcondor` / `ironbutterfly` / debit-spread rows. **The unit of account is the POSITION
(a condor = its two spread rows paired by `trade_id`); risk = the larger side.** Exp(R) with no unit label
is untrustworthy: the champion's post-fix window is −2.5% per leg raw, −3.8% per condor raw, and
**−1.7% per condor ex-artifact** — the last is the one that means anything. Always write "per condor,
ex-artifact" or "per leg, raw".

Say **"positions"** or **"condors"**, never a bare count: the Fortress pre-June window is 30 *rows* and
21 *condors*; the champion's post-fix window is 47 *rows* and 29 *condors*. Both pairs describe the
same trades.
Detail: `docs/evidence-standards.md` (Phase 3; written to be revised — Andy wants a redesign pass).
Machinery — not verdicts — is inherited from `docs/independent-audit-2026-07-27*.md`: its tiers and sample
gates stand; its **kill-IC** verdict and its **custody-separation / independent-go-live-authority**
recommendations (audit §5.5 items 6–7) are **overruled/declined**. ⚠️ Corrected 2026-07-31: this
previously read "third-party-switch" — that meant the **go-live switch held by a third party**,
not a platform change. Reason: go-live authority stays with Andy; substitutes are external review
of `rules-of-engagement.md` + pre-registration. `docs/evidence-standards.md` §9.2.

## 5. Discipline rules
- **Pre-register before restart**: hypothesis, kill criterion, sample target, review date, config-capture hash.
  No entry in the ledger, no restart.
- **Refactor first (behavior-neutral), then change values.** Pilot on a dead bot; the champion goes last.
- **No changes during streaks.** Sizing set once at restart, never ad hoc.
- **Never reset OA history by cloning** — Symbols drop, history fragments, slots burn. Epoch boundaries live
  in `data/bots_meta.csv` + the local ledger.
- **Claude detects and instructs; Andy makes ALL OA edits.** Every edit is verified by opening the FIRST NEW
  POSITION after the fix and reading its **Trades list**. A fix unverified after one trading day is repeated
  at the top of every brief until closed.
- **Standing exception**: the legacy champion (`IC-SPX-FastPT25-S2`) and its `-130PM` clone are deliberately
  **Exit-Option-free ride+S2 controls**. Do not "fix" them, do not re-arm them. See §Day-0 in
  `docs/reactivation-runbook.md`.

## 6. File map (load on demand)
- `docs/current-state.md` — what is true right now. Read first.
- `docs/build-plan.md` — the adopted plan (supersedes approach-reset Part 3/5).
- `docs/reactivation-runbook.md` — Day-0 sequence. Read before the account comes back.
- `docs/phase1-kickoff-2026-07-30.md` · `docs/rebuild-audit-2026-07-29.md` — the governing pair.
- `docs/config-vs-reality-2026-07-28.md` · `docs/qqq-fortress-loss-forensic-2026-07-27.md` ·
  `docs/execution-audit-*.md` — the forensics / correction layer.
- `docs/oa-docs-research-2026-07-29.md` — what OA can and cannot express. Check before designing a mechanic.
- `docs/oa-capture-bookmarklet-2026-07-28.md` · `-coverage-2026-07-29.md` — the capture ritual.
- `docs/daily-review-design-2026-07-29.md` · `docs/instrumentation-decision-2026-07-29.md` — loop design.
- `docs/independent-audit-2026-07-27.md` + `-precommitment-ledger.md` — evidence machinery.
- `docs/directional-oa-build-sheet.md` — validated directional results + queue.
- `docs/strategy-taxonomy.md` · `docs/backtest-ingest-protocol.md` · `docs/cross-functional-reference.md`.
- `docs/oa-mirror-reference.md` (§3 evidence standards load-bearing) · `docs/ic-trailing-stop-backtest.md` ·
  `docs/oo-trial-backtests.md` · `docs/lean-backtesting-reference.md` ·
  `docs/quantconnect-lean-exploration-brief.md`.
- `docs/daily-loop-spec.md` — the daily-loop contract (three verdicts, never blended).
- `docs/evidence-standards.md` — tiers, both gate systems, the R methodology. **Written to be revised.**
- `docs/oa-platform-reference.md` · `docs/hedge-research.md` — the two v2 REWRITEs. Read the platform
  reference before designing any mechanic; it says what OA affirmatively cannot express.
- `docs/oa-ops-runbook.md` — how to touch the account: capture ritual, template versioning,
  group scheme, edit verification, and the nine traps. Read before any OA session.
- `docs/pre-registration-ledger.md` — template + drafted entries for all ≈18–20 active bots.
- **Not written yet** (do not go looking for them): `data/bots_config_v2.csv`,
  `data/mirror_baseline.csv`, `STATUS.md`. All are Phase 2–4 deliverables
  tracked in the `bot-fleet-migration` artifact (Andy's tracker, outside this folder).
- `data/archive/` — **frozen v1 ledger, never a reporting input.** `README-v1-ledger.md` first.
- `data/`: `bots_meta.csv` · `execution_audit.csv` — the **frozen 35-row detector
  validation fixture**, a test asset that survives the cutover, together with the two loss-side impossible
  fills T00147 and T00845 · `lessons.csv` · `raw/` · `brief/` (⚠️ both still hold pre-cutover data; Phase 3
  must filter by `LEDGER_START` or move them to `archive/`).

## 7. Build lanes
Cowork = strategy, ops, decisions, docs. Claude Code = code and VPS. **OA edits = Andy only.**

## 8. Archive pointer
`~/bot-fleet` — permanent READ-ONLY archive, git remote `chace2827/bot-fleet` (note: `.env` is NOT in the
backup). It holds: `docs/session-log.md` (the full narrative history), `docs/daily-ledger-archive.md`,
the Intraday Cockpit and reversal-scalp lane, `docs/pivot-vwap-research.md` + `docs/trigger-rules.md`
(deprioritized 7/03), superseded planning docs, `investor-profile.md`, `docs/_archive/`, and full git history.

It also holds **eight files marked REWRITE that were deliberately NOT carried in Phase 1** — they are still
needed, but only after correction, and none should be copied verbatim:
`oa-platform-reference.md` (its §14 "Conditional" definition is unbuildable on OA; Exit-Options-panel-as-
evidence is implicit throughout; needs the 8 new primitives folded in) · `ic-strategy-reference.md` (good IC
primer, wrong program description) · `hedge-research.md` (philosophy carries; every tournament ranking is
INVALIDATED) · `methodology.md` (silent on tiers) · `backlog.md` · `research-roadmap.md` ·
`rules-of-engagement.md` (strip TT3) · `north-star.md` (TT3-as-pillar line is wrong — Andy's edit, not
Claude's). If v2 seems to be missing a platform fact, it is probably in `oa-platform-reference.md` — read it
in the archive, distrust §14, and do not copy it over without the rewrite.
Never modify it. If v2 seems to be missing context, look there before assuming it never existed.

## 9. Communication & session continuity
Andy: direct, answer-first, concise. No filler.

### 9.1 The close-out sequence — every session, in this order
**Mandatory after any meaningful work.** Not once at the end of a long stretch of it — after
each piece, before starting the next.

1. Append `docs/session-log.md` (and update `docs/current-state.md` if a stated fact changed).
2. Update the `bot-fleet-migration` tracker artifact via `update_artifact`.
3. **Hand off for commit** — say "ready to commit" with a one-line summary of the changed
   files. **Andy runs the commit and confirms it. Claude does not commit.**

**Why commits moved to Andy (2026-07-31):** the device bridge cannot unlink files, so every git
operation from this side stranded `index.lock`, `HEAD.lock` and temp objects in `.git/` — each
one blocking Andy's next git command. Moving the commit to Andy removes that friction
permanently and puts the final check with the person who can see the result.

**Uncommitted work at session end is unfinished work.** A session that produced files but no
commit produced nothing durable — the folder is the only memory this project has, and an
untracked folder cannot be diffed, reverted, or trusted. Claude's obligation is to leave the
tree in a state Andy can commit in one command, and to say so plainly.

> ### ⛔ 9.1a — TOOL SUCCESS MESSAGES ARE NOT VERIFICATION
> A tool returning "updated" is a claim, not evidence. Neither is a stage-back read: the
> staleness seen on 2026-07-31 — **fresh metadata, stale content** — reproduced on a plain file
> in a separate session, so it is a caching defect in the verification channel. A stage-back
> can therefore be wrong in *either* direction and proves nothing on its own.
>
> **Files** verify by a direct device read or hash of the file itself.
> **The tracker artifact** verifies by **Andy's visual confirmation**, and that confirmation is
> part of the close-out — the close-out is not complete without it.
>
> Never report a write as landed on the strength of the tool call that made it. State what was
> attempted, state how it was checked, and if it was not checked, say so.

> **Failure record — this rule has now failed twice.**
> The 7/29 sessions skipped it entirely. On 2026-07-31 two governing documents
> (`oa-platform-reference.md`, `hedge-research.md`) were written and committed to disk with
> **no log entry and no tracker update** — leaving the tracker showing them `todo` while they
> sat complete in the folder.
> **The tracker is the one dashboard Andy reads. When it lags the folder it is worse than
> absent: it reports finished work as missing, and invites it to be done twice.**

### 9.2 "Stopped for review" means stopped
When a session says it is stopping for Andy's review, or Andy places a hold, **no further
writes happen** — no files, no edits, no "while I'm waiting" work — until Andy explicitly
releases the hold. A review checkpoint the session works past is not a checkpoint.

Work already in flight is finished, logged, committed, and *then* the session stops.
