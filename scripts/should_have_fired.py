#!/usr/bin/env python3
"""should_have_fired.py — per-ON-bot gate evaluation report.

For each tape day in data/brief/ and each ON bot with zero fills that day,
reads the SIGNED gate from data/bot_gates.csv, evaluates it against the tape,
and emits JUSTIFIED / SUSPECT / UNEVALUABLE_<class>.

Output: p3_verdicts.tsv at the repo root, sorted by date then bot.

The unsigned-bot banner for PR-02 / PR-04 is printed in the run summary per
R-2026-08-11-PR-02-PR-04-STAY-ON.
"""

import argparse
import csv
import json
import os
import re
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(__file__))

import gate_parser as gp

DATA_META = os.path.join("data", "bots_meta.csv")
DATA_GATES = os.path.join("data", "bot_gates.csv")
DATA_TRADES = os.path.join("data", "trades.csv")
DATA_BRIEF = os.path.join("data", "brief")
OUTPUT_FILE = "p3_verdicts.tsv"


def load_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def load_on_bots(path):
    return {r["bot"]: r for r in load_csv(path) if r.get("status", "").upper() == "ON"}


def load_fills(path):
    """Return set of (bot, open_date_ymd) with at least one row."""
    fills = set()
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            bot = r.get("bot", "")
            od = (r.get("open_date") or "")[:10]
            if bot and od:
                fills.add((bot, od))
    return fills


def load_tape(path):
    with open(path) as f:
        return json.load(f)


def find_tapes(brief_dir):
    tapes = []
    for fn in sorted(os.listdir(brief_dir)):
        m = re.match(r"^(\d{4}-\d{2}-\d{2})_tape\.json$", fn)
        if m:
            tapes.append((m.group(1), os.path.join(brief_dir, fn)))
    return sorted(tapes)


def write_tsv(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["date", "bot", "pr_id", "verdict", "reason"])
        for r in rows:
            w.writerow([r["date"], r["bot"], r["pr_id"], r["verdict"], r["reason"]])


def build_report(data_dir, output_path, quiet=False):
    """Core report builder.  data_dir is the repo/scratch root."""
    brief_dir = os.path.join(data_dir, DATA_BRIEF)
    meta = load_on_bots(os.path.join(data_dir, DATA_META))
    gates = gp.load_bot_gates(os.path.join(data_dir, DATA_GATES))
    gates_by_bot = {r["bot"]: r for r in gates}
    fills = load_fills(os.path.join(data_dir, DATA_TRADES))
    tapes = find_tapes(brief_dir)

    rows = []
    filled = []
    for date, tape_path in tapes:
        tape = load_tape(tape_path)
        for bot in sorted(meta):
            if (bot, date) in fills:
                filled.append((date, bot))
                continue
            gate = gates_by_bot.get(bot)
            if gate is None:
                verdict = "UNEVALUABLE_MISSING_GATE"
                reason = f"no gate row in data/bot_gates.csv for {bot}"
                pr_id = ""
            else:
                pr_id = gate.get("pr_id", "")
                v = gp.evaluate_gate(gate, tape, date)
                verdict = v.verdict
                reason = v.reason
            rows.append({
                "date": date,
                "bot": bot,
                "pr_id": pr_id,
                "verdict": verdict,
                "reason": reason,
            })

    rows.sort(key=lambda r: (r["date"], r["bot"]))
    write_tsv(rows, output_path)
    if not quiet:
        print_summary(rows, filled)
        print(f"\nWrote {output_path}: {os.path.abspath(output_path)}")
    return rows


def print_summary(rows, filled):
    print("\n*** R-2026-08-11-PR-02-PR-04-STAY-ON: PR-02 and PR-04 are ON and "
          "unsigned; their verdicts are produced under a knowing exception. ***\n")
    by_date = {}
    for r in rows:
        by_date.setdefault(r["date"], []).append(r)
    for d in sorted(by_date):
        rr = by_date[d]
        n_j = sum(1 for r in rr if r["verdict"] == "JUSTIFIED")
        n_s = sum(1 for r in rr if r["verdict"] == "SUSPECT")
        n_u = len(rr) - n_j - n_s
        print(f"{d}: {len(rr)} bots judged ({n_j} JUSTIFIED, {n_s} SUSPECT, {n_u} UNEVALUABLE)")
    print(f"\nExcluded {len(filled)} filled (date,bot) pairs from report.")
    for d, b in sorted(filled):
        print(f"  filled: {d} {b}")


# -----------------------------------------------------------------------------
# Self-test fixtures
# -----------------------------------------------------------------------------

def _write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(text)


def _tape(date, underlyings, any_reconstructed=False, reconstructed_reasons=None):
    return {
        "date": date,
        "generated": f"{date}T00:00:00",
        "any_reconstructed": any_reconstructed,
        "reconstructed_reasons": reconstructed_reasons or [],
        "underlyings": underlyings,
        "divergence": None,
    }


def _run_selftest():
    scratch = tempfile.mkdtemp(prefix="p3-shf-selftest-")
    try:
        data = os.path.join(scratch, "data")
        os.makedirs(os.path.join(data, "brief"))

        # bots_meta.csv
        bots = [
            "bot,pillar,role,underlying,status,champion,epoch_boundary,hedge,strike_fix,superseded,focus,notes,ops_class",
            "BandJust,IC,test,SPX,ON,,,,,,,,",
            "BandSus,IC,test,SPX,ON,,,,,,,,",
            "BandStrictSus,IC,test,QQQ,ON,,,,,,,,",
            "VixMinJust,Directional,test,VIX,ON,,,,,,,,",
            "VixMinSus,Directional,test,VIX,ON,,,,,,,,",
            "VixMinStraddle,Directional,test,VIX,ON,,,,,,,,",
            "VixChangeJust,Directional,test,VIX,ON,,,,,,,,",
            "VixChangeSus,Directional,test,VIX,ON,,,,,,,,",
            "VixChangeStraddle,Directional,test,VIX,ON,,,,,,,,",
            "VixMissingBar,Directional,test,VIX,ON,,,,,,,,",
            "WeekdayJust,OA-Mirror,test,,ON,,,,,,,,",
            "WeekdaySus,OA-Mirror,test,,ON,,,,,,,,",
            "OrbSus,OA-Mirror,test,SPX,ON,,,,,,,,",
            "NoneSus,IC,test,SPX,ON,,,,,,,,",
            "Floor,IC,test,QQQ,ON,,,,,,,,",
            "Unknown,OA-Mirror,test,,ON,,,,,,,,",
            "SourceBad,IC,test,SPX,ON,,,,,,,,",
            "MissingData,IC,test,SPX,ON,,,,,,,,",
            "MissingBar,IC,test,SPX,ON,,,,,,,,",
            "NoGate,IC,test,SPX,ON,,,,,,,,",
        ]
        _write(os.path.join(data, "bots_meta.csv"), "\n".join(bots))

        # bot_gates.csv
        gates = [
            "bot,pr_id,underlying,entry_window_et,gate_type,gate_params,eval_class,fill_precondition,source",
            "BandJust,PR-BandJust,SPX,11:00,band_prior_close,abs_lt=0.25,EVALUABLE,,",
            "BandSus,PR-BandSus,SPX,11:00,band_prior_close,abs_lt=0.75,EVALUABLE,,",
            'BandStrictSus,PR-BandStrictSus,QQQ,13:30-14:00,band_prior_close_strict,"gt=-0.75,lt=0.75,per_side_not_opened=true",EVALUABLE,,',
            "VixMinJust,PR-VixMinJust,VIX,11:00,vix_min,threshold=100,EVALUABLE_ASYM,,",
            "VixMinSus,PR-VixMinSus,VIX,11:00,vix_min,threshold=10,EVALUABLE_ASYM,,",
            "VixMinStraddle,PR-VixMinStraddle,VIX,11:00,vix_min,threshold=14.5,EVALUABLE_ASYM,,",
            "VixChangeJust,PR-VixChangeJust,VIX,11:00,vix_change_max,threshold_pct=-35,EVALUABLE_ASYM,,",
            "VixChangeSus,PR-VixChangeSus,VIX,11:00,vix_change_max,threshold_pct=-2,EVALUABLE_ASYM,,",
            "VixChangeStraddle,PR-VixChangeStraddle,VIX,11:00,vix_change_max,threshold_pct=-27,EVALUABLE_ASYM,,",
            "VixMissingBar,PR-VixMissingBar,VIX,12:00,vix_min,threshold=100,EVALUABLE_ASYM,,",
            "WeekdayJust,PR-WeekdayJust,,Friday,weekday,day=Mon,EVALUABLE,,",
            "WeekdaySus,PR-WeekdaySus,,Friday,weekday,day=Fri,EVALUABLE,,",
            "OrbSus,PR-OrbSus,SPX,after 10:30,orb_60min,range=09:30-10:30,EVALUABLE,,",
            "NoneSus,PR-NoneSus,SPX,11:00,none,,SUSPECT_WHEN_SILENT,,",
            "Floor,PR-Floor,QQQ,daily,none,,UNEVALUABLE_FLOOR,declared credit floor (exact value unrecorded),",
            "Unknown,PR-Unknown,,,unknown,,UNEVALUABLE_BY_DESIGN,,",
            "SourceBad,PR-SourceBad,SPX,11:00,band_prior_close,abs_lt=0.75,EVALUABLE,,",
            "MissingData,PR-MissingData,SPX,11:00,band_prior_close,abs_lt=0.75,EVALUABLE,,",
            "MissingBar,PR-MissingBar,SPX,15:00,band_prior_close,abs_lt=0.75,EVALUABLE,,",
        ]
        _write(os.path.join(data, "bot_gates.csv"), "\n".join(gates))

        # trades.csv — fill WeekdaySus so it is excluded; leave others zero-fill.
        trades = [
            "bot,pillar,underlying,role,epoch,trade_id,symbol,structure,status,quantity,credit,exit_price,pnl,risk,open_date,close_date,expiration,tags,single_sided,short_put,long_put,short_call,long_call,premium,underlying_open,underlying_close,mfe_pct,mae_pct,mfe_date,mae_date",
            "WeekdaySus,IC,SPX,test,baseline,T90001,SPX,shortputspread,closed,1,0.1,0.1,0,100,2026-08-14,2026-08-14 12:00,2026-08-14 16:00,,True,100,99,,,-1,100,100,0,0,2026-08-14 12:00,2026-08-14 10:00",
        ]
        _write(os.path.join(data, "trades.csv"), "\n".join(trades))

        # 2026-08-14 tape — fully tradier, covers SUSPECT cases and most JUSTIFIED cases.
        spx_series = [
            {"t": "09:30", "p": 1000.0, "h": 1002.0, "l": 999.0},
            {"t": "10:30", "p": 1001.0, "h": 1002.0, "l": 1000.0},
            {"t": "10:35", "p": 1003.0, "h": 1004.0, "l": 1002.0},
            {"t": "11:00", "p": 1005.0, "h": 1006.0, "l": 1004.0},
            {"t": "13:30", "p": 1002.0, "h": 1003.0, "l": 1001.0},
            {"t": "13:35", "p": 1002.5, "h": 1003.5, "l": 1001.5},
            {"t": "13:55", "p": 1002.5, "h": 1003.0, "l": 1002.0},
            {"t": "14:00", "p": 1003.0, "h": 1004.0, "l": 1002.5},
        ]
        qqq_series = [
            {"t": "13:30", "p": 401.0, "h": 401.5, "l": 400.5},
            {"t": "13:35", "p": 401.2, "h": 401.8, "l": 400.8},
            {"t": "13:55", "p": 401.1, "h": 401.5, "l": 400.9},
            {"t": "14:00", "p": 401.5, "h": 402.0, "l": 401.0},
        ]
        tape14 = _tape("2026-08-14", {
            "SPX": {
                "symbol": "SPX", "source": "tradier", "prior_close": 1000.0,
                "open": 1000.0, "high": 1006.0, "low": 999.0, "close": 1003.0,
                "series": spx_series, "series_interval": "5min",
            },
            "QQQ": {
                "symbol": "QQQ", "source": "tradier", "prior_close": 400.0,
                "open": 400.0, "high": 402.0, "low": 400.0, "close": 401.5,
                "series": qqq_series, "series_interval": "5min",
            },
            "VIX": {
                "symbol": "VIX", "source": "tradier", "prior_close": 20.0,
                "open": 20.0, "high": 15.0, "low": 14.0, "close": 14.5,
                "series": [{"t": "11:00", "p": 14.5, "h": 15.0, "l": 14.0}],
                "series_interval": "5min",
                "vix_close": 14.5, "vix_change_pct": -27.5,
            },
        })
        _write(os.path.join(data, "brief", "2026-08-14_tape.json"),
               json.dumps(tape14, indent=2))

        # 2026-08-10 tape — reconstructed SPX (source rule), plus a VIX straddle and a missing QQQ.
        tape10 = _tape("2026-08-10", {
            "SPX": {
                "symbol": "SPX", "source": "reconstructed", "prior_close": None,
                "open": 1000.0, "high": 1000.0, "low": 998.0, "close": 998.0,
                "series": [], "series_interval": None,
                "pct_move": -0.2, "gap_pct": None, "full_pct": None,
                "range_pct": None, "net_pct": -0.2,
            },
            "VIX": {
                "symbol": "VIX", "source": "tradier", "prior_close": 20.0,
                "open": 20.0, "high": 21.0, "low": 18.0, "close": 19.0,
                "series": [{"t": "11:00", "p": 19.0, "h": 21.0, "l": 18.0}],
                "series_interval": "5min",
                "vix_close": 19.0, "vix_change_pct": -5.0,
            },
        }, any_reconstructed=True, reconstructed_reasons=["token-absent"])
        _write(os.path.join(data, "brief", "2026-08-10_tape.json"),
               json.dumps(tape10, indent=2))

        # 2026-08-08 tape — empty underlyings.
        tape08 = _tape("2026-08-08", {}, any_reconstructed=False)
        _write(os.path.join(data, "brief", "2026-08-08_tape.json"),
               json.dumps(tape08, indent=2))

        output = os.path.join(scratch, "verdicts.tsv")
        rows = build_report(scratch, output, quiet=True)

        # Build lookup and assert one example per verdict class.
        by_key = {(r["date"], r["bot"]): r["verdict"] for r in rows}

        def check(date, bot, expected):
            got = by_key.get((date, bot))
            if got != expected:
                print(f"SELFTEST FAIL: {date} {bot} expected {expected}, got {got}", file=sys.stderr)
                return False
            return True

        ok = True
        ok &= check("2026-08-14", "BandJust", "JUSTIFIED")
        ok &= check("2026-08-14", "BandSus", "SUSPECT")
        ok &= check("2026-08-14", "BandStrictSus", "SUSPECT")
        ok &= check("2026-08-14", "VixMinJust", "JUSTIFIED")
        ok &= check("2026-08-14", "VixMinSus", "SUSPECT")
        ok &= check("2026-08-14", "VixMinStraddle", "UNEVALUABLE_INTRADAY")
        ok &= check("2026-08-14", "VixChangeJust", "JUSTIFIED")
        ok &= check("2026-08-14", "VixChangeSus", "SUSPECT")
        ok &= check("2026-08-14", "VixChangeStraddle", "UNEVALUABLE_INTRADAY")
        ok &= check("2026-08-14", "VixMissingBar", "UNEVALUABLE_MISSING_BAR")
        ok &= check("2026-08-14", "WeekdayJust", "JUSTIFIED")
        # WeekdaySus excluded because it filled.
        ok &= check("2026-08-14", "OrbSus", "SUSPECT")
        ok &= check("2026-08-14", "NoneSus", "SUSPECT")
        ok &= check("2026-08-14", "Floor", "UNEVALUABLE_FLOOR")
        ok &= check("2026-08-14", "Unknown", "UNEVALUABLE_BY_DESIGN")
        ok &= check("2026-08-10", "SourceBad", "UNEVALUABLE_SOURCE")
        ok &= check("2026-08-08", "MissingData", "UNEVALUABLE_MISSING")
        ok &= check("2026-08-14", "MissingBar", "UNEVALUABLE_MISSING_BAR")
        ok &= check("2026-08-08", "NoGate", "UNEVALUABLE_MISSING_GATE")

        if not ok:
            print("\nSELFTEST produced:")
            for r in rows:
                print(f"  {r['date']}\t{r['bot']}\t{r['verdict']}\t{r['reason']}")
            sys.exit(1)

        print("SELFTEST PASSED")
        return 0
    finally:
        shutil.rmtree(scratch)


def main():
    parser = argparse.ArgumentParser(description="Should-Have-Fired gate report")
    parser.add_argument("--selftest", action="store_true",
                        help="run hermetic self-test in a temp scratch root")
    parser.add_argument("--data-dir", default=ROOT,
                        help="root containing data/ (defaults to repo root)")
    parser.add_argument("--output", default=os.path.join(ROOT, OUTPUT_FILE),
                        help="output TSV path")
    args = parser.parse_args()

    if args.selftest:
        return _run_selftest()

    build_report(args.data_dir, args.output, quiet=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
