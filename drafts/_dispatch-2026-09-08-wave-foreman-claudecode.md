# WAVE FOREMAN — 2026-09-08 — Opus, Claude Code, in ~/bot-fleet-v2 (NOT Cowork: needs ~/0dte-day-taxonomy and the devin-free wrapper)

Paste into a new Opus Claude Code session started in `~/bot-fleet-v2`:
"Read `drafts/_dispatch-2026-09-08-wave-foreman-claudecode.md` and execute it. Andy launches the
dispatcher himself in a plain Terminal tab; you build, verify, and foreman. Never run git
commit/push on master; never edit ~/.config/devin/config.json; never dispatch via the Devin MCP
(no model pin) or raw `devin` (not free) — the `devin-free` wrapper is the ONLY route."

Ruling: `R-2026-09-07-DEVIN-WAVE-SCOPE`. Lane specs: `drafts/_wave-2026-09-08-lanes.md` (six lanes)
+ `drafts/_dispatch-2026-09-03-t44-g4-caps.md` (lane 1 full spec). Promo dies 2026-09-16.

## 0 · Read before building (the machine already exists; do not re-derive it)
- `~/0dte-day-taxonomy/prompts/foreman-2026-09-01.md` — cost law, receipts protocol, validate/merge.
- `~/0dte-day-taxonomy/workers/dispatch.sh` — cap 4, 8 s stagger, append-only wave.log, per-lane
  dispatch.log, 60-min timeout. COPY and adapt; do not point it at gitstore.
- Wrapper form (verified): `devin-free --workspace DIR --permission-mode dangerous -- "prompt"`.
  Prompt is POSITIONAL after `--`. No --prompt-file. The wrapper refuses --model/-r/--resume/--config
  and refuses `~/gitstore` workspaces — so every lane gets its OWN fresh clone from origin, e.g.
  `~/waves/2026-09-08/<lane>/bot-fleet-v2`, never the mounted repo (its .git is a gitfile into gitstore).
- Workspace trust: the working config key is `skip_workspace_trust: true` in a PER-RUN config
  copied into the workspace (never the global file) — `drafts/_foreman-notes-2026-08-19.md` TRAP 1.
- Receipts: per-session `resolved_model_uid=swe-1-7` in `~/.local/share/devin/cli/logs` + the
  wrapper provenance line. There is NO acu field in CLI logs. Billing surface = Andy's before/after
  Devin balance snapshot (delta must be 0). Ask Andy for the BEFORE snapshot in your first message.
- Rate limit escalates → cap stays 4 (`fleet_harness_lessons`). Never `devin -r` on a pin.
  Heredoc-only incremental append. Each clone is the isolation boundary — agents must not write
  outside it ($HOME clobber gap: two agents wrote ~/.claude/primer.md on 08-31).

## 1 · Build (≈30 min, all on disk, nothing dispatched)
1. `mkdir -p ~/waves/2026-09-08`; for each of the six lanes clone origin/master fresh into
   `~/waves/2026-09-08/<lane>/bot-fleet-v2` and `git checkout -b <lane>` (lanes: t44-g4-caps,
   t45-export-range-guard, t46-catchup-capture, t43-manifest-selftest-ci, t03-ledger-regression,
   t47-s24-freeze). Record each clone's head sha in `~/waves/2026-09-08/wave.log` header.
2. Write six lane prompt files `~/waves/2026-09-08/prompts/<lane>.md`: the common pre-flight +
   acceptance block from `_wave-2026-09-08-lanes.md`, then that lane's section verbatim, then the
   closing contract: "open a PR against origin/master titled `<T-id>: <one line>`; PR body = head
   sha, red run, green run, the independent derivation the spec asks for, `Andy merges`; update
   data/portfolio.csv <T-id> status → Ready for review with the PR number; never touch master;
   never run any OA/browser tool; stop and write STOP-<reason>.md in the workspace root if a
   premise is false." Lane 1's prompt body is `_dispatch-2026-09-03-t44-g4-caps.md` verbatim.
3. Copy dispatch.sh → `~/waves/2026-09-08/dispatch.sh`, edit only: LANES list, workspace paths,
   prompt-file → positional-prompt read, per-run config with `skip_workspace_trust`. Keep cap 4,
   stagger, timeout, append-only logs.
4. PREFLIGHT GATES (all must pass; print a table): each clone clean at the recorded sha; each
   prompt file cites the spec's line premises; `which devin-free` resolves to the v2 wrapper
   (`3479939d…` per devin_cost_guard — recompute and compare); the dry-run flag of the wrapper (if
   any) or `--help` shows no model override; six workspaces, six prompts, zero overlap in files
   touched between lanes 2/3/4 (they all touch close/ingest — state the file lists side by side and
   confirm disjoint, else serialize lanes 3 and 4 after 2).
5. Print the ONE line Andy pastes: `bash ~/waves/2026-09-08/dispatch.sh`. Then STOP and wait.

## 2 · Foreman (after Andy launches; poll, don't spawn)
- Poll `wave.log` every few minutes; per lane, on completion: verify the receipt (model uid line),
  `git -C <clone> log --oneline -5`, the PR exists via `gh pr view`, phase0 status via
  `gh pr checks`. A lane with no PR after 60 min = read its dispatch.log, classify (stale premise /
  rate limit / refusal), record, do NOT relaunch without Andy.
- For each PR: read the diff yourself against the spec's acceptance predicates. Confirm the red run
  is real (a predicate never seen red is not a predicate). Confirm no file outside the lane's stated
  set changed. Confirm no CSV gained a column, LF endings. Post a review comment "FOREMAN: <verdict>"
  with the checklist. You do not merge — Andy merges.
- Lanes 2 and 3 both change close-path files: if both PRs are green, note the merge ORDER (2 then 3)
  and whether 3 needs a rebase after 2 merges.
- End-of-wave report `~/waves/2026-09-08/REPORT.md` and appended to `docs/session-log.md` in the
  mounted repo (that one file only; Andy commits): per lane — PR #, sha, verdict, receipt, minutes;
  balance delta (from Andy's two snapshots); anything that should go in the runbook.

## 3 · Do not
No OA. No git on the mounted repo except appending session-log.md. No global Devin config edits.
No relaunches, no cap changes, no extra lanes. If the wrapper refuses free mode at any point,
STOP the whole wave and report — a paid lane is not a free wave.
