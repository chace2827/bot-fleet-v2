# 2026-09-07 — catch-up close bundle (09-01…09-04) + Layer 2 + drift audit

Cowork + Claude in Chrome, 12:24–13:00 ET. **READ-ONLY on OA — no edit was made and none was
queued.** ACCOUNT = Paper Trading on every page; `TR ****4219` never selected.
Labor Day: markets closed, so this is a config-drift + catch-up read, not a trading day.

| file | what it establishes |
|---|---|
| `01-drift-verdict-2026-09-07.md` | §B. **NO CONFIG DRIFT.** 44/44 bots byte-identical to the 09-02 POST capture on both instruments (`allbots`; `i.sticon` AUTOS/EXITS). AUTOS 18/44, EXITS 16/44. Includes the method and why it is a signature diff. |
| `02-roster-2026-09-07-124739.txt` | §B raw. The `/bots` capture, `oa_grab_page.js` instrument, byte-identical to the in-page original (len 10,291, rolling ck `cd7c4ba4`, verified both sides). Also bundled by `capture_bundle.py` into `data/captures/2026-09-07-roster/`. |
| `03-layer2-2026-09-07.md` | §C. **Quantity PASSES** on all seven arms (26 ct × 6, 1 ct Canary). **Both-sides FAILS** — put side only on 09-04, filtered at "Mid price is $0.07". 09-03 had no fills: QQQ up >+0.75%. |
| `04-followups-2026-09-07.md` | §D. No automation node sets position size on `3DTE $140-$350` (22 input-refs, 0 literals) — but the input reads **26% of net liquid**, which contradicts `R-2026-09-03-3DTE-POSITION-SIZE-CORRECTION`. `GF-QQQ-IC-Ride-Delta` still AUTOS OFF. |

Ingest input: the OA closed-position export Andy attached, placed at `_inbox/`
(gitignored) and read via `INGEST_DOWNLOADS`; installed as `data/raw/2026-09-04.csv`.
sha256 `07a70a3652d55e9c1d1d5cddb3d7955bb778bb4fbeb03ed7bbde31a923274f73`, 251 data rows,
closeDate 2026-08-10…2026-09-04. It is **range-limited, not full history** — safe here only
because post-cutover bot coverage is identical (18 bots, zero dropped) to the 08-31 full
export; checked by dry-run and a full scratch-root close before the repo was touched.

Not in this bundle, on purpose: screenshots. Toggle state is carried by the
`i.sticon` title attributes in `02-roster-…txt` and by the signature diff in `01-…md`;
the one screenshot-only claim (Ride-Delta AUTOS OFF) is corroborated there too.
