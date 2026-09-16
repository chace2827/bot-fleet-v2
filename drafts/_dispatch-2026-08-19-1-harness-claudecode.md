# DISPATCH 1-CC — Fleet Harness v1 — foreman: Claude Code (terminal, Opus)

Launch: `cd ~/bot-fleet-v2 && claude --model opus` → paste:
"Read _dispatch-2026-08-19-1-harness-claudecode.md and execute it as foreman."

## 0. Mission
Build **`scripts/fleet/` — harness v1**: the reusable runner/collector/assertion toolkit that
encodes every lesson from the 08-17→08-19 Devin fleet runs, so future fleets launch from one
command instead of a hand-built script. Devin (free local CLI) writes the code; you diff, merge,
pilot, and ship it as a PR. **Additive only** — new files under `scripts/fleet/` exclusively; if
any existing tracked file needs an edit, queue it for Andy, do not make it.

You cannot read Cowork memory. Everything you need is in this file plus the repo.

## 1. Ground rules (non-negotiable)
- **Never run git against `~/bot-fleet-v2` in write form. Andy runs every commit to the main
  tree** (CLAUDE.md §9.1 step 3). Git inside your own `/tmp` clones is unrestricted.
- **Never modify `~/bot-fleet-v2`, `~/gitstore`, or `~/.claude`** from any Devin agent. Every
  agent prompt carries this ban verbatim — a D2 agent overwrote `~/.claude/primer.md` on 08-18.
- **A tool/agent success message is not verification** (§9.1a). Files verify by sha256 + grep;
  merges verify by fetching origin and reading the ref; agent claims verify by reading the bytes.
- **A blocked instruction goes back to the ruling lane** — an agent that hits a CI guard never
  resolves it by widening the guard. Kill any agent that tries (happened 08-18, D5).
- **Decisions stay gated.** Nothing here touches build-plan, specs, sizing, kill criteria,
  pre-registration, go-live gates, or any existing guard predicate.

## 2. The free Devin lane — invocation + traps (all earned first-hand)
```bash
DEVIN=/Applications/Devin.app/Contents/Resources/app/extensions/windsurf/devin/bin/devin
"$DEVIN" -p --model swe-1-7 -- "prompt after a -- separator"
```
- **Pin `--model swe-1-7` on EVERY attempt** (the `-p` default is swe-1-7-medium; "lightning" is
  a PAID name collision). **NEVER `devin -r`** — resume silently falls back to the default model
  (proven 08-19; the warning text claiming otherwise is false). Every retry = fresh session,
  explicit pin.
- **Probe permission modes at session start** (`"$DEVIN" -p --help`) — `smart` was removed in an
  update; modes drift. Read fleets: `--sandbox` (forces autonomous; the FILE-WRITE TOOL is
  rejected under it — prompts must mandate **heredoc-only shell writes** to the agent's own cwd).
  Write fleets: `dangerous` WITHOUT sandbox + the guardrails in §5.
- **Cost/model assertion is mandatory per batch**: sessions.db `metadata.response_dimensions
  [uid=model].value` on the first logged turn (the `model` column is empty/untrustworthy);
  `backend_type=windsurf`; in-flight sessions carry NULL metadata — exclude and count; a session
  killed pre-finalisation has an unrecorded tier — name it, never fold into a pass. Fail loudly.
- **Rate limit is account-wide, message-based, and ESCALATES** (7 min → 22 → 29 under load).
  **CAP 5 concurrent for deep work** (6 survived a light run; nothing above ~12 total is safe;
  ~25–35 is proven fatal). On a mass trip: **park ALL workers for the full reset + buffer**;
  parse reset text in minutes AND seconds.
- **Workspaces: independent `/tmp` clones, never worktrees** (`git worktree add` writes into the
  live repo). Clone `origin/master` once with `--no-hardlinks`, `cp -R` per agent, **pin every
  clone to the same sha and print it**. Gitignored `*.csv` are absent from clones — stage
  read-only copies if a task needs them; agents report absence, never invent.
- **Output discipline**: append each result row to `out.txt` via heredoc THE MOMENT it is
  established (kills destroy batched output — proven, 4 runs lost); archive `out.partial.N.txt`
  before any retry truncates; success = rc==0 AND rows present; stdout `<<<ROWS…ROWS>>>` sentinel
  accepted only for rows with ≥4 pipes. `-p` buffers all stdout until exit — liveness via
  sessions.db `last_activity_at` (idle 5 min / age 30 min), per-attempt cap 90 min.
- **Warm-up**: first run after idle takes 30–60s — fire one throwaway first.
- **Launch via `bash -c`** (macOS: no setsid/timeout; zsh aborts on unmatched globs and does NOT
  word-split unquoted vars — foreman verification loops also run under `bash -c`). Verify
  `--model` survives into the final argv.
- **Prompt-specify the scratch root INSIDE each workspace** — silent prompts made agents default
  to shared /tmp paths; the sandbox rejection was the only thing preventing cross-contamination.
- **Pilot one slice after ANY harness change before fanning out.**
- **Pre-flight every premise** (docs/devin-queue.md discipline): run the command a claim names;
  base all work on `origin/master`, never the local working tree.

## 3. THE SPEC — scripts/fleet/ v1 (this section is shared with the Cowork variant)
Deliverables, each with `--selftest` (fixture-based, no network, no repo mutation):

1. **`runner.sh`** — queue manager. Manifest of slice-prompt files → launches attempts under
   `bash -c` with explicit `--model swe-1-7`, warm-up first, CAP default 5 (flag-tunable),
   per-attempt 90-min cap, retry = fresh session (never `-r`), archives partials before retry,
   escalation-aware 429 gate: parse reset (min AND sec), on mass trip park ALL workers and
   schedule relaunch after the gate expires. Read mode (`--sandbox`) default; `--write-fleet`
   flag switches to dangerous-no-sandbox and requires the write PREAMBLE.
2. **`collector.py`** — unions `out.txt` + `out.partial.*`, dedups, validates sentinel rows
   (≥4 pipes), emits `union.tsv` + per-slice status (COMPLETE / PARTIAL / ZERO-ROWS / KILLED);
   **MUT_PROOF gate**: any mutation-axis row without a `git diff --stat` proof, or with 0 files
   changed, is discarded, never a survivor.
3. **`assert_costs.py`** — sessions.db audit for a time-window/workspace: asserts
   backend_type=windsurf + first-turn response_dimensions model pin; carve-outs per §2; counts
   rate-limit casualties separately (not billing events); nonzero exit on any violation.
4. **`liveness.py`** — last_activity_at polling with the idle/age thresholds; prints stuck
   sessions for the runner to kill/retry.
5. **`PREAMBLE-read.md` / `PREAMBLE-write.md`** — versioned prompt preambles. Read: heredoc-only
   incremental append + file-write-tool prohibition + sentinel fallback + in-workspace
   scratch-root directive + seeder-deadlock note (seed_scratch_root.sh refuses in-repo, sandbox
   refuses out-of-workspace → use `FLEET_ROOT=<in-workspace scratch>` direct-drive) +
   "UNVERIFIABLE with reason, never silently downgraded to code-reading" + ~/.claude write ban +
   sed ban for mutations (aligned whitespace defeats anchored sed; python read/replace with
   `assert old in s`). Write adds: push ONLY `devin/*` branches, never master (creds are ADMIN
   and bypass protection); close via `gh pr merge --auto --squash`; work only inside the /tmp
   clone; never touch ~/bot-fleet-v2, ~/gitstore, ~/.claude.
6. **`README.md`** — operating defaults table (CAP, slicing by workload not file — RULINGS-style
   cross-file slices run 2–3×; ~15–20 checks/agent), the clone protocol, union-of-claims rule
   (N≥3 blind for extraction; 77–93% of findings are single-agent — never gate 2-of-3), the
   deepest-consumer question, pilot-before-fanout, and a dated lessons ledger.

**Salvage first**: `/private/tmp/pr-sweep/` (if it survived reboot) and
`~/Documents/fleet-runs/` may hold runner v5 + collector from the 08-18/19 sweep — use as the
starting point if present; copy anything found into the /tmp workspace before it dies.

## 4. Protocol
1. **Pre-flight**: probe modes; fetch origin in a /tmp clone; print pinned sha; salvage per §3.
2. **Write the spec file** for the builders: this §3 verbatim + the pinned sha + the salvage
   material paths (or "greenfield").
3. **Dual blind build**: two Devin write-mode-OFF builds (they only create files inside their own
   /tmp workspaces — read-fleet rules apply, sandbox on), D-A and D-B, same spec, no
   cross-visibility. Free, so let both run to completion.
4. **Foreman diff + merge**: pick the stronger base per component, graft the better ideas,
   note every disagreement in the PR description. Run all selftests yourself.
5. **Pilot**: a 2-slice trivial read fleet through the merged harness end-to-end. Must observe:
   warm-up fired; CAP honored; rows appended incrementally (check bytes mid-run); kill one slice
   deliberately mid-write and confirm the collector unions its partial; `assert_costs.py` passes
   with the pin; zero ACU. Unit-test the 429 parser against the verbatim reset strings (minutes
   and seconds variants) — don't try to trigger a real 429.
6. **Ship**: commit in your /tmp clone, push `devin/fleet-harness-v1`, `gh pr create`, CI green,
   `gh pr merge --auto --squash`. Verify per §9.1a: fetch origin, confirm master moved by exactly
   this merge and the local live tree is untouched (`git -C ~/bot-fleet-v2 status --porcelain`
   read from terminal is permitted — the mounted-tree git ban binds bridge sessions).
7. **Close-out (§9.1)**: append `docs/session-log.md` in the live tree (file edit only, no git);
   list the PR, the pilot evidence, and any queued edits to existing files; say **"ready to
   commit"** — Andy commits the log. Append new harness lessons to
   `_foreman-notes-<date>.md` (untracked) for Cowork to absorb into memory later.

## 5. Token thrift (Andy is short on Claude usage until Thursday)
The runner is autonomous — do not poll. Launch, then check at batch boundaries only. Spend your
own turns on: the spec, the merge-diff, the pilot readout, the PR. Delegate all reading/writing
volume to Devin. If you hit a judgment call the spec doesn't cover, write it down as a question
for Andy and take the conservative branch; do not burn turns deliberating.
