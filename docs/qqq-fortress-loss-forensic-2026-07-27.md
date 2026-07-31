# QQQ-IC-0DTE-Fortress — loss forensic on the two −$4.8K days (2026-07-27)

> **Scope:** `QQQ-IC-0DTE-Fortress` only (paper). 41 closed positions, 36W/5L, closed P/L **−$1,834**,
> PF 0.83, avg win +$253 / avg loss −$2,185. Two positions account for essentially all of it.
> **Method:** ledger (`data/trades.csv`) + Tradier 5-min tape + BS re-pricing of each spread at the
> candidate exit moment (IV solved from the entry credit). Every counterfactual is an **optimistic
> bound** — fills at the modeled mark, no slippage (project law: live runs below model).

## 1. The finding in one line

**The exits that would have prevented both days already existed on this bot and stopped firing on
2026-06-12.** Nothing new needs inventing — a config regression needs reverting.

| Window | Positions | `status=closed` | `status=expired` | P/L |
|---|---|---|---|---|
| 2026-03-17 → 2026-05-21 | 30 | **29** | 1 | **+$2,975** |
| 2026-06-12 → 2026-06-26 | 11 | **0** | **11** | **−$4,809** |

Pre-June, closes land at PT50-consistent marks (e.g. 4/29 put: $0.40 credit × 31 → +$620 = exactly
50%) and at **15:50:00** on losers (5/19 −$754, 4/30 −$375, 4/29 −$62 — the time-exit capping the
day). The single pre-June "expired" position is 3/17 with a **$0.01** credit, where PT50 is sub-penny
and unfillable — a consistency check that PT50 was genuinely live.

From 2026-06-12 on, **every** position expires at 16:15. Not one early close, winners or losers.
The OA position panel still *shows* `PROFIT % 50%` and `EXPIRATION 10 minutes`; neither executed.
`data/bots_config.csv` already records the end-state ("bot Exit Options OFF … Monitors: none —
downside-naked, CONFIRMED", 2026-07-03).

**Cause — RESOLVED 2026-07-27 from the position Trades lists.** The June positions generated
**no exit orders at all.** Not sent-and-unfilled — never sent.

| Position | Trades list |
|---|---|
| **May 19** put (working) | `Open` 1:31PM Market filled $0.08 · `Close` 3:15PM **"Profit Taking: 50% of credit at $0.04"** limit 0.04 → **canceled** · `Close` 3:50PM **"Exit Trigger: Expires in 10 minutes"** Market → **filled $0.37** |
| **Jun 17** put | `Open` 1:31PM Market filled $0.32 — **and nothing else** |
| **Jun 24** put *and* call | `Open` 1:31PM Market filled $0.31 — **and nothing else** |
| **Jun 26** put | `Open` 1:31PM Market filled $0.13 — **and nothing else** |

May 19 shows exactly how the mechanic is supposed to work: OA sends a PT limit order when the target
comes into range, then at 15:50 cancels it and sends a **market** close. Neither event exists on any
June position.

**This refutes the expiration-timestamp hypothesis.** A 16:15-vs-16:00 basis drift would suppress the
15:50 exit — but it would not suppress the *PT order*, and the Jun 24 put marked **67.7% high**
(above its 50% target) with no PT order ever sent. Both mechanics are dead, so the exit conditions
were not attached to these positions at all.

**The `Exit Options` panel on a position is therefore not evidence.** It renders the automation's
*current* settings, not the conditions that were live on that position. The Trades list is ground
truth. `data/bots_config.csv` already captured the true state on 2026-07-03 — "bot Exit Options OFF
… Monitors: none — downside-naked, CONFIRMED."

**It is not an OA-wide failure — it is these two bots.** Account-wide check across all 16 bots in
`data/trades.csv` (ledger runs to 2026-07-02):

| Bot | Last early close | After 6/12: closed / expired |
|---|---|---|
| IC-SPX-FastPT25-S2-130PM | 2026-07-02 | **70 / 0** |
| IC-SPX-Fortress-Defang | 2026-07-02 | **13 / 0** |
| IC-SPX-FastPT25-S2 | 2026-07-02 | 14 / 20 |
| IC-SPX-Fortress-Unstopped | 2026-07-01 | 5 / 8 (unstopped by design) |
| **QQQ-IC-0DTE-Fortress** | **2026-05-21** | **0 / 11** |
| **QQQ-IC-0DTE-Fortress-NoPT50** | **2026-05-21** | **0 / 11** |

The two QQQ Fortress bots are the *only* ones that stopped exiting, they broke on the **same date**,
they resumed trading on the **same date** (6/12), they traded the **same 6 days**, and they **both
stopped entirely after 6/26** while the rest of the account traded through 7/2. Pre-5/22 their exit
record was near-perfect (Fortress 29 closed / 1 expired; NoPT50 24 closed / 0 expired).

**Andy reports making no edits.** Combined with the paired, same-date break, that points at account
state rather than configuration — most plausibly the billing lapse (memory:
*bots-kept-off-billing-error*, "lost a week of data"), which would have degraded these two bots'
exit conditions while leaving the SPX book intact. 6/12–6/26 is the **only** window these bots ran
post-incident, and it produced zero exit orders. Inferred, not proven — but it is the only
hypothesis consistent with every observation.

## 2. What actually happened on each day

**Jun 17** (open 735.19 · high 735.68 · low 720.85 · close 722.51) — **whipsaw, then real break.**
IC opened 13:31 @ 732.32; put spread 727/725, 29 ct, $0.32 credit, solved IV ≈ 51%.

- 14:00 — short 727 **touched** (bar low 726.92); 14:05 low 724.53 → *through the long strike*.
- Then a full reclaim to 735+ by 14:40. Put leg marks **+56.3% of credit at 14:45** (OA: "$522 high").
- 15:20 breaks 727 again and never returns. 15:50 @ 723.07 — already past both strikes.
- Settled 722.51 → full $2.00 width. **−$4,872.**

**Jun 26** (gap −1.29%, open 707.13 · high 715.56 · low 702.81 · close 706.52) — **last-10-minutes flush.**
IC opened 13:31 @ 714.10; put spread 709/707, 26 ct, $0.13 credit, solved IV ≈ 33%.

- 14:45 — short 709 touched (low 708.64), then reclaims and holds 709–711 for an hour.
- **15:50 → QQQ 710.87. Both strikes still OTM. The spread is worth ~$0.01–0.18.**
- 15:50→16:00 QQQ falls 711 → 704.88. Settles 706.52 — **$0.48 below the long strike**.
- Full width. **−$4,862.** Note the put leg's peak mark all day was only +15.4% of credit.

Both days classify **Trend** (`tape.json` label). Range075 measured at entry passed on both
(Jun 26 was −0.32% vs prior close at 1:31pm despite a −1.29% gap) — the filter is measuring the
wrong thing on gap-and-recover days. Separate issue; noted, not scoped here.

## 3. Counterfactuals — existing mechanics only

Put-leg P/L at each exit, priced at the modeled mark. IV-stress column shows the same exit repriced
with IV at 1.5–2× the solved level (vol pops when tape breaks — this is the honest downside).

| Mechanic | Built? | Jun 17 put leg | Jun 26 put leg |
|---|---|---|---|
| **Actual (ride to settlement)** | — | **−$4,872** | **−$4,862** |
| **PT50** (bot's own PT) | yes, on the position | **+$463** ✅ fires 14:45 | ✗ never reached (mfe 15.4%) |
| **15:50 time-exit** (bot's own) | yes, on the position | −$4,615 (−$3,791 @ 2× IV) — too late | **+$301** ✅ (+$126 @1.5× IV, −$130 @2× IV) |
| **S2 strike-touch close-all** | yes (live on SPX bots; **off here**) | −$1,574 (−$1,713 @1.5× IV) | −$1,558 (−$1,785 @1.5× IV) |
| SL100 (%-of-credit) | no | ≈ −$928 (fires ~14:00) | ≈ −$338 (fires ~14:45) |
| SL130 | no | ≈ −$1,206 | ≈ −$439 |
| Defang ($0.05 close-shorts) | on SPX-Defang | not modelable (needs premium path) | not modelable |

Call side both days was a full winner (+$899, +$175) and is unaffected by PT/time exits. **S2 is
close-all**, so it also closes the call side early — modeled at +$777 (Jun 17) and +$175 (Jun 26).

### Fill realism on PT50 (added 2026-07-27 — the May 19 log forces this)

May 19 proves the PT can be **sent and canceled unfilled**: target $0.04 on a $0.08 credit, no fill,
and the 15:50 market order cleaned up at $0.37. So "the mark reached 50%" ≠ "the PT filled."

Base rate from the 29 pre-June closed positions: **28 legs saw their mark reach ≥50% of credit; 25
of them filled the PT early (89%).** All three misses had a target of **≤ $0.06** (credits $0.01 /
$0.08 / $0.12) — thin-credit spreads where the target sits inside the bid/ask.

Jun 17's target was **$0.16 on a $0.32 credit**, and the mark traded two cents *through* it to $0.14.
That sits in the reliable bucket (cf. 4/29: $0.20 target on $0.40 credit, filled at exactly 50%).
So the **+$463** figure is *very likely* but not certain — call it an ~89% base rate, not a
guarantee. The 15:50 exit carries no such doubt: it is a **market** order and filled on every
pre-June occasion.

### Read
- **The two days fail in different places, and each is caught by a different one of the bot's own
  two exits.** Jun 17 was rescuable only *early* (PT50 at 14:45); by 15:50 the damage was done.
  Jun 26 was rescuable only *late* (15:50, still OTM); no PT was ever available.
- **Together, PT50 + the 15:50 time-exit rescue both days.** That is the configuration this bot was
  supposed to be running.
- **S2 is the only single rule that materially fixes both** (−$1.6K instead of −$4.9K, twice) — but
  it's second-best on each day individually, and it fires on a false break on Jun 17 (14:00 touch,
  full reclaim to 735). Worth noting the SPX production diagnostic already says the same thing:
  S2 caps the tail, the bleed is strike-touch frequency, not the hedge.
- **SL100/SL130 look best on paper but are the least trustworthy row.** They're priced at a
  threshold fill on a 0DTE spread that was gapping — SL-trigger slippage is the worst kind, and
  neither rung exists on this bot.

## 4. Bot-level impact

Restoring **PT50 + 15:50 time-exit** across all 11 June positions (winners get capped at 50% too —
this is the honest full-period restatement, not just cherry-picking the two losers):

| | Actual | Exits restored |
|---|---|---|
| June (11 positions) | **−$4,809** | **+$3,227** |
| Bot total (41 positions) | **−$1,834** | **≈ +$6,202** |

Swing **+$8,036**, of which +$10,499 comes from the two loss legs and **−$2,463 is the cost paid on
the nine winners** that would have been cut at 50% instead of expiring worthless. That give-back is
real and is exactly the ride-vs-cut question already queued in `docs/ic-trailing-stop-backtest.md` —
it does not change the conclusion here, because the loss side dominates by 4×.

15:50-time-exit **only** (no PT — winners keep full credit): June ≈ **+$611**. Positive, but Jun 17
still books −$4,615. The PT is what saves that day.

## 5. What to do

1. **Restore the exits, then verify against the Trades list — not the Exit Options panel.** The panel
   displayed `Profits: 50%, Expiration: 10 minutes` on all three broken positions. The only proof a
   position is protected is a **working PT order and/or a 15:50 exit-trigger row in its Trades list**
   (May 19 is the reference). Check the first new position intraday, not after the fact. Same check
   on `-NoPT50`, which shows the identical naked-to-settlement pattern.
   Corollary: **the 15:50 market exit is the load-bearing mechanic** — PT50 misses ~11% of the time
   and misses hardest on thin credits. Do not let the PT be the only thing standing between this bot
   and settlement.
2. **Quarantine the 6/12–6/26 rows for both QQQ Fortress bots.** They are execution artifacts, not
   strategy results. The bot's headline −$1,834 / PF 0.83 and NoPT50's "avg loss −$1,873" (noted in
   `bots_config.csv`) are both measuring a broken bot. Flag or exclude them in `report.py`, the
   readiness board, and `hedge_tournament.csv` before any of those numbers inform a decision.
3. **Add an execution-integrity check to `daily.sh`:** flag any day where a 0DTE bot with a
   configured time-exit produces `status=expired` legs. This failure was silent for 6 sessions and
   two −$4.8K days; the ledger already has everything needed to catch it on day one.
4. **Report it to OA with the position IDs.** The Exit Options panel rendering settings that
   produced no orders is a supportable bug, and the billing lapse gives them a place to look.
   Ask directly whether the lapse suspended exit conditions on these bots.
5. **Then** decide PT-vs-trail on the merits (the T1 batch), not under the pressure of a broken bot.
6. **Add a `time_exit_1550` arm to `scripts/hedge_tournament.py`.** It is currently the single
   highest-value missing rule — it's the mechanic that would have saved Jun 26, and the library
   can't see it. Also worth fixing the `s2` arm's cut pricing: it books the leg's **MAE**, which on
   Jun 17 models S2 at −$5,394 (worse than max loss). Price the cut at the *touch moment* instead.

## 6. Caveats
- All non-`ride` numbers are **optimistic bounds** — modeled marks, no slippage, no commission.
- Spread values are Black-Scholes with a single IV solved from the entry credit and held flat;
  the IV-stress columns bracket the error. 5-min tape grain, not a sub-second latch.
- Touch times come from 5-min bar lows; a sub-minute wick could move an S2 fire earlier.
- n = 2 losing days. This is a forensic, not evidence for a rule change. The config regression in
  §1 is the part that is established fact from the ledger; §3–4 are estimates.
