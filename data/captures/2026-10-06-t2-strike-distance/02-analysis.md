# T2 strike-distance sweep — analysis

Dispatch: `docs/dispatch-strike-distance-2026-10-06.md`. Question: does moving the
short strikes off `.10Δ` (to `.05`, `.07`, `.15`), alone or with Touch $10, reduce
bad days (loss ≥ 0.5R) relative to A0? Backtests only; paired by condor-day; R per
position. Rules: `R-2026-10-06-TAIL-SCORING-RULE`, `-TAIL-HOLDOUT`, `-TAIL-FEES-IGNORED`.

## Sources (SHA256 in SHA256SUMS.txt)

| file | test | n | sha256 (first 16) |
|---|---|---|---|
| A0-ride.csv | ZT217913212733763171103 | 825 | 62e42f8860d32735 |
| A3-t10.csv | ZT217913214243169681106 | 825 | 00f70e5216c1aeec |
| D05-ride.csv | ZT217913302687266451310 | 824 | 62d8c261d023c804 |
| D05-t10.csv | ZT217913305943676011317 | 824 | e038d7fc70c795cb |
| D07-ride.csv | ZT217913303682146891313 | 826 | dd4e3a9e8220ebf1 |
| D07-t10.csv | ZT217913307185959691324 | 826 | eb175920e92fd5aa |
| D15-ride.csv | ZT217913304644751371315 | 825 | 6b8e5926be62bb16 |
| D15-t10.csv | ZT217913309624633191333 | 825 | 5ebb85092a80efee |

## Date-set audit vs A0 (not padded)

| arm | n | missing vs A0 | extra vs A0 |
|---|---|---|---|
| A3-t10 | 825 | — | — |
| D05-ride / D05-t10 | 824 | 2025-07-21, 2025-07-25 | 2026-04-09 |
| D07-ride / D07-t10 | 826 | — | 2026-04-09 |
| D15-ride / D15-t10 | 825 | — | — |

2026-04-09 is a date A0 did not trade but both `.05` and `.07` variants did (both
missing/extra identical across ride/t10 pairs → driven by strike availability at
entry, not by the touch leg). D05's two missing dates fall in the holdout window.
All pairing below is on shared dates only.

## Full-period paired results (825 A0 dates, 2021-10 → 2026-10)

| arm | paired n | mean R | % of A0 | bad | fixed | created | p (sign) | gross $ | maxDD R | worst5% R | touches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A0-ride | 825 | +0.0022 | 100% | 95 | — | — | — | 848 | 9.37 | −1.000 | 0 |
| A3-t10 (D10 ref) | 825 | +0.0135 | 614% | 11 | 84 | 0 | 1.0e-25 | 4,691 | 4.08 | −0.469 | 406 |
| D05-ride | 823 | −0.0006 | −27% | 42 | 53 | 0 | 2.2e-16 | −191 | 10.05 | −0.946 | 0 |
| D05-t10 | 823 | +0.0041 | 186% | 16 | 80 | 1 | 6.8e-23 | 1,568 | 4.18 | −0.541 | 117 |
| D07-ride | 825 | −0.0026 | −118% | 62 | 33 | 0 | 2.3e-10 | −997 | 13.38 | −1.000 | 0 |
| D07-t10 | 825 | +0.0000 | 0% | 23 | 73 | 1 | 7.9e-21 | 8 | 4.57 | −0.644 | 223 |
| D15-ride | 825 | +0.0123 | 559% | 153 | 0 | 58 | 6.9e-18 | 3,801 | 11.34 | −1.000 | 0 |
| D15-t10 | 825 | +0.0188 | 855% | 2 | 94 | 1 | 4.8e-27 | 5,992 | 1.57 | −0.245 | 672 |

Note D15-ride: the widest cushion **created 58 bad days** — closer-to-money short
strikes breach more often; a wider credit does not mean a safer trade.

## Selection window (2021-10 → 2024-12; 515 shared dates; A0 mean −0.0098 → guard: arm ≥ control)

| arm | bad | fixed | created | net removed | p | mean R | guard | verdict |
|---|---|---|---|---|---|---|---|---|
| A3-t10 | 5 | 59 | 0 | −59 | 3.5e-18 | +0.0203 | pass | PASS |
| D05-ride | 35 | 29 | 0 | −29 | 3.7e-09 | −0.0146 | **fail** | FAIL |
| D05-t10 | 14 | 50 | 0 | −50 | 1.8e-15 | −0.0050 | pass | PASS |
| D07-ride | 48 | 16 | 0 | −16 | 3.1e-05 | −0.0199 | **fail** | FAIL |
| D07-t10 | 15 | 49 | 0 | −49 | 3.6e-15 | −0.0034 | pass | PASS |
| D15-ride | 106 | 0 | 42 | +42 | 4.5e-13 | −0.0108 | — | FAIL |
| **D15-t10** | **1** | **64** | **1** | **−63** | **3.6e-18** | **+0.0217** | **pass** | **PASS — WINNER** |

## Holdout window (2025-01 → 2026-10; 310 shared dates; A0 mean +0.0221 → guard: arm ≥ +0.0177)

| arm | bad | fixed | created | p | mean R | % of A0 | verdict |
|---|---|---|---|---|---|---|---|
| **D15-t10 (chosen)** | 1 | 30 | 0 | 1.9e-09 | +0.0140 | **63%** | **FAIL — return guard** |
| D05-t10 | 2 | 30 | 1 | 3.0e-08 | +0.0192 | 87% | PASS |
| D05-ride | 7 | 24 | 0 | 1.2e-07 | +0.0230 | 104% | PASS (but failed selection) |
| D07-ride | 14 | 17 | 0 | 1.5e-05 | +0.0261 | 118% | PASS (but failed selection) |
| A3-t10 | 6 | 25 | 0 | 6.0e-08 | +0.0022 | 10% | FAIL |
| D07-t10 | 8 | 24 | 1 | 1.6e-06 | +0.0057 | 26% | FAIL |
| D15-ride | 47 | 0 | 16 | 3.1e-05 | +0.0506 | — | FAIL |

## Verdicts

**Selection winner: D15-t10** (`.15Δ` + Touch $10): most net bad days removed (−63),
p=3.6e-18, return guard passes.

**Holdout confirmation: FAILED.** D15-t10 still eliminates bad days on holdout
(30 fixed / 0 created, p=1.9e-9, worst day −0.51R) but its mean R falls to 63% of
control, below the 80% guard. In the calm 2025–26 regime the $10 touch clips 243
of 310 positions and gives back more premium than it saves.

**Only D05-t10 passes the full rule on both windows** (selection −50 net, p=1.8e-15,
mean ≥ control; holdout −29 net, p=3.0e-8, 87% of control). The rulings do not say
whether a runner-up may be advanced when the winner fails holdout — logged as a
question for Andy rather than decided here.

**No recommendation is made about any bot.** `R-2026-10-06-TAIL-LIVE-CLONE` governs
any eventual live change.

## Fees (informational only — gross decides, per R-2026-10-06-TAIL-FEES-IGNORED)

Fee constant re-derived from rendered Estimated-fees insights:
$2,607/825 = $3.1600 (A0, D15-ride); $2,610.16/826 = $3.16 (D07-ride);
$3,889.96/1,231 = $3.16 (A3); $3,314.84/1,049 = $3.16 (D07-t10);
$4,730.52/1,497 = $3.16 (D15-t10). **$3.16 per transaction, transactions = opens +
touch closes** — matches the T1 estimate exactly.

| arm | transactions | est. fees | gross | est. net |
|---|---|---|---|---|
| A0-ride | 825 | $2,607.00 | +848 | −1,759 |
| A3-t10 | 1,231 | $3,889.96 | +4,691 | +801 |
| D05-ride | 824 | $2,603.84 | −191 | −2,795 |
| D05-t10 | 941 | $2,973.56 | +1,568 | −1,406 |
| D07-ride | 826 | $2,610.16 | −997 | −3,607 |
| D07-t10 | 1,049 | $3,314.84 | +8 | −3,307 |
| D15-ride | 825 | $2,607.00 | +3,801 | +1,194 |
| D15-t10 | 1,497 | $4,730.52 | +5,992 | +1,261 |

Fees exceed gross P/L on 5 of 8 arms. Only touch arms at .10Δ/.15Δ stay positive net.

## Register-day rows

Full verbatim rows are in `01-raw-capture.txt`. Highlights:

- **2026-08-26**: all rides expired ~+5% ROR except D15-ride +19.3%. Touch arms
  mixed: A3 touched out −2 (−0.45%), D07-t10 −53 (−11.2%), D05-t10 escaped
  (+25), D15-t10 touched out +18 (+4.3%).
- **2026-09-30** (max-loss day on every T1 arm): **D05 arms dodged it entirely**
  (+20, expired worthless — strikes outside the range). D07-ride/D07-t10 −100%,
  D15-ride −100%, **D15-t10 touch-exited at 3:48pm for +28 (+7.1%)** — the only
  arm that was both ITM-enough to take the touch and early enough to close green.

## Caveats (carried forward)

- Backtester exits stop around 15:45; late-session breaches after that are
  invisible in every arm equally (T1 finding, restated).
- `R` capped at −1.0 by construction (max loss = risk).
- Position counts differ by strike availability at entry; pairing is on shared
  dates only, never padded.
