#!/usr/bin/env node
// PROPOSED — loss-packet browser runner (untested as a unit; every step below is
// copied from selectors/actions proven in this bundle's run on 2026-10-06).
// Produces §2 (positions+trades+autologs), §3 (run list + close-minute decision
// texts) and §5 (backtest rows) as JSON on stdout.
//
//   node PROPOSED-packet-runner.js --bot IC-SPX-FastPT25-S2-130PM \
//     --date 2026-08-26 --tests ZTid1,ZTid2,...
//
// Preconditions: Chrome on :9222 logged into app.optionalpha.com, PAPER account.
// READ-ONLY: clicks Load more, position rows, INFO cells, showPositions, pager.
// Never: automation-name links, Save, toggles, Clear Log, Create Bot, exports.

const args = Object.fromEntries(process.argv.slice(2).map(a => {
  const m = a.match(/^--(\w+)(?:=(.*))?$/); return m ? [m[1], m[2] ?? true] : null;
}).filter(Boolean));
const BOT = args.bot, DATE = args.date;                 // '2026-08-26'
const TESTS = (args.tests || '').split(',').filter(Boolean);
if (!BOT || !DATE) { console.error('need --bot --date'); process.exit(1); }
const MON = { '01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun',
  '07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec' };
const DATEHDR = MON[DATE.slice(5,7)].toUpperCase() + ' ' + String(+DATE.slice(8,10)); // "AUG 26"
const DATETXT = MON[DATE.slice(5,7)] + ' ' + String(+DATE.slice(8,10)) + ', ' + DATE.slice(0,4); // "Aug 26, 2026"

let ws, idc = 0, page = null;
async function conn() {
  const list = await (await fetch('http://127.0.0.1:9222/json/list')).json();
  page = list.find(t => t.type === 'page' && t.url.includes('app.optionalpha.com'));
  if (!page) throw new Error('NO_OA_PAGE');
  ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);
}
const PRELUDE = `
const sleep=(ms)=>new Promise(r=>setTimeout(r,ms));
const dispatchAt=(el)=>{const r=el.getBoundingClientRect();
 const x=r.left+r.width/2,y=r.top+r.height/2;
 const t=document.elementFromPoint(x,y)||el;
 for(const e of['pointerover','pointerdown','mousedown','pointerup','mouseup','click'])
  t.dispatchEvent(new(e.startsWith('pointer')?PointerEvent:MouseEvent)(e,
   {bubbles:true,cancelable:true,clientX:x,clientY:y,button:0,pointerId:1}));};`;
function ev(body, timeout = 45000) {
  return new Promise((resolve, reject) => {
    const id = ++idc;
    const timer = setTimeout(() => reject(new Error('EVAL_TIMEOUT')), timeout);
    const h = e => { const m = JSON.parse(e.data); if (m.id === id) {
      ws.removeEventListener('message', h); clearTimeout(timer); resolve(m.result); } };
    ws.addEventListener('message', h);
    ws.send(JSON.stringify({ id, method: 'Runtime.evaluate', params: {
      expression: `(async()=>{${PRELUDE}\nreturn await(async()=>{\n${body}\n})()})()`,
      returnByValue: true, awaitPromise: true, timeout: timeout - 3000 } }));
  }).then(r => {
    if (r?.exceptionDetails) throw new Error('EVAL_ERR: ' + r.exceptionDetails.exception?.description);
    return r?.result?.value;
  });
}
const nav = async (url, ms = 6000) => {
  try { await ev(`location.href=${JSON.stringify(url)};return 'nav';`, 5000); } catch (_) {}
  await new Promise(r => setTimeout(r, ms));
};
const assertLogin = async () => {
  const u = await ev('return location.href');
  if (/\/login/.test(u)) throw new Error('LOGIN_REQUIRED — stop');
};

// ---------- §2: positions ----------
async function section2() {
  await nav('https://app.optionalpha.com/positions/closed', 6000);
  // Load more until the group AFTER the target appears (target group complete),
  // or Load more vanishes. Chunked to stay under eval timeouts.
  for (let i = 0; i < 12; i++) {
    const st = await ev(`
const bd=document.querySelector('grid#bots-postabs-closed-grid bd');
const hdrs=[...bd.querySelectorAll('.rowhd')].map(h=>h.innerText.trim().toUpperCase());
const target=${JSON.stringify(DATEHDR)};
let clicks=0,last=bd.querySelectorAll('row.pos').length;
const mi=hdrs.indexOf(target);
while((mi<0||hdrs.length<=mi+1)&&clicks<12){
 const lm=[...document.querySelectorAll('a.loadmore,.loadmore')].find(e=>e.offsetParent!==null);
 if(!lm)break;dispatchAt(lm);clicks++;await sleep(2200);
 const n=bd.querySelectorAll('row.pos').length;if(n===last)break;last=n;
 const h2=[...bd.querySelectorAll('.rowhd')].map(h=>h.innerText.trim().toUpperCase());
 const mi2=h2.indexOf(target);if(mi2>=0&&h2.length>mi2+1)break;
 hdrs.length=0;hdrs.push(...h2);}
return {clicks,hdrs:hdrs.slice(-3),rows:last};`);
    if (st.hdrs.includes(DATEHDR) && st.hdrs.indexOf(DATEHDR) < st.hdrs.length - 1) break;
    if (i === 11 && !st.hdrs.includes(DATEHDR)) return { error: 'target date group not loaded', st };
    if (st.clicks === 0 && !st.hdrs.includes(DATEHDR)) return { error: 'load-more stalled', st };
    if (st.hdrs.includes(DATEHDR)) break;
  }
  // collect target rows in the target group
  const rows = await ev(`
const bd=document.querySelector('grid#bots-postabs-closed-grid bd');let cur=null;const out=[];
for(const k of[...bd.children]){
 if(k.classList&&k.classList.contains('rowhd')){cur=k.innerText.trim();continue;}
 if(k.tagName!=='ROW'||cur!==${JSON.stringify(DATEHDR)})continue;
 const bot=k.querySelector('i[title]')?.getAttribute('title');
 if(bot===${JSON.stringify(BOT)})out.push({key:k.getAttribute('data-key'),
  close:k.querySelector('.closeDate desc[title]')?.getAttribute('title'),
  text:k.innerText});}
return out;`);
  const positions = [];
  for (const r of rows) {
    // close anything open first, then open THIS row, then VERIFY strikes/side
    const p = await ev(`
const cb=[...document.querySelectorAll('a.btn.gray.close')].find(e=>e.offsetParent!==null);
if(cb){dispatchAt(cb);await sleep(2000);}
const row=document.querySelector('row[data-key="${r.key}"]');
row.scrollIntoView({block:'center'});await sleep(900);
dispatchAt(row.querySelector('.closeDate')||row);await sleep(2200);
const v=[...document.querySelectorAll('view.pos-view')].find(x=>x.offsetParent!==null);
return v?v.innerText:'NO_VIEW';`, 30000);
    const posText = typeof p === 'string' ? p : '';
    // VERIFY: row text's first strike must appear in the drawer (trap check)
    const firstStrike = (r.text.match(/\d,\d{3}|\d{3}/) || [])[0];
    if (firstStrike && !posText.includes(firstStrike)) {
      positions.push({ key: r.key, error: 'STALE_DRAWER — retry needed', got: posText.slice(0, 120) });
      continue;
    }
    // every trade's automation log, all pager iterations
    const logs = await ev(`
const items=[...document.querySelector('view.pos-view').querySelectorAll('ct.trades item')];
const out=[];
for(const it of items){
 const link=it.querySelector('a.tlink[data-click="showAutoLog"]');if(!link)continue;
 link.scrollIntoView({block:'center'});await sleep(600);dispatchAt(link);await sleep(2200);
 const lv=document.querySelector('view.logentry-view');
 const iters=[lv?lv.innerText:'NO_LOG'];
 for(let i=0;i<8;i++){
  const nx=lv&&lv.querySelector('[data-click="nextRepeatItem"]');
  if(!nx||nx.className.includes('disabled'))break;
  dispatchAt(nx);await sleep(1500);iters.push(lv.innerText);}
 const cl=document.querySelector('overlay.drawer.logentry a.btn.gray.tool.close');
 if(cl&&cl.offsetParent!==null){dispatchAt(cl);await sleep(1200);}
 out.push({trade:it.innerText,iterations:iters});}
return out;`, 120000);
    positions.push({ key: r.key, rowText: r.text, details: posText, logs });
  }
  await ev(`
const cb=[...document.querySelectorAll('a.btn.gray.close')].find(e=>e.offsetParent!==null);
if(cb)dispatchAt(cb);return 1;`);
  return positions;
}

// ---------- §3: bot log ----------
async function section3(botId) {
  await nav(`https://app.optionalpha.com/bots/bot/${botId}/log?date=${DATE}`, 6000);
  for (let i = 0; i < 10; i++) {                       // ~50 rows/load
    const st = await ev(`
const bd=document.querySelector('grid.botlog bd.dim-scroller');
const rows=[...bd.querySelectorAll('row.logitem')];
const lastT=rows.length?rows[rows.length-1].innerText.split('\\n')[0]:'';
const m=t=>{const x=t.match(/(\\d+):(\\d\\d)(AM|PM)/);return x?((+x[1])%12+(x[3]==='PM'?12:0))*60+(+x[2]):1e9};
let clicks=0;
while(m(lastTcheck())>m('13:20PM')&&clicks<8){   // buffer below window
 const lm=[...document.querySelectorAll('a.loadmore,.loadmore')].find(e=>e.offsetParent!==null);
 if(!lm)break;const n=rows.length;dispatchAt(lm);clicks++;await sleep(2000);
 if(bd.querySelectorAll('row.logitem').length===n)break;
 function lastTcheck(){const r=[...bd.querySelectorAll('row.logitem')].pop();return r?r.innerText.split('\\n')[0]:''}}
return {clicks,last:lastTcheck(),n:bd.querySelectorAll('row.logitem').length};
function lastTcheck(){const r=[...bd.querySelectorAll('row.logitem')].pop();return r?r.innerText.split('\\n')[0]:''}`, 60000);
    if (!st || st.clicks === 0) break;
  }
  const list = await ev(`
return [...document.querySelectorAll('grid.botlog bd.dim-scroller row.logitem')]
 .map(e=>e.innerText);`);
  // decision texts: rows whose time is in the target minutes (caller filters)
  return { rows: list,
    openRun: async (idx) => ev(`
const rows=[...document.querySelectorAll('grid.botlog bd.dim-scroller row.logitem')];
const ex=document.querySelector('overlay.drawer.logentry a.btn.gray.tool.close');
if(ex&&ex.offsetParent!==null){dispatchAt(ex);await sleep(1000);}
const row=rows[${idx}];row.scrollIntoView({block:'center'});await sleep(500);
const cells=[...row.querySelectorAll('div,.cell')].filter(e=>e.offsetParent!==null
 &&!e.querySelector('a.autolink')&&!e.closest('a.autolink')&&e.innerText.trim());
dispatchAt(cells[cells.length-1]);await sleep(2200);
const lv=document.querySelector('view.logentry-view');const iters=[lv?lv.innerText:'NO_LOG'];
for(let i=0;i<8;i++){const nx=lv&&lv.querySelector('[data-click="nextRepeatItem"]');
 if(!nx||nx.className.includes('disabled'))break;dispatchAt(nx);await sleep(1500);iters.push(lv.innerText);}
return {row:row.innerText,iterations:iters};`, 60000) };
}

// ---------- §5: backtest rows ----------
async function section5() {
  const out = [];
  for (const id of TESTS) {
    await nav(`https://app.optionalpha.com/backtests/test/${id}`, 6500);
    const r = await ev(`
const res=document.querySelector('view.bots-ztresults');
const name=res&&res.querySelector('item.tdesc');
const t=document.body.innerText;const si=t.lastIndexOf('Settings');
const seg=si>=0?t.slice(si):t;const i=seg.indexOf('Exit Options');
const link=[...document.querySelectorAll('a[data-click="showPositions"]')].find(e=>e.offsetParent!==null);
if(link&&!document.querySelector('grid[id*="posgrid"]')){dispatchAt(link);await sleep(3000);}
const rows=[...document.querySelectorAll('grid[id*="posgrid"] row')];
const aug=rows.filter(e=>e.innerText.includes(${JSON.stringify(DATETXT)})).map(e=>({
 txt:e.innerText,status:e.querySelector('.status .lbl')?.innerText,
 risk:e.querySelector('.risk .val')?.innerText,pnl:e.querySelector('.pnl .val')?.innerText,
 legs:[...e.querySelectorAll('.strike')].map(s=>({side:s.className.includes('long')?'long':(s.className.includes('short')?'short':'?'),txt:s.innerText}))}));
return {name:name?name.innerText.trim():null,
 exit:i>=0?seg.slice(i,i+80).split('\\n').filter(Boolean).slice(0,4).join(' | '):null,
 nRows:rows.length,aug};`, 45000);
    out.push({ id, ...r });
  }
  return out;
}

const main = async () => {
  await conn(); await assertLogin();
  const out = { bot: BOT, date: DATE };
  out.s2_positions = await section2();
  const botId = args.botid || '';                        // roster-derived id
  out.s3_botlog = botId ? await section3(botId) : 'provide --botid=';
  out.s5_backtests = await section5();
  console.log(JSON.stringify(out, null, 1));
};
main().catch(e => { console.error('FATAL', e.message); process.exit(1); });
