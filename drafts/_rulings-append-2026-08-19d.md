```yaml
ruling_id: R-2026-08-19-LEDGER-FRONT-GUARD
date: 2026-08-19
scope: >-
  G-2 guards ONE END of the ledger. scripts/build_ledger.py:595-599 refuses
  when the rebuild's maximum open_date is EARLIER than the prior ledger's
  maximum — the rear. Nothing guards the front. A day-only export, or a
  rolling export window too narrow to reach LEDGER_START, moves the maximum
  FORWARD while deleting every day behind it, so G-2 passes on the wrong
  axis and the rebuild — which is FULL and destructive, "the OA website
  export is FULL trade history, not a delta" — writes a ledger containing
  one day. The only other thing in the path is the FILTERED-EXPORT warning
  at build_ledger.py:834, which is a `print`, not a `sys.exit`; the run
  continues and commits the truncation. This is the 2026-08-12 failure
  (commit 0051b5e6, five legs erased, live on master for five days) arriving
  through the door its guard does not watch.
  ⚠️ DATED: Andy's OA export range is "Since 08/19/2025", which has no
  cliff. A "30 days" rolling window stops reaching LEDGER_START = 2026-08-10
  around 2026-09-09 and would begin truncating silently from that date.
  Ruled: (1) A named guard change per charter §4 is PRE-AUTHORIZED at this
  scope — G-2b, THE FRONT MIRROR. It mirrors G-2 exactly rather than
  resembling it: a min_open_date(rows, key) helper beside max_open_date();
  a truncation_refusal(...) that is RETURNED, not raised, so the self-test
  can read its text; evaluated at the SAME call site, BEFORE the first byte
  is written, against the SAME new_working set with the ops rows already
  subtracted. Refuse when `prior_min and new_min > prior_min`. The escape
  hatch is an explicit `--allow-front-truncate`, distinct from
  `--allow-rewind` because it is a different axis and a different intent;
  when passed, it prints the same shape of loud banner G-2 prints.
  (2) ORDER: when an export trips BOTH guards, the REAR refusal fires first.
  It names the more severe loss and it is the failure with the recorded
  precedent.
  (3) BLANK DATES ARE IGNORED, and the reason is the OPPOSITE of G-2's.
  max_open_date() ignores blanks so a malformed row cannot fake a rewind;
  min_open_date() must ignore them so a malformed row cannot sort to the
  front and fake a PASS. State that reason in the docstring — the symmetry
  is deceptive and the next reader will assume it is the same argument.
  (4) ⛔ THE FILTERED-EXPORT WARNING IS NOT PROMOTED HERE. Making
  build_ledger.py:834 fatal is a separate question with a real cost — it
  would refuse legitimate runs when a bot is genuinely retired — and is not
  authorized by this ruling.
  (5) ⛔ NOTHING ELSE MOVES. No change to LEDGER_START, to the cutover
  partition, to the ops exclusion, to the FILTERED-EXPORT text, to G-2, or
  to a single byte the rebuild writes when it is not refusing. This ruling
  adds a refusal path; it does not alter any accepted rebuild.
  (6) KNOWN-POSITIVE REQUIRED, mirroring the existing rewind-guard tests: a
  fixture whose export drops the earliest banked day must REFUSE with
  nothing written, and the same fixture with --allow-front-truncate must
  proceed and emit the banner. Two cases, so neither branch can regress
  silently — not the P1-4 / P2-5a pattern again.
  (7) ANTICIPATED CORRECT FIRING — do not "fix" it. When OA's retention
  window eventually stops reaching LEDGER_START (roughly 2027-08 on a
  one-year range), this guard WILL refuse a legitimate export. That refusal
  is the correct signal that the ledger can no longer be rebuilt from a
  single export and the design needs revisiting. It is not a false alarm and
  it is not to be silenced by widening the guard — a blocked rebuild returns
  to Andy, as always.
  The G-2b label is clerical; if the G-series has a canonical allocator the
  number may be reassigned without a further ruling.
verbatim: >-
  Mirror the rewind guard on the front. Refuse when the rebuild would move
  the ledger's earliest day forward — that is truncation from the front, and
  right now nothing sees it. Explicit flag to override, rear guard fires
  first, and leave the filtered-export warning alone for now.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  scripts/build_ledger.py — new min_open_date() and truncation_refusal()
  helpers, the guard at the existing pre-write call site, the
  --allow-front-truncate argument, and the self-test (named change, cites
  this ruling). No other file. Extends the G-2 monotonicity guard
  (docs/ledger-truncation-forensics-2026-08-17.md §7) without altering it;
  R-2026-08-19-VERDICT-FILE-PER-DAY and the daily loop are unaffected.
superseded_by: none
source: >-
  Rulings-lane analysis 2026-08-19 prompted by Andy asking whether the daily
  OA export could be filtered to one day. Read against master 794a6a6:
  build_ledger.py's own docstring on the full destructive rebuild, the G-2
  call site at :595-599 comparing only maxima, and the FILTERED-EXPORT
  warning at :834 being a print rather than an exit. Andy's ruling in the
  Cowork session.
unclear: false
```
