"""
karmic-ledger: Symbolic Transit Strain & Friction Indices Engine
Evaluates geometric planetary transit tensions and Vimshottari dasha cycles as
abstract archetypal strain themes (e.g. structural career evaluation, foreign-domain
unfamiliarity, commitment boundary testing).

Strict Epistemic Primacy:
Zero assertions of real-world bureaucratic, legal, medical, or relational events.
No claims of visa invalidation, job loss, marriage status, or physiological diagnoses.
Astrology is treated as symbolic reflection and pattern language, never factual diagnosis.
"""

from datetime import datetime
from typing import Any

from core.transits import get_planet_transit_positions


def audit_live_frictions(
    natal: dict[str, Any], timeline: list[dict[str, Any]], current_dt: datetime = None
) -> dict[str, Any]:
    """
    Evaluates real-time planetary transits and active Vimshottari dasha to identify
    abstract symbolic strain themes and geometric friction cycles.
    Operates strictly on archetypal mood/theme language without inferring concrete facts.
    """
    if current_dt is None:
        current_dt = datetime.now()

    from core.dasha import get_active_dasha_at_date

    active_dasha = get_active_dasha_at_date(timeline, current_dt)
    transits = get_planet_transit_positions(current_dt)

    lagna_sign = natal["lagna"]["sign"]
    moon_sign = natal["planets"]["Moon"]["sign"]

    zodiac = [
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
    lagna_idx = zodiac.index(lagna_sign)

    # Calculate house indices (1-indexed)
    def sign_for_house(h: int) -> str:
        return zodiac[(lagna_idx + h - 1) % 12]

    def house_for_sign(s: str) -> int:
        s_idx = zodiac.index(s)
        return ((s_idx - lagna_idx) % 12) + 1

    t_saturn_sign = transits["Saturn"]["sign"]
    t_saturn_house = house_for_sign(t_saturn_sign)

    t_rahu_sign = transits["Rahu"]["sign"]
    t_rahu_house = house_for_sign(t_rahu_sign)

    t_jupiter_sign = transits["Jupiter"]["sign"]
    t_jupiter_house = house_for_sign(t_jupiter_sign)

    maha = active_dasha.get("mahadasha", "")
    antar = active_dasha.get("antardasha", "")

    strain_indices: list[dict[str, Any]] = []

    # Saturn aspects (Drishtis): Conjunction, 3rd, 7th, 10th
    saturn_aspect_houses = [
        t_saturn_house,
        ((t_saturn_house + 2 - 1) % 12) + 1,  # 3rd aspect
        ((t_saturn_house + 6 - 1) % 12) + 1,  # 7th aspect
        ((t_saturn_house + 9 - 1) % 12) + 1,  # 10th aspect
    ]

    sign_lords = {
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

    # -------------------------------------------------------------
    # 1. CAREER AXIS STRAIN: H10_SATURN_TRANSIT_TENSION
    # -------------------------------------------------------------
    career_signals = []
    if 10 in saturn_aspect_houses:
        career_signals.append(
            f"Saturn currently influences your 10th House of Career ({sign_for_house(10)}): Call to focus on professional responsibility."
        )

    if (maha == "Mercury" and antar == "Rahu") or (maha == "Venus" and antar == "Rahu"):
        career_signals.append(
            f"Current {maha}-{antar} life chapter marks a transition period testing career priorities and direction."
        )

    tenth_house_sign = sign_for_house(10)
    tenth_lord = sign_lords[tenth_house_sign]
    tenth_lord_house = natal["planets"][tenth_lord]["house"]
    if tenth_lord_house in saturn_aspect_houses:
        career_signals.append(
            f"Your career governing planet ({tenth_lord}) in House {tenth_lord_house} receives focusing pressure from Saturn."
        )

    if career_signals:
        strain_indices.append(
            {
                "domain": "Career & Life Direction",
                "code": "CAREER_FOCUS_CYCLE",
                "strain_index": "ACTIVE_GROWTH",
                "theme": "Career Accountability & Clarifying Your True Purpose",
                "mechanisms": career_signals,
                "symbolic_archetype": (
                    "Saturn's influence on your career area indicates a time of building solid foundations, "
                    "taking on real responsibility, and working with patience. It encourages long-term mastery "
                    "rather than quick shortcuts, carrying zero prediction of job loss or hiring outcomes."
                ),
            }
        )

    # -------------------------------------------------------------
    # 2. FOREIGN DOMAIN ADAPTATION: H12_RAHU_DISPERSION
    # -------------------------------------------------------------
    foreign_signals = []
    if t_rahu_house == 12:
        foreign_signals.append(
            f"Rahu occupies your 12th House ({t_rahu_sign}): Themes of travel, solitude, and exploring unfamiliar spaces."
        )
    if house_for_sign(transits["Ketu"]["sign"]) == 12:
        foreign_signals.append(
            "Ketu in your 12th House: Encourages quiet reflection, decluttering, and letting go of unnecessary baggage."
        )
    if natal["planets"]["Ketu"]["house"] == 12 and t_rahu_house == 12:
        foreign_signals.append(
            "Major cycle shift: Highlights themes of exploring new cultures or adapting to unfamiliar ground."
        )

    if foreign_signals:
        strain_indices.append(
            {
                "domain": "Travel, Solitude & New Environments",
                "code": "EXPANDING_HORIZONS_CYCLE",
                "strain_index": "DEVELOPMENT_THEME",
                "theme": "Adapting to Unfamiliar Surroundings & Broadening Your World",
                "mechanisms": foreign_signals,
                "symbolic_archetype": (
                    "Activity in your 12th house reflects psychological adaptation to new surroundings, "
                    "travel, or spending productive time in quiet reflection. This is an invitation to expand your worldview, "
                    "carrying zero legal, immigration, or bureaucratic assertions."
                ),
            }
        )

    # -------------------------------------------------------------
    # 3. LUNAR & ASCENDANT PRESSURE: LUNAR_SATURN_PRESSURE_CYCLE
    # -------------------------------------------------------------
    lunar_signals = []
    moon_idx = zodiac.index(moon_sign)
    saturn_s_idx = zodiac.index(t_saturn_sign)
    dist_moon = (saturn_s_idx - moon_idx) % 12

    if dist_moon in [11, 0, 1]:  # 12th, 1st, 2nd from Moon (Sade Sati)
        phase = (
            "Approaching (12th from Moon)"
            if dist_moon == 11
            else (
                "Direct Peak (Over Moon)"
                if dist_moon == 0
                else "Concluding (2nd from Moon)"
            )
        )
        lunar_signals.append(
            f"Major 7-year Saturn cycle: {phase} in {t_saturn_sign} (Period of emotional maturity and focus)"
        )

    if t_saturn_house == 1:
        lunar_signals.append(
            f"Saturn crossing your Rising Sign ({t_saturn_sign}): Call for personal discipline and honest self-appraisal."
        )

    if lunar_signals:
        strain_indices.append(
            {
                "domain": "Emotional Resilience & Personal Maturation",
                "code": "MATURATION_CYCLE",
                "strain_index": "DEVELOPMENT_THEME",
                "theme": "Emotional Strength, Self-Discipline & Inner Clarity",
                "mechanisms": lunar_signals,
                "symbolic_archetype": (
                    "Saturn passing near your Moon or Rising Sign is traditionally a milestone cycle of emotional "
                    "maturity, calm patience, and self-reliance. It helps you cut away superficial distractions and "
                    "commit to what truly matters. It carries zero medical diagnostic meaning."
                ),
            }
        )

    # -------------------------------------------------------------
    # 4. DOMESTIC RESTRUCTURING: H4_DOMESTIC_RESTRUCTURING_CYCLE
    # -------------------------------------------------------------
    domestic_signals = []
    if dist_moon == 3:  # 4th from Moon
        domestic_signals.append(
            f"Saturn 4th from your Moon ({t_saturn_sign}): Directing focus toward home life and personal well-being."
        )
    if t_saturn_house == 4:
        domestic_signals.append(
            f"Saturn in your 4th House of Home ({sign_for_house(4)}): Need for stability and comforting routines."
        )
    if 4 in saturn_aspect_houses:
        domestic_signals.append(
            f"Saturn influences your 4th House of Home and Inner Peace ({sign_for_house(4)})."
        )

    fourth_house_sign = sign_for_house(4)
    fourth_lord = sign_lords[fourth_house_sign]
    fourth_lord_house = natal["planets"][fourth_lord]["house"]
    if fourth_lord_house in saturn_aspect_houses:
        career_signals.append(
            f"Your home & family governing planet ({fourth_lord}) in House {fourth_lord_house} receives attention from Saturn."
        )

    if domestic_signals:
        strain_indices.append(
            {
                "domain": "Home, Living Space & Emotional Sanctuary",
                "code": "DOMESTIC_FOUNDATIONS_CYCLE",
                "strain_index": "DEVELOPMENT_THEME",
                "theme": "Strengthening Your Home Base & Finding Inner Grounding",
                "mechanisms": domestic_signals,
                "symbolic_archetype": (
                    "Saturn influencing your 4th house corresponds to evaluating your living environment and emotional "
                    "sanctuary. It encourages establishing long-term roots, peace of mind, and domestic stability, "
                    "carrying zero negative family or property dispute assertions."
                ),
            }
        )

    # -------------------------------------------------------------
    # 5. TRANSFORMATION AXIS: H8_TRANSIT_INTENSITY_WINDOW
    # -------------------------------------------------------------
    shock_signals = []
    if dist_moon == 7:  # 8th from Moon
        shock_signals.append(
            f"Saturn moving through 8th sign from your Moon ({t_saturn_sign}): Deep personal transformation and patience."
        )
    if t_saturn_house == 8:
        shock_signals.append(
            f"Saturn in your 8th House of Resilience ({sign_for_house(8)}): Building inner grit and emotional endurance."
        )
    if t_rahu_house == 8:
        shock_signals.append(
            "Rahu in your 8th House: Curiosity about life's deeper mysteries and hidden psychology."
        )

    if shock_signals:
        strain_indices.append(
            {
                "domain": "Inner Transformation & Navigating Change",
                "code": "TRANSFORMATION_CYCLE",
                "strain_index": "ACTIVE_GROWTH",
                "theme": "Inner Resilience & Managing Unplanned Life Shifts",
                "mechanisms": shock_signals,
                "symbolic_archetype": (
                    "8th house activity highlights periods of quiet introspection, handling uncertainties gracefully, "
                    "and cultivating deep personal resilience. It teaches you how to adapt when plans change, "
                    "carrying zero assertion of financial trauma, accidents, or disasters."
                ),
            }
        )

    # -------------------------------------------------------------
    # 6. RELATIONAL CONTRACTS: H7_RELATIONAL_TRANSIT_FRICTION
    # -------------------------------------------------------------
    relational_signals = []
    if 7 in saturn_aspect_houses or t_saturn_house == 7:
        relational_signals.append(
            f"Saturn influences your 7th House of Relationships ({sign_for_house(7)}): Focus on mutual respect and commitment."
        )
    if t_rahu_house in [1, 7] or house_for_sign(transits["Ketu"]["sign"]) in [1, 7]:
        relational_signals.append(
            "Balancing personal independence with partnership responsibilities."
        )

    seventh_house_sign = sign_for_house(7)
    seventh_lord = sign_lords[seventh_house_sign]
    seventh_lord_house = natal["planets"][seventh_lord]["house"]
    if seventh_lord_house in saturn_aspect_houses:
        relational_signals.append(
            f"Your partnership governing planet ({seventh_lord}) in House {seventh_lord_house} receives structuring energy from Saturn."
        )

    if relational_signals:
        strain_indices.append(
            {
                "domain": "Love, Partnerships & Close Relationships",
                "code": "RELATIONSHIP_CLARITY_CYCLE",
                "strain_index": "DEVELOPMENT_THEME",
                "theme": "Setting Healthy Boundaries & Deepening Mutual Respect",
                "mechanisms": relational_signals,
                "symbolic_archetype": (
                    "Focus on the partnership sector highlights times where relationship commitments, mutual expectations, "
                    "and communication boundaries are realistically reviewed. It encourages honest dialogue and mature "
                    "cooperation, making zero claims of relationship breakup or marital discord."
                ),
            }
        )

    # -------------------------------------------------------------
    # 7. ASTRONOMICAL CYCLE TRANSITIONS (Pure Ephemeris Horizons)
    # -------------------------------------------------------------
    cycle_horizons = []
    if t_rahu_house == 12:
        cycle_horizons.append(
            "Transition into more familiar, grounded surroundings: January 2027."
        )
    if 10 in saturn_aspect_houses:
        cycle_horizons.append(
            "Transition to an expansive, opportunity-rich career chapter: January 2028."
        )
    if t_saturn_house == 1:
        cycle_horizons.append(
            "Personal maturation and heavy self-discipline cycle completes: early 2028."
        )
    if 7 in saturn_aspect_houses or t_saturn_house == 7:
        cycle_horizons.append(
            "Favorable timing window opening for partnerships and cooperative ventures: late 2027 – 2028."
        )
    if t_jupiter_house in [7, 10]:
        cycle_horizons.append(
            f"Jupiter moves into an uplifting area (House {t_jupiter_house}): brings optimism and helpful connections."
        )

    # Format output for backwards compatibility while establishing clean symbolic schema
    return {
        "status": "TRANSIT_TENSION_DETECTED" if strain_indices else "TRANSIT_HARMONY",
        "crisis_count": len(strain_indices),
        "tension_count": len(strain_indices),
        "active_crises": strain_indices,
        "active_strain_indices": strain_indices,
        "threat_vectors": [
            {
                "target": s["domain"],
                "code": s["code"],
                "manifestation": s["theme"],
                "stoppage_citation": s["symbolic_archetype"],
                "severity": s["strain_index"],
            }
            for s in strain_indices
        ],
        "resolution_roadmap": cycle_horizons,
        "predictive_roadmap": [
            {"timeframe": "Ephemeris Horizon", "predicted_phenomenon": h}
            for h in cycle_horizons
        ],
        "generated_epoch": current_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
    }
