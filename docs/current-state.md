# Current state — Bot Fleet v2

*Every figure below was re-verified against the v1 ledger on 2026-07-30 and reproduces exactly.*

> ## ⚠️ THIS PAGE DESCRIBES THE FROZEN v1 ERA
> As of the consolidation pass (2026-07-30), everything below is **history**. The v2 fleet does a
> **data cutover at Day-0 reactivation** (`LEDGER_START`) and an **OA-side clean slate**: ~20 legacy bots
> archived outright, 4 cloned-to-spec with their originals archived, 9 validated builds left untouched,
> 5–7 fresh builds. **Every active bot restarts at n=0.** None of the figures on this page describes a bot
> that will be running on Day-0.
>
> **Read this page to understand what went wrong and why the architecture is what it is.**
> **Do not read it for the state of the fleet** — after Day-0 that lives in `STATUS.md`.
>
> - The plan: **`docs/build-plan.md`** (under decision freeze).
> - Day-0 execution: **`docs/reactivation-runbook.md`**.
> - The frozen ledger and its one-page summary: **`data/archive/README-v1-ledger.md`**.
> - The source files moved: `trades.csv` and `corrections.csv` now live in `data/archive/`.
>   **As of Phase 3 so do `data/archive/raw/` (12 exports), `data/archive/brief/` (10 day files)
>   and `data/archive/lessons-v1.csv`.** `data/` now means post-cutover working data, no exceptions.

> ## ✅ PHASE 3 (part 1) IS CODE — 2026-07-30
> The cutover is no longer a plan. `build_ledger.py` carries `LEDGER_START`, **refuses to run
> without it**, filters on `open_date`, routes straddlers to `data/straddlers.csv`, and writes a
> run receipt to `data/ledger_meta.json`. `scripts/execution_audit.py` exists and passes **12/12**
> on its validation matrix. `daily.sh` is 8 stages (drift audit at stage 3) and degrades cleanly
> at n=0. `STATUS.md` still does not exist — `report.py` generates it on the first post-cutover
> run, now with the cutover date in a header banner and an explicit n=0 section.
> **Day-0 action: set `LEDGER_START` in `build_ledger.py` before anything else.**

*This doc is a pointer to the archived CSVs, not an independent record. If it disagrees with them, they win.*

## Account status
OA subscription **INACTIVE**. May 18 charge failed → ~5-day grace → deactivated ~5/23 → May 31 paid →
Jun 30 failed → inactive now. Andy reactivates **~mid-Aug**.
**No new entries since 7/02** — but "frozen" means no new positions, not no activity. Existing multi-day
positions continued to **resolve** through platform-level expiration processing: **6 mirror closes running
through 7/27** (+$632, absent from the archived `trades.csv` because they landed after its last ingest),
and **5 mirror positions still open** at the 2026-07-30 capture — `QQQ long call` ×4 (~$13K risk,
~−$10.8K unrealized) and `Tasty Condor` ×1 (~+$328). Every 0DTE bot is immune to this by construction;
only the multi-day mirrors straddle. Per the straddle rule (`build-plan.md` §3), all of these resolve into
the **mirror baseline layer**, never the working ledger — a position's era is its **open** date.
Edits made while inactive **do persist** (verified empirically 7/29→7/30) — building ahead is safe.

## Fleet
| | |
|---|---|
| Raw P/L (1,380 ledger rows = **934 positions**) | **−$83,130** |
| Cash-real total (only A1 never happened economically) | **−$80,130** |
| **Strategy-evidence total** (ex A1–A3 — the memo's "economic" figure) | **−$70,512** |
| Of which sits in the 15 still-flagged strike-bug / mis-built QQQ bots | **−$64,621 raw** → signal ≈ nil |

**Read the second and third rows carefully — they are not the same claim.** Only **A1 ($3,000)** never
happened economically. **A2/A3 (−$9,618) were real cash**; they are excluded from the −$70,512 because they
are *execution* evidence, not *strategy* evidence. Quote −$70,512 as "strategy-evidence P/L", never as
"what Andy actually lost" — that number is −$80,130. Note also that the memo's headline of "−$79,997 across
16 bots" was computed **before** HedgeD's contamination flag was removed; it double-counts HedgeD's
−$15,376, which is valid evidence. Post-correction the cohort is **15 bots / −$64,621**
(−64,621 + −15,376 = −79,997). See `data/corrections.csv` C1/C2.

The headline is dominated by artifacts and a contaminated cohort. Root-cause attribution across the audited
slice (35 losing positions, `data/execution_audit.csv`): settings 23 · by_design 9 · oa_execution 3
(66% / 26% / 9% — rounded, sums to 101%). **Only A1 ($3,000) never happened economically.** A2/A3 (−$9,618) were real cash but are
*execution* evidence, not *strategy* evidence. Genuine cleanly-attributed strategy losses are a small minority
— which is exactly why "continue vs shelve" was unanswerable from this data.

## The champion — `IC-SPX-FastPT25-S2`
- All-time **−$11,155 raw** / 364 legs. Pre-fix epoch −$5,700 (192 condors). Post-fix epoch (from 2026-06-08,
  the only window the declared entry config governed): **−$5,455 raw over 29 condors → −$2,455 ex-A1,
  Exp(R) −1.7%**. n=29 is **THIN** under the adopted gates — meaningless in either direction.
- **The strategy that ran was ride+S2, not PT25+S2.** PT25 generated 0 orders across 47 post-fix positions.
  The go-live gate that "cleared 18/15" certified a strategy nobody chose. G5 compliance scored 100% on five
  consecutive graded days while PT25 never fired once — it was scoring fidelity to a false record.
- **PT25 was not misbuilt.** Pre-lapse (**Apr 9 – May 22** — the champion's first ledger row is 2026-04-09;
  the "Mar 5" in the memo and kickoff is the *fleet's* first row, `QQQ-IC-0DTE-Baseline`): **306 legs, 306
  closed, 0 expired.** 119 of those legs closed capturing **25–35% of credit** — the PT25 target rounded onto
  the $0.05 tick grid, with 82 filling a nickel better than target; only **37** closed at literally
  0.75 × credit. So "~119 closes at the *exact* PT25 price" overstates it: the conclusion (PT25 fired
  routinely) holds, the word "exact" does not. It worked, then the billing lapse killed it.
  Caveat: that pre-lapse record is exit-clean but **entry-contaminated** (positions opened ~9:xx; the
  11:00/Range075 config only governed from 6/08).
- **"Pre-fix" and "pre-lapse" are different windows — do not use them interchangeably.**
  Pre-fix = before 2026-06-08 (the config epoch boundary in `bots_meta.csv`) = 317 legs / 192 condors / −$5,700.
  Pre-lapse = before 2026-06-01 (when the exit engine died; the A4 quarantine boundary) = 306 legs, all closed.
  The 11 legs / 6 condors / **−$2,000** between them (6/01–6/07) are labelled `pre-fix` in `trades.csv` but sit
  **inside** the A4 exit-off quarantine. Of those 11 legs, **6 expired and 5 closed** — the 6/04 condor closed
  fully at −$1,600 via S2, as did the 6/05 condor at −$1,800, plus one put leg on 6/03.
  **The signature is not "everything expired" — it is winners expiring at `mfe_pct` 1.00.** The three
  profitable condors (6/01, 6/02, 6/03) each reached full profit and expired instead of taking it, because
  PT25 was dead; the losers still closed, because S2 is a monitor and monitors survived the lapse.
  That split — dead Exit Options, live automations — is the whole diagnostic.
  **The "pre-fix epoch" figure is therefore NOT exit-clean**, even though the pre-lapse figure is.
- **The full declared combo — 11:00 + Range075 + PT25 + S2 — has never run as a whole. Its clean sample is zero.**
- **DECIDED**: the dead PT25 is formally **REMOVED**. `ride+S2` is the champion's official, pre-registered
  config — 29 post-fix condors of exactly that behavior, so the baseline continues unbroken. PT-variant
  questions belong to the greenfield arms, which are built matched for that purpose.
- S2 hedge: executes flawlessly, but **healthy ≠ profitable**. Post-fix S2 net **−$3,285**. The 7/02
  "S2 fired and helped" claim is **FALSE** — SPX settled 7483.24 vs the 7445 short put; holding was +$350,
  S2 cost $2,300. The error was misreading OA's "PRICE AT CLOSE" (a 13:02 exit print, not settle).

## The Fortress pair — `QQQ-IC-0DTE-Fortress` / `-NoPT50`
- Stated as −$1,834 / −$2,049 losers needing a put-side stop. **Both figures are wrong as strategy evidence.**
- **Fortress: +$2,975 strategy-attributable** (pre-6/12, 21 condors, **Exp(R) +2.9%**).
  **NoPT50: +$2,760** (18 condors, **+3.1%**).
- Their June losses (−$4,809 each, 11 legs each, 6/12–6/26) are a **dead-exit execution artifact**: zero exit
  orders were generated. The "naked tail that needs a stop" was a broken bot. Restored, June flips
  −$4,809 → +$3,227. The decision is **restore & verify, then re-ask** — not "add a stop".
- Pre-regression this pair was **the fleet's only positive-Exp(R), n≥18 IC cohort.** It is the IC history
  worth preserving. Restore **in place** — never by cloning.
- **The 6/12 regression is now encoded as an epoch boundary** — `bots_meta.csv` `epoch_boundary = 2026-06-12`
  on both bots (Andy approved 2026-07-30). Before this, all 41 Fortress and 35 NoPT50 rows carried
  `epoch=baseline` with a blank boundary, so any script grouping by `epoch` pooled +$2,975 with −$4,809 and
  regenerated **−$1,834** — the exact misleading headline this project exists to correct.
  ~~Residual: the `epoch` column in `trades.csv` is still `baseline` on all 76 rows. The boundary is
  declarative in `bots_meta` until `build_ledger.py` is taught to apply it (Phase 3).~~
  **CORRECTION 2026-07-30 (Phase 3): `build_ledger.py` already applied `epoch_boundary`** — it always
  has. The stale artefact was the *old* `trades.csv`, built before Andy set the cell, not the code.
  A rebuild splits the pair correctly: **Fortress pre-fix +$2,975 / post-fix −$4,809**, NoPT50
  **+$2,760 / −$4,809**. No code change was needed and none was made.
- **⚠️ UNRESOLVED — both Fortress bots still carry `strike_fix=Y`**, which places them inside the
  "decision-grade signal ≈ nil" cohort (see §Fleet) while Arm C of `build-plan.md` rests entirely on their
  +2.9% / +3.1% record. Only HedgeD's flag was adjudicated (0/86 malformed). **Nobody has checked the
  Fortress pair's strikes against the tape.** Until someone does, the pair's numbers and the cohort flag
  contradict each other and the folder does not say which wins. Queued as a Phase 2 verification.

## Other bots
- **`QQQ-IC-0DTE-Baseline` −$31,580 (38% of the entire fleet loss): NEVER AUDITED.** Largest unknown in the
  fleet. A Fortress-style forensic is required before any IC-growth conclusion. It could move aggregate
  expectancy either way.
- **`QQQ-HedgeD-Conditional` −$15,376 is real and its contamination flag was wrong** — 0 of 86 strikes are
  malformed. It tested an **immediate $1-ITM stop**, not a "Conditional" hedge: OA cannot express time
  persistence at all, so the mechanic as documented in the old platform reference is unbuildable.
  `bots_meta.csv` `strike_fix` corrected Y→blank 2026-07-30.
- **The hedge tournament cannot select anything.** S1≈D produced identical P/L on 73 of 86 days; S3 is a
  different execution class; no arm carries Range075. INVALIDATED pending rebuilt, matched arms.
  **Widened 2026-07-30 by the Phase-3 detector: there were THREE identical arms, not two.**
  `QQQ-IC-0DTE-HedgeTest` matches HedgeA-S1 on **73** positions and HedgeD on **70** — the same
  identity class. (`DUPLICATE_ARM`, reproduced independently from the ledger.) The detector also
  flags `IC-SPX-Fortress-Defang` ≈ `-Unstopped` on 10 positions and the QQQ Fortress pair on 14:
  small, but those A/B arms are less independent than their names imply. Recorded, not re-litigated
  — all of these bots are in the archive-directly group.
- **Directional**: put (+6.4% RoR OOS) and call (+21.9%) both OOS-passed; params frozen.
  `DIR-SPX-PutVIX22-SL75` took 0 positions in 22 days — VIX never reached 22, so **the gate is correct and
  the bot's health is unverifiable** from the evidence it emitted. Correctly-gated and switched-off look
  identical. Only the liveness check (bot logs) closes this.
  `DIR-SPX-Put-Control`: **default is NOT restarted** — its gate-proof function is already served by the
  OOS control backtest. Confirm at Phase 4 pre-registration.

## The lapse mechanism (SOLVED 2026-07-30)
Deactivation turns off automations **and** Exit Options. On resubscribe, **automations resume but Exit
Options on pre-lapse bots do NOT re-arm.** **Mechanism, answered by OA support 2026-07-30:** each bot's
dashboard carries a per-bot **`EXIT OPTIONS` ON/OFF toggle** at the top right, beside `AUTOMATIONS`. That
toggle is the hidden state — it stayed OFF while `AUTOMATIONS` came back ON. It is **visible only on the
dashboard, never in the editor**, which keeps displaying every setting as configured. One toggle kills PT,
Touch and time exit together. Andy has confirmed **both toggles are currently OFF on every bot.**
Proof: the champion's PT25 died June 1 (the first session back) while its 6/14 clone works 70/0; Fortress
used *bot-level* exits and died the same way. **Placement is not protection: one Exit Options engine, one
off state.** Bots built after May 31 are all fine; monitors were unaffected.
This is why the Day-0 runbook exists and why greenfield exits get a Scheduled-Event backstop in a different
execution class.

## Impossible fills — the detector rule is LOSS-SIDE ONLY
**The rule is `pnl < −risk`, not `|pnl| > risk`.** A loss larger than max loss is structurally impossible for
a defined-risk spread. A *gain* larger than the recorded risk is not: a long debit spread can return more
than its debit, and a high-credit iron condor can return more than its recorded risk. Flagging on absolute
value produces false positives on legal wins — `DIR-SPX-CallVIXdrop` T00038 (6/30, R +1.03, a
`longcallspread`) and `1-45pm-Sandwich-Paper-v1` T00339 (5/14, R +1.78, an `ironcondor`) are both clean
wins and must **not** be flagged.

Under the loss-side rule `trades.csv` contains exactly **two** rows:
- `IC-SPX-FastPT25-S2` **T00147** (6/11, −$7,740 on risk $4,740, **R = −1.63**) — this is A1, corrected.
  Mechanism diagnosed: Cleanup priced at Market.
- `QQQ-IC-0DTE-Raw-HoldToExp` **T00845** (3/31, −$200 on risk $181, **R = −1.10**) — logged as C4 and
  **deliberately left uncorrected**: immaterial in dollars, no diagnosed mechanism.

Phase 3 must reproduce **both**, and must stay silent on T00038 and T00339.
**DONE 2026-07-30** — `scripts/execution_audit.py --validate`, assertions V1–V4. V4 also proves
the choice is load-bearing: the `|pnl|>risk` rule would add **exactly** T00038 and T00339 and
nothing else.

**The rule runs per LEG, and that does not contradict `CLAUDE.md` §4.** §4 fixes the *position*
as the unit of **account** for expectancy; this is a *structural integrity* check on one vertical
spread's own max-loss guarantee, which is a per-spread property. Netted to the condor, T00147
still reads R −1.44 — but **T00845 reads R −0.99 and vanishes.**

**A second, independent detector finds T00147 with no risk column and no config.**
`FILL_WORSE_THAN_MAE` compares the exit against the worst price the position was ever *marked*
at: T00147 filled **$5.05/contract — 4.81 credits — outside its own recorded price path**. The
next worst of 1,232 closed rows is 0.91 credits. Two rules converging on one row, the second
corroborating the "Cleanup priced at Market" mechanism from the data alone.

## Known reconciliation gaps in the carried v1 docs
These were carried verbatim (CARRY files are not rewritten in Phase 1) and do **not** reconcile against
`data/trades.csv`. **The CSV wins.** Do not quote these figures:
- `independent-audit-2026-07-27.md` lines ~235/236/350 cite **6/17 = −$7,530**. The CSV shows the Fortress
  pair on 6/17 at −$7,946 and the fleet at −$7,901. Its 6/11 and 6/26 figures reconcile exactly, so this
  is a one-off bad number, not a convention difference.
- `execution-audit-ic-spx-fastpt25-s2-2026-07-27.md` line ~90 says "five of the ten closed at a loss;
  three had `mfe_pct 0.00`". The CSV — and the doc's own table 14 lines above — show **six** losers and
  **two** legs at `mfe_pct 0.00`.
- `approach-reset-2026-07-29.md` line ~227 says recoverable **+$11,944**; `execution-audit-ic...` line ~200
  says **+$11,922** for the identical counterfactual. $22 apart; immaterial, but do not average them.

## Reporting-stack defects found by the Phase-3 n=0 dry run (all fixed 2026-07-30)
The empty-ledger dry run was not a formality — it found four live defects, two of them destructive.

1. 🔴 **`lessons.py` silently truncated `data/lessons.csv` from 33 rows to 0.** It is a full
   rebuild, so a rebuild that finds no source lessons erases a populated index without a word.
   **On Day-1 this would have destroyed the v1 lessons index.** Fixed with a shrink guard
   (refuses to truncate a populated index to zero; `LESSONS_ALLOW_TRUNCATE=1` to override) and
   `data/archive/lessons-v1.csv`.
2. 🔴 **`daily_brief.py` was still reading `data/bots_config.csv`** — the discredited
   hand-written record, wrong on 3 of 4 audited bots — as the config input behind **every
   instruction-mirror compliance grade.** That is the "G5 scored 100% while PT25 never fired"
   mechanism, still wired in. Repointed to `bots_config_v2.csv`; absent that, it runs
   **CONFIG-BLIND and grades nothing**, loudly.
3. `daily_brief.py` crashed on any missing optional input. Optional inputs now degrade to empty.
4. `report.py` printed a hard-coded interpretive paragraph asserting facts about bot sizing
   above an empty table. Suppressed when its table is empty; `STATUS.md` gains a cutover banner
   and an explicit **EMPTY LEDGER — n=0** section.

## Known gaps
48 cached symbol-days of 5-min SPX/QQQ tape (5/29→7/02) were never committed to `data/brief/`; Tradier's
window is rolling and the early days are already unrecoverable. RoE figures remain blank by decision.
Notion has been unreconciled since 6/07 and its role in v2 is undecided.
