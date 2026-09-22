"""
karmic-ledger: Classical Parashari Ashtakavarga Engine
Computes Bhinna Ashtakavarga (BAV) for the 7 classical planets and Samudaya/Sarvashtakavarga (SAV)
for all 12 Bhavas as per Brihat Parashara Hora Shastra (BPHS Ch. 66-72).
Provides bindu strength multipliers to weight planetary transits and house vitality.
"""

from typing import Any

# BPHS Ashtakavarga Benefic Contribution Tables (1-indexed house offsets from donor planet/Lagna)
# Reference: BPHS Ch. 66-72 / Phaladeepika Ch. 24
ASHTAKAVARGA_RULES: dict[str, dict[str, list[int]]] = {
    "Sun": {
        "Sun": [1, 2, 4, 7, 8, 9, 10, 11],
        "Moon": [3, 6, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [5, 6, 9, 11],
        "Venus": [6, 7, 12],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Lagna": [3, 4, 6, 10, 11, 12],
    },
    "Moon": {
        "Sun": [3, 6, 7, 8, 10, 11],
        "Moon": [1, 3, 6, 7, 10, 11],
        "Mars": [2, 3, 5, 6, 9, 10, 11],
        "Mercury": [1, 3, 4, 5, 7, 8, 10, 11],
        "Jupiter": [1, 4, 7, 8, 10, 11, 12],
        "Venus": [3, 4, 5, 7, 9, 10, 11],
        "Saturn": [3, 5, 6, 11],
        "Lagna": [3, 6, 10, 11],
    },
    "Mars": {
        "Sun": [3, 5, 6, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [3, 5, 6, 11],
        "Jupiter": [6, 10, 11, 12],
        "Venus": [6, 8, 11, 12],
        "Saturn": [1, 4, 7, 8, 9, 10, 11],
        "Lagna": [1, 3, 6, 10, 11],
    },
    "Mercury": {
        "Sun": [5, 6, 9, 11, 12],
        "Moon": [2, 4, 6, 8, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [1, 3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [6, 8, 11, 12],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 11],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Lagna": [1, 2, 4, 6, 8, 10, 11],
    },
    "Jupiter": {
        "Sun": [1, 2, 3, 4, 7, 8, 9, 10, 11],
        "Moon": [2, 5, 7, 9, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [1, 2, 4, 5, 6, 9, 10, 11],
        "Jupiter": [1, 2, 3, 4, 7, 8, 10, 11],
        "Venus": [2, 5, 6, 9, 10, 11],
        "Saturn": [3, 5, 6, 12],
        "Lagna": [1, 2, 4, 5, 6, 7, 9, 10, 11],
    },
    "Venus": {
        "Sun": [8, 11, 12],
        "Moon": [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "Mars": [3, 5, 6, 9, 11, 12],
        "Mercury": [3, 5, 6, 9, 11],
        "Jupiter": [5, 8, 9, 10, 11],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 10, 11],
        "Saturn": [3, 4, 5, 8, 9, 10, 11],
        "Lagna": [1, 2, 3, 4, 5, 8, 9, 11],
    },
    "Saturn": {
        "Sun": [1, 2, 4, 7, 8, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [3, 5, 6, 10, 11, 12],
        "Mercury": [6, 8, 9, 10, 11, 12],
        "Jupiter": [5, 6, 11, 12],
        "Venus": [6, 11, 12],
        "Saturn": [3, 5, 6, 11],
        "Lagna": [1, 3, 4, 6, 10, 11],
    },
}


def compute_sarvashtakavarga(natal_chart: dict[str, Any]) -> dict[str, Any]:
    """
    Computes Sarvashtakavarga (SAV) bindu scores (0-56) for all 12 houses.
    Returns:
    - sav_by_house: Dict[int, int] (House 1 to 12 -> bindu count)
    - sav_by_sign: Dict[str, int] (Zodiac Sign -> bindu count)
    - bav_tables: Individual planet bindu charts
    """
    planets = natal_chart["planets"]
    lagna_sign_idx = (
        natal_chart["lagna"]["sign_index"]
        if "sign_index" in natal_chart["lagna"]
        else (
            [
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
            ].index(natal_chart["lagna"]["sign"])
        )
    )

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

    # Map each planet & Lagna to its 0-indexed zodiac sign
    donor_sign_indices: dict[str, int] = {}
    for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        if p_name in planets:
            p_sign = planets[p_name]["sign"]
            donor_sign_indices[p_name] = zodiac.index(p_sign)
        else:
            donor_sign_indices[p_name] = 0
    donor_sign_indices["Lagna"] = lagna_sign_idx

    # Initialize 12 zodiac signs for SAV
    sav_by_sign_idx = [0] * 12
    bav_by_planet: dict[str, list[int]] = {}

    for recipient_planet, rules in ASHTAKAVARGA_RULES.items():
        bav = [0] * 12
        for donor, house_offsets in rules.items():
            d_sign_idx = donor_sign_indices.get(donor, 0)
            for offset in house_offsets:
                # 1-indexed offset from donor sign
                target_sign_idx = (d_sign_idx + offset - 1) % 12
                bav[target_sign_idx] += 1
                sav_by_sign_idx[target_sign_idx] += 1
        bav_by_planet[recipient_planet] = bav

    # Map to Houses (House 1 = Lagna sign)
    sav_by_house: dict[int, int] = {}
    for h in range(1, 13):
        sign_idx = (lagna_sign_idx + h - 1) % 12
        sav_by_house[h] = sav_by_sign_idx[sign_idx]

    sav_by_sign_name: dict[str, int] = {
        zodiac[i]: sav_by_sign_idx[i] for i in range(12)
    }

    return {
        "sav_by_house": sav_by_house,
        "sav_by_sign": sav_by_sign_name,
        "bav_by_planet": bav_by_planet,
    }


def get_ashtakavarga_house_multiplier(sav_bindus: int) -> float:
    """
    Returns heuristic scaling multiplier based on Sarvashtakavarga bindu count:
    - >= 32 bindus: Highly fortified house (1.20x multiplier)
    - 28 - 31 bindus: Robust/Average (1.00x)
    - 25 - 27 bindus: Mildly deficient (0.85x)
    - < 25 bindus: Severe obstruction / deficit (0.65x)
    """
    if sav_bindus >= 32:
        return 1.20
    elif sav_bindus >= 28:
        return 1.00
    elif sav_bindus >= 25:
        return 0.85
    else:
        return 0.65
