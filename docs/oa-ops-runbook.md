# OA ops runbook

*Written 2026-07-31 for Bot Fleet v2. **MERGE** of the archive's `oa-capture-bookmarklet-2026-07-28.md`,
`oa-capture-coverage-2026-07-29.md`, `oa-cleanup-runbook.md`, and the template/group material from
`oa-setup-exploration-2026-07-29.md`. Supersedes all four for operational purposes.*

> **What this is:** how to touch the OA account. The capture ritual, template versioning, the
> group scheme, and the edit-verification procedure.
>
> **What this is not:** what to build (`build-plan.md`, frozen), what the platform can express
> (`oa-platform-reference.md`), or how to read the results (`daily-loop-spec.md`).
>
> **The one rule underneath all of it — AMENDED 2026-08-04, at Andy's explicit instruction:**
> *Claude executes every OA edit directly (Chrome-direct: read, drive, save), and self-verifies it
> before reporting it done.* A save confirmation or tool-success message is never the verification.
> Andy retains authority to revoke direct-edit access, globally or per-bot, at any time. Supersedes
> "Andy makes every OA edit" — see `CLAUDE.md` §5, `build-plan.md` §5.

---

## 1. The capture ritual

### 1.1 Why `Ctrl+S` does not work

`Ctrl+S` **re-fetches the document from the server.** It does not save what is on your screen.
OA renders automation trees **client-side**, after you click into an automation — so a saved
copy of a template overview page contains automation **names and nothing else.** Verified by
probing a saved file: `FOMC`, `11:00am`, `Loop QQQ`, `Profit Taking`, `50% of credit` — **none
present.**

**The fix is not a different service. It is capturing the live DOM, with the tree already
expanded on screen.**

### 1.2 The bookmarklet — the primary instrument

Install once: Chrome → Bookmark Manager (`⌥⌘B`) → ⋮ → Add new bookmark → name it `OA Grab` →
paste as the URL:

```
javascript:(function(){var h=document.querySelector('h1,h2');var n=((h&&h.innerText)||document.title||'oa').trim().replace(/[^\w\-]+/g,'_').slice(0,60);var d=new Date().toISOString().slice(0,19).replace(/[:T]/g,'-');var t='# '+n+'\n'+location.href+'\ncaptured: '+new Date().toString()+'\n\n'+document.body.innerText;var g=[];document.querySelectorAll('a[href^="/bots/bot/"]').forEach(function(a){var id=(a.getAttribute('href')||'').split('/').pop();var row=a.closest('tr')||a.closest('[role="row"]')||a.parentElement;if(!row||!id)return;var ic=row.querySelectorAll('i.sticon[title]');if(ic.length<2)return;g.push(id+'\t'+(ic[0].getAttribute('title')||'')+'\t'+(ic[1].getAttribute('title')||''));});if(g.length){t+='\n\n# AUTOS/EXITS -- i.sticon title attribute, S0b-3 fix, additive. bot_id\tautos_title\texits_title\n'+g.join('\n')+'\n';}var b=new Blob([t],{type:'text/plain'});var el=document.createElement('a');el.href=URL.createObjectURL(b);el.download='oa_'+n+'_'+d+'.txt';document.body.appendChild(el);el.click();el.remove();})()
```

> ### 📝 APPENDED 2026-08-08 — S0b-3 FIX LANDED IN THE INSTRUMENT. ⛔ VERIFY-ON-NEXT-CAPTURE, NOT YET RUN AGAINST LIVE OA.
> **Finding, evidence, ruling:** `session-log.md` S0b-3 (2026-08-07, S0b-RESUME session) — the
> `/bots` rows emit 18 values, not 20, because the AUTOS/EXITS cells are icons with no text node,
> but the state is on `i.sticon`'s `title` attribute. Ruled `day0-session-pack-2026-08-07.md`
> §0.0 A-27(d): *"the bookmarklet must read the icon `title` attribute, not `innerText`…
> Implementing it is Claude Code's lane (`CLAUDE.md` §7)."*
>
> **The change above, additive only.** On any page, the prefix — name header, URL, `captured:`
> line, blank line, full `document.body.innerText` — is byte-identical to the prior version. A
> new trailing section is appended **only when** `a[href^="/bots/bot/"]` rows carrying two
> `i.sticon[title]` elements are found — i.e. only on `/bots`; zero elsewhere, so output on
> every other page this bookmarklet is used on (automation-tree captures included) is unchanged.
> Example output line, appended verbatim per bot, tab-separated:
> ```
> BOTfw5TkkCRF3317782764426812572	Scheduled automations are off	Exit Options for positions managed by this bot are off
> ```
> §1.5's "AUTOS/EXITS counts — the highest-value miss" and §1.6's "does not survive text
> capture" are **left standing, not amended** — both describe the OLD capture and remain true of
> it; this is new output, not a correction to those claims.
>
> **Readers checked, no restructure needed.** Grepped `scripts/*.py` for `oa_Bots`, `innerText`,
> `sticon`, `AUTOS`, `EXITS`, and `/bots`-roster patterns: no script parses the `/bots` list-view
> capture programmatically. `data/bots_config_v2.csv` is built from PER-BOT automation-tree
> captures via `a_series.py`'s `classify_and_parse` (`BOT_ID` / `BOT GF-QQQ-IC-` / `AUTOMATION
> GF-` markers) — a different capture class, unaffected. `build_ledger.py`'s `data/bots.csv` is
> built from the ledger / Export Data, not this capture — unaffected. The only consumers of the
> raw `/bots` capture text today are first-hand human/Claude reads (S0a Step 3; the STEP 4b manual
> field-by-field diff) — an appended trailing section changes nothing read from the unchanged
> prefix.
>
> **Unit-checked, not live-verified.** The extraction/tab-join logic was run against a synthetic
> DOM shaped exactly to the documented `i.sticon[title]` strings (`session-log.md` S0b-3 / the
> s0b toggle TSV comment) and reproduces the expected line shape exactly. **What this does NOT
> prove: that the real `/bots` DOM matches the assumed selectors** — `a[href^="/bots/bot/"]` as
> the row anchor, `tr` as the row container, exactly two `i.sticon[title]` per row in
> AUTOS-then-EXITS order. Captures are Andy's hand (A-22); this cannot be run against live OA
> from here.
> ⛔ **VERIFY-ON-NEXT-CAPTURE.** The next `/bots` bookmarklet pull either produces the trailing
> section above (fix confirmed) or the unchanged old-format output with zero new lines (selectors
> wrong — a new finding, not a silent failure, since the `document.body.innerText` prefix is
> unaffected either way).

Use:
1. Open the automation so **the full tree is visible on screen**.
2. **Expand every collapsed node** (the `^` carets). ⚠️ **Collapsed nodes may not be in the DOM
   at all** — an unexpanded caret is a silently missing branch, and it will not announce itself.
3. Click **OA Grab**. A timestamped `.txt` lands in Downloads.

You get the decision nodes verbatim — `FOMC Meeting today`, `Current market time is after
11:00am`, `Position is more than $1 in the money`, `Profit Taking % 50% of credit`. **Diffable,
greppable, git-trackable.**

### 1.3 The three fallbacks, and when each is right

| Method | Use it for |
|---|---|
| **`⌘P` → Save as PDF** | **The Exit Options modal**, which the bookmarklet may miss if the modal renders in a separate layer. Prints what is *rendered*, text stays selectable. |
| **SingleFile extension** | A visual archive alongside the text. Saves current DOM state, not a re-fetch. Heavier than needed for config. |
| **DevTools → Copy outerHTML** | One-off precision on a single subtree. Tedious past one automation. Console equivalent: `copy(document.body.innerText)`. |

### 1.4 ⛔ What NOT to use — image screenshot tools

GoFullPage, Awesome Screenshot, Fireshot and the region-capture services all produce PNGs, which
means OCR, which means **transcription errors in exactly the place errors are most expensive:
strike prices, percentages, thresholds.** Images do not diff, do not grep, and do not version.
Text does all three.

**The one exception is a screenshot you cannot get any other way — see §1.6.**

### 1.5 Page-by-page coverage — what the bookmarklet actually gets

Tested against three live captures with matching screenshots, 2026-07-28.

| Page | Verdict | Use it for |
|---|---|---|
| **`/bots`** | **Strong** — 35/35 bots, **18 fields each**, fixed schema, no heuristics | The roster authority and the per-bot drift diff |
| **`/positions/analyze`** | **Weak** — scalars survive, **every chart dies** | **Nothing. Use Export Data.** |
| **Day drill-down modal** | **Strong but anonymous** — 27/27 rows, **no bot ID** | Intraday sequence forensics, single-bot-filtered only |

**`/bots` schema, 18 fields per bot, consistent across full-data, partial-data and zero-trade bots:**
```
name, TOTAL_PL, RETURN_PCT, CLOSED_PL, CLOSED_PCT, CHANGE, CHANGE_PCT,
POS, RISK, ALLOCATION, WIN_RATE, BETA_WEIGHT, BETA_EXPOSURE,
AVG_PL, AVG_WIN, AVG_LOSS, P_FACTOR, STREAK, CLOSED
```

**What `/bots` loses — know these before trusting a capture:**

| Lost | Consequence |
|---|---|
| **`AUTOS` / `EXITS` counts** | **The highest-value miss.** This is the column that would have flagged `QQQ-IC-0DTE-HedgeC-S3` having zero monitors. |
| **ON/OFF toggle state** | The capture **cannot** tell a switched-off bot from a correctly-gated one. `DIR-SPX-PutVIX22-SL75` emits all dashes. §1.6 exists for this. |
| Live/Paper per bot | Only inferable from the global filter chip |
| Bot Group membership | No trace |
| **Precision above $10K** | `-$11.2K`, `-$31.6K` — 3 significant figures. **A move from −$11,200 to −$11,249 will not diff.** Sub-$10K values are exact. |

> ### 📝 APPENDED 2026-08-08 — the AUTOS/EXITS miss above has a fix in the instrument now; table above LEFT STANDING (still true of the OLD capture).
> §1.2's banner has the change, the evidence, the readers checked, and the unit-check. ⛔
> VERIFY-ON-NEXT-CAPTURE — not yet run against live OA.

**Normalise before diffing**, or you get false positives every single day: strip the `captured:`
line, the sidebar clock, the `Opportunities N` counter, the two-line *"Account inactive, no
changes will be saved / See plans"* banner, the footer *"N active bots • N left in your plan •
Upgrade"*, and any hover tooltip that happened to be in the DOM.

⚠️ **`/positions/analyze` also fails to capture its own filter state** — eight dropdowns, and the
text gets two. **The file then records numbers without recording what produced them.** Numbers
whose scope cannot be reconstructed are precisely the failure class this project exists to
eliminate. Do not use the bookmarklet on that page.

### 1.6 Toggle screenshots — the one place images are mandatory

**`AUTOMATIONS` and `EXIT OPTIONS` toggle state does not survive text capture.** It is the single
config state that does not, and it is the state that killed v1.

**Per bot: screenshot both toggles.** File as `data/captures/toggles/<date>/<bot>.png`.

⚠️ **A toggle screenshot is necessary and not sufficient.** The per-bot `EXIT OPTIONS` toggle is
a **single-source claim** — one OA support rep, absent from OA's documentation entirely
(`oa-platform-reference.md` §10). If it is not on the dashboard at Day-0, the lapse mechanism is
**unexplained, not solved.** Keep §4's order-level verification as the actual proof.

> ### ⛔ CONTESTED 2026-08-05 — "single-source" and "absent from OA's documentation" are BOTH false.
> **The toggle is [DOCUMENTED].** Verbatim, `tools/managing-positions/exit-options`:
> > *"Exit Options always run, even if your automations inside a bot are turned off… **unless you
> > turn off Exit Options in your bot**"* — **OA-0871**
> > *"Additionally, you can enable and disable Exit Options from **the main Bots page, inside of
> > the bot** as shown below, or individually within each position"* — **OA-0896**
>
> Three documented control surfaces, one of them bot-level. The 2026-07-31 sweep missed the page.
> "Single-source" was already wrong on a second count — `oa-platform-reference.md` §10 has carried
> **[FIRST-HAND ×2]** since 2026-07-31 (the rep's screenshot + Andy's fleet-wide read of all 35
> bots). This paragraph had been lagging its own cited source.
>
> ✅ **What does NOT change — the operative half of this warning stands.** The *causal* lapse claim
> — that resubscription restores only `AUTOMATIONS` — is still **UNSOURCED** (R-10: zero corpus
> facts on subscription lapse, deactivation or billing state). **§4's order-level verification
> remains the only actual proof and is not weakened by this correction.**
> `oa-reconciliation-report.md` R-01 · `data/oa_facts.csv` sha256 `435abe0d…3527b`.

### 1.7 Export Data — the ledger source

`Export Data`, **all bot groups selected**, → `data/raw/YYYY-MM-DD.csv`.

- **`botName` is column 1 of 26.** Attribution is direct; no reconstruction needed.
- `highReturnPct` / `lowReturnPct` + their dates are **native MFE/MAE**.
- `risk` / `ror` / `ev` ship per position, so R is computed at ingest.
- **Exports work while the subscription is lapsed** — positions closing as late as 7/27 came
  back after the 6/30 lapse.

> ⛔ **THE EXPORT RESPECTS THE BOT-GROUP FILTER.** An export taken with any group deselected is a
> **subset**, and rebuilding the ledger from it would erase the excluded bots' history.
> `build_ledger.py` carries a filtered-export guard that compares against the prior ledger and
> warns loudly — but it can only catch bots that were already there. **Select all groups.**

### 1.8 The sweep, end to end

1. **`/bots` bookmarklet capture first** — it is the roster authority, and the only record
   zero-trade bots will ever have.
2. Per bot: open each automation, **expand every node**, click OA Grab.
3. Open Position action → Exit Options → `⌘P` → Save as PDF.
4. **Both toggle screenshots per bot.**
5. `Export Data`, all groups → `data/raw/YYYY-MM-DD.csv`.
6. Drop everything into `data/captures/<date>/`.
7. Hand off for commit.

**Then the diff against the previous snapshot IS the drift detector** — the thing that would
have caught PT25 dying, HedgeD's missing Range075, and the unattached call-side PT50, on day one
instead of month four.

---

## 2. Template versioning — OA-native, and it replaces the clone scheme

> **This is the single most useful thing in the account that this project was not using.**

OA templates carry a **VERSION counter, LAST UPDATE, Tags, Notes, and History with "Clone
version N" restore.** [FIRST-HAND — screenshot; **the OA docs describe no versioning at all**,
so this is a case where the docs lag the product and the screenshot wins.]

**Why it matters more than it sounds:** the fleet's previous versioning scheme was *clone the
bot and archive the original*. But **the Symbols panel is not carried on clone** — so a
clone-based versioning scheme silently produces a bot that looks configured and never scans.
Template versions have no such failure mode.

### 2.1 The convention

- **Save a template version at every spec change.** Version numbers are the config's identity.
- **The pre-registration goes in Notes**, at V1, **before** the bot runs — hypothesis, kill
  criterion, sample target, review date (`pre-registration-ledger.md` §2).
- **Tags carry the pre-registration ID**, so a template is greppable back to its entry.
- **The capture cites the version.** `bots_config_v2.csv` carries `capture_file` and
  `capture_hash`; the template version is what those describe.

> ### 📝 APPENDED 2026-08-04 — the tag convention collides with an OA platform limit. Ruled.
> **OA normalises tags: lowercase, and every non-alphanumeric becomes a space.** Typing `PR-03`
> into the tag widget offers exactly one suggestion — **`pr 03`**. Every pre-existing account tag
> is consistent with this (`experiment`, `focus ic`, `focus oa mirror`, `focus directional`).
> [FIRST-HAND — observed in the tag widget on template `Tfw5TkkCRF2617858650531245641`,
> 2026-08-04, `session-log.md` 2026-08-04 part 4 finding 5.]
>
> The bullet above and `pre-registration-ledger.md` §2 both assume the **bare** ID in the tag.
> **Not expressible.** This is the substitution-at-a-platform-limit class, so it is documented
> rather than absorbed silently.
>
> **RULED (Andy, 2026-08-04): adopt `pr 03`.** The scheme is **`PR-NN` → `pr nn` in OA tags,
> literal `PR-NN` in Notes.** The tag is a **search handle, not the record** — the record is the
> pre-registration entry pasted verbatim into Notes, which carries the literal `ID   PR-NN` line
> and is what makes the template greppable back to its entry.
>
> Applied on the pilot: template tags read `experiment,pr 03`, verified after a hard reload from
> `input[name=tags].value`; Notes verified byte-exact at 1574/1574 characters after the tag write.

### 2.2 The proposed `BUILD_ID` mirror — and its precondition

Mirror the template VERSION into a non-functional `BUILD_ID` bot input so **the running bot
self-reports which pre-registration it is executing.**

> ⚠️ **The obvious failure: hand-mirroring VERSION into BUILD_ID is a manual step that will be
> forgotten, reproducing the `bots_config.csv` disease in a new location.**
> **Guard: the nightly script asserts `BUILD_ID` == the version named in the current
> pre-registration file, and fails loudly on mismatch.**
> **If that assert is not built, do not build the BUILD_ID mechanism at all.** A self-report
> nobody checks is worse than no self-report — it manufactures confidence.

> ### ✅ APPENDED 2026-08-04 — DO NOT BUILD THIS. OA already mirrors the version natively.
> **Saving a template binds the bot to it and stamps the version on the bot's own settings page.**
> After the pilot's template save, the bot settings page gained a panel reading:
>
> ```
> Template      QQQ-IC-0DTE-Fortress   (→ /bots/templates/Tfw5TkkCRF2617858650531245641)
> BOT VERSION   1  Aug 4, 2026
> ```
>
> [FIRST-HAND — read from the live DOM on `BOTfw5TkkCRF2717857919585029021` after a hard reload,
> 2026-08-04; the panel was absent from the same page before the save.]
>
> **This is exactly what §2.2 wanted, without the step §2.2 correctly predicted would be
> forgotten.** The whole precondition above — build the nightly assert or do not build the
> mechanism — exists because hand-mirroring is a manual step. The platform maintains this field
> itself, so there is no hand-step and no drift to assert against.
>
> **RULED (Andy, 2026-08-04): ACCEPTED — do not build the manual `BUILD_ID` mirror.**
> The §2.2 proposal above is superseded for the VERSION field and is left standing as the record
> of why. If a future need arises for a self-reported value OA does *not* maintain, the assert
> precondition still governs it.

### 2.3 Unverified

> ### ✅ ANSWERED 2026-08-04 — saving a template does NOT disturb the bot.
> Run on the pilot (`BOTfw5TkkCRF2717857919585029021`), which had zero open positions and an
> inactive account — the safest possible moment, as the pilot card intended.
> **Every bot field re-read identical after the save:** 3 automations, same names and same order ·
> Symbols `No symbols yet` · Allocation `$100,000` · Daily 2 per day · Position limit 2 at once ·
> Day trading `Allowed` · scan speeds `Every 1m` / `Every 1m` · `AUTOMATIONS` OFF ·
> `EXIT OPTIONS` ON · all four Activity Alerts on · Tags `experiment`.
> The only change was an **addition**: the `Template` / `BOT VERSION` panel — see §2.2's append.
> [FIRST-HAND — DOM re-read after a hard reload, 2026-08-04.]
> **The "verify on a dead bot first" instruction above has now been discharged. §2.3 is closed;
> the versioning convention is unblocked.**
>
> ⚠️ **What this does NOT answer** is whether the template stores a *reference* to the same
> automation objects as the live bot. The template page's automation rows carry
> `rid=RTfw5TkkCRF2717857919585272551` — **the same object id as the bot's live ScannerA.**
> Whether a later edit to the bot's automation therefore changes what the template describes is
> **UNTESTED**. Do not assume a template is a frozen snapshot until this is checked.

Whether **saving a template from a live bot disturbs the bot** (position count, automation
states) is [EXPECTED, not confirmed]. **Verify on a dead bot before saving a template from a
live one.**

---

## 3. The group scheme — Group = Pillar

OA Bot Group is a **single-select container**: a bot is in exactly one group.

**Convention: `Group = Pillar`** — `IC` · `Directional` · `OA-Mirror` · `Lab`.
Groups must reconcile to `bots_meta.csv`'s `pillar` column, exactly.

**Current state (v1, pre-sweep):** `SPX-IC` and `OA-Mirror` only. The v1 cleanup plan was:
rename `SPX-IC` → `IC`, create `Directional` and `Lab`, move every bot per its `pillar` cell,
then check group counts against the CSV.

> 📝 **STALE 2026-08-07** — `[FIRST-HAND 2026-08-07, Chrome session, Bot Group dropdown
> DOM read while building `GF-QQQ-IC-Ride`]`: the v1 state above no longer describes the
> account. Actual groups are **`Archive · Directional-Focus · IC-Focus · Lab · Monitor ·
> OA-Mirror-Focus`** plus a newly-created **`IC`** group (`greenfield-family-spec.md` §5.2,
> executed literally — `IC-Focus` holds only the champion and is a workflow group, not the
> Pillar container this §3 convention describes). The account now has both `IC` and
> `IC-Focus`. **Not amended** — flagged per Andy's 2026-08-07 ruling; both groups stay.

> ⚠️ **The v2 roster changes all of these counts.** `build-plan.md` §2 archives ~20 bots, deletes
> 2, clones 4 and builds 5–7. **Do the group reorganisation as part of the Phase 4 sweep, not
> before it** — otherwise you sort bots you are about to archive. The reconciliation check
> (group counts == `bots_meta.csv` pillar counts) is what closes it, and it can only be run once
> the roster is final.

**Two operational uses beyond tidiness:**
1. **Export scope.** The export respects the group filter (§1.7) — which makes "all groups
   selected" a thing you can only verify if the groups are correct.
2. **Experiment cohorts.** Tournament arms live in one group so they can be queried as a set,
   and so the nightly script can **assert arm-level parameter distinctness.** If two arms' inputs
   are identical, the tournament is degenerate — **that is exactly the S1 ≈ HedgeD finding, made
   detectable in advance** instead of four months late.

> ⚠️ Shared Library automations across a cohort are **fleet-wide blast radius disguised as a
> single edit** — edit one and all arms change. Fork via **Copy** (§5, trap 1), and let the group
> be the thing that makes the arms *queryable*, not the thing that makes them *shared*.

> **📝 NARROWED 2026-08-05 — the warning is right; its scope was too wide.** It applies to
> automations that are **in the Automation Library**, and only those: **OA-0682** — *"Any changes
> made to an automation will flow through anywhere the automation is used, including other bots."*
> It does **not** apply to cohort arms built by cloning — **cloning copies** (direct test
> 2026-08-03; **OA-0683**, **OA-0845**; §5 Trap 1 as corrected 2026-08-05). The cross-reference
> above to "§5, trap 1" now points at the corrected trap. **Tournament arms built by cloning are
> already independent; arms built from a Library automation are not.** The arm-level
> parameter-distinctness assertion is what proves which you have — keep it either way.
>
> ⚠️ **This does NOT decide the tournament design.** `state.md` records an open conflict between
> this section (fork so arms are NOT shared) and `build-plan.md` §2D + `hedge-research.md` §5.2
> (shared automation **required**). That is a build decision, gated behind "amend the plan", and it
> remains open.

> ### 📝 APPENDED 2026-08-06 — Decision 4 RULED 2026-08-04: Architecture E. The conflict above is resolved for the greenfield family. Applied on Andy's explicit "amend the plan" (`decision-card-2026-08-06.md` ruling 1; text per `decision-memo-2026-08-04.md` Decision 4 draft (a)).
> The ⚠️ warning at the top of this subsection is right and is about UNINTENDED sharing — editing
> a Library automation changes every bot that uses it by surprise. **It does not forbid DESIGNED
> sharing.** A tournament's arms are matched precisely because their shared half is one object.
> **Architecture E:** share the entry automation deliberately (`GF-ScannerA-PutSpread` /
> `GF-ScannerB-CallSpread`, attached via the Library, not forked); let the differing half be the
> per-arm exit-bundle Bot Input (D-1 Option A); let the group be the thing that makes the arms
> *queryable*, not the thing that makes them *shared*. This satisfies `build-plan.md` §2D's
> "shared automation, shared inputs" and `hedge-research.md` §5.2 rule 1 literally — **the open
> conflict above is resolved for the greenfield family; this section's fork-via-Copy instruction
> stands unchanged for every other cohort**, where designed sharing has not been ruled.

---

## 4. Edit verification — the procedure that is not optional

Every OA edit carries **two required layers of proof.** Neither substitutes for the other, and an
edit is not reported done until both are satisfied (or, for Layer 2, queued and tracked until the
next trading day produces a position).

### 4.0 Layer 1 — the immediate self-check (every edit, every time)

Before moving to the next action, independently re-observe the changed value **from OA itself** —
never trust the save confirmation, a toast, or the tool call that made the edit (`CLAUDE.md` §9.1a).

1. **Toggle / UI state** (`AUTOMATIONS`, `EXIT OPTIONS`, template version, and anything else that
   does not survive text capture per §1.6) — take a fresh **screenshot** *after* the save. File as
   `data/captures/edit-verify/<date>/<bot>_<field>.png`.
2. **Text-capturable fields** (decision-node values, bot inputs, template Notes/Tags) — take a
   fresh bookmarklet capture or `Export Data` *after* the save and diff it against the intended
   value. Same reading rules as the capture ritual: read `input.value` / `input.checked` /
   `data-value` on `<item>` nodes, **never `innerText` alone** — it has produced wrong findings
   three separate times, most recently on CSS-rendered filter chips whose `innerText` is `""`.
3. Log the self-check result (match / mismatch) against the edit in the session log. A mismatch is
   surfaced as its own finding, not silently retried.

⚠️ **Known traps from the Chrome-direct trial** (full record: `docs/state.md`): `read_page`'s
reported viewport and screenshot pixel coordinates disagree by ~1.675× — **use element refs for
every click, never raw coordinates.** A `selected` CSS class on a multi-select option does not
imply a committed value — closing the menu is what commits it; check the underlying field, not the
checkmarks.

⚠️ **APPENDED 2026-08-04 — three more, all first-hand from the pilot part-4 session
(`session-log.md` 2026-08-04 part 4, method failures A–C).**

1. **⛔ ELEMENT REFS ARE NOT SUFFICIENT ON THIS APP.** The rule above is right about coordinates
   and **incomplete about refs.** `computer.left_click` with an element ref returns
   `Clicked on element ref_N` and **nothing happens** — reproduced on automation rows
   (`a.autolink[data-click=editAuto]`), on tree node cards (`card[data-nid=…]`), and on the bot
   `…` menu's `Archive` item. No error is raised, and the tool reports success.
   **A tool's success message is not evidence the app received the click** (`CLAUDE.md` §9.1a
   applies to clicks, not only to writes).
   **What works:** dispatch the full sequence on the element —
   `pointerdown → mousedown → pointerup → mouseup → click`, each a `MouseEvent` with
   `bubbles:true, cancelable:true, view:window` and `clientX`/`clientY` set to the element's
   `getBoundingClientRect()` centre. Every write of 2026-08-04 committed through that path.
   **Known exception:** `archiveBot` fired from *none* of the three methods. If an action resists
   all three, **stop — do not fall back to coordinates.** On that menu `Delete` sits ~29px below
   `Archive`; a mis-landed coordinate click is unrecoverable. Hand it to Andy.
   *(This is the same wall the 2026-08-03 part-2 session hit and recorded as tool degradation. It
   is a standing property of the app, not a bad session.)*

2. **⛔ THE NOTES EDITOR'S SANITIZER DECODES ENTITIES, THEN STRIPS UNKNOWN TAGS.** Pasting the
   PR-03 entry into template Notes silently lost `<capture>` and `<hash>`: `&lt;capture&gt;` was
   decoded to `<capture>` and then removed as markup. The rendered panel looked correct — the
   `CONFIG HASH` line simply read `CONFIG HASH       @ `.
   **Counter:** double-escape (`&amp;lt;`) so one decode pass leaves `&lt;` intact, **and verify
   every paste by a byte-exact length-and-content compare against the source**, not by reading the
   panel. The loss was caught only by a 1574-character compare. This extends
   `evidence-standards.md`'s byte-exact quote rule from the READ path to the WRITE path.

3. **`computer.type` lands intermittently; `form_input` does not.** Real typing committed one
   rename, then silently failed twice with `document.activeElement` correctly set to the target
   input — the characters never arrived. `form_input` (native setter + input event) worked every
   time. **Prefer `form_input`, and re-read `.value` after every text entry.**
   **Tag widgets are the exception:** they need per-character `input` events to open their
   suggestion menu, and a bulk `form_input` + Enter does **not** commit. Drive them by clicking
   the suggestion item.

### 4.1 Layer 2 — the behavioral check (unchanged from the original procedure)

**Every OA edit is also verified by reading the first NEW position's Trades list.** A fix
unverified after one trading day is repeated at the top of every brief until closed.

**The two acceptable proofs, in order of preference:**

1. **Button test-fire**, then read the resulting **Trades list**; or
2. Open the **first new position** and confirm the Trades list contains the PT row and the
   exit-trigger row.

### 4.2 ⛔ The Exit Options panel is NEVER evidence

Exit Options are **copied onto the position at open**. The panel renders the *automation's
current settings*, which can diverge from every live position silently and indefinitely — and in
v1 they did: Fortress positions generated **no exit orders at all**, not sent-and-unfilled,
**never sent**, while the panel still displayed `PROFIT % 50%`.

**The Trades list is the only order-level ground truth.** This has no exception.

### 4.3 Inverted verification — the two control clones

For `IC-SPX-FastPT25-S2` and `-130PM`, the check runs backwards: confirm the Trades list shows
**NO** PT row and **NO** exit-trigger row, and that the S2 monitor **is** firing. Their spec is
Exit-Option-free by design (`build-plan.md` §4). **Do not "fix" them.**

### 4.4 The timestamp gap test — sibling closes

For a mechanism that closes both spreads of a condor: a **designed** close-both shows `:00`/`:00`.
An **emergent**, Cleanup-driven one shows `:00`/`:01–:02`. **The timestamp gap is the test** —
it is how you tell a real mechanism from a side effect.

### 4.5 Verify values, not presence

Assert each bot's **live input values** against the **pre-registered values**, not merely that
inputs exist. ⚠️ OA's input chain is three-tier (decision ← automation ← bot) and **a broken link
does not error — it silently falls back to a stale Default and keeps trading**
(`oa-platform-reference.md` §5.2). Presence proves nothing; the value is the check.

---

## 5. The traps — every one of these has bitten this fleet

| # | Trap | What it does | The counter |
|---|---|---|---|
| **1** | ~~**Clones share automations by reference**~~ — **FALSE. Corrected 2026-08-05.** Cloning **copies**; sharing is **opt-in via the Automation Library** | The old counter was a **no-op ritual**. The real risk is narrower and still real: editing an automation you have added to the Library changes it in **every** bot that uses it | **Before editing any automation, check whether it is in the Library** — it is at **`/bots/automations`** (⭐ path established first-hand 2026-08-08 from the `/bots` Library button's own `data-ui` menu JSON: `[{"text":"Templates","href":"/bots/templates"},{"text":"Automations","href":"/bots/automations"}]`; `/automations` 404s and is NOT the Library — finding FS-3, applied at the 2026-08-08 sitting, slot 8).** In-Library → **Copy to fork**. Not in the Library (the default for a clone) → edit it directly; no fork is needed. Verify by the §4 two-layer check, never by assumption |
| **2** | **Symbols drop silently on clone** | The bot looks fully configured and **simply never scans** | **Re-add Symbols.** Verify, don't assume |
| **3** | **Collapsed nodes may not be in the DOM** | A branch missing from the capture with no error | **Expand every caret** before clicking OA Grab |
| **4** | **The export respects the group filter** | A subset export rebuilds the ledger and erases history | **All groups selected**, every time |
| **5** | **IC = 2 positions** | Limits set to 1 mean one side never opens | Daily/Total limits **× 2 per IC** |
| **6** | **Market orders fill outside the spread** | The 6/11 fill came in **$5.05/contract beyond the worst mark the position ever traded at** — R −1.63 on a defined-risk spread | ~~Market pricing is banned on every exit except a hard end-of-day flat close~~ **Market pricing is banned on every entry AND every exit except a hard end-of-day flat close** (extended to entries 2026-08-06 — see the footnote below §5) |
| **7** | **A time gate that was never implemented** | The v1 11:00 gate did not exist; 20+ sessions of entry drift | Confirm the gate is **a real decision node**, then check the first five entry timestamps |
| **8** | **Name collision on archive** | `Opening Range Breakout 60m` is archived; **`60min-ORB-10W-Paper-v1` stays live** | **Read the full name** before archiving |
| **9** | **Zero-trade ≠ worthless** | `DIR-SPX-PutVIX22-SL75` has 0 positions because its VIX≥22 gate **correctly never fired** | Delete only bots that are **both** zero-trade **and** absent from the disposition table |
| **10** | **`disableExits` resets 1 → 0 on clone** — a config-present/toggle-off exit arms itself silently on every clone | An Exit-Option “off” toggle that was OFF pre-clone reads ON post-clone; any exit config the automation already carries (e.g. a dead profit target) is live again even though nothing was edited | **Check `disableExits` immediately after cloning and restore before any other edit** |

> ### ⛔ TRAP 1 CORRECTED 2026-08-05 — the original wording is preserved here, struck above.
> **Original:** *"Clones share automations by reference | Edit the clone, you edited the original
> — or the original's later edit silently changes your clone | Fork every automation via Copy
> immediately after cloning, then confirm the clone's list points at the copies."*
>
> **Falsified first-hand, 2026-08-03 (part 1).** The CLONE's `ScannerA` was renamed, saved and
> hard-reloaded; the ORIGINAL read back **unchanged** in both name and allocation. A shared object
> would have propagated. **Corroborated structurally:** the Automation Library is opt-in ("Add to
> My Library"), reports per-automation usage, and contained exactly **one** shared automation
> fleet-wide (`Defang-Mon-S2-StrikeTouch` → 2 bots).
>
> **Corroborated in the docs** — `tools/bots/automations`, `tools/clone-bot-templates`:
> **OA-0681** *"Automations can also be shared across multiple bots."* ·
> **OA-0682** *"Any changes made to an automation will flow through anywhere the automation is
> used, including other bots."* ·
> **OA-0683** *"You can copy an automation and make changes to the new version without impacting
> the original."* ·
> **OA-0845** a clone arrives *"complete with all the settings and strategies of the original
> bot."*
> **No fact in the 1,548-fact corpus states that a clone shares by reference.**
> `oa-reconciliation-report.md` R-02 · `data/oa_facts.csv` sha256 `435abe0d…3527b`.
> Downstream corrections applied the same day: `pilot-clone-card-qqq-fortress.md` STEP 2 (voided),
> `reactivation-runbook.md` §2 step 2 (rewritten), §3 below (narrowed).

> ### 📝 TRAP 6 EXTENDED 2026-08-06 — the ban now covers entries. Ruled by Andy, decision memo 2026-08-04 (Decision 5); applied on Andy's explicit "amend the plan" (`decision-card-2026-08-06.md` ruling 1).
> **Original counter, struck above and preserved here:** *"Market pricing is banned on every exit
> except a hard end-of-day flat close."* The mechanism cited in the trap's middle column is
> **order-type-specific, not side-specific** — a market order takes no limit on either side, so an
> entry carries the same unbounded-slippage exposure the trap documents for exits. Full rationale
> and the accepted-cost caveat (n=1 position, below `CLAUDE.md` §4's T2 gate — a mechanism
> decision, not a sample decision): `oa-platform-reference.md` §7's dated append.

> ### ⛔ TRAP 10 ADDED 2026-08-07 — finding F-C2, ruled AUTHORIZED same day (Andy, first-hand).
> **[FIRST-HAND 2026-08-07, read on a fresh clone before any edit; corroborated by the top-bar
> toggle rendering ON.]** The other traps above leave a clone inert; this one makes a clone
> **do something**: a config-present/toggle-off exit — e.g. a dead profit target still sitting in
> `exits.profits` — re-arms itself silently the instant `disableExits` resets 1→0, with no field
> edited. Caught on the `IC-SPX-FastPT25-S2` → PR-01 clone, composed with finding F-C1
> (`exits.profits = 0.25` present behind the same toggle) — restored to 1 and verified before it
> could arm anything. **Invisible to text capture by construction (§1.6)** — check the toggle state
> directly on every clone, never infer it from a capture diff.

---

## 6. Standing operational rules

- **Claude executes every OA edit directly, self-verified per §4 (both layers).** *Amended
  2026-08-04, at Andy's explicit instruction — supersedes "Andy makes every OA edit."* Andy retains
  revoke authority, globally or per-bot, at any time.
- **Refactor first (behaviour-neutral), then change values.** Pilot on a dead bot; the champion
  goes last.
- **No changes during streaks.** Sizing is set once at restart, never adjusted ad hoc.
- **Log every inactive-era edit.** Edits made while the account is inactive **do persist**
  (verified 7/29→7/30), so the pre-lapse capture is not the current state.
- **Never reset OA history by cloning to escape a bad record.** Cloning to build a **new
  strategy identity to a written spec**, with the original renamed `-ARCHIVED-<date>` and
  archived and the reason logged, is the sanctioned path. The distinction is whether a spec
  change is being **documented or hidden**.
- **Append to `data/archive/rename_map.csv` as the sweep runs** — `original_name` · `archived_as`
  · `clone_name` · `date` · `disposition`. Live, not reconstructed afterwards from memory.
  Without it, no name in the frozen ledger can be traced to a bot running today.

---

## 7. Open UI checks that belong to ops

Carried from `oa-platform-reference.md` §9 — the ones that change how you *operate*, not what you
build:

| Check | Why ops cares |
|---|---|
| **Is re-applying `Update Position Exit Options` side-effect-free?** | Gates any re-assertion watchdog — the architecturally correct fix for panel-vs-position drift |
| **What is the automation-log retention window?** | Every liveness check depends on it, and looking back more than a day is currently unproven |
| ~~**Does saving a template from a live bot disturb the bot?**~~ **ANSWERED 2026-08-04 — NO.** | ~~§2.3 — gates the whole versioning convention~~ **Closed. See §2.3's append. Successor check, NOT yet run: does a template store a REFERENCE to the bot's live automation objects?** |
| ~~**Do the Fortress bots show ≥10 errors in June?**~~ **ANSWERED 2026-08-04 — NO. ZERO June errors on either bot.** | ~~Confirms or kills the Excessive Errors Failsafe hypothesis for the 6/12 regression~~ **⛔ KILLED as the 6/12 cause. Correction applied 2026-08-05.** **[FIRST-HAND 2026-08-04, bot-log read on both Fortress bots, dates taken from each row's `title` attribute, not the group headers]**: newest error on either bot is **`Apr 16, 2026 3:55PM`**; error days are **Apr 16 (91)** and **Mar 16 (138+)** on `QQQ-IC-0DTE-Fortress`, **Apr 16 (91)** on `-NoPT50`. ⚠️ **This kills the hypothesis as the 2026-06-12 cause; it does NOT retire the mechanism** — the failsafe is real and this fleet has tripped it, in March and April, on **entry scanners**. **The June cause is UNKNOWN.** Ruled **D-4**, 2026-08-04. ⚠️ **Log-retention caveat carried:** the date *filter* reaches only ~3 weeks of weekdays while stored *data* reaches `Mar 16, 2026`, and `Load more` stalled at ~229 rows — the zero-in-June result rests on the stored rows that were reachable. |

---

*Sources: `oa-capture-bookmarklet-2026-07-28.md` (methods, the Ctrl+S finding, the ritual) ·
`oa-capture-coverage-2026-07-29.md` (page-by-page coverage, the 18-field schema, what is lost) ·
`oa-cleanup-runbook.md` (the Group = Pillar convention) · `oa-setup-exploration-2026-07-29.md`
§2.1/§2.9/H1 (template versioning, groups, BUILD_ID) · `capture-architecture-2026-07-30.md` (the
export as ledger source) · `oa-platform-reference.md` (primitives, traps, the open checks).*
