# OA CATCH-UP + LAYER 2 — 2026-09-07 — Opus Cowork chat, bot-fleet-v2 + Claude in Chrome

Four trading days are un-ingested (last raw export `data/raw/2026-08-31.csv`; 09-01, 09-02,
09-03, 09-04 missing; 09-07 is Labor Day — `market_calendar.py` knows). The 26-ct sizing landed
2026-09-02 evening and its Layer-2 behavioural check has NEVER been run. This session does the
READ + INGEST leg. Andy commits. A separate Fable session verifies your captures afterward —
so record everything to disk, not to the chat.

## 0 · Setup
1. Invoke `oa-driving`. Read `CLAUDE.md` §4/§5/§9.1, the top of `docs/state.md` (the
   UNVERIFIED-L2 banner), and `docs/RULINGS.md` tail (R-2026-09-03-POSITION-LIMITS-RESCINDED,
   R-2026-09-03-3DTE-POSITION-SIZE-CORRECTION).
2. `git status` must be clean at `d0b4d41` or later. If not, STOP and report.
3. Chrome: tabs_context, new tab, OA must already be logged in (never enter credentials).
   ACCOUNT = Paper Trading on every page. Never select `TR ****4219`.
4. Capture dir `data/captures/<ET-date>-catchup/` (ET date from OA's page header). `SHA256SUMS.txt`
   at the end. NO OA EDITS THIS SESSION — read-only throughout. Any state you think needs
   changing goes in the report as a finding.

## A · Full closed-position export (the ingest input)
OA → Trades/Positions → Export Data, FULL history, closed positions. Save under its DEFAULT
filename to `~/Downloads` (never type a path into the save dialog). Record filename, size,
sha256, row count, min/max closeDate. Expected: rows through 2026-09-04 present.

## B · Roster capture (drift control)
Full `/bots` capture with the same instrument as `data/captures/2026-09-02-gf-sizing/07-roster-POST-*.txt`
(`scripts/oa-driver/oa_grab_page.js`). Save `01-roster-<ts>.txt`. Diff against 09-02 POST:
expected NO config drift — allocations, groups, AUTOS 18/44, EXITS 16/44 identical; only P/L,
open-risk and position-count cells move. Any toggle/allocation/group difference = FINDING.
Also read `a5.bots.allbots` → `02-allbots-<ts>.tsv` (name,id,group,seed,status,disableExits,
posLimit,account,tags) and diff against `06b-allbots-FINAL-2026-09-02-222800.tsv`.

## C · LAYER 2 — the sizing check (the reason this session exists)
For each of `GF-QQQ-IC-Ride`, `-PT50`, `-Trail`, `-Touch0`, `-SL100`, `-SL200`, `-Canary`:
open the bot → TRADES LIST (positions opened on/after 2026-09-03). Record per position:
open date/time · side (put/call spread) · **quantity** · strikes · open price · status/close.
Predicates (state pass/fail per arm, derived from the Trades list, never from Exit Options):
- six arms: every post-09-02 position shows **26 contracts**;
- Canary: every position shows **1 contract** AND its 5% profit target FILLED on at least one
  day (that is the instrument's whole job);
- every arm that traded opened BOTH a put spread and a call spread on the same day at least
  once (the 2/2 limit is not blocking the second side);
- an arm with ZERO positions since 09-03 is a finding, not a pass (the gate chain may have
  filtered every day — read its bot Log for 09-03/09-04 and say which node filtered).
Save `03-layer2-<ts>.md` with the table and the verdict per arm.

## D · Two small read-only follow-ups
1. `3DTE $140-$350`: open its three `xDTE $140-$350 +10` automations and `Early Exits 70%-90%`;
   record whether ANY node sets position size (quantity / % of allocation / % net liq). This
   closes the R-2026-09-03-3DTE-POSITION-SIZE-CORRECTION follow-up either way. Hash each.
2. `GF-QQQ-IC-Ride-Delta`: confirm still AUTOS OFF (it is still attached to the 26-ct shared
   scanners; re-arming would be 26 ct).

## E · Ingest + close, on the Mac (device shell), NO git
`INGEST_DOWNLOADS=~/Downloads scripts/close.sh 2026-09-04` from the repo root. Expect all
stages exit 0 and the manifest to record capture from §B (set `CAPTURE_TXT` to the §B file).
If any stage refuses, STOP — never pass an override flag, never edit a guard. Then run
`scripts/close.sh` for 09-01/09-02/09-03 ONLY if close.sh does not already fold prior missing
days into one run — read `ingest_export.py --help` first and say which it is. Verify:
- STATUS.md cumulative == `git show HEAD:STATUS.md` cumulative + sum of export rows with
  closeDate in 09-01..09-04 and openDate ≥ LEDGER_START (derive both sides, show the arithmetic);
- new ledger rows for the GF arms carry quantity 26 (the ledger's own view of Layer 2);
- `roster.py --check`, `portfolio.py --check`, `pre_registration_ledger.py --selftest` green.

## F · Records
- If §C passes on every arm: replace the UNVERIFIED-L2 banner at the top of `docs/state.md`
  with a dated "L2 VERIFIED" entry citing `03-layer2-*.md`. If any arm fails: leave the banner,
  add the failing arms to it.
- `docs/session-log.md` entry; `docs/state.md` dated section; `data/portfolio.csv` M-37
  (liveness + drift day 1) → Done if §B/§C support it, T-36 note with the 130PM n count.
- Report: files, sha256s, the §B diff verdict, the §C table, the §E arithmetic, findings, and
  the paste-ready `git add … && git commit -m …` line. Never run git.
