# Config Record vs. Reality — Fleet Audit 2026-07-28

> **The single biggest theme of the execution audit.** Across four bots and 35 losing positions, **66% of losses classified as `settings`** — the bot doing something other than what `bots_config.csv` and `oa-platform-reference.md` say it does. Only **9%** were OA platform failures.
>
> This table is the reconciliation. Every "Actual" cell is sourced from an OA automation tree, Exit Options panel, or Trades list supplied 2026-07-27/28 — not inferred from P/L unless marked.

---

## 1. IC-SPX-FastPT25-S2 — the champion

| Field | Config record | **Actual** | Status |
|---|---|---|---|
| Entry time | 11:00 | **11:00** — `Current market time is after 11:00am`, a real node | ✅ |
| Filter | Range075 + skip FOMC | **Both present**, Range075 as a two-sided %-change gate | ✅ |
| Profit target | PT25 | **Attached** (`25% of credit`, pricing **Normal**) — but **generated zero exit orders across all 47 post-fix positions** | ❌ **BROKEN** |
| Hedge | S2 strike-touch | **Fires correctly and fast** (2 min on 7/02) | ✅ |
| Exit pricing | "Fast / 100% bid-ask" | **Three different settings:** PT25 = Normal · S2-StrikeTouch = Fast · **Cleanup = Market** | ⚠️ incomplete |
| Re-entry gate | ≤10 | Gates on **currently-open** put positions → **can loop** (7/01, 10 round-trips in 29 min) | ❌ **DEFECT** |
| Bid-Ask Guard | *unrecorded* | **OFF** (unchecked, blank) | ⚠️ missing |
| Cleanup automation | *unrecorded* | **`Scalp-Mon-S2-Cleanup`** — closes any position open ≥2 min when only 1 position is open. **Uses Market pricing.** | ⚠️ missing |

**The 6/14 Market→SmartPricing remediation reached `Scalp-Mon-S2-StrikeTouch` but NOT `Scalp-Mon-S2-Cleanup`.** Cleanup still sends Market orders — the same configuration that produced the $3,000 structurally-impossible fill on 6/11.

---

## 2. QQQ-IC-0DTE-Range075-PT50-Wide2-1230PM

| Field | Config record | **Actual** | Status |
|---|---|---|---|
| Profit target | PT50 | **Put side: attached, fires 21/21.** **Call side: NOT attached — 0 of 15 reachable opportunities fired** | ❌ **HALF-BROKEN** |
| Stop / hedge | `<verify>` | **NONE.** No stop, no touch hedge ever fired across 40 positions | ✏️ **fill in: none** |
| Re-entry | `<verify>` | **0** — max 1/side/day, zero exceptions in 23 days | ✏️ **fill in: 0** |
| Time exit | *unrecorded* | **15:50 flat exit** — drives 19 of 40 closes, including **all 6 losses** | ⚠️ missing |

*Call-side non-attachment is INFERRED (strong) from 21/21 vs 0/15; no screenshot supplied for this bot.*

---

## 3. QQQ-IC-0DTE-HedgeD-Conditional

| Field | Config record | **Actual** | Status |
|---|---|---|---|
| Entry time | `<verify>` | **11:00** | ✏️ fill in |
| Filter | `<verify: Range075>` | **NONE — no filter node exists.** 16 of 45 entry days (36%) opened outside ±0.75% | ❌ **MISSING** |
| Profit target | `<verify>` | **PT50, both sides** — 69 of 70 winners closed at their own MFE timestamp | ✏️ fill in |
| Hedge | "Conditional" | **`$1 in the money` + `open 30 minutes or more` → Close.** The second gate is **position age**, not breach persistence — permanently true after 11:30 | ❌ **MIS-DOCUMENTED** |
| Re-entry | `<verify>` | **0** — gates on `opened this side today` (per-day flag) | ✏️ fill in |
| Expiration exit | *unrecorded* | **10 min before close, Market pricing** | ⚠️ missing |
| Bid-Ask Guard | *unrecorded* | **OFF** | ⚠️ missing |

**`oa-platform-reference.md` §14 defines Conditional as *"sustained ~$1 past the strike for ~10 minutes."* There is no time-persistence condition anywhere in either monitor.** What ran is an immediate $1-ITM stop.

---

## 4. DIR-SPX-PutVIX22-SL75

| Field | Config record | **Actual** | Status |
|---|---|---|---|
| Filter | VIX ≥ 22 | **Correct** — VIX never reached 22 on any of 22 trading days since 6/25 (max high 20.72) | ✅ |
| Everything else | PT100 / SL75 / 11:00 / 1ct | **UNVERIFIED — zero positions, zero information** | ⚠️ **untested** |
| Automations ON? | assumed yes | **UNKNOWN.** A correctly-gated bot and a switched-off bot emit identical evidence | ⚠️ **unverifiable** |

---

## 5. The QQQ hedge tournament — fleet-level

| Claim | **Actual** |
|---|---|
| All four arms are Range075 bots | **None of them is.** All four run the identical filter-free 4-node scanner |
| Four independent hedge mechanics tested | **~Three.** S1 and Conditional share **identical P/L on 73 of 86 positions (85%)** |
| S3 = "50% max-loss stop" | **A percentage-of-*credit* stop, SL50–SL75 range.** Exits at ~$0.24 median vs ~$1.07 for a true 50%-max-loss stop — **an order of magnitude tighter** *(INFERRED from exit ratios + 44/44 MAE fingerprint)* |
| Arms differ only in hedge | **They also differ in execution class.** S3 = Exit Option (1-min, runs **first**). S1/S2/D = Monitors (scan speed, run **third**). S3's win is confounded with being the fastest implementation |
| Conditional was tested | **Never implemented as specified**, and now **untestable** — modelling a 10-min sustain needs 5-min tape, and Tradier's window opens 2026-05-29 vs a last position of 2026-05-22 |

**Consequence: the tournament cannot select a fleet hedge until the arms are rebuilt.** `current-state.md` currently assigns the hedge question to this tournament.

---

## 6. Cross-bot corrections to existing records

| Record | Correction |
|---|---|
| `current-state.md`: *"7/2's −1550 was a genuine put breach where **S2 fired and cut early (helped** — hold-to-expiry ≈ max loss)"* | **Wrong.** SPX settled **7483.24**, 38 pts *above* the 7445 short put; legs settled $0.05/$0.03. **Hold-to-expiry was a full winner, +$350.** S2 cost $2,300. `PRICE AT CLOSE 7,442.66` on the OA panel is SPX at the 13:02 exit, not the 4:00 close |
| `current-state.md`: *"S2 mechanic is healthy in production"* | **Healthy ≠ profitable.** S2 executes correctly and cost **−$3,285** over the post-fix window (−$6,285 raw, less the $3,000 6/11 artifact) |
| `current-state.md`: *"QQQ hedge family … strike-bug contaminated"* | **Does not apply to HedgeD** — 0 of 86 positions have malformed strike geometry |
| Champion's **G2 go-live gate (18/15 clean condors)** | Those condors were produced by **ride+S2**, not PT25+S2. **The gate certifies a strategy that never ran** |
| 6/11 T00147 −$7,740 | **$3,000 of it is not a real loss.** A $5-wide spread filled at $7.50 into a 0×7.50 quote. Exclude from performance records |

---

## 7. Architecture note — the QQQ bots are built right, the SPX champion isn't

Both carry a Cleanup-family automation. Only the champion loops.

| | Champion `Scalp-Scan-Put` | QQQ `HedgeB/D-Scan-Put` |
|---|---|---|
| Re-entry gate | `Bot has exactly 0 positions with put side and **open status**` | `Bot **opened** a position with put side **today**` |
| Can Cleanup→Scanner loop? | **Yes** — 10 round-trips on 7/01 | **No** — locked out for the day once traded |

Same Cleanup automation, different gate, opposite outcome. **The QQQ pattern is the correct one.**

---

## Legend
✅ config matches reality · ✏️ blank in config, now known · ⚠️ real behaviour absent from the record · ❌ config asserts something false

*Sources: OA automation trees, Exit Options panels, Trades lists and Automation Logs supplied by operator 2026-07-27/28; `data/trades.csv`; Tradier daily/intraday history. Per-position detail in `docs/execution-audit-*.md`; per-position rows in `data/execution_audit.csv`.*
