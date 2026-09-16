# T-53 — Map audit gates A–K onto board gates G1–G6 — Claude Code, in ~/bot-fleet-v2

Paste into a new Claude Code session started in `~/bot-fleet-v2`:
"Read `drafts/_dispatch-2026-09-08-t53-gate-map-claudecode.md` and execute it. Proposal only —
you draft, Andy rules. Never run git commit/push; never touch OA, a browser, or Devin; never edit
`docs/evidence-standards.md` or `scripts/report.py` in this session."

Ruling: `R-2026-09-07-DA-8-GATE-MAP-OUT-OF-SCOPE` (docs/RULINGS.md, grep the id). Board item T-53
(P7, lane CC). **Clock: T-36** — the 130PM G2/G3 review at n=20 clean condors, a few trading days
out. The map must exist BEFORE the first board-gate G3 pass on any bot, because today a bot can be
LIVE-READY on the board while its pillar fails audit gate B and nothing notices
(`docs/evidence-standards.md` §10 item 3).

## 0 · Read first (≈15 min). Locate by grep, never by remembered line number.
- `docs/evidence-standards.md` §3 (the two systems, the letter-collision warning), §4 (System I,
  gates A–K — note there is no `### A` heading; find every `**[A-K][0-9]**` criterion), §5
  (System II, G1–G6 + the ladder INCUBATE→VALIDATE→CANDIDATE→LIVE-READY), §10 items 3–5.
- `docs/RULINGS.md`: `R-2026-09-07-DA-8-GATE-MAP-OUT-OF-SCOPE`, `R-2026-09-07-DA-2-BRACKETS-RATIFIED`
  (brackets, lazy mapping to C0–C3), `R-2026-09-07-DA-7-N0-ADMISSIBILITY-CLARIFICATION` (D0–D3;
  B1/B2 never gated build or sizing), `R-2026-09-07-EVIDENCE-STANDARDS-OPTION-2` (tier ×
  corroboration table — T-49, may or may not be written yet; check the doc, don't assume).
- `docs/evidence-standards-redesign-proposal-2026-08-08.md` §6 register row DA-8 and any §
  that discusses the two gate systems.
- `scripts/report.py`: `grep -n 'stage = \[\|def .*readiness\|# G[1-6] ' scripts/report.py` — how
  `passed` (0–6) becomes a stage, how controls/mirror-watch are flagged non-graduating.
- `CLAUDE.md` §4 (evidence law, unit labelling) and §5 (go-live gates are DECISIONS — gated).

## 1 · Deliverable — ONE file, `drafts/_t53-gate-map-proposal-2026-09-08.md`
Structure, in this order:
1. **The map as a table**: rows = board stages INCUBATE · VALIDATE · CANDIDATE · LIVE-READY ·
   LIVE (real capital); columns = audit gate families A–K. Each cell one of: `HOLD` (must pass
   for the stage to be honest) · `PENDING-OK` (may be pending, never FAIL) · `N/A` · `—`. A
   one-line rationale per non-`—` cell, citing the evidence-standards § that defines the gate.
   Grain mismatch is the hard part: A–K are per system/pillar, G1–G6 per bot per condor. State
   explicitly how a bot inherits its pillar's audit verdict (the IC pillar for every `IC-*` /
   `GF-*` bot, etc.) and where that inheritance is read from.
2. **The n=0 problem, as OPTIONS for Andy, not a recommendation smuggled in**: B1 (≥100
   positions) and B2 (≥6 months) are unreachable for months after the 07-30 cutover (§10 item 5;
   DA-7). Present at least: (a) B is `HOLD` at LIVE only, LIVE-READY carries a visible
   "audit B pending" flag; (b) B is `HOLD` at LIVE-READY — state the consequence in dates, read
   from `data/trades.csv` this session (earliest post-cutover `open_date` + 6 months) and label
   the unit; (c) B split: B3 (regime) `PENDING-OK`, B1/B2 `HOLD` at LIVE. Consequences of each
   for T-36 spelled out.
3. **The "notice" mechanism** — the defect §10 item 3 names is that nothing NOTICES. Propose a
   report-only rider on the readiness board: per bot, an `audit:` cell that prints the worst
   failing/pending audit family for its pillar (e.g. `audit B pending 19/100`), no gate effect.
   Write it as a Devin lane spec in the `_wave-2026-09-10-lanes.md` house style: locate by grep,
   red test (a fixture whose pillar fails B must print it), green test, acceptance predicate,
   `--validate` still passes. Where the pillar verdict lives is part of the spec (propose a
   small `data/audit_gates.csv`: pillar · gate · verdict · as_of · evidence — written only by
   ruling, never by code). Gating on it later is a separate decision; say so.
4. **Exact doc text** for `docs/evidence-standards.md`: a new §5.1 "How the two systems meet"
   (the table + inheritance rule) and the strike-through of §10 item 3 with a dated banner citing
   T-53 and the ruling id Andy will sign. Write it so it can be pasted verbatim after the ruling.
   Do NOT apply it — go-live gates are decisions (CLAUDE.md §5). Also list the collisions §3
   warns about that your text touches (audit G1 vs board G1) and show you wrote the system every
   time.
5. **Gated vs mechanical**: one list of what needs Andy's ruling (the map, the n=0 option, any
   HOLD at LIVE-READY) and what is mechanical propagation once ruled (the doc paste, the
   portfolio row, the T-5x lane spec).
6. **What you did not read / could not verify**, plainly.

## 2 · Rules for this session
- No number without its source file read this session; an absent number is not a zero.
- Units on every figure: "positions", "condors", "per condor, ex-artifact". Never a bare count.
- Cite files and §, don't retell history. No v1 story.
- Do not edit `docs/evidence-standards.md`, `scripts/report.py`, `docs/RULINGS.md`. Edit only:
  the new drafts file, one appended entry in `docs/session-log.md`, and — LAST, one row —
  `data/portfolio.csv` T-53 status → `Working on it`, metric_note appended
  `| 2026-09-08 proposal drafted: drafts/_t53-gate-map-proposal-2026-09-08.md, awaiting ruling`.
  Then `python3 scripts/portfolio.py --check` must pass. Another Cowork session may be writing
  `session-log.md` / `portfolio.csv` tonight (T-48, T-50): re-read each immediately before the
  edit, append-only, never rewrite.
- Verify your own writes by `shasum -a 256 <file>` + a single-match grep, not by the tool's reply.
- Budget ≈45 min. If the reading shows the map is already written somewhere, STOP, write where,
  and do nothing else — check before doing (wave-1 trap 3).

## 3 · Close-out
Say "ready to commit" with the three changed paths and the proposal's sha256. Andy commits.
