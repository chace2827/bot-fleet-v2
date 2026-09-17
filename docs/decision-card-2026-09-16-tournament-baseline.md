# Decision card — 2026-09-16 — the tournament baseline

**ONE SLOT. NOT RULED.** Drafted for Andy's signature; closes §9.3 of
`docs/hedge-design-spec-2026-09-16.md`. Nothing here is applied.

---

## Finding that reframes the slot: the reconciliation is a no-op

§9.3 was written on the premise that widening the replay past `status=expired` would **break the
ride-arm reconciliation**. Dated first-hand device read, 2026-09-16: **it cannot break, because it
does not check anything.**

`scripts/hedge_tournament.py`:
- `:200` `arm_ride(leg)` returns `fl(leg["pnl"])` — the ledger `pnl` column verbatim, with **no
  reference to `status`**.
- `:306` `ride_check[day] += pnl` (that same value) and `:307` `ledger_check[day] += fl(t["pnl"])`
  are incremented **in the same loop iteration, from the same leg**.
- `:345-348` then asserts the two dicts agree per day.

Both sides are the same number, summed over the same population, in the same pass. The
`risk <= 0` guard at `:292` `continue`s **before both** increments, so they cannot even diverge on
skipped legs. `ride_check == ledger_check` is **tautologically true**.

It is not a correctness check. It is a check that addition works.

**Consequence for the slot:** the barrier §9.3 guarded against is not there. The real question is
not "how do we preserve the invariant" but **"what should the invariant have been, and what is the
baseline each rule is scored against."**

---

## The slot

### Proposed ruling — `R-2026-09-16-TOURNAMENT-BASELINE` (UNSIGNED)

**1. The replay universe widens** from `status=expired` to every leg with a positive `risk`.
`:279` `expired = [t for t in trades if t["status"] == "expired"]` becomes the full set. This
admits the **43 losing legs** the engine has never seen (all `status=closed`), which is the entire
reason the tournament cannot currently rank a loss-capping mechanic
(`hedge-design-spec-2026-09-16.md` §3.1).

**2. The baseline becomes per-population, and the arm is renamed.**

| Population | Baseline | Meaning |
|---|---|---|
| `status=expired` | settlement | riding *is* what happened — unchanged |
| `status=closed` | **what actually happened** | the recorded early exit |

The `ride` arm is renamed **`actual`**. Every rule's `else` branch changes from *"else ride"* to
*"else actual"*: **a rule that did not fire yields what the position actually returned.** It does
not claim the position would have recovered.

**3. This is backward compatible, and that is testable.** `arm_ride` already returns the `pnl`
column verbatim for any leg, so on the expired population `actual` **is** settlement, bit for bit.
**Acceptance test: re-run restricted to `status=expired` and every existing number in
`data/hedge_tournament.csv` must be unchanged.** A single altered value means the change did more
than it was authorized to do.

**4. What is NOT evaluable, and must be marked, never modeled.** For a closed leg the position
stopped generating data at its exit. Therefore:
- **Evaluable:** any rule whose trigger timestamp falls at or before the actual close — i.e. rules
  that would have **intervened earlier**. `mfe_date`/`mae_date` are bounded by the position's life,
  so all threshold rules qualify.
- **NOT EVALUABLE:** anything requiring the position to have continued past its actual exit — the
  hold-longer counterfactual, and the "would it have recovered" hypothesis. These emit a
  `NOT EVALUABLE` marker, as `defang` already does at `:333`. **They are never modeled**
  (`hedge_tournament.py` docstring: *"v1 = mark approx or defer with a clear TODO; do not fake
  precision"*).

> ⚠️ The hold-longer direction is where the strongest hypothesis lives — `hedge-design-spec`
> §2.4 shows 40% of losers close within 5 minutes of their own MAE. This ruling does **not** answer
> it and must not appear to. It is answerable only in OA's `zdte.*` backtester, which simulates the
> full path (spec §3 banner, §6.1 option 4), and that path is gated on written OA authorization.

**5. The dead recon is replaced by three checks that can actually fail:**
- **Population:** replayed leg count == count of `trades.csv` legs with positive `risk`. Catches the
  currently-silent drop at `:292`.
- **Ordering law:** for every *fired* rule on a closed leg, trigger timestamp `<=` actual
  `close_date`. This is item 4's rule, machine-checked rather than trusted.
- **Bounds:** every `modeled_pnl` lies within `[-risk, credit_basis]`. Catches fabrication.

**6. Scope limit.** This changes what the engine measures against. It does **not** change any
evidence tier, sample gate, kill criterion or go-live gate, and it ranks nothing by itself.

---

## Why this is the right baseline

It is the question that was actually asked. Andy, 2026-09-16: *"which hedges would have turned a
losing position to less neutral or positive."* The comparison target in that sentence is **what
happened**, not settlement. The engine has been scoring every rule against a settlement the losing
positions never reached — which is the same defect as §3.1 wearing different clothes.

**Rejected alternative:** keep `ride` on all legs and model settlement for closed legs. Rejected —
it invents the one number the data cannot supply, and it does so in the arm every other arm falls
back to, so a single fabricated value would propagate into every rule's `else` branch.

---

## If signed — the Devin queue item (drafted, not yet added to `docs/devin-queue.md`)

> **H-1 — widen the hedge tournament to the closed-leg population.** Implements
> `R-2026-09-16-TOURNAMENT-BASELINE`. Base on `origin/master`, not the working tree
> (`devin-dispatch-discipline`). Changes: `:279` universe; `arm_ride` → `arm_actual` with the
> `else actual` fallback in `arm_pt`/`arm_sl`; `NOT EVALUABLE` markers per item 4; the three checks
> in item 5 replacing `:343-348`; regenerate `data/hedge_tournament.csv` (currently **stale** — last
> `open_date` 2026-09-04 against a ledger running to 09-16); update the `report.py` standings
> section to show the two populations **separately and never pooled**.
> **Acceptance:** item 3's regression test passes — expired-only re-run reproduces every existing
> value unchanged. Deliver as a `devin/*` PR. No OA dependency; runs entirely against `trades.csv`.

---

## Open, not in this slot

- §9.7 probe (can `zdte` express a second position) — blocked on written OA authorization.
- Terminology sweep under `R-2026-09-16-HEDGE-DEFINITION` — gated, unruled.
- `hedge-research.md` §1.3 overrule banner — owed.
- §9.6 defang stub deletion.
