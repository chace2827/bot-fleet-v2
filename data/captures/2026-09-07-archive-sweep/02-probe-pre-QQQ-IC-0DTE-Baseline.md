# Step 3 — probe bot PRE-ARCHIVE full state

**Bot:** `QQQ-IC-0DTE-Baseline` · id `BOTfw5TkkCRF3317727290514286611`
**Read:** 2026-09-07 14:46–14:48 ET, Claude-in-Chrome "Browser 1", four surfaces
(`/bots` model, bot Dashboard, `/positions`, `/settings`). Read-only; no field was written.

## Identity & placement
| Field | Value | Surface |
|---|---|---|
| ACCOUNT | **Paper Trading** | header + model `account` |
| BOT GROUP | **Archive** | header + model `group` |
| AUTOMATIONS | **OFF** | header toggle + `status=off` + sticon title "Scheduled automations are off" |
| EXIT OPTIONS | **OFF** | header toggle + `disableExits=1` + sticon title "…are off" |
| Tags | `control` (one tag) | Dashboard Tags panel + model `tags` |
| Icon | default bot icon | /bots row |

## Safeguards (Settings, verbatim)
| ALLOCATION | DAILY POSITIONS | POSITION LIMIT | DAY TRADING |
|---|---|---|---|
| **$100,000** | **3 per day** | **2 at once** | **Allowed** |

Scan Speeds — AUTOMATIONS `OFF` / Every 1m · EXIT OPTIONS `OFF` / Every 1m.
Symbols — **"No symbols yet"** (empty). Bot Inputs — **none**. Notes — **empty** ("Add Notes").
Activity Alerts — Open position ✓, Close position ✓, Automation warning ✓, Automation error ✓.

## Capital (Dashboard, verbatim)
ALLOCATION $100,000 · NET LIQUID $68,420 · **AT RISK 0** · AVAILABLE $68,420 · **MAINTENANCE 0**

## Position Stats (Dashboard, verbatim)
CLOSED POSITIONS **43** · CLOSED P/L -$31,580 · PROFIT FACTOR 0.50 · MAX DRAWDOWN $25,730
WIN RATE 73.2% · WINS 30 · LOSSES 11 · AVG P/L -$734 · AVG WIN $1,039 · AVG LOSS -$5,704 · STREAK 1 loss
Chart footer: "Since Mar 5, 2026".

## Positions list
`/positions` Open Positions table reads **"No open positions"** — a fourth surface agreeing with
`pcount = 0`, `AT RISK 0` and `MAINTENANCE 0`. **The bot is safe to archive under the dispatch's
"skip any bot with an open position" rule.**
Closed table: 43 rows, most recent **MAY 22 · QQQ Iron Condor 727C/726C/717P/716P · Closed · qty 109
· trade 0.09 → close 0.19 · -$1,090 · DIT 0d**, then MAY 21, MAY 20, MAY 19 … back to Mar 5.

## Automations — 1 automation, hashed
| # | Name | Trigger | Root card | Inputs | version | counter |
|---|---|---|---|---|---|---|
| 1 | `Entry - IC - 1:30PM` | Every day, 1:30pm EST | `Open QQQ Iron Condor` (single card) | **0** | 2 | 0 |

**CONFIG HASH — `aed7afe2dc1836c9d47e3333391895a8d9a105411148302e97d6c7df95a80ddb`**

Formula, unchanged from every baseline in `data/captures/`:
`sha256(JSON.stringify({name, inputs, root}))` over `a5.bots.acedit.routine`, computed **in-page by
`crypto.subtle`** immediately after opening the automation fresh. Payload 3,019 chars.
`root` keys: `nid|name|type|input`.

**How the editor was opened and closed (trap discipline).** Opened by dispatching the full
`pointerover→pointerenter→pointerdown→mousedown→pointerup→mouseup→click` sequence on the row's own
`a.autolink` — never `a5.bots.editAuto()`, which hydrates a phantom "New Automation" draft. The
editor that opened was titled `Entry - IC - 1:30PM` with one `Open QQQ Iron Condor` card, matching
the stored model — **not** a draft. Closed via the editor's own `Close` control. **No "Leave site?"
guard fired and `a5.bots.acedit` went back to `undefined`, so no dirty state existed: nothing was
edited and nothing was saved.** Exactly one editor was opened in this page life (trap 6).

## Why this bot
See `02a-probe-selection-2026-09-07.md`. Row-count fingerprint **43** agrees across three
independent surfaces: `a5.bots.allbots.closedCount`, the bot Dashboard's CLOSED POSITIONS tile, and
43 rows in `data/raw/2026-08-31.csv`. The exact row set is `02b-probe-rowset-QQQ-IC-0DTE-Baseline.tsv`.
