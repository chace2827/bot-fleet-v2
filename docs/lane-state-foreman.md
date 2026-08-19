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
| base sha believed | `65799e04c563b3ffe0a76e1c994c66ce50f94850` |
| last verified against `origin/master` | 2026-08-19T00:53:19Z |
| how | `git fetch origin && git rev-parse origin/master` — matched; local `master` in sync |
| ruling count at that sha | 155 (`git show origin/master:docs/RULINGS.md \| grep -c '^ruling_id:'`) |

That sha is the merge of PR #56, `build_ledger: G-2/G-2b/G-2c ledger guards + bots_meta
duplicate-key FATAL`.

## Open PRs owned by this lane

**None.** (`gh pr list --state open --json number -q '. | length'` → 0 at the timestamp above.)

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

1. **F-7's `build_ledger.py` work.** Queued **deliberately behind PR #56's merge** — same file, and
   Andy will not have two changes to it in flight at once. PR #56 is now merged, so this is the next
   dispatch when its prompt arrives.
2. Rulings/dispatches for F-1, F-4, F-6 and stage-5 fatality. None are this lane's to resolve.

## Operating notes that cost real time to learn

- **Devin invocation**: `-p --model swe-1-7 --permission-mode dangerous`, **no `--sandbox`**.
  `smart` does not exist on this install; `dangerous + --sandbox` fails, because sandbox forces
  autonomous mode which still gates some tools on confirmation, and in `-p` those are rejected —
  it produces zero commits.
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
