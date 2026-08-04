#!/usr/bin/env python3
"""Build data/mirror_baseline.csv — the PRE-CUTOVER anchor for the OA-Mirror pillar.

Contract (CLAUDE.md §3, docs/build-plan.md):
  * Written FROM THE EXPORT, never from the archived v1 ledger and never from memory.
  * Written ONCE. It is an anchor, not a metric — recomputing it later against a
    different export would silently move the baseline every comparison is measured
    against. Refuses to overwrite unless --force is passed explicitly.
  * Every row cites its capture file and that file's sha256.

R convention (CLAUDE.md §4): R = pnl / risk, per position. Positions whose risk is
absent or <= 0 CANNOT yield an R and are EXCLUDED from the R columns but still
counted in n_positions — the exclusion is reported per bot, never silently dropped.

NOTE ON AGGREGATION: the condor roll-up (risk = larger side) is defined for iron
condors and is NOT applied here. The mirror pillar is heterogeneous — long calls,
broken-wing flies, ORB breakouts — and there is no single correct multi-leg roll-up
across them. These are per-POSITION statistics and the unit column says so.
"""
import argparse, csv, hashlib, json, os, statistics, sys, datetime

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()

def num(x):
    try:
        v = float(x)
        return v
    except (TypeError, ValueError):
        return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", default="data/captures/oa_export_positions_2026-07-30.csv")
    ap.add_argument("--meta", default="data/bots_meta.csv")
    ap.add_argument("--out", default="data/mirror_baseline.csv")
    ap.add_argument("--receipt", default="data/receipts/mirror-baseline.txt")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    if os.path.exists(a.out) and not a.force:
        sys.exit(f"REFUSING: {a.out} already exists. It is written ONCE and never "
                 f"recomputed (see module docstring). Pass --force only if you have "
                 f"decided deliberately to move the baseline.")
    for p in (a.export, a.meta):
        if not os.path.exists(p):
            sys.exit(f"ERROR: missing input {p}")

    cap_hash = sha256(a.export)
    cap_name = os.path.basename(a.export)

    mirrors = {r["bot"]: r for r in csv.DictReader(open(a.meta))
               if r.get("pillar") == "OA-Mirror"}
    if not mirrors:
        sys.exit("ERROR: no OA-Mirror rows in bots_meta.csv — wrong pillar label?")

    rows = [r for r in csv.DictReader(open(a.export)) if r["botName"] in mirrors]

    by = {}
    for r in rows:
        by.setdefault(r["botName"], []).append(r)

    out, report = [], []
    for bot in sorted(mirrors):
        pos = by.get(bot, [])
        n = len(pos)
        Rs, excluded, pnls, dates = [], 0, [], []
        for p in pos:
            pnl, risk = num(p.get("pnl")), num(p.get("risk"))
            if pnl is not None:
                pnls.append(pnl)
            if p.get("closeDate"):
                dates.append(p["closeDate"][:10])
            if pnl is None or risk is None or risk <= 0:
                excluded += 1
            else:
                Rs.append(pnl / risk)
        wins = sum(1 for v in pnls if v > 0)
        out.append({
            "bot": bot,
            "pillar": "OA-Mirror",
            "status_at_capture": mirrors[bot].get("status", ""),
            "unit": "position",
            "n_positions": n,
            "n_with_R": len(Rs),
            "n_excluded_no_risk": excluded,
            "first_close": min(dates) if dates else "",
            "last_close": max(dates) if dates else "",
            "sum_pnl": round(sum(pnls), 2) if pnls else "",
            "mean_R": round(statistics.mean(Rs), 4) if Rs else "",
            "median_R": round(statistics.median(Rs), 4) if Rs else "",
            "win_rate": round(wins / len(pnls), 4) if pnls else "",
            "epoch_boundary": mirrors[bot].get("epoch_boundary", ""),
            "capture_file": cap_name,
            "capture_sha256": cap_hash,
        })
        if excluded:
            report.append(f"  {bot}: {excluded}/{n} positions excluded from R (risk absent or <= 0)")

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    lines = [
        "MIRROR BASELINE — pre-cutover anchor",
        f"built            : {datetime.datetime.now().isoformat(timespec='seconds')}",
        f"export           : {cap_name}",
        f"export sha256    : {cap_hash}",
        f"meta             : {os.path.basename(a.meta)}",
        f"mirrors          : {len(out)}",
        f"positions        : {sum(r['n_positions'] for r in out)}",
        f"with R           : {sum(r['n_with_R'] for r in out)}",
        f"excluded (no risk): {sum(r['n_excluded_no_risk'] for r in out)}",
        f"out              : {a.out}",
        f"out sha256       : (computed below)",
    ]
    if report:
        lines.append("EXCLUSIONS:")
        lines += report
    else:
        lines.append("EXCLUSIONS: none")
    lines.append("")
    lines.append("This file is an ANCHOR. Do not recompute it against a later export.")
    os.makedirs(os.path.dirname(a.receipt), exist_ok=True)
    txt = "\n".join(lines).replace("(computed below)", sha256(a.out))
    open(a.receipt, "w").write(txt + "\n")
    print(txt)

if __name__ == "__main__":
    main()
