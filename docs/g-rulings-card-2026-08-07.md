# G-RULINGS CARD — 2026-08-07

*Written 2026-08-07 (early). **This card presents; it does not re-derive.** Every statistic below is
quoted from `docs/comparative-machinery-spec.md` (914 lines, sha256
`d26a3960a860a2667f0641748cfb3e4989c0bfd4fad347a171ad0613cf61c3dc`, on-device verified 2026-08-07)
or from the source document named on the line. No number here was recomputed and none is new.*

**What this is.** The spec's §8 is a 16-item ruling queue, G-1…G-16, presented flat. This card
groups them by **when the ruling has to happen**, so the ones that change tomorrow morning's build
are ruled first and the rest can wait.

**What this is not.** It applies nothing. It edits no existing document. It authorises no build, no
switch-on and no OA edit. `CLAUDE.md` §5 keeps every item below **gated** — each needs an explicit
"amend the plan."

**Standing context, so no item below is read as urgent when it is not.** The working ledger is
**EMPTY — n=0** (`data/ledger_meta.json`: `"ledger_start": "2099-01-01"`, `"export_rows": 0`,
`"n_trades_condors": 0`; read on device 2026-08-07). Under the spec's refusal **R-1** the engine
**refuses to run at all** at this state, so **no Group C ruling can be exercised before Day-0.**
Group A and Group B are different: they change text and configuration that gets stamped *before*
the ledger exists.

---

## RULING SHEET — copy, fill, return

```
RULING SHEET  ·  G-1…G-16  ·  2026-08-07
Source: docs/comparative-machinery-spec.md §8, sha256 d26a3960…cf61c3dc

── A. CHANGES WHAT GETS BUILT / STAMPED TOMORROW MORNING — rule these first ──
G-1   exit_rows.csv capture surface           [ AUTHORIZE | DECLINE | DEFER ]  AUTHORIZE, conditional on U-1 positive (Trades list renders per-row pricing mode + memo); reverts to HOLD if U-1 negative. Ruled Andy 2026-08-06.
G-5   PR-19 (SL200): gate conjunct (c)        [ DISAPPLY | ACCEPT-NO-GATE | DROP-ARM ]  DISAPPLY — the deliberate parallel to CF-11; with (a) inert (G-6), PR-19's gate reduces to conjunct (b) alone — chosen, not arrived at. Ruled Andy 2026-08-06.
G-13  PR-19 (SL200): degeneracy criterion     [ RESPEC | REPLACE-EQUIV | ACCEPT-AS-IS ]  REPLACE-EQUIV — TOST equivalence test on mean paired ΔR vs Ride, band ±0.015R (Andy-signed 2026-08-06 as the R-3 minimum-effect margin), evaluated once at the stamped gate-eval date; strikes the 40-day-window rule as unfireable (≈1.2 expected hits vs 20 required). Ruled Andy 2026-08-06.
G-7   GATE EVAL DATE, PR-14…PR-20             [ STAMP = Day-0 + 6 months (relational; resolves to calendar at Day-0); interim look at n=60 | DEFER ]  STAMP. Ruled Andy 2026-08-06.
        └ and add the field to pre-registration-ledger.md §2 template? [ YES | NO ]  YES. Ruled Andy 2026-08-06.

── B. GATES ARM-B2 (PR-22) SIGNING ──────────────────────────────────────────
G-1   see above — head of this group too
G-11  PR-21/PR-22 in the greenfield family?   [ IN | SEPARATE | DEFER ]  ______
G-9   BONFERRONI_K                            [ 6 | 5 | 9 | CENSUS | DEFER ]  ______
G-10  Bonferroni → joint day-bootstrap max-T? [ SWITCH | KEEP | DEFER ]  ______
G-8   n≥60 absolute kill vs the gate          [ SEQUENCE+CS | KEEP | DEFER ]  ______

── C. ANALYSIS / PUBLICATION ONLY — every one safe past the downgrade ───────
G-2   Matched-day predicate                   [ M7 | M6 | DEFER ]  ______
G-3   "exactly one condor per arm per day"    [ CONFIRM | REJECT | DEFER ]  ______
G-4   X-1 group reading of R-7                [ CONFIRM | ROW-WISE | ANY-EXPIRED | DEFER ]  ______
G-6   +0.015R on a fire-rate-diluted mean     [ STANDS | RESCALE | DEFER ]  ______
G-12  PR-16 worst-condor test                 [ RESPEC | ADVISORY-ONLY | ACCEPT | DEFER ]  ______
G-14  <D100> calendar / unit / C10            [ DEFER-TO-DAY-0 | OTHER ]  ______
G-15  put-breached / call-not-breached        [ PER-SIDE | EITHER | BOTH | DEFER ]  ______
G-16  n_matched_days ≥ 20 emission floor      [ 20 | ______ | DEFER ]  ______

Signed .......................................  Date ..................
```

---

# GROUP A — ⚡ CHANGES WHAT GETS BUILT OR STAMPED TOMORROW MORNING

*Four items. Three of them (G-5, G-13, G-7) touch **PR-19 / SL200** directly. G-1 changes what
tomorrow's build has to stamp into every arm's exit bundle. Everything in this group is cheaper to
rule before the build than after, because a post-build change moves the arm's config hash and
`pre-registration-ledger.md` §7 item 1 fills that hash **from the bot's own capture** at signing.*

---

## ⚡ A1 · G-1 — Authorise `data/exit_rows.csv`, the exit-attribution capture surface

**Forcing fact.** The 26-column OA export carries no exit-reason field; `tags` is bot-level and set
at open. So nothing in any named input says *which mechanic closed this position*.
`pre-registration-ledger.md` §2 rule 2, verbatim:

> *"A criterion needing evidence nobody collects is not a criterion."*

The spec drafted a close-time + MFE/MAE proxy and **rejected it outright** (§1.4), on five grounds
each verified against the folder: 15:44 is a dead constant (the C8 ruling removed the object S-4
gated it on); the proxy classifies PR-22's own 15:45 mechanic as NOT FIRED on every day; the export
timezone is unverified (open check D3); the ITM limb needs the memo and the SmartPricing mode,
neither of which is exported (open check D4); and MFE/MAE **censor at the trigger**, so a threshold
test resolves on the sign of the slippage, which is monotone in `d_i` — selection on the outcome.

**Options.**
1. **AUTHORIZE** — one capture step per trading day, reading each position's Trades list into
   `data/exit_rows.csv` per §1.4's schema.
2. **DECLINE** — Layer 2 stays `BLOCKED`, permanently.
3. **DEFER** — same as decline until it is revisited; the arms accrue days with no attribution
   record, and the record cannot be reconstructed retroactively.

**Recommendation — AUTHORIZE, after the 5-minute verification in §Unverified below.**
Five declared criteria across all seven greenfield arms plus PR-22's K2 are unfireable without it,
and one of them — PR-20's *"no profit-taking fill on ≥ 2 consecutive days on which it held a
position → RED"* — is, in the spec's words, *"the fleet's only forward exit-engine detector"*, i.e.
the instrument built specifically to catch the failure that ran six invisible sessions in v1.
DECLINE is a coherent choice, but it should be made knowing that it makes the Canary's slot largely
decorative and leaves `pre-registration-ledger.md` §7 item 3 permanently open for Layer 2.

**Unblocks:** GATE-CM conjunct (c) · PR-14's inverted liveness · PR-18/PR-19 stop-row liveness ·
PR-20's PT-fill detector · PR-22's K2 · CF-1's own publication precondition — which today no ΔR in
this family meets.
**Forecloses if declined:** every Layer-2 criterion reports `BLOCKED` forever (refusal R-9, never
`PASS`), and §7 item 3 closes for Layer 1 only.

> ### ⚡ WHY THIS ONE IS IN GROUP A — it changes what tomorrow's build stamps.
> §1.4's schema makes `pricing_mode` the discriminator for §6.2 Rule 1. But
> `greenfield-family-spec.md` §6.1 currently assigns **`speedy` to Profit Taking AND `speedy` to
> the 15:50 Expiration exit**, and leaves the rest as, verbatim:
> `| Trailing / Touch / Stop Loss | Exit Option | non-Market, exact control per Phase-0 check C3 |`
> — i.e. **unstamped**. If G-1 is AUTHORIZED, the exit-pricing sub-fields the build stamps tomorrow
> should be chosen **distinct per mechanic**, and recorded. Doing it tomorrow costs nothing; doing
> it after signing moves every affected arm's config hash and re-opens `pre-registration-ledger.md`
> §7 item 1. **This is a reading of §1.4 + §6.1, not a ruled fact — it is flagged, not asserted.**

---

## ⚡ A2 · G-5 — PR-19 / SL200: disapply gate conjunct (c), or accept an unreachable gate

**Forcing fact.** GATE-CM is conjunctive and conjunct (c) is an exact two-sided binomial sign test
on the **fired** subpopulation. The spec's arithmetic: at `K = 6` the test can reach significance
only if `n_fired ≥ 8`, all signed the same way (`2 · 0.5^8 = 0.0078125 ≤ 0.008333`; at
`n_fired = 7`, `2 · 0.5^7 = 0.015625 > 0.008333`). PR-19's hypothesis is that it **rarely fires** —
`hedge-research.md` §2.1, quoted inside the entry: *"Above ~200% is effectively no-stop."*

This is CF-11's defect one layer up. CF-11 already disapplied the **liveness** rule on this arm for
exactly this reason — greenfield §9, verbatim: the draft's version *"would have switched the arm off
precisely when it was CONFIRMING itself"* — and the same asymmetry was reintroduced in the PASS
gate, by inheritance rather than by decision.

**Options.**
1. **DISAPPLY (c) on PR-19**, recorded as the deliberate parallel to CF-11.
2. **ACCEPT-NO-GATE** — PR-19 keeps a kill criterion and has no reachable PASS gate; it can be
   killed but never confirmed.
3. **DROP-ARM** — don't build SL200; the slot and the Bonferroni term go back.

**Recommendation — DISAPPLY (option 1), with one thing stated plainly on the record.** It is the
identical move CF-11 already made on the identical arm for the identical reason, so it is a
consistency fix rather than a new concession. **But** under §2.5 conjunct (a) is inert (see C4/G-6),
so disapplying (c) reduces PR-19's gate to **conjunct (b) alone** — a single bootstrap CI. That may
be the right answer for an arm whose whole hypothesis is a null, and it should be *chosen*, not
arrived at.

**Unblocks:** PR-19 can pass its gate at all.
**Forecloses:** option 2 means the arm's only reachable disposition is death, which interacts badly
with G-13 below (its only retirement rule can't fire either) — read A2 and A3 together.

---

## ⚡ A3 · G-13 — PR-19 / SL200: the degeneracy criterion cannot fire

**Read this one with A2. With liveness disapplied by design, degeneracy is PR-19's *only*
retirement rule.**

**Forcing fact.** The criterion, verbatim from `greenfield-family-spec.md` §9:

> *"if this arm's per-condor R is within ±0.005R of the Ride control's on ≥ 20 of any 40 consecutive
> MATCHED days, AND its stop-loss row count over that window is 0, the arm carries no information
> and is retired."*

Three separate defects, per spec §4:
- **Not computable** — the second limb needs a stop-row count, i.e. I-5 (G-1).
- **Not well-posed** — *"any 40 consecutive matched days"* is a scan over overlapping windows
  (N−39 windows sharing 39 days each), with no declared start date, no cadence and no correction;
  a rolling scan is also repeated evaluation, which `research-loop-spec.md` §10a item 2 forbids
  (*"No nightly gate evaluation"*). And "consecutive" is undefined — matched-day index, or calendar.
- **Cannot fire** — at the family's own declared SD(R) ≈ 0.30 and ρ ≈ 0.90 the paired daily SD is
  `0.30·√0.20 ≈ 0.134R`, so `P(|d| ≤ 0.005) ≈ 0.030` and the expected count in a 40-day window is
  **≈1.2 against a requirement of 20** — ANDed to a limb (zero stop rows) that is near-certain for
  SL200 by hypothesis. Impossible ∧ near-certain = never fires.

CF-11's status line reads **"FIXED — degeneracy rewritten with a tolerance and a config-backed
second condition."** It is not fixed; the rewrite exchanged one unfireable rule for another.

**Options.**
1. **RESPEC** — keep the shape, size the tolerance against the family's own paired SD (0.134R, not
   0.005R), declare a start date and a single evaluation cadence.
2. **REPLACE-EQUIV** — replace it with an equivalence test (e.g. TOST on mean `d` against a declared
   equivalence band) evaluated **once**, at the stamped gate-eval date.
3. **ACCEPT-AS-IS** — SL200 ships with `degeneracy_fireable: false` and, given A2, effectively no
   retirement rule.

**Recommendation — REPLACE-EQUIV (option 2).** It fixes all three defects at once: an equivalence
test is computable from Layer 1 alone (no I-5 dependency), it is evaluated once so it does not
collide with §10a item 2, and it is well-posed. It also asks the arm's actual question — *does SL200
collapse to Ride* — as a hypothesis rather than as a hit-count. **It requires you to declare an
equivalence band, and this card does not supply one**: that is a new margin, so it is a signature,
not a calculation. The spec's paired daily SD of **0.134R** is the scale to set it against.

**Unblocks:** PR-19 gets a retirement rule that can actually fire, and the arm's second declared
question becomes answerable.
**Forecloses if accepted as-is:** the arm can only ever be killed by the Exp(R)<0 criterion or the
family-level VOID — it can never be retired for being uninformative, which is the specific failure
its hypothesis predicts.

---

## ⚡ A4 · G-7 — Stamp a `GATE EVAL DATE` for PR-14…PR-20

**Cheapest item on the sheet: one date, plus one template field.**

**Forcing fact.** `research-loop-spec.md` §10a item 2: the gate is evaluated ONCE, at the
pre-declared n, *"on a date written into `pre-registration-ledger.md` BEFORE n reaches 100."*
`track-b-arms-spec.md` §11 item 5, verbatim: *"`pre-registration-ledger.md` §2's template has
**no GATE EVALUATION DATE field**, which §10a item 2 now requires before n reaches 100."*
PR-21 and PR-22 carry one voluntarily; **PR-14…PR-20 have none.**

Two consequences. The engine's refusal **R-5** emits **no verdict at all** for an arm without a
stamped date — descriptive numbers forever, for all seven greenfield arms including PR-19. And
ruling 5's package part 3 (the no-influence rule) is anchored on *"that arm's own pre-declared gate
date"*, which for five of the seven does not exist.

**Options.**
1. **STAMP** a date into all seven entries now, and add the field to §2's template in the same pass.
2. **DEFER** to Day-0 signing.

**Recommendation — STAMP now, at the REVIEW DATE §9 already declares** (`Day-0 + 6 months; interim
at n = 60`), unless you want the gate evaluation separated from the review. n is 0 today, so
stamping now is trivially compliant with §10a item 2; deferring to Day-0 is also compliant, but
Day-0 is a busy surface and this is the kind of field that gets missed. Adding the field to the §2
template is the same edit either way, and `track-b-arms-spec.md` §11 item 5 has been open since
2026-08-04.

**Note on form:** Day-0's calendar date is not fixed (`ledger_start` is still the `2099-01-01`
sentinel), so the stamp is relational — *"Day-0 + 6 months"* — and resolves to a calendar date at
Day-0. That satisfies §10a item 2, which requires the date be written before n reaches 100, not
before Day-0.

**Unblocks:** any verdict at all for PR-14…PR-20; the no-influence rule gets its anchor.
**Forecloses if deferred:** nothing permanently — but until it is stamped the entire greenfield
family is descriptive-only by construction.

---

# GROUP B — 🔒 GATES ARM-B2 (PR-22 `GF-QQQ-IC-Exp1545`) SIGNING

*ARM-B2 is the arm `track-b-arms-spec.md` §7 nominates to be **built first** — value stampable at
Day-0, one differing field, earliest first observation Day-0. Its signing runs through
`pre-registration-ledger.md` §7 item 3: **"Kill criterion re-read against the daily loop"** — does
the loop actually produce that number? For PR-22 the answer today is: **K1 yes, K2 no, and the
level K1 is read at is unruled.** These four items are that answer.*

---

## 🔒 B1 · G-1 — see A1. Head of this group.

PR-22's **K2** is, per spec §4: *zero `speedy` close rows at ~15:45 across 10 consecutive matched
days*, which needs `row_type == expiration_exit` **and** `pricing_mode == speedy` **and** an
`exit_ts`. All three live only in I-5. **Without G-1, PR-22 cannot be signed with K2 in it** — the
criterion fails §2 rule 2 on its face.

Second dependency, not a G-item and already open: **D3**, the export/backstop timezone. K2 contains
a wall-clock predicate (~15:45) and no file states the export's timezone; a one-hour DST error moves
every close across the cut. **K2 is not signable until D3 is answered either.**

---

## 🔒 B2 · G-11 — Are PR-21/PR-22 statistically inside the greenfield family?

**Forcing fact.** The spec's draft claimed they sit outside the greenfield Bonferroni family *"per
ruling S-1"*, and **withdrew the claim as a category error**. S-1 is a **bot-slot allocation**
ruling — `track-b-arms-spec.md` §3.3, verbatim: *"the seven family bots are `build-plan.md` §2D
fresh builds; Track B's 8 slots are yours"*. It says nothing about error rates. Both Track B arms
declare **`GF-QQQ-IC-Ride` as their control** — same control, same underlying, same shared entry
automations, same day-series, same 1-lot sizing.

**Options.** IN (one family, one K) · SEPARATE (own family, own K, no pooled alpha — recorded as a
carried limitation, the same shape §10a already uses for the two engines) · DEFER.

**Recommendation — IN.** By every definition except the slot budget it is one family, and the
conservative choice is also the honest one at a *signing* decision: signing PR-22 while the engine
carries `k_basis: "DECLARED — statistical family not ruled"` means signing a criterion whose alpha
level is unstated. Cost of IN: K rises and power falls further — which is precisely the argument for
ruling B4 (G-10) in the same sitting.

**Unblocks:** PR-22's K1 has a defined level. **Forecloses:** SEPARATE is defensible, but it should
carry §10a's honesty line verbatim rather than an implication of independence.

---

## 🔒 B3 · G-9 — `BONFERRONI_K`: 6, 5, or 9

**Forcing fact.** K is wrong in **both directions at once**. Six is declared, but PR-20 (Canary)
carries no comparative criterion, so only **five** comparative tests run — K=6 over-corrects by
~2.4 % on z. That is the small error. Enumerating the decisions actually taken against the single
`GF-QQQ-IC-Ride` control across the named documents gives **nine**: PR-15 ΔR · PR-16 ΔR · PR-17 ΔR ·
PR-18 ΔR · PR-19 ΔR · PR-16's second test (worst-condor-R vs Ride) · PR-19's degeneracy equivalence
test vs Ride · PR-21 K1 vs Ride · PR-22 K1 vs Ride — plus PR-21's secondary vs GF-SL100.
**K=6 is under-corrected by roughly 1.8× against the family that actually exists.**

**Options.** 6 (ship the declared value) · 5 (tests that run) · 9 (decisions against the control) ·
CENSUS (K = whatever `family_census` enumerates at signing) · DEFER.

**Recommendation — rule G-9 and G-10 (B4) together, and if G-10 goes to max-T, G-9 is moot.**
If Bonferroni stands, **9** is the defensible number and CENSUS is the maintainable one — but note
what raising K does: §2.5's family half-width is already **±0.0354R at K=6, n=100**, against
**+0.0150R** as the largest effect this program has ever measured (SL75, n=1,254 positions). Raising
K raises that bar further. **Fixing the under-correction by raising K makes an already-unreachable
gate less reachable; that is the argument for B4, not against B3.**

**Unblocks:** the interval PR-22's K1 reads. **Forecloses:** shipping 6 unruled means the family's
alpha is wrong by ~1.8× in the anti-conservative direction and nothing on the run says so — the
engine's `family_census` block makes it visible but does not fix it.

---

## 🔒 B4 · G-10 — Replace Bonferroni-across-6 with a joint day-bootstrap max-T?

**Forcing fact.** The two engines' corrections are arguably **swapped relative to where power is
scarce.** Bonferroni is conservative under strong positive dependence — and this family has one
control, one day-series and one entry signal, i.e. maximal dependence — while max-T absorbs exactly
that dependence and is applied to Track A, which has the looser sample constraint
(`research-loop-spec.md` §10a item 3, verbatim: *"the max-T null absorbs the inter-variant
correlation, so **no Bonferroni term is applied**"*). A joint day-bootstrap with max-T across arms
would recover most of the 2.638 → ~2.3 z gap at no cost. `greenfield-family-spec.md` Phase C step
C4's *"Bonferroni across the 6"* is a **declared analysis convention**, so this is gated.

**Options.** SWITCH to joint day-bootstrap max-T · KEEP Bonferroni · DEFER.

**Recommendation — SWITCH.** It is the same correction Track A already uses, on a family with
*more* dependence to absorb, in an engine the spec describes as having *"no power to spare"*. It
also dissolves G-9: under max-T the number of tests enters through the resampling null rather than
through a hand-set K, so the 6-vs-5-vs-9 problem stops being a decision. Cost: it is a change to a
declared convention, and it must be declared **before** any data exists — which is today, and stops
being true at Day-0.

**Unblocks:** a materially reachable gate; G-9 becomes moot.
**Forecloses if deferred past Day-0:** switching the correction after data exists is a
post-hoc analysis change, and the spec's whole sequencing discipline (§2.6) exists to prevent that
class of move. **This is the one Group-B item that is genuinely cheaper today than in a month.**

---

## 🔒 B5 · G-8 — The absolute n≥60 kill is an interim look on the gate's own vector

**Forcing fact.** Every PR-14…PR-19 entry carries *"CI entirely below 0 at n ≥ 60"* and both Track B
K1s carry *"bootstrap 95 % CI entirely below 0 at n >= 60 matched condors."* These are **fixed-n
interim looks on the same statistic** the gate reads at n=100 — which `research-loop-spec.md` §10a
item 4 forbids in terms: *"Any nightly monitoring of the gate statistic must use an **always-valid
confidence sequence**, not a fixed-n CI."*

Labelling them separately does not decouple them. The kill is **one-sided**, so it removes arms
whose first-60 draw came in low, and the arms surviving to the gate are conditioned on a favourable
interim draw — that inflates the pass rate under the null. Seven arms × an uncorrected 95 % absolute
CI at n=60 also gives a family-wise kill rate far above 5 %, and the kill is reachable **40 days
before** the gate. This is CF-2's finding, still live: *"so the criteria would fire on the winners."*

**Options.**
1. **SEQUENCE+CS** — the n≥60 read is emitted only as an always-valid confidence sequence (which the
   engine already does by construction, §2.6), and the absolute kill is sequenced so it cannot
   retire an arm before its gate-eval date, except via the family-level and sentinel criteria which
   are execution-integrity rules and are unaffected.
2. **KEEP** — the PR text stands and the conflict with §10a item 4 is carried.
3. **DEFER.**

**Recommendation — SEQUENCE+CS.** The engine already refuses to do the forbidden thing; what is
left is the **pre-registration text**, which still says the forbidden thing, and it is that text
Andy signs. Cost of the fix is bounded: an arm with a genuinely bad first 60 days stays on longer, at
1 lot, on a paper account at Day-0. **This is the clearest null-looks-like-pass path in the design**
and it sits inside the exact sentence being signed.

**Unblocks:** PR-22's K1 (and every greenfield arm's kill line) becomes signable without contradicting
a signed spec.
**Forecloses if kept:** §10a item 4 is contradicted by the text of every entry that cites it.

---

# GROUP C — 🕓 ANALYSIS / PUBLICATION ONLY — **every item here is safe past the 14:52 downgrade**

*Stated explicitly, per item, because the point of the grouping is that none of these blocks the
build, the signing, or Day-0 readiness. And there is a structural backstop: with
`ledger_start == "2099-01-01"` and `export_rows == 0`, refusal **R-1** means the engine cannot run,
so **not one of these rulings can be exercised until the ledger has post-cutover rows.** Each item
below names its own latest-safe moment, which is never tomorrow.*

---

## 🕓 C1 · G-2 — Matched-day predicate: `M7` (all seven) or `M6` (six comparative arms)

**SAFE TO WAIT.** Latest safe moment: **before Day-0 signing** — Phase C step C4 requires the §8.4
matched-day definition be *"written into all seven pre-registrations before signing, not after."*

**Forcing fact.** `greenfield-family-spec.md` §8.4, verbatim: *"A trading day is **matched** iff
**all seven arms opened a condor on it.**"* That includes the Canary, whose own entry says
*"this bot is NOT run for edge. Its P/L is expected to be ~flat and is not evidence about anything"*
and whose kill line reads **`NONE ON P/L`**. Requiring its fill to declare a day matched costs `n`
for zero inferential gain and makes the one bot with no scientific role a single point of failure
over all five real comparisons.

⚠️ **One correction to how the spec states this.** Spec §1.5's G-2 box says PR-20 *"carries a
2-consecutive-day RED that switches it **off**"*. The source entry says the alert is *"→ RED,
escalated in the brief as a candidate exit-engine failure"* — **it does not state a switch-off.**
The argument survives without that limb: `M7` halts whenever the Canary simply fails to fill, for
any reason, and its own text says a no-fill day is *"AMBIGUOUS between 'the exit engine died' and
'the spread widened by a cent'"* with an **UNMEASURED** false-negative rate.

**Recommendation — `M6` for the gate, `|M7|` printed alongside.** The Canary is an instrument, not a
comparison; conditioning five real comparisons on an instrument's daily fill buys nothing and can
cost everything. Changing the declared predicate is a decision, which is why it is here.

---

## 🕓 C2 · G-3 — Confirm "exactly one condor per arm per day"

**SAFE TO WAIT.** Latest safe moment: **before Day-0 signing** (same C4 clause as C1).

**Forcing fact.** §8.4 says only *"opened a condor on it"*. The spec **tightens** this to exactly
one, dropping any day where an arm shows two included condors and logging it as an anomaly. That
tightening is what makes the day-level mean and the condor-level mean the same number (§2.4
rationale 2) — so it is load-bearing, not cosmetic — and it is a third departure from R-3 where
`greenfield-family-spec.md` §12 row 16 names only two.

**Recommendation — CONFIRM.** The shared entry automation already carries a position-tag re-entry
gate (check C7, PASS: *"Bot opened a position with call side today"* → NO → Open), so two condors on
one arm on one day is a **finding**, not a sample. Averaging it away would hide exactly the failure
the gate exists to catch.

---

## 🕓 C3 · G-4 — Confirm X-1's group-level reading of R-7 (`expired`)

**SAFE TO WAIT.** Latest safe moment: **before the engine's first real run** (which cannot be before
Day-0 + the emission floor).

**Forcing fact.** R-7 (`research-loop-spec.md` §10) stratifies `expired`: *"excluded from every count
and from the PT family's comparison."* But `status` is a **per-row** field (154 expired / 1,232
closed of 1,386 rows on the v1 capture, `oa-export-schema.md` §6) and the unit here is a **group**.
Both naive readings bias `d_i` in opposite directions, at **arm-dependent** rates:
- **Row-wise** drops the expired leg, deleting a positive P/L contribution while keeping the tested
  side's loss — and `single_sided` is computed at open, so the resulting half-condor is **not
  flagged** and enters silently.
- **Group-wise-if-any** drops the whole condor whenever either leg expired — but under the C8 ruling
  the untested side running to its own expiry **is the designed behaviour** of Touch0, SL100, SL200
  and both Track B arms.

**Recommendation — CONFIRM X-1 as written** (exclude only groups where *every* row is expired). It
is the only reading that neither mangles a condor nor deletes an arm's signature outcome. Note it is
an **interpretation of a signed ruling**, not a quotation of one — which is why it is gated. The
engine prints `n_all_expired`, `n_mixed_status` and `n_all_closed` **per arm** every run whichever
way it is ruled, so the incidence asymmetry stays visible.

---

## 🕓 C4 · G-6 — Does +0.015R stand as a bar on a fire-rate-diluted mean?

**SAFE TO WAIT — and largely moot, which is worth knowing before spending time on it.**
Latest safe moment: **before the first gate evaluation**.

**Forcing fact, two limbs.** R-3 calibrated +0.015R as *"the arithmetic ceiling on a PT50→PT70 move
at the fleet's median credit/risk of 0.070 is 0.014R per fired position"* — a **PT**-derived
ceiling, now used as the materiality bar for three **stop/touch** arms that can move R by ±1.0 in a
day. And R-3's figure is **per fired position**, while conjunct (a) is a mean **diluted by
non-firing days**: a single 0.015R bar means ≈0.025R per fired condor for a 60 %-firing arm and
≈0.30R per fired condor for a 5 %-firing arm — **~12× harsher on the hedge arms than on the
profit-target arms**, and nothing in R-3's text sets the fire rate that decides it.

**Why it is moot.** §2.5: conjunct (b) at K=6, n=100 requires an observed mean(d) ≥ **+0.035R**,
which is 2.4× conjunct (a)'s +0.015R. **Every sample that satisfies (b) satisfies (a) automatically
— (a) can never bind.** The operative bar is set by the CI width, not by the calibrated margin.

**Recommendation — STANDS, unchanged, with `fire_rate` published beside (a) always.** Re-scaling the
margin to this family's credit would be a **new margin needing a new signature**, for a conjunct
that does no work at this n and K. Rule it "stands, and recorded as inert" and move on. If B4 (G-10)
switches to max-T the half-width falls and (a) may start to bind — at which point this item becomes
live again, and that is the trigger to revisit it.

---

## 🕓 C5 · G-12 — PR-16's worst-condor test is a coin flip

**SAFE TO WAIT.** Latest safe moment: **before PR-16 reaches n = 60**, which is the criterion's own
trigger — months away.

**Forcing fact.** The criterion, verbatim from `greenfield-family-spec.md` §9: *"worst-condor-R worse
than the Ride control's at n ≥ 60 → the 'no new risk' claim is refuted and the arm is retired."*
That compares two **sample minima** — an extreme order statistic — with no CI, no tolerance, no
correction and no membership in the Bonferroni family. Under a null of exchangeable arms,
`P(min_X < min_C) ≈ 0.5`. **The Trail arm is retired on a coin flip, and the retirement is worded as
a refuted claim.**

**Recommendation — RESPEC to a tail quantile with a CI** (the natural repair), or **ADVISORY-ONLY**
if you want to keep a blunt tripwire without letting it retire an arm on its own. ACCEPT is
defensible only if it is *chosen* as a deliberately blunt tripwire — the current wording promotes a
coin flip to a refutation.

---

## 🕓 C6 · G-14 — `<D100>`: calendar basis, per-condor vs per-side, and C10

**SAFE TO WAIT — and it cannot be settled tomorrow even if you wanted to.** Latest safe moment:
**before ARM-B1 is stamped**, which is Day-0 + 90 at the earliest.

**Forcing fact.** Four defects, two of which change its value: "trading days" needs an exchange
calendar and none of the named inputs is one; the formula is stated over **condors** while `dstop`
is carried **per side** (a condor-level median stamped into a per-spread control is ≈2× the intended
level — `track-b-arms-spec.md` names this as *"the D-6 units failure one layer up"*); **C10 is
ASSIGNED, not answered** (`dstop` per contract / position / leg), and the spec's own words are
*"assignment is not an answer"*; and an estimated constant is stamped once and held with its
estimation error never propagated.

**Recommendation — DEFER-TO-DAY-0. No ruling needed tomorrow.** C10 needs a **behavioural read
against a known contract count** on a live account, which does not exist yet; ARM-B1 *"is NOT AN ARM
until both close"* regardless of how G-14 is ruled. The engine already emits `d100_candidate` with
`basis: "days-with-rows, NOT trading days"` and `unit: "UNRESOLVED — C10"` and **refuses to stamp**,
which is the correct behaviour under every option.

---

## 🕓 C7 · G-15 — The put-breached / call-not-breached case

**SAFE TO WAIT.** Latest safe moment: **with G-1** — the breach test only becomes live once I-5
exists, so if G-1 is declined this item never arises.

**Forcing fact.** Under the C8 ruling the **exit mechanic's unit is the SPREAD**, while the
**analysis unit is the CONDOR**, and `mfe_pct`/`mae_pct` are **per row**. So "the declared threshold
was reached" is a per-spread indicator classifying a per-condor `d_i`, **with no rule anywhere in
the folder for the case where the put side breached and the call side did not.** Separately,
`mfe_pct`/`mae_pct` are on the **credit** basis while `d_i` is on the **risk** basis — the bases
match for PR-18/PR-19's breach test, but every emission has to name which one it is on.

**Recommendation — PER-SIDE.** The C8 ruling already made the spread the exit unit for early exits;
running the liveness indicator on the side that actually breached is the reading consistent with the
mechanic. The engine emits `breach_put`, `breach_call` and `breach_either` separately either way and
takes no verdict from them until this is ruled.

---

## 🕓 C8 · G-16 — The `n_matched_days ≥ 20` emission floor

**SAFE TO WAIT.** Latest safe moment: **before the engine's first run.** Lowest-stakes item on the
sheet.

**Forcing fact.** 20 is a **proposal**, not a ruling. It mirrors R-4's start condition in form —
R-4's own threshold (`n ≥ 30` post-cutover closed positions fleet-wide) was **ruled**, and this one
was assumed. Below the floor the engine prints a single suppressed-output line, so the stage is
exercised without publishing noise.

**Recommendation — confirm 20, or set your own number.** It carries no inferential content; it is a
noise-suppression threshold. It is on the sheet only because R-4's analogue was ruled rather than
assumed, and the folder's convention is that an assumed threshold gets a signature or gets flagged.

---

# UNVERIFIED FACTS THIS CARD'S RECOMMENDATIONS DEPEND ON

*Per the brief: where a recommendation rests on something not yet observed, it is named here with
the check that would settle it, rather than asserted above.*

| # | The unverified fact | Whose recommendation depends on it | How to verify |
|---|---|---|---|
| **U-1** | **That a position's Trades list renders a per-row pricing mode and a memo at all.** §1.4's schema takes `pricing_mode` and `memo` from the Trades list, and §6.2 Rule 2 is *"provisional until it is read"* (open check **D4**) | **G-1 (A1)** — the whole schema, and therefore the AUTHORIZE recommendation | Open **one existing position** on any live v1 bot → Trades list → read whether a pricing/mode column and a memo field render **per exit row**. ~5 minutes, no greenfield object needed. If they do not render, the schema degrades to `(exit_ts, fill_price)` and `row_type` becomes hand-assigned — which is a materially different capture cost and should change the ruling |
| **U-2** | **That the `sm*` exit-pricing sub-fields can be set to *distinct* values per mechanic.** C3 (2026-08-05) established every exit mechanic has an `sm*` sibling and read `smdstop` defaulting to `{"smart":"normal"}`; the **enumerated value list per sub-field is not recorded in the folder** | **G-1's build-time consequence** (the ⚡ box in A1) — the recommendation to stamp distinct modes tomorrow | Open one arm's exit-bundle editor at build time and **enumerate the `sm*` picker's values**, the same way the `stoploss` picker was enumerated for C1. Record what was read; do not infer from the default |
| **U-3** | **That the export timezone is what a 15:45 predicate assumes.** No file states it; DST is an open pre-switch-on check (**D3**) | **G-1 / B1** — PR-22's K2 is a wall-clock predicate | D3's existing procedure. Until answered, **no wall-clock predicate is safe**, and K2 is not signable regardless of G-1 |
| **U-4** | **That `itmlive` is `market`.** Read **`auto`** on 2026-08-06; **D2** sets it to `market` before any capital is live. Under `auto`, an ITM-expiring position's P/L is *"estimated from the underlying close price — a modeled number, not a fill"* and lands in the ledger with no flag | **Every verdict** — refusal **R-6** blocks all of them while `pnl_may_be_modelled` is true | The D2 step already on the Day-0 list: set `itmlive = market`, then re-observe the value from OA per `CLAUDE.md` §5's two-layer check |
| **U-5** | **The `family_census` count of nine.** It is the spec's enumeration of declared decisions against the Ride control, presented here as written, **not recomputed by this card** | **G-9 (B3)** — the "9" option and the ~1.8× figure | Re-enumerate against `greenfield-family-spec.md` §9 and `track-b-arms-spec.md` §5–§6 at signing; the engine emits the census on every run so it is checkable then |

**Three non-G dependencies, already open and already on other lists:** **D2** (`itmlive = market`) ·
**D3** (export/backstop timezone) · **D4** (whether the ITM action appears in a Trades list and under
what label). **D3 and D4 both gate G-1's value; D2 gates every verdict.** None of them is ruled here.

---

# WHAT THIS CARD DOES NOT DO

- It **applies nothing.** No file was edited to produce it; it is the only file written.
- It **re-derives no statistic.** Every figure is quoted from the source named on its line.
- It **does not touch PR text, the build plan, or any spec.** Each item above is a decision under
  `CLAUDE.md` §5 and stays gated until an explicit "amend the plan."
- It **does not discharge `pre-registration-ledger.md` §7 item 3.** The spec discharges it for
  Layer 1 and explicitly not for Layer 2; **G-1 decides whether Layer 2 can ever close.**
