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
> active bots~~ ~~**≈18–20 plan bots plus up to 8 pre-registered Track B arms — ceiling 28**~~
> **≈18–20 plan bots plus up to 8 pre-registered Track B arms plus up to 2 Lab ops bots — ceiling
> 30** — **including the nine untouched ones**, every Track B arm, and every Lab ops bot.
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
> >
> > > **🔓 AMENDED 2026-08-07 — `build-plan.md` §2D's `🔓 AMENDMENT 2026-08-07` (E-1).** A third,
> > > separate allocation — **`≤2 Lab ops bots`, ceiling 28 → 30** — citing
> > > `exploratory-bots-design-2026-08-07.md` §3.1 SLOT A. Wave 1 becomes **24 of 50**; full spend
> > > **30 of 50**. Class and entries: §2a/§6a (added same date, E-2). ⛔ Still scopes a count
> > > only; still no entry, no restart, for Lab ops bots too — and E-3's hard precondition (§2a)
> > > gates any Lab bot's `AUTOMATIONS` regardless of signing.

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
GATE EVAL DATE   📝 FIELD ADDED 2026-08-06 (G-7, STAMP, ruled by Andy). The single date (or
                 n) at which the comparative gate evaluates, once — required before n reaches
                 100 (research-loop-spec.md §10a item 2). Relative to Day-0, resolves to a
                 calendar date at Day-0. Distinct from REVIEW DATE. Previously absent from this
                 template (track-b-arms-spec.md §11 item 5, open since 2026-08-04).
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

## 2a. Ops-class entries

> ### 🔓 ADDED 2026-08-07 — "amend the plan", Andy's explicit words (E-2)
> Andy signed **E-2** 2026-08-07 (~14:40 ET), together with E-1 and E-3. This section is added
> **exactly per** `exploratory-bots-design-2026-08-07.md` §3.2 SLOT B's drafted text, proposed for
> "a named class that follows PR-20's pattern exactly" — write `n/a`, state the exemption in the
> entry, state its retirement condition, never drop the entry. Nothing existing in this document
> is changed by this section; it is additive.

An **ops-class** bot is one run to observe the *platform*, never to estimate a *return*. It uses
the §2 template unchanged, with three fields declared `n/a` and a fourth added:

- **`HYPOTHESIS`** — an **INSTRUMENT** hypothesis, in PR-20's sense: what the bot will let us
  observe that no other bot can. **Never a market hypothesis.**
- **`MECHANISM`** — `n/a — not run for edge.` ⚠️ And, unlike PR-20, **P/L is not expected to be
  flat**: e.g. a `dstop`-instrument bot loses money by design. State that in the entry so it
  cannot later be mistaken for a losing bot nobody killed.
- **`SAMPLE TARGET`** — `n/a — the daily observation is the output.`
- **`KILL CRITERION`** — none on P/L, by design and stated. Killed instead on **instrument
  failure**: no usable observation for K consecutive sessions where the cause is the bot rather
  than the platform. Plus a hard `RETIREMENT DATE`.
- **`PHASE LOG`** **(new field, ops-class only)** — every configuration change, dated, with the
  phase ID and the unknown it targets. **This field is the class's whole justification for being
  mutable**, and its absence is the `HedgeD` failure: an undocumented substitution at a platform
  limit, where *"the config record and the tree agreed with each other and both were wrong about
  the intent."*

**Guardrails G1–G10 — the conditions on the class.**

| | Guardrail |
|---|---|
| **G1** | ⛔ **Publication interdict.** No number from an ops-class bot may enter any Exp(R), any arm or variant comparison, any funding decision, any tiered T1–T5 claim, or any brief section other than the ops/mechanics section. |
| **G2** | **G1 is enforced in code, not by intent** — the `build_ledger.py` ledger exclusion (`exploratory-bots-design-2026-08-07.md` §3.3; implementation queued, `CLAUDE.md` §5, E-3). A rule with no mechanism is the failure class this project keeps re-learning. |
| **G3** | ⛔ **Never an arm, never a control.** Ops bots enter no tournament, are matched to nothing, and are deliberately non-matched to each other. `DUPLICATE_ARM` must not scope them, and no A-series assert may read them (§3.3). |
| **G4** | ⛔ **No shared Library object, ever.** Every ops automation is a per-bot copy. `oa-platform-reference.md` **OA-0682**: an edit *"will flow through anywhere the automation is used."* |
| **G5** | **Paper only.** Promotion to live requires a separate ruling (`exploratory-bots-design-2026-08-07.md` §3.4). |
| **G6** | **Sizing declared once per phase**, with the reason in writing — not by preference. |
| **G7** | ⛔ **Account-wide probes are separately gated.** `maxexits`, the ITM actions, the Bot Schedule and notification settings are account-wide; any phase touching them does not run without its own ruling. |
| **G8** | **Every phase is declared and dated in `PHASE LOG` BEFORE it starts.** An undeclared configuration change voids that phase's observations. |
| **G9** | **Deliberate-failure phases** (`EXIT OPTIONS` OFF; induced errors) require a named window, a named expected signature, and a restore step in the same declaration. |
| **G10** | ⛔ **Retirement is the default.** Each unknown is struck from the bot's phase list once answered; when the phase list empties, the bot is archived and its slot returns. An ops bot with no open phase is not earning its slot. |

⛔ **E-3 hard precondition** (`exploratory-bots-design-2026-08-07.md` §3.3, ruled 2026-08-07): no
Lab bot's `AUTOMATIONS` may go ON until the `build_ledger.py` exclusion, the `a_series` scoping
(`_a4b`/`_a6`), and the Lab group/tag fencing are **all implemented and verified**. Implementation
is a queued Claude Code task; nothing above authorizes it to be built.

---

## 3. The roster — ≈18–20 plan bots, plus ≤8 Track B arms, plus ≤2 Lab ops slots. Ceiling 30.

~~Per `build-plan.md` §2, under decision freeze: **4 clones + 9 untouched + 5–7 fresh.**~~
Per `build-plan.md` §2 as amended 2026-08-05: **4 clones + 9 untouched + 5–7 fresh
= ≈18–20 plan bots**, **plus ≤8 pre-registered Track B arms** as a separate allocation, **plus ≤2
Lab ops slots** as a third, separate allocation (🔓 amended 2026-08-07, banner below).

| Group | Count | Entries below |
|---|--:|---|
| **B — clone-to-spec** (original archived) | 4 | §4 |
| **C — untouched** (validated, lived through the lapse) | 9 | §5 |
| **D — fresh builds** | 5–8 | §6 |
| **plan-bot subtotal** | **≈19–21** | |
| **Track B arms** (separate allocation, `research-loop-spec.md` §10) | **≤8** | `track-b-arms-spec.md` §9 — PR-21 / PR-22 proposed, wave-1 spend **2** |
| **E — Lab ops bots** (non-inferential; separate allocation, `exploratory-bots-design-2026-08-07.md` §3.1) | **≤2** | §6a |
| **ceiling** | **30** | |

> ### 🔓 AMENDED 2026-08-07 — "amend the plan", Andy's explicit words (E-1, propagated here)
> **The `ceiling` row previously read `28`; no `E — Lab ops bots` row existed.** `build-plan.md`
> §2D now carries a `🔓 AMENDMENT 2026-08-07` block adding a third, separate allocation —
> **`OPS/Lab ≤2 bots`, ceiling 28 → 30** — citing `exploratory-bots-design-2026-08-07.md` §3.1
> SLOT A. Wave 1 becomes **24 of 50**; full spend **30 of 50**. The Lab-ops entries themselves are
> §2a/§6a (added same date, E-2). ⛔ **This scopes a count and authorizes no build** — every Lab
> bot needs its own signed entry here before it may be switched on, **and** E-3's hard
> precondition (§2a) must clear first.

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
CONFIG HASH      FILLED AT DAY-0 SIGNING 2026-08-09 (same convention as the greenfield arms,
                 per Andy's ruling in-chat: capture path @ file sha256, plus the recorded
                 per-automation hashes).
                 CAPTURE  data/captures/2026-08-07-s0b/IC-SPX-FastPT25-S2-post-FC1-2026-08-07.txt
                 SHA256   ee39ef7f1abde0402daac70cd08aac732c4cd0eb8c78e4b6453d689ed145f656
                 PER-AUTOMATION HASHES (from data/bots_config_v2.csv, post-F-C1):
                   Scalp-Scan-Put           f83ed32bb24c0bc20e703164d68d309e1423d5be9069cc577fafb434aaf1c52f  (v4)
                   Scalp-Scan-Call          892ba0c9fb7dfbfa038d95eec9ed953a91e25acc12a44f7c0aee1c960755bfa7  (v5)
                   Scalp-Mon-S2-StrikeTouch  01af4963aafb58566789662aafa68d94d846d042869590eccbede9fb6d57ca85  (v4, unchanged)
                   Scalp-Mon-S2-Cleanup     f3673f2991541420c7124f3a6d2e2a2996002f6c61dc61ac8389ea348db2ccd7  (v2, unchanged)
                 This bot's hash IS established — it has a pre-restore baseline and its archived
                 original is byte-identical to its own step-0 baseline. A-27c's NOT-EVALUABLE
                 carry does NOT apply here.
VERIFICATION     INVERTED — the first new position's Trades list must contain NO PT row and NO
                 exit-trigger row, and the S2 monitor must be observed firing. Both toggles
                 screenshotted. Exit Options panel is not evidence.
SIGNED           2026-08-09 · ANDY — gate A7, in-chat at the S2 Day-0 sitting. Ruling recorded
                 verbatim: "Fill its CONFIG HASH and sign it".
                 SIGNED != VERIFIED. The INVERTED Step-6 check is deferred to the first trading
                 session (2026-08-10) — the market was closed on the day this was signed — and
                 it stays ADVISORY until D4 is answered (whether the account-level ITM action
                 appears in a Trades list, and under what label, is UNOBSERVED; a mislabelled
                 ITM close reads as a PT row and would kill a ride control on day one). READ
                 THE LABEL FIRST, FIRE THE RULE SECOND.
                 FLAGGED at signing, not a blocker: PR-02, this entry's 13:00 A/B partner, has
                 no Template V1 and therefore cannot trade, so the 11:00-vs-13:00 comparison
                 starts with one arm. PR-01 stands alone as the RIDE BENCHMARK and is
                 unaffected; the cost falls on PR-02's matched-day count.
                 CONFIG NOTE: limits are 10/10 on this bot. Per decision-card-2026-08-08 slot 2,
                 posLimitDay/posLimit are set to 1 for the first-position read and REVERTED
                 immediately after, with the revert HASH-PROVEN.
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
CONFIG HASH      FILLED AT S2b SIGNING 2026-08-09, same convention as PR-01 and the greenfield
                 arms (Andy's ruling 4 at the S2 sitting: capture path @ file sha256, plus the
                 recorded per-automation hashes).
                 CAPTURE  data/captures/2026-08-08-clones/PR-02-clone-final-2026-08-08.txt
                 SHA256   d542587ffa4b012fd63e0b2ef50d6aa8d900fec477c2718102cae7c1f9d06162
                 PER-AUTOMATION HASHES (from data/bots_config_v2.csv, post-F-C1 + post-5b):
                   Scalp-Scan-Put            41f2505a0f5119f3ed7b4d712f881afa68d104a43f13bbb15600989124238d87  (v6, 4796B)
                   Scalp-Scan-Call           144b45e69c40289714752715a3986d1c1b6e7ab8190797f67081c120e7ccad3d  (v7, 4813B)
                   Scalp-Mon-S2-StrikeTouch  01af4963aafb58566789662aafa68d94d846d042869590eccbede9fb6d57ca85  (v4, 4584B, byte-identical to PR-01's)
                   Scalp-Mon-S2-Cleanup      f3673f2991541420c7124f3a6d2e2a2996002f6c61dc61ac8389ea348db2ccd7  (v2, 2610B, byte-identical to PR-01's)
                 TEMPLATE V1  Tfw5TkkCRF1717862960217463041 ("Template V1 - pre-reg PR-02 -
                 saved 2026-08-09"), by Andy's hand 2026-08-09. The clone's own `tid` resolves
                 to it, so the link is proven BOT-SIDE, not only in the templates list.
                 This bot's hash IS established (a pre-restore baseline exists) - A-27c's
                 NOT-EVALUABLE carry does not apply here.
VERIFICATION     INVERTED, as above. PLUS: the first five entries' timestamps land in the
                 declared window. The 11:00 gate on the v1 bot was never implemented and ran
                 20+ sessions before anyone noticed.
SIGNED           2026-08-09 - ANDY - gate cleared at S2b, in-chat. Runbook Step 4's
                 precondition (Template V1) is MET as of this sitting; PR02-R1 (allocation
                 $50,000 STANDS) was ruled 2026-08-08 and is DISCHARGED, and it was the only
                 other block on this entry.
                 SIGNED != VERIFIED. The INVERTED Step-6 check (NO PT row, NO exit-trigger row,
                 and the S2 monitor observed firing) is DEFERRED to the first trading session,
                 2026-08-10 - the market was closed on the day this was signed - and it stays
                 ADVISORY until D4 is answered, exactly as on PR-01. READ THE LABEL FIRST,
                 FIRE THE RULE SECOND.
                 FIRST-TRADING-DAY CAPTURE OWED 2026-08-10.
                 CONFIG NOTE: limits read 10/10 at signing and were set to 2/2 in the same
                 sitting on Andy's in-chat ruling - "2 per day / 2 at once", condor-aware: an IC
                 is TWO positions, so 2/2 IS one condor per day, one at a time. Per slot-2
                 ruling 2a a position-limit edit does NOT fork this signature. Allocation
                 untouched at $50,000.
                 EXIT OPTIONS stays OFF by design - this is the -130PM Exit-Option-free control
                 (oa-ops-runbook.md 4.3, build-plan.md 4). Do not "fix" it.
                 A/B NOTE: PR-01, this entry's 11:00 partner, went ON at S2b the same sitting,
                 so the 11:00-vs-13:00 comparison starts with BOTH arms live - the one-armed
                 start flagged in PR-01's signature on 2026-08-09 no longer applies.
                 RIDER DISCHARGED BY SUBSTITUTE 2026-08-18 per R-2026-08-18-PR02-DISCHARGE-PR04-REANCHOR; capture data/captures/2026-08-18-pr02pr04/01-PR-02-closed-positions-2026-08-18-042142.txt sha256 61c9fdae944b6569f5d7126f02973f21a47001e07fbe625cf1b7900fedae17d5; evidence 2026-08-10..2026-08-17 remains SIGNED != VERIFIED.
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
CONFIG HASH      FILLED AT S2b SIGNING 2026-08-09, same convention as PR-01 and the greenfield
                 arms (Andy's ruling 4 at the S2 sitting: capture path @ file sha256, plus the
                 recorded per-automation hashes).
                 CAPTURE  data/captures/2026-08-08-clones/PR-04-clone-final-2026-08-08.txt
                 SHA256   e58db65fff3f0c69141eeb80a0db01791bfdf6b4dfbe8045d08493e06667bdc0
                 PER-AUTOMATION HASHES (from data/bots_config_v2.csv). PR04-R1 governs the
                 count: this family has TWO scanners plus the built backstop, so THREE is the
                 COMPLETE set, not a partial capture.
                   FortNoPT-Scan-Put                 2eab2d95541b44536c452fcb4b7acd005ae45dd712ce07675d4d66d95db211e2  (v9, 4682B, UNEDITED)
                   FortNoPT-Scan-Call                7dd2df800d47d4c4f4ba97cfd5fc83d588fcc4c20d9fd12ef9928b4e607bc6be  (v9, 4649B, UNEDITED)
                   FortNoPT-Backstop-1552-FlatClose  6794b56b672e7e625ee731ac949ddeffddf5e325522b38a8f73d6d0cb34f7e04  (v1, 1447B, BUILT 2026-08-08)
                 TEMPLATE V1  Tfw5TkkCRF1717862960769161432 ("Template V1 - pre-reg PR-04 -
                 saved 2026-08-09"), by Andy's hand 2026-08-09. The clone's own `tid` resolves
                 to it, so the link is proven BOT-SIDE, not only in the templates list.
VERIFICATION     Trades list contains a time-exit row and NO PT row. Same backstop check.
SIGNED           2026-08-09 - ANDY - gate cleared at S2b, in-chat. Runbook Step 4's
                 precondition (Template V1) is MET as of this sitting, and it was this entry's
                 only block: there is no allocation gate here, unlike PR02-R1 - both readings
                 agree at $100,000.
                 SIGNED != VERIFIED. Step 6 (the Trades list carries a TIME-EXIT row and NO PT
                 row, plus BACKSTOP_CAUGHT_IT NEGATIVE) is DEFERRED to 2026-08-10.
                 FIRST-TRADING-DAY CAPTURE OWED 2026-08-10.
                 CONFIG NOTE: limits read 2/2 at signing - ALREADY the value Andy ruled for this
                 bot in-chat at S2b ("2 per day / 2 at once", condor-aware). NO EDIT WAS MADE,
                 so nothing forked and there is nothing to revert. Allocation $100,000 untouched.
                 CARRIED, NOT BLOCKING: PR04-R3 / S2-R4 - `rdata.next` = 1786369500000 (09:45 ET
                 Monday) against a rendered "Every week on Mon-Fri, 3:52pm EST". It reproduces to
                 the millisecond on `GF-QQQ-IC-Ride`, a different bot with a different backstop
                 object, which is consistent with a bot-level next-scan stamp - but that is an
                 INFERENCE and it discharges nothing. Not re-timed. Monday's first 15:52 fire
                 disambiguates it.
                 SIGNED WITH AN OPEN GATE NAMED: finding S2b-R3 - this bot's EXIT OPTIONS read
                 OFF (`disableExits` 1) at signing, while the VERIFICATION line above requires a
                 TIME-EXIT row and a NEGATIVE BACKSTOP_CAUGHT_IT. With Exit Options off the
                 inherited 15:50 exit cannot fire and the 15:52 backstop becomes the closing
                 mechanism by construction. THIS SIGNATURE DOES NOT AUTHORIZE SWITCH-ON. The bot
                 stays OFF until that finding is ruled. See the S2b session-log entry.
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
GATE EVAL DATE   📝 STAMPED 2026-08-07 (item 7 above; Andy's ruling: stamp both). Day-0 + 6
                 months (relational; resolves to calendar at Day-0) — matches REVIEW DATE. This
                 is a standalone R kill (Exp(R) < −0.10, CI below 0, n≥50), not a comparative
                 gate under research-loop-spec.md §10a — no interim look at n=60 applies.
MAX LOSS         1 lot, ≈$500/position (the debit).
SIZING TIER      1 lot — experiment.
CONFIG HASH      <capture> @ <hash>
                 ⛔ A-27c RULING 2026-08-08 (decision-card-2026-08-08 slot 6, OPTION 2):
                 ⬜ NOT EVALUABLE — no pre-restore baseline exists for this bot, so A-07's
                 ESTABLISHED-hash precondition does NOT apply and does NOT block this signature.
                 A capture is taken ON THE FIRST DAY THIS BOT TRADES; forward drift detection
                 starts from that capture. ⛔ It establishes nothing about the pre-restore past.
                 Opening this bot for that capture is a PURE READ (6a) and does not spend Step 2c.
VERIFICATION     ⚠️ CANNOT be verified from position data. A correctly-gated bot and a dead bot
                 are indistinguishable. **The bot LOG is the only proof**: a scanner run with no
                 entry = healthy. Both toggles ON and screenshotted.
SIGNED           2026-08-09 · ANDY — in-chat at the S2 Day-0 sitting. Ruling recorded
                 verbatim: "Sign the seven that can trade (ledger reading)". The A-27c
                 carry in the CONFIG HASH field above does NOT block this signature
                 (decision-card-2026-08-08 slot 6, OPTION 2). Signed for Day-0
                 2026-08-10; LEDGER_START = 2026-08-10.
                 SIGNED != VERIFIED — runbook §4 Step 6's order-level Trades-list check is
                 still required before this bot may trade, and rider 2's first-trading-day
                 capture is still owed. [PR-05]
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
GATE EVAL DATE   📝 STAMPED 2026-08-07 (item 7 above; Andy's ruling: stamp both). Day-0 + 6
                 months (relational; resolves to calendar at Day-0) — matches REVIEW DATE. This
                 is a standalone R kill (Exp(R) < −0.10, CI below 0, n≥50), not a comparative
                 gate under research-loop-spec.md §10a — no interim look at n=60 applies.
MAX LOSS         1 lot, ≈$700/position.
SIZING TIER      1 lot. ⚠️ Allocation is set to $50k vs the put pair's $10k — harmless for a
                 1-ct bot, but ALIGN IT before signing if cross-bot comparability is wanted.
CONFIG HASH      <capture> @ <hash>
                 ⛔ A-27c RULING 2026-08-08 (decision-card-2026-08-08 slot 6, OPTION 2):
                 ⬜ NOT EVALUABLE — no pre-restore baseline exists for this bot, so A-07's
                 ESTABLISHED-hash precondition does NOT apply and does NOT block this signature.
                 A capture is taken ON THE FIRST DAY THIS BOT TRADES; forward drift detection
                 starts from that capture. ⛔ It establishes nothing about the pre-restore past.
                 Opening this bot for that capture is a PURE READ (6a) and does not spend Step 2c.
VERIFICATION     Trades list shows an SL row and NO PT row. Confirm AUTOMATIONS is ON — it was
                 OFF at creation.
SIGNED           2026-08-09 · ANDY — in-chat at the S2 Day-0 sitting. Ruling recorded
                 verbatim: "Sign the seven that can trade (ledger reading)". The A-27c
                 carry in the CONFIG HASH field above does NOT block this signature
                 (decision-card-2026-08-08 slot 6, OPTION 2). Signed for Day-0
                 2026-08-10; LEDGER_START = 2026-08-10.
                 SIGNED != VERIFIED — runbook §4 Step 6's order-level Trades-list check is
                 still required before this bot may trade, and rider 2's first-trading-day
                 capture is still owed. [PR-06]
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
> a one-time frozen snapshot, nine rows **[CORRECTED 2026-08-07 — actually TEN rows; item 9 below; `device_bash` read, sha `cdceb0a8d444e570…`]**, written once, **built from the capture export and NOT
> from the archived `trades.csv`** (the ledger is missing 6 mirror positions worth +$632). This
> is the ONLY place pre-cutover numbers enter a decision. `build-plan.md` §3.
>
> ⚠️ **`QQQ long call` carries ~$13K risk at ~−$10.8K unrealized on 4 open positions**, and
> `Tasty Condor` one at ~+$328. Day-0 Step 2 is an explicit, logged **ride-or-close** call on
> all five. **That decision goes in this ledger too** — it is exactly the quiet exposure that
> survives a clean-slate rebuild and then surprises someone.

> ### 📝 EXPANDED 2026-08-07 — the shared frame above is stamped into seven per-bot entries below.
> The frame's `<per bot>` placeholders in `HYPOTHESIS`, `MECHANISM` and `MAX LOSS` are resolved
> here, one entry per bot, so each is tagged and signed on its own — §5's own instruction. **The
> frame is left standing as the shared skeleton**: where an entry below is silent, the frame
> governs. **These are DRAFTS. None is signed. Day-0 is signing, not authoring.**
>
> **Three rules that apply to all seven, stated once here rather than seven times:**
> 1. **NO VERDICT = DO NOT FUND.** For an already-running bot, "insufficient evidence" silently
>    means "keep going" — a capital decision made by default
>    (`mirror-funding-memo-2026-08-05.md` §8 item 4).
> 2. **G-8's SEQUENCE+CS form does not bind any entry below**, because no entry below draws an
>    **n≥60 absolute kill**: the mirror class defunds on the §2.6 funding bar, not on a
>    comparative-arm read, so there is no fixed-n CI here to convert into a confidence sequence.
>    If a mirror ever acquires an n≥60 kill line, G-8 binds it
>    (`g-rulings-card-2026-08-07.md` G-8, ruled by Andy 2026-08-06).
> 3. **The n≥100 edge limb's regime-change conjunct is `evidence-standards.md` §4 gate B3** —
>    ratified by Andy 2026-08-06 as THE definition: *a VIX move of ≥10 points peak-to-trough, or
>    both a sub-15 and an above-25 VIX period.* Until B3 is wired to a `scripts/` detector it is
>    evaluated **manually and each evaluation is logged** (§4's RESOLVED banner, 2026-08-06).
>    These are the **first pre-registration entries to cite B3 by name**, which is the gap that
>    banner records as still open.
>
> ⚠️ **Two tensions carried, not resolved — both are Andy's at signing, both filed in §8:** the
> §2.6 funding bar is stated in **P/L and win rate**, which §2's rule 1 forbids for a kill
> criterion; and **Tier M** (`mirror-funding-memo-2026-08-05.md` §7a) is **DRAFT and NOT IN
> FORCE**, so every `SAMPLE TARGET` below is written against the **n≥100 bar as it stands**.
>
> ⛔ **Every baseline figure quoted below is PRE-LAPSE**, from `data/mirror_baseline.csv` — the
> one-time frozen snapshot that is the ONLY place pre-cutover numbers enter a decision
> (`build-plan.md` §3). It is a **closed-position** anchor: open positions were never in the
> source. None of it is post-cutover evidence, and none of it substitutes for the n≥20 the
> funding bar asks for.

### `3DTE $140-$350`
```
ID               PR-07
DISPOSITION      untouched            PILLAR/ROLE  OA-Mirror · mirror-watch   STATUS  DRAFT
HYPOTHESIS       Not a strategy hypothesis — a FUNDING question: does this mirror reproduce its
                 source's claimed edge closely enough to justify live capital? Watch-only until
                 that is answered; never refactored. Pre-lapse anchor (`mirror_baseline.csv`):
                 n=46, mean R +0.0156, median R +0.0423, sd 0.1545, worst R −1.0000, maxDD
                 1.0000R, win 95.7%. DRAFT verdict today: **WATCH — priority 1, nearest to
                 fundable; fails on SAMPLE alone** (`mirror-funding-memo-2026-08-05.md` §6).
MECHANISM        Short-DTE SPX premium decay, auto-tuned to whatever premium the day offers.
                 Symmetric $10-wide iron condor at 3 DTE; 22-tier waterfall short-strike ladder
                 ($140→$350 in $10 steps, first tier clearing the Return% threshold fires);
                 10:00–10:10am entry window. Profit-take only — 90% decay on 0DTE behind a 1pm
                 gate, 70% after day 1, trade price ≥$0.50; NO stop, removed at v8 by the author
                 (`oa-mirror-reference.md` §5.2). Primitive: one entry scanner + Exit Options
                 profit gates. Mirrored as captured — the mechanism is the SOURCE's, not ours.
KILL CRITERION   The shared funding bar, all five conjuncts (frame above; `oa-mirror-reference.md`
                 §2.6). Failing any after ≥20 completed post-cutover positions = DEFUND, switch
                 OFF. ⚠️ The binding conjunct here is **instance profitability, not win rate**:
                 the source runs 91.3% trade WR against **46.0% instance profitability**, and
                 §2.6 names this bot as the trap that conjunct exists for. Avg loss ≈10× avg win
                 with no stop, so one sustained multi-day breach erases 30+ wins.
SAMPLE TARGET    n = 20 completed post-cutover positions for the funding decision; n = 100 over
                 ≥6 months **including a B3 regime change** for any edge claim. At its observed
                 cadence (0.561 positions/day, memo §7) n=100 arrives ≈3.2 months from a resumed
                 clock — the only mirror that gets there quickly.
REVIEW DATE      Day-0 + 3 months (funding), Day-0 + 6 months (edge).
GATE EVAL DATE   Day-0 + 6 months (relational; resolves to calendar at Day-0); interim look at
                 n=60. ✅ REACHABLE: 0.561/day × ~180 days ≈ 101 positions, so n=60 lands
                 ≈107 days after Day-0, inside the window.
MAX LOSS         Paper allocation **$5K**, deliberately small — one bad position is 20%+ of it.
                 Source avg win / avg loss $173 / −$1,665 (`oa-mirror-reference.md` §5.2); worst
                 realised in the baseline −1.0000R. No stop by construction.
SIZING TIER      Unchanged from current. Do not resize a watch-only bot.
CONFIG HASH      PENDING DAY-0 CAPTURE — the per-bot config capture does not exist yet. Do not
                 fill from `bots_meta.csv`, from the 2026-07-30 export, or from memory.
                 ⛔ A-27c RULING 2026-08-08 (decision-card-2026-08-08 slot 6, OPTION 2):
                 ⬜ NOT EVALUABLE — no pre-restore baseline exists for this bot, so A-07's
                 ESTABLISHED-hash precondition does NOT apply and does NOT block this signature.
                 A capture is taken ON THE FIRST DAY THIS BOT TRADES; forward drift detection
                 starts from that capture. ⛔ It establishes nothing about the pre-restore past.
                 Opening this bot for that capture is a PURE READ (6a) and does not spend Step 2c.
VERIFICATION     Both toggles ON and screenshotted (1 of the 7 mirrors in the Day-0 re-arm
                 sweep), plus the FIRST post-cutover position's **Trades list** read. The Exit
                 Options panel is never evidence (`oa-platform-reference.md` §0.3).
SIGNED           2026-08-09 · ANDY — in-chat at the S2 Day-0 sitting. Ruling recorded
                 verbatim: "Sign the seven that can trade (ledger reading)". The A-27c
                 carry in the CONFIG HASH field above does NOT block this signature
                 (decision-card-2026-08-08 slot 6, OPTION 2). Signed for Day-0
                 2026-08-10; LEDGER_START = 2026-08-10.
                 SIGNED != VERIFIED — runbook §4 Step 6's order-level Trades-list check is
                 still required before this bot may trade, and rider 2's first-trading-day
                 capture is still owed. [PR-07]
```

### `Nigiri-Paper-v1`
```
ID               PR-08
DISPOSITION      untouched            PILLAR/ROLE  OA-Mirror · mirror-watch   STATUS  DRAFT
HYPOTHESIS       FUNDING question, not a strategy one: does this mirror reproduce its source's
                 claimed edge closely enough to justify live capital? Pre-lapse anchor: n=38,
                 mean R +0.0102, median R +0.0102, **sd 0.0065 — the tightest distribution in
                 the fleet**, worst R 0.0000, maxDD 0.0000R, win 94.7%. DRAFT verdict: **WATCH —
                 priority 2** (memo §6).
MECHANISM        Short-premium collection on a 0.05-delta, $5-wide short put spread, one at a
                 time, with day-of-week DTE routing to the nearest Friday (Mon 4 / Tue 3 / Wed 2
                 / Thu 8 / Fri 7 — min 2, max 8 DTE, avoiding 0–1 DTE gamma). Exits: a 7-Day
                 Accelerated Profit monitor (close if return% > 10 × days-in-trade), a 0-Day ITM
                 check at 3pm on expiry day, and a 75% default profit target. **No stop by
                 design** — the author's stop is position sizing and spread width
                 (`oa-mirror-reference.md` §5.2).
KILL CRITERION   The shared funding bar, all five conjuncts (§2.6). Failing any after ≥20
                 completed post-cutover positions = DEFUND, switch OFF. ⚠️ Two things this bar
                 cannot see and a signer must: (a) **the loss tail is UNOBSERVED — zero losing
                 positions in n=38**, so `maxDD 0.0000R` is an absence of evidence, not a risk
                 statement; (b) **the per-position magnitude is tiny** (median +0.0102R), so the
                 edge must be shown to survive real fills before it is ever sized.
SAMPLE TARGET    n = 20 completed post-cutover positions for funding; n = 100 over ≥6 months
                 including a B3 regime change for an edge claim. Observed cadence 0.458/day →
                 n=100 ≈4.4 months from a resumed clock (memo §7).
REVIEW DATE      Day-0 + 3 months (funding), Day-0 + 6 months (edge).
GATE EVAL DATE   Day-0 + 6 months (relational; resolves to calendar at Day-0); interim look at
                 n=60. ✅ REACHABLE: 0.458/day × ~180 days ≈ 82 positions; n=60 lands ≈131 days
                 after Day-0.
MAX LOSS         Paper allocation **$10K**; bounded **$500 max loss per trade** by the $5 width.
                 A single position consumes ~49% of allocation by design (2–4 concurrent
                 intended) — validated as normal, not a sizing error. Concentration: all SPY;
                 the named kill shape is a gap-down.
SIZING TIER      Unchanged from current. Do not resize a watch-only bot.
CONFIG HASH      PENDING DAY-0 CAPTURE — does not exist yet; do not invent one.
                 ⛔ A-27c RULING 2026-08-08 (decision-card-2026-08-08 slot 6, OPTION 2):
                 ⬜ NOT EVALUABLE — no pre-restore baseline exists for this bot, so A-07's
                 ESTABLISHED-hash precondition does NOT apply and does NOT block this signature.
                 A capture is taken ON THE FIRST DAY THIS BOT TRADES; forward drift detection
                 starts from that capture. ⛔ It establishes nothing about the pre-restore past.
                 Opening this bot for that capture is a PURE READ (6a) and does not spend Step 2c.
VERIFICATION     Both toggles ON and screenshotted (Day-0 re-arm sweep), plus the first
                 post-cutover position's Trades list.
SIGNED           2026-08-09 · ANDY — in-chat at the S2 Day-0 sitting. Ruling recorded
                 verbatim: "Sign the seven that can trade (ledger reading)". The A-27c
                 carry in the CONFIG HASH field above does NOT block this signature
                 (decision-card-2026-08-08 slot 6, OPTION 2). Signed for Day-0
                 2026-08-10; LEDGER_START = 2026-08-10.
                 SIGNED != VERIFIED — runbook §4 Step 6's order-level Trades-list check is
                 still required before this bot may trade, and rider 2's first-trading-day
                 capture is still owed. [PR-08]
```

### `QQQ long call`
```
ID               PR-09
DISPOSITION      untouched            PILLAR/ROLE  OA-Mirror · mirror-watch   STATUS  DRAFT
HYPOTHESIS       FUNDING question — and it is currently **unanswerable**, which is this entry's
                 whole content. Pre-lapse anchor: n=6, mean R +0.3401, median R +0.3045, worst R
                 +0.2521, maxDD 0.0000R, sum R +2.040, win 100%. ⛔ **DO NOT READ THE +0.3401.**
                 The baseline is a closed-position anchor and this bot's **4 open positions
                 (≈$13K risk, ≈−$10.8K unrealized at the 2026-07-30 capture) were never in the
                 source.** On those figures the lifetime record is near −1.3R over 10 positions,
                 i.e. **the sign flips and 6-of-6 becomes 6-of-10** (memo §3 — labelled an
                 ESTIMATE there, and it stays one here). DRAFT verdict: **WATCH — RECORD
                 INCOMPLETE; verdict BLOCKED until Andy's ride-or-close is executed.**
MECHANISM        Not long-premium asymmetry, whatever the shape suggests: a **long call debit
                 spread** (0.5Δ long / 0.1Δ short, 90 DTE, QQQ) with a **low 25% profit target**
                 that is easy to hit on small rallies inside 60 days, plus the 2023–2026 tech
                 tailwind. Zero inputs, entirely hard-coded; a pure binary scanner. Redundant
                 dual exit: 25% PT (Exit Options) + a 30-market-day time exit. **No stop, no
                 regime filter.** The author's own words: *"about as bullish as it gets, will get
                 destroyed in a bear market"* (`oa-mirror-reference.md` §5.2).
KILL CRITERION   The shared funding bar, all five conjuncts (§2.6), after ≥20 completed
                 post-cutover positions. ⛔ **PRIOR CONDITION — no funding verdict may be taken,
                 in either direction, until the ride-or-close call on the 4 open positions is
                 made AND executed**, because that call determines whether the −$10.8K becomes a
                 realised part of the record (memo §3; `build-plan.md` §3). A verdict taken
                 before it is a verdict on a record that does not exist.
SAMPLE TARGET    n = 20 completed post-cutover positions for funding; n = 100 over ≥6 months
                 including a B3 regime change for an edge claim. ⚠️ Observed cadence 0.102/day →
                 **n=100 is ≈30.4 months away** (memo §7). Under the bar as written this bot is
                 not fundable on any useful horizon; Tier M would change that and is **DRAFT,
                 not in force**.
REVIEW DATE      Day-0 + 3 months (funding), Day-0 + 6 months (edge). ⛔ The open-position
                 decision is Day-0, not a review date.
GATE EVAL DATE   Day-0 + 6 months (relational; resolves to calendar at Day-0); interim look at
                 n=60. ⚠️ **NOT REACHABLE**: 0.102/day × ~180 days ≈ 18 positions. The gate will
                 evaluate on a sample far below the interim look — a signer must accept that or
                 respec the look for this bot.
MAX LOSS         Paper allocation **$30K** (10%-NL × 10 positions default). ≈$1,128 average loss,
                 ≈$2,000–$2,500 max per contract; a documented real drawdown of **$6,500+ on
                 $30K paper** in the March-2025 correction (`oa-mirror-reference.md` §5.2).
                 ⛔ Plus the ≈$13K of legacy open risk above, which is **live exposure, not a
                 modelled figure**.
SIZING TIER      Unchanged from current. Do not resize a watch-only bot.
CONFIG HASH      PENDING DAY-0 CAPTURE — does not exist yet; do not invent one.
                 ⛔ A-27c RULING 2026-08-08 (decision-card-2026-08-08 slot 6, OPTION 2):
                 ⬜ NOT EVALUABLE — no pre-restore baseline exists for this bot, so A-07's
                 ESTABLISHED-hash precondition does NOT apply and does NOT block this signature.
                 A capture is taken ON THE FIRST DAY THIS BOT TRADES; forward drift detection
                 starts from that capture. ⛔ It establishes nothing about the pre-restore past.
                 Opening this bot for that capture is a PURE READ (6a) and does not spend Step 2c.
VERIFICATION     ⛔ **Ordering is load-bearing: the ride-or-close call must be decided, LOGGED
                 and EXECUTED before this bot is armed.** Day-0 audit **F-34** flags that Step 2
                 requires the decision logged but never executed, while Step 3 then arms this
                 very bot. Then: both toggles ON and screenshotted, and the first post-cutover
                 position's Trades list.
SIGNED           NOT SIGNED — 2026-08-09. Andy's gate-A6 ruling at the S2 Day-0 sitting:
                 RIDE on all five open mirror positions. Runbook §4 Step 2 item 3 therefore
                 keeps this bot's EXIT OPTIONS OFF so the ride survives Step 3, and an
                 unsigned bot never reaches Step 7. **BOT STAYS OFF for the whole of Day-0.**
                 FORCING OBSERVATION (finding S2-R1, first-hand 2026-08-09, capture
                 data/captures/2026-08-09-s2/step2-five-positions-2026-08-09.txt): this bot's
                 4 open QQQ long call spreads ALREADY satisfy the per-position EXPIRATION
                 rung read off their own Exit Options screen, so arming EXIT OPTIONS would
                 close them at Monday's first Exit-Options scan — a capital disposition
                 executed by a re-arm sweep. Recorded, not acted on.
                 REOPEN: when the ride ends (closed or expired), or on Andy's ruling. [PR-09]
```

### `Friday 14 DTE Broken Wing IB (B-70)`
```
ID               PR-10
DISPOSITION      untouched            PILLAR/ROLE  OA-Mirror · mirror-watch   STATUS  DRAFT
HYPOTHESIS       FUNDING question. Pre-lapse anchor: n=7, mean R +0.0893, median R +0.0773, sd
                 0.0337, worst R **+0.0634 (no losing position)**, maxDD 0.0000R, win 100%.
                 DRAFT verdict: **WATCH — no verdict possible. A perfect record at n=7 is not
                 evidence** (memo §6).
MECHANISM        Positive theta from a **60/40 broken-wing iron butterfly placed 70 points below
                 the money** — both shorts on one strike, long put 60 below (wider, because that
                 is the direction it moves against), long call 40 above. Fixed-dollar offset
                 distance logic; exact-DTE match on Fridays (14 default; skips the week if the
                 exact DTE is unavailable), 10:30–11:05am, tag-gated by a 9:31am event. Three
                 exit layers: $105/contract PT, a **$1,105/contract stop that is a switch and is
                 deliberately OFF**, and a dynamic PT reduction near expiry. **The structure is
                 the hedge** (`oa-mirror-reference.md` §5.2).
KILL CRITERION   The shared funding bar, all five conjuncts (§2.6), after ≥20 completed
                 post-cutover positions. ⚠️ Two things the bar cannot see: (a) the loss tail is
                 **unobserved** here (0 losers in n=7); (b) **live operational cost is absent
                 from the record** — ITM call legs have wide bid/ask, closes fail repeatedly,
                 one operator paid $150 to close manually, and paper DIT runs ≈1/5 of live DIT,
                 so paper overstates. ⛔ **Do not "fix" the OFF stop.** Enabling it costs $1,792
                 of P/L to save ≈$290 of drawdown — 6.2× net edge destruction on the author's
                 own 96-trade disclosure. That is a source design choice; changing it makes this
                 no longer a mirror.
SAMPLE TARGET    n = 20 completed post-cutover positions for funding; n = 100 over ≥6 months
                 including a B3 regime change for an edge claim. ⚠️ Cadence 0.111/day →
                 **n=100 ≈27.5 months** (memo §7); un-fundable on a useful horizon under the bar
                 as written. Tier M is DRAFT, not in force.
REVIEW DATE      Day-0 + 3 months (funding), Day-0 + 6 months (edge).
GATE EVAL DATE   Day-0 + 6 months (relational; resolves to calendar at Day-0); interim look at
                 n=60. ⚠️ **NOT REACHABLE**: 0.111/day × ~180 days ≈ 20 positions.
MAX LOSS         Paper allocation **$10K**; structural max ≈**$2,000/contract** — the wings, not
                 a stop, are the bound. Named kill shape: a fast bear gap-down >70 points inside
                 14 days (the one ≈$1,900 loss in the author's set was the Feb-2025 tariff
                 shock). Weekend gap risk is unavoidable by construction.
SIZING TIER      Unchanged from current. Do not resize a watch-only bot.
CONFIG HASH      PENDING DAY-0 CAPTURE — does not exist yet; do not invent one.
                 ⛔ A-27c RULING 2026-08-08 (decision-card-2026-08-08 slot 6, OPTION 2):
                 ⬜ NOT EVALUABLE — no pre-restore baseline exists for this bot, so A-07's
                 ESTABLISHED-hash precondition does NOT apply and does NOT block this signature.
                 A capture is taken ON THE FIRST DAY THIS BOT TRADES; forward drift detection
                 starts from that capture. ⛔ It establishes nothing about the pre-restore past.
                 Opening this bot for that capture is a PURE READ (6a) and does not spend Step 2c.
VERIFICATION     Both toggles ON and screenshotted, **plus an explicit read that the stop switch
                 is still OFF** — its state is the mirror's fidelity to the source. Then the
                 first post-cutover position's Trades list, confirming the 60/40 structure.
SIGNED           2026-08-09 · ANDY — in-chat at the S2 Day-0 sitting. Ruling recorded
                 verbatim: "Sign the seven that can trade (ledger reading)". The A-27c
                 carry in the CONFIG HASH field above does NOT block this signature
                 (decision-card-2026-08-08 slot 6, OPTION 2). Signed for Day-0
                 2026-08-10; LEDGER_START = 2026-08-10.
                 SIGNED != VERIFIED — runbook §4 Step 6's order-level Trades-list check is
                 still required before this bot may trade, and rider 2's first-trading-day
                 capture is still owed. [PR-10]
```

### `Trendy-Paper-v1`
```
ID               PR-11
DISPOSITION      untouched            PILLAR/ROLE  OA-Mirror · mirror-watch   STATUS  DRAFT
HYPOTHESIS       FUNDING question. Pre-lapse anchor: n=15, mean R **−0.0365** but median R
                 **+0.0405**, sd 0.2822, worst R −0.9842, maxDD 1.2877R, win 80.0%. DRAFT
                 verdict: **WATCH — tail undetermined.** The negative mean is **one max-loss
                 event**; remove it and the sign flips. n=15 cannot separate "an unlucky draw
                 from a positive process" from "a process whose tail eats it", and saying which
                 is which is exactly what this entry refuses to do in advance (memo §4, §6).
MECHANISM        Short-premium collection on a trend-gated 0.15-delta, $10-wide short put spread
                 at 10 DTE, which **dynamically hedges into an asymmetric iron condor on
                 breach**. Entry gates: not already hedging; VIX < 40 AND price > 200-day SMA;
                 short-put OI > 500; exactly 0 SPS open. Exits: 90% absolute PT + SmartStops +
                 an Exit Options preset. Hedge manager closes the call spread <1 DTE if the
                 underlying is above the short call (`oa-mirror-reference.md` §5.2).
KILL CRITERION   The shared funding bar, all five conjuncts (§2.6), after ≥20 completed
                 post-cutover positions. ⚠️ Two structural facts a signer must hold: (a) the
                 **hedge can INCREASE the tail** — the documented failure mode is a V-shaped
                 reversal after breach in which both legs lose, ≈200% of intended loss; (b) the
                 **breakeven win-rate buffer is ~5 points** — at ≈83% WR expectancy flips
                 negative, against 87.9% at source and 80.0% in the baseline. That is the
                 thinnest buffer of the seven and it is already inside its own margin.
SAMPLE TARGET    n = 20 completed post-cutover positions for funding; n = 100 over ≥6 months
                 including a B3 regime change for an edge claim. ⚠️ Cadence 0.197/day →
                 **n=100 ≈14.1 months** (memo §7). Tier M is DRAFT, not in force.
REVIEW DATE      Day-0 + 3 months (funding), Day-0 + 6 months (edge).
GATE EVAL DATE   Day-0 + 6 months (relational; resolves to calendar at Day-0); interim look at
                 n=60. ⚠️ **NOT REACHABLE**: 0.197/day × ~180 days ≈ 35 positions.
MAX LOSS         Paper allocation **$10–15K**; unhedged max ≈**$1,000/contract** at $10 width —
                 but see the V-reversal shape above, where the realised loss exceeds the
                 unhedged bound. Not live-ready below a $5K account.
SIZING TIER      Unchanged from current. Do not resize a watch-only bot.
CONFIG HASH      PENDING DAY-0 CAPTURE — does not exist yet; do not invent one.
                 ⛔ A-27c RULING 2026-08-08 (decision-card-2026-08-08 slot 6, OPTION 2):
                 ⬜ NOT EVALUABLE — no pre-restore baseline exists for this bot, so A-07's
                 ESTABLISHED-hash precondition does NOT apply and does NOT block this signature.
                 A capture is taken ON THE FIRST DAY THIS BOT TRADES; forward drift detection
                 starts from that capture. ⛔ It establishes nothing about the pre-restore past.
                 Opening this bot for that capture is a PURE READ (6a) and does not spend Step 2c.
VERIFICATION     Both toggles ON and screenshotted, plus the first post-cutover position's
                 Trades list. If a breach fires, the hedge leg must appear as its own row in the
                 Trades list — an intended hedge that never executed is the HedgeD lesson
                 (`hedge-research.md` §7).
SIGNED           2026-08-09 · ANDY — in-chat at the S2 Day-0 sitting. Ruling recorded
                 verbatim: "Sign the seven that can trade (ledger reading)". The A-27c
                 carry in the CONFIG HASH field above does NOT block this signature
                 (decision-card-2026-08-08 slot 6, OPTION 2). Signed for Day-0
                 2026-08-10; LEDGER_START = 2026-08-10.
                 SIGNED != VERIFIED — runbook §4 Step 6's order-level Trades-list check is
                 still required before this bot may trade, and rider 2's first-trading-day
                 capture is still owed. [PR-11]
```

### `60min-ORB-10W-Paper-v1`
```
ID               PR-12
DISPOSITION      untouched            PILLAR/ROLE  OA-Mirror · mirror-watch   STATUS  DRAFT
HYPOTHESIS       FUNDING question. Pre-lapse anchor: n=12, mean R **−0.0328** but median R
                 **+0.0786**, sd 0.3885, worst R −1.0000, maxDD 1.0000R, win 83.3%. DRAFT
                 verdict: **WATCH — tail undetermined**, the same shape as `Trendy-Paper-v1`
                 (memo §4, §6).
MECHANISM        Fading a failed 60-minute opening-range breakout: an SPX 0DTE **10-wide** short
                 put OR call credit spread with the short strike at the ORB level ($0.01
                 buffer), a **built-in $140 stop and $50 profit target**, min credit $0.70,
                 Mon/Tue/Wed/Fri only, FOMC excluded, entries before 2pm. The narrow wing
                 pre-commits the loss cap at entry rather than relying on stop execution
                 (`oa-mirror-reference.md` §5.2).
KILL CRITERION   The shared funding bar, all five conjuncts (§2.6), after ≥20 completed
                 post-cutover positions. ⚠️ **Conjunct 3 has a weak referent here**: the source
                 is tagged *"Backtest: None"* and is community-validated only, so "win rate
                 within ~10% of the source's claim" is measured against a leaderboard figure and
                 not against a disclosed backtest. State which number is being used when the
                 conjunct is evaluated, or the conjunct is unfalsifiable.
SAMPLE TARGET    n = 20 completed post-cutover positions for funding; n = 100 over ≥6 months
                 including a B3 regime change for an edge claim. ⚠️ Cadence 0.250/day →
                 **n=100 ≈11.6 months** (memo §7). Tier M is DRAFT, not in force — and the memo
                 explicitly doubts the Tier-M defined-risk carve-out applies to a **stop-managed**
                 strategy, because a stop is an execution promise and this fleet has already paid
                 for the difference between a promised exit and an executed one (§7a Q3).
REVIEW DATE      Day-0 + 3 months (funding), Day-0 + 6 months (edge).
GATE EVAL DATE   Day-0 + 6 months (relational; resolves to calendar at Day-0); interim look at
                 n=60. ⚠️ **NOT REACHABLE**: 0.250/day × ~180 days ≈ 45 positions.
MAX LOSS         Paper allocation **$10K**; 10-wide SPX 0DTE credit spread with a built-in $140
                 stop; source avg loss −$326 against −$650 for the wide-wing sibling. Worst
                 realised in the baseline −1.0000R, so the stop is not a guarantee.
SIZING TIER      Unchanged from current. Do not resize a watch-only bot.
CONFIG HASH      PENDING DAY-0 CAPTURE — does not exist yet; do not invent one.
                 ⛔ A-27c RULING 2026-08-08 (decision-card-2026-08-08 slot 6, OPTION 2):
                 ⬜ NOT EVALUABLE — no pre-restore baseline exists for this bot, so A-07's
                 ESTABLISHED-hash precondition does NOT apply and does NOT block this signature.
                 A capture is taken ON THE FIRST DAY THIS BOT TRADES; forward drift detection
                 starts from that capture. ⛔ It establishes nothing about the pre-restore past.
                 Opening this bot for that capture is a PURE READ (6a) and does not spend Step 2c.
VERIFICATION     ⚠️ **NAME-COLLISION GUARD — read the bot name character by character before
                 arming.** `60min-ORB-10W-Paper-v1` **stays live**; `Opening Range Breakout 60m`
                 is a DIFFERENT bot, is OFF, and is **being archived** (`build-plan.md` §2A;
                 memo §1). Arming the wrong one re-arms a bot with a draft KILL against it. Then
                 both toggles ON and screenshotted, plus the first post-cutover Trades list.
SIGNED           2026-08-09 · ANDY — in-chat at the S2 Day-0 sitting. Ruling recorded
                 verbatim: "Sign the seven that can trade (ledger reading)". The A-27c
                 carry in the CONFIG HASH field above does NOT block this signature
                 (decision-card-2026-08-08 slot 6, OPTION 2). Signed for Day-0
                 2026-08-10; LEDGER_START = 2026-08-10.
                 SIGNED != VERIFIED — runbook §4 Step 6's order-level Trades-list check is
                 still required before this bot may trade, and rider 2's first-trading-day
                 capture is still owed. [PR-12]
```

### `Tasty Condor`
```
ID               PR-13
DISPOSITION      untouched            PILLAR/ROLE  OA-Mirror · mirror-watch   STATUS  DRAFT
HYPOTHESIS       FUNDING question. Pre-lapse anchor: n=4, mean R +0.3468, median R +0.3794, sd
                 0.0812, worst R +0.2266, maxDD 0.0000R, win 100%. DRAFT verdict: **WATCH — no
                 verdict possible at n=4**, plus **1 open position (≈+$328) that the baseline
                 cannot see** — the same structural blind spot as PR-09, directionally
                 favourable and evidentially worth nothing at n=4 (memo §3, §6).
MECHANISM        Pure 45-DTE theta, exited before gamma acceleration: a ±0.20-delta iron condor,
                 single scanner, **no monitors** — the most mechanically minimalist bot in the
                 mirror set. Entry gates: VIX < `Max VIX`, a frequency throttle, exactly 0
                 same-cycle positions, 10:00am+. Exit **entirely via Exit Options — 50% of
                 opening credit OR a mechanical 21-DTE time exit, whichever comes first.** The
                 time exit IS the risk management (`oa-mirror-reference.md` §5.2).
KILL CRITERION   The shared funding bar, all five conjuncts (§2.6), after ≥20 completed
                 post-cutover positions. ⛔ **No cadence-based kill.** A 45-DTE entry does not
                 expire for ~6 weeks; the v1 "kill if no trades by day 21" flag was struck for
                 exactly this reason (`oa-mirror-reference.md` §5.2, June note) and must not be
                 reintroduced under another name. Slow is this bot's design, not a defect —
                 the same reasoning PR-05 carries for a gate that correctly never fires.
                 ⚠️ The open position must be resolved into the record before any verdict, on
                 the PR-09 principle, even though its sign is favourable.
SAMPLE TARGET    n = 20 completed post-cutover positions for funding; n = 100 over ≥6 months
                 including a B3 regime change for an edge claim. ⚠️ Cadence 0.103/day →
                 **n=100 ≈30.7 months** (memo §7), the slowest of the seven. Tier M is DRAFT,
                 not in force.
REVIEW DATE      Day-0 + 3 months (funding), Day-0 + 6 months (edge).
GATE EVAL DATE   Day-0 + 6 months (relational; resolves to calendar at Day-0); interim look at
                 n=60. ⚠️ **NOT REACHABLE**: 0.103/day × ~180 days ≈ 19 positions.
MAX LOSS         Paper allocation **$10K**; **$500 max loss per position at $5 wings**. Source
                 avg win / avg loss $225 / −$397 — ratio 0.57, the most balanced in the set;
                 the 21-DTE exit caps the damage. ⛔ Plus the 1 open position (≈+$328) above.
SIZING TIER      Unchanged from current. Do not resize a watch-only bot.
CONFIG HASH      PENDING DAY-0 CAPTURE — does not exist yet; do not invent one.
                 ⛔ A-27c RULING 2026-08-08 (decision-card-2026-08-08 slot 6, OPTION 2):
                 ⬜ NOT EVALUABLE — no pre-restore baseline exists for this bot, so A-07's
                 ESTABLISHED-hash precondition does NOT apply and does NOT block this signature.
                 A capture is taken ON THE FIRST DAY THIS BOT TRADES; forward drift detection
                 starts from that capture. ⛔ It establishes nothing about the pre-restore past.
                 Opening this bot for that capture is a PURE READ (6a) and does not spend Step 2c.
VERIFICATION     Both toggles ON and screenshotted, plus the first post-cutover position's
                 Trades list showing the 50%-credit OR 21-DTE exit — this bot has **no
                 monitors**, so the Exit Options preset is the entire exit engine and its
                 execution is the only thing that proves it lives.
SIGNED           NOT SIGNED — 2026-08-09. Andy's gate-A6 ruling at the S2 Day-0 sitting:
                 RIDE on all five open mirror positions. Runbook §4 Step 2 item 3 therefore
                 keeps this bot's EXIT OPTIONS OFF so the ride survives Step 3, and an
                 unsigned bot never reaches Step 7. **BOT STAYS OFF for the whole of Day-0.**
                 FORCING OBSERVATION (finding S2-R1, first-hand 2026-08-09, capture
                 data/captures/2026-08-09-s2/step2-five-positions-2026-08-09.txt): this bot's
                 1 open SPY iron condor ALREADY satisfy the per-position EXPIRATION
                 rung read off their own Exit Options screen, so arming EXIT OPTIONS would
                 close them at Monday's first Exit-Options scan — a capital disposition
                 executed by a re-arm sweep. Recorded, not acted on.
                 REOPEN: when the ride ends (closed or expired), or on Andy's ruling. [PR-13]
```

---

## 5a. The ride-or-close decision on the five open mirror positions — DRAFTED AND RULED 2026-08-09

*Opened by `reactivation-runbook.md` §4 Step 2 (gate A6) and by §8 item 5 of this ledger, which
recorded that this entry "is not yet drafted". It is drafted here, at Day-0, before Step 3 touched
any toggle. It is a CAPITAL decision and go-live authority is Andy's.*

```
ID               PR-RC-01   (ride-or-close, not a bot)
DISPOSITION      capital decision on pre-cutover positions   STATUS  RULED 2026-08-09
SCOPE            The five mirror positions open through the 2026-06 lapse, the 2026-08-07 account
                 disable, and the 2026-08-07 roster loss. Two bots: `QQQ long call` (4) and
                 `Tasty Condor` (1).
A-10 BRANCH      ALL FIVE PRESENT, structure unchanged (same legs, same quantity, same open
                 dates); only mark-to-market moved. => proceed as written with FRESH numbers.
                 `RIDE-OR-CLOSE MOOTED BY THE 2026-08-07 ROSTER LOSS` is NOT recorded — it does
                 not apply. Re-read first-hand 2026-08-09 ~11:27 ET; capture
                 data/captures/2026-08-09-s2/step2-five-positions-2026-08-09.txt
                 sha256 068922df08b133306f44f103f9c17a31515d367478f12a36fb88c7f16f1a31ef
THE FIVE         P1 Tasty Condor  SPY IC AUG 21 689P/704P/784C/799C  +$197 (47.13%)  risk $1,082
                 P2 QQQ long call QQQ LCS AUG 31 743C/850C          -$2,335 (-78.59%) risk $2,971
                 P3 QQQ long call QQQ LCS SEP 18 745C/865C          -$2,181 (-66.11%) risk $3,299
                 P4 QQQ long call QQQ LCS SEP 30 745C/870C          -$2,113 (-60.58%) risk $3,488
                 P5 QQQ long call QQQ LCS SEP 30 727C/839C          -$1,113 (-33.95%) risk $3,278
                 Account: TOTAL P/L -$7,545 · RISK $14,118 · COUNT 5.
THE DECISION     RIDE, all five. Andy, in-chat at the S2 Day-0 sitting 2026-08-09, gate A6.
THE REASON       Two reasons, both stated at the gate rather than inferred afterwards.
                 (a) The alternative on the day was not a hand close — the market was closed on
                     2026-08-09 — but ARMING, and arming is not a close: it is a disposition
                     executed by the exit stack on a schedule nobody chose. See EXECUTION below.
                 (b) `mirror-funding-memo-2026-08-05.md` §1: ZERO of ten mirrors clears the
                     evidence bar and none can before late Oct 2026. The Day-0 mirror action is
                     RE-ARM, WATCH-ONLY, SIZE NOTHING. There is no evidentiary basis on which to
                     realise -$7,545 today, and none on which to add.
                 SAID OUT LOUD, per Step 2 item 4: "insufficient evidence" is NOT "do nothing".
                     For a RUNNING position, riding IS a capital decision, and it is being made
                     here deliberately, by Andy, on the record — not by default.
EXECUTION        A RIDE executes by NOT acting, but it only survives if Step 3 leaves it alone.
                 Finding S2-R1, first-hand 2026-08-09, read from each position's OWN Exit Options
                 screen (the third toggle surface — FIRST observation ever on a lapse-surviving
                 position; a close destroys it permanently):
                   P1  PROFIT % 50%  · EXPIRATION 21 days · 12 days to expiration  -> rung ALREADY MET
                   P2  PROFIT % 25%  · EXPIRATION 30 days · 22 days to expiration  -> rung ALREADY MET
                   P3  PROFIT % 25%  · EXPIRATION 30 days · 40 days to expiration  -> fires ~2026-08-19
                   P4  PROFIT % 25%  · EXPIRATION 30 days · 52 days to expiration  -> fires ~2026-08-31
                   P5  PROFIT % 25%  · EXPIRATION 30 days · 52 days to expiration  -> fires ~2026-08-31
                 P1 additionally sits at 47.13% against a 50% PT rung.
                 => Arming EXIT OPTIONS on either bot would CLOSE P1 and P2 at Monday's first
                 Exit-Options scan and pre-commit P3/P4/P5. Runbook §4 Step 2 item 3 governs:
                 "If anything would act on the five positions against the decision, leave that
                 bot's EXIT OPTIONS OFF." APPLIED: `QQQ long call` and `Tasty Condor` are EXCLUDED
                 from the Step 3 re-arm sweep, stay EXIT OPTIONS OFF, stay AUTOMATIONS OFF, and
                 their entries PR-09 and PR-13 are deliberately NOT SIGNED.
COST, NAMED      Step 6a — the mechanism verdict, "the step that settles §1" — runs on the NINE
                 leave-in-place bots ONLY. Two of the nine are now out of scope for Day-0, so 6a
                 can reach at most 7 subjects, and only once those seven open a first position.
                 This is a real reduction in the evidence available to settle the June cause and
                 it is accepted with the ruling, not discovered later.
STRADDLE RULE    All five opened pre-cutover (Jun 1 - Jun 29 2026), so under `CLAUDE.md` §3 their
                 P/L resolves into the MIRROR BASELINE layer and NEVER into the working ledger.
                 `data/mirror_baseline.csv` is an ANCHOR and is NOT recomputed (no --force).
                 `QQQ long call`'s baseline record stays structurally incomplete — the export held
                 only closed positions, so these four were never in the source. Its +0.3401 must
                 not be read (mirror-funding-memo §1). That does not change on a ride.
REVIEW           Re-read at every close-out while any of the five is open. The ride ENDS by
                 expiry or by an explicit later ruling — never by an unremarked re-arm.
REOPEN           (i) Any position closes or expires; (ii) Andy rules otherwise; (iii) either bot
                 is proposed for the Step 3 sweep again — at which point S2-R1 is re-read FIRST.
SIGNED           2026-08-09 · ANDY — in-chat at the S2 Day-0 sitting, gate A6, ruling recorded
                 verbatim: "Ride: leave both bots' EXIT OPTIONS OFF".
```

**§8 item 5 is discharged by this entry.** It read *"The ride-or-close decision on the five open
mirror positions belongs in this ledger and is not yet drafted"*. It is drafted, ruled and signed.

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
                 "quantity":1}`. Applies to all eight greenfield-family arms, PR-14…PR-23
                 (`greenfield-family-spec.md` C4, memory row).
KILL CRITERION   Per arm: Exp(R) per condor < 0 with CI entirely below 0 at n≥60.
                 📝 AMENDED 2026-08-06 (G-8, SEQUENCE+CS, ruled by Andy) — the n≥60 read
                 above is emitted as an always-valid confidence sequence, not a fixed-n CI, and
                 the absolute kill cannot retire an arm before its own stamped GATE EVAL DATE
                 (§2 template). FAMILY-LEVEL and sentinel criteria (execution-integrity rules)
                 are unaffected.
                 FAMILY-LEVEL (REPLACED 2026-08-05 — see the banner below this entry):
                 if a capture-diff ever shows two arms differing in MORE THAN ONE MECHANIC
                 (a trigger field and, if present, its own pricing sub-field), or if any of
                 greenfield-family-spec.md §8.3's A1, A2, A3, A7 or A8 fires, the family's
                 ranking is VOID and all arms are re-based — the comparison, not the bots,
                 is what dies.

                 📝 ADDED 2026-08-07 (G-12b, SIGNED AS DRAFTED, Andy) — PR-16-SPECIFIC TAIL
                 RETIREMENT CRITERION. Applies to PR-16 (`GF-QQQ-IC-Trail`) only — PR-14, PR-15
                 and PR-17 are unaffected and keep only the arm-level criterion above. Replaces
                 the struck worst-condor-R clause recorded in `greenfield-family-spec.md` §9's
                 PR-16 entry; that struck text is left standing there per this project's standing
                 convention (`CLAUDE.md` §5) and is not repeated here. Exact ledger text, pasted
                 verbatim from `post-u1-package-2026-08-07.md` §1.7:

                 TAIL RETIREMENT CRITERION — PR-16 T1, FAST-MOVE TAIL PAIRED NON-HARM
                 TEST. Replaces the struck worst-condor-R clause per ruling G-12
                 (RESPEC, Andy, 2026-08-06); method signed 2026-08-07 under ruling G-12b.

                 STATISTIC.  Over the G-2 matched-day set M6 (PR-14..PR-19), with
                 d_i = R_X(i) - R_C(i) per condor (X = this arm, C = GF-QQQ-IC-Ride,
                 R = sum(pnl)/max(risk), risk = larger side, [DERIVED, UNCORROBORATED]):
                   move_i = |underlying_close - underlying_open| / underlying_open
                   T      = the m days in M6 with the LARGEST move_i,
                            m = ceil(p*n), n = n_matched_days
                   dTail  = mean of d_i over i in T
                 T is selected on move_i -- a day-level variable IDENTICAL for every arm --
                 and NEVER on any arm's own outcome. X and C are therefore exchangeable
                 under the null and E[dTail] = 0 BY SYMMETRY. This is the arm's own
                 declared mechanism domain: "bites in the fast-move tail"
                 (hedge-research.md 14.1, quoted in this entry's HYPOTHESIS).
                 DECLARED LIMITATION, CHOSEN NOT DISCOVERED: move_basis is OPEN-TO-CLOSE,
                 NOT the intraday extreme, so it under-ranks reversal days. The ledger
                 carries endpoints only and this is not fixable by exit_rows.csv. It costs
                 power; it does not cost the null centering.

                 SIGNED CONSTANTS.   p     = 0.20        (tail fraction)
                                     delta = 0.10 R      (non-harm margin, per condor, on T)
                                     floor = n_matched_days >= 100   (so m >= 20)
                 delta IS A NEW MARGIN. It is NOT re-scaled or transported from R-3's
                 +0.015R; that argument was refuted in adversarial review and withdrawn.
                 It carries no inherited authority and stands only on this signature.

                 DECISION.  RETIRE this arm iff ci_fam_hi(dTail) < -delta, where ci_fam_hi
                 is the family-corrected upper bound from the joint day-bootstrap
                 simultaneous region under ruling G-10, with THIS MEMBER'S DIRECTION
                 DECLARED UPPER BEFORE ANY DATA EXISTS. B >= 200,000; seed declared and
                 recorded. T is recomputed inside every bootstrap replicate.
                 If n_matched_days < 100 the verdict is INCAPABLE -- never RETIRE, never
                 FAIL, and never read as a retirement.

                 SEQUENCING.  Computed EXACTLY ONCE, at this arm's stamped GATE EVAL DATE
                 (G-7). No confidence sequence is emitted for dTail; pre-gate it is
                 descriptive and flagged NOT_A_GATE, and retirement cannot fire before the
                 gate-eval date (G-8). RE-ARM, DECLARED IN ADVANCE: if n_matched_days < 100
                 at that date, the test re-arms ONCE at Day-0 + 9 months. If n < 100 again,
                 INCAPABLE is TERMINAL and this arm carries no tail retirement rule.

                 PUBLICATION.  A RETIRE verdict may not be published without mde_tail
                 (computed from sd_dtail_boot, never from se_dtail), sd_d_tail,
                 n_matched_days, m, c, seed, B, family_census, pnl_may_be_modelled,
                 n_all_expired_X/C, n_days_dropped_all_expired and move_basis.
                 Refusal R-6 stands: no verdict while pnl_may_be_modelled == true
                 (itmlive != market).
                 CF-1's precondition -- "no tail-based ranking is published without" the D7
                 per-arm Market-priced / ITM-action counts -- is UNMET while G-1 is on HOLD.
                 The verdict therefore carries CF1_PUBLICATION_PRECONDITION: UNMET.

                 CARRIED LIMITS, declared: (1) dTail is a COMPONENT of mean d, not an
                 orthogonal statistic (mean d = p*dTail + (1-p)*d_offT). (2) X-1 excludes
                 all-expired groups, which is the ITM-expiry tail; counts are published.
                 (3) An arm-specific loss mode occurring on a CALM day lies outside T and
                 this criterion cannot see it -- T1 answers "does the trail harm the tail in
                 the regime it claims to operate in", not "does the trail add loss anywhere".

                 Family membership: INSIDE the family correction (ruled 2026-08-07). Publication
                 cap acknowledged (package §3 — no option meets CF-1's precondition while G-1 is
                 on HOLD).
SAMPLE TARGET    n = 100 positions per arm, on matched days.
REVIEW DATE      Day-0 + 6 months, interim at n=60.
MAX LOSS         1 lot per arm until one clears its interim read; then ≈$5K risk/position.
SIZING TIER      1 lot — experiment. IDENTICAL across all arms.
CONFIG HASH      ✅ STAMPED 2026-08-17 under `R-2026-08-17-GF-ENTRY-METHOD`. The entry surface is
                 the two SHARED Library automations (`sharing:1`, "8 bots"), so ONE pair of hashes
                 covers all eight arms — there is no per-arm entry hash to capture.
                   GF-ScannerA-PutSpread  v12  1e5eb9936a1adf067af65a4841d42e755592f7c179f3c0cad477502dfdbfcdc8
                   GF-ScannerB-CallSpread v4   a925d490b8a0d2337566f47307fc52470da129935d3bd83d24389c6dc433dfb5
                 Formula: sha256(JSON.stringify({name, inputs, root})), computed after opening the
                 automation fresh. Both re-read after a HARD RELOAD from the Library surface, not
                 from a save confirmation. ⚠️ A VERSION INCREMENT IS NOT EVIDENCE — ONLY THE HASH IS
                 (ScannerA once went v10→v11 with a byte-identical payload and an identical hash).
                 ⛔ CARRIED, GATED: `GF-ScannerB-CallSpread` still stores the legacy
                 `price {pct:100}` while ScannerA stores `{limit:100, limitType:"pct"}`. Ruled to
                 STAY as-is for this sample so the delta change is the only variable. Migration
                 mechanism is named and gated — see the open item in RULINGS.md. It does NOT block
                 this signature; it is a known, recorded carry.
VERIFICATION     A CAPTURE-DIFF showing exactly ONE differing line between any two arms. Not a
                 claim, a diff. Plus each arm's first-position Trades list.
SIGNED           2026-08-17 · ANDY — in-session, verbatim "Sign now", under
                 `R-2026-08-17-GF-ENTRY-METHOD`. Config hashes as stamped above. Sample restarts at
                 the 2026-08-17 edit; nothing before it counts. Review at 10 sessions.
                 ⚠️ LAYER 2 IS OUTSTANDING — the first new position's Trades list must confirm the
                 strikes are delta-selected, not 0.40%-selected. Signature stands on Layer 1.
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
                 "quantity":1}`. Applies to all eight greenfield-family arms, PR-14…PR-23
                 (`greenfield-family-spec.md` C4, memory row).
KILL CRITERION   The tournament is VOID (not the bots) if any of hedge-research.md §5.2's five
                 conditions fails: shared automation · one differing input proven by
                 capture-diff · same execution class · Range075 on every arm · a proof-of-fire
                 artifact identified in advance. Per arm: Exp(R) < 0, CI below 0, n≥60.
                 📝 AMENDED 2026-08-06 (G-8, SEQUENCE+CS, ruled by Andy) — the n≥60 read
                 above is emitted as an always-valid confidence sequence, not a fixed-n CI, and
                 the absolute kill cannot retire an arm before its own stamped GATE EVAL DATE
                 (§2 template). The tournament-VOID and sentinel criteria (execution-integrity
                 rules) are unaffected.
SAMPLE TARGET    n = 100 positions per arm.
REVIEW DATE      Day-0 + 6 months.
MAX LOSS         1 lot per arm.
SIZING TIER      1 lot — IDENTICAL across arms.
CONFIG HASH      ✅ STAMPED 2026-08-17 under `R-2026-08-17-GF-ENTRY-METHOD`. The entry surface is
                 the two SHARED Library automations (`sharing:1`, "8 bots"), so ONE pair of hashes
                 covers all eight arms — there is no per-arm entry hash to capture.
                   GF-ScannerA-PutSpread  v12  1e5eb9936a1adf067af65a4841d42e755592f7c179f3c0cad477502dfdbfcdc8
                   GF-ScannerB-CallSpread v4   a925d490b8a0d2337566f47307fc52470da129935d3bd83d24389c6dc433dfb5
                 Formula: sha256(JSON.stringify({name, inputs, root})), computed after opening the
                 automation fresh. Both re-read after a HARD RELOAD from the Library surface, not
                 from a save confirmation. ⚠️ A VERSION INCREMENT IS NOT EVIDENCE — ONLY THE HASH IS
                 (ScannerA once went v10→v11 with a byte-identical payload and an identical hash).
                 ⛔ CARRIED, GATED: `GF-ScannerB-CallSpread` still stores the legacy
                 `price {pct:100}` while ScannerA stores `{limit:100, limitType:"pct"}`. Ruled to
                 STAY as-is for this sample so the delta change is the only variable. Migration
                 mechanism is named and gated — see the open item in RULINGS.md. It does NOT block
                 this signature; it is a known, recorded carry.
NAMING           ✅ GATE A8 RULED BY ANDY 2026-08-08 (decision-card-2026-08-08 slot 5) — PR-18,
                 OPTION C / THE SPLIT. LEDGER / INTERNAL LABEL: "Breakeven" (CF-4 discharged
                 2026-08-06 by the C8 ruling; the untested side is left to decay, so the arm can
                 reach the shape its anchor describes). PUBLISHED OR EXTERNALLY COMPARED: the
                 MECHANICAL name only — `SL100` / "stop at 100% of credit" — with the CF-1 caveat
                 attached at that surface. ⛔ CF-1 IS NOT DISCHARGED and bounds what this family
                 may conclude against Sandvand's rung. OA bot name `GF-QQQ-IC-SL100` unchanged.
                 THIS FIELD IS NOW RESOLVED — it no longer holds the entry UNSIGNED under §7
                 item 2. PR-19 (`SL200`) follows the same convention by construction.
VERIFICATION     Capture-diff, one differing input. No ranking published until it passes.
SIGNED           2026-08-17 · ANDY — in-session, verbatim "Sign now", under
                 `R-2026-08-17-GF-ENTRY-METHOD`. Config hashes as stamped above. Sample restarts at
                 the 2026-08-17 edit; nothing before it counts. Review at 10 sessions.
                 ⚠️ LAYER 2 IS OUTSTANDING — the first new position's Trades list must confirm the
                 strikes are delta-selected, not 0.40%-selected. Signature stands on Layer 1.
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
                 "quantity":1}`. Applies to all eight greenfield-family arms, PR-14…PR-23
                 (`greenfield-family-spec.md` C4, memory row).
KILL CRITERION   None on P/L — it is exempt by design, and that exemption is stated here so it
                 cannot later be mistaken for a losing bot nobody killed. It is retired when the
                 detector's Tier C rules cover the same ground with a live config.
SAMPLE TARGET    n/a — daily fill/no-fill is the output.
REVIEW DATE      Day-0 + 3 months: is it still earning its slot?
MAX LOSS         1 lot, smallest expressible risk.
SIZING TIER      1 lot.
CONFIG HASH      ✅ STAMPED 2026-08-17 under `R-2026-08-17-GF-ENTRY-METHOD`. The entry surface is
                 the two SHARED Library automations (`sharing:1`, "8 bots"), so ONE pair of hashes
                 covers all eight arms — there is no per-arm entry hash to capture.
                   GF-ScannerA-PutSpread  v12  1e5eb9936a1adf067af65a4841d42e755592f7c179f3c0cad477502dfdbfcdc8
                   GF-ScannerB-CallSpread v4   a925d490b8a0d2337566f47307fc52470da129935d3bd83d24389c6dc433dfb5
                 Formula: sha256(JSON.stringify({name, inputs, root})), computed after opening the
                 automation fresh. Both re-read after a HARD RELOAD from the Library surface, not
                 from a save confirmation. ⚠️ A VERSION INCREMENT IS NOT EVIDENCE — ONLY THE HASH IS
                 (ScannerA once went v10→v11 with a byte-identical payload and an identical hash).
                 ⛔ CARRIED, GATED: `GF-ScannerB-CallSpread` still stores the legacy
                 `price {pct:100}` while ScannerA stores `{limit:100, limitType:"pct"}`. Ruled to
                 STAY as-is for this sample so the delta change is the only variable. Migration
                 mechanism is named and gated — see the open item in RULINGS.md. It does NOT block
                 this signature; it is a known, recorded carry.
VERIFICATION     A PT fill on day 1, read from the Trades list.
SIGNED           2026-08-17 · ANDY — in-session, verbatim "Sign now", under
                 `R-2026-08-17-GF-ENTRY-METHOD`. Config hashes as stamped above. Sample restarts at
                 the 2026-08-17 edit; nothing before it counts. Review at 10 sessions.
                 ⚠️ LAYER 2 IS OUTSTANDING — the first new position's Trades list must confirm the
                 strikes are delta-selected, not 0.40%-selected. Signature stands on Layer 1.
```

---

## 6a. Group E — Lab ops bots (≤2)

> ### 🔓 ADDED 2026-08-07 — "amend the plan", Andy's explicit words (E-2)
> Class defined in §2a. **No specific bot is named or entered here yet** —
> `exploratory-bots-design-2026-08-07.md` §1/§2 catalogs the candidate instruments (e.g. an
> R2/C10 `dstop`-unit instrument, an R3 `dprofit` instrument) but §8 open items leaves final
> selection, naming and IDs to build time, same as Group D's fresh builds. Entries land here per
> the §2 template as amended by §2a, each with a signed `PHASE LOG` (guardrail G8) before its
> first phase starts. ⛔ **No entry, no restart applies to this group exactly as to every other**
> — §1's exemption pattern is PR-20's, not a waiver.
>
> ⛔ **Gated ahead of any entry becoming signable:** E-3's hard precondition — `build_ledger.py`
> exclusion + `a_series` scoping + Lab group/tag fencing, implemented and verified
> (`exploratory-bots-design-2026-08-07.md` §3.3, Claude Code task, not yet queued as implemented)
> — and the OA restore landing, and Andy's go.

---

## 7. Signing checklist — Day-0

For each of the ~~≈18–20~~ **≈18–20 plan bots, every Track B arm, and every Lab ops bot — up to
30 in total** (scoped 2026-08-05, amended 2026-08-07; `build-plan.md` §2D's
`🔓 SCOPING AMENDMENT 2026-08-05` and `🔓 AMENDMENT 2026-08-07`, §3 above), in this
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

> ### 📝 ADDED 2026-08-07 — three open items surfaced while drafting PR-07…PR-13 (§5).
> **None of them is decided here.** Each is a decision or a correction that touches text outside
> this session's scope, so each is filed rather than applied.

7. **PR-05 and PR-06 predate the `GATE EVAL DATE` field** and do not carry it. The field was
   added to §2's template on 2026-08-06 (**G-7**, STAMP, ruled by Andy); PR-07…PR-13 carry it,
   PR-14…PR-23 carry it, and the two Directional entries in §5 do not. Under §7 item 2 an entry
   with an unresolved field is unsigned, so this must be closed before Day-0 — but adding the
   field to a written entry is an edit to that entry, and the Task-10 scope forbade one. **Andy's
   call: stamp both, or rule the field inapplicable to non-comparative bots.**
   ✅ **RULED 2026-08-07 (Andy): stamp both.** Applied — PR-05 and PR-06 in §5 now carry
   `GATE EVAL DATE`, stamped as a standalone R kill, not a comparative gate.
8. **The funding bar is stated in P/L and win rate; §2's rule 1 forbids both in a kill
   criterion.** `oa-mirror-reference.md` §2.6's conjuncts 2 and 3 are *"positive P/L overall —
   instance-profitable"* and *"win rate within ~10% of the source's claim"*, and §2 rule 1 above
   reads *"The kill criterion is in R. Never dollars, never win rate."* Seven entries now carry
   the §2.6 bar verbatim, so the tension is load-bearing rather than cosmetic. It may well be
   correct — a **funding** bar is not an **edge** bar, and the two rules may be about different
   questions — but that is a ruling, not a reading. ⚠️ `CLAUDE.md` §4's *"compare by R, never
   raw P/L"* points the same way.
   ✅ **RESOLVED 2026-08-07 (Andy's ruling).** Scoping note added to
   `oa-mirror-reference.md` §2.6 — the funding bar governs a **funding** decision, not a
   **kill/edge** criterion; §2 rule 1 and `CLAUDE.md` §4 bind the latter only. No conflict.
9. **`data/mirror_baseline.csv` exists and holds TEN rows, not nine.** `[FIRST-HAND 2026-08-07,
   direct `device_bash` read of the file]`: header plus 10 mirror rows, 174 positions, written
   2026-08-04, sha cited as `cdceb0a8d444e570…` by `mirror-funding-memo-2026-08-05.md` §9. Two
   statements elsewhere are now stale — §5's frame note calls it *"a one-time frozen snapshot,
   nine rows"*, and `CLAUDE.md` §3 lists it as *"not yet written"*. Neither is inside a PR entry
   and neither changes a decision (the funding scope is still the **7** live mirrors; the other
   three are OFF and out of scope, memo §1), so both are **flagged here, not edited**.

---

### PR-23 — `GF-QQQ-IC-Ride-Delta`   ⚠️ DRAFT, UNSIGNED. Authored 2026-08-11.

> ✅ **AMENDED 2026-08-12.** Andy ruled `GF-QQQ-IC-Ride-Delta` is the **8th greenfield family
> arm**, not an external control. The family definition in `greenfield-family-spec.md` §0/§1 is
> widened from "one Exit-Options bundle" to "one input value" so that a strike-selection method
> (delta vs fixed percent) is a valid arm variable. The original rationale is left standing below.

```
ID               PR-23
DISPOSITION      8th greenfield arm    PILLAR/ROLE  IC · experiment    STATUS  DRAFT
SOURCE           GF-QQQ-IC-Ride  BOTfw5TkkCRF4417860701930934951
HYPOTHESIS       Short-strike selection by DELTA adapts to volatility and time-to-expiry;
                 selection by FIXED PERCENT OF LAST does not. Paired against Ride — identical
                 symbol, wings, window, regime gates, sizing, pricing, floor and exit policy
                 (ride to expiry) — the two differ in EXACTLY ONE input: the short-strike
                 selection method. Any divergence in entry FREQUENCY or in realised OTM% over
                 time is therefore attributable to that method alone.
MECHANISM        Established 2026-08-11, first-hand: PR-01 and the eight GF arms use
                 `legpctprice pct=0.75`; PR-02 uses `delta 0.1` and is the only bot in the
                 fleet filling daily. PR-01 vs PR-02 are byte-identical in wings, price,
                 sizing and filter — the selection method is the sole differing field.
                 Supporting: credit at >=0.70% OTM on SPX 0DTE fell ~60% Apr->Aug 2026
                 (0.320 / 0.291 / 0.343 / 0.153 / 0.125), i.e. the fixed-% spec aged out of
                 its regime rather than breaking.
PRIMARY READ     ENTRY FREQUENCY and REALISED OTM% — not P/L. This bot is run to answer a
                 mechanical question, and n will be far too small for an R read for months.
KILL CRITERION   Exp(R) per condor < 0 with CI entirely below 0 at n>=60, emitted as an
                 always-valid confidence sequence (per G-8), and not before GATE EVAL DATE.
                 ⚠️ P/L IS NOT THE POINT AND MUST NOT RETIRE IT EARLY. If at n>=20 the bot has
                 taken ZERO entries, the delta value is wrong, not the method — re-tune, do not
                 kill.
GATE EVAL DATE   2026-11-11 (3 months from authoring).
ALLOCATION       $2,500 — matched to the GF arms. Sizing `amount:{"type":"quantity",
                 "quantity":1}`, fixed 1 contract, per the PR-14…PR-23 SIZING STAMP 2026-08-06.
                 Position limit 2/2.
STARTING DELTA   0.10 / -0.10 — PR-02's observed-working value, NOT a derivation. On QQQ a given
                 delta sits further out in percent terms than on SPX, so this may land near the
                 0.40% the pct arms will run. ⚠️ RECORD WHERE IT ACTUALLY LANDS ON DAY ONE. If
                 it lands far from 0.40%, the pairing is degraded and must be re-tuned before
                 any comparison is read.
RISK NOTE        PAPER. $2,500 allocation, 1 contract, $2 wings — max risk ~$200/condor.
SIGNED           2026-08-17 · ANDY — in-session, verbatim "Sign now", under
                 `R-2026-08-17-GF-ENTRY-METHOD`. Config hashes as stamped above. Sample restarts at
                 the 2026-08-17 edit; nothing before it counts. Review at 10 sessions.
                 ⚠️ LAYER 2 IS OUTSTANDING — the first new position's Trades list must confirm the
                 strikes are delta-selected, not 0.40%-selected. Signature stands on Layer 1.
```

> **Andy authorised the build and the switch-on verbally, 2026-08-11** ("i give permission to
> for you to turn the clone on. its just a test."). **That authorisation is recorded, but it is
> NOT a signature** — §5's `SIGNED` line takes a date and a config-capture hash, and the hash
> does not exist until the bot is built. Sign it from the build capture.

---

## 6b. Incumbent benchmark — re-opened pre-lapse build (1)

### INC-01 — `IC-SPX-Fortress-Unstopped`   ✅ SIGNED 2026-08-17
Authored and signed under `R-2026-08-17-UNSTOPPED-REOPEN` + `R-2026-08-17-UNSTOPPED-REOPEN-A1`.
Slot accounting net zero — funded by PR-23's retired slot (`R-2026-08-17-PR23-RETIRE`).

```
ID               INC-01
BOT              IC-SPX-Fortress-Unstopped   BOTfw5TkkCRF3317787955825912621
DISPOSITION      re-opened pre-lapse build — REMOVED from build-plan §2 Group A by
                 R-2026-08-17-UNSTOPPED-REOPEN (that row amended inline, not deleted)
ROLE             SIGNED INCUMBENT BENCHMARK. The only pre-lapse build live. Pre-registered as the
                 comparator for whether post-lapse builds beat what already worked.
                 COMPARISON METRIC: per-leg R vs the GF arms and IC-SPX-FastPT25-S2-130PM.
STRATEGY IDENTITY
                 `disableExits: 1` IS THE DESIGN — not a defect, not a toggle left off. Any config
                 edit ends incumbent status and requires a fresh ruling. THERE IS NO "SMALL FIX" ON
                 THIS BOT. Its value is the untouched record; an edited incumbent is just another
                 new bot.
CLOSE MECHANISM  ⭐ HOLD TO EXPIRATION, SAME DAY. Established from the 2026-08-17 capture, not
                 assumed:
                   · Exit Options: `disableExits: 1`; the open action's exits bundle reads `None`.
                   · `Fortress-Mon-S2-Cleanup`  — per-bot state "Automation is off".
                   · `Defang-Mon-S2-StrikeTouch` — per-bot state "Automation is off".
                   · Entry series `{days:0, compare:"exact"}` = 0DTE, so expiry is same session.
                 With AUTOS on, the ONLY automations that run are the two scanners. Nothing closes
                 a position except expiration. Both close-capable monitors exist but are disabled
                 on this bot — that disabled state is what makes it "Unstopped".
ENTRY (recorded, NOT edited)
                 Scanners `Fortress-Scan-Put` / `Fortress-Scan-Call`, after 1:30pm, Range075
                 (±0.75% since previous close), an `FOMC Meeting today` gate, and a per-side
                 "exactly 0 open positions" re-entry gate. Short leg `legpctprice pct=0.75`,
                 `filter minPrice 0.08`, price `75% of bid/ask` SmartPricing `speedy`,
                 size `Up to $5,000 risk` (draw), NOT a fixed contract count.
SHARED-AUTOMATION SURFACE
                 `Defang-Mon-S2-StrikeTouch` (`RTfw5TkkCRF3317787955826108344`, `sharing:1`) is
                 shared with **`IC-SPX-Fortress-Defang`** — identified from that bot's own settings
                 page, not inferred from the name. It is ON there and OFF here: sharing couples
                 DEFINITIONS, not execution. ⛔ RECORDED EDIT-FROZEN: any future edit goes via
                 `/bots/automations` only and writes into the archived Defang's config too. Flag
                 before anyone touches it.
RECORD AS SIGNED (pre-lapse, earned under the captured config)
                 closed P/L $2,350 · 26 closes (16W / 7L / 3 scratch) · win rate 69.57%
                 · profit factor 6.222 · allocation $50,000 · posLimit 2/2 · account sim (paper)
CONFIG HASH      Capture file `data/captures/unstopped-reopen-capture-2026-08-17.txt`
                 sha256 91e2076f94a3f8ee2a03ee8298a6dd67756a4eb092437907d1fe62597b03dd82
                 Four automation hashes, formula sha256(JSON.stringify({name, inputs, root})):
                   Fortress-Scan-Put         v4 sharing0  01f37cdd96b4b09e2613dab1bc1c5395f78615d914c3b23e6d23b486cd29fe67
                   Fortress-Scan-Call        v4 sharing0  c0dba2f5dc40f1be48df968f794dc264cd44ee6321e4dc4bcaa6d5f0e7211e02
                   Defang-Mon-S2-StrikeTouch v5 sharing1  291e05ad09c2f6f801a7dcab0a121d503525fb6c015e27763cca3effa20155b6
                   Fortress-Mon-S2-Cleanup   v2 sharing0  a3f0ada0180311856db3fdc4c214e1f1f19c1f954910acad8aaa3d65e5522413
                 All four last written 2026-05-14 — untouched for three months.
SAMPLE           BENCHMARK, NOT EXPERIMENT. Interim read at n=15 NEW closes.
REVIEW DATE      n=30 new closes or 2026-11-30, whichever comes FIRST.
KILL CRITERION   (a) new-sample profit factor < 1.0 at n ≥ 15; OR
                 (b) ANY hash drift from the signed capture above → AUTOS OFF IMMEDIATELY and
                     escalate. NO DIAGNOSIS WHILE ARMED.
LAYER 2          ⚠️ OUTSTANDING — top-of-brief until confirmed. As amended by
                 R-2026-08-17-UNSTOPPED-REOPEN-A1, the first position's Trades list must show:
                   (a) NO Exit-Option rows — the inverted-check class used for PR-01's Day-0
                       verification; and
                   (b) a close consistent with the documented mechanism = closed BY EXPIRATION,
                       with no Cleanup and no StrikeTouch close row.
                 Because entries are 0DTE, both legs of this check resolve the same session.
SIGNED           2026-08-17 · ANDY — in-session, under R-2026-08-17-UNSTOPPED-REOPEN and its
                 AMENDMENT 1. Signed BEFORE arming, per the ruling's capture → sign → arm order.
```

> ⚠️ **Observation recorded at signing, NOT acted on and NOT ruled.** This bot's short leg is
> `legpctprice pct=0.75` — the very method ruled unable to adapt for the GF family earlier the same
> day (`R-2026-08-17-GF-ENTRY-METHOD`). Yet it earned 26 closes at profit factor 6.22 on SPX
> pre-lapse, while PR-01 — same symbol, same `pct=0.75`, same `75%/speedy` pricing, same
> `$5,000 draw` sizing — reportedly never fills its call side now. Same config, different eras.
> That points at a REGIME or market-data change rather than the config, and it bears directly on
> whether delta was the right fix. It is logged here as a live tension for the delta sample's read;
> **no edit follows from it** — the CONSTRAINT holds absolutely on this bot.
>
> ### 🔮 PRE-REGISTERED INTERPRETATION — recorded 2026-08-17, BEFORE any of it resolves
> Ruled by Andy the same day, under `R-2026-08-17-GF-ENTRY-METHOD` and this card. Written down now
> precisely so it cannot be fitted to the outcome later.
>
> **THE READING.** The method ruling predicts that fixed-% strike placement works only when
> volatility is high enough that blind placement lands in tradeable premium. **Unstopped pre-lapse,
> PR-01 now, and GF's 1-in-3 fire rate are ONE CURVE AT DIFFERENT VOL** — not three separate
> defects. High vol: 0.75% of spot carries real premium, so the pct bots fill (Unstopped, 26 closes,
> P-factor 6.22). Low vol: the same blind offset lands outside tradeable premium, so they starve
> (PR-01's call side; GF firing 1 session in 3 even after the tune to 0.4%).
>
> **SIDE PREDICTION 1 — falsifiable, logged daily.** In the current quiet regime **INC-01 may rarely
> fire**. A no-fire day from Unstopped is *evidence FOR* the regime reading, replicated on an
> INDEPENDENT bot (different symbol scale, different sizing, different era of build). Its
> fire/no-fire is therefore logged DAILY alongside the GF decision capture — a quiet Unstopped is a
> result, not a malfunction, and must not be diagnosed as one.
>
> **SIDE PREDICTION 2 — the disconfirming test.** If the regime turns per **B3**, the pct bots
> should RESUME FILLING. **If they do not, the regime explanation weakens and the method-only
> explanation strengthens.** That is the outcome that would falsify the reading above; it is named
> here in advance.
>
> **THE DELTA RULING STANDS UNDER EITHER OUTCOME** — delta adapts in both regimes, pct in only one.
> No result from these two predictions reopens `R-2026-08-17-GF-ENTRY-METHOD`.
>
> **CONSEQUENCE ACCEPTED, CARD UNCHANGED.** INC-01's n=15 interim may accrue slowly, or very slowly,
> if prediction 1 holds. **Review dates stay as signed** (n=30 or 2026-11-30, whichever first). Slow
> accrual is not grounds to retune, resize, or re-scope this bot — see STRATEGY IDENTITY above.
