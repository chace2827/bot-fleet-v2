#!/usr/bin/env node
/**
 * oa_driver.mjs — the WRITE path. Playwright over CDP, attached to the Chrome you are
 * already logged into.
 *
 * Companion to oa_capture.mjs (the READ path, zero-dependency raw CDP). Reads stay there:
 * they are faster and need no dependency. Everything that CLICKS lives here.
 *
 * WHY PLAYWRIGHT FOR THIS AND NOT FOR READS
 * -----------------------------------------
 * Not because it can click — raw CDP can click too. Because of what surrounds the click:
 *
 *   1. LOCATORS RE-RESOLVE on every action. Runbook §5 trap 6 (stale editor DOM — two
 *      automations open in one page life, node queries return the PREVIOUS automation's
 *      cards, a click edits the wrong automation SILENTLY) is a stale-handle bug. A
 *      locator has no handle to go stale.
 *   2. ACTIONABILITY + HIT-TARGET TEST. Before clicking, Playwright waits for visible,
 *      stable (bounding box unchanged across two animation frames), enabled, and then
 *      verifies the point it is about to hit actually resolves to the target element.
 *      That is trap 1 (overlays animating) and the "Delete sits ~29px below Archive"
 *      hazard, checked automatically instead of by discipline.
 *   3. NETWORK AS A SECOND SURFACE. `waitForResponse` turns "did the save commit?" from
 *      an INFERENCE off the Leave-site guard (trap 8) into an OBSERVATION of OA's own
 *      POST and status code.
 *   4. TRACES. Every action gets a screenshot, a DOM snapshot and its network log, written
 *      to a file. That is a §9.1a evidence artifact per edit, produced automatically.
 *
 * ⚠️ A HYPOTHESIS THIS SCRIPT EXISTS TO TEST — not a claim, do not cite it as fact.
 * The skill records: "Element-ref clicks silently no-op on this app. The app binds
 * delegated handlers and ignores the synthetic single click." The documented workaround
 * dispatches a JS MouseEvent chain, which produces events with `isTrusted: false`.
 * Playwright clicks via CDP `Input.dispatchMouseEvent` — injected at the browser's input
 * pipeline, `isTrusted: true`, indistinguishable from a human hand. That is a THIRD
 * mechanism, different from both the extension's element-ref click and from the JS chain.
 * It MAY simply work where both failed. `--method` lets you test all three on a dead bot
 * and record which lands. Until that test is run and logged, nothing here is proven.
 *
 * SAFETY MODEL
 * ------------
 *   - DRY RUN IS THE DEFAULT. Without `--allow-write` this script performs every
 *     actionability check and reports exactly what it WOULD click — and clicks nothing.
 *   - `--allow-write` additionally requires `--bot <id-or-name>` naming the intended
 *     target, and refuses if the page's own model disagrees with it.
 *   - It refuses to run off app.optionalpha.com.
 *   - Tracing is always on for write runs. A write with no trace file is not a write this
 *     script performed.
 *
 * SETUP
 *   npm i               # playwright-core only; no browser download, we attach to yours
 *   Chrome must already be running with:
 *     --remote-debugging-port=9222 --user-data-dir="$HOME/.chrome-oa-profile"
 *
 * COMMANDS
 *   status                    Connect, report the attached page. Changes nothing.
 *   watch [seconds]           ⭐ RECON. Log every OA request/response while YOU click by
 *                             hand. This is how the backtest flow and the save endpoint
 *                             get learned instead of guessed.
 *   hash                      Config hash of the automation open in the tab.
 *   click <selector>          Actionability report; clicks only with --allow-write.
 *   save-automation           Composed: pre-hash -> click a.saveclose -> network watch ->
 *                             beforeunload oracle -> hard reload -> post-hash -> verdict.
 *
 * FLAGS
 *   --allow-write             Arm the write path. Without it, nothing is clicked.
 *   --bot <id|name>           Required with --allow-write. Asserted against the page model.
 *   --method trusted|js|both  Click mechanism (default trusted). `js` is the documented
 *                             MouseEvent chain. `both` tries trusted, then js on no-op.
 *   --trace DIR               Trace output dir (default data/receipts/traces/).
 *   --cdp URL                 Default http://127.0.0.1:9222 or $OA_CDP.
 */

import { chromium } from 'playwright-core';
import { createHash } from 'node:crypto';
import { mkdirSync, writeFileSync, appendFileSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '..', '..');
const HOST = 'app.optionalpha.com';

const argv = process.argv.slice(2);
const cmd = argv[0];
const rest = argv.slice(1).filter((a) => !a.startsWith('--'));
const flag = (n, d = null) => {
  const i = argv.indexOf('--' + n);
  if (i === -1) return d;
  const v = argv[i + 1];
  return v && !v.startsWith('--') ? v : true;
};

const CDP = flag('cdp', process.env.OA_CDP || 'http://127.0.0.1:9222');
const ALLOW_WRITE = flag('allow-write') === true;
const TARGET_BOT = flag('bot');
const METHOD = flag('method', 'trusted');
const stamp = () => new Date().toISOString().slice(0, 19).replace(/[:T]/g, '-');

// ---------------------------------------------------------------- connect

async function connect() {
  let browser;
  try {
    browser = await chromium.connectOverCDP(CDP);
  } catch (e) {
    throw new Error(
      `cannot attach to Chrome at ${CDP}\n` +
        `  Launch it with --remote-debugging-port=9222 --user-data-dir="$HOME/.chrome-oa-profile"\n` +
        `  (${e.message})`
    );
  }
  const context = browser.contexts()[0];
  if (!context) throw new Error('no browser context — is the debug Chrome showing a window?');
  const pages = context.pages();
  const oa = pages.filter((p) => {
    try {
      return new URL(p.url()).hostname === HOST;
    } catch {
      return false;
    }
  });
  if (!oa.length) {
    throw new Error(
      `no ${HOST} tab open. Log into Option Alpha first — this script will not open a tab.\n` +
        `  Tabs seen: ${pages.map((p) => p.url()).join(', ') || '(none)'}`
    );
  }
  if (oa.length > 1) console.error(`! ${oa.length} OA tabs; using the first (runbook §6: one OA session at a time)`);
  console.error(`> attached: ${oa[0].url()}`);
  return { browser, context, page: oa[0] };
}

/**
 * ⛔ NEVER call browser.close() here. We attached to Andy's own Chrome; on a
 * connectOverCDP browser close() can terminate the real browser process, taking the
 * logged-in OA session and every other tab with it (observed 2026-08-19/20 — the debug
 * window vanished at the end of a run). Disconnect instead: we did not open it, we do not
 * close it.
 */
function release(_browser) {
  // Deliberately a NO-OP. Dropping the CDP websocket is what detaching means, and that
  // happens when this process exits. Calling anything on the browser handle here is how
  // you end up closing a window you did not open.
}

function traceDir() {
  const d = flag('trace');
  return typeof d === 'string' ? d : join(REPO, 'data', 'receipts', 'traces');
}

// ---------------------------------------------------------------- page reads

const ROUTINE_PAYLOAD = () => {
  const r = window.a5?.bots?.acedit?.routine;
  if (!r) return null;
  return JSON.stringify({ name: r.name, inputs: r.inputs, root: r.root });
};

const BOT_IDENTITY = () => {
  const b = window.a5?.bots?.bot;
  return b ? { id: b.id ?? null, name: b.name ?? null } : null;
};

async function routineHash(page) {
  const payload = await page.evaluate(ROUTINE_PAYLOAD);
  if (!payload) return null;
  return { sha: createHash('sha256').update(payload).digest('hex'), payload };
}

/** --allow-write demands the caller name the target, and the PAGE must agree. */
async function assertIntendedTarget(page) {
  if (!ALLOW_WRITE) return;
  if (!TARGET_BOT) throw new Error('--allow-write requires --bot <id|name> naming the intended target');
  const id = await page.evaluate(BOT_IDENTITY);
  if (!id) throw new Error('a5.bots.bot not hydrated — cannot confirm which bot this page is. Refusing to write.');
  const match = id.id === TARGET_BOT || id.name === TARGET_BOT;
  if (!match) {
    throw new Error(
      `TARGET MISMATCH — refusing to write.\n` +
        `  you named : ${TARGET_BOT}\n` +
        `  page says : id=${id.id} name=${id.name}`
    );
  }
  console.error(`> target confirmed against the page model: ${id.name} (${id.id})`);
}

// ---------------------------------------------------------------- actionability report

async function describe(page, selector) {
  const loc = page.locator(selector);
  const count = await loc.count();
  if (count === 0) return { selector, count, resolvable: false };
  if (count > 1) {
    return {
      selector,
      count,
      resolvable: false,
      note: 'selector is AMBIGUOUS — refusing. Narrow it; never index into a guess.',
    };
  }
  const box = await loc.boundingBox();
  const detail = await loc.evaluate((el) => {
    const r = el.getBoundingClientRect();
    const cx = r.left + r.width / 2;
    const cy = r.top + r.height / 2;
    const top = document.elementFromPoint(cx, cy);
    return {
      tag: el.tagName.toLowerCase(),
      classes: el.className?.toString().slice(0, 120) ?? '',
      text: (el.innerText || '').trim().slice(0, 80),
      hitTargetIsSelf: top === el || el.contains(top),
      topAtCentre: top ? top.tagName.toLowerCase() + '.' + (top.className?.toString().split(' ')[0] || '') : null,
    };
  });
  return {
    selector,
    count,
    resolvable: true,
    visible: await loc.isVisible(),
    enabled: await loc.isEnabled(),
    box,
    ...detail,
  };
}

// ---------------------------------------------------------------- click mechanisms

/** The documented workaround: a JS MouseEvent chain. isTrusted:false. */
const JS_CHAIN = (el) => {
  const r = el.getBoundingClientRect();
  const x = r.left + r.width / 2;
  const y = r.top + r.height / 2;
  const opts = { bubbles: true, cancelable: true, view: window, clientX: x, clientY: y };
  for (const type of ['pointerover', 'pointerenter']) el.dispatchEvent(new PointerEvent(type, opts));
  el.focus?.();
  for (const type of ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click']) {
    const Ev = type.startsWith('pointer') ? PointerEvent : MouseEvent;
    el.dispatchEvent(new Ev(type, opts));
  }
  return true;
};

/**
 * `both` falls back to the JS chain only when the trusted click THROWS (not actionable,
 * occluded, detached). It cannot fall back on a SILENT no-op, because a silent no-op
 * raises nothing — that is the whole reason the trap was expensive to find. Silent no-ops
 * are caught downstream by the post-condition (the hash), never here.
 */
async function performClick(page, selector, method) {
  const loc = page.locator(selector);
  if (method === 'js') {
    await loc.evaluate(JS_CHAIN);
    return 'js-chain';
  }
  try {
    // trusted: CDP Input.dispatchMouseEvent, with actionability + hit-target check.
    await loc.click({ timeout: 15000 });
    return 'trusted';
  } catch (e) {
    if (method !== 'both') throw e;
    console.error(`! trusted click threw (${e.message.split('\n')[0]}) — falling back to the JS chain`);
    await loc.evaluate(JS_CHAIN);
    return 'js-chain (trusted threw)';
  }
}

// ---------------------------------------------------------------- commands

async function cmdStatus() {
  const { browser, page } = await connect();
  const model = await page.evaluate(() => ({
    bot: window.a5?.bots?.bot ? { id: window.a5.bots.bot.id, name: window.a5.bots.bot.name } : null,
    automationOpen: !!window.a5?.bots?.acedit?.routine,
    automationName: window.a5?.bots?.acedit?.routine?.name ?? null,
  }));
  const h = await routineHash(page);
  console.log(JSON.stringify({ url: page.url(), ...model, routineSha: h?.sha ?? null }, null, 2));
  release(browser);
}

/**
 * RECON — the highest-value command in this file right now.
 *
 * docs/backtest-ingest-protocol.md is a PASTE protocol: Andy screenshots the Compare page
 * and downloads positions.csv by hand. oa-platform-reference.md:47 lists the June 2026
 * backtester as UI-research-pending. There are no selectors for it anywhere in this repo,
 * and inference from absence is not evidence.
 *
 * So: run this, then drive ONE backtest by hand. Every request OA's own frontend makes is
 * logged. If those are JSON endpoints, the backtest lane may not need clicking at all —
 * issuing the same POST the frontend issues, on the same session cookies, is faster than
 * any driver and parallelises. That is the difference between a fast backtest lane and a
 * slightly-less-slow one.
 */
async function cmdWatch() {
  const seconds = Number(rest[0] || 120);
  const { browser, context, page } = await connect();
  const log = [];

  /**
   * ⚠️ Registering a `download` listener makes PLAYWRIGHT own the download: the browser
   * stops writing to ~/Downloads and the bytes go to a temp dir that is deleted when the
   * connection closes. Found 2026-08-19 the hard way — a positions.csv downloaded during a
   * watch run was unreachable from Finder and gone afterwards.
   * So the listener MUST call saveAs(). The recon dir is created up front, not at the end,
   * because a download can arrive before the run does.
   */
  const dir = join(REPO, 'data', 'captures', `${new Date().toISOString().slice(0, 10)}-recon`);
  mkdirSync(dir, { recursive: true });
  console.error(`> downloads and the request log will land in: ${dir}`);

  /**
   * ⛔ Write EVERY event to disk as it happens. The first version buffered in memory and
   * serialised once, at the end of the timer — so Ctrl+C, a crash, or closing the terminal
   * threw away the entire session. A recon run you cannot interrupt safely is a recon run
   * you will lose. JSONL append is the sink; the consolidated .json is a convenience
   * written at the end, never the only copy.
   */
  const jsonlPath = join(dir, `oa-network-recon-${stamp()}.jsonl`);
  writeFileSync(jsonlPath, '');
  const record = (e) => {
    log.push(e);
    try {
      appendFileSync(jsonlPath, JSON.stringify(e) + '\n');
    } catch {}
  };
  console.error(`> live log: ${jsonlPath}`);

  let stopping = false;
  const finish = (why) => {
    if (stopping) return;
    stopping = true;
    console.error(`\n=== ${why} — ${log.length} events captured ===`);
    console.log(`\nlog    ${jsonlPath}`);
    console.log(`events ${log.length}`);
    try {
      const body = JSON.stringify(log, null, 2);
      const jsonPath = jsonlPath.replace(/\.jsonl$/, '.json');
      writeFileSync(jsonPath, body);
      console.log(`json   ${jsonPath}`);
      console.log(`sha256 ${createHash('sha256').update(body).digest('hex')}`);
    } catch (e) {
      console.error(`! consolidated json failed (${e.message}) — the .jsonl above is intact`);
    }
    process.exit(0);
  };
  process.on('SIGINT', () => finish('INTERRUPTED by Ctrl+C'));
  process.on('SIGTERM', () => finish('TERMINATED'));
  const interesting = (u) => {
    try {
      const url = new URL(u);
      return url.hostname === HOST && !/\.(png|jpe?g|svg|woff2?|css|ico)$/i.test(url.pathname);
    } catch {
      return false;
    }
  };

  /**
   * Listen at CONTEXT level, not page level. If OA opens the backtester in a new tab —
   * and we do not know that it doesn't — a page-scoped listener records nothing and the
   * recon run is silently wasted. Attach to every OA page now and to every one opened
   * later. WebSocket frames are captured too: if the backtester streams progress rather
   * than polling, that is the finding, and a request log alone would miss it.
   */
  const attach = (p) => {
    p.on('request', (req) => {
      if (!interesting(req.url())) return;
      if (req.method() === 'GET' && !req.url().includes('?')) return;
      const post = req.postData();
      record({
        t: new Date().toISOString(),
        dir: '>',
        method: req.method(),
        url: req.url(),
        body: post ? post.slice(0, 4000) : null,
      });
      console.error(`> ${req.method()} ${req.url().replace('https://' + HOST, '')}`);
    });

    p.on('response', async (res) => {
      if (!interesting(res.url())) return;
      const ct = res.headers()['content-type'] || '';
      let body = null;
      if (ct.includes('json')) {
        body = await res.text().then((t) => t.slice(0, 4000)).catch(() => null);
      }
      record({ t: new Date().toISOString(), dir: '<', status: res.status(), url: res.url(), body });
    });

    p.on('websocket', (ws) => {
      // ⛔ HOST FILTER — the request/response handlers had one from the start and this did
      // not. Found 2026-08-20: a recon run captured 41 WebSocket frames from an unrelated
      // site open in another tab of the same browser, straight into a repo file. A recorder
      // pointed at "the browser" records the WHOLE browser. Never log a frame you have not
      // first confirmed belongs to the host under study.
      if (!interesting(ws.url())) return;
      record({ t: new Date().toISOString(), dir: 'WS', url: ws.url() });
      console.error(`> WEBSOCKET ${ws.url()}`);
      ws.on('framereceived', (f) => {
        const d = typeof f.payload === 'string' ? f.payload : '(binary)';
        record({ t: new Date().toISOString(), dir: 'WS<', url: ws.url(), body: d.slice(0, 2000) });
      });
      ws.on('framesent', (f) => {
        const d = typeof f.payload === 'string' ? f.payload : '(binary)';
        record({ t: new Date().toISOString(), dir: 'WS>', url: ws.url(), body: d.slice(0, 2000) });
      });
    });

    p.on('download', async (d) => {
      // Never clobber: a sweep downloads positions.csv per column, and saving under the
      // suggested name overwrote the previous column's data silently (seen 2026-08-20).
      const name = d.suggestedFilename() || 'download';
      const dot = name.lastIndexOf('.');
      const stem = dot > 0 ? name.slice(0, dot) : name;
      const ext = dot > 0 ? name.slice(dot) : '';
      const dest = join(dir, `${stem}-${stamp()}${ext}`);
      try {
        await d.saveAs(dest);
        record({ t: new Date().toISOString(), dir: 'DL', url: d.url(), suggested: name, savedTo: dest });
        console.error(`> DOWNLOAD ${name}  ->  ${dest}`);
      } catch (e) {
        record({ t: new Date().toISOString(), dir: 'DL', url: d.url(), suggested: name, error: e.message });
        console.error(`! DOWNLOAD ${name} could not be saved: ${e.message}`);
      }
    });
  };

  context.pages().forEach((p) => {
    try {
      if (new URL(p.url()).hostname === HOST) attach(p);
    } catch {}
  });
  context.on('page', (p) => {
    console.error(`> new tab: ${p.url()}`);
    attach(p);
  });

  console.error(`\n=== RECORDING ${seconds}s — drive OA by hand now ===`);
  console.error(`Run one backtest end to end: set it up, run it, open Compare, download the CSV.`);
  console.error(`This script clicks NOTHING. It only listens.\n`);
  await page.waitForTimeout(seconds * 1000);

  finish('recording window elapsed');
  release(browser);
}

async function cmdHash() {
  const { browser, page } = await connect();
  const h = await routineHash(page);
  if (!h) throw new Error('a5.bots.acedit.routine absent — open an automation first');
  console.log(`CONFIG HASH  ${h.sha}`);
  console.log(`formula      sha256(JSON.stringify({name, inputs, root}))`);
  console.log(`\n! §5 trap 6: opened a second automation in this page life? Hard-reload and re-run.`);
  release(browser);
}

async function cmdClick() {
  const selector = rest[0];
  if (!selector) throw new Error('usage: oa_driver.mjs click <selector> [--allow-write --bot <id>]');
  const { browser, context, page } = await connect();
  try {
    const report = await describe(page, selector);
    console.log(JSON.stringify(report, null, 2));
    if (!report.resolvable) throw new Error(report.note || 'selector did not resolve to exactly one element');
    if (!report.hitTargetIsSelf) {
      console.error(`\n⛔ HIT-TARGET FAIL: the centre point resolves to ${report.topAtCentre}, not the target.`);
      console.error(`   Something overlays it. Clicking here would hit the wrong element.`);
      throw new Error('refusing to click an occluded element');
    }
    if (!ALLOW_WRITE) {
      console.log(`\nDRY RUN — nothing clicked. Re-run with --allow-write --bot <id|name> to arm.`);
      return;
    }
    await assertIntendedTarget(page);
    mkdirSync(traceDir(), { recursive: true });
    await context.tracing.start({ screenshots: true, snapshots: true });
    const used = await performClick(page, selector, METHOD === 'both' ? 'trusted' : METHOD);
    const tracePath = join(traceDir(), `click-${stamp()}.zip`);
    await context.tracing.stop({ path: tracePath });
    console.log(`\nclicked via ${used}`);
    console.log(`trace  ${tracePath}   (npx playwright show-trace ${tracePath})`);
    console.log(`\n! A click is not a commit and a trace is not verification (§9.1a).`);
    console.log(`! Layer 1: hard-reload and re-observe the value. Layer 2: the next position's Trades list.`);
  } finally {
    release(browser);
  }
}

/**
 * The composed primitive: automates LAYER 1 of §5, and adds a second surface.
 * It does not automate Layer 2 — the Trades list of the first new position is still
 * a live-market observation, and nothing here can shortcut it.
 */
async function cmdSaveAutomation() {
  const { browser, context, page } = await connect();
  try {
    const pre = await routineHash(page);
    if (!pre) throw new Error('no automation open — a5.bots.acedit.routine is absent');
    console.error(`> pre-save  hash ${pre.sha}`);

    const report = await describe(page, 'a.saveclose');
    console.log(JSON.stringify(report, null, 2));
    if (!report.resolvable) throw new Error('a.saveclose did not resolve — is the automation editor open?');
    if (!ALLOW_WRITE) {
      console.log(`\nDRY RUN — nothing saved. Re-run with --allow-write --bot <id|name> to arm.`);
      return;
    }
    await assertIntendedTarget(page);

    mkdirSync(traceDir(), { recursive: true });
    await context.tracing.start({ screenshots: true, snapshots: true });

    // Surface 2: OA's own POST. Never fails the run on timeout — absence of an observed
    // response is not evidence the save failed, only that we did not see it.
    const savePost = page
      .waitForResponse((r) => r.request().method() === 'POST' && r.url().includes(HOST), { timeout: 20000 })
      .catch(() => null);

    const used = await performClick(page, 'a.saveclose', METHOD === 'both' ? 'trusted' : METHOD);
    const res = await savePost;
    console.error(`> clicked via ${used}; POST ${res ? `${res.status()} ${res.url()}` : 'NOT OBSERVED'}`);

    // Surface 3: trap 8's dirty-state oracle, read instead of dismissed.
    let guardFired = false;
    page.on('dialog', async (d) => {
      if (d.type() === 'beforeunload') guardFired = true;
      await d.accept();
    });

    await page.reload({ waitUntil: 'load' });
    await page.waitForTimeout(2000);
    const post = await routineHash(page);

    const tracePath = join(traceDir(), `save-${stamp()}.zip`);
    await context.tracing.stop({ path: tracePath });

    console.log(`\n--- three surfaces ---`);
    console.log(`network POST      ${res ? res.status() : 'NOT OBSERVED'}`);
    console.log(`beforeunload      ${guardFired ? 'FIRED — uncommitted state existed at reload' : 'silent'}`);
    console.log(`hash pre          ${pre.sha}`);
    console.log(`hash post         ${post?.sha ?? '(automation not open after reload — reopen and re-hash)'}`);
    console.log(`hash changed      ${post ? (post.sha !== pre.sha ? 'YES' : 'NO')  : 'UNKNOWN'}`);
    console.log(`trace             ${tracePath}`);
    console.log(`\n! Read these together, not separately. A changed hash with a fired guard is`);
    console.log(`! NOT a clean save. Layer 2 (first new position's Trades list) is still owed.`);
  } finally {
    release(browser);
  }
}

const COMMANDS = { status: cmdStatus, watch: cmdWatch, hash: cmdHash, click: cmdClick, 'save-automation': cmdSaveAutomation };

if (!cmd || !COMMANDS[cmd]) {
  console.error(`usage: node oa_driver.mjs <status|watch [sec]|hash|click <sel>|save-automation> [--allow-write --bot X]`);
  process.exit(2);
}
COMMANDS[cmd]()
  .then(() => process.exit(0))
  .catch((e) => {
    console.error(`\nFAILED: ${e.message}`);
    process.exit(1);
  });
