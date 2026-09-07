# §B — Roster / config drift audit, 2026-09-07

ET date from OA page header: **2026-09-07** (Labor Day; markets closed — this is a
config-drift read, not a trading day).
Session: Cowork + Claude in Chrome, read-only. ACCOUNT = **Paper Trading** on every page
(`a5.bots.allbots` account field is "Paper Trading" for all 44 bots; header reads
Paper Trading on every bot page opened). `TR ****4219` never selected.

## Verdict: **NO CONFIG DRIFT.** No finding.

## Method — why this is a signature diff and not a text diff

The harness truncates any single tool result at roughly 1 KB, so the 10,291-byte `/bots`
capture text and the 5,211-byte `allbots` TSV cannot be moved out of the page intact
without ~15 chunked round-trips, and a chunk boundary that silently drops bytes would
produce a *false* clean diff. Instead both instruments were reduced **in the page** to a
per-row 32-bit rolling signature (`x = (x*31 + charCodeAt(i)) >>> 0`, hex), and the same
function was applied on the device to the 2026-09-02 POST capture files. Equal signature
row-by-row, in the same order, is a stronger claim than an eyeballed diff: it is byte
equality of every drift-bearing field, per bot.

## Instrument 1 — `a5.bots.allbots` (allocations, groups, tags, limits, account)

Columns, in the order of `06b-allbots-FINAL-2026-09-02-222800.tsv`:
`bot_name, bot_id, group, seed, status, disableExits, posLimit, account, tags`

- rows: **44** both sides
- serialized length: **5,211 bytes** both sides
- **44 / 44 row signatures identical.** Zero differing rows.

2026-09-07 signatures (sorted by bot_name, same order as the 09-02 file):

```
5db4b685,41b7d504,4c1d49d8,55c1b410,ef1c9204,07f3c6a4,745338fb,4a02e937,e946b203,bc6565fe,
e5de71db,03cad095,d23204ee,55de8544,7952ad0e,f8fb9012,c804c05c,093d14d7,408e84f2,9c0a861b,
4919a8a2,1158a9c2,e293b772,5a155e09,c6da3b46,0b9a4ee7,9e716f2d,27da0753,246e273e,83888570,
96c1ddac,689cf722,bd2a10c7,70d1cf2c,82a97c38,0b86d3ec,89084593,a1edf45f,9029a20b,b0e42c23,
b202f18b,c34da653,adbec97d,6bc12565
```

Identical, element for element, to the same function applied to
`data/captures/2026-09-02-gf-sizing/06b-allbots-FINAL-2026-09-02-222800.tsv`.

## Instrument 2 — AUTOS / EXITS toggles (`i.sticon` title attribute, ancestor-climb v2.1)

The toggle state is NOT in `allbots` — `b.autos` is not the toggle (it counts automations;
reading it as a boolean yields 0/44, which is why the `i.sticon[title]` attribute is the
documented source, `oa-driving` skill and `oa-ops-runbook.md` §1.2). Rows are
`bot_id \t autos_title \t exits_title`; "on" is the suffix ` are on`.

- rows: **44** both sides
- **AUTOS ON 18/44** — matches 09-02
- **EXITS ON 16/44** — matches 09-02
- **44 / 44 row signatures identical**, in the same DOM order, bot ids included:

```
aec8c4c0,053ca446,b4b1c30c,3e5e7433,e89a6b21,41d04446,8cbd266e,bb1c69b2,b9e84af6,aaa3814c,
c2672955,8540c38f,7520de07,148f4d5b,9970566a,db770c28,e816d973,6e2c3015,637fee82,48eaa0af,
6bd68c4a,d0cf348e,f67dcd5f,71509a79,e43d47da,d7ef1cad,b3c7e262,0cd792a2,8e4cfc38,43e4d645,
49d5cc4a,2a97fcf4,8e12eecf,5eabfc15,5a4b77cc,ab11b4b9,716f7e0f,771c4f85,e3dd7e0a,b5cd802e,
0efe7ef2,b3b9a8f4,d46a899f,2e64a69f
```

Identical to the AUTOS/EXITS block appended to
`data/captures/2026-09-02-gf-sizing/07-roster-POST-2026-09-02-222827.txt`.

Because the count alone (18/16) could be preserved by two bots swapping states, the
**per-row** equality above is what closes the question, not the totals.

## What is NOT covered by this file

The full `/bots` innerText capture (P/L, return %, risk, market marks, footer) was NOT
written to disk this session — see the transfer limit above. Those cells are the ones the
dispatch expects to move, and they are not drift-bearing. Every field the dispatch names as
a FINDING trigger — allocation, group, AUTOS, EXITS, position limits, tags, account — is
covered above and is unchanged.

Live roster header for the record, read 2026-09-07 12:33 ET:
TOTAL P/L -$83,731 · RETURN -3.8% · CLOSED P/L -$83,750 · CLOSED -3.8% · CHANGE -$294 ·
RISK $9,682 · ALLOCATION $2,190,000 · BETA WEIGHT 49.39 · BETA EXPOSURE 0 · 44 bots.
