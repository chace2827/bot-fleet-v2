# WAVE 2026-09-08 — six free Devin lanes before the promo dies 09-16
Ruled: `R-2026-09-07-DEVIN-WAVE-SCOPE`. Cap 4 concurrent (dispatch.sh default), the rest queue.
Every lane: branch from origin/master, one PR, red-green evidence in the PR body, `Andy merges`,
never touch master, never touch OA, never pass a guard override. Foreman: see the free-wave
runbook (`~/0dte-day-taxonomy/prompts/foreman-2026-09-01.md`) and adapt; receipts = model uid.

Common pre-flight for every lane (3 dispatches died on stale premises 08-17):
`git fetch && git checkout -b <lane> origin/master`; record the head sha; verify every file/line
premise below against the working tree before acting; if a premise is false, STOP and report.
Common acceptance: predicates stated as derivations, never literals; a red run shown before the
green run; `roster.py --check`, `portfolio.py --check`, `pre_registration_ledger.py --selftest`
unchanged; no new CSV columns; LF line endings. Update `data/portfolio.csv` status of your item
to `Ready for review` with the PR number in metric_note, in the same PR.

---
## Lane 1 · T-44 — G4 $ caps into report.py
Full spec: `drafts/_dispatch-2026-09-03-t44-g4-caps.md`. Use it verbatim.

## Lane 2 · T-45 — ingest REFUSES a range-shortened export (P1)
Premise: `scripts/build_ledger.py` rebuilds `data/trades.csv` from the NEWEST `data/raw/*.csv`
only (`newest_raw()`, ~L76-79); the FILTERED-EXPORT GUARD (~L696) compares bot SETS and only
warns; LEDGER_START = 2026-08-10 (L158). On 2026-09-07 a since-08-01 export (251 rows) replaced
a full-history one (1,596 rows) and passed with a WARN.
Build: a REFUSAL (exit non-zero, write nothing) in `build_ledger.py` when the new export's
minimum `openDate` is LATER than max(LEDGER_START, the previous raw file's minimum `openDate`
among rows with openDate >= LEDGER_START). Message names both dates and the two files. Keep the
existing bot-set guard as is. Add the same check to `ingest_export.py` so close.sh stops at
stage 1/5 rather than 2/5. No override flag.
Red test: fixture pair (prev raw min openDate 08-10, new raw min openDate 09-01) → refuses;
(new min 08-10) → passes; (new min 08-01, earlier than prev) → passes. Show red before green.
Docs: one paragraph in `docs/daily-loop-spec.md` under the export step: "export start date must
be on or before LEDGER_START; the guard refuses otherwise."

## Lane 3 · T-46 — catch-up close records capture PRESENT (P2)
Premise: `scripts/close_manifest.py` ~L352 reads `data/captures/<day>-roster`; `capture_bundle.py`
names the dir by the CAPTURE date; they coincide only when the close runs the same day. On
2026-09-07 `close.sh 2026-09-04` wrote `data/captures/2026-09-07-roster/` and the 09-04 manifest
says `capture: ABSENT` (`data/close/2026-09-04/manifest.json`).
Build: close_manifest accepts the capture dir actually produced in this run (close.sh passes it
explicitly), falling back to `<day>-roster`; manifest records the dir name and the capture's
own ET timestamp; `capture.status` = PRESENT when the .txt exists and its sha256 matches
SHA256SUMS.txt in that dir. Do NOT rewrite the 09-04 manifest (history); add a `--reconcile`
that prints what the 09-04 manifest WOULD say, for the PR body.
Red test: a fixture close where capture dir ≠ day → ABSENT before, PRESENT after.

## Lane 4 · T-43 — close_manifest.py --selftest into phase0 CI (P3)
Premise: `.github/workflows/phase0*.yml` runs `roster.py --check` and `portfolio.py --check`
(PR #70); `close_manifest.py --selftest` exists and passes locally; the T-38 root guard has no
CI coverage. Build: one CI step. Red proof: a sacrificial commit that breaks the selftest must
turn phase0 red (the PR #68 pattern) — link the red run in the PR body, then the green.

## Lane 5 · T-03 — ledger regression investigation (P1, oldest open item)
Premise: board item T-03 "Investigate the ledger regression", est 10 min, unowned since 08-16;
`docs/ledger-truncation-forensics-2026-08-17.md` and `data/archive/README-v1-ledger.md` describe
the 08-17 truncation. Task: READ-ONLY. Determine whether the regression T-03 names is the
08-17 truncation (already fixed by the max-open_date-backwards guard in build_ledger.py, ~L91-99)
or something else; write a one-page finding `docs/t03-ledger-regression-finding-2026-09.md`
that either closes T-03 with the guard as evidence (cite the code and a red test that exists) or
names the still-open defect with a reproduction. No code change unless a red test is missing for
the closed case — then add only that test.

## Lane 6 · T-47 — section 2.4 hash-freeze PR (P3)
Premise: `R-2026-08-18-MECHANICS-IN-FORCE` (docs/RULINGS.md) names the trigger: re-record the
fixed panel (`scripts/execution_audit.py`, `scripts/build_ledger.py`) at FULL sha256 as of the
PR's base commit; retire the 16-hex short form in `docs/daily-loop-spec.md` L36/L152; append a
lineage trace citing the merged PR behind each hash movement since the original declaration
(67a53797… → fdc43d0d…; 9ec21da9… → e12c9ef1… → 314d449a… → current); record the version-bump
procedure (new version re-records its hash with a changelog line; counting/detector changes
Class C; display-only Class A). Also add the corresponding line to
`docs/roster-mechanics-ruling.md` s2.4 marking it IN FORCE as of the merge sha.
Acceptance: `sha256sum` of both scripts at the base commit equals the recorded values (show the
command and output); a selftest or CI step that recomputes and compares (so the freeze is a
predicate, not a sentence). Class C by nature — the PR body must say "guard-bearing files,
hashes re-recorded, no behavior change" and Andy pre-authorizes by merging.
