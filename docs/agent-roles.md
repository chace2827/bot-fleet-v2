# Agent Roles — reading page

A printable description of every role in the fleet, in the order information actually moves.

**This is a reading view, not an authority.** `AI Agent Stack.md` §6 remains authoritative for job
descriptions, triggers, inputs, outputs and escalation rules — if this page and §6 disagree, §6
wins. `agent-charter.md` remains authoritative for permission. Status lines here name their source
and carry no figures, so this page cannot drift out of sync with the ledger.

**Two corrections from §6 that the earlier build-map artifact got wrong**, now applied here:
Lesson-Extractor runs **on** the daily path (§6: *"Daily after grading/audit"*), not off it; and the
Orchestrator is the **hub** that dispatches at the start and applies ruled changes at the end — it
is not a single middle step in a chain.

**One deliberate deviation from §6.** §6 fires the Propagator from a hook on a signed ruling. We
implement it as a CI check instead — vendor-neutral, and it survives changing agents. Noted so the
difference is a choice on record rather than a misreading.

---

## The shape

```
        ┌─────────────────── ORCHESTRATOR (hub) ───────────────────┐
        │  dispatches ↓                              applies ↑     │
        │                                                          │
        └→ OA-Reader → Pipeline-Runner → Execution-Auditor ─┐       │
                                       └ Statistician ──────┤       │
                                          Lesson-Extractor ─┤       │
                                                            ↓       │
                                                    gated queue     │
                                                            ↓       │
                                                          ANDY      │
                                                            ↓       │
                                                       Propagator ──┘

   off the daily path, feeding only the queue:  Researcher · Surface-Explorer
   read-only, no writes at all:                 Reconciler (proposed)
```

---

# The daily path

## Orchestrator
*Cowork. Class A — open.*

**Job.** Hold the plan and the canonical rulings, dispatch the other agents, and apply only changes
that have been ruled.

**Runs.** Daily, pre-open and post-close.

**Reads.** The canonical rulings file, `STATUS.md`, the prior day's briefs.
**Uses.** Its own tooling, memory, and task dispatch to the others.
**Produces.** The daily plan, a dispatch log, and the commits that apply ruled changes.

**Escalates rather than decides.** Any state change lacking a signed ruling. Any threshold breach.

**Today.** Live. It is the hub, so it appears twice in one lap — once dispatching, once applying.
No scheduler yet, so it runs when a person opens a session.

---

## OA-Reader
*Devin builds. Class B — writes are open, but a write is not done until it is read back.*

**Job.** Read bot logs, per-decision detail, and positions out of the Option Alpha browser into a
declared schema.

**Runs.** Post-close daily, plus on demand.

**Reads.** The bot list and the active-bot watchlist (count per the current `/bots` capture, not
stated here).
**Uses.** Browser automation with screenshot and trace capture.
**Produces.** Raw capture CSV, per-decision JSON, screenshots.

**Escalates rather than decides.** Any read it cannot verify against a second source is marked
**unverified** and is never recorded as first-hand.

**Today.** Not built — this step is done by hand. Blocked on OA reactivation. Its justification is
config drift: there is no automated path from the account to the repo, which is the defect that
ended v1. It is *not* the unblocker for the statistical layer — see Statistician.

---

## Pipeline-Runner
*Devin builds. Class A.*

**Job.** Execute the eight-stage `daily.sh` and halt on config-blind stages.

**Runs.** Daily, after OA-Reader.

**Reads.** The raw export, config, the ledger.
**Uses.** Bash and the Python scripts.
**Produces.** Ledger, audit output, compliance scores, the HTML dashboard.

**Escalates rather than decides.** A missing grader column or a skipped audit rule means it emits
*"no inference licensed"* and halts scoring rather than guessing.

**Today.** The code exists and exits non-zero correctly. What it lacks is a trigger and a heartbeat
— so a run that never happened is currently indistinguishable from a run with nothing to report.

---

## Execution-Auditor
*Devin builds the loader only — the rule bodies stay frozen. Class A.*

**Job.** Compare executed-versus-should-have per bot and flag discrepancies.

**Runs.** Daily, after the pipeline.

**Reads.** The ledger, bot rules, OA captures.
**Uses.** Python comparators, frozen at a sha on purpose.
**Produces.** A discrepancy report, as gated proposals.

**Escalates rather than decides.** Any proposed rule change is gated and never applied by the
auditor itself.

**Today.** Running but half-blind: several rules skip for want of the mechanics schema. The blocker
is a signature, not code. **Why it must stay deterministic:** frozen means the same input yields the
same finding forever, which is what makes a finding evidence rather than an opinion.

---

## Statistician
*Devin wires it. Class A to run; Class C to change what it measures.*

**Job.** Run paired bootstrap CIs, sign tests and stratified permutation max-T — and grade only
above threshold.

**Runs.** Weekly, or when n crosses its threshold.

**Reads.** The ledger and the pre-registration ledger.
**Uses.** Python statistics in a sandbox.
**Produces.** A grading report with confidence intervals, or *"no inference licensed."*

**Escalates rather than decides.** Grading a pair below n≥100. Any post-hoc variant → refuse.

**Today.** Validated code, not wired into the daily loop. Its Layer 2 reports `BLOCKED` — **this is
correct output, not a gap.** Exit attribution needs a mechanic label that the platform does not
expose anywhere; G-1′ was declined on that basis and the ruling stands. Do not re-propose building
the input. **No language model belongs anywhere near this** — a model cannot perform the resampling
and would narrate a result instead, and the whole value of this layer is its willingness to say no.

---

## Lesson-Extractor
*Cowork proposes; Devin builds the queue. Class A.*

**Job.** Convert each run's outcomes into candidate durable lessons.

**Runs.** Daily, after grading and audit. **On the critical path**, per §6.

**Reads.** Briefs, audit output, grading, and human rulings.
**Uses.** Reasoning plus memory.
**Produces.** Candidate lessons, gated, each with evidence links.

**Escalates rather than decides.** Promoting a lesson to a rule. That is a human ruling, always.

**Today.** The index script exists; the gated queue does not. Blocked on the lessons-archive
ruling — pre-cutover rows still sit inside the post-cutover boundary, and nothing should write
lessons next to them.

---

## Propagator
*Devin builds; any agent may run it. Class A.*

**Job.** After a ruling, update every affected document — and fail if any stays stale.

**Runs.** On a signed ruling. (§6 says hook-triggered; we implement a CI check — see the deviation
note above.)

**Reads.** The ruling ID and the doc corpus.
**Uses.** Grep, Python, git.
**Produces.** A propagation diff and a verification report.

**Escalates rather than decides.** Ambiguous ruling scope.

**Today.** Not built as a check. `check_refs.py` is the seed. Under the charter, **applying a signed
ruling needs no second approval from anyone** — an unapplied signed ruling is a defect, not a queue.
Extend it to assert that no narrative document states a figure the CSVs contradict, and figure drift
becomes a red build instead of somebody's discovery.

---

# Off the daily path — feeding only the gated queue

## Researcher
*Cowork frames the questions; Devin runs the batches. Class A to explore; Class C to pre-register.*

**Job.** Propose new bots and arms, and pre-test them in the OA backtester and Option Omega before
pre-registration.

**Runs.** Weekly.

**Reads.** Docs, backtest results, regime coverage.
**Uses.** Web, the OA backtester, Option Omega, market data.
**Produces.** Pre-registered proposals, gated.

**Escalates rather than decides.** Any live bot on/off toggle. Any un-pre-registered grading.

**Today.** The counterfactual engine is a signed spec with a draft implementation carrying known
fatal defects — **do not wire it in.** The agentic part is the framing layer above it; the
counterfactual arithmetic underneath must stay deterministic code. Best pattern for the weekly
batch: two independent runs of the same question, blind to each other, and a third agent reporting
only where they disagree.

---

## Surface-Explorer
*Cowork. Class A.*

**Job.** Map unused Option Alpha features and propose gated adoptions.

**Runs.** Monthly.

**Reads.** The OA documentation and feature list.
**Uses.** Web fetch and the OA browser.
**Produces.** Feature-adoption proposals, gated.

**Escalates rather than decides.** Any actual config change.

**Today.** Ad hoc — it happens when someone opens a tab. Seed material already exists in
`AI Agent Stack.md` §9 UNEXPLORED PLATFORM SURFACE, and `oa-platform-reference.md` records what the
platform affirmatively cannot express. Lowest priority of the roster; nothing downstream waits on it.

---

# Read-only

## Reconciler — proposed tenth role, unsigned
*Cowork. Class A. Writes nothing, ever.*

**Job.** Read the last day's PRs, the ledger, and the rulings, and report **only** contradictions
between them.

**Runs.** Daily, after the others.

**Produces.** A contradiction list. No analysis, no proposals, no commits.

**Why it should exist.** Several agents now hold several partial pictures of the same repo. The fix
is not fewer agents — it is one designated reconciliation point with no write access. Needed from
the day a second writer starts merging.

---

## How work gets routed

One test: **can you write the pass/fail before the work starts?**

- **Yes** → Devin. Parsers, loaders, CI, migrations, schedulers, fixtures, sweeps.
- **No, but the output is a judgment needing an audit trail** → Cowork. Decision cards, propagation
  sweeps, OA driving, drafting rulings.
- **High-volume mechanical work with a schema** → Sonnet subagents. Extractions, classifications,
  blind second opinions. Never adversarial verification — a cheaper model accepts plausible claims,
  which is the opposite of what a skeptic is for.
- **No, and it changes what the fleet may do** → Andy. Class C only.

If the deliverable is a **PR**, Devin. If it is an **answer**, a subagent.

## The five things that still need a signature

Fixed panel · pre-registrations · kill criteria and thresholds · go-live and sizing · force-push.
Everything else is open. If a case is unclear, it is open.

---

*Sources: `AI Agent Stack.md` §6 and its handoff topology; `agent-charter.md` for class and
permission; `CLAUDE.md` §5 for the OA automation amendment. Deviations from §6 are named at the top
of this page.*
