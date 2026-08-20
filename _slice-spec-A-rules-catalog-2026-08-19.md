# SLICE-SPEC A — triage `docs/rules-catalog.md` (2310 rules, 56 slices)

**Written by the wave-3 foreman, 2026-08-19. Read this file in full before executing a slice.
Do not ask a question — if the spec does not answer it, you write `UNRESOLVED`, per §5.**

Basis: `docs/rules-catalog.md` at master `1d56fc0`. Every count in this spec was re-derived, not
copied: 2310 rules, two independent ways (table-row parse = per-source-doc declared sum = 2310, and
every one of the 56 sections reconciles individually). A third structural check: the file has 2422
lines beginning `|` = 2310 data rows + 56 header rows + 56 separator rows. **If your slice's
numbers do not reconcile, the slice is wrong — say so, do not adjust.**

## §1 — Slice unit and the full slice list

**Slice unit = one source document = one `### ` section of the catalog.** 56 slices, all named.
Line ranges are as the file stands at `1d56fc0`; they are given so you can find your section, but
you must locate it by its `### ` heading text, not by line number.

| Slice | Source doc (the `### ` heading) | Declared rules | Lines | Output file |
|---|---|---|---|---|
| A01 | `CLAUDE.md` | 91 | 44–139 | `_wave3/rules/A01__CLAUDE_md.tsv` |
| A02 | `README.md` | 3 | 140–147 | `_wave3/rules/A02__README_md.tsv` |
| A03 | `STATUS.md` | 39 | 148–194 | `_wave3/rules/A03__STATUS_md.tsv` |
| A04 | `docs/state.md` | 55 | 195–254 | `_wave3/rules/A04__docs__state_md.tsv` |
| A05 | `docs/build-plan.md` | 34 | 255–293 | `_wave3/rules/A05__docs__build-plan_md.tsv` |
| A06 | `docs/reactivation-runbook.md` | 91 | 294–392 | `_wave3/rules/A06__docs__reactivation-runbook_md.tsv` |
| A07 | `docs/oa-ops-runbook.md` | 69 | 393–466 | `_wave3/rules/A07__docs__oa-ops-runbook_md.tsv` |
| A08 | `docs/pilot-clone-card-qqq-fortress.md` | 22 | 467–493 | `_wave3/rules/A08__docs__pilot-clone-card-qqq-fortress_md.tsv` |
| A09 | `docs/daily-loop-spec.md` | 52 | 494–550 | `_wave3/rules/A09__docs__daily-loop-spec_md.tsv` |
| A10 | `docs/evidence-standards.md` | 108 | 551–663 | `_wave3/rules/A10__docs__evidence-standards_md.tsv` |
| A11 | `docs/pre-registration-ledger.md` | 97 | 664–765 | `_wave3/rules/A11__docs__pre-registration-ledger_md.tsv` |
| A12 | `docs/oa-platform-reference.md` | 87 | 766–857 | `_wave3/rules/A12__docs__oa-platform-reference_md.tsv` |
| A13 | `docs/oa-platform-reference-v3-DRAFT.md` | 6 | 858–868 | `_wave3/rules/A13__docs__oa-platform-reference-v3-DRAFT_md.tsv` |
| A14 | `docs/hedge-research.md` | 33 | 869–906 | `_wave3/rules/A14__docs__hedge-research_md.tsv` |
| A15 | `docs/capture-architecture-2026-07-30.md` | 10 | 907–924 | `_wave3/rules/A15__docs__capture-architecture-2026-07-30_md.tsv` |
| A16 | `docs/backtest-ingest-protocol.md` | 25 | 925–954 | `_wave3/rules/A16__docs__backtest-ingest-protocol_md.tsv` |
| A17 | `docs/directional-oa-build-sheet.md` | 34 | 955–993 | `_wave3/rules/A17__docs__directional-oa-build-sheet_md.tsv` |
| A18 | `docs/lean-backtesting-reference.md` | 17 | 994–1015 | `_wave3/rules/A18__docs__lean-backtesting-reference_md.tsv` |
| A19 | `docs/quantconnect-lean-exploration-brief.md` | 18 | 1016–1038 | `_wave3/rules/A19__docs__quantconnect-lean-exploration-brief_md.tsv` |
| A20 | `docs/oa-mirror-reference.md` | 52 | 1039–1095 | `_wave3/rules/A20__docs__oa-mirror-reference_md.tsv` |
| A21 | `docs/strategy-taxonomy.md` | 16 | 1096–1116 | `_wave3/rules/A21__docs__strategy-taxonomy_md.tsv` |
| A22 | `docs/cross-functional-reference.md` | 20 | 1117–1141 | `_wave3/rules/A22__docs__cross-functional-reference_md.tsv` |
| A23 | `docs/oo-trial-backtests.md` | 16 | 1142–1162 | `_wave3/rules/A23__docs__oo-trial-backtests_md.tsv` |
| A24 | `docs/ic-trailing-stop-backtest.md` | 29 | 1163–1199 | `_wave3/rules/A24__docs__ic-trailing-stop-backtest_md.tsv` |
| A25 | `docs/history-index.md` | 6 | 1200–1210 | `_wave3/rules/A25__docs__history-index_md.tsv` |
| A26 | `docs/session-log.md` | 175 | 1211–1393 | `_wave3/rules/A26__docs__session-log_md.tsv` |
| A27 | `data/archive/README-v1-ledger.md` | 9 | 1394–1407 | `_wave3/rules/A27__data__archive__README-v1-ledger_md.tsv` |
| A28 | `data/receipts/README.md` | 8 | 1408–1423 | `_wave3/rules/A28__data__receipts__README_md.tsv` |
| A29 | `docs/decision-memo-2026-08-04.md` | 28 | 1424–1456 | `_wave3/rules/A29__docs__decision-memo-2026-08-04_md.tsv` |
| A30 | `docs/research-loop-review-2026-08-04.md` | 19 | 1457–1480 | `_wave3/rules/A30__docs__research-loop-review-2026-08-04_md.tsv` |
| A31 | `docs/sprint-2026-08-04.md` | 42 | 1481–1527 | `_wave3/rules/A31__docs__sprint-2026-08-04_md.tsv` |
| A32 | `docs/day0-audit-2026-08-05.md` | 38 | 1528–1570 | `_wave3/rules/A32__docs__day0-audit-2026-08-05_md.tsv` |
| A33 | `docs/day0-release-2026-08-05.md` | 44 | 1571–1619 | `_wave3/rules/A33__docs__day0-release-2026-08-05_md.tsv` |
| A34 | `docs/mirror-funding-memo-2026-08-05.md` | 14 | 1620–1638 | `_wave3/rules/A34__docs__mirror-funding-memo-2026-08-05_md.tsv` |
| A35 | `docs/r-edit-authorization-2026-08-05.md` | 26 | 1639–1669 | `_wave3/rules/A35__docs__r-edit-authorization-2026-08-05_md.tsv` |
| A36 | `docs/decision-card-2026-08-06.md` | 36 | 1670–1710 | `_wave3/rules/A36__docs__decision-card-2026-08-06_md.tsv` |
| A37 | `docs/baseline-forensic-2026-08-07.md` | 17 | 1711–1732 | `_wave3/rules/A37__docs__baseline-forensic-2026-08-07_md.tsv` |
| A38 | `docs/day0-session-pack-2026-08-07.md` | 108 | 1733–1845 | `_wave3/rules/A38__docs__day0-session-pack-2026-08-07_md.tsv` |
| A39 | `docs/exploratory-bots-design-2026-08-07.md` | 56 | 1846–1906 | `_wave3/rules/A39__docs__exploratory-bots-design-2026-08-07_md.tsv` |
| A40 | `docs/g-rulings-card-2026-08-07.md` | 18 | 1907–1929 | `_wave3/rules/A40__docs__g-rulings-card-2026-08-07_md.tsv` |
| A41 | `docs/post-u1-package-2026-08-07.md` | 14 | 1930–1948 | `_wave3/rules/A41__docs__post-u1-package-2026-08-07_md.tsv` |
| A42 | `docs/rebuild-contingency-2026-08-07.md` | 12 | 1949–1965 | `_wave3/rules/A42__docs__rebuild-contingency-2026-08-07_md.tsv` |
| A43 | `docs/research-loop-fix-spec-2026-08-07.md` | 65 | 1966–2035 | `_wave3/rules/A43__docs__research-loop-fix-spec-2026-08-07_md.tsv` |
| A44 | `docs/audit-report-2026-08-08.md` | 7 | 2036–2047 | `_wave3/rules/A44__docs__audit-report-2026-08-08_md.tsv` |
| A45 | `docs/decision-card-2026-08-08.md` | 37 | 2048–2089 | `_wave3/rules/A45__docs__decision-card-2026-08-08_md.tsv` |
| A46 | `docs/evidence-standards-redesign-proposal-2026-08-08.md` | 29 | 2090–2123 | `_wave3/rules/A46__docs__evidence-standards-redesign-proposal-2026-08-08_md.tsv` |
| A47 | `docs/split2-design-2026-08-08.md` | 26 | 2124–2154 | `_wave3/rules/A47__docs__split2-design-2026-08-08_md.tsv` |
| A48 | `docs/pending-tracker-items-2026-08-10.md` | 24 | 2155–2183 | `_wave3/rules/A48__docs__pending-tracker-items-2026-08-10_md.tsv` |
| A49 | `docs/AI Agent Stack.md` | 27 | 2184–2215 | `_wave3/rules/A49__docs__AI_Agent_Stack_md.tsv` |
| A50 | `docs/AI Agentic.pdf` | 1 | 2216–2221 | `_wave3/rules/A50__docs__AI_Agentic_pdf.tsv` |
| A51 | `docs/comparative-machinery-spec.md` | 108 | 2222–2334 | `_wave3/rules/A51__docs__comparative-machinery-spec_md.tsv` |
| A52 | `docs/greenfield-family-spec.md` | 144 | 2335–2483 | `_wave3/rules/A52__docs__greenfield-family-spec_md.tsv` |
| A53 | `docs/oa-export-schema.md` | 27 | 2484–2515 | `_wave3/rules/A53__docs__oa-export-schema_md.tsv` |
| A54 | `docs/oa-reconciliation-report.md` | 18 | 2516–2538 | `_wave3/rules/A54__docs__oa-reconciliation-report_md.tsv` |
| A55 | `docs/research-loop-spec.md` | 37 | 2539–2580 | `_wave3/rules/A55__docs__research-loop-spec_md.tsv` |
| A56 | `docs/track-b-arms-spec.md` | 66 | 2581–2742 | `_wave3/rules/A56__docs__track-b-arms-spec_md.tsv` |

**Special case — slice A50 (`docs/AI Agentic.pdf`, 1 rule).** Its single row is a placeholder
recording that the file could not be read; it is not a rule. Bucket it `dead` with
`notes=placeholder-not-a-rule`. It still counts as 1 row for the reconciliation in §4.

## §2 — The decision procedure

Run tests **in this order** and stop at the first that fires. Exactly one bucket per row.
**A bucket you cannot produce the required evidence for is a bucket you may not assign.**

### Test 0 — ANCHOR. Does the rule's textual basis still exist?

**You do not derive the fragment. `anchor.py` does.** Pass it the source doc and the row's
**raw `Source quote/anchor` cell**, exactly as it appears in the catalog:

```
python3 anchor.py <source doc> "<the whole raw cell>"
```

An identical script fed a hand-derived input is not an identical instrument. Fragment extraction —
take the longest `"…"` span, split on ellipsis, take the longest surviving part, never search a
string that still contains an ellipsis — now lives inside the tool, so every agent's *input* is
derived the same way too.

⛔ **Assert the tool before your first anchor call, and abort the slice if it disagrees:**

```
shasum -a 256 anchor.py
# must be 973b68058e28b18b42ecbabb0641a923b4f2518358683c3df0f12c7341daa6e5
```

`anchor.py` is shared load-bearing code. If your copy differs, every row you produce is measured
with a different instrument than the rest of the wave and nothing in the output would say so.
A mismatch is a **halt**, not a note.

**The four outcomes, and what each one means for the row:**

| Output | Exit | Bucket |
|---|---|---|
| `FOUND start_line=N end_line=M wrapped=… trimmed=…` | 0 | record `anchor_line=N`, continue to Test 1 |
| `AMBIGUOUS n=k lines=…` | 2 | **`UNRESOLVED`**, `notes=ambiguous-anchor:<lines>` |
| `TOO_SHORT longest=n` | 3 | **`UNRESOLVED`**, `notes=fragment-too-short`, cell verbatim in `quote_fragment` |
| `TRIM_EXCEEDED trimmed=n limit=n` | 4 | **`UNRESOLVED`**, `notes=anchor-trim-exceeded:<n>` |
| `ABSENT` | 1 | run it against every other `.md` in the repo → found elsewhere = `UNRESOLVED`, `notes=anchor-moved:<file>:<line>`; found nowhere = **`dead`**, `notes=anchor-absent` |

**`AMBIGUOUS` is never resolved by taking the first match.** The tool used to do that silently, and
first-match-wins with no signal is exactly the miscite class this wave exists to find — it makes
`anchor_line` a coin flip on 45 rows across the catalog while the spec claims the cited line is the
line the span begins on. If the tool cannot tell you which occurrence is yours, neither can you.

`trimmed=<n>` reports characters dropped by longest-matching-prefix backoff, which exists because
the catalog appends terminal punctuation the source does not carry. **Record it in the `trimmed`
column on every row, always** — `0` included.

⛔ **The backoff is capped, and the cap exists because the backoff was shipped unproven.** It was
added on reasoning and validated on A21, where **all 16 rows are `trimmed=0` — it never once
fired there**, and it then became the sole basis for hundreds of anchors catalog-wide. A dry run
found matches surviving after **120 characters** were dropped; a 120-character trim is not the same
quote with its full stop removed, it is a different string. The cap is `trimmed > 15` **or**
`trimmed > 20%` of the fragment → `TRIM_EXCEEDED` → `UNRESOLVED`. Never `FOUND`.

**Measured over all 2310 rows with the shipped tool, post-cap** (run by subprocess against
`scripts/anchor.py` itself, not a reimplementation — an earlier count was taken from a
reimplementation and was wrong, which is the very failure this spec keeps finding):

| Outcome | Rows | % |
|---|---|---|
| `FOUND` | 1963 | 85.0% |
| `TRIM_EXCEEDED` | 152 | 6.6% |
| `ABSENT` | 100 | 4.3% |
| `TOO_SHORT` | 51 | 2.2% |
| `AMBIGUOUS` | 43 | 1.9% |
| unreadable source (the PDF) | 1 | — |

Of the 1963 `FOUND`, **205 matched only through the backoff** (max 15 after the cap, median 1).
**Expect about one row in seven not to reach a clean anchor** — 347 of 2310. That is the data, not
your slice going wrong, and it is deliberately higher than before the cap: 152 rows that used to be
recorded as clean matches are now explicitly unresolved.

**The cited line must be the line the span begins on.** A span that starts on line N and continues
onto N+1, cited as N+1, is the wrap-driven miscite.

### Test 0.5 — THE `Status` COLUMN. Read it before you judge anything.

⛔ **Added 2026-08-20. The catalog carries a `Status` cell on all 2310 rows and this spec ignored
it entirely** — which is the root cause of the row-14 three-way split, and would have sent every
gated rule to `LIVE`.

Measured here with an **escape-aware** splitter (`(?<!\\)\|`; all 2310 rows have exactly 5 cells,
so there are no malformed *rows*), **174 distinct status strings**:

| Status | Rows | What you do |
|---|---|---|
| `Active` exactly | 1703 | continue to Test 1 |
| `Active — Frozen` | 56 | continue to Test 1; frozen ≠ inactive. Note `frozen` |
| other dated `Active — …` variants | ~25 | continue to Test 1 |
| `Gated — Pending` (296 exact, 318 incl. variants) | 318 | **`UNRESOLVED`**, `notes=status-gated:<cell verbatim>` |
| contains `Supersed*`, not compound | 75 | **`RETIRED-CANDIDATE`**, `notes=status-superseded` |
| **compound** — contains BOTH `supersed*` and `active` | 13 | **`UNRESOLVED`**, `notes=status-compound` |
| `unclear…` | ~6 | **`UNRESOLVED`**, `notes=status-unclear` |
| not a status at all — `t` ×3, `t\` ×2, `premium\` ×1 | 6 | **`UNRESOLVED`**, `notes=status-not-a-status` |

**A gated rule is not a live rule.** 318 rows say `Gated — Pending` in their own Status cell; under
the previous spec every one reached Test 3 and bucketed `LIVE`. **Proposed and NOT applied** (§5 —
bucket definitions are Andy's): a first-class `GATED` bucket, so 318 rows do not sit in the
`UNRESOLVED` queue purely for want of a name.

**Compound statuses are real and must not be collapsed.** Thirteen rows carry both readings at
once, e.g. `Superseded (prior rationale) / Active (current framing)` and
`Superseded (original one-window claim) / Active (corrected)`. The cell itself refuses to answer;
so do you.

> **The two derivations of "non-Active" are now resolved, and the manager's own number was the
> defective one — by their own re-check.** `Status == 'Active'` exactly = **1703 → 607
> not-exactly-Active**. `Status.startswith('Active')` = 1885 → 425 in the Active family. The pair
> is **607 vs 425**; the earlier 497 came from an ad-hoc classifier that bucketed frozen ahead of
> active and swallowed ~31 rows into a catch-all. **Carry 607** — it is the operative set for this
> test, because `Active — Frozen` (56) and the dated `Active — ruled…` variants (118) carry
> information Tests 0–3 never consult, exactly like `Gated`.
>
> Likewise the malformed-cell count: the real figure is **6** (`t`×3, `t\`×2, `premium\`×1). An
> earlier "33" came from a splitter that ignored `\|` escapes. **Do not carry 33 or 497 anywhere.**
> Both were instrument errors, not catalog errors — the catalog was right both times.

### Test 1 — SUPERSEDED. Has a dated correction overtaken the rule?
Read the anchor line and the enclosing section of the source doc. A rule is superseded if the doc
carries any of: `[CORRECTED`, `[AMENDED`, `SCOPE AMENDMENT`, `~~`-struck text, `supersedes`,
`superseded`, `overruled`, `declined`, `REMOVED`, or a dated banner in `docs/RULINGS.md` naming it —
**and** that banner changes what the rule requires or who it binds.
⛔ **RULED 2026-08-20: agents render no terminal judgement verdict at all.** Both outcomes below
are **`RETIRED-CANDIDATE`**, which routes to pass 2 exactly like a contradiction candidate. Pass 2
decides between `dead`, `SUPERSEDED-BUT-STILL-READS-AS-LIVE` and `LIVE`.
- Banner present **and the original rule text is still standing and still reads as an instruction**
  → **`RETIRED-CANDIDATE`**, `notes=reads-as-live`. Required evidence: `superseded_by` = the
  banner's ruling id or its `file:line`.
- Banner present **and the rule text is struck, removed, or explicitly retired** →
  **`RETIRED-CANDIDATE`**, `notes=retired`, `superseded_by` = same.

**`dead` is now reachable from exactly one place: Test 0's anchor-absent branch**, where it is
mechanical — the fragment is in no `.md` in the repo. Nothing you *judge* may be `dead`.
- Banner changes only scope, not the requirement → **not** superseded; continue to Test 1b.
  (Worked example: `R-2026-08-17-GIT-RULE-SCOPE` scopes the git prohibition to bridge sessions on
  the mounted tree. Rows stating the prohibition are **LIVE**, scoped — not superseded.)

### Test 1b — CUTOVER SUPERSESSION. The v1-era rule with no banner over it.
Most superseded rules carry no banner at all: the 2026-07-30 rebuild replaced them wholesale and
the old doc still reads as an instruction. That is what this bucket is *for*, and a banner-only
Test 1 misses every one of them — in the pilot it sent a v1-era slice to `LIVE` 16 times out of 16.

Fires only when **both** hold, and both are mechanical:
1. The source doc's own date — the date in its filename, else the `Created`/`Generated` line in its
   first 10 lines — is **before 2026-07-30**; **and**
2. the rule's text or its quote names at least one of:
   - a v1 ledger artifact: `trades.csv`, `corrections.csv`, `bots_config.csv`, `compliance.csv`;
   - a pre-cutover P/L or trade-count figure (any count of trades/positions predating the cutover);
   - an item on `CLAUDE.md` §1's out-of-scope list: TT3, the Intraday Cockpit, discretionary
     scalping (including `Scalp-` bot names), `investor-profile.md`.

→ **`RETIRED-CANDIDATE`**, `notes=cutover`, `superseded_by` = `CLAUDE.md §3 DATA CUTOVER
2026-07-30` (or `CLAUDE.md §1` when it is the out-of-scope list that fires). Otherwise continue to
Test 2.

**Neither condition is a judgement call.** If you find yourself arguing that a rule "feels" stale
without condition 2 firing, that is `LIVE` — or `UNRESOLVED` if you can name the specific conflict.

### Test 2 — CONTRADICTS **CANDIDATE**. Flag it; do not rule on it.

⛔ **RULED 2026-08-19, after the pilot: agents do not render final `CONTRADICTS` verdicts.**
The pilot agreed 16/16 on every mechanical test and disagreed 3/3 here — so this test is split out
rather than allowed to drag the mechanical result down with it. You flag; a second, smaller
adjudication pass (§7) rules the flagged set only.

**The test — and it is a writing test, not a judgement call:**

> **Write one sentence describing a concrete situation in which following one rule violates the
> other.** If you can write that sentence, it is a `CONTRADICTS-CANDIDATE`. If you cannot, it is
> not a contradiction — it is `LIVE`, or `UNRESOLVED` if you can name a specific unresolved
> tension. **Topic overlap is not contradiction.** Two rules discussing the same bot, the same
> file or the same pillar are not in conflict merely for that.

Where to look — **widened, deliberately.** The pilot's agent looked past the catalog into the
project's own precedence documents and was **more correct than the foreman** for doing so: it found
two real contradictions the foreman missed and evidenced both. So you may check:
1. the catalog's `## Conflicts` section (line 2653 to end of file),
2. any rule named in your row's own `Impacts other areas` column, and
3. the precedence documents themselves — `CLAUDE.md`, `docs/build-plan.md`, `docs/RULINGS.md`.

You may **not** read all 2310 catalog rows. Fan-out safety depends on slice-local work.

**Run the deference check before you may conclude `LIVE`.** If the rule's own text defers to
another mechanism or authority — "superseded by X", "per Y", "decided by Z", "pending the W
tournament" — then **X, Y, Z or W is load-bearing for this rule, and you must confirm it is still
standing.** Search `docs/build-plan.md` and `docs/RULINGS.md` for it by name. If that authority has
itself been invalidated, archived, or ruled out, the rule is a `CONTRADICTS-CANDIDATE` whose
`winner` is the document that invalidated it.

> **A rule can be undermined by the invalidation of the authority it defers to — neither a banner
> over it nor a contradiction on its face.**
>
> **Worked example, A21 row 14, ruled 2026-08-20.** The rule says the QQQ "Hedge family" is
> reclassified and *"superseded by the backtest tournament"*. The tournament is the authority. But
> `docs/build-plan.md:85` places `HedgeA-S1` / `HedgeB-S2` / `HedgeC-S3` / `HedgeD-Conditional` /
> `HedgeTest` in the **archive-directly, no-clone** group with the reason *"Tournament invalid as a
> selector: S1≈D identical on 73/86 days, S3 a different execution class, no arm carries
> Range075"*, and `CLAUDE.md:38` / `:115` make build-plan frozen. The authority was ruled out from
> under the rule. **Correct verdict: `CONTRADICTS-CANDIDATE`, `winner=docs/build-plan.md`.**
> Three earlier passes returned `LIVE`, `SUPERSEDED-BUT-STILL-READS-AS-LIVE` and `dead` — three
> different *terminal* answers, which is why no agent renders this class at all.

When it fires, bucket **`CONTRADICTS-CANDIDATE`** and fill **all four**:
- `contradicts_row` — the other rule's label **and** its source doc,
- `concrete_case` — **the one sentence.** A candidate without it is rejected in pass 2 unread,
- a verbatim quote of the other rule in `notes`,
- `winner` — your reading under the precedence order below, or `NONE` if it does not resolve.
  Pass 2 decides; your `winner` is an input to that, never the ruling.

Precedence order, applied top-down, first step that resolves it:
  1. a dated ruling in `docs/RULINGS.md` naming either rule;
  2. `CLAUDE.md` §3 source-of-truth hierarchy;
  3. `docs/build-plan.md` (frozen) over any non-frozen doc;
  4. the more recent dated banner over the older;
  5. the more specific rule over the more general.

### Test 3 — LIVE
Anchor found, no superseding banner, no cutover supersession, no contradiction candidate →
bucket **`LIVE`**.

## §3 — Output contract

One file per slice. **No two slices write the same file.** Path is derived from the slice id and
the source doc, exactly as in the §1 table: `_wave3/rules/A<NN>__<slug>.tsv`, where `<slug>` is the
source doc path with `/` → `__`, ` ` → `_`, `.` → `_`.

Tab-separated, one header line, then one row per catalog row **in catalog order**:

```
row_ord	rule_label	bucket	anchor_file	anchor_line	trimmed	quote_fragment	superseded_by	contradicts_row	concrete_case	winner	notes
```

- `row_ord` — 1-based position of the row within your section. Every integer 1..N exactly once.
- `bucket` — one of `LIVE`, `CONTRADICTS-CANDIDATE`, `RETIRED-CANDIDATE`, `dead`, `UNRESOLVED`.
  **`CONTRADICTS`, `SUPERSEDED-BUT-STILL-READS-AS-LIVE` and judgement-based `dead` are not
  available to you** — all three are pass-2 verdicts. `dead` is reachable only from Test 0's
  mechanical anchor-absent branch.
- `concrete_case` — required and only meaningful for `CONTRADICTS-CANDIDATE`: the one sentence.
- `trimmed` — **the integer `anchor.py` printed**, copied, not judged. `0` means the quote matched
  exactly. Non-zero means the match survived only after characters were dropped from its tail.
  ⛔ **Without this column a heavily-trimmed anchor is recorded identically to an exact one.** The
  `#TOOLS` sha stops whole slices being silently incomparable; this stops *rows inside one slice*
  being silently incomparable. It is not optional and it is not derivable after the fact.
- Empty cells are a literal `-`. Never leave a tab-run empty; never re-order columns.

## §4 — Acceptance predicate (a derivation, and it can fail)

The agent recomputes all three of these **from the file itself** and writes them as the last line
of its output, prefixed `#RECONCILE`:

1. `declared` = the integer in your section's `### ` heading, parsed from the heading.
2. `parsed` = the number of lines in your section's line range that begin with `|` **minus 2**
   (the header row and the separator row).
3. `written` = the number of data rows you wrote.

**`declared == parsed == written` must hold.** Write them even when they disagree — especially then.
A slice that silently drops rows is detectable from its own output alone, because `written` will
differ from the other two. **Do not reconcile by editing your output to match.** If they disagree,
write `#RECONCILE declared=<a> parsed=<b> written=<c> MISMATCH` and stop; the foreman handles it.

Bucket totals must also sum to `written`.

### The tool sha — required, and it is part of acceptance
`anchor.py` is **shared load-bearing code**: every slice runs it, so a mid-wave change to it would
make slices silently incomparable — slice 3 and slice 40 would have been measured with different
instruments and nothing in the outputs would say so. Therefore emit, as the line **immediately
after** `#RECONCILE`:

```
#TOOLS anchor_py_sha256=<output of `shasum -a 256 anchor.py`>
```

**The wave's declared sha is `973b68058e28b18b42ecbabb0641a923b4f2518358683c3df0f12c7341daa6e5`.**
A slice output without this line is **not accepted**, and the foreman rejects — does not merge —
any slice whose sha differs. This is a second check on the in-clone assertion in Test 0: the first
catches a wrong tool before the work, this one catches it after.

## §5 — Escalation

- Ambiguous rule → `UNRESOLVED`, with **both readings** written out in `notes`. Never guess.
- Never widen a bucket to make something fit. `LIVE` is not the default — it is Test 3, reached only
  after 0, 1 and 2 have all been run.
- Anything requiring a ruling from Andy (a real doc-vs-doc conflict with no precedence winner)
  stays `UNRESOLVED`. You do not resolve it, and you do not edit any project file. **Read-only.**

## §6 — Dispatch law (measured in the pilot, not assumed)

- Invoke `~/bin/devin-free` **literally** — the allow rule is a prefix match on that path.
  Never pass `-p` (the wrapper owns it), never a `$DEVIN` variable, never `-r`.
- Use `--workspace <clone>`, never `cd`. One disposable `/tmp` clone per agent, never a worktree,
  never the live tree. The wrapper refuses `~/bot-fleet-v2`, `~/gitstore` and `~/bot-fleet` above
  `exec`, but the dispatch must not rely on that as its only guard.
- ⛔ **`--permission-mode dangerous` is required, and the pilot proved why.** Default `-p` mode
  auto-approves read-only tools only: the agent silently rejected the tool call that writes its
  output. `accept-edits` covers workspace edits but **not the exec tool**, so `anchor.py` cannot
  run. `smart` is advertised in `--help` but prints *"Smart permission mode is not available.
  Falling back to normal"* on this build and fails identically. Three runs produced nothing before
  `dangerous` produced the slice. It is contained by the disposable clone and the wrapper's cwd
  guard, not by the mode.
- ⛔ **Exit code 0 is NOT an acceptance signal.** All three blocked runs exited **0** with an empty
  stdout and no output file. Acceptance is: the output file exists, its `#RECONCILE` line is
  present and reconciles, and the row-id set matches. Check the file, never the exit code.
- The provenance line on stderr (`devin-free: v2 sha256 … | model swe-1-7 (free) | …`) is the
  per-run marker that the binary was actually reached. Its absence means no invocation happened.
- After every batch, assert `model` / `backend_type=windsurf` / `acu=0.0` / `credit=0` on each new
  row of `~/.local/share/devin/cli/sessions.db` (read-only, `mode=ro`). **A non-zero acu halts the
  wave and is reported — never a footnote.**
- ⛔ **NEVER KILL A SESSION.** Killing is what permanently destroys the acu evidence: a session
  that is killed — or merely left lingering — keeps `metadata=NULL` and `model=''` in
  `sessions.db` **forever**, and killing it later does not backfill. Established by test on
  2026-08-20: the A21 re-pilot **completed and wrote a valid slice** and its row is still NULL.
  **Lingering is wait-and-report, never kill.**
- ⛔ **Output present ≠ session finalised**, and a NULL-metadata row is **not** `$0`. Report it as
  **"two evidence surfaces dropped to one"**: the wrapper's provenance line still proves the
  *model* (`model swe-1-7 (free)`), and nothing proves the *cost*. Never fold a NULL row into a
  `$0` total. Assert acu only after a session has exited naturally.


## §7 — PASS 2: adjudicating the flagged candidates (a separate, smaller wave)

Pass 1 produces `CONTRADICTS-CANDIDATE` rows and nothing more. Pass 2 rules on **only** those rows,
gathered across all 56 slices into one queue. It is deliberately small and slower per row.

**Input.** One row per candidate: the rule, the `concrete_case` sentence, `contradicts_row`, the
quoted counter-rule, the pass-1 `winner` reading.

**Rejection before adjudication — do this first, it is cheap.** A candidate whose `concrete_case`
is missing, or is a restatement of topic overlap rather than a situation ("both discuss the
champion"), is returned as `LIVE` **without adjudication**. The sentence is the filter; that is why
it is mandatory in pass 1.

**Verdicts.** Pass 2 owns every terminal judgement: `CONTRADICTS` (winner named under the §2
precedence order) · `SUPERSEDED-BUT-STILL-READS-AS-LIVE` · `dead` · `LIVE` (the concrete case does
not hold on inspection) · `UNRESOLVED` (real conflict, precedence silent).

**Pass 2 takes both candidate kinds** — `CONTRADICTS-CANDIDATE` and `RETIRED-CANDIDATE` — in one
queue, because a rule can be flagged as both and the two readings must be settled together.

### Worked example — row 14 of A21, ruled 2026-08-20

Three passes gave three different terminal answers on a stable anchor: `LIVE` (foreman by hand),
`SUPERSEDED-BUT-STILL-READS-AS-LIVE` (agent run 1), `dead` (agent re-pilot). **The ruling is
`CONTRADICTS-CANDIDATE`, winner `docs/build-plan.md`, routed to pass 2** — not `dead`, not `LIVE`,
not superseded.

The basis, verified in the tree: `docs/build-plan.md:85` places `HedgeA-S1` / `HedgeB-S2` /
`HedgeC-S3` / `HedgeD-Conditional` / `HedgeTest` in the **archive-directly, no-clone** group, with
the reason *"Tournament invalid as a selector: S1≈D identical on 73/86 days, S3 a different
execution class, no arm carries Range075"*; `CLAUDE.md:38` and `:115` make `build-plan.md` frozen.
**The authority the rule defers to has been ruled out from under it** — the taxonomy rule says the
hedge family is superseded *by the backtest tournament*, and the tournament is itself invalid as a
selector. Test 1b's condition 2 never fires, so it was never cutover-superseded either.

The lesson generalises: **a rule can be undermined by the invalidation of the thing it defers to,
which is neither a banner over it nor a contradiction on its face.** That is why no agent renders
this class of verdict.

**⛔ `UNRESOLVED` with a real concrete case is Andy's, not the wave's.** Per dispatch §5, whether a
CONTRADICTS verdict becomes a ruling is Andy's decision. Pass 2 delivers the case, both quotes and
the precedence trace; it never edits a project document and never writes a ruling.

**Batching.** One agent per 10 candidates, same dispatch law (§6), same `#RECONCILE` /`#TOOLS`
discipline, output at `_wave3/rules-pass2/P<NN>.tsv`.

## §8 — Provenance of this spec

The pilot slice is **A21 = `docs/strategy-taxonomy.md`** (16 rules, catalog lines 1096–1116).
Both pilot artifacts — the foreman's by-hand execution and the agent's — are committed at
`data/wave3-pilot-2026-08-19/`, so the agreement rate is re-derivable by anyone.

**The rate, both ways.** Raw, all 16 rows: **13/16**, the number the bar was set against and met.
On what agents actually produce under Andy's split ruling: **16/16** — all three disagreements were
Test-2 `CONTRADICTS` verdicts, which agents no longer render. Anchor lines agreed 16/16 throughout.

**Correction.** An earlier draft of this spec said the `grep -F` wrap defect was hit on "the very
first row of the pilot slice". It was found in **A15** (`docs/capture-architecture-2026-07-30.md`,
the `DIR-SPX-PutVIX22-SL75` KEEP quote, lines 67–68) — the slice the foreman began by hand and set
aside as non-discriminating, since every row in it buckets `LIVE`. A21 became the pilot. Two slices
were narrated as one; the defect reproduces in A15 either way.
