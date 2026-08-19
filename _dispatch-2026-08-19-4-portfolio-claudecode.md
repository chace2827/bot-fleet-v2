# DISPATCH 4-CC — Portfolio board generator — foreman: Claude Code (terminal, Opus)

> ## ⛔ SUPERSEDED — NOT DISPATCHED — 2026-08-19
> `scripts/portfolio.py` was written and verified in the Cowork session instead, on Andy's call.
> Shipped with `--validate` (11/11), `--check` drift detection, hard-fail on unknown program /
> duplicate id / bad status / out-of-range priority, and three live-derived facts cross-checked
> against an independent shell derivation (roster 44 rows / 19 ON / 4 unsigned — exact match).
> **Nothing in this file was executed. Retained as the spec the implementation was built against,
> and as the template for the next Devin dispatch.** Do not launch it.


Launch: `cd ~/bot-fleet-v2 && claude --model opus` → paste:
"Read _dispatch-2026-08-19-4-portfolio-claudecode.md and execute it as foreman."

## 0. Mission
Build **`scripts/portfolio.py`** — the generator that renders the portfolio board from repo
data instead of by hand. Devin (free local CLI) writes the code; you diff, pilot, and ship it
as a PR. **Additive only** — new files under `scripts/`, `docs/`, `tests/` exclusively. If any
existing tracked file needs an edit (including `scripts/daily.sh`), **queue it for Andy in the
PR body — do not make it.**

The board currently exists as a hand-compiled HTML artifact. That is a snapshot, and under
§9.1a a hand-compiled dashboard is not evidence. This dispatch converts it into a derived
surface: edit the CSV, re-run, the board is true.

You cannot read Cowork memory. Everything you need is in this file plus the repo.

## 1. Ground rules (non-negotiable)
- **Never run git against `~/bot-fleet-v2` in write form. Andy runs every commit to the main
  tree** (CLAUDE.md §9.1 step 3). Git inside your own `/tmp` clones is unrestricted.
- **Never modify `~/bot-fleet-v2`, `~/gitstore`, or `~/.claude`** from any Devin agent. Carry
  this ban verbatim in every agent prompt — a D2 agent overwrote `~/.claude/primer.md` on 08-18.
- **A tool/agent success message is not verification** (§9.1a). Files verify by sha256 + grep;
  merges verify by fetching origin and reading the ref; agent claims verify by reading the bytes.
- **Decisions stay gated.** Nothing here touches build-plan, specs, sizing, kill criteria,
  pre-registration, go-live gates, or any existing guard predicate. This is a renderer.
- **⛔ No literals in acceptance predicates.** Every test states its derivation and computes
  both sides from source. `assert n_items == 77` is a defect; `assert n_items == len(rows)` is
  the test. A literal freezes today's data into tomorrow's CI.

## 2. The free Devin lane
Reuse §2 of `_dispatch-2026-08-19-1-harness-claudecode.md` verbatim — invocation, the
`--model swe-1-7` pin on every attempt, **never `devin -r`**, permission-mode probe, cost/model
assertion, the rate-limit cap, `/tmp` clones never worktrees, heredoc-only incremental output,
warm-up, `bash -c` launch. Nothing about that lane changes here.

**Scale: this is a small job. CAP 2 concurrent agents.** One writes the generator, one writes
the tests, against the same pinned `origin/master` sha. Do not fan out further — a 2-file
Python task fanned to five agents produces five opinions and one merge conflict.

## 3. Inputs — verify each exists before dispatching (pre-flight)
Print the sha256 of each. **If any is missing, STOP and report — do not have an agent invent it.**

| Path | Role |
|---|---|
| `data/portfolio.csv` | **canonical item list** — schema in §4.1. Produced by Cowork; must exist before launch |
| `docs/portfolio.template.html` | the board template with DATA sentinels. Produced by Cowork; must exist before launch |
| `STATUS.md` | headline P&L, unsigned-bot list, focus roster |
| `data/bots_meta.csv` | roster — row count and ON count feed P1/P9 metrics |
| `scripts/report.py` | **read for house style only.** Match its arg handling, path resolution and output conventions; do not import from it |

## 4. The build

### 4.1 `data/portfolio.csv` — schema (Cowork delivers; agents READ ONLY, never rewrite)
```
kind,id,program,title,owner,status,priority,est,blocked_by,source,anchor
```
- `kind` — `program` or `item`
- For `kind=program`: `id` = P1…P9, `title` = name, plus the trailing metric columns
  `question,metric,metric_state,metric_note`
- For `kind=item`: `program` = its P-id, `status` ∈ {Not started, Working on it, Ready,
  Needs sign-off, Stuck, Done}, `priority` 1–4
- `source` — `todo-2026-08-16.csv` or `bot-fleet-migration` — provenance, never dropped

### 4.2 `scripts/portfolio.py` — the generator
- Reads the §3 inputs. **No network. No OA. No git.**
- Emits `portfolio.html` at repo root by replacing everything between the sentinels
  `/* ==== DATA START ==== */` and `/* ==== DATA END ==== */` in the template with one
  `const DATA = {...}` object built from the CSV.
- **Nothing else in the template is touched.** The generator is a data injector, not a
  templating engine — the styling is settled and is not yours to change.
- Counters (`items mapped`, `done`, `awaiting sign-off`, `empty programs`) are **computed**,
  never carried in the CSV. A counter that can disagree with its own rows will.
- `--check` mode: render to a temp buffer, diff against the committed `portfolio.html`,
  exit 1 on drift, write nothing. This is what CI runs.
- Unknown `program` on an item → **hard fail naming the row**. Never silently drop it; a
  dropped item reads as a finished one.

### 4.3 `tests/test_portfolio.py`
State the derivation in each test. Minimum set:
1. Emitted item count == CSV `kind=item` row count.
2. Every item's `program` appears in the `kind=program` set — **zero orphans**.
3. No duplicate item `id` (this is the roster-invariant defect class: a dup key silently
   reroutes a row and every other check stays green).
4. Every `kind=program` id appears in the emitted programs array — an empty program still
   renders, because an unrendered program reads as a completed one.
5. The DATA block extracts and parses as valid JSON.
6. **Idempotence:** two consecutive runs are byte-identical.
7. Every emitted counter recomputed independently from the CSV matches the rendered value.
8. `--check` exits 1 when a CSV row is mutated, 0 when it is not.

## 5. Acceptance — the merge bar
- `python3 scripts/portfolio.py` writes `portfolio.html`; `--check` on the fresh output exits 0.
- All §4.3 tests pass, and **you have read them** to confirm none contains a literal count.
- Cross-surface check (do not skip — two agreeing derivations are weaker than one checked
  against a different surface): the roster count the generator reports for P9 must equal
  `tail -n +2 data/bots_meta.csv | wc -l` computed in your own shell, not by the script.
- Open `portfolio.html` and confirm all four view tabs render and the group headers collapse.
- No tracked file modified outside `scripts/portfolio.py`, `tests/test_portfolio.py`,
  `portfolio.html`.

## 6. Ship
One PR, base `origin/master`, additive. Body carries:
- the pinned base sha every clone was cut from,
- the sha256 of each new file,
- the cross-surface roster figure and how you derived it,
- **QUEUED FOR ANDY** — the one-line `scripts/daily.sh` addition to run the generator after
  the ledger stage, written out verbatim but **not applied**.

Auto-merge is live and phase0 is the required check; approvals are 0 by design. Do not widen
a guard to get green — a blocked instruction goes back to the ruling lane.

## 7. Do NOT
- Do not restyle the board. The template is settled.
- Do not add a database, a server, a build step, or a JS dependency. One Python file, one
  HTML file, standard library only.
- Do not edit `data/portfolio.csv` — categorising an item into a program is a judgment call
  that belongs to Andy and Cowork, not to a code agent. An agent that "fixes" a category is
  making a decision, which is gated.
- Do not wire `daily.sh` yourself. Queue it.
- Do not touch `STATUS.md`, `report.py`, `build_ledger.py`, or anything under `data/` other
  than reading.
