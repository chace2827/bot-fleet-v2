# FINISH — capture-diff: Step 6 (clone final) vs Step 0 (original baseline)

Run 2026-08-04. Compares `06-clone-final/*` (bot BOTfw5TkkCRF2717857919585029021, now named
`QQQ-IC-0DTE-Fortress`) against `00-original/*` (bot BOTfw5TkkCRF817734373392552121, now named
`QQQ-IC-0DTE-Fortress-ARCHIVED-2026-08-03`).

Method: field-level comparison of decoded values, NOT rendered-label comparison.
Rationale: decision-memo-2026-08-04.md Decision 7 item 2 — OA re-serializes an `exits` blob on
save even when nothing changed, so a label diff reports false differences.

**VERDICT: no unintended edits. Every difference is accounted for.**

---

## A. Differences INSIDE the exit block — intended by the card

| # | Difference | Origin |
|---|---|---|
| 1 | NEW automation `Fortress-Backstop-1552-FlatClose`, TRIGGERS class, Mon-Fri 3:52pm EST, Close Position 100% of position, Price Market, memo `1552 backstop flat close`. Automation count 2 -> 3. | Card Step 5b, built 2026-08-03, reload-verified. INTENDED. |

Nothing else in the exit configuration changed. PT50 and the 15:50 Expiration exit were ALREADY
present on the original (Step 0 finding 1); card Step 5a was a verification, not an edit.

---

## B. Differences OUTSIDE the exit block — FINDINGS, reported not fixed

| # | Difference | Status |
|---|---|---|
| 2 | **BOT GROUP `Monitor` -> `None`** | Clone trap: Bot Group is not carried on clone (session-log 2026-08-03 finding 4). RULED 2026-08-04: stays unset until the Phase 4 sweep, when the `Group = Pillar` scheme is applied. NOT FIXED, by ruling. |
| 3 | **EXIT OPTIONS toggle `OFF` -> `ON`** | The clone was BORN with it ON (session-log 2026-08-03 finding 5). Left ON then and now; the card's rule is "leave them as they are". Switching it off would be an unrequested edit. NOT FIXED, deliberately. |
| 4 | **ScannerA exits label `"Profits: 50%, ..."` -> `"Profit: 50%, ..."`**, and its `sig` gained an `xevents` key. ScannerB still reads `"Profits:"` and has no `xevents` key. | The 2026-08-04 TIER2-CHECK4 save residue. **Numeric payload byte-identical on both sides: `^^0.5\|0.01^$0`** = 50% PT, 10-min expiration, Market on the expiration exit. RULED KEEP: a re-serialization cannot be reverted by saving. Cosmetic. |
| 5 | **NEW: Template binding + BOT VERSION panel** on the bot settings page — `Template: QQQ-IC-0DTE-Fortress`, `BOT VERSION 1, Aug 4, 2026`. | Created by this session's Step 7. INTENDED. See the finding below. |
| 6 | **Trade history: 41 closed positions / -$1,834 / chart since Mar 13 2026 -> 0 closed positions / chart since Aug 3 2026** | Expected. A clone starts at n=0; that is exactly what PR-03 declares ("this starts at n=0"). |
| 7 | **NET LIQUID / AVAILABLE `$98,166` -> `$100,000`** | Consequence of #6. |

---

## C. Verified IDENTICAL, field by field

- **Automation trees**, node for node, both scanners, every decision node exposing BOTH branches.
  0 nodes carried a collapsed class at capture time.
- **ScannerA action**: Symbol QQQ · exactly 0 days · Long Put $2.00 below short put leg ·
  Short Put 0.75% below underlying price · Up to $5,000 risk · Price Market · Tags `put side`
- **ScannerB action**: Symbol QQQ · exactly 0 days · Short Call 0.75% above underlying price ·
  Long Call $2.00 above short call leg · Up to $5,000 risk · Price Market · Tags `call side`
- **Exit bundle, decoded, BOTH sides**: profits `0.5` · smprofits `normal` · expdays `0.01` ·
  smexpdays `market` · dprofit/price/stoploss/dstop/tstop/touch/xevents/epsdays all `""`
- **Entry Criteria**: all 7 unchecked, both sides, both bots
- **Position Criteria**: 1 of 16 checked — Mid price between $0.08 and no max — both sides, both bots
- **Safeguards**: Allocation $100,000 · Daily 2 per day · Position limit 2 at once · Day trading Allowed
- **Scan speeds**: AUTOMATIONS every 1m · EXIT OPTIONS every 1m
- **Symbols**: "No symbols yet" on both — CORRECT, the symbol lives in the automations
  (`Loop QQQ` + action `Symbol: QQQ`). Card Trap 2 does not bite this bot.
- **Activity Alerts**: Open position · Close position · Automation warning · Automation error, all on
- **Tags**: `experiment` (dropped on clone, restored this session)
- **AUTOMATIONS toggle**: OFF on both

---

## D. What this diff CANNOT establish

The behavioural layer. `oa-ops-runbook.md` 4.2: the Exit Options panel is never evidence, because
exits are copied onto a position at open and can diverge from the panel silently. In v1 the panel
read `PROFIT % 50%` while the positions generated **no exit orders at all**.

**DEFERRED TO DAY-0** — not done, not partially done:
- first new position's Trades list must contain a PT row AND a time-exit row
- BACKSTOP_CAUGHT_IT check: the 15:52 backstop must NOT be the thing closing positions
- DST / "Market Time (EST)": whether `ntime=1552` fires at 15:52 ET in August
- NEW, opened 2026-08-04: `itmpaper` is now `market`, which closes ITM positions **10 minutes
  before the close** — the SAME instant as the bot's own Expiration exit. Watch for a race.
