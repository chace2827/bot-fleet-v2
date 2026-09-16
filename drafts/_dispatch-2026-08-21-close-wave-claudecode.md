# CLOSE-WAVE — Claude Code foreman — free-lane Devin dispatch, 3 agents, SEQUENTIAL

⛔ **GATED. Do not dispatch until BOTH hold:**
1. Andy has signed all three rulings in `_rulings-draft-2026-08-21-close-automation.md`
   (R-ARGV · R-CLOSE-RECEIPT-SURFACE with an option circled · R-STAGING-MANIFEST).
2. Andy has pushed local master — `a7ffc52` is ahead of `origin/master` `3d456bd` as of
   2026-08-21; clones base on origin, so an unpushed base makes every premise check stale.

Paste into the Claude Code terminal, in `~/bot-fleet-v2`:
"Read `_dispatch-2026-08-21-close-wave-claudecode.md` in the repo root. You are the CLOSE-WAVE
foreman. Execute §1 pre-flight, then §3 in order. Report in the §5 format."

## 0. Lane split
- **Cowork (Andy's chat)** = manager: wrote this file, verifies claims read-only, rules nothing.
  (Manager template: `_dispatch-2026-08-19-manager-cowork.md`.)
- **You (Claude Code)** = foreman: terminal, clones, queue, merges, local verification.
- **Devin via `devin-free`** = worker. Free lane only. One deliverable per agent.
- **Andy** = every decision, every commit to the main tree, the relay.

## 1. Pre-flight — ALL of it before dispatching anything
1. **Wrapper integrity.** Dispatch ONLY via `~/bin/devin-free`. Assert
   `devin-free --selfhash` == `shasum -a 256 scripts/devin_free.sh` at the pinned base.
   ⛔ Never the raw binary, never `$DEVIN`, never `-p`, never a model flag, never `cd` into a
   workspace — the wrapper owns binary path, model, flags and chdir (`--workspace DIR`).
   ⛔ **Never kill a Devin session** — a killed row is `acu=UNKNOWN` forever.
2. **Pin the base.** Fresh `/tmp` clone, `git fetch origin && git rev-parse origin/master`.
   Every clone pins that sha and prints it. Never touch `~/bot-fleet-v2` or `~/gitstore`.
3. **Verify every premise in §2 against the file at that sha.** A failed premise = do not
   dispatch that agent; report it in §5. (Three dispatches died on stale premises 08-17.)
4. **CI is blind — verify locally.** `phase0` has not run on recent pushes and `check_refs.py`
   exits 0 on danglers. Acceptance is what YOU run in the clone (selftests, dry runs, DOM/output
   checks), never a green PR page.
5. After every session: assert `model=swe-1-7|swe-1-7-medium`, `backend_type=windsurf`,
   `acu=0.0`, `credit=0`. Non-zero acu = halt and report.
6. Results land as PRs on `devin/*` branches, `gh pr merge --auto --squash`. Never push master.

## 2. Premises to verify at the pinned sha (per agent, before dispatch)
- **P-D1a** `scripts/daily.sh` has `TOTAL_STAGES=9` and plumbs only `--allow-rewind` as `$2`.
- **P-D1b** `scripts/run_receipt.py` receipts carry no `argv`/`overrides` field.
- **P-D1c** The 26-column export schema is stated in `docs/capture-architecture-2026-07-30.md`
  (D1 detects exports by header content, never by filename).
- **P-D2a** `data/captures/2026-08-19-roster/01-bots-roster-recent-activity-2026-08-19-211733.txt`
  is committed and carries a `captured:` header line with an ET-offset timestamp, plus the
  AUTOS/EXITS title block.
- **P-D2b** `data/captures/2026-08-19-roster/02-roster-toggles-44-2026-08-19.tsv` is committed
  (44 data rows, header carries the cross-check requirement) — it is D2's acceptance fixture.
- **P-D2c** `data/bots_config_v2.csv` has an `oa_id` column AND leading `#` comment lines before
  the header (a naive DictReader reads a comment as the header — known trap).
- **P-D3a** `scripts/render_brief.py` exists; reads `<DAY>_brief.json` + `trades.csv`, narrative
  sidecar optional, absent sections render as visible unfilled slots.
- **P-D3b** `daily.sh` supports `FLEET_ROOT` scratch isolation (D3's acceptance runs use it —
  the live `data/` is never an acceptance surface).

## 3. The three agents — SEQUENTIAL. D1 is the pilot; D3 only after D1+D2 are merged.
Every acceptance is a **derivation, not a literal**. An agent hardcoding a number to satisfy a
predicate has failed. Every predicate must be SEEN RED once (mutate a fixture, watch it fail)
before it counts as a predicate. Agents render no judgment verdicts — mechanics only.

**D1 · `scripts/ingest_export.py` + argv-in-receipts (implements R-ARGV)**
New file `scripts/ingest_export.py`:
- Finds OA position exports in a directory (default `~/Downloads`, `--downloads DIR` for tests)
  **by header content against the 26-column schema**, never by filename.
- Derives the ET trading day TWO ways — file mtime converted to America/New_York, and max
  `open_date` across rows — prints both; on disagreement beyond mtime-date ≥ max-open-date
  same-day, REFUSES. `--day` overrides but is still cross-checked. (Kills the UTC trap.)
- Refuses when min open_date > LEDGER_START (export range too short — resolve LEDGER_START the
  same way `build_ledger.py` does; read that file, don't guess).
- Destination `data/raw/<day>.csv`: exists with equal sha → "already ingested", exit 0
  (idempotent); exists and differs → REFUSE loudly. Never overwrites.
- Detects colon-mangled path artifacts (`*data:raw*` names) in the source dir and REPORTS them;
  never deletes anything.
- `--dry-run` and `--selftest` (house style: fixtures + named check matrix, cf. run_receipt.py).
Plus the R-ARGV change exactly as the signed ruling states (daily.sh `FLEET_ARGV`,
build_ledger resolved-overrides into ledger_meta.json, run_receipt `argv`+`overrides` fields,
selftest rows for present/absent/old-shape).
Accept when: all selftests pass in the clone; a scratch `FLEET_ROOT` fixture run WITH
`--allow-rewind` yields a receipt whose `overrides.allow_rewind` is true and one without yields
all-false — both read back from the receipt file itself, not from stdout.

**D2 · `scripts/capture_bundle.py`**
Builds `data/captures/<day>-roster/` from raw capture files (bookmarklet txt + screenshot):
- ET day from the txt's own `captured:` header — never filename, never clock.
- Numbered renames per the `2026-08-19-roster` convention; screenshots under `screenshots/`.
- Toggle TSV derived from the AUTOS/EXITS title block, `oa_id → name` join from
  `bots_config_v2.csv` (skip leading `#` comment lines — P-D2c). Row count derived from the
  block, never asserted.
- ⛔ **The cross-check is built in as a FATAL:** every `(name, bot_id)` pair must match the
  previous bundle's TSV pairing exactly; any pairing mismatch aborts the bundle. (The 08-19
  off-by-one produced 12 false toggle changes; this check is what caught it, so it is now code.)
- Drift verdict vs previous bundle written into the generated README.md; no previous bundle →
  `NOT EVALUABLE`, stated — never "no drift".
- `SHA256SUMS.txt` excluding itself and `.DS_Store`; `--selftest`.
Accept when: (a) run against the committed raw txt of `2026-08-19-roster` with the 08-17 map as
previous, the derived TSV matches the committed `02-roster-toggles-44-2026-08-19.tsv` row-for-row
on (name, bot_id, autos, exits); (b) a fixture with one shifted row makes the FATAL fire — the
predicate is seen red.

**D3 · `scripts/close.sh` + `scripts/close_manifest.py` (implements R-CLOSE-RECEIPT-SURFACE
Option 1 + R-STAGING-MANIFEST; dispatch ONLY after D1 and D2 are merged and the rulings signed;
if Andy circled Option 2, STOP and report — this card is written for Option 1)**
- `close.sh [day]`: ingest_export → `daily.sh <day>` (UNTOUCHED, still 9 stages) →
  capture_bundle when raw capture files are present (absent → manifest records
  `capture: ABSENT` loudly, never a pass) → `render_brief.py <day>` →
  `close_manifest.py` writes `data/close/<day>/manifest.json` — export sha, daily-receipt
  summary, capture bundle shas + drift verdict, brief path + narrative-slot status, close argv —
  and appends `data/receipts/close-runs.jsonl` (append-only, mode 'a' only, selftest-pinned like
  run_receipt S8).
- Prints the commit command per R-STAGING-MANIFEST: file-by-file `git add` list derived from the
  manifest; independent re-derivation of the list must match; `_*` / `.claude/**` /
  `_locktrash/**` / `one` = FATAL refusal; commit message figures derived from the manifest.
- **Gap statement (added 2026-08-21, Andy's request):** close.sh derives the previous recorded
  close from the last receipt in `data/receipts/daily-runs.jsonl` (its `day` field, never file
  mtimes) and states the gap on stdout AND in the manifest — e.g. `last close 2026-08-19,
  1 trading day unobserved (2026-08-20)`. Unobserved days are US-market trading days between the
  two dates (weekends/holidays excluded; derive the calendar the same way existing stages do —
  read how tape.py/should_have_fired.py treat non-trading days, don't invent a second calendar).
  Zero gap states `previous close <day>, no gap`. An empty receipts file states
  `no prior close on record` — NOT EVALUABLE, never "no gap". A skipped night must be visible in
  the record, not silent.
- Never runs git itself. Printing is the boundary.
Accept when: a full `FLEET_ROOT` scratch run on a fixture day yields (a) a manifest whose every
sha equals `shasum -a 256` of the file on disk, checked by a loop the foreman runs, not by the
script's own claim; (b) printed-command path list == manifest path list, derived both ways;
(c) a planted `_scratch.md` in the output set makes the generator refuse — seen red;
(d) `close-runs.jsonl` append-only selftest passes;
(e) gap statement: a fixture receipts file whose last `day` is two trading days back yields the
correct unobserved-day list, a consecutive-day fixture yields `no gap`, and an empty receipts
file yields the NOT EVALUABLE form — all three derived from the fixture, none hardcoded.

## 4. Held out — deliberately, do not add
- **OA-surface anything** (export automation, roster capture via oa-driver) — `lane=OA`, never
  Devin. Phase 2/3 of the agreed plan, Cowork lane, separate authorization.
- **Wiring render_brief or close.sh into `daily.sh`** — contract change beyond the signed rulings.
- **Ritual/doc updates** (`docs/daily-loop-spec.md`, ritual memory) — Cowork does these after
  the wave lands, as their own reviewed edit.
- **I-06, F-6, F-7** — separate items, separate rulings.

## 5. Report back — exactly this shape, for Andy to paste into Cowork
```
CLOSE-WAVE REPORT
base sha:            <sha>   wrapper selfhash: <PASS/FAIL>
rulings gate:        <R-ARGV / R-SURFACE(option) / R-MANIFEST: signed y/n>
premise checks:      <P-D1a..P-D3b: PASS / FAIL + one line>
per agent:           <D1/D2/D3> <PR # or branch> <each accept clause: PASS/FAIL> <seen-red: y/n>
cost assertion:      model=<> backend_type=<> acu=<> credit=<>  [PASS/FAIL]
merged to master:    <PR #s>  origin/master now: <sha>
escalations for Andy: <numbered, with both readings — or NONE>
```

## 6. Escalation
- **You decide:** retries, clone mechanics, re-prompting, merge order within the wave.
- **Andy decides:** anything touching a guard predicate, the receipt contract beyond the signed
  rulings, any spend outside the free lane, any acceptance the evidence does not settle.
- **Halt immediately:** a push to master, git against `~/bot-fleet-v2` or `~/gitstore`,
  non-zero acu, an agent widening a guard or relaxing a check to unblock itself.
