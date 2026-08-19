# Migration tracker — disposition of the 44 open items
**2026-08-19 · RULED BY ANDY · supersedes the "parking lot" draft of the same date**

Source: `bot-fleet-migration` artifact.

> **⛔ CORRECTED 2026-08-19 (same day, before commit).** The first pass of this document said
> **136 items / 92 done / 44 open**. That was wrong. The parse used one regex over a file that
> mixes two literal styles (`w:"CLAUDE"` and `"w": "CLAUDE"`) and silently under-matched the
> JSON-quoted form. Re-parsed permissively and checked against a second derivation (per-phase
> split vs whole-file count, which disagreed and exposed the bug):
> **201 items · 132 done · 69 open**, across **15 phases, not 13.**
> Two phases were invisible to the first pass — `e3impl` (5 items, 1 open) and
> **`agentconv` — "Agent conversion & governance", 34 items, 21 open.**
> The ruling below is unchanged; the arithmetic around it is restated in §Disposition.
> *Lesson, already in the project's own doctrine: two agreeing derivations are weaker than one
> checked against a different surface. Here they disagreed, which is the only reason this was caught.*

## Ruling — 2026-08-19 (Andy, explicit)
1. The 11 superseded clean-slate-sweep items **STAY LIVE AT LOW PRIORITY**. Not retired.
2. They are **ADDED TO THE BOARD** (program **P9 · OA Platform & Account**, priority Low).
3. The `bots_config_v2.csv` staleness is **CORRECTED** — applied to `CLAUDE.md` §3.2 and §6
   the same day under §5 evidence-backed-correction authority.

The placeholder item *"re-rule the clean-slate sweep against the actual 19-ON / 44-row roster"*
is **withdrawn** — this ruling is that decision.

## Disposition — all 69 accounted for

| Disposition | Count |
|---|--:|
| Re-homed to programs P1–P9 at normal priority | 33 |
| Added to **P9** at **LOW** priority (list A below, plus the Phase-2 twin) | 12 |
| Closed — stale or already answered (list B below) | 2 |
| **Duplicates of `todo-2026-08-16.csv` items already on the board** (the `agentconv` phase) | 17 |
| **New items found only in `agentconv` / `e3impl`** (list C below) | 5 |
| **Total** | **69** |

### ⭐ What the `agentconv` phase actually is
It is a **second copy of the todo CSV**, carrying the same T-numbers — and in four cases a
**fresher status**: T-01, T-04, T-10 and T-21 all read *in progress* there while the CSV still
says OPEN. This is the duplicate-authority failure the charter exists to stop, and **T-21 is the
open task that names it.** On the board these merge to one row each; the tracker's status wins
because it is newer. That merge is why 69 open tracker items become 52 board rows, not 69.

---

## A · Live at LOW priority — P9 · OA Platform & Account — 11 items

Phase 4 targeted "35 roster bots → ≈18–20 active". `bots_meta.csv` reads **44 rows / 19 ON**:
the end state was reached via the 08-07 restore plus greenfield builds, not via this sweep.
These therefore gate nothing, but they remain real roster hygiene and stay open.

1. DELETE the zero-trade bots (2 known, capture-determined) — [CLAUDE]
2. Archive the 2 SPX Fortress arms — [CLAUDE]
3. Archive the 2 unverified QQQ Fortress variants — [CLAUDE]
4. Archive the 5-bot QQQ hedge family — [CLAUDE]
5. Archive the 3 QQQ controls — [CLAUDE]
6. Archive the 4 old Range075 experiments — [CLAUDE]
7. Archive the 3 killed mirrors — [CLAUDE]
8. Archive DIR-SPX-Put-Control — [CLAUDE]
9. Write `data/archive/rename_map.csv` as the sweep runs — [CLAUDE] · in progress
10. Confirm the 2 directional bots untouched — [CLAUDE]
11. Confirm the 7 live mirrors untouched — [CLAUDE]

## C · New — found only in the phases the first pass missed — 5 items

Not in `todo-2026-08-16.csv`. All five are now on the board.

- **T-29** · Merge the gate — PR #3 plus branch protection — [ANDY] → **P6**
- **T-30** · Rule the Reconciler IN (`roles-and-ingredients.md` row 10) — [ANDY] → **P7**
- **T-31** · Build the Reconciler — daily read-only contradiction report — [CLAUDE] → **P7**
- **G-4** · Re-key `hedge_tournament.csv` on the natural key — [DEVIN] → **P4**
  *(this one gates P4's own metric: unjoinable rows are why the tournament cannot select)*
- **E3-1** · E-3 §3.3 — three items gated, nothing decided by that session — [ANDY] → **P7**

## B · Closed — 2 items

12. Build `data/bots_config_v2.csv` from captures — [CLAUDE] · was BLOCKED
    → **DONE.** File exists: 246 data rows, sha `e54ee4ea9f3bfa7d…`, header line 1 reads
    `# bots_config_v2.csv — POST-CUTOVER config record. Built ONLY from capture, never hand-written`.
    Direct device read 2026-08-19.
13. Decide Notion's role in v2 — [ANDY]
    → **DECIDED 2026-08-19.** Notion is demoted to **P8 · The Business only**. Boundary rule:
    work whose evidence is a file lives in git; work whose evidence is a conversation, a bank
    balance, or a signature lives in Notion.

---

## Consequent — tracker freeze

With all 44 dispositioned, the `bot-fleet-migration` artifact **freezes read-only as the
rebuild's history**, the way `history-index.md` treats v1. One authority per kind of work
(cf. open **T-21**, the duplicate-authority task). The board is the forward queue from here;
the tracker is the record of how the rebuild happened.

## Correction record — `CLAUDE.md`, applied 2026-08-19 under §5

| | |
|---|---|
| Anchors | §3 item 2 (source-of-truth hierarchy) · §6 File map, `data/` paragraph |
| Falsified claim | "`data/bots_config_v2.csv` (not yet written — Phase 2)" · "Not written yet: `bots_config_v2.csv`, `mirror_baseline.csv`" |
| Evidence | Dated first-hand device read 2026-08-19 — `bots_config_v2.csv` 246 data rows, sha `e54ee4ea9f3bfa7d…`; `mirror_baseline.csv` 10 data rows, sha `cdceb0a8d444e570…` (matches the pre-existing §3 banner) |
| Form | Dated `[CORRECTED 2026-08-19 …]` banner; original text left standing / struck, not removed |
| Verification | `CLAUDE.md` sha `9f0f0d8c15b1e23d…` → `96bade2fb8df2b50…`; single-match grep on both banner strings |
| Decision changed | **None.** Both edits state file existence only. |

Andy may reject this correction at commit review (§5, veto moves to commit review).
