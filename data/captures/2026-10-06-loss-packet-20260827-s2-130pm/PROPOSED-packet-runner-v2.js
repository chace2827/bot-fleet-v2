#!/usr/bin/env node
// PROPOSED-packet-runner-v2 — loss-packet browser runner, v2.
// Produces §2 (positions+trades+autologs+leg classes+UTC ids), §3 (run list +
// close-minute decision texts serialized into JSON) and §5 (backtest rows with
// absence-proof paging) as JSON on stdout.
//
//   node PROPOSED-packet-runner-v2.js --bot IC-SPX-FastPT25-S2-130PM \
//     --botid BOT... --date 2026-08-27 --minutes 2:27PM,2:28PM \
//     --tests ZTid1,ZTid2,...
//
// v2 fixes (recorded 2026-10-06 in 00-runner-pilot.txt of this bundle):
//   1. Args: both `--k v` and `--k=v` work (v1 silently took `true` on spaces).
//   2. Process exits: ws.close + explicit exit after printing (v1 leaked the
//      CDP WebSocket and hung forever).
//   3. §3 decision texts are now SERIALIZED: --minutes=H:MMPM,... opens those
//      rows' INFO cells and captures every pager iteration inline (v1 returned
//      openRun as a callback — invisible in JSON — needing a second script).
// v2 gap-closures (also recorded in 00-runner-pilot.txt):
//   4. §2 captures leg side classes (.strike flex long|short), trade item
//      data-id, and em.from[data-value] UTC timestamps — removes the second
//      §2 pass used on the 08-27 run.
//   5. §5 pages the positions grid with an absence PROOF: sorted newest-first,
//      stop when the oldest loaded row predates the target date (absent) or
//      the target appears; emits coverage. v1 read only the first 100 rows.
//   6. Emits out.timings — per-section ms + total, so the next run answers
//      "which section is slowest" with numbers, not estimates.
//
// Preconditions: Chrome on :9222 logged into app.optionalpha.com, PAPER account.
// READ-ONLY: clicks Load more, position rows, INFO cells, showPositions, pager.
// Never: automation-name links, Save, toggles, Clear Log, Create Bot, exports.

const argv = process.argv.slice(2);
const args = {};
for (let i = 0; i < argv.length; i++) {
  const m = argv[i].match(/^--(\w+)(?:=(.*))?$/);
  if (!m) continue;
  if (m[2] !== undefined) args[m[1]] = m[2];
  else if (argv[i + 1] && !argv[i + 1].startsWith('--')) args[m[1]] = argv[++i];
  else args[m[1]] = true;
}
const BOT = args.bot, DATE = args.date, BOTID = args.botid || '';
const TESTS = String(args.tests || '').split(',').filter(Boolean);
const MINUTES = String(args.minutes || '').split(',').filter(Boolean);
if (!BOT || !DATE) { console.error('need --bot --date'); process.exit(1); }
const MON = { '01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun',
  '07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec' };
const DATEHDR = MON[DATE.slice(5,7)].toUpperCase() + ' ' + String(+DATE.slice(8,10)); // "AUG 27"
const DATETXT = MON[DATE.slice(5,7)] + ' ' + String(+DATE.slice(8,10)) + ', ' + DATE.slice(0,4); // "Aug 27, 2026"

let ws, idc = 0;
async function conn() {
  const list = await (await fetch('http://127.0.0.1:9222/json/list')).json();
  const page = list.find(t => t.type === 'page' && t.url.includes('app.optionalpha.com'));
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

// ---------- §2: positions (with leg classes + trade UTC ids) ----------
async function section2() {
  await nav('https://app.optionalpha.com/positions/closed', 6000);
  for (let i = 0; i < 12; i++) {
    const st = await ev(`
const bd=document.querySelector('grid#bots-postabs-closed-grid bd');
const hdrs=[...bd.querySelectorAll('.rowhd')].map(h=>h.innerText.trim().toUpperCase());
const target=${JSON.stringify(DATEHDR)};
let clicks=0,last=bd.querySelectorAll('row.pos').length;
let mi=hdrs.indexOf(target);
while((mi<0||hdrs.length<=mi+1)&&clicks<12){
 const lm=[...document.querySelectorAll('a.loadmore,.loadmore')].find(e=>e.offsetParent!==null);
 if(!lm)break;dispatchAt(lm);clicks++;await sleep(2200);
 const n=bd.querySelectorAll('row.pos').length;if(n===last)break;last=n;
 const h2=[...bd.querySelectorAll('.rowhd')].map(h=>h.innerText.trim().toUpperCase());
 mi=h2.indexOf(target);if(mi>=0&&h2.length>mi+1)break;}
return {clicks,done:mi>=0,complete:mi>=0&&hdrs.length>mi+1,rows:last,
 tail:[...bd.querySelectorAll('.rowhd')].slice(-3).map(h=>h.innerText)};`);
    if (st.complete) break;
    if (i === 11) return { error: 'target date group not loaded', st };
    if (st.clicks === 0 && !st.complete) return { error: 'load-more stalled', st };
  }
  const rows = await ev(`
const bd=document.querySelector('grid#bots-postabs-closed-grid bd');let cur=null;const out=[];
for(const k of[...bd.children]){
 if(k.classList&&k.classList.contains('rowhd')){cur=k.innerText.trim();continue;}
 if(k.tagName!=='ROW'||cur!==${JSON.stringify(DATEHDR)})continue;
 const bot=k.querySelector('i[title]')?.getAttribute('title');
 if(bot===${JSON.stringify(BOT)})out.push({key:k.getAttribute('data-key'),
  text:k.innerText});}
return out;`);
  const positions = [];
  for (const r of rows) {
    let rec = null;
    for (let attempt = 0; attempt < 2; attempt++) {          // stale-drawer retry
      const p = await ev(`
const cb=[...document.querySelectorAll('a.btn.gray.close')].find(e=>e.offsetParent!==null);
if(cb){dispatchAt(cb);await sleep(2000);}
const row=document.querySelector('row[data-key="${r.key}"]');
row.scrollIntoView({block:'center'});await sleep(900);
dispatchAt(row.querySelector('.closeDate')||row);await sleep(2200);
const v=[...document.querySelectorAll('view.pos-view')].find(x=>x.offsetParent!==null);
if(!v)return{err:'NO_VIEW'};
return{details:v.innerText,
 legs:[...v.querySelectorAll('.strike')].map(s=>({txt:s.innerText,cls:s.className,title:s.getAttribute('title')})),
 trades:[...v.querySelectorAll('ct.trades item')].map(it=>({txt:it.innerText,
  id:it.getAttribute('data-id'),
  ts:it.querySelector('em.from')?.getAttribute('data-value')||it.querySelector('em.from')?.getAttribute('title')||null}))};`, 30000);
      const firstStrike = (r.text.match(/\d,\d{3}|\d{3}/) || [])[0];
      if (p && p.details && firstStrike && !p.details.includes(firstStrike)) {
        if (attempt === 0) continue;                          // stale view — retry
        rec = { key: r.key, rowText: r.text, error: 'STALE_DRAWER', got: (p.details || '').slice(0, 120) };
        break;
      }
      rec = { key: r.key, rowText: r.text, ...p };
      break;
    }
    if (rec && !rec.error) {
      rec.logs = await ev(`
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
 out.push({trade:it.innerText,id:it.getAttribute('data-id'),iterations:iters});}
return out;`, 120000);
    }
    positions.push(rec);
  }
  await ev(`
const cb=[...document.querySelectorAll('a.btn.gray.close')].find(e=>e.offsetParent!==null);
if(cb)dispatchAt(cb);return 1;`);
  return positions;
}

// ---------- §3: bot log — run list (13:20-bounded) + decision texts ----------
async function section3(botId) {
  await nav(`https://app.optionalpha.com/bots/bot/${botId}/log?date=${DATE}`, 6000);
  // Load until the last row is at/before 13:20 (covers the 13:25 window edge)
  // or the day runs out. Decision texts need only loaded rows — for a bot
  // that goes flat at the close they're on the FIRST page.
  for (let i = 0; i < 10; i++) {
    const st = await ev(`
const bd=document.querySelector('grid.botlog bd.dim-scroller');
const lastT=()=>{const r=[...bd.querySelectorAll('row.logitem')].pop();return r?r.innerText.split('\\n')[0]:''};
const m=t=>{const x=t.match(/(\\d+):(\\d\\d)(AM|PM)/);return x?((+x[1])%12+(x[3]==='PM'?12:0))*60+(+x[2]):1e9};
let clicks=0;
while(m(lastT())>800&&clicks<8){
 const lm=[...document.querySelectorAll('a.loadmore,.loadmore')].find(e=>e.offsetParent!==null);
 if(!lm)break;const n=bd.querySelectorAll('row.logitem').length;dispatchAt(lm);clicks++;await sleep(2000);
 if(bd.querySelectorAll('row.logitem').length===n)break;}
return {clicks,last:lastT(),n:bd.querySelectorAll('row.logitem').length};`, 60000);
    if (!st || st.clicks === 0) break;
  }
  const rows = await ev(`
return [...document.querySelectorAll('grid.botlog bd.dim-scroller row.logitem')]
 .map(e=>e.innerText);`);
  // decision texts for each requested minute — serialized inline (v2 fix 3)
  const decisions = [];
  for (const minute of MINUTES) {
    const idxs = await ev(`
return [...document.querySelectorAll('grid.botlog bd.dim-scroller row.logitem')]
 .map((e,i)=>e.innerText.split('\\n')[0]===${JSON.stringify(minute)}?i:-1).filter(i=>i>=0);`);
    for (const idx of idxs) {
      const r = await ev(`
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
const cl=document.querySelector('overlay.drawer.logentry a.btn.gray.tool.close');
if(cl&&cl.offsetParent!==null){dispatchAt(cl);await sleep(1000);}
return {minute:${JSON.stringify(minute)},row:row.innerText,iterations:iters};`, 60000);
      decisions.push(r);
    }
  }
  return { rows, decisions };
}

// ---------- §5: backtest rows with absence-proof paging ----------
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
const g=document.querySelector('grid[id*="posgrid"]');
if(!g)return{name:name?name.innerText.trim():null,err:'no posgrid'};
const re=${JSON.stringify(DATETXT)};
const MONNUM={Jan:1,Feb:2,Mar:3,Apr:4,May:5,Jun:6,Jul:7,Aug:8,Sep:9,Oct:10,Nov:11,Dec:12};
const rowDate=e=>{const m=e.innerText.match(/([A-Z][a-z]{2}) (\\d+), (\\d{4})/);if(!m)return null;
 return (+m[3])*10000+MONNUM[m[1]]*100+(+m[2]);};   // y*10000+m*100+d, sortable
const iso=v=>Math.floor(v/10000)+'-'+String(Math.floor(v/100)%100).padStart(2,'0')+'-'+String(v%100).padStart(2,'0');
const target=(${DATE.slice(0,4)})*10000+(${+DATE.slice(5,7)})*100+(${+DATE.slice(8,10)});
let clicks=0,exhausted=false,predates=false;
// sorted newest-first: stop when the oldest loaded row predates the target
// (absence proven), a target row exists, or load-more vanishes.
for(let i=0;i<12;i++){
 const rows=[...g.querySelectorAll('row')];
 if(rows.some(e=>e.innerText.includes(re)))break;
 const ds=rows.map(rowDate).filter(Boolean);
 if(ds.length&&Math.min(...ds)<target){predates=true;break;}
 const lm=[...document.querySelectorAll('a.loadmore,.loadmore')].find(e=>e.offsetParent!==null);
 if(!lm){exhausted=true;break;}
 const n=rows.length;dispatchAt(lm);clicks++;await sleep(2200);
 if(g.querySelectorAll('row').length===n){exhausted=true;break;}}
const rows=[...g.querySelectorAll('row')];
const aug=rows.filter(e=>e.innerText.includes(re)).map(e=>({
 txt:e.innerText,status:e.querySelector('.status .lbl')?.innerText,
 risk:e.querySelector('.risk .val')?.innerText,pnl:e.querySelector('.pnl .val')?.innerText,
 legs:[...e.querySelectorAll('.strike')].map(s=>({side:s.className.includes('long')?'long':(s.className.includes('short')?'short':'?'),txt:s.innerText}))}));
const ds=rows.map(rowDate).filter(Boolean);
return {name:name?name.innerText.trim():null,
 exit:i>=0?seg.slice(i,i+80).split('\\n').filter(Boolean).slice(0,4).join(' | '):null,
 nRows:rows.length,oldest:ds.length?iso(Math.min(...ds)):null,
 clicks,predates,exhausted,aug};`, 120000);
    out.push({ id, ...r });
  }
  return out;
}

const main = async () => {
  const T0 = Date.now();
  await conn(); await assertLogin();
  const timings = {};
  const out = { bot: BOT, date: DATE };
  let t = Date.now();
  out.s2_positions = await section2();            timings.s2_ms = Date.now() - t; t = Date.now();
  out.s3_botlog = BOTID ? await section3(BOTID) : 'provide --botid=';
                                                    timings.s3_ms = Date.now() - t; t = Date.now();
  out.s5_backtests = await section5();            timings.s5_ms = Date.now() - t;
  timings.total_ms = Date.now() - T0;
  out.timings = timings;
  console.log(JSON.stringify(out, null, 1));
  try { ws && ws.close(); } catch (_) {}
  process.exit(0);                                // v2 fix 2 — never hang
};
main().catch(e => { console.error('FATAL', e.message); try { ws && ws.close(); } catch (_) {} process.exit(1); });
