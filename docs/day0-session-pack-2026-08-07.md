# Day-0 session pack — written 2026-08-07

**What this is.** Four ready-to-paste session prompts covering reactivation day end to end, written
while the OA account is locked so that Day-0 runs on **Pro-tier models with zero re-derivation**.
Each prompt is self-contained: paste it into a fresh chat, and that session knows what it needs
without reading this file first.

**What this is NOT.** It is not a plan. `docs/reactivation-runbook.md` (801 lines) is the plan and it
governs. **These prompts EXECUTE it. Nothing here re-plans, re-orders or re-scopes a runbook step**,
and where the lockout forced a sequencing question it is raised as an Andy gate (S0 gate A2), never
resolved silently.

**This session wrote exactly one file — this one.** No existing doc was edited. No OA action was
attempted (impossible — the account is disabled). No git command in any form.

---

# §0 · THE STANDING PREAMBLE

Every prompt below already embeds this block. It is repeated here once so it can be maintained in
one place; if you edit it, edit it in all four prompts too.

## 0.1 Standing facts — true in every Day-0 session

1. ⛔ **NEVER RUN GIT. In any form, including `git status`.** The device bridge cannot unlink files,
   so a git run from this side strands `.git/index.lock` and Andy has to remove it by hand
   (established 2026-07-31; two slips in one night 2026-08-06, different sessions). File
   verification is **`device_bash` sha256 plus a single-match grep of the new text** — never the
   write tool's response, never a stage-back read (`CLAUDE.md` §9.1a; stage-backs serve stale
   content under fresh metadata, reproduced 2026-07-31). **Andy runs every commit.**

2. ⛔ **SESSIONS START LOGGED OUT.** The OA login page read **"Account disabled, please purchase a
   plan"** at ~04:20 ET 2026-08-07. This **SUPERSEDES** the standing "the account-inactive banner is
   cosmetic, not a save-blocker" finding — that finding was TRUE through ~04:00 08-07 (every write
   server-verified through hard reloads) and then OA escalated from *inactive* to *fully disabled*.
   Do not expect a live session. Do not log in and poke. **Purchasing IS Day-0.**

3. ⛔ **NOTES: DOUBLE-ESCAPE FROM THE FIRST WRITE.** OA's sanitizer **decodes entities, then strips
   unknown tags** — `&lt;capture&gt;` becomes `<capture>` and is then removed as markup, and the
   rendered panel looks correct. Write `&amp;lt;` so one decode pass leaves `&lt;` intact. **Verify
   by byte-exact length-and-content compare against the source, never by reading the panel.**
   Reproduced and defeated on PR-14 (two lost writes, 2324/2339 both times).

4. ⛔ **DECISION-NODE INNER-ATTACH: use `NOT`, never a rebuild.** OA's decision editor has **no
   move-node control** (its menu is Settings / Precede with / Copy Action / Edit Caption / Edit
   Notes / Delete). To move an action onto the other branch you would have to delete and rebuild the
   whole action *including its `exits` bundle*. **Do not.** `NOT` is first-class on the criterion
   toolbar (`Create Group | NOT | 🗑`) and stores as `not:true` on the criterion — logically
   identical, action node left byte-untouched. This is how PR-01's re-entry gate was built
   (`postagtoday{oc:opened, not:true, tag:"put|call side"}`, action left on YES).

5. ⛔ **PICKER NO-OP — force with a two-step.** Clicking a picker's already-displayed value is a
   **no-op**; the field never materializes. Force it with a two-step through a different value and
   back (e.g. `exitrate`: Instant `0` → save → Every 1m `1` → save). **Verify the STORED model
   field, not the rendering.** Record the intermediate state rather than hiding it, and only do this
   while the bot is inert (AUTOMATIONS OFF, no positions).

6. **Clicking, on this app.** Element-**ref** clicks silently no-op and the tool still reports
   success. JS event dispatch (`pointerdown→…→click`) is blocked by the Cowork harness classifier on
   this app. **The path that works from Cowork: compute the target from the DOM.**
   `scale = screenshotWidth / window.innerWidth`; click at `rect.centre × scale`.
   ⚠️ **Never carry a coordinate across a window resize** — the ratio changed mid-session on
   2026-08-07 (2560×1314/1548×795 → 3456×1314/1568×596) and silently invalidated every in-flight
   coordinate. Re-derive the scale after any resize.

7. **Other app traps, all first-hand.** `overlay.innerText` goes stale while a drawer animates —
   screenshot before concluding a click failed. The title editor commits on **blur**, not Enter.
   `Runtime.evaluate` times out at ~45s **with the work COMMITTED** — re-read state, **never re-fire
   the action**. `form_input` over `computer.type`; re-read `.value` after every text entry. Tag
   widgets need per-character `input` events — click the suggestion item. OA lowercases tags and
   maps non-alphanumerics to spaces: `PR-01` stores as `pr 01`. Tags live on the bot's **Dashboard**
   tab, not Settings. `a5.bots.bot` is the hydrated client model and is better Layer-1 evidence than
   any DOM scrape.

8. ⛔ **`archiveBot` IS ANDY'S HAND. 3-for-3 failed from this side** (2026-08-04, and again
   2026-08-07 as `showBotMenu`). **Three attempts, then stop.** ⛔ **Never fall back to raw
   coordinates on that menu** — `Delete` sits ~29px below `Archive` and a mis-landed click is
   unrecoverable. Renames DO commit; the rename is what frees the production name, so the archive is
   hygiene, not a blocker.

9. **Two-layer OA edit proof, every edit, no substitutions** (`CLAUDE.md` §5, `oa-ops-runbook.md`
   §4). **Layer 1** — re-observe the changed value from OA itself after a hard reload (screenshot for
   toggle/UI state, fresh capture/model read for text-capturable fields). **Layer 2** — the first NEW
   position's **Trades list**. ⛔ **The Exit Options panel is NEVER evidence.** A save confirmation,
   a toast, or a tool-success message is never either layer.

10. **Decisions stay gated; evidence-backed corrections of falsified claims may be applied
    directly** — the five-condition test in `CLAUDE.md` §5. **When it is ambiguous, it is gated.**
    Inference from absence is never an evidence-backed correction.

11. **Close out after each piece of work, not once at the end** (`CLAUDE.md` §9.1): append
    `session-log.md` (+ `state.md` if a stated fact changed) → update the `bot-fleet-migration`
    tracker via `update_artifact` → say "ready to commit" with the changed-files list. **The tracker
    verifies by Andy's visual confirmation and the close-out is not complete without it.**

12. **Close the chat at a clean boundary.** Long OA build chats saturate and start dropping reads.
    Stop at a per-bot / per-step boundary and hand to the next session against a written close-out.

## 0.2 The STOP ladder

Applies to every action in every session. It is what makes a Sonnet session safe.

```
1. Do it the documented way.
2. Failed? Try the ONE documented alternative. (Never a third invented method.)
3. Failed again? THIRD attempt maximum — then STOP.
     - Do NOT force it.
     - Do NOT fall back to raw coordinates.
     - Do NOT improvise a remedy. build-plan.md is under decision freeze
       and Day-0 is not a build day.
4. Record what was attempted, verbatim, and take the runbook's own branch:
     "bot stays OFF"   -> that bot does not trade today; the fleet proceeds.
     "fleet stays OFF" -> nothing else is switched on today; stop the sequence.
     unrun check       -> NOT EVALUABLE. Written down by name. NEVER a pass.
5. Ambiguous / two frozen decisions conflict / it would change a decision
   -> GATED. Escalate to Andy. Stop that thread; the others proceed.
6. MODEL ESCALATION: a Sonnet session that reaches step 5, or that finds a
   documented branch does not fit what it is actually seeing, STOPS and hands
   to Andy. Andy re-opens it in an Opus session. A Sonnet session never
   reasons its way past a gate.
```

## 0.3 Andy's steps — the gates that are HIS hands, in order

| # | Gate | Session | Why it cannot be Claude's |
|---|---|---|---|
| A1 | **Log in and purchase the plan** | S0 | Payment. Also the only way in — the account is disabled. |
| A2 | **Acknowledge the pay-before-`itmlive` order** (S0 §2) | S0 | Runbook §4 says do not reorder; the lockout forced it. One line. |
| A3 | **Rule / re-confirm F-C1 and F-C2** if not already recorded in the folder | S0 | The rulings exist only in project memory (see §1.3). |
| A4 | **Declare the roster and A-series verdict accepted** | S0 | Same class as "Andy declares the pilot clean" (runbook §3 Step A). |
| A5 | **The ~23 archive clicks** (20 Group-A + 3 clone originals) | S3 | `archiveBot` 3-for-3 failed from this side. |
| A6 | **Ride-or-close decision on the 5 open mirror positions — drafted, SIGNED, and EXECUTED** | S2 Step 2 | Capital decision. Go-live authority is Andy's. |
| A7 | **Sign every pre-registration entry** (20 plan bots + the ride-or-close entry) | S2 Step 2b | "Andy signs and dates. Only then may the bot be switched ON." |
| A8 | **Rule the three open signature items**: PR-16 T1 δ/p/floor (G-12b), PR-18 "Breakeven" naming, G-1′ | S2 Step 2b | Unfilled field ⇒ unsigned entry (ledger §7 item 2). |
| A9 | **Run `bash scripts/daily.sh` at n=0 from his own terminal** | S0 pre-flight | `tape.py` needs network; `device_bash` has none. |
| A10 | **Visually confirm the tracker artifact** | every close-out | §9.1a — the tracker is the one dashboard Andy reads. |
| A11 | **Run every commit** | every close-out | The bridge cannot unlink; git from this side strands lock files. |

---

# §1 · PRE-FLIGHT STATE — what is true as of 2026-08-07

Read fresh from the folder this session. Every prompt below repeats the parts it needs.

## 1.1 The fleet, as built

**Expected roster at reactivation: 41 active bots · 9 slots left of the Pro 50.**
Arithmetic: 35 (2026-07-30 capture) − 2 deleted (sweep, 08-06 night) = 33; + 7 greenfield = 40;
+ 1 PR-01 clone = **41**. The `/bots` footer read `40 active bots • 10 left` immediately before the
PR-01 clone. The PR-01 original was **renamed, not archived** — it still counts.

**The greenfield family — COMPLETE, 7 of 7, server-verified, nothing ON.**
All seven: Paper · `seed 2500` · limits 2/2 · scan 1m/1m · Day Trading Allowed · Group `IC` ·
`status "off"` (AUTOMATIONS OFF) · `disableExits 0` (EXIT OPTIONS ON) · symbols empty · both bot
inputs bound, non-empty and EQUAL · three shared automations attached by `rid` (**attach, not
copy** — the Library reads "7 bots" on each) · Notes byte-exact · Template V1 each.

| Arm | PR | Bot ID | Mechanic |
|---|---|---|---|
| `GF-QQQ-IC-Ride` | PR-14 | `BOTfw5TkkCRF4417860701930934951` | control, base only, `mechanics = {}` |
| `-PT50` | PR-15 | `…4417860738688735152` | `profits 0.5` + `smprofits speedy` |
| `-Trail` | PR-16 | `…4417860754672239833` | `tstop {target:40, trail:15}` + `smtstop normal` |
| `-Touch0` | PR-17 | `…4417860760818962144` | `touch {usd, 0}` + `smtouch normal` |
| `-SL100` | PR-18 | `…4417860767788927225` | `stoploss 1` + `smstoploss normal` |
| `-SL200` | PR-19 | `…4417860785000861357` | `stoploss 2` + `smstoploss normal` |
| `-Canary` | PR-20 | `…4417860774419022836` | `profits 0.05` + `smprofits speedy` |

Shared objects and A7 baselines (in `data/bots_config_v2.csv`):
`GF-ScannerA-PutSpread` **`3308ce8b476d2bd090d9519b445748fc4c0d0fdbe71861c83a249729b1a5a30a`** @ v9
(A7-DRIFT-1 ruled ADOPT 2026-08-07, applied) · `GF-ScannerB-CallSpread`
`bb4ba866a13e7ecd682f7bda9a19011003e9e3ef73fffd0fb64a80a4cd0eb32e` @ v2 ·
`GF-Backstop-1552-FlatClose` `116069bddf8b8c9e58bd8f28313c2ad95726fa3f7205df4dfde82de7a3e2e5b5` @ v1.
Library holds exactly **4** objects: those three (7 bots each) + `Defang-Mon-S2-StrikeTouch` (2 bots).

**Asserts at n=7, all runnable ones green** —
`data/captures/2026-08-07-greenfield/ASSERTS-A1-A9-and-capture-diff.txt`:
**A1 21/21** (amended rule) · **A2 7/7** (12 of 12 non-bundle fields equal) · **A3 7/7** ·
**A7 3/3** · **A8 7/7** · **A9 7/7**. A4 struck moot · **A5 · A4b · A6 not runnable pre-Day-0**
(A5 needs the account fields re-read; A4b and A6 need positions).

**Clones — 2 of 4 done.** Pilot `QQQ-IC-0DTE-Fortress` (PR-03, 08-03/04, declared clean by Andy
2026-08-06). `IC-SPX-FastPT25-S2` (PR-01, 08-07) — clone `BOTfw5TkkCRF4417860821948715488`, n=0,
AUTOMATIONS OFF, EXIT OPTIONS OFF, group `IC-Focus`, tags `live candidate,focus ic`, allocation
$50,000, limits 10/10; original renamed `IC-SPX-FastPT25-S2-ARCHIVED-2026-08-07`
(`BOTfw5TkkCRF1217757048550308561`) and verified byte-identical to its Step-0 baseline.
**PR-02 (`-130PM`) and PR-04 (`-NoPT50`) were never started — both originals untouched and
un-renamed.**

## 1.2 What is NOT done — the Day-0 work list

**⛔ HARD BLOCKERS still unticked on the runbook's Pre-Day-0 checklist:**

- `itmlive` = `market` (runbook §4 Step 0a). `itmpaper` is already `market` — **do not re-set it**.
- `LEDGER_START` set in `build_ledger.py` and verified by an n=0 run. Currently
  `data/ledger_meta.json` reads `"ledger_start": "2099-01-01"` — a refuse-everything sentinel, which
  is correct pre-Day-0, not a value to keep.
- **Template V2 on the pilot** (15:50 Expiration exit re-priced OFF Market → SmartPricing internal
  value `speedy`, **NOT `fast`**; the 15:52 backstop KEEPS Market) **with its AMENDED PR-03 signed.**
  ⚠️ Without V2 the three 15:50–15:52 mechanics are three Market orders in two minutes with only
  memo strings between them.
- `daily.sh` n=0 dry run passing end to end.
- Sizing written down: 1 lot experiments, ≈$5K risk/position CANDIDATE+, identical across arms.
- Ride-or-close prepared, **signed, and ready to EXECUTE** on the 5 open mirror positions.
- Every pre-registration entry SIGNED, including the nine untouched.
- Phase 0 `C9` (firing semantics — re-scoped to a Day-0 pre-switch-on read) and the **A7 baselines
  wired into `daily.sh`**. ⚠️ The baselines ARE recorded in `bots_config_v2.csv`; **A7 is not wired
  into `daily.sh`** — `daily.sh`'s eight stages carry `execution_audit.py` as the detector and no
  A-series runner. The A-series is currently run by hand. That is an open Step-4(b) gate.
  `C0c · C2 · C7 · C8` are **CLOSED** (decision card 2026-08-06 late-night Phase 0 closure).
- ✅ `data/raw/` and `data/brief/` are **empty** — the pre-cutover-files box is satisfiable by a read.
- ✅ `data/mirror_baseline.csv` written 2026-08-04, 10 rows / 174 positions. **It is an anchor — do
  not recompute it, do not pass `--force`.**

**Build-side leftovers:**

- PR-01 clone: **Template V1 + PR-01 Notes + `pr 01` tag** (record artifacts; nothing depends on
  them) — not done, `showBotMenu` went dead.
- **PR-02 (`-130PM`) and PR-04 (`-NoPT50`) clones** — never started.
- **The ~23 archives** (20 Group-A + 3 clone originals) — **Andy's hand.**
- The pilot's **Bot Group** (runbook §3 Step A, audit F-21).

**Open observations queued to Day-0, each with a decision tree already written:**
Step 2c no-touch · Step 5a **D3 DST** (`ntime=1552` vs 16:52 ET under EDT — reproduces on all six
arms, `startDate 2026-08-07T20:52:00.000Z`) · Step 6 the 15:50 attribution · Step 6a **D4 mechanism
verdict** · Step 6b **C10 `dstop` unit** (blocks ARM-B1) · Tier-2 **§9 #5**.
**Any one left unread at close-out is reported OPEN, never passed.**

## 1.3 ⛔ THREE DIVERGENCES THIS SESSION FOUND — read before S0

**(a) The lockout is NOT in `docs/state.md` or `docs/session-log.md`.** It exists only in project
memory (`greenfield-build-status`). The last `state.md` block is the 08-07 morning clone sweep and
the last `session-log.md` entry is the same session — both written ~06:20, both silent on the
~04:20 disable. **S0 records it.**

**(b) The F-C1 and F-C2 rulings are NOT in the folder either.** `state.md` line 1495 and
`session-log.md` line 5198 both still read **GATED**. Project memory `greenfield-build-status`
records them as ruled — **F-C1: REMOVE PT25 from the clones' Open actions** (the controls are
genuinely Exit-Option-free) and **F-C2: Trap 10 authorized** — but a memory note is not the folder.
⛔ **S0 opens with Andy re-confirming both in one line before any edit is made** (gate A3), then
records them in `state.md` + `session-log.md` as ruled-and-applied. Two documents vouching for each
other is a citation loop; a ruling that lives only in memory is worse.

**(c) Uncommitted work is sitting in the tree.** `docs/decision-card-2026-08-06.md` is modified and
`data/captures/2026-08-06-gfam/GF-Backstop-1552-FlatClose.txt` is untracked. **Andy commits before
Day-0 starts** — an untracked folder cannot be diffed or reverted, and Day-0 is the worst day to
discover that.

---

# §2 · SESSION PROMPTS

Run in order. **S0 → S1 → S2 → S3.** Each hands off to the next in writing.

---

## S0 — REACTIVATION OPENING

**Model: Sonnet.** Escalate to Opus only if §1's roster or the A-series diverges — that is a STOP,
not a judgment call, and the judgment about what to do next is Andy's.
**Andy attended: yes, for gates A1–A4.** Everything after gate A4 is unattended-safe.

```text
You are working in bot-fleet-v2 (~/bot-fleet-v2 via the device bridge). TODAY IS DAY-0: the OA
account is being reactivated. This is the OPENING session. Its job is to establish that the fleet
came out of the lockout exactly as it went in, then finish the two record artifacts the lockout
interrupted. It does NOT run the Day-0 sequence — that is a later session.

READ FIRST, FRESH, IN THIS ORDER (never from memory of a prior session):
  docs/day0-session-pack-2026-08-07.md  §0, §1  (this pack — your standing facts and pre-flight)
  docs/state.md                          the 2026-08-07 blocks and the clone-sweep banner at the tail
  docs/session-log.md                    the last two entries
  docs/reactivation-runbook.md           §2 (the per-clone checklist), §3 Step B, §4 Steps 0, 0a, 1
  docs/oa-ops-runbook.md                 §1 (capture ritual), §4 (edit verification), §5 (traps)
  docs/build-plan.md                     §2B (the four clones' specs — FROZEN)
  data/bots_config_v2.csv                the config record — 3 shared automations + 8 bots
  data/captures/2026-08-07-greenfield/ASSERTS-A1-A9-and-capture-diff.txt
  project memory: greenfield-build-status, clone-sweep-status

=== STANDING FACTS — TRUE ALL SESSION ===
1. NEVER RUN GIT, in any form, INCLUDING `git status`. The bridge cannot unlink, so git from this
   side strands .git/index.lock and Andy removes it by hand. Verify files by direct `device_bash`
   sha256 + a single-match grep of the new text. Never the write tool's response, never a
   stage-back read (stage-backs serve stale content under fresh metadata). ANDY RUNS EVERY COMMIT.
2. YOU START LOGGED OUT. At ~04:20 ET 2026-08-07 the OA login page read "Account disabled, please
   purchase a plan". This SUPERSEDES the old "the inactive banner is cosmetic" finding — that was
   true through ~04:00 08-07, then OA escalated from inactive to fully disabled.
3. NOTES: DOUBLE-ESCAPE FROM THE FIRST WRITE. OA's sanitizer decodes entities THEN strips unknown
   tags, so `&lt;capture&gt;` silently vanishes and the rendered panel still looks right. Write
   `&amp;lt;`. Verify by byte-exact length-and-content compare against the source, never by
   reading the panel.
4. DECISION NODES: use the `NOT` operator, never a rebuild. OA has no move-node control; moving an
   action to the other branch means deleting and rebuilding it including its `exits` bundle. `NOT`
   is first-class on the criterion toolbar and stores as `not:true`.
5. PICKERS NO-OP on the already-displayed value. Force with a two-step through another value and
   back. Verify the STORED model field, not the rendering. Only while the bot is inert.
6. CLICKING: element-ref clicks silently no-op and the tool still reports success; JS event
   dispatch is blocked by the harness on this app. Compute from the DOM:
   scale = screenshotWidth / window.innerWidth, click at rect.centre × scale.
   NEVER carry a coordinate across a window resize — re-derive the scale.
7. `Runtime.evaluate` times out at ~45s WITH THE WORK COMMITTED — re-read state, never re-fire.
   Title fields commit on BLUR, not Enter. `overlay.innerText` goes stale mid-animation —
   screenshot before concluding a click failed. Prefer `form_input` and re-read `.value`.
   Tags: click the suggestion item; OA stores `PR-01` as `pr 01`; tags live on the DASHBOARD tab.
   `a5.bots.bot` is the hydrated client model and beats any DOM scrape as Layer-1 evidence.
8. `archiveBot` / `showBotMenu` are ANDY'S HAND — 3-for-3 failed from this side. Three attempts,
   then STOP. NEVER fall back to raw coordinates on that menu: `Delete` sits ~29px below `Archive`.
9. TWO-LAYER EDIT PROOF, no substitutions. Layer 1 = re-observe the changed value from OA after a
   HARD RELOAD. Layer 2 = the first NEW position's Trades list. The Exit Options panel is NEVER
   evidence. A save confirmation proves nothing.
10. Decisions stay gated; evidence-backed corrections of falsified claims may be applied directly
    (CLAUDE.md §5's five conditions). WHEN IT IS AMBIGUOUS, IT IS GATED.

=== THE STOP LADDER ===
Documented method -> ONE documented alternative -> third attempt max -> STOP. Do not force, do not
fall back to coordinates, do not improvise a remedy. Record verbatim what was attempted and take
the runbook's own branch: "bot stays OFF" (fleet proceeds) / "fleet stays OFF" (stop the sequence)
/ an unrun check is NOT EVALUABLE and is never a pass. Ambiguous or decision-touching -> GATED,
escalate to Andy, stop that thread. You do not reason past a gate; you stop and hand it to Andy.

=== ⛔ ANDY'S STEPS — HIS HANDS, NOT YOURS ===
A1. ANDY LOGS IN AND PURCHASES THE PLAN. Ask for it, then WAIT. Record the exact payment timestamp
    he reports (date + time + timezone) — that timestamp is LEDGER_START and a later session sets
    it. Do not attempt to log in or pay.
A2. ANDY ACKNOWLEDGES A SEQUENCING NOTE, in one line. The runbook puts Step 0a (`itmlive` =
    `market`, "HARD GATE, before any capital is live") BEFORE Step 1 (pay), and §4 says do not
    reorder the steps. THE LOCKOUT MAKES THAT ORDER IMPOSSIBLE — `/settings` is unreachable until
    the plan is purchased. The gate's INTENT is preserved: no capital is live until Step 7 turns
    AUTOMATIONS on, and nothing is switched on in this session or the next. State this to Andy
    plainly and get an explicit acknowledgment before you set `itmlive`. DO NOT proceed on your own
    reading of it. If he declines, `itmlive` stays `auto`, you record it, and FLEET STAYS OFF.
A3. ANDY RE-CONFIRMS F-C1 AND F-C2 IN ONE LINE. Project memory records them as ruled — F-C1: REMOVE
    `exits.profits` (PT25) from BOTH Open Position actions of the champion pair, per build-plan.md
    §2B; F-C2: authorize `disableExits` resets 1→0 on clone as oa-ops-runbook.md §5 Trap 10 — but
    docs/state.md and docs/session-log.md BOTH STILL READ "GATED". A ruling that lives only in
    memory is not a ruling in the folder. Get the one-line re-confirmation, then apply and record.
    IF HE DOES NOT RE-CONFIRM: change nothing, record it as still GATED, and PR-01 and PR-02 keep
    their INVERTED-check failure-by-construction. Their Day-0 verification stays blocked.
A4. ANDY DECLARES THE ROSTER + A-SERIES VERDICT ACCEPTED, before you write the close-out. Same
    class as "Andy declares the pilot clean" — you do not self-certify it.

=== YOUR WORK, IN ORDER ===

STEP 1 — Wait for gate A1. Record the payment timestamp verbatim. Do not set LEDGER_START (that is
the next session's Step 1); just carry the timestamp into the close-out under a heading a later
session cannot miss.

STEP 2 — Gate A2, then runbook §4 Step 0a: /settings -> set `itmlive` = `market` -> HARD RELOAD ->
re-read `input.value` -> screenshot before and after. A save banner is not verification.
  ⚠️ `itmpaper` is ALREADY `market` (set + verified 2026-08-04). DO NOT RE-SET IT. Read it back as
     part of the same self-check.
  ⛔ IF the value will not persist through a hard reload -> NO CAPITAL GOES LIVE. FLEET STAYS OFF.
     Escalate to Andy: YES.
  While you are on /settings, record all seven account-level fields — they are in no /bots capture
  and they override every bot: itmlive · itmpaper · maxexits · scanstart · scanend · exitstart ·
  exitend. Expected from 2026-08-04: maxexits = 0 (Unlimited) · Bot Schedule 09:31/5 and 09:31/1.
  ⛔ `maxexits` is the dangerous one — a non-zero value reproduces the June failure shape fleet-wide
  with nothing per-bot to show for it. This closes assert A5. Record the values verbatim.

STEP 3 — VERIFY THE ROSTER. Bookmarklet capture of /bots FIRST — write the expected count down
before you capture. EXPECTED: 41 active bots, 9 left of the Pro 50.
  Arithmetic: 35 (2026-07-30) − 2 deleted = 33; + 7 greenfield = 40; + 1 PR-01 clone = 41. The
  PR-01 original was RENAMED, not archived, so it still counts.
  Confirm by name: the seven greenfield arms; `IC-SPX-FastPT25-S2` (the clone, holding the
  production name) and `IC-SPX-FastPT25-S2-ARCHIVED-2026-08-07`; `QQQ-IC-0DTE-Fortress` (pilot
  clone) and `QQQ-IC-0DTE-Fortress-ARCHIVED-2026-08-03`; the nine leave-in-place bots
  (DIR-SPX-PutVIX22-SL75, DIR-SPX-CallVIXdrop, 3DTE $140-$350, Nigiri-Paper-v1, QQQ long call,
  Friday 14 DTE Broken Wing IB (B-70), Trendy-Paper-v1, 60min-ORB-10W-Paper-v1, Tasty Condor);
  the two un-started clone originals `IC-SPX-FastPT25-S2-130PM` and `QQQ-IC-0DTE-Fortress-NoPT50`,
  both expected UNTOUCHED and UN-RENAMED.
  Also read `My Automations`: EXACTLY 4 objects — GF-ScannerA-PutSpread, GF-ScannerB-CallSpread,
  GF-Backstop-1552-FlatClose (7 bots each) and Defang-Mon-S2-StrikeTouch (2 bots).
  ⛔ IF THE COUNT DISAGREES -> recapture ONCE. IF IT STILL DISAGREES -> ⛔ STOP. FLEET STAYS OFF.
     ESCALATE TO ANDY: YES. A short roster silently drops bots from every future drift diff, and
     the drift diff is the whole detector. Do not reconcile it yourself.
  ⛔ IF A BOT IS MISSING, RENAMED, OR AN AUTOMATION'S BOT-COUNT HAS MOVED -> same STOP. The disable
     was supposed to block access, not delete anything; a deletion is a different event entirely
     and it is Andy's call, not yours.

STEP 4 — RE-RUN THE A-SERIES AGAINST FRESH CAPTURES. Not against the 08-07 file — that file is the
reference you compare TO. One page load per bot, after a hard reload, read from `a5.bots.bot` (and
`a5.bots.acedit.routine` for the three Library objects). Never innerText, never a save banner.
  RUN: A1 (21/21 under the AMENDED rule — arm-vs-control differ in exactly ONE mechanic;
       arm-vs-arm in exactly TWO, precisely each arm's own; PT50/Canary and SL100/SL200 share a
       field and differ in ONE, so they are checked under the arm-vs-control rule. ⛔ Build against
       the AMENDED text, not the struck one.)
       A2 (7/7 — every non-bundle field equal INCLUDING trigger config and scan speeds; `exitrate`
       is stored = 1 on all seven since the 08-07 two-step fix)
       A3 (7/7 — each arm's decoded set == its pre-registered set. A3 is the load-bearing one.)
       A5 (from Step 2's /settings read)
       A7 (3/3 — payload hash of each shared automation vs its recorded baseline:
           ScannerA 3308ce8b476d2bd090d9519b445748fc4c0d0fdbe71861c83a249729b1a5a30a @ v9
           ScannerB bb4ba866a13e7ecd682f7bda9a19011003e9e3ef73fffd0fb64a80a4cd0eb32e @ v2
           Backstop 116069bddf8b8c9e58bd8f28313c2ad95726fa3f7205df4dfde82de7a3e2e5b5 @ v1)
       A8 (7/7 — decoded(GF_EXITS_PUT) == decoded(GF_EXITS_CALL) per arm)
       A9 (7/7 — both bot inputs BOUND and NON-EMPTY on every arm)
  ⛔ THE G2 RIDER APPLIES, TWO HOPS DEEP. The saved action stores a REFERENCE, not values. Resolve
     action -> automation input -> BOT input and read the INPUT OBJECT'S VALUE. A capture that
     reads only the action records the input's NAME and every arm diffs as identical — the
     tournament is then undetectably void. ⚠️ NEVER read `oldValue` as current config: it is a
     stale pre-link snapshot. The control is at: bot settings page -> the automation row's ⚙ Edit
     Settings -> 🔗 -> `Bot Inputs`.
  NOT RUNNABLE YET, and say so by name rather than omitting them: A4 (struck moot),
  A4b and A6 (both need positions — they belong to Day-1).
  ⛔ IF ANY ASSERT FAILS -> record the failure verbatim with the bot and the field. DO NOT FIX IT.
     FLEET STAYS OFF for the family. ESCALATE TO ANDY: YES. The family was green on 2026-08-07
     with AUTOMATIONS OFF; a fail now means something changed during a lockout that was supposed
     to block access, and that is a finding, not a repair job.
  ⚠️ A7 drift is NOT automatically a failure — A7-DRIFT-1 (2026-08-07) was ruled ADOPT because the
     tree and the full Open-Position payload diffed field-by-field UNCHANGED. But that ruling was
     Andy's, on evidence. If A7 drifts again: diff the tree and payload field-by-field, report what
     you find, and GATE it. Do not re-baseline on your own.

STEP 5 — APPLY THE RULED F-C1 REMOVAL TO THE PR-01 CLONE (only after gate A3).
  TARGET: `IC-SPX-FastPT25-S2`, the CLONE `BOTfw5TkkCRF4417860821948715488`. NOT the archived
  original — that is a lineage record and stays byte-identical to its Step-0 baseline.
  DO: remove `exits.profits` (0.25) from BOTH Open Position actions — put side and call side.
  Read first-hand 2026-08-07: `exits.profits = 0.25`, `smprofits "normal"`, text "Profits: 25%".
  build-plan.md §2B, verbatim: "PT25 removed from the Open Position action explicitly — not left
  dead behind an off toggle."
  ⛔ REMOVE ONLY `profits`/`smprofits`. Touch nothing else in the bundle, nothing else in the
     action, and nothing in `Scalp-Mon-S2-Cleanup` — S2 depends on Cleanup (build-plan §2B).
  ⛔ DO NOT rebuild the action to do it. If `profits` cannot be cleared in place, STOP —
     rebuilding the action would destroy the exits bundle and the re-entry-gate work.
  VERIFY: hard reload -> re-read `node.input.exits` on both actions -> confirm `profits` is absent
  -> confirm `disableExits` is still 1 (EXIT OPTIONS OFF) -> screenshot the toggle. Re-hash all
  four of the clone's automations and confirm only the two scanners' Open actions moved.
  ⛔ ALSO CONFIRM the ORIGINAL `…-ARCHIVED-2026-08-07` is untouched: `Scalp-Scan-Put` must still
     hash `91da84fd2b7aafbb…`, 5027 bytes, version 2.
  Layer 2 is DEFERRED to Day-0's Step 6 and it is INVERTED for this bot — the Trades list must show
  NO PT row and NO exit-trigger row, and the S2 monitor MUST be firing. Say so in the close-out.

STEP 6 — FINISH PR-01's RECORD ARTIFACTS (interrupted when `showBotMenu` went dead).
  a. Save Template V1 with the PR-01 pre-registration note attached.
  b. Write the PR-01 Notes block. ⛔ DOUBLE-ESCAPE FROM THE FIRST WRITE and verify byte-exact
     length-and-content against the source. The pilot's defect reproduced twice on PR-14 before it
     was defeated this way.
  c. Add the tag. It will store as `pr 01` — that is correct, not a failure. Tags are on the
     DASHBOARD tab. Click the suggestion item; re-read the input's value per add (the tag menu
     serves stale lists after a timeout).
  ⛔ IF `showBotMenu` GOES DEAD AGAIN -> three attempts, then STOP. These are RECORD ARTIFACTS;
     nothing in the Day-0 sequence reads them. Record them as NOT DONE and carry them forward.
     Do not let this block anything.

STEP 7 — RECORD WHAT THE FOLDER IS MISSING. Three items, found 2026-08-07:
  (a) The ~04:20 ET 2026-08-07 lockout ("Account disabled, please purchase a plan") is in project
      memory only — NOT in docs/state.md and NOT in docs/session-log.md. Write it into both, as a
      dated first-hand record, noting that it SUPERSEDED the "inactive banner is cosmetic" finding.
  (b) The F-C1 and F-C2 rulings are in project memory only; state.md line ~1495 and session-log.md
      line ~5198 both still read GATED. Once gate A3 lands, record both as ruled-and-applied with
      the date and Andy's re-confirmation. Leave the original GATED text standing per the doc's
      correction convention.
  (c) `docs/decision-card-2026-08-06.md` was modified and
      `data/captures/2026-08-06-gfam/GF-Backstop-1552-FlatClose.txt` untracked as of 2026-08-07.
      Tell Andy at close-out so the tree is committed before the Day-0 sequence starts.

STEP 8 — PRE-FLIGHT FOR THE NEXT SESSIONS. Read and REPORT, do not fix:
  - `data/raw/` and `data/brief/` — expected EMPTY (they were on 2026-08-07). If not, the
    pre-cutover-files box is unticked and the runbook says resolve before §4 starts.
  - `data/ledger_meta.json` — expected `"ledger_start": "2099-01-01"` (the refuse-everything
    sentinel). It is CORRECT pre-Day-0 and it is NOT the value to keep.
  - ⛔ ANDY'S GATE A9: `daily.sh` at n=0 has NOT been run and is a HARD BLOCKER. You cannot run it
    — `tape.py` needs network and `device_bash` has none. Ask Andy to run `bash scripts/daily.sh`
    from his own terminal and paste the output. Read it against the runbook §3 Step E branches:
    a script that raises -> fix the script, NEVER the data, NEVER seed a synthetic row; `0.0%`
    expectancy or a populated-looking table at n=0 is a FAILURE, not a pass; Tier C rules
    reporting SKIPPED because bots_config_v2.csv is incomplete is CORRECT behaviour — silence in
    its place is the failure. ⛔ Day-0's §4 does not start until a clean end-to-end n=0 run is on
    file.
  - `daily.sh`'s eight stages carry NO A-series runner. The A7 baselines are recorded in
    bots_config_v2.csv but A7 IS NOT WIRED INTO daily.sh, which runbook Step 4(b) requires. Report
    it as an OPEN Step-4(b) gate. Wiring it is Claude Code's lane, not yours.

=== ⛔ WHAT THIS SESSION MUST NOT DO ===
- DO NOT TOUCH ANY OF THE NINE LEAVE-IN-PLACE BOTS, in any way, for any reason. Runbook Step 2c
  requires a NO-TOUCH OBSERVATION of their dashboard toggles before anything is moved, and the
  information it captures is NOT RECOVERABLE afterwards: if exits resume at reactivation with no
  toggle intervention, billing state is implicated as the June cause; touch a toggle first and the
  toggle candidate and the billing candidate become permanently indistinguishable.
  ⚠️ Step 2's ACCOUNT-LEVEL `itmlive` is explicitly NOT toggle intervention. Nothing else may
  touch a bot before Step 2c runs.
- DO NOT switch AUTOMATIONS ON on anything. Not one bot. That is Step 7 of the sequence, two
  sessions from now, and only for bots that passed Step 6.
- DO NOT flip any EXIT OPTIONS toggle on the nine. That is Step 3, in S2.
- DO NOT start the PR-02 or PR-04 clones. That is S1.
- DO NOT archive anything. Andy's hand.
- DO NOT sign a pre-registration entry, or fill a SIGNED line. Andy's, at Step 2b.
- DO NOT run the Day-0 sequence. This session is the opening, not the sequence.

=== CLOSE-OUT (CLAUDE.md §9.1 — mandatory, in this order) ===
1. Append docs/session-log.md; update docs/state.md for every fact that changed (the lockout
   record, the F-C1/F-C2 rulings, the roster verification, the A-series re-run verdict, `itmlive`).
   Verify EVERY edited file by direct `device_bash` sha256 + a single-match grep of the new text.
2. Update the `bot-fleet-migration` tracker artifact via `update_artifact`, and ASK ANDY TO
   VISUALLY CONFIRM IT. The close-out is not complete without his confirmation.
3. Say "ready to commit" with a one-line summary of the changed files. DO NOT COMMIT.
4. HAND-OFF BLOCK for S1, written so the next session needs nothing else:
   - the payment timestamp, verbatim, labelled LEDGER_START CANDIDATE
   - roster verdict: count, and every by-name confirmation or divergence
   - A-series verdict, per assert, including the ones not run and why
   - the seven /settings values, verbatim
   - F-C1 / F-C2: ruled or still gated, and what was applied
   - PR-01: what landed, what did not
   - everything still OPEN, by name — an unrun check is NOT EVALUABLE, never a pass
```

---

## S1 — THE TWO REMAINING CLONES

**Model: Sonnet.** The clone ritual is a nine-step checklist with an explicit branch at every step
and no judgment left in it. Every branch here says either "bot stays OFF, fleet proceeds" or
"escalate" — both are mechanical.
**Andy attended: not required**, except if a branch fires. S1 can run unattended.

```text
You are working in bot-fleet-v2 (~/bot-fleet-v2 via the device bridge). Day-0 is in progress. S0
has run (read its close-out first). Your job: build the last two clones — PR-02 and PR-04 — per the
ruled pattern, and NOTHING else.

READ FIRST, FRESH:
  docs/day0-session-pack-2026-08-07.md   §0, §1, and S0's hand-off block
  docs/session-log.md                     S0's entry, in full
  docs/reactivation-runbook.md            §2 — the nine-step per-clone checklist, IN FULL
  docs/build-plan.md                      §2B — the two clone specs. FROZEN. Nothing beyond spec.
  docs/pilot-clone-card-qqq-fortress.md   the live-follow card; every clone reuses this shape
  docs/oa-ops-runbook.md                  §4 (edit verification), §5 (the traps)
  data/archive/rename_map.csv             the lineage record you append to as you go
  project memory: clone-sweep-status      (⚠️ its "F-C1/F-C2 GATED" lines are superseded if S0
                                           landed gate A3 — S0's close-out is authoritative)

=== STANDING FACTS — TRUE ALL SESSION ===
[Identical to S0's block. Reproduced verbatim so this prompt is self-contained.]
1. NEVER RUN GIT, in any form, INCLUDING `git status`. The bridge cannot unlink, so git from this
   side strands .git/index.lock and Andy removes it by hand. Verify files by direct `device_bash`
   sha256 + a single-match grep. Never the write tool's response, never a stage-back read.
   ANDY RUNS EVERY COMMIT.
2. THE LOCKOUT SUPERSEDED THE OLD BANNER FINDING — sessions start LOGGED OUT unless S0 has already
   reactivated the account. Confirm from S0's close-out; do not assume a live session.
3. NOTES: DOUBLE-ESCAPE FROM THE FIRST WRITE (`&amp;lt;`). OA's sanitizer decodes entities THEN
   strips unknown tags, and the rendered panel still looks correct. Verify byte-exact.
4. DECISION NODES: use `NOT`, never a rebuild. OA has no move-node control; rebuilding an action
   destroys its `exits` bundle.
5. PICKERS NO-OP on the already-displayed value. Force with a two-step. Verify the STORED field.
6. CLICKING: refs silently no-op; JS dispatch is harness-blocked on this app. Compute from the DOM:
   scale = screenshotWidth / window.innerWidth, click at rect.centre × scale. NEVER carry a
   coordinate across a window resize.
7. `Runtime.evaluate` times out at ~45s WITH THE WORK COMMITTED — re-read, never re-fire. Titles
   commit on BLUR. `overlay.innerText` goes stale mid-animation — screenshot first. Prefer
   `form_input`, re-read `.value`. Tags: click the suggestion; `PR-02` stores as `pr 02`; tags are
   on the DASHBOARD tab. `a5.bots.bot` is the hydrated client model.
8. `archiveBot` / `showBotMenu` are ANDY'S HAND. Three attempts, then STOP. NEVER coordinates on
   that menu — `Delete` sits ~29px below `Archive`.
9. TWO-LAYER EDIT PROOF. Layer 1 = re-observe after a HARD RELOAD. Layer 2 = the first NEW
   position's Trades list. The Exit Options panel is NEVER evidence.
10. WHEN IT IS AMBIGUOUS, IT IS GATED.

=== THE STOP LADDER ===
Documented method -> ONE documented alternative -> third attempt max -> STOP. No forcing, no
coordinate fallback, no improvised remedy. Record verbatim and take the runbook's own branch. An
unrun check is NOT EVALUABLE and is never a pass. Ambiguous -> GATED, escalate, stop that thread.
⚠️ ON THIS SESSION SPECIFICALLY: a failed clone stops THAT CLONE. The other one proceeds. Only a
Library-propagation event (step 2's branch) stops both.

=== ⛔ WHAT THIS SESSION MUST NOT DO ===
- DO NOT TOUCH ANY OF THE NINE LEAVE-IN-PLACE BOTS. Step 2c's no-touch observation has not run yet
  and its information is not recoverable afterwards. Clones only.
- DO NOT switch AUTOMATIONS ON. Both clones end this session with AUTOMATIONS OFF.
- DO NOT archive anything — not the originals you rename. Renames commit; archives are Andy's hand
  and they are hygiene, not a blocker.
- DO NOT sign anything.
- DO NOT touch the pilot (`QQQ-IC-0DTE-Fortress`) or the PR-01 clone. Both are finished.
- DO NOT run the Day-0 sequence.

=== ORDER OF WORK: PR-02 FIRST, THEN PR-04. PER-CLONE ATOMIC. ===
Finish and verify one completely before starting the other. A mistake made once is a lesson; the
same mistake across two bots is a rebuild.

────────────────────────────────────────────────────────────────
CLONE 1 — PR-02 · `IC-SPX-FastPT25-S2-130PM`
────────────────────────────────────────────────────────────────
SPEC (build-plan.md §2B, frozen): identical to PR-01 with a 1:30 PM entry. Ride + S2. The entry-time
A/B partner. Same two safety fixes, same Exit-Option-free spec. NO NEW EXIT ARCHITECTURE — it is a
control. ⛔ DO NOT TOUCH `Cleanup` ITSELF — S2 depends on it.

Run runbook §2's nine steps in order. The clone-specific points that cost real time on PR-01:

0. STEP-0 BASELINE CAPTURE OF THE ORIGINAL FIRST, and hash all four of its automations. That
   baseline is what proves later that the original was never touched.
1. RENAME THE ORIGINAL FIRST — `IC-SPX-FastPT25-S2-130PM-ARCHIVED-<today>`. It frees the production
   name and keeps the archived record self-labelling. Titles commit on BLUR.
2. CLONE. ⭐ The Clone Settings drawer exposes Name + Account + Allocation BEFORE creation — set
   the production name and the real allocation THERE. This pre-empts the allocation trap and
   retires the pilot card's temporary-name step entirely.
3. CHECK THE AUTOMATION LIBRARY BEFORE EDITING ANYTHING. ⚠️ CLONING COPIES — the old "clones share
   automations by reference" text is FALSE and corrected. Clone-owned automations read `sharing=0`
   and get NEW rids. Sharing is opt-in via the Library only, and this bot's automations are not in
   it (the Library holds exactly 4 objects: the three GF objects at 7 bots each, and
   `Defang-Mon-S2-StrikeTouch` at 2). So: EDIT DIRECTLY, no fork needed. Then confirm the
   ORIGINAL's automation list is unchanged — a sanity check, one page load.
   ⛔ IF THE ORIGINAL'S LIST CHANGED -> you are editing a shared object and the edit HAS ALREADY
      PROPAGATED. STOP THIS CLONE. Do not proceed. Record which automation and what changed. BOTH
      CLONES STOP until the blast radius is known — check every bot the Library reports as using
      it. ESCALATE TO ANDY: YES.
4. THE FOUR CLONE TRAPS. All four bit on PR-01; check every one, by reading the value back:
   - Allocation resets to a flat `1000` (original $50,000) — a silent 100× sizing error on a bot
     that looks fine on the dashboard. Pre-empt it in the Clone Settings drawer; read it back.
   - Bot Group drops to `None`. PR-01's clone is `IC-Focus` — match it.
   - Tags drop to empty. PR-01's clone carries `live candidate,focus ic`.
   - ⛔ TRAP 10 (F-C2, found 2026-08-07, authorized by Andy): `disableExits` RESETS 1 -> 0 ON
     CLONE. EXIT OPTIONS turns ON. Unlike the other three this makes the clone DO SOMETHING —
     composed with F-C1 it would arm PT25 on a ride benchmark and trip its own REMOVED_EXIT_FIRED
     kill criterion on day one. It is INVISIBLE TO TEXT CAPTURE by construction. RESTORE
     `disableExits` TO 1 AND VERIFY IT — screenshot the toggle, it does not survive text capture.
   Then READ THE SYMBOLS PANEL BACK, character by character, against the original's list. It is
   NOT empty — look at it again; this is the single most common silent clone failure in this fleet.
   ⛔ IF IT IS EMPTY OR DOES NOT MATCH -> re-add ONCE via the form control, re-read `.value`
      (typed input lands intermittently). STILL WRONG -> STOP THIS CLONE, BOT STAYS OFF, the other
      clone proceeds, ESCALATE TO ANDY: YES. Every later step would sit on a bot that never scans.
5. THE TWO SAFETY FIXES, both per the PR-01 pattern, both Layer-1 verified after a hard reload:
   a. RE-ENTRY GATE, on BOTH scanners:
      `countpostag{cop:eq, tags:"…side", count:0, status:"open"}`
        -> `postagtoday{"oc":"opened", "not":true, "tag":"put|call side"}`, ACTION LEFT ON YES.
      ⚠️ This diverges in FORM from the greenfield scanners (plain `postagtoday`, action on NO) and
      the divergence is DELIBERATE and recorded, not smuggled: OA has no move-node control, so the
      NO form requires deleting and rebuilding the Open Position action IN FULL — including its
      `exits` bundle. `NOT` is a first-class criterion operator (`Create Group | NOT | 🗑`) and
      `oc` offers only opened/closed, so there is no negated recipe variant. Logically identical;
      the action node stays byte-untouched. USE THE SAME FORM PR-01 USES.
   b. CLEANUP PRICING: `{"text":"Market","smart":"market"}` -> `{"pct":100, "smart":"speedy"}`.
      ⚠️ §2B says only "Market -> SmartPricing" and does not name a tier. PR-01 chose `speedy`
      (= Fast) as byte-identical to this same bot's own StrikeTouch closes — least-invention.
      USE `speedy`. Do not re-open the choice. ⛔ Nothing else in Cleanup is touched.
6. ⛔ F-C1 — APPLY THE RULED PT25 REMOVAL, on the CLONE only. Remove `exits.profits` (0.25) and
   `smprofits` from BOTH Open Position actions, put side and call side. build-plan.md §2B: "PT25
   removed from the Open Position action explicitly — not left dead behind an off toggle."
   ⛔ PRECONDITION: S0's gate A3 landed and F-C1 reads RULED: REMOVE in S0's close-out. IF IT IS
      STILL GATED -> DO NOT REMOVE IT. Build the clone with PT25 in place, record that PR-02's Day-0
      INVERTED check fails by construction exactly as PR-01's does, and ESCALATE TO ANDY: YES.
   ⛔ Remove ONLY `profits`/`smprofits`. Do not rebuild the action to do it — that destroys the
      exits bundle and the re-entry-gate work. If it cannot be cleared in place, STOP.
7. NO-UNINTENDED-EDITS PROOF, BY HASH, NOT BY EYE. Re-hash the ORIGINAL's automations after every
   clone edit and confirm they are byte-identical to the Step-0 baseline. Confirm all four of the
   clone's automations carry DIFFERENT rids from the original's. (On PR-01: the original's
   `Scalp-Scan-Put` still hashed `91da84fd2b7aafbb…`, 5027 bytes, v2, after every edit.)
8. CAPTURE the automation tree -> `data/captures/<date>-clones/`. Save Template V1 with the PR-02
   pre-registration note attached (⛔ DOUBLE-ESCAPE, verify byte-exact). Add the tag — it stores as
   `pr 02`, which is correct.
9. VERIFY BOTH DASHBOARD TOGGLES AND SCREENSHOT THEM. For this bot EXIT OPTIONS stays OFF BY DESIGN
   and PT25 is removed from the action — VERIFY THE REMOVAL, not the toggle.
   ⛔ IF PT25 IS STILL PRESENT after step 6 and F-C1 was ruled -> BOT STAYS OFF, ESCALATE: YES.
   Layer 2 is DEFERRED TO DAY-0 AND IT IS INVERTED: the Trades list must show NO PT row and NO
   exit-trigger row, and the S2 monitor MUST be firing. ⚠️ Monitor silence is NOT "ride behavior
   intact" — zero log rows is a liveness RED.
10. APPEND `data/archive/rename_map.csv` AS YOU GO, not afterwards from memory:
    original_name, archived_as, clone_name, date, disposition. It is the only thing that will later
    connect a name in the frozen ledger to a bot running today. Append the row to
    `data/bots_config_v2.csv` too, with the config-capture hash.

────────────────────────────────────────────────────────────────
CLONE 2 — PR-04 · `QQQ-IC-0DTE-Fortress-NoPT50`
────────────────────────────────────────────────────────────────
Same nine steps, same four traps, same hash proof, same rename_map row.
SPEC (build-plan.md §2B, frozen): 15:50 time exit + 15:52 flat-close Scheduled Event backstop.
**NO PT50.** This restores the bot's declared no-PT design and preserves the real A/B — PT50 vs
none, against the pilot clone, everything else matched. The name stays; it is now accurate.

DIFFERENCES FROM PR-02, and they matter:
- ⚠️ THE SYMBOLS TRAP DOES NOT BITE THIS FAMILY. The Fortress pair's symbol is AUTOMATION-RESIDENT
  (`Loop QQQ` + action `Symbol: QQQ`) and carried across the clone correctly on the pilot. It still
  bites any bot using the Bot Symbols loop. CHECK WHICH KIND YOU HAVE — do not assume either way.
- F-C1 DOES NOT APPLY. F-C1 is about the champion pair's PT25. This bot's spec is "no PT50", which
  is a different clause. Read the action and confirm no `profits` is present; if one IS present,
  that is a NEW finding — record it and GATE it. Do not treat it as F-C1 by analogy.
- THE 15:52 BACKSTOP. ⛔ IF IT IS NOT BUILDABLE, that does NOT make the clone unclean — it is a
  known unknown with its own branch: LEAVE IT UNBUILT, FLAG IT, FINISH THE CARD. ⛔ DO NOT
  SUBSTITUTE A DIFFERENT TIME. The minute is in build-plan.md §2B and §0 says do not improvise a
  change here on the day.
- ⚠️ D3 IS OPEN AND IT BEARS ON THIS BOT. The 15:52 trigger serialises `startDate
  …T20:52:00.000Z` = 15:52 at UTC−5 but **16:52 ET in August (EDT)**. `ntime=1552` is the operative
  field and nobody has observed which one wins. It is UNRESOLVED and it is READ AT STEP 5a OF THE
  SEQUENCE, not here. Build to spec; do not re-time anything; note in the close-out that this bot
  is affected.

=== CLOSE-OUT (CLAUDE.md §9.1 — mandatory, after EACH clone, not once at the end) ===
1. Append docs/session-log.md; update docs/state.md. Verify every edited file by direct
   `device_bash` sha256 + a single-match grep. Rows in rename_map.csv and bots_config_v2.csv.
2. Update the `bot-fleet-migration` tracker via `update_artifact`; ASK ANDY TO VISUALLY CONFIRM.
3. "Ready to commit" + the changed-files list. DO NOT COMMIT.
4. HAND-OFF FOR S2: per clone — built / partial / stopped and why; F-C1 applied or still gated;
   every toggle state with its screenshot filename; the capture hash; the rename_map row; the
   Layer-2 INVERTED check queued for Step 6; and every branch that fired, verbatim.
   ⛔ State plainly which of the four clones now have a signable config-capture hash. A bot whose
   hash is NOT ESTABLISHED cannot be signed at Step 2b, and a bot that is not signed stays OFF for
   the whole of Day-0.
```

---

## S2 — THE DAY-0 SEQUENCE, STEPS 0 → 8

**Model: Opus.** This is where judgment is real: the mechanism verdict that settles §1 either way,
the C10 unit read that exists exactly once, the DST verdict, and the three-mechanics-in-two-minutes
attribution. Each has a written decision tree, but reading which branch you are actually in is not
mechanical.
**Andy attended: YES, throughout.** Gates A6, A7, A8 are his and they sit in the middle of the
sequence.

```text
You are working in bot-fleet-v2 (~/bot-fleet-v2 via the device bridge). This is DAY-0's MAIN
SEQUENCE. S0 and S1 have run. Your job is to execute docs/reactivation-runbook.md §4, Steps 0
through 8, in order, and NOTHING ELSE.

⛔ YOU DO NOT RE-PLAN THIS. The runbook is 801 lines and it governs. Every check below carries an
explicit branch and there is no step that requires you to invent a remedy. Where a branch says
escalate, escalate and stop that thread. build-plan.md is under decision freeze and DAY-0 IS NOT A
BUILD DAY.

READ FIRST, FRESH, IN FULL:
  docs/reactivation-runbook.md            THE WHOLE FILE. §4 is not self-contained — the Pre-Day-0
                                          checklist at the foot is a set of PRECONDITIONS for it,
                                          and Step 4 does not re-assert them.
  docs/day0-session-pack-2026-08-07.md    §0, §1, and S0's + S1's hand-off blocks
  docs/session-log.md                     the S0 and S1 entries, in full
  docs/pre-registration-ledger.md         §2 (template), §4–§6 (entries), §7 (signing checklist),
                                          §8 (open items)
  docs/greenfield-family-spec.md          §8.3 (the A-series, A1 AMENDED), §9 (the seven DRAFT
                                          entries PR-14…PR-20 — this is where they live, NOT in
                                          the ledger), §12 (open items)
  docs/post-u1-package-2026-08-07.md      the two ruling slots, and §1.7's ready-to-paste PR-16 text
  docs/oa-ops-runbook.md                  §4 (edit verification), §4.3 (the inverted check)
  docs/decision-card-2026-08-06.md · docs/g-rulings-card-2026-08-07.md   the ruled sheets
  docs/mirror-funding-memo-2026-08-05.md  §1, §9 — for Step 2's mirror verdict
  docs/build-plan.md                      §2 — FROZEN
  project memory: greenfield-build-status, decision-card-2026-08-06, mirror-funding

=== STANDING FACTS — TRUE ALL SESSION ===
[Identical to S0's block. Reproduced verbatim so this prompt is self-contained.]
1. NEVER RUN GIT, in any form, INCLUDING `git status`. The bridge cannot unlink; git from this side
   strands .git/index.lock. Verify by direct `device_bash` sha256 + single-match grep. Never the
   write tool's response, never a stage-back read. ANDY RUNS EVERY COMMIT.
2. The ~04:20 ET 2026-08-07 lockout SUPERSEDED the old "inactive banner is cosmetic" finding.
   Sessions start LOGGED OUT; S0 reactivated the account — confirm from its close-out.
3. NOTES: DOUBLE-ESCAPE FROM THE FIRST WRITE (`&amp;lt;`); verify byte-exact, never the panel.
4. DECISION NODES: use `NOT`, never a rebuild. No move-node control exists.
5. PICKERS NO-OP on the already-displayed value. Force with a two-step; verify the STORED field.
6. CLICKING: refs silently no-op; JS dispatch is harness-blocked. Compute from the DOM:
   scale = screenshotWidth / window.innerWidth, click at rect.centre × scale. Never carry a
   coordinate across a resize.
7. `Runtime.evaluate` times out at ~45s WITH THE WORK COMMITTED — re-read, never re-fire. Titles
   commit on BLUR. `overlay.innerText` goes stale mid-animation. Prefer `form_input`; re-read
   `.value`. Tags store lowercased with non-alphanumerics as spaces. `a5.bots.bot` is the hydrated
   client model.
8. `archiveBot` / `showBotMenu` are ANDY'S HAND. Three attempts, then STOP. Never coordinates.
9. TWO-LAYER EDIT PROOF. Layer 1 = re-observe after a HARD RELOAD. Layer 2 = the first NEW
   position's Trades list. ⛔ THE EXIT OPTIONS PANEL IS NEVER EVIDENCE — exits are copied onto the
   position at open, so the panel shows intent and the Trades list shows what was attached. In v1
   the panel displayed `PROFIT % 50%` while the bot generated NO exit orders at all for four
   months. This has no exception.
10. WHEN IT IS AMBIGUOUS, IT IS GATED.

=== THE STOP LADDER + HOW TO READ §4 ===
Documented method -> ONE documented alternative -> third attempt max -> STOP. No forcing, no
coordinate fallback, no improvised remedy.
  "bot stays OFF"   -> that bot does not trade today. THE REST OF THE FLEET PROCEEDS.
  "fleet stays OFF" -> NOTHING ELSE IS SWITCHED ON TODAY. Stop the sequence and escalate.
  a check you could not run -> ⬜ NOT EVALUABLE. Write it down BY NAME. It is never a pass, and it
  is never reported as a negative result.
⚠️ THE STEPS ARE IN DEPENDENCY ORDER. DO NOT REORDER THEM. Several exist only because something
later cannot be read until they have run.

=== ⛔ ANDY'S GATES INSIDE THIS SEQUENCE ===
A6 (Step 2)  — the ride-or-close call on the 5 open mirror positions: DRAFTED, SIGNED, AND EXECUTED.
               A logged call is not a disposition. Capital decision; go-live authority is Andy's.
A7 (Step 2b) — every pre-registration signature. "Andy signs and dates. Only then may the bot be
               switched ON."
A8 (Step 2b) — the three open signature items (see Step 2b below).
Ask for each explicitly and WAIT. Do not proceed past a gate on your own reading of it.

────────────────────────────────────────────────────────────────
STEP 0 — CLOSE THE PRE-DAY-0 CHECKLIST. NOTHING IN §4 STARTS UNTIL IT IS CLOSED.
────────────────────────────────────────────────────────────────
The checklist is at the foot of the runbook. Confirm EACH BOX BY READING THE ARTIFACT ITSELF, never
from a memory of a prior session and never from another document's claim about it.
⛔ IF ANY ⛔ HARD BLOCKER BOX IS UNTICKED -> DO NOT PAY, DO NOT RE-ARM. ESCALATE TO ANDY: YES.
Blocker classes: ⛔ HARD (§4 does not start) · ⚠️ PER-BOT (blocks only the bots it names) ·
📝 ADVISORY (proceed; log and carry as an open card).

Known state entering this session — VERIFY each, do not assume:
  ✅ `itmlive` = `market` — S0 Step 2. `itmpaper` was already `market`; do not re-set it.
  ✅ `data/mirror_baseline.csv` — written 2026-08-04, 10 rows / 174 positions. An ANCHOR: do not
     recompute it, do not pass `--force`.
  ✅ Pilot ritual complete + declared clean by Andy 2026-08-06; `rename_map.csv` started.
  ❓ `LEDGER_START` — Step 1 below.
  ❓ `data/raw/` + `data/brief/` pre-cutover files resolved — S0 reported them empty.
  ❓ `daily.sh` n=0 dry run — S0 asked Andy to run it. ⛔ HARD BLOCKER. Read the output against
     runbook §3 Step E's branches: a script that raises -> FIX THE SCRIPT, NEVER THE DATA, and
     NEVER seed a synthetic row to make it pass. `0.0%` expectancy / a flat R / a populated-looking
     table at n=0 is a FAILURE, not a pass — an absent number is not a zero. Tier C reporting
     SKIPPED because bots_config_v2.csv is incomplete is CORRECT — silence in its place is the
     failure. Do not set LESSONS_ALLOW_TRUNCATE=1 to make a shrink guard pass.
  ❓ ⛔ TEMPLATE V2 ON THE PILOT, with its AMENDED PR-03 signed. Ruled 2026-08-04, execution
     deferred as part of the ruling. Re-price the 15:50 Expiration exit OFF Market -> SmartPricing,
     internal value `speedy`, ⛔ NOT `fast` (a capture parser keying on "fast" silently misses it).
     THE 15:52 BACKSTOP KEEPS MARKET. This is a SPEC CHANGE, not a config tweak: it lands as
     Template V2 with an amended pre-registration, never as a quiet edit, and the amendment and the
     signature happen together. ⚠️ WITHOUT V2 THE THREE 15:50–15:52 MECHANICS ARE INDISTINGUISHABLE
     — three Market orders in two minutes with only memo strings between them (see Step 6).
  ❓ Sizing written down: 1 lot experiments · ≈$5K risk/position CANDIDATE+ · IDENTICAL allocation
     across tournament arms. SET ONCE, HERE. If it is not written down before Step 3 it will be set
     mid-sample.
  ❓ Ride-or-close prepared, signed, ready to EXECUTE — Step 2.
  ❓ Every pre-registration entry SIGNED — Step 2b.
  ❓ Phase 0: `C0c · C2 · C7 · C8` are CLOSED (decision card 2026-08-06). ⛔ `C9` is RE-SCOPED TO A
     DAY-0 PRE-SWITCH-ON READ and is still open. `C10` is open and blocks ARM-B1 — observed at
     Step 6b, not before. ⛔ C7 and C8 carry their own STOP; C8's verbatim: "Do NOT substitute
     position age — that is the literal substitution that cost −$15,376."
  ❓ ⛔ A7 BASELINES + A7 WIRED INTO `daily.sh`. The baselines ARE recorded in bots_config_v2.csv;
     A7 IS NOT WIRED INTO daily.sh (its eight stages carry execution_audit.py and no A-series
     runner). Under Architecture E the three automations are shared across seven bots, so one edit
     changes all seven at once with no template version bump and a mis-built gate fails IDENTICALLY
     on all seven — which the arms cannot detect by diffing each other. A7 IS THE ONLY DETECTOR.
     ⛔ No baseline and no detector before Day-0 = no detector for the whole sample. Report the
     gate state plainly to Andy; wiring it is Claude Code's lane, not yours.

────────────────────────────────────────────────────────────────
STEP 0a — `itmlive` = `market`. Already done in S0. VERIFY, do not re-do.
────────────────────────────────────────────────────────────────
Re-read `input.value` after a hard reload and confirm S0's screenshots are on file.
⛔ IF IT DID NOT PERSIST -> NO CAPITAL GOES LIVE. FLEET STAYS OFF. ESCALATE: YES.
⚠️ `market` is NOT a substitute for the 15:52 flat-close backstop — it reaches only EXPIRING ITM
positions on expiration day. Do not let the two be conflated later.

────────────────────────────────────────────────────────────────
STEP 1 — LEDGER_START
────────────────────────────────────────────────────────────────
S0 recorded the exact payment timestamp. THAT DATE IS `LEDGER_START`. Set it in
`scripts/build_ledger.py` before anything else, so no pre-cutover row can enter the working ledger.
⛔ VERIFY IT, DO NOT ASSUME IT. Run `build_ledger.py` once and confirm the row count is 0 and the
status reads EMPTY LEDGER, n=0. (`data/ledger_meta.json` currently reads
`"ledger_start": "2099-01-01"` — the refuse-everything sentinel, correct pre-Day-0 and NOT the
value to keep.)
⛔ IF THE LEDGER RETURNS ANY ROW -> a pre-cutover row has entered. STOP. NOTHING IS RE-ARMED. FLEET
STAYS OFF. ESCALATE: YES. Every downstream number would be cross-era.
⚠️ THE STRADDLE RULE: a position's era is its OPEN date. Pre-cutover positions resolve into the
MIRROR BASELINE layer, never the working ledger.

────────────────────────────────────────────────────────────────
STEP 2 — RIDE OR CLOSE, on the 5 open mirror positions. ⛔ ANDY'S GATE A6.
────────────────────────────────────────────────────────────────
`QQQ long call` ×4 (~$13K risk, ~−$10.8K unrealized) and `Tasty Condor` ×1 (~+$328), open at the
2026-07-30 capture and still open. An unmanaged legacy position is exactly the quiet exposure that
survives a clean-slate rebuild and then surprises someone.
⛔ THE DECISION IS NOT COMPLETE UNTIL IT IS EXECUTED AND RE-OBSERVED. A logged call is not a
disposition. Before Step 3 touches any toggle:
1. ⚠️ DRAFT AND SIGN THE LEDGER ENTRY FIRST. `pre-registration-ledger.md` §8 item 5 records that
   this entry "is not yet drafted" — THERE IS NO PLACE TO WRITE THE REASON UNTIL IT EXISTS.
2. CLOSE -> close the positions now, then re-read the TRADES LIST and confirm the closing rows are
   there. A save confirmation is not evidence.
3. RIDE -> the ride must survive Step 3. Turning EXIT OPTIONS ON for `QQQ long call` or
   `Tasty Condor` re-arms EVERY exit on that bot at once and CAN CLOSE A RIDDEN POSITION WITHIN
   MINUTES OF REACTIVATION. Before flipping either toggle, read that bot's Exit Options and record
   what would fire. If anything would act on the five positions against the decision, LEAVE THAT
   BOT'S EXIT OPTIONS OFF until the positions are closed or the exits are removed.
4. ⚠️ MIRROR FUNDING DOES NOT GATE THIS AND IS NOT DECIDED TODAY. ZERO OF TEN MIRRORS CLEARS THE
   EVIDENCE BAR AND NONE CAN BEFORE LATE OCT 2026. The Day-0 mirror action is RE-ARM, WATCH-ONLY,
   SIZE NOTHING. ⛔ Do not read "insufficient evidence" as "do nothing" — for a RUNNING bot that
   means CONTINUE, which is a capital decision made by default. SAY THE VERDICT OUT LOUD IN THE LOG.
⛔ IF THE CALL HAS NOT BEEN MADE, SIGNED AND EXECUTED FOR ALL FIVE -> DO NOT PROCEED TO STEP 3. NO
BOT IS RE-ARMED. ESCALATE: YES.

────────────────────────────────────────────────────────────────
STEP 2b — SIGNING. ⛔ ANDY'S GATES A7 + A8. NO TOGGLE IS TOUCHED UNTIL THIS IS COMPLETE.
────────────────────────────────────────────────────────────────
Run `pre-registration-ledger.md` §7's six-item checklist for EVERY BOT THAT WILL BE ON TODAY:
config hash from the bot's OWN capture file · every `<placeholder>` and `TBD` resolved · kill
criterion re-read against the daily loop (does the loop actually produce that number?) · max-loss
line filled · ANDY SIGNS AND DATES · verification artifact identified.

THE SIGNING SET — 20 plan bots plus the ride-or-close entry:
  Group B, 4 clones — ledger §4:
    PR-01 `IC-SPX-FastPT25-S2` · PR-02 `-130PM` · PR-03 `QQQ-IC-0DTE-Fortress` (pilot — ⛔ ITS
    AMENDED ENTRY AND ITS SIGNATURE HAPPEN TOGETHER, with Template V2) · PR-04 `-NoPT50`
  Group C, 9 untouched — ledger §5:
    PR-05 `DIR-SPX-PutVIX22-SL75` · PR-06 `DIR-SPX-CallVIXdrop` · PR-07…PR-13, the seven mirrors
    (3DTE $140-$350 · Nigiri-Paper-v1 · QQQ long call · Friday 14 DTE Broken Wing IB (B-70) ·
    Trendy-Paper-v1 · 60min-ORB-10W-Paper-v1 · Tasty Condor)
    ⛔ THE LEDGER NAMES THE NINE EXPLICITLY BECAUSE THEY ARE THE GROUP MOST LIKELY TO BE WAVED
    THROUGH AS "UNTOUCHED". A bot whose entry is unsigned stays OFF for the whole of Day-0. No
    exceptions, including the nine.
  Group D, 7 fresh — ⚠️ THEIR ENTRIES LIVE IN `greenfield-family-spec.md` §9, NOT in the ledger:
    PR-14 Ride (control) · PR-15 PT50 · PR-16 Trail · PR-17 Touch0 · PR-18 SL100 · PR-19 SL200 ·
    PR-20 Canary
  Plus the ride-or-close entry from Step 2.
  ⛔ NOT IN THE SIGNING SET: PR-21 / PR-22 (Track B) are DRAFT and unsigned, and ARM-B1 is not an
  arm until C10/C11 close. They are not switched on today. Do not sign them to be tidy.

⛔ THREE OPEN SIGNATURE ITEMS — ANDY'S GATE A8. Under §7 item 2 an entry with an unresolved field
is UNSIGNED, so each of these blocks a signature until it is ruled:

  (i) PR-16's TAIL RETIREMENT CRITERION — ruling slot G-12b.
      G-12 was ruled RESPEC (Andy, 2026-08-06): the worst-condor coin-flip test is STRUCK and the
      replacement was deliberately NOT invented by the applying session. ⛔ DO NOT INVENT ONE.
      `docs/post-u1-package-2026-08-07.md` §1 drafts it and §1.7 carries the EXACT ledger text
      ready to paste. Three constants need Andy's signature:
        S1  delta = 0.10 R per condor, on the tail set T   [ 0.10 | other ]
            ⚠️ A NEW MARGIN. The transport-from-R-3 argument was REFUTED in adversarial review and
            WITHDRAWN — delta carries no inherited authority and stands only on this signature.
        S2  p = 0.20 (tail fraction; m = ceil(p·n))         [ 0.20 | other ]
        S3  floor = n_matched_days >= 100, plus ONE re-arm at Day-0 + 9 months   [ as stated | other ]
      Plus: family membership [ INSIDE the family correction (recommended) | uncorrected one-sided
      5% ] and an acknowledgment of the standing publication cap.
      ⚠️ Until this is signed, the engine keeps emitting `worst_r_*` annotated `no_inference`.
      ⚠️ Whatever is ruled, the verdict carries `CF1_PUBLICATION_PRECONDITION: UNMET` while G-1 is
      on HOLD, and Refusal R-6 stands: no verdict while `pnl_may_be_modelled == true`.

  (ii) PR-18's NAME — "Breakeven", or not. Sandvand's rung is called Breakeven because stopping the
      tested spread at 100% of credit leaves the UNTESTED side to decay to zero, netting ≈$0 on the
      condor. The C8 ruling removed sibling-close, so the untested side IS left to decay and the
      construction objection is GONE — CF-4 is discharged and the arm CAN now reach Breakeven. The
      name is withheld PENDING ANDY'S READ OF HOW IT SHOULD BE PUBLISHED. The decision card records
      it explicitly as ANDY'S CALL AT DAY-0 SIGNING, not before. Ask; do not choose.

  (iii) G-1′ — `exit_rows.csv` under the degraded schema. U-1 came back NEGATIVE (Trades-list rows
      carry no per-row pricing-mode label and no memo field), so G-1 reverted to HOLD and the
      question re-presents. `post-u1-package-2026-08-07.md` §4: [ AUTHORIZE-DEGRADED | DECLINE |
      DEFER ], recommendation DECLINE plus two ~5-minute Day-0 checks — D3 (export timezone) and
      the Automation Log link's target. ⚠️ NO OPTION HERE MAKES CF-1's PUBLICATION PRECONDITION
      MEETABLE; the acknowledgment is part of the ruling.

⚠️ SIGNED ≠ VERIFIED. Signing does not satisfy Step 6.

────────────────────────────────────────────────────────────────
STEP 2c — ⭐ THE NO-TOUCH OBSERVATION. BEFORE ANY TOGGLE IS MOVED.
────────────────────────────────────────────────────────────────
⛔ THIS IS FREE AND THE INFORMATION IS NOT RECOVERABLE AFTERWARDS. Day-0 is itself an
inactive→active transition. If exits resume at reactivation with NO toggle intervention, BILLING
STATE IS IMPLICATED as the June cause. Flip a toggle first and re-arm is confounded with
reactivation — the toggle candidate and the billing candidate become PERMANENTLY
INDISTINGUISHABLE, and §1's causal story stays unfalsifiable forever.

OBSERVE: read BOTH dashboard toggles on ONE live mirror and ONE directional bot, and SCREENSHOT
BOTH. Andy's pre-Day-0 state is both toggles OFF on every bot, so the question is whether either
now reads ON without anyone touching it.
- EITHER READS ON WITHOUT INTERVENTION -> ⭐ BILLING STATE IS IMPLICATED. Log it as a first-hand
  observation with the screenshot filename and the timestamp, REPORT TO ANDY BEFORE PROCEEDING, and
  carry it into the Step 6a verdict. Do not re-flip anything first.
- BOTH READ OFF ON BOTH BOTS -> the toggle candidate survives. RECORD IT VERBATIM ANYWAY — a
  confirmed expectation is evidence and an unrecorded one is not. Proceed.
- UNREADABLE -> ⚠️ an unread toggle is not an OFF toggle. Re-screenshot. Still unreadable -> record
  `NO-TOUCH OBSERVATION UNREAD` and say so at close-out. PROCEED — this does not gate the sequence,
  but a missing answer is never reported as a negative one.
⚠️ Step 0a's ACCOUNT-LEVEL `itmlive` is NOT toggle intervention. Nothing else may touch a bot before
this observation. S0 and S1 were both instructed to leave the nine alone for exactly this reason —
confirm from their close-outs that they did.

────────────────────────────────────────────────────────────────
STEP 3 — RE-ARM SWEEP: `EXIT OPTIONS` ONLY. The nine leave-in-place bots.
────────────────────────────────────────────────────────────────
⛔ DO NOT TURN `AUTOMATIONS` ON IN THIS STEP. Re-arming and authorizing entries are two different
acts and Step 7 is the gate between them. `AUTOMATIONS` ON *IS* THE ENTRY AUTHORIZATION: a bot
switched on here takes a position before Step 6 can prove it — which is the v1 failure (−$9,618)
reproduced on Day-0, with Step 7 gating nothing.

THE NINE: `DIR-SPX-PutVIX22-SL75` · `DIR-SPX-CallVIXdrop` · `3DTE $140-$350` · `Nigiri-Paper-v1` ·
`QQQ long call` · `Friday 14 DTE Broken Wing IB (B-70)` · `Trendy-Paper-v1` ·
`60min-ORB-10W-Paper-v1` · `Tasty Condor`.
For each: EXIT OPTIONS -> ON · AUTOMATIONS LEFT OFF · then screenshot BOTH toggles.
Nothing else needs re-arming — clones and fresh builds were born correct and the ~20 Group-A bots
are being archived.

⛔ THE NINE ARE NOT EXEMPT FROM STEP 6. This step scopes RE-ARMING, not VERIFICATION. A pre-existing
bot is not a proven bot — these nine are the ONLY bots that lived through the lapse, which makes
them the MOST in need of the check, not the least.

BRANCHES:
- TOGGLE NOT PRESENT ON THE DASHBOARD -> try the TWO OTHER DOCUMENTED SURFACES first: inside the
  bot, and individually within each position. ⚠️ A SURFACE YOU DID NOT OPEN IS NOT AN ABSENT
  CONTROL. All three absent -> the lapse mechanism is UNEXPLAINED, not solved. BOT STAYS OFF · the
  other eight proceed · ESCALATE: YES.
- TOGGLE REVERTS TO OFF, or the post-save screenshot reads OFF -> re-drive it ONCE via the full
  pointer sequence. Reverts a second time -> BOT STAYS OFF · fleet proceeds · ESCALATE: YES.
  ⛔ No coordinate fallback. ⚠️ This revert branch is a DRAFTED remedy, not a corpus-cited one — no
  observation of a reverting toggle exists. RECORD WHAT ACTUALLY HAPPENS.
- THREE OR MORE OF THE NINE WILL NOT HOLD ON -> ⛔ STOP THE SWEEP. FLEET STAYS OFF. ESCALATE: YES.
  §1's mechanism is falsified and Day-0 is not a checklist day.
⚠️ THE TOGGLE HAS THREE DOCUMENTED SURFACES AND THIS STEP TOUCHES ONE. On any position that was
open THROUGH the lapse — the five from Step 2 — READ THAT POSITION'S OWN EXIT OPTIONS STATE before
acting on it. This has never been observed on those five: it is an UNOPENED SCREEN, not a
known-good one.

────────────────────────────────────────────────────────────────
STEP 4 — CONFIRM THE BUILD WINDOW IS COMPLETE
────────────────────────────────────────────────────────────────
Every clone and fresh build has: a capture on file · a saved template AT ITS CURRENT RULED VERSION
(⚠️ THE PILOT REQUIRES V2, NOT V1) · a signed pre-registration entry · a `rename_map.csv` row.
Anything missing is finished now or ITS BOT STAYS OFF.
PLUS the two gates the four artifacts do not satisfy:
  (a) Phase 0 blocking checks CLOSED. C0c · C2 · C7 · C8 are closed; ⛔ C9 is still open as a Day-0
      pre-switch-on read. ⛔ IF ANY IS STILL UNANSWERED, THE FAMILY DOES NOT TRADE TODAY — those
      bots stay OFF and the checks are run AS READS, NEVER WRITES, before switch-on. DO NOT
      IMPROVISE A SPEC ON THE FLY. Fleet proceeds. Escalate: YES.
  (b) A7 payload-hash baselines RECORDED and A7 WIRED INTO `daily.sh`. Baselines: recorded. Wiring:
      NOT DONE (see Step 0). ⛔ No detector before Day-0 = no detector for the whole sample.
      Report the state; the wiring is Claude Code's lane. Andy rules whether the family trades
      today without a nightly A7.

────────────────────────────────────────────────────────────────
STEP 5 — CAPTURE EVERYTHING, AND RESOLVE THE INPUT CHAIN
────────────────────────────────────────────────────────────────
Full bookmarklet sweep of /bots across the whole new roster, plus toggle screenshots.
⚠️ A /bots SWEEP IS NOT `bots_config_v2.csv`. It carries names and P/L and NO Exit Options values.
That file is written PER-BOT AS EACH BOT IS BUILT. Step 5 VERIFIES its rows are present and
current; it does not create them.
⛔ THE D-1 G2 RIDER APPLIES HERE, TWO HOPS DEEP. The saved action stores a REFERENCE, NOT VALUES:
`{"type":"input","input":"IN…","text":"<label>","oldValue":{…}}`. Every capture, capture-diff and
drift baseline must resolve action -> automation input -> BOT input and read THE INPUT OBJECT'S
VALUE. A CAPTURE THAT READS ONLY THE ACTION RECORDS THE INPUT'S NAME, SO EVERY ARM DIFFS AS
IDENTICAL AND THE TOURNAMENT IS UNDETECTABLY VOID. ⚠️ NEVER read `oldValue` as current config — it
is a stale pre-link snapshot. The control lives at: bot settings page -> the automation row's ⚙ Edit
Settings -> 🔗 -> `Bot Inputs`.
⛔ IF THE INPUT OBJECT'S VALUE CANNOT BE READ -> THE CAPTURE IS NOT A BASELINE. Do NOT record it as
one and do NOT fall back to `oldValue`. Mark those bots' config-capture hash NOT ESTABLISHED; their
entries CANNOT BE SIGNED. Those bots stay OFF · the rest of the fleet proceeds · escalate: YES.
⛔ ALSO CAPTURE /settings SEPARATELY — SEVEN ACCOUNT-LEVEL FIELDS THAT ARE IN NO /bots CAPTURE AND
OVERRIDE EVERY BOT: `itmlive` · `itmpaper` · `maxexits` · `scanstart` · `scanend` · `exitstart` ·
`exitend`. ⛔ `maxexits` is the dangerous one — a single switch that can cap EVERY bot's ability to
close, and a non-zero value reproduces the exact failure shape of the June lapse with nothing
per-bot to show for it. It read `0` = Unlimited on 2026-08-04 and again in S0. RECORD THE VALUE AND
MAKE IT A DRIFT-AUDIT ROW.
⛔ IF `Export Data` IS TAKEN WITH ANY BOT GROUP DESELECTED -> DISCARD IT. The export respects the
bot-group filter and a subset export rebuilds the ledger as a subset. Re-export with ALL GROUPS
SELECTED.
THEN CONFIRM THE COMPARATOR IS REAL: open one arm's row and one shared-object row and read the
DECODED BUNDLE and the A7 hash back. IF EITHER IS MISSING, the drift detector's Tier C is SKIPPED
and the daily loop runs config-blind — SAY SO IN THE BRIEF rather than reporting a green baseline.

────────────────────────────────────────────────────────────────
STEP 5a — ⛔ DST CHECK: does `ntime=1552` actually fire at 15:52 ET? (D3)
────────────────────────────────────────────────────────────────
WHY THIS IS A HARD GATE: one toggle kills every Exit Option on a bot at once, which is exactly why
the flat close lives in the Events class. IF IT FIRES AT 16:52 ET, THE FLEET HAS NO LAST-RESORT FLAT
CLOSE AT ALL — the single point of failure the design was built to remove.
The saved trigger serialises `startDate …T20:52:00.000Z` — 15:52 at UTC−5 (EST) but 16:52 ET in
August (EDT). It reproduces on ALL SIX arms (`2026-08-07T20:52:00.000Z`) and on PR-14. `ntime` is
the operative field and `startDate`'s time component may be a stamp only. NOBODY HAS OBSERVED WHICH.
DO NOT ASSUME.
OBSERVE, on the pilot's backstop automation, on the FIRST TRADING DAY THE BOT IS ON: bot Log tab ->
filter Type = `Event` -> find the backstop's run row -> read THAT ROW'S `title` ATTRIBUTE, NOT the
visible group header (the group header is unreliable; the `title` carries a year-bearing timestamp).
- `title` reads between 3:52PM and 3:56PM -> `ntime` is operative. ✅ DST CLOSED. Record the verbatim
  `title` string and the date. Proceed. (A minute or two of drift is expected — automations run on a
  distributed queue with no guaranteed slot.)
- `title` reads `4:5xPM`, OR THERE IS NO EVENT ROW FOR THE BACKSTOP THAT DAY -> ⛔ THE BACKSTOP IS
  DEAD UNDER DST. STOP. Every bot carrying it is now single-layer. ⛔ DO NOT RE-TIME THE TRIGGER
  YOURSELF — the minute is in build-plan.md §2B and §0 says do not improvise a change here on the
  day. Then: (1) set every affected bot's toggles OFF and record it; (2) emit an instruction card
  headed `DST-BACKSTOP-DEAD` naming every affected bot; (3) hand to Andy for an explicit "amend the
  plan". ENTRIES STAY BLOCKED FOR THOSE BOTS UNTIL ANDY RULES.
- LOG FILTER RETURNS NOTHING READABLE (chips render labels via CSS, so `innerText` on the filters is
  the empty string) -> ⚠️ DO NOT CONCLUDE "NO ROWS". Read the hidden inputs named `date`, `time`,
  `autotypes` directly, or take it to Andy as UNREAD. ⛔ AN UNREAD DST CHECK IS TREATED AS THE
  FAILURE BRANCH — those bots stay OFF.
⚠️ RE-RUN THIS EXACT CHECK on the first trading day after the November EST transition, whichever way
it resolves now.

────────────────────────────────────────────────────────────────
STEP 6 — ORDER-LEVEL VERIFICATION, PER BOT, BEFORE IT MAY TRADE
────────────────────────────────────────────────────────────────
Two acceptable proofs, in order of preference: BUTTON TEST-FIRE then read the resulting TRADES LIST;
or allow the bot ONE position — the first-position exception — and read it the moment it opens.
⚠️ THE FIRST-POSITION EXCEPTION, stated plainly because Steps 6 and 7 are otherwise circular: the
Trades list is the only order-level ground truth AND IT DOES NOT EXIST UNTIL A POSITION DOES. If the
test-fire is unavailable, the bot is allowed EXACTLY ONE position at 1 LOT, read the moment it opens.
The test-fire prohibition elsewhere is scoped to the INACTIVE-ACCOUNT BUILD WINDOW, not to Day-0.
⛔ THE EXIT OPTIONS PANEL IS NOT EVIDENCE. Exit Options are copied per-position at open; the panel
shows intent, the Trades list shows what was attached.

FOR THE TWO CONTROL CLONES (PR-01 `IC-SPX-FastPT25-S2`, PR-02 `-130PM`) THE CHECK IS INVERTED:
confirm their Trades lists show NO PT row and NO exit-trigger row, and that their S2 monitor IS
firing.
⚠️ THE INVERTED CHECK IS ADVISORY UNTIL D4 IS ANSWERED. Whether the account-level ITM action appears
in a Trades list, AND UNDER WHAT LABEL, IS UNOBSERVED. Until it is read, a mislabelled ITM close
READS AS A PT ROW and would kill a ride control on day one — taking the referent of every comparison
in the family with it. READ THE LABEL FIRST; FIRE THE RULE SECOND.
⚠️ AND: the inverted check only means anything if F-C1 was applied. If PT25 is still in either
control's Open actions, THE CHECK FAILS BY CONSTRUCTION — that is a known state, not a finding.
Confirm from S0's and S1's close-outs which applies.

BRANCHES:
- NO PT ROW AND/OR NO EXIT-TRIGGER ROW -> BOT STAYS OFF. Record as MECHANICS 🔴 RED with the
  trade_id. Then, in order: (a) re-observe both dashboard toggles by a FRESH screenshot; (b) re-read
  the Open Position action's Exit Options VALUES, NOT PRESENCE; (c) re-drive the toggle once. Fleet
  proceeds. Escalate: YES if it fails a second position.
- NO POSITION OPENS AT ALL -> ⬜ NOT EVALUABLE, WHICH IS NEVER A PASS. Bot stays OFF. Carry the open
  card forward.
- THREE OR MORE BOTS SHOW THE SAME MISSING ROW -> ⛔ STOP. FLEET STAYS OFF. ESCALATE: YES. This is
  the v1 failure repeating, not a per-bot defect.
- TEST-FIRE UNAVAILABLE OR UNREADABLE -> fall back to the first-position exception. ⛔ NEVER
  SUBSTITUTE THE EXIT OPTIONS PANEL. NO EXCEPTION.
- ⛔ THE INVERTED CHECK'S OWN BRANCH — AND THE GENERIC ONE IS THE WRONG ACTION HERE. If either
  control clone's Trades list shows a PT row or an exit-trigger row, THE RIDE+S2 CONTROL IS
  CONTAMINATED and the arm's comparison is VOID, NOT DELAYED. ⛔ DO NOT EDIT THE BOT TO REMOVE IT —
  CLAUDE.md §5 standing exception: "Do not 'fix' them, do not re-arm them." Capture the Trades list,
  screenshot the Open Position action. BOT STAYS OFF · fleet proceeds · ESCALATE: YES.
  If the S2 monitor shows NO firing -> BOT STAYS OFF · fleet proceeds · escalate: YES. Zero log rows
  is the liveness RED of Step 8. ⛔ DO NOT READ MONITOR SILENCE AS "RIDE BEHAVIOR INTACT."

⚠️ THREE MECHANICS NOW AIM AT THE SAME TWO MINUTES — ATTRIBUTE BEFORE YOU CONCLUDE. `itmpaper` =
`market` closes expiring ITM positions 10 minutes before the close = 15:50, THE SAME INSTANT as the
bot's own Expiration exit and two minutes before the 15:52 backstop. AN EXIT-OPTION ORDER STAYS LIVE
TWO MINUTES, so the 15:50 order is still working when the backstop fires. RECORD BOTH ROWS'
TIMESTAMPS AND ATTRIBUTE BY THE GAP, NOT THE ABSOLUTE MINUTE — automations run on a distributed
queue and the clock is jittered. Feed `time_exit` and `itm_action` to the detector as SEPARATE
config columns. ⚠️ After Template V2 lands the three are distinguishable BY PRICING — 15:50
Expiration on SmartPricing (`speedy`), ITM action Market, backstop Market-with-memo. WITHOUT V2 THEY
ARE THREE MARKET ORDERS IN TWO MINUTES WITH ONLY MEMO STRINGS BETWEEN THEM.

────────────────────────────────────────────────────────────────
STEP 6a — ⛔ MECHANISM VERDICT (D4). THIS IS THE STEP THAT SETTLES §1.
────────────────────────────────────────────────────────────────
Run ONCE, on THE NINE leave-in-place bots ONLY — the clones and fresh builds were never lapsed and
cannot test it. PRECONDITION: Step 3 done AND the bot has opened its first new position. Do not run
it earlier.
⚠️ WHAT IS AND IS NOT ESTABLISHED, going in: the toggle's EXISTENCE is documented + first-hand ×2.
The CAUSAL claim — that flipping it back ON re-arms exit-order generation, and that its being OFF is
what killed the June exits — is NOT ESTABLISHED. The independently ruled position is D-4: THE JUNE
CAUSE IS UNKNOWN. The Excessive Errors Failsafe is excluded as the June cause (zero June errors on
either Fortress bot; newest error Apr 16 2026 3:55PM) but the mechanism itself is real.

- TOGGLES READ ON *AND* THE TRADES LIST CONTAINS THE PT ROW AND THE EXIT-TRIGGER ROW ->
  ✅ MECHANISM CONFIRMED. Record per bot: name, screenshot filename, VERBATIM PT row text, date.
  Write the verdict into docs/state.md and retire the CAUSAL caveat BY CITING THIS OBSERVATION.
- TOGGLES READ ON *AND* THE TRADES LIST SHOWS NO PT ROW -> ⛔ MECHANISM REFUTED. FULL STOP — THIS IS
  NOT A PER-BOT PROBLEM. The Failsafe moves back into contention and the June cause is again UNKNOWN.
  Do ALL of the following before anything else:
    1. AUTOMATIONS OFF ON ALL NINE, screenshotted. Do not leave a bot opening positions it cannot
       exit.
    2. ⛔ DO NOT ALLOW ENTRIES ON THE CLONES OR FRESH BUILDS EITHER. They were built on the premise
       that a correct-from-birth exit stack cannot suffer this failure. THAT PREMISE IS NOW
       UNPROVEN. FLEET STAYS OFF.
    3. Check the competing mechanisms, IN ORDER, recording each answer verbatim: (a) bot Log ->
       `Errors` filter, read each row's `title` — any day at or above 10 ERRORS since re-arm?
       (b) /settings -> `maxexits` still 0/Unlimited? (c) /settings -> Bot Schedule
       `exitstart`/`exitend` — do the window bounds still admit the exit's stamped minute?
       (d) Bid-Ask Guard — was the spread wide at the stamped minute?
    4. Emit an instruction card headed `LAPSE-MECHANISM-REFUTED`, repeated at the top of every brief
       until closed, and hand to Andy. ⛔ DO NOT DIAGNOSE PAST THIS POINT AND DO NOT RE-ARM ANYTHING.
       The cause is a research question, not a Day-0 step.
- NO POSITION HAS OPENED YET ON A BOT -> that bot is UNTESTED, NOT PASSING. ⬜ Do not count an
  untested bot as a confirmation.
- TOGGLE STATE UNREADABLE -> ⚠️ absence of a readable toggle is not an observation. Re-screenshot;
  still unreadable -> that bot is UNTESTED and STAYS OFF.
⚠️ FEED STEP 2c's RESULT INTO THIS VERDICT. If a toggle read ON without intervention at Step 2c, then
re-arm and reactivation were NEVER CLEANLY SEPARATED for that bot, and a CONFIRMED verdict on it is
WEAKER THAN IT LOOKS. SAY SO.

────────────────────────────────────────────────────────────────
STEP 6b — 📝 C10 OBSERVATION: the unit of `dstop` (Stop Loss $)
────────────────────────────────────────────────────────────────
AN OBSERVATION, NOT A BUILD. Nothing is re-stamped on Day-0 either way — Andy re-stamps PR-21.
⛔ WHY IT NEEDS ITS OWN STEP: C10 cannot be read off the modal. It is headed `Stop Loss Amount`, the
only unit marker is a bare `$`, `step=1`, and there is NO per-contract / per-position / per-leg
qualifier anywhere on it. It needs a LIVE POSITION WHOSE CONTRACT COUNT YOU WROTE DOWN BEFORE IT
OPENED. THAT MOMENT EXISTS EXACTLY ONCE. DO NOT LET IT PASS UNRECORDED.
SET UP: the 1-lot canary (PR-20) IS THE C10 INSTRUMENT — run it, and run it at EXACTLY 1 CONTRACT.
On the canary ONLY, set `dstop` to a round, unmistakable value (e.g. −100) and RECORD, BEFORE THE
POSITION OPENS: bot name, `dstop` as typed, and CONTRACT COUNT PER LEG.
- FIRED AT ≈ −$100 TOTAL ON THE POSITION -> PER POSITION. `<D100>` as specified by R-1 "in dollars"
  is on the correct basis; the PR-21 re-stamp is a formality. ✅ C10 CLOSED.
- FIRED AT ≈ −$100 × (CONTRACT COUNT) -> PER CONTRACT. ⛔ This is the D-6 units failure one layer up.
  (1) Emit a card headed `C10-PER-CONTRACT`; (2) state plainly that `<D100>` is off by the contract
  count and ARM-B1 MUST NOT BE BUILT until Andy re-derives the rung and re-stamps PR-21;
  (3) ⛔ DO NOT RE-DERIVE `<D100>` YOURSELF — the rung basis is signed ruling R-1 and changing it is
  a plan amendment. C10 CLOSED, ARM-B1 STILL BLOCKED.
- FIRED AT NEITHER FIGURE -> record realised P/L, contract count and leg count; report
  `C10-UNRESOLVED`. ARM-B1 stays blocked. DO NOT FIT A BASIS TO ONE DATA POINT.
- CANARY NOT RUN / STOP NEVER FIRES / COUNT NOT RECORDED FIRST -> ⚠️ C10 STAYS OPEN. SAY SO in
  docs/state.md and at close-out. ⛔ DO NOT INFER THE UNIT FROM `dstop` PERSISTING AS A NEGATIVE
  NUMBER — that is a sign convention and it is INADMISSIBLE as the answer.

⛔ ALSO DUE HERE, and it is easy to lose: TIER-2 CHECK §9 #5 is the last open item from the
2026-08-04 Tier-2 pass (seven of eight answered). Read it, record the answer verbatim, and if it
cannot be run say NOT EVALUABLE by name.

────────────────────────────────────────────────────────────────
STEP 7 — ONLY NOW ALLOW ENTRIES: `AUTOMATIONS` -> ON, PER BOT
────────────────────────────────────────────────────────────────
HARD GATE, NOT A PREFERENCE. A bot that cannot be proven stays OFF until it can.
FOR EACH BOT THAT PASSED STEP 6 — AND ONLY THOSE — set AUTOMATIONS -> ON and SCREENSHOT.
A BOT THAT DID NOT PASS STEP 6 DOES NOT GET THIS STEP, INCLUDING ANY OF THE NINE.
⛔ IF STEP 6a RETURNED MECHANISM REFUTED, NO BOT GETS THIS STEP. FLEET STAYS OFF.
⛔ A BOT WHOSE PRE-REGISTRATION IS UNSIGNED DOES NOT GET THIS STEP EITHER.
⚠️ THE STANDING EXCEPTION: the legacy champion (`IC-SPX-FastPT25-S2`) and its `-130PM` clone are
deliberately Exit-Option-free ride+S2 controls. Do not "fix" them and do not re-arm them.

────────────────────────────────────────────────────────────────
STEP 8 — DAY-1 MONITORING
────────────────────────────────────────────────────────────────
LIVENESS: every ON bot must show a position OR a scanner run in the capture window. OA bot logs
record NON-ACTIONS, so ZERO LOG ENTRIES = presumed OFF or Failsafe-tripped -> RED.
SAME-DAY ENGINE-DEATH CHECKS: the expired:closed ratio flip, and any position with `mfe_pct` ≥ its
declared PT and NO PT order.
⛔ WHAT RED DOES — A CARD IS A QUESTION, NOT AN ACTION. An instruction card is a notification with an
address. It is NOT a disposition. Each RED also carries one:
- ZERO LOG ENTRIES FOR AN ON BOT IN THE CAPTURE WINDOW -> the bot is SWITCHED OFF pending
  investigation (PR-05's liveness kill). Fleet proceeds. Escalate: NO on day 1; YES if unresolved
  after two sessions. ⚠️ DISTINGUISH THE WINDOWS: PR-05's KILL criterion is a 10-SESSION window;
  this Day-1 check is ONE capture window and switches the bot off TO BE RE-ARMED — it does not
  retire the bot. ⚠️ `SILENT_BOT` CAN NEVER BE RED FROM POSITION DATA ALONE — only the bot log
  closes it. If the log cannot be read the verdict is ⬜ NOT EVALUABLE, NEVER GREEN.
- `mfe_pct` ≥ DECLARED PT WITH NO PT ORDER, or the expired:closed ratio flips -> BOT STAYS OFF FROM
  THE NEXT SESSION until a Trades list proves the PT row exists. Fleet proceeds. Escalate: YES —
  this is the exact 2026-06 signature.
- `BACKSTOP_CAUGHT_IT` FIRES -> the Exit-Options side is dead even though nothing was lost that day.
  BOT STAYS OFF. Escalate: YES.
Any RED emits an instruction card, repeated at the top of every brief until closed.
⚠️ ASSERTS A4b AND A6 BECOME RUNNABLE TODAY and belong here: A4b (no arm shows a ledger day of
stop-outs within minutes of open with no `stoploss` in its config — the broken-input-link signature)
and A6 (every arm opened EXACTLY 1 contract per leg today — the $-risk sizing fallback silently
sizing 2 lots, and doing it on SOME arms only). Run both. Report the result.

=== CLOSE-OUT (CLAUDE.md §9.1 — mandatory, AFTER EACH STEP GROUP, not once at the end) ===
1. Append docs/session-log.md; update docs/state.md for every fact that changed — and the Step 6a
   verdict goes into state.md BY NAME whichever way it lands. Verify every edited file by direct
   `device_bash` sha256 + a single-match grep.
2. Update the `bot-fleet-migration` tracker via `update_artifact`; ASK ANDY TO VISUALLY CONFIRM.
3. "Ready to commit" + the changed-files list. DO NOT COMMIT.
4. ⛔ THE FIVE DEFERRED OBSERVATIONS, EACH REPORTED BY NAME WITH ITS ANSWER OR AS OPEN:
   no-touch (2c) · DST (5a) · the 15:50 attribution (6) · mechanism verdict (6a) · C10 `dstop` (6b).
   Plus Tier-2 §9 #5. ANY ONE LEFT UNREAD IS REPORTED AS OPEN, NEVER AS PASSED.
5. A per-bot ON/OFF table: every bot, its Step 6 verdict, its signature status, and — for every bot
   that is OFF — the named reason and what would close it.
```

---

## S3 — CLOSE-DOWN

**Model: Sonnet.** Records, tracker, hand-off. The one judgment call — whether an archive is safe —
is resolved by handing every archive click to Andy.
**Andy attended: yes, for gate A5** (the ~23 archive clicks) **and A10/A11.**

```text
You are working in bot-fleet-v2 (~/bot-fleet-v2 via the device bridge). Day-0's sequence has run
(S0, S1, S2). This is the CLOSE-DOWN session. Its job is to leave the folder in a state Andy can
commit in one command, get the ~23 archives done under Andy's hand, and hand Day-1 forward.

⛔ THIS SESSION MAKES NO SPEC DECISION AND NO OA CONFIG EDIT. If you find something that wants
changing, record it and gate it.

READ FIRST, FRESH:
  docs/day0-session-pack-2026-08-07.md   §0, §1
  docs/session-log.md                     the S0, S1 and S2 entries, in full
  docs/state.md                           the Day-0 blocks S2 wrote
  docs/reactivation-runbook.md            §3 Step B (the sweep + its name-collision warning), §4
                                          Step 8, and the Pre-Day-0 checklist
  docs/build-plan.md                      §2 group A (the 20) and §2B (the 4 clone originals)
  docs/daily-loop-spec.md                 the three-verdict contract — Day-1 runs on it
  data/archive/rename_map.csv             every lineage row written so far

=== STANDING FACTS — TRUE ALL SESSION ===
[Identical to S0's block. Reproduced verbatim so this prompt is self-contained.]
1. NEVER RUN GIT, in any form, INCLUDING `git status`. The bridge cannot unlink; git from this side
   strands .git/index.lock and Andy removes it by hand. Verify files by direct `device_bash` sha256
   + a single-match grep. Never the write tool's response, never a stage-back read. ANDY RUNS EVERY
   COMMIT — and on this session that is the whole deliverable.
2. The ~04:20 ET 2026-08-07 lockout superseded the old banner finding; sessions start LOGGED OUT.
3. NOTES: DOUBLE-ESCAPE FROM THE FIRST WRITE; verify byte-exact, never the panel.
4. DECISION NODES: use `NOT`, never a rebuild.
5. PICKERS NO-OP on the already-displayed value; force with a two-step; verify the STORED field.
6. CLICKING: refs no-op; JS dispatch is harness-blocked. scale = screenshotWidth / innerWidth,
   click at rect.centre × scale. Never carry a coordinate across a resize.
7. `Runtime.evaluate` times out at ~45s WITH THE WORK COMMITTED — re-read, never re-fire.
8. ⛔ `archiveBot` IS ANDY'S HAND — 3-for-3 failed from this side, and this session is where that
   bites hardest. Three attempts, then STOP. ⛔ NEVER FALL BACK TO COORDINATES: `Delete` sits ~29px
   below `Archive`, and on the pilot's original a mis-landed click would have destroyed 41
   POSITIONS OF HISTORY.
9. TWO-LAYER EDIT PROOF; the Exit Options panel is never evidence.
10. WHEN IT IS AMBIGUOUS, IT IS GATED.

=== THE STOP LADDER ===
Documented method -> ONE documented alternative -> third attempt max -> STOP. No forcing, no
coordinate fallback, no improvised remedy. Record verbatim and escalate.

────────────────────────────────────────────────────────────────
TASK 1 — SUPPORT THE ARCHIVE SWEEP. ⛔ ANDY'S GATE A5. EVERY CLICK IS HIS.
────────────────────────────────────────────────────────────────
~23 archives: the 20 Group-A bots plus the 3 clone originals whose clones now hold the production
names (the pilot's original was archived 2026-08-04 and is already done).
YOUR JOB IS TO MAKE HIS CLICKS SAFE, NOT TO CLICK. For each, present: the EXACT full name, its bot
ID, and a one-line confirmation of what it is. Then read `/bots` back after each batch and confirm
the active-bot footer decremented by exactly the number archived.

THE 20 (build-plan.md §2A): `IC-SPX-Fortress-Unstopped` · `IC-SPX-Fortress-Defang` ·
`QQQ-IC-0DTE-Fortress-NoFilter` · `QQQ-IC-0DTE-Fortress-S2` · `QQQ-IC-0DTE-HedgeA-S1` ·
`-HedgeB-S2` · `-HedgeC-S3` · `-HedgeD-Conditional` · `-HedgeTest` · `QQQ-IC-0DTE-Baseline` ·
`-Raw-HoldToExp` · `-InverseFilter-HoldToExp` · `-VIX25-Range075-PT50` · `-Range075-PT50` ·
`-Range075-PT50-Wide2-155PM` · `-Range075-PT50-Wide2-1230PM` · `Weekly-IB-SPY-Paper-v1` ·
`1-45pm-Sandwich-Paper-v1` · `Opening Range Breakout 60m` · `DIR-SPX-Put-Control`.
THE 3 CLONE ORIGINALS: `IC-SPX-FastPT25-S2-ARCHIVED-2026-08-07` and the two S1 renamed this Day-0.

⛔ NAME-COLLISION WARNING — READ FULL NAMES BEFORE ANY ARCHIVE. `Opening Range Breakout 60m` IS
ARCHIVED. `60min-ORB-10W-Paper-v1` IS A DIFFERENT BOT AND STAYS LIVE — it is one of the nine.
⛔ `DIR-SPX-PutVIX22-SL75` IS ZERO-TRADE AND MUST NOT BE TOUCHED. Its VIX≥22 gate correctly never
fired in 22 days. EMPTY ≠ WORTHLESS, and it is in the leave-in-place group.
⛔ DELETE NOTHING. The two deletes (`TEST QQQ-IC-0DTE-HedgeC-S3 Clone`,
`QQQ-IC-0DTE-InvFilter-Wide150`) and the Library object `CLAUDE-C5-SHARED-SCRATCH` were all
executed 2026-08-06. There is nothing left to delete. If something looks like it needs deleting,
that is a finding, not a task.
VERIFY READ-ONLY afterwards, per bot: active-bot footer decremented by one · exactly one bot under
the production name · the `-ARCHIVED-` name no longer listed.
APPEND `data/archive/rename_map.csv` as you go — original_name, archived_as, clone_name, date,
disposition. It is the ONLY thing that will later connect a name in the frozen ledger to a bot
running today.
⛔ IF ANY ARCHIVE WILL NOT FIRE FROM ANDY'S CLICKS EITHER -> record it, leave the bot renamed, and
carry it forward. An un-archived renamed original is untidy; it is not a blocker. Renames are what
free the production names and they already committed.

────────────────────────────────────────────────────────────────
TASK 2 — THE RECORDS
────────────────────────────────────────────────────────────────
a. `data/bots_config_v2.csv` — one row per bot and per shared object, each citing its own capture
   file and hash. ⚠️ It is written PER-BOT AS EACH BOT IS BUILT, not as a big-bang extraction; this
   task VERIFIES completeness and currency. ⛔ Every row's config-capture hash must resolve the
   input chain two hops (action -> automation input -> BOT input, reading the INPUT OBJECT'S VALUE).
   A row whose hash is NOT ESTABLISHED must say so — its bot could not have been signed.
b. `data/archive/rename_map.csv` — complete for all four clones plus every Group-A archive.
c. `docs/state.md` — the Day-0 facts, current. Specifically: the roster after archiving, the Step 6a
   mechanism verdict, the DST verdict, the C10 verdict, `LEDGER_START`, `itmlive`, the seven
   account-level fields, and which bots are ON.
d. `docs/session-log.md` — a Day-0 entry per session, already appended by S0/S1/S2. Add the
   close-down entry.
e. ⛔ THE OPEN-ITEMS LIST, BY NAME. Everything still open at the end of Day-0: every bot that is OFF
   and why · every ⬜ NOT EVALUABLE check · the five deferred observations and Tier-2 §9 #5 with
   their verdicts or OPEN · the A7-not-wired-into-daily.sh gate · G-12b / PR-18 naming / G-1′ if
   any went unruled · Track B (PR-21/22 unsigned, ARM-B1 blocked on C10) · the post-downgrade
   backlog. ⛔ AN ABSENT NUMBER IS NOT A ZERO AND AN UNRUN CHECK IS NOT A PASS.
VERIFY EVERY EDITED FILE by direct `device_bash` sha256 + a single-match grep of the new text.

────────────────────────────────────────────────────────────────
TASK 3 — THE TRACKER. ⛔ ANDY'S GATE A10.
────────────────────────────────────────────────────────────────
Update the `bot-fleet-migration` tracker artifact via `update_artifact` so it matches the folder,
then ASK ANDY TO VISUALLY CONFIRM IT. ⛔ THE CLOSE-OUT IS NOT COMPLETE WITHOUT HIS CONFIRMATION —
`update_artifact` returning success is a claim, not evidence (CLAUDE.md §9.1a). This rule has failed
twice (7/29, 7/31). THE TRACKER IS THE ONE DASHBOARD ANDY READS; when it lags the folder it reports
finished work as missing and invites it to be done twice.

────────────────────────────────────────────────────────────────
TASK 4 — THE COMMIT HAND-OFF. ⛔ ANDY'S GATE A11.
────────────────────────────────────────────────────────────────
Say "READY TO COMMIT" with a one-line summary of every changed file. ⛔ DO NOT COMMIT — the bridge
cannot unlink files and git from this side strands lock files in `.git/`.
UNCOMMITTED WORK AT SESSION END IS UNFINISHED WORK. The folder is the only memory this project has;
an untracked folder cannot be diffed, reverted or trusted. Leave the tree in a state Andy can commit
in ONE command, and say so plainly.
⚠️ CHECK FOR THE PRE-DAY-0 STRAGGLERS TOO: as of 2026-08-07,
`docs/decision-card-2026-08-06.md` was modified and
`data/captures/2026-08-06-gfam/GF-Backstop-1552-FlatClose.txt` untracked. If they are still
uncommitted, name them.

────────────────────────────────────────────────────────────────
TASK 5 — HAND DAY-1 FORWARD
────────────────────────────────────────────────────────────────
Write the Day-1 opening note into the session log:
- WHICH BOTS ARE ON, by name, with each one's Step 6 verdict.
- THE DAILY LOOP resumes per `docs/daily-loop-spec.md`: capture (bookmarklet on /bots + Export Data,
  ⛔ ALL GROUPS SELECTED) -> `daily.sh` -> ledger -> tape -> DRIFT AUDIT -> the three verdicts,
  NEVER BLENDED -> an instruction card for any RED. NO FINDINGS is the expected common case.
- EVERY OPEN INSTRUCTION CARD, repeated at the top of every brief until closed.
- THE STEP 8 CHECKS that run tomorrow: liveness · expired:closed ratio flip · `mfe_pct` ≥ declared
  PT with no PT order · asserts A4b and A6.
- ⚠️ RE-RUN THE STEP 5a DST CHECK on the first trading day after the November EST transition,
  whichever way it resolved today.
- ⚠️ THE FIRST POST-CUTOVER TRADING DAY is when `STATUS.md` stops reading EMPTY LEDGER — n=0. Until
  then, an absent number is not a zero.

=== CLOSE-OUT ===
Same §9.1 sequence: session-log + state.md (sha-verified) -> tracker + Andy's visual confirmation ->
"ready to commit" + changed-files list. DO NOT COMMIT.
```

---

# §3 · SEQUENCING AND MODEL SUMMARY

| Session | Model | Andy attended | Runbook coverage | Ends when |
|---|---|---|---|---|
| **S0** Reactivation opening | **Sonnet** | Yes — A1, A2, A3, A4, A9 | Step 0a; Step 1's timestamp; §3 Step B roster; the A-series | Roster + A-series accepted, F-C1 applied, PR-01 finished |
| **S1** Clones | **Sonnet** | No, unless a branch fires | §2's nine steps ×2 (PR-02, PR-04) | Both clones built and verified, or stopped with a named branch |
| **S2** The sequence | **Opus** | **Yes, throughout** — A6, A7, A8 | §4 Steps 0 → 8, in order | Step 7 done per bot, Step 8 queued for Day-1 |
| **S3** Close-down | **Sonnet** | Yes — A5, A10, A11 | §3 Step B's archives; §4 Step 8's hand-off | Tree committable in one command, Day-1 handed forward |

**Why Opus only on S2.** S0, S1 and S3 execute checklists whose every branch is written. S2 carries
four reads where the branch you are in is not obvious from the surface: the mechanism verdict
(CONFIRMED vs REFUTED changes what the entire fleet is allowed to do), the C10 unit read (a moment
that exists exactly once and cannot be re-created), the DST verdict (an unread check is treated as
the failure branch, so "I couldn't read it" and "it failed" have to be distinguished carefully), and
the three-mechanics-in-two-minutes attribution. A Sonnet session at a STOP hands to Andy; Andy
re-opens it on Opus. That ladder is in §0.2 of every prompt.

**Close the chat between sessions.** Long OA sessions saturate and start dropping reads — every
2026-08 build session that ran past a natural boundary paid for it. Each prompt is written to be
pasted into a fresh chat against the previous session's written close-out.

---

# §4 · WHAT THIS PACK DOES NOT COVER

Named so nothing is assumed handled:

- **`daily.sh` at n=0** — Andy's terminal (gate A9). `tape.py` needs network; `device_bash` has none.
- **Wiring A7 into `daily.sh`** — Claude Code's lane (`CLAUDE.md` §7). Runbook Step 4(b) requires
  it; it is not done, and S0/S2 report it as an open gate rather than closing it.
- **The comparative machinery implementation** and `research_loop.py`'s D-1…D-17 fixes — Claude
  Code, post-downgrade, with the two G-10 constraints from `post-u1-package-2026-08-07.md` §2
  (the max-T restatement must not silently undo G-10; the family region needs a per-member
  direction vector declared pre-data). ⛔ `research_loop.py` is 0.1.0-DRAFT with three fatal
  defects — DO NOT WIRE IN until its fixtures pass.
- **Track B** — PR-21/PR-22 unsigned, ARM-B1 blocked on C10. Nothing is switched on for Track B on
  Day-0. Wave 1 is 22 of 50; ceiling 28.
- **`post-u1-package-2026-08-07.md` §10's seven gated items** and the post-downgrade backlog
  generally.
- **The pilot's Bot Group** (runbook §3 Step A / audit F-21) — small, and it belongs to whichever
  session is on the pilot when Template V2 lands.
- **Mirror funding.** Zero of ten mirrors clears the bar and none can before late Oct 2026. The
  Day-0 action is re-arm, watch-only, size nothing. It is not a Day-0 decision and this pack does
  not open it.

---

*Written 2026-08-07. This file is the pack; it edits nothing else. Every number in it was read from
the folder this session. Where the folder and project memory disagree — the lockout record and the
F-C1/F-C2 rulings — the divergence is stated in §1.3 rather than resolved, and S0 closes it under
Andy's gate A3.*
