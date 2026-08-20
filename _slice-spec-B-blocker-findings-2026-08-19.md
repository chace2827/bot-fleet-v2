# SLICE-SPEC B — triage the blocker-audit findings (369 rows, 25 slices)

**Written by the wave-3 foreman, 2026-08-19. Read in full before executing a slice.
If the spec does not answer your question, you write `UNRESOLVED` — you never ask and never guess.**

## §0 — What this data is, and what was re-derived

The artifact is `findings_final.json` (869 rows, sha256 `8374e2e1…`) from the 58-slice PR sweep,
now in git at `data/blocker-audit-2026-08-19/` (PR #64); previously only under
`~/Documents/fleet-runs/2026-08-19/pr-sweep/`, where nothing backed it up. **Memory's two figures were wrong as
labelled and are corrected here** — both were re-derived from the files themselves:

- **"804 findings" is not a finding count.** 869 raw rows collapse into **804 clusters**
  (`analysis.json` → `clusters`, sizes summing to 869: 749 singletons, 47 pairs, 6 triples, 2 quads).
  The sweep really did run **58/58** — 58 distinct workspaces in the data.
- **"130 likely-valid" is real but has a different denominator.** It is 130 of the **352 actionable**
  rows (284 DEFECT-SUSPECT + 68 GUARD-UNNAMED), split 175 re-verify / 130 likely-valid / 47 no-file-
  citation — reproduced exactly from the stored `t` field. ⚠️ **The number 130 also appears as
  DEFECT-SUSPECT∧re-verify. Two different quantities, same value.** Carry the denominator, always.
- ⛔ **The code that computed `t` is not in the durable copy.** An independent reconstruction lands
  at 159/128/65 with 30 of 352 rows disagreeing. **Therefore no slice in this spec may use `t`.**
  Every row is re-classified here from its own citations, by the stated rule, at a stated sha.

**Row basis for this wave is `work/canon.json`** (369 rows, `R001`–`R369`, sha256 `a96f35a1…`,
in git at `data/blocker-audit-2026-08-19/canon.json` (PR #64)) = the 352 actionable rows
+ 21 UNVERIFIABLE − 4 dedup. It carries `row_id`, `files` and `cites` already extracted, which is
why this spec can be slice-local.

**Window discipline:** the sweep agents READ `c0e24b4`; the sweep's own report compared against
`7596bb6`; this wave's pin is `1d56fc0`. **Every staleness figure you write must name both shas.**
A delta without its window is not checkable.

## §1 — Slice unit and the full slice list

**Slice unit = one batch of 15 canon rows, in `row_id` order.** 25 slices, all named. The last is
short by design.

| Slice | Row ids | Rows | of which no-file-citation | Output file |
|---|---|---|---|---|
| B01 | `R001`–`R015` | 15 | 2 | `_wave3/findings/B01.tsv` |
| B02 | `R016`–`R030` | 15 | 1 | `_wave3/findings/B02.tsv` |
| B03 | `R031`–`R045` | 15 | 0 | `_wave3/findings/B03.tsv` |
| B04 | `R046`–`R060` | 15 | 1 | `_wave3/findings/B04.tsv` |
| B05 | `R061`–`R075` | 15 | 0 | `_wave3/findings/B05.tsv` |
| B06 | `R076`–`R090` | 15 | 1 | `_wave3/findings/B06.tsv` |
| B07 | `R091`–`R105` | 15 | 0 | `_wave3/findings/B07.tsv` |
| B08 | `R106`–`R120` | 15 | 1 | `_wave3/findings/B08.tsv` |
| B09 | `R121`–`R135` | 15 | 1 | `_wave3/findings/B09.tsv` |
| B10 | `R136`–`R150` | 15 | 2 | `_wave3/findings/B10.tsv` |
| B11 | `R151`–`R165` | 15 | 1 | `_wave3/findings/B11.tsv` |
| B12 | `R166`–`R180` | 15 | 2 | `_wave3/findings/B12.tsv` |
| B13 | `R181`–`R195` | 15 | 3 | `_wave3/findings/B13.tsv` |
| B14 | `R196`–`R210` | 15 | 3 | `_wave3/findings/B14.tsv` |
| B15 | `R211`–`R225` | 15 | 4 | `_wave3/findings/B15.tsv` |
| B16 | `R226`–`R240` | 15 | 1 | `_wave3/findings/B16.tsv` |
| B17 | `R241`–`R255` | 15 | 3 | `_wave3/findings/B17.tsv` |
| B18 | `R256`–`R270` | 15 | 1 | `_wave3/findings/B18.tsv` |
| B19 | `R271`–`R285` | 15 | 2 | `_wave3/findings/B19.tsv` |
| B20 | `R286`–`R300` | 15 | 1 | `_wave3/findings/B20.tsv` |
| B21 | `R301`–`R315` | 15 | 1 | `_wave3/findings/B21.tsv` |
| B22 | `R316`–`R330` | 15 | 1 | `_wave3/findings/B22.tsv` |
| B23 | `R331`–`R345` | 15 | 2 | `_wave3/findings/B23.tsv` |
| B24 | `R346`–`R360` | 15 | 0 | `_wave3/findings/B24.tsv` |
| B25 | `R361`–`R369` | 9 | 1 | `_wave3/findings/B25.tsv` |

**Slice pack — the agent cannot work without it, and this is not optional.** 164 of 369 rows carry
a premise about the **PR body**, which is unverifiable from a repo clone. Each slice's clone must be
seeded with: `rows.json` (that slice's 15 canon rows, verbatim) and `_packet/` (`body.txt`,
`diff.patch`) for every PR named in them. **A slice dispatched without its packet returns
`UNVERIFIABLE-FROM-CLONE` for those rows, and that is a foreman error, not an agent finding.**

## §2 — The decision procedure

For each row, at the pin `1d56fc0`, assign exactly one verdict. Tests run in order; stop at the
first that fires.

### Test 0 — REPRODUCE THE PREMISE, NOT THE NUMBER
The row's `finding` is a claim; `check` is the command that produced it; `observed` is what it
produced. **Re-run `check` verbatim.**
- ⛔ **Invocation flags are part of the premise.** `check_refs.py --strict` exits 1; without
  `--strict` it exits 0. Running a different command and reporting a different result manufactures
  a false verdict. If you must deviate, the `command` column must begin `DEVIATION:` and say why.
- ⛔ **A word can falsify a claim, not only a figure.** 102 of 369 rows turn on `green`, `clean`,
  `never`, `passes`, `exits 1`. Bucketing compared numbers; it never adjudicated premises. If the
  claim's operative word is false, the row is `REFUTED` even when every number matches.

### Test 1 — STALE PREMISE (the row is about a file that has moved under it)
Compute, do not assume: for each path in the row's `files`, does it differ between `c0e24b4` and
the pin `1d56fc0`? (`git diff --name-only c0e24b4 1d56fc0`, intersected with `files`.)
- Any cited file changed **and** re-running `check` no longer reproduces `observed` →
  **`STALE-PREMISE`**, and `notes` must name which file changed and both shas.
- Cited files unchanged → continue.

### Test 2 — ASSIGN
- `check` re-run reproduces `observed` → **`REPRODUCES`**.
- `check` re-run contradicts `observed` (number **or** operative word) → **`REFUTED`**, with the
  actual output quoted in `evidence_span`.
- The premise is about PR body text and no `_packet/` was supplied →
  **`UNVERIFIABLE-FROM-CLONE`**.
- `files` is empty (35 rows across the wave, listed per slice in §1) and the premise names no
  runnable check → **`MANUAL-READ`**, with the specific question the foreman must answer in `notes`.

### Test 3 — the quote rule
Any span you quote as evidence **must begin on the line you cite**. A grep that matched token A on a
wrapped line, cited as token B on the next line, is the exact defect class this wave exists to
find. If your span and your line number disagree, the row is `UNRESOLVED`.

⛔ **Carve-out for hard wrapping, added after the spec-A pilot hit it.** Project docs wrap at ~105
columns, so a real quote can legitimately span two lines and no `grep -F` will ever match it. When
that happens, cite the line the span **begins** on and append `wrapped:<start>-<end>` to `notes`.
Use the `anchor.py` in your slice pack — the same script slice-spec A uses — so that "absent" means
absent, not merely unmatched by a line-oriented search.

## §3 — Output contract

One file per slice, `_wave3/findings/B<NN>.tsv`. **No two slices write the same file.**
Tab-separated, one header line, then one row per canon row in `row_id` order:

```
row_id	pr	verdict	command	rc	evidence_file	evidence_line	evidence_span	files_changed_since_c0e24b4	notes
```

- `verdict` ∈ `REPRODUCES`, `REFUTED`, `STALE-PREMISE`, `UNVERIFIABLE-FROM-CLONE`, `MANUAL-READ`,
  `UNRESOLVED`.
- `command` — exactly what you ran, including every flag; prefix `DEVIATION:` if it differs from
  `check`.
- Empty cells are a literal `-`.

## §4 — Acceptance predicate (a derivation, and it can fail)

Last line of the output, prefixed `#RECONCILE`:

1. `expected` = the count of `row_id`s in **your** `rows.json`, counted by you.
2. `written` = the data rows you wrote.
3. `ids_ok` = whether the set of `row_id`s you wrote is **exactly** the set in `rows.json` —
   no additions, no omissions, no re-ordering.
4. `verdict_sum` = the sum of your per-verdict counts.

Then, as the line **immediately after** `#RECONCILE`:

```
#TOOLS anchor_py_sha256=<output of `shasum -a 256 anchor.py`>
```

`anchor.py` is shared load-bearing code across every slice of both specs. A mid-wave change to it
makes slices silently incomparable, so the sha travels with every output and the foreman rejects a
slice whose sha differs from the wave's declared sha. **A slice output without this line is not
accepted.**

**`expected == written == verdict_sum` and `ids_ok=true` must all hold.** Write the line even when
it fails — `#RECONCILE expected=<a> written=<b> ids_ok=<t/f> verdict_sum=<c> MISMATCH` — and stop.
Never edit your output to make the predicate pass.

## §5 — Escalation

- Ambiguous → `UNRESOLVED` with **both readings** in `notes`.
- **Never widen a verdict to make a row fit.** `REPRODUCES` is not the default.
- Never write to any project file; never `git` anything but read-only commands in your own clone;
  never push. Results leave as your slice TSV only.
- A non-zero acu on your session is a halt, reported immediately — not a footnote.

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
