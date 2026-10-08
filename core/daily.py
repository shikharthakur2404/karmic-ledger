"""
karmic-ledger: Full-Spectrum Daily Transit & Incident Radar Engine
Computes 24-hour transit dynamics for real-time tactical awareness:
- Lunar Mind State & Nakshatra Drivers (Ardra/Rahu nightlife, Rohini/Venus dining)
- Kinetic Vitality & Physical Output (Mars/Lagnesha stamina, endurance, high step capacity)
- Recreational, Social & Culinary Vectors (5th/11th house, Rahu/Venus social pulse)
- Short-Range Mobility & Exploration (3rd house, train hops, hiking trails)
- Social Gatekeeper & Access Friction (Saturnian venue screening / bouncers)
- Cognitive & Logistical Fluidity (Mercury communication & tactical advice)

Strict Epistemic Primacy:
All outputs represent symbolic atmospheric timing vectors — not medical prophecies
or rigid fatalism. Designed to empower sovereignty and grounded situational awareness.
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

# Nakshatra span: 360 / 27 = 13.3333 degrees
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

    name, lord = NAKSHATRAS[nak_idx % 27]
    progress_fraction = remainder / NAK_SPAN

    return {
        "index": (nak_idx % 27) + 1,
        "name": name,
        "pada": pada,
        "lord": lord,
        "fraction_elapsed": progress_fraction,
        "degrees_into_nakshatra": remainder,
    }


def _get_transits(target_dt: datetime) -> dict[str, Any]:
    """Computes sidereal transit positions for target datetime using Lahiri Ayanamsha."""
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
        deg = res[0] % 360.0
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
        "formatted": f"{ZODIAC_SIGNS[ketu_sign_idx]} {int(ketu_deg_in_sign):02d}°{int((ketu_deg_in_sign % 1) * 60):02d}'",
        "nakshatra": _calculate_nakshatra(ketu_deg),
    }

    return transits


def _get_parashari_aspects(planet: str, sign_index: int) -> list[int]:
    """Returns sign indices (0-11) aspected by a planet via classical Parashara rules."""
    aspects = [(sign_index + 6) % 12]  # All planets cast 7th aspect

    if planet == "Mars":
        aspects.extend([(sign_index + 3) % 12, (sign_index + 7) % 12])  # 4th and 8th
    elif planet in ["Jupiter", "Rahu", "Ketu"]:
        aspects.extend([(sign_index + 4) % 12, (sign_index + 8) % 12])  # 5th and 9th
    elif planet == "Saturn":
        aspects.extend([(sign_index + 2) % 12, (sign_index + 9) % 12])  # 3rd and 10th

    return list(set(aspects))


def _detect_lunar_state(
    transits: dict[str, Any],
    natal_moon_sign: str,
    natal_lagna_sign: str,
) -> dict[str, Any]:
    """
    Evaluates the Lunar Emotional State, Nakshatra Driver, and Chandrashtama.
    """
    natal_moon_idx = SIGN_TO_INDEX[natal_moon_sign]
    natal_lagna_idx = SIGN_TO_INDEX[natal_lagna_sign]
    transit_moon = transits["Moon"]
    transit_moon_idx = transit_moon["sign_index"]

    house_from_moon = ((transit_moon_idx - natal_moon_idx) % 12) + 1
    house_from_lagna = ((transit_moon_idx - natal_lagna_idx) % 12) + 1

    nak = transit_moon["nakshatra"]
    nak_lord = nak["lord"]
    pct_in_sign = (transit_moon["degree_in_sign"] / 30.0) * 100.0

    is_chandrashtama = house_from_moon == 8

    # Determine emotional & cognitive driver based on Nakshatra Lord & House
    driver_summary = ""
    if nak_lord == "Rahu":
        driver_summary = (
            f"Moon in {nak['name']} (Lord: Rahu) — Sparks appetite for unconventional exploration, "
            "nocturnal stimulation, late hours, and curious detachment from rigid routines."
        )
    elif nak_lord == "Mars":
        driver_summary = (
            f"Moon in {nak['name']} (Lord: Mars) — Restless kinetic motivation; urge to move, "
            "walk, explore, or conquer outdoor physical environments."
        )
    elif nak_lord == "Venus":
        driver_summary = (
            f"Moon in {nak['name']} (Lord: Venus) — Aesthetic receptivity, social warmth, "
            "indulgence in good food, music, and cozy relational spaces."
        )
    elif nak_lord == "Mercury":
        driver_summary = (
            f"Moon in {nak['name']} (Lord: Mercury) — High conversational agility, witty banter, "
            "intellectual curiosity, and rapid multi-channel information exchange."
        )
    elif nak_lord == "Jupiter":
        driver_summary = (
            f"Moon in {nak['name']} (Lord: Jupiter) — Expansive, grounded perspective, "
            "philosophical clarity, and generous social composure."
        )
    elif nak_lord == "Saturn":
        driver_summary = (
            f"Moon in {nak['name']} (Lord: Saturn) — Serious, structured endurance; favors "
            "practical persistence, duty execution, and measured emotional pacing."
        )
    elif nak_lord == "Sun":
        driver_summary = (
            f"Moon in {nak['name']} (Lord: Sun) — High self-reliance, radiant initiative, "
            "and decisive independent clarity."
        )
    elif nak_lord == "Ketu":
        driver_summary = (
            f"Moon in {nak['name']} (Lord: Ketu) — Intuitive detachment, sudden instinctual shifts, "
            "and craving for low-demand, quiet environments."
        )
    else:
        driver_summary = f"Moon in {nak['name']} (Lord: Moon) — Heightened emotional receptivity and fluid perception."

    # House from Moon context
    house_flavor = ""
    if house_from_moon == 12:
        house_flavor = "House 12 transit: High expenditure of sensory energy, late-night hours, and delayed sleep cycle."
    elif house_from_moon == 2:
        house_flavor = "House 2 transit: Strong focus on culinary enjoyment, speech, dining, and immediate personal resources."
    elif house_from_moon == 3:
        house_flavor = "House 3 transit: High local mobility, short rail/road excursions, and casual camaraderie."
    elif house_from_moon == 5:
        house_flavor = "House 5 transit: Prime recreational vector, spontaneous nightlife, creativity, and romantic play."
    elif house_from_moon == 11:
        house_flavor = "House 11 transit: Expansive social circulation, group gatherings, clubs, and celebratory crowds."

    alert_text = ""
    tactical_advice = ""
    if is_chandrashtama:
        alert_text = (
            f"Transit Moon in {transit_moon['formatted']} (8th from natal Moon). "
            f"Nakshatra: {nak['name']} ({nak_lord}). High emotional variance window."
        )
        tactical_advice = (
            "Heightened cognitive sensitivity today. Keep major irreversible commitments measured; "
            "prioritize trusted companions and allow room for emotional variance."
        )
    else:
        tactical_advice = f"{driver_summary} {house_flavor}".strip()

    return {
        "is_active": is_chandrashtama,
        "house_from_moon": house_from_moon,
        "house_from_lagna": house_from_lagna,
        "transit_moon_sign": transit_moon["sign"],
        "transit_moon_formatted": transit_moon["formatted"],
        "transit_moon_nakshatra": nak["name"],
        "transit_moon_nakshatra_pada": nak["pada"],
        "transit_moon_nakshatra_lord": nak_lord,
        "pct_through_sign": round(pct_in_sign, 1),
        "driver_summary": driver_summary,
        "house_flavor": house_flavor,
        "alert": alert_text,
        "tactical_advice": tactical_advice,
    }


def _detect_kinetic_and_somatic(
    natal: dict[str, Any],
    transits: dict[str, Any],
) -> dict[str, Any]:
    """
    Somatic & Kinetic Vitality Engine.
    Evaluates physical drive, stamina capacity, and manual/athletic output.
    Replaces alarmist injury heuristics with empowering somatic telemetry.
    """
    zodiac = ZODIAC_SIGNS
    lagna_sign = natal["lagna"]["sign"]
    lagna_idx = zodiac.index(lagna_sign)

    def house_for_sign(sign: str) -> int:
        return ((SIGN_TO_INDEX[sign] - lagna_idx) % 12) + 1

    lagna_lord = SIGN_LORDS.get(lagna_sign, "Unknown")
    lagna_lord_transit = transits.get(lagna_lord)
    lagna_lord_house = (
        house_for_sign(lagna_lord_transit["sign"]) if lagna_lord_transit else None
    )

    mars_transit = transits["Mars"]
    mars_sign_idx = mars_transit["sign_index"]
    mars_aspects = _get_parashari_aspects("Mars", mars_sign_idx)

    saturn_transit = transits["Saturn"]
    saturn_sign_idx = saturn_transit["sign_index"]
    saturn_aspects = _get_parashari_aspects("Saturn", saturn_sign_idx)

    lagna_lord_sign_idx = (
        SIGN_TO_INDEX[lagna_lord_transit["sign"]] if lagna_lord_transit else -1
    )

    is_mars_aspecting_lagnesha = lagna_lord_sign_idx in mars_aspects
    is_mars_aspecting_lagna = lagna_idx in mars_aspects
    is_saturn_aspecting_lagnesha = lagna_lord_sign_idx in saturn_aspects

    somatic_vectors: list[str] = []
    stamina_level = "Steady"
    output_capacity = "Normal baseline endurance."
    target_limbs: list[str] = ["Feet", "Legs", "Core"]

    # Kinetic Output Analysis
    if is_mars_aspecting_lagnesha or is_mars_aspecting_lagna:
        stamina_level = "Surging High"
        output_capacity = (
            "Elevated kinetic adrenaline and high physical stamina. Exceptional capacity "
            "for extensive outdoor hiking, high step-counts (20k–35k+), and active physical movement."
        )
        somatic_vectors.append(
            f"Mars ({mars_transit['formatted']}) energizes Lagnesha {lagna_lord} / Ascendant: "
            "High athletic stamina and restless kinetic drive ready for discharge."
        )

    if is_saturn_aspecting_lagnesha:
        somatic_vectors.append(
            f"Saturn ({saturn_transit['formatted']}) aspects Lagnesha {lagna_lord}: "
            "High structural endurance under sustained, repetitive physical loading."
        )

    if lagna_lord_house == 6:
        somatic_vectors.append(
            f"Lagnesha {lagna_lord} transiting House 6 ({lagna_lord_transit['sign']}): "
            "Active Seva Bhāva — disciplined execution of operational shifts or routine service duties."
        )

    # Friendly advice
    if stamina_level == "Surging High":
        tactical_advice = (
            "Kinetic reserves are exceptionally high. Excellent window for outdoor terrain, "
            "long walking expeditions, or intense physical discharge. Hydrate and maintain pacing."
        )
    else:
        tactical_advice = "Physical baseline is steady. Balance physical output with adequate muscular recovery."

    # For UI backwards compatibility:
    is_active = bool(somatic_vectors)
    risk_level = (
        "Elevated"
        if (is_mars_aspecting_lagnesha and lagna_lord_house == 6)
        else "Steady"
    )
    status_label = f"Kinetic Output: {stamina_level}"
    step_endurance_rating = 9 if stamina_level == "Surging High" else 6

    return {
        "is_active": is_active,
        "stamina_level": stamina_level,
        "status_label": status_label,
        "step_endurance_rating": step_endurance_rating,
        "output_capacity": output_capacity,
        "lagnesha": lagna_lord,
        "lagnesha_transit": (
            lagna_lord_transit["formatted"] if lagna_lord_transit else "N/A"
        ),
        "lagnesha_transit_house": lagna_lord_house,
        "in_house_6": lagna_lord_house == 6,
        "risk_level": risk_level,
        "target_limbs": target_limbs,
        "somatic_vectors": somatic_vectors,
        "alert": somatic_vectors[0] if somatic_vectors else "",
        "tactical_advice": tactical_advice,
    }


def _detect_recreation_and_social(
    natal: dict[str, Any],
    transits: dict[str, Any],
    moon_state: dict[str, Any],
) -> dict[str, Any]:
    """
    Recreational, Social, Nightlife & Mobility Engine (5th, 11th, 3rd, Venus & Rahu).
    Maps real-world nightlife, club access dynamics, short-range travel, and dining.
    """
    zodiac = ZODIAC_SIGNS
    lagna_sign = natal["lagna"]["sign"]
    lagna_idx = zodiac.index(lagna_sign)

    def house_for_sign(sign: str) -> int:
        return ((SIGN_TO_INDEX[sign] - lagna_idx) % 12) + 1

    venus_transit = transits["Venus"]
    saturn_transit = transits["Saturn"]
    mars_transit = transits["Mars"]

    venus_house = house_for_sign(venus_transit["sign"])
    venus_is_strong = venus_transit["sign"] in ["Taurus", "Libra", "Pisces"]

    # 11th house (social gatherings, clubs, collective spaces)
    h11_sign_idx = (lagna_idx + 10) % 12
    saturn_aspects = _get_parashari_aspects("Saturn", saturn_transit["sign_index"])
    saturn_on_11th = (saturn_transit["sign_index"] == h11_sign_idx) or (
        h11_sign_idx in saturn_aspects
    )

    # 3rd house (short travel, trains, local excursions)
    h3_sign_idx = (lagna_idx + 2) % 12
    h3_active = (transits["Moon"]["sign_index"] == h3_sign_idx) or (
        mars_transit["sign_index"] == h3_sign_idx
    )

    # Nightlife & Nocturnal Stimulation Vector
    moon_nak_lord = moon_state.get("transit_moon_nakshatra_lord")
    nightlife_active = (moon_nak_lord == "Rahu") or (
        venus_is_strong
        and (moon_state["house_from_moon"] in [5, 11, 12] or venus_house in [5, 11, 12])
    )

    social_signals: list[str] = []
    if nightlife_active:
        social_signals.append(
            "Rahu/Venus nocturnal excitation: Strong pull toward evening celebration, "
            "music, nightlife, late-hour urban wandering, and social exploration."
        )

    if saturn_on_11th:
        social_signals.append(
            "Saturnian 11th-house gatekeeping: Friction or selective entry at social venues "
            "(door policies, bouncer resistance, initial venue rejections). Requires persistence to find the right room."
        )

    if h3_active or moon_state["house_from_moon"] == 3:
        social_signals.append(
            "3rd House mobility active: Spontaneous short-range travel, regional rail trips, "
            "and outdoor trails / hiking routes favored."
        )

    # Culinary Vector (2nd house dynamics)
    culinary_active = (
        moon_state["house_from_lagna"] == 2
        or moon_state["house_from_moon"] == 2
        or venus_is_strong
    )
    culinary_desc = ""
    if culinary_active:
        culinary_desc = "Strong 2nd-house sensory nourishment: High appreciation for cozy dining, foreign/Asian flavors, and quality post-exertion meals."

    tactical_advice = ""
    if social_signals:
        tactical_advice = " ".join(social_signals)
    else:
        tactical_advice = "Social baseline is balanced. Good rhythm for steady interpersonal interactions."

    return {
        "is_active": bool(social_signals),
        "nightlife_active": nightlife_active,
        "saturn_gatekeeper_active": saturn_on_11th,
        "mobility_active": h3_active or moon_state["house_from_moon"] == 3,
        "culinary_active": culinary_active,
        "culinary_desc": culinary_desc,
        "social_signals": social_signals,
        "tactical_advice": tactical_advice,
    }


def _detect_mercury_flow(transits: dict[str, Any]) -> dict[str, Any]:
    """
    Cognitive & Communication Fluidity Engine (Budha Matrix).
    Evaluates banter, logistics, mental speed, and Sandhi transition zones.
    """
    mercury = transits["Mercury"]
    deg_in_sign = mercury["degree_in_sign"]

    is_end_zone = deg_in_sign >= 28.75
    is_beginning_zone = deg_in_sign <= 1.25
    is_sandhi = is_end_zone or is_beginning_zone

    sandhi_type = ""
    if is_end_zone:
        sandhi_type = f"End-zone Sandhi ({deg_in_sign:.2f}° in {mercury['sign']})"
    elif is_beginning_zone:
        sandhi_type = f"Beginning-zone Sandhi ({deg_in_sign:.2f}° in {mercury['sign']})"

    if is_sandhi:
        alert_text = (
            f"Mercury at {mercury['formatted']} ({sandhi_type}) — Communication latency zone. "
            "Expect recruiter response delays, mild logistical detours, or slow email turnaround."
        )
        tactical_advice = "Patience with bureaucratic/recruiter responses. Double-check transit tickets and follow up in writing."
    else:
        alert_text = (
            f"Mercury at {mercury['formatted']} — High conversational agility. "
            "Excellent flow for tactical banter, social roasting, quick negotiation, and clear intellectual synthesis."
        )
        tactical_advice = "Communication channels are rapid and sharp. Great window for witty dialogue and problem solving."

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
    Computes the Full-Spectrum 24-Hour Daily Transit & Incident Radar.

    Integrates:
    1. Lunar Mind Matrix (Chandra Bhāva, Nakshatra Driver & Chandrashtama)
    2. Somatic & Kinetic Vitality (Mars & Lagnesha Stamina, Hiking/Step Capacity)
    3. Recreational & Social Drivers (5th/11th House, Rahu/Venus Nightlife & Gatekeeping)
    4. Communication Fluidity (Budha Banter & Recruiter Latency Index)

    Maintains 100% backwards-compatibility with existing HUD UI contracts while
    providing realistic, empowering full-spectrum life intelligence.
    """
    if target_dt is None:
        target_dt = datetime.utcnow()

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    transits = _get_transits(target_dt)

    natal_moon_sign = natal["planets"]["Moon"]["sign"]
    natal_lagna_sign = natal["lagna"]["sign"]

    moon_state = _detect_lunar_state(transits, natal_moon_sign, natal_lagna_sign)
    kinetic_state = _detect_kinetic_and_somatic(natal, transits)
    social_state = _detect_recreation_and_social(natal, transits, moon_state)
    mercury_state = _detect_mercury_flow(transits)

    # Consolidated Tactical Advice List
    all_advice: list[str] = []
    if social_state["tactical_advice"]:
        all_advice.append(social_state["tactical_advice"])
    if kinetic_state["tactical_advice"]:
        all_advice.append(kinetic_state["tactical_advice"])
    if moon_state["tactical_advice"]:
        all_advice.append(moon_state["tactical_advice"])
    if mercury_state["tactical_advice"]:
        all_advice.append(mercury_state["tactical_advice"])

    # Determine Day Archetype Flavor
    if (
        social_state["nightlife_active"]
        and kinetic_state["stamina_level"] == "Surging High"
    ):
        archetype_flavor = "Recreational Exploration & High-Output Kinetic Drive"
        status_label = "High Kinetic Energy & Nocturnal Social Exploration"
        overall_status = "ELEVATED"
    elif kinetic_state["stamina_level"] == "Surging High":
        archetype_flavor = "High Physical Endurance & Active Mobility"
        status_label = "High Kinetic Output Active"
        overall_status = "SINGLE_ACTIVE"
    elif social_state["nightlife_active"]:
        archetype_flavor = "Social Circulation & Nocturnal Vibe"
        status_label = "Social & Recreational Pulse Active"
        overall_status = "SINGLE_ACTIVE"
    elif moon_state["is_active"]:
        archetype_flavor = "Inward Emotional Introspection (Chandrāṣṭama)"
        status_label = "Chandrāṣṭama Sensitivity Active"
        overall_status = "SINGLE_ACTIVE"
    else:
        archetype_flavor = "Balanced Execution & Grounded Flow"
        status_label = "All Clear — Fluid Flow"
        overall_status = "CLEAR"

    active_count = sum(
        [
            moon_state["is_active"],
            social_state["nightlife_active"],
            kinetic_state["stamina_level"] == "Surging High",
            mercury_state["is_active"],
        ]
    )

    now_utc = datetime.utcnow()
    same_calendar_day = target_dt.date() == now_utc.date()
    return {
        "generated_at": target_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "as_of_date": target_dt.strftime("%Y-%m-%d"),
        "as_of_label": "today" if same_calendar_day else "other_day",
        "overall_status": overall_status,
        "overall_status_label": status_label,
        "archetype_flavor": archetype_flavor,
        "active_vector_count": active_count,
        # Core Sub-Systems
        "chandrashtama": moon_state,
        "somatic_injury": kinetic_state,
        "mercury_sandhi": mercury_state,
        "recreation_social": social_state,
        # Consolidated Synthesis
        "tactical_advice": all_advice,
        "ephemeris_timestamp": target_dt.isoformat(),
        "freshness_hint": "latest",
    }
