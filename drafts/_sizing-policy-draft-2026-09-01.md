# SIZING POLICY — DRAFT FOR SIGNATURE
**Drafted 2026-08-31 ~19:15 ET** (dispatch dated 2026-09-01; ET clock read in-session, not assumed).
**DRAFT-ONLY.** No OA edit was made. No repo-tracked file was changed. Nothing here executes.
Session scope: `_dispatch-2026-09-01-sizing-policy-cowork.md` **plus** Phase 1 only of
`_dispatch-2026-09-01-gf-sizing-cowork.md` — see §0.

## 0. Scope ruling on the second dispatch
`_dispatch-2026-09-01-gf-sizing-cowork.md` is **a component of this session, in part.**
Its **Phase 1 (draft)** is the GF-family instance of deliverables 1, 2, 5 and 6 here — folded in,
and written out as `_rulings-draft-2026-09-01-gf-sizing.md`.
Its **Phase 2 (execute in OA)** and **Phase 3 (record to repo)** are **out of scope** — they are
post-signature, and this session is draft-only by your instruction. The execution paste in §6
is what a Phase-2 session would run.

## 1. Derivation base — every figure below traces to one of these
| # | Surface | What it establishes |
|---|---|---|
| S1 | `data/trades.csv`, 205 rows, 16 trading days 2026-08-10→08-31 | current risk/leg, qty, credit, P/L, R, per-day series |
| S2 | `data/captures/2026-08-31-roster/07-allocation-and-groups-2026-08-31.tsv` | allocation + OA bot group, all 44 bots (pre-edit 17:31 ET) |
| S3 | `data/captures/2026-08-31-roster/10-authorized-edits-2026-08-31.md` | the four 08-31 edits; post-edit AUTOS 18/44; groups 44/44 |
| S4 | `STATUS.md` (generated 2026-08-31) | readiness board, stages, gates, allocation-realism table |
| S5 | `docs/pre-registration-ledger.md` | sizing ladder (L82-83), per-entry MAX LOSS / SIZING TIER, sleeve caps |
| S6 | `data/archive/trades.csv` + `data/archive/README-v1-ledger.md` | the pre-cutover same-tier drawdown record (history only, never a fleet-state claim) |
| S7 | `scripts/roster.py` `FAMILY_RULES` (L38-53) | the 12-family taxonomy |
| S8 | `data/bots_config_v2.csv` | the post-cutover config record (see §5 — it does **not** answer the shared-scanner question) |

**Unit law applied throughout** (`CLAUDE.md` §4): the unit is the **POSITION**; a condor = its two
spread rows paired by `trade_id`; **risk = the larger side.** Consequence you should see stated
once, plainly: for an equal-width condor, **risk per position = one side ≈ $5K, not $10K.** Both
sides cannot max-lose on the same expiry. Your "≈$5K per leg → ≈$10K total per bot" is the sum of
the two spreads' widths; the amount actually at risk per condor is **$5K**. Every aggregate below
uses $5K/position.

## 2. Deliverable 1 — the fleet sizing ladder

### 2.1 The conflict this ruling has to resolve, stated first
The ledger's ladder (S5 L82-83) is **`1 lot (experiment) | ≈$5K risk/position (CANDIDATE+)`** —
i.e. size follows stage. On the readiness board today (S4), **every graduating bot is VALIDATE**,
every one blocked at **G2 (need 20 clean condors; best is n=16)**, and **not one bot is CANDIDATE.**
Under the ladder as written, **nothing sizes up today.** That is a direct contradiction of your
stated intent, and no amount of drafting hides it. So the ruling has to either defer your intent
or change the ladder's principle. Recommendation below changes the principle, with a reason.

### 2.2 The reason to change it — from your own board, not from preference
S4's allocation-realism table flags twelve ON bots **"1-lot — fill-untested"**, with the note:
*"their edge won't survive the slippage of a real order size."* That is the board saying its own
1-lot Exp(R) is not evidence about a $5K-sized version of the same bot. If that is true — and it
is the board's own standing text — then running a 1-lot arm to n=100 produces a number **that does
not transfer to the size it would be traded at.** Size-on-graduation therefore certifies a
statistic about an instrument nobody will trade.

Gate **G6** (S5 L137) requires sizing be *"declared once per phase, with the reason in writing —
not by preference."* The reason in writing is: **R is size-free, fills are not.**

### 2.3 Proposed ladder — SIZE AT ENTRY, not size on graduation
> **Principle.** A bot is sized, from its first position, at the tier its results are intended to
> be read at. Sizing is set **once per epoch**, never ad hoc, and a sizing change **opens an epoch
> boundary**: raw P/L is not poolable across it; R, sample counts and gate progress are unaffected.

| Class | Who it is (by S4 `role`) | Risk per position | Rationale |
|---|---|--:|---|
| **A — read at live scale** | `live-candidate`, `experiment` whose result is meant to inform live capital | **≈$5K** | its Exp(R) must be a fill-realistic number |
| **B — control** | `control` arms paired to a class-A arm | **≈$5K, identical to its arm** | a control at a different size is not a control |
| **C — instrument (ops-class)** | `instrument` (PR-20 Canary) | **1 lot, permanently** | S5 §2a: not run for edge; its output is fill/no-fill, which 1 lot answers as well as 26 |
| **D — mirror-watch** | `mirror-watch` | **unchanged, never resized** | S5: *"Do not resize a watch-only bot"* ×7 entries; resizing breaks mirror fidelity |
| **E — negative-CI arms** | any bot whose Exp(R) 95% CI lies entirely below 0 | **frozen at current size** | see §3, `DIR-SPX-CallVIXdrop` |
| **F — OFF / archived** | AUTOS OFF | **no change, ever, while OFF** | sizing an idle bot is an unverifiable edit |

Class E is an addition, not in the current ladder. It exists because the ladder as written has no
brake: without it, "size at entry" would size up a bot the board already shows losing.

### 2.4 The GF "1 lot until interim (n=60)" clause — the three options
S5 PR-14…PR-23 carry **`MAX LOSS  1 lot per arm until one clears its interim read; then ≈$5K risk/position`**
and `SIZING TIER  1 lot — IDENTICAL across all arms`. Signed 2026-08-09, re-signed 2026-08-17.
Current progress: **n = 4 clean condors per arm** (S4 readiness board). n=60 is not close.

| | Option | What it costs | What it buys |
|---|---|---|---|
| **(i)** | **Amend now to ≈$5K/leg, all 7 active arms, identically** | family single-day tail **$1.3K → $33.9K** (§4.2) | fill realism on the whole family from today; direct comparability with `QQQ-IC-0DTE-Fortress-NoPT50`, which already runs **26 ct** on the same underlying |
| **(ii)** | **Hold the signed clause — stay 1 lot to n=60** | your stated intent deferred ~; at 4 condors/arm over 9 fill-days the interim read is far out | nothing changes; no new tail |
| **(iii)** | **Retire arms first, then size the survivors** | a decision you have not made | 7 arms × $5K is expensive *because there are 7 arms*; the tail is linear in arm count |

**Recommendation: (i), conditional on §4's caps being signed in the same sitting.** The clause's
own trigger ("until one clears its interim read") was written to defer size until the evidence
justified it — but §2.2 shows the evidence collected at 1 lot cannot justify it, because it is not
about the traded size. The clause is self-blocking. Amend it.

**Do not sign (i) without §4.** Sizing up 26× with G4's dollar cap still an unfilled `<FILL>`
(S4 gate line; `scripts/report.py` L1022 `MAXDD_R_CAP = -5.0  # RoE $ cap still a <FILL> blank`)
is the one combination this project's own evidence law forbids.

### 2.5 The sleeve aggregate caps — MUST be re-ruled, or (i) contradicts standing signatures
Standing, signed (S5): **`Daily aggregate ≤ $10K across the SPX IC sleeve`** (PR-01, PR-02) and
**`≤ $10K across the QQQ IC sleeve`** (Fortress/NoPT50 entries).

Post-(i) reality, at $5K/position, ON bots only (S3 post-edit toggles):

| Sleeve | ON members | Aggregate at $5K/position | Standing cap | Verdict |
|---|---|--:|--:|---|
| QQQ IC | 7 GF arms + `QQQ-IC-0DTE-Fortress-NoPT50` = 8 | **$40,000** | $10,000 | **4.0× over — breached** |
| SPX IC | `FastPT25-S2`, `-130PM`, `Fortress-Unstopped` = 3 | **$14,700** (already, today) | $10,000 | **1.5× over — ALREADY BREACHED TODAY** |
| Directional | `CallVIXdrop`, `PutVIX22-SL75` (1 lot) | ~$1,300 | — | — |
| OA-Mirror | 5 ON, unchanged | ~$10,300 concurrent | — | — |

⚠️ **Finding, independent of any sizing change:** the **SPX IC sleeve is over its signed $10K daily
cap right now** — three ON arms at ~$4,900/position each (S1: `IC-SPX-FastPT25-S2` $4,900,
`-130PM` $4,750 med / $4,900 max, `IC-SPX-Fortress-Unstopped` $4,900). This is a live breach of a
signed pre-registration line and it predates this session. Proposed ruling text is in
`_rulings-draft-2026-09-01-sizing.md` §R-3.

**Proposed re-ruled caps** (the ruling must state these explicitly, never let them be silently
violated):

| Sleeve | Proposed daily aggregate cap | Derivation |
|---|--:|---|
| SPX IC | **$15,000** | 3 ON arms × $5K; = the roster as it stands, made legal rather than silently breached |
| QQQ IC | **$40,000** | 8 ON arms × $5K |
| Directional | **$5,000** | 1 position × $5K — a ceiling, not a target; both arms stay 1 lot per §3 |
| OA-Mirror | **$12,000** | current concurrent open risk ~$10.3K (S2 `open_risk` column), rounded up; watch-only, never resized |
| **FLEET** | **$72,000/day authorized risk-at-work** | sum |

That $72K is the number to look at before signing. It is what the fleet is *authorized to have at
risk* on a single trading day after (i). It is not a loss estimate — §4 is.

## 3. Deliverable 2 — per-bot target table
Current risk/leg and qty are **derived from S1**, not from the roster display and not guessed:
median `risk` per leg, per bot, over the post-cutover ledger. `N` targets are `round(5000 / risk-per-contract)`.

### 3.1 ON bots
| Bot | Family (S7) | Role (S4) | Cur qty | Cur risk/leg (S1) | Risk/ct | **Target** | OA lever | Epoch note |
|---|---|---|--:|--:|--:|---|---|:--:|
| `GF-QQQ-IC-Ride` | Greenfield QQQ IC | control | 1 | $193 | $193 | **26 ct ≈ $5,018** | shared `GF-ScannerA/B` `amount.quantity` 1→26 **+** allocation $2.5K→$10K | **Y** |
| `GF-QQQ-IC-PT50` | " | experiment | 1 | $193 | $193 | **26 ct ≈ $5,018** | ditto (shared) | **Y** |
| `GF-QQQ-IC-Trail` | " | experiment | 1 | $193 | $193 | **26 ct ≈ $5,018** | ditto (shared) | **Y** |
| `GF-QQQ-IC-Touch0` | " | experiment | 1 | $193 | $193 | **26 ct ≈ $5,018** | ditto (shared) | **Y** |
| `GF-QQQ-IC-SL100` | " | experiment | 1 | $193 | $193 | **26 ct ≈ $5,018** | ditto (shared) | **Y** |
| `GF-QQQ-IC-SL200` | " | experiment | 1 | $193 | $193 | **26 ct ≈ $5,018** | ditto (shared) | **Y** |
| `GF-QQQ-IC-Canary` | " | **instrument** | 1 | $193 | $193 | **1 ct — NO CHANGE** | none | N |
| `IC-SPX-FastPT25-S2` | SPX FastPT25 | live-candidate | 10 | $4,900 | $490 | **10 ct — no change** (already ≈$5K) | none | N |
| `IC-SPX-FastPT25-S2-130PM` | " | experiment | 10 | $4,750 (max $4,900) | $490 | **10 ct — no change** | none | N |
| `IC-SPX-Fortress-Unstopped` | SPX Fortress | control | 10 | $4,900 | $490 | **10 ct — no change** | none | N |
| `QQQ-IC-0DTE-Fortress-NoPT50` | QQQ Fortress line | experiment | **26** | $4,940 | $190 | **26 ct — no change** | none | N |
| `DIR-SPX-CallVIXdrop` | SPX directional | experiment | 1 | $635 (max $675) | $635 | **1 ct — FROZEN, class E** | none | N |
| `DIR-SPX-PutVIX22-SL75` | SPX directional | experiment | — *(no post-cutover fills)* | — | — | **1 ct — no change** | none | N |
| `Nigiri-Paper-v1` | Live mirrors | mirror-watch | 10 | $4,910 | $491 | **no change** | none | N |
| `3DTE $140-$350` | Live mirrors | mirror-watch | 1 | $955 | $955 | **no change** — but see §4a | (alloc already $5K→$10K, 08-31) | see §4a |
| `Friday 14 DTE BW IB (B-70)` | Live mirrors | mirror-watch | 1 | $1,960 | $1,960 | **no change** | none | N |
| `Trendy-Paper-v1` | Live mirrors | mirror-watch | 1 | $930 | $930 | **no change** | none | N |
| `60min-ORB-10W-Paper-v1` | Live mirrors | mirror-watch | 1 | $915 | $915 | **no change** | none | N |

### 3.2 OFF bots — no sizing action while OFF (class F)
`GF-QQQ-IC-Ride-Delta` (AUTOS ON→OFF 2026-08-31, S3 Edit 1) is **excluded from the GF amendment**,
matching the GF dispatch's own exclusion. Its $2.5K allocation and 1-lot sizing stay as they are.
All 17 `Archive`-group bots, `IC-SPX-Fortress-Defang`, `DIR-SPX-Put-Control`, `Tasty Condor`,
`QQQ long call`, `QQQ-IC-0DTE-Fortress` and the 3 `-ARCHIVED-` clones: **no change.**

### 3.3 A/B integrity check — "identically or not at all"
- **GF family:** 7 active arms all move to 26 ct **except Canary**, which stays at 1 ct. This is a
  deliberate, stated exception, not a drift — see §3.4. Ride (control) moves with its experiments ✓.
- **SPX FastPT25 pair:** both at 10 ct, unchanged ✓ — the A/B is untouched by this ruling.
- **`IC-SPX-Fortress-Unstopped`** is a control with its paired arm (`-Defang`) **OFF**. Sizing is
  unchanged, so no A/B is disturbed; flagged only because a control without a live counterpart is
  a standing oddity, not a sizing question.

### 3.4 Canary check (GF dispatch Phase-1 item 4) — **recommend keeping Canary at 1 ct**
PR-20 (S5 L1617-1652) is `PILLAR/ROLE  IC · control (instrument)`, `MECHANISM  n/a — this bot is
NOT run for edge. Its P/L is expected to be ~flat and is not evidence about anything.`,
`SAMPLE TARGET  n/a — daily fill/no-fill is the output.`, `MAX LOSS  1 lot, smallest expressible
risk.`, `KILL CRITERION  NONE ON P/L — exempt by design.`
Its instrument role is *detecting that the exit engine died* via a 5%-PT fill that should occur
every day. **A fill/no-fill signal is size-invariant** — 26 ct buys no extra detection power and
adds ~$4,825 of daily tail to a bot whose P/L is stipulated to be meaningless. Keeping it at 1 ct
does **not** break the A/B, because Canary is not an arm of the A/B: it is a control *on the
platform*, not on the exit policy, and it is already excluded from every family Exp(R) comparison
by role. **Your call — it is stated in the ruling either way.**

## 4. Deliverable 3 — mirrors
**Default: NO RESIZE. Stated explicitly.**
`docs/pre-registration-ledger.md` carries **`SIZING TIER  Unchanged from current. Do not resize a
watch-only bot.`** on **seven** mirror entries (S5 L540, L623, L678, L740, L802, L855, L909, L965)
plus the shared §5 frame. The reason is not conservatism, it is measurement: a mirror exists to
reproduce a third party's published record, and the funding bar (S5 L530-536) scores
*"max single-trade loss ≤20% of intended live allocation"* and *"no single loss >1.5× the source's
largest disclosed loss"* — **both are denominated against the source's size.** Resize the mirror
and both criteria stop meaning what they were written to mean. The mirrors are also the pillar
whose numbers feed a **funding** decision (`data/mirror_baseline.csv`), which is the one place
pre-cutover figures are admissible; changing size mid-stream contaminates it.

**No mirror is resized by this ruling.** `Nigiri-Paper-v1` already sits at $4,910/position (S1) —
that is its own configuration, not a target this ruling set.

### 4a. The one exception — `3DTE $140-$350`, already applied 2026-08-31
S3 Edit 2 raised its **allocation** $5,000 → $10,000, with the consequence disclosed in the same
capture: its Bot Input **POSITION SIZE is "26% of net liquid", not a fixed dollar figure**, so
doubling allocation doubles the dollar size of every future position. This crossed the
"do not resize a watch-only bot" line **in effect**, though not in the field that was edited —
the canonical allocation-is-not-position-size trap, arriving from the other direction.
Exception ruling text: `_rulings-draft-2026-09-01-sizing.md` §R-4. Two paths are drafted there
(ratify, or revert to $5K); **revert is the recommendation**, because the bot's own pre-reg
`MAX LOSS` line reads *"Paper allocation $5K, deliberately small — one bad position is 20%+ of it"*
— the $5K figure is load-bearing in its funding criterion, not incidental.

## 5. Deliverable 4 — OA groups / tags audit
Post-edit (S3 Edit 4): **44 of 44 bots grouped, no ungrouped bot remains** ✓.
Seven groups: `Archive 17 · Directional-Focus 2 · IC 8 · IC-Focus 3 · Lab 0 · Monitor 10 · OA-Mirror-Focus 4`.

**The two schemes are orthogonal by design and that is correct:** OA groups encode *lifecycle /
attention* (Focus, Monitor, Archive, Lab); `FAMILY_RULES` (S7) encodes *strategy lineage*. A family
spanning several groups is expected — `Live mirrors` legitimately spans Archive/Monitor/OA-Mirror-Focus.
Cross-tab run in-session over all 44 (S2 × S7). **Three findings, one of them a real defect:**

| # | Finding | Severity |
|---|---|---|
| **A** | **All three `-ARCHIVED-` clones are outside the `Archive` group.** `IC-SPX-FastPT25-S2-ARCHIVED-2026-08-07` sits in **`IC-Focus`**; `IC-SPX-FastPT25-S2-130PM-ARCHIVED-2026-08-08` and `QQQ-IC-0DTE-Fortress-NoPT50-ARCHIVED-2026-08-08` sit in **`Monitor`**. All three are AUTOS OFF. `IC-Focus` is defined in S4 as *"the bots you're actively perfecting"* — an archived clone in it is a misfiling that inflates the Focus roster. | **fix** |
| **B** | **`IC` is the only group named for a pillar rather than a lifecycle stage**, and it contains exactly the 8 GF arms and nothing else. It reads as "the IC pillar" (which would be 13 bots) but means "the greenfield family". Naming collision. Propose rename **`IC` → `GF-Family`**. | rename |
| **C** | `Lab` group is **empty (0 bots)**, consistent with S5 §6a (*"No specific bot is named or entered here yet"*). **Not a defect** — leave it. | none |

**Tag scheme — one proposal, deliberately minimal.** S5 §8 item 1 already fixes the scheme:
*"`PR-NN`, two digits, ledger entry order, **OA Tag = the bare ID**."* Propose: **verify and
complete the `PR-NN` tag on every bot that has a pre-registration entry.** That single tag is the
only label that makes the OA surface joinable to the ledger by key rather than by name-match, and
name-matching is what breaks when a bot is renamed or cloned. **Nothing else.** No new taxonomy,
no colour scheme, no per-strategy tags — groups already carry lifecycle, `FAMILY_RULES` already
carries lineage, and a third axis would need a third thing to keep in sync.
⚠️ Whether the `PR-NN` tags are actually applied in OA today is **not readable from any local
surface** — it needs a read-only OA pass. Not asserted here.

## 6. Deliverable 5 — execution paste for the follow-up OA session
> ⛔ **Two blockers must clear before this runs. Both are stated inside the paste.**

```
OA SIZING EXECUTION SESSION — paste into a new Opus Cowork chat with bot-fleet-v2 + Chrome/OA.

PRECONDITION 1 — SIGNATURE. Do not touch OA unless Andy's signature is in-chat on
  _rulings-draft-2026-09-01-sizing.md and _rulings-draft-2026-09-01-gf-sizing.md.
  Read both from ~/bot-fleet-v2 first. If either is unsigned: STOP, report, change nothing.

PRECONDITION 2 — SHARED-SCANNER ENUMERATION (unresolved; see §7 of the sizing policy draft).
  GF-ScannerA-PutSpread / GF-ScannerB-CallSpread are SHARED Library automations. The local
  config record (data/bots_config_v2.csv) records attached_to = "NONE (Unused)" at v9 — STALE
  and useless; the ledger says sharing:1 / "8 bots" at v12, which is a COUNT, not a membership
  list. A count is not evidence of membership.
  STEP 0, read-only: open each shared automation from the OA Library and enumerate EVERY bot
  it is attached to. Expected: exactly the 8 GF-QQQ-IC-* arms.
    - If it is exactly those 8 -> proceed; record the list in the capture.
    - If ANY non-GF bot appears -> STOP, report, make no edit. A quantity change on a shared
      scanner propagates to every attached bot.
  This step is a READ. It is not gated by "no OA edits" — it is gated by nothing.

CAPTURE DISCIPLINE (oa-driving skill; CLAUDE.md §5 two-layer proof)
  - ET date from the capture's own page header, never the container clock (UTC trap).
  - Save to data/captures/<ET-date>-gf-sizing/ with SHA256SUMS.txt.
  - OUTER CHECK: full /bots roster capture BEFORE any edit and AFTER all edits, same
    instrument, same parse, diffed. Exactly the intended bots differ and nothing else.
    (The 08-31 10-authorized-edits pattern.)
  - Per automation: sha256(JSON.stringify({name, inputs, root})) read after a fresh open with a
    HARD RELOAD, before and after. A VERSION INCREMENT IS NOT EVIDENCE — only the hash is
    (ScannerA once went v10->v11 byte-identical).
  - Confirm ACCOUNT = Paper Trading on every bot's own page before acting. The OA login also
    carries a live brokerage account (TR ****4219). Never select it.
  - Drawer ✕ discards. Never type paths into save dialogs.
  - If a JS call returns "Inspected target navigated or closed": DO NOT RE-FIRE. Hard reload and
    re-read state; the work may already be committed.

BATCH 1 — GF family entry sizing (the shared lever, ONE edit, propagates to the arms)
  Pre-hashes to match before editing (from docs/pre-registration-ledger.md CONFIG HASH,
  re-confirmed 2026-08-31 in 10-authorized-edits):
    GF-ScannerA-PutSpread  1e5eb9936a1adf067af65a4841d42e755592f7c179f3c0cad477502dfdbfcdc8
    GF-ScannerB-CallSpread a925d490b8a0d2337566f47307fc52470da129935d3bd83d24389c6dc433dfb5
  If either pre-hash does not match: STOP — the library moved since the stamp.
  Edit: amount {"type":"quantity","quantity":1} -> {"type":"quantity","quantity":N}
        with N = the value Andy signed (proposal: 26 — derivation in the gf-sizing ruling).
  Post: re-open fresh + hard reload, recompute both hashes, record the new pair.

  ⚠️ CANARY. If Andy signed "Canary stays at 1 ct", the shared scanner CANNOT be the lever for
  Canary — one shared edit hits all 8. Resolve before Batch 1 by ONE of:
    (a) detach Canary from the shared pair onto a bot-local 1-ct copy of each scanner
        (mirrors the Ride-Delta bot-local pattern already on the account), or
    (b) size Canary with the rest and record the deviation from PR-20's "1 lot, smallest
        expressible risk" as an amendment.
  Do not improvise a third route.

BATCH 2 — GF allocations, one bot at a time, 7 bots (Ride-Delta EXCLUDED — archived 08-31)
  Safeguards drawer, input[name="seed"] 2500 -> 10000. Save. HARD RELOAD.
  Verify: a5.bots.bot.seed === 10000 AND the Safeguards panel reads $10,000.
  Re-read and record unchanged: DAILY POSITIONS, POSITION LIMIT, DAY TRADING, BOT GROUP,
  AUTOMATIONS, EXIT OPTIONS.
  Bots: GF-QQQ-IC-Ride, -PT50, -Trail, -Touch0, -SL100, -SL200, -Canary(per the Canary ruling).

BATCH 3 — group hygiene (§5 findings A and B; only if signed)
  A: move the 3 -ARCHIVED- clones into the Archive group.
  B: rename group IC -> GF-Family.
  Both are metadata; still hash/verify per the same protocol.

LAYER 2 — BEHAVIOURAL, THE DAY AFTER (CLAUDE.md §5; a fix unverified after one trading day is
  repeated at the top of every brief until closed)
  On the FIRST NEW POSITION each amended arm opens, read its TRADES LIST and confirm
  quantity = N. The Exit Options panel is NEVER evidence. Report per arm.

DELIVERABLE at end: ruling signed y/n · N applied · scanner attachment list from STEP 0 ·
  hash pairs before/after · allocation seed pairs · fleet pre/post diff result ·
  files awaiting Andy's commit. Then CLAUDE.md §9.1 close-out.
```

## 7. Open blocker carried out of this session
**The shared-scanner attachment list is UNRESOLVED from local surfaces.** `data/bots_config_v2.csv`
records `attached_to = "NONE (Unused)"` for `GF-ScannerA-PutSpread` at **v9** — a stale 2026-08-06
Phase-A capture; the automation is at **v12** per the ledger's CONFIG HASH stamp. The ledger's
`sharing:1, "8 bots"` is a **count**, and a count is not a membership list. Per `CLAUDE.md` §5,
*"inference from absence is never an evidence-backed correction"* — so this draft does **not**
assert the scanners are GF-only. It is STEP 0 of the execution paste, read-only, and it is a
**STOP condition** if it comes back with any non-GF bot attached.

## 8. Deliverable map
| # | Deliverable | Where |
|---|---|---|
| 1 | Sizing policy draft ruling (fleet ladder) | §2 here; ruling text `_rulings-draft-2026-09-01-sizing.md` §R-1, §R-3 |
| 2 | Per-bot target table | §3 here |
| 3 | Mirrors recommendation | §4 here; ruling text §R-4 |
| 4 | OA groups/tags audit | §5 here; ruling text §R-5 |
| 5 | Execution paste | §6 here |
| 6 | Rulings drafts for signature | `_rulings-draft-2026-09-01-sizing.md` + `_rulings-draft-2026-09-01-gf-sizing.md` |
| 7 | G4 RoE $ cap (T-39) + breach playbook (T-40) | `_roe-cap-proposal-2026-09-01.md` |
