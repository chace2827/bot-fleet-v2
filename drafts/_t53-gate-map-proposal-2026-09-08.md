# T-53 — PROPOSAL: mapping audit gates A–K onto board gates G1–G6

**Status: PROPOSAL. Nothing here is applied.** Drafted Claude Code 2026-09-08 under
`R-2026-09-07-DA-8-GATE-MAP-OUT-OF-SCOPE` (board item T-53, P7, lane CC).
Andy rules; §5 lists what needs a ruling and what is mechanical afterwards.

**The defect this closes** (`evidence-standards.md` §10 item 3, verbatim): *"a bot can be
LIVE-READY on the board while its pillar fails audit gate B, and nothing currently notices."*
**Clock:** T-36 — `IC-SPX-FastPT25-S2-130PM` at **n=19 clean condors as of 2026-09-04**
(`data/portfolio.csv` T-36 metric_note, read 2026-09-08), one condor short of board gate G2's ≥20.

**Naming discipline, per `evidence-standards.md` §3.** Every gate below is written with its system:
**audit gate** `A`…`K` (System I, per pillar/system) · **board gate** `G1`…`G6` (System II, per bot,
grain = condor). The collisions this document touches are listed in §4.3. Never a bare `G1`, `B1`,
`C1`, `C2`, `G2`, or `T3`.

---

## 0 · Was this already written? No.

Checked before drafting (wave-1 trap 3, "check whether the task is already done"):
`grep -rln "How the two systems meet\|gate map\|gate-map\|audit_gates" .` over the repo returns
**two files, both dispatches** — `drafts/_dispatch-2026-09-08-t53-gate-map-claudecode.md` and
`drafts/_dispatch-2026-09-09-t50-archive-sweep-cowork.md`. No `§5.1` exists in
`docs/evidence-standards.md` (`grep -n "^## \|^### "` → §5 is followed by §6). No `data/audit_gates.csv`
exists (`ls data/`). `grep -oE 'gate [A-K]' scripts/` returns nothing — **System I is implemented
nowhere in code**, as `evidence-standards-redesign-proposal-2026-08-08.md` §2.2 S-6 already records.

---

## 1 · The map

### 1.1 First: what audit family `A` is

`evidence-standards.md` §4 is titled *"the pre-commitment gates (A–K)"* and has no `### A` heading —
family A lives in **§2, the evidence tiers**. Confirmed against the locked original, read this
session: `~/bot-fleet/docs/independent-audit-2026-07-27-precommitment-ledger.md` line 8,
*"## A. EVIDENCE TIERS (a system is scored at its HIGHEST-QUALITY tier, never averaged up)"*.
`docs/history-index.md` says the same in one line: *"tiers A, gates B–H, rubric I, automatic kills
J, worth-zero K"*.

A has no numbered criteria. Its two testable obligations, named here for the table:

| | Obligation | Source |
|---|---|---|
| **A-tier** | Every claim about the bot carries an evidence tier T1–T5; the system is scored at its highest tier and never borrows credibility upward. | §2 |
| **A-cite** | A T4 result may never be cited as support for a T1/T2 claim; a backtest re-run after seeing its own output is T4 by definition. | §2, ledger §A |

Also not a gate, and excluded from the table's HOLD logic for that reason: **audit gate `I`** is a
0–100 **rubric**, not a pass/fail; **audit family `K`** is a list of things worth zero, i.e. a
prohibition on rationales, not a test of the bot. Both still appear as columns, because both bind.
The 22-gate count in §4 (*"1.5 of 22 gates passed"*) is B+C+D+E+F+G+H = 3+4+4+3+4+1+3 = 22 — I, J
and K are outside it. **Audit gate `T3`** (§4.5) is a separate weaker gate and gets its own row-note
in §1.5, not a column.

### 1.2 The table

Rows = board stage. Columns = audit gate family.
**`HOLD`** = must not be FAIL for the stage to be honest (PENDING is tolerated only where the cell
says so) · **`PENDING-OK`** = may be pending, **never FAIL** · **`N/A`** = not applicable at this
grain or with no cited artifact · **`—`** = out of scope for this row.

| Board stage | A | B | C | D | E | F | G | H | I | J | K |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **INCUBATE** (board passed=0) | HOLD | PENDING-OK | PENDING-OK | HOLD (D4) | HOLD (E1) | PENDING-OK | N/A | — | — | HOLD | HOLD |
| **VALIDATE** (passed=1–2) | HOLD | PENDING-OK | PENDING-OK | HOLD (D4) | HOLD (E1) | PENDING-OK | N/A | — | — | HOLD | HOLD |
| **CANDIDATE** (passed=3–4) | HOLD | PENDING-OK | HOLD (C4) | HOLD (D1, D4) | HOLD (E1) | **HOLD** | N/A\* | — | — | HOLD | HOLD |
| **LIVE-READY** (passed=5–6) | HOLD | **see §2 — the open question** | **HOLD** | **HOLD** | **HOLD** | **HOLD** | HOLD\* | **HOLD** | — | HOLD | HOLD |
| **LIVE** (real capital) | HOLD | **HOLD (B1+B2+B3)** | HOLD | HOLD | HOLD | HOLD | HOLD\* | HOLD | HOLD (band) | HOLD | HOLD |

\* audit gate `G` is `N/A` for any bot whose pre-registration cites no backtest; `HOLD` the moment
one is cited. It is the only cell whose value is per-bot rather than per-stage.

### 1.3 Rationale, one line per non-`—` cell

**A — HOLD at every stage** (§2, §2.1). Free to evaluate at n=0: it is a labelling obligation, not a
sample test. A bot advancing on a citation that violates A-cite is advancing on inadmissible
evidence whatever its board dots say.
**B — PENDING-OK through CANDIDATE** (§4 B1–B3). B is a sample gate; at INCUBATE/VALIDATE/CANDIDATE
the board's own gate G2 (≥20 clean condors) is the sample test at bot grain, and B is measuring a
different thing (pillar admissibility). **Its value at LIVE-READY is the one genuinely open
question — §2.** At LIVE it is HOLD in full; that is not new, it is `CLAUDE.md` §4 restated.
**C — PENDING-OK, then HOLD (C4) at CANDIDATE, full HOLD at LIVE-READY** (§4 C1–C4). C4 (*"edge
visible only in raw P/L but not in R = FAIL"*) is checkable at any n and is exactly the error that
makes a CANDIDATE call wrong. C1–C3 (after costs, ex-best-winner, worst-5%-degraded) need the
pillar's expectancy and belong at LIVE-READY, where the board has already asserted an edge via board
gate G3.
**D — HOLD (D4) from INCUBATE; add D1 at CANDIDATE; full at LIVE-READY** (§4 D1–D4). D4
(*"undefined-risk or naked exposure at any point = automatic kill"*) is structural and knowable on
day 1. D1 (*"max realized drawdown, in R, must be known and stated. Unknown = FAIL"*) is cheap once
a series exists; board gate G4 already computes maxDD-R, so D1 costs nothing. D2/D3 need the window.
**E — HOLD (E1) from INCUBATE, full HOLD at LIVE-READY** (§4 E1–E3). E1 (a named economic source in
one sentence) is already a precondition of the bot existing — pre-registration requires hypothesis
and mechanism before restart (`CLAUDE.md` §5; `evidence-standards.md` §8). E2 (mechanism consistent
with the observed P&L shape) needs a shape, so it lands at LIVE-READY.
**F — HOLD at CANDIDATE** (§4 F1–F4). CANDIDATE is the stage that names a winner, and F1 is the
multiple-comparisons haircut on exactly that act (|t| > √(2 ln N)). The GF family is seven arms plus
controls; N is known at design time, so F1 is evaluable now. F2 (re-tune → *"the sample count resets
with it"*) must bind before the count is trusted, not after. F3 (post-hoc subset) is the same act.
**G — N/A unless a backtest is cited; then HOLD** (§4 G1). Audit gate G1 is *live Exp(R) ≥ 50% of
backtested Exp(R)* — it has no meaning where no backtest was cited, and it is decisive where one was
(*"no backtest from it may be cited as evidence anywhere"*).
**H — HOLD at LIVE-READY** (§4 H1–H3). Fleet grain, and it bites precisely at the moment several
bots sit at LIVE-READY at once: H1 says that if every pillar is net-short-vol the fleet is *"ONE bet,
not four, and is scored as one system with one sample."* Five LIVE-READY IC bots are one bet, not
five. H3 (worst historical stress day at current size) has no number — `rules-of-engagement.md`
carries four `<FILL>` blanks (§10 item 4), so H3 is permanently pending until someone writes one.
**I — reported, never a board gate** (§4 I). The 0–100 rubric's own band language is about capital
(*51–70 → "Advance to live at reduced size"*), so its only HOLD row is LIVE. It is computed nowhere
today (redesign proposal §2.2 S-6); a HOLD on a number nothing produces would be a false gate.
**J — HOLD at every stage** (§4 J1–J5). By construction: *"any one of these ends the system, no
discussion."* J1 is the live-capital one; J2–J5 bind at any stage.
**K — HOLD at every stage** (§4 K). Read as a prohibition on rationales: nothing in the worth-zero
list (hours logged, bot count, doc quality, infrastructure, conviction) may appear as a reason a bot
advanced. Cheap, always evaluable, and the one that most resembles what this project actually does.

### 1.4 The grain mismatch, and how a bot inherits a pillar verdict

Audit gates A–K are **per system / pillar / fleet**; board gates G1–G6 are **per bot, grain =
condor** (§3 table). The map above therefore needs one join and one rule.

**The join.** A bot inherits its pillar's audit verdict. The pillar is read from
`data/bots_meta.csv`, column `pillar` — the same column `scripts/report.py` already uses for the
scorecard. Read this session: 31 bots pillar `IC` (every `IC-*` and every `GF-*` arm), 10
`OA-Mirror`, 3 `Directional`. **No new taxonomy is introduced and no bot is re-assigned.**

**Two families do not join on pillar:**
- **H** is fleet grain. Its verdict is carried once, under the scope name `FLEET`.
- **A** is per *claim*, not per bot. It is evaluated at the decision that cites the claim, not on
  the readiness board. It is in the table because it binds; it is not in the board rider of §3.

**Where the verdict is read from.** A new `data/audit_gates.csv` (schema in §3.2). **Written only by
ruling, never by code** — System I is adjudicated, not computed (§4: *"Binary, per system. The
ledger is the source of record"*), and nothing in `scripts/` computes it today.

**The absent-row rule, non-negotiable:** *a pillar with no row for a gate reads **pending**, never
**pass***. This is the G5 lesson applied before the fact (§5, ⛔ *"G5 IS THE GATE THAT LIED"*): a
pending gate is honest; a passing gate built on an absent record is not. An absent number is not a
zero and an absent verdict is not a pass.

### 1.5 What maps to nothing, in both directions — this asymmetry *is* the defect

**Board gates with no audit family:** board gate G1 (clean data — a data-integrity test the audit
never contemplated) and board gate G5 (instruction-mirror compliance — a v2 invention answering the
v1 drift failure). Both are additive; neither needs an audit counterpart.

**Audit families with no board gate: A, E, F, H, I, J, K — seven of eleven.** The board can only see
B-, C-, D- and G-shaped things (sample, expectancy, risk, tracking) because those are the four the
ledger can compute. Mechanism, overfitting, portfolio concentration, the kill list and the
worth-zero list are invisible to it by construction. **That is why "nothing notices" — not an
oversight in the board, but the board's grain.** The rider in §3 does not fix it; it makes it
visible.

**Audit gate T3** (§4.5, criteria T3.1–T3.6) is `N/A` on every board row. It authorizes *building*
an experiment, paper-running it, and setting its sizing tier — never live capital, and it does not
shorten B1 or the six-month clock (§4.5, ⛔ box). It is a precondition of a bot existing, which is
upstream of INCUBATE, not a stage gate. Note the collision it creates: a **evidence tier T3**
backtest that fails **audit gate T3** is still evidence tier T3 (redesign proposal §2.2 S-5).

---

## 2 · The n=0 problem — options, not a recommendation

### 2.1 The numbers, read this session

All from `data/trades.csv` (the post-cutover working ledger), read 2026-09-08. `LEDGER_START =
"2026-08-10"` — `scripts/build_ledger.py:158`.

| Figure | Value | Unit |
|---|---|---|
| Leg rows post-cutover | 246 | legs |
| Distinct positions post-cutover | 187 | positions |
| Earliest post-cutover `open_date` | **2026-08-10** | date |
| Latest `open_date` | 2026-09-04 | date |
| Span so far | 25 calendar days | days |
| **B2 satisfied on** | **2027-02-10** (2026-08-10 + 6 calendar months) | date |
| Closed/expired positions, pillar **IC** | **147** | positions |
| … of which paired condors | 59 | condors |
| Closed/expired positions, pillar **OA-Mirror** | 34 | positions |
| Closed/expired positions, pillar **Directional** | 6 | positions |
| Open (not closed or expired) positions | 0 | positions |

### 2.2 ⚠️ A finding that changes the shape of the question: **B1 is not the binding conjunct**

`evidence-standards.md` §10 item 5 says B1 (≥100 positions) and B2 (≥6 months) are *"unreachable for
roughly six months by construction."* **For B1 and the IC pillar, that premise is now stale.** B1
requires *n ≥ 100 closed positions at T1 or T2*; §4's own ⚠️ note settles the unit as **positions**,
not trades. The IC pillar holds **147 closed positions** post-cutover. Everything in the fleet runs
on OA Paper Trading, which `docs/state.md` line 334–336 settles as correct and expected (*"'live' in
this project means live-running on paper"*, *"NO LIVE CAPITAL UNTIL AT LEAST FEBRUARY"*) — i.e.
**evidence tier T2**, which B1 admits.

**Three reasons this is stated as a finding and not as "B1 passes":**
1. **T2 carries a conjunct nobody has ruled on** — *"automated paper execution **with realistic
   fills**"* (§2; §2.1 seam 1 records that the audit's wording drops "realistic fills" and the
   stricter reading was adopted). Whether OA paper fills clear it is unruled. [UNCLEAR]
2. **F2 may have already reset the count.** *"Parameters changed more than once per 30 trading days
   on average → RE-TUNED; the live record restarts at the last change and the sample count resets
   with it."* The GF arms were re-baselined 2026-09-02 (sizing). Whether F2 fires — and if so, from
   which date — is an audit-gate F question that has never been evaluated.
3. **Grain.** 147 is positions. At condor grain the IC pillar is **59 condors**. If a future ruling
   reads B1 at condor grain the answer flips. §4's note says positions; the board says condors; both
   are written down and they disagree in effect.

**Consequence for the options below: B2 (span → 2027-02-10) is the only conjunct that is
unreachable-by-construction today.** B3 (regime change) is separately special — it has no detector,
is *evaluated manually and logged*, and no such evaluation has been run (§4, ✅ RESOLVED 2026-08-06
banner; trigger = the earlier of any arm's n=60 interim read or 2026-11-30).

### 2.3 The three options

---

**OPTION (a) — audit gate B is HOLD at LIVE only. LIVE-READY carries a visible "audit B pending" flag.**

The board stage ladder is untouched. A bot reaching board passed=5 or 6 still prints `LIVE-READY`,
and prints alongside it `audit B pending — IC 147/100 positions, span 25/184 days`.

*Consequence for T-36:* none on the ladder. `IC-SPX-FastPT25-S2-130PM` clears board gate G2 at its
20th clean condor; if board gate G3's bootstrap CI lower bound also clears zero it advances exactly
as it does today, with the pending flag printed beside it. The G2/G3 review is not blocked and does
not need this ruling to land first.

*What it costs:* `LIVE-READY` keeps meaning "board-clean", which is what it means today and what §10
item 3 objects to. The defect is downgraded from silent to noisy, not removed. Whoever reads the
board must know that LIVE-READY ≠ admissible.

*Locking clause (§1):* not a loosening and not a tightening — it is today's behaviour plus a printed
flag. It is also the option most consistent with `R-2026-09-07-DA-7-N0-ADMISSIBILITY-CLARIFICATION`,
which declares that *"B1 (≥100 positions) and B2 (≥6 months) never gated build or sizing decisions"*
— they are audit gates on live capital. Under DA-7's reading, B at LIVE is where B already was.

---

**OPTION (b) — audit gate B is HOLD at LIVE-READY.**

A bot cannot print `LIVE-READY` while its pillar's B is FAIL or pending. Board passed=5–6 with B
unmet tops out at `CANDIDATE`.

*Consequence in dates, read from `data/trades.csv` this session:* the earliest post-cutover
`open_date` is **2026-08-10**, so B2 (span ≥ 6 calendar months of forward time) cannot be satisfied
before **2027-02-10**. B1 is at 147/100 closed positions for IC (§2.2) and 34 and 6 positions for
OA-Mirror and Directional respectively, so **B2 alone holds the date**. B3 additionally requires a
manual regime evaluation that has not been run. Under (b), **no bot in any pillar reaches LIVE-READY
before 2027-02-10**, regardless of its own record — and OA-Mirror and Directional not even then, on
their current position counts.

*Consequence for T-36:* `IC-SPX-FastPT25-S2-130PM` clearing board gates G2 and G3 would be reported
as `CANDIDATE`, not `LIVE-READY`. **The T-36 review itself is unaffected** — its question is whether
G2 and G3 clear, and both still compute — but the stage word printed beside it changes, and it
changes for `IC-SPX-FastPT25-S2` and the GF arms at the same time.

*What it buys:* `LIVE-READY` would mean what it says. Note the coincidence worth weighing: 2027-02-10
and `state.md` line 336's *"NO LIVE CAPITAL UNTIL AT LEAST FEBRUARY"* are the same month, so under
(b) the board word and the capital plan agree by construction rather than by anyone remembering to
check.

*Locking clause (§1):* **this is a tightening and must be flagged as one.** Today a bot can reach
LIVE-READY on board gates alone; (b) removes that. §1's locking clause permits making a threshold
stricter and requires saying so out loud — this paragraph is that flag.

---

**OPTION (c) — split B: B3 `PENDING-OK` everywhere, B1 and B2 `HOLD` at LIVE.**

Same ladder behaviour as (a) — nothing blocks below LIVE — but the flag names the missing conjunct
rather than the family: `audit B2 pending — span 25/184 days` rather than `audit B pending`.

*Rationale for the split:* B3 has no detector and is evaluated manually and logged (§4's 2026-08-06
banner). A cell that HOLDs on a manual evaluation nobody has scheduled is a gate that will read
pending forever for a reason unrelated to the bot. Naming B3 `PENDING-OK` explicitly, with the
2026-11-30 / n=60 trigger already on the record, is the honest encoding of that.

*Consequence for T-36:* identical to (a) — nothing blocks, the printed text is more specific.

*What it costs:* three cells where the other options have one, and a per-criterion (not per-family)
column in `data/audit_gates.csv`. §3.2's schema is per-criterion already, so this costs nothing in
code — only in the ruling's length.

*Locking clause:* not a loosening; B3 is not being weakened, only its evaluation-timing made
explicit. Worth noting that (c) can be layered onto (b) as easily as onto (a) — the split and the
stage are independent choices.

---

## 3 · The "notice" mechanism — a report-only rider (proposed board item **T-55**, lane DEVIN)

§10 item 3's defect is that **nothing notices**. This is the smallest thing that notices. It has
**no gate effect**: no stage changes, no dot changes, no blocker changes. Gating on it later is a
separate decision and needs its own ruling — say so in the ruling that authorizes this.

### 3.1 Lane spec — house style of `_wave-2026-09-10-lanes.md`

> ## Lane N · T-55 — `audit:` rider column on the readiness board (report-only)
>
> **Locate.** `grep -n 'Readiness board\|Exp(R) \[95% CI\]\|def gate_eval\|G5 instruction-mirror'
> scripts/report.py` — run the grep first, STOP if zero or >1 match on `def gate_eval`. Read the
> `compliance` loader at `grep -n '_comp_path' scripts/report.py` — **that is the pattern to copy**:
> an optional CSV, absent-file tolerated, feeding a `(value, detail)` pair.
>
> **Build.** Load `data/audit_gates.csv` (§3.2) into `audit[scope][gate] = (verdict, note)`. Add
> `def audit_rider(bot)` returning one string: resolve the bot's pillar from `data/bots_meta.csv`
> (the dict `report.py` already builds), select the **worst** row for that pillar under precedence
> `fail > pending > pass`, ties broken by gate letter ascending, and format
> `"{gate} {verdict} — {note}"`, e.g. `B2 pending — span 25/184 days`. All rows `pass` → `clear`.
> File absent or pillar unknown → `pending (no audit_gates.csv)`. Family `H` rows are looked up
> under scope `FLEET` and compete in the same precedence for every bot. Family `A` is **not** in the
> rider (per-claim grain, §1.4).
> Add one column `audit` to **both** readiness tables (graduating and non-graduating), immediately
> right of `Blocker`. Extend the gate-legend line with one sentence: the column is **report-only per
> the ruling, and has no gate effect**.
>
> **Red test.** Fixture ledger + `data/bots_meta.csv` giving a bot enough clean condors to reach
> `LIVE-READY` (board passed ≥5), plus an `audit_gates.csv` with `IC,B2,fail`. Assert: the row prints
> `LIVE-READY` **and** `B2 fail` in the same line. *This fixture is §10 item 3 itself; if it does not
> print both, the lane has not done its job.*
>
> **Green test.** (i) `data/audit_gates.csv` absent → every `audit` cell reads
> `pending (no audit_gates.csv)`, and (ii) on the real 2026-09-04 ledger, the `Stage`, `Gates`,
> `n`, `Exp(R)` and `Blocker` columns are **byte-identical** to the pre-change output — diff the two
> generated `STATUS.md` files with the new column stripped. Byte-identity is the proof of "no gate
> effect"; a passing eyeball is not.
>
> **Acceptance predicate.** `python3 scripts/report.py --validate` exits 0 · the byte-identity diff
> in green test (ii) is empty · `grep -c 'audit_gates' scripts/report.py` ≥ 1 · `gate_eval`'s return
> tuple is **unchanged in arity and content** (the rider is computed outside it) · the red-test
> fixture prints `LIVE-READY` and `fail` on one line.
>
> **Out of scope for this lane, explicitly:** any change to `stage`, `passed`, `dots` or `blocker`;
> any code that *writes* `data/audit_gates.csv`; any threshold. Gating on the column is a later
> ruling.

### 3.2 `data/audit_gates.csv` — schema

```
# data/audit_gates.csv — System I (audit gates A–K) verdicts, per pillar.
# ⛔ WRITTEN ONLY BY RULING. NEVER BY CODE, NEVER HAND-INFERRED. An absent row reads
#    PENDING, never PASS (evidence-standards.md §5, "G5 IS THE GATE THAT LIED").
scope,gate,verdict,as_of,note,evidence,ruling_id
```

| Column | Meaning |
|---|---|
| `scope` | a pillar name exactly as it appears in `data/bots_meta.csv` (`IC` · `Directional` · `OA-Mirror`), or the literal `FLEET` for family H. |
| `gate` | an audit criterion id — `B1`, `B2`, `B3`, `C1`…`C4`, `D1`…`D4`, `E1`…`E3`, `F1`…`F4`, `G1`, `H1`…`H3`, `J1`…`J5`. Per-criterion, not per-family, so option (c) needs no schema change. |
| `verdict` | `pass` · `fail` · `pending`. Nothing else. |
| `as_of` | the date the verdict was ruled. |
| `note` | the short string the board prints, with its unit (`span 25/184 days`, `147/100 positions`). |
| `evidence` | file + what was read, e.g. `data/trades.csv 2026-09-08: 147 closed positions post-cutover, pillar IC`. |
| `ruling_id` | the `docs/RULINGS.md` id that wrote the row. Required. A row with no ruling id is not a verdict. |

The file does not exist and **this proposal does not create it** — it is written by the ruling that
settles §2, with its first rows being that ruling's own findings.

---

## 4 · Exact doc text, to paste **after** the ruling

⛔ **Not applied in this session.** Go-live gates are decisions (`CLAUDE.md` §5); the map, the n=0
option and any HOLD at LIVE-READY all change what gets built. `docs/evidence-standards.md` was not
edited. Both blocks below are written for verbatim paste once Andy signs, with
`R-2026-09-XX-T-53-GATE-MAP` standing in for the ruling id he assigns.

### 4.1 New `docs/evidence-standards.md` §5.1 — insert between the end of §5 and `## 6. The R methodology`

```markdown
### 5.1 How the two systems meet

*Written by T-53 under `R-2026-09-XX-T-53-GATE-MAP`. Closes §10 item 3.*

§3 keeps the two systems apart. This section is the one place they touch: **which audit gate must
not be FAIL for a board stage to be honest.** It adds no gate and changes no threshold — it says
what an existing gate means at an existing stage. Both systems are written with their prefix
throughout, per §3.

**HOLD** = must not be FAIL for the stage to be honest · **PENDING-OK** = may be pending, never
FAIL · **N/A** = not applicable at this grain or with no cited artifact · **—** = out of scope.

| Board stage | A | B | C | D | E | F | G | H | I | J | K |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **INCUBATE** | HOLD | PENDING-OK | PENDING-OK | HOLD (D4) | HOLD (E1) | PENDING-OK | N/A | — | — | HOLD | HOLD |
| **VALIDATE** | HOLD | PENDING-OK | PENDING-OK | HOLD (D4) | HOLD (E1) | PENDING-OK | N/A | — | — | HOLD | HOLD |
| **CANDIDATE** | HOLD | PENDING-OK | HOLD (C4) | HOLD (D1, D4) | HOLD (E1) | HOLD | N/A* | — | — | HOLD | HOLD |
| **LIVE-READY** | HOLD | «B-CELL» | HOLD | HOLD | HOLD | HOLD | HOLD* | HOLD | — | HOLD | HOLD |
| **LIVE** (real capital) | HOLD | HOLD (B1+B2+B3) | HOLD | HOLD | HOLD | HOLD | HOLD* | HOLD | HOLD (band) | HOLD | HOLD |

\* audit gate `G` is N/A for a bot whose pre-registration cites no backtest, and HOLD the moment one
is cited — the only cell whose value is per-bot rather than per-stage.

**Audit family `A` is §2, the evidence tiers** — §4's title says A–K and §4 has no `### A` heading.
Its two obligations: every claim carries a tier and is scored at its highest, never averaged up
(**A-tier**); a T4 result may never be cited as support for a T1/T2 claim, and a backtest re-run
after seeing its own output is T4 by definition (**A-cite**).

**Audit gate `I`** is a rubric, not a pass/fail, and is computed by no surface today — it is HOLD
only at LIVE, where its own band language lives. **Audit family `K`** is read as a prohibition on
rationales: nothing worth zero may be cited as a reason a bot advanced. **Audit gate `T3`** (§4.5)
is N/A on every board row — it authorizes building and sizing an experiment, never live capital,
and it is upstream of INCUBATE rather than a stage gate.

**Inheritance — how a per-pillar verdict reaches a per-bot row.** A bot inherits its pillar's audit
verdict. The pillar is `data/bots_meta.csv`'s `pillar` column — the same one `scripts/report.py`
already reads — so every `IC-*` and every `GF-*` arm inherits the IC pillar's verdict, and so on.
Two families do not join on pillar: **H** is fleet grain (scope `FLEET`), and **A** is per *claim*,
evaluated at the decision that cites it rather than on the board. Verdicts live in
`data/audit_gates.csv`, one row per pillar × criterion, **written only by ruling and never by
code** — System I is adjudicated, not computed (§4).

> ⛔ **An absent row reads PENDING, never PASS.** This is §5's G5 lesson applied before the fact: a
> pending gate is honest, a passing gate built on an absent record is not.

**What maps to nothing, in both directions.** Board gate G1 (clean data) and board gate G5
(instruction-mirror compliance) have no audit counterpart — both are v2 additions answering v1
failures. Going the other way, **seven of eleven audit families — A, E, F, H, I, J, K — have no
board gate at all**, because the board computes what the ledger can compute: sample, expectancy,
risk, tracking. Mechanism, overfitting, portfolio concentration, the kill list and the worth-zero
list are invisible to it by construction. That is why §10 item 3's defect existed: not an oversight
in the board, but the board's grain. The `audit:` rider column makes it visible; it does not fix it.
```

Where `«B-CELL»` is replaced by exactly one of, per Andy's §2 ruling:

| Option | Paste into the `LIVE-READY` × `B` cell | Plus this sentence after the table |
|---|---|---|
| **(a)** | `PENDING-OK (flagged)` | *"Audit gate B is HOLD at LIVE only. A bot at LIVE-READY with B unmet prints a visible `audit B pending` rider — LIVE-READY means board-clean, not admissible, and the rider says so."* |
| **(b)** | `HOLD` | *"Audit gate B is HOLD at LIVE-READY: a bot whose pillar has not cleared B tops out at CANDIDATE. **This is a tightening and is flagged as one under §1's locking clause.** B2 (span ≥ 6 months) is satisfiable no earlier than 2027-02-10, from the earliest post-cutover `open_date` of 2026-08-10 in `data/trades.csv`."* |
| **(c)** | `B3 PENDING-OK · B1, B2 HOLD at LIVE` | *"Audit gate B splits: B3 (regime change) is PENDING-OK at every board stage — it has no detector and is evaluated manually and logged (§4, 2026-08-06 banner; trigger = the earlier of any arm's n=60 interim read or 2026-11-30). B1 and B2 are HOLD at LIVE. The rider names the missing conjunct, not the family."* |

### 4.2 `docs/evidence-standards.md` §10 item 3 — strike, following items 1 and 2's convention

```markdown
3. ~~**Reconcile the two gate systems** (§3). Nothing anywhere maps audit A–K onto board G1–G6.
   They measure different things at different grains, which is fine — but a bot can be
   LIVE-READY on the board while its pillar fails audit gate B, and nothing currently notices.~~
   — **CLOSED 2026-09-XX: mapped** (§5.1, written by T-53 under `R-2026-09-XX-T-53-GATE-MAP`).
   The map is §5.1's table; the inheritance rule is `data/bots_meta.csv`'s `pillar` column joined
   to `data/audit_gates.csv`; the *"nothing notices"* half is closed by the report-only `audit:`
   rider on the readiness board (board item T-55). **Still open, and narrower:** the rider notices
   but does not gate — whether a FAIL row may block a board stage in code is a separate decision,
   not taken here.
```

### 4.3 Collisions §3 warns about that this text touches

§3's warning names `G1`, `B1`, `C1`, `C2` and `G2` as colliding. Every one of them appears above,
and every one is written with its system:

| Collision | Audit meaning (System I) | Board meaning (System II) | Where both appear above |
|---|---|---|---|
| `G1` | live Exp(R) ≥ 50% of backtested Exp(R) (§4 G) | clean data — no strike-bug, single-sided excluded (§5) | §1.2 column G vs §1.5 |
| `B1` | n ≥ 100 closed positions at T1/T2 | *(no board B)* — the board's sample gate is **G2** | §2.2, §2.3 |
| `G2` | *(no audit G2)* | ≥ 20 clean condors | §1.3 B-row, §2.3 |
| `C1` | expectancy per position in R > 0 after costs | *(no board C)* — the board's edge gate is **G3** | §1.3 C-row |
| `C2` | expectancy > 0 with the largest winner removed | — | §1.3 C-row |
| `T3` | audit gate T3, criteria T3.1–T3.6 (§4.5) | — ; and **evidence tier T3** = OOS backtest (§2) | §1.5 |

A bare letter appears nowhere in §4.1's paste text: every instance is prefixed *audit gate* / *audit
family* or *board gate* / *board stage*, or sits inside a table whose column header is the system.

---

## 5 · Gated vs mechanical

### 5.1 Needs Andy's ruling — nothing below may be applied without it

1. **The map itself** (§1.2 table + §1.3 rationales). It states which audit gate must not be FAIL at
   which board stage — a go-live gate statement, gated by `CLAUDE.md` §5 with no exception.
2. **The n=0 option** — (a), (b) or (c) from §2.3, or a fourth. Option (b) is additionally a
   **tightening** and §1's locking clause requires it be flagged as one out loud; §4.1's option (b)
   sentence carries that flag.
3. **Any HOLD at LIVE-READY** — specifically the `LIVE-READY` row's B, C, D, E, F, G and H cells.
   The C/D/E/F/G/H cells at LIVE-READY are new HOLDs regardless of which B option is chosen.
4. **The inheritance rule** (§1.4) — that a bot inherits its pillar's verdict and that an absent row
   reads pending. It decides what a stage word means, so it is a decision.
5. **`data/audit_gates.csv` existing at all, and its first rows.** The file is a decision record;
   its rows are rulings. Nothing writes it but a ruling.
6. **Board item T-55** as a Devin lane (the rider). Report-only, but it changes a surface Andy reads.
7. **Whether a FAIL row may ever gate a board stage in code.** Explicitly *not* proposed here.
   Named so it is on the record as an open decision rather than an omission.

### 5.2 Mechanical propagation once ruled — no further judgment

Each of these is entailed by the ruling above, per `R-2026-08-31-DERIVED-RULING-AUTHORITY` (a):

1. **Paste §4.1 into `docs/evidence-standards.md` as §5.1**, `«B-CELL»` filled per the chosen option
   and the ruling id substituted. Verify by `shasum -a 256` + single-match grep, never a tool reply.
2. **Paste §4.2 over §10 item 3**, following items 1 and 2's `~~struck~~ — **CLOSED**` convention.
3. **`data/portfolio.csv`**: T-53 → `Done` with the ruling id; add item **T-55** (P7, lane DEVIN,
   the §3.1 spec) — then `python3 scripts/portfolio.py --check`.
4. **`drafts/_wave-2026-09-10-lanes.md`** (or the next wave file): append §3.1 verbatim as a lane.
5. **`data/audit_gates.csv`**: create with the header in §3.2 and the ruling's own rows.
6. **`docs/RULINGS.md`**: the ruling entry, plus a cross-reference from §5.1's banner.

Steps 1–2 are still `docs/evidence-standards.md` edits and are **decision-class, not
corrections-class** — they are mechanical only in the sense that the text is already written; the
authority to write it comes from the ruling, not from `CLAUDE.md` §5's corrections carve-out.

---

## 6 · What I did not read, and what I could not verify

**Not read this session:**
- `~/bot-fleet/docs/independent-audit-2026-07-27-precommitment-ledger.md` beyond its section
  headings and §A's ten lines. Sections B–K were taken from `evidence-standards.md` §4, which
  `docs/history-index.md` records as verified line-by-line against the original on 2026-08-03.
- `docs/build-plan.md` §5 and §1 — cited by `CLAUDE.md` §4 and by §10 item 5, not opened.
- `docs/rules-of-engagement.md` — its four `<FILL>` blanks are the audit H3 gap; the count comes
  from `evidence-standards.md` §10 item 4, not from the file.
- `docs/pre-registration-ledger.md` — so which bots' entries cite a backtest (deciding audit gate
  G's N/A-vs-HOLD per bot, §1.2 footnote \*) is **unenumerated**.
- `data/compliance.csv` — read only as a code pattern in `report.py`, not for its contents.
- `docs/oa-mirror-reference.md` §3, named in `evidence-standards.md`'s source line as the project's
  prior standards.

**Could not verify:**
- **[UNCLEAR] Whether OA paper fills satisfy evidence tier T2's *"with realistic fills"* conjunct.**
  Nothing in the repo rules on it, and it is load-bearing for §2.2 — if paper is not T2, the IC
  pillar's 147 closed positions do not count toward B1 and §10 item 5's original premise stands
  unchanged. This is a ruling-sized question hiding inside a units question.
- **Whether audit gate F2 has fired on any pillar** (parameters changed more than once per 30
  trading days → sample count resets). Evaluating it needs the config-change history per bot, which
  I did not reconstruct. If F2 has fired, the B1 counts in §2.1 restart from the last change date.
- **Whether audit gate B3 has ever been evaluated.** §4's banner requires each manual evaluation to
  be logged in `docs/session-log.md` citing the VIX read; I did not grep the session log for one.
  Stated as "no such evaluation has been run" in §2.2 on the strength of the banner's own framing —
  **that is an inference from absence and is flagged as one** (`CLAUDE.md` §5).
- **The 25-calendar-day span in §2.1** is `open_date` max − min. If B2's *"forward/live time"* is
  meant to run to today rather than to the last trade, it is 29 days as of 2026-09-08. Either way
  the 2027-02-10 date is set by the 2026-08-10 start, not by the end.

**A note on one number I did not use:** `data/portfolio.csv` T-36 records `IC-SPX-FastPT25-S2-130PM`
at **n=19 clean condors, Exp(R) +0.055 per condor** at 2026-09-04. I cite it as the clock only. I
did not recompute it, and this proposal makes no claim about whether board gate G3 will clear.
