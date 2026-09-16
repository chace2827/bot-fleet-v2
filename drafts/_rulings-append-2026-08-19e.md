```yaml
ruling_id: R-2026-08-19-TRADE-ID-STABILITY
date: 2026-08-19
scope: >-
  F-7. scripts/build_ledger.py:701 seeds `tid = max_existing_tid(day)` from
  the PERSISTED accumulator (hedge_tournament.csv + trades.csv, excluding the
  day being rebuilt) and then assigns ids in EXPORT ROW ORDER across a FULL
  rebuild of every day. The OA export is ordered newest-first, so every run
  renumbers every position. MEASURED between 6d5f1e8 and 7e5b715: all 45
  pre-existing positions changed id in the 2026-08-18 run; T00075 became
  T00195 and T00075 no longer exists. The banked result is that trade_id now
  runs BACKWARDS against time with interleaved per-day ranges — 2026-08-10
  holds T00182-T00196 while 2026-08-18 holds T00155-T00157.
  EXPOSURE, measured: docs/RULINGS.md cites ZERO trade_ids, so the register
  is clean. 22 of 23 trade_ids cited across docs/*.md are dangling; most sit
  in dated forensic history, but docs/evidence-standards.md:387 reads as a
  LIVE assertion ("exactly two false positives on clean wins — T00038 and
  T00339") keyed on ids that do not exist, and T00179 is worse than dangling
  because it RESOLVES, to a different position. data/hedge_tournament.csv,
  which is committed and ACCUMULATES across runs, carries 8 distinct
  trade_ids of which 7 are not in the current ledger — and it is also the
  file that seeds the counter, so the counter is seeded from ids that are
  themselves stale. Nothing is lost: that file carries open_date, bot,
  short_put and short_call, so its rows are reconstructible from content.
  ⚠️ THE REPO ALREADY RULED THIS ELSEWHERE.
  docs/comparative-machinery-spec.md:111 states that trade_id "is never
  persisted… not stable across runs" and that any cached set, anomaly log or
  exclusion log "keys on (bot, open_date, short_put, short_call), never on
  trade_id". build_ledger's design silently violates the spirit of a rule
  this repo wrote down for another subsystem. This ruling propagates it.
  Ruled: (1) IDS FREEZE. A named guard change per charter §4 is
  PRE-AUTHORIZED at this scope: on rebuild, a position already present in the
  PRIOR data/trades.csv KEEPS ITS EXISTING trade_id, matched on position
  CONTENT — the leg set's (bot, open_date, symbol, structure, short_put,
  long_put, short_call, long_call, quantity). Only genuinely new positions
  draw from the counter, and the counter is seeded above every id reused, so
  a new position can never collide with a frozen one.
  (2) ⛔ AMBIGUITY IS LOUD, NEVER A GUESS. If two prior positions share a
  content key, or a content key matches no prior position when one was
  expected, build_ledger REFUSES with nothing written, naming the key and
  both candidates. A wrong id silently reused is worse than the churn this
  ruling fixes.
  (3) THIS DOES NOT MAKE SCRATCH RUNS REPRODUCIBLE, and must not be claimed
  to. A scratch root with no prior trades.csv still numbers from its own
  counter. Ids become stable within a LINEAGE, not globally. Cross-root
  comparisons therefore still blank the trade_id column before comparing —
  the four-outcome acceptance pattern the foreman lane adopted stands and is
  endorsed here: accepted+identical passes; accepted+differs-only-in-trade_id
  passes as F-7, proven by blanking the column; accepted+differs-elsewhere
  STOPS; refused STOPS. ⛔ Reseeding a scratch root until hashes align
  manufactures a pass and is forbidden.
  (4) TRADE_ID IS NON-REFERENTIAL, STANDING. It is a within-run, within-
  lineage join key. It is never cited in a document as a stable reference to
  a position, and no persisted artifact keys on it. Persisted artifacts key
  on (bot, open_date, short_put, short_call) per the existing spec.
  (5) NOT REPAIRED HERE, NAMED SO IT IS NOT A LATER STOP:
  data/hedge_tournament.csv's 7 orphaned trade_ids stay as committed. Its
  content columns are the real key and the rows are reconstructible from
  them; rewriting banked rows to match a later convention is the retroactive
  edit this project refuses. The column is decorative in that file from here.
  (6) THE DOC SWEEP IS A SEPARATE CORRECTIONS PR with evidence per citation:
  live assertions convert to content keys, dated forensic history is marked
  as historical and left standing. docs/evidence-standards.md:387 is the one
  identified live assertion. Not in this PR.
  (7) KNOWN-POSITIVE REQUIRED: a fixture rebuilding a day whose positions
  already exist asserts every id UNCHANGED; a fixture adding one new position
  asserts the existing ids unchanged and the new one above them; a fixture
  with a duplicated content key asserts the REFUSAL with nothing written.
  Bounds: scripts/build_ledger.py and its self-test. No change to
  data/hedge_tournament.csv, to any doc, to the export, or to any verdict.
verbatim: >-
  Freeze the ids — a position that already exists keeps its number, only new
  positions draw from the counter, and ambiguity refuses rather than guesses.
  And trade_id is a join key, not a reference: never cite it in a document,
  never key a stored file on it. This does not make scratch runs reproducible
  and nobody may claim it does.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  scripts/build_ledger.py max_existing_tid()/the pairing block at :701-717
  and its self-test (named change, cites this ruling);
  docs/comparative-machinery-spec.md:111 (the existing rule, now propagated
  fleet-wide, unchanged); data/hedge_tournament.csv (orphaned ids named and
  NOT repaired); docs/evidence-standards.md:387 and the other dangling
  citations (queued to a separate corrections PR); the scratch-comparison
  acceptance pattern used by the foreman lane.
superseded_by: none
source: >-
  Rulings-lane investigation 2026-08-19 against master 7e5b715, prompted by
  the foreman lane's F-7 report of a +42 trade_id offset. Measured by
  diffing data/trades.csv between 6d5f1e8 and origin/master on a content key
  (45 of 45 positions renumbered), by counting trade_id citations across
  docs/*.md against the live ledger (22 of 23 dangling), and by intersecting
  data/hedge_tournament.csv's trade_ids with the current ledger (7 of 8
  orphaned). Andy's ruling in the Cowork session.
unclear: false
```

```yaml
ruling_id: R-2026-08-19-LANE-STATE-OWNERSHIP
date: 2026-08-19
scope: >-
  On 2026-08-19 a report describing origin/master as 02ee43c — 38 commits
  stale — was read as belonging to the foreman lane when it came from the
  guard-adversarial lane. The rulings lane compounded it by drafting a
  correction against the wrong lane, having verified the report's CONTENT
  and not its PROVENANCE. Root cause, diagnosed by the foreman lane and
  accepted: ~/.claude/primer.md is read by every Claude Code session in this
  repo, was overwritten by the guard-adversarial lane, and pins a stale
  origin/master with carryover about another lane's PRs. That file has now
  caused two distinct failures — a D2 agent clobbering it (2026-08-18) and
  this cross-lane confusion — and it is a CONFIRMED CONTAMINATION VECTOR.
  Ruled: (1) ⛔ NO LANE AND NO AGENT WRITES ANYTHING UNDER ~/.claude/.
  Already a standing guardrail in every write-dispatch prompt; it is now a
  ruling. The prohibition covers primer.md specifically and the directory
  generally. Reading it is permitted; nothing read from it is evidence.
  (2) EACH LANE OWNS ONE TRACKED FILE: docs/lane-state-<lane>.md. No lane
  writes another lane's file. It is versioned, reviewable in a PR, survives
  session death, and cannot be silently clobbered the way a dotfile can.
  Minimum contents: the base sha the lane believes it is working from and
  when that was last verified against origin/master; open PRs it owns;
  findings it has raised that are not yet ruled; and what it is holding for.
  (3) ⛔ A LANE-STATE FILE IS A CLAIM, NOT EVIDENCE. Every lane re-verifies
  against origin/master at the start of a session and before any dispatch,
  branch or merge — `git fetch origin && git rev-parse origin/master` — and
  states the result. A stale base is the P2-5 failure class; that near-miss
  was 4 commits and was caught in pre-flight, this incident was 38.
  (4) PROVENANCE IS PART OF A CLAIM. When a report is relayed between lanes,
  the lane it came from is stated. An unlabelled report is treated as
  unattributed and its provenance verified before any reply is drafted
  against it — the rulings lane's error here, recorded so it is not repeated.
  (5) The Cowork rulings lane's durable state remains its project memory,
  which is outside the repo and outside this ruling; it gains no
  docs/lane-state file. The foreman lane gains
  docs/lane-state-foreman.md.
verbatim: >-
  Nobody writes under ~/.claude — it is a proven contamination vector. Each
  lane keeps its own tracked state file in the repo and does not touch
  another's. And a state file is a claim: verify against origin/master before
  you act, and say which lane a report came from.
verbatim_of: andy
owner: Andy
status: Active
applies_to: >-
  ~/.claude/primer.md and the ~/.claude/ directory (write prohibition, all
  lanes and all agents); a new tracked docs/lane-state-foreman.md; every
  write-dispatch prompt's guardrail set (the ban is now cited as a ruling);
  the pre-flight discipline in R-2026-08-17 era practice and
  [[devin_dispatch_discipline]]; the Cowork rulings lane is excluded from the
  lane-state file requirement.
superseded_by: none
source: >-
  The 2026-08-19 cross-lane misattribution incident: a 38-commit-stale report
  (02ee43c vs origin/master 7e5b715, verified by git rev-list --count),
  attributed to the wrong lane by the rulings lane, corrected by the foreman
  lane which identified the overwritten primer as the shared surface. Andy's
  ruling in the Cowork session.
unclear: false
```
