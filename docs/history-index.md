# History index — v1-era documents removed from the read path

*Created 2026-08-03 (folder cleanup, Block 1). Each doc below was carried into v2 in Phase 1
and has been removed from this folder. Every one has a verified copy in the permanent
read-only archive:*

**Archive root: `~/bot-fleet/docs/` — git remote `chace2827/bot-fleet`. Never modify it.**

**Standing rules:**
- Cite these as **history, never as the state of the fleet**. Any figure they carry is
  superseded by the frozen CSVs in `data/archive/` (start with `README-v1-ledger.md`).
- Every operating rule these docs produced already lives in a v2 doc — the citation is given
  per entry. If a rule seems missing from v2, check the named successor before opening the
  archive.
- 13 of the 16 were removed byte-identical to their archive copies (sha256-verified
  2026-08-03). Three differed **only by v2-added banners** (zero deletions, verified by diff);
  those banners are preserved verbatim in their entries below, because the archive copies do
  not carry them.

---

## The governing pair (migration-era)

**`rebuild-audit-2026-07-29.md`** — the consultant memo that governed the v1→v2 migration:
corrected loss figures, the twelve-contradiction register, the curated-copy manifest, and the
seven-step daily verification loop. Successors: the loop → `daily-loop-spec.md`; the P0/P1
per-bot fixes → `build-plan.md` §2B; the capture workarounds → `oa-ops-runbook.md`.
*Preserved from its not-verifiable register (the one item with no other v2 home):* **intra-day
drift between captures is not solvable and is an accepted residual, bounded to one day by
construction.**
⚠️ Reconciliation note: its migration manifest and doc-triage buckets describe a move that has
already happened — do not re-execute them.

**`phase1-kickoff-2026-07-30.md`** — the locked decision register for the rebuild, the corrected
v1 truth, and the billing-lapse mechanism (deactivation kills automations *and* Exit Options;
resubscription silently restores only automations). Successors: decisions → `build-plan.md`
(frozen); lapse mechanism + Day-0 consequences → `reactivation-runbook.md` §1 and
`oa-platform-reference.md` §10; champion control-arm exception → `CLAUDE.md` §5.
Where this doc and the rebuild-audit disagreed, **this one won** (it is later and records
decisions Andy confirmed after the memo) — all such conflicts are now settled in
`build-plan.md`; the known instance (champion PT25 removed, not open) is `build-plan.md` §2B.

## The forensics / correction layer (7/27–29)

**`config-vs-reality-2026-07-28.md`** — established that 3 of 4 audited v1 bots ran something
materially different from their hand-written config record, and that the correct scanner
re-entry gate is the per-day "opened this side today" flag. Successors: re-entry gate →
`build-plan.md` §2B champion clone spec; config-from-capture-only → `CLAUDE.md` §3.2.

**`qqq-fortress-loss-forensic-2026-07-27.md`** — established that the Fortress pair's June
losses were a dead-exit execution artifact, not a strategy property, and that **the position's
Trades list — never the Exit Options panel — is the only evidence a position is protected**.
Successors: panel-is-not-evidence → `CLAUDE.md` §3.3, `oa-platform-reference.md` §0.3;
expired:closed ratio flip detector → `daily-loop-spec.md` §5.

**`execution-audit-ic-spx-fastpt25-s2-2026-07-27.md`** — established that the champion never ran
its declared PT25+S2 (it ran ride+S2; PT25 generated zero orders across 47 post-fix positions),
named the 7/01 orphan loop, the Cleanup live trap, and the 6/11 impossible fill. Successors:
A–E forensic schema → encoded in `data/execution_audit.csv` + `scripts/execution_audit.py`;
do-not-touch-Cleanup → `build-plan.md` §2B.
⚠️ Known bad figure (from the v2 reconciliation pass): its line ~90 says "five of the ten closed
at a loss; three had mfe_pct 0.00" — the CSV and its own table show **six** losers and **two**
legs at 0.00. Its +$11,922 counterfactual vs approach-reset's +$11,944: $22 apart, immaterial,
do not average them.

**`execution-audit-qqq-hedged-conditional-2026-07-28.md`** — established that HedgeD tested an
immediate $1-ITM stop, not a "Conditional" hedge (OA cannot express time persistence), and that
the v1 hedge tournament cannot select anything (duplicate arms, mixed execution classes, no
Range075). Successors: valid-arm definition → `hedge-research.md` §5.2; duplicate-arm detector →
`daily-loop-spec.md` §5; Conditional correction → `oa-platform-reference.md` §11.

**`execution-audit-qqq-range075-pt50-wide2-1230pm-2026-07-27.md`** — established half-attached
profit targets as a failure mode detectable per side (the `mfe_date == close_date` fingerprint),
and the rule that a breach-free sample cannot price breach insurance. Successors: per-side PT
fingerprint → `daily-loop-spec.md` §5 detector set.

**`execution-audit-dir-spx-putvix22-sl75-2026-07-27.md`** — established that a correctly-gated
bot and a switched-off bot emit identical evidence when the gate never fires — the origin of the
liveness check. Successors: liveness rule → `daily-loop-spec.md` §5 (`SILENT_BOT`),
`oa-platform-reference.md` §4.4, `reactivation-runbook.md` §4 Step 8.

## The audits and superseded plans

**`independent-audit-2026-07-27.md`** — the external adversarial audit: evidence machinery
(adopted) plus a 9/100 confidence verdict, kill-IC and custody-separation recommendations
(overruled/declined). Successor for everything adopted: `evidence-standards.md` (§1 records
what was overruled and why).
⚠️ Known bad figure: its lines ~235/236/350 cite 6/17 = −$7,530; the CSV shows the Fortress pair
at −$7,946 and the fleet at −$7,901 that day. One-off bad number — its 6/11 and 6/26 figures
reconcile exactly.
*Preserved v2 banner (the archive copy does not carry it):* "⚠️ PARTIALLY OVERRULED — carried
for its evidence machinery only: the T1–T5 tiers and the sample gates. Its verdicts are
overruled: kill-IC; §5.5 items 6–7 (custody separation, independent go-live authority)
DECLINED; the Fortress auto-kill overruled; the 94%-vs-36% argument not decision-grade.
Corrected 2026-07-31: 'third-party-switch' meant the go-live switch held by a third party, not
a platform change. The CSVs win."

**`independent-audit-2026-07-27-precommitment-ledger.md`** — the locked pre-results criteria
(tiers A, gates B–H, rubric I, automatic kills J, worth-zero K). Successor:
`evidence-standards.md` carries the full A–K text (verified line-by-line 2026-08-03, including
B3's VIX definition and the locking clause). The archive copy remains the locked original — a
redesign that loosens a gate must say so against it.
*Preserved v2 banner:* "⚠️ Carried for machinery, not verdicts. Tiers and sample gates adopted;
kill-IC and custody-separation / independent-go-live-authority overruled/declined. Gate T3 —
the 'separate, weaker gate' §B1 promises and never defines — is now DEFINED in
`evidence-standards.md` §4.5 (Andy, 2026-07-31)."

**`approach-reset-2026-07-29.md`** — the diagnosis of why the v1 method failed (five drift
patterns; "nothing compares what a bot does to what we believe it does") and the original
remediation plan. Successors: discipline rules → `CLAUDE.md` §5; plan → `build-plan.md`
(which supersedes its Parts 3 and 5); drift-detector table → `scripts/execution_audit.py`.
⚠️ Known bad figure: its line ~227 says recoverable +$11,944 (see execution-audit-ic entry).
*Preserved v2 banner:* "⚠️ DEMOTED — authoritative as diagnosis, superseded as a plan. Its
Part 3 and Part 5 are replaced by `docs/build-plan.md`. Do not execute a plan from this file."

**`instrumentation-decision-2026-07-29.md`** — the decision memo that scoped instrumentation to
~5 hours (Phase 0+1), on the argument that negative expectancy measured on mis-built bots
cannot distinguish edge failure from execution artifact. The decision was made; the standing
self-warning ("instrumentation can be a sophisticated way of not deciding") is quoted here so
it survives: build measurement only in service of a decision someone has committed to make.

## Superseded loop / capture design docs

**`daily-review-design-2026-07-29.md`** — proposed the daily review as a data-collection ritual:
the three-verdict split, the fixed counterfactual panel, the prosecution section, NO FINDINGS as
the expected case. Fully superseded by `daily-loop-spec.md` (its header says so).

**`oa-capture-bookmarklet-2026-07-28.md`** — established the OA Grab bookmarklet and the finding
that Ctrl+S re-fetches from the server and captures nothing. Fully superseded by
`oa-ops-runbook.md` §1 (which carries the bookmarklet source itself).

**`oa-capture-coverage-2026-07-29.md`** — page-by-page capture-fidelity assessment: the 18-field
`/bots` schema, the do-not-bookmarklet verdict on `/positions/analyze`, the precision limits.
Fully superseded by `oa-ops-runbook.md` §1.5.

**`oa-docs-research-2026-07-29.md`** — the docs.optionalpha.com sweep that established OA has no
time-persistence primitive and named the eight platform primitives. Subsumed by
`oa-platform-reference.md` (the v2 rewrite). ⚠️ Its V1–V24 verification appendix — per-claim
DOCUMENTED / DOCS-SILENT / DOCS-CONFLICT verdicts with source paths — was **not** carried
forward anywhere and lives only in the archive copy; consult it when a platform-reference claim
needs its original source.

---

## Reading the v1 era — standing warnings

*(Moved here 2026-08-03 when `docs/current-state.md` was retired in cleanup Block 2. Its full
v1-era analysis is preserved in this repo's git history — last full version at commit `298d7a3`'s
parent — and summarized in `data/archive/README-v1-ledger.md`. The live facts it carried now live
in `docs/state.md`.)*

- **"Pre-fix" ≠ "pre-lapse" — never use them interchangeably.** Pre-fix = before 2026-06-08 (the
  champion's config epoch boundary in `bots_meta.csv`). Pre-lapse = before 2026-06-01 (when the exit
  engine died; the A4 quarantine boundary). The 6/01–6/07 gap is labelled `pre-fix` in the archived
  `trades.csv` but sits **inside** the exit-off quarantine — so pre-fix figures are **not**
  exit-clean, even though pre-lapse figures are. The lapse signature is winners expiring at
  `mfe_pct 1.00` while losers still close (dead Exit Options, live monitors).
- **Any condor Exp(R) computed before 2026-07-31 used the summed-sides denominator** and is the
  flattered number (`evidence-standards.md` §6.2; receipt `data/receipts/r-denominator-fix.txt`).
  Restate or drop.
- **The archived ledger is missing 6 mirror positions (+$632)** that closed after its last ingest —
  which is why `data/mirror_baseline.csv` must be built from
  `data/captures/oa_export_positions_2026-07-30.csv`, never from the archived `trades.csv`
  (`capture-architecture-2026-07-30.md`).
