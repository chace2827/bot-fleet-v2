# OA internal backtest API — RPC verification — 2026-09-15

**Verdict: OA backtest API: USABLE** — a single `zdte.startTest` POST runs the exact config sent (verified by `testDetails.opts` echo and the UI settings panel), produces results byte-identical to UI-built twins, and needs nothing beyond the session cookie and a `Content-type` header.

## Step results

| Step | Result | Evidence |
|---|---|---|
| 2 — `listTests` read | PASS | `listTests-01.json` (RPCTEST-BASE present) |
| 3 — API replay of BASE | PASS | `replay-details-results.json` + `replay-body.json`; stats byte-identical to BASE UI; UI list/detail show same numbers |
| 4 — PT50 variant via API | PASS | `variant-diff.txt`, `pt50-both.json`, `pt50-settings.png`; UI settings view shows "PROFIT TAKING 50%" / "SLIPPAGE $0.05" |
| 5 — UI PT50 twin + Touch discovery | PASS | `pt50-ui-args.json` (UI args ≡ API variant args except name/tid), `touch-field-diff.txt`, `touch-startTest-req.json` |
| 6 — Trade-level detail | PASS | `trades-sample.json`, `touch-results-raw.txt`, `touch-details-raw.txt` |

## Stats table

| stat | BASE (UI) | Replay (API) | PT50 (API) | PT50 (UI) | TOUCH (UI) |
|---|---|---|---|---|---|
| test id | ZT4178951645761466778 | ZT4178951664872930779 | ZT4178951710152798882 | ZT4178951705082069481 | ZT4178951789730109583 |
| Total P/L | -$150 | -$150 | -$173 | -$173 | +$155 |
| Max drawdown | -$639 | -$639 | -$487 | -$487 | -$214 |
| Return on DD | -23.5% | -23.5% | -35.5% | -35.5% | +72.4% |
| Trades | 63 | 63 | 63 | 63 | 63 |
| Win rate | 82.5% | 82.5% | 90.5% | 90.5% | 74.6% |
| Profit factor | 0.87 | 0.87 | 0.76 | 0.76 | 1.21 |
| Avg P/L | -$2.38 | -$2.38 | -$2.75 | -$2.75 | +$2.46 |
| Avg win / avg loss | $18.9 / -$113.3 | $18.9 / -$113.3 | $9.7 / -$121 | $9.7 / -$121 | $18.96 / -$49.07 |
| Exits | expired 63 | expired 63 | profits 54, expired 9 | profits 54, expired 9 | touch 15, expired 48 |

BASE-UI and Replay-API stats objects are **byte-identical**; PT50-UI and PT50-API are **byte-identical** (all 30 stat fields equal).

## Request shape vs docs/oa-internal-api.md

1. Doc's capture path `data/captures/2026-08-20-recon/` doesn't exist; actual file is under `data/captures/2026-08-19-recon/`.
2. `testStatus` requires `args:[id, symbol]` — omitting the symbol returns `error:"Data server not available."` (an arg error in disguise, not an outage).
3. `testResults` requires `args:[{id, pos:true}]`; positional `["id",{pos:true}]` fails with `WHERE parameter "id" has invalid "undefined" value`.
4. The UI batches `member.setData` ("bots",{ztestseed:50000}) with `startTest`; API replay without it works fine.
5. Errors return HTTP 200 with `{t:"res",tid,api,error:{message}}` — check the payload, not the status code.
6. `startTest` has no dedup: identical configs create a fresh test each call.

## Touch exit — UI surface and wire fields

Touch editor popover (verbatim):
- Title: **"Close position if underlying price is..."**
- Value input: number, placeholder `0`, step `0.01`
- Unit pick items: **"$"** (value `usd`), **"%"** (value `pct`)
- Fixed suffix text: **"from ITM or less"**
- Info tooltip: "Use a negative value to allow the position to go ITM before exiting"
- Buttons: Cancel / Clear / Apply

Choice made: `0` + `$` = underlying 0 dollars from ITM = touches the short strike.

Wire fields (see `touch-field-diff.txt`): `exits.touch = {"type":"usd","value":0,"text":"$0"}` — the only diff vs BASE besides `name`. `testDetails.opts` echoes it back identically.

## Trade-level fields (Step 6)

Available per trade in `testResults.results[]`:
- **Entry time**: `ntime` (HHMM int, e.g. `1330`) + `ndate` (YYYYMMDD)
- **Exit time**: `closeTime` (YYYYMMDDHHMM — full intraday minute) + `cndate`
- **Exit reason**: `status` — observed values `expired`, `touch` (also `profit` seen in PT50 run's stats.exits)
- Others: `pnl`, `risk`, `premium`, `closePrice`, `upriceClose`, `slip`, `legs[]` (entry legs w/ OCC id, delta, strike), `clegs[]` (closing legs — touch trades only), `bac` (touch trades only), `exdate`, `maxLoss`, `maxProfit`, `ror`, `rwr`

**Touch exits: 15 of 63 trades**, each with a specific intraday `closeTime` (14:06–15:58 ET range, e.g. `202606161554` = 3:54pm). Expired trades close at `…1600`. So yes — touch exits carry real intraday timestamps, not synthetic EOD times.

## Required extra headers (names only)

`Content-type` — the only header the UI sends on `/api/request`. No CSRF, bearer, or custom auth headers observed; auth is the session cookie.

## Risks / unknowns

1. **ToU exposure is real and unresolved.** This run was AI-driven browser control + scripted RPC on a clause that prohibits exactly that without written authorization; the account (44 bots, backtest history) is the thing at risk. Ask OA via the Contact form / team@optionalpha.com before any repeat.
2. **Undocumented internal API.** Already quirky (misleading error strings, arg-shape sensitivity); can change or disappear without notice.
3. **`startTest` bypasses client-side validation.** A malformed config could yield garbage or a stuck test; no dedup means reruns stack up rows.
4. **Coverage is narrow.** Verified for one strategy family (QQQ short put spread, 0DTE, custom range) with 2 API starts; other strategies/fields/periods are unverified, and heavy use is untested.
5. **Detectability.** API replays omit the UI's `member.setData` companion and page-flow choreography; they look normal per-request but are reconstructible in server logs if OA ever audits.
