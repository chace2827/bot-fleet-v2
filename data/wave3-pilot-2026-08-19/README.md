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
