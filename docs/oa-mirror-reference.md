# Project #8 — OA Mirror & Combine: Complete Methodology & Bot Reference

> Standalone reference. Distills the capture→classify→paper→graduate pipeline, every bot analyzed, the evidence standards, the factor-bucket framework, all kill decisions, the OA platform knowledge accumulated, and the research conducted (with storage locations).
>
> **Sources:** project files (`bots-tracked.md`, `research-phase-sequence.md`, `research-progress.md`, `portfolio-hypotheses.md`, `matrix-tuple-batch-v0.md`, `kill-log.md`, `oa-feature-notes.md`, `oa-specialist-full-spec.md`, `project-setup.md`) dated through 2026-04-23, plus session history through 2026-06-06.
>
> **Timeline note:** The project files capture the state as of sessions 4–6 (Apr 17–23, 2026): 7 paper clones, Matrix v0 received, ORB on an A/B observation hold. The portfolio has since expanded to 10 bots and several decisions changed (ORB killed, three new bots added, factor-bucket framework adopted). Both states are documented; "Current state (June 2026)" sections flag what's changed.

---

## 1. Mission & scope

**Goal:** Systematically identify proven options-bot edges on the Option Alpha (OA) community leaderboard, decide which to mirror or combine, paper-trade many simultaneously, and graduate the survivors to live capital.

**Five-stage roadmap (adopted ~May 2026):** Mirror → Build → Methodology → Cross-Project Signal → Productize. Stage 3 (Methodology) targeted Aug–Sep 2026.

**Capital plan:**
- Paper phase: $100K virtual, up to 50 bot slots (OA paper + Tradier sandbox).
- Live phase start: ~$2K, scales monthly through $5K → $10K → $25K → $100K.
- Every recommendation must work at $2K **and** scale cleanly. Where a strategy stops making sense at small size (per-contract max loss > ~20–25% of account), that's flagged explicitly.

**Platform setup:** OA Pro subscription; Tradier broker (production + sandbox). Tradier MCP connector and a VPS SPX chain recorder exist but are not critical to mirror work.

**Parallel-project firewall:** A separate Claude project holds the user's *original* 0DTE iron-condor edge (Fortress/Scalp/VolDay on SPX+QQQ), referred to here as the **0DTE Project** (also Project #1). Two rules:
- **No strategy firewall** — if an SPX/QQQ IC on the leaderboard is profitable and differs from the user's own setup, it's fair game. Finding a better variant of the user's approach is useful signal.
- **Infrastructure firewall** — dashboards, logs, and tracking stay separate. This project has its own files.

**What this project is NOT:** not a place to build the user's original edge; not a daily trade log (OA logs trades); not a real-time execution tool (trading happens in OA/Tradier).

---

## 2. The capture → classify → paper → graduate pipeline

The core operating loop. Each stage has explicit entry/exit criteria.

### 2.1 Core principles

- **Don't boil the ocean.** OA has many surfaces (Leaderboard, Top Strategies, Backtester, Trade Ideas, 0DTE Oracle, Earnings Edge, Webhooks). Pick one, extract its edge, move on. Parallel exploration produces shallow analysis.
- **Paper bots run in the background.** Once cloned and tracked, you don't wait 4 weeks before advancing. Data accrues while you work the next surface.
- **Validated edges before speculative ones.** Leaderboard templates have live-money validation across many traders → start there, work outward toward Top Strategies/Backtester (aggregated history) and Oracle/Earnings Edge (pattern tools).
- **"Do nothing" is the binding default on hedging.** The project does not apply hedges speculatively to bots outside the Matrix's confirmed classes.

### 2.2 Research phase sequence

| Phase | Purpose | Exit criteria |
|---|---|---|
| **1 — Leaderboard Mining** | Mirror proven, live-validated edges | Shortlist (8–12) cloned to paper + tracking live |
| **2 — Static Edge Discovery** (Top Strategies + Trade Ideas) | Find untemplated, lower-crowding edges; diversify away from SPX/QQQ | Obvious candidates evaluated; watchlist updated |
| **3 — Oracle Pattern Extraction** | Repeatable daily 0DTE patterns as bot/filter/webhook signal | 2–3 patterns extracted from 10–20 sessions of logging |
| **4 — Earnings Edge Sweep** | Event-driven exposure (the portfolio's known gap) | Not started |

**Status:** Phase 1 active throughout. Phases 2–4 largely deferred. Oracle reframed as a *live screener* (longitudinal logging), not a source of bots to mirror.

### 2.3 Capture (HTML pipeline)

Chrome **Save As → "Webpage, Complete"** on a template page with modals open captures the full automation logic as parseable text. The proven 5-save pattern:

1. Main page (no modals) → `01_main.html`
2. Open Scanner modal → `02_scanner.html`
3. Open Monitor modal → `03_monitor.html`
4. Each Event modal → `04_event_*.html`, `05_event_*.html`, …

~5 saves per bot, ~2–3 minutes. Yields 100% of on-screen content: decision trees, strategy definitions, input usage counts, version history, author notes, full comment threads with community live-P/L screenshots.

**Pre-capture sanity check (mandatory, added after the Kirk Hybrid kill):** Open the template, **count automations before spending saves.** A bot with **≥1 scanner** is autonomous. A bot with **0 scanners** is a manual-entry tool — its leaderboard P/L reflects operator skill, not strategy edge — and is out of scope regardless of rank. Red flags: a "Buttons" section that outnumbers scanners; "Bot Workshop" in the name; zero events or zero monitors (partial automation).

**Capture gotchas learned:**
- Complex scanner/monitor modals can silently save *empty* HTML even at normal file size (Pink Panther v14 Open Position scanner saved 103 KB with no content). **Always take screenshot backups for complex modals**, regardless of apparent save success.
- When an author keeps multiple parallel URLs for one bot (OA assigns a unique ID per template save), anchor on the URL showing **full version history**, not the one the leaderboard links to. (Pink Panther has 4+ URLs; only `-new-2` shows the complete v4→v14 history.)
- Grab linked backtest files when the author includes them (validated on ORB and BWB) — they enable direct edge-preservation testing of any prescription.
- **Parsing pipeline:** Python + BeautifulSoup. Decompose `<script>`/`<style>`, `get_text(separator='\n', strip=True)`, collapse whitespace runs, validate with landmark strings (e.g. "Start automation"); `md5sum` diffing to detect duplicate saves.
- **Chrome MCP** was blocked by Anthropic's allowlist; manual Save-As is the proven fallback. **Playwright MCP** identified as fallback for auth-walled captures if needed.

### 2.4 Classify (the 6-field Matrix tuple)

Every captured bot produces a standardized **6-field classification tuple** — both for internal correlation analysis and as the "API" delivered to the 0DTE Project's Hedge Classification Matrix:

1. **Position structure** — IC / IB / credit spread / naked / strangle / debit spread / calendar / diagonal / long premium / other
2. **Short-strike distance logic** — fixed delta / fixed % OTM / fixed $ offset / waterfall / expected-move / technical-anchored / manual / other
3. **DTE at entry** — exact DTE, range, or variable logic
4. **Existing exit logic** — profit targets, stops, time exits, or explicit "none"
5. **Hedging already present** — dynamic breach response, rolls, stops, opposite-side protection, or none
6. **Underlying(s)** — ticker list

### 2.5 Paper

Shortlist is cloned to OA paper at chosen allocations, labeled, tracked. Data review cadence:
- **Week 2:** quick check — is it firing? Do entries match expected mechanics?
- **Week 4:** first real data review — trade count, WR, avg loss vs backtest.
- **Week 6:** formal graduation review (the 6 graduation criteria).
- **Week 8+:** monthly portfolio-level correlation checks.

### 2.6 Fund (paper → live) — OA-Mirror is a funded pillar; bots fund IN PLACE

> ⚠️ **Reconciled 2026-06-08 to the single taxonomy bar** (`strategy-taxonomy.md`). Mirror bots
> are funded **in place** (they don't graduate out to another pillar). The headline gate is the
> taxonomy bar; the older items below are kept only as **supporting checks**, not separate gates.

**The funding bar (all must hold):**
1. **≥20 completed trades** in paper.
2. **Positive P/L** overall — instance-profitable, not just trade-level (the 3DTE/ORB trap: 91%
   trade WR can still bleed).
3. **Win rate within ~10% of the source's claim.** A large gap = do not fund.
4. **Max drawdown under the risk cap** — and max single-trade loss ≤ 20% of the intended live
   allocation (sizing is a Kelly/allocation decision made at funding time).

**Supporting checks (investigate, don't auto-fund/disqualify on alone):**
- Avg loss not materially worse than backtest (e.g. −$363 claimed vs −$600 paper = execution friction).
- No single loss > 1.5× the backtest's largest disclosed loss.

**Continuous rules layered on top:**
- **Variant Watch:** log community-forked variants per bot; require either multiple independent commenters describing the same fix OR live-P/L screenshots before treating as signal. Never use comment sentiment alone as a trading signal.
- **Post-Mortem Trigger:** on any live loss or paper loss > 1.5× avg loss, compare actual behavior vs flowchart intent; structural findings → `kill-log.md`, educational → `oa-feature-notes.md`; if on a Matrix-prescribed hedge, flag to the 0DTE Project.
- **Pre-commit kill thresholds in writing before data arrives** — identified as the highest-leverage discipline anchor (rules written after seeing data get rationalized away).

---

## 3. Evidence standards

The discipline that separates real edges from leaderboard mirages.

### 3.1 Leaderboard column priority

**Highest signal:** (1) Live vs paper flag — live is ~10× more trustworthy; (2) Time in market / age — <6 months = high suspicion; (3) Sample size — <100 trades = warning, <50 = near-useless; (4) Max drawdown — the tail tells you what you'll feel; (5) Profit factor — PF >1.5 on 100+ live trades is legit, PF >3 usually means small sample or cherry-picked window.

**Medium signal:** avg win/avg loss ratio; win rate (only *with* the ratio, never alone); Sharpe/MAR if shown.

**Traps that look good and mislead:** win rate alone (credit sellers hit 85–95% until they don't); avg P/L alone (one outlier win inflates small samples); follower/clone count (popularity ≠ edge); total P/L (contaminated by bot age); recent-only performance (hides cross-cycle regime mismatch).

**Always require if not shown:** max drawdown; sample size with live/paper split; bot creation / first-trade date.

### 3.2 Instance profitability vs trade win rate

The single most clarifying distinction. **Winners %** (fraction of bot *instances* that are profitable) beats **Win Rate** (per-*trade*). A bot at 95% trade WR but 50% instance profitability means half the operators lose money despite the trade-level edge — the losses are big enough to wipe many wins per operator. This is the "win small, lose big, no protection" pattern (3DTE: 91.3% trade WR / 46% instance profitability; ORB: 81.7% / 55.5%).

### 3.3 Math sanity check (data-mining detector)

For every bot, verify: `WR × avg_win − (1−WR) × avg_loss ≈ reported Avg P/L`. A clean match means no data-mining fingerprint. Examples that reconciled to the penny: Nigiri (0.957×$40 − 0.043×$253 = $27.42 vs $27), Trendy ($19.37 vs $19), Tasty ($94.38 vs $95), QQQ LC ($39.46 vs $40), Pink Panther v6 ($7.06 vs $7).

### 3.4 Breakeven WR buffer

`breakeven_WR = avg_loss / (avg_loss + avg_win)`; `buffer = current_WR − breakeven_WR`. Wider buffer = more headroom for a hedge/stop or regime shift to erode WR before edge goes negative. **Matrix prescriptions are calibrated to buffer width, not applied uniformly** — a 3-pt WR reduction is fine for BWB, existential for Pink Panther v6.

| Bot | Buffer above breakeven |
|---|---|
| Friday 14 DTE BWB | **14.1 pt** (widest) |
| Trendy SPS | 5.0 pt |
| QQQ long call | 2.8 pt |
| Pink Panther v6 | **1.2 pt** (thinnest) |

### 3.5 Other standing evidence rules

- **All-time *Live* leaderboard is the correct signal source.** All-time All Trades (paper+live) is for sanity checks and spotting Martingale bots only.
- **CSV export contains only *closed* trades.** Bots with only open positions show zero rows; the dashboard screenshot is the source of truth for open positions, current P/L, and risk.
- **Bot-name exact-match filtering** on the `botName` column isolates Project #8 trades from the full account export (which also contains Project #1 bots). Names must match OA exactly (e.g. `Friday 14 DTE Broken Wing IB (B-70)`, `60min-ORB-10W-Paper-v1`). CSV filename pattern: `undefined-YYYYMMDD-XXXXXX.csv`; fields include `botName, openDate, closeDate, pnl, type, description`.
- **Backtest-vs-live divergence is a first-class input.** ORB shows ~50% live degradation vs backtest; BWB community operators report live DIT 5× longer than paper (HughT: 1.1 vs 5.7 days) — paper overstates frequency/P&L for that class.
- **Author quality signals:** clean version discipline = quality; version sprawl (TFMITH's v6.01/v6.1/v6.23/v6.3/v6.3.1…) = uncertainty. The leaderboard cannot distinguish autonomous bots from manual-hybrid tools, so author intent must be verified.
- **~40% of actionable community findings come from comments**, not post bodies; threads with score ≥50 or comments ≥30 warrant full comment fetching.

---

## 4. Factor-bucket framework

Adopted to make the diversification gap precise. Every bot is mapped to one of five risk factors:

- **Short-vol** — sells premium, profits from decay/calm, fat-tail downside.
- **Long-vol / convexity** — buys protection/optionality, profits from spikes.
- **Directional** — net long/short the underlying.
- **Mean-reversion** — fades extension.
- **Carry** — harvests roll/term-structure.

**Diagnosis:** the portfolio is **dangerously concentrated in short-vol — 9 of 10 bots.** The only non-short-vol exposure is QQQ long call (directional). There is **no genuine long-vol/convexity bot and no bear-regime profit source.** Every short-vol bot either sits out or loses in a sustained bear trend; portfolio P/L tracks "we survive bears" at best, not "we profit in them."

**Sourcing problem:** long-vol/convexity strategies are **largely absent from the OA marketplace** (it's a premium-selling community). A **Stage 1 filter** was established to surface long-vol-*shaped* candidates: **WR < 55%, win:loss ≥ 1.5, PF > 1.2, traders ≥ 10.** The likely path to fill the gap is **Stage 2 custom bot builds** using Option Omega backtesting + Project #1 hedge IP (S2 strike-touch monitor, hg9 decision tree, ah12 A/B protocol, 13-mechanic hedge catalog), since the marketplace can't supply it.

---

## 5. Bot inventory

Status flow: `watching` → `cloned-paper` → `live` → `killed`.

### 5.1 Quick reference

| Bot | Author | Structure | Underlying | DTE | Factor | Status |
|---|---|---|---|---|---|---|
| 3DTE $140-$350 | jose78531 | Iron condor, $10 wings | SPX | 3 | short-vol | cloned-paper ($5K) |
| Nigiri Friday 0.05 delta | Alex D | Short put spread | SPY | 2–8 (Fri-routed) | short-vol | cloned-paper ($10K) |
| Trendy Short Put Spread | Kirk Du Plessis | SPS → IC on breach | SPY | 10 | short-vol | cloned-paper ($10–15K) |
| Tasty Condor | Jack Slocum | Iron condor | SPY | 45 | short-vol | cloned-paper ($10K) |
| Opening Range Breakout 60m | Jack Slocum | Dual 0DTE credit spread (fade) | SPX | 0 | short-vol / mean-rev | **killed** (was $10K) |
| QQQ long call | @johnb | Long call debit spread | QQQ | 90 | directional | cloned-paper ($30K) |
| Friday 14 DTE BWB (B-70) | Otto Mation | 60/40 broken-wing iron butterfly | SPX | 14 | short-vol | cloned-paper ($10K) |
| 60Min ORB 10 Wide | Arianne / @tradesinLulu | 0DTE 10-wide credit spread (fade) | SPX | 0 | short-vol / mean-rev | cloned-paper ($10K) |
| 1:45pm Sandwich | Jack Slocum | short-vol (no backtest) | — | — | short-vol | **paused** (0-for-6) |
| Weekly IB SPY | doug37866 | Weekly iron butterfly (ATM) | SPY | 5–7 | short-vol | cloned-paper ($10K) |
| Pink Panther BPS/BCS v6+v14 | Pink Panther | SPS↔SCS regime rotation + hedge | SPX/XSP/SPY | 15–40 | short-vol | watching (no clone) |
| Pink Panther Vertical Assets v19 | Pink Panther | Bull SPS + Profit-Boost IC | SPX | 15–35 | short-vol | watching (no clone) |
| TFMITH-The Hare | stuart96718 | Long directional premium, Martingale | 10 symbols | ~0 | directional | watching (demoted) |
| Kirk Hybrid Trading | Kirk Du Plessis | manual-hybrid (0 scanners) | — | — | — | **killed pre-capture** |

---

### 5.2 Active paper clones

#### 3DTE $140-$350 — jose78531
- **Structure:** Symmetric iron condor, $10-wide wings. **Waterfall short-strike logic:** 22 tiers, $140→$350 in $10 increments; first tier clearing the Return% threshold fires. Entry window 10:00–10:10am.
- **DTE:** 3 (default v11; author guidance 3–4).
- **Exit:** Profit-taking only — close at 90% decay on 0DTE (1pm time gate), 70% after day 1; gate: trade price ≥ $0.50. **No stop loss** (intentionally removed in v8).
- **Stats (All-time Live, 4/17):** $107.95K P/L, 309 instances, 91.3% WR on 8,434 trades, avg P/L $13, avg win/loss $173/−$1,665 (ratio 0.10), PF 1.09, **46.0% instance profitability**.
- **Edge / risk:** Short-DTE SPX premium decay, auto-tuned to whatever premium the day offers. Avg loss ~10× avg win, no stop → one sustained multi-day breach (the March 2026 event) wipes 30+ wins. Community: "9 of 16 positions dipped past max loss and recovered" — the false-positive rate is why the author removed the stop, but recoveries come with catastrophic tail events in between.
- **Paper:** $5K (deliberately small — "run small while skeptical"; one bad position = 20%+ of allocation). Validated as appropriate for 3–4 concurrent positions.
- **A/B note:** Cloned vanilla v11 to feed the 0DTE Project's conditional-hedge pilot (vanilla control + "$1 past short strike, sustained to next scan" variant; raw S2 dropped because S2 was derived on 0.75% OTM $5-wide symmetric ICs and doesn't transfer to the $140–$350 waterfall).

#### Nigiri Friday 0.05 delta — Alex D (@alex_d)
- **Structure:** Short put spread, 0.05-delta short / $5-wide, one at a time. **Day-of-week DTE routing to nearest Friday:** Mon=4, Tue=3, Wed=2, Thu=8, Fri=7 — keeps min 2 / max 8 DTE, avoids 0–1 DTE gamma.
- **Exit:** "7-Day Accelerated Profit" monitor (close if return% > 10 × days-in-trade); "0-Day ITM Check" (close 3pm on expiry day, guards OA's 2-hr force-close); default 75% profit target. **No stop by design** — author: "the stop loss is (and always should be) the position sizing and spread width."
- **Stats (90d Live, 4/18):** $22.30K / $34.26K all-time, 39 live instances, **92.3% instance profitability**, 95.7% WR on 815 live trades, avg win/loss $40/−$253 (0.16), PF 3.52 / 4.14 all-time. **Version 1, no revisions in 14 months.**
- **Risk:** bounded $500 max loss/trade; concentration risk (all SPY). Destroyed by gap-downs.
- **Paper:** $10K at defaults (50% net-liquid, 0.05 delta, $5 width). Live needs 20–25% NL not 50% (at $2K, $500 max loss = 25% drawdown). Single position consumes ~49% of allocation by design (2–4 concurrent intended) — validated as normal, not a sizing error.

#### Trendy Short Put Spread — Kirk Du Plessis (@kirk)
- **Structure:** SPS with trend filter that **dynamically hedges into an asymmetric IC on breach.** Entry gated on: not already `actively hedging`; VIX < 40 AND price > 200-day SMA; short-put OI > 500; exactly 0 SPS open. Opens 0.15-delta short, $10-wide.
- **DTE:** 10 fixed.
- **Exit:** 90% absolute profit target (author added after seeing positions sit at 90% for 3–4 days taking needless tail risk) + SmartStops + Exit Options preset.
- **Hedge:** On breach within the hedge-DTE window, opens an SCS at the SPS short-put strike / long $10 above underlying → asymmetric IC; hedge manager closes the call spread <1 DTE if underlying > short call. **Known failure mode (JaniZ, Aug 2021):** V-shaped reversal after breach → both legs lose → ~200% loss.
- **Stats (All-time Live, 4/18):** **$222.59K (rank 2), 444 instances, 11,700 live trades (largest captured)**, 87.9% WR, avg win/loss $72/−$363 (0.20), PF 1.44, 69.8% instance profitability, 8,000 clones.
- **Risk:** unhedged $1,000 max loss; the hedge can *increase* tail loss on V-reversals. WR buffer 5 pt — if WR drops to ~83%, expectancy flips negative.
- **Paper:** $10–15K. Not live-ready until $5K+ ($1,000 max loss = 50% of $2K).

#### Tasty Condor — Jack Slocum (@jackslocum)
- **Structure:** Iron condor, ±0.20-delta shorts, configurable spread width. Single scanner, **no monitors** — most mechanically minimalist bot captured. Entry: VIX < `Max VIX`, frequency throttle, exactly 0 same-cycle positions, 10:00am+.
- **DTE:** 45 fixed.
- **Exit:** Entirely via Exit Options — **50% of opening credit OR mechanical 21-DTE time exit, whichever first.** The TastyTrade canonical IC protocol. **The time exit IS the risk management** (first such bot captured).
- **Stats (All-time Live, 4/18):** $107.97K (rank 9), 57 instances, **82.5% instance profitability (highest captured)**, 79.0% WR on 1,140 trades, avg win/loss $225/−$397 (**ratio 0.57, most balanced**), **PF 2.14 (highest credible captured)**, 38 traders, 1,400 clones. Version 1, no revisions ~11 months.
- **Edge / risk:** pure 45-DTE theta, exit before gamma acceleration. Lower per-trade tail than Trendy (more room to recover; 21-DTE exit caps damage). First long-theta (monthly) bot in the portfolio.
- **Paper:** $10K (at $5 wings, $500 max loss = 5%). **Live-ready at $2K–$5K at $5 wings** — one of only two bots that fit a $5K account cleanly.
- **June note:** at day 21, 2 positions open, −$410 unrealized — *not broken, just slow* (45-DTE entries don't expire for ~6 weeks). The "kill if no trades by day 21" flag was struck.

#### QQQ long call — Venerable Sage of Money Mt. (@johnb)
- **Structure:** **Long call debit spread** — long 0.5 delta (ATM), short 0.1 delta (far OTM). **Zero inputs**, entirely hard-coded. Pure binary scanner: if a 90-DTE QQQ long call spread with bid/ask < $0.50 is available → open. No time/day/regime/VIX gate.
- **DTE:** 90 (nearest available ≥90).
- **Exit (dual, redundant):** 25% profit target (Exit Options, v2) + 30-*market*-day time exit (legacy Exit Monitor; ~45 calendar days; community treats it as redundant). **No stop, no regime filter.** Version 3, frozen 3 years.
- **Stats (All-time Live, 4/18):** **$346.78K — rank 1.** 248 instances, 154 traders, 8,591 live trades, 82.1% WR, 60.1% instance profitability, avg win/loss $294/−$1,128 (0.26), PF 1.2, 5,000 clones (most captured).
- **Edge (the real one):** *not* long-premium asymmetry — it's a debit spread with a **low 25% profit target** that's easy to hit on small QQQ rallies within 60 days, plus the 2023–2026 tech bull tailwind. Author: "about as bullish as it gets, will get destroyed in a bear market."
- **Risk:** ~$1,128 avg / ~$2,000–$2,500 max loss per contract; documented real drawdowns of $6,500+ on $30K paper in the March 2025 correction. Live/paper parity unusually tight (minimal slippage sensitivity).
- **Paper:** $30K (10%-NL × 10 positions default). The **most diversifying bot in the mix** — first long-premium, first QQQ, first zero-input bot; uncorrelated with everything else. Not live-ready until 3 months paper through a pullback.
- **June note:** best-performing bot (+$2,174 on 3 trades) but *only* because of regime tailwind. Open Week-1 question (closes at 25% profit and reopens every ~4 days — captured logic or divergence?) flagged for resolution.

#### Friday 14 DTE Broken Wing IB (B-70) — Otto Mation (@otto_mation)
- **Structure:** **60/40 broken-wing iron butterfly, below the money.** Both shorts at the same strike, **70 points below underlying;** long put 60 below (wider), long call 40 above (narrower). Wider put protection because that's the direction it moves against. Positive theta; neutral-to-slightly-bullish. Adapted from the Amy Meissner "A14" course strategy (external validation). **Fixed dollar offset** distance logic (new sub-type). **Exact-DTE match:** 7/14/21 switch-selected (default 14 only); skips the week if exact DTE unavailable.
- **Exit (3-layer):** $105/contract profit target; **stop loss $1,105/contract — switch, default OFF;** dynamic profit-target reduction near expiry (<2 market days + risk >$1,950 → loosen to ~$50). Schedule-gated to Fridays 10:30–11:05am; tag-gated by a 9:31am event.
- **Backtest (author-disclosed, 96 trades, ~1.8 yr):** no-stop → $7,140 P/L, 30.7% CAGR, −13.7% max DD, 90.6% WR, largest loss $1,947, avg DIT 5.2. With $1,105 stop → $5,348, 23.8% CAGR, −10.8% DD, 88.5% WR.
- **The headline result:** enabling the stop **costs $1,792 of P/L to save ~$290 of drawdown — a 6.2× net edge destruction.** Cleanest "stops destroy edge" datapoint in the set. Of 9 losers, 8 were < $400 and 1 was ~$1,900.
- **Buffer:** breakeven WR 76.5% vs 90.6% actual = **14.1 pt, widest captured.**
- **Risk:** structural max loss ~$2,000/contract (the structure IS the hedge). Killed by fast bear gap-downs >70 pts in 14 days (Feb 2025 tariff shock = the one ~$1,900 loss). Weekend gap risk unavoidable.
- **Operational cost (live, not in backtest):** ITM call legs have wide bid/ask → multiple failed closes; one operator paid $150 to close manually. Paper DIT ~1/5 of live DIT — paper overstates.
- **Paper:** $10K, stop OFF, 14-DTE only, v4. Live-ready only after 3 months paper + broker close-fill confirmation. The other bot that fits a $5K account (1 contract).
- **June note:** fired correctly on 4/24 at 14 DTE with the confirmed 60/40 structure.

#### 60Min ORB 10 Wide — Arianne (@tradesinLulu)  *(added pre-travel, May 2026)*
- **Structure:** SPX 0DTE **10-wide** short put OR call credit spread (breakout-failure / fade), short strike at the 60-min opening-range breakout level ($0.01 buffer). **Built-in $140 stop + $50 profit target** (else expire).
- **Filters:** Mon/Tue/Wed/Fri only; FOMC excluded; entries before 2pm; min credit $0.70. Author tag "Backtest: None" — community-validated only (1.1k clones, ~27–32 active live).
- **Leaderboard vs ORB 60m:** **78.1% instance profitability vs 53.3%**, avg loss −$326 vs −$650 (tail ~halved), PF 1.27 vs 1.13, WR ~78% vs 81%, 27 traders.
- **Rationale:** the narrower wing pre-commits the loss cap at entry (no stop-loss whipsaw / late-day chase / hedge-fill drift). **Reframed the ORB Matrix-v0 A/B** — instead of building a 90%-stop clone of ORB 60m, run ORB 60m vs the marketplace-validated 10-Wide as the comparison. Caveat: the package bundles narrower wing + stop + day/FOMC filters, so the A/B can't isolate which improvement does the work.
- **Paper:** $10K (`60min-ORB-10W-Paper-v1`).

#### Weekly IB SPY — doug37866  *(added pre-travel, May 2026)*
- **Structure:** SPY weekly **iron butterfly, ATM shorts** (symmetric). 30% rate-of-return scanner threshold, 7 configurable inputs. 5-year-old template (2021).
- **DTE:** 5–7 weekly.
- **Exit:** 50% profit-take primary; 25% if <4 DTE; forced close at 2 DTE (IB Monitor automation). Structural wing cap, no stop.
- **Paper:** $10K full size (exit logic robust enough for unattended operation).

#### 1:45pm Sandwich — Jack Slocum  *(added pre-travel; paused)*
- Time-of-day short-vol bot. **No author backtest** ("Backtest: None"). Stage-2 read confirmed **short-vol, not long-vol** (did not fill the convexity gap). **Paused after a 0-for-6 losing streak during the travel period.**

---

### 5.3 Watching (captured, not cloned)

#### Pink Panther [↑↓] BPS/BCS — XSP/SPX (v6 + v14) — Pink Panther (@pinkp)
- **Structure:** Directionally-rotating SPS/SCS with a multi-indicator regime classifier (100 EMA, RSI/CCI/STOCH/MACD, 9/20 EMA cross with 8-day persistence since v7, IV Rank), DTE waterfall 15–40 (5 buckets cycling), VIX gate (35+ blocks opens), and a **layered hedge architecture.** Default deltas: short put −0.14 / short call +0.09 (bullish skew). Bull regime opens SPS, bear opens SCS.
- **Exit (v14, 4 layers):** (a) 90% direct + Market Reversal close (≥10% profit + regime flip, added v11); (b) DTE-adjusted profit ladder (10 rungs); (c) raw-breach close + hedge (strike-matched OR expected-move-offset, added v14); (d) **VIX-conditional sustained-breach stop** — `VIX Δ ≥ 3 over 2 market days AND DTE < 10 AND return% < −100 → close`.
- **The stable primitive:** those VIX-stop thresholds are **unchanged across all 8 v6→v14 iterations** (and across the sibling Vertical Assets, v19) — the strongest revealed-preference signal in the capture set. The author tuned everything else and never touched these.
- **v6→v14 evolution (all defensive):** removed user-configurable Hedge Expiration (the Robert DiNero footgun); added expected-move-offset hedges; added Market Reversal close; 8-day regime confirmation; ITM Warning 35%→30%; 1pm Early Warning gate. Revised Matrix verdict: **"already well-hedged, do nothing."**
- **Stats (v6 cohort, All-time Live):** $22.72K, 115 instances, 90 traders, **56.5% instance profitability**, 85.7% WR on 3,354 trades, avg win/loss $93/−$508 (0.18), PF 1.09. **Buffer 1.2 pt — thinnest captured.** v14 (4 days old at capture) has ~no cohort data.
- **Why no clone (Path 1):** Trendy covers the same raw-breach-hedge SPY-family failure class with far better stats (PF 1.44 vs 1.09, 5 pt buffer vs 1.2 pt, 11,700 vs 3,354 trades). Pink Panther's bear-SCS rotation partially overlaps ORB's bear behavior. The Matrix tuple can be sent without cloning. **Never live-ready** in $50K SPX mode at current capital.

#### Pink Panther Vertical Assets v19 — Pink Panther (@pinkp)
- **Structure:** Bull-biased SPS + tactical (always super-conservative) bear SCS, with **user-selectable Risk Profile** (Conservative/Balanced/Aggressive/Auto → 3 BPS delta tiers, −0.06→−0.14, across 5 DTE buckets D1–D5 = 15–35 days). Adds **Call Side Profit Boost** (0DTE BPS→IC conversion, 11am–1pm) — a **structural modification of *winning* positions** (new Matrix category: not a hedge, not a profit target). Inherits the VIX-conditional stop unchanged. Adds configurable **Hedge Position Size** (1×–2×).
- **No live cohort yet** (v1 = Jan 2026). Not cloned (same Path-1 correlation logic). Matrix tuple ready to send.

#### TFMITH-The Hare (v6.23) — stuart96718
- **Structure:** Long directional premium (calls/puts by momentum), **Martingale position sizing** (L0–L4 tiers scaling up after losses), 5-loss-streak circuit breaker, ~0DTE, 10 user symbols. Profit ladder (max 500%), 1:55pm fallback close >25%. No stop.
- **Stats:** $52.81K, 57 instances, 63.4% WR on 1,238 trades, avg win/loss $227/−$277 (**0.82, most balanced**), PF 1.42.
- **Demoted because:** severe version sprawl (author: "I've created a mess…"; running v6.3.1 while leaderboard tracks v6.23); author called v6.4 a failure; **Martingale on long premium is a hard avoid** (zzkazu nearly opened 383 contracts after a loss streak — fixed-capital allocation explodes contract count when option prices crash). Revisit only if the author publishes a stable named version or a fork removes the Martingale.

---

### 5.4 Killed

#### Kirk Hybrid Trading [Bot Workshop] — Kirk Du Plessis  *(killed pre-capture, 2026-04-19)*
- Appeared rank-3 All-time Live ($143K, 1k clones). **0 scanners, 1 monitor, 4 manual buttons** → a manual/automated hybrid workshop teaching template, not an autonomous bot. The $143K is operator skill, not replicable edge.
- **Lesson — the manual-entry trap:** a bot with 0 scanners cannot have "edge" in the sense this project cares about. Produced the binding **count-scanners-before-capturing** rule. Not revisited (structural mismatch, not tuning).

#### Opening Range Breakout 60m — Jack Slocum  *(killed ~May 2026, per Matrix v0)*
- **Structure:** Fade-the-breakout — two parallel 0DTE SPX credit spreads fired *against* the 60-min opening-range breakout direction. Test A (clean bull break) → SPS $0.01 below range low, $15-wide; Test B (clean bear break) → SCS $0.01 above range high, $15-wide. Compound gate (skip half-days, skip FOMC, clean one-sided breakout only, range width ≥ 0.2% of open). **Zero inputs.** **Zero exit logic** — all positions held to 0DTE expiry. **Technical-level-anchored** short strike (new Matrix distance category).
- **Backtest (3 yr, 601 trades):** $23,387 P/L, −$3,453 max DD, PF 1.44, 89.4% WR (537W/64L), avg win/loss $143/−$832.
- **Live degradation:** WR 81.7% (−8 pt), avg P/L $19 vs $39 (~50% degradation), PF 1.17, **55.5% instance profitability** (lowest on shortlist). Causes: 0DTE slippage, no exit logic (positions at the mercy of 4pm), possible regime shift.
- **Matrix v0 prescription (accepted 4/23):** Class E "unprotected-but-protectable" → **90% hard stop.** Defensibility: at 90% the backtest shows exactly 24 firings, all full-assignment losses, **zero partial losers in the 90–99% bucket** (no intraday-trajectory ambiguity); simulation is a lower bound; 2025-weighted it's better (8 of 24 assignments in a half-year sample). Simulated effect: $23,387 → $26,505 (+$3,118 / +13%), max DD −10%. 58.6% of total loss dollars come from full-assignment events; the 90% stop catches 100% of them.
- **Why killed instead:** by the 5/4–5/17 window, paper showed **six documented tail-loss events** and **negative per-trade EV (~−$137)**, with a **bimodal loss distribution** confirming 90% as the uniquely defensible threshold. ORB was the entire portfolio drag (portfolio +$2,132 with ORB; +$3,983 without). There was no information value in collecting more — kill the vanilla bleeder and let 60Min ORB 10 Wide carry the slot. ORB's confirmed live pathology (a single lucky early fill made it look strong before the max-loss events emerged) became the cleanest case study fed back to Matrix v1.

---

## 6. The Hedge Classification Matrix workstream (cross-project)

**What it is:** Project #8 delivers a 6-field classification tuple per captured bot to the 0DTE Project, which builds a "Hedge Classification Matrix" that prescribes, per bot class, whether to add a hedge/stop, do nothing, or consider killing.

**Milestones:** 10 captures = Matrix v0; 25 = v1; 50 = locked (prescriptions applied to clones).
**Status:** **v0 reached (10 tuples).** Tracking toward 25. Tuples sent weekly as a batch.

**Matrix v0 result:** "do nothing" for 6 of 7 paper clones; **90% hard stop for ORB** (the lone Class E intervention).

**Key cross-batch synthesis points delivered:**
1. **VIX-conditional sustained-breach stop is a stable primitive** — unchanged across 3 Pink Panther bots / 27 version iterations. Treat thresholds as validated.
2. **"Hedges destroy edge" has direct empirical proof** — BWB's same-trades stop/no-stop backtest = 6.2× net destruction. The cleanest calibration datapoint.
3. **New dimension proposed: structural vs dynamic hedges/stops** — structural (wings/long legs, passive, paid at entry); dynamic hedges (breach-triggered); dynamic stops (compound-trigger close-outs). Dynamic interventions may be net-negative on bots that already have good structural hedges + wide buffers.
4. **WR buffer varies 12× across bots** — prescriptions calibrated to buffer, not uniform.
5. **Pink Panther ↔ Trendy correlation** — same failure mode; a prescription for one likely applies to both; a single VIX shock could fire both breach responses simultaneously.

**New categories surfaced by the capture set:** technical-level-anchored strike (ORB); zero-exit-logic (ORB); mechanical time-exit as risk management (Tasty); fixed-dollar-below-market offset + exact-DTE match (BWB); long-premium debit-spread asymmetry (QQQ); user-selectable delta ladder + "Profit Boost" winning-position modification (Vertical Assets).

**A/B protocol design (ORB, before the kill):** Phase 1 vanilla observation; Phase 2 `ORB-Stop90` clone for ≥30 trades; Phase 3 per-event stop-trigger logging (trade ID, time-of-trigger, breach depth, would-have-been vanilla P/L) → Matrix v1 compound-trigger training data. Fallback: screenshot each trigger + `orb_ab_trigger_log.csv`. The Matrix v1 compound trigger (intraday move + P/L + time-remaining gates) is blocked on intraday SPX tick data 2022–2025 that the project doesn't have — hence the 90% hard stop as v0.

---

## 7. Portfolio hypothesis & regime coverage

**H1 — "Short-Premium Core + Long-Premium Diversifier"** (the pre-paper-data starting portfolio, 7 bots, $85K of $100K).

**Regime coverage grid** (+ profit, 0 break-even/sit-out, − loss):

| Regime | 3DTE | Nigiri | Trendy | Tasty | ORB | QQQ LC | BWB | Net |
|---|---|---|---|---|---|---|---|---|
| Low vol / chop | + | + | + | + | + | 0 | + | Strongly positive |
| High vol (VIX 25–35) | − | 0 | 0 | 0 | 0 | 0 | 0 | Sit out / small loss |
| Very high vol (35+) | −− | − | 0 | 0 | ?? | − | 0/− | Loss |
| Bull trend (steady) | + | + | + | + | 0 | ++ | + | Strongly positive |
| Bull trend (fast rally) | 0 | 0 | 0 | 0 | − | ++ | − | QQQ carries; BWB call-wing risk |
| Bear (slow grind) | − | − | − | − | 0 | −− | − | Bleeds |
| Bear (sharp gap-down) | −−− | −− | −− | − | ?? | − | −− | Worst case |
| Multi-day drift (Mar '26) | −−− | − | − | 0 | 0 | − | − | 3DTE's documented failure |
| Event (FOMC/earnings) | ?? | ?? | ?? | 0 | ?? | ?? | ?? | **Uncovered** |

**Honest diversification accounting:** four DTE profiles spread across the curve, but **5 of 6 bots on S&P products** (SPX≈SPY ~1:1); **no event-driven exposure; no bear-regime profit source; gap-down tail risk is stacked, not hedged** (one bad Monday hits 5 of 6). Two bots (3DTE 46%, ORB 55.5%) show most operators lose money. **The portfolio is optimized for the regime we've been in, not the one we may be entering.**

**Worst-case correlation (2-week sustained drift):** −$14K to −$24.5K ≈ **16–29% drawdown** on $85K — survivable on paper, nightmarish on a live $10K account; ~2× scaling headroom needed before any live mirror.

**Scaling reality:** only **Tasty Condor and BWB fit a $5K live account cleanly.** Everything else needs $10K+ due to per-contract max-loss math. The "works at $2K" criterion is **not met by 4 of 6 bots** — at a $2K live start you'd pick 1–2 bots, not 6.

**Expected paper P/L (illustrative, not predictions):** conservative $300–800/mo (~5–10% ann.); base $800–1,500/mo (~12–20%); optimistic $1,500–2,500/mo (~20–35%). Realistic first-90-day expectation: $0–1,500/mo with 1–2 drawdown weeks that feel like −$2K to −$4K before recovery.

---

## 8. OA platform knowledge

**Core tools (confirmed 2026-04-17):** Autotrading Bot Builder (visual flowchart; Delta/DTE/IV-Rank criteria); Exit Options automation (1-min monitoring); SmartPricing (algorithmic limit placement, Patient/Normal/Fast); Backtester; Screener; Trade Ideas; 0DTE Oracle; positions dashboard. Any bot is saveable as a template, shared public/private, cloned one-click with all settings. The community leaderboard ranks public templates by paper and live performance.

**0DTE Oracle:** backtests the exact current-market metrics against 1 year of intraday minute data; SPX/XSP only; risk-defined strategies only (no calendars/diagonals/straddles/strangles); refreshes every minute. Reframed in this project as a **live screener** — value comes from longitudinal logging, not one-time scoping; usable as an entry filter or a "don't trade today" signal.

**Earnings Edge:** tests position metrics (OTM%, credit/debit, width, max loss) across 5 years of earnings reports.

**Webhooks:** inbound signals trigger automations; connects to TradingView, email, Python, TTM Squeeze. **Deferred** until a concrete trigger (an Oracle pattern worth automating, an external signal to route in, or 0DTE-Project hedge logic OA's recipe language can't express).

**Broker integrations:** Tradier, TradeStation (platform free if either is connected).

**Feb 2026 release:** monthly/weekday/hourly result breakdowns; DTE/day-of-week/hour-of-day filters; OI + volume with call/put split; P/L-or-capital with drawdown toggle.
**March 2026 release:** $ or % strike increments; prev-day-close or today's-open entry; calendar/market DTE check; "Analyze" export to Excel/AI; Flat Flyer template.

**Leaderboard quirks (from real use):**
- Stats aggregate across all instances **regardless of how positions were opened** → the leaderboard **cannot distinguish autonomous bots from manual-hybrid tools** (Kirk Hybrid). Count scanners.
- Authors post multiple parallel URLs for one bot (OA assigns a unique ID per save) — even Pink Panther lost track of which is latest.
- Version history is visible on every template page and is an author-quality signal.
- The UI **Min Trades filter maxes at 10** — apply the 100-trade floor in analysis, not in the UI.
- **Exit Monitor "market days" ≠ calendar days** (QQQ's 30 market days ≈ 45 calendar) — a common source of confusion.
- 2-hours-to-expiry **force-close** behavior is a real edge case bots guard against (Nigiri's 0-Day ITM Check).

**Re-scope trigger:** re-run a *targeted* web search (not the full bootstrapping protocol) only when OA ships a major feature or the platform behaves differently than described.

---

## 9. Research conducted & where it's stored

**Tooling & sources used:**
- **HTML capture pipeline** — Chrome Save-As (Webpage Complete), 5 saves/bot + screenshot backups; Python/BeautifulSoup parsing in the bash tool.
- **Custom Reddit scraping** — `reddit_comments_v2.py` against `old.reddit.com/.json`; engagement thresholds score ≥50 / comments ≥30; ~40% of actionable findings live in comments.
- **Firecrawl API** — public web discovery (non-auth-walled).
- **Chrome MCP** — attempted, blocked by allowlist; **Playwright MCP** = identified fallback for auth-walled captures.
- **Option Omega** — backtesting platform (used in Project #1; planned for Stage 2 custom builds here).
- **Notion** — project home pages + dashboard database.
- Key subreddits r/thetagang, r/VegaGang, r/PMTraders; Substack `leptokurticapital` flagged high-priority.

**Research performed:**
- **Leaderboard mining:** seven 90-day snapshots across six sort orders + All-time Live + All-time All-Trades (sanity only). ~25 bots identified at the ≥100-live-trade floor; shortlist of ~12.
- **10 full bot captures** (parsed HTML + community comment analysis, 110,000+ chars on some threads): 3DTE, TFMITH, Nigiri, Trendy, Tasty Condor, ORB 60m, Pink Panther v6, Pink Panther v14, QQQ long call, Pink Panther Vertical Assets v19, Friday 14 DTE BWB. Plus the three pre-travel captures (60Min ORB 10 Wide, 1:45pm Sandwich, Weekly IB SPY).
- **ORB backtest validation:** exported OA backtester HTML for Variant A (316 bull SPS) + Variant B (285 bear SCS), parsed to CSV reconciling to the penny ($23,387 / 89.4% / 601 trades); loss-distribution analysis (24 full-assignment losses = 58.6% of loss dollars, zero in 90–99% bucket).
- **Variant logging** per bot (community forks): e.g. 3DTE (Detective31VPM −500% ROR overlay, Richard R close-if-ITM); Nigiri (arzinator 5-delta + stop, Ziv PoP monitor); Trendy (JaniZ 100%-stop hedge, Trader_Joe SCS mirror, Momentum Trader close-on-breach); Tasty (Lee Dunkelberger Trade-Ideas, Shiv ITM extension, Mikey D ladder, UncleRico delta-neutral *cautionary tale*, david83963 SPX); QQQ LC (NCR VIX/IVRank toggle, vishal3270 $6-drop dip-buy); BWB (Otto's Ratio Asymmetrical Condor 50 DTE, Jared T Tank Hedge, David K all-put); plus full Pink Panther v4→v19 author iteration history.
- **Strategic planning:** factor-bucket framework, five-stage roadmap (HTML artifact built), long-vol sourcing analysis (confirmed largely absent from OA), Stage-1 long-vol filter, Stage-2 custom-build path via Option Omega + Project #1 hedge IP.

**Where everything is stored (file map):**

| File | Contents |
|---|---|
| `project-setup.md` | Purpose, capital plan, platform setup, parallel-project firewall, file map |
| `research-phase-sequence.md` | The reasoning doc — phases, capture pipeline, capture template, continuous rules, scope log |
| `research-progress.md` | Living checklist — per-phase status, capture/tuple tracking, next-session priorities |
| `bots-tracked.md` | The living bot inventory — one section per bot (full mechanics, stats, analysis, decisions, Matrix tuple, variants, capture refs) |
| `portfolio-hypotheses.md` | H1 + regime grid, diversification accounting, correlation scenarios, allocation/scaling tables, graduation & kill criteria |
| `matrix-tuple-batch-v0.md` | The 10-tuple v0 delivery to the 0DTE Project + cross-batch synthesis points |
| `kill-log.md` | Dropped bots/hypotheses + lessons (prevents re-mirroring) |
| `oa-feature-notes.md` | Personal notes on OA tool behavior, leaderboard quirks, the manual-entry & sample-size traps |
| `oa-specialist-full-spec.md` | Workflow descriptions, output formats, column-priority guidance, knowledge-bootstrapping record |
| `leaderboard-snapshots_README.md` (+ snapshot files) | Weekly leaderboard pastes (naming `YYYY-MM-DD_<sort>_<scope>.md`) |

**Capture asset paths:** bot HTML in one folder per bot (e.g. `3dte_140-350/01_main.html`, `friday_14dte_bwb/`, `qqq_long_call/`, `pink_panther_vertical_assets/`); parsed entries live in `bots-tracked.md`; classification tuples under each bot's `Matrix Tuple` heading. Project files at `/mnt/project/` (read-only); outputs staged at `/mnt/user-data/outputs/` for manual sync. Session continuity is file-based: living docs regenerated at session end, old versions deleted.

---

## 10. Standing principles & hard rules (condensed)

- Teach the *why* behind every recommendation; push back on weak ideas and flag real risks.
- Never fabricate win rates, follower counts, or stats — if data isn't provided, say so and request it.
- Every strategy recommendation includes: mechanics, edge rationale, capital requirement, risk profile, portfolio fit, what to pair it with.
- Flag sample-size risk on any bot with <100 backtested trades or <6 months live.
- Flag undefined-risk on a small account once, then execute if confirmed.
- "Do nothing" on hedging is binding, not suggested — no speculative hedges outside Matrix-confirmed classes.
- All-time *Live* is the signal source; instance profitability beats trade WR; always run the expectancy math sanity check; calibrate interventions to the WR buffer.
- Stop-loss destroys edge on high-WR positive-theta structures with structural caps (BWB proof, 6.2×); stop-loss also harms BWB-class bots generally; Martingale sizing is a hard avoid.
- Count scanners before capturing; verify author intent before trusting a leaderboard rank.
- Pre-commit kill thresholds in writing before data arrives.
