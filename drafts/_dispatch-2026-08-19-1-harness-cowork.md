# DISPATCH 1-CW — Fleet Harness v1 — foreman: Opus in Cowork

Paste into a fresh Cowork chat in the bot-fleet-v2 project:
"Read _dispatch-2026-08-19-1-harness-cowork.md in the repo root and execute it as foreman."

## 0. Mission
Same deliverable as the Claude Code variant: **`scripts/fleet/` harness v1**, built by free
Devin CLI agents, shipped as a `devin/fleet-harness-v1` PR. You are the foreman, but you cannot
run the Devin CLI — it lives on the Mac (`/Applications/Devin.app/.../bin/devin`), and
`device_bash` is a Linux VM without it. So your job splits: **you prepare everything and verify
everything; Andy (or computer-use, Mode B) fires each launch with one pasted command.**

## 1. Read first
- Memory: `fleet_harness_lessons.md`, `devin_cli_promo_lane.md`, `cowork_git_commit_trap.md`,
  `devin_dispatch_discipline.md`.
- **The build spec is `_dispatch-2026-08-19-1-harness-claudecode.md` §3 in the repo root — use
  it verbatim. Do not fork the spec**; if you find a defect in it, fix it in that file (it is
  untracked scratch) so both lanes stay on one spec.
- CLAUDE.md §9.1/§9.1a govern close-out and verification. The mounted-tree git ban is TOTAL for
  you, including read-only commands — verify commits/merges by reading
  `$HOME/mnt/gitstore/bot-fleet-v2.git/logs/HEAD` and `packed-refs` (loose refs first, then
  packed — a stale packed line silently gives the pre-commit sha), or by cloning the repo
  read-only in your cloud container (clone works; push is 403 — never promise a push).

## 2. Protocol
1. **Pre-flight**: clone `origin/master` in your cloud container; pin + record the sha. Verify
   the spec file exists on the mount; verify each spec premise you rely on against the clone
   (a queue item is a claim, not evidence).
2. **Author the dispatch pack** in the cloud workspace, then land it on the mount at
   `~/bot-fleet-v2/_fleet-dispatch/2026-08-19-harness/` via SendUserFile + device_commit_files
   (verify each file per §9.1a: `device_bash` sha256 + single-match grep — never trust the tool
   response or a stage-back read). Contents:
   - `spec.md` — the §3 spec + pinned sha + salvage-paths note.
   - `builder-A.prompt` / `builder-B.prompt` — the two blind build prompts (read-fleet
     PREAMBLE rules from memory baked in: heredoc-only writes, sandbox, ~/.claude ban,
     in-workspace scratch root, incremental append).
   - `launch.sh` — one script Andy runs in Terminal: probes permission modes, makes the /tmp
     clone at the pin, salvages `/private/tmp/pr-sweep` + `~/Documents/fleet-runs` runner-v5
     material, warm-up run, launches A and B under `bash -c` with explicit `--model swe-1-7`,
     CAP 2 (only two builders), and **tees all agent output + workspace results into
     `~/bot-fleet-v2/_fleet-runs/2026-08-19-harness/`** so you can read it over the mount.
   - `verify.sh` — post-build: run all `--selftest`s in the merged candidate, print shas.
3. **Launch**: hand Andy exactly one line — `bash ~/bot-fleet-v2/_fleet-dispatch/2026-08-19-harness/launch.sh`.
   *Mode B (optional, only if Andy approves):* drive Terminal yourself via computer-use
   (`computer_resolve_access` → `computer_request_access` for Terminal on macbookpro). If access
   is declined or flaky, fall back to paste-to-Andy — do not retry-loop.
4. **Monitor** via `_fleet-runs/` on the mount at batch boundaries only (the builders take a
   while; do not poll — schedule a check-in instead of burning turns).
5. **Merge**: stage both builds' outputs into your cloud clone, diff, compose the final
   `scripts/fleet/` yourself (this is the judgment step and it is yours), run the selftests in
   the container, then hand the result back two ways: (a) preferred — a third Devin write-mode
   dispatch prompt (dangerous, no sandbox, devin/*-branch guardrails from memory) that applies
   your composed diff verbatim, pushes `devin/fleet-harness-v1`, opens the PR with auto-merge;
   Andy launches it with one line; (b) fallback — `git format-patch` from your clone, verified
   with `git apply --check`, delivered via SendUserFile for Andy to apply and push.
6. **Pilot before declaring done**: the 2-slice pilot from spec §4.5 runs on the Mac — include
   it in `verify.sh`/the write-dispatch, and judge its outputs from `_fleet-runs/`. A merged PR
   without pilot evidence is not done.
7. **Verify the merge** from gitstore refs (loose then packed) or a fresh container clone —
   master moved by exactly the expected merge, CI green.
8. **Close-out (§9.1)**: append `docs/session-log.md` (edit via device tools, sha-verify),
   update the migration tracker artifact with per-row cited evidence (PR id, shas), say
   **"ready to commit"** with the changed-file list. Save any new lessons to project memory
   (that is your lane's advantage — Claude Code cannot).

## 3. Hard rules
- Devin agents never touch `~/bot-fleet-v2`, `~/gitstore`, `~/.claude` — in every prompt.
- Additive only: new files under `scripts/fleet/`; edits to existing tracked files are queued
  for Andy, never made.
- A blocked agent goes back to the ruling lane; a guard is never widened to unblock work.
- Commit window = write freeze: when Andy says he's committing, stop, post final hashes, queue.
- Token thrift: Andy is short on Claude usage until Thursday. Author once, launch, judge at
  boundaries. No narration, no polling.
