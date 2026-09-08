# 2026-09-07 · T-50 archive sweep — Evening 1 (PROBE), PAUSED MID-STEP-6

**Ruling:** `R-2026-09-07-ARCHIVE-SWEEP-SESSION` · board T-50 / M-08.
**State: PAUSED by Andy ~14:56 ET.** One bot archived. M-08 NOT answered. Evening 2 NOT started.
M-36 NOT started. No records outside this directory were touched — `docs/session-log.md`,
`docs/state.md`, `data/portfolio.csv`, `data/bots_meta.csv` and `data/archive/rename_map.csv`
are all UNCHANGED, so nothing claims a verdict that was not reached.

## Files
| File | What it is |
|---|---|
| `01-allbots-PRE-2026-09-07-184246.tsv` | 44-bot roster PRE, from `a5.bots.allbots`; footer + account header + Paper-Trading assertion in the banner |
| `01b-toggles-PRE-2026-09-07-184246.tsv` | AUTOS/EXITS PRE from `i.sticon` titles; AUTOS 18 / EXITS 16; drift vs the 12:47 capture = ZERO |
| `02a-probe-selection-2026-09-07.md` | **Finding P1** — the dispatch's step-2 window is unsatisfiable and its hazard is absent; the derived ruling; why the probe is `QQQ-IC-0DTE-Baseline` |
| `02b-probe-rowset-QQQ-IC-0DTE-Baseline.tsv` | the exact 43-row fingerprint the post-probe export must reproduce |
| `02-probe-pre-QQQ-IC-0DTE-Baseline.md` | probe full pre-state incl. automation config hash `aed7afe2…` |
| `03-probe-post.md` | the archive dialog verbatim, the five step-5 answers, three unasked consequences, the unrecorded bot in the Bot Archive, and where step 6 stopped |

## Deviations from the dispatch — all deliberate, all flagged for veto
1. **`git status` clean check NOT RUN.** `CLAUDE.md` §9.1 (`R-2026-08-17-GIT-RULE-SCOPE`) forbids
   git in **any** form, read-only included, from a bridge session on the mounted tree; the folder
   wins over the dispatch line. (The tree is a worktree whose gitdir resolves to a host path the
   VM cannot see, so git could not have run here regardless.)
2. **Step-2's 08-01..08-08 window dropped** — unsatisfiable and moot. See `02a`, Finding P1.
3. **The PRE `/bots` capture is the structured TSV pair above, not the raw `oa_grab_page.js`
   innerText blob.** The blob was produced in-page (44 sticon rows, 10,290 chars) and its
   in-page `crypto.subtle` sha256 `2b9497a1ef0866d8bcf371e359e61cf3c7735c7fbe65f8a63b23af2c10fc08ec`
   is recorded as the provenance anchor, but the harness chunks JS return values and filters
   base64 transport, so no byte-exact reconstruction could be **verified** — and an unverified
   reconstruction is not evidence (§9.1a). The structured TSV is a better diff surface for
   Evening 2 anyway: it compares fields, not rendered text.

## Findings raised
- **P1** — step-2 criterion falsified; FILTERED-EXPORT GUARD cannot fire on these 20 bots (`02a`).
- **P2** — `showBotMenu` / `archiveBot` are **drivable**, contradicting runbook §5 / skill finding
  S0b-2 ("the human's hand"). Method and guard in `03-probe-post.md`.
- **P3** — the Bot Archive lives at **`/settings/archive`**; runbook records "no documented URL;
  `/bots/archive` 404s". Restore is a per-row button.
- **P4** — an OA-archived bot's `/bots/bot/<id>` URL **404s**. Per-bot pre-state must be captured
  before archiving, not after.
- **P5** — archiving **frees a plan slot** (6 left → 7 left) and **removes the bot from the
  account roll-up** (TOTAL P/L -$83,731 → -$52,151; ALLOCATION $2,190,000 → $2,090,000).
- **P6** — **`QQQ-IC-0DTE-Fortress-ARCHIVED-2026-08-03` is already in the Bot Archive** and the
  folder never recorded it. Not in the 44-row roster, not in `bots_meta.csv`.
- **P7** — the account export route is **`/positions/analyze` → `Export Data`** (not `/bots`).
