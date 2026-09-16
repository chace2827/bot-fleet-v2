# G5 redefinition + brief config repairs — Claude Code hand-off

*Written 2026-09-16 (Cowork). Authority: `R-2026-09-16-G5-AUDIT-REDEFINITION` (Andy, go-live
gate) and `R-2026-09-16-BRIEF-CONFIG-REPAIRS` (Andy instructed; implementation derived under
`R-2026-08-31-DERIVED-RULING-AUTHORITY(b)`). Both in `docs/RULINGS.md`. Doctrine amended in
`docs/evidence-standards.md` §6. **This spec adds no decision** — where it and a ruling differ,
the ruling wins.*

**Lane:** Claude Code (`CLAUDE.md` §7 — code). Cowork wrote the rulings and docs; it does not
touch these scripts.

---

## Task 1 — `daily_brief.py`: comment-skipping config loader

**Defect.** `data/bots_config_v2.csv` opens with a 137-line comment banner. `csv.DictReader`
takes line 1 as the header, so the loader's schema tests (`"bot" in _hdr`, and
`"name" in _hdr and (_MECH & set(_hdr))`) both fail against nonsense fieldnames and
`cfg_blind_reason` prints a defect that is not the real one.

**Change.** Before constructing the `DictReader`, drop leading lines whose first character is
`#`. Do not strip the banner from the CSV on disk — it is that file's correction-record
convention (`CLAUDE.md` §5 condition 2).

**Do not claim this lights G5.** After the skip the true header is
`object_kind,name,oa_id,version,attached_to,input_id,input_type,input_label,input_default,a7_hash,captured,layer2_status`,
which carries none of `_MECH = {filter, entry_time, profit_target, reentry}`. The loader stays
CONFIG-BLIND — correctly. Update `cfg_blind_reason` to state the real position: schema carries no
graded mechanic columns, and coverage is 10 of 43 roster bots.

**Acceptance.**
- `python3 -c "import scripts.daily_brief"`-level unit or a fixture asserting the loader returns
  the line-138 fieldnames for a banner-prefixed file.
- A fixture with a banner **and** mechanic columns returns a populated `cfgs` — proving the skip
  works and the schema test is what gates, not the parser.
- On the live file, the printed reason names the schema, not the phantom header.

## Task 2 — `daily_brief.py`: split the card, ungate the hedge clinic

**Defect.** `for bot in (sorted(by_bot) if cfgs else [])` empties `cards`, `hedge_clinic` **and**
`grades` whenever the config is blind. `data/brief/2026-09-16_brief.json` carries
`cards: []`, `hedge_clinic: []`, `grades: {green: 0, amber: 0, red: 0}` — and every brief since
the loop began does the same. The instruction-mirror card and the hedge clinic are both named in
`docs/daily-loop-spec.md` as having survived the 2026-07-31 merge.

**Change.** Iterate ON bots with trades that day regardless of `cfgs`. Inside `build_card`, split:

| rows | source | when rendered |
|---|---|---|
| Filter · Entry · Profit target · Re-entry, and `compliance_pct` | `cfgs` | only when `cfgs` is non-empty |
| breach lines · naked losses · hedge clinic · `day_pnl` · `grade` | `trades.csv` + `bots_meta.csv` | whenever the bot traded |

With `cfgs` empty: `compliance_pct = None`, `n_applicable = 0`, `n_pass = 0`. **Never 0%, never
100%.** `hard_fail` currently keys on Filter/Entry/Hedge — with config blind, only the Hedge row
exists, so `grade` must be derived from the rows that actually rendered; a card that graded no
config rows must not silently grade green.

**Acceptance.**
- Re-running the 2026-09-16 brief yields `hedge_clinic` populated where the ledger shows breaches,
  and `cards` non-empty, with `compliance_pct: null` on every card.
- `compliance.csv` is still written when `cfgs` is non-empty, and is **not** written from a blind
  run (a row with a null `compliance_pct` is not a graded day).
- Existing selftest/fixtures stay green.

## Task 3 — `report.py`: the new G5

**Replace** the `data/compliance.csv` feed, `G5_MIN_DAYS`, `G5_THRESH` and `g5_eval()`.

**New inputs:** `data/execution_audit_findings.csv` (detector frozen v1.1.0, sha
`fdc43d0dcb727556`) and the per-day should-have-fired verdicts
(`data/brief/<day>_p3_verdicts.tsv`). **`compliance.csv` is no longer a gate input** — leave it
written, stop reading it here.

**Rule.** ⭐ **AMENDED by `R-2026-09-16-G5-STREAK-UNIT` — the streak counts CLOSES, not trading
days.** Only 30 of 59 rows in `execution_audit_findings.csv` carry a `date`; `SILENT_BOT`,
`DUPLICATE_ARM` and 9 of 10 `EXPIRY_RATIO_FLIP` rows are **undated window-level findings**, so a
per-day streak is not computable. G5 passes when a bot has **N = 5 consecutive CLEAN CLOSE RUNS** (`R-2026-09-16-G5-N-FIVE`).
A close run is **CLEAN** for a bot when that run's findings name no COUNTING finding for it.
A close run is **DIRTY** for a bot if it carries either:

- severity `RED` or `AMBER` on axis `MECHANICS`; or
- rule `SILENT_BOT` (axis `FIRE`) **and** a should-have-fired verdict of `SUSPECT` for that
  bot-day.

**COUNTING excludes, always** (the carve-out — `R-2026-09-16-G5-AUDIT-REDEFINITION`):

- `DUPLICATE_ARM`, any severity — a property of a **pair**, not of one bot's fidelity.
- `SILENT_BOT` whose verdict is `JUSTIFIED` or `UNEVALUABLE_BY_DESIGN`.
- severity `INFO` (`NEVER_IN_PROFIT`, `CLOSED_AT_MAE`).
- severity `SKIPPED` — reads *"NOT a pass"*; neither pass nor fail.

**⛔ PREREQUISITE — Task 3 is inert without Task 5 below.** `execution_audit_findings.csv` is
regenerated every close and keeps no history, so consecutive closes cannot be read from it. G5
reads the new append-only `data/findings_ledger.csv`, **not** the regenerated file.

**Pending.** A close with no gradeable evidence for a bot is **not a graded close** and does not advance the
streak. All-`SKIPPED`/`INFO` bots accrue zero graded days → `None` (pending) forever, never
`True`. Return the existing `(value, detail)` shape; detail should read like
`"7/10 consecutive clean graded days"` or `"dirty 2026-09-16: EXPIRY_RATIO_FLIP (RED/MECHANICS)"`.

✅ **N = 5 — RATIFIED 2026-09-16 (`R-2026-09-16-G5-N-FIVE`).** Named constant
`G5_STREAK_DAYS = 5`. Paired operating commitment: the close runs every trading day. Earliest
possible pass, streak starting at the 09-17 close: **2026-09-23**.

**Acceptance — the anti-regression test, and it is the point of this task.**
- `IC-SPX-FastPT25-S2` evaluates **G5 = False** on the 2026-09-16 data, blocker citing
  `EXPIRY_RATIO_FLIP`. *The old gate scored this defect class 100% for five days; the new one must
  fail it.* A build where the champion passes G5 today is wrong, whatever else is green.
- A bot carrying only `DUPLICATE_ARM` AMBERs is **not** dirtied by them.
- `DIR-SPX-PutVIX22-SL75` (AMBER `SILENT_BOT` + `JUSTIFIED` verdict) is **not** dirtied.
- A bot with only `SKIPPED` rows returns **pending**, not pass.
- ⛔ **THE NO-TRADE LOOPHOLE — the test that matters most after the champion one.** A bot that is
  OFF, or that simply never fires, generates no counting findings and would otherwise accrue clean
  closes forever and **pass G5 by doing nothing**. That is the old gate's failure mode wearing new
  clothes. Implement the pending rule as *"the detector **evaluated** this bot at this close **and**
  returned no counting finding"* — **not** *"no counting finding was found for this bot"*. Absence
  of a row is absence of evidence. Test: a bot with zero positions in the window returns
  **pending** across five closes, never `True`.
- `grep -c "G5_THRESH\|compliance_pct" scripts/report.py` = **0**.

## Task 5 — `data/findings_ledger.csv` (NEW — build this first)

`R-2026-09-16-G5-STREAK-UNIT`, board **T-67**. Append-only, keyed on
`(close_day, bot, rule, severity)`, written by the close immediately after the audit stage.
Follow the **APPEND/UPSERT** pattern already in `daily_brief.py:upsert_compliance()` and
`hedge_tournament.py` — re-running the same close replaces that close's rows and never
double-counts. This is the file `g5_eval` reads.

⛔ **Do not date the findings inside `execution_audit.py`.** It is the frozen fixed panel
(`daily-loop-spec.md` §0, v1.1.0, sha `fdc43d0dcb727556`) — changing what it emits makes every
banked day uncomparable. The ledger records *when a finding was seen*, a property of the close,
and adds nothing to the detector.

**Expected state on day one:** the ledger has one close in it, so **every bot reads G5 PENDING**
until five closes are banked. That is correct, not a regression.

## Task 4 — the readiness-board blocker string

G5's board column currently renders `·` with `"compliance N/5 graded days (daily brief)"`. It must
render the new detail, and the **first-red-gate** blocker logic must be unchanged — G5 remains
gate 5 of 6 in order.

---

## Out of scope — do not touch
- `execution_audit.py`. It is the **frozen fixed panel** (`daily-loop-spec.md` §0): changing a
  detector rule or threshold makes every banked day uncomparable. G5 consumes its output; it does
  not get a vote in it.
- `data/bots_config_v2.csv` content or banner.
- G4's `<FILL>` RoE $ cap — **NOT an open decision.** Ruled 2026-09-02 as
  `R-2026-09-01-G4-ROE-CAP` (per-bot $15,000 / fleet $35,000 / single-day halt $8,000). What
  remains is propagation: `evidence-standards.md` L277 still prints `<FILL>` (board **T-65**) and
  `report.py` still lacks the cap (board **T-44**). Separate tasks; don't fold them in here.
- The `verify_by` trade-id staleness defect (`execution_audit.py:344`) — **RULED 2026-09-16,
  `R-2026-09-16-VERIFY-BY-NO-STOPGAP`: no stopgap.** It waits for T-10/G-4, the root fix. Do not
  touch those strings. While T-10 is open, every verify is addressed by **bot + open time**, never
  by trade_id.
