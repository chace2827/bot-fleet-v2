# T-44 — G4 $ CAPS INTO report.py — DEVIN / Claude Code lane — 2026-09-03

Paste into a NEW Devin (free wrapper) or Claude Code session on a clone of origin/master:
"Read `drafts/_dispatch-2026-09-03-t44-g4-caps.md`. Implement it on a branch, open a PR with
red-green evidence in the body. Never commit to master. Never touch OA."

Ruling: `R-2026-09-01-G4-ROE-CAP` (docs/RULINGS.md; signed Andy 2026-09-02). Derivation:
`drafts/_roe-cap-proposal-2026-09-01.md` §1.5 (the values) and §2.5 (breach actions).
Portfolio item T-44 (P1). Devin promo expires 2026-09-16 — DEVIN lane first.

## 0 · Pre-flight (3 dispatches died on stale premises 08-17 — verify, don't assume)
- `git fetch && git checkout -b t44-g4-caps origin/master`. Record the head sha.
- Confirm these still hold in the working tree, else STOP and report:
  - `scripts/report.py` L~1001 `MAXDD_R_CAP = -5.0  # ... RoE $ cap still a <FILL> blank`
  - `scripts/report.py` L~1111-1112: G4 appended as `(mdd >= MAXDD_R_CAP, "... (RoE $ cap pending)")`
  - `docs/evidence-standards.md` G4 row says the `$` cap is an unfilled `<FILL>`
  - `data/bots_meta.csv` has an `epoch_boundary` column; 8 rows now carry a 2026-09-02 sizing note
    in `notes` (6 GF arms 1ct→26ct, Canary detach, 3DTE revert).
- Unit law (CLAUDE.md §4): unit = POSITION; condor = two spread rows paired by `trade_id`;
  risk = larger side. `pnl` column in `data/trades.csv` is per row (per leg). Sum per trade_id
  for position P/L.

## 1 · What to build — three caps, all read from one constants block
```python
# G4 dollar caps — R-2026-09-01-G4-ROE-CAP (signed 2026-09-02). Re-derive at n>=100.
G4_PER_BOT_DD_CAP   = -15_000   # cap 1: per-bot cumulative drawdown, PER EPOCH
G4_FLEET_DD_CAP     = -35_000   # cap 2: fleet cumulative drawdown (post-cutover, all signed bots)
G4_DAY_HALT_CAP     =  -8_000   # cap 3: single-day fleet loss halt
```
1. **Cap 1, per bot, per epoch.** Cumulative realised P/L (closed positions, by close_date) from
   the bot's latest epoch boundary (bots_meta `epoch_boundary`, else LEDGER_START); running peak;
   maxDD$ = min(cum − peak). G4 passes iff maxDD$ ≥ cap. The existing maxDD-R half stays as is;
   G4 is now `maxDD-R ≥ −5.0 AND maxDD$ ≥ −15,000`. Replace the "(RoE $ cap pending)" text.
2. **Cap 2, fleet.** Same computation over all ledger-eligible bots pooled, by close date, from
   LEDGER_START. Not a per-bot gate: surfaces as a fleet line in STATUS.md, GREEN/BREACHED.
3. **Cap 3, daily.** Per trading day (ET, close_date), fleet realised P/L; BREACHED iff any day
   ≤ −8,000. Report the worst day and its date. Also a fleet line.
4. **STATUS.md**: a new block `## G4 $ caps` with the three lines + the constants + the ruling id;
   and any BREACHED line is repeated at the TOP of STATUS.md (the standing "top of every brief
   until closed" rule, CLAUDE.md §5). Absent input renders `—`, never `0` (roster_board rule).
5. **docs/evidence-standards.md** G4 row: replace the `<FILL>` sentence with the three caps and
   the ruling id. Do not edit any other row.

## 2 · Acceptance predicates — state the derivation, never a literal
- Running `python3 scripts/report.py` on current data: every ON bot's G4 $ half PASSES (the
  ruling says no bot is near cap 1 today) and both fleet lines are GREEN; the worst single day
  in the post-cutover ledger is reported with its date and equals the minimum of the per-day
  sums you can recompute independently with a 5-line pandas/csv script in the PR body.
- **Red test, mandatory** (wave1 lesson: a predicate never seen red is not a predicate): a unit
  test that feeds a synthetic ledger with (a) one bot at −$15,001 cum DD → G4 FAIL, (b) a fleet
  day at −$8,000 exactly → BREACHED (≤, inclusive), (c) −$7,999 → GREEN, (d) an epoch boundary
  that resets a bot's DD so a pre-boundary loss does NOT count. Show the tests failing before
  the implementation (commit order or a pasted run) and passing after.
- `scripts/report.py --check` (if present) / `daily.sh` dry path still green; `roster.py --check`,
  `portfolio.py --check`, `pre_registration_ledger.py --selftest` unchanged.
- No new columns in any data CSV. No CRLF (`lineterminator='\n'`).

## 3 · Out of scope — do not do
- No OA edit, no toggle, no brake that ACTS. The caps REPORT; humans act (§2.5 "Who" column).
- No %-of-capital form (underived, R-6 says so).
- Do not re-baseline MAXDD_R_CAP. Do not touch G1–G3, G5, G6.

## 4 · PR body must contain
Head sha started from · the three constants · red-run output · green-run output · the
independent recompute of the worst day · a STATUS.md excerpt of the new block · "Andy merges".
Update `data/portfolio.csv` T-44 status → `Ready for review` with the PR number in metric_note
(same PR). Never commit to master; Andy merges (phase0 must be green).
