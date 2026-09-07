# WAVE 2 — four Devin lanes (T-31 T-51 T-52 T-54) — run after wave 1's t45/t46/t43 merge
Rulings: R-2026-09-07-RECONCILER-IN · -T-16-A7-ONLY · -DA-4-TIER-COLLISIONS-RENAMED ·
-DA-10-INSTANCE-PROFITABILITY-REPORT-ONLY. Same foreman machine as wave 1 (`~/waves/2026-09-08/`
scripts, copied to `~/waves/2026-09-10/`); same cost law; free only before 09-16.

⛔ Lessons from wave 1 baked in: (1) origin/master MUST equal local master before clones are cut;
(2) premises below are located BY GREP, never by line number — each lane runs its grep first and
STOPs if zero or >1 match; (3) never instruct a wrapper config file; (4) check whether the task is
already done before doing it.

Common pre-flight / acceptance / PR contract: identical to `_wave-2026-09-08-lanes.md` header.
Merge order: t31 → t51 (both add close.sh stages; t51 after t31 so stage numbering is stable);
t52 and t54 independent.

---
## Lane 1 · T-31 — Reconciler as a read-only close.sh stage (P1 bet input)
Locate: `grep -n '== [0-9]/5' scripts/close.sh` (five stages today; t46 may have changed the
capture path — read the merged close.sh, not the spec's memory). `grep -n 'def ' scripts/capture_bundle.py`.
Build `scripts/reconcile.py --root R --day D`: inputs = the day's `/bots` roster capture text (as
capture_bundle placed it), the day's raw export (`data/raw/<D>.csv`), `data/trades.csv`,
`data/bots_meta.csv`. Per bot, three sources reconciled: (a) roster: exists / AUTOS / EXITS /
open-position count; (b) export: closed rows for D and open rows; (c) ledger: rows with
close_date D. Output `data/close/<D>/reconcile.tsv`: bot · field · roster · export · ledger ·
agree(y/n) · source-per-cell. Any y/n=n → exit non-zero → close RED ("stage 6/6 reconcile").
Expected disagreements that are NOT findings must be encoded as rules, not ignored: ops-class
bots (bots_meta `ops_class`), bots absent from the roster capture because archived (rename_map),
pre-cutover-only bots. Discrepancy count printed and written to the manifest (coordinate with
t46's manifest shape — read the merged close_manifest.py).
Red test: fixture where the roster says AUTOS ON for a bot the export shows no rows for on a
fill day AND the ledger shows a row → disagreement → non-zero. Green: 09-04 real files agree.
Prototype to reuse: the per-row signature diff in `data/captures/2026-09-07-catchup/01-drift-verdict-2026-09-07.md`.

## Lane 2 · T-51 — a_series.py assert A7 as a read-only close.sh stage
Locate: `grep -n 'def a7_hashes\|WIRING_SNIPPET\|--emit-wiring' scripts/a_series.py`;
`grep -n 'a7_hash\|shared_automation' data/bots_config_v2.csv | head`. Read the WIRING_SNIPPET the
script already carries (`python3 scripts/a_series.py --emit-wiring`) — that is the intended
wiring; use it, do not invent another. A7 compares each shared automation's adopted payload hash
(from the day's capture) to the CSV baseline. ⚠️ The baselines moved 2026-09-02 (ScannerA
`2c4a96c5…`, ScannerB `a1a48af1…` — see `docs/pre-registration-ledger.md` CONFIG HASH RE-STAMPED
lines and `data/captures/2026-09-02-gf-sizing/04-shared-qty-*.md`). Check whether
`data/bots_config_v2.csv` a7_hash rows were re-baselined; if not, the FIRST run must go RED
against the stale baseline — that IS the red test — then re-baseline by appending a new A7
BASELINE line (the script's documented convention: original left standing, superseded) citing
the 09-02 capture, and re-run green. Stage is read-only; a hash change on any later day = RED close
with the A7 DRIFT REPORT printed. Scope only what the daily capture contains: if the roster grab
does not carry automation payloads, say so and define the minimal additional read the Cowork
close must capture (a per-automation `{name,inputs,root}` JSON, the 09-02 method) — do not
pretend A7 can run on a surface it cannot see.

## Lane 3 · T-52 — rename the colliding "tier" vocabularies (spec only)
Locate: `grep -n -i 'tier' docs/daily-loop-spec.md | grep -v 'T[1-5]'` — every hit is one of:
detector Tier S/C → "detector class S/C"; counterfactual cost tiers → "cost band"; Build tiers
0–2 → "build level 0–2". Evidence tiers T1–T5 keep the word. Also grep `scripts/` for the same
identifiers in printed strings (`grep -rn 'Tier S\|Tier C\|cost tier\|Build tier' scripts/`) and
rename the printed label only, never a variable or a CSV column. Acceptance: the grep above
returns zero non-evidence "tier" uses; `daily.sh` dry path output unchanged except the labels;
one banner at the top of daily-loop-spec.md citing the ruling.

## Lane 4 · T-54 — instance-profitability column on the readiness board (report-only)
Locate: `grep -n 'Readiness board\|Exp(R) \[95% CI\]\|def .*readiness' scripts/report.py`.
Definition (evidence-standards.md §6.3, `grep -n 'Instance profitability' docs/evidence-standards.md`):
per bot, fraction of INSTANCES that are profitable, where an instance = one position (a condor =
its paired rows, CLAUDE.md §4 unit law) on one day. Add a column `inst% (n)` beside Exp(R) on both
readiness tables; `—` when n=0; NO gate effect, NO threshold, NO stage change. Red test: a fixture
ledger with 3 positions (+,+,−) → 67% (3); one with a paired condor counted once, not twice.
Update the gate legend line to say the column is report-only per the ruling.
