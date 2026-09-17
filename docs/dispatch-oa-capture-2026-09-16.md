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

0. **YOU DO NOT LOG IN.** Andy launches Chrome and authenticates to OA **by hand**, before you
   start (`oa-drive` §1 — *"What Andy does by hand (the session cannot)"*). You attach to an
   already-authenticated browser. **Never request, enter, store or read credentials.** If any URL
   contains `/login`, or a sign-in form appears, **STOP and report** — do not attempt to proceed,
   and do not ask Andy for a password. If you cannot attach to an authenticated session, the answer
   is "not attached," not "let me log in."
1. **NO LIVE-FLEET EDITS — EVER.** Bot, automation, scanner, position and account-settings
   surfaces are **read-only**. Do not open an edit form, change a field, toggle anything, or
   enable/disable a bot — whatever the tooling permits. If an action would alter what a live bot
   does, **stop and report instead**, whatever screen it is reached from. Live edits are a different
   lane under `CLAUDE.md` §5 and are not yours.
   **✅ BACKTESTS ARE THE EXCEPTION** (`R-2026-09-16-DEVIN-OA-CHROME-CAPTURE-A2`). You may
   **create, save, duplicate, rename, delete and run backtest configurations** — a backtest is not a
   bot and touches nothing live.
   ⛔ **Every backtest you create is named `ZZ-AGENT-<YYYY-MM-DD>-<arm>`.** No exceptions, not a
   judgment call. Saved backtests land in shared account state and a later capture reading "the
   backtest list" cannot otherwise tell your artifacts from Andy's. One unprefixed backtest is a
   defect to be renamed, and you report it if you make one.
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

### PHASE 0 — TASK: backtester surface reconnaissance (read-only)

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

## PHASE 0b — the Compare & Combine surface (RULED 2026-09-16, `R-2026-09-16-BACKTEST-COMBINE-S2`)

**Phase 0 is answered and closed** — the bundle exists and the answer is NO for one backtest.
Phase 0b, read-mostly, on the authorized UI path, asks the question Phase 0's dispatch never
asked: what do **two** backtests do together.

Andy has 65 existing backtests. Open `/backtests/compare/<ids>` with two of them and answer,
with screenshots and verbatim labels:

1. **Procedure** — how backtests are added to a comparison and combined. `OA-1143` and
   `OA-1144` are DOCS-SILENT on exactly this; the capture is the only possible record.
2. **Granularity** — does the combined portfolio curve expose **per-day rows**, or summary
   stats only? Day-level is what the loss anatomy and the day-strip heatmap require.
   Summary-only means two trade lists still get transcribed and joined by hand, and the
   combine saving shrinks.
3. **Conditionality** — is combination additive at the portfolio level only, or does any
   control condition one backtest's entries on the other's state? This is the load-bearing
   question. Expect additive; report what is rendered, not what is expected.
4. **Size ratio** — is there a control for relative sizing between combined backtests, or is
   it 1:1? Size ratio is a required field of the Monitor spec (`hedge-north-star.md` §6). If
   absent, the ratio has to be swept as separate backtests and the grid grows.
5. **Duplicate fidelity** — does duplicating a config preserve the full fixed frame so only
   the differ changes? If yes it also retires the `text`/`textValues` display-string trap on
   the 21 untouched fields — a second reason to prefer duplicate over hand-construction.
6. **Ceiling** — confirm or falsify `OA-1090`'s *"up to four backtests simultaneously"* against
   the live surface, and record whether the four-way cap applies to Compare only or to Combine
   Results as well.

**Naming.** Any saved comparison lands in shared account state exactly as a saved backtest
does — `ZZ-AGENT-<YYYY-MM-DD>-<arm>` applies to it (`-A2`), or nothing is saved at all.

**Read scope — RULED 2026-09-16 (`R-2026-09-16-BACKTEST-COMBINE-S4`):** DOM/JS reads of page
state are inside the grant — rendered text, `input.value`, hidden-input serialization,
hydrated models. Still forbidden, unchanged: any API call, replay, network inspection, or
traffic recorder.

**Do not start Phase 1 in the same session as Phase 0b either.** Phase 0b's answers re-size
the grid and decide whether any manual join survives outside V3.

### The Phase 0b prompt (paste below the line)

---

You are working in the `bot-fleet-v2` repo, connected as a local folder.

**Read these three, in this order, before doing anything:**
1. `CLAUDE.md` — the project contract.
2. `.agents/skills/option-alpha/SKILL.md` — **the law.** When it and any other file disagree,
   it wins.
3. `.agents/skills/oa-drive/SKILL.md` — **the plumbing and the authorization boundary.** Read
   the top banner first and treat it as binding, not advisory.

Then read `docs/decision-card-2026-09-16-backtest-combine.md` — all five slots are ruled; it
tells you why this task exists.

### ⛔ THE BOUNDARY — three rules, no exceptions, no judgment calls

0. **YOU DO NOT LOG IN.** Andy launches Chrome and authenticates to OA **by hand** before you
   start (`oa-drive` §1). You attach to an already-authenticated browser. **Never request,
   enter, store or read credentials.** If any URL contains `/login`, or a sign-in form appears,
   **STOP and report.** "Not attached" is the answer, not "let me log in."
1. **NO LIVE-FLEET EDITS — EVER.** Bot, automation, scanner, position and account-settings
   surfaces are **read-only**. If an action would alter what a live bot does, **stop and
   report**, whatever screen it is reached from.
   **✅ BACKTESTS ARE THE EXCEPTION** (`-A2`): you may create, save, duplicate, rename, delete
   and run backtest **configurations**. For this task you should not need to create any —
   Andy has 65 existing backtests; use them.
   ⛔ **If you save anything — including a saved comparison — it is named
   `ZZ-AGENT-<YYYY-MM-DD>-<arm>`.** No exceptions.
2. **NO WIRE PROTOCOL.** No fetch/XHR wrapping, no `POST /api/request` calls of your own, no
   `zdte.*` replay, no traffic recorder, no reading the network panel. You drive the interface
   as a user does.
   **Read scope — RULED 2026-09-16 (`R-2026-09-16-BACKTEST-COMBINE-S4`):** DOM/JS reads of page
   state are inside the grant — rendered text, `input.value`, hidden-input serialization,
   hydrated models. "The inspection portion" means the API-discovery path, not DOM reads.
3. **SCOPE EVERY CAPTURE TO THE HOST AT CAPTURE TIME** — filter to `app.optionalpha.com` at
   the moment of capture, never afterwards in analysis.

### ⛔ THE EVIDENCE RULE

**The position's Trades list is the only order-level evidence.** A tool returning success is
not verification (`CLAUDE.md` §9.1a). State what you observed and where you observed it,
every time. Report what is **rendered**, not what you expect — this task's whole point is
that the expected answer is unverified.

### PHASE 0b — TASK: the Compare & Combine surface (read-mostly)

Phase 0 proved **one** backtest is single-structure. OA also offers `/backtests/compare/<ids>`
with `Add Backtest` and `Combine Results` (capture `01-…-223758.txt`, lines 219-222). What
**two** backtests do together was never asked. Answer it by **opening the surface and
looking.**

Open `/backtests/compare/` with two of Andy's existing backtests (pick any two — this is a
surface recon, not a result read) and answer, with screenshots and **verbatim labels** —
do not paraphrase:

1. **Procedure** — how are backtests added to a comparison, and how is `Combine Results`
   invoked? Record the exact controls and the exact click path.
2. **Granularity** — does the combined portfolio view expose **per-day rows** (a trade list
   or daily P/L table), or summary stats only? Verbatim the column headers of whatever table
   exists.
3. **Conditionality** — is combination additive at the portfolio level only, or does ANY
   control condition one backtest's entries on the other's state? **This is the load-bearing
   question.** Expect additive; report what is rendered.
4. **Size ratio** — is there any control for relative sizing between combined backtests, or
   is it 1:1? Verbatim the control label if one exists.
5. **Duplicate fidelity** — open one of the compared backtests' settings and duplicate it.
   Does the duplicate carry the full configuration, so only the differ changes? Do not save
   the duplicate — report what the duplicate form pre-fills.
6. **Ceiling** — `OA-1090` documents *"up to four backtests simultaneously."* Confirm or
   falsify against the live surface: try to add a fifth; record the exact error or the exact
   fifth slot. Record whether the cap applies to Compare only or to Combine Results as well.

**Also confirm first-hand:** whether the results/compare view has any **export** mechanism
(`docs/AI Agent Stack.md`:256 says backtest data is not exportable — confirmation-by-absence,
not an OA statement). Report what you find.

### 📚 REFERENCE SHELF — what to read when the UI is ambiguous (ADDED 2026-09-16, at Andy's instruction)

You are not expected to derive this surface from nothing. The repo carries a harvest of OA's own
documentation and one first-hand capture of the adjacent surface. **Use them to know what to look
for and what to name it. Never use them to answer.**

#### ⛔ The precedence law — read this before you open any of them

**What is RENDERED on the live surface outranks every file in this repo, always.** A repo file can
tell you a control is supposed to exist; only the screenshot proves it does. If a file and the
screen disagree, the screen wins and **the disagreement is itself a finding you must report** — fact
ID, verbatim doc quote, verbatim rendered label, screenshot.

Three rules that follow from it:

- **A docs fact is CONTEXT, never EVIDENCE.** Every one of the six answers is established by a
  screenshot plus a verbatim rendered label. A `data/oa_facts.csv` fact ID may appear in your README
  only as *"docs said X; the surface renders Y"* — never as the basis for an answer.
- **Never cite a project document as evidence for a claim about OA.** Two documents vouching for
  each other is a citation loop (`CLAUDE.md` §5, provenance rule). Cite OA's own words (a fact ID
  with its verbatim `quote` column) or a dated first-hand observation you made. Nothing else.
- **Inference from absence is not an observation** (`CLAUDE.md` §5). "The docs don't mention a size
  ratio control" is not an answer to question 4. "I opened Combine Results, expanded every pane, and
  no control bearing on relative sizing is rendered — screenshot `04-combine-results.png`" is.

#### 🔧 `data/oa_facts.csv` — 1,548 facts harvested from docs.optionalpha.com on 2026-08-04

Columns: `fact_id,area,page_title,page_url,claim,quote,tier,gap_flag,last_verified,page_fingerprint`.
`quote` is OA's verbatim sentence — that is the citable unit. `claim` is the harvester's paraphrase
and is **not** citable.

Query it, don't read it whole:

```
grep -i "backtest" data/oa_facts.csv | cut -d, -f1,3,5 | head -50
python3 -c "import csv;[print(r['fact_id'],'|',r['tier'],'|',r['quote']) for r in csv.DictReader(open('data/oa_facts.csv')) if r['page_title']=='Backtesting Metrics']"
```

**Two tiers matter here.** `DOCUMENTED` = OA published a sentence saying it. `DOCS-SILENT` = the
harvest established that OA's docs **do not** cover it, with the open question recorded in
`gap_flag`. A `DOCS-SILENT` row is a licence to go look, not a finding.

**The 117 backtest-related rows, mapped to your six questions:**

| Your question | Facts to pull first | What they give you |
|---|---|---|
| 1. Procedure | `OA-1141`…`OA-1144`, `OA-1147` | All **DOCS-SILENT**. `OA-1143`/`OA-1144` record that OA's "Comparing and combining backtests" page is an *empty embed block with a blank URL* — there is no written procedure anywhere. **Your capture is the only record that will ever exist.** |
| 2. Granularity | `OA-1079`, `OA-1099`, `OA-1107`, `OA-1109` | The per-backtest vocabulary: "detailed trade logs", `Count`, per-trade averaging, the `Filtered Trades` view. Whether any of it survives into the *combined* view is exactly what is unknown. |
| 3. Conditionality | `OA-1076`, `OA-1077`, `OA-1091` | The only three sentences OA has ever published on combining. All three describe **result aggregation** — *"combine the results of multiple strategies into one portfolio curve."* None describes coupling. Expect additive; report what is rendered. |
| 4. Size ratio | *(nothing — no fact in the harvest mentions relative sizing between backtests)* | Genuine silence. Treat as unknown, not as absent. |
| 5. Duplicate fidelity | `OA-1076` | *"Quickly add multiple variations to stress-test different variations and variables"* — the vendor's own framing of the variant workflow. It does not say what a duplicate carries. |
| 6. Ceiling | `OA-1089`, `OA-1090`, `OA-1091` | ⚠️ **Read the trap below before using these.** |

#### ⚠️ The worked example — why you check the render even when the docs are unambiguous

`OA-1089`, `OA-1090` and `OA-1091` are **three clauses of one sentence** on one page
(`docs.optionalpha.com/tools/backtesting/backtesting-metrics`):

> *"Traders can use a test period of up to three years, and compare up to four backtests
> simultaneously, and combine multiple backtested strategies to see a single portfolio P/L curve."*

The first clause is **already falsified by first-hand capture.**
`data/captures/2026-09-16-oa-backtester/01-backtest-settings-form-2026-09-16-223758.txt` lines 77-82
render `Test Period` as `1 year · 2 years · 3 years · 5 years · Custom`. The docs sentence is stale —
it predates the June-2026 backtester release.

**Therefore the four-backtest cap in the sibling clause inherits the same staleness risk.** Do not
report question 6 as "confirmed by `OA-1090`." Add backtests until the surface refuses, and record
the exact refusal — the error text, or the fifth slot accepting. One stale clause in a sentence
means the whole sentence is dated, not that the rest is fine.

#### 📁 The rest of the shelf — what each file is for, and its limit

| File | Use it for | Limit |
|---|---|---|
| `data/captures/2026-09-16-oa-backtester/` | **The template and the baseline.** `02-second-position-expressivity-2026-09-16.md` is a control-by-control table of the single-backtest form with verbatim labels — reuse its vocabulary so your bundle is diffable against it. `01-…-223758.txt` lines 219-222 are the sighting that generated your task. | It is the **New Backtest** surface, not Compare. Nothing in it answers a two-backtest question. |
| `docs/decision-card-2026-09-16-backtest-combine.md` | **Why this task exists.** §"What it changes" maps V0-V4 onto the variant frame; it states plainly that additive-only combination makes V1/V2 *unconditional overlays, not reactive hedges*. Read it so you understand which answer costs what. | It is a decision record, not evidence about OA. Never cite it for a platform fact. |
| `docs/backtest-ingest-protocol.md` | The house standard for reading backtest results — DISCOVERY vs CONFIRMATION, window policy, compare-by-R. Useful for naming things the way this project names them. | About analysing results. Not about the Compare UI. |
| `.agents/skills/option-alpha/SKILL.md` | **The law**, already in your read-first list. §7 is what OA affirmatively cannot express. | Governs; when it and any other file disagree, it wins. |
| `data/oa_facts.csv` `page_title='Backtesting'` / `'Backtesting Metrics'` | Metric definitions in OA's own words — `Max Risk`, `Max Drawdown`, `Profit Factor`, `Count`, `Win Rate`. Use them to read the Compare grid's column headers correctly. | Definitions for a **single** backtest. Whether a combined view recomputes them or sums them is unknown and is worth recording if the surface shows it. |

#### ⛔ Not on the shelf — do not read these for this task

- `docs/oa-platform-reference.md` and its v3 draft. 1,431 lines on **bots**, and the backtester
  appears exactly once (line 47) as an aside noting the June-2026 release postdates its research.
  There is no backtester content in it. Reading it will cost you an hour and teach you nothing.
- `docs/ic-trailing-stop-backtest.md` — carries a **PREMISE FALSIFIED** banner.
- `docs/lean-backtesting-reference.md`, `docs/quantconnect-lean-exploration-brief.md` — QuantConnect,
  a different platform entirely.
- `docs/oo-trial-backtests.md` — OptionOmega, a different vendor.
- `docs/experiments/oa-rpc-test-2026-09-15/` — **history, not a toolkit.** The RPC path is outside
  the grant (BOUNDARY rule 2). Do not open it looking for a shortcut.
- Anything under `data/archive/` or `~/bot-fleet` — frozen v1, never an input.

#### 📝 What the shelf obliges you to report

Add one section to your `README.md`, **`## Docs-vs-render deltas`**: every place a
`data/oa_facts.csv` fact and the live surface disagreed, as a row of *fact ID · verbatim doc quote ·
verbatim rendered label · screenshot*. `OA-1089` is already one and is yours to confirm if the
Compare surface restates a period. If you find none, say "none found" and name the facts you checked
against — a checked-and-agreed list is a result.

If a question is unanswerable because the shelf is silent **and** the surface does not render it,
the answer is `NOT DETERMINABLE` with both halves stated. That is a legitimate result here and is
strongly preferred to a confident guess.

### DELIVERABLE — same bundle shape, new directory

`data/captures/2026-09-16-oa-backtester/` is the template. Copy its shape into
`data/captures/2026-09-16-oa-compare/`: raw capture files (`01-…` unmodified), derived files
whose headers name the raw source **and its sha256**, `screenshots/` named by section,
`README.md` (purpose · timestamp **with TZ offset** · file/sha256/what table · the six answers
each with its verbatim-label evidence), `SHA256SUMS.txt` over everything.

### PROHIBITIONS

- No git: no `add`, `commit`, `push`, no branches. **Andy runs every commit.**
- Touch nothing outside `data/captures/2026-09-16-oa-compare/`.
- Do not edit `CLAUDE.md`, `docs/build-plan.md`, any spec, or any ruling.
- Do not run a backtest; do not create, save, rename or delete one; do not save a comparison.
  Read-only navigation plus, at most, opening a duplicate form to read what it pre-fills.
- **Stop conditions — no retries past these:** 401/403/429 · an unrecognized response shape ·
  UI numbers disagreeing with each other · a URL containing `/login` · any terms or payment
  prompt · **anything indicating a live (non-PAPER) account.** Stop and report.

### REPORT

The six answers, each YES/NO/NOT-DETERMINABLE where that applies, each with its screenshot and
verbatim label; the export finding; the bundle path; and **the refusals** — anything you
declined because a rule above forbade it. A run with no refusals in a boundary this tight is
more suspicious than one with several.

**Do not start Phase 1 in this session.** Report Phase 0b, stop, wait for Andy.

---

## PHASE 1 — the hedge tests (only after Phase 0 answers)

**Do not start Phase 1 in the same session as Phase 0.** Phase 0's answer decides which Phase 1
exists. Report Phase 0, stop, wait for Andy.

### ✅ THE ARM TABLE — RULED 2026-09-17, `R-2026-09-17-PHASE1-ARM-TABLE`

**This replaces the YES/NO branching below.** That branching was written before Phase 0b and 0c and
is superseded: Phase 0 answered NO *for one backtest*, but `Combo Rules` makes the question a
two-backtest one, and 0c settled its semantics. The original text is preserved beneath, struck.

**Arm count is the budget** — the UI path has no sweep. Stage 1 spends five arms to reach the
decision. Stage 2 runs **only** if Stage 1's combine clears the `R-2026-09-17-PAPER-ARM-PREAUTH`
bar.

#### Stage 1 — 4 backtests + 1 combine. Fits one 7-way Compare.

| # | Arm | Build | What it answers |
|---|---|---|---|
| **S1-0** | **H-0 control** — primary condor, ride to settlement. No PT, no SL, expiration only. | 1 backtest | The baseline. **Run FIRST**; nothing else means anything without it. |
| **S1-a** | **SL100** — primary + stop | 1 backtest | incumbent exit to beat |
| **S1-b** | **SL200** — primary + stop | 1 backtest | incumbent exit to beat |
| **S1-c** | **Overlay** — long put debit spread, **14:00 ET**, 1 contract | 1 backtest | the hedge leg's standalone cost |
| **S1-H** | **H-B** = S1-0 ⊕ S1-c, **presence-gated**, caps pinned in `crules` | 1 combine | ⭐ **the question: does hold-plus-hedge beat stop?** |

**The comparison that decides Phase 1: S1-H against S1-a and S1-b, in R, against S1-0.**

#### The Stage-1 primary — from `greenfield-family-spec.md` §3, NOT invented

`QQQ` · expiration **exactly 0 days** · short strikes **0.75% OTM** both sides · width **$2.00** ·
**1 contract** · entry **after 13:30 ET** · **Range075** gate (symbol change % between −0.75 and
+0.75 since previous close, via the backtester's `Change %` entry filter) · minimum credit mid
**≥ $0.08**.

⚠️ **Divergence to record in the bundle, not smooth over:** the fleet builds this as **two paired
spreads** (ScannerA put / ScannerB call); the backtester offers **Iron Condor as one structure**.
Stage 1 uses the single structure, which collapses the fleet's per-side exit independence.

#### Three constraints that bind every arm

1. **No arm is tested-side-reactive, and none may be described as such.** Nothing in the predicate
   surface reads a sibling position's state — `Combo Rules` is `open`|`not open`, entry filters are
   underlying/market state, the 8-structure picker is set at config time. Every hedge arm is a
   **fixed-side unconditional overlay with a presence gate**. `hedge-north-star.md` §4's
   "tested-side" V1 is not buildable here.
2. **Put side only**, and every Stage-1 write-up says so. Side selection is not expressible, so
   choosing one is a **choice, not a finding**.
3. **The presence gate is kept ON and is not a separate arm.** It removes precisely the
   Range075-rejected days — the large-move days on which the condor never enters and an ungated
   overlay would fire with nothing to protect, booking pure cost.

#### Stage 2 — gated on S1-H clearing the bar. Nothing here runs otherwise.

| sweep | arms | note |
|---|--:|---|
| Entry time — 13:30 / 14:00 / 14:30 / 15:00 | 4 | §2.3 puts 89% of loss in 14:00–15:30 |
| **Size ratio** — overlay at 2ct, 3ct | 2 | **not optional, only deferrable**: no relative-sizing control exists (0b Q4) and `hedge-north-star.md` §6 makes ratio a required Monitor field |
| Call side | 1–2 | a strangle overlay is S1-0 ⊕ put ⊕ call = 3 tests, inside the 7-cap |
| No-hedge-after cutoff | 1–2 | cheapest inferred from the time sweep first |

#### Measurement

Compare by **R**, never raw $ (`CLAUDE.md` §4), and label the unit every time. For a combined arm
the denominator is stated explicitly — **primary risk + overlay debit, per condor, ex-artifact**.
**A combined Exp(R) whose denominator is not written down is not a result.**

<details>
<summary>⊗ SUPERSEDED — the original YES/NO branching, preserved verbatim (2026-09-16)</summary>

### If Phase 0 = YES (the backtester can express a second, separate position)

Then a hedge in the project's sense is testable, and these are the hypotheses — **in this order**,
one backtest at a time. The UI path has no sweep, so the order is the budget.

| # | Arm | What it tests |
|---|---|---|
| **H-0** | **Control — no hedge, no stop, ride to settlement.** | The baseline every other arm is measured against. Run it FIRST. Without it the others mean nothing. |
| **H-A** | Primary + a **separate protective position opened at/after 14:00 ET**, only on days the primary is already losing. | The core hypothesis. `hedge-design-spec` §2.3: 75% of losing positions take their worst tick after 14:00 vs 32% of winners; 89% of all loss has its MAE inside 14:00-15:30. |
| **H-B** | Same as H-A but opened at a **fixed time regardless** of whether the primary is losing. | Isolates whether the *conditionality* earns its cost, or whether the clock alone does the work. §2.3 warns a bare time gate also fires on the 29% of winners whose MAE lands 14:00-15:00. |
| **H-C** | Primary + **SL100** and, separately, **SL200**. | Not a hedge — an exit, and included deliberately as the incumbent to beat. Both are **net negative on live data** (-$173, -$584), the only two GF arms underwater. If the hedge cannot beat a stop that is already losing money, it is not a finding. |

**Compare by R (pnl ÷ risk), never by raw $** (`CLAUDE.md` §4). Report per-arm: N, Exp(R), win
rate, max drawdown in R, worst single R. Label the unit — *"per condor, ex-artifact"* or
*"per leg, raw"* — every time. An Exp(R) with no unit label is untrustworthy.

> ### 📌 AMENDED 2026-09-17 — two rulings bear on this table. FULL RESPEC STILL OWED.
> **`R-2026-09-17-PHASE1-SUBSTRATE-SPLIT` (Slot A = A3).** The Phase 1 grid is **self-contained**.
> No live-ledger number enters any ranking in it. **H-C's `-$173` / `-$584` demote to CONTEXT and
> are no longer the bar** — H-C's bar is restated in **R against H-0**, like every other arm. The
> incumbent-to-beat comparison against live GF is not cancelled; it becomes its **own deliverable**,
> and that deliverable is gated on resolving the `Ride`/`Touch0` identity (§8 banner above).
>
> **`R-2026-09-17-COMBO-RULES-PRESENCE-ONLY`.** H-A ("only on days the primary is already losing")
> is **NOT expressible** — no P/L predicate exists in `Combo Rules`, whose only vocabulary is
> `open` | `not open`. H-B becomes natively expressible **and improves** (a presence gate removes
> false fires on days the primary never entered). Any arm built on a combo rule is named a
> **presence-gated overlay**, never a reactive hedge.
>
> **`R-2026-09-17-PAPER-ARM-PREAUTH` (Slot B = B3).** One paper arm is pre-authorized for the
> single winning variant, on the bar recorded in that ruling, pre-registered per `CLAUDE.md` §5.
> Measurement remains the default for everything else.
>
> ⛔ **The table above is NOT yet rewritten.** The respec waits on Phase 0c's `open` semantics
> (`R-2026-09-17-COMBO-SEMANTICS-RUN`) and on Slot 4 of the 2026-09-17 sitting, both open at the
> time of this banner. Do not run Phase 1 off this table until the respec lands.

### If Phase 0 = NO or NOT DETERMINABLE

There is no hedge to test in the backtester. **Do not substitute an exit variant and call it a
hedge** — `R-2026-09-16-HEDGE-DEFINITION` makes that a category error, not a near-enough. Run
**H-0 and H-C only**, report them as an *exit* comparison, and say plainly in the README that the
hedge question is unanswered and why.

</details>

### Rules that bind both phases

- **Backtests only. No live bot is created, cloned, enabled, or edited.** Saving and duplicating
  backtests is **authorized** (`-A2`); every one carries the `ZZ-AGENT-<date>-<arm>` prefix.
> ### ⛔ SUPERSEDED 2026-09-17 — `R-2026-09-17-PHASE1-EVIDENCE-PROCEDURE`. Bullet below stands, struck.
> **Export EXISTS at position level.** Every positions drawer renders `Copy CSV` / `Download CSV`;
> proven 2026-09-16 with a 126-row, 24-column CSV carrying minute-level `Opened`/`Closed` and a
> per-test `Test` column. The regime is **narrowed, not struck**:
> - **Position data** comes from the CSV export.
> - **Summary statistics** (Stats table, equity chart, Combined Monthly P/L) have **no export
>   control** and remain screenshot-and-transcribe.
> - ⛔ **A combined export is a RESULT, not a CENSUS.** Standalone 249 + 249 = 498 against an
>   unruled control of **497** — the `2025-11-03` overlay row is absent from *every* combined run
>   including the rules-free one, with caps permitting it and **no error rendered**. **Reconcile
>   every combine row-for-row against standalone exports of its constituent tests BEFORE ranking.
>   Report an unexplained delta; never absorb it.**
> - ⛔ **Pin `posLimit` and `posLimitDay` explicitly in `crules` on every combine** and record them
>   with the run. Defaults scale exactly N (2 tests → 2/2, 4 → 4/4, 7 → 7/7) and demonstrably change
>   results, so combined results are not comparable across pass sizes under defaults.
> - ⛔ **A malformed rule or invalid JSON does NOT error** — the page silently falls back to the
>   unruled control and renders a complete-looking result, while the SPA-sticky drawer can display a
>   rule the URL does not carry. **Verify what ran from the URL and the row count, never the
>   drawer.** Any combined run whose row count equals the unruled control's is **presumed UNRULED**
>   until its URL is re-read.

- ⚠️ **ASSUME THERE IS NO EXPORT.** `docs/AI Agent Stack.md`:256 records that OA **backtest data is
  not exportable** — *"licensing agreements prevent OA from providing download capabilities of
  backtest data."* **Confirm this first-hand against the results screen and report what you find**;
  it is currently confirmation-by-absence, not an affirmative OA statement. If it holds, the capture
  bundle is the **primary record**, not a convenience: transcribe every result by hand, screenshot
  it, and capture its configuration verbatim alongside it. A number whose configuration was not
  captured cannot be re-derived — re-running the variant is the only way to re-check it.
- **Every run gets its own raw capture**: the configuration as the UI displays it (verbatim labels,
  not your paraphrase) and the results as rendered. Config and result travel together or the run is
  uninterpretable later.
- **State the sample.** OA's backtest history window is whatever the UI says it is — quote it. A
  result with an unstated sample period is not a result.
- ⚠️ **These are PAPER/backtest figures and are T4 at best.** Nothing here supports a live-capital
  decision (`CLAUDE.md` §4 requires T2 with n>=100 / 6 months / a regime change). Do not write a
  recommendation. Report the numbers and stop.

---

## Why this task first

It is the blocking question for the hedge program (`hedge-design-spec-2026-09-16.md` §6.1 option 4),
it is pure read, it has a verifiable answer, and it exercises the whole lane — skills, boundary,
bundle discipline — on a task where a wrong answer is cheap and visible. `CLAUDE.md` §5: pilot on a
dead bot; the champion goes last.

---

## PHASE 1 — Stage 1. The hedge grid. (RULED 2026-09-17, `R-2026-09-17-PHASE1-ARM-TABLE`)

Every gate is discharged. Stage 1 is **4 backtests + 1 combine**, and Stage 2 does not exist until
Andy rules on Stage 1's result.

### The Phase 1 Stage-1 prompt (paste below the line)

---

You are working in the `bot-fleet-v2` repo, connected as a local folder.

**Read these, in this order, before doing anything:**
1. `CLAUDE.md` — the project contract. §4 (evidence law, compare by R) and §9.1a are load-bearing.
2. `.agents/skills/option-alpha/SKILL.md` — **the law.** When it and any other file disagree, it wins.
3. `.agents/skills/oa-drive/SKILL.md` — the plumbing and the authorization boundary.
4. `docs/decision-card-2026-09-17-phase1-arm-respec.md` — **the table you are building**, and why
   each arm exists.
5. `docs/phase0c-verification-2026-09-17.md` — §1, §3 and §5 are the traps that will bite this run.

Then read these four rulings in `docs/RULINGS.md`. They govern how you build, verify and phrase
everything: `R-2026-09-17-PHASE1-ARM-TABLE` · `R-2026-09-17-PHASE1-EVIDENCE-PROCEDURE` ·
`R-2026-09-17-COMBO-RULES-PRESENCE-ONLY` · `R-2026-09-17-PAPER-ARM-PREAUTH`.

### ⛔ THE BOUNDARY

0. **YOU DO NOT LOG IN.** Andy authenticates Chrome by hand before you start. Attach to an
   already-authenticated browser. If a URL contains `/login` or a sign-in form appears, **STOP and
   report.** Never request, enter, store or read credentials.
1. **NO LIVE-FLEET EDITS — EVER.** Bot, automation, scanner, position and account-settings surfaces
   are read-only. ⛔ **NO `Create Bot`** — not on a single backtest, not on a combined one, not on
   any surface, whatever the ruling says about paper arms. A paper arm is a separate, pre-registered
   act that is not yours.
   ✅ **RUNS ARE AUTHORIZED FOR THIS TASK** (`-A2`, `R-2026-09-17-PHASE1-ARM-TABLE`): create, save,
   duplicate, rename, delete and run **backtest configurations and combines**.
   ⛔ **Everything you save is named `ZZ-AGENT-<YYYY-MM-DD>-P1-<arm>`** — e.g.
   `ZZ-AGENT-2026-09-17-P1-S1-0`. No exceptions. Note the 0c fixtures
   (`ZZ-AGENT-2026-09-17-primary` / `-overlay`) already exist and are **NOT** Phase 1 arms — do not
   reuse, rename or delete them.
2. **NO WIRE PROTOCOL.** No fetch/XHR wrapping, no `POST /api/request` of your own, no `zdte.*`
   replay, no traffic recorder, no network panel. DOM/JS reads of page state remain in scope
   (`R-2026-09-16-BACKTEST-COMBINE-S4`).
3. **Scope every capture to `app.optionalpha.com` at capture time**, never afterwards in analysis.

### ⛔ THE THREE TRAPS THAT WILL BITE THIS RUN — read before building

1. **A malformed `crules` rule or invalid JSON does NOT error.** The page silently falls back to the
   **unruled control** and renders a complete-looking result. The drawer's form state is
   **SPA-sticky** and can display a rule the URL does not carry. **Verify what ran from the URL and
   the row count, never the drawer.** ⛔ **Any combined run whose row count equals the unruled
   control's is PRESUMED UNRULED until its URL is re-read.**
2. **A combined export is a RESULT, not a CENSUS.** Proven: standalone 249 + 249 = 498 against an
   unruled control of **497**, one row absent from every combined run with caps permitting it and no
   error shown. ⛔ **Reconcile every combine row-for-row against standalone exports of its
   constituent tests BEFORE computing any ranking. Report an unexplained delta; never absorb it.**
3. **Caps change results and default to exactly N.** ⛔ **Pin `posLimit` and `posLimitDay`
   explicitly in `crules` on the combine, and record the pinned values with the run.** Do not accept
   the defaults silently.

### THE PRIMARY — build it exactly; do not improvise

From `greenfield-family-spec.md` §3. This mirrors the live fleet and is not negotiable:

| Field | Value |
|---|---|
| Symbol | `QQQ` |
| Expiration | `exactly 0 days` |
| Strategy | **Iron Condor** (single structure) |
| Short strikes | **0.75% OTM** both sides |
| Width | **$2.00** each side |
| Position Size | **1 contract** |
| Entry time | **13:30 ET** |
| Entry filter | **`Change %` between −0.75 and +0.75** (the Range075 gate) |
| Position Criteria | mid price **≥ $0.08** |
| Test Period | the longest the UI offers; **quote it verbatim in the README** |

⚠️ Record in your README: the fleet builds this as **two paired spreads** (ScannerA put /
ScannerB call); you are using the backtester's **single Iron Condor**, which collapses per-side exit
independence. State the divergence; do not smooth it over.

### THE FIVE ARMS — build and run in this order

| # | Name | Config |
|---|---|---|
| **S1-0** | `…-P1-S1-0` | The primary above. **No Exit Options at all** — no PT, no SL, no trail, no touch. Expiration only. **RUN THIS FIRST.** |
| **S1-a** | `…-P1-S1-a` | Primary + **Stop Loss % = 100**. Nothing else changed. |
| **S1-b** | `…-P1-S1-b` | Primary + **Stop Loss % = 200**. Nothing else changed. |
| **S1-c** | `…-P1-S1-c` | **Overlay**, standalone: **Long Put Spread** (debit), QQQ, `exactly 0 days`, entry **14:00 ET**, **1 contract**, same test period. Strike selection: mirror the primary's method (0.75% OTM short leg reference, $2.00 wide) so the two are comparable. No entry filter. |
| **S1-H** | comparison, not a new backtest | **Combine S1-0 ⊕ S1-c** with the rule `Only open [S1-c] if [S1-0] is [open]`, caps **pinned**. |

**Export the standalone positions CSV for every one of S1-0, S1-a, S1-b, S1-c** before building the
combine — you need S1-0's and S1-c's for trap 2's reconciliation, and all four for the ranking.

### THE COMBINE — S1-H

- Open `/backtests/compare/<S1-0>,<S1-c>`, enable `Combine Results`.
- Add the rule: `Only open [S1-c] if [S1-0] is [open]`. **`open`, not `not open`.**
- **Pin the caps explicitly** rather than accepting defaults. Record the values.
- **Re-read the URL** and paste the full `crules` payload verbatim into your raw capture.
- Export the combined positions CSV.
- **Reconcile**: combined A-rows against S1-0 standalone, combined B-rows against S1-c standalone.
  Report every discrepancy with its date and both rows.

### MEASUREMENT — the denominator is part of the number

Compare by **R (P/L ÷ risk)**, never raw $ (`CLAUDE.md` §4). Report per arm: **N, Exp(R), win rate,
max drawdown in R, worst single R**.

⛔ **For S1-H the denominator is stated explicitly: primary risk + overlay debit, per condor,
ex-artifact.** A combined Exp(R) whose denominator is not written down **is not a result.** Label
the unit on every figure, every time.

**The comparison that decides Phase 1: S1-H against S1-a and S1-b, in R, against S1-0.**

### PHRASING — three things you may not write

1. **No arm is "tested-side-reactive"** and none may be described that way. Nothing in the predicate
   surface reads a sibling position's state. Every hedge arm here is a **fixed-side unconditional
   overlay with a presence gate**.
2. **This is put-side only.** Say so in every write-up. Side selection is not expressible, so
   choosing one is a **choice, not a finding**.
3. **Do not write a recommendation.** These are **T4** figures (`CLAUDE.md` §4 requires T2 with
   n≥100 / 6 months / a regime change for live capital). Report the numbers and stop. Whether the
   `PAPER-ARM-PREAUTH` bar is cleared is **Andy's call on your numbers**, not your verdict.

### DELIVERABLE

`data/captures/<YYYY-MM-DD>-p1-stage1/` — same bundle shape as the 0c bundle: raw capture(s)
unmodified (`01-…`), derived file(s) naming their raw source **and its sha256**, `screenshots/` per
arm and per results screen, **every exported CSV as a raw file**, `README.md` (purpose · timestamp
with TZ offset · file/sha256/what table · the per-arm table with units labelled · the reconciliation
result · the verbatim `crules` payload · the Iron-Condor-vs-paired-spreads divergence note ·
`## Docs-vs-render deltas`), and `SHA256SUMS.txt` over everything.

### PROHIBITIONS

- No git: no `add`, `commit`, `push`, no branches. **Andy runs every commit.**
- Touch nothing outside the new bundle directory.
- Do not edit `CLAUDE.md`, `docs/build-plan.md`, any spec, or any ruling.
- **No `Create Bot`. No Stage 2** — no time sweep, no size-ratio sweep, no call side, no cutoff.
- **Never run a script that re-executes a prior capture sequence.** On 2026-09-17 `/tmp/oa_shots.mjs`
  re-ran its built-in sequence and overwrote 8 PNGs inside an already-verified bundle. Scope every
  screenshot script to this run's directory before you invoke it.
- **Stop conditions — no retries past these:** 401/403/429 · an unrecognized response shape · UI
  numbers disagreeing with each other · a URL containing `/login` · any terms or payment prompt ·
  **anything indicating a live (non-PAPER) account.**

### REPORT

The five arms with N / Exp(R) / win rate / max DD in R / worst R, **units labelled**; the S1-H
denominator written out; the reconciliation result for the combine; the verbatim `crules` payload;
the bundle path; and **the refusals.** A run with no refusals in a boundary this tight is more
suspicious than one with several.

**Stop after Stage 1. Do not start Stage 2 in this session.**
