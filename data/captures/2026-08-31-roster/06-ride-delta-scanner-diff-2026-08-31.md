# Ride-Delta double-fire — root-cause diagnosis (dispatch task C)
Captured 2026-08-31 ~17:37–17:50 ET, Claude in Chrome, READ-ONLY. No OA edits made.
Bot: GF-QQQ-IC-Ride-Delta  BOTfw5TkkCRF1317864858068078811
Sibling/control: GF-QQQ-IC-Ride  BOTfw5TkkCRF4417860701930934951

## 1. Automation inventory (settings page, i.sticon title attributes)
GF-QQQ-IC-Ride-Delta — 5 automations, ALL "Automation is on":
  SCANNERS  GF-ScannerA-PutSpread   (shared library) 1 input
            GF-ScannerB-CallSpread  (shared library) 1 input
            Ride-Delta-Scan-Put     (bot-local)      1 input
            Ride-Delta-Scan-Call    (bot-local)      2 inputs
  TRIGGERS  GF-Backstop-1552-FlatClose  Mon-Fri 3:52pm EST

GF-QQQ-IC-Ride (control) — 3 automations:
  SCANNERS  GF-ScannerA-PutSpread, GF-ScannerB-CallSpread
  TRIGGERS  GF-Backstop-1552-FlatClose

=> Ride-Delta carries TWO put-side scanners and TWO call-side scanners.
   The control carries one of each. This is the whole defect.

## 2. Config hashes — sha256(JSON.stringify({name,inputs,root})), read fresh per automation
   (hard reload between opens; a5.bots.acedit.routine, never a DOM read)

GF-ScannerA-PutSpread   1e5eb9936a1adf067af65a4841d42e755592f7c179f3c0cad477502dfdbfcdc8  (len 5379)
GF-ScannerB-CallSpread  a925d490b8a0d2337566f47307fc52470da129935d3bd83d24389c6dc433dfb5  (len 5044)
Ride-Delta-Scan-Put     a8643224fa99a7f79286aa81ce487cd64cace272442c2c55f9ccb7d5d9f3db86  (len 5133)
Ride-Delta-Scan-Call    4f7251025257d95d1ee49de48b115a5b6a50cb98bd77434e937a60d141cee967  (len 5271)

The two shared hashes are BYTE-IDENTICAL to the "CONFIG HASH ScannerA v12 / ScannerB v4"
values stamped in GF-QQQ-IC-Ride's own bot Notes (ruling R-2026-08-17-GF-ENTRY-METHOD).
=> The shared library pair is unmodified and at the ruled delta-0.10 config.
=> The two bot-local scanners are the additions.

## 3. Behaviour diff — the bot-local scanners are FUNCTIONAL DUPLICATES, not a variant
Gate chains (verbatim node text) are identical across the matching pair:
  after 1:30pm / before 2:00pm / symbol change % > -0.75 / symbol change % < 0.75 /
  "Bot opened a position with <put|call> side today" -> NO branch opens
Actions are identical:
  put:  open-shortputspread   1 contract, exactly 0 days, $2.00 below short put leg, -.10 delta
  call: open-shortcallspread  1 contract, exactly 0 days, $2.00 above short call leg, .10 delta
Only cosmetic differences: node ids, and Ride-Delta-Scan-Call carries a vestigial second
input (GF_EXITS_PUT) it does not use.
=> Ride-Delta has NO distinguishing variable vs GF-QQQ-IC-Ride. It is a duplicate arm
   running its entry logic twice, not a delta variant.

## 4. Behavioural proof — bot Log, 2026-08-31 (capture 05-ride-delta-log-2026-08-31.txt)
  1:39PM  Ride-Delta-Scan-Put      1 OPEN POSITION   5 decisions  1 loop
  1:39PM  Ride-Delta-Scan-Call     1 filtered position
  1:39PM  GF-ScannerB-CallSpread   1 filtered position
  1:39PM  GF-ScannerA-PutSpread    1 OPEN POSITION   5 decisions  1 loop
Positions (drawer, Trades list): both QQQ 712/710 Short Put Spread, both "Open 1 contract -
Aug 31, 2026 1:39PM", price at open 714.42 and 714.43, both tagged "put side".

MECHANISM: the `postagtoday` gate is evaluated inside the same 1-minute scan tick by both
put scanners. Neither position exists yet when the other evaluates, so both pass the gate
and both open. The gate cannot arbitrate between two automations; it only prevents a
SECOND fire by the SAME automation on a LATER tick.

## 5. Second-order damage (not previously recorded)
Safeguards: DAILY POSITIONS 2 per day, POSITION LIMIT 2 at once.
Two same-side fires consume the entire daily budget, so the opposite side is blocked for
the rest of the day. 2026-08-31 closed BOTH sides as put spreads and no call side traded.
=> The double-fire does not merely double the winners (F-3); on double-fire days it
   DESTROYS THE CONDOR, leaving a naked one-sided position. The arm's realised P/L is
   therefore not a doubled version of the intended strategy — it is a different strategy.

## 6. Proposed minimal fix (NOT APPLIED — awaiting Andy)
Turn OFF (do not delete) Ride-Delta-Scan-Put and Ride-Delta-Scan-Call on this bot only.
  - Leaves the shared library ScannerA/B untouched -> no blast radius to the other GF arms.
  - Leaves the two automations in place for forensics; hashes above are the before-state.
  - Restores 1 put + 1 call per day and makes Ride-Delta byte-comparable to GF-QQQ-IC-Ride.
CONSEQUENCE ANDY MUST RULE ON: after the fix Ride-Delta is configurationally IDENTICAL to
GF-QQQ-IC-Ride. It is not a delta arm; it is a duplicate control. Fixing it produces a
second copy of PR-14 rather than a distinct experiment.
Per Andy's 2026-08-31 decision the sample count resets from the fix date; on the reading
above the pre-fix sample is not merely contaminated, it is a different strategy and should
be excluded, not discounted.
