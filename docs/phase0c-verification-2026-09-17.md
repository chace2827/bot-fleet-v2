# Phase 0c — independent verification pass

**Written 2026-09-17 by the Cowork session**, per `CLAUDE.md` §9.1a (a reported result is a claim,
not evidence). The 0c bundle is **not modified by this document** — its `SHA256SUMS.txt` attestation
stands as Devin delivered it. This file records what a second read of the same CSVs found.

**Bundle:** `data/captures/2026-09-17-oa-combo-semantics/` — **17/17 SHA256SUMS verified** by direct
`device_bash` read. Every figure below is computed from those files, not from the report.

---

## 1. ⛔ FINDING — the combined export is NOT a census. One row is silently dropped.

> ### ⛔ CORRECTED 2026-09-17, same session — two errors in this section's original framing.
> **(a)** The original read *"the '249/497' filenames are line counts."* **False.** The filenames
> carry the TRUE row counts; `wc -l` is what undercounts, because the CSVs have no trailing newline.
> Devin's naming was right and this document's first pass was wrong.
> **(b)** The original said Devin *"gives the count as 8 without reconciling it against the 9
> available."* **False.** His full 0c report identifies the `Nov 3, 2025` drop explicitly, names it
> in all three runs, and answers Task 3 as *"combined positions export is a RESULT, not a census —
> CONFIRMED."* **He found this; this pass confirmed it independently.** The original text of both
> claims is struck here rather than deleted.

**True row counts** (`csv.DictReader` — `wc -l` undercounts each file by one, no trailing newline):

| file | rows | A | B |
|---|--:|--:|--:|
| `standalone-primary-249.csv` | 249 | — | — |
| `standalone-overlay-249.csv` | 249 | — | — |
| `combined-control-497.csv` (no rules, default caps) | **497** | 249 | **248** |
| `combined-open-257.csv` | 257 | 249 | 8 |
| `combined-notopen-489.csv` | 489 | 249 | 240 |
| `combined-cap-day1-249.csv` | 249 | 249 | 0 |
| `combined-cap-pos1-489.csv` | 489 | 249 | 240 |

249 + 249 = **498**. The unconstrained control returns **497**.

**The missing row is `2025-11-03`, and it is absent from EVERY combined run — including the control
that carries no rule at all.**

| | Opened | Closed | Status | P/L |
|---|---|---|---|--:|
| primary (standalone) | Nov 3, 2025 9:35am | Nov 3, 2025 4:00pm | `expired` | **−48** |
| overlay (standalone) | Nov 3, 2025 3:00pm | Nov 3, 2025 3:01pm | `profits` | **+5** |
| control combined | 9:35am row present (`A`) | — | — | overlay row **ABSENT** |

**It is not a cap effect.** Only two positions exist that day and the control's default caps are
`2 per day` / `2 positions`. Two does not exceed two. **It is not a rule effect** — the control
carries `"rules":[]`. No error is rendered and no `Filtered Trades` entry accounts for it.

⚠️ **The bias direction is the bad one.** The dropped row is an **overlay winner (+5) on a day the
primary lost (−48) and was still open at 15:00** — precisely a hedge-fire day. **n=1, so this is not
yet evidence of a systematic bias**, and it must not be reported as one. But the single instance
lands on the exact day-type the whole program exists to measure, and the mechanism is unknown.

**Consequence, and it is cheap to adopt:** every combine run in Phase 1 is reconciled against
standalone exports of its constituent tests, row for row, before any ranking is computed. A combined
export is a **result**, not a census, until this is explained.

## 2. ✅ Answer 1 (CONCURRENT) stands — with a corrected denominator

The primary closed **before 15:00 on 240 of 249 days** and at/after 15:00 on **9**.

Under `is open`, the overlay traded on **8** days — and all 8 are late-close days. **Zero false
positives.** The verdict is correct: `open` evaluates **concurrent presence at the gated test's
entry moment**, not same-day.

📝 **It is 8 of 9, not 8 of 8** — the ninth late-close day is `2025-11-03`, the dropped row from §1.
**Devin's report reconciles this correctly**; this pass confirms it from the same CSVs independently.
The partition is exact: run (b) and run (c) are disjoint, neither admits a day from the other's
partition, and their union equals the control's B set.

`is open` (8) + `is not open` (240) = **248**, against 249 overlay days. The mirror is exact **once
the dropped row is accounted for**, and inexact if it is not.

## 3. ✅ Answer 4 (caps) confirmed independently

- `posLimitDay=1` → **249 rows, A only.** Every overlay row gated out; the 15:00 open is always the
  day's second.
- `posLimit=1` → **489 = A 249 + B 240**, and the B-day set is **identical** to the `is not open`
  rule run. A concurrent-position cap and the `not open` predicate evaluate live presence the same
  way — genuine independent corroboration of §2, and Devin was right to flag it.
- Defaults scale exactly N (2→2/2, 4→4/4, 7→7/7), both pickers editable `1…10`.

**The cross-pass-comparability concern is confirmed.** A 7-way combine defaults to `7/day + 7
concurrent`, a 2-way to `2/2`. Combined results are not comparable across pass sizes under default
caps. Caps must be pinned explicitly in `crules` or test count held fixed.

## 4. ⭐ What this says about the presence gate for the REAL fleet — read before the arm respec

In this test the primary closed before 15:00 on **96% of days** — *by construction*, because the
test spec called for a tight profit target precisely to create early closes. **That is a property of
the test, not of the fleet.**

The fleet's actual primary is a 0DTE condor carried into the 14:00–15:30 window
(`hedge-design-spec` §2.3). It is open at hedge time **essentially always**. Therefore:

- A presence gate on the real structure filters **only days the primary never entered** — real, but
  small.
- **H-B-with-gate ≈ H-B-without-gate** for the fleet's actual structure. They are unlikely to be
  worth two arms.
- This does not weaken `R-2026-09-17-COMBO-RULES-PRESENCE-ONLY`; it right-sizes what the gate buys,
  and it may **save an arm** in a grid where the UI path makes arm count the budget.

## 5. ⛔ The trap that matters most operationally — malformed `crules` fails SILENTLY

From Devin's Task 2, and it is the most dangerous thing in the whole bundle:

- A **malformed rule** or **invalid JSON** in `crules` does not error. The page **silently falls
  back to the unruled control** and renders 497 — a plausible, complete-looking result.
- The drawer's form state is **SPA-sticky**: it can display a rule the URL does not carry. The
  combine toggle also persists across bare navigations.

**Together these produce "wrong data returned as valid."** An operator can look at the drawer, see
the intended rule rendered, read the combined numbers, and be reading **control data** — with no
error anywhere on the screen. A URL-driven sweep is exactly the workflow that walks into this.

**Rule for Phase 1, non-negotiable:** verify what actually ran from the **URL and the row count**,
never from the drawer. A combined run whose row count equals the unruled control's is presumed
**unruled** until its URL is re-read. This belongs in the `oa-driving` skill.

## 5b. 📌 Incident worth noting — a script overwrote a verified, committed bundle

Devin reports `/tmp/oa_shots.mjs` re-ran its built-in sequence and overwrote **8 PNGs inside the
already-verified `data/captures/2026-09-16-oa-backtester/` bundle**, repaired via `git restore` and
re-verified 13/13.

⭐ **It was recoverable only because that bundle was committed** (`bc8d726`, earlier the same day).
An uncommitted bundle overwritten this way is gone, and its `SHA256SUMS.txt` would have been
silently wrong rather than obviously wrong. This is the concrete argument for the commit-early
cadence in `CLAUDE.md` §9.1, and it should be cited the next time committing feels like overhead.

## 6. What is NOT in question

Hashes (17/17), the CONCURRENT direction, the cap findings, the URL-addressability of `crules`, and
Devin's boundary discipline. The bundle is good work. §1 is a reconciliation gap in the write-up and
an unexplained platform behaviour — not a capture failure.
