# Run receipts

Proof that the Phase-3 scripts ran **on Andy's machine**, not only in a cloud sandbox.
Written 2026-07-31. Regenerate any time; nothing here is a reporting input.

| File | What it proves |
|---|---|
| `validation-matrix.txt` | `execution_audit.py --validate` — **21/21 PASS**, detector v1.0.0 sha `67a537977c5d0896` |
| `archive-fixture-run.txt` | the detector run against the frozen v1 archive — 6 RED / 13 AMBER / 291 context / 21 not evaluated |
| `archive-fixture-findings.csv` + `_meta.json` | those findings as data, with the detector version stamped |
| `build-ledger-receipts.txt` | Receipt A behaviour-neutral regression · Receipt B the straddle rule · Receipt C the refusal |
| `straddlers-receiptB.csv` | the 6 mirror straddlers (+$632) the rule produces independently |
| `ledger_meta-receiptB.json` | that run's receipt: 0 post-cutover / 6 straddlers / 1,380 discarded |

## Two things to read carefully

**1. The archive fixture findings live HERE, not in `data/`.**
The detector's live output is `data/execution_audit_findings.csv`, which reads the
**post-cutover** working ledger and is currently empty (n=0). The archive run is a
*test-fixture* result. Putting archive findings in the live `data/` directory would put
pre-cutover numbers on a working surface — the exact thing the cutover exists to prevent.

**2. `data/ledger_meta.json` currently carries `ledger_start = 2099-01-01`. THIS IS A
PLACEHOLDER, NOT A CUTOVER DATE.**
Day-0 has not happened, so no real `LEDGER_START` exists yet. To produce a live receipt at
all, the run was given a deliberately impossible sentinel date, passed **via the environment**
so the file records `ledger_start_source: "$LEDGER_START"` — an override, never the constant.
`LEDGER_START` in `scripts/build_ledger.py` is still `"UNSET"`, and a bare
`python3 scripts/build_ledger.py` still exits 1 and writes nothing.

**On Day-0: set the constant in `build_ledger.py` and re-run. That overwrites this file.**
Until then, treat any `ledger_start` you see here as meaningless.
