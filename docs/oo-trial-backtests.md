# OO Trial-Verification Backtests (queued)

> **Purpose:** two backtests to run on an OptionOmega **free trial** (Backtesting tier) to confirm the
> docs-verified hedge-expressibility claims that are marked *verify* in `hedge-research.md`
> (OO hedge-expressibility inventory). These are **plumbing tests** — they confirm the mechanic *fires
> and logs correctly*, NOT that the mechanic *wins* (that's the tournament). Run when logged in;
> Claude-in-Chrome can drive OO (OA is blocklisted).
>
> Status: **QUEUED — not yet run** (need a logged-in OO session).
> UI note: feature names below are quoted from OO docs; a few exact click-paths are marked
> **[confirm live]** because the docs describe the feature but not every menu location.

---

## Shared base config (both tests)

Set these identically so the two tests are comparable and easy to read:

| Field | Value |
|---|---|
| Ticker | **SPX** (PM-settled; matches the champion) |
| Date range | **2024-01-01 → most recent** (≈18 mo; 0DTE-rich, post-daily-expiry) |
| Strategy | **Iron Condor** (custom legs below) |
| Strike selection | **Percentage (OTM) = 0.75%** on both shorts |
| Width | **$5** ($5-wide each side via child/dependent leg offset −5 put / +5 call) |
| DTE | **0** (0DTE) |
| Entry Time | **11:00** ET |
| Frequency | **Daily** |
| Max Contracts per Trade | **1** (clean per-trade reading; bypasses allocation) |
| Commissions & Fees | **$0.60 / contract** (match locked all-in; do NOT use OO's $0.10 default) |
| Slippage | **$0.05 entry + $0.05 exit** (modest, realistic) |
| Close Open Trades on Test Completion | **ON** (so runners/open legs appear in the trade log) |

Leg structure (custom, 4 legs):
- **Short put:** sell, 0.75% OTM · **Long put:** buy, linked, offset **−5**
- **Short call:** sell, 0.75% OTM · **Long call:** buy, linked, offset **+5**

---

## TEST 1 — Defang via Leg Groups

**Claim under test:** *"exit the short upon SL and leave the long as a runner"* (Leg Groups / SEME) can
be configured so each **short is bought back at ~$0.05** while each **long rides** — i.e., the "defang"
mechanic — and the trade log shows correct per-side behavior without the default whole-trade coupling.

**Extra toggles to flip (on top of base config):**

1. Enable **Leg Groups (Single Entry Multi Exit)**.
2. Create **4 leg groups**, one per leg (so longs survive — *"By default, when any leg is closed in OO,
   the whole trade closes"*; only leg-grouping decouples them):
   - G1 = short put · G2 = long put · G3 = short call · G4 = long call
3. On the **short groups (G1, G3)**: set the exit to **Profit Target → Closing Order = $0.05**
   (*"set a closing order at a certain price and get out when that price is filled"* = buy back the short
   at $0.05). **[confirm live]** that per-group exit conditions accept a closing-order value.
4. On the **long groups (G2, G4)**: **no PT, no SL** — let them ride to settlement / test-completion.

**Success criteria (all must hold):**
- Trade log shows **short legs closing at ≈$0.05** with reason = profit target / closing order.
- **Long legs remain open** after the shorts close, then close at settlement or test-completion
  (reason = expiry / close-on-completion), **not** at the moment the short closed.
- Each leg group appears as **its own row** in the log (*"each leg group is counted as its own trade"*).
- Per-side P&L is separable and the riding longs show their own (likely small/negative) P&L.

**What this does NOT verify:**
- That $0.05 is the *right* defang level, or that defang *beats* S2 (that's the tournament).
- **Real fills at $0.05** — deep-OTM/cheap 0DTE options are illiquid; the backtest assumes a fill that
  live may not get. Flag as a known optimism.
- Margin realism — docs warn the tester *"will not currently check… margin requirements if you happen to
  exit… the long leg of a spread before the short leg."*
- Sub-second timing (irrelevant here — defang is a price-buyback, not a touch).

---

## TEST 2 — Reclaim Re-Entry

**Claim under test:** **Re-Enter After Exit** triggers on a **"short tested"** exit, honoring a **delay**
and a **min/max time window** — and, importantly, **documents what it does NOT do** (no native
"price reclaimed the level" confirmation).

**Extra toggles to flip (on top of base config):**

1. Enable **Exit When OTM Short Put/Call is touched** ("Exit When Tested") = **0 points** (exit exactly at
   touch). This is the exit that will fire the re-entry.
2. Enable **Re-Enter Trades After Exit**:
   - Trigger on the **"short tested"** exit condition.
   - **Delay = 5 minutes** before re-entry.
   - **Min re-entry time = 11:05**, **Max re-entry time = 14:00**.
3. Leave PT/SL off for this test (isolate the touch-exit → re-entry path). Optional: add a PT later.

**Success criteria (all must hold):**
- Trade log shows an **initial trade exited with reason = tested/touched**.
- A **new trade opens ≥5 min later**, within 11:05–14:00, using the **same entry criteria** (deltas/%OTM,
  width, DTE) — per docs *"the re-entered trade will use the same entry criteria… as the original trade."*
- On a choppy day that tests repeatedly, **multiple re-entries** appear (each respecting delay + window).
- No re-entry fires **outside** the 11:05–14:00 window.

**What this does NOT verify (document explicitly in the result):**
- **No "reclaim" confirmation.** OO re-enters on delay + time + original entry criteria — **NOT** on price
  returning inside the breached level. So it will re-enter into a **still-trending day** (the exact trap a
  true reclaim rule avoids). This is the gap that keeps reclaim-confirmation re-entry a **LEAN** job.
- **No sustain/dwell distinction** — "Exit When Tested" is 1-min sampled (*"does not look at the OHLC of
  the minute"*), and there's no tunable "held N min then act" timer.
- **No regime gating** of the re-entry decision.

---

## After running (both tests)

Record in `hedge-research.md` (OO inventory section): flip each matrix row from *verify* to
**confirmed / partial / failed** with the trade-log evidence. If Test 1 passes, defang graduates to a real
OO tournament entrant; if Test 2 behaves as expected, lock the verdict that reclaim-confirmation re-entry
stays on LEAN. Then append a 2–3 line `session-log.md` entry.
