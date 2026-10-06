# Dispatch — loss-day evidence packets (Devin, read-only OA + backtest reads)

**Purpose:** move the token-heavy *gathering* half of the loss-day register to Devin. Devin collects
a hashed **evidence packet** per (bot, losing day). Cowork reads the packet and writes the
`data/loss_register.csv` row: root cause, fix and what we learned. **Devin gathers facts only.**

**Run 1 is a calibration.** 2026-08-26 · `IC-SPX-FastPT25-S2-130PM` has already been written up by
Cowork. Devin rebuilds the packet without seeing that answer, and Cowork compares the two. **Stop after this one
packet.** Days 2–7 are dispatched only after the calibration passes.

Queue after calibration (one packet per run unless Andy says otherwise):
`2026-08-27`, `2026-09-08`, `2026-09-18`, `2026-10-05` × `IC-SPX-FastPT25-S2-130PM` ·
`2026-09-30` × `IC-SPX-FastPT25-S2` · `2026-09-18` × `GF-QQQ-IC-{Ride,PT50,Trail,Touch0}` (one packet).

---

## The prompt (paste below the line)

---

You are working in the `bot-fleet-v2` repo, connected as a local folder. Fresh session — assume no
context from prior work.

**TARGET:** bot `IC-SPX-FastPT25-S2-130PM` · date **2026-08-27**.

(Run 1, 2026-08-26, PASSED calibration 2026-10-06 — bundle `data/captures/2026-10-06-loss-packet-20260826-s2-130pm/` is the reference shape. Reuse its methods; read its README first.)

**Read, in order:** `CLAUDE.md` (§3, §5, §9.1a) · `.agents/skills/option-alpha/SKILL.md` (the law) ·
`.agents/skills/oa-drive/SKILL.md` · this file.

⛔ **Do not open** `data/loss_register.csv` (Cowork writes it from your packet).

### ⛔ BOUNDARY
0. **YOU DO NOT LOG IN.** Andy authenticates Chrome first. If `/login` or a sign-in form appears,
   STOP and report. Never request, enter, store or read credentials.
1. **READ-ONLY.** Bots, automations, positions, account settings: read only. ⛔ No `Create Bot`, no
   toggles, no Save on any automation editor. ⛔ **Never click an automation NAME link in the bot
   log** — it opens the automation editor. Open log entries by clicking the row's INFO area.
   If an editor opens by accident, leave via its `Close` button, never `Save`, and report it.
   ⛔ Never click `Clear Log`.
2. **Backtests: READ ONLY.** Do not run, edit, rename or delete any backtest. Only read the existing
   tests listed in TASK §5.
3. **NO WIRE PROTOCOL.** DOM/JS reads are in scope. No API calls to OA, no replay, no network panel,
   no recorder. Scope every capture to `app.optionalpha.com`.
4. Assert `ACCOUNT` reads **Paper Trading** before any read. Anything live: STOP.

### ⛔ TRAPS (each has bitten before)
- **Drawer occlusion:** with a position drawer open, clicking the next grid row returns the
  PREVIOUS position's details, well-formed. **Close the drawer before every row open**, and confirm
  the drawer's strikes/side changed before recording.
- **Element-ref clicks silently no-op** on this app. Use the `oa-drive` dispatch helpers
  (pointer+mouse event sequence at `elementFromPoint`).
- **Automation Log pager:** a monitor run iterates over every open position (`1 / 2`, `2 / 2`).
  Record **every** iteration (chevron-right), not just the first page.
- **`/positions/closed` loads 30 rows at a time** — use `Load more` until the target date appears.
  `?bot=` URL params are ignored; filter rows by the bot-name `[title]`.
- **Tradier 1-min bars are only kept for ~20 trading days.** Request `1min` first. If it fails,
  fall back to `5min` and **record which interval you got.**

### TASK — one packet, six sections, facts only

**§1 Ledger.** Copy verbatim every `data/trades.csv` row where `bot` = target and `open_date`
starts with the target date (header + rows).

**§2 OA positions.** On `/positions/closed`, for each position of the target bot opened on the
target date:
- the Position Details text (strikes, credit, close price, P/L, risk, price at open and close)
- the **Trades list verbatim** (every Open/Close line with time, label and fill)
- for **every** trade's `Automation Log`: the full panel text, every pager iteration

**§3 Bot log.** `/bots/bot/<id>/log`, Date filter = target date. The bot id is in
`data/captures/2026-10-06-roster/02-roster-toggles-43-2026-10-06.tsv`. Record:
- the list of runs (time, automation, info) from 13:25 to 16:00
- the full decision text (every iteration) of each run in the **minute of each close** and the
  **minute before it**

**§4 Tape.** Copy `scripts/` and `.env` into a scratch root outside `data/`, e.g.
`/tmp/lp-<date>/`, and never into the repo. From that root call `tape.tradier_timesales(<underlying>,
<date>, token, "https://api.tradier.com", interval=...)`. Save the raw series (t, p, h, l) from
13:00–16:00 as CSV. Then derive, for **each short strike** of the target positions, **counting only bars at or after the position's open time**:
- the first bar where price came within $20, within $10, and at or through the strike
- the extreme beyond the strike, and the underlying close

State the interval used.

**§5 Backtest rows (read-only).** These existing tests reproduce the S2 shape (SPX .10Δ IC, $5 wings,
5y). Open each test page → positions list (`Load more` until the date appears). Copy the row for the
target date **verbatim**: strikes, open→close time, status, risk, P/L.
- 13:30 set: A0 `ZT217913212733763171103` · A1 `ZT217913213667172591104` · A2
  `ZT217913214071275321105` · A3 `ZT217913214243169681106` · A4 `ZT217913214629138811108` · A5
  `ZT217913214854667371110` · A6 `ZT217913221146838271122` · A7 `ZT217913221268980491124` · A8
  `ZT217913221505807901126` · A9 `ZT217913221702251821127` · A10 `ZT217913221818381131128`
- 11:00 set (use only for an 11:00-entry bot): B0 `ZT217913222049733751130` · B1
  `ZT217913222373382861132` · B2 `ZT217913222495258171133` · B3 `ZT217913222671105881135` · B4
  `ZT217913222793032421136`
- Record each test's name and its Settings-card `Exit Options` line next to its row.
- Then state **STRIKES MATCH / DO NOT MATCH**: do the backtest condor's four strikes equal the live
  position's strikes?

**§6 Derived facts table** (no interpretation): per position — side · short strike · credit · close
time · close label · which automation closed it · fill · P/L · underlying at close · underlying at
16:00 · "would it have expired OTM at 16:00?" (yes/no, from the tape).

⛔ **DO NOT write a root cause, a fix, a recommendation, or a "loss with fix" estimate.** That is
Cowork's job and the point of the calibration. Observations that look odd go under
`## Questions for Cowork`.

### DELIVERABLE
`data/captures/<today>-loss-packet-<YYYYMMDD>-s2-130pm/` containing:
- `01-ledger.csv` · `02-oa-positions.txt` · `03-bot-log.txt` · `04-tape-<interval>.csv` ·
  `05-backtest-rows.txt` · `06-facts.md`
- `README.md`: purpose · timestamp with TZ offset · the model/session you ran on · a
  file / sha256 / what table · `## Assumptions` · `## Questions for Cowork` · `## Refusals`
- `SHA256SUMS.txt`

Raw text is verbatim from the page or file. Do not paraphrase inside `01`–`05`.

### PROHIBITIONS
No git. No writes outside the bundle directory **except** appending a close-out entry to
`docs/session-log.md` — append with a shell `>>` heredoc **without reading the file**. No writes under `~/.claude`. Nothing written into `data/` other than the
bundle. Never reuse or re-run a script from a prior capture.

**Stop conditions:** 401/403/429 · `/login` · terms or payment prompt · non-Paper account · any
editor or destructive dialog opening · the target date not found on a surface after exhausting
`Load more`. A missing date is reported, never filled in.

### REPORT
The bundle path, its file list with sha256, the STRIKES MATCH line, the interval of the tape, and
the refusals. **Stop after this one packet.**
