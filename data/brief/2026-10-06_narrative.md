# Narrative for the 2026-10-06 brief.
# Injected by scripts/render_brief.py into the slots of the same name.
# Sections: since-yesterday | convexity | lesson | tomorrow | fire | strategy

## since-yesterday
**Catch-up close.** Last close 2026-09-16; **13 trading days unobserved** (09-17 → 10-05).
Everything below about those days comes from closed-position rows in the 10-06 export. There is
**no tape, no p3 verdict and no roster state** for any of them (see **the gap**).

**The window, 09-17 → 10-06 (14 sessions): 172 legs, −$7,030 on $697,235 of risk (−1.0%).**
Two days account for all of it and more: **09-18 −$9,407** and **09-30 −$8,590** (−$17,997
together). The other twelve sessions made **+$10,967**. Cumulative working ledger:
**508 legs, 41 trading days, +$5,063 on $1,494,857 of risk.**

**Grading the 09-16 `## tomorrow` list:**

1. **Does PR-01 fire at 11:00?** — **YES, most days.** `IC-SPX-FastPT25-S2` fired on 11 of the
   13 missed sessions. It was silent today, and today's verdict is **JUSTIFIED**: SPX Δ% 0.77
   at 11:00 against the 0.75 band.
2. **If PR-01 fires two-sided, does the condor ride to 16:15 with no exit order?** — **The
   "rides" half held 5 of 5. The "at full credit" half FAILED on 09-30.** The five condors in the
   window where both sides were open at once (09-18, 09-25, 09-29, 09-30, 10-01) all held to
   expiry (09-18's settled 16:08). On **09-30** SPX closed at 7651.54, below the 7655 short put. The put side
   expired at **−$3,310**. That is the distribution the 09-16 narrative said the expiries were
   hiding (see `## lesson`).
   ⚠ **Refinement to the 09-16 partition.** PR-01 now has **10 ledger-paired trades (8 expired)
   and 28 single-leg trades (0 expired)**. The two paired trades that did *not* expire (09-24
   11:01/11:03, 10-02 11:08/11:10) are sides that filled **2 minutes apart**. The ledger pairs
   them as one trade (`PAIR_WINDOW_S`), but each one closed in 2–3 minutes while it was the
   bot's only open position. So the clean separation is by **"both sides open at the same time"**,
   not by the ledger's pairing label. That is still consistent with the `countpos == 1` cleanup
   rule.
3. **Does the 130PM arm ever produce a single-leg trade?** — **NO. 36 trades, 36 two-leg, 0
   single-leg.** The test of the cleanup rule remains unrun on this arm.
4. **Do all seven GF arms pair same-minute again?** — **NO, it is not a regime.** Today the
   call side filled at 13:35 and the put side at 13:56. Only Ride, Touch0 and Canary got a put
   at all. On 09-18 SL100 and SL200 got no call leg. Fill latency varies from session to
   session.
5. **Another band break: do the stop arms lose to the hold arms again?** — **YES on the put
   side, twice.** On **10-01** SL100 lost −$312 and SL200 −$676 on the put, while Ride/Touch0
   held to +$260/+$182. On **10-05** SL100 lost −$312 and SL200 −$520 on the call, while every
   holder closed at +$26. Together with 09-16 that makes **three of three** observed breaks.
   ⚠ **The counter-case is 09-18:** the call side ran through 719 to 720.06, and the holders
   took **−$2,548** each (Ride, PT50, Trail). The stop arms had no call leg that day, so there
   is no comparison. **n=3 one-directional, and the one day that would have cut against it is
   missing its comparison.** Still not a finding.
6. **Does the roster hold at 43?** — **YES.** Footer verbatim `43 active bots • 7 left in your
   plan`. AUTOS ON 18 / EXITS ON 16. **Drift ZERO** against the 09-16 bundle. ⚠ This compares
   two endpoints 14 sessions apart: a toggle flipped and restored inside the window reads as
   ZERO.
7. **Do the three UNEVALUABLE bots get a signed gate?** — **NO.** PR-07, PR-08 and PR-11 are
   still `gate_type=unknown`, now 33 sessions running.

**⭐ NEW — the 09-17 "Touch0 is not firing" claim is FALSIFIED as stated.** `R-2026-09-17` /
`gf-exit-spread-verification-2026-09-17.md` inferred from 27/27 identical Ride/Touch0 opens
that the live touch exit was almost certainly dead. On **09-18** `GF-QQQ-IC-Touch0`'s call
spread (short 719) **closed at 14:53 with QQQ at 719.13**, which is a strike touch. Ride's
identical leg rode to 15:50 at −$2,548, and Touch0 closed at **−$1,222**. It is the **only**
divergence in 39 shared Ride/Touch0 legs. **Revised claim:** the exit fires, but at about
1 in 39 live versus 69 of 353 days in the backtest. The rate gap stands; "dead config" does
not. ⚠ **OWED:** the Trades list of `GF-QQQ-IC-Touch0`, position opened 2026-09-18 13:36 ET,
to confirm that an exit order exists and which rule sent it. Ledger timing is a derivation,
not the surface.

**THE RED — `EXPIRY_RATIO_FLIP` on `IC-SPX-FastPT25-S2`, unchanged in substance from 09-16.**
It is the same onset (2026-08-31), now addressed as **`T01079`**. On 09-16 the same position
was `T00694`. **That is the renumbering defect flagged on 09-16, reproduced live:** one
position, a third ID. The verify is still **OWED** and is recorded by natural key:
`IC-SPX-FastPT25-S2`, position opened **2026-08-31 11:01 ET**.

**⭐ VERIFIES DISCHARGED — dated first-hand OA reads, 2026-10-06 ~16:45 ET (built-in browser,
Paper Trading, read-only; Trades lists from `/positions/closed`, bot log `?date=2026-09-30`):**
- **09-30, both S2 put legs → reading (a) CONFIRMED.** Both Trades lists hold **only the Open
  trade**: `Open 10 contracts - Sep 30, 2026 11:01AM` (PR-01) and `… 1:31PM` (130PM). There is
  no close order, rejected order or unfilled order. OA banner, verbatim: *"This position expired in-the-money.
  The close price and P/L is estimated based on the underlying price (7,651.54) at
  expiration."* The 130PM bot log for 09-30 ends at **3:55PM**, and the 3:55PM
  `Scalp-Mon-S2-StrikeTouch` run reads, for `SPX-7,665 put, +7,660 put`: *"Position underlying
  price is below short put strike price — **No**"*. SPX was above 7665, and so also above PR-01's
  7655, at the last monitor tick. **The breach came in the final 5 minutes, after the loop
  stopped.** StrikeTouch did not miss it. Neither position's worst marked loss before settlement got
  near the realized loss: PR-01 marked a low of −$330 (realized −$3,310), 130PM −$1,250 (realized
  −$4,750). **The 15:55 → 16:00 window is a structural blind spot with no exit on either S2
  arm.** That is a design property now, not a hypothesis.
- **09-18 Touch0 → CONFIRMED as the touch Exit Option.** The close trade reads verbatim
  `Close 26 contracts - Sep 18, 2026 2:53PM` · `Touch: OTM -$0.13` · filled at $0.55. The Exit
  Options panel shows `TOUCH $0 / 0 OTM` (intent only). The Trades-list label is the evidence.
- **08-31 RED onset (`T01079`) → DISCHARGED.** `IC-SPX-FastPT25-S2` opened 2026-08-31: put
  `Open … 11:01AM` and call `Open … 11:02AM`, and **no exit order on either side**. That answers
  the RED's question, *"is there an exit order at all?"*: **no**. The cause is the
  `countpos == 1` cleanup guard, not a dead exit engine.

**09-30 POST-MORTEM — added 2026-10-06 at Andy's request.** Day: **−$8,590 on $75,574 risk**;
the two S2 put legs are **−$8,060 (94%)**. Bot by bot (ledger `data/trades.csv`):

| bot | P/L | legs |
|---|---|---|
| `IC-SPX-FastPT25-S2-130PM` | **−$4,400** | put −$4,750 · call +$350 |
| `IC-SPX-FastPT25-S2` | **−$3,210** | put −$3,310 · call +$100 |
| `GF-QQQ-IC-Touch0` / `-Ride` | −$338 each | call −$286 · put −$52 |
| `QQQ-IC-0DTE-Fortress-NoPT50` | −$302 | call −$250 · put −$52 |
| `GF-QQQ-IC-SL100` / `-SL200` / `-PT50` | −$52 each | put only |
| `GF-QQQ-IC-Canary` (1ct) | −$8 | |
| `Nigiri` / `3DTE` / `ORB` / `GF-Trail` | +$20 / +$40 / +$50 / +$52 | |

**Cause: a closing sell-off that landed after the monitors stopped.** Tradier 1-minute SPX
bars (pulled 2026-10-06 into a scratch root, not the repo): 7,687 at 15:45 → low 7,666.02 at
15:54 → **15:55 low 7,662.95** (the 130PM short 7665 first breached) → back to 7,665–7,667 at 15:56–57 →
15:58 low 7,662.66 → **15:59 low 7,652.9** (PR-01 short 7655 first breached) → settle 7,651.54.
The 3:55PM StrikeTouch run read "not below" (see VERIFIES above). It evidently evaluated at
the minute's open, near 7,666. The QQQ arms all closed at or before about 15:50 with no strike
threatened.

**Why it cost so much:** (1) the paired S2 condors have no exit after 15:55. (2) The payoff is
asymmetric: the 130PM put collected $250 against $4,750 at risk (~1:19), so one breach erases
~16 typical winning days. (3) The strikes were close: the 130PM short put was 0.45% below SPX at
entry, and PR-01's 0.75%. **Counterfactual, estimated and not measured:** a Touch Exit Option
(checked each minute to 15:59) would likely have closed the 130PM put on the 15:55–58 dips. Its
three prior breach closes cost −$1,750 to −$2,250, against −$4,750 here. PR-01's breach falls
only inside the 15:59 minute, so it is a coin-flip whether any exit fires in time. Any such
change to OA bot behavior is gated (`CLAUDE.md` §5 standing exception).

**THE GAP.**
- **No tape for 09-17 → 10-05.** `2026-10-06_tape.json` covers 10-06 only. Both loss days
  (09-18, 09-30) have P&L and fill times and **no market context**.
- **No p3 verdicts and no roster state per day** for the 13 missed sessions. Silences on those
  days were never adjudicated and now cannot be.
- **No OA bot logs.** Every exit attribution here is inferred from ledger timestamps.
- **Pre-window rows moved.** Rows opened before 09-17 now read 336 legs / +$12,093 / $797,622
  risk, against the 09-16 narrative's 333 / +$11,945 / $790,834. That is +3 legs and +$148,
  most likely multi-day positions open at the 09-16 export that closed later. Not reconciled
  row by row.

## convexity
**A clean loss for the long-vol case today.** VIX opened 15.50 against a 15.52 prior close, made
its high of 15.54 at 10:00, bottomed at 14.96 at 12:40 and settled at **15.01 (−3.29%)**,
range 3.9%. SPX gapped up (+0.41% open) and closed **+0.58%** on a 0.49% range. No structure
that pays on a vol expansion earns anything on this tape.

**The window's two loss days are the ones that matter, and the tape for them is missing.** 09-18
and 09-30 are the two sessions in this log where a short strike was crossed and held. Whether VIX
moved enough on either day to fund an overlay is **unknowable from this close**. The
convexity series still has **one ambiguous day (09-16), several clean losses and two blank
pages** where the answer was. An overlay exit rule is still unspecified.

## lesson
**The warning in the 09-16 lesson came due on 09-30.**

On 09-16 this log said PR-01's best trades earned full credit because no exit order was ever
generated, and that this was "an untested short gamma position running to settlement." On
**09-30** both S2 arms held a paired condor with no exit, and SPX closed below both short puts:

| arm | short put | SPX close | put leg | trade |
|---|---|---|---|---|
| `IC-SPX-FastPT25-S2` | 7655 | 7651.54 | **−$3,310** (expired) | −$3,210 |
| `IC-SPX-FastPT25-S2-130PM` | 7665 | 7651.54 | **−$4,750** (expired, max loss) | −$4,400 |

**−$8,060 from two legs**, against +$100/+$350 on their call sides. That is roughly what 16
average full-credit 130PM expiries earn.

**What the ledger cannot settle is why no breach exit fired.** The 09-16 refined rule
(*StrikeTouch closes a breached leg regardless of count, but only while the monitor loop
runs*) has fresh support. StrikeTouch-shaped closes landed at **14:54 on 09-18** (130PM call,
SPX 7646.71 vs 7645 short) and **15:15 on 10-05** (130PM call, 7790.35 vs 7790), both inside
the session. On 09-30 both legs' `mae_date` reads **15:55**, which is the last 5-minute tape
bar, so the breach time cannot be resolved from the ledger. Two readings fit:
**(a)** SPX crossed after the monitor loop stopped, which is C-2 and benign as mechanics but
leaves a known blind window into settlement. **(b)** It crossed earlier and StrikeTouch missed
it, which is a live exit defect on the champion. **They predict different Trades lists**, and
that is the cheapest check this brief can name.

And **09-18** is the same lesson on the GF side. The call breach cost the holders −$2,548 each,
and the one arm that left early (Touch0, 14:53) lost half that. Holding beats stopping on
breaks that revert (09-16, 10-01, 10-05). It loses on the break that doesn't. **The fleet has
no instrument that knows which kind of break it is in**, and the two worst days of the program
are both the kind that doesn't revert.

## tomorrow
1. ✅ ~~09-30 Trades lists~~ **DISCHARGED 10-06: reading (a), the breach came after the 15:55 loop end.**
   **Decision for Andy (gated, OA bot behavior):** does either S2 arm get a pre-15:55 exit for
   paired condors? Riding the last 5 minutes is the risk that cost $8,060 on 09-30.
2. ✅ ~~09-18 Touch0~~ **DISCHARGED: `Touch: OTM -$0.13`.**
3. ✅ ~~T01079 / 08-31~~ **DISCHARGED: no exit order on either side.**
4. **Does 130PM ever produce a single-leg trade?** 0 in 36.
5. **Next break: does the 3-for-3 hold-beats-stop pattern meet a non-reverting break where
   both have legs?** That comparison is the one the data is missing.
6. **Close cadence.** Fourteen sessions without a close cost the tape, the verdicts and the
   roster history for both loss days. That is a process finding, not a bot one.

## fire
AMBER — Today: 12 legs across 8 bots. PR-01's silence is JUSTIFIED (Δ% 0.77 vs 0.75). The GF
family fired 7 of 7 but split-sided again (call 13:35, put 13:56, put on 3 arms only). Against
that, **two SUSPECTs**: the ORB range broke (SPX 7836.17 at 11:05 vs 7835.09 top) with nothing
fired, and INC-01 has no declared gate. Three bots remain UNEVALUABLE for want of a signed
entry condition. Across the window PR-01 fired on 11 of 13 missed sessions, which is not a
fire problem.

## strategy
RED — Today +$1,620 on $49,873 (3.2%), but the window is **−$7,030 on $697,235 (−1.0%)**.
**Two breach days cost $17,997, more than the other twelve sessions made.** 09-30 is the
failure mode named on 09-16, now realized: an S2 condor with no exit held through a breach to
settlement, −$8,060 on two legs. Until the 09-30 Trades lists say whether an exit should have
fired, the S2 arms' expiry income should be read as **premium collected against an uncapped
late-session tail**, not as edge.
