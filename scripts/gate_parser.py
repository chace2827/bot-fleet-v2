#!/usr/bin/env python3
"""Mechanics / gate parser for the SHOULD-HAVE-FIRED report.

Reads the SIGNED gate source (data/bot_gates.csv) and evaluates one gate
against a day's TAPE.  Every semantics below is taken from the header
comment block of data/bot_gates.csv and the 2026-08-18 signed package.
"""

import csv
import datetime
import re
from collections import namedtuple

Verdict = namedtuple("Verdict", ["verdict", "reason"])


def parse_gate_params(params):
    """Parse a 'k=v,k=v' string into a dict."""
    out = {}
    if not params:
        return out
    for token in params.split(","):
        token = token.strip()
        if not token or "=" not in token:
            continue
        k, v = token.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def parse_time(s):
    m = re.match(r"^(\d{1,2}):(\d{2})$", s or "")
    if not m:
        return None
    return int(m.group(1)) * 60 + int(m.group(2))


def parse_window(s):
    """Return (start_minutes, end_minutes, mode) where mode is one of:
    'single', 'range', 'after', 'none'.
    """
    s = (s or "").strip()
    if not s:
        return None, None, "none"
    m = re.match(r"^after\s+(\d{1,2}:\d{2})$", s, re.I)
    if m:
        return parse_time(m.group(1)), None, "after"
    m = re.match(r"^(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})$", s)
    if m:
        return parse_time(m.group(1)), parse_time(m.group(2)), "range"
    m = re.match(r"^(\d{1,2}:\d{2})$", s)
    if m:
        return parse_time(m.group(1)), None, "single"
    # non-numeric tokens such as 'daily' or 'Friday'
    if re.match(r"^[A-Za-z]", s):
        return None, None, "none"
    return None, None, "none"


def select_bars(series, start, end, mode):
    """Pick the 5-min bar(s) in a window."""
    if mode == "none" or start is None:
        return []
    out = []
    for b in series:
        t = b.get("t", "")
        tm = parse_time(t)
        if tm is None:
            continue
        if mode == "single" and tm == start:
            return [b]
        if mode == "range" and tm >= start and (end is None or tm < end):
            out.append(b)
        if mode == "after" and tm > start:
            out.append(b)
    return out


def pct_change(value, prior):
    if value is None or prior is None or prior == 0:
        return None
    return round((value - prior) / prior * 100, 2)


def load_bot_gates(path):
    rows = []
    with open(path, newline="") as f:
        reader = csv.DictReader(line for line in f if not line.startswith("#"))
        for r in reader:
            extras = r.pop(None, None)
            row = {k: (v or "").strip() for k, v in r.items()}
            if extras:
                row["__extras"] = extras
            rows.append(row)
    return rows


def needed_underlyings(row):
    """The tape underlyings a bot's gate needs to evaluate.

    This follows the per-underlying source rule: only underlyings the gate
    actually consumes are checked.  UNEVALUABLE_BY_DESIGN and UNEVALUABLE_FLOOR
    rows are handled before this is called.
    """
    gt = (row.get("gate_type") or "").strip()
    ec = (row.get("eval_class") or "").strip()
    if gt == "weekday":
        return []
    if gt == "unknown":
        return []
    if gt == "none" and ec == "UNEVALUABLE_FLOOR":
        return []
    u = (row.get("underlying") or "").strip()
    return [u] if u else []


def get_underlying(tape, symbol):
    return tape.get("underlyings", {}).get(symbol)


def check_underlyings(row, tape, date):
    for u in needed_underlyings(row):
        rec = get_underlying(tape, u)
        if rec is None:
            return Verdict("UNEVALUABLE_MISSING", f"{u} missing from {date} tape")
        src = rec.get("source")
        if src != "tradier":
            return Verdict("UNEVALUABLE_SOURCE", f"{u} source={src} (need tradier) on {date}")
    return None


def evaluate_gate(row, tape, date):
    ec = (row.get("eval_class") or "").strip()
    if ec == "UNEVALUABLE_BY_DESIGN":
        return Verdict(
            "UNEVALUABLE_BY_DESIGN",
            f"gate_type={row.get('gate_type')} for {row['bot']}; no signed entry condition",
        )
    if ec == "UNEVALUABLE_FLOOR":
        return Verdict("UNEVALUABLE_FLOOR", "fill_precondition credit floor value unrecorded")

    v = check_underlyings(row, tape, date)
    if v:
        return v

    gt = (row.get("gate_type") or "").strip()
    if gt == "none":
        return Verdict("SUSPECT", "no market gate and no fill_precondition declared; silence is suspect")
    if gt == "weekday":
        return eval_weekday(row, date)
    if gt == "band_prior_close":
        return eval_band_prior_close(row, tape, date)
    if gt == "band_prior_close_strict":
        return eval_band_prior_close_strict(row, tape, date)
    if gt == "vix_min":
        return eval_vix_min(row, tape, date)
    if gt == "vix_change_max":
        return eval_vix_change_max(row, tape, date)
    if gt == "orb_60min":
        return eval_orb_60min(row, tape, date)
    return Verdict("UNEVALUABLE_BY_DESIGN", f"gate_type={gt} for {row['bot']} not handled")


def eval_weekday(row, date):
    params = parse_gate_params(row.get("gate_params", ""))
    day = params.get("day", "Fri")
    try:
        d = datetime.date.fromisoformat(date)
    except Exception:
        return Verdict("UNEVALUABLE", f"cannot parse date {date}")
    actual = d.strftime("%a")
    if actual == day:
        return Verdict("SUSPECT", f"date is {actual}, gate requires {day}")
    return Verdict("JUSTIFIED", f"date is {actual}, gate requires {day}")


def eval_band_prior_close(row, tape, date):
    u = needed_underlyings(row)[0]
    rec = get_underlying(tape, u)
    prior = rec.get("prior_close")
    if prior is None:
        return Verdict("UNEVALUABLE_MISSING", f"{u} prior_close missing")
    if not rec.get("series"):
        return Verdict("UNEVALUABLE_MISSING", f"{u} 5-min series missing")
    params = parse_gate_params(row.get("gate_params", ""))
    try:
        threshold = float(params["abs_lt"])
    except Exception:
        return Verdict("UNEVALUABLE", "abs_lt missing or malformed")

    start, end, mode = parse_window(row.get("entry_window_et", ""))
    bars = select_bars(rec["series"], start, end, mode)
    if not bars:
        return Verdict("UNEVALUABLE_MISSING_BAR", f"no {u} 5-min bars in window {row.get('entry_window_et')}")

    met_bar = None
    for b in bars:
        dlt = pct_change(b.get("p"), prior)
        if dlt is not None and abs(dlt) < threshold:
            met_bar = b
            break

    if met_bar:
        dlt = pct_change(met_bar["p"], prior)
        return Verdict(
            "SUSPECT",
            f"{u} p={met_bar['p']} at {met_bar['t']}, Δ%={dlt}, |Δ%|={abs(dlt)} < threshold {threshold}",
        )

    # Justified: report the most-extreme |Δ%| seen in the window.
    def _abs(b):
        d = pct_change(b.get("p"), prior)
        return abs(d) if d is not None else -1

    rep = max(bars, key=_abs)
    max_abs = _abs(rep)
    if max_abs < 0:
        return Verdict("UNEVALUABLE_MISSING", "no usable prices in window")
    dlt = pct_change(rep["p"], prior)
    return Verdict(
        "JUSTIFIED",
        f"{u} max |Δ%|={max_abs} (p={rep['p']} at {rep['t']}, Δ%={dlt}) vs threshold <{threshold}",
    )


def eval_band_prior_close_strict(row, tape, date):
    u = needed_underlyings(row)[0]
    rec = get_underlying(tape, u)
    prior = rec.get("prior_close")
    if prior is None:
        return Verdict("UNEVALUABLE_MISSING", f"{u} prior_close missing")
    if not rec.get("series"):
        return Verdict("UNEVALUABLE_MISSING", f"{u} 5-min series missing")
    params = parse_gate_params(row.get("gate_params", ""))
    try:
        gt = float(params["gt"])
        lt = float(params["lt"])
    except Exception:
        return Verdict("UNEVALUABLE", "gt/lt missing or malformed")

    start, end, mode = parse_window(row.get("entry_window_et", ""))
    bars = select_bars(rec["series"], start, end, mode)
    if not bars:
        return Verdict("UNEVALUABLE_MISSING_BAR", f"no {u} 5-min bars in window {row.get('entry_window_et')}")

    met_bar = None
    for b in bars:
        dlt = pct_change(b.get("p"), prior)
        if dlt is not None and gt < dlt < lt:
            met_bar = b
            break

    if met_bar:
        dlt = pct_change(met_bar["p"], prior)
        return Verdict(
            "SUSPECT",
            f"{u} p={met_bar['p']} at {met_bar['t']}, Δ%={dlt}, within {gt}<Δ%<{lt}",
        )

    # Find the first bar that is outside the band.
    for b in bars:
        dlt = pct_change(b.get("p"), prior)
        if dlt is not None and (dlt <= gt or dlt >= lt):
            return Verdict(
                "JUSTIFIED",
                f"{u} p={b['p']} at {b['t']}, Δ%={dlt}, outside {gt}<Δ%<{lt}",
            )
    return Verdict("UNEVALUABLE_MISSING", "no usable prices in window")


def eval_vix_min(row, tape, date):
    u = needed_underlyings(row)[0]
    rec = get_underlying(tape, u)
    prior = rec.get("prior_close")
    high = rec.get("high")
    low = rec.get("low")
    if high is None or low is None or prior is None:
        return Verdict("UNEVALUABLE_MISSING", "VIX high/low/prior_close missing")
    params = parse_gate_params(row.get("gate_params", ""))
    try:
        threshold = float(params["threshold"])
    except Exception:
        return Verdict("UNEVALUABLE", "threshold missing or malformed")

    if high < threshold:
        return Verdict(
            "JUSTIFIED",
            f"VIX high={high}, low={low}, prior_close={prior}; threshold >={threshold}; high < threshold all day",
        )
    if low >= threshold:
        return Verdict(
            "SUSPECT",
            f"VIX high={high}, low={low}, prior_close={prior}; threshold >={threshold}; low >= threshold all day",
        )
    return Verdict(
        "UNEVALUABLE_INTRADAY",
        f"VIX high={high} >= {threshold} but low={low} < {threshold}; straddles threshold; no intraday VIX series",
    )


def eval_vix_change_max(row, tape, date):
    u = needed_underlyings(row)[0]
    rec = get_underlying(tape, u)
    prior = rec.get("prior_close")
    high = rec.get("high")
    low = rec.get("low")
    if high is None or low is None or prior is None:
        return Verdict("UNEVALUABLE_MISSING", "VIX high/low/prior_close missing")
    params = parse_gate_params(row.get("gate_params", ""))
    try:
        threshold = float(params["threshold_pct"])
    except Exception:
        return Verdict("UNEVALUABLE", "threshold_pct missing or malformed")

    low_change = pct_change(low, prior)
    high_change = pct_change(high, prior)

    if low_change > threshold:
        return Verdict(
            "JUSTIFIED",
            f"VIX low={low} vs prior={prior} gives {low_change}% change, threshold <={threshold}%; never reached",
        )
    if high_change <= threshold:
        return Verdict(
            "SUSPECT",
            f"VIX high={high} vs prior={prior} gives {high_change}% change, threshold <={threshold}%; met all day",
        )
    return Verdict(
        "UNEVALUABLE_INTRADAY",
        f"VIX low={low} -> {low_change}% <= {threshold}% but high={high} -> {high_change}% > {threshold}%; straddles; no intraday VIX series",
    )


def eval_orb_60min(row, tape, date):
    u = needed_underlyings(row)[0]
    rec = get_underlying(tape, u)
    prior = rec.get("prior_close")
    if prior is None:
        return Verdict("UNEVALUABLE_MISSING", f"{u} prior_close missing")
    if not rec.get("series"):
        return Verdict("UNEVALUABLE_MISSING", f"{u} 5-min series missing")

    params = parse_gate_params(row.get("gate_params", ""))
    range_str = params.get("range", "09:30-10:30")
    rs, re, _ = parse_window(range_str)
    orb_bars = select_bars(rec["series"], rs, re, "range")
    if not orb_bars:
        return Verdict("UNEVALUABLE_MISSING_BAR", f"no {u} 5-min bars for ORB range {range_str}")

    highs = [b.get("h") for b in orb_bars if b.get("h") is not None]
    lows = [b.get("l") for b in orb_bars if b.get("l") is not None]
    if not highs or not lows:
        return Verdict("UNEVALUABLE_MISSING", "ORB high/low missing")
    orb_high, orb_low = max(highs), min(lows)

    start, _, _ = parse_window(row.get("entry_window_et", "after 10:30"))
    after_bars = select_bars(rec["series"], start, None, "after")
    if not after_bars:
        return Verdict("UNEVALUABLE_MISSING_BAR", f"no {u} 5-min bars after {row.get('entry_window_et')}")

    for b in after_bars:
        p = b.get("p")
        if p is None:
            continue
        if p > orb_high or p < orb_low:
            return Verdict(
                "SUSPECT",
                f"{u} p={p} at {b['t']} breaks ORB range {orb_low}-{orb_high} (prior_close {prior})",
            )
    return Verdict(
        "JUSTIFIED",
        f"{u} held inside ORB range {orb_low}-{orb_high} after {row.get('entry_window_et')} (prior_close {prior})",
    )
