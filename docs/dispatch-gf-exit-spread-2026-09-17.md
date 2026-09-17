# Dispatch — GF exit-mechanic spread test (`R-2026-09-17-GF-EXIT-SPREAD-TEST`)

**Purpose:** measure the greenfield family's **real** exit-mechanic spread before anything is
concluded about the family. Phase 1 Stage 1 ran three of the seven arms; this adds the other four.
**Seven arms is exactly the Compare ceiling** — the whole family fits one pass.

⛔ **This test measures a SPREAD. It does not rank arms.** See §"What the answer looks like".

---

## 📐 The threshold, corrected — the test is 3× more sensitive than first stated

The Cowork session first quoted a **±0.076 R** floor. **That was the UNPAIRED figure and it is the
wrong instrument here.** Exit variants on the same primary are *identical on every day no exit
fires*, so the paired difference carries far less variance. Measured from the Stage-1 CSVs:

| paired vs S1-0 (Ride) | days the arms differ | sd of paired diff | mean diff | t | MDE |
|---|--:|--:|--:|--:|--:|
| S1-a SL100 | 66 of 353 (18.7%) | 0.1998 | −0.0044 | −0.41 | **0.0298 R** |
| S1-b SL200 | 26 of 353 (7.4%) | 0.1249 | +0.0015 | +0.22 | **0.0186 R** |

**Pooled paired sd ≈ 0.1624 → MDE at n=353 is 0.0242 R**, not 0.076.

Two consequences:
1. **The threshold for this test is ±0.0242 R paired**, and `R-2026-09-17-GF-EXIT-SPREAD-TEST`'s
   "±0.076" should be read as superseded by this tighter, correctly-paired figure.
2. ⭐ **What Stage 1 already established is stronger than "cannot distinguish."** Both stop arms are
   measurably **within ~0.03 R of ride**, with t-statistics of −0.41 and +0.22. That is
   *demonstrated practical equivalence*, not an absence of evidence. And exit ranking is **not**
   unachievable in principle — paired, 0.03 R needs ~230 positions (~3 years live), not 73 years.

## The seven arms

Three exist from Stage 1 and are **reused, not rebuilt**: `S1-0` (Ride), `S1-a` (SL100),
`S1-b` (SL200). Four are new. Exit mechanic is the **only** variable; every other field is S1-0's.

| arm | mechanic | field | value | source |
|---|---|---|---|---|
| Ride | *nothing* | — | — | existing `S1-0` |
| SL100 | Stop Loss % | `stoploss` | `1` (= 100% of credit) | existing `S1-a` |
| SL200 | Stop Loss % | `stoploss` | `2` (= 200% of credit) | existing `S1-b` |
| **PT50** | Profit Taking % | `profits` | **`0.5`** | spec §, C1/C3 discharged |
| **Trail** | Trailing Stop | `tstop` | **armed trail: `target` = 40, `trail` = 15** | ⭐ C2 ruling 2026-08-06 |
| **Touch0** | Touch | `touch` | **`$0`** | spec § |
| **Canary** | Profit Taking % | `profits` | **`0.05`** | spec § |

⚠️ **Trail is the armed trail, not a plain trail.** `R`-check C2 (2026-08-06) established `tstop`
opens a sub-form with `target` ("Activate at __ % of credit") and `trail` ("Close on __ % pullback"),
and PR-16 was re-scoped to the **armed** trail at `target`=40 / `trail`=15. Building a plain trail
would be a different arm wearing the name.

---

## The prompt (paste below the line)

---

You are working in the `bot-fleet-v2` repo, connected as a local folder. Fresh session — assume no
context from prior work.

**Read, in order:** `CLAUDE.md` (§4, §9.1a) · `.agents/skills/option-alpha/SKILL.md` (the law) ·
`.agents/skills/oa-drive/SKILL.md` · `docs/dispatch-gf-exit-spread-2026-09-17.md` (this file — the
threshold section above is the point of the exercise) · `docs/phase1-stage1-verification-2026-09-17.md`
(§1's amendment box and §5b are the traps and the standard of proof).

**Rulings that govern:** `R-2026-09-17-GF-EXIT-SPREAD-TEST` · `R-2026-09-17-PHASE1-EVIDENCE-PROCEDURE`
· `R-2026-09-17-HEDGE-PROGRAM-DISPOSITION`.

### ⛔ BOUNDARY

0. **YOU DO NOT LOG IN.** Andy authenticates Chrome by hand first. If a `/login` URL or sign-in form
   appears, **STOP and report.** Never request, enter, store or read credentials.
1. **NO LIVE-FLEET EDITS.** Bot, automation, scanner, position and account-settings surfaces are
   read-only. ⛔ **NO `Create Bot`, on any surface, ever.**
   ✅ Backtest **runs are authorized** for arms you create under `ZZ-AGENT-<YYYY-MM-DD>-GF-<arm>`.
   ⛔ **Do not modify, rename or delete the existing `ZZ-AGENT-2026-09-17-P1-*` tests** — three of
   them are inputs to this comparison.
2. **NO WIRE PROTOCOL.** DOM/JS reads are in scope; no API calls, replay, network panel, recorder.
3. Scope every capture to `app.optionalpha.com` at capture time.

### ⛔ THE TRAPS (all three bit earlier runs)

1. **Malformed `crules` silently falls back to the unruled control**, and the drawer is SPA-sticky —
   it can show a rule the URL does not carry. **Verify from the URL and the row count, never the
   drawer.**
2. **Combined exports are RESULTS, not censuses** — 21 rows vanished in Stage 1 with caps permitting
   and no error. **Reconcile row-for-row against standalones before any ranking.** *(This test is
   Compare-only, so it should not bite — but reconcile anyway if you combine anything.)*
3. **Caps default to exactly N and change results.** Pin them if you combine.

Two driving facts: **`Copy CSV` does not write the clipboard under CDP** — use
`Browser.setDownloadBehavior` + `Download CSV`. Several delegated `data-click` handlers **ignore
trusted `Input.dispatchMouseEvent` but respond to a JS `.click()`**.

### TASK — build four arms, then measure the spread across seven

**Start by duplicating `ZZ-AGENT-2026-09-17-P1-S1-0`** (Add Variation) for each new arm, so every
non-exit field is inherited rather than retyped. Change **one** thing per arm:

| new arm | set |
|---|---|
| `…-GF-PT50` | Profit Taking % = **50%** (`profits` = `0.5`) |
| `…-GF-Trail` | Trailing Stop — **armed**: `target` = **40** (activate at 40% of credit), `trail` = **15** (close on 15% pullback) |
| `…-GF-Touch0` | Touch = **$0** |
| `…-GF-Canary` | Profit Taking % = **5%** (`profits` = `0.05`) |

⚠️ **Trail must be the ARMED trail** (`target` + `trail` sub-form). A plain always-on trail is a
different mechanic and is not this arm.

**Verify before running each:** serialize the form and confirm **exactly one** field differs from
S1-0 besides the name. Paste that diff into the raw capture. An arm that differs in two fields is
not an arm — stop and report it.

Run all four. Export the **standalone positions CSV** for each (Download CSV path).

### ⛔ WHAT THE ANSWER LOOKS LIKE — read this before you analyse

**The question is: how wide is the spread, and is it inside or outside ±0.0242 R paired?**

Compute, for each of the six non-Ride arms, the **PAIRED** difference against Ride, matched by
expiration date:

- mean paired diff in R, its sd, SE, t, and 95% CI
- the number of days the arm differs from Ride at all (the non-zero days)
- the max−min spread of **mean paired diff** across all six

⛔ **Do NOT rank the arms and do NOT name a winner.** With seven arms there are 21 pairwise
comparisons and some will look significant by chance. Report the **spread** and each arm's paired CI
against Ride. If an arm's CI excludes zero, say so plainly and state its width — that is a finding.
If none do, that is also a finding and it is the more likely one.

Report Exp(R) unpaired per arm as well, for the record, **with the unit labelled** — per condor,
ex-artifact — but the paired numbers are the answer.

⛔ **Do not write a recommendation, and do not conclude anything about the GF family's future.**
These are T4 backtest figures. The family's disposition is Andy's ruling on your spread, not your
verdict.

### DELIVERABLE

`data/captures/<YYYY-MM-DD>-gf-exit-spread/` — the Stage-1 bundle shape: raw capture (`01-…`,
including the one-field-diff verification for all four new arms), derived analysis (`02-…`, naming
its raw source **and sha256**), **every CSV raw**, `screenshots/` per arm config and results,
`README.md` (purpose · timestamp with TZ offset · file/sha256/what table · the paired table · the
spread · `## Assumptions` · `## Questions for Andy` · `## Docs-vs-render deltas`), `SHA256SUMS.txt`.

### PROHIBITIONS

No git. Nothing outside the bundle directory **except** `docs/session-log.md`, which you **may and
should** append a close-out entry to (`CLAUDE.md` §9.1 — the Stage-1 dispatch wrongly forbade this).
No `Create Bot`. Do not touch the `P1-*` tests. Never run a script that re-executes a prior capture
sequence — one overwrote 8 verified PNGs on 2026-09-17.

**Stop conditions:** 401/403/429 · unrecognized response shape · UI numbers disagreeing · `/login` ·
terms or payment prompt · **anything indicating a live (non-PAPER) account.**

### REPORT

The paired table (six arms vs Ride: mean diff, sd, SE, t, 95% CI, non-zero days), the **spread**,
the unpaired Exp(R) per arm with units, the bundle path, and **the refusals**.

**Stop after the measurement. Conclude nothing about the family.**
