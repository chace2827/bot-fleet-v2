# Hedge program — the north star

**STATUS: direction document — the aim, not an authorization.** Written 2026-09-16 at Andy's
explicit instruction: *"build me a new hedging guide as our north star going forward."* It merges
the Cowork strategy chat (sections "The honest verdict" and "How I'd run the research natively,"
pasted by Andy into the Devin session of the same date) with this project's signed rulings and
post-cutover evidence. **It changes no decision.** What gets built still requires "amend the
plan," pre-registration, and the gates in `CLAUDE.md` §4–§5. Where the chat conflicts with
evidence produced after it was written, the evidence wins and the conflict is flagged, not
smoothed over.

---

## 1. The definition (signed)

`R-2026-09-16-HEDGE-DEFINITION` — Andy, verbatim: *"separate protective position, exit
strategy != hedge."*

- A **hedge** is a SEPARATE protective position, opened while the primary position is already
  on, that pays when the primary loses.
- PT, SL, S2, Touch, ride, defang are **exits**. They may still be built, ranked and improved —
  as exits. They may never discharge a hedge item.
- `hedge-research.md` §1.3 is overruled (banner applied 2026-09-16). The fleet-wide terminology
  sweep is open and unruled.

## 2. The loss signature the hedge exists to kill

All from the post-cutover ledger — `hedge-design-spec-2026-09-16.md` §2, which cites
`data/trades.csv`:

- **Every dollar of loss came from an exit.** −$11,211 across 35 positions; nothing held to
  settlement has ever lost (56 expired legs, +$12,525).
- **It is a clock, not a magnitude.** 75% of losers take their worst tick after 14:00 ET vs 32%
  of winners; 89% of all loss has its MAE inside 14:00–15:30. Underlying net move on the worst
  days is ±0.20–0.78% — the largest move day was a +$1,142 winner.
- **Losers were green first.** 24 of 30 had positive MFE (median +0.70%); the give-back happens
  in the last two hours.
- **The exits book the extreme.** 40% of losers close within 5 minutes of their own MAE vs 6%
  of winners.

⚠️ **Correction to the chat's framing, carried deliberately:** the chat says *"condors mostly
die on large directional moves."* That is the v1 mental model. This fleet's post-cutover losses
are **late-day give-backs to the short strike on small-net-move days**. The tested-side debit
spread still maps — MAE at the short strike means the underlying traveled to it intraday — but
"protection against big days" is the wrong spec. The spec is: *offset the 14:00–15:30 give-back
without taxing the days that never come near the strike.*

## 3. The strategy — native first, reactive, separate

The chat's directive, ratified in substance by the ruling:

> After a position opens and starts losing, the platform reads a trigger and deploys a NEW
> position — a hedge — on top of it.

**What OA can do natively** (verified against `oa-platform-reference.md` §4, §11 and the
2026-09-16 Phase-0 backtester recon):

- A **Monitor automation can OPEN a new position** — Scanner/Monitor are organizational labels,
  not different objects. The reactive shape is buildable today as a bot.
- Native trigger inputs read every minute: position return %, underlying % move since open,
  short-strike touch, VIX level, time of day.
- So: *"if this condor is down X% or the put short strike is touched after 14:00, buy a debit
  spread on the tested side"* — **buildable today, on paper.**

**What OA cannot do** (§11, all load-bearing):

- "Sustained for N minutes," any condition referencing its own past (the give-back-from-MFE
  trigger T-H1 is dead as a decision node), intraday indicators, mid-trade regime branching.
- **The "read the market and choose the response" version requires a webhook** — signal computed
  off-platform (VPS), pushed in. Months of plumbing; untestable in either backtester.

**Why native first (the chat's honest verdict, condensed):** it is real protection with no
infrastructure; it is running and producing evidence within weeks; and it prices the smart
version — if the dumb trigger already recovers most of the loss, regime-awareness adds little;
if it bleeds on whipsaw, the false-fire cluster tells you exactly what the webhook signal must
filter. The $15,376 `HedgeD-Conditional` loss is the standing warning against building what the
platform silently substitutes.

**Venue:** a paper clone built to spec — never the champion `IC-SPX-FastPT25-S2-130PM` itself
(standing exception, `CLAUDE.md` §5), and the HedgeA–D fleet exists on the roster, all OFF.
Every arm needs the five conditions of `hedge-research.md` §5.2 and a pre-registration entry —
no entry, no restart.

## 4. The research method — joined backtests

> **[CORRECTED 2026-09-16 — this section's premise was factually falsified; the correction is
> now **RULED 2026-09-16** — Andy in-chat to Devin, verbatim: *"Slot 1 - rule it"* —
> `R-2026-09-16-BACKTEST-COMBINE-S1`. The replacement below is in force.]**
>
> "The way around it" was written as though OA offered no native way to combine backtests. It
> does. Evidence, on two independent surfaces:
>
> - `data/oa_facts.csv` **OA-1077**, DOCUMENTED, verbatim: *"Then, combine the results of multiple
>   strategies into one portfolio curve."*
> - `data/oa_facts.csv` **OA-1091**, DOCUMENTED, verbatim: *"and combine multiple backtested
>   strategies to see a single portfolio P/L curve."*
> - `data/oa_facts.csv` **OA-1090**, DOCUMENTED, verbatim: *"and compare up to four backtests
>   simultaneously,"* — note that ceiling of **four** against this section's **five**-variant frame.
> - `data/oa_facts.csv` **OA-1143 / OA-1144**, DOCS-SILENT: the *procedure* for comparing and for
>   combining is documented nowhere, which is why the capability could be harvested and still not
>   surface as a method.
> - Dated first-hand device read **2026-09-16 22:37:58-04:00**,
>   `data/captures/2026-09-16-oa-backtester/01-backtest-settings-form-2026-09-16-223758.txt`
>   sha256 `02376a44a3b60afdaf069974ae50292f4cdc93e2bfe10003413ae6fcfebe9973`, lines 219-222:
>   `/backtests/compare/<ids>` renders verbatim
>   `Compare Backtests · Save · Add Backtest · Results · Combine Results`.
>
> The platform-wall sentence below remains true **per backtest** and is irrelevant **across**
> backtests — `Position Limit: 1 position` is a per-config constraint, which is why combining
> works. Under the drafted replacement, V1, V2 and V4 become native combines and only V3 keeps a
> manual join. ⚠️ Combination is expected to be **additive at the portfolio level** — UNVERIFIED —
> so a combined overlay is not a reactive hedge under `R-2026-09-16-HEDGE-DEFINITION`.


**The platform wall (confirmed twice):** neither OO nor OA's backtester can open a second
position mid-trade — chat premise, and the 2026-09-16 Phase-0 UI recon answered **NO**
(single-structure: 8 fixed strategies, "Position Limit: 1 position," one position per
expiration, exits-only exit stack; entry filters are all underlying-market state).

**The way around it — RULED 2026-09-16 (Slot 1):** OA combines backtests **natively**.
`/backtests/compare/<ids>` exposes `Add Backtest` and `Combine Results` (first-hand capture
2026-09-16, sha `02376a44…`), and **OA-1077** documents *"combine the results of multiple
strategies into one portfolio curve."* Run each hedge structure as its own standalone backtest
over the fixed frame, then combine it with the condor backtest in the Compare surface. The
manual day-by-day join is reserved for **V3 alone** — its trigger references the condor's own
P&L and cannot be expressed as an independent backtest's entry filter. One hand-joined variant
is retained anyway as a cross-check on the native result.

**The variant frame (V0–V4, fixed frame: period, seed, symbol, sizing):**

| Variant | Construction | How tested |
|---|---|---|
| **V0** | 130PM condor, no hedge | Native backtest — the control everything is measured against |
| **V1** | Short-strike touch → tested-side debit spread | **Native combine** — trigger is underlying state, so it runs as its own backtest |
| **V2** | Underlying % move since open → debit spread | **Native combine** — same |
| **V3** | Condor return −X% → debit spread | **Manual join** — the only cross-position variant left; still **approximate** — needs intraday option marks (the owed premium path, spec §3.3; Tradier tape is the in-repo source) |
| **V4** | Far-OTM put / strangle bought at 1:30 alongside the condor | **Native combine** — trigger = entry time |

**Mapping to the dispatched arms:** V0 = H-0 (control, runs first); V1–V3 are the H-A family
realized through the join rather than in one test; V4 is the entry-time overlay the dispatch
didn't yet name; H-C (SL100/SL200) stands separately as the incumbent-exit bar — **an exit any
hedge must beat, and both are net-negative live.**

**What the research must produce, in order:**

1. **Loss anatomy** — which days lose, which side, when the loss develops, how concentrated.
   (Post-cutover answer exists: §2 above. The backtest extends it over ~3 years, not 27 days.)
2. **Trigger quality per native trigger** — recall on losing days; false fires on winning days
   (the whipsaw cost); lead time vs the loss.
3. **Hedge payoff given a fire** — cost per fire, payout on true fires, bleed on false ones.
4. **Combined result** — net P&L, worst day, worst-5, max drawdown, and the decision metric:
   **tail loss removed per dollar of drag.**

**The single screen (the chat's compare spec):** five equity curves overlaid · stats table one
column per variant · a day-strip heatmap sorted by V0 loss (a good hedge pales the red rows and
leaves the rest untouched) · condor-P/L × hedge-P/L scatter (want negative slope on the left,
nothing on the right) · histogram of fire times vs loss-arrival times.

**The pass bar is written before any results come back**, and each run's config record is
verified — the `text`/`textValues` display-string trap is proven real
(`docs/experiments/oa-rpc-test-2026-09-15/`).

**Hold-out for free:** run the full ~3 years once, export/transcribe the trade list, split
years 1–2 vs year 3 in analysis.

## 5. The authorization boundary — as it stands TODAY

This is where the chat is stale, and the correction is binding:

- **UI path only.** OA's written grant is scoped: Devin's own browser driving the interface —
  yes. The `zdte.*` wire protocol, request replay, traffic recorders, network inspection —
  **no** (`R-2026-09-16-DEVIN-OA-CHROME-CAPTURE` as amended by `-A1`). DOM/JS reads of page
  state — `input.value`, hidden inputs, hydrated models — are **inside** the grant
  (`R-2026-09-16-BACKTEST-COMBINE-S4`, ruled 2026-09-16): the Chrome-era read method was
  exactly this, and "the inspection portion" means the API-discovery path, not DOM reads. The chat's "each runs
  through `zdte.startTest`" is **withdrawn as a plan**; the RPC verification is history, not a
  toolkit. If Andy wants that speed back it takes a broader written grant, stated plainly:
  ~200 scripted backtests, serial, no parallelism.
- **What UI-only costs: scale.** One backtest at a time, hand-constructed, ~5–8 min each for a
  mapped family plus a discovery pass per new shape. The grid survives; *which hypotheses get
  run now matters more than coverage* — §2's ranked candidates are the pruning order.
- **Every agent-created backtest is named `ZZ-AGENT-<YYYY-MM-DD>-<arm>`** (`-A2`). No exceptions.
- **Assume no export** (`docs/AI Agent Stack.md`:256 — confirm first-hand on the results
  screen). The capture bundle is the primary record: config verbatim + results transcribed +
  screenshots + sha256. A number whose config wasn't captured can't be re-derived.
- **T4 evidence, ceiling.** Backtest figures support paper arms and measurement only — never a
  live-capital decision (`CLAUDE.md` §4: T2 needs n≥100 / 6 months / a regime change).

## 6. From backtest to bot — what winning produces

The winning variant *is* the Monitor automation's spec:

- which trigger, at what threshold;
- which structure (width, delta), at what size ratio to the condor;
- a no-hedge-after cutoff, if late fires don't pay;
- the hedge's own exit rule (hold to close vs close with the condor);
- a **pre-registered paper expectation** — e.g. "≈3 fires/month, worst-day loss cut ≈40%" — so
  the paper bots have a bar to hit, not just a thing to watch;
- and the webhook answer from evidence: if false fires cluster on identifiable chop days, the
  VPS regime filter earns its build; if they don't, native is enough.

**The paper phase cannot be shortened** — it depends on how often the hedge fires. A 3–5
fires/month trigger needs 2–3 months for ~10 fires. Joined backtests buy sample; only paper
proves live mechanics (slippage at a 15:00 touch is exactly what joined results assume away).

## 7. The precondition the chat asked for — the assumption register

Before the backtest day, one sitting: pull every sentence in the six core docs that is a *rule*
rather than a fact; tag each with origin (v1 / 7-27 audit / Andy's ruling / Cowork's), its
evidence, and whether anything post-08-10 tested it. ≈30–50 assumptions to ratify or strike.

Two already-known examples of why: a carried-forward v1 finding ("min-credit filter hurts")
contradicts the $0.07 credit filter currently stripping the call side off every GF arm; and
"stop losses are counterproductive on the Fortress structure" is the ancestor of the champion
running with no stop and no hedge today. Whether the register runs before or after the first
grid is Andy's call — **unruled.**

## 8. Cost and calendar (merged estimates)

| Route | ~175-run grid | Calendar |
|---|---|---|
| Devin driving the UI (authorized path) | ~5–8 min/run → ~25–30 agent-hrs | ~2–4 weeks |
| You by hand | ~8–10 min/run → ~25–30 hrs | 5–7 weeks |
| `zdte.*` scripted | ~2–3 min/run → ~1–2 days | **Parked — not authorized** |

Chat calendar, adjusted for the UI-only path: nav/recon + fixed frame this week (Phase 0 done,
H-0 next) → hedge grids + refinement + hold-out over weeks 1–3 → hedge bots on paper late
October with fires/month and worst-day reduction written down in advance → first paper read
late November → a trustworthy read December–January. One decision sitting at the end of the
grid, not a ruling per step — otherwise review, not backtests, becomes the bottleneck.

## 9. What would change this document

- Phase-1 results that invert §2's signature (e.g., loss arriving before 14:00 over the 3-year
  sample).
- A broader OA grant reopening the RPC path — scale assumptions get rewritten.
- Any amendment to `R-2026-09-16-HEDGE-DEFINITION`.
- The assumption register striking a carried-forward rule this document leans on.

---

**Provenance.** Chat content: Andy's paste into the Devin session, 2026-09-16 (the
claude.ai share `7e2b86c3…` could not be fetched programmatically — Cloudflare interstitial —
so the pasted text is the source of record). Project evidence: `hedge-design-spec-2026-09-16.md`
§2–§6, `decision-card-2026-09-16-tournament-baseline.md`, `dispatch-oa-capture-2026-09-16.md`,
`docs/experiments/oa-rpc-test-2026-09-15/summary.md`, `oa-platform-reference.md` §4/§11/§13,
`hedge-research.md` §5. `RULINGS.md`: `R-2026-09-16-HEDGE-DEFINITION`,
`R-2026-09-16-TOURNAMENT-BASELINE`, `R-2026-09-16-DEVIN-OA-CHROME-CAPTURE` + `-A1` + `-A2`.
