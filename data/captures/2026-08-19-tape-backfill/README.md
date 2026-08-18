# Tape-backfill evidence — 2026-08-19

Landed under `R-2026-08-19-TAPE-BACKFILL-AND-VIX-SERIES` (Active). **Evidence only.** Nothing in
this capture changes a generator, a tape, a banked row, or a verdict. W1–W5 do that work and each
cites this directory.

## Why this exists, and why it was urgent

Tradier's 5-minute history is a **rolling window of roughly 57 days**. The intraday data for
2026-08-10 leaves that window around **2026-10-06**. After that it is unrecoverable. These captures
were taken while it was still reachable.

## `raw/` — Tradier v1 response bodies, **verbatim**

One file per endpoint call, named `{SYMBOL}_{DATE}_{interval}.json`, written as the exact bytes
returned by the API — no parsing, no re-encoding, no pretty-printing. 36 calls: 6 dates
(2026-08-10, -11, -12, -13, -14, -17) × 3 symbols (SPX, QQQ, VIX) × 2 endpoints
(`markets/history` daily, `markets/timesales` 5min). All 36 returned data.

`MANIFEST.json` records, per call: the endpoint, the exact query parameters, HTTP status, byte
count and sha256. The credential is never recorded — the auth field carries the literal
`Bearer <TRADIER_TOKEN from .env — not recorded>`.

`fetch_raw.py` is the capture tool, included so the calls are reproducible.

**A first-hand fact these captures establish:** `VIX_*_5min.json` returns a full 79-bar session for
every date. Tradier serves a VIX intraday series. `scripts/tape.py` has simply never asked for one
(the `sym != "VIX"` guard, ~line 358). That absence is a generator choice, not a data gap — the
premise W1 corrects.

## `derived/` — PROOF-OF-CONCEPT PRODUCTS, **not raw**

Everything in this directory is computed output. It is kept because it is what the investigation
actually examined, and because it cross-checks the raw captures. **Do not cite it as a source where
the raw bytes will do.**

- `*_tape.CANDIDATE-*.json` — 8 candidate tapes (4 dates × 2 symbol-selection modes, `gates` and
  `ledger`). Each carries `backfilled_at` and `backfill_evidence` recording the calls behind it.
  They are **candidates**: no committed tape is derived from them.
- `backfill_poc.py`, `probe.py`, `lookback.py` — the investigation's tools. `backfill_poc.py`
  deliberately reuses `scripts/tape.py`'s own helpers rather than reimplementing them, so schema
  identity is structural.
- `tw_baseline.csv`, `tw_backfilled.csv` — `data/trade_window.csv` before and after a simulated
  backfill. The delta they show is the banked-row correction W3 will make with evidence.
- `ht_backfilled_pre.csv` — hedge-tournament state observed during the investigation.
- `crosscheck.py` — the validation described below.

## The cross-check, and what it proves

`crosscheck.py` rebuilds the candidate tapes **from the raw captures alone** — it monkeypatches
`tape.py`'s `_get` so derivation reads the saved bytes and never the network — then compares against
the candidates the PoC produced live against the API.

Result: **4 of 4 match exactly.** Every OHLC value and all 237 five-minute bars (79 × SPX/QQQ/VIX)
are identical on every date.

Two fields are necessarily volatile and are normalized before comparison, stated here rather than
hidden: `generated` and `backfilled_at` (wall-clock stamps), and `backfill_evidence` (which records
the live call, absent by construction on a replay). Nothing else is excluded.

The match is the point: it establishes that the derived candidates are exactly what the raw Tradier
bytes imply, with no drift between fetch and derivation. The PoC pipeline is validated against its
own inputs before any of it is allowed to touch a committed tape.

## Integrity

`SHA256SUMS.txt` carries a sha256 for all 53 files in `raw/` and `derived/`.
