# QQQ-IC-0DTE-Range075-PT50-Wide2-1230PM — Execution Forensic

*Audit date 2026-07-27 · bot status OFF · positions 2026-03-24 → 2026-05-22*

**Declared:** exit = PT50 | hedge = `<verify>` — **blank in config** | entry = 12:30, Range075 filter, 0.75% OTM, $2 wide | sizing = 1 contract, ~$160–195 risk/leg | reentry = `<verify>` — **blank in config**

**Ledger:** 40 positions, 6 losses, P/L **+$78**, Exp(R) **+0.0108**, 23 trading days

**Verdict:** **MIXED — PT50 works perfectly on the put side and was never attached to the call side.** [Put-side PT50 CONFIRMED firing 21/21. Call-side non-attachment INFERRED (strong) from 17/17 population evidence.] **Flag: 40 positions over 23 days — far below the ≥100-trade / ≥6-month bar. This bot is OFF and none of this authorises restarting it.**

---

## Findings, most severe first

### F1 — PT50 is attached to the put side and NOT to the call side
The split is total and leaves no room for a market explanation.

| | Put side (n=23) | Call side (n=17) |
|---|---|---|
| Closed **mid-session** at a PT50 price | **21** | **0** |
| Closed at the **15:50** time exit | 2 | **17 — all of them** |
| Reached ≥50% profit at some point | 21 | **15** |
| …of which ≥50% was reached **before 15:00** | — | **9** |
| PT50 fired | **21 / 21 reachable** | **0 / 15 reachable** |

**The put-side signature is unmistakable: `mfe_date` equals `close_date` on all 21 fills.** The position's best moment *is* the moment it closed — that is what a working profit target looks like, and it happens 21 times out of 21, at times scattered from 12:52 to 15:35.

**The call side never does it once.** Fifteen call spreads reached 50%+ profit — nine of them before 15:00, several hours of runway — and every one rode to the 15:50 time exit instead. Six reached **100%** (premium decayed to zero) and still were not closed by PT50.

Worst case: **2026-04-07**, a call spread that hit **100% profit at 14:51** and was closed at 15:50 for **−$5**. A full winner turned into a loss by sitting there.

**Cause: `settings` [INFERRED — strong].** Two scanners, two independent Open Position actions, two independent Exit Options configs — and the call-side one has no profit target. Benign explanations ruled out:
- *by_design* — no. `bots_config` declares PT50 for the bot, not for one leg.
- *market_unfillable* — no. Six call spreads decayed to $0.01–0.02 against PT50 targets of $0.035–$0.09. Those are inside the market by a wide margin, for hours.
- *Bid-Ask Guard* — no. It would have to trip on the call side and never on the put side, on the same underlying, on the same 17 days.
- *oa_execution* — **actively contradicted by this bot's own put side**, which fired 21/21 on the same platform, same account, same day, same 1-minute evaluation loop.
- *tick granularity* — partially real (PT50 on a $0.07 credit = $0.035, and QQQ quotes in pennies), but it cannot explain positions that traded down to $0.01.

**Evidence that would settle it:** the Exit Options panel of the **call-side** Open Position action (the `Scan-Call` equivalent). One screenshot converts this to CONFIRMED.

### F2 — Every one of the 40 positions settled worthless. The bot captured 17% of what was there.
| | Actual | Held to settlement | Delta |
|---|---|---|---|
| Put side (n=23) | +$52 | +$270 | **+$218** |
| Call side (n=17) | +$26 | +$183 | **+$157** |
| **All 40** | **+$78** | **+$453** | **+$375** |

**40 of 40 positions — 100% — expired with the short strike untested at the close.** Not one position in this bot's entire history was going to lose money at settlement. The bot's exits converted $453 of available profit into $78.

And it follows that **all six "losses" are exit artifacts, not market outcomes:**

| Date | Side | Short K | QQQ close | Actual | Held |
|---|---|---|---|---|---|
| 4/23 | put | 651 | **651.42** | −$63 | **+$7** |
| 4/30 | call | 669 | **667.74** | −$35 | **+$7** |
| 3/30 | put | 557 | **558.28** | −$20 | **+$11** |
| 4/29 | call | 663 | **661.57** | −$10 | **+$42** |
| 5/21 | call | 715 | **714.51** | −$9 | **+$8** |
| 4/07 | call | 589 | **588.59** | −$5 | **+$18** |
| **Total** | | | | **−$142** | **+$93** |

**Adversarial reading — do not act on this.** A 40/40 settlement record over 23 filtered days is exactly what a 0.75%-OTM 0DTE spread entered at 12:30 on a calm-tape filter *should* produce. It is not luck, and it is not edge — **it means this sample contains zero instances of the tail the exits exist to protect against.** A sample with no breach days cannot price breach insurance. One QQQ gap-through at ~$190 max loss erases half the $375, two erase all of it. The $375 is the *observed premium paid* for protection, not evidence the protection is mispriced.

### F3 — The 15:50 exit is real, costly on this sample, and absent from the config
Nineteen of 40 positions closed at exactly 15:50, including all six losses. This is the "flat by 3:50 PM" hard exit from the build checklist (`oa-platform-reference.md` §15, item 9). It is **not recorded anywhere in `bots_config.csv`** — the config lists only `profit_target: PT50`.

Unlike Bot 1, this matters materially here: **QQQ is a physically-settled ETF.** An ITM short leg at expiry means real share assignment, not a cash debit. The 3:50 flat rule is assignment protection — a categorical risk control, not a P/L optimisation. Its cost on this sample is measurable ($157 on the call side). Its benefit is **unmeasurable from a sample with zero ITM finishes.**

I am recording the cost. I am explicitly **not** suggesting the rule is wrong.

### F4 — The two blank config fields, filled from behaviour
| Field | Config | Observed across 40 positions | Confidence |
|---|---|---|---|
| `stop_or_hedge` | `<verify>` | **NONE.** 21 mid-session closes, **all profitable**; **all 6 losses closed at 15:50**. No stop, no touch hedge, no defensive exit ever fired. | High — behaviourally conclusive |
| `reentry` | `<verify>` | **0.** Max 1 entry per side per day; **zero** days with a second same-side entry across 23 days. | High |

Because there is no loss-side mechanic at all, **section B of the per-position schema has no subject on this bot.** The ledger is capable of showing a hedge fire (it does on Bot 1) and shows none here.

### F5 — Range075 on 2026-03-30: indeterminate, not a breach
QQQ opened **+0.853%** from the prior close (562.58 → 567.38), outside the ±0.75% band, and the bot traded. That looks like a filter breach.

**It probably is not.** The gate evaluates `% change since previous close` **at scan time (12:31)**, not at the open. QQQ fell all day — range 555.60–568.05, close 558.28 — so by 12:31 it was very likely back inside the band. **I cannot reconstruct the 12:31 level:** Tradier's 5-minute history does not reach back before 2026-05-29, and this date is two months outside that window.

**UNKNOWN.** Recorded so it is not mistaken for a clean pass, and not asserted as a breach. The evidence is permanently unavailable.

---

## What this bot says about Bot 1 — a caveat against my own conclusion
On Bot 1 I concluded PT25 was attached and generated no orders — `oa_execution`, CONFIRMED. **This bot's put side fires the same OA profit-target mechanic 21 times out of 21, in the same account.** That is useful two ways:

1. It **rules out a platform-wide defect.** OA's `Profit Taking %` exit option demonstrably works. Bot 1's failure is specific to Bot 1.
2. It **slightly raises the prior on Bot 1's one residual caveat** — that PT25 was added to `Scalp-Scan-Put` recently rather than being live-and-broken since June. A mechanic that works everywhere else failing 47 times in one bot is a stronger anomaly than I framed it. It does not change the verdict — the Exit Options editor shows PT25 attached today and the Bid-Ask Guard off — but it raises the value of the automation change-history request from "nice to have" to "worth chasing."

---

## Position log

### `2026-04-23 | shortputspread | 651/649 | 1ct | cr $0.07 | −$63 | R −0.326`
- **A) Exit:** PT50 → **N/A** — `mfe 0.14`, never within reach. Correct non-fire.
- **B) Hedge:** declared blank; none exists on this bot (F4). No subject.
- **C) Cause:** `by_design` **[INFERRED]** — closed 15:50 by the time exit. *Ruled out:* oa_execution (nothing was due to fire); market_unfillable; filter gating (QQQ open −0.238%, inside band); config staleness (the 15:50 rule is absent from config — F3). **Evidence that would change this verdict:** confirmation the 15:50 exit is a configured rule rather than a manual/other close.
- **D) If declared logic worked:** no declared rule was due to fire; **−$63** stands.
- **E) Best alternative:** **ride +$7** (R +0.036). Largest single R in the set — QQQ dipped to 645.52 intraday, well through the 651 short, then recovered to close at **651.42**, above it. Classic intraday breach that repaired. No preemption.

### `2026-04-30 | shortcallspread | 669/671 | 1ct | cr $0.07 | −$35 | R −0.181`
- **A) Exit:** PT50 → **NOT FIRED** — reached **57%** profit at **12:57**, under three minutes after entry, and held to 15:50.
- **B) Hedge:** no subject.
- **C) Cause:** `settings` **[INFERRED — strong]** — call-side Open action has no PT attached (F1). *Ruled out:* market_unfillable (target $0.035 against a spread that traded to $0.08/$0.03 on the legs); oa_execution (put side fired 21/21).
- **D) If declared logic worked:** **+$4** (R +0.021), delta **+$39** — PT50 fill at $0.035 around 12:57. *Optimistic bound; $0.035 is not a penny tick, so a real fill needs $0.03.*
- **E) Best alternative:** **ride +$7** (R +0.036); runner-up PT50 +$4. Ride beats the declared exit here. No within-position preemption (`mae_date 15:45` is after `mfe_date 12:57`).

### `2026-03-30 | shortputspread | 557/555 | 1ct | cr $0.11 | −$20 | R −0.106`
- **A) Exit:** PT50 → **N/A** — `mfe 0.45`, just short of the 50% threshold. Correct non-fire, and a real near-miss.
- **B) Hedge:** no subject.
- **C) Cause:** `by_design` **[INFERRED]** — 15:50 time exit. **Filter status UNKNOWN — see F5.** *Ruled out:* oa_execution; market_unfillable.
- **D) If declared logic worked:** no declared rule was due to fire; **−$20** stands.
- **E) Best alternative:** **ride +$11** (R +0.058). QQQ low 555.60 pierced the 557 short, closed **558.28** above it. No preemption.

### `2026-04-29 | shortcallspread | 663/665 | 1ct | cr $0.42 | −$10 | R −0.063`
- **A) Exit:** PT50 → **N/A** — `mfe 0.12`. Correct non-fire.
- **B) Hedge:** no subject.
- **C) Cause:** `by_design` **[INFERRED]** — 15:50 time exit. *Ruled out:* oa_execution; filter gating (open +0.164%, inside band).
- **D) If declared logic worked:** no declared rule was due to fire; **−$10** stands.
- **E) Best alternative:** **ride +$42** (R **+0.266**) — **the largest recoverable R on this bot.** The biggest credit in the set ($0.42) was closed at $0.52 for a loss while it was heading to zero; QQQ closed 661.57 against a 663 short. No preemption.

### `2026-05-21 | shortcallspread | 715/717 | 1ct | cr $0.08 | −$9 | R −0.047`
- **A) Exit:** PT50 → **N/A** — `mfe 0.38`. Correct non-fire.
- **B) Hedge:** no subject.
- **C) Cause:** `by_design` **[INFERRED]** — 15:50 time exit. *Ruled out:* oa_execution; filter gating (open −0.583%, inside band).
- **D) If declared logic worked:** no declared rule was due to fire; **−$9** stands.
- **E) Best alternative:** **ride +$8** (R +0.042). QQQ high 717.12 went through both strikes, closed **714.51** below the short. No preemption.

### `2026-04-07 | shortcallspread | 589/591 | 1ct | cr $0.18 | −$5 | R −0.027`
- **A) Exit:** PT50 → **NOT FIRED** — reached **100% profit at 14:51** (premium to zero) and closed at 15:50 for a loss. **The single most damning position on this bot.**
- **B) Hedge:** no subject.
- **C) Cause:** `settings` **[INFERRED — strong]** — F1. *Ruled out:* market_unfillable (the spread was worth ~$0.00 with an hour to run); oa_execution (put side fired 21/21); Bid-Ask Guard (would have to be call-side-only).
- **D) If declared logic worked:** **+$9** (R +0.049), delta **+$14** — PT50 fill at $0.09. *Optimistic bound.*
- **E) Best alternative:** **ride +$18** (R +0.099); runner-up PT50 +$9. No preemption (`mae_date 13:37` precedes `mfe_date 14:51`, but mae was only −0.61 — no loss-side rule exists to fire anyway).

---

## Open evidence requests
1. **Exit Options panel of the CALL-side Open Position action.** Converts F1 from INFERRED to CONFIRMED. One screenshot.
2. **Confirmation that the 15:50 flat exit is a configured rule** — an Expiration/time Exit Option or a scheduled event — and where it lives. It drives 19 of 40 closes and appears nowhere in `bots_config.csv`.
3. Nothing else. F5 is permanently unresolvable (5-minute history expired).

**Config record should be updated** — `stop_or_hedge: none`, `reentry: 0`, and the missing 15:50 exit — but per the audit's terms I am not editing `bots_config.csv`; that is a config change, not a forensic finding.

---

## Fleet-level running table

| Bot | Verdict | Confirmed execution failures | $ recoverable | $ explained by strategy |
|---|---|---|---|---|
| **IC-SPX-FastPT25-S2** (post-fix) | **Execution-broken** — PT25 dead; entry, S2 firing + scanner gates clean | PT25 non-firing (CONFIRMED, bot-wide) · orphan-loop race (CONFIRMED) · Cleanup on Market (CONFIRMED, unremediated) · 1 structural artifact | $3,000 artifact · +$11,922 if PT25 ran *(optimistic bound)* · $305 churn | −$3,285 S2 whipsaw cost |
| **QQQ-Range075-PT50-Wide2-1230PM** | **Mixed** — PT50 perfect on puts, absent on calls | 0 platform failures; **1 config gap** (call-side PT50, INFERRED strong) | **+$375** total exit drag *(optimistic bound; sample has zero tail events)* · of which **+$157** call-side | **$0** — no loss in this bot's history was a market outcome; all 40 settled worthless |
| **DIR-SPX-PutVIX22-SL75** | **Clean but untested** — non-trading fully explained; bot health unverified | 0 | $0 | $0 — nothing traded, nothing learned |
| QQQ-IC-0DTE-HedgeD-Conditional | *blocked — declared exit is blank in config* | — | — | — |

---

### Data provenance
Ledger `data/trades.csv`. QQQ daily OHLC and expired-option daily OHLC (OCC symbols) via Tradier `/v1/markets/history` — settlement values for all 40 positions computed from QQQ closes against short strikes. No 5-minute tape exists for any date in this bot's range (Tradier window begins 2026-05-29; this bot's last position is 2026-05-22), so all intraday timing is taken from the ledger's OA-sourced `mfe_date`/`mae_date`, not modelled. No OA screenshots were supplied for this bot.
