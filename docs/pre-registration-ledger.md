# Pre-registration ledger

*Written 2026-07-31 for Bot Fleet v2. Template + drafted entries for every planned active bot.*

> ## ⚠️ EVERY ENTRY BELOW IS A DRAFT. NONE IS SIGNED.
> **Day-0 is signing, not authoring.** Drafting them now means the day the account comes back is
> a short checklist rather than a writing session — which is the only reason they exist yet.
>
> An entry becomes binding when Andy fills its `SIGNED` line with a date and a config-capture
> hash. **Until then it authorises nothing.**
>
> **No entry, no restart.** A bot without a signed entry stays OFF on Day-0, regardless of how
> ready it looks. This is `build-plan.md` §5 and `CLAUDE.md` §5, and it applies to all ~~≈18–20
> active bots~~ **≈18–20 plan bots plus up to 8 pre-registered Track B arms — ceiling 28** —
> **including the nine untouched ones**, and including every Track B arm.
>
> > **📝 SCOPED 2026-08-05 on Andy's explicit release — `build-plan.md` §2D's
> > `🔓 SCOPING AMENDMENT 2026-08-05` ("amend the plan", Andy's explicit words).** §2D now reads
> > *"End state: ≈18–20 plan bots plus ≤8 pre-registered Track B arms (`research-loop-spec.md`
> > §10, signed), ceiling 28."* Track B is a **separate allocation**, not a silent collision with
> > the plan count (ruling **S-1**; `track-b-arms-spec.md` §3.3/§3.5). Operative figures:
> > **≈18–20 plan bots · wave-1 Track B spend 2 · ceiling 28**, against a Pro cap of 50 that
> > counts **active** bots only (**C12 discharged** — `[FIRST-HAND, UNCORROBORATED]`, residual and
> > reopen condition at `track-b-arms-spec.md` §3.2). **Wave 1 is 22 of 50.**
> > ⛔ **The amendment scopes a count. It authorizes no build** — and it changes nothing about
> > *this* document's rule: **no entry, no restart**, for plan bots and Track B arms alike.

---

## 1. Why this exists, in one paragraph

The v1 fleet had pre-committed rules. They fired. They were then re-opened for debate rather
than executed, and the audit's §3.5 finding is the reason this document is structured the way it
is:

> *"When a pre-committed rule fired against a system the owner is attached to, the rule was
> re-opened for debate rather than executed. Every one of these deferrals happens to keep a
> losing bot running. None of them ever went the other way. **No strategy the owner built
> himself has ever been killed by a triggered rule.** That asymmetry is the whole tell."*

So the design constraint is not "write down a criterion." It is **write down a criterion that
can fire without you.** Every field below exists to make that possible.

---

## 2. The template

Copy this block per bot. Fields are mandatory unless marked optional.

```
### <exact OA bot name>
ID               PR-NN            two digits, assigned in this ledger's entry order. The OA
                                  template Tag is the bare ID, e.g. `PR-03`.
DISPOSITION      clone-to-spec | untouched | fresh build     (build-plan.md §2 group)
PILLAR / ROLE    IC | Directional | OA-Mirror  ·  candidate | control | experiment | mirror-watch
STATUS           DRAFT — unsigned

HYPOTHESIS       One falsifiable sentence. What this bot is being run to find out, stated so
                 that a result could contradict it. Not "test the strategy."
MECHANISM        Why it should make money — a named economic source. Per audit gate E1,
                 "it backtested well" is not a mechanism. AND the platform primitive it will
                 be built from, so a substitution at a platform limit has something to
                 contradict (see the HedgeD lesson, hedge-research.md §7).
KILL CRITERION   R-based. Must be falsifiable from data the daily loop already produces, and
                 must be able to fire in code with no human in the loop.
SAMPLE TARGET    n, in positions. The audit's admissibility bar is n≥100 at T1/T2 over
                 ≥6 months incl. a regime change (evidence-standards §4, gate B).
REVIEW DATE      Day-0 + N. Relative, because Day-0 is not yet fixed.
MAX LOSS         Per-position $ risk cap, and the daily aggregate this bot may contribute.
SIZING TIER      1 lot (experiment) | ≈$5K risk/position (CANDIDATE+). Set once, never ad hoc.
CONFIG HASH      <capture file> @ <hash>            ← filled at signing, from the capture
VERIFICATION     The artifact that proves it is running as declared, before it may trade.
SIGNED           <date> ................................  ← blank until Andy signs
```

**Three rules about filling it in:**

1. **The kill criterion is in R.** Never dollars, never win rate. A fleet-wide win-rate bar was
   retired 2026-07-31 precisely because it fired on the champion and was argued with instead of
   executed (`evidence-standards.md` §7).
2. **A criterion needing evidence nobody collects is not a criterion.** If the daily loop does
   not produce the number, either the loop changes or the criterion does.
3. **A fired trigger not executed within 48 hours is itself a kill condition.** That rule is
   what makes the rest of it real.

---

## 3. The roster — ≈18–20 plan bots, plus ≤8 Track B arms. Ceiling 28.

~~Per `build-plan.md` §2, under decision freeze: **4 clones + 9 untouched + 5–7 fresh.**~~
Per `build-plan.md` §2 as amended 2026-08-05: **4 clones + 9 untouched + 5–7 fresh
= ≈18–20 plan bots**, **plus ≤8 pre-registered Track B arms** as a separate allocation.

| Group | Count | Entries below |
|---|--:|---|
| **B — clone-to-spec** (original archived) | 4 | §4 |
| **C — untouched** (validated, lived through the lapse) | 9 | §5 |
| **D — fresh builds** | 5–7 | §6 |
| **plan-bot subtotal** | **≈18–20** | |
| **Track B arms** (separate allocation, `research-loop-spec.md` §10) | **≤8** | `track-b-arms-spec.md` §9 — PR-21 / PR-22 proposed, wave-1 spend **2** |
| **ceiling** | **28** | |

> ### 📝 SCOPED 2026-08-05 — S-2's count amendment propagated here on Andy's explicit release
> **This heading and line previously read `≈18–20 active bots` / `4 clones + 9 untouched + 5–7
> fresh`, struck above.** `build-plan.md` §2D now carries a
> `🔓 SCOPING AMENDMENT 2026-08-05 — "amend the plan", Andy's explicit words` block reading
> **`End state: ≈18–20 plan bots plus ≤8 pre-registered Track B arms (research-loop-spec.md §10,
> signed), ceiling 28.`** It cites `track-b-arms-spec.md` §3.5 and closes **S-2** by name.
> Ruling **S-1** established the separation: the seven greenfield family bots are §2D **fresh
> builds** (Group D above), **not** Track B spend, so `n_used = 20` and **Track B keeps all 8**.
>
> **Against the Pro 50-bot cap: wave 1 is 22 of 50, ceiling 28 of 50.** The denominator counts
> **ACTIVE** bots — **C12 discharged**, `[FIRST-HAND 2026-08-04, `/bots` footer read]`:
> `35 active bots • 15 left in your plan` immediately after the Fortress original was archived
> (against `36 active` through three failed attempts), so **35 + 15 = 50** and archived bots do
> not consume slots. ⚠️ **Residual, carried:** tier `[FIRST-HAND, UNCORROBORATED]` — that is the
> footer's *accounting*, not OA's *enforcement* (`left = 50 − active` renders identically under
> either hypothesis), observed with **one** archived bot where the Group-A sweep archives
> **twenty**. ⛔ **Pre-declared reopen: if a build ever fails at the cap despite archived bots
> existing, C12 reopens.** Full block: `track-b-arms-spec.md` §3.2.
>
> ⛔ **This scopes a count and authorizes no build.** Every Track B arm needs its own signed
> entry here before it may be switched on — PR-21 and PR-22 are **DRAFT and unsigned**, and
> ARM-B1 is **not an arm** until C10/C11 close (`track-b-arms-spec.md` §10).

---

## 4. Group B — the four clones

### `IC-SPX-FastPT25-S2` (clone; original archived `-ARCHIVED-<date>`)
```
ID               PR-01
DISPOSITION      clone-to-spec        PILLAR/ROLE  IC · control        STATUS  DRAFT — unsigned
HYPOTHESIS       The legacy configuration, run as ride+S2 with no Exit Options at all, has
                 non-negative Exp(R) per condor over ≥100 post-cutover positions. This is the
                 RIDE BENCHMARK the greenfield PT variants are measured against — it is not
                 expected to win, it is expected to be a clean baseline.
MECHANISM        Short-premium variance risk premium on SPX 0DTE, with S2 strike-touch close
                 capping the tail. Primitive: S2 is a MONITOR (automations side); PT25 is
                 REMOVED from the Open Position action, not toggled off.
KILL CRITERION   Exp(R) per condor < −0.02 with the bootstrap 95% CI entirely below 0, at n≥60.
                 OR: any REMOVED_EXIT_FIRED finding — a PT firing on a bot whose PT was deleted
                 means it is no longer the ride benchmark and the comparison is void.
SAMPLE TARGET    n = 100 positions (condors), T2 paper.
REVIEW DATE      Day-0 + 6 months, with an interim read at n=60.
MAX LOSS         ≈$5K risk/position. Daily aggregate ≤ $10K across the SPX IC sleeve.
SIZING TIER      ≈$5K risk/position (CANDIDATE tier).
CONFIG HASH      <capture> @ <hash>
VERIFICATION     INVERTED — the first new position's Trades list must contain NO PT row and NO
                 exit-trigger row, and the S2 monitor must be observed firing. Both toggles
                 screenshotted. Exit Options panel is not evidence.
SIGNED           ..............................
```
> ⚠️ **This entry deliberately does NOT inherit the 29 post-fix condors.** `build-plan.md` §4:
> the clone is a fresh pre-registered control at n=0; the old "the baseline continues unbroken"
> argument is dead and must not reappear.

### `IC-SPX-FastPT25-S2-130PM` (clone; original archived)
```
ID               PR-02
DISPOSITION      clone-to-spec        PILLAR/ROLE  IC · experiment     STATUS  DRAFT — unsigned
HYPOTHESIS       A 1:30 PM entry produces a materially lower short-strike touch rate than the
                 11:00 entry, and that difference shows up as higher Exp(R) per condor. The A/B
                 partner above; ONLY entry time differs.
MECHANISM        Less time to expiry = less path for the underlying to reach the short strike.
                 The v1 S2 diagnostic located the bleed at touch FREQUENCY (~40% of legs), not
                 at the hedge — this tests the cheapest lever on that. Primitive: a General
                 time-of-day decision node, verified present, not assumed.
KILL CRITERION   Exp(R) per condor is not better than the 11:00 arm's by ≥0.01 at n≥60 with
                 non-overlapping bootstrap CIs. A null result kills the ENTRY-TIME question,
                 not the bot.
SAMPLE TARGET    n = 100 positions, matched days with the 11:00 arm.
REVIEW DATE      Day-0 + 6 months, interim at n=60.
MAX LOSS         ≈$5K risk/position, inside the same $10K SPX IC daily aggregate.
SIZING TIER      ≈$5K risk/position — IDENTICAL allocation to the 11:00 arm. Non-negotiable:
                 unequal sizing makes the A/B unreadable.
CONFIG HASH      <capture> @ <hash>
VERIFICATION     INVERTED, as above. PLUS: the first five entries' timestamps land in the
                 declared window. The 11:00 gate on the v1 bot was never implemented and ran
                 20+ sessions before anyone noticed.
SIGNED           ..............................
```

### `QQQ-IC-0DTE-Fortress` (clone; original archived) — the pilot bot
```
ID               PR-03
DISPOSITION      clone-to-spec        PILLAR/ROLE  IC · experiment     STATUS  DRAFT — unsigned
HYPOTHESIS       With PT50 and the time exit actually attached and firing, this structure has
                 positive Exp(R) per condor. The pre-regression window (+2.9% Exp(R), 21
                 condors) suggested it does; that window is archive-only context and this
                 starts at n=0.
MECHANISM        Short-premium VRP on QQQ 0DTE with profit-taking before the late-day gamma
                 window. Primitives: PT50 + 15:50 time exit as a NAMED EXIT OPTION PRESET in
                 the Open Position action, plus a flat-close Scheduled Event backstop in the
                 AUTOMATIONS execution class.
KILL CRITERION   Exp(R) per condor < 0 with the bootstrap 95% CI entirely below 0, at n≥60.
                 OR: any EXPIRY_RATIO_FLIP finding — positions expiring instead of closing is
                 the exact 6/12 signature, and it is a mechanics kill, not a strategy kill.
SAMPLE TARGET    n = 100 positions.
REVIEW DATE      Day-0 + 6 months, interim at n=60.
MAX LOSS         ≈$5K risk/position. Daily aggregate ≤ $10K across the QQQ IC sleeve.
SIZING TIER      ≈$5K risk/position — IDENTICAL to the NoPT50 arm.
CONFIG HASH      <capture> @ <hash>
VERIFICATION     First new position's Trades list contains BOTH a PT row and a time-exit row.
                 Plus a BACKSTOP_CAUGHT_IT check on day 1: the backstop must NOT be the thing
                 closing positions.
SIGNED           ..............................
```
> ⚠️ **This is the pilot bot for the 9-step clone ritual** (runbook §3 Step A). Nothing else in
> Phase 4 starts until this one is clean.
> ⚠️ **The 15:52 backstop timestamp is unverified** — the Market-close trigger is hard-coded to
> 3:50 pm and Exit Options stop 1 minute before close. A Repeating trigger may reach 15:52;
> nobody has checked. `oa-platform-reference.md` §8.2. **Resolve before signing.**

### `QQQ-IC-0DTE-Fortress-NoPT50` (clone; original archived)
```
ID               PR-04
DISPOSITION      clone-to-spec        PILLAR/ROLE  IC · experiment     STATUS  DRAFT — unsigned
HYPOTHESIS       Removing the profit target improves Exp(R) per condor versus the PT50 arm —
                 i.e. PT50 caps winners more than it protects. The genuine A/B: PT50 vs none,
                 everything else matched.
MECHANISM        Same VRP source. The difference is exit policy only. Primitives: 15:50 time
                 exit + flat-close Scheduled Event backstop. NO PT50 — removed from the action,
                 not toggled off.
KILL CRITERION   Exp(R) per condor < 0 with the CI entirely below 0 at n≥60. OR any
                 REMOVED_EXIT_FIRED finding at the PT50 rung — a PT firing here voids the A/B.
SAMPLE TARGET    n = 100 positions, matched days with the Fortress arm.
REVIEW DATE      Day-0 + 6 months, interim at n=60.
MAX LOSS         ≈$5K risk/position, inside the same $10K QQQ IC daily aggregate.
SIZING TIER      ≈$5K risk/position — IDENTICAL to the Fortress arm.
CONFIG HASH      <capture> @ <hash>
VERIFICATION     Trades list contains a time-exit row and NO PT row. Same backstop check.
SIGNED           ..............................
```
> The name is accurate under this spec — `build-plan.md` §2B resolved the earlier
> name-vs-spec conflict in favour of keeping the name and removing the PT.

---

## 5. Group C — the nine untouched

**These need entries too.** They are the only bots that lived through the lapse, and "we didn't
change it" is not a hypothesis. Their kill criteria are mostly **funding** decisions rather than
strategy ones.

### `DIR-SPX-PutVIX22-SL75`
```
ID               PR-05
DISPOSITION      untouched            PILLAR/ROLE  Directional · experiment   STATUS  DRAFT
HYPOTHESIS       A VIX≥22-gated long put debit spread has positive RoR out-of-sample. Backtest
                 +6.4% RoR OOS, params frozen. The open question is not the edge — it is
                 whether the bot is ALIVE.
MECHANISM        Directional convexity in high-vol selloffs; defined risk by construction (the
                 debit). Primitive: VIX gate in a Passes-market-conditions node.
KILL CRITERION   Exp(R) per position < −0.10 with CI below 0 at n≥50. SEPARATELY, a LIVENESS
                 kill: zero bot-log entries across any 10-session window = presumed OFF or
                 failsafe-tripped → RED, and the bot is switched off pending investigation.
SAMPLE TARGET    n = 50 positions (the gate is selective — 0 fired in 22 days).
REVIEW DATE      Day-0 + 6 months. Liveness reviewed WEEKLY from day 1.
MAX LOSS         1 lot, ≈$500/position (the debit).
SIZING TIER      1 lot — experiment.
CONFIG HASH      <capture> @ <hash>
VERIFICATION     ⚠️ CANNOT be verified from position data. A correctly-gated bot and a dead bot
                 are indistinguishable. **The bot LOG is the only proof**: a scanner run with no
                 entry = healthy. Both toggles ON and screenshotted.
SIGNED           ..............................
```
> ⛔ **The zero-trade bot that must NOT be deleted.** Zero positions in 22 days because its
> VIX≥22 gate correctly never fired. `build-plan.md` §2 and runbook Step B both carry this as a
> one-way-door call-out.

### `DIR-SPX-CallVIXdrop`
```
ID               PR-06
DISPOSITION      untouched            PILLAR/ROLE  Directional · experiment   STATUS  DRAFT
HYPOTHESIS       A VIX-drop-gated long call debit spread, ridden to settlement with SL50 and no
                 PT, has positive RoR out-of-sample. Backtest +21.9% RoR, IS +24.8% / OOS
                 +19.1%, positive every year 2021–26. The regime COMPLEMENT to the put bot.
MECHANISM        Directional convexity in low-vol melt-ups; defined risk (the debit). Primitive:
                 VIX Change% gate; SL50 only, no PT, 100%-bid-ask exits, no Market pricing.
KILL CRITERION   Exp(R) per position < −0.10 with CI below 0 at n≥50. Plus the same liveness kill.
SAMPLE TARGET    n = 50 positions.
REVIEW DATE      Day-0 + 6 months.
MAX LOSS         1 lot, ≈$700/position.
SIZING TIER      1 lot. ⚠️ Allocation is set to $50k vs the put pair's $10k — harmless for a
                 1-ct bot, but ALIGN IT before signing if cross-bot comparability is wanted.
CONFIG HASH      <capture> @ <hash>
VERIFICATION     Trades list shows an SL row and NO PT row. Confirm AUTOMATIONS is ON — it was
                 OFF at creation.
SIGNED           ..............................
```

### The seven live mirrors — one shared frame, seven entries

One frame, seven separate entries — **one ID per bot**, so each is tagged and signed on its own:

| ID | Bot |
|---|---|
| **PR-07** | `3DTE $140-$350` |
| **PR-08** | `Nigiri-Paper-v1` |
| **PR-09** | `QQQ long call` |
| **PR-10** | `Friday 14 DTE Broken Wing IB (B-70)` |
| **PR-11** | `Trendy-Paper-v1` |
| **PR-12** | `60min-ORB-10W-Paper-v1` |
| **PR-13** | `Tasty Condor` |

```
ID               PR-07 … PR-13    one per bot, per the table above
DISPOSITION      untouched            PILLAR/ROLE  OA-Mirror · mirror-watch   STATUS  DRAFT
HYPOTHESIS       <per bot> This mirrored strategy reproduces its source's claimed edge closely
                 enough to justify funding. Watch-only — never refactored.
MECHANISM        <per bot — inherited from the source strategy, stated in one sentence>
KILL CRITERION   Funding bar, all must hold (oa-mirror-reference §2.6):
                   · ≥20 completed post-cutover positions
                   · positive P/L AND instance-profitable
                   · win rate within ~10% of the source's claim
                   · max single-trade loss ≤20% of intended live allocation
                   · no single loss >1.5× the source's largest disclosed loss
                 Failing any of these after 20 positions = defund, switch OFF.
SAMPLE TARGET    n = 20 positions for the funding decision; n = 100 for an edge claim.
REVIEW DATE      Day-0 + 3 months (funding), Day-0 + 6 months (edge).
MAX LOSS         <per bot — current allocation>
SIZING TIER      unchanged from current. Do not resize a watch-only bot.
CONFIG HASH      <capture> @ <hash>
VERIFICATION     Both toggles ON and screenshotted. These are 7 of the 9 bots in the Day-0
                 re-arm sweep.
SIGNED           ..............................
```
> ⚠️ **Funding is judged on the PRE-LAPSE lifetime record, from `data/mirror_baseline.csv`** —
> a one-time frozen snapshot, nine rows, written once, **built from the capture export and NOT
> from the archived `trades.csv`** (the ledger is missing 6 mirror positions worth +$632). This
> is the ONLY place pre-cutover numbers enter a decision. `build-plan.md` §3.
>
> ⚠️ **`QQQ long call` carries ~$13K risk at ~−$10.8K unrealized on 4 open positions**, and
> `Tasty Condor` one at ~+$328. Day-0 Step 2 is an explicit, logged **ride-or-close** call on
> all five. **That decision goes in this ledger too** — it is exactly the quiet exposure that
> survives a clean-slate rebuild and then surprises someone.

---

## 6. Group D — the 5–7 fresh builds

> ⚠️ **Names and the exact arm count are Andy's at build time.** `build-plan.md` §2D specifies
> "4–6 bots" for the greenfield IC family plus rebuilt hedge arms plus an optional canary; it
> does not name them. The entries below are drafted against the *roles* the plan defines. **Do
> not treat these names as decided.**

### Greenfield IC family — 4 matched arms (names TBD)
```
ID               PR-14 … PR-17    one per arm, in creation order, as drafted at four arms.
                                  ⚠️ build-plan.md §2D allows 4–6; if the count changes, the
                                  hedge block below shifts with it. Stamp literals at build time.
DISPOSITION      fresh build          PILLAR/ROLE  IC · experiment      STATUS  DRAFT
HYPOTHESIS       Across four arms differing in EXACTLY ONE input value — the exit policy —
                 at least one has positive Exp(R) per condor, and the ranking between them is
                 readable. Arms: hard-PT · trailing · ride · <fourth, Andy's call>.
MECHANISM        Short-premium VRP on 0DTE. The arms share every other input, so any Exp(R)
                 difference is attributable to exit policy alone. Primitives: a NAMED Exit
                 Option Preset in the Open Position action (the Exit-Options SET as a Bot Input · Touch on the
                 challenged side · time exit) + a flat-close Scheduled Event backstop + a
                 position-closed-trigger automation to close the sibling spread.
                 📝 SIZING STAMP 2026-08-06: primitive observed FIRST-HAND as the FIXED
                 CONTRACT COUNT (1), not the `Up to $250 risk` fallback (spec §5.4/C4) —
                 `GF-ScannerA-PutSpread`, Phase A build, `amount:{"type":"quantity",
                 "quantity":1}`. Applies to all seven greenfield-family arms, PR-14…PR-20
                 (`greenfield-family-spec.md` C4, memory row).
KILL CRITERION   Per arm: Exp(R) per condor < 0 with CI entirely below 0 at n≥60.
                 FAMILY-LEVEL (REPLACED 2026-08-05 — see the banner below this entry):
                 if a capture-diff ever shows two arms differing in MORE THAN ONE MECHANIC
                 (a trigger field and, if present, its own pricing sub-field), or if any of
                 greenfield-family-spec.md §8.3's A1, A2, A3, A7 or A8 fires, the family's
                 ranking is VOID and all arms are re-based — the comparison, not the bots,
                 is what dies.
SAMPLE TARGET    n = 100 positions per arm, on matched days.
REVIEW DATE      Day-0 + 6 months, interim at n=60.
MAX LOSS         1 lot per arm until one clears its interim read; then ≈$5K risk/position.
SIZING TIER      1 lot — experiment. IDENTICAL across all arms.
CONFIG HASH      <capture> @ <hash> — one per arm
VERIFICATION     A CAPTURE-DIFF showing exactly ONE differing line between any two arms. Not a
                 claim, a diff. Plus each arm's first-position Trades list.
SIGNED           ..............................
```
> ### 📝 D-1 RULED 2026-08-04 — the arm variable is the WHOLE Exit-Options bundle, not PT%.
> *Applied 2026-08-05 on Andy's explicit release, from `docs/decision-memo-2026-08-04.md`'s draft
> amendment (a). The `MECHANISM` substring above was changed from `PT% as a Bot Input` to
> `the Exit-Options SET as a Bot Input`; nothing else in the entry moved. **This entry is still
> DRAFT and unsigned.***
>
> **D-1 → Option A: Exit-Options-SET as a Bot Input.** Per-field 🔗 does not exist — **[FIRST-HAND
> 2026-08-04, Exit Options editor on `QQQ-IC-0DTE-Fortress Clone`]**: the 🔗 on the Exit Options
> row opens `Add Input / Exit Options`, and inside the Default Value editor `i.fa-link` count is
> **0**. The linkable unit is the whole bundle (`oa-platform-reference.md` §9 row 3).
> The FAMILY-LEVEL kill criterion below reads "one differing input" at **BUNDLE** granularity;
> **the capture-diff must therefore decode the exits payload, not compare rendered labels.**
>
> ⛔ **THE G2 RIDER, and it is the one that bites.** The saved action stores a **REFERENCE, not
> values** — `{"type":"input","input":"IN…","text":"<label>","oldValue":{…}}`. **A capture that
> reads only the action records the input's NAME, so every arm diffs as identical.**
> `bots_config_v2.csv`, the capture-diff and the drift detector must **also read the input
> object's value**. ⚠️ **`oldValue` is a trap** — a pre-link snapshot that goes stale; never read
> it as current config.
>
> **Gate status at application:** G1 **YES** (an empty bundle saves and survives a hard reload, so
> the `ride` arm IS expressible — the memo's G1 fallback is not needed) · G3 **compatible** (a
> bundle input and a named Preset compose on the same action) · G4 **no propagation** (the `exits`
> payload stores no preset reference). ⛔ **Still blocking before this entry is signed:
> greenfield check C0a — the BOT-INPUT tier has never been observed.** G1/G2/G3 and §9 row 3 all
> exercised the *Automation* Input; `oa-platform-reference.md` §5.2's `[DOCS-SILENT]` tag on the
> Bot-Input tier stands. **If C0a fails, Architecture E is not buildable and this entry returns to
> Andy — do NOT fall back to per-arm copies** (`greenfield-family-spec.md` §10 Phase 0).

> ### ⛔ FAMILY-LEVEL KILL CRITERION REPLACED 2026-08-05 — the original was vacuously unfireable
> **Original wording:** *"FAMILY-LEVEL: if a capture-diff ever shows more than one differing input
> between two arms, the family's ranking is VOID and all arms are re-based — the comparison, not
> the bots, is what dies."*
>
> **Why it could never fire.** Under **D-1 Option A** each arm holds **exactly one** exit input, so
> *"more than one differing input"* is a state the family cannot reach. This is the identical defect
> `docs/decision-memo-2026-08-04.md` used to **reject** Options B and C (*"with no inputs it can
> never fire"*) — it survived in the criterion that was supposed to catch it, and two independent
> reviewers found it separately (`greenfield-family-spec.md` §11-CF2, §9).
>
> **The replacement is `greenfield-family-spec.md` §9's comparative form, at FIELD granularity** —
> "more than one **mechanic**" (a trigger field plus, if present, its own pricing sub-field), plus
> the §8.3 assert rules A1/A2/A3/A7/A8. It is fireable because arms genuinely can differ in two
> mechanics, and the §8.3 asserts are machine-checkable against `bots_config_v2.csv`.
>
> ⚠️ **STATUS: DRAFT — UNSIGNED**, exactly as before. This edit changes the *text* of an unsigned
> draft entry; it signs nothing and authorizes no build. Signing remains Andy's at Day-0 per §7,
> and §7 item 3's gate still applies: **does the loop actually produce the number this criterion
> needs?** Authorized by Andy 2026-08-05 (row S-5).

> ⛔ **This is where the v1 tournament died.** Three arms turned out to be one arm
> (`HedgeA-S1` ≈ `HedgeD` ≈ `HedgeTest`, 70–73 identical positions), and one ran in a different
> execution class. The capture-diff requirement is not bureaucracy — a single diff would have
> caught it on day one. `hedge-research.md` §5.2 and §6.
>
> ~~⚠️ **Two spec dependencies are unverified and must be resolved before signing:** whether Exit
> Options can reference a Bot Input at all (the "PT% as a Bot Input" design), and whether one
> Preset can be referenced from both the call-side and put-side Open actions.
> `oa-platform-reference.md` §9 items 3 and 4.~~
>
> > **✅ BOTH ANSWERED 2026-08-04; struck 2026-08-05. One replacement dependency, and it is
> > sharper.** **[FIRST-HAND 2026-08-04, live UI on `QQQ-IC-0DTE-Fortress Clone`.]**
> > **#3 — YES, but the input's TYPE is the whole Exit-Options bundle**: `i.fa-link` count is
> > **0** inside the Default Value editor, so *"PT% as a Bot Input"* is **not expressible** and
> > the design is D-1 Option A, **Exit-Options-SET as a Bot Input** (see the D-1 banner above).
> > **#4 — YES, one preset serves BOTH Open Position actions, across two automations**; presets
> > are **account-scoped** (`UI…` id namespace), so the cross-automation `[DOCS-SILENT]` is
> > closed. Preset naming is confirmed too — `input[name="pretext"]`, hidden until `defs` is
> > ticked.
> > ⛔ **REPLACEMENT DEPENDENCY, still unverified and still blocking this signature: greenfield
> > check C0a — the BOT-INPUT tier has never been observed.** Everything above tested the
> > **Automation** Input. `oa-platform-reference.md` §5.2's `[DOCS-SILENT]` tag on the Bot-Input
> > tier is deliberately unstruck. **C0a can stop Architecture E outright.**

### Rebuilt hedge tournament arms (count TBD)
```
ID               PR-18 onward     one per arm, in creation order. Count is TBD, so the literals
                                  are assigned at build time — not now.
DISPOSITION      fresh build          PILLAR/ROLE  IC · experiment      STATUS  DRAFT
HYPOTHESIS       With matched arms in a single execution class, the hedge tournament can rank
                 mechanics. The v1 tournament could not, and this is the rebuild that makes the
                 question askable again — not an answer to it.
MECHANISM        Per arm, one hedge mechanic from the library. Shared automation, shared inputs,
                 Range075 carried as a preset on every arm.
                 📝 SIZING STAMP 2026-08-06: primitive observed FIRST-HAND as the FIXED
                 CONTRACT COUNT (1), not the `Up to $250 risk` fallback (spec §5.4/C4) —
                 `GF-ScannerA-PutSpread`, Phase A build, `amount:{"type":"quantity",
                 "quantity":1}`. Applies to all seven greenfield-family arms, PR-14…PR-20
                 (`greenfield-family-spec.md` C4, memory row).
KILL CRITERION   The tournament is VOID (not the bots) if any of hedge-research.md §5.2's five
                 conditions fails: shared automation · one differing input proven by
                 capture-diff · same execution class · Range075 on every arm · a proof-of-fire
                 artifact identified in advance. Per arm: Exp(R) < 0, CI below 0, n≥60.
SAMPLE TARGET    n = 100 positions per arm.
REVIEW DATE      Day-0 + 6 months.
MAX LOSS         1 lot per arm.
SIZING TIER      1 lot — IDENTICAL across arms.
CONFIG HASH      <capture> @ <hash> per arm
VERIFICATION     Capture-diff, one differing input. No ranking published until it passes.
SIGNED           ..............................
```
> ⚠️ **Do not include a `Conditional` / sustained-touch arm.** OA cannot express time
> persistence; the only build path is a 10-rung tag ladder that consumes the scan budget and
> fails safe-looking at every rung. `hedge-research.md` §7.1 recommends against it. Building it
> anyway is a roster decision and is Andy's.

### Optional 1-lot canary
```
ID               <next free ID after the hedge arms are stamped>
DISPOSITION      fresh build          PILLAR/ROLE  IC · control          STATUS  DRAFT
HYPOTHESIS       Not a strategy hypothesis — an INSTRUMENT hypothesis: a bot whose PT should
                 fill every single day will stop filling the day the exit engine dies, giving
                 same-day detection of the failure that ran six invisible sessions in v1.
MECHANISM        n/a — this bot is not run for edge. Its P/L is expected to be ~flat and is not
                 evidence about anything.
                 📝 SIZING STAMP 2026-08-06: primitive observed FIRST-HAND as the FIXED
                 CONTRACT COUNT (1), not the `Up to $250 risk` fallback (spec §5.4/C4) —
                 `GF-ScannerA-PutSpread`, Phase A build, `amount:{"type":"quantity",
                 "quantity":1}`. Applies to all seven greenfield-family arms, PR-14…PR-20
                 (`greenfield-family-spec.md` C4, memory row).
KILL CRITERION   None on P/L — it is exempt by design, and that exemption is stated here so it
                 cannot later be mistaken for a losing bot nobody killed. It is retired when the
                 detector's Tier C rules cover the same ground with a live config.
SAMPLE TARGET    n/a — daily fill/no-fill is the output.
REVIEW DATE      Day-0 + 3 months: is it still earning its slot?
MAX LOSS         1 lot, smallest expressible risk.
SIZING TIER      1 lot.
CONFIG HASH      <capture> @ <hash>
VERIFICATION     A PT fill on day 1, read from the Trades list.
SIGNED           ..............................
```

---

## 7. Signing checklist — Day-0

For each of the ~~≈18–20~~ **≈18–20 plan bots and every Track B arm — up to 28 in total**
(scoped 2026-08-05; `build-plan.md` §2D's `🔓 SCOPING AMENDMENT 2026-08-05`, §3 above), in this
order:

1. **Config hash filled** from the bot's own capture file. Not from memory, not from
   `bots_config.csv`.
2. **Every `<placeholder>` and `TBD` resolved.** An entry with an unfilled field is unsigned.
3. **Kill criterion re-read against the daily loop** — does the loop actually produce that
   number? If not, fix one of the two now.
4. **Max-loss line filled.** The `<FILL>` blanks in `rules-of-engagement.md` are an open audit
   gate H3 failure; do not add more.
5. **Andy signs and dates.** Only then may the bot be switched ON.
6. **Verification artifact read** before it may take a position — the Trades list, per
   `oa-platform-reference.md` §8.3. Signed ≠ verified.

**Enforcement, proposed and not yet built:** mirror the template VERSION into a `BUILD_ID` bot
input so the running bot self-reports which pre-registration it is executing, and have the
nightly script assert `BUILD_ID` == the version named here, failing loudly on mismatch.
⚠️ **If that assert is not built, do not build the `BUILD_ID` mechanism** — a self-report nobody
checks is worse than none.

---

## 8. Open items

1. **Fresh-build names and arm counts** (§6) — Andy's, at build time. **This also blocks their
   `ID` literals:** PR-01…PR-13 are stamped and final; §6's IDs are ranges until the greenfield
   arm count (4 or 6) and the hedge arm count are decided, which is why the canary has no literal
   yet. Scheme decided 2026-08-03: `PR-NN`, two digits, ledger entry order, OA Tag = the bare ID.
2. **The 15:52 backstop timestamp** — unverified, gates two clone specs
   (`oa-platform-reference.md` §8.2).
3. **Exit Options ← Bot Input, and Preset cross-automation scope** — both unverified, and the
   greenfield spec depends on them (§9 items 3–4 of the platform reference).
4. **`CallVIXdrop` allocation** is $50k vs the put pair's $10k. Harmless at 1 lot; align before
   signing if comparability matters.
5. **The ride-or-close decision on the five open mirror positions** belongs in this ledger and
   is not yet drafted — it depends on where they stand at Day-0.
6. **Per-bot max-loss lines** are drafted from the sizing law, not measured. Revisit once
   `mirror_baseline.csv` exists.
