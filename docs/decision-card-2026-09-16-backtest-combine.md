# Decision card — 2026-09-16 — native compare & combine

**FIVE SLOTS — NONE RULED.** Raised by Andy in-chat 2026-09-16, verbatim: *"Does this plan know
that backtests can be duplicated as variants and compared? And then we can add several backtests
to a portfolio to compare? This is all native in the OA."*

Answer: **the plan did not.** The capability is documented in `data/oa_facts.csv` (harvested
2026-08-04) and was observed first-hand in the 2026-09-16 Phase-0 capture, and neither
`docs/hedge-north-star.md` §4 nor `docs/hedge-design-spec-2026-09-16.md` §6.1 cites either source.
Slots 1, 2 and 5 change what gets built and are therefore **gated** (`CLAUDE.md` §5). Nothing in this
card is applied.

---

## The finding — on two independent surfaces

Per `verification_surfaces`: two agreeing derivations would be weaker than one check against a
different surface. These are different surfaces — vendor documentation and a dated device read.

### Surface 1 — `data/oa_facts.csv`, harvested 2026-08-04

| fact ID | status | verbatim |
|---|---|---|
| **OA-1090** | DOCUMENTED | *"and compare up to four backtests simultaneously,"* |
| **OA-1077** | DOCUMENTED | *"Then, combine the results of multiple strategies into one portfolio curve."* |
| **OA-1091** | DOCUMENTED | *"and combine multiple backtested strategies to see a single portfolio P/L curve."* |
| **OA-1141/1142** | DOCUMENTED | the docs page *"Comparing and combining backtests"* is **an empty embed block** — `{% embed url=" " %}` |
| **OA-1143/1144** | DOCS-SILENT | the procedure for comparing, and for combining into a portfolio curve, is **not explained anywhere** |

The capability is documented. The **procedure** is documented nowhere — which is why a docs-first
research pass could harvest the facts and still not surface them as a method.

### Surface 2 — `data/captures/2026-09-16-oa-backtester/01-backtest-settings-form-2026-09-16-223758.txt`

sha256 `02376a44a3b60afdaf069974ae50292f4cdc93e2bfe10003413ae6fcfebe9973`, captured
2026-09-16 22:37:58-04:00. Lines 219-222, verbatim:

```
[OA Portfolio tab - /backtests/portfolio - published backtest library]
Tabs verbatim: "My Backtests 65 · Saved Backtests 0 · Top Backtests 1.4M · OA Portfolio"
Compare link navigates to /backtests/compare/<ids>: "Compare Backtests · Save · Add Backtest ·
Results · Combine Results" - aggregates equity curves of independent single-structure backtests.
```

Verbatim UI controls: **`Compare Backtests`** · **`Save`** · **`Add Backtest`** · **`Results`** ·
**`Combine Results`**. Route: **`/backtests/compare/<ids>`**. Existing inventory: **65 backtests**.

### Why it was missed

The Phase-0 recon **did find it** and filed it as the last line of its findings list, framed as a
negative — *"it combines results, not positions inside one test"* — answering the question the
dispatch asked. The dispatch asked whether **one backtest** can hold a second position. The answer
is NO and it is correct. The question that mattered — whether **two backtests** can be combined
into one curve — was never asked, so a YES sitting in the same capture read as a disclaimer.

⭐ **Lesson for the register:** a dispatch question scoped to one object cannot return a finding
about the relation between two. `NOT EVALUABLE` guards against a confident wrong answer; nothing in
the current dispatch format guards against a **correct answer to the wrong question.**

---

## What it changes — the variant frame re-mapped

`hedge-north-star.md` §4's premise, *"neither OO nor OA's backtester can open a second position
mid-trade,"* is **true per backtest and irrelevant across backtests.** `Position Limit: 1 position`
is a per-config constraint, which is precisely why combining works.

| | §4 as written | Under this card |
|---|---|---|
| **V0** — 130PM condor, no hedge | native | native, unchanged |
| **V1** — short-strike touch → tested-side debit spread | joined, manual | **native combine** — trigger is underlying state, so it runs as its own backtest |
| **V2** — underlying % move since open → debit spread | joined, manual | **native combine** — same |
| **V3** — condor return −X% → debit spread | joined, approximate | **unchanged — still cross-position.** The only variant that needs the intraday premium path |
| **V4** — far-OTM put / strangle at 1:30 | native + trivial join | **native combine** |

**Consequence: `hedge-design-spec-2026-09-16.md` §3.3 (the intraday premium path) comes off the
Phase-1 critical path.** It gates V3 and the ledger-side ranking. It does not gate the grid.

⚠️ **The limit of this, stated plainly so no arm is mis-ranked.** Combination is expected to be
**additive at the portfolio level** — both backtests run their own entry rules independently over
the same period. It does **not** make the hedge's entry conditional on the condor's state.
Therefore **V1/V2 combined are not reactive hedges; they are unconditional overlays that trade on
the same days.** That is a valid and far cheaper Phase-1 measurement — it yields cost-per-fire and
bleed-on-false-fires directly — but the pass bar must say so in those words, or the program ranks
an overlay and calls it a hedge. This is the `HedgeD-Conditional` failure mode (−$15,376: a
mechanic named without its platform primitive) approaching from the opposite direction.
**Whether combination is additive-only is UNVERIFIED and is the first thing Phase 0b must answer.**

---

## Slot 1 — replace §4's research method  ⬜ UNRULED

Replace `hedge-north-star.md` §4's *"The way around it"* paragraph and the **How tested** column of
the variant table. Proposed text:

> **The way around it:** OA combines backtests natively. `/backtests/compare/<ids>` exposes
> `Add Backtest` and `Combine Results` (first-hand capture 2026-09-16, sha `02376a44…`), and
> **OA-1077** documents *"combine the results of multiple strategies into one portfolio curve."*
> Run each hedge structure as its own standalone backtest over the fixed frame, then combine it
> with the condor backtest in the Compare surface. The manual day-by-day join is reserved for V3
> alone, whose trigger references the condor's own P&L and therefore cannot be expressed as an
> independent backtest's entry filter.

**Rejected alternative:** keep the manual join as primary and treat combine as a cross-check.
Rejected — it spends the expensive lane (agent-hours of transcription plus a bespoke join script)
to reproduce a rendered number, and every transcription is a fresh opportunity for the
config-capture defect class. Combine becomes primary; a **single** hand-joined variant is retained
as the cross-check against a different surface.

---

## Slot 2 — rewrite the dispatch's Phase-0 question  ⬜ UNRULED

`docs/dispatch-oa-capture-2026-09-16.md` Phase 0 is **answered and closed** — the bundle exists and
the answer is NO. Proposed replacement, **Phase 0b**, read-mostly, on the authorized UI path:

> **PHASE 0b — the Compare & Combine surface.** Andy has 65 existing backtests. Open
> `/backtests/compare/<ids>` with two of them and answer, with screenshots and **verbatim** labels:
>
> 1. **Procedure** — how backtests are added to a comparison and combined. OA-1143 and OA-1144 are
>    DOCS-SILENT on exactly this; the capture is the only possible record.
> 2. **Granularity** — does the combined portfolio curve expose **per-day rows**, or summary stats
>    only? Day-level is what the loss anatomy and the day-strip heatmap require. Summary-only means
>    two trade lists still get transcribed and joined by hand, and Slot 1's saving shrinks.
> 3. **Conditionality** — is combination additive at the portfolio level only, or does any control
>    condition one backtest's entries on the other's state? **This is the load-bearing question.**
>    Expect additive; report what is rendered, not what is expected.
> 4. **Size ratio** — is there a control for relative sizing between combined backtests, or is it
>    1:1? Size ratio is a required field of the Monitor spec (`hedge-north-star.md` §6). If absent,
>    the ratio has to be swept as separate backtests and the grid grows.
> 5. **Duplicate fidelity** — does duplicating a config preserve the full fixed frame so only the
>    differ changes? If yes it also retires the `text`/`textValues` display-string trap on the 21
>    untouched fields, which is a second reason to prefer duplicate over hand-construction.
> 6. **Ceiling** — confirm or falsify OA-1090's *"up to four backtests simultaneously"* against the
>    live surface, and record whether the four-way cap applies to `Compare` only or to
>    `Combine Results` as well.
>
> **Naming.** Any saved comparison lands in shared account state exactly as a saved backtest does.
> `ZZ-AGENT-<YYYY-MM-DD>-<arm>` applies to it (`-A2`), or nothing is saved at all.

---

## Slot 3 — the four-backtest ceiling vs a five-variant frame  ⬜ UNRULED

OA-1090 caps simultaneous comparison at **four**. The frame is **V0–V4 — five.** §4's "single
screen" spec (five equity curves overlaid, one stats column per variant) cannot render as written.
Three options, none ruled:

- **(a)** Two comparisons sharing V0 as the common control: `V0/V1/V2` and `V0/V3/V4`. Preserves
  every variant; the control appears twice, which is also a free consistency check — V0's curve
  must be identical in both or something is wrong with the fixed frame.
- **(b)** Drop V3 from the on-screen compare (it is the manual-join variant anyway) and render
  `V0/V1/V2/V4` in one view.
- **(c)** Confirm the cap first in Phase 0b item 6 and rule after. **Draft recommends (c) then (a).**

---

## Slot 4 — was the Phase-0 capture inside the authorization boundary?  ⬜ UNRULED — permission question, raise before the next capture

The bundle's own README states it was taken *"over CDP against Andy's authenticated Chrome"* and
that `01-…txt` contains *"rendered innerText + all 51 serialized form inputs."*

`R-2026-09-16-DEVIN-OA-CHROME-CAPTURE-A1` scopes the grant to driving the interface **as a user
does** — navigate, click, read what is rendered, screenshot, OA's own Export Data — and excludes
page-context inspection. Reading rendered innerText is plainly inside. **Serializing 51 form
inputs, including hidden ones, is not obviously inside**, and the same file quotes a hidden
`name=series type=hidden` payload at line 90.

This is raised as a question, not a charge: the capture produced no edit, no save and no run, and
its findings stand. But the boundary is Andy's to state, and stating it now is cheaper than
discovering it in the middle of a 25-run grid. **No further capture should read hidden inputs until
this is ruled.**

---

## Slot 5 — which surface dispatches the OA grid  ⬜ UNRULED

Raised by Devin 2026-09-16, correcting an earlier claim in the Cowork chat that OA-lane dispatch
requires Andy pasting into Devin Desktop. **The correction is accepted on mechanism and rejected on
readiness.**

**Accepted.** Claude Code (terminal) is the foreman for both lanes — `docs/state.md` "Lane note"
already says dispatch and foreman duty belong there, not in Cowork. Two surfaces exist:
`devin_session_create` (cloud, repo-only, no local Chrome) and the local CLI lane
`scripts/devin_free.sh` → `~/bin/devin-free` (runs on the laptop, so a spawned session can in
principle attach to the authenticated Chrome). Andy's paste-into-Desktop is one manual route, not
the only one. Caveat (c) is right and unchanged: the hand-launched Chrome login stays, the grant is
UI-only, `zdte.*` stays parked.

**Rejected as ready.** Three blockers, all already in this repo, none mentioned in the correction:

**5a — the cost guard is on the wrong lane.** The correction puts the model-pin caveat on the CLI
lane. That lane *can* pin; it is the only one that can. `devin_session_create` exposes **no model
parameter at all** — its only agent selector is `devin_mode` (`normal`/`fast`/`lite`/`ultra`/
`fusion`), none of which resolves `swe-1-7`, so an MCP session inherits the org default and
**cannot be guaranteed free**. Proposing MCP as dispatch surface #1 without that caveat inverts the
risk. *A dispatch surface that cannot express the cost constraint is not a cheaper dispatch
surface — it is an unguarded one.* **Ruling needed:** MCP for repo work only with an explicit
per-session cost assertion, or not at all.

**5b — the CWD guard makes CLI-driven OA work non-executable today.** `scripts/devin_free.sh`
refuses, above exec, `exit 2`, to run anywhere inside `$HOME/bot-fleet-v2`, `$HOME/gitstore` or
`$HOME/bot-fleet`, and **the guard resolves `--workspace`, so pointing at the live tree is refused
exactly like standing in it** (script header, lines 29-33 and 64-68). The OA grid's deliverable is a
capture bundle under `data/captures/` **in the live repo.** So the lane as proposed refuses itself.
**Ruling needed:** foreman runs sessions in a scratch workspace outside all three roots and moves
bundles into the repo itself, or the wrapper is amended. Draft recommends the former — the guard is
the only thing left standing between a wrapper invocation and a session loose in the live repo once
`skip_workspace_trust` is in play.

**5c — "settle the pin conflict" is a wrapper redesign, not a flag.** `docs/state.md` lines 62-67
already carries this as unresolved and already says **"Resolve before any CLI dispatch."** The part
the correction omits: the wrapper **refuses `--model` by design** — that refusal is the wrapper's
entire reason to exist, because `swe-1-7-lightning` prefix-matches `swe-1-7` and is PAID. So the
options are (i) the wrapper learns SWE-2 MAX as a second hardcoded constant, touching the one file
whose purpose is that the model is not an argument, or (ii) the CLI lane stays `swe-1-7` and
SWE-2 MAX remains Desktop-only. Draft recommends (ii) until a live `acu 0.0` receipt exists for
SWE-2 MAX on the CLI backend. Caveat (b) stands too: `devin auth status` is verified before the
lane is relied on, every session.

**5d — one unproven premise, cheap to close.** Dispatching Devin from Claude Code is well
established. **A `devin-free`-spawned session attaching to Chrome and driving OA is a different
claim, and no session-log entry records it** — the CDP/Playwright driving on record
(`session-log.md` 2026-08-19, and the 2026-09-16 Phase-0 capture) came from other lanes. Per
`fleet_harness_lessons`, an agent's claim of a capability is not the capability. **Prove it with one
session** — attach, read one rendered backtest, exit — before the lane carries 25+ agent-hours.

**5e — the grid shrinks before the foreman is built.** The correction argues the foreman shape is
right "for the ~175-run §4 grid." Under Slot 1 that grid is the wrong size: V1/V2/V4 become
combines of a much smaller set of standalone hedge backtests, and Phase 0b may shrink it further.
Sizing the dispatch machinery to a number that is about to change produces inventory, not output.
**Order: rule Slot 1 → run Phase 0b → re-size the grid → then choose the dispatch surface.**

---

## What this card does NOT do

- It does not rank any mechanic, authorize any paper arm, or change any evidence tier. Backtest
  figures remain **T4** — paper arms and measurement only, never a live-capital decision
  (`CLAUDE.md` §4).
- It does not amend `R-2026-09-16-HEDGE-DEFINITION`. A combined overlay is still not a reactive
  hedge, and this card says so twice deliberately.
- It does not reopen the RPC path. `R-2026-09-16-DEVIN-OA-CHROME-CAPTURE-A1` stands; everything
  proposed here is the authorized UI path.
- It does not close `hedge-design-spec-2026-09-16.md` §3.3. It removes §3.3 from the Phase-1
  critical path and leaves it owed for V3 and for ledger-side ranking.

## Open, carried from the prior card

- §9.2 — does the hedge spec authorize paper arms, or measurement only?
- §9.4 — intraday premium path before or after the F-6 config-capture gap?
- §9.5 — `<FILL>` thresholds, blocked on §3.3.
- §9.6 — delete the `defang` stub.
- §7 assumption register (T-57) — before or after the first grid, still unruled. Draft
  recommends a **scoped** register first: only the assumptions the hedge grid leans on.
- The GF triple-identity defect (`hedge-design-spec` §8) — `GF-QQQ-IC-Ride`, `-Touch0` and
  `-Ride-Delta` are 100% identical on every shared open. Unresolved, and it blocks the GF family
  from serving as the measurement substrate for any hedge arm.
