# RULING DRAFTS — daily-close automation — 2026-08-21 — ✅ SIGNED, ALL THREE IN FORCE

Status: **SIGNED 2026-08-21.** Signatures applied by Claude at Andy's explicit in-chat
authorization ("I give you permission to edit and sign them for me", Cowork Fable chat
2026-08-21). All three registered in `docs/RULINGS.md` same day. Scratch file (`_*`), never
committed; retained until the wave lands, then disposable.
Plan context: agreed in the Cowork chat 2026-08-21 (daily-recording fix, Phases 0–3).
These three rulings are Phase 0. The Phase 1 build (`_dispatch-2026-08-21-close-wave-claudecode.md`)
is GATED on all three being signed. Sign by writing **SIGNED — Andy — date** under each, and for
R-B circling one option.

---

## R-2026-08-21-RECEIPT-ARGV — resolves inbox I-05 (guard change; this signature is the pre-auth)

**Decision.** Every daily-run receipt records how the run was invoked, so a run made with an
override flag is distinguishable in the permanent record from one made without.

Mechanics (verified against the tree 2026-08-21, `daily.sh` mtime 08-19 / `run_receipt.py` 08-18):
1. `daily.sh` exports `FLEET_ARGV` = its exact invocation argv (JSON list of `"$@"`).
2. `build_ledger.py` writes the **resolved** override state (`allow_rewind`,
   `allow_front_truncate`, `allow_ops_reclass`, each true/false) into `ledger_meta.json`.
   This is the load-bearing half: `daily.sh` only plumbs `--allow-rewind` as `$2`, so the other
   two flags can reach `build_ledger.py` only by direct invocation — recording at the point of
   use captures both routes; recording only the wrapper's argv would miss one.
3. `run_receipt.py` adds two fields: `argv` (from `FLEET_ARGV`, null when absent) and
   `overrides` (copied from `ledger_meta.json`; subject to the existing `ledger_stale` flag).
4. Reading rule: in receipts written **before** this lands, the absent field means **UNKNOWN**,
   never "no override" (an absent value never falls through to a pass).
5. Selftest checks added for: override recorded when passed; `[]`/all-false recorded when not;
   absent-field-is-null on old-shape env.

**Not changed:** the guards themselves, their thresholds, the append-only receipt contract.

SIGNED — Andy — 2026-08-21 (via explicit in-chat authorization, applied by Claude)

---

## R-2026-08-21-CLOSE-RECEIPT-SURFACE — where the new close stages are receipted

**Question.** The close gains stages (export ingest, capture bundle, brief render, manifest).
Do they go inside `daily.sh`'s receipted run, or around it?

**OPTION 1 — WRAP (recommended).** `daily.sh` is untouched; `TOTAL_STAGES=9` and the
"stages 9" receipt invariant stand unchanged. A new `scripts/close.sh` orchestrates
ingest → `daily.sh <day>` → capture bundle → `render_brief.py` → manifest, and leaves its own
trace: `data/close/<day>/manifest.json` plus an append-only `data/receipts/close-runs.jsonl`
(same house style as `run_receipt.py`). The ritual's receipt check becomes two lines instead of
one. Rationale: refactor-first / behavior-neutral (§5) — no existing checker, CI fixture, or
memory note about "stages 9" is invalidated; the daily receipt keeps meaning exactly what it has
meant since 2026-08-18.

**OPTION 2 — EXTEND.** `daily.sh` grows to N stages; every receipt checker, ritual step and
fixture that asserts 9 is updated in the same change. Rejected by the drafter as higher blast
radius for zero additional evidence, but it is Andy's call, not the drafter's.

**Decision: OPTION 1 — WRAP.** (Recommended option adopted under Andy's blanket in-chat
authorization; Andy may overturn at commit review before the wave dispatches.)

SIGNED — Andy — 2026-08-21 (via explicit in-chat authorization, applied by Claude)

---

## R-2026-08-21-STAGING-MANIFEST — §9.1 step 3 mechanics amendment

**Decision.** For the daily close, the commit file list is **generated, not hand-typed**.
`close.sh` derives it from the manifest and prints the exact command: file-by-file `git add`
(never `-A`), then commit with a message whose figures are derived from the manifest, then push.

Constraints the generator enforces:
- Every path in the printed list appears in the manifest **with a sha256**; the two lists are
  derived independently and must match (no path rides along uncited).
- Paths matching `_*`, `.claude/**`, `_locktrash/**`, or `one` are a FATAL refusal, never a
  silent skip.
- **Unchanged and explicit:** Andy runs every commit and push to the main tree; Claude/agents
  still never run git on the mounted tree; Andy's commit-review veto is untouched. This ruling
  replaces the *typing*, not the *authority* — it amends the mechanics of CLAUDE.md §9.1 step 3
  for the daily close only.

SIGNED — Andy — 2026-08-21 (via explicit in-chat authorization, applied by Claude)

---

## Recorded observations attached to these drafts (not decisions)

- Local master `a7ffc52` is **one commit ahead of `origin/master` `3d456bd`, unpushed**
  ("wave 3: lane-state close-out", reflog 2026-08-20). Push before any Devin dispatch — clones
  base on origin.
- `daily.sh` line 152 `TOTAL_STAGES=9`; override plumbing gap as described in R-ARGV item 2.
- Receipts already carry `pinned`, `source_export`, per-output sha256, `ledger_stale` — the
  argv/overrides fields are the only gap I-05 names.
