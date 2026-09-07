# T-50 — OA ARCHIVE SWEEP (ARCHIVE ONLY, NO DELETES) — Opus Cowork chat, bot-fleet-v2 + Claude in Chrome

Ruling: `R-2026-09-07-ARCHIVE-SWEEP-SESSION`. Closes board items M-17…M-26 (M-06 / M-16 deletes are
NOT authorized — Class C, stay open). Unattended. Andy commits. Fable verifies from the capture files.

## ⛔ Why this is TWO evenings, not one — the M-08 probe comes first
"Archive" in this project has meant the OA *group* named `Archive` (20 bots sit there today, all
AUTOS OFF). OA also has a real **Archive Bot** action that removes a bot from the active roster
(footer today: "44 active bots • 6 left in your plan"). **Nobody has checked whether an OA-archived
bot's closed positions still appear in the Export Data CSV** (board M-08). If they vanish, the
ledger's FILTERED-EXPORT GUARD sees a bot disappear on the next close and the export convention
("since 08-01") has rows for several of these bots between 08-01 and 08-08. So:
- **Evening 1 = probe ONE bot.** Archive exactly one, chosen so it has export rows in the 08-01..08-08
  window. Next day's close (the routine prompt) tells us whether its rows survived.
- **Evening 2 = the rest**, only if the probe says rows survive — or, if they don't, with the
  ingest guard (T-45) merged and a ruling on how to handle vanished pre-cutover rows.

## 0 · Setup
Invoke `oa-driving`. Read `CLAUDE.md` §5/§9.1, the ruling, `docs/migration-parking-lot-2026-08-19.md`
list A, and `data/captures/2026-09-02-gf-sizing/10-*`-style verify protocol (hard reload, two
surfaces, pre/post roster diff). Chrome: own tab, OA logged in, ACCOUNT Paper Trading, never
`TR ****4219`. Capture dir `data/captures/<ET-date>-archive-sweep/` + `SHA256SUMS.txt`.
`git status` clean, else STOP.

## Evening 1 — the probe
1. PRE: full `/bots` capture (`oa_grab_page.js`) + `a5.bots.allbots` TSV. Record footer count.
2. Pick the probe bot: from the 20 `Archive`-group bots, one that is AUTOS OFF, EXITS OFF, has NO
   open positions, and DOES have closed positions with closeDate in 2026-08-01..2026-08-08 in the
   latest `data/raw/*.csv` (compute this from the file; record the row count). Prefer
   `QQQ-IC-0DTE-Baseline` or a Range075 bot; never a `-ARCHIVED-` clone (they are the S2b
   originals — keep them intact until T-53's gate map is done), never a mirror, never DIR.
3. Record the bot's full state (settings page: allocation, limits, groups, tags, automations +
   hashes, positions list) → `02-probe-pre-<bot>.md`.
4. Archive it via the bot's own menu → Archive Bot. READ THE DIALOG VERBATIM before confirming; if
   it mentions deleting data, positions, or history, CANCEL and STOP — report the text.
5. Hard reload. POST: does it still appear in `/bots`? in `a5.bots.allbots`? footer count 44→43?
   Is there an "archived bots" view and does it list it? Can it be un-archived (read the
   affordance, do NOT click it)? Record all → `03-probe-post.md`.
6. Export Data (full history, no filter) to `_inbox/oa-export-<date>-postprobe.csv` (Andy drops
   it in chat if Downloads is unreachable): does the probe bot's row set match step 2 exactly?
   That is M-08's answer. Record the verdict in `04-m08-verdict.md`.
7. `data/archive/rename_map.csv`: append the probe row (old name, OA id, archived date, group,
   pre-archive seed, export-rows-survive y/n). Create the file with a header if absent.
8. Records: `docs/session-log.md`, `docs/state.md` dated section, portfolio M-08 → Done with the
   verdict, T-50 note "probe done, evening 2 pending". STOP. Report with the paste-ready commit.

## Evening 2 — the sweep (run ONLY if M-08 verdict = rows survive, or Andy rules otherwise)
Same protocol per bot, in this order, batch of 19 (the 20 minus the probe):
- 3 `-ARCHIVED-` clones: SKIP (see above) — they stay in the group, not OA-archived.
- Everything else in the `Archive` group: archive one at a time; per bot record pre-state one line
  (name, id, seed, autos, exits, open positions = must be 0, group, tags), archive, hard reload,
  confirm gone from active roster, append rename_map row.
- After the last: full `/bots` capture + allbots TSV; diff vs PRE. Expected: exactly the archived
  bots gone; every remaining bot's row byte-identical; AUTOS 18 / EXITS 16 unchanged; the 7 live
  mirrors + 2 DIR + 8 GF + 3 SPX IC + NoPT50 untouched (name them in the report — that closes
  M-25 / M-26).
- Any bot with an OPEN position: skip and report; never close a position in this session.
- `data/bots_meta.csv`: do NOT delete rows (roster authority, §2.5). Add a dated note per archived
  bot in `notes`: "<date>: OA-archived (T-50); status stays OFF". `roster.py --check` must pass.
- Records + report + paste-ready commit. Never run git.
