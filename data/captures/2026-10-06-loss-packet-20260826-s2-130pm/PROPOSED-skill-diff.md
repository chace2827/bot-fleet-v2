# PROPOSED additions to `.agents/skills/oa-drive/SKILL.md`
(not applied — for Andy/Cowork review. Evidence: 2026-10-06 loss-packet run,
`data/captures/2026-10-06-loss-packet-20260826-s2-130pm/`)

Insert a new section "§7 — Read-path surface map (verified 2026-10-06)":

```
## 7. Read-path surface map (verified 2026-10-06)

### Positions
- `/positions/closed` rows: `grid#bots-postabs-closed-grid > bd.dim-scroller >
  row.pos` · date groups = `div.rowhd` (sorted by CLOSE date desc) ·
  ~30 rows per Load-more · a date group is complete only when the NEXT `rowhd`
  renders (~390 rows ≈ 6 weeks at current fleet volume).
- Bot name: `row.pos i.fa-robot[title]` · position id: `row[data-key]` ·
  open: click a neutral cell (`.closeDate`), never the robot icon (it's a
  `/bots/bot/<id>` link).
- Drawer: `overlay.drawer > view.pos-view` (STALE-VIEW TRAP, see below) ·
  close-all: `a.btn.gray.close[data-click=close]` · leg sides:
  `.strike.long|short` + `[title]` · UTC ts on trades: `em.from[data-value]` ·
  trades: `ct.trades item` · per-trade log link: `a.tlink[data-click=showAutoLog]`.
- Automation-log overlay: `overlay.drawer.logentry > view.logentry-view` ·
  its own closer: `a.btn.gray.tool.close` · positions-loop pager `bar.rebar`
  (`span.cursor`/`span.count`, `[data-click=prevRepeatItem|nextRepeatItem]`,
  `.disabled`) — iterate EVERY page before recording.

### Bot log
- `/bots/bot/<id>/log?date=YYYY-MM-DD` reaches dates BEYOND the Date filter's
  3-week preset list — the view honors the param (UI read path).
- Rows: `grid.botlog > bd.dim-scroller > row.logitem` (~50/load) · year-bearing
  `title` is on a CHILD element, not the row; the row's first cell is the time.
- Filters: `div.input-ct.filterbtn-ct` wrap hidden inputs `date|time|autotypes`;
  labels render via CSS (innerText empty) · `input.value=` + events does NOT
  apply — onDate is component-bound.
- Open a run: click the row's INFO cell (rightmost non-link cell). NEVER click
  `a.autolink` (automation editor). Run detail = same `view.logentry-view`
  + `bar.rebar` pager as the position-side log.

### Backtests (read-only scope)
- List `/backtests` · test page **`/backtests/test/<id>`** (NOT `/backtests/<id>`
  — that lands on the list) · compare `/backtests/compare/<id1,id2,...>`.
- Test name: `item.tdesc` (inside `view.bots-ztresults`) · Settings card = last
  section of the page; `innerText` carries it fully — no scrolling needed
  (`window.scrollBy` is a no-op; the view scrolls internally).
- Positions list: click `a[data-click="showPositions"]` (the COUNT link) →
  `grid[id$="-posgrid"]`, 100 rows/load, newest first · row fields:
  `.strike.long|short`, `.closeTime`, `.status .lbl`, `.risk .val`, `.pnl .val`.

### Trap update — stale drawer can fire AFTER a close
The drawer-occlusion trap also fires when the previous drawer was closed ~1–2 s
before the next row open: `view.pos-view` persists and re-renders the PREVIOUS
position, well-formed. Mandatory after every row open: pick the VISIBLE
`view.pos-view` (offsetParent-gated) and confirm strategy text + a strike from
the ROW appears in it before recording.

### Timing (observed)
SPA page hydrate after `location.href=` ~5–6 s · drawer open ~2 s ·
logentry ~2 s · Load-more re-render ~2 s · `Runtime.evaluate` default budget
45 s — chunk load-more loops (≤12 clicks/eval).
```

And a one-line addendum to §2 step 3 (verification list):

```
- Stale-view check is part of every drawer read: re-verify the visible
  `view.pos-view` content against the row you clicked (see §7 trap update).
```
