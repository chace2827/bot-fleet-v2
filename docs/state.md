# State — Bot Fleet v2

*The live facts. Updated whenever a stated fact changes (CLAUDE.md §9.1). Numbers live in
`STATUS.md`; the plan in `docs/build-plan.md`; progress in the `bot-fleet-migration` tracker.
Last updated 2026-08-04 (Tier 2 product verification).*

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
> ⚠️ **NOT YET PROPAGATED — the rulings are recorded, the docs are not yet amended.** D-1, D-4,
> Decision 4 and Decision 5 all imply edits to `build-plan.md`, `oa-platform-reference.md`,
> `hedge-research.md`, `oa-ops-runbook.md`, `pre-registration-ledger.md` and
> `reactivation-runbook.md` that have **not** been made. The memo carries the ready-to-paste text;
> the two touching frozen or gated surfaces still require an explicit *"amend the plan"*.
>
> **Three load-bearing findings remain open** (memo Appendix B has all seven): the broken
> `build-plan.md` §5.2/§8.1 citation, flagged on the D-1 row above and still present in three
> files · **"Range075 as a preset" looks unbuildable** — presets are an Exit Options object while
> `hedge-research.md` §8 specifies Range075 as an entry decision, hitting frozen §2D and §5.2
> rule 3 · **the arm-distinctness assert `oa-ops-runbook.md` §3 promises does not exist** —
> `execution_audit.py` has 13 rules and none is config-based, so §3 cannot be cited as a proof leg
> until it is built. ⚠️ **G2's REFERENCE result raises the stakes on the second and third:** an
> arm-matching proof that reads the action alone now returns identical for every arm.

---

## ⭐ GREENFIELD FAMILY SPEC — WRITTEN 2026-08-04. Design closed; SIX blocking checks before build.

`docs/greenfield-family-spec.md` (1,548 lines, sha256 `aee1d763…4d251fdb`, on-device verified).
**The design document Phase 4's fresh builds are built from.** It **implements** `build-plan.md`
§2D and §5 — no frozen doc was edited, no OA surface touched, no git command run.

**Seven bots as ONE matched family, not two builds.** The "greenfield IC family" and the "rebuilt
hedge tournament arms" are two views of the same family, which is what fits 4 IC arms + 2 hedge
arms + 1 canary inside §2D's 5–7 fresh ceiling with no remainder. Underlying **QQQ**. Arms:
`GF-QQQ-IC-Ride` (control, PR-14) · `-PT50` (PR-15) · `-Trail` (PR-16) · `-Touch0` (PR-17) ·
`-SL100` (PR-18) · `-SL200` (PR-19) · `-Canary` (PR-20). Four shared Library automations attached
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

**⚠️ Three of the seven are not arms yet** under `hedge-research.md` §5.2's own definition —
Trail's `tstop` shape, SL100/SL200's `stoploss` unit, and four arms' exit-pricing sub-field are
unconfirmed primitives. §5.2: *"An arm failing any of these is not a weak arm, it is not an arm."*

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
3. **`research-loop-spec.md` §10's signed 0.10R margin is unreachable here.** Max per-condor
   return = total credit ⇒ **R_max ≈ +0.083 to +0.162**. Either the margin is re-declared for this
   family or nothing here can ever graduate.
4. **The family consumes 7 of the 8 signed Track B slots** (it meets §4's own definition of a
   Track B arm), and `GF-SL200` duplicates a variant in the signed Track A §3 set. **This
   constrains the Track B task directly.**
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
- `data/bots_config_v2.csv` (Phase 2 — written from capture, never by hand) and
  `data/mirror_baseline.csv` (one-time frozen mirror snapshot, built from
  `data/captures/oa_export_positions_2026-07-30.csv`, **not** from the archived ledger).
- The liveness check is half-done: the `SILENT_BOT` rule ships, but the bot-log side needs a
  log source the detector does not have.

## Day-0 first action
**Set `LEDGER_START` in `build_ledger.py` before anything else.** Then
`reactivation-runbook.md` top to bottom.

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

### Still needing authorization (NOT amended)
- **`oa-ops-runbook.md` §5 Trap 1** still asserts the false shared-automations claim.
- **`pilot-clone-card-qqq-fortress.md` Step 2** still contains the void fork step.
- **`build-plan.md` §2B**'s "restored exits" justification wording is still inaccurate.
- ⚠️ **`_to_delete/index.lock.stranded-2026-08-03`** — Claude ran `git status` against the standing
  instruction not to, stranding `.git/index.lock`; the lock was moved out (the bridge cannot
  delete) and `.git/index.lock` confirmed gone. **Andy should delete `_to_delete/`** — untracked,
  not in `.gitignore`.

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
