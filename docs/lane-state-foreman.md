# Lane state — FOREMAN

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
     5. **TWO deny tests, both must be SEEN RED before any dispatch. NOT YET RUN** — they require
        the post-restart grant, and running them beforehand proves nothing:
        - the raw binary directly → must be **DENIED by the classifier**
        - `devin-free --model swe-1-7-lightning` → must **exit 2 from the wrapper**, no invocation
     6. Only after step 5 passes is workspace trust revisited. `/tmp` clones are untrusted and
        Devin refuses them; the two documented fixes are interactive trust or
        `respect_workspace_trust: false` in config. **Neither has been attempted.**
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
