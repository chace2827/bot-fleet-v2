# Derived facts — IC-SPX-FastPT25-S2-130PM · 2026-08-27

Facts only; no root cause, no fix. Sources: 01 ledger · 02 OA positions · 03 bot
log · 04 tape (5min) · 05 backtests.

## Per position

| field | put leg | call leg |
|---|---|---|
| side | Short Put Spread (tag `put side`) | Short Call Spread (tag `call side`) |
| short strike | **7,715** (long 7,710) | **7,755** (long 7,760) |
| credit | $0.30 ($300, 10 ct) | $0.15 ($150, 10 ct) |
| open | 1:46PM (ts 17:46:01.038Z) via **Scalp-Scan-Put** (Scanner) | 1:46PM (ts 17:46:02.702Z) via **Scalp-Scan-Call** (Scanner) |
| close time | 2:28PM (trade ts 18:28:00.506Z = 14:28:00.5 ET) | 2:28PM (trade ts 18:28:01.897Z = 14:28:01.9 ET) |
| close label | "Close 10 contracts" | "Close 10 contracts" |
| closed by | **Scalp-Mon-S2-StrikeTouch** (Monitor) | **Scalp-Mon-S2-Cleanup** (Monitor) |
| close fill | $2.20 (trades list: "2.20 → 2.30") | $0.05 |
| P/L | **−$1,900** | **+$100** |
| risk (OA) | $4,700 | $4,850 |
| underlying at close (OA "PRICE AT CLOSE") | 7,713.29 | 7,713.31 |
| underlying at close (tape 14:25 bar) | p 7,712.38 · h 7,719.48 · l 7,711.38 | same bar |
| underlying at 16:00 (tape) | 7,730.99 | 7,730.99 |
| would it have expired OTM at 16:00? (tape) | **YES** — 7,730.99 > 7,715 short put | **YES** — 7,730.99 < 7,755 short call |

Net day P/L: −$1,800 (both legs).

## Entry timing (verbatim bot-log facts)

- Day-filtered log: 150 rows, 1:14PM → 2:28PM. Scanners ran every minute;
  pre-open rows read "2 decisions | 1 loop" vs the 1:46PM rows' "1 open
  position | 5 decisions | 1 loop".
- 1:30PM Scalp-Scan-Put/Call (both): "Symbol change % is greater than -0.75
  since previous close" → Yes · "…is less than 0.75 since previous close" →
  **No** → End (no open).
- 1:45PM Scalp-Scan-Put/Call (both): identical — the less-than-0.75 gate still
  **No**.
- 1:46PM Scalp-Scan-Put/Call (open-trade logs, from §2): all five decisions
  Yes → Open Position.

## Tape approach table (5min bars, 13:00–16:00; 1min unavailable)

Per dispatch §4, counting only bars at or after the position's open (13:46:01;
first qualifying bar is 13:50). The reference packet's table was full-window —
see Questions #3.

| milestone | put short 7,715 (price above) | call short 7,755 (price below) |
|---|---|---|
| first bar within $20 | 13:50 (l 7,730.28) | never post-open (full-window: 13:00, h 7,739.47) |
| first bar within $10 | 14:00 (l 7,723.68) | never (window) |
| first bar at/through strike | 14:25 (l 7,711.38) | never (window) |
| extreme beyond strike | −4.83 (min l 7,710.17) | — (post-open max h 7,732.86; stayed 22.14 below strike) |
| 16:00 close | 7,730.99 | 7,730.99 |

## Monitor evaluations (bot log decision text)

| run | put-leg eval | call-leg eval | action |
|---|---|---|---|
| 2:27PM Scalp-Mon-S2-StrikeTouch (1/2,2/2) | "below short put strike" → No | "above short call strike" → No | none |
| 2:27PM Scalp-Mon-S2-Cleanup (1/2,2/2) | open ≥2min Yes / exactly-1-position No | same → No | none |
| 2:28PM Scalp-Mon-S2-StrikeTouch (1/2,2/2) | "below short put strike" → **Yes** | "above short call strike" → No | Close Position (put), filled $2.20 at 14:28:00.5 |
| 2:28PM Scalp-Mon-S2-Cleanup (1/1) | (put already closed — loop had 1 item) | open ≥2min Yes / exactly-1-position Yes | Close Position (call), filled $0.05 at 14:28:01.9 |

## Backtests

No Aug-27 row exists in any of the 11 tests (verified: all loaded grids
filtered; A0 paged to exhaustion — 825 rows back to Oct 6, 2021 — with Aug 28
and Aug 26 present either side of the gap). The 13:30-set entry is a one-shot
1:30pm trigger behind the same CHANGE % −0.75…+0.75 filter that the live
scanner logs show failing at 1:30PM and 1:45PM. Strikes cannot be compared.

## Sequence (established by trade timestamps + log iterations)

1. From ≥1:14PM — both scanners run every minute; the "<0.75% change" gate
   fails (2-decision rows). SPX is up more than +0.75% vs previous close.
2. 1:46PM — the gate passes; Scalp-Scan-Put opens the put leg ($0.30, ts
   :01.038), Scalp-Scan-Call the call leg ($0.15, ts :02.702).
3. Every minute 1:47–2:27PM — StrikeTouch + Cleanup monitors run; all evals No.
4. Between the 2:27PM and 2:28PM evaluations, underlying crossed below the
   7,715 short put strike (tape: 14:25 bar l 7,711.38).
5. 14:28:00.5 — StrikeTouch closes the put leg at $2.20 (−$1,900).
6. 14:28:01.9 — Cleanup sees exactly-1-position (call survivor), closes it at
   $0.05 (+$100).
7. No further log rows that day (bot flat).
8. By the 16:00 tape print SPX = 7,730.99 — inside the condor; both legs would
   have expired OTM.

## Same-shape note vs the 2026-08-26 packet

Mirror image: on 08-26 the CALL leg was strike-touched at 15:05 (underlying
pushed UP through 7,690, retreated by the bell); on 08-27 the PUT leg was
strike-touched at 14:28 (underlying pushed DOWN through 7,715, recovered by
the bell). Both days: touched leg loses ~$1.7–1.9k, survivor leg wins
+$100–150, both legs would have expired OTM at 16:00.
