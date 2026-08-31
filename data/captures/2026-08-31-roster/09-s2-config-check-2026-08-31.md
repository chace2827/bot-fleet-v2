# IC-SPX-FastPT25-S2 (11AM) — read-only config check (dispatch task F)
Captured 2026-08-31 ~17:44–17:52 ET, Claude in Chrome. READ-ONLY, no edits, nothing toggled.
Bot: IC-SPX-FastPT25-S2  BOTfw5TkkCRF4417860821948715488

## Q: did anything change ~08-28–08-31?   A: NO. Zero config delta.
Bot page header: ALLOCATION $50,000 · BOT GROUP IC-Focus · AUTOMATIONS ON · EXIT OPTIONS **OFF**
  (the standing exception, CLAUDE.md §5 — deliberately Exit-Option-free) · BOT VERSION 1, Aug 7 2026.
Safeguards: DAILY POSITIONS 2/day (2 used today) · POSITION LIMIT 2 at once · Scan 1m.
Automations: 4, all "Automation is on" —
  SCANNERS Scalp-Scan-Put, Scalp-Scan-Call · MONITORS Scalp-Mon-S2-StrikeTouch, Scalp-Mon-S2-Cleanup

Config hashes re-read live (sha256 over {name,inputs,root}, fresh open, hard reload between each)
vs the 2026-08-07 baseline recorded in data/bots_config_v2.csv line 227 and
docs/pre-registration-ledger.md PR-01:

  Scalp-Scan-Put            f83ed32bb24c0bc20e703164d68d309e1423d5be9069cc577fafb434aaf1c52f  (v4) MATCH
  Scalp-Scan-Call           892ba0c9fb7dfbfa038d95eec9ed953a91e25acc12a44f7c0aee1c960755bfa7  (v5) MATCH
  Scalp-Mon-S2-StrikeTouch  01af4963aafb58566789662aafa68d94d846d042869590eccbede9fb6d57ca85  (v4) MATCH
  Scalp-Mon-S2-Cleanup      f3673f2991541420c7124f3a6d2e2a2996002f6c61dc61ac8389ea348db2ccd7  (v2) MATCH

4 of 4 byte-identical. Nothing was edited on this bot between 2026-08-07 and 2026-08-31.

## The 08-31 "anomaly" is not an anomaly — it is the rule, seen from the other side
Scalp-Mon-S2-Cleanup, node text read verbatim from the model:
    ALL of:
      posopentime :: "Position has been open 2 minutes or more"
      countpos    :: "Bot has exactly 1 position with any type and open status"
    -> YES: closepos, 100% of position

Cleanup fires ONLY when the bot holds EXACTLY ONE open position.
  - One side fills  -> count == 1 -> the leg is scratched ~2 minutes after entry.
    This is the "puts-only 11:01->11:03 scratch" of review finding F-6.
  - Both sides fill -> count == 2 -> the guard fails, nothing closes, the condor rides to
    expiration. 2026-08-31: both SPX sides expired at full profit, +$100 / +$100 = +$200,
    risk $4,900/side (see /positions/closed, 08-31 "Expired").
  - Log 08-31 (08-s2-log-2026-08-31.txt): both monitors loop every minute through 3:55PM with
    no close action — consistent with the count==2 branch, not with a changed config.

## Consequence for F-6
The defect is NOT "the exit mechanism is broken" and NOT "puts-only exits". The Cleanup monitor
is behaving exactly as built: it destroys any UNPAIRED leg after 2 minutes. The failure upstream
is that the CALL SIDE does not fill on most days (3 of 14 bot-days two-sided). Fixing the exit
would be fixing the wrong end; the question to put to the scanner pair is why Scalp-Scan-Call
fills on ~1 day in 5.
NOT A DECISION — recorded for Andy. No edit proposed here; PR-01 is DRAFT/unsigned.
