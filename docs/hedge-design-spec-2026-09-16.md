# Hedge design spec — the give-back window

**STATUS: DRAFT — UNSIGNED. Nothing here is ratified.**
Written 2026-09-16 at Andy's request ("yes hedge design"). Under `CLAUDE.md` §5, a spec is a
**gated decision**: this document changes nothing until Andy issues an explicit "amend the plan".
It is a proposal plus its evidence, with the open rulings listed in §9.

**Evidence tier: T4.** n=30 losing positions over 27 fill days, single post-cutover epoch, one
regime. Below the T2 / n>=100 / 6-month / regime-change bar that `CLAUDE.md` §4 requires for any
live-capital decision. This spec may authorize *paper arms and measurement work only*.

---

## 1. What this spec is for

To define the trigger, instrument and proof-of-fire for a hedge aimed at **one specific loss
pattern** — the one the post-cutover ledger actually produced. Not a general hedge library.
`hedge-research.md` §1.1 already rules that hedge choice is pattern-dependent; this is the first
pattern this fleet has enough data to name.

Source of numbers: `data/trades.csv` (246 positions, `LEDGER_START` 2026-08-10 through 2026-09-16),
position grain, **risk = larger side** per `CLAUDE.md` §4.

---

## 2. The loss signature

Five findings, all derived from the working ledger this session.

**2.1 Every dollar of loss came from an exit. Zero came from expiration.**
Exit losses: **-$11,211 across 35 positions.** Expired losses: **$0 across 0 positions.** All 56
expired legs in the ledger are winners, totalling **+$12,525**. Nothing this fleet has ever held
to settlement has lost money.

**2.2 It is not a large-move pattern.**
Underlying net move on the ten worst losses by R (ex `DIR-SPX-CallVIXdrop`) is +/-0.20% to 0.78%.
The single largest move in the sample — 2026-09-16, SPX -0.43% / QQQ -0.50% — was a **+$1,142
winning day**. Directional magnitude does not separate losers from winners. A hedge sized to the
move is dead weight.

**2.3 It is a clock pattern.** MAE timestamp, 0DTE IC bots only:

| MAE hour | Losers (n=28) | Winners (n=154) |
|---|--:|--:|
| 11:00-12 | 14% | 6% |
| 13:00-14 | 11% | **61%** |
| 14:00-15 | **36%** | 29% |
| 15:00-16 | **39%** | 3% |

Winners take their worst tick early and decay. **75% of losers have their MAE after 14:00, vs 32%
of winners.** **89% of all loss** ($-9,827 of $-11,011 across positions carrying an MAE timestamp)
has its MAE inside **14:00-15:30 ET**.

**2.4 The exits are realizing the worst tick.**
Positions closing within 5 minutes of their own MAE: **losers 12/30 (40%), winners 11/194 (6%).**
The stop is not capping the loss; it is booking the extreme.

**2.5 The losers were green first.**
**24 of 30** losers had positive MFE. Median MFE **+0.70%**, median MAE **-2.30%**. These are not
bad entries. They are working positions that gave it back in the last two hours.

**Top 10 losers by R, `DIR-SPX-CallVIXdrop` excluded** — -$7,459 on $31,500 risk, aggregate R
**-23.7%**, **67% of every dollar the fleet has lost**:

| # | Day | Bot | R | $ | Close | MAE @ | MFE |
|--:|---|---|--:|--:|---|---|--:|
| 1 | 08-27 | IC-SPX-FastPT25-S2-130PM | -37.1% | -1,800 | 14:28 | 14:28 | +1.0% |
| 2 | 09-08 | IC-SPX-FastPT25-S2-130PM | -34.4% | -1,650 | 16:15 | 14:49 | +1.0% |
| 3 | 08-26 | IC-SPX-FastPT25-S2-130PM | -31.2% | -1,500 | 15:05 | 15:05 | +1.0% |
| 4 | 09-08 | GF-QQQ-IC-SL100 | -18.1% | -910 | 14:49 | 14:49 | +0.4% |
| 5 | 09-08 | GF-QQQ-IC-SL200 | -18.1% | -910 | 14:49 | 14:49 | +0.4% |
| 6 | 08-21 | 60min-ORB-10W-Paper-v1 | -17.3% | -140 | 10:57 | 10:57 | -0.0% |
| 7 | 08-10 | 60min-ORB-10W-Paper-v1 | -16.5% | -150 | 12:38 | 12:38 | +0.3% |
| 8 | 08-26 | GF-QQQ-IC-SL200 | -10.5% | -20 | 15:50 | 15:05 | +0.7% |
| 9 | 08-26 | GF-QQQ-IC-Canary | -7.9% | -15 | 15:50 | 15:05 | +0.2% |
| 10 | 09-16 | GF-QQQ-IC-SL200 | -7.4% | -364 | 15:50 | 15:14 | +1.0% |

**Rows 6 and 7 are excluded from the pattern.** `60min-ORB-10W-Paper-v1` has its MAE at 10:57 and
12:38 — a different entry regime. Fitting a 14:00 rule to a 10:45 bot is how a spec acquires a
false positive. Model it separately or not at all.

---

## 3. ⛔ THE BLOCKING DEFECT — no arm may be ranked until it is closed

### 3.1 The hedge tournament has never seen a loss

`scripts/hedge_tournament.py` replays **only `status=expired` legs** (docstring, ARMS v1). Per
§2.1, **every expired leg in this ledger is a winner.** Verified in `data/hedge_tournament.csv`:
23 legs, 3 bots, **ride arm minimum R = +0.0204, zero losing legs.**

The 43 losing legs in the ledger are all `status=closed` and are excluded **by construction**.

The tournament is therefore a hedge evaluator whose sample contains no losses. That is why every
PT arm shows 100% WR and why `ride` wins — there was nothing to protect against. Its standings in
`STATUS.md` cannot rank a loss-capping mechanic, and should not be read as doing so.

This is a **fifth defect** of the same family as `hedge-research.md` §5.1's four. Same verdict
applies: not a weak measurement, **not a measurement**.

`data/hedge_tournament.csv` is also **stale** — last `open_date` 2026-09-04 against a ledger
running to 09-16.

### 3.2 Defang — not a gap, dead code

`hedge_tournament.py:50`/`:333` emit 23 `defang` marker rows with `modeled_pnl` empty, deferred for
want of an intraday premium path. **This is not a blocker and should not be treated as one.** Defang
is already excluded twice over — `oa-platform-reference.md` §11 row 5 (true defang as a single
action is NOT NATIVE) and `greenfield-family-spec.md` §3.1 (excluded as an arm; a workaround would
be an undocumented substitution at a platform limit) — and `IC-SPX-Fortress-Defang` is OFF in
`bots_meta.csv` with **zero rows in the post-cutover ledger**. The arm cannot be built, so modeling
it buys nothing. **Recommendation: delete the stub** from `hedge_tournament.py` and drop the
`Defang: deferred v1` line from `report.py:830`, so the standings stop advertising a gap that is
actually a closed decision. Ruling slot §9.6.

### 3.3 Root cause

The ledger carries entry, exit, MFE and MAE — four points, not a curve. **There is no intraday
premium path.** §3.1 needs one to model what any rule would have done between entry and an early
exit; §4's give-back trigger needs one to price "gave back X% of the high" in dollars at 14:30.
Closing it is the prerequisite for ranking anything, and it is the only item in this section that
is actually owed.

---

## 4. Proposed trigger

**T-H1 (proposed, unsigned):** a position is *deteriorating* when all three hold:

1. `mfe_pct > 0` has already occurred (the position was green), **and**
2. current mark has given back a threshold fraction of that high-water mark, **and**
3. wall-clock is at or after **14:00 ET**.

Rationale: (1) and (2) are what §2.5 and §2.4 describe; (3) is what §2.3 isolates. Condition (3)
alone would fire on the 29% of winners whose MAE also lands 14:00-15:00, so the time gate is
necessary but **not sufficient** — it must be conjunct with the give-back, never alone.

Thresholds are deliberately left as **`<FILL>`** — they are calibration, and calibration without
§3's premium path is invention.

---

## 5. ⛔ The platform wall

`oa-platform-reference.md` §11 rules three things NOT NATIVE that this trigger appears to need:

| Needed | Platform | Consequence |
|---|---|---|
| "Condition sustained for N minutes" | **NOT NATIVE** (§11 row 2) | Only build path is the ~10-rung tag ladder, which **fails safe-looking at every rung** and eats the 1-minute scan budget. Ruled out by `greenfield-family-spec.md` §3.1. |
| **Any condition referencing its own past** | **NOT NATIVE** (§11 row 6) | **A give-back-from-MFE decision node cannot be built.** T-H1 as written is not expressible as a decision. |
| True defang as one action | **NOT NATIVE** (§11 row 5) | Multi-leg workaround only; excluded as an undocumented substitution at a platform limit. |

**But** — `greenfield-family-spec.md` §3.1, falsified-and-reinstated 2026-08-06 by Phase-0 check
C2 — the platform **does** track a high-water mark natively, **inside exit primitives**:
`tstop` (`target` = activate at __% of credit, `trail` = close on __% pullback) and `maxtrail`
("Pullback is more than __% from high").

**So T-H1 is natively expressible as an EXIT and not as a HEDGE OPENER.** That is the central
design constraint, and it collides with §9.1 below.

---

## 6. Candidate instruments — re-ranked under `R-2026-09-16-HEDGE-DEFINITION`

A hedge is a **separate protective position**. An exit strategy is not a hedge. Applying that:

| # | Instrument | Hedge? | Expressible? | Disposition |
|--:|---|---|---|---|
| C1 | Armed trail (`tstop` target/trail), time-gated | **No — exit** | Yes, native | **Disqualified as a hedge.** May still be built and ranked as an exit arm; may not discharge a hedge item. Already the reinstated PR-16 mechanic — check double-testing first. |
| C2 | `maxtrail` pullback-from-high | **No — exit** | Yes, native | Same. |
| C3 | Time-gated flat close | **No — exit** | Yes, native | Same. |
| C4 | **Separate protective position opened on deterioration** | **Yes** | **Trigger NOT NATIVE** | The only true hedge on the list. Blocked — see §6.1. |
| C5 | Tag ladder for sustained touch | No — exit | Technically | Ruled out, `hedge-research.md` §7.1. |
| C6 | Defang | No — exit | NOT NATIVE | Ruled out twice over (§3.2). |

### 6.1 ⛔ The operative consequence

**Under this ruling the fleet has no buildable hedge on Option Alpha today.** Every natively
expressible candidate is an exit and is disqualified. The one true hedge, C4, needs a trigger that
`oa-platform-reference.md` §11 row 6 rules NOT NATIVE — *"any condition referencing its own past"* —
and give-back-from-high is self-referential by construction.

This is a finding, not a failure. It means the hedge program needs one of three things, and the
choice is **not ruled here**:

1. **A present-state trigger proxy** that never references the position's own history. Leading
   candidate: *at/after 14:00 ET, underlying within X of our own short strike* — time and distance
   are both present-state, so §11 row 6 may not bite. **Expressibility UNVERIFIED — must be probed
   in OA before it is specced**, and §2.2 warns that net daily move does not discriminate, so
   distance-to-strike must be tested against the ledger before it is trusted.
2. **An off-platform trigger** (webhook into OA), moving the self-referential logic outside.
3. **An explicit decision to accept a time-only opener** — blunt, and §2.3 shows a bare time gate
   also fires on the 29% of winners whose MAE lands 14:00-15:00.

Until one is chosen, §4's T-H1 stands as a **measurement definition** — the thing to detect and
count in the ledger — not as a buildable trigger.

## 7. Definition of done — inherited, not restated

Any arm built from this spec must satisfy **all five** conditions in `hedge-research.md` §5.2
(shared automation / one differing input proven by capture-diff; same execution class; Range075
carried via the shared entry automation per Architecture E; a pre-registration entry naming the
**platform primitive**; a proof-of-fire artifact identified in advance). An arm failing any of
them is not a weak arm — it is not an arm.

---

## 8. ⚠️ The v1 tournament's defect 1 is live again, right now

`hedge-research.md` §5.1 defect 1: *"`HedgeA-S1` and `HedgeD-Conditional` produced identical P/L
at an identical entry minute on 73 positions. They are one arm wearing two names."*

Measured this session on the current GF family: **`GF-QQQ-IC-Ride`, `GF-QQQ-IC-Touch0` and
`GF-QQQ-IC-Ride-Delta` are 100% identical** on every shared open — 27/27, 9/9, 9/9 — same close
timestamp, same P/L to the cent. Three of the eight-arm family are one arm wearing three names.

This is not a hedge-spec item, but it must be resolved before the GF family is used as the
measurement substrate for any hedge arm, or the same defect that invalidated the v1 tournament
invalidates this one.

---

## 9. Open rulings — for Andy

**9.1 — ✅ RULED 2026-09-16. `R-2026-09-16-HEDGE-DEFINITION`.**
Andy, verbatim: *"Rule of thumb going forward should be : separate protective position, exit
strategy != hedge"*. `hedge-research.md` §1.3 is **OVERRULED** (banner owed, original text stands).
**This disqualifies C1, C2 and C3 below as hedges** — they are exits. See §6 as re-ranked, and the
consequence in §6.1.

**9.2** Does this spec authorize paper arms, or measurement work only? (Draft assumes
measurement only, per the T4 tier.)

**9.3** Is the §3.1 tournament-universe defect fixed by widening the replay to `status=closed`
legs, or does that break the ride-arm reconciliation (`hedge_tournament.py` recon: ride sum ==
ledger expired-pnl sum, per day)? Widening likely requires re-deriving that invariant.

**9.4** Priority: does the intraday premium-decay path (§3) get built before or after the F-6
config-capture gap, which blocks stage 3/4/8 grading?

**9.5** `<FILL>` thresholds in §4 — not to be filled until §3.3 is closed.

**9.6** Delete the `defang` stub from `hedge_tournament.py` and its `report.py` standings line
(§3.2)? Draft recommends yes — it advertises an open gap where there is a closed decision.

---

## 10. What this spec does NOT do

- Does not rank any mechanic. §3 says ranking is currently impossible.
- Does not name thresholds. Calibration without the premium path is invention.
- Does not authorize an OA edit, a bot build, or a slot.
- Does not apply to `DIR-SPX-CallVIXdrop` (debit/directional — `hedge-research.md` §5.3: the exit
  *is* the hedge) or to `60min-ORB-10W-Paper-v1` (§2.5, different clock).
