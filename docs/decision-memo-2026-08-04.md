# Decision memo — 2026-08-04

*Seven open decisions, one ruling line each.*

> ### ✅ RULED BY ANDY 2026-08-04 — all seven decided. Rulings are recorded in the slots below.
> **Superseding the original note that "nothing in this memo has been executed":** D-3 and
> Decision 7 were **ruled AND executed** in the pilot session; Decision 6 is ruled with execution
> **deferred to Template V2**; D-1, D-4, Decision 4 and Decision 5 are ruled and not yet
> propagated. **Gates G1–G4 are CLOSED** — see the D-1 slot. Four secondary slots remain
> unruled and are marked as such. No frozen doc has been amended and no git command was run in
> the session that wrote this memo.

**How to use this.** Each section gives the forcing fact (cited file + section), the options,
a recommendation, and a `RULING` line. Write one line per section. Amendment text is **draft
only** — text marked `EXECUTES ONLY ON ANDY'S "amend the plan"` is inert until you say those
words (`CLAUDE.md` §3 item 6).

**Evidence discipline for this memo.** Every quoted phrase below was asserted byte-exact
against the device file with a match count of exactly one before being pasted. Every aggregate
carries its n. Nothing here is inferred from a screen that was not opened — the account was not
touched this session, so anything requiring a live read is named as a **GATE**, not answered.

**Two recommendations in this memo reversed under adversarial review** (D-1 and Decision 4).
Both reversals, and the objections that survived, are recorded in **Appendix A**. The memo
presents the post-review positions, not the drafts.

---

## Reading note — three citations in `state.md` point at sections that do not exist

`state.md` D-1 says the decision bites `` `build-plan.md` §5.2 / §8.1 ``. **`build-plan.md` has
no §5.2 and no §8.1** — its headings run `## 1` through `## 6`, and a search for the strings
`5.2` and `8.1` in that file returns **0 matches**. The §5.2/§8.1 anchors belong to
`oa-platform-reference.md`. The same broken citation is replicated in `session-log.md` and in
`sprint-2026-08-04.md`.

**Consequence, and it changes D-1's shape:** the phrase `PT% as a Bot Input` appears **nowhere
in the frozen plan**. It lives in `pre-registration-ledger.md` (an unsigned DRAFT entry),
`reactivation-runbook.md`, and `oa-platform-reference.md` §8.1. What the frozen plan actually
says about the greenfield family is §2D:

> `the matched tournament: hard-PT vs trailing vs ride, arms differing`
> `  in exactly one input value.`

**So D-1 is not, by itself, an amendment to the frozen plan.** Which option you pick determines
whether an amendment becomes necessary — see D-1.

**RULING (Andy) — fix the broken §5.2/§8.1 citations in `state.md` and `session-log.md`?**
⏳ **NOT RULED as of 2026-08-04.** Slot left open deliberately — it was not among the seven
rulings. `.................................................................................`

---

## D-1 — What replaces "PT% as a Bot Input"

### The forcing fact

`oa-platform-reference.md` §9 row 3, answered 2026-08-04 first-hand:

> `there is no 🔗 on Profit Taking % or any individual field`

The 🔗 sits on the **Exit Options row**, so the input's type is the whole bundle. Same row:

> `What IS expressible is "Exit-Options-SET as a Bot Input" — one variable holding a whole exit configuration, swapped as a unit.`

Corroborating constraint, `oa-platform-reference.md` §5.2:

> `documented chain terminates at a *decision* input; Exit Options are never named as a consumer.`

**Scope this ruling to the greenfield IC family.** Decision-side variables (entry deltas, DTE,
credit, indicator thresholds) *are* per-field linkable via the documented decision-input chain,
so a blanket "no bot inputs" verdict would silently foreclose the hedge rebuild too.

### Options

| | Option | What it means |
|---|---|---|
| **A** | **Exit-Options-SET as a Bot Input** | One bot input per arm whose value is the entire exit configuration. Arms differ in exactly one input, whose value is a bundle. |
| **B** | **Per-arm hand-set values** | Each arm's Open Position action carries its own Exit Options, typed in. No inputs. Matching proved by capture-diff only. |
| **C** | **Drop the input idea; preset identity is the arm** | Each arm carries a differently-named account-scoped Exit Option Preset. |
| **D** | **Defer** — settle GATES G1–G4 in one UI session, then rule | Costs one Chrome session. Nothing else in Phase 4 depends on it before the greenfield build. |

### Recommendation — **A, conditional on gates G1–G4. If any gate fails, fall back per below.**

**Rationale.** §2D's frozen arm set is `hard-PT vs trailing vs ride`. Those three are not three
values of one field: hard-PT populates the profit field, trailing populates the trailing-stop
field, ride populates neither. **At field granularity these arms differ in two or three fields
by construction** — so "PT% as a Bot Input" would not have satisfied §2D's "exactly one input
value" even if the per-field 🔗 had existed. The bundle is the *only* object type under which
the frozen sentence is literally true, which means Option A is the choice that requires **no
amendment to the frozen plan**, and B/C are the choices that force one. The draft of this memo
recommended B and was reversed on exactly this point. Two further reversals matter: the failure
that killed the v1 tournament — `HedgeA-S1` ≈ `HedgeD` ≈ `HedgeTest`, 73/73/70 identical
positions across 3 bots (`hedge-research.md` §6), invisible for four months — was produced by
**independently hand-set bots with no inputs at all**, so hand-setting is the pathogen and not
the cure; and `oa-platform-reference.md` §5.2 supplies a designed fail-loud guard that exists
only under the input architecture:

> `distinctive sentinel`

(`Mitigation, required on every input-parameterised arm:` make each Default Value a distinctive
sentinel `-999` that a decision explicitly tests for and refuses to trade on.) Under B or C
there is no link to break, therefore no sentinel and no designed detector — drift is silent by
default rather than silent-on-failure. Finally, the family's own pre-registered kill criterion
is written over **inputs** (`pre-registration-ledger.md` PR-14…PR-17):

> `FAMILY-LEVEL: if a capture-diff ever shows more than one differing input`

Under B or C the arms have zero inputs and that criterion is **vacuously unfireable**.

### GATES — none of these is answerable from the folder, all are one UI session

| | Gate | Why it blocks |
|---|---|---|
| **G1** | **Can a bundle Bot Input hold an EMPTY / no-exit-options value?** | Required for the `ride` arm. Unaddressed in §6.1a and §9. **If G1 fails, Option A cannot express the ride arm** — fall back to: 3 input-parameterised arms + `ride` specified separately as an Exit-Option-free control (the shape `build-plan.md` §4 already uses for the two legacy controls), and §2D's "exactly one input value" then needs an amendment naming the ride arm as an exception. |
| **G2** | **Does the per-bot capture record field-level values, or an input reference, when Exit Options are driven by a bot input?** | Decides whether the capture-diff is field-legible. The blob is decodable — `state.md` records the clone's as `^^0.5\|0.01^$0` decoded to 50% PT / 10-min expiration — so a bundle diff is a **parser feature, not an opacity problem**, provided the capture carries the payload rather than a reference. |
| **G3** | **Are a bundle Bot Input on the Exit Options row and a NAMED Preset on the same Open Position action compatible, or mutually exclusive?** | `oa-platform-reference.md` §8.1 requires the preset; §9 row 3 established the input; **no file tests them together.** |
| **G4** | **Does editing a preset propagate to already-attached actions?** | `oa-platform-reference.md` §6.1: `**A preset makes the VALUES consistent, not the ATTACHMENT.**` If it propagates, an account-scoped preset is a shared definition with account-wide blast radius. |

Related and already tracked: `oa-platform-reference.md` §9 **#5** (is re-applying Update
Position Exit Options side-effect-free) is the check that would make *either* design
self-healing. It needs positions, so it stays a Day-0 check.

### Draft amendment text

**(a) `docs/pre-registration-ledger.md` PR-14…PR-17 — DRAFT entry, unsigned, no plan amendment
needed.** Replace in the `MECHANISM` block:

- current: `Option Preset in the Open Position action (PT% as a Bot Input · Touch on the`
- replacement: `Option Preset in the Open Position action (the Exit-Options SET as a Bot Input · Touch on the`

And append to the entry's warning block:

```
> ⚠️ **D-1 RULED 2026-08-__ — the arm variable is the WHOLE Exit-Options bundle, not PT%.**
> Per-field 🔗 does not exist (`oa-platform-reference.md` §9 row 3). The FAMILY-LEVEL kill
> criterion above reads "one differing input" at BUNDLE granularity; the capture-diff must
> therefore decode the exits payload, not compare rendered labels. Gates G1–G4 of
> `docs/decision-memo-2026-08-04.md` must be closed before this entry is signed.
```

**(b) `docs/reactivation-runbook.md` Step C** — same substring replacement, one occurrence:
`(PT% as a Bot Input · Touch $0 on the challenged side · time exit)` →
`(the Exit-Options SET as a Bot Input · Touch $0 on the challenged side · time exit)`.

**(c) `docs/oa-platform-reference.md` §8.1 — ⛔ NOT EDITED. §8 is gated.** Recorded against it
for Andy's authorization; the draft append is:

```
> ### 📝 APPENDED 2026-08-__ — D-1 ruled. The item-1 dependency resolves, with a new shape.
> §9 row 3 answered the second dependency: Exit Options DO accept a Bot Input, but the input's
> type is the whole bundle. Item 1's "PT%" is therefore not the variable — the exit SET is.
> Preset naming (§9 row 4) is confirmed and cross-automation scope is closed.
```

**(d) `docs/build-plan.md` §2D — NO AMENDMENT REQUIRED under Option A.** Under B, C, or the G1
fallback, §2D's `arms differing / in exactly one input value` becomes false as written and the
following would be needed —
**EXECUTES ONLY ON ANDY'S "amend the plan":**

```
*Amended 2026-08-__, at Andy's explicit instruction. The greenfield family's arms differ in
exit POLICY, and OA links Exit Options as an input only at whole-bundle granularity
(`oa-platform-reference.md` §9 row 3) — so "exactly one input value" is expressible only if the
value is the whole exit configuration. Where an arm carries no exit configuration at all (the
`ride` arm), it is specified as an Exit-Option-free control per §4 rather than as an input
value, and the one-differing-input proof is asserted across the remaining arms only.
Nothing else in this plan changed.*
```

**RULING (Andy) — D-1:** ✅ **RULED 2026-08-04 — Option A. Exit-Options-SET as a Bot Input**, per
the recommendation. Gates closed first: **G1 YES** (server-confirmed — an empty bundle saved on the
TEST bot and survived a hard reload, so the `ride` arm IS expressible and the G1 fallback is not
needed) · **G3 compatible** · **G4 no propagation**.

> ⚠️ **REQUIRED RIDER, forced by G2 — part of this ruling, not commentary.**
> **G2 came back REFERENCE, not values.** The action stores
> `{"type":"input","input":"IN…"}`, so a capture that reads only the action records the input's
> **name**. **Every capture surface — `bots_config_v2.csv`, the capture-diff, and the drift
> detector — must read the INPUT OBJECT, not just the action, or every arm diffs as identical.**
> **`oldValue` must never be read as current config: it is a stale pre-link snapshot.**
**RULING (Andy) — authorize the one UI session to close G1–G4 before the greenfield build?**
✅ **SUPERSEDED — the gates were RUN AND CLOSED in the pilot session, 2026-08-04.** G1 YES
(server-confirmed) · **G2 REFERENCE not values — see the rider on the D-1 ruling above** · G3
compatible · G4 no propagation. Full detail in `state.md`'s pilot entry.

---

## D-3 — In-the-money Position Action

### The forcing fact

`oa-platform-reference.md` §13.1, `input.value` read from the settings page 2026-08-04:

> `**Read 2026-08-04: `itmpaper` = `auto`, `itmlive` = `auto`.**`

and the option table's first row:

> `| **`auto`** | Calculate estimated P/L from underlying close price | **NO** |`

`market` is the only one of the three that sends a closing order, and per the same section it
fires `10 minutes before the close = 15:50` — the same instant as the clone's existing
Expiration exit (`state.md`: the clone's exits decode as 50% PT + 10-min expiration). OA's own
description of the setting:

> `Positions expiring in-the-money are subject to assignment and/or broker intervention`

Two independent controls exist — `oa-platform-reference.md` §13.1:
`**Two independent controls, one for paper and one for live**, each with the same three options:`
— so paper and live can be ruled separately, and should be.

### What is actually at stake, separated

- **On paper (now):** *data quality*, specifically on the loss tail. Under `auto` an ITM
  expiring position's P/L is **estimated from the underlying close price** — a modeled number,
  not a fill — and it lands in the export, and therefore in the ledger. ITM-at-expiry is by
  definition the losing tail of a credit condor. The mirror baseline (n=174 positions, 10
  mirrors, zero excluded) found **four mirrors with positive median R and negative mean R** —
  they win most trades and lose money. The tail is where the answer lives, and `auto`
  guarantees the tail is synthetic.
- **On live (Day-0):** *assignment*. QQQ is a physically-settled ETF, and per §13.1 the bot is
  assignment-blind. `auto` means real stock delivered.

### Options

| | Paper setting | Consequence |
|---|---|---|
| **1** | leave `itmpaper` = `auto` | Loss-tail P/L stays modeled. No 15:50 contention. |
| **2** | set `itmpaper` = `market` | Real closing orders, real fills, real slippage in the ledger. Introduces a 15:50 co-fire with the Expiration exit. |
| **3** | set `itmpaper` = `release` | Strictly worse — no order *and* manual data entry. |

### Recommendation — **paper: set `itmpaper` = `market` now. Live: `itmlive` = `market` as a hard Day-0 gate, set before any capital is live.**

**Rationale.** Paper's only job is to produce honest data; `auto` fails that job precisely on
the positions that decide funding. The obvious objection — that `market` races the 15:50
Expiration exit — cuts the other way on a paper account: watching which of two 15:50 mechanics
actually wins is exactly the §8.3-class discrimination the fleet needs *before* live capital,
and it partly answers Decision 6 with data instead of design. Note the race is loose, not
tight: `state.md`'s Tier-1 block records OA's own statement that there is
`no guarantee an automation will run exactly on` the 15-minute marks. On the live side there is nothing to weigh — `auto` on a
physically-settled underlying with an assignment-blind bot is an uncapped tail risk taken for
no benefit, and §13.1 already calls it `**This is a Day-0 decision, not a preference.**`

⚠️ **`market` is not a substitute for the 15:52 backstop.** It covers only *expiring ITM*
positions on expiration day. The backstop covers everything else.

⚠️ **This is a value change on a live-config surface, so `CLAUDE.md` §5 applies:** refactor
first, values second, pilot before champion. The setting is **account-wide** — it cannot be
piloted on one bot. That is an argument for setting it now, while the account is inactive and
holds no post-cutover positions, rather than at Day-0 with capital moving.

### Draft amendment text

**(a) `docs/reactivation-runbook.md` — insert into the Day-0 sequence, before the first
capital-live step:**

```
0a. **Read and set the In-the-money Position Action.** `app.optionalpha.com/settings` →
    confirm `itmlive` = `market` ("Close position with a market order") and `itmpaper` =
    `market`. ⛔ `auto` sends NO closing order and a QQQ condor rides into physical settlement
    (`oa-platform-reference.md` §13.1). Screenshot both fields after saving — Layer 1 of
    `oa-ops-runbook.md` §4.0. This gates capital, not convenience.
```

**(b) `docs/oa-ops-runbook.md` §1.7 or the capture set — add three account-level fields** that
currently appear in no capture: `itmlive`, `itmpaper`, `maxexits`. Draft line:

```
- **Account settings (`/settings`), captured every sweep:** `itmlive` · `itmpaper` ·
  `maxexits` · `scanstart`/`scanend`/`exitstart`/`exitend`. These are account-wide, override
  nothing per-bot and are overridden by nothing per-bot, and `maxexits` in particular is a
  single switch that can cap every bot's ability to close (`oa-platform-reference.md` §13.2,
  read `0` = Unlimited on 2026-08-04).
```

**RULING (Andy) — paper setting:** ✅ **RULED AND EXECUTED 2026-08-04 — `itmpaper` = `market`.**
Verified by hard reload + `input.value` re-read, with before/after screenshots on file.
**RULING (Andy) — live/Day-0 stance:** ✅ **RULED — `itmlive` = `market` is a hard Day-0 gate.**
**Left UNTOUCHED at `auto`; the gate stands and must be set before any capital is live.**

---

## D-4 — Retire the Excessive Errors Failsafe as the June-lapse hypothesis

### The forcing fact

`oa-platform-reference.md` §4.5, first-hand from the bot Log `Errors` filter, 2026-08-04:

> `**The newest error on either bot is `Apr 16, 2026 3:55PM`.**`

| Bot | Error day | n (errors) |
|---|---|---|
| `QQQ-IC-0DTE-Fortress` | Apr 16, 2026 | **91** |
| `QQQ-IC-0DTE-Fortress` | Mar 16, 2026 | **138+** (more unloaded) |
| `QQQ-IC-0DTE-Fortress-NoPT50` | Apr 16, 2026 | **91** |

Zero June errors on either bot. The list is newest-first, so a June error would have to sit
above these rows. §4.5's instruction is already written:

> `Do not carry this into pre-registration as a live hypothesis; carry it as a closed one.`

**Retire it as the JUNE CAUSE. Do not retire the mechanism** — both March and April days are
far above the 10-error threshold (n=91, n=138+), so the failsafe plausibly did fire on those
days, on the entry scanners, months before the lapse.

### Every doc that carries it, and what each needs

| # | Location | What it says now | Action |
|---|---|---|---|
| 1 | `oa-platform-reference.md` §4.5 | Already carries the dated ⛔ answered banner (2026-08-04). Original text stands per §0.2. | **No change.** ✅ Already done. |
| 2 | `oa-platform-reference.md` §9 row 8 | Already struck with the answer. | **No change.** ✅ |
| 3 | `oa-platform-reference.md` §4.5, "Carry the uncertainty" block | Still instructs `State it as a hypothesis in pre-registration and check the June error counter before claiming it.` | **Stale instruction.** One-line dated append — §0.2 permits evidence-backed appends without authorization. |
| 4 | `oa-platform-reference.md` §10 | Lists the failsafe as an independent candidate and says `Neither has been tested.` | **Now half-false.** Dated append. |
| 5 | `oa-ops-runbook.md` §7 | `Confirms or kills the Excessive Errors Failsafe hypothesis for the 6/12 regression` — an OPEN check | **Strike as answered.** |
| 6 | `reactivation-runbook.md` §1 | `this came from **one rep**, who did not know the documented Excessive Errors` | **Keep — still true and still useful** (it is about rep reliability, not the June cause). Add one clause. |
| 7 | `pre-registration-ledger.md` PR-05 | `failsafe-tripped → RED, and the bot is switched off pending investigation.` | **KEEP UNCHANGED.** This is a *liveness kill criterion*, not a June-lapse hypothesis. The mechanism is real and this fleet tripped it. |

⚠️ **Correction to the sprint plan's premise.** Task 5 of `sprint-2026-08-04.md` instructs a
future session to "Update `docs/pre-registration-ledger.md` entries that carry it as candidate
cause." **A search of that file finds exactly one mention of the failsafe — row 7 above — and
it is not a June-lapse hypothesis.** There is no propagation work to do in the ledger. Do not
let a downstream session invent an edit to satisfy the instruction.

### Replacement wording — the standard sentence, for any doc that needs one

```
The 2026-06-12 exit-order lapse has **no established cause.** The Excessive Errors Failsafe was
excluded 2026-08-04 by direct log read — zero June errors on either Fortress bot, newest error
`Apr 16, 2026 3:55PM` (`oa-platform-reference.md` §4.5). The mechanism is real and this fleet
tripped it on entry scanners in March (n=138+) and April (n=91), but not in June. Carry the
lapse as an OPEN question with a named Day-0 discriminator, never as a solved one.
```

### Remaining candidate causes, ranked — with the Day-0 evidence that discriminates each

The observed signature constrains this hard: **entries kept flowing while exits stopped**, and
it was **not uniform across bots** — the champion's PT25 died June 1 while its 6/14 clone
worked 70/0 (`reactivation-runbook.md` §1). So the cause must be exits-only and per-bot, not
account-wide and not whole-bot.

**1. The per-bot `EXIT OPTIONS` toggle was OFF** — *best signature fit.*
Existence is `[FIRST-HAND ×2]` (§10); the *causal* claim is not established. Exits-only ✔,
per-bot ✔.
**Discriminator (Day-0, already specified):** re-arm, then read the first new position's Trades
list. PT row present → supports. §10 states the refutation condition in its own words: if the
toggles read ON and the Trades lists still show no PT rows, the mechanism is refuted.

**2. A platform-side regression in the Exit Options engine** — *equal signature fit, harder to test.*
The observed shape — editor displays every setting correctly, engine emits nothing — is §0.3's
exact failure class, and §0.3 is a standing rule precisely because of it.
**Discriminator:** none available to this project retrospectively. Forward: the 1-lot canary
from `build-plan.md` §2D, `whose PT should fill every single day. If it stops filling, the exit engine died.`
**This is the only candidate the canary was designed to catch, and it is the argument for
building the canary in the first wave rather than treating it as optional.**

**3. Exit Options were never attached to those positions** — *config, not failure.*
`oa-ops-runbook.md` §4.2: `Exit Options are **copied onto the position at open**` — so a
position opened before a config existed carries no exits, permanently and invisibly.
**Discriminator:** in principle the archived v1 captures could show whether the 6/12+ positions
predate a config change. ⚠️ **But `CLAUDE.md` §3 bars the v1 record as a reporting input, and
the v1 config record is proven wrong on 3 of 4 audited bots** — so this is checkable as
*history* only and can never be promoted above T4. Treat as unresolvable, not as unlikely.

**4. The `maxexits` account throttle was non-zero** — *right mechanism, wrong distribution.*
`oa-platform-reference.md` §13.2: `` `maxexits` — read **`0`** = `Unlimited`. `` It caps exit
attempts only — a perfect signature match on the exits-only half. **But it is account-wide**,
and the 6/14 clone working 70/0 through the same window argues against any account-wide cause.
Its June value is unrecoverable; account settings carry no history.
**Discriminator:** none retrospectively. Forward: capture `maxexits` every sweep (see D-3
amendment b) so this can never again be an unanswerable question.

**5. The Bid-Ask Guard silently suppressed exits** — *excluded for the current config, unfalsifiable for June.*
§6.3: `While the position's spread exceeds the configured width, Exit Options are **disabled**`.
Re-confirmed first-hand 2026-08-03 as **OFF on the Fortress line** (unchecked, dollar field
empty). Its June state is unknown and unrecoverable.
**Discriminator:** none. Forward: it is in the §6.1a field roster, so capture it.

**6. Billing/subscription state change** — *listed for completeness; timing argues against it.*
§10 flags `the docs' total silence on what happens to a running bot's exit conditions when billing state changes`.
⚠️ **But the account traded through 7/02 and went inactive later, so the June lapse predates the
lapse in subscription.** Rank last.
**Discriminator, and it has a sequencing cost:** Day-0 is itself an inactive→active transition.
If exits resume at reactivation **with no toggle intervention**, billing is implicated. To keep
that observable, the first Day-0 observation must happen **before** the re-arm sweep flips
anything — otherwise re-arm and reactivation are confounded and candidate 1 and candidate 6
become permanently indistinguishable. **This is a concrete change to Day-0 ordering and it is
free.**

**RULING (Andy) — retire as June cause, keep as mechanism:** ✅ **RULED 2026-08-04 — retire the
Excessive Errors Failsafe as the 2026-06-12 lapse cause; KEEP it as a real, documented mechanism
this fleet has tripped** (March/April, on entry scanners). **June cause: UNKNOWN**, per the ranked
candidate shortlist above.
**RULING (Andy) — Day-0 ordering: one no-touch observation before the re-arm sweep?**
⏳ **NOT RULED as of 2026-08-04.** Slot left open deliberately — it was not among the seven
rulings. `.................................................................................`

---

## Decision 4 — The tournament shared-automation conflict

### The forcing facts

`build-plan.md` §2D (frozen):

> `**Rebuilt hedge tournament arms** — shared automation, shared inputs, same execution class, Range075 as a`
> `  preset. Proof of matching is a capture-diff showing one differing input.`

`hedge-research.md` §5.2 rule 1: `**Shared automation, shared inputs.**` — and rule 2:

> `2. **Same execution class.** All arms as Exit Options, or all as Monitors. Never mixed.`

Against which, `oa-ops-runbook.md` §3:

> `let the group`
> `> be the thing that makes the arms *queryable*, not the thing that makes them *shared*.`

Tier-2 adds: presets are account-scoped (§9 row 4 — `The `UI…` namespace means presets are **account-scoped**.`)
and Exit Options link as an input only at bundle level (§9 row 3).

### The resolution — the shared object is the ENTRY side, not the exit side

The draft of this memo declared the conflict "verbal, not architectural" and resolved it toward
per-arm copies with hand-set values. **That was refuted and is withdrawn** (Appendix A). The
error was assuming the shared automation had to be the automation carrying the difference.

**Architecture E — recommended.** One shared Library automation on the **entry** side (the
scanner: entry logic, symbol, the Range075 filter), attached to every arm. The differing
variable lives in the **exit** configuration, carried per-arm as the bundle-valued Bot Input of
D-1 Option A. Every arm sits in the Exit Options execution class.

Checked against §2D clause by clause:

| §2D clause | Under Architecture E |
|---|---|
| shared automation | ✔ the entry scanner, genuinely shared via the Library |
| shared inputs | ✔ every entry input is one object |
| same execution class | ✔ all arms Exit Options — and note §9 row 1 resolved `Touch` as an Exit Option, which is what dissolved the v1 tournament's "S3 was the only Exit Option" execution-class confound. **Moving arms to Monitor class would re-introduce it.** |
| one differing input, proven by capture-diff | ✔ the exit bundle input, subject to gate G2 |
| Range075 as a preset | ⛔ **see the new finding below** |

**No amendment to frozen §2D is required for the first four clauses.** That is the strongest
argument for E: it is the only architecture that makes the frozen sentence true without asking
you to change it.

`oa-ops-runbook.md` §3 is **not contradicted** and needs no substantive change. Its warning is
about *unintended* blast radius — a Library automation edited once and changing every arm by
surprise. Under E the sharing is *designed*, and it is the mechanism that makes the arms
provably matched rather than a hazard to be forked away from.

### ⛔ NEW FINDING opened by this analysis — "Range075 as a preset" looks unbuildable

Presets are an **Exit Options** object. `oa-platform-reference.md` §6.1 quotes OA verbatim:
`Save your Exit Option criteria as a Preset to be reused for`. But Range075 is an **entry
filter**, and `hedge-research.md` §8 says so explicitly:

> `Note it is a **gap filter, not an intraday-range filter**: implement as a symbol %-change`
> `decision, not a high-low range check.`

An entry decision node cannot be an Exit Option preset. If that holds, **`build-plan.md` §2D's
"Range075 as a preset" and `hedge-research.md` §5.2 rule 3 are a category error** — the same
defect class as §7's `Conditional` correction of record, where a mechanic was specified in a
primitive that could not express it. Under Architecture E the *substance* survives untouched
(Range075 lives in the shared entry scanner, which is a stronger guarantee than a per-arm
preset), but the wording is wrong in a frozen doc and in a signed-off rule.

**This is raised as a finding, not acted on.** It needs one UI check (does the preset picker
accept anything that is not an Exit Option criterion — presumed no, not observed) plus an
"amend the plan".

### ⛔ SECOND NEW FINDING — the arm-distinctness assert is not built

`oa-ops-runbook.md` §3 promises the nightly script can `assert arm-level parameter distinctness.`
and claims this makes the S1 ≈ HedgeD failure detectable `instead of four months late.`
**Nothing in `scripts/` implements it.** `execution_audit.py` has 13 rules (S1–S8, C1–C5); the
closest is `rule_S7_duplicate_arm`, which is:

- **post-hoc and outcome-based**, not config-based — it keys on `(open_date[:16], pnl, structure)`
- **silent until 5 identical trading days** — `DUP_MIN_DAYS         = 5`
- **AMBER**, and its own remedy is `verify_by="a capture-diff of the two bots' automation trees"`
- **blind until Day-0**, since the ledger is n=0

So a wrongly-set arm on day 1 is caught by nothing until either five identical fills accumulate
or a human runs a diff. **Under any architecture, "the nightly assert" cannot be cited as a
proof leg until it exists.** Recommended: adopt `oa-ops-runbook.md` §2.2's `BUILD_ID` mechanism,
which is the only fail-loud design in the folder — *with its own precondition honoured*:
`**If that assert is not built, do not build the BUILD_ID mechanism at all.**`

### Options

| | Architecture | Amends |
|---|---|---|
| **E** | Shared entry automation; per-arm exit bundle input; all arms Exit Options | Nothing frozen (except the separate Range075 finding) |
| **S′** | Shared automation; arms as **Monitors** with per-field scalar decision inputs | Nothing frozen — but re-introduces the execution-class confound §9 row 1 just dissolved |
| **C** | Per-arm copies, hand-set values, capture-diff only | `build-plan.md` §2D **and** `hedge-research.md` §5.2 rule 1 **and** trips PR-18's kill criterion at build time |

⚠️ **Option C is worse than it looks.** `pre-registration-ledger.md` PR-18's kill criterion
voids the tournament if `shared automation · one differing input proven by` capture-diff fails
— so under C the tournament is void on day one, before it trades.

### Recommendation — **E. Amend nothing frozen. Fix one citation in `oa-ops-runbook.md` §3.**

This ruling is **coupled to D-1**: E requires D-1 = Option A. If you rule D-1 as B or C, the
tournament architecture must be re-decided, and `build-plan.md` §2D plus `hedge-research.md`
§5.2 rule 1 both need amendments. **Rule them together.**

### Draft amendment text

**(a) `docs/oa-ops-runbook.md` §3 — citation fix + one clarifying sentence.** §3 currently
instructs `Fork via **Copy** (§5, trap 1)`, and trap 1 is the claim
`oa-platform-reference.md` §2 falsified on 2026-08-03 (`state.md` lists it under *Still needing
authorization*). Replacement for that sentence:

```
> ⚠️ Shared Library automations across a cohort are **fleet-wide blast radius disguised as a
> single edit** — edit one and all arms change. That hazard is real and is about UNINTENDED
> sharing. It does not forbid DESIGNED sharing: a tournament's arms are matched precisely
> because their shared half is one object. Share the entry automation deliberately; let the
> differing half be the per-arm input; and let the group be the thing that makes the arms
> *queryable*. (⚠️ §5 trap 1's "clones share automations by reference" is FALSE — falsified
> 2026-08-03, `oa-platform-reference.md` §2. Sharing is opt-in via the Library. That trap's
> correction is separately pending authorization.)
```

**(b) `docs/hedge-research.md` §5.2 rule 3 — flag only, pending the Range075 UI check:**

```
> ⚠️ **FLAGGED 2026-08-__ — "carried as a preset" may be a category error.** Presets are an
> Exit Options object (`oa-platform-reference.md` §6.1); §8 of this file specifies Range075 as
> `a symbol %-change decision`. An entry decision cannot be an exit preset. Under the
> Architecture-E ruling the substance is stronger, not weaker — Range075 lives in the SHARED
> entry automation, so it is identical across arms by construction rather than by repetition.
> Rule 3 is not withdrawn pending a UI check; it is marked.
```

**(c) `docs/build-plan.md` §2D — no amendment under Architecture E.** If the Range075 finding
is confirmed, the following is needed —
**EXECUTES ONLY ON ANDY'S "amend the plan":**

```
*Amended 2026-08-__, at Andy's explicit instruction. "Range075 as a preset" is corrected to
"Range075 in the shared entry automation." Presets are an Exit Options object and Range075 is
an entry decision (`hedge-research.md` §8), so the original wording named a primitive that
cannot express the mechanic — the same defect class as `hedge-research.md` §7. The requirement
is unchanged in substance and strengthened in enforcement: carried once in the shared entry
automation rather than repeated per arm. Nothing else in this plan changed.*
```

**RULING (Andy) — tournament architecture (coupled to D-1):** ✅ **RULED 2026-08-04 —
Architecture E. Share the entry automation, differ on exits.** Consistent with D-1 = Option A, as
the coupling required.
**RULING (Andy) — build the arm-distinctness assert before the tournament trades?**
⏳ **NOT RULED as of 2026-08-04.** Slot left open deliberately — it was not among the seven
rulings. `.................................................................................`

---

## Decision 5 — Should the Market-pricing ban cover entries?

### The forcing fact

`oa-platform-reference.md` §7:

> `**Rule: Market pricing is banned on every exit in the v2 fleet, with one exception**`

— a hard end-of-day flat close. `oa-ops-runbook.md` §5 trap 6 states the same scope:
`**Market pricing is banned on every exit except a hard end-of-day flat close**`. The cited
mechanism, however, is about the **order type**, not the side:

> `**$5.05/contract beyond the worst price the position was ever marked at**`

— −$7,740 on $4,740 of risk, **R −1.63, n=1 position** (`T00147`; the frozen detector fixture
holds **n=2** loss-side impossible fills, `T00147` R −1.63 and `T00845` R −1.10). And
first-hand from §7, the reason the mechanism is order-type-specific:

> `selecting `Market` **collapses the Final Price ladder entirely**`

A market order takes no limit. That is true on an entry exactly as on an exit. The Fortress
enters at Market on both sides (`state.md`, *Entry pricing open question*) — so the exposure is
live today on the bot the pilot clone was cloned from.

### Options

| | Option |
|---|---|
| **A** | Extend the ban to entries. All v2 entries on SmartPricing with an explicit final price. No carve-out. |
| **B** | Keep the ban exit-scoped. Entries stay Market. |
| **C** | Extend, but as a pre-registered A/B: one arm Market entry, one SmartPricing entry. |

### Recommendation — **A, and label it a risk-control decision, not an evidence-backed one.**

**Rationale.** The carve-out's own logic does not reach entries. Market is permitted on the
flat close because fill certainty beats fill quality when expiry is minutes away and an unclosed
position is an uncapped risk. An entry has the opposite asymmetry: **if the entry does not fill,
no position opens, which costs nothing.** There is no urgency to buy with unlimited slippage.
And the downstream damage is quiet rather than loud — a bad entry credit does not show up as an
impossible fill, it shows up as a slightly wrong denominator on every subsequent measurement of
that position, and `CLAUDE.md` §4's R convention is the `ror` basis (return on RISK), so it
propagates silently into the one number the whole program compares by.

**The honesty caveat, and it is important.** The fill evidence here is **n=1 position** for the
$5.05 figure and **n=2** in the frozen fixture — far below `CLAUDE.md` §4's T2 gate (n≥100
positions / 6 months / a regime change). **This cannot be sold as an evidence-backed decision
and this memo does not sell it as one.** It is a decision about a mechanism with unbounded
downside and a cheap alternative, taken on mechanism rather than on sample. Recording it that
way is what keeps the evidence law meaning something.

**Known cost, to be accepted explicitly:** a limit-priced entry that does not fill biases the
sample toward days when spreads were tight — a selection effect on the entry distribution
rather than on the exit distribution. Mitigation: a generous final price (the ladder is
`min="50" max="150"`, first-hand) rather than Market, and **log non-fills** so the selection
effect is measurable rather than invisible. Option C would measure it directly, but it spends
an arm slot on a question that has no plausible upside branch — Market entry cannot be *better*
than a generous limit, only faster.

**Sequencing:** this is a value change, so `CLAUDE.md` §5 governs — pilot on a dead bot, the
champion goes last, and nothing changes during a streak.

### Draft amendment text

**`docs/oa-platform-reference.md` §7 — ⛔ NOT EDITED here** (the rule sits inside §7, which is
not gated, but the wording is quoted verbatim by `oa-ops-runbook.md` §5 trap 6 and by
`hedge-research.md` §10, so it changes as a set). Draft append for §7:

```
> ### 📝 APPENDED 2026-08-__ — the ban is extended to ENTRIES. Ruled by Andy, decision memo 2026-08-04.
> The mechanism above is **order-type-specific, not side-specific**: a market order takes no
> limit (first-hand — selecting `Market` collapses the Final Price ladder), so an entry carries
> the same unbounded-slippage exposure. The flat-close carve-out does NOT extend to entries:
> its logic is that fill certainty beats fill quality when an unclosed position is an uncapped
> risk, and an unfilled ENTRY is simply no position — a costless outcome.
> **Amended rule: Market pricing is banned on every entry and every exit in the v2 fleet, with
> one exception — a hard end-of-day flat close.**
> ⚠️ **Evidence tier: this is a mechanism decision, not a sample decision.** The impossible-fill
> evidence is n=1 position (`T00147`, R −1.63; n=2 in the frozen fixture with `T00845`, R −1.10),
> below `CLAUDE.md` §4's T2 gate. **Accepted cost:** limit entries that do not fill bias the
> entry distribution toward tight-spread days. **Log non-fills** so that bias is measurable.
```

**`docs/oa-ops-runbook.md` §5 trap 6, counter column** — replacement for one cell:
`**Market pricing is banned on every entry and every exit except a hard end-of-day flat close**`

**RULING (Andy) — Decision 5:** ✅ **RULED 2026-08-04 — extend the Market-pricing ban to
ENTRIES.** Recorded as a **MECHANISM decision, not an evidence-backed one** (n=1 position for the
$5.05 figure, n=2 in the frozen fixture — below `CLAUDE.md` §4's T2 gate), per the memo's wording.

---

## Decision 6 — The §8.2 attribution guard

### The forcing fact

`oa-platform-reference.md` §8.2:

> `Give the Event a **distinct SmartPricing setting** from the Exit Option so the`
> Trades list distinguishes them

The backstop was built `Market` under §7's flat-close carve-out. But per `state.md`:

> `the existing **Expiration (15:50) exit is ALSO `Market`**`

so the pricing distinction §8.2 asks for does not exist. What remains: the memo string
(`state.md`: `tree = Positions loop (unrestricted) → Close Position (`Market`, 100%, memo` /
`  `1552 backstop flat close`). Warnings 0.`) and a 2-minute timestamp gap.

### Why the memo + gap are weaker than they look

The 2-minute gap collides with the exit-order lifetime. `oa-platform-reference.md` §6.4 quotes
OA verbatim: `no additional orders will be sent to your broker` — orders triggered by an exit
option stay active **two minutes**. **A 15:50 Exit Option order is therefore still live at
15:52 when the backstop fires.** The two mechanics genuinely overlap in time, and with identical
pricing the resulting fill is ambiguous in exactly the window that matters. Separately,
`oa-ops-runbook.md` §4.4's timestamp-gap test is calibrated on `:00`/`:01–:02` gaps for sibling
closes — a 2-minute designed gap sits on top of its discrimination threshold, not clear of it.
And per `state.md`'s Tier-1 block, OA states there is
`no guarantee an automation will run exactly on` the 15-minute marks, so the 2 minutes is a
nominal figure, not a measured one.

### Options

| | Option | Cost |
|---|---|---|
| **A** | Keep as-is; rely on memo + timestamp | Free. Leaves §8.2 unsatisfied and the overlap ambiguous. |
| **B** | **Set the 15:50 Expiration exit to SmartPricing (`speedy`)** | One config change on the pilot clone. Restores pricing distinction. |
| **C** | Set the backstop to SmartPricing | ⛔ Violates §7's carve-out — the flat close is where fill certainty is the point. |
| **D** | Remove the 15:50 Expiration exit; let 15:52 be the only time close | Loses the PT-independent time exit and makes the Events class a single point of failure. |

### Recommendation — **B.**

**Rationale.** §7's carve-out is for `a hard end-of-day flat close, where fill certainty beats
fill quality`. **The 15:50 Expiration exit is not that.** It is a routine time exit with roughly
nine minutes of Exit Options window left to run (Exit Options run to ~15:59 per the two-window
Bot Schedule finding), and it is `Market` only because it was inherited from the original
Fortress configuration — nothing ever specified it. So it is already inside §7's existing ban by
that ban's own terms, and Decision 5 would put it there twice over. Setting it to `speedy`
(up to 3 prices / 5s each, first-hand verified — note the internal value is `speedy`, not
`fast`, and any capture parser keying on "fast" will silently miss it) restores the §8.2
distinction at the pricing level, leaves the backstop's fill certainty untouched, and makes the
detector's job real: `execution_audit.py`'s `rule_C5_backstop_caught_it` reads `time_exit` and
`event_backstop` as separate config columns for exactly this purpose.

**Interaction with D-3, worth stating:** if `itmpaper` is set to `market`, then at 15:50 the ITM
action is Market and the Expiration Exit Option is SmartPricing — which makes those two
distinguishable in the fill record as well. Ruling B and D-3-market together produces three
mutually distinguishable mechanics; ruling A and D-3-market produces three Market orders inside
two minutes with only memo strings to tell them apart.

⚠️ **This is an OA config change on the pilot clone, and it is a value change, not a
behaviour-neutral refactor.** `CLAUDE.md` §5 sequencing applies. §8 of the platform reference is
gated, so the section text is **not edited** — the draft append is recorded for authorization.

### Draft amendment text

**`docs/oa-platform-reference.md` §8.2 — ⛔ NOT EDITED, §8 IS GATED.** Recorded for Andy:

```
> ### 📝 APPENDED 2026-08-__ — attribution restored by re-pricing the 15:50 exit. Ruled by Andy, decision memo 2026-08-04.
> As built, the 15:52 Event backstop and the 15:50 Expiration Exit Option were BOTH `Market`,
> so the attribution guard above was unsatisfied. Resolved by setting the **Expiration exit** to
> SmartPricing (`speedy`), NOT by re-pricing the backstop — §7's carve-out is for the hard flat
> close specifically, and the 15:50 exit is a routine time exit with the Exit Options window
> still open to ~15:59.
> ⚠️ The two mechanics OVERLAP: an exit-option order stays live two minutes (§6.4), so the
> 15:50 order is still working when the backstop fires at 15:52. The timestamp gap alone was
> never sufficient. `execution_audit.py`'s `BACKSTOP_CAUGHT_IT` still requires `time_exit` and
> `event_backstop` as separate config columns.
```

**RULING (Andy) — Decision 6:** ✅ **RULED 2026-08-04 — re-price the 15:50 Expiration exit OFF
Market; the 15:52 backstop KEEPS Market.**
⏸ **EXECUTION DEFERRED, and the deferral is part of the ruling.** The pilot's **Template V1 /
PR-03 config hash is now frozen**, so this is a **spec change, not a config tweak**. It lands as
**Template V2 with an amended pre-registration, before Day-0** — **not as a quiet edit now.**

---

## Decision 7 — Clone residue

### The forcing fact

`state.md`, *WRITES MADE TO THE CLONE 2026-08-04 — Andy's call, not reverted*:

> `1. Account now holds Exit Option preset **`TIER2-CHECK4-PUTSIDE`**`
> `   (`UIfw5TkkCRF1517858152565216101`). The account previously held **zero** presets.`

and, on the scanner save:

> `numeric payload byte-identical (`^^0.5|0.01^$0`: 50% PT, 10-min`
> `   expiration, Market pricing all unchanged)`

with the `text` label changed `"Profits: 50%, …"` → `"Profit: 50%, …"` and
`the sig gained an `xevents` key`. Plus three open loose ends:

> `ScannerA still named`
> `  `Fortress-ScannerA-PutSpread-CLONE` (revert pending), Bot Group is `None` (was `Monitor`),`
> `  Tags are empty (were `experiment`).`

### Item-by-item recommendation

**1. Preset `TIER2-CHECK4-PUTSIDE` → KEEP (defer the naming decision).**
Blast radius is zero: a preset is an inert account object until something selects it. Its
evidentiary value is not zero: it is the artifact behind §9 row 4's finding that presets are
account-scoped and cross-automation, and deleting it makes that finding unreproducible for no
gain. Its name is a test string in a namespace that will hold production presets — but **the
greenfield preset naming convention does not exist yet**, and whether a preset can be *renamed*
at all was **not observed**. Do not assume it can. Decide its final name or deletion when the
greenfield spec defines the convention; until then it is a labelled test artifact, which is what
it is.

**2. The re-serialized `exits` blob → KEEP. Do not attempt a revert.**
The numeric payload is byte-identical, so behaviour is unchanged. More to the point, **a
re-serialization cannot be reverted by saving** — another save re-serializes again and produces
a *new* diff. The only true revert is delete-and-re-clone, which throws away the 15:52 backstop
build (`Fortress-Backstop-1552-FlatClose`, verified by hard reload) and burns a bot slot to undo
a cosmetic label change. Instead: **treat the clone's current state as its birth state.** The
pre-registration `CONFIG HASH` field is still `<capture> @ <hash>` — unfilled — so nothing has
been anchored to the pre-save bytes. Behaviour is verified at Day-0 by the standard that governs
anyway: `oa-ops-runbook.md` §4.1's Trades-list check, PT row present at 50%.
⚠️ **Worth recording as a platform fact:** OA re-serializes an `exits` blob on save even when
nothing was changed. **Any capture-diff that compares rendered labels rather than decoded
payloads will report a false difference.** This directly affects Decision 4's proof procedure
and D-1's gate G2.

**3. ScannerA's `-CLONE` name → REVERT**, as part of the clone ritual, not as a separate task.
`state.md` already records the intent (`revert pending`), and clone-ritual Steps 5c and 6–9 are
not started. Fold it in; do not make a standalone edit out of it.

**4. Bot Group `None` → DO NOT restore `Monitor`. Set at the Phase 4 sweep.**
`Monitor` is not in the v2 scheme — `oa-ops-runbook.md` §3 sets `Group = Pillar`
(`IC` · `Directional` · `OA-Mirror` · `Lab`), and §3 explicitly says to do the group
reorganisation as part of the Phase 4 sweep — `— otherwise you sort bots you are about to archive.`
⚠️ **But `None` carries an unverified risk:** trap 4 is that the export respects the group
filter, and **whether a bot in NO group is included when "all groups" are selected has not been
observed.** If it is excluded, an ungrouped pilot silently vanishes from the export that builds
the ledger. **Recommend: leave `None`, and add "does an ungrouped bot appear in an all-groups
export?" to the open UI checks** — it is a one-minute check with a ledger-integrity consequence.

**5. Tags empty → REVERT, restore `experiment`.**
Cheap, reversible, and tags are the only writable state on the platform
(`oa-platform-reference.md` §5.3). An untagged pilot is invisible to any tag-based query and to
any future tag-ladder mechanic. No reason to leave it empty.

**RULING (Andy) — preset:** ✅ **RULED AND EXECUTED 2026-08-04 — `TIER2-CHECK4-PUTSIDE` KEPT.**
**RULING (Andy) — exits blob:** ⏳ **NOT SEPARATELY RULED.** Decision 7's ruling names the
ScannerA name, the tag, the Bot Group and the preset; the re-serialized `exits` blob is not among
them and no revert was reported. It stands as-is — which is also what the recommendation above
concluded, since a re-serialization cannot be reverted by saving. **Recorded as unruled, not as
ruled-by-silence.** `.......................................................................`
**RULING (Andy) — `-CLONE` name / Bot Group / Tags:** ✅ **RULED AND EXECUTED 2026-08-04 —
ScannerA name REVERTED and tag REVERTED. Bot Group stays UNSET until the Phase 4 sweep**, per
`oa-ops-runbook.md` §3's sequencing.
**RULING (Andy) — add the ungrouped-export UI check?** ⏳ **NOT RULED as of 2026-08-04.** Slot
left open deliberately — it was not among the seven rulings. ⚠️ Still live: the pilot's Bot Group
remains unset by the ruling above. `...................................................`

---

## Appendix A — Adversarial review: what survived

Two subagents were spawned with instructions to **refute** the memo's D-1 and tournament
recommendations, defaulting to "this is wrong." Both succeeded. The recommendations above are
the post-review positions. Recorded here so the reversal is auditable and so the surviving
caveats travel with the ruling.

### Reversal 1 — D-1: the memo originally recommended per-arm hand-set values. Withdrawn.

Objections that forced it:

1. **FATAL — `hard-PT vs trailing vs ride` differ in 2–3 FIELDS, not one.** They populate
   different Exit-Options fields. Only at bundle granularity is §2D's `arms differing / in
   exactly one input value` literally true. The recommendation that "avoids amending the frozen
   plan" is Option A, not the hand-set option.
2. **FATAL — the cited failure argues the opposite way.** `HedgeA-S1` ≈ `HedgeD` ≈ `HedgeTest`
   (73/73/70 identical positions, n=3 bots) were **independently hand-set bots with no inputs**.
   Hand-setting produced the identity class; a shared definition plus one differing variable
   makes a three-way identity arithmetically impossible.
3. **FATAL — the recommendation guts the guards it cited as proof.** `pre-registration-ledger.md`
   PR-14…PR-17's family-level kill criterion reads `more than one differing input`; with no
   inputs it can never fire.
4. **FATAL — "the blob is opaque" is false.** The payload `^^0.5|0.01^$0` has already been
   decoded three times in this folder. Diff legibility is a ~20-line parser feature, not an
   architecture constraint. **(Survives as gate G2: it is only true if the capture stores the
   payload rather than an input reference — unverified.)**
5. **MATERIAL — silent-fallback runs the other way.** One bundle input = one breakable link, one
   loud sentinel (`-999`), one assert surface. 4–6 hand-set bundles = no link, no sentinel, no
   designed detector. **The fleet already accepts this trade** in `oa-ops-runbook.md` §2.2's
   `BUILD_ID` bot input, so rejecting Option A on fallback grounds is inconsistent.
6. **MATERIAL, SURVIVES INTO THE RULING — nothing catches a day-1 hand-set error under ANY
   architecture.** `rule_S7_duplicate_arm` needs 5 identical trading days (`DUP_MIN_DAYS = 5`),
   is AMBER, and detects accidental *sameness* — never a wrong-but-distinct value. A capture-diff
   of arms against each other diffs clean if all arms were mistyped identically. This is a real
   uncovered hole and it is why the `BUILD_ID` loud-fail assert is recommended alongside.
7. **MATERIAL, SURVIVES — a per-arm preset enforces nothing.** `oa-platform-reference.md` §6.1:
   `**A preset makes the VALUES consistent, not the ATTACHMENT.**` Whether editing a preset
   propagates to attached actions is unverified either way, and **both branches hurt** — if it
   propagates, an account-scoped preset has account-wide blast radius; if not, per-arm presets
   give no ongoing guarantee. **This is gate G4.**
8. **WEAK, but scoped into the ruling — do not over-reject.** Decision-side variables ARE
   per-field linkable, so a blanket "no bot inputs" verdict would foreclose the hedge rebuild.
   The D-1 ruling is scoped to the greenfield IC family only.

**Not conceded:** the reviewer's claim that Option A "dominates on every axis" understates gate
G1 (can a bundle input hold an empty value, for the `ride` arm). That gate is unaddressed in
every file and is why the recommendation is conditional rather than clean.

### Reversal 2 — Decision 4: the memo originally called the conflict "verbal" and chose per-arm copies. Withdrawn.

1. **FATAL — "only two architectures" was false.** The shared object need not be the object
   carrying the difference. Sharing the **entry** automation (Architecture E) satisfies §2D
   literally while the exits differ per arm. A Monitor-class variant (S′) is also live, since
   `hedge-research.md` §5.2 rule 2 permits `All arms as Exit Options, or all as Monitors.`
   **(E is preferred over S′ because §9 row 1 resolved `Touch` as an Exit Option, which is what
   dissolved the v1 execution-class confound. S′ would re-introduce it.)**
2. **FATAL — the omitted binding document.** `pre-registration-ledger.md` PR-18's kill criterion
   voids the tournament if `shared automation · one differing input proven by` capture-diff
   fails. Under per-arm copies the tournament is void at build time.
3. **FATAL — the enforcement cited does not exist.** See Decision 4's second new finding.
4. **MATERIAL, SURVIVES — capture-diff cannot catch the v1 failure class.** `hedge-research.md`
   §7 on the `HedgeD-Conditional` arm: `**This is a distinct failure pattern: an undocumented
   substitution made at a platform limit.**` — config and tree agreed with each other and both
   were wrong about intent. The named defence is §5.2 rule 4 (pre-registration naming the
   **primitive**), not the diff. **Consequence for the ruling: the capture-diff is necessary and
   not sufficient, and every arm's pre-registration must name the platform primitive.**
5. **MATERIAL, SURVIVES — the capture-diff has a known false-positive mode.** The Exit Options
   line in a capture is a *rendered label*, and the clone's label drifted
   `"Profits: 50%, …"` → `"Profit: 50%, …"` while the payload was byte-identical. A differing
   line does not entail a differing value. **The diff must decode, not compare strings** —
   same conclusion as D-1 gate G2, reached independently.
6. **MATERIAL, FOLDED IN — "ops-runbook §3 needs no change" was wrong** because §3 cites
   `(§5, trap 1)`, and trap 1 is falsified and pending authorization. Hence draft amendment (a).
7. **MATERIAL, FOLDED IN — Range075 as a preset.** Raised as Decision 4's first new finding.
8. **MATERIAL, ACKNOWLEDGED — this is Andy's call, not a wording cleanup.** `state.md` and §9
   row 3 both reserve it: `**Andy's decision` before anything is written into the spec.` Which
   is why it is in this memo as a ruling line rather than executed.

**Not conceded:** the reviewer's objection that the ⛔ CONTESTED clone finding is misapplied is
correct on its own terms — the hedge arms are fresh builds with no parent — but it does not
change the ruling, because Architecture E does not rest on that finding.

---

## Appendix B — New findings opened by this memo (none acted on)

| # | Finding | Where it bites |
|---|---|---|
| **N-1** | `build-plan.md` §5.2 / §8.1 do not exist. The plan has §1–§6. Broken citation replicated in `state.md`, `session-log.md`, `sprint-2026-08-04.md`. | D-1 is not, by itself, a plan amendment. |
| **N-2** | **"Range075 as a preset" appears unbuildable** — presets are an Exit Options object; Range075 is an entry decision (`hedge-research.md` §8). | `build-plan.md` §2D (frozen) + `hedge-research.md` §5.2 rule 3. Needs a UI check + "amend the plan". |
| **N-3** | **The arm-distinctness assert `oa-ops-runbook.md` §3 promises is not built.** `execution_audit.py` has 13 rules; the nearest is post-hoc, outcome-based, AMBER, and silent below 5 identical days. | Any tournament citing it as a proof leg. |
| **N-4** | **OA re-serializes an `exits` blob on save even when nothing changed** — label drift with a byte-identical payload. | Every capture-diff. Compare decoded payloads, never rendered labels. |
| **N-5** | **Whether an ungrouped bot appears in an all-groups export is unobserved.** The pilot clone is currently `Bot Group = None`. | Ledger integrity (trap 4). One-minute check. |
| **N-6** | **A 15:50 exit order is still live at 15:52** (two-minute order lifetime, §6.4), so the backstop's 2-minute gap does not cleanly separate the mechanics. | Decision 6; `oa-ops-runbook.md` §4.4's gap test. |
| **N-7** | `sprint-2026-08-04.md` Task 5 assumes pre-registration entries carry the failsafe as June cause. **They do not** — one mention, in a different role. | Prevents an invented edit downstream. |

---

## Appendix C — Files changed by this session

**Written:**

- `docs/decision-memo-2026-08-04.md` — this file. New.

**Not changed, deliberately:** `docs/build-plan.md`, `docs/oa-platform-reference.md` (all
sections, §8 included), `docs/hedge-research.md`, `docs/oa-ops-runbook.md`,
`docs/pre-registration-ledger.md`, `docs/reactivation-runbook.md`, `docs/state.md`. Every
amendment in this memo is **draft text awaiting a ruling.** No OA edit was made. No git command
was run.

**Pending the close-out sequence (`CLAUDE.md` §9.1):** `docs/session-log.md` append and any
`docs/state.md` update follow this memo; the tracker artifact update needs Andy's visual
confirmation to be complete.
