# SIZING POLICY SESSION — Opus chat (Cowork, bot-fleet-v2 connected) — drafted 2026-08-31

Paste into a NEW Opus Cowork chat with the bot-fleet-v2 folder connected:
"Read `_dispatch-2026-09-01-sizing-policy-cowork.md` in ~/bot-fleet-v2. Produce the six
deliverables. DRAFT-ONLY session: no OA edits, no repo-tracked-file edits, no commits — outputs
are `_*` draft files at repo root + chat tables. Andy signs before anything executes."

## Andy's stated intent (2026-08-31, Fable chat) — the anchor for everything
Realistic wager ≈ **$5K per leg → ≈$10K total per bot** (both sides). Harmonize the fleet on
**RISK PER POSITION**, not allocation. He is done with $7 opens / $1 closes on the GF arms.

## Inputs (read all before drafting)
- `docs/pre-registration-ledger.md` — the frame's sizing ladder (lines ~82-83: "1 lot
  (experiment) | ≈$5K risk/position (CANDIDATE+). Set once, never ad hoc."), the GF arms' own
  "1 lot per arm until one clears its interim read" MAX LOSS clauses, the $10K SPX/QQQ sleeve
  daily-aggregate caps, and the mirrors' "Do not resize a watch-only bot" lines.
- `data/captures/2026-08-31-roster/07-allocation-and-groups-2026-08-31.tsv` (current allocations
  + groups, verified) and `10-authorized-edits-2026-08-31.md` (3DTE $5K→$10K already applied;
  its POSITION SIZE is 26%-of-net-liquid — allocation is NOT position size, the canonical trap).
- Post-backfill `STATUS.md` readiness board (stages/gates per bot) and
  `_review-2026-08-31-vacation.md` (current per-leg risk figures: GF ~$193, FastPT25 ~$4,900,
  NoPT50 $4,940, DIR ~$650, mirrors various).

## Deliverables
1. **Sizing policy draft ruling** — one fleet ladder: which stage gets which risk/position;
   whether the GF "1 lot until interim (n=60)" clause is amended to the $5K tier now, or to an
   intermediate step; what happens to the $10K sleeve aggregate caps (7 GF arms × $5K ≈ $35K/day
   — the caps MUST be explicitly re-ruled or the amendment contradicts standing entries).
2. **Per-bot target table** — every ON bot + GF family: current risk/leg (derived from the
   export, never guessed), target risk/leg, the OA lever that gets there (contract count in
   which scanner action / allocation / % sizing), and epoch-note y/n. A/B families move
   IDENTICALLY or not at all.
3. **Mirrors recommendation** — default NO resize (watch-only rule + mirror fidelity), stated
   explicitly; plus the one-line exception ruling text for the already-applied 3DTE change.
4. **OA groups/tags audit** — groups are 44/44 as of 08-31; check group membership vs the
   FAMILY_RULES taxonomy and propose any tag/label scheme worth having. Small; don't gold-plate.
5. **Execution paste** for a follow-up OA session: per-bot edits with the verified-edit protocol
   (hash before/after; a version bump is not evidence), one family per batch, fleet pre/post
   capture diff as the outer check (the 08-31 pattern).
6. **Rulings drafts** ready for Andy's signature (amendment texts + epoch notes), as
   `_rulings-draft-2026-09-01-sizing.md`.
7. **G4 RoE $ cap proposal + breach playbook draft.** Andy does NOT know what cap to set —
   DERIVE a proposed cap from his own data, don't ask him to invent one: the champion's observed
   maxDD-R (-0.68 at n=16), the archived predecessor's -$11.2K/364-close record, and the
   tail-risk math (one max loss ≈ 1.7 winning days at current tier — recompute at the NEW tier,
   since the sizing change moves this). Present it as "cap = X because Y", sized in the new
   tier's dollars, for approve/adjust. Plus a ONE-PAGE breach playbook draft: what happens, by
   rule, when a position goes against a bot today (exit config → else expiry; who checks what
   when a breach is noticed intraday; what gets captured for the record). Both ride the same
   signature sitting as the sizing ruling.

## Discipline
"Set once, never ad hoc" — this session exists so sizing changes happen ONCE, by signature,
fleet-wide. Derive every current figure from a file surface (export / TSV / ledger), cite it,
and state derivations in any acceptance language — no literals. Nothing executes here: OA edits
happen in a separate session after signature; repo records ride the nightly close commit.
