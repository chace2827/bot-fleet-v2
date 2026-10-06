# 07 — Debrief: how the packet actually went

## 1. Where the time went

| § | ~time | browser actions* | notes |
|---|---|---|---|
| §1 ledger | ~2 min | 0 | local grep only |
| §2 OA positions | ~20 min | ~40 | 12 Load-more clicks to reach the complete AUG-26 group; 4 drawer opens; 4 automation-log opens; 1 pager advance; ~15 structure/verify probes; one stale-drawer recovery |
| §3 bot log | ~15 min | ~30 | date-filter dead end (~5 min) before `?date=`; 4 Load-more clicks (250 rows); 4 run opens; 2 pager advances; ~10 probes |
| §4 tape | ~5 min | 0 | scratch copy + 1min fail + 5min pull + derive |
| §5 backtests | ~18 min | ~35 | URL-pattern detour (~4 min); showPositions discovery (~4 min); 11 page loads × ~6 s hydrate; 11 extract calls |
| §6 + files | ~10 min | 0 | write, hash, README |

\* one "action" ≈ one CDP eval or one dispatched click.

**Slowest: §2** — deepest pagination (~390 rows before the AUG-25 boundary proved the
AUG-26 group complete) plus the stale-drawer detour plus two separate overlay
stacks to open per leg. §3's date-filter dead end was the single most expensive
wrong turn inside one section.

## 2. Every retry, dead end, wrong turn

| # | tried | happened | finally worked |
|---|---|---|---|
| 1 | `location.href=` + reads inside one eval | eval returned `undefined` — navigation invalidated the context mid-call | separate nav snippet, Node-side `sleep`, then read |
| 2 | PAPER check via `innerText.includes('PAPER')` on `/positions/closed` | `false` — that page shows Live/Paper filter tabs, not the badge | badge check on `/home` at session start; `ACCOUNT Paper Trading` on the bot header |
| 3 | expected `group`/`item` rows in positions grid | 0 groups — rows are `row.pos` under `grid … > bd.dim-scroller`, date headers are `div.rowhd` | queried `row.pos`, grouped by `div.rowhd` |
| 4 | stopped at first AUG-26 header | group was partial (3 rows, none target) — Load-more boundary cut it | kept loading until the *next* header (AUG 25) appeared = complete group |
| 5 | first Automation Log open → scanned `overlay`s | reported empty; the log had actually opened in `overlay.drawer.logentry > view.logentry-view` | select `view.logentry-view` directly |
| 6 | pos-view `a.btn.gray.close` while logentry on top | closed the WHOLE stack (both overlays) | acceptable — reopen is cheap; logentry also has its own `a.btn.gray.tool.close` |
| 7 | **stale drawer (the documented trap)** — closed stack, opened call row | `view.pos-view` rendered the PUT position's details, well-formed | verify step caught it (`Short Call/7,69x` expected, got put): closed, longer waits, reopened, re-verified strikes before recording |
| 8 | `grid.botlog bd` for log rows | picked a different `bd` (held an INPUT) | `grid.botlog bd.dim-scroller` |
| 9 | log rows as `item` | wrong tag — they're `row.logitem` | — |
| 10 | row `title` attr for year-bearing timestamp | empty — title lives on a *child* element | took the time from the row's first cell text |
| 11 | date filter: set `input[name=date].value` + change/input events | nothing — `onDate` is component-bound, not `window`-visible | **`?date=2026-08-26` URL param**, which the log view honors |
| 12 | `/backtests/<id>` | lands on the tests list page, not the test | `/backtests/test/<id>` (pattern from the t1-s2-tail README's compare URL) |
| 13 | positions table on test page as `row`/`grid` scan | only the hidden list-view grid exists; the positions list is behind `a[data-click="showPositions"]` (the COUNT link) | click it → `grid[id$="-posgrid"]`, 100 rows/load |
| 14 | `window.scrollBy` to reach the Settings card | `scrollY` stayed 0 — the view scrolls internally (`view.bots-ztresults`) | unnecessary anyway: `innerText` carries the card; extract from text |
| 15 | `.cell.info` for the log's INFO column | grabbed the automation cell instead | used whole row text (time\|automation\|info) — lossless |
| 16 | clicks that did nothing | the first `.loadmore` dispatch on `/positions/closed` needed the element visible check; elementFromPoint misses when occluded (drawer overlay over `a.saveclose`-class targets) | `offsetParent !== null` gate + `scrollIntoView` + re-read state after every action |

## 3. 06-facts.md — READ vs DERIVED

**READ** (copied from a page/file): both sides' structure, tags; all four
strikes + long/short classes; credits $0.20/$0.40 ($200/$400); open times and
automation names (Scalp-Scan-Put/Call, 1:31PM); close times 3:05PM and the trade
timestamps; "Close 10 contracts" labels; closing automations
(Scalp-Mon-S2-StrikeTouch / -Cleanup); fills $0.05 and $2.05 incl. the verbatim
"2.05 → 2.10" ladder; P/L +$150 / −$1,650; risks $4,800/$4,600; OA PRICE AT CLOSE
7,690.36 / 7,690.64; every tape (t,p,h,l) row incl. 16:00 = 7,675.70; all log
decision texts; all 11 backtest rows, names, Exit Options lines; leg classes.

**DERIVED** (computed/inferred): ET conversion of the UTC trade timestamps
(15:05:01.686 / 15:05:04.195); the within-$20/$10/at-or-through first-bar times
and the +0.73 / 9.15-short extremes (computed over the 5-min tape); "underlying
at close (tape)" — my choice of the 15:05 bar as the containing bar; both
"expired OTM" verdicts (16:00 close vs strikes); net −$1,500; the cleanup
ordering claim (call closed first → loop had 1 item); STRIKES MATCH; "no further
log rows" (first row = 3:05PM — an absence claim, flagged as inference).

**Least sure:**
- *underlying at close (tape)* — the 15:05 bar's close `p` is a ~15:05:59 mark;
  OA's mark is 15:05:01 inside the same bar. Same bar ≠ same print. Mitigated by
  reporting OA's PRICE AT CLOSE as primary and the bar's h/l/p alongside.
- *the 0.73 max breach* — 5-min granularity; the real wick may have exceeded it
  between bars. 1-min tape was unavailable.
- *ladder text "2.05 → 2.10"* — copied verbatim; its semantics (SmartPricing
  final-price path) are not asserted anywhere in the packet.
- *"no log rows after 15:05"* — true of the loaded day-filtered list; it's the
  expected flat-bot silence, but it is an inference from absence.

## 4. Did the drawer trap fire?

**Yes, once** — and it fired in a subtler form than documented. The documented
form is "drawer open → next row click returns previous details." Here the drawer
had been *closed* ~1.5 s prior and the row click still re-rendered the stale
put-position view (well-formed, wrong position — `view.pos-view` persists).

**Confirm procedure** (now in the packet): after every row open, read the
*visible* `view.pos-view` (offsetParent-gated), and check the strategy text +
leg strikes match the row's own values before recording anything. The put
misread failed that check immediately ("Short Put / 7,65x" where a call
7,690/7,695 was expected) and was discarded, not written.

## 5. Disagreements — OA vs trades.csv, vs backtests

- Ledger `open_date` put leg `13:31:03` vs trade ts `17:31:02.845Z` → 13:31:02.8 —
  ~0.2 s rounding drift. Call side `13:31:04` vs ts `…:04.367Z` — consistent.
- Ledger `underlying_close` = OA "PRICE AT CLOSE" (7,690.36/.64) — consistent,
  but the field is **position-close print, not 16:00** (tape 7,675.70). Naming
  hazard, not a data error.
- Ledger `premium` = −200/−400 vs OA "CREDIT TO OPEN" $200/$400 — sign-convention
  difference (premium stored negative in the ledger).
- Backtest `1:30pm` entry vs live `1:31PM` fills — the backtest stamps entry at
  the 13:30 bar; OA fills logged 13:31:02/04.
- Backtest row `risk $445` (1-lot IC) vs live $4,600–4,800/side (two 10-lot
  spreads) — expected structure difference, not a conflict; flagged so nobody
  compares raw P/L.
- Everything else agreed: strikes (all 11 arms), credits, exit prices, P/L,
  risks, close dates, statuses.

## 6. PROPOSED-packet-runner.js
See `PROPOSED-packet-runner.js` in this bundle — one Node/CDP pass producing the
§2 positions+logs, §3 run list + close-minute decision texts, and §5 rows as
JSON, given `--bot --date --tests`.

## 7. PROPOSED-tape.py
See `PROPOSED-tape.py` — one command: symbol, date, strike list → bars CSV +
per-strike distance/extreme table + interval used.

## 8. What the dispatch should have said up front

1. `/backtests/test/<id>` is the test-page URL (not `/backtests/<id>`);
   compare pages take comma-joined ids.
2. The positions list on a test page is behind `a[data-click="showPositions"]`
   (the COUNT link); grid id ends `-posgrid`, 100 rows/load; test name is
   `item.tdesc`; the Settings card is the page's last section and `innerText`
   needs no scrolling.
3. Bot log accepts `?date=YYYY-MM-DD` — reaches past the 3-week preset filter.
4. `/positions/closed` groups by **close date**; ~30 rows per Load-more; a date
   group is only provably complete once the NEXT `div.rowhd` appears (≈390 rows
   for 6 weeks back at current fleet volume).
5. The stale-drawer trap can fire *after a close*, not only drawer-open; always
   verify the visible `view.pos-view` strikes before recording.
6. Log rows: `grid.botlog bd.dim-scroller row.logitem`, ~50/load; year-bearing
   `title` is on a child, not the row.
7. Automation-log overlay = `overlay.drawer.logentry > view.logentry-view`;
   iterates via `bar.rebar` (`.cursor`/`.count`, `nextRepeatItem`); its own
   closer is `a.btn.gray.tool.close`; the position drawer's closer
   (`a.btn.gray.close`) closes the whole stack.
8. Trades rows: `view.pos-view ct.trades item`, log links
   `a.tlink[data-click="showAutoLog"]`, UTC ts in `em.from[data-value]`.
9. 1-min Tradier retention is ~20 trading days — budget a 5-min fallback for
   targets older than that and record which interval ran.
10. Ledger `underlying_close`/`underlying_open` are *position-event* prints, not
    end-of-day — put the caveat in the dispatch so the facts table can't invert it.

## 9. PROPOSED-skill-diff.md
See `PROPOSED-skill-diff.md` — additions to `.agents/skills/oa-drive/SKILL.md`
covering selectors, page paths, pager behavior and timings. Skill itself not edited.

## 10. Knowledge note
**Attempted, blocked: devin MCP returned HTTP 401** — "API key has expired or
been revoked" on `devin_knowledge_manage` create. The full note (exact title
**"bot-fleet-v2 loss-packet procedure"**, trigger, content) is saved verbatim in
`PROPOSED-knowledge-note.md` in this bundle — paste it or retry once Andy
refreshes the devin API key.

## 11. Next-run estimate + remaining 6

With the runner: ~**15–20 min per packet**, mostly unattended — the long poles
are mechanical (positions Load-more ~1–2 min, bot-log paging ~1 min, 11 test
hydrates ~1.5 min). Manual verification stays: drawer-strike check, pager
exhaustion, tape interval note.

**Six packets in one session: yes**, if they're same-shaped (S2 family, similar
depth). Budget ~2 h of agent time plus anomaly handling — a flat-day log (no
rows), a position held past close-date, or a stale-drawer will each add a few
minutes. The first reused run also validates the runner on live selectors before
trusting it at volume.
