# Step 2 — probe-bot selection, and the dispatch criterion that no bot can satisfy

**Session:** T-50 Evening 1, 2026-09-07 ET. **Ruling:** `R-2026-09-07-ARCHIVE-SWEEP-SESSION`.

## ⛔ FINDING P1 — the dispatch's step-2 criterion is unsatisfiable, and the hazard it guards is absent

The dispatch requires a probe bot that "DOES have closed positions with closeDate in
2026-08-01..2026-08-08 in the latest `data/raw/*.csv`". **No bot in the `Archive` group has one.
Not one row. Computed from the files, not recalled:**

| Surface | What it says |
|---|---|
| `data/raw/2026-09-04.csv` (the latest raw) | 251 rows; `closeDate` min **2026-08-10**, `openDate` min 2026-06-01. **Zero rows for any of the 20 Archive-group bots.** The current daily export is already range-shortened past 08-08, so it cannot answer the question at all. |
| `data/raw/2026-08-31.csv` (the last full-history raw) | 1,596 rows; 1,158 of them Archive-group. **Max `closeDate` across all 20 Archive-group bots = 2026-07-02.** Rows in 2026-08-01..08-08: **0.** |
| `data/trades.csv` (the working post-cutover ledger, LEDGER_START 2026-08-10) | 246 rows / 18 distinct bots. **Not one of the 20 Archive-group bots appears in it.** |

The dispatch's premise — "the export convention ('since 08-01') has rows for several of these bots
between 08-01 and 08-08" — is **false**. Every one of these 20 bots stopped trading on or before
2026-07-02.

**Consequence for the stated hazard.** `scripts/build_ledger.py` computes the FILTERED-EXPORT GUARD as
`dropped = prior_bots - {export botNames} - ops_bots`, where `prior_bots` is read from the existing
`data/trades.csv` (line 678/704). Since **no Archive-group bot is in `prior_bots`**, archiving any or
all 20 of them **cannot trip the guard**, whatever OA-archiving does to the export. The two-evening
split exists to protect against a hazard that does not exist on this roster.

## Ruling applied — derived, under `R-2026-08-31-DERIVED-RULING-AUTHORITY` clause (b)

`R-2026-09-07-T50-PROBE-WINDOW-VOID` — **the 08-01..08-08 window is dropped from the step-2 criterion
and replaced by full-history closed-row identity.** The probe still answers M-08 exactly as the
dispatch asks it (step 6 already specifies a *full history, no filter* export); it answers it on a
larger and stricter row set than the window would have given. Rejected alternative: STOP and return
the dispatch to Andy unrun — rejected because the criterion is falsified by file evidence, its
purpose is provably moot on this roster, and the M-08 question is fully answerable without it.
This changes no capital, sizing, kill criterion, pre-registration, go-live gate, or OA bot behavior.
**Andy may veto at commit review.**

## Probe bot chosen — `QQQ-IC-0DTE-Baseline`

The dispatch's own first preference. Every step-2 gate except the void window is met, and the
row-count fingerprint agrees across two independent surfaces:

| Gate | Value | Source |
|---|---|---|
| In the `Archive` group | Archive | `a5.bots.allbots` 18:42 read |
| AUTOS OFF | `status = off` / sticon "Scheduled automations are off" | model + DOM, both |
| EXITS OFF | `disableExits = 1` / sticon "…are off" | model + DOM, both |
| NO open positions | `pcount = 0` | model read |
| Not a `-ARCHIVED-` clone, not a mirror, not DIR | control bot, tag `control` | model read |
| Closed rows in full history | **43** | `a5.bots.allbots.closedCount = 43` **and** 43 rows in `data/raw/2026-08-31.csv` — two surfaces, exact agreement |

**Bot id:** `BOTfw5TkkCRF3317727290514286611` · seed $100,000 · posLimit 2 · tag `control` ·
account Paper Trading · TOTAL P/L -$31.6K / -31.6% · WIN RATE 73% · STREAK 1L.

## The 43 rows — the exact set the post-probe export must reproduce

Status split: **33 `closed`, 10 `expired`** (the probe therefore tests both status kinds).
`closeDate` span **2026-03-05 .. 2026-05-22**. `openDate` span 2026-03-05 .. 2026-05-22.
Per-date closed-row counts are in `02b-probe-rowset-QQQ-IC-0DTE-Baseline.tsv`, which is the
byte-level comparison target for step 6.
