"""
karmic-ledger: Classical Transit & Drishti Engine
Computes planetary transits (Gochar) and Parashari aspects for event backtesting.
"""

from datetime import datetime
from typing import Any

import swisseph as swe

ZODIAC_SIGNS: list[str] = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

SIGN_TO_INDEX: dict[str, int] = {s: i for i, s in enumerate(ZODIAC_SIGNS)}


def get_planet_transit_positions(target_dt: datetime) -> dict[str, Any]:
    """
    Computes sidereal planetary transit positions on any historical or future date.
    """
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    decimal_hours = target_dt.hour + target_dt.minute / 60.0 + target_dt.second / 3600.0
    jd = swe.julday(target_dt.year, target_dt.month, target_dt.day, decimal_hours)

    planets = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mars": swe.MARS,
        "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS,
        "Saturn": swe.SATURN,
        "Rahu": swe.TRUE_NODE,
    }

    transits: dict[str, Any] = {}

    for name, p_id in planets.items():
        res, _ = swe.calc_ut(jd, p_id, swe.FLG_SIDEREAL | swe.FLG_SWIEPH)
        deg = res[0]
        sign_idx = int(deg // 30)
        deg_in_sign = deg % 30.0

        transits[name] = {
            "longitude": deg,
            "sign": ZODIAC_SIGNS[sign_idx],
            "sign_index": sign_idx,
            "degree_in_sign": deg_in_sign,
            "formatted": f"{ZODIAC_SIGNS[sign_idx]} {int(deg_in_sign):02d}°{int((deg_in_sign % 1) * 60):02d}'",
        }

    # Ketu opposite Rahu
    ketu_deg = (transits["Rahu"]["longitude"] + 180.0) % 360.0
    ketu_sign_idx = int(ketu_deg // 30)
    transits["Ketu"] = {
        "longitude": ketu_deg,
        "sign": ZODIAC_SIGNS[ketu_sign_idx],
        "sign_index": ketu_sign_idx,
        "degree_in_sign": ketu_deg % 30.0,
        "formatted": f"{ZODIAC_SIGNS[ketu_sign_idx]} {int(ketu_deg % 30):02d}°{int(((ketu_deg % 30) % 1) * 60):02d}'",
    }

    return transits


def get_parashari_aspects(planet: str, sign_index: int) -> list[int]:
    """
    Returns list of sign indices (0-11) aspected by a planet based on classical Parashara rules.
    1-indexed house aspects:
    - All planets aspect 7th sign.
    - Mars: 4th, 7th, 8th signs.
    - Jupiter: 5th, 7th, 9th signs.
    - Saturn: 3rd, 7th, 10th signs.
    - Rahu/Ketu: 5th, 7th, 9th signs.
    """
    aspects = [(sign_index + 6) % 12]  # Standard 7th aspect

    if planet == "Mars":
        aspects.extend([(sign_index + 3) % 12, (sign_index + 7) % 12])  # 4th and 8th
    elif planet in ["Jupiter", "Rahu", "Ketu"]:
        aspects.extend([(sign_index + 4) % 12, (sign_index + 8) % 12])  # 5th and 9th
    elif planet == "Saturn":
        aspects.extend([(sign_index + 2) % 12, (sign_index + 9) % 12])  # 3rd and 10th

    return list(set(aspects))


def check_double_transit(target_dt: datetime, target_sign: str) -> dict[str, Any]:
    """
    Checks if classical Double-Transit (Jupiter AND Saturn) aspects a target sign.
    Required condition in classical Jyotish for major life events (marriage, progeny, relocation).
    """
    transits = get_planet_transit_positions(target_dt)
    target_idx = SIGN_TO_INDEX[target_sign]

    jup_sign_idx = transits["Jupiter"]["sign_index"]
    sat_sign_idx = transits["Saturn"]["sign_index"]

    # Check Jupiter conjunct or aspecting target sign
    jup_aspects = get_parashari_aspects("Jupiter", jup_sign_idx)
    jup_hits = (jup_sign_idx == target_idx) or (target_idx in jup_aspects)

    # Check Saturn conjunct or aspecting target sign
    sat_aspects = get_parashari_aspects("Saturn", sat_sign_idx)
    sat_hits = (sat_sign_idx == target_idx) or (target_idx in sat_aspects)

    return {
        "target_date": target_dt.strftime("%Y-%m-%d"),
        "target_sign": target_sign,
        "jupiter_transit": transits["Jupiter"]["formatted"],
        "saturn_transit": transits["Saturn"]["formatted"],
        "jupiter_aspects_target": jup_hits,
        "saturn_aspects_target": sat_hits,
        "double_transit_active": (jup_hits and sat_hits),
    }
