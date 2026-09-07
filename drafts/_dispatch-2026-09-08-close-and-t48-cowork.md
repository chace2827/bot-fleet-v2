# CLOSE 2026-09-08 + T-48 GF CALL-SIDE STUDY — Opus Cowork chat, bot-fleet-v2 + Claude in Chrome

Read-only on OA throughout. No edit, no toggle. Andy commits. A Fable session verifies your
files afterward — so every result lands as a file before you move on.
Start after the 09-08 close (~16:15 ET) so the export is complete. Andy drops the export into
the chat (Cowork cannot reach ~/Downloads); export must be "since 2026-08-01", no bot-group filter.

## 0 · Setup
1. Invoke `oa-driving`. Read `CLAUDE.md` §4/§5/§9.1; the top of `docs/state.md`; RULINGS.md tail
   (R-2026-09-07-GF-CALL-SIDE-SHAPE, -P3-…, -P1-…, -P2-…). Read
   `data/captures/2026-09-07-catchup/03-layer2-2026-09-07.md` §3-4 — that is the method for the
   Log reads (URL params `/log?date=YYYY-MM-DD&time=1330-1400`), reuse it.
2. `git status` clean at `6ce3567` or later, else STOP. Chrome: tabs_context, own tab, OA already
   logged in (Browser 2 last time), ACCOUNT = Paper Trading on every page, never `TR ****4219`.
3. Capture dir `data/captures/2026-09-08-close/` with `SHA256SUMS.txt` at the end. Known trap:
   the browser tool result truncates ~1KB silently — chunk with rolling checksums as on 09-07.

## A · Routine close (the 09-07 pattern, one day)
1. Roster capture (`oa_grab_page.js`) → `01-roster-<ts>.txt`; `a5.bots.allbots` → `02-allbots.tsv`;
   signature-diff both against `data/captures/2026-09-07-roster/` → expect zero config drift,
   AUTOS 18/44, EXITS 16/44. Any drift = finding.
2. Save Andy's export to `_inbox/oa-export-2026-09-08.csv`; check min openDate ≤ 2026-08-10 and
   row count ≥ the 09-07 file's; then `INGEST_DOWNLOADS=_inbox CAPTURE_TXT=<01 file>
   scripts/close.sh 2026-09-08`. All stages exit 0, no override. Verify STATUS.md cumulative ==
   `git show HEAD:STATUS.md` cumulative + export rows closing 09-08 with openDate ≥ LEDGER_START
   (show both sides). Note: the manifest will still say capture ABSENT (T-46 open) — record, don't fix.
3. P3 bet inputs, from today's Trades lists on the seven GF arms: per arm, positions opened 09-08,
   qty, side(s), open/close price, P/L. Both-sides? y/n. Append one row per arm to
   `data/captures/2026-09-08-close/03-gf-daily-shape.tsv` (date, arm, put_qty, call_qty, both,
   call_filter_reason). This file is the P3 bet's daily input from now on.
4. T-36 check: 130PM clean-condor count from the readiness board after the close. If n ≥ 20,
   write the G2/G3 result verbatim into the report (CI bounds) — do NOT change any board status;
   Andy rules.

## B · T-48 — GF call-side study (the decision-3 data)
Goal: every GF fill-day since 2026-08-10, what ScannerB did with the call side, and why.
⭐ READ FIRST: `drafts/_t48-ledger-prep-2026-09-07.md` — the ledger half is DONE (11 fill-days,
36.4% put-only, seven arms in lockstep, Ride-Delta separate). Its key finding: 70 of 126 GF legs
filled at EXACTLY $0.07 including 28 CALL legs, so "Filtered: Mid price is $0.07" cannot be a
plain mid < $0.07 rule. Two hypotheses it could not separate: (i) a quantity interaction (09-04
was the first 26-ct day), (ii) the filter reads a pre-fill mid that differs from the booked
credit. START THE LOG READ AT 09-04 and 09-02 (26 ct vs 1 ct, same scanner) — that pair is
decisive. Do not redo B.1; cite the prep file.
1. From `data/trades.csv`, list fill-days for `GF-QQQ-IC-Ride` (the control; the family shares
   the scanners): expect 08-14, 08-17, 08-19, 08-20, 08-21, 08-25, 08-26, 08-28, 08-31, 09-02,
   09-04 (+ 09-08). Mark each both / put-only / call-only from the ledger first.
2. For each day, open Ride's Log with `/log?date=<day>&time=1330-1400` and read
   `GF-ScannerB-CallSpread`'s decisions: gate outcomes (range %, time window, "opened a position
   with call side today"), whether an order was built (strikes), and the terminal reason
   (filled / "Filtered: Mid price is $X" / no candidate / other). Record the credit $X and the
   short-call delta/strike vs spot. Do the same for ScannerA on the put-only days (why did the
   put fill when the call didn't — credit at the same moment). OA Log retention may be short:
   any day whose Log is gone is recorded as LOG-UNAVAILABLE, not inferred.
3. Also read, once, the current ScannerB config from the Library (fresh open, hard reload):
   the credit/price filter node text and threshold, the short-call delta, the wing width; hash it
   and confirm it equals the 09-02 POST hash `a1a48af1…` (no change since sizing).
4. Write `04-t48-call-side-study.md`: a table (day · ledger shape · ScannerB terminal reason ·
   credit · delta/strike · QQQ move that day · put credit same minute), the put-only rate, the
   realised naked-side P/L on put-only days (from the ledger), and a one-paragraph reading of the
   mechanism (is $0.07 the floor's own value, and how often would $0.05 / $0.06 have cleared?).
   State what you could NOT observe. No recommendation to change OA — options were tabled in the
   ruling; you supply the data.

## C · Records (Andy commits)
`docs/session-log.md` entry; `docs/state.md` dated section (close + T-48 headline);
`data/portfolio.csv`: T-48 → Ready for review citing the study file; M-37 untouched (Done).
Report: files + sha256s, drift verdict, ingest arithmetic, GF daily-shape rows, T-36 count,
T-48 table headline, findings, paste-ready `git add … && git commit -m …`. Never run git.
