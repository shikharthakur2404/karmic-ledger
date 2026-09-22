"""
karmic-ledger: Planetary Primer & Plain-Language Education Engine
Translates classical Vedic technical jargon into intuitive, modern, systems-architecture terms.
"""

from typing import Any

CORE_CONCEPTS: dict[str, dict[str, str]] = {
    "lagna": {
        "title": "Ascendant / Lagna (The Operating System & Physical Container)",
        "analogy": "The physical chassis and root operating system of a machine.",
        "explanation": (
            "Your Lagna is the exact zodiac sign that was rising on the eastern horizon at the moment of your birth. "
            "It defines your physical build, stamina, default defensive posture, and how the external world perceives you."
        ),
    },
    "moon_sign": {
        "title": "Moon Sign / Rashi (The Emotional Substrate & Mind)",
        "analogy": "The CPU memory, internal RAM, and psychological operating rhythm.",
        "explanation": (
            "While Western astrology emphasizes the Sun, Vedic astrology places the Moon at the center. "
            "Your Moon reveals what your mind needs to feel safe, how you process heartbreak, and your instinctual emotional reactions."
        ),
    },
    "sun_sign": {
        "title": "Sun Sign / Surya (The Core Energy Generator & Authority)",
        "analogy": "The power supply unit and sovereign soul mission.",
        "explanation": (
            "The Sun represents your self-respect, your relationship with father figures, and your innate sense of purpose. "
            "It is the flame that cannot be extinguished by circumstance."
        ),
    },
    "vimshottari_dasha": {
        "title": "Vimshottari Dasha (The Cosmic Execution Schedule)",
        "analogy": "The task scheduler and runtime thread allocation of your life.",
        "explanation": (
            "You do not experience your entire birth chart all at once. The Vimshottari Dasha is a 120-year cycle where "
            "different planets take the conductor's baton for specific years. When Venus runs, relationships and aesthetics activate. "
            "When Rahu runs, exploration of unconventional domains and intense ambition activate. When Saturn runs, hard reality and discipline are demanded."
        ),
    },
}

PLANET_PROFILES: dict[str, dict[str, Any]] = {
    "Sun": {
        "sanskrit": "Surya (सूर्य)",
        "role": "The Sovereign / The King",
        "keywords": ["Self-respect", "Father", "Vitality", "Authority", "Government"],
        "how_it_works": "The Sun gives you the backbone to stand up for yourself. When strong, you command respect without shouting.",
    },
    "Moon": {
        "sanskrit": "Chandra (चन्द्र)",
        "role": "The Mother / The Mind",
        "keywords": ["Emotions", "Intuition", "Mother", "Nourishment", "Memory"],
        "how_it_works": "The Moon governs how you feel at night when the world is quiet. It is your empathy, your attachment, and your mental peace.",
    },
    "Mars": {
        "sanskrit": "Mangal / Kuja (मंगल)",
        "role": "The Commander / The Fire",
        "keywords": [
            "Courage",
            "Drive",
            "Engineering",
            "Muscle",
            "Brothers",
            "Real Estate",
        ],
        "how_it_works": "Mars is your inner warrior. It decides whether you run from conflict or advance under fire. It is pure tactical execution.",
    },
    "Mercury": {
        "sanskrit": "Budh (बुध)",
        "role": "The Systems Architect / The Intellectual",
        "keywords": [
            "Coding",
            "Syntax",
            "Languages",
            "Calculations",
            "Handwriting",
            "Humor",
        ],
        "how_it_works": "Mercury is your analytical processor. It governs software programming, rapid pattern recognition, and learning foreign languages.",
    },
    "Jupiter": {
        "sanskrit": "Guru / Brihaspati (गुरु)",
        "role": "The Mentor / The Expander",
        "keywords": [
            "Wisdom",
            "Higher Education",
            "Ethics",
            "Luck",
            "Expansion",
            "Mentors",
        ],
        "how_it_works": "Jupiter is the ultimate protector. Wherever Jupiter looks in your chart, it softens blows and brings grace, university degrees, and sound judgment.",
    },
    "Venus": {
        "sanskrit": "Shukra (शुक्र)",
        "role": "The Designer / The Harmonizer",
        "keywords": [
            "Love",
            "Marriage",
            "Aesthetics",
            "Hospitality",
            "Automobiles",
            "Refinement",
        ],
        "how_it_works": "Venus is how you connect with beauty, romantic partners, and luxury. It governs the visual arts, good food, and fine architecture.",
    },
    "Saturn": {
        "sanskrit": "Shani (शनि)",
        "role": "The Grand Architect / The Taskmaster",
        "keywords": [
            "Patience",
            "Discipline",
            "Old Age",
            "Labor",
            "Endurance",
            "Reality",
        ],
        "how_it_works": "Saturn does not give free gifts; it makes you earn everything through honest sweat. But what Saturn builds lasts forever.",
    },
    "Rahu": {
        "sanskrit": "Rahu (राहु)",
        "role": "The Rebel / The Frontier Explorer",
        "keywords": [
            "Unconventional Frontiers",
            "Emerging Tech",
            "Ambition",
            "Disruption",
            "Exploration",
        ],
        "how_it_works": "Rahu represents the frontier edge. It catalyzes exploration of unconventional domains, technological boundaries, and unfamiliar horizons.",
    },
    "Ketu": {
        "sanskrit": "Ketu (केतु)",
        "role": "The Ascetic / The Liberator",
        "keywords": [
            "Spiritual Liberation",
            "Detachment",
            "Mysticism",
            "Sudden Exits",
            "Moksha",
        ],
        "how_it_works": "Ketu is the knife that severs attachments. It teaches you that nothing in this material world is permanent, guiding the soul toward peace.",
    },
}


def explain_planet_placement(planet: str, house_num: int, sign_name: str) -> str:
    """
    Generates a simple, accessible 2-sentence explanation of a planet's placement for a layman.
    """
    p_info = PLANET_PROFILES.get(planet, {})
    role = p_info.get("role", "Cosmic Agent")

    house_meanings = {
        1: "your personal identity and physical vitality",
        2: "your core values, family roots, and resource management",
        3: "your courage, technical skills, and communicative efforts",
        4: "your inner peace, emotional grounding, and domestic sanctuary",
        5: "your intellect, creative expression, and inspiration",
        6: "your daily routines, problem-solving, and overcoming friction",
        7: "your interpersonal commitments, partnerships, and collaborative dynamics",
        8: "your deep psychological transformation, resilience, and hidden reserves",
        9: "your higher learning, guiding philosophies, and search for meaning",
        10: "your vocational trajectory, leadership, and public role",
        11: "your professional network, ambitions, and community gains",
        12: "unfamiliar environments, reflective solitude, and exploring distant horizons",
    }

    meaning = house_meanings.get(house_num, "this life arena")
    return f"{planet} ({role}) is stationed in {sign_name} in House {house_num}, actively shaping {meaning}."
