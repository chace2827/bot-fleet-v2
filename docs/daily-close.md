# Daily close — the one-pager

*Written 2026-09-16. The close is a terminal job, not a chat job: both inputs land in
`~/Downloads` and `scripts/close.sh` picks them up from there. Nothing is dropped into a
chat. If a project memory or another doc describes a different flow, this file wins.*

## The ritual — each trading day, after the close (~17:30 ET)

1. **OA → Analyze → Export Data.** Start date on/before **08-10**, **all bot groups**
   selected, default filename. It lands in `~/Downloads`.
2. **`/bots` → click the OA Grab bookmarklet.** An `oa_*.txt` lands in `~/Downloads`.
3. **Terminal:**
   ```bash
   cd ~/bot-fleet-v2 && scripts/close.sh
   ```
   No argument needed: the close day is derived from the export's newest position
   (`max openDate`) — today for an after-close export, yesterday for a next-morning
   one. To close a specific day instead: `scripts/close.sh YYYY-MM-DD`.
4. **Write `data/brief/<day>_narrative.md`** — the six `##` slots: `since-yesterday`,
   `convexity`, `lesson`, `tomorrow`, `fire`, `strategy`. This is the judgment step;
   nothing generates it, and an unfilled slot is recorded as unfilled.
5. **`python3 scripts/render_brief.py <day>`** — re-injects the narrative into the html.
6. **Run the commit command `close.sh` printed.** Andy commits; agents do not.

## What close.sh does

ingest export (`~/Downloads` → `data/raw/<day>.csv`, sha- and range-guarded) → the
nine-stage `daily.sh` (ledger → tape → drift audit → brief → verdicts → hedge
tournament → trade window → lessons → report) → roster capture bundle (toggle table +
drift vs previous bundle) → `render_brief` → manifest + close-runs receipt → derived
commit command. ~10 minutes.

## Where the agents fit

- **Cowork:** the narrative (step 4) and the review of the brief. It reads the project
  files itself; nothing is uploaded to it.
- **Claude Code / Devin:** script and doc changes.

## The rules that bite

- **Export range:** earliest `openDate` later than the coverage floor (`LEDGER_START`
  08-10, or the previous export's front) → refused at stage 1/5, nothing written.
  Re-export wider; there is no override.
- **All groups selected.** A group-filtered export is a subset; the guard only catches
  bots that already existed.
- **Day vs. export:** a close day earlier than the export's newest `openDate` refuses —
  you cannot close a day the export hasn't reached.
- **Downloads hygiene is automatic for banked exports** (sha-matched and ignored), but
  a second *unbanked* OA-shaped csv still refuses as ambiguous — delete stray partial
  exports if you make them.
- **Captures are auto-discovered** from `~/Downloads` by their `captured:` header. One
  dated *before* the close day is ignored as stale (warning printed); one dated after
  is used — that is the catch-up case. To place one by hand instead: exactly one `.txt`
  in `data/captures/<day>/` (plus any screenshots), or `CAPTURE_TXT=/path/file.txt`.
- **Catch-up:** one export covers all missed days and the manifest records the gap
  honestly. Roster evidence for the missed days themselves is unrecoverable — a capture
  only shows the fleet as it is now.
- **The manifest is written at close time.** A narrative written afterward shows as
  unfilled in that record — honest and intended; step 5 fixes the html.

## If it refuses

Every refusal names the file and the fix, at stage 1/5 before anything is written.
`--dry-run` (`python3 scripts/ingest_export.py --dry-run`) prints every derivation
without touching `data/raw/`.

## Overrides (rarely needed)

`FLEET_ROOT=/path` runs the whole close against a scratch root without touching `data/`
(the repo's scripts seed it). `INGEST_DOWNLOADS=/path` scans a different directory for
both the export and the capture. `CAPTURE_TXT` / `CAPTURE_INBOX` / `CAPTURE_SCREENSHOTS`
override capture discovery — see the `close.sh` header.
