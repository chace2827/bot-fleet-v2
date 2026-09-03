# Batch A · STEP 0 — shared-scanner attachment enumeration (GATE)
Captured 2026-09-02 ~21:01–21:05 ET, Claude in Chrome, **READ-ONLY**. No OA edit made in this step.
ET date/time taken from the OA page's own header (`captured: Wed Sep 02 2026 20:59:36 GMT-0400`),
never the container clock (which reads 2026-09-03 UTC).
Surface: Automation Library, `https://app.optionalpha.com/bots/automations`.

## 1. Library inventory — 4 shared automations exist
| automation | attached-bot badge |
|---|---|
| Defang-Mon-S2-StrikeTouch | 2 bots |
| GF-Backstop-1552-FlatClose | 8 bots |
| **GF-ScannerA-PutSpread** | **8 bots** |
| **GF-ScannerB-CallSpread** | **8 bots** |

## 2. Attachment MEMBERSHIP — the list, not the count
Read by firing the row's own `data-click="showBots"` control and reading the resulting
`.menuitems` popup's child list from the DOM. Each popup was read while visible; the two popups
were distinguished by their `getBoundingClientRect().top` (303 for ScannerA's row, 358 for
ScannerB's row) so neither list was attributed to the wrong automation.

**GF-ScannerA-PutSpread — 8 bots:**
```
GF-QQQ-IC-Ride-Delta
GF-QQQ-IC-SL200
GF-QQQ-IC-Ride
GF-QQQ-IC-Trail
GF-QQQ-IC-PT50
GF-QQQ-IC-Touch0
GF-QQQ-IC-Canary
GF-QQQ-IC-SL100
```
**GF-ScannerB-CallSpread — 8 bots:** identical membership, same eight names.

**VERDICT: exactly the 8 `GF-QQQ-IC-*` arms on both. No non-GF bot is attached to either.**
The G-3a gate condition "any non-GF bot present -> STOP" does not fire.

## 3. Config hashes — `sha256(JSON.stringify({name, inputs, root}))`
Each automation opened FRESH from the library with a HARD RELOAD between opens (stale-editor-DOM
trap, `oa-driving` trap 6); read from `a5.bots.acedit.routine`, never from a DOM scrape.

| automation | expected (ruling G-3b) | observed 2026-09-02 | bytes | verdict |
|---|---|---|--:|---|
| GF-ScannerA-PutSpread | `1e5eb9936a1adf067af65a4841d42e755592f7c179f3c0cad477502dfdbfcdc8` | `1e5eb9936a1adf067af65a4841d42e755592f7c179f3c0cad477502dfdbfcdc8` | 5379 | **MATCH** |
| GF-ScannerB-CallSpread | `a925d490b8a0d2337566f47307fc52470da129935d3bd83d24389c6dc433dfb5` | `a925d490b8a0d2337566f47307fc52470da129935d3bd83d24389c6dc433dfb5` | 5044 | **MATCH** |

Byte counts also match the 2026-08-31 record (5379B / 5044B, `10-authorized-edits-2026-08-31.md`).
No version number was used as evidence anywhere in this step.

## 4. Open-position action `amount` — the lever field
Located by walking `routine.root` for any node carrying an `amount` key. **Exactly one node per
scanner carries it**, at the same path in both:
```
root.outcome.outcomes.0.outcomes.0.outcomes.0.outcomes.0.outcomes.1.input
amount = {"text":"1 contract","type":"quantity","quantity":1}
```
Expected `{"type":"quantity","quantity":1}` — **confirmed**, with an additional display field
`text:"1 contract"` that the ruling's shorthand did not name. Recorded here because the edit in
Batch C must leave the stored object self-consistent.

## 5. Gate verdict
| STOP condition (dispatch §3) | result |
|---|---|
| any non-GF bot attached | NOT TRIPPED — 8/8 GF on both |
| either hash mismatch | NOT TRIPPED — 2/2 byte-identical |
| quantity != 1 | NOT TRIPPED — 1 on both |

**GATE PASSES. Batch B may proceed.**

## Files
- `02a-scannerA-PRE-routine.json` — the exact `{name,inputs,root}` payload whose sha256 is the
  hash above; the file's own sha256 therefore equals the config hash.
- `02b-scannerB-PRE-routine.json` — same, for ScannerB.
