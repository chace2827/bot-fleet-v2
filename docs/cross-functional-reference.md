# Systematic Options Trading & Bot Selection — Reference

*Distilled from #09 Cross-Project Research. Standalone: nothing here requires the source files to interpret. Scope: only what applies to systematic options trading, bot selection, strategy methodology, and the Options Alpha (OA) platform. Crypto / Kalshi / sports findings are excluded.*

Finding IDs (F-NNN) are the stable substrate identifiers. Confidence labels follow the substrate ladder defined in §6.

---

## 1. Sizing & risk (apply to every bot, always)

### F-001 — Half-Kelly + reserve floor *(High confidence)*
**Rule:** Never size a premium-selling strategy at full backtest-implied Kelly. Run ~half-Kelly and hold ~25% margin in reserve specifically for vol spikes.

**Mechanism:** Financial returns are leptokurtic — fat tails. Any backtest undersamples those tails (the worst days mostly haven't happened yet in-sample), so the variance and drawdown inputs feeding a Kelly calculation are systematically understated. Kelly computed on those inputs is therefore systematically *too aggressive*. Halving Kelly absorbs the underestimation; the reserve floor exists to survive the vol expansion the backtest didn't see.

**Corroboration:** Multiple practitioners with 30+ years futures experience agreed (get2thePith, sittingGiant, XxNoKnifexX — the last confirming an 81% win rate as claimed, i.e. high WR does *not* exempt you from tail blowups). Sources: Meile13 r/thetagang post 2026-04-30 (434 pts), leptokurtic distribution post in r/PMTraders (14 pts), Leptokurtic Capital Substack.

**Bot-fleet application:** Allocation defaults across the fleet. Size the *aggregate* fleet, not just each bot, at half-Kelly with the reserve held at portfolio level — correlated short-premium bots all bleed simultaneously in a vol spike, so per-bot reserves are not additive protection.

### F-004 — Martingale logic is a hard avoid-criterion *(High confidence)*
**Rule:** Any strategy or bot that recovers losses by sizing up the next entry is high tail-risk. Reject on sight. Add to every project's kill-criteria.

**Mechanism:** Loss-recovery-by-upsizing has positive expectancy across most paths and catastrophic expectancy on the tail — "martingaling only works until it doesn't." It converts a series of small wins into one terminal loss.

**Anecdote vs principle:** The Captain Condor case (reported $50M loss running 0DTE SPX iron condors with double-down behavior; ~$5K/yr subscription, 1000+ followers copying) is the *illustration*. The *principle* is the avoid-criterion — do not confuse the war story for the rule. Source: r/thetagang Captain Condor post + comments (SocraticGoats, UnnameableDegenerate).

**Bot-fleet application:** Screen every bot's configurable inputs for any rule that increases position size, contracts, or allocation after a losing trade. Presence = automatic reject, regardless of backtest. This is the criterion that justified the TFMITH demotion in #8.

---

## 2. Regime detection / entry filters

### F-002 — Vol term structure as entry filter, not just IVR *(Medium-High confidence)*
**Rule:** IV Rank alone is insufficient to gate entry. Read the VIX-futures term structure and act on its *shape*:
- **Front-end backwardation** (near > far) → sell short-DTE premium aggressively.
- **Flat curve at an elevated level** → widen strikes, reduce size.
- **Whole curve shifting up** → sit out, or go long vol.

**Mechanism:** IVR tells you where vol sits relative to its own recent range; term structure tells you what the market expects vol to *do*. Backwardation is the market pricing near-term stress that is expected to resolve — exactly the condition where short-DTE premium is richest relative to realized risk. A parallel upward shift means the whole vol surface is repricing higher; selling into that is selling in front of a trend.

**Sources:** r/VegaGang term-structure post + comments (Connect_Boss6316, Aigpil).

**Bot-fleet application:** Build a term-structure regime overlay that gates bot *activation*, not just entry within an active bot. A premium-selling bot with no vol-regime filter (see F-014) is structurally exposed precisely when the curve shifts up.

### F-005 — Backwardation + double calendar (derived rule) *(Medium confidence)*
**Rule:** Enter double calendars *only* when VIX-futures front-end is in backwardation (short vol high, long vol lower). Do not enter when the curve is flat or in contango.

**Mechanism:** Synthesis of F-002 + F-003. In contango/flat you pay full price for the long-dated leg with no curve tailwind, so the structure's edge evaporates. Backwardation is the specific signal that makes the long leg cheap relative to the short.

---

## 3. Structural strategies

### F-003 — Double calendar as a long-vega income structure *(Medium confidence — strong post, real caveats)*
**What it is:** A vertical (across-time) analogue of the iron condor — long vega *and* long theta simultaneously, achieved with a ~1-week differential (e.g. 2w/3w).

**The binding constraint is gamma, not vega.** Gamma risk near the short strikes is what actually kills the position; whipsaw — price oscillating through the short strikes — does the damage. Requires active roll management at ~3 DTE on the shorts.

**Counterevidence (why it's only Medium):**
- PhotoJCW (2008-era trader): front-month IV moves much faster than back-month, so the "net long vega" claim holds only with a tight term-structure differential.
- FunCranberry112122: holding different *durations* of vol is not the same as being long vega.

**Bot-fleet application:** A candidate structural archetype distinct from the standard IC, but only viable with (a) the F-005 backwardation gate and (b) automated roll logic at 3 DTE. Without both, do not deploy.

---

## 4. Bot selection methodology (OA-specific)

### The triage schema (apply to every bot identically)
1. **Classification** — structure, underlying, DTE, trigger type, exit logic.
2. **Risk flags** — enumerated below.
3. **Mechanical breakdown** — exactly how the bot enters, manages, and exits.
4. **Gaps** — what the template does *not* specify or disclose.
5. **Recommended next actions** — what to pull/test before a verdict.

### OA platform signals
- **Clone activation rate is signal, not noise.** A low activation rate (many clones, few people actually running it) is a flag — the crowd cloned and then declined to deploy, which usually means they found something on inspection.
- **Template age is a survivorship signal.** A 5-year-old template that's still live has survived multiple regimes — a positive, weighable signal (it carried weight in F-014's favor).
- **Configurable-input count is a complexity/overfitting flag.** More inputs = larger overfitting surface and harder quality assessment. 7+ configurable inputs (F-014) materially complicates judging whether the edge is real or curve-fit.
- **No backtest = flag**, not an automatic reject, but it shifts the burden to "scout the author's channels for undisclosed backtests / trade logs" before any verdict.

### Archetype framing (the two poles)
Classify each bot against two structural opposites; most bots sit on the spectrum between them:
- **Event-trigger + tight stops** — enters on a discrete signal, defines risk hard. (Exemplar: F-013.)
- **Pure structural premium capture + no stop** — sells premium continuously, relies on the structure rather than a stop. (Exemplar: F-014.)
This framing lets you reason about *correlation and failure mode* across the fleet rather than evaluating each bot in isolation.

### Worked example A — F-013 candidate: "60Min ORB 10 Wide"
*Author: Arianne / @tradesinLulu. 0DTE SPX short credit spread, 10-wide, triggered on a 60-minute opening-range-breakout (ORB) failure.*
- **Archetype:** Event-trigger with tight stops.
- **Flags:** no backtest; low clone activation rate; demanding break-even win rate (credit is tight relative to the 10-wide, so required WR is high); unexplained Thursday exclusion; ambiguity around how much directional discretion the trigger leaves.
- **Next actions:** scout author's social for any trade log; build a regime-overlay test on historical SPY/SPX; pin down whether Thursday exclusion has a basis (e.g. specific event clustering) or is curve-fit.

### Worked example B — F-014 candidate: "Weekly IB SPY"
*Author: doug37866. Symmetric ATM iron butterfly on SPY at 5–7 DTE, tiered profit exits, no stop loss.*
- **Archetype:** Pure structural premium capture.
- **Positive:** 5-year template age (survivorship).
- **Flags:** no vol-regime filter (directly the F-002 gap); tail exposure from ATM short strikes with no hard stop; 7 configurable inputs complicating quality assessment.
- **Next actions:** build a regime-overlay test on historical SPY; assess whether a term-structure gate (F-002/F-005) would have avoided the worst historical drawdowns; reduce/stress the input set.

---

## 5. Confidence calibration & what counts as a finding

### Confidence ladder
- **High** — multi-source corroboration *plus* math/empirics support. (e.g. F-001 half-Kelly.)
- **Medium** — single strong source + plausible mechanism, ideally with community pushback that sharpened the caveats. (e.g. F-003 double calendar.)
- **Low** — single source, plausible but unverified, often with identified internal inconsistency. (e.g. the asymmetric-IC-wings post — see §7.)
- **Unverified** — posted but no corroboration; flag for follow-up or skip. (e.g. the "ultimate vega play" 70% CAGR claim.)

### What is NOT a finding
- A single P&L brag with no disclosed mechanic.
- A strategy whose author won't disclose the actual rule.
- Something already in the substrate at equal-or-higher confidence.
- Opinion without supporting structure.

### The governing heuristic
**Cross-corroboration beats score.** A 14-point post backed by a 30-year practitioner is higher confidence than a 1000-point post with no informed responses. Upvotes measure popularity; agreement from credible operators measures truth.

---

## 6. Operating disciplines (carry these into the fleet)
- **Distinguish principle from anecdote.** "X lost $50M" is the anecdote; the avoid-criterion is the finding. Never store the war story as the rule.
- **Never invent stats.** If a source claims a win rate, Sharpe, CAGR, or follower count, attribute it explicitly to that source. Unattributed numbers are not allowed.
- **Tag conservatively.** Over-tagging dilutes; under-tagging is cheap to fix. When unsure whether a finding applies to a bot, leave it off.
- **Kill-criteria are cumulative.** Martingale (F-004) and missing vol-regime filter (F-002) join the existing kill-log. A bot can pass on structure and still die on a single hard criterion.

---

## 7. Strategy-discovery sources (options-relevant only)

### Validated
| Source | Type | Best for | Cadence |
|---|---|---|---|
| r/thetagang (`t=year`, **not** `t=week`) | Reddit | Community-vetted short-premium strategy posts | Weekly |
| r/VegaGang | Reddit | Long-vol / hedge discovery — highest S/N for hedges | Monthly |
| r/PMTraders | Reddit | PM-account sophistication, weighty hedging mechanics | Monthly |
| Leptokurtic Capital | Substack | Highest-quality single author found (origin of F-001, F-003) | Monthly |

### Queued (high priority for options)
Tastytrade research blog (publishes SPX 0DTE backtests), Kris Abdelmessih / Moontower (vol structure), Robert Carver (canonical systematic-trading frameworks), Elite Trader options subforum (more SPX-savvy than Reddit).

### Kill-log — patterns to recognize and skip
- **"Won't disclose the mechanic" → skip.** The "Ultimate Vega Play" (u/Right_Business9301): author refused to share the actual rule, likely a WealthyOption clone, unverified 70% CAGR with no disclosed filter for "high-risk days." Demoted from Tier-1 to skip. *Pattern: opacity is the tell.*
- **Small sample + internal inconsistency → skip.** The IV-crush asymmetric-IC-wings author: asymmetric wings are logically inconsistent with an IV-crush thesis (per u/hl_lost), and a 4-trade sample is "a coin flip that went well." *Pattern: a result that contradicts its own stated mechanism is noise.*
- **`t=week` filters on any subreddit → skip.** Weekly tops are dominated by P&L brags and current-events takes (~4/25 substantive). Use `t=year` / `t=all`, which surface community-vetted strategy.

---

## Quick-reference checklist for any new bot

1. Does any rule size *up* after a loss? → **reject** (F-004).
2. Is there a vol-regime / term-structure gate? → if no, flag the F-002 gap.
3. ATM or near-ATM shorts with no hard stop? → flag tail exposure (F-014 pattern).
4. Backtest present? Clone activation rate? Template age? → weigh the OA signals.
5. How many configurable inputs? → more = more overfitting surface (F-014 pattern).
6. Author disclose the full mechanic? → if no, scout channels before any verdict; opacity trends toward skip.
7. Size the *fleet* at half-Kelly with a portfolio-level reserve, not each bot independently (F-001).
