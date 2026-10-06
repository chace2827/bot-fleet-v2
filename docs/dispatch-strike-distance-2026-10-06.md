# Dispatch — T2 strike-distance sweep (Devin, backtests only)

**Purpose:** answer the open item from the 2026-08-26 loss (short call only 15 pts / 0.19% OTM at
entry): **does a wider cushion at entry, alone or combined with Touch $10, cut bad days better than
the current .10Δ strikes?** Scoring is `R-2026-10-06-TAIL-SCORING-RULE` on **gross** R (`R-2026-10-06-TAIL-FEES-IGNORED`), with the
**holdout split** of `R-2026-10-06-TAIL-HOLDOUT`: choose on 2021-10→2024-12, confirm on 2025-01→present.

**Gate:** dispatch only **after** the loss-packet calibration (`docs/dispatch-loss-packet-2026-10-06.md`,
run 1) passes Cowork review. Two OA-driving sessions must never overlap.

## Arms — 8, one compare page, exit and short delta are the only variables
Base = T1 `ZZ-COWORK-2026-10-06-T1-A0-ride` (`ZT217913212733763171103`): SPX IC, 0 DTE, long legs
$5 beyond shorts, 1 contract, 13:30, Change % −0.75…+0.75, 5y.

| arm | short put / short call | exit |
|---|---|---|
| D05-ride | −.05 / .05 delta | none |
| D05-t10 | −.05 / .05 | Touch $10 |
| D07-ride | −.07 / .07 | none |
| D07-t10 | −.07 / .07 | Touch $10 |
| D10-ride | −.10 / .10 | none — **must reproduce T1 A0 row-for-row** (control check) |
| D10-t10 | −.10 / .10 | Touch $10 — **must reproduce T1 A3** |
| D15-ride | −.15 / .15 | none |
| D15-t10 | −.15 / .15 | Touch $10 |

D10-* exist already (A0/A3). Re-read them and **do not rebuild**. Build the 6 new arms via
Compare → ⋮ → Add Variation on A0. Each variation changes only the fields in its row.

---

## The prompt (paste below the line)

---

You are working in the `bot-fleet-v2` repo, connected as a local folder. Fresh session.

**Read, in order:** `CLAUDE.md` (§4, §9.1a) · `.agents/skills/option-alpha/SKILL.md` ·
`.agents/skills/oa-drive/SKILL.md` · `docs/tail-test-s2-2026-10-06.md` ·
`data/captures/2026-10-06-t1-s2-tail/README.md` (the T1/T1b method, the fee derivation, and the
caveats) · this file.

### ⛔ BOUNDARY
0. You do not log in. Assert `Paper Trading`. If `/login` appears: STOP.
1. **Backtests only.** ✅ Create and run the 6 new arms named `ZZ-AGENT-<YYYY-MM-DD>-T2-<arm>`.
   ⛔ Do not modify, rename, re-run or delete any existing `ZZ-COWORK-*` or `ZZ-AGENT-*` test.
   ⛔ No `Create Bot`, no bot, automation or position surface edits.
2. DOM/JS reads OK. No API calls, replay, network panel or recorder.

### TASK
1. Open `/backtests/compare/ZT217913212733763171103`. For each new arm: ⋮ → **Add Variation** →
   set short put delta, short call delta (the leg picker's `delta` recipe, value from the table) and,
   for `-t10` arms, Touch = $10. Long legs stay `$5.00 below/above short leg`.
   **Before Run:** dump the drawer's serialized inputs and confirm that only `shortPut`, `shortCall`,
   `touch` and `name` differ from A0 (A0's `touch` is empty). Paste the diff into the raw capture.
   Two unexpected fields = not an arm: stop and report.
2. Run all 6. Then confirm **every arm has the same date set as A0**. If a delta yields no fill on
   some days, the date sets differ: report the count and the missing dates, and do **not** pad them.
3. Export each new arm's positions with **Download CSV**. Also export A0 and A3, so the bundle is
   self-contained.

### ANALYSIS — per arm, paired by date
- **vs A0 (current ride):** bad days (≤ −0.5R) · fixed / created · exact two-sided sign-test p ·
  mean R · keeps % of A0 mean · gross P/L · max DD (R) · worst-5% mean · touch-exit count.
- **Fees:** est. net = gross − $3.16 × (opens + touch closes). The $3.16 per 1-lot IC transaction is
  the README's derived figure. **Re-derive it** from any arm's `Estimated fees` insight and state
  both values.
- **Rule verdict (gross R):** name the winner on the 2021-10→2024-12 window, then report whether that
  same arm passes the rule on 2025-01→present (holdout). Net-of-fees may be listed as information only.
- Copy the 2026-08-26 and 2026-09-30 rows from every arm verbatim (the two register days).
- ⚠ Carry the T1 caveat: the backtester's exits stop ~15:45.

⛔ No recommendation about any bot.

### DELIVERABLE
`data/captures/<date>-t2-strike-distance/`: `01-raw-capture.txt` (the diffs, test ids, rendered stats),
`02-analysis.md` (naming its source CSVs with sha256), every CSV raw, `README.md` (purpose ·
timestamp with TZ · file/sha256/what · the table · both verdicts · `## Assumptions` ·
`## Questions for Andy` · `## Refusals`), `SHA256SUMS.txt`. Append a close-out to
`docs/session-log.md`. No git. No writes under `~/.claude`.

**Stop conditions:** 401/403/429 · `/login` · non-Paper · terms/payment prompt · an arm diff with
unexpected fields · D10 arms not reproducing A0/A3 row-for-row.

### REPORT
The table, both verdicts, fee re-derivation, the 08-26/09-30 rows, bundle path, refusals.
