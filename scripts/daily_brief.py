#!/usr/bin/env python3
"""Compute the automatable half of the Fleet Brief for one trading day.

For every ON bot that traded `day` it builds the **instruction-mirror after-action
card** on the skeleton of the bot's OWN config (Filter → Entry → Profit-target →
Hedge → Re-entry → Verdict), comparing PROGRAMMED (from data/bots_config.csv +
bots_meta.csv) vs ACTUAL (derived from that day's ledger legs), flagging each row
✓ (executed as designed) or ⚠ (deviation — the thing that mattered). It also
computes per-leg breach flags (short strike vs the day's high/low from the tape),
a behavior grade (green/amber/red — process, not P/L), and a hedge counterfactual
for each breach (cut helped vs hurt; naked loss = a hedge candidate).

OUTPUTS
  data/brief/<date>_brief.json  — structured pack Claude renders (cards + charts + clinic).
  data/compliance.csv           — APPEND/UPSERT one row per (bot, date): compliance_pct,
                                  grade, breaches, naked_losses. This is the feed that
                                  LIGHTS the readiness board's G5 gate in report.py.

Grade is BEHAVIOR not outcome:
  green = did exactly what its config says (fired on a GO, hedge fired on a touch),
          win or lose;  amber = clean process but a losing day (a "good loss") or a
          borderline call;  red = a real deviation (fired on a NO-GO, wrong entry
          time, a hedge that should have fired didn't, rode past a stop).

Usage:  python3 scripts/daily_brief.py [YYYY-MM-DD]   (default = newest ledger date)
Run AFTER build_ledger.py + tape.py, and BEFORE report.py (so G5 reads fresh compliance).
"""
import csv, os, sys, json, datetime, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")
BRIEF = os.path.join(D, "brief")

EXPIRY_CUT = "15:58"     # close at/after this = rode to expiry/settlement
ENTRY_TOL_MIN = 6        # actual entry must land within this of programmed time
BAND = 0.75              # Range075 GO band, ±% from prior close
MAXLOSS_ROR = -0.9       # ror at/below this = (near) max loss = a definite breach


def fl(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load(name, required=True):
    """Missing OPTIONAL inputs degrade to empty rather than crashing. The n=0
    state (no post-cutover data yet) must produce a brief that says so, not a
    traceback."""
    path = os.path.join(D, name)
    if not os.path.exists(path):
        if required:
            sys.exit(f"daily_brief.py: missing required input {name} "
                     f"— run scripts/build_ledger.py first")
        return []
    return list(csv.DictReader(open(path)))


def hhmm(ts):
    return ts[11:16] if ts and len(ts) >= 16 else ""


def to_min(hm):
    try:
        h, m = hm.split(":")
        return int(h) * 60 + int(m)
    except (ValueError, AttributeError):
        return None


def first_int(s):
    m = re.search(r"\d+", s or "")
    return int(m.group()) if m else None


# ----------------------------------------------------------------------------
def exit_mode(leg):
    """Classify how a leg left the position from its close time + P/L."""
    pnl = fl(leg["pnl"]) or 0.0
    rode = hhmm(leg["close_date"]) >= EXPIRY_CUT
    if rode:
        return "expired-win" if pnl >= 0 else "expiry-loss"   # rode to settlement
    return "profit-exit" if pnl >= 0 else "defensive-exit"     # left early


def post_entry_window(series, entry_hm):
    """(low, high) of the intraday path FROM the bot's entry time onward. Using the
    post-entry window (not the full-day range) is what makes a late-entry bot's
    breach flag correct — a pre-entry spike to a strike isn't a breach of a
    position that didn't exist yet (e.g. 6/26 SPX hit 7294 at 9:30, but the 11:00
    champion's post-entry low was 7335, well above its 7300 short put)."""
    if not series:
        return None, None
    post = [b for b in series if b.get("t", "") >= (entry_hm or "00:00")]
    post = post or series
    lows = [b["l"] for b in post if b.get("l") is not None]
    highs = [b["h"] for b in post if b.get("h") is not None]
    return (min(lows) if lows else None, max(highs) if highs else None)


def leg_breach(leg, post_lo, post_hi, approx):
    """Did this leg's SHORT strike get breached? (definite | approx | no).
    Definite: near-max-loss ror, or underlying_close beyond the short strike.
    Path: the POST-ENTRY intraday low/high crossed the short strike (exact with
    Tradier timesales; ~approx if reconstructed with no real path)."""
    pnl, risk = fl(leg["pnl"]), fl(leg["risk"])
    ror = (pnl / risk) if (pnl is not None and risk) else None
    uc = fl(leg["underlying_close"])
    if leg["structure"] == "shortputspread":
        sp = fl(leg["short_put"])
        if sp is None:
            return "n/a", None
        if (ror is not None and ror <= MAXLOSS_ROR) or (uc is not None and uc <= sp):
            return "BREACH", sp
        if post_lo is not None and post_lo <= sp:
            return ("BREACH~" if approx else "BREACH"), sp
        return "NO BREACH", sp
    if leg["structure"] == "shortcallspread":
        sc = fl(leg["short_call"])
        if sc is None:
            return "n/a", None
        if (ror is not None and ror <= MAXLOSS_ROR) or (uc is not None and uc >= sc):
            return "BREACH", sc
        if post_hi is not None and post_hi >= sc:
            return ("BREACH~" if approx else "BREACH"), sc
        return "NO BREACH", sc
    return "n/a", None


# ----------------------------------------------------------------------------
def build_card(bot, cfg, meta, legs, tape_u):
    """One instruction-mirror card: rows (programmed vs actual, ✓/⚠) + grade."""
    condors = collections.defaultdict(list)
    for lg in legs:
        condors[lg["trade_id"]].append(lg)
    n_cond = len(condors)
    hedge_type = (meta.get("hedge") or "").strip() or "none"
    is_naked = hedge_type.lower() in ("", "none", "unstopped")

    rows = []          # each: {name, programmed, actual, flag} flag ∈ ✓ ⚠ ·
    breach_lines = []  # per-leg §1 lines
    naked_losses = []  # breached + rode-to-expiry + no hedge = hedge candidate
    counterfactuals = []

    # ---- Filter (Range075 verifiable from strikes; other filters: note only) --
    filt = cfg.get("filter", "")
    pc = (tape_u or {}).get("prior_close")
    if "range075" in filt.lower() and pc:
        outside = []
        for tid, lg in condors.items():
            sp = next((fl(x["short_put"]) for x in lg if fl(x["short_put"])), None)
            sc = next((fl(x["short_call"]) for x in lg if fl(x["short_call"])), None)
            center = None
            if sp and sc:
                center = (sp + sc) / 2
            elif lg:
                center = fl(lg[0]["underlying_open"])
            if center:
                dev = abs(center - pc) / pc * 100
                if dev > BAND + 0.05:
                    outside.append(round(dev, 2))
        if outside:
            rows.append({"name": "Filter", "programmed": filt,
                         "actual": f"{len(outside)}/{n_cond} entries outside ±{BAND}% "
                                   f"(worst {max(outside)}%) — fired on a NO-GO",
                         "flag": "⚠"})
        else:
            rows.append({"name": "Filter", "programmed": filt,
                         "actual": f"all {n_cond} entries inside ±{BAND}% band",
                         "flag": "✓"})
    else:
        rows.append({"name": "Filter", "programmed": filt or "—",
                     "actual": "not ledger-verifiable (needs the intraday gate value)",
                     "flag": "·"})

    # ---- Entry time ----------------------------------------------------------
    # Validate ONLY the first (initial) entry against the programmed time.
    # Re-entries fire later through the session by design and are governed by the
    # Re-entry cap row, NOT the entry window — treating each re-entry timestamp as
    # "drift" produced false REDs on busy scalper days (e.g. the champion's
    # 11:01→11:27 ladder on 2026-07-01). Band violations on any condor are still
    # caught by the Filter row; too many re-entries by the Re-entry row.
    prog_t = cfg.get("entry_time", "")
    prog_min = to_min(prog_t)
    entry_times = sorted({hhmm(lg[0]["open_date"]) for lg in condors.values() if lg})
    first_entry = entry_times[0] if entry_times else None
    reentries = entry_times[1:]
    # Bell drift = ANY entry before 11:00 when the gate is >=11:00 (an early entry
    # nullifies Range075 — the real failure this check exists to catch).
    early_bell = [t for t in entry_times if to_min(t) is not None and to_min(t) < 11 * 60
                  and prog_min is not None and prog_min >= 11 * 60]
    if prog_min is not None and first_entry is not None:
        first_min = to_min(first_entry)
        first_late = first_min is not None and (first_min - prog_min) > ENTRY_TOL_MIN
        reentry_note = (f" · +{len(reentries)} re-entr{'y' if len(reentries) == 1 else 'ies'} "
                        f"through {reentries[-1]} (by design)") if reentries else ""
        if early_bell:
            rows.append({"name": "Entry", "programmed": prog_t,
                         "actual": f"{early_bell} — BELL DRIFT (before 11:00; gate not holding)",
                         "flag": "⚠"})
        elif first_late:
            rows.append({"name": "Entry", "programmed": prog_t,
                         "actual": f"first entry {first_entry} late vs {prog_t} "
                                   f"(>{ENTRY_TOL_MIN}m){reentry_note}",
                         "flag": "⚠"})
        else:
            rows.append({"name": "Entry", "programmed": prog_t,
                         "actual": f"first entry {first_entry} ✓ on time{reentry_note}",
                         "flag": "✓"})
    else:
        rows.append({"name": "Entry", "programmed": prog_t or "—",
                     "actual": ", ".join(entry_times) or "—", "flag": "·"})

    # ---- Profit target -------------------------------------------------------
    pt = cfg.get("profit_target", "")
    modes = collections.Counter(exit_mode(lg) for legset in condors.values() for lg in legset)
    pt_prog = bool(re.search(r"pt\s*\d+|\d+%", pt.lower())) if pt else False
    if pt_prog:
        took = modes["profit-exit"]
        won_exp = modes["expired-win"]
        if took or won_exp:
            rows.append({"name": "Profit target", "programmed": pt,
                         "actual": f"{took} PT-exit + {won_exp} expired-worthless-win"
                                   + (" (never needed PT)" if won_exp and not took else ""),
                         "flag": "✓"})
        else:
            rows.append({"name": "Profit target", "programmed": pt,
                         "actual": "no profit leg today (all losers/held)", "flag": "·"})
    else:  # 'none' / ride
        rode = modes["expired-win"] + modes["expiry-loss"]
        rows.append({"name": "Profit target", "programmed": pt or "none (ride)",
                     "actual": f"{rode} rode to settlement" + (" ✓" if rode else ""),
                     "flag": "✓" if rode else "·"})

    # ---- Hedge (+ breach lines + counterfactual) -----------------------------
    hedge_failed = False
    hedge_fired = 0
    series = (tape_u or {}).get("series") or []
    approx = (tape_u or {}).get("source") == "reconstructed"
    for tid, legset in sorted(condors.items()):
        entry_hm = min((hhmm(lg["open_date"]) for lg in legset), default="00:00")
        post_lo, post_hi = post_entry_window(series, entry_hm)
        for lg in legset:
            state, strike = leg_breach(lg, post_lo, post_hi, approx)
            if state == "n/a":
                continue
            side = "put" if lg["structure"] == "shortputspread" else "call"
            m = exit_mode(lg)
            pnl = fl(lg["pnl"]) or 0.0
            applied = "—"
            if state.startswith("BREACH"):
                if m == "defensive-exit":
                    applied = "hedge FIRED (cut early)"; hedge_fired += 1
                    counterfactuals.append(
                        f"{side} {strike}: cut at ${pnl:,.0f}; hold-to-expiry ≈ "
                        f"{'still breached → max loss (cut HELPED)' if _still_out(lg, side, strike) else 'recovered inside → cut may have HURT'}")
                elif m == "expiry-loss":
                    if is_naked:
                        applied = "none (by design) — rode to expiry"
                        naked_losses.append(f"{bot} {side} {strike}: naked ${pnl:,.0f} loss — hedge candidate")
                    else:
                        applied = "hedge FAILED to fire — rode to expiry"
                        hedge_failed = True
                        naked_losses.append(f"{bot} {side} {strike}: {hedge_type} did not fire, ${pnl:,.0f}")
                else:
                    applied = f"{m}"
            tag = state + (" (approx)" if state.endswith("~") else "")
            breach_lines.append(f"{side} short {strike} · {tag.replace('~','')} · {applied}")
    if hedge_failed:
        rows.append({"name": "Hedge", "programmed": hedge_type,
                     "actual": "a short strike was touched but the hedge did NOT fire — rode to loss",
                     "flag": "⚠"})
    elif is_naked and naked_losses:
        rows.append({"name": "Hedge", "programmed": f"{hedge_type} (naked by design)",
                     "actual": "breach rode to expiry — the ABSENT hedge is the lesson",
                     "flag": "·"})
    elif hedge_fired:
        rows.append({"name": "Hedge", "programmed": hedge_type,
                     "actual": f"fired on {hedge_fired} touched leg(s) — cut as designed",
                     "flag": "✓"})
    else:
        rows.append({"name": "Hedge", "programmed": hedge_type,
                     "actual": "no breach today — nothing to hedge", "flag": "✓"})

    # ---- Re-entry cap --------------------------------------------------------
    cap = first_int(cfg.get("reentry", ""))
    if cap is not None:
        rows.append({"name": "Re-entry", "programmed": cfg.get("reentry", ""),
                     "actual": f"{n_cond} condor(s) today",
                     "flag": "✓" if n_cond <= cap else "⚠"})
    else:
        rows.append({"name": "Re-entry", "programmed": cfg.get("reentry", "") or "—",
                     "actual": f"{n_cond} condor(s) today", "flag": "·"})

    # ---- grade + verdict -----------------------------------------------------
    day_pnl = sum(fl(lg["pnl"]) or 0.0 for legset in condors.values() for lg in legset)
    hard_fail = any(r["flag"] == "⚠" and r["name"] in ("Filter", "Entry", "Hedge") for r in rows)
    if hard_fail:
        grade = "red"
    elif day_pnl >= 0 and all(r["flag"] != "⚠" for r in rows):
        grade = "green"
    else:
        grade = "amber"  # clean process, losing day (good loss) or borderline
    lesson = _lesson(grade, day_pnl, naked_losses, hedge_fired, is_naked)
    rows.append({"name": "Verdict",
                 "programmed": "behave as designed",
                 "actual": f"P/L ${day_pnl:,.0f} · {grade.upper()} — {lesson}",
                 "flag": {"green": "✓", "amber": "·", "red": "⚠"}[grade]})

    applic = [r for r in rows if r["flag"] in ("✓", "⚠") and r["name"] != "Verdict"]
    n_pass = sum(1 for r in applic if r["flag"] == "✓")
    compliance = round(n_pass / len(applic) * 100) if applic else None

    return {"bot": bot, "hedge_type": hedge_type, "n_condors": n_cond,
            "day_pnl": round(day_pnl), "grade": grade, "rows": rows,
            "breach_lines": breach_lines, "naked_losses": naked_losses,
            "counterfactuals": counterfactuals,
            "compliance_pct": compliance, "n_applicable": len(applic), "n_pass": n_pass}


def _still_out(lg, side, strike):
    uc = fl(lg["underlying_close"])
    if uc is None or strike is None:
        return True
    return uc <= strike if side == "put" else uc >= strike


def _lesson(grade, pnl, naked, fired, is_naked):
    if naked and is_naked:
        return "naked breach rode to expiry — log a convexity/hedge candidate here"
    if grade == "red":
        return "deviation from config — see the ⚠ row"
    if grade == "amber":
        return "good loss — design held, tape unlucky" if pnl < 0 else "borderline; watch"
    return "clean win" if fired == 0 else "hedge did its job"


# ----------------------------------------------------------------------------
def upsert_compliance(rowsout):
    """APPEND/UPSERT (bot, date) rows into data/compliance.csv — the G5 feed."""
    path = os.path.join(D, "compliance.csv")
    cols = ["date", "bot", "compliance_pct", "n_applicable", "n_pass",
            "grade", "n_condors", "day_pnl", "breaches", "naked_losses"]
    existing = {}
    if os.path.exists(path):
        for r in csv.DictReader(open(path)):
            existing[(r["date"], r["bot"])] = r
    for r in rowsout:
        existing[(r["date"], r["bot"])] = r
    with open(path, "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=cols)
        w.writeheader()
        for k in sorted(existing):
            row = existing[k]
            w.writerow({c: row.get(c, "") for c in cols})


def build(day):
    trades = load("trades.csv")
    # CONFIG SOURCE: bots_config_v2.csv ONLY — built from capture (CLAUDE.md §3).
    # The v1 data/archive/bots_config.csv is the discredited hand-written record
    # (wrong on 3 of 4 audited bots) and must NEVER be read for a config fact.
    # Absent v2 config => grade nothing rather than grade against a false record.
    # AMENDED 2026-08-08 — same defect class as execution_audit.py's gate-A9
    # split (i), fixed the same day (session-log 2026-08-08): the file as built
    # is a CAPTURE INVENTORY — a '#' comment preamble, heterogeneous object rows
    # keyed by `object_kind`, identity in `name`, and NONE of the mechanic
    # columns this brief grades against (filter / entry_time / profit_target /
    # reentry). csv.DictReader ate the preamble as a header and r["bot"] crashed.
    # Now: skip '#' lines; key on 'bot' if that column exists (the v1 contract),
    # else 'name' filtered to object_kind == 'bot'; and if the schema carries
    # NONE of the graded mechanic columns, stay CONFIG-BLIND loudly — grading
    # against a record that does not declare mechanics is scoring fidelity to
    # nothing. Never silence, never a crash.
    cfgs, cfg_blind_reason = {}, "NO data/bots_config_v2.csv"
    _cfg_path = os.path.join(D, "bots_config_v2.csv")
    if os.path.exists(_cfg_path):
        with open(_cfg_path, newline="") as _fh:
            _rdr = csv.DictReader(ln for ln in _fh if not ln.lstrip().startswith("#"))
            _hdr = [f.strip() for f in (_rdr.fieldnames or [])]
            _rows = list(_rdr)
        _MECH = {"filter", "entry_time", "profit_target", "reentry"}
        if "bot" in _hdr:
            cfgs = {r["bot"]: r for r in _rows if (r.get("bot") or "").strip()}
        elif "name" in _hdr and (_MECH & set(_hdr)):
            if "object_kind" in _hdr:
                _rows = [r for r in _rows if (r.get("object_kind") or "").strip() == "bot"]
            cfgs = {r["name"]: r for r in _rows if (r.get("name") or "").strip()}
        else:
            cfg_blind_reason = (f"bots_config_v2.csv present but its schema carries "
                                f"none of the graded mechanic columns {sorted(_MECH)} "
                                f"(header starts: {_hdr[:4]})")
    if not cfgs:
        print(f"daily_brief.py: {cfg_blind_reason} — running CONFIG-BLIND. "
              "Instruction-mirror compliance is NOT graded (it would be scoring "
              "fidelity to a record that does not exist). This is not a pass.")
    metas = {r["bot"]: r for r in load("bots_meta.csv")}
    tape_path = os.path.join(BRIEF, f"{day}_tape.json")
    tape = json.load(open(tape_path)) if os.path.exists(tape_path) else {"underlyings": {}}
    tape_u = tape.get("underlyings", {})

    by_bot = collections.defaultdict(list)
    for t in trades:
        if t["open_date"][:10] == day:
            by_bot[t["bot"]].append(t)

    cards, comp_rows = [], []
    for bot in (sorted(by_bot) if cfgs else []):
        meta = metas.get(bot, {})
        if (meta.get("status", "OFF").upper() != "ON"):
            continue  # only grade ON bots
        cfg = cfgs.get(bot, {})
        card = build_card(bot, cfg, meta, by_bot[bot], tape_u.get(meta.get("underlying", "")))
        cards.append(card)
        comp_rows.append({"date": day, "bot": bot,
                          "compliance_pct": card["compliance_pct"],
                          "n_applicable": card["n_applicable"], "n_pass": card["n_pass"],
                          "grade": card["grade"], "n_condors": card["n_condors"],
                          "day_pnl": card["day_pnl"],
                          "breaches": len([b for b in card["breach_lines"] if "BREACH" in b and "NO BREACH" not in b]),
                          "naked_losses": len(card["naked_losses"])})

    out = {"date": day,
           "generated": datetime.datetime.now().isoformat(timespec="seconds"),
           "tape": tape, "cards": cards,
           "hedge_clinic": [nl for c in cards for nl in c["naked_losses"]],
           "grades": {g: sum(1 for c in cards if c["grade"] == g)
                      for g in ("green", "amber", "red")}}
    os.makedirs(BRIEF, exist_ok=True)
    json.dump(out, open(os.path.join(BRIEF, f"{day}_brief.json"), "w"), indent=2)
    if comp_rows:
        upsert_compliance(comp_rows)

    g = out["grades"]
    print(f"daily_brief.py: {day} | {len(cards)} ON bots graded "
          f"(🟢{g['green']} 🟡{g['amber']} 🔴{g['red']}) | "
          f"{len(out['hedge_clinic'])} hedge-candidate breach(es) | "
          f"wrote brief/{day}_brief.json + compliance.csv")
    return out


def newest_date():
    return max((t["open_date"][:10] for t in load("trades.csv")),
               default=datetime.date.today().isoformat())


if __name__ == "__main__":
    day = sys.argv[1] if len(sys.argv) > 1 else newest_date()
    build(day)
