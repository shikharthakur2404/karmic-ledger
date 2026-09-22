"""
karmic-ledger: Vimshottari Dasha Engine
Computes 120-year planetary dasha cycles and granular sub-periods down to exact calendar days.
"""

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


def decimal_year_to_date(decimal_year: float) -> str:
    """Converts a decimal year (e.g. 2022.99) into ISO YYYY-MM-DD string."""
    year = int(decimal_year)
    remainder = decimal_year - year
    start_of_year = datetime(year, 1, 1)
    days_in_year = (
        366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365
    )
    target_date = start_of_year + timedelta(days=remainder * days_in_year)
    return target_date.strftime("%Y-%m-%d")


def compute_vimshottari_timeline(
    birth_dt: datetime, moon_nakshatra_lord: str, fraction_elapsed: float
) -> list[dict[str, Any]]:
    """
    Computes complete lifetime Vimshottari Mahadasha and Antardasha timeline.
    """
    # Find starting lord index
    start_idx = -1
    for i, (lord, span) in enumerate(DASHA_ORDER):
        if lord.lower() == moon_nakshatra_lord.lower():
            start_idx = i
            break

    if start_idx == -1:
        raise ValueError(f"Unknown Nakshatra Lord: {moon_nakshatra_lord}")

    birth_year_decimal = birth_dt.year + (birth_dt.timetuple().tm_yday - 1) / (
        366.0 if birth_dt.year % 4 == 0 else 365.0
    )

    first_lord, first_span = DASHA_ORDER[start_idx]
    remaining_balance_years = first_span * (1.0 - fraction_elapsed)

    timeline: list[dict[str, Any]] = []
    current_year_dec = birth_year_decimal

    for cycle_step in range(9):
        idx = (start_idx + cycle_step) % 9
        lord, span = DASHA_ORDER[idx]

        # First Mahadasha uses remaining balance
        mahadasha_duration = remaining_balance_years if cycle_step == 0 else span
        maha_start_dec = current_year_dec
        maha_end_dec = maha_start_dec + mahadasha_duration

        # Compute Antardashas within this Mahadasha
        antardashas: list[dict[str, Any]] = []
        sub_start_dec = maha_start_dec

        # In the first dasha, we scale sub-periods proportionally to the remaining balance
        sub_ratio = (remaining_balance_years / span) if cycle_step == 0 else 1.0

        for sub_step in range(9):
            sub_idx = (idx + sub_step) % 9
            sub_lord, sub_base_years = DASHA_ORDER[sub_idx]

            # Sub-period formula: (Mahadasha Years * Sub Lord Years / 120) * sub_ratio
            sub_duration = (span * sub_base_years / TOTAL_DASHA_CYCLE) * sub_ratio
            sub_end_dec = sub_start_dec + sub_duration

            antardashas.append(
                {
                    "mahadasha": lord,
                    "antardasha": sub_lord,
                    "start_decimal": round(sub_start_dec, 4),
                    "end_decimal": round(sub_end_dec, 4),
                    "start_date": decimal_year_to_date(sub_start_dec),
                    "end_date": decimal_year_to_date(sub_end_dec),
                    "duration_years": round(sub_duration, 3),
                }
            )
            sub_start_dec = sub_end_dec

        timeline.append(
            {
                "mahadasha": lord,
                "start_decimal": round(maha_start_dec, 4),
                "end_decimal": round(maha_end_dec, 4),
                "start_date": decimal_year_to_date(maha_start_dec),
                "end_date": decimal_year_to_date(maha_end_dec),
                "duration_years": round(mahadasha_duration, 3),
                "antardashas": antardashas,
            }
        )

        current_year_dec = maha_end_dec

    return timeline


def get_active_dasha_at_date(
    timeline: list[dict[str, Any]], target_dt: datetime
) -> dict[str, Any]:
    """
    Returns the exact Mahadasha and Antardasha active at a given target date.
    """
    target_dec = target_dt.year + (target_dt.timetuple().tm_yday - 1) / (
        366.0 if target_dt.year % 4 == 0 else 365.0
    )

    for maha in timeline:
        if maha["start_decimal"] <= target_dec <= maha["end_decimal"]:
            for antar in maha["antardashas"]:
                if antar["start_decimal"] <= target_dec <= antar["end_decimal"]:
                    return {
                        "target_date": target_dt.strftime("%Y-%m-%d"),
                        "target_decimal": round(target_dec, 4),
                        "mahadasha": maha["mahadasha"],
                        "antardasha": antar["antardasha"],
                        "period_start": antar["start_date"],
                        "period_end": antar["end_date"],
                    }

    return {"error": "Target date out of computed timeline bounds"}
