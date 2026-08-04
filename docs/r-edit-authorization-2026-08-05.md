# R-edit authorization package — 2026-08-05

*Prepared for Andy's per-item ruling. **Nothing in this package has been applied.** No file in the
repo has been modified by the session that wrote this document. `git` was not run.*

---

## 0. What this is and how to rule on it

`docs/oa-reconciliation-report.md` (Phase 6, 2026-08-04) checked every platform claim in the six
OA judgment docs against `data/oa_facts.csv` and produced R-01…R-20. Nine were CONTRADICTED.
This package converts **R-01…R-07** — plus the **three standing items** `docs/state.md` lists
under *"Still needing authorization"* — into **13 concrete, byte-verified edits**, each with its
exact current text, its exact replacement, its evidence, and its `§0.2` class.

*(Two of the three standing items are the same edits as R-02's targets — `oa-ops-runbook.md` §5
Trap 1 is R-02a, and the pilot card's Step 2 fork step is R-02b. They are presented as merged rows
carrying both IDs rather than duplicated, which is why 7 R-items plus 3 standing items make 13
rows and not 10.)*

**It also carries a second, separate question:** the standing-policy amendment Andy approved in
conversation on 2026-08-04 ("Yes"), splitting the edit-authorization regime. Exact amendment text
for `CLAUDE.md` §5 and `oa-platform-reference.md` §0.2 is in **§4**.

### How to rule

Reply with a line per item. `YES` / `NO` / `YES BUT <change>` is enough. Items are independent —
authorizing R-03 does not authorize R-04.

```
R-01a  R-01b  R-01c  R-02a/S1  R-02b/S2  R-02c  R-02d
R-03   R-04   R-05   R-06      R-07      S3
ALT    (adopt v3-DRAFT wholesale — recommended NO, see §3)
POLICY (the §4 amendment — CLAUDE.md §5 + platform-reference §0.2)
```

**S3 (`build-plan.md` §2B) will not be touched without the literal words "amend the plan."**
A `YES` on S3 alone is not sufficient and will be treated as a hold.

### Provenance of every "current text" block below

Each was read by **direct `device_bash`** from the file on the MacBook and asserted to occur
**exactly once** in that file. No stage-back, no cached read, no write-tool response was trusted
(`oa-platform-reference.md` §0.2, ⚠️ paragraph; `CLAUDE.md` §9.1a).

| File | sha256 (at package close) | Anchors verified |
|---|---|---|
| `docs/oa-platform-reference.md` | `57a9576c52d7440149d7f015fe647768150ca9b393833db05d8422bcc0a1986e` | 6 · all n=1 |
| `docs/oa-ops-runbook.md` | `573999402528f1e900c51e92ea87970700ef9662dc884781975b1f68c94664d4` ⚠️ | 3 · all n=1 (re-asserted) |
| `docs/pilot-clone-card-qqq-fortress.md` | `52e1bc652ef6b8c9095ac2303cccf8c737df4c133675a2de491c345b07809391` | 2 · all n=1 |
| `docs/reactivation-runbook.md` | `160b49f62f8c0fab17aad565e662152b0243162b954c7497323da0c69d82f9c8` | 1 · n=1 |
| `docs/build-plan.md` | `588d2740cdaffdc5b1e0a41a39f769232689678851fb0bb48574a369b6f77eaa` | 1 · n=1 |
| `docs/state.md` | `13d1910b08aa9b5d7d40e640ede65d9d01dfe1f28eafabd7a8d800304c686e0d` ⚠️ | — |
| `CLAUDE.md` | `8cb0a1a42bd9c5eae1ed757ecff4c2678f9e5cdd4def592e3c18864a64f9650c` | — |
| `data/oa_facts.csv` | `435abe0d2ec0b5a11f689853e48a62db23559a36a5e621edeecdf17ff813527b` | 15 fact IDs re-read |

> ### ⚠️ BASELINE DRIFT DETECTED MID-PACKAGE — read this before ruling
> **Two files changed on disk while this package was being written, and not by this session.**
> `oa-ops-runbook.md` (20,630 → 27,553 bytes, mtime `2026-08-04 18:14 UTC`) and `state.md`
> (32,372 → 47,916 bytes, mtime `2026-08-04 19:04 UTC`) both grew after this session's first read
> at ~17:00 UTC. The added content is the **2026-08-04 part-4 work** — the `pr nn` tag-convention
> ruling (§2.1), the "do not build the `BUILD_ID` mirror" ruling (§2.2), the template-does-not-
> disturb-the-bot answer (§2.3), and three capture-method failures (§1.x). **None of it is mine;
> this session has written nothing to the repo except this file.**
>
> **All three `oa-ops-runbook.md` anchors were re-asserted against the new bytes and all three
> still return exactly one match.** The `state.md` *"Still needing authorization"* block is
> unchanged in content — it moved from line 289 to line 434. **The package is valid.** Line
> numbers quoted anywhere below are indicative only; every edit is applied by exact-text match,
> never by line number.
>
> **Why this is in the package rather than a footnote:** a stale baseline is precisely how a
> single-match assert silently becomes a wrong-place edit. The re-assert immediately before
> applying (§5 step 1) is not ceremony — it caught real drift today.

**13 / 13 anchors returned exactly one match** (14 assertions were run — the
`reactivation-runbook.md` anchor was re-asserted at full 4-line length after an initial
single-line check). If any file changes before the ruling is applied, every anchor is re-asserted
before any write and the run aborts on n≠1.

### The `§0.2` classification rule used here

`oa-platform-reference.md` §0.2 (`📝 THE ⛔ CONTESTED CONVENTION`) draws the line at **marking vs
replacing**:

> *"When an observation falsifies a claim in this file, the claim is **marked in place, dated, and
> left standing** — not deleted… **Rewriting a contested section requires Andy's authorization.
> Marking it does not.** Appends backed by a value that was read or a sentence that can be quoted
> need no authorization. **§8 stays gated.**"*

So: **a dated banner citing a quotable sentence = FREE APPEND. Changing or deleting the original
sentence = GATED REWRITE.** Under today's policy every row below is presented for authorization
regardless of class, because the free-append reading is exactly what §4's amendment would settle.
The class column tells you which rows would become automatic if you approve POLICY.

**Scope guard:** `oa-platform-reference.md` **§8 is not touched by any row in this package.**
No row appends an inference from absence.

---

## 1. The 14 edits

Rows are ordered by operational risk, not by R-number. **Recommendation** is mine; the ruling is
yours.

---

### R-02a / S1 — `oa-ops-runbook.md` §5, Trap 1 row · **GATED REWRITE** · ⭐ highest priority

**Why first:** this is the only row that currently instructs a **false ritual in an operational
doc that governs the remaining three clones**. Every clone session reads §5 before touching the
account.

**Current text** (n=1):

```text
| **1** | **Clones share automations by reference** | Edit the clone, you edited the original — or the original's later edit silently changes your clone | **Fork every automation via Copy** immediately after cloning, then confirm the clone's list points at the copies |
```

**Replacement** — the table row, plus a dated note inserted immediately **after** the trap table
(the original wording is preserved verbatim inside the note, so nothing is lost):

```text
| **1** | ~~**Clones share automations by reference**~~ — **FALSE. Corrected 2026-08-05.** Cloning **copies**; sharing is **opt-in via the Automation Library** | The old counter was a **no-op ritual**. The real risk is narrower and still real: editing an automation you have added to the Library changes it in **every** bot that uses it | **Before editing any automation, check whether it is in the Library.** In-Library → **Copy to fork**. Not in the Library (the default for a clone) → edit it directly; no fork is needed. Verify by the §4 two-layer check, never by assumption |
```

…and, appended below the table:

```text
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
```

**Evidence:** first-hand direct test 2026-08-03 (a value that was read) + OA-0681, OA-0682,
OA-0683, OA-0845.
**Class:** **GATED REWRITE** — the row's text is replaced, not merely banner-marked. A table cell
cannot carry an in-place banner legibly, which is why this is a rewrite and not an append.
**Recommendation: AUTHORIZE.** Leaving a false counter-measure standing in the doc that gates the
next three clone sessions is the live risk here, and the correction narrows the rule rather than
removing it — Library-shared automations really do propagate (OA-0682).

---

### R-02c — `reactivation-runbook.md` §2 step 2 · **GATED REWRITE** · ⭐ high priority

**Why high:** this is a **Day-0 script that has not yet been executed**. Unlike the pilot card,
there is no record to preserve — only a wrong instruction waiting to be followed.

**Current text** (n=1):

```text
2. **Fork ALL automations via Copy.** ⚠️ **THE TRAP: clones share automations by reference.** Edit one and
   you have edited the original too — or worse, the original's later edit silently changes your clone.
   Copy every automation so the clone owns its own, then confirm the clone's automation list points at the
   copies.
```

**Replacement:**

```text
2. **Check the Automation Library before editing anything.** ⚠️ **Corrected 2026-08-05 — the old
   step here said "clones share automations by reference." That is FALSE** (direct test 2026-08-03;
   OA-0681/0682/0683/0845; `oa-ops-runbook.md` §5 Trap 1). **Cloning copies.** Sharing is opt-in via
   the Library only. For each automation on the clone: if it is **in the Library**, use **Copy** to
   fork it before editing — a Library edit propagates to every bot using it (OA-0682). If it is
   **not** in the Library — the default for a clone — **edit it directly; no fork is needed.**
   Then confirm the ORIGINAL's automation list is unchanged. That confirmation is now a
   sanity check, not a trap counter, and it costs one page load.
```

**Evidence:** first-hand direct test 2026-08-03 + OA-0681, OA-0682, OA-0683, OA-0845.
**Class:** **GATED REWRITE.**
**Recommendation: AUTHORIZE.** Also note the line immediately above step 1 — *"Two of these steps
exist because of traps that will silently produce a broken bot"* — becomes "one of these steps"
once this lands. I will make that one-word change with this row unless you say otherwise.

---

### R-02b / S2 — `pilot-clone-card-qqq-fortress.md` STEP 2 · **FREE APPEND** (banner)

**Why an append and not a rewrite:** this card is the **record of what was actually executed on
2026-08-03**. Step 2 *was* performed. Deleting it would falsify the record of the pilot, which is
precisely the failure mode the `⛔ CONTESTED` convention exists to prevent.

**Current text** (n=1):

```text
> ### ⛔ THE TRAP
> **Clones share automations BY REFERENCE.** Right now, the clone and the original point at the
> *same* automation objects. Edit the clone's automation and **you have edited the original
> too** — and worse, any later edit to the original silently changes your clone.
>
> **This is the trap most likely to produce a bot that looks right and is not.** It leaves no
> error and no visible sign.
```

**Replacement** — the block above is left **byte-identical**; the following is inserted
immediately after the `## STEP 2 — ⚠️ TRAP 1: fork EVERY automation via Copy` heading, i.e.
*above* the preserved trap box:

```text
> ### ⛔ VOID 2026-08-05 — THIS STEP'S PREMISE IS FALSE. It was executed 2026-08-03 as a no-op.
> **Clones do NOT share automations by reference.** The direct test run the same day (part 1)
> renamed the clone's `ScannerA`, saved, hard-reloaded — and the ORIGINAL read back unchanged.
> Corroborated by the docs: **OA-0681/0682/0683** (sharing is a *Library* feature; Copy forks) and
> **OA-0845** (a clone arrives complete with the original's settings). No fact in the 1,548-fact
> corpus supports the premise. `oa-reconciliation-report.md` R-02.
>
> **The step and its confirm-checks are LEFT STANDING because this card is the record of what was
> actually executed on 2026-08-03.** Do not run this step on the remaining three clones.
>
> **What replaces it:** before editing an automation, check whether it is in the **Automation
> Library**. In-Library → **Copy to fork** (OA-0682: Library edits propagate). Not in the Library —
> the default — → edit directly. The Step 0-vs-Step 2 "original unchanged" check is still worth one
> page load per clone; it is now a **confirmation**, not a trap counter.
> Superseding rule: `oa-ops-runbook.md` §5 Trap 1, as corrected 2026-08-05.
```

**Evidence:** first-hand direct test 2026-08-03 + OA-0681, OA-0682, OA-0683, OA-0845.
**Class:** **FREE APPEND** under §0.2 as written (dated banner, quotable sentences, original left
standing).
**Recommendation: AUTHORIZE.**
**Note, not a separate row:** the failure table at the card's `IF SOMETHING GOES WRONG` section
carries *"Original's automation list changed at Step 2 → The fork did not take; you are editing
shared objects."* That row stays **valid as written** — if the original's list ever *does* change,
something genuinely is shared and stopping is still correct. No edit proposed.

---

### R-01a — `oa-ops-runbook.md` §1.6 · **FREE APPEND**

**Current text** (n=1):

```text
⚠️ **A toggle screenshot is necessary and not sufficient.** The per-bot `EXIT OPTIONS` toggle is
a **single-source claim** — one OA support rep, absent from OA's documentation entirely
(`oa-platform-reference.md` §10). If it is not on the dashboard at Day-0, the lapse mechanism is
**unexplained, not solved.** Keep §4's order-level verification as the actual proof.
```

**Replacement** — paragraph preserved byte-identical, banner appended beneath it:

```text
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
> bots). This paragraph has been lagging its own cited source for five days.
>
> ✅ **What does NOT change — the operative half of this warning stands.** The *causal* lapse claim
> — that resubscription restores only `AUTOMATIONS` — is still **UNSOURCED** (R-10: zero corpus
> facts on subscription lapse, deactivation or billing state). **§4's order-level verification
> remains the only actual proof and is not weakened by this correction.**
> `oa-reconciliation-report.md` R-01 · `data/oa_facts.csv` sha256 `435abe0d…3527b`.
```

**Evidence:** OA-0871, OA-0896.
**Class:** **FREE APPEND.**
**Recommendation: AUTHORIZE.** If you would rather the false sentence not stand at all, say
`R-01a REWRITE` and I will replace "a **single-source claim** — one OA support rep, absent from
OA's documentation entirely" with "**[DOCUMENTED + FIRST-HAND ×2]** — three documented control
surfaces (OA-0871/0896) plus two independent observations" and keep the rest intact. That is a
gated rewrite; it needs the explicit word.

---

### R-01b — `oa-platform-reference.md` §10 · **FREE APPEND**

**Current text** (n=1):

```text
**It still appears nowhere in OA's documentation** — a full sweep returns nothing. That is a
docs gap, not an evidence gap: the docs demonstrably lag the product in at least three other
confirmed places (§0.2), and a first-hand observation beats a stale doc.
```

**Replacement** — paragraph preserved byte-identical, banner appended beneath it:

```text
> ### ⛔ CONTESTED 2026-08-05 — THE PARAGRAPH ABOVE IS FALSE. The toggle IS documented.
> The 2026-07-31 sweep missed `tools/managing-positions/exit-options`. Verbatim:
> > *"Exit Options always run, even if your automations inside a bot are turned off… **unless you
> > turn off Exit Options in your bot**"* — **OA-0871** [DOCUMENTED]
> > *"Additionally, you can enable and disable Exit Options from **the main Bots page, inside of
> > the bot** as shown below, or individually within each position"* — **OA-0896** [DOCUMENTED]
>
> **Existence retags to [DOCUMENTED + FIRST-HAND ×2]** — the strongest tier any claim in this file
> holds. Three documented control surfaces: the main Bots page, inside the bot, per position.
>
> ⚠️ **The section heading still stands, unchanged.** *"MECHANISM still unverified"* is untouched:
> the docs establish the toggle's existence and its surfaces and say **nothing** about subscription
> lapse, deactivation, or what resubscription restores (R-10 — zero corpus facts; the only adjacent
> row, OA-0423, is DOCS-SILENT and about broker authorization). The ⚠️ CAUSAL block below is
> unmodified, and **§8.3's Day-0 Trades-list check remains the only test that settles it.**
> `oa-reconciliation-report.md` R-01 · `data/oa_facts.csv` sha256 `435abe0d…3527b`.
```

**Evidence:** OA-0871, OA-0896.
**Class:** **FREE APPEND.**
**Recommendation: AUTHORIZE.**

---

### R-03 — `oa-platform-reference.md` §7 SmartPricing tag · **GATED REWRITE**

**Why this one matters more than its size suggests:** the tag is load-bearing for tier decisions,
it is factually wrong, and the file **already contains a first-hand block instructing that it be
promoted** (`"Promote off [PROJECT-RULE] to [FIRST-HAND]"`, 2026-08-03) — which was never carried
out. Now the docs state every cell too, so the correct tier is higher than that block asked for.

**Current text** (n=1):

```text
⚠️ **[PROJECT-RULE, not doc-verified.]** These mode names, price counts and timings come from
project files. The docs do not state them.
```

**Replacement:**

```text
✅ **[DOCUMENTED + FIRST-HAND].** Every cell above is stated verbatim on `tools/bots/smartpricing`:
**OA-0785** *"Normal will try up to 4 prices, 10 seconds each."* · **OA-0786** *"Fast will try up
to 3 prices, 5 seconds each."* · **OA-0787** *"Patient will try up to 5 prices, 20 seconds each."*
· **OA-0784** *"…turn SmartPricing off and use a single limit, or send a market order."*
Independently confirmed cell-for-cell by the first-hand read recorded immediately below — docs and
product agree, which is rare enough in this file to be worth stating.

*(⛔ Corrected 2026-08-05. This line previously read:* ⚠️ *"**[PROJECT-RULE, not doc-verified.]**
These mode names, price counts and timings come from project files. The docs do not state them."
That was wrong on both counts —* `oa-reconciliation-report.md` *R-03. The `speedy` internal value
remains **[FIRST-HAND]** only; the docs do not give internal values.)*
```

**Evidence:** OA-0784, OA-0785, OA-0786, OA-0787 + the 2026-08-03 first-hand selector read already
in the file.
**Class:** **GATED REWRITE** — the tag line itself is replaced. The original wording is preserved
verbatim inside the parenthetical, so nothing is lost.
**Recommendation: AUTHORIZE.**

---

### R-04 — `oa-platform-reference.md` §6.4 mid-price residue · **FREE APPEND**

**Why an append suffices:** the block sets its own release condition — *"until it can be quoted
directly"* — and OA-0872 quotes it directly. Appending the quote **satisfies the file's own stated
precondition**; no rewrite is needed to close it.

**Current text** (n=1):

```text
> The **mid-price** half remains unquoted; it is only implied, by the docs' Stop Loss definition
> ("closes position when mid-price reaches specified loss threshold"). **Leave that half as
> [PROJECT-RULE] until it can be quoted directly** — half a claim being documented does not
> document the other half.
```

**Replacement** — block preserved byte-identical, appended beneath:

```text
> ### ✅ RESOLVED 2026-08-05 — the mid-price half CAN now be quoted directly. Promote it.
> The condition the block above sets is met, verbatim from `tools/managing-positions/exit-options`:
> > *"Exit Options use a position's mid-price when evaluating returns."* — **OA-0872** [DOCUMENTED]
>
> **Both halves of §6.4 are now [DOCUMENTED]**: the 2-minute order lifetime (OA-0877 / OA-0883 /
> OA-0878, quoted in the ⛔ block above) and mid-price evaluation (OA-0872). The
> ⚠️ **[PROJECT-RULE, not doc-verified.]** tag at the head of this section is therefore wrong on
> **both** counts and is superseded by this block together with the ⛔ block above it.
> `oa-reconciliation-report.md` R-04.
```

**Evidence:** OA-0872.
**Class:** **FREE APPEND.**
**Recommendation: AUTHORIZE.** If you also want the §6.4 head tag itself rewritten (rather than
left standing and marked superseded), say `R-04 REWRITE` — that is gated separately.

---

### R-05 — `oa-platform-reference.md` §3 allocation-shrink flag · **FREE APPEND**

**Current text** (n=1):

```text
> ⚠️ **[UNVERIFIED] — flagged 2026-08-04 (Tier 1 audit).** The percentage-allocation-shrinking
> claim is **not on the safeguards page** and carries no source anywhere in this file. It sits in a
> section whose other claims are all [DOCUMENTED], which makes it read as documented. **Treat as
> unsourced until someone finds the page or observes it.** Sizing decisions must not rest on it.
```

**Replacement** — flag preserved byte-identical, appended beneath:

```text
> ### ✅ RESOLVED 2026-08-05 — the claim IS sourced. The audit looked on the wrong page.
> It is not on `tools/bots/safeguards`. It is on
> `technical-documentation/platform/automation-behavior`, verbatim:
> > *"If you attempt to open multiple positions using a percentage-based allocation greater than
> > 50%, the contract/share amount of a subsequent position is intentionally reduced to avoid
> > allocating more than 100% of bot capital."* — **OA-0083** [DOCUMENTED]
>
> **Retag [DOCUMENTED]. The [UNVERIFIED] flag above is lifted** — sizing may rest on this again, as
> documented platform behavior rather than folklore. The flag's own release condition ("until
> someone finds the page") is met. `oa-reconciliation-report.md` R-05.
```

**Evidence:** OA-0083.
**Class:** **FREE APPEND.**
**Recommendation: AUTHORIZE.**
**Companion, included in this row:** `docs/state.md`'s Tier-1 list carries the same lifted flag
(*"sizing must not rest on it"*). `state.md` is the live-facts doc and is updated as routine
close-out under §9.1 — I will strike that line and point it at §3 in the same pass. Say `R-05
STATE-NO` if you want state.md left alone.

---

### R-06 — `oa-platform-reference.md` §6 operating window · **FREE APPEND** *(narrowed — see note)*

**⚠️ This row deviates from what the reconciliation report proposed, and the deviation matters.**
R-06 asked for a `[CONFLICT]` retag on the start time as an open question. It is **not open for
this account**: §4.1's `✅ RESOLVED IN THE PRODUCT 2026-08-04` block already records a first-hand
DOM read of `exitstart` = `09:31` (`type=time min="09:31" max="15:30"`), and §6.1a records that
the Exit Options modal header renders that phrase **live from the same Bot Schedule**. The docs
conflict is real; the product answer is settled and read, not inferred. The replacement below says
both.

**Current text** (n=1):

```text
**Operating window: 9:31 am ET until 1 minute before the market close** [DOCUMENTED].
*(The v1 file said "roughly 9:40 AM–3:58 PM ET". The docs are more precise; adopt them. This
change matters — see §8.2.)*
```

**Replacement** — text preserved byte-identical, appended beneath:

```text
> ### 📝 [CONFLICT] 2026-08-05 — the START time is docs-internal-contradictory. The product settles it.
> Two DOCUMENTED pages disagree on the start:
> > *"Exit Options can run from 9:31 am ET until 1 minute before the market close. You can
> > customize the Exit Options schedule in your Settings."*
> > — `tools/managing-positions/exit-options` — **OA-0870**
> > *"The user-defined parameters are checked every one market minute between 9:40 AM and 3:59 PM
> > Eastern."*
> > — `technical-documentation/platform/automation-behavior` — **OA-0085**
>
> The **end** (~15:59 / 3:59 PM) agrees. The **start** is 9:31 on one page and 9:40 on the other.
> Retag the START **[CONFLICT]**; the sentence above may no longer be read as a single documented
> window. The §4.2 "three windows" append gains a fourth number.
>
> ✅ **For THIS account the product has already settled it, first-hand.** §4.1's
> `✅ RESOLVED IN THE PRODUCT 2026-08-04` block reads `exitstart` = `09:31`
> (`type=time min="09:31" max="15:30"`) and `exitend` = `1` → 15:59; §6.1a confirms the modal
> header renders `9:31am to 1 minute before market close` **live from that same Bot Schedule**.
> **09:31 is the operative value here — read, not inferred.** The conflict is a docs defect to
> carry, not an open question about this account. No project design depends on the start minute.
> `oa-reconciliation-report.md` R-06.
```

**Evidence:** OA-0870, OA-0085 + the 2026-08-04 first-hand `exitstart` read already in §4.1.
**Class:** **FREE APPEND.**
**Recommendation: AUTHORIZE as narrowed above** (not as the report worded it).

---

### R-07 — `oa-platform-reference.md` §2 clone traps · **FREE APPEND**

**Current text** (n=1):

```text
> ⚠️ **Three clone traps that ARE real and appear in NO document** (first-hand, 2026-08-03):
```

**Replacement** — line preserved byte-identical; appended after the paragraph it heads:

```text
> ### 📝 SHARPENED 2026-08-05 — it is worse than silence. The docs address cloning and get it wrong.
> **OA-0845** [DOCUMENTED], `tools/clone-bot-templates`:
> > *"With a single click, you can add a cloned bot to your portfolio, complete with all the
> > settings and strategies of the original bot."*
>
> Allocation reset to a flat `1000`, Bot Group dropped to `None` and Tags dropped to empty are
> **not** "all the settings and strategies". Per §0.2 the screenshot beats the doc and the three
> traps stand **[FIRST-HAND 2026-08-03]** — but record this as a **documented claim contradicted by
> observation**, which is stronger ammunition than "appears in NO document". Doc-side corroboration
> that clone drift is a known problem: **OA-0721** — users are told to confirm Automation and Bot
> Input values after upgrading or cloning a bot, *"not only can this result in subpar performance
> for you, but it can also misrepresent the bot template's performance on the Top Bots page."*
> `oa-reconciliation-report.md` R-07.
```

**Evidence:** OA-0845, OA-0721.
**Class:** **FREE APPEND.**
**Recommendation: AUTHORIZE.** Lowest operational stakes in the package — it strengthens a claim
that is already correct and already acted on. Skip it without cost if you want a shorter list.

---

### R-01c — `pilot-clone-card-qqq-fortress.md` STEP 9 · **FREE APPEND** · *optional*

**Current text** (n=1):

```text
> The `EXIT OPTIONS` toggle's **existence is established** — the support rep's screenshot of both
> toggles on a bot dashboard, plus your own fleet-wide observation of both toggles OFF on all 35
> bots. Two independent observations. Nothing to report here.
```

**Replacement** — preserved byte-identical, appended beneath:

```text
>
> **📝 2026-08-05 — a third source exists: the docs.** **OA-0871** and **OA-0896** document the
> toggle and its three control surfaces (`tools/managing-positions/exit-options`). The evidence set
> is **[DOCUMENTED + FIRST-HAND ×2]**, not two first-hand observations alone. R-01.
> **The ⚠️ below is unchanged** — the causal claim is still untested, still a Day-0 Trades-list
> question.
```

**Evidence:** OA-0871, OA-0896.
**Class:** **FREE APPEND.**
**Recommendation: OPTIONAL — lean NO.** The card documents a session already executed on
2026-08-03 and its Step 9 conclusion ("nothing to report") was correct then and is correct now.
Annotating an executed record with a fact that changes none of its conclusions adds noise. Include
it only if you want the card to be self-contained for a future reader.

---

### R-02d — `oa-ops-runbook.md` §3 cohort blast-radius warning · **FREE APPEND**

**Note:** this warning is **substantially correct** — Library-shared automations across a cohort
really are a fleet-wide blast radius (OA-0682). The only defect is that it cross-references the
now-false Trap 1 and implies clones are shared by default.

**Current text** (n=1):

```text
> ⚠️ Shared Library automations across a cohort are **fleet-wide blast radius disguised as a
> single edit** — edit one and all arms change. Fork via **Copy** (§5, trap 1), and let the group
> be the thing that makes the arms *queryable*, not the thing that makes them *shared*.
```

**Replacement** — preserved byte-identical, appended beneath:

```text
> **📝 NARROWED 2026-08-05 — the warning is right; its scope was too wide.** It applies to
> automations that are **in the Automation Library**, and only those: **OA-0682** — *"Any changes
> made to an automation will flow through anywhere the automation is used, including other bots."*
> It does **not** apply to cohort arms built by cloning — **cloning copies** (direct test
> 2026-08-03; OA-0683, OA-0845; §5 Trap 1 as corrected 2026-08-05). The cross-reference above to
> "§5, trap 1" now points at the corrected trap. **Tournament arms built by cloning are already
> independent; arms built from a Library automation are not.** The arm-level
> parameter-distinctness assertion is what proves which you have — keep it either way.
```

**Evidence:** OA-0682, OA-0683, OA-0845 + the 2026-08-03 direct test.
**Class:** **FREE APPEND.**
**Recommendation: AUTHORIZE.** Cheap, and it removes the last live pointer to the false trap.
**Related and NOT resolved by this row:** `state.md` records an open *"Tournament doc conflict"* —
`oa-ops-runbook.md` §3 (fork so arms are NOT shared) vs `build-plan.md` §2D + `hedge-research.md`
§5.2 (shared automation **required**). This append clarifies the mechanics but **does not decide
which design the tournament uses.** That is a build decision and is gated behind "amend the plan".
Flagged, not touched.

---

### S3 — `build-plan.md` §2B `QQQ-IC-0DTE-Fortress` justification · **PLAN AMENDMENT — needs "amend the plan"**

**The build does not change. Only the stated reason changes.** The spec cell (`Restored exits:
PT50 + 15:50 time exit + 15:52 flat-close Scheduled Event backstop`) is untouched. What is
inaccurate is the *Notes* column's justification.

**Current text** (n=1):

```text
| `QQQ-IC-0DTE-Fortress` | **Restored exits: PT50 + 15:50 time exit + 15:52 flat-close Scheduled Event backstop** | The restoration the forensic called for, now built into a clean bot instead of patched into a broken one |
```

**Replacement:**

```text
| `QQQ-IC-0DTE-Fortress` | **Restored exits: PT50 + 15:50 time exit + 15:52 flat-close Scheduled Event backstop** | ⛔ **Justification corrected 2026-08-05 — wording only; the build is unchanged.** *Original: "The restoration the forensic called for, now built into a clean bot instead of patched into a broken one."* **The clone's exits already existed:** both Open Position actions carry PT50 + a 15:50 time exit, read first-hand 2026-08-03. Only the **15:52 Scheduled Event backstop** was new work. What died in v1 was **execution, not configuration** (§0.3 of `oa-platform-reference.md` — a dead profit target displayed correctly for four months). The forensic called for the backstop and for **order-level proof that the configured exits actually fire** — not for restoring exits that were never absent from the config. Day-0 Trades-list verification is the deliverable this row depends on. |
```

**Evidence:** first-hand read of both Open Position actions, 2026-08-03 (recorded in `state.md`:
*"The clone's exits already existed. Both Open Position actions carry PT50 + a 15:50 time exit…
only the 15:52 backstop was new work"*).
**Class:** **PLAN AMENDMENT.** `build-plan.md` is 🔒 frozen. This will not be applied on a bare
`YES`.
**Recommendation: AUTHORIZE — but only with the words "amend the plan."** The inaccuracy is
consequential in one specific way: read as written, §2B implies the pilot restored missing exits,
which would make a Day-0 Trades-list check look like confirmation of work already done rather than
the first real test of whether exit *execution* was ever alive. That is the exact confusion §0.3
exists to prevent. If you prefer zero movement on a frozen file, the alternative is to record the
correction in `state.md` only and leave §2B untouched — say `S3 STATE-ONLY`.

---

## 2. Summary table

| # | File | § | Class | Recommend |
|---|---|---|---|---|
| **R-02a / S1** | `oa-ops-runbook.md` | §5 Trap 1 | GATED REWRITE | ⭐ **YES** |
| **R-02c** | `reactivation-runbook.md` | §2 step 2 | GATED REWRITE | ⭐ **YES** |
| **R-02b / S2** | `pilot-clone-card…md` | STEP 2 | FREE APPEND | ⭐ **YES** |
| **R-01a** | `oa-ops-runbook.md` | §1.6 | FREE APPEND | **YES** |
| **R-01b** | `oa-platform-reference.md` | §10 | FREE APPEND | **YES** |
| **R-03** | `oa-platform-reference.md` | §7 | GATED REWRITE | **YES** |
| **R-04** | `oa-platform-reference.md` | §6.4 | FREE APPEND | **YES** |
| **R-05** | `oa-platform-reference.md` | §3 | FREE APPEND | **YES** (+ `state.md`) |
| **R-06** | `oa-platform-reference.md` | §6 | FREE APPEND | **YES**, as narrowed |
| **R-07** | `oa-platform-reference.md` | §2 | FREE APPEND | **YES** (low stakes) |
| **R-02d** | `oa-ops-runbook.md` | §3 | FREE APPEND | **YES** |
| **R-01c** | `pilot-clone-card…md` | STEP 9 | FREE APPEND | **lean NO** — noise on an executed record |
| **S3** | `build-plan.md` | §2B | 🔒 PLAN AMENDMENT | **YES**, needs *"amend the plan"* |
| **ALT** | adopt v3-DRAFT wholesale | — | — | ❌ **NO** — see §3 |

**Not in this package, by design:** `oa-platform-reference.md` **§8** (gated, untouched);
R-08 / R-09 / R-19 (`oa-mirror-reference.md` — archive-era context, the report proposes no edits);
R-10 through R-18, R-20 (UNSOURCED findings needing no doc change, or already resolved in-file).

**Two report items are already closed in the live file and need no edit** — worth knowing because
the report does not reflect them:
- **R-11** (position limits above 10 "UNSOURCED") — §9 check #9 and the §3 first-hand box already
  record `posLimitDay` / `posLimit` as pickers capped at `10`, no free-text path. **Answered
  first-hand 2026-08-04; the real ceiling is 5 ICs/day per bot.** The report's proposed "add to the
  §9 open-checks table" is stale.
- **R-13** (`Profit Taking $` / `Stop Loss $` / `Avoid Events` "UNSOURCED") — §9 check #10 records
  all three as live controls (`dprofit`, `dstop`), with the full field roster in §6.1a. **Answered
  first-hand 2026-08-04.**

---

## 3. The alternative: adopt `oa-platform-reference-v3-DRAFT.md` wholesale

**Recommendation: NO — and not on stylistic grounds. Adopting it would silently delete a day of
first-hand work.**

The draft announces its own base: *"the v2 file **byte-for-byte** (sha256 `1330dc59…7386` at draft
time)"*. The live file today is **`57a9576c…1986e`**. The draft was generated 2026-08-04 02:57;
the live reference was last written 2026-08-04 03:55 — **58 minutes later**, by the first-hand
Settings/DOM session. The draft never saw those edits.

Measured directly on the device:

| | v3-DRAFT | live `oa-platform-reference.md` |
|---|---|---|
| sha256 | `675eb2a66ee1357d…` | `57a9576c52d74401…` |
| lines | 1,194 | 1,158 |
| §6.1a — full Exit Options panel field roster, 13 fields, first-hand | **absent (0 matches)** | present, line 656 |
| `ANSWERED 2026-08-04` §9 rows | **0** | **11** |
| §13 | *"The expiration protocol, assignment blindness…"* (Phase 6, docs-derived) | *"Account-level settings"* (first-hand DOM read, `itmpaper`/`itmlive`/`maxexits`) |

**Adopting it wholesale would destroy:**

1. **§6.1a** — the complete Exit Options panel read field-by-field off the live account, including
   the PDT checkbox state (`chposLimitDay`, unchecked) that Phase 6's own §5 item 3 called a fatal
   0DTE risk. The draft's §13 *asks* for that check; the live file *has the answer*.
2. **All 11 `ANSWERED 2026-08-04` §9 rows** — including check #11, the finding that
   `itmpaper` = `itmlive` = `auto`, i.e. **the account is on the setting that sends no closing
   order.** That is the single most consequential first-hand finding in the file.
3. **§4.1's `✅ RESOLVED IN THE PRODUCT` block** — `scanstart`/`scanend`/`exitstart`/`exitend`, the
   two-independent-windows finding, and the Repeating-trigger carve-out that governs the 15:52
   backstop.
4. **A §13 collision.** Both files have a §13 with different content. A wholesale swap does not
   merge them; it replaces one with the other.

**What the draft has that the live file lacks:** its §13 assembles Phase 6's documented
expiration / assignment / PDT / partial-fill / stale-quote facts with fact IDs. That content is
genuinely valuable, and it is **mostly** — not entirely — superseded: the live §13.1 covers the
ITM setting first-hand and §6.1a covers PDT, but the draft's assignment-blindness chain
(OA-0245/0246/0145/0146/0147/0251), partial fills (OA-0140–0142), stale quotes (OA-0105–0108),
in-flight invisibility (OA-0136–0138) and manual-override-frees-limits (OA-0130/0759) have no home
in the live file.

**If you want the draft's substance, the safe path is a cherry-pick, not a swap:** lift the draft's
§13 residue into a **new §14** of the live file, as a documented-facts appendix with fact IDs, and
leave §13 (first-hand account settings) where it is. That is a **free append** — every line of it
is a quotable sentence. Say `ALT CHERRY-PICK` and I will prepare it as a separate row for a
separate ruling; it is not included in this package's 14 edits.

**Either way, `oa-platform-reference-v3-DRAFT.md` should stop being described as "what the
reference looks like with the report applied."** It is now a stale branch, and the reconciliation
report's closing line points at it as if it were current. That line is worth a note; not proposed
as an edit here.

---

## 4. POLICY — the standing-policy amendment

*Approved in principle in conversation 2026-08-04 (Andy: "Yes"). Exact text below. Ruling on this
is separate from the 14 edits and does not depend on them.*

**The problem it solves.** Today every doc correction queues behind an authorization round-trip,
including corrections where a `oa_facts.csv` quote already settles the question and no decision is
at stake. Eight of the 14 rows above are corrections of that kind. Meanwhile the things that
genuinely need a gate — what gets built, what gets sized, what goes live — sit in the same queue
and compete with them. The amendment separates the two and moves the veto on the harmless half
from *before* the edit to *at commit review*, where you see the diff anyway.

**What it does not change:** §8 stays gated. `build-plan.md` stays frozen behind "amend the plan".
Inference from absence stays forbidden. Verification stays mandatory and unchanged.

### 4.1 `CLAUDE.md` §5 — new bullet, inserted after the *"OA automation authority"* bullet

```text
- **Doc-edit authority — AMENDED 2026-08-05, at Andy's explicit instruction.** The
  edit-authorization regime splits in two. The gate is on **decisions**, not on **corrections**.
  - **DECISIONS STAY GATED.** Anything that changes *what gets built* requires an explicit
    **"amend the plan"** from Andy: `docs/build-plan.md` in any part; `docs/oa-platform-reference.md`
    **§8** (build instructions); any spec, sizing rule, kill criterion, pre-registration text, or
    go-live gate. Unchanged.
  - **EVIDENCE-BACKED CORRECTIONS OF FALSIFIED CLAIMS MAY BE APPLIED DIRECTLY**, with no pre-edit
    authorization, when **all five** hold:
    1. The claim is falsified by a **quotable sentence** — a `data/oa_facts.csv` fact ID with its
       verbatim quote — or by a **dated first-hand observation of a value that was read** (a DOM
       field, a hidden-input payload, a screenshot).
    2. The correction is carried as a **dated banner**, and **the original text is left standing**
       wherever the doc's own convention requires it (`oa-platform-reference.md` §0.2; and in any
       doc that is a record of something executed, e.g. `docs/pilot-clone-card-qqq-fortress.md`).
    3. The **evidence is cited in the edit itself** — fact ID or dated observation. **Never another
       project document**: two documents vouching for each other is a citation loop
       (`oa-platform-reference.md` §0.2 provenance rule).
    4. The edited file is verified by a **direct `device_bash` sha256 plus a single-match grep of
       the new text**. Never the write tool's response; never a stage-back or cached read (§9.1a).
    5. The edit **changes no decision.** If it would, it is a decision, and it is gated. When it is
       ambiguous, it is gated.
  - **Andy's veto moves to commit review — it is replaced, not removed.** Every directly-applied
    correction is listed in the close-out hand-off (§9.1 step 3) with its file, its anchor, its
    evidence and its verification hash, and Andy may reject any of them at commit.
  - **Inference from absence is never an evidence-backed correction.** "I did not see a control" is
    not an observation; it is a screen that was not opened (`oa-platform-reference.md` §0.2).
  - **Andy retains revoke authority** — globally or per-file, at any time.
```

### 4.2 `oa-platform-reference.md` §0.2 — appended to the `📝 THE ⛔ CONTESTED CONVENTION` block

```text
> ### 📝 AMENDED 2026-08-05 — the authorization split, at Andy's explicit instruction
> **The gate is on decisions, not on corrections.**
>
> - **Correcting a claim in this file that has been falsified needs no authorization** — provided it
>   is a **dated banner** citing a **quotable sentence** (an `oa_facts.csv` fact ID with its
>   verbatim quote) or **a value that was read first-hand on a stated date**, and the original text
>   is **left standing beneath it** per the convention above. This makes explicit what every
>   2026-08-03 `⛔ CONTESTED` block already did: the banner that says *"the claim above is false,
>   and here is the quote"* is an append, and appends backed by a quotable sentence were already
>   free.
> - **Replacing or deleting the original text still requires Andy's authorization.** Marking is
>   free; overwriting is not. The record must stay auditable.
> - **§8 stays gated**, unchanged — it is build-plan-adjacent, and `build-plan.md` changes require
>   an explicit "amend the plan".
> - **Inference from absence is never a correction.** The provenance rule above is unaffected and
>   is not relaxed by anything in this block.
> - **Verification is unchanged and not optional:** a direct `device_bash` sha256 plus a
>   single-match grep of the new text. A tool success message is not verification (`CLAUDE.md`
>   §9.1a). Every directly-applied correction is listed at commit review, where Andy may veto it.
>
> Full regime: `CLAUDE.md` §5, *"Doc-edit authority"*. Worked example of the split applied to
> thirteen concrete edits: `docs/r-edit-authorization-2026-08-05.md`.
```

### 4.3 What this package would have looked like under the amendment

**9 of the 13 rows are FREE APPEND** — R-01a, R-01b, R-01c, R-02b/S2, R-02d, R-04, R-05, R-06,
R-07 — and would have been applied directly, then listed at commit review for your veto. The
remaining **4** would still have come to you first: **R-02a/S1, R-02c, R-03** (rewrites) and
**S3** (plan amendment).

**The honest counter-argument, since it is your call:** the two edits with the most operational
teeth in this package — R-02a/S1 and R-02c, the false shared-automations ritual in two live
runbooks — are **rewrites**, so the amendment would not have accelerated them. It buys speed
mostly on the low-stakes half. Whether that is worth loosening a gate that has, so far, caught
things is a judgment I do not have standing to make for you.

---

## 5. Execution plan once authorized

Applied **only** to items ruled YES, in this order:

1. Re-assert all 13 anchors against the live files (`n==1` required). **Abort the whole run on any
   n≠1** — a changed file means a changed baseline and a fresh package.
2. Apply each authorized edit as a dated amendment, matching the existing convention:
   supersedes-notes, `⛔ CONTESTED` banners left standing wherever §0.2 requires.
3. After **each** file: direct `device_bash` **sha256** + **grep of the new text asserting a single
   match**. Never the write tool's response; never a staged read-back
   (`oa-platform-reference.md` §0.2 ⚠️, `CLAUDE.md` §9.1a).
4. `build-plan.md` §2B is written **only** on the literal words *"amend the plan."*
5. Append `docs/session-log.md`; update `docs/state.md` (clear the resolved *"Still needing
   authorization"* entries; lift the R-05 Tier-1 flag).
6. **List every changed file with its before/after sha256 for commit.** `git` is not run.

**Still outstanding regardless of this ruling** — carried, not resolved here:

- `_to_delete/index.lock.stranded-2026-08-03` — the bridge cannot delete. **Andy deletes
  `_to_delete/`** (untracked, not in `.gitignore`).
- The **tournament doc conflict**: `oa-ops-runbook.md` §3 (fork so arms are NOT shared) vs
  `build-plan.md` §2D + `hedge-research.md` §5.2 (shared automation required). A build decision —
  gated.
- **R-10**: the lapse mechanism is still UNSOURCED. Nothing in this package touches it, and the
  **Day-0 Trades-list check remains the only test.**
- **Day-0 decision, unchanged and unaffected:** `itmlive` = `auto` — the account sends **no closing
  order** on expiring ITM positions. §13.1.

---

*Prepared 2026-08-05. No file in the repo was modified to produce this package. `git` was not run.
Awaiting per-item ruling.*
