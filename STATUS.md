# Bot Fleet — STATUS  ·  generated 2026-07-31

> **Numeric source of truth.** Auto-generated from `data/trades.csv` by `scripts/report.py`. Do not edit by hand. All figures are PAPER. Task backlog: `docs/backlog.md` (also in `dashboard.html`).

> **POST-CUTOVER LEDGER — `LEDGER_START = 2099-01-01`.** Every figure below is drawn from positions **opened on or after** that date. The v1 era is frozen in `data/archive/` and is never an input here.

## ⏳ EMPTY LEDGER — n=0

**No positions have been opened since the cutover.** Every table below is empty by construction, not by failure. There is nothing here to read as a result: an absent number is not a zero, and a blank expectancy is not a flat one. This page becomes meaningful on the first post-cutover trading day.

## Headline
- **Total closed P/L:** $0  ·  0 legs  ·  0 bots

## Champion — IC-SPX-FastPT25-S2
- P/L **$0**  ·  0 condors (0 legs)  ·  0 trading days (0 green / 0 red)
- Max drawdown (daily cumulative): $0
- Go-live gate (≥15 clean post-fix condor trades): **0 / 15**

## Allocation audit — sizing realism  (ON bots, per-position)
> R (pnl÷risk) already cancels size, so this changes **no ranking** — it flags whether the paper sizing is realistic to carry live. Hold class sets the rule: **0DTE** recycles risk daily; **swing/multi-week** ties capital up for the whole hold (max-risk/day = concurrent open risk, not daily deploy). **1-lot bots are fill-untested at scale** — their edge won't survive the slippage of a real order size (ties to the v5-slippage task).

| Bot | Pillar | Hold | Pos | med Qty | med Risk$ | max Risk$ | Realism |
|---|---|---|--:|--:|--:|--:|:--|
## Lessons index — tagged, searchable  (data/lessons.csv)
> Every graded bot-day's "day's lesson" (from the brief JSON's Verdict row; session-log fallback only for dates the brief never covered), tagged from a fixed vocabulary (`entry-timing · hedge · filter · regime · sizing · other`) by simple keyword rules (see `scripts/lessons.py` docstring) — not an ML classifier. Grouped by tag, most recent first.

**Tag counts:** entry-timing 1  ·  hedge 2  ·  regime 12  ·  other 18

#### other (18)
- **2026-07-02** · DIR-SPX-Put-Control — borderline; watch
- **2026-07-02** · IC-SPX-FastPT25-S2-130PM — borderline; watch
- **2026-07-02** · IC-SPX-Fortress-Defang — clean win
- **2026-07-02** · IC-SPX-Fortress-Unstopped — clean win
- **2026-07-01** · IC-SPX-FastPT25-S2-130PM — borderline; watch
- **2026-07-01** · IC-SPX-Fortress-Defang — clean win
- **2026-07-01** · IC-SPX-Fortress-Unstopped — clean win
- **2026-07-01** · Nigiri-Paper-v1 — borderline; watch
- **2026-06-30** · 60min-ORB-10W-Paper-v1 — clean win
- **2026-06-30** · DIR-SPX-CallVIXdrop — borderline; watch
- **2026-06-30** · IC-SPX-FastPT25-S2 — clean win
- **2026-06-30** · IC-SPX-FastPT25-S2-130PM — borderline; watch
- **2026-06-30** · Nigiri-Paper-v1 — clean win
- **2026-06-30** · Trendy-Paper-v1 — clean win
- **2026-06-29** · 3DTE $140-$350 — clean win
- **2026-06-29** · IC-SPX-FastPT25-S2 — clean win
- **2026-06-29** · Nigiri-Paper-v1 — clean win
- **2026-06-26** · IC-SPX-FastPT25-S2 — clean win

#### regime (12)
- **2026-07-02** · DIR-SPX-CallVIXdrop — good loss — design held, tape unlucky
- **2026-07-02** · IC-SPX-FastPT25-S2 — good loss — design held, tape unlucky
- **2026-07-01** · DIR-SPX-Put-Control — good loss — design held, tape unlucky
- **2026-07-01** · IC-SPX-FastPT25-S2 — good loss — design held, tape unlucky
- **2026-06-30** · DIR-SPX-Put-Control — good loss — design held, tape unlucky
- **2026-06-30** · IC-SPX-Fortress-Defang — good loss — design held, tape unlucky
- **2026-06-30** · IC-SPX-Fortress-Unstopped — good loss — design held, tape unlucky
- **2026-06-29** · DIR-SPX-Put-Control — good loss — design held, tape unlucky
- **2026-06-26** · DIR-SPX-Put-Control — good loss — design held, tape unlucky
- **2026-06-26** · IC-SPX-FastPT25-S2-130PM — good loss — design held, tape unlucky
- **2026-06-26** · IC-SPX-Fortress-Defang — good loss — design held, tape unlucky
- **2026-06-26** · IC-SPX-Fortress-Unstopped — good loss — design held, tape unlucky

#### hedge (2)
- **2026-06-26** · QQQ-IC-0DTE-Fortress — naked breach rode to expiry — log a convexity/hedge candidate here
- **2026-06-26** · QQQ-IC-0DTE-Fortress-NoPT50 — naked breach rode to expiry — log a convexity/hedge candidate here

#### entry-timing (1)
- **2026-06-23** · (session-log) — **Key lesson surfaced (6/17 vs 6/23):** Range075 protects against gap days (move visible at entry) but NOT against an intraday trend after entry — 6/17 opened +0.7%, passed filter, Fortress entered 1:31 and ate −$7,530; 6/23 gapped −3% pre-open so filter blocked. Naked-downside risk = "quiet open, trend after 11am," the exact hole a stop-loss / long-vol overlay plugs.

## Per-bot (sorted by P/L)
| Bot | Pillar | Und | Role | Status | Trades | Legs | P/L | WR | Fix? |
|---|---|---|---|---|--:|--:|--:|--:|:--:|

## Readiness board — per-condor, gated (the graduation view)
> **Grain = condor** (legs summed), not leg. Six ordered gates; the **first red (○) gate is the named blocker**. `●`=pass `○`=fail `·`=pending. Exp(R) shows the **bootstrap 95% CI** (replaces the t-stat). Stage: INCUBATE→VALIDATE→CANDIDATE→LIVE-READY (LIVE = real capital). Controls & mirror-watch are listed separately — they can't graduate by design.
> **Gates:** G1 clean data (no strike-bug, single-sided excluded) · G2 ≥20 clean condors · G3 Exp(R)>0 w/ 95% CI above 0 · G4 maxDD-R within cap (RoE $ cap still a `<FILL>` blank) · G5 instruction-mirror ≥90% (from the daily brief / `data/compliance.csv`; pending until ≥5 graded days) · G6 OOS/regime robustness.

| Bot | Role | Stage | Gates | n | Exp(R) [95% CI] | Blocker |
|---|---|---|:--:|--:|--:|---|

#### Non-graduating (controls / mirror-watch — tracked, can't go live)
| Bot | Role | Gates | n | Exp(R) [95% CI] | Note |
|---|---|:--:|--:|--:|---|

## Scorecard — normalized (Return on Risk) · legacy per-LEG view
> ⚠️ **Per-LEG grain** (kept for continuity) — for the graduation decision use the **Readiness board** above (per-condor, gated). Each trade = **pnl ÷ capital-at-risk** ("R"), so allocation and contract size cancel out. Sorted by expectancy. t-stat blows up for low-variance grinders (e.g. 3DTE) — don't rank on it alone.

### Ranked (n ≥ 20)
| Bot | Pillar | n | Exp(R) | t | Tot R | maxDD-R | WR |
|---|---|--:|--:|--:|--:|--:|--:|

### Provisional (n < 20 — tracked, not ranked; samples too small to trust)
| Bot | Pillar | n | Exp(R) | Tot R | raw P/L |
|---|---|--:|--:|--:|--:|

### Decision rules (read against the right column)
- **Kill** — Exp(R) < 0 held with conviction (|t| ≳ 2, or n large). Raw P/L size is irrelevant.
- **Graduate** — Exp(R) > 0 **and** |t| ≳ 2 **and** n ≥ threshold (edge is real, not noise).
- **Size live capital** — among graduates, weight by Tot R + low maxDD-R (consistency); never size on raw P/L.
- **Exp(R)** = avg return per $1 risked. **Tot R** = size-free analog of total P/L. **maxDD-R** = worst cumulative-R drawdown (risk shape). **t** = evidence the edge is real.

## Caveats
- **Trades = condors** (the two legs of one entry paired); **Legs = OA position rows** (matches OA's "Positions" count). Win rate shown is per-condor.
- A combined-`ironcondor` bot logs 1 leg per condor; a legged bot logs 2 — so Legs ≈ 2× Trades only for legged bots. That's why they were confusing before.
- `Fix? = Y`: QQQ-IC bot carrying the call-side strike-resolution bug; data contaminated until fixed.
- Single-sided condors (only one leg opened): 0 legs flagged.
- Tiny-N bots are tracked but **not** evidence; read Trades before P/L.
