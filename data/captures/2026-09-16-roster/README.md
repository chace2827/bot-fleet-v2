# Capture bundle — 2026-09-16 roster + toggle state

Purpose: the end-of-day `/bots` roster capture for trading day **2026-09-16**.
Captured **2026-09-16 17:30:41-04:00**.

## Files

| file | sha256 | what it is |
|---|---|---|
| `01-bots-roster-recent-activity-2026-09-16-173041.txt` | `fd7eafdc59a1b451d349bc12bcaabf538fca08473c707156d1d60206b37e25d2` | RAW bookmarklet capture, unmodified. 43 list rows + the 43-row `i.sticon[title]` AUTOS/EXITS block (S0b-3 fix v2.1). |
| `02-roster-toggles-43-2026-09-16.tsv` | `028c16a39c07d06fef94022b0e77b8d85e833208f799ab2cc66fdb89ad5d81f2` | DERIVED join into `bot_name / bot_id / AUTOS / EXITS`. |

## Closing state

- footer, verbatim: `43 active bots • 7 left in your plan • Upgrade`
- rows parsed: 43
- **AUTOMATIONS ON: 18 of 43**
- **EXIT OPTIONS ON: 16 of 43**
- **DRIFT vs previous bundle:** ZERO. Not one bot changed either toggle.

Cross-checked against: `/Users/andrewchace/bot-fleet-v2/data/captures/2026-09-07-roster`
