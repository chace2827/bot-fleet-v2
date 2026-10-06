# 07 — Debrief: 2026-08-27 packet run

## Section timings (this run, post-pilot — agent-side estimates, ±1 min)

| § | ~min | browser actions | notes |
|---|---|---|---|
| §1 ledger | <1 | 0 | local awk only |
| §2 OA positions | ~7 | ~45 | runner pass ~3 min (Load-more to the AUG-27 group + 2 drawer opens + 6 automation-log opens) + supplementary pass ~4 min (re-nav + re-page + same opens) for leg classes + UTC trade ids the runner omits |
| §3 bot log | ~4 | ~15 | runner day-load ~1 min (150 rows ≈ 2 Load-more clicks) + two decision-text passes (~1.5 min each: re-nav, day reload, 4 row opens, pager iterations) |
| §4 tape | <1 | 0 | 1min fails (~28 trading days out) → 5min pull + derive |
| §5 backtests | ~6.5 | ~50 | runner ~3 min (11 hydrates × ~6.5s + extract) + absence proof ~3.5 min (probe: A0 paged to 825 rows, plus an Aug-dates dump) |
| §6 + files + README + SHA | ~5 | 0 | writes only |
| **total** | **~23–25** | | pilot was a separate ~15 min, one-time per calibration |

**Slowest on this run: §5** — but ~3.5 min of it was proving a row's ABSENCE
(paging A0's grid to exhaustion). The structural long pole on a normal run is
§2's Load-more depth (same as the reference run's finding). The avoidable cost
on both runs was duplicated passes: v2 removes the second §2 and both §3
reloads, putting §2 and §5 at ~3 min each — the §5 floor is ~75s of mandatory
page hydrates.

## Can §3 skip the full log load and jump to the close minute?

**Not under the current spec.** The dispatch requires "the list of runs …
from 13:25 to 16:00" verbatim — that forces loading down to the 13:20
boundary, which the runner already does (stops at last row ≤13:20 or day end;
the 250/150-row totals are the day itself, not overshoot). The close-minute
**decision texts** alone would need only the FIRST loaded page — nothing logs
after the close on a bot that goes flat — so a spec variant without the run
list would cost zero Load-more clicks. As long as the run list stays a
deliverable, the load is already minimal.

## PROPOSED-packet-runner-v2.js — changelog

1. **Args**: `--k v` and `--k=v` both accepted (v1's parser silently read
   space-separated values as `true` despite the usage line showing spaces).
2. **Exit**: `ws.close()` + `process.exit` after print — v1 leaked the CDP
   WebSocket and never exited (killed by hand on both runs).
3. **§3 decision texts serialized**: `--minutes=H:MMPM,...` opens those rows'
   INFO cells and captures every pager iteration into `s3_botlog.decisions` —
   v1 returned `openRun` as a callback (unserializable), forcing a second
   script per run.
4. **§2 enrichment**: captures leg `.strike` classes, trade item `data-id`s
   and `em.from[data-value]` UTC timestamps inline — removes the second §2
   pass used on this run.
5. **§5 absence-proof paging**: posgrid paged until the target date appears,
   the oldest loaded row predates it (sorted newest-first ⇒ absent), or
   Load-more vanishes; emits `oldest`/`predates`/`exhausted` — v1 read only
   the first 100 rows and could not distinguish "absent" from "not loaded".
6. **`out.timings`**: per-section ms + total, so the next run's §-timing
   question answers itself with numbers.
