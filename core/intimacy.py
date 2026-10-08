"""
karmic-ledger: Intimacy & Desire Telemetry (symbolic)

Maps Venus, Mars, and houses 5 / 7 / 8 into a plain-language intimacy profile.
Outputs are archetypal heuristics — not medical advice, not a claim about any
partner's behavior, and never a permission structure for non-consent.
"""

from __future__ import annotations

from typing import Any

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

VENUS_STYLE = {
    "Aries": ("Direct & initiatory", "Attraction moves fast; you prefer clear desire and chase."),
    "Taurus": ("Sensual & steady", "Touch, pace, and physical comfort matter more than drama."),
    "Gemini": ("Playful & verbal", "Flirting, talk, and variety keep desire alive."),
    "Cancer": ("Tender & bonding", "Emotional safety unlocks physical closeness."),
    "Leo": ("Warm & expressive", "Appreciation and being wanted are central to arousal."),
    "Virgo": ("Attentive & precise", "Care, hygiene, and thoughtful pacing deepen trust."),
    "Libra": ("Harmonic & reciprocal", "Mutual beauty, balance, and fairness shape intimacy."),
    "Scorpio": ("Intense & private", "Depth, loyalty, and emotional honesty intensify desire."),
    "Sagittarius": ("Adventurous & open", "Freedom, humor, and exploration keep chemistry fresh."),
    "Capricorn": ("Loyal & reserved", "Commitment and respect unlock gradual physical trust."),
    "Aquarius": ("Unconventional & mental", "Friendship, novelty, and autonomy feed attraction."),
    "Pisces": ("Dreamy & merging", "Romance, softness, and emotional immersion lead."),
}

MARS_STYLE = {
    "Aries": ("High drive", "Passion is straightforward and physical."),
    "Taurus": ("Enduring heat", "Desire builds slowly and lasts."),
    "Gemini": ("Curious energy", "Variety and mental spark fuel pursuit."),
    "Cancer": ("Protective passion", "Care and emotional bond amplify drive."),
    "Leo": ("Proud magnetism", "Confidence and play raise the temperature."),
    "Virgo": ("Focused craft", "Skill, timing, and attentiveness matter."),
    "Libra": ("Charm pursuit", "Seduction through harmony and aesthetics."),
    "Scorpio": ("Concentrated intensity", "All-or-nothing focus once engaged."),
    "Sagittarius": ("Exploratory fire", "Spontaneity and openness excite."),
    "Capricorn": ("Controlled stamina", "Discipline and long-game desire."),
    "Aquarius": ("Detached spark", "Unpredictable, experimental attraction."),
    "Pisces": ("Fluid longing", "Fantasy and emotional absorption."),
}


def _house_for_planet(natal: dict[str, Any], planet: str) -> int:
    return int(natal["planets"][planet]["house"])


def _sign_for_house(natal: dict[str, Any], house: int) -> str:
    lagna_idx = ZODIAC_SIGNS.index(natal["lagna"]["sign"])
    return ZODIAC_SIGNS[(lagna_idx + house - 1) % 12]


def _occupants(natal: dict[str, Any], house: int) -> list[str]:
    return [
        name
        for name, data in natal["planets"].items()
        if int(data["house"]) == house
    ]


def _dignity_note(dignity: str) -> str:
    if "Exalted" in dignity:
        return "strongly supported"
    if "Own" in dignity:
        return "in familiar strength"
    if "Debilitated" in dignity:
        return "under stretch / needs care"
    return "neutral baseline"


def evaluate_intimacy_telemetry(
    natal: dict[str, Any],
    *,
    active_dasha: dict[str, Any] | None = None,
    birth_time_unknown: bool = False,
) -> dict[str, Any]:
    """
    Symbolic intimacy / desire profile for UI Sector display.
    """
    venus = natal["planets"]["Venus"]
    mars = natal["planets"]["Mars"]
    v_sign = venus["sign"]
    m_sign = mars["sign"]
    v_style, v_blurb = VENUS_STYLE.get(v_sign, ("Open", "Venus shapes attraction style."))
    m_style, m_blurb = MARS_STYLE.get(m_sign, ("Active", "Mars shapes pursuit energy."))

    h5 = _sign_for_house(natal, 5)
    h7 = _sign_for_house(natal, 7)
    h8 = _sign_for_house(natal, 8)
    h7_lord = SIGN_LORDS[h7]
    h7_occ = _occupants(natal, 7)
    h8_occ = _occupants(natal, 8)
    h5_occ = _occupants(natal, 5)

    # Simple confluence score 0–100 (heuristic, not prediction of partners)
    score = 55.0
    if "Exalted" in venus.get("dignity", "") or "Own" in venus.get("dignity", ""):
        score += 12
    if "Debilitated" in venus.get("dignity", ""):
        score -= 10
    if "Exalted" in mars.get("dignity", "") or "Own" in mars.get("dignity", ""):
        score += 8
    if "Debilitated" in mars.get("dignity", ""):
        score -= 6
    if venus["house"] in (1, 5, 7):
        score += 6
    if mars["house"] in (1, 7, 8):
        score += 4
    if "Venus" in h7_occ or "Mars" in h7_occ:
        score += 5
    if "Saturn" in h7_occ:
        score -= 4  # slower / more serious bonding tempo
    if "Rahu" in h8_occ or "Ketu" in h8_occ:
        score += 2  # intensity / unconventional bonding themes

    dasha_note = "No dasha context supplied."
    if active_dasha and "error" not in active_dasha:
        maha = active_dasha.get("mahadasha", "")
        antar = active_dasha.get("antardasha", "")
        hot = {"Venus", "Mars", "Rahu", "Moon"}
        if maha in hot or antar in hot:
            dasha_note = (
                f"Active chapter {maha}–{antar} touches desire / bonding significators — "
                "intimacy themes may feel louder in this period (symbolic timing only)."
            )
            score += 4
        else:
            dasha_note = (
                f"Active chapter {maha}–{antar} is not a classic desire-lord pair; "
                "intimacy still follows Venus/Mars baseline."
            )

    score = round(max(20.0, min(score, 92.0)), 1)

    if score >= 72:
        badge = "Warm & available chemistry (symbolic)"
        feel = "POSITIVE"
    elif score >= 52:
        badge = "Balanced desire baseline (symbolic)"
        feel = "BALANCED"
    else:
        badge = "Careful / paced intimacy (symbolic)"
        feel = "CAUTION"

    partner_house_blurb = (
        f"7th house in {h7} (lord {h7_lord})"
        + (f"; occupied by {', '.join(h7_occ)}" if h7_occ else "; no natal planets inside")
        + ". This describes partnership style, not a specific person’s looks or destiny."
    )

    if birth_time_unknown:
        return {
            "status": "LAGNA_SUPPRESSED",
            "title": "Intimacy & Desire Profile",
            "badge": "Needs exact birth time",
            "semantic_feel": "NEUTRAL",
            "desire_index": None,
            "summary": (
                "House-based intimacy mapping needs a reliable Lagna. "
                "Venus/Mars sign styles can still be shown once time is confirmed."
            ),
            "epistemic_notice": (
                "Symbolic only. Never override consent. Not medical or therapeutic advice."
            ),
            "factors": [],
        }

    factors = [
        {
            "id": "venus",
            "label": "Venus — attraction & pleasure style",
            "value": f"{v_sign} · House {venus['house']} · {_dignity_note(venus.get('dignity', ''))}",
            "style": v_style,
            "note": v_blurb,
        },
        {
            "id": "mars",
            "label": "Mars — drive & pursuit",
            "value": f"{m_sign} · House {mars['house']} · {_dignity_note(mars.get('dignity', ''))}",
            "style": m_style,
            "note": m_blurb,
        },
        {
            "id": "house_5",
            "label": "5th house — romance & flirtation",
            "value": f"{h5}"
            + (f" · {', '.join(h5_occ)}" if h5_occ else " · empty"),
            "style": "Romantic play",
            "note": "How courtship and playful attraction show up.",
        },
        {
            "id": "house_7",
            "label": "7th house — partnership chemistry",
            "value": f"{h7} · lord {h7_lord}"
            + (f" · {', '.join(h7_occ)}" if h7_occ else ""),
            "style": "Relating pattern",
            "note": partner_house_blurb,
        },
        {
            "id": "house_8",
            "label": "8th house — deep bonding / private intimacy",
            "value": f"{h8}"
            + (f" · {', '.join(h8_occ)}" if h8_occ else " · empty"),
            "style": "Depth & trust",
            "note": (
                "Private closeness, vulnerability, and shared intensity — "
                "not a forecast of harm or secrecy drama."
            ),
        },
        {
            "id": "dasha",
            "label": "Current timing chapter",
            "value": (
                f"{active_dasha.get('mahadasha')}-{active_dasha.get('antardasha')}"
                if active_dasha and "error" not in (active_dasha or {})
                else "n/a"
            ),
            "style": "Timing tone",
            "note": dasha_note,
        },
    ]

    summary = (
        f"Attraction leans {v_style.lower()}; pursuit energy is {m_style.lower()}. "
        f"{v_blurb} {m_blurb} "
        "Read this as a mirror for self-awareness with a partner — never as pressure."
    )

    shastra_queries = ["venus", "mars", "kalatra", "marriage"]

    return {
        "status": "OK",
        "title": "Intimacy & Desire Profile",
        "badge": badge,
        "semantic_feel": feel,
        "desire_index": score,
        "summary": summary,
        "venus_style": v_style,
        "mars_style": m_style,
        "factors": factors,
        "shastra_query_hints": shastra_queries,
        "epistemic_notice": (
            "Symbolic Jyotiṣa heuristic from Venus, Mars, and houses 5/7/8. "
            "Not medical, fertility, or orientation diagnosis. "
            "Consent and mutual comfort always outrank any chart reading."
        ),
        "rag_seed": " OR ".join(shastra_queries[:3]),
    }
