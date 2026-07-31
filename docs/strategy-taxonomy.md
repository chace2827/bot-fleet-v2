# Strategy Taxonomy — Bot Fleet

> Created 2026-06-08, finalized same day in a consulting pass with Andy. This is the
> **organizing model** for the whole fleet — read it whenever "what is this bot *for*?"
> is unclear. It sits on top of `bot-configs.md` (per-bot configs) and `STATUS.md` (live
> numbers); it tells you which drawer every bot lives in and why.

## The core idea: every bot is **Pillar · Role**

Confusion comes from sorting bots into one flat list. They don't fit, because each bot
has two *independent* properties:

1. **Pillar** — the strategy program it belongs to (what it harvests / where it lives).
2. **Role** — why it exists *right now* (its lifecycle job).

A bot is always "**Pillar · Role**", e.g. "Iron Condor · Live-candidate". A secondary
attribute is the **underlying** (SPX / QQQ / SPY) — NOT a pillar; the QQQ bots are mostly
pre-migration legacy that fed the SPX champion.

---

## The four Pillars

The fleet is two mature own-built pillars + two incubators:

| # | Pillar | What it is | Fires / scope | Live status |
|---|---|---|---|---|
| 1 | **Iron Condor** | 0DTE premium / short realized-vol | **chop days (most days)** | Mature — champion in validation |
| 2 | **Directional** | 0DTE high-vol play | **high-vol days** (when IC stands down) | To build (2 experiments) |
| 3 | **OA-Mirror** | subscribed *external* bots | always — its own live diversification book | Paper; fund the winners |
| 4 | **Lab / R&D** | *our own* new ideas not yet a pillar | exploratory | Empty — to populate |

**The daily logic:** something fires every day. A **morning go/no-go router** classifies the
session and routes it: **chop → Iron Condor**, **high-vol → Directional**. The two are
anti-correlated by design — that pairing is the spine of the book.

**The two incubators are symmetric:** Mirror incubates *other people's* bots; Lab incubates
*our own* untested ideas. When something in either proves out, it graduates (a role change) —
into an existing pillar, or by becoming its own.

### Pillar 1 — Iron Condor (0DTE, chop days)
Own-built, the mature core. Champion = the current `Scalp-SPX-PT25-S2` (being **renamed**
`IC-SPX-FastPT25-S2` — it's an IC, not a scalp). All IC variants, controls, and exit-mechanic
experiments live here.

### Pillar 2 — Directional (0DTE, high-vol days)
Own-built, to design. **Two experiments run head-to-head** for the high-vol slot, decided by
live data:
- **(a) Aggressive debit-buy** — long options / debit spreads to ride fast moves, *tight* stops
  + profit targets. (This absorbs the earlier "momentum-scalp" idea; it is not a separate pillar.)
- **(b) High-vol IC variant** — stay in condors but a high-vol config (wider / later / different
  hedge) on those days.

### Pillar 3 — OA-Mirror (subscribed externals)
A live diversification pillar in its own right — subscribe to external bots that work, prove
them on paper, **fund the winners**. Bots stay here (they do NOT graduate out). Mostly
multi-day / non-0DTE structures, which is exactly the diversification value.

**Graduation bar (paper → funded):** ≥20 trades **and** positive P/L **and** win-rate within
~10% of the source's claim **and** max drawdown under the risk cap.

### Pillar 4 — Lab / R&D (our own experimental ideas)
Sandbox for own-built ideas that don't fit an existing pillar yet: longer-dated options,
multi-day scalping on chop days, novel structures. Graduates into a pillar (or becomes one)
when it proves out. **Distinct from the "Experiment" role:** the role is a *variant of a
defined pillar strategy* (e.g. a stop tweak on the IC); Lab is a *strategy with no pillar yet*.

---

## The Roles (lifecycle job, within any pillar)

| Role | Definition | Graduates to |
|---|---|---|
| **Live-candidate** | The bot per pillar you intend to fund / are funding. | (live) |
| **Experiment** | A paper variant of that pillar's strategy: a filter, stop, PT, width, entry-time tweak. | Live-candidate if it wins |
| **Control** | An unfiltered / no-logic baseline whose only job is to prove the edge is real. | (never — measurement tool) |
| **Mirror-watch** | An external bot we're tracking pre-funding. **Pillar 3 only.** | Funded (stays in Mirror) |
| **Standalone-hedge** | A genuine *separate protective position* (tail put, long-vol overlay). **Rare.** | (stays as overlay) |

Graduation is a **role change, not a new bot**.

---

## Naming & grouping convention (OA)
The two taxonomy axes map onto OA's two grouping mechanisms, so the platform UI mirrors the model:

- **OA Bot Group = Pillar** — the four groups are `IC`, `Directional`, `OA-Mirror`, `Lab`.
- **OA Tag = Role** — `live-candidate`, `experiment`, `control`, `mirror-watch`. Because role is
  a *tag*, **graduation is a retag, not a rename** — names stay stable for a bot's whole life.
- **Bot name = `Pillar-Underlying-Config-Hedge`**:
  - *Pillar*: `IC` / `DIR` / `MIR` / `LAB`.
  - *Underlying*: `SPX` / `QQQ` / `SPY`.
  - *Config*: the offensive setup — entry/structure/PT, e.g. `FastPT25`, `Fortress`, `DebitBuy`.
  - *Hedge*: the defensive mechanic code — `S2` / `S3` / `SL100` / `SL130` / `Defang` / `Tighten`,
    or **`Unstopped`** for a deliberate no-hedge control.

Examples: `IC-SPX-FastPT25-S2` (champion), `IC-SPX-Fortress-Unstopped` (control),
`IC-SPX-Fortress-Defang` (experiment), `DIR-SPX-DebitBuy`.

**Why the hedge slot matters:** the hedge tournament holds the base fixed and varies only the
suffix — `IC-SPX-FastPT25-S2`, `IC-SPX-FastPT25-SL100`, `IC-SPX-FastPT25-Defang` — so the bracket
reads straight off the roster. Mirror bots keep their source names (they're external) but live in
the `OA-Mirror` group.

## Hedging = a config layer, run as a tournament (not a pillar)

A hedge is a **config** when it's a parameter on an existing position — stop level (S1/S2/S3),
profit target, defang threshold, Sandvand $0.05 short-leg close, strike-touch close. It's a
**standalone bot** only when it's a separate position that trades on its own (tail put, VIX
hedge) — which you don't run today.

**The "which hedge is best" tournament runs backtest-first, then live the finalists:**
1. **Backtest** the bracket on the champion's *clean SPX history* (in the Claude Code / backtest
   lane, not OA) to narrow the field. This deliberately sidesteps the **contaminated QQQ
   hedge-family data** (QQQ pre-migration + call-side strike bug + billing-lapse gap — high
   volume, but not decision-grade).
2. **Live the 1-2 survivors** as parallel copies of the champion for a clean head-to-head.

**Tournament field:** stop-level sweep (S1 / S2 / S3) + Sandvand $0.05 close + defang +
Fortress-Tighten (intraday SL schedule) + the SL% × Range075 interaction sweep (from 5/12
research).

**Consequence:** the QQQ "Hedge family" (HedgeA-S1, B-S2, C-S3, D-Conditional, Test) is **not a
hedge tier** — it's five exit-mechanic experiments on the same IC (and several are suspected
duplicates). Reclassified to "Iron Condor · Experiment"; superseded by the backtest tournament.

---

## Current roster, slotted

Underlying in (parens). P/L from `STATUS.md` 2026-06-08. ON/OFF = current OA toggle.

### Pillar 1 — IRON CONDOR
| Bot | Role | Und. | P/L | On |
|---|---|---|---:|:--:|
| **Scalp-SPX-PT25-S2** → rename `IC-SPX-FastPT25-S2` | **Live-candidate** | SPX | −$4,905 | ON |
| SPX-IC-0DTE-Fortress-Baseline-v1 | Control | SPX | +$450 | ON |
| SPX-IC-0DTE-Fortress-Defang-v1 | Experiment (defang) | SPX | −$450 | ON |
| QQQ-IC-0DTE-Fortress | Experiment (reference) | QQQ | +$2,975 | ON |
| QQQ-IC-0DTE-Fortress-NoPT50 | Experiment (no-PT) | QQQ | +$2,760 | ON |
| QQQ-IC-0DTE-Fortress-NoFilter | Experiment (no-filter) | QQQ | +$908 | OFF |
| QQQ-IC-0DTE-Fortress-S2 | Experiment (S2) | QQQ | −$445 | OFF |
| QQQ-IC-0DTE-HedgeA-S1 | Experiment (S1 stop) | QQQ | −$12,501 | OFF |
| QQQ-IC-0DTE-HedgeB-S2 | Experiment (S2 stop) | QQQ | −$3,130 | OFF |
| QQQ-IC-0DTE-HedgeC-S3 | Experiment (S3 stop) | QQQ | −$2,702 | OFF |
| QQQ-IC-0DTE-HedgeD-Conditional | Experiment (cond. stop) | QQQ | −$15,376 | OFF |
| QQQ-IC-0DTE-HedgeTest | Experiment (stop test) | QQQ | −$11,196 | OFF |
| QQQ-IC-0DTE-Baseline | Control | QQQ | −$31,580 | OFF |
| QQQ-IC-0DTE-Raw-HoldToExp | Control | QQQ | −$303 | OFF |
| QQQ-IC-0DTE-InverseFilter-HoldToExp | Experiment (inverse filter) | QQQ | +$37 | OFF |
| QQQ-IC-0DTE-VIX25-Range075-PT50 | Experiment (VIX filter) | QQQ | +$5 | OFF |
| QQQ-IC-0DTE-Range075-PT50 | Experiment (filter+PT) | QQQ | +$24 | OFF |
| QQQ-IC-0DTE-Range075-PT50-Wide2-155PM | Experiment (width/time) | QQQ | +$67 | OFF |
| QQQ-IC-0DTE-Range075-PT50-Wide2-1230PM | Experiment (width/time) | QQQ | +$78 | OFF |

### Pillar 2 — DIRECTIONAL
**No bots yet.** Build two head-to-head experiments: (a) aggressive 0DTE debit-buy, tight exits;
(b) high-vol IC variant. Both run on high-vol days (per the morning router).

### Pillar 3 — OA-MIRROR (all Mirror-watch until funded)
| Bot | Real structure | Und. | P/L | On | Read vs funding bar |
|---|---|---|---:|:--:|---|
| QQQ long call | Directional (multi-day) | QQQ | +$4,864 | ON | Strong (100% WR) but only 5 trades — short of ≥20. Top fund-watch. |
| Nigiri-Paper-v1 | Iron Condor | — | +$1,260 | ON | +$1,260 / 93%, 27 trades — closest to the bar. |
| 3DTE $140-$350 | IC (3DTE, multi-day) | SPX | +$1,040 | ON | +$1,040 / 100%, 27 trades. |
| Friday 14 DTE Broken Wing IB (B-70) | Directional (skewed) | — | +$775 | ON | 5 trades — too few. |
| Trendy-Paper-v1 | Directional (trend) | — | +$306 | ON | 8 trades. |
| 60min-ORB-10W-Paper-v1 | Directional (ORB) | SPX | −$490 | ON | Negative — fails bar. |
| 1-45pm-Sandwich-Paper-v1 | IC (sandwich) | — | −$473 | OFF | 22% WR — kill candidate. |
| Weekly-IB-SPY-Paper-v1 | Directional (iron fly) | SPY | −$2,011 | ON | Negative — reassess. |
| Opening Range Breakout 60m | Directional (ORB) | — | −$2,602 | OFF | Negative, off — near-kill. |
| Tasty Condor | Iron Condor | — | (no closed) | ON | Newly tracked; no data. |

### Pillar 4 — LAB / R&D
**Empty — to populate.** Candidate ideas: longer-dated options, multi-day scalping on chop days,
novel structures.

---

## Build priority (decided 2026-06-08)
**Parallel:** keep closing the **IC champion go-live gate** while standing up the two
**Directional paper bots** now, so they accrue data in the background. Mirror funding and Lab
follow once those two fronts are moving.

## Open follow-ups (tracked in `backlog.md`)
- **Rename `Scalp-SPX-PT25-S2` → `IC-SPX-FastPT25-S2`** (easy in OA per Andy) — move the ledger
  keys (`EPOCH_BOUNDARY` / `BOTS_ON` / `build_ledger.py`) in the same change so the 214-trade
  history doesn't fork.
- **Build the two Directional experiments** (debit-buy + high-vol IC) on paper.
- **Define the morning go/no-go router** (range + vol + calendar checklist) — draft + tune.
- **Run the hedge tournament** (backtest field above → live the 1-2 finalists). Code-lane task.
- **OA-Mirror funding watch** — track each mirror bot vs the ≥20-trade / +P&L / WR-within-10% /
  DD-under-cap bar; fund the first to clear it.
- **Kill review:** `1-45pm-Sandwich` (22% WR), `Opening Range Breakout 60m` (−$2,602, off).
- **Decouple `SPX-Fortress-Baseline`** from the Scalp-paused gate so it can build a sample.
