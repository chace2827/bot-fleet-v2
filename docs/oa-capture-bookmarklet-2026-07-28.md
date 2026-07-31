# OA Config Capture — bookmarklet + methods

## Why Ctrl+S failed

`Ctrl+S` ("Save Page As") **re-fetches the document from the server**. It does not save what's on your screen. Option Alpha renders the automation trees *client-side*, after you click into an automation — so a saved copy of the template overview page contains the automation **names** and nothing else. Confirmed by probing your saved file: `FOMC`, `11:00am`, `Loop QQQ`, `Profit Taking`, `50% of credit` — none present.

**The fix is not a different service. It's capturing the live DOM instead of re-fetching the URL, with the tree already expanded on screen.**

---

## Method 1 — The bookmarklet (recommended)

One click, no install, outputs **text** (not an image), downloads straight to your Downloads folder.

### Install
1. Chrome → Bookmarks → **Bookmark Manager** (`⌥⌘B`)
2. ⋮ menu → **Add new bookmark**
3. Name: `OA Grab`
4. URL: paste the entire line below

```
javascript:(function(){var h=document.querySelector('h1,h2');var n=((h&&h.innerText)||document.title||'oa').trim().replace(/[^\w\-]+/g,'_').slice(0,60);var d=new Date().toISOString().slice(0,19).replace(/[:T]/g,'-');var t='# '+n+'\n'+location.href+'\ncaptured: '+new Date().toString()+'\n\n'+document.body.innerText;var b=new Blob([t],{type:'text/plain'});var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='oa_'+n+'_'+d+'.txt';document.body.appendChild(a);a.click();a.remove();})()
```

### Use
1. Open an automation so the **full tree is visible on screen**
2. Expand every collapsed node (the `^` carets) — collapsed nodes may not be in the DOM
3. Click **OA Grab**
4. A `.txt` lands in Downloads, named after the automation, timestamped

Repeat per automation. For 4 bots × 4 automations that's ~16 clicks, once.

### What you get
Plain text containing the decision nodes verbatim — `FOMC Meeting today`, `Current market time is after 11:00am`, `Position is more than $1 in the money`, `Profit Taking % 50% of credit`, etc. Diffable, greppable, git-trackable. **No OCR, no screenshots, no parsing images.**

---

## Method 2 — Ctrl+P → Save as PDF

Zero install, works right now.

`⌘P` → Destination: **Save as PDF** → Save.

Prints the **rendered** page, so unlike Ctrl+S it captures what you can see. The text stays selectable, which means it can be parsed directly rather than OCR'd. Slightly lossier than the bookmarklet (page-break artifacts, layout noise) but perfectly workable.

**Use this for the Exit Options modal**, which the bookmarklet may miss if the modal renders in a separate layer.

---

## Method 3 — SingleFile extension

[SingleFile](https://chromewebstore.google.com/detail/singlefile/mpiodijhokgodhhofbcjdecpffjipkle) ([source](https://github.com/gildas-lormeau/SingleFile)) saves **the current DOM state**, not a re-fetch — exactly the thing Ctrl+S doesn't do. One click → one self-contained `.html`.

Better than Ctrl+S. Heavier than the bookmarklet (saves CSS/images/fonts you don't need). Worth it if you want a visual archive alongside the text.

---

## Method 4 — DevTools, for one-off precision

Right-click the automation container → **Inspect** → right-click the highlighted node → **Copy → Copy outerHTML**.

Highest fidelity, gets the exact subtree. Fine for one automation, tedious for sixteen.

Console equivalent, if you prefer typing:
```js
copy(document.body.innerText)
```
Puts the whole rendered page text on your clipboard. Paste anywhere.

---

## What NOT to use

**Image-based screenshot tools** — GoFullPage, Awesome Screenshot, Fireshot, and the region-capture services you asked about. They produce PNGs, which means OCR, which means transcription errors in exactly the place errors are most expensive: strike prices, percentages, thresholds. **You already proved images work** — you've been sending them and I've been reading them — but they don't diff, don't grep, and don't version. Text does all three.

The one case for images: an Exit Options panel that renders in a way text capture mangles. Fall back to Method 2 first.

---

## The capture ritual

Once the account is active again, this becomes ~15 minutes per full sweep:

1. Open bot → Settings → Automations
2. For each automation: open it, expand all nodes, click **OA Grab**
3. Open the Open Position action → Exit Options → `⌘P` → Save as PDF
4. Drop the folder into `data/oa_config_snapshots/<date>/`
5. Commit

Then a diff against the previous snapshot **is** your drift detector — the thing that would have caught PT25 dying, HedgeD's missing Range075, and Bot 2's unattached call-side PT50, on day one instead of month four.

Sources: [SingleFile — Chrome Web Store](https://chromewebstore.google.com/detail/singlefile/mpiodijhokgodhhofbcjdecpffjipkle) · [SingleFile — GitHub](https://github.com/gildas-lormeau/SingleFile) · [getsinglefile.com](https://www.getsinglefile.com/)
