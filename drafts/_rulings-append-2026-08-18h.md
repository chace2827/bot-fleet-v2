```yaml
ruling_id: R-2026-08-19-TAPE-SYMBOLS-FROM-GATES
date: 2026-08-19
scope: >-
  Resolves the W2 symbol-set conflict and the circularity beneath it, found
  by the foreman lane: scripts/tape.py underlyings_on() selects tape symbols
  from which bots FILLED that day, but the SHOULD-HAVE-FIRED detector exists
  to judge bots that did NOT fill — so the generator structurally cannot
  supply the data the detector needs on quiet days (next live day with no
  QQQ fill, all GF rows go UNEVALUABLE_MISSING). Ruled 3+1: (3) a named
  guard change per charter §4 is PRE-AUTHORIZED — underlyings_on() (or its
  call site) selects the tape's symbol set as the UNION of underlyings
  referenced by data/bot_gates.csv rows (currently SPX, QQQ, VIX), not from
  that day's fills; live and backfilled tapes become rule-identical
  permanently. Bounds: symbol selection only; no other tape.py behaviour
  changes; the docstring and any dependent fixtures update to match.
  (1) W2's backfilled tapes for 2026-08-10/08-11 (and the new 08-12/08-13)
  carry the gates union, consistent with the new rule — no divergence to
  record beyond backfilled_at + backfill_evidence. W5's expectation stands:
  the GF-QQQ Q1 rows on backfilled days move to real verdicts.
verbatim: >-
  Fix the generator and use the gates union: tape symbols come from the
  gates table, not from fills, live and backfilled alike. Named guard
  change pre-authorized at that scope.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  scripts/tape.py underlyings_on()/call site (guard change, named in the PR,
  cites this ruling); W2's backfilled tape files; W5's expected movers
  (unchanged). Extends R-2026-08-19-TAPE-BACKFILL-AND-VIX-SERIES; nothing
  superseded.
superseded_by: none
source: >-
  Foreman lane W2 conflict report 2026-08-19 (underlyings_on definition read
  from the tree); Andy's ruling in the Cowork session.
unclear: false
```
