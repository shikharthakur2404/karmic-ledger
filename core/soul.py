"""
karmic-ledger: Soul Age & Metaphysical Archetype Telemetry Engine
Determines a soul's evolutionary age (Old Soul vs. Young Soul) and core archetype
using classical Jaimini Atmakaraka (AK) telemetry, nodal axes (Rahu-Ketu), and Nakshatra maturity.
"""

from typing import Any

PLANET_SANSKRIT = {
    "Sun": "सूर्य",
    "Moon": "चन्द्र",
    "Mars": "मंगल",
    "Mercury": "बुध",
    "Jupiter": "बृहस्पति",
    "Venus": "शुक्र",
    "Saturn": "शनि",
    "Rahu": "राहु",
    "Ketu": "केतु",
}

ARCHETYPE_MAP = {
    "Saturn": {
        "title": "The Structural Architect",
        "sanskrit": "कर्माधिकारी (Karmādhikārī)",
        "summary": "Duty-bound builder and master of endurance. Incarnates to shoulder heavy systemic responsibilities, build resilient structures, and burn past-life debts through patient discipline.",
        "lesson": "Transcending cynicism; learning compassion while enforcing structure.",
    },
    "Jupiter": {
        "title": "The Dharmic Counselor & Sage",
        "sanskrit": "धर्माचार्य (Dharmāchārya)",
        "summary": "Teacher, philosopher, and custodian of ancestral wisdom. Operates on universal law, ethics, and cosmic order.",
        "lesson": "Must practice what is preached without intellectual arrogance or dogmatic compromise.",
    },
    "Mercury": {
        "title": "The Ancient Scribe & Polymath",
        "sanskrit": "शास्त्रवित् (Śāstravit)",
        "summary": "Master of languages, logic, scripts, and universal translation. Incarnates to observe, document, analyze, and synthesize disparate systems of knowledge.",
        "lesson": "Moving from endless intellectual dissection into experiential stillness and spiritual surrender.",
    },
    "Venus": {
        "title": "The Relational Aesthete & Empath",
        "sanskrit": "रसज्ञ (Rasajña)",
        "summary": "Explorer of beauty, unconditional devotion, emotional harmonics, and relational boundaries. Seeks the divine through refined artistic and interpersonal unity.",
        "lesson": "Distinguishing pure love from codependency, sensory attachment, and fear of relational abandonment.",
    },
    "Sun": {
        "title": "The Sovereign Monarch & Lightbearer",
        "sanskrit": "तेजस्वी (Tejasvī)",
        "summary": "Soul of leadership, self-realization, and divine will. Incarnates with innate sovereignty to guide, protect, and illuminate pathless frontiers.",
        "lesson": "Dissolving egoic self-absorption; mastering selfless stewardship rather than royal entitlement.",
    },
    "Mars": {
        "title": "The Strategic Vanguard & Warrior",
        "sanskrit": "रणनीतिज्ञ (Raṇanītijña)",
        "summary": "Protector, engineer, and elemental conqueror. Possesses boundless courage, tactical precision, and a visceral drive to defend righteousness.",
        "lesson": "Channelling raw reactive aggression into deliberate, disciplined strategic power.",
    },
    "Moon": {
        "title": "The Collective Healer & Sustainer",
        "sanskrit": "पोषणकर्ता (Poṣaṇakartā)",
        "summary": "Deeply empathic and intuitive mother-soul. Carries a cosmic instinct to shelter, feed, nourish, and heal suffering living beings.",
        "lesson": "Guarding emotional boundaries so collective pain does not drown personal inner peace.",
    },
}


ANCIENT_NAKSHATRAS = {
    "Magha",
    "Pushya",
    "Mula",
    "Revati",
    "Uttara Bhadrapada",
    "Ashlesha",
    "Jyeshtha",
}
GENESIS_NAKSHATRAS = {"Ashwini", "Krittika", "Rohini"}


def evaluate_soul_telemetry(natal: dict[str, Any]) -> dict[str, Any]:
    """
    Computes deterministic soul age and archetype telemetry.
    Based on Jaimini Atmakaraka degree, Nodal house polarity, and Nakshatra epoch.
    """
    # 1. Identify Atmakaraka (highest degree among 7 classical planets)
    classical_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    candidates = {}
    for p in classical_planets:
        p_data = natal["planets"][p]
        candidates[p] = p_data["degree_in_sign"]

    ak_planet = max(candidates, key=candidates.get)
    ak_deg = candidates[ak_planet]
    ak_data = natal["planets"][ak_planet]

    # 2. Calculate Soul Antiquity Score (0.0 to 5.0)
    score = 0.0

    # AK Degree weighting (0°-30°):
    if ak_deg >= 26.0:
        score += 3.5  # Extreme late-stage soul
    elif ak_deg >= 20.0:
        score += 2.8
    elif ak_deg >= 12.0:
        score += 1.8
    else:
        score += 0.8  # Early-stage exploration

    # Ketu (Moksha/Detachment Vector):
    ketu_house = natal["planets"]["Ketu"]["house"]
    if ketu_house in [1, 12]:
        score += 1.2  # Deep past-life fatigue / liberation path
    elif ketu_house in [8, 9]:
        score += 0.8
    elif ketu_house in [3, 4]:
        score += 0.3

    # Nakshatra Age:
    moon_nak = natal["planets"]["Moon"]["nakshatra"]["name"]
    lagna_nak = natal["lagna"]["nakshatra"]["name"]

    if moon_nak in ANCIENT_NAKSHATRAS or lagna_nak in ANCIENT_NAKSHATRAS:
        score += 0.8
    elif moon_nak in GENESIS_NAKSHATRAS:
        score -= 0.3

    # 3. Categorize Soul Age & Evolutionary Cycle
    if score >= 4.0:
        age_category = "Ancient / End-Cycle Soul"
        sanskrit_cat = "परम-प्राचीन जीव (Parama-Prāchīna Jīva)"
        maturity_level = "Late Stage (90%+ Cycle Completion)"
        semantic_feel = "TRANSCENDENT"
        semantic_badge = "Transcendent · End-Cycle Soul (90%+ Cycle)"
        score_meaning = (
            "Score "
            f"{round(score, 1)} / 5.0 indicates an Ancient, End-Cycle Soul (90%+ cycle completed). "
            "Innate detachment, unlearned mastery, and little desire for trivial accolades. "
            "Focus is burning residual debts (Nirjara) and preparing for liberation."
        )
        description = (
            "This soul has traversed numerous incarnations across eons. It enters this life with innate "
            "detachment, unlearned mastery, and little desire for trivial worldly accolades. The focus "
            "of this incarnation is burning final residual debts (Nirjara) and preparing for liberation."
        )
    elif score >= 2.6:
        age_category = "Old Soul"
        sanskrit_cat = "प्राचीन जीव (Prāchīna Jīva)"
        maturity_level = "Advanced Maturity (70–89% Cycle Completion)"
        semantic_feel = "POSITIVE"
        semantic_badge = "Advanced Maturity · Old Soul (70–89% Cycle)"
        score_meaning = (
            "Score "
            f"{round(score, 1)} / 5.0 places you in the Old Soul tier (70–89% cycle completed). "
            "This is a deeply positive, grounded position. You possess high natural endurance, "
            "instinct for structural order, and zero patience for superficial social drama."
        )
        description = (
            "A seasoned, duty-bound soul that has built systems and held heavy responsibilities in prior cycles. "
            "It possesses high natural endurance, low patience for superficial social games, and an innate "
            "instinct for structural order."
        )
    elif score >= 1.2:
        age_category = "Mid-Cycle Evolutionary Soul"
        sanskrit_cat = "मध्यम जीव (Madhyama Jīva)"
        maturity_level = "Intermediate Evolution (40–69% Cycle Completion)"
        semantic_feel = "BALANCED"
        semantic_badge = "Balanced Growth · Mid-Cycle Soul (40–69% Cycle)"
        score_meaning = (
            "Score "
            f"{round(score, 1)} / 5.0 represents a Mid-Cycle Evolutionary Soul (40–69% cycle completed). "
            "Active worldly balance: navigating desires, career ambition, boundary-setting, and human relationships."
        )
        description = (
            "This soul is actively navigating the complex human arena of desire, power, boundary-setting, "
            "and emotional relationships. It is neither a detached ascetic nor an earthly novice; it is "
            "mastering foundational relational and social contracts."
        )
    else:
        age_category = "Young / Exploratory Soul"
        sanskrit_cat = "नवीन जीव (Navīna Jīva)"
        maturity_level = "Pioneering Stage (10–39% Cycle Completion)"
        semantic_feel = "EXPLORATORY"
        semantic_badge = "Pioneering Stage · Young Soul (10–39% Cycle)"
        score_meaning = (
            "Score "
            f"{round(score, 1)} / 5.0 represents a Young, Exploratory Soul (10–39% cycle completed). "
            "High vitality, enthusiasm for worldly experiences, rapid adaptation, and fresh material curiosity."
        )
        description = (
            "A fresh, enthusiastic soul eager for worldly experience, material conquest, sensory delights, "
            "and new emotional frontiers. High vitality, curiosity, and rapid adaptation to physical plane realities."
        )

    # 4. Refine Archetype for Special Conditions (e.g. Debilitated AK)
    base_arch = ARCHETYPE_MAP.get(ak_planet, ARCHETYPE_MAP["Saturn"])
    archetype_title = base_arch["title"]
    archetype_sanskrit = base_arch["sanskrit"]
    archetype_summary = base_arch["summary"]
    archetype_lesson = base_arch["lesson"]

    if ak_planet == "Jupiter" and ak_data["dignity"] == "Debilitated (Neecha)":
        archetype_title += " (Ethical Stress-Test)"
        archetype_summary += " With Jupiter (Guru) in debilitation as Ātmakāraka, the soul carries past-life karma of compromised ethics or dogmatic abuse. This incarnation is an active stress-test of foundational integrity."
    elif ak_planet == "Saturn" and ak_data["dignity"] == "Debilitated (Neecha)":
        archetype_title += " (Forged in Fire)"
        archetype_summary += " Saturn in Aries tests endurance in the fire of worldly friction, transforming early struggle into unshakeable technical and moral fortitude through Neecha Bhanga."

    # 5. Compile Telemetry Manifest
    rahu_house = natal["planets"]["Rahu"]["house"]
    rahu_sign = natal["planets"]["Rahu"]["sign"]
    ketu_sign = natal["planets"]["Ketu"]["sign"]

    # Calculate percentage into 30-degree cycle
    odometer_pct = round((ak_deg / 30.0) * 100, 1)
    gauge_pct = min(max(round((score / 5.0) * 100, 1), 4.0), 98.0)

    return {
        "soul_age_category": age_category,
        "sanskrit_category": sanskrit_cat,
        "maturity_level": maturity_level,
        "semantic_feel": semantic_feel,
        "semantic_badge": semantic_badge,
        "score_meaning": score_meaning,
        "stage_description": description,
        "antiquity_score": round(score, 1),
        "antiquity_index": round(score, 1),
        "gauge_pct": gauge_pct,
        "atmakaraka_planet": ak_planet,
        "atmakaraka_sanskrit": PLANET_SANSKRIT.get(ak_planet, ak_planet),
        "atmakaraka_degree": f"{ak_deg:.2f}°",
        "atmakaraka_formatted": ak_data["formatted"],
        "atmakaraka_dignity": ak_data["dignity"],
        "odometer_percentage": f"{odometer_pct}%",
        "odometer_pct": odometer_pct,
        "archetype_title": archetype_title,
        "archetype_sanskrit": archetype_sanskrit,
        "archetype_summary": archetype_summary,
        "archetype_description": archetype_summary,
        "core_lesson": archetype_lesson,
        "past_life_mastery": f"House {ketu_house} ({ketu_sign}) • Instinctual mastery, emotional detachment, and pre-learned wisdom.",
        "unmastered_frontier": f"House {rahu_house} ({rahu_sign}) • Active growth edge, worldly impact, and unspent appetite.",
    }
