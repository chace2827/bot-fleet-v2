#!/usr/bin/env node
/**
 * oa_capture.mjs — read-only Option Alpha capture over the Chrome DevTools Protocol.
 *
 * WHY THIS EXISTS
 * ---------------
 * Driving OA through a per-call browser tool costs one bridge round-trip per read.
 * This script opens ONE CDP connection to the Chrome you are already logged into and
 * does the whole job in one process. A 44-row roster capture is one round-trip, not
 * forty. Nothing here is an agent: it is the runbook's own instrument, scripted.
 *
 * ZERO DEPENDENCIES. Node 22+ only (global fetch + global WebSocket). No npm install,
 * no node_modules in the repo, no Playwright version to drift.
 *
 * SAFETY — what this script can and cannot do
 * -------------------------------------------
 *   - It only ever READS. It dispatches no pointer/mouse/click events, types nothing,
 *     and never touches a Save control. It cannot edit a bot.
 *   - It refuses to navigate anywhere except app.optionalpha.com.
 *   - It attaches to an EXISTING OA tab. It will not open one, so it can never race a
 *     login screen or a session you did not intend it to touch.
 *   - `Runtime.evaluate` can time out at ~45s (runbook §5 trap 2). For a read that is
 *     harmless — nothing was committed, so re-running is safe. That trap only bites
 *     writes, and this script does not write.
 *
 * SETUP (once)
 * ------------
 *   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
 *     --remote-debugging-port=9222 --user-data-dir="$HOME/.chrome-oa-profile"
 *   ...then log into Option Alpha in that window. Chrome 136+ requires the separate
 *   --user-data-dir; without it the debugging port is refused.
 *
 * USAGE
 * -----
 *   node oa_capture.mjs targets                 # list attachable OA tabs, change nothing
 *   node oa_capture.mjs roster                  # /bots capture, bookmarklet-identical text
 *   node oa_capture.mjs roster --no-navigate    # capture whatever the tab shows now
 *   node oa_capture.mjs bot BOTxxxxxxxx         # dump the hydrated a5.bots.bot model
 *   node oa_capture.mjs automation-hash         # hash the automation open in the tab
 *
 *   --out DIR    write here instead of data/captures/<today>-pw/
 *   --cdp URL    CDP host (default http://127.0.0.1:9222, or $OA_CDP)
 *
 * Every written file's sha256 is printed. That hash — not this script's exit code — is
 * the evidence (CLAUDE.md §9.1a).
 */

import { createHash } from 'node:crypto';
import { writeFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '..', '..');
const ALLOWED_HOST = 'app.optionalpha.com';

// ---------------------------------------------------------------- args

const argv = process.argv.slice(2);
const cmd = argv[0];
const positional = argv.slice(1).filter((a) => !a.startsWith('--'));
const flag = (name, fallback = null) => {
  const i = argv.indexOf('--' + name);
  if (i === -1) return fallback;
  const v = argv[i + 1];
  return v && !v.startsWith('--') ? v : true;
};
const CDP = flag('cdp', process.env.OA_CDP || 'http://127.0.0.1:9222');

// ---------------------------------------------------------------- CDP client

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function withTimeout(promise, ms, label) {
  return Promise.race([
    promise,
    new Promise((_, rej) => setTimeout(() => rej(new Error(`${label} timed out after ${ms}ms`)), ms)),
  ]);
}

async function listTargets() {
  let res;
  try {
    res = await fetch(CDP + '/json/list');
  } catch (e) {
    throw new Error(
      `cannot reach Chrome at ${CDP}\n` +
        `  Start it with:  --remote-debugging-port=9222 --user-data-dir="$HOME/.chrome-oa-profile"\n` +
        `  (${e.message})`
    );
  }
  if (!res.ok) throw new Error(`CDP /json/list returned ${res.status}`);
  return (await res.json()).filter((t) => t.type === 'page');
}

class Session {
  constructor(ws) {
    this.ws = ws;
    this.seq = 0;
    this.pending = new Map();
  }

  static async open(wsUrl) {
    const ws = new WebSocket(wsUrl);
    const s = new Session(ws);
    ws.addEventListener('message', (ev) => {
      let msg;
      try {
        msg = JSON.parse(ev.data);
      } catch {
        return;
      }
      const slot = s.pending.get(msg.id);
      if (!slot) return;
      s.pending.delete(msg.id);
      if (msg.error) slot.reject(new Error(`${msg.error.message} (CDP ${msg.error.code})`));
      else slot.resolve(msg.result);
    });
    await new Promise((res, rej) => {
      ws.addEventListener('open', res, { once: true });
      ws.addEventListener('error', () => rej(new Error('CDP websocket refused')), { once: true });
    });
    return s;
  }

  send(method, params = {}, timeoutMs = 60000) {
    const id = ++this.seq;
    const p = new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
    return withTimeout(p, timeoutMs, method);
  }

  close() {
    try {
      this.ws.close();
    } catch {}
  }
}

async function evaluate(sess, expression, timeoutMs = 60000) {
  const res = await sess.send(
    'Runtime.evaluate',
    { expression, returnByValue: true, awaitPromise: true, allowUnsafeEvalBlockedByCSP: true },
    timeoutMs
  );
  if (res.exceptionDetails) {
    const d = res.exceptionDetails;
    throw new Error('page exception: ' + (d.exception?.description || d.text || 'unknown'));
  }
  return res.result?.value;
}

// ---------------------------------------------------------------- tab selection

async function attachToOA() {
  const pages = await listTargets();
  const oa = pages.filter((t) => {
    try {
      return new URL(t.url).hostname === ALLOWED_HOST;
    } catch {
      return false;
    }
  });
  if (oa.length === 0) {
    throw new Error(
      `no ${ALLOWED_HOST} tab is open in the debug Chrome.\n` +
        `  Open Option Alpha and log in FIRST — this script will not open a tab for you.\n` +
        `  Tabs seen: ${pages.length ? pages.map((p) => p.url).join(', ') : '(none)'}`
    );
  }
  if (oa.length > 1) {
    console.error(`! ${oa.length} OA tabs open; using the first. Runbook §6: one OA session at a time.`);
    oa.forEach((t, i) => console.error(`    [${i}] ${t.url}`));
  }
  const target = oa[0];
  console.error(`> attached: ${target.url}`);
  return { sess: await Session.open(target.webSocketDebuggerUrl), target };
}

function assertOAUrl(url) {
  const u = new URL(url);
  if (u.hostname !== ALLOWED_HOST) throw new Error(`refusing to navigate off ${ALLOWED_HOST}: ${url}`);
  return u.toString();
}

async function navigate(sess, url) {
  assertOAUrl(url);
  await sess.send('Page.enable');
  await sess.send('Page.navigate', { url });
  await waitReady(sess);
}

async function waitReady(sess, timeoutMs = 45000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const state = await evaluate(sess, 'document.readyState').catch(() => null);
    if (state === 'complete') return;
    await sleep(300);
  }
  throw new Error('page never reached readyState=complete');
}

/**
 * The SPA hydrates after load. Poll `expr` until it returns the same non-zero value
 * twice in a row — that beats a fixed sleep, which is either too short (partial
 * roster, silently) or wastefully long.
 */
async function waitStable(sess, expr, { tries = 30, gapMs = 700, label = 'value' } = {}) {
  let prev = null;
  let stable = 0;
  for (let i = 0; i < tries; i++) {
    const v = await evaluate(sess, expr);
    if (v && v === prev) {
      if (++stable >= 2) return v;
    } else {
      stable = 0;
    }
    prev = v;
    await sleep(gapMs);
  }
  console.error(`! ${label} never stabilised (last: ${prev}) — capture may be partial. Re-run before trusting it.`);
  return prev;
}

// ---------------------------------------------------------------- page expressions

const GRAB = readFileSync(join(HERE, 'oa_grab_page.js'), 'utf8');

const BOT_MODEL = `(function(){
  var b = (window.a5 && a5.bots && a5.bots.bot) || null;
  if (!b) return { ok:false, reason:'a5.bots.bot is not hydrated on this page' };
  var seen = new WeakSet();
  var json = JSON.stringify(b, function(k, v){
    if (typeof v === 'function') return '[function]';
    if (v && typeof v === 'object') { if (seen.has(v)) return '[circular]'; seen.add(v); }
    return v;
  }, 2);
  return { ok:true, url: location.href, name: (b.name || null), inputs: (b.inputs ? b.inputs.length : null), json: json };
})()`;

// Hash formula per docs/oa-ops-runbook.md + the oa-driving skill:
//   sha256(JSON.stringify({name, inputs, root}))  computed AFTER opening the automation fresh.
// Key order is load-bearing — every baseline in data/captures/ used this literal order.
const AUTOMATION_PAYLOAD = `(function(){
  var r = (window.a5 && a5.bots && a5.bots.acedit && a5.bots.acedit.routine) || null;
  if (!r) return { ok:false, reason:'a5.bots.acedit.routine absent — open an automation first' };
  return { ok:true, url: location.href, name: (r.name || null),
           payload: JSON.stringify({ name: r.name, inputs: r.inputs, root: r.root }) };
})()`;

// ---------------------------------------------------------------- output

function today() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
}

function outDir() {
  const f = flag('out');
  return typeof f === 'string' ? f : join(REPO, 'data', 'captures', `${today()}-pw`);
}

function emit(filename, body) {
  const dir = outDir();
  mkdirSync(dir, { recursive: true });
  const path = join(dir, filename);
  writeFileSync(path, body);
  const sha = createHash('sha256').update(body).digest('hex');
  console.log(`\nwrote  ${path}`);
  console.log(`bytes  ${Buffer.byteLength(body)}`);
  console.log(`sha256 ${sha}`);
  return { path, sha };
}

// ---------------------------------------------------------------- commands

async function cmdTargets() {
  const pages = await listTargets();
  if (!pages.length) return console.log('(no pages — is the debug Chrome running?)');
  for (const t of pages) console.log(`${new URL(t.url).hostname === ALLOWED_HOST ? '* ' : '  '}${t.url}`);
  console.log('\n* = attachable');
}

async function cmdRoster() {
  const { sess } = await attachToOA();
  try {
    if (flag('no-navigate') !== true) {
      await navigate(sess, `https://${ALLOWED_HOST}/bots`);
    } else {
      await waitReady(sess);
    }
    const rows = await waitStable(
      sess,
      `document.querySelectorAll('a[href^="/bots/bot/"]').length`,
      { label: 'roster row count' }
    );
    console.error(`> ${rows} bot anchors present`);
    const grab = await evaluate(sess, GRAB);
    console.error(`> AUTOS/EXITS section: ${grab.rows} rows`);
    if (grab.rows === 0) {
      console.error('! zero toggle rows. Per runbook §1.2 that means the selectors missed —');
      console.error('! a finding, not a silent failure. The innerText prefix is still valid.');
    }
    emit(`oa_${grab.name}_${grab.stamp}.txt`, grab.text);
  } finally {
    sess.close();
  }
}

async function cmdBot(botId) {
  if (!botId || !/^BOT/.test(botId)) throw new Error('usage: oa_capture.mjs bot BOTxxxxxxxx');
  const { sess } = await attachToOA();
  try {
    await navigate(sess, `https://${ALLOWED_HOST}/bots/bot/${botId}`);
    await waitStable(sess, `(window.a5 && a5.bots && a5.bots.bot && a5.bots.bot.inputs) ? a5.bots.bot.inputs.length + 1 : 0`, {
      label: 'a5.bots.bot hydration',
    });
    const r = await evaluate(sess, BOT_MODEL);
    if (!r.ok) throw new Error(r.reason);
    console.error(`> bot: ${r.name} — ${r.inputs} inputs`);
    emit(`bot_${botId}_${new Date().toISOString().slice(0, 19).replace(/[:T]/g, '-')}.json`, r.json);
  } finally {
    sess.close();
  }
}

async function cmdAutomationHash() {
  const { sess } = await attachToOA();
  try {
    const r = await evaluate(sess, AUTOMATION_PAYLOAD);
    if (!r.ok) throw new Error(r.reason);
    const sha = createHash('sha256').update(r.payload).digest('hex');
    console.error(`> automation: ${r.name}`);
    console.log(`\nCONFIG HASH  ${sha}`);
    console.log(`formula      sha256(JSON.stringify({name, inputs, root}))`);
    console.log(`source       ${r.url}`);
    const stamp = new Date().toISOString().slice(0, 19).replace(/[:T]/g, '-');
    const safe = (r.name || 'automation').replace(/[^\w\-]+/g, '_').slice(0, 60);
    emit(`autohash_${safe}_${stamp}.json`, r.payload);
    console.log('\n! Runbook §5 trap 6: if you opened a second automation in this page life,');
    console.log('! hard-reload and re-run. A stale editor model hashes the WRONG automation.');
  } finally {
    sess.close();
  }
}

// ---------------------------------------------------------------- main

const COMMANDS = {
  targets: cmdTargets,
  roster: cmdRoster,
  bot: () => cmdBot(positional[0]),
  'automation-hash': cmdAutomationHash,
};

if (!cmd || !COMMANDS[cmd]) {
  console.error(`usage: node oa_capture.mjs <targets|roster|bot BOTxxx|automation-hash> [--out DIR] [--cdp URL]`);
  process.exit(2);
}

COMMANDS[cmd]().catch((e) => {
  console.error(`\nFAILED: ${e.message}`);
  process.exit(1);
});
