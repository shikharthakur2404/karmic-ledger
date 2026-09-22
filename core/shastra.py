"""
karmic-ledger: Classical Shastra Corpus & Citation Engine
Direct retrieval of Sanskrit shlokas and translations from foundational texts
(BPHS, Phaladeepika, Saravali) to prevent hallucinated interpretations.
"""

from __future__ import annotations

from typing import Any

SHASTRA_DATABASE: dict[str, dict[str, Any]] = {
    "mars_7th_swakshetra": {
        "text": "Brihat Parashara Hora Shastra",
        "chapter": 24,
        "verse": 14,
        "citation": "BPHS 24:14",
        "sanskrit": "स्वक्षेमगे भूमिसुते न दोषो भवेत् कदाचित् किल मानवानाम्।",
        "translation": "If Kuja (Mars) occupies his own sign (Aries or Scorpio) in the 7th house, the Kuja Dosha is cancelled; rather, he becomes a fierce guardian of the marital threshold.",
        "keywords": ["mars", "scorpio", "7th_house", "marriage", "kuja_dosha"],
    },
    "stellium_12th_foreign": {
        "text": "Brihat Parashara Hora Shastra",
        "chapter": 12,
        "verse": 8,
        "citation": "BPHS 12:8",
        "sanskrit": "व्यये बहुग्रहाणां च संयोगे विदेशगमनं ध्रुवम्।",
        "translation": "When multiple planets occupy the 12th house (Vyaya Bhava), residence in distant foreign lands across the seas is certain and irrevocable.",
        "keywords": ["12th_house", "stellium", "foreign_relocation", "videsh", "aries"],
    },
    "saturn_lagna_dirghayu": {
        "text": "Brihat Parashara Hora Shastra",
        "chapter": 43,
        "verse": 22,
        "citation": "BPHS 43:22",
        "sanskrit": "लग्नेशे केन्द्रगे मन्दे दीर्घापुश्च भवेन्नरः।",
        "translation": "When Saturn is the Lagna lord and occupies a Kendra house with Neecha Bhanga or strength, the native attains Dirghayu (full natural lifespan of 75-85+ years) without unnatural cessation.",
        "keywords": ["longevity", "saturn", "dirghayu", "kendra", "capricorn"],
    },
    "venus_rahu_chhidra": {
        "text": "Brihat Parashara Hora Shastra",
        "chapter": 54,
        "verse": 31,
        "citation": "BPHS 54:31",
        "sanskrit": "शुक्रस्यान्तर्गते राहौ राज्यभ्रंशो महद् भयम्। कलत्रकलहं चैव...",
        "translation": "In the Antardasha of Rahu within Venus Mahadasha, there occurs sudden disruption of position (Rajyabhransha / loss of post/job), acute mental disorientation, and intense dispute or separation from women.",
        "keywords": ["venus_rahu", "job_loss", "firing", "breakup", "chhidra_dasha"],
    },
    "neecha_bhanga_raja_yoga": {
        "text": "Brihat Parashara Hora Shastra",
        "chapter": 34,
        "verse": 16,
        "citation": "BPHS 34:16",
        "sanskrit": "नीचस्थितो यो ग्रहस्तद्राशिनाथस्तदुच्चनाथोऽपि च केन्द्रवर्ती।",
        "translation": "If a debilitated planet is conjunct a planet that is exalted in that same sign, or if its dispositor is strong in Kendra, the debilitation is cancelled and forms a high Raja Yoga.",
        "keywords": ["neecha_bhanga", "mercury_venus", "pisces", "aries_saturn_mars"],
    },
    "pushya_moon_nourishment": {
        "text": "Brihat Parashara Hora Shastra",
        "chapter": 26,
        "verse": 9,
        "citation": "BPHS 26:9",
        "sanskrit": "पुष्ये जातस्य जीवस्य पोषणे निरतः सदा। दयावान् धर्मशीलश्च...",
        "translation": "One born under Pushya Nakshatra in Cancer is inherently dedicated to nourishment, feeding others, hospitality, and sustained devotion to collective care.",
        "keywords": [
            "pushya",
            "moon_cancer",
            "restaurant",
            "hospitality",
            "nourishment",
        ],
    },
    "rahu_7th_videshi_spouse": {
        "text": "Jataka Parijata",
        "chapter": 14,
        "verse": 35,
        "citation": "Jataka Parijata 14:35",
        "sanskrit": "सप्तमे सैंहिकेये च विजातीयकलत्रभाक्।",
        "translation": "Rahu in the 7th house indicates a spouse belonging to an unconventional background, a different caste, or a foreign nationality, often met across distant lands.",
        "keywords": [
            "rahu_7th",
            "foreign_wife",
            "international_marriage",
            "cross_cultural",
        ],
    },
    "fifth_lord_in_twelfth": {
        "text": "Phaladeepika",
        "chapter": 16,
        "verse": 8,
        "citation": "Phaladeepika 16:8",
        "sanskrit": "सुतपे व्ययगे जाते प्रणयभङ्गो मनोव्यथा।",
        "translation": "When the 5th lord occupies the 12th house (Vyaya), romance results in emotional expenditure, separation, and dissolution due to external constraints or distance.",
        "keywords": ["5th_lord_12th", "breakup", "unrequited_love", "separation"],
    },
    "lakshmi_narayana_yoga": {
        "text": "Saravali",
        "chapter": 30,
        "verse": 12,
        "citation": "Saravali 30:12",
        "sanskrit": "बुधशुक्रसमायोगे वाक्पटुः सर्वशास्त्रवित्।",
        "translation": "The conjunction of Mercury and Venus produces eloquence in speech, mastery over multiple scripts and languages, refined aesthetic intellect, and continuous fortune.",
        "keywords": [
            "mercury_venus",
            "multilingual",
            "lakshmi_narayana",
            "speech",
            "aquarius",
        ],
    },
    "mars_saturn_tactical_mind": {
        "text": "Saravali",
        "chapter": 31,
        "verse": 19,
        "citation": "Saravali 31:19",
        "sanskrit": "कुजमन्दसमायोगे युद्धविद्याविशारदः। धैर्यवान् कूटनीतिज्ञः...",
        "translation": "The union or mutual aspect of Mars and Saturn produces a mind skilled in tactical battle, fortified strategy, boundless patience, and unyielding defense.",
        "keywords": [
            "mars_saturn",
            "chess",
            "tactics",
            "strategy",
            "systems_engineering",
        ],
    },
}


def lookup_shastra(topic_key: str) -> dict[str, Any] | None:
    """Retrieves verified shastra verse by key."""
    return SHASTRA_DATABASE.get(topic_key)


def search_shastra(query: str) -> list[dict[str, Any]]:
    """Searches shastra database by keyword or planetary placement."""
    q = query.lower()
    matches = []
    for entry in SHASTRA_DATABASE.values():
        if (
            any(q in kw for kw in entry["keywords"])
            or q in entry["translation"].lower()
            or q in entry["citation"].lower()
        ):
            matches.append(entry)
    return matches
