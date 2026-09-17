# Devin OA capture — dispatch prompt

**Lane:** Devin, browser-driven UI path only. **Authorized by** `R-2026-09-16-DEVIN-OA-CHROME-CAPTURE`
as amended by `-A1`. **HOLD released 2026-09-16 by Andy.**

⚠️ **TWO STANDING GATES — BOTH ANDY'S, NEITHER DISCHARGED BY THIS DOCUMENT.**
1. **The verbatim OA email controls.** Andy re-reads it **before the first run**. If it is narrower
   than "the API process," the `oa-drive` banner narrows and **page-context reads
   (`Runtime.evaluate`, the OA Grab bookmarklet) fall first** — note that the 2026-09-16 roster
   bundle this prompt imitates was produced **by the bookmarklet**, so a narrowing changes the
   method, not just the paperwork.
2. **If the email is ambiguous, Andy sends OA a one-line mechanism clarification** — *"operates its
   own browser, clicks and reads like a user, never calls internal API endpoints"* — rather than
   proceeding on inference.

Do not dispatch until gate 1 is discharged.

---

## The prompt (paste below the line)

---

You are working in the `bot-fleet-v2` repo, connected as a local folder.

**Read these three, in this order, before doing anything:**
1. `CLAUDE.md` — the project contract.
2. `.agents/skills/option-alpha/SKILL.md` — **the law.** Five laws, §5 Traps, §4 two-layer
   verification, §7 what is not expressible, §8 rules of engagement. This governs. When it and any
   other file disagree, it wins.
3. `.agents/skills/oa-drive/SKILL.md` — **the plumbing and the authorization boundary.** Read the
   top banner first and treat it as binding, not advisory.

### ⛔ THE BOUNDARY — three rules, no exceptions, no judgment calls

1. **CAPTURE ONLY. NEVER EDIT.** Bot, automation, scanner, position and settings surfaces are
   **read-only**. Do not open an edit form, do not change a field, do not toggle anything, do not
   click Save — whatever the tooling permits. If a click would mutate state, **stop and report
   instead**. Edits are a different lane under `CLAUDE.md` §5 and are not yours.
2. **NO WIRE PROTOCOL.** No fetch/XHR wrapping or patching, no `POST /api/request` calls of your
   own, no `zdte.*` replay, no traffic recorder, no reading the network panel. You drive the
   interface as a user does: navigate, click, read what is rendered, screenshot, use OA's own
   Export Data. `docs/experiments/oa-rpc-test-2026-09-15/` proves the RPC path exists — **that
   record is history, not a toolkit.** Using it is out of scope pending a broader written grant.
3. **SCOPE EVERY CAPTURE TO THE HOST AT CAPTURE TIME — never afterwards in analysis.** On
   2026-08-20 a recorder pointed at "the browser" wrote 41 WebSocket frames **from an unrelated
   site in another tab** into a repo file. A recorder pointed at the browser records the whole
   browser. Filter to `app.optionalpha.com` at the moment of capture, not when cleaning up.

### ⛔ THE EVIDENCE RULE

**The position's Trades list is the only order-level evidence.** The Exit Options panel shows
*intent*, not execution — it is never evidence of what a bot did (`option-alpha` SKILL.md §0.3
lineage; `oa-platform-reference.md` §0.3). A tool returning success is not verification either
(`CLAUDE.md` §9.1a). State what you observed and where you observed it, every time.

### TASK — backtester surface reconnaissance (read-only)

Under `R-2026-09-16-HEDGE-DEFINITION` a **hedge is a separate protective position**; an exit
strategy is not a hedge. The blocking question for the whole hedge program is:

> **Can OA's backtester express a SECOND, separate protective position — one opened after the
> primary position is already on — or is it single-structure only?**

Answer it by **opening the backtester in the UI and looking.** Not by probing an endpoint.

Capture, read-only:
- The backtester's full configuration surface — every section, every control, expanded.
- Specifically: whether any control adds a second structure/leg-group/position distinct from the
  primary, and whether any control opens a position **conditionally, mid-trade**.
- The vocabulary the UI uses for these, verbatim. Do not paraphrase labels.
- Screenshots of each configuration section.

**Report the answer as YES / NO / NOT DETERMINABLE, with the screenshot and the verbatim label
that establishes it.** "Not determinable" is a legitimate and useful answer — `NOT EVALUABLE` is
preferred over a confident guess throughout this project. Do not run a backtest to find out; do
not build a variant; do not save a configuration.

### DELIVERABLE — imitate this bundle, do not reinvent it

`data/captures/2026-09-16-roster/` is the template. Copy its shape exactly into
`data/captures/2026-09-16-oa-backtester/`:

| file | what |
|---|---|
| `01-<surface>-<YYYY-MM-DD>-<HHMMSS>.txt` | **RAW capture, unmodified.** Rendered text as read. Never hand-edited. |
| `02-<derived>-<YYYY-MM-DD>.tsv` or `.md` | **DERIVED.** Its header comment names the raw file **and its sha256** as the source of every field. |
| `screenshots/` | One per configuration section, named by section. |
| `README.md` | Purpose · capture timestamp **with TZ offset** · a `file / sha256 / what it is` table · the findings · a **verbatim** quote of any footer or label relied on · cross-check path if one exists. |
| `SHA256SUMS.txt` | Hashes for every file in the bundle. |

Read `data/captures/2026-09-16-roster/README.md` and match its structure before writing yours.

### PROHIBITIONS

- No git: no `add`, `commit`, `push`, no branches. **Andy runs every commit** (`CLAUDE.md` §9.1).
  Leave the bundle in the working tree and say it is there.
- Touch nothing outside `data/captures/2026-09-16-oa-backtester/`.
- Do not edit `CLAUDE.md`, `docs/build-plan.md`, any spec, or any ruling.
- No figures in prose. If you state a number, name the file and line that produced it.
- **Stop conditions — no retries past these:** 401/403/429 · an unrecognized response shape · UI
  numbers disagreeing with each other · a URL containing `/login` · any terms or payment prompt ·
  **anything indicating a live (non-PAPER) account.** Stop and report; do not work around.

### REPORT

What you read, where you read it, the YES/NO/NOT-DETERMINABLE answer with its evidence, the bundle
path, and anything you declined to do because a rule above forbade it. **List the refusals** — a
run with no refusals in a boundary this tight is more suspicious than one with several.

---

## Why this task first

It is the blocking question for the hedge program (`hedge-design-spec-2026-09-16.md` §6.1 option 4),
it is pure read, it has a verifiable answer, and it exercises the whole lane — skills, boundary,
bundle discipline — on a task where a wrong answer is cheap and visible. `CLAUDE.md` §5: pilot on a
dead bot; the champion goes last.
