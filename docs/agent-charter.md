# Agent Charter

**Signed:** Andy — 2026-08-17  ·  **Amended by:** signature only  ·  **Version:** 2

*Signed at v2 with two amendments made at signature: §3's flagged sub-classes are ruled into Class C,
and §4 gains the guard-change line. Rulings `R-2026-08-17-CHARTER-SIGN` and
`R-2026-08-17-CHARTER-IRREVERSIBLES` in `docs/RULINGS.md`.*

This file is the single answer to *who may do what*. It carries no figures and no dates.
Status cells point at sources; they never quote numbers.

**It supersedes, on signature:**

- the ownership table in Devin's 2026-08-12 deep review §4
- the twelve-row ownership table in the `bot-fleet-build-map` artifact — which becomes **generated
  output of this file**, not a parallel statement of it
- the *ownership implications* of `AI Agent Stack.md` §6

§6 **remains authoritative** for job descriptions, triggers, inputs, outputs and escalation rules.
This file governs permission only. Where the two disagree on permission, this file wins.

---

## 1. The rule

**Gate by reversibility, not by identity.**

Anything reversible and observable is open to every agent with no approval step. Anything that
cannot be undone by another commit needs either a verification step or a human signature — and
which one depends on *why* it can't be undone.

Identity-based restrictions ("only Andy may write", "Devin may not merge") are **removed**. They
were costing throughput without protecting anything, because the things that actually need
protection aren't protected by who holds the keyboard.

---

## 2. Class A — Open. No approval, no gate, no batch.

Any agent — Cowork, Devin, subagents — may do these directly and merge them:

- Parsers, loaders, engines, tests, fixtures, migrations, CI, schedulers — **except any change to a
  guard, detector predicate or refusal contract, which is Class C (§4)**
- Any doc edit, including specs, `CLAUDE.md`, and the pre-registration ledger's **non-evidence**
  fields (typos, wording, structure, cross-references, archive moves)
- **Applying a signed ruling everywhere it lands.** Once Andy signs, propagation is mechanical and
  requires no second approval from anyone. An unapplied signed ruling is a defect, not a queue.
- Roster/classification data, tracker items, status files, the todo CSV
- Reading anything, anywhere, including OA
- **Merging any PR whose CI is green** — the check is the gate, not a person's attention

No gated batch is required for Class A. Gated batches are retired except for Class C.

## 3. Class B — Open, but a write is not done until it is read back.

**Option Alpha account writes: toggles, parameter changes, bot builds, automation edits.**

Agents write to OA **without asking and without waiting.** There is no approval step.

The one requirement is verification, and it exists because of recorded failures on this exact
surface, not as a control: OA reference clicks can no-op, titles commit only on blur, and cached
`innerText` has produced silent double-writes. CI cannot see any of this — git gates nothing here,
and no other system will tell you the edit missed.

**Definition of done for any OA write:**

1. Hard reload, then read the value back from the reloaded DOM — never from pre-write state
2. Record the observed value and a config hash
3. If the read-back disagrees with intent: **stop, do not retry blind**, and say so

An unverified write is not a faster write. It is an account in an unknown state, which is the
condition that ended v1.

**RULED AT SIGNATURE, 2026-08-17 — these two are Class C, not Class B.** The only OA actions another
write cannot reverse are **(a) deleting a bot or automation** and **(b) increasing capital
allocation.** Both require Andy's signature; they are listed in §4. **Allocation *decreases* remain
Class B** — cutting size is the safety direction and does not wait on a signature.
Ruling `R-2026-08-17-CHARTER-IRREVERSIBLES`.

## 4. Class C — Signed. The short list.

Only these need Andy's signature, and the reason is comparability, not safety:

- The **fixed panel** — change one and every banked day becomes uncomparable
- **Pre-registrations**: creating, amending, or retiring an arm
- **Kill criteria and thresholds**, including any change to what counts as evidence
- **Go-live and sizing**
- **Force-push or history rewrite** — the record's value is that it is verifiable back to Day-0
- **Irreversible OA actions**: deleting a bot or automation, and **increasing** capital allocation.
  Allocation decreases stay Class B. *(Ruled at signature 2026-08-17 — see §3.)*
- **Any change to a guard, detector predicate, or refusal contract** — in any file, including files
  that are otherwise Class A (`scripts/build_ledger.py`, `scripts/execution_audit.py`, CI checks).
  It must be **named as a guard change in the PR description** and pre-authorized by Andy.
  Plausible correctness is not authorization: three unilateral guard changes on 2026-08-17 were each
  plausibly correct. *(Ruled at signature 2026-08-17.)*

Everything not on this list is Class A or B. If something is unclear, it is Class A.

---

## 5. Routing — who picks up a piece of work

One test: **can you write the pass/fail before the work starts?**

| | Goes to |
|---|---|
| Yes — deterministic acceptance | **Devin.** Parsers, loaders, CI, migrations, schedulers, fixtures, sweeps |
| No, but the output is a judgment needing an audit trail | **Cowork.** Decision cards, propagation sweeps, OA driving, drafting rulings |
| High-volume mechanical work with a schema | **Sonnet subagents.** Extractions, classifications, blind second opinions |
| No, and it changes what the system may do | **Andy.** Class C only |

If the deliverable is a **PR**, Devin. If the deliverable is an **answer**, a subagent.
Disputes resolve toward Class A: pick it up and do it.

---

## 6. Working rules — mechanical, not permissions

- Work on a branch and open a PR **because that's how CI runs**, not as a control. Merge it
  yourself when green.
- **Start of session: fetch, and state divergence in one line** before analysis. This is the only
  defence against two writers holding different pictures, and it costs one line.
- **Every PR carries a trailer**: files read, files changed, rulings relied on, anything refused
  and why, suites run and their exit codes. Sessions read trailers instead of the session log.
  *(Open: Devin has been asked for a better mechanism. Replace if he has one.)*
- No agent invents a Class C change and calls it Class A. Surface it and keep moving on
  something else.

---

## 7. Roster status

Roles per `AI Agent Stack.md` §6. Status points at its source; no figures here.

| Role | Class | Owner | State | Blocked by |
|---|---|---|---|---|
| Orchestrator | A | Cowork | Live; hub — dispatches at start, applies ruled changes at end | — |
| OA-Reader | B | Devin | Not built | OA reactivation |
| Pipeline-Runner | A | Devin | Exists; no trigger, no heartbeat | — |
| Execution-Auditor | A | Devin | Exists; rules skip for want of the mechanics schema | mechanics contract |
| Statistician | A | Devin | Exists; unwired. Layer 2 correctly `BLOCKED` | see G-1′ — not a gap |
| Researcher | A | Cowork frames · Devin runs | Script is draft; defects on record | do not wire in |
| Lesson-Extractor | A | Cowork proposes · Devin builds queue | Daily path per §6; queue not built | lessons archive ruling |
| Surface-Explorer | A | Cowork | Ad hoc. Seed material: `AI Agent Stack.md` §9 | — |
| Propagator | A | Devin builds · any agent runs | Not built as a check | — |
| Reconciler | A | Cowork | **Signed 2026-08-17** (`R-2026-08-17-RECONCILER`) — read-only; writes nowhere but `docs/reconciler/`; weekday 07:30 ET. Contract: `docs/reconciler/README.md` | — |

---

## 8. Enforcement — honest about which is which

| Rule | How it's enforced |
|---|---|
| Green CI before merge | **Mechanical** — branch protection, required check |
| No force-push to master | **Mechanical** |
| Class C needs a signature | **Honor system.** No CI can detect intent. Deliberate. |
| Guard changes named in the PR | **Honor system + the PR description.** A guard change merged without being named is a charter violation on its face, reviewable after the fact in the diff |
| Repo admin held by Andy alone | **Mechanical** — no agent token carries admin; `--admin` merge bypasses are retired (`R-2026-08-17-REPO-ADMIN`) |
| OA write verification | **Honor system + the artifact.** A write with no recorded read-back is invalid on its face |
| Routing | **Honor system.** It's a tiebreaker, not a wall |

CODEOWNERS is retained for **notification only** — it must not block a merge.

---

## 9. Amendment

Anyone may propose an amendment as a PR against this file. Andy signs. Version bumps.
If this charter is ever the thing slowing work down, that is a defect in the charter.
