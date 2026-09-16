// oa_grab_page.js — the OA Grab instrument, as a page-context expression.
//
// Logic is a transcription of the `OA Grab` bookmarklet v2.1 (ancestor-climb,
// 2026-08-09) from docs/oa-ops-runbook.md §1.2. The ONLY difference: instead of
// building a Blob and clicking a download link, it RETURNS the capture. Output
// text is byte-identical to what the bookmarklet writes to Downloads.
//
// Read-only. Queries the DOM. Dispatches no events. Saves nothing to OA.
//
// Two ways to use it:
//   1. node oa_capture.mjs roster        (the runner reads this file and evaluates it)
//   2. paste the whole file into a Playwright MCP `browser_evaluate` call, or into
//      the DevTools console, and read the returned object.
//
// If the runbook's instrument changes, change it HERE and nowhere else.

(function () {
  var h = document.querySelector('h1,h2');
  var n = ((h && h.innerText) || document.title || 'oa').trim().replace(/[^\w\-]+/g, '_').slice(0, 60);
  var d = new Date().toISOString().slice(0, 19).replace(/[:T]/g, '-');
  var t = '# ' + n + '\n' + location.href + '\ncaptured: ' + new Date().toString() + '\n\n' + document.body.innerText;
  var seen = {}, g = [];
  document.querySelectorAll('a[href^="/bots/bot/"]').forEach(function (a) {
    var id = (a.getAttribute('href') || '').split('/').pop();
    if (!id || !/^BOT/.test(id) || seen[id]) return;
    var row = a, i, ic;
    for (i = 0; i < 8 && row; i++) {
      ic = row.querySelectorAll ? row.querySelectorAll('i.sticon[title]') : [];
      if (ic.length >= 2) break;
      row = row.parentElement;
    }
    if (!row || !ic || ic.length < 2 || ic.length > 4) return;
    seen[id] = 1;
    g.push(id + '\t' + (ic[0].getAttribute('title') || '') + '\t' + (ic[1].getAttribute('title') || ''));
  });
  if (g.length) {
    t += '\n\n# AUTOS/EXITS -- i.sticon title attribute, S0b-3 fix v2.1 (ancestor-climb 2026-08-09), additive. bot_id\tautos_title\texits_title\n' + g.join('\n') + '\n';
  }
  return { name: n, stamp: d, text: t, rows: g.length, url: location.href };
})()
