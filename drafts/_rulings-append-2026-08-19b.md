```yaml
ruling_id: R-2026-08-19-VERDICT-SURFACING
date: 2026-08-19
scope: >-
  Phase 5. The should-have-fired detector has been wired as daily.sh stage 5
  of 9 since PR #44, but scripts/report.py contains ZERO references to
  p3_verdicts, should_have_fired or SUSPECT, and neither STATUS.md nor
  dashboard.html mentions a verdict. The detector writes a TSV that nothing
  the operator reads ever opens — a signal about silence that is itself
  silent, which is the failure class this whole project exists to remove.
  Ruled: (1) A named change to scripts/report.py is PRE-AUTHORIZED at this
  scope: report.py READS the day's verdict file produced by stage 5 at
  <root>/data/brief/<DAY>_p3_verdicts.tsv and surfaces it on BOTH operator
  surfaces — the STATUS.md headline and dashboard.html — following the
  two-surface precedent set by the unsigned-bot banner (report.py:436 and
  the dashboard at :1086). report.py runs as stage 9, after stage 5, so the
  file exists by then and NO stage reordering is authorized.
  (2) THE SPLIT. SUSPECT rows are presented in two counts, not one.
  A SUSPECT row whose bot's row in the SIGNED data/bot_gates.csv carries
  gate_type "none" or "unknown" is STRUCTURAL — it is suspect because no
  market gate is declared, so no computation stands behind it. Every other
  SUSPECT row is EVIDENCED — a signed gate was evaluated against tape data
  and the reason string carries the number. Measured on the 96-row record at
  master 4f11b02: 26 SUSPECT = 6 structural + 20 evidenced; the structural
  set is IC-SPX-Fortress-Unstopped (INC-01, gate_type none) alone, at
  exactly one row per day on every day it does not fill; no gate_type
  "unknown" row is SUSPECT anywhere in the record. This predicate invents no
  taxonomy — it is read wholly from the signed gates table.
  Rationale: INC-01 contributes a standing one-per-day forever until its
  gate is signed, so a single flat count never returns to zero and stops
  carrying information. The split keeps the evidenced number meaningful
  without hiding anything.
  (3) ⛔ PRESENTATION ONLY. report.py MUST NOT compute, recompute, alter,
  suppress or second-guess a verdict. It reads the TSV stage 5 wrote and
  renders it. Structural rows are COUNTED SEPARATELY, NEVER HIDDEN — they
  remain listed and readable. Importing gate_parser or should_have_fired to
  re-derive anything is outside this authorization.
  (4) LOUD ON ABSENCE. If the day's verdict file is missing or unreadable,
  report.py says so prominently on both surfaces. It may not silently omit
  the section — a missing detector output must never look like a clean day.
  (5) KNOWN-POSITIVE REQUIRED. report.py's self-test fixtures gain a verdict
  file containing at least one STRUCTURAL and one EVIDENCED SUSPECT row, and
  assert both counts, so this section ships tested rather than repeating the
  untested-guard pattern of P1-4 and P2-5a.
  Bounds: scripts/report.py and its self-test fixtures only. No change to
  daily.sh, to stage order, to should_have_fired.py, to gate_parser.py, to
  data/bot_gates.csv, or to any verdict. Not authorized here and still open
  for Andy: whether stage 5 should remain FATAL (run_stage exits the whole
  run on non-zero rc, so a stage-5 failure costs STATUS.md, dashboard.html
  and the entire evening report), and F-4 (gate_parser.py
  eval_band_prior_close's unguarded rec["series"], a KeyError path into that
  same fatal stage).
verbatim: >-
  Put the verdicts where I actually read them, on both surfaces, and split
  the SUSPECT count into structural and evidenced so one permanently silent
  bot cannot drown the rows that carry a number. Presentation only — the
  report renders verdicts, it never computes them. Loud if the file is
  missing.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  scripts/report.py (named change, cites this ruling) and its self-test
  fixtures; STATUS.md and dashboard.html as rendered outputs;
  data/bot_gates.csv gate_type column (READ ONLY, as the split's authority);
  R-2026-08-18-REPORT-BUILD-AUTH (extended to the surfacing step, not
  superseded); R-2026-08-18-BOT-GATES-TABLE (the signed gate source the
  split reads; unchanged).
superseded_by: none
source: >-
  Rulings-lane audit 2026-08-19 against master 4f11b02: report.py grepped
  for p3_verdicts / should_have_fired / SUSPECT (zero hits), STATUS.md and
  dashboard.html likewise; data/receipts/daily-runs.jsonl showing the last
  two real runs (2026-08-14 and 2026-08-17) recording eight stages with
  should_have_fired absent, and no <DAY>_p3_verdicts.tsv existing anywhere
  in the repo; the 6/20 structural-vs-evidenced split computed from the
  96-row W5 artifact joined to the signed gates table. Andy's ruling in the
  Cowork session.
unclear: false
```
