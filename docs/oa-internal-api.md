# Option Alpha's internal RPC API — mapped 2026-08-20

**Status: PARKED FINDING. Nothing here has been replayed.** The API was observed, not exercised.
Every statement below is a first-hand read of traffic OA's own frontend produced while Andy drove
the backtester by hand; no endpoint has been called by us.

**Source:** `data/captures/2026-08-20-recon/oa-network-recon-2026-08-20-00-32-14.CLEAN.json`
— 64 events, captured by `scripts/oa-driver/oa_driver.mjs watch 900`, 2026-08-19 ~20:17–20:32 ET.
The `.CLEAN` file is the artifact of record; see §6 for why the raw file was quarantined.

---

## 1. Shape

One endpoint. Everything goes through it.

```
POST https://app.optionalpha.com/api/request
```

Body is a JSON **array** of calls — the frontend batches several per request:

```json
[{"t":"rpc","tid":"1787185042469-10008","api":"zdte.listTests",
  "args":[{"where":{},"start":0,"limit":30,"order":["updated","desc"]}]}]
```

| field | meaning |
|---|---|
| `t` | always `"rpc"` in everything observed |
| `tid` | client-generated correlation id, `<epoch-ms>-<counter>` |
| `api` | `<namespace>.<method>` |
| `args` | array; for `zdte.startTest` a single config object |

Auth rides the session cookie — no bearer token was present in any observed call.

## 2. Methods observed (backtester = the `zdte.*` namespace)

| method | seen | role |
|---|---|---|
| `zdte.startTest` | 3 | **launches a backtest**; args[0] is the whole config |
| `zdte.testStatus` | 7 | progress poll |
| `zdte.testResults` | 14 | result rows |
| `zdte.testDetails` | 11 | per-column config read-back |
| `zdte.listTests` | 1 | enumerate past tests (`where`/`start`/`limit`/`order`) |
| `zdte.counts` | 1 | test counts |
| `zdte.getBotDefs` | 1 | strategy definitions |
| `zdte.symdata` | 3 | symbol metadata |
| `market.time` | 3 | server clock |
| `member.setData` | 3 | UI/member preferences |
| `bots.listItems` | 1 | **bot list — the live fleet, same endpoint** |
| `accounts.menuItems` | 1 | account menu |
| `posts.exists` | 2 | content/notification check |

⭐ **Progress is POLLED (`zdte.testStatus`), not streamed.** No OA WebSocket was observed at all.
A sweep is therefore a plain request/poll loop — no socket handling required.

⭐ **`bots.listItems` and `accounts.menuItems` mean the live fleet rides this same RPC.** Bot reads
and probably bot edits are reachable here. See §5 before acting on that.

## 3. `zdte.startTest` — the sweep template

`args[0]`, verbatim from variant #1 (SPX long call, 2y):

```json
{
  "entry": {},
  "exits": { "profits": 0.05 },
  "cri": {},
  "series": { "days": 0, "text": "exactly 0 days", "type": "days", "dtype": "m", "compare": "exact" },
  "posLimit": 1,
  "seed": 50000,
  "opp": {
    "type": "longcall", "symbol": "SPX",
    "longCall": { "delta": 0.05, "mode": "closest", "type": "delta",
                  "textValues": { "delta": ".05", "mode": "or closest" },
                  "text": ".05 delta", "optionType": "call" },
    "text": ".05 delta"
  },
  "text": "SPX Long Call",
  "emode": "time", "ntime": 945,
  "psize": { "pct": 10, "prop": "seed", "text": "10% of allocation",
             "type": "drawpct", "textValues": { "pct": "10%", "prop": "allocation" } },
  "period": "2y"
}
```

### The knobs, derived not guessed

Three variants were run in one session and diffed field-by-field. Exactly these differed:

| field | values across the 3 variants | what it is |
|---|---|---|
| `exits.profits` | 0.05 → 0.10 → 0.10 | profit target |
| `opp.longCall.delta` | 0.05 → 0.82 → 0.82 | strike selection by delta |
| `series.days` | 0 → 0 → 1 | DTE |
| `series.filter` | absent → absent → `"*"` | appears only at days ≥ 1 |

Everything else was identical across all three and is the fixed frame: `emode`, `ntime`,
`opp.symbol`, `opp.type`, `period`, `posLimit`, `psize.*`, `seed`, `series.compare`, `series.dtype`,
`series.type`, and the `opp.longCall.mode`/`type`/`optionType` triple.

### ⛔ The display-string trap

`text` and `textValues` are **denormalised mirrors of the numeric values**, and they change with
them: `opp.longCall.delta 0.82` travels with `text: ".82 delta"` and `textValues.delta: ".82"`;
`series.days 1` travels with `series.text: "exactly 1 market day"`.

A sweep that sets `delta` and leaves `text` at the old value produces a test whose label disagrees
with its own config — the exact class of silent mislabelling that made three of four audited bot
config records wrong. **Whether OA validates against these strings or merely displays them is
UNKNOWN and must be tested, not assumed.** Until then, update every mirror.

## 4. What a sweep would look like

Not built. Sketch only, and every step needs first-hand confirmation:

1. `zdte.startTest` with a config → response presumably carries a test id (**not yet inspected**)
2. poll `zdte.testStatus` until complete
3. `zdte.testResults` / `zdte.testDetails` for the numbers and the config read-back
4. compare payload-sent vs `testDetails`-returned — that read-back is the setting-slip check
   `backtest-ingest-protocol.md` §83 currently does from a screenshot

⭐ **The CSV export appears to be built client-side**, not fetched: the download event carried a
blob/data URL whose "host" parsed as CSV header text (`L,Risk,ROR,Premium,Reward`), and no export
endpoint appears in the log. If that holds, a sweep reads positions straight from `zdte.testResults`
and never downloads anything. **Unconfirmed — check before relying on it.**

Compare by **R**, never raw P/L, and keep the 30–40% haircut on absolute economics
(`backtest-ingest-protocol.md` §157). None of that changes because the transport changed.

## 5. ⛔ Reads yes, writes no — for now

Reading through this API is a clear win. **Writing bot configs through it is not**, and the reason
is specific: an RPC call skips the app's own client-side validation. That is precisely how you
create a bot config the UI would never have permitted, and not discover it for weeks — the failure
mode this project already has scar tissue for.

Rule until proven otherwise: **backtests and reads via RPC; bot edits via the browser**
(`oa_driver.mjs`, dry-run default, `--bot` assertion, three-surface verification). §5's two proof
layers are unchanged and are not satisfied by an HTTP 200.

## 6. Provenance and the quarantined raw file

The raw capture also contained 41 WebSocket frames from `naiadsystems.com` — an unrelated site open
in another tab of the same browser. The recorder's `websocket` handler lacked the host filter its
request/response handlers already had.

- `…CLEAN.json` (64 events, `optionalpha.com` only) is the artifact of record.
- The raw 109-event file was moved to `data/captures/2026-08-20-recon/_to_delete/` for Andy to
  delete. It must not be committed.
- Handler fixed 2026-08-20; the fix carries the finding in a comment.

⭐ **The lesson, which generalises past this incident:** a recorder pointed at "the browser" records
the *whole* browser. Scope every capture to the host under study at the point of capture, not
afterwards in analysis.

## 7. Why this is parked

Mapping the API was the perishable, session-dependent work and it is done. Building the sweep costs
the same in October as tonight, so there is no urgency premium. It stays parked until either the
"why did 29 of 44 bots trade zero times" diagnosis returns *strategy* rather than *plumbing*, or
research becomes the thing being waited on instead of triage.

⚠️ Undocumented internal API: no contract, no support, and it will change without notice. Treat a
sweep built on it as something that must fail loudly and be re-mapped, not as infrastructure.
