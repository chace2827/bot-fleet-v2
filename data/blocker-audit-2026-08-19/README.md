# Blocker-audit basis — 2026-08-19 PR sweep

**Why these files are here.** Until this commit they existed only under
`~/Documents/fleet-runs/`, outside git and outside every connected folder: no manager could verify
a number against them and nothing backed them up. That is the same class of risk as leaving the
Devin wrapper in `/tmp`. Wave 3 depends on these files, so they are in git before the wave is.

Copied verbatim, byte-for-byte. Verify with `shasum -a 256`:

| File | sha256 | Source |
|---|---|---|
| `findings_final.json` | `8374e2e150479ee9f419c9bf2ecea3ae9bb92fe20a2112058d29c8bc4cfd1550` | `~/Documents/fleet-runs/2026-08-19/pr-sweep/` |
| `analysis.json` | `9e7a9120d7459473e5cb8cee8cd1a03f57867fc635fad66c669eefd0785cf71c` | same |
| `rows_slim.json` | `e27ccbb76d2ee8d5714c8f6c4ec4f6bbad74ebd137b65230783ecec34c7a4aa2` | same |
| `canon.json` | `a96f35a158276b9ae6d40829aaae8252ad174f634791a57404cdf26033f64f41` | `~/Documents/fleet-runs/2026-08-19-triage/work/` |

## What each file is, and the derivation of every number quoted from it

**`findings_final.json` — 869 rows.** The raw sweep output, 58 distinct `ws` values, so the
"sweep 58/58" claim checks out. Verdicts: 496 OK, 284 DEFECT-SUSPECT, 68 GUARD-UNNAMED,
21 UNVERIFIABLE.

**`analysis.json` — `rows` (869) + `clusters` (804).** ⚠️ **"804 findings" is a mislabel that has
been propagating.** 804 is the CLUSTER count: 749 singletons + 47 pairs + 6 triples + 2 quads,
whose sizes sum back to 869. Quote it as clusters or not at all.

**`rows_slim.json` — 869 rows, carries the `t` staleness field.** Of the **352 actionable** rows
(284 DEFECT-SUSPECT + 68 GUARD-UNNAMED): `t=2` re-verify **175**, `t=1` untouched-since-pin
**130**, `t=0` no file citation **47**. That is the real basis of "130 likely-valid" — its
denominator is **352, not 869 and not 804**.

> ⚠️ **130 is also the count of DEFECT-SUSPECT ∧ `t=2`.** The same value names two different
> quantities in the same table. Always carry the denominator.

> ⛔ **`t` MUST NOT be consumed by any slice.** The code that computed it is not in the durable
> copy and was lost with `/tmp`. An independent reconstruction from git (citations parsed from
> `evidence`, intersected with `git diff --name-only c0e24b4 7596bb6`) lands at 159/128/65 and
> disagrees on 30 of the 352 rows. `t` is retained here as **provenance for the published figures**,
> not as an input. Slice-spec B re-derives every citation itself, at a stated sha.

**`canon.json` — 369 rows, `R001`–`R369`.** The de-duplicated row basis for triage:
352 actionable + 21 UNVERIFIABLE − 4 dedup. Carries `files` and `cites` already extracted, plus
`row_id`, `dedup`, `n_dup`, `witnesses`. 35 rows have an empty `files` list — those are the
manual-read rows.

## Window discipline

The sweep agents READ `c0e24b4`. The sweep's own report compared against `7596bb6`. Wave 3's pin is
`1d56fc0`. **Every staleness figure derived from these files must name both ends of its window.**
A delta without its window is not checkable — that is how "130" came to mean two things.
