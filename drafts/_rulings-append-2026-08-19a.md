```yaml
ruling_id: R-2026-08-19-VIX-ENTRY-WINDOW
date: 2026-08-19
scope: >-
  Amends R-2026-08-19-GATES-SEMANTICS-Q1-Q3 Q3 in interpretation. Q3 ruled
  that a VIX gate is JUSTIFIED "only if the gate was unreachable all day"
  and that a straddling day is UNEVALUABLE_INTRADAY. That clause was written
  when no intraday VIX series existed: scripts/gate_parser.py eval_vix_min()
  and eval_vix_change_max() read the day-level rec["high"]/rec["low"] and
  never called parse_window()/select_bars(), so "all day" was the only
  window the detector could see. Their straddle branch says so in the
  reason text it emits — "no intraday VIX series" — a sentence that
  R-2026-08-19-TAPE-BACKFILL-AND-VIX-SERIES made false when tape.py began
  fetching the VIX 5-min series. Ruled: (1) the evaluation window for a VIX
  gate is the bot's DECLARED entry_window_et, not the session. A gate is an
  entry condition; whether VIX crossed the threshold hours after the entry
  window closed does not bear on whether the bot should have fired at its
  entry time. (2) A named guard change per charter §4 is PRE-AUTHORIZED at
  this scope: eval_vix_min() and eval_vix_change_max() select their high/low
  from parse_window(entry_window_et) + select_bars() over the VIX series,
  the same path eval_band_prior_close() already uses; where the window
  yields no bars the verdict is UNEVALUABLE_MISSING_BAR naming the window;
  the emitted reason states the window and its bar count.
  ⛔ EXPLICITLY FORBIDDEN: any fallback to day-level high/low when the
  window yields no bars. A missing window is UNEVALUABLE_MISSING_BAR and
  says so. A silent day-level fallback would restore the very semantic this
  ruling amends, on exactly the days where the evidence is weakest, and is
  the failure this bound exists to prevent. It is not authorized here and
  may not be adopted to unblock a failing test.
  (2a) CONSEQUENTIAL PRE-AUTHORIZATION — the self-test. The VIX fixtures in
  scripts/should_have_fired.py (_run_selftest, the 2026-08-14 and 2026-08-10
  tapes) carry "series": [], so the window path returns
  UNEVALUABLE_MISSING_BAR for all six VIX self-test bots and the self-test
  fails. Updating those fixtures is PRE-AUTHORIZED at this scope: the two
  VIX fixture records gain a 5-min series covering the declared 11:00
  window, and the fixture gate thresholds may be retuned, PROVIDED the
  self-test still asserts one JUSTIFIED, one SUSPECT and one
  UNEVALUABLE_INTRADAY for EACH of vix_min and vix_change_max — the
  three-outcome coverage is load-bearing and may not shrink. A SEVENTH VIX
  case is REQUIRED: one bot whose entry window falls outside its fixture's
  series, asserting UNEVALUABLE_MISSING_BAR, so the new branch ships with a
  known-positive rather than repeating the untested-guard pattern of P1-4
  and P2-5a. Bounds on the whole change: scripts/gate_parser.py's two VIX
  evaluators, their self-test fixtures and expectations in
  scripts/should_have_fired.py, and the data/bot_gates.csv header straddle
  note. No change to the three-state semantics, to the
  JUSTIFIED/SUSPECT/UNEVALUABLE vocabulary, to any other gate type, to any
  other evaluator, or to any other file. (3) Q1 and Q2 are untouched, and Q3's own intent — never
  SUSPECT on a guess — is preserved in substance: the window narrows the
  evidence, it does not license accusing a silent bot. It is nonetheless
  ACKNOWLEDGED and ACCEPTED that this widens the SUSPECT side in principle,
  because a day that straddles at session scale can be met throughout a
  narrow entry window. No row on the 2026-08-08..2026-08-17 record does
  this; the widening is prospective, and a future SUSPECT arising this way
  is a correct verdict under this ruling, not a defect. Verified effect on
  the current record: exactly ONE verdict changes (PR-06 2026-08-14
  UNEVALUABLE_INTRADAY -> JUSTIFIED; the 11:00 bar gives low 14.48 against
  prior_close 14.63 = -1.03%, never reaching the -2% threshold inside the
  window, where the session low of 14.18 = -3.08% did) and TEN VIX rows keep
  their verdict with a narrower reason string.
verbatim: >-
  The window supersedes "all day". A VIX gate is judged over the bot's
  declared entry window, because that is when the bot would have fired.
  Q3's fallback was a limitation of the old detector, not a semantic.
  Named guard change pre-authorized at that scope.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  scripts/gate_parser.py eval_vix_min() and eval_vix_change_max() (guard
  change, named in the PR, cites this ruling); scripts/should_have_fired.py
  _run_selftest VIX fixtures and expectations (consequential, bounded by
  §2a incl. the required seventh case); data/bot_gates.csv header
  straddle note (clerical fix, rides the PR per
  R-2026-08-18-BOT-GATES-TABLE's clerical-fix provision);
  R-2026-08-19-GATES-SEMANTICS-Q1-Q3 Q3 (AMENDED IN INTERPRETATION, NOT
  SUPERSEDED — Q1 and Q2 stand unchanged and every existing reference to
  that ruling id remains valid); the W5 expected-mover set fixed by
  R-2026-08-19-REPLAY-PROVENANCE-AND-W5-MOVERS.
superseded_by: none
source: >-
  Rulings-lane investigation 2026-08-19 against master c28fc34: the two
  evaluators read at gate_parser.py:271 and :301, the window path they do
  not use at :191-194, and a throwaway reference implementation run over
  data/brief/2026-08-{08,10,11,12,13,14,17}_tape.json to measure the effect
  before authorizing it. Andy's ruling in the Cowork session.
unclear: false
```

```yaml
ruling_id: R-2026-08-19-REPLAY-PROVENANCE-AND-W5-MOVERS
date: 2026-08-19
scope: >-
  Two provenance decisions and the acceptance predicate for W5.
  (1) REPLAY SATISFIES THE SOURCE RULE. A tape rebuilt by replaying tape.py
  against committed raw Tradier response bodies, carrying
  any_reconstructed=false and source="tradier" per underlying, SATISFIES the
  per-underlying source rule at gate_parser.py:126. The bytes are genuine
  Tradier data; only the fetch moment differs, and the fetch moment is not
  what the source rule protects. source="tradier" is therefore accurate on a
  backfilled tape and is not to be weakened. Consequence:
  IC-SPX-Fortress-Unstopped (INC-01, eval_class SUSPECT_WHEN_SILENT) moves
  UNEVALUABLE_SOURCE -> SUSPECT on 2026-08-10 and 2026-08-11; those two rows
  BANK. (2) NOTED, NOT RULED: W2 regenerated all six tapes, so every tape on
  disk now carries backfilled_at — including 2026-08-17, which was live.
  That field therefore does NOT discriminate live from replayed and must not
  be used as such by any future detector; anything needing that distinction
  requires a new field and a ruling. (3) The PR-05/PR-06 rows on 2026-08-10
  and 2026-08-11 moving UNEVALUABLE_MISSING -> JUSTIFIED bank as AUTHORIZED
  BY EXTENSION of R-2026-08-19-TAPE-SYMBOLS-FROM-GATES: those verdicts meant
  "no VIX in this tape", the gates-union rule put VIX in every tape, and the
  11:00 window clears the 22 threshold by roughly seven points. (4) W5's
  COMPLETE expected delta against the banked p3_verdicts.tsv snapshot is
  fixed as: 65 rows -> 96; 31 NEW rows, all on 2026-08-12 and 2026-08-13,
  none removed; 23 verdict changes, being 16 GF-QQQ UNEVALUABLE_MISSING ->
  SUSPECT on 08-10/08-11, 4 PR-05/PR-06 UNEVALUABLE_MISSING -> JUSTIFIED on
  08-10/08-11, 2 INC-01 UNEVALUABLE_SOURCE -> SUSPECT on 08-10/08-11, and 1
  PR-06 UNEVALUABLE_INTRADAY -> JUSTIFIED on 08-14; plus 3 reason-only
  rewrites on already-JUSTIFIED VIX rows. Totals move SUSPECT 5 -> 26,
  JUSTIFIED 7 -> 34, UNEVALUABLE_MISSING 34 -> 14, UNEVALUABLE_SOURCE 2 ->
  0, UNEVALUABLE_INTRADAY 1 -> 0. ANY row moving outside this enumeration
  STOPS the wave and returns to Andy with evidence. The superseded snapshot
  is kept as a dated witness at repo root; it is not deleted.
  (5) The 21 net-new SUSPECT rows are real action items entering the evening
  ritual, not a detector defect.
verbatim: >-
  A replayed tape is a real tape — source=tradier is honest and the source
  rule passes. Bank the INC-01 rows and the VIX rows. The mover list in
  this ruling is the whole list; anything else stops and comes back to me.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  scripts/gate_parser.py:126 per-underlying source rule (interpretation
  fixed, no code change authorized here); p3_verdicts.tsv at repo root
  (regenerated by W5, prior snapshot retained dated); the W5 PR's acceptance
  predicate; R-2026-08-19-TAPE-BACKFILL-AND-VIX-SERIES and
  R-2026-08-19-TAPE-SYMBOLS-FROM-GATES (extended, neither superseded);
  R-2026-08-18-BOT-GATES-TABLE (INC-01 eval_class unchanged).
superseded_by: none
source: >-
  Rulings-lane reference run 2026-08-19 against master c28fc34 (engine run
  over the post-W3 tapes, diffed key-by-key against the banked
  p3_verdicts.tsv); tape provenance read from the backfill_evidence field of
  data/brief/2026-08-10_tape.json and 2026-08-17_tape.json. Andy's rulings
  in the Cowork session.
unclear: false
```
