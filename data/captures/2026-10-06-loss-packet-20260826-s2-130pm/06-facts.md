# Derived facts — IC-SPX-FastPT25-S2-130PM · 2026-08-26

Facts only; no root cause, no fix. Sources: 01 ledger · 02 OA positions · 03 bot
log · 04 tape (5min) · 05 backtests.

## Per position

| field | put leg | call leg |
|---|---|---|
| side | Short Put Spread (tag `put side`) | Short Call Spread (tag `call side`) |
| short strike | **7,655** (long 7,650) | **7,690** (long 7,695) |
| credit | $0.20 ($200, 10 ct) | $0.40 ($400, 10 ct) |
| open | 1:31PM (ts 17:31:02.845Z) via **Scalp-Scan-Put** (Scanner) | 1:31PM (ts 17:31:04.367Z) via **Scalp-Scan-Call** (Scanner) |
| close time | 3:05PM (trade ts 19:05:04.195Z = 15:05:04 ET) | 3:05PM (trade ts 19:05:01.686Z = 15:05:01 ET) |
| close label | "Close 10 contracts" | "Close 10 contracts" |
| closed by | **Scalp-Mon-S2-Cleanup** (Monitor) | **Scalp-Mon-S2-StrikeTouch** (Monitor) |
| close fill | $0.05 | $2.05 (trades list: "2.05 → 2.10") |
| P/L | **+$150** | **−$1,650** |
| risk (OA) | $4,800 | $4,600 |
| underlying at close (OA "PRICE AT CLOSE") | 7,690.36 | 7,690.64 |
| underlying at close (tape 15:05 bar) | p 7,687.22 · h 7,690.73 · l 7,687.08 | same bar |
| underlying at 16:00 (tape) | 7,675.70 | 7,675.70 |
| would it have expired OTM at 16:00? (tape) | **YES** — 7,675.70 > 7,655 short put | **YES** — 7,675.70 < 7,690 short call |

Net day P/L: −$1,500 (both legs).

## Tape approach table (5min bars, 13:00–16:00; 1min unavailable)

| milestone | put short 7,655 (price above) | call short 7,690 (price below) |
|---|---|---|
| first bar within $20 | 13:00 (l 7,664.15) | 13:15 (h 7,672.79) |
| first bar within $10 | 13:00 (l 7,664.15) | 14:45 (h 7,682.33) |
| first bar at/through strike | never (window) | 15:00 (h 7,690.72) |
| extreme beyond strike | — (min l 7,664.15; stayed 9.15 above strike) | +0.73 (15:05 bar h 7,690.73) |
| 16:00 close | 7,675.70 | 7,675.70 |

## Monitor evaluations (bot log decision text)

| run | put-leg eval | call-leg eval | action |
|---|---|---|---|
| 15:04 Scalp-Mon-S2-StrikeTouch (1/2,2/2) | "below short put strike" → No | "above short call strike" → **No** | none |
| 15:04 Scalp-Mon-S2-Cleanup (1/2,2/2) | open ≥2min Yes / exactly-1-position No | same → No | none |
| 15:05 Scalp-Mon-S2-StrikeTouch (1/2,2/2) | "below short put strike" → No | "above short call strike" → **Yes** | Close Position (call), filled $2.05 at 15:05:01 |
| 15:05 Scalp-Mon-S2-Cleanup (1/1) | open ≥2min Yes / exactly-1-position Yes | (call already closed — loop had 1 item) | Close Position (put), filled $0.05 at 15:05:04 |

## Backtest vs live (single-day, same strikes — STRIKES MATCH, all 11 tests)

| arm | exit option | Aug-26 close | status | P/L (1 ct) |
|---|---|---|---|---|
| A0 ride | None | 4:00pm | Expired | +$55 |
| A1 touch $0 | TOUCH $0 | 4:00pm | Expired | +$55 |
| A2 touch $5 | TOUCH $5.00 | 3:01pm | Touch | −$107 |
| A3 touch $10 | TOUCH $10.00 | 2:47pm | Touch | −$2 |
| A4 sl 100% | STOP LOSS 100% | 3:01pm | Stop Loss | −$107 |
| A5 exp 10m | EXPIRATION 10 minutes | 4:00pm | Expired | +$55 |
| A6 touch $7.50 | TOUCH $7.50 | 2:58pm | Touch | −$22 |
| A7 touch $12.50 | TOUCH $12.50 | 2:46pm | Touch | +$10 |
| A8 touch $15 | TOUCH $15.00 | 1:31pm | Touch | −$5 |
| A9 touch $20 | TOUCH $20.00 | 1:31pm | Touch | −$5 |
| A10 touch $25 | TOUCH $25.00 | 1:31pm | Touch | −$5 |

Live (10 ct, two separate spreads): call leg −$1,650 at 15:05 · put leg +$150 at 15:05.

## Sequence (established by trade timestamps + log iterations)

1. 13:31:02/04 — scanners open put leg ($0.20) and call leg ($0.40).
2. Every minute 13:32–15:04 — StrikeTouch + Cleanup monitors run; all evals No.
3. Between the 15:04 and 15:05 monitor evaluations, underlying crossed above
   the 7,690 short call strike (tape: 15:00 bar h 7,690.72; 15:05 bar h 7,690.73).
4. 15:05:01 — StrikeTouch closes call leg at $2.05 (−$1,650).
5. 15:05:04 — Cleanup sees exactly-1-position (put survivor), closes it at $0.05 (+$150).
6. No further log rows that day (bot flat).
7. By 16:00 tape, SPX = 7,675.70 — inside the condor; both legs would have
   expired OTM.
