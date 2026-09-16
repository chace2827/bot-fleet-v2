# GF FAMILY SIZING — Opus chat (Cowork, bot-fleet-v2 folder + Chrome/OA) — drafted 2026-08-31

Andy's intent (2026-08-31, Fable chat): **size the GF family like real-life trading —
≈$5K risk per leg, per bot, per day (≈$10K total per bot)** — so its results are directly
comparable to the SPX arms and no longer read as $7 opens / $1 closes. Identical across all
arms or not at all.

## Order of operations — STRICT
Phase 1 DRAFT (no edits anywhere) → Andy SIGNS in-chat → Phase 2 EXECUTE in OA → Phase 3 RECORD.

## Phase 1 — draft (read first, touch nothing)
Read: `docs/pre-registration-ledger.md` (the 7 GF arms' MAX LOSS "1 lot per arm until one
clears its interim read; then ≈$5K risk/position" + "~$185 net risk per condor; 1 condor/day"
lines, and Canary's entry specifically), project memory [[shared_automation_edit_surface]] +
[[gf_entry_gate]], `data/captures/2026-08-31-roster/07-allocation-and-groups-2026-08-31.tsv`,
STATUS.md readiness board.
Produce for Andy's signature:
1. **The amendment ruling** (`_rulings-draft-2026-09-01-gf-sizing.md`): amends the 7 ACTIVE
   arms' MAX LOSS/SIZING lines (Ride-Delta is ARCHIVED — excluded) from 1-lot to
   ≈$5K risk/leg; STATES the new family daily aggregate explicitly (7 arms × ≈$5K ≈ $35K —
   the old $10K QQQ-sleeve language must be re-ruled, never silently violated); one-time
   amendment under "set once, never ad hoc".
2. **The contract math, derived live**: risk/contract on the $2-wide QQQ spread =
   (width − typical credit) × 100 ≈ $193 → N = round(5000/193) ≈ 26ct. Derive N from the
   actual current numbers in-session and show the derivation; Andy approves the final N.
3. **The exact edit plan** — CRITICAL: the entry scanners `GF-ScannerA/B` are a SHARED
   library. First enumerate EVERY automation/bot referencing them (any non-GF bot sharing
   them = STOP and report). Decide and state whether the contract-count lever is the shared
   scanner (one edit propagates to all arms — ideal for "identical", dangerous if shared
   wider) or per-bot; plus allocation $2,500 → $10,000 per arm so the new size fits.
4. **Canary check**: read its pre-reg entry — if its instrument role requires 1-lot, flag it
   and propose keeping Canary at 1ct with that stated in the ruling; Andy decides.

## Phase 2 — execute (ONLY after Andy signs in-chat)
oa-driving skill discipline throughout: config hash before/after every edit, re-read after
save, a version bump is NOT evidence, drawer ✕ discards, never type paths into save dialogs.
All arms edited in one sitting, identically. Confirm each bot Paper Trading before touching.
Outer check: full /bots capture BEFORE and AFTER, diffed — exactly the intended bots changed
and nothing else (the 08-31 `10-authorized-edits` pattern). Save captures to
`data/captures/<ET-date>-gf-sizing/` with SHA256SUMS.
⚠️ ET date from the capture's own header, never the clock (UTC trap).

## Phase 3 — record
- Apply the signed amendment text to `docs/pre-registration-ledger.md` (append DISCHARGE/
  AMENDED lines; never rewrite original text — the PR-04 discharge pattern).
- `data/bots_meta.csv`: SIZING EPOCH note per amended arm ("<date>: 1ct→Nct, ≈$5K risk/leg
  per R-<ruling id>; raw P/L not poolable across this boundary; R unaffected").
- Everything rides the next nightly close commit (Andy commits). NOTHING here changes R,
  sample counts, or gate progress — the readiness board is size-free by construction.

Deliverable at end: one summary — ruling signed y/n, N chosen, edits applied with hash pairs,
fleet diff result, files awaiting commit.
