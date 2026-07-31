# v1 ledger — FROZEN 2026-07-30

**Nothing in this folder is a reporting input.** It is the pre-cutover evidentiary record, frozen
permanently. `build_ledger.py` must not read it. `STATUS.md` must not derive from it. No claim about the
live fleet may cite it.

## Why it is frozen
The v2 fleet does a **data cutover at Day-0 reactivation** (`LEDGER_START`). Every active bot on Day-0 is
either fresh-built, cloned-to-spec, or an untouched validated build. None of them carries meaningful
pre-cutover history, and the history that does exist was produced by configs that no longer run —
in several cases by an exit engine that was silently dead. Mixing the two eras is the specific failure the
v2 rebuild exists to end, so the working ledger simply starts empty.

## Contents
- `trades.csv` — 1,380 rows / 934 positions, 2026-03-05 → 2026-07-02. The complete v1 ledger.
- `corrections.csv` — the 8-row correction layer (A1–A4, C1–C4) that makes `trades.csv` readable.
  Frozen with the approved hygiene fixes applied: C4 narrowed to the loss-side rule, HedgeD's strike flag
  removed, the cohort figure corrected to 15 bots / −$64,621.
- `bots_config.csv` — the discredited hand-written config record. Wrong on 3 of 4 audited bots. Kept only
  as the historical artifact of *how* the record went wrong.
- `compliance.csv` — the v1 G5 compliance scores. Scored fidelity to `bots_config.csv`, so it certified
  100% on five consecutive days while the champion's PT25 never fired. Kept for the post-mortem.

## One-page summary of what the v1 ledger established
Numbers below are final; they were each recomputed from `trades.csv` and reproduce exactly.

**Fleet.** Raw −$83,130 across 1,380 rows / 934 positions. Cash-real −$80,130 (only A1's $3,000 never
happened economically). Strategy-evidence −$70,512 after excluding A1–A3. Of the raw total, −$64,621 sits
in the 15 bots still flagged `strike_fix=Y` — decision-grade signal from that cohort is approximately nil.

**The champion (`IC-SPX-FastPT25-S2`).** All-time −$11,155 raw. Post-fix epoch (from 2026-06-08):
29 condors, −$5,455 raw → **−$2,455 ex-A1, Exp(R) −1.7% per condor**. THIN under the adopted gates.
It ran **ride+S2, not PT25+S2** — PT25 generated zero exit orders across 47 post-fix positions.
PT25 was not misbuilt: pre-lapse (Apr 9 – May 22) it closed 306 of 306 legs with 0 expiries, 119 of them
capturing 25–35% of credit. The billing lapse killed it. **The full declared combo — 11:00 + Range075 +
PT25 + S2 — never ran as a whole; its clean sample is zero.** S2 executes flawlessly and still lost money:
post-fix net −$3,285. The 7/02 "S2 helped" claim is false — S2 cost $2,300 against a +$350 hold.

**The Fortress pair.** Pre-6/12: Fortress +$2,975 over 21 condors (**+2.9%**), NoPT50 +$2,760 over 18
(**+3.1%**) — the fleet's only positive-Exp(R), n≥18 IC cohort. Their June losses (−$4,809 each) were a
dead-exit execution artifact, not a strategy property: zero exit orders were generated from 6/12.
`epoch_boundary = 2026-06-12` records the break in `bots_meta.csv`.

**Unresolved at freeze, and now permanently so.** `QQQ-IC-0DTE-Baseline` (−$31,580, 38% of the fleet loss)
was never audited. The Fortress pair's `strike_fix=Y` flag was never adjudicated against the tape. Both
questions concern archived bots and pre-cutover data; neither gates anything in v2. The Baseline forensic
survives only as optional research.

**The lapse mechanism.** Each bot's dashboard carries a per-bot `EXIT OPTIONS` ON/OFF toggle beside
`AUTOMATIONS`. Deactivation turns both off; resubscription restores only `AUTOMATIONS`. The editor keeps
displaying every Exit Option setting regardless — the toggle is the only place the failure is visible.
One toggle kills PT, Touch and time exit together. This is why v2's flat-close backstop lives on the
automations side.
