# Capture bundle — 2026-08-31 return sweep (OA session, dispatch tasks A–F)

Trading day **2026-08-31** (ET date taken from each capture's own `captured:` header, never the
filename or the shell clock). Executed from `_dispatch-2026-08-31-1-oa-session-cowork.md` in a
Cowork/Claude-in-Chrome bridge session. Third bundle in the `roster-toggles-44` series (after
2026-08-17-r3 and 2026-08-19-roster).

**TWO PHASES.** Files 01-09 are the READ-ONLY dispatch sweep (tasks A-F): no OA edit, no toggle,
no save. Files 10-13 are FOUR EDITS Andy authorized in-chat afterwards, applied under the
verified-edit protocol; `10-authorized-edits-2026-08-31.md` is their record, including two
disclosed incidents. File 01 is the pre-edit fleet state and file 13 the post-edit fleet state;
diffing them shows exactly three changed bots and nothing else.

## Files
| file | what it is |
|---|---|
| `01-bots-roster-recent-activity-2026-08-31-173107.txt` | `/bots` OA Grab capture, all groups, 17:31:07 ET. Verbatim instrument: `scripts/oa-driver/oa_grab_page.js` (bookmarklet v2.1 transcription), run in page context; the returned text was written to disk by the page's own Blob download and copied in unmodified — its sha256 was computed in the browser BEFORE transfer (`3c9c0ac5…`) and re-computed on disk after; they match, so the file is byte-exact. |
| `02-roster-toggles-44-2026-08-31.tsv` | DERIVED. 44 (bot_name, bot_id, AUTOS, EXITS) rows + join proof + drift verdict. |
| `03-open-positions-2026-08-31-173500.txt` | `/positions` Open Positions capture with the per-row `Opened:` title attributes (task E). |
| `04-pr04-discharge-trades-2026-08-31.txt` | QQQ-IC-0DTE-Fortress-NoPT50 — both 08-26 positions' Position Details drawers incl. the **Trades list** (task B). |
| `05-ride-delta-log-2026-08-31.txt` | GF-QQQ-IC-Ride-Delta automation Log, 08-31 (task C behavioural proof). |
| `06-ride-delta-scanner-diff-2026-08-31.md` | DERIVED. Root-cause diagnosis + four config hashes (task C). |
| `07-allocation-and-groups-2026-08-31.tsv` | DERIVED. allocation + bot group + toggles + open risk, all 44 (task D). |
| `08-s2-log-2026-08-31.txt` | IC-SPX-FastPT25-S2 automation Log, 08-31 (task F). |
| `09-s2-config-check-2026-08-31.md` | DERIVED. 4/4 hash match vs the 08-07 baseline + the Cleanup mechanism (task F). |
| `10-authorized-edits-2026-08-31.md` | DERIVED. The four authorized edits, before/after evidence, hashes, and two disclosed incidents. |
| `11-qqqlongcall-postclose-2026-08-31.txt` | QQQ long call positions after the three legacy closes (edit 2). |
| `12-ride-delta-postedit-2026-08-31.txt` | GF-QQQ-IC-Ride-Delta settings + toggle titles after the archive edit (edit 1). |
| `13-bots-roster-POSTEDIT-2026-08-31-181115.txt` | `/bots` OA Grab capture taken AFTER all four edits — the fleet-wide control. |

## Headline results
- **BOT COUNT 44, not 45.** Footer verbatim: `44 active bots • 6 left in your plan • Upgrade`.
  "Friday 14 DTE Broken Wing IB (B-70)" was **already in the 08-19 bundle** — the dispatch's
  "+1" premise is falsified by both captures. It is also already in the **OA-Mirror-Focus** group.
- **TOGGLE DRIFT vs 2026-08-19: ZERO**, over 8 trading days. AUTOS 19/44, EXITS 16/44 —
  membership byte-identical. Join proof: all 44 (name, bot_id) pairs identical to the 08-19 file.
- **PR-04 discharge evidence: all three checks PASS** (see task B section of the session log).
- **Ride-Delta double-fire root cause: two put scanners and two call scanners on one bot**, all
  four functionally identical; proven by hash and by the 08-31 log.
- **Allocation**: every family is already internally equal EXCEPT the mirror family.
- **11AM S2: zero config delta since 2026-08-07**; the 08-31 both-sides expiry is the Cleanup
  monitor's `exactly 1 position` guard failing, exactly as built.
- **Edits applied (phase 2):** Ride-Delta archived (2 bot-local scanners off, bot automations
  off, 5/5 config hashes unchanged) - QQQ long call's 3 legacy positions closed, all filled
  immediately in the paper account for **-$8,693** realised - 3DTE allocation $5K -> $10K -
  QQQ-IC-0DTE-Fortress added to Monitor. Fleet diff 01 vs 13: **three bots changed, nothing
  else**; AUTOS ON 19 -> 18, EXITS ON 16 -> 16.

## Provenance rules honoured
- Toggle state is the `title` ATTRIBUTE of the two `i.sticon` elements per row, never innerText.
- The (name, bot_id) pairing is cross-checked against the independent 08-19 capture, not trusted
  to row order (the 08-19 bundle records why: an off-by-one row join once produced 12 false
  toggle changes).
- Every automation hash was computed after opening that automation **fresh with a hard reload**
  between opens, from `a5.bots.acedit.routine` — never from a DOM read (stale-editor-DOM trap).
- No number in this README is stated that is not in one of the files above.
