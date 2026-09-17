# 02 — Stage 1 derived metrics (R-normalized)

Derived from raw exports (unmodified). Sources + SHA-256:

| Source file | SHA-256 |
|---|---|
| standalone-S1-0.csv | 229c5a3d6b8f39b3c59719485d0e212379cc7e983c2ff6e2b09cecbaf9c291df |
| standalone-S1-a.csv | 79c01c34379b48cd21ddbf96c062960ddccbf1848579f83d628920126591fea4 |
| standalone-S1-b.csv | 4aed3fca450c828266eb0dc68059096c713745f1f5f909db5b26a6b386c45048 |
| standalone-S1-c.csv | 7c9560c4e7aecb50822ed4f1779a05e41b0faef7b7f8a70afe4d98dff31cd280 |
| combined-S1-H.csv | 33a3415567e875e4e9d4a69cb54d3d4a59e063d80a68e5b551cf3708a5487071 |

Method: R per row = `P/L ÷ Risk` (export columns). Exp(R) = mean. Win rate =
share of rows with P/L > 0. Max drawdown in R = max peak-to-trough decline of
the cumulative-R series ordered by `Closed`. Worst single R = min row R.
Row counts from a CSV parser (OA exports carry no trailing newline).

| Arm | N | Exp(R) | Win rate | Max DD (R) | Worst single R | Unit |
|---|---|---|---|---|---|---|
| S1-0 | 353 positions | +0.0367 | 84.70% | 5.38 | −1.00 | per IC position |
| S1-a (SL 100%) | 353 positions | +0.0323 | 72.24% | 4.16 | −1.00 | per IC position |
| S1-b (SL 200%) | 353 positions | +0.0382 | 80.74% | 5.28 | −1.00 | per IC position |
| S1-c (put overlay, standalone) | 1,109 positions | −0.2047 | 16.41% | 253.91 | −1.00 | per debit-spread position |
| S1-H (S1-0 ⊕ S1-c, gated `is open`) | 353 condors (316 paired) | −0.0019 | 35.41% | 8.28 | −1.00 | **per condor, denominator = primary risk + overlay debit, ex-artifact** |

S1-H denominator, written out per dispatch: each combined position-day is one
primary iron condor; on the 316 days the overlay also opened, that condor's
risk = primary Risk + overlay debit (overlay `Risk` column = debit paid, equal
to `Premium`). On the 37 unpaired days the condor carries primary risk only.

Row-status split (sanity): S1-0 {expired 353} · S1-a {expired 287, stoploss
66} · S1-b {expired 327, stoploss 26} · S1-c {expired 1109}. Stop-armed arms
still contain −1R rows (14 in S1-a, 20 in S1-b) — the stop never marked
intraday on those days; row-level status is `expired`.

Reconciliation caveat that moves the number: 21 combined-B rows were silently
dropped (see 01-capture §7). Their standalone P/L sums to **+$580** on $715
debit. As-exported S1-H Exp(R) = −0.0019 R/condor; had those rows been
included, the condor-level total P/L would have been ~$663 rather than $83.
The export understates overlay contribution; the delta is reported, not
absorbed, and S1-H figures above are exactly what the export contains.
