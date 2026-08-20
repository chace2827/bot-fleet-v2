# SLICE-SPEC C — bot-disposition contradictions (slice unit = ONE BOT)

**Scope, ruled by Andy 2026-08-20 (scope-down from spec A):**
> Find doc-vs-doc contradictions that change **which bots run or are archived.**

Spec A (2310 rules) is **HELD, not cancelled** — it produces a TSV and no one could name the
decision that changes because of it. This spec is the row-14 class and nothing else: the class that
already surfaced five QQQ hedge bots whose status depends on which document you read.

## §1 — Slice unit and the roster

**One slice = one bot.** The roster is `docs/build-plan.md` §2, which states its own counts:
**§0 Delete 2 · §A Archive 20 · §B Clone→spec→archive original 4 · §C Leave in place 9 = 35**,
plus §D fresh builds (5–8, amended to 8) which do not yet exist and are **out of scope**.

⛔ **The roster must be curated by hand before dispatch, and it is the first acceptance gate.**
Three counts exist and none of them agree: build-plan states **35** dispositioned bots; the
manager's extractor found **28** named tokens; mine found **25**, then **40** once abbreviated
`-Suffix` forms were expanded — and that 40 included `bots_meta`, `data/archive/`, two ruling ids
and the fragment `opened this side today`. §C's 7 mirrors (`3DTE $140-$350`, `Nigiri-Paper-v1`,
`QQQ long call`, `Friday 14 DTE Broken Wing IB (B-70)`, `Trendy-Paper-v1`,
`60min-ORB-10W-Paper-v1`, `Tasty Condor`) are OA display names that no bot-name regex will ever
match. **A regex cannot produce this list.** Curate the 35 by hand against build-plan's own four
sub-lists, commit it as `data/wave3-roster-2026-08-20.tsv` (`bot`, `section`, `stated_disposition`),
and reconcile 2/20/4/9 before any slice is dispatched. A roster that does not reconcile is a
foreman error, exactly as a missing slice pack is.

## §2 — Source scoping (this is a rule, not a convenience)

**In scope:** `docs/*.md` and root `*.md` — prose that *states a disposition*.
**Out of scope, and each for a reason from `CLAUDE.md`:**
- `data/archive/**` — the frozen v1 ledger, §3: never a reporting input, history only.
- generated output — `data/brief/**`, `STATUS.md`'s computed body, `dashboard.html`: these report
  state, they do not state a disposition, and a contradiction with them is a pipeline bug.
- `docs/rules-catalog.md` — it is an *index of* the other docs. Counting it doubles every rule it
  quotes.

The pilot bot appears in **90 files** but only **18 prose docs**. Ungated grep is not a slice.

## §2.5 — DOCUMENT-LEVEL GATE. Run this once per doc, before any bot row inside it.

⛔ **Added 2026-08-20 after the pilot.** Test 1b (cutover supersession) applies to the **document**,
not to each bot row inside it. Run it once per in-scope doc, first:

1. Is the doc's own date **before 2026-07-30**? (filename date, else its `Created`/`Generated` line.)
2. Does the block you are reading state a **pre-cutover P/L or trade-count figure**, or name a v1
   ledger artifact, or an item on `CLAUDE.md` §1's out-of-scope list?

Both true → **the whole block is `SUPERSEDED-BUT-STILL-READS-AS-LIVE`**, recorded once, and its bot
rows are **not adjudicated individually**.

*Worked example:* `docs/strategy-taxonomy.md` is dated **2026-06-08** and its roster table states
pre-cutover P/L for every bot in it. The entire roster block is superseded. Without this gate, spec
C re-litigates the same v1 table **once per bot, 28 times**, and calls it 28 findings.

## §2.6 — EVERY CITATION MUST RESOLVE

⛔ **The foreman's own pilot cited `CLAUDE.md §3.5`. That section does not exist** — `CLAUDE.md`
has `## 3. Source-of-truth hierarchy` with numbered items, and the rule meant was **§3 item 5**
("Narrative docs never carry numbers"), at line 37. The idea was right and the citation was
invented. **That is precisely the defect class this effort exists to find, produced by this effort.**

So: **before writing any citation, resolve it.** `grep -n` the section marker in the named file and
record the line. A citation that does not resolve to a line is not evidence, and the row is
`UNRESOLVED`, never "close enough". This applies to `§`-style references, ruling ids, and file:line
anchors alike.

## §3 — Per bot, the decision procedure

For each doc naming the bot (`grep -l` over the in-scope set):
1. **Disposition** — what does this doc say happens to this bot? One of: `LIVE/ON` · `ARMED` ·
   `ARCHIVE` · `DELETE` · `CLONE-THEN-ARCHIVE-ORIGINAL` · `LEAVE-IN-PLACE` · `UNSIGNED/GATED` ·
   `NONE` (names it without stating a disposition — most mentions).
2. **Anchor it.** `python3 anchor.py <doc> "<the quoted claim>"` — declared sha
   `973b68058e28b18b42ecbabb0641a923b4f2518358683c3df0f12c7341daa6e5`, asserted in-clone before the
   first call. Record `trimmed` on every row. `AMBIGUOUS` / `TOO_SHORT` / `TRIM_EXCEEDED` →
   `UNRESOLVED`, never a guess. `dead` remains the anchor-absent branch only.
3. **CONTRADICTS-CANDIDATE** where two in-scope docs state dispositions that cannot both hold.
   The test is unchanged and it is a writing test: **one sentence naming a concrete situation in
   which following one doc violates the other.** No sentence → not a contradiction. Topic overlap
   is not contradiction.
4. **Deference check** — if a doc defers to an authority ("superseded by X", "per Y"), confirm that
   authority still stands. *A rule can be undermined by the invalidation of the authority it defers
   to — neither a banner over it nor a contradiction on its face.*
5. ⛔ **FALSIFIED-BY-DATA — check this BEFORE the precedence ladder, and rank it above it.**
   **Precedence is for two defensible readings. It is not for one wrong fact.** If a doc states a
   *number* about a bot — P/L, trade count, win rate, position count — adjudicate it against the
   numeric sources of truth, not against the other document:
   - `data/trades.csv` — the post-cutover working ledger;
   - `STATUS.md` — the reporting surface built from it.

   If the ledger has **no row** for that bot, or `STATUS.md` reports `insufficient data`, then the
   doc's figure is **`FALSIFIED-BY-DATA`**, and that is the verdict — not a precedence winner.

   *Worked example, and the reason this class exists:* `strategy-taxonomy.md:140` states
   `| QQQ-IC-0DTE-Fortress-NoPT50 | Experiment (no-PT) | QQQ | +$2,760 | ON |`. `data/trades.csv`
   holds **71 rows across 15 bots and zero for this one**; `STATUS.md:237` reads
   `| … | 0 | 0 | 0 | insufficient data | insufficient data |`, and `STATUS.md:14` puts the bot on
   the **UNSIGNED — DO NOT SWITCH ON** list. The same is true of every P/L in that block
   (`+$2,975`, `+$908`, `−$445`, `−$450`) — **all five name bots with no post-cutover ledger row.**

   A precedence verdict here says "prefer the inbox" and **leaves the false number sitting in a
   live document.** Only the factual verdict closes it: *":140 states a number that is not true."*

6. **Winner** by the §2 precedence order (RULINGS → `CLAUDE.md` §3 hierarchy → frozen build-plan →
   more recent dated banner → more specific) — **used only when both readings are defensible.**
   Agents render **no terminal verdict**: candidates only, pass 2 rules. `FALSIFIED-BY-DATA` is
   reported with its two numeric citations and is not a candidate — the data already settled it.

## §4 — Output contract

`_wave3/bots/<bot>.tsv`, one row per in-scope doc naming the bot. No two slices write one file.
`falsified_by` carries the two numeric citations (`data/trades.csv` row count, `STATUS.md:<line>`)
whenever the verdict is `FALSIFIED-BY-DATA`, and `-` otherwise.

```
bot	doc	disposition	anchor_line	trimmed	quote	contradicts_doc	concrete_case	winner	falsified_by	notes
```

**Acceptance, derived and able to fail** — last two lines:
```
#RECONCILE docs_in_scope=<a> rows_written=<b> candidates=<c>
#TOOLS anchor_py_sha256=<shasum of anchor.py>
```
`a == b` must hold. `docs_in_scope` is recomputed by the agent from its own `grep -l`, never copied
from the prompt.

## §5 — Dispatch law (unchanged, all measured)

Invoke `~/bin/devin-free` literally · never `-p` · never `$DEVIN` · never `-r` · `--workspace`, not
`cd` · `--permission-mode dangerous` (`smart` is advertised in `--help` and dead) · **exit 0 is not
acceptance** — file presence + `#RECONCILE` + `#TOOLS` only · **NEVER KILL A SESSION**: a killed or
lingering session keeps `metadata=NULL` forever and the acu evidence is destroyed permanently.
Lingering is wait-and-report. A NULL row is "two evidence surfaces dropped to one", never `$0`.

## §6 — Pilot gate, still binding

One bot by hand, then one agent on the same bot, compare, before any fan-out. **It has caught
something every single round** — four spec defects, an uncapped backoff that had never fired, and
an ignored `Status` column.

**Pilot bot: `QQQ-IC-0DTE-Fortress-NoPT50`** — chosen because it is **armed ON while on the
unsigned list** (inbox I-06, AUTOS ON / EXITS ON in two independent first-hand captures 48h apart).
If the docs disagree about that bot, it is a live control failure with money on it, not a
documentation defect.
