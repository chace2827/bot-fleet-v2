# Loss packet — IC-SPX-FastPT25-S2-130PM · 2026-08-27

Purpose: one loss-day fact packet for Cowork's loss-day register — the
S2-130PM condor whose put leg was strike-touched at 14:28 on a dip that
recovered by the bell. Facts only; interpretation is Cowork's job.
Queue item #1 of `docs/devin-queue.md`; spec `docs/dispatch-loss-packet-2026-10-06.md`.

Captured: 2026-10-06 ~18:55–19:35 ET (UTC-4, America/New_York).
Runner: Devin (SWE-2 Max) in Devin Desktop, this repo mounted as local folder.
Browser: dedicated Chrome profile `~/.chrome-oa-profile`, CDP on :9222; Andy
logged in by hand. Account verified Paper Trading (bot header "Paper Trading"
in drawer text; no live indicators seen).

## Files

| file | sha256 | what |
|---|---|---|
| 00-runner-pilot.txt | (see SHA256SUMS.txt) | Calibration diff of PROPOSED-packet-runner.js + PROPOSED-tape.py vs the 08-26 reference bundle — CLEAN; runner quirks recorded |
| 01-ledger.csv | " | `data/trades.csv` header + the 2 verbatim rows for bot/date (T01110, both legs) |
| 02-oa-positions.txt | " | Both OA positions: drawer text verbatim, leg classes, trades list with UTC ids, every Automation Log iteration |
| 03-bot-log.txt | " | Bot-log run list 13:25–16:00 (128 rows verbatim of a 150-row day) + decision texts for all 2:27PM and 2:28PM runs + pre-open scanner texts (1:30PM, 1:45PM) |
| 04-tape-5min.csv | " | Tradier timesales SPX 2026-08-27 13:00–16:00, cols t,p,h,l |
| 05-backtest-rows.txt | " | All 11 tests: names, Settings-card Exit Options lines, grid coverage — and the finding that NO Aug-27 row exists anywhere |
| 06-facts.md | " | Derived facts table (side/strike/credit/close/automation/fill/P-L/underlying/OTM) |
| 07-debrief.md | " | Post-run debrief: per-section timings, §3 load question, v2 changelog |
| PROPOSED-packet-runner-v2.js | " | v2 runner — fixes the 3 quirks from 00-runner-pilot.txt + §2/§5 gap closures + timing instrumentation. Original kept untouched in the 08-26 bundle |
| SHA256SUMS.txt | — | hashes of the above |

## Assumptions

- `/positions/closed` groups rows by close date; the AUG-27 group was paged
  until the next `rowhd` rendered (provably complete), then filtered by bot
  `i[title]`. Two positions found — put + call legs of condor T01110.
- "The minute of each close" = 2:28PM for both legs (put 14:28:00.5, call
  14:28:01.9 per trade timestamps); "the minute before" = 2:27PM. Both monitor
  runs in each minute captured (StrikeTouch + Cleanup), all pager iterations.
- Tape: `1min` requested first per spec — unavailable (~28 trading days back,
  beyond ~20-day retention). Fell back to **`5min`**; interval stated in the
  filename and used everywhere.
- "Would it have expired OTM" judged from the 5-min tape's 16:00 print
  (7,730.99) vs the short strikes.
- OA's "PRICE AT CLOSE" = underlying at position close (7,713.29/.31, inside
  the 14:25 bar's 7,711.38–7,719.48 range), not the 16:00 settlement print.
- Ledger `underlying_close`/`underlying_open` are position-event prints, not
  end-of-day (per reference bundle's question #1).
- §6 approach table counts bars at/after the 13:46:01 open (first bar 13:50),
  per dispatch §4 — see Questions #3 for the reference-shape difference.
- Scratch/CDP helpers lived in `/tmp/lp-20260827/` (outside the repo): copies
  of the PROPOSED scripts (unedited), pilot-s3.js (bot-log decision-text
  capture — the runner emits `openRun` as a callback, not JSON), target-s2.js
  (adds leg classes + trade UTC ids the runner omits), probe-s5.js /
  probe-dates.js (posgrid depth/absence checks). scripts/ + .env copied there
  for the tape call, never into the repo tree.

## Questions for Cowork

1. **The day's opens were 1:46PM, not ~1:31PM.** Scanner decision texts show
   "Symbol change % is less than 0.75 since previous close → No" at 1:30PM and
   1:45PM; all five decisions Yes at 1:46PM. The live scanner re-evaluates
   every minute so the position was eventually opened — the backtester's
   one-shot 1:30pm entry never retried, which is consistent with the missing
   backtest rows (§5). Recorded as verbatim log facts, not interpretation.
2. **No Aug-27 backtest row exists in any of the 11 tests** (A0 verified
   exhaustively to Oct-2021; all 11 first-100 grids reach ~Mar-2026 and show
   zero hits). STRIKES verdict is therefore "cannot be compared" — recorded,
   not filled in.
3. **Approach-table window:** dispatch §4 says count only bars at/after the
   position's open; the reference packet counted from 13:00. This packet's
   table uses post-open bars (put within-$20: 13:50 vs reference-shape 13:25;
   call within-$20: never post-open vs 13:00 full-window). Flagging so the
   register doesn't silently mix conventions.
4. Call-leg open trade reads "0.10 | filled at $0.15" — a ladder notation
   with only the first rung visible; copied verbatim like 08-26's
   "2.05 → 2.10". Put-leg close reads "2.20 → 2.30".
5. Put-leg Exit Options panel renders "PROFIT % / None" with NO high/low
   markers at all (call leg shows 100.0% high / 20.0% low). Verbatim in 02;
   the panel is intent, not evidence (law 1) — noted only as a rendering fact.
6. Leg `title` attributes read absent on both positions (reference bundle
   recorded title="Long"/"Short"); side taken from the `strike flex long|short`
   class, which matches the reference's own classes.
7. `data/trades.csv` read as §1 ledger per spec — the working post-cutover
   ledger here (rows present), not the frozen archive.

## Refusals

- Did not open `data/loss_register.csv`, `docs/loss-day-register.md`, or any
  session-log entries (blind rule).
- No clicks on automation-name links, no automation editors, no Save, no
  `Clear Log`, no `Create Bot`, no backtest run/edit/rename/delete, no
  toggles. Backtest positions accessed via the read-only "showPositions" count
  link only.
- No credentials touched; login was Andy's, in his Chrome window.
- No OA-bound API calls from my code; all reads are DOM/JS of rendered pages.
- No OA exports/downloads.
- No stale-drawer misread recorded — the runner's strike-check and a second
  independent §2 pass returned identical details for both positions.
- The runner process was terminated after its JSON flushed (it holds the CDP
  WebSocket open and never exits — recorded in 00-runner-pilot.txt).
