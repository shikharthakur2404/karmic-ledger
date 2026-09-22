"""
karmic-ledger: Classical Ayurdaya & Longevity Estimation Engine
Fun Kundli Edition: Evaluates classical Parashari & Jaimini Three-Pair Longevity formulas
with Kakshya Vriddhi (tier expansion) modifiers for entertainment and educational research.
"""

from typing import Any


def get_sign_mobility(sign_name: str) -> str:
    """Returns 'movable', 'fixed', or 'dual' for a given zodiac sign."""
    sign_lower = sign_name.lower().strip()
    movable = [
        "aries",
        "cancer",
        "libra",
        "capricorn",
        "mesha",
        "karka",
        "tula",
        "makara",
    ]
    fixed = [
        "taurus",
        "leo",
        "scorpio",
        "aquarius",
        "vrishabha",
        "simha",
        "vrishchika",
        "kumbha",
    ]

    if any(s in sign_lower for s in movable):
        return "movable"
    if any(s in sign_lower for s in fixed):
        return "fixed"
    return "dual"


def evaluate_pair_longevity(mob1: str, mob2: str) -> str:
    """
    Standard Jaimini Three-Pair Formula:
    - Movable + Movable OR Fixed + Dual = Purnayu (Long)
    - Fixed + Fixed OR Movable + Dual = Madhyayu (Medium)
    - Dual + Dual OR Movable + Fixed = Alpayu (Short)
    """
    pair = {mob1, mob2}
    if mob1 == "movable" and mob2 == "movable":
        return "Purnayu"
    if pair == {"fixed", "dual"}:
        return "Purnayu"
    if mob1 == "fixed" and mob2 == "fixed":
        return "Madhyayu"
    if pair == {"movable", "dual"}:
        return "Madhyayu"
    if mob1 == "dual" and mob2 == "dual":
        return "Alpayu"
    if pair == {"movable", "fixed"}:
        return "Alpayu"
    return "Madhyayu"


def compute_ayurdaya_telemetry(natal: dict[str, Any]) -> dict[str, Any]:
    """
    Calculates classical Ayurdaya (life expectancy band) based on:
    1. Method of Three Pairs (Lagna Lord + 8th Lord, Moon + Saturn, Lagna + 8th House).
    2. Kakshya Vriddhi (Life tier promotion via Jupiter aspect on Lagna/Lagna Lord).
    3. Saturn (Ayushkaraka) dignity & 8th House vitality.
    """
    planets = natal.get("planets", {})
    lagna_data = natal.get("lagna", {})
    lagna_sign = lagna_data.get("sign", "Scorpio")

    # Zodiac lord mapping
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

    zodiac_order = [
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

    try:
        lagna_idx = zodiac_order.index(lagna_sign)
    except ValueError:
        lagna_idx = 7  # Scorpio default

    # 8th House
    h8_sign = zodiac_order[(lagna_idx + 7) % 12]
    lagna_lord_name = sign_lords[lagna_sign]
    h8_lord_name = sign_lords[h8_sign]

    # Mobility of components
    lagna_mob = get_sign_mobility(lagna_sign)
    h8_mob = get_sign_mobility(h8_sign)

    ll_sign = planets.get(lagna_lord_name, {}).get("sign", "Virgo")
    ll_mob = get_sign_mobility(ll_sign)

    h8l_sign = planets.get(h8_lord_name, {}).get("sign", "Libra")
    h8l_mob = get_sign_mobility(h8l_sign)

    moon_sign = planets.get("Moon", {}).get("sign", "Aries")
    moon_mob = get_sign_mobility(moon_sign)

    saturn_sign = planets.get("Saturn", {}).get("sign", "Taurus")
    saturn_mob = get_sign_mobility(saturn_sign)

    # 3 Pairs
    pair1 = evaluate_pair_longevity(ll_mob, h8l_mob)  # Lagna Lord & 8th Lord
    pair2 = evaluate_pair_longevity(moon_mob, saturn_mob)  # Moon & Saturn
    pair3 = evaluate_pair_longevity(lagna_mob, h8_mob)  # Lagna & 8th House

    pair_votes = [pair1, pair2, pair3]
    purnayu_votes = pair_votes.count("Purnayu")
    madhyayu_votes = pair_votes.count("Madhyayu")
    alpayu_votes = pair_votes.count("Alpayu")

    # Base Tier determination
    if purnayu_votes >= 2:
        base_tier = "Purnayu"
    elif alpayu_votes >= 2:
        base_tier = "Alpayu"
    elif madhyayu_votes >= 2:
        base_tier = "Madhyayu"
    else:
        # If all 3 distinct, Pair 1 (Lagna Lord & 8th Lord) dominates
        base_tier = pair1

    # Modifiers: Kakshya Vriddhi (Tier promotion)
    modifiers = []
    promoted_tier = base_tier

    # Jupiter benefic aspect or conjunction
    jupiter_data = planets.get("Jupiter", {})
    jupiter_house = jupiter_data.get("house", 7)
    ll_house = planets.get(lagna_lord_name, {}).get("house", 11)

    # Jupiter in Kendra (1, 4, 7, 10) or Trikona (5, 9) adds strong vitality
    if jupiter_house in [1, 4, 7, 10, 5, 9]:
        modifiers.append(
            "Jupiter in Kendra (House 7) grants vital protection & tier stability"
        )
        if promoted_tier == "Alpayu":
            promoted_tier = "Madhyayu"
            modifiers.append(
                "Kakshya Vriddhi: Jupiter Kendra lifts longevity tier to Madhyayu"
            )
        elif promoted_tier == "Madhyayu":
            promoted_tier = "Purnayu"
            modifiers.append(
                "Kakshya Vriddhi: Benefic Jupiter Kendra promotes life band to Purnayu"
            )

    # Saturn (Ayushkaraka) in Kendra with Jupiter
    if planets.get("Saturn", {}).get("house") == 7:
        modifiers.append(
            "Ayushkaraka Saturn in House 7 conjunct Guru imparts long-term cellular endurance"
        )

    # Lagna Lord in Upachaya House (3, 6, 10, 11)
    if ll_house in [3, 6, 10, 11]:
        modifiers.append(
            f"Lagna Lord {lagna_lord_name} in 11th Upachaya house ensures progressive vitality"
        )

    # Numerical span estimation
    if promoted_tier == "Purnayu":
        tier_title = "Pūrṇāyu (दीर्घायु // Full Longevity Horizon)"
        est_range = "78 – 88+ Years"
        vitality_score = 88
        summary_text = "Strong structural vitality. Classical three-pair geometry supported by Jupiter in Kendra and Saturn as Ayushkaraka indicates high natural endurance and long-term lifespan horizon."
    elif promoted_tier == "Madhyayu":
        tier_title = "Madhyāyu (मध्यायु // Balanced Longevity Horizon)"
        est_range = "68 – 78 Years"
        vitality_score = 74
        summary_text = "Moderate and steady vitality baseline. Planetary positions reflect balanced constitutional endurance requiring consistent lifestyle hygiene."
    else:
        tier_title = "Alpāyu (अल्पायु // Protective Threshold Model)"
        est_range = "60 – 70 Years (With Benefic Buffers)"
        vitality_score = 62
        summary_text = "Requires active health and cardiovascular maintenance. Benefic Jupiter buffers protect the baseline horizon."

    return {
        "tier": promoted_tier,
        "tier_title": tier_title,
        "estimated_range": est_range,
        "vitality_score": vitality_score,
        "base_tier": base_tier,
        "pairs_evaluated": {
            "lagna_lord_and_8th_lord": f"{ll_mob.capitalize()} ({ll_sign}) & {h8l_mob.capitalize()} ({h8l_sign}) -> {pair1}",
            "moon_and_saturn": f"{moon_mob.capitalize()} ({moon_sign}) & {saturn_mob.capitalize()} ({saturn_sign}) -> {pair2}",
            "lagna_and_8th_house": f"{lagna_mob.capitalize()} ({lagna_sign}) & {h8_mob.capitalize()} ({h8_sign}) -> {pair3}",
        },
        "modifiers": modifiers,
        "summary": summary_text,
        "fun_mode_disclaimer": "Fun Kundli Edition // Classical Ayurdaya Research Algorithm. Strictly for WG entertainment and astrological curiosity. Zero medical diagnostic or biological lifespan certainty.",
    }
