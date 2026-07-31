# Phase 1 Kickoff — Bot Fleet v2 Migration

*Written 2026-07-30, revised same day after deep review. Primary consumer: the dedicated MIGRATION CHAT in the current (old) Cowork project — that chat retains this project's memory. Secondary consumer: the eventual v2 Cowork project, which will have NO access to this project's chat history or memory — this file must therefore stand alone, and gets copied into `bot-fleet-v2/docs/` during Phase 1 as the permanent handoff record. Everything needed is in this file + `docs/rebuild-audit-2026-07-29.md` (the full audit memo, same folder).*

**Execution spec for the migration session:**

---

Requires both folders connected: `bot-fleet` (old — treat as READ-ONLY archive; never modify) and `bot-fleet-v2` (new — the build target; Andy creates the empty folder and adds it via "Add folder"). Read, in order: `bot-fleet/docs/phase1-kickoff-2026-07-30.md` (this file) and `bot-fleet/docs/rebuild-audit-2026-07-29.md` (the governing memo — its DOC TRIAGE, MIGRATION MANIFEST, and PHASED PLAN sections are the spec). Then execute Phase 1:

1. Run the memo's copy manifest: CARRY files verbatim into `bot-fleet-v2/` (same subpaths), including `data/`, `scripts/`, `.env`.
2. Write fresh in v2: `CLAUDE.md` (9-section outline in the memo), `docs/current-state.md` (seed from §"Corrected truth" below), `data/corrections.csv`, `docs/build-plan.md` (from §"Adopted plan" below — this SUPERSEDES approach-reset Part 3/5), `docs/reactivation-runbook.md` (from §"Lapse mechanism" below), `README.md`.
3. Apply the one-cell fix: `bots_meta.csv` HedgeD `strike_fix` Y→blank.
4. Completion test: answer "what is actually true about the champion and the Fortress pair?" from v2 files alone, correctly.

Do NOT copy: Cockpit/scalp files, session-log, pivot-vwap/trigger-rules, investor-profile, cleanup-proposal, `_archive/` (see memo KILL list). Old folder is never modified.

---

## Decisions already made (do not re-litigate; Andy confirmed each)

- **New project, new folder, curated import.** Old folder = permanent archive (git repo `chace2827/bot-fleet`; `.env` NOT in backup).
- **`approach-reset-2026-07-29.md` is DEMOTED**: authoritative diagnosis, superseded plan. Andy distrusts it as a plan. `rebuild-audit-2026-07-29.md` + this file govern on conflict.
- **Adopted plan = hybrid**: greenfield IC family (4–6 fresh bots) + legacy champion & 130PM kept ON as the control/benchmark arm with only two safety fixes (re-entry gate → `opened this side today`; Cleanup Market→SmartPricing). Fortress pair restored in place (its pre-regression record, +2.9%/+3.1% Exp(R), is the IC history worth preserving). Mirrors never refactored. Directional params frozen (only OOS-validated assets). **Put-Control: decision deferred to Phase 4 pre-registration — default is NOT restarted** (its gate-proof function is already served by the OOS control backtest).
- **Legacy champion identity (DECIDED — see Day-0 exception below): its dead PT25 is formally REMOVED, making ride+S2 its official, pre-registered config.** Rationale: it has 29 post-fix condors of exactly that behavior (the baseline continues unbroken), and PT-variant questions belong to the greenfield arms (hard-PT / trailing / ride), which are built matched for that purpose. Consequence: the Day-0 re-arm sweep applies to all bots EXCEPT the legacy champion + 130PM pair, whose Exit Options are deliberately absent/removed — document this exception in the runbook so a future session doesn't "fix" the control arm. [If Andy overrides to re-arm PT25 instead, the champion needs a new epoch boundary and the greenfield ride arm becomes the sole ride benchmark.]
- **IC pillar stays and grows** — growth earned at gate-clearance, not scheduled.
- **Evidence law**: T1–T5 tiers + sample gates (n≥100 / 6 mo / regime change) from the independent audit's pre-commitment ledger, layered on the R methodology. The audit's verdicts (kill-IC, third-party switch) are overruled; its machinery stands. Andy may redesign scoring later.
- **Sizing**: stage-tiered — experiments 1-lot; CANDIDATE+ uniform ~$5K risk/position via OA $-risk cap; tournament arms always identical allocation; set once at restart, never ad hoc. Compare by R, never raw P/L.
- **Never reset OA history by cloning** (Symbols drop, history fragments, slot burn). Epoch boundaries in `bots_meta` + the local ledger are the clock-reset. Fresh builds only for new strategy identities + rebuilt tournament arms.
- **Excluded from v2**: TT3, Intraday Cockpit, discretionary-scalp material, `investor-profile.md` (do-not-distribute per independent audit).
- Daily loop: Claude detects → instruction cards → **Andy makes ALL OA edits**, each verified via the first new position's **Trades list** (the Exit Options panel/editor is NEVER evidence).

## Corrected truth (numbers recomputed from trades.csv, 2026-07-29; ledger current to 7/02 — fleet frozen since)

- Fleet raw −$83,130 → **economic −$70,512** (= raw + A1 $3,000 + A2 $4,809 + A3 $4,809; A4 is NOT a dollar exclusion — see next line). −$79,997 of raw sits in 16 strike-bug/mis-built QQQ bots → decision signal ≈ nil.
- `corrections.csv` has two record types — **dollar artifacts**: A1 champion T00147 6/11 call leg, $3,000 impossible fill (R −1.63); A2/A3 Fortress + NoPT50 legs 6/12–6/26 (−$4,809 each, zero exit orders). **Quarantine flags** (real cash, excluded from strategy evidence, not from dollar totals): A4 champion legs ≥2026-06-01 = "exit-engine-off era" (see Lapse section).
- Champion: −$11,155 raw all-time; post-fix epoch −$2,455 ex-A1 over 29 condors, Exp(R) −1.7% — THIN, and it ran ride+S2, not PT25+S2 (the post-fix epoch sits entirely inside the exit-off era). **Pre-lapse (Mar 5–May 22): 306 legs, 306 closed, 0 expired, ~119 closes at the exact PT25 price → PT25 worked; the bot was NOT misbuilt.** Caveat: that pre-lapse record is exit-clean but ENTRY-contaminated (positions opened ~9:xx; the 11:00/Range075 entry config only governed from 6/08). **The full declared combo — 11:00 + Range075 + PT25 + S2 — has never run as a whole; its clean sample size is zero.**
- Fortress +$2,975 / NoPT50 +$2,760 strategy-attributable (pre-6/12, +2.9%/+3.1% Exp(R)); their June losses were execution artifacts.
- 7/02 "S2 helped" is FALSE — S2 cost $2,300 (SPX settled above the short put). S2 post-fix net −$3,285: healthy ≠ profitable.
- HedgeD −$15,376 is real but tested an immediate $1-ITM stop (no sustain condition exists on OA), not "Conditional"; 0/86 strikes malformed. Hedge tournament INVALID as selector (S1≈D 73/86 identical; S3 wrong mechanic + faster execution class; no arm has Range075).
- `QQQ-IC-0DTE-Baseline` −$31,580 (38% of fleet loss): NEVER audited — forensic required before any IC-growth conclusion.
- Directional put (+6.4% RoR OOS) and call (+21.9%) both OOS-passed; PutVIX22 0 trades in 22 days (VIX never ≥22 — gate correct, bot health unverified).

## Lapse mechanism (SOLVED 2026-07-30 — OA support + billing history + ledger)

Billing: May 18 charge FAILED → ~5-day grace → deactivated ~5/23 → May 31 PAID → Jun 30 FAILED → **inactive now**; Andy reactivates ~mid-Aug.
Mechanism: deactivation turns off automations + Exit Options. On resubscribe, **automations resume but Exit Options on pre-lapse bots do NOT re-arm** — invisibly (editor still displays the settings). Proof: champion PT25 died June 1 (first session back) while its 6/14 clone works (70/0); Fortress (bot-level exits) died the same way → placement is not protection; one Exit Options engine, one off state. Bots built after May 31 all fine; monitors unaffected.
Consequences baked into the build:
- **Day-0 Reactivation Runbook (write it in Phase 1):** pay → re-arm + verify Exit Options on ALL bots **except the legacy champion + 130PM pair (deliberately Exit-Option-free ride+S2 controls — do not "fix" them)** → capture everything → Button test-fire / first-position Trades-list check per bot → only then allow entries.
- **Re-arm procedure ANSWERED (OA support, Zack, 7/30): each bot's dashboard has a per-bot "EXIT OPTIONS" ON/OFF toggle at top right, next to the AUTOMATIONS toggle.** This is the hidden state: post-lapse, AUTOMATIONS toggles were back on (monitors fired) but EXIT OPTIONS toggles stayed off (all PT/time exits dead). Day-0 sweep = verify BOTH toggles per bot (screenshot them — toggle state doesn't survive text capture) + still do one order-level verification, since the toggle being ON was never the failure we observed being detected. Design implication (already built in): one toggle kills every Exit Option on a bot at once — PT, Touch, time exit together — which is why the 15:52 Scheduled Event backstop lives on the AUTOMATIONS side. For the champion + 130PM controls, remove PT25 from the Open Position action explicitly rather than relying on their toggle staying off.
- **Greenfield exit architecture:** exits = named Exit Option Preset in the Open Position action (PT% as Bot Input · Touch $0 challenged-side · time exit) + **15:52 flat-close Scheduled Event backstop** (different execution class — automations survived the lapse, Exit Options didn't) + position-closed-trigger automation to close the sibling spread (replaces the emergent Cleanup race) + daily behavioral checks (expired:closed flip; mfe≥PT with no PT order) which catch engine death same-day. Optional: 1-lot canary bot whose PT should fill daily.
- Edits made while inactive DO persist (verified empirically 7/29→7/30). Build-before-reactivation is viable; log every inactive-era edit.

## Support answers on capabilities (one rep — verify in UI during Phase 2)

- Touch Exit Option: underlying vs short strike; "Touch $0" exits the challenged position. Per-spread → sibling-close needs the trigger automation.
- Exit Options CAN reference Bot Inputs (at open and via update-exit-options actions).
- Archived bots in Export CSV: "I believe so" — run the one-dead-bot probe before archiving anything.
- Rep did not know the documented Excessive Errors Failsafe — treat single-rep answers as one source.

## Open items to carry

Export-Data bot-column check (10 min, decides capture architecture) · re-arm procedure (support pending) · Baseline forensic · PutVIX22/CallVIXdrop toggle screenshots · 48 cached symbol-days of 5-min tape possibly unrecoverable (note the gap) · RoE `<FILL>` blanks stand (per-bot max-loss placeholder in pre-registration template) · Notion role undecided · evidence-standards redesign session (Andy wants one) · Sonnet for mechanical sessions, big model for judgment sessions.
