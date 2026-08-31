# RULING DRAFT — GF family sizing — 2026-09-01 — ⬜ UNSIGNED

Status: **DRAFT. Phase 1 only.** No OA edit made, no repo-tracked file changed, nothing executed.
Source dispatch: `_dispatch-2026-09-01-gf-sizing-cowork.md` — **Phase 1 folded into the sizing
policy session; Phases 2 (execute) and 3 (record) are out of scope and post-signature.**
Companion: `_rulings-draft-2026-09-01-sizing.md` (R-2 is the same decision at family grain — sign
both or neither). Analysis: `_sizing-policy-draft-2026-09-01.md`. Caps: `_roe-cap-proposal-2026-09-01.md`.

---

## G-1 — THE AMENDMENT RULING

**Amends** `docs/pre-registration-ledger.md`, entries **PR-14, PR-15, PR-16, PR-17, PR-18, PR-19**
(and **PR-20 only if R-2b so chooses**), at their `MAX LOSS` and `SIZING TIER` lines.
**`PR-23 / GF-QQQ-IC-Ride-Delta` is EXCLUDED** — AUTOMATIONS set OFF 2026-08-31
(`data/captures/2026-08-31-roster/10-authorized-edits-2026-08-31.md` Edit 1; bot-level
`a5.bots.bot.scanning === false` on three agreeing surfaces after hard reload). A bot that is OFF
is not resized (`_rulings-draft-2026-09-01-sizing.md` R-1, class F).

**Standing text being amended** (all six/seven identical):
```
MAX LOSS         ~$185 net risk per condor; 1 condor/day.        [PR-14…PR-19]
MAX LOSS         1 lot per arm until one clears its interim read; then ≈$5K risk/position.
SIZING TIER      1 lot — IDENTICAL across arms.
```
Note the standing `~$185` is itself now stale: the ledger's realised figure is **$193/leg**
(median, `data/trades.csv`, all 8 arms, n=15 legs each) — QQQ $2-wide less $0.07 median credit.
The amendment restates it from measurement rather than from the design estimate.

**Amended text, proposed:**
```
MAX LOSS         ≈$5K risk per position (the larger side of the condor), N ct; 1 condor/day.
                 Family daily aggregate ≤ $35,000 (7 active arms × ≈$5K).
                 📝 AMENDED 2026-09-01 per R-2026-09-01-GF-SIZING. Prior text — "~$185 net risk
                 per condor; 1 condor/day" / "1 lot per arm until one clears its interim read" —
                 left standing above. Measured pre-amendment risk was $193/leg at 1 ct
                 (data/trades.csv median, n=15 legs/arm), not the $185 design estimate.
SIZING TIER      ≈$5K risk/position, N ct — IDENTICAL across all active arms.
                 Set once, never ad hoc. Opens a SIZING EPOCH at the edit date: raw P/L is not
                 poolable across the boundary. R, sample counts and gate progress are unaffected.
```

**The family daily aggregate, stated explicitly — the old sleeve language MUST be re-ruled, never
silently violated.** 7 active arms × ≈$5K = **$35,000/day**, inside a re-ruled **QQQ IC sleeve cap
of $40,000/day** (7 GF + `QQQ-IC-0DTE-Fortress-NoPT50`). The standing `≤ $10K across the QQQ IC
sleeve` line is superseded by `_rulings-draft-2026-09-01-sizing.md` **R-3**, which must be signed
in the same sitting. **Signing G-1 without R-3 puts two signed documents in contradiction.**

SIGNED — Andy — ......................        N = ......

---

## G-2 — THE CONTRACT MATH, DERIVED LIVE

**Derivation, from `data/trades.csv` (post-cutover ledger, 8 GF arms, 15 legs each, 1 ct):**
```
QQQ spread width                  $2.00        (structure: shortputspread / shortcallspread, $2 wide)
median credit per contract        $0.07        (median `credit`, all GF legs)
risk per contract  = (2.00 - 0.07) × 100  =  $193
                    ← reproduces `risk` = $193 exactly (median; min $190, max $193, n=120 legs)
N = round(5000 / 193) = round(25.9)       =  26 contracts
resulting risk/position (larger side)      =  26 × $193 = $5,018
```

**Independent cross-check on a different surface** — the number is not just arithmetic:
`QQQ-IC-0DTE-Fortress-NoPT50` **already runs 26 ct on QQQ**, with `risk` = **$4,940** per leg
(= 26 × $190) in the same ledger. So 26 ct on a QQQ 0DTE IC is a size **OA is observed expressing
today**, on this account, not a projection. Sizing the GF family to 26 makes its Exp(R) directly
comparable to NoPT50 at identical contract size and identical fill regime — a second benefit
beyond fill realism.

**Alternative if you want to stay strictly under $5,000:** **N = 25** → 25 × $193 = **$4,825**.
**Recommendation: N = 26**, for the NoPT50 comparability above. $18 over $5,000 is inside the
`≈` the ledger's own tier language uses.

**What this costs, stated plainly** (`_roe-cap-proposal-2026-09-01.md` §1.3):
family single-day tail (all 7 arms max-lose together) **$1,302 → $33,852**, ×26.
Correlation is **proven, not assumed**: on **2026-08-26 all 8 arms lost on the same day** — the
only bad day in the sample hit every arm at once. This family is one bet in seven wrappers.

**Andy approves the final N.**   N = ......        SIGNED — Andy — ......................

---

## G-3 — THE EXACT EDIT PLAN

### ⛔ G-3a · STEP 0 — SHARED-SCANNER ENUMERATION. UNRESOLVED. THIS IS A GATE.
`GF-ScannerA-PutSpread` / `GF-ScannerB-CallSpread` are **SHARED Library automations**. A quantity
change on a shared scanner **propagates to every attached bot**. The attachment list is
**not answerable from any local surface**:
- `data/bots_config_v2.csv` records `attached_to = "NONE (Unused)"` for ScannerA at **v9** — a
  stale 2026-08-06 Phase-A capture. The automation is at **v12** per the ledger's CONFIG HASH stamp.
- `pre-registration-ledger.md` records `sharing:1`, `"8 bots"` — that is a **count**. A count is
  not a membership list.

Per `CLAUDE.md` §5, *"inference from absence is never an evidence-backed correction"*. This draft
therefore **does not assert the scanners are GF-only.**

**STEP 0, read-only, before any edit:** open each shared automation from the OA Library and
enumerate **every bot it is attached to**. Expected: exactly the 8 `GF-QQQ-IC-*` arms.
- exactly those 8 → proceed, record the list in the capture;
- **any non-GF bot present → STOP and report. Make no edit.**

### G-3b · Which lever — decided and stated
**The contract-count lever is the SHARED SCANNER**, not per-bot:
`amount:{"type":"quantity","quantity":1}` → `{"type":"quantity","quantity":N}`.
**Why the shared lever:** "identical across arms" is the family's validity condition
(`SIZING TIER  1 lot — IDENTICAL across arms`). One shared edit makes drift structurally
impossible; seven per-bot edits make it a matter of seven chances not to typo.
**Why it is dangerous, and how that is contained:** it propagates to everything attached — which is
precisely what STEP 0 exists to bound. **The shared lever is safe if and only if STEP 0 comes back
with exactly the 8 GF arms.** If it does not, fall back to per-bot copies and report first.

Pre-hashes that must match before editing (`pre-registration-ledger.md` CONFIG HASH, re-confirmed
byte-identical 2026-08-31 in `10-authorized-edits-2026-08-31.md`):
```
GF-ScannerA-PutSpread  v12  1e5eb9936a1adf067af65a4841d42e755592f7c179f3c0cad477502dfdbfcdc8
GF-ScannerB-CallSpread v4   a925d490b8a0d2337566f47307fc52470da129935d3bd83d24389c6dc433dfb5
```
Either pre-hash not matching → **STOP**: the library moved since the stamp.
⚠️ **A VERSION INCREMENT IS NOT EVIDENCE — only the hash is.** ScannerA once went v10→v11 with a
byte-identical payload and an identical hash.

### G-3c · Allocation, per bot, so the new size fits
`$2,500 → $10,000` on each of the 7 active arms (`data/captures/…/07-…tsv`: all 8 GF arms at $2.5K).
Safeguards drawer, `input[name="seed"]`, Save, **HARD RELOAD**, verify `a5.bots.bot.seed === 10000`
**and** the Safeguards panel reads $10,000 — two surfaces, per the 08-31 Edit 3 pattern.
⚠️ **Allocation is not position size.** It is a container. This edit alone changes nothing about
what the bot trades; G-3b is the edit that changes size. (The inverse of this trap bit `3DTE
$140-$350` on 08-31, where allocation *was* position size because its Bot Input is "26% of net
liquid".) Re-read and record unchanged on each bot: DAILY POSITIONS, POSITION LIMIT, DAY TRADING,
BOT GROUP, AUTOMATIONS, EXIT OPTIONS.

### G-3d · The Canary conflict — must be resolved BEFORE the shared edit
If R-2b holds Canary at 1 ct, **the shared scanner cannot be its lever** — one shared edit hits all
eight. Two routes, pick one at signing; **do not improvise a third:**
- **(a) Detach Canary** onto bot-local 1-ct copies of both scanners. Precedent exists on the
  account: `GF-QQQ-IC-Ride-Delta` already carried bot-local `Ride-Delta-Scan-Put/Call` alongside the
  shared pair (`10-authorized-edits-2026-08-31.md` Edit 1). *Cost:* Canary's entry surface stops
  being the shared pair, so its CONFIG HASH stamp needs re-issuing.
- **(b) Size Canary with the family** and record the deviation from PR-20's `MAX LOSS  1 lot,
  smallest expressible risk` as an amendment. *Cost:* ~$4,825/day of tail on a bot whose P/L is
  stipulated to be meaningless.

Route: ☐ (a)   ☐ (b)        SIGNED — Andy — ......................

### G-3e · Verification — both layers, neither substitutes for the other (`CLAUDE.md` §5)
- **Layer 1, immediate:** re-open each edited automation fresh with a **HARD RELOAD**, recompute
  `sha256(JSON.stringify({name, inputs, root}))`, record the before/after pair. Re-read `seed` from
  the server-hydrated model **and** the panel. A save confirmation or tool-success message is
  **never** this check.
- **Outer check:** full `/bots` roster capture **before** and **after**, same instrument, same
  parse, **diffed** — exactly the intended bots differ and nothing else. Footer bot count and
  AUTOS/EXITS tallies compared. (The 08-31 pattern.)
- **Layer 2, behavioural, the day after:** the **first new position** each amended arm opens —
  read its **Trades list** and confirm quantity = N. **The Exit Options panel is NEVER evidence.**
  A fix unverified after one trading day is repeated at the top of every brief until closed.
- Captures to `data/captures/<ET-date>-gf-sizing/` with `SHA256SUMS.txt`. **ET date from the
  capture's own page header, never the container clock.**
- Confirm **ACCOUNT = Paper Trading** on each bot's own page before acting. The OA login also
  carries a live brokerage account (`TR ****4219`) — never select it.
- If a JS call returns `Inspected target navigated or closed`: **do not re-fire.** Hard reload and
  re-read; the work may already be committed.

---

## G-4 — CANARY CHECK (dispatch Phase-1 item 4)
Read of PR-20 (`pre-registration-ledger.md` L1617-1652): `PILLAR/ROLE  IC · control (instrument)` ·
`MECHANISM  n/a — this bot is NOT run for edge. Its P/L is expected to be ~flat and is not evidence
about anything.` · `SAMPLE TARGET  n/a — daily fill/no-fill is the output.` · `MAX LOSS  1 lot,
smallest expressible risk.` · `KILL CRITERION  NONE ON P/L — exempt by design.`

**Its instrument role requires 1 lot in substance, though the entry does not say so in words.**
Canary detects a dead exit engine by whether its 5% profit target fills each day. **A fill/no-fill
signal is size-invariant.** 26 ct buys no detection power and adds ~$4,825 of daily tail to a bot
whose P/L the ledger stipulates is meaningless. It is not an arm of the exit-policy A/B — it is a
control on the *platform*, not on the exit policy, and it is already excluded from family Exp(R)
comparisons by role — so holding it at 1 ct does not make the A/B unreadable.

**Flagged, as instructed. Proposal: keep Canary at 1 ct, stated in the ruling.** Andy decides
(R-2b in the companion file). If he holds it at 1 ct, G-3d must be resolved before Batch 1.

---

## G-5 — EPOCH NOTES, drafted for `data/bots_meta.csv` (Phase 3 — NOT written here)
One row-note per amended arm, on the edit date, verbatim shape:
```
<ET-date>: 1ct -> Nct, ≈$5K risk/position per R-2026-09-01-GF-SIZING; raw P/L not poolable
across this boundary; R, sample counts and gate progress unaffected.
```
Arms: `GF-QQQ-IC-Ride`, `-PT50`, `-Trail`, `-Touch0`, `-SL100`, `-SL200` (+ `-Canary` only under
route (b)). **Not** `-Ride-Delta` (OFF).

Ledger discharge lines follow the **PR-04 discharge pattern**: append `AMENDED` lines with the
ruling id; **never rewrite the original text.**

---

## G-6 — WHAT PHASE 2 MAY NOT DO
Phase 2 executes **only** what is signed above. It does not touch strikes, filters, exit policy,
schedules, groups (except under R-5 if separately ticked), or any bot outside the 7 named arms.
It does not switch any bot ON or OFF. `GF-QQQ-IC-Ride-Delta` is not re-armed. The legacy champion
`IC-SPX-FastPT25-S2` and its `-130PM` clone are **deliberately Exit-Option-free ride+S2 controls**
(`CLAUDE.md` §5 standing exception) — not touched, not "fixed", not re-armed.
