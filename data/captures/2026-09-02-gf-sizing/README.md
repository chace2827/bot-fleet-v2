# Capture bundle — 2026-09-02 sizing execution (OA session)

Trading day **2026-09-02** (ET date taken from OA's own page header,
`captured: Wed Sep 02 2026 20:59:36 GMT-0400`, never the container clock — which read
2026-09-03 UTC). Executed from `drafts/_dispatch-2026-09-03-sizing-execution-cowork.md` in a
Cowork / Claude-in-Chrome bridge session, 20:59–22:45 ET. Fourth bundle in the roster series
(after 2026-08-17-r3, 2026-08-19-roster, 2026-08-31-roster).

**One phase, all edits.** Unlike the 08-31 bundle this is not a read-only sweep with edits bolted
on: everything here executes rulings Andy signed on 2026-09-02. File `01` is the pre-edit fleet
state and `07` the post-edit fleet state; diffing them shows exactly the intended changes.

## Files
| file | what it is |
|---|---|
| `01-roster-PRE-2026-09-02-205936.txt` | `/bots` OA Grab capture, all groups, 20:59:36 ET. Instrument verbatim: `scripts/oa-driver/oa_grab_page.js` (bookmarklet v2.1 transcription) run in page context. sha256 computed **in the browser before transfer** and re-computed on disk — they match, so the file is byte-exact. |
| `02-roster-toggles-44-2026-09-02.tsv` | DERIVED. 44 (bot_name, bot_id, AUTOS, EXITS) rows, joined to the independent 08-31 capture by bot_id (44/44 matched, zero unmatched). Toggle drift vs 08-31: **1**, and it is 08-31's own Ride-Delta edit. |
| `02-scanner-attachments-2026-09-02-210500.md` | DERIVED. Batch A / STEP 0 gate: the attachment **list** (not the count) for both shared scanners, their pre-hashes, and the `amount` field. |
| `02a-scannerA-PRE-routine.json` · `02b-scannerB-PRE-routine.json` | The exact `{name,inputs,root}` payloads whose sha256 **is** the config hash. Each file's own sha256 equals the hash quoted for it. |
| `03-canary-detach-2026-09-02-212700.md` | DERIVED. Batch B: the bot-local copies, the field-diff proof, the verbatim removal dialog, and the library blast-radius check. |
| `03a-canary-scan-put-routine.json` · `03b-canary-scan-call-routine.json` | The two bot-local copies' payloads. |
| `03c-scannerA-postdetach-routine.json` · `03d-scannerB-postdetach-routine.json` | The shared pair re-read AFTER the detach — `cmp` byte-identical to `02a`/`02b`. |
| `04-shared-qty-2026-09-02-214200.md` | DERIVED. Batch C: quantity 1 → 26, hash pairs, and the leaf-by-leaf diff showing four changed leaves and nothing else. |
| `04a-scannerA-POST26-routine.json` · `04b-scannerB-POST26-routine.json` | Post-edit payloads. |
| `05-allocations-2026-09-02-215500.md` | DERIVED. Batches D and E: seven seed pairs, the read-only limits table, and the reasoning for **withholding** the 1/1 limit edit. |
| `06-groups-tags-2026-09-02-222800.md` | DERIVED. Batch F: group moves, the rename, the tag table, one corrected wrong tag, and PR-23 not applied. |
| `06a-allbots-state-2026-09-02-220600.tsv` | Fleet state mid-Batch-F, one pass from `a5.bots.allbots`. |
| `06b-allbots-FINAL-2026-09-02-222800.tsv` | Fleet state after everything: name, id, group, seed, status, disableExits, posLimit, account, tags — all 44. |
| `07-roster-POST-2026-09-02-222827.txt` | `/bots` OA Grab capture taken after all edits — the fleet-wide control. |
| `08-REPORT-2026-09-02-224500.md` | DERIVED. The session report: per-batch result, every hash and seed pair, the PRE/POST diff verbatim, seven disclosed incidents, and the two open items for Andy. |

## Headline results
- **GATE PASSED before any edit.** Both shared scanners attached to exactly the 8 `GF-QQQ-IC-*`
  arms, both pre-hashes byte-matching the ruling's stamps, both at quantity 1.
- **Six live GF arms are at 26 contracts** — one edit per shared scanner, `≈$5,018` risk per
  position (larger side). New CONFIG HASHes `2c4a96c5…` / `a1a48af1…`.
- **Canary is detached and stays at 1 ct**, on bot-local copies proven field-identical to the
  shared originals. The library was not modified: the shared hashes are byte-identical across the
  detach, and no library object was deleted.
- **Allocations**: six arms $2.5K → $10K; `3DTE $140-$350` reverted $10K → $5K.
- **Groups/tags**: three archived clones → `Archive`; `IC` → `GF-Family` (8 members); `pr 01`…
  `pr 20` now each appear exactly once, on the right bot.
- **Fleet control**: 44 bots, AUTOS ON 18/44, EXITS ON 16/44, footer identical in both captures.
  Total ALLOCATION $2,150,000 → $2,190,000 = exactly the intended +$40,000.
- ⛔ **NOT executed, escalated:** the GF `1 per day / 1 at a time` limits. A GF condor is two OA
  positions; 1/day would open one side. All seven arms read 2/2 and were left there.
- ⛔ **NOT applied:** the `PR-23` tag on `GF-QQQ-IC-Ride-Delta` (widget refused; entry is
  DRAFT/unsigned; bot is AUTOS OFF).

## Provenance rules honoured
- Toggle state is the `title` ATTRIBUTE of the two `i.sticon` elements per row, never innerText.
- Every automation hash computed after opening that automation **fresh with a hard reload**
  between opens, from `a5.bots.acedit.routine` — never a DOM read (stale-editor-DOM trap).
- Every edit re-verified on **two surfaces after a full navigation reload** — the server-hydrated
  model and a second surface (rendered panel, `i.sticon` title, or the library's own attachment
  list). No save toast and no tool-success message was treated as evidence.
- ACCOUNT confirmed `Paper Trading` on every bot's own page before acting; the live brokerage
  account was never selected. One accidental opening of that dropdown is disclosed in `06` and `08`.
- Captures transferred by the page's own Blob download and copied in unmodified; the in-browser
  sha256 was compared against the on-disk sha256 for the roster captures.
- No number in this README is stated that is not in one of the files above.
