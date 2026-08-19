#!/usr/bin/env python3
"""Hermetic test: tape.py's Tradier failure modes are SPLIT, never swallowed.

T-11 / wave-1 A3-residue. `scripts/tape.py` already implements the split; what
was missing was a test that BINDS it. `_run_selftest()` in tape.py covers only
`underlyings_on`/GateSymbolError and asserts nothing about `_get()`'s four modes
or about the exit-3 path, so the split could regress silently on the next
rotation. This file is that test. It changes no production code.

Two claims under test:

  1. PRESENT-BUT-REJECTED (HTTP 401/403) is LOUD and NON-RECOVERABLE.
     `build()` exits 3 and writes NO tape. A credential that was presented and
     refused must never be papered over with reconstructed data — that is the
     failure mode that hides a dead feed behind a plausible-looking chart.

  2. ABSENT (no token) and FEED-DOWN (any other HTTP status, network error, or
     unparseable body) are RECOVERABLE. `build()` falls back to
     source="reconstructed" and records WHICH mode caused it in
     `reconstructed_reason`, so the brief can say so out loud.

ORDER IS PART OF THE CONTRACT. The loud check runs before any fallback, so a
rejected token can never be reclassified as feed-down. Test 5 pins that by
asserting no tape file exists after the loud path fires.

No network: urllib.request.urlopen is stubbed in every case.

    python3 scripts/test_tape_failure_modes.py
    python3 scripts/test_tape_failure_modes.py --show-red

--show-red inverts the expectation table and must FAIL. It is the proof that
these assertions bind rather than passing vacuously: every check is required to
flip. A check that still passes against an inverted expectation is reported as
VACUOUS and fails the run in its own right.
"""
import argparse
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tape  # noqa: E402


# ---------------------------------------------------------------- stub plumbing
class _FakeResponse(io.BytesIO):
    """Minimal stand-in for the urlopen context manager."""
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
        return False


@contextlib.contextmanager
def stub_urlopen(behaviour):
    """Patch urllib.request.urlopen. `behaviour` is an exception to raise or
    a bytes body to return."""
    original = urllib.request.urlopen

    def fake(req, timeout=None):
        if isinstance(behaviour, Exception):
            raise behaviour
        return _FakeResponse(behaviour)

    urllib.request.urlopen = fake
    try:
        yield
    finally:
        urllib.request.urlopen = original


def http_error(code):
    return urllib.error.HTTPError(
        url="https://api.tradier.com/v1/markets/history",
        code=code, msg=f"HTTP {code}", hdrs=None, fp=None)


TRADES_HEADER = ("bot,pillar,underlying,role,epoch,trade_id,symbol,structure,status,"
                 "quantity,credit,exit_price,pnl,risk,open_date,close_date,expiration,"
                 "tags,single_sided,short_put,long_put,short_call,long_call,premium,"
                 "underlying_open,underlying_close,mfe_pct,mae_pct,mfe_date,mae_date")

# One SPX position on the test day, plus a prior day so prior_close resolves.
# underlying_open/underlying_close are what the reconstructed path reads.
TRADES_ROWS = [
    "B1,IC,SPX,champion,1,T00001,SPX,shortputspread,closed,1,1.0,0.0,50,955,"
    "2026-08-17 10:00:00,2026-08-17 16:00:00,2026-08-17,,,7500,7495,,,1.0,"
    "7600.0,7610.0,,,,",
    "B1,IC,SPX,champion,1,T00002,SPX,shortputspread,closed,1,1.0,0.0,50,955,"
    "2026-08-18 10:00:00,2026-08-18 16:00:00,2026-08-18,,,7500,7495,,,1.0,"
    "7620.0,7640.0,,,,",
]

GATES = ("bot,pr_id,underlying,entry_window_et,gate_type,gate_params,eval_class,"
         "fill_precondition,source\n"
         "B1,PR-1,SPX,11:00,band_prior_close,abs_lt=0.75,EVALUABLE,,\n")

DAY = "2026-08-18"


@contextlib.contextmanager
def temp_fleet():
    """A throwaway ROOT/data tree so build() never reads or writes the real repo.

    tape.ROOT is redirected too, so load_env() cannot pick up a real .env and
    silently supply a token the test did not set.
    """
    td = tempfile.mkdtemp(prefix="tape-failmode-")
    try:
        data = os.path.join(td, "data")
        os.makedirs(os.path.join(data, "brief"))
        with open(os.path.join(data, "trades.csv"), "w") as f:
            f.write(TRADES_HEADER + "\n" + "\n".join(TRADES_ROWS) + "\n")
        with open(os.path.join(data, "bot_gates.csv"), "w") as f:
            f.write(GATES)
        saved = (tape.ROOT, tape.D, tape.BRIEF)
        tape.ROOT, tape.D = td, data
        tape.BRIEF = os.path.join(data, "brief")
        try:
            yield td
        finally:
            tape.ROOT, tape.D, tape.BRIEF = saved
    finally:
        shutil.rmtree(td, ignore_errors=True)


@contextlib.contextmanager
def env(**kw):
    """Set/clear environment keys for the duration of the block."""
    saved = {k: os.environ.get(k) for k in kw}
    for k, v in kw.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    try:
        yield
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def run_build(day=DAY):
    """build() with stdout/stderr captured. Returns (result, exit_code, stderr).
    exit_code is None when build() returned normally."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            return tape.build(day), None, err.getvalue()
        except SystemExit as e:
            return None, e.code, err.getvalue()


# ------------------------------------------------------------------- the checks
# Each check returns the OBSERVED value; the table below holds what it should be.
# --show-red inverts the table, so every check must flip. That is the point.

def obs_mode(behaviour, token="tok"):
    """The TradierError mode _get() raises for a given transport behaviour."""
    try:
        with stub_urlopen(behaviour):
            tape._get("https://api.tradier.com", "markets/history", {}, token)
    except tape.TradierError as e:
        return e.mode
    return "no-error-raised"


def obs_build_exit(behaviour, token):
    """build()'s exit code (None = returned normally)."""
    with temp_fleet(), env(TRADIER_TOKEN=token, TRADIER_BASE="https://api.tradier.com"):
        with stub_urlopen(behaviour):
            _, code, _ = run_build()
    return code


def obs_build_reason(behaviour, token):
    """reconstructed_reason recorded on the SPX tape when build() falls back."""
    with temp_fleet(), env(TRADIER_TOKEN=token, TRADIER_BASE="https://api.tradier.com"):
        with stub_urlopen(behaviour):
            res, code, _ = run_build()
    if res is None:
        return f"exited-{code}"
    spx = res["underlyings"].get("SPX", {})
    if spx.get("source") != "reconstructed":
        return f"source-{spx.get('source')}"
    return spx.get("reconstructed_reason")


def obs_loud_writes_nothing():
    """After the loud path fires, is the tape file absent? 'absent' | 'WROTE-A-TAPE'"""
    with temp_fleet() as root, env(TRADIER_TOKEN="tok",
                                   TRADIER_BASE="https://api.tradier.com"):
        with stub_urlopen(http_error(401)):
            run_build()
        path = os.path.join(root, "data", "brief", f"{DAY}_tape.json")
        return "WROTE-A-TAPE" if os.path.exists(path) else "absent"


def obs_loud_is_named():
    """Does the loud path name the rejection on stderr? 'named' | 'silent'"""
    with temp_fleet(), env(TRADIER_TOKEN="tok", TRADIER_BASE="https://api.tradier.com"):
        with stub_urlopen(http_error(403)):
            _, _, err = run_build()
    return "named" if "TOKEN REJECTED" in err else "silent"


CHECKS = [
    # (name, callable, expected, wrong)  -- `wrong` is a value that must NOT pass
    ("_get 401 -> token-rejected",
     lambda: obs_mode(http_error(401)), "token-rejected", "feed-down"),
    ("_get 403 -> token-rejected",
     lambda: obs_mode(http_error(403)), "token-rejected", "feed-down"),
    ("_get 500 -> feed-down",
     lambda: obs_mode(http_error(500)), "feed-down", "token-rejected"),
    ("_get network error -> feed-down",
     lambda: obs_mode(urllib.error.URLError("unreachable")), "feed-down", "token-rejected"),
    ("_get bad JSON -> parse-error",
     lambda: obs_mode(b"<html>not json</html>"), "parse-error", "feed-down"),
    ("_get no token -> token-absent",
     lambda: obs_mode(b"{}", token=None), "token-absent", "feed-down"),

    ("build 401 is NON-RECOVERABLE (exit 3)",
     lambda: obs_build_exit(http_error(401), "tok"), 3, None),
    ("build 403 is NON-RECOVERABLE (exit 3)",
     lambda: obs_build_exit(http_error(403), "tok"), 3, None),
    ("build loud path writes NO tape",
     obs_loud_writes_nothing, "absent", "WROTE-A-TAPE"),
    ("build loud path NAMES the rejection",
     obs_loud_is_named, "named", "silent"),

    ("build 500 is RECOVERABLE -> reconstructed/feed-down",
     lambda: obs_build_reason(http_error(500), "tok"), "feed-down", "exited-3"),
    ("build no-token is RECOVERABLE -> reconstructed/token-absent",
     lambda: obs_build_reason(b"{}", None), "token-absent", "exited-3"),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--show-red", action="store_true",
                    help="invert every expectation; the run MUST fail")
    args = ap.parse_args()

    red = args.show_red
    if red:
        print("=== --show-red: expectations INVERTED. This run must FAIL. ===\n")

    failures, vacuous = [], []
    for name, fn, expected, wrong in CHECKS:
        want = wrong if red else expected
        try:
            got = fn()
        except Exception as e:                      # a check that blows up is a failure
            got = f"RAISED {type(e).__name__}: {e}"
        ok = (got == want)
        if red:
            # Under inversion, passing means the check does not bind.
            if ok:
                vacuous.append(f"{name}: passed against the WRONG value {want!r} — VACUOUS")
                print(f"  VACUOUS  {name}: got {got!r}, wrong-value {want!r}")
            else:
                print(f"  flipped  {name}: got {got!r} != wrong-value {want!r}")
        else:
            if ok:
                print(f"  ok       {name}")
            else:
                failures.append(f"{name}: expected {want!r}, got {got!r}")
                print(f"  FAIL     {name}: expected {want!r}, got {got!r}")

    print()
    if red:
        if vacuous:
            print(f"SHOW-RED INCONCLUSIVE — {len(vacuous)} check(s) did not bind:",
                  file=sys.stderr)
            for v in vacuous:
                print(f"  - {v}", file=sys.stderr)
            return 1
        print(f"SHOW-RED OK — all {len(CHECKS)} checks flipped and the run failed "
              "as required. The assertions bind.")
        return 1                                    # red means red: non-zero exit
    if failures:
        print(f"test_tape_failure_modes: FAIL ({len(failures)}/{len(CHECKS)})",
              file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(f"test_tape_failure_modes: OK ({len(CHECKS)}/{len(CHECKS)}) — "
          "present-but-rejected is loud and non-recoverable; absent and feed-down "
          "fall back with the reason recorded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
