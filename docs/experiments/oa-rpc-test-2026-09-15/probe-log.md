# OA internal backtest RPC probe log — 2026-09-15

- **Session model**: SWE-2 Max (Devin CLI agent)
- **Runtime**: Node v25.8.2, Chrome via CDP :9222 (profile /tmp/oa-chrome-profile)
- **Account mode**: PAPER (badge on /home activity header; `.userbar` hidden on /backtests shell)
- **Endpoint under test**: `POST https://app.optionalpha.com/api/request`
- **Scope discipline**: `zdte.*` only. No `bots.*`/`accounts.*`/`member.*` calls from script (the UI itself batches `member.setData` with its own startTest — observed, not replayed). `startTest` API calls: 2 of max 2. All reads sequential, ≥15s apart.
- **Docs read**: `docs/oa-internal-api.md`; clean capture found at `data/captures/2026-08-19-recon/oa-network-recon-2026-08-20-00-32-14.CLEAN.json` (doc says `2026-08-20-recon/` — path drift noted).

## Documented request shape (5 lines)

1. Every call is `POST /api/request`; body is a JSON ARRAY of `{t:"rpc", tid:"<epoch-ms>-<n>", api:"<ns>.<method>", args:[...]}`.
2. Auth = logged-in session cookie; no bearer/CSRF observed in capture.
3. Backtester namespace `zdte.*`: `startTest` (args[0]=config), `testStatus` (args `[id, symbol]` → % or "done"), `testResults` (args `[{id, pos:true}]`), `testDetails` (args `[id]` → `opts` echo), `listTests`, `counts`, `getBotDefs`, `symdata`.
4. Progress is polled via `testStatus`, not streamed.
5. `text`/`textValues` fields mirror numeric settings; mismatch mislabels the run.

## Pre-flight

| time (local) | api | args summary | HTTP | result summary |
|---|---|---|---|---|
| 19:14 | (page read) | GET /backtester → redirects to /backtests | — | logged in after hydration; no /login |
| 19:15 | (page read) | backtest list | — | renders: NAVTEST-BASE (ran ~8m before session, NOT ours), SPX Long Call rows |
| 19:17 | (page read) | /home header | — | **PAPER badge present** |

Banner on /backtests: "discontinued … will no longer function after March 30th, 2026" — stale; API demonstrably ran tests today.

## Call log

| time | api | args summary | HTTP | result |
|---|---|---|---|---|
| 19:54 | zdte.startTest (UI, captured) | BASE config: QQQ shortputspread 0DTE, −.20Δ short put, $2-below long put, 1330 entry, 1ct, custom 2026-06-15→09-15, xslip 0.05, name RPCTEST-BASE | 200 | `ZT4178951645761466778`; batched w/ member.setData |
| 19:55 | zdte.testResults | `[{id: BASE, pos:true}]` | 200 | status done; 63 positions; stats pnl −150, dd −639, winrate .8254 |
| 19:55 | zdte.testDetails | `[BASE]` | 200 | `opts` echoes sent config verbatim |
| 19:57 | zdte.listTests | `[]` | 200 | RPCTEST-BASE first row — **Step 2 PASS** |
| 19:57 | zdte.startTest | BASE args verbatim, fresh tid only (API call 1/2) | 200 | `ZT4178951664872930779` — new test, **no dedup on identical config** |
| 19:58 | zdte.testStatus | `[REPLAY]` | 200 | done |
| 19:58 | zdte.testResults + testDetails | replay id | 200 | stats **byte-identical** to BASE UI; UI list + detail page show same — **Step 3 PASS** |
| 20:04 | zdte.startTest (UI, captured) | PT50 config = BASE + exits.profits 0.5, name RPCTEST-PT50 | 200 | `ZT4178951705082069481` |
| 20:05 | zdte.startTest | PT50 UI args verbatim, fresh tid (API call 2/2) | 200 | `ZT4178951710152798882` |
| 20:05 | zdte.testResults + testDetails | both PT50 ids | 200 | API run ≡ UI run byte-identical; details echo `exits:{xslip:.05,profits:.5}` — **Step 4 PASS** |
| 20:08 | (page read) | API-PT50 settings panel | — | "PROFIT TAKING 50%", "SLIPPAGE $0.05", name RPCTEST-PT50 — settings view confirms |
| 20:18 | zdte.startTest (UI, captured) | TOUCH config = BASE + exits.touch {usd,0,"$0"}, name RPCTEST-TOUCH | 200 | `ZT4178951789730109583` |
| 20:20 | zdte.testStatus | `[TOUCH]` (no symbol) | 200 | `error: "Data server not available."` |
| 20:21 | zdte.testStatus | `[TOUCH]` retry after 60s | 200 | same error |
| 20:22 | zdte.testResults | `["id-string",{pos:true}]` (wrong shape) | 200 | `error: WHERE parameter "id" has invalid "undefined" value` |
| 20:22 | zdte.testResults | `[{id, pos:true}]` correct shape | 200 | done; 63 pos; pnl +155, dd −214, touch exits 15 |
| 20:23 | zdte.testDetails | `[TOUCH]` | 200 | `opts.exits.touch = {text:"$0",type:"usd",value:0}` echoed |
| 20:24 | zdte.testStatus | `[TOUCH, "QQQ"]` | 200 | `"done"` — **symbol arg is required**; earlier errors were arg-shape, not outage |

## Request-shape differences vs docs/oa-internal-api.md

1. Doc's capture path `data/captures/2026-08-20-recon/` does not exist; actual file is under `data/captures/2026-08-19-recon/`.
2. `testStatus` requires `args:[id, symbol]` — `[id]` alone returns `{"error":{"message":"Data server not available."}}` (misleading message; it is an arg error, not an outage).
3. `testResults` requires the object form `args:[{id, pos:true}]` — positional `["id",{pos:true}]` errors `WHERE parameter "id" has invalid "undefined" value`.
4. UI batches `member.setData` ("bots",{ztestseed:50000}) alongside `startTest`; API replay without it still executes.
5. Errors return HTTP 200 with `{t:"res", tid, api, error:{message}}` — never 4xx; status must be read from the payload.
6. `startTest` returns a bare test-id string in `data`; identical configs create new tests each call (no dedup, shared `okey` notwithstanding).

## Required extra headers (names only)

- `Content-type` (application/json) — the only request header observed on `/api/request`. No CSRF, bearer, or custom auth headers.

## Stop-condition check

No 401/403/429, no /login, no terms/payment prompts, no unrecognized shapes, no API↔UI stat mismatches, no settings drift. All runs verified read-back via `testDetails.opts` + UI settings panel.
