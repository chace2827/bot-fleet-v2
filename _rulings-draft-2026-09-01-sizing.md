# RULING DRAFTS — fleet sizing policy — 2026-09-01 — ⬜ UNSIGNED, ALL SIX

Status: **DRAFT. Nothing signed, nothing applied, no OA edit made, no repo-tracked file changed.**
Analysis and derivations: `_sizing-policy-draft-2026-09-01.md`.
GF-family instance: `_rulings-draft-2026-09-01-gf-sizing.md` (sign both or neither — R-1 and
R-2 are the same decision at two grains).
Cap proposal these rulings depend on: `_roe-cap-proposal-2026-09-01.md`.

**How to sign:** write `SIGNED — Andy — <date>` under each ruling. Where a ruling offers options,
circle one. An unsigned ruling gates the OA execution session
(`_sizing-policy-draft-2026-09-01.md` §6, PRECONDITION 1).

⛔ **R-1 and R-6 are a package.** Do not sign R-1 (size up 26×) without R-6 (the caps). Sizing up
with G4's `$` half still an unfilled `<FILL>` is the one combination this project's evidence law
forbids.

---

## R-2026-09-01-SIZING-LADDER — the fleet ladder: size at entry, not on graduation

**Supersedes in principle** the ladder at `docs/pre-registration-ledger.md` L82-83
(`SIZING TIER  1 lot (experiment) | ≈$5K risk/position (CANDIDATE+). Set once, never ad hoc.`).
The "set once, never ad hoc" half is **unchanged and reaffirmed**. What changes is *when* the
tier is set.

**Decision.** A bot is sized, from its first position, at the tier its results are intended to be
read at — not at 1 lot until it graduates.

**Reason, in writing, per gate G6** (`pre-registration-ledger.md` L137, *"sizing declared once per
phase, with the reason in writing — not by preference"*): **R is size-free; fills are not.**
`STATUS.md`'s own allocation-realism table flags twelve ON bots *"1-lot — fill-untested"* with the
note *"their edge won't survive the slippage of a real order size."* If that is true, a 1-lot arm
run to n=100 yields a statistic about an instrument nobody will trade. Size-on-graduation
therefore certifies the wrong number. The old ladder was self-blocking: it deferred size until the
evidence justified it, using evidence that by its own admission cannot justify it.

**The ladder.**

| Class | Who | Risk per position |
|---|---|--:|
| A — read at live scale | `live-candidate`; `experiment` whose result informs live capital | ≈$5K |
| B — control | a `control` paired to a class-A arm | ≈$5K, identical to its arm |
| C — instrument (ops-class) | `instrument` role, §2a | 1 lot, permanently |
| D — mirror-watch | `mirror-watch` | unchanged, never resized |
| E — negative-CI | any bot whose Exp(R) 95% CI lies entirely below 0 | frozen at current size |
| F — OFF / archived | AUTOS OFF | no change while OFF |

Class E is new. The old ladder had no brake; without E, "size at entry" would size up a bot the
readiness board already shows losing.

**Epoch rule, unchanged in force and restated:** a sizing change opens an **epoch boundary**. Raw
P/L is not poolable across it. **R, sample counts and gate progress are unaffected** — the
readiness board is size-free by construction. Recorded per bot in `data/bots_meta.csv`.

SIGNED — Andy — ......................

---

## R-2026-09-01-GF-INTERIM-CLAUSE — amend the GF "1 lot until interim (n=60)" clause

**What stands today.** `pre-registration-ledger.md` PR-14…PR-23:
`MAX LOSS  1 lot per arm until one clears its interim read; then ≈$5K risk/position.` ·
`SIZING TIER  1 lot — IDENTICAL across all arms.` Signed 2026-08-09, re-signed 2026-08-17.
Current progress: **n = 4 clean condors per arm** (`STATUS.md` readiness board). n=60 is distant.

**CIRCLE ONE.**

**OPTION 1 — AMEND NOW (recommended).** The seven ACTIVE arms move to **≈$5K risk/position**,
identically, in one sitting. `GF-QQQ-IC-Ride-Delta` is **excluded** (AUTOS OFF since 2026-08-31).
`GF-QQQ-IC-Canary` is handled by R-2b.
*Cost:* family single-day tail **$1,302 → $33,852** (×26).
*Buys:* fill realism on the whole family from today, and direct size-comparability with
`QQQ-IC-0DTE-Fortress-NoPT50`, which already runs **26 ct** on the same underlying.
*Conditional on R-6.*

**OPTION 2 — HOLD.** The signed clause stands; arms stay 1 lot to the interim read. Nothing
changes, no new tail, and the stated intent is deferred.

**OPTION 3 — RETIRE FIRST.** Reduce the arm count, then size the survivors. The tail is linear in
arm count; 7 × $5K is expensive *because there are 7 arms*. This is a separate decision and is not
drafted here.

SIGNED — Andy — ......................        OPTION: ......

### R-2b — Canary exception (sub-ruling; only if Option 1)
PR-20 is `IC · control (instrument)`, `MECHANISM n/a — not run for edge`, `SAMPLE TARGET n/a —
daily fill/no-fill is the output`, `MAX LOSS 1 lot, smallest expressible risk`, `KILL CRITERION
NONE ON P/L`. Its output is a **fill/no-fill signal, which is size-invariant** — 26 ct buys no
detection power and adds ~$4,825 of daily tail to a bot whose P/L is stipulated meaningless.
It is not an arm of the exit-policy A/B, so holding it at 1 ct does not make the A/B unreadable.

**CIRCLE ONE:**  ☐ **Canary stays at 1 ct (recommended)**  ☐ Canary moves with the family
⚠️ If "stays at 1 ct": the **shared scanner cannot be the lever for Canary** — one shared edit hits
all eight. Resolution route must be chosen before execution; see
`_rulings-draft-2026-09-01-gf-sizing.md` §G-3.

SIGNED — Andy — ......................        CHOICE: ......

---

## R-2026-09-01-SLEEVE-CAPS — re-rule the daily aggregate sleeve caps

**Why this ruling is mandatory and not optional.** `pre-registration-ledger.md` carries signed
lines `Daily aggregate ≤ $10K across the SPX IC sleeve` (PR-01, PR-02) and `≤ $10K across the QQQ
IC sleeve`. Under R-2 Option 1 the QQQ sleeve becomes **$40,000/day** — 4× its signed cap. An
amendment that leaves those lines standing puts two signed documents in contradiction.

⚠️ **Finding that stands regardless of any sizing decision: the SPX IC sleeve is over its signed
cap today.** Three ON arms at ~$4,900/position each = **$14,700** against a **$10,000** signed cap
(`IC-SPX-FastPT25-S2` $4,900, `-130PM` $4,750 med/$4,900 max, `IC-SPX-Fortress-Unstopped` $4,900 —
all derived from `data/trades.csv`). This is a live breach of a signed line and it **predates this
session**. It is disclosed here rather than fixed quietly.

**Decision — the re-ruled caps** (all at $5K risk/position, per `CLAUDE.md` §4 larger-side rule):

| Sleeve | Cap | Derivation |
|---|--:|---|
| SPX IC | **$15,000/day** | 3 ON arms × $5K — makes the roster as it stands legal rather than silently breached |
| QQQ IC | **$40,000/day** | 8 ON arms × $5K (7 GF + NoPT50) |
| Directional | **$5,000/day** | a ceiling, not a target; both arms stay 1 lot per R-1 class E |
| OA-Mirror | **$12,000/day** | current concurrent open risk ~$10.3K, rounded up; never resized |
| **FLEET** | **$72,000/day authorized risk-at-work** | sum |

This is *authorized exposure*, not a loss estimate. The loss brake is R-6.

SIGNED — Andy — ......................

---

## R-2026-09-01-MIRRORS-NO-RESIZE — mirrors are not resized, and the 3DTE exception

**Decision, part 1 — the default, stated explicitly as requested.** **No OA-Mirror bot is resized
by this or any sizing ruling.** `pre-registration-ledger.md` carries `SIZING TIER  Unchanged from
current. Do not resize a watch-only bot.` on seven mirror entries plus the §5 shared frame. The
reason is measurement, not caution: the funding bar (§5, L530-536) scores *"max single-trade loss
≤20% of intended live allocation"* and *"no single loss >1.5× the source's largest disclosed
loss"* — **both denominated against the source's size.** Resize the mirror and both criteria stop
meaning what they were written to mean, and `data/mirror_baseline.csv` — the one place pre-cutover
figures are admissible — stops being comparable to what follows it.

**Decision, part 2 — the exception, already applied.** On 2026-08-31 `3DTE $140-$350` had its
**allocation** raised $5,000 → $10,000 (`data/captures/2026-08-31-roster/10-authorized-edits-2026-08-31.md`
Edit 2, verified `a5.bots.bot.seed === 10000` after hard reload). The same capture disclosed the
consequence: the bot's Bot Input **POSITION SIZE is "26% of net liquid", not a fixed dollar
figure**, so the change **doubles the dollar size of every future position**. It therefore crossed
the do-not-resize line in effect, though not in the field edited.

**CIRCLE ONE.**

☐ **REVERT to $5,000 (recommended).** The bot's own `MAX LOSS` line reads *"Paper allocation $5K,
deliberately small — one bad position is 20%+ of it."* The $5K figure is load-bearing inside its
funding criterion, not incidental. Its one open position (opened 08-27, risk $965) is unaffected
either way.

☐ **RATIFY at $10,000**, and amend PR-07's `MAX LOSS` and `SIZING TIER` lines by dated banner,
recording that the 20%-of-allocation criterion is re-based to $10K and that its post-08-31
positions are a **new sizing epoch** not poolable with what came before.

SIGNED — Andy — ......................        CHOICE: ......

---

## R-2026-09-01-GROUP-HYGIENE — three group findings

Cross-tab of OA bot groups (`data/captures/2026-08-31-roster/07-…tsv`) against `FAMILY_RULES`
(`scripts/roster.py` L38-53), all 44 bots. **The two schemes are orthogonal by design and that is
correct** — groups encode lifecycle/attention, families encode strategy lineage.

**A · fix.** All three `-ARCHIVED-` clones sit outside the `Archive` group:
`IC-SPX-FastPT25-S2-ARCHIVED-2026-08-07` in **`IC-Focus`**;
`IC-SPX-FastPT25-S2-130PM-ARCHIVED-2026-08-08` and
`QQQ-IC-0DTE-Fortress-NoPT50-ARCHIVED-2026-08-08` in **`Monitor`**. All are AUTOS OFF.
`IC-Focus` is defined in `STATUS.md` as *"the bots you're actively perfecting"* — an archived clone
in it inflates the Focus roster. **Proposed: move all three to `Archive`.**

**B · rename.** `IC` is the only group named for a **pillar** rather than a lifecycle stage, and it
contains exactly the 8 GF arms and nothing else — it reads as "the IC pillar" (13 bots) but means
"the greenfield family". **Proposed: rename `IC` → `GF-Family`.**

**C · no action.** `Lab` is empty (0 bots), consistent with `pre-registration-ledger.md` §6a
(*"No specific bot is named or entered here yet"*). Leave it.

**Tag scheme — one proposal, deliberately minimal.** §8 item 1 already fixes the scheme:
*"`PR-NN`, two digits, ledger entry order, OA Tag = the bare ID."* **Proposed: verify and complete
the `PR-NN` tag on every bot carrying a pre-registration entry — and nothing else.** That tag is
the only label that joins the OA surface to the ledger by key rather than by name-match, and
name-matching is what breaks on rename or clone. Groups already carry lifecycle; `FAMILY_RULES`
already carries lineage; a third axis would need a third thing kept in sync.
⚠️ Whether `PR-NN` tags exist in OA today is **not readable from any local surface** — a read-only
OA pass, not asserted here.

SIGNED — Andy — ......................   (A ☐ · B ☐ · tags ☐ — tick what you authorize)

---

## R-2026-09-01-G4-ROE-CAP — fill the G4 dollar blank ⛔ PACKAGE WITH R-1/R-2

**Decision.** Fill the `<FILL>` at `docs/evidence-standards.md` L277 / `scripts/report.py` L1022
with **three levels**, each derived in `_roe-cap-proposal-2026-09-01.md` §1.5:

| | Cap | Value | Anchor |
|---|---|--:|---|
| 1 | per-bot cumulative drawdown (per epoch) | **$15,000** | v1 champion's worst cumulative DD at this exact tier, **−$14,540**, 221 positions |
| 2 | fleet cumulative drawdown | **$35,000** | the GF family's own structural single-day maximum at the new tier, 7 × $5K |
| 3 | **single-day fleet loss halt** | **$8,000** | the worst single day this program has had at this tier, **−$8,050** (2026-06-11) |

Three, not one, because each covers the others' blind spot: per-bot misses correlated loss —
and correlation is **proven, not assumed** (2026-08-26: **all 8 GF arms lost the same day**);
fleet-drawdown misses a single catastrophic session; the daily halt misses slow bleed.

**Breach actions** are drafted at `_roe-cap-proposal-2026-09-01.md` §2.5 and signed with this
ruling.

**Two things this signature does NOT do, stated so they are not assumed:**
1. It does not create a brake. Nothing in `scripts/report.py` computes these; the caps are
   **human-checked at the daily brief** until the Claude Code lane implements them. A criterion
   the loop does not produce is, by §2 rule 2, *not a criterion*. **Signing creates a code task.**
2. It does not re-score anything today. Against Cap 1, no ON bot is anywhere near the limit, so
   G4-`$` passes for every bot on day one and no stage changes.

**Carried limit:** every post-cutover figure behind these caps is **T5** (n = 16 trading days) —
far below the n≥100 / 6-month / regime-change bar. The v1 anchors are larger-sample but
pre-cutover and are cited **as history only**. Re-derive at n≥100.
**Not derived, and not invented:** a percentage-of-live-capital form. The only capital figures on
any surface are OA paper allocations, which are not capital. State a live figure and all three
convert in one pass.

SIGNED — Andy — ......................
