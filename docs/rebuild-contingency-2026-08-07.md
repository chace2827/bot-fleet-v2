# Rebuild contingency — 2026-08-07

> ⚠️ **INSURANCE, NOT A PLAN IN MOTION.** OA support (Zack) replied ~12:30 ET 2026-08-07: the 41
> lost bots will be restored, "operational again by Monday." Restore is the expected path. This
> document exists only for the case that restore does not land by then — it is written now,
> while the roster and every capture file are still fresh in context, precisely so it does not
> need to be written under pressure later. **Do not start any step in this document** without
> reading its DO-NOT-START gate (§4) first. See `docs/state.md`'s dated incident block
> (2026-08-07, "OA REACTIVATED BUT ROSTER LOST") for the facts this plan responds to, and
> `day0-session-pack-2026-08-07.md` §1.1 for the roster arithmetic it supersedes-in-part.

---

## §1 · Inventory — the 8 built bots

Source: `data/bots_config_v2.csv` (BOT rows only) cross-checked against each bot's own capture
file. Scope is exactly the 8 rows that file tracks as built — the 7 greenfield arms (PR-14…PR-20)
plus the PR-01 clone. It does **not** include `QQQ-IC-0DTE-Fortress` (PR-03, the pilot clone,
built 2026-08-03/04 under a separate card, `pilot-clone-card-qqq-fortress.md`, and never entered
into this CSV) — Fortress's own template survived and its rebuild is a template-clone like the
greenfield seven; it is not re-tabled here because it was never at risk of being untracked.

| Bot | PR | Template | Rebuild source | Capture file | Unrecoverable if rebuilt |
|---|---|---|---|---|---|
| `GF-QQQ-IC-Ride` | PR-14 | **EXISTS** — V1 `Tfw5TkkCRF4417860721733331241` | Template clone + `greenfield-family-spec.md` §9 (arm entry) + this CSV's DECODED row | `data/captures/2026-08-07-greenfield/GF-QQQ-IC-Ride/GF-QQQ-IC-Ride.txt` | Bot ID `BOTfw5TkkCRF4417860701930934951` and bot-input IDs `IN178607080900761`/`IN178607092377072` — a rebuild gets new IDs; every doc citing these needs the new ones pasted in. **Nothing traded** — `AUTOMATIONS OFF` throughout its life, so there is no live trade history to lose. |
| `GF-QQQ-IC-PT50` | PR-15 | **EXISTS** — V1 `Tfw5TkkCRF4417860751149180062` | same pattern | `.../GF-QQQ-IC-PT50/GF-QQQ-IC-PT50.txt` | Bot ID `...4417860738688735152` + inputs `IN178607449758461`/`IN178607460887972`. Never traded. |
| `GF-QQQ-IC-Trail` | PR-16 | **EXISTS** — V1 `Tfw5TkkCRF4417860759179743713` | same pattern | `.../GF-QQQ-IC-Trail/GF-QQQ-IC-Trail.txt` | Bot ID `...4417860754672239833` + inputs `IN178607567686951`/`IN17860757187372`. Never traded. The signed G-12b tail-retirement criterion (`pre-registration-ledger.md` PR-14…PR-17 entry) lives in the doc, not the bot — unaffected by a rebuild. |
| `GF-QQQ-IC-Touch0` | PR-17 | **EXISTS** — V1 `Tfw5TkkCRF4417860766269007264` | same pattern | `.../GF-QQQ-IC-Touch0/GF-QQQ-IC-Touch0.txt` | Bot ID `...4417860760818962144` + inputs `IN178607636188121`/`IN178607647487782`. Never traded. |
| `GF-QQQ-IC-SL100` | PR-18 | **EXISTS** — V1 `Tfw5TkkCRF4417860773009022425` | same pattern | `.../GF-QQQ-IC-SL100/GF-QQQ-IC-SL100.txt` | Bot ID `...4417860767788927225` + inputs `IN178607699688851`/`IN178607709288872`. Never traded. The "Breakeven" naming question (OPEN-4…7, gated) is a doc-side item, unaffected. |
| `GF-QQQ-IC-Canary` | PR-20 | **EXISTS** — V1 `Tfw5TkkCRF4417860782548949126` | same pattern | `.../GF-QQQ-IC-Canary/GF-QQQ-IC-Canary.txt` | Bot ID `...4417860774419022836` + inputs `IN178607794990451`/`IN178607800989862`. Never traded. |
| `GF-QQQ-IC-SL200` | PR-19 | **EXISTS** — V1 `Tfw5TkkCRF4417860791919674137` | same pattern | `.../GF-QQQ-IC-SL200/GF-QQQ-IC-SL200.txt` | Bot ID `...4417860785000861357` + inputs `IN178607891888981`/`IN178607897588482`. Never traded. |
| `IC-SPX-FastPT25-S2` (clone, held the production name) | PR-01 | **NONE** — `template NOT SAVED (showBotMenu unresponsive)` per this CSV's clone-session row. This is a **pre-existing defect** (the Trap-10 class in `oa-ops-runbook.md` §5), not new loss from today's incident. | Capture file + `pre-registration-ledger.md` PR-01 entry (hypothesis/kill criterion/INVERTED verification) + the four cloned automations' hashes recorded in this CSV's clone-session row | `data/captures/2026-08-07-clones/06-clone-final/IC-SPX-FastPT25-S2.txt` | Bot ID `BOTfw5TkkCRF4417860821948715488`. Fresh clone at n=0 per the ledger's own note ("deliberately does NOT inherit the 29 post-fix condors") — never traded, so no trade history lost. **Must be REDONE, not re-cloned from a template** — none was ever saved. Re-run the clone-to-spec ritual (`build-plan.md` §2B, `reactivation-runbook.md` §3 Step A's 9-step checklist) against the champion bot — see §2 below: that champion bot is itself one of the 41 lost, so this clone cannot start until the champion exists again, restored or rebuilt. |

**Before trusting "clone-from-template" for the seven rows marked EXISTS**: the Automation
Library **survived** (all 4 objects, reading "Unused") — but "Unused" means no bot currently
references them, not that their `rid`s are unchanged. Read each of the 3 shared automations
fresh and confirm its `rid` still matches the value recorded in `bots_config_v2.csv`
(`RTfw5TkkCRF178605283747821` ScannerA · `RTfw5TkkCRF178606271659881` ScannerB ·
`RTfw5TkkCRF178606373201751` Backstop) **before** assuming re-attachment reuses the same object.
A changed `rid` means the object was recreated, not preserved, and `CLAUDE.md` §5's "never reset
OA history by cloning" concern applies to it directly.

---

## §2 · What needs rebuilding WITHOUT a template

**Three clone-program bots — no template exists for any of them:**
- **PR-02** — `IC-SPX-FastPT25-S2-130PM` (never-started clone; the *original* bot itself, an
  entry-time A/B, was one of the 41 lost — there is nothing left to clone even from, template or
  otherwise). Rebuild source: `pre-registration-ledger.md` PR-02 entry + `data/bots_meta.csv`'s
  row (last known config, pre-cutover) + `data/oa_facts.csv` for any first-hand field reads on
  file. This is a from-scratch build against a written spec, not a clone.
- **PR-04** — `QQQ-IC-0DTE-Fortress-NoPT50` (same situation: never-started, original lost, no
  template). Rebuild source: `pre-registration-ledger.md` PR-04 entry + `bots_meta.csv` row. The
  `QQQ-IC-0DTE-Fortress` **template does survive** (PR-03, the pilot) and shares this bot's base
  mechanic minus PT50 — usable as a structural reference, not a source of record for NoPT50's own
  config.
- **PR-01 redo** — see §1's last row. Blocked on the champion bot existing again (restored or
  independently rebuilt) since the clone-to-spec ritual clones FROM a live bot, not from a spec
  alone.

**The nine leave-in-place bots** (`day0-session-pack-2026-08-07.md` §S0 Step 3's roster list):
`DIR-SPX-PutVIX22-SL75` · `DIR-SPX-CallVIXdrop` · `3DTE $140-$350` · `Nigiri-Paper-v1` ·
`QQQ long call` · `Friday 14 DTE Broken Wing IB (B-70)` · `Trendy-Paper-v1` ·
`60min-ORB-10W-Paper-v1` · `Tasty Condor`. None of these has ever had a saved OA template — they
predate the template-based build entirely. Two are Directional paper bots; seven are OA-Mirror
watch-only. **They are rebuildable as watchers/paper bots from `data/bots_meta.csv` and
`docs/directional-oa-build-sheet.md`** (config notes, VIX gates, position sizing are all recorded
there) — a fresh bot object can be stood back up.

**What a rebuild of the nine cannot recover, stated plainly:**
- **Live trade history predating `data/mirror_baseline.csv`'s freeze is safe** — that snapshot
  (174 positions, 10 mirrors, zero excluded, written 2026-08-04) is a frozen local file, untouched
  by today's incident regardless of what OA does. What is lost is any trading these bots did
  **between the 2026-08-04 freeze and the 2026-08-07 disable**, and all OA-side identity (bot ID,
  Automation Log, toggle history) — a rebuilt bot is a new object with no memory of the old one.
- **D-4's Day-0 discrimination test is foreclosed, not delayed.** `day0-session-pack-2026-08-07.md`
  §S2 Step 2c (the no-touch toggle observation, run once, before any toggle is moved) and Step 6a
  (the mechanism verdict) both depend on reading these bots' exit-toggle state at the *exact*
  moment of reactivation, on the *original* bots that sat lapsed since the June failure — that is
  the entire point of the observation (`day0-session-pack-2026-08-07.md` line ~936: "THIS IS FREE
  AND THE INFORMATION IS NOT RECOVERABLE AFTERWARDS"). A rebuilt bot starts at whatever default
  state OA gives a fresh object — it was never lapsed, so it cannot answer whether the June
  toggle was OFF by billing-state or OFF by hand. **If rebuild is needed, D-4 stays `THE JUNE
  CAUSE IS UNKNOWN` permanently** — not "pending Day-0" but closed-unanswered.
- **The 5-position ride-or-close decision is mooted, not preserved.** `reactivation-runbook.md`
  §4 Step 2 (Andy's gate A6) calls for a signed, executed ride-or-close call on the 5 open mirror
  positions. If the account wipe closed or dropped those positions outright, there is no longer a
  decision to make — the outcome was forced by the incident, not chosen by Andy, and that
  distinction should be recorded rather than silently absorbed into "the position closed" the next
  time anyone reads the mirror ledger.

---

## §3 · Rebuild sequence (per bot with a surviving template)

Applies to the seven greenfield arms and, once the champion exists again, PR-01's redo minus its
own template step (see §1/§2).

1. **Clone-from-own-template.** Bot Templates → the arm's own saved template → create bot.
   Confirm the new bot inherits Paper mode, `seed 2500`, limits 2/2, scan 1m/1m, Day Trading
   Allowed, Group `IC`, and starts `status "off"` / `disableExits 0` (AUTOMATIONS OFF, EXIT
   OPTIONS ON) — the greenfield family's own build convention
   (`day0-session-pack-2026-08-07.md` §1.1), not something to re-decide.
2. **Re-link the 3 shared automations by `rid`** — attach by reference, not copy (the Library
   must keep reading "N bots" per object afterward, never split into a new object). Confirm each
   `rid` first per §1's note above.
3. **Re-create the two bot inputs per arm** — `GF_EXITS_PUT` and `GF_EXITS_CALL`, each Automation
   Input's Default Value set to `NONE` (not `SENTINEL-SL1` — that convention was struck by the
   F-4 ruling, `greenfield-family-spec.md` §1.3a), then load the arm's own exits preset onto the
   Open Position action per `greenfield-family-spec.md` §4.4. Read back **both bot input objects**
   (not the action, not `oldValue`) and decode them; assert `GF_EXITS_PUT == GF_EXITS_CALL` (A8)
   and that both are bound and non-empty (A9).
4. **Verify against the bot's own capture file, field-by-field.** Templates carry Notes/PR blocks
   that are easy to fat-finger by re-typing — compare byte-exact instead
   (`greenfield-family-spec.md` line ~1624's convention: length-and-content compare, not eyeball).
5. **Re-run the A-series** (`greenfield-family-spec.md` §8.3, run by hand — there is no
   `daily.sh` runner for it) against fresh captures of the rebuilt roster, including an A7
   re-baseline read on the 3 shared automations. Nothing goes to `AUTOMATIONS ON` until the
   A-series is green and Andy has accepted the roster (`day0-session-pack-2026-08-07.md` A4).

For PR-02, PR-04, and PR-01's redo (no template): the same field-by-field capture-diff
verification applies at the end, but steps 1–2 are replaced by the full clone-to-spec ritual
(`build-plan.md` §2B, `reactivation-runbook.md` §3 Step A) run from whatever source bot exists —
and for PR-02/PR-04, that source bot no longer exists either, so the build is from the written
spec in `pre-registration-ledger.md` and `bots_meta.csv`, not a clone.

---

## §4 · DO-NOT-START GATE

**Nothing in §§1–3 executes without Andy's explicit word, given after OA's answer.** This
document is contingency planning, not authorization. Restore is the expected path
(the note at the top of this file) — if it lands, this entire document is moot and stays in the folder as a record of
what was prepared, not what was done. If it does not land, come back to this file, confirm it is
still current against a fresh read of `/bots` and `data/bots_config_v2.csv`, and get Andy's word
before the first click.
