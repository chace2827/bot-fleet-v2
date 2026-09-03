# T-39 · G4 RoE $ CAP — PROPOSAL   ·   T-40 · BREACH PLAYBOOK — DRAFT
**Drafted 2026-08-31 ~19:15 ET. DRAFT-ONLY — nothing applied, no repo-tracked file changed.**
Rides the same signature sitting as `_rulings-draft-2026-09-01-sizing.md`.

---

# PART 1 — T-39: the G4 dollar cap

## 1.1 What is actually blank
`docs/evidence-standards.md` L277: **G4 | Risk — maxDD-R within cap | `maxDD-R ≥ −5.0`. ⚠️ The RoE
$ cap is an unfilled `<FILL>`, so half of G4 is permanently pending.**
`scripts/report.py` L1022: `MAXDD_R_CAP = -5.0   # maxDD-R floor for G4 (RoE $ cap still a <FILL> blank)`
L1133 emits `f"maxDD-R {mdd:.1f} (RoE $ cap pending)"`.

So G4 has two halves. The **R half** is live and size-free. The **$ half** is the one that notices
size — and it has been blank the whole time size never changed. **The sizing ruling is the event
that makes it load-bearing.** Filling it is not housekeeping; it is the brake on the ruling.

**You do not invent this number.** Every figure below is derived from a file surface and cited.
There is exactly one input I cannot derive — see §1.7.

## 1.2 The four anchors, all derived in-session

| # | Anchor | Value | Derivation |
|---|---|--:|---|
| **A1** | v1 champion's worst cumulative $ drawdown, **at the tier being adopted** | **−$14,540** | `data/archive/trades.csv`, `IC-SPX-FastPT25-S2`: 364 legs / 221 positions, 10 ct SPX ≈ $4,900/leg. Daily cumulative closed-P/L series, peak-to-trough. All-time raw **−$11,155** (matches `README-v1-ledger.md`'s −$11,155). |
| **A2** | v1 champion's worst **single day**, same tier | **−$8,050** on **2026-06-11** | same series |
| **A3** | Post-cutover fleet, **replayed at the new tier** (GF arms ×26, everything else unchanged, Ride-Delta excluded) | worst day **−$4,112** (08-26) · worst cumulative DD **−$6,150** · mean **+$681/day** | `data/trades.csv`, 16 trading days 08-10→08-31 |
| **A4** | Post-cutover fleet **as it runs today** | worst day **−$2,038** (08-27) · worst cumulative DD **−$3,937** · mean **+$285/day** · total **+$4,557 / 205 legs** | `data/trades.csv`; total matches `STATUS.md` headline |

⚠️ **Two corrections to figures named in the dispatch.**
1. *"the champion's observed maxDD-R (−0.68 at n=16)"* — **−0.684 at n=16 condors is
   `IC-SPX-FastPT25-S2-130PM`**, not the champion. The champion proper,
   `IC-SPX-FastPT25-S2`, is **−0.010 at n=16**. Both derived per-condor from `data/trades.csv`.
   Grain: per-condor, day-ordered cumulative-R drawdown; the champion's −0.010 cross-checks
   against `STATUS.md` L33 (`Max drawdown (daily cumulative): $-50`) ÷ $4,900 risk = −0.0102.
   The −0.68 arm is the right one to reason from (it has the real risk shape), but it must be
   labelled correctly or the ruling cites a number that isn't where it says it is.
2. *"one max loss ≈ 1.7 winning days at current tier"* — **does not reproduce.** Derived:
   largest single-position max loss today is **$4,940** (`QQQ-IC-0DTE-Fortress-NoPT50`, 26 ct);
   fleet mean is **$285/day** (A4); **$4,940 / $285 = 17.3 winning days.** Probably a lost
   factor of ten. Recomputed at the new tier in §1.3.

## 1.3 The tail math, recomputed at the new tier
> **Unit law** (`CLAUDE.md` §4): risk per condor = **the larger side**. One side maxes, the other
> keeps its credit. Per arm at 26 ct: $5,018 risk − $182 surviving credit = **$4,836 worst case**.

| Quantity | Current tier | **New tier** | Change |
|---|--:|--:|--:|
| One position's max loss | $4,940 | ~$5,018 | ~flat |
| Fleet mean $/day | $285 | $681 | ×2.4 |
| **One max loss, in mean-winning-days** | **17.3** | **7.4** | **improves** |
| **GF family full tail — all 7 arms max-lose the same day** | **$1,302** | **$33,852** | **×26** |
| that tail, in mean-winning-days | 4.7 | **49.7** | **×10.6** |
| Fleet authorized risk-at-work per day (sizing draft §2.5) | ~$26K | **~$72K** | ×2.8 |

**Read this carefully, because the headline ratio lies.** "One max loss = N winning days" *improves*
when you size up, because the winning side scales with the losing side. That ratio is not the risk.
**The absolute tail is**, and the tail goes from a rounding error to a number that erases seven
weeks of average performance in one session.

## 1.4 Correlation is proven, not assumed — this is the load-bearing finding
The seven GF arms are the same underlying, the same day, the same shared entry scanner, with
strikes differing only by exit policy. **They are not seven bets. They are one bet in seven
wrappers.** Derived from `data/trades.csv` — daily sum of per-arm R across the family:

| Date | 08-14 | 08-17 | 08-19 | 08-20 | 08-21 | 08-25 | **08-26** | 08-28 | 08-31 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| family Σ R | +0.244 | +0.316 | +0.383 | +0.228 | +0.207 | +0.363 | **−0.532** | +0.364 | +0.228 |
| arms losing | 0/8 | 0/8 | 0/8 | 2/8 | 1/8 | 0/8 | **8/8** | 1/8 | 1/8 |

On **2026-08-26, all eight arms lost on the same day.** There has been exactly one bad day in the
sample and it hit every arm at once. Any cap that treats the arms as independent is wrong on the
only evidence available.

**Therefore a per-bot cap alone cannot be the answer** — seven arms each comfortably inside a
per-bot cap can breach a sensible fleet limit together, on the same afternoon, by construction.

## 1.5 THE PROPOSAL — three levels, each derived, none invented

> ### CAP 1 — per-bot drawdown: **$15,000**
> **Because:** −$14,540 is the only drawdown ever actually observed **on this account, in this
> instrument, at this size** (A1 — 221 positions of 10 ct SPX at ~$4,900/leg, which is the tier
> the fleet is adopting). Rounded up to the nearest thousand.
> **Sanity, both directions:** it is **2.4×** the worst post-cutover drawdown replayed at the new
> tier (A3, −$6,150), so it does not fire on noise; and at the new-tier mean of $681/day it is
> **22 trading days** to recover — inside a quarter.
> **Measured as:** worst peak-to-trough cumulative *closed* P/L, per bot, within an epoch.

> ### CAP 2 — fleet drawdown: **$35,000**
> **Because:** Cap 1 is not binding under correlation, and §1.4 proves correlation. $35,000 is the
> GF family's own structural single-day maximum at the new tier (7 active arms × $5K risk/position),
> i.e. **the fleet halts the first time one family's full tail actually arrives** — rather than
> discovering the number by living through it.
> **Sanity:** 5.7× the worst post-cutover fleet drawdown replayed at the new tier (A3, −$6,150);
> 51 trading days to recover at $681/day. That recovery time is long, and it is *supposed* to be:
> a cap you can shrug off in a fortnight is not a cap.

> ### CAP 3 — single-day loss halt: **$8,000**  ← the one that actually protects you
> **Because:** Caps 1 and 2 are retrospective — they notice a drawdown after it has accumulated.
> A max-loss day is **instantaneous**: 0DTE, one gap, one afternoon. $8,000 = **A2, the worst
> single day this program has ever had at this tier (−$8,050 on 2026-06-11)**, rounded to the
> nearest thousand. Stated plainly: *the worst day you have already lived through, at this size,
> is the day the fleet stops.*
> **Sanity:** 1.9× the worst post-cutover day replayed at the new tier (A3, −$4,112) — it would
> not have fired on any day in the current sample; and it is **less than a quarter** of a full
> GF-family tail ($33,852), so it fires *while* a bad day is developing rather than after.

### Why three and not one
| Cap | Catches | Blind to |
|---|---|---|
| 1 · per-bot $15K | one bot bleeding steadily at size | seven bots bleeding together |
| 2 · fleet $35K | correlated slow bleed across the fleet | a single catastrophic session |
| 3 · daily $8K | the gap day | slow bleed that never has a bad day |

Each covers the other two's blind spot. Removing any one leaves a hole you can drive the whole
account through.

## 1.6 What signing this does to the readiness board
G4's `$` half becomes evaluable. Against **Cap 1 ($15,000)**, today: **no ON bot is anywhere near
it** — the worst post-cutover per-bot cumulative drawdown at the new tier is far inside $15K
(fleet-wide it is $6,150, A3). So **G4-$ passes for every bot on day one and changes no stage
today.** That is the correct outcome: the cap is a brake, not a re-scoring. It starts mattering
the moment the GF family runs at 26 ct.
⚠️ Implementing the `$` half is a `scripts/report.py` change — **Claude Code lane, not this one**,
and it is a code change to a repo-tracked file, so it is out of scope here by two rules.

## 1.7 The one input I cannot derive, stated rather than guessed
A cap expressed as **a percentage of your trading capital** is the form that would survive a
change in account size, and it is strictly better than three fixed dollars. I cannot derive it:
the only capital figures on any surface are **OA paper allocations** (`data/captures/…/07-…tsv`:
account ALLOCATION $2,145,000) which are not your capital and never were.
**I am not asking you to invent a cap** — the three above are derived and signable as they stand.
If you state a live-capital figure, all three convert to percentages in one pass and become
size-portable. Until then they are fixed dollars, correctly anchored, and they need re-deriving
after the next sizing epoch.

---

# PART 2 — T-40: breach playbook — ONE PAGE, DRAFT

> **Definition.** A **breach** is a position that has gone against the bot far enough that its
> outcome is no longer governed by its intended exit — or a day/bot/fleet loss crossing Cap 3 / 1 / 2.
> **Scope: paper.** Nothing here presumes live capital.

## 2.1 What happens by rule, in order — the position level
1. **The bot's own Exit Options fire, if it has any and they are ON.**
   ⚠️ `AUTOMATIONS` and `EXIT OPTIONS` are **two separate per-bot toggles**. Deactivation turns both
   off; resubscription restores **only AUTOMATIONS**, and the editor keeps displaying every Exit
   Option setting regardless — *"the toggle is the only place the failure is visible"*
   (`data/archive/README-v1-ledger.md`, the lapse mechanism). This is the failure that ran six
   invisible sessions in v1. **The toggle is the first thing checked on any breach, on every bot.**
2. **The automations-side backstop fires** — `GF-Backstop-1552-FlatClose` for the GF family, the
   per-bot equivalent elsewhere. v2 deliberately puts the backstop on the automations side
   *because* the Exit-Options toggle is the thing that dies.
   ⚠️ **The 15:52 timestamp is UNVERIFIED** — `docs/pre-registration-ledger.md` L344: the
   Market-close trigger is hard-coded to 15:50 and Exit Options stop one minute before close;
   whether a Repeating trigger reaches 15:52 is an open item. **Do not rely on the backstop as
   the sole line.**
3. **Else it goes to expiry.** For 0DTE that is the same afternoon and the loss is the full spread
   width less credit — **$4,836 per arm at 26 ct** (§1.3). There is no step 4.

**Standing exception, do not "fix" it mid-breach:** `IC-SPX-FastPT25-S2` and its `-130PM` clone are
**deliberately Exit-Option-free ride+S2 controls** (`CLAUDE.md` §5). Their EXITS toggle reading OFF
is correct, not a breach. Their only cap is the **S2 strike-touch monitor** on the automations side.
Re-arming them during an incident destroys the control and the comparison.

## 2.2 Who checks what, when a breach is noticed intraday
| When | Check | Surface | Never |
|---|---|---|---|
| **immediately** | Is the bot's `EXIT OPTIONS` toggle ON? And `AUTOMATIONS`? | the bot's own dashboard toggles | not the Exit Options *panel* — it displays settings whether or not they are live |
| **immediately** | Has the **excessive-errors failsafe** tripped? 10 errors in one day disables **all** that bot's automations; **re-enabling is manual**, and one further error the same day trips it again; the counter resets next trading day | homepage + the bot dashboard's "errors" (`docs/oa-platform-reference.md` §4.5) | assuming a silent bot is a gated bot |
| **immediately** | Is it actually a breach, or a correctly-gated bot doing nothing? | **bot logs.** A scanner run with no entry = healthy. **Zero log rows = presumed OFF or failsafe-tripped** (`oa-platform-reference.md` L418) | `SILENT_BOT` can never be RED on the strength of silence alone (`daily-loop-spec.md`) |
| **before acting** | Which account is this bot on? | the bot's own page, `ACCOUNT` field | the OA login also carries a live brokerage account (`TR ****4219`). Confirm **Paper Trading** before any intervention |
| **before acting** | Is it one bot or the family? | the other six GF arms | treating a family event as a bot event — §1.4 |
| **after** | Did every declared exit actually generate an order? | **the position's Trades list** | ⛔ the Exit Options panel is **NEVER** evidence (`oa-platform-reference.md` §0.3) |

## 2.3 Intervention authority
- **Claude may execute OA edits directly**, self-verified under the two-layer proof
  (`CLAUDE.md` §5, amended 2026-08-04): (1) an immediate independent re-observation of the changed
  value from OA itself — a save confirmation is never this check; (2) the behavioural check on the
  **first new position's Trades list**. Andy retains **revoke authority**, globally or per-bot.
- **A breach is not authority to retune.** Closing a position, or switching a bot OFF, is
  incident response. Changing sizing, strikes, filters or exits is a **decision** and stays gated
  behind "amend the plan" (`CLAUDE.md` §5, doc-edit authority). Do not fix strategy during a fire.
- **"No changes during streaks"** (`CLAUDE.md` §5) governs afterwards too: a breach is exactly the
  moment the rule exists to survive.

## 2.4 What gets captured, for the record — non-negotiable
1. **The position's Trades list**, full, before anything is closed. It is the only evidence of what
   actually executed; the panel is not.
2. **Both toggles**, screenshotted, for every affected bot — `AUTOMATIONS` and `EXIT OPTIONS`.
3. **The bot's automation logs** for the day (scanner runs, errors, error count vs the 10 failsafe).
4. **A fleet `/bots` roster capture**, pre- and post-intervention, same instrument, same parse,
   **diffed** — exactly the intended bots differ and nothing else. (The 08-31
   `10-authorized-edits` pattern.)
5. Everything to `data/captures/<ET-date>-breach-<bot>/` with `SHA256SUMS.txt`.
   ⚠️ **ET date from the capture's own page header, never the container clock** (the UTC trap).
6. A `docs/session-log.md` entry and a `data/lessons.csv` row. If the breach was caused or masked
   by a config fact that turned out to be wrong, that is an **evidence-backed correction** and
   follows `CLAUDE.md` §5's five conditions — never a quiet edit.

## 2.5 Cap-breach actions — what each cap actually triggers
| Trigger | Action | Who |
|---|---|---|
| **Cap 3 · single-day loss ≥ $8,000 (fleet)** | Switch **AUTOMATIONS OFF fleet-wide** for the remainder of the session. Do not close open positions on a rule — closing into a gap is itself a decision. Capture per §2.4. Resume next session only on Andy's explicit say-so. | Claude executes; Andy informed same day |
| **Cap 1 · per-bot drawdown ≥ $15,000 (epoch)** | That bot to **AUTOMATIONS OFF**. It is a **kill review**, not an automatic kill — the kill criterion in its pre-registration entry is the thing that kills it, and it is in R, not dollars. The $ cap stops it trading while the R question is answered. | Claude executes; entry reviewed at the next brief |
| **Cap 2 · fleet drawdown ≥ $35,000** | **Full stop.** All bots AUTOMATIONS OFF. No restart without a re-signed pre-registration sitting. This is the program-level circuit breaker. | Andy only |
| **Any cap breached** | It goes to the **top of every brief until closed** — the standing rule for an unverified fix (`CLAUDE.md` §5) applies to an open breach identically. | — |

## 2.6 Known gaps in this playbook, stated rather than papered over
1. **The 15:52 backstop is unverified** (§2.1 step 2). Until it is, step 2 is a hope, not a rule.
2. **Caps 1–3 are not code-enforced.** Nothing in `scripts/report.py` computes them today; the
   `$` half of G4 is still `<FILL>`. Until the Claude Code lane implements them, these are
   **human-checked at the daily brief** — and a criterion the loop does not produce is, by this
   project's own rule 2 (`pre-registration-ledger.md` §2), *not a criterion*. **Signing these caps
   creates a code task; it does not by itself create a brake.**
3. **No live-capital percentage** (§1.7).
4. **n = 16 trading days.** Every post-cutover figure here is **T5 by the evidence law** — far
   below the n≥100 / 6-month / regime-change bar. The v1 anchors (A1, A2) are larger-sample but
   pre-cutover, and are cited **as history only**, never as a claim about the current fleet.
   These caps are a *starting brake set by the best available evidence*, and they should be
   re-derived at n≥100.
