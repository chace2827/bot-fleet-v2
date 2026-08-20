# Capture bundle — 2026-08-19 roster + toggle state

Purpose: the end-of-day `/bots` roster capture for trading day **2026-08-19**, taken as part of
the daily loop (CLAUDE.md §2). It is the second capture in the `roster-toggles-44` series and the
first drift check against the 2026-08-17 R-3 bundle, which `docs/roster-mechanics-ruling.md` §2.5
made the roster authority.

Captured by Andy, **Wed Aug 19 2026 21:17:33 GMT-0400** (page clock 9:17PM), `/bots`, all groups.
Bridge session; no OA writes, no config edits, nothing toggled.

## Files

| file | sha256 | what it is |
|---|---|---|
| `01-bots-roster-recent-activity-2026-08-19-211733.txt` | `b4738278e6e2dde2d20d902c4e4b5ac59e7f5c36aaaa05ce92798c19babb6b9b` | RAW bookmarklet capture, unmodified. 44 list rows + the 44-row `i.sticon[title]` AUTOS/EXITS block (S0b-3 fix v2.1). |
| `02-roster-toggles-44-2026-08-19.tsv` | `fb62fa7b5643630a2241f03df72d8e6596a56fb56f67711d3897c82e3c0a7fbd` | DERIVED join of the above into `bot_name / bot_id / AUTOS / EXITS`. Its header states the method and the join proof. |
| `screenshots/01-bots-roster-2026-08-19-211733.pdf` | `da1756a2b8b9fea86301c1f2fc622209017bd7aa553b2fa63cd0540f7c2d27bf` | FireShot full-page `/bots` capture, same instant. PDF, not PNG. |

⭐ **This bundle satisfies both halves of §2.5** — bookmarklet text **and** an image of the roster —
which the 2026-08-17 R-3 bundle did not (its screenshots were supplied in chat and never committed).
The image is a PDF rather than the `.png` named in `oa-ops-runbook.md` §1.6; the text block is the
evidence either way, and §1.6's screenshot requirement is for per-bot toggle state, which the
`title`-attribute block already carries as text.

## The OA Export Data CSV is not duplicated here

Tonight's export is committed at `data/raw/2026-08-19.csv` and is cited by that path, not copied.
It carries **no** AUTOS/EXITS field; all toggle state in this bundle comes from the `title` block.

## Closing state

- footer, verbatim: `44 active bots • 6 left in your plan • Upgrade`
- rows parsed: 44 · **AUTOMATIONS ON: 19 of 44** · **EXIT OPTIONS ON: 16 of 44**
- **DRIFT vs 2026-08-17: ZERO.** Not one bot changed either toggle across two trading days; the
  19/16 membership is identical, bot for bot. No unexplained arming, no silent disarm.
- RIDE BOTS: `QQQ long call` and `Tasty Condor` both OFF/OFF — **gate A6 still intact.**
- The Exit-Option-free controls (`IC-SPX-FastPT25-S2`, `-130PM`) remain EXITS OFF, as designed
  (CLAUDE.md §5 standing exception).
- `IC-SPX-Fortress-Unstopped` (INC-01): AUTOS ON / EXITS OFF, unchanged — `disableExits 1` holds.
- The three `-ARCHIVED-` bots: present, OFF/OFF.
- PILOT PR-03 `QQQ-IC-0DTE-Fortress`: OFF/OFF. Unsigned by ruling. Expected.

## ⛔ FINDING — an unsigned bot is armed, and has been for at least two trading days

`QQQ-IC-0DTE-Fortress-NoPT50` reads **AUTOS ON / EXITS ON** in this capture and in the 08-17
capture. It is listed under **UNSIGNED PRE-REGISTRATION BOTS — DO NOT SWITCH ON** in `STATUS.md`.
Two independent first-hand captures, 48 hours apart, agree.

Its roster row shows every performance column as `--` — no P/L, no closed count, no win rate — so
it is armed but has not filled. The exposure is prospective, not realised. Not ruled here; it needs
either a signature or a disarm.

## ⚠️ Method note — the join proof caught a real error

The first derivation of `02-*.tsv` skipped the title block's first data row, shifting every name
onto the next bot's id. It produced a plausible-looking file reporting **12 toggle changes**, all
false. The 44/44 cross-check against the 08-17 map is what surfaced it. A positional join is not
self-checking; do not ship one without the proof.
