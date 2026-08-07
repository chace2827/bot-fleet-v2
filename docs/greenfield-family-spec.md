# Greenfield family — build spec

*Written 2026-08-04. The design document Phase 4's fresh builds are built from, mechanically.
It **implements** `build-plan.md` §2D and §5; it does not amend them. Nothing here has been
built, and no OA surface was touched in the session that wrote it.*

> ### Date note, once
> The task that commissioned this file states "Today is 2026-08-06". The device clock and the
> session environment both read **2026-08-04**. Every date stamped in this file is the
> verifiable one. If the build runs on a later day, the `<date>` literals in §10 are stale —
> re-stamp them at the head of the build session, not mid-ritual (the pilot card's rule).

> ### 📝 CORRECTED 2026-08-04 (later same day) — `research-loop-spec.md` was AMENDED after this
> ### file was drafted. Four passages updated: §3.1's fixed-$ row, §11.2 CF-2, §12 rows 9 and 10.
> Andy's rulings **R-1** and **R-3** on `docs/research-loop-review-2026-08-04.md` landed after this
> spec staged its copy of that document. **R-1 signed the fixed-$ rungs as MEDIAN-CREDIT DOLLAR
> rungs and REJECTED the RISK basis** — this file had recorded the rung basis as an open unsigned
> amendment. **R-3 replaced the 0.10R margin** with a three-part test. ⭐ **The margin collision
> this spec raised is RESOLVED** — see §12 row 10. Verified against the device file
> (`research-loop-spec.md`, 296 lines, sha256 `4fe4b3e5…1d314176`), quotes asserted single-match.

> ### ⚠️ THIS IS THE POST-ADVERSARIAL-REVIEW TEXT. READ §11 BEFORE BUILDING.
> Two adversarial subagents attacked the finished draft and returned **10 FATAL** and **24
> MATERIAL** objections between them. Roughly two-thirds are fixed in the text above; the rest are
> **carried as named limitations**, because they are properties of the platform or of the
> question, not of the wording. **Six blocking Phase-0 checks now exist that the draft did not
> have, and one of them — C0a — can stop the architecture outright.** Three of the seven arms are
> **not arms yet** under `hedge-research.md` §5.2's own definition, because their platform
> primitives are unconfirmed. None of that is hidden in an appendix: §11 is the record and §12 is
> what remains open.

> ### ✅ RULING GATE — CLEARED
> `docs/decision-memo-2026-08-04.md` was read first. **D-1 is RULED** (line 171: Option A,
> Exit-Options-SET as a Bot Input, with the G2 rider) and **Decision 4 is RULED** (line 548:
> Architecture E, share the entry automation, differ on exits). Decisions 5, 6, 7 and D-3, D-4
> are also ruled. The four secondary slots the memo marks `NOT RULED` are named where they
> bite (§12). This spec therefore proceeds.

---

## 0. What this document is, in six lines

Seven fresh bots, built as **one matched family**, not two families.

Every bot shares **the same entry automations, the same backstop, the same sibling-close, the
same bot settings, and the same sizing** — shared as Library objects, so they are identical *by
construction* rather than by repetition. Each bot differs in **exactly one mechanic**: the value
of a per-bot input whose type is the whole Exit-Options bundle (one per side, asserted equal).

The "greenfield IC family" and the "rebuilt hedge tournament arms" of `build-plan.md` §2D are
**two views of this one family**, not two builds. That is what makes the hedge arms matched to a
no-hedge control without spending extra slots on one.

---

## 1. The mechanism, stated before the bots

This is the part a build session must understand before it clicks anything. Everything else is
consequence.

### 1.1 The input chain — where the arm variable actually lives

`oa-platform-reference.md` §5.2, [DOCUMENTED]:

> *"the decision input is linked to the Automation Input, which is linked to the Bot Input – and
> the Bot Input value takes priority."*

So: **one shared Open Position action → one Automation Input → N Bot Inputs, one per arm.**

```
   Fortress-family ScannerA-PutSpread      (ONE Library automation object, shared by all 7 bots)
      └─ Open Short Put Spread
           └─ Exit Options  =  🔗 automation input  GF_EXITS_PUT
                                    (ScannerB carries its own GF_EXITS_CALL — see §4.1)
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
   bot GF-Ride                 bot GF-PT50                 bot GF-Touch0     …
   Bot Input GF_EXITS_* =      Bot Input GF_EXITS_* =      Bot Input GF_EXITS_* =
   {time exit only}            {time exit + PT 50%}        {time exit + Touch $0}
   (put and call, equal)       (put and call, equal)       (put and call, equal)
```

The exit configuration is the **only** object that varies. Entry logic, strike selection,
sizing, credit floor, entry pricing, the Range075 filter, the backstop and the sibling-close all
live in shared objects and cannot drift apart without an edit that changes every arm at once.

**Why this is the design and not a per-arm copy:** `hedge-research.md` §6 — `HedgeA-S1` ≈
`HedgeD` ≈ `HedgeTest`, 73/73/70 identical positions across three bots, invisible for four
months — was produced by independently hand-set bots with **no inputs at all**. Hand-setting is
the pathogen. A shared definition plus one differing variable makes a three-way identity
arithmetically impossible.

### 1.2 ⛔ The G2 rider — binding on every capture surface in this spec

`state.md` (pilot part-4 block), and the rider attached to the D-1 ruling:

> the action stores a **REFERENCE**, not values —
> `{"type":"input","input":"IN…","text":"<label>","oldValue":{…}}`

**Consequence, and it is the single most dangerous thing in this document:** a capture-diff that
reads the Open Position action returns **identical for every arm**, because every arm's action
holds the same reference to the same automation input. It will look like a clean pass. It proves
nothing.

**Binding rules:**

1. `bots_config_v2.csv`, the capture-diff, the drift detector and the arm-matching proof of §8
   **must read the BOT INPUT OBJECT's value** — the per-bot end of the chain — and decode it.
2. **`oldValue` is never config.** It is a pre-link snapshot and goes stale the moment the link
   is made. Any parser that falls back to `oldValue` when the input object is missing is
   reporting history as state.
3. The diff **decodes the payload; it never compares rendered labels.** Finding N-4: OA
   re-serialises an `exits` blob on save even when nothing changed — the pilot's label drifted
   `"Profits: 50%, …"` → `"Profit: 50%, …"` with the numeric payload byte-identical
   (`^^0.5|0.01^$0` before and after). A differing line does not entail a differing value, and
   an identical value does not entail an identical line.
4. Any parser keying on the string `"fast"` for SmartPricing **silently misses it** — the
   internal value is `speedy` (§7, first-hand).

### 1.3 The sentinel — and ⛔ the half of §5.2 it CANNOT discharge

> 📝 **RULED 2026-08-06 (Andy, final) — SENTINEL-SL1 IS ABANDONED, STRUCK.** Phase A found it
> literally inexpressible (picker-floor evidence below), not just weak. Detection moves to
> config-level instead of the runtime signature this section designs. **See §1.3a, appended at
> the end of this section, for the ruled replacement.** Everything below is history — the design
> that was tried and why it failed — left standing, not corrected in place.

§5.2's failure mode: *"The Default Values are not used UNLESS the Automation/Bot Input link is
broken"*, and **a broken link does not error.** It silently reverts to the stale Default and
keeps trading.

**§5.2's mitigation, quoted with the clause that matters:**

> *"make each Default Value a distinctive sentinel (`-999`) **that a decision explicitly tests
> for and refuses to trade on**."*

⛔ **The refusal half is NOT EXPRESSIBLE for a bundle-typed input, and this spec does not pretend
otherwise.** Exit Options are not a decision family (§5.1), and §9 row 3 established there is no
🔗 on any individual exit field — *"Inside the Default Value editor, `i.fa-link` count is 0"* —
so **no decision node can read this input's value**. There is no pre-trade refusal available. Any
design that claims one would be a substitution at a platform limit performed on the very rule
written to prevent them.

**What is available is a post-hoc signature, and it is strictly weaker:**

> **`GF_EXITS` Automation-Input Default Value = `SENTINEL-SL1`** — an Exit-Options bundle whose
> only content is **Stop Loss % = 1**.

A broken link then produces an unmistakable, same-day, harmless signature: that arm's positions
close within minutes of opening, every day, on the first adverse tick. It is loud in the ledger
and cheap at 1 lot. **Stop Loss, not Profit Taking**, because a low PT is behaviourally
indistinguishable from the Canary arm (PR-20), and a sentinel that looks like a legitimate arm is
not a sentinel.

⛔ **Do NOT use an EMPTY bundle as the sentinel**, even though G1 confirmed the server accepts
one: an empty bundle is behaviourally indistinguishable from a legitimate no-management arm — the
silent, plausible-looking fallback §5.2 exists to prevent.

> ### ⛔ THE RESIDUAL HOLE, STATED RATHER THAN PAPERED OVER
> When the link breaks, the **Bot Input object still holds the arm's correct value** — the
> runtime falls back to the Default, the stored config does not. So §8.2's read (which is
> mandated to read exactly that object) records the intended bundle and **passes**. §8.3's
> assert A4 therefore catches only a *typo* — someone stamping the sentinel as an arm value —
> **not the broken link it is named for.**
>
> **The only detector for a broken link is behavioural: the SL1 signature in the Trades list and
> the ledger, one trading day after it happens.** That is a genuine uncovered hole between the
> break and the next day's brief, it is a property of the platform's silent-fallback design and
> not of this spec, and it is why the §9 SENTINEL criterion is written as a *ledger* criterion
> rather than a config one.

> ### §1.3a — AMENDED 2026-08-06 (Andy, final ruling). Default Value = NONE; detection is config-level.
>
> **(a) SENTINEL-SL1 is struck — it is not expressible.** [FIRST-HAND 2026-08-06, live Exit Options
> `stoploss` modal, Phase A build session]: the picker floors at **`-5% of credit` (`0.05`)**, 42
> entries, no free-text path — `-5%` … `-100%`(`=1`) … `-500%`(`=5`). `stoploss: 1`, the value
> `SENTINEL-SL1` calls for, is **exactly `GF-SL100`'s own value** — behaviourally identical to a
> real arm, which this section's own text forbids by name (*"a sentinel that looks like a
> legitimate arm is not a sentinel"*). The nearest expressible value, `0.05`, is a **spec change**
> to what a sentinel means, not a build detail, and is not adopted here. No runtime sentinel is
> built. Every `GF_EXITS_*` Automation Input's **Default Value = `NONE`.**
>
> **(b) New assert — §8.3 A9, BOUND + NON-EMPTY, replaces A4's job.** A4 (*"no arm's stored bundle
> equals `SENTINEL-SL1`"*) is now vacuous — nothing is ever stamped `SENTINEL-SL1` because it does
> not exist — and is struck as moot, not deleted (§8.3). **A9: every arm's `GF_EXITS_PUT` /
> `GF_EXITS_CALL` bot input is BOUND (an input object is attached, `oldValue`/link state aside) and
> NON-EMPTY (`decoded(value) != {}`), checked before any arm's `AUTOMATIONS` toggle goes ON at
> Day-0.** This is unambiguous because **no arm legitimately runs empty exits** — `Ride` (PR-14) is
> time-exit-only via its own dedicated close row, not via an empty exits bundle — so BOUND
> non-empty is a clean necessary condition for every one of the seven arms, checkable from
> `bots_config_v2.csv` with no behavioural read required.
>
> **(c) Residual cap, recorded rather than hidden.** An arm whose exit link is unbound or empty is
> **not left riding unmanaged**: `GF-Backstop-1552-FlatClose` (§4.2, attached to every bot at Day-0)
> flat-closes it at 15:52 regardless. The failure mode a broken/empty exit link produces is *"rides
> to the 15:52 backstop instead of its own exit policy that day"* — bounded, loud in the ledger
> (an anomalous 15:52 close on a day with no early exit), and not a silent open-ended hold. This is
> weaker than same-day detection but it is not the unbounded risk an un-backstopped design would
> carry, and A9 catches the config-level version before Day-0 rather than after a live miss.
>
> Applied 2026-08-06 by Andy's explicit final ruling on F-4 (superseding the earlier probe-first
> answer — Default Value left at NONE, sentinel unimplemented, flagged for a ruling — which is now
> resolved by this amendment). `state.md` and `session-log.md` updated to match.

### 1.4 Where G1's empty-bundle result is and is not used

G1 came back **YES, server-confirmed** — an empty bundle saves and survives a hard reload — and
`state.md` records this as meaning "the `ride` arm IS expressible". **This spec deliberately does
not use it.**

An empty bundle would give the ride arm no time exit, so the ride arm would differ from every
other arm in **two** things: the absence of a management trigger *and* the absence of a 15:50
time exit. Its positions would live two minutes longer than every other arm's and would exit
through a **Market** backstop while the other arms exit through **SmartPricing** — a pricing
confound layered on an exposure confound, in the one arm that is supposed to be the control.

Instead: **every arm's bundle carries the identical time exit**, and the arms differ by the
presence and identity of one management trigger on top of it. The ride arm is the base; each
other arm is base + exactly one trigger. G1 remains recorded as an available escape hatch and is
not relied upon.

**This is a spec choice, not a ruling, and Andy may overrule it.** If overruled, §11's
confound-A objection applies in full and must be written into PR-14's pre-registration.

---

## 2. Scope decision — QQQ, and the reason, because it is not free

`build-plan.md` §2 does not name an underlying for the greenfield family. It archives the SPX
Fortress arms saying `Roles superseded — the greenfield family supplies the new control and A/B
arms` and archives the old QQQ Range075 experiments as `Superseded by the greenfield family`.
Both lines are satisfied by either choice, so the choice is this spec's to make and to justify.

**Specified: QQQ.** Three reasons, in order of weight:

1. **The 15:52 flat-close backstop is a QQQ mechanic.** `hedge-research.md` §11:
   `The 3:50 PM flat rule is QQQ-only. It backfires on SPX cash settlement.` The backstop is
   load-bearing in every arm of this family. On SPX it would pay to close condors that would
   have settled worthless.
2. **The entry tree already exists and is verified.** The pilot's ScannerA tree was read at the
   value layer on 2026-08-04 and is reproduced verbatim in §4. Reusing a verified tree is the
   single largest risk reduction available to this build.
3. **Cross-readability.** `QQQ-IC-0DTE-Fortress` and `-NoPT50` are QQQ clones in the same
   pillar; the family's ride arm and the Fortress clones become legible against each other.

**The cost, stated:** QQQ is a physically-settled ETF, so the family carries assignment risk that
an SPX family would not. That risk is entirely governed by the ITM Position Action — see §7,
which is why that section is a hard gate rather than a note.

**If Andy prefers SPX:** it is not a one-line change. The backstop mechanic must be re-designed
(reason 1), the strike width moves $2 → $5 (`hedge-research.md` §11), and the sizing arithmetic
in §5.4 changes with it. Do not substitute the underlying at build time — that is the HedgeD
error shape.

---

## 3. The roster — seven bots, and how they fit `build-plan.md` §2D's arithmetic

§2D allows **5–7 fresh builds** total, covering the greenfield IC family (4–6 bots), the rebuilt
hedge tournament arms, and the optional canary. Four + hedge arms + canary does not obviously fit
inside seven. It fits here because the hedge arms are arms of the same family, sharing the same
control.

| # | Bot name | Role | Arm variable (the whole bundle) | PR |
|---|---|---|---|---|
| 1 | `GF-QQQ-IC-Ride` | **control** | time exit only | PR-14 |
| 2 | `GF-QQQ-IC-PT50` | experiment | time exit + Profit Taking % 50 | PR-15 |
| 3 | `GF-QQQ-IC-Trail` | experiment | time exit + Trailing Stop | PR-16 |
| 4 | `GF-QQQ-IC-Touch0` | experiment | time exit + Touch $0 | PR-17 |
| 5 | `GF-QQQ-IC-SL100` | experiment (hedge arm) | time exit + Stop Loss 100 | PR-18 |
| 6 | `GF-QQQ-IC-SL200` | experiment (hedge arm) | time exit + Stop Loss 200 | PR-19 |
| 7 | `GF-QQQ-IC-Canary` | instrument | time exit + Profit Taking % 5 | PR-20 |

**Total fresh = 7.** At §2D's ceiling, with no remainder. `build-plan.md` §2's accounting —
35 = 20 archived + 2 deleted + 4 cloned + 9 untouched — is untouched; end state is 20 active
bots (4 clones + 9 untouched + 7 fresh), inside §2D's `≈18–20`.

> ⚠️ **Finding, not an amendment.** §2D's `Greenfield IC family (4–6 bots)` reads most naturally
> as 4–6 bots *before* the hedge arms and the canary, which would exceed the 5–7 total in the
> same paragraph. This spec resolves the tension by treating the IC family and the hedge arms as
> one matched set (4 IC arms + 2 hedge arms = 6, inside "4–6"), plus the canary. **If Andy reads
> §2D as requiring separate families, the arithmetic needs an "amend the plan" and this spec's
> §3 is what changes.** Flagged, not decided here.

**Arm IDs.** `pre-registration-ledger.md` §8 item 1 holds PR-14…PR-17 for the IC family and
`PR-18 onward` for the hedge arms, with the literals unstamped until the counts are decided.
The literals above are **PROPOSED**, consistent with those ranges, and become final when Andy
fixes the count.

### 3.1 What is deliberately NOT an arm

| Excluded | Why | Authority |
|---|---|---|
| **`Conditional` / sustained-touch** | The platform cannot express time persistence at all. The only build path is a ~10-rung tag ladder that consumes the whole 1-minute scan budget and **fails safe-looking at every rung**. | §11; `hedge-research.md` §7, §7.1; `pre-registration-ledger.md` §6 warning |
| **Defang** (close shorts ~$0.05, longs ride) | `True "defang" as a single action` is **NOT NATIVE** — multi-leg workaround required. A workaround here would be an undocumented substitution at a platform limit. | §11 row 5 |
| **SL130** (Pearce) | Fits the slot budget nowhere in wave 1. Queued as the first wave-2 arm if a slot frees. | §3's ceiling |
| **Fixed-$ stop rungs** (`dstop`) | 📝 **CORRECTED 2026-08-04** — the draft said the rung basis was "under an unsigned amendment (RISK-basis, not credit-basis)". **It is now SIGNED.** Ruling **R-1** fixed the rungs at **1.00× and 1.50× the bot's trailing-90-day MEDIAN credit, in dollars**, and **REJECTED the RISK basis** outright: *"0.50×risk lands at ~720% of credit at the fleet's median credit/risk of 0.070 (n=1,254), beyond the no-stop boundary."* `DSTOP_100` / `DSTOP_150` are members of the **frozen 12-variant Track A set**. Excluded here for the unchanged reason — **they are Track A's, and building them as family arms would double-test them across two engines whose error rates pool nowhere** (§11-CF10). | `research-loop-spec.md` §3 as amended 2026-08-04 (R-1), §10 |
| ~~**Armed trailing stop** ("arm @ 40%, then trail 15%")~~ | ⭐ **FALSIFIED AND REINSTATED 2026-08-06 by Phase-0 check C2.** OA implements the armed trail as a **native Exit-Options primitive**: `tstop` opens a sub-form with **`target`** ("Activate at __ % of credit") and **`trail`** ("Close on __ % pullback"). §11 rows 4 and 6 bound what **decision nodes** can express; they do not bound what a native exit primitive does internally — and `maxtrail` ("Pullback is more than __ % from high") is direct evidence the platform tracks a high-water mark natively. **RULED 2026-08-06: PR-16 is re-scoped to the ARMED trail, `target`=40 / `trail`=15.** Rows 4 and 6 themselves are untouched by this. Original exclusion, now struck: ~~A two-stage mid-trade state change. **Excluded by the same two §11 rows §3.1 uses against stop-tightening.** PR-16 is scoped to a plain, always-on trail instead.~~ | §11 rows 4, 6 — **misapplied here**; `phase0_C2.txt` |
| **VIX filter** | Redundant once Range075 is present; validated. | `hedge-research.md` §11 |
| **Intraday stop-tightening schedule** | Requires mid-trade state change; no primitive. Backtest-only (`hedge-research.md` §9 item 3). | §11 rows 4, 6 |

---

## 4. The shared objects — built once, attached to all seven

Four Library automations. Every one of them is identical across all arms **because it is the same
object**, not because it was copied correctly.

### 4.1 `GF-ScannerA-PutSpread` — the shared entry automation, put side

Reproduced from the pilot's verified tree (`session-log.md` 2026-08-03 part 2, read at the value
layer from `input.value` / hidden-field payloads, not `innerText`), with the two changes the
rulings force.

```
Loop QQQ
 └─ Current market time is after 1:30pm                                    [General decision]
     └─ YES → Current market time is before 2:00pm            ⭐ ADDED      [General decision]
         └─ YES → Symbol change % > -0.75 since previous close              [Symbol decision]
             └─ YES → Symbol change % < 0.75 since previous close           [Symbol decision]
                 └─ YES → Bot opened a position with tag `put side` today  ⚠️ C7
                     └─ NO → Open QQQ Short Put Spread
```

> ⭐ **The 2:00pm upper bound is ADDED to the pilot's tree, deliberately, and it is a spec change.**
> The pilot's tree has no upper bound, so the scanner re-evaluates every minute until the
> automations window closes at 15:55. Two consequences the family cannot carry:
> **(a) Range075 stops being a gap filter.** A day is excluded only if |Δ%| stays outside ±0.75%
> for the *whole* post-1:30 window. A day that opens −1.4% and mean-reverts to −0.6% at 14:40
> **passes and is entered late** — and those are the high-realised-vol days the filter exists to
> avoid. `state.md` records the fleet paying for exactly this: *6/17 opened +0.7%, passed the
> filter, Fortress entered 1:31 and ate −$7,530.*
> **(b) Late entries neutralise the arm variable.** A condor opened at 14:40 has ~70 minutes
> before the 15:50 exit; one opened at 13:31 has ~140. PT/Trail/SL/Touch can only differentiate
> inside that window, so on late-entry days **all seven arms converge toward Ride** — a dilution
> whose incidence is set by the tape rather than by design. The bound caps the time-to-exit
> spread at ~1.4×, not 4×.
> **Cost, accepted:** fewer qualifying days, which §11-C9's arithmetic already shows is the
> binding constraint on sample size. That is a smaller problem than an entry-time confounder.

`Open Short Put Spread` action:

| Field | Value | Note |
|---|---|---|
| Symbol | `QQQ` | carried in the automation, not the Symbols panel |
| Expiration | `exactly 0 days` | 0DTE |
| Short put | `0.75% below underlying price` | matches the champion structure |
| Long put | `$2.00 below short put leg` | $2-wide, most hedgeable on QQQ (`hedge-research.md` §11) |
| Size | **1 contract** — see §5.4 for the primitive and its fallback | ⚠️ Phase-0 check C4 |
| Minimum credit | `Mid price is between $0.08 – (no max)` | the pilot's live floor, carried |
| **Entry pricing** | **SmartPricing `normal`**, Final Price `pct` = `100` (the control's default) | ⛔ **CHANGED from the pilot's `Price: Market`** — Decision 5 |
| Exit Options | **🔗 automation input `GF_EXITS_PUT`** | the arm variable; §1.1. ScannerB carries `GF_EXITS_CALL` |
| Tag | `put side` | consumed by the re-entry gate above |

`GF-ScannerB-CallSpread` is the mirror image: short call `0.75% above underlying price`, long
call `$2.00 above short call leg`, tag `call side`, everything else identical.

> ### ⛔ TWO INPUTS, NOT ONE — corrected under review
> The draft of this spec said ScannerB carries *"the same `GF_EXITS` input"*. **That is almost
> certainly not expressible.** The object is an **Automation** Input; the one instance ever
> created (`IN178586615441261`) was scoped to a single automation's action, and OA's id
> namespaces are scope markers — §9 row 4 makes the point in the platform's own vocabulary:
> *"the id namespace: **`UI…`**, not `BOT…` or `RT…` — presets are **account-scoped** user
> objects, not bot- or automation-scoped."* Nothing establishes that an `IN…` object crosses
> automations. Two Library automations means **two** automation inputs, necessarily.
>
> **Specified: `GF_EXITS_PUT` on ScannerA, `GF_EXITS_CALL` on ScannerB**, each linking to a
> per-bot Bot Input of the same name. **Every arm therefore holds TWO exit variables, and they
> must be equal to each other.**
>
> ⛔ **This creates a failure mode the draft's diff was blind to:** a bot whose put side is set to
> Ride and whose call side is set to PT50 has two well-formed, non-identical, correctly-decoding
> bundles, and would have **passed** a cross-arm diff. §8.2 now carries an intra-arm equality
> test and §8.3 carries assert **A8** for exactly this. If Phase-0 check **C0b** shows one input
> *can* span both automations, collapse to a single `GF_EXITS` and A8 becomes trivially true —
> keep the assert either way.

> **Range075 — the primitive, named.** Range075 is built from **two Symbol-change-% decision
> nodes in this shared entry automation**. It is **not** an Exit-Options preset.
> `build-plan.md` §2D's phrase `Range075 as a preset` names a primitive that cannot express the
> mechanic: presets are an Exit Options object (§6.1) and Range075 is an entry decision
> (`hedge-research.md` §8: `implement as a symbol %-change decision, not a high-low range
> check`). This is memo finding **N-2**, and it is the same defect class as the `Conditional`
> correction of record. **The substance is stronger under Architecture E, not weaker:** carried
> once in the shared entry automation, Range075 is identical across arms by construction rather
> than by per-arm repetition. `build-plan.md` §2D is **not edited** — the wording correction
> requires Andy's "amend the plan"; draft text is in the memo, Decision 4 amendment (c).

> ⛔ **Entry pricing changed, and it is a spec change, not a carry-forward.** The pilot enters at
> `Price: Market` on both sides. Decision 5 is RULED — the Market-pricing ban extends to entries.
> No family bot enters at Market. Recorded there as a **MECHANISM decision, not an
> evidence-backed one** (n=1 position for the $5.05 figure, n=2 in the frozen fixture — below
> `CLAUDE.md` §4's T2 gate). **Accepted cost:** a limit entry that does not fill biases the
> sample toward tight-spread days. **Mitigation, required:** log non-fills so the bias is
> measurable rather than invisible (§8.4).

### 4.2 `GF-Backstop-1552-FlatClose` — the shared Events-class backstop

Built exactly as it was built and reload-verified on the pilot
(`Fortress-Backstop-1552-FlatClose`, automation id `RTfw5TkkCRF1785795329406099999991`):

```
Trigger   Repeating → Pattern → Market Time (EST) → Custom → 15:52
          Every week on Mon-Fri, 3:52pm EST · holidays = skip · no end date
          (commits as ntime=1552; the visible 5-minute grid is a convenience list, not the
          constraint — native <input type="time" min="09:31" max="15:55">, 1-minute step)
Tree      Positions loop (unrestricted) → Close Position
Action    Market · 100% · memo `1552 backstop flat close`
```

**Why the Events class and not an Exit Option:** §6, [DOCUMENTED] —
*"Exit Options always run, even if your automations inside a bot are turned off."* The inverse is
the point: v1's failure was Exit Options dead while automations ran, so a backstop living
*inside* Exit Options would have died with them. `0.008` = "8 minutes before" exists in the
Expiration dropdown, so a 15:52 Exit Option **was** expressible all along — the objection was
never impossibility, it is architectural, and the architecture is unchanged.

**Market pricing here is inside §7's carve-out** — `a hard end-of-day flat close, where fill
certainty beats fill quality`. Decision 6 keeps it. Do not "fix" it.

⚠️ **Two known unresolved properties:**

- **⛔ DST — and it is promoted to a FIRST-DAY observation, not a later one.** The saved trigger
  serialised `startDate 2026-08-03T20:52:00.000Z` = 15:52 at UTC−5 (EST), but Day-0 falls in
  **EDT (UTC−4)**, where that is **16:52 ET — after the close**. `ntime=1552` is the operative
  field and `startDate`'s time component may be a stamp only. **If the literal-EST reading is
  right the backstop never fires, on all seven arms at once, and the absence looks exactly like
  "nothing needed closing."** `itmpaper = market` does not cover it — §7 says so in its own
  words: *"`market` is not a substitute for the 15:52 backstop."* **Build order D6 is therefore
  ordered BEFORE the arms are switched on** (revised under review), observed on the first
  session-day the account is active.
- **Jitter.** *"no guarantee an automation will run exactly on the 15-minute marks."* The
  reference's own figure is *"an **8-minute buffer to the bell**"* — 15:52 → 16:00. The draft
  attributed that 8 minutes to the **15:59 Exit-Options window edge**, which is (a) 7 minutes,
  not 8, and (b) the wrong boundary: the backstop is an **Events-class automation**, so the
  Exit-Options window is not one of its bounds at all. Corrected. **Three windows exist and the
  reference forbids conflating them: scan cadence ends 15:45 · automations customizable to
  15:55 · Exit Options run to ~15:59.** The backstop's governing bound is the 15:55 automations
  cap, which 15:52 clears by three minutes.

### 4.3 `GF-SiblingClose` — the shared condor-close automation

> ### ⛔ RULED 2026-08-06 — BUILD WITHOUT SIBLING-CLOSE. C8's STOP was returned; the spec's own
> named fallback is TAKEN, on Andy's explicit ruling. **The spread, not the condor, is the unit for
> early exits.** Everything below is LEFT STANDING as the design that was specified and is now
> superseded — per this file's convention, and because §11 PE-5's fix is the thing that failed.
> **Cause:** the closed position is not an addressable referent in a `Position closed` automation —
> OA offers only `Lookup a position` (literal filters) and `Opened Position`, the latter explicitly
> *"Only available in automations scheduled with the 'position opened' trigger"*. Clauses 1 and 3
> (the Positions loop, the opened-today scope) are real; clause 2 is not expressible.
> Evidence: `data/captures/edit-verify/2026-08-06/phase0_C8.txt`; `session-log.md` 2026-08-06.
>
> **CONSEQUENCES, all of which change the build:**
> - **Phase A builds THREE shared automations, not four.** `GF-SiblingClose` is not built. Step
>   **A4 is struck**; the **A7** payload-hash baseline covers **three** objects; **B3** attaches three.
>   Post-Phase-A the Automation Library holds **4** rows (the 3 shared + `Defang-Mon-S2-StrikeTouch`),
>   not 5.
> - **The 15:44 gate is MOOT** — recorded, not deleted, because it is the record of a ruling (S-4).
> - **The arms are no longer close-both.** `Touch0` is **S1, not S2**; `PT50` is **PT50 per spread**,
>   not "PT50 on either side closes the condor"; `SL100`/`SL200` are **no longer wrapped in a
>   close-both exit**. All seven MECHANISM blocks are re-stamped below.
> - ⭐ **CF-4 is DISCHARGED, not carried** — the anchor-transfer defect it named was *caused by*
>   sibling-close. Without it, the untested side is left to decay and PR-18 **can** reach the
>   Breakeven shape its ★★★★★ anchor describes. See §4.3's CONSEQUENCE block and §12 row 15.
> - **A second leg left open by an early exit now closes at its own 15:50 Expiration exit**, or at
>   the 15:52 backstop. That is the accepted cost of the fallback and it is what makes the spread
>   the unit.

`build-plan.md` §8.1 item 3 and §5.4. An IC is two positions; closing "the whole condor"
requires an explicit mechanism, and in v1 this was an *emergent side effect* of a 2-minute
Cleanup monitor — unnamed, undocumented, load-bearing.

```
Trigger   Position closed
Tree      Positions loop (the bot's open positions)          ⭐ REQUIRED — supplies the target
           └─ Current market time is before 3:44pm            ⭐ AMENDED 2026-08-04 — see (c)
               └─ YES → position's side tag != the closed position's side tag   ⚠️ C8
                   └─ YES → position opened today                               ⚠️ C8
                       └─ YES → Close Position (SmartPricing `patient`, 100%,
                                                 memo `sibling close`)   ⭐ patient, not speedy
```

⭐ **Three corrections to the draft, all forced under review:**

**(a) The Positions loop is not optional — the draft omitted it.** The one automation in this
project that was actually built and reload-verified reads *"tree = **Positions loop
(unrestricted)** → Close Position"* (`state.md`, the 15:52 backstop). A bare `Close Position`
inside a `Position closed` automation has no stated referent — the position that triggered it is
already gone. The loop is what supplies the action a target.

**(b) ⛔ OA has no "sibling" relation.** §3: *"OA models **each spread as a separate position**."*
The pairing is a **project** construct (`trade_id` in the ledger), not a platform one. "Sibling
still open" must be built from **position-loop decisions on the side tag**, which is why the tree
above tests `side tag != the closed position's side tag` rather than naming a relation that does
not exist. **Whether that comparison and the "opened today" scope are real decision nodes is
Phase-0 check C8** — it is not assumed here. `oa-ops-runbook.md` §5 trap 7 is this exact failure:
*"A time gate that was never implemented — the v1 11:00 gate did not exist; 20+ sessions of entry
drift."*

**(c) The 3:44pm gate de-races the backstop AND the 15:45 exit class.** Without it: the 15:52 backstop's unrestricted
Positions loop closes leg 1 → that fires `Position closed` → sibling-close sees leg 2 still open
and issues a **SmartPricing** close on it **while the backstop's loop issues a Market close on
the same leg.** §4.2's redundant-position check is the only defence and the reference disclaims
it in the same breath: *"Note this did not prevent the 7/01 orphan loop."* Gating sibling-close
to before 15:44 removes the race entirely, at near-zero cost — after 15:50 the backstop closes both
legs anyway.

> ### 📝 AMENDED 2026-08-04 — gate moved 15:50 → 15:44. Ruled by Andy. Apply in PHASE A.
> **`before 3:50pm` was not tight enough, and the gap is a confound, not just an operational
> risk.** Found by the Track B task while specifying `GF-QQQ-IC-Exp1545` (ARM-B2), whose
> `expdays` = `0.015` closes both legs at ~**15:45** — which **is** before 15:50, so the gate does
> not exclude it. Leg 1 fills → `Position closed` fires → sibling-close finds leg 2 open, differing
> side tag, opened today, time < 15:50 → issues a `patient` close on leg 2 **while leg 2's own
> `speedy` Expiration order is still working** (N-6: an exit-option order stays live **two
> minutes**). That is the 7/01 orphan-loop shape reintroduced at 15:45 — and because it bites
> **that arm and not its Ride control**, it is a **mechanic difference between arm and control**,
> i.e. a confound in the one comparison the arm exists to make.
> *(Source: `docs/track-b-arms-spec.md` §6.6, which named the fix and correctly declined to apply
> it to a shared object in a spec that task could not amend.)*
>
> **Cost, stated:** on the five triggered greenfield arms, a trigger firing in **[15:44, 15:50)**
> now leaves the sibling open until its own 15:50 Expiration exit closes it — the condor still
> closes, at worst six minutes later, **with no orphan**. One minute of gate buys the removal of a
> whole race class for every current and future arm whose exit lands before 15:50.
>
> ⛔ **This edits a SHARED object, so it changes all seven arms at once.** It must be applied in
> **Phase A, before any arm is switched on** — never as a later edit — and it requires a **fresh
> A7 payload-hash baseline** (§8.3) plus re-verification of every attached arm. Applying it after
> Day-0 would splice two different experiments into one sample, which is precisely what A7 exists
> to detect.

⛔ **This is the highest-risk shared object in the family and it is §4.7's exact shape** — a
position-closed trigger that closes a position can re-trigger itself.

> ### ⛔ CORRECTION OF RECORD — the draft cited an interlock the platform says does not exist
> The draft's interlock 2 read: *"Bot daily position limit stays at 2. The docs name position and
> allocation limits as the designed anti-loop defence."* **That is false for this loop.** §3,
> quoted verbatim from `tools/bots/safeguards`:
>
> > *"**Position limits are for opening positions only; there is no limit on the amount of
> > closing positions.**"*
>
> and, same section: *"**There is no limit on closing.**"* The documented loop limits defend
> against is close→**open**→close (§4.7: *"an event could automatically open a position when
> another is closed"*). §4.3's mechanism is close→**close**. A limit of 2 constrains nothing on
> that path. The **allocation** limit is equally inert here (§5's corrected note): with
> `posLimit` = 2 and IC = 2 positions the bot can never hold more than one condor, so the
> position limit binds at ~17% of allocation, always, first.
>
> **Two of the three "mandatory interlocks" were one interlock and a procedural test.** The
> honest interlock set is now:

1. **Structural:** the tree gates on side-tag inequality **and** opened-today **and** before-15:50
   — three decision nodes, each of which must be confirmed to exist (C8) and each of which must
   be verified as *a real node* in build step A4, not assumed.
2. **Temporal:** the 3:44pm gate bounds the loop's lifetime to the trading day and removes the
   backstop race.
3. **Procedural:** **test on a dead bot first** — build-order step A4, before it is attached to
   any arm. This is now load-bearing rather than belt-and-braces, because the platform-level
   defence the draft leaned on is not there.

⚠️ **If C8 shows the side-tag or opened-today comparison is not expressible, STOP.** Do not
substitute position age (`open 30 minutes or more`) — that is the literal substitution that cost
−$15,376 (§11 correction of record). The named fallback is: **build the family without
sibling-close**, accept that the unit of account becomes the spread rather than the condor for
early exits, and re-stamp all seven MECHANISM blocks before build.

> ### 📝 SUPERSEDED 2026-08-06 BY THE C8 RULING — the whole block below is MOOT, and left standing.
> Sibling-close is **not built**. The arms are **not** close-both: `Touch0` is S1, `PT50` is per
> spread, and **`SL100`/`SL200` CAN now reach the Breakeven shape** their anchor describes, because
> the untested side is left to decay exactly as `hedge-research.md` §2 assumes. ⭐ **CF-4 is
> therefore DISCHARGED rather than carried** — it was an artefact of sibling-close, not of the
> structure. The text below is the analysis that made the case *for* carrying it, and it is the
> reason the ruling went the way it did; it is preserved, not deleted.
>
> ### ⛔ CONSEQUENCE — and the draft's claim that it "cannot confound" is WITHDRAWN
> With sibling-close on every arm, every arm is a **close-both (S2-shaped) family**.
> `GF-QQQ-IC-Touch0` is therefore S2, not S1. `GF-QQQ-IC-PT50` is "PT50 on either side closes the
> condor", not "PT50 per spread". **Each pre-registration says this in its MECHANISM block**,
> because the bare mechanic name would name something the bot is not running — the HedgeD rule.
>
> The draft then said it *"cannot confound the ranking … it changes what every arm means,
> equally."* **That is wrong and it is withdrawn. Identical treatment is not equal effect.**
> Sibling-close **never fires meaningfully on the Ride control** — both legs close at 15:50
> anyway — and **fires on every trigger event** on PT50, Trail, Touch0, SL100 and SL200. It is an
> **effect modifier**, not a constant.
>
> **Concretely, it breaks the ★★★★★ anchor PR-18 imports.** `hedge-research.md` §2 names it *"the
> **~100%-of-credit 'Breakeven' stop**"* — and the name *is* the mechanic. Put credit $15,
> stopped at 100% of credit ⇒ −$15 on that spread while the untested call side decays to zero ⇒
> the condor nets ≈ **$0**. That is why it is called Breakeven. With sibling-close, the call side
> is force-closed at its then-current mid the instant the put stops, and **the arm cannot reach
> breakeven by construction.** SL100 and SL200 are therefore biased **downward** relative to their
> published comparables by the forfeited untested-side decay.
>
> **This is not repaired by removing sibling-close from those arms** — that would break matching,
> which is worse. It is carried as a **named limitation on the transfer of the operator anchors**,
> written into PR-18 and PR-19, and recorded in §11 as surviving objection **CF-4**.

### 4.4 The exit bundles — per arm, the only thing that varies

Every bundle is expressed **only** in fields confirmed to exist on the live modal
(`oa-platform-reference.md` §6.1a, [FIRST-HAND 2026-08-04]).

**The common base, identical in all seven bundles:**

| # | UI label | Field | Value |
|---|---|---|---|
| 8 | Expiration | `expdays` | `0.01` (= 10 minutes before close = 15:50) |
| 8b | ↳ PRICING | `smexpdays` | **`speedy`** (SmartPricing Fast — ⛔ **not** `market`) |
| 11 | ☐ Wait at least 1 day to avoid pattern day trading | `chposLimitDay` | **unchecked** |
| 12 | ☐ Disable exit options if bid/ask exceeds $ | `chbidask` / `bidask` | **unchecked / empty** |
| 13 | ☐ Save as presets | `pretext` | see §4.5 |

⛔ **The Bid-Ask Guard stays OFF on every arm.** §6.3: while the spread exceeds the configured
width, Exit Options are **disabled** and high%/low% tracking **pauses**, with no error. On a
touch-class arm that is *"the worst-timed possible failure"* — a hedge that stops working exactly
when the market is fast. Off on all arms, identically, and recorded as a decision rather than a
default.

⛔ **Item 11 is the PDT checkbox.** Checked, it delays closes by ≥1 day, which on a 0DTE program
is total failure. Unchecked on every arm, and read back per bot in the §10 verification.

**Per-arm addition — exactly one trigger on top of the base:**

| Bot | Adds | Field | Value | Pricing |
|---|---|---|---|---|
| `GF-QQQ-IC-Ride` | — nothing — | — | — | — |
| `GF-QQQ-IC-PT50` | Profit Taking % | `profits` | `0.5` | `smprofits` = `speedy` |
| `GF-QQQ-IC-Trail` | Trailing Stop | `tstop` | ⚠️ **Phase-0 check C2** | ⚠️ C3 |
| `GF-QQQ-IC-Touch0` | Touch | `touch` | `$0` | ⚠️ C3 |
| `GF-QQQ-IC-SL100` | Stop Loss % | `stoploss` | `100` ⚠️ **C1** | ⚠️ C3 |
| `GF-QQQ-IC-SL200` | Stop Loss % | `stoploss` | `200` ⚠️ **C1** | ⚠️ C3 |
| `GF-QQQ-IC-Canary` | Profit Taking % | `profits` | `0.05` | `smprofits` = `speedy` |

**Touch $0, what it means, quoted rather than assumed** — §6.2, resolved 2026-08-03 from OA's own
published material: *"The new 'Touch' Exit Option references the underlying price relative to a
position's strike price(s)."* It fires when the underlying is `$X` or `X%` from in-the-money or
less; **`$0` exits on the first 1-minute evaluation at which the position is ITM.** ⚠️ *"The
moment"* is the draft's wording and it is **wrong**: Exit Options are *"evaluated every **1 market
minute**"* (§6) and §11 row 3 rules out *"Sub-second strike-touch with a latch — **NOT NATIVE.**
1-minute cadence at best."* On 0DTE QQQ a full minute past the strike is material to the very
quantity this arm is measured on, and the arm must be described as a **1-minute-sampled** touch
hedge, never as an instantaneous one. Each position's Touch references its own
strike, so "the challenged side" is expressed by the trigger's own semantics — no cross-leg
mechanic is required or implied. ⚠️ Whether a Touch on one spread can close its **sibling** is
unresolved; this spec **assumes not** and uses §4.3's mechanism, per §6.2's own instruction.

### 4.5 Presets — used, and what they are and are not doing

§9 check #4, answered 2026-08-04: one preset serves **both** Open Position actions across **two
different automations**; the `UI…` id namespace means presets are **account-scoped**. G3
confirmed a bundle input and a named preset **compose** on the same action. G4 confirmed **no
propagation** — presets are load-by-value, so editing a preset never reaches an attached action.

**Therefore:** presets are used here as a **build-time convenience only** — a way to load the
seven bundles without retyping them, reducing typo surface at the moment of stamping. They are
**not** a matching guarantee and are **not** cited as a proof leg anywhere in §8.

> §6.1: `**A preset makes the VALUES consistent, not the ATTACHMENT.**` And G4's no-propagation
> result means a per-arm preset gives **no ongoing guarantee at all** — the value is copied in
> once and thereafter drifts freely. The proof of matching is the decoded bot-input diff of §8,
> and nothing else.

**Naming convention, decided here because Decision 7 deferred it to this spec:**
`GF-<ARM>-EXITS` — `GF-RIDE-EXITS`, `GF-PT50-EXITS`, `GF-TRAIL-EXITS`, `GF-TOUCH0-EXITS`,
`GF-SL100-EXITS`, `GF-SL200-EXITS`, `GF-CANARY-EXITS`. ~~plus `GF-SENTINEL-SL1`~~ 📝 **STRUCK 2026-08-06 — not built, F-4 ruling (§1.3a).**
The residual test preset `TIER2-CHECK4-PUTSIDE` is **KEPT** (ruled 2026-08-04) and is now an
obvious non-member of this namespace, which is what Decision 7 item 1 wanted.
⚠️ **Whether a preset can be renamed at all was never observed.** Do not plan on renaming
`TIER2-CHECK4-PUTSIDE`; leave it.

---

## 5. Per-bot configuration — identical on every arm

These are **bot-level settings**, which the Library automations do **not** carry. They are set by
hand per bot and are therefore a real matching surface: **§8's capture-diff must cover them, not
just the exit input.**

| Setting | Value on every arm | Why this value |
|---|---|---|
| Account | Paper | Day-0 is paper; the whole family is Track-B-class evidence |
| Allocation (`seed`) | **$2,500** | `min="250" max="100000"`. ⚠️ **Not an interlock** — corrected under review. With `posLimit` = 2 and IC = 2 positions the bot can never hold more than one condor (~$400 gross entry risk), so the **position limit binds first, always, at ~17% of allocation.** The value is set identically across arms per `build-plan.md` §5 and for capture legibility; it does not defend anything |
| Daily Position Limit (`posLimitDay`) | **2** | IC = 2 positions. One condor per day |
| Total Position Limit (`posLimit`) | **2** | Same. Also interlock 2 of §4.3 |
| Scan Speed | **Every 1m** (both) | Matches the pilot; the entry gate is time-based so cadence only affects promptness |
| Day Trading | **Allowed** | 0DTE requires it |
| Symbols panel | (empty — `QQQ` is carried in the automation) | Matches the pilot. ⚠️ trap 2 does not bite fresh builds, but verify anyway |
| Bot Group | **`IC`** | §5.2 below |
| Bot Tags | `experiment`, `gfam`, `arm <role>`, `pr nn` | §5.1 below |
| `AUTOMATIONS` toggle | **OFF until Day-0** | The account is inactive; nothing may trade before signing |
| `EXIT OPTIONS` toggle | **ON** | Matches the pilot's verified state |

### 5.1 Tags — and the platform limit they hit

⛔ **OA normalises tags: lowercase, every non-alphanumeric becomes a space.** `PR-14` is **not
expressible** as a tag; the widget offers exactly `pr 14`. Ruled 2026-08-04:
**`PR-NN` → `pr nn` in OA tags, literal `PR-NN` in Notes.** The tag is a *search handle*; the
record is the pre-registration entry pasted verbatim into template Notes, which carries the
literal `ID               PR-14` line.

Per-bot tags, in order: `experiment` · `gfam` · `arm ride` (or `arm pt50`, `arm trail`,
`arm touch0`, `arm sl100`, `arm sl200`, `arm canary`) · `pr 14` (…`pr 20`).
Template tags: `experiment,pr nn,gfam`.

⚠️ **Tag widgets need per-character `input` events to open their suggestion menu; a bulk
`form_input` + Enter does not commit.** Drive them by clicking the suggestion item, then re-read
`input[name=tags].value` after a hard reload.

### 5.2 Bot Group — and the internal tension in `oa-ops-runbook.md` §3, resolved

§3 says two things that cannot both be satisfied by the group field:

> `**Convention: `Group = Pillar`** — `IC` · `Directional` · `OA-Mirror` · `Lab`.`

and

> `Tournament arms live in one group so they can be queried as a set`

A bot is in exactly one group (single-select). Under Pillar grouping, *every* IC bot shares `IC`,
so the group cannot also be the cohort handle.

**Resolved here: Group = `IC` (the convention wins, and it is what reconciles to
`bots_meta.csv`'s `pillar` column). The cohort handle is the tag `gfam`.** §3's second use is
served by the tag, not the group. Flagged as a §3 wording tension; **not amended.**

⚠️ Set the group **at creation**, not at the sweep. §3's "do the group reorganisation as part of
the Phase 4 sweep, not before it" is about *not sorting bots you are about to archive* — these
are new bots that survive the sweep. Setting `IC` at birth also sidesteps memo finding **N-5**
(whether an ungrouped bot appears in an all-groups export is **unobserved**, and an ungrouped bot
silently missing from the export would erase the family from the ledger). The pilot's group
remains unset by Decision 7's ruling; that is a separate open item and is not this family's.

### 5.3 Position limits — the ceiling, and why it does not bite here

§9 check #9, answered 2026-08-04: `posLimitDay` and `posLimit` are **hidden inputs behind
1–10 pickers** — no `max` attribute, no free-text path. Combined with IC = 2 positions, the real
ceiling is **5 ICs/day per bot**, not ten. D-2 ruled: **cap at 5 ICs/day, one bot** — do not split
a strategy across two bots to reach ten.

This family runs **one condor per day per arm**, enforced twice over: by the
`Bot opened a position with tag <side> today → NO` gate in the shared entry tree, and by the 2/2
limits. The ceiling is nowhere near binding. Recorded so a later "add re-entries" idea meets the
constraint before it meets the build.

### 5.4 Sizing — 1 lot, identical, and the primitive it is built from

`build-plan.md` §5: **experiments 1 lot; tournament arms always identical allocation.**

Size is set in the **shared** Open Position action, so it is identical across arms **by
construction** — this is one of Architecture E's largest wins and it retires the
`CallVIXdrop` allocation-mismatch class of defect (`pre-registration-ledger.md` §8 item 4) for
this family entirely.

⚠️ **The primitive is a Phase-0 check (C4), not an assumption.** The pilot's live action uses
`Up to $5,000 risk`. Whether a **fixed contract count** is selectable in the same control has
**not been observed**, and this file will not assert it.

- **If a contract-count option exists:** set **1 contract**.
- **If it does not:** set **`Up to $250 risk`** — with the failure band below stated, not hidden.
- **Either way, record which primitive was used in every pre-registration's MECHANISM block
  before the build**, not after. That is the HedgeD rule: a substitution at a platform limit has
  to have something to contradict.

> ### ⛔ THE $-RISK FALLBACK IS NOT DETERMINISTIC — corrected under review
> Max risk per contract = $200 − 100·c, for credit `c`. Two contracts fit under a $250 cap when
> `2 × (200 − 100c) ≤ 250`, i.e. **c ≥ $0.75**. The credit filter is
> `Mid price is between $0.08 – (no max)` — no upper bound — and `hedge-research.md` §11 records
> *"Min-credit filter hurts — winners averaged **lower** credit than losers"*, so high-credit days
> are admitted on purpose. A $0.75 credit on a $2-wide 0.75%-OTM QQQ 0DTE spread is unusual, not
> impossible, in a high-IV regime.
>
> **And on such a day the arms can diverge from each other**, because §8.4-H1 concedes the seven
> SmartPricing ladders fill independently: at $0.74 vs $0.76 across two arms, one sizes 1 lot and
> the other sizes 2. **A shared *action* does not guarantee a shared *contract count* when the
> sizing primitive is risk-denominated and the denominator is the fill.** The draft's claim that
> this *"retires the `CallVIXdrop` allocation-mismatch class of defect for this family entirely"*
> is **false under the fallback** and is withdrawn; it holds only if C4 returns a contract-count
> primitive.
>
> **Guard, mandatory under the fallback:** nightly assert **A6** — every `gfam` arm opened
> **exactly 1 contract per leg** today, or RED. This is computable from the export's quantity
> field and it converts a silent tail-day divergence into a same-day alarm.

---

## 6. Pricing and the 15:50 / 15:52 attribution stance

### 6.1 What is priced how, and why

| Mechanic | Class | Pricing | Authority |
|---|---|---|---|
| Entry (both sides) | Scanner action | **SmartPricing `normal`**, final price `pct` = 100 | Decision 5 — ban extends to entries |
| Profit Taking % | Exit Option | `speedy` | §7 ban; §7's guidance *"Fast for 0DTE exits where fill certainty matters"* |
| Expiration 15:50 | Exit Option | **`speedy`** — ⛔ **not Market** | **Decision 6** |
| Trailing / Touch / Stop Loss | Exit Option | non-Market, exact control per Phase-0 check C3 | §7 ban |
| 15:52 flat close | **Events** | **`Market`** | §7's single carve-out; Decision 6 keeps it |
| ITM Position Action, 15:50 | **Account-level** | `market` | D-3 — see §7 |

Decision 6, verbatim in its ruling: **re-price the 15:50 Expiration exit OFF Market; the 15:52
backstop KEEPS Market.** For the pilot this is deferred to Template V2 pre-Day-0, because PR-03's
config hash is frozen and it is a spec change rather than a config tweak. **The family specifies
non-Market Expiration pricing from birth**, so no deferral applies here.

### 6.2 The attribution stance — three mechanics aimed at two minutes

§8.2's guard: *"Give the Event a **distinct SmartPricing setting** from the Exit Option so the
Trades list distinguishes them."* On this family, **four** mechanics can close a position between
15:50 and 15:52 — the draft counted three and its Rule 1 was false as a result:

1. **Expiration Exit Option, 15:50, `speedy`** — SmartPricing.
2. **ITM Position Action, 15:50, `market`** — account-level, expiring-ITM positions only.
3. **15:52 Events backstop, `Market`**, memo `1552 backstop flat close`.
4. **⭐ `GF-SiblingClose`** — fires on `Position closed`, so it fires *precisely when* mechanic
   1, 2 or 3 closes the first leg. The draft priced it `speedy`, i.e. **identical to mechanic 1**,
   which made "the Expiration exit is the only SmartPricing close in that window" untrue for all
   seven arms and left §8.5's Ride artifact satisfiable by either mechanic.

**The stance, in four rules:**

- 📝 **SUPERSEDED 2026-08-06 — Rule 0 is MOOT: sibling-close is not built (C8 ruling, §4.3). The
  15:50–15:52 window now holds THREE mechanics, not four, and Rule 1 is satisfied without it.
  Left standing below.**
- **Rule 0 — ⭐ sibling-close is re-priced `patient` and gated to before 15:44** (§4.3, amended
  2026-08-04 from 15:50 — the tighter gate also clears the 15:45 `Expiration 0.015` exit class).
  Two
  changes, one purpose: the gate removes it from the window entirely, and the distinct pricing
  keeps it distinguishable from mechanic 1 in the rest of the day, when it *is* the mechanic that
  closes second legs. `patient` (up to 5 prices / 20s each) is a documented mode, is non-Market,
  and is used nowhere else in this family.
- **Rule 1 — pricing separates mechanic 1 from mechanics 2 and 3.** With Rule 0 applied, the
  Expiration exit is the only `speedy` close in the window. §8.2 is satisfied at the pricing
  level, which it was not on the pilot (both were `Market`).
- **Rule 2 — the memo separates mechanic 3 from mechanic 2.** The backstop's Close Position
  action carries `1552 backstop flat close`; the account-level ITM action carries no bot memo.
  ⚠️ **Open Day-0 check (D-2 in §12):** whether the ITM action appears in the position's Trades
  list at all, and under what label, is **unobserved**. Rule 2 is provisional until it is read.
- **Rule 3 — ⛔ ambiguous fills are NOT assigned.** Memo finding **N-6**: an exit-option order
  stays live **two minutes** (§6.4, [DOCUMENTED] — *"no additional orders will be sent to your
  broker"*), so the 15:50 order is **still working when the backstop fires at 15:52**. The
  mechanics genuinely overlap. `oa-ops-runbook.md` §4.4's timestamp-gap test is calibrated on
  `:00`/`:01–:02` gaps and sits *on* a 2-minute designed gap, not clear of it. Automation timing
  is jittered anyway.
  **Any Market-priced close in [15:50, 15:53] without the backstop memo is bucketed
  `UNATTRIBUTED` and counted, never assigned to a mechanic.** The count is reported in the daily
  brief. `execution_audit.py`'s `rule_C5_backstop_caught_it` continues to read `time_exit` and
  `event_backstop` as separate config columns; a third bucket is added rather than forcing a
  binary.

**Why not just remove the 15:50 exit and let 15:52 be the only time close** (memo Decision 6
option D): it loses the PT-independent time exit and makes the Events class a single point of
failure. Rejected there; rejected here.

---

## 7. ITM Position Action — the assumption, stated explicitly

**This family is specified on two assumptions about an account-wide setting it does not
control:**

1. **`itmpaper` = `market`.** ✅ **RULED AND EXECUTED 2026-08-04** — verified by hard reload +
   `input.value` re-read, before/after screenshots in
   `data/captures/2026-08-03-pilot/06-clone-final/`.
2. **`itmlive` = `market` before any capital is live.** ⏳ **NOT YET SET — deliberately left at
   `auto`.** It is a **hard Day-0 gate**, not a preference.

**What breaks if assumption 1 regresses.** Under `auto` an ITM-expiring position's P/L is
*estimated from the underlying close price* — a modeled number, not a fill — and it lands in the
export and therefore in the ledger. **ITM-at-expiry is by definition the losing tail of a credit
condor**, and the loss tail is exactly what separates these arms: SL100 from SL200 from ride.
Under `auto` the tail is synthetic and **the ranking measures a model, not the arms.** The mirror
baseline (n=174 positions, 10 mirrors, zero excluded) found four mirrors with positive median R
and negative mean R — they win most trades and lose money. The tail is where the answer lives.

**What breaks if assumption 2 is missed.** QQQ is a physically-settled ETF and the bot is
assignment-blind (§13.1). `auto` means real stock delivered. This is the single largest reason
§2's QQQ choice carries a cost.

> ### ⛔ THE DRAFT SAID THIS "CANNOT CONFOUND THE RANKING". THAT IS WRONG AND IT IS WITHDRAWN.
> The draft argued: the setting is account-wide, it overrides nothing per-bot, therefore it
> degrades every arm's tail identically. **The setting is account-wide; its INCIDENCE is not.**
>
> §13.1: `market` closes *"Positions expiring in-the-money"*, 10 minutes before the close. So it
> reaches a position only if that position is **still open at 15:50 AND in-the-money**. Trace the
> incidence:
>
> | Arm | Share of the loss tail still open & ITM at 15:50 |
> |---|---|
> | `Ride` | ~all of it |
> | `PT50` | ~all of it — PT truncates winners, not losers |
> | `SL100` / `SL200` | much less — truncated by the stop |
> | `Touch0` | **~none, by construction** — Touch `$0` closes as the position goes ITM |
>
> **The arms whose hypothesis is "capping the loss tail raises Exp(R)" are the same arms that are
> systematically NOT exposed to the fleet's own worst documented execution mechanic** — the
> Market fill that came in *"$5.05/contract beyond the worst mark the position ever traded at"*,
> R −1.63. The same asymmetry applies to the 15:52 backstop, which is also `Market` and also only
> touches positions still open at 15:52.
>
> **And it is not repairable by choosing the other setting.** Under `auto` the identical
> ride-heavy, touch-free subset gets a *modeled* P/L instead of a *slipped* one. **There is no
> value of `itmpaper` under which the tail measurement is arm-neutral.**
>
> This is `hedge-research.md` §5.1 defect 2 wearing new clothes — *"S3's win is inseparable from
> its execution class"* — and it is the single most serious surviving objection against this
> design. It is carried as **CF-1** in §11 with its mitigation, not dismissed.

⚠️ **`market` is not a substitute for the 15:52 backstop.** It covers only *expiring ITM*
positions on expiration day. The backstop covers everything else.

**Add to the capture set, every sweep** (D-3 amendment b, drafted and not yet applied):
`itmlive` · `itmpaper` · `maxexits` · `scanstart`/`scanend`/`exitstart`/`exitend`. `maxexits`
reads `0` = Unlimited today and is a single account-wide switch that can silently cap every
bot's ability to close — the exact failure shape §0.3 and §10 are about.

---

## 8. The arm-matching mechanism and its PROOF procedure

`hedge-research.md` §5.2 is the definition of done. An arm may enter a ranking only when **all
five** hold. Here is each, and what discharges it.

| # | §5.2 requirement | Discharged by |
|---|---|---|
| 1 | Shared automation, shared inputs; arms differ in exactly one input value, proven by capture-diff | §1.1 (shared Library objects) + §8.2 (the diff) |
| 2 | Same execution class — all Exit Options or all Monitors, never mixed | **All seven arms are Exit Options.** §9 row 1 resolved `Touch` as an Exit Option, which is what dissolved v1's confound. Moving any arm to Monitor class would re-introduce it |
| 3 | Range075 on every arm | §4.1 — in the shared entry automation, identical by construction. The `as a preset` wording is N-2 |
| 4 | Pre-registration naming the hypothesis, kill criterion, sample target, review date **and the platform primitive** | ✅ **DISCHARGED FOR ALL SEVEN, 2026-08-06.** C1 confirms `stoploss` = **% of credit** (SL100 = `1`, SL200 = `2`), C2 confirms `tstop` carries a **native arming threshold** (`target` % of credit + `trail` % pullback), and C3 closed the pricing sub-field on 2026-08-05. **Trail, SL100 and SL200 are arms.** The row's original text is left standing below. ⛔ **Separately — and this is NOT a §5.2 failure — C8's STOP removed `GF-SiblingClose`, so all seven MECHANISM blocks are re-stamped** (§4.3 ruling). <br>~~⛔ **NOT DISCHARGED FOR THREE ARMS.**~~ §9 names the primitive for Ride, PT50, Touch0 and the Canary. For **Trail** the primitive is unconfirmed (C2), and for **SL100/SL200** the *unit* of `stoploss` is unconfirmed (C1); C3 leaves the pricing sub-field unknown on four arms. §5.2's own closing sentence governs: an arm failing any of the five is *"not a weak arm, it is not an arm."* **Those three arms are not arms until Phase 0 closes.** The draft marked this row discharged; corrected |
| 5 | A proof-of-fire artifact identified in advance, checked on the first live position | §8.5 |

### 8.1 What "one differing input" means here, precisely

**Granularity: the bundle.** `hard-PT vs trailing vs ride` populate *different* Exit-Options
fields — at field granularity these arms differ in two or three fields **by construction**. The
bundle is the only object type under which §2D's `arms differing / in exactly one input value` is
literally true, which is why Option A required no amendment to the frozen plan.

**Consequence that must be stated and carried — corrected under review:**

> **Arm-vs-control comparisons are ONE-TRIGGER, TWO-FIELD deltas. Arm-vs-arm comparisons are
> three- or four-field.**
>
> The draft claimed arm-vs-control was a "single-field delta". §4.4's own table refutes it: each
> trigger comes with its own pricing sub-field, so `PT50` vs `Ride` differs in **`profits` AND
> `smprofits`** — two fields. For Trail, Touch0, SL100 and SL200 the second field is currently
> **unknown** (Phase-0 check C3), so four of six experiment arms have an unspecified pricing
> field in their bundle as this is written.
>
> Every experiment arm = Ride's base bundle + exactly **one mechanic** (trigger + its pricing).
> `SL100` vs `SL200` differs in one field's *value* only — that pair is the cleanest comparison
> in the family. `PT50` vs `Trail` differs in **four** fields.
>
> **The family is designed for arm-vs-control readings.** A direct PT50-vs-Trail ranking is a
> comparison of *policies*, not of one parameter, and **must be caveated as such wherever it is
> published.** The CI on it is not the CI on a single-variable experiment.
>
> ⚠️ **Arithmetic correction:** seven arms give **21 unordered pairs** and **42 ordered** ones.
> The draft said "21 ordered". The diff runs over the 21 unordered pairs.

### 8.2 The capture-diff — the procedure, step by step

Run pairwise across all seven arms (**21 unordered pairs**) at build completion, and again at
every sweep.

```
FOR each arm:
  1. Capture the bot page and every automation, every caret expanded (trap 3).
  2. Read BOTH BOT INPUT objects — GF_EXITS_PUT and GF_EXITS_CALL — their VALUES, from the
     per-bot input surface.
     ⛔ NOT the Open Position action (it holds {"type":"input",...} — identical on every arm).
     ⛔ NOT `oldValue` (stale pre-link snapshot).
  3. DECODE both exits payloads to FIELDS. The blob is decodable: the pilot's `^^0.5|0.01^$0`
     decodes to 50% PT / 10-minute expiration. A ~20-line parser feature, not an opacity problem.
  4. INTRA-ARM: assert decoded(PUT) == decoded(CALL).            ⭐ per-side asymmetry check
  5. Read the bot-level settings block: seed · posLimitDay · posLimit · scan speeds ·
     day trading · group · tags · toggles.
  6. Read the attached-automation id list (rid values) — proving the SAME objects, not copies.
  7. Write the row into data/bots_config_v2.csv, carrying the DECODED FIELD SET, not the blob.

FOR each unordered pair (A,B):
  Let dA, dB be the decoded FIELD SETS (base fields + the arm's one mechanic).
  PASS  iff  symmetric_difference(dA, dB) is confined to EXACTLY ONE MECHANIC       ⭐
             (a trigger field and, if present, its own pricing sub-field — nothing else)
        AND  every base field (expdays, smexpdays, chposLimitDay, chbidask) is EQUAL
        AND  every bot-level setting in step 5 is EQUAL except name / arm tag / PR tag
        AND  the rid lists in step 6 are EQUAL (same shared objects, not copies)
  Any other outcome is a FAIL and the family does not trade.
```

> ⭐ **The PASS condition is rewritten. The draft's test was `decoded_bundle(A) != decoded_bundle(B)`
> — DISTINCTNESS, not `build-plan.md` §2D's "arms differing in exactly one input value".** Under
> the draft's test, an SL100 arm that also accidentally carried a Touch, or a different
> `smexpdays`, or a stray PT, **passed**. The diff detected only the v1 failure (arms that are
> *identical*) and was structurally blind to the failure this architecture actually invites —
> arms differing in *more than one* mechanic. Both adversarial reviewers found this independently.
> The condition above tests **one-mechanic difference at field granularity**, which is what §2D
> and `hedge-research.md` §5.2 rule 1 actually require.

⚠️ **Two known failure modes of the diff itself, both already paid for once:**

- **False positive (N-4).** OA re-serialises an `exits` blob on save even when nothing changed;
  labels drift while payloads are byte-identical. **Compare decoded payloads, never rendered
  labels.**
- **False negative — and it is the one the diff cannot fix.** `hedge-research.md` §7: HedgeD's
  *"config record and automation tree agreed with each other and both were wrong about the
  intent"*, −$15,376. **A capture-diff between arms passes clean if every arm was mistyped
  identically.** The diff is **necessary and not sufficient.** The defences are (a) §8.3 rule 3,
  which compares each arm to its *pre-registration* rather than to its siblings, and (b) §5.2
  rule 4 — every pre-registration names the platform primitive.

### 8.3 The nightly arm-distinctness assert — ⛔ it does not exist and must be built

`oa-ops-runbook.md` §3 promises the nightly script can `assert arm-level parameter distinctness.`
and claims this makes the S1 ≈ HedgeD failure detectable `instead of four months late.`
**Nothing in `scripts/` implements it** (memo finding **N-3**). `execution_audit.py` has 13 rules
(S1–S8, C1–C5); the nearest, `rule_S7_duplicate_arm`, is post-hoc and outcome-based
(`(open_date[:16], pnl, structure)`), **silent until 5 identical trading days**
(`DUP_MIN_DAYS = 5`), **AMBER**, and its own remedy is
`verify_by="a capture-diff of the two bots' automation trees"`.

**Until it is built, §3 may not be cited as a proof leg by this spec or by any pre-registration.**

**Specification of the missing assert** (a new config-based rule set, reading
`data/bots_config_v2.csv`, run in `daily.sh` and fail-loud RED):

| Rule | Assertion | Catches |
|---|---|---|
| ~~**A1**~~ | ~~For every unordered pair of `gfam` arms, the decoded field sets differ in **exactly one mechanic**~~ 📝 **AMENDED 2026-08-07 — RULED BY ANDY. ORIGINAL LEFT STANDING, STRUCK. See A1 (amended) immediately below.** | ~~Two arms that are one arm (the S1 ≈ HedgeD class) **and** two arms that differ in more than one thing, on day 1~~ |
| **A1** 📝 **AMENDED 2026-08-07** | **Pair type decides the expected count, because the family is a control + K design.** (a) **ARM-vs-CONTROL** (each of the six arms against `GF-QQQ-IC-Ride`): the decoded field sets differ in **EXACTLY ONE mechanic** — a trigger field and, if present, its own pricing sub-field. (b) **ARM-vs-ARM** (two different treatment arms): they differ in **EXACTLY TWO mechanics**, and those two must be **precisely each arm's own declared mechanic** — arm A's, absent on B, and arm B's, absent on A — **with nothing else differing**. ⭐ **Two arms that share a mechanic FIELD at different VALUES** (`PT50`/`Canary` on `profits`; `SL100`/`SL200` on `stoploss`) **differ in exactly ONE** and are checked under (a)'s rule. In every case the base fields (`expdays`, `smexpdays`, `chposLimitDay`, `chbidask`) must be EQUAL. | Two arms that are one arm (the S1 ≈ HedgeD class); an arm carrying a mechanic that is not its own; an arm that has lost its own mechanic; **and** any difference outside the arms' declared mechanics — all still caught. **What is no longer caught as a failure is the design itself.** |

> ### 📝 A1 AMENDMENT — 2026-08-07, RULED BY ANDY ON FINDING A1-SPEC-1. The original row is struck above, left standing.
> **The forcing fact, recorded because it is what made this a bug and not a preference:** the
> assert was run for the first time against a complete family on 2026-08-07, at n=7 bots and
> **21 real pairs. It produced 8 PASS and 13 FAIL — and all 13 failures were correct builds.**
> In a control + K design two DIFFERENT treatment arms differ from each other in exactly TWO
> mechanics **by construction** (arm A's mechanic is absent on B and B's is absent on A), so the
> original text was **unsatisfiable for 13 of the 21 pairs and would have fired 13 false alarms
> every night, forever, on a family with nothing wrong with it.** An assert that cannot be
> satisfied is not a strict assert; it is an assert that gets muted, and a muted A1 is exactly
> the S1 ≈ HedgeD hole it was written to close.
> **This is the same defect class §9 already corrected once** — the family-level kill criterion
> that counted *inputs* and was "vacuously unfireable" under Option A. Both reviewers caught
> that one on paper; this one only surfaced when the seventh bot existed. **The lesson recorded
> for the other asserts: an assert is not verified until it has been run against a COMPLETE,
> CORRECT population and produced zero failures.** A1, A2 and A8 had all been "run" at n=1 arm,
> where A1 and A2 were vacuous.
> **What the amendment does NOT relax:** every failure mode the original was written to catch is
> still caught — see the Catches column. Arm-vs-arm is not waived, it is given its correct
> expected value (2) plus the requirement that the two differing mechanics be **exactly the two
> arms' own declared mechanics and nothing else**, which is strictly stronger than "differs".
> **Verified against the built family the same day:** under the amended rule all **21 of 21**
> pairs pass — 6 arm-vs-control at one mechanic, 2 shared-field pairs at one, 13 arm-vs-arm at
> exactly two, each pair's two being precisely the two arms' own mechanics.
> ⛔ **THE NIGHTLY ASSERT BUILDS AGAINST THE AMENDED TEXT, NOT THE STRUCK ONE.** Evidence:
> `data/captures/2026-08-07-greenfield/ASSERTS-A1-A9-and-capture-diff.txt`;
> `session-log.md` 2026-08-07 (six-arm session) and (rulings).
| **A2** | Every non-bundle field (rid list, seed, both limits, scan speeds, day trading, entry-action payload) is equal across all `gfam` arms. 📝 **AMENDED 2026-08-06 (Andy, authorized):** add **trigger config** (class / time / repeat / days) to the comparison — trigger lives at the bot, not the shared Library object (F-3, `session-log.md` 2026-08-06 late), so §8.2 step 6's rid-list diff does not cover it and the backstop's 15:52 / Mon–Fri / holidays-skip config (§4.2) was an undetected matching hazard. | Silent divergence in the "shared" half, **including a per-arm trigger-config mismatch** (e.g. the backstop's 15:52 hand-set on all seven bots) |
| **A3** | Each arm's decoded field set **equals its pre-registered field set**, value-by-value | ⭐ **The all-arms-mistyped-identically hole.** A1 and A2 both pass in that case; A3 is the only rule that fires |
| ~~**A4**~~ | ~~No arm's stored bundle equals `SENTINEL-SL1`~~ 📝 **MOOT 2026-08-06 (F-4 ruling, §1.3a) — SENTINEL-SL1 is struck, nothing is ever stamped it.** | ~~A *typo* stamping the sentinel as an arm value.~~ Superseded by **A9** below |
| **A4b** | ⭐ No arm shows a ledger day of stop-outs within minutes of open with no `stoploss` in its config | The **broken input link** — the runtime fell back to the Default while the stored config still reads correct |
| **A5** | `itmpaper`, `itmlive`, `maxexits` match their recorded values | Account-wide regressions |
| **A6** | ⭐ Every arm opened **exactly 1 contract per leg** today | The $-risk sizing fallback silently sizing 2 lots on a high-credit day (§5.4) — and doing it on *some* arms only |
| **A7** | ⭐ The **payload hash of each shared automation** matches its recorded baseline | **Architecture E's own blind spot** — see below |
| **A8** | ⭐ For each arm, `decoded(GF_EXITS_PUT) == decoded(GF_EXITS_CALL)` | Per-side exit asymmetry inside one arm (§4.1), which A1 and A3 cannot see |
| **A9** | 📝 **NEW 2026-08-06 (F-4 ruling, §1.3a).** Every arm's `GF_EXITS_PUT` / `GF_EXITS_CALL` bot input is BOUND and NON-EMPTY (`decoded(value) != {}`). Verified before any arm's `AUTOMATIONS` toggle goes ON at Day-0 — not a nightly-only check | The broken/unset-link failure mode config-level, replacing A4/sentinel detection. No arm legitimately runs empty exits (`Ride` is time-exit-only via its own close row) |

**A3 is the load-bearing one** and it is the direct answer to the surviving adversarial objection
in the memo's Appendix A item 6 — *"nothing catches a day-1 hand-set error under ANY
architecture"*. A3 catches it because it compares each arm to a written intention, not to its
siblings.

> ### ⭐ A7 exists because Architecture E creates a failure mode per-arm copies do not have
> An edit to a shared automation — strike distance, credit floor, entry pricing, a Range075
> threshold — changes **all seven arms simultaneously**. Trace it against A1–A6: A1 compares arms
> to each other (all seven changed together → **pass**). A2 asserts the shared half is *equal
> across arms* (still equal → **pass**). A3 compares the **exit bundle**, which is not what
> changed → **pass**. A4/A5/A6 are unrelated.
>
> **Every assert in the draft's set passed on a mid-sample edit that silently splices two
> different experiments into one n=100 sample**, with no boundary recorded anywhere — and, per
> the Phase-B note, possibly with no template version bump either, since template rows carry the
> live `rid`. A7 is the only detector, and it is why the shared-object payload hashes must be
> recorded as a baseline at build completion (build step C7).

⚠️ **Ordering: the assert is a precondition, not a follow-up.** `oa-ops-runbook.md` §2.2's
governing logic — `**If that assert is not built, do not build the BUILD_ID mechanism at all.**`
— was about a self-report nobody checks manufacturing confidence. The same logic applies to
citing "the nightly assert" as a proof leg. **Whether the assert must be built before the
tournament trades is one of the memo's four `NOT RULED` slots** (Decision 4, second ruling line).
This spec's build order (§10) places it before Day-0 as the safe default and marks it as awaiting
that ruling.

### 8.4 Two matching hazards the diff cannot see

**H1 — entry-credit dispersion, and it moves TRIGGERS as well as denominators.** All seven bots
run the same signal but fill **independently**: seven SmartPricing ladders walking separately
produce seven possibly-different entry credits. `ror` is return on **risk**, so a differing credit
moves the denominator. ⭐ **And it does more than that, which the draft missed:** `profits`,
`stoploss` and `tstop` are all **credit-referenced**, while `touch` and the Ride base are not. At
$0.30 vs $0.34 fills, PT50 and SL100 are not merely scored on different denominators — **their
trigger levels are different prices.** Tick quantisation compounds it: 50% of a $0.15 credit is
$0.075, off the penny grid, so the *realised* PT% and SL% vary with credit day to day and arm to
arm. **Required instrumentation:** log entry credit per arm per day; assert nightly that cross-arm
credit dispersion on matched days stays inside a pre-declared band; report breaches.

**H2 — non-fill selection, and it is NOT family-level.** The draft claimed *"a non-fill day is a
non-fill day for the whole family — the bias is on the family's day distribution, not between
arms."* **That contradicts H1 four lines above and it is withdrawn.** Seven independent ladders
produce seven independent fill/no-fill outcomes; a limit that fills for four bots and not three
is the normal case. Worse, the *signal evaluation* is independent too — §4.2, [DOCUMENTED]:
*"All user automations are pushed into a **distributed work queue and executed in parallel** …
There is no guarantee an automation will run exactly on the 15-minute marks."* Sharing a Library
*object* does not share an evaluation *instant*. On a day where |Δ%| sits near the 0.75% band
edge, bot A evaluates at 13:31:05 with Δ = 0.74% and opens while bot B evaluates at 13:31:50 with
Δ = 0.76% and does not — **arm-specific selection on precisely the highest-information days.**
**Required:** define "matched day" explicitly (below), log non-fills per arm, and report unequal n.

> ⭐ **"Matched day", defined — the draft used the phrase in every SAMPLE TARGET line without
> defining it.** A trading day is **matched** iff **all seven arms opened a condor on it.** All
> primary arm-vs-control comparisons run on matched days only, **paired by day** (§9's analysis
> convention). Unmatched days are logged, counted per arm, and **excluded from the primary
> comparison** — never silently absorbed. The matched-day count, not the per-arm position count,
> is the sample size that matters, and §11-CF9's arithmetic is stated against it.
>
> 📝 **RULED 2026-08-06 (G-2, M6, by Andy)** — `comparative-machinery-spec.md` §1.5: the
> engine's gate reads **`M6`** (the six comparative arms PR-14…PR-19), not `M7` as defined above.
> The Canary PR-20's fill no longer gates the five real comparisons. `M7` (all seven, as defined
> here) is still computed and printed for visibility. This definition of "matched" is otherwise
> unchanged.

**H3 — live-only, recorded now.** Seven identical condors entered at the same second create
fill-queue interaction if this family ever leaves paper. Matching degrades the moment it goes
live. Day-0 is paper; this is a gate on any funding decision, not a build issue.

### 8.5 Proof-of-fire, per arm — declared in advance

`hedge-research.md` philosophy §6: *a hedge that cannot be proven to have fired is not a hedge.*
Every artifact below is read from the position's **Trades list**. ⛔ **The Exit Options panel is
never evidence** — §0.3, `oa-ops-runbook.md` §4.2: in v1, Fortress positions generated **no exit
orders at all** — not sent-and-unfilled, **never sent** — while the panel still displayed
`PROFIT % 50%`.

| Arm | Artifact that proves it is running its declared mechanic |
|---|---|
| `Ride` | **Inverted check:** NO profit-taking row, NO trail row, NO touch row, NO stop row; **and** a close row at ~15:50 priced **`speedy`** (the Expiration exit). ⚠️ Read `speedy` specifically, not "SmartPricing". 📝 **2026-08-06: the ambiguity this warning guarded against is GONE — sibling-close is not built, so `speedy` at ~15:50 can only be the Expiration exit.** The warning is kept because reading the pricing field is still the check. Original: ~~sibling-close is `patient` and the draft's shared `speedy` made this artifact satisfiable by either mechanic (§6.2 Rule 0)~~ |
| `PT50` | A profit-taking row at 50% |
| `Trail` | A trailing-stop row |
| `Touch0` | A touch row **within 2 minutes** of the first 1-minute bar on which the underlying is at or through the short strike. ⚠️ The tolerance is explicit because the control is 1-minute-sampled (§4.4) and automation timing is jittered; "immediately after" has no testable meaning |
| `SL100` / `SL200` | A stop-loss row |
| `Canary` | A profit-taking fill **on day 1** |
| ~~**all**~~ | ⛔ **VOID 2026-08-06 — this artifact will not exist. Sibling-close is not built (C8 ruling, §4.3), so there is no `sibling close` memo row on any arm.** Replacement artifact for early-exit arms: the tested spread's own exit row, and the **second leg closing at its own ~15:50 Expiration exit or the 15:52 backstop** — which is what "the spread is the unit" looks like in the Trades list. `oa-ops-runbook.md` §4.4's designed-vs-emergent timestamp test no longer applies to this family; **an emergent `:00`/`:01–02` close-both pattern is now a FINDING, not a pass.** Original left standing: ~~A `sibling close` memo row on the second leg, priced **`patient`**, timestamped `:00`/`:00` against the first — `oa-ops-runbook.md` §4.4's designed-vs-emergent test. ⚠️ Only on closes **before 15:44** (amended 2026-08-04 from 15:50); in **[15:44, 15:50)** the sibling is left to its own 15:50 Expiration exit, and after 15:50 the backstop closes both legs — sibling-close is gated off in both cases (§4.3)~~ |

---

## 9. DRAFT pre-registration entries — all seven, unsigned

*Format per `pre-registration-ledger.md` §2. Every entry below is **DRAFT — unsigned**. Signing
is Andy's, at Day-0, per §7 of that ledger: config hash filled from the bot's own capture, every
placeholder resolved, kill criterion re-read against the daily loop, max-loss filled, then signed
— and only then may the bot be switched ON. **Signed ≠ verified**: the Trades-list artifact is
read before it may take a position.*

> ### ⭐ ALL SEVEN MECHANISM BLOCKS RE-STAMPED 2026-08-06 — two rulings, both Andy's, both applied.
> Every entry below is still **DRAFT — unsigned**; this is a re-stamp of the drafts, not a signing.
>
> **1 · C8 ruling — BUILD WITHOUT SIBLING-CLOSE (§4.3).** `GF-SiblingClose` is not built, so
> **no arm is a close-both mechanic**. Applying to all seven: the **spread**, not the condor, is
> the unit for **early exits**; a second leg left open by an early exit closes at its own 15:50
> Expiration exit or at the 15:52 backstop. Concretely — `Touch0` is **S1, not S2**; `PT50` is
> **PT50 per spread**; `SL100`/`SL200` are **not** wrapped in a close-both exit and **can** reach
> the Breakeven shape their anchor describes; `Ride` and the `Canary` are unaffected (sibling-close
> never fired meaningfully on Ride). ⚠️ **The reporting unit is unchanged** — every `Exp(R)` below
> is still **per condor, ex-artifact**; what changed is the *exit mechanic's* unit, not the
> analysis unit. Any VERIFICATION line calling for a `sibling close` row is void; those rows will
> not exist.
>
> **2 · PR-16 ruling — RE-SCOPED TO THE ARMED TRAIL** (`target`=40, `trail`=15, % of credit), on
> Phase-0 check **C2**, which found the armed shape is a native primitive. See PR-16 below.
>
> Evidence for both: `data/captures/edit-verify/2026-08-06/phase0_C8.txt` and `phase0_C2.txt`;
> `session-log.md` 2026-08-06. **Original text throughout §9 is LEFT STANDING per convention.**

**Conventions applying to all seven, stated once so each entry stays readable:**

- **Unit: the POSITION = the CONDOR** (the two spread rows paired by `trade_id`); **risk = the
  larger side**. Every `Exp(R)` below is **per condor, ex-artifact**. `R` basis is `ror` (return
  on **risk**), never `returnPct` (return on credit).
- ⭐ **ANALYSIS CONVENTION — PAIRED BY DAY, on matched days only** (§8.4's definition). The draft
  never said whether the analysis was paired, and pairing is the only thing that makes this
  family statistically tractable at all — see the power note below.
- ⭐ **COMPARATIVE CRITERION** (added — the draft had only an absolute one; see §11-CF2):
  *Arm X beats the Ride control iff the paired per-condor ΔR (arm − control) has a bootstrap 95%
  CI entirely above 0 after ~~Bonferroni correction across the 6 arm-vs-control tests~~ **the
  family's joint day-bootstrap max-T correction across arms (SWITCHED 2026-08-06, G-10, ruled by
  Andy — declared before any data exists: `data/ledger_meta.json` `export_rows 0`)**, on matched
  days, at the declared n.* This is the form `pre-registration-ledger.md` PR-02 already uses
  (*"not better than the 11:00 arm's by ≥0.01 at n≥60 with non-overlapping bootstrap CIs"*).
- **SAMPLE TARGET** n = 100 **matched days** per arm. ⚠️ **Declared with its power, not without
  it** (§11-CF3): at SD(R) ≈ 0.30 and day-pairing at ρ ≈ 0.90, n = 100 gives a 95% CI half-width
  on ΔR of **±0.026R** — against a largest-ever-measured effect in this program of **+0.0150R**
  (`state.md`, SL75, n = 1,254). **n = 100 is underpowered for the effects this program actually
  sees, by roughly 2–3×**, and reaching ±0.015R needs ~307 matched days paired, ~560 with
  Bonferroni. ⚠️ **The Bonferroni-based figure above is superseded by G-10's switch to max-T
  (2026-08-06) and has not been restated under the new correction — flagged, not recomputed.**
  n = 100 is therefore a **first-read** target, not a decision target; the
  graduation gate is `build-plan.md` §5's, and it is not reachable inside six months.
- **REVIEW DATE** Day-0 + 6 months, interim read at n = 60 matched days.
- **MAX LOSS** 1 lot. Per-condor risk ≈ $200 gross per side less credit (≈$185 net) on a $2-wide
  QQQ spread; daily aggregate per bot = one condor.
- **SIZING TIER** 1 lot — experiment. **IDENTICAL across all arms**, enforced by the shared entry
  action (§5.4).
- **CONFIG HASH** `<capture> @ <hash>` — filled at signing from the arm's own capture file.
  ⚠️ **Not from the template.** Templates do **not** freeze automations: template rows carry the
  **same `rid`** as the bot's live automation (`oa-ops-runbook.md` §2.3 append; successor check
  open in §7). **The capture is the snapshot.**
- ⭐ **FAMILY-LEVEL KILL CRITERION**, carried identically on all seven — **rewritten at FIELD
  granularity**: *if a capture-diff ever shows two arms differing in **more than one mechanic**
  (a trigger field and, if present, its own pricing sub-field), or if any of §8.3's A1, A2, A3,
  A7 or A8 fires, the family's ranking is **VOID** and all arms are re-based — the comparison,
  not the bots, is what dies.*
  > ⛔ **The draft's wording — "more than one differing **input**" — was vacuously unfireable and
  > both reviewers found it independently.** Under Option A each arm holds exactly one exit input,
  > so "more than one differing input" is a state the family cannot reach. This is the identical
  > defect the memo used to *reject* Options B and C (*"with no inputs it can never fire"*); one
  > input has the same property as zero for a rule that counts inputs. It survived the ruling
  > unnoticed and is corrected here. `pre-registration-ledger.md` PR-14…PR-17's existing wording
  > carries the same defect and needs the same correction at signing.
- ⭐ **LIVENESS KILL CRITERION**, carried identically — **rewritten to stop censoring
  informatively** (§11-CF12): *zero exit-trigger rows of the arm's declared type across 10
  consecutive matched days **on which the ledger shows the arm's threshold was breached** →
  **RED**, bot switched off pending investigation.*
  > The draft's version — a bare 10-day dry spell — deletes arms during **calm regimes**, which
  > is exactly the sample a stop arm needs to look good, in a known direction, with no re-entry
  > rule. Conditioning on *threshold breached* makes it a genuine liveness test rather than a
  > regime filter. ⚠️ It requires MFE/MAE, which the ledger carries.
  > **The `Ride` control's inverted version is fenced:** *any profit-taking, trail, touch or stop
  > row → RED — **EXCEPT** rows attributable to the account-level ITM action*, whose Trades-list
  > label is **unobserved** (§6.2 rule 2, Day-0 check D2). ⛔ **Until D2 is answered the inverted
  > rule is ADVISORY, not fireable** — otherwise a mislabelled ITM close kills the control on day
  > one and every comparison in the family loses its referent.
- ⭐ **SENTINEL KILL CRITERION**, carried identically — **written as a LEDGER criterion, not a
  config one**: *the arm's positions close within 5 minutes of open on ≥ 2 consecutive days while
  its stored config carries no `stoploss` → **RED**, bot off* (§8.3 A4b). Plus the config form:
  *stored bundle == `SENTINEL-SL1` → RED* (A4). §1.3 explains why the config form alone cannot
  detect the failure it is named for.

---

```
### GF-QQQ-IC-Ride
ID               PR-14  (proposed)
DISPOSITION      fresh build
PILLAR / ROLE    IC · control
STATUS           DRAFT — unsigned

HYPOTHESIS       A QQQ 0DTE iron condor entered after 1:30pm on Range075-passing days, with NO
                 active management and a 15:50 time exit, has Exp(R) per condor ≥ 0 over
                 n≥100 condors. This arm is the control every other arm is read against; if it
                 is not measurable, no ranking in this family is.
MECHANISM        Short-premium VRP on 0DTE QQQ, harvested by time decay with no intervention.
                 PRIMITIVES: shared Library entry automation (Loop → time decision → two
                 Symbol-change-% decisions = Range075 → position-tag re-entry gate → Open Short
                 Put/Call Spread, SmartPricing `normal` entry) + a bundle-typed Bot Input
                 `GF_EXITS` holding {Expiration `expdays`=0.01, `smexpdays`=speedy} and nothing
                 else + a Repeating Events-class 15:52 Market flat close + a Position-closed
                 sibling-close automation with all three §5.4 interlocks. Size primitive per
                 §5.4 check C4 — RECORD WHICH ONE WAS USED BEFORE BUILD.
KILL CRITERION   Exp(R) per condor < 0 with the CI entirely below 0 at n ≥ 60 condors.
                 Plus the family-level, liveness (inverted) and sentinel criteria above.
                 📝 AMENDED 2026-08-06 (G-8, SEQUENCE+CS, ruled by Andy) — the n≥60 read above is
                 emitted as an always-valid confidence sequence, not a fixed-n CI; the absolute
                 kill cannot fire before this arm's own stamped GATE EVAL DATE (below).
                 Family-level and sentinel criteria (execution-integrity rules) are unaffected.
SAMPLE TARGET    n = 100 condors.
REVIEW DATE      Day-0 + 6 months; interim at n = 60.
GATE EVAL DATE   Day-0 + 6 months (relational; resolves to calendar at Day-0); interim look at
                 n=60.
MAX LOSS         ≈$185 net risk per condor; 1 condor/day.
SIZING TIER      1 lot — IDENTICAL across arms.
CONFIG HASH      <capture> @ <hash>
VERIFICATION     INVERTED Trades-list check: no PT / trail / touch / stop row, and a ~15:50
                 SmartPricing close row. Plus the pairwise capture-diff of §8.2.
SIGNED           ..............................
```

```
### GF-QQQ-IC-PT50
ID               PR-15  (proposed)
DISPOSITION      fresh build      PILLAR/ROLE  IC · experiment      STATUS  DRAFT — unsigned

HYPOTHESIS       Taking profit at 50% of credit raises Exp(R) per condor above the Ride control
                 over n≥100 matched condors. (Directionally contested: `hedge-research.md` §11
                 records `PT50 killed across all configs except Scalp`, and the archived
                 tournament put Ride above the tight-cut arm — this arm exists to re-ask that
                 on post-cutover evidence, not to confirm it.)
MECHANISM        Converts a probabilistic tail into a booked mid-day gain, trading the last 50%
                 of decay for removal of late-day gamma risk. PRIMITIVE: the Ride base bundle
                 plus ONE field — Exit Options `profits` = 0.5, `smprofits` = speedy. Sibling
                 close means this is "PT50 on either side closes the CONDOR", not per spread.
KILL CRITERION   Exp(R) per condor < 0 with CI entirely below 0 at n ≥ 60. Plus family-level,
                 liveness and sentinel.
                 📝 AMENDED 2026-08-06 (G-8, SEQUENCE+CS, ruled by Andy) — the n≥60 read above is
                 emitted as an always-valid confidence sequence, not a fixed-n CI; the absolute
                 kill cannot fire before this arm's own stamped GATE EVAL DATE (below).
                 Family-level and sentinel criteria (execution-integrity rules) are unaffected.
GATE EVAL DATE   Day-0 + 6 months (relational; resolves to calendar at Day-0); interim look at
                 n=60.
VERIFICATION     A 50% profit-taking row in the first new position's Trades list.
SIGNED           ..............................
```

```
### GF-QQQ-IC-Trail
ID               PR-16  (proposed)
DISPOSITION      fresh build      PILLAR/ROLE  IC · experiment      STATUS  DRAFT — unsigned

HYPOTHESIS       A trailing stop on position profit raises Exp(R) per condor above BOTH the Ride
                 control and PT50, by letting winners keep decaying while holding a floor.
                 Judge on the LOSS TAIL and maxDD-R, not mean R — `hedge-research.md` §14.1:
                 the mechanic is nearly free on calm tape and bites in the fast-move tail, and
                 the tail is where IC losses already live.
MECHANISM        Ratchets a floor under an open profit instead of closing flat.
                 PRIMITIVE: the Ride base bundle plus ONE mechanic — Exit Options `tstop`
                 (+ its pricing sub-field, if it has one — C3).
                 ⭐ RE-SCOPED 2026-08-06, RULED BY ANDY, ON PHASE-0 CHECK C2. THE MECHANIC IS THE
                 ARMED TRAIL: Exit Options `tstop` sub-form, `target` = 40 ("Activate at 40 % of
                 credit"), `trail` = 15 ("Close on 15 % pullback"). Both are % of CREDIT / % of
                 pullback-from-high, read first-hand off the live sub-form
                 (data/captures/edit-verify/2026-08-06/phase0_C2.txt).
                 THE EXCLUSION BELOW IS FALSIFIED AND IS STRUCK: OA implements the armed trail as
                 a NATIVE exit primitive, so §11 rows 4 and 6 -- which bound what DECISION NODES
                 can express -- never applied to it. `maxtrail` ("Pullback is more than __ % from
                 high") is direct evidence the platform tracks a high-water mark natively.
                 §11 rows 4 and 6 themselves are untouched by this and still stand.
                 ⚠️ NOT OBSERVED, AND NOT TO BE ASSUMED: whether a PLAIN non-armed trail is
                 expressible at all (whether `target` may be left blank). `target` has min=0 and
                 a placeholder of 50. If the armed values above cannot be entered as specified,
                 STOP and return to Andy -- do not fall back to a plain trail by leaving a field
                 empty and hoping.
                 ~~⛔ THE MECHANIC IS SCOPED TO A PLAIN, ALWAYS-ON TRAILING STOP — a single field,
                 no arming threshold. AN "ARM AT 40%, THEN TRAIL 15%" SHAPE IS NOT SOUGHT AND
                 MUST NOT BE BUILT: that is a two-stage mid-trade state change, which §11 rules
                 out twice — "Regime-conditional branching at a breach | NOT NATIVE. No mid-trade
                 branching" and "Any condition referencing its own past | NOT NATIVE" — and it is
                 the same reasoning §3.1 uses to exclude the intraday stop-tightening schedule.
                 The draft treated the armed trail as an open question; the folder already
                 answers it against us, and the correction is recorded rather than absorbed.~~
                 ✅ `tstop`'s UNITS ARE NOW OBSERVED (C2, 2026-08-06): arming threshold in % of
                 CREDIT, trail in % PULLBACK from the high. hedge-research.md §14.1's standing
                 instruction is MET.
                 ~~⛔ `tstop`'s UNITS are still UNOBSERVED (§6.1a records the field as existing and
                 EMPTY). Phase-0 C2 settles them, and hedge-research.md §14.1's standing
                 instruction is unmet until it does: "Verify whether OA supports a true intraday
                 trailing stop on a 4-leg condor before assuming."~~
                 ⛔ IF C2 SHOWS NO PLAIN TRAILING STOP ON A 4-LEG CONDOR, DO NOT SUBSTITUTE
                 ANYTHING AT BUILD TIME. Named fallback: replace this arm with SL130 (Pearce,
                 ★★★★), re-stamp THIS pre-registration first, then build. That is the HedgeD
                 rule; −$15,376 is what ignoring it cost.
KILL CRITERION   Exp(R) per condor < 0 with CI entirely below 0 at n ≥ 60. Plus family-level,
                 liveness and sentinel.
                 📝 CORRECTED 2026-08-06 (G-12, RESPEC, ruled by Andy) — the worst-condor-R
                 retirement criterion below is STRUCK, PENDING RESPEC: it compared two sample
                 minima with no CI, no tolerance and no correction (P≈0.5 under the null,
                 `comparative-machinery-spec.md` §8, CM-19) and retired the arm on what was
                 arithmetically a coin flip worded as a refutation. REPLACEMENT (a tail quantile
                 with a CI) is not yet specified — Andy ruled RESPEC, not the concrete method; that
                 is a follow-up decision, not fabricated here. Until specified, this criterion does
                 not fire. Plus: ~~worst-condor-R worse than the Ride control's at
                 n ≥ 60 → the "no new risk" claim is refuted and the arm is retired.~~
                 📝 AMENDED 2026-08-06 (G-8, SEQUENCE+CS, ruled by Andy) — the n≥60 read above is
                 emitted as an always-valid confidence sequence, not a fixed-n CI; the absolute
                 kill cannot fire before this arm's own stamped GATE EVAL DATE (below).
                 Family-level and sentinel criteria (execution-integrity rules) are unaffected.
GATE EVAL DATE   Day-0 + 6 months (relational; resolves to calendar at Day-0); interim look at
                 n=60.
VERIFICATION     A trailing-stop row in the first new position's Trades list.
SIGNED           ..............................
```

```
### GF-QQQ-IC-Touch0
ID               PR-17  (proposed)
DISPOSITION      fresh build      PILLAR/ROLE  IC · experiment      STATUS  DRAFT — unsigned

HYPOTHESIS       Closing the condor on the first 1-minute evaluation at which either short
                 strike is ITM (this fleet's S2, sampled at the platform's cadence — NOT an
                 instantaneous touch; see §4.4 and §11 row 3)
                 raises Exp(R) per condor above the Ride control. The archived S2 diagnostic
                 (n=326 legs, 2026-06-10) found S2 MECHANICALLY sound — worst loss ror −0.47,
                 no −1.0 blowups, false-fires only 7 legs / −$400 — but EXPECTANCY-UNPROVEN,
                 and concluded the bleed was ENTRY, not the hedge. This arm re-asks expectancy
                 on post-cutover data. It is not a re-tune of the hedge to solve an entry
                 problem — `hedge-research.md` §4's standing rule forbids that.
MECHANISM        Caps the loss at first breach instead of at expiry.
                 PRIMITIVE: the Ride base bundle plus ONE field — Exit Options `touch` = $0.
                 Touch references the UNDERLYING relative to the position's own strike(s)
                 (§6.2, from OA's published material); $0 exits on the first 1-minute
                 evaluation at which the position is ITM. 📝 CORRECTED 2026-08-06 (C8 ruling): sibling-close is NOT
                 BUILT, so THIS ARM IS S1, NOT S2. A touch closes the touched SPREAD; the other
                 spread runs to its own 15:50 Expiration exit or the 15:52 backstop. Cross-leg
                 close is still NOT assumed. Original, left standing: ~~the condor is closed by
                 §4.3's Position-closed sibling automation, so this arm is S2-shaped, not S1.~~
                 ⚠️ Bid-Ask Guard is OFF on this arm (as on all arms) — §6.3: a touch hedge
                 silently suppressed exactly when the market is fast is the worst-timed failure
                 available.
KILL CRITERION   Exp(R) per condor < 0 with CI entirely below 0 at n ≥ 60. Plus family-level,
                 liveness and sentinel.
                 📝 AMENDED 2026-08-06 (G-8, SEQUENCE+CS, ruled by Andy) — the n≥60 read above is
                 emitted as an always-valid confidence sequence, not a fixed-n CI; the absolute
                 kill cannot fire before this arm's own stamped GATE EVAL DATE (below).
                 Family-level and sentinel criteria (execution-integrity rules) are unaffected.
GATE EVAL DATE   Day-0 + 6 months (relational; resolves to calendar at Day-0); interim look at
                 n=60.
VERIFICATION     A touch row at/after the underlying crosses the short strike.
                 📝 CORRECTED 2026-08-06: ~~plus a `sibling close` row on the second leg at
                 `:00`/`:00`~~ — VOID, that row will not exist (C8 ruling).
SIGNED           ..............................
```

```
### GF-QQQ-IC-SL100
ID               PR-18  (proposed)
DISPOSITION      fresh build      PILLAR/ROLE  IC · experiment (hedge arm)   STATUS  DRAFT

HYPOTHESIS       A stop at Sandvand's ~100%-of-credit level, APPLIED CLOSE-BOTH, raises Exp(R)
                 per condor above the Ride control. The rung is the SL spectrum's best-evidenced
                 (★★★★★, ~9,100 documented 0DTE SPX IC trades, Apr 2021 – Feb 2026) and the
                 fleet has never run it — the fleet's SL50 sits BELOW the lower bound of every
                 rigorously documented operator.
                 ⛔ TWO PRIORS THIS ARM IS RUN AGAINST, NAMED SO THE ARM IS NOT READ AS
                 CONFIRMATORY. (1) hedge-research.md §11, validated: "Stop losses are
                 counterproductive on the Fortress structure — sizing and hedging are the risk
                 management there." This family reuses the Fortress structure verbatim. §11 opens
                 "Confirm each still holds before relying on it," so re-asking is legitimate —
                 but the prior says this arm should lose, and it is recorded here rather than
                 omitted. (2) §5.1: every v1 arm's Exp(R) was negative INCLUDING no-hedge.
                 ⛔ THE ANCHOR DOES NOT TRANSFER CLEANLY, AND THE NAME IS WITHHELD BECAUSE OF IT.
                 Sandvand's rung is called "BREAKEVEN" because stopping the tested spread at
                 100% of credit leaves the UNTESTED side to decay to zero, netting ≈ $0 on the
                 condor. ⭐ RESOLVED 2026-08-06 BY THE C8 RULING: sibling-close is NOT BUILT, so
                 the untested side IS left to decay exactly as the anchor assumes. THIS ARM CAN
                 NOW REACH BREAKEVEN, the downward bias is removed, and CF-4 is DISCHARGED. The
                 arm may be read against Sandvand's rung on its own terms. Original objection,
                 left standing: ~~§4.3's sibling-close force-closes the untested side at its
                 then-current mid, so THIS ARM CANNOT REACH BREAKEVEN BY CONSTRUCTION and is
                 biased downward against its published comparable by the forfeited decay. This
                 arm is "SL100-close-both", not "Breakeven". Do not publish it under the anchor's
                 name.~~ ⚠️ The name is still withheld pending Andy's read of how it should be
                 published now that the construction objection is gone.
MECHANISM        Caps the loss at a level calibrated by the largest public 0DTE IC dataset.
                 📝 CORRECTED 2026-08-06: ~~wrapped in a close-both exit~~ — NOT close-both; the
                 stop closes the tested SPREAD only (C8 ruling, §4.3).
                 PRIMITIVE: the Ride base bundle plus ONE field — Exit Options `stoploss`.
                 ✅ THE UNIT OF `stoploss` IS CONFIRMED % OF CREDIT (C1, 2026-08-06): the control
                 is labelled "Stop Loss %" and its picker enumerates "-100% of credit" = 1.
                 THE RE-STAMP CONDITION IS NOT TRIGGERED — this entry was written against the
                 operator anchors' % OF CREDIT basis and the control matches it. RUNG: stoploss = 1.
                 ~~⛔ THE UNIT OF `stoploss` IS UNCONFIRMED. §6.1a records the field as existing
                 and EMPTY on the pilot; whether it is % of CREDIT or % of RISK is not
                 established anywhere in this folder, and the operator anchors are % of CREDIT.
                 Phase-0 check C1 settles it. IF THE CONTROL IS %-OF-RISK, THE RUNG VALUES ARE
                 RE-DERIVED AND THIS ENTRY IS RE-STAMPED BEFORE BUILD — not adjusted after.~~
KILL CRITERION   Exp(R) per condor < 0 with CI entirely below 0 at n ≥ 60. Plus family-level,
                 liveness and sentinel.
                 📝 AMENDED 2026-08-06 (G-8, SEQUENCE+CS, ruled by Andy) — the n≥60 read above is
                 emitted as an always-valid confidence sequence, not a fixed-n CI; the absolute
                 kill cannot fire before this arm's own stamped GATE EVAL DATE (below).
                 Family-level and sentinel criteria (execution-integrity rules) are unaffected.
GATE EVAL DATE   Day-0 + 6 months (relational; resolves to calendar at Day-0); interim look at
                 n=60.
VERIFICATION     A stop-loss row in the first new position's Trades list.
SIGNED           ..............................
```

```
### GF-QQQ-IC-SL200
ID               PR-19  (proposed)
DISPOSITION      fresh build      PILLAR/ROLE  IC · experiment (hedge arm)   STATUS  DRAFT

HYPOTHESIS       A stop at Chambless's SL200 raises Exp(R) per condor above the Ride control —
                 AND, the second question this arm answers, SL200 does NOT collapse to the Ride
                 arm. `hedge-research.md` §2.1: above ~200% is effectively no-stop on a $5-wide
                 SPX IC; whether that also holds on a $2-wide QQQ condor is unknown and is
                 directly measurable here, because Ride is a matched sibling.
MECHANISM        As PR-18, at the loose end of the documented spectrum.
                 PRIMITIVE: the Ride base bundle plus ONE field — Exit Options `stoploss`.
                 ✅ C1 ANSWERED 2026-08-06 — % OF CREDIT. RUNG: stoploss = 2 ("-200% of credit").
                 The re-stamp-before-build rule is NOT triggered.
                 📝 CORRECTED 2026-08-06: this arm is likewise NOT close-both (C8 ruling).
KILL CRITERION   Exp(R) per condor < 0 with CI entirely below 0 at n ≥ 60 matched days. Plus
                 family-level and sentinel.
                 ⭐ LIVENESS IS DISAPPLIED ON THIS ARM, DELIBERATELY. The shared liveness rule
                 kills an arm that stops firing — but "SL200 rarely fires" IS this arm's
                 hypothesis (hedge-research.md §2.1: "Above ~200% is effectively no-stop"). The
                 draft's version would have switched the arm off precisely when it was
                 CONFIRMING itself. Replaced by the degeneracy criterion below, which measures
                 the same thing in the right direction.
                 📝 ADDED 2026-08-06 (G-5, DISAPPLY, ruled by Andy) — GATE-CM CONJUNCT (c) IS
                 ALSO DISAPPLIED ON THIS ARM, the deliberate parallel to the liveness
                 disapplication above: conjunct (c) is an exact sign test on the fired
                 subpopulation, unpassable by construction when the arm's hypothesis is that it
                 rarely fires (`comparative-machinery-spec.md` §8, CM-8). With conjunct (a)
                 already inert at this family's K and n (G-6), this arm's gate reduces to
                 conjunct (b) alone — a single bootstrap CI. Chosen, not arrived at.
                 📝 CORRECTED 2026-08-06 (G-13, REPLACE-EQUIV, ruled by Andy) — the degeneracy
                 criterion below is STRUCK AS UNFIREABLE: at the family's declared paired daily
                 SD ≈ 0.134R, P(|d| ≤ 0.005) ≈ 0.030, so the expected count in a 40-day window
                 is ≈ 1.2 against a requirement of 20 (`comparative-machinery-spec.md` §8, CM-9).
                 REPLACED BY a TOST equivalence test on mean paired ΔR vs the Ride control,
                 equivalence band ±0.015R (the program's R-3 minimum-effect margin, signed by
                 Andy 2026-08-06 as the band), evaluated ONCE, at this entry's GATE EVAL DATE.
                 ⭐ DEGENERACY CRITERION, REWRITTEN TO BE FIREABLE: ~~if this arm's per-condor R
                 is within ±0.005R of the Ride control's on ≥ 20 of any 40 consecutive MATCHED
                 days, AND its stop-loss row count over that window is 0, the arm carries no
                 information and is retired.~~
                 ⛔ The draft's version — "identical P/L, structure and entry minute" — was
                 unfireable three times over: identical P/L is impossible given H1's independent
                 fills; identical entry minute is impossible given §4.2's parallel work queue;
                 and no rule implementing it exists (the nearest, rule_S7_duplicate_arm, is
                 post-hoc, outcome-based, AMBER and silent below 5 identical days). The version
                 above uses a TOLERANCE and a CONFIG-BACKED second condition, both computable
                 from the ledger the daily loop already writes.
                 📝 AMENDED 2026-08-06 (G-8, SEQUENCE+CS, ruled by Andy) — the n≥60 read above is
                 emitted as an always-valid confidence sequence, not a fixed-n CI; the absolute
                 kill cannot fire before this arm's own stamped GATE EVAL DATE (below).
                 Family-level and sentinel criteria (execution-integrity rules) are unaffected.
GATE EVAL DATE   Day-0 + 6 months (relational; resolves to calendar at Day-0); interim look at
                 n=60.
VERIFICATION     A stop-loss row in the first new position's Trades list.
SIGNED           ..............................
```

> ### 📝 APPENDED 2026-08-06 — double-testing RULED, RETIRE-SCOPED (PR-18/PR-19 vs Track A's signed SL100/SL200). Applied on Andy's explicit "amend the plan" (`decision-card-2026-08-06.md` ruling 5).
> §12 row 11's finding — `GF-SL100`/`GF-SL200` duplicate signed `research-loop-spec.md` §3
> variants and pool error rates nowhere — is resolved by **scoped retirement, the R-2 precedent**:
> `research-loop-spec.md` §10a now excludes these two (bot, variant) pairs from Track A's computed
> family, so PR-18/PR-19's own ledgers no longer re-enter Track A's family carrying their own
> variant. **This is not a claim that Track A and these arms test the same thing.** PR-18's
> ⚠️ **CORRECTED 2026-08-06 — THIS PARAGRAPH'S STATED REASON IS NARROWED BY THE C8 RULING, WHICH
> POSTDATES IT. The retirement ruling itself is UNCHANGED and stands.** With `GF-SiblingClose` not
> built, these arms are **no longer close-both** — the stop closes the tested spread only, i.e.
> **per-spread, the same exit unit as Track A's counterfactuals**. The close-both leg of the
> non-equivalence argument therefore **falls away**. What survives it: a **different incumbent**, a
> **different engine**, and the **self-comparison degeneracy** the retirement was granted to remove.
> ⛔ **FLAGGED FOR ANDY — not resolved here:** whether the surviving grounds alone still support
> "non-equivalent estimands". This edit records the falsified premise; it does **not** re-rule the
> retirement, which is Andy's. Original, left standing: ~~HYPOTHESIS block above already
> establishes the arms as **close-both** mechanics (`SL100-close-both` / by extension
> `SL200-close-both`) — Track A's `SL100`/`SL200` counterfactuals are computed **per-spread**,
> against a different incumbent. The two remain non-equivalent estimators;~~ retirement removes a degenerate self-comparison, not a duplicate
> measurement. **No-influence rule:** a Track A advisory read on `SL100`/`SL200` may not trigger,
> accelerate, or veto either arm's disposition before that arm's own pre-declared gate date; kill
> authority stays with each arm's own pre-registered criteria (this entry's KILL CRITERION line).
> No cross-engine multiplicity accounting exists or is created by this ruling — within-family
> multiplicity stays with Phase C step C4's ~~Bonferroni-across-6~~ **joint day-bootstrap max-T
> (SWITCHED 2026-08-06, G-10, ruled by Andy)**; Track A's stays with §10a's max-T.

```
### GF-QQQ-IC-Canary
ID               PR-20  (proposed)
DISPOSITION      fresh build      PILLAR/ROLE  IC · control (instrument)     STATUS  DRAFT

HYPOTHESIS       Not a strategy hypothesis — an INSTRUMENT hypothesis. A bot whose 5% profit
                 target should fill every single day will stop filling the day the exit engine
                 dies, giving SAME-DAY detection of the failure that ran six invisible sessions
                 in v1. `build-plan.md` §2D: `whose PT should fill every single day. If it stops
                 filling, the exit engine died.`
MECHANISM        n/a — this bot is NOT run for edge. Its P/L is expected to be ~flat and is not
                 evidence about anything. PRIMITIVE: the Ride base bundle plus ONE mechanic —
                 Exit Options `profits` = 0.05, `smprofits` = speedy.
                 ⚠️ THE THRESHOLD IS SUB-TICK, AND THAT IS STATED RATHER THAN DISCOVERED. 5% of
                 the admissible credit range is $0.004–$0.0075, below QQQ's $0.01 increment, and
                 §6.4 evaluates Exit Options on the MID. So the effective trigger is "the first
                 tick of favourable movement", set by the tick grid and the quoted spread, not by
                 the number 0.05. That is acceptable FOR A CANARY — it is what makes it fill
                 daily — but it means a no-fill day is AMBIGUOUS between "the exit engine died"
                 and "the spread widened by a cent." The instrument's false-negative rate is
                 UNMEASURED, and that is a real limit on the only forward discriminator this
                 project has for candidate 2 of the June-lapse shortlist (a platform-side
                 regression in the Exit Options engine) — which remains the argument for building
                 it in the FIRST wave rather than treating it as optional.
KILL CRITERION   NONE ON P/L. Exempt by design, stated here so it cannot later be mistaken for a
                 losing bot nobody killed. Retired when the detector's Tier C rules cover the
                 same ground with a live config.
                 ⭐ BUT IT CARRIES A CODE-FIREABLE ALERT, added under review: no profit-taking
                 fill on ≥ 2 consecutive days on which it held a position → RED, escalated in
                 the brief as a candidate exit-engine failure. pre-registration-ledger.md §2
                 requires every kill criterion to "fire in code with no human in the loop"; a
                 detector whose own failure rule is human judgement is the thing it exists to
                 prevent. It also carries the family-level and sentinel criteria.
SAMPLE TARGET    n/a — daily fill / no-fill is the output.
REVIEW DATE      Day-0 + 3 months: is it still earning its slot?
GATE EVAL DATE   Day-0 + 6 months (relational; resolves to calendar at Day-0); interim look at
                 n=60.
VERIFICATION     A profit-taking fill on DAY 1, read from the Trades list.
SIGNED           ..............................
```

---

## 10. Build order — executable per-bot, zero design decisions left open

*Every step ends in a **two-layer verification** per `oa-ops-runbook.md` §4. Layer 1 is the
immediate self-check: re-observe the changed value **from OA itself** — a fresh screenshot for
toggle/UI state, a fresh capture or export for text-capturable fields. **A save confirmation, a
toast, or a tool-success message is never Layer 1** (`CLAUDE.md` §9.1a). Layer 2 is the
behavioural check: the first NEW position's Trades list.*

> ⏸ **Layer 2 is DEFERRED to Day-0 for every step in this build.** The OA account is INACTIVE
> and holds no post-cutover positions, so order-level verification is **impossible on build
> day** — the pilot card's rule. Do not attempt a test-fire. Every deferred Layer 2 is **queued
> and tracked**, and per `CLAUDE.md` §5 it is **repeated at the top of every brief until closed**.

> ⚠️ **Method warnings, all first-hand, all reproduced on this app.** Element-ref clicks
> **silently no-op** — `computer.left_click` returns `Clicked on element ref_N` and nothing
> happens. Dispatch the full sequence instead:
> `pointerdown → mousedown → pointerup → mouseup → click`, each a `MouseEvent` with
> `bubbles:true, cancelable:true, view:window` and `clientX`/`clientY` at the element's
> `getBoundingClientRect()` centre. Use `form_input` for text, never `computer.type`, and re-read
> `.value` after every entry. **If an action resists all three methods, STOP — do not fall back
> to coordinates.** Notes editors decode entities then strip unknown tags: double-escape
> (`&amp;lt;`) and verify every paste by a **byte-exact length-and-content compare**, not by
> reading the rendered panel.

### Phase 0 — blocking checks. No value is stamped until every one is answered.

Each is a read, not a write. Each has a named outcome and a named fallback. **If a check cannot
be answered, STOP and report — do not improvise a spec on the fly.**

> ### ✅ PHASE 0 PARTIALLY ANSWERED — 2026-08-05, the C0a probe session.
> **Rows are marked in place below; original check text is LEFT STANDING per this file's convention.**
> Evidence: first-hand DOM / client-model reads on two delete-list scratch bots
> (`BOTfw5TkkCRF2217852702121253931`, `BOTfw5TkkCRF4517755136823526783`), each taken **after a hard
> reload**, never from a save banner (`CLAUDE.md` §9.1a). Full record with verbatim payloads:
> `session-log.md` 2026-08-05 part 2.
>
> **⭐ C0a PASSES ON BOTH CLAUSES — Architecture E is buildable. The build is no longer blocked on it.**
> ✅ **C0a · C3 · C4 · C5 · C6** answered · ⚠️ **C1 PARTIAL** · ⚠️ **C0b yes-by-implication, one direct
> look still worth it** · ⛔ **C10 (`dstop` unit, this spec's sibling check in `track-b-arms-spec.md`
> §10) REMAINS OPEN and blocks ARM-B1 to a Day-0 behavioural read** · **C11 ANSWERED** (`smdstop`
> exists, defaults `normal`) · **untouched: C0c · C2 · C7 · C8 · C9.**
>
> ⚠️ **NEW BUILD CONSTRAINT, not a check — the G2 rider is now TWO hops.** With a bot input in the
> chain the binding stores only the bot input's **id and label** plus a stale `oldValue`. Step **B4**
> and §8.2's diff must resolve action → automation input → **bot input** or every arm diffs identical.

| # | Check | If it fails |
|---|---|---|
| ~~**⛔ C0a**~~<br>✅ **PASS 2026-08-05 — BOTH CLAUSES.** Bot input `IN178588971538691`, **`type:"exits"`** (whole bundle), survived hard reload. Control lives on the **bot's** automation row → ⚙ Edit Settings → 🔗 → menu `Bot Inputs` → `Add Bot Input`, **not** in the automation editor. Clause two: shared Library automation `rid RTfw5TkkCRF178589028977611` + automation input `IN178589048006251` **identical on both scratch bots**, bot inputs **distinct** (`Profit: 25%` vs `Profit: 75%`). **Attach, not copy.** | **THE LOAD-BEARING ONE. Can an Exit-Options Automation Input be upgraded to a BOT INPUT, and can two bots resolve the same shared automation to DIFFERENT values?** Build it on two dead bots and read both. | ⛔ **STOP. Architecture E is not buildable and the tournament architecture returns to Andy.** Do **not** fall back to per-arm copies — `pre-registration-ledger.md` PR-18's kill criterion voids the tournament at build time under copies (memo Decision 4: *"under C the tournament is void on day one, before it trades"*). |
| ~~**⛔ C0b**~~<br>✅ **CLOSED 2026-08-06 — THE LITERAL TEST WAS RUN. THE ANSWER IS NO.** On `HedgeC-Scan-Call`'s Open Position action, the Exit Options 🔗 Inputs panel reads verbatim *"Select an existing input or add one to **your automation** for this value."* and **"No compatible inputs found."** — `CLAUDE-G1-EMPTY-EXITS` (`IN178586615441261`), an `exits`-typed **automation** input on the sibling automation `HedgeC-Scan-Put` **on the same bot**, is **not offered**. Type-compatible, same bot, not listed. **The two-input design of §4.1 stands and assert A8 stays SUBSTANTIVE.** [FIRST-HAND 2026-08-06 — `phase0_C0bc.txt`]<br>⚠️ **YES BY IMPLICATION 2026-08-05, NOT DIRECTLY TESTED.** One BOT input (`CLAUDE-C0A-BOT-EXITS`) was offered for reuse by a **second, different** automation on the same bot. The literal question — one AUTOMATION input spanning two automations — was not run. **Worth one direct look before B4.** | **Can ONE Automation Input be referenced from TWO automations** (ScannerA and ScannerB)? | Expected NO — proceed with the two-input design of §4.1, and assert **A8** (put bundle == call bundle) nightly. Not a blocker, but it changes the build and the diff. |
| ~~**C0c**~~<br>✅ **ANSWERED 2026-08-06 — YES, IT DOES.** The bot-input value editor opens the Exit Options modal, whose header carries a **`Presets`** control; opening it enumerates the account-scoped preset `TIER2-CHECK4-PUTSIDE` = **`UIfw5TkkCRF1517858152565216101`** (the `UI…` namespace, matching §9 row 4). The same modal also carries **"Save as presets for short option positions"**, so presets can be **created** from the input editor too. **§4.5's typo-reduction survives; B4 does NOT become seven manual entries; A6 is executable from this screen.** [FIRST-HAND 2026-08-06 — `phase0_C0bc.txt`] | **Does a `Presets` picker render inside the BOT INPUT value editor**, or only on the Open Position action? G3 tested the action. | §4.5's typo-reduction disappears and B4 becomes seven manual field-by-field entries — **hand-setting, the pathogen of §1.1, at the one place the design still touches values by hand.** Compensate by running the §8.2 diff after *each* arm rather than at the end. |
| ~~**C1**~~<br>✅ **CLOSED 2026-08-06 — `% of CREDIT`.** The control's own label is **`Stop Loss %`** (`input[name="stoploss"]`), and its picker enumerates credit: `-5% of credit`→`0.05` … `-100% of credit`→`1` … `-200% of credit`→`2` … `-500% of credit`→`5` (5% steps to 100%, 10% to 200%, 25% beyond; 42 entries, every one negative). **SL100 = `stoploss: 1`, SL200 = `stoploss: 2` — both exactly selectable, no re-derivation needed.** ⭐ **PR-18/PR-19's re-stamp condition is NOT triggered**: both entries name `% of CREDIT` as the operator-anchor basis and make re-stamping conditional on *"IF THE CONTROL IS %-OF-RISK"*. `dstop` is a **separate** control labelled `Stop Loss $` — that is C10's subject and stays open. [FIRST-HAND 2026-08-06 — `phase0_C1.txt`]<br>⚠️ **PARTIAL 2026-08-05 — NOT CLOSED.** What was read is **Profit Taking %**, whose picker enumerates `% of credit` (`50% of credit` → `profits: 0.5`). **`stoploss`'s own unit — this row's literal subject — was NOT read.** SL100/SL200 stay underived. | **Unit of Exit Options `stoploss`** — read the control's own label and any suffix on the live modal. % of CREDIT or % of RISK? | Re-derive the SL100/SL200 rungs on the actual basis and **re-stamp PR-18/PR-19 before build.** |
| ~~**C2**~~<br>✅ **CLOSED 2026-08-06 — AN ARMING THRESHOLD EXISTS, AND IT IS NATIVE.** `tstop` is **not a scalar** — it opens a sub-form headed `Trailing Stop` with four number inputs: **`target`** (min 0, step 1, placeholder 50) rendered **"Activate at __ % of credit"** — *the arming threshold*; **`trail`** (min 1, step 1, placeholder 15) rendered **"Close on __ % pullback"**; plus two optional disable conditions, **`minr`** ("Return % is less than __ % of credit") and **`maxtrail`** ("Pullback is more than __ % from high"). Buttons Cancel / Clear / Apply. **The backtester's "arm @ 40%, trail 15%" maps directly: `target`=40, `trail`=15.** ⭐ **This falsifies the exclusion of the armed shape** — `§11` rows 4 and 6 bound what DECISION NODES can express, not what a native exit primitive does internally, and `maxtrail` is direct evidence the platform tracks a high-water mark natively. **RULED 2026-08-06 (Andy): PR-16 IS RE-SCOPED TO THE ARMED TRAIL.** ⚠️ **NOT observed:** whether a *plain* non-armed trail is expressible (whether `target` may be left blank) — do not assume it. [FIRST-HAND 2026-08-06 — `phase0_C2.txt`] | **Unit and shape of `tstop`** — %? $? Does an ARMING threshold exist (the backtester's "arm @ 40%, trail 15%")? | If no armed trail is expressible: **replace the Trail arm with SL130, re-stamp PR-16 first.** Do not substitute silently. |
| ~~**C3**~~<br>✅ **ANSWERED 2026-08-05 — YES, and the default is `normal`, NOT `market`.** Every exit mechanic carries an `sm*` sibling: `smprofits · smdprofit · smprice · smstoploss · smdstop · smtstop · smtouch · smexpdays · smxevents · smepsdays`, each defaulting to `{"limitType":"pct","limit":100,"smart":"normal","text":"100% of bid/ask"}`. **No arm inherits `market`; §7 and Decision 5 are not tripped.** | **Do `tstop`, `touch` and `stoploss` carry their own SmartPricing sub-controls** (as `profits`→`smprofits` and `expdays`→`smexpdays` do), or inherit a default? **What is that default?** | ⛔ If any inherits **`market`**, that arm violates §7 and Decision 5 *and* confounds the family with a pricing difference. **Stop. Report. Do not build that arm.** |
| ~~**C4**~~<br>✅ **ANSWERED 2026-08-05 — YES, a fixed CONTRACT COUNT is selectable.** The Open Position action's Position Size defaulted to **`1 contract`**. §5.4's `Up to $250 risk` arithmetic is a **choice, not a necessity** — record which primitive is used in all seven MECHANISM blocks either way. | **Size control options** on Open Position — is a fixed CONTRACT COUNT selectable? | Use `Up to $250 risk` (§5.4 arithmetic). **Record which primitive was used in all seven MECHANISM blocks before build.** |
| ~~**C5**~~<br>✅ **PASS 2026-08-05.** `CLAUDE-C5-SHARED-SCRATCH` attached to both scratch bots; both instances resolve to the **same `rid RTfw5TkkCRF178589028977611`**; library page reads `2 bots`, one row. **Attach, not copy — confirmed.** | **Can one Library automation be attached to N bots?** Attach `GF-ScannerA` to two dead bots and re-read both bots' automation lists for the SAME `rid`. | ⛔ Architecture E is not buildable. **STOP — the tournament architecture returns to Andy.** Do not fall back to per-arm copies: `pre-registration-ledger.md` PR-18's kill criterion voids the tournament at build time under copies. |
| ~~**C6**~~<br>✅ **ANSWERED 2026-08-05 — YES, non-empty is accepted.** The C0a bot input persisted `profits: 0.5` + `dstop: {"value":-137}` + `smdstop` through a hard reload. **§1.3's silent-fallback objection does not stand in full; a distinctive non-empty sentinel IS expressible.** | **Does a bundle-typed Automation Input accept a Default Value that is a non-empty bundle** (`SENTINEL-SL1`)? G1 proved EMPTY is accepted; non-empty is not proven. | If only empty is accepted, the sentinel becomes the empty bundle **and §1.3's objection stands in full** — record it as an accepted silent-fallback risk in every entry, and rely on A4b's behavioural detector alone. |
| ~~**⛔ C7**~~<br>✅ **PASS 2026-08-06 — IT IS A REAL NODE, VERBATIM.** Recipe **`postagtoday`**, group `Bot`, format `Bot [oc: opened|closed, default "opened"] a position with [tag: tags, limit 1] today`. Bot-scoped, tag-scoped and day-scoped, exactly as §4.1's tree assumes. ⭐ **Corroborated as already running on this account, not merely available:** `HedgeC-Scan-Call` contains the live node **"Bot opened a position with call side today"** whose `NO` branch leads to `Open QQQ Short Call Spread`. **No STOP, no substitution.** [FIRST-HAND 2026-08-06 — `phase0_C7.txt`] | **Is `Bot opened a position with tag <side> today` a real decision node** — bot-scoped AND day-scoped? It is one of the two enforcers of the one-condor-per-day cadence and it is sourced from the pilot's tree, not from the platform reference. | ⛔ **STOP.** `oa-ops-runbook.md` §5 trap 7 is this exact failure — *"A time gate that was never implemented — the v1 11:00 gate did not exist; 20+ sessions of entry drift."* If "today" is not expressible, the nearest substitutions (an unscoped tag → never re-enters; a position-count gate → different semantics) change the family's entry behaviour on all seven bots identically, which is precisely the failure the arms cannot detect. |
| ~~**⛔ C8**~~<br>⛔ **STOP RETURNED 2026-08-06 — CLAUSE 2 IS NOT EXPRESSIBLE. Clauses 1 and 3 pass.** **Clause 1 ✓** `posrepeater` ("Positions — Run subsequent actions for open positions") IS available inside a `Position closed` automation; built, renders "Repeat for each position". **Clause 3 ✓** `posopendays` = `[position] has been open [cop] [days]` carries `zero:true`, so "open **0 market days**" is the opened-today scope. **Clause 2 ⛔ — the closed position is not an addressable referent.** The position picker in a closepos automation offers exactly two entries under `Bot`: **"Lookup a position"** (a `Position Lookup` sub-form — *"Finds the first position that matches these filters"*, Symbol / Position Type / Tag, all **literal**) and **"Opened Position"**, greyed, with OA's own copy *"**Only available in automations scheduled with the "position opened" trigger**"*. **There is no "Closed Position" entry.** Inside the loop the referent auto-binds to the looped position (`em.ex.output.n-posrepeater`) with no picker at all. And **no recipe compares a tag to another position's tag** — `postag` takes a literal tag list; `posprop2prop` compares numeric `posprop`s only. **Scopes opened** (so this is not inference from absence): bot scope · automation scope · the referent picker at top level · the binding inside the loop · the Position Lookup sub-form · **all 127 recipes across all 6 groups**. The enumeration is closed and the exclusion is stated in OA's own copy. ⭐ **RULED 2026-08-06 (Andy): TAKE THE NAMED FALLBACK — BUILD WITHOUT SIBLING-CLOSE.** See §4.3. [FIRST-HAND 2026-08-06 — `phase0_C8.txt`] | **Are §4.3's sibling-close nodes real?** A Positions loop inside a `Position closed` automation; a comparison of a looped position's **side tag** against the closed position's; and an **opened-today** scope. | ⛔ **STOP. Do NOT substitute position age** (`open 30 minutes or more`) — that is the literal substitution that cost −$15,376. Named fallback: **build the family without sibling-close**, accept the spread (not the condor) as the unit for early exits, and re-stamp all seven MECHANISM blocks before build. |
| ~~**C9**~~<br>⏳ **NOT ANSWERABLE IN THE UI — DAY-0 BEHAVIOURAL READ, same class as C10.** The only copy the app offers is the trigger's own description, verbatim **"After the bot closes a position"** (slot counter `0/5`, no help control). The closepos trigger's settings expose only a **`Position Type`** filter — there is **no "closed by" filter** — and no recipe in the 127-recipe catalogue distinguishes the provenance of a close. **Scopes opened:** the Add-Automation schedule picker (all 12 trigger types with descriptions) · the closepos trigger's own settings · the full recipe catalogue. ⚠️ That the copy says "the **bot** closes" reads as excluding the *account-level* ITM action — recorded as **suggestive and INADMISSIBLE** (`CLAUDE.md` §5). ⭐ Under the 2026-08-06 C8 ruling the 3:44pm-gate half of this check is **moot**; the second-legs-open-at-15:50 half survives and still needs Day-0. [2026-08-06 — `phase0_C9.txt`] | **Does the `Position closed` trigger fire on a position closed by an EVENTS-class automation and by the account-level ITM action**, or only by Exit Options? | Changes whether §4.3's 3:44pm gate is needed at all, and whether second legs are left open at 15:50 on early-exit arms. Read it; do not infer it. |

> ### ⛔ C10 — `dstop`'s UNIT — IS OPEN AND BLOCKS ARM-B1. Recorded here because it gates a Track B
> arm that shares this family's controls. **Read 2026-08-05:** the modal is headed `Stop Loss Amount`,
> the only unit marker is a bare `$`, `step=1`, **no min, no max, no suffix, no helper text, no
> tooltip, and no per-contract / per-position / per-leg qualifier anywhere on the control.** OA's own
> rendered label is `"Stop Loss: -$137"`. The prescribed method returns nothing. That `dstop` persists
> as a **negative** number is *suggestive* of a position-level P/L threshold and is **inadmissible as
> the answer** — inference from a sign convention is not an observation (`CLAUDE.md` §5).
> **Needs a Day-0 behavioural read against a known contract count.** Until then `<D100>` is underived
> and PR-21 is unstampable. Owner: `track-b-arms-spec.md` §10 C10.

> ### ✅ PHASE 0 CLOSED 2026-08-06 — the second probe session. Every remaining check that is
> answerable in the UI is answered. **The 2026-08-05 block above is LEFT STANDING; rows are marked
> in place below.**
> Evidence: first-hand DOM / value-layer reads, all on the delete-list scratch bot
> `BOTfw5TkkCRF2217852702121253931`, filed to
> `data/captures/edit-verify/2026-08-06/phase0_C1.txt · _C2 · _C7 · _C8 · _C0bc · _C9`.
> Full record: `session-log.md` 2026-08-06.
>
> ✅ **C1** `% of CREDIT` · ✅ **C2** an **armed** trail is native · ✅ **C7** the node is real and is
> already running on this account · ✅ **C0c** the Presets picker IS in the input editor ·
> ✅ **C0b literal** — **NO**, one automation input cannot span two automations ·
> ⛔ **C8 clause 2 — STOP** · ⏳ **C9** and the runbook §7 template check — not answerable in the UI.
>
> ⭐ **THE THREE "NOT ARMS YET" ARE NOW ARMS.** C1 confirms SL100/SL200's primitive and C2 confirms
> Trail's; C3 closed the pricing sub-field on 2026-08-05. §8's table row 4 is corrected accordingly.
>
> ⛔ **C8's STOP IS FAMILY-WIDE, NOT AN ARM CUT** — it removes a *shared object*. **RULED 2026-08-06
> (Andy): take the spec's named fallback — BUILD WITHOUT SIBLING-CLOSE.** See §4.3's ruling banner.

**Layer 1 for Phase 0:** each answer is a fresh screenshot or DOM read filed to
`data/captures/edit-verify/<date>/phase0_C<n>.png|.txt`, with the read value written into the
session log. **Nothing is answered from memory or from this document.**

### Phase A — the shared objects (build once)

| Step | Do | Layer 1 verification |
|---|---|---|
| **A1** | Create Automation Input `GF_EXITS_PUT` on `GF-ScannerA-PutSpread` (and `GF_EXITS_CALL` on ScannerB at A3); set each **Default Value = `NONE`** 📝 **AMENDED 2026-08-06 — was `SENTINEL-SL1`, struck by the F-4 ruling (§1.3a); done for ScannerA in the first Phase A pass, carry forward for ScannerB** | Fresh capture; read each input object's default back and decode it (expect unset/None, not a bundle). Screenshot the 🔗 state on the Exit Options row |
| **A2** | Build `GF-ScannerA-PutSpread` per §4.1, every field. **Entry pricing SmartPricing `normal`, NOT Market** | Fresh capture with **every caret expanded** (trap 3). Diff every field against §4.1's table, reading `input.value` / `data-value`, **never `innerText`** |
| **A3** | Build `GF-ScannerB-CallSpread` — mirror image, own `GF_EXITS_CALL` input (or the shared one if C0b said yes) | As A2, plus record whether the two actions reference the same or different input ids — this sets whether A8 is substantive or trivial |
| ~~**A4**~~ | ⛔ **STRUCK 2026-08-06 — DO NOT BUILD. C8 ruling (§4.3): the family is built without sibling-close.** Original step left standing: ~~Build `GF-SiblingClose` per §4.3 — **Positions loop, 3:44pm gate (amended 2026-08-04, NOT 3:50pm), side-tag comparison, opened-today, `patient` pricing, memo** — **and test it on a dead bot first** | Fresh capture; confirm **each gate is an actual decision node**, not assumed (trap 7). Then fire it on the dead bot and read the resulting Trades list: exactly one close, no re-trigger. **This is now load-bearing, because the platform-level limit defence does not apply to closes** (§4.3)~~ |
| **A5** | Build `GF-Backstop-1552-FlatClose` per §4.2 | Fresh capture + **hard reload**; read `ntime=1552`, `holidays=skip`, memo string, `Market`, warnings 0 |
| **A6** | Save the seven exit-bundle presets of §4.5 (skip if C0c said the picker is absent from the input editor) | Re-open each from the picker on a **different** automation and read its decoded payload back |
| **A7** | ⭐ **Record the payload hash of each of the ~~four~~ **THREE** shared automations** as the A7 baseline (📝 **three, not four, 2026-08-06** — A4 is struck) | Hash written to `data/bots_config_v2.csv`'s shared-object rows; re-read and re-hash once after a hard reload to confirm stability |

### Phase B — per arm, seven times, in this order: Ride first, then PT50, Trail, Touch0, SL100, SL200, Canary

*Ride first because it is the control and every other arm is its base plus one field. Canary last
because it is an instrument, not an arm.*

| Step | Do | Layer 1 verification |
|---|---|---|
| **B1** | Create the bot. Name per §3 | `/bots` read-back: exactly one bot with that name, resolving to one bot_id. Trap 8 — read the **full** name |
| **B2** | Set every bot-level setting of §5 — allocation `$2,500`, limits 2/2, scan 1m both, Day Trading Allowed, Group `IC`, tags per §5.1 | Fresh capture of the settings page; **assert values, not presence** (§4.5 — a broken input link does not error, it falls back to a stale Default and keeps trading) |
| **B3** | Attach the ~~four~~ **three** shared Library automations from Phase A (📝 **three, 2026-08-06 — C8 ruling**). **Attach, do not copy** | Read the bot's automation list and confirm the `rid` values are **identical to Phase A's objects.** A different `rid` means a copy, and a copy breaks Architecture E |
| **B4** | Create the **Bot Inputs** `GF_EXITS_PUT` and `GF_EXITS_CALL` on this bot and set **both** to this arm's bundle (§4.4), loading from the arm's preset if C0c allows | ⛔ **Read back BOTH BOT INPUT OBJECTS' values and DECODE them** — not the action (which holds a reference), not `oldValue`. Compare field-by-field against §4.4, **and assert put == call** (A8). Hard reload, then read again |
| **B5** | Confirm `EXIT OPTIONS` toggle ON, `AUTOMATIONS` toggle **OFF** | **Screenshot both toggles** — §1.6, this is the one config state that does not survive text capture. File to `data/captures/edit-verify/<date>/<bot>_toggles.png` |
| **B6** | Take the arm's full capture into `data/captures/<date>-greenfield/<bot>/` | One `.txt` per automation; open one and confirm **actual decision text** is present, not just names |
| **B7** | Write the arm's row into `data/bots_config_v2.csv` — including the **decoded** bundle from B4 | Re-read the row; assert the decoded bundle matches B4's read |
| **B8** | Save **Template V1**; paste the arm's §9 entry verbatim into **Notes**; set template tags `experiment,pr nn,gfam` | **Byte-exact length-and-content compare** of Notes against the source (the pilot lost `<capture>`/`<hash>` silently and it was caught only by a 1574-character compare). Re-read `input[name=tags].value` after a hard reload. Then confirm the bot's settings page gained its `Template / BOT VERSION` panel |

> ⚠️ **Templates are not a config snapshot here, and under Architecture E they are less of one
> than usual.** Template rows carry the same `rid` as the live automation, and this family's
> automations are **shared across seven bots** — so a later edit to one shared automation changes
> all seven bots and may change all seven templates, with no template version bump to show it.
> **The capture (B6) and the nightly assert (§8.3) are the only detectors.** This is a designed
> consequence of Architecture E and is the strongest argument for §8.3 being a precondition.

### Phase C — the proof

| Step | Do | Verification |
|---|---|---|
| **C1** | Run the pairwise capture-diff of §8.2 across all **21 unordered pairs**, plus the intra-arm put==call test on each of the seven | Every pair PASSes on all four conditions, or the family does not trade |
| **C2** | Build and run the §8.3 nightly assert (rules **A1–A8**) against `bots_config_v2.csv` | All eight green. ⏳ **Whether this must precede trading is one of the memo's four NOT-RULED slots** — this spec places it before Day-0 |
| **C3** | ⭐ Record the shared-automation payload hashes as the **A7 baseline** and wire A7 into `daily.sh` | Baseline re-read and re-hashed after a hard reload |
| **C4** | ⭐ Declare and record the analysis convention: **paired by day, matched days only**, ~~Bonferroni across the 6 arm-vs-control tests~~ **SWITCHED 2026-08-06 (G-10, ruled by Andy) to a joint day-bootstrap max-T across arms — declared before any data exists (`data/ledger_meta.json`: `export_rows 0`)**, and the §8.4 matched-day definition | Written into all seven pre-registrations before signing, not after |
| **C5** | Add the account-settings rows to the capture set: `itmlive` · `itmpaper` · `maxexits` · `scanstart`/`scanend`/`exitstart`/`exitend` | Read back from `/settings`; `itmpaper` = `market` confirmed |
| **C6** | Append seven rows to `data/archive/rename_map.csv`? **No** — these are fresh builds with no original. Append seven rows to `bots_meta.csv` instead, with `pillar = IC`, and reconcile group counts | Group counts == `bots_meta.csv` pillar counts |

### Phase D — Day-0, and not before

| Step | Do |
|---|---|
| **D1** | Set `LEDGER_START` in `build_ledger.py` — the Day-0 first action, before anything else |
| **D2** | ⛔ **Set `itmlive` = `market`** before any capital is live (§7, hard gate) |
| **D3** | ⭐ **BEFORE the arms are switched on: observe the 15:52 backstop's actual fire time** on the pilot — the DST / `Market Time (EST)` question (§4.2). **Reordered under review.** If it fires at 16:52 or not at all, seven arms would otherwise run a full day with no flat close and the absence would look like "nothing needed closing" |
| **D4** | Read whether the ITM Position Action appears in a Trades list, and under what label (§6.2 rule 2). **Until this is answered the Ride control's inverted liveness rule is ADVISORY, not fireable** (§9) |
| **D5** | Andy signs each of PR-14…PR-20 per `pre-registration-ledger.md` §7. **Only then may a bot be switched ON** |
| **D6** | Switch `AUTOMATIONS` ON per arm; read **each arm's first new position's Trades list** against §8.5. **Signed ≠ verified** |
| **D7** | Record the `UNATTRIBUTED` bucket count for [15:50, 15:53] Market closes (§6.2 rule 3), and the per-arm count of Market-priced closes — the CF-1 instrumentation |

---

## 11. Adversarial review — what survived

*Two subagents were spawned against the finished draft with instructions to **refute** it,
defaulting to "this is wrong" — one on platform expressibility, one on confound and matching
defects. **Both succeeded.** Between them they returned **10 FATAL** and **24 MATERIAL**
objections. The spec above is the post-review text. What follows is the record: what was fixed,
what could not be fixed and is carried as a named limitation, and what was refuted.*

**Reading key:** **FIXED** — the spec changed. **CARRIED** — real, unfixable at this design's
level, travels with the family as a stated limitation. **PARTIAL** — mitigated, not closed.

### 11.1 Platform-expressibility review — surviving objections

| # | Objection | Status |
|---|---|---|
| **PE-1** | **FATAL — the BOT INPUT tier was never observed.** G1/G2/G3 all tested the *Automation* Input; `state.md`'s bot-input line is *"Inference from a screenshot."* §5.2's caveat is unstruck: *"Whether Exit Options can reference **Bot Inputs** is [DOCS-SILENT] and unverified."* The draft's Phase 0 did not check the one primitive the whole family rests on | **FIXED** — added as blocking check **C0a**, with STOP (not fallback) if it fails |
| **PE-2** | **FATAL — one Automation Input cannot span two automations.** So put and call sides need separate inputs, and a put=Ride / call=PT50 asymmetry would have diffed clean | **FIXED** — §4.1 two-input design, §8.2 intra-arm test, assert **A8**, check **C0b** |
| **PE-3** | **FATAL — the sentinel discharges neither half of §5.2, and A4 cannot fire on a broken link** (the Bot Input object still holds the correct value; the capture reads that object and passes) | **FIXED in part, CARRIED in part** — §1.3 rewritten to state the refusal clause is not expressible, sentinel changed to `SENTINEL-SL1`, behavioural detector **A4b** added. **The window between a link breaking and the next day's ledger is a genuine uncovered hole and is now named as one** |
| **PE-4** | **FATAL — position limits bound OPENINGS only.** §3, verbatim: *"Position limits are for opening positions only; there is no limit on the amount of closing positions."* Two of §4.3's three "mandatory interlocks" were one interlock and a procedural test | **FIXED** — §4.3's correction-of-record box; interlocks rewritten as structural / temporal / procedural |
| ~~**PE-5**~~<br>⛔ **THE FIX FAILED AT PHASE 0, 2026-08-06.** C8 confirmed the Positions loop and the opened-today scope are real, but the **side-tag comparison against the closed position is NOT expressible** — the closed position is not an addressable referent. PE-5 was right that the draft's tree was wrong; the redrawn tree is *also* not buildable. **Resolved by ruling: build without sibling-close (§4.3).** | **FATAL — §4.3's tree had no Positions loop**, and "sibling" is not an OA relation (*"OA models each spread as a separate position"*); "opened today" is unconfirmed | **FIXED** — tree redrawn with the loop and a side-tag comparison; blocking check **C8** with an explicit no-substitution STOP |
| **PE-6** | **MATERIAL — the $250 sizing fallback is not deterministic.** Two contracts fit when credit ≥ $0.75, and independent fills can put one arm at 1 lot and another at 2 on the same day | **FIXED** — §5.4's failure band stated; nightly assert **A6** |
| ~~**PE-7**~~<br>📝 **MOOT 2026-08-06 — sibling-close is not built, so there are three mechanics in the window, which is what Rule 1 wanted.** | **MATERIAL — four mechanics in the 15:50–15:52 window, not three.** `GF-SiblingClose` was priced `speedy`, identical to the Expiration exit, falsifying Rule 1 for all seven arms | **FIXED** — sibling-close re-priced `patient` and gated before 15:50, **tightened to 15:44 on 2026-08-04** (§4.3); §6.2 Rule 0 added |
| ~~**PE-8**~~<br>📝 **MOOT 2026-08-06 — the race is removed with the object. The 15:44 gate (ruling S-4) is recorded, not deleted.** | **MATERIAL — backstop / sibling-close race.** The backstop's unrestricted loop closes leg 1, which triggers sibling-close on leg 2 while the loop also closes it. §4.2's redundant-position check *"did not prevent the 7/01 orphan loop"* | **FIXED** — the gate removes the overlap entirely. ⭐ **Tightened 3:50pm → 3:44pm on 2026-08-04**: the Track B task found the 15:50 value left the race open for any arm exiting before 15:50 (ARM-B2 at 15:45), so PE-8's fix was correct in kind and one minute short in degree |
| ~~**PE-9**~~<br>⛔ **OBJECTION FALSIFIED 2026-08-06 by Phase-0 check C2 — the armed trail is a NATIVE primitive and was never on §11's list.** Recorded as an attack that *succeeded in review and was wrong in fact*; the "fix" it forced has been reverted by ruling. **A folder-derived exclusion is not an observation** — that is the lesson. | **MATERIAL — an armed trailing stop is on §11's not-expressible list by the spec's own §3.1 reasoning**, so §13's "no mechanic appears on the list" was false | **FIXED** — PR-16 scoped to a plain always-on trail; the armed shape explicitly excluded; §13 corrected |
| **PE-10** | **MATERIAL — "Touch $0 exits the moment the position goes ITM" overstates a 1-minute-cadence control.** §11 row 3: *"Sub-second strike-touch with a latch — NOT NATIVE. 1-minute cadence at best"* | **FIXED** — §4.4 and PR-17 restated with the cadence and a defined artifact tolerance |
| **PE-11** | **MATERIAL — the family-level kill criterion is vacuously unfireable** with exactly one input, exactly as Options B and C were rejected for | **FIXED** — rewritten at field/mechanic granularity in §9. ⚠️ **`pre-registration-ledger.md` PR-14…PR-17 carry the same defective wording and need the same correction at signing** |
| **PE-12** | **MATERIAL — presets inside the Bot Input value editor were never observed.** G3 tested the *action* | **FIXED** — check **C0c**, with the consequence (B4 becomes hand-entry) named |
| **PE-13** | **MATERIAL — the allocation "interlock" is inert**; the position limit binds first, always | **FIXED** — §5's justification corrected |
| **PE-14** | **MATERIAL — DST was deferred to a step AFTER switch-on.** If the literal-EST reading holds, the backstop never fires on all seven arms and the absence is invisible | **FIXED** — reordered to **D3**, before any arm is switched on |
| **PE-15** | **MATERIAL — the 8-minute buffer was stated against the wrong boundary** (15:52→15:59 is 7 minutes, and the Exit-Options window is not an Events-class bound) | **FIXED** — §4.2 corrected to the 15:55 automations cap |
| **PE-16** | **MATERIAL — the entry tree is sourced from `session-log.md`, outside the reference set, and its `opened today` gate is unconfirmed** — `oa-ops-runbook.md` §5 trap 7's exact shape | **FIXED** — blocking check **C7** with a STOP |
| **PE-17** | **WEAK — the sentinel bundle carries no time exit, so a broken-link arm is backstop-only and Market-priced** — the state §1.4 calls unacceptable for the Ride arm | **CARRIED** — accepted; a sentinel is meant to be an abnormal state, and A4b flags it within a day |

### 11.2 Confound / matching review — surviving objections

| # | Objection | Status |
|---|---|---|
| **CF-1** | ⛔ **FATAL, AND NOT FIXABLE — the exit-pricing regime is confounded with the arm variable.** The ITM Market action and the 15:52 Market backstop reach only positions still open at 15:50/15:52, so `Ride` and `PT50` are heavily exposed to Market fills while `Touch0` is ~never exposed and the SL arms much less. **The arms hypothesising "capping the tail helps" are the arms systematically spared the fleet's worst execution mechanic** (the fill *"$5.05/contract beyond the worst mark"*, R −1.63). `auto` does not help — it makes the same subset *modeled* instead of *slipped*. **There is no setting under which the tail measurement is arm-neutral.** | **CARRIED — the most serious surviving objection.** §7's "cannot confound" claim withdrawn. **Mitigation, not a fix:** D7 records the per-arm count and R-contribution of Market-priced and ITM-action closes; every arm-vs-control ΔR is reported **alongside** that count; and no tail-based ranking is published without it. This is `hedge-research.md` §5.1 defect 2 in a new form and it should be treated as a standing limit on what this family can conclude |
| **CF-2** | **FATAL — no ranking procedure existed.** Hypotheses were comparative, kill criteria absolute; the two are anti-correlated exactly where it matters, so the criteria would fire on the winners. And the only signed margin in the folder was `research-loop-spec.md` §10's **0.10R**, arithmetically unreachable here: max per-condor return = total credit ⇒ **R_max ≈ +0.083 to +0.162** | **FIXED — and the margin half is now CLOSED, not open.** A comparative criterion in PR-02's form is added to §9. 📝 **CORRECTED 2026-08-04:** ruling **R-3** replaced 0.10R with a three-part test — mean ΔR ≥ **+0.015R** per position, a **paired bootstrap 95% CI excluding zero**, and a **paired sign test on the fired subpopulation**; the median-ΔR test is **WITHDRAWN** as *"not a statistic"*. **+0.015R < R_max on every credit this structure admits, so the collision this objection raised is resolved** (§12 row 10). The draft's *"OPEN in part"* status is withdrawn |
| **CF-3** | **FATAL — n = 100 is underpowered by 2–30×**, and the draft never said whether the analysis was paired. Paired at ρ=0.90, n=100 gives ±0.026R against a largest-ever-measured effect of +0.0150R; ±0.015R needs ~307 paired days, ~560 with Bonferroni | **FIXED** — §9 declares day-pairing, states the CI arithmetic, and reframes n=100 as a first-read rather than a decision target |
| **CF-4** | **FATAL — sibling-close is a shared treatment with an arm-dependent effect**, and it destroys the ★★★★★ anchor PR-18 imports: Sandvand's rung is called *Breakeven* because the untested side decays to zero, which close-both forfeits | **CARRIED, and named** — §4.3's "cannot confound" claim withdrawn; PR-18/PR-19 renamed in substance to "SL100/SL200-close-both" with an explicit instruction not to publish under the anchor's name |
| **CF-5** | **FATAL — the diff tested DIFFERENCE, not ONE-FIELD difference.** An SL100 arm also carrying a stray Touch would have passed | **FIXED** — §8.2's PASS condition rewritten at mechanic granularity; **A1** rewritten to match |
| **CF-6** | **MATERIAL — Architecture E's own blind spot: a mid-sample edit to a shared object passes every assert**, changes all seven arms at once, and may not bump any template version | **FIXED** — assert **A7** (shared-object payload hash vs a recorded baseline), build steps A7 and C3 |
| **CF-7** | **MATERIAL — H1 and H2 contradicted each other**, and §4.2's parallel work queue means the arms do not even evaluate the entry signal at the same instant — arm-specific selection on days near the 0.75% band edge | **FIXED** — H2 rewritten; **"matched day" now defined** and the analysis restricted to matched days |
| **CF-8** | **MATERIAL — the entry window had no upper bound**, so Range075 degraded from a gap filter to an any-time-it-dips filter, and late entries collapse all arms toward Ride | **FIXED** — `before 2:00pm` node added to the shared tree, with its cost stated |
| **CF-9** | **MATERIAL — n = 100 in 6 months needs a 79% qualifying-day rate** (100/126 trading days) before non-fills, the credit floor, or the matched-day requirement; under a strict matched-day reading the per-arm rate needed rises to ~98%. And `build-plan.md` §5's gate is conjunctive — n≥100 **and** 6 months **and** a regime change — with no regime-change criterion anywhere | **CARRIED** — arithmetic stated in §9 and §12; **the review date will arrive with n below target on most plausible pass rates.** The regime-change criterion is added to §12 as an open item, not invented here |
| **CF-10** | **MATERIAL — 21 comparisons and ≥30 simultaneous decision rules with no correction** (FWER 66% at 21 pairs); ~~the family silently consumes **7 of the 8 signed Track B slots**~~ 📝 **first clause SUPERSEDED 2026-08-04 by ruling S-1 — see below**; and `GF-SL200` duplicates a variant already in the signed Track A §3 set | **FIXED in part** — Bonferroni declared in §9's comparative criterion and in build step C4. 📝 **CORRECTED 2026-08-04:** the slot-budget half is **withdrawn** — S-1 ruled **separate allocation**, so the seven family bots are `build-plan.md` §2D fresh builds and **Track B keeps all 8 slots**. ⭐ **The Track A duplication half STANDS and is unaffected:** `GF-SL100` / `GF-SL200` still duplicate signed §3 variants (`SL100`, `SL200`) and still **pool error rates nowhere** — two engines testing one hypothesis with no shared multiplicity accounting. **CARRIED** on that half, recorded in §12 row 11 |
| **CF-11** | **MATERIAL — PR-19's degeneracy criterion was unfireable three ways, and its liveness criterion cancelled its own hypothesis** (SL200 rarely firing *is* the hypothesis) | **FIXED** — liveness disapplied on PR-19 with the reason stated; degeneracy rewritten with a tolerance and a config-backed second condition |
| **CF-12** | **MATERIAL — informative censoring.** A stop arm's 10-day dry spell is a *calm regime*, not a failure; and the Ride control's inverted rule could kill the control via a mislabelled ITM close | **FIXED** — liveness now conditions on *threshold breached*; the control's inverted rule is **advisory until D4** |
| **CF-13** | **MATERIAL — §8's table marked §5.2 rule 4 discharged for all seven arms** when three have unconfirmed primitives. §5.2: *"An arm failing any of these is not a weak arm, it is not an arm."* | **FIXED** — table row 4 corrected; those three are not arms until Phase 0 closes |
| **CF-14** | **MATERIAL — selective citation of `hedge-research.md` §11.** The one line that bears on the stop arms — *"Stop losses are counterproductive on the Fortress structure"* — was the one line not quoted, while PR-15 modelled the correct discipline for PT50 | **FIXED** — both contested priors written into PR-18/PR-19 |
| **CF-15** | **MATERIAL — the $0.08 credit floor contradicts a validated decision** (*"Min-credit filter hurts — winners averaged lower credit than losers"*) and was carried purely by inheritance; and credit dispersion moves **trigger levels**, not just denominators, because `profits`/`stoploss`/`tstop` are credit-referenced while `touch` is not | **FIXED in part** — H1 rewritten to state the trigger-level effect and tick quantisation. **CARRIED:** the floor is retained for comparability with the pilot line, and the contradiction is now recorded rather than silent. Added to §12 |
| **CF-16** | **MATERIAL — "single-field delta" was false** (each trigger carries a pricing sub-field), and 7 arms give 21 *unordered* / 42 *ordered* pairs, not "21 ordered" | **FIXED** — §8.1 restated as one-mechanic/two-field; arithmetic corrected throughout |
| **CF-17** | **MATERIAL — the "hedge tournament" view is two rungs of ONE mechanic, and the control is not a no-hedge control** — `Ride` carries a time exit, a Market backstop, an ITM action and sibling-close, so every hedge effect is measured against an already-hedged baseline and biased toward zero | **CARRIED** — real and structural. Recorded in §12: the hedge lane's own question (*"rank mechanics"*, `pre-registration-ledger.md` §6) is **not** answered by this family, and a null result here means "no help *beyond* the existing three mechanics", not "hedges don't help" |
| **CF-18** | **MATERIAL — the canary's 5% threshold is sub-tick** across the whole admissible credit range, so its real trigger is the tick grid; a no-fill day is ambiguous between engine death and a one-cent spread widening; and it carried no code-fireable rule | **FIXED in part** — PR-20 states the sub-tick reality and adds a 2-consecutive-day RED. **CARRIED:** the false-negative rate of the fleet's only forward exit-engine detector remains unmeasured |
| **CF-19** | **MATERIAL — the hypotheses are not computable from anything the loop produces.** No surface generates a cross-bot paired statistic; `research_loop.py` is advisory-only and *"must not"* be wired in; and the liveness rule needs an **exit-reason field the export may not carry** | **CARRIED, and it is a signing gate** — `pre-registration-ledger.md` §7 item 3: *"does the loop actually produce that number? If not, fix one of the two now."* Added to §12 as the largest piece of unbuilt work this spec implies |

### 11.3 Attacks that failed

Recorded because a review that only reports hits is not a review.

- **"15:52 is unreachable / the Repeating trigger cannot express it."** Defeated — built and
  reload-verified on the pilot, `ntime=1552`, `max="15:55"` corroborated twice.
- **"One Library automation cannot be attached to N bots."** Defeated — the Library reports
  per-automation usage and already contained a shared automation attached to **2 bots**. C5 is
  conservatism, not doubt.
- **"The Bot Schedule's 15:55 cap kills the Repeating backstop."** Defeated by the footnote read
  verbatim: *"Repeating and date/time scheduled automations are **not affected by this
  schedule**."*
- **"Presets cannot cross automations / cannot be named."** Defeated — §9 check #4, first-hand.
- **"The spec cites presets as a matching guarantee."** Defeated — §4.5 demotes them to build-time
  convenience and refuses them as a proof leg. Both reviewers called this the correct discharge
  of Appendix A's G4 objection.
- **"The capture-diff will read the action and see identical arms."** Defeated — the G2 rider is
  applied in §1.2, §8.2 and B4, and `oldValue` is forbidden in all three.
- **"Range075-as-a-preset is a category error the spec commits."** Defeated — the spec identifies
  it as N-2, implements the correct primitive, and declines to edit frozen §2D.
- **"The spec cites the Exit Options panel as evidence somewhere."** Defeated — every verification
  path routes to a capture, a screenshot, or the Trades list.
- **"Seven bots × four automations breaches OA's per-bot automation slots."** Defeated —
  Scanner 2/5, Repeating 0/10, Position-closed 0/5 leaves room.
- **"The arms are not all in one execution class."** Defeated as stated — the *arm variable* is an
  Exit Option on all seven, which is what §5.2 rule 2 asks. The real defect is differential
  *exposure* to the other classes, which is CF-1.

---

## 12. Open items this spec does not close

| # | Item | Why it is not closed here |
|---|---|---|
| **1** | The four memo slots marked `NOT RULED` — fix the broken `build-plan.md` §5.2/§8.1 citations · Day-0 no-touch ordering before the re-arm sweep · **build the arm-distinctness assert before the tournament trades** · the ungrouped-export UI check | Andy's. Item 3 bites §8.3 directly; this spec assumes YES as the safe default and says so |
| **2** | **N-2 — `Range075 as a preset`** in frozen §2D and `hedge-research.md` §5.2 rule 3 | The substance is implemented correctly (§4.1); the **wording** in a frozen doc needs an "amend the plan". Draft text is in the memo |
| **3** | **§3's arithmetic reading of §2D** — 4–6 IC bots *plus* hedge arms *plus* canary vs 5–7 fresh total | Resolved here by treating them as one family. If Andy reads §2D as two families, §3 changes and an amendment is needed |
| **4** | §2's **QQQ-vs-SPX** scope choice | Specified with reasons; overrulable, but not at build time (§2's last paragraph) |
| **5** | §1.4's **ride arm = time-exit-only, not empty bundle** | A spec choice departing from `state.md`'s framing of G1. Overrulable; §11's confound-A objection applies if overruled |
| **6** | `oa-ops-runbook.md` §3's Pillar-vs-cohort tension | Resolved operationally (§5.2) by using a tag; the §3 wording is flagged, not amended |
| **7** | The **successor template check** — does a template store a REFERENCE to the bot's live automation objects? | Open in `oa-ops-runbook.md` §7. Under Architecture E it matters more than usual (Phase B note) |
| **8** | §9 check **#5** — is re-applying `Update Position Exit Options` side-effect-free? | Needs positions; Day-0 |
| **9** | **SL130** and the fixed-$ rungs | SL130 deferred to wave 2 on slot budget. 📝 **CORRECTED 2026-08-04 — the fixed-$ half is no longer pending.** R-1 **signed** the rungs as median-credit dollar rungs (`DSTOP_100` / `DSTOP_150`) inside the frozen 12-variant Track A set and **rejected the RISK basis**. They stay out of this family because they are **Track A's**, not because their basis is unsettled. ⚠️ Note R-1 also puts **SL150** in the signed Track A set — so wave 2's SL130 sits between two rungs Track A already runs, and its marginal value should be re-argued before a slot is spent |
| ~~**10**~~ | ✅ **RESOLVED 2026-08-04 by ruling R-3 — no longer an open item.** The draft raised that §10's **0.10R** margin exceeded this structure's theoretical maximum per-condor return (**R_max ≈ +0.083R to +0.162R**), so nothing here could ever graduate. **R-3 replaced it:** mean ΔR ≥ **+0.015R** per position, **paired bootstrap 95% CI excluding zero**, and a **paired sign test on the fired subpopulation**; the median test withdrawn. R-3's own calibration reasoning is *"the arithmetic ceiling on a PT50→PT70 move at the fleet's median credit/risk of 0.070 is 0.014R per fired position, so the previously declared 0.10R was unreachable by construction"* — the same defect, found independently from the fleet-median side. **+0.015R sits below R_max at every credit this structure admits** (its credit/risk of ≈0.083–0.162 is *above* the 0.070 fleet median the margin was calibrated on), so the margin is comfortably reachable here | ⚠️ **The power problem is now SHARPER, not softer, and it moves to §12 row 16.** A reachable threshold is not a resolvable one |
| **16** | ⭐ **NEW, opened by R-3's resolution of row 10.** The signed margin is **+0.015R** — which is also **the largest effect this program has ever measured** (SL75, +0.0150R, n=1,254) and sits *below* §11-CF3's CI half-width for this family at the declared sample (**±0.026R** paired at ρ=0.90, n=100). **The threshold is now finer than the family can resolve at n=100**, and CF-3's arithmetic says ~307 paired matched days are needed to resolve ±0.015R, ~560 under Bonferroni. Row 10 is closed; **the question it was standing in for — what n this family actually needs — is not.** ⚠️ Note also that R-3's test is written **per position over a bot's full population**, while this family's comparative criterion (§9) is **per condor, day-paired, matched days only**. The two are not the same statistic and the family must not be scored against R-3's gate without restating it | Andy's, and it is the sample-size question, not the margin question |
| **11** | ~~⭐ **Slot budget.** These seven bots meet `research-loop-spec.md` §4's definition of Track B arms, so the family consumes **7 of the 8 signed Track B slots**~~ 📝 **SUPERSEDED 2026-08-04 — ruling S-1, recorded in `docs/track-b-arms-spec.md` §3.3.** Andy, verbatim in substance: *"the seven family bots are `build-plan.md` §2D fresh builds; Track B's 8 slots are yours, `n_used=20` confirmed."* **Separate allocation (Reading B).** The family does **not** spend Track B's budget; **Track B keeps all 8.** `n_used = 20` (4 clones + 9 untouched + 7 greenfield) is confirmed by ruling, not inferred. ⭐ **THE SECOND CLAUSE STANDS, UNCHANGED AND STILL OPEN:** `GF-SL100` / `GF-SL200` **duplicate signed Track A §3 variants** (`SL100`, `SL200`) and **pool error rates nowhere** — the same hypothesis tested in two engines with no shared multiplicity accounting. ARM-B1 (`DSTOP_100`) has the identical defect per `track-b-arms-spec.md` §6.3. ⚠️ **S-1 unblocked the allocation; it did not touch the double-testing.** | Double-testing half: still **Andy's**, and still binds two signed documents |
| ~~**17**~~ | ⭐ **NEW, surfaced by S-1's fleet arithmetic — then RESOLVED within the hour.** The finding: `build-plan.md` §2D and `pre-registration-ledger.md` §3 both declare **≈18–20 active bots**, but with separate allocation the fleet is **22 at wave 1 and up to 28 if Track B is fully spent** (`track-b-arms-spec.md` §3.4) — and `build-plan.md` is 🔒 frozen, so it needed an explicit *"amend the plan"*. ✅ **THAT AMENDMENT HAS LANDED** — `build-plan.md` §2D now carries a **`🔓 SCOPING AMENDMENT 2026-08-05 — "amend the plan", Andy's explicit words`** block naming Track B as a separate allocation, with operative figures *"≈18–20 plan bots · wave-1 Track B spend **2** · **ceiling 28**"*. It cites this spec's §12 item 11 as the finding that forced it. **The plan-bot arithmetic is unchanged; what changed is that Track B is now named rather than silently colliding.** ⚠️ **The amendment scopes a count and authorizes no build** — every Track B arm still needs its own signed pre-registration. ~~⛔ **STILL BLOCKING: C12** — whether ARCHIVED bots count against the Pro 50-bot cap. The amendment's headroom claim rests on the reading that they do not, and *"that reading is not verified"*: if they do count, Day-0 is 36 + 7 = 43 and the ≤8 allocation does not fit (43 + 8 = 51)~~ ✅ **C12 DISCHARGED — propagated into this row 2026-08-05** (correction only; this row's status and every figure in the amendment are unchanged, and no build is authorized). **[FIRST-HAND 2026-08-04, `/bots` footer read]**: `35 active bots • 15 left in your plan`, read read-only immediately after the Fortress original was archived, against `36 active bots` during three failed attempts — **35 + 15 = 50**, so the plan complement counts **ACTIVE** bots and **archived bots do not consume slots.** Wave 1 is **22 of 50**; the struck `43` / `43 + 8 = 51` arithmetic is **void**. ⚠️ **RESIDUAL, carried not dropped — [FIRST-HAND, UNCORROBORATED]:** this is the footer's *accounting*, not OA's *enforcement* (`left = 50 − active` renders identically under either hypothesis), observed with **one** archived bot where the Group-A sweep archives **twenty**. ⛔ **Pre-declared reopen: if a build ever fails at the cap despite archived bots existing, C12 reopens** and the ≤8 allocation is re-derived against an observed slot count. Full evidence block: `track-b-arms-spec.md` §3.2 | ✅ Amendment landed. ✅ **C12 discharged with its residual** (`track-b-arms-spec.md` §3.2 / §10) |
| **12** | ~~⭐ **No regime-change criterion exists anywhere.**~~ 📝 **CORRECTED 2026-08-06 — FALSE. `evidence-standards.md` §4 gate B3 already defines it**: *"a VIX move of ≥ 10 points peak-to-trough, or both a sub-15 and an above-25 VIX period"*, cross-referenced by that file's own T3.3. `build-plan.md` §5's gate is still conjunctive — n≥100 **and** ≥6 months **and** a regime change — but the third conjunct has a definition; it lacks a `scripts/` detector and a pre-registration citation by name. | ~~Must be defined before any arm can graduate; not invented here~~ **Must be WIRED (detector) and CITED (at signing) before any arm can graduate — the definition itself already exists.** `decision-card-2026-08-06.md` slot 6 deferred a definition on a false premise; Andy's fresh read is needed on the wiring question. |
| **13** | ⭐ **The comparative machinery does not exist.** No surface produces a cross-bot paired ΔR with a bootstrap CI; `research_loop.py` is advisory-only and must not be wired in; and the liveness rule needs an **exit-reason field the export may not carry** (`oa-export-schema.md` was not in this session's reference set). **This is the largest piece of unbuilt work the spec implies**, and `pre-registration-ledger.md` §7 item 3 makes it a signing gate | Needs scoping as its own task before Day-0 |
| **14** | ⭐ **The `$0.08` credit floor contradicts `hedge-research.md` §11's validated "min-credit filter hurts"** and was carried by inheritance from the pilot | Retained for comparability; the contradiction is now recorded rather than silent. Andy's to keep or drop |
| **15** | ⭐ **CF-1 stands as a structural limit. ~~CF-4~~ is ✅ DISCHARGED 2026-08-06** — the close-both wrapper on the SL arms was an artefact of `GF-SiblingClose`, which the C8 ruling removes; PR-18/PR-19 can now reach the Breakeven shape their anchor describes. **CF-1 is unaffected** — the exit-pricing / ITM exposure asymmetry has nothing to do with sibling-close. Original text left standing: ~~The exit-pricing/ITM exposure asymmetry and the close-both wrapper on the SL arms cannot be designed away at this level~~ | CF-1 carried with named mitigations; CF-4 discharged (§4.3 ruling) |

---

## 13. What this spec is measured against

- `build-plan.md` §2D and §5 — **implemented, not amended.** No text in that file was edited.
- `hedge-research.md` §5.2's five conditions — §8's table maps each to what discharges it.
- `oa-platform-reference.md` §11 — **no mechanic in this spec appears on the not-expressible
  list.** ~~⚠️ **This claim was FALSE in the draft** and is true only after review: PR-16's target
  was an *armed* trailing stop, which §11 rows 4 and 6 rule out and which §3.1 already used those
  rows to exclude elsewhere. PR-16 is now scoped to a plain always-on trail and the armed shape
  is explicitly excluded (§3.1, PR-16).~~
  ⭐ **RE-CORRECTED 2026-08-06 — the review's correction was ITSELF WRONG, and Phase-0 check C2
  falsified it.** The armed trailing stop **is** expressible: OA implements it as a native
  Exit-Options primitive (`tstop` → `target` "Activate at __ % of credit" + `trail` "Close on __ %
  pullback"). §11 rows 4 and 6 bound what **decision nodes** express, not what a native exit
  primitive does internally. **PR-16 is re-scoped to the ARMED trail (ruled 2026-08-06)**, and
  §13's headline claim stands for the ORIGINAL reason — no mechanic in this spec is on §11's list. **Three further candidate mechanics were excluded for §11
  reasons** and are named in §3.1.
  ✅ **2026-08-06 — EVERY ARM'S PRIMITIVE IS NOW CONFIRMED** (C1 `stoploss` = % of credit, C2
  `tstop` = armed sub-form, C3 the pricing sub-fields). **All seven are arms.** Left standing:
  ~~⚠️ **Every mechanic names the primitive it is built from — but three arms' primitives are
  UNCONFIRMED** (Trail's `tstop` shape, SL100/SL200's `stoploss` unit, and four arms' exit-pricing
  sub-field). Per `hedge-research.md` §5.2's closing sentence they are **not arms until Phase 0
  closes**, and §8's table says so.~~
- `oa-ops-runbook.md` §4 — every build step ends in a two-layer verification, with Layer 2
  deferred to Day-0 and tracked.
- `CLAUDE.md` §9.1a — no write in this spec's build order is reported done on the strength of the
  tool call that made it.
- **No mechanic anywhere in this document depends on the Exit Options panel as evidence.**
