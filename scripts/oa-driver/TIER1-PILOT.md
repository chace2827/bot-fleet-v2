# Tier 1 pilot — prove the driver, on a dead bot

Written 2026-08-20. **Nothing in this file has been run.** It is the procedure, not a result.

**What Tier 1 is:** the verification half of `scripts/oa-driver/`. It serves the measurement
problem, not the throughput problem. The backtest sweep is Tier 2 and is deliberately parked —
see `docs/oa-internal-api.md` §7.

**What it settles:** one open hypothesis and one new instrument.

- ⚠️ **Hypothesis:** the runbook records that element-ref clicks silently no-op because OA's
  delegated handlers ignore a synthetic click, and the workaround is a JS `MouseEvent` chain
  (`isTrusted: false`). Playwright clicks via CDP input injection (`isTrusted: true`) — a third
  mechanism, distinct from both. **It may simply work.** Untested either way.
- **Instrument:** `save-automation`, which performs §5's Layer 1 across three independent
  surfaces instead of one.

**Pilot target: `QQQ-IC-0DTE-HedgeTest`.** Chosen because `data/bots_meta.csv` records it
`status=OFF`, `role=experiment`, `superseded=yes`, notes *"suspected dup of A/D; archive
candidate"* — and it appears **zero** times in `data/trades.csv` and **zero** times in
`RULINGS.md`. Nothing depends on it. Do not substitute a bot that has traded.

---

## Preflight

```bash
# Chrome, backgrounded, dedicated profile. Skip if already running.
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 --user-data-dir="$HOME/.chrome-oa-profile" \
  >/dev/null 2>&1 &
disown

cd ~/bot-fleet-v2/scripts/oa-driver
node oa_driver.mjs status
```

**Gate:** `status` prints JSON. If it errors, stop and read the error — do not work around it.

Now open `QQQ-IC-0DTE-HedgeTest` in that Chrome window and **copy its bot id out of the URL**
(`/bots/bot/BOT…`). That id is first-hand; do not take it from a CSV.

---

## Step 1 — baseline read (no risk, proves the read path)

```bash
node oa_capture.mjs bot BOT<paste-id-here>
```

**Gate:** writes a JSON model dump and prints a sha256. Record that hash — it is the pre-state.

---

## Step 2 — TEST A: does a trusted click land? ⭐ NON-MUTATING

This is the experiment that settles the hypothesis, and it changes **nothing**. The post-condition
is UI state, not saved data: before the click `a5.bots.acedit.routine` is absent; after a click
that lands, it is populated. A click that no-ops leaves it absent. Nothing is ever saved.

```bash
node oa_driver.mjs status                      # expect: "automationOpen": false
```

Dry run first. Use the automation's visible name — Playwright resolves `text=` selectors, so this
needs no DevTools:

```bash
node oa_driver.mjs click 'text=<exact automation name>'
```

**Gate:** the report must show `"count": 1`, `"visible": true`, `"hitTargetIsSelf": true`.
If `count` > 1 the script refuses — narrow the selector rather than indexing into a guess.
If `hitTargetIsSelf` is false something overlays it; do not force.

Then arm it:

```bash
node oa_driver.mjs click 'text=<exact automation name>' --allow-write --bot QQQ-IC-0DTE-HedgeTest
node oa_driver.mjs status                      # the post-condition
```

### Reading the result — record whichever happens

| `status` after | verdict |
|---|---|
| `automationOpen: true`, name matches | ⭐ **trusted click LANDS.** The no-op trap is a property of the old harness, not of OA. A large part of the trap catalogue is then UI-harness scar tissue, not app behaviour. |
| `automationOpen: false` | trusted click no-ops too. Re-run with `--method js`. If that lands, the trap is real and mechanism-specific — which is also a clean finding. |
| both fail | the trap is neither, and the selector or the open path is the thing to question next. |

**Then hard-reload the page.** Nothing was saved; the reload discards the opened editor and
restores a clean page life (§5 trap 6 — never carry a second automation into one page life).

⛔ Whatever happens, this is **one observation on one bot**. It licenses a note in the session log,
not an edit to the runbook or the `oa-driving` skill. Those change after it reproduces.

---

## Step 3 — TEST B: the three-surface save. Only if A passed.

B tests the *instrument*, not the click. Make the edit by hand so the only thing under test is the
commit-and-verify path.

1. Open one automation on `QQQ-IC-0DTE-HedgeTest`.
2. Change **one** trivial value by hand (a profit-taking % by one point is enough). Do **not** save.
3. Capture the pre-state hash:

```bash
node oa_driver.mjs hash          # record this
```

4. Dry run, then arm:

```bash
node oa_driver.mjs save-automation
node oa_driver.mjs save-automation --allow-write --bot QQQ-IC-0DTE-HedgeTest
```

It clicks `a.saveclose` — the real commit, not the drawer Save (§5 trap 7) — watches for OA's POST,
hard-reloads with `beforeunload` **observed rather than dismissed** (trap 8 read as an oracle), and
re-hashes.

### Reading the three surfaces — together, never separately

| network POST | beforeunload | hash | reading |
|---|---|---|---|
| 2xx | silent | changed | clean save |
| 2xx | **FIRED** | changed | ⛔ **not** a clean save — uncommitted state still existed at reload |
| NOT OBSERVED | silent | changed | saved; we simply did not see the call. Absence of an observation is not evidence of absence |
| any | any | unchanged | the edit did not persist, whatever the tool reported |

The script prints all three and refuses to blend them into a verdict. That refusal is the design.

⛔ **Layer 2 is not satisfied by any of this** and is not owed here, because a superseded OFF bot
will never open a position. The moment this procedure is used on a live bot, the first new
position's **Trades list** is still the second layer. The Exit Options panel is never evidence.

---

## Step 4 — record, then stop

Append to `docs/session-log.md`: the bot id, the selector used, each command's output hash, the
Test A verdict verbatim, and the three surfaces from Test B. Then hand off for commit — Cowork does
not run git (`CLAUDE.md` §9.1a, and see the gitdir move to `~/gitstore`).

**Do not** amend `docs/oa-ops-runbook.md` §5 or the `oa-driving` skill on one run. A trap recorded
from repeated experience is not overturned by a single green result — reproduce it on a second dead
bot first.

---

## What Tier 1 does not do

- No backtest sweep. Parked; `docs/oa-internal-api.md`.
- No live-bot edits. This proves the instrument on something inert.
- No runbook edits. Those follow reproduction.
- Nothing here fixes the 130-row triage queue, the blind `check_refs`, or the roster invariant gap
  — which remain the actual constraints this phase.
