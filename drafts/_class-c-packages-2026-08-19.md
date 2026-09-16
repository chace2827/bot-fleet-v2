# Class C packages — 2026-08-19 triage

**Pin: `c48327546b99f89dc372e3728bce6954ed3a5323`** (#57, 2026-08-19 00:57 UTC), fetched fresh from
origin into a scratch clone. Every premise below was reproduced by running the command shown against
that clone. **Nothing here is applied.** Class C = changes what a guard accepts or rejects, so it is
Andy's ruling (dispatch §2, agent-charter §4).

Six defects. **Three of them live in one function** (`scripts/ci/validate_all.py`), and all three are
green today.

> ## ⏰ READ THIS ONE FIRST — it has a date attached and nothing else here does
> **`check_heartbeat` is holiday-blind. Labor Day is Monday 2026-09-07 — 19 days out. The Tuesday
> 2026-09-08 run goes RED on a correct pipeline.** Full entry at the end of this file. Every other
> defect below is green-and-stable and will wait for a ruling; this one fires on the calendar
> whether or not anyone has ruled on it.

---

## C-1 — `validate_all.py` positional `zip` hides a deleted suite  ⚠️ sharpest

**Premise, verbatim — `scripts/ci/validate_all.py:55`:**
```python
for exp, act in zip(expected.splitlines(), actual.splitlines()):
```
There is no length check anywhere in the file. `grep -nE "len\(|count|!=|set\(" scripts/ci/validate_all.py`
returns only line 57's `if exp != act`. `SUITES` is a hardcoded list at `:24`, iterated at `:40`;
`actual` is built only from suites that ran.

**The failure it permits.** `zip` truncates to the shorter sequence, so a suite that stops emitting a
line is compared against nothing. **Deleting one string from `SUITES` makes the gate green on a suite
that no longer runs** — no `MOVED` line, no error, rc=0.

**It is position-dependent, and the position favors the defect.** Replaying `:54-68` verbatim against
the real baseline:

| deletion | result |
|---|---|
| control, all 4 suites | PASS rc=0 |
| **minus `comparative_machinery` (last)** | **PASS rc=0 — silent** |
| minus `research_loop` (middle) | FAIL rc=1 |
| **minus the last three** | **PASS rc=0 — silent** |

A middle deletion is caught only *by accident*: the remaining lines shift and mismatch. A **tail**
deletion is invisible by construction. `comparative_machinery` is both the last entry and the only
suite recorded as failing — the most plausible thing for someone to delete is exactly the silent case.

**Reading A — fix.** Compare by suite name, not line position: an expected suite with no actual line
is a FAIL, an unexpected extra line is a FAIL. *Changes:* the gate gains two failure modes it cannot
currently express. Any PR that removes a suite starts failing until the baseline is updated in the
same PR — which is the stated intent at `:11`, "update `validate_baseline.txt` in the same PR".

**Reading B — leave, with rationale.** `SUITES` edits are visible in PR review and CODEOWNERS covers
`scripts/ci/`. *Changes:* nothing. Accepts that the gate's coverage is asserted by review rather than
by the gate. Note this is the roster-invariant shape from the 08-18 fleet — a guard bound to one
deletable token — and that review did not catch the same shape last time.

---

## C-2 — the baseline can bless a failing suite

**Premise, verbatim — `scripts/ci/validate_baseline.txt:4`:**
```
comparative_machinery exit=1 35/36
```
`validate_all.py:54-66` fails only on **movement**. Run at the pin: all four lines `ok`,
`PASS: all suites match baseline`, rc=0.

**The failure it permits.** A suite exits non-zero forever and the gate stays green, because red *is*
the pinned expectation. The gate answers "did anything move", never "is anything failing".

**Not a bug on its own** — a movement-detector is a legitimate design, and it is what caught the stale
`trade_id` defect. It is listed because it compounds C-1 and C-3: the one suite whose failure is
blessed is also the one whose deletion is silent.

**Reading A — fix.** Require an explicit, dated waiver token per blessed failure
(`comparative_machinery exit=1 35/36 WAIVED-UNTIL=<date> REASON=<ruling>`) and fail when a waiver
expires. *Changes:* blessed failures acquire an expiry; the gate gains a clock.

**Reading B — leave, with rationale.** The baseline file is short, tracked, and read in review.
*Changes:* nothing. Accepts indefinite green on a known-red suite.

---

## C-3 — a real assertion failure inside the blessed suite

**Premise, verbatim — `python3 scripts/ci/validate_all.py` at the pin:**
```
  FAIL  R-1 ledger_start sentinel (2099-01-01) refuses the run (exit non-zero) (did not raise)
  35/36 passed   engine 0.1.0-DRAFT sha cfaff1abc287d39c
```

**The failure it permits.** `R-1` asserts that a sentinel `ledger_start` of 2099-01-01 refuses the
run. It **did not raise**. That is the 36th assertion, and it is the one failing — permanently green
via C-2. Whatever R-1 protects is unprotected, and the gate reports `PASS`.

**Note the engine:** `comparative_machinery` is still `0.1.0-DRAFT` (sha `cfaff1abc287d39c`), whereas
`research_loop` has moved to `0.2.0-DRAFT`.

**Reading A — fix.** Diagnose R-1: either the sentinel path no longer reaches the refusal, or the
assertion is testing the wrong thing. *Changes:* depends on the diagnosis — if the refusal is genuinely
absent, this is a ledger guard defect, not a test defect, and it is upstream of C-2.

**Reading B — leave, with rationale.** 35/36 has been the pinned state since the baseline was written.
*Changes:* nothing. **Not recommended without at least a diagnosis** — this is the only entry here
where the green may be hiding a live guard gap rather than a reporting gap.

---

## C-4 — CI runs `check_refs` without `--strict`; 30 dangling refs are green

**Premise, verbatim — `.github/workflows/ci.yml:225`:**
```yaml
        run: python3 scripts/check_refs.py
```
**`scripts/check_refs.py:358`:**
```python
    if args.strict and dangling:
        failed = True
```

Measured at the pin, same tree, same moment:

| invocation | rc |
|---|---|
| `check_refs.py` (as CI runs it) | **0** — `check_refs: invariants clean` |
| `check_refs.py --all` | 0 |
| `check_refs.py --strict` | **1** |
| `check_refs.py --all --strict` | **1** |

**The failure it permits.** `check_refs: 30 DANGLING REFERENCE(S)` on master with a green build. The
word "clean" is printed while 30 references dangle, because "invariants" and "dangling" are separate
verdicts sharing one exit code.

**Reading A — fix.** Add `--strict` to `ci.yml:225`. *Changes:* the build goes red immediately — 30
references must be resolved or exempted first, several of which are C-5 and C-6 below. This is a
sequencing decision, not a one-line edit.

**Reading B — leave, with rationale.** Dangling refs in narrative docs are not build-breaking, and
strictness would block unrelated PRs. *Changes:* nothing. Accepts that `check_refs` is advisory in CI
and that the count can grow unobserved. If chosen, the honest follow-up is to stop describing it as a
guard.

---

## C-5 — `check_refs` flags its own selftest literal (scanner self-flag)

**Premise, verbatim — `scripts/check_refs.py:263`:**
```python
                errors = check_row_count_invariant(["docs/fixture.md"], actual)
```
Output at the pin: `scripts/check_refs.py:263  ->  docs/fixture.md`.

**Carried queue item, re-checked as instructed. Still reproduces at `c483275`.** `check_refs.py` did
change upstream (last at `02ee43c`, #34) — the self-flag survived because the change was elsewhere.

**The failure it permits.** Noise, not risk: one of the 30 is the scanner reporting itself. It matters
only because it inflates the count that C-4 turns on.

**Reading A — fix.** Exempt the scanner's own selftest fixtures. *Changes:* the dangling set shrinks by
one; no predicate changes for any other file.

**Reading B — leave, with rationale.** Zero risk, and any exemption mechanism is a hole that could be
widened later — the "never widen a guard to unblock" rule. *Changes:* nothing.

---

## C-6 — `run_receipt.py:11` false-DANGLING: prose parsed as a path

**Premise, verbatim — `scripts/run_receipt.py:11`:**
```python
    "There are none for August. data/receipts/ stops at mirror-baseline.txt,
```
Output at the pin: `scripts/run_receipt.py:11  ->  data/receipts/ stops at mirror-baseline.txt`.

**Known-reproducing per the dispatch; confirmed at `c483275`.** The scanner extracted an English
sentence — "`data/receipts/` stops at mirror-baseline.txt" — as a filesystem path, because it begins
with a real directory prefix.

**The failure it permits.** A false positive that trains the reader to skim the dangling list. Same
inflation problem as C-5, and the same interaction with C-4.

**Reading A — fix.** Require a path-shaped token (no spaces before the extension) before reporting.
*Changes:* the reference detector's accept/reject predicate — genuinely Class C. Narrows what counts
as a reference everywhere, which could mask a real dangling ref written unusually.

**Reading B — leave, with rationale.** One known false positive is cheaper than a detector change that
could silently drop true positives. *Changes:* nothing.

---

## ⏰ Time-sensitive — `check_heartbeat` is holiday-blind

Not a Class C ruling so much as a dated warning: **this one fires on its own schedule.**

**Premise, verbatim — `scripts/check_heartbeat.py:19-23`:**
```python
    """Previous calendar day that is not a weekend (US markets)."""
    d = datetime.date.fromisoformat(day)
    d -= datetime.timedelta(days=1)
    while d.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        d -= datetime.timedelta(days=1)
```
`grep -nE "holiday|nyse|calendar|business" scripts/check_heartbeat.py` returns only the docstring on
:19. There is no holiday calendar.

**The failure it permits.** After any NYSE holiday, `previous_trading_day` returns the holiday itself
and the check demands a heartbeat for a day the market was closed — **RED on a correct pipeline.** It
is a false alarm, not a missed defect, which is why it is a warning rather than a risk. But a guard
that cries wolf on a known schedule is a guard that gets ignored.

`check_heartbeat.py` last changed at `1ccad01` (#38) — the FLEET_ROOT change, which did not touch this.
**Next NYSE holiday: Labor Day, Monday 2026-09-07.** The first run on Tuesday 2026-09-08 goes red.

**Reading A — fix.** A holiday list, or accept any of the last N weekdays. *Changes:* the staleness
predicate — a wrong list silently widens the window and hides a genuinely stale heartbeat.

**Reading B — leave, with rationale.** Known, understood, ~9 false alarms a year, each obvious in
context. *Changes:* nothing. If chosen, note it in the runbook so the September red is not re-diagnosed
from scratch.

---

## Not in this file

**`roles-and-ingredients.md:39`** — `research_loop 62/62` where `validate_baseline.txt:3` records
`66/66`. **Class A**, banked for the fix batch, not applied. The engine sha moved
(`302bef72778a1a35` → `3125be15810076fd`) and the count moved with it, so the three *other* sites
(`state.md:533`, `state.md:1222`, `session-log.md:5534`) are **stale-with-their-sha and correct as
history — they must not be edited.** No guard reads `roles-and-ingredients.md`, so the edit touches no
predicate.

Row 13's "the gate exists and is green" was examined and is **true** — the gate returns 0 (C-2). Not a
falsification.
