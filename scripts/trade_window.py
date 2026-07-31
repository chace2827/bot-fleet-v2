#!/usr/bin/env python3
"""Trade-window heat map — WHEN do short strikes actually get touched / when
does adverse excursion peak, by hour x regime? (backlog COCKPIT LANE step 3;
cleanup-proposal.md §4 item 2). Generalizes the 11am-vs-1:30 entry-time
question into an empirical, all-days aggregate.

For every position (trade_id) in data/trades.csv:
  - MAE moment = the time-of-day of mae_date (worst adverse excursion for that
    leg; per-position we take the EARLIEST leg's mae_date so a condor counts
    once, at whichever leg was hit worse first).
  - Bucketed by hour-of-day (09:30-16:00 ET market hours) x regime (Drift /
    Trend / Chop / n/a), regime read from that day's tape file's per-underlying
    "label" (data/brief/<date>_tape.json) when one exists for the position's
    (date, underlying); else "n/a" (most of history predates tape.py).
  - "Touch" reuses daily_brief.py's leg_breach() logic (short strike vs the
    post-entry intraday high/low from the tape) — a touch requires tape
    coverage; positions without a same-day tape file can't be touch-scored
    (counted in the MAE-only aggregate, excluded from touch_rate's
    denominator — see the printed reconciliation).

OUTPUT: data/trade_window.csv — one row per (hour, regime):
  hour, regime, n_positions, n_touches, touch_rate, avg_mae_pct
  n_positions = count of positions whose MAE-hour falls in this bucket
    (tape or no tape -- this is the MAE aggregate, always available).
  n_touches / touch_rate = out of the SUBSET of those n_positions that had
    tape coverage that day (a per-leg short-strike touch check); touch_rate
    is that subset's touch fraction, not of n_positions overall when tape
    coverage is partial. avg_mae_pct = mean mae_pct across n_positions.

Idempotent full rebuild (matches hedge_tournament.py/build_ledger.py
convention) -- re-running replaces the whole CSV from the current ledger +
whatever tape files are on disk.

Usage: python3 scripts/trade_window.py
Run AFTER tape.py (so today's tape file exists) and BEFORE report.py.
"""
import csv, os, json, collections, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")
BRIEF = os.path.join(D, "brief")
OUT_CSV = os.path.join(D, "trade_window.csv")

MARKET_OPEN_MIN = 9 * 60 + 30    # 09:30
MARKET_CLOSE_MIN = 16 * 60       # 16:00


def fl(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load(name):
    p = os.path.join(D, name)
    return list(csv.DictReader(open(p))) if os.path.exists(p) else []


def hhmm(ts):
    return ts[11:16] if ts and len(ts) >= 16 else ""


def to_min(hm):
    try:
        h, m = hm.split(":")
        return int(h) * 60 + int(m)
    except (ValueError, AttributeError):
        return None


def hour_bucket(hm):
    """Hour-of-day bucket label, e.g. '09:30-10' for market open, else 'HH-HH+1'.
    Clamps to market hours 09:30-16:00; returns None outside that range (bad
    timestamp / after-hours artifact) so the caller can flag/skip it."""
    m = to_min(hm)
    if m is None or m < MARKET_OPEN_MIN or m > MARKET_CLOSE_MIN:
        return None
    h = m // 60
    if h == 9:
        return "09:30-10"
    return f"{h:02d}-{h+1:02d}"


HOUR_ORDER = ["09:30-10", "10-11", "11-12", "12-13", "13-14", "14-15", "15-16"]
REGIME_ORDER = ["Chop", "Drift", "Trend", "n/a"]


# ----------------------------------------------------------------------------
# tape access — mirrors hedge_tournament.py / daily_brief.py
# ----------------------------------------------------------------------------
def load_tapes():
    """date -> {underlying: tape_record}"""
    out = {}
    if not os.path.isdir(BRIEF):
        return out
    for fn in sorted(os.listdir(BRIEF)):
        if not fn.endswith("_tape.json"):
            continue
        day = fn[: -len("_tape.json")]
        try:
            tape = json.load(open(os.path.join(BRIEF, fn)))
        except (ValueError, OSError):
            continue
        out[day] = tape.get("underlyings", {})
    return out


def post_entry_window(series, entry_hm):
    """(low, high) of the intraday path from entry onward — same as daily_brief.py."""
    if not series:
        return None, None
    post = [b for b in series if b.get("t", "") >= (entry_hm or "00:00")]
    post = post or series
    lows = [b["l"] for b in post if b.get("l") is not None]
    highs = [b["h"] for b in post if b.get("h") is not None]
    return (min(lows) if lows else None, max(highs) if highs else None)


def short_strike(leg):
    if leg["structure"] == "shortputspread":
        sp = fl(leg.get("short_put"))
        return ("put", sp) if sp is not None else (None, None)
    if leg["structure"] == "shortcallspread":
        sc = fl(leg.get("short_call"))
        return ("call", sc) if sc is not None else (None, None)
    return (None, None)


def leg_touched(leg, post_lo, post_hi):
    """Did this leg's short strike get touched post-entry? True/False/None(n/a)."""
    side, strike = short_strike(leg)
    if side is None or strike is None:
        return None
    if side == "put":
        return post_lo is not None and post_lo <= strike
    return post_hi is not None and post_hi >= strike


def regime_for(tapes_by_date, day, underlying):
    tape_u = (tapes_by_date.get(day) or {}).get(underlying)
    if not tape_u:
        return "n/a", False
    return (tape_u.get("label") or "n/a"), True


# ----------------------------------------------------------------------------
def build():
    trades = load("trades.csv")
    tapes_by_date = load_tapes()

    by_pos = collections.defaultdict(list)
    for t in trades:
        by_pos[t["trade_id"]].append(t)

    # bucket[(hour, regime)] -> {"n": int, "touch_n": int (tape-covered), "touched": int, "mae": [pct,...]}
    buckets = collections.defaultdict(lambda: {"n": 0, "touch_n": 0, "touched": 0, "mae": []})

    n_total_pos = 0
    n_valid_mae = 0
    n_bad_hour = 0
    n_tape_covered_pos = 0

    for tid, legs in by_pos.items():
        n_total_pos += 1
        # pick the EARLIEST leg mae_date as the position's worst-excursion moment
        dated = [(lg["mae_date"], lg) for lg in legs if lg.get("mae_date")]
        if not dated:
            continue  # no mae_date at all for this position (shouldn't happen per recon check)
        dated.sort(key=lambda x: x[0])
        mae_ts, mae_leg = dated[0]
        n_valid_mae += 1
        hm = hhmm(mae_ts)
        hb = hour_bucket(hm)
        if hb is None:
            n_bad_hour += 1
            continue

        day = legs[0]["open_date"][:10]
        underlying = legs[0]["underlying"]
        regime, has_tape = regime_for(tapes_by_date, day, underlying)

        # avg MAE% for the bucket: average the position's legs' mae_pct
        mae_pcts = [fl(lg.get("mae_pct")) for lg in legs if fl(lg.get("mae_pct")) is not None]
        pos_mae = sum(mae_pcts) / len(mae_pcts) if mae_pcts else None

        key = (hb, regime)
        b = buckets[key]
        b["n"] += 1
        if pos_mae is not None:
            b["mae"].append(pos_mae)

        # touch check: only when tape covers this (date, underlying)
        if has_tape:
            n_tape_covered_pos += 1
            tape_u = tapes_by_date[day][underlying]
            series = tape_u.get("series") or []
            entry_hm = min((hhmm(lg["open_date"]) for lg in legs), default="00:00")
            post_lo, post_hi = post_entry_window(series, entry_hm)
            touched_any = False
            any_applicable = False
            for lg in legs:
                t = leg_touched(lg, post_lo, post_hi)
                if t is None:
                    continue
                any_applicable = True
                if t:
                    touched_any = True
            if any_applicable:
                b["touch_n"] += 1
                if touched_any:
                    b["touched"] += 1

    # --- emit CSV --------------------------------------------------------------
    rows = []
    for hour in HOUR_ORDER:
        for regime in REGIME_ORDER:
            b = buckets.get((hour, regime))
            if not b or b["n"] == 0:
                continue
            touch_rate = (b["touched"] / b["touch_n"]) if b["touch_n"] else None
            avg_mae = (sum(b["mae"]) / len(b["mae"])) if b["mae"] else None
            rows.append({
                "hour": hour, "regime": regime, "n_positions": b["n"],
                "n_touches": b["touched"], "touch_rate": round(touch_rate, 4) if touch_rate is not None else "",
                "avg_mae_pct": round(avg_mae, 4) if avg_mae is not None else "",
            })
    # keep any (hour, regime) combos that exist in buckets but weren't in the fixed
    # order lists (defensive; shouldn't happen with the fixed vocab above)
    for (hour, regime), b in buckets.items():
        if hour in HOUR_ORDER and regime in REGIME_ORDER:
            continue
        if b["n"] == 0:
            continue
        touch_rate = (b["touched"] / b["touch_n"]) if b["touch_n"] else None
        avg_mae = (sum(b["mae"]) / len(b["mae"])) if b["mae"] else None
        rows.append({
            "hour": hour, "regime": regime, "n_positions": b["n"],
            "n_touches": b["touched"], "touch_rate": round(touch_rate, 4) if touch_rate is not None else "",
            "avg_mae_pct": round(avg_mae, 4) if avg_mae is not None else "",
        })

    with open(OUT_CSV, "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=["hour", "regime", "n_positions", "n_touches",
                                           "touch_rate", "avg_mae_pct"])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    n_bucketed = sum(b["n"] for b in buckets.values())
    print(f"trade_window.py: {n_total_pos} ledger positions | {n_valid_mae} with a valid mae_date "
          f"| {n_bad_hour} outside 09:30-16:00 (dropped) | {n_bucketed} bucketed "
          f"| {n_tape_covered_pos} positions had same-day tape coverage (touch-scored) "
          f"| reconciliation: {n_bucketed} bucketed == {n_valid_mae - n_bad_hour} valid-in-range "
          f"({'OK' if n_bucketed == n_valid_mae - n_bad_hour else 'MISMATCH'}) "
          f"-> {len(rows)} (hour,regime) rows -> data/trade_window.csv")
    return n_bucketed == (n_valid_mae - n_bad_hour)


if __name__ == "__main__":
    ok = build()
    raise SystemExit(0 if ok else 1)
