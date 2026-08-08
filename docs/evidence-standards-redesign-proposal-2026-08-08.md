# Evidence-standards REDESIGN PROPOSAL — 2026-08-08

> ## ⛔ PREPARED, NOT RULED. THIS DOCUMENT DECIDES NOTHING.
> It proposes; it does not amend. **`docs/evidence-standards.md` was not edited by the session
> that wrote this**, no other file's text was changed, nothing was propagated, no OA surface was
> touched, no browser tool was run, no git command was run (including `status`).
> Every "RECOMMENDATION" below is labelled as one. Every item that would change a decision is
> flagged **DECISION — ANDY**. Adopting any part of this requires an explicit **"amend the
> plan"** (`CLAUDE.md` §5): `evidence-standards.md` carries sizing rules, kill criteria and
> go-live gates, so it is a gated surface end to end.
>
> **Written against fresh device reads.** Every quoted phrase was asserted byte-exact against
> the device file by a `device_bash` `grep -cF` with the count stated; the assert table and the
> sha256 set are in §8.

**Why this exists.** `evidence-standards.md`'s own header says **✍️ WRITTEN TO BE REVISED**, and
its §10 lists seven items it thinks a redesign should fix. Andy has asked for a scoring system
beyond tiers + gates. This is the argument-with-something-concrete that header asked for.

**Standing constraint, quoted from the document being redesigned** (`evidence-standards.md` §1,
grep `THESE CRITERIA ARE LOCKED` = 1):

> *"THESE CRITERIA ARE LOCKED. I WILL NOT LOOSEN THEM AFTER SEEING THE RESULTS. If I find a
> threshold was wrong, I may only make it STRICTER, and I must flag that I did."*

**Every option below is checked against that clause in §3, out loud.** Two loosen nothing.
One can loosen if written carelessly, and that is flagged rather than hidden.

**⛔ WHAT IS NOT ON THE TABLE — §1 and §9.2 are a RECORD, not a rule up for redesign.**
`evidence-standards.md` §1's overrule table (kill-IC overruled · Fortress auto-kill overruled ·
custody separation and independent go-live authority DECLINED) and §9.2's 2026-07-31 correction
of the "third-party switch" transcription are decisions Andy already made. **Under every option
in this proposal they are carried verbatim, unmoved, and are never re-scored** — no corroboration
cell, no ladder position, no threshold is attached to them, and no migration step rewrites them.
§10 item 7's *optional* reconsideration of custody separation is Andy's to open and is
deliberately not argued here.

---

## 1. The downstream-consumer map — built first, because everything else depends on it

A redesign of a scoring system is only as safe as the list of things that read it. That list did
not exist; this is it. Method: `device_bash` `grep -rl` over `docs/`, `scripts/`, `CLAUDE.md`,
`STATUS.md`, `data/`. Counts are from the device on 2026-08-08.

### 1.1 Five consumer classes

| # | What is consumed | Consumers (files) | Reach |
|---|---|---|--:|
| **A** | **Evidence tiers T1–T5** — a claim carrying an evidence class | `CLAUDE.md` · `evidence-standards.md` · `history-index.md` · `session-log.md` · `baseline-forensic-2026-08-07.md` · `build-plan.md` · `exploratory-bots-design-2026-08-07.md` · `mirror-funding-memo-2026-08-05.md` · `pre-registration-ledger.md` · `sprint-2026-08-04.md` | **10** |
| **B** | **Audit gates A–K** (System I) | `evidence-standards.md` · `state.md` · `session-log.md` · `baseline-forensic-2026-08-07.md` · `decision-card-2026-08-06.md` · `greenfield-family-spec.md` · `pre-registration-ledger.md` · `track-b-arms-spec.md` | **8** |
| **C** | **Board gates G1–G6** (System II, code-enforced) | `scripts/report.py` · `STATUS.md` · `evidence-standards.md` · `session-log.md` | **4** |
| **D** | **Gate T3** (§4.5, T3.1–T3.6) | `evidence-standards.md` · `state.md` · `session-log.md` · `baseline-forensic-2026-08-07.md` · `greenfield-family-spec.md` · `track-b-arms-spec.md` | **6** |
| **E** | **The bracket provenance vocabulary** — `[FIRST-HAND]` / `[FIRST-HAND, UNCORROBORATED]` / `[DERIVED, UNCORROBORATED]` / `[LEDGER]` / `[EXPORT]` / `[PROJECT-RULE]` / `[DOCUMENTED]` / `[DOCS-SILENT]` / `[MACHINE-VERIFIED]` | 25 docs + `scripts/comparative_machinery.py` + `scripts/research_loop.py` + 2 capture files | **29** |

**Class E is roughly three times the reach of class A, and it appears nowhere in
`evidence-standards.md`.** 342 tagged instances across `docs/` alone.

### 1.2 And there is a third vocabulary, in data

`data/oa_facts.csv` carries a `tier` column over **1,548 facts**. Its values are **not** T1–T5
and **not** the bracket set — they are exactly two: **`DOCUMENTED` (1,401)** and **`DOCS-SILENT`
(147)**. So the project runs three unrelated provenance vocabularies at once: T1–T5 in ten docs,
the bracket set in twenty-nine surfaces, and a two-value column over fifteen hundred facts.

⭐ **And the operative authorization test uses the third one, not the first.** `CLAUDE.md` §5's
evidence-backed-correction rule turns on *"a `data/oa_facts.csv` fact ID with its verbatim"*
quote (grep, `CLAUDE.md` line 87 = 1) — **the daily gate on whether Claude may edit a document at
all runs on a vocabulary the standards file does not define.**

### 1.3 The collision map — six live namespaces, of which §2.2 lists four

`evidence-standards.md` §2.2 warns about `T1–T3` in `hedge-research.md`, `oa-platform-reference.md`,
the old brief spec, and `build-plan.md` §6. Two more are live and unlisted:

- **`ic-trailing-stop-backtest.md`** uses `T1` / `T2` as **tournament round labels** —
  `T1-Control`, `T1-Ride`, `T1-Trail-A/B/C`, then `T2` = refine the width (grep `T1-Control` = 4).
- **`daily-loop-spec.md` carries three unrelated "tier" axes in one file**: detector build-classes
  **Tier S / Tier C** (§5, grep = 1), counterfactual **cost tiers** EXACT / APPROXIMATE (§7), and
  **Build tiers 0–2** (§11, grep = 1). None is an evidence tier.

And **`G` now carries three schemes, not two**: audit gates A–K, board gates G1–G6, and the
ruling-slot IDs **G-1 … G-16** including **G-12b** (`comparative-machinery-spec.md` §8,
`g-rulings-card-2026-08-07.md`). §3's warning that *"`G1` means two different things"* is now an
undercount.

> ⚠️ **A note the migration story depends on: G-12b's `T1` is not an evidence tier.**
> `pre-registration-ledger.md`'s signed entry reads *"TAIL RETIREMENT CRITERION — **PR-16 T1**,
> FAST-MOVE TAIL PAIRED NON-HARM TEST"*. That `T1` is **test one of PR-16**, a test identifier
> inside a signed ruling. No option in this proposal touches it, re-scores it, or re-reads it as
> an evidence class. It is listed here because the collision is live enough that the brief
> commissioning this proposal referred to *"G-12b's T1"* as a tiered claim — which is exactly the
> failure mode §2.2 exists to prevent, occurring in the request for the fix.

---

## 2. Diagnosis

### 2.1 What the tiers-and-gates system does well — keep all of this

1. **The kill list is binary and that is correct.** J1–J5 and worth-zero K need no scoring. A
   kill that can be scored can be argued with, and audit §3.5's finding is that this project
   argues with rules that fire against bots its owner built. Do not put a number on a kill.
2. **Gate E (mechanism) is unscoreable and load-bearing.** *"It backtested well is not a
   mechanism"* is the cheapest, least gameable test in the corpus. No redesign should numeric-ize it.
3. **§6's unit-of-account and §6.1's labelling law are the document's most-used export** —
   *"per condor, ex-artifact"* vs *"per leg, raw"*, three numbers for one window and only one
   meaning anything. This is cited across the specs and is not in dispute.
4. **The gate-T3 authorize/does-not-authorize split is the right shape.** §4.5 answers "what does
   this evidence *buy* you" rather than "how good is it" — build it, paper it, size it; never live
   capital. Every option below reuses that shape.
5. **§3's diagnosis that the two gate systems measure different things at different grains is
   correct.** It is unfinished, not wrong.
6. **The locking clause is machinery worth keeping**, and it binds this proposal too.

### 2.2 Where it strains — seven, each with a worked example from this repo

**S-1 · The tier saturates, so it carries no information.**
`baseline-forensic-2026-08-07.md` scores every one of its five ranked hypotheses at the **highest
tier**: *"**Evidence tier is T1 LIVE for all of them**"*, and says so plainly — *"that is the
**least** interesting thing about it, because T1 data at n=43 still fails gate B1."* Five claims,
one tier, and the tier did none of the work. **A five-level scale on which every live observation
scores 1 is not a scale.**

**S-2 · So the author invented the missing axis — and mis-cited it into existence.**
The same file adds a second column: *"each hypothesis below carries **two** labels: its evidence
tier (uniformly T1) and a separate **confidence** in the *inference***", then guards it —
*"Confidence is not a tier and must not be cited"* as one (grep = 1). The resulting citations read
**`Tier T1 LIVE · confidence HIGH · gate B1 FAIL (n=10)`** — a three-field form the standards
document does not define. And the block that introduces it cites **`evidence-standards.md` §2.1
note 4** (grep = 1) — **§2.1 has three notes** — and cites **§3** for the tiers, which live in
**§2**; §3 is the two-gate-systems section. *(Recorded as diagnosis. Not corrected here — this
document edits nothing.)* **When a competent downstream author has to invent a scoring axis and
mis-attribute it to the standards file, the standards file is missing that axis.**

**S-3 · A parallel vocabulary already won on volume, and it is the one that gates edits.**
Class E above: 342 instances, 29 surfaces, versus T1–T5's 10. It is also **internally
inconsistent** — `[PROJECT-RULE, not doc-verified.]` (7) vs `[PROJECT-RULE, not doc-verified]`
(6); `[FIRST-HAND, UNCORROBORATED]` (20) vs `[FIRST-HAND, **UNCORROBORATED**]` (1) — because
nothing defines it, so nothing normalizes it. And per §1.2, `CLAUDE.md` §5's edit gate runs on the
third vocabulary again. **Three provenance systems, and the official one has the smallest reach
and the least authority.**

**S-4 · Residual attachment is a real, working primitive with no home in the standards.**
C12's discharge does not travel as a verdict. It travels as a **four-part object**: the claim, its
tier `[FIRST-HAND, UNCORROBORATED]`, a **residual** (*"this is the footer's accounting, not OA's
enforcement… observed with **one** archived bot where the Group-A sweep archives twenty"*), and a
**pre-declared reopen condition** (*"if a build ever fails at the cap despite archived bots
existing, C12 reopens"*). It was propagated across four surfaces in that shape, under a rule
stated in `state.md`: *"A discharge propagated without its residual is worse than no
propagation."* (grep = 1), and in `track-b-arms-spec.md`: propagating it bare *"converts an
[UNCORROBORATED] footer read into a settled fact"* (grep = 1). **T1–T5 cannot express "highest
tier, one witness, and here is what reopens it." The project built the mechanism anyway and wrote
its governing rule into a live-facts page and a spec instead of the standards document.**

**S-5 · Gate-vs-tier confusion is structural, not a naming accident.**
**`T3` is simultaneously an evidence tier (§2: OOS BACKTEST) and a gate (§4.5, criteria
T3.1–T3.6).** The gate is *named after* the tier and *does not correspond to it*: a T3 backtest
that fails gate T3 is still tier T3. Add §1.3's six namespaces and three `G` schemes and the
result is that a reader cannot resolve `T2` or `G1` without knowing which document they are in.
§2.2 and §3 both flag this and neither can fix it, because the fix is renaming, and renaming is a
change to specs.

**S-6 · The one scoring system already in the document is not computed anywhere.**
§4-I's **0–100 confidence score** is the only continuous scale in the corpus. It has one recorded
value — **9/100, at the 2026-07-27 audit** — and no surface produces it. `grep -rn confidence
scripts/*.py` returns only `comparative_machinery.py`'s empirical-Bernstein **confidence
sequence**, an unrelated statistical object. `grep -oE 'gate [A-K]' scripts/` returns **nothing**:
**System I is not implemented at all.** Read literally, "a scoring system beyond tiers and gates"
is a request for the thing §4-I already promises and no code delivers.

**S-7 · Retiring a standard is not currently an executable act.**
§5 retires the legacy go-live bar and says so in bold: *"Do not reinstate a 15-condor bar."*
(grep = 1). **`scripts/report.py` line 141 still emits it and `STATUS.md` line 17 carries it
today**: `- Go-live gate (≥15 clean post-fix condor trades): **0 / 15**` (grep = 1 in each). The
numeric source-of-truth page currently publishes a gate the standards document retired eight days
ago. Nothing enumerated the consumers, so the retirement reached the document it was written in
and no further — this repo's most-reproduced defect class, applied to the standards file itself.

**S-8 · At n=0 the whole system reports one value, for six months.**
§10 item 5 says it: B1 (≥100 positions) and B2 (≥6 months) are *"unreachable for roughly six
months **by construction, and that is accepted and priced in**"*, and the honest answer on what is
admissible meanwhile is *"almost none"* (line 505). A binary PASS/FAIL admissibility system
therefore returns FAIL for every bot on every day until roughly mid-February 2027. **It cannot
distinguish week one from month five, and it gives the interim no vocabulary at all** — which is
precisely where an unscored project starts making unscored decisions.

---

## 3. Three candidate designs

**Backward compatibility is a first-class requirement and is scored first for each option. A
design that re-litigates a settled ruling is disqualified — not discounted.** The signed
population a migration must survive: **G-12b**'s three constants (δ=0.10R, p=0.20, floor
n_matched_days≥100 + one re-arm at Day-0+9mo) · **G-1′ DECLINED** · the sixteen **G-1…G-16**
rulings of 2026-08-06/07 · **C12**'s discharge with its residual and reopen condition · the seven
slots of `decision-card-2026-08-06.md` · **B3**'s ratification as the regime-change definition ·
every tiered claim in `pre-registration-ledger.md`, `greenfield-family-spec.md`,
`track-b-arms-spec.md`, `build-plan.md` and `baseline-forensic-2026-08-07.md`.

---

### OPTION 1 — RATIFY THE PRACTICE. Two-axis *labelling*, residual attachment, consumer registry. No new thresholds.

**Shape.** Add three sections to `evidence-standards.md` and change no value anywhere.

- **§2.3 — the provenance axis.** Adopt the bracket vocabulary already in use (class E) as a named
  second axis, orthogonal to T1–T5, with a normalized closed set and one spelling each:
  `[DOCUMENTED]` · `[FIRST-HAND]` · `[FIRST-HAND, UNCORROBORATED]` · `[DERIVED, UNCORROBORATED]` ·
  `[LEDGER]` · `[EXPORT]` · `[PROJECT-RULE]` · `[DOCS-SILENT]` · `[MACHINE-VERIFIED]`.
  Reconcile `data/oa_facts.csv`'s two-value column as a *subset* of it, not a rival.
- **§2.4 — the citation form.** Ratify `baseline-forensic`'s invention as the standing shape:
  **`tier · provenance · confidence-in-the-inference · gate status (n)`**, with its own guard
  quoted — confidence is not a tier.
- **§2.5 — residual attachment.** Codify the C12 object: any claim used at a decision while
  carrying a known weakness travels as **{claim · tier · provenance · residual · pre-declared
  reopen condition}**, and *"a discharge propagated without its residual is worse than no
  propagation"* becomes a standards rule rather than a line in `state.md`.
- **§11 — the consumer registry.** §1 of this document, maintained. Retiring or changing a
  standard requires walking it.

**Cost.** It does **no new statistical work**. §4-I's 0–100 score stays uncomputed; §10 items 3
(map the two gate systems), 4 (the `<FILL>` blanks) and 5 (interim admissibility) stay open;
S-6 and S-8 are untouched. It is documentation catching up with practice — the smallest possible
change, therefore the least likely to be wrong, **and it is not a scoring system.** If Andy's ask
is scoring, Option 1 alone does not answer it.

**Locking clause:** loosens nothing. Adds one requirement (residual attachment) — strictly
stricter.

**Migration story: nothing moves.** No signed ruling changes value or is re-read. G-12b's `T1` is
a test label and is out of scope by construction. C12's discharge is *already* in the §2.5 shape
and becomes conformant retroactively with zero text change. The 342 existing bracket tags stay
valid; the ~13 inconsistent spellings are normalized **lazily, on next edit of the line**, never
as a sweep. Every tiered claim in the specs keeps its tier and *may* gain a second axis; none is
required to. **Backward compatibility: complete.**

---

### OPTION 2 — TWO-AXIS SCORING: TIER × CORROBORATION, with a decision-grade threshold table *(recommended, see §5)*

**Shape.** Option 1's three sections, plus a genuine second dimension and the thing that makes it
bite.

- **Axis 1 — evidence tier T1–T5, carried verbatim.** Not renumbered, not reworded, not
  rethresholded. What kind of execution produced this.
- **Axis 2 — corroboration C0–C3.** How many independent witnesses stand behind it.

| | Corroboration level |
|---|---|
| **C0** | Asserted. No witness recorded. (Includes inference-from-absence, which `CLAUDE.md` §5 already refuses.) |
| **C1** | One first-hand witness — a DOM read, a screenshot, one capture, one export column. |
| **C2** | Two independent witnesses, or one witness plus a machine check that could have failed. |
| **C3** | C2, plus a recorded attempt to refute it that failed. |

- **A claim cites `T<n>/C<m>`.** `T1/C1` — real fills, one witness. `T3/C2` — OOS backtest with a
  control. `T5/C0` — an idea nobody checked; still scores zero, as today.
- **Corroboration never loosens a gate and never substitutes for sample.** It does exactly two
  things: (i) it decides whether a **residual is mandatory** — any C0 or C1 claim used at a
  decision must carry a residual and a pre-declared reopen condition, the C12 shape generalized;
  (ii) it decides **how the claim may be cited** — a C0/C1 claim may not be propagated as settled,
  and may not be the sole support for a decision one class above it.
- **Decision-grade threshold table** — the §4.5 authorize/does-not-authorize shape, generalized
  across decision classes:

| Decision class | Minimum cell | Also required |
|---|---|---|
| **D0** record a fact | any, tier labelled | provenance stated |
| **D1** correct a doc | ≥ C1, quotable | `CLAUDE.md` §5's five conditions, unchanged |
| **D2** authorize a build | ≥ T3/C1 | gate T3 §4.5 for anything mechanism-dependent |
| **D3** set sizing | ≥ T3/C2 | gate T3 full pass; §4.5's existing "sets its sizing tier" |
| **D4** live capital | ≥ T2/C2 | audit gates B + C + D + E, unchanged; J1–J5 clear |
| **D5** grow size | ≥ T1/C2 | B + C + D + E + F + G, unchanged; §4-I band ≥ 51 |

  ⛔ **D4 and D5 restate today's bars; they do not lower them.** *"Nothing below T2 with n≥100
  positions / 6 months / a regime change supports a live-capital or growth decision"* is unchanged
  and is what D4/D5 point at. **The table's whole contribution is at D0–D3**, where the corpus
  currently has no vocabulary at all.

**Cost, stated honestly.**
1. **A second thing to argue about per claim.** Every new fact needs a corroboration judgment, and
   corroboration judgments are cheap to inflate.
2. **C2 is often unavailable in a one-operator project, structurally.** `research-loop-spec.md` §6
   item 1 says it outright about the load-bearing case: MFE/MAE have *"no second witness — nothing
   else on hand can check them. Treat as `[FIRST-HAND, UNCORROBORATED]`."* (grep = 1). A design
   that demands C2 for ordinary work will be routed around.
3. **Saturation risk, one level up (the S-1 defect repeating).** If nearly everything lands at C1,
   the axis carries no information either. **Mitigation, and it is the design's core choice: the
   C-axis is not a quality bar, it is a *residual trigger*.** It never blocks a D0–D3 decision; it
   decides what must be written down alongside it. An axis that mostly reads C1 and mostly demands
   a residual is still doing the job — that is the C12 precedent, which worked.
4. **It does not compute §4-I's score** (S-6 survives) and does not map A–K to G1–G6 (§10 item 3
   survives).

**Locking clause:** loosens nothing. C-levels add requirements only. **Declared explicitly in the
adopting text**, per the clause.

**Migration story — additive, lazy, and non-retroactive by rule.**

> **THE NO-RE-LITIGATION CLAUSE, which is part of the design and not a caveat on it:**
> *Every ruling signed before the adoption date keeps its tier, its text and its force, and is
> read at **C-unspecified**. The corroboration axis is not applied retroactively to any signed
> ruling, and no signed ruling is re-scored, re-opened, weakened or invalidated by it. Where a
> signed ruling's own text already carries a residual, that residual is its C-record and needs no
> restatement.*

- **G-12b** — its three constants are *signed values*, not evidence claims. Untouched. Its `T1` is
  a test identifier (§1.3). Untouched.
- **C12's residual** — maps to **C1-with-residual with zero text change**; it is the worked example
  the design is generalized from. It does not need re-propagating, which matters, because
  re-propagating it is how it would get damaged.
- **The 342 bracket tags** — a mapping table is supplied (`[FIRST-HAND, UNCORROBORATED]` → C1 ·
  `[FIRST-HAND ×2]` / `[DOCUMENTED + FIRST-HAND]` → C2 · `[DERIVED, UNCORROBORATED]` → C1 ·
  `[DOCUMENTED]` → C2 when the verbatim quote is present, else C1 · `[PROJECT-RULE]` → C0 by
  definition, it is a rule not an observation) and is applied **lazily, on next edit of a line,
  never as a sweep**. The bracket forms remain permanently valid citations. **A mechanical re-tag
  of 29 surfaces is exactly the propagation surface this project fails at; the design must not
  require one, and this one does not.**
- **Gate T3, gates A–K, board G1–G6, B3, the R methodology, §6.1's labelling law** — unchanged in
  wording and threshold.

**Backward compatibility: complete, by an explicit clause rather than by hope.**

---

### OPTION 3 — DECISION-GRADE LADDER: a computed, per-decision admissibility position, printed nightly

**Shape.** Option 2, plus: the decision-class table becomes a **computed ladder**. `scripts/`
evaluates, per bot and per pillar, the highest decision class the current evidence supports, and
prints it on `STATUS.md` beside the readiness board and in the daily brief. §10 item 5's interim
question gets a structural answer: **D0–D2 are reachable at n=0; D3 needs a full gate-T3 pass;
D4/D5 need B+C+D+E+F+G** — so the six-month interim has a *stated, non-empty* admissible set
instead of *"almost none"*. §10 item 3's A–K ↔ G1–G6 map becomes a by-product: the ladder is the
join, and a bot that is LIVE-READY on the board while its pillar fails audit gate B lands at D3,
visibly, instead of nobody noticing.

**Cost — the largest of the three, and some of it is timing.**
1. **It is a code deliverable.** `report.py` changes plus a new ladder table, at a moment when
   `research_loop.py` is 0.1.0-DRAFT with three fatal defects and not wired in, A7 is not wired
   into `daily.sh`, and Day-0 is the live constraint. Code-lane work, `CLAUDE.md` §7.
2. **A ladder printed nightly is a bar that can be argued with nightly.** Audit §3.5: *"no
   strategy the owner built himself has ever been killed by a triggered rule."* A daily-visible
   position invites daily negotiation with it in a way an annual gate does not.
3. **It touches frozen text.** §10 item 5's answer implies wording on `build-plan.md` §5's
   conjunctive gate — 🔒 frozen, explicit "amend the plan".
4. **⚠️ It is the only option that can loosen a gate.** Writing "D2 is reachable at n=0" is either
   a clarification (B1 was never a gate on *build* decisions, only on live-capital and growth
   decisions) or a loosening (B1 now has an exception). **The first reading looks correct on the
   text** — §4.5 already authorizes building and sizing off a T3 pass with B1 expressly unchanged —
   **but which reading it is, is a decision, not a transcription, and the locking clause requires
   it be declared out loud either way.** Flagged **DECISION — ANDY**.

**Migration story — the highest re-litigation risk in the proposal, and it is concentrated in one
place.** §4-I's **0–100 band is an audit artifact** and the **9/100** verdict is the number the
overruled kill-IC recommendation was scored against (`evidence-standards.md` §1, §4-K).

> ⛔ **A ladder that REPLACES gate I is disqualified under this proposal's own terms.** Replacing
> the rubric re-opens the scoring basis of a verdict Andy already overruled, which is
> re-litigation of a settled ruling. **Option 3 is admissible only in its additive form: the
> ladder is added *beside* gate I, gate I's band text and the 9/100 record are preserved verbatim,
> and the ladder is never described as superseding them.** In additive form its backward
> compatibility is complete; in replacing form it is disqualified.

---

## 4. What each option changes in the daily loop's three verdicts and the detector's tiers

**The invariant, first, because every option must protect it.** `daily-loop-spec.md` §2: three
verdicts, **never blended**; each carries its own status; 🟢 GREEN / 🟡 AMBER / 🔴 RED per axis.
And §5: the detector *"is a **detector, not a judge**"* — no rule sits on the STRATEGY axis, and
mixing detection with judgment *"is the failure this document exists to prevent."*
**The three verdicts are BEHAVIORAL — did the bot do what it was built to do. Evidence scoring is
EPISTEMIC — how well do we know a claim. Nothing in any option couples them, and every option must
say so in writing, or the loop starts blending an evidence score into a behavior verdict, which is
the exact failure §2 was written against.**

| | Three verdicts (§2) | Detector Tier S / Tier C (§5) | Counterfactual cost tiers (§7) | Instruction cards (§8) |
|---|---|---|---|---|
| **Opt 1** | No mechanical change. Facts cited in the brief gain a provenance label. | No change. **Recommend renaming Tier S/C → Class S/C** to clear the §1.3 collision — a spec edit, so **DECISION — ANDY**. | No change. `approx` labelling already *is* a provenance rule; §2.3 should name it as one. | No change. |
| **Opt 2** | No change to the three axes, their independence, or GREEN/AMBER/RED. | No change to what runs. The **SKIPPED-with-reason rule maps exactly onto C0** — a config-blind Tier C detector is an unwitnessed claim, and reporting it as SKIPPED rather than silent is corroboration discipline already implemented. Same rename recommendation. | `EXACT` ≈ C2 (from data already held, machine-checkable); `APPROXIMATE` ≈ C1 with a mandatory residual — which restates §7's existing rule *"never let an approximate counterfactual drive a config decision on its own"* as an instance of the general one. **A ratification, not a change.** | One addition: a card carries the **corroboration cell of the finding it rests on**, so a C0/C1 finding cannot authorize a config change on its own — it authorizes a *look*. This is `SILENT_BOT`'s existing rule generalized: *"`SILENT_BOT` can never be RED"* is precisely a one-witness-is-insufficient rule, and Opt 2 explains it rather than altering it. |
| **Opt 3** | Unchanged, **and the separation must be written into `daily-loop-spec.md` §2 explicitly**: the ladder position is not a fourth verdict and never blends with the three. | As Opt 2. Additionally, **B3's still-unwired detector** (ratified 2026-08-06, manual until wired, trigger n=60 or 2026-11-30) becomes a ladder input — the ladder cannot compute D4/D5 without it, which turns a deferred item into a dated dependency. | As Opt 2. | As Opt 2, plus a ladder row in §6's brief and on `STATUS.md`. |

**Common to all three, and independent of which is chosen:** `STATUS.md` and `scripts/report.py`
currently publish the **retired** ≥15-condor go-live gate (S-7). Whatever else is adopted, that
line is either removed or the retirement in §5 is reversed. It cannot stay as-is under any design.
**DECISION — ANDY** (it is a code change and it changes what the numeric source-of-truth asserts).

---

## 5. RECOMMENDATION

> ### ⭐ RECOMMENDATION — **OPTION 2, staged, with Option 1 as its first stage and Option 3 deferred behind a dated trigger.**
> *(RECOMMENDATION, NOT A RULING. Adopting it is an "amend the plan".)*

**Stage A — ratify the practice** (all of Option 1). Normalize the provenance vocabulary, adopt
the tier · provenance · confidence · gate-status citation form, codify residual attachment, and
stand up the consumer registry from §1. Nothing changes value; nothing is re-litigated.

**Stage B — add the corroboration axis** (Option 2's C0–C3 and the D0–D5 threshold table), under
the no-re-litigation clause, migrated lazily with no sweep.

**Stage C — the computed ladder** (Option 3, **additive form only**), **deferred behind a
trigger**: the earlier of (i) the first post-cutover decision that needs a D3-or-higher ruling, or
(ii) **2026-11-30** — deliberately the same date B3's detector trigger already carries, so the two
code-lane dependencies land together rather than twice.

**Why 2 and not 1.** Andy asked for scoring beyond tiers and gates. Option 1 delivers no scoring —
it delivers vocabulary. Vocabulary is necessary and is Stage A, but on its own it answers a
different question than the one asked.

**Why 2 and not 3 now.** Option 3 is a code deliverable competing directly with Day-0, its
aggressive form re-opens an overruled verdict's scoring basis, and it is the only option that can
loosen a gate. Its good idea — a per-decision admissibility position — is fully available as a
*table* in Option 2 and only becomes expensive when it becomes *computed*. Take the table now,
buy the computation when there is a decision that needs it.

**Why 2 at all — the strongest argument for it is that the project already built both halves.**
The tier × confidence citation form was invented independently in `baseline-forensic-2026-08-07.md`
because the author needed it and it was not there. The residual-with-reopen-condition object was
invented independently for C12 and worked well enough that propagating it *without* the residual
became a named defect. **Option 2 is not a new system; it is the two things this project already
does under pressure, written down, normalized, and given a threshold table so they bite at
decision points rather than at whoever remembers.** That is the lowest-risk way to add a real
second dimension, and it is why the migration story can be "nothing moves" rather than "here is
the sweep."

**What Option 2 does NOT fix, stated so it is not discovered later.** §4-I's 0–100 score stays
uncomputed (S-6). The A–K ↔ G1–G6 map stays unbuilt (§10 item 3). The `<FILL>` blanks stay blank
(§10 item 4). T3.4's 30–40% haircut band stays a range (§10 item 2's remainder). Instance
profitability still appears in no gate (§10 item 6). **Five of the seven §10 items survive this
recommendation.** A redesign that claimed to close them all would be claiming more than a
vocabulary-and-threshold change can deliver.

---

## 6. DECISION — ANDY register

Every item here changes a decision. None is an evidence-backed correction, so none is applicable
under `CLAUDE.md` §5's direct-application path. Nothing below was applied.

| # | Decision | Surface it would move |
|---|---|---|
| **DA-1** | **Adopt any option at all**, and which — 1, 2 (rec), 3-additive, or none | `evidence-standards.md` (gated end to end) |
| **DA-2** | Whether the bracket vocabulary is **ratified** as the provenance axis or **retired** in favour of C0–C3 (recommendation: ratified — retiring it orphans 342 citations) | `evidence-standards.md` §2.3; 29 surfaces by reference |
| **DA-3** | **The retired ≥15-condor gate still printed by `report.py:141` / `STATUS.md:17`** — remove it, or reverse §5's retirement. Required under every option including "adopt none" | `scripts/report.py`, `STATUS.md` |
| **DA-4** | Rename the detector's **Tier S/C**, the counterfactual **cost tiers**, and **Build tiers 0–2** to clear the §1.3 collisions | `daily-loop-spec.md` §5, §7, §11 — a spec |
| **DA-5** | Is §4-I's **0–100 score** ever computed, or formally marked **dormant** with its 9/100 preserved as the audit record? | `evidence-standards.md` §4-I |
| **DA-6** | **T3.4's 30–40% haircut → one number, or structure-dependent** (§10 item 2's open remainder; a redesign should not leave it) | `evidence-standards.md` §4.5 |
| **DA-7** | **§10 item 5 — what IS admissible at n=0.** Option 2's D0–D3 rows are a proposed answer; whether "B1 was never a gate on build/sizing decisions" is a **clarification or a loosening** must be declared either way, per the locking clause | `evidence-standards.md` §10; `build-plan.md` §5 if the wording moves (🔒 frozen) |
| **DA-8** | Whether the **A–K ↔ G1–G6 map** (§10 item 3) is in scope for this redesign or stays open | `evidence-standards.md` §3, §10 |
| **DA-9** | The **`<FILL>` blanks** — RoE `$` cap (board G4) and the four in `rules-of-engagement.md` (audit H3). Permanent-pending until someone writes a number | `rules-of-engagement.md` (archive REWRITE), `scripts/report.py` |
| **DA-10** | Whether **instance profitability** enters a gate (§10 item 6) — the project's own most clarifying metric, in no gate | `evidence-standards.md` §5 or §4 |

**Not in this register, deliberately:** §10 item 7's optional reconsideration of custody
separation and independent go-live authority. It is Andy's to open; this proposal does not argue
it in either direction, and §7 below is why.

---

## 7. Preservation clause — §1 and §9.2 carry verbatim under every option

Restated at the end because it is the constraint most likely to be eroded by a migration step.

1. **§1's ADOPTED / OVERRULED table** — kill-IC **overruled** (with its recorded reason, including
   that the 94%-vs-36% band was *not decision-grade*), the QQQ-Fortress automatic-kill
   **overruled**, custody separation and independent go-live authority **DECLINED** — is a
   **record of decisions already made**. It is carried **verbatim**, with its wording, its table
   form and its citations intact.
2. **§9.2's 2026-07-31 correction** — that *"third-party switch"* meant the **go-live switch held
   by a third party**, not a platform change; that go-live authority **stays with Andy**; that the
   substitutes are external review of `rules-of-engagement.md` plus the pre-registration
   discipline; and the stated-plainly paragraph explaining why §7's *fired in code, without a
   human in the loop* is load-bearing rather than a nicety — is carried **verbatim**, including
   its reopen trigger.
3. **Neither is scored.** No tier, no corroboration cell, no ladder position, no decision class and
   no threshold is ever attached to either. They are not claims about the world; they are the
   record of what was decided about claims.
4. **No migration step touches them.** Not the lazy re-tag, not the normalization pass, not the
   consumer-registry walk. If any adopted text would move a word of §1 or §9.2, that alone is
   grounds to reject the adopted text.
5. **The audit's locking clause is carried with them**, and it binds the redesign: a gate may be
   made stricter and may not be loosened silently. Options 1 and 2 loosen nothing. Option 3's one
   loosening risk is DA-7 and is declared, not buried.

---

## 8. Verification appendix

**Method.** Every quoted phrase in this document was asserted byte-exact against the **device
file** by `device_bash` `grep -cF`, count stated below. No quote was taken from a staged copy
(`CLAUDE.md` §9.1a). No file other than this one was written. No OA surface, no browser, no git.

**Asserts (file · pattern · count):**

```
baseline-forensic-2026-08-07.md  `evidence-standards.md` §2.1 note 4                       1
baseline-forensic-2026-08-07.md  Confidence is not a tier and must not be cited            1
evidence-standards.md            THESE CRITERIA ARE LOCKED                                 1
evidence-standards.md            Do not reinstate a 15-condor bar.                         1
evidence-standards.md            3. ~~The "separate, weaker gate" for T3 evidence …~~      1
evidence-standards.md            Nothing anywhere maps audit A–K onto board G1–G6.         1
evidence-standards.md            The default state of any project that has not yet …       1
STATUS.md                        Go-live gate (≥15 clean post-fix condor trades)           1   (line 17)
scripts/report.py                Go-live gate (≥15 clean post-fix condor trades)           1   (line 141)
state.md                         A discharge propagated without its residual is worse …    1
track-b-arms-spec.md             without its residual converts an [UNCORROBORATED] …       1
research-loop-spec.md            Treat as `[FIRST-HAND, UNCORROBORATED]`.                  1
daily-loop-spec.md               **Tier C (needs `data/bots_config_v2.csv`):**             1
daily-loop-spec.md               ## 11. Build tiers                                        1
ic-trailing-stop-backtest.md     T1-Control                                                4
CLAUDE.md                        `data/oa_facts.csv` fact ID with its                      1   (line 87)
evidence-standards.md            §2.1 numbered notes present                               3   (not 4)
evidence-standards.md            "almost none" (interim admissibility)                     1   (line 505)
```

**Counts (device, 2026-08-08):**

```
docs/ bracket-tag instances (class E)                          342
data/oa_facts.csv facts                                      1,548   tier: DOCUMENTED 1,401 · DOCS-SILENT 147
T1–T5 consumer files (class A)                                  10
audit gate A–K consumer files (class B)                          8
board gate G1–G6 consumer files (class C)                        4
gate T3 consumer files (class D)                                 6
class E surfaces (25 docs + 2 scripts + 2 captures)              29
grep 'gate [A-K]' over scripts/                                   0   (System I is not implemented)
```

**Files read in full or in cited sections this session, sha256 at read time:**

```
5f21c134dbc1ed63…  docs/evidence-standards.md          (READ ONLY — NOT EDITED)
```

*Remaining files were read via targeted `sed`/`grep` and are cited by their asserted patterns and
line numbers above rather than by hash.*

---

*Prepared 2026-08-08. **Nothing in this document has been ruled, applied or propagated.**
`docs/evidence-standards.md` is unmodified. The next act is Andy's: rule DA-1, and DA-3 regardless.*
