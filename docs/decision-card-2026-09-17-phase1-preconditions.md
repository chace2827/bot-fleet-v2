# Decision card — 2026-09-17 — Phase 1 preconditions

**Status: ✅ BOTH SLOTS RULED 2026-09-17** (Andy, in-chat: *"i agree w reccomendations"*). Originally drafted as two unruled slots. Drafted by the Cowork session at Andy's instruction while
Phase 0c runs, so that Phase 1 has zero open gates when Devin reports. This card authorizes
nothing by itself (`CLAUDE.md` §5 — decisions are gated).

**Why now.** Phase 0c answers a *platform* question. These two are **not platform questions** and
will not be answered by any capture. Left unruled, they surface after the grid has run, which is
the expensive place to find them.

---

## ⚠️ Finding first — `hedge-design-spec-2026-09-16.md` §8 is STALE, and the defect is smaller than it reads

§8, written 2026-09-16, states:

> *"`GF-QQQ-IC-Ride`, `GF-QQQ-IC-Touch0` and `GF-QQQ-IC-Ride-Delta` are 100% identical on every
> shared open — 27/27, 9/9, 9/9 … Three of the eight-arm family are one arm wearing three names."*

**The measurement stands. The scope does not.** `R-2026-08-17-PR23-RETIRE` (RULINGS.md, Andy's own
words, 2026-08-17 — one month *before* §8 was written) already retired one of the three:

> *"PR-23 / GF-QQQ-IC-Ride-Delta is RETIRED. Under the shared delta scanners it is redundant with
> PR-14 (GF-QQQ-IC-Ride) on every axis."*

So the live defect is a **PAIR, not a triple: `GF-QQQ-IC-Ride` vs `GF-QQQ-IC-Touch0`.** Ride-Delta's
identity was ruled and dispositioned a month ago; §8 re-discovered it and counted it as open.

**What that changes:** one of the three legs needs no work, and the remaining question is narrow and
answerable — *has `Touch0`'s touch trigger ever fired, and if it has not, is it an arm or a duplicate
of Ride?* A grep of the ledger for a `Touch0` close attributable to a touch answers it. That is a
much smaller gate than §8 implies.

**What it does NOT change:** `Touch0` vs `Ride` is still unruled, and `hedge-research.md` §5.1
defect 1 (`HedgeA-S1` / `HedgeD-Conditional`, 73 positions, one arm two names) is the precedent that
invalidated the v1 tournament. The class of error is real; the count is wrong.

📝 **Owed regardless of both slots below:** a dated staleness banner on `hedge-design-spec` §8 citing
`R-2026-08-17-PR23-RETIRE`, original text standing. ✅ **APPLIED 2026-09-17** — evidence-backed correction of a falsified count (`CLAUDE.md` §5), not a
decision. Original §8 text stands above the banner.

---

## Slot A — Does Phase 1 rank against LIVE GF results, or is the grid self-contained?  ✅ RULED A3 — `R-2026-09-17-PHASE1-SUBSTRATE-SPLIT`

**Why this is not obvious.** The Phase 1 arm table already reaches into live GF data without saying
so. `docs/dispatch-oa-capture-2026-09-16.md`, arm **H-C**, verbatim:

> *"Both are **net negative on live data** (-$173, -$584), the only two GF arms underwater. If the
> hedge cannot beat a stop that is already losing money, it is not a finding."*

That is a **live-ledger number used as the bar a backtest arm must clear.** Backtest-vs-live is a
cross-surface comparison nobody ruled, and it is the seam where the GF identity defect would enter.

**Mitigating fact, stated so the slot is not over-weighted:** the identity pair is `Ride` / `Touch0`.
H-C rests on `SL100` / `SL200`, which are **not** implicated. H-C may be clean even if the pair is
not. The exposure is to any *later* ranking that touches Ride or Touch0, not to H-C as written.

| | Option | Consequence |
|---|---|---|
| **A1** | **Self-contained grid.** No live GF number enters any Phase 1 ranking. H-C's −$173/−$584 demote to context, and H-C's bar is restated in R against H-0. | Launch is **not gated** by the identity defect. Cheapest. Loses the incumbent-to-beat framing. |
| **A2** | **Ranks against live GF.** | The `Ride`/`Touch0` identity must be resolved **before** the grid runs, and H-C's two figures re-verified against the post-cutover ledger with their unit labels. Gates launch. |
| **A3** | **Split.** Grid is self-contained and launches now (A1); a separate, later **ledger-side comparison** is defined as its own deliverable and IS gated on the identity resolution. | ⭐ **Recommended.** Nothing blocks, nothing is quietly compared across surfaces, and the defect gets a real gate instead of an implicit one. |

**Draft recommends A3.** Rejected alternative recorded: A1 alone, because it silently discards the
incumbent-to-beat question rather than scheduling it.

---

## Slot B — `hedge-design-spec` §9.2: does the spec authorize paper arms, or measurement only?  ✅ RULED B3 — `R-2026-09-17-PAPER-ARM-PREAUTH` (bar accepted as proposed)

The spec's draft assumes **measurement only**, on the T4 tier. That assumption has never been ruled,
and it decides what "Phase 1 done" means.

**The calendar fact that makes this worth ruling now**, `hedge-north-star.md` §6 verbatim:

> *"**The paper phase cannot be shortened** — it depends on how often the hedge fires. A 3–5
> fires/month trigger needs 2–3 months for ~10 fires."*

Paper is the long pole. Ruled B1 and left there, the 2–3 months starts only after the grid is
finished and separately re-ruled — serial. Ruled B2, it can overlap.

| | Option | Consequence |
|---|---|---|
| **B1** | **Measurement only.** Phase 1 ends at a ranked T4 grid plus a written Monitor-spec candidate. Any paper bot needs a fresh ruling. | Safest, and the draft's standing assumption. Adds 2–3 months **serially** to anything actionable. |
| **B2** | **Paper arms authorized on a PASS.** | Compresses the calendar. But a blanket authorization lets a weak grid result walk into a paper slot. |
| **B3** | **Measurement only, PLUS a pre-authorized paper arm for the SINGLE winning variant**, contingent on a pass bar written into this card *before* results exist, and pre-registered per `CLAUDE.md` §5 (hypothesis, kill criterion, sample target, review date, config-capture hash). | ⭐ **Recommended.** Gets B2's calendar compression without B2's blanket. The bar is set blind, which is the only time it is honest. |

**Draft recommends B3, with the pass bar named in the ruling, not after.** Proposed bar, for Andy to
accept or replace: *the winning arm beats H-0 on Exp(R) per condor ex-artifact, beats both H-C stop
arms, and its fire count implies ≥10 fires within 3 months.* A variant that cannot clear a bar
written before the data exists is not a finding.

⚠️ Note for whichever option is chosen: backtest figures remain **T4** (`CLAUDE.md` §4). A paper arm
is not live capital, and nothing in this slot touches the live-capital gate (T2, n≥100 / 6 months /
a regime change).

---

## What this card does NOT do

- It does not rank any mechanic, name a threshold, or authorize an OA edit or a bot build.
- It does not amend `R-2026-09-16-HEDGE-DEFINITION`, `R-2026-09-17-COMBO-RULES-PRESENCE-ONLY`, or
  the frozen `build-plan.md`.
- It does not resolve the `Ride`/`Touch0` identity. It scopes when that resolution is required.
- It does not close `hedge-design-spec` §3.3 (still owed for V3 and ledger-side ranking), §9.4,
  §9.5, §9.6, or the T-57 assumption register.

## Open, carried

- §9.4 — intraday premium path before or after the F-6 config-capture gap.
- §9.5 — `<FILL>` thresholds, blocked on §3.3.
- §9.6 — delete the `defang` stub (draft recommends yes).
- T-57 assumption register — scoped-register-first is the standing draft recommendation.
- Slot 4 from the 2026-09-17 in-chat sitting: (a) narrow the transcribe-by-hand regime rather than
  strike it; (b) Compare-7 free, Combine held at a fixed test count pending Phase 0c task 4.
