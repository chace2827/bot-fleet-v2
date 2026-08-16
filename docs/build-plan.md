# Build plan — Bot Fleet v2

*Rewritten from scratch 2026-07-30 after the consolidation pass. **This is the settled architecture.**
It supersedes every earlier version of this file and `approach-reset-2026-07-29.md` Parts 3 and 5.*

> ## 🔒 DECISION FREEZE — 2026-07-30
> The architecture below is settled. **Changing any of it requires an explicit "amend the plan"
> instruction from Andy.** Not a suggestion in passing, not an inference from a new finding, not a
> "while we're here". If a session believes something here is wrong, it says so and stops — it does not
> edit this file. Three amendment rounds in one day is what made this freeze necessary.

---

## 1. The organising idea

Two clean slates at once, on the same date.

**The data slate.** `build_ledger.py` takes a `LEDGER_START` constant set to the Day-0 reactivation date. **[AMENDED 2026-08-08 — `LEDGER_START` = `2026-08-10`; see §3's amendment banner.]**
The working ledger, `STATUS.md`, the daily brief and every drift report read **post-cutover data only**.
The v1 ledger is frozen in `data/archive/` and is never a reporting input.

**The OA slate.** Every bot that is active on Day-0 is one of exactly three things: **fresh-built**,
**cloned-to-spec from a legacy bot whose original is then archived**, or **left untouched because it was
already built correctly**. Roughly 20 legacy bots are archived outright.

The point of doing both together: **from Day-0, every number on the OA dashboard is real.** No epoch
boundaries to remember, no contaminated cohorts to mentally subtract, no "that figure predates the fix."
The reason the v1 project became untrustworthy was that reading any number required knowing four caveats.
This ends that by construction rather than by discipline.

**What it costs, stated plainly:** every bot restarts at n=0. The IC-continue question — the program's
central question — begins accruing evidence from zero on Day-0. Under the adopted gates (n≥100 positions
/ 6 months / a regime change) that is roughly six months before anything is decidable. That is the price
of a record that means what it says, and it is accepted.

---

## 2. Fleet disposition — all 35 bots on the OA roster
*(Confirmed against the 2026-07-30 `/bots` capture. Earlier drafts framed this as a 33-bot table drawn
from `bots_meta.csv`; that universe was ledger-derived and structurally blind to zero-trade bots.
**The roster authority is the capture.**)*

> **⚠️ ROSTER AUTHORITY: the bookmarklet capture of the OA `/bots` page — not `bots_meta.csv`.**
> `bots_meta.csv` knows only the 32 bots that ever traded (33 rows, one of which never traded).
> The live `/bots` page carries **35**, because zero-trade bots never enter the ledger.
> **CONFIRMED by the capture of 2026-07-30** (`data/captures/oa_bots_capture_2026-07-30.txt`):
> 35 active bots, **exactly 3 of them zero-trade**.
> **Take the capture first, then sweep against the capture.**
>
> *(Correction of record: an earlier note identified "the TEST bot" as `QQQ-IC-0DTE-HedgeTest`. That was
> wrong. `HedgeTest` traded 93 positions and is archived with the hedge family. The real name is
> **`TEST QQQ-IC-0DTE-HedgeC-S3 Clone`** — a zero-trade clone of HedgeC-S3.)*

### The sweep rule
**Positions → archive. Empty → delete.** A bot that never traded has no history to preserve, so archiving
it just moves clutter. **The capture must be taken before any deletion**, so even the empty bots appear in
the pre-sweep record exactly once.

> ### ⛔ THE DELETE RULE DOES NOT OVERRIDE THIS TABLE
> **"Empty" is not the same as "worthless."** `DIR-SPX-PutVIX22-SL75` has **zero closed positions** —
> not because it is a test bot, but because **its VIX≥22 gate correctly never fired** in 22 days. It is an
> OOS-validated directional build and it is in the leave-in-place group. Applying the empty→delete
> heuristic to it would destroy a validated bot to tidy a dashboard.
> **Rule as it now stands: delete only bots that are BOTH zero-trade AND absent from this disposition
> table.** Where the heuristic and the table disagree, the table wins.

### 0. Delete — zero-trade bots (exactly 2, confirmed by capture)
- `TEST QQQ-IC-0DTE-HedgeC-S3 Clone`
- `QQQ-IC-0DTE-InvFilter-Wide150`

Nothing to archive: no positions, no ledger rows, no `bots_meta` entry, no place in the plan.

**NOT deleted despite being zero-trade:** `DIR-SPX-PutVIX22-SL75` — see the call-out above. It is the
third zero-trade bot on the roster and it stays, untouched, in group C.

### A. Archive directly — no clone (20)
Every bot in this group traded, so every one has history in the frozen archive ledger.
Nothing is carried forward. History dies with the cutover; the bots remain in OA archived, and
`data/archive/` holds their ledger.

| Group | Bots | Why |
|---|---|---|
| SPX Fortress arms | `IC-SPX-Fortress-Unstopped`, `IC-SPX-Fortress-Defang` | Roles superseded — the greenfield family supplies the new control and A/B arms, built matched from the start |
| QQQ Fortress variants | `QQQ-IC-0DTE-Fortress-NoFilter`, `-Fortress-S2` | Both tagged S2 but UNVERIFIED; never adjudicated |
| QQQ hedge family | `HedgeA-S1`, `HedgeB-S2`, `HedgeC-S3`, `HedgeD-Conditional`, `HedgeTest` | Tournament invalid as a selector: S1≈D identical on 73/86 days, S3 a different execution class, no arm carries Range075 |
| QQQ controls | `QQQ-IC-0DTE-Baseline`, `-Raw-HoldToExp`, `-InverseFilter-HoldToExp` | Baseline was never audited and now never will be — see §6 |
| Old Range075 experiments | `-VIX25-Range075-PT50`, `-Range075-PT50`, `-Range075-PT50-Wide2-155PM`, `-Range075-PT50-Wide2-1230PM` | Superseded by the greenfield family |
| Killed mirrors | `Weekly-IB-SPY-Paper-v1`, `1-45pm-Sandwich-Paper-v1`, `Opening Range Breakout 60m` | Already kill-flagged pre-lapse; funding bar failed |
| Directional control | `DIR-SPX-Put-Control` | Its gate-proof function is served by the OOS control backtest. Default was never to restart it; this makes that final |

⚠️ **Name-collision warning for the archive sweep:** `Opening Range Breakout 60m` is archived.
`60min-ORB-10W-Paper-v1` is a **different bot and stays live**. Read the full name before archiving.

### B. Clone → spec → archive original (4)
The clone takes the production name; the original is renamed with an `-ARCHIVED-20260812`-style suffix
*before* being archived, so the live dashboard reads clean and the capture files stay legible.

| Original | Clone spec | Notes |
|---|---|---|
| `IC-SPX-FastPT25-S2` | **ride + S2**, and **only** the two safety fixes: scanner re-entry gate → `opened this side today`, and Cleanup pricing Market → SmartPricing | **No new exit architecture. It is a control.** PT25 removed from the Open Position action explicitly — not left dead behind an off toggle. **Do NOT touch Cleanup itself** — S2 depends on it |
| `IC-SPX-FastPT25-S2-130PM` | Identical, 1:30 PM entry | The entry-time A/B partner. Same two fixes, same Exit-Option-free spec |
| `QQQ-IC-0DTE-Fortress` | **Restored exits: PT50 + 15:50 time exit + 15:52 flat-close Scheduled Event backstop** | ⛔ **Justification corrected 2026-08-05 on Andy's "amend the plan" — wording only; the build is unchanged.** *Original: "The restoration the forensic called for, now built into a clean bot instead of patched into a broken one."* **The clone's exits already existed:** both Open Position actions carry PT50 + a 15:50 time exit, read first-hand 2026-08-03. Only the **15:52 Scheduled Event backstop** was new work. What died in v1 was **execution, not configuration** (`oa-platform-reference.md` §0.3 — a dead profit target displayed correctly for four months). The forensic called for the backstop and for **order-level proof that the configured exits actually fire** — not for restoring exits that were never absent from the config. Day-0 Trades-list verification is the deliverable this row depends on. |
| `QQQ-IC-0DTE-Fortress-NoPT50` | **15:50 time exit + 15:52 Scheduled Event backstop. NO PT50.** | **RESOLVED 2026-07-30.** This restores the bot's declared no-PT design and preserves the real A/B: PT50 vs none, against the Fortress clone, with everything else matched. Name stays — it is now accurate |

### C. Leave in place, untouched (9)
Validated builds with negligible or specially-treated history. No clone, no spec change. These are the
**only** bots that need the Day-0 re-arm sweep, because they are the only ones that lived through the lapse.

- **Directional (2):** `DIR-SPX-PutVIX22-SL75`, `DIR-SPX-CallVIXdrop`. Both OOS-passed, params frozen,
  negligible live history. PutVIX22's health is still unverified — 0 positions in 22 days because VIX never
  reached 22. Only the liveness check closes that.
- **Mirrors (7):** `3DTE $140-$350`, `Nigiri-Paper-v1`, `QQQ long call`,
  `Friday 14 DTE Broken Wing IB (B-70)`, `Trendy-Paper-v1`, `60min-ORB-10W-Paper-v1`, `Tasty Condor`.
  **Never refactored, watch-only.** Their lifetime record is the funding-decision input — see §3.

### D. Fresh builds (5–8)
- **Greenfield IC family (4–8 bots)** — the matched tournament: hard-PT vs trailing vs ride, arms differing
  in exactly one input value.
- **Rebuilt hedge tournament arms** — shared automation, shared inputs, same execution class, Range075 as a
  preset. Proof of matching is a capture-diff showing one differing input. No ranking until then.
- **Optional 1-lot canary** whose PT should fill every single day. If it stops filling, the exit engine died.

> ### 🔓 AMENDMENT 2026-08-12 — 8th greenfield arm
> Andy ruled `GF-QQQ-IC-Ride-Delta` is added as the 8th greenfield arm. The greenfield family
> now counts 8 bots, so the family-size range and fresh-build range are widened accordingly.
> End-state arithmetic below is unchanged except the greenfield count.

**End state: ≈18–20 plan bots plus ≤8 pre-registered Track B arms
(`research-loop-spec.md` §10, signed) plus ≤2 Lab ops slots (a third, separate allocation —
🔓 AMENDMENT 2026-08-07 below), ceiling 30.**
**Accounting: 35 on the roster = 20 archived + 2 deleted + 4 cloned (originals archived) + 9 untouched.**
Confirmed against the 2026-07-30 capture. No remainder.

> ### 🔓 SCOPING AMENDMENT 2026-08-05 — "amend the plan", Andy's explicit words
> **This row previously read:** *"End state: ≈18–20 active bots (4 clones + 9 untouched + 5–7
> fresh)."* The plan-bot arithmetic is unchanged; what changed is that **Track B arms are now named
> as a separate allocation rather than silently colliding with this count.**
>
> **Why.** `research-loop-spec.md` §10 (signed 2026-08-04) reserves **≤8 bot slots for Track B**.
> `greenfield-family-spec.md` §12 item 11 found that the seven greenfield family bots meet
> `research-loop-spec.md` §4's definition of a Track B arm, so on one reading the family consumed
> **7 of those 8 slots** — leaving one slot to fund three questions rulings R-1, R-2 and R-6 had
> just created. `track-b-arms-spec.md` §3.5 ruled that reading out: **S-1 — separate allocation
> (Reading B)**, the seven family bots are §2D fresh builds and Track B's 8 slots are Track B's,
> with `n_used = 20` confirmed. **S-2** recorded that this spec's slot accounting was
> **CONDITIONAL on an "amend the plan" scoping amendment to this section.** This is that amendment.
>
> **Operative figures:** ≈18–20 plan bots · wave-1 Track B spend **2** · **ceiling 28** if Track B
> is fully spent. Well inside the Pro plan's 50-bot cap on the reading where archived bots do not
> count against it. ~~⚠️ **That reading is not verified** — whether archived bots consume plan slots
> is check **C12** in `track-b-arms-spec.md` §10, blocking, because if they do count the Day-0
> arithmetic is 36 + 7 = 43 and the ≤8 allocation does not fit (43 + 8 = 51).~~
>
> > ### 📝 C12 DISCHARGED — correction applied 2026-08-05
> > *Factual reconciliation of this amendment block only, under `CLAUDE.md` §5's corrections
> > clause. **No operative figure in this amendment changes** and no build is authorized. The
> > struck caveat above is retired; it is left standing per the doc convention.*
> >
> > **Evidence — [FIRST-HAND 2026-08-04, `/bots` footer read].** Immediately after the original
> > `QQQ-IC-0DTE-Fortress` was archived, the `/bots` footer was read read-only as
> > **`35 active bots • 15 left in your plan`**; it had read **`36 active bots`** throughout the
> > three preceding failed archive attempts. **35 + 15 = 50** — the plan complement is computed
> > against the **ACTIVE** count, and one archive decremented that count by exactly one.
> > **Archived bots do not consume plan slots.**
> >
> > **Consequence:** wave 1 is **22 of 50**, ceiling **28 of 50**. The `36 + 7 = 43` Day-0
> > arithmetic and the `43 + 8 = 51` overflow scenario struck above are **void**.
> >
> > ⚠️ **RESIDUAL — carried, not dropped. Tier: [FIRST-HAND, UNCORROBORATED]** (no second
> > witness). This reads the footer's **accounting**, not OA's **enforcement**, and two limits
> > bound the inference: (1) a footer rendering `left = 50 − active` is self-consistent under
> > *both* hypotheses — "archived are free" and "the display subtracts from a constant 50"
> > produce the identical string, so only a *create* attempt at the boundary can distinguish
> > them, and none has been made; (2) it was observed with **one** archived bot in existence,
> > where the Group-A sweep archives **twenty** — nothing demonstrates the accounting holds at
> > that scale. Per `CLAUDE.md` §3 item 3 a footer is a panel, and a panel is intent.
> >
> > ⛔ **REOPEN CONDITION, pre-declared:** *if a bot build ever fails at the cap despite archived
> > bots existing, **C12 reopens** and the ≤8 allocation is re-derived against an observed slot
> > count.* Full evidence block, residual and reopen condition: `track-b-arms-spec.md` §3.2.
> >
> > **This amendment still scopes a count. It still authorizes no build.**
>
> **This amendment scopes a count. It authorizes no build.** Every Track B arm still needs its own
> signed pre-registration entry before it may be switched on.

> ### 🔓 AMENDMENT 2026-08-06 — "amend the plan", Andy's explicit words. Range075 wording corrected.
> **This section's "Rebuilt hedge tournament arms" bullet previously read, and read until now:**
> *"Rebuilt hedge tournament arms — shared automation, shared inputs, same execution class,
> Range075 as a preset. Proof of matching is a capture-diff showing one differing input."*
>
> **Corrected to:** *"Rebuilt hedge tournament arms — shared automation, shared inputs, same
> execution class, Range075 in the shared entry automation. Proof of matching is a capture-diff
> showing one differing input."*
>
> **Why.** Presets are an Exit Options object (`oa-platform-reference.md` §6.1, verbatim: "Save
> your Exit Option criteria as a Preset to be reused for…"); Range075 is an entry decision
> (`hedge-research.md` §8: "a gap filter, not an intraday-range filter: implement as a symbol
> %-change decision, not a high-low range check"). An entry decision cannot be an Exit Option
> preset, so "Range075 as a preset" named a primitive that cannot express the mechanic — the same
> defect class as `hedge-research.md` §7's HedgeD lesson. Under **Architecture E** (Decision 4,
> ruled 2026-08-04), the substance is unchanged and strengthened, not weakened: Range075 lives in
> the shared entry automation (`GF-ScannerA-PutSpread` / `GF-ScannerB-CallSpread`,
> `greenfield-family-spec.md` §4.1), identical across all seven arms by construction rather than
> by repeated preset attachment. **Nothing else in §2D changed; no build authorized by this
> amendment.**
> Ruled 2026-08-04 (`decision-memo-2026-08-04.md` Decision 4, draft (c)); applied 2026-08-06 per
> `decision-card-2026-08-06.md` ruling 1a — reopens only if the UI check (does the preset picker
> accept a non-Exit-Option criterion — presumed no, not yet directly observed) ever contradicts.

> ### 🔓 AMENDMENT 2026-08-07 — "amend the plan", Andy's explicit words (E-1)
> **This row previously read:** *"End state: ≈18–20 plan bots plus ≤8 pre-registered Track B arms
> (`research-loop-spec.md` §10, signed), ceiling 28."* **A third, separate allocation is added:
> `OPS/Lab ≤2 bots`. Ceiling 28 → 30.**
>
> **Why.** `exploratory-bots-design-2026-08-07.md` §3.1 SLOT A found that the 2 Lab ops bots Andy
> asked for (`session-log.md` 2026-08-06, *"create a few bots that fire on every day… so we can
> learn more about the mechanics and operations and testing of how OA fully operates"*) do not fit
> under the existing ceiling: *"plan bots (18–20) + Track B (8) = 26–28 ← the ceiling IS this sum…
> 2 ops bots do not reliably fit under ceiling 28."* The design doc's recommendation — mirror what
> **S-1** did for Track B, a **third named allocation rather than a raid on the second** — is
> adopted as stated:
>
> > *"`≤2 Lab ops slots`, a separate allocation. Ceiling 28 → 30. Wave 1 becomes 24 of 50; full
> > spend 30 of 50."*
>
> **Operative figures:** ≈18–20 plan bots · ≤8 Track B arms · **≤2 Lab ops slots** · **ceiling 30**.
> Wave 1 spend is now **24 of 50**; full spend **30 of 50** against the Pro 50-bot cap (active-count
> reading, `§2D` `🔓 SCOPING AMENDMENT 2026-08-05`, C12 discharged).
>
> **⚠️ Cost stated, not buried — carried from `exploratory-bots-design-2026-08-07.md` §3.1:**
> 1. **It makes C12's residual more likely to bite.** C12 was discharged on a footer read that is
>    `[FIRST-HAND, UNCORROBORATED]` — observed with **one** archived bot where the sweep archives
>    **twenty**. Under the pessimistic reading, 30 + ~23 archives = **53 > 50**. The pre-declared
>    reopen condition — *"if a bot build ever fails at the cap despite archived bots existing, C12
>    reopens"* — becomes materially likelier. 2 slots is the cost of that.
> 2. **This arithmetic is provisional on the restore.** `/bots` read **`0 active bots • 50 left in
>    your plan`** against an expected 41 at time of writing (`state.md` 2026-08-07 incident block).
>    Every number above describes a fleet that does not presently exist until the restore lands and
>    Andy verifies the roster count.
>
> **This amendment scopes a count. It authorizes no build.** No Lab bot's `AUTOMATIONS` may go ON
> until **E-3**'s hard precondition clears — `build_ledger.py` exclusion + `a_series` scoping + Lab
> group/tag fencing, implemented and verified (`exploratory-bots-design-2026-08-07.md` §3.3,
> queued as a Claude Code task) — **and** the OA restore lands, **and** Andy's go.
> Ruled by Andy 2026-08-07 (~14:40 ET), signing E-1/E-2/E-3 together. Design doc:
> `exploratory-bots-design-2026-08-07.md` §3.1 SLOT A.

---

## 3. Data architecture after the cutover

**`LEDGER_START` = the Day-0 reactivation date.** Everything downstream reads post-cutover only.

> 🔓 **AMENDMENT 2026-08-08 — explicit "amend the plan" given by Andy at the 2026-08-08 ruling
> sitting (slot 1 · A-02 · CA-1).** The sentence above stands as the original; this banner governs.
> Once payment (2026-08-07) and Day-0 separated, *"the Day-0 reactivation date"* named two
> different days. **RULED: `LEDGER_START` = `2026-08-10`** — Monday's open, the first market
> session on or after switch-on; never the payment timestamp, and never a non-trading day on which
> a toggle was flipped. **The date is FIXED:** it does not move if switch-on slips, because a bot
> that is OFF opens nothing, so a floor of 2026-08-10 admits no row it should not.
> `scripts/build_ledger.py`'s constant is set to this value **at Day-0**, per that script's own
> line-151 instruction — not before. Evidence for the two-days problem: `data/ledger_meta.json`
> (`ledger_start 2099-01-01` sentinel, `post_cutover 0`) and the 2026-08-07 payment timestamp
> recorded first-hand in `docs/state.md`'s incident block.

### The straddle rule — a position's era is its OPEN date
**`LEDGER_START` filters on `open_date`, never `close_date`.** A position belongs to the era in which the
decision was made to enter it; when it happened to resolve is an accident of its structure.

Straddling positions — opened pre-cutover, closing after it — **resolve into the mirror baseline layer,
never into the working ledger.** Two groups exist, both mirrors, and both already identified:
- **6 already-closed rows**: `3DTE $140-$350` ×3, `Nigiri-Paper-v1` ×1, `Tasty Condor` ×1,
  `Trendy-Paper-v1` ×1 — opened before the 7/02 freeze, closed by 7/27, worth +$632.
- **5 still open at capture**: `QQQ long call` ×4 (~$13K risk, ~−$10.8K unrealized) and
  `Tasty Condor` ×1 (~+$328 unrealized).

Only multi-day structures can straddle. Every 0DTE bot in the fleet is immune by construction, which is
why this rule costs nothing anywhere except the mirrors — and the mirrors are already carved out.

**Why open-date and not close-date:** a close-date rule would let a position entered under a dead exit
engine, at a strike chosen by a config that no longer exists, land in the clean post-cutover ledger and
be read as evidence about the new fleet. That is precisely the contamination the cutover exists to
prevent, arriving through the one door left open.

**The one exception — mirror funding.** The 7 live mirrors are judged for funding on their **pre-lapse
lifetime record**, which by definition predates the cutover. Mechanism: a **one-time frozen snapshot
table** (`data/mirror_baseline.csv`) holding per-mirror R, n, and funding status as of the pre-lapse
window. It is written once, never recomputed, and read **only** by funding decisions.
⚠️ **Build it from `data/captures/oa_export_positions_2026-07-30.csv`, NOT from the archived
`trades.csv`.** The v1 ledger is missing **6 mirror positions worth +$632** — multi-day mirror trades that
were opened before the 7/02 freeze and closed after it, so the ledger's last ingest never saw them.
The 0DTE bots have no such tail; the mirrors do, and they are precisely the bots this table is about. Every other
reporting surface stays strictly post-cutover. This is the only place pre-cutover numbers enter the
working layer, and it is bounded to nine rows and one decision.

**Frozen forever in `data/archive/`:** `trades.csv`, `corrections.csv`, `bots_config.csv`,
`compliance.csv`, and `README-v1-ledger.md` (the one-page summary). Not reporting inputs. See that README.

**`data/archive/rename_map.csv`** — written as the sweep runs: `original_name`, `archived_as`,
`clone_name`, `date`, `disposition`. Without it, a name in the frozen ledger cannot be traced to the bot
running today, and every later question about lineage becomes archaeology.

**Still live in `data/`:** `execution_audit.csv` — the **frozen 35-row detector validation fixture** for
Phase 3, together with the two loss-side impossible fills **T00147 (R −1.63)** and **T00845 (R −1.10)**.
This fixture is a test asset, not a ledger, and it does not expire at the cutover. `bots_meta.csv` carries
forward and gets rewritten for the new roster. `lessons.csv` carries forward.

⚠️ **Phase 3 must resolve:** `data/raw/` and `data/brief/` still hold pre-cutover exports and tape.
Either `build_ledger.py` filters them by `LEDGER_START`, or they move to `data/archive/` too. Do not leave
this ambiguous — it is exactly the kind of gap that lets a pre-cutover number back into a report.

**Dead — do not revive as blockers:**
- Fortress `epoch_boundary` work. The boundary stays recorded in `bots_meta.csv` as archive metadata, but
  no script needs to apply it and no report depends on it.
- The Fortress `strike_fix=Y` adjudication. It concerned archived bots and pre-cutover data.
- The `QQQ-IC-0DTE-Baseline` forensic **as a growth gate**. Re-filed as optional research (§6).

---

## 4. Arm A — what the champion clone actually is now

**A fresh, pre-registered control arm starting at n=0.** Nothing else.

The earlier rationale — "29 post-fix condors of exactly ride+S2, so the baseline continues unbroken" —
**no longer holds and must not be repeated.** The clone is a new bot, and the cutover means those 29
condors are archive-only context. They are not a prior, they are not a head start, and they do not appear
in any v2 report.

What the clone is *for*: the legacy configuration deserves a fair, instrumented run as the control against
which the greenfield PT variants are judged. It is held to the same gates as every other arm. If it fails
them, it fails them on its own new evidence.

Its one distinguishing property is deliberate: **it carries no Exit Options at all.** That makes it the
ride benchmark. It is still subject to the `AUTOMATIONS` toggle, because its S2 monitor lives on the
automations side.

---

## 5. Standing rules

**Sizing** — set once at restart, never adjusted ad hoc: experiments 1 lot; CANDIDATE and above a uniform
**≈$5K risk per position** via OA's $-risk cap; tournament arms always identical allocation.
**Compare by R, never raw P/L.** Condor risk = the larger side. The unit of account is the **position**.

**Evidence law** — every claim tiered T1–T5. Nothing below T2 with n≥100 / 6 months / a regime change
supports a live-capital or growth decision. Machinery adopted from the independent audit; its **kill-IC**
verdict and its **custody-separation / independent-go-live-authority** recommendations (audit §5.5 items
6–7) are overruled/declined.
*Amended 2026-07-31, wording only, at Andy's explicit instruction. This clause previously read
"third-party-switch verdicts overruled" — a garbled transcription of "the go-live **switch** held by a
**third party**", which had come to read as a platform change. No platform-migration recommendation exists
anywhere in the audit. **Nothing else in this plan changed.** Reason and reopen condition:
`docs/evidence-standards.md` §9.2.*

**Pre-registration** — hypothesis, kill criterion, sample target, review date, config-capture hash. Written
**before** the bot starts. No entry, no restart. Every one of the ≈18–20 active bots needs one, including
the untouched nine.

**The daily loop** — Claude detects, instructs, **and executes: Claude makes OA edits directly**
(Chrome-direct), self-verified before being reported done — an immediate screenshot/capture
re-observation of the changed value, **plus** the pre-existing **first new position's Trades list**
check for behavior. The Exit Options panel is never evidence. Three verdicts, never blended: did it
fire? / did the mechanics execute? / was it right for the tape?
*Amended 2026-08-04, at Andy's explicit instruction — supersedes "Andy makes all OA edits." Andy
retains revoke authority, globally or per-bot, at any time. Full procedure:
`docs/oa-ops-runbook.md` §4; `CLAUDE.md` §5.*

**Never reset OA history by cloning** — this rule still stands and is *not* contradicted by §2B. Cloning to
escape a bad record is forbidden. Cloning to build a **new strategy identity to a written spec**, with the
original archived and the reason logged, is the sanctioned path. The distinction is whether a spec change
is being documented or hidden.

---

## 6. Optional research — not gating anything
- **`QQQ-IC-0DTE-Baseline` forensic.** −$31,580, 38% of the v1 fleet loss, never audited. Now concerns an
  archived bot and frozen data. Worth doing for the lesson; gates nothing.
- **Batch T1** (exit mechanic) and **Batch M** (middle-band coverage) per `backtest-ingest-protocol.md`.
- **Evidence-standards redesign** — Andy wants a scoring system beyond tiers+gates.
