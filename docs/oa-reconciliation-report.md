# OA reconciliation report — Phase 6

*Written 2026-08-04 by the Phase 6 session. This is the judgment pass the extraction waves were
deliberately blind to: every platform claim in the six OA judgment docs, checked against the
ground-truth fact ledger.*

## 0. Method and provenance

- **Corpus:** `data/oa_facts.csv` — 1,548 facts (OA-0001–OA-1548; 1,401 DOCUMENTED + 147
  DOCS-SILENT) from 100/100 pages of `docs.optionalpha.com`, extracted Waves 1–4.
  sha256 `435abe0d…3527b`, verified this session by direct `device_bash` read (not stage-back).
- **Docs audited** (sha256 device-vs-staged verified byte-identical this session):
  `oa-platform-reference.md` · `oa-ops-runbook.md` · `pilot-clone-card-qqq-fortress.md` ·
  `reactivation-runbook.md` · `hedge-research.md` · `oa-mirror-reference.md` (§8 platform claims).
- **Verdicts.** **CONTRADICTED** = a DOCUMENTED fact opposes the claim as stated.
  **UNSOURCED** = no fact in the corpus speaks to it (a DOCS-SILENT row counts as silence, per the
  handoff rule: a plausible project assumption does not pass as CONFIRMED merely because nothing
  contradicts it). **CONFIRMED** = a DOCUMENTED fact supports the claim as stated.
  UNSOURCED does **not** mean false — under `oa-platform-reference.md` §0.2 a first-hand
  observation can still carry a claim; it means *the docs cannot* carry it. Each finding states
  its basis.
- **Ordering:** CONTRADICTED first. Within each section, claims in **step-by-step-executed docs**
  (pilot card — executed 2026-08-03; reactivation runbook §§2–3 — partially executed;
  ops runbook — operational) rank above claims in merely-read docs (platform reference,
  hedge research, mirror reference).
- The unresolved Wave-1 fingerprint mismatch on `data-feeds` and `autotrading-best-practices` is
  **informational, not blocking** — every sampled quote from both pages is still an exact
  substring of a fresh fetch; their facts are cited here normally.

---

## 1. CONTRADICTED

### R-01 ⛔ The per-bot `EXIT OPTIONS` toggle IS documented — "absent from OA's documentation" is false
**Where:** `oa-ops-runbook.md` §1.6 (*"a single-source claim — one OA support rep, absent from
OA's documentation entirely"*) · `oa-platform-reference.md` §10 (*"It still appears nowhere in
OA's documentation — a full sweep returns nothing"*) · echoed in `pilot-clone-card` Step 9's
framing of the evidence set.
**Facts:** **OA-0871** — *"Exit Options always run, even if your automations inside a bot are
turned off… **unless you turn off Exit Options in your bot**"*; **OA-0896** — *"you can
enable and disable Exit Options from **the main Bots page, inside of the bot**… or individually
within each position"* (`tools/managing-positions/exit-options`).
**Verdict:** the toggle's **existence** is CONTRADICTED as undocumented — it is **[DOCUMENTED]**,
at bot level, with three documented control surfaces. The prior sweep missed it.
**What this does NOT change:** the **causal** lapse claim (resubscription restores only
`AUTOMATIONS`) stays UNSOURCED (R-10) and the Day-0 Trades-list gate stays mandatory. What it
does change: the toggle is no longer single-source, and §10's "docs gap" framing, §1.6's
"single-source" warning, and the Step 9 parenthetical should be corrected when edits are
authorized.

### R-02 ⛔ "Clones share automations by reference" — still asserted in three operational docs; unsupported by the corpus and falsified first-hand
**Where:** `pilot-clone-card` Step 2 (executed doc — the trap box and the fork procedure) ·
`reactivation-runbook.md` §2 step 2 · `oa-ops-runbook.md` §5 Trap 1 · `oa-ops-runbook.md` §3
(cohort blast-radius warning).
**Facts:** no fact states clones share automations by reference. The corpus says sharing is a
**Library** feature: **OA-0681** (automations can be shared across bots), **OA-0682** (edits to a
*shared* automation flow through), **OA-0683** (Copy forks without impacting the original),
**OA-0845** (a clone arrives *"complete with all the settings and strategies of the original
bot"* — nothing about references).
**Basis:** UNSOURCED in the corpus **and falsified by the 2026-08-03 direct test** (already
banner-marked in `oa-platform-reference.md` §2; per `state.md` the three docs above are still
unamended). Ranked here rather than in §2 because three step-by-step docs still instruct a fork
ritual on a false premise — Step 2 is a documented no-op pending Andy's authorization to edit.

### R-03 ⛔ The SmartPricing table's "[PROJECT-RULE, not doc-verified]" tag is wrong — the docs state every cell
**Where:** `oa-platform-reference.md` §7 (*"These mode names, price counts and timings come from
project files. The docs do not state them."*).
**Facts:** **OA-0785** (Normal: up to 4 prices, 10s each) · **OA-0786** (Fast: up to 3, 5s) ·
**OA-0787** (Patient: up to 5, 20s) · **OA-0784** (plus Off = single limit order, and Market)
— all on `tools/bots/smartpricing`.
**Verdict:** the table itself is CONFIRMED (docs + the 2026-08-03 first-hand read agree, cell for
cell); the *tag* is CONTRADICTED. Promote to **[DOCUMENTED + FIRST-HAND]** — the strongest tier
any claim in the file holds. (The `speedy` internal-value caveat remains first-hand only.)

### R-04 ⛔ Mid-price evaluation IS documented — §6.4's residual [PROJECT-RULE] half is wrong
**Where:** `oa-platform-reference.md` §6.4 contested-banner residue: *"The mid-price half remains
unquoted; it is only implied"* … *"Leave that half as [PROJECT-RULE] until it can be quoted
directly"*
**Facts:** **OA-0872** — *"Exit Options use a position's mid-price when evaluating returns"*
(`tools/managing-positions/exit-options`).
**Verdict:** CONTRADICTED — the docs state it directly. Both halves of §6.4 (2-minute lifetime,
mid-price evaluation) are now [DOCUMENTED].

### R-05 ⛔ The percentage-allocation-shrinking claim IS sourced — the 2026-08-04 [UNVERIFIED] flag is overturned
**Where:** `oa-platform-reference.md` §3 (*"not on the safeguards page and carries no source
anywhere in this file… Treat as unsourced"*; also `state.md` Tier-1 list: *"sizing must not rest
on it"*).
**Facts:** **OA-0083** — with percentage allocation >50%, a subsequent position's contract amount
*is intentionally reduced* to avoid allocating more than 100% of bot capital
(`technical-documentation/platform/automation-behavior`).
**Verdict:** the claim is CONFIRMED [DOCUMENTED]; the audit flag looked on the wrong page. Sizing
may rest on it again — as documented behavior, not folklore.

### R-06 ⛔ The Exit Options operating window is a docs-internal CONFLICT, not a single documented fact
**Where:** `oa-platform-reference.md` §6 (*"Operating window: 9:31 am ET until 1 minute before
the market close [DOCUMENTED]"*) and the §4.2 "three windows" append.
**Facts:** **OA-0870** — 9:31 am ET until 1 minute before close, customizable in Settings
(`exit-options` page) — vs **OA-0085** — user-defined parameters are *"checked every one market minute
between 9:40 AM and 3:59 PM Eastern"* (`automation-behavior` page).
**Verdict:** the end (~15:59) agrees; the **start** is 9:31 on one page and 9:40 on another.
Retag the window **[CONFLICT]** on the start time and carry both quotes. The §4.2 "three
windows" note gains a fourth number. No project design currently depends on the start minute —
but the file's claim of a single documented window is contradicted by the corpus.

### R-07 ⛔ Clone completeness — the docs affirmatively claim what the product contradicts
**Where:** `oa-platform-reference.md` §2 (*"Three clone traps that ARE real and appear in NO
document"*) · pilot card Step 3's trap framing (symbols).
**Facts:** **OA-0845** — cloning adds the clone *"complete with all the settings and strategies
of the original bot"* (`tools/clone-bot-templates`). Corroborating doc-side hint that clone drift is
real: **OA-0721** — users are told to confirm Automation/Bot Input values after upgrading or
cloning a bot.
**Verdict:** the traps themselves stand [FIRST-HAND — allocation→$1000, Group→None, Tags→empty,
2026-08-03], and per §0.2 the screenshot beats the doc. But "appear in NO document" understates
it: **the docs address cloning and get it wrong** — OA-0845 is a documented claim contradicted by
observation. Record it as a docs-defect, which is stronger ammunition than silence.

### R-08 ⛔ `oa-mirror-reference.md` §8: "0DTE Oracle — SPX/XSP only" is contradicted by current docs
**Facts:** **OA-1177** (SPX widths $5–$25) · **OA-1178** (**SPY, XSP, QQQ** widths $0.50–$5) ·
**OA-1187** (whether anything *beyond* those four is supported is unstated).
**Verdict:** CONTRADICTED — the Oracle covers at least SPX, SPY, XSP, QQQ in the current docs.
(Likely platform expansion since the April 2026 capture; either way the doc's claim no longer
holds.) Same section's "risk-defined strategies only" and "refreshes every minute": UNSOURCED for
the Oracle specifically (R-19).

### R-09 ⛔ `oa-mirror-reference.md` §8: OA's "2-hours-to-expiry force-close" does not exist in the corpus — the documented protocol is materially different and more dangerous
**Where:** §8 leaderboard quirks (*"2-hours-to-expiry force-close behavior is a real edge case
bots guard against (Nigiri's 0-Day ITM Check)"*).
**Facts:** the documented expiration protocol is: last moneyness check **10 minutes before
close** (**OA-0238**); handling per a **Settings** choice of three options (**OA-0233**); and the
**default is "calculate estimated P/L from underlying close price" — the bot sends NO closing
order** (**OA-0157, OA-0231**). OTM positions are never closed (**OA-0236**).
**Verdict:** CONTRADICTED as stated — no 2-hour force-close exists anywhere in the corpus, and
the actual default is the opposite of a force-close. See R-22, because this documented default is
absent from every v2 judgment doc and it matters for the fleet.

---

## 2. UNSOURCED

### R-10 ⚠️ The lapse mechanism itself — "deactivation turns both toggles off; resubscription restores only AUTOMATIONS"
**Where:** `reactivation-runbook.md` §1 (executed-adjacent — it scripts Day-0 Step 3) ·
`docs/state.md` Account section.
**Corpus:** zero facts on subscription lapse, billing state, or what deactivation/reactivation
does to bots or toggles. (The corpus's only adjacent row is **OA-0423**, a DOCS-SILENT question
about *broker authorization* lapses.)
**Verdict:** UNSOURCED — remains exactly what the runbook already says it is: one support rep,
unverified, with the Day-0 Trades-list check as the only real test. The toggle's *existence* is
now documented (R-01); its *causal role in the lapse* is not. The runbook's own caveat is
correct and must survive any edit.

### R-11 ⚠️ Daily/Total position limits above 10 — the docs never say they can be raised
**Where:** `oa-platform-reference.md` §3 (*"Defaults allow 10 daily / 10 total, both editable"*,
and the IC box: *"Ten re-entries of a single IC is a daily limit of 20"*) · downstream:
`build-plan.md` §2B re-entry sizing.
**Facts:** **OA-0763** (bots allow ten daily / ten total) · **OA-0762/OA-0320** (limits can be
"manually selected and modified" / "safeguards edited") · **OA-0764** — DOCS-SILENT on whether
10 is a ceiling or a default.
**Verdict:** "editable" is CONFIRMED; **editable-above-10 is UNSOURCED**. The pilot clone
(2/2) is unaffected; ~~any 10-re-entry spec (daily limit 20) rests on an unverified assumption.
**One-click UI check: open the safeguard input and type 20.** Add to the §9 open-checks table.~~

> ### ⛔ CORRECTED 2026-08-05 — the check was run, and it came back NO. Limits **cannot** exceed 10.
> *Struck text left standing above per this file's convention. Correction only — the R-11 verdict
> on the DOCS ("editable-above-10 is UNSOURCED") is unchanged and still correct; what changes is
> that the product question behind it is no longer open.*
>
> **[FIRST-HAND 2026-08-04 — Bot Safeguards panel read on `QQQ-IC-0DTE-Fortress Clone`.]**
> `posLimitDay` (Daily Positions) and `posLimit` (Position Limit) are **hidden inputs behind
> pickers offering `1` … `10` only** — not number fields. There is no `max` attribute to read and
> **no free-text path to type `20` into**, so the one-click check proposed above is not
> performable as written; the picker itself is the answer. (`seed` read `type=number
> min="250" max="100000"`; Day Trading is a two-item picker.) Re-read identical after a hard
> reload; nothing was saved.
>
> ⛔ **Consequence — this is ruling D-2's basis.** An IC is **2 positions**, so a daily cap of 10
> positions is a real ceiling of **5 ICs/day per bot**, not ten. *"Ten re-entries of a single IC
> is a daily limit of 20"* is arithmetically correct and **unconfigurable**. **D-2 ruled
> 2026-08-04: cap at 5 ICs/day, ONE bot** — do not split a strategy across two bots to reach ten.
> **Any spec assuming a daily re-entry limit above 10, or a 20/day IC ceiling, must be
> re-scoped to 5 ICs/day.** The downstream surface this row names — `build-plan.md` §2B re-entry
> sizing — was checked on the device 2026-08-05 and **states no re-entry count**, so nothing is
> carried there.

### R-12 ⚠️ Touch semantics are blog-sourced — outside the docs corpus
**Where:** `oa-platform-reference.md` §6.2 ✅ RESOLVED block · `hedge-research.md` §7.2 ·
tournament architecture (`build-plan.md` §2D "Touch $0").
**Facts:** the corpus only *names* Touch as a trigger (**OA-0875**; and the six-vs-eight count
defect, **OA-0874**). What Touch references — underlying vs position price — appears nowhere in
the 100 docs pages; the §6.2 resolution cites `optionalpha.com/blog/new-exit-option-for-itm-price-touches`.
**Verdict:** UNSOURCED **relative to this corpus**; the blog citation stands on its own and the
resolution is not weakened — but a `oa_facts.csv` fact_id cannot be attached to it, and the §8.3
proof-of-fire check is the real gate. Do not silently upgrade the blog to "the docs".

### R-13 ⚠️ `Profit Taking $ / Stop Loss $` (June 2026) and `Avoid Events` — not in the docs corpus
**Where:** `oa-platform-reference.md` §6.1 (*"Also available: Profit Taking $ / Stop Loss $…
and Avoid Events"*) · `hedge-research.md` §2.1 (*"Dollar-anchored stops are now runnable"*) and
§9 item 6 (fixed-$ SL variants).
**Facts:** the exit-options page's trigger list (**OA-0875**) contains no $-variants and no
Avoid Events; nothing else in the corpus does either.
**Verdict:** UNSOURCED — release-notes-sourced, docs lag plausible. Before the backtest sweep's
fixed-$ rungs are pre-registered, verify the $-controls exist in the product UI and record where.

### R-14 ⚠️ *"Connecting one makes the platform free"* (`oa-platform-reference.md` §1)
No pricing/subscription facts exist in the corpus. UNSOURCED; harmless, but it is a marketing
claim, not a docs claim.

### R-15 ⚠️ IC = 2 positions — correctly tagged [PROJECT-RULE]; the corpus is silent, as the tag says
**Where:** `oa-platform-reference.md` §3 · ops-runbook §5 Trap 5 · pilot card Step 4.
No fact addresses how OA models a condor across positions. The tag is honest; nothing to fix.
Noted because it is load-bearing everywhere and Phase 6's instruction is to say out loud which
load-bearing rules the docs do not carry: this one, the Trades-list rule (R-16), and the
Exit-Options-panel rule all rest on project evidence, and their in-file tags already say so.

### R-16 ⚠️ "The Trades list is the only order-level ground truth" — the docs never draw the panel-vs-record distinction
**Where:** `oa-platform-reference.md` §0.3 · ops-runbook §4.2 · pilot card FINISH · runbook §4
Step 6 — the project's most load-bearing rule.
**Facts:** **OA-0894/OA-0895** CONFIRM the documented half (Exit Options are shared at entry,
then become per-position and independently editable). **OA-0899** (DOCS-SILENT) — the docs never
state that the panel is intent rather than execution record; every outcome statement is hedged
with "no guarantee" (**OA-0881**).
**Verdict:** the rule's premise is documented; the rule itself is a project inference the docs
support but never state. Correctly framed in-file. Keep the tags as they are; cite OA-0894/0895
+ OA-0899 when the rule needs defending.

### R-17 ⚠️ Ops-runbook first-hand operational claims — corpus silent, as expected
Export Data mechanics (§1.7: 26 columns, `botName` first, native MFE/MAE, works while lapsed,
group-filter subset trap), template versioning (§2: VERSION counter — and §2's *"the OA docs
describe no versioning at all"* is CONFIRMED-silent: OA-0843–OA-0859 describe cloning/templates
with no versioning), bookmarklet coverage (§1.5), toggle screenshots (§1.6). All UNSOURCED in
the corpus and all carried by capture evidence; no conflict found. The one *documented* addition:
**OA-0847** — any bot can be saved as a template stored indefinitely; **OA-1025** — no limit on
saved templates.

### R-18 ⚠️ The outage claim — "OA outage = no execution and no broker-side protection"
**Where:** `oa-platform-reference.md` §12.
**Facts:** infrastructure facts (**OA-0028–OA-0032**) describe OAuth delegation and that bots are
not constantly connected to brokers and track positions via OA's own feed (**OA-0032**, also
**OA-0124/OA-0247**) — which *supports* the architecture of the claim (no resting orders at the
broker: **OA-0865**, Exit-Option orders are only sent when criteria are met) but never addresses
outages. Verdict: UNSOURCED as stated, though OA-0865 is the strongest documented support for the
"no broker-side protection without a bracket" design concern.

### R-19 ⚠️ `oa-mirror-reference.md` §8 product observations
the Oracle *"refreshes every minute"* · risk-defined-strategies-only for the Oracle · "Min Trades filter maxes at 10" · "leaderboard cannot
distinguish autonomous bots from manual-hybrid tools". All UNSOURCED in the corpus (the last two
are leaderboard-UI observations the docs don't cover; **OA-0858** is DOCS-SILENT even on the
leaderboard's ranking metric). The Oracle *is* documented to scan ATM→3% OTM in 0.1% steps
(**OA-1176**) over 9:31–15:55 (**OA-1179**), with custom backtests to 3 years of minute data
(**OA-1172**) — none of which was in the mirror doc. Note: `oa-mirror-reference.md` is
archive-era context; no edits proposed, but do not cite its §8 as current platform truth.

### R-20 ⚠️ Option Omega claims (`hedge-research.md` §13)
Out of scope for this corpus (OA docs only). The OA-side claims in `hedge-research.md` all
reconcile: the §7 automation-behavior quote is exact (**OA-0094**), "1-minute at best" is
CONFIRMED (**OA-0092/OA-0867**), the tag-ladder primitives are CONFIRMED (**OA-0820/OA-0821** —
with tag-count limits DOCS-SILENT, **OA-0822**), and the Bid-Ask-Guard failure mode is CONFIRMED
(**OA-0891**). The OO inventory needs its own trial-test, as §13 already says.

---

## 3. CONFIRMED — the load-bearing claims that check out

The v2 rewrite is substantially accurate against the full corpus. Verified, by section of
`oa-platform-reference.md` (shared claims in the runbooks/card confirm with it):

| Claim | Facts |
|---|---|
| §0.1 no memory between scans; Smart Stops the exception (every-minute gain/high-gain checks) | OA-0094 |
| §0.3 Exit Options copied per-position at open, then independent | OA-0894, OA-0895 |
| §1 paper/live binding fixed at creation; convert = clone + change account | OA-0917, OA-0921, OA-0922 |
| §1 paper fills simulated at/near mid; PT/SL fill divergence is the top live-vs-paper gap | OA-0930, OA-0932, OA-0258 |
| §2 Library sharing: edits to shared automations propagate; Copy forks safely | OA-0681, OA-0682, OA-0683 |
| §3 allocation computed at entry; close-side risk can exceed it (wide spreads) | OA-0168, OA-0169, OA-0751, OA-0754–0756 |
| §3 limits: 10/10, trip turns scanners off, allocation limit trips too, warning displayed (Position statement + Bot Log), no closing limit | OA-0763, OA-0769, OA-0770, OA-0767, OA-0320 |
| §4 Scanner/Monitor are labels, not objects | OA-0051 |
| §4.1 trigger set incl. Position opened/closed; Market open = 9:40 default, close = 3:50 default; window customizable 9:31 → 5 min before close (15:55); market-open runs at the user-specified start | OA-0663, OA-0673, OA-0674, OA-0671, OA-0677 |
| §4.1 scheduled events: repeating patterns, holiday skip/before/after | OA-0057, OA-0058 |
| §4.2 execution order Exit Options → Events → Monitors → Scanners; monitors-before-scanners rationale; in-flight duplicate-action block | OA-0073, OA-0090, OA-0069 |
| §4.2 within-class order genuinely contradictory in docs ("adjustable synchronous order" vs "never guaranteed") | OA-0067, OA-0070 |
| §4.2 distributed work queue — no exact-minute guarantee (15:52 backstop has a buffer, not a slot) | OA-0093 |
| §4.2 default cadence 15 min, ~9:45–15:45, last scan 3:45; 1-min scans skip a beat if the prior interval hasn't finished | OA-0091, OA-0096, OA-0670, OA-0672 |
| §4.3 position loop oldest→newest — **with a documented caveat the file lacks: OA "reserves the right to change" the ordering** | OA-0076 |
| §4.4 logs record actions *and* non-actions; filter by date/type/errors; retention DOCS-SILENT | OA-0642–OA-0646, OA-0647 |
| §4.5 failsafe: 10 errors/day turns off all automations at the 10th; same-day re-enable re-trips on 1 error; resets next trading day; surfaced homepage + dashboard "errors"; which error types count is DOCS-SILENT | OA-0356–OA-0362, OA-0364 |
| §4.5-adjacent: the four named Warnings do NOT count toward the failsafe | OA-0324 |
| §4.6 Instant Exit Options are live-bots-only | OA-0868 |
| §4.7 event loops documented; limits are the designed defence | OA-0365–OA-0374 |
| §5.1 six decision families; conditional actions distinct from Yes/No; std-dev strike selection (price ± X·sd30, expiration plays no role) | OA-0687, OA-0690–0692, OA-0486–0488 |
| §5.1 indicators daily, cached pre-market; intraday toggle shifts bars + substitutes live price as final bar; IV Rank cached once daily | OA-1276–OA-1281, OA-0111, OA-1286, OA-0456 |
| §5.2 input chain: Bot Input takes priority; Default used only when the link is broken; documented silent-fallback instance ("copy to bot" → undefined Bot Input → Default used) | OA-0715, OA-0716, OA-0717, OA-0718 |
| §5.2 Exit Options as Bot-Input consumers: still absent from the inputs page (§9 #3 stands) | (no fact; OA-0704 DOCS-SILENT on the "5 types" count) |
| §5.3 tags: bot tags persist until user reset/untag; 9 actions; Reset replaces rather than adds; limits/expiry/clone-survival DOCS-SILENT | OA-0814, OA-0820, OA-0821, OA-0822, OA-0823 |
| §5.4 Position opened/closed triggers run once, **instantly/as-soon-as** — supports the `:00/:00` sibling-close timestamp test | OA-0368, OA-0369, OA-0675 |
| §6 Exit Options always run when automations are off (the backstop's architectural reason) | OA-0871 |
| §6 orders sent only when criteria met — nothing rests at the broker in advance | OA-0865, OA-0867 |
| §6.1 "six triggers" vs eight listed — reproduced defect confirmed | OA-0874, OA-0875 |
| §6.1 presets: named, reusable, auto-populate; cross-action scope genuinely DOCS-SILENT (§9 #4 stands) | OA-0892 |
| §6.4 2-minute order lifetime; "no additional orders" clause; re-check next interval and re-send if still met | OA-0877, OA-0883, OA-0878 |
| §6.5 re-apply Exit Options: "set and re-set" documented, side-effects still unaddressed (§9 #5 stands) | OA-0897, OA-0898 |
| §6.2/§6.3 Bid-Ask Guard disables closes and high/low tracking while spread is wide; while active no order is sent | OA-0873, OA-0891, OA-0263 |
| §7 SmartPricing walks mid→final; unfilled orders canceled and replaced; final-price order lives 2 minutes; PT auto-sets final price to lock the target | OA-0776–OA-0781, OA-0788, OA-0884, OA-0885 |
| §7 final-price % scale: 50 = mid-only, 100 = full traverse; default 100; best-of-multiple used — corroborates the first-hand floor-at-50 (and the v1-era "0% (bid)" docs wording exists nowhere in the current corpus) | OA-0791–OA-0794, OA-0808, OA-0789, OA-0810 |
| §8.2 (as amended): 15:52 inside the documented 15:55 cap; independently corroborated by the Oracle's 9:31–15:55 scan window | OA-0671, OA-1179 |
| §12 webhooks: 1 webhook → up to 10 automations in a bot + automations across multiple bots; persists across clones; instant; payload params + auth DOCS-SILENT | OA-0836, OA-0837, OA-0831, OA-0835, OA-0842 |
| Safeguards philosophy: risk-defined positions only; missing-input alert | OA-0774, OA-0745 |

`hedge-research.md` and the mirror doc's OA-side claims reconcile per R-20/R-19. **No CONTRADICTED
finding touches `build-plan.md`'s frozen decisions**; R-11 (limits >10) is the only finding that
grazes a plan assumption, and only for future re-entry specs.

---

## 4. Docs-internal conflicts to carry (new [CONFLICT] entries)

1. **Exit Options start time:** 9:31 (OA-0870) vs 9:40 (OA-0085). End (~15:59/3:59) agrees. → R-06.
2. **Expiring-ITM behavior:** `automation-behavior` says bots *"attempt to close the entire
   position"* if any leg is ITM on expiration day (**OA-0097**) vs the expiration-protocol page:
   the **default** sends **no order**, only an estimated P/L (**OA-0231/OA-0157**); a close
   happens only if the *"Close position with a market order"* Settings option is selected (**OA-0233**).
   Presumably OA-0097 describes the non-default setting, but as written the pages conflict.
3. **Negation:** "decisions do not use negation" vs the NOT property subsection (**OA-0044**).
4. **Safeguard trip scope:** *"automations automatically turn off if a limit triggers"*
   (**OA-0744**) vs *"Scanners are automatically turned off if a bot reaches either limit"*
   (**OA-0769**). The narrower scanner reading is what
   the file carries; keep both cites.
5. **Inputs count:** "5 types of inputs", 3 enumerated (**OA-0704**); the docs' own six-vs-eight
   trigger count (**OA-0874**) is the same defect class. Cite these when someone asks why OA's
   docs require a fact ledger.

---

## 5. Material DOCUMENTED facts absent from every judgment doc

Ranked by operational risk to an automated 0DTE program. These are the Phase 6 payload — each is
in `oa_facts.csv` and in **no** v2 doc.

1. **Expiration default = estimate, not close.** Default expiring-ITM handling is *"Calculate
   estimated P/L from Underlying Price"* — **no closing order is sent**; the reported P/L is
   synthetic while the real position rides into settlement (OA-0157, OA-0230, OA-0231). OTM
   positions are never closed (OA-0236). Last moneyness check at 15:50 (OA-0238); which price
   decides ITM is DOCS-SILENT (OA-0252). **Fleet consequence:** if the PT, the 15:50 time exit
   and the 15:52 backstop all fail on a QQQ position (physical settlement), the default setting
   quietly holds it into assignment. **Day-0 action: read the account's Options Expiration
   Protocol setting and record it in the capture**; decide deliberately between the three options
   (OA-0233).
2. **Assignment blindness.** Bots do not support and are unaware of assignment (OA-0245,
   OA-0246); the broker API does not report assignment events (OA-0145); OTM legs can still be
   assigned before or after the close (OA-0097, OA-0239); after assignment the bot keeps tracking
   the pre-assignment position and will still attempt exits against it, erroring (OA-0146,
   OA-0147, OA-0251). OA tracks positions independently of the broker (OA-0247) — **OA-side
   position state can silently diverge from broker truth**, which is exactly the class of failure
   the daily loop should be able to name.
3. **The PDT checkbox delays closes by a day.** If the PDT safeguard inside Exit Options is
   checked, the bot *"wait at least one day to close a position to avoid pattern day trading"* (OA-0890) — fatal
   to any 0DTE exit if ever enabled. **Add to §8.3/capture checklist: confirm the PDT box is
   UNCHECKED on every 0DTE bot.**
4. **Partial fills can strand a partial position.** Opening-order partial fills reset a 2-minute
   timeout; at expiry the remainder is canceled and the position flips to "open" **with the
   partial quantity** (OA-0140–OA-0142). Closing-order partial-fill behavior is DOCS-SILENT
   (OA-0144). A condor-leg spread that half-fills is a live sizing/lopsided-risk event no
   current detector rule names.
5. **Quotes can be stale exactly where this fleet trades.** Contract data updates at most every
   500ms **unless no new market update arrived** — thinly traded, far-OTM contracts can sit
   stale (OA-0105–OA-0107); bot-vs-broker screen mismatch is expected by design (OA-0108).
   Relevant to every "the mark was X at the trigger minute" forensic.
6. **Externally-closed positions keep receiving bot close attempts.** The bot honors automation
   close instructions and ITM handling *as if the position were open*, errors at the broker, and
   needs a manual override to stop retrying (OA-0131–OA-0133). Relevant to any manual
   intervention during the pilot/Day-0 window.
7. **The 10-symbol daily limit counts everything.** Opening, analyzing, monitoring, and custom
   inputs all count (OA-0347); with 10 assigned, symbol swaps must wait for after-hours
   (OA-0351). Multi-symbol Lab bots can hit this.
8. **Scheduled events are UTC-anchored.** *"A UTC offset is employed for all Scheduled
   events"* — a next-day automation must exist before UTC 00:00, the docs' own example being
   *"7:00pm EST or 8:00pm EDT"* (OA-0059). The
   docs' own EST/EDT split is the closest documented evidence bearing on the §8.2 DST question —
   it confirms OA schedules in UTC terms and does *not* resolve whether `ntime=1552` tracks
   market time across the DST boundary. The Day-0 observation stands.
9. **SPX pricing granularity.** Legs fill in nickels; the "mid" of an SPX leg with a $0.10–$0.15
   spread is $0.15 buying / $0.10 selling — not the arithmetic mid (OA-0801–OA-0806). Feeds the
   R-methodology's fill-quality analysis and the `IMPOSSIBLE_FILL` detector's tolerance.
10. **In-flight positions are invisible.** While an order is with the broker service the position
    is released from the bot and other automations do not see it as Open (OA-0136–OA-0138) —
    the documented mechanism behind the 7/01 orphan-loop shape, sharper than §4.2's "redundant
    position check" framing.
11. **Manual override frees limits.** An overridden position stops counting against position and
    allocation limits (OA-0130, OA-0759) — overriding a runaway position *raises* the bot's
    capacity to open more.
12. **Opportunity-check failures are silent by design** (OA-0382) — one more documented
    fail-quiet path for the liveness work.
13. **No canonical "automated trading" definition exists** — the platform's core-concept page is
    empty (OA-0632), as are Screener/Trade Grid/Top Strategies and both guides pages (OA-1508ff
    coverage rows). Any project doc citing detail from those pages cites something that is not
    there (none currently does).
14. **Before Expiration / Before Earnings use calendar days** (OA-0886) — matters if a time exit
    is ever specified in DTE terms on a Friday-weekend boundary.

---

## 6. Standing notes

- **Wave-1 fingerprints** on `data-feeds` / `autotrading-best-practices`: mismatch is a
  stripping-convention artifact until proven otherwise; all sampled quotes verify. Optional
  hygiene: re-run those two pages through the Wave-2 pipeline to refresh fingerprints.
- **OA-1285** (IV Rank formula) is recorded with an intentionally empty quote (`QUOTE
  UNVERIFIED`); treat as unquoted, usable.
- This report changes **no doc** by itself. Edits it motivates (R-01, R-02, R-03, R-04, R-05,
  R-06 tag changes; the §9 additions from R-11 and §5 items 1/3) go through the
  `oa-platform-reference.md` §0.2 editing policy and Andy's authorization where gated. ⛔ **CORRECTED 2026-08-05
  — the sentence that stood here was falsified within the hour it was written.** It read: *"The
  companion draft `docs/oa-platform-reference-v3-DRAFT.md` shows what the reference looks like with
  this report applied."* **It does not, and has not since 2026-08-04 03:55.** The draft was
  generated at 02:57 that day off base sha `1330dc59…7386`; the live reference was rewritten 58
  minutes later by the first-hand Settings/DOM session. The draft carries **0** `ANSWERED
  2026-08-04` §9 rows (the live file has **11**), **no §6.1a**, and a **§13 that collides** with the
  live §13 — so adopting it would *delete* the `itmlive`=`auto` finding and the PDT check.
  **`docs/oa-platform-reference-v3-DRAFT.md` is a superseded branch. Do not adopt it and do not
  cite it as current.** Its genuinely unique content — assignment blindness, the expiration
  protocol's documented half, partial fills, quote staleness, in-flight invisibility, UTC-anchored
  scheduled events, SPX nickel granularity, the empty core pages — was cherry-picked into the live
  reference as **§14 on 2026-08-05**, under Andy's ruling `ALT: NO` on
  `docs/r-edit-authorization-2026-08-05.md`. **R-01…R-07 and the three standing items were ruled
  per-item and applied 2026-08-05**; R-11 and R-13 above are **stale** — both were answered
  first-hand on 2026-08-04 (§9 checks #9 and #10) and need no doc change.
