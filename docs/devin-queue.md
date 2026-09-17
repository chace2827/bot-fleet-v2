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

**North star:** the hedge program's aim is `docs/hedge-north-star.md` (2026-09-16). Read it before
any hedge/backtest dispatch — it carries the signed definition, the authorization boundary
(UI-only; `zdte.*` is parked), and the joined-backtest method that Phase-0's NO answer requires.

---

## Now

- [x] **P0-1 — CI gate. DONE — ruled 2026-08-19 (`R-2026-08-19-P0-1-ACCEPTANCE`, Reading 1).**
      GitHub Actions runs on every PR: the four `--validate` suites, `check_refs.py`, and a
      rerun-and-diff. Andy ruled that `.github/workflows/ci.yml:65` ("run daily.sh twice against
      the scratch root and diff outputs") and `.github/workflows/ci.yml:133` ("rerun-and-diff is
      hermetic under disabled network") together satisfy the acceptance test; the item's own
      `generated`-timestamp-normalizer wording described one possible implementation, not the
      requirement. Delivered by PR #7 (`0051b5e`), which superseded the closed PR #3; hardened by
      #13, #20 and #27. Owner: Devin.
- [ ] **P0-2 — branch protection. Devin side DONE; Andy's click remains.** `.github/CODEOWNERS`
      already exists and covers the gated surfaces (build-plan, pre-registration ledger,
      evidence-standards, CLAUDE.md, all specs, source-of-truth CSVs, `data/archive/`). The
      item's original "lock the Devin lane out" model is **superseded by the signed charter**:
      §1 removed identity-based restrictions and §8 rules CODEOWNERS is *notification only and
      must not block a merge* — the mechanical gate is branch protection + required CI check,
      which only Andy can enable in repo settings. Verified 2026-09-16 by direct read.
- [x] **P0-3 — `.env.example`. DONE — premise was stale.** `.env.example` exists and lists
      `TRADIER_TOKEN` first (plus `TRADIER_BASE`, `LEDGER_START`, `LESSONS_ALLOW_TRUNCATE`);
      `.gitignore` already carries `!.env.example`. Verified 2026-09-16 by direct read.
- [x] **PR #26 — disposition recorded: merged at 424d57b, no rework.** The original "still open
      with changes requested" premise was falsified. `gh pr view 26` reads `state: MERGED`
      (`Add decidability countdown to report.py`); `git log -S _condor_close_dates -- scripts/report.py`
      and `git log -S 'n_window / 20' -- scripts/report.py` return no matches; `master`'s countdown
      already uses `_position_close_dates` (which consumes `single_sided`) and
      `fire_rate = n_window / trading_days_present`. The two named defects were therefore never
      merged and there is nothing to rework. Do not manually close or re-open the PR from this
      session — its queue disposition is Andy's.

## Next — identity and roster seams

- [x] **P1-1 — `data/bots_meta.csv` roster facts verified.** R-2026-08-18-P1-1A-ROSTER-FACTS
      ratifies the 19 ON bots — including all eight GF arms (PR-14…PR-20 and the previously
      signed PR-23) and their `PR-NN` registrations — against the 2026-08-17-r3 capture. The
      pre-cutover-roster premise was false. Seven individual pre-registration ledger entries for
      PR-14…PR-20 are added in the same PR (PR-23 already had its own signed row). **Done.**
- [x] **P1-1a — RULING: roster facts applied.** Andy ruled R-2026-08-18-P1-1A-ROSTER-FACTS,
      ordering seven individual pre-registration ledger entries for the GF arms. The entries
      cite the active build, sizing, naming, signature, go-live and entry-method rulings. Owner: Devin.
- [x] **P1-2 — UNCLASSIFIED is already a refusal. DONE — premise was stale.**
      `build_ledger.py` (the `unclassified` block after roster gating) prints
      `ERROR: UNCLASSIFIED bot(s) in the post-cutover working set:` naming each bot and
      `sys.exit(1)` — the refusal the item asked for already exists. Verified 2026-09-16
      by direct read.
- [ ] **P1-3 — stable `trade_id`.** Currently assigned positionally, so a rebuild re-keys it and
      accumulators keyed on it go stale (`data/hedge_tournament.csv` is stale against the
      `data/trades.csv` committed beside it). Derive it from
      `(bot, open_date, short_put, short_call)` — the natural key
      `docs/comparative-machinery-spec.md` §1.4 already chose, explicitly "not `trade_id`". Migrate
      the accumulator forward. **Sized 2026-09-16: ~115 `trade_id` touchpoints across scripts/
      plus a re-key of every `trades.csv` row — too big to fold into a batch; wants its own
      dispatch/PR.** **DISPATCHED 2026-09-16 — cloud session
      `ac1033c682c54d9db23d843c640e62b1` (app.devin.ai/sessions/ac1033c682c54d9db23d843c640e62b1),
      tags T-10/G-4; the portfolio "in flight" marker was stale — zero live sessions existed when
      checked first-hand.** Owner: Devin.
- [x] **P1-4 — fixture-isolate the non-hermetic tests. DONE 2026-09-16.**
      `load_meta(path=I2_META)` gained a defaulted fixture seam (production caller unchanged);
      `--validate` now exercises all four R-1 refusal branches plus a post-sentinel LOADS check
      against a scratch file, never the live `ledger_meta.json`. Suite moved 35/36 (known-red,
      baseline-pinned) → **40/40 exit 0**; `scripts/ci/validate_baseline.txt` updated in the
      same change per its own rule. The same live-input pattern is predicted in
      `execution_audit`'s V7 matrix (`docs/split2-design-2026-08-08.md`) — the `path=` seam is
      the template. Owner: Devin.
- [ ] **P1-5 — `TRADIER_TOKEN`. Devin side DONE; Andy's token remains.** `tape.py` already reads
      env `TRADIER_TOKEN` or a `TRADIER_TOKEN=` line in `./.env`, honors `TRADIER_BASE`, and
      prints a token-rejected diagnostic; `intraday_read.py` same. `.env.example` documents both.
      Check `data/brief/<date>_tape.json` for `"source"`. Verified 2026-09-16 by direct read.
      Owner: Andy (token only).

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
- [x] **P2-5a — the banner guard HAS a test. DONE — verified green 2026-09-16.** `validate()`
      builds a scratch-root pre-registration-ledger fixture with one unsigned bot in
      `bots_meta.csv` and asserts the banner renders and names it (`report.py` validate block,
      marked P2-5a). `python3 scripts/report.py --validate` → `selftest OK`. Premise was stale.
- [ ] **P2-5b — 🔒 the banner can under-report — now WARNED, not silent.** `report.py` prints
      `WARNING: ledger-unsigned bot not in bots_meta.csv — roster gap` for each ledger-unsigned
      bot absent from `data/bots_meta.csv` (added since this item was written — the "dropped with
      no warning" premise is stale). The open question is now only whether that warning should
      become a refusal — a detector-predicate change → **Class C**, pre-authorisation required
      per charter §4. Verify the gap set with
      `python3 -c "import scripts.pre_registration_ledger as p; print(sorted(p.unsigned_from_ledger('docs/pre-registration-ledger.md')))"`
      against the `bot` column of `data/bots_meta.csv`. Owner: Andy rules, Devin applies.
- [ ] **P2-6 — the 24 dangling citations.** `python3 scripts/check_refs.py` (prints **25**; one of them, `scripts/check_refs.py:263 -> docs/fixture.md`, is the checker's own `--selftest` temp fixture, not a citation — 24 real citations remain). Each needs a
      source-of-truth call (rewrite vs. drop the citation), so none are fixed unilaterally.
      Owner: Andy rules, Devin applies.
- [ ] **P2-7 — selftest known-positive tuple pins mutable ruled facts.** The live
      known-positive tuple in `scripts/pre_registration_ledger.py` pins a ruled fact
      that has already changed once. Future known-positives must either read from a
      fixture or carry a comment naming the ruling that can change them. Recorded, not
      fixed here; see `R-2026-08-18-SELFTEST-KNOWN-POSITIVE-PREAUTH`. Owner: Devin.
- [x] **P2-8 — gate source.** CLOSED by `R-2026-08-18-BOT-GATES-TABLE`. The Phase-3
      verdict engine's sole gate source is `data/bot_gates.csv`; `data/bots_config_v2.csv`
      is explicitly NOT the gate source (it records Bot Inputs, not gates) and is
      unchanged. Owner: Devin.

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
- [ ] **P7 — §2.4 freeze-hash phase0 check.** The §2.4 version-bump procedure is not CI-enforced —
      a phase0 check comparing recorded freeze hashes to the files would have caught PR #44's miss;
      designing that check is a new guard needing its own pre-auth. Owner: Devin.

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
