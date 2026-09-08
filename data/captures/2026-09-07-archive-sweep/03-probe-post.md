# Steps 4–5 — the probe archive, and what OA-archiving actually does

**Bot:** `QQQ-IC-0DTE-Baseline` (`BOTfw5TkkCRF3317727290514286611`)
**Archived:** 2026-09-07 ~14:50 ET. **Session PAUSED by Andy at ~14:56 ET, mid-step-6.**

## Step 4 — the dialog, verbatim

> **Archive bot? You can restore it later in Settings -> Bot Archive**
> `Cancel`  `Yes`

**It does not mention deleting data, positions, or history — it promises the opposite.** The
step-4 CANCEL-AND-STOP condition did not fire, so the confirm was given.

**How the menu and the item were driven — and a runbook correction.** `oa-ops-runbook.md` §5 /
the `oa-driving` skill both say **"`archiveBot` / `showBotMenu` resist everything — they are the
human's hand"** (finding S0b-2). **That is now falsified.** Both yielded on the first attempt to
the documented full pointer sequence
`pointerover → pointerenter → pointerdown → mousedown → pointerup → mouseup → click`
dispatched on the element at its `getBoundingClientRect()` centre:
- the `...` header button is `a.btn.gray.ionly[data-click="showBotMenu"][aria-label="More options"]`
- the menu item is `ITEM.mi.nodesc.has-icon[data-click="archiveBot"]`

**No coordinate was used anywhere near the menu.** The item was selected by its `data-click`
attribute and then guarded before dispatch: the script refused unless the element's own text was
exactly `"Archive"` and its class did **not** contain `danger`. Recorded at dispatch time:
`archiveBot` class `mi nodesc has-icon` at y=342; `deleteBot` class `mi danger nodesc has-icon`
at y=397 — **55px apart, and Delete carries a class the guard rejects.** This is the mechanism the
runbook's "no coordinate fallback on menus" warning was protecting against, closed by attribute.

## Step 5 — POST-ARCHIVE observations, after a hard reload

| Question the dispatch asks | Answer | Evidence |
|---|---|---|
| Still in `/bots`? | **No** | `QQQ-IC-0DTE-Baseline` absent from page innerText |
| Still in `a5.bots.allbots`? | **No** | `allbots` length **44 → 43**; the probe object is gone |
| Footer count 44 → 43? | **Yes** | `44 active bots • 6 left in your plan` → `43 active bots • 7 left in your plan` |
| Is there an archived-bots view? | **YES — `/settings/archive`**, labelled **"Bot Archive"**, reachable from Settings' left nav | navigated and read |
| Can it be un-archived? | **Yes — a `Restore` button per row.** Read only; **NOT clicked.** | `/settings/archive` |

### Three things the dispatch did not ask, that matter more

**1. A plan slot is FREED.** `6 left in your plan` → `7 left`. OA-archiving returns the bot's slot.
Archiving the remaining 16 sweep candidates would return the roster to 27 active bots and free
23 slots. That is a real, previously unrecorded consequence.

**2. The account roll-up EXCLUDES archived bots — immediately.** `/bots` header:
| | PRE | POST |
|---|---|---|
| TOTAL P/L | -$83,731 | **-$52,151** |
| CLOSED P/L | -$83,750 | **-$52,170** |
| ALLOCATION | $2,190,000 | **$2,090,000** |

The probe's -$31,580 and its $100,000 allocation left the account header the moment it was
archived. **Any figure ever read off the `/bots` header is scoped to non-archived bots**, so the
sweep will move these numbers a long way. It does not touch `data/trades.csv`, which is built from
the export and contains none of these bots.

**3. ⛔ THE BOT'S OWN URL 404s AFTER ARCHIVING.**
`/bots/bot/BOTfw5TkkCRF3317727290514286611` now redirects to
`/bots/error?error=Bot%20not%20found&icon=fal-robot` — page body reads **"Error / Bot not found"**.
**Operational consequence for Evening 2: every per-bot pre-state must be captured BEFORE that bot
is archived. There is no going back for a forgotten field** short of `Restore`.

## 🔎 UNRECORDED BOT FOUND IN THE BOT ARCHIVE

`/settings/archive` lists **two** bots, not one:

| # | Name | Note |
|---|---|---|
| 1 | `QQQ-IC-0DTE-Baseline` | this session's probe |
| 2 | **`QQQ-IC-0DTE-Fortress-ARCHIVED-2026-08-03`** | **already OA-archived — by whom and when is not in the folder** |

`data/archive/rename_map.csv` row 1 records that `QQQ-IC-0DTE-Fortress` was renamed to
`-ARCHIVED-2026-08-03` and cloned on 2026-08-03, with disposition `clone-to-spec`. It does **not**
record that the original was ever OA-archived — and the three surviving `-ARCHIVED-` clones are all
still on the active roster, which is why the sweep treats them as "renamed, not OA-archived".
**So one bot was OA-archived at some point and the folder never learned.** It is not in the 44-row
roster, not in `bots_meta.csv`'s 44 rows, and not in any capture. Flagged, not touched.

## Step 6 — INCOMPLETE (session paused here)

The full-history export was requested and **confirmed**, but the file had not landed in
`~/Downloads` when Andy paused the session, so **M-08 is NOT ANSWERED and no verdict was written.**

Route found (not previously documented in the folder): **`/positions/analyze` → `Export Data`**.
`/bots` has no account-level export; the per-bot `...` menu's `Export Data` is per-bot only.
Filter state at request time, read verbatim before confirming — **Live/Paper/Account/Symbols/Tags/
Strategy/DTE/Bot/Bot Group/Day/Hour all UNSET (no filter)**, `Range: Since 09/08/2025` (URL
`?range=2025-09-08,*`), which spans the whole history (earliest data 2026-03-05).
Confirmation dialog, verbatim:

> **Are you sure you want to export all closed position data? (up to 10,000 positions)**
> `Cancel`  `Yes`

Page-level `Metrics` at that moment: **POSITIONS 1,637 · WINS 1,145 · LOSSES 443**.

**What still has to happen to answer M-08:** get that CSV, and check it against
`02b-probe-rowset-QQQ-IC-0DTE-Baseline.tsv` — **43 rows, 43 distinct closeDates, 33 `closed` +
10 `expired`, rowset sha256 `c32b2c8cf5cf66a95e27d8b28f0ce485e1927b277b405012005cdf1e39261c97`.**
Match exactly → "rows survive". Missing or altered → they do not.
