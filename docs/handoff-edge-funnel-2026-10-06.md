# Handoff — the Edge Funnel (new Cowork chat, written 2026-10-06)

You are taking over one arm of `bot-fleet-v2`: **the search for an edge.** Read this whole file
before acting. Then read `CLAUDE.md`, `docs/state.md` (top block) and `STATUS.md`. Answer from
files, never from memory of prior chats.

## 1. Why this arm exists (the honest picture, 2026-10-06)
- **Live paper ledger:** +$5,063 over 41 trading days on $1.49M cumulative risk, ≈0.34% (`STATUS.md`).
  Two breach days (09-18, 09-30) cost about $18k.
- **The backtester now answers in minutes what live trading answers in years.** On 2026-10-06 the S2
  shape (SPX .10Δ IC, $5 wings, 13:30, 5y, 825 days) showed:
  - **ride has ~zero edge** (+$848 gross, PF 1.02)
  - **Touch-buffer exits cut bad days 95 → 11 ($10) or → 0 ($20)**
  - the **11:00 (PR-01) shape is unfixable by any exit**
  - Evidence: `data/captures/2026-10-06-t1-s2-tail/README.md`.
- **Andy's question is "is there an edge at all?"** Tail fixes only pay once there is one.
  This arm's job is to find one honestly, or establish that there isn't one.

## 2. The design you are growing — the Edge Funnel
```
1 SEARCH     Claude Code ⇄ Devin      backtest arms on 2021-10 → 2024-12 only
2 HOLDOUT    Devin, sealed run        nominated candidates on 2025-01 → present
3 LIVE PAPER Cowork builds bots       survivor + paired control, in open slots
4 PROMOTE    Andy rules               keep / size / kill; failures go back to 1
```
**Roles:**
- **Claude Code** is the research lead: plans batches, scores, writes digests, launches Devin via
  `~/bin/devin-free` (its Devin connector key needs re-provisioning first).
- **Devin** runs backtests and **read-only** OA reads. It never edits bots and never uses Create Bot
  (`R-2026-09-16-DEVIN-OA-CHROME-CAPTURE`).
- **Cowork (you)** reviews digests, drafts rulings, and **builds and edits live test bots** in the
  built-in browser, with the two-layer verification (`CLAUDE.md` §5, `oa-driving` skill).
- **Andy** approves the search scope, approves which survivors go live, and decides promotions.

**Live room:** 43 bots, about 25 off, 7 open plan slots (10-06 `/bots` capture). New test bots go into
**fresh** slots (archive dead bots to free more). Never repurpose an old bot, and never clone to reset
history (`CLAUDE.md` §5).

## 3. Rules already signed — they bind you
- `R-2026-10-06-TAIL-SCORING-RULE` — bad day ≤ −0.5R per condor-day. Pass = paired fixed > created
  (exact sign test p<0.05) and mean R ≥ 80% of control.
- `R-2026-10-06-TAIL-FEES-IGNORED` — tail scoring is gross. ⚠ **This was ruled for bad-day work.
  An EDGE search needs its own fee ruling.** Ask Andy before scoring edge gross. OA's estimate is
  $3.16 per 1-lot IC transaction (open or close).
- `R-2026-10-06-TAIL-HOLDOUT` — choose on 2021-10→2024-12, confirm on 2025-01→present.
- `R-2026-10-06-TAIL-LIVE-CLONE` — one paired live clone, for 20 trading days or the first 3 days the
  fix fires (whichever is later), before anything spreads.
- `R-2026-10-06-TAIL-PROFILE-PREREG` — no bot is signed without a backtested tail profile.
- Every OA bot change, sizing, kill criterion and pre-registration text is **gated** ("amend the plan").

**Known backtester limits:**
- single structure only (no paired spreads + Cleanup)
- **exits stop ~15:45**
- touch check coarser than the live monitor
- optimistic mid fills
- no trailing stop
- 1-min Tradier bars are only kept ~20 trading days

## 4. YOUR FIRST JOB — mine what's already been learned, before any new test
Build **`data/backtest_findings.csv`**, one row per prior finding: source path · date · what was tested
· result (with unit) · tier/caveat · still valid? · implication for the search. Then write
**`docs/edge-funnel-prior-art.md`** (≤2 pages, no figures without their CSV/source cited).

**Where to look (v2 repo, connected as `bot-fleet-v2`):**
- `data/captures/2026-10-06-t1-s2-tail/` · `2026-10-06-loss-packet-20260826-s2-130pm/` ·
  `2026-09-17-gf-exit-spread/` · `2026-09-17-p1-stage1/` · `2026-09-17-oa-combo-semantics/` ·
  `2026-09-16-oa-backtester/` · `2026-09-16-oa-compare/`
- `docs/phase1-stage1-verification-2026-09-17.md` · `docs/gf-exit-spread-verification-2026-09-17.md` ·
  `docs/oo-trial-backtests.md` · `docs/ic-trailing-stop-backtest.md` · `docs/backtest-ingest-protocol.md`
  · `docs/lean-backtesting-reference.md` · `docs/quantconnect-lean-exploration-brief.md` ·
  `docs/strategy-taxonomy.md` · `docs/hedge-research.md` · `docs/hedge-north-star.md` ·
  `docs/hedge-design-spec-2026-09-16.md` · `docs/experiments/` · `docs/RULINGS.md` (backtest rulings)
- **The v1 archive `~/bot-fleet` (READ-ONLY, never modify).** Go through `docs/history-index.md` first;
  it maps every removed v1 doc to its archive path. It is **not** connected to this session by default:
  request folder access to `~/bot-fleet` for read-only use. Cite v1 as history, never as the fleet's
  state (`CLAUDE.md` §3, §8).
- **OA's own backtest list** (`/backtests`, read-only in the built-in browser) holds older tests not in the
  repo. ⭐ Example worth checking: an **SPX long call spread, 11:00, 5Y, listed at +$42.1K P/L / −$3.2K max
  DD** (row shown 2026-10-06). **That number is unverified.** Open it, record the config and stats, and treat
  it as a lead to test under the holdout, never as a finding. Also listed: SPX long calls at
  .05/.30/.82Δ, and `PUT-OOS-control` vs `PUT-OOS-gated`. Record each one's settings card.

**Watch for:** prior results stated without units, without a holdout, or computed before the
2026-07-31 denominator fix (`CLAUDE.md` §4), and figures in narrative docs with no source CSV
(CSV wins). Mark each one.

## 5. Then — draft (do not run) the search scope for Andy to sign
One page:
- which structures, underlyings, entry times and exits are in
- the arm budget per week
- the fee ruling question
- the ledger format (every arm logged, dead ends included)
- the sealed-holdout mechanics
- the stop rule (no holdout survivor by an agreed date → shrink the fleet, stop hunting)

Seed it with what §4 found. **No search runs until Andy signs it.**

## 5b. QUEUED STUDY — the "touch decision" hedge (Andy, 2026-10-06)
**Idea:** instead of a fixed exit, at a $10 strike-touch the bot **reads conditions and picks a plan**:
hold, close, or open a protective debit spread on the tested side. The loss register shows why a fixed
exit can't work: 08-26 and 08-27 **reverted** (closing was the mistake), while 09-30 and 09-18
**continued** (holding was the mistake). T2 also showed every fixed touch exit at .10Δ flips many
winners (`data/captures/2026-10-06-t2-strike-distance/03-cowork-tail-winside-score.md`).

**What OA can build** (`docs/hedge-north-star.md` §"What OA can do natively"; `oa-platform-reference.md` §11):
- A Monitor can OPEN a position.
- It can branch on time of day, VIX level, underlying % move since open, position return %, and strike touch.
- It can NOT use time persistence, look-back conditions, intraday indicators, or mid-trade regime detection.
- The plan may only use what OA can see at that minute.

**Why it's untested:** the OA backtester can't model branching or trigger-opened hedges; live samples are tiny.

**Study path (go/no-go at each step):**
1. **Touch study, underlying data only.** On multi-year SPX intraday bars (needs a purchased dataset;
   Tradier keeps ~20 days of 1-min), find every moment price came within $10 of a .05–.10Δ-equivalent
   strike after 13:30. Label it **reverted vs continued** by the close. Test whether the OA-visible signals at
   that minute (time, VIX level and change, % move since open, approach speed) predict the label
   **out of sample** (choose ≤2024, holdout ≥2025). **No predictive signal = stop here.** Cheap, and that answer
   is valuable too.
2. If it predicts: design a 2–3-branch plan and price the hedge legs. This needs **historical option chain
   data** plus a Claude Code simulator (the 09-09 "buy chain data" idea). Score it with `scripts/tail_score.py`
   (bad days + win-side, both windows).
3. Survivor gets **one paired live clone** (`R-2026-10-06-TAIL-LIVE-CLONE`), built by Cowork, gated.

**First action:** price the data. Find a multi-year SPX/VIX 1-min dataset (and later an SPX 0DTE chain
dataset), with cost and licence terms, and present them to Andy for a buy decision. No purchase without him.

## 6. What's in flight (don't collide)
**Scope boundary:** this chat owns the **edge search only**. The **loss-day program** (loss packets,
`data/loss_register.csv`, the T2 strike-distance sweep, tail fixes on existing bots) stays with the
original Cowork chat. Don't run, edit or re-order those items. Read their results as inputs.
- `docs/devin-queue.md`: the top of the file is the pointer list (08-27 loss packet, then the T2
  strike-distance sweep, then the remaining packets). Below it is the restored prior backlog. **Append
  only.**
- T2 strike-distance dispatch: `docs/dispatch-strike-distance-2026-10-06.md` (gross + holdout).
- **One OA-driving session at a time.** If Devin is running, do not drive OA. Ask Andy first.
- Devin is free until **2026-10-16**. Front-load backtest work.

## 7. Working rules
- Andy is direct: answer-first, concise.
- Close-out per `CLAUDE.md` §9.1: session-log append, and say "ready to commit" with paste-ready
  commands. **Andy commits.** No git from the bridge, ever.
- Verify every file write with `device_bash` sha256 plus a grep. Hand him commands; never ask him to
  rename files.
- Be blunt about edge. The 2026-10-06 assessment ("method strong, strategies thin, odds well under even
  until a net-of-fee holdout survivor exists") stands until evidence changes it.
