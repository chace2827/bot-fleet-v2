# Split (ii) — the Tier-C column contract for `bots_config_v2.csv`

**Status: PREPARED, NOT RULED.** Nothing here is applied. No code, no CSV, no reshaping.
This is the design that gate A9 split (ii) was deferred to; §5 is the list Andy rules on.

**Scope.** How `data/bots_config_v2.csv` comes to carry declared mechanic columns so that
`execution_audit.py`'s five Tier-C rules and `daily_brief.py`'s instruction-mirror grading both
turn ON, from capture, never by hand (`CLAUDE.md` §3 rule 2).

**Split (i) is done and is the floor this builds on.** `execution_audit.py` 1.1.0 and
`daily_brief.py` (2026-08-08) both skip `#` lines, key on `bot` or on `name`+`object_kind=='bot'`,
and degrade loudly. Verified this session: `python3 scripts/execution_audit.py --validate` → **21/21
passed**. That state — *"Structural rules run · Tier C SKIPPED until bots_config_v2.csv carries the
mechanic columns"* — is the acceptable interim (`load_config` docstring, `reactivation-runbook.md`
§3 Step E). This memo is how it ends.

---

## 0. The reconciliation — two consumers, two column sets, one file

| | `execution_audit.py` (Tier C) | `daily_brief.py` (compliance grading) |
|---|---|---|
| gate | `TIERC_RULE_COLUMNS`, per rule | `_MECH = {filter, entry_time, profit_target, reentry}`, any-one |
| columns read | `pt_pct` · `sl_pct` · `time_exit` · `event_backstop` | `filter` · `entry_time` · `profit_target` · `reentry` |
| blind behaviour | SKIPPED BY NAME, per rule | CONFIG-BLIND, whole run |
| cell semantics | three-state via `cell()` — value / `none` / blank | two-state — truthy / falsy, regex-sniffed |
| overlap | `pt_pct` | `profit_target` |

**They overlap in exactly one place and they disagree about it.** `cell()` parses `pt_pct` as a
float in `0 < v <= 5`. `daily_brief` tests `profit_target` with
`re.search(r"pt\s*\d+|\d+%", pt.lower())`.

> ⚠️ **Defect this creates if the two are naively merged.** Point `daily_brief` at `pt_pct` as-is
> and a declared PT of `0.50` matches **neither** alternation branch — no `pt` prefix, no `%` — so
> `pt_prog` is False and the brief takes its `else: # 'none' / ride` branch and grades a PT50 bot
> as a **ride**. A real profit target reads as "none (ride)" and the row still flags `✓`. Renaming
> the column is not sufficient; the *reader* has to change with it.

**RECOMMENDATION — one column set, and `cell()` becomes the shared reader.**
Carry `pt_pct` (machine-legible fraction, three-state). Do **not** carry `profit_target` as a
second, label-shaped column: two columns for one fact is the hand-written-record failure mode with
extra steps. Lift `cell()` + `NONE_TOKENS` into a small shared module both scripts import, so
"blank ≠ none" holds identically on both surfaces. `daily_brief`'s `_MECH` set changes to
`{filter, entry_time, pt_pct, reentry}`. That reader change is **split (iii)** — code, Claude Code's
lane (`CLAUDE.md` §7) — and it is a *precondition* of populating `pt_pct`, not a follow-up.

---

## 1. The column contract

### 1.1 The columns

Additive to the existing header. Existing columns are untouched.

| column | consumer | type | source object |
|---|---|---|---|
| `pt_pct` | audit C1/C2/C4 · brief PT row | fraction, `0 < v <= 5` | exits `profits` |
| `sl_pct` | audit (declared only; no rule reads it yet) | fraction | exits `stoploss` |
| `time_exit` | audit C3/C5 | `HH:MM` wall clock | exits `expdays` + `smexpdays`, **converted** |
| `event_backstop` | audit C5 | `HH:MM` wall clock | trigger `repeat.ntime` |
| `exit_mechanic` | audit C4 gate (**new — see §5 D-1**) | token set | `mechanic_map()` over the decoded field set |
| `filter` | brief Filter row | verbatim gate token | scanner decision nodes |
| `entry_time` | brief Entry row | `HH:MM` | scanner `timeofday` decision node |
| `reentry` | brief Re-entry row | integer cap | bot setting `posLimitDay` |
| `capture_hash` | provenance | sha256 | sha256 of the capture file named in `captured` |

**`capture_file` is NOT added.** `load_config`'s docstring proposes it, but the file already has
`captured`, which holds exactly that. No rule reads either. One fact, one column.

**`event_backstop` stays a separate column from `time_exit`** — different execution class, and C5
exists precisely because the two can disagree (`load_config` docstring; `rule_C5` docstring).

### 1.2 Three-state, per cell

Per `cell()` and the template's own preamble, unchanged and now binding on both consumers:

```
"0.50" / "15:50"   DECLARED       -> the rule evaluates
"none"             REMOVED BY     -> forward rule OFF, INVERSE rule (C4) ON
                   DESIGN
""  (blank)        MISSING DATA   -> rule SKIPPED, blind spot ANNOUNCED. BLANK IS NOT NONE.
row absent         MISSING DATA   -> every Tier C rule SKIPPED for that bot
```

`NONE_TOKENS = {none, removed, n/a, na}`. Anything else is refused, not coerced (`cell()` → `bad`
→ RED). **The `N/A` already sitting in `input_id`/`a7_hash` on the clone rows is a `NONE_TOKEN`** —
harmless there because no rule reads those columns, but it is a reason never to reuse those columns
for a mechanic.

### 1.3 What `none` means, per control clone — and why the inverse rule depends on it

`rule_C4_removed_exit_fired` is *only reachable* because `none` is distinct from blank. It is the
automated form of the control clones' Day-0 proof: their Trades lists must show **no PT row**.

- **`IC-SPX-FastPT25-S2`** (PR-01) — F-C1 applied 2026-08-07. Capture, verbatim:
  `input.exits = { text:"None", profits:"", … expdays:"", … }` with *"`profits` EMPTY. No
  `smprofits` key present at all. **PT25 GONE.**"* → `pt_pct none`, `time_exit none`. Deliberately
  Exit-Option-free (`CLAUDE.md` §5 standing exception).
- **`IC-SPX-FastPT25-S2-130PM`** (PR-02) — same, F-C1 applied both sides 2026-08-08.
- **`QQQ-IC-0DTE-Fortress-NoPT50`** (PR-04) — `pt_pct none` for a *different reason*: nothing was
  removed, nothing was ever there. Capture: *"`exits.profits` is `""` … `0.5` does not occur in
  either routine. Nothing was removed, because nothing was there."* The cell reads the same; the
  provenance line in `captured` is what distinguishes them.
- **`GF-QQQ-IC-Ride`** — `pt_pct none`, and it is the true control: `mechanic_map()` is empty.

**Read as blank, all four become permanent blind spots. Read as a declared value, all four
false-alarm every single day.** That is the whole reason for the third state.

> ⛔ **And this is where `none` alone is not enough — the finding that forces `exit_mechanic`.**
> `GF-QQQ-IC-Trail` has no `profits` (so `pt_pct` would be `none`) but carries
> `tstop {type:tstop, target:40, trail:15}`. C4 probes rungs `0.25 / 0.50 / 0.75` and fires RED at
> **≥3 hits**. A 40%-target trailing stop closes squarely in the 0.25 band. `GF-QQQ-IC-Touch0`
> (`touch {type:usd, value:0}`) and `GF-QQQ-IC-SL100/SL200` have the same exposure. Declaring
> `pt_pct none` on those four turns C4 into a **daily false RED on four of the seven arms**.
> `pt_pct` cannot express "no PT, but a different mechanic governs exits". See §5 **D-1**.

---

## 2. The build path — how the cells get populated without hand-writing

### 2.1 The two capture shapes, and the G2 rider over both

**Shape A — bot-input family (the 7 GF arms).** Exit config lives on a **bot input object**
(`GF_EXITS_PUT` / `GF_EXITS_CALL`); the Open Position action stores only
`{"type":"input","nid":"bot","input":"IN…","text":"GF_EXITS_PUT"}`.

> ⛔ **The G2 rider is binding here and it is two hops deep.** `greenfield-family-spec.md` §1.2:
> *"a capture-diff that reads the Open Position action returns **identical for every arm** … It
> will look like a clean pass. It proves nothing."* Read the **BOT INPUT OBJECT's** decoded value.
> **`oldValue` is never config** — it is a stale pre-link snapshot. Decode the payload; never
> compare rendered labels (N-4: the label drifted `"Profits: 50%…"` → `"Profit: 50%…"` with the
> payload byte-identical). Never key on the string `"fast"` — the internal value is `speedy`.

**Shape B — §2B clones (PR-01/02/03/04).** These carry **no bot inputs and no shared Library
objects**; the exit fields sit inline in each owned scanner's Open Position action.

> 📝 **Reading the action on Shape B is not a G2 violation.** G2 is about which *end of a chain* is
> authoritative. Where there is no chain, the action **is** the per-bot end. A parser that refuses
> to read the action makes the four clones unbuildable; a parser that reads it *when a reference is
> present* is the defect G2 names. The rule the build tool encodes: **if the field's value is a
> `{"type":"input",…}` reference, resolve it to the input object and decode there; otherwise the
> inline value is the value; in neither case read `oldValue`.**

### 2.2 What already exists

`scripts/a_series.py` already contains the decoder: `parse_decoded_fieldset()` → `norm_val()`
(drops the `text` label key, per §1.2 rule 3) → `mechanic_map()` over
`MECHANIC_TRIGGERS = [profits, dprofit, stoploss, dstop, tstop, touch, price, xevents, epsdays]`.
Its module docstring states it reads the bot-input end and *"ignores the action reference and
oldValue."* It also already parses `posLimitDay`, `posLimit`, `status`, `disableExits` and
`backstop_ntime`.

**But `classify_and_parse()` gates on `^BOT_ID` **and** `^BOT GF-QQQ-IC-`** — it is scoped to the
greenfield family by construction, and `a_series.py` is standalone, not wired into `daily.sh`.

**RECOMMENDATION — a new `scripts/build_config.py` that imports those three functions from
`a_series.py` rather than reimplementing them.** One decoder, one place, one set of traps already
paid for. It emits the mechanic columns and a receipt into `data/receipts/`; it never edits the
`#` preamble; it refuses to write a mechanic cell it cannot hash the source of.

### 2.3 Does the capture format carry enough? — **No. One thing is missing, and it is not the bookmarklet.**

- **Shape A: YES, today.** The GF captures carry a `DECODED FIELD SET` block in a fixed shape
  (`profits 0.5` · `expdays 0.01` · `smexpdays {…}`), already machine-parsed by `a_series.py`.
- **Shape B: NO.** PR-04's capture records the same facts **in prose**, inside a `--- SPEC CHECK ---`
  narrative: *"`exits.expdays 0.01`, text "Expiration: 10 minutes", `smexpdays {"text":"Market",…}`
  on both sides."* True, first-hand, and **not parseable without regexing English**.
- **`filter` / `entry_time`: prose too.** PR-02's capture has the gate as a tree line —
  `decision stockchangepct(gt -0.75) > Yes > decision stockchangepct (lt 0.75) > Yes > decision
  FOMC-today > No > decision timeofday "after 1:30pm"`. PR-04's capture has **no entry-gate line at
  all** (its scanners were unedited, so the tree was never dumped).

**The missing thing is a capture-TEMPLATE field, not a bookmarklet field.** The bookmarklet dumps
`document.body.innerText`; the decoded exits come from `a5.bots.acedit.routine` via Chrome-direct
read, which is already the ritual. The change is to make every per-bot capture carry the same three
fixed blocks the GF captures already carry:

```
--- DECODED EXITS ---        one line per field, `name value`, both sides, Shape A and B alike
--- ENTRY GATE ---           the scanner decision-node chain, verbatim
--- SETTINGS ---             posLimitDay · posLimit · status · disableExits · trigger ntime
```

That is an `oa-ops-runbook.md` §1 change (a capture-ritual amendment) — **gated**, per `CLAUDE.md`
§5: it changes a spec, not a falsified claim.

### 2.4 The nine

`decision-card-2026-08-08.md`: *"The nine leave-in-place · **UNVERIFIED** — no per-bot capture
exists (slot 6)"* and *"No bot page has ever been opened on any of them. Slot 6 is the whole of
this gap."*

**Consequence, stated rather than worked around: the nine get no rows, and therefore blank cells,
and therefore per-bot SKIPPED rows on every Tier-C rule that has a column.** That is the design
working — an announced blind spot — not a gap to paper over. **Nothing is inferred from
`data/archive/bots_config.csv`**, which is the discredited hand-written record (wrong on 3 of 4
audited bots). A row appears for one of the nine only when slot 6's worklist runs and produces a
capture. Until then their absence *is* the finding.

---

## 3. Migration — additive, per-column, never a flag day

The v1.1.0 loader makes this free: `TIERC_RULE_COLUMNS` gates **per rule**, and
`daily_brief`'s `_MECH` gate is **any-one-of**. So rules light one at a time.

| step | columns added | rules that turn ON |
|---|---|---|
| 1 | `pt_pct`, `exit_mechanic`, `capture_hash` | `PT_DECLARED_NOT_TAKEN` · `PT_NEVER_FIRES` · `REMOVED_EXIT_FIRED` |
| 2 | `time_exit` | `TIME_EXIT_MISSED` |
| 3 | `event_backstop` | `BACKSTOP_CAUGHT_IT` |
| 4 | `filter`, `entry_time`, `reentry`, `sl_pct` | brief grading leaves CONFIG-BLIND |

**Which bots light up first: eleven.** The 7 GF arms + 4 clones (PR-01 champion, PR-02 130PM,
PR-03 pilot `QQQ-IC-0DTE-Fortress`, PR-04 NoPT50). PR-01/02/04 already have rows; the 7 arms have
rows; **PR-03 has a bot and a capture but no row in this file** — adding its row is part of step 1.

**How the blind spot MOVES, and the one place it gets quieter.** Today, one loud fleet-level row
per rule: `(fleet) … SKIPPED BY NAME … the declared config's schema does not carry what this rule
reads`. The moment a column exists, that row disappears and is replaced by **per-bot** `missing`
rows from `_tierC_cell_guard`. Measured this session against a synthetic post-split-(ii) schema on
the archive ledger: `tierc_ran = True`, and **30 per-bot `SKIPPED` rows** each for
`PT_DECLARED_NOT_TAKEN` and `TIME_EXIT_MISSED`.

> ⚠️ **Therefore: never add a column in the same commit as zero populated cells.** A column with no
> rows trades one loud banner for N quiet ones. Add the column **and** the eleven rows together.

---

## 4. Acceptance

### 4.1 ⛔ FINDING — the frozen 21/21 matrix **breaks on step 1** unless V7 is re-pointed first

`validate()` line 861 runs the detector against **the real file**:

```python
_, findings, has_cfg, _ = run(ledger, os.path.join(D, "bots_config_v2.csv"), …)
```

and V7 asserts `(not has_cfg) and skipped_c >= {…}`. The third return value is `tierc_ran`, not
"a config exists". **Measured this session** (synthetic schema, archive ledger, real code, no file
touched): adding the mechanic columns gives `tierc_ran = True` → **V7 FAILS**. Matrix goes 20/21.

**RECOMMENDATION — preserve V7's semantics by decoupling it from the live file, and harden it.**
V7's meaning is *"the detector knows what it cannot see"* — that must not depend on today's state
of a data file. Re-point V7 at a deliberately non-existent temp path, then add two siblings:

- **V7a** — no config file at all → all five Tier-C rules `SKIPPED` (today's V7, made hermetic).
- **V7b** — config present, schema lacks the mechanic columns → `SKIPPED BY NAME` (the split-(i)
  branch, currently untested by any V).
- **V7c** — columns present, bot absent from the config → that bot `SKIPPED` `missing` (the
  split-(ii) branch).

Cost: three lines of test wiring, no detector-rule change. **`VERSION` is bumped and `--validate`
re-run before it ships**, per the frozen-file banner. Also worth fixing in the same pass: `has_cfg`
is a misleading name for `tierc_ran` at lines 778/784/830/1089.

### 4.2 What must hold, unchanged

- **21/21** (V1–V19 + V15) after the V7 re-point. V11–V14 already exercise the three-state cell
  against synthetic configs keyed on `bot`; the `name`+`object_kind` path is untouched by them and
  stays untouched.
- **V7 semantics preserved**: no Tier-C rule ever silently passes. Every non-evaluable cell yields
  a row naming *which* bot, *which* column, and *why*.
- **Frozen 35-row fixture unchanged** — a test asset that survives the cutover, not a reporting
  input.
- **`REDUCED` vs `FULL` still reported** in the run header.
- Detector **rules** unchanged. Split (ii) is a data-contract change; the only code changes are the
  shared `cell()` (split iii), the C4 gate (§5 D-1), and the V7 re-point.

### 4.3 Worked rows — as they would actually read

New columns only (existing columns unchanged). `‹blank›` is an empty cell, and it is not `none`.

**`IC-SPX-FastPT25-S2-130PM` (PR-02) — everything removed by design**

| pt_pct | sl_pct | time_exit | event_backstop | exit_mechanic | filter | entry_time | reentry | capture_hash |
|---|---|---|---|---|---|---|---|---|
| `none` | `none` | `none` | `none` | `none` | `Range075` | `13:30` | `10` | `d542587ffa4b012f…` |

Evidence, all from `data/captures/2026-08-08-clones/PR-02-clone-final-2026-08-08.txt`:
F-C1 applied both sides → Exit Options None → `pt_pct`/`time_exit`/`exit_mechanic` `none`. Four
automations, none a repeating trigger → `event_backstop none`. Gate chain
`stockchangepct(gt -0.75) … (lt 0.75)` → `filter Range075` (the literal token `daily_brief` tests
for with `"range075" in filt.lower()`). `timeofday "after 1:30pm"` → `entry_time 13:30`.
`posLimit 10 at once / 10 per day` → `reentry 10`.
**`exit_mechanic none` + `pt_pct none` = C4 armed.** This bot's Day-0 proof is now automated.

**`QQQ-IC-0DTE-Fortress-NoPT50` (PR-04) — declared time exit, declared backstop, and one honest blank**

| pt_pct | sl_pct | time_exit | event_backstop | exit_mechanic | filter | entry_time | reentry | capture_hash |
|---|---|---|---|---|---|---|---|---|
| `none` | `none` | `15:50` | `15:52` | `expdays:0.01` | `‹blank›` | `‹blank›` | `2` | `e58db65fff3f0c69…` |

Evidence, all from `data/captures/2026-08-08-clones/PR-04-clone-final-2026-08-08.txt`:
*"`exits.profits` is `""` … Nothing was removed, because nothing was there"* → `pt_pct none`.
*"`exits.expdays 0.01`, text "Expiration: 10 minutes""* → `time_exit 15:50` (see D-2).
Trigger `ntime 1552` → `event_backstop 15:52`. `DAILY POSITIONS 2 per day` → `reentry 2`.
**`filter` and `entry_time` are BLANK because this capture never dumped the scanner tree** — the
scanners were inherited unedited. Blank, not `none`: the brief will report those two rows
CONFIG-BLIND rather than grade them, and that is correct. They fill when §2.3's `ENTRY GATE` block
lands.
**With `time_exit 15:50` and `event_backstop 15:52`, C5 — the $9,618 rule — is live on this bot.**

---

## 5. Open decisions — Andy's

**D-1 — `exit_mechanic`: add the column and gate C4 on it, or leave C4 to false-RED four arms?**
`pt_pct none` currently means both "removed by design" and "absent", and C4 cannot tell them apart
on Trail / Touch0 / SL100 / SL200.
> **RECOMMENDATION: add it.** One column, populated verbatim from `mechanic_map()`; `pt_pct` and
> `sl_pct` derived deterministically from the same field set (`profits`→`pt_pct`,
> `stoploss`→`sl_pct`). C4's gate becomes `pt_pct == 'none' AND exit_mechanic == 'none'`. The
> alternative — a fourth cell state — needs the same extra column to say *what* governs instead,
> and buys a new token that `cell()` would have to learn.

**D-2 — `time_exit`: store the wall clock, or store `expdays` raw?**
OA stores a *duration before expiry* (`expdays 0.01`, label "Expiration: 10 minutes"). C3 compares
`close_date[11:16] > te` and C5 compares `te < ct <= bs` — both need a **wall clock**. Converting
needs the underlying's expiry close, which is **not the same for SPX and for QQQ**.
> **RECOMMENDATION: store `HH:MM`.** Put the conversion in `build_config.py` against a declared
> per-underlying expiry-close constant, and write the raw `expdays` + the constant used into the
> receipt in `data/receipts/`, so the derivation is auditable without a second column. **The
> constant itself is a config fact and must come from OA, not from arithmetic** — until it is read
> first-hand, `time_exit` is populated only for QQQ bots and left **blank** for SPX ones.

**D-3 — the `filter` token: verbatim gate text, or a normalized token?**
`daily_brief` only lights the verifiable branch on `"range075" in filt.lower()`; a verbatim
`stockchangepct(gt -0.75)…` would never match and every filter row would degrade to `·`.
> **RECOMMENDATION: a normalized token (`Range075`), with the verbatim chain in the capture.** The
> CSV cell is a *contract with the grader*; the capture is the evidence. Declare the token
> vocabulary in the file's `#` preamble so a new token is a visible addition, not a silent typo.

**D-4 — per-bot missing-skip volume: all ledger bots, or ON bots only?**
Measured: 30 per-bot `SKIPPED` rows per rule against the archive ledger. At Day-0 the nine
leave-in-place bots would each emit one per rule, every day, until slot 6 runs.
> **RECOMMENDATION: keep them all.** They are correct, they are the pressure to close slot 6, and
> suppressing them is how a blind spot becomes silence. If the brief gets noisy, collapse the
> *rendering* into one line naming the bots — never the detector's output.

**D-5 — split (iii): does `cell()` move to a shared module now, or does `daily_brief` keep its own reader?**
Populating `pt_pct` without changing `daily_brief`'s reader ships the §0 defect (a PT50 bot graded
as a ride, flagged `✓`).
> **RECOMMENDATION: shared module, and it lands BEFORE any `pt_pct` cell is written.** Order
> matters: reader first, column second, rows third. Code is Claude Code's lane (`CLAUDE.md` §7).

**D-6 — the capture-template amendment (§2.3) — three fixed blocks in every per-bot capture.**
This is an `oa-ops-runbook.md` §1 change and is **gated** under `CLAUDE.md` §5: it changes a
procedure, not a falsified claim.
> **RECOMMENDATION: amend, and make it retroactive only where cheap.** Shape A captures already
> satisfy it. For Shape B, the blocks are re-derivable at the *next* capture of each clone; do not
> re-open OA solely to backfill. Bots without the blocks keep blank cells and announced skips.

**D-7 — `sl_pct` has no rule reading it. Carry it anyway?**
> **RECOMMENDATION: yes, carry it.** SL100 and SL200 are two of the seven arms and their whole
> distinctness is `stoploss 1` vs `stoploss 2`. A declared column with no consumer is a design
> commitment; an undeclared mechanic is a blind spot nobody is looking for. It costs one column and
> `cell()` already parses it (`0 < v <= 5` admits `2.0`).

---

## Provenance of every claim in this memo

First-hand this session, by direct `device_bash` read of the working tree:
`scripts/execution_audit.py` (`load_config` docstring · `cell()` · `_tierC_cell_guard` ·
`TIERC_RULE_COLUMNS` · `rule_C1`–`rule_C5` · `run()` · `validate()` L861 · V7 L903–907) ·
`scripts/daily_brief.py` (L146–293 graded rows · L361–396 config load · `_MECH`) ·
`scripts/a_series.py` (docstring · L65–69 · `parse_decoded_fieldset` · `mechanic_map` ·
`parse_bot_capture` · `classify_and_parse`) · `data/bots_config_v2.csv` (full header + preamble +
all 12 rows) · `data/bots_config_v2.template.csv` · `docs/greenfield-family-spec.md` §1.2 ·
`docs/decision-memo-2026-08-04.md` D-1 rider · `docs/capture-architecture-2026-07-30.md` ·
`docs/oa-ops-runbook.md` §1.2–1.6 · `docs/decision-card-2026-08-08.md` (slot 6 / the nine, read
only) · `docs/pilot-clone-card-qqq-fortress.md` · the PR-02 / PR-04 / PR-01-post-F-C1 / GF-PT50
capture files. Two runs: `execution_audit.py --validate` → 21/21; one synthetic-schema probe
against the archive ledger through the real `run()` (temp file, deleted; **no project file
written**).

**Nothing in this memo has been applied.** No CSV column exists yet. No code has changed.
