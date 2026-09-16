# `scripts/oa-driver/` — driving OA from a script instead of a per-call browser tool

Drafted in Cowork 2026-08-19. **Code is Claude Code's lane (`CLAUDE.md` §7)** — a working
starting point, not a maintained module. Nothing is committed; hand-off is Andy's.

> Renamed from `scripts/oa-playwright/` on 2026-08-19: the read path contains no Playwright,
> and after the write path was added the folder holds both. `oa-driver` describes both.

---

## 1. Two paths, on purpose

| | Read path | Write path |
|---|---|---|
| File | `oa_capture.mjs` | `oa_driver.mjs` |
| Stack | **Raw CDP.** Zero dependencies — Node 22's global `fetch` + `WebSocket` | **Playwright** (`playwright-core`, attaches to your Chrome, downloads no browser) |
| Does | roster capture, bot model dump, config hash | clicks, saves, network recon |
| Default | runs | **dry run** — clicks nothing without `--allow-write` |

Reads stay on raw CDP because a read is one `Runtime.evaluate` and a dependency buys nothing.
Clicks moved to Playwright, and **not because Playwright can click** — raw CDP clicks too,
via `Input.dispatchMouseEvent`. It is what surrounds the click:

1. **Locators re-resolve on every action.** §5 trap 6 — two automations open in one page
   life, node queries return the *previous* automation's cards, a click edits the wrong
   automation **silently** — is a stale-handle bug. A locator has no handle to go stale.
   This is the trap that could do real damage, and it is the one the dependency retires.
2. **Actionability + hit-target test.** Before clicking: visible, stable (bounding box
   unchanged across two animation frames), enabled — then Playwright verifies the point it
   is about to hit actually resolves to the target. That is trap 1 (overlays mid-animation)
   and the "`Delete` sits ~29px below `Archive`" hazard, checked automatically rather than
   by discipline.
3. **Network as a second surface.** `waitForResponse` turns "did the save commit?" from an
   inference off the Leave-site guard (trap 8) into an observation of OA's own POST and
   status. Per [[verification_surfaces]], a second surface beats a second derivation.
4. **Traces.** Every action gets a screenshot, DOM snapshot and network log in one file —
   a §9.1a evidence artifact per edit, produced automatically.

### ⚠️ One hypothesis this exists to test — do not cite it as fact

The skill records: *"Element-ref clicks silently no-op on this app. The app binds delegated
handlers and ignores the synthetic single click."* The documented workaround dispatches a JS
`MouseEvent` chain — which produces `isTrusted: false` events.

Playwright clicks through CDP `Input.dispatchMouseEvent`: injected at the browser's input
pipeline, **`isTrusted: true`**, indistinguishable from a human hand. That is a *third*
mechanism, different from both the extension's element-ref click and from the JS chain. It
may simply work where both failed — or it may not.

`--method trusted|js|both` exists to settle it **on a dead bot**, with the result logged.
Until that runs, no claim either way.

---

## 2. Safety model for the write path

- **Dry run is the default.** Without `--allow-write`, `oa_driver.mjs` runs every
  actionability check, prints exactly what it *would* click, and clicks nothing.
- `--allow-write` additionally requires `--bot <id|name>`, and the script **reads
  `a5.bots.bot` and refuses if the page disagrees with the name you gave**. Fat-fingering
  the wrong tab cannot become an edit.
- Refuses to operate off `app.optionalpha.com`. Refuses ambiguous selectors (never indexes
  into a guess). Refuses to click an occluded element.
- Tracing is always on for a write. A write with no trace file is not a write this script
  performed.

**None of this replaces §5.** Layer 1 is automated below and is stronger for it; **Layer 2
— the first new position's Trades list — is a live-market observation and nothing here
shortcuts it.** The Exit Options panel is still never evidence.

---

## 3. Setup

```bash
# once: Chrome with a dedicated profile (136+ requires the separate --user-data-dir)
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 --user-data-dir="$HOME/.chrome-oa-profile"
# log into Option Alpha in that window

cd ~/bot-fleet-v2/scripts/oa-driver && npm i    # playwright-core only, ~50MB, no browser download
```

`node_modules/` and `data/receipts/traces/` were added to `.gitignore` — check that edit at
commit review.

---

## 4. Backtesting — read this before scripting a single click

**The backtest UI is not scriptable from this repo, and guessing at it would be inventing
evidence.** `docs/backtest-ingest-protocol.md` is a *paste* protocol: you screenshot the
Compare page, screenshot each column's Details, and download `positions.csv` by hand.
`oa-platform-reference.md:47` lists the June 2026 backtester as UI-research-pending. There
are no selectors for it anywhere in the folder, and inference from absence is not evidence.

So the first move is recon, not automation:

```bash
node oa_driver.mjs watch 300
# now drive ONE backtest by hand, end to end:
# set it up -> run it -> open Compare -> download the CSV
```

This clicks nothing. It logs every request and response OA's own frontend makes, plus every
download, to `data/captures/<date>-recon/`.

**Why this is the highest-leverage command in the folder.** If OA's frontend drives the
backtester through JSON endpoints — which a June-2026 SPA almost certainly does — then the
backtest lane does not need clicking *at all*. Issuing the same POST the frontend issues, on
the same session cookies, is faster than any driver, parallelises across parameter sets, and
returns the results as data instead of as a screenshot to be re-read. That is the difference
between a fast backtest lane and a slightly-less-slow one.

If the recon shows the backtester is server-rendered or WebSocket-driven, we script the
clicks instead — but we will know, rather than assume.

Two notes for when the sweep exists: `.gitignore` ignores `*.csv` outside `data/`, so land
downloaded `positions.csv` under `data/`. And a parameter sweep is load on Andy's own OA
account — rate is a decision for Andy, not a default for a script.

---

## 5. Commands

**Read path** (`oa_capture.mjs`, no deps):

```bash
node oa_capture.mjs targets              # list attachable OA tabs
node oa_capture.mjs roster               # /bots capture, bookmarklet-identical text
node oa_capture.mjs bot BOTxxxxxxxx      # hydrated a5.bots.bot model
node oa_capture.mjs automation-hash      # sha256(JSON.stringify({name,inputs,root}))
```

**Write path** (`oa_driver.mjs`, Playwright):

```bash
node oa_driver.mjs status                        # what is this tab? changes nothing
node oa_driver.mjs watch 300                     # network recon while you click
node oa_driver.mjs hash                          # config hash of the open automation
node oa_driver.mjs click 'a.saveclose'           # DRY RUN — actionability report only
node oa_driver.mjs click 'a.saveclose' --allow-write --bot PR-02
node oa_driver.mjs save-automation --allow-write --bot PR-02
```

### `save-automation` — Layer 1, automated, across three surfaces

1. hash the open automation (`a5.bots.acedit.routine`)
2. click `a.saveclose` — the **real** commit; the action-drawer Save is not (§5 trap 7)
3. watch for OA's POST and its status
4. hard reload, with `beforeunload` **observed rather than dismissed** — trap 8's dirty-state
   oracle, read as evidence
5. re-hash and report all three surfaces together

A changed hash with a fired guard is **not** a clean save. The script prints the surfaces and
declines to blend them into a verdict, per `daily-loop-spec.md`'s three-verdicts rule.

---

## 6. Pilot order

1. `oa_capture.mjs roster`, then `oa_normalize.py compare` against
   `data/captures/2026-08-17-r3/01-oa-bots-capture-2026-08-17-195713.txt`. Acceptance is
   stated as a derivation in §7, never as the literal `44`.
2. `oa_driver.mjs status` — confirm it attaches and identifies the bot.
3. `oa_driver.mjs watch 300` + one hand-driven backtest. **Do this before writing any
   backtest code.**
4. `--method` shoot-out on a **dead bot**: trusted vs js chain, post-condition = the hash.
   Log which lands. That result belongs in the runbook, not in this README.
5. Only then, a real edit — and Layer 2 is still owed.

## 7. Acceptance predicate for the read pilot

Stated as a derivation; a literal passes a broken read the day the roster changes.

1. `toggle_section_present` true in both. False on the new capture means the ancestor-climb
   selectors missed — a **finding** per §1.2, not a formatting problem.
2. `only_in_old` / `only_in_new` both empty, unless a bot was genuinely added or archived in
   the window — then the difference must equal that change and nothing else.
3. `toggle_changes` empty, unless a toggle was genuinely flipped.
4. P/L, RETURN %, CHANGE will differ. That is the market. `compare` ignores them.

Already cross-checked on a second surface: `oa_normalize.py summary` recomputes the reference
capture's raw sha256 as `8d9c59b71858c97f…`, matching the hash recorded independently in
`02-roster-toggles-44-2026-08-17.tsv`'s header.

---

## 8. Files

| File | What it is |
|---|---|
| `oa_capture.mjs` | Read path. Raw CDP, zero deps. |
| `oa_grab_page.js` | `OA Grab` bookmarklet v2.1 as a page expression that returns instead of downloading. **The single copy of the instrument** — if `oa-ops-runbook.md` §1.2 is revised, this is a reader that must be revised with it. |
| `oa_driver.mjs` | Write path. Playwright, dry-run by default. |
| `oa_normalize.py` | §1.5 noise-stripping, structural `summary`, `compare`. |
| `package.json` | `playwright-core` 1.62.1, pinned. |

## 9. Known limits

- **Browserbase and cloud browsers stay out of scope.** They relocate latency to a network
  hop rather than removing it. Their parallel-session advantage is real for backtest sweeps
  only, and only if recon shows clicking is unavoidable — revisit then.
- `compare` reads only the appended AUTOS/EXITS section, not the 18-field prefix.
- Precision above $10K is 3 significant figures in the capture (§1.5), here as in the
  bookmarklet. −$11,200 → −$11,249 does not diff.
- `--method both` cannot fall back on a **silent** no-op — a silent no-op raises nothing.
  Only the post-condition catches those.
- Nothing automates Layer 2.
