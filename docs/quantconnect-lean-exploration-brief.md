# QuantConnect / LEAN Exploration Brief — Bot Fleet

> Created 2026-06-24 with Andy. **Purpose: a self-contained onboarding brief for Claude research agents**
> joining the Bot Fleet project, covering the new code-backtesting toolchain (QuantConnect / LEAN CLI /
> Polygon) we stood up over 2026-06-23 → 06-24. Read this to get current on *why we added a code engine,
> what it can and can't do, which tool to use for which job, and what we're building toward.* Pairs with
> the deeper docs it points to: `lean-backtesting-reference.md` (verified LEAN code patterns),
> `qc-api-lean-cli.md` (CLI/automation), `backtest-tooling-roi.md` (tool-by-use-case decision),
> `research-roadmap.md` (the P0–P3 schedule).

---

## 0. TL;DR for a new agent

- We added **QuantConnect/LEAN** as a **code backtesting engine** alongside **Option Alpha (OA)**.
- **OA is the default and the live gate** (its backtester *is* its live engine — it predicts live). **LEAN
  is a specialized instrument** for the two things OA fundamentally cannot do: (1) backtest **touch/breach
  hedges** (S2, Defang, Tighten, the breach engine), and (2) run **giant combinatorial sweeps** + null/OOS
  rigor. **LEAN fills run ~4× hot** vs OA, so LEAN ranks; OA validates absolute economics.
- The pipeline is fixed: **LEAN sweeps → OA validates structural survivors → OA paper is the live gate.**
- **Calibration is LOCKED** (LEAN reproduces OA's IC win rate: 92.1% vs 92.6%). We now trust LEAN for win
  rate + relative ranking.
- Immediate goal: a **paper directional bot live for tracking ASAP**, gated only on the **C1 regime
  classifier**. Directional structures + the paper bot are built **in OA**; C1 research is **in LEAN**.
- The CLI/Polygon/automation build is **deferred to the hedge tournament** — that's where code earns its keep.

---

## 1. What we did, 2026-06-23 → 06-24 (the narrative)

### Phase 0 — pick the engine and prove it (06-23)
- **Tooling decision finalized:** evaluated OptionOmega (OO), Polygon, QuantConnect. Chose **LEAN → OA →
  paper**, dropped OO (it can't express our cross-leg/persistence/reclaim hedge logic any better than OA).
  The deciding insight: **OA cannot backtest our touch-triggered hedges at all** — it defers them to paper.
  Code with intraday option data *can*. That's a **capability unlock, not just a speedup.**
- **Calibration discipline:** before trusting any new LEAN result, reproduce a known OA number. Built
  `lean/gap_batch1.py` (SPX 0DTE IC control) as the calibration probe.
- **First calibration (1yr): PASS** — 247 ICs, per-condor win rate 87.9%, internally consistent, directionally
  matching OA. Wrote **`lean-backtesting-reference.md`** = the verified-patterns "skill" (see §6).
- **Fee model:** Tradier **Pro Plus = ~$0.60/contract** all-in → built a custom per-contract `TradierSpxFeeModel`
  (the default ConstantFeeModel was wrong-structured). Set OA commission to match.

### Phase 1 — lock calibration + design the research schedule (06-24)
- **Research roadmap** written (`research-roadmap.md`): the edge is a **chain** — `regime classifier →
  regime-matched structure → matched hedge`. The classifier (C1) and the hedge library are **shared deps**
  across directional days, gap days, and the mirror bots → both are **P0**.
- **Re-prioritization (Andy):** bump **Directional** up to get a **paper bot live ASAP**, but never fire
  directional without **C1** (it bleeds theta on chop days; the momentum thesis is already falsified).
- **CALIBRATION LOCKED** — v5 Control full-window: **707 ICs, per-condor WR 92.1% ≈ OA control 92.6% ✓,
  RoR/IC +1.31%, fees $1,699** (Pro Plus model applying). Two findings carried forward (critical — see §7):
  1. **LEAN RoR ~4× hot** (+1.31% vs OA +0.3%) — fill optimism (LEAN mid/market vs OA SmartPricing + 0.03
     slippage). → trust LEAN for **win rate + relative ranking only**; OA/paper owns absolute economics.
  2. **Quote filter skips ~24% of days** (707 vs OA ~920) — must verify it isn't biased toward calm days
     before trusting any gap/directional result.

### Phase 2 — build the C1 classifier (06-24)
- Built **`lean/c1_regime.py`** (the regime classifier feature recorder) + **`lean/c1_analyze.py`** (offline
  gate sweep + random-day null + bias check). Design: trade ONE naked champion-config IC/day so the IC's
  P&L *is* the day-type label (win = chop/IC day; loss = trend/directional day). Features: **ATM IV, ATR5,
  gap** (VIX dropped — see below). GEX deliberately excluded (FlashAlpha verdict: GEX adds nothing after
  VIX/IV control).
- **Two real-world LEAN gotchas hit and fixed (agent lessons):**
  - **VIX data crash:** QC's CBOE VIX feed throws a runtime "Stale file handle" that a user `try/except`
    can't catch (engine-level data reader). → **dropped the VIX subscription**; ATM IV (from the 0DTE chain)
    is the implied-vol proxy. Lesson: *don't gate a run on a fragile alt-data feed; degrade gracefully.*
  - **Log cap:** free tier = **10kb logs/backtest, 10kb/day** → a 700-row dump truncates at ~178 rows. →
    **re-architected:** run the full gate sweep + null + bias check **in-algo**, log only a compact
    `=== C1 SUMMARY ===`, and save full per-day rows to the **ObjectStore** (`c1_rows.csv`). Lesson:
    *on the free tier, compute summaries in-algo; never rely on logs for bulk data.*
- **Partial-window preview** (178 days, 2022-bear): pipeline validated on real data, but **no gate separated**
  (null p 0.78–0.97) — *expected*: a uniformly high-vol slice has no calm cohort. The classifier needs the
  **full window's regime variation.** Full-window re-run pending (the SUMMARY-version paste).

### Phase 3 — explore the automation toolchain (06-24)
- Deep dive on **QC API + LEAN CLI** (`qc-api-lean-cli.md`), VPS vs Mac, true cost, the "24/7 agent" idea,
  and a **best-tool-by-use-case** decision (`backtest-tooling-roi.md` UPDATE). Summarized in §8–§10 below.

---

## 2. End goal and the process to get there

### End goal
A **profitable, systematic, bot-run options fleet** whose edge is a **chain**, not a single strategy:

> **regime classifier → regime-matched structure → matched hedge**, validated **LEAN → OA → paper → live**,
> judged by **R (return on risk), not raw P&L or win rate.**

Concretely: each morning a classifier calls the day (IC-chop / directional-trend / gap); the matched
structure trades it (0DTE IC / directional debit spread / 2DTE gap-up vega); each carries a *validated*
hedge; survivors run live, sized by half-Kelly with hard guardrails. **Near-term milestone: a paper
directional bot live for tracking ASAP.**

### The process (how we get there)
1. **Pre-register hypotheses** (3–5, motivated) — never dredge. One factor at a time.
2. **Backtest** on the right engine (LEAN for sweeps/hedges, OA for structural/validation).
3. **Judge on R / Exp(R) + worst-loss**, beat **control AND a random-day null**, then an **OOS holdout**.
4. **Re-validate LEAN survivors in OA** (absolute economics; OA = live engine).
5. **Paper in OA** (proves fills — mandatory, especially for hedges).
6. **Graduate to live** on data, sized by F-001 (half-Kelly + 25% reserve), F-004 (no martingale).
7. **Kill on data** (e.g., ORB 60m). Trust the framework over the equity curve.

---

## 3. Project to-do list — with the software for each

> Priority tags from `research-roadmap.md`: **P0 critical · P1 high · P2 medium · P3 later.** "Software"
> = the engine that owns the task. **Bold = the active near-term path.**

| # | To-do | Priority | Software / tool | Status |
|---|---|---|---|---|
| 1 | **Re-run C1 full-window, read `=== C1 SUMMARY ===`** | **P0** | **LEAN (QC cloud)** | in progress |
| 2 | C1 gate analysis (sweep + null + bias) | **P0** | LEAN in-algo + `c1_analyze.py` (sandbox) | pending run |
| 3 | Set OA commission $0.60 | P0 | **OA** (Andy) | pending |
| 4 | **C2 put-side fade test** (up-moves fade → downside lean) | P1 | **OA backtester** | next |
| 5 | **C3 OR-break trigger** (15 vs 30 min), gated by C1 | P1 | **OA backtester** | queued |
| 6 | **C4 DebitBuy vs HiVolIC** structure sweeps | P1 | **OA backtester** | queued |
| 7 | **Paper a directional experiment** (the ASAP goal) | P1 | **OA paper** | after C2–C4 |
| 8 | A1 SL% ladder (50…unstopped) on champion IC | P0 (hedge) | LEAN/code | hedge stage |
| 9 | A2 S2 strike-touch validation (the −$45K question) | P0 (hedge) | **LEAN/code ONLY** | hedge stage |
| 10 | A3 SL% × Range075 grid (~840 runs) | P0 (hedge) | LEAN/code (CLI sweep) | hedge stage |
| 11 | A4 Defang vs S2 vs Tighten tournament | P1 | LEAN/code → OA paper | hedge stage |
| 12 | A5 breach-response engine (reclaim/sustain/flip) | P1 | LEAN/code (CLI) | hedge stage |
| 13 | A6 intraday stop-tightening schedule | P1 | LEAN/code | hedge stage |
| 14 | B1 2DTE gap-up vega-crush | P1 | OA + LEAN | after directional |
| 15 | B2 retire centered gamma-IC lanes (confirm + document) | P2 | LEAN → OA | after directional |
| 16 | B3 gap-down → route to directional | P1 | feeds C1 | with C1 |
| 17 | D1/D2 OA-Mirror hedging + stop A/B | P2 | OA paper (+ LEAN hedge lib) | after A |
| 18 | E Lab credit-spread income; pivot/VWAP as C1 inputs | P3 | OA | later |
| 19 | Build the CLI **runner** (autonomous loop) | — | **LEAN CLI + script on Mac/VPS** | at hedge stage |
| 20 | (optional) Local LEAN + Polygon for free compute / trade-level fills | — | LEAN CLI local + Polygon | hedge-fidelity stage |

**Software ownership at a glance:** structural strategy + bots + paper + live = **OA**. Hedges + giant
sweeps + classifier rigor + automation = **LEAN/code** (cloud now, +Polygon later if needed). Live
brokerage = Tradier. Durable record = Notion. Working context = this repo.

---

## 4. Timeline (the ~2-month accelerated window)

From `research-roadmap.md`, adjusted for the 06-24 re-prioritization (directional pulled forward):

| Phase | Focus | Items | Engine |
|---|---|---|---|
| **Now / Wk 1** | Lock harness + C1 | finish calibration ✓ · OA fee $0.60 · **C1 run + gate** | LEAN + OA |
| **Wk 1–2** | Directional core | **C2 put-side · C3 OR-break · C4 structures** | **OA** |
| **Wk 2** | **Paper directional bot live (milestone)** | graduate a directional experiment to OA paper | **OA paper** |
| **Wk 2–3** | Hedge tournament begins → **upgrade trigger** | A1 SL ladder · A2 S2 · A3 SL×Range075 | **LEAN/code (CLI)** |
| **Wk 3–4** | Hedge core + gap | A4 tournament · A5 breach · B1 gap-up vega | LEAN + OA |
| **Wk 5–6** | Mirror + sizing | D1/D2 · C5 sizing (F-001/F-004) | OA + LEAN |
| **Wk 7–8** | Lock | OOS holdout on survivors → stage to OA paper/live | OA |

**What we're trying to achieve, restated:** compress what would be ~12–18 months of validation into ~2
months by adding code throughput + the hedge backtests OA can't run — **without** letting cheap compute
manufacture overfit (the 95.3%→57% scar). The live deployment is still paced by paper; the accelerant is
research/validation, not risk-taking.

---

## 5. The tool landscape — three approaches compared

The strategic choice isn't "OA or LEAN" — it's **which tool for which job.** Three operating modes:

### A) Option Alpha (OA) — the default + the gate
- **Strengths:** OA's backtester **is its live engine → it predicts live**; fast per-run; zero setup; one
  platform from backtest → paper → live; clicking is friction that enforces discipline; $0 incremental.
- **Limits:** **cannot** backtest touch/breach/cross-leg hedges (defers to paper); big combinatorial sweeps
  are infeasible by hand; manual copy-paste loop; no automation/reproducibility; 3yr window cap (moot — SPX
  0DTE only since 2022).
- **Use for:** new strategy structural sweeps, bot build, paper, go-live, regime-gate entry filters.

### B) LEAN cloud (QuantConnect) — the code engine
- **Strengths:** can model the **full stateful hedge logic** OA can't; **parallel** sweeps (2 nodes
  Researcher / up to 12 in cloud optimize); CLI **automation**; reproducible, version-controlled; ObjectStore
  for full-data export.
- **Limits:** **fills ~4× hot** → must re-validate in OA; **paid tier** (~$84/mo Researcher); per-backtest
  inherently ~10–15 min (minute-only option data, largely serial — bigger nodes give only modest gains);
  **QCC (real money)** meters heavy cloud optimize; free tier has the 10kb log cap + single throttled node.
- **Use for:** hedge tournament, giant sweeps, classifier research (C1), null/OOS rigor, win-rate/relative
  ranking.

### C) LEAN local + Polygon — the unlimited-compute / high-fidelity option
- **Strengths:** **unlimited free compute** on your own machine (no QCC, no node rental); **Polygon Developer
  (~$79/mo)** adds **trade/quote-level fills** = the fidelity to make the S2/hedge tournament *decision-grade*;
  Polygon Starter (~$29/mo) = minute aggregates; runs on the VPS 24/7.
- **Limits:** **Docker + data-format setup** (~½ day); your hardware is the speed ceiling; LEAN CLI still
  requires **paid QC org membership**; you manage the data pipeline.
- **Use for:** the 24/7 autonomous runner, the heavy hedge grids where cloud QCC would bleed, and the
  trade-level hedge-fill read.

**Decision rule (the standing answer):** *OA is the default and the gate. Reach for LEAN/code only for
(a) hedges OA can't express, (b) sweeps too big to click, (c) null/OOS/classifier rigor. Always
re-validate LEAN survivors in OA before paper.* Full use-case matrix in `backtest-tooling-roi.md`.

---

## 6. LEAN code patterns every agent must know (don't relearn the hard way)

From `lean-backtesting-reference.md` — these are *verified by code that ran and was cross-checked vs OA*:

- **SPX options:** `add_index("SPX")` → `add_index_option(spx, "SPXW")` (weeklies/dailies, **not** SPX
  monthlies). `set_filter(lambda u: u.include_weeklys().expiration(0,0).strikes(-35,35))`. **Narrow strikes
  = the #1 speed lever.**
- **0DTE = `expiration(0,0)`.** SPX daily 0DTE only exists from **~May 2022** — earlier dates find nothing.
- **Built-in "Win Rate" is LEG-level (~49% for any IC)** — 2 legs win, 2 lose. **Always compute per-condor
  win rate yourself** (track portfolio value across traded days). The `profitLoss` export is also per-leg.
- **Index options are European, cash-settled** — hold-to-expiry = do nothing; they auto-settle at 4pm
  (matches OA hold-to-settlement). No assignment modeling.
- **Fees must be set per *contract*** via `set_security_initializer`, not on the canonical option (else
  Total Fees = $0). Verify `portfolio.total_fees > 0`. Our model = `TradierSpxFeeModel($0.60/contract)`.
- **Model hedges at 1-minute reaction granularity** (OA Monitors poll ~1 min; finer flatters the hedge).
- **Always calibrate to a known OA number before trusting a new sweep.** (Calibration is now LOCKED.)
- **Free tier:** B-MICRO single node, ~12 min full-window minute run, **200 backtests/day**, **10kb
  logs/backtest + 10kb/day** → compute summaries in-algo, dump full data to ObjectStore.

---

## 7. Two findings that color every LEAN result (carry these always)

1. **LEAN RoR runs ~4× hot vs OA** (calibration: +1.31% vs +0.3% RoR/IC). LEAN fills mid/market; OA models
   SmartPricing + 0.03/leg slippage. **→ LEAN for win rate + relative ranking; OA/paper for absolute
   economics.** TODO to tighten: add a ~0.03/leg slippage model to LEAN.
2. **The quote filter skips ~24% of days** (707 vs OA ~920) — days with no clean bid/ask at the entry
   minute. **Must verify it isn't biased toward calm days** before trusting gap/directional reads, or every
   sweep silently drops the volatile sessions those strategies live on. C1 now skip-logs days and the
   analyzer runs a traded-vs-skipped distribution check exactly for this.

---

## 8. The autonomous toolchain — CLI + runner + nodes, deep

### How the pieces fit
```
  repo (lean/*.py algos, run_queue)
        │  lean cloud push
        ▼
  Mac/VPS runner script  ──►  QC cloud nodes  (lean cloud backtest / optimize, 2–12 parallel)
        │  lean cloud pull (results JSON) + ObjectStore (full per-day CSV)
        ▼
  bot-fleet/lean/results/  ◄── Claude reads from the mounted folder, analyzes, picks next configs
```

- **`lean` CLI** (`pip install lean`): `lean login` (user ID + API token) → `lean init` → `lean cloud
  push` syncs repo algos to QC projects → `lean cloud backtest "Proj"` runs them → `lean cloud optimize`
  sweeps (grid, **up to 3 params**, 1–12 nodes, `--estimate` shows QCC cost first). Local mode: `lean
  backtest` in Docker with your own data.
- **The runner** (`scripts/lean_run.sh`, to be written): reads a **run queue** (configs), pushes, loops
  backtests/optimizes, writes each result JSON into `lean/results/` with an index ledger
  (run → algo → config → metrics). One command launches a whole batch.
- **Nodes:** **B4-12 (4CPU/12GB, $24/mo) is the sweet spot** for our minute-options work. A single LEAN
  backtest is largely **serial**, so big/GPU/24-core nodes give little single-run gain and are *useless to
  us* — **the real lever is parallelism** (run many at once) and **automation** (no human in the loop).

### Where it runs (a hard constraint agents must know)
- **Claude's sandbox cannot host the CLI** — it can't reliably reach the QC API (`api.quantconnect.com`
  doesn't resolve), it's ephemeral, and the API token shouldn't live there. **The runner runs on Andy's
  Mac or the VPS** (`149.28.47.235`, always-on, better for scheduled overnight sweeps; but it's Claude
  Code's lane). Claude reads results from the **mounted repo folder** — that's the loop closure.
- **Trigger:** Andy runs one command, **or** a cron/launchd job fires it (mirroring the existing 6pm
  backup agent). After the trigger, everything is automatic; Claude reads results next session.

### What "perfecting this process" does for the bots + hedging
This is the payoff, stated plainly:

1. **It makes the hedge tournament possible at all.** S2 validation, SL%×Range075, Defang/Tighten, the
   breach engine — the questions behind the **−$45K hedge divergence** and the **production-unvalidated S2**.
   OA can't express them; a code backtester with intraday data runs them on 4 years in one job. *This is the
   single biggest unlock — the hedge is what makes directional and IC days survivable.*
2. **It runs the disciplined pipeline unattended.** A pre-registered hypothesis queue executes overnight —
   each item judged against control + random-day null + OOS holdout — and Claude reads the results in the
   morning. Throughput on *robustness checks* (the things that catch overfit), not just raw runs.
3. **It compresses the validation timeline ~12–18 months → ~2.** Sweeps that are weeks of clicking become
   one parallel job; the bottleneck shifts from your hands to compute.
4. **It gives the bots a *validated* hedge library + a hedge→bot matrix** — which hedge for which bot —
   instead of hedges proven only slowly in paper. That directly improves live survivability and sizing.

### The limits (and the trap) of full autonomy
- **Overfitting is the dominant risk.** An agent that runs backtests 24/7 to "find the perfect combination"
  is the exact machine that produced the **95.3% backtest → 57% live** scar. Search N configs and the best
  is inflated by ~√N of noise. **Build the disciplined version, never the dredge:** pre-registered queue,
  one factor at a time, control + null + OOS, read main effects not the best cell.
- **The surface is already inflated** (LEAN fills 4× hot) — harder search just finds configs that exploit
  the optimism. **OA/paper stays the mandatory gate.**
- **QCC bleed** — continuous cloud backtests cost real money; cap with `--estimate` or go local+Polygon.
- **Throughput ceiling** — even on 12 nodes, ~12 min/run = hundreds/day, not millions; the real parameter
  space is un-exhaustible, so hypotheses still have to come first.
- **Fidelity ceiling** — minute fills aren't trade-level; the decision-grade hedge read wants Polygon
  Developer ($79). No amount of searching closes the backtest→live gap.

**The defensible autonomous system = "automate the pipeline, never the dredge":** an overnight runner of a
pre-registered hypothesis queue, QCC-budgeted, every survivor cleared against control + null + OOS, with
OA/paper as the final gate before any capital.

---

## 9. Cost summary (verified 2026-06-24)

- **Free tier:** $0. Covers the rest of C1, the directional core, and small hedge experiments. Limits: one
  throttled B-MICRO node, 200 backtests/day, 10kb log cap.
- **QC Researcher:** **~$84/mo** recommended (seat + CLI/API + a node), caps at **2 backtest nodes**. Node
  menu: B2-8 $14 / **B4-12 $24** / B8-16 $96 / GPU $400 / B24-128 $768. **Skip:** Object Store ($60/10GB —
  we use MB), datasets (bundled), live/GPU/research/assistant nodes.
- **QC Team:** $144/user/mo, **2-user min ($288)**, up to 10 nodes — overkill for solo.
- **Polygon:** Starter ~$29/mo (minute) / Developer ~$79/mo (trade-level) — for local compute / hedge-fill
  fidelity.
- **Realistic spend:** **$0 now**; **~$84–110/mo** when the hedge tournament starts (Researcher + B4-12,
  add a 2nd node for parallel sweeps); **+$29–79 Polygon** only if going local / wanting trade-level fills.

---

## 10. Decisions on record (so agents don't relitigate them)

- **Engine = LEAN → OA → paper.** OO dropped. (06-23)
- **Calibration LOCKED** — trust LEAN for WR + relative ranking; OA for absolute. (06-24)
- **C1 = pure day-type labeler** (no hedge), features = ATM IV / ATR5 / gap; **GEX excluded.** (06-24)
- **Directional structures + paper bot → OA, now. C1 research → LEAN. Code path (CLI/Polygon/runner) →
  built at the hedge tournament, not before.** (06-24)
- **Don't build a brute-force "perfect combination" agent** — build the pre-registered disciplined runner.
  (06-24)
- **Best-tool-by-use-case matrix** is the standing reference — now in §12a below. (06-24)

---

## 11. Pointers (where the depth lives)

- `lean-backtesting-reference.md` — verified LEAN code patterns + calibration protocol + gotchas. **Read
  before writing any LEAN algorithm.**
- **§12 below** — consolidated tooling-ROI + acceleration + CLI/automation digest (merged 2026-07-03;
  originals `backtest-tooling-roi.md` / `backtest-acceleration-before-after.md` / `qc-api-lean-cli.md` are
  archived in `docs/_archive/`).
- `research-roadmap.md` — the P0–P3 workstream schedule (A hedging, C directional, B gap, D mirror, E lab).
- `directional-oa-build-sheet.md` — the authoritative Directional batch queue + results (supersedes the
  archived `directional-research.md`).
- `methodology.md` — evidence standards, factor-bucket lens, kill discipline, the overfitting rules.
- `lean/c1_regime.py` + `lean/c1_analyze.py` — the C1 classifier + analyzer (the live example to learn from).

---

## 12. Consolidated tooling memos (merged 2026-07-03)

> Merged from `backtest-tooling-roi.md`, `backtest-acceleration-before-after.md`, and `qc-api-lean-cli.md`
> (all now in `docs/_archive/`). Decision-grade digest; the archived originals hold the full tables.

### 12a. Tooling ROI + best-tool-by-use-case (from `backtest-tooling-roi.md`)
- **The one asymmetry:** only LEAN/code can backtest **touch/breach/cross-leg hedges** (S2, Defang, Tighten,
  breach engine) — OA can't express that logic at all; it defers it to paper. That's the ~−$45K open
  question and the sole reason to spend.
- **Everything structural, OA does natively — and OA's backtest predicts live** (it *is* the live engine).
  LEAN fills run ~4× hot, so LEAN ranks; **always re-validate LEAN survivors in OA before paper.**
- **Backlog scale:** ~45 specs ≈ 120–160 disciplined runs (500–1,200+ full grid); SL%×Range075 and the
  sustain-timer walk-forward are ~840 runs each — infeasible by hand, trivial in code.
- **Rule of thumb:** OA = default + gate; reach for LEAN/code only for (a) hedges OA can't express, (b)
  sweeps too big to click, (c) null/OOS/classifier rigor (C1 stays in LEAN). **Speed cuts both ways** — the
  95.3%→57% champion scar came from best-cell dredging; hold pre-registered, one-factor, beat-control-and-null
  discipline.

### 12b. Acceleration — what speed does and doesn't fix (from `backtest-acceleration-before-after.md`)
- **Fixes:** manual GUI hours (→ code), structural throughput (weeks→days), and **makes hedge backtesting
  possible** (the unlock). Knowledge-timeline compression ≈ **12–18 months** for ~$120 (2 mo QC Researcher) +
  a few days of build.
- **Does NOT fix:** overfitting (gets *worse*), the backtest→live gap (30–40% haircut, the 95→57 scar), the
  paper-validation calendar, or the live-capital discipline gates. **Paper stays the gate**, especially for
  hedges. The win is *better pre-vetted candidates arriving at paper*, not faster live deployment.

### 12c. CLI / automation — the hands-off endpoint (from `qc-api-lean-cli.md`)
- **LEAN CLI** (`pip install lean`) drives the same engine in **cloud mode** (QC nodes, recommended) or
  **local mode** (Docker + bring-your-own Polygon data). **Hard gate: the CLI/API need a paid QC org**
  (Quant Researcher ≈ **$84/mo** — seat + CLI + a B4-12 node; the older ~$60 figure is stale). Free tier =
  paste-loop only.
- **Sandbox can't host it** (`api.quantconnect.com` unreachable + ephemeral). Runner lives on **Andy's Mac
  or the VPS** (`149.28.47.235`, always-on, better for scheduled sweeps — but Claude Code's lane).
  Architecture: repo algos → runner (`lean cloud push` → loop the queue → save result JSON to
  `lean/results/`) → Claude reads from the mount; launchd/cron (clone the 6pm backup agent) makes recurring
  sweeps hands-off.
- **Cost caveats:** `lean cloud optimize` parallel nodes burn **QCC (real money)** beyond the included node
  (`--estimate` first); >3-param sweeps exceed the cloud optimizer's grid limit (scripted queue loop or
  local mode). Per-run LEAN won't beat OA (architectural) — levers are **parallelism** (2–12 nodes) +
  **automation**, not single-run speed.
- **Timing:** the directional paper bot ships on the free tier; make the Researcher jump **when the hedge
  tournament (Workstream A3/A5) starts** — CLI automation comes free with that tier.
- **Guardrail:** don't build a 24/7 "perfect combination" dredger (the 95→57 machine). DO build an overnight
  runner over a **pre-registered hypothesis queue** — one factor at a time, each survivor vs control +
  random-day null + OOS holdout, QCC budget cap, OA/paper as the gate.
