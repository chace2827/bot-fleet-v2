# Phase 3 witness

Archived read-only copy of build A's verdict set, for the blind dual-build
adjudication described in `R-2026-08-19-GATES-SEMANTICS-Q1-Q3`.

- **Build A**: commit `71e2336`, verdicts `build-A-71e2336-verdicts.tsv`,
  sha256 `133919da1f9003e3e7cee07dd03ab278b6f017dcffa3e91151efb75b389d1c28`.
- **Build B (this PR)**: commit `ec6e786`, verdicts `p3_verdicts.tsv`,
  sha256 `bfa4a90505c1be1d1bae60fe4af682dc1e0bbbaf10e0518275e76b91cb0c53fc`.

The two builds were blind and independent implementations of the same
`scripts/should_have_fired.py` spec. Both consumed the same signed
`data/bot_gates.csv` and the same tape days in `data/brief/`.

Both builds produced the same 65 judged `(date, bot)` rows and passed the same
acceptance gate: PR-05 JUSTIFIED, PR-06 JUSTIFIED, PR-10 JUSTIFIED, and PR-01
SUSPECT. 38 rows differed in verdict; the differences collapsed to three
semantic questions (Q1/Q2/Q3), all ruled to build B's reading by
`R-2026-08-19-GATES-SEMANTICS-Q1-Q3`.

- **Q1 (label taxonomy, 34 rows)**: an underlying absent from the tape is
  `UNEVALUABLE_MISSING` naming the underlying and date; an underlying present
  with source != tradier is `UNEVALUABLE_SOURCE`.
- **Q2 (tape-free gates, 3 rows)**: a gate that consumes no tape field
  (e.g. weekday) evaluates regardless of tape state; therefore PR-10 is
  `JUSTIFIED` on non-Fridays.
- **Q3 (straddle scope, 1 row, 2026-08-14 PR-06)**: the asymmetric/straddle
  rule applies to every VIX gate type, so a straddling day is
  `UNEVALUABLE_INTRADAY`, never `SUSPECT`.

Build A's verdict set is archived here unmodified. Build B's verdict set is the
generated `p3_verdicts.tsv` at the repo root.
