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

