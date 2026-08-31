# Four authorized OA edits — 2026-08-31 evening session
Authorized by Andy in-chat, 2026-08-31. Verified-edit protocol throughout: state read before,
change applied, **HARD RELOAD**, state re-read from the server-hydrated model and the
`i.sticon` title attributes, and every automation re-hashed. Version numbers were never used as
evidence. Account on every bot touched: **Paper Trading** (checked on each bot's own page before
acting; the OA login also carries a live brokerage account, which was never selected).

Fleet-wide control: `01-…-173107.txt` (pre) vs `13-bots-roster-POSTEDIT-…-181115.txt` (post),
same instrument, same parse. **Exactly three bots differ and nothing else on the fleet moved.**
Footer both captures: `44 active bots • 6 left in your plan • Upgrade`.
AUTOS ON 19/44 -> **18/44**; EXITS ON 16/44 -> **16/44** (unchanged).

---
## Edit 1 · GF-QQQ-IC-Ride-Delta — archived
`BOTfw5TkkCRF1317864858068078811`. Evidence: `12-ride-delta-postedit-2026-08-31.txt`
(`bfcbb5f156465985…`).

Toggle state, `i.sticon` title attributes, after hard reload:
| automation | before | after |
|---|---|---|
| GF-ScannerA-PutSpread (shared) | Automation is on | Automation is on but bot automations master switch is off |
| GF-ScannerB-CallSpread (shared) | Automation is on | Automation is on but bot automations master switch is off |
| **Ride-Delta-Scan-Put** (bot-local) | Automation is on | **Automation is off** |
| **Ride-Delta-Scan-Call** (bot-local) | Automation is on | **Automation is off** |
| GF-Backstop-1552-FlatClose | Automation is on | Automation is on but bot automations master switch is off |

Bot-level: AUTOMATIONS **ON -> OFF** (`a5.bots.bot.scanning === false`; Scan Speeds panel shows
the `OFF` badge; the three still-enabled automations report the master switch off in their own
title text — three independent surfaces agreeing).
EXIT OPTIONS left **ON** (`disableExits === 0`) — Andy's instruction named automations only, and
the bot holds no open positions, so exits are inert. Flagged for his call.
Neither bot-local scanner was deleted; both remain listed and re-openable.

Config hashes, sha256 over `{name,inputs,root}`, each read after a fresh open with a hard reload
between opens — **5 of 5 byte-identical before and after**, so the toggling changed enabled state
only and touched no configuration:
```
GF-ScannerA-PutSpread       1e5eb9936a1adf067af65a4841d42e755592f7c179f3c0cad477502dfdbfcdc8  (5379B)
GF-ScannerB-CallSpread      a925d490b8a0d2337566f47307fc52470da129935d3bd83d24389c6dc433dfb5  (5044B)
Ride-Delta-Scan-Put         a8643224fa99a7f79286aa81ce487cd64cace272442c2c55f9ccb7d5d9f3db86  (5133B)
Ride-Delta-Scan-Call        4f7251025257d95d1ee49de48b115a5b6a50cb98bd77434e937a60d141cee967  (5271B)
GF-Backstop-1552-FlatClose  116069bddf8b8c9e58bd8f28313c2ad95726fa3f7205df4dfde82de7a3e2e5b5  (1441B)
```
The two shared hashes still match the `ScannerA v12` / `ScannerB v4` values stamped in
GF-QQQ-IC-Ride's Notes under `R-2026-08-17-GF-ENTRY-METHOD` — the shared library was not touched,
so no other GF arm was affected.

⚠️ ONE INCIDENT, DISCLOSED: the JS call that fired the bot-level AUTOMATIONS toggle returned
`Inspected target navigated or closed` instead of a result — the documented ~45s / navigation
class of failure where the work may already be committed. Per the runbook the action was **NOT
re-fired**; state was re-read after a hard reload instead, and it showed the toggle off exactly
once. The fleet-wide pre/post diff independently confirms a single change on this bot.

## Edit 2 · QQQ long call — three legacy positions CLOSED
`BOTfw5TkkCRF1017766424258604555`, ACCOUNT **Paper Trading**, AUTOMATIONS OFF, EXIT OPTIONS OFF.
Evidence: `11-qqqlongcall-postclose-2026-08-31.txt` (`95b273f473975c10…`).
Each close was placed manually from the position's own Close Position form (Quantity 1 contract,
SmartPricing Normal, no memo), one at a time, with a hard reload and a re-read between each.

**All three FILLED IMMEDIATELY — nothing is left working or queued.** The paper account fills
outside regular hours, so Andy's "fills may land next session" caveat did not apply.

| opened | legs | exp | close price | realised P/L | DIT | state |
|---|---|---|--:|--:|--:|---|
| Jun 15 2026 9:45AM | 865/745 C | Sep 18 | 1.41 | **-$3,158** | 77d | Closed Aug 31 |
| Jun 22 2026 2:15PM | 870/745 C | Sep 30 | 3.24 | **-$3,164** | 70d | Closed Aug 31 |
| Jun 29 2026 12:30PM | 839/727 C | Sep 30 | 9.07 | **-$2,371** | 63d | Closed Aug 31 |

Realised total **-$8,693** on $10,065 of capital at risk. Open Positions for this bot now reads
`No open positions`; bot open risk went `$10.1K` -> `--` in the fleet capture.
All three opened before LEDGER_START (2026-08-10), so none is ledger-eligible; the realised loss
is a pre-cutover legacy figure and must not be folded into post-cutover cumulative P/L.
Allocation left at **$30K** as instructed.

## Edit 3 · 3DTE $140-$350 — allocation $5,000 -> $10,000
`BOTfw5TkkCRF2217765235512870291`. Safeguards drawer, `input[name="seed"]` 5000 -> 10000, Save.
After hard reload: `a5.bots.bot.seed === 10000` and the Safeguards panel reads **$10,000**.
Unchanged and re-read: DAILY POSITIONS 1 per day, POSITION LIMIT 1 at a time, DAY TRADING
Allowed, BOT GROUP OA-Mirror-Focus, AUTOMATIONS ON, EXIT OPTIONS ON.
⚠️ CONSEQUENCE ANDY SHOULD KNOW: this bot's Bot Input **POSITION SIZE is "26% of net liquid"**,
not a fixed dollar figure. Doubling the allocation doubles the dollar size of every future
position it opens. Equalizing the *allocation* did not hold *risk per trade* constant here.
Its one open position (opened 08-27, risk $965) is unaffected.

## Edit 4 · QQQ-IC-0DTE-Fortress — added to the Monitor group
`BOTfw5TkkCRF2717857919585029021`. BOT GROUP **None -> Monitor**.
After hard reload: `a5.bots.bot.group.name === "Monitor"` and the header reads Monitor.
Toggles untouched and re-read: **AUTOMATIONS OFF, EXIT OPTIONS OFF**. ACCOUNT Paper Trading.
Group membership now totals 44 of 44 — no ungrouped bot remains.
⚠️ DISCLOSED: while locating the group control, one click landed on the adjacent ACCOUNT
dropdown and opened it (it lists `Paper Trading` and a live brokerage account `TR ****4219`).
Nothing was selected; it was dismissed with Escape and ACCOUNT re-read as `Paper Trading` both
immediately and after the hard reload. No account was changed on any bot in this session.
