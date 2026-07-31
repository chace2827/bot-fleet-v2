# Day-0 reactivation runbook

*Rewritten from scratch 2026-07-30 after the consolidation pass. Supersedes all earlier versions.
Account inactive; reactivation ~mid-Aug 2026. **Not blocked** — the re-arm mechanism is known (§1).*

> **Read `docs/build-plan.md` first.** It is under decision freeze and defines the fleet disposition this
> runbook executes. Do not improvise a change here on the day.

---

## 0. What is different this time

Day-0 used to mean re-arming ~35 lapsed bots and hoping. It doesn't any more.

**Every active bot on Day-0 is fresh-built, cloned-to-spec, or untouched-validated.** The clones and fresh
builds are constructed *after* reactivation with their exits correct from birth, so they were never lapsed
and have nothing to re-arm. **The re-arm sweep applies to nine bots only** — the two directional bots and
the seven live mirrors, the only ones that lived through the lapse.

Most of the build work happens **before** you pay. Edits made while the account is inactive **do persist**
(verified empirically 7/29→7/30). Do as much of §3 as OA allows before Day-0, and log every inactive-era
edit.

---

## 1. The lapse mechanism — ANSWERED (OA support / Zack, 2026-07-30)

**Each bot's dashboard carries a per-bot `EXIT OPTIONS` ON/OFF toggle at the top right, beside the
`AUTOMATIONS` toggle. That toggle is the hidden state.**

Deactivation turns both off. Resubscription restores **only `AUTOMATIONS`** — which is why the monitors
fired while every PT and time exit stayed dead. The failure is **visible only on that dashboard toggle,
never in the editor**: the Exit Options editor keeps displaying every setting exactly as configured.

**Andy has confirmed both toggles are currently OFF on every bot.** That is the state Day-0 starts from.

What this cost in v1: **−$9,618** net across the Fortress pair over six June days — concentrated enough
that two put legs alone lost −$9,734 across two of those days, with call-side wins offsetting the rest.
It was invisible for six sessions. The champion's PT25 died on June 1, the first session back, while its
6/14 clone worked 70/0.

Two design consequences, already built in:
- **One toggle kills every Exit Option on a bot at once** — PT, Touch and time exit together. No partial
  failure mode, no redundancy inside Exit Options. This is why the **15:52 flat-close backstop lives on the
  `AUTOMATIONS` side**, a different execution class.
- **On the two control clones, PT25 is removed from the Open Position action explicitly** rather than left
  dead behind an off toggle. A toggle can be flipped by accident; a removed action cannot.

Caveat that still stands: this came from **one rep**, who did not know the documented Excessive Errors
Failsafe. Verify capabilities in the UI. And **the toggle being ON was never the failure we observed being
detected** — a toggle screenshot is necessary but not sufficient. Keep the order-level verification.

---

## 2. The per-clone checklist — run this for each of the 4 clones

Order matters. Two of these steps exist because of traps that will silently produce a broken bot.

1. **Clone** the original bot.
2. **Fork ALL automations via Copy.** ⚠️ **THE TRAP: clones share automations by reference.** Edit one and
   you have edited the original too — or worse, the original's later edit silently changes your clone.
   Copy every automation so the clone owns its own, then confirm the clone's automation list points at the
   copies.
3. **Re-add Symbols.** ⚠️ They drop silently on clone. A bot with no Symbols looks configured and simply
   never scans.
4. **Apply the spec** from `build-plan.md` §2B. Nothing beyond the spec.
5. **Capture the automation tree** (bookmarklet) — this is what `bots_config_v2.csv` will cite.
6. **Save as template V1** with the pre-registration note attached, so the config has a versioned identity
   from birth.
7. **Verify both dashboard toggles** — `AUTOMATIONS` and `EXIT OPTIONS` — and screenshot them.
   Toggle state does not survive text capture. *(For the two control clones, `EXIT OPTIONS` stays OFF by
   design and PT25 is already removed from the action — verify the removal, not the toggle.)*
8. **Rename the original** with an `-ARCHIVED-<date>` suffix, **then archive it.** Renaming first frees the
   production name for the clone and keeps the archived record self-labelling.
9. **Log it** — clone date, spec applied, template version, capture filename, and the archived original's
   new name. **Append the row to `data/archive/rename_map.csv`** (`original_name`, `archived_as`,
   `clone_name`, `date`, `disposition`) as you go, not afterwards from memory. This is the only thing that
   will later connect a name in the frozen ledger to a bot running today.

---

## 3. Before Day-0 — the build window

**Edits made while the account is inactive persist** (verified 7/29→7/30), so the entire build happens
*before* you pay. Day-0 itself should be a short, boring checklist — not a build day.

### Step A — Pilot the clone ritual on ONE bot first
Run the full 9-step checklist on **`QQQ-IC-0DTE-Fortress`** and nothing else. Find out where the automation
Copy-vs-reference trap and the Symbols drop actually bite, on a bot whose spec is simple and whose original
is already superseded. **Do not start the other three clones or any fresh build until this pilot is clean.**
A mistake made once is a lesson; the same mistake made across nine bots is a rebuild.

### Step B — Capture the roster, then sweep
Bookmarklet capture of `/bots` **first** — it is the roster authority and the only record the zero-trade
bots will ever have. *(Done 2026-07-30: `data/captures/oa_bots_capture_2026-07-30.txt`, 35 bots.)*
Then: **positions → archive, empty → delete** (`build-plan.md` §2).

Two traps in this step, both of which destroy something if you move fast:
- ⛔ **Delete exactly two bots**: `TEST QQQ-IC-0DTE-HedgeC-S3 Clone` and `QQQ-IC-0DTE-InvFilter-Wide150`.
  **`DIR-SPX-PutVIX22-SL75` is also zero-trade and must NOT be deleted** — it is an OOS-validated build
  whose VIX≥22 gate correctly never fired. Empty ≠ worthless.
- ⚠️ **Read full names before archiving**: `Opening Range Breakout 60m` is archived,
  `60min-ORB-10W-Paper-v1` stays live.

### Step C — Build the rest
The remaining 3 clones per §2, then the 5–7 fresh builds. Greenfield exits are a named **Exit Option Preset
in the Open Position action** (PT% as a Bot Input · Touch $0 on the challenged side · time exit), plus the
**15:52 flat-close Scheduled Event backstop**, plus a **position-closed-trigger automation** to close the
sibling spread. Optional 1-lot canary.

### Step D — Pre-register everything
Draft a pre-registration entry for all ≈18 active bots during this window, so **Day-0 is signing, not
authoring**. Hypothesis · kill criterion · sample target · review date · config-capture hash.

### Step E — Dry-run the pipeline at n=0
Run `daily.sh` end-to-end against an empty post-cutover ledger. Every script must **degrade gracefully at
n=0** — no divide-by-zero, no empty-frame crash, no misleading 0.0% expectancy rendered as a finding.
Day-1 is the worst possible time to discover the reporting stack cannot handle having no data yet.

---

## 4. Day-0 sequence

### Step 1 — Pay / reactivate
Note the exact timestamp. **This date is `LEDGER_START`.** Set it in `build_ledger.py` before anything
else, so no pre-cutover row can enter the working ledger.

### Step 2 — Decide the open mirror positions: ride or close
Five positions were open at the 2026-07-30 capture and will still be open at reactivation:
**`QQQ long call` ×4** — ~$13K risk, ~**−$10.8K unrealized** — and **`Tasty Condor` ×1** (~+$328).

Make an explicit, logged **ride-or-close** call on each before anything else trades.
This must not be the one undecided thing on the account: an unmanaged legacy position is exactly the kind
of quiet exposure that survives a clean-slate rebuild and then surprises someone. Whichever way it goes,
write the reason into the pre-registration ledger — these are pre-cutover positions, so under the straddle
rule their P/L resolves into the **mirror baseline layer**, never the working ledger, and they will not
appear in any post-cutover report unless someone deliberately looks.

### Step 3 — Re-arm sweep: the nine leave-in-place bots ONLY
`DIR-SPX-PutVIX22-SL75`, `DIR-SPX-CallVIXdrop`, and the seven live mirrors
(`3DTE $140-$350`, `Nigiri-Paper-v1`, `QQQ long call`, `Friday 14 DTE Broken Wing IB (B-70)`,
`Trendy-Paper-v1`, `60min-ORB-10W-Paper-v1`, `Tasty Condor`).

For each: **`AUTOMATIONS` → ON** and **`EXIT OPTIONS` → ON**, then screenshot both toggles.

Nothing else on the fleet needs re-arming. Clones and fresh builds are born correct; the ~20 archived bots
are gone.

### Step 4 — Confirm the build window is complete
Every clone and fresh build has: a capture on file, a saved template V1, a signed pre-registration entry,
and a `rename_map.csv` row. Anything missing is finished now or its bot stays OFF.

### Step 5 — Capture everything
Full bookmarklet sweep of `/bots` across the whole new roster, plus toggle screenshots. This is the
baseline `bots_config_v2.csv` and the comparator the drift detector needs.

### Step 6 — Order-level verification, per bot, before it may trade
Two acceptable proofs, in order of preference:
- **Button test-fire**, then read the resulting **Trades list**; or
- open the **first new position** and confirm the Trades list contains the PT row and the exit-trigger row.

**The Exit Options panel is NOT evidence.** Exit Options are copied per-position at open; the panel shows
intent, the Trades list shows what was attached.

For the two control clones the verification is **inverted**: confirm their Trades lists show **no** PT or
exit-trigger rows — the ride behavior is intact and their S2 monitor is firing.

### Step 7 — Only now allow entries
Hard gate, not a preference. A bot that cannot be proven stays OFF until it can.

### Step 8 — Day-1 monitoring
Liveness check: every ON bot must show a position **or** a scanner run in the capture window. OA bot logs
record non-actions, so **zero log entries = presumed OFF or Failsafe-tripped → RED.**
Same-day engine-death checks: the expired:closed ratio flip, and any position with `mfe_pct` ≥ its declared
PT and no PT order. Any RED emits an instruction card, repeated at the top of every brief until closed.

---

## Pre-Day-0 checklist
- [x] ~~Support's re-arm procedure~~ — **ANSWERED, see §1**
- [ ] `LEDGER_START` implemented in `build_ledger.py` and defaulted to refuse pre-cutover rows
- [ ] `data/mirror_baseline.csv` written — the one-time frozen pre-lapse snapshot for the 7 mirrors
- [ ] `data/raw/` + `data/brief/` pre-cutover files resolved (filtered or moved to `data/archive/`)
- [ ] `execution_audit.py` passing its validation matrix against the frozen 35-row fixture, surfacing
      **both** T00147 and T00845 and staying silent on the R>1 winners
- [ ] A **pre-registration entry** for every one of the ≈18–20 active bots — including the untouched nine —
      dated before its restart
- [ ] `oa-platform-reference.md` and `hedge-research.md` rewritten from the archive (they gate the
      greenfield and tournament builds)
- [ ] Sizing decided and written down: 1 lot for experiments, ≈$5K risk/position for CANDIDATE+,
      identical allocation across tournament arms
- [ ] Clone ritual **piloted on `QQQ-IC-0DTE-Fortress`** and clean before any other clone or build
- [ ] `data/archive/rename_map.csv` started
- [ ] `daily.sh` dry-run at n=0 passes — every script degrades gracefully on an empty ledger
- [ ] All ≈18 pre-registration entries **drafted** during the build window
- [ ] Ride-or-close decision prepared for the 5 open mirror positions (`QQQ long call` ×4, `Tasty Condor` ×1)
