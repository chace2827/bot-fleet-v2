```yaml
ruling_id: R-2026-08-19-VERDICT-FILE-PER-DAY
date: 2026-08-19
scope: >-
  Fixes F-5. scripts/should_have_fired.py build_report() iterates EVERY tape it
  finds and writes every date's verdicts into whatever --output names, so
  daily.sh stage 5 — which names data/brief/<DAY>_p3_verdicts.tsv — produces a
  day-stamped file containing the FULL history. Measured: the 2026-08-17 file
  holds 96 rows and the 2026-08-18 file 112, on a day with 16 verdicts. Any
  consumer that trusts the filename reads seven dates as one day.
  scripts/report.py survives only because it applies its own date filter at
  :444 — a shield on one consumer, not a fix to the artifact.
  Ruled: (1) THE CONTENT IS CORRECTED, NOT THE NAME. A named change to
  scripts/should_have_fired.py is PRE-AUTHORIZED at this scope: a `--day
  YYYY-MM-DD` option restricts the run to that date's tape, so the file
  daily.sh writes contains only the day it is named for. daily.sh's stage-5
  invocation passes the day it is processing. Rationale for content over
  rename: git already preserves the whole record as of every daily commit, so
  the duplicated history inside each file buys nothing that `git log` does not
  give better, and the filename is the contract the next consumer will trust.
  (2) THE FULL-HISTORY PATH IS PRESERVED, UNCHANGED. Invoked WITHOUT `--day`,
  build_report() still evaluates every tape and writes the complete record —
  that is how the repo-root p3_verdicts.tsv snapshot is produced, and its
  behaviour, output and semantics do not move.
  (3) ⛔ NO VERDICT SEMANTICS CHANGE. Not one JUSTIFIED / SUSPECT /
  UNEVALUABLE_* decision, reason string, gate evaluation, fill exclusion or
  class boundary may move. This ruling changes WHICH ROWS ARE WRITTEN to one
  file, nothing about how any row is decided. A verdict that differs before
  and after this change is a STOP.
  (4) ⛔ report.py's date filter at :444 STAYS. It is now redundant and must
  NOT be removed as cleanup. Defense in depth is the point: the filter is what
  protected the report when the artifact lied, and the next regression will
  arrive the same way.
  (5) A missing tape for the named day is a LOUD non-zero exit naming the day
  and the path it looked for — never an empty file, never a silent full-history
  fallback.
  (6) THE TWO EXISTING BANKED FILES ARE NOT REGENERATED.
  data/brief/2026-08-17_p3_verdicts.tsv (96 rows) and
  data/brief/2026-08-18_p3_verdicts.tsv (112 rows) stay exactly as committed in
  2d17fbe. They are honest witnesses of what the pipeline produced on those
  nights; rewriting banked artifacts to match a later convention is the
  retroactive edit this project refuses. The new shape applies from the next
  run forward, and the discontinuity is recorded here rather than erased.
  (7) KNOWN-POSITIVE REQUIRED. The self-test asserts BOTH paths: with `--day`,
  the output contains only that date and the expected row count; without it,
  the output still contains every fixture date. Two assertions, so neither path
  can regress silently — the P1-4 / P2-5a pattern is not repeated.
  Bounds: scripts/should_have_fired.py (build_report signature, argparse, the
  tape selection, self-test fixtures) and scripts/daily.sh's stage-5
  invocation line. No change to scripts/report.py, scripts/gate_parser.py,
  data/bot_gates.csv, the root snapshot, or any committed verdict file.
verbatim: >-
  Fix the content, not the name — the daily file holds the day it is named
  for. The no-flag full-history path stays exactly as it is, report.py keeps
  its filter even though it is now redundant, and the two files already
  committed stay as they are. No verdict may move.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  scripts/should_have_fired.py (named change, cites this ruling) and its
  self-test; scripts/daily.sh stage-5 invocation (line 208 at master 2d17fbe);
  data/brief/<DAY>_p3_verdicts.tsv from the next run forward;
  data/brief/2026-08-17_p3_verdicts.tsv and 2026-08-18_p3_verdicts.tsv
  (EXPLICITLY NOT regenerated); scripts/report.py:444 (unchanged, and
  protected from cleanup by §4); R-2026-08-19-VERDICT-SURFACING (the surfacing
  contract is unaffected — report.py keeps selecting the newest dated file).
superseded_by: none
source: >-
  Rulings-lane finding during the Phase-5 review 2026-08-19 (the build agent
  added report.py's date filter unprompted, which exposed the artifact defect
  it was working around), confirmed against master 2d17fbe by row-counting the
  two committed daily files: 96 and 112 rows for days carrying 16 verdicts.
  Andy's ruling in the Cowork session.
unclear: false
```
