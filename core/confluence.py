"""
karmic-ledger: Astrological Event-Domain Confluence Engine
Evaluates mathematical consistency between active Dasha lords, transit degree-aspects (Gochar),
Sarvashtakavarga (SAV) house bindus, and classical Parashari Bhava signatures.
Treats all outputs as symbolic heuristics with input-sensitivity metrics, never physical causation.
"""

from typing import Any

from core.ashtakavarga import (
    compute_sarvashtakavarga,
    get_ashtakavarga_house_multiplier,
)

ZODIAC_SIGNS = [
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

SIGN_LORDS = {
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

# Special aspects (offset from occupied house, 1-indexed)
PLANET_ASPECT_OFFSETS = {
    "Sun": [1, 7],
    "Moon": [1, 7],
    "Mercury": [1, 7],
    "Venus": [1, 7],
    "Mars": [1, 4, 7, 8],
    "Jupiter": [1, 5, 7, 9],
    "Saturn": [1, 3, 7, 10],
    "Rahu": [1, 5, 7, 9],
    "Ketu": [1, 5, 7, 9],
}

# Angular aspect offsets in degrees for exact orb calculations
PLANET_ASPECT_DEGREES = {
    "Sun": [0.0, 180.0],
    "Moon": [0.0, 180.0],
    "Mercury": [0.0, 180.0],
    "Venus": [0.0, 180.0],
    "Mars": [0.0, 90.0, 180.0, 210.0],
    "Jupiter": [0.0, 120.0, 180.0, 240.0],
    "Saturn": [0.0, 60.0, 180.0, 270.0],
    "Rahu": [0.0, 120.0, 180.0, 240.0],
    "Ketu": [0.0, 120.0, 180.0, 240.0],
}


def calculate_angular_orb(deg1: float, deg2: float) -> float:
    """Computes shortest angular distance between two ecliptic longitudes (0 to 180°)."""
    diff = abs(deg1 - deg2) % 360.0
    return 360.0 - diff if diff > 180.0 else diff


def get_min_aspect_orb(transit_lon: float, planet: str, target_lon: float) -> float:
    """Computes minimum angular deviation from exact Parashari aspect angle."""
    offsets = PLANET_ASPECT_DEGREES.get(planet, [0.0, 180.0])
    min_orb = 360.0
    for off in offsets:
        aspect_point = (target_lon + off) % 360.0
        dist = calculate_angular_orb(transit_lon, aspect_point)
        min_orb = min(min_orb, dist)
    return min_orb


def classify_event_domain(
    event_name: str, category_hint: str = None, is_historical_benchmark: bool = False
) -> str:
    """
    Classifies an event text into an astrological domain.
    EPISTEMIC SAFETY MANDATE:
    Domains involving mortality (death/demise/assassination) and legal incarceration (jail/prison)
    are strictly restricted to closed, retrospective historical archives (is_historical_benchmark=True).
    For any living or non-historical profile, these are hard-remapped to abstract symbolic resilience
    or transformation cycles, preventing fatalistic or judicial claims.
    """
    name_lower = event_name.lower()
    hint_lower = (category_hint or "").lower()

    # Incarceration / Confinement
    if any(
        k in name_lower or k in hint_lower
        for k in [
            "imprisonment",
            "prison",
            "sentenced",
            "incarceration",
            "jail",
            "captivity",
            "hostage",
        ]
    ):
        if is_historical_benchmark:
            return "INCARCERATION_OR_BANDHANA"
        return "STRUCTURAL_CONFINEMENT_OR_DISCIPLINE"

    # Mortality / Bereavement
    if any(
        k in name_lower or k in hint_lower
        for k in [
            "assassination",
            "demise",
            "death",
            "killed",
            "bereavement",
            "funeral",
            "fatal",
            "mortality",
        ]
    ):
        if "mother" in name_lower or "maternal" in name_lower:
            return (
                "MATERNAL_BEREAVEMENT"
                if is_historical_benchmark
                else "FAMILY_AXIS_RESTRUCTURING"
            )
        elif "father" in name_lower or "paternal" in name_lower:
            return (
                "PATERNAL_BEREAVEMENT"
                if is_historical_benchmark
                else "FAMILY_AXIS_RESTRUCTURING"
            )
        return (
            "MORTALITY_CRISIS"
            if is_historical_benchmark
            else "TRANSFORMATIVE_CROSSING_WINDOW"
        )

    # Acute Disease / Health Crisis / Surgical Intervention
    if any(
        k in name_lower or k in hint_lower
        for k in [
            "surgery",
            "illness",
            "disease",
            "hospital",
            "hospitalization",
            "cancer",
            "medical",
            "operation",
            "diagnosis",
            "infection",
            "ailment",
            "stroke",
            "infarct",
            "pathology",
            "tumor",
        ]
    ):
        if is_historical_benchmark:
            return "HEALTH_CRISIS_OR_ROGA"
        return "SOMATIC_AWARENESS_WINDOW"

    # Relational Friction / Crisis / Marriage (Domain 01 Structural Fix)
    if any(
        k in name_lower or k in hint_lower
        for k in [
            "divorce",
            "separation",
            "infidelity",
            "affair",
            "cheating",
            "breakup",
            "heartbreak",
            "marital discord",
            "marital crisis",
        ]
    ):
        if is_historical_benchmark:
            return "RELATIONAL_CRISIS_OR_VIVIDHA"
        return "RELATIONAL_COMMUNICATION_AND_BOUNDARIES"

    if any(
        k in name_lower or k in hint_lower
        for k in [
            "marriage",
            "wedding",
            "proposed",
            "relationship",
            "romance",
            "engaged",
        ]
    ):
        if is_historical_benchmark:
            return "MARRIAGE_OR_RELATIONSHIP"
        return "RELATIONAL_COMMUNICATION_AND_BOUNDARIES"

    if any(
        k in name_lower or k in hint_lower
        for k in [
            "relocation",
            "foreign",
            "canada",
            "germany",
            "abroad",
            "visa",
            "departure",
            "move",
            "london",
        ]
    ):
        return "FOREIGN_RELOCATION"

    if any(
        k in name_lower or k in hint_lower
        for k in [
            "fired",
            "termination",
            "loss of office",
            "defeat",
            "chhidra",
            "bust",
            "arrest",
            "emergency",
        ]
    ):
        return "CAREER_OR_STATUS_LOSS"

    if any(
        k in name_lower or k in hint_lower
        for k in [
            "prime minister",
            "sworn in",
            "job",
            "financial advisor",
            "bank",
            "elevation",
            "launch",
            "startup",
            "promotion",
            "election",
            "power",
            "return to power",
            "ipo",
            "career",
            "release from prison",
            "freedom",
        ]
    ):
        return "CAREER_OR_POWER_ELEVATION"

    if any(
        k in name_lower or k in hint_lower
        for k in [
            "marriage",
            "wedding",
            "proposed",
            "relationship",
            "romance",
            "engaged",
        ]
    ):
        return "MARRIAGE_OR_RELATIONSHIP"

    if any(
        k in name_lower or k in hint_lower
        for k in [
            "12th",
            "degree",
            "graduation",
            "bachelor",
            "master",
            "thesis",
            "school",
            "college",
            "bca",
            "mca",
            "education",
        ]
    ):
        return "ACADEMIC_COMPLETION"

    return "GENERAL_SIGNIFICANT_EVENT"


def evaluate_event_confluence(
    natal: dict[str, Any],
    dasha_active: dict[str, Any],
    transits_active: dict[str, Any],
    event_name: str,
    category_hint: str = None,
    is_historical_benchmark: bool = False,
) -> dict[str, Any]:
    """
    Computes Heuristic Consistency Score (HCS) for a single milestone.
    Evaluates active Dasha lords, exact degree-level transit orbs (Gochar),
    and Sarvashtakavarga (SAV) bindu vitality.
    """
    lagna_sign = natal["lagna"]["sign"]
    lagna_deg = float(natal["lagna"]["longitude"])
    lagna_idx = ZODIAC_SIGNS.index(lagna_sign)

    def sign_for_house(h: int) -> str:
        return ZODIAC_SIGNS[(lagna_idx + h - 1) % 12]

    def house_for_sign(s: str) -> int:
        return ((ZODIAC_SIGNS.index(s) - lagna_idx) % 12) + 1

    # Map house numbers to ruling planets
    house_lords: dict[int, str] = {
        h: SIGN_LORDS[sign_for_house(h)] for h in range(1, 13)
    }

    # Map planets to houses owned
    planet_owned_houses: dict[str, list[int]] = {}
    for h, lord in house_lords.items():
        planet_owned_houses.setdefault(lord, []).append(h)
    planet_owned_houses.setdefault("Rahu", []).append(house_for_sign("Aquarius"))
    planet_owned_houses.setdefault("Ketu", []).append(house_for_sign("Scorpio"))

    # Map planets to natal house occupied and longitude
    planet_natal_house: dict[str, int] = {
        p_name: p_val["house"] for p_name, p_val in natal["planets"].items()
    }
    planet_natal_lon: dict[str, float] = {
        p_name: float(p_val["longitude"]) for p_name, p_val in natal["planets"].items()
    }

    def houses_aspected_by(planet: str, from_house: int) -> list[int]:
        offsets = PLANET_ASPECT_OFFSETS.get(planet, [1, 7])
        return [((from_house + off - 2) % 12) + 1 for off in offsets]

    domain = classify_event_domain(
        event_name=event_name,
        category_hint=category_hint,
        is_historical_benchmark=is_historical_benchmark,
    )

    # Safety Interceptor: Enforce hard restriction even if category_hint forced a restricted domain
    if not is_historical_benchmark:
        if domain in ["RELATIONAL_CRISIS_OR_VIVIDHA", "MARRIAGE_OR_RELATIONSHIP"]:
            domain = "RELATIONAL_COMMUNICATION_AND_BOUNDARIES"
        elif domain == "INCARCERATION_OR_BANDHANA":
            domain = "STRUCTURAL_CONFINEMENT_OR_DISCIPLINE"
        elif domain == "MORTALITY_CRISIS":
            domain = "TRANSFORMATIVE_CROSSING_WINDOW"
        elif domain in ["MATERNAL_BEREAVEMENT", "PATERNAL_BEREAVEMENT"]:
            domain = "FAMILY_AXIS_RESTRUCTURING"
        elif domain == "HEALTH_CRISIS_OR_ROGA":
            domain = "SOMATIC_AWARENESS_WINDOW"

    domain_rules = {
        "RELATIONAL_CRISIS_OR_VIVIDHA": {
            "primary_houses": [7, 6, 8],
            "secondary_houses": [12, 1],
            "karakas": ["Venus", "Mars", "Rahu"],
            "shastra": "BPHS 18:14-22 (Historical Archive: Kalatra Dosha & Stri-Sangha Vividha)",
        },
        "RELATIONAL_COMMUNICATION_AND_BOUNDARIES": {
            "primary_houses": [7, 1, 9],
            "secondary_houses": [5, 11],
            "karakas": ["Venus", "Jupiter", "Mercury"],
            "shastra": "Parampara Jyotish: Symbolic Interpersonal Dynamics & Relational Boundaries (Zero Predictive Outcome/Marital Diagnosis)",
        },
        "HEALTH_CRISIS_OR_ROGA": {
            "primary_houses": [6, 8, 12],
            "secondary_houses": [1, 2, 7],
            "karakas": ["Mars", "Saturn", "Rahu"],
            "shastra": "BPHS 13:1-15 (Historical Archive: Roga & Chikitsa Nirupana)",
        },
        "SOMATIC_AWARENESS_WINDOW": {
            "primary_houses": [1, 6, 9],
            "secondary_houses": [5, 11],
            "karakas": ["Sun", "Jupiter", "Moon"],
            "shastra": "Ayur-Jyotish: Symbolic Somatic Equilibrium & Restorative Vitality (Zero Clinical Diagnostic Claim)",
        },
        "INCARCERATION_OR_BANDHANA": {
            "primary_houses": [12, 6, 8],
            "secondary_houses": [1, 10],
            "karakas": ["Saturn", "Rahu", "Ketu"],
            "shastra": "BPHS 39:1-12 (Historical Archive: Bandhana Yoga & Confinement)",
        },
        "STRUCTURAL_CONFINEMENT_OR_DISCIPLINE": {
            "primary_houses": [10, 8, 9],
            "secondary_houses": [1, 5],
            "karakas": ["Saturn", "Jupiter"],
            "shastra": "Parampara Jyotish: Symbolic Discipline & Restraint Theme",
        },
        "FOREIGN_RELOCATION": {
            "primary_houses": [12, 9, 3],
            "secondary_houses": [7, 1],
            "karakas": ["Rahu", "Moon", "Saturn"],
            "shastra": "BPHS 12:8 (Vyaya Bhava & Mleccha Yatra)",
        },
        "MORTALITY_CRISIS": {
            "primary_houses": [2, 7, 8],
            "secondary_houses": [12, 6, 1],
            "karakas": ["Saturn", "Mars", "Rahu", "Ketu"],
            "shastra": "BPHS 43:2-10 (Historical Archive: Maraka & Ayur Nirupana)",
        },
        "TRANSFORMATIVE_CROSSING_WINDOW": {
            "primary_houses": [8, 9, 5],
            "secondary_houses": [1, 10],
            "karakas": ["Jupiter", "Sun"],
            "shastra": "Parampara Jyotish: Symbolic Transformation & Recalibration Theme",
        },
        "MATERNAL_BEREAVEMENT": {
            "primary_houses": [4, 10, 5],
            "secondary_houses": [8, 12],
            "karakas": ["Moon", "Saturn", "Rahu"],
            "shastra": "BPHS 11:14 (Historical Archive: Matru Bhava Nasha)",
        },
        "PATERNAL_BEREAVEMENT": {
            "primary_houses": [9, 3],
            "secondary_houses": [8, 12],
            "karakas": ["Sun", "Saturn", "Rahu"],
            "shastra": "BPHS 12:4 (Historical Archive: Pitru Bhava Nasha)",
        },
        "FAMILY_AXIS_RESTRUCTURING": {
            "primary_houses": [4, 9, 5],
            "secondary_houses": [1, 10],
            "karakas": ["Sun", "Moon", "Jupiter"],
            "shastra": "Parampara Jyotish: Lineage Transition & Family Axis Recalibration",
        },
        "CAREER_OR_STATUS_LOSS": {
            "primary_houses": [10, 8, 12],
            "secondary_houses": [6, 1],
            "karakas": ["Saturn", "Rahu", "Ketu"],
            "shastra": "BPHS 54:31 (Rajyabhransha & Chhidra Dasha)",
        },
        "CAREER_OR_POWER_ELEVATION": {
            "primary_houses": [10, 1, 11],
            "secondary_houses": [9, 2, 5],
            "karakas": ["Sun", "Jupiter", "Mercury", "Mars"],
            "shastra": "BPHS 35:12 (Raja Yoga & Simhasana Adhikara)",
        },
        "MARRIAGE_OR_RELATIONSHIP": {
            "primary_houses": [7, 2],
            "secondary_houses": [11, 5],
            "karakas": ["Venus", "Jupiter"],
            "shastra": "BPHS 18:6 (Kalatra Bhava Vivaha Yoga)",
        },
        "ACADEMIC_COMPLETION": {
            "primary_houses": [4, 5, 9],
            "secondary_houses": [1, 10, 11],
            "karakas": ["Mercury", "Jupiter"],
            "shastra": "Phaladeepika 6:22 (Vidya Prapti)",
        },
        "GENERAL_SIGNIFICANT_EVENT": {
            "primary_houses": [1, 10, 9],
            "secondary_houses": [5, 11],
            "karakas": ["Jupiter", "Saturn"],
            "shastra": "Parampara Jyotish Shastra",
        },
    }

    cfg = domain_rules.get(domain, domain_rules["GENERAL_SIGNIFICANT_EVENT"])
    target_primary = cfg["primary_houses"]
    target_secondary = cfg["secondary_houses"]
    target_karakas = cfg["karakas"]

    md_planet = dasha_active.get("mahadasha", "")
    ad_planet = dasha_active.get("antardasha", "")

    confluence_factors: list[str] = []

    # -------------------------------------------------------------------------
    # 1. MAHADASHA LORD EVALUATION (Max 40 points)
    # -------------------------------------------------------------------------
    md_score = 0.0
    md_aspected_h = []
    if md_planet:
        md_houses_owned = planet_owned_houses.get(md_planet, [])
        md_natal_h = planet_natal_house.get(md_planet, 0)
        md_aspected_h = houses_aspected_by(md_planet, md_natal_h) if md_natal_h else []

        # Primary house ownership
        owned_primary = [h for h in md_houses_owned if h in target_primary]
        if owned_primary:
            md_score += 24.0
            confluence_factors.append(
                f"Mahadasha Lord {md_planet} owns primary house H{owned_primary[0]}"
            )
        elif any(h in target_secondary for h in md_houses_owned):
            md_score += 5.0
            confluence_factors.append(
                f"Mahadasha Lord {md_planet} owns secondary supporting house"
            )

        # Placement
        if md_natal_h in target_primary:
            md_score += 14.0
            confluence_factors.append(
                f"Mahadasha Lord {md_planet} occupies primary house H{md_natal_h}"
            )
        elif any(h in target_primary for h in md_aspected_h):
            md_score += 9.0
            confluence_factors.append(
                f"Mahadasha Lord {md_planet} casts classical Drishti on primary house"
            )

        # Karaka status (only credited if planet has some house mandate or sambandha)
        if md_planet in target_karakas and (
            owned_primary
            or md_natal_h in target_primary
            or any(h in target_primary for h in md_aspected_h)
        ):
            md_score += 6.0
            confluence_factors.append(
                f"Mahadasha Lord {md_planet} holds natural Karakatva for {domain}"
            )

    md_score = min(md_score, 40.0)

    # -------------------------------------------------------------------------
    # 2. ANTARDASHA LORD EVALUATION (Max 40 points)
    # -------------------------------------------------------------------------
    ad_score = 0.0
    ad_aspected_h = []
    if ad_planet:
        ad_houses_owned = planet_owned_houses.get(ad_planet, [])
        ad_natal_h = planet_natal_house.get(ad_planet, 0)
        ad_aspected_h = houses_aspected_by(ad_planet, ad_natal_h) if ad_natal_h else []

        owned_primary = [h for h in ad_houses_owned if h in target_primary]
        if owned_primary:
            ad_score += 24.0
            confluence_factors.append(
                f"Antardasha Lord {ad_planet} owns primary house H{owned_primary[0]}"
            )
        elif any(h in target_secondary for h in ad_houses_owned):
            ad_score += 5.0
            confluence_factors.append(
                f"Antardasha Lord {ad_planet} owns secondary supporting house"
            )

        if ad_natal_h in target_primary:
            ad_score += 14.0
            confluence_factors.append(
                f"Antardasha Lord {ad_planet} occupies primary house H{ad_natal_h}"
            )
        elif any(h in target_primary for h in ad_aspected_h):
            ad_score += 9.0
            confluence_factors.append(
                f"Antardasha Lord {ad_planet} casts classical Drishti on primary house"
            )

        if ad_planet in target_karakas and (
            owned_primary
            or ad_natal_h in target_primary
            or any(h in target_primary for h in ad_aspected_h)
        ):
            ad_score += 6.0
            confluence_factors.append(
                f"Antardasha Lord {ad_planet} holds natural Karakatva for {domain}"
            )

        # Sambandha: Check if AD lord is conjunct or aspected by MD lord
        if md_planet and ad_natal_h:
            md_natal_h = planet_natal_house.get(md_planet, 0)
            if md_natal_h == ad_natal_h:
                ad_score += 5.0
                confluence_factors.append(
                    f"MD Lord {md_planet} and AD Lord {ad_planet} form exact Sambandha in H{ad_natal_h}"
                )
            elif ad_natal_h in houses_aspected_by(md_planet, md_natal_h):
                ad_score += 4.0
                confluence_factors.append(
                    f"MD Lord {md_planet} casts mutual Parashari aspect onto AD Lord {ad_planet}"
                )

    ad_score = min(ad_score, 40.0)

    # -------------------------------------------------------------------------
    # 3. TRANSIT CONFLUENCE WITH NAVAMSHA PADA ORB LOCK & ASHTAKAVARGA WEIGHTING
    # -------------------------------------------------------------------------
    transit_score = 0.0

    # Compute Sarvashtakavarga bindu matrix
    sav_data = compute_sarvashtakavarga(natal)
    sav_by_house = sav_data["sav_by_house"]

    # Target sensitive ecliptic longitudes for the primary domain
    target_longitudes: list[float] = [lagna_deg]
    for ph in target_primary:
        # Exact house cusp
        target_longitudes.append((lagna_deg + (ph - 1) * 30.0) % 360.0)
        # Any natal planets in primary house
        for p_name, h_occ in planet_natal_house.items():
            if h_occ == ph and p_name in planet_natal_lon:
                target_longitudes.append(planet_natal_lon[p_name])

    if transits_active and "Saturn" in transits_active and "Jupiter" in transits_active:
        t_sat = transits_active["Saturn"]
        t_sat_lon = float(t_sat["longitude"])
        t_sat_h = house_for_sign(t_sat["sign"])
        t_sat_aspects = houses_aspected_by("Saturn", t_sat_h)

        t_jup = transits_active["Jupiter"]
        t_jup_lon = float(t_jup["longitude"])
        t_jup_h = house_for_sign(t_jup["sign"])
        t_jup_aspects = houses_aspected_by("Jupiter", t_jup_h)

        # 3.1 SATURN TRANSIT IMPACT (Max 13 points scaled by orb & bindus)
        sat_hits_primary = (t_sat_h in target_primary) or any(
            h in target_primary for h in t_sat_aspects
        )
        if sat_hits_primary:
            # Measure exact minimum aspect orb against target longitudes
            sat_min_orb = min(
                get_min_aspect_orb(t_sat_lon, "Saturn", t_lon)
                for t_lon in target_longitudes
            )

            # Navamsha Pada Orb Scaling (3°20' = 3.333°)
            if sat_min_orb <= 3.3333:
                sat_orb_weight = 1.0  # Exact Pada Lock
                confluence_factors.append(
                    f"Transit Saturn tight Pada Orb Lock ({sat_min_orb:.1f}° deviation)"
                )
            elif sat_min_orb <= 7.0:
                sat_orb_weight = 0.5 + 0.5 * (1.0 - (sat_min_orb - 3.3333) / 3.6667)
            elif sat_min_orb <= 12.0:
                sat_orb_weight = 0.25  # Broad sign background
            else:
                sat_orb_weight = 0.10  # Out-of-orb whole-sign artifact

            # Ashtakavarga multiplier for transit sign
            sat_bindus = sav_by_house.get(t_sat_h, 28)
            sat_bindu_mult = get_ashtakavarga_house_multiplier(sat_bindus)

            base_sat_points = 13.0 if t_sat_h in target_primary else 9.0
            transit_score += base_sat_points * sat_orb_weight * sat_bindu_mult
            confluence_factors.append(
                f"Transit Saturn H{t_sat_h} SAV Bindus: {sat_bindus} (mult: {sat_bindu_mult:.2f}x)"
            )

        # 3.2 JUPITER TRANSIT IMPACT (Max 12 points scaled by orb & bindus)
        jup_hits_primary = (t_jup_h in target_primary) or any(
            h in target_primary for h in t_jup_aspects
        )
        if jup_hits_primary:
            jup_min_orb = min(
                get_min_aspect_orb(t_jup_lon, "Jupiter", t_lon)
                for t_lon in target_longitudes
            )

            if jup_min_orb <= 3.3333:
                jup_orb_weight = 1.0
                confluence_factors.append(
                    f"Transit Jupiter tight Pada Orb Lock ({jup_min_orb:.1f}° deviation)"
                )
            elif jup_min_orb <= 7.0:
                jup_orb_weight = 0.5 + 0.5 * (1.0 - (jup_min_orb - 3.3333) / 3.6667)
            elif jup_min_orb <= 12.0:
                jup_orb_weight = 0.25
            else:
                jup_orb_weight = 0.10

            jup_bindus = sav_by_house.get(t_jup_h, 28)
            jup_bindu_mult = get_ashtakavarga_house_multiplier(jup_bindus)

            base_jup_points = 12.0 if t_jup_h in target_primary else 8.0
            transit_score += base_jup_points * jup_orb_weight * jup_bindu_mult
            confluence_factors.append(
                f"Transit Jupiter H{t_jup_h} SAV Bindus: {jup_bindus} (mult: {jup_bindu_mult:.2f}x)"
            )

    transit_score = min(transit_score, 25.0)

    # -------------------------------------------------------------------------
    # 4. CONFLUENCE SYNTHESIS & ADVERSARIAL DISCRIMINATION
    # -------------------------------------------------------------------------
    raw_confluence = md_score + ad_score + transit_score

    # Synergistic check taking into account ownership, placement, AND classical Drishti
    has_primary_md = (
        any(h in target_primary for h in planet_owned_houses.get(md_planet, []))
        or (planet_natal_house.get(md_planet, 0) in target_primary)
        or any(h in target_primary for h in md_aspected_h)
    )
    has_primary_ad = (
        any(h in target_primary for h in planet_owned_houses.get(ad_planet, []))
        or (planet_natal_house.get(ad_planet, 0) in target_primary)
        or any(h in target_primary for h in ad_aspected_h)
    )

    if has_primary_md and has_primary_ad:
        raw_confluence += 12.0
        confluence_factors.append(
            "Dual Dasha Confluence: Both Mahadasha & Antardasha hold jurisdictional mandate"
        )
    elif not has_primary_md and not has_primary_ad:
        # Severe penalty if neither dasha lord governs or aspects primary event houses
        raw_confluence = min(raw_confluence * 0.55, 38.0)
        confluence_factors.append(
            "Primary House Void: Neither Dasha lord rules, occupies, or aspects primary event houses"
        )

    if "error" in dasha_active:
        raw_confluence = 5.0
        confluence_factors.append("Dasha timeline out of astronomical range")

    vcs = round(max(min(raw_confluence, 98.0), 15.0), 1)

    if not is_historical_benchmark:
        sanitized_factors = []
        for factor in confluence_factors:
            f_clean = factor
            for old_term, safe_term in [
                ("MORTALITY_CRISIS", "TRANSFORMATIVE_CROSSING_WINDOW"),
                ("HEALTH_CRISIS_OR_ROGA", "SOMATIC_AWARENESS_WINDOW"),
                ("INCARCERATION_OR_BANDHANA", "STRUCTURAL_CONFINEMENT_OR_DISCIPLINE"),
                (
                    "RELATIONAL_CRISIS_OR_VIVIDHA",
                    "RELATIONAL_COMMUNICATION_AND_BOUNDARIES",
                ),
                ("MARRIAGE_OR_RELATIONSHIP", "RELATIONAL_COMMUNICATION_AND_BOUNDARIES"),
                ("Maraka", "Developmental Cycle"),
                ("Roga", "Somatic Balance"),
                ("Bandhana", "Discipline Cycle"),
                ("Kalatra Dosha", "Relational Boundaries"),
            ]:
                f_clean = f_clean.replace(old_term, safe_term)
            sanitized_factors.append(f_clean)
        confluence_factors = sanitized_factors

    return {
        "event": event_name,
        "domain": domain,
        "confluence_score": vcs,
        "shastra_citation": cfg["shastra"],
        "confluence_mechanics": confluence_factors,
        "scores_breakdown": {
            "mahadasha_score": round(md_score, 1),
            "antardasha_score": round(ad_score, 1),
            "transit_score": round(transit_score, 1),
        },
    }
