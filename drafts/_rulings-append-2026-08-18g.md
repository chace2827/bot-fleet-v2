```yaml
ruling_id: R-2026-08-19-TAPE-BACKFILL-AND-VIX-SERIES
date: 2026-08-19
scope: >-
  Four decisions from the tape-backfill investigation
  (/tmp/tape-backfill-package-2026-08-19.md, sha256 e089e653…), each premise
  verified against the tree (tape.py:357 skips the VIX series request;
  underlyings_on() reads trades.csv; no 08-12/08-13 tape files exist).
  (1) BACKFILL = READING A: the 2026-08-10 and 2026-08-11 tapes are
  backfilled from real Tradier data (which exists in full: SPX/QQQ/VIX daily
  OHLC + 5-min series; plain tickers), and 2026-08-12/2026-08-13 tapes are
  generated (they have ledger positions and no tape at all). Every
  backfilled file carries source per underlying set truthfully,
  backfilled_at, and backfill_evidence citing the raw API captures. The
  falsified banked facts are corrected with evidence: 08-10 pct_move
  sign-flip, the two hidden strike touches, and the one moved row
  (data/trade_window.csv 12-13,Chop touch_rate 0.0 -> 1.0), each cited to
  the re-run in the correction PR. URGENT FIRST STEP, before anything else:
  the raw Tradier API captures land as evidence files under
  data/captures/2026-08-19-tape-backfill/ with sha256s — Tradier's 5-min
  lookback rolls at ~57 days and 08-10 becomes unretrievable ~2026-10-06.
  (2) GUARD CHANGE PRE-AUTHORIZED per charter §4 (the package's §6.2):
  scripts/tape.py stops excluding VIX from the timesales request (the
  sym != "VIX" condition at ~:358); VIX gains a 5-min series in the tape
  like SPX/QQQ; no other generator behaviour changes.
  (3) Q3 AMENDED, not reversed: when the tape carries a VIX 5-min series,
  VIX gates evaluate directly at the entry window; the asymmetric/straddle
  rule of R-2026-08-19-GATES-SEMANTICS-Q1-Q3 remains the governing rule for
  any day whose tape lacks the series. Consequence recorded: PR-06's
  2026-08-14 row upgrades to JUSTIFIED (window move -1.03% vs gate -2.0%,
  first breach 13:25) when the enriched 08-14 tape lands.
  (4) SEQUENCING: the Phase-3 PR (build B) merges NOW against current tapes;
  the enrichment lands afterwards as ONE coordinated wave (evidence
  captures -> tape.py change -> backfilled + new tapes -> banked-row
  correction -> verdict-engine VIX-window path), each PR citing this ruling.
verbatim: >-
  Backfill and correct (A) with evidence preserved immediately; the VIX
  series guard change is pre-authorized; Q3 is amended so window data beats
  the asymmetric rule when present; B merges now and the enrichment follows
  as one wave.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  data/brief/2026-08-10..13 tape files (backfilled/created with provenance);
  data/captures/2026-08-19-tape-backfill/ (new evidence, lands FIRST);
  scripts/tape.py ~:358 (named guard change); data/trade_window.csv one-row
  correction with evidence; the Phase-3 verdict engine (VIX-window path
  follow-up); R-2026-08-19-GATES-SEMANTICS-Q1-Q3 (amended in scope, not
  superseded).
superseded_by: none
source: >-
  Tape-backfill lane package 2026-08-19 (PoC verified by full pipeline
  re-run in /tmp whose baseline reproduced trade_window.csv byte-identically
  before the correction); premises re-verified against the tree by the
  Cowork lane; Andy's four rulings in the Cowork session.
unclear: >-
  [UNCLEAR] Deliberately recorded: the backfill corrects INPUTS and the one
  proven-wrong derived row; whether any additional derived surface shifts is
  established by the wave's own re-runs, and any further moved row returns
  to Andy with evidence before it is committed.
```
