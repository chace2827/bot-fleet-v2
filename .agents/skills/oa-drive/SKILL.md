---
name: oa-drive
description: How an agent session connects to and operates Option Alpha — the CDP Chrome launch Andy does by hand, the read path (oa_capture.mjs), and the write path (oa_driver.mjs) for UI-level capture and UI-built backtests. Invoke for any task that must navigate, read, drive, or capture OA.
---

# OA Drive — how a session touches Option Alpha

Companion to the `option-alpha` skill (which is the law: evidence rules, traps, verification).
This file is the **plumbing**: how to get connected, which tool does what. Canonical docs still
win: `docs/oa-ops-runbook.md`, `scripts/oa-driver/README.md`.

## ⚠️ Authorization boundary — read first

OA's Terms of Use ("Third Party Agents and Tools") prohibit automated/agent access **without
prior written authorization**. Written authorization exists for **one scope only**
(`R-2026-09-16-DEVIN-OA-CHROME-CAPTURE`; Andy verbatim: *"chrome based navigation to capture
what we need … down the road we can look into using the API zdte path"*):

- **AUTHORIZED — the UI path.** Drive OA's interface like a user: launch/attach Chrome,
  navigate, click, fill forms, read rendered content, screenshot, use OA's own Export Data,
  build and run backtests through the UI. CDP is the mechanism that performs the navigation —
  Devin has no other way to operate a browser — so it is inside the grant, not a separate
  thing needing one.
- **CAPTURE ONLY — no OA edits.** Ruling scope: reads, screenshots, exports, backtest
  construction and comparison in the browser. Bot, automation, scanner, position, and
  settings surfaces are **read-only** — never open/edit/enable/save them, whatever the
  tooling allows. Edits stay in the Cowork lane under CLAUDE.md §5's two-layer proof regime;
  this skill must never be the mechanism for one.
- **NOT AUTHORIZED — the wire protocol.** Never observe or issue OA's internal RPC: no
  fetch/XHR wrapping or patching, no `POST /api/request` calls of our own, no `zdte.*`
  replay, no traffic recorder. The 2026-09-15 verification
  (`docs/experiments/oa-rpc-test-2026-09-15/`, PR #79) proved the path exists and is exactly
  the fingerprinted one — that record is history, not a toolkit. Out of scope until a
  broader written grant, and a grant that says only "later" is not one.
- **Page-context reads** (`Runtime.evaluate` DOM reads, the OA Grab bookmarklet) are in
  scope: they record what the page rendered and emit no OA-bound traffic. This is the
  interpretation most exposed if OA's written reply turns out narrower than the ruling's
  reading — if the verbatim grant prohibits all inspection rather than the API process,
  this line is the first to fall.

If a task needs anything past this boundary: **stop and ask Andy.** The grant's wording is the
authority; this file is only its plumbing.

## 1. What Andy does by hand (the session cannot)

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 --user-data-dir="$HOME/.chrome-oa-profile"
# then log into https://app.optionalpha.com in that window
```

The session cookie lives in that profile — use the persistent profile path above, never
`/tmp` (a wiped profile is a logged-out session). Do NOT launch a second Chrome on the
default profile; CDP requires the dedicated `--user-data-dir`.

## 2. Attach and verify — before anything else

1. `curl -s http://127.0.0.1:9222/json/list` — find targets with `type:"page"` on
   `app.optionalpha.com`. No targets → Chrome isn't up or the tab was closed; stop and ask.
2. Attach via `Runtime.evaluate` on the page's `webSocketDebuggerUrl` (raw CDP needs zero
   dependencies — Node ≥22 global `fetch` + `WebSocket`; see `scripts/oa-driver/oa_capture.mjs`
   for the exact pattern).
3. Verify, in order:
   - **URL has no `/login`** → if it does, stop and tell Andy.
   - **Logged in**: page text hydrates past the "Login / Get Started Free" shell (the SPA
     shows a pre-auth shell for a few seconds on fresh loads — wait and re-read once before
     concluding logged-out).
   - **PAPER badge**: `/backtests` is a minimal shell with the account bar hidden
     (`display:none`). Check `/home` — "PAPER" appears in the activity header. Anything
     indicating a live brokerage account → stop.

## 3. Read path — `scripts/oa-driver/oa_capture.mjs`

Raw CDP, runs by default. Roster capture, bot model dump, config hash. A read is one
`Runtime.evaluate` — no dependencies needed, and no OA-bound traffic: it inspects what the
page already rendered.

For ad-hoc reads, evaluate an expression that returns a JSON string; the page context has
no `require`/Node APIs — pull data out as a string and write files locally.

## 4. Write path — `scripts/oa-driver/oa_driver.mjs`

Playwright over CDP (`playwright-core`, `npm i` in that folder — no browser download).
Why Playwright for clicks: locators re-resolve per action (retires the stale-handle bug),
actionability + hit-target checks, `waitForResponse` as a second verification surface,
and a trace artifact per write.

**Grant scope on writes:** under the current authorization the write path's legitimate targets
are the **backtester UI and export/download controls only**. Bot surfaces are read-only —
the script's `--allow-write --bot` mechanism must never be exercised on them, even though it
exists.

- **Dry run is default.** `--allow-write` additionally requires `--bot <id|name>`; the
  script reads `a5.bots.bot` and refuses if the page disagrees.
- Refuses: non-`app.optionalpha.com` pages, ambiguous selectors, occluded elements.
- OA's DOM uses custom elements (`item.mi`, `group`/`hd`/`bd`, `a.cbox`, `overlay.*editor`).
  Text selectors often fail on markup like `<bd>-.20</bd>` — inspect the real structure,
  then use `scrollIntoView` + coordinate clicks when selectors can't disambiguate.
- A click that "succeeded" may have done nothing: **re-read the page after every action.**
  After a timeout, re-read state — never blindly repeat the action.
- Collapsed `group` elements (`bd` display:none) must be expanded via their `hd` header first.
  Form fields live in hidden inputs that ARE the serialized config — read them to verify
  state instead of trusting the visible widget.

## 5. Out of scope — the wire protocol (reference only)

Do not exercise. The 2026-09-15 probe verified `zdte.*` is usable end-to-end
(`docs/experiments/oa-rpc-test-2026-09-15/`; shapes in `docs/oa-internal-api.md`) — and
established it is the detectable path: bare `startTest` sequences the frontend never
produces, results pulled with no matching page-load/RUM beacon, metronome polling, and
malformed-arg errors the UI cannot emit, all sitting in server logs beside the account id.
The passive-recorder pattern (wrapping `fetch`/`XHR` to observe `/api/request`) is the same
class — it is network inspection, which is the prohibited "inspection portion." If a task's
data is only reachable through the wire protocol, that is a stop-and-ask, not an improvise.

## 6. Stop conditions — no retries past these

401/403/429 · URL contains `/login` · terms/payment prompt · anything indicating a live
(non-PAPER) account · any action whose only route is the wire protocol · a write outside
the backtester/export scope.
