# OA position-export schema — verified conventions

*Written 2026-08-04. Every claim below is **[FIRST-HAND, MACHINE-VERIFIED]** against
`data/captures/oa_export_positions_2026-07-30.csv` (n=1,386, sha256 `dca69ada…fcadc`) with the
mismatch count stated. This file exists because the folder documented a convention for every
platform behaviour and none for its own primary data source — and that gap produced a live bug on
2026-08-04 (see §5).*

---

## 1. Columns

`botName · type · description · symbol · status · quantity · daysInTrade · openPrice ·
closePrice · premium · pnl · ror · returnPct · risk · ev · alpha · highReturnPct · lowReturnPct ·
highReturnPctDate · lowReturnPctDate · expiration · openDate · closeDate · tags · underlyingOpen ·
underlyingClose`

## 2. ⚠️ THE SIGN CONVENTION — the one that bites

**`premium` is SIGNED BY CASH-FLOW DIRECTION.** It is **negative for every credit structure** and
positive for debit structures. `openPrice` is the unsigned per-contract price and is **positive on
1,386/1,386 rows**.

| structure | n | `premium` sign | identity | mismatches |
|---|---|---|---|---|
| `ironcondor`, `ironbutterfly`, `shortputspread`, `shortcallspread` | 1,373 | **negative** | `premium == -openPrice × 100 × quantity` | **0** |
| `longputspread`, `longcallspread` | 13 | positive | `premium == +openPrice × 100 × quantity` | **0** |

**Use `openPrice` when you want a magnitude. Use `abs(premium)` if you must use `premium`. Never
take `premium` at face value as "the credit".**

`build_ledger.py` already does the right thing: the ledger's **`credit` column is populated from
`openPrice`**, so anything reading `trades.csv` is safe. `premium` is carried through as a raw
passthrough column and keeps its sign — do not confuse the two.

## 3. Verified identities — all 0 mismatches

| identity | scope | n | mismatches |
|---|---|---|---|
| `pnl == (openPrice − closePrice) × 100 × quantity` | credit structures | 1,373 | **0** |
| `pnl == (closePrice − openPrice) × 100 × quantity` | debit structures | 13 | **0** |
| `returnPct == pnl / abs(premium)` | all | 1,386 | **0** |
| `ror == pnl / risk` | all | 1,386 | **0** |

`returnPct` is therefore **return on credit**; `ror` is **return on risk**. They are different
denominators and the project's R convention (`CLAUDE.md` §4) is the **`ror` basis**, not `returnPct`.

## 4. MFE / MAE — present, timestamped, and on the credit basis

`highReturnPct` / `lowReturnPct` are maximum favourable and adverse excursion, **populated on
1,386/1,386 rows**, expressed on the **same basis as `returnPct`** (fraction of `abs(premium)`).

`highReturnPctDate` / `lowReturnPctDate` are **full timestamps to the minute**, e.g.
`2026-07-01 09:31:00` — not dates. `build_ledger.py` carries all four into `trades.csv` as
`mfe_pct · mae_pct · mfe_date · mae_date`.

**What they can and cannot answer.** They give the *extreme* and *when it occurred*. That makes a
profit-target or stop-loss counterfactual decidable — if the mark reached the level at any point,
the order fills. It does **not** make a *time-exit* counterfactual decidable: the mark at 15:45 is
not an extreme and is not recorded anywhere in this export. Time-exit questions require a live A/B
arm. (`research-loop-spec.md` §2; the `TIME_*` variants return `UNDECIDABLE` by design.)

⚠️ **MFE/MAE are marks, not fills**, and are sampled at the bot's Scan Speed (1/5/15 min), so they
are the max *observed*, not the true intraday max. The error is **one-sided: it flatters tighter
profit targets.** They also have **no second witness** — nothing else on hand can check them, unlike
`risk`, which `execution_audit.py` re-derives from leg strikes. Treat as
`[FIRST-HAND, UNCORROBORATED]`.

## 5. The bug this file exists to prevent

On 2026-08-04 a dry-run harness hand-mapped `credit = premium` straight off the raw export. Because
`premium` is negative for credit structures, a `credit <= 0` guard rejected **1,247 of 1,254
positions** as undecidable. The engine then printed `DSTOP_50R +89/pos` — a mean over **seven**
positions, rendered identically to a mean over all 1,254.

Nothing shipped and no committed script was affected (`execution_audit.py` reads `credit`, which is
`openPrice`, which is positive). Two fixes came out of it:

1. **Never print an aggregate without its `n`.** A mean over 7 and a mean over 1,254 must not look
   the same. `research_loop.py` now prints the decidable count beside every mean.
2. **Every validation fixture must include at least one row copied verbatim from a real capture.**
   Synthetic rows test logic; only real rows test conventions. The 18-check fixture was fully green
   while the harness was wrong, because every row in it was hand-authored with a positive credit.

## 6. Other observed facts

- `status` ∈ {`closed` (1,232), `expired` (154)}. **`expired` is not a close** — `execution_audit.py`
  excludes it from PT-consistency, because a ride to worthless captures 1.00 and is not a PT fill.
- `risk` is **positive on 1,386/1,386**; `execution_audit.py` re-derives it from leg strikes as a
  second witness and never trusts this column alone.
- `type` ∈ {`shortputspread` 687, `shortcallspread` 559, `ironcondor` 102, `ironbutterfly` 25,
  `longcallspread` 8, `longputspread` 5}.
- `description` carries the leg list as `<sign><strike> <side>`, where **`-` = SHORT and `+` = LONG,
  universally across structures** (`build_ledger.parse_strikes`).
- `quantity` varies widely (1 … 100+). Every per-contract identity above needs the `× quantity`
  term; omitting it is silent and wrong only on multi-contract rows.
- An **iron condor arrives as ONE row**, not two. Single-sided spreads are paired into condors by
  `build_ledger.py` on a time window; unpaired short spreads are flagged `single_sided`.

---

*Re-verify this file against a fresh export before Day-0. OA changes its product and its docs
demonstrably lag it; there is no reason to assume the export schema is more stable than either.*
