# IC defense / hedge prior art — research summary

Dispatch: `docs/dispatch-ic-defense-research-2026-10-06.md`. Feeds: `docs/handoff-edge-funnel-2026-10-06.md` §5b
(touch-decision hedge). Register: `ic-defense-register.csv` — 66 rows, one per (mechanic × source).
Evidence-type counts: **backtest 17 · live 2 · anecdote 17 · theory 30.** Gathered 2026-10-06; no OA
access used (option-alpha docs MCP only for platform facts).

## Top 10 mechanics, ranked by evidence quality × OA expressibility

| # | Mechanic | Best evidence | OA-expressible | Rows |
|---|----------|---------------|----------------|------|
| 1 | **Fixed-time flat — no positions into the close** (15:45–15:50 cutoff) | backtest context (optionkrafter, n=602) + universal vendor doctrine | native (time exit) | R04, R27, R28, R34 |
| 2 | **Day-level gates** — FOMC/CPI skip, weekday exclusion | two real backtests (optionkrafter n=556; quantish n=603→363, t-test p=0.013) | native (day-of-week + econ-event decisions documented) | R06, R08, R09 (MC), R10 (external data → partial) |
| 3 | **Per-side stop ≈ total credit** ("Breakeven IC") + tighten survivor after first stop (Talon) | live self-reported (~9,000 trades, Apr 2021–); double-stop 8.6% / 15–17% | native per-side exits; state memory needs tags (§5.3) → partial | R31, R32 |
| 4 | **Multiple-of-credit stop** — the best-quantified trade-off | tastytrade 0DTE SPX study via stockwirex: 0.5x stop → 48% would've recovered ≥BE, CVaR −>50%; tastylive multi-DTE studies show stops underperform holding | native (SL Exit Option) | R03, R01, R02, R05 |
| 5 | **VIX-level conditioning** (day-gate or touch-time branch) | Monte Carlo (Sharpe 5.88→8.98, simulated) + regime-anecdote | native — VIX is a readable symbol input | R09, R25 |
| 6 | **Tested-side debit spread / "mouse ear"** — the §5b hedge shape | practitioner worked examples only (anecdote) | partial — Monitor-open is native (R53), but overlapping-strikes failsafe (R55) forbids sharing the condor's strike in-bot; use adjacent strikes or a sibling bot | R47, R48 |
| 7 | **Roll untested side in / convert to iron fly** | tastylive internal studies (n undisclosed → anecdote): +P/L,+WR for rolls; +profit,−WR for fly conversion | partial — close+reopen mechanics native; re-striking untestable in backtester | R12–R17, R14, R22, R23, R29 |
| 8 | **Close tested side only, keep winner (leg out)** | doctrine/worked examples | native — per-spread close | R21, R65 |
| 9 | **Re-entry after a whipsawed exit** | no published results at all; Option Omega ships the feature | partial — Position-closed trigger + scanner re-fire; limits apply | R61, R62 |
| 10 | **Dealer-gamma regime → expect reversion vs momentum** | strongest academic support (Dim/Eraker/Vilkov; Cboe proprietary-data study; Gao et al. JFE w/ OOS) | **no** — needs external level; webhook-only (§11/§12) | R36, R43, R37, R39 |

Notable constraints surfaced: OA's overlapping-strikes failsafe rejects a hedge leg sharing the
condor's strike (R55) — the classic mouse-ear must sit at adjacent strikes or in a second bot; the
bid-ask guard can silently suppress exits in fast markets (R56); automations cap at 15:55 but
Repeating/Date events escape the schedule window (platform ref §4.1/§8.2) — late backstops are legal.

## Mapping to our two loss shapes (`data/loss_register.csv`)

**Shape 1 — reverting touch / whipsaw (08-26, 08-27):** the literature is unambiguous that tight
stops pay badly here — R03's headline is literally our failure mode quantified (~48% of 0.5x-stopped
condors recover to ≥breakeven). Responses with any support: hold/wider buffer (ride), per-side stops
that sacrifice only the tested side (R31–R32), re-entry after revert (R61 — feature exists, results
don't), and gamma-regime conditioning (positive GEX days revert — R36/R43). Doctrine warning: don't
leg out tested side in whipsaw (R65).

**Shape 2 — continuing breach, especially after 15:45 (09-30):** every vendor source converges on
"flat before the final window" (R27/R28/R34 — 'final 10 min are pure gamma noise'); intraday momentum
(R39) says directional days continue into the close; a tested-side debit spread is the only mechanic
that *pays* on continuation (R47/R48); tail overlays (R49) and late-entry-only designs (R58/R63)
sidestep the window entirely. OA can run a Repeating-trigger backstop past 15:55 — inside the breach
window where the fleet's StrikeTouch died on 09-30.

## Conspicuously missing from the literature

1. **Nobody has published a conditional touch response.** Every studied trigger is unconditional —
no "at strike touch, read time/VIX/momentum, then choose hold/close/hedge." §5b's study is open
   ground (Vilkov R40 supports conditioned rules at entry-time; nobody extends it mid-trade).
2. **No whipsaw-vs-continuation labeling on 0DTE.** The 48% recovery stat (R03) is the only
   estimate; nothing splits it by time-of-day, approach speed, or day regime.
3. **The >15:45 window is a blind spot** — universal doctrine is to be flat by then, so nobody
   measures defenses inside it. Our biggest loss lives exactly there.
4. **Hedge-leg fills are never modeled.** Every hedge/adjustment claim is theory or mid-marked; the
   one careful fill study (optionkrafter) shows fills decide the entire edge.
5. **Re-entry after whipsaw** — Option Omega ships it; zero published results anywhere.
6. **No OA-native hedge backtest or track record** — the community template (R51) proves the
   machinery exists natively, but publishes no performance.
7. **Academic work is market-level, not trade-level** — gamma/VRP/momentum papers inform the regime
   variable, never the defense mechanic itself.
8. **Practitioner "predictive entry signal" track record is a negative** — Talon's builder found
   nothing sufficiently predictive for entries on a 71B-row tick DB (R33). Expect the same for the
   touch decision until proven otherwise.

## Caveats on this register

- tastylive studies are real internal studies whose n/period live in video, not text → anecdote-tier
  per the dispatch's mechanical rule; the direction of their findings is consistent across episodes.
- stockwirex reports a tastytrade 0DTE SPX study secondhand (period stated, n not) — the single most
  on-point external result; finding the primary episode would upgrade it.
- TradeAlgo and similar SEO sites publish confident numbers without any study behind them — carried
  as theory; one claimed "12,000-trade tastytrade study" could not be verified and is flagged in R24.
- Monte Carlo (R09) is simulation over fitted distributions — weaker than real-fills backtests.
