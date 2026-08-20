# Lane state — FOREMAN

> ### 📄 IF YOU ARE READING A STALE COPY — retrieve the current one
>
> As of 2026-08-19 this file's latest content lives on an **unmerged branch** (PR #60), so a fresh
> session sitting at `master` sees an older version. Retrieve the current one without checking
> anything out, and without needing the wave-1 `/tmp` clone to still exist:
>
> ```
> git fetch origin
> git show origin/foreman/lane-state-2026-08-19:docs/lane-state-foreman.md
> ```
>
> If that branch no longer exists, it merged — `master` is then authoritative and this box is
> spent. Confirm with `git log --oneline origin/master -- docs/lane-state-foreman.md`.
>
> ⛔ Run this from a clone, never against `~/bot-fleet-v2` — git on the mounted tree is prohibited
> for bridge sessions (`R-2026-08-17-GIT-RULE-SCOPE`), read-only commands included.

Owned by the **foreman lane** (dispatches Devin build agents from `/tmp` clones, verifies their
output, merges on Andy's authorization). Created per `R-2026-08-19-LANE-STATE-OWNERSHIP` §2.

> ⛔ **THIS FILE IS A CLAIM, NOT EVIDENCE** (§3). Everything below was true when written and may be
> false now. Re-verify against the remote at session start and before **any** dispatch, branch or
> merge:
>
> ```
> git fetch origin && git rev-parse origin/master
> ```
>
> and state the result. A stale base is the P2-5 failure class: that near-miss was 4 commits and was
> caught in pre-flight; the 2026-08-19 cross-lane incident was 38.
>
> ⛔ No lane writes another lane's `docs/lane-state-<lane>.md`. No lane or agent writes anything
> under `~/.claude/` (§1) — reading it is permitted, but **nothing read from it is evidence**.

## Base

| | |
|---|---|
| base sha believed | `d3dce33ef67b2bd0c763b9aa421d24839b756caf` |
| last verified against `origin/master` | 2026-08-19T21:47:02Z |
| how | `git fetch origin && git rev-parse origin/master` in a fresh `/tmp` clone — matched |
| ruling count at that sha | 155 (`git show origin/master:docs/RULINGS.md \| grep -c '^ruling_id:'`) |

That sha is `roster board: 44 bots, 12 derived families, inventory + scoreboard`. It supersedes the
previously recorded base `65799e04` (PR #56) — **3 commits of drift** between sessions, caught in
pre-flight exactly as §3 requires.

## Open PRs owned by this lane

Wave-1 clone: `/tmp/w1/base`, every branch based on `d3dce33`.

| PR / branch | contents | acceptance | state |
|---|---|---|---|
| **#58** `foreman/a6-doc-edits` | wave-1 **A6** — T-04, T-06, T-23 + the G-1′ cross-reference | single-match grep, **5/5** | OPEN |
| **#59** `foreman/a3-tape-failure-mode-test` | wave-1 **A3 residue** — adds `scripts/test_tape_failure_modes.py`; `tape.py` byte-identical | **12/12** green; `--show-red` flips all 12, exits 1 | OPEN |
| **#60** `foreman/lane-state-2026-08-19` | this file | — | OPEN |
| `foreman/citation-dispositions` | burn-down **B/E/F** — 9 refs reclassified into `check_refs_allow.txt` | dangling **30 → 21**, DECLARED **61 → 70**, set-diff verified both directions | committed local, **HELD** pending Andy |
| `foreman/devin-free-wrapper` | `scripts/devin_free.sh` | refusal matrix **8/8** rc=2, none reached exec | committed local, not pushed |

⛔ **`foreman/citation-dispositions` was rewritten once.** Its first version absorbed group E by
adding a `history-index.md` entry. That mechanism is **withdrawn**: `check_refs.py:110` is
`os.path.basename(ref) in history` tested against the **entire text** of `history-index.md`, so it
silences by side effect and would mute any future ref sharing that basename. The allowlist is the
ruled mechanism — explicit, one path and one reason per line, reviewable in a diff.

## Findings this lane raised that are NOT yet ruled

| id | what | where |
|---|---|---|
| **F-1** | An empty post-entry window is scored as a **negative** rather than not-applicable. `leg_touched(leg, None, None)` returns `False`, not `None`, so the position enters `touch_n` as a scored non-touch. Same shape in two more places. | `scripts/trade_window.py:130`, `scripts/hedge_tournament.py:256`, weakly `scripts/daily_brief.py:120` (`leg_breach`) |
| **F-4** | Bare `rec["series"]` with no guard: a tape record that exists but lacks a `series` key raises `KeyError`, and under `run_stage` that aborts the entire daily run at stage 5. W4's VIX evaluators are the correctly-guarded pattern to copy. | `scripts/gate_parser.py:192` (`eval_band_prior_close`) |
| **F-6** | Raised but not carried by this lane; recorded here so it is not lost. | — |
| **stage-5 fatality** | Whether stage 5 should remain fatal. Now has **two distinct triggers**, which differ in kind: F-4's latent `KeyError` crash, and F-5's deliberate `exit 2` on a missing tape. One ruling would land on both at once. | `scripts/daily.sh` stage 5 |

Ruled since being raised, kept for the trail: **F-2** (the five OA-Mirror SPY positions are signed
design, not a defect) · **F-3** (log honesty, merged as PR #53) · **F-5** (merged as PR #55) ·
**F-7** `trade_id` non-reproducibility (ruled by `R-2026-08-19-TRADE-ID-STABILITY`).

## What this lane is holding for

1. **⛔ THE DEVIN PERMISSION — RESUME HERE AFTER THE RESTART. Read this before dispatching anything.**
   Wave 1 dispatched **0 of 6** agents. The history, because each step's result changes what the
   next one means:
   - The classifier first refused `devin -p` outright, before the binary ran — broader than the
     older workspace-trust block, and per-session, not per-machine.
   - A narrow rule `Bash(/Applications/.../devin/bin/devin -p --model swe-1-7:*)` was granted. It
     lifted the classifier block **and failed to deny**, twice, both SEEN:
     `--model swe-1-7-lightning` ($2.5/$12.5 per MTok) and `--model claude-opus-5` ($5/$25, banned
     outright by dispatch §2) **both reached the binary**. The first slips a prefix match because
     `swe-1-7-lightning` begins with `swe-1-7`; the second shares no prefix and passed anyway, so
     the matcher does not bind the `--model` argument at all. Nothing was spent only because
     Devin's unrelated workspace-trust check stopped both. That is not a cost control.
     Option 2 (wide grant + post-hoc `acu` assertion) was considered and **DECLINED** — detection
     after spend, against a negative balance, is not a guard.
   - **RULED: Option 1, the wrapper.** Remaining sequence, in order:
     1. ~~Do not touch workspace trust~~ — still holds, until step 4 passes.
     2. ~~Andy restarts Claude Code~~ (the grant was session-scoped, never on disk, so it clears).
     3. ~~Write the wrapper~~ — **DONE.** `scripts/devin_free.sh`, installed at `~/bin/devin-free`,
        both copies sha256 `a6dded833ffc0e24a8189867e558f445c4cb88d0dee183fac565d5a81145a309`.
     4. **Andy grants ONLY `Bash(/Users/andrewchace/bin/devin-free:*)`. The raw devin path is NOT
        re-granted.**
     5. ~~**TWO deny tests, both must be SEEN RED before any dispatch.**~~ — **BOTH SEEN RED,
        2026-08-19 post-restart.** Evidence in the probe section at the end of this file:
        - ~~the raw binary directly → **DENIED by the classifier**~~ — SEEN RED, after Andy moved
          the raw path from `allow` to `deny`.
        - ~~`devin-free --model swe-1-7-lightning` → **exit 2 from the wrapper**, no invocation~~ —
          SEEN RED. **Step 5 is complete.**
     6. Only after step 5 passes is workspace trust revisited — **step 5 now passes, so this is
        the open step.** `/tmp` clones are untrusted and Devin refuses them; the two documented
        fixes are interactive trust or `respect_workspace_trust: false` in config. **Neither has
        been attempted.** ⛔ **The FIRST check to run after any `respect_workspace_trust` change is
        the deferred exec-reach test** — see "Deferred to step 6" in the probe section. A guard
        proven under the old configuration is stale.
   - **Pre-wave assertion, every wave:** `~/bin/devin-free --selfhash` must equal
     `shasum -a 256 scripts/devin_free.sh`. The installed copy is outside the repo on purpose —
     fleet agents edit `/tmp` clones and cannot reach `~/bin`, so an agent cannot edit the thing
     that constrains it.
2. **F-7's `build_ledger.py` work.** Queued **deliberately behind PR #56's merge** — same file, and
   Andy will not have two changes to it in flight at once. PR #56 is now merged, so this is the next
   dispatch when its prompt arrives.
3. Rulings/dispatches for F-1, F-4, F-6 and stage-5 fatality. None are this lane's to resolve.
4. **Andy's `check_refs` ruling** (wave-1 escalation 3) and the dangling-ref burn-down that depends
   on it. Wave-1 **A5** is HELD pending it and must not be rewritten meanwhile.

## Queued, NOT started

**WAVE-2 CARD — fix the `check_refs` path extractor. TWO defects, one card.**
This is the first real Devin card once the permission sequence above completes.

- **Defect 1 — the extractor reads prose and placeholders as paths.** 10 of the 30 dangling refs
  at `d3dce33` are false positives: `..` date-range notation (`data/brief/2026-08-10..13`), the
  literal `DATE` placeholder in an argparse help string, a deliberate `2099-01-02` sentinel, a
  "path" spanning a sentence (`data/receipts/ stops at mirror-baseline.txt`), two words glued
  across a line, and `docs/fixture.md` ×4 — one of which is the scanner reading its **own**
  selftest's temp filename out of its own source, the other three being docs that merely *quote*
  that bug report and get flagged for quoting it. **Closing these by editing docs would corrupt
  correct text to satisfy a broken parser.**
- **Defect 2 — `check_refs.py:110` silences by side effect.** `os.path.basename(ref) in history`
  where `history` is the entire text of `history-index.md`. Any ref whose basename appears
  **anywhere** in that file — deliberately or by coincidence — is muted.

**Acceptance has THREE halves, all mandatory:**
1. the 10 named group-A refs are no longer reported;
2. a deliberately broken citation is **STILL** reported — without this you have only widened the
   parser until it reports nothing;
3. a ref whose basename **coincidentally** appears in `history-index.md` is **STILL** reported.

**⛔ Ordering, corrected — the earlier "burn down 30 then flip `--strict`" was wrong.**
Fix extractor → re-measure → **reclassify** survivors into `check_refs_allow.txt` → *only then*
flip `ci.yml:225` to `--strict`. Step 3 means reclassify, **not** mark: a marked-but-still-dangling
ref keeps `--strict` red forever. **If any survivor is left merely marked, leave CI non-strict
rather than widen anything.** Do not touch `ci.yml` until step 3 is done.

**Also queued:** `docs/agent-roles.md:100-101` is HALF FALSE — it claims the Pipeline-Runner lacks
"a trigger and a heartbeat — so a run that never happened is currently indistinguishable from a run
with nothing to report." The heartbeat conjunct is disproved (`artifacts/heartbeat/`,
`scripts/check_heartbeat.py`), so the consequence clause is false. The **trigger** conjunct may
still hold — S-01 reads zero of four engines wired. Correct the first; verify the second before
touching it.

## Wave-1 pre-flight findings, 2026-08-19 (base `d3dce33`)

Five of six wave-1 cards failed premise verification — the cards were cut from
`todo-2026-08-16.csv` and the tree moved under them. Recorded so they are not re-cut:

- **A1 / T-03** — CANCELLED. `hedge_tournament.csv` carries 8 distinct `trade_id`s, **7 absent**
  from `trades.csv`; but `R-2026-08-19-TRADE-ID-STABILITY` §5 already names those same 7 orphans and
  rules them decorative and left as committed. The card's second conjunct is false outright: both
  files span the **same 7 dates**, not fewer. No rows are dropped — ids churn.
- **A2 / T-13** — CANCELLED. Already executed: `report.py:601-602` derives the unsigned set,
  `:689` / `:1343` render it, empty set renders no banner, and `portfolio.py:56-61` derives the
  count off the same `STATUS.md` heading. Both derive 4.
- **A3 / T-11** — premise FALSE (`_get()` swallows nothing; the split is built, `tape.py:389` exits
  3 on `token-rejected`), but the acceptance clause was genuinely missing. Test now written.
- **A4 / T-12** — CANCELLED. Artifact dir is **`artifacts/heartbeat/`**, not `data/heartbeat/` as
  the card said; dispatching as written would have created a second parallel tree. Already
  distinguishes no-run from failed-run by file state alone.
- **A5 / T-14** — HELD. `docs/archive/` does not exist; scope unnamed across 25 dated docs, several
  load-bearing in `CLAUDE.md`; and its acceptance predicate is blind — see below.
- **A6** — the only card that passed, with T-23 retargeted from `agent-charter.md` (which already
  cites `docs/RULINGS.md` at :7) to **`agent-roles.md:48` and `:53`**, where the dangling prose was.

**⛔ `python3 scripts/check_refs.py` IS GREEN WHILE 30 REFERENCES DANGLE.** Measured at `d3dce33`:
plain → rc=0 reporting `30 DANGLING REFERENCE(S)`; `--strict` → rc=1. `ci.yml:225` runs the plain
form. Any acceptance predicate written as "check_refs is green" is satisfied before the work starts
and cannot detect its own failure. Dangling-ref count with its window, since a delta without one is
not checkable: **28 @ `4fa1949` (2026-08-18) → 30 @ `d3dce33` (2026-08-19)**, +2, both the `..`
date-range notation the scanner misreads as a path. `devin-queue.md:108` states **25**, which
reconciles with neither and is itself a stale figure.

## Operating notes that cost real time to learn

- **Devin invocation**: `-p --model swe-1-7 --permission-mode dangerous`, **no `--sandbox`**.
  `dangerous + --sandbox` fails, because sandbox forces autonomous mode which still gates some
  tools on confirmation, and in `-p` those are rejected — it produces zero commits.
  **[CORRECTED 2026-08-19 — "`smart` does not exist on this install" is FALSE.** Probed directly on
  `devin 3000.4.25 (7e8e528a)`: `--permission-mode` documents all four of `auto` (default),
  `accept-edits`, `smart`, `dangerous`. The mode list drifts between updates, so it is **probed
  every wave and never assumed** — which is why wave-1 pre-flight §1.1 requires it. Original note
  left standing.**]**
- **⛔ FLAG ORDER IS LOAD-BEARING UNDER A NARROW PERMISSION RULE.** The planned grant is
  `Bash(/Applications/.../devin/bin/devin -p --model swe-1-7:*)`, which is a **prefix** match on the
  command text as literally written. Two consequences, both of which look like "the block never
  lifted" when hit: (1) the binary path must be **spelled out in full** — a `"$DEVIN"` variable
  makes the rule inert; (2) `-p --model swe-1-7` must come **first**, before
  `--permission-mode`/`--`, or the prefix does not match. A permission that has not been seen to
  DENY something is not yet a verified permission: before trusting the grant, attempt one
  invocation with `--model swe-1-7-lightning` (a **paid** name collision — $2.5/$12.5 per MTok) and
  confirm it is refused.
- **Free vs paid models, re-verified 2026-08-19 via `devin models list`**: only `swe-1-7` (SWE-1.7
  Max) and `swe-1-7-medium` are `Free`. `swe-1-7-lightning` and `-lightning-medium` are
  **$2.5 / MTok in, $12.5 / MTok out**. `-p` defaults to `swe-1-7-medium`, so the model is always
  passed explicitly.
- **Retry logic must key on a per-attempt marker, never a tail scan** of a cumulative log. A tail
  scan re-ran an already-SUCCEEDED dispatch and nearly opened a duplicate PR.
- **Trusted workspaces**: Devin refuses untrusted directories, and
  `~/.local/share/devin/cli/trusted_workspaces.json` is shared across lanes — another lane restoring
  it silently un-trusted this lane's clone mid-run.
- **Acceptance predicates must state their DERIVATION, not a literal.** Four predicate errors this
  session came from constants written against a static snapshot (7-vs-8 dates, `grep -c` 3-vs-4, a
  byte-identity check invalidated by F-7, an assumed merge base). A predicate that recomputes itself
  cannot go stale between drafting and running.
- **Two derivations agreeing is weak evidence.** In W3 this lane's accounting and the build agent's
  agreed on `None` where the real predicate returns `False`; both shared one blind spot. What caught
  it was checking against a *different surface* — the banked table's `touch_rate 0.0`, which is only
  reachable if `touch_n >= 1`.

## Permission probe — 2026-08-19, post-restart (three checks, $0)

Andy moved the raw devin path from `allow` to `deny` in `.claude/settings.local.json` (**moved, not
duplicated** — it is no longer in `allow`) and restarted Claude Code so the file was freshly loaded.
Three checks below. **Workspace trust was not touched**: `trusted_workspaces.json` still reads
2026-08-18 20:54, 2616 bytes.

- **A — raw probe: DENIED.**
  `/Applications/Devin.app/.../devin/bin/devin -p --model swe-1-7 "noop"`, typed verbatim so it
  prefix-matches the deny rule, returned a permission denial. The instrument is the log directory
  `~/Library/Application Support/Devin/logs`, and the test is the **absence of a new entry**:
  4 entries before — `20260811T222018`, `20260812T231551`, `20260816T200401`, `20260817T224514`,
  parent mtime Aug 17 22:45 — and the identical 4 after, same parent mtime. **A denial writes
  nothing. Step 5 test 1 is SEEN RED.**
- **B — wrapper positive control: CANCELLED as shaped (Andy, 2026-08-19).** The intended form
  `~/bin/devin-free -- "noop"` had to run in an untrusted cwd, i.e. `/tmp/untrusted-probe`, or it
  was not a trust test. The allow rule `Bash(/Users/andrewchace/bin/devin-free:*)` is a **prefix**
  match, so any `cd … && ` in front of it falls through to the auto-mode classifier, which blocked
  it; the Bash tool resets cwd to the project directory every call, so no allowed form lands in the
  probe directory. **The fix was NOT to add a `cd` allow rule — widening permission surface to run
  a test is backwards.** It must also never be run from the default cwd:
  `/Users/andrewchace/bot-fleet-v2` is IN `trusted_paths` (file read 2026-08-19;
  `/tmp/untrusted-probe` is not, `grep -c` = 0), so that invocation would start a **real Devin
  session in the live tree** rather than stopping at trust. B's one irreplaceable half — that the
  deny rule does not over-match onto the wrapper — is now carried by D below.
- **D — deny test 2, and B's replacement. Both halves SEEN, one command, from the default cwd.**
  `~/bin/devin-free --model swe-1-7-lightning -- "noop"` is safe anywhere: the refusal loop runs
  above `exec`, so no working directory is ever entered.
  1. **The classifier PERMITTED the invocation.** The deny rule on the raw binary path does not
     over-match onto `~/bin/devin-free`. This is what cancelled test B was for.
  2. **The wrapper exited 2, no invocation.** stderr was the `REFUSED: --model is not yours to set`
     block naming `swe-1-7-lightning` at $2.5/$12.5 per MTok; `exit=2`. **Deny test 2, SEEN RED.**
  Corroboration that `exec` was never reached: **the provenance line did not print.** The
  `devin-free: sha256 … | model swe-1-7 (free)` printf sits below the refusal loop and above the
  `exec`, so its absence places the exit ahead of any invocation. The log directory was the same 4
  entries before and after, parent mtime Aug 17 22:45.
- **C — `--selfhash` unchanged.** `~/bin/devin-free --selfhash` →
  `a6dded833ffc0e24a8189867e558f445c4cb88d0dee183fac565d5a81145a309`, exit 0 — byte-equal to
  `shasum -a 256 scripts/devin_free.sh` and to the value recorded at line 101 of this file.

**$0 asserted three ways, and re-asserted the same three ways after D.**
(1) **Nothing reached the binary** — A was a permission denial before exec, D exited in the argv
loop above exec, C returns above exec; B never started a process at all.
(2) **The log directory never changed** — the same 4 entries with the same parent mtime
(Aug 17 22:45) before A, after A, before D and after D.
    **[CORRECTED 2026-08-19 step 6 — THIS LEG IS VOID. Original text left standing.**
    `~/Library/Application Support/Devin/logs` is the **GUI app's** launch log. It did **not**
    move when the CLI genuinely ran a session (acceptance 5), so its stillness never
    distinguished "denied" from "ran" and was never evidence. The real per-run instrument is
    `~/.local/share/devin/cli/logs/devin_<ts>_<pid>.log` — 744 files before acceptance 5, 746
    after one session, and 744 → 744 across the re-run of deny test 1. **Legs (1) and (3) stand
    and are sufficient**: A was refused by the harness before any process existed, and the
    provenance line — which prints immediately above `exec` — was absent from every refused run.
    Lesson: an instrument that has never been SEEN to move is not an instrument.]**
(3) **No provenance line was ever emitted.** `devin-free` prints
`sha256 … | model swe-1-7 (free)` to stderr immediately before `exec`, so its absence across every
check is a per-run marker that no invocation occurred. No Devin session was created, and
`trusted_workspaces.json` is untouched at 2026-08-18 20:54, 2616 bytes.

### Carry-forward — binding on every dispatch prompt

1. **Dispatch prompts must never pass `-p`.** The wrapper supplies it:
   `exec "$DEVIN_BIN" -p --model swe-1-7 "$@"`. A prompt that adds its own sends it twice — the
   manager's earlier `devin-free -p "…"` was malformed for exactly this reason. The call shape is
   `devin-free [flags] -- "prompt"`.
2. **Dispatch prompts must never reintroduce a `$DEVIN` variable.** The wrapper owns the binary
   path (`DEVIN_BIN=` in `scripts/devin_free.sh`). A dispatch-side path variable is precisely how
   the raw binary gets invoked again under a string the deny rule does not match.

   The wrapper owns **both the flag and the path**. A dispatch prompt owns neither.

### Deferred to step 6 — the one thing these probes cannot show

**That the wrapper reaches `exec` at all has NOT been demonstrated.** Every check so far exits
above the `exec` line — A never reached the binary, D refused in the argv loop, `--selfhash`
returns before it. The only way to see `exec` fire and be stopped by nothing but Devin's own
workspace-trust check is to run the wrapper in an untrusted directory, and **step 6 changes what
untrusted means.**

⛔ **Therefore: after ANY change to `respect_workspace_trust` (or to `trusted_workspaces.json`),
the FIRST check to run — before any dispatch, before any wave — is the exec-reach test:**
`~/bin/devin-free -- "noop"` in a directory that is untrusted *under the new configuration*,
expecting the provenance line `devin-free: sha256 a6dded83… | model swe-1-7 (free)` on stderr
followed by Devin's trust refusal. The provenance line is the assertion; the trust refusal is the
stop. **A guard proven under the old configuration is stale** — the whole point of step 6 is to
move the line these probes were measured against.

## STEP 6 — RULED AND EXECUTED, 2026-08-19: devin-free v2

**Ruling:** do not disable trust globally, do not touch Andy's real Devin config. v2 hardcodes the
config the way v1 hardcodes the model, and replaces the protection that turning trust off removes.

**PR #63, `devin-free-v2-scratch-config-cwd-guard`. OPEN, NOT MERGED.** Wave 2 does not dispatch
until Andy has the six results below.

- **Scratch config, wrapper-owned.** `--config` still refused from argv in both spellings; the
  wrapper supplies `~/.local/share/devin-free-lane/config.json` = `{"skip_workspace_trust": true}`.
  Created if absent; otherwise left alone unless the trust key goes missing.
- **Separation is asserted at run time, not just commented.** The script refuses if its scratch
  config resolves inside `~/.config/devin`, `~/.local/share/devin`, or any guarded repo. Andy's
  real config `~/.config/devin/config.json` and the shared `trusted_workspaces.json` appear in the
  file only inside refusals, and neither was touched: 158 bytes / 2026-08-17 22:49 and 2616 bytes /
  2026-08-18 20:54, unchanged across every run tonight.
- **⛔ THE CWD GUARD IS THE POINT.** `skip_workspace_trust` removes the only thing that had been
  protecting the live tree all evening — `~/bot-fleet-v2` is already in `trusted_paths`. v2 refuses,
  above `exec`, exit 2, inside `~/bot-fleet-v2`, `~/gitstore`, and `~/bot-fleet` (the read-only
  archive per CLAUDE.md §8 — one root beyond the two ruled, same argument, flagged for Andy).
- **`--workspace DIR` was added, and it is load-bearing.** The grant is a PREFIX match on the
  script path, so `cd DIR && devin-free` never matches it — the same wall that cancelled test B.
  The wrapper owns the chdir; the guard runs on the RESOLVED target, so `--workspace` into the live
  tree is refused exactly like standing in it (SEEN).

### The six results — all re-proven against the shipped hash, none inherited

The first build was `01013b19…`; a defect found by running it (below) changed the file, so every
guard was re-run against the shipped hash. **Shipped: `3479939d4129996a580e3fdea3ed96241bfead3999889d371d9ea57bfcb868ec`.**

1. **`--selfhash` == canonical.** `3479939d…` equals `shasum -a 256 scripts/devin_free.sh` on the
   PR branch. ⚠️ **It does NOT equal the copy in the live tree, which is still v1 `a6dded83…`
   until PR #63 merges.** The pre-wave assertion will fail by design until then; that is the
   interlock, not a fault.
2. **Deny test 1 re-proven.** Raw devin path, typed bare, DENIED by the classifier. CLI log count
   744 → 744.
3. **Deny test 2 re-proven.** `--model swe-1-7-lightning` → exit 2, no provenance line. Also
   `--model=claude-opus-5` → exit 2, and `--config /tmp/evil.json` → exit 2. The scratch-config
   directory did not exist at all until acceptance 5, which independently places all these
   refusals above the config block as well as above `exec`.
4. **NEW cwd guard: SEEN RED.** From `~/bot-fleet-v2` → exit 2. Also `--workspace
   ~/bot-fleet-v2/scripts` → exit 2, `--workspace ~/gitstore` → exit 2, `--workspace ~/bot-fleet`
   → exit 2. Sibling paths (`bot-fleet-v2-sandbox`, `bot-fleet-vault`) correctly NOT caught.
5. **THE DEFERRED CHECK RAN, AND PASSED. First thing ever observed below the `exec` line.**
   From a fresh untrusted `/tmp` clone (`grep -c` against `trusted_paths` = 0): the provenance line
   printed, `exec` fired, the binary ran (`✓ Organization: chace2827`), and the agent replied `OK`.
   No "Refusing to run in an untrusted workspace". Exit 0. The clone was left clean
   (`git status --porcelain` empty).
6. **Session row — the first real free-lane session of this sequence.**
   `bead-hyssop` · `backend_type=windsurf` · `model=swe-1-7` · `agent_mode=normal` ·
   `total_acu_cost=0.0` · `total_credit_cost=0`, read read-only from
   `~/.local/share/devin/cli/sessions.db`. The first build's session `brook-trilby` reads
   identically. **acu 0.0 / credit 0 on both.**

### Two findings from running it

1. **The deny-test instrument used all evening was the wrong directory.** See the CORRECTED banner
   in the probe section above. `~/Library/Application Support/Devin/logs` is the GUI app's; the CLI
   writes `~/.local/share/devin/cli/logs/devin_<ts>_<pid>.log`, two files per session (the `-p`
   parent and its helper child).
2. **The CLI writes back into whatever config it is handed** — it added `version`, `devin.org_id`,
   `shell.setup_complete` and `theme_mode` to the scratch config on first use. v2's first draft
   rewrote the file whenever its content differed from the literal, which would have reset that
   every run and pushed the CLI's first-run banner (`Welcome to Devin CLI! … You're all set.`)
   into the stdout of every dispatch, where a fleet parser reads it as agent output. Fixed before
   the PR: create-if-absent, repair only a missing trust key. Proof it works — the second run's
   stdout is exactly `OK`, and the config's sha was identical before and after it.

**Open for Andy:** review PR #63 and merge, or reject the `~/bot-fleet` third root. Until it
merges, `~/bin/devin-free` (v2) and `scripts/devin_free.sh` in the live tree (v1) deliberately
disagree, and **wave 2 does not dispatch.**

## WAVE 3 — §0/§1/§2 done, HOLDING AT THE §3 PILOT GATE, 2026-08-19

**§0 gate PASSED.** master `1d56fc0`; `~/bin/devin-free --selfhash` == `shasum -a 256
scripts/devin_free.sh` == `3479939d4129996a580e3fdea3ed96241bfead3999889d371d9ea57bfcb868ec`.

### §1 — both counts re-derived. Neither was taken on trust.

**Item 1 — `docs/rules-catalog.md` = 2310 rules. CONFIRMED, three ways.**
Table-row parse = 2310; per-source-doc declared sum = 2310; **and all 56 sections reconcile
individually**, so offsetting errors are excluded, not merely unlikely. Structural check:
2422 lines beginning `|` = 2310 data + 56 headers + 56 separators.
The board's "55 source docs" and the file's "56" are **both right and count different things**:
55 files rules were extracted from (3 root + 50 `docs/*.md` + 2 `data/*.md`), plus one section for
`docs/AI Agentic.pdf`, which the audit could not read. That section's single row is a
"file not found" placeholder — **1 of the 2310 rows is not a rule.**

**Item 2 — LOCATED, and both memory figures were mislabelled.**
Artifact: `~/Documents/fleet-runs/2026-08-19/pr-sweep/findings_final.json` (869 rows, sha256
`8374e2e1…`); 58 distinct workspaces, so **58/58 is confirmed**.
- **"804 findings" is a cluster count, not a finding count.** 869 rows collapse to 804 clusters
  (`analysis.json`; 749 singletons, 47 pairs, 6 triples, 2 quads, summing to 869).
- **"130 likely-valid" is real but its denominator is 352, not 869.** Of the 352 actionable rows
  (284 DEFECT-SUSPECT + 68 GUARD-UNNAMED): 175 re-verify / **130** untouched-since-pin / 47 no file
  citation. Reproduced exactly from the stored `t` field.
- ⚠️ **130 also appears as DEFECT-SUSPECT ∧ re-verify.** Same value, different quantity — the
  "a fabricated number can equal a real quantity" trap, live in this dataset.
- ⛔ **The code that computed `t` is NOT in the durable copy.** An independent reconstruction from
  git lands at 159/128/65, disagreeing on 30 of 352 rows. So **no slice may consume `t`** — spec B
  re-derives every citation itself, at a stated sha.

### §2 — two slice-specs written (repo root, untracked)
`_slice-spec-A-rules-catalog-2026-08-19.md` — 56 slices, one per source doc, all named.
`_slice-spec-B-blocker-findings-2026-08-19.md` — 25 slices of 15 canon rows, all named, over
`work/canon.json` (369 rows `R001`–`R369`, sha256 `a96f35a1…`).

### §3 — PILOT RUN. Bar was set BEFORE anything ran.
**Bar: ≥80% exact bucket agreement (≥13/16), plus three hard gates** — `#RECONCILE` present and
reading `declared=parsed=written=16`; no bucket assigned without the evidence its test requires;
no row omitted, duplicated or re-ordered.

**Result: 13/16 = 81% bucket agreement — bar met. All three hard gates passed.
Anchor agreement 16/16 — every anchor line identical.**

**Executing the spec by hand found four defects in it, before any agent saw it. That is what §3 is
for, and it is the whole return on this gate:**
1. `grep -F` cannot find a quote that spans a hard wrap (~105 cols). The `DIR-SPX-PutVIX22-SL75`
   KEEP quote is real at `capture-architecture-2026-07-30.md:67-68` and greps as absent.
2. The fragment must be taken from **inside** the row's quotes; the trailing `" — <section>` is the
   catalog's own note. Taking the whole cell produced **14 false ABSENTs out of 16**.
3. The catalog normalises the source's `"` to `'` and moves `**` inside quotes, so the match must
   normalise whitespace, emphasis and quote characters. All three fixes now live in a shipped
   `anchor.py` that every agent runs identically — 16/16 after, and the wrap case still passes.
4. **A banner-only supersession test sends every v1-era rule to LIVE** — 16 of 16 on a doc dated
   2026-06-08. Added **Test 1b (cutover supersession)**, mechanical on two conditions, which is
   what caught row 16 (`Scalp-` name + 214-trade pre-cutover count).

**Where the 3 disagreements fell is the real signal: all of them in Test 2 (CONTRADICTS), none in
the mechanical tests.** The agent found two contradictions the foreman missed (row 5 mirror-funding
bar vs `CLAUDE.md` §1 watch-only; row 15 build priority vs `build-plan.md` §2B) and both are
evidenced and defensible; row 14 is a genuine edge (is "superseded by the backtest tournament" a
banner *over* the rule, or the rule itself?). **Test 2's scope rule is under-determined and is the
one thing to tighten before fan-out — Andy's call, per §5.**

### Dispatch law learned in the pilot, now in §6 of both specs
- ⛔ `--permission-mode dangerous` is required. Default `-p` auto-approves read-only tools only;
  `accept-edits` does not cover the exec tool; **`smart` is advertised in `--help` but prints
  "Smart permission mode is not available. Falling back to normal"** on this build. Three runs
  produced nothing before `dangerous` produced the slice. (This contradicts the harness lane's
  TRAP-2 note that `smart` is present — present in help, unavailable at runtime.)
- ⛔ **Exit 0 is not an acceptance signal.** All three blocked runs exited 0, empty stdout, no file.
- All 6 sessions tonight: `backend_type=windsurf`, `model=swe-1-7`, **acu 0.0, credit 0**.

**HOLDING. No fan-out. Andy authorises the pilot (or rules on Test 2) before §4.**

## WAVE 3 — FAN-OUT HALTED ON MANAGER VERIFICATION, 2026-08-20

MANAGER-CW verified the wave read-only and called HOLD. **The fan-out was live when the hold
arrived and was killed immediately.** What that cost, stated plainly rather than smoothed over:

- **Banked: 1 slice** — A02 (`README.md`, the warm-up), which passed the post-split contract.
- **Killed in flight: 10** — A01, A06, A07, A10, A11, A12, A26, A38, A51, A52. No output, nothing
  partial merged, nothing half-written into `out/`.
- **Never started: 45.** Total 56.

### What the manager confirmed independently
2310 rules · 2422 pipe-lines · 56 sections all reconciling individually · pin `1d56fc0` ·
`devin_free.sh` `3479939d…` · `anchor.py` logic including a RED test · the wrapped case at 67–68
where `grep -Fn` returns nothing · and a **third-party re-run of pilot A21: 16/16 FOUND, 0 ABSENT,
7 of 16 wrapped**. The anchor claim is reproducible by someone who did not write it.

### Blocker 1 — the tool existed only as a fenced block in the spec. FIXED.
`anchor.py` was real in the foreman's template and in PR #64, but **not in either mount and with no
declared sha in the spec**, so `#TOOLS` was an acceptance gate with nothing to compare against and
56 clones meant 56 possible transcriptions. Now: the file ships in PR #64, the spec states the
declared sha, and Test 0 requires an **in-clone assertion before the first anchor call** — a
mismatch is a halt, not a note. Two checks now, one before the work and one in the output.

### Blocker 2 — spec B has no row basis. HELD, and the spec now says so at the top.
`data/blocker-audit-2026-08-19/` does not exist at `origin/master` because **PR #64 is unmerged**.
All 25 B slices are undispatchable, and by spec B's own §1 a slice sent without its pack is
**foreman error, not an agent finding**. Spec B carries a HOLD banner until #64 lands and
`a96f35a1…` / `8374e2e1…` re-assert against the merged tree. **This was the foreman's own rule
being broken by the foreman.**

### Defect 5 — the ≥40-char fragment rule. CONFIRMED INDEPENDENTLY, FIXED IN THE TOOL.
Re-derived here before acting: **239 of 2310 rows (10.3%)** can never reach 40 characters, 187 of
them in the 25–39 band. The spec was silent past that point, so each agent improvised — which is
what "the tool is identical but its input is hand-derived" actually costs. All three fixes landed
**in the tool, not in prose**:
- **(a)** the raw cell goes in and `anchor.py` derives the fragment, so the input is derived
  identically too. It never searches a string still containing an ellipsis.
- **(b)** threshold 40 → **25**; below that it emits `TOO_SHORT` (exit 3) → `UNRESOLVED`.
- **(c)** **multiplicity is reported**: >1 match prints `AMBIGUOUS n=k lines=…` (exit 2) →
  `UNRESOLVED`. First-match-wins with no signal made `anchor_line` a coin flip on 45 rows.

**A fifth class surfaced while re-running the regression:** the catalog appends terminal
punctuation the source does not carry (`never fired**.` against the source's `never fired** in 22
days`), so the full fragment reported ABSENT on text plainly present. Added longest-matching-prefix
backoff, never below the threshold, reporting `trimmed=n`.

**Measured over all 2310 rows with the fixed tool:** FOUND 2096 (90.7%) · ABSENT 107 ·
TOO_SHORT 61 · AMBIGUOUS 45 · 1 unreadable (the PDF placeholder). The 106 ambiguous/too-short rows
are now forced to `UNRESOLVED` instead of silently guessed. Declared sha
**`e20fed809784be2a8de86a4e49543bd71694ac3d902e5b77dc6ed6cd58c3f6aa`**.

### Defect 6 — the pilot slice was named nowhere. FIXED.
The pilot is **A21 = `docs/strategy-taxonomy.md`** (lines 1096–1116). The wrap defect was found in
**A15** (`capture-architecture-2026-07-30.md:67-68`) — the slice begun by hand and set aside as
non-discriminating — and the spec narrated the two as one, which made 13/16 un-re-derivable by
anyone. Both pilot TSVs are now committed at `data/wave3-pilot-2026-08-19/` with the correction.

### The rate, stated correctly
**13/16** raw — the number the bar was set against and met. **16/16** on what agents actually
produce under the split ruling, because all three disagreements were Test-2 `CONTRADICTS` verdicts
and agents no longer render those. Anchor lines agreed 16/16 throughout. Both are true of different
questions; the second is the one that describes the fan-out's actual work.

### Two findings from the session table that no one asked for
1. ⛔ **A killed session leaves a row with NULL metadata and an empty `model`.** The §4 rule
   "assert acu=0.0 on each new session row" **cannot be satisfied for a killed run** — 12 of
   tonight's rows are unassertable this way. Their model is recoverable only from the wrapper's own
   provenance line (all 11 killed fan-out runs printed `model swe-1-7 (free)`). **A NULL metadata
   row is "unknown", not "$0"** — the assertion must say which it is.
2. ⛔ **Two historical sessions ran with `~/bot-fleet-v2` itself as the working directory** —
   `wooden-cathedral` (2026-08-18 03:10) and `lush-sparrow` (2026-08-19 01:00), both before the v2
   cwd guard existed. The hazard the guard closes is not hypothetical; it had already happened
   twice. Both were short and both are acu 0.0.

**Batch spend: 22 rows inspected, non-zero acu or credit = 0.**

**Order from here (manager's, adopted):** land PR #64 → re-pilot A21 with the patched tool → then
fan out spec A. **Spec B stays held until its basis exists.** Merging #64 is a push to master:
per dispatch §5 that is halt-and-report, so it is Andy's, not this lane's.

### RE-PILOT A21 under the patched tool — done 2026-08-20, still holding

**Mechanical layer 16/16** against `anchor.py`'s deterministic output, driven independently over
the same 16 raw cells. `#RECONCILE 16/16/16`; `#TOOLS` = declared `e20fed80…`.

**RED TEST PASSED.** Row 8 (`**Pillar 3 only.**`, 14 chars normalised) → `TOO_SHORT` → the agent
recorded `UNRESOLVED / fragment-too-short`. Under the old spec **both the foreman by hand and the
first agent** improvised a sub-threshold fragment and called it `LIVE` at line 77. That is defect 5
demonstrated and closed on the row that exhibited it.

**Judgement layer moved:** 5 `CONTRADICTS-CANDIDATE`s (rows 4, 5, 9, 13, 15) vs the first run's 2,
each with a genuine one-sentence case — row 9 cites `R-2026-08-07-IC-GROUPS-BOTH-STAY`. Under the
split that is a flag routed to pass 2, so more candidates is not a regression.

⛔ **OPEN FOR ANDY — row 14 has given three terminal answers in three passes**, on a stable anchor
(line 125): `LIVE` (foreman) / `SUPERSEDED-BUT-STILL-READS-AS-LIVE` (agent run 1) / `dead` (agent
re-pilot, citing `build-plan.md` §2D). The rule's own text says the QQQ hedge family is
"Reclassified … superseded by the backtest tournament" — is a rule describing its own supersession
retired, or descriptive? **`dead` is terminal and does not route to pass 2**, so at 56-slice scale
this divergence ships unreviewed. **Proposed, NOT applied** (§5: bucket-definition change after the
pilot is Andy's): restrict `dead` to the mechanical anchor-absent branch, and route judgement-based
retirement to a flag pass 2 adjudicates.

### ⛔ THE acu ASSERTION HAS A HOLE — established by test, not inference
`plain-brain` (the re-pilot) **completed, wrote a valid slice, and its session row still reads
`model=''`, `agent_mode=''`, `metadata=NULL`.** Killing the lingering process did **not** backfill
it. Sessions that exit naturally (`patch-evening`, `grand-rondeletia`, `bead-hyssop`, …) all carry
`acu=0.0 / credit=0`; sessions killed or left lingering never do, permanently.

Consequences for §4, both now binding:
1. **Output present ≠ session finalised.** The re-pilot wrote its complete TSV and the process
   lingered afterwards.
2. **A NULL-metadata row is `acu=UNKNOWN`, never `$0`.** 14 of tonight's rows are permanently
   unassertable this way. The only compensating evidence is the wrapper's own provenance line —
   all 11 killed fan-out runs printed `model swe-1-7 (free)` — plus the fact that the wrapper
   hardcodes the free model. That is evidence about the MODEL, not about acu.
   The runner must wait for natural exit before asserting, and must report killed/lingering
   sessions as UNKNOWN rather than counting them into a `$0` total.

**Status: spec A is re-piloted and ready to fan out. Still HOLDING** on: (1) PR #64 merge —
a push to master, therefore Andy's under §5 — and (2) the row-14 bucket ruling. Spec B stays held
until its basis exists in the merged tree.

## 2026-08-20 01:34 — manager re-check answered; everything landed on disk

**The one thing asked for is done: the artifacts are in `~/bot-fleet-v2` on disk**, not only on a
PR branch and not only in `/tmp`. Paths, all verified by `shasum -a 256` against their sources:

| Path | sha256 |
|---|---|
| `scripts/anchor.py` | `e20fed809784be2a8de86a4e49543bd71694ac3d902e5b77dc6ed6cd58c3f6aa` |
| `data/wave3-pilot-2026-08-19/A21-foreman-by-hand.tsv` | the by-hand pass, written before any agent ran |
| `data/wave3-pilot-2026-08-19/A21-agent.tsv` | agent, run 1 |
| `data/wave3-pilot-2026-08-19/A21-agent-repilot-patched-tool.tsv` | `30dfc8cd77272100ee7f218c81a319c912caf7a44b3c43f8eb1878e4783e559f` |
| `data/wave3-pilot-2026-08-19/A02-warmup-agent.tsv` | the §4 warm-up |
| `data/blocker-audit-2026-08-19/{findings_final,analysis,rows_slim,canon}.json` | `8374e2e1…` `9e7a9120…` `e27ccbb7…` `a96f35a1…` |

**16/16 re-derived reading nothing but the live tree** — `docs/rules-catalog.md`,
`scripts/anchor.py` and the committed TSV. `#RECONCILE declared=16 parsed=16 written=16`;
`#TOOLS` = the declared sha.

### Correction to the manager, with evidence
`docs/lane-state-foreman.md` was **NOT** swept into the daily-loop commit. `git show --stat
3943f51` contains **0** matches for it — the only `docs/` files in that commit are
`portfolio-inbox-2026-08-19.md` and `session-log.md`. Its last commit is
**`d857ee4 "wave 3: slice-specs A and B, pilot gate passed 13/16"`**, correctly titled. The mtime
coincidence at 01:14:50 was real but the file was not in the commit. No pointer commit is needed;
what *is* uncommitted is everything written since d857ee4, which still needs a wave-3-titled commit.

### Rulings applied
- **Row 14 → `CONTRADICTS-CANDIDATE`, winner `docs/build-plan.md`, routes to pass 2.** Basis
  verified in the tree: `build-plan.md:85` puts the QQQ hedge family in archive-directly with
  *"Tournament invalid as a selector: S1≈D identical on 73/86 days…"*, and `CLAUDE.md:38`/`:115`
  make build-plan frozen. Recorded as a worked example in spec A §7, with the generalisation: **a
  rule can be undermined by the invalidation of the authority it defers to**, which is neither a
  banner over it nor a contradiction on its face.
- **`RETIRED-CANDIDATE` adopted; agents now render no terminal judgement verdict at all.** `dead`
  is reachable only from Test 0's mechanical anchor-absent branch. `CONTRADICTS`,
  `SUPERSEDED-BUT-STILL-READS-AS-LIVE` and judgement-`dead` are all pass-2 verdicts. Pass 2 takes
  both candidate kinds in one queue, since a rule can be flagged as both.
- **§6, both specs: NEVER KILL A SESSION.** Killing is what destroys the acu evidence permanently.
  Lingering is wait-and-report. A NULL row is reported as **"two evidence surfaces dropped to
  one"** — the provenance line still proves the model, nothing proves the cost — never as `$0`.

### Test 0.5 added — and it is bigger than reported
The `Status` column exists on all 2310 rows and the spec ignored it. Re-measured here with an
escape-aware splitter (all 2310 rows have exactly 5 cells; **174 distinct status strings**):
`Active` 1703 · `Gated — Pending` 318 · `Supersed*` 88 (59 exact) · `Active — Frozen` 56 ·
**13 compound rows carrying BOTH `Supersed*` and `Active`** · 6 cells that are not statuses.
**The 6 is confirmed exactly** (`t`×3, `t\`×2, `premium\`×1); the earlier 33 was a splitter
ignoring `\|` escapes and is not carried anywhere.

Gated rows now go to `UNRESOLVED` rather than falling through to `LIVE`; a first-class `GATED`
bucket is **proposed, not applied** (§5), because 318 rows should not sit in the unresolved queue
purely for want of a name.

> **Two derivations of "non-Active" disagree and both are recorded: 607 (not exactly `Active`) vs
> the manager's 497.** The entire gap is `Active — Frozen` (56) + ~25 dated `Active — …` variants
> + `Supersed*` counted exactly (59) vs by substring (88). **318, 64 and 6 agree exactly in both.**
> The operative conclusion is identical, which is why the disagreement is recorded rather than
> resolved by fiat.

## 2026-08-20 — THIRD PILOT. The backoff cap, proven where it fires.

**The manager found the blocker inside my own fix, and it was the same defect class this wave
exists to find.** The prefix backoff was added on reasoning and validated on A21 — where **all 16
rows are `trimmed=0`, so it never once fired on its own validation set** — and then became the
sole basis for hundreds of anchors, with matches surviving after up to **120 characters** were
dropped and recorded identically to exact matches.

**Fix, all three parts:**
- **(a) `trimmed` is a 12th column** in both specs, copied from the tool on every row, `0` included.
  The `#TOOLS` sha stops slices being silently incomparable; this stops **rows inside one slice**
  being silently incomparable.
- **(b) The backoff is capped:** `trimmed > 15` or `> 20%` of the fragment → `TRIM_EXCEEDED`
  (exit 4) → `UNRESOLVED`, never `FOUND`. New declared sha
  **`973b68058e28b18b42ecbabb0641a923b4f2518358683c3df0f12c7341daa6e5`**.
- **(c) Re-piloted on a slice where it actually fires**, plus A21 for the row-14 acceptance row.

**Shipped-tool dry run, post-cap, all 2310 rows** (by subprocess against `scripts/anchor.py`, not a
reimplementation — the previous count came from a reimplementation and was wrong):
`FOUND` 1963 (85.0%, of which **205 via backoff, max 15, median 1**) · `TRIM_EXCEEDED` 152 ·
`ABSENT` 100 · `TOO_SHORT` **51** · `AMBIGUOUS` 43 · 1 unreadable.
The manager's `TOO_SHORT 51` reproduces exactly; their `ABSENT 101` = my 100 + the PDF counted
separately; their `AMBIGUOUS 44` = my 43 + one row that was ambiguous only *via* an over-trim and
now returns `TRIM_EXCEEDED` first. **347 rows (15.0%) will not anchor cleanly** — deliberately more
than the pre-cap 196, because 152 rows that read as clean matches are now explicitly unresolved.

### Results
**A08 `pilot-clone-card-qqq-fortress.md`, 22 rows — 22/22 anchors, 22/22 `trimmed`, 22/22 twelve
columns**, `#RECONCILE 22/22/22`, `#TOOLS` correct. **Nine rows hit the cap** (trims 25, 31, 34, 35,
37, 47, 77, 85, 94), every one `UNRESOLVED / anchor-trim-exceeded:<n>`. Test 0.5 fired on three
classes in the same slice: `Superseded` → `RETIRED-CANDIDATE`; `Gated — Pending` → `UNRESOLVED /
status-gated` (the 318-row class that used to reach `LIVE`); `Active — Frozen` → `LIVE`. Row 1
`ABSENT` → `dead`, the only mechanical branch where `dead` survives.

**A21 row 14 — named acceptance row — PASSED.** `CONTRADICTS-CANDIDATE`,
`winner=docs/build-plan.md`, reached **independently**: the prompt never named `build-plan.md:85`.
The agent found the archive-directly disposition through the new **deference check** in Test 2 and
wrote the concrete case itself. 16/16 anchors, 16/16 `trimmed`.

**Both sessions finalised with full metadata** — `lean-dolomite`, `auspicious-balmoral`, both
`windsurf` / `swe-1-7` / **acu 0.0 / credit 0**. Neither was killed. The never-kill rule is now
demonstrated rather than asserted: let a session exit naturally and both evidence surfaces survive.

### Counts settled
**Carry 607** (`Status=='Active'` exact = 1703). The pair is **607 vs 425**, not 497 — the manager
withdrew 497 as an ad-hoc classifier that bucketed frozen ahead of active. Malformed cells: **6**,
not 33. Docstring corrected from `239 / 10.3%` to **250 / 10.8%**, measured with the tool's own
`fragment()`. **497, 33 and 239 are all retired as instrument errors — the catalog was right every
time.** `GATED` remains proposed, with the manager's recommendation to adopt.

# ═══ WAVE 3 SCOPE-DOWN, 2026-08-20 — Andy, relayed by MANAGER-CW ═══

**Spec A is HELD, not cancelled. The 56-slice fan-out will not run, and its three open defects
are deliberately NOT being fixed** — they only matter if the wave runs. `anchor.py`, the cap and
the `trimmed` column stay exactly as they are; the narrow pass reuses them verbatim.

## ✅ WHAT THE WAVE ALREADY BOUGHT — banked here, needs no fan-out

1. **Five QQQ hedge bots whose status depends on which document you read.**
   `docs/strategy-taxonomy.md` keeps `HedgeA-S1` / `HedgeB-S2` / `HedgeC-S3` / `HedgeD-Conditional`
   / `HedgeTest` as live "Iron Condor · Experiment" bots; `docs/build-plan.md` §2A archives them
   directly, no clone, because the *"Tournament [is] invalid as a selector"*. This is the A21
   row-14 finding and it is about **five real bots**, not a sentence.
2. **318 catalog rows marked `Gated — Pending` read as LIVE** to anything consuming the catalog —
   the `Status` column existed on all 2310 rows and every triage test ignored it (Test 0.5).
3. **The blocker dataset's two structural facts:** 44% of rows (164/369) carry a PR-body premise
   that is unverifiable from a repo clone, and 28% (102/369) can be falsified by a *word* rather
   than a figure. Both change how any future sweep must be packed and prompted.
4. **The instrument itself:** `scripts/anchor.py` at declared sha
   `973b68058e28b18b42ecbabb0641a923b4f2518358683c3df0f12c7341daa6e5`, capped, with `trimmed`
   carried per row — plus the standing finding that **three consecutive count disputes were
   instrument errors, never catalog errors** (497, 33, 239 all withdrawn; the catalog was right
   every time).

## ⭐ RE-AIMED: slice-spec C — one slice = one BOT

`_slice-spec-C-bot-disposition-2026-08-20.md`. Scope: **doc-vs-doc contradictions that change which
bots run or are archived.** Roster = `build-plan.md` §2 (35 dispositioned bots: 2 delete, 20
archive, 4 clone-then-archive, 9 leave-in-place); §D fresh builds are out of scope.

⛔ **The roster must be curated by hand and reconciled to 2/20/4/9 before any dispatch — it is the
first acceptance gate.** Three counts exist and none agree: build-plan says 35, the manager's
extractor found 28, mine found 25 and then 40 once abbreviated `-Suffix` forms were expanded, and
that 40 included `bots_meta`, `data/archive/`, two ruling ids and the fragment "opened this side
today". §C's seven mirrors are OA display names (`3DTE $140-$350`, `QQQ long call`, `Tasty
Condor`…) that **no bot-name regex will ever match**. A regex cannot produce this list.

**Source scoping is a rule, not a convenience.** The pilot bot appears in **90 files** and only
**18 prose docs**. `data/archive/**` is barred by `CLAUDE.md` §3, generated output states no
disposition, and `docs/rules-catalog.md` is an index of the others — counting it double-counts
every rule it quotes.

## PILOT — `QQQ-IC-0DTE-Fortress-NoPT50`, foreman by hand (agent running now)

Chosen because it is **armed ON while unsigned** — inbox I-06, `AUTOS ON / EXITS ON` in two
independent first-hand captures 48h apart (`2026-08-17-r3`, `2026-08-19-roster`). A disagreement
about this bot is a live control failure with money on it.

| Doc | States |
|---|---|
| `build-plan.md:103` §B | clone → spec → archive original; 15:50 time exit + 15:52 backstop, **NO PT50**, RESOLVED 2026-07-30 |
| `portfolio-inbox-2026-08-19.md:11` | **I-06, P1**: armed while unsigned — *"sign it or disarm it"* |
| `state.md:22` | listed in the **UNSIGNED** banner, pending an owed first-trading-day capture |
| `RULINGS.md:1803` | Active ruling, `applies_to: PR-04 … — ARMED + ON` |
| `strategy-taxonomy.md:140` | roster table: status **ON**, +$2,760 |

**CONTRADICTS-CANDIDATE — `strategy-taxonomy.md:140` vs `portfolio-inbox-2026-08-19.md:11`.**
*Concrete case:* reading the taxonomy roster, this bot being **ON** is its normal validated state
and needs no action; reading I-06 and `state.md`, that same ON state is a **P1 roster-truth defect
that must be signed or disarmed today** — so the taxonomy row licenses leaving armed a bot the
inbox says to disarm.
**⛔ RE-TYPED 2026-08-20 — this is not a precedence verdict. `FALSIFIED-BY-DATA`.**
The original verdict (below, left standing) preferred the inbox on precedence and **left the false
number sitting in a live document**. The number is not merely outranked; it is untrue:
`data/trades.csv` holds **71 rows across 15 bots and ZERO for this one**; `STATUS.md:237` reads
`| … | 0 | 0 | 0 | insufficient data | insufficient data |`; `STATUS.md:14` puts the bot on the
**UNSIGNED — DO NOT SWITCH ON** list. Every P/L in that taxonomy block (`+$2,760`, `+$2,975`,
`+$908`, `−$445`, `−$450`) names a bot with **no post-cutover ledger row**. Verified against two
independent surfaces. **Only a factual verdict closes it: `:140` states a number that is not true.**

**⛔ AND MY OWN CITATION WAS FABRICATED. `CLAUDE.md §3.5` DOES NOT EXIST.** The rule I meant is
**§3 item 5** — *"Narrative docs never carry numbers. If a `.md` states a figure, the CSV wins"* —
at `CLAUDE.md:37`. The idea was right; the section number was invented. **This is exactly the
defect class this effort exists to find, produced by this effort, in the acceptance row of its own
pilot.** Spec C §2.6 now requires every citation to be resolved by `grep -n` to a line before it
may be written; a citation that does not resolve is not evidence.

~~Original verdict: winner `portfolio-inbox` + `state.md` on precedence — current dated first-hand
captures over a 2026-06-08 pre-cutover doc, and `CLAUDE.md` §3.5.~~ Left standing per the doc
convention; superseded by the two corrections above.

**Note the shape:** the sharpest conflict here is doc-vs-**capture**, not doc-vs-doc — no document
says "armed is correct", yet the bot is armed. Spec C finds the doc-vs-doc half; the doc-vs-reality
half is I-06 and is already Andy's.

## Manager's own note, kept because it is the transferable lesson
> *"I should have asked 'what decision changes because of this TSV' three rounds ago… being right
> about each defect is not the same as the exercise being worth continuing."*
That question belongs in §0 of every future dispatch, above the gates.


## Two amendments the pilot forced into spec C, 2026-08-20

**§2.5 — the cutover gate belongs to the DOCUMENT, not the bot row.** `strategy-taxonomy.md` is
dated 2026-06-08 and its roster table states pre-cutover P/L for every bot in it. Test 1b's two
conditions both fire **on the block**, with no judgement, so the whole roster block is
`SUPERSEDED-BUT-STILL-READS-AS-LIVE` and is recorded **once**. Without this gate spec C
re-litigates the same v1 table once per bot — **28 times — and calls it 28 findings.**

**§2.6 — every citation must resolve** by `grep -n` before it is written. See the fabricated
`§3.5` above.

## Sharpening I-06 — the false number is the operational risk

The live risk on `QQQ-IC-0DTE-Fortress-NoPT50` is **not only that it is armed**. It is that a live
document tells any reader it has made **$2,760** and is **ON**. Anyone checking *"is this thing
fine?"* lands on `strategy-taxonomy.md:140` and concludes yes. **The false number is the single
thing most likely to keep an unsigned, never-filled bot armed.** That belongs in the I-06 item
itself, not only here.

## The 10 killed agents — the never-kill rule's first real cost

The halted fan-out killed 10 sessions. Those are now **10 permanently unassertable acu rows**:
`metadata=NULL`, `model=''`, and killing them later does not backfill. That is not a footnote to
the halt — **it is the reason the never-kill rule exists**, and it was paid before the rule was
written. The compensating evidence is only the wrapper's provenance line, which proves the *model*
and says nothing about cost.
