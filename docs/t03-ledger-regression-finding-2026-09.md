# T-03 ledger regression finding — 2026-09-08

## Tracker
T-03 "Investigate the ledger regression" (`data/portfolio.csv`, P1).

## Question
Is the regression named by T-03 the 2026-08-12/08-17 ledger truncation
documented in `docs/ledger-truncation-forensics-2026-08-17.md`, or a different,
still-open defect?

## Verdict
**CLOSED.** The regression is the 08-17 truncation. It is covered by the
monotonicity guard family in `scripts/build_ledger.py`, and an explicit red test
for the exact failure shape already exists. No code change was made.

## Evidence

### 1. T-03 description matches the truncation

`docs/ledger-truncation-forensics-2026-08-17.md` opens with the tracker item:

> hedge_tournament 2026-08-11 points at a trade_id absent from trades.csv;
> trades.csv now holds one day only.

The same file names commit `0051b5e6` as the moment a build pinned to the stale
`2026-08-10.csv` export erased 2026-08-11 and the truncated file was committed
to `master`.

### 2. The backwards-max-open_date guard is implemented

The docstring at `scripts/build_ledger.py:82-109` explains the guards, but the
**implementations** are:

- `scripts/build_ledger.py:728` — `--- THE MONOTONICITY GUARD (G-2) ---`
- `scripts/build_ledger.py:750` — `--- THE FRONT MONOTONICITY GUARD (G-2b) ---`
- `scripts/build_ledger.py:773` — `--- THE OPS-RECLASSIFICATION GUARD (G-2c) ---`

G-2 compares the max `openDate` of the post-cutover working set against the max
`open_date` of the existing `data/trades.csv`. When `new_max < prior_max` the
script calls `rewind_refusal()` and exits before any byte is written, unless
`--allow-rewind` is passed. G-2b mirrors this on the front (min open_date
moving forward); G-2c covers the interior axis (banked rows moving to
`ops_rows.csv`).

### 3. A red test for the exact T-03 scenario already exists

`python3 scripts/build_ledger.py --selftest` runs in CI
(`.github/workflows/ci.yml` job `selftests`). The selftest block
`---- G1-G8: THE MONOTONICITY GUARD (G-2) ----`
(`scripts/build_ledger.py:1250-1304`) explicitly rebuilds the `0051b5e6` shape:

- `G1` builds a two-day ledger from the newest export.
- `G2` pins to the **older** export and asserts the run exits with
  `REFUSED: this rebuild would walk the working ledger BACKWARDS`.
- `G2b` asserts the refusal names both max open_dates and the source export.
- `G2c` asserts `trades.csv` is byte-identical after the refusal — nothing was
  written.

Additional cases cover `--allow-rewind` (`G3`), forward builds (`G4-G5`), empty
ledger (`G6-G7`), blank-date handling (`G8`), the front guard (`G9-G12`), and
ops reclass with the required REAR / FRONT / INTERIOR ordering (`G13-G15`).

No new red test is required because `G2` is already present.

### 4. First-hand reproduction against the live ledger

- **RED run**: `python3 scripts/build_ledger.py 2026-08-10` on the working tree
  refused with the G-2 message, naming `2026-09-04 -> 2026-08-10`,
  `246 leg(s) -> 4 leg(s)`, and source export `2026-08-10.csv`. Exit code 1.
  SHA-256 of `data/trades.csv`, `data/bots.csv`, and `data/ledger_meta.json`
  were identical before and after the run, confirming nothing was written.

- **GREEN run**: `python3 scripts/build_ledger.py --selftest` — 49/49 passed.

## Boundaries

The 08-17 forensics also identified a separate latent defect:
`hedge_tournament.csv` keys on `trade_id`, and a cross-file `trade_id` join is
unsound after any pinned rebuild. That is tracker **T-10** ("Stable trade_id
from the natural key and migrate the accumulator"), not T-03. The T-03
symptom — `T00005` in `hedge_tournament.csv` with no matching row in
`trades.csv` — was a downstream consequence of the ledger being truncated, not
the root cause itself.

## Hand-off
T-03 is closed. The only artifacts added by this lane are this finding and the
matching `data/portfolio.csv` status update (in the same PR).
