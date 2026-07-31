# Rebuild Audit & Migration Plan — 2026-07-29

*Consultant memo. Phase 2 of the rebuild engagement. Decisions locked in Phase 1: IC pillar stays and grows; independent audit retains evidence-machinery authority only (tiers + sample gates, per Q2=B/Q14=B); Cockpit + discretionary-scalp material stays behind; new Cowork project in a new folder with curated copies; daily loop = detect → instruct Andy to fix in OA (~2–5 min/day); deliverable saved here + chat.*

*Every number recomputed from `data/trades.csv` (1,380 legs, ledger current to 2026-07-02 — the fleet has been frozen since, so this ledger is current) with the 7/27–28 forensics as the sanctioned correction layer (Q16=a). Condor risk = larger side, per the independent audit's harsher (correct) convention.*

---

## VERDICT

**New project, new folder, curated import — confirmed, and I'd make the same call unprompted.**

The strongest reason: the thing being rebuilt is not the docs, it is the *trust chain*. The current project's daily loop (`daily.sh` → instruction-mirror cards → G5 compliance gate) validates bots against `bots_config.csv` — a hand-written record the forensic proved wrong on 3 of 4 audited bots. The champion scored **100% compliance on 5 consecutive graded days while its PT25 never fired once** (`data/compliance.csv` rows 6/26–7/02 vs `config-vs-reality-2026-07-28.md` §1). Cleaning in place means rebuilding the loop on top of 50 documents whose narrative layer still asserts the pre-audit world, with every future session inheriting the ambiguity about which layer wins. A fresh folder makes the corrected record the *only* record, and the old folder (intact, git-backed to `chace2827/bot-fleet`) remains the evidentiary archive.

The three criteria, weighed honestly rather than pretended into alignment:

- **(a) Speed to a trustworthy daily brief:** mildly favors clean-in-place — `daily.sh` runs today. But "runs" ≠ "trustworthy": the brief's compliance layer is the thing that failed. Since the loop must be rebuilt either way, the speed penalty of a new folder is one session of copying, not weeks. Net: wash.
- **(b) Long-term maintainability:** strongly favors new. The doc corpus is ~1.0 MB across 50+ files; the load-bearing, still-true subset is ~15 files. CLAUDE.md's file map is itself a maintenance liability (33 entries, several pointing at superseded content).
- **(c) Risk of losing hard-won knowledge:** the real risk of migration — and it is fully mitigated here because *nothing is deleted*. The old folder persists with git history; anything the manifest misses is retrievable. The residual risk is subtler: a future session in the new project won't know what it doesn't know. Mitigation: the new CLAUDE.md carries an explicit "archive pointer" section naming the old folder and what lives there.

**Biggest risk of the call:** the new project starts before the OA account is reactivated, and the momentum of a clean folder substitutes for the harder work of the OA-side remediation and the continue decision. The phased plan below is sequenced so that instrumentation and remediation — not doc curation — are the critical path.

**On the IC-continue question (Q1, argued as requested):** continuing the IC pillar is defensible *only* in the form the reset doc prescribes — instrumented, pre-registered, and on the small roster. The honest evidence status: the champion's declared strategy (PT25+S2) has literally never run, so it is neither validated nor falsified; what *did* run (ride+S2, post-fix) shows Exp(R) −1.7%/condor ex-artifact (n=29 — THIN under the adopted gates, meaningless either way). The independent audit's "94% vs 36% band" argument is the strongest counter-case and deserves a real answer — but it was computed on the contaminated full ledger including 317 pre-fix champion legs that opened at 9:xx against an 11:00 config, and on QQQ arms now known to be mis-built. It is not decision-grade either. Meanwhile the pre-regression QQQ-Fortress window (+0.029 Exp(R), 21 condors) and the 130PM clone (+0.000, n=28, CI straddling zero) show the structure is not obviously dead when its exits actually fire. **Verdict on IC: continue at pilot scale under pre-registration; "grow it" is earned at gate-clearance, not scheduled.** Growing the pillar before one IC bot has produced 100 provable-config positions would repeat the exact failure this rebuild exists to end.

---

## LOSS FIGURES: STATED vs. ACTUAL

Corrections applied (provenance for each in the forensics; all CONFIRMED unless noted):
**A1** — 6/11 champion T00147 call leg: $3,000 of the −$7,740 is a structurally impossible fill ($5-wide filled at $7.50; R = −1.63 > max loss 1.0 — visible in the ledger itself). **A2** — QQQ-Fortress 6/12–6/26: 11 legs, −$4,809, zero exit orders generated (execution artifact, real cash but not strategy evidence). **A3** — same for Fortress-NoPT50: 11 legs, −$4,809 (INFERRED strong — same pattern, no order-level screenshot).

| Bot | Stated | Actual (corrected) | Source of stale figure | Root cause of delta | Confidence |
|---|---|---|---|---|---|
| **Fleet total** | −$83,130 | −$70,512 economic (ex A1–A3); of which −$79,997 raw sits in 16 strike-bug-flagged QQQ bots → decision-grade signal ≈ nil | `current-state.md` L22, `STATUS.md` L6 (raw is *arithmetically* right, decision-wrong) | Artifacts + contaminated cohort dominate the headline | CONFIRMED (recomputed) |
| **IC-SPX-FastPT25-S2** (champion) | −$10,305 / 207 condors (`current-state.md` §IC — stale even vs its own ledger); −$11,155 / 221 (`STATUS.md`) | −$8,155 ex-A1 all-time; **post-fix epoch (only window declared entry config governed): −$5,455 raw → −$2,455 ex-A1, 29 condors, Exp(R) −3.8% raw → −1.7% corrected** | `current-state.md` (pre-7/03-ingest number never updated in §IC) | A1 + epoch conflation + the strategy that ran was ride+S2, not PT25+S2 | CONFIRMED |
| **QQQ-IC-0DTE-Fortress** | −$1,834, PF 0.83, "naked tail needs a stop" | **+$2,975 strategy-attributable** (pre-6/12, 21 condors, Exp(R) +2.9%); June −$4,809 = dead-exit artifact | `STATUS.md` L35; `backlog.md` NOW (put-stop framing) | Exit conditions silently dead from 6/12 (billing-lapse-coincident); zero exit orders sent | CONFIRMED (Trades lists) |
| **QQQ-IC-0DTE-Fortress-NoPT50** | −$2,049 | +$2,760 pre-6/12 (18 condors, +3.1%) | `STATUS.md` L34 | Same regression, same dates | INFERRED (strong) |
| **S2 hedge (champion)** | "fired and cut early and helped" (7/02) | 7/02 cost $2,300 (SPX settled 7483.24 vs 7445 short put; hold = +$350); post-fix S2 net **−$3,285** | `session-log.md` 7/03 entry; `current-state.md` ingest block | Misread OA "PRICE AT CLOSE" (13:02 exit print, not settle) | CONFIRMED |
| **QQQ-HedgeD-Conditional** | −$15,376, "strike-bug contaminated," tests the Conditional hedge | −$15,376 is real — but it tested an **immediate $1-ITM stop** (no sustain condition exists), not Conditional; 0/86 strikes malformed, so the contamination label is wrong for this bot | `current-state.md` L23 ("~−$45K, strike-bug contaminated"); `bots_meta.csv` strike_fix=Y; readiness board G1 blocker | Mis-implemented mechanic + mis-applied contamination flag | CONFIRMED |
| **Hedge tournament (S1/S2/S3/D)** | Matched-day Exp(R) ranking selects a hedge | Ranking cannot select: S1≈D identical P/L 73/86, S3 mis-implemented + faster execution class, no arm has Range075 | `hedge-research.md`, `STATUS.md` tournament section | Arms tested something other than their names | CONFIRMED |
| **QQQ-IC-0DTE-Baseline** | −$31,580 (38% of fleet loss) | **Unverified** — never audited; largest unknown in the fleet | — | Would settle: forensic pass like the Fortress one (strikes vs tape vs settle, per-position) | — |
| **DIR-SPX-PutVIX22-SL75** | "paper-live since 6/25" | 0 positions in 22 days; VIX max 20.72 — gate correct, **bot health unverifiable** from evidence emitted | `current-state.md` §Directional | Correctly-gated and switched-off emit identical evidence | CONFIRMED (Tradier) |

Root-cause attribution across the audited slice (35 losing positions, `data/execution_audit.csv`): **settings 23 (66%) · by_design 9 (26%) · oa_execution 3 (9%)**. The hard line: **only A1 ($3,000) is pure accounting artifact** (never happened economically). A2/A3 (−$9,618) were real cash losses but are *execution* evidence, not *strategy* evidence. The QQQ hedge-family losses (~−$45K) were real and are evidence about mis-built mechanics, not about the strategies they were named for. Genuine strategy losses with clean attribution are a small minority of the headline — which is exactly why "continue vs shelve" was unanswerable from this data.

---

## CONTRADICTIONS THAT WOULD MISLEAD

Only contradictions a future session would actually trip over; trivia skipped.

| # | Claim | File asserting it | File that wins | Why |
|---|---|---|---|---|
| 1 | Champion runs PT25+S2; go-live gate CLEARED 18/15 | `STATUS.md` L14; `current-state.md` §IC; `ic-strategy-reference.md` | `config-vs-reality-2026-07-28.md` §1 | PT25 generated 0 orders / 47 positions; the gate certified ride+S2, a strategy nobody chose |
| 2 | G5 instruction-mirror compliance = config verified (champion 100%×5) | `data/compliance.csv`; `daily-brief-spec.md`; readiness board | `approach-reset-2026-07-29.md` §1.1 | Compliance was scored against `bots_config.csv`, itself hand-written and wrong — fidelity to a false record |
| 3 | "7/02: S2 fired and cut early — helped" | `session-log.md` 7/03; `daily-ledger-archive.md` | `config-vs-reality-2026-07-28.md` §6 | SPX settled 38 pts above the short put; hold was +$350, S2 cost $2,300 |
| 4 | Conditional hedge = "sustained ~$1 past strike ~10 min (monitor with time-persistence condition)" | `oa-platform-reference.md` §14 | `oa-docs-research-2026-07-29.md` §1 | OA cannot express persistence at all (docs affirm); the mechanic as documented is unbuildable natively |
| 5 | "QQQ hedge family ~−$45K, strike-bug contaminated" (incl. HedgeD); `strike_fix=Y` on HedgeD | `current-state.md` L23; `data/bots_meta.csv`; readiness board G1 | `config-vs-reality-2026-07-28.md` §6 | HedgeD: 0/86 malformed strikes — its result is real (and damning of the mis-built mechanic), not noise |
| 6 | Fortress needs a put-side stop (ride −8.3% vs SL75 +2.7%) — the OVERDUE NOW decision | `backlog.md` NOW; `STATUS.md` per-bot cut | `qqq-fortress-loss-forensic-2026-07-27.md` | The "naked tail" was a broken bot: its own PT50+15:50 exits were dead; restored, June flips −$4,809 → +$3,227. Decision is *restore & verify*, then re-ask |
| 7 | Hedge question owned by the tournament; decide by tournament | `hedge-research.md`; `research-roadmap.md` | `approach-reset-2026-07-29.md` §1.3 | Tournament invalid as a selector until arms are rebuilt matched |
| 8 | Three pillars: IC, OA Mirror, **TT3** | `north-star.md` | `CLAUDE.md` (4 pillars, TT3 excluded) | Predates the reorg; would reintroduce excluded content |
| 9 | HedgeD `filter: Range075` | `data/bots_config.csv` | `config-vs-reality-2026-07-28.md` §3 | No filter node exists; 36% of entries outside the band |
| 10 | Position Exit Options panel shows what will execute | implicit throughout pre-7/27 docs | `qqq-fortress-loss-forensic` §1 + `oa-docs-research` N3 | Exit Options copy per-position at open; the panel is not evidence — the Trades list is |
| 11 | "Edge proven on data" (family-facing) | `investor-profile.md` | `independent-audit-2026-07-27.md` | The same folder's ledger contradicts it; do not distribute |
| 12 | Champion −$10,305 / 207 condors | `current-state.md` §IC | `STATUS.md` (−$11,155 / 221) | Narrative not updated after the 6/29–7/02 ingest; generated file wins by law |

---

## DOC TRIAGE

Buckets map to migration actions: **CARRY** = copy to new folder verbatim (header note allowed) · **REWRITE** = copy with substantive correction · **MERGE** = fold into a named winner during the copy · **KILL** = stays behind in the old folder (nothing is deleted; the old folder is the archive).

**CARRY (17)**
`docs/approach-reset-2026-07-29.md` (the vision) · `docs/config-vs-reality-2026-07-28.md` · `docs/execution-audit-ic-spx-fastpt25-s2-2026-07-27.md` · `docs/execution-audit-qqq-range075-pt50-wide2-1230pm-2026-07-27.md` · `docs/execution-audit-qqq-hedged-conditional-2026-07-28.md` · `docs/execution-audit-dir-spx-putvix22-sl75-2026-07-27.md` · `docs/qqq-fortress-loss-forensic-2026-07-27.md` · `docs/independent-audit-2026-07-27.md` + `-precommitment-ledger.md` (evidence-machinery authority per Q2=B; verdicts annotated as overruled where they are) · `docs/oa-docs-research-2026-07-29.md` · `docs/oa-capture-coverage-2026-07-29.md` · `docs/oa-capture-bookmarklet-2026-07-28.md` · `docs/daily-review-design-2026-07-29.md` · `docs/instrumentation-decision-2026-07-29.md` · `docs/directional-oa-build-sheet.md` (validated results + queue) · `docs/strategy-taxonomy.md` · `docs/backtest-ingest-protocol.md` · `docs/cross-functional-reference.md` · `docs/oo-trial-backtests.md` · `docs/ic-trailing-stop-backtest.md` · `docs/lean-backtesting-reference.md` · `docs/quantconnect-lean-exploration-brief.md` · `docs/oa-mirror-reference.md` (§3 evidence standards load-bearing; add header pointing to the new evidence-standards doc). Data/scripts: `data/trades.csv`, `data/raw/`, `data/brief/`, `data/execution_audit.csv`, `data/compliance.csv`, `data/lessons.csv`, `data/bots_meta.csv` (with fix below), `scripts/` (path review on copy), `.env`/`.env.example`.

**REWRITE (8)** — reason each:
- `docs/oa-platform-reference.md` — §14's Conditional definition is unbuildable (contradiction #4); Exit-Options-panel-as-evidence implicit throughout; fold in the 8 new primitives from `oa-docs-research` (Touch, position-opened triggers, Failsafe, input fallback, Instant-Exit live-only).
- `docs/ic-strategy-reference.md` — describes a two-chat architecture and bot names that no longer exist ("Scalp-SPX"), and asserts champion mechanics (#1) the audit falsified. The IC mechanics primer inside it is good; the program description is wrong.
- `docs/hedge-research.md` — philosophy + mechanic catalog + evidence anchors carry; every tournament-derived ranking and the hedge→bot matrix must be stamped INVALIDATED-7/28 pending rebuilt arms.
- `docs/methodology.md` — layer in the adopted evidence law (T1–T5 tiers + B-gates over the existing R framework, per Q14=B); currently silent on tiers.
- `docs/backlog.md` — the queue must be rebuilt from post-audit reality; its NOW section's top item is contradiction #6.
- `docs/research-roadmap.md` — priorities predate the audit; hedge-tournament ownership invalid; P0 is now instrumentation, not discovery.
- `rules-of-engagement.md` — keep structure and discipline clauses; strip TT3 allocation (§2/§8); blanks stay blanks per Q11=B but the drawdown-ladder mismatch with IC v8 gets resolved in the rewrite.
- `north-star.md` — personal anchor worth keeping; TT3-as-pillar line is contradiction #8. Andy's edit, not mine.
- `data/bots_meta.csv` — one-cell fix: HedgeD `strike_fix` Y→blank (contradiction #5); also `superseded=yes` review after tournament-rebuild decision.

**MERGE (4)**
- `docs/daily-brief-spec.md` + `docs/daily-review-design-2026-07-29.md` → **new `docs/daily-loop-spec.md`** (winner: the merged doc; the brief's render conventions survive, its compliance semantics are replaced by the three-verdict split + drift detector).
- `docs/oa-cleanup-runbook.md` → new `docs/oa-ops-runbook.md` (phases 1–3 are done; the group-probe result from 7/03 and the capture ritual + template-versioning procedure join it).
- `docs/audit.md` → new CLAUDE.md architecture section (local-first decision carries; the doc itself retires).
- `docs/versioning-prompt-2026-07-28.md` → its question is answered by OA's native template versioning (`approach-reset` §2.3); the answer merges into `oa-ops-runbook.md`, the prompt doc stays behind.

**KILL (stay behind — with justification)**
- *Cockpit/scalp lane (per Q7=A):* `docs/intraday-cockpit.md`, `docs/cockpit-upgrades-2026-07-08.md`, `docs/reversal-scalp-workstream.md`, `docs/reversal-fingerprint-probe.md`, `data/scalp_*.csv/md`, `data/paper_scalps.csv`, `data/goal_config.json`, `data/intraday/`, `data/scalp_journal.md`, `data/scalp_trading_contract.md`.
- *Adjudicated P3 / mostly-falsified:* `docs/pivot-vwap-research.md`, `docs/trigger-rules.md` (both explicitly deprioritized 2026-07-03; retrievable if the breach-engine revives).
- *Superseded planning:* `docs/cleanup-proposal.md` (this memo supersedes it), `docs/research-factory-decision.md` + `docs/discovery-loop-spec.md` (carry a one-line pointer only — both predate the instrumentation reset and the factory memo's premise is flagged falsified in `backlog.md` SOON; revisit after Phase 4).
- *Archive/narrative history:* `docs/session-log.md`, `docs/daily-ledger-archive.md` (the evidentiary record stays with the archive folder; new project starts fresh logs — old log referenced by pointer).
- *Stale/duplicative:* `docs/notion-guide.md` (Notion unreconciled since 6/07; decide Notion's role later), `Bot-Fleet-Overview.md` (Jun 8, pre-audit claims), `README.md` (write fresh), `dashboard.html` (regenerated artifact), `docs/current-state.md` (write fresh — the current one's body is frozen at 7/03 with a 7/28 banner grafted on), `STATUS.md` (regenerate from scripts after the corrections layer exists).
- *Do-not-distribute:* `investor-profile.md` (contradiction #11).
- *All of `docs/_archive/`* (already archived once; stays).

---

## DAILY VERIFICATION LOOP

Design principle (from `daily-review-design`): a data-collection ritual that produces a report as a byproduct; every day appends machine-readable rows; NO FINDINGS is the expected common case. Claude detects and **instructs**; Andy executes all OA edits (Q10). Note: while the OA account is inactive no bots run — until reactivation the loop runs in *config-drift-only* mode (steps 1, 6, 7 weekly).

**The loop (each trading day, ~17:30 ET):**

1. **Capture (Andy, ~2–5 min):** (a) bookmarklet on `/bots` — 35 bots × 18 fields, fixed schema; (b) OA positions **Export Data** (full history, ALL groups — the filtered-export guard already enforces this); (c) *only on days a config was edited:* bookmarklet capture of the edited automation trees + one screenshot for toggle states. Files land in the project folder.
2. **Ledger update (script):** `build_ledger.py` ingests the export; `tape.py` pulls Tradier daily + 5-min bars.
3. **Drift detection (script — `execution_audit.py`, the Phase-0 build):** per bot, against `bots_config` v2 (capture-derived, never memory-derived):
   - declared PT reached (`mfe_pct` ≥ threshold) but no PT-consistent exit → **Pattern A/B**
   - `mfe_date == close_date` fingerprint present/absent per side → **Pattern B**
   - close→open same minute, repeated → **orphan loop**
   - exit-price clustering at $1-ITM-style signatures → **Pattern C**
   - `|pnl| > risk` (impossible fill) → **the 6/11 class** (T00147 shows R = −1.63 in the raw ledger — one line of code)
   - entry-day % change vs declared filter band → **Pattern D**
   - per-bot expired:closed ratio flip vs its own baseline → **the Fortress regression signature**
   - identical P/L + identical entry minute across two bots → **duplicate-arm (S1≈D) signature**
   - `/bots` diff: AVG LOSS / P FACTOR / CLOSED deltas beyond bands → independent second surface (needs no ledger)
4. **Liveness check (script):** every ON bot must show either a position or a scanner run in the capture window. OA bot logs record non-actions (`oa-docs-research` N7) — zero log entries = presumed OFF/Failsafe-tripped → RED. This is the *only* way to close the PutVIX22 ambiguity.
5. **Three-verdict brief (script + Claude render):** per bot — *did it fire? / did mechanics execute? / right for the tape?* — never blended. Counterfactual ledger appends the two exact rows (hold-to-expiry from settle vs strikes; PT-would-have-fired from `mfe_pct`) per position, every day.
6. **Escalation (Claude → Andy):** any RED emits an *instruction card*: the exact OA screen, the exact edit, and the mandatory verification — **open the first new position after the fix and check its Trades list for the PT/exit-trigger rows** (the panel is not evidence). Fix unverified after 1 trading day → repeated at the top of every brief until closed.
7. **Prosecution section (Claude, always):** each ON bot's standing vs its pre-registered kill criterion, restated daily. Plus the free riders: morning ATM IV vs realized range (C1 live evidence), and the day's row into `counterfactual_ledger.csv`.

**Pass/fail per bot per day:** GREEN = liveness ✓ + zero drift flags + entries within declared filter/time. AMBER = flags explainable by tape (documented in the brief). RED = any drift flag, liveness failure, or unverified fix.

**Last-week failures this design catches same-day:** PT25 0/47 (step 3, position 1: expiry at `mfe 1.00` with declared PT25); Fortress 6/12 regression (step 3 ratio flip + step 4, session 1 of 6 — this alone was ~$9,700 across two days); the 7/01 orphan loop (step 3, same day — 10 same-minute round-trips); the 6/11 impossible fill (step 3, same day); HedgeD's $1-ITM clustering (step 3, within ~5 losses); S1≈D duplicate arms (step 3, day 1); PutVIX22's unverifiable health (step 4, day 1); call-side PT50 non-attachment (step 3 per-side fingerprint, first reachable opportunity).

**Not verifiable under OA's constraints, with workarounds:**
- *Toggle states* don't survive text capture → screenshot on edit days + weekly sweep; `/bots` all-dash pattern as a secondary hint.
- *Exit Options actually attached to a position* can't be confirmed before the first exit fires → post-edit first-position Trades-list check (step 6); optionally a Button test-fire.
- *A bot that trades rarely* (PutVIX22) emits no mechanic evidence for months → liveness via bot logs (step 4) covers ON-ness; mechanics stay UNVERIFIED until first fire — say so in the brief rather than assuming.
- *Sub-minute race detection* is invisible in exports (minute granularity) → same-minute flag triggers a manual order-level Trades-list pull.
- *Edits-persisting-while-inactive* → one-time DevTools network check (200 vs 402/403) before any build hours (reset doc Open Question 1).
- *Intra-day drift between captures* → not solvable; accepted residual, bounded to one day by construction.

---

## PER-BOT IMPROVEMENT SURFACE

"Evidence" column distinguishes **in-project evidence (act now)** from **needs-backtest (pre-register first)**. Compare by R throughout.

| Bot / pillar | Change | Evidence | Validating test | Priority |
|---|---|---|---|---|
| QQQ-Fortress + NoPT50 | **Restore PT50 + 15:50 exits; verify via Trades list on first new position** | In-project, CONFIRMED: dead exits caused −$9,618; restored config was +$2,975/+$2,760 pre-regression | First-position Trades list shows PT row + 15:50 exit-trigger row | **P0** |
| IC-SPX-FastPT25-S2 | **Scanner re-entry gate → `opened this side today`** (QQQ pattern) | In-project, CONFIRMED: 7/01 loop, 10 round-trips/29 min; HedgeB never loops with the correct gate; do NOT touch Cleanup (S2 depends on it — the live trap) | Capture the edited tree; next multi-entry day shows no same-minute churn | **P0** |
| IC-SPX-FastPT25-S2 + 130PM | **Cleanup pricing Market → SmartPricing** | In-project, CONFIRMED: the 6/14 fix missed Cleanup; mechanism of the $3,000 impossible fill; 130PM carries the same pair | Tree capture + no `|pnl|>risk` rows ever again | **P0** |
| IC-SPX-FastPT25-S2 | **PT25: attach-for-real vs drop (ride)** — decide by test, not restore-by-default | Mixed: tournament ride +7.3% vs SL75 +2.0% and Hindsight say exits too tight, BUT those measured the contaminated cohort; PT25 itself has zero runtime | Batch T1 (`ic-trailing-stop-backtest.md`): PT25 vs PT50 vs trail vs ride, OA Compare, judged on R; pre-register before restart | **P1** |
| IC pillar entries | **Scheduled-Event triggers replace scanner-retry entries** | In-project: champion's 38-min entry scatter = an unchosen strategy + A/B confound (`approach-reset` §2.2) | Entry-time distribution collapses to one minute in the ledger | **P1** |
| All restarted bots | **Bot Inputs parameterization, behavior-neutral; pilot on dead HedgeD; champion last** | In-project (reset §3.1–3.3); N6 caveat: input-link fallback is silent — capture must include the link chain | One week of unchanged ledger behavior post-refactor | **P1** |
| Hedge tournament | **Rebuild arms matched: shared automation + inputs, same execution class (Touch Exit Option if it = strike-touch), Range075 as preset** | In-project: current arms unmatched (S1≈D, S3 wrong class); Touch primitive documented | Arm configs differ only in one input value (capture-diff proof); then accrue | **P1** |
| QQQ-IC-0DTE-Baseline | **Forensic audit before any IC-growth conclusion** | −$31,580 = 38% of fleet loss, 3 max-loss events, never examined; could move aggregate expectancy either way | Fortress-style forensic: per-position strikes vs tape vs settle | **P1** |
| DIR-SPX-PutVIX22 / CallVIXdrop | **Verify toggles ON (liveness check); freeze params; accrue toward n≥100 / 6 mo** | In-project: OOS-passed both tracks; PutVIX22 health unverified; Put-Control proves the PT100 mechanic ($11.10 = modeled $11.10) | Adopted gates (B1–B3) + haircut/commission math before any live capital | **P1** |
| S2 hedge (champion) | **Re-examine S2's value once PT decision lands** — executes flawlessly, cost −$3,285 post-fix (sign held ex-6/09 but ~zero) | In-project; healthy ≠ profitable | Include S2-on vs S2-off arms in the T1/tournament rebuild | **P2** |
| IC growth (Andy's goal) | **Middle-band coverage (Batch M): wider-IC vs long-gamma on VIX 15–22 cohort** | Needs-backtest; coverage map sizes the gap at ~50% of days; three tools converged on trend-after-entry as the hole | Batch M per `directional-oa-build-sheet.md`: beat control + random-day null, then OOS | **P2** |
| OA-Mirror | **Formalize kills (Sandwich −0.412R, Weekly-IB, ORB); track Nigiri/3DTE vs funding bar — stamped THIN under new tiers (n=37/43)** | In-project R rankings | Funding bar + B-gates | **P2** |

---

## MIGRATION MANIFEST

**Carry** (copy verbatim): the 17-item CARRY list above + `data/` + `scripts/` + env files.
**Carry with rewrite**: the 8 REWRITE items.
**Leave behind**: everything in KILL (old folder = permanent archive; git remote `chace2827/bot-fleet` continues to back it up — note `.env` is not backed up, copy it by hand).
**Write fresh** (does not exist today):

1. `CLAUDE.md` — outline below.
2. `docs/current-state.md` — seeded from this memo's corrected truth.
3. `docs/daily-loop-spec.md` — the merged loop contract (design section above is the seed).
4. `docs/evidence-standards.md` — T1–T5 tiers + B/C sample-and-expectancy gates layered on the R methodology (Q2=B, Q14=B); every claim in the project carries a tier label from day 1. Open for Andy's redesign pass.
5. `docs/pre-registration-ledger.md` — template (hypothesis · kill criterion · sample target · review date · config-capture hash) + one entry per bot before it restarts.
6. `data/bots_config_v2.csv` — regenerated from bookmarklet captures + screenshots, never from memory; each row cites its capture file.
7. `data/corrections.csv` — the artifact layer (A1–A3 + strike-bug flags) with provenance, so `report.py` renders raw *and* economic views instead of a hand-edited headline.
8. `scripts/execution_audit.py` — Phase 0 of the reset doc; validated against the 35-row labelled set.
9. `docs/oa-ops-runbook.md` — capture ritual, template versioning, group scheme, edit-verification procedure (merge target).
10. `README.md` — one paragraph.

**New `CLAUDE.md` outline** (target < 6 KB — half the current size):

1. **What this project is** — 4 pillars, IC as focus; explicitly out of scope: TT3, Intraday Cockpit, discretionary scalping (pointer to old folder).
2. **⚡ Trigger: daily loop** — capture → `daily.sh` (ledger → tape → drift audit → three-verdict brief) → render → instruction cards for any RED → append logs. One paragraph, points at `daily-loop-spec.md`.
3. **Source-of-truth hierarchy** — `trades.csv` + `corrections.csv` → `STATUS.md` (numbers); capture files → `bots_config_v2.csv` (config; never hand-written); **Trades list > Exit Options panel**; forensics = sanctioned correction layer; narrative docs never carry numbers.
4. **Evidence law** — tier every claim T1–T5; nothing below T2 with n≥100/6mo/regime-change supports a live-capital or growth decision; R not raw P/L; pointer to `evidence-standards.md`.
5. **Discipline rules** — pre-register before restart; refactor-first (behavior-neutral) → then change values; pilot on dead bot, champion last; no changes during streaks; Claude instructs, Andy edits OA, every edit verified by first-position Trades list.
6. **File map** — ~15 entries, load-on-demand.
7. **Build lanes** — Cowork = strategy/ops/decisions; Claude Code = code/VPS; OA edits = Andy only.
8. **Archive pointer** — old folder path + what lives there (session-log, superseded research, Cockpit lane, full git history).
9. **Communication & session continuity** — Andy: direct, answer-first; **mandatory**: update `current-state.md` + append `session-log.md` after meaningful work (the 7/29 sessions skipped this — make it a hard rule).

**Exact commands (for review — not executed; read-only engagement):**
```bash
mkdir -p ~/bot-fleet-v2/{docs,data/raw,data/brief,scripts}
cd ~/bot-fleet
cp docs/approach-reset-2026-07-29.md docs/config-vs-reality-2026-07-28.md \
   docs/execution-audit-*.md docs/qqq-fortress-loss-forensic-2026-07-27.md \
   docs/independent-audit-2026-07-27*.md docs/oa-docs-research-2026-07-29.md \
   docs/oa-capture-*.md docs/daily-review-design-2026-07-29.md \
   docs/instrumentation-decision-2026-07-29.md docs/directional-oa-build-sheet.md \
   docs/strategy-taxonomy.md docs/backtest-ingest-protocol.md \
   docs/cross-functional-reference.md docs/oo-trial-backtests.md \
   docs/ic-trailing-stop-backtest.md docs/lean-backtesting-reference.md \
   docs/quantconnect-lean-exploration-brief.md docs/oa-mirror-reference.md \
   ~/bot-fleet-v2/docs/
cp data/trades.csv data/execution_audit.csv data/compliance.csv data/lessons.csv \
   data/bots_meta.csv data/bots_config.csv ~/bot-fleet-v2/data/
cp -R data/raw data/brief ~/bot-fleet-v2/data/
cp -R scripts ~/bot-fleet-v2/          # then path-review
cp .env .env.example ~/bot-fleet-v2/   # .env is NOT in the git backup — manual copy required
cd ~/bot-fleet-v2 && git init && git add -A && git commit -m "bot-fleet v2: curated import per rebuild-audit-2026-07-29"
# REWRITE items are copied then edited in v2; new files (CLAUDE.md etc.) written fresh in v2.
# Old folder: untouched. Later: new private repo or branch for v2 backup; launchd backup agent re-point.
```

---

## PHASED PLAN

**Phase 1 — Skeleton + corrected truth (single session — executable next session).**
First action: run the command block above (after Andy's review), then write `CLAUDE.md`, `docs/current-state.md`, `data/corrections.csv`, and the `bots_meta.csv` HedgeD fix in v2.
Completion test: a cold session in the new project, asked "what is actually true about the champion and the Fortress pair?", answers with the corrected figures (−$2,455 ex-artifact post-fix / +$2,975 pre-regression) without touching the old folder.
Unblocks: everything; ends the stale-narrative bleed.

**Phase 2 — Capture-derived config + platform checks (1–2 sessions, Andy in the loop).**
First action: the 10-minute **Export-Data bot-column check**, then full bookmarklet sweep of all bots + toggle screenshots → build `bots_config_v2.csv`; run the DevTools edit-persistence check.
Completion test: every ON bot's config row cites a capture file; zero rows sourced from memory; edit-persistence answered yes/no.
Unblocks: drift detection has a truthful comparator; versioning/inputs work is safe to schedule.

**Phase 3 — `execution_audit.py` + corrected reporting (~3–4 hrs, Claude Code lane).**
First action: build the detector set from first principles; validate against `execution_audit.csv` as a labelled test set (reproduce the ~20 ledger-detectable findings, stay silent on known-clean: champion entry logic, HedgeD's PT50, Bot-4 gating, S2 7/02).
Completion test: validation matrix passes; `daily.sh` runs end-to-end with the drift step; STATUS renders raw + economic views from `corrections.csv`.
Unblocks: the daily loop is real; reactivation becomes safe.

**Phase 4 — OA remediation + pre-registration (Andy executes, Claude instructs and verifies).**
First action: restore Fortress exits (P0 row 1) and verify via first-position Trades list; then champion scanner gate + Cleanup pricing; inputs pilot on HedgeD; write a pre-registration entry (hypothesis, kill criterion, sample target, review date) for every bot that will be ON.
Completion test: every ON bot GREEN on the drift report for 5 consecutive trading days after reactivation; every ON bot has a pre-registration entry dated before its restart.
Unblocks: the fleet can run and mean something; the continue-vs-shelve question starts accruing a real answer.

**Phase 5 — Growth research, gated (ongoing).**
First action: Batch T1 (exit mechanic) in OA Compare; then Baseline forensic; then tournament rebuild; then Batch M.
Completion test: each batch judged by R vs control per `backtest-ingest-protocol.md`; any go-live decision clears the adopted B/C gates.
Unblocks: the IC-growth goal — on evidence instead of momentum.

---

## OPEN QUESTIONS

1. **Export Data bot-name column** — 10 minutes; decides the capture architecture (Phase 2 first action).
2. **Do edits persist while the account is inactive?** DevTools check before any OA build hours.
3. **Does the Excessive Errors Failsafe explain the 6/12 Fortress regression?** Check the bots' error logs / ask OA support with position IDs — turns the scariest unknown into a monitorable known.
4. **Are PutVIX22 / CallVIXdrop automations toggled ON?** (CallVIXdrop was OFF at creation per `bots_meta`.) One screenshot each.
5. **Reactivation timing** — Phases 1–3 are account-independent; Phase 4 isn't. When?
6. **The 48 symbol-days of cached 5-min SPX/QQQ tape (5/29→7/02) were never committed to `data/brief/`** and Tradier's window is rolling — the early days are already unrecoverable via API. If any session still holds them, commit immediately; otherwise note the gap.
7. **QQQ-Fortress pair's roster status post-restoration** — pre-regression it was the fleet's only positive-Exp(R) n≥18 IC cohort (+2.9/+3.1%); does it re-enter as a pre-registered experiment?
8. **Notion's role in v2** — unreconciled since 6/07; propose: archive-only, reconcile quarterly or drop.
9. **Evidence-standards redesign** — Andy flagged wanting a possible new scoring system beyond tiers+gates; `evidence-standards.md` is written to be revised — schedule the redesign session.
10. **RoE numbers** — blanks stand (Q11=B) but Phase 4's pre-registration entries need at least a per-bot max-loss line; a placeholder convention is proposed in the template.
