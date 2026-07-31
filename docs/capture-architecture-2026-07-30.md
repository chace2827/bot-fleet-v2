# Capture architecture — decided 2026-07-30 (Phase 2, first action)

*Open Question #1 is answered. This doc records the answer and what follows from it.*

## The question
Does OA's **Export Data** CSV carry a bot-name column? It decides whether position→bot attribution can be
read directly, or has to be reconstructed from symbols and timestamps.

## The answer: YES — `botName` is column 1
Export taken 2026-07-30, saved at `data/captures/oa_export_positions_2026-07-30.csv`.
**26 columns, 1,386 rows, 32 distinct bots, 2026-03-05 → 2026-07-02.**

```
botName,type,description,symbol,status,quantity,daysInTrade,openPrice,closePrice,premium,
pnl,ror,returnPct,risk,ev,alpha,highReturnPct,lowReturnPct,highReturnPctDate,lowReturnPctDate,
expiration,openDate,closeDate,tags,underlyingOpen,underlyingClose
```

## What follows

**1. The export is the ledger source. The bookmarklet is the config source.** Clean split, no overlap:
- `Export Data` → **what happened** (positions, P/L, risk, MFE/MAE, underlying). Keyed on `botName`.
- Bookmarklet `/bots` → **what is configured** (the roster, the 18 dashboard fields, automation trees) and,
  with screenshots, the toggle states that no text capture can reach.

**2. No attribution reconstruction is needed.** This was the expensive branch and it is closed.
`build_ledger.py` joins on `botName` directly. In particular `highReturnPct` / `lowReturnPct` and their
dates are native MFE/MAE — the drift detector's "declared PT reached but no PT-consistent exit" and
`mfe_date == close_date` fingerprints read straight off the export with no derivation.

**3. `risk`, `ror` and `ev` ship per position.** R can be computed at ingest rather than reconstructed,
which is what the R-comparison discipline needs.

**4. The export is live while the account is inactive.** It returned positions closing as late as 7/27
despite the subscription having lapsed on 6/30 — so exports are not gated by subscription state. Useful:
the pre-sweep record can be pulled at any point before Day-0.

## Reconciliation against the frozen v1 ledger — clean, with one real finding

| | Export | Frozen ledger | Delta |
|---|---|---|---|
| Rows | 1,386 | 1,380 | **+6** |
| Total P/L | **−$82,498** | −$83,130 | **+$632** |
| Distinct bots | 32 | 32 | 0 |

The export's −$82,498 matches the `/bots` dashboard **CLOSED P/L** figure exactly.

**All 6 extra rows are mirror positions that closed after the 7/02 freeze** — opened before the fleet
stopped, closed afterwards, so the ledger's last ingest never saw them:
`3DTE $140-$350` +3 rows / +$85 · `Nigiri-Paper-v1` +1 / +$80 · `Tasty Condor` +1 / +$405 ·
`Trendy-Paper-v1` +1 / +$62. The 0DTE bots have no such tail by construction; **multi-day mirrors do.**

⚠️ **Consequence: `data/mirror_baseline.csv` must be built from this export, not from the archived
`trades.csv`.** The mirrors are exactly the bots with a post-freeze tail, and they are exactly the bots
that table is about. Using the ledger would understate four of the seven.

*(The dashboard's TOTAL P/L of −$92,966 differs from CLOSED −$82,498 by the open positions — 4 on
`QQQ long call`, 1 on `Tasty Condor`. Not a discrepancy.)*

## Roster confirmed: 35 active bots, 3 of them zero-trade
`data/captures/oa_bots_capture_2026-07-30.txt`. The capture is the roster authority; `bots_meta.csv`
carries 33 rows covering only the 32 bots that ever traded.

**Zero-trade (absent from the export entirely):**
1. `TEST QQQ-IC-0DTE-HedgeC-S3 Clone` → **DELETE**
2. `QQQ-IC-0DTE-InvFilter-Wide150` → **DELETE**
3. `DIR-SPX-PutVIX22-SL75` → ⛔ **KEEP — do not delete.** Zero positions because its **VIX≥22 gate
   correctly never fired** in 22 days, not because it is a test bot. OOS-validated, in the leave-in-place
   group. This is the case that proves "empty → delete" needs the disposition table as a guardrail.

**Disposition closes with no remainder: 35 = 20 archived + 2 deleted + 4 cloned + 9 untouched.**

## One observation, recorded not re-litigated
Two bots in the archive-directly group show positive records on the dashboard:
`IC-SPX-Fortress-Unstopped` **+$2,350 / 26 closed / P-factor 6.22** and `IC-SPX-Fortress-Defang`
**+$600 / 26 closed / 1.71**. The decision to archive them was taken on grounds of *role* — the greenfield
family supplies the new control and A/B arms, built matched from the start — not on grounds of
performance, and n=26 is far below the adopted gates either way. Noted here so the numbers are on the
record rather than discovered later and mistaken for an oversight.
