# QQQ-IC-0DTE-HedgeD-Conditional — Execution Forensic

*Audit date 2026-07-28 · bot status OFF · positions 2026-03-19 → 2026-05-22 · automation screens supplied by operator*

**Declared (config):** exit = `<verify>` | hedge = "Conditional" | entry = `<verify>` | filter = `<verify: Range075>` | reentry = `<verify>`

**Declared (project doc, `oa-platform-reference.md` §14):** *"Conditional trigger — close the tested spread only after price is **sustained ~$1 past the strike for ~10 minutes** (a monitor with a time-persistence condition)."*

**Ledger:** 86 positions, 16 losses, P/L **−$15,376**, Exp(R) **−0.0367**, 45 trading days

**Verdict:** **EXECUTION-CLEAN, DESIGN-BROKEN, AND MIS-DOCUMENTED.** [Every automation executed exactly as built — CONFIRMED from the automation trees. But two of the four things the config claims about this bot are false.] Nothing here is OA's fault. **Flag: 86 positions / 45 days is below the ≥100-trade, ≥6-month bar.**

---

## Findings, most severe first

### F1 — The "Conditional" hedge has no conditional in it
Both monitors — `HedgeD-Mon-Cond-PutBreach` and `HedgeD-Mon-Cond-CallBreach` — are identical:

> `Repeat for each position` → `Position has tags: put side` → **`Position is more than $1 in the money`** → **`Position has been open 30 minutes or more`** → `Close Position`

The second gate is **position age**, not breach persistence. Entry is 11:00, so from 11:30 onward it is **permanently true**. There is no time-persistence condition anywhere in either tree.

**What the project believes it tested:** close only after price is sustained $1 past the strike for ~10 minutes.
**What actually ran:** close on the **first minute** QQQ is $1 in the money, any time after 11:30.

These are different mechanics. The bot is an **immediate $1-ITM stop** wearing the name "Conditional."

**Confirmed by the fills.** $1 ITM on a $2-wide spread means $1.00 of intrinsic value. Thirteen of the sixteen losses exited between **$0.91 and $1.07** — mean $1.012, standard deviation $0.054. That is the mechanic's signature written directly into the exit prices, and it rules out the alternatives: exit price does *not* fall as quantity rises (`corr = +0.46`, so not a fixed-dollar stop) and does not scale with credit the way a percentage stop would.

**Cause: `settings` [CONFIRMED].** *Ruled out:* by_design (the doc specifies a sustain condition the tree does not contain); oa_execution (both monitors fired correctly every time the gates were true); market_unfillable (all 13 filled); data_error (fills reconcile to $1 intrinsic exactly).

**The consequence is bigger than this bot.** `HedgeD-Conditional` is one arm of the QQQ hedge tournament — the experiment meant to settle *which hedge* the fleet should use. **The Conditional arm never tested the conditional mechanic.** Any tournament conclusion that names Conditional as tested is invalid.

**I cannot tell you what the real Conditional would have done.** Modelling a 10-minute sustain requires intraday tape, and Tradier's 5-minute history begins 2026-05-29 — this bot's last position is 2026-05-22. **That evidence is permanently gone.** The genuine mechanic remains untested and now untestable on this data.

### F2 — There is no Range075 filter on this bot
`HedgeD-Scan-Put` and `HedgeD-Scan-Call` in full:

> `Loop QQQ` → `FOMC Meeting today` **No** → `Current market time is after 11:00am` **Yes** → `Bot opened a position with [put/call] side today` **No** → `Open QQQ Short [Put/Call] Spread`

Four nodes. **No `Symbol change % greater than −0.75`. No `Symbol change % less than 0.75`.** Compare the champion's `Scalp-Scan-Put`, which carries both.

`bots_config.csv` records `filter: <verify: Range075>`. The answer is **no filter exists.** This bot takes a trade every single day the market is open and it hasn't already traded that side.

**Consequence:** **16 of its 45 entry days (36%) opened outside the ±0.75% band** — including 2026-03-23 at **+1.45%** and 2026-03-31 at +1.08%. Five of those sixteen days produced losses. A Range075-filtered version of this bot would not have taken them.

**Cause: `settings` [CONFIRMED]** — direct observation of the automation tree.

**RESOLVED in the Addendum (A1):** all four hedge bots carry the identical filter-free scanner, so the tournament **is** matched on entries and F3 is not confounded by this. But the documentation error is fleet-wide — none of the four is a Range075 bot.

### F3 — The sibling comparison: Conditional is the worst hedge in the family, and worse than no hedge at all
42 matched days, identical entries, identical sizing (26 contracts, $392,248 total risk each for the four hedge bots).

| Hedge | P/L | **Exp(R)** | Losses | Read |
|---|---|---|---|---|
| **S3 (50% max-loss stop)** | −$1,103 | **−0.0029** | 39 | **Best.** Cuts often, cuts small |
| S2 (close whole IC on touch) | −$3,652 | −0.0095 | 42 | Second |
| **Raw — no hedge at all** | −$303 | **−0.0211** | 15 | Third by R |
| S1 (close tested spread) | −$10,104 | −0.0260 | 15 | Fourth |
| **D — "Conditional"** | **−$11,994** | **−0.0308** | 14 | **Worst** |

**Conditional is worse by R than not hedging at all.** Head-to-head against S2 it wins **29 of 42 days** and still loses **$8,342** cumulatively — the classic wins-small-often, loses-huge-rarely signature, the same shape as the champion's.

Why: a $1-ITM trigger on a $2-wide spread fires at **50% of maximum loss**. The mechanic waits until half the damage is done, then locks it in. It fires rarely (14 losses vs 39–42 for S2/S3) and each fire costs ~$2,237.

*Caveat on Raw:* it is sized at 1 contract / $186 risk versus 26 contracts / $4,900 for the hedge bots — a 26× difference. **Its dollar figure is not comparable; only its R is.** The four hedge bots are directly comparable on both.

### F4 — This is the fleet's only trustworthy hedge sample, and it contains real tail events
Unlike Bot 2 (40 of 40 settled worthless, zero breaches), this sample has genuine two-sided evidence: **13 of 86 positions finished in the money.** Among the 16 losses, **7 recovered to settle worthless and 9 finished ITM.**

That means the hedge's cost and benefit are both measurable here:

| | Positions | Effect |
|---|---|---|
| Hedge **helped** (position finished deep ITM) | 6 | **saved $10,277** |
| Hedge **hurt** (position recovered by the close) | 10 | **cost $18,710** |
| **Net** | 16 | **cost $8,433** |

The mechanic is not useless — on 3/31 it saved $2,511, on 4/07 $2,660, on 3/26 $2,565. It simply pays out less than it costs at this trigger level. **That is a far more credible finding than anything in Bot 2**, because the sample actually contains the disaster the hedge exists to prevent.

Bot-level: actual **−$15,376** vs ride-to-settlement **−$645**, delta **+$14,731**. But 13 positions did finish ITM, so ride is a genuine risk position here, not the free lunch it appeared to be on Bot 2.

### F5 — The Expiration exit uses Market pricing
Both scanners' Exit Options carry `Expiration: 10 minutes before` with **`PRICING: Market`**. This is the 15:50 exit, and it accounts for 3 of the 16 losses.

Same unremediated pattern as the champion's Cleanup automation (Bot 1, F6). Lower stakes here — $2-wide QQQ spreads at 15:50 quote tightly — but it is the same configuration choice that cost $3,000 on SPX on 6/11. Recorded, not recommended.

### F6 — What the automations got right
Worth stating plainly, because it is the only clean architecture in the audit:

- **PT50 is attached to BOTH sides** — `Profit Taking %: 50% of credit`, pricing Normal, on both `Scan-Put` and `Scan-Call`. Bot 2 had it on the put side only. Here it works: **69 of 70 winners closed at their own MFE timestamp.**
- **The re-entry gate is built correctly.** It checks `Bot opened a position with [side] today` — a per-day flag, not a live position count. **This is why HedgeD cannot suffer the champion's 7/01 orphan loop:** once a side has traded, it is locked out for the day regardless of what closes. Ledger confirms: max 1 entry per side per day, **zero exceptions across 45 days**. The champion should be built this way.
- **Zero strike-geometry defects** — 0 of 86 malformed. `current-state.md`'s blanket *"QQQ hedge family is strike-bug contaminated"* does **not** apply to this bot.

---

## Config record — corrected from primary evidence

| Field | `bots_config.csv` | **Actual** |
|---|---|---|
| `entry_time` | `<verify>` | **11:00** (`Current market time is after 11:00am`) |
| `filter` | `<verify: Range075>` | **NONE — no filter exists.** FOMC skip only |
| `profit_target` | `<verify>` | **PT50**, pricing Normal, both sides |
| `stop_or_hedge` | "Conditional" | **Immediate $1-ITM close after 30 min position age.** No sustain condition |
| `reentry` | `<verify>` | **0** — once per side per day, gated on "opened today" |
| *(unrecorded)* | — | **Expiration exit 10 min before close, Market pricing** |
| *(unrecorded)* | — | **Bid-Ask Guard OFF** (unchecked, both scanners) |

---

## Position log (16 losses)

**Thirteen monitor-closed positions** — `2026-03-20, 03-23, 03-26, 03-30, 03-31, 04-07, 04-09, 04-23, 05-04, 05-07, 05-12, 05-18, 05-19`. Identical treatment:

- **A) Exit:** PT50 → **NOT FIRED** where `mfe ≥ 0.50`, **N/A** below it. Attached and working (69/70 winners prove it); these positions simply moved against the bot before reaching target.
- **B) Hedge:** "Conditional" → **FIRED** — at $1 ITM, exit $0.91–$1.07, mean $1.012. 13 of 16 closed at their own **MAE timestamp**, the defensive-exit fingerprint.
- **C) Cause:** `settings` **[CONFIRMED]** — the monitor implements an immediate $1-ITM stop, not the documented sustained trigger (F1). *Ruled out:* by_design (doc specifies a sustain); oa_execution (fired correctly every time); market_unfillable (all filled); data_error. **Evidence that would change this verdict:** none outstanding — the automation trees are dispositive.
- **D) If declared logic worked:** the logic **as built** did work; actual P/L stands. **What the *documented* mechanic would have produced is unknowable** — a 10-minute sustain needs intraday tape that no longer exists for these dates.
- **E) Best alternative:** **ride** on 12 of 13 (range −$4,887 to +$728); **PT50 +$336 on 03-20**, the one position where the target was reachable before the breach. *Preemption:* naming ride is safe per-position, but at bot level ride removes the $10,277 the hedge genuinely saved on the 6 deep-ITM days — both halves or neither.

**Three Expiration-closed positions** — `2026-05-08 (−$250), 05-13 (−$891), 05-20 (−$551)`:

- **A) Exit:** PT50 → **N/A** (05-08, mfe 0.00) / **NOT FIRED** (05-13 mfe 0.44, 05-20 mfe 0.19 — both below threshold, correct non-fire).
- **B) Hedge:** Conditional → **NOT FIRED** — never reached $1 ITM. Correct.
- **C) Cause:** `by_design` **[CONFIRMED]** — `Expiration: 10 minutes before`, Market pricing (F5).
- **D) If declared logic worked:** no declared rule was due to fire; actual stands.
- **E) Best alternative:** **ride** — +$432, +$928, −$400. Two of three recovered; 05-08 finished ITM and ride was worse.

---

## Open evidence requests
1. ~~Do the siblings carry Range075?~~ **RESOLVED 2026-07-28 — none of them do. See Addendum A1.**
2. ~~Do the siblings share the monitor shape?~~ **Partly resolved — see Addendum A2–A4.** Remaining gaps are listed at the end of the Addendum; none is blocking.

---

## Fleet-level running table — FINAL

| Bot | Verdict | Confirmed execution failures | $ recoverable | $ explained by strategy/design |
|---|---|---|---|---|
| **IC-SPX-FastPT25-S2** (post-fix) | **Execution-broken** — PT25 dead; entry, S2 firing, scanner gates clean | PT25 non-firing (CONFIRMED) · orphan-loop race (CONFIRMED) · Cleanup on Market (CONFIRMED) · 1 structural artifact | $3,000 artifact · +$11,922 if PT25 ran *(optimistic bound)* · $305 churn | −$3,285 S2 whipsaw |
| **QQQ-HedgeD-Conditional** | **Execution-clean, design-broken, mis-documented** | **0 platform failures.** 2 config-record falsehoods (no Range075; no sustain condition) | **$0 from execution** | **−$8,433** net hedge cost · **−$11,994** vs S3 on matched days |
| **QQQ-Range075-PT50-1230PM** | **Mixed** — PT50 perfect on puts, absent on calls | 0 platform; 1 config gap (call-side PT50) | +$375 exit drag *(sample has zero tail events)* | $0 — all 40 settled worthless |
| **DIR-SPX-PutVIX22-SL75** | **Clean but untested** | 0 | $0 | $0 — nothing traded, nothing learned |

**Audit-wide cause tally across 35 losing positions: `oa_execution` 3 (9%) · `settings` 23 (66%) · `by_design` 9 (26%).**

---

### Data provenance
Ledger `data/trades.csv`. QQQ daily OHLC via Tradier `/v1/markets/history`; settlement values for all 86 positions computed from QQQ closes against short strikes. **No 5-minute tape exists for any date in this bot's range** (Tradier window opens 2026-05-29; last position 2026-05-22) — all intraday timing is from OA-sourced `mfe_date`/`mae_date`, none modelled. OA screens supplied 2026-07-28: bot Settings/Automations list; `HedgeD-Mon-Cond-PutBreach` and `-CallBreach` trees; `HedgeD-Scan-Put` and `-Scan-Call` trees with Exit Options panels.

---

# ADDENDUM — Sibling automation trees (operator-supplied 2026-07-28)

The open item from F2/F3 is resolved, and it turned up three further structural problems with the hedge tournament.

### A1 — All four hedge bots share the identical scanner. None has Range075.
`HedgeA-Scan-Put/Call`, `HedgeB-Scan-Put/Call`, `HedgeC-Scan-Put/Call` are node-for-node identical to HedgeD's:

> `Loop QQQ` → `FOMC Meeting today` **No** → `Current market time is after 11:00am` **Yes** → `Bot opened a position with [side] today` **No** → `Open QQQ Short [Put/Call] Spread`

**Good news:** the tournament **is** matched on entries. F3's ranking is **not** confounded by filter differences — the arms differ only in hedge. That was the risk I flagged and it resolves favourably.

**Bad news:** **the entire QQQ hedge tournament ran with no entry filter.** `bots_config` describes these as Range075 bots. All four are unfiltered, taking a trade every open day. The documentation error is fleet-wide, not HedgeD-specific.

### A2 — S3, the winning arm, runs in a different execution class from the other three
`HedgeC-S3`'s Automations panel lists **SCANNERS only — no monitors at all.** S3 must therefore be implemented as a **`Stop Loss %` Exit Option** on the Open Position action.

That means the tournament varies **two things at once**:

| Arm | Mechanic lives in | Evaluated | Cycle order |
|---|---|---|---|
| **C — S3** | **Exit Option** | **every 1 min** | **FIRST** |
| A — S1 | Monitor | bot scan speed | third |
| B — S2 | Monitor | bot scan speed | third |
| D — Conditional | Monitor | bot scan speed | third |

**S3's win may be partly an execution-class advantage, not a mechanic advantage.** Exit Options evaluate every minute and run before Monitors in every cycle. Any conclusion of the form "S3 is the best hedge" is confounded with "S3 is the fastest-firing implementation." The tournament cannot separate them as built.

### A3 — S3 is also mis-documented, by an order of magnitude
Documented (`oa-platform-reference.md` §14): *"S3 — a **50% max-loss stop** on the position."*

Observed across its 44 losses: **exit/credit median 1.67** (p25 1.62, p75 1.75), and **44 of 44 closed at their own MAE timestamp** — an unmistakable stop-loss fingerprint.

- A true 50%-of-max-loss stop on a $2-wide spread with median credit $0.14 would exit near **$1.07**.
- Observed median exit is **$0.24**.

The implemented rule is a **percentage-of-credit stop in the SL50–SL75 range** — roughly **$0.10 of loss per contract** versus the documented **~$93**. Nearly an order of magnitude tighter. That is *why* it fires on 51% of positions (44 of 86) for small amounts and wins on Exp(R): it is a hair-trigger scalp stop, not the max-loss stop the project believes it tested.

*Confidence: INFERRED (strong) — from exit ratios and the MAE fingerprint. `HedgeC-Scan-Put` → Open Position → Exit Options would confirm the exact percentage.*

### A4 — S1 and Conditional are effectively the same arm
Position-by-position across all 86 matched positions: **73 have identical P/L (85%)**. Only 13 differ, and D is worse on 11 of them (median ~$460 worse per position). Exit-price medians: **A $0.81 vs D $1.00**.

S1 fires marginally earlier and cheaper, but these are not two independent tests of two mechanics — **the tournament has roughly three distinct arms, not four.** (A's monitor trees were not supplied, so the exact trigger difference is unconfirmed. Note A's $0.81 median also does not match its documented *"close the tested spread at ~$0.50."*)

### A5 — Independent confirmation of the champion's orphan loop
`HedgeB-S2` carries **`HedgeB-Mon-S2-Cleanup`** — the same cleanup automation family as the champion's `Scalp-Mon-S2-Cleanup`, which caused the 7/01 churn loop (Bot 1, F3).

**HedgeB never loops.** Its scanner gates on `Bot opened a position with [side] today` — a per-day flag. Once a side has traded it is locked out regardless of what closes. The champion gates on *currently open* positions, which is exactly why it can re-fire.

**This is a clean natural experiment: same Cleanup automation, different scanner gate, no loop.** It confirms the Bot 1 F3 diagnosis independently — the defect is the champion's scanner gate, not Cleanup.

### Revised tournament standing
The F3 ranking stands on entries (A1) but carries two new caveats: S3's lead is confounded with its execution class (A2), and both S3 and Conditional are testing mechanics other than the ones they are named for (A3, F1).

**The blunt version: of the four hedge mechanics this tournament was built to compare, at least two — S3 and Conditional — were never actually implemented as specified, one pair (S1/Conditional) is 85% redundant, and all four ran without the entry filter the config claims. The tournament's output should not be used to select a fleet hedge until the arms are rebuilt.**

### Remaining evidence gaps (none blocking)
1. `HedgeC-Scan-Put` → Open Position → **Exit Options** — pins S3's exact stop percentage (A3).
2. `HedgeA-Mon-S1-PutBreach` tree — confirms how S1 differs from Conditional (A4).
3. `HedgeB-Mon-S2-StrikeTouch` / `-Cleanup` trees — confirms S2 matches its documentation.
