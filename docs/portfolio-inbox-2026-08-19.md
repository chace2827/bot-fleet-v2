# Portfolio inbox — items raised but not yet built
**Intake list. Merges into `data/portfolio.csv` when that file is created; delete this file then.**

| # | Item | Program | Priority | Raised | Notes |
|---|---|---|---|---|---|
| I-01 | **Fleet roster visual** — every bot with its purpose, goal, and family/group | P1 (roster truth) · render lane P6 | 2 | 2026-08-19 (Andy) | Separate surface from the portfolio board. Sources confirmed present: `data/bots_meta.csv` (44 rows, 13 cols incl. `pillar`/`role`/`hedge`/`focus`/`ops_class`), `data/bot_gates.csv`, `docs/pre-registration-ledger.md` (143 KB — the per-bot hypothesis, i.e. the "goal"), `data/trades.csv`, `STATUS.md`. **Framework to be agreed before building** — same review order as the portfolio board. |
| I-02 | `data/portfolio.csv` + `docs/portfolio.template.html` | P6 | 1 | 2026-08-19 | Cowork deliverable. **Blocks dispatch 4-CC** — that dispatch stops at pre-flight if either is missing. Categorising an item into a program is judgment, gated, not a code-agent task. |
| I-03 | Daily republish of the board artifact | P6 | 2 | 2026-08-19 | Scheduled task, device-bound: run the generator via the bridge, then `update_artifact`. Needed because a Cowork artifact is static at publish time — see the architecture note in the 2026-08-19 session. |
| I-04 | `scripts/daily.sh` — add the generator stage | P6 | 2 | 2026-08-19 | **Queued for Andy, not applied.** Written verbatim in the dispatch-4-CC PR body. Editing a tracked file is outside that dispatch's additive-only scope. |

## Note on I-01 scope
"Purpose" and "goal" are different fields and live in different places. `bots_meta.csv` carries
what a bot *is* (pillar, role, hedge code, family, ops_class). The pre-registration ledger carries
what it was *predicted to do* — the falsifiable hypothesis. A roster visual that shows only the
first is an inventory; showing both is what makes it a scoreboard. Decide which one is wanted
before building.
