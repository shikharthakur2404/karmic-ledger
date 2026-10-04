"""
karmic-ledger: Vimshottari Dasha Engine
Computes 120-year planetary dasha cycles and granular sub-periods down to exact calendar days.

Year length is fixed at 365.25 days (study KL-N30-001 / engine freeze). Civil 365/366
day-of-year scaling is intentionally not used.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta
from typing import Any

# Vimshottari Dasha sequence and year durations
DASHA_ORDER: list[tuple[str, float]] = [
    ("Ketu", 7.0),
    ("Venus", 20.0),
    ("Sun", 6.0),
    ("Moon", 10.0),
    ("Mars", 7.0),
    ("Rahu", 18.0),
    ("Jupiter", 16.0),
    ("Saturn", 19.0),
    ("Mercury", 17.0),
]

TOTAL_DASHA_CYCLE: float = 120.0
DASHA_MAP: dict[str, float] = dict(DASHA_ORDER)

# Fixed Vimshottari year (days). Alternative 360.0 reserved for sensitivity analyses.
DASHA_YEAR_DAYS: float = 365.25

# Mean lunar motion — fallback only when natal Moon speed is unavailable.
# Prefer natal["planets"]["Moon"]["speed_deg_per_hour"] (ephemeris at birth).
MEAN_MOON_DEG_PER_HOUR: float = 0.55
NAKSHATRA_SPAN_DEG: float = 360.0 / 27.0

# Registered AA birth-time uncertainty (minutes). Single source of truth.
AA_UNCERTAINTY_MINUTES: float = 2.0

# Window half-width uses math.ceil on the continuous day estimate (registered rounding).
WINDOW_ROUNDING: str = "ceil"

_DECIMAL_ANCHOR = datetime(1, 1, 1)


def years_to_timedelta(years: float, year_days: float = DASHA_YEAR_DAYS) -> timedelta:
    """Convert Vimshottari years to a timedelta using a fixed-length year."""
    return timedelta(days=years * year_days)


def datetime_to_fixed_year_decimal(
    dt: datetime, year_days: float = DASHA_YEAR_DAYS
) -> float:
    """
    Map a datetime onto a continuous year measure with fixed-length years.
    Used for interval comparisons inside timelines (not civil calendar years).
    """
    return (dt - _DECIMAL_ANCHOR).total_seconds() / (86400.0 * year_days)


def decimal_year_to_date(decimal_year: float) -> str:
    """
    Backward-compatible helper: interpret decimal_year under fixed 365.25-day years
    from the same anchor used by datetime_to_fixed_year_decimal.
    """
    dt = _DECIMAL_ANCHOR + years_to_timedelta(decimal_year)
    return dt.strftime("%Y-%m-%d")


def dasha_boundary_shift_days_per_minute(
    birth_moon_nakshatra_lord: str,
    year_days: float = DASHA_YEAR_DAYS,
    moon_deg_per_hour: float | None = None,
) -> float:
    """
    Days of Vimshottari boundary shift per minute of birth-time error.

    Uses the lord of the Moon's nakshatra **at birth** (the balance lord that
    starts the Vimshottari sequence). Every later Mahadasha/Antardasha boundary
    shifts by the same amount; do **not** pass the dasha lord active at an event.

    moon_deg_per_hour: natal Moon speed from the ephemeris when available;
    defaults to MEAN_MOON_DEG_PER_HOUR (0.55) for documentation/tests only.
    """
    lord_key = birth_moon_nakshatra_lord.strip().title()
    if lord_key not in DASHA_MAP:
        raise ValueError(f"Unknown Nakshatra Lord: {birth_moon_nakshatra_lord}")
    speed = (
        MEAN_MOON_DEG_PER_HOUR
        if moon_deg_per_hour is None
        else abs(float(moon_deg_per_hour))
    )
    moon_deg_per_min = speed / 60.0
    return DASHA_MAP[lord_key] * year_days * (moon_deg_per_min / NAKSHATRA_SPAN_DEG)


def event_window_half_width_days(
    birth_moon_nakshatra_lord: str,
    aa_uncertainty_min: float | None = None,
    year_days: float = DASHA_YEAR_DAYS,
    moon_deg_per_hour: float | None = None,
) -> int:
    """
    Per-subject event window half-width (days) for KL-N30-001.

    Continuous estimate is rounded with math.ceil (WINDOW_ROUNDING='ceil'):
    values just above an integer (e.g. Sun 3.01) advance a full day. That is a
    registered artifact of the constant/speed, not a free parameter.

    birth_moon_nakshatra_lord: Moon nakshatra lord at birth only.
    """
    if aa_uncertainty_min is None:
        aa_uncertainty_min = AA_UNCERTAINTY_MINUTES
    shift = dasha_boundary_shift_days_per_minute(
        birth_moon_nakshatra_lord,
        year_days=year_days,
        moon_deg_per_hour=moon_deg_per_hour,
    )
    return max(1, int(math.ceil(aa_uncertainty_min * shift)))


def event_window_half_width_from_natal(natal: dict[str, Any]) -> int:
    """
    Study window from natal chart only (no event dates).

    Propagates AA uncertainty using the birth Moon nakshatra lord and the
    ephemeris Moon speed at birth.
    """
    moon = natal["planets"]["Moon"]
    return event_window_half_width_days(
        birth_moon_nakshatra_lord=moon["nakshatra"]["lord"],
        moon_deg_per_hour=float(moon["speed_deg_per_hour"]),
    )


def compute_vimshottari_timeline(
    birth_dt: datetime,
    moon_nakshatra_lord: str,
    fraction_elapsed: float,
    year_days: float = DASHA_YEAR_DAYS,
) -> list[dict[str, Any]]:
    """
    Computes complete lifetime Vimshottari Mahadasha and Antardasha timeline
    using fixed-length Vimshottari years (default 365.25 days).
    """
    start_idx = -1
    for i, (lord, span) in enumerate(DASHA_ORDER):
        if lord.lower() == moon_nakshatra_lord.lower():
            start_idx = i
            break

    if start_idx == -1:
        raise ValueError(f"Unknown Nakshatra Lord: {moon_nakshatra_lord}")

    first_lord, first_span = DASHA_ORDER[start_idx]
    remaining_balance_years = first_span * (1.0 - fraction_elapsed)

    timeline: list[dict[str, Any]] = []
    current_dt = birth_dt

    for cycle_step in range(9):
        idx = (start_idx + cycle_step) % 9
        lord, span = DASHA_ORDER[idx]

        mahadasha_duration = remaining_balance_years if cycle_step == 0 else span
        maha_start_dt = current_dt
        maha_end_dt = maha_start_dt + years_to_timedelta(
            mahadasha_duration, year_days=year_days
        )

        antardashas: list[dict[str, Any]] = []
        sub_start_dt = maha_start_dt
        sub_ratio = (remaining_balance_years / span) if cycle_step == 0 else 1.0

        for sub_step in range(9):
            sub_idx = (idx + sub_step) % 9
            sub_lord, sub_base_years = DASHA_ORDER[sub_idx]

            sub_duration = (span * sub_base_years / TOTAL_DASHA_CYCLE) * sub_ratio
            sub_end_dt = sub_start_dt + years_to_timedelta(
                sub_duration, year_days=year_days
            )

            antardashas.append(
                {
                    "mahadasha": lord,
                    "antardasha": sub_lord,
                    # Full precision — rounding here drops the birth instant outside [start, end].
                    "start_decimal": datetime_to_fixed_year_decimal(
                        sub_start_dt, year_days
                    ),
                    "end_decimal": datetime_to_fixed_year_decimal(
                        sub_end_dt, year_days
                    ),
                    "start_date": sub_start_dt.strftime("%Y-%m-%d"),
                    "end_date": sub_end_dt.strftime("%Y-%m-%d"),
                    "duration_years": round(sub_duration, 3),
                }
            )
            sub_start_dt = sub_end_dt

        timeline.append(
            {
                "mahadasha": lord,
                "start_decimal": datetime_to_fixed_year_decimal(
                    maha_start_dt, year_days
                ),
                "end_decimal": datetime_to_fixed_year_decimal(maha_end_dt, year_days),
                "start_date": maha_start_dt.strftime("%Y-%m-%d"),
                "end_date": maha_end_dt.strftime("%Y-%m-%d"),
                "duration_years": round(mahadasha_duration, 3),
                "antardashas": antardashas,
            }
        )

        current_dt = maha_end_dt

    return timeline


def get_active_dasha_at_date(
    timeline: list[dict[str, Any]],
    target_dt: datetime,
    year_days: float = DASHA_YEAR_DAYS,
) -> dict[str, Any]:
    """
    Returns the exact Mahadasha and Antardasha active at a given target date.
    """
    target_dec = datetime_to_fixed_year_decimal(target_dt, year_days=year_days)

    for maha in timeline:
        if maha["start_decimal"] <= target_dec <= maha["end_decimal"]:
            for antar in maha["antardashas"]:
                if antar["start_decimal"] <= target_dec <= antar["end_decimal"]:
                    return {
                        "target_date": target_dt.strftime("%Y-%m-%d"),
                        "target_decimal": target_dec,
                        "mahadasha": maha["mahadasha"],
                        "antardasha": antar["antardasha"],
                        "period_start": antar["start_date"],
                        "period_end": antar["end_date"],
                    }

    return {"error": "Target date out of computed timeline bounds"}
