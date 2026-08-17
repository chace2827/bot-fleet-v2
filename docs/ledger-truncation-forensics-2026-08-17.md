# Ledger truncation forensics — 2026-08-17

**Tracker item:** T-03 (`todo-2026-08-16.csv`) — "hedge_tournament 2026-08-11 points at a trade_id
absent from trades.csv; trades.csv now holds one day only."

**Scope.** Read-only forensic. No file in this repo was edited, no OA screen was opened, no git
command was run. Git history was read by decompressing loose objects under `.git/objects` directly
(reads only; no index, no lock). Everything below is first-hand from the working tree and from
committed blobs, 2026-08-17.

**Verdict in one line.** Nothing was corrupted and nothing is lost. A **hermetic CI determinism
run pinned to the `2026-08-10` fixture overwrote the live working ledger in place**, and the
overwritten file was committed as part of PR #7. Both missing days are recoverable two independent
ways. The larger, separate problem is that **08-12, 08-13 and 08-14 never entered the repo at all.**

---

## 1. The mechanism

`build_ledger.py` is a **full-rebuild-from-one-export** script, by design (module docstring,
lines 77–79): *"the OA website export is FULL trade history (not a delta), so re-importing the
newest daily file reconstructs the entire ledger… the newest file wins."* Every run truncates
`data/trades.csv` and rewrites it from a single file in `data/raw/`.

Which file it uses is decided by the optional positional `date` argument (`main()`, ~line 396):

```
if args.date:  src = data/raw/<date>.csv      # pinned
else:          src = newest_raw()             # newest by filename sort
```

`daily.sh` passes that argument straight through (`python3 scripts/build_ledger.py ${DAY:-}`).

**There is no separation between a fixture run and a live run.** `scripts/daily.sh 2026-08-10`,
the command used to prove byte-for-byte determinism for CI, writes to exactly the same
`data/trades.csv` that carries the fleet's real numbers. `TAPE_FIXTURE=1` isolates the tape stage
from the network; nothing isolates stage 1 from the ledger.

So the sequence that produced the current state is:

| # | Run | Export used | `trades.csv` after |
|---|-----|-------------|--------------------|
| 1 | Day 1 loop, 2026-08-10 | `2026-08-10.csv` | 4 legs, 08-10 only, `T00001–T00003` |
| 2 | Day 2 loop, 2026-08-11 | `2026-08-11.csv` | **9 legs, 08-10 + 08-11**, `T00001–T00007` |
| 3 | PR #7 verification, pinned | `2026-08-10.csv` | **4 legs, 08-10 only**, `T00006–T00008` |

Run 3 is the truncation. It is not a bug in the filter and not a bug in the guard — it is the
script doing precisely what it is documented to do, aimed at a stale fixture.

### Why the guards did not fire

Three guards could have caught this and each is correctly scoped past it:

- **FILTERED-EXPORT GUARD** (~line 432) compares `prior_bots` to the bots in the new export. The
  08-10 export contains all three bots that traded on 08-10; the 08-11 export adds no *new bot*, only
  more rows for the same bots. `dropped` is empty. The guard protects against a bot vanishing, not
  against a **day** vanishing.
- **THE REFUSAL ASSERTION** (~line 592) kills the run if any row with `open_date < LEDGER_START`
  reaches the writer. Every surviving row is 2026-08-10, i.e. `>= LEDGER_START`. Passes cleanly.
- **The "would erase them" refusal** (~line 415) only fires when `data/raw/` is *empty* and
  `trades.csv` is not. `data/raw/` had three exports. Never reached.

**There is no guard on the axis that actually moved: the max `open_date` of the rebuilt ledger going
backwards.**

### The `LEDGER_START` / straddle-rule check — clean, ruled out

`LEDGER_START = "2026-08-10"` (`build_ledger.py:108`, read directly today). It is the correct
Day-0 value, set at commit `621baf43` (2026-08-08) and re-proven at `6b6ea59c` (2026-08-09,
"LEDGER_START 2026-08-10 set (n=0 proven)"). It has not been edited since. The filter is on
`open_date` per the straddle rule, and it is behaving correctly:

- `data/raw/2026-08-11.csv` — 1,395 rows, 1,386 of them pre-cutover, **9 post-cutover** (08-10 + 08-11).
- `data/raw/2026-08-10.csv` — 1,390 rows, 1,386 pre-cutover, **4 post-cutover** (08-10 only).
- `data/ledger_meta.json` — `post_cutover: 4`, `pre_cutover: 1386`, `source_export: "2026-08-10.csv"`.

The arithmetic ties exactly. `LEDGER_START` filtering is **not** the cause; `straddlers.csv` is
header-only and correct. The `source_export` field in `ledger_meta.json` is the tell that was
already on disk and unread: it names the 08-10 fixture, not the newest export.

---

## 2. The exact commit

**`0051b5e660f4b11f5416f0d7058ea1dd03faafb9`** — *"Phase 0 CI: hermetic daily.sh, stable trade_id,
UNCLASSIFIED refusal, green CI."*, branch `phase0-ci-2026-08-12`, authored **2026-08-12 20:03 ET**,
merged to `master` as **PR #7**.

Verified by reading `data/trades.csv` out of the committed trees:

| Commit | When (ET) | `trades.csv` | Dates | trade_ids |
|---|---|--:|---|---|
| `81fc270a` Day 1 | 08-10 16:37 | 4 rows | 08-10 | T00001–T00003 |
| `19ccc719` Day 2 — *"ledger $1,200/9 legs"* | 08-11 16:52 | **9 rows** | 08-10, 08-11 | T00001–T00007 |
| `8a25c956`, `0a2d0216`, `21544c47`, `27a297db` | 08-11 | 9 rows | 08-10, 08-11 | T00001–T00007 |
| **`756e36b5`** *"Track .claude/"* — **last good** | **08-11 20:19** | **9 rows** | **08-10, 08-11** | T00001–T00007 |
| **`0051b5e6`** PR #7 — **the truncation** | **08-12 20:03** | **4 rows** | **08-10** | **T00006–T00008** |
| `01a98752` … `456fd5c6` (HEAD) | 08-16 → 08-17 | 4 rows | 08-10 | T00006–T00008 |

**`756e36b5` is the last commit where `trades.csv` held multiple days.** `0051b5e6` is its direct
child and the commit where the rows disappeared. Every commit since carries the 4-row file; the
truncation reached `master` through the PR #7 merge and has been the committed state for five days.

### The 08-16 rewrite did not lose anything further

`data/trades.csv`, `bots.csv`, `ledger_meta.json` and `hedge_tournament.csv` all carry mtime
**2026-08-16 19:45:08 UTC** (scripts, from the checkout, 19:30:03 UTC) — one `daily.sh 2026-08-10`
run, ~0.25 s end to end. Its output is **byte-identical to the already-committed 4-row state**. It
re-derived the same truncation; it did not deepen it. The premise in T-03 that the rewrite happened
on 08-16 is off by four days: **it happened on 08-12, in `0051b5e6`.**

---

## 3. The orphan `trade_id` — expected, and a real latent defect

`hedge_tournament.csv` holds `2026-08-11 / T00005`, and `T00005` does not exist in `trades.csv`.

**Why the row survived:** `hedge_tournament.py` is an upsert keyed per date — line 354,
`kept = [r for r in existing if r["date"] not in touched_days]`. A run pinned to 08-10 touches only
08-10 and copies every 08-11 row through verbatim. So `hedge_tournament.csv` is the only accumulator
that *outlived* the truncation, which is exactly why it is the surface where the damage became
visible.

**Why the number changed:** PR #7 added `max_existing_tid()` (~line 182), which continues the
counter from ids already persisted in `hedge_tournament.csv` and in other days' `trades.csv` rows.
In the PR #7 session two runs happened in order:

1. a run on the 08-11 export → 08-11's `130PM` condor was assigned **`T00005`** and upserted into
   `hedge_tournament.csv`;
2. the pinned 08-10 run → `max_existing_tid(day="2026-08-10")` reads back `T00005`, so 08-10's
   condors start at **`T00006`**, and `trades.csv` is rebuilt from the 08-10 export alone.

Result: hedge rows at `T00005`/`T00006`, a ledger holding only `T00006`–`T00008`. This is also what
resolved the older `check_docs_vs_csv.py` contradiction "`T00001` persists across 2 dates" — the ids
stopped colliding and started dangling instead.

**The latent defect.** `docs/rules-catalog.md` §1.3 guard 2 already states the rule:

> `trade_id` is regenerated every rebuild, not stable across runs; any cache/log must key on
> `(bot, open_date, short_put, short_call)`, never `trade_id`.

`hedge_tournament.csv` keys on `(date, trade_id, leg identity, rule)` — it **violates the guard it is
covered by**. PR #7 made ids *monotonic*, not *stable*: they still depend on which day a run was
pinned to and in what order runs happened. Every cross-file join on `trade_id` is unsound by
construction, and will silently re-break on the next rebuild even after this incident is repaired.
That is tracker T-10's subject, and it is a genuine defect independent of the truncation.

---

## 4. daily.sh stage receipts

**There are none for August.** `data/receipts/` stops at `mirror-baseline.txt`, 2026-08-04. Nothing
in the eight-stage pipeline writes a per-run receipt; `data/ledger_meta.json` is the only per-run
artifact and it is *overwritten* by each run, so it records the last run and no history.

Corroborating per-run traces that do survive:

- `data/brief/2026-08-11_brief.json` — mtime **19:30:03 UTC** (i.e. it arrived with the git
  checkout, not from a run), while `2026-08-10_brief.json` is **19:45:08 UTC** (written by the run).
  Confirms exactly one, 08-10-pinned run on 08-16.
- No `2026-08-12/13/14` brief or tape file exists.

The absence of receipts is why a rebuild that walked the ledger *backwards* left no alarm anywhere
except the dangling id in `hedge_tournament.csv`.

---

## 5. What is recoverable

**08-10 and 08-11: fully recoverable, two independent ways. Nothing is lost.**

1. **Git.** Commit `756e36b5` (and `19ccc719`, `8a25c956`, `0a2d0216`, `21544c47`, `27a297db`) each
   hold the 9-row `data/trades.csv` verbatim.
2. **Re-derivation.** `data/raw/2026-08-11.csv` (1,395 rows, 433,394 bytes, mtime 2026-08-11
   20:23 UTC) is the full-history source export. `python3 scripts/build_ledger.py` with **no date
   argument** selects it via `newest_raw()` and reproduces the 9 post-cutover rows.

Because the OA export is full history, path 2 is authoritative and path 1 is a cross-check. They
should agree; if they do not, that is a second finding.

**08-12, 08-13, 08-14: absent from the repo, recoverable only from OA.**

No export for those dates was ever placed in `data/raw/` (contents: `2026-08-07.csv`,
`2026-08-10.csv`, `2026-08-11.csv` — nothing else). No brief, no tape, no capture. This is a
**capture gap, not a deletion** — no run ever deleted them because they never arrived.

Scale, from `docs/gf-entry-gate-forensics-2026-08-17.md` (first-hand read of the OA closed-position
export, same day): **34 legs across 08-10 → 08-14**. The repo's best available reconstruction covers
**9**. Roughly **25 legs across three trading days are missing from the working ledger**, an order
of magnitude larger than the 5 legs the truncation removed. That export was supplied to the 08-17
session but was never saved into `data/raw/`; it may still be in Andy's downloads, and OA can
re-export it regardless.

**Unrecoverable outright:** only the per-day OA *bot Log* decision records for 08-10 → 08-13 — OA
retains ~25 minutes and they had already expired when read on 08-17 (that doc, §"NOT EVALUABLE").
Position-level data is not affected.

---

## 6. Contamination of the reporting surface

Per `CLAUDE.md` §3, `STATUS.md` is the numeric source of truth. It currently reads
`generated 2026-08-10`, **`$500 · 4 legs · 3 bots`**, and is derived from the truncated ledger. Every
figure on it — headline P/L, champion record, focus/monitor tables, the allocation audit, the hedge
tournament section — is the 08-10-only slice presented without qualification.

Any decision taken off `STATUS.md` since 2026-08-12 was taken on **1 of 5** trading days.
`dashboard.html` (mtime 2026-08-16 19:45 UTC) has the same provenance.

Also worth flagging, not established here: an earlier session note recorded *"08-12 DAY 3:
cum $1,795 / 14 legs."* No export, ledger state, or commit in this repo ever contained 14 legs. That
figure did not come from `trades.csv` and should be treated as unsourced until reconciled against a
fresh OA export — `CLAUDE.md` §10, no number without its source file.

---

## 7. Fix options — GATED, nothing applied

All five are recommendations only. None has been executed; no file outside this report was written.

**G-1 — Restore the ledger (do this first, and only this, to stop the bleeding).**
Take a fresh OA positions export covering the full window, save it as `data/raw/2026-08-14.csv`
(or later), then run `scripts/daily.sh` **with no date argument** and let `newest_raw()` pick it.
That rebuilds all five trading days in one pass and regenerates `STATUS.md` from a complete ledger.
Do **not** restore the 9-row file from `756e36b5` as the fix — it would re-freeze a ledger that is
still missing three days, and it is only worth doing as a cross-check against the re-derived output.
*Gated: it writes the numeric source of truth.*

**G-2 — Add a monotonicity guard to `build_ledger.py`.**
Refuse, rather than overwrite, when the rebuilt ledger's maximum `open_date` is **earlier** than the
prior `trades.csv`'s maximum `open_date`, unless an explicit `--allow-rewind` is passed. This is the
one axis none of the three existing guards covers, and it is the check that would have stopped
`0051b5e6` at the moment it ran. *Gated: it changes the ledger writer's refusal contract.*

**G-3 — Separate the fixture path from the live ledger.**
CI determinism runs should write to a scratch root, not `data/`. `build_ledger.py` already
parameterises `RAW`/`OUT`/`META_PATH` for its self-test (~line 686) — a `--root` flag plus
`daily.sh` honouring an output root would let `scripts/daily.sh 2026-08-10` prove determinism
without ever touching the real ledger. This removes the incident class, not just this instance.
*Gated: it changes `daily.sh`'s contract and the CI invocation.*

**G-4 — Re-key `hedge_tournament.csv` on the natural key (this is tracker T-10).**
Key on `(bot, open_date, short_put, short_call)` per `rules-catalog.md` §1.3 guard 2, and migrate
the existing accumulator rows. Until this lands, `trade_id` joins across files stay unsound and the
dangling reference will recur on any pinned rebuild — including after G-1. *Gated: schema change to
a persisted accumulator; needs a migration, not an edit.*

**G-5 — Write per-run stage receipts.**
`daily.sh` should append a receipt per run to `data/receipts/` carrying the resolved export path,
`LEDGER_START`, row counts in/out, the min/max `open_date` written, and the file hashes — rather
than only overwriting `ledger_meta.json`. This incident was silent for five days because no run left
a trace anything could diff. *Gated: new artifact in a tracked directory.*

**Sequencing note.** G-2 before G-1 if both are authorized in one sitting — otherwise the restoring
run is itself unguarded.

---

## 8. Open questions, recorded not inferred

1. Whether the OA closed-position export read by the 08-17 session is still on disk somewhere
   outside this repo. If it is, G-1 needs no new OA capture.
2. Whether re-deriving 08-10/08-11 from `data/raw/2026-08-11.csv` reproduces `756e36b5`'s 9 rows
   exactly. Not tested here — testing it writes `trades.csv`.
3. The provenance of the "$1,795 / 14 legs" figure (§6).
4. Why no export was captured on 08-12, 08-13 or 08-14 — process gap, OA availability, or something
   else. Not established.

---

## Verification

- Working-tree facts read via `device_bash` on 2026-08-17; no stage-back reads were used (§9.1a).
- Git history read by direct `zlib` decompression of loose objects in `.git/objects` — no `git`
  process, no index, no lock file. All objects were loose (`.git/objects/pack/` is empty), so the
  full reflog range was resolvable.
- Row counts, dates and `trade_id` sets in §2 are parsed from the committed blobs themselves, not
  from commit messages.
- Nothing in this repo was modified except the creation of this file.

**Hand-off.** New untracked file: `docs/ledger-truncation-forensics-2026-08-17.md`. No tracked file
was touched — `session-log.md`, `RULINGS.md` and `state.md` are deliberately untouched so this does
not collide with the concurrent session's end-of-day freeze. Claude does not commit.
