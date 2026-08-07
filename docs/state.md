# State — Bot Fleet v2

*The live facts. Updated whenever a stated fact changes (CLAUDE.md §9.1). Numbers live in
`STATUS.md`; the plan in `docs/build-plan.md`; progress in the `bot-fleet-migration` tracker.
Last updated 2026-08-06 (decision-card-2026-08-06.md — all seven ruling slots decided by Andy;
gated propagation batch applied (G-1…G-6, U-1…U-4); double-testing RETIRE-SCOPED package applied;
regime-change finding corrected (B3 already exists — slot 6 needs Andy's fresh read); greenfield
build + mechanical sweep AUTHORIZED, deferred to a separate OA-touching session. NOTE: a second
session was editing `state.md`, `session-log.md` and `greenfield-family-spec.md` concurrently
tonight — every edit here was applied against a freshly re-read device copy immediately before
writing, so any content not authored by this session is that session's work, not an unexpected
diff.
Previously: 2026-08-05 part 2: the C0a probe — Architecture E CLEARED, C0a both clauses PASS,
C5 PASS, C11/C4/C6 answered, C10 still blocking ARM-B1; earlier the same day: propagation sweep +
the released gated batch — C12 and S-2 propagated to
every surface, D-1 propagated, `research-loop-spec.md` corrected ×6, §8.4 step 1 corrected on
explicit authorization; earlier the same day: R-edit package applied + edit-policy split).*

## 🔁 PROPAGATION SWEEP — 2026-08-05. Eight files reconciled to the 08-04/05 rulings.

*Ran because three independent sessions caught the same defect class: **a ruling that reached the
document it was recorded in and no further.** Every fix below is an evidence-backed correction
under `CLAUDE.md` §5 — dated banner, original struck not deleted, evidence cited as a fact ID or a
dated first-hand observation (never another project document), verified by direct `device_bash`
sha256 + single-match grep. **No decision was changed and no build was authorized.**
Full record, per-file hashes and the gated remainder: `session-log.md` 2026-08-05.*

**Applied (8 files):** `build-plan.md` §2D amendment block (C12 caveat only — nothing else in that
file touched) · `state.md` (this file: C12 ×2, greenfield hash, sweep record) ·
`greenfield-family-spec.md` §12 row 17 (C12) · `track-b-arms-spec.md` (§0, §1, §6.6 hash, §10 C13,
§11-1f, §11-1g, §12.3, ruling-index block) · `oa-reconciliation-report.md` R-11 (D-2 ceiling) ·
`oa-platform-reference.md` §5.2 (**"PT% as a Bot Input" status only — §8 untouched, and the
[DOCS-SILENT] Bot-Input tag is deliberately LEFT STANDING because greenfield check C0a rests on
it**) · `oa-ops-runbook.md` §7 (D-4 failsafe check) · `oa-export-schema.md` (`TIME_*` set).

**⭐ C12's discharge is now on every surface WITH its residual attached** — the
`[FIRST-HAND, UNCORROBORATED]` tier, both limbs (footer *accounting* ≠ OA *enforcement*; observed
at **one** archived bot where the sweep archives **twenty**), and the pre-declared reopen
condition. **A discharge propagated without its residual is worse than no propagation.**

**⭐ Two findings the sweep produced that were not on its list:**
1. **A propagation FLAG goes stale on the same clock as the thing it flags.**
   `track-b-arms-spec.md` §11 item **1g** said this file still carried the 7-of-8 and 0.10R
   figures. It did not — this file's owner had struck both **two minutes after** that spec was
   written. The flag was true when written and false within the same task. **Date-stamp the
   observation and name the hash you read it at.**
2. **This page's own greenfield hash was one amendment behind** (`da3c440e…` for a file that had
   moved to `e6dec33c…`), which is the same defect as the `track-b` §6.6 citation the sweep was
   sent to fix. **Nothing in this repository re-hashes a cross-reference.**

> ### ✅ THE GATED BATCH BELOW WAS RELEASED BY ANDY AND APPLIED, 2026-08-05, SAME DAY.
> **All four items authorized in one release; all four applied and device-verified.** **Three
> files new to the commit** — `pre-registration-ledger.md` · `reactivation-runbook.md` ·
> `research-loop-spec.md` — plus second edits to `oa-platform-reference.md` (§8.4, **explicitly
> authorized as a §8 edit**), `track-b-arms-spec.md` (§11-1f item (iv) closed), this page and the
> log, all four of which the sweep had already changed. **TWELVE files total for the commit.**
> - **S-2 count scoping propagated** to `pre-registration-ledger.md` §1 / §3 / §7 —
>   *"≈18–20 plan bots plus ≤8 Track B arms, ceiling 28"*, citing `build-plan.md` §2D's
>   `🔓 SCOPING AMENDMENT 2026-08-05`. **§11-1f item (iv) is now closed; all four surfaces are
>   propagated.**
> - **D-1 propagated** to `reactivation-runbook.md` Step C and `pre-registration-ledger.md` §6
>   from the memo's paste text (a)/(b): `PT% as a Bot Input` → **`the Exit-Options SET as a Bot
>   Input`**, with the **G2 rider** (the action stores a REFERENCE, not values — every capture
>   surface must read the input OBJECT; `oldValue` is a stale trap) carried into both.
>   ⛔ **C0a is preserved as the live blocker in both**, and §5.2's `[DOCS-SILENT]` Bot-Input tag
>   stays unstruck.
> - **`research-loop-spec.md`: six corrections.** §1a D-14 (`74 (19%)` → **101/394 = 25.6%**;
>   population relabelled 1,254 all-status / n=1,136 closed-only) · §5's gate `n` → R-4's signed
>   companion, **per (bot, variant)** · §5's *"12-variant count"* → §10a's permutation test, **no
>   Bonferroni** · **new §6 limit 5, the censoring block — the dangling `(§6.5)` reference is
>   resolved** · §5a items 1 and 3 status-corrected against R-1 and R-2.
> - **`oa-platform-reference.md` §8.4 step 1** — the last surviving *"shared by reference"* in the
>   tree, and it sat in the build instructions. Struck in place, replaced by the Library check.
>   **Nothing else in §8 touched.**
>
> ⚠️ **The spec corrections do NOT touch the engine.** `research_loop.py` is still `0.1.0-DRAFT`
> with **three fatal defects** (units × 100 × quantity · the tautological `CONTROL` · censoring),
> still **not wired into `daily.sh`**, and must not be. The `censored` flag depends on
> `bots_config_v2.csv`, so **Track A's honesty remains gated on Phase-2 config capture.**

⛔ ~~**DELIBERATELY NOT APPLIED — gated, and each needs Andy.**~~ **APPLIED 2026-08-05 — the list
below is the record of what was released, kept for audit:** `pre-registration-ledger.md`
§3/§1/§7 `≈18–20 active bots` (pre-registration text; needs the S-2 count scoping, not C12) ·
`reactivation-runbook.md` Step C and `pre-registration-ledger.md` §6 / §6-preamble
`PT% as a Bot Input`
(D-1 propagation — ready-to-paste text is in the memo) · `research-loop-spec.md` §5a items 1 and 3
(*"this amendment is unsigned"* / *"decide whether `TIME_*` keep their slots"*, both retired by
R-1/R-2) **and** the four consequential §5/§6/§1a edits from the review's §9 ·
`oa-platform-reference.md` §8.4's *"(§2 — shared by reference)"* (**§8 is gated**).
*(`build-plan.md` §2B was checked on the device and **carries no re-entry count** — R-11 named it
as a downstream surface; there is nothing there to correct.)* ⚠️ **All of these fail `CLAUDE.md` §5 condition 3 or 5:** their falsifying evidence is
*another project document* (a ruling), not a fact ID or a first-hand observation — or applying
them would change what gets built. **They are decisions, so they stay gated.**

## ✅ FOUR DECISIONS — ALL DECIDED 2026-08-04 (opened same day by Tier-2 verification)

> ### ✅ UPDATE 2026-08-04 (pilot part 4) — D-1's gates are CLOSED and D-3 is EXECUTED.
> **D-1 gates G1–G4 all answered** (detail: `session-log.md` 2026-08-04 part 4, finding 2).
> **G1 YES, server-confirmed** — an EMPTY Exit-Options bundle saves and survives a hard reload, so
> Option A can express the `ride` arm and the memo's G1 fallback is not needed.
> **G3 COMPATIBLE** — a bundle input and a named Preset compose on the same action.
> **G4 NO propagation** — the `exits` payload stores no preset reference at all [STRUCTURAL].
> **⚠️ G2 IS THE ONE THAT BITES: the action stores a REFERENCE, not values** —
> `{"type":"input","input":"IN…","text":"<label>","oldValue":{…}}`. A capture that reads only the
> action records the input's NAME. `bots_config_v2.csv`, the capture-diff and the drift detector
> must ALSO read the input object's value, or every arm diffs as identical. **`oldValue` is a trap:
> it is a pre-link snapshot and goes stale.**
>
> **D-3 EXECUTED 2026-08-04** (ruled to Claude's call; memo recommendation taken):
> **`itmpaper` = `market`**, verified by hard reload + `input.value` re-read, before/after
> screenshots in `data/captures/2026-08-03-pilot/06-clone-final/`. **`itmlive` UNTOUCHED at `auto`
> — that remains the Day-0 gate.**
> ⚠️ **New Day-0 watch item:** the setting closes ITM positions *"10 minutes before the close"* —
> the SAME instant as the bot's own Expiration exit, also Market. Two Market closes now aim at the
> same moment. Use `oa-ops-runbook.md` §4.4's timestamp-gap test.

*Read this block first. Each one is a product fact that invalidates something this project had
already decided or assumed. None can be closed by more research; each needs Andy's call.*

| # | Decision | What forces it | Where it bites |
|---|---|---|---|
| ~~**D-1**~~ ✅ **DECIDED 2026-08-04: Option A — Exit-Options-SET as a Bot Input.** Gates closed first: G1 YES (empty bundle saves, server-confirmed — the `ride` arm IS expressible), G3 compatible, G4 no propagation. ⚠️ **RIDER, forced by G2 (REFERENCE not values): every capture surface — `bots_config_v2.csv`, the capture-diff and the drift detector — must read the INPUT OBJECT, not just the action, or every arm diffs as identical; and `oldValue` must never be read as current config (stale pre-link snapshot).** | The 🔗 on the Exit Options row makes the **whole exit bundle** an input; there is no 🔗 on Profit Taking % or any single field. | `build-plan.md` §5.2 / §8.1. The only expressible form swaps entire exit configurations instead of tuning a number — a materially different mechanic. Plan is **frozen**, so this needs an explicit *"amend the plan"* either way, **including a decision to drop the bot-input idea**. ⛔ **DEFECT FLAGGED 2026-08-04 (in place, row not rewritten): `build-plan.md` has NO §5.2 and NO §8.1** — its headings run §1–§6 and the strings `5.2`/`8.1` return 0 matches in that file. Those anchors belong to `oa-platform-reference.md`; the same broken citation is replicated in `session-log.md` and `sprint-2026-08-04.md`. `PT% as a Bot Input` appears nowhere in the frozen plan, so **D-1 is not by itself a plan amendment** — the frozen text at stake is §2D's `arms differing / in exactly one input value`, and which option is ruled decides whether an amendment is needed at all. ✅ **RULED 2026-08-04 — ruling + the G2 rider recorded in `docs/decision-memo-2026-08-04.md`.** ⚠️ The broken-citation defect flagged above is **still unruled** and still present in three files. |
| ~~**D-2**~~ ✅ **DECIDED 2026-08-04: cap at 5 ICs/day, ONE bot.** Accept the platform ceiling; do not split a strategy across two bots to reach 10. Rationale: one bot = one config row = one pre-registration entry = one ledger identity, so the unit stays "condor" with no cross-bot aggregation and the drift detector keeps a single subject. Revisit only if a spec genuinely needs >5 entries in a session. | **Re-scope every re-entry spec to 5 ICs/day.** | `posLimitDay` / `posLimit` are **1–10 pickers**, no free-text path. An IC is two positions. | §3's [PROJECT-RULE] "ten IC re-entries = a daily limit of 20" is correct arithmetic and **unconfigurable**. Real ceiling is **5 ICs/day per bot**. Anything above that must be redesigned or split across bots. |
| ~~**D-3**~~ ✅ **DECIDED AND PART-EXECUTED 2026-08-04: `itmpaper` = `market` (done, hard-reload + `input.value` verified, before/after screenshots on file). `itmlive` = `market` is a HARD DAY-0 GATE — deliberately left at `auto`; it must be set before any capital is live.** | `itmpaper` = `itmlive` = **`auto`** — *"Calculate estimated P/L from underlying close price"*, which sends **no closing order**. `market` is the only option that closes. | **Day-0, hard gate.** A QQQ condor outliving its exits rides into **physical settlement**. Note `market` fires at **15:50** — same instant as the clone's Expiration exit; they would race. §13.1. ✅ **RULED 2026-08-04 — both slots recorded in `docs/decision-memo-2026-08-04.md`.** ⚠️ Day-0 watch item stands: two Market closes now aim at 15:50 (ITM action + the bot's Expiration exit) — use `oa-ops-runbook.md` §4.4's timestamp-gap test. |
| ~~**D-4**~~ ✅ **DECIDED 2026-08-04: RETIRED as the 2026-06-12 lapse cause. KEPT as a real, documented mechanism this fleet has tripped — March/April, on entry scanners. June cause: UNKNOWN.** | Newest error on either Fortress bot is **`Apr 16, 2026 3:55PM`**. Error days: Apr 16 (91) + Mar 16 (138+); `-NoPT50` Apr 16 (91). **Zero in June.** | §4.5 and every pre-registration entry that still carries it as the candidate cause of the 2026-06-12 lapse. The mechanism is real and this fleet tripped it — in March/April, on **entry scanners**. The June cause is still **unknown**. ✅ **RULED 2026-08-04.** Doc-by-doc carrier list, replacement wording and the ranked six-candidate shortlist with Day-0 discriminators: `docs/decision-memo-2026-08-04.md`. **Propagation NOT yet done.** ⚠️ Note for downstream sessions: **no pre-registration entry carries the failsafe as the June cause** — one mention only, PR-05's liveness kill criterion, which stays. |

**Also awaiting a call, lower stakes:** the two writes left on the clone by check #4 (preset
`TIER2-CHECK4-PUTSIDE`; `Fortress-ScannerA-PutSpread-CLONE` saved with a re-serialized `exits`
blob) — detail under *WRITES MADE TO THE CLONE* below.

> ### ✅ DECISION MEMO RULED 2026-08-04 — `docs/decision-memo-2026-08-04.md`. **ALL SEVEN DECIDED.**
> 886-line memo, 15 ruling slots. **Seven decisions ruled; four secondary slots left open and
> marked NOT RULED** (fix the broken §5.2/§8.1 citations · Day-0 no-touch ordering before the
> re-arm sweep · build the arm-distinctness assert · the ungrouped-export UI check). The
> re-serialized `exits` blob was **not separately ruled** and is recorded as unruled, not as
> ruled-by-silence.
>
> **D-1 → Option A**, Exit-Options-SET as a Bot Input, with the **G2 rider** (read the input
> object, never `oldValue`) — see the D-1 row above. **Decision 4 → Architecture E**, share the
> entry automation and differ on exits; consistent with D-1 as the coupling required.
> **Decision 5 → the Market-pricing ban extends to ENTRIES**, recorded as a **MECHANISM decision,
> not evidence** (n=1 position, n=2 fixture — below the T2 gate). **Decision 6 → re-price the
> 15:50 Expiration exit off Market, backstop keeps Market — ⏸ EXECUTION DEFERRED**: Template V1 /
> PR-03's config hash is frozen, so it lands as **Template V2 with an amended pre-registration
> before Day-0**, not as a quiet edit. **Decision 7 → RULED AND EXECUTED**: ScannerA name and tag
> reverted, preset `TIER2-CHECK4-PUTSIDE` kept, **Bot Group stays unset until the Phase 4 sweep**.
>
> ✅ **PROPAGATED 2026-08-06 — Andy granted "amend the plan" in full** (`decision-card-2026-08-06.md`
> ruling 1; YES, no items struck). Applied and device-verified (sha256 + single-match grep per
> file): `oa-platform-reference.md` (§7 entries-ban append, §8.1 D-1 append, §8.2 Decision-6
> append, §10 append, §4.5 cross-reference) · `build-plan.md` §2D (Range075 wording, ruling 1a,
> APPLY NOW) · `hedge-research.md` (§5.2 rule 3 flag, §10 entries-ban clause) ·
> `oa-ops-runbook.md` (§3 Architecture-E append, §5 trap 6 entries-ban + footnote) ·
> `reactivation-runbook.md` §1 (Excessive-Errors cross-reference). `pre-registration-ledger.md`
> needed no edit here — D-1(a) and D-4 carrier 7 were already applied 2026-08-05's gated-batch
> release. ~~NOT YET PROPAGATED — the rulings are recorded, the docs are not yet amended.~~
>
> **Three load-bearing findings remain open** (memo Appendix B has all seven): the broken
> `build-plan.md` §5.2/§8.1 citation, flagged on the D-1 row above and still present in three
> files · **"Range075 as a preset" looks unbuildable** — presets are an Exit Options object while
> `hedge-research.md` §8 specifies Range075 as an entry decision, hitting frozen §2D and §5.2
> rule 3 · **the arm-distinctness assert `oa-ops-runbook.md` §3 promises does not exist** —
> `execution_audit.py` has 13 rules and none is config-based, so §3 cannot be cited as a proof leg
> until it is built. ⚠️ **G2's REFERENCE result raises the stakes on the second and third:** an
> arm-matching proof that reads the action alone now returns identical for every arm.
>
> 📝 **N-1 (the broken §5.2/§8.1 citation) is STILL UNRULED as of 2026-08-06** — it was one of the
> memo's four secondary slots left open 2026-08-04 and was not in `decision-card-2026-08-06.md`'s
> seven slots either. Still present in `state.md` (this D-1 row), `session-log.md`, and
> `sprint-2026-08-04.md`. Not invented a fix here.

---

## 🗂️ DECISION CARD 2026-08-06 — all seven ruling slots decided by Andy. Six applied, one flagged.

`docs/decision-card-2026-08-06.md`, sha256 `5dda6b823998a54b457222e1387cc47da8fcb66edd0a07a54081fe73dcd1bb6d`
at delivery. Written the second-to-last day of Max capacity (downgrade 2026-08-07 14:52 ET), to
batch every open ruling so Andy rules once. Two of seven slots were adversarially reviewed before
presentation (subagents attacking slots 4 and 5); both original recommendations were **refuted**
and the card carried the post-review versions. **All rulings received and applied same-session,
2026-08-06**, except where noted.

**Slot 1 — propagation grant: YES, in full** (no items struck). Applied — see the
✅ **PROPAGATED 2026-08-06** banner above, replacing the stale NOT-YET-PROPAGATED block. Six gated
targets (G-1…G-6) + four ungated riders (U-1…U-3 applied above; **U-4, this section's own hash
refresh, applied in the GREENFIELD FAMILY SPEC block below**). **Slot 1a — Range075 wording:
APPLY NOW.** Applied to `build-plan.md` §2D as a new dated 🔓 amendment block (2026-08-06),
original left standing per the frozen-doc convention; reopens only if the preset-picker UI check
ever contradicts.

**Slot 2 — ledger count scoping: CONFIRMED, no action needed.** Verified in place 2026-08-06
(already applied 2026-08-05's gated-batch release).
**Slot 3 — PR-14…17 kill criterion: CONFIRMED, no action needed.** Verified in place 2026-08-06
(already replaced 2026-08-05, ruling S-5).

**Slot 4 — greenfield build session: AUTHORIZED, package items 1–8, with two amendments from
Andy:** (i) the OA build itself (Phase 0 probes onward) runs in a **separate session** — this
session applied doc edits only, touched no OA surface, ran no browser tool; (ii) sequencing per
slot 7 — C0b look → 2 deletions → C5 Library delete + exactly-one verify-back run **tonight**,
before Phase A, in that separate session. **Slot 4a — pilot declared CLEAN: Andy, 2026-08-06**, on
the ritual-complete record and the FINISH capture-diff no-unintended-edits verdict
(`reactivation-runbook.md` §3 Step A's gate). ⚠️ **QUEUED, not yet executed** — the separate OA
session that runs Phase 0 onward has not been opened by this session. The four decisions the
authorization finalizes (arm count = 7 / PR-14…20, the one-family reading of §2D, underlying QQQ,
ride = time-exit-only) are **ruled** as of tonight but **not yet stamped into
`greenfield-family-spec.md`'s own build-time literals** — deliberately left for the build session
per that spec's own "stamp literals at build time" convention (§9 preamble), so nothing here
duplicates or races that session's writes.

**Slot 5 — double-testing: RETIRE-SCOPED, package parts 1–4.** Applied: `research-loop-spec.md`
§10a (scoped-retirement paragraph + honesty line, signed spec, amended on Andy's explicit
instruction) · `greenfield-family-spec.md` §9 (dated note after PR-19) and §12 row 11 already
carried the finding, cross-referenced · `track-b-arms-spec.md` §5.5 and §6.3 (dated notes). Part 3
(no-influence rule carried into PR-14…20 / PR-21 / PR-22) is **written into the §10a append now**
but the ledger entries themselves are **DRAFT, unsigned** — the rule applies at signing, per the
ruling's own terms; no ledger edit made tonight.

**Slot 6 — regime-change conjunct: RESOLVED 2026-08-06, in two steps.** Andy's first ruling
(DEFER W/ TRIGGER, exactly as drafted) was **not applied** — mid-execution the card's premise was
found FALSE. **[FIRST-HAND 2026-08-06, direct `device_bash` read of `evidence-standards.md` §4
gate B3]**: a regime-change definition already existed — *"a VIX move of ≥ 10 points peak-to-trough,
or both a sub-15 and an above-25 VIX period"* — cross-referenced by that file's own T3.3. The
"undefined everywhere" claims the card's forcing facts were built on (`greenfield-family-spec.md`
§12 row 12, `track-b-arms-spec.md` §11 item 6) were themselves wrong; both corrected in place,
dated, original struck not deleted, verified by device sha256 + single-match grep (`CLAUDE.md` §5
evidence-backed-correction path — changes no decision). Flagged for Andy's fresh read rather than
silently substituting a decision.
>
> ✅ **Andy's fresh ruling, 2026-08-06: RATIFY B3 as the regime-change conjunct's definition** for
> `build-plan.md` §5 / `CLAUDE.md` §4's gate — **no new definition authored.** The deferral trigger
> survives, narrowed to the detector question: **B3 must be wired to a `scripts/` detector — or a
> recorded manual-evaluation protocol run at each review date — before the earlier of (i) any
> arm's/variant's first n=60 interim read, or (ii) 2026-11-30.** Until then, B3 is evaluated
> manually and every evaluation is logged (`session-log.md`, dated, citing the VIX read that
> settled it). Applied to `evidence-standards.md` §4 (the operative gate text) 2026-08-06.

**Slot 7 — mechanical sweep: GO, re-ordered.** C0b look + 2 deletions + C5 Library delete/verify-
back queued for **tonight**, before Phase A, in the separate OA session (slot 4(ii)). Three clones
+ the ~23 manual archives queued for **tomorrow morning**, pilot-clean gate (slot 4a) now
satisfied. ⚠️ **QUEUED, not yet executed** — no OA surface touched by this session.

**Files changed by this session, all device-hash-verified, none via git:**
`oa-platform-reference.md` · `build-plan.md` · `hedge-research.md` · `oa-ops-runbook.md` ·
`reactivation-runbook.md` · `research-loop-spec.md` · `track-b-arms-spec.md` (×2 passes) ·
`evidence-standards.md` · `greenfield-family-spec.md` · `state.md` (this file) ·
`session-log.md`. Full per-file before/after hashes in `session-log.md`'s 2026-08-06 entry.

⚠️ **Concurrent-edit note.** A second session was editing `state.md`, `session-log.md` and
`greenfield-family-spec.md` at the same time as this one tonight. Every edit in this session
re-read each of those three files immediately before writing and asserted the hash was unchanged
since that read (compare-and-swap, no `device_commit_files` mtime guard applicable since edits
went directly through `device_bash`). No collision was detected on any of the edits made here. Any
content in these three files not described in this section or in `session-log.md`'s 2026-08-06
entry is the other session's work, not an unexpected diff.

---

> ### 🔨 PHASE A STARTED AND **NOT FINISHED** — 2026-08-06 (late), the first OA BUILD session.
> **ONE of the three shared Library automations exists. NO BOT EXISTS. Phase A is OPEN.**
>
> **Built + Layer-1 verified after a hard reload:** `GF-ScannerA-PutSpread`
> (`RTfw5TkkCRF178605283747821`, version 3, Library state `Unused`, `Warnings 0`). Tree matches
> `greenfield-family-spec.md` §4.1 node-for-node. Action `open-shortputspread`:
> `exactly 0 days` · short put `0.75% below underlying price` · long put `$2.00 below short put
> leg` · **`amount` = 1 contract — the SIZING PRIMITIVE IN USE IS THE FIXED CONTRACT COUNT**, not
> the `$250 risk` fallback (stamp this in all seven MECHANISM blocks) · `price`
> `{"limit":100,"smart":"normal"}` — **not Market**, Decision 5 holds · `tags` `put side` ·
> `filter {"minPrice":0.08}` · `exits` = a **REFERENCE** to automation input `IN178605447966781`
> (`GF_EXITS_PUT`, type `exits`) — **the G2 rider reproduced first-hand on a new object.**
> **A7 baseline** `sha256(JSON{name,inputs,root})` =
> `d35307e54d10c3457b383cdb9106f703f7bee0f5ad3f9c664787b98fda871ec7`.
> Capture: `data/captures/2026-08-06-gfam/GF-ScannerA-PutSpread.txt`. First-ever rows written to
> `data/bots_config_v2.csv`.
>
> **NOT built:** `GF-ScannerB-CallSpread` · `GF-Backstop-1552-FlatClose` · presets (A6) ·
> **`GF-QQQ-IC-Ride` (Phase B never started)**. `GF-SiblingClose` correctly not built (C8 ruling).
> **Layer 2 is DEFERRED TO DAY-0 for every item** — account inactive, no positions, nothing fired.
>
> ⛔ **F-4 — DAY-0 BLOCKER: `SENTINEL-SL1` IS NOT EXPRESSIBLE AND IS UNSET.** §1.3 wants Stop
> Loss % = 1; **the `stoploss` picker floors at `-5% of credit` (`0.05`)**, 42 entries, no
> free-text [FIRST-HAND 2026-08-06, live modal enumerated]. `stoploss: 1` is **−100%**, i.e.
> **exactly the `GF-SL100` arm's value** — a sentinel indistinguishable from a real arm, which
> §1.3 forbids by name. The input was created with **Default Value = NONE** and the sentinel left
> unimplemented. **Andy must rule (0.05, or re-spec) before any arm's `AUTOMATIONS` goes ON.**
>
> ⛔ **F-3 — THE TRIGGER IS NOT PART OF A SHARED LIBRARY OBJECT.** The Library editor carries the
> tree only; a bot's Settings groups attached automations under `SCANNERS`/`MONITORS`, so trigger
> class — and the whole **Repeating / 15:52 / Mon–Fri / holidays-skip** config of §4.2 — is set
> **per bot at attach time**. **The backstop's 15:52 is therefore a per-arm hand-set surface on
> all seven bots**, and neither §8.2 step 6 (rid lists) nor §8.3 **A2** enumerates trigger config.
> **A2 needs a trigger clause or the family has an undetected matching hazard in its only
> backstop.** Spec text — Andy's, not amended here.
>
> ⚠️ **F-1 — the slot-4 gate surface.** `decision-card-2026-08-06.md` is an **unfilled** ruling
> sheet (lines 240–241 still read the option lists); the rulings live on **this page**. This
> session proceeded on this page and flags the divergence. See `session-log.md` 2026-08-06 (late).
>
> Also read first-hand and unchanged: `itmpaper` = `market` ✅ · `itmlive` = `auto` ✅ ·
> `maxexits` = `0` · Bot Schedule `09:31`/`5`, `09:31`/`1`. `/bots` = **33 active bots**;
> `My Automations` was exactly one row before the build, **two** after.

> ### ✅ UPDATE — 2026-08-07 (same session, continued late). Seven presets done, ScannerB built +
> **Layer-1 verified**, Backstop confirmed present. **Phase A is STILL OPEN — Ride not started.**
> Block above LEFT STANDING per the doc's own correction convention; read this banner with it.
>
> **Presets (A6) — all seven built, F-4-compliant (Default Value forced back to `None` on every
> one), each independently confirmed in the account Presets picker after a hard reload:**
> `GF-RIDE-EXITS` · `GF-PT50-EXITS` · `GF-TRAIL-EXITS` (Trailing Stop 40%/15% + Expiration
> 10min/Fast) · `GF-TOUCH0-EXITS` (Touch $0 default-Normal + Expiration 10min/Fast) ·
> `GF-SL100-EXITS` (Stop Loss % −100% credit default-Normal + Expiration 10min/Fast) ·
> `GF-CANARY-EXITS` (Profit Taking % 5% credit/Fast + Expiration 10min/Fast) · `GF-SL200-EXITS`
> (Stop Loss % −200% credit default-Normal + Expiration 10min/Fast).
>
> **`GF-ScannerB-CallSpread` now COMPLETE + Layer-1 verified after a hard reload**
> (`RTfw5TkkCRF178606271659881`, version 2, Library state `Unused`, `Warnings 0`). Tree mirrors
> ScannerA node-for-node through the Range075 gate, then diverges only where the spec calls for it:
> `Bot opened a position with call side today` (`postagtoday`) → NO → `Open Symbol Short Call
> Spread`. Action `open-shortcallspread`: `exactly 0 days` · short call `0.75% above underlying
> price` · long call `$2.00 above short call leg` · `amount` = 1 contract (same sizing primitive as
> ScannerA) · `price {"pct":100,"smart":"normal"}` — **not Market**, confirmed via the SmartPricing
> modal itself, not just the collapsed label · `tags` `call side` · `filter {"minPrice":0.08}` ·
> `exits` = a REFERENCE to a **newly created** automation input `IN178606782436781`
> (`GF_EXITS_CALL`, type `exits`, **Default Value = None, F-4 compliant**) — confirms automation
> inputs are per-automation, `GF_EXITS_PUT` was correctly NOT reused. **A7 baseline**
> `sha256(JSON{name,inputs,root})` = `bb4ba866a13e7ecd682f7bda9a19011003e9e3ef73fffd0fb64a80a4cd0eb32e`.
> Capture: `data/captures/2026-08-06-gfam/GF-ScannerB-CallSpread.txt`. Row appended to
> `data/bots_config_v2.csv` (now 2 rows).
>
> **`GF-Backstop-1552-FlatClose` confirmed present** in the Library list this session (`Unused`
> row) — built earlier in this same continued session; **not independently field-verified or
> captured in this pass** (no capture file, no CSV row yet — open item, next session's task before
> Phase A can be called done).
>
> **Still NOT built:** **`GF-QQQ-IC-Ride` (Phase B never started)** and the six research arms.
> `GF-SiblingClose` correctly not built (C8 ruling, unchanged).
>
> ⛔ **ACCOUNT-INACTIVE BANNER — RE-FLAGGED AND RE-ADJUDICATED, this session.** The
> "Account inactive, no changes will be saved until you select a plan" banner was re-raised as a
> possible save-blocker mid-session (found hidden in the DOM behind the full-screen editor overlay,
> not visible in screenshots). Andy ruled it pre-adjudicated (activates by design at Day-0; the
> session's own presets/ScannerA/Backstop work already passed hard-reload verification under it)
> and directed the decisive test: node Save → finish tree → top-level Save → hard reload →
> server-verify. **Result: PASSED.** The full ScannerB tree, every action field, and the new
> `GF_EXITS_CALL` input all persisted exactly as built. One transient false alarm during
> re-verification is logged for the record, not as a data-loss event: a second browser tab
> rendered the Automation Library as empty on its first cold load; re-navigating the same tab
> immediately after showed all four automations correctly, and Andy's own 10:12PM screenshot
> independently corroborated the correct state throughout. **Banner question closed for this
> account — treat it as cosmetic, not a save-blocker, going forward**, but keep doing the
> hard-reload check anyway (§9.1a — a save confirmation is still never verification).
>
> ⛔ **U-1 RESOLVED — NEGATIVE.** Trades-list rows carry no per-row pricing-mode label and no memo
> field (only description/qty/timestamp, a bid→fill price pair, an Automation Log link, "filled at
> $X"); the linked Automation Log detail view's Close Position action card likewise has none.
> **Consequence, per Andy's conditional ruling: G-1 reverts to HOLD.** The six research arms will
> be stamped uniform `{"smart":"normal"}` under G-1-HOLD, not per-arm pricing-mode tagging. The
> `exit_rows.csv` schema question re-presents post-downgrade with the degraded `(exit_ts,
> fill_price)` capture cost — **open item for the Ride/six-arm session, not resolved here.**
>
> ⛔ **RIDE DELIBERATELY NOT STARTED THIS SESSION.** Andy's instruction: after this banner
> re-flag/re-adjudication, treat it as a context-window-saturation signal and continue
> `GF-QQQ-IC-Ride` and the six research arms in a **fresh session**, against this close-out.
>
> F-1, F-3, F-4 (SENTINEL-SL1 unexpressible, Day-0 blocker) all **unchanged, still open** — see the
> 2026-08-06 (late) block above for full text.

## ⭐ GREENFIELD FAMILY SPEC — WRITTEN + AMENDED ×4 2026-08-04. Design closed; SIX blocking checks before build.

`docs/greenfield-family-spec.md` — **1,628 lines, sha256
`207517211f05de50f92ebadacc23e8974021f58a25fb8520fe823fd11fef83ee`**, on-device verified
**2026-08-06** (two more amendments tonight: §9 double-testing RETIRE-SCOPED note after PR-19,
§12 row 12 regime-change correction — both listed in the hash chain below).
📝 **CROSS-REFERENCE, 2026-08-06:** this block previously cited `99abab8f…` (1,585), one close-out
behind — the C0a-probe session amended the file further after that close-out (source unclear from
this session's reads; treat as the same "hash goes stale" class flagged just below). **This is a
snapshot at read time, not a fact that stays true** — see the standing warning two lines down.
📝 **CROSS-REFERENCE CORRECTED 2026-08-05** — this block previously read *"AMENDED ×3"* /
*"AMENDED THREE TIMES"* and cited **`da3c440e…` (1,585)**, one amendment behind.
**[FIRST-HAND 2026-08-05, `device_bash sha256` of the device file.]**
**Content claims about the spec elsewhere on this page were re-verified and stand; only the hash
moved.** ⚠️ **Treat an embedded hash as a timestamp, not a fact** — cite a file's content claim
and the date it was read.
📝 **AMENDED SEVEN TIMES after writing** — the first five per the chain already on record: as-written
`aee1d763…` (1,548) → R-1/R-3 correction `84ea156a…` (1,558) → 15:44 gate move `d9c686ac…` (1,584)
→ S-1 slot correction `da3c440e…` (1,585) → §12 row 17 closed at close-out `e6dec33c…` (1,585) →
C12 discharge propagated into §12 row 17, 2026-08-05, `99abab8f…` (1,585) → **§9 double-testing
RETIRE-SCOPED note added, 2026-08-06, `0797de38…` → intermediate** → **§12 row 12 regime-change
correction, 2026-08-06, `20751721…` (1,628, current)**. Full record: `session-log.md`
2026-08-04 *amended three times post-write* + *Amendment 4*, 2026-08-05 *propagation sweep*, and
2026-08-06 *decision-card rulings applied*.
⚠️ **Treat an embedded hash as a timestamp, not a fact** — cite a file's content claim and the
date it was read.
**The design document Phase 4's fresh builds are built from.** It **implements** `build-plan.md`
§2D and §5 — no frozen doc was edited, no OA surface touched, no git command run.

**Seven bots as ONE matched family, not two builds.** The "greenfield IC family" and the "rebuilt
hedge tournament arms" are two views of the same family, which is what fits 4 IC arms + 2 hedge
arms + 1 canary inside §2D's 5–7 fresh ceiling with no remainder. Underlying **QQQ**. Arms:
`GF-QQQ-IC-Ride` (control, PR-14) · `-PT50` (PR-15) · `-Trail` (PR-16) · `-Touch0` (PR-17) ·
`-SL100` (PR-18) · `-SL200` (PR-19) · `-Canary` (PR-20). ~~Four~~ 📝 **THREE (2026-08-06 — C8 ruling
removed `GF-SiblingClose`)** shared Library automations attached
to all seven; the only per-bot variable is a bundle-typed exit input, per D-1 Option A and
Decision 4 Architecture E.

> ### ⛔ DO NOT START THE BUILD. Phase 0 has SIX blocking checks and one can stop the architecture.
> **C0a — the BOT INPUT tier has never been observed.** G1/G2/G3 all tested the *Automation*
> Input; this file's own bot-input line is *"Inference from a screenshot"*, and
> `oa-platform-reference.md` §5.2's *"Whether Exit Options can reference Bot Inputs is
> [DOCS-SILENT] and unverified"* is unstruck. **If C0a fails, Architecture E is not buildable and
> the tournament architecture returns to Andy — do NOT fall back to per-arm copies**, which void
> the tournament at build time under PR-18's kill criterion.
> Also blocking: **C0b** (can one input span two automations — expected NO, hence two inputs per
> arm) · **C0c** (presets inside the input editor) · **C1** `stoploss` unit · **C2** `tstop` shape
> · **C3** exit-pricing sub-fields · **C7** the `opened today` entry gate · **C8** the
> sibling-close nodes. C7 and C8 also carry explicit no-substitution STOPs.

> ### ✅ SUPERSEDED IN PART, 2026-08-05 (C0a probe session). The block above is LEFT STANDING as the
> state it was written in; these are the answers.
> **⭐ C0a PASSES ON BOTH CLAUSES. Architecture E is buildable and does NOT return to Andy.**
> - **Clause one — the BOT INPUT tier exists and is typed `exits`,** the whole bundle. Bot input
>   `IN178588971538691` on the TEST clone, read from `a5.bots.bot.inputs` after a hard reload.
>   The control is on the **bot's** automation row → ⚙ Edit Settings → the 🔗 beside the input →
>   menu `Bot Inputs` → `Add Bot Input`. **G1/G2/G3 missed it because they searched the automation
>   scope for a control that only renders in the bot scope.**
> - **Clause two + C5 — one Library automation, two bots, DIFFERENT values.**
>   `rid RTfw5TkkCRF178589028977611` and automation input `IN178589048006251` are **identical** on
>   both scratch bots; the bot inputs are **distinct** (`IN178589092511981` = `Profit: 25%` vs
>   `IN178589106268631` = `Profit: 75%`). **Attach, not copy.** Library page agrees: `2 bots`, one rid.
> - **C11 — `dstop` HAS its own pricing sub-field `smdstop`, defaulting to `{"smart":"normal"}`,
>   NOT `market`.** Every exit mechanic has an `sm*` sibling — **this answers C3 too.**
> - **C6 — a non-empty bundle IS accepted as a Default Value.** **C4 — `1 contract` IS selectable.**
>   **C1 — Profit Taking % is `% of CREDIT`** *(this does NOT close C1, whose literal subject is
>   `stoploss`'s unit — that was not read)*. **C0b — YES by implication only** (one BOT input drove
>   two automations on one bot); the literal question, one AUTOMATION input spanning two automations,
>   **is still worth one direct look.**
> - ⛔ **C10 REMAINS OPEN AND BLOCKS ARM-B1.** The `dstop` modal is headed `Stop Loss Amount`, unit
>   marker a bare `$`, `step=1`, no min/max/suffix/helper/tooltip and **no per-contract vs
>   per-position qualifier anywhere.** The prescribed method returns nothing. `dstop` persisting as a
>   **negative** number is *suggestive* of a position-level P/L threshold and is **inadmissible as the
>   answer** (`CLAUDE.md` §5 — inference is not observation). **Needs a Day-0 behavioural read
>   against a known contract count.** `<D100>` cannot be derived and PR-21 cannot be re-stamped.
> - **Still untouched:** C0c · C2 · C7 · C8 · C9. Full record: `session-log.md` 2026-08-05 part 2.

> ### ✅ PHASE 0 CLOSED — 2026-08-06, the second probe session. Both blocks above are LEFT STANDING.
> Every remaining check answerable in the UI is answered. First-hand DOM / value-layer reads on the
> delete-list scratch bot `BOTfw5TkkCRF2217852702121253931`, filed to
> `data/captures/edit-verify/2026-08-06/phase0_C1.txt · _C2 · _C7 · _C8 · _C0bc · _C9`.
> Full record: `session-log.md` 2026-08-06.
>
> - ✅ **C1 CLOSED — `stoploss` is `% of CREDIT`.** Control label `Stop Loss %`; picker enumerates
>   `-5% of credit`=0.05 … `-100% of credit`=1 … `-200% of credit`=2 … `-500% of credit`=5.
>   **SL100 = `stoploss: 1`, SL200 = `stoploss: 2`.** PR-18/PR-19's re-stamp condition (*"IF THE
>   CONTROL IS %-OF-RISK"*) is **NOT triggered** — both were written against the credit basis.
>   `dstop` is the separate `Stop Loss $` control; **C10 stays open.**
> - ✅ **C2 CLOSED — an ARMING THRESHOLD EXISTS and is NATIVE.** `tstop` opens a sub-form:
>   `target` (min 0, step 1, ph 50) = "Activate at __ **% of credit**"; `trail` (min 1, step 1,
>   ph 15) = "Close on __ **% pullback**"; optional `minr` and `maxtrail`. **"Arm @ 40%, trail 15%"
>   is expressible.** ⭐ **RULED 2026-08-06 (Andy): PR-16 RE-SCOPED TO THE ARMED TRAIL**, target=40 /
>   trail=15. This falsifies the §11-rows-4-and-6 exclusion *as applied to the armed trail* — those
>   rows bound decision nodes, not native exit primitives. ⚠️ Whether a *plain* non-armed trail is
>   expressible was **NOT** observed; do not assume it.
> - ✅ **C7 PASS — the node is real, and is already running on this account.** Recipe `postagtoday`
>   (group Bot): `Bot [opened|closed] a position with [tag, limit 1] today`. Corroborated live:
>   `HedgeC-Scan-Call` contains "Bot opened a position with call side today" → NO → Open.
> - ⛔ **C8 — STOP RETURNED ON CLAUSE 2.** Clause 1 (`posrepeater` inside a `Position closed`
>   automation) and clause 3 (`posopendays`, `zero:true` = "open 0 market days") are **real**. But
>   **the closed position is NOT an addressable referent**: the picker offers only `Lookup a
>   position` (literal Symbol/Type/Tag filters) and `Opened Position`, greyed — *"Only available in
>   automations scheduled with the 'position opened' trigger"*. No recipe compares a tag to another
>   position's tag. Scopes opened: bot · automation · top-level referent picker · in-loop binding ·
>   Position Lookup · all 127 recipes in all 6 groups. **⭐ RULED 2026-08-06 (Andy): BUILD WITHOUT
>   SIBLING-CLOSE** — the spec's named fallback; **the spread, not the condor, is the unit for early
>   exits.** See `greenfield-family-spec.md` §4.3.
> - ✅ **C0c PASS** — a `Presets` picker DOES render in the bot-input value editor; enumerates
>   `TIER2-CHECK4-PUTSIDE` = `UIfw5TkkCRF1517858152565216101`. B4 is not seven manual entries.
> - ✅ **C0b LITERAL — the answer is NO.** `HedgeC-Scan-Call`'s Exit Options 🔗 panel reads *"Select
>   an existing input or add one to **your automation**"* and **"No compatible inputs found."** —
>   `CLAUDE-G1-EMPTY-EXITS` (`IN178586615441261`), same bot, sibling automation, same `exits` type,
>   is **not offered**. Two-input design stands; **assert A8 stays substantive.**
> - ⏳ **C9 — NOT ANSWERABLE IN THE UI. Day-0, same class as C10.** Only copy is *"After the bot
>   closes a position"*; the trigger exposes a `Position Type` filter and no "closed by" filter.
>   That it says "the **bot** closes" is **suggestive and inadmissible** (`CLAUDE.md` §5).
> - ⏳ **`oa-ops-runbook.md` §7's template successor-rid check — NOT RUN.** It needs either a
>   template saved from a delete-list bot (fresh account-level residue on the eve of the sweep) or a
>   production bot, which this session was barred from. Ops check, not a Phase 0 blocker.
>
> ⭐ **ALL SEVEN ARE NOW ARMS.** C1 + C2 confirm the last two unconfirmed primitives; C3 closed the
> pricing sub-field on 2026-08-05. **§8's row-4 objection is discharged.**
> ⛔ **C8's STOP is a SHARED-OBJECT cut, not an arm cut** — Phase A now builds **THREE** shared
> automations, not four, and the post-Phase-A Library holds **4** rows, not 5.

**⚠️ AMENDED 2026-08-05 — the G2 rider is now TWO hops, not one.** Once a param is driven by a bot
input the chain is action → automation input → **bot input**, and the binding record carries only the
bot input's **id and label** plus a stale `oldValue`. A capture that stops at the action reads one
name; a capture that stops at the automation input reads another. `bots_config_v2.csv`, the
capture-diff and the drift detector must resolve **both** hops or every arm diffs as identical.

📝 **RESOLVED 2026-08-06 — ALL SEVEN ARE ARMS.** C1 (`stoploss` = % of credit), C2 (`tstop`'s armed
sub-form) and C3 (pricing sub-fields, 2026-08-05) confirm every primitive. Left standing:
~~**⚠️ Three of the seven are not arms yet** under `hedge-research.md` §5.2's own definition —
Trail's `tstop` shape, SL100/SL200's `stoploss` unit, and four arms' exit-pricing sub-field are
unconfirmed primitives. §5.2: *"An arm failing any of these is not a weak arm, it is not an arm."*~~

**Adversarial review: 2 subagents, 10 FATAL + 24 MATERIAL objections, ~2/3 fixed.** Full record in
the spec's §11, including the attacks that failed. **Two structural limits are CARRIED, not
fixed:**
- **CF-1 — the exit-pricing regime is confounded with the arm variable.** The ITM Market action
  and the 15:52 Market backstop reach only positions still open at 15:50/15:52, so `Ride`/`PT50`
  are heavily exposed to Market fills while `Touch0` is ~never exposed. The arms hypothesising
  "capping the tail helps" are the arms spared the fleet's worst execution mechanic. **`auto` does
  not help — there is no `itmpaper` value under which the tail measurement is arm-neutral.** This
  is `hedge-research.md` §5.1 defect 2 in a new form and it bounds what the family can conclude.
- **CF-4 — sibling-close destroys the anchor PR-18 imports.** Sandvand's rung is called
  *Breakeven* because the untested side decays to zero; close-both forfeits that, so the arm
  cannot reach breakeven by construction. Renamed in substance to "SL100-close-both"; **do not
  publish it under the anchor's name.**

**Six findings for Andy, none acted on:**

1. **§2D's arithmetic is ambiguous** — "IC family (4–6)" + hedge arms + canary vs "5–7 fresh".
   Resolved by the one-family reading; **a two-family reading needs an amendment.**
2. **⛔ `pre-registration-ledger.md` PR-14…PR-17's family-level kill criterion is vacuously
   unfireable.** It reads "more than one differing **input**"; under Option A each arm holds
   exactly one exit input, so that state cannot be reached — the identical defect the memo used to
   *reject* Options B and C. **It survived the D-1 ruling unnoticed.** The spec rewrites it at
   field granularity; the ledger needs the same correction at signing.
3. ~~**`research-loop-spec.md` §10's signed 0.10R margin is unreachable here.**~~ ✅ **RESOLVED
   2026-08-04 by ruling R-3** — 0.10R replaced by mean ΔR ≥ **+0.015R** per position + paired
   bootstrap 95% CI excluding zero + paired sign test on the fired subpopulation; median test
   withdrawn. **+0.015R < R_max at every credit this structure admits**, and R-3 reached the same
   defect independently from the fleet-median side. ⚠️ **But the power problem is SHARPER, not
   softer** (new spec §12 row 16): +0.015R is also the largest effect this program has ever
   measured (SL75, n=1,254) and sits *below* the family's CI half-width at n=100 (±0.026R paired);
   ≈307 paired matched days are needed to resolve it, ≈560 under Bonferroni. **Also: R-3's test is
   per position over a bot's full population; the family's is per condor, day-paired, matched days
   only. Different statistics — do not score the family against R-3's gate without restating it.**
4. ~~**The family consumes 7 of the 8 signed Track B slots**~~ 📝 **SUPERSEDED 2026-08-04 by
   ruling S-1** (`track-b-arms-spec.md` §3.3): *"the seven family bots are `build-plan.md` §2D
   fresh builds; Track B's 8 slots are yours, `n_used=20` confirmed."* **Separate allocation —
   Track B keeps all 8**, `n_used = 20` confirmed by ruling. ⭐ **THE SECOND CLAUSE STANDS AND IS
   STILL OPEN:** `GF-SL100`/`GF-SL200` duplicate signed Track A §3 variants and **pool error rates
   nowhere** — one hypothesis, two engines, no shared multiplicity accounting; ARM-B1
   (`DSTOP_100`) has the identical defect. **S-1 unblocked the allocation; it did not touch the
   double-testing.**
   ~~⭐ **NEW, opened by S-1's arithmetic (spec §12 row 17): the end-state count breaks under EVERY
   reading.**~~ ✅ **RESOLVED — the amendment LANDED 2026-08-05, within the hour.**
   `build-plan.md` §2D now carries a **`🔓 SCOPING AMENDMENT 2026-08-05 — "amend the plan",
   Andy's explicit words`** block naming Track B as a **separate allocation**, citing this spec's
   §12 item 11 as the finding that forced it. Operative figures: *"≈18–20 plan bots · wave-1
   Track B spend **2** · **ceiling 28**"*. The plan-bot arithmetic is unchanged; what changed is
   that Track B is now **named** rather than silently colliding with the count.
   ⚠️ **The amendment scopes a count and authorizes no build** — every Track B arm still needs its
   own signed pre-registration. ~~⛔ **STILL BLOCKING: C12**, whether ARCHIVED bots count against the
   Pro 50-bot cap. The headroom claim rests on the reading that they do not, and the amendment says
   *"that reading is not verified"*: if they do, Day-0 is 36 + 7 = **43** and ≤8 does not fit
   (43 + 8 = 51).~~
   ✅ **C12 DISCHARGED — propagated here 2026-08-05.** **[FIRST-HAND 2026-08-04, `/bots` footer
   read]**: `35 active bots • 15 left in your plan`, read read-only immediately after the archive
   (it had read `36 active bots` through three failed attempts). **35 + 15 = 50** — the complement
   is computed against the **ACTIVE** count, so **archived bots do not consume slots.** Wave 1 is
   **22 of 50**; the `43` / `43 + 8 = 51` arithmetic struck above is **void**.
   ⚠️ **RESIDUAL, carried not dropped — [FIRST-HAND, UNCORROBORATED].** This is the footer's
   *accounting*, not OA's *enforcement*: `left = 50 − active` renders identically under both
   hypotheses, and it was observed with **one** archived bot where the Group-A sweep archives
   **twenty**. ⛔ **Pre-declared reopen: if a build ever fails at the cap despite archived bots
   existing, C12 reopens** and the ≤8 allocation is re-derived against an observed slot count.
   Full evidence block: `track-b-arms-spec.md` §3.2.
5. **No regime-change criterion exists anywhere** — `build-plan.md` §5's gate is conjunctive and
   the third conjunct is undefined in every document.
6. **`oa-ops-runbook.md` §3 has an internal tension** — `Group = Pillar` vs "arms live in one
   group so they can be queried as a set". Resolved operationally (Group `IC`, cohort tag `gfam`);
   §3's wording flagged, not amended.

**N-3 is confirmed binding.** The arm-distinctness assert §3 promises still does not exist, so §3
may not be cited as a proof leg. The spec specifies it as rules **A1–A8** and places it before
Day-0 — noting that whether it *must* precede trading is one of the memo's four unruled slots.
**N-2 handled without an amendment:** Range075 is implemented as two Symbol-change-% decision
nodes in the shared entry automation, the substitute primitive named explicitly.

> ### 📝 AMENDED 2026-08-04 — `GF-SiblingClose` gate moved **15:50 → 15:44**. Ruled. PHASE A.
> Source: `track-b-arms-spec.md` §6.6, which found the defect and correctly declined to apply it
> to a shared object it could not amend. **`before 3:50pm` was not tight enough.** ARM-B2
> (`expdays 0.015`) closes both legs at ~**15:45**, which **is** before 15:50 — so leg 1's fill
> fires `Position closed`, sibling-close issues a `patient` close on leg 2 **while leg 2's own
> `speedy` Expiration order is still working** (N-6: exit-option orders stay live two minutes).
> The 7/01 orphan-loop shape at 15:45. **It bites that arm and NOT its Ride control, so it is a
> mechanic difference between arm and control** — a confound in the one comparison the arm exists
> to make, not merely an operational risk.
> **Cost:** a trigger firing in **[15:44, 15:50)** on the five triggered arms leaves the sibling
> until its own 15:50 Expiration exit — the condor still closes, at worst six minutes later, **no
> orphan.**
> ⛔ **Ten dependent references in the spec, not one** — tree, rationale, interlock 2, §6.2 Rule 0,
> §8.5 artifact, C9, build step A4, PE-7, PE-8. Editing the diagram alone would have left eight
> passages contradicting it.
> ⛔ **It mutates a SHARED object: apply in Phase A BEFORE any arm is switched on**, never as a
> later edit, and take a **fresh A7 payload-hash baseline** with re-verification of every attached
> arm. Applying it post-Day-0 would splice two experiments into one sample — what A7 exists to
> detect.

---

## Research loop — ALL 7 RULINGS SIGNED 2026-08-04, spec amended, ⛔ STILL DO NOT WIRE IN

`docs/research-loop-spec.md` is signed **and amended 2026-08-04** by Andy's seven rulings.
`scripts/research_loop.py` is **`0.1.0-DRAFT`, NOT frozen**, 23/23 validation checks, writes
`data/counterfactuals.csv` and nothing else, silent below n=30. **It is not wired into `daily.sh`
and must not be — the rulings fixed the SPEC, not the ENGINE.** Three fatal code defects stand.

**Review: `docs/research-loop-review-2026-08-04.md`** (three adversarial reviewers; 27 quotes
byte-exact single-match; every figure recomputed from the n=1,386 capture). Five §5a defects ruled,
nine further defects recorded. **Three fatal, all still unfixed in code:**

- **every `cf`/`delta` is off by 100 × quantity** — `credit` is a per-contract price, `pnl` is
  dollars, `quantity` is never read. `delta ≈ -pnl` on every FILLED row; `DSTOP_*` fires 0/1,254
- **`CONTROL` is a tautology** — `abs(pnl - pnl) < 1e-9`; the self-test compares a variable to
  itself, so it did not catch the units bug
- **MFE/MAE are censored by the incumbent exit** — Track A can only evaluate variants TIGHTER than
  the bot already runs. MFE ≥ 0.70 on 65/80 for unstopped `Raw-HoldToExp` vs **0/70** for the PT25
  `-130PM` clone (median MFE 0.250). Not fixable in code

**Rulings, all SIGNED 2026-08-04 and applied to spec §3/§10 as dated amendments:** R-1 fixed-$ rungs
→ dollar stop at 1.00×/1.50× the bot's trailing-90-day median credit (the unsigned 0.50×/0.75× RISK
substitution is REJECTED) · R-2 `TIME_*` replaced by trough-timing rungs, time question retired to
Track B · R-3 margin → mean ΔR ≥ +0.015R, **median test withdrawn** · R-4 start condition → n ≥ 30
closed POSITIONS fleet-wide · R-5 → new §10a, permutation max-T, **no Bonferroni term** · R-6 unit
of account is the POSITION and **combined MFE for a paired condor is a Track B question** · R-7
`expired` stratified. **The §3 set remains 12, so the freeze holds without a count change.**

⚠️ **Four consequential edits NOT applied** (outside the §3/§10 authorisation) — spec is internally
inconsistent until ruled: §5's `n ≥ 100 positions` line · §5's `12-variant count` phrase · §6's
censoring limit, which R-2's applied text already references as `(§6.5)` — **that reference
currently dangles** · §1a's `74 (19%)` figure, correctly 101/394 = 25.6%. Listed in the review's §9.

**Next on the engine, in order:** fix units + `CONTROL` before anything else, add real-row VALUE
assertions to the fixture, then the `censored` flag — which **depends on `bots_config_v2.csv`** to
know each bot's incumbent exit, so Track A's honesty is gated on Phase-2 config capture.

**Track B is the better half and is unstarted:** run the variant as a real paper bot rather than
simulating it. Pro allows 50 bots, the fleet uses ~20, Day-0 is paper, so a slot costs only
configuration. Cap ≤8 slots. **First arms go on the LOSS side** (`Stop Loss $`, `Touch`) — both
confirmed to exist 2026-08-04, and the mirror baseline independently says the tail is where the
money goes. **Nothing in the review applies to an arm** — every finding is a limit on Track A, so
the review argues for starting Track B sooner, not later. R-2 and R-6 now put two further questions
in Track B by ruling: the time exits, and combined MFE for paired condors.

## Data conventions — `docs/oa-export-schema.md` (new 2026-08-04)

Machine-verified, **0 mismatches on 1,386 rows**. The one that bites: **`premium` is SIGNED and
negative for every credit structure**; use `openPrice` (positive on 1,386/1,386) for a magnitude.
`build_ledger.py` already writes the ledger's `credit` from `openPrice`, so anything reading
`trades.csv` is safe — but a harness mapping straight off the raw export is not, and one did.
Also: **`returnPct` is return on CREDIT, `ror` is return on RISK.** `CLAUDE.md` §4's R convention
is the **`ror`** basis. Do not grab the wrong denominator.

## Mirror baseline — WRITTEN 2026-08-04, do not recompute

`data/mirror_baseline.csv` via `scripts/build_mirror_baseline.py` + receipt. 174 positions, 10
mirrors, zero excluded. **It is an anchor, not a metric** — the script refuses to overwrite without
`--force`, because recomputing it against a later export silently moves the baseline every future
comparison is measured against. Finding: **four mirrors have positive median R and negative mean
R** — they win most trades and lose money.

## ⚠️ `bots_config_v2.csv` is BLOCKED, not neglected

A 2026-08-04 session called it the oldest neglected deliverable. **Wrong.** The `/bots` roster
capture carries names and P/L and **no Exit Options values**, and the file describes the
*post-Phase-4* fleet, which does not exist yet. It is written **per-bot as each bot is built**, not
as a big-bang extraction. Do not queue it as a standalone task.

## Account
- OA subscription **INACTIVE**. Andy reactivates **~mid-Aug**. The reactivation date is
  **Day-0 = `LEDGER_START`**.
- No new entries since 7/02. **5 multi-day mirror positions were still open** at the 7/30
  capture (`QQQ long call` ×4, `Tasty Condor` ×1) — ride-or-close is an explicit Day-0
  decision (`reactivation-runbook.md` §4 Step 2). Per the straddle rule they resolve into the
  mirror baseline layer, never the working ledger.
- **Edits made while inactive persist** (verified empirically 7/29→7/30). **Extended 2026-08-03:
  bot CREATION persists** (roster 35→36), automation renames persist, and — part 2 —
  **automation CREATION and ATTACHMENT persist through a hard reload.** OA's "no changes will be
  saved" banner is false.
- Andy has confirmed **both dashboard toggles (`AUTOMATIONS`, `EXIT OPTIONS`) are OFF on all
  35 bots.** The lapse mechanism and its Day-0 consequences: `reactivation-runbook.md` §1,
  `oa-platform-reference.md` §10.

## What is built
- **The ledger stack is code.** `build_ledger.py` refuses to run without `LEDGER_START`,
  filters on `open_date`, routes straddlers to `data/straddlers.csv`, writes run receipts.
  `scripts/execution_audit.py` passes its 12/12 validation matrix. `daily.sh` is 8 stages
  (drift audit at stage 3) and degrades cleanly at n=0. `STATUS.md` and `dashboard.html`
  generate at n=0 — **empty by construction, not by failure.**
- **Phase 3's document set is complete.** The pilot-clone card
  (`pilot-clone-card-qqq-fortress.md`) is written and is **partly executed** — see Open items.
- **The pilot clone EXISTS in OA**: `QQQ-IC-0DTE-Fortress Clone`,
  bot_id `BOTfw5TkkCRF2717857919585029021`, allocation $100,000, limits 2/2, `AUTOMATIONS` OFF,
  `EXIT OPTIONS` ON. It cannot trade. The original `QQQ-IC-0DTE-Fortress`
  (`BOTfw5TkkCRF817734373392552121`) is **untouched and verified so**. Roster is now **36 bots**.
- **The 15:52 backstop is BUILT on the clone** (2026-08-03 part 2):
  `Fortress-Backstop-1552-FlatClose`, automation id `RTfw5TkkCRF1785795329406099999991`.
  Repeating trigger, `Every week on Mon-Fri, 3:52pm EST`, `holidays=skip`, no end date;
  tree = Positions loop (unrestricted) → Close Position (`Market`, 100%, memo
  `1552 backstop flat close`). Warnings 0. **Verified by hard reload, not by the save message.**
- **Folder cleanup in progress** (approved 2026-08-03): Block 1 done — 16 v1-history docs
  removed, `docs/history-index.md` added. Block 2 = this page + the CLAUDE.md rewrite.
  Blocks 3–4 (ops-doc trims, reference merges) deferred until after the pilot / Day-0.

## Not built yet — do not go looking for them
- `data/bots_config_v2.csv` (Phase 2 — written from capture, never by hand). See
  §`bots_config_v2.csv` is BLOCKED, not neglected — it is written **per-bot as each bot is built**.
- ~~`data/mirror_baseline.csv` (one-time frozen mirror snapshot, built from
  `data/captures/oa_export_positions_2026-07-30.csv`, **not** from the archived ledger).~~
  ⚠️ **CORRECTED 2026-08-05 — this limb was stale and contradicted this same file.**
  **[FIRST-HAND 2026-08-04: `data/mirror_baseline.csv` written via
  `scripts/build_mirror_baseline.py` + receipt — 174 positions, 10 mirrors, zero excluded.]**
  It **exists**. See §Mirror baseline — WRITTEN 2026-08-04, do not recompute.
  ⛔ **Do not rebuild it.** It is an anchor, not a metric; the script refuses to overwrite without
  `--force`, because recomputing it against a later export silently moves the baseline every future
  comparison is measured against.
- The liveness check is half-done: the `SILENT_BOT` rule ships, but the bot-log side needs a
  log source the detector does not have.

## Day-0 first action
**Set `LEDGER_START` in `build_ledger.py` before anything else.** Then
`reactivation-runbook.md` top to bottom.

## ⭐ DAY-0 RUNBOOK AUDIT — 2026-08-05. 36 findings. ✅ ALL 28 GATED ITEMS RULED AND APPLIED SAME DAY.

> ### ✅ RELEASE SHEET RULED IN FULL 2026-08-05 — D0 through D6, all RELEASE. Applied and verified.
> `docs/day0-release-2026-08-05.md` (28 items → 7 decisions). **Every one released.** The runbook
> went **223 → 801 lines**; `STOP` went from **0 occurrences to 11**; **6 fleet-halt branches** now
> exist where there were none. Applied hash `919349b6bc5f1e46`, 13 anchored single-match edits, all
> verified by direct `device_bash` sha256 + single-match grep.
>
> - **D0 — the no-touch observation: OBSERVE FIRST.** The `NOT RULED` slot is now ruled. New
>   **Step 2c**, placed before any toggle moves, with all three branches. ⚠️ Account settings are
>   explicitly carved out as *not* toggle intervention, so Step 0a does not spoil it.
> - **D1 — propagation, all three.** `itmlive` = `market` is now **Step 0a**, a hard gate before
>   capital is live · **Template V2** is §2 step 6a and a ⛔ checklist box · the fleet count is
>   ≈18–20 plan bots **plus ≤8 Track B arms, ceiling 28**.
> - **D2 — the failure-branch set, FULL version with fleet-halt branches.** §4 opens with a
>   how-to-read block defining *bot stays OFF* vs *fleet stays OFF* and **"a check you could not run
>   is NOT a pass."** §1's heading corrected from *"ANSWERED"* to **EXISTENCE ESTABLISHED, CAUSE
>   STILL UNVERIFIED**, with **Step 6a** added to settle it and a full REFUTED branch.
> - **D3 — the swap, and the nine are NOT exempt from Step 6.** Step 3 arms **`EXIT OPTIONS` only**;
>   `AUTOMATIONS` → ON moved to **Step 7**, per bot, only for bots that passed. The exemption
>   question is now answered in the document: *"a pre-existing bot is not a proven bot."*
> - **D4 — all four observations.** DST (**Step 5a**) · the `/settings` capture set incl.
>   **`maxexits`** · C10's `dstop` read (**Step 6b**) · Phase 0 + A7 in the **Step 4** gate.
> - **D5 — the sweep deletes `CLAUDE-C5-SHARED-SCRATCH`** after both scratch bots, in that order,
>   with a verify-back to exactly one shared automation and a do-not-force branch.
> - **D6 — the remainder, all nine.**
>
> ⏸ **One new DRAFT, ruled 2026-08-05 and NOT in force:** a **cadence-scaled graduation bar
> (Tier M)** for the mirror class, drafted as §7a of `docs/mirror-funding-memo-2026-08-05.md`.
> ⛔ **`docs/evidence-standards.md` is UNTOUCHED — verified `7d6c4f139a076975`, mtime Aug 3 — and
> the n≥100 bar remains in force as written. Andy signs Tier M separately.**

`docs/day0-audit-2026-08-05.md` (1,174 lines). Four parallel lenses against
`docs/reactivation-runbook.md`: new facts · deferred observations · sequencing · failure branches.
**44 raw findings, 3 refuted or narrowed, 36 carried — CRITICAL 7 · HIGH 13 · MEDIUM 12 · LOW 4.**

**The three that matter most, all CRITICAL, all still GATED:**
1. ⛔ **`itmlive` = `market` — the ruled hard Day-0 gate — is absent from the Day-0 runbook.**
   Zero matches for `itmlive` in 223 lines. Amendment drafted as Step 0a (audit F-1).
2. ⛔ **41 of 44 checks (93%) have no usable failure branch**, the word `STOP` appears **zero**
   times, and there is **no fleet-level abort anywhere** — every disposition is per-bot (F-3…F-10).
3. ⛔ **Step 3 arms nine bots 24 lines before Step 6/7 authorizes them.** `AUTOMATIONS` ON *is* the
   entry authorization. The fix is one swap: **Step 3 arms `EXIT OPTIONS` only; `AUTOMATIONS` goes
   ON in Step 7, per bot, only for bots that passed** (F-2).

**Applied directly** (evidence = dated first-hand observation of a value read; no decision changed;
`CLAUDE.md` §5): runbook — pilot ritual is DONE (F-21) · C0a stale gate superseded, build still
gated on C0c/C2/C7/C8/C9 + C10 (F-11) · three clone traps incl. the silent 100× Allocation reset
(F-19) · `archiveBot` hazard, no coordinate fallback (F-20) · Library residue is not just two bots
(F-22) · Bot Schedule is two windows (F-14). Plus `oa-platform-reference.md` §13.1 (F-30) and this
file's "Not built yet" list (F-31).

~~**GATED, needs Andy**~~ ✅ **ALL RELEASED AND APPLIED 2026-08-05** — see the banner above.
**F-1** `itmlive` Step 0a · **F-12** Template V2 · **F-32** the ceiling-28 count · **F-2** the
Step 3/7 swap · **F-3…F-10** the failure-branch set · **F-7** DST · **F-13** the `/settings` capture
set incl. `maxexits` · **F-15** the Library-object delete · **F-16** C10's `dstop` read · **F-18**
Phase 0 + A7 in the Step 4 gate · **F-17, F-24…F-28, F-33…F-35** the remainder.
✅ **F-36 is RULED — OBSERVE FIRST.** It was the one genuinely unruled slot; Step 3 as written would
have resolved it by acting and made the toggle and billing candidates permanently
indistinguishable. It is now **Step 2c**, before any toggle moves.

**Nothing touching `build-plan.md` was written.**

## ⭐ MIRROR FUNDING MEMO — 2026-08-05. Verdict: no mirror funding decision is due at Day-0.

`docs/mirror-funding-memo-2026-08-05.md` (289 lines). Sprint Rank 8 / Task 9, pulled forward two days
because the Day-0 audit made it a Step-2 dependency.

⛔ **Zero of ten mirrors clears `CLAUDE.md` §4's bar** (n≥100 / 6 months / a regime change). Best n is
**46** (`3DTE`); best span **83 days** (`Nigiri`). The 7 live mirrors hold **n=128 between them**.
**No FUND verdict exists for any mirror, and none can until late Oct 2026 at the earliest.**
**Day-0 mirror action: re-arm the seven, watch-only, size nothing.**

⚠️ **The asymmetry that keeps it actionable:** the bar gates *funding*, not *withholding*. DO-NOT-FUND
and KILL are available on weaker evidence. **For an already-running bot, "insufficient evidence" read
as "do nothing" means CONTINUE — a capital decision by default.** Memo recommends an explicit runbook
line.

⛔ **`QQQ long call`'s record is structurally incomplete — do not read its +0.3401.** Best-looking
mirror in the fleet (6/6 wins, zero drawdown) **and** the bot holding ~$13K risk / ~−$10.8K unrealized
across 4 open positions. **The export contains only closed positions — all 174 rows have a close date,
zero open** — so the open book was never in the source. Estimated effect: sum R +2.040 → ≈ **−1.3 over
10 positions; the sign flips.** **Its funding verdict is blocked until Andy's ride-or-close is
executed** (audit F-34: Step 2 requires the call *logged*, never *executed*, and Step 3 then arms this
bot).

📝 **The positive-median/negative-mean four, narrowed:** the two that are **structural** are both
already OFF (`Opening Range Breakout 60m`, `Weekly-IB-SPY-Paper-v1` — mean-R-ex-worst stays negative).
The two **in scope** (`60min-ORB-10W-Paper-v1`, `Trendy-Paper-v1`) flip positive on removal of one
max-loss position — **single-event, UNDETERMINED, undeterminable at n=12/n=15.**

⏳ **NEEDS A RULING (not before Day-0 — before late Oct):** at their own observed trade rates,
**four of the seven live mirrors need >1 year to reach n≥100; three need >2.5 years** (`Friday 14 DTE`
27.5 mo · `QQQ long call` 30.4 · `Tasty Condor` 30.7). **Under the rule as written they are
permanently un-fundable** — the n≥100 bar was set against 0DTE cadence. Three options in §7: accept
it · a time-based equivalent for low-frequency strategies (**an explicit weakening of the evidence
law**) · never fund from the mirror pillar.

**DRAFT kills, all on OFF bots, permitted by the asymmetry:** `1-45pm-Sandwich-Paper-v1` KILL
(median R **−1.0000**, 22.2% win, maxDD 5.4667R) · `Opening Range Breakout 60m` KILL (already
dispositioned to archive) · `Weekly-IB-SPY-Paper-v1` DO NOT FUND.

✅ **Anchor cross-check PASS — 10 of 10 mirrors reproduced exactly** from the source export
(`dca69adaf771f064…`, matching the hash the anchor cites). **`mirror_baseline.csv` unchanged
(`cdceb0a8d444e570…`); `--force` not used; nothing written to `data/`.**

## Open items

### ⭐ PILOT CLONE — RITUAL COMPLETE 2026-08-04. Archive confirmed; nothing outstanding.

**Steps 5c, 6, 7, 8, 9 and FINISH are ALL DONE — the ritual is complete end to end.** Full record:
`docs/session-log.md` 2026-08-04 part 4. Capture-diff:
`data/captures/2026-08-03-pilot/FINISH-capture-diff-2026-08-04.md` — **verdict: no unintended
edits**; every difference outside the exit block is a known clone trap already ruled on, a
deliberate prior-session act, or this session's authorized work.

- **The clone now holds the production name `QQQ-IC-0DTE-Fortress`** (`BOTfw5TkkCRF2717857919585029021`).
  The original is renamed `QQQ-IC-0DTE-Fortress-ARCHIVED-2026-08-03` (`BOTfw5TkkCRF817734373392552121`).
  `data/archive/rename_map.csv` row written.
- **✅ ARCHIVE DONE 2026-08-04 — by Andy, manually** (Claude could not fire `archiveBot`; see
  below). **Verified read-only from `/bots` immediately after:** footer **`35 active bots`** (was
  36) · **exactly one** bot named `QQQ-IC-0DTE-Fortress`, resolving to
  **`BOTfw5TkkCRF2717857919585029021`** (the clone) · the `-ARCHIVED-2026-08-03` name no longer
  listed · Trap-8 collision guard clean (`60min-ORB-10W-Paper-v1` and `Opening Range Breakout 60m`
  both present, neither touched) · `-NoPT50`, `IC-SPX-FastPT25-S2` and `-130PM` all present.
- **[RESOLVED 2026-08-04 — kept for the method record, because the failure is the finding]**
  **`archiveBot` would not fire from Claude.** `Archive` on the bot
  `...` menu would not fire across three attempts and three distinct mechanisms (dispatched event
  sequence on the item; the same on the hit-tested target; `computer.left_click` by element ref).
  No error, no dialog, `/bots` unchanged at `36 active bots`. Stopped at three per the standing
  rule. **A coordinate fallback was deliberately refused** — `Delete` sits ~29px below `Archive`
  and would have destroyed 41 positions of history. The rename is verified, so the production
  name is already free; the archive is hygiene, not a blocker.
- **⚠️ NEW OPEN CHECK, NOT RUN — is a template a frozen snapshot?** The template page’s
  automation rows carry `rid=RTfw5TkkCRF2717857919585272551` — **the same object id as the bot’s
  live ScannerA.** Whether editing the bot’s automation later changes what the template describes
  is **untested**. Recorded against `oa-ops-runbook.md` §2.3 and as the successor row in its §7
  open-checks table. **Do not assume a template freezes anything.**
- **Template `QQQ-IC-0DTE-Fortress` V1** = `Tfw5TkkCRF2617858650531245641`, Notes carry PR-03
  **byte-exact (1574/1574 chars, verified after hard reload)**.
- **⛔ `PR-03` IS NOT EXPRESSIBLE AS AN OA TAG.** The widget normalises to **`pr 03`** (lowercase,
  non-alphanumerics → spaces). `pre-registration-ledger.md` §2 and `oa-ops-runbook.md` §2.1 both
  assume the bare ID. **The tag was NOT written** — a silent substitution at a platform limit is
  what the card forbids at the time it was found. Notes carry the literal `ID               PR-03`,
  so the template IS greppable, via Notes not Tags.
  **→ THEN RULED (Andy, 2026-08-04): ADOPT `pr 03`.** Written and verified — template tags read
  `experiment,pr 03` after a hard reload, and Notes re-verified **byte-exact 1574/1574** after the
  tag write. Convention **`PR-NN` → `pr nn` in tags, literal `PR-NN` in Notes** appended to
  `oa-ops-runbook.md` §2.1. The tag is a search handle; Notes are the record.
- **Step 5c PASS, nothing changed.** Only Market-priced exits are the two Expiration (15:50) exits
  and the 15:52 backstop. PT50 is SmartPricing `normal` on both sides. Entries remain `Market` —
  an entry, outside §7's letter, untouched.
- **Step 6 PDF NOT produced** — `⌘P` is outside the browser tool's reach. Substituted a DOM read of
  the same modal, every field expanded, and said so in the file. Recorded as a substitution.

### [SUPERSEDED 2026-08-04 — kept for the record] Pilot clone — parts 1 and 2 done, ritual still incomplete
- **BOTH Decision Points are ANSWERED** (2026-08-03 part 2).
  - **A — an Exit Option Preset control EXISTS.** A `Presets` picker plus a
    `Save as presets for short option positions` checkbox. Account holds **zero** presets
    (`"No presets found for short option positions"`). Nothing saved.
    **RETRACTED (part 3):** part 2 flagged "no name field observed → build-plan's *NAMED* preset
    may not be expressible." OA's docs say *"You can name your presets for easy identification."*
    The checkbox was never ticked, so the naming step was never reached — absence was inferred
    from an unopened screen. **`build-plan.md` §2B/§8.1 is fine as written.** What stays open is
    narrower: whether ONE preset serves both the put-side and call-side Open Position actions
    (§9 check #4).
  - **B — 15:52 IS REACHABLE.** `Repeating` → `Market Time (EST)` → **`Custom`** opens a native
    `<input type="time" min="09:31" max="15:55">` at 1-minute step; `15:52` validates and commits
    as `ntime=1552`. The visible 5-minute grid is a convenience list, not the constraint.
- **Step 5a VERIFIED / 5b BUILT. Steps 5c, 6–9 and FINISH NOT STARTED.**
- **Three loose ends on the clone, all still open:** ScannerA still named
  `Fortress-ScannerA-PutSpread-CLONE` (revert pending), Bot Group is `None` (was `Monitor`),
  Tags are empty (were `experiment`).
- **The §8.2 attribution guard is NOT satisfied.** The backstop was set to `Market` per §7's
  flat-close carve-out; the existing **Expiration (15:50) exit is ALSO `Market`**, so pricing no
  longer distinguishes the two mechanics. Only the memo `1552 backstop flat close` and the
  2-minute timestamp gap do. **Andy's call** — not changed unilaterally.
- **DST / "EST" ambiguity, UNRESOLVED.** The trigger serialized
  `startDate 2026-08-03T20:52:00.000Z` = 15:52 at UTC-5, but August is EDT (UTC-4), where that is
  **16:52 ET — after the close**. `ntime=1552` is the operative field and the `startDate` time may
  be a stamp only. **Requires a Day-0 observation**; do not assume.

### TIER 1 AUDIT DONE 2026-08-04 — diagnosis: **partial-page reading, not fabrication**
All 9 cited OA doc pages re-read in full. **The file's quotations are substantially accurate.** The
defect class is **quoting a page correctly then missing the adjacent sentence that reverses the
conclusion** — §4.1, §6.1, §6.2 and §6.4 are all the same shape. **Single defect class, single fix:
completion, not replacement.** This also explains why the 2026-07-31 from-scratch rewrite did not
help — rewriting prose does not re-read sources. **Do not rewrite this file again.**
- **§4.1 upgraded CONTESTED → CONFIRMED FALSE.** `tools/bots/automations.md` — the page §4.1 quotes
  — says *"In your settings, you can customize when automations run, from as early as 9:31 am EST
  until 5 minutes before the market close."* 9:40/3:50 are DEFAULTS. **§8.2's premise collapses.**
  It also gives the platform cap **15:55**, matching the observed `max="15:55"`; **15:52 is inside
  it**, so the backstop is legal, not lucky.
- **⚠️ Biggest missing fact: timing is not guaranteed.** *"All user automations are pushed into a
  distributed work queue and executed in parallel… no guarantee an automation will run exactly on
  the 15-minute marks."* The 15:52 backstop has an **8-minute buffer, not a slot**, and this
  compounds with the DST question. Any exact-timestamp rule (incl. §8.3's sibling-close test) reads
  a jittered clock.
- **Three windows, do not conflate:** scan cadence ends **15:45** · automations customizable to
  **15:55** · Exit Options run to **~15:59**.
- **Recovered and written in:** failsafe **re-trips same day** after re-enabling and the count
  resets next trading day, with errors surfaced on the homepage/dashboard (the surface §9 #8
  needed); the **allocation** limit also trips scanners **and displays a warning**; logs filter by
  date too; the docs name position+allocation limits as the designed anti-loop defence,
  **corroborating §5.4's interlock**.
- **Tags needing change, flagged in place:** §3's percentage-allocation-shrinking claim is
  **[UNVERIFIED]** with no source — **sizing must not rest on it**; §5.3's "entire memory of the
  platform" is **[PROJECT-RULE], not [DOCUMENTED]** (§0.1 and §11 rest on it); §5.3's second quote
  and §4.5's quote **could not be reproduced verbatim** — re-verify or drop the quote marks.
  **→ OVERTURNED IN PART by Phase 6 (2026-08-04):** the allocation-shrinking claim IS documented
  (`automation-behavior`, OA-0083) — sizing may rest on it; §5.3's second quote resolves to
  *"Tags can be used in conjunction with decisions to create powerful and flexible automations"*
  (OA-0819) — drop the old quote marks. The [PROJECT-RULE] retag of "entire memory" stands.
  **→ ✅ WRITTEN INTO THE REFERENCE 2026-08-05 (R-05, authorized).** `oa-platform-reference.md` §3
  now carries the OA-0083 quote beneath the [UNVERIFIED] flag, and the flag is lifted — **sizing may
  rest on the allocation-shrink behavior as documented platform behavior.** The §5.3 quote-marks fix
  is NOT yet applied; it was not in the R-package and remains open.
- **Confirmed correct:** §4.2 execution order · §5.2 input chain and both its [DOCS-SILENT] tags ·
  §4.4 retention genuinely open · §3 limits · §5.1 indicators · §5.3's nine tag actions · §4.7 ·
  §0.1. **The file got more right than wrong.**
- **NEW LEAD, not a finding:** a 🔗 link icon sits on the **Exit Options row** of the Open Position
  panel, and any automation input can be upgraded to a bot input via that button — **suggests §9 #3
  is YES**, which would unblock the greenfield "PT% as a Bot Input" spec. Inference from a
  screenshot; **one click settles it.**

### PHASE 6 RECONCILIATION DONE 2026-08-04 — all six judgment docs vs the 1,548-fact corpus
The OA docs ground-truth program is complete: 100/100 pages read (Waves 1–4), and Phase 6 marked
every platform claim in the six judgment docs CONFIRMED / CONTRADICTED / UNSOURCED against
`data/oa_facts.csv`. Two new files, both hash-verified on device: **`docs/oa-reconciliation-report.md`**
(findings R-01–R-20, CONTRADICTED-first) and **`docs/oa-platform-reference-v3-DRAFT.md`** (the v2
file byte-preserved + 30 fact-cited annotation blocks + new §13; `oa-platform-reference.md` itself
untouched). Headlines:
- **The per-bot `EXIT OPTIONS` toggle IS documented** (OA-0871/OA-0896) — §10 and ops-runbook
  §1.6's "absent from docs / single-source" claims are false. The causal lapse claim stays
  one-rep-only; Day-0 Trades-list gate unchanged.
- **Two [PROJECT-RULE] tags were wrong the other way:** SmartPricing modes/counts/timings
  (OA-0785–0787) and Exit-Options mid-price evaluation (OA-0872) are fully documented.
- **⛔ NEW RISK CLASS (draft §13):** the default Options Expiration Protocol sends **no closing
  order** for expiring ITM positions (OA-0157/OA-0231) and bots are assignment-blind
  (OA-0245/0246) — a QQQ position that outlives its exits rides into physical settlement. The
  Exit-Options **PDT checkbox** delays closes ≥1 day (OA-0890). Both added to §8.3-class
  verification; Day-0 must read the expiration-protocol Setting.
- **Limits above 10 are UNSOURCED** (OA-0763/OA-0764) — gates any daily-limit-20 re-entry spec.
- **Exit Options window start is a docs-internal [CONFLICT]** (9:31 OA-0870 vs 9:40 OA-0085).
- Touch semantics are blog-sourced (outside the corpus); `Profit Taking $ / Stop Loss $` and
  `Avoid Events` are corpus-absent — verify in UI before fixed-$ rungs are pre-registered.
- **No CONTRADICTED finding touches `build-plan.md`'s frozen decisions.**
New §9-class checks queued: #9 limits>10 · #10 $-exits/Avoid-Events exist? · #11 read the
expiration-protocol Setting. The R-01…R-07 doc edits remain gated on Andy's authorization.

### TIER 2 DONE 2026-08-04 — eight checks run in the live UI, seven answered. **Only §9 #5 is open.**
Chrome-direct against the inactive account, confined to the clone plus read-only visits to the two
Fortress bots. Full detail in `session-log.md`; every result written into
`oa-platform-reference.md` under its §0.2 policy (§9 rows 3/4/7/8 struck, new rows 9/10/11 added
and struck, new **§6.1a** field roster, new **§13** account settings).

- **#3 Exit Options → Bot Input: YES, but the input's type is the WHOLE bundle.** No per-field 🔗
  (`i.fa-link` count is 0 inside the editor). ⛔ **The greenfield "PT% as a Bot Input" spec is NOT
  expressible.** "Exit-Options-SET as a Bot Input" is — a different design. **Andy's decision
  before anything is written into the spec.**
- **#11 Options Expiration Protocol: `itmpaper` = `itmlive` = `auto`** = *"Calculate estimated P/L
  from underlying close price"* — **the option that sends NO closing order.** `market` is the only
  one that closes ITM expiring positions. **Day-0 must decide this before capital is live.**
- **#9 Position limits CANNOT exceed 10** — pickers, not number fields. ⛔ §3's [PROJECT-RULE]
  "ten IC re-entries = a daily limit of 20" is right arithmetic and **unconfigurable**; the real
  ceiling is **5 ICs/day per bot**. Allocation `seed` is `min="250" max="100000"`.
- **#4 One preset serves BOTH Open Position actions, across two AUTOMATIONS.** Presets are
  **account-scoped** (`UI…` id namespace). Cross-automation [DOCS-SILENT] closed.
- **#10 `Profit Taking $`, `Stop Loss $`, `Avoid Events` all EXIST** — R-13 was a docs gap, not a
  product gap. `hedge-research.md` §9's fixed-$ rungs are buildable.
- **#7 Log retention is TWO numbers:** date **filter** reaches 3 weeks of weekdays (oldest
  `Mon Jul 13`; yesterday `Mon Aug 3` is not offered), stored **data** reaches `Mar 16, 2026`
  (≥141 days). The filter is the constraint, not retention.
- **#8 ⛔ THE EXCESSIVE ERRORS FAILSAFE HYPOTHESIS IS DEAD.** Newest error on either Fortress bot
  is `Apr 16, 2026 3:55PM`. Error days: Fortress Apr 16 (91) + Mar 16 (138+); `-NoPT50` Apr 16
  (91). **Zero June errors on either bot.** Carry it as a closed hypothesis, not a live one.
- **§4.1 / market open-close: RESOLVED IN THE PRODUCT.** The Settings surface is **Bot Schedule**
  and it holds **two independent windows** — Automations `09:31`→`5 min before close` (15:55) and
  Exit Options `09:31`→`1 min before close` (15:59). ⚠️ **This project had been treating one
  window where the product has two.** Footnote read verbatim: *"Repeating and date/time scheduled
  automations are not affected by this schedule"* — the 15:52 backstop is Repeating, so the Bot
  Schedule does not bind it.

**Bonus, unqueued:** `maxexits` ("Maximum Exit Options Close Attempts", account-wide, read `0` =
Unlimited) **appears in no other document in this folder** — a single switch that can cap every
bot's ability to close · the Expiration dropdown is 1-minute granular near expiry and
**`0.008` "8 minutes before" EXISTS**, so a 15:52 Exit Option was expressible all along (§8.2's
stated objection is falsified by the control itself; §8 is gated so this is recorded against it,
not edited into it) · `paper` notifications are **unchecked** while the whole fleet is paper, so
position-open/close emails are not reaching Andy.

**⚠️ STILL OPEN: §9 #5** (is re-applying Update Position Exit Options side-effect-free) — needs
positions, so it is a Day-0 check. The **DST / "Market Time (EST)"** question also still needs a
Day-0 observation; nothing this session touched it.

### ✅ OA RESIDUE FROM THE C0a PROBE — **FULLY SWEPT 2026-08-06.** Block below LEFT STANDING.

**Slot-7 deletions executed 2026-08-06, in the build-plan §2 order (capture first), on Andy's
ruling. All three targets gone; nothing else touched.**

| # | Object | Before | After |
|---|---|---|---|
| 1 | Pre-deletion `/bots` capture — **taken first** | expected **35 active bots** | **35** ✅ footer *"35 active bots • 15 left in your plan"*, 35 distinct `BOT…` ids. Filed `data/captures/2026-08-06/oa_Bots_2026-08-06-17-21-38.txt`, sha256 `ad6f2a40…f0f5`, **byte-exact against the page-computed hash** |
| 2 | Bot `TEST QQQ-IC-0DTE-HedgeC-S3 Clone` `BOTfw5TkkCRF2217852702121253931` | present, `status:off` | **DELETED** — roster 35 → **34** |
| 3 | Bot `QQQ-IC-0DTE-InvFilter-Wide150` `BOTfw5TkkCRF4517755136823526783` | present, `status:off` | **DELETED** — roster 34 → **33** |
| 4 | Library object `CLAUDE-C5-SHARED-SCRATCH` `RTfw5TkkCRF178589028977611` | read **`Unused`** after the two bot deletions (was `2 bots`) | **DELETED** via `removeAuto` → *"Remove from My Library?"* → Yes |
| 5 | ⭐ **Verify-back after a hard reload** | — | **`My Automations` = EXACTLY ONE ROW: `Defang-Mon-S2-StrikeTouch` (`RTfw5TkkCRF3317787955826108344`, 2 bots).** ✅ As required |

**Method:** every click dispatched on an element selected **by identity** — `data-click=deleteBot`,
`data-rid=RTfw5TkkCRF178589028977611` — never by coordinate. `oa-ops-runbook.md` §5's
`archiveBot` hazard (Delete sits ~29px below Archive) was therefore never in play. Each irreversible
confirmation was preceded by a re-read of `a5.bots.bot.id` to prove the right bot was still loaded.
**Not touched and re-confirmed present afterwards:** `DIR-SPX-PutVIX22-SL75` (zero-trade, must not be
deleted), `IC-SPX-FastPT25-S2` and `IC-SPX-FastPT25-S2-130PM`.

⚠️ **The bot-local residue named below died with the two bots** — bot inputs `CLAUDE-C0A-BOT-EXITS`
(`IN178588971538691`), `C5_BOTVAL_TESTCLONE` (`IN178589092511981`), `C5_BOTVAL_INVFILTER`
(`IN178589106268631`), `CLAUDE-G1-EMPTY-EXITS` (`IN178586615441261`), and both C5 instances.
**Nothing from the C0a probe or the 2026-08-06 probe remains on the account.**
⚠️ **The 2026-08-06 probe added NO residue:** its one scratch object, `CLAUDE-C8-SCRATCH`
(a `closepos` automation), was **discarded unsaved** and verified absent from both the bot's
automation list and the Library before the deletions began.
⚠️ **Fleet arithmetic moves: `n_used` drops by 2.** Day-0 active-bot count is now **33**, footer
*"33 active bots • 17 left in your plan"*. `track-b-arms-spec.md` §3.2/§3.4's headroom figures were
computed at 35 and should be re-read against 33 before the next allocation claim.

### ⚠️ OA RESIDUE FROM THE C0a PROBE — 2026-08-05. Andy ruled it STAYS; two lines the sweep needs.

Eight writes, all on scratch objects, all logged in `session-log.md` 2026-08-05 part 2. Both scratch
bots re-read post-state `status:"off"`, `AUTOMATIONS OFF`, `EXIT OPTIONS OFF`, `closedCount: 0`.

1. ✅ **SWEPT 2026-08-06 — deleted explicitly, exactly as this line required.** ~~⛔ **`CLAUDE-C5-SHARED-SCRATCH` (`RTfw5TkkCRF178589028977611`) IS A LIBRARY OBJECT AND DOES NOT DIE
   WITH THE TWO SCRATCH BOTS.** It is an account-level shared automation carrying automation input
   `C5_EXITS` (`IN178589048006251`). **The Phase 4 sweep must DELETE IT EXPLICITLY** after
   `TEST QQQ-IC-0DTE-HedgeC-S3 Clone` and `QQQ-IC-0DTE-InvFilter-Wide150` are deleted, or it orphans
   in `My Automations` — where the account previously held exactly one shared automation
   (`Defang-Mon-S2-StrikeTouch`), so an orphan is conspicuous and will be mistaken for a real object.~~
2. **Both scratch bots now carry C5 bindings, and those DIE with the bots' deletion — no sweep action
   needed for these.** TEST clone: bot inputs `CLAUDE-C0A-BOT-EXITS` (`IN178588971538691`) and
   `C5_BOTVAL_TESTCLONE` (`IN178589092511981`), plus instance `fw5TkkCRF3317858909367702271`.
   InvFilter-Wide150: bot input `C5_BOTVAL_INVFILTER` (`IN178589106268631`), plus instance
   `fw5TkkCRF3317858910757101732`. The 2026-08-04 `CLAUDE-G1-EMPTY-EXITS` residue is unchanged and is
   also in this class.

### ⚠️ WRITES MADE 2026-08-04 (pilot part 4) — all authorized, all logged

**On the production bot** (`QQQ-IC-0DTE-Fortress`, ex-clone): ScannerA renamed back to
`Fortress-ScannerA-PutSpread` · Tags restored to `experiment` · renamed to the production name ·
Template V1 saved and bound. **Bot Group deliberately left `None`** until the Phase 4 sweep.
**On the original**: renamed to `QQQ-IC-0DTE-Fortress-ARCHIVED-2026-08-03`. **Not yet archived.**
**On the account**: `itmpaper` = `market`.
**On `TEST QQQ-IC-0DTE-HedgeC-S3 Clone` ONLY** (authorized probe, delete-list bot): automation
input **`CLAUDE-G1-EMPTY-EXITS`** (`IN178586615441261`) created on `HedgeC-Scan-Put`'s Open
Position action with an **EMPTY** Exit-Options default. **NOT REVERTED.** That action now carries
no exit options. Zero behavioural risk — AUTOMATIONS OFF, account inactive, bot is delete-list.
The pre-link config survives in the param's `oldValue`. Revert on request.

### ⭐ ANSWERED 2026-08-04 — saving a template does NOT disturb the bot, and `BUILD_ID` is free
`oa-ops-runbook.md` §2.3's `[EXPECTED, not confirmed]` question is closed. Every bot field re-read
identical after the template save. What changed is an **addition**: a `Template` panel now shows
`QQQ-IC-0DTE-Fortress` + `BOT VERSION 1, Aug 4, 2026` on the bot's settings page.
**That is §2.2's `BUILD_ID` mirror, native and platform-maintained.** §2.2's whole failure mode was
that hand-mirroring would be forgotten. **Do not build the hand-mirrored `BUILD_ID`.**
Also closed: the preset NAME field exists — `input[name="pretext"]`, hidden until `defs` is ticked.
`build-plan.md` §2B/§8.1's NAMED preset is expressible. Observed, not inferred.

### ⚠️ WRITES MADE TO THE CLONE 2026-08-04 — Andy's call, not reverted
1. Account now holds Exit Option preset **`TIER2-CHECK4-PUTSIDE`**
   (`UIfw5TkkCRF1517858152565216101`). The account previously held **zero** presets.
2. **`Fortress-ScannerA-PutSpread-CLONE` was saved.** Its Open Position `exits` blob
   **re-serialized** — numeric payload byte-identical (`^^0.5|0.01^$0`: 50% PT, 10-min
   expiration, Market pricing all unchanged) but the `text` label changed `"Profits: 50%, …"` →
   `"Profit: 50%, …"` and the sig gained an `xevents` key. Cosmetic on inspection, persisted
   through a hard reload, **and still a diff on a pilot bot.**
3. `Fortress-ScannerB-CallSpread` was opened read-only and closed **without saving**.
4. `QQQ-IC-0DTE-Fortress` and `-NoPT50` were **read-only** throughout. The original Fortress
   remains untouched.

### `oa-platform-reference.md` — UNFROZEN 2026-08-03, and amended

**Editing policy (Andy, 2026-08-03), now written into that file's §0.2:** appends backed by direct
evidence need no authorization; **never append an inference from absence**; a falsified claim is
marked **in place** with a dated `⛔ CONTESTED` banner and its original text left standing, with the
**rewrite** still gated; **§8 stays gated** (build-plan-adjacent); and a tier tag must name what was
observed and when — citing a sibling project doc is not provenance.

**Amended 2026-08-03** (618 → 828 lines, nothing deleted): 4 × `⛔ CONTESTED` (§2 clone trap, §4.1
market open/close, §6.4 order-lifetime tag, §8.2 the 15:52 premise — marked, **not** rewritten),
3 × `✅ RESOLVED` (§6.2 Touch, §7 SmartPricing table, §7 final-price conflict), 5 × `📝` appends,
and §9 rows 1/2/6 struck as answered with row 4 narrowed.

### ⛔ A STAGED READ RETURNED TEXT THAT IS NOT IN THE FILE (2026-08-03)
A session-start `Read` of `oa-platform-reference.md` returned §2's clone-trap paragraph **as a
paraphrase** — same meaning, different sentences — while the staged copy and the device file carried
the **identical sha256**. Not stale content: **altered** content. `CLAUDE.md` §9.1a warns about
stage-backs serving stale bytes; this is the same defect in the read direction and strictly worse.
**Every verbatim quotation taken from a staged read is suspect.** Spot-checks of §6.1/§6.2/§6.4/§7
came back accurate, so it was localised — which is the dangerous shape, not the reassuring one.
**Standing mitigation:** derive quotation anchors from the device file itself and assert an exact
single match before relying on them.

### ✅ AUTHORIZED AND APPLIED 2026-08-05 — the R-edit package (was "Still needing authorization")
**Ruled per-item by Andy 2026-08-05 against `docs/r-edit-authorization-2026-08-05.md`; all sixteen
rows YES, applied the same day.** Every edit carries a dated banner, cites a `oa_facts.csv` fact ID
or a dated first-hand observation, and was verified by direct `device_bash` sha256 + single-match
grep. **No `git` run.**

- ~~**`oa-ops-runbook.md` §5 Trap 1** still asserts the false shared-automations claim.~~
  **CORRECTED** — row rewritten (cloning copies; sharing is Library opt-in), original preserved in
  the dated note beneath the trap table. R-02a/S1.
- ~~**`pilot-clone-card-qqq-fortress.md` Step 2** still contains the void fork step.~~
  **VOIDED IN PLACE** — banner added; the step is left standing because the card is the record of
  what was executed 2026-08-03. R-02b/S2.
- ~~**`build-plan.md` §2B**'s "restored exits" justification wording is still inaccurate.~~
  **CORRECTED on an explicit "amend the plan"** — wording only; the build is unchanged. S3.
- **Also applied:** R-01a/b/c (the `EXIT OPTIONS` toggle IS documented — OA-0871/0896) ·
  R-02c (`reactivation-runbook.md` §2 step 2 rewritten — the Day-0 script no longer instructs a
  no-op fork) · R-02d (ops-runbook §3 narrowed to Library-shared only) · R-03 (SmartPricing table
  → **[DOCUMENTED + FIRST-HAND]**, OA-0784–0787) · R-04 (mid-price → [DOCUMENTED], OA-0872) ·
  R-05 (allocation-shrink sourced, OA-0083 — **sizing may rest on it again**) · R-06 (Exit Options
  START time retagged **[CONFLICT]**, OA-0870 vs OA-0085; settled first-hand at 09:31 for this
  account) · R-07 (clone completeness is a **docs defect**, OA-0845, not silence).
- **NEW §14 in `oa-platform-reference.md`** — the Phase 6 documented-facts payload cherry-picked
  from the v3 draft: assignment blindness, the expiration protocol's documented half, partial
  fills, quote staleness, in-flight invisibility, UTC-anchored scheduled events, SPX nickel
  granularity, the empty core pages.
- ⛔ **`oa-platform-reference-v3-DRAFT.md` IS A STALE BRANCH — do not adopt it.** Ruled **ALT: NO**.
  It was generated off base sha `1330dc59…7386` at 02:57 on 2026-08-04; the live reference was
  rewritten at 03:55 the same day. The draft has **0** `ANSWERED 2026-08-04` §9 rows (live has 11),
  **no §6.1a**, and a **§13 that collides** with the live §13. Adopting it wholesale would have
  deleted the `itmlive`=`auto` finding and the PDT check. Its unique content now lives in §14;
  **the draft itself is superseded and should not be cited as "the reference with Phase 6
  applied."**
- **`CLAUDE.md` §5 + `oa-platform-reference.md` §0.2 — POLICY SPLIT APPLIED.** Decisions stay
  gated behind "amend the plan"; evidence-backed corrections of falsified claims may be applied
  directly under five conditions, with **Andy's veto moved to commit review**. §8 still gated.
  Inference from absence still forbidden.
- **Three new rows ruled the same day:** **S4** — `build-plan.md` §2D fleet count scoped to
  *"≈18–20 plan bots plus ≤8 pre-registered Track B arms, ceiling 28"* on an explicit "amend the
  plan"; this **discharges `track-b-arms-spec.md` §3.5's S-2 condition**, so ARM-B2's slot
  accounting is no longer conditional. **S5** — `pre-registration-ledger.md` PR-14…PR-17's
  family-level kill criterion replaced (the old *"more than one differing input"* was vacuously
  unfireable under D-1 Option A); still **DRAFT, unsigned**. **S6** — `research-loop-spec.md`
  annotated: the Track B `Expiration 0.005` (15:55) rung is **unreachable** under the 15:52
  backstop, so R-2's time question is served by **0.015 (15:45) alone**.

### Still needing authorization (NOT amended)
- ~~⚠️ **`_to_delete/index.lock.stranded-2026-08-03`** — Claude ran `git status` against the standing
  instruction not to, stranding `.git/index.lock`; the lock was moved out (the bridge cannot
  delete) and `.git/index.lock` confirmed gone. **Andy should delete `_to_delete/`** — untracked,
  not in `.gitignore`.~~
  ✅ **DONE — row retired 2026-08-05.** **[FIRST-HAND 2026-08-05, `find` across the repo tree at
  depth 3 from the device]**: **no `_to_delete` directory and no `*stranded*` file exists anywhere
  in `bot-fleet-v2`.** Andy deleted it. The tree root holds only `.DS_Store · .env · .env.example ·
  .git · .gitignore · .tmp.driveupload · CLAUDE.md · README.md · STATUS.md · dashboard.html ·
  data · docs · scripts`. ⚠️ **Standing lesson unchanged and still binding: do not run `git` from
  this side** — the bridge cannot unlink, so a stranded lock file needs Andy's hand to clear.
  *(This row was itself a propagation miss: the cleanup happened and the state page was never
  told. Same class as everything else this sweep fixed — found only by looking at the filesystem
  rather than at the document describing it.)*
- **Tournament doc conflict, still open.** `oa-ops-runbook.md` §3 (fork so arms are NOT shared) vs
  `build-plan.md` §2D + `hedge-research.md` §5.2 (shared automation **required**). R-02d clarified
  the mechanics but **did not decide the design** — that is a build decision, gated.
- ~~⚠️ **C12 — do archived bots count against the Pro 50-bot cap?** Unowned, blocking. If they do,
  the Day-0 arithmetic is 36 + 7 = 43 and the ≤8 Track B allocation does not fit (43 + 8 = 51).
  S4's ceiling of 28 assumes they do not. `track-b-arms-spec.md` §10.~~
  ✅ **DISCHARGED — this row is retired 2026-08-05; C12 no longer needs authorization.**
  **[FIRST-HAND 2026-08-04, `/bots` footer read]**: `35 active bots • 15 left in your plan`, read
  read-only immediately after Andy archived the original Fortress, against `36 active bots` during
  three failed attempts. **35 + 15 = 50** — the plan complement counts **ACTIVE** bots, so
  **archived bots do not consume slots**, and archiving *frees* a slot rather than relabelling one.
  S4's ceiling of 28 holds; wave 1 is **22 of 50**.
  ⚠️ **RESIDUAL, carried not dropped — [FIRST-HAND, UNCORROBORATED], no second witness.** It is
  the footer's *accounting*, not OA's *enforcement*: `left = 50 − active` is self-consistent under
  both hypotheses and cannot distinguish them, and it was observed with **one** archived bot where
  the Group-A sweep archives **twenty**. ⛔ **Pre-declared reopen: if a bot build ever fails at the
  cap despite archived bots existing, C12 reopens** and the ≤8 allocation is re-derived against an
  observed slot count. Full block: `track-b-arms-spec.md` §3.2. Propagated the same day to
  `build-plan.md` §2D and `greenfield-family-spec.md` §12 row 17.

### Findings previously queued — now written into the reference
- **TRAP 1 IS FALSE — cloned bots do NOT share automations by reference** (direct test,
  2026-08-03 part 1). Sharing is opt-in via the Automation Library only. Falsifies
  `oa-platform-reference.md` §2, `oa-ops-runbook.md` §5 Trap 1, and voids the card's Step 2.
- **§4.1 appears FALSIFIED BY THE PRODUCT — now on two independent lines of evidence.** §4.1
  concludes Market open / Market close are hard-coded 9:40am / 3:50pm and "neither is adjustable".
  (i) The live trigger menu reads **"Market open — At scheduled time in settings"** and
  **"Market close — At scheduled time in settings"**. (ii) OA's Exit Options docs say the
  9:31am→1-min-before-close window is **customizable via Settings**. Both point at the same
  Settings surface. Not yet verified in Settings directly.
- **§9 check #6 RESOLVED.** Final Price control is `min="50" max="150"` → the §7 `[CONFLICT]`
  resolves **in favour of the v1 file's 150%**; the docs' "0%…100%" is wrong. Floor is 50 (mid).
- **§7's SmartPricing table is now FIRST-HAND VERIFIED** (Normal/Fast/Patient/Off/Market, exact
  price counts and timings; `Fast` has internal value `speedy`) — promote it off
  `[PROJECT-RULE, not doc-verified]`.
- **NEW, undocumented: per-bot automation slot limits** — Scanner 2/5 · Monitor 0/5 · Date 0/10 ·
  Repeating 0/10 · Market open 0/5 · Market close 0/5 · Position opened 0/5 · Position closed 0/5 ·
  Webhook 0/10 · Button 0/10.
- **`oa-platform-reference.md` tag-provenance audit still needed.** Its `[FIRST-HAND]` tag on the
  clone trap cites the runbook, which asserts the same claim — a citation loop. §4.1 above is a
  second instance of the same disease.
- **§9 check #1 — ANSWERED 2026-08-03 part 3, from OA's own docs, not a UI check.**
  *"The new 'Touch' Exit Option references the underlying price relative to a position's strike
  price(s)."* Triggers when the underlying is `$X`/`X%` from ITM or less; `$0` = exit on first
  going ITM, negative allows penetration, positive exits before ITM. **§6.2's condition is met:**
  S1/S2 become Exit Options (1-min cadence, first in cycle) instead of monitors, the v1 §14
  "cannot live in Exit Options" claim is wrong, and **the tournament's S3-was-the-only-Exit-Option
  confound dissolves.** `build-plan.md` §2D/§8.1's "Touch $0 on the challenged side" is
  expressible exactly as written. ⚠️ **Still open: whether a Touch on one spread closes its
  SIBLING** — keep §5.4's mechanism, do not assume.
- **§6 has FOUR defects, queued 2026-08-03 part 3:** (a) §6.2 superseded — Touch is answered;
  (b) §6.4's `[PROJECT-RULE, not doc-verified]` tag is **wrong** — the 2-minute order lifetime is
  documented verbatim, including *"no additional orders will be sent to your broker"*, a clause
  absent from the folder; (c) §6.1's preset quote is **truncated**, dropping the naming sentence;
  (d) §6 omits that the operating window is **customizable via Settings** — and the Exit Options
  modal renders that phrase as a hyperlink that was read as plain text and not followed.
- **MISSING FROM THE FOLDER ENTIRELY:** *"Exit Options always run, even if your automations inside
  a bot are turned off."* So **a bot with `AUTOMATIONS` OFF is NOT inert if it holds positions** —
  and this is the documented reason the 15:52 backstop belongs on the automations side.
- **§8.2's justification is WRONG (the build is not).** It argues a 15:52 Exit Option "does not
  exist" because Exit Options stop 1 minute before close — but **15:52 is inside a window running
  to ~15:59**. An `Expiration: 8 minutes before` would plausibly reach it (⚠️ that dropdown's
  options were NOT read). The correct objection is architectural: we do not *want* the backstop in
  the Exit Options execution class. Same build, wrong stated reason.
- **The clone's exits already existed.** Both Open Position actions carry PT50 + a 15:50 time
  exit. `build-plan.md` §2B's "restored exits" is a no-op; only the 15:52 backstop was new work.
  The §2B justification wording is inaccurate — flagged, frozen, not edited.
- **Three undocumented clone traps**: Allocation resets to `1000`, Bot Group drops to `None`,
  Tags drop. None are in any doc.
- **Tournament doc conflict**: `oa-ops-runbook.md` §3 (fork so arms are NOT shared) vs
  `build-plan.md` §2D + `hedge-research.md` §5.2 (shared automation required). Unresolved.
- **Entry pricing open question**: `oa-platform-reference.md` §7 bans Market pricing "on every
  exit"; the Fortress enters at Market on both sides. Exit-scoped ban, so no literal conflict —
  but the cited failure mechanism is order-type-specific. A future pre-registered decision.

### Capture discipline
- **⛔ ELEMENT REFS ARE NOT SUFFICIENT ON THIS APP — found 2026-08-04.** `oa-ops-runbook.md` §4.0
  says "use element refs for every click, never raw coordinates." Correct about coordinates,
  **incomplete about refs**: `computer.left_click` by element ref reported success and **nothing
  happened** — on automation rows, on node cards, and on the archive item. No error. **A tool's
  success message is not evidence the app received the click.** What works is dispatching
  `pointerdown → mousedown → pointerup → mouseup → click` on the element with `clientX/clientY` at
  its bounding-rect centre. Every write of 2026-08-04 went through that path. Same wall the
  2026-08-03 part-2 session hit; read it as a standing property, not session degradation.
- **`computer.type` lands intermittently — found 2026-08-04.** It committed one rename, then
  silently failed twice with the correct input focused. `form_input` worked every time.
  **Prefer `form_input`, and re-read `.value` after every text entry.**
- **⛔ OA's HTML sanitizer DECODES THEN STRIPS — found 2026-08-04.** Pasting `&lt;capture&gt;` into
  template Notes round-tripped to nothing: it was decoded to `<capture>` and removed as markup.
  The panel looked fine. **Caught only by a byte-exact 1574-character compare.** Double-escape
  (`&amp;lt;`) to survive one decode pass, and always assert byte-exact on write-backs, not just
  on quotes read out.

- **A THIRD `innerText` trap, found 2026-08-04.** The bot log's `Date` / `Time` / `Type` filter
  chips render their labels via CSS, so `innerText` on them is the **empty string**; they are
  `div.input-ct.filterbtn-ct` wrappers around hidden inputs `date` / `time` / `autotypes`. A
  reader trusting `innerText` concludes the filters do not exist.
- **Log rows carry a `title` attribute holding a year-bearing timestamp** (`Apr 16, 2026 3:55PM`).
  **Use it.** The visible date *group header* is unreliable — on `-NoPT50` it did not render at
  all, on `Fortress` it changed value mid-scroll. The #8 result rests on `title`, not headers.
- **`Load more` on the raw log stalls** — it stopped yielding at ~229 rows while still displaying
  the button. Do not assume deep history is pageable.
- **`innerText` has now produced two wrong findings in two sessions.** Part 1: a capture asserted
  "Position Criteria ALL EMPTY". Part 2: `Custom` read as a heading, briefly making 15:52 look
  unreachable. **Extend the standing rule** — read `input.value`, `input.checked`, **and
  `data-value` on `<item>` nodes**, never `innerText` alone.
- **`selected` CSS classes do not imply a committed value.** The weekday multi-select showed five
  checkmarks while the hidden `byweekday` still held `Monday`; only closing the menu committed it.
- **Viewport/screenshot mismatch reproduced**: `read_page` reports 2560×1314, screenshots return
  1528×784 (~1.675×). This is the mechanism behind part 1's coordinate-click failures. **Element
  refs are unaffected** — use refs, never coordinates.

### Operating mode
- **CHROME-DIRECT OA EDITS — STANDING AUTHORITY, decided 2026-08-04.** Part 1's trial verdict was
  qualified pass (Claude reads and detects, Andy clicks); Part 2 released Claude to drive and save,
  in-session. **Doc amendment now made, at Andy's explicit instruction**: `CLAUDE.md` §5,
  `build-plan.md` §5, `daily-loop-spec.md` §8, and `oa-ops-runbook.md` (header, §4, §6) all updated
  from "Andy makes every OA edit" to Claude-executes-directly. Every edit now requires a **two-layer
  proof** — an immediate screenshot/capture re-observation of the changed value (new, formalizes
  what Part 1/2 did ad hoc), plus the pre-existing Trades-list behavioral check. Andy retains revoke
  authority, globally or per-bot, at any time. Known traps from the trial (viewport/coordinate
  mismatch, `innerText` on CSS-rendered chips, `selected` classes not implying commit) are now
  written into `oa-ops-runbook.md` §4.0 so they aren't re-discovered per session.

### Standing / unchanged
- **Fortress strike check — optional research, non-gating.** Both Fortress bots still carry
  `strike_fix=Y` in `bots_meta.csv`. `build-plan.md` §3 rules this adjudication **dead as a
  blocker**; it affects only how the frozen v1 record is read.
- 48 cached symbol-days of 5-min SPX/QQQ tape (5/29→7/02) were never committed; unrecoverable.
  Noted, closed as a loss.
- RoE `$` blanks stand by decision (an active audit-gate H3 failure — `evidence-standards.md`
  §10 item 4). Notion's role in v2 is undecided.
- ✅ **RESOLVED 2026-08-04 — `bot-fleet-v2` now has a remote.** Private repo
  **`chace2827/bot-fleet-v2`**, `origin` → `https://github.com/chace2827/bot-fleet-v2.git`,
  branch `master` tracking `origin/master`. First push 2026-08-04 at commit `c290429`:
  227 objects, 920 KiB. **`data/oa_facts.csv` and `data/oa_docs_coverage.csv` went up with it** —
  they had been untracked since extraction, so the 100-page corpus had no off-machine copy at all.
  `.env` verified absent from the index before pushing (`.gitignore` covers `.env`, `.env.*`,
  `*.env`, `*.pem`, `*.key`, `*_token*`, `*_secret*`).
  *(Was: no remote at all, discovered 2026-08-03 — `CLAUDE.md` §8's `chace2827/bot-fleet` is the
  ARCHIVE's remote, not v2's. Do not confuse them.)*
  Confirm `.gitignore` covers `.env` before the first push.
- **HOLD in force on the builder chat.**
