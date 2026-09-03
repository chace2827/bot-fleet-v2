# OA SIZING EXECUTION — 2026-09-03 — Opus Cowork chat, bot-fleet-v2 + Claude in Chrome

You are executing SIGNED sizing rulings on Option Alpha (app.optionalpha.com), unattended.
Andy is NOT watching. Do the whole run in one session. Never ask a question you can answer by
reading OA or the repo; never wait for a reply. When a STOP condition fires, leave OA in a
consistent state (finish or fully revert the batch you are in), write the report, and end.

## 0. Setup — do this first, in this order
1. Invoke the `oa-driving` skill. Every trap in it applies. Read `CLAUDE.md` §4 (unit law),
   §5 (two-layer proof), §9.1 (close-out).
2. Read the two SIGNED rulings in full: `_rulings-draft-2026-09-01-sizing.md` (R-1…R-6 + the
   R-2026-09-02-POSITION-LIMITS addendum) and `_rulings-draft-2026-09-01-gf-sizing.md` (G-1…G-6).
   Confirm every `SIGNED — Andy — 2026-09-02` line is present. If any ruling reads `......`
   (unsigned), STOP before touching OA.
3. Read the precedent capture `data/captures/2026-08-31-roster/10-authorized-edits-2026-08-31.md`
   and `06-ride-delta-scanner-diff-2026-08-31.md` — they are the exact protocol and the
   bot-local-scanner precedent you will reuse.
4. Browser: Claude in Chrome. Call tabs_context first; open a NEW tab for OA. If OA is not logged
   in, STOP and report (do not enter credentials).
5. Create `data/captures/<ET-date>-gf-sizing/` (ET date read from OA's own page header, never
   the container clock) and write every capture there; finish with `SHA256SUMS.txt`.

## 1. Hard rules (violations have caused silent failures on this account)
- ACCOUNT = **Paper Trading** on every bot's own page before any edit. The login also carries a
  live brokerage account (`TR ****4219`). Never select it. If a click opens the ACCOUNT dropdown,
  Escape, re-read, and disclose it in the report.
- Evidence = state re-read from the server-hydrated model (`a5.bots.bot`, `a5.bots.acedit.routine`)
  **after a HARD RELOAD**, plus a second surface (panel text / `i.sticon` title). A save toast, a
  tool "success", or a version increment is NEVER evidence. Config hash =
  `sha256(JSON.stringify({name,inputs,root}))`.
- Drawer ✕ discards. Panel-level Save commits the panel; top-level Save commits the tree; some
  edits need both (see 08-07 F-C1 trap). Never type a path into a save dialog.
- If a JS call returns `Inspected target navigated or closed`: DO NOT RE-FIRE. Hard reload,
  re-read; the write may already have landed.
- Do not touch: strikes, filters, exit policy, schedules, any bot's AUTOMATIONS/EXITS toggle,
  `GF-QQQ-IC-Ride-Delta` (OFF, stays OFF), `DIR-SPX-*` (explicitly deferred by Andy),
  `IC-SPX-FastPT25-S2` / `-130PM` (Exit-Option-free ride+S2 controls — not "fixed"), any mirror
  other than the one 3DTE allocation revert, any OFF/archived bot's sizing.
- One shared-scanner edit propagates to every attached bot. That is why Batch A exists.

## 2. OUTER CHECK — before anything
Full `/bots` roster capture (same instrument/parse as `01-bots-roster-recent-activity-…txt`):
name · group · allocation · AUTOS · EXITS · open risk · positions · footer count. Save as
`01-roster-PRE-<ts>.txt`. Expected baseline: 44 bots, AUTOS ON 18/44, EXITS ON 16/44
(08-31 post-edit). If AUTOS/EXITS tallies differ from 18/16, record the delta and CONTINUE
(someone may have traded/toggled since) — but any GF arm not ON, or Ride-Delta ON, is a STOP.

## 3. Batch A — STEP 0, read-only: shared-scanner attachment enumeration (GATE)
Open `GF-ScannerA-PutSpread` and `GF-ScannerB-CallSpread` from the OA Library. For each:
- Enumerate EVERY bot it is attached to (the sharing/"used by" list — a count is not a list).
- Compute the hash after a fresh open + hard reload. Must equal:
  `ScannerA 1e5eb9936a1adf067af65a4841d42e755592f7c179f3c0cad477502dfdbfcdc8`
  `ScannerB a925d490b8a0d2337566f47307fc52470da129935d3bd83d24389c6dc433dfb5`
- Read `amount` on the open-position action. Expected `{"type":"quantity","quantity":1}`.
Expected attachment list: exactly the 8 `GF-QQQ-IC-*` bots (Ride, PT50, Trail, Touch0, SL100,
SL200, Canary, Ride-Delta). Save as `02-scanner-attachments-<ts>.md`.
STOP conditions: any non-GF bot attached · either hash mismatch · quantity ≠ 1.

## 4. Batch B — Canary detach (G-3d route (a)) — MUST precede Batch C
Goal: `GF-QQQ-IC-Canary` keeps 1 ct after the shared pair goes to 26. Precedent: Ride-Delta's
bot-local `Ride-Delta-Scan-Put/Call` (06-ride-delta-scanner-diff). Procedure:
1. On Canary's page: ACCOUNT Paper Trading; record all automations + hashes + toggles (pre).
2. Create bot-local copies of both scanners INSIDE the Canary bot (copy/duplicate into the bot —
   NOT a shared reference). Name them `Canary-Scan-Put` and `Canary-Scan-Call`. Do not edit the
   library originals. Verify each copy's tree + open-position action is field-identical to the
   shared original (gate chain, `exactly 0 days`, `$2.00` wing, `±.10 delta`, quantity **1**,
   inputs). Hash each and record; the hash will differ from the shared one because `name`
   differs — that is expected; the field diff is the proof.
3. Enable both bot-local copies (automation-level ON). Then REMOVE the two SHARED scanners from
   Canary — detach from this bot only. ⛔ Do NOT delete the library automation. Before confirming
   any removal dialog, read its text: if it says anything about deleting from the library or
   affecting other bots, cancel and find the per-bot detach.
4. Hard reload. Verify Canary now lists exactly: `Canary-Scan-Put`, `Canary-Scan-Call`,
   `GF-Backstop-1552-FlatClose` (shared trigger stays) — all ON; bot AUTOMATIONS ON, EXITS ON,
   allocation $2.5K, limits unchanged. Verify from the Library that ScannerA/B attachment lists
   now show 7 bots (the 8 minus Canary) and both shared hashes are still byte-identical to §3.
5. Save `03-canary-detach-<ts>.md`. STOP if the shared hashes changed or the library lost an object.
   If step 2 proves impossible in the UI (no copy-into-bot affordance), STOP the whole run before
   Batch C and report — Canary must not be swept to 26 by accident.

## 5. Batch C — the shared lever: quantity 1 → 26 (G-3b), ONE edit per scanner
For ScannerA then ScannerB, from the Library: fresh open, hard reload, confirm pre-hash (§3),
edit the open-position action `amount` → `{"type":"quantity","quantity":26}`, save with the
panel Save AND the top-level Save, hard reload, re-open, re-read `amount` from
`a5.bots.acedit.routine` (quantity === 26), recompute hash, record pre/post pair. Confirm
nothing else in the tree changed (diff the JSON minus `amount`). Then open ONE arm (Ride) and
confirm its view of the scanner shows 26 contracts. Save `04-shared-qty-<ts>.md`.

## 6. Batch D — allocations, 6 arms (NOT Canary, NOT Ride-Delta)
Bots: `GF-QQQ-IC-Ride`, `-PT50`, `-Trail`, `-Touch0`, `-SL100`, `-SL200`.
Per bot: ACCOUNT Paper Trading → Safeguards drawer → `input[name="seed"]` 2500 → 10000 → Save →
HARD RELOAD → verify `a5.bots.bot.seed === 10000` AND the Safeguards panel reads $10,000.
Read and record DAILY POSITIONS / POSITION LIMIT / DAY TRADING / BOT GROUP / AUTOS / EXITS.
Position limits (R-2026-09-02-POSITION-LIMITS): target 1 per day / 1 at a time on these six and
on Canary. If a bot already reads 1/1 → record, no edit. If not → set 1/1, record the prior
value, and flag it for the Layer-2 both-sides check. Save `05-allocations-<ts>.md`.

## 7. Batch E — 3DTE revert (R-4)
`3DTE $140-$350` (`BOTfw5TkkCRF2217765235512870291`): seed 10000 → 5000, same verify protocol.
Everything else on the bot unchanged and re-read. Its open position is not touched.

## 8. Batch F — group hygiene + tags (R-5, all three ticked)
A. Move to group `Archive`: `IC-SPX-FastPT25-S2-ARCHIVED-2026-08-07` (from IC-Focus),
   `IC-SPX-FastPT25-S2-130PM-ARCHIVED-2026-08-08` and `QQQ-IC-0DTE-Fortress-NoPT50-ARCHIVED-2026-08-08`
   (from Monitor). Verify `a5.bots.bot.group.name === "Archive"` after hard reload; toggles untouched.
B. Rename group `IC` → `GF-Family`. Verify all 8 GF arms now show group `GF-Family` and the
   group count is unchanged (8).
C. Tags: for every bot with a `PR-NN` entry in `docs/pre-registration-ledger.md` (parse the
   `### PR-nn —` headings + `BOT` fields — key on both), read its OA tags. Apply the bare `PR-NN`
   tag where missing. Record a table bot · PR id · tag before · tag after. Do not add any other tag.
Read-only confirm on `IC-SPX-FastPT25-S2` and `-130PM`: limits still 2 per day / 2 at a time.
Save `06-groups-tags-<ts>.md`.

## 9. OUTER CHECK — after everything
Full `/bots` capture `07-roster-POST-<ts>.txt`, same parse as §2. Diff PRE vs POST. Expected to
differ and NOTHING else: 6 GF allocations $2.5K→$10K; 3DTE $10K→$5K; 3 archived clones' group;
group label IC→GF-Family on 8 arms; tags. AUTOS/EXITS tallies identical to PRE. Footer identical.
Any unexpected diff → investigate, and if it is yours, revert it and disclose.

## 10. Phase 3 — record to repo (do it, don't defer; Andy commits)
- `data/bots_meta.csv` `notes` column, the 6 sized arms:
  `<ET-date>: 1ct -> 26ct, ≈$5K risk/position per R-2026-09-01-GF-SIZING; raw P/L not poolable across this boundary; R, sample counts and gate progress unaffected.`
  Canary: `<ET-date>: detached from shared GF-ScannerA/B onto bot-local Canary-Scan-Put/Call, 1 ct, per R-2b route (a); CONFIG HASH re-issued.`
  Write with `lineterminator='\n'` (CRLF trap). Do NOT add columns. Run `python3 scripts/roster.py --check` and `scripts/portfolio.py --check` after.
- `docs/pre-registration-ledger.md`: append `AMENDED 2026-09-03 per R-2026-09-01-GF-SIZING` lines
  under PR-14…PR-19 (MAX LOSS / SIZING TIER, amended text from G-1), PR-20 (Canary detach + new
  hashes), PR-01/PR-02 + QQQ entries (sleeve caps re-ruled per R-3: SPX $15K, QQQ $40K), PR-07
  (3DTE reverted). Never rewrite original text. Run `scripts/pre_registration_ledger.py --selftest`.
- `docs/RULINGS.md`: append the seven rulings (R-1…R-6, POSITION-LIMITS) with signatures, Andy's
  verbatim answers, and the deferred DIR item.
- `data/portfolio.csv`: add a DEVIN-lane item "G4 $ caps into report.py: per-bot $15K / fleet
  $35K / day-halt $8K (R-6)"; mark the sizing items done with this capture as evidence.
- `SHA256SUMS.txt` in the capture dir; `README.md` there listing every file and its purpose.
- `git mv` the four signed/tracked `_rulings-draft-2026-09-01-*.md`, `_sizing-policy-draft-…`,
  `_roe-cap-proposal-…` from repo root to `drafts/` (the 08-21 close-automation ruling's pattern:
  RULINGS.md is the record, the draft file is history in `drafts/`). Note: `.git` is a gitfile
  pointing at `~/gitstore/bot-fleet-v2.git`; git commands may only work from Andy's Terminal, in
  which case leave the moves to him. Never commit or push: end with the exact
  `git add … && git commit -m …` one-liner he can paste.

## 11. Layer 2 — schedule the day-after check
Append to the top of `STATUS.md` (or the brief template if that is what daily.sh reads — check):
`⚠️ UNVERIFIED-L2: first new position on each of Ride/PT50/Trail/Touch0/SL100/SL200 must show
quantity 26 in the TRADES LIST; Canary must show 1 and fill its 5% PT; both sides must still open
on any arm whose limits were changed. Exit Options panel is never evidence.` Repeat until closed.

## 12. Report (final message, also saved as `08-REPORT-<ts>.md`)
Per batch: done / STOPPED-at / reverted. Scanner attachment list from STEP 0. Hash pairs
before/after for ScannerA, ScannerB, Canary-Scan-Put/Call. Seed pairs ×7. Limits table (before →
after) ×9. Group/tag table. PRE/POST diff result verbatim. Incidents disclosed. Files awaiting
Andy's commit, with the paste-ready git command. Then CLAUDE.md §9.1 close-out.
