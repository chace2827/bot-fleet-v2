# GF-QQQ entry-gate forensics — 2026-08-17

**Question asked:** why did the 8-arm GF-QQQ-IC family open a position on only one session
(2026-08-14) in the 08-10 → 08-14 export window?

**Method:** Chrome-direct read of the hydrated OA model (`a5.bots.bot`,
`a5.bots.acedit.routine`) on `GF-QQQ-IC-Ride` (BOTfw5TkkCRF4417860701930934951) and
`GF-QQQ-IC-Canary` (BOTfw5TkkCRF4417860774419022836). Reads only — no edit was attempted,
no automation was saved. All values below are first-hand observations of 2026-08-17.

## 1. The entry gate, exactly as stored

Two shared Library scanners, `sharing: 1`, both referenced by every arm checked:

| | GF-ScannerA-PutSpread | GF-ScannerB-CallSpread |
|---|---|---|
| routine id | `RTfw5TkkCRF178605283747821` | (opened, id not captured) |
| version | **10** | **3** |
| created | 2026-08-06T21:49:52.941Z | 2026-08-07T00:35:50.954Z |
| updated | **2026-08-11T21:52:12.727Z** | **2026-08-11T21:57:48.680Z** |
| config hash | `094f111a703bd392266534774c83f73de6fa18fa6eafa282547f315c49761035` | `ffaaa199982c78552069b53572546d406e351b25ea17e985a4bcc21276e13ea4` |
| payload bytes | 5478 | 5147 |

Hash formula per `oa-ops-runbook.md` §4: `sha256(JSON.stringify({name, inputs, root}))`,
computed after opening the automation fresh.

Decision chain (identical in both, mirrored put/call):

```
Loop QQQ
└ timeofday cop=after  time=1330
  └YES timeofday cop=before time=1400
    └YES stockchangepct cop=gt value=-0.75 prop=close
      └YES stockchangepct cop=lt value=+0.75 prop=close
        └YES "Bot opened a position with <put|call> side today"
          ├YES (empty)
          └NO  Open Symbol Short <Put|Call> Spread
```

Open-action config, both scanners:

- `series: {days: 0, compare: "exact"}` — 0DTE only
- `amount: 1 contract`
- `filter: {minPrice: 0.08}` — **both sides**
- short leg `legpctprice pct=0.4` (`0.4% below` put / `0.4% above` call), `mode: closest`
- long leg `leggap gap=2` (`$2.00` beyond short), `mode: closest`
- exits: bundle-typed Bot Input `GF_EXITS_PUT` / `GF_EXITS_CALL`

**Strike rule confirmed by reproduction.** QQQ 728.87 on 08-14 × (1 − 0.4%) = 725.95 →
closest strike 726; long 2 lower = 724. The export's observed fill is `-726 put, +724 put`.
Exact match. This corrects the prior project note recording the GF strike rule as
`legpctprice pct=0.75` — **the stored value is 0.4**; 0.75 is the *Range* filter, a different
node. (Evidence: this section's first-hand model read, 2026-08-17.)

## 2. Finding A — the sample window is 3 sessions, not 7

`GF-ScannerA-PutSpread` was last written **2026-08-11 21:52 UTC (5:52pm ET)**, i.e. after the
08-11 close, at version 10. `GF-ScannerB-CallSpread` likewise at 21:57 UTC, version 3.

Any GF position opened before 2026-08-12 was produced by a *different* configuration. The
family's fire rate under the current config is therefore **1 of 3 sessions (08-12, 08-13,
08-14)**, not 1 of 7. The pre-registered sample cannot begin before 2026-08-12.

This is exactly the failure the `CONFIG HASH` field in each arm's pre-registration card exists
to prevent, and in `GF-QQQ-IC-Ride` that field is still the unfilled placeholder
`<capture> @ <hash>`, with `SIGNED` blank and `STATUS  DRAFT — unsigned`.

## 3. Finding B — the two gates are anti-correlated (leading hypothesis)

The bot can only enter on a day that satisfies both:

- **Range075** — |QQQ change since previous close| < 0.75% at 1:30–2:00pm → requires a **quiet** day
- **minPrice 0.08** — the 0.4%-OTM, $2-wide, 0DTE spread must be worth ≥ $0.08 at 1:30pm →
  requires **enough premium**, which a quiet day suppresses

These pull in opposite directions. The single observed fill went off at `openPrice 0.07` —
*below* the stated 0.08 floor, i.e. right at the boundary, filled through SmartPricing
(`100% of bid/ask`, `smart: normal`) rather than comfortably inside it.

**Status: LEADING HYPOTHESIS, not established.** It is consistent with every value read and
with the one observed fill, but the decisive per-day evidence is missing (below).

## 4. Finding C — the call side is not structurally broken

`GF_EXITS_CALL` exists, `GF-ScannerB-CallSpread` is enabled, runs every 1m, and its tree is a
correct mirror of ScannerA. The earlier read that the family is "structurally put-side-only"
is **wrong** and is retracted here. The call side is configured and live; it has simply never
produced a fill.

One real asymmetry was found and is unexplained:

| | ScannerA (v10) | ScannerB (v3) |
|---|---|---|
| `price` object | `{text, limit: 100, limitType: "pct", smart: "normal"}` | `{text, pct: 100, smart: "normal"}` |

Same displayed text ("100% of bid/ask"), **different stored schema**. ScannerA carries
`limit`/`limitType`; ScannerB carries the older `pct`. ScannerA has been saved 10 times,
ScannerB 3. Whether the engine treats the legacy `pct` form as a valid limit or silently
fails to price the order is **NOT EVALUABLE from a config read** — it needs the test in §5.

## 5. What is NOT EVALUABLE, and why

- **Per-day gate evaluation for 08-10 → 08-13.** The bot Log holds ~200 rows ≈ 25 minutes;
  at 08-17 it retained only 08-14 15:30–15:55. No per-day decision record survives.
- **QQQ change% at 1:30pm on 08-10 → 08-13.** No market-data source was available in-session.
  Not inferred, not estimated.
- **Whether ScannerB's legacy `price.pct` prices correctly.** Requires a live market run.

## 6. Standing facts captured

- Safeguards (both arms read): `DAILY POSITIONS 2 per day`, `POSITION LIMIT 2 at once`,
  `DAY TRADING Allowed`; scan speeds `AUTOMATIONS 1m`, `EXIT OPTIONS 1m`.
- `GF-QQQ-IC-Ride`: status on, AUTOMATIONS ON, EXIT OPTIONS ON, allocation $2,500,
  net liquid $2,506, `disableExits: 0`, tags `experiment / gfam / arm ride / pr 14`,
  bot version 1 dated Aug 6 2026, Symbols panel **empty** ("No symbols yet" — the loop
  carries `symbols: "QQQ"` inside the automation, so this is not itself a defect).
- Third automation on every arm: `GF-Backstop-1552-FlatClose`, trigger, Mon–Fri 3:52pm EST.
- Pre-registration card (Ride): MAX LOSS ≈$185 net risk per condor, **1 condor/day**;
  SAMPLE TARGET n=100 condors; REVIEW Day-0 + 6 months, interim at n=60;
  KILL Exp(R) per condor < 0 with CI entirely below 0 at n ≥ 60.
  Design rate is 1/day → n=100 in ~100 trading days. Observed under current config: 1 in 3.

## 7. Open items for Andy (all gated — nothing applied)

1. **Sign the arms, or don't.** The `CONFIG HASH` field is blank on a live, funded, ON bot.
   The two hashes in §1 are ready to be stamped. Filling a pre-registration card is gated
   text under CLAUDE.md §5 — not applied.
2. **Rule on the anti-correlated gates (§3).** Any change to `minPrice`, to the 0.4% strike
   offset, or to the 1:30–2:00pm window is a decision and needs "amend the plan".
3. **Rule on the ScannerB `price` schema drift (§4).** Re-saving ScannerB would migrate it to
   the v10 schema, but that is a value change on a live arm mid-sample.
4. **Log retention.** 25 minutes of log on a bot whose whole purpose is a 100-condor sample
   means non-firing days leave no evidence. Consider a daily capture of the decision path.

---

## 8. THE ANSWER — added after cross-checking the 2026-08-11 diagnosis

The 2026-08-11 strike-selection diagnosis (recorded that evening) established:

> PR-01/GF use `legpctprice pct=0.75`, PR-02 uses `delta 0.10`, and that is the ONLY differing
> field. Delta adapts to vol and time-to-expiry; fixed-% of last is blind to both. **Any 0DTE bot
> on `legpctprice` sits outside tradeable premium by construction. Tuning the number cannot fix
> an inability to adapt.**

Its recommendation #1 was: *authorize the 2 GF shared-scanner edits → `delta`.*

**What is in OA today is `legpctprice pct=0.4`.** Still `legpctprice`. The scanners were written
2026-08-11 at ~21:52–21:57 UTC — the same evening.

So the diagnosis was acted on **with the wrong instrument**: the number was tuned 0.75% → 0.4%
instead of the method being changed to `delta`. That is precisely the fix the diagnosis said
could not work, and the outcome matches its prediction:

| | before 08-11 | after 08-11 (`pct=0.4`) |
|---|---|---|
| GF fills | none | 1 in 3 sessions |
| design target | 1 condor/day | 1 condor/day |
| the one fill | — | `openPrice 0.07`, **below** the `minPrice 0.08` floor, via SmartPricing |

A fixed 0.4% of last is still blind to vol and DTE. It simply lands close enough to clear the
premium floor *occasionally*. The single fill clearing at 0.07 — under the stated floor — is the
signature of a strike rule that is marginal rather than correct.

**This supersedes §3 as the leading explanation.** The Range075 / minPrice anti-correlation in §3
is real and still worth ruling on, but it is a second-order effect: the first-order cause of the
low fire rate is that the strike-selection *method* was never changed.

**Consequence for §2:** the 08-11 rewrite is not an incidental config touch. It is the partial
application of a known diagnosis, and it resets the sample window. No GF position before
2026-08-12 belongs to the current arm.

**Open, unchanged from 08-11:** what delta for QQQ? 0.10 is the only observed-working value but it
is SPX with $5 wings; GF is QQQ with $2 wings. Copying 0.10 is a defensible starting point, not a
derivation — and it must be proposed as a *method* change, stated plainly as the fix the 08-11
number tune was a substitute for.
