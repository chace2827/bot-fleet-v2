# BACKFILL + HYGIENE — Opus chat (Claude Code, ~/bot-fleet-v2) — 2026-08-31

Paste into a NEW Opus Claude Code session in ~/bot-fleet-v2:
"Read `_dispatch-2026-08-31-2-backfill-hygiene-claudecode.md`. Execute phases 0–E in order.
Andy runs every commit (R-2026-08-21-STAGING-MANIFEST). Report in the §R format."

PREREQ from Andy before Phase C: tonight's FULL closed-position export from OA, saved under its
DEFAULT filename in ~/Downloads (never type a path into the save dialog), then
`mv` → `data/raw/2026-08-31.csv`.

## 0 · Pre-flight
- ⚠️ The close-wave merged D1 (PR #65) and D2 (PR #66) to origin/master AFTER local last
  pulled, and may merge D3 too. First: `git fetch origin && git pull --ff-only`. If the pull is
  not a fast-forward, STOP and report — never merge or rebase on your own. Then verify the
  rulings commit `1f29e2f` is an ancestor of the new head (`git merge-base --is-ancestor`), and
  record the head sha you're working from (read LOOSE refs; `packed-refs` is stale by design).
- Verify every premise below against the working tree before acting on it (3 dispatches died on
  stale premises 08-17). Context files: `_review-2026-08-31-vacation.md` (findings + expected
  numbers), `docs/RULINGS.md` (the three 08-21 close rulings).

## A · Hygiene (working-tree fixes; nothing committed yet)
1. `git mv`/rename `data/captures/2026-08-20-recon/` → `data/captures/2026-08-19-recon/`
   (misdated: ran 20:32 ET on 08-19; UTC trap). Untracked, so plain `mv`.
2. Delete `one` (0-byte 08-18 shell accident, repo root).
3. `docs/AI Agentic.pdf` (20.4MB untracked binary): move OUT of the repo to `~/Documents/` and
   tell Andy where it went. Do not commit it.
4. `.gitignore`: ensure `_locktrash/` is listed; review Andy's uncommitted .gitignore diff and
   keep it.
5. `git rm --cached .claude/settings.local.json` (tracked despite `.claude/` ignore rule —
   confirmed lane-contamination vector, R-2026-08-19-LANE-STATE-OWNERSHIP).
6. Keep the uncommitted `docs/session-log.md` addendum (7 lines, 08-21) staged for the commit.

## B · B-70 verification + PR-04 discharge edit
1. **B-70: VERIFY, do NOT add.** ⚠️ CORRECTION (08-31 OA sweep): "Friday 14 DTE Broken Wing IB
   (B-70)" is ALREADY in `data/bots_meta.csv` (line ~24, pillar OA-Mirror, role mirror-watch)
   and roster.py's Live-mirrors rule places it. Assert EXACTLY ONE row matches `B-70` — adding a
   second row is the known silent-P&L-reroute defect (roster-invariant lesson). Run
   `roster.py --validate`; expect 44 bots, set-diff OA-roster vs bots_meta = zero (the 08-31
   capture bundle proves the OA side).
2. **PR-04 discharge edit (Andy-authorized 2026-08-31, Fable chat).** In
   `docs/pre-registration-ledger.md`, the `QQQ-IC-0DTE-Fortress-NoPT50` (PR-04) SIGNED block:
   append a discharge note — first trading day 2026-08-26 verified from
   `data/captures/2026-08-31-roster/04-pr04-discharge-trades-2026-08-31.txt`
   (sha256 ea520796b5e6019d…, complete it from the bundle's SHA256SUMS.txt): time-exit row
   present (Close 3:50PM, `Exit Trigger: Expires in 10 minutes`), NO PT row (Exit Options all
   None), backstop negative (15:50 trigger, not the 15:52 backstop). Precedent
   R-2026-08-18 SUBSTITUTE-VERIFY (5a). Remove/annotate the `FIRST-TRADING-DAY CAPTURE OWED`
   phrase so the banner parser (which keys on `SIGNED != VERIFIED` + `FIRST-TRADING-DAY CAPTURE
   OWED` together) clears the bot — then re-run report.py and CONFIRM the unsigned banner drops
   NoPT50 and keeps QQQ-IC-0DTE-Fortress / QQQ long call / Tasty Condor. Do not touch the parser.
3. **PR-23 (GF-QQQ-IC-Ride-Delta) MOOT annotation (Andy-authorized 2026-08-31, Fable chat).**
   IF AND ONLY IF the OA lane confirms the archive was executed (bot-local scanners OFF +
   automations OFF, with before/after hashes in that chat): annotate PR-23's ledger entry —
   hypothesis MOOTED by `R-2026-08-17-GF-ENTRY-METHOD` (family-wide delta adoption removed the
   fixed-strike comparator); pre-fix sample EXCLUDED (four-scanner race made those days
   one-sided trades — see `_review-2026-08-31-vacation.md` addenda); bot archived 2026-08-31.
   Update its `bots_meta.csv` row: status OFF, note the archival. If the OA edit is NOT yet
   confirmed, skip this step entirely and flag it — never record an OA state you haven't seen
   evidenced.
4. **bots_meta notes (small, evidence-backed — from `10-authorized-edits-2026-08-31.md`):**
   3DTE $140-$350 — append a note: "SIZING EPOCH 2026-08-31: allocation $5K→$10K; POSITION SIZE
   is 26% of net liquid, so per-position dollar size DOUBLES from this date — don't pool raw
   P/L across the boundary (R unaffected)." QQQ long call — append: "2026-08-31: 3 legacy opens
   closed (realised -$8,693, all opened pre-LEDGER_START, ledger-ineligible); zero open
   positions remain; F-8 class closed."

## C · Backfill — one run ingests all 8 missing days
`scripts/daily.sh 2026-08-31` on the fresh full export. All 9 stages exit 0. NO override flags;
if any stage refuses, STOP and report — do not silence a guard (I-05: receipts can't show argv
yet).
Acceptance — DERIVATIONS, never literals; each predicate must be seen red once against a mutated
fixture before it counts:
  (a) Frozen history: sum of ledger P&L for close-days ≤ 2026-08-19 equals the value in
      `git show HEAD:STATUS.md` (derive both sides; do not hardcode).
  (b) Continuity: new cumulative == (a) + [sum over export rows with openDate ≥ LEDGER_START
      and closeDate in 2026-08-20..2026-08-31] — derive the bracket from the raw export
      yourself.
  (c) Legacy exclusion: rows opened before LEDGER_START (a Jun-1 QQQ long call expiry, a Jun-22
      Tasty Condor expiry) appear NOWHERE in the post-cutover ledger.
  (d) B-70's trade is IN the ledger, routed to the OA-Mirror pillar, roster.py runs clean, and
      bots_meta still has EXACTLY ONE B-70 row.
Second surface: `_review-2026-08-31-vacation.md` §Headline states the independently derived
expectations (ex-legacy vacation ≈ -$149; cum ≈ $4,557). If your derivation disagrees, STOP and
report the delta — never reconcile silently (verification-surfaces rule).
Known benign anomalies to REPORT not patch: should-have-fired / decidability-countdown windows
assume daily cadence and will look odd across an 8-day gap.

## D · Regenerate the boards
`daily.sh` stage `report.py` rewrites STATUS.md — **this is where the Readiness board (G1–G6)
and R scorecard update** with the vacation sample (130PM should land n≈20 within days; check
whether it crosses G2 right now). Then run `scripts/roster.py` and `scripts/portfolio.py`
manually (they are NOT in daily.sh — parked I-03/I-04) with their --check/--validate modes, and
regenerate roster.html / portfolio.html.

## E · Staging manifest for Andy
Also include the Fable chat's 08-31 portfolio refresh (`data/portfolio.csv` + `portfolio.html`
— run `portfolio.py --check` first, expect clean, 9 programs / 92 items) and the OA sweep's
ready-to-commit files: `data/captures/2026-08-31-roster/` (11 files,
verify `shasum -c SHA256SUMS.txt` first), plus the sweep's `docs/session-log.md` and
`docs/state.md` edits.
Print a file-by-file `git add` list + one commit command covering phases A–D outputs, per
R-2026-08-21-STAGING-MANIFEST (`close_manifest.py` doesn't exist yet — hand-write the list).
`_*` files, `.claude/`, `_locktrash/`, `one` in the staged set = FATAL. Andy reviews and runs
the commit + push himself. Leave `_review-2026-08-31-vacation.md` and the `_dispatch-*` files
untracked.

## R · Report format
Per phase: done/blocked + evidence. Then: predicates (a)–(d) with both derived sides shown, red
test proof for each, STATUS.md new headline (cum P&L / legs / bots), readiness-board movements
(who crossed or approaches G2), roster bot count, the staging manifest verbatim.
