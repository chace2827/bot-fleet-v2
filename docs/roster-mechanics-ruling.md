# Draft ruling — post-cutover roster mechanics

*Prepared 2026-08-11. This is a draft for Andy to sign. It does not make rulings; it only assembles the evidence and proposes contract wording.*

---

## 1. Roster Facts

### 1.1 Roster authority

- The post-cutover roster is proven by an **OA `/bots` capture** (bookmarklet text + toggle screenshots), not by `data/bots_meta.csv`. `data/bots_meta.csv` is only the classification source for `pillar`, `role`, `underlying`, `status`, `champion`, `superseded`, and `ops_class` (`capture-architecture-2026-07-30.md`; `build-plan.md` §2).
- The current closing-state authority is `data/captures/2026-08-09-s2b/partB-hands-signatures-and-final-sweep-2026-08-09.txt` (sha256 `58704c6881479ffa3a2f046ceb15fa0f5bb4c495aeb873e634c458ef636a825d`). It records **43 active bots**, **17 with AUTOMATIONS ON**, and lists them explicitly at lines 202-213.
- The prior list-view authority is `data/captures/2026-08-08-audit/01-roster-toggles-43-2026-08-08.tsv` (sha256 `4e300dcb36a376cf607a51752bf2846ed13a0c976af04d128956fffc91f17771`). It carries all 43 `oa_id`s, list-view allocation, and toggle state.
- `data/bots_meta.csv` (sha256 `34932bab666e744340d7e4f1a662bdce595a8b215745c1bcdb0cd6b0caf7e659`) was updated 2026-08-12 and now contains the 7 greenfield-family bots with `pillar=IC`, `role` (`control`/`experiment`/`canary`), `underlying=QQQ`, and `status=ON`.

### 1.2 Live roster (17 bots, 2026-08-09 S2b final sweep)

| bot_name | oa_id | pillar | role | underlying | champion | superseded_by | ops_class | capture_file | capture_hash | status | source_note |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `IC-SPX-FastPT25-S2` | `BOTfw5TkkCRF4417860821948715488` | IC | control | SPX | yes | — | — | `data/captures/2026-08-07-s0b/IC-SPX-FastPT25-S2-post-FC1-2026-08-07.txt` | `ee39ef7f1abde0402daac70cd08aac732c4cd0eb8c78e4b6453d689ed145f656` | live | PR-01; `build-plan.md` §2A champion; `pre-registration-ledger.md` PILLAR/ROLE `IC · control`; exit-option-free inverted control (disableExits 1); Template V1 `Tfw5TkkCRF2317861409017023081`; limits 2/2 ruled at S2b; S2b Step 6 owed |
| `IC-SPX-FastPT25-S2-130PM` | `BOTfw5TkkCRF3017861977616287731` | IC | experiment | SPX | no | — | — | `data/captures/2026-08-08-clones/PR-02-clone-final-2026-08-08.txt` | `d542587ffa4b012fd63e0b2ef50d6aa8d900fec477c2718102cae7c1f9d06162` | live | PR-02; clone of champion; entry-time A/B (1:30 PM vs 11:00 AM); `pre-registration-ledger.md` PILLAR/ROLE `IC · experiment`; exit-option-free inverted control; Template V1 `Tfw5TkkCRF1717862960217463041`; limits 2/2; D4 Trades-list check owed |
| `QQQ-IC-0DTE-Fortress-NoPT50` | `BOTfw5TkkCRF3017862038322323202` | IC | experiment | QQQ | no | — | — | `data/captures/2026-08-08-clones/PR-04-clone-final-2026-08-08.txt` | `e58db65fff3f0c69141eeb80a0db01791bfdf6b4dfbe8045d08493e06667bdc0` | live | PR-04; `pre-registration-ledger.md` PILLAR/ROLE `IC · experiment`; EXIT OPTIONS armed (expdays=0.01); no PT; 15:52 flat-close backstop; Template V1 `Tfw5TkkCRF1717862960769161432`; S2b-R4 observed close-time owed |
| `GF-QQQ-IC-Ride` | `BOTfw5TkkCRF4417860701930934951` | IC | control | QQQ | no | — | — | `data/captures/2026-08-07-greenfield/GF-QQQ-IC-Ride/GF-QQQ-IC-Ride.txt` | `5b333324e93ab8331cab6e89a4d66eb392bf7058f66918cc22160632297edb19` | live | PR-14; `greenfield-family-spec.md` §2 role `control`; exit bundle `expdays=0.01` only (time-exit-only control); Template V1 `Tfw5TkkCRF4417860721733331241`; captured 2026-08-07; in `data/bots_meta.csv` as of 2026-08-12 |
| `GF-QQQ-IC-PT50` | `BOTfw5TkkCRF4417860738688735152` | IC | experiment | QQQ | no | — | — | `data/captures/2026-08-07-greenfield/GF-QQQ-IC-PT50/GF-QQQ-IC-PT50.txt` | `8ea2743a81762bbc8b0537bc797c9599d5adbd88b7b2d98d8a7d67d9d91ac6f4` | live | PR-15; `greenfield-family-spec.md` §2 role `experiment`; arm `profits=0.5`; Template V1 `Tfw5TkkCRF4417860751149180062`; in `data/bots_meta.csv` as of 2026-08-12 |
| `GF-QQQ-IC-Trail` | `BOTfw5TkkCRF4417860754672239833` | IC | experiment | QQQ | no | — | — | `data/captures/2026-08-07-greenfield/GF-QQQ-IC-Trail/GF-QQQ-IC-Trail.txt` | `b65faab35c70c3fa2fa7437b85c77e3f7f90b5d3e70207544488cf96e6c67db3` | live | PR-16; `greenfield-family-spec.md` §2 role `experiment`; arm `tstop target=40 trail=15`; Template V1 `Tfw5TkkCRF4417860759179743713`; tail retirement criterion G-12; in `data/bots_meta.csv` as of 2026-08-12 |
| `GF-QQQ-IC-Touch0` | `BOTfw5TkkCRF4417860760818962144` | IC | experiment | QQQ | no | — | — | `data/captures/2026-08-07-greenfield/GF-QQQ-IC-Touch0/GF-QQQ-IC-Touch0.txt` | `f5937391c74f201b7d9965c3ed890c5b2100dd331a4758a946053759fb675051` | live | PR-17; `greenfield-family-spec.md` §2 role `experiment`; arm `touch=0`; Template V1 `Tfw5TkkCRF4417860766269007264`; in `data/bots_meta.csv` as of 2026-08-12 |
| `GF-QQQ-IC-SL100` | `BOTfw5TkkCRF4417860767788927225` | IC | experiment | QQQ | no | — | — | `data/captures/2026-08-07-greenfield/GF-QQQ-IC-SL100/GF-QQQ-IC-SL100.txt` | `bc6dbb4647dfb1599154ab5457f64e92d01e7d84c6cd0eae1ae76659300d94c5` | live | PR-18; `greenfield-family-spec.md` §2 role `experiment (hedge arm)`; arm `stoploss=1` (100% of credit); internal name "Breakeven"; Template V1 `Tfw5TkkCRF4417860773009022425`; in `data/bots_meta.csv` as of 2026-08-12 |
| `GF-QQQ-IC-SL200` | `BOTfw5TkkCRF4417860785000861357` | IC | experiment | QQQ | no | — | — | `data/captures/2026-08-07-greenfield/GF-QQQ-IC-SL200/GF-QQQ-IC-SL200.txt` | `e01578f924ab431be02520569199e6780397b00d7e17b522522976ae71f38e36` | live | PR-19; `greenfield-family-spec.md` §2 role `experiment (hedge arm)`; arm `stoploss=2` (200% of credit); Template V1 `Tfw5TkkCRF4417860791919674137`; in `data/bots_meta.csv` as of 2026-08-12 |
| `GF-QQQ-IC-Canary` | `BOTfw5TkkCRF4417860774419022836` | IC | canary | QQQ | no | — | — | `data/captures/2026-08-07-greenfield/GF-QQQ-IC-Canary/GF-QQQ-IC-Canary.txt` | `28baa673c8a7da4ac20c5c16f2c7acc3d6d75f9ca6213d833f34c6d76fef3df7` | live | PR-20; `greenfield-family-spec.md` §2 role `instrument` (used here as `canary`); arm `profits=0.05`; Template V1 `Tfw5TkkCRF4417860782548949126`; in `data/bots_meta.csv` as of 2026-08-12 |
| `DIR-SPX-PutVIX22-SL75` | `BOTfw5TkkCRF217824306963282811` | Directional | experiment | SPX | no | — | — | `[TO RULE]` | `[TO RULE]` | live | PR-05; `pre-registration-ledger.md` PILLAR/ROLE `Directional · experiment`; VIX≥22 gate; no per-bot config capture; first-trading-day capture owed per S2b Step 6; `oa_id` from `01-roster-toggles-43-2026-08-08.tsv` |
| `DIR-SPX-CallVIXdrop` | `BOTfw5TkkCRF217824370390678863` | Directional | experiment | SPX | no | — | — | `[TO RULE]` | `[TO RULE]` | live | PR-06; `pre-registration-ledger.md` PILLAR/ROLE `Directional · experiment`; VIX-change ≤ -2 gate; no per-bot config capture; first-trading-day capture owed per S2b Step 6; `oa_id` from `01-roster-toggles-43-2026-08-08.tsv` |
| `3DTE $140-$350` | `BOTfw5TkkCRF2217765235512870291` | Mirror | mirror-watch | SPX | no | — | — | `[TO RULE]` | `[TO RULE]` | live | PR-07; `pre-registration-ledger.md` PILLAR/ROLE `OA-Mirror · mirror-watch`; `data/mirror_baseline.csv` n=46 mean_R +0.0156; no per-bot config capture; first-trading-day capture owed per S2b Step 6; `oa_id` from `01-roster-toggles-43-2026-08-08.tsv` |
| `Nigiri-Paper-v1` | `BOTfw5TkkCRF1017766118057607741` | Mirror | mirror-watch | SPY | no | — | — | `[TO RULE]` | `[TO RULE]` | live | PR-08; `pre-registration-ledger.md` PILLAR/ROLE `OA-Mirror · mirror-watch`; `data/mirror_baseline.csv` n=38; no per-bot config capture; first-trading-day capture owed per S2b Step 6; `oa_id` from `01-roster-toggles-43-2026-08-08.tsv` |
| `Friday 14 DTE Broken Wing IB (B-70)` | `BOTfw5TkkCRF1017766446781407596` | Mirror | mirror-watch | SPX | no | — | — | `[TO RULE]` | `[TO RULE]` | live | PR-10; `pre-registration-ledger.md` PILLAR/ROLE `OA-Mirror · mirror-watch`; `data/mirror_baseline.csv` n=7; no per-bot config capture; first-trading-day capture owed per S2b Step 6; `oa_id` from `01-roster-toggles-43-2026-08-08.tsv` |
| `Trendy-Paper-v1` | `BOTfw5TkkCRF1017766118431160782` | Mirror | mirror-watch | SPY | no | — | — | `[TO RULE]` | `[TO RULE]` | live | PR-11; `pre-registration-ledger.md` PILLAR/ROLE `OA-Mirror · mirror-watch`; `data/mirror_baseline.csv` n=15; no per-bot config capture; first-trading-day capture owed per S2b Step 6; `oa_id` from `01-roster-toggles-43-2026-08-08.tsv` |
| `60min-ORB-10W-Paper-v1` | `BOTfw5TkkCRF3317782759988647731` | Mirror | mirror-watch | SPX | no | — | — | `[TO RULE]` | `[TO RULE]` | live | PR-12; `pre-registration-ledger.md` PILLAR/ROLE `OA-Mirror · mirror-watch`; `data/mirror_baseline.csv` n=12; name-collision guard with archived `Opening Range Breakout 60m`; no per-bot config capture; first-trading-day capture owed per S2b Step 6; `oa_id` from `01-roster-toggles-43-2026-08-08.tsv` |

**Role taxonomy note.** The requested role column was drafted as `(champion / control / mirror / canary / lab)`. The source documents use `control` (PR-01, GF-Ride), `experiment` (PR-02, PR-04, PR-05, PR-06, GF-PT50/Trail/Touch0/SL100/SL200), `mirror-watch` (the 5 mirrors), and `instrument` (GF-Canary). These mappings are flagged as decisions in §3.

### 1.3 Roster arithmetic

- **35 total dispositions** = 20 archived + 2 deleted + 4 cloned + 9 untouched (`build-plan.md` §2; `capture-architecture-2026-07-30.md` §"Roster confirmed").
- **43 active bots** in `/bots` after the 2026-08-08 cleanup (footer: "43 active bots • 7 left in your plan"), confirmed by `01-roster-toggles-43-2026-08-08.tsv` and the S2b final sweep.
- **17 live (AUTOMATIONS ON)** as of 2026-08-09 S2b: the 7 greenfield arms + PR-01 + PR-02 + PR-04 + PR-05/06/07/08/10/11/12.
- **Not in the live 17:**
  - `QQQ-IC-0DTE-Fortress` (PR-03) — unsigned/OFF.
  - `QQQ long call` (PR-09) and `Tasty Condor` (PR-13) — OFF by A6 ride ruling.
  - `Weekly-IB-SPY-Paper-v1` (PR-13 mirror) — OFF.
  - Three renamed archive-queued bots (`IC-SPX-FastPT25-S2-ARCHIVED-2026-08-07`, `IC-SPX-FastPT25-S2-130PM-ARCHIVED-2026-08-08`, `QQQ-IC-0DTE-Fortress-NoPT50-ARCHIVED-2026-08-08`) — present in `/bots` but OFF/OFF, awaiting OA archive.

---

## 2. Mechanics Contract (proposed wording for Andy to sign)

### 2.1 Join keys and data lineage

1. **OA Export Data** (`data/raw/YYYY-MM-DD.csv`, 26 columns) is the position source. Key: exact `botName`.
2. **`build_ledger.py`** (sha256 `9ec21da902e23cdbe5f9ea442a60a9d5ff7f8028b386b559d69bb0b3889cc321`) reads the newest `data/raw/*.csv`, filters on `open_date >= LEDGER_START` (`2026-08-10`), joins `data/bots_meta.csv` on `bot`, pairs legs into condors, assigns a global `trade_id` (`T00001`…), and writes:
   - `data/trades.csv` (sha256 `f3b9fe5c67d90ff80c2b4fd227410e0688adeb1348f336394e52bde58837b69e`) — one row per leg.
   - `data/bots.csv` — one row per bot.
   - `data/straddlers.csv` — pre-cutover opens that close post-cutover.
   - `data/ops_rows.csv` — `ops_class=lab-ops` rows excluded from the working ledger.
   - `data/ledger_meta.json` — run receipt.
3. **`data/bots_meta.csv`** (sha256 `34932bab666e744340d7e4f1a662bdce595a8b215745c1bcdb0cd6b0caf7e659`) is the classification source. Key: `bot`. It carries `pillar`, `role`, `underlying`, `status`, `champion`, `superseded`, `ops_class`. It is **not** the roster authority. Updated 2026-08-12: now includes the 7 greenfield-family bots.
4. **`data/bots_config_v2.csv`** (sha256 `e54ee4ea9f3bfa7da5939920cddf5f88814297f3fb5f6be0151c7f43a462aef9`) is the config record. Key: `name`/`oa_id`. It is built from capture, never hand-written. Currently it contains only the 7 greenfield arms + shared automations (Phase A) and does not yet follow the graded-mechanic template (see §2.2 and §3).
5. **`data/trades.csv`** is the working ledger for the daily loop. Key for mechanics: `(trade_id, bot)`. The `trade_id` pairs the two spread rows of a condor.
6. **`data/hedge_tournament.csv`** (sha256 `ce475eb92745ba39dd03fcf8e3259987b0dc87d4cbd7173ee68c9aea7fe1090b`) is the counterfactual engine output. Key: `(date, trade_id, rule)`. It joins back to `data/trades.csv` on `(trade_id, bot)` and is consumed by `report.py` and `STATUS.md`.
7. **`data/mirror_baseline.csv`** is a one-time frozen pre-lapse snapshot for mirror funding decisions. Key: `bot`. It is **not** a daily-loop input and **not** a roster authority. It contains 10 mirror rows; 5 of them are in the live ON set.

### 2.2 `data/bots_config_v2.csv` — current schema

**Current header (line 138, sha `e54ee4ea…`):**

```
object_kind,name,oa_id,version,attached_to,input_id,input_type,input_label,input_default,a7_hash,captured,layer2_status
```

**Current column meaning (as used by the Phase A capture):**

| column | type | meaning |
|---|---|---|
| `object_kind` | enum (`shared_automation` / `bot`) | `shared_automation` for shared scanners/backstops; `bot` for per-bot rows. |
| `name` | string | OA bot name or shared-automation name. |
| `oa_id` | string | OA object id (`RT...` for routines/automations, `BOT...` for bots, `IN...` for inputs, `T...` for templates). |
| `version` | string | For shared rows, the OA automation version number; for bot rows, `template V1 (Tid...)`. |
| `attached_to` | string | Trigger list for bot rows (`rid ...`); `NONE` for shared rows. |
| `input_id` | string | Input object id(s) attached to the bot. |
| `input_type` | enum (`exits` / `NONE`) | The type of input object. |
| `input_label` | string | Human-readable input label(s). |
| `input_default` | string / decoded blob | For shared rows, the literal default value; for bot rows, the decoded exit bundle (e.g., `expdays=0.01; profits=0.5; ...`). |
| `a7_hash` | hex or `N/A` | For shared rows, sha256 of the `{name, inputs, root}` JSON from the client model; for bot rows, `N/A` because the matching proof is the capture-diff. |
| `captured` | path | The capture file proving the recorded state. |
| `layer2_status` | string | e.g. `DEFERRED TO DAY-0` — marks items needing first-trading-day verification. |

**Current file also contains embedded comment blocks** (lines starting with `#`) and is therefore not a plain CSV. It is incomplete: it contains the 7 greenfield arms and shared automations, but not PR-01, PR-02, PR-04, PR-05/06, or the 7 untouched mirrors.

### 2.3 Intended schema — `data/bots_config_v2.template.csv` and three-state semantics

**Template header (sha of `data/bots_config_v2.template.csv` not separately recorded):**

```
bot,pt_pct,sl_pct,time_exit,event_backstop,capture_file,capture_hash
```

**Three-state cell semantics (from the template comments):**

| state | meaning | example | rule effect |
|---|---|---|---|
| `value` | Declared and evaluates. | `0.50`, `15:50` | Forward rule is ON. |
| `none` | Removed by design. | `none` | Forward rule is OFF; inverse rule is ON (e.g., `pt_pct=none` means PT removed — a ride control). |
| `(blank)` | Missing data. | empty cell | Rule is SKIPPED and reported as a blind spot. |

**`none` is not `(blank)`.** `none` is an explicit design choice; `(blank)` is an evidence gap. The current `data/bots_config_v2.csv` does not implement these columns; the mechanic values are embedded in the `input_default` decoded blob. Migrating to the template schema is a decision (see §3).

### 2.4 Versioned fixed-panel rule

- Counterfactual policies, detector rules, and their thresholds are frozen inputs. Changing one makes the accumulated ledger uncomparable and silently destroys every day already banked. Version and re-baseline instead.
- `scripts/execution_audit.py` is declared frozen at v1.0.0, sha `67a537977c5d0896`, in `docs/daily-loop-spec.md` §0 and §7, and in `docs/rules-catalog.md`.
- The current `scripts/execution_audit.py` file sha is `fdc43d0dcb7275560069048e62d897f528d9620b5a6be87de7a410fae1851e2d`. Whether this matches the declared frozen version is flagged in §3.

### 2.5 Roster authority rule

- The live roster is proven by the **OA `/bots` capture** (bookmarklet text + toggle screenshots), taken before and after any edit.
- `data/bots_meta.csv` is only a classification source and cannot prove a bot is on/off.
- The current roster authority is `data/captures/2026-08-09-s2b/partB-hands-signatures-and-final-sweep-2026-08-09.txt` (sha `58704c68…`).
- A bot must be in the final sweep's `AUTOMATIONS ON` list to be in the live roster. Anything else is OFF, archived, or unsigned.

### 2.6 Pre-registration IDs and OA tags

- `docs/pre-registration-ledger.md` assigns `PR-NN` IDs. The OA tag is `pr nn` (non-alphanumeric normalized); the literal `PR-NN` lives in notes.
- `PR-01`…`PR-04` and `PR-14`…`PR-20` are signed. `PR-05`…`PR-13` are in various draft/signed states; the live set uses `PR-05/06/07/08/10/11/12`.
- Template V1 ids for the signed clones and GF arms are recorded in `pre-registration-ledger.md` and `data/bots_config_v2.csv`.

### 2.7 Data flow contract

- Each trading day ~17:30 ET: Andy supplies the OA Export Data CSV (all groups), a `/bots` bookmarklet capture, toggle screenshots for changed bots, and one line of context.
- `scripts/daily.sh` runs: `build_ledger.py` → `tape.py` → `daily_brief.py` → `hedge_tournament.py` → `report.py` → `STATUS.md` / `dashboard.html`.
- The export must be taken with **all bot groups selected**; a filtered export is a subset and would erase excluded bots' history (`daily-loop-spec.md` §1.1).
- `build_ledger.py` has guards: filtered-export warning, pre-cutover row refusal, `ops_class=lab-ops` leak refusal, and a fatal refusal for any bot whose `pillar`/`role`/`underlying` resolve to `UNCLASSIFIED` (2026-08-12 update: stable monotonic `trade_id` continues from the existing ledger instead of restarting at `T00001`).

### 2.8 Mirror funding baseline

- `data/mirror_baseline.csv` is a one-time frozen pre-lapse snapshot built from `oa_export_positions_2026-07-30.csv` (CLAUDE.md §3). It is read only by funding decisions, not by the daily loop or the roster authority.
- It contains the 5 live mirrors (`3DTE`, `Nigiri`, `Friday`, `Trendy`, `60min-ORB`) and 5 others that are OFF.

---

## 3. Decisions still to rule

1. **Role taxonomy mapping.** The requested roster table uses `(champion / control / mirror / canary / lab)`. The source docs use `control`, `experiment`, `mirror-watch`, `instrument`, and `live-candidate`. Specifically:
   - `IC-SPX-FastPT25-S2` is the champion (`champion=yes`; `build-plan.md` §2A) but `pre-registration-ledger.md` labels its PILLAR/ROLE `IC · control`. Should its `role` be `champion` or `control`?
   - The 6 greenfield experiment arms and the 2 directional experiment arms are labeled `experiment` in source. Should the requested role set be expanded to include `experiment`, or should they be mapped to `lab` / `control` / another label?
   - The 5 mirrors are labeled `mirror-watch` in source. Should they be `mirror` in the final table?
2. **`data/bots_config_v2.csv` schema and completeness.** Should the file be migrated to the `data/bots_config_v2.template.csv` schema (`bot, pt_pct, sl_pct, time_exit, event_backstop, capture_file, capture_hash`)? Should it be filled for all 17 live bots, not just the 7 greenfield arms?
3. **`data/bots_meta.csv` GF rows.** Resolved 2026-08-12 — the 7 greenfield-family bots are now present with `pillar=IC`, `role` matching `greenfield-family-spec.md`, `underlying=QQQ`, `status=ON`, `champion=no`.
4. **Config captures for the 10 S2b-switched bots.** `PR-05, PR-06, PR-07, PR-08, PR-10, PR-11, PR-12` (and the first-trading-day verification for `PR-02` and `PR-04`) need per-bot config/Trades-list capture. Is the 2026-08-08 list-view capture sufficient as interim evidence, or must a per-bot automation-tree capture be taken before sign-off?
5. **`scripts/execution_audit.py` frozen hash.** `daily-loop-spec.md` declares the file frozen at v1.0.0 with sha `67a537977c5d0896`; the current file sha is `fdc43d0d…`. Confirm whether the current file is the intended frozen version or whether the spec reference is stale.
6. **Three `-ARCHIVED-` renamed bots.** `IC-SPX-FastPT25-S2-ARCHIVED-2026-08-07`, `IC-SPX-FastPT25-S2-130PM-ARCHIVED-2026-08-08`, and `QQQ-IC-0DTE-Fortress-NoPT50-ARCHIVED-2026-08-08` are still in `/bots` OFF/OFF. Should they be OA-archived now, or is their current state acceptable?
7. **`superseded_by` semantics.** The table leaves `superseded_by` blank for all 17 live bots. Should the archived originals (e.g., `IC-SPX-FastPT25-S2-ARCHIVED-2026-08-07`) be recorded as superseded by their live clones?
8. **`DIR-SPX-Put-Control`.** It is a live-candidate/ON control in `data/bots_meta.csv` but was not switched on at S2b. Should it remain OFF, or be added to the live roster?

---

## 4. Missing evidence

1. Per-bot automation-tree/exit-bundle captures for the 10 S2b-switched untouched/directional/clone bots (`PR-05, PR-06, PR-07, PR-08, PR-10, PR-11, PR-12` and the first-trading-day Trades-list for `PR-02` and `PR-04`).
2. `data/bots_meta.csv` rows for the 7 greenfield-family bots — resolved 2026-08-12.
3. `data/bots_config_v2.csv` rows for `PR-01`, `PR-02`, `PR-04`, `PR-05`, `PR-06`, `PR-07`, `PR-08`, `PR-10`, `PR-11`, `PR-12`, and a decision on which schema (current or template) is canonical.
4. Verification that `scripts/execution_audit.py` current sha (`fdc43d0d…`) matches the declared frozen v1.0.0 sha (`67a53797…`) in `docs/daily-loop-spec.md`.
5. GitHub write access / `gh auth` status to open a PR (local state: logged out).

---

## 5. Files and hashes referenced in this draft

| file | sha256 |
|---|---|
| `docs/roster-mechanics-ruling.md` | *(self-reference: compute on device after final edits)* |
| `data/captures/2026-08-09-s2b/partB-hands-signatures-and-final-sweep-2026-08-09.txt` | `58704c6881479ffa3a2f046ceb15fa0f5bb4c495aeb873e634c458ef636a825d` |
| `data/captures/2026-08-08-audit/01-roster-toggles-43-2026-08-08.tsv` | `4e300dcb36a376cf607a51752bf2846ed13a0c976af04d128956fffc91f17771` |
| `data/bots_meta.csv` | `34932bab666e744340d7e4f1a662bdce595a8b215745c1bcdb0cd6b0caf7e659` |
| `data/bots_config_v2.csv` | `e54ee4ea9f3bfa7da5939920cddf5f88814297f3fb5f6be0151c7f43a462aef9` |
| `data/bots_config_v2.template.csv` | `77556064409ea704eade027ec7fddee1c5526ad50e53e6b985c869aa9f8718c7` |
| `data/trades.csv` | `f3b9fe5c67d90ff80c2b4fd227410e0688adeb1348f336394e52bde58837b69e` |
| `data/hedge_tournament.csv` | `ce475eb92745ba39dd03fcf8e3259987b0dc87d4cbd7173ee68c9aea7fe1090b` |
| `scripts/build_ledger.py` | `9ec21da902e23cdbe5f9ea442a60a9d5ff7f8028b386b559d69bb0b3889cc321` |
| `data/mirror_baseline.csv` | `cdceb0a8d444e57047697c9d9f2d2f7211355858d1235c26f9c51e571eefadf3` |
