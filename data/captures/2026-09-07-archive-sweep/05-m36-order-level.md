# M-36 — Order-level verification: 5 ON mirrors + 2 DIR bots

**Ruling:** `R-2026-09-07-M-36-RESCOPED` (GF arms covered by the P3 daily GF-shape TSV; this
read-only pass on the 5 ON mirrors + 2 DIR bots closes the item).
**Session:** Cowork, 2026-09-07, ~15:17–15:35 ET. **Read-only — nothing was written to OA.**
**Account asserted:** `Paper Trading` on every bot page read (never `TR ****4219`).
**Browser:** Claude built-in browser pane (not the Chrome extension), viewport forced 1440x900.
**Roster at read time:** 43 active bots • 7 left in plan (post-probe; `QQQ-IC-0DTE-Baseline` archived).

## Method
For each bot: the most recent CLOSED position was opened from `/positions/closed` (account-level
list, `Load more` x3 → 120 rows) and its **Position Details + Trades list** read. Config was read
from each bot's `/settings` page (Bot Inputs, automation names + schedules, Safeguards, template).

⛔ **The Exit Options panel is NOT used as evidence of execution** (`CLAUDE.md` §3). The "exit that
fired" column is taken from the **Trades list** close-trade label only.

## The table

| # | Bot | Order placed (most recent closed) | Config | Structure | Strikes / width | Qty | Exit that fired (Trades list) | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | **3DTE $140-$350** | SPX Iron Condor, exp Sep 1, opened Aug 27 10:15AM, credit $0.35, risk $965, DIT 5d | Inputs: EXPIRATION 3 market days · POSITION SIZE 26% of net liquid · < RETURN % 6%. Scanner `xDTE $140-$350 +10` 10:00am–1:00pm. Alloc $5,000 | IC ✓ | 7505P/7515P + 7900C/7910C — **10 wide both sides ✓** (`+10`) | 1 | **No close trade.** Status `Expired` Sep 1; P/L $35 = 100% of credit | ⚠️ **2 FINDINGS** (F1, F2) |
| 2 | **Nigiri-Paper-v1** | SPY Short Put Spread, exp Sep 11, opened Sep 3 10:30AM, credit $0.09, risk $4,910, DIT 1d | Inputs: SYMBOL SPY ✓ · POSITION SIZE 50% of allocation · EXIT OPTIONS Profits 75% · SHORT PUT DELTA -.05 · SPREAD WIDTH $5.00. Alloc $10,000 | Short put spread ✓ | 735P/740P — **$5 wide ✓** | 10 — risk $4,910 = **49.1% of $10,000 alloc ✓** | Close Sep 4 9:45AM @ $0.05 — **`Automation Log`** (monitor), realized 44.4% of credit | ⚠️ **F3** |
| 3 | **Trendy-Paper-v1** | SPY Short Put Spread, exp Sep 14, opened Sep 3 10:30AM, credit $0.57, risk $943, DIT 1d | Inputs: TICKER SPY ✓ · PROFIT MARGIN 50% · ABSOLUTE PROFIT MARGIN 90% · TRAILING PROFIT MARGIN 10%. Alloc $10,000 | Short put spread ✓ | 740P/750P — $10 wide (**width is not a bot input — not assertable at bot level**) | 1 | Close Sep 4 10:45AM @ $0.33 — **`Automation Log`**, realized **42.11%** of credit | ✅ **F4 RESOLVED 2026-09-07** — see below |
| 4 | **Friday 14 DTE Broken Wing IB (B-70)** | SPX Iron Butterfly, exp Sep 11, opened **Fri** Aug 28 10:30AM, credit $40.05, risk $1,995, DIT 6d | Template: "Classic Broken Wing **60/40** IB placed **70 points below the money**". Scanner `BWB Opener` **10:30am–11:05am Friday**. Triggers incl. `Reset PT`, `Set Exit Options Trigger`. Alloc $10,000 | Broken-wing IB ✓ | 7600P/7660P/7660C/7700C → put wing **60** ✓, call wing **40** ✓; body 7660 vs SPX 7730.40 at open = **70.4 pts below ✓**; **14 DTE ✓**; opened at window open ✓ | 1 | Close Sep 3 12:16PM — **`Profit Target: $105.00 profit at $39.00`**, filled $38.95 ✓ | ✅ **CLEAN — matches on every dimension** (note N1) |
| 5 | **60min-ORB-10W-Paper-v1** | SPX Short Put Spread, exp Sep 1 (0 DTE), opened Sep 1 11:00AM, credit $0.75, risk $925, DIT 0d | Template: "60Min ORB **10 Wide**". Scanners Put/Call Spread `2:00pm or earlier`. **No bot inputs.** Alloc $10,000 | Short put spread ✓ | 7615P/7625P — **10 wide ✓**; opened 11:00AM, inside `≤2:00pm` ✓ | 1 | Close Sep 1 11:48AM — **`Profit Target: $50.00 profit at $0.25`**, filled $0.25 ✓ | ✅ **CLEAN** (note N1) |
| 6 | **DIR-SPX-CallVIXdrop** | SPX **Long** Call Spread (debit), exp Sep 3 (0 DTE), opened Sep 3 **11:00AM**, debit $5.65, risk $565, DIT 0d | Trigger `Entry Scanner` **every day 11:00am EST** ✓. **No bot inputs.** Notes: "Generated from a backtest". Alloc $10,000 | Long call spread ✓ | 7710C/7725C — 15 wide (no configured width to compare) | 1 | Close Sep 3 3:50PM — **`Auto close ITM position before expiration` / `Market`**, filled $9.90 | ⚠️ **F5** |
| 7 | **DIR-SPX-PutVIX22-SL75** | **NONE — no closed position, no open position, `closedCount` = 0** | Trigger `Entry Scanner` every day 11:00am EST. No bot inputs. "Generated from a backtest". Alloc $10,000. Status **ON** | — | — | — | — | ⚠️ **F6 — not verifiable** |

## Findings

**F1 — `3DTE $140-$350`: filled credit $0.35 is far below the automation's own named band.**
The scanner is named `xDTE $140-$350 +10`, i.e. a $1.40–$3.50 credit band. The order filled at
**$0.35** — an order of magnitude under the floor. Either the name no longer describes the
scanner's price filter, or the filter is not binding. **This is the same class of defect as the
open T-48 puzzle** (ScannerB $0.07 credit filter with 70/126 legs filled *at* $0.07). Recommend
folding F1 into T-48 rather than opening a separate item.

**F2 — `3DTE $140-$350`: the sizing comparison spans a config change and is therefore void.**
Risk $965 on net liq $5,964 ≈ **16%**; the current Bot Input reads **26% of net liquid**. But the
position opened **Aug 27**, and the 26% figure was executed **2026-09-02** (`oa_sizing_execution_2026-09-02`).
Comparing them is comparing across the change. **Not a defect. Not evidence either way.** The
first post-09-02 close for this bot is the one that tests sizing; it has not happened yet.

**F3 — `Nigiri-Paper-v1`: the exit that fired is not the exit named in Bot Inputs.**
Bot Input `EXIT OPTIONS Profits: 75%`; the close came from **`Automation Log`** (the
`7 Day Accelerated Profit` monitor) at **44.4%** of credit. Pre-emption is what that monitor is
for, so this is very likely by design — but the bot-level input advertises 75% and the realized
exit rule is a monitor. Anyone reading Bot Inputs alone would mis-model this bot.

**F4 — `Trendy-Paper-v1`: exit attribution UNRESOLVED (open).**
Closed at **42.11%** of credit. Config offers three candidate rules: PROFIT MARGIN 50%,
ABSOLUTE 90%, TRAILING 10%. The position's high was 57.9% → a 10% trail off that high lands
≈47.9%. **42.11% matches none of the three.** Resolving this needs the close trade's
**`Automation Log`** opened, which this read-only pass did not do. **Left OPEN — the one item in
M-36 that is not closed.**

> ### ✅ F4 RESOLVED — 2026-09-07 ~15:35 ET (original text above left standing)
> The close trade's **Automation Log** was opened (read-only). Verbatim:
> - **Automation:** `Put Spread Manager (Short Duration)` with 3 inputs
> - **Triggered by:** `Monitor`, Sep 4 2026 10:45AM
> - **Decision node:** *"Position trails a Profit Margin target by Trailing Profit Margin **or**
>   Position premium decreased by Absolute Profit Margin since it was opened"* → evaluated **Yes**
> - **Action:** `Close Position` — SPY Short Put Spread Sep 14, -750 put, +740 put
>
> **The premise of F4 was wrong.** 42.11% was never supposed to equal one of the three margins:
> the decision is a **compound OR on a trailing condition**, and the realized number is simply
> where the ask sat at fill (`0.32 → 0.33`, filled $0.33) on the monitor's scan tick — not the
> trigger threshold. The ABSOLUTE branch (90%) cannot have fired, since the position's high was
> 57.9%; therefore the **trailing branch** fired, which is exactly what Bot Inputs
> `PROFIT MARGIN 50%` / `TRAILING PROFIT MARGIN 10%` feed.
>
> **Verdict: config and behavior agree. No defect. Not a finding.**
>
> **Method note (new, reusable):** exit attribution is read by opening the close trade's
> `Automation Log` link (`a.link.tlink`, first instance = the close trade). It returns automation
> name, trigger type, the decision text verbatim, and the action taken. This is the correct
> Layer-2 surface for "which exit fired" — strictly better than inferring from the close-trade
> label, and it is *not* the Exit Options panel.

**F5 — `DIR-SPX-CallVIXdrop`: the realized exit is an OA platform safety net, not a bot rule.**
The close trade reads **`Auto close ITM position before expiration` / `Market`** at 3:50PM. The
bot configures a `-50%` stop and **no profit target**, so a winning 0-DTE debit spread has no
bot-side exit at all — OA's ITM auto-close disposes of it with a **market order** in the last ten
minutes. The bot's Notes say "Generated from a backtest"; a backtest almost certainly did not
model a 3:50PM market-order exit. **Slippage on this path is unmodeled and unmeasured.**

**F6 — `DIR-SPX-PutVIX22-SL75` is ON and has never filled anything.**
`closedCount` 0, open positions 0. Its entry scanner (same 11:00am shape as CallVIXdrop) has never
produced a position. Order-level verification is impossible; the bot is also generating no
evidence toward any sample target while occupying a plan slot.

## Notes
**N1 — two bots are running behind their template version.**
`Friday 14 DTE Broken Wing IB (B-70)`: BOT VERSION **4** (Nov 22 2025), LATEST **6** (Jul 29 2026).
`60min-ORB-10W-Paper-v1`: BOT VERSION **2** (Oct 26 2025), LATEST **3** (Jun 26 2026).
Both currently match their orders cleanly, so this is not a defect — recorded because an
`Upgrade Bot` click would silently change a verified bot.

## Verdict
**6 of 7 verifiable; 3 clean matches (#3, #4, #5 — #3 cleared on the F4 resolution below); 1 bot
unverifiable (F6).** ~~1 exit attribution left OPEN (F4)~~ — **F4 RESOLVED 2026-09-07, no defect.** No order was found that contradicts its bot's structure, strike geometry or
quantity. Every finding is about **exits and price filters**, not about the shape of what was
ordered.
