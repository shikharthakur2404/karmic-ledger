"""
karmic-ledger: Daily Somatic & Micro-Incident Telemetry Engine
Computes 24-hour transit-based incident radar indices for real-time
tactical awareness: Chandrāṣṭama disruption, somatic injury vectors,
and Mercury communication bottlenecks.

Strict Epistemic Primacy:
Zero assertions of real-world medical events, physical injuries, or
bureaucratic outcomes. All outputs are symbolic planetary tension indices
framed as abstract archetypal strain themes.
"""

from datetime import datetime
from typing import Any, Optional

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

SIGN_LORDS: dict[str, str] = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}

SIGN_TO_INDEX: dict[str, int] = {s: i for i, s in enumerate(ZODIAC_SIGNS)}

# Mars debilitation signs (water signs → slips, liquid/dishwashing accidents)
MARS_WEAK_SIGN_INDICES: list[int] = [
    SIGN_TO_INDEX["Cancer"],  # Mars debilitated in Cancer
    SIGN_TO_INDEX["Pisces"],
    SIGN_TO_INDEX["Scorpio"],  # Own sign but water element → liquid risk context
]

# Nakshatra span: 360/27 = 13.3333 degrees
NAK_SPAN = 360.0 / 27.0
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


def _calculate_nakshatra(longitude: float) -> dict[str, Any]:
    """Computes Nakshatra, Pada, Lord, and fractional progress for a longitude."""
    nak_idx = int(longitude // NAK_SPAN)
    remainder = longitude % NAK_SPAN
    pada = int(remainder // (NAK_SPAN / 4.0)) + 1

    name, lord = NAKSHATRAS[nak_idx]
    progress_fraction = remainder / NAK_SPAN

    return {
        "index": nak_idx + 1,
        "name": name,
        "pada": pada,
        "lord": lord,
        "fraction_elapsed": progress_fraction,
        "degrees_into_nakshatra": remainder,
    }


def _get_transits(target_dt: datetime) -> dict[str, Any]:
    """Computes sidereal transit positions for target datetime."""
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
        nak = _calculate_nakshatra(deg)

        transits[name] = {
            "longitude": deg,
            "sign": ZODIAC_SIGNS[sign_idx],
            "sign_index": sign_idx,
            "degree_in_sign": deg_in_sign,
            "formatted": f"{ZODIAC_SIGNS[sign_idx]} {int(deg_in_sign):02d}°{int((deg_in_sign % 1) * 60):02d}'",
            "nakshatra": nak,
        }

    ketu_deg = (transits["Rahu"]["longitude"] + 180.0) % 360.0
    ketu_sign_idx = int(ketu_deg // 30)
    ketu_deg_in_sign = ketu_deg % 30.0
    transits["Ketu"] = {
        "longitude": ketu_deg,
        "sign": ZODIAC_SIGNS[ketu_sign_idx],
        "sign_index": ketu_sign_idx,
        "degree_in_sign": ketu_deg_in_sign,
        "formatted": f"{ZODIAC_SIGNS[ketu_sign_idx]} {int(ketu_deg_in_sign):02d}°{int(((ketu_deg_in_sign) % 1) * 60):02d}'",
        "nakshatra": _calculate_nakshatra(ketu_deg),
    }

    return transits


def _get_parashari_aspects(planet: str, sign_index: int) -> list[int]:
    """Returns sign indices (0-11) aspected by a planet via classical Parashara rules."""
    aspects = [(sign_index + 6) % 12]

    if planet == "Mars":
        aspects.extend([(sign_index + 3) % 12, (sign_index + 7) % 12])
    elif planet in ["Jupiter", "Rahu", "Ketu"]:
        aspects.extend([(sign_index + 4) % 12, (sign_index + 8) % 12])
    elif planet == "Saturn":
        aspects.extend([(sign_index + 2) % 12, (sign_index + 9) % 12])

    return list(set(aspects))


def _detect_chandrashtama(
    transits: dict[str, Any],
    natal_moon_sign: str,
) -> dict[str, Any]:
    """
    Chandrāṣṭama Radar — The 8th-House Disruption Index.

    Detects when the transit Moon occupies the 8th house from natal Moon,
    signaling high-variance disruption potential: last-minute cancellations,
    cognitive fatigue, interview rescheduling, and travel delays.
    """
    natal_moon_idx = SIGN_TO_INDEX[natal_moon_sign]
    transit_moon = transits["Moon"]
    transit_moon_idx = transit_moon["sign_index"]

    # House from natal Moon (1-indexed)
    house_from_moon = ((transit_moon_idx - natal_moon_idx) % 12) + 1

    is_active = house_from_moon == 8
    nak = transit_moon["nakshatra"]

    # Percentage completion of 8th-house transit (approximate)
    # The Moon spends ~2.25 days per sign. 8th house transit = current sign position within that sign.
    pct_in_sign = (transit_moon["degree_in_sign"] / 30.0) * 100.0

    alert_text = ""
    tactical_advice = ""
    if is_active:
        alert_text = (
            f"Transit Moon in {transit_moon['formatted']} (8th from natal Moon in {natal_moon_sign}). "
            f"Nakshatra: {nak['name']} (Pada {nak['pada']}, Lord: {nak['lord']}). "
            f"Transit Moon at {pct_in_sign:.1f}% through current sign."
        )
        tactical_advice = (
            "Postpone high-stakes interviews, negotiations, or first-impression meetings until Moon "
            "enters the next sign. Cognitive variance is elevated — expect last-minute rescheduling, "
            "delayed responses, or travel friction. Prioritize rest and low-stakes administrative work."
        )

    return {
        "is_active": is_active,
        "house_from_moon": house_from_moon,
        "transit_moon_sign": transit_moon["sign"],
        "transit_moon_formatted": transit_moon["formatted"],
        "transit_moon_nakshatra": nak["name"],
        "transit_moon_nakshatra_pada": nak["pada"],
        "transit_moon_nakshatra_lord": nak["lord"],
        "pct_through_sign": round(pct_in_sign, 1),
        "alert": alert_text,
        "tactical_advice": tactical_advice,
    }


def _detect_somatic_injury(
    natal: dict[str, Any],
    transits: dict[str, Any],
) -> dict[str, Any]:
    """
    Somatic Injury & Seva (Manual Labor) Index.

    Tracks the Lagnesha (Lord of House 1) transit through House 6
    (Roga/Kshata/Seva Bhāva) and checks for conjunctions/aspects with
    Mars (cuts, falls, acute trauma) and Saturn (joints, bones, chronic load).
    """
    zodiac = ZODIAC_SIGNS
    lagna_sign = natal["lagna"]["sign"]
    lagna_idx = zodiac.index(lagna_sign)

    def house_for_sign(sign: str) -> int:
        return ((SIGN_TO_INDEX[sign] - lagna_idx) % 12) + 1

    # Identify Lagnesha
    lagna_lord = SIGN_LORDS.get(lagna_sign, "Unknown")

    # Transit Lagnesha position
    if lagna_lord in transits:
        lagna_lord_transit = transits[lagna_lord]
        lagna_lord_house = house_for_sign(lagna_lord_transit["sign"])
    else:
        lagna_lord_transit = None
        lagna_lord_house = None

    in_house_6 = lagna_lord_house == 6

    somatic_vectors: list[str] = []
    risk_level = "Low"
    target_limbs: list[str] = []

    if in_house_6:
        # Check Mars conjunction or tight aspect (< 5° orb)
        mars_transit = transits["Mars"]

        mars_sign_idx = mars_transit["sign_index"]
        lagna_lord_sign_idx = SIGN_TO_INDEX[lagna_lord_transit["sign"]]
        sign_distance = abs(mars_sign_idx - lagna_lord_sign_idx)
        is_mars_conjunct = (
            sign_distance <= 1
            and abs(lagna_lord_transit["longitude"] - mars_transit["longitude"]) < 5.0
        )

        mars_aspects = _get_parashari_aspects("Mars", mars_sign_idx)
        is_mars_aspecting = lagna_lord_sign_idx in mars_aspects

        if is_mars_conjunct or is_mars_aspecting:
            somatic_vectors.append(
                f"Mars ({mars_transit['formatted']}) in tight aspect/conjunction with Lagnesha {lagna_lord} — "
                f"symbolic tension for acute physical disruption (cuts, falls, impact)."
            )
            risk_level = "Elevated"
            target_limbs.extend(["Joints", "Knees"])

        # Check Saturn aspects on Lagnesha
        saturn_transit = transits["Saturn"]
        saturn_sign_idx = saturn_transit["sign_index"]
        saturn_aspects = _get_parashari_aspects("Saturn", saturn_sign_idx)
        is_saturn_aspecting = lagna_lord_sign_idx in saturn_aspects

        if is_saturn_aspecting:
            somatic_vectors.append(
                f"Saturn ({saturn_transit['formatted']}) aspects Lagnesha {lagna_lord} — "
                f"symbolic pressure on bones, joints, and chronic physical load."
            )
            if risk_level != "Elevated":
                risk_level = "Moderate"
            target_limbs.extend(["Bones", "Joints"])

        # Check debilitated Mars (water signs → slips, liquid accidents)
        if mars_transit["sign_index"] in MARS_WEAK_SIGN_INDICES:
            somatic_vectors.append(
                f"Mars debilitated in {mars_transit['sign']} — elevated symbolic variance for slips, "
                f"falls, or liquid-related physical disruption."
            )
            if risk_level == "Low":
                risk_level = "Moderate"
            target_limbs.extend(["Feet", "Balance"])

        # Seva (manual labor) alert when Lagnesha in H6
        somatic_vectors.append(
            f"Lagnesha {lagna_lord} transiting House 6 ({lagna_lord_transit['sign']}): "
            f"Symbolic activation of service, subordinate tasks, or unexpected manual obligations (Seva Bhāva)."
        )

    tactical_advice = ""
    if in_house_6 and somatic_vectors:
        limb_str = (
            ", ".join(sorted(set(target_limbs))) if target_limbs else "General physical"
        )
        tactical_advice = (
            f"Physical risk vectors active for {limb_str}. Avoid heavy joint-impact activities, "
            f"prolonged standing, or rushed physical exertion for the next 24–48 hours. "
            f"Manual labor or subordinate task obligations may surface unexpectedly."
        )

    return {
        "is_active": in_house_6,
        "lagnesha": lagna_lord,
        "lagnesha_transit": lagna_lord_transit["formatted"]
        if lagna_lord_transit
        else "N/A",
        "lagnesha_transit_house": lagna_lord_house,
        "in_house_6": in_house_6,
        "risk_level": risk_level,
        "target_limbs": sorted(set(target_limbs)),
        "somatic_vectors": somatic_vectors,
        "alert": somatic_vectors[0] if somatic_vectors else "",
        "tactical_advice": tactical_advice,
    }


def _detect_mercury_sandhi(transits: dict[str, Any]) -> dict[str, Any]:
    """
    Planetary Sandhi / Gandanta Communication Bottleneck.

    Checks if transit Mercury is in Rāshi Sandhi zones:
    28°45' – 29°59' (end of a sign) or 00°00' – 01°15' (beginning of a sign).
    Mercury governs emails, interviews, contracts, and hiring communications.
    """
    mercury = transits["Mercury"]
    deg_in_sign = mercury["degree_in_sign"]

    # Sandhi zones: 28.75°–30° (end) or 0°–1.25° (beginning)
    is_end_zone = deg_in_sign >= 28.75
    is_beginning_zone = deg_in_sign <= 1.25
    is_sandhi = is_end_zone or is_beginning_zone

    sandhi_type = ""
    if is_end_zone:
        sandhi_type = f"End-zone Sandhi ({deg_in_sign:.2f}° in {mercury['sign']})"
    elif is_beginning_zone:
        sandhi_type = f"Beginning-zone Sandhi ({deg_in_sign:.2f}° in {mercury['sign']})"

    alert_text = ""
    tactical_advice = ""
    if is_sandhi:
        alert_text = (
            f"Mercury at {mercury['formatted']} — Communication dead-zone detected ({sandhi_type}). "
            f"Expect stalled recruiter emails, unanswered messages, automated dispatch glitches, "
            f"or interview scheduling misfires."
        )
        tactical_advice = (
            "Avoid sending critical emails, signing contracts, or initiating important conversations "
            "for the next 24–48 hours. Follow up in writing after Mercury clears the Sandhi zone. "
            "Do not rely on automated scheduling tools."
        )

    return {
        "is_active": is_sandhi,
        "sandhi_type": sandhi_type,
        "mercury_sign": mercury["sign"],
        "mercury_formatted": mercury["formatted"],
        "mercury_degree_in_sign": round(deg_in_sign, 2),
        "alert": alert_text,
        "tactical_advice": tactical_advice,
    }


def compute_daily_incident_radar(
    natal: dict[str, Any],
    target_dt: Optional[datetime] = None,
) -> dict[str, Any]:
    """
    Computes the 24-hour Daily Micro-Incident Radar telemetry payload.

    Integrates three mathematical incident detectors:
    1. Chandrāṣṭama Radar (8th-house disruption index from natal Moon)
    2. Somatic Injury & Seva Index (Lagnesha in House 6 with Mars/Saturn aspects)
    3. Mercury Sandhi / Gandanta Communication Bottleneck

    Returns a consolidated telemetry dict for pipeline integration and HUD rendering.
    """
    if target_dt is None:
        target_dt = datetime.utcnow()

    swe.set_sid_mode(swe.SIDM_LAHIRI)

    transits = _get_transits(target_dt)

    natal_moon_sign = natal["planets"]["Moon"]["sign"]

    chandrashtama = _detect_chandrashtama(transits, natal_moon_sign)
    somatic = _detect_somatic_injury(natal, transits)
    mercury_sandhi = _detect_mercury_sandhi(transits)

    # Aggregate tactical advice
    all_advice: list[str] = []
    if chandrashtama["tactical_advice"]:
        all_advice.append(chandrashtama["tactical_advice"])
    if somatic["tactical_advice"]:
        all_advice.append(somatic["tactical_advice"])
    if mercury_sandhi["tactical_advice"]:
        all_advice.append(mercury_sandhi["tactical_advice"])

    # Overall risk assessment
    active_count = sum(
        [
            chandrashtama["is_active"],
            somatic["is_active"],
            mercury_sandhi["is_active"],
        ]
    )

    if active_count >= 3:
        overall_status = "HIGH_VAR"
        status_label = "High Variance — Multiple vectors active"
    elif active_count == 2:
        overall_status = "ELEVATED"
        status_label = "Elevated — Dual vector activation"
    elif active_count == 1:
        overall_status = "SINGLE_ACTIVE"
        status_label = "Single vector active"
    else:
        overall_status = "CLEAR"
        status_label = "Clear — No active incident vectors"

    return {
        "generated_at": target_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "overall_status": overall_status,
        "overall_status_label": status_label,
        "active_vector_count": active_count,
        "chandrashtama": chandrashtama,
        "somatic_injury": somatic,
        "mercury_sandhi": mercury_sandhi,
        "tactical_advice": all_advice,
        "ephemeris_timestamp": target_dt.isoformat(),
    }
