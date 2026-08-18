# Converting a Solo Options-Research Operation into a Durable, Gated Multi-Agent Workflow

## 0. ASSUMPTIONS

- **Anthropic ecosystem is the default model tier.** You already run "one long Claude session per day," so Claude models and the Claude Code / Claude Agent SDK toolchain are assumed available and preferred. If you were locked to a non-Anthropic model, the recommended architecture's specifics (hooks, skills, memory tool) would change, though the shape would not.
- **Paper-trading-only through at least February 2026 holds.** The "no live capital" window means the cost of an agent error is currently a corrupted document or a wrong proposal, not lost money. This lets Phases 0–2 move faster. **If live capital arrives sooner than expected, the gating and audit requirements harden and the migration must slow down** — this is the single assumption that most changes the plan if wrong.
- **Option Alpha has no programmatic read/data API.** Confirmed below; the agent must drive the browser for reads. If Option Alpha shipped a read API mid-project, the browser-automation agent could be retired and reliability would jump.
- **You will personally implement and maintain this.** No platform team. Anything requiring dedicated ops (a Temporal cluster, a Kubernetes deployment) is scored down heavily.
- **The existing local repo (git, ~22 scripts, 9-stage `daily.sh`, ~50 markdown docs) is sound and stays authoritative.** The conversion wraps it, not replaces it.
- **"Measurably better over time" means decision quality and audit completeness, not P&L.** With an n=3 live ledger and paper capital, profit is not yet a legitimate signal. Improvement metrics target propagation defects, ungraded-bot rate, context re-derivation errors, and compliance-audit coverage.
- **Costs are estimated from published vendor rates as of mid-2026 and labeled where uncertain.** Token-cost math assumes Sonnet-class pricing and prompt caching.

---

## 1. EXECUTIVE SUMMARY

**Recommended architecture: a single persistent orchestrator (Claude Code / Claude Agent SDK) that spawns ephemeral, read-only subagents, with all state changes gated behind deterministic hooks and a git-tracked ruling ledger — keeping your existing `daily.sh` pipeline intact underneath.** This is the "one writer, many readers" pattern that both sides of the 2025 multi-agent debate actually agree on. In Anthropic's June 13, 2025 write-up "How we built our multi-agent research system," a lead-plus-subagent design (Claude Opus 4 lead, Claude Sonnet 4 subagents) "outperformed single-agent Claude Opus 4 by 90.2%" on their internal research eval — but at roughly 15× the tokens of a chat, with token usage alone explaining about 80% of the performance variance. Cognition's "Don't Build Multi-Agents" (Walden Yan, June 12, 2025) argues the opposite for coding, its Principle 2 being that "actions carry implicit decisions, and conflicting decisions carry bad results"; his April 22, 2026 follow-up sharpens the reconciliation — the setups that work are those "where multiple agents contribute intelligence to a task while writes stay single-threaded." Your problem is overwhelmingly a *reading and auditing* problem with a *single human writer*, which is precisely the case where this hybrid wins and where a fan-out-of-writers design would fail.

The one reason it wins: **it removes context exhaustion and serialization (your top two pain points) without violating the governance model, because gating and audit become deterministic hooks — code that runs regardless of what the model "decides" — rather than prompt instructions the model can drift past.** A `PreToolUse` hook can mechanically block any write to a bot or any state mutation and route it to a "gated" queue; a `PostToolUse` hook logs every read and conclusion to an append-only audit trail. Sample-size gates and the "no inference licensed" rule become Python assertions in those hooks, not polite requests in a system prompt.

**Estimated cost: roughly $150–300/month** at ~40 model-runs per trading day on Sonnet-class pricing ($3 input / $15 output per million tokens), assuming ~3M input tokens/day at ~75% prompt-cache hit and ~300K output tokens/day. This can fall toward $100–150 if the interactive orchestrator runs under a Claude Max subscription rather than metered API. Infrastructure is otherwise your existing MacBook plus launchd; a small VPS ($5–20/month) is optional for unattended scheduling. Browser automation adds $0 if self-hosted (Playwright) or ~$40–100/month if you use a managed browser (Browserbase).

Do **not** adopt Temporal, a LangGraph rewrite, or an n8n/Windmill low-code canvas as the primary spine. Each is individually excellent and each is the wrong tool for a solo, judgment-heavy, gate-everything operation right now.

---

## 2. DIAGNOSIS

Eight bottlenecks, each mapped to the specific capability that removes it.

1. **Context exhaustion — the session re-derives state and sometimes contradicts prior rulings.** *Removed by:* externalizing state out of the context window. Anthropic's blog "Managing context on the Claude Developer Platform" (Sept 2025) reports that combining the memory tool with context editing "improved performance by 39% over baseline," context editing alone delivered 29%, and in a 100-turn web-search evaluation context editing reduced token consumption by 84%. The memory tool (`memory_20250818`) is now GA on the Messages API (no beta header); context editing remains beta under header `context-management-2025-06-27`. Combined with a git-tracked "canonical rulings" file the orchestrator reads first, the session stops re-deriving and stops contradicting.
2. **Everything serialized in one session.** *Removed by:* read-only subagents with isolated context windows running in parallel — browser reads, pipeline execution, and statistical analysis no longer compete for one context window or one wall clock. This is exactly the workload (breadth-first, independent reads) where Anthropic found multi-agent parallelism paid off.
3. **Rulings fail to propagate across ~50 docs.** *Removed by:* a dedicated propagation subagent plus a deterministic post-ruling hook that greps every doc for the ruling ID and fails the run if any doc is stale. This converts propagation from "the model remembered to" into "the build breaks if it didn't."
4. **Pipeline stages run config-blind; audit rules silently skip; bots go ungraded.** *Removed by:* a schema-validated config and a hook that refuses to score if a required column is missing, emitting "no inference licensed" instead of silently skipping. This is a data-contract problem, not an AI problem — the fix is a validator, and the agent's role is to surface the gap, not paper over it.
5. **Reading Option Alpha through a browser is slow and brittle (stale text, no-op clicks, blur-commit fields).** *Partially removed by:* a DOM-first browser layer (Playwright, or Stagehand for the parts that keep moving) run as an isolated tool with retries and screenshot/trace capture, so failures are reproducible. **Not fully removable** — see below.
6. **Large parts of Option Alpha never explored.** *Removed by:* a scheduled "surface exploration" research subagent that reads the platform docs and proposes (gated) uses of the backtester, scanners, 0DTE Oracle, Exit Options, and cloning.
7. **Trade ledger only recently live; sample tiny (n=3).** *Not removable by any architecture.* No orchestration produces statistical power. The system can only enforce that inference stays gated until n≥30 fleet-wide / n≥100 per bot-variant pair, and accelerate evidence collection via Option Alpha's own backtester and third-party options history.

**Bottlenecks a multi-agent system will NOT fix, stated plainly:** (a) the tiny sample — more agents cannot manufacture trades; (b) the fundamental brittleness of reading a web app with no API — automation reduces but does not eliminate it; (c) any flaw in your statistical pre-registration or thresholds — agents will faithfully execute a bad rubric; (d) reward-hacking and drift in the learning loop, which require deliberate countermeasures (Section 7), not more agents.

---

## 3. LANDSCAPE MAP

| Tool | Category | What it uniquely provides | Maturity | Verdict | One-line reason |
|---|---|---|---|---|---|
| Claude Agent SDK / Claude Code | Agent runtime | Subagents, skills, hooks (deterministic lifecycle control), bundled CLI; same harness Anthropic runs internally | GA; SDK renamed from Claude Code SDK Sept 29, 2025 | **Adopt** | Hooks give mechanical gating/audit for free; matches your existing workflow |
| Anthropic memory tool + context editing | Context mgmt | Client-side file memory + server-side tool-result clearing; 84% token savings reported | Memory GA on Messages API; context editing beta | **Adopt** | Directly kills context exhaustion, your #1 pain |
| Prompt caching | Cost/context | Cached input at ~10% of fresh price | GA | **Adopt** | Makes a large, reused context corpus affordable daily |
| LangGraph | Orchestration framework | Graph state machine, `interrupt()` for HITL, checkpointer persistence, time-travel | Mature; ~34.5M monthly downloads reported | **Trial** | Best fallback if you outgrow Claude-native; adds maintenance and framework churn |
| LangSmith | Observability/eval | Deep LangGraph tracing, 30+ eval templates | Mature | **Watch** | Only compelling if you adopt LangGraph |
| Temporal | Durable execution | Event-history replay, resume-exactly-where-failed, 7 SDKs | Very mature; $300M Series D at $5B, Feb 17 2026 | **Reject (now)** | Deterministic-workflow rules + cluster ops are too heavy for solo |
| Inngest | Durable execution | Serverless, event-driven, per-step retries, no cluster | Mature (TS-first) | **Watch** | Nice if you go event-driven later; TS ecosystem stronger than Python |
| Restate / DBOS / Hatchet | Durable execution | Journal-based exactly-once; DBOS is Postgres-native | Emerging | **Watch** | Lighter than Temporal; revisit at live-capital stage |
| Prefect / Dagster / Airflow | Data orchestration | Task caching, retries, schedules | Mature | **Reject (now)** | Your `daily.sh` + launchd already does this; adds ops |
| n8n | Low-code automation | 400+ integrations, visual canvas, approval nodes | Mature | **Reject (as spine)** | Breaks down on judgment-heavy audit; glue only |
| Windmill | Code-first workflow | Python/TS scripts as workflow steps, schedules, audit logs, self-host in minutes | Mature; 12,400+ GitHub stars May 2026 | **Trial (glue)** | The one low-code option that respects code; possible scheduler/UI layer |
| Zapier / Make | Low-code automation | SaaS glue | Mature | **Reject** | Per-task billing, no judgment, weak audit |
| Letta | Memory/agent runtime | LLM-managed memory hierarchy (MemGPT lineage) | Production (Bilt runs >1M agents) | **Watch** | Powerful but a whole runtime to adopt; overkill vs files |
| Mem0 | Memory layer | Bolt-on vector/graph memory; AWS Agent SDK provider; +26% accuracy in ECAI 2025 paper | Production; $24M raise Oct 28 2025 | **Watch** | Consider only if file memory proves insufficient |
| Zep / Graphiti | Memory (temporal graph) | Timestamped facts, state-change modeling | Cloud-only since 2025 (Graphiti OSS) | **Watch** | Temporal graph is elegant but SaaS lock-in |
| Braintrust | Eval-first observability | Trace-to-test pipeline, eval-as-first-class | Mature; $80M Series B | **Trial** | Best if "did it get better?" becomes the central question |
| Arize Phoenix | Observability (OSS) | OpenTelemetry-native, self-host, free | Mature | **Trial** | Free, OTel-standard telemetry sink |
| Weave (W&B) | Observability | Trace view + eval harness | Mature | **Watch** | Fine if already on W&B |
| promptfoo | Eval (local) | Config-driven prompt/agent tests, supports Claude Agent SDK provider | Mature | **Adopt (light)** | Cheap local regression tests for prompts/skills |
| OpenTelemetry GenAI conventions | Telemetry standard | Vendor-portable span schema | Emerging standard | **Adopt** | Make it a requirement so you're not locked in |
| Playwright | Browser automation | Deterministic DOM control, tracing, auto-wait | Industry standard | **Adopt** | The reliable core for reading Option Alpha |
| Stagehand | AI browser automation | `act`/`extract`/`observe` over Playwright, action caching | Growing (~8k stars Feb 2026) | **Trial** | For the OA screens that keep changing; caches to stay cheap |
| Browserbase | Managed browser | Hosted headless, session replay, stealth | Mature | **Watch** | Only if unattended cloud runs need it |
| Anthropic/OpenAI computer-use | Vision agents | Pixel-level control when DOM fails | Beta-ish; 12–17pt reliability gap vs DOM | **Watch** | Last-resort fallback; less reliable, more expensive |
| E2B / Modal / Daytona | Sandboxed execution | Isolated microVM/gVisor code execution | Mature; Modal $355M Series C May 2026 | **Trial** | Run agent-written analysis code safely off your laptop |
| Option Alpha webhooks | Platform surface | Inbound trigger of automations from external signals | GA (2024) | **Adopt** | Only programmatic surface OA exposes |
| Option Alpha backtester / 0DTE Oracle / Exit Options | Platform surface | 1-min historical backtests → instant bot; per-minute exit mgmt | GA | **Adopt** | Underused evidence-generation engine you already pay for |
| Option Omega | Backtesting | 1-min data back to 2013, modeling + automate tiers | Mature | **Trial** | Independent backtest to cross-check OA and pre-test new arms |
| ORATS / ThetaData / Polygon | Options data | Historical chains + greeks; ORATS hosted backtests; ThetaData cheap raw | Mature | **Watch** | For agents that pre-test proposed strategies against outside data |
| QuantConnect LEAN | Backtesting engine | Full research/backtest engine, ThetaData connector | Mature | **Watch** | Heavy; only if you outgrow OA + Option Omega |

---

## 4. RANKED ARCHITECTURES

Weights (sum = 1.0), reflecting your non-negotiables: **gating/audit 0.20, context 0.15, learning 0.15, solo maintenance 0.15, migration risk 0.15, parallelism 0.10, cost 0.10.** Scores 1–5 (5 best; for maintenance/migration, 5 = lowest burden/risk).

| Architecture | Gating/Audit (.20) | Context (.15) | Parallelism (.10) | Learning (.15) | Maint. (.15) | Migration (.15) | Cost (.10) | **Weighted** | Est. $/mo |
|---|---|---|---|---|---|---|---|---|---|
| **A. Hardened single session** | 4 | 2 | 1 | 3 | 5 | 5 | 5 | **3.65** | $80–150 |
| **B. Claude-native orchestrator + read-only subagents (RECOMMENDED)** | 5 | 4 | 4 | 4 | 4 | 5 | 4 | **4.35** | $150–300 |
| **C. LangGraph + LangSmith + Playwright** | 5 | 4 | 4 | 4 | 2 | 3 | 3 | **3.65** | $250–450 |
| **D. Durable-execution heavy (Temporal/Windmill + LangGraph + sandbox + Phoenix)** | 5 | 4 | 5 | 4 | 1 | 2 | 2 | **3.35** | $400–700 |
| **E. Low-code canvas (n8n/Windmill primary)** | 3 | 2 | 3 | 2 | 3 | 3 | 4 | **2.80** | $50–150 |

**A. Hardened single session.** Keep one Claude Code session per day, but add hooks (mechanical gating + audit logging), skills (reusable graded workflows), and the Anthropic memory tool so the session stops re-deriving context. Cheapest, lowest risk, delivers value in days. *Most likely failure mode:* it only half-fixes context exhaustion and does nothing for serialization — browser reads still block statistical work in one window, so on heavy days you still hit the wall. It is the correct **Phase 0**, not the destination.

**B. Claude-native orchestrator + read-only subagents (RECOMMENDED).** A persistent orchestrator holds the plan and the canonical rulings; it dispatches isolated, read-only subagents for (i) Option Alpha browser reads, (ii) pipeline execution/audit, (iii) statistical grading, (iv) strategy research, (v) ruling propagation. Subagents return compressed summaries; only the human, via a gated ruling, causes any state change. Hooks enforce gating, audit, and sample-size rules deterministically. Memory lives in git-tracked markdown plus the memory tool. *Most likely failure mode:* subagent sprawl and prompt drift — if you let subagents write to shared docs, you recreate the propagation defect. Mitigation: exactly one writer (the orchestrator, post-ruling), everyone else read-only.

**C. LangGraph + LangSmith + Playwright.** Model the daily job as an explicit graph; use `interrupt()` for human-in-the-loop gating (checkpointed, survives restarts) and LangSmith for node-by-node traces. Strong on auditability and durable pause/resume. *Most likely failure mode:* solo-maintenance drag — you now own graph code, a checkpointer store, LangSmith seats, and the framework's fast-moving API surface (v0.4 → per-node timeouts, DeltaChannel, typed streaming in 2026). For one person, this is a second job. It is the **right escalation** if you outgrow B, not the starting point.

**D. Durable-execution heavy.** Temporal (or Windmill) orchestrates; LangGraph runs agent steps; E2B/Modal sandboxes agent code; Arize Phoenix collects OTel traces. This is what a *team* would build for a mission-critical, live-capital fleet. *Most likely failure mode:* you spend your time operating infrastructure instead of doing research. Temporal's deterministic-workflow constraints alone (no `Date.now`, wrapped side effects, workflow versioning) are a real tax; multiple 2026 analyses (e.g., Diagrid) argue checkpoint-style frameworks "would need to fundamentally rearchitect" to match true durable execution — meaning you'd be gluing two hard systems together solo. Reserve for post-live-capital scale.

**E. Low-code canvas primary.** Drive everything from n8n or Windmill nodes. *Most likely failure mode:* judgment-heavy audit and statistical grading do not fit a node canvas; you end up embedding large code blocks anyway, losing the visual benefit while keeping the platform's limits. Windmill (code-first) is the least-bad of these and earns a role as an optional scheduler/dashboard, not the brain.

---

## 5. RECOMMENDATION AND DISSENT

**The pick: Architecture B**, reached in stages so that Architecture A is literally its Phase 0. Build on Claude Code / the Claude Agent SDK because your gating and audit non-negotiables map one-to-one onto **hooks** — deterministic scripts that fire on `PreToolUse`, `PostToolUse`, `Stop`, and `SubagentStop` and *cannot be talked out of it by the model*. A `PreToolUse` hook that pattern-matches any Option Alpha write action or any state-mutating file edit and returns "blocked → gated queue" is the mechanical embodiment of "nothing changes state without an explicit human ruling." That is worth more to you than any framework's feature list.

**The strongest honest case against the pick (written as a skeptic):**

> "You're betting your governance model on a single vendor's beta-grade primitives and on hooks that are only as good as the patterns you write. Three concrete problems. First, **Claude Code hooks and subagents are a moving target** — subagent spawning, memory tooling, and context editing all shipped or changed in 2025–2026, and betas get renamed and re-scoped; you're building compliance-critical controls on shifting sand. Second, **hooks are allow/deny scripts, not a durable state machine.** If a multi-hour run dies at stage 6, Claude Code has no event-history replay; you re-run and hope idempotency holds. LangGraph's checkpointer or Temporal's event history would let you resume at stage 6 with an auditable record of exactly what already happened — which is *precisely* the audit trail your requirements demand. You picked the option with the weakest durable-execution story. Third, **you're still scraping a browser with no API**; a 10-step Stagehand flow at 95% per-step reliability is ~60% end-to-end (0.95¹⁰), so your 'first-hand, verified' evidence discipline is undermined at the source, and no orchestrator fixes that. The honest call is LangGraph (C): explicit graph, real HITL interrupts, real checkpoints, real traces — the durability and reproducibility your own rules require."

**What in the first 60 days would prove the dissent right:**
- A run fails mid-pipeline and you cannot resume without re-doing earlier stages, **and** the audit log can't reconstruct what stage 6 had already done → you needed checkpointed durable execution.
- You write more than a handful of hook scripts and they start silently missing cases (a write slips through un-gated even once) → allow/deny scripting is insufficient; you need a state machine that makes the gate a required edge.
- Browser-read error rate stays high enough that you catch the agent recording stale/unverified values as "first-hand" → the evidence layer is the real bottleneck and orchestration choice is secondary.
- Anthropic changes or deprecates a beta you depend on (context editing header, memory tool schema) and it breaks a gating control → single-vendor beta risk is real.

**Why I still hold the pick:** every one of those is survivable at paper-trading stage, cheap to detect (the metrics in Section 7 catch them), and each has a defined escalation — the migration plan explicitly keeps LangGraph as the Phase-3 off-ramp. Paying LangGraph/Temporal's maintenance tax *before* you've hit their failure modes is the more expensive mistake for a solo operator. Critically, the gate itself does not depend on beta features: it can be a plain Python `PreToolUse` script plus a git-tracked ruling ledger, both of which survive any vendor change.

---

## 6. AGENT ROSTER

All agents are **read-and-propose only**. The human is the sole writer of rulings; the orchestrator is the sole applier of ruled changes.

| Name | Job (one sentence) | Trigger/Schedule | Inputs | Tools | Outputs | Must escalate (not decide) | Memory: reads / writes |
|---|---|---|---|---|---|---|---|
| **Orchestrator** | Hold the plan and canonical rulings; dispatch subagents; apply only human-ruled changes | Daily, launchd/cron (pre-open + post-close) | Canonical rulings file, STATUS.md, prior day's briefs | Claude Code, memory tool, task dispatch | Daily plan, dispatch log, applied-ruling commits | Any state change lacking a signed ruling; any threshold breach | Reads: rulings, memory index / Writes: plan, applied changes |
| **OA-Reader** | Read bot logs, per-decision detail, positions from the Option Alpha browser | Post-close daily; on-demand | Bot list, watchlist of ~17 active bots | Playwright (+ Stagehand fallback), screenshot/trace capture | Raw captures CSV, per-decision JSON, screenshots | Any read it cannot verify against a second source → mark "unverified," do not record as first-hand | Reads: last-seen state / Writes: captures, trace artifacts |
| **Pipeline-Runner** | Execute the 9-stage `daily.sh`; halt on config-blind stages | Daily after OA-Reader | Raw CSV export, config, ledger | Bash, Python scripts, sandbox (E2B/Modal optional) | Ledger, audit output, compliance scores, HTML dashboard | Missing grader column / audit-rule skip → emit "no inference licensed," halt scoring | Reads: config schema / Writes: pipeline logs |
| **Execution-Auditor** | Compare executed-vs-should-have per bot; flag discrepancies | Daily after pipeline | Ledger, bot rules, OA captures | Python comparators | Discrepancy report (gated proposals) | Any proposed rule change → gated, never applied | Reads: rulings / Writes: audit findings |
| **Statistician** | Run paired bootstrap CIs, sign tests, stratified permutation max-T; grade only above thresholds | Weekly or when n crosses threshold | Ledger, pre-registration ledger | Python stats (sandbox) | Grading report with CIs, or "no inference licensed" | Grading a pair below n≥100; any post-hoc variant → refuse | Reads: pre-registration / Writes: grading results |
| **Researcher** | Propose new bots/arms; pre-test in OA backtester & Option Omega before pre-registration | Weekly | Docs, backtest results, regime coverage | Web, OA backtester (browser), Option Omega, market data | Pre-registered proposals (gated) | Any live bot on/off toggle; any un-pre-registered grading | Reads: lessons, coverage / Writes: proposals |
| **Surface-Explorer** | Map unused Option Alpha features; propose (gated) adoptions | Monthly | OA docs (`docs.optionalpha.com`), feature list | Web fetch, OA browser | Feature-adoption proposals (gated) | Any actual config change | Reads: platform reference / Writes: exploration notes |
| **Lesson-Extractor** | Convert each run's outcomes into candidate durable lessons | Daily after grading/audit | Briefs, audit, grading, human rulings | Claude, memory tool | Candidate lessons (gated) with evidence links | Promoting a lesson to a rule (human ruling only) | Reads: prior lessons / Writes: candidate lessons |
| **Propagator** | After a ruling, update every affected doc; fail if any stays stale | On human ruling (hook-triggered) | Ruling ID, doc corpus | Grep/sed, Python, git | Propagation diff + verification report | Ambiguous ruling scope → escalate | Reads: ruling / Writes: propagation report |

**Handoff topology.** The **Orchestrator** is the hub. Each trading day: Orchestrator → dispatches **OA-Reader** (parallel per bot) → **Pipeline-Runner** → **Execution-Auditor** and (on schedule) **Statistician** run on the ledger → **Lesson-Extractor** compiles candidates. All findings return to the Orchestrator, which writes a single daily brief and a **gated proposals queue**. The **human** sits between the gated queue and any state change: you read proposals, sign rulings. A signed ruling fires a hook that invokes the **Propagator**, and only the Orchestrator applies the ruled change. **Researcher** and **Surface-Explorer** run off the daily critical path (weekly/monthly) and feed only the gated queue. No subagent writes to shared docs; no subagent can toggle a bot. This is the "many readers, one writer, human-in-the-graph" shape — Anthropic's parallel read subagents for breadth, Cognition's single-writer discipline for state.

---

## 7. LEARNING LOOP DESIGN

**What gets captured after each run:** a structured run record (not prose) — date, bots read, decisions audited, discrepancies found, sample sizes reached, gradings attempted vs licensed, proposals generated, rulings applied, and every subagent's inputs/outputs/traces. Structured state ("ungraded_bots: 4", "propagation_stale_docs: 0") is deliberately preferred over prose ("good progress") because numbers are harder to spin than adjectives.

**How outcomes are scored:** three families of metric, none of which the agent can directly optimize by talking:
- *Process integrity* (deterministic, from hooks): un-gated write attempts blocked, propagation-stale docs after a ruling, config-blind halts, unverified reads recorded as first-hand.
- *Evidence discipline*: ungraded-bot rate, count of gradings correctly refused below threshold, pre-registration compliance.
- *Decision quality*: audit discrepancy rate, human override rate on proposals (how often you reject a proposal — a proxy for proposal quality), and time-to-propagate a ruling.

**How a scored outcome becomes a durable change:** the Lesson-Extractor proposes; the human rules; a ruled lesson is written into the canonical rulings file and (if it changes agent behavior) into the relevant skill/prompt, then the Propagator updates all docs. **No lesson becomes a rule without a human ruling** — this is the same gate as everything else, which is what stops the loop from self-reinforcing bad "lessons." This is the "structured reflection + markdown files + human gate" pattern that published practitioners report works with nothing more exotic than files and a scheduled job.

**What prevents drift and reward-hacking** (this is where most self-improvement projects fail):
- *At least one metric the agent cannot optimize during its loop.* The human override rate and the deterministic process-integrity counters are computed outside the agent's reach. The reward-hacking literature is explicit (Salesforce's "Toward Self-Improving Agents"; multiple 2026 practitioner writeups): if the evaluator "measures the wrong target — say, cases closed rather than cases actually resolved" the agent learns to hedge or to avoid escalation because escalation hurts the visible score. Every self-improving deployment needs a metric the agent cannot touch.
- *Temporal decay of lessons.* Older reflections carry less weight; a February lesson should not override recent evidence. The paper "Agent Drift: Quantifying Behavioral Degradation" (arXiv:2601.04170) finds degradation emerging after a median ~73 interactions even without weight updates, so recency-weighting is mandatory, not optional.
- *Frozen base, verbal reinforcement only.* No weight updates. Lessons are text with evidence links. Shinn et al., "Reflexion" (NeurIPS 2023, arXiv:2303.11366), reports a 91% pass@1 on HumanEval versus GPT-4's 80% and an absolute +22% on AlfWorld decision-making tasks using verbal self-reflection — keeping the loop inspectable and reversible.
- *Defensive reflection.* The Statistician and Execution-Auditor treat their own conclusions as claims to verify against data, because reflection reusing the same base model can create a "closed loop" of self-confirming errors (trustworthy-agentic-AI survey, arXiv:2605.23989), and injected/poisoned lessons are a documented attack surface.

**Improvement metrics over time (targets, paper-trading stage):**
- *30 days:* propagation-stale-docs after a ruling → 0 (from the current recurring defect); ungraded-bot rate down; zero un-gated writes; context re-derivation contradictions eliminated (the memory/rulings file is authoritative).
- *90 days:* audit discrepancy rate trending down as lessons accumulate; human override rate on proposals declining (proposals getting better) *without* a rise in hedged/vague proposals (the anti-hack check); n≥30 fleet-wide reached so first licensed inferences appear.
- *180 days:* several bot-variant pairs crossing n≥100 with graded results carrying paired-bootstrap CIs; a documented, reproducible record for every graded conclusion; measurable coverage of previously unexplored Option Alpha features.

**Proven vs experimental, labeled:** structured reflection + external memory + human gating is *proven practice*. Automatic prompt/skill self-editing from outcomes is *experimental* — keep it human-gated and behind the same ruling wall until the metrics above show it helps rather than drifts.

---

## 8. PHASED MIGRATION PLAN

**Phase 0 — Harden the single session (delivers value in < 1 week).**
- *Entry:* today's repo and daily session.
- *Build:* (1) a `PreToolUse` hook that blocks any Option Alpha write and any state-mutating edit, routing to a `gated/` queue; (2) a `PostToolUse` hook that appends every read/conclusion to an append-only audit log; (3) a canonical `RULINGS.md` the session reads first; (4) enable the Anthropic memory tool + context editing so the session stops re-deriving; (5) a config-schema validator that halts config-blind scoring.
- *Stays manual:* all rulings, all browser reading, the daily pipeline invocation.
- *Exit:* one full trading day where no un-gated write occurred, the audit log is complete, and the session did not contradict a prior ruling.
- *Duration:* 3–5 days. *Rollback:* delete hooks; you are back to today's session with zero data loss (everything is git-tracked).

**Phase 1 — Extract read-only subagents (2–3 weeks).**
- *Entry:* Phase 0 exit met.
- *Build:* OA-Reader, Pipeline-Runner, Execution-Auditor, Lesson-Extractor as Claude Code subagents with isolated context; wire the Orchestrator to dispatch and collect; add promptfoo local regression tests for each subagent's prompt/skill; add OpenTelemetry spans.
- *Stays manual:* Statistician grading, Researcher proposals, all rulings.
- *Exit:* a full day runs with subagents in parallel, wall-clock down materially, audit trail reproducible, and a deliberate re-run produces the same conclusions.
- *Duration:* 2–3 weeks. *Rollback:* collapse subagents back into the single session (Phase 0 still works).

**Phase 2 — Statistics, propagation, and research (3–4 weeks).**
- *Entry:* Phase 1 stable for a week.
- *Build:* Statistician (paired bootstrap/sign/permutation, threshold-gated) running in an E2B/Modal sandbox; Propagator triggered by a ruling hook; Researcher + Surface-Explorer on weekly/monthly schedules using the OA backtester and Option Omega; optional Windmill or a tiny VPS for unattended scheduling and a dashboard.
- *Stays manual:* rulings; live-capital decisions.
- *Exit:* a ruling propagates to all docs automatically with a verification report; gradings correctly refuse below threshold and produce CIs above it; at least one gated new-bot proposal was pre-tested end-to-end.
- *Duration:* 3–4 weeks. *Rollback:* disable the newest agents; Phase 1 remains the working system.

**Phase 3 — Durability off-ramp (only if triggered).**
- *Entry:* one of the dissent's failure signals fires (mid-run resume impossible with audit gap; hooks miss a gate; scale grows past a single session).
- *Build:* wrap the daily job in LangGraph with a checkpointer and `interrupt()` for HITL gating, keeping subagents as nodes; add LangSmith or Braintrust for eval-driven traces; consider Inngest/Restate for step-level durability before ever reaching for Temporal.
- *Stays manual:* rulings.
- *Exit:* a stage-6 failure resumes at stage 6 with a complete audit record.
- *Duration:* 4–6 weeks. *Rollback:* the Claude-native Phase 2 system stays runnable in parallel; adopt LangGraph only for the daily spine, not memory or gating, so you can revert the spine alone.

---

## 9. UNEXPLORED PLATFORM SURFACE

Confirmed from Option Alpha's own docs (`docs.optionalpha.com`), with the owning agent:

- **Backtester (1-min historical, SPX/SPY/QQQ/IWM/XSP; instant "create bot from backtest").** Worth the most here: it generates evidence *without* waiting for paper trades to accumulate, directly attacking your n=3 problem. You can also compare/combine up to four backtests into one P/L curve. *Owner:* Researcher.
- **0DTE Oracle & Earnings Edge.** Purpose-built for your 0DTE/short-DTE credit spreads and for earnings-adjacent regimes; a math-based, backtested opportunity finder you're likely under-using. *Owner:* Researcher.
- **Exit Options & Monitor Automations (per-minute position management).** Directly relevant to your seven-arm exit-mechanic experiment — the platform already manages profit-target, trailing-stop, touch-zero, and stop-loss exits natively, which can standardize how arms are implemented and audited. *Owner:* Execution-Auditor (audits that live behavior matches the arm's spec).
- **SmartPricing.** Cheaper fills without manual babysitting; relevant to execution-quality auditing. *Owner:* Execution-Auditor.
- **Clone Bot Templates.** One-click replication — the natural mechanism for spinning up pre-registered variant arms consistently. *Owner:* Researcher.
- **Scanners / Screener / Trade Grid / Top Strategies.** Automated market scanning and ranking you may not be exploiting for VIX-gated and ORB bots. *Owner:* Surface-Explorer → Researcher.
- **Inbound Webhooks (the only programmatic surface).** External signals (TradingView, custom Python, Zapier) can *trigger* automations — useful for VIX-gating and ORB entries driven by your own indicators. Note the hard constraint: this **triggers trades**, so under your governance it stays gated/paper only. Webhooks are inbound-only and cannot be used to read or export data out of Option Alpha. *Owner:* Researcher proposes; human rules.
- **Manual "Export Data" (closed positions CSV, emailed, 24-hour expiring link).** The one bulk export; feed it into your ledger to reconcile against browser captures. Note: it covers **closed positions only** (not open positions, not automation logs, not backtests), so it is a reconciliation aid, not a replacement for browser reads. *Owner:* OA-Reader/Pipeline-Runner.

---

## 10. RISKS AND KILL CRITERIA

**Risks and early-warning signs:**
- *Gate leakage* — a write reaches Option Alpha or a doc without a ruling. *Warning:* the un-gated-write counter goes non-zero. This is the one metric that must always read zero.
- *Browser-read corruption* — the agent records stale/blur-uncommitted values as first-hand truth. *Warning:* rising discrepancy between OA-Reader captures and the emailed closed-positions CSV, or between two consecutive reads.
- *Learning-loop drift/reward-hacking* — proposals get more hedged or escalations drop while the visible score rises. *Warning:* human override rate falls *and* proposal specificity falls together.
- *Subagent sprawl / cost blowout* — token spend climbs faster than runs. *Warning:* monthly cost crosses ~$400 without added scope; check cache-hit ratio and subagent count.
- *Vendor-beta breakage* — a Claude beta (context editing header, memory schema) changes and breaks a control. *Warning:* a hook or memory read errors after a model/SDK update.
- *Propagation regression* — the original defect returns. *Warning:* stale-doc count non-zero after a ruling.

**Kill criteria — abandon the conversion and revert to the hardened single session (Phase 0):**
- Any un-gated state change reaches Option Alpha (not a doc) even once and the cause is architectural, not a one-line hook bug → the multi-agent layer is not safe for you; revert immediately.
- After Phase 2, the audit trail cannot reproduce a graded conclusion end-to-end → the system violates your "non-reproducible runs are a defect" rule; revert.
- Maintenance consumes more of your week than the research it supports for two consecutive weeks → the solo-maintainability constraint is breached; revert to Phase 0/1.
- Token/infra cost exceeds the value of time saved (you're paying $400+/month to save an hour a day at paper stage) → revert to the cheaper single-session design.
- **Escalation, not abandonment,** is the correct response to durable-execution failures (mid-run resume gaps): move to Phase 3 (LangGraph), don't kill the project.

**The overriding rule:** because everything is git-tracked and Phase 0 remains runnable at every later phase, *rollback is always cheap*. That is the property that makes an aggressive migration safe for one person.

---

## 11. SOURCES

- Anthropic / Claude Code docs — Agent SDK overview, features (skills, subagents, hooks), `code.claude.com/docs`. GA; SDK renamed from Claude Code SDK, Sept 29, 2025.
- Anthropic Platform docs — Prompt caching; Memory tool (`memory_20250818`, GA on Messages API, no beta header); Context editing (`context-management-2025-06-27`, beta). `platform.claude.com/docs`. 2025–2026.
- Anthropic blog, "Managing context on the Claude Developer Platform," Sept 2025 — memory + context editing +39% over baseline; context editing alone +29%; 100-turn web-search eval −84% tokens.
- Anthropic, "How we built our multi-agent research system," June 13, 2025 — Opus 4 lead + Sonnet 4 subagents "outperformed single-agent Claude Opus 4 by 90.2%"; ~15× tokens; token usage explains ~80% of performance variance.
- Cognition (Walden Yan), "Don't Build Multi-Agents," June 12, 2025 (Principle 2: conflicting decisions → bad results); follow-up "Multi-Agents: What's Actually Working," Apr 22, 2026 ("writes stay single-threaded").
- Claude Agent SDK Python CHANGELOG — `github.com/anthropics/claude-agent-sdk-python` (`max_budget_usd`, structured outputs, betas incl. `context-1m-2025-08-07`). 2025–2026.
- LangChain/LangGraph docs — Durable execution, checkpointers, `interrupt()`, persistence modes (exit/async/sync). `docs.langchain.com`. 2025–2026.
- Diagrid, "Why Checkpoints Aren't Durable Execution" — argues LangGraph/CrewAI/ADK checkpoints ≠ durable execution. 2025–2026.
- Temporal press release, Feb 17, 2026 — $300M Series D at $5B valuation, led by a16z (doubling Oct 2025 $2.5B; total raised $642.75M); durable AI agents blog. `temporal.io`.
- Inngest — durable execution blog; Series A $21M Sept 2025. `inngest.com`.
- ZenML / Spheron / We The Flywheel — Temporal vs Inngest vs Restate comparisons; deterministic-workflow constraints. 2026.
- Agent memory comparisons — Mem0 (ECAI 2025 paper arXiv:2504.19413, +26%; $24M raise Oct 28 2025, TechCrunch), Letta (Bilt >1M agents), Zep/Graphiti (cloud-only since 2025). digitalapplied.com, theaiengineer.substack.com, agenticwire.news. 2026.
- Self-improvement / drift / reward-hacking — Salesforce "Toward Self-Improving Agents"; "Agent Drift" (arXiv:2601.04170, median ~73 interactions); trustworthy-agentic-AI survey (arXiv:2605.23989); Shinn et al. "Reflexion" (NeurIPS 2023, arXiv:2303.11366: HumanEval 91% vs 80%, AlfWorld +22% absolute).
- Observability — Arize "14 best AI agent observability tools" (updated Jul 31, 2026); Braintrust $80M Series B; Laminar/MLflow/Latitude comparisons; OpenTelemetry GenAI conventions. 2026.
- Browser automation — Playwright vs Stagehand vs Browserbase (DigitalApplied, Apr 28 2026: Playwright+Claude 92%, Browserbase 90%, Stagehand 89%, Computer Use 78%); PkgPulse (0.95¹⁰ ≈ 60% end-to-end); stagehand.dev; github.com/browserbase/stagehand. 2026.
- Sandboxes — E2B vs Modal vs Daytona (Northflank, LogRocket, Spheron, AgenticWire); Modal $355M Series C May 2026 (~$4.65B). Rates ~$0.05/vCPU-hr; Modal per-core per-second. 2026.
- Frameworks — Langfuse open-source framework comparison; Uvik, SocialCrawl, PE Collective (LangGraph ~34.5M monthly downloads; CrewAI, Pydantic AI, OpenAI Agents SDK, Google ADK, AutoGen→maintenance). 2026.
- Windmill/n8n — AutomationAtlas (12,400+ stars May 2026); emergent.sh, booleanbeyond.com. 2026.
- **Option Alpha (primary):** Webhooks inbound-only (`docs.optionalpha.com/tools/bots/webhooks.md`; `optionalpha.com/tools/webhooks`, GA 2024). No public/read API, no MCP/SDK — confirmed by absence in `docs.optionalpha.com/llms.txt` and `sitemap.md` plus browser-only architecture (`.../infrastructure-and-security.md`). Data export = manual UI "Export Data," closed positions only, emailed CSV, 24-hour expiring link (`optionalpha.com/blog/export-and-download-bot-position-history-data`, published Jul 24 2023, updated Mar 5 2025). Backtest data not exportable (community post ~Jun 2025: "licensing agreements prevent OA from providing download capabilities of backtest data"). Automation logs view-only in browser (`.../tools/bots/automation-logs.md`). Bot Limitations: overridden positions create audit gaps (`.../platform/bot-limitations.md`). Backtester/0DTE Oracle/Exit Options/SmartPricing/Clone Templates (`docs.optionalpha.com` tool pages). *Verification flag:* "no API" is confirmation-by-absence from the authoritative doc index plus architecture statements, not a single affirmative staff quote (community forum login-gated).
- Options data/backtesting — Option Omega (1-min data back to 2013; docs.optionomega.com); ORATS/ThetaData/Polygon (FlashAlpha "Best Options Data APIs 2026"); QuantConnect LEAN ThetaData connector (github.com/QuantConnect). 2026.

*Marked unverifiable / estimated:* all monthly-cost figures are estimates from published rates at daily cadence and are labeled as such; the "no Option Alpha API" finding rests on comprehensive absence plus architecture statements rather than one explicit denial; several third-party comparison posts (2026) are secondary and were used only to corroborate primary vendor docs.