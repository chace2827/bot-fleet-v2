# T2 strike-distance sweep — 2026-10-06

Queue item #2 (`docs/dispatch-strike-distance-2026-10-06.md`). Six new backtest
arms built off T1-A0 (`ZZ-COWORK-2026-10-06-T1-A0-ride`, ZT217913212733763171103)
via Add Variation, testing short-strike deltas `.05` / `.07` / `.15` each with and
without Touch $10, against the `.10Δ` baseline (A0/A3, not rebuilt).

Captured 2026-10-06 ~22:30–00:15 America/Los_Angeles. OA Paper Trading. Backtests
only — no bot, automation, position, scanner, or settings surface touched.
Pacing rule applied throughout (1.5–4s per action, +10s every 5); per-arm
paceMs/actionCount in `01-raw-capture.txt`.

## Files

| file | sha256 (first 16) | description |
|---|---|---|
| 01-raw-capture.txt | see SHA256SUMS | serialized input diffs vs A0, test IDs, timings, rendered stats + fee insights, verbatim register-day rows |
| 02-analysis.md | see SHA256SUMS | paired-by-date stats, date-set audit, selection + holdout verdicts, fees |
| A0-ride.csv | 62e42f8860d32735 | T1-A0 positions export (control) |
| A3-t10.csv | 00f70e5216c1aeec | T1-A3 Touch $10 positions export (.10Δ reference) |
| D05-ride.csv | 62d8c261d023c804 | ZZ-AGENT-2026-10-06-T2-D05-ride (824 pos) |
| D05-t10.csv | e038d7fc70c795cb | ZZ-AGENT-2026-10-06-T2-D05-t10 (824 pos) |
| D07-ride.csv | dd4e3a9e8220ebf1 | ZZ-AGENT-2026-10-06-T2-D07-ride (826 pos) |
| D07-t10.csv | eb175920e92fd5aa | ZZ-AGENT-2026-10-06-T2-D07-t10 (826 pos) |
| D15-ride.csv | 6b8e5926be62bb16 | ZZ-AGENT-2026-10-06-T2-D15-ride (825 pos) |
| D15-t10.csv | 5ebb85092a80efee | ZZ-AGENT-2026-10-06-T2-D15-t10 (825 pos) |
| SHA256SUMS.txt | — | full hashes of everything above |

## Results (full period, paired vs A0)

| arm | bad days | fixed | created | mean R | % of A0 | gross |
|---|---|---|---|---|---|---|
| A0 (control) | 95 | — | — | +0.0022 | 100% | +$848 |
| A3-t10 | 11 | 84 | 0 | +0.0135 | 614% | +$4,691 |
| D05-ride | 42 | 53 | 0 | −0.0006 | −27% | −$191 |
| D05-t10 | 16 | 80 | 1 | +0.0041 | 186% | +$1,568 |
| D07-ride | 62 | 33 | 0 | −0.0026 | −118% | −$997 |
| D07-t10 | 23 | 73 | 1 | +0.0000 | 0% | +$8 |
| D15-ride | 153 | 0 | 58 | +0.0123 | 559% | +$3,801 |
| D15-t10 | 2 | 94 | 1 | +0.0188 | 855% | +$5,992 |

## Verdicts

- **Selection (2021-10→2024-12): winner = D15-t10** — 64 fixed / 1 created,
  p=3.6e-18, mean R +0.0217 vs control −0.0098.
- **Holdout (2025-01→present): D15-t10 FAILS the return guard** — bad-day
  elimination still perfect (30/0, p=1.9e-9) but mean R is 63% of control
  (< 80%). Not confirmed.
- **Only D05-t10 passes the full rule on both windows.** Whether a runner-up may
  be advanced is a ruling question, not decided here.
- **No bot recommendation made.** Fees ($3.16/txn, re-derived from rendered
  insights) are informational only; they exceed gross on 5 of 8 arms.

## Assumptions

- Pairing is on shared `Opened` dates only; divergent date sets reported, never
  padded. D05 arms lack 2025-07-21/25; D05+D07 carry an extra 2026-04-09.
- `R = P/L ÷ Risk` from the CSV; capped at −1 by construction.
- Touch-exit count = CSV `Status == "touch"` (cross-checked: A3=406, D07-t10=223,
  D15-t10=672 — all match the rendered Exits blocks).
- Backtester exits stop ~15:45; late breaches invisible equally in all arms.

## Questions for Andy

1. Winner D15-t10 fails the holdout return guard (63% < 80%) while acing the
   bad-day test. D05-t10 is the only arm passing both windows — may a runner-up
   be advanced under `R-2026-10-06-TAIL-HOLDOUT`, or does this lane close with
   "no confirmed setting"? [UNCLEAR]
2. On holdout, A3 (the T1 winner) also fails the return guard (10% of control
   mean). Does that change the standing of the T1 result, or is the 2025+
   calm regime being read as a different environment?

## Refusals

None taken on OA. No login, no Create Bot, no edits to any live surface, no
existing test re-run. One deviation: D15-t10's first build script was killed
mid-drawer (hang); the open drawer was finished by a second script after
re-verifying staged values — documented in `01-raw-capture.txt`.
