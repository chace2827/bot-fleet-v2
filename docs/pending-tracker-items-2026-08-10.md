# PENDING TRACKER ITEMS — fold into the `bot-fleet-migration` artifact on Thursday

> **Temporary holding file, created 2026-08-10.** Exists only to keep artifact updates out of
> a constrained usage week. Everything here is a tracker item that has NOT yet been added to
> the artifact. **Delete this file once the items are folded in.**

## NEW ITEM — [CLAUDE] Chop-day aggressive IC: detector + bot + backtest
**Andy, 2026-08-10.** Build a backtest **and** a bot that **detects a likely chop day early in
the session** and then opens **aggressive** iron condors — closer strikes / more premium — on
the thesis that price stays near its current level.

**⚠️ THIS IS NEW WORK. NO PRIOR ART. (Andy, explicitly, 2026-08-10.)** Nothing like it has
been built or backtested before. **It is also SEPARATE from the GF-arm / 1:30–2:00pm window
investigation** — do not merge the two, do not let one gate the other.

**Do not confuse it with the Range075 family.** `QQQ-IC-0DTE-Range075-PT50`, the two `-Wide2-`
variants, `QQQ-IC-0DTE-VIX25-Range075-PT50`, and the `±0.75% since previous close` gate on every
GF arm are **PASSIVE**: they refuse to trade when it is not quiet. Andy's item is **ACTIVE**:
detect quiet early, then *lean in* — tighter strikes, more credit, possibly more size. Different
mechanic, different hypothesis, different bot. The only thing worth borrowing from those bots is
the range-measurement plumbing, not the design.

**Pre-register before any restart** (`CLAUDE.md` §5): hypothesis, kill criterion, sample target,
review date, config-capture hash. Backtest first — `docs/backtest-ingest-protocol.md` is the
processing contract.

**Open design questions:** what counts as an early chop signal (realized range by 10:30? gap
size? VIX? opening-range width?) · how early is early enough to still collect premium ·
how much more aggressive, and against which control.

---

## AGREED THURSDAY SEQUENCE (2026-08-10, after usage reset)
1. **Confirm the GF strike config** — read one arm's Open Position action first-hand:
   selection type (%OTM vs delta) and width. Cheap, and it kills or confirms the hypothesis
   below before any backtest spend. **Do not wait on this one.**
2. **Fix `bots_config_v2.csv`** — its schema (`object_kind,name,oa_id,version`) carries none of
   the graded mechanic columns, which kills instruction-mirror grading, 5 detector rules, and
   §3 of the daily brief. **Highest-leverage item in the folder.**
3. **Re-sync the Tradier API**, then render the **proper** brief per `daily-loop-spec.md` §6 —
   tape chart per underlying, ±0.75% GO zone as a shaded band, marker convention
   (● entry · ◆ defensive exit · ▪ profit target · no mark = rode to expiry), descriptive
   legend, quantified regime read, expected-vs-actual. **As a persisted HTML artifact.**
   Render for all accumulated days, not just Thursday.
4. **Backtests** — `docs/ic-trailing-stop-backtest.md` is already spec'd with 5 pre-registered
   arms. Add a strike-selection batch: **delta vs %-OTM**, **$2 vs $5 width**, at the 1:30pm
   entry. Plus the chop-day item above.

**This week's posture (Andy, 2026-08-10): investigations and cleaning up bots/automations only.
The proper review process resumes after Thursday.**

---

## STANDING HYPOTHESIS from Day 1 (unconfirmed — item 1 above tests it)
Fixed **%-OTM** strike selection breaks at a **1:30pm** entry: 0.75% is a session-sized distance,
unreachable with 2.5 hours left, so premium → $0.02 and the $0.08 floor correctly rejects it.
**Delta** selection auto-tightens as theta burns; percentage selection cannot.
Evidence: PR-02 (`−10Δ` per `ic-trailing-stop-backtest.md:33`, **$5** wide) entered 1:31pm the
same quiet day and collected **$0.60** → **+$600**. GF candidate was **$2** wide at **$0.02**.
⚠️ The GF arms' selection type has **NOT** been read first-hand — this is an inference from the
observed strikes (-716/+714) plus the documented convention. Confirm before acting.

## ALSO PENDING for the artifact
- `lessons.py` refuses to truncate `data/lessons.csv` (33 v1 rows) without
  `data/archive/lessons-v1.csv` written first. **Archive decision, GATED.** v1 rows are
  currently a post-cutover reporting input.
- 3 OA-archives still owed (Andy's hand; verify by ID + footer 43→40).
- 4 ON bots never read on Day 1: `DIR-SPX-CallVIXdrop`, `DIR-SPX-PutVIX22-SL75`,
  `Trendy-Paper-v1`, `Friday 14 DTE Broken Wing IB`.

---

## ⭐ BACKTEST HISTORY FOUND (other Claude project, 2026-08-10) — AND IT IS ALL SPX

Retrieved from `QQQ_IC_Checklist2.jsx` + `infrastructure.md` in another Claude project.
**Summary text only — no positions.csv, no Compare grid, no R values.** Marked ACTUALLY RUN.

**Validated on SPX (0.75% OTM, $5 wide baseline):**
- **Entry time:** Round A — **1:30 PM standard width $744K, PF 3.31, 12L, DD -$100K** ·
  1:30 PM Wide2 $541K, PF 2.88 · **12:00 PM and 1:00 PM REJECTED (17L/24L)**.
  → **The 1:30 PM entry is the WINNER, not the suspect.**
- **Strike distance:** Round D — Strikes050 / 100 / BearAsym tested,
  **0.75% symmetric CONFIRMED OPTIMAL** (beat both 0.50% and 1.00%).
- **Width:** Round E — **$1.50 REJECT · $2.50 REJECT · $3.00 REJECT · Asymmetric REJECT**
  against the **$5** baseline. **Every narrow width was rejected.**
- Exits: PT25 REJECT / PT60 $477K / NoExit $619K · PT50 DROPPED · PT25 is the floor
  (all lower PTs negative) · S2 confirmed on **964 trades** · 7–9 re-entries optimal.
- Walk-forward PASSED twice (2016-23→2024-25; 2016-24→2025-Q1'26). 40 OO backtests, 17 on 2yr.
- Champion crowned: **Scalp — 11AM, PT25, S2, 10 re-entries** (= `IC-SPX-FastPT25-S2`, PR-01).

**⛔ EVERY ARM ABOVE IS SPX. NONE IS QQQ.** `oo14` ("SPX vs QQQ comparison: same parameters,
compare WR/PF/DD") is **STILL UNCHECKED**. Also unrun: `oo7` (full sweep: 7 entry times × 4
filters × 6 hedges × 3 widths × 4 PTs), `ad12` (earlier entries with filters).

### ⭐⭐ THE FINDING THIS PRODUCES
**The GF family is a QQQ build running parameters validated only on SPX, never re-validated on
QQQ.** SPX ≈ 7,750 and QQQ ≈ 720 — a $5 SPX spread is **0.065%** of the underlying; a $2 QQQ
spread is **~0.28%**, i.e. ~4× wider in relative terms. Absolute widths do not port between
these two instruments, and 0.75% OTM does not have to behave the same on both.
**This outranks the $0.08 mid-price floor as the Day-1 explanation.** The floor is a symptom.

### HYPOTHESIS STATUS — my Day-1 hypothesis is now WEAKENED, not confirmed
I proposed that fixed %-OTM breaks at a 1:30 PM entry. Round A says 1:30 PM is the best entry
time tested and Round D says 0.75% is optimal — **on SPX**. But PR-02, which worked today
(+$600, $0.60 credit, $5 wide), selects on **−10Δ** ≈ **0.26% OTM** at 1:31 PM, not 0.75%.
So delta-vs-percentage at a late entry is **still unresolved**, and cannot be resolved from
summary lines. **Do not treat any of this as settling the GF question.**

### ⚠️ UNACTIONED LIVE-FLEET FINDING — THURSDAY
`infrastructure.md` (Grid Optimizer, real OO trade logs): **"Skip Thursday doubles MAR: 13.91
(skip-Thu) vs 7.35 (all days)"** · **"Thursday: 50 S2 fires vs 29–36 other days, −$2,452 P/L
(only negative day)"** · global optimum = Actual P/L + 9 re-entries + skip-Thu →
$9,110 / MAR 13.91 / Sharpe 2.87 at 1 contract (~$228K/yr at 25 contracts).
**No day-of-week filter appears anywhere in the v2 folder or on any ON bot.** Adjudicate this.

### NEXT RETRIEVAL TARGETS (raw data, not summaries)
1. **`~/projects/grid-optimizer/results_test37.csv` and `results_test40.csv`** — on the MacBook,
   reachable via a folder grant. **The only raw backtest data located so far.**
2. **Notion — Backtest Registry `917dae3e-6fbf-430e-bdfc-40ee35128993` and Testing Queue
   `b2ba3f05-7d51-426e-82fe-c8e4d093bd50`.** Named as that project's source of truth.
   **NOT QUERYABLE** — the Notion MCP tools available in both that session and this one expose
   only list/search-agents/attachments, **no page fetch and no database query.** Andy must read
   these directly, or a Notion connector with page-fetch must be added. **Likely the trove.**

---

## ⭐⭐⭐ NOTION BACKTEST REGISTRY RETRIEVED 2026-08-10 — QQQ DATA EXISTS. IT ANSWERS DAY 1.

Source: Notion "🏗️ QQQ 0DTE Iron Condor — Command Center" → Backtest Registry, CSV export by Andy.
**35 data rows, 4 of them flagged "Orphaned backtest" duplicates → 31 distinct.** Both exported
files are **byte-identical** (the `_all` view returned the same rows) — a fuller view may exist.

### THE CHAMPION IS A QQQ CONFIG AND IT IS ALREADY VALIDATED
`Fortress (VIX25-Range075-PT50-Wide2)` — 2yr: **$347,091 · PF 3.49 · 97.2% WR · 6 losses ·
DD −$54,923 · $2.00 wide · 1:55 PM · Range075.** 3yr (v1): $444K · PF 3.08 · 96.2% WR · 12L.

### ⭐ STRIKE DISTANCE — THE DAY-1 ANSWER. WIDER STRIKES KILL THE CREDIT.
- `Strikes100` (**1.00% OTM**) — **REJECTED. P/L collapsed to $46,000, PF 1.36.**
  Registry note, verbatim: *"Too wide = not enough credit."*
- `Sym075` (**0.75% symmetric both sides**) — **REJECTED**, PF only 2.70.
  Verbatim: *"Thinner premium not worth wider call distance."*
- `Strikes050` (**0.50% OTM**) — REJECTED, *"fewer trades, similar DD to Fortress."*
→ **The champion's strike distance is TIGHTER than 0.75% OTM, and 0.75% symmetric was
explicitly tested and rejected as too thin.** The GF arms appear to be running exactly the
rejected geometry. **CONFIRM the GF strike-selection config first-hand — still not read.**

### ⭐ THE QUANTITATIVE ARGUMENT THAT SETTLES IT
`QQQ-IC-3PM-Range075-PT50` — **"BUST. 3PM entry kills premium ($0.09 avg). PF drops to 1.95.
Equity went negative."** That is the champion's strike distance at the **worst** entry time,
still collecting **$0.09**. Today the GF arms, at the **best** entry window (1:30–2:00 PM),
collected **$0.02** — **4.5× less premium at a far better hour.** The entry time cannot explain
that gap. **The strikes must be materially wider than the validated config.**

### ⭐ CORRECTION — THE $2 WIDTH IS VINDICATED ON QQQ
Earlier this session I flagged the GF arms' $2 width as suspect, citing SPX Round E
($1.50/$2.50/$3.00 all REJECTED against a $5 baseline). **That was SPX and it does not port.**
On QQQ, **Wide2 = $2.00 IS the champion** (`Fortress`, and `Range075-PT50-Wide2`: lowest DD
−$76K, *"Best for hedging"*, only 3/10 losses at max). **Width is not the problem. Strikes are.**

### ENTRY TIME ON QQQ — THE VALIDATED HOUR IS 1:55 PM, NOT 1:30
`1:30 PM Wide2 (la1)`, 3yr: $541K, PF 2.88, DD −$105K — *"22% more profit but 2x drawdown vs
1:55 PM. Higher risk/reward, **not strictly better**."* The GF window (1:30–2:00 PM) straddles
both. Worth deciding deliberately rather than by accident.

### ⛔ THE NOTION COMMAND CENTER IS STALE — DO NOT TREAT IT AS CURRENT TRUTH
Its "non-negotiable" Daily Trading Rules say **"Exit: PT50 auto-close is mandatory and
non-negotiable"** and its champion line reads **"Range075 · PT50 · $2 Wide."**
**v2 dropped PT50** (champion is `IC-SPX-FastPT25-S2`; PR-04 is literally `Fortress-NoPT50`).
The registry's own OO runs explain why v2 is right:
- `Run23` (S2+Range075+PT50): $1,955 vs `Run22` (S2+Range075, no PT) $3,755 —
  *"**KEY FINDING: S2 and PT50 are in conflict. Cannot stack both and get full benefit of either.**"*
- `Run24` (baseline, Range075, NoPT): *"**Without PT50, baseline P/L jumps from $499 to $3,291 —
  PT50 was destroying $2,800 of value on the filtered dataset.**"*
**v2 supersedes Notion on PT50. Record it so no future session "restores" PT50 from Notion.**

### OTHER CONFIRMATIONS
- **S2 is the tournament winner** — `Run19` $7,583 vs do-nothing `Run17` $499, **15× P/L on the
  same 84 losses**, 964 trades. Validates the S2 monitor now running live on PR-01/PR-02.
- **VIX filter redundant** — *"Range075 does the work alone. VIX only caught 7 extra days over
  3 years."* (though on 2yr, VIX25-Range075-PT50 was best overall at PF 4.58).
- **Stops are counterproductive**: Stop100 → 116 losses; Stop200 best-of-stops; VIX25-Stop200
  *"adds 27 false exits… costs $273K. Stop is redundant when VIX filter is active."*

### ⚠️ REGISTRY DATA-QUALITY DEFECTS (fix in Notion)
1. **4 orphaned duplicate rows** (Strikes050/Strikes100/AsymWide/BearAsym each appear twice with
   identical figures). Any count of "backtests complete" is inflated by 4.
2. **`QQQ-IC-3PM-Range075-PT50` has `Entry Time = 1:55 PM`** — wrong; it is the 3PM variant.
   Corrupts any query grouped by entry time.
3. Several rows have blank `Total Trades`, and every OO row has blank `Profit Factor` / `Max
   Drawdown` — so PF is not comparable across the QQQ and OO cohorts.

### TOOLING — WHY THE CSV WAS NEEDED
The Notion MCP integration available in this session and in the other project is **write/list
only**: `list-private-pages`, `list-shared-pages`, `list-recent-pages`, `search-agents`,
`create-attachment`, `create-folder`, `convert-page-to-skill`. **No page fetch, no database
query, no content search.** WebFetch fails on authenticated `app.notion.com`. Page *text* is
reachable via Claude-in-Chrome `get_page_text` (cheap — no screenshots); **database rows are
not**. **ACTION: add a Notion connector with read/fetch + database-query scope.**
Other databases on the Command Center, still unread: **Testing Queue · Losing Trades (39
analyzed) · Hedge Strategies (7) · Paper Bots · Key Decisions · Daily Trade Log.**

---

## ⭐⭐⭐⭐ KEY DECISIONS DB RETRIEVED 2026-08-10 — TWO RETRACTIONS AND ONE ARCHITECTURE CONFLICT
Source: Notion "⚡ Key Decisions" CSV (41 decisions, Feb 2025 → Jun 2026). Both exports identical.

### ⛔ RETRACTION 1 — PR-01's MISSING CALL SIDE WAS ROOT-CAUSED ON 2026-06-07. NOT A FINDING.
Decision **"5/15 SPX-Fortress call-only is correct behavior, not a bug (put-credit skew)"**
(🟢 High, 2026-06-07), verbatim: *"put/call skew compressed the 0.75%-OTM put-spread credit
below OA's minimum sellable mid; the put order was rejected at placement (**'Filtered: Mid price
is $0.05'/$0.07**), so the bot correctly opened only the call side… Three prior hypotheses
disproven… The 1:34 second call = **Fortress-Mon-S2-Cleanup** closing the 1:31 call then the
scanner re-opening."*
Rule created: *"**Single-sided opens caused by sub-minimum credit (one leg's mid < OA's $0.05
floor) are documented behavior, not failures. Flag such days; do NOT count them as clean IC
data points.**"*
→ Today's PR-01 (call side filtered at **mid $0.05**, put side opened, `Scalp-Mon-S2-Cleanup`
closing it) is **the same documented condition, message string for message string.** I escalated
it as the highest-priority unknown. It was closed two months ago. **ACTION: apply the rule —
flag 2026-08-10 PR-01 as a NON-CLEAN IC data point in the ledger.**

### ⛔ RETRACTION 2 — 0.75% SYMMETRIC STRIKES ARE CORRECT. MY DAY-1 HYPOTHESIS IS DEAD.
**"Symmetric 0.75%/0.75% strikes are correct"** (🟢 High): *"Asymmetric (0.75%/0.50%) produces
74% WR with 107 losses — garbage. Use symmetric."* And **"Fortress confirmed champion"**
(🟢 High, 2026-03-15): *"Range075 = Goldilocks. **0.75% symmetric = optimal.** $2 wide = perfect
balance."*
→ Earlier tonight I read the registry's `Sym075` rejection row as proof the champion runs
**tighter** than 0.75%. **Wrong.** That row is a **$1.25-wide** variant; Fortress is **$2 wide**
at 0.75% symmetric. **Strikes are right. Width is right. Entry window is right.**
**The GF arms are NOT misconfigured on any parameter I can point to.**

### SO WHAT DID HAPPEN TODAY: the sub-$0.05 floor, on BOTH sides, all window
Today's GF mid was **$0.02** — below the bot's $0.08 criterion **and** below **OA's own $0.05
minimum sellable mid**. Under the 2026-06-07 rule this is **documented no-trade behavior, not a
defect.** But note what it implies: **on the ideal IC day (QQQ < ±0.75%), QQQ 0.75%-OTM $2-wide
paid sub-floor credit at the best hour.** Compare `QQQ-IC-3PM` — the *worst* hour at the same
geometry still averaged **$0.09**. That gap is a **regime** signal, not a config signal.
Cross-reference the ORB decision's regime note: *"2025 half-year sample shows full-assignment
rate doubled and per-trade expectancy down 3–4x vs 2023–2024."*

### ⛔⛔ THE ARCHITECTURE CONFLICT — QQQ WAS RETIRED AS A TARGET IN MAY, THEN REBUILT IN AUGUST
- **"Defer QQQ-IC selector workaround"** (🟢 High, 2026-04-28): *"Zack (OA support) confirmed
  2026-04-28 that the **QQQ call-side strike-resolution failure is structural (~13.3% of trading
  days)**."* Three workarounds proposed; **none adopted.**
- **"Build SPX-Fortress-Baseline + SPX-Fortress-Defang"** (🟢 High, 2026-05-13), rule created:
  *"**All new hedge variant bots go on SPX (production target) not QQQ. SPX has uniform $5
  strikes (no strike-resolution bug), 60/40 tax treatment**…"*
→ **The v2 greenfield family — built 2026-08-09 — is SEVEN QQQ ARMS.** That is directly against
a 🟢 High architecture decision three months old, on an underlying with an unfixed structural
strike bug affecting ~13.3% of days. **NOT a Cowork call. Andy must rule: port the GF family to
SPX, or formally supersede the 2026-05-13 decision.** Nothing touched.

### CONFIRMATIONS (no action, just closure)
- **S2 is validated**: *"S2 confirmed as hedge winner… zero false positives on 671 trades."*
- **Range075 is a gap/change-%-since-previous-close filter, NOT intraday range** (2026-05-13) —
  matches what the GF logs showed today. Externally validated by Sandvand (9,100 trades).
- **Time gates are mandatory**: *"Any IC scanner that relies on an intraday filter MUST gate
  entry time so the filter sees the developed move."* GF arms have 1:30/2:00 gates ✓.
- **Side-gating rule** (Open Position on the NO path of the tag check) — **GF arms and PR-01
  both observed COMPLIANT today.** ✓
- **Daily Positions safeguard must be ≥2 for IC bots** (OA models each spread as a position).
  GF arms are 2/2 ✓. **Verify, do not edit.**

### ⚠️ THE KEY DECISIONS DB HAS NO SUPERSESSION FIELD — CONTRADICTORY 🟢 HIGH ROWS COEXIST
- *"PT50 is optimal exit — mandatory and non-negotiable"* (🟢 High) vs **"PT50 DROPPED from
  Fortress"** (🟢 High, 2026-04-08). Both live, no marker.
- *"VIX < 25 filter is REDUNDANT"* (🟢 High) vs **"VIX filter is strike-distance-dependent, NOT
  universally redundant"** (🟢 High, 2026-03-16 — *"Wide strikes (1.0%): VIX critical, removing
  collapses PF 3.7→1.36"*). Both live.
- Several 2026 backtests are dated **2025** (rows dated Feb/Mar 2025 cite Mar-2026 registry runs).
**A future session reading this DB cold will act on a superseded rule.** Add a Superseded-By
relation. Until then: **v2 folder > Notion on any conflict.**

### ⭐ RECOMMENDED BOT EDITS FOR 2026-08-11: **NONE.**
Every parameter is validated; today's non-entry is documented behavior; this week is
investigation + cleanup by Andy's own call; n=3. Changing a signed config forks it and voids the
A/B. **The only action is a LEDGER action: flag 2026-08-10 PR-01 as non-clean IC data.**

---

## 📥 NEW — TWO RESEARCH DOCS DROPPED IN `docs/` 2026-08-10. REVIEW AFTER THURSDAY RESET.
Andy added these late on Day 1. **NOT read, NOT summarised, NOT acted on** — flagged only.
- **`docs/AI Agent Stack.md`**
- **`docs/AI Agentic.pdf`**

Stated subject: research + **suggestions for agentic workflows**.

**Review task (Thursday or later — deliberately NOT this week):**
1. Read both in full and summarise into a single dated note in `docs/`.
2. Judge each suggestion against the **existing** contract before adopting anything:
   `docs/daily-loop-spec.md` (the loop is a data-collection ritual; the fixed panel never
   changes; NO FINDINGS is the goal), `CLAUDE.md` §5 (pre-register before restart; doc-edit
   authority), §7 (Cowork vs Claude Code lanes), `docs/evidence-standards.md`.
3. **Anything that would change the fixed panel, a detector rule or a threshold is GATED** —
   `daily-loop-spec.md` §0: *"Change one and the accumulated ledger becomes uncomparable —
   which silently destroys every day already banked. Version and re-baseline instead."*
   The ledger is now **live at n=3**; it is no longer free to re-baseline.
4. Cross-check against Key Decisions **"OO + OA dual-platform stack"** and **"Tradier API =
   Phase 3, not Phase 1"** before any new tooling is proposed — the platform lanes are already
   ruled, and agentic-workflow proposals are a common way to re-litigate them by accident.

**Sequencing note:** these land BEHIND the four already-agreed Thursday items (GF strike-config
read → `bots_config_v2.csv` schema → Tradier re-sync + render the real brief → backtests).
Do not let a new-tooling doc displace the config fix that is currently blocking §3 of the brief.

---

## PR-02 "FastPT25" NAME QUESTION — CLOSED. NO DEFECT. (Andy asked 2026-08-10 evening.)
**`build-plan.md:100`, verbatim:** *"**ride + S2**… **No new exit architecture. It is a control.
PT25 removed from the Open Position action explicitly — not left dead behind an off toggle.**
Do NOT touch Cleanup itself — S2 depends on it."* `:101` — `-130PM` = *"Identical, 1:30 PM entry.
The entry-time A/B partner. Same Exit-Option-free spec."*
→ **The absence of PT25 is DELIBERATE, DOCUMENTED AND EXPLICIT.** The name is legacy, inherited
from the archived original. **Do not "fix" it. Do not rename it** (the name is load-bearing in
`pre-registration-ledger.md`, `bots_config_v2.csv` and every capture filename).
⛔ **Earlier this evening I offered "unimplemented spec" as a live hypothesis, citing the 5/13
Scalp 11 AM precedent. That was wrong — the answer was in `build-plan.md` the whole time.**

### ⭐ VERIFICATION PARTIALLY DISCHARGED FROM TODAY'S DATA (pre-reg PR-02, VERIFICATION block)
Requirement: *"INVERTED… PLUS: the first five entries' timestamps land in the declared window."*
- **Entry 1 of 5: 2026-08-10 13:31:00 / 13:31:02 vs a declared 1:30 PM window — LANDS. ✓**
- INVERTED Step-6: **NO PT row ✓** and **NO exit-trigger row ✓** (both legs ran to 16:15 expiry,
  status `expired`, +$200 put / +$400 call). **Third clause — "S2 monitor observed firing" — NOT
  yet checked on PR-02** (its Log tab was never opened; only the Settings automation list was).
- **4 more entry timestamps owed. FIRST-TRADING-DAY CAPTURE still owed for 2026-08-10.**

---

# ADDED 2026-08-11 (DAY 2) — fold into the artifact Thursday

## ⭐ DECISION DUE TOMORROW (08-12) — GF strike selection
**Cause established:** PR-01/GF use `legpctprice pct=0.75`; PR-02 uses `delta 0.1`. Wings, price,
sizing and filter are byte-identical between PR-01 and PR-02 — **the selection method is the only
differing field.** See `docs/session-log.md` 08-11.
**Prior art REVERSES the framing:** `docs/ic-trailing-stop-backtest.md:42` — *"0.75% OTM short
strikes (NOT the −10Δ the 130PM clone uses — match the champion)"*. **0.75% is the deliberate
champion spec; PR-02 is the documented deviation.** Not a bug — the spec aged out of its regime.
**Evidence — credit at ≥0.70% OTM, SPX 0DTE, by month:** Apr 0.320 (n=146) · May 0.291 (179) ·
Jun 0.343 (72) · **Jul 0.153 (20) · Aug 0.125 (2)** — ~60% collapse since June.
**Evidence AGAINST copying 0.10Δ — avg R by OTM band:**
| band | n | avg mid | avg R |
|---|--:|--:|--:|
| 0.20–0.35% (≈0.10Δ) | 30 | 1.435 | **−0.145** |
| 0.35–0.50% | 38 | 0.729 | **+0.003** |
| 0.50–0.75% | 266 | 0.348 | −0.007 |
| ≥0.75% (current) | 194 | 0.274 | −0.005 |
The −0.145 is NOT one bad day: 14 distinct days, 6 green / 8 red, **two full −1.0R days** (05-07,
05-21) plus −0.80 and −0.58. `docs/hedge-research.md:125` independently: the 0.75% strike is
**already touched ~40% of legs**, and the lever is **wider**, not closer.
**CAVEAT:** the bands mix ORB/DIR bots with the ICs, and ≥0.75% is contaminated by higher-vol
months. Direction is consistent; precision is not there. PR-02's 2/2 is **n=2 in a quiet drift
market** — not evidence its zone is safe.
**RECOMMENDATION:**
- **TOMORROW — Option B: keep `legpctprice`, 0.75% → ~0.40%.** One number, same field. Only band
  with non-negative avg R; ~2× current credit; still wider than PR-02. **Preserves method-
  comparability with the champion** — GF exists to test EXITS, and switching entry method would
  confound every exit result against PR-01. 0.40% is INTERPOLATED from n=38, not derived.
- **QUEUE — Option A: `delta` 0.05–0.07.** The permanent structural fix for vol-blindness. Do NOT
  ship on n=2 from PR-02; that is the inference the T-levels forbid.
- **SCOPE: 2 edits.** `GF-ScannerA-PutSpread` + `GF-ScannerB-CallSpread` are SHARED across all 7 arms.
- **HOLD PR-01** (signed control; changing entry mid-stream destroys the only clean read on
  `Scalp-Mon-S2-Cleanup`). **HOLD PR-04 and sign it first** — unsigned, **$100,000**.

## ANDY'S RULINGS 2026-08-11 (6/6) — all recorded in session-log
1. **PR-02 + PR-04 STAY ON** while unsigned — knowing exception to §5. ⇒ needs an unsigned-bot
   banner in `scripts/report.py` (STATUS.md is machine-generated, no hand edits). — **done**
   2026-08-17: `report.py:436` (markdown) + dashboard line 1086. Built PR #12 `ed53b53`,
   hardened #16 `108da28`; records corrected in `78b3195`.
2. GF/PR-04 QQQ log read AUTHORIZED — **done**, cause established.
3. **Split (ii) join key = `oa_id`**, not bot name.
4. **Store `pt_pct` only**, format for the brief.
5. **Add `exits_enabled`** (0/1 from `disableExits`); gates Exit-Options-side rules ONLY —
   `event_backstop` NOT gated.
6. **`none` requires a capture.** PR-04's lands now; **PR-01 stays BLANK** until Day-0 Layer-2.
7. **SIGN PR-02** (Andy, 08-11).
8. **Close the 08-09 switch-on gap** with one line in `docs/state.md` (Andy's wording).
9. **Accept the 10-of-17 coverage gap, but make `daily_brief` SAY SO** — "10 of 17 graded, 7
   uncaptured by design". Silence reads as coverage.

## BUILD QUEUE (not started)
- **Split (ii):** new `data/bots_mechanics_v2.csv` + 2 loader changes. Ends the CONFIG-BLIND state
  (`daily_brief` 0 ON bots graded; `execution_audit` 9 rules SKIPPED, 2 days running).
- `scripts/cw_git.sh` — mv-sweep wrapper. `device_bash` cannot unlink; locks recur every session.
- Width-relative floor (express `minPrice` as a fraction of spread width). **QUEUED, not now** —
  changing it alongside strike selection destroys attribution.
- `SILENT_BOT` blind spots: no-history bots invisible; open-but-unclosed false-flagged.
- `lessons.py` truncation — GATED on archiving 33 v1 rows to `data/archive/lessons-v1.csv`.

## CAPTURE-DISCIPLINE NOTE (worth a line in evidence-standards)
GF's strike rule was **fully captured 2026-08-06 and sat unread for five days.** PR-01's capture
said *"everything else in the action, read and recorded as unchanged"* **and did not record it** —
which is why establishing cause needed a browser read. **"Unchanged" is not a recorded value.**

## ANDY'S HAND
3 OA archives (verify by ID + footer 43→40) · untracked `_to_delete/`, `docs/AI Agent Stack.md`,
`docs/AI Agentic.pdf` · `docs/state.md` Day-2 reframe.
