# DISPATCH 3-CW — Sweep triage → fixes — foreman: Opus in Cowork

Paste into a fresh Cowork chat in the bot-fleet-v2 project:
"Read _dispatch-2026-08-19-3-triage-cowork.md in the repo root and execute it as foreman."

## 0. Mission
Same as the Claude Code variant: turn the 08-18/19 PR-sweep's actionable rows — **130
likely-valid + 175 re-verify + 47 manual-read**, plus the carried queue items — into merged
Class A PRs and Class C decision packages. **The work definition, class discipline, and fleet
protocol live in `_dispatch-2026-08-19-3-triage-claudecode.md` (repo root) — §0, §2, and §4
apply verbatim. Do not fork them.** This file only defines how the Cowork lane executes, since
you cannot run the Devin CLI (Mac binary; device_bash is a Linux VM).

## 1. Read first
- Memory: `dispatch_2026-08-18_blocker_audit.md` (the sweep's state + morning order),
  `fleet_harness_lessons.md`, `devin_cli_promo_lane.md`, `devin_dispatch_discipline.md`,
  `cowork_git_commit_trap.md`, `roster_invariant_gap.md`, `session_2026-08-18_expedite.md`.
- The mounted-tree git ban is TOTAL for you including reads — verify merges via
  `$HOME/mnt/gitstore/bot-fleet-v2.git/logs/HEAD` + `packed-refs` (loose refs first), or a
  read-only clone in your cloud container (clone works, push 403s — deliver `.patch` files if
  a push lane is ever unavailable).

## 2. Protocol
1. **Dataset first.** The sweep outputs are NOT on the mount (`/private/tmp/pr-sweep/`,
   durable copies queued for `~/Documents/fleet-runs/2026-08-19/`). Get them one of two ways:
   ask Andy to `device_request_folder_access` grant `~/Documents/fleet-runs` (preferred), or
   have the launch script (below) copy the row files into
   `~/bot-fleet-v2/_fleet-runs/2026-08-19-triage/` where the mount reaches them. If the data
   is gone from both locations, STOP and report — never re-run the 58-slice sweep uninvited.
2. **Pre-flight.** Clone `origin/master` in the cloud container, pin + print the sha. Verify
   the premise of the carried queue items by command against the clone before writing any
   prompt on them.
3. **Author the dispatch pack** → land at `~/bot-fleet-v2/_fleet-dispatch/2026-08-19-triage/`
   via SendUserFile + device_commit_files, each file sha256+grep verified per §9.1a:
   - Slice prompt files for the **verify fleet** (130 rows, then 175), sliced by file/workload
     ~10–15 rows each, read-PREAMBLE rules baked in (sandbox, heredoc-only incremental append,
     `row_id | verdict | evidence` format, UNVERIFIABLE-with-reason, ~/.claude ban,
     in-workspace scratch root).
   - `launch.sh` — probes permission modes, /tmp clone at the pin, stages read-only copies of
     gitignored CSVs any slice needs, warm-up, CAP 5 queue with park-all-on-429, model pinned
     `swe-1-7` every attempt (never `-r`), tees results into
     `~/bot-fleet-v2/_fleet-runs/2026-08-19-triage/`. If harness v1 (`scripts/fleet/`) has
     merged, launch.sh just drives it.
   - Later, after classification: **write-fleet prompts** for the Class A batch PRs
     (dangerous, no sandbox, devin/*-only push, auto-squash-merge, row ids + quoted premise
     per fix in the PR body).
4. **Launch** = one pasted line for Andy per batch (`bash …/launch.sh`). *Mode B optional:*
   drive Terminal via computer-use if Andy grants access; fall back to paste on any friction.
5. **Classify yourself** (this is the judgment core and stays in your lane): read the union
   from `_fleet-runs/` over the mount, assign Class A / C / FIXED-UPSTREAM / INVALID per the
   CC file §2, spot-check ≥10% of agent verdicts against your cloud clone, escalate splits to
   Andy. **The 47 manual-read rows are yours** — read them in the clone directly.
6. **Class C packages**: write `_class-c-packages-2026-08-19.md` to the repo root (both
   readings per finding, zero edits applied), flagging the export-range guard and the
   roster-uniqueness invariant as time-sensitive if touched. Deliver via device_commit_files,
   sha-verify.
7. **Verify every merged PR** from gitstore refs or a fresh container clone: master moved only
   by expected merges, CI green, and each PR's diff matches its claimed rows.
8. **Close-out (§9.1)**: append `docs/session-log.md` (device tools, sha-verified), update the
   migration tracker artifact with per-row cited evidence (PR ids, shas, row counts), say
   **"ready to commit."** Write new lessons to project memory — your lane's advantage.

## 3. Hard rules
- Agents never touch `~/bot-fleet-v2`, `~/gitstore`, `~/.claude`; a blocked agent returns to
  the ruling lane, never widens a guard; ambiguous class = Class C; commit window = write
  freeze; no number without its source file.
- **Never let anything run `daily.sh` outside a /tmp clone with staged copies** — full
  destructive rebuild + newest-file input trap (CC file §4.6).
- Token thrift: Andy is short on Claude usage until Thursday. Author once, launch once per
  batch, judge at boundaries. Classification and the 47 manual rows are where your tokens go;
  everything mechanical is Devin's.
