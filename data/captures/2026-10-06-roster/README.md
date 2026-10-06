# Capture bundle — 2026-10-06 roster + toggle state

Purpose: the end-of-day `/bots` roster capture for trading day **2026-10-06**.
Captured **2026-10-06 16:36:53-04:00**.

## Files

| file | sha256 | what it is |
|---|---|---|
| `01-bots-roster-bots-2026-10-06-163653.txt` | `b9701aacf677c18153cad0ea8013356f787ac8b205bff9963db80eecefc92128` | RAW bookmarklet capture, unmodified. 43 list rows + the 43-row `i.sticon[title]` AUTOS/EXITS block (S0b-3 fix v2.1). |
| `02-roster-toggles-43-2026-10-06.tsv` | `4c0262407dc8ec71c0faa68e2cb0ad1fc81aec3fdfeed20b8a8ff37d5eee9aa6` | DERIVED join into `bot_name / bot_id / AUTOS / EXITS`. |

## Closing state

- footer, verbatim: `43 active bots • 7 left in your plan • Upgrade`
- rows parsed: 43
- **AUTOMATIONS ON: 18 of 43**
- **EXIT OPTIONS ON: 16 of 43**
- **DRIFT vs previous bundle:** ZERO. Not one bot changed either toggle.

Cross-checked against: `/Users/andrewchace/bot-fleet-v2/data/captures/2026-09-16-roster`
