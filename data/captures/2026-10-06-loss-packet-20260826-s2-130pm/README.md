# Loss packet — IC-SPX-FastPT25-S2-130PM · 2026-08-26

Purpose: one loss-day fact packet for Cowork's calibration — the S2-130PM condor
whose call leg was stopped at 15:05 on a strike touch that retreated by the bell.
Facts only; interpretation is Cowork's job.

Captured: 2026-10-06 ~18:05–18:45 ET (UTC-4, America/New_York).
Runner: Devin (SWE-2 Max) in Devin Desktop, this repo mounted as local folder.
Browser: dedicated Chrome profile `~/.chrome-oa-profile`, CDP on :9222; Andy
logged in by hand. Account verified Paper Trading on `/home` (PAPER badge) and on
the bot header (`ACCOUNT Paper Trading`) before every read.

## Files

| file | sha256 | what |
|---|---|---|
| 01-ledger.csv | (see SHA256SUMS.txt) | `data/trades.csv` header + the 2 verbatim rows for bot/date (T01125, both legs) |
| 02-oa-positions.txt | " | Both OA positions: drawer text verbatim, leg long/short classes, trades list, every Automation Log iteration |
| 03-bot-log.txt | " | Bot log run list 13:25–16:00 (202 rows verbatim) + decision text for all 3:04PM and 3:05PM runs, all pager iterations |
| 04-tape-5min.csv | " | Tradier timesales SPX 2026-08-26 13:00–16:00, cols t,p,h,l |
| 05-backtest-rows.txt | " | 11 test pages: name, Settings-card Exit Options line, verbatim Aug-26 row, leg classes, STRIKES MATCH |
| 06-facts.md | " | Derived facts table (side/strike/credit/close/automation/fill/P-L/underlying/OTM) |
| SHA256SUMS.txt | — | hashes of the above |

## Assumptions

- `/positions/closed` groups rows by **close date**; the target positions
  (opened+closed Aug 26) were found in the complete AUG 26 group after loading
  through the AUG 25 boundary (390 rows).
- The bot-log Date filter only presets 3 weeks of weekdays (oldest: Mon, Sep 14).
  The Aug-26 log was reached via `/bots/bot/<id>/log?date=2026-08-26` — a URL the
  log view itself honored; still a UI read path, no RPC.
- "The minute of each close" = 3:05PM for both legs (call 15:05:01, put 15:05:04
  per trade timestamps); "the minute before" = 3:04PM. Both runs in each minute
  were captured (StrikeTouch + Cleanup).
- Tape: requested `1min` first per spec — HTTP 400 (Aug-26 is ~29 trading days
  back, beyond the ~20-day 1min retention). Fell back to **`5min`**; interval
  stated in filename and used everywhere.
- "Would it have expired OTM" is judged from the 5-min tape's 16:00 print
  (7,675.70) vs the short strikes.
- OA's "PRICE AT CLOSE" = underlying at position close (≈7,690.4–.6, inside the
  15:05 bar's 7,687.08–7,690.73 range), not the 16:00 settlement print.
- Backtest positions = single 1-contract iron condor, $445 risk — a different
  position structure than live (two 10-lot spreads, $4.6–4.8k risk/side) but the
  same four strikes.
- Scratch/CDP helpers lived in `/tmp/lp-20260826/` (outside the repo), per spec;
  scripts/ + .env were copied there for the tape call, never into the repo tree.

## Questions for Cowork

1. Ledger `underlying_close` (7,690.36/7,690.64) = price at **position** close,
   matching OA's "PRICE AT CLOSE" — not the 16:00 underlying (tape 7,675.70).
   Worth flagging in any downstream consumer that reads it as end-of-day.
2. The StrikeTouch condition fired on a single 1-minute evaluation ("underlying
   price is above short call strike price" → Yes at 15:05, No at 15:04). Tape
   shows the breach was real but shallow (+0.73 max, gone by 16:00).
3. Backtest "TOUCH $N" semantics are not documented in this packet — verbatim
   Settings lines only. Whether $N measures underlying-distance-to-strike vs
   position-value was not verified on the page.
4. A8/A9/A10 show "Touch 1:31pm" — one minute after entry — consistent with the
   1:30pm underlying (~7,675) already being within $15–$25 of the 7,690 call
   strike at entry; recorded as observed, not interpreted.
5. Put leg fill $0.05 (Cleanup scratch) vs call leg "2.05 → 2.10" ladder
   notation — the arrow text was captured verbatim from the trades list.
6. `data/trades.csv` was read as the §1 ledger per spec; per CLAUDE.md §3 it is
   the working post-cutover ledger here (rows present), not the frozen archive.

## Refusals

- Did not open `data/loss_register.csv`, `docs/loss-day-register.md`, or any
  2026-10-06 session-log entries (blind rule). The existence of
  `data/captures/2026-10-06-t1-s2-tail/` was noted only for its README's test-URL
  pattern (`/backtests/test/<id>`), after the landing URL failed; its findings
  were not read into this packet's conclusions. (The README was read once to
  obtain the URL pattern; names/exit-fields were independently re-verified on
  each test page itself and are the packet's only source.)
- No clicks on automation-name links, no automation editors, no Save, no
  `Clear Log`, no `Create Bot`, no backtest run/edit/rename/delete, no toggles.
- No credentials touched; login was Andy's, in his Chrome window.
- No OA-bound API calls from my code; all reads are DOM/JS of rendered pages.
- No OA exports/downloads (export needs Andy's OK per convention).
- One accidental stale-drawer read (put details returned on the call row) was
  detected and discarded — re-opened and verified before recording (02 notes).
