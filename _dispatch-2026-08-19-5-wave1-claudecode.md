# WAVE-1 — Claude Code foreman — free-lane Devin dispatch, 6 agents

Paste into the Claude Code terminal, in `~/bot-fleet-v2`:
"Read `_dispatch-2026-08-19-5-wave1-claudecode.md` in the repo root. You are the WAVE-1 foreman.
Execute §1 pre-flight, then §3. Report in the §5 format."

## 0. Lane split — who does what
- **Cowork (Andy's chat)** = manager. Wrote this file, classifies the board, verifies your claims
  read-only, writes the next wave. Not a second foreman.
- **You (Claude Code)** = foreman. Own the terminal, the clones, the queue, the merges.
- **Devin `-p`** = worker. Free SWE-1.7 only. One deliverable per agent.
- **Andy** = relay + every decision. He pastes your §5 report into Cowork and Cowork's reply back.

## 1. Pre-flight — do ALL of it before dispatching anything
1. **Probe the permission modes.** `"$DEVIN" -p --help`. `--permission-mode smart` was REMOVED in
   an update; modes drift. Never assume yesterday's flags. Record what exists in the §5 report.
2. **Pin the base.** `git -C /tmp/... fetch origin && git rev-parse origin/master`. Every clone
   pins that sha and prints it. Base on `origin/master`, never the working tree.
3. **Verify each card's premise against the file at that sha** before dispatching it. Three
   dispatches in one evening died on a premise that was already false. If a premise fails,
   do not dispatch — report it in §5 and move on.
4. **Warm-up.** One throwaway `devin -p` run. Cold start is 30-60s vs 1.5-4.6s steady; without it
   the first real agent looks hung.
5. **Confirm the CAP.** Wave 1 is 6 concurrent. If any other Devin fleet is live on this account,
   the ceiling is total, not per-fleet — drop wave 1 to fill the gap to ~10 and say so.

## 2. Invocation and clone protocol — non-negotiable
```bash
DEVIN=/Applications/Devin.app/Contents/Resources/app/extensions/windsurf/devin/bin/devin
"$DEVIN" -p --model swe-1-7 --permission-mode <probed> -- "…prompt…"
```
- **`--model swe-1-7` explicitly.** `-p` defaults to `swe-1-7-medium`; `swe-1-7-lightning` is a
  PAID name collision. Only `swe-1-7` and `swe-1-7-medium` are free.
- **Never `devin -r`.** Never a paid alias. Never an Anthropic/OpenAI model in Devin Desktop.
- **One `/tmp` clone per agent.** `git clone --no-hardlinks` once, `cp -R` per agent, every clone
  pinned to the wave sha. **No `git worktree`** — it writes into `~/bot-fleet-v2/.git/`.
- **Never run anything against `~/bot-fleet-v2` or `~/gitstore`.** Not even read-only git.
- `data/**/*.csv` IS tracked, so clones carry the ledger. **`todo-2026-08-16.csv` at the repo root
  is NOT tracked** — if a card needs it, stage a read-only copy into the clone.
- Results land as **PRs to `devin/*` branches**, merged `gh pr merge --auto --squash`.
  **Never push to master** — Andy's gh creds are ADMIN and a stray push bypasses protection.
- After every batch: assert `model`, `backend_type=windsurf`, `acu=0.0`, `credit=0` on each new
  session row. **Fail loudly.** A non-zero acu is a halt-and-report, not a footnote.

## 3. The six agents — dispatch all six, they are independent
Every card's acceptance is a **derivation**, not a literal. An agent that hardcodes a number to
satisfy the predicate has failed the card.

**A1 · T-03 — ledger regression forensic (READ-ONLY + a finding, NO fix)**
Premise to verify first: `data/hedge_tournament.csv` references a `trade_id` absent from
`data/trades.csv`, and `trades.csv` holds fewer distinct dates than the tournament spans.
Deliver: `docs/finding-ledger-regression-2026-08-19.md` naming the code path that drops the rows,
plus a command that reproduces the loss from a fixture. **Do not change `build_ledger.py`** —
the fix is a separate ruling. Accept when: the reproduction runs from a clean clone and its
row-count delta is computed from the fixture, not asserted.

**A2 · T-13 — unsigned banner in `scripts/report.py`**
Andy's 2026-08-11 ruling, still unexecuted, ~10 lines. The banner's bot list and count must be
**derived from the unsigned set in `STATUS.md`**. Accept when: the banner's count equals the count
`scripts/portfolio.py` derives from the same STATUS.md section, and an empty unsigned set renders
no banner rather than a zero.

**A3 · T-11 — split the Tradier failure modes, `scripts/tape.py` `_get()`**
`_get()` swallows every error into `reconstructed`. Present-but-rejected must be LOUD; absent may
fall back. Order matters or it recurs on the next rotation. **Token re-issue is Andy's, not
yours** — code only. Accept when: a test distinguishes the two paths and the loud path is
non-recoverable.

**A4 · T-12 — heartbeat artifact per trading day, `data/heartbeat/`**
v1 died of undetected silence: a scheduled job that never ran must be detectable. `scripts/heartbeat.py`
and `scripts/check_heartbeat.py` already exist — read them before writing anything.
Accept when: a day with no run is distinguishable from a day with a failed run, by file state alone.

**A5 · T-14 — archive sweep: `git mv` + citation rewrite in ONE commit**
Moving the dated docs breaks every citation to them. Accept when: `python3 scripts/check_refs.py`
is green on the post-move tree AND the count of rewritten citations equals the count of moved
files' inbound references computed before the move. One commit, not two.

**A6 · T-04 + T-06 + T-23 — three one-line doc edits, ONE PR**
All three are Class A, already un-gated. Do not spend three sessions on three lines.
- T-04 `docs/pending-tracker-items-2026-08-10.md:40` — the line implies a missing Tradier token;
  the token is present and the base is production. The real defect is A3's.
- T-06 `docs/state.md` G-1' block — add the exit_rows anti-rediscovery note; two reviewers have
  re-proposed the already-declined option.
- T-23 — name `docs/RULINGS.md` explicitly as the canonical rulings file the charter references,
  or the reference dangles.
Accept when: `check_refs.py` green and each edit is a single-match grep.

## 4. Held out of wave 1 — deliberately, do not add them
- **T-15** (fixture-isolate + TAPE_FIXTURE) — rewrites the CI every other PR runs under. Lands
  alone, after wave 1 merges.
- **T-28** (2310-rule catalog triage) and **M-32** (draft ~18 pre-registration entries) — both are
  fan-outs in their own right, sliced by source doc / by bot. Wave 2 and 3.
- **T-10, G-4** — already in flight. Do not re-dispatch.
- Anything with `lane=OA` or `lane=ANDY` in `data/portfolio.csv`. Ever.

## 5. Report back — exactly this shape, for Andy to paste into Cowork
```
WAVE-1 REPORT
base sha:            <sha>          modes available: <probed list>
premise checks:      <A1..A6: PASS / FAIL + one line>
dispatched:          <n>  concurrent peak: <n>  429s: <n>
cost assertion:      model=<> backend_type=<> acu=<> credit=<>  [PASS/FAIL]
per agent:           <id> <PR # or branch> <accept predicate: PASS/FAIL/partial> <one line>
merged to master:    <PR #s>  origin/master now: <sha>
working tree:        <porcelain clean? y/n>
escalations for Andy: <numbered, with both readings — or NONE>
```

## 6. Escalation
- **You decide:** slicing, retries, clone mechanics, which PR merges first, re-prompting an agent.
- **Andy decides:** any Class C edit, any guard/detector predicate change, any spend outside the
  free lane, amending any plan or spec, any acceptance verdict the evidence does not settle.
  Put the question and BOTH readings in the escalations block. When in doubt, it is Andy's.
- **Halt immediately and report:** a push to master, any git write against `~/bot-fleet-v2` or
  `~/gitstore`, a non-zero acu, an agent widening a guard or relaxing CI to unblock itself.
