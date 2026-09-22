"""
karmic-ledger: Core Ephemeris Engine
High-precision astronomical compute layer using Swiss Ephemeris (Lahiri Sidereal).
"""

from datetime import datetime
from typing import Any

import swisseph as swe

# 27 Nakshatras with Ruling Planet and Span
NAKSHATRAS: list[tuple[str, str]] = [
    ("Ashwini", "Ketu"),
    ("Bharani", "Venus"),
    ("Krittika", "Sun"),
    ("Rohini", "Moon"),
    ("Mrigashira", "Mars"),
    ("Ardra", "Rahu"),
    ("Punarvasu", "Jupiter"),
    ("Pushya", "Saturn"),
    ("Ashlesha", "Mercury"),
    ("Magha", "Ketu"),
    ("Purva Phalguni", "Venus"),
    ("Uttara Phalguni", "Sun"),
    ("Hasta", "Moon"),
    ("Chitra", "Mars"),
    ("Swati", "Rahu"),
    ("Vishakha", "Jupiter"),
    ("Anuradha", "Saturn"),
    ("Jyeshtha", "Mercury"),
    ("Mula", "Ketu"),
    ("Purva Ashadha", "Venus"),
    ("Uttara Ashadha", "Sun"),
    ("Shravana", "Moon"),
    ("Dhanishta", "Mars"),
    ("Shatabhisha", "Rahu"),
    ("Purva Bhadrapada", "Jupiter"),
    ("Uttara Bhadrapada", "Saturn"),
    ("Revati", "Mercury"),
]

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

PLANET_IDS: dict[str, int] = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.TRUE_NODE,
}

# Classical Planetary Dignities (Exaltation & Debilitation degrees)
DIGNITIES: dict[str, dict[str, Any]] = {
    "Sun": {
        "exalt_sign": "Aries",
        "exalt_deg": 10.0,
        "deb_sign": "Libra",
        "deb_deg": 10.0,
        "own": ["Leo"],
    },
    "Moon": {
        "exalt_sign": "Taurus",
        "exalt_deg": 3.0,
        "deb_sign": "Scorpio",
        "deb_deg": 3.0,
        "own": ["Cancer"],
    },
    "Mars": {
        "exalt_sign": "Capricorn",
        "exalt_deg": 28.0,
        "deb_sign": "Cancer",
        "deb_deg": 28.0,
        "own": ["Aries", "Scorpio"],
    },
    "Mercury": {
        "exalt_sign": "Virgo",
        "exalt_deg": 15.0,
        "deb_sign": "Pisces",
        "deb_deg": 15.0,
        "own": ["Gemini", "Virgo"],
    },
    "Jupiter": {
        "exalt_sign": "Cancer",
        "exalt_deg": 5.0,
        "deb_sign": "Capricorn",
        "deb_deg": 5.0,
        "own": ["Sagittarius", "Pisces"],
    },
    "Venus": {
        "exalt_sign": "Pisces",
        "exalt_deg": 27.0,
        "deb_sign": "Virgo",
        "deb_deg": 27.0,
        "own": ["Taurus", "Libra"],
    },
    "Saturn": {
        "exalt_sign": "Libra",
        "exalt_deg": 20.0,
        "deb_sign": "Aries",
        "deb_deg": 20.0,
        "own": ["Capricorn", "Aquarius"],
    },
    "Rahu": {
        "exalt_sign": "Taurus",
        "exalt_deg": 15.0,
        "deb_sign": "Scorpio",
        "deb_deg": 15.0,
        "own": ["Aquarius"],
    },
    "Ketu": {
        "exalt_sign": "Scorpio",
        "exalt_deg": 15.0,
        "deb_sign": "Taurus",
        "deb_deg": 15.0,
        "own": ["Scorpio"],
    },
}


def calculate_nakshatra(longitude: float) -> dict[str, Any]:
    """Computes exact Nakshatra, Pada, Lord, and fractional progress."""
    nak_span = 360.0 / 27.0  # 13°20' = 13.333333°
    pada_span = nak_span / 4.0  # 3°20' = 3.333333°

    nak_idx = int(longitude // nak_span)
    remainder = longitude % nak_span
    pada = int(remainder // pada_span) + 1

    name, lord = NAKSHATRAS[nak_idx]
    progress_fraction = remainder / nak_span

    return {
        "index": nak_idx + 1,
        "name": name,
        "pada": pada,
        "lord": lord,
        "fraction_elapsed": progress_fraction,
        "degrees_into_nakshatra": remainder,
    }


def evaluate_dignity(planet: str, sign: str, deg_in_sign: float) -> str:
    """Evaluates whether a planet is Exalted, Debilitated, Own Sign, or Neutral."""
    rule = DIGNITIES.get(planet)
    if not rule:
        return "Neutral"

    if sign == rule.get("exalt_sign"):
        return "Exalted (Uccha)"
    elif sign == rule.get("deb_sign"):
        return "Debilitated (Neecha)"
    elif sign in rule.get("own", []):
        return "Own Sign (Swakshetra)"
    return "Neutral"


def compute_natal_chart(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    second: int,
    lat: float,
    lon: float,
    tz_offset_hours: float = 5.5,
) -> dict[str, Any]:
    """
    Computes complete Vedic Natal Chart with Lahiri Sidereal Ayanamsha.
    """
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    from datetime import timedelta

    local_dt = datetime(year, month, day, hour, minute, second)
    utc_dt = local_dt - timedelta(hours=tz_offset_hours)
    utc_hours = utc_dt.hour + (utc_dt.minute / 60.0) + (utc_dt.second / 3600.0)

    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_hours)
    ayanamsa = swe.get_ayanamsa_ut(jd)

    # Calculate Ascendant & Houses (Whole Sign / Porphyry)
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b"W", swe.FLG_SIDEREAL)
    lagna_deg = ascmc[0]
    lagna_sign_idx = int(lagna_deg // 30)
    lagna_sign = ZODIAC_SIGNS[lagna_sign_idx]
    lagna_nak = calculate_nakshatra(lagna_deg)

    planets_data: dict[str, Any] = {}

    for p_name, p_id in PLANET_IDS.items():
        res, _ = swe.calc_ut(jd, p_id, swe.FLG_SIDEREAL | swe.FLG_SWIEPH)
        deg = res[0]
        sign_idx = int(deg // 30)
        sign_name = ZODIAC_SIGNS[sign_idx]
        deg_in_sign = deg % 30.0
        nak_info = calculate_nakshatra(deg)
        dignity = evaluate_dignity(p_name, sign_name, deg_in_sign)

        # House from Lagna (1-indexed)
        house_num = ((sign_idx - lagna_sign_idx) % 12) + 1

        planets_data[p_name] = {
            "longitude": deg,
            "sign": sign_name,
            "degree_in_sign": deg_in_sign,
            "formatted": f"{sign_name} {int(deg_in_sign):02d}°{int((deg_in_sign % 1) * 60):02d}'",
            "house": house_num,
            "nakshatra": nak_info,
            "dignity": dignity,
        }

    # Compute Ketu (180° opposite to True Node Rahu)
    ketu_deg = (planets_data["Rahu"]["longitude"] + 180.0) % 360.0
    ketu_sign_idx = int(ketu_deg // 30)
    ketu_sign = ZODIAC_SIGNS[ketu_sign_idx]
    ketu_deg_in_sign = ketu_deg % 30.0
    ketu_nak = calculate_nakshatra(ketu_deg)
    ketu_house = ((ketu_sign_idx - lagna_sign_idx) % 12) + 1

    planets_data["Ketu"] = {
        "longitude": ketu_deg,
        "sign": ketu_sign,
        "degree_in_sign": ketu_deg_in_sign,
        "formatted": f"{ketu_sign} {int(ketu_deg_in_sign):02d}°{int((ketu_deg_in_sign % 1) * 60):02d}'",
        "house": ketu_house,
        "nakshatra": ketu_nak,
        "dignity": evaluate_dignity("Ketu", ketu_sign, ketu_deg_in_sign),
    }

    return {
        "julian_day": jd,
        "ayanamsa": ayanamsa,
        "lagna": {
            "longitude": lagna_deg,
            "sign": lagna_sign,
            "degree_in_sign": lagna_deg % 30.0,
            "formatted": f"{lagna_sign} {int(lagna_deg % 30):02d}°{int(((lagna_deg % 30) % 1) * 60):02d}'",
            "nakshatra": lagna_nak,
        },
        "planets": planets_data,
    }
