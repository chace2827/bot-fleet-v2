# Capture bundle — 2026-09-07 roster + toggle state

Purpose: the end-of-day `/bots` roster capture for trading day **2026-09-07**.
Captured **2026-09-07 12:47:39-04:00**.

## Files

| file | sha256 | what it is |
|---|---|---|
| `01-bots-roster-bots-2026-09-07-124739.txt` | `7cab7905c94f9f15eab1e0d1e6cffba391f5f73e4f25c8cc58fe97e319e68785` | RAW bookmarklet capture, unmodified. 44 list rows + the 44-row `i.sticon[title]` AUTOS/EXITS block (S0b-3 fix v2.1). |
| `02-roster-toggles-44-2026-09-07.tsv` | `d6a13d4b45f2670d80eb8c68194a879d904d40c44473de4cf1c4c122b04445a8` | DERIVED join into `bot_name / bot_id / AUTOS / EXITS`. |

## Closing state

- footer, verbatim: `44 active bots • 6 left in your plan • Upgrade`
- rows parsed: 44
- **AUTOMATIONS ON: 18 of 44**
- **EXIT OPTIONS ON: 16 of 44**
- **DRIFT vs previous bundle:** ZERO. Not one bot changed either toggle.

Cross-checked against: `/sessions/rcw-019ctakyucnbtxzawgene1nd/mnt/bot-fleet-v2/data/captures/2026-09-02-gf-sizing`
