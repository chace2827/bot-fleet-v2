# T-48 GF call-side study — LEDGER-DERIVED PREP (partial)

**Status: PARTIAL. This is NOT the T-48 deliverable.** It covers only step B.1 of
`drafts/_dispatch-2026-09-08-close-and-t48-cowork.md` plus the ledger-derived half of B.4.
Steps B.2 (OA Log reads), B.3 (ScannerB config hash) and all of section A require Chrome +
Option Alpha and the 2026-09-08 close, neither available to this session (see "Not done", below).

Produced 2026-09-07 by a Claude Code terminal session, offline, from `data/trades.csv` only.
Source file at time of read: sha256 recorded in the report; no OA contact of any kind.
The 09-08 Cowork session should fold this into `04-t48-call-side-study.md` and re-derive rather
than trust it.

## 1 · The family splits into two scanner groups

Shape by arm and fill-day, all `GF-QQQ-IC-*` rows in `data/trades.csv`:

| day | Canary | PT50 | Ride | SL100 | SL200 | Touch0 | Trail | **Ride-Delta** |
|---|---|---|---|---|---|---|---|---|
| 2026-08-14 | put | put | put | put | put | put | put | put |
| 2026-08-17 | put | put | put | put | put | put | put | put |
| 2026-08-19 | both | both | both | both | both | both | both | **put** |
| 2026-08-20 | both | both | both | both | both | both | both | both |
| 2026-08-21 | put | put | put | put | put | put | put | put |
| 2026-08-25 | both | both | both | both | both | both | both | **call** |
| 2026-08-26 | both | both | both | both | both | both | both | both |
| 2026-08-28 | both | both | both | both | both | both | both | both |
| 2026-08-31 | both | both | both | both | both | both | both | **put** |
| 2026-09-02 | both | both | both | both | both | both | both | **—** |
| 2026-09-04 | put | put | put | put | put | put | put | **—** |

Seven arms move in **exact lockstep** on all 11 days — this is the ledger evidence for the
dispatch's "the family shares the scanners", and it identifies the "seven GF arms" of A.3 as
Canary / PT50 / Ride / SL100 / SL200 / Touch0 / Trail.

**`GF-QQQ-IC-Ride-Delta` is not on the shared scanners.** It diverges on 4 of 11 days
(08-19 put-only, 08-25 **call-only**, 08-31 put-only, and no fill at all 09-02 or 09-04).
Treat it as an independent observation, not a family member, in the study. Its 08-25 call-only
day is the only call-only day anywhere in the GF complex.

Fill-days match the dispatch's expected list exactly: 08-14, 08-17, 08-19, 08-20, 08-21, 08-25,
08-26, 08-28, 08-31, 09-02, 09-04. No extra days, none missing.

## 2 · Per-day credits and P/L — the seven lockstep arms

| day | put credit | call credit | put legs | call legs | put P/L | call P/L | day P/L | shape |
|---|---|---|---|---|---|---|---|---|
| 2026-08-14 | $0.07 | — | 7 | 0 | +35 | 0 | **+35** | put-only |
| 2026-08-17 | $0.10 | — | 7 | 0 | +43 | 0 | **+43** | put-only |
| 2026-08-19 | $0.07 | $0.07 | 7 | 7 | +30 | +32 | **+62** | both |
| 2026-08-20 | $0.07 | $0.07 | 7 | 7 | −4 | +36 | **+32** | both |
| 2026-08-21 | $0.07 | — | 7 | 0 | +28 | 0 | **+28** | put-only |
| 2026-08-25 | $0.08 | $0.07 | 7 | 7 | +28 | +30 | **+58** | both |
| 2026-08-26 | $0.10 | $0.10 | 7 | 7 | +26 | −115 | **−89** | both |
| 2026-08-28 | $0.08 | $0.07 | 7 | 7 | +35 | +21 | **+56** | both |
| 2026-08-31 | $0.07 | $0.09 | 7 | 7 | +31 | +1 | **+32** | both |
| 2026-09-02 | $0.07 | $0.12 | 7 | 7 | +27 | −1 | **+26** | both |
| 2026-09-04 | $0.10 | — | 7 | 0 | +1,327 | 0 | **+1,327** | put-only |

- **Put-only rate: 4 / 11 fill-days = 36.4%.** Call-only: 0 / 11. Both: 7 / 11 = 63.6%.
- **Realised naked put-side P/L on put-only days (7 arms, sum): +$1,433.**
  Of that, +$1,327 is 09-04 alone, the first day at 26 contracts; the three 1-contract
  put-only days total +$106. Unit: raw leg P/L in dollars, as carried in `trades.csv` — this is
  **not** an R figure and must not be compared to one (`CLAUDE.md` §4).
- The only losing day in the window is 08-26, and the loss is entirely call-side (−$115 call vs
  +$26 put). QQQ closed 708.38→+1.5 that day (open 710.69, close 712.14) — an up-move into the
  short calls at 716/718.

## 3 · The $0.07 question — what the ledger alone establishes

Credit distribution over all 126 lockstep GF legs in the window:

| credit | put legs | call legs |
|---|---|---|
| $0.07 | 42 | 28 |
| $0.08 | 14 | 0 |
| $0.09 | 0 | 7 |
| $0.10 | 21 | 7 |
| $0.12 | 0 | 7 |

**No leg — put or call — ever filled below $0.07.** $0.07 is the observed floor of the whole
family, and 70 of 126 legs (56%) filled exactly at it.

This sharpens the 09-04 finding rather than explaining it. The 09-04 close recorded the call side
**filtered at $0.07 mid** (commit `55642fc`), yet 28 call legs across five other days filled at
exactly $0.07. A plain "reject if mid < $0.07" threshold is therefore **not** consistent with the
ledger; something else differed on 09-04. Two hypotheses for the Log read (B.2) to settle:

1. **A quantity interaction.** 09-04 is the first day at 26 contracts (sizing executed 09-02;
   the 09-02 positions had already opened at 1ct at 13:31 ET, so 09-04 is the first 26ct fill-day).
   Canary, detached to bot-local 1ct, also took no call side on 09-04 — but Canary shares the
   scanner, so that is expected either way and is **not** evidence against the hypothesis.
2. **The filter is on a value the ledger does not carry** — a pre-fill mid or a limit price that
   differs from the credit ultimately booked, so that "$0.07 mid" and "$0.07 credit" are not the
   same number. The ledger carries only the filled credit.

The ledger cannot distinguish these. **B.2's Log read is the decisive evidence**, and it should be
directed at 09-04 first, then at 08-14 / 08-17 / 08-21 for contrast.

## 4 · What could NOT be observed from the ledger

- **The terminal reason** for any non-fill. `trades.csv` records fills; a call side that never
  opened leaves no row. Every "put-only" above is an *absence*, and per `oa-platform-reference.md`
  §0.2 an absence is not an observation of a filter firing. Only the OA Log can supply the reason.
- **Gate outcomes** (range %, time window, "opened a position with call side today"), whether an
  order was built, and the candidate strikes on non-fill days.
- **Short-call delta and wing width as configured** — the ledger has realised strikes only, and
  only for legs that filled.
- **The put credit at the same minute the call was rejected.** The table's put credit is the
  filled credit at the put's own fill time, not a quote at the call's decision moment.
- **The counterfactual** "how often would $0.05 / $0.06 have cleared". Nothing below $0.07 exists
  in the ledger, so this is unanswerable without the Log's rejected-candidate mids.
- **ScannerB's current config hash** (B.3) — requires a fresh Library read.
- QQQ intraday range; only `underlying_open` / `underlying_close` per position are carried.

## 5 · Not done, and why

| dispatch step | status | reason |
|---|---|---|
| 0 · setup, Chrome/OA | **not done** | no browser tool and no `oa-driving` skill in this session |
| A · routine close 09-08 | **not done** | today is 2026-09-07; the 09-08 close has not happened. `_inbox/` holds `oa-export-2026-09-07.csv` only |
| A.3 · GF daily shape 09-08 | **not done** | same |
| A.4 · T-36 130PM count | **not done** | needs the OA readiness board |
| B.1 · fill-days + ledger shape | **DONE** | §1 above |
| B.2 · OA Log reads | **not done** | needs Chrome + OA |
| B.3 · ScannerB config hash | **not done** | needs Chrome + OA |
| B.4 · study file | **partial** | ledger half in §2–4; no Log data, so no mechanism reading and no `04-t48-call-side-study.md` written |
| C · records | **not done** | `session-log.md`, `state.md` and `portfolio.csv` deliberately untouched — marking T-48 "Ready for review" would be false while B.2/B.3 are outstanding |

No recommendation to change anything on OA is made or implied; per
`R-2026-09-07-GF-CALL-SIDE-SHAPE` the options are tabled and this is data only.
