# Narrative for the 2026-08-19 brief.
# Injected by scripts/render_brief.py into the slots of the same name.
# Sections: since-yesterday | convexity | lesson | tomorrow | fire | strategy

## since-yesterday
Four questions were carried in from the 08-17 brief. Three now have answers, and the first is
the headline of the day.

- **Will the GF call side ever fill?** **YES — first time ever.** Seven of eight arms sold a 720 call spread at 13:52. Before today the call side had never filled, on any arm, on any day.
- **PR-01 champion fires, or misses twice?** **Fired** — one put spread at 13:31, flat. It broke the 08-17 silence, but single-sided and at $0.
- **Ride-Delta double-fills again?** **Yes, third time** (08-14, 08-17, 08-19). Two put spreads at 13:33, both short 712, and no call side at all — alone among the eight arms.
- **A day where delta and pct imply different strikes?** **Not yet.** Short put 712 again. Layer 2 stays unresolved, four sessions running.
- **PR-04 still floored?** **Not evaluable** — the credit-floor value is still unrecorded.

## convexity
**No long-vol overlay would have paid today.** VIX fell 6.0% (15.84 to 14.89) and every convexity
structure available would have bled. Log it as a day **against** the long-vol case — the empirical
argument is built by accumulation, and honest accumulation includes the days on the other side.

## lesson
**The fleet got a nearly perfect day for its strategy and earned $354 on $21,940 of risk — 1.6%.**
Directionality 0.084, 43 reversals in 79 bars, every single bar inside the ±0.75% GO band, and not
one short strike approached within 0.45%. If the greenfield book cannot produce a meaningful number
on a day like this, the constraint is not the market and it is not the filter. It is size, and it is
structure.

Look at where the $354 came from: **$550 from one bot** (130PM, the only true condor opened today),
**−$320 from one bot** (the directional), and **$74 total across all eight greenfield arms** — the
entire experiment the program is built around. Eight arms, a full clean session, seventy-four
dollars. The arms are not wrong; they are not sized to say anything. That is the roster board's
finding reached from the other direction: zero of eighteen bots has reached its sample target, so
every number on the fleet — including today's — is still noise being read as signal.

**The call side filling is worth more than the $354.** It is a mechanism discovery, not a P/L event.
But note what it did **not** do: the put spread filled at 13:33 and the call at 13:52, nineteen minutes
apart, two separate `trade_id`s, `single_sided=True` on both rows. That is two positions, not one
condor. Eight arms, eight sessions, **zero condors**. The old hypothesis — "the call leg never
fills" — is dead. The narrower one that replaces it: **the two sides fill as separate events**, and
if that is permanent, the n=100-**condor** sample targets are unreachable as written.

## tomorrow
1. **Does the call side fill again, or was 08-19 a one-off?** One occurrence is not a pattern.
2. Do the two sides ever fill as a **single** condor, or is separate-event filling the permanent shape? This decides whether the n=100-condor targets are reachable at all.
3. Ride-Delta: fourth consecutive double-fill?
4. A day where delta and pct imply different strikes — still waiting, four sessions.
5. PR-01 champion: two fills in a row, or back to silence?

## fire
AMBER — Entries landed inside the GO band and the call side filled for the
first time. Against that: Ride-Delta double-filled a third time, and four of seven silent bots are
unevaluable for want of a declared gate.

## strategy
AMBER — Correct process, negligible outcome. One clean directional loss
with the stop working exactly as designed — `DIR-SPX-CallVIXdrop` lost $320 of $640 risk in 28
minutes on a VIX drop of 6.0% that SPX simply did not follow. Gate satisfied, bet wrong. No
counterfactual replay exists yet.
