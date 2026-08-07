# Exploratory ops bots — design

*Written 2026-08-07. **DESIGN ONLY.** Nothing here is built, signed, or authorized. No OA action was
taken while writing it — the account is untouchable pending OA's roster restore (`state.md`,
2026-08-07 incident block). Every build step is gated on **two** things: the restore landing, and
Andy ruling the three slots in §3.*

---

## 0. What this document is

### 0.1 Provenance — the task, verbatim

`session-log.md` 2026-08-06, *"Tracker: new Phase-4 group 'Exploring test bots'"*, recording Andy's
instruction:

> *"create a few bots that fire on every day, and usually trade so we can learn more about the
> mechanics and operations and testing of how OA fully operates."*

The tracker item recorded the intent as *"learn OA by OPERATING it daily rather than probing it
once"*, the design as *"1-lot, deliberately high fill probability, so a no-trade day is itself a
signal, and explicitly **not** a research arm — no hypothesis, no ranking, no performance number
ever read from them"*, and named the three constraints it collides with — slot budget,
pre-registration, ledger contamination — plus two open sub-questions (paper vs live-tiny; their own
Bot Group). §3 below is those five items, presented as ruling slots.

That entry closes: *"**Not done** — Nothing built in OA. No count, no names, no spec — this is a
checklist entry, not an authorization."* This document is the spec. It is still not an
authorization.

### 0.2 Evidence conventions

Every claim about an OA control below carries its confirmation inline. Tiers follow
`oa-platform-reference.md` §0.2. Nothing is asserted from a screen that was not opened —
`CLAUDE.md` §5: *"Inference from absence is never an evidence-backed correction."* Every mechanic
specified in §2 is expressible in a control confirmed **[FIRST-HAND]** or **[DOCUMENTED]**, and
nothing in `oa-platform-reference.md` §11's not-expressible list is used.

### 0.3 ⛔ The finding that reshaped this design

The first draft of §2 was three bots justified as *"a bot that enters and exits every session
exercises the whole chain."* One adversarial subagent was run against it. **Most of that draft did
not survive**, and the failures were of one kind: the bots generated **activity** where the claim
required an **observation**, and the readout surface either did not exist, was already answered, or
could not discriminate the alternatives. Nine claims were fatal, ten more had to be narrowed. The
full list is §5; it is recorded rather than tidied away because the pattern matters more than the
individual claims.

The design conclusion that survived is narrower and, I think, more defensible:

> **⭐ Daily trading is the precondition, not the instrument. The instrument is a bot that trades
> daily AND may be freely mutated — and the mutation schedule is what converts activity into
> observations.**
>
> Every plan bot and every Track B arm is **frozen by matching**: `greenfield-family-spec.md` §5's
> per-bot table is *"identical on every arm"*, `build-plan.md` §5 sets sizing once, and
> `day0-session-pack-2026-08-07.md` **A-12** forbids editing a signed arm to close an observation —
> *"DO NOT EDIT A SIGNED ARM TO CLOSE AN OBSERVATION… Put it to Andy: run C10 on an instrument
> OUTSIDE the tournament, or leave C10 OPEN."* The fleet currently has **no such instrument**, and
> A-12 explicitly routes standing one up to Andy: *"Standing up a separate canary is a plan
> question."*
>
> That is the gap. Not "we need more activity" — we need a bot whose config is allowed to be the
> variable.

This also relocates the value. A bot that merely trades daily duplicates **PR-20**, the signed 1-lot
canary (`profits 0.05` + `smprofits speedy`, `greenfield-family-spec.md` §4.4), which
`post-u1-package-2026-08-07.md` already calls *"the fleet's only forward exit-engine detector"*.
Duplicating it buys nothing. §2 therefore specifies nothing that PR-20 already does.

---

## 1. The unknowns catalog

Harvested from `state.md`, `day0-session-pack-2026-08-07.md` (**re-read at 2333 lines** — its §0.0
was added 2026-08-07 and carries 25 amendments; earlier line references in this folder are stale),
`oa-platform-reference.md` §6/§9/§11/§13/§14, `oa-ops-runbook.md` §7, `greenfield-family-spec.md`
§10 Phase 0, `post-u1-package-2026-08-07.md` §4, `research-loop-fix-spec-2026-08-07.md`, and
`pre-registration-ledger.md` §8. Deduplicated across files.

Three classes. **Class Q** is covered by a one-shot observation already queued — say where, and stop.
**Class S** is one-shot, *not* queued, and blocked only for want of a bot somebody is allowed to
break. **Class R** is the exploratory bots' actual niche: it needs repeated live operation, and no
one-shot probe reaches it.

### 1.1 Class R — needs REPEATED live operation

| ID | The unknown | What settles it | Why one shot is not enough |
|---|---|---|---|
| **R1** | **Is re-applying `Update Position Exit Options` side-effect-free?** §6.5 calls it *"the highest-value unverified operation"*; §9 check **#5** is the last open item of the 2026-08-04 Tier-2 pass. | Re-applying against live positions and reading the Trades list for spurious orders. | The property asserted is *"without generating spurious orders"* — **a rate, not a fact.** One clean re-apply is consistent with a defect that fires intermittently. It gates the re-assertion watchdog, which `oa-ops-runbook.md` §7 calls *"the architecturally correct fix for panel-vs-position drift"*, so the confidence bar is high. ⭐ **The single strongest case in this catalog.** |
| **R2** | **C10 — the unit of `dstop` (`Stop Loss $`).** Blocks ARM-B1; `comparative-machinery-spec.md` §671 states the axis as *"`dstop` per contract / position / leg"* — **three-way, not two.** | A `dstop` STOP firing at a contract count recorded *before* the position opened, on an instrument outside the tournament. | **A-12(b):** *"At 1 contract per leg, per-leg count = 1, so `−$100` and `−$100 × 1` are the same number — the two primary branches become indistinguishable."* And A-12's own instruction: *"do not fit a basis to one data point."* One firing at the wrong lot size settles nothing; a repeatable instrument at the right lot size settles it and then **confirms** it. §2.2 derives the required count. |
| **R3** | **`dprofit` (`Profit Taking $`) — does it fire, and on what unit?** Confirmed to EXIST first-hand (§6.1a row 2, `dprofit`); it was **absent from the entire 100-page docs corpus** (Phase 6, R-13) and has never been exercised anywhere in this folder. | A `dprofit` target firing at a known contract count. | Same three-way unit ambiguity as R2, same reason. **Queued nowhere.** It gates `hedge-research.md` §9's fixed-$ stop rungs, which §9 check #10 declared *"buildable"* on the strength of the control existing — existence is not behaviour. |
| **R4** | **C9's surviving limb — does the `Position closed` trigger fire on a close by an EVENTS-class automation, and by the account-level ITM action, or only by Exit Options?** | A `Position closed` witness on a bot where each close class can be made the **only** close class, in turn. | `greenfield-family-spec.md` Phase 0 C9: *"NOT ANSWERABLE IN THE UI — DAY-0 BEHAVIOURAL READ… The closepos trigger's settings expose only a `Position Type` filter — there is **no "closed by" filter**."* Three close classes cannot be isolated on one day; isolating them is a **phase schedule**, not an observation. |
| **R5** | **The bot log's `Load more` stall** — is it bounded by row count, elapsed time, or session? §9 check #7: *"at ~229 rows in, stopped yielding while still displaying the button."* | A bot whose log accumulates past ~229 rows, paged repeatedly across days. | The stall is a function of accumulated volume, which only exists after days of it. It constrains every liveness design that looks back more than the 3-week filter. ⚠️ **This is the narrowed survivor of a claim that died** — the *retention window* is already answered (§1.2 Q7). |
| **R6** | **`maxexits` (`Maximum Exit Options Close Attempts`)** — read `0` = Unlimited, *"a single switch that can silently cap every bot's ability to close"*, and §13.2 notes it *"appears in no other document here."* | A bot attempting enough closes per day to reach a non-zero setting, with the setting deliberately lowered. | Needs a sustained daily close-attempt rate to have anything to cap. ⛔ **The setting is ACCOUNT-WIDE** (§13 preamble: *"it overrides nothing per-bot"*), so the probe is fleet-scoped and must be scheduled and ruled, never improvised. |
| **R7** | **Which error types count toward the Excessive Errors Failsafe.** §4.5: the page *"refers specifically to 'automation error', which suggests not all error types count… which are excluded is [DOCS-SILENT]."* | Generating errors of known kinds on a disposable bot and reading the counter. | It is an **enumeration** — one error type tells you about one error type. The fleet has tripped this failsafe twice (Mar/Apr 2026, on entry scanners), so the taxonomy is load-bearing. ⛔ Gated: deliberately breaking a bot is Andy's call. |
| **R8** | **What a dead exit engine looks like in the DATA** — the ledger rows and bot-log rows a bot with `EXIT OPTIONS` OFF produces, as a labelled negative example for calibrating `EXPIRY_RATIO_FLIP`, `PT_NEVER_FIRES` and PR-20's PT-fill detector. | A declared, dated window with the per-bot `EXIT OPTIONS` toggle OFF on a bot that otherwise closes daily, then ON. | The detectors are validated today only against the **frozen v1 fixture** (`execution_audit.py` V1/V15/V18). A forward-labelled positive from a *known* dead state does not exist and cannot be manufactured by a one-shot read. ⛔ **NARROWED — see §5 O10:** this settles the observable *signature*, **not** §10's causal claim about the June lapse, which `day0-session-pack` restricts to the nine lapsed bots: *"the clones and fresh builds were never lapsed and cannot test it."* |
| **R9** | **Does the account-level ITM action produce a Trades-list row at all, and is its Automation Log link ABSENT?** | Positions allowed to reach expiration ITM under `itmpaper = market`. | ⛔ **NARROWED — the LABEL half is already answered NEGATIVE.** U-1: rows carry *"no per-row pricing-mode label and no memo field"*, and `post-u1-package` §4 rules the ITM limb *"UNCHANGED, AND NOW PERMANENT… There is no route to labelling an ITM-action row."* What survives is whether a row appears and whether the Automation Log link is **missing** — an account-level action is not an automation, so its absence is the only candidate discriminator left. Distinguishing *"absent"* from *"absent this once"* takes several. Every production bot is designed to exit at 15:50 and never produce one. |

### 1.2 Class Q — a one-shot observation already covers it. Do not build for these.

| ID | The unknown | Where it is already queued |
|---|---|---|
| **Q1** | **D3 / DST** — does `ntime=1552` fire at 15:52 ET? | `day0-session-pack` **Step 5a**, with a mandated re-run *"on the first trading day after the November EST transition."* It *"reproduces on all six arms"* — the object is already attached by `rid` to all seven, so a TESTOPS copy adds nothing. ⚠️ And the risk direction inverts: the dangerous reading (literal EST ⇒ 16:52 ET) is falsified or confirmed **on day 1, in EDT**; November is the safe direction. |
| **Q2** | **D4 — the lapse mechanism verdict.** | **Step 6a**, *"Run ONCE, on THE NINE leave-in-place bots ONLY."* Structurally unavailable to any new bot. |
| **Q3** | **The 15:50/15:52 attribution.** | **Step 6**, and it is **not settleable without Template V2**: *"WITHOUT V2 THEY ARE THREE MARKET ORDERS IN TWO MINUTES WITH ONLY MEMO STRINGS BETWEEN THEM."* TESTOPS does not fix this and must not claim to. |
| **Q4** | **The Automation Log link's target for an Exit-Option close.** | Pack S2 close-out item 4 — *"~5 min, NOT a numbered step — run it opportunistically during Step 6."* `post-u1-package` §4.6: *"Two ~5-minute Day-0 checks are worth more than 126 days of capture."* |
| **Q5** | **The no-touch toggle read.** | **Step 2c**, strictly one-shot and *"not recoverable afterwards"* — and now partly spent by the wipe (**A-09** adds a `CONFOUNDED — RESTORE` branch). |
| **Q6** | The **one-shot half** of R1 — a single re-apply read. | Tier-2 **§9 #5**, pack S2. R1 is the *rate*; this is the *first datum*. |
| **Q7** | **The automation-log retention window.** | ⛔ **ANSWERED 2026-08-04**, §9 check #7: the date *filter* reaches 3 weeks of weekdays; stored *data* reaches `Mar 16, 2026`, ≥141 days. *"Retention is not the constraint — the filter is."* Nothing left to measure. R5 is what survives. |
| **Q8** | **The ITM-action row's LABEL.** | ⛔ **ANSWERED NEGATIVE** by U-1, and ruled **PERMANENT** by `post-u1-package` §4. |
| **Q9** | **`itmlive` = `market`.** | A Day-0 **write** and hard gate (`itmlive` deliberately at `auto`). No paper bot touches it; nothing here reduces that risk. |

### 1.3 Class S — one-shot, NOT queued, blocked only for want of a disposable bot

These do not justify daily operation. They justify **owning a bot you are allowed to break**, and
they should be run in the first week and then retired from the list.

| ID | The unknown | Status in the folder |
|---|---|---|
| **S1** | Does a **template store a REFERENCE** to the bot's live automation objects? (`oa-ops-runbook.md` §7 successor check; §2.3 records the template's rows carrying `rid=RTfw5TkkCRF2717857919585272551`, *"the same object id as the bot's live ScannerA"*.) | `state.md`: *"NOT RUN. It needs either a template saved from a delete-list bot… or a production bot, which this session was barred from."* ⭐ A TESTOPS bot **is** that substrate. |
| **S2** | **C0a** — can an Exit-Options input be promoted to a **Bot** Input? | §5.2: *"the BOT-INPUT tier has never been observed… **C0a can stop that architecture outright.**"* Marked PASSED in the 2026-08-05 Phase-0 pass; a free substrate makes it cheap to re-confirm on a bot whose hash nobody signed. |
| **S3** | **Do tags persist across a clone?** | §5.3: [DOCS-SILENT], and *"directly relevant to the clone ritual"* — two clones (PR-02, PR-04) are still outstanding. |
| **S4** | **Does an ungrouped bot appear in an all-groups export?** | Memo **N-5**, **unobserved**, and *"an ungrouped bot silently missing from the export would erase the family from the ledger."* One bot left ungrouped for one day settles a ledger-integrity question. |
| **S5** | Is a **plain, non-armed trailing stop** expressible (may `tstop.target` be blank)? | *"Whether a plain non-armed trail is expressible was NOT observed; do not assume it."* Bounds PR-16's scope. |
| **S6** | Does **§8.3's Button test-fire** proof work, and what does it produce? | `Button` confirmed to exist first-hand (*"`Button` — Add a button to bot dashboard — 0/10"*, a tenth trigger type absent from OA's documented list) and **never used**. ⛔ **NARROWED — see §5 O22:** §8.3's proof is per-bot, so this is a **rehearsal of the technique**, not an unblocking of anyone else's verification. |
| **S7** | Can a **`Touch` on one spread close its sibling?** | Unresolved twice in §6.2. Not blocking (C8 ruled build-without-sibling-close 2026-08-06), still open. Needs a live condor — **neither bot in §2 is a condor**, so this is **not covered**. |

### 1.4 ⛔ Unknowns this catalog does NOT cover, stated so the gap is not mistaken for coverage

- **Per-side exit fire-rate asymmetry** (§6.1: *"the per-side fire-rate assertion still has to run"*).
  Both bots in §2 are **single-sided put spreads**. Not covered; it rides on the family.
- **Anything requiring a condor** — S7, sibling-close timing, the `:00`/`:01–:02` gap test of §8.3.
- **`itmlive`, `maxexits` as configured, the Bot Schedule, notification settings** — all
  **account-wide**. A per-bot instrument can *detect drift* in them; it cannot *test* them without
  changing behaviour for every bot on the account.
- **Anything about fill quality.** See §4.

---

## 2. The test-bot designs

**Two bots, not three.** The third died: its claims were either duplicates of PR-20 or defeated by
paper-fill semantics (§5 O2, O29). Two is what the surviving unknowns support.

### 2.0 Common configuration

Identical on both, and every value cites its confirmation.

| Setting | Value | Confirmation |
|---|---|---|
| Account | **Paper** | §3.4 recommends it; the fleet is entirely paper at Day-0 |
| Underlying | **QQQ** | Cross-readable with the family (`greenfield-family-spec.md` §2); 0DTE available daily |
| Structure | **Short put vertical, $2.00 wide** — a single spread, **not** a condor | `hedge-research.md` §11 ($2-wide most hedgeable on QQQ); a vertical is **1 position** and **2 legs**, which keeps R2/R3's unit arithmetic unambiguous. An IC would be 2 positions / 4 legs (§3 [PROJECT-RULE]) |
| Expiration | `exactly 0 days` | Pilot's verified tree, `greenfield-family-spec.md` §4.1 |
| Size primitive | **fixed CONTRACT COUNT** | ✅ Phase-0 **C4** ANSWERED 2026-08-05: *"YES, a fixed CONTRACT COUNT is selectable. The Open Position action's Position Size defaulted to `1 contract`."* Corroborated first-hand in the Phase-A build: `amount:{"type":"quantity","quantity":1}` |
| Entry pricing | **SmartPricing `normal`**, Final Price `pct` = `100` | ⛔ Market is banned on **entries and exits** (§7, amended 2026-08-06 on Andy's *"amend the plan"*). Control read first-hand: `<input name="pct" min="50" max="150" value="100">` |
| Minimum credit | `Mid price is between $0.05 – (no max)` | The pilot carries `$0.08`; loosened deliberately for fill probability. ⚠️ **This is a gate** — see the no-trade-day check |
| Scan Speed | **Every 1m** | §3: default 15 min, *"down to 1 min"* |
| Day Trading | **Allowed** | §9 check #9: two-item picker, `0` Allowed / `1` Blocked |
| Bid-Ask Guard (`chbidask`) | **unchecked / empty** | §6.3: on, it *"suppresses exits silently"*. Off, deliberately, recorded as a decision |
| PDT checkbox (`chposLimitDay`) | **unchecked** | §6.1a row 11: checked, it *"delays closes by ≥1 day"* — total failure on 0DTE |
| Bot Group | **`Lab`** | §3.5 — the pillar container that already exists |
| Bot Tags | `experiment` · `ops` · `lab` · `pr nn` | ⛔ OA normalises tags lowercase, non-alphanumeric → space; `PR-NN` is **not expressible** as a tag (ruled 2026-08-04) |
| `AUTOMATIONS` | **OFF until every §3 ruling lands** | `pre-registration-ledger.md` header: *"No entry, no restart"* |
| `EXIT OPTIONS` | **ON** | Per-bot, documented on three surfaces (**OA-0896**), stored as `disableExits` |
| Library sharing | ⛔ **NONE. Every automation is a per-bot COPY.** | **OA-0682**: *"Any changes made to an automation will flow through anywhere the automation is used, including other bots."* Attaching the family's `GF-Backstop-1552-FlatClose` would make the Library read *"8 bots"* and put all seven arms one edit from a fleet-wide change, and would invalidate its A7 payload-hash baseline. See §5 O25 |

**Entry rule shape, both bots** — deliberately loose, so a no-trade day is a signal:

```
Loop QQQ
 └─ Current market time is after 9:45am                      [General decision]
     └─ YES → Open QQQ Short Put Spread
```

⛔ **No Range075. No upper time bound. No IV filter. No `postagtoday` re-entry gate.** Each omission
is deliberate and each is a departure from the family's tree (`greenfield-family-spec.md` §4.1),
which carries all four. **The `postagtoday` gate is omitted specifically because it is a
one-per-day enforcer, not a re-entry permitter** — *"enforced twice over: by the `Bot opened a
position with tag <side> today → NO` gate… and by the 2/2 limits."* Carrying it would have made the
position limits dead configuration (§5 O1, which killed the first draft's multi-cycle design).

### 2.1 `TESTOPS-LAB-OPS` — the probe substrate

**Role.** The bot the account does not have: one that trades every session and may be reconfigured
at will. It is the vehicle for **R1, R4, R5, R6, R7, R8** and all of **Class S**.

| Field | Value |
|---|---|
| Short put | `0.50% below underlying price` |
| Long put | `$2.00 below short put leg` |
| Size | **1 contract** |
| `posLimitDay` / `posLimit` | **5 / 5** |
| Exit bundle, base | `profits` = **0.25** (25% of credit), `smprofits` = `speedy` · `expdays` = `0.01` (15:50), `smexpdays` = `speedy` |
| Extra automations (all per-bot copies) | (i) `Position closed` → **Untag** `pc fired`, then **Tag** `pc fired` — the witness · (ii) `Button` → Open Position — §8.3 rehearsal · (iii) `Repeating`, `Market Time (EST)` `Custom` **15:52**, Mon–Fri, holidays skip → flat close, `Market` — the Events-class close |

**Why `profits` = 0.25 and not 0.05.** `profits 0.05` + `smprofits speedy` is **PR-20 byte for
byte**. 25% still fills on most 0DTE sessions and is not a duplicate (§5 O29).

**Why the witness untags before it tags.** §5.3: bot tags *"do not change state and remain applied
to the bot unless reset or untagged by the user."* A bare Tag action is a **saturating latch** — one
fire and every later close is indistinguishable (§5 O23). Untag-then-Tag makes each firing produce
its own pair of **Event rows in the bot log**, which is the real per-fire readout, at the row
`title` attribute's minute granularity. §4.4: bot logs *"record NON-actions"* and are the only
surface that distinguishes a gated bot from a dead one.

**⚠️ No event-loop exposure.** The `Position closed` automation only tags. §4.7's documented loop
class requires a close that triggers an *open*; there is none here, and the 5/5 limits are the
platform's own stated safeguard against it.

**Phase schedule — this is the instrument, not the config.** Each phase is dated in the bot's
ledger entry before it starts (guardrail **G8**, §3.3).

| Phase | Configuration change | Answers |
|---|---|---|
| **P0** | As built. Run 5 sessions untouched. | Baseline: does it fill daily; what the three close classes look like; **S1–S6** run opportunistically |
| **P1** | Re-apply the exit bundle to a live position every session, and again mid-session. | **R1** — spurious orders, over ~20 re-applies rather than one |
| **P2** | Remove `profits` and `expdays`, leaving the 15:52 Repeating flat close as the **only** automation-class close. Far-OTM strike for the window. | **R4** limb 1 — does `Position closed` fire on an EVENTS-class close |
| **P3** | Remove the 15:52 automation too. Strike moved to ~0.10% OTM to make ITM expiry likely. | **R4** limb 2 (ITM action) and **R9** — does an ITM-action row exist, is its Automation Log link absent |
| **P4** | Restore P0. Set **`EXIT OPTIONS` → OFF** for a declared window of N sessions, then ON. | **R8** — the labelled dead-engine signature |
| **P5** | Page its own bot log past ~229 rows, repeatedly, across the accumulated window. | **R5** — the `Load more` stall's boundary |
| **P6** | ⛔ **Andy-gated, account-wide.** Lower `maxexits` from `0`; then deliberate errors to enumerate the failsafe taxonomy. | **R6**, **R7**. Not run without an explicit ruling — both change behaviour for every bot on the account |

**Daily capture must record** — beyond the standard per-bot capture (`capture-architecture-2026-07-30.md`):

1. The declared **phase ID** for the session. Without it, every observation is uninterpretable and
   §5 O27's contamination objection stands.
2. Entries **attempted vs filled**, and every **non-fill** — required by the Decision-5 mitigation
   (*"log non-fills so the bias is measurable"*), and here it is also the fill-probability metric.
3. Per exit: `(exit_ts, fill_price, bid→fill pair, close class as configured)`. ⛔ **`row_type` is
   assigned by a deterministic rule declared in writing beforehand and executed by code, never by
   hand** — `post-u1-package` §4: *"A degraded capture assigns `row_type` from close time. It does
   the thing the spec forbade."*
4. Bot-log **row count** and every row's `title` attribute (the visible date group header is
   unreliable — *"on one bot it did not render at all, on another it re-rendered mid-scroll and
   changed value"*).
5. The witness's Untag/Tag Event rows, with timestamps.
6. Screenshots of **both** dashboard toggles. §6: *"A bot with `AUTOMATIONS` OFF is NOT inert if it
   holds positions."*
7. The account-wide settings that could have moved under it: `maxexits`, `itmpaper`, `itmlive`,
   `scanstart`/`scanend`/`exitstart`/`exitend`.
8. ⛔ **A NO-TRADE-DAY ROW IS WRITTEN AS A ROW**, never as a gap.

**No-trade-day check.** Expected every session: **≥1 entry** and **≥1 close**.

- 0 entries → the scanner did not run, or a limit tripped, or the account changed. §3's 2026-08-04
  append gives the discriminator: *"If a bot has reached an allocation or position limit, the scanner
  turns off **and a warning is displayed**"* — a detectable signal.
- Entries but 0 closes → exit-engine suspect. **RED**, and unlike `SILENT_BOT` this one is
  actionable, because the bot has no strategic gate that could legitimately have declined.
- ⚠️ **The claim must be stated carefully.** The entry is **not** ungated: the `$0.05` minimum credit
  is a gate, strike availability is a gate, and *"the 'Opportunity is available' check fails without
  alerting"* [**OA-0382**]. So zero activity is **narrower** than ambiguous, not unambiguous — and
  realising even that requires code `execution_audit.py` does not have today (§5 O19).

### 2.2 `TESTOPS-LAB-DSTOP` — the dollar-unit instrument

**Role.** The instrument **A-12** routes to Andy. It answers **R2** and **R3** — and it is the one
design decision in this document that is quantitative rather than editorial.

| Field | Value |
|---|---|
| Short put | `1.50% below underlying price` — deliberately **far** OTM |
| Long put | `$2.00 below short put leg` |
| Size | ⭐ **3 contracts** — see the derivation |
| `posLimitDay` / `posLimit` | **1 / 1** |
| Exit bundle, **phase D1** | `dstop` = **−60**, `smdstop` = `speedy`. **No PT. No time exit. No backstop.** |
| Exit bundle, **phase D2** | `dprofit` = **60**, `smdprofit` = `speedy`. **No stop. No time exit.** |
| Extra automation | `Position closed` → Untag/Tag witness (a second copy) |

**Both dollar controls are confirmed to exist first-hand** — §6.1a rows 2 and 5, `dprofit` and
`dstop`, closing §9 check #10: *"all three EXIST."* Both carry their own SmartPricing sibling
defaulting to `normal`, never `market` (✅ Phase-0 **C3**, 2026-08-05: *"`smprofits · smdprofit ·
smprice · smstoploss · smdstop · smtstop · smtouch · smexpdays · smxevents · smepsdays`, each
defaulting to… `"smart":"normal"`"*), so §7's ban is not tripped.

#### ⭐ Why 3 contracts — the derivation

Let `D` be the typed dollar value, `n` the contracts **per leg**, and `L` the legs (`L = 2` for a
vertical). Four bases are plausible for what `D` is measured against, and the folder does not settle
which:

| Basis | Threshold |
|---|---|
| B1 per **position** | `D` |
| B2 per **leg** | `D × L` = `2D` |
| B3 per **contract per leg** | `D × n` |
| B4 per **total contract** on the position | `D × n × L` = `2nD` |

| `n` | B1 | B2 | B3 | B4 | Discriminates? |
|--:|--:|--:|--:|--:|---|
| 1 | `D` | `2D` | `D` | `2D` | ⛔ **B1=B3, B2=B4** — two values for four bases |
| 2 | `D` | `2D` | `2D` | `4D` | ⛔ **B2=B3** |
| **3** | `D` | `2D` | `3D` | `6D` | ✅ **all four distinct** |

**`n = 3` is the minimum count that separates all four candidate bases on a 2-leg vertical.** This
goes past A-12, which requires recording *"BOTH numbers — per leg and total"* but does not derive a
count at which the reading can discriminate; at A-12's own prescribed *"EXACTLY 1 CONTRACT"* it
cannot, which is the defect A-12(b) itself names.

**Why `D = 60`, and why far OTM.** Max loss at 3 contracts on a $2-wide vertical is
`3 × ($2.00 − credit) × 100 ≈ $555`. All four bands must be **reachable** (`6D = $360 < $555` ✅) and
must be **resolvable at the 1-minute Exit-Options cadence**. In mid-price terms the bands sit at a
mid rise of `$0.20 / $0.40 / $0.60 / $1.20` above the entry credit — gaps of ≥ $0.20. A near-ATM
0DTE spread traverses $0.20 of mid between two consecutive minute checks, in which case two bands
trip on the same evaluation and the reading answers nothing (§5 O21). **Far OTM makes the mid move
slowly enough to resolve the bands** — and it is the same choice that stops the stop pre-empting the
expiry observation (§5 O16). Two objections, one fix.

**Why paper HELPS here, unusually.** Exit Options evaluate **mid-price** [**OA-0872**] and paper
*"simulate fills based on current live market pricing, typically at or near the mid price"*
[**OA-0930**]. So the realised fill sits close to the threshold that fired it, and slippage does not
obscure which band it was. On a live account it would. ⭐ **For R2/R3 specifically, paper is the
better instrument, not a compromise.**

**Unknowns answered per day of operation.** On a stop-trip / target-hit day: one datum on the
basis, with the contract count recorded before the position opened. On a quiet day: the position runs
to expiration → OTM expiry (worthless; *"OTM positions are never closed"* [**OA-0236**]) or ITM →
the account-level ITM action at 15:50 → a second reading for **R9** and **R4** limb 2. The two
outcomes are complementary, and the far-OTM strike sets the mix toward expiry days.

**Daily capture must record**, in addition to §2.1's list, and **before the position opens**:
`dstop`/`dprofit` **as typed**, contracts **per leg**, **total** contracts on the position, and the
legs count. A-12: *"THAT MOMENT EXISTS EXACTLY ONCE. DO NOT LET IT PASS UNRECORDED"* — except that
on this bot it exists **daily**, which is the entire point. Then the realised close: which band the
implied position-level P/L matches, or **none of them**.

⛔ **Reporting rule.** `C10-UNRESOLVED` unless the same basis is reproduced on **≥3 separate firings**
and no firing lands off-basis. A-12: *"do not fit a basis to one data point."*

**No-trade-day check.** Expected every session: exactly 1 entry, and exactly one of {stop/target
fired, ITM action closed it, OTM expiry}. None of the three → **RED**. Two closes → config drift.

### 2.3 What §2 does NOT claim

Recorded here so no later reader has to reconstruct it: these bots do **not** answer Q1–Q9, do not
observe SmartPricing ladder steps or partial fills or the 2-minute order lifetime (§4), do not cover
per-side asymmetry or anything requiring a condor (§1.4), and do not settle §10's causal claim
(§5 O10).

---

## 3. The three governance constraints — RULING SLOTS

⛔ **Nothing below is decided. Each slot states the arithmetic or the text, gives a recommendation,
and stops.** `CLAUDE.md` §5: decisions that change *what gets built* require an explicit
*"amend the plan"* from Andy.

### 3.1 SLOT A — slot budget

**The arithmetic, from the numbers as they stand.**

| Quantity | Value | Source |
|---|--:|---|
| Pro plan cap | **50** active bots | `Settings → Membership: BOTS 50` |
| Complement rule | `left = 50 − ACTIVE` | [FIRST-HAND 2026-08-04] `/bots` footer read `35 active bots • 15 left in your plan`; 35 + 15 = 50. **Archived bots do not consume slots** |
| Plan bots | **≈18–20** = 4 clones + 9 untouched + 5–7 fresh | `build-plan.md` §2D |
| Track B arms | **≤8**, a separate allocation | Ruling **S-1**; *"Track B's 8 slots are Track B's"*, `n_used = 20` |
| **Governance ceiling** | **28** | `build-plan.md` §2D scoping amendment 2026-08-05 |
| Wave 1 | **22 of 50** (Track B wave-1 spend **2**) | §2D C12 discharge |

**⛔ Finding: the "6 remaining headroom slots" are not free.**

The tracker item reasoned that the ops bots *"either fit the 6 remaining headroom slots or need an
explicit 'amend the plan'."* Those 6 slots are **Track B's unspent allocation** — 8 authorized,
wave-1 spend 2, 6 remaining. Ruling **S-1** exists precisely to stop that allocation being consumed
by something else; **S-2** made the count amendment conditional for the same reason. Taking 2 of the
6 for ops bots re-creates the exact collision those rulings were written to prevent.

**Against the ceiling itself:**

```
plan bots (18–20)  +  Track B (8)              = 26–28   ← the ceiling IS this sum
plan bots (18–20)  +  Track B (8)  +  ops (2)  = 28–30
```

At the top of the plan-bot range this **breaches 28**. At the bottom it **equals** 28 exactly, i.e.
it fits only if the plan-bot count lands at 18 and never grows. **2 ops bots do not reliably fit
under ceiling 28. An "amend the plan" is required.**

**Recommendation.** Mirror what S-1 did for Track B: a **third named allocation**, not a raid on the
second.

> **`≤2 Lab ops slots`, a separate allocation. Ceiling 28 → 30.**
> Wave 1 becomes 24 of 50; full spend 30 of 50.

**⚠️ Two costs to state, not bury.**

1. **It makes C12's residual more likely to bite.** C12 was discharged on a footer read that is
   [FIRST-HAND, **UNCORROBORATED**] — *"a footer rendering `left = 50 − active` is self-consistent
   under both hypotheses"*, observed with **one** archived bot where the sweep archives **twenty**.
   Under the pessimistic reading, 30 + ~23 archives = **53 > 50**. The pre-declared reopen condition
   — *"if a bot build ever fails at the cap despite archived bots existing, C12 reopens"* — becomes
   materially likelier. 2 slots is the cost of that.
2. **The whole arithmetic is provisional on the restore.** `/bots` currently reads
   **`0 active bots • 50 left in your plan`** against an expected 41. Until OA's restore lands and
   Andy verifies the roster count, every number above describes a fleet that does not presently
   exist.

### 3.2 SLOT B — pre-registration

**The rule the class must be written against**, `pre-registration-ledger.md` header:

> *"**No entry, no restart.** A bot without a signed entry stays OFF on Day-0, regardless of how
> ready it looks… **including the nine untouched ones**, and including every Track B arm."*

**⭐ Finding: the ledger already has the pattern, and it is NOT an exemption from having an entry.**

The only exemption anywhere in that document is inside **PR-20**'s entry:

> `KILL CRITERION   None on P/L — it is exempt by design, and that exemption is stated here so it`
> `                 cannot later be mistaken for a losing bot nobody killed.`

PR-20 also writes `MECHANISM n/a — this bot is not run for edge` and `SAMPLE TARGET n/a — daily
fill/no-fill is the output` — **and still carries a full entry, a config hash, a verification
artifact and a signature line.** The document's convention is: *write `n/a`, state the exemption in
the entry, state its retirement condition — never drop the entry.*

**Recommendation.** A named class that follows PR-20's pattern exactly. Proposed text, for Andy's
signature — a new §3 roster row plus a new §2a:

> ### 📝 PROPOSED AMENDMENT — a named class for non-inferential ops bots
>
> **§3 roster, new row:**
>
> | Group | Count | Entries below |
> |---|--:|---|
> | **E — Lab ops bots** (non-inferential; separate allocation, `exploratory-bots-design-2026-08-07.md` §3.1) | **≤2** | §6a |
>
> **New §2a — Ops-class entries.** An **ops-class** bot is one run to observe the *platform*, never
> to estimate a *return*. It uses the §2 template unchanged, with three fields declared `n/a` and a
> fourth added:
>
> - `HYPOTHESIS` — an **INSTRUMENT** hypothesis, in PR-20's sense: what the bot will let us observe
>   that no other bot can. **Never a market hypothesis.**
> - `MECHANISM` — `n/a — not run for edge.` ⚠️ And, unlike PR-20, **P/L is not expected to be flat**:
>   `TESTOPS-LAB-DSTOP` loses money by design. State that in the entry so it cannot later be
>   mistaken for a losing bot nobody killed.
> - `SAMPLE TARGET` — `n/a — the daily observation is the output.`
> - `KILL CRITERION` — none on P/L, by design and stated. Killed instead on **instrument failure**:
>   no usable observation for K consecutive sessions where the cause is the bot rather than the
>   platform. Plus a hard `RETIREMENT DATE`.
> - `PHASE LOG` **(new field, ops-class only)** — every configuration change, dated, with the phase
>   ID and the unknown it targets. **This field is the class's whole justification for being
>   mutable**, and its absence is the `HedgeD` failure: an undocumented substitution at a platform
>   limit, where *"the config record and the tree agreed with each other and both were wrong about
>   the intent."*
>
> **Guardrails G1–G10 — the conditions on the class.**
>
> | | Guardrail |
> |---|---|
> | **G1** | ⛔ **Publication interdict.** No number from an ops-class bot may enter any Exp(R), any arm or variant comparison, any funding decision, any tiered T1–T5 claim, or any brief section other than the ops/mechanics section. |
> | **G2** | **G1 is enforced in code, not by intent** — §3.3's ledger exclusion. A rule with no mechanism is the failure class this project keeps re-learning. |
> | **G3** | ⛔ **Never an arm, never a control.** Ops bots enter no tournament, are matched to nothing, and are deliberately non-matched to each other. `DUPLICATE_ARM` must not scope them, and no A-series assert may read them (§3.3). |
> | **G4** | ⛔ **No shared Library object, ever.** Every ops automation is a per-bot copy. **OA-0682**: an edit *"will flow through anywhere the automation is used."* |
> | **G5** | **Paper only.** Promotion to live requires a separate ruling (§3.4). |
> | **G6** | **Sizing declared once per phase**, with the reason. `TESTOPS-LAB-DSTOP`'s 3 contracts is justified in writing by §2.2's derivation, not by preference. |
> | **G7** | ⛔ **Account-wide probes are separately gated.** `maxexits`, the ITM actions, the Bot Schedule and notification settings are account-wide; phase **P6** does not run without its own ruling. |
> | **G8** | **Every phase is declared and dated in `PHASE LOG` BEFORE it starts.** An undeclared configuration change voids that phase's observations. |
> | **G9** | **Deliberate-failure phases** (`EXIT OPTIONS` OFF; induced errors) require a named window, a named expected signature, and a restore step in the same declaration. |
> | **G10** | ⛔ **Retirement is the default.** Each Class-S unknown is struck from the bot's phase list once answered; when the phase list empties, the bot is archived and its slot returns. An ops bot with no open phase is not earning its slot. |

### 3.3 SLOT C — ledger contamination

**The problem, precisely.** `build_ledger.py` has **no bot, tag or group filter of any kind**. Its
only exclusion is the temporal cutover on `open_date`; `data/archive/` is excluded not by code but
by never being addressed — the enumerator is a **non-recursive** `glob.glob(os.path.join(RAW,
"*.csv"))`. Every export row with `open_date >= LEDGER_START` is written to `data/trades.csv`, and
`report.py` sums all of it. `report.py`'s existing group logic excludes the Archive group **from the
view, not from the ledger** — *"excluded from the working view (still exported for the ledger)"* —
so there is no group-based ledger exclusion to mirror. **The only pattern available to mirror is
`LEDGER_START`'s own**, which is a good one:

> constant + sentinel (CLI > env > module) → partition writing excluded rows to a **visible sidecar**
> with **counts** → a post-transform **FATAL** leak assertion → a **receipt contract string**
> downstream asserts read.

**⛔ And the exclusion is three-surface, not one.** Verified directly:

- `a_series.py` `_a6` (**L488–L490**) iterates **all** `ledger_rows` and flags any
  `_num(r.get("quantity")) not in (1.0, 1)`. It is **not scoped to `GF-QQQ-IC-*`**. One
  `TESTOPS-LAB-DSTOP` row at qty 3 turns **A6 FAIL** — the family's mandated sizing guard — on its
  first fill.
- `a_series.py` `_a4b` (**L467–L485**) scans **all** rows for ≥2 same-day closes within 300s of open,
  and `cfg_stop.get(bot, False)` returns **False** for any bot absent from the seven-arm dict.
  `TESTOPS-LAB-OPS` *is* that signature, so **A4b FAILs** every day it trades, with no broken link
  anywhere — permanently destroying the broken-input-link detector it exists to be.
  ⚠️ **`scripts/a_series.py` carried mtime `2026-08-07 17:22` while this document was being written**
  — i.e. the tree moved under it. These line numbers are against that version and must be re-read
  before the change is made.
- `execution_audit.py` is **FROZEN** (`v1.0.0`, sha `67a537977c5d0896`) with a pinned validation
  fixture. It must not be edited.

**Recommended mechanism — implementable as stated.**

1. **Source of truth: `data/bots_meta.csv`, a new column `ops_class`** (empty | `lab-ops`). ⛔ **Not**
   the export's `tags` string (lossy — OA normalises tags, and `build_ledger.py` treats `tags` as
   pass-through only), and ⛔ **not** the bot name, per the script's own docstring principle:
   *"CLASSIFICATION COMES FROM data/bots_meta.csv, NOT from bot-name heuristics."* ⚠️ This is a
   **schema addition** and is named as part of the ruling, matching how the missing
   `bots_config_v2.csv` `exitrate` column was *"flagged, not taken."*
2. **Partition** in `build_ledger.py` immediately after `rows = post` and **before** the condor
   pairing block — pairing assigns `trade_id` from a global counter, so excluding afterwards would
   corrupt the numbering. Write `data/ops_rows.csv` with an `OPS_NOTE` constant mirroring
   `STRADDLER_NOTE`, and add `ops_rows` to the `counts` dict.
3. **FATAL leak assertion** mirroring the pre-cutover one: if any row whose bot is in the ops set
   reaches `out_rows`, `sys.exit("FATAL: …")`. Nothing written.
4. **Receipt.** Extend `write_receipt()`'s `contract` string to name the second axis, and add
   `ops_bots` and `ops_rows` fields. Downstream scripts assert against `contract`; changing the
   partition without changing the contract is the stale-assert failure.
5. ⛔ **The FILTERED-EXPORT GUARD interaction — this sets a build-order constraint.** The guard
   computes `dropped = prior_bots − {current bots}` and shouts, because *"an export taken with any
   group deselected is a SUBSET — rebuilding from it would silently erase the excluded bots'
   history."* Therefore: **the exclusion must ship BEFORE the first ops bot trades.** If ops rows
   ever reach `trades.csv`, removing them later trips the guard and requires surgery on the ledger.
   Also subtract the ops set from `prior_bots` inside the guard, defensively.
6. **Scope the A-series.** `_a4b` and `_a6` take the ops set and skip those bots, with the skip
   **reported**, not silent — the same discipline as Tier C's `SKIPPED` rows: *"A detector that
   answers 'no findings' while structurally blind is worse than no detector."*
7. **Report an ops block.** Ops bots vanish silently from `bots.csv` otherwise. Add an explicit
   printed block mirroring the straddler / unclassified / dropped blocks. No silent caps.
8. ⭐ **How the detectors still get their labelled examples.** Because ops rows never enter the
   nightly ledger, `execution_audit.py` never sees them and needs no edit. To use phase **P4**'s
   dead-engine signature for calibration, point the **frozen** script at `data/ops_rows.csv` as an
   explicitly-invoked fixture — the mechanism it already uses for `data/archive/trades.csv` — and
   **never from `daily.sh`**. Frozen script unedited, nightly ledger clean, labelled negatives still
   available. This also answers the contamination objection in §5 O27: the injected positive is
   distinguishable because it is declared, dated, and lives in a different file.

⛔ **Group-based *export* exclusion is the wrong mechanism** and must not be used: deselecting a
group at export time produces exactly the subset the FILTERED-EXPORT GUARD exists to catch. The
daily export must **include** the ops bots; the **ledger** excludes them, post-ingest.

### 3.4 Paper vs live-tiny — **recommend PAPER**

1. **For R2/R3 paper is strictly better**, not a compromise: exits evaluate mid-price [**OA-0872**]
   and paper fills *"at or near the mid price"* [**OA-0930**], so the realised fill sits at the
   threshold that fired it and slippage does not obscure which band it was.
2. Live-tiny would require `itmlive` to move off `auto`, and that is a **hard Day-0 gate**.
3. Deliberate-failure phases (P4, P6, P7) put real capital behind an induced fault.
4. A high-churn bot on a live account acquires PDT and 390-rule exposure the paper account does not
   have.
5. The fleet is entirely paper at Day-0, so paper is the **matched** surface.
6. ⚠️ **The cost is real and is stated in §4:** paper cannot answer anything about fill quality, and
   §4.6 means paper and live run *different exit execution classes*.

### 3.5 Bot Group — **recommend `Lab`, not a new `TESTOPS` group**

**⭐ The container already exists.** `strategy-taxonomy.md` defines Pillar 4:

> | 4 | **Lab / R&D** | *our own* new ideas not yet a pillar | exploratory | **Empty — to populate** |

and *"Lab incubates our own untested ideas."* `oa-ops-runbook.md` §3's convention is
**`Group = Pillar`** — `IC` · `Directional` · `OA-Mirror` · **`Lab`** — and *"Groups must reconcile
to `bots_meta.csv`'s `pillar` column, exactly."*

A new `TESTOPS` group would be an eighth non-pillar group in an account §3 already flags as carrying
both `IC` and `IC-Focus` with the section *"stale on its face."* **`Lab` satisfies the convention,
reconciles to the `pillar` column, and requires no amendment.** The cohort handle is the **tag**
`ops`, exactly as the greenfield family uses `gfam` while sitting in group `IC`.

⚠️ **Group is single-select**, so an ops bot is not in `IC`. And ⛔ set the group **at creation** —
memo **N-5** (whether an ungrouped bot appears in an all-groups export) is **unobserved**, and an
ungrouped bot silently missing from the export *"would erase the family from the ledger."* Which is
also unknown **S4**: leaving one ops bot ungrouped for exactly one declared day is the cheapest way
to settle it — and an ops bot is the only bot it is safe to try it on.

---

## 4. What this doesn't cover

Honest limits. Several were promises in the first draft that the review destroyed.

**Paper fills are not live fills, and the gap is documented and specific.**
> *"Paper trading bots simulate a fill based on the current market's live pricing, typically at or
> near the mid price"* [**OA-0930**] · *"Backtesting and paper trading operate under the assumption
> of an order being filled"* [**OA-1138**] · *"The most common reason that a paper bot's results
> differ from a live bot is the ability to fill orders, **specifically profit taking or stop
> losses**"* [**OA-0932**].

Consequences, each a claim these bots **cannot** make:

- **No SmartPricing ladder observation.** A ladder step is visible only when an order *fails* to
  fill — the one thing the paper engine does not model.
- **No 2-minute order-lifetime signature**, for the same reason.
- **No closing-order partial fills.** DOCS-SILENT [**OA-0144**], and there is no book to partially
  fill against. *"A half-filled condor leg is a live lopsided-risk event no detector rule currently
  names"* — and nothing here changes that.
- **No fill-quality detector validation.** `IMPOSSIBLE_FILL` requires `pnl < -risk`, the documented
  consequence of a **Market** order; Market is banned. `FILL_WORSE_THAN_MAE` needs a fill beyond the
  worst recorded mark. Both are structurally unreachable by a limit order into a mid-price
  simulator. A detector cannot be validated by a stream containing no positives.

**§4.6 is a harder wall than the fill-price gap.** *"**Live bots** can enable Instant Exit Options,
which continuously monitor and update position returns"* — so *"any paper result carrying an exit-
timing claim does not transfer cleanly to live."* Exit **timing** learned here is paper timing.

**Assignment cannot be reached at all.** Bots *"do not support"* and are *"unaware of"* assignment
[**OA-0245/0246**]; the broker API does not report assignment events [**OA-0145**]; OA tracks
positions independently of the broker [**OA-0247**]. Paper has no broker. Everything in phase P3 and
in R9 is an observation of **OA-side handling and labelling**, never of broker truth. §14.1 records
this as *"a known blind spot, not a fixable one"*, and these bots do not fix it.

**The June 2026 lapse cause stays UNKNOWN.** Phase P4 can establish what a toggle-OFF engine looks
like in the data. It cannot establish that the toggle was OFF in June — no history exists — and
`day0-session-pack` reserves that verdict to the nine lapsed bots: *"the clones and fresh builds
were never lapsed and cannot test it."* Confirming a sufficient mechanism is not evidence it was the
actual cause.

**Account-wide settings are detected, not tested.** `maxexits`, `itmpaper`/`itmlive`, the Bot
Schedule and notifications are account-scoped. An ops bot is a fast **tell** if one drifts; it is
not a probe, and phase P6's probes change behaviour for every bot on the account.

**Timing observations are minute-granular, from a shared queue.** The only reliable log stamp is the
row `title` attribute, at minute granularity. Automations run in *"a distributed work queue…
executed in parallel by worker processes"*, so any jitter measured on a two-bot paper account is the
**unloaded** case and may not be stationary. **The first draft's "measure the jitter distribution"
claim is withdrawn** (§5 O6).

**Nothing observed on an ops bot proves anything about a plan bot.** `CLAUDE.md` §5's two-layer
proof is per-bot, and §8.3's verification standard is per-bot. Phase P0's Button test-fire
**rehearses** the technique; it does not discharge any arm's verification.

**Observations are perishable.** They live on OA surfaces whose date filter reaches 3 weeks and
whose `Load more` stalls. If the daily capture is not taken, the record is gone — which reintroduces
the exact fragility `post-u1-package` §4 warns of: *"a surface that must run every trading day can
silently stop running — the shape of the v1 failure this program exists to prevent."* **The capture
needs its own liveness assert: rows appear every trading day, or the brief goes RED.**

**And the instrument can go silent too.** These bots exist to detect the fleet's silence; their own
silence is detectable only because their expectation is positive and daily. The **capture step's**
silence is not. That circularity is not closed by anything in this document.

**Finally: none of it is available until the roster comes back.** `/bots` reads `0 active bots`. If
the restore does not land and `rebuild-contingency-2026-08-07.md` runs instead, these bots are the
**last** thing built, not the first — they earn their slots only against a fleet that exists.

---

## 5. Surviving objections from the adversarial review

One adversarial subagent, instructed to refute rather than improve, was run against §2's first draft
(three bots). Its citations were spot-checked directly against the files; every one I checked held.
Verdicts below are mine.

### 5.1 FATAL — killed a claim or a bot outright

| ID | The claim | The objection | Disposition |
|---|---|---|---|
| **O1** | 5 cycles/day via the `postagtoday` tag gate | The gate is a **one-per-day enforcer**; once tagged it is TRUE all session and the NO branch never runs again. `posLimitDay 5` was dead config. | **ACCEPTED.** Gate removed from both bots (§2.0). Every volume-dependent claim was rebuilt on the limits instead. |
| **O2** | SmartPricing ladder + 2-minute lifetime + partial fills | Paper *"simulate[s] a fill… at or near the mid price"* [OA-0930/1138]; a ladder step is visible only on a **failure** to fill. | **ACCEPTED.** All three claims **withdrawn** → §4. |
| **O3** | Measure the automation-log retention window | Answered 2026-08-04, §9 #7: filter 3 weeks, data ≥141 days. *"Retention is not the constraint — the filter is."* | **ACCEPTED.** Withdrawn → Q7. Narrowed survivor is **R5**, the `Load more` stall. |
| **O4** | The Automation-Log-link target | Already a queued **~5-minute** opportunistic Day-0 read. | **ACCEPTED** → Q4. |
| **O5** | A standing daily DST check | Already reproduces on all six/seven arms; and November is the **safe** direction — the risky reading resolves on day 1, in EDT. | **ACCEPTED** → Q1. |
| **O6** | Measure the jitter distribution | No fire-time readout finer than the log row's **minute**; and it would be the unloaded case. | **ACCEPTED.** Withdrawn → §4. |
| **O7** | Validate `BACKSTOP_CAUGHT_IT` | The rule `continue`s unless **both** `time_exit` and `event_backstop` are values with `bs > te`. A bot with no time exit can never fire it. Verified at `execution_audit.py` L594. | **ACCEPTED.** Withdrawn. |
| **O8** | Validate `IMPOSSIBLE_FILL` / `FILL_WORSE_THAN_MAE` | Both need a fill outside the spread — the signature of a **Market** order, which is banned. | **ACCEPTED.** Withdrawn → §4. |
| **O9** | Read the open/close notification email | `paper` notifications are **unchecked**, so no email is sent; turning it on is **account-wide**. | **ACCEPTED.** Demoted to a gated account-wide probe; not a design claim. |
| **O10** | Test §10's causal claim | §10's claim is **historical**; only the nine lapsed bots can test it. A new bot establishes the forward direction, already documented [OA-0871]. | **ACCEPTED AND NARROWED.** R8 now claims the **observable signature in the data** — which is not documented — and explicitly not the causal claim. |
| **O11** | C9 on the churn bot | C9's open limb is the **Events-class and ITM-action** limbs; the bot with the witness had no Events-class close, and the bot with the Events-class close had no witness. | **ACCEPTED.** Consolidated: the witness and all three close classes now live on one bot, isolated by phase (P2/P3). |
| **O12** | 2–3 contracts is harmless | `_a6` is **unscoped** and flags any `quantity not in (1.0, 1)` → **A6 FAIL** on the first fill. Verified. | **ACCEPTED.** The §3.3 exclusion is now a **hard precondition**, three-surface, and must ship before the first fill. |
| **O13** | The churn bot gives A4b a labelled positive | `_a4b` is **unscoped**, and the churn bot's own fast same-day closes ARE the signature → **A4b FAILs permanently**. Verified. | **ACCEPTED.** Claim **withdrawn**; A4b scoping moved into §3.3. |
| **O14** | Deliberately break an input link | A4b's signature is **stop-outs on a bot with no `stoploss`** — the churn bot has no stop mechanic. And no observed UI operation induces a broken link. | **ACCEPTED.** Withdrawn entirely. |
| **O15** | "not a research arm" is sufficient | Intent excludes nothing; `build_ledger.py` has **no filter**, and `report.py` sums every row. | **ACCEPTED** — this *is* §3.3, and it is why §3.3 is a precondition rather than hygiene. |
| **O16** | One bot for both the stop and the expiry path | At 0.10% OTM, `dstop −40` ≈ $0.20 of mid — traversed on a routine move, so the position almost never survives to 15:50. The two claims were mutually exclusive. | **ACCEPTED.** Fixed by the far-OTM strike (1.50%) + wider `D`, which §2.2 needed for O21 anyway. |
| **O17** | Observe the ITM action's **label** | Answered NEGATIVE by U-1 and ruled **PERMANENT**. | **ACCEPTED AND NARROWED** → R9 now claims row **existence** and **link absence** only. |
| **O18** | Observe closing partials at 2 lots | Most liquid contracts listed, and no book in paper. Expected positives ≈ 0. | **ACCEPTED.** Withdrawn → §4. |
| **O19** | "the only bots for which zero activity is unambiguous" | The entry is **not** ungated — minimum credit, strike availability, and *"the 'Opportunity is available' check fails without alerting"* [OA-0382]. And `SILENT_BOT` emits AMBER regardless; realising the benefit needs code that does not exist. | **ACCEPTED AND NARROWED** in §2.1's no-trade-day check, which now says *narrower*, not *unambiguous*. |
| **O29** | A daily 5%-PT bot | That is **PR-20 byte for byte**, already signed and already the fleet's forward exit-engine detector. | **ACCEPTED.** Third bot **deleted**; churn bot moved to `profits 0.25`. |

### 5.2 MATERIAL — the design changed rather than the claim dying

| ID | Objection | Disposition |
|---|---|---|
| **O20** | C10's axis is **three-way** (`per contract / position / leg`), so 2 contracts collides per-contract with per-leg. | **ACCEPTED and extended.** §2.2 enumerates **four** candidate bases and derives **n = 3** as the minimum that separates all four. |
| **O21** | At a near-ATM strike the bands are traversed between consecutive 1-minute checks. | **ACCEPTED.** Far-OTM strike + `D = 60`, giving ≥$0.20 of mid between bands. |
| **O22** | A Button fire on an ops bot verifies **that** bot. | **ACCEPTED.** S6 narrowed to *"rehearses the technique."* |
| **O23** | A bare Tag witness is a **saturating latch**. | **ACCEPTED.** Untag-then-Tag, with the bot-log Event rows as the per-fire readout. |
| **O24** | With Exit Options OFF, `itmpaper = market` still closes ITM positions at 15:50, masking the death signature — and disambiguating needs the label O17 says is gone. | **ACCEPTED, PARTIALLY OPEN.** P4 runs at the far-OTM strike to make ITM days rare, and any ITM day in the window is reported as **confounded**, not as signal. ⚠️ **Residual: the confound is not eliminated, only made rare and labelled.** |
| **O25** | Reusing `GF-Backstop-1552-FlatClose` puts all seven arms one edit from a fleet-wide change and invalidates its A7 baseline. | **ACCEPTED.** Guardrail **G4**: per-bot copies only, never a Library object. |
| **O26** | Riding a physically-settled ETF to expiration can produce assignment errors, and 10 errors in a day disables all automations — *"if another error occurs that same day the automations turn off again."* | **ACCEPTED, RESIDUAL.** Phase P3 can die silently by the mechanism it is characterising. Mitigation is only that P3 is short, declared, and its no-trade-day check fires. ⚠️ **Genuinely unresolved.** |
| **O27** | Deliberate config mutation generates drift findings indistinguishable from real ones, each emitting an instruction card *"repeated at the top of every brief until closed."* | **ACCEPTED, ANSWERED BY §3.3.** Ops rows never enter the nightly ledger, so the detector never sees them; calibration runs read `ops_rows.csv` explicitly. ⚠️ Contingent on §3.3 shipping first. |
| **O28** | Absent from `bots_config_v2.csv`, Tier-C rules emit daily `SKIPPED` rows; present, the ops bots join the capture ritual they were meant to sit outside. | **ACCEPTED.** They join the capture ritual. §3.3 item 7 makes the ops block explicit so the SKIPPEDs are not noise. |
| **O30** | A `TESTOPS` group violates `Group = Pillar`. | **ACCEPTED.** §3.5 recommends the existing **`Lab`** pillar instead. |

### 5.3 Attacks that failed — recorded, because it says which claims are solid

- **`posLimitDay 5` is illegal** — no; the pickers offer 1–10 and a vertical is one position.
- **Fixed contract count is unobserved** — no; ✅ **C4** answered 2026-08-05, and corroborated
  first-hand in the Phase-A build.
- **`dstop` may not be settable** — no; §6.1a confirms it first-hand, and ✅ **C3** confirms its
  SmartPricing sibling defaults to `normal`, not `market`.
- **The 1-contract-indistinguishability claim is wrong** — ⭐ **no, it is right**, and the Day-0 pack
  had already found it: **A-12(b)**, *"at 1 contract per leg, per-leg count = 1, so `−$100` and
  `−$100 × 1` are the same number."* §2.2 extends it to a derived count.
- **The `EXIT OPTIONS` toggle probe is account-wide** — no; it is **per-bot**, documented on three
  surfaces [OA-0896], stored as `disableExits`.
- **The churn bot trips the §4.7 event-loop class, or the failsafe via limit warnings** — neither.
  The witness only tags, so there is no close→open loop; and *"the four named Warnings never count
  toward the failsafe"* [OA-0324]. (The failsafe exposure is real but arrives via **O26**.)
- **The `Button` trigger does not exist / no slots** — it exists (`0/10`, a tenth type absent from
  OA's documented list), and both bots fit inside every per-class slot budget.
- **15:52 is not reachable** — it is; built and reload-verified as `ntime=1552`, and Repeating
  triggers are exempt from the Bot Schedule.
- **The §7 Market ban is violated** — it is not. The only Market order reaching these positions is
  the **account-level ITM action**, which is not the bot's choice.
- **The template successor-rid check is not really blocked on a bot** — it is: *"NOT RUN. It needs
  either a template saved from a delete-list bot… or a production bot, which this session was barred
  from."* ⚠️ But it is a **one-shot ~10-minute check**, so it justifies *a* disposable bot, not daily
  operation — which is why it sits in **Class S**, not Class R.

---

## 6. What Andy is being asked to rule

| Slot | Question | Recommendation |
|---|---|---|
| **A** | Do 2 ops bots fit under ceiling 28, or is an amendment needed? | ⛔ **They do not fit.** Amend: **third named allocation, `≤2 Lab ops slots`, ceiling 28 → 30.** Costs stated in §3.1 |
| **B** | Exemption class, or individual entries? | **Neither, as posed.** A named **ops-class** following PR-20's pattern — full entries, declared `n/a` fields, a new `PHASE LOG` field, guardrails G1–G10 |
| **C** | The exclusion mechanism | Mirror `LEDGER_START`'s three-layer pattern on a second axis, sourced from a **new `bots_meta.csv` `ops_class` column**; **three surfaces** (`build_ledger.py`, `a_series.py` A4b/A6, the report view); `execution_audit.py` stays **frozen** and reads `ops_rows.csv` only as an explicit fixture. ⛔ **Ships before the first ops bot trades** |
| **D** | Paper or live-tiny? | **Paper** — and for R2/R3 it is the better instrument, not a compromise |
| **E** | Own Bot Group? | **`Lab`** — the existing pillar, no amendment needed. Cohort handle is the tag `ops` |
| **F** | *(new — surfaced by this design)* | **G7/P6:** are the account-wide probes (`maxexits`, failsafe error taxonomy) authorized at all? Separate ruling |
| **G** | *(new — surfaced by this design)* | **O26 residual:** phase **P3** can die by the very failsafe it characterises. Accept, or drop P3? |

⛔ **Nothing is built until: the OA restore lands and Andy verifies the roster; slots A, B, C are
ruled; and the §3.3 exclusion is shipped and tested at n=0.** `build-plan.md`'s own standard —
*"Every script must degrade gracefully at n=0… Never seed a synthetic row to make the run pass"* —
applies to the new partition.

---

*Sources, in the order they carried weight: `docs/state.md` · `docs/day0-session-pack-2026-08-07.md`
(re-read at 2333 lines; §0.0 A-01…A-25) · `docs/oa-platform-reference.md` §3/§4/§5/§6/§7/§8/§9/§11/§13/§14
· `docs/greenfield-family-spec.md` §4/§5/§10 · `docs/build-plan.md` §2D · `docs/pre-registration-ledger.md`
§2/§3/§6/§7 · `docs/oa-ops-runbook.md` §3/§7 · `docs/post-u1-package-2026-08-07.md` §4 ·
`docs/research-loop-fix-spec-2026-08-07.md` · `docs/daily-loop-spec.md` §5 · `docs/strategy-taxonomy.md` ·
`docs/comparative-machinery-spec.md` · `docs/session-log.md` 2026-08-06 · `scripts/build_ledger.py` ·
`scripts/a_series.py` · `scripts/execution_audit.py` · `scripts/report.py` · `data/oa_facts.csv` ·
`CLAUDE.md` §4/§5/§9. Platform features change and the docs demonstrably lag the product — re-verify
every control cited here against the running account before building on it.*
