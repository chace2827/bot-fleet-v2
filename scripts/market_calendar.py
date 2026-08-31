#!/usr/bin/env python3
"""market_calendar.py — the single source of US-equity trading-day truth.

Derived holidays (NYSE-style, full-day closures only):
  - New Year's Day       Jan 1   (observed Fri if Sat, Mon if Sun)
  - Martin Luther King   3rd Monday of January
  - Presidents' Day      3rd Monday of February
  - Good Friday          Friday before Easter Sunday (Anonymous algorithm)
  - Memorial Day         last Monday of May
  - Juneteenth           Jun 19  (observed Fri if Sat, Mon if Sun)
  - Independence Day     Jul 4   (observed Fri if Sat, Mon if Sun)
  - Labor Day            1st Monday of September
  - Thanksgiving         4th Thursday of November
  - Christmas Day        Dec 25  (observed Fri if Sat, Mon if Sun)

No hardcoded per-year lists.  The rules produce correct answers for any
Gregorian year.  Early closes (e.g. Black Friday) are intentionally NOT
modelled — only full trading-day closures.
"""
import argparse
import datetime
import functools
import sys


# ---------------------------------------------------------------------------
# Holiday derivation
# ---------------------------------------------------------------------------
def _easter_sunday(year):
    """Compute Easter Sunday for a Gregorian year using the Anonymous algorithm."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime.date(year, month, day)


def _observed_weekday(d):
    """Return the observed closure for a fixed-date holiday.

    Saturday -> preceding Friday, Sunday -> following Monday, weekday -> itself.
    """
    wd = d.weekday()
    if wd == 5:      # Saturday
        return d - datetime.timedelta(days=1)
    if wd == 6:      # Sunday
        return d + datetime.timedelta(days=1)
    return d


def _nth_weekday_of_month(year, month, weekday, n):
    """Return the nth occurrence of `weekday` (0=Monday) in `month`."""
    d = datetime.date(year, month, 1)
    count = 0
    while d.month == month:
        if d.weekday() == weekday:
            count += 1
            if count == n:
                return d
        d += datetime.timedelta(days=1)
    raise ValueError(f"no {n}th weekday {weekday} in {year}-{month:02d}")


def _last_weekday_of_month(year, month, weekday):
    """Return the last occurrence of `weekday` in `month`."""
    if month == 12:
        d = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
    else:
        d = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
    while d.weekday() != weekday:
        d -= datetime.timedelta(days=1)
    return d


@functools.lru_cache(maxsize=None)
def holidays_for_year(year):
    """Return the set of market-closure dates for `year` (observed, not raw)."""
    h = {
        # Fixed-date holidays with weekend observation.
        _observed_weekday(datetime.date(year, 1, 1)),   # New Year's Day
        _observed_weekday(datetime.date(year, 6, 19)),  # Juneteenth
        _observed_weekday(datetime.date(year, 7, 4)),   # Independence Day
        _observed_weekday(datetime.date(year, 12, 25)), # Christmas Day

        # Floating / rule-based holidays.
        _nth_weekday_of_month(year, 1, 0, 3),   # MLK Day: 3rd Monday of Jan
        _nth_weekday_of_month(year, 2, 0, 3),   # Presidents' Day: 3rd Monday of Feb
        _easter_sunday(year) - datetime.timedelta(days=2),  # Good Friday
        _last_weekday_of_month(year, 5, 0),     # Memorial Day: last Monday of May
        _nth_weekday_of_month(year, 9, 0, 1),   # Labor Day: 1st Monday of Sep
        _nth_weekday_of_month(year, 11, 3, 4),  # Thanksgiving: 4th Thursday of Nov
    }

    # New Year's observation can shift to the previous calendar year (Dec 31).
    # Include it in the year it actually falls in so is_trading_day() is correct.
    ny_next = _observed_weekday(datetime.date(year + 1, 1, 1))
    if ny_next.year == year:
        h.add(ny_next)

    return h


# ---------------------------------------------------------------------------
# Trading-day primitives
# ---------------------------------------------------------------------------
def _to_date(x):
    if isinstance(x, datetime.datetime):
        return x.date()
    if isinstance(x, datetime.date):
        return x
    if isinstance(x, str):
        return datetime.date.fromisoformat(x)
    raise TypeError(f"expected date, datetime, or ISO string, got {type(x).__name__}")


def is_trading_day(d):
    """Return True if `d` is a US equity trading day (Mon-Fri, not a holiday)."""
    d = _to_date(d)
    if d.weekday() >= 5:
        return False
    return d not in holidays_for_year(d.year)


def add_trading_days(d, n):
    """Add `n` trading days to date `d`; `n` may be negative or zero."""
    d = _to_date(d)
    step = 1 if n >= 0 else -1
    count = 0
    while count < abs(n):
        d += datetime.timedelta(days=step)
        if is_trading_day(d):
            count += 1
    return d


def count_trading_days(start, end):
    """Count trading days in [start, end] inclusive."""
    start = _to_date(start)
    end = _to_date(end)
    n = 0
    d = start
    while d <= end:
        if is_trading_day(d):
            n += 1
        d += datetime.timedelta(days=1)
    return n


def previous_trading_day(day):
    """Return the last trading day strictly before `day`.

    Accepts and returns an ISO date string (the contract used by
    check_heartbeat.py).  If a date object is supplied a date object is returned.
    """
    d = _to_date(day)
    d -= datetime.timedelta(days=1)
    while not is_trading_day(d):
        d -= datetime.timedelta(days=1)
    if isinstance(day, str):
        return d.isoformat()
    return d


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
def selftest():
    """Run the --selftest suite and exit non-zero on any failure."""
    checks = []

    def check(name, got, want):
        ok = got == want
        checks.append((ok, name, got, want))
        return ok

    # Labor Day 2026-09-07 is a holiday; normal Monday 2026-09-14 is not.
    check("Labor Day 2026-09-07 is a holiday",
          is_trading_day("2026-09-07"), False)
    check("normal Monday 2026-09-14 is a trading day",
          is_trading_day("2026-09-14"), True)

    # July 4 2026 falls on Saturday -> observed Friday 2026-07-03.
    check("July 4 2026 is a Saturday (not a trading day)",
          datetime.date(2026, 7, 4).weekday(), 5)
    check("observed Independence Day 2026-07-03 is a holiday",
          is_trading_day("2026-07-03"), False)
    check("July 3 2025 (ordinary Thursday) is a trading day",
          is_trading_day("2025-07-03"), True)

    # Thanksgiving 2026-11-26.
    check("Thanksgiving 2026-11-26 is a holiday",
          is_trading_day("2026-11-26"), False)

    # Good Friday 2026-04-03.
    check("Good Friday 2026-04-03 is a holiday",
          is_trading_day("2026-04-03"), False)

    # Weekend day.
    check("Saturday 2026-09-05 is not a trading day",
          is_trading_day("2026-09-05"), False)
    check("Sunday 2026-09-06 is not a trading day",
          is_trading_day("2026-09-06"), False)

    # Derivation (not list) sanity: ensure we do not carry hardcoded 2026 strings.
    # Pick a non-2026 year and verify derived holidays land on expected weekdays.
    check("Labor Day 2030-09-02 is the 1st Monday",
          _nth_weekday_of_month(2030, 9, 0, 1),
          datetime.date(2030, 9, 2))
    check("Thanksgiving 2030-11-28 is the 4th Thursday",
          _nth_weekday_of_month(2030, 11, 3, 4),
          datetime.date(2030, 11, 28))
    check("Memorial Day 2030-05-27 is the last Monday",
          _last_weekday_of_month(2030, 5, 0),
          datetime.date(2030, 5, 27))

    # Cross-year New Year's observation: 2027-01-01 is Friday, so observed on
    # the day itself.  2022-01-01 was Saturday -> observed 2021-12-31.
    check("New Year's 2022 observed on 2021-12-31 (Saturday shift)",
          is_trading_day("2021-12-31"), False)
    check("2022-01-01 itself is a Saturday (not a trading day)",
          is_trading_day("2022-01-01"), False)
    check("2022-01-03 (Monday after New Year's weekend) is a trading day",
          is_trading_day("2022-01-03"), True)

    # add_trading_days / count_trading_days invariants.
    check("80 trading days from 2026-08-14 lands on 2026-12-08",
          add_trading_days("2026-08-14", 80),
          datetime.date(2026, 12, 8))
    check("20 trading days in the window 2026-07-20 .. 2026-08-14",
          count_trading_days("2026-07-20", "2026-08-14"), 20)

    fails = sum(1 for ok, *_ in checks if not ok)
    print("market_calendar.py selftest")
    print("=" * 74)
    for ok, name, got, want in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
        if not ok:
            print(f"        got  {got!r}\n        want {want!r}")
    print("-" * 74)
    print(f"{len(checks) - fails}/{len(checks)} passed")
    return 0 if fails == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--selftest", action="store_true",
                    help="run the rule-derived holiday selftest")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())

    # Default: run selftest so CI can call the script without flags if desired.
    sys.exit(selftest())


if __name__ == "__main__":
    main()
