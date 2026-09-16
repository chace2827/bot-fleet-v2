# Narrative for the 2026-09-16 brief.
# Injected by scripts/render_brief.py into the slots of the same name.
# Sections: since-yesterday | convexity | lesson | tomorrow | fire | strategy

## since-yesterday
**This is a catch-up close.** Last close 2026-09-04; **6 trading days unobserved**
(09-08, 09-09, 09-10, 09-11, 09-14, 09-15). The last *narrative* is older still — 2026-08-19 —
so the watch list below is graded across **19 sessions**, not one. Read the grades as
end-state readings, not as a day-by-day record. What the ledger cannot see is stated in
**the gap** at the end of this slot.

**Grading the 08-19 `## tomorrow` list:**

1. **Does the call side fill again, or was 08-19 a one-off?** — **ANSWERED: not a one-off.**
   The call side has filled on every GF session since: 09-09 (4 of 7 arms), 09-14 (5), 09-15 (5),
   09-16 (7 of 7). The old "the call leg never fills" hypothesis is dead twice over.
2. **Do the two sides ever fill as a single condor, or is separate-event filling permanent?** —
   **ANSWERED: separate-event filling was not permanent.** On 08-19 the two sides filled 19
   minutes apart (13:33 / 13:52) and never paired. On 09-14, 09-15 and 09-16 the two sides fill
   **in the same minute** (13:31:xx both legs) and the ledger pairs them into one `trade_id`
   with `single_sided=False` — 6 of 7 arms on 09-16. ⚠ **Caveat, not a hedge:** "one condor" here
   is the *ledger's* pairing label (`build_ledger.py` pairs a call and a put on the same bot-day
   within `PAIR_WINDOW_S`). It is not an OA-side observation that one condor order was sent. The
   falsifiable claim is the narrower one: **inter-side fill latency collapsed from ~19 min to ≤1 min.**
3. **Ride-Delta: fourth consecutive double-fill?** — **CLOSED BY DECOMMISSION, not by evidence.**
   `GF-QQQ-IC-Ride-Delta` has not traded since 08-31. It is still on the roster and reads
   **AUTOS OFF / EXITS ON** in the 09-16 capture. It was switched off somewhere between 08-31 and
   the 09-07 capture; no day is attributable. The question is unanswerable as posed and should be
   struck, not carried.
4. **A day where delta and pct imply different strikes?** — **STILL NO OBSERVATION, 19 sessions
   running.** All arms carry an identical short put on every one of the 16 GF sessions in the
   ledger. Layer 2 is no closer. One new datum worth a claim: on **09-16 the short put sat 1.50%
   below the underlying open** (699 vs 709.67) against a 0.28–0.58% band on every prior session —
   a 3x jump on the one day the tape actually moved. Whether that is a vol response or a
   selection-method difference is **a claim to verify, not a finding**.
5. **PR-01 champion: two fills in a row, or back to silence?** — **ANSWERED: it fires most days
   and it is silent today.** `IC-SPX-FastPT25-S2` fired 09-08, 09-09, 09-10, 09-14, 09-15 —
   five of the six unobserved days — then **did not fire on 09-16**, which is why it carries a
   SUSPECT verdict below. And the *shape* of those fills is the headline of this close.

**THE HEADLINE — the EXPIRY_RATIO_FLIP RED on `IC-SPX-FastPT25-S2`.**
The audit (detector 1.1.0, frozen 2026-07-30, REDUCED mode) fires exactly **one RED** across
333 position rows: `EXPIRY_RATIO_FLIP`, MECHANICS/S, **40% expired over the last 10 vs 0% over
the prior 15**, onset addressed as *"the Trades list of T00694 (2026-08-31)"*, tripped on the
position opened 09-10. The detector's own wording: *"Positions stopped CLOSING and started
EXPIRING — the signature of an exit that no longer generates orders."*

**The ledger says the signature is real and the reading is wrong.** Partition PR-01's 26 trades
by leg count:

| | trades | of which expired |
|---|---|---|
| **two-leg (paired condor)** | **3** | **3 — all of them** |
| **one-leg (unpaired spread)** | **23** | **0 — none of them** |

Perfect separation, 26 of 26. Every expiry (08-31 T00694, 09-10 T00640, 09-15 T00613) is a
**two-sided condor that rode to 16:15 and expired at `exit_price=0`** — full credit, +$100/+$150
per leg, `mfe_pct=1`. Every single-sided fill closed **in 2–6 minutes** (11:01→11:03, over and
over). Nothing about the exit degraded. The bot started filling *both* sides, and both-sided
positions have a different exit path from one-sided ones.

**The sister arm is the control.** `IC-SPX-FastPT25-S2-130PM` has **48 positions, 24 two-leg
trades, and zero one-leg trades ever** — it always fills both sides — and **21 of its 24 condors
expired**. Its baseline expiry ratio was already 73%, so it never "flipped" and never tripped the
RED. Two bots, opposite fill behavior, opposite exit behavior. The detector caught the arm that
*changed*, and what changed is upstream of the exit.

**The mechanism — one part verified, one part hypothesis.** The chat session proposed that
`Scalp-Mon-S2-Cleanup` closes only when the bot holds exactly one position. **That part is
already verified on disk** and does not need re-deriving: the 08-31 read-only config capture
(`data/captures/2026-08-31-roster/09-s2-config-check-2026-08-31.md`) records the node text
verbatim — `ALL of: posopentime ≥ 2 minutes AND countpos "Bot has exactly 1 position" → closepos
100%` — with all four automation hashes byte-identical to the 2026-08-07 baseline
(cleanup `f3673f29…`, v2). One side fills → count 1 → scratched at 2 minutes. Both fill → count 2
→ the guard fails → nothing closes. **Two sides filling is therefore not a better trade; it is the
absence of an exit.**

What is **not** verified, and is filed as a claim:
- **(C-1)** The config was last read **08-31**. The 09-10 and 09-15 expiries are *after* that read
  and no re-hash has been taken since; the 09-16 capture is roster toggles only. The mechanism is
  established for the 08-31 expiry and *consistent with* the two later ones.
- **(C-2)** The cleanup window appears to end before the cash close. On **09-08** the 130PM arm's
  put closed at **15:59** at −$1,850 (StrikeTouch, a breach) leaving its call unpaired — and the
  call was **never cleaned up**; it expired at 16:15. Under a naive count==1 reading it should have
  closed ~16:01. The 08-31 bot log notes both monitors looping *through 3:55PM*. The refined rule —
  *StrikeTouch closes a breached leg regardless of count; Cleanup closes an unpaired leg after
  2 min but only while the monitor loop runs; a paired, unbreached condor has no exit at all* —
  fits all three of the 130PM non-expiry trades (08-26, 08-27, 09-08: each one leg closed at a
  −$1,650 to −$1,900 breach). **Inferred from timestamps. Not read from the bot.**

**⚠ OWED — the T00694 verify, and how to address it.** The RED's `verify_by` asks: *"the Trades
list of T00694 (2026-08-31): is there an exit order at all?"* **This is recorded as OWED and is
NOT discharged by the above.** The ledger and the config capture are two derivations of the same
claim; the Trades list is the independent third surface, and two agreeing derivations are weaker
than one checked against a different surface. **Record the verify by bot + open time —
`IC-SPX-FastPT25-S2`, position opened 2026-08-31 11:01 ET — never by trade ID.**

**Why the ID is unsafe, verified:** `build_ledger.py` assigns `trade_id` from a counter seeded at
`max_existing_tid(day)` and renumbers **every** row in the export on every build, so a given
position's ID moves with each close. This is not a code reading only — the same 08-31 11:01:01
PR-01 condor is **`T00261` in `data/hedge_tournament.csv`** and **`T00694` in today's
`data/trades.csv`**. One position, two IDs, on disk right now.

**⚠ TRACKER ITEM, FLAGGED NOT FIXED — `execution_audit.py` bakes stale IDs into `verify_by`.**
Line 344 emits `f"the Trades list of {onset_tid} ({onset})"`, and ~12 other `verify_by` strings
address positions the same way. Every one of those pointers is valid only against the export that
produced it and silently misaddresses after the next close. The fix is to address by
`bot + open_date` (a natural key that survives renumbering). **Gated machinery — flagged for a
ruling, no edit proposed or made here.**

**ROSTER — 44 → 43.** The 09-16 capture footer reads verbatim `43 active bots • 7 left in your
plan`; the 09-07 capture read `44 active bots • 6 left`. The bot that left is
**`QQQ-IC-0DTE-Baseline`** (`BOTfw5TkkCRF3317727290514286611`), present in the 09-07 toggle table
at OFF/OFF, absent from the 09-16 one. AUTOS ON held at 18 and EXITS ON at 16 across the change,
consistent with an OFF/OFF bot leaving. `data/bots_meta.csv` still carries its row —
*"unfiltered control; archive candidate"* — so the meta now has an **orphaned row with no roster
counterpart**, which is the same class of invariant gap that rerouted $600 of realized P&L in the
08-19 finding. Not a P&L risk here (the bot has no rows in the working ledger) but it should be
reconciled, and **no day in the window is attributable** for the deletion.

**VERDICTS — 4 SUSPECT, 3 UNEVALUABLE_BY_DESIGN, 2 JUSTIFIED (9 evaluated).**
- `IC-SPX-FastPT25-S2` (PR-01) — SPX 7616.17 at 11:00, Δ% 0.4 against a 0.75 threshold. **Inside
  the band, and silent.** The champion did not fire on a GO day.
- `IC-SPX-FastPT25-S2-130PM` (PR-02) — SPX 7609.19 at 13:30, Δ% 0.31. **Same story, same day.**
  Both S2 arms silent together is the single most interesting silence in this brief.
- `60min-ORB-10W-Paper-v1` (PR-12) — SPX 7616.17 at 11:00 breaks the ORB range 7597.61–7614.97.
  The range broke and nothing fired.
- `IC-SPX-Fortress-Unstopped` (INC-01) — no market gate and no `fill_precondition` declared;
  silence is suspect **because nothing was ever declared**, which is a documentation defect, not
  a bot defect.
- UNEVALUABLE_BY_DESIGN: `3DTE $140-$350` (PR-07), `Nigiri-Paper-v1` (PR-08),
  `Trendy-Paper-v1` (PR-11) — `gate_type=unknown`, no signed entry condition. Unchanged from
  08-19; three bots have now been unevaluable for 19 sessions.
- JUSTIFIED: `DIR-SPX-PutVIX22-SL75` (VIX high 16.75 < 22.0 threshold),
  `Friday 14 DTE Broken Wing IB` (Wednesday, gate requires Friday).

**THE GAP — what this close does not know.** The six unobserved days are reconstructed **only**
from closed-position rows in the 09-16 export. Specifically absent:
- **No tape for 09-08…09-15.** `data/brief/2026-09-16_tape.json` covers 09-16 alone. Every
  verdict, band check and convexity reading below is a **09-16-only** statement. The six missed
  days have P&L and fill times and **no market context whatsoever**.
- **No p3 verdicts for the missed days** — the TSV is 09-16 only. Silences on those six days were
  never adjudicated and now cannot be.
- **No roster or toggle state per day.** The drift verdict *"ZERO. Not one bot changed either
  toggle"* compares **09-16 against 09-07**. A bot toggled and toggled back inside the window
  reads as ZERO. The 44→43 deletion happened somewhere in that window and the capture cannot say
  when.
- **No OA bot logs**, so every exit attribution in this narrative is inferred from ledger
  timestamps rather than read from the mechanic that fired.
- **Anything opened and closed without landing in the export is invisible.** 338 rows in, 333 out.
- **Ledger totals, for scale:** 333 legs, 27 trading days, **+$11,945 cumulative on $790,834 of
  cumulative risk**. The window itself: 83 legs, **+$3,396 on $338,808 (1.0%)**.

## convexity
**The first day in this log where the long-vol case has something to show — and it still would
not have paid at the close.** VIX opened 16.91 against a 17.20 prior close, bottomed at **16.40
at 14:00** (−4.65%), then ran to **18.94 at 15:25** (+10.12% over the prior close) before settling
at **17.71 (+2.97%)**. Intraday range 15.5%.

An overlay bought at the morning lows and sold into the 15:25 spike would have paid handsomely.
Held to the close it earns +2.97% on the index — positive, but a fraction of what the path
offered. **Log it as the first genuinely ambiguous day**: the previous entries in this series were
clean losses for the long-vol case (08-19: VIX −6.0%, every structure bleeds). The honest reading
is that the convexity argument is now **one day for, several against, and entirely dependent on an
exit rule that has never been specified.** An overlay with no stated exit is not a strategy and
cannot be scored — that is the gap to close before the next such day, not after it.

Against the convexity case on the same tape: `DIR-SPX-CallVIXdrop` fired at 11:00 betting on a VIX
drop and lost **$425 of $725 risk** by 14:36 — it was right about the 14:00 low and did not
survive to see it matter.

## lesson
**The one clear trading lesson and the one clear governance lesson are the same event seen from
two ends: the fleet's best outcomes came from positions that had no exit.**

Start with the trading side, because 09-16 finally produced a tape worth reading. SPX ran to
+0.54% at 11:45, broke the ±0.75% GO band for **four bars, 15:10–15:25**, bottomed at
**7507.77 (−1.03%) at 15:25** — the same minute VIX printed its high — and closed at −0.45%.
QQQ made a 1.70% range around a +0.03% close. This is the first real intraday break in the record.

Watch what the GF arms did with it, all seven entered at 13:31, all on identical strikes:

| arm | put leg | exit | call leg | trade P/L |
|---|---|---|---|---|
| Touch0 / Ride | held to 15:50 | +$234 | +$312 | **+$546** |
| SL200 | **stopped 15:14** | **−$676** | +$312 | **−$364** |
| SL100 | **stopped 15:11** | **−$338** | +$390 | **+$52** |
| PT50 | 14:44 | +$182 | +$182 | +$364 |
| Trail | 14:07 | +$78 | +$78 | +$156 |
| Canary (1ct) | 14:06 | +$5 | +$1 | +$6 |

**Both stop arms fired 11 and 14 minutes before the low, and the arms that held recovered in
full.** SL200 turned a +$546 day into −$364 by having a stop. That is one observation, on one
break, and it is exactly the observation the family was built to produce — the first time in
19 sessions the stop arms have been asked a real question. **It is not yet a finding.** n=1.

Now the governance side. PR-01's three best trades in the entire ledger are its three condors, and
each earned full credit **because no exit order was ever generated** — the Cleanup monitor's
`countpos == 1` guard fails when both sides are open, and nothing else touches an unbreached
paired position. +$200, +$250, +$250 at 16:15, every time, `mfe_pct=1`. The 130PM arm has done the
same 21 times. **A bot that makes money by not having an exit is not a strategy that works; it is
an untested short gamma position running to settlement**, and its P/L record is a record of six
weeks in which SPX happened not to close through a short strike between 11:00 and 16:15. The three
times something *did* touch — 08-26, 08-27, 09-08 — the breached leg closed at −$1,650, −$1,900
and −$1,850, which is the shape of the distribution the expiries are hiding.

And the audit reported this as *"an exit that no longer generates orders"* — the right signature,
attached to the wrong cause, aimed at the wrong end of the bot. The 08-31 capture said so three
weeks ago in plain text and the detector had no way to know. **The lesson for the machinery: a
finding is an address, not a diagnosis, and the diagnosis in this case was already sitting in a
capture file that nothing reads.** The RED is correct and useful precisely because it is
under-specified — it pointed at the right position. What closed it was a human-readable artifact
the detector cannot see.

## tomorrow
1. **Does PR-01 fire at 11:00 at all?** It was silent today with SPX 0.4% from the prior close,
   well inside its 0.75% band. One silent day after five consecutive fires is the thing to watch.
2. **If it fires two-sided, does the condor ride to 16:15 again with no exit order?** Prediction,
   stated in advance so it can fail: **yes**, and at full credit. Four for four would make the
   mechanism a fact rather than a fit.
3. **Does the 130PM arm ever produce a single-leg trade?** Zero in 48 positions. The first one
   would be the cleanest possible test of the `countpos == 1` rule — it should scratch in ~2
   minutes.
4. **Do all seven GF arms pair same-minute again?** Six of seven did today; SL100's call came in
   11 minutes late (13:42) as a separate trade. Two clean sessions makes the ≤1-min fill latency
   a regime rather than a run.
5. **Another band break — do the stop arms lose to the hold arms a second time?** Today's is n=1.
   This is the only question in this list whose answer is worth money.
6. **Does the roster hold at 43?** One bot left unattributably inside a six-day window. A second
   unexplained departure changes this from housekeeping to a control problem.
7. **Do the three UNEVALUABLE bots get a signed gate?** Nineteen sessions unevaluable. Nothing in
   the data will change this; only a ruling will.

## fire
AMBER — The GF family fired 7 of 7 and paired 6 as same-minute condors, which is the
cleanest entry record the family has produced. Against that: **both S2 champions were silent on a
GO day** (Δ% 0.4 and 0.31 against a 0.75 band), the ORB range broke with nothing fired, and three
bots remain unevaluable for want of a declared gate — unchanged for 19 sessions.

## strategy
AMBER — +$1,142 on $69,452 of risk today (1.6%), +$3,396 on $338,808 across the
seven-session window (1.0%). It is not GREEN because the mechanics audit shows **where the money
came from**: PR-01's three largest trades earned full credit by expiring unexited, and the 09-16
GF result flatters the no-stop arms on a single break (n=1). The one day in the window that a
short strike was genuinely tested — 09-08, −$4,199 — cost more than the other six made.
