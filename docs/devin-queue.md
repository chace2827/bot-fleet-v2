# Devin work queue

**What this is.** The cross-session backlog for the Devin lane (§7 build lanes). Devin sessions are
stateless; this file is their memory. It is the single place that says what Devin is doing next and
what it is waiting on.

**What this is not.** Not a decision record and not a plan. Nothing here amends `docs/build-plan.md`
or any spec — items that need a decision are listed under *Blocked on a ruling* and stay there until
Andy rules. Per §3 rule 5 this file carries **no figures**; where a claim is numeric it names the
command that produces it, and the command's output wins.

**Convention.** Devin proposes edits to this file in the same PR as the work. Andy may reject any
line at commit review (§5 doc-edit authority — this file is a corrections-class artifact, not a
decision-class one).

---

## Now

- [ ] **P0-1 — CI gate.** GitHub Actions on every PR: the four `--validate` suites, `check_refs.py`,
      and a rerun-and-diff (re-run `daily.sh` on committed inputs through a `generated`-timestamp
      normalizer; fail on any other diff). *Acceptance:* a PR reintroducing a stale accumulator
      fails. Owner: Devin.
- [ ] **P0-2 — CODEOWNERS + branch protection.** Mechanically lock the Devin lane out of
      `docs/build-plan.md`, `docs/pre-registration-ledger.md`, `CLAUDE.md` and every spec. Nothing
      merges red. Owner: Devin. *Andy must enable branch protection in repo settings.*
- [ ] **P0-3 — `.env.example`.** Currently swallowed by `.gitignore`'s `.env.*`. Un-ignore and list
      the vars a fresh clone needs, `TRADIER_TOKEN` first. Owner: Devin.

## Next — identity and roster seams

- [ ] **P1-1 — `data/bots_meta.csv` is the pre-cutover roster.** It contains none of the GF arms and
      none of the `PR-NN` registrations, and still marks archived bots `ON`. Three consequences:
      `SILENT_BOT` fires on archived bots (the detector's whole AMBER budget), it structurally
      cannot fire on the GF arms, and a first GF fill lands `UNCLASSIFIED` in the ledger while being
      reported `OFF`. Verify with `python3 scripts/build_ledger.py` and
      `python3 scripts/execution_audit.py`. **Blocked on P1-1a.**
- [ ] **P1-1a — 🔒 RULING: roster facts.** pillar / role / underlying / champion / ops_class for
      every currently-ON bot. Devin will propose rows from `docs/pre-registration-ledger.md`;
      Andy corrects and signs. Owner: Andy.
- [ ] **P1-2 — promote the UNCLASSIFIED warning to a refusal.** `build_ledger.py` prints a warning
      to stdout for export bots absent from `bots_meta.csv` and exits 0. A warning is not a gate,
      and stdout is unread in a scheduled run. Same shape as the existing ops-class fence.
      Owner: Devin. Depends on P1-1.
- [ ] **P1-3 — stable `trade_id`.** Currently assigned positionally, so a rebuild re-keys it and
      accumulators keyed on it go stale (`data/hedge_tournament.csv` is stale against the
      `data/trades.csv` committed beside it). Derive it from
      `(bot, open_date, short_put, short_call)` — the natural key
      `docs/comparative-machinery-spec.md` §1.4 already chose, explicitly "not `trade_id`". Migrate
      the accumulator forward. Owner: Devin.
- [ ] **P1-4 — fixture-isolate the non-hermetic tests.** `comparative_machinery.py --validate` R-1
      calls `load_meta()` with no argument, so it reads the live `data/ledger_meta.json`; when the
      ledger went live it stopped exercising the sentinel path it exists to guard. Do this before
      config work touches the same pattern in `execution_audit`'s V7 matrix
      (`docs/split2-design-2026-08-08.md` predicts it there). Owner: Devin.
- [ ] **P1-5 — `TRADIER_TOKEN`.** Without it `tape.py` falls back to a reconstructed tape: no
      intraday series, so `daily-loop-spec.md` §1's chart cannot be drawn and §2's directionality
      ratio is null. Check `data/brief/<date>_tape.json` for `"source"`. Owner: Andy (token), Devin
      (wiring).

## Then — the mechanics contract

- [ ] **P2-1 — 🔒 RULING: one mechanics contract.** Four schemas currently disagree:
      `data/bots_config_v2.template.csv`, `docs/split2-design-2026-08-08.md`, the 2026-08-11 rulings
      in `docs/session-log.md`, and what `daily_brief.py` actually reads. The loader joins on `bot`
      and looks for `profit_target`; the ruling says join on `oa_id` and store `pt_pct` only — so
      **the loader change is half the decision, not an afterthought.** Needs: file name, join key,
      column list, three-state cell semantics (value / `none` with capture provenance / blank), and
      `exits_enabled` gating with `event_backstop` ungated. Owner: Andy + Fable.
- [ ] **P2-2 — the parser.** Build the mechanics file from `data/captures/`, importing
      `a_series.py`'s existing decoder rather than writing a second one. Owner: Devin. Depends on
      P2-1.
- [ ] **P2-3 — loader changes + coverage line.** `daily_brief.py` and `execution_audit.py`; the
      coverage gap is printed out loud, never omitted. *Acceptance:* the Tier-C `SKIPPED` rules
      evaluate. Owner: Devin.
- [ ] **P2-4 — OA reads for missing fields.** Read-only, provenance recorded per cell, blank ≠ none.
      Owner: Devin, under §5 two-layer verification.
- [x] **P2-5 — unsigned-bot banner in `report.py`. DONE — verified 2026-08-17 on `f4f07e2`.**
      Ruling `R-2026-08-11-PR-02-PR-04-STAY-ON` requires every report stating the headline to say it
      comes from an unsigned bot. **It already did.** The banner renders at `scripts/report.py:436`
      immediately before `## Headline`, and into the HTML dashboard at line 1086 — both surfaces.
      Built by PR #12 (`ed53b53`), hardened by #16 (`108da28`). This item's own premise was stale:
      `grep -ci unsigned scripts/report.py` returns **12**, not zero. A dispatch built on that premise
      was written and refused in pre-flight; it would have added a second banner.
      **Two real tasks remain, carried forward as P2-5a and P2-5b below.** Owner: Devin.
- [ ] **P2-5a — the banner is a guard with no test.** `validate()` (`report.py:184`) builds fixtures for
      `bots_meta.csv`, `bots.csv`, `trades.csv` and `ledger_meta.json` — **and no pre-registration
      ledger** — so `_ledger_unsigned` is empty and the `if unsigned_bots:` branch is never exercised
      by the self-test. Same shape as P1-4. Class A. Owner: Devin.
- [ ] **P2-5b — 🔒 the banner can under-report silently.** `report.py:351` is an intersection:
      `unsigned_bots = sorted(b for b in meta if b in _ledger_unsigned)`. A bot unsigned in the ledger
      but absent from `data/bots_meta.csv` is dropped with **no warning** — and P1-1 records that roster
      as the pre-cutover one, carrying none of the GF arms and none of the `PR-NN` registrations.
      Verify with `python3 -c "import scripts.pre_registration_ledger as p; print(sorted(p.unsigned_from_ledger('docs/pre-registration-ledger.md')))"`
      against the `bot` column of `data/bots_meta.csv`. A fix changes a detector predicate → **Class C**,
      pre-authorisation required per charter §4. Owner: Andy rules, Devin applies.
- [ ] **P2-6 — the eleven dangling citations.** `python3 scripts/check_refs.py`. Each needs a
      source-of-truth call (rewrite vs. drop the citation), so none are fixed unilaterally.
      Owner: Andy rules, Devin applies.

## Later

- [ ] **P3 — scheduled Pipeline-Runner.** After close: run `daily.sh`, open a PR only if outputs
      changed, silent otherwise. Safe only once P0 exists.
- [ ] **P4 — OA-Reader, three graded steps.** (a) shadow the manual capture and diff daily;
      (b) promote to input once clean, second-sourced against the emailed closed-positions CSV, any
      disagreement a red build; (c) **`data/exit_rows.csv`** to the `comparative-machinery-spec.md`
      §1.4 schema — the missing input that makes every Layer-2 criterion emit `BLOCKED`.
      `UNATTRIBUTED` stays first-class; unread is never inferred.
- [ ] **P5 — Statistician / Researcher.** Wire `comparative_machinery.py` and `research_loop.py` into
      scheduled runs with a **versioned fixed panel** (`daily-loop-spec.md` §0: change the panel and
      every banked day becomes uncomparable). Thursday backtest batch as parallel child sessions.
- [ ] **P6 — Propagator as CI, not an agent.** Extend `check_refs.py` to assert that a figure stated
      in a doc matches the ledger. Depends on the lessons-archive ruling below.

## Blocked on a ruling

| Item | Ruling needed | Owner |
|---|---|---|
| P1-1a | Roster facts for every ON bot | Andy |
| P2-1 | The mechanics contract (four schemas disagree) | Andy + Fable |
| P2-6 | `docs/backlog.md`: rewrite from archive, or drop the citations | Andy |
| Lessons | Archive the v1 index to `data/archive/lessons-v1.csv`, then `LESSONS_ALLOW_TRUNCATE=1`. `lessons.py` refuses until then — correctly. | Andy |
| MCP dispatch | If Cowork can dispatch Devin, a Claude ruling is two hops from a commit. Compatible with §9.1 "Claude does not commit"? Devin's read: yes, **because** the PR gate exists — which is why P0 lands first. | Andy |
| PR-02 / PR-04 | Sign or switch off before live capital. Recorded as a knowing exception; costs nothing on paper. | Andy |

## Never

Writes to OA without an explicit ruling. Any strategy call. Any LLM inside `execution_audit.py` or
`comparative_machinery.py` — they are frozen and deterministic and that is their entire value.
Changing the `$0.08` floor and the strike-selection method in the same experiment.

---

*Devin lane only. The fleet's numbers are `STATUS.md`; the fleet's facts are `docs/state.md`; the
plan is `docs/build-plan.md` (frozen).*
