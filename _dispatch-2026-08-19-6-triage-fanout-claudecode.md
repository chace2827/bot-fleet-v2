# WAVE 3 — Claude Code foreman — SLICE-SPEC FIRST, then fan out wide on the free lane

Paste into Claude Code, in `~/bot-fleet-v2`:
"Read `_dispatch-2026-08-19-6-triage-fanout-claudecode.md`. You are the WAVE-3 foreman.
Execute §0, then §1, then §2. Stop at the §3 gate and report."

**The premise of this whole file:** you can dispatch faster than you can specify. Agents are free
and effectively unlimited for the next few weeks; **specification is the only scarce resource.**
So the foreman's job here is NOT to run agents. It is to write two slice-specs good enough that
fifty agents underneath them produce work that can be merged without re-reading every line.

## §0 — HARD GATE. Do not proceed past this section if either is false.
1. **Step 6 is complete** — wrapper v2 built, and all six acceptance results reported and passing,
   including check 5 (the wrapper reaches exec from a fresh `/tmp` clone). Until that lands, no
   agent can run in a clone at all and this entire file is theoretical.
2. **`~/bin/devin-free --selfhash` equals `shasum -a 256 scripts/devin_free.sh`.** Record the value.

If either fails: stop, report, do nothing else.

Dispatch law, unchanged: invoke `~/bin/devin-free` **literally**. Never pass `-p` (the wrapper owns
it). Never reintroduce a `$DEVIN` variable. Never `devin -r`. One `/tmp` clone per agent, never a
worktree, never the live tree, all pinned to one sha you print.

## §1 — PRE-FLIGHT: re-derive both counts. Neither figure is trusted.
The 08-19 lesson: *before ruling against a count, validate the instrument that produced it.* A
single regex under-counted the migration tracker by a third and nobody noticed.

**Item 1 — `docs/rules-catalog.md`.** The board claims "2310 rules from 55 source docs."
Measured at the mount on 2026-08-19: 2,741 lines, 2,422 lines beginning `|`, 52 distinct
`docs/*.md` mentions. **None of those is the rule count.** Derive it **two independent ways**
(e.g. table-row parse vs. per-source-doc sum) and require agreement. If they disagree, the parser
is wrong, not the file — chase the gap before writing any spec.

**Item 2 — the blocker-audit findings.** Memory records "sweep 58/58, 804 findings, 130 likely-valid,
NEXT: triage them." **That artifact is not in `docs/` or `data/` at the pin** — locate it
(`_fleet-runs/**`, a merged PR, an artifact) and re-derive both numbers from the file itself.
**If you cannot find it, item 2 is DROPPED from this wave — say so plainly and do not reconstruct
it from memory.**

## §2 — WRITE THE TWO SLICE-SPECS. This is the work. Do not dispatch any part of it.
For each item, produce ONE spec file that a single agent can execute against a single slice
without asking a question. Each spec must contain, and will be rejected without:

1. **The slice unit and the full slice list.** Item 1 slices by source doc. Item 2 slices by row
   batch. Every slice named explicitly — no "and so on."
2. **The decision procedure**, not just the bucket names. For item 1 the buckets are
   LIVE · CONTRADICTS (name BOTH rules and which wins) · SUPERSEDED-BUT-STILL-READS-AS-LIVE · dead.
   Write the test that assigns a rule to a bucket, in a form where two different agents reading it
   reach the same verdict. If you cannot write that test, the bucket is not yet defined.
3. **The output contract.** One file per slice, path derived from the slice name, fixed columns.
   **No two agents may write the same file** — that is the whole reason this fans out safely.
4. **An acceptance predicate stated as a derivation, never a literal** — and one that can FAIL.
   Per-slice row count must reconcile against the whole-file count; a slice that silently drops
   rows must be detectable from the output alone.
5. **The escalation rule**: what the agent does when a rule is ambiguous. It writes an
   `UNRESOLVED` verdict with both readings. It never guesses, and it never widens a bucket to
   make something fit.

## §3 — THE PILOT GATE. Stop here and report. Do not fan out.
**You execute one slice yourself, by hand, before any agent sees the spec.** Then dispatch exactly
ONE agent on that same slice and compare.

- Agreement at or above your stated bar → the spec is validated, fan-out is authorized by Andy.
- Below it → the spec is wrong, not the agent. Rewrite and re-pilot.

**A spec you have not executed yourself is a predicate you have not seen fail.** That single rule is
what wave 1 cost us; at 50-way fan-out it would cost fifty times as much.

Report: both derived counts (and how they were derived twice), the two spec files, the pilot
slice, your hand result vs the agent result, the agreement rate, and the bar you set beforehand.

## §4 — FAN-OUT (only after Andy authorizes the pilot)
- **Concurrency ≤ 10 total, account-wide**, not per item. The 429 escalates and mid-run deaths
  waste the work. Throttled queue, retry-on-429 with backoff.
- **One warm-up run first** — cold start is 30–60s and the first agent otherwise looks hung.
- After **every** batch, assert `model` / `backend_type=windsurf` / `acu=0.0` / `credit=0` on each
  new session row. **A non-zero acu is a halt-and-report, not a footnote.**
- Merge per slice-group, not per agent. Results as PRs to `devin/*`; never push to master.
- **`log` what you drop.** If any slice is skipped, sampled, or truncated, say so — silent
  truncation reads as full coverage.

## §5 — Escalation
- **You decide:** slicing, batch size, retries, re-prompting, which slice-group merges first.
- **Andy decides:** the pilot agreement bar, any bucket-definition change after the pilot, anything
  Class C, any spend outside the free lane, and whether a CONTRADICTS verdict becomes a ruling.
- **Halt and report:** a push to master, any git write against `~/bot-fleet-v2` or `~/gitstore`,
  a non-zero acu, an agent widening a bucket to resolve an ambiguity.
