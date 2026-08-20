# Wave-3 pilot evidence — slice A21, 2026-08-19

**The pilot slice is `A21` = `docs/strategy-taxonomy.md`, 16 rules, catalog lines 1096–1116.**
Named here because it was previously named nowhere, which made the reported agreement rate
un-re-derivable by anyone but the foreman. Both artifacts are committed so the rate can be
recomputed from the files.

| File | What it is |
|---|---|
| `A21-foreman-by-hand.tsv` | the foreman's by-hand execution, written **before** the agent ran |
| `A21-agent.tsv` | one agent, same slice, same spec |
| `A02-warmup-agent.tsv` | the §4 warm-up (`README.md`, 3 rules) under the post-split contract |

## The rate, stated both ways

- **Raw, all 16 rows: 13/16 = 81%.** The three disagreements were rows 5, 14 and 15.
- **On what agents actually produce under the split ruling: 16/16.** All three disagreements were
  Test-2 (`CONTRADICTS`) verdicts, and after Andy's 2026-08-19 ruling **agents no longer render
  those** — they flag `CONTRADICTS-CANDIDATE` with a one-sentence concrete case and a separate
  pass-2 wave adjudicates. Anchor lines agreed **16/16** before the split and still do.

Both numbers are true of different questions. 13/16 was the bar-setting number and the bar was
met; 16/16 is the number that describes the work the fan-out will actually do.

## A correction carried here

An earlier draft of slice-spec A said the `grep -F` wrap defect was hit on "the very first row of
the pilot slice". It was not: that defect was found in **A15** (`docs/capture-architecture-2026-07-30.md`,
the `DIR-SPX-PutVIX22-SL75` KEEP quote at lines 67–68), which was the first slice the foreman
started executing by hand and then set aside as non-discriminating — every row in it buckets `LIVE`.
A21 became the pilot. Two slices were narrated as one. The defect is real either way and is
reproducible in A15; the slice attribution was wrong.

## Re-pilot, 2026-08-20 — A21 with the patched `anchor.py` (`e20fed80…`)

`A21-agent-repilot-patched-tool.tsv`. Run after the manager's verification, to test the fragment-
extraction fix rather than the buckets.

**Mechanical layer: 16/16 against the tool's deterministic output.** Every `anchor_line` matches
what `anchor.py` returns when driven independently over the same 16 raw cells;
`#RECONCILE declared=16 parsed=16 written=16`; `#TOOLS` sha equals the declared sha.

**The red test passed.** Row 8's quote is `**Pillar 3 only.**` — 14 characters normalised. Under
the old spec **both the foreman's by-hand pass and the first agent** hand-picked a fragment below
even the 40-char threshold and recorded `LIVE` at line 77. With the patched tool the row comes back
`TOO_SHORT` and the agent recorded **`UNRESOLVED / fragment-too-short`**, taking the tool's verdict
instead of improvising. That is the defect-5 fix demonstrated on the row that exhibited it.

**Judgement layer moved, and one row needs a ruling.** The re-pilot flagged **5**
`CONTRADICTS-CANDIDATE`s (rows 4, 5, 9, 13, 15) against the first run's 2. That is expected and
harmless: under the split a candidate is a flag, pass 2 adjudicates, and each of the five carries a
real one-sentence concrete case — row 9's even cites `R-2026-08-07-IC-GROUPS-BOTH-STAY`.

⛔ **Row 14 has now produced three different terminal answers in three passes:** `LIVE` (foreman by
hand), `SUPERSEDED-BUT-STILL-READS-AS-LIVE` (agent, run 1), `dead` (agent, re-pilot, citing
`build-plan.md` §2D). Its anchor is stable at line 125 in all three. The rule's own text says the
QQQ hedge family is "Reclassified … superseded by the backtest tournament", so the question is
whether a rule that describes its own supersession is retired or merely descriptive.

**`dead` is terminal — unlike a candidate it does not route to pass 2**, so this divergence would
ship unreviewed at 56-slice scale. **Proposed and NOT applied** (a bucket-definition change after
the pilot is Andy's under dispatch §5): restrict `dead` to the mechanical branch only — anchor
absent from every `.md` in the repo — and route banner/judgement-based retirement to a flag that
pass 2 adjudicates alongside the contradiction candidates.
