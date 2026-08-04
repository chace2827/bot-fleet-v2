# State — Bot Fleet v2

*The live facts. Updated whenever a stated fact changes (CLAUDE.md §9.1). Numbers live in
`STATUS.md`; the plan in `docs/build-plan.md`; progress in the `bot-fleet-migration` tracker.
Last updated 2026-08-04 (Tier 2 product verification).*

## ⚠️ FOUR DECISIONS PENDING REVIEW — opened 2026-08-04 by Tier-2 verification

*Read this block first. Each one is a product fact that invalidates something this project had
already decided or assumed. None can be closed by more research; each needs Andy's call.*

| # | Decision | What forces it | Where it bites |
|---|---|---|---|
| **D-1** | **What replaces "PT% as a Bot Input"?** | The 🔗 on the Exit Options row makes the **whole exit bundle** an input; there is no 🔗 on Profit Taking % or any single field. | `build-plan.md` §5.2 / §8.1. The only expressible form swaps entire exit configurations instead of tuning a number — a materially different mechanic. Plan is **frozen**, so this needs an explicit *"amend the plan"* either way, **including a decision to drop the bot-input idea**. |
| ~~**D-2**~~ ✅ **DECIDED 2026-08-04: cap at 5 ICs/day, ONE bot.** Accept the platform ceiling; do not split a strategy across two bots to reach 10. Rationale: one bot = one config row = one pre-registration entry = one ledger identity, so the unit stays "condor" with no cross-bot aggregation and the drift detector keeps a single subject. Revisit only if a spec genuinely needs >5 entries in a session. | **Re-scope every re-entry spec to 5 ICs/day.** | `posLimitDay` / `posLimit` are **1–10 pickers**, no free-text path. An IC is two positions. | §3's [PROJECT-RULE] "ten IC re-entries = a daily limit of 20" is correct arithmetic and **unconfigurable**. Real ceiling is **5 ICs/day per bot**. Anything above that must be redesigned or split across bots. |
| **D-3** | **Set the In-the-money Position Action before capital is live.** | `itmpaper` = `itmlive` = **`auto`** — *"Calculate estimated P/L from underlying close price"*, which sends **no closing order**. `market` is the only option that closes. | **Day-0, hard gate.** A QQQ condor outliving its exits rides into **physical settlement**. Note `market` fires at **15:50** — same instant as the clone's Expiration exit; they would race. §13.1. |
| **D-4** | **Retire the Excessive Errors Failsafe as a live hypothesis.** | Newest error on either Fortress bot is **`Apr 16, 2026 3:55PM`**. Error days: Apr 16 (91) + Mar 16 (138+); `-NoPT50` Apr 16 (91). **Zero in June.** | §4.5 and every pre-registration entry that still carries it as the candidate cause of the 2026-06-12 lapse. The mechanism is real and this fleet tripped it — in March/April, on **entry scanners**. The June cause is still **unknown**. |

**Also awaiting a call, lower stakes:** the two writes left on the clone by check #4 (preset
`TIER2-CHECK4-PUTSIDE`; `Fortress-ScannerA-PutSpread-CLONE` saved with a re-serialized `exits`
blob) — detail under *WRITES MADE TO THE CLONE* below.

---

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

### Pilot clone — parts 1 and 2 done, ritual still incomplete
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
- **CHROME-DIRECT OA EDITS.** Part 1's trial verdict was **qualified pass — Claude reads and
  detects, Andy clicks.** Part 2: **Andy released Claude to drive and to save, in-session.**
  `build-plan.md` §5 / `CLAUDE.md` §5 remain **UNAMENDED**; "Andy makes all OA edits" stands
  textually. Doc amendment still pending Andy's decision.

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
