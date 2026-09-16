# DISPATCH 3-CC — Sweep triage → fixes — foreman: Claude Code (terminal, Opus)

Launch: `cd ~/bot-fleet-v2 && claude --model opus` → paste:
"Read _dispatch-2026-08-19-3-triage-claudecode.md and execute it as foreman."

## 0. Mission
Convert the 08-18/19 PR-sweep's actionable findings into merged fixes and decision packages.
The sweep (58/58 slices, 804 distinct findings, $0) left, per its own foreman handoff:
- **130 likely-valid rows** — findings in files NOT touched by PRs #36–40 (start here),
- **175 re-verify rows** — findings in files that #36–40 changed (verify at current head),
- **47 manual-read rows** — need human-grade reading (yours),
- carried queue items: scanner self-flag re-check (check_refs selftest literal counted as
  dangling — re-check against current head, check_refs changed upstream); T-01 gitignore
  exemption (root todo CSV ignored); the PR #12 daily.sh idempotency verdict-split (ran-it=OK
  vs couldn't-run=UNVERIFIABLE — settle on the real tree, see §4.6).
Known-still-reproducing (foreman-confirmed 08-19): check_heartbeat holiday-blindness;
run_receipt.py:11 false-DANGLING. Top corroboration cluster: check_refs.py:181 (fixed
upstream), ci.yml:217, check_refs.py:39, check_heartbeat.py:18, pre_registration_ledger.py:39,
report.py:184, ci.yml:99, research_loop.py:809, gen_notes_cards.py:554.

You cannot read Cowork memory. Everything needed is in this file, the sweep outputs, the repo.

## 1. Locate the dataset — FIRST, before anything
Sweep outputs lived in `/private/tmp/pr-sweep/` (dies on reboot); durable copies were queued to
`~/Documents/fleet-runs/2026-08-19/`. Check both. If /tmp still exists, copy it to
~/Documents/fleet-runs/ immediately. **If neither exists, STOP and report to Andy** — do not
re-run the 58-slice sweep on your own initiative. The foreman's handoff state also lives in a
claude.ai artifact you cannot reach; Andy can export it if the disk copies are gone.

## 2. Ground rules
- **Never run git in write form against `~/bot-fleet-v2`; Andy runs every commit to the main
  tree** (§9.1 step 3). Git in your /tmp clones is unrestricted; that is how PRs ship.
- **Pre-flight every row's premise**: a finding is a claim, not evidence. Verify against
  `origin/master` at a pinned sha (fetch fresh, print it; the 08-18 pin went stale mid-run —
  record the pin per row, and re-verify survivors at head before publishing if it moves).
- **§9.1a**: agent claims verify by reading bytes; merges verify by fetching origin.
- **Class discipline — this is the whole job:**
  - **Class A (apply)**: mechanical fix; premise falsified/verified by a quotable line or a
    command's output; changes no guard predicate, no detector semantics, no decision.
    → write-fleet PR.
  - **Class C (package, never apply)**: anything that changes what a guard/detector
    accepts or rejects, adds/removes a check, or could change a verdict. → both readings
    written up for Andy, zero edits. **When ambiguous, it is Class C.**
  - **FIXED-UPSTREAM**: cite the fixing PR/commit + the line as it now stands.
  - **INVALID**: refutation evidence recorded.
- **A blocked agent returns to the ruling lane** — never widen a guard to unblock (recurred
  08-17 and 08-18; assume it recurs tonight). Kill on sight.
- Devin agents never touch `~/bot-fleet-v2`, `~/gitstore`, `~/.claude` — in every prompt.

## 3. The free Devin lane (condensed; identical to dispatch 1-CC §2 — read that file's §2 in
## the repo root for the full trap list, it applies verbatim)
`DEVIN=/Applications/Devin.app/.../windsurf/devin/bin/devin`; `"$DEVIN" -p --model swe-1-7 --
"<prompt>"`. Pin the model every attempt; NEVER `devin -r`; probe permission modes first;
read fleets use `--sandbox` + heredoc-only incremental append to out.txt (file-write tool is
rejected under sandbox); CAP 5; park-all on a mass 429 (resets escalate, parse min AND sec);
/tmp clones pinned to one printed sha, never worktrees; gitignored CSVs absent from clones —
stage read-only copies; warm-up run first; bash -c launcher; liveness via sessions.db
last_activity_at; per-batch cost assertion via response_dimensions model pin +
backend_type=windsurf; pilot one slice before each fan-out. **If `scripts/fleet/` (harness v1)
has merged by the time you run, use it instead of hand-rolling — that is what it is for.**

## 4. Protocol
1. **Verify fleet — 130 likely-valid rows.** Slice by file/workload (~10–15 rows per agent;
   cross-file rows run 2–3× — slice thinner). One read agent per slice at the pin:
   for each row output `row_id | REPRODUCED/REFUTED/UNVERIFIABLE | evidence` — evidence is a
   verbatim quoted line with path:line, or a command + its output; UNVERIFIABLE carries the
   reason and is never silently downgraded to code-reading. Incremental append, sentinel
   fallback ≥4 pipes.
2. **Foreman classification.** You (not agents) assign Class A / C / FIXED-UPSTREAM / INVALID
   per §2 to every REPRODUCED row. Spot-check ≥10% of agent verdicts by hand; escalate any
   split to Andy rather than adjudicating a guard-semantics question yourself.
3. **Build fleet — Class A batches.** Cluster Class A rows into coherent PRs (batch #2, #3 —
   e.g. the Reconciler + row-13 clusters already staged per the 08-18 handoff). One write-mode
   Devin agent per PR: `dangerous` WITHOUT sandbox + guardrails (push ONLY `devin/*` branches —
   the gh creds are ADMIN and a stray master push bypasses protection; `gh pr merge --auto
   --squash`; work only in the /tmp clone). Every PR body: the row ids, the pin, the quoted
   premise per fix. Post-batch foreman verification: origin/master moved only by expected
   merges; `git -C ~/bot-fleet-v2 status --porcelain` clean (terminal read is permitted).
4. **Re-verify fleet — 175 rows** against current head, same protocol as step 1; then classify
   (most will be FIXED-UPSTREAM — cite the PR) and fold survivors into step 3 batches.
5. **Manual 47** — read them yourself; classify; fold in.
6. **Carried items.** Scanner self-flag: re-run check_refs at head, one row. T-01: check the
   gitignore exemption claim by command. **PR #12 idempotency split: settle by running daily.sh
   twice in a /tmp CLONE with staged read-only copies of the needed CSVs — NEVER run daily.sh
   against the real tree for this** (build_ledger is a full destructive rebuild; the newest-file
   trap means a wrong input silently rebuilds from the wrong day).
7. **Class C packages.** Write `_class-c-packages-2026-08-19.md` (repo root, untracked): one
   entry per finding — the quoted premise, the failure it permits, BOTH candidate readings
   (fix vs leave-with-rationale), and what each changes about detector behavior. Include the
   two known-reproducing defects (check_heartbeat holiday-blindness, run_receipt false-
   DANGLING) and, if any row lands on them, the export-range guard and roster-uniqueness
   invariant — flag those two as time-sensitive for Andy.
8. **Outputs**: `~/Documents/fleet-runs/2026-08-19-triage/` — `triage-union.tsv` (row id,
   verdict, class, evidence, pin, disposition/PR), the Class C file, PR list. Copy the union
   into the repo root as `_triage-union-2026-08-19.tsv` so Cowork can read it over the mount.
9. **Close-out (§9.1)**: append `docs/session-log.md` (file edit only, no git on the live
   tree): PRs merged with ids, Class C count, spot-check results, anything killed and why.
   Say **"ready to commit."** New harness lessons → `_foreman-notes-<date>.md`.

## 5. Token thrift (Andy is short on Claude usage until Thursday)
Fleets run unattended — check at batch boundaries, never poll. Your turns go to:
classification, the 47 manual rows, PR review, the Class C write-ups. Everything mechanical
goes to Devin. Conservative branch + a written question beats deliberation.
