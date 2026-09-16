# OA SESSION — Opus chat (Cowork/Chrome lane) — 2026-08-31 return sweep

Paste into a NEW Opus chat with Claude in Chrome connected:
"Read `_dispatch-2026-08-31-1-oa-session-cowork.md` in ~/bot-fleet-v2. Execute tasks A–F in
order. READ-ONLY except where a task says Andy may authorize an edit in-chat. Report in the §R
format."

## Discipline (oa-driving skill — violations have caused silent failures)
- Load the `oa-driving` skill FIRST. A version bump is NOT evidence — only the hash is. Three
  save layers; the drawer ✕ DISCARDS; a 45s timeout may be a LOGOUT — re-verify auth.
- Export/save dialogs: save under the DEFAULT filename and `mv` after — never type a path into
  the dialog (colon-mangled artifact trap, seen 08-18/08-19).
- ET date comes from the capture's own `captured:` header, never the filename or shell (UTC trap).
- Context: `_review-2026-08-31-vacation.md` (findings F-1…F-8) and `docs/pre-registration-ledger.md`
  PR-04 entry.

## A · Roster/toggle capture #3 (first — before anything changes state)
Run the roster bookmarklet on /bots; save text capture. Expect the `roster-toggles-44` series'
third bundle. ⚠️ Bot count may now be 45 — "Friday 14 DTE Broken Wing IB (B-70)" (OA-Mirror
family per Andy 2026-08-31) traded 08-14 but is not in bots_meta. A +1 vs the 08-19 bundle is
EXPECTED and must be reported, not "fixed". Derive the toggle TSV only with the (name,bot_id)
cross-check against the 08-19 bundle (positional-join lesson, 08-19). Report drift bot-by-bot
vs 08-19 (last capture was 12 days ago).

## B · PR-04 discharge capture (QQQ-IC-0DTE-Fortress-NoPT50)
Its FIRST trading day happened 2026-08-26 (one condor, put +$104 / call -$442, both legs closed
15:50). The pre-reg entry's SIGNED line is held "unsigned" by the banner only because the
first-trading-day capture is OWED. Capture the 08-26 position's Trades list showing:
(1) a time-exit row present, (2) NO PT row, (3) BACKSTOP_CAUGHT_IT negative — the 15:52 backstop
must NOT be what closed it (closes read 15:50). Precedent: R-2026-08-18 SUBSTITUTE-VERIFY (5a).
Save capture + note sha256. Do NOT edit the ledger — the discharge edit happens in the repo lane
with Andy's authorization, citing this capture.

## C · Ride-Delta double-fire diagnosis (GF-QQQ-IC-Ride-Delta)
Duplicate SAME-SIDE entries seconds apart on 6 of 9 recent trading days (08-25: two CALL
spreads; 08-31: two put spreads). Read its automations; diff scanner configs against sibling
GF-QQQ-IC-Ride (hashes, not versions). Hypothesis to test: a leftover duplicate scanner or
double-added automation from the pre-fix build (bot was "added before the defect was fixed").
Report root cause + proposed minimal fix. EDIT ONLY IF ANDY APPROVES IN-CHAT during the session;
if edited, verified-edit protocol (hash before/after, re-read after save). Andy's 08-31 decision:
fix + RESET its sample count from fix date.

## D · Allocation read — every bot, for the equalization list
From /bots read each bot's allocation (name, alloc $, group). Deliver as a TSV in chat or a
saved capture. Purpose: Andy ruled EQUALIZE WITHIN FAMILIES (GF-QQQ arms · FastPT25 siblings ·
DIR put/call pair · QQQ Fortress arms · mirrors). Known suspects: DIR-SPX-CallVIXdrop $50k vs
put pair $10k; Fortress line $100k. READ ONLY — the edit list is drafted by the manager chat
afterward.

## E · Legacy open-position sweep (F-8)
Open Positions tab: list EVERY position with an open date before 2026-08-10 (LEDGER_START).
Vacation lesson: toggles-OFF stops new entries, not existing exposure — QQQ long call's Jun-1
position expired 08-31 at -$2,971 invisibly. Report symbol, bot, open date, current risk.

## F · 11AM S2 read-only config check (IC-SPX-FastPT25-S2)
On 08-31 BOTH sides expired at full profit (+$200) — first held-to-close day ever, vs the
standing puts-only 2-minute-scratch pattern. Read (don't touch) its exit config and recent
automation history: did anything change ~08-28–08-31?

## R · Report format
Per task: what was captured (path + sha256), findings, anomalies. End with: bot count (44/45?),
toggle drift count vs 08-19, PR-04 evidence verdict (3 checks), Ride-Delta root cause,
allocation TSV, legacy opens list, S2 config delta y/n.
