# Phase 1 — Stage 1: QQQ 0DTE iron condor + fixed put-side overlay (T4)

**Purpose.** Does a fixed-side protective overlay improve the actual QQQ
iron-condor primary? Stage 1 only: four standalone backtests plus one presence-
gated combine. **PUT-SIDE ONLY** — the overlay is a Long Put Spread on the put
side, chosen because it is the side the arm table specifies; side selection is a
choice, not a finding. The overlay is a **fixed-side unconditional overlay with
a presence gate** — nothing in it reads the primary's state except open/not-open
at entry time.

Captured 2026-09-17T02:34:34-0400 (America/New_York). Host
`app.optionalpha.com`, PAPER account. Raw captures are unmodified; derived files
name their raw source and its SHA-256.

## Files

| File | SHA-256 (prefix) | What |
|---|---|---|
| 01-p1-stage1-capture-2026-09-17-0234.txt | (see SHA256SUMS) | Raw capture: session, configs, rendered results, crules, reconciliation, refusals |
| standalone-S1-0.csv | 229c5a3d… | S1-0 positions export, 353 rows |
| standalone-S1-a.csv | 79c01c34… | S1-a positions export, 353 rows |
| standalone-S1-b.csv | 4aed3fca… | S1-b positions export, 353 rows |
| standalone-S1-c.csv | 7c9560c4… | S1-c positions export, 1,109 rows |
| combined-S1-H.csv | 33a34155… | S1-H combined export, 669 rows (Test col A|B) |
| 02-stage1-metrics.md | (see SHA256SUMS) | Derived R metrics; names every source hash |
| screenshots/ | (see SHA256SUMS) | Per-arm config + results, compare results, combined positions drawer |

## The five arms

| Arm | OA test id | N | Exp(R) | Win rate | Max DD (R) | Worst R | Unit |
|---|---|---|---|---|---|---|---|
| S1-0 control | ZT41789623864833548127 | 353 | +0.0367 | 84.70% | 5.38 | −1.00 | per IC position |
| S1-a (stop 100%) | ZT41789624201365562128 | 353 | +0.0323 | 72.24% | 4.16 | −1.00 | per IC position |
| S1-b (stop 200%) | ZT41789624286078295129 | 353 | +0.0382 | 80.74% | 5.28 | −1.00 | per IC position |
| S1-c overlay standalone | ZT41789624566260834130 | 1,109 | −0.2047 | 16.41% | 253.91 | −1.00 | per debit-spread position |
| S1-H combine | — | 353 condors | −0.0019 | 35.41% | 8.28 | −1.00 | per condor, ex-artifact |

**S1-H denominator:** primary risk + overlay debit, per condor, ex-artifact.
316 of 353 condor-days carry both legs; 37 carry the primary alone.

Dollar sanity (rendered): S1-0 +$2,030 · S1-a ~+$1.9K · S1-b ~+$2.1K ·
S1-c −$6,110 · S1-H +$83.

## Combine rule — verbatim crules payload (re-read from location.href)

```json
{"posLimit":2,"posLimitDay":2,"rules":[{"type":"state","test1":"ZT41789624566260834130","test2":"ZT41789623864833548127","state":"open","text":"Only open Test B if Test A is open"}]}
```

URL: `/backtests/compare/ZT41789623864833548127,ZT41789624566260834130?crules=<above,url-encoded>&combine=1`.
A = S1-0 (predicate), B = S1-c (gated). `open` = concurrent presence at B's
14:00 entry moment. Caps pinned explicitly at 2/2 — defaults not accepted.
Rendered counts 353 / 1,109 / 669; unruled would be ~1,462, so the rule ran.

## Reconciliation result (row-for-row before any ranking)

- Combined A rows: **353/353 = exact match to standalone S1-0.** 0 missing, 0 extra.
- Combined B rows: 316, all exact subsets of standalone S1-c rows; 0 extra;
  every combined-B day is an A-day (gate never fired without presence).
- 16 A-days have no standalone-B row at all (overlay simply didn't trade;
  nothing to include).
- **21 A-days have a standalone-B row but no combined-B row — silent drops,
  the phase0c §1 anomaly replicated at 21×.** Every date + both rows listed in
  01-capture §7. Dropped rows' standalone aggregate: **+$580 P/L / $715 debit**.
  The export is a result, not a census; reported, not absorbed. S1-H figures
  reflect the export exactly as written.

## Iron-Condor-vs-paired-spreads divergence

The live fleet builds the primary as TWO PAIRED SPREADS (ScannerA put /
ScannerB call). The backtester only offers a single Iron Condor structure,
which collapses per-side exit independence. Used as-is; stated, not smoothed.

## Docs-vs-render deltas

- Dispatch says overlay "1 contract … same test period"; render confirms
  $50,000 allocation / 1 contract / 5Y — matches.
- Stop-armed arms still produced −1R rows (S1-a: 14, S1-b: 20, status
  `expired`) — the stop does not guarantee the level; docs describe SL% as a
  cap on loss, render shows otherwise on those rows.
- Combine "Count" column: 669 rendered; reconciliation shows 353+316 with 21
  silently dropped B rows — larger drop count than phase0c's single-row case.
- Test period: longest offered = **"5Y"** (picker option verbatim). S1-c spans
  ~Sep 2021 – Sep 2026 rows (first row Sep 29, 2021; last Aug 28, 2026) — the
  5Y label covers a ~5-year window including future-dated 2026 rows, i.e. the
  sim calendar runs past today. Noted, not resolved.

## Assumptions

- S1-c strike selection: short leg 0.75% below underlying (same reference as
  the primary's short put), long leg $2.00 above it — the closest expressible
  equivalent of the dispatch spec; confirmed verbatim on the settings card.
- S1-c has no entry filter and no position criteria (spec silent; unconditional
  overlay intent). Result: it trades 1,109 of ~1,250 days.
- Combine built by URL-addressable crules (proven to round-trip identically to
  drawer-built rules, phase0c bundle §5) rather than drawer pickers; drawer was
  not needed for correctness and its state is documented unreliable.
- 16 no-B-row days treated as overlay non-trades (data/fill gaps in B
  standalone), not as gate failures — gate only admits; it cannot create rows.
- Exp(R) uses export `P/L ÷ Risk` per row; S1-H pairs rows by Exp date into
  one condor-day before computing R.

## Questions for Andy

1. The 21-row silent drop is now a replicated, material behavior (drops carried
   +$580). Do you want a second ruled-combine run to test drop determinism, or
   is one reconciliation enough for Stage 1?
2. S1-c traded 1,109 days vs primary's 353 — overlay is unconditional by design.
   Stage 2 sizing should know the gate admitted B on 316/353 primary days.
3. The sim calendar runs past today (rows through Aug 2026) — is that expected
   for the 5Y period, or should the window be re-anchored?

## Refusals / anomalies this run

- Copy CSV never wrote the clipboard under CDP (stale clipboard content on JS
  and trusted clicks, `clipboard-write` granted). Worked around via Download
  CSV + `Browser.setDownloadBehavior` into the bundle dir.
- Trusted clicks did not fire several delegated `data-click` handlers;
  `element.click()` did. Used only for read-only navigation + export clicks.
- One accidental Combine-Results toggle-off while probing the rules drawer;
  URL lost `&combine=1`. Restored by re-navigating to the full crules URL;
  re-rendered 669 identically and URL re-read after.
- Combined rules drawer could not be re-opened non-destructively; rule evidence
  is the verbatim URL payload + the 669 ruled count (≠ ~1,462 unruled).
- Chrome was closed once mid-session; operator re-authenticated. Agent never
  touched a login form. PAPER re-verified on /home before continuing.

## Stop condition

None fired. Stage 1 complete; **stopping here per dispatch — no Stage 2.**

**No recommendation is written.** These are T4 figures (single platform, one
window, one configuration family). Whether the paper-arm preauthorization bar
is cleared is Andy's decision on these numbers, not a verdict in this bundle.
