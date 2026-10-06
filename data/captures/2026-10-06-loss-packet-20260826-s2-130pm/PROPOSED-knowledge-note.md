# PROPOSED Devin Knowledge note — paste/retry once the devin MCP key is refreshed
# (create returned HTTP 401 "API key has expired or been revoked" on 2026-10-06T22:1x ET)

## Title (exact)
bot-fleet-v2 loss-packet procedure

## Trigger
When building a read-only loss-packet / evidence bundle for a bot+date from the
Option Alpha web app via Chrome CDP (positions, trades, automation logs, bot log,
backtest rows, Tradier tape)

## Content
Procedure for an OA loss-packet (proven 2026-10-06; bundle
`data/captures/2026-10-06-loss-packet-20260826-s2-130pm/`, incl.
PROPOSED-packet-runner.js + PROPOSED-tape.py + PROPOSED-skill-diff.md).

CONNECT: Andy launches Chrome `--remote-debugging-port=9222
--user-data-dir=$HOME/.chrome-oa-profile` and logs in. Verify: no /login in URL,
PAPER badge on /home, `ACCOUNT Paper Trading` on the bot header. Drive via raw
CDP Runtime.evaluate (returnByValue+awaitPromise); clicks must be a pointer+mouse
event sequence dispatched at elementFromPoint — element-ref .click() no-ops.
After every action re-read the page. Navigation kills the eval — nav in one call,
read in a later one.

POSITIONS (/positions/closed): rows `grid#bots-postabs-closed-grid >
bd.dim-scroller > row.pos`, date groups `div.rowhd` sorted by CLOSE date,
~30 rows/Load-more. A date group is complete only when the NEXT rowhd appears
(~390 rows ≈ 6 weeks). Bot name in `i.fa-robot[title]`, position id
`row[data-key]`; open via a neutral cell (.closeDate), never the robot icon.
Drawer = `overlay.drawer > view.pos-view`. STALE-VIEW TRAP: the drawer can
re-render the PREVIOUS position even after a close — always pick the VISIBLE
view.pos-view (offsetParent) and verify a strike from the row before recording.
Trades: `ct.trades item`, log links `a.tlink[data-click=showAutoLog]`, UTC ts in
`em.from[data-value]`. Automation log overlay: `overlay.drawer.logentry >
view.logentry-view`, its own closer `a.btn.gray.tool.close`; iterate `bar.rebar`
pager (nextRepeatItem) to exhaustion. The position drawer's `a.btn.gray.close`
closes the WHOLE stack.

BOT LOG: `/bots/bot/<id>/log?date=YYYY-MM-DD` reaches dates past the 3-week
Date-filter presets — the view honors the URL param. Rows `grid.botlog >
bd.dim-scroller > row.logitem`, ~50/load; year-bearing title on a child element;
open a run via the INFO cell, NEVER `a.autolink` (automation editor).
`input.value=` on filter inputs does NOT apply (component-bound handlers).

BACKTESTS (read-only): test page `/backtests/test/<id>` (`/backtests/<id>` =
list page; compare = `/backtests/compare/<csv ids>`). Name `item.tdesc` in
view.bots-ztresults; Settings card is the last page section, fully in innerText
(window.scrollBy is a no-op — view scrolls internally). Positions via
`a[data-click=showPositions]` (the COUNT link) → `grid[id$=-posgrid]`,
100 rows/load.

TAPE: copy scripts/+.env to a /tmp scratch root, `tape.tradier_timesales(sym,
date, token, base, interval)`. 1min retention ~20 trading days → 5min fallback
for older dates; record which interval ran. Ledger `underlying_close/open` are
POSITION-event prints, not end-of-day.

TIMING: hydrate ~6s, drawer ~2s, logentry ~2s, load-more ~2s; chunk load-more
loops ≤12 clicks per eval (45s budget).

NEVER: automation-name links, Save, toggles, Clear Log, Create Bot, backtest
run/edit, OA exports, credentials, wire protocol/RPC. Missing date after
exhausted Load-more = report, don't fill.
