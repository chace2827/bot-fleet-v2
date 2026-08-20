# Portfolio inbox — items raised but not yet built
**Intake list. Merges into `data/portfolio.csv` when that file is created; delete this file then.**

| # | Item | Program | Priority | Raised | Notes |
|---|---|---|---|---|---|
| I-01 | **Fleet roster visual** — every bot with its purpose, goal, and family/group | P1 (roster truth) · render lane P6 | 2 | 2026-08-19 (Andy) | Separate surface from the portfolio board. Sources confirmed present: `data/bots_meta.csv` (44 rows, 13 cols incl. `pillar`/`role`/`hedge`/`focus`/`ops_class`), `data/bot_gates.csv`, `docs/pre-registration-ledger.md` (143 KB — the per-bot hypothesis, i.e. the "goal"), `data/trades.csv`, `STATUS.md`. **Framework to be agreed before building** — same review order as the portfolio board. |
| I-02 | `data/portfolio.csv` + `docs/portfolio.template.html` | P6 | 1 | 2026-08-19 | Cowork deliverable. **Blocks dispatch 4-CC** — that dispatch stops at pre-flight if either is missing. Categorising an item into a program is judgment, gated, not a code-agent task. |
| I-03 | Daily republish of the board artifact | P6 | 2 | 2026-08-19 | Scheduled task, device-bound: run the generator via the bridge, then `update_artifact`. Needed because a Cowork artifact is static at publish time — see the architecture note in the 2026-08-19 session. |
| I-04 | `scripts/daily.sh` — add the generator stage | P6 | 2 | 2026-08-19 | **Queued for Andy, not applied.** Written verbatim in the dispatch-4-CC PR body. Editing a tracked file is outside that dispatch's additive-only scope. |
| I-05 | **`run_receipt.py` must persist `argv` + an explicit `overrides` list** | P1 (ledger truth) | 1 | 2026-08-19 (close) | A receipt records `day`, `final_exit` and per-stage exits — **not the command line**. A run made with `--allow-rewind` / `--allow-front-truncate` / `--allow-ops-reclass` is indistinguishable in the permanent record from one made without. The three guards at `65799e0` are each overridable, so the artifact whose job is "what was this ledger built from" cannot answer whether a guard was silenced. **Guard change — needs Andy's pre-auth.** Evidence: `data/receipts/daily-runs.jsonl`, the 2026-08-19 pair `exit 1 / 1 stage` then `exit 0 / 9 stages`. |
| I-06 | **`QQQ-IC-0DTE-Fortress-NoPT50` is armed while unsigned — sign it or disarm it** | P1 (roster truth) | 1 | 2026-08-19 (close) | AUTOS ON / EXITS ON in two independent first-hand captures 48h apart: `data/captures/2026-08-17-r3/02-roster-toggles-44-2026-08-17.tsv` and `data/captures/2026-08-19-roster/02-roster-toggles-44-2026-08-19.tsv` (`fb62fa7b56436302…`), bot id `BOTfw5TkkCRF3017862038322323202`. Listed under **UNSIGNED — DO NOT SWITCH ON** in `STATUS.md`. Every performance column reads `--`: armed, never filled, so exposure is prospective. **Andy's decision, gated.** |

## Note on I-01 scope
"Purpose" and "goal" are different fields and live in different places. `bots_meta.csv` carries
what a bot *is* (pillar, role, hedge code, family, ops_class). The pre-registration ledger carries
what it was *predicted to do* — the falsifiable hypothesis. A roster visual that shows only the
first is an inventory; showing both is what makes it a scoreboard. Decide which one is wanted
before building.
