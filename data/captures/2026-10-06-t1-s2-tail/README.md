# T1 — S2-shape tail test, results (Cowork built-in browser, 2026-10-06 ~17:10–17:40 ET)

Spec (pre-registered before any run): `docs/tail-test-s2-2026-10-06.md`. Scoring: `R-2026-10-06-TAIL-SCORING-RULE`.
Paper account. Backtests only — no bot touched. Built via New Backtest (A0) then Compare → ⋮ → Add Variation
(exit field the only change, verified from each drawer's serialized inputs before Run).

## Tests (OA ids — persist in OA; raw positions re-exportable from each test page)
| arm | name | id | exit field |
|---|---|---|---|
| A0 | ZZ-COWORK-2026-10-06-T1-A0-ride | ZT217913212733763171103 | none |
| A1 | ZZ-COWORK-2026-10-06-T1-A1-touch0 | ZT217913213667172591104 | touch {"type":"usd","value":0} |
| A2 | ZZ-COWORK-2026-10-06-T1-A2-touch5 | ZT217913214071275321105 | touch {"type":"usd","value":5} |
| A3 | ZZ-COWORK-2026-10-06-T1-A3-touch10 | ZT217913214243169681106 | touch {"type":"usd","value":10} |
| A4 | ZZ-COWORK-2026-10-06-T1-A4-sl100 | ZT217913214629138811108 | stoplosssh=1 |
| A5 | ZZ-COWORK-2026-10-06-T1-A5-exp10m | ZT217913214854667371110 | exp=m10 |
Compare URL: /backtests/compare/ZT217913212733763171103,ZT217913213667172591104,ZT217913214071275321105,ZT217913214243169681106,ZT217913214629138811108,ZT217913214854667371110

Base (serialized, A0): SPX ironcondor · 0 DTE · shortPut −.10 delta closest · longPut $5 below · shortCall .10 delta
· longCall $5 above · 1 contract · time 13:30 · Change % −0.75..0.75 · period 5y · posLimit 1 · default slippage/bid-ask.
Window 2021-10-06 → 2026-10-05, **825 positions per arm, identical date sets (verified)**. Avg risk $441, credit $61.
**Replication check:** the backtest's 09-30 condor = 7660/7665 P · 7725/7730 C — the live 130PM put strikes exactly.

## Results — R per condor-day, paired vs A0 (DOM read of every arm's full positions list, 825/825 rows parsed)
| arm | bad days (≤−0.5R) | fixed / created | sign p | mean R | keeps % of A0 | total P/L | max DD (R) | worst-5% mean | verdict |
|---|---|---|---|---|---|---|---|---|---|
| A0 ride | 95 | — | — | +0.0022 | 100 | $848 | 9.37 | −1.00 | control |
| A1 touch $0 | 58 | 42 / 5 | 2.5e-8 | +0.0028 | 128 | $1,013 | 6.44 | −0.99 | PASS |
| A2 touch $5 | 29 | 67 / 1 | 4.7e-19 | +0.0048 | 223 | $1,766 | 4.40 | −0.79 | PASS |
| **A3 touch $10** | **11** | **84 / 0** | **1e-25** | **+0.0135** | **620** | **$4,691** | **4.08** | **−0.47** | **PASS — WINNER** |
| A4 SL −100% | 21 | 75 / 1 | 2e-21 | +0.0041 | 191 | $1,535 | 4.21 | −0.64 | PASS |
| A5 close 10m pre-close | 92 | 3 / 0 | 0.25 | +0.0035 | 161 | $1,351 | 9.09 | −1.00 | FAIL (p) |
Specific days (P/L, 1 contract): 09-18 A0 −$450 · A1 −$197 · A2 −$127 · A3 −$42 · A4 −$127 · A5 −$182.
09-30: **−$437 (max loss) on EVERY arm.**

## ⛔ Caveats that bind the reading
1. **The backtester stops evaluating exits ~3:45pm.** Latest Touch close in A3's 406 touch exits = **3:43pm**; A5's
   "10 min before close" closed only 28 positions (only when ITM at 3:50). So **late breaches like 09-30 are
   invisible to every arm here** — SPX was within $10 of 7665 from 15:50 and live Exit Options run to 15:59, but the
   backtest cannot show it. These results measure breaches before ~3:45 only.
2. A0's edge is ~zero over 5 years (mean +0.0022 R, PF 1.02): the S2 shape's backtested income is the exits', not the ride's.
3. Single IC vs live paired spreads + Cleanup scratch; no FOMC skip; backtest fills.
4. Mean-R significance is not claimed (MDE far above these means); the deciding test is the paired bad-day count.
Raw CSVs not downloaded (download needs Andy's OK); per-day data was read from the DOM into the page session,
scored in-page, then cleared.

---
# T1b — buffer sweep + 11:00 entry (same session, ~17:55–18:25 ET)
Tests (config re-read from each test page's Settings card before scoring — entry time + Exit Options line):
13:30 vs A0: A6 $7.50 ZT217913221146838271122 · A7 $12.50 ZT217913221268980491124 · A8 $15 ZT217913221505807901126 ·
A9 $20 ZT217913221702251821127 · A10 $25 ZT217913221818381131128.
11:00: B0 ride ZT217913222049733751130 · B1 $5 ZT217913222373382861132 · B2 $10 ZT217913222495258171133 ·
B3 $15 ZT217913222671105881135 · B4 $20 ZT217913222793032421136. 13:30 n=825, 11:00 n=875 (page COUNT matched), same window.

Fees: OA estimates **$3.16 per 1-lot IC transaction** (open or close) — derived from two pages: A0 $2,607/825 opens;
B4 $5,008/(875 opens + 710 touch closes). Backtest P/L is GROSS of fees. Net column = P/L − $3.16 × (opens + closes).

## 13:30 (S2-130PM shape) vs A0
| arm | bad | fixed/created | keeps % | gross P/L | est. net of fees | max DD R | touches | 09-18 | 09-30 |
|---|---|---|---|---|---|---|---|---|---|
| A0 ride | 95 | — | 100 | $848 | −$1,759 | 9.37 | 0 | −450 | −437 |
| A6 $7.50 | 17 | 78/0 | 453 | $3,599 | +$66 | 3.89 | 293 | −127 | −437 |
| A3 $10 | 11 | 84/0 | 620 | $4,691 | **+$801** | 4.08 | 406 | −42 | −437 |
| A7 $12.50 | 9 | 86/0 | 398 | $2,957 | −$1,337 | 3.95 | 534 | −10 | −437 |
| A8 $15 | 7 | 88/0 | 228 | $1,673 | −$2,941 | 3.03 | 635 | +15 | −437 |
| A9 $20 | **0** | **95/0** | 415 | $3,144 | −$1,817 | **1.32** | 745 | +3 | **+8** |
| A10 $25 | 0 | 95/0 | 240 | $1,824 | −$3,286 | 0.54 | 792 | +3 | +3 |
All pass the signed rule. **By the rule as signed (gross R), A9 Touch $20 WINS** (95 fixed/0, tie with A10 broken on mean).
⚠ Touch $20 closes on 90% of days (745/825): it is close to an intraday scratch strategy and carries ~2× the fee load.
**Net of OA's fee estimate only A3 $10 (+$801) and A6 $7.50 (+$66) are positive.** The rule does not see fees.
$20/$25 catch 09-30 because their buffer is crossed before the backtester's exit cutoff (~15:45).

## 11:00 (PR-01 shape) vs B0
| arm | bad | fixed/created | keeps % | gross P/L | est. net | max DD R | touches |
|---|---|---|---|---|---|---|---|
| B0 ride | 117 | — | 100 | $926 | −$1,839 | 15.63 | 0 |
| B1 $5 | 31 | 87/1 | 68 | $654 | −$2,885 | 6.24 | 245 |
| B2 $10 | 17 | 101/1 | −191 | −$1,805 | −$5,894 | 9.27 | 419 |
| B3 $15 | 11 | 106/0 | −93 | −$823 | −$5,392 | 4.86 | 571 |
| B4 $20 | 7 | 110/0 | −69 | −$588 | −$5,597 | 4.32 | 710 |
**No 11:00 arm passes** — every one fails the 80% return floor. The 11:00 ride itself: 117 bad days, max DD 15.6R,
mean +0.0025R gross, negative net. A touch exit cannot rescue this shape; it trades the tail for the income.
