"""
karmic-ledger: Engine 11 — Saṃskāra & Karmic Trace Engine (Karma-Trace v1.0.0)
Translates classical Sanskrit textual frameworks (Yoga Sūtra 3.18, BPHS Ch. 84,
Bṛhat Jātaka, Bhagavad Gītā 2.22 / 4.5) and academic case literature (UVA DOPS)
into an auditable, text-grounded computational model with strict epistemic boundaries.

Strict Epistemic Primacy:
- Layer 1: Textual / Scriptural Claims (Exact Sanskrit verses and verified sources).
- Layer 2: Traditional Jyotiṣa Interpretations (Drekkāṇa Loka & Pūrva Puṇya classifications).
- Layer 3: Empirical Research Benchmarks (Comparative feature overlap without asserting literal identity).
Zero assertions of unverified literal historical identities or supernatural certainty.
"""

from __future__ import annotations

from typing import Any, Optional

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

# BPHS Ch. 84 / Bṛhat Jātaka Drekkāṇa Lord -> Realm (Loka) Mapping
LOKA_MAPPING: dict[str, dict[str, Any]] = {
    "Jupiter": {
        "loka": "Devaloka",
        "sanskrit": "देवलोक",
        "description": "Higher celestial realm of wisdom, contemplative virtue, and divine philosophy.",
        "epistemic_grade": "Subtle / Elevated",
        "traditional_realm_lord": "Brihaspati (The Guru of the Gods)",
    },
    "Venus": {
        "loka": "Pitṛloka",
        "sanskrit": "पितृलोक",
        "description": "Ancestral lunar realm of aesthetic refinement, familial continuity, and affectionate duty.",
        "epistemic_grade": "Lunar / Ancestral",
        "traditional_realm_lord": "Shukra (The Harmonizer / Regent of Ojas)",
    },
    "Moon": {
        "loka": "Pitṛloka",
        "sanskrit": "पितृलोक",
        "description": "Ancestral realm of emotional memory, maternal protection, and familial bonds.",
        "epistemic_grade": "Lunar / Ancestral",
        "traditional_realm_lord": "Chandra (The Sustainer of Mind)",
    },
    "Sun": {
        "loka": "Mṛtyuloka",
        "sanskrit": "मृत्युलोक (भूलोक)",
        "description": "Terrestrial mortal realm of sovereign struggle, executive dharma, and visible action.",
        "epistemic_grade": "Terrestrial / Sovereign",
        "traditional_realm_lord": "Surya (The Cosmic Witness)",
    },
    "Mars": {
        "loka": "Mṛtyuloka / Tiryagloka",
        "sanskrit": "मृत्युलोक / तिर्यग्लोक",
        "description": "Active terrestrial realm of intense physical testing, strategic courage, and friction.",
        "epistemic_grade": "Terrestrial / Dynamic",
        "traditional_realm_lord": "Mangala (The Commander)",
    },
    "Mercury": {
        "loka": "Naraka / Pātāla",
        "sanskrit": "पाताल / विमर्शन-लोक",
        "description": "Dense communicative or subterranean realm of intellectual labor and transactional balance.",
        "epistemic_grade": "Subterranean / Intellectual Exhaustion",
        "traditional_realm_lord": "Budha (The Intellect)",
    },
    "Saturn": {
        "loka": "Naraka / Pātāla",
        "sanskrit": "पाताल / तपस्-लोक",
        "description": "Dense foundational realm of heavy duty, endurance testing, and karmic purification.",
        "epistemic_grade": "Subterranean / Ascetic Duty",
        "traditional_realm_lord": "Shani (The Great Taskmaster)",
    },
}

# Canonical Shastric Provenance Corpus
SAMSKARA_SHASTRA_CITATIONS: list[dict[str, str]] = [
    {
        "id": "YS-3.18",
        "tradition": "Yoga Darśana",
        "text": "Patañjali Yoga Sūtras",
        "chapter": "3 (Vibhūti Pāda)",
        "verse": "18",
        "sanskrit": "संस्कारसाक्षात्करणात् पूर्वजातिज्ञानम्॥",
        "iast": "saṃskāra-sākṣātkaraṇāt pūrva-jāti-jñānam",
        "translation": "Through direct intuitive perception (sākṣātkāraṇa) of latent impressions (saṃskāras), knowledge of prior births arises.",
        "source_url": "https://www.gitasupersite.iitk.ac.in/dv/yogasutra/3.18",
        "epistemic_layer": "Textual Claim (Phenomenology of Consciousness)",
    },
    {
        "id": "BPHS-84.1-4",
        "tradition": "Parāśarī Jyotiṣa",
        "text": "Bṛhat Parāśara Horā Śāstra",
        "chapter": "84 (Pūrva-Janma-Loka-Adhyāya)",
        "verse": "1-4",
        "sanskrit": "सूर्येन्द्वोर्बलिनो ज्ञेयो द्रेष्काणेशः शुभो यदि। देवलोकात् समायातो...",
        "iast": "sūryendvor balino jñeyo dreṣkāṇeśaḥ śubho yadi | devalokāt samāyāto...",
        "translation": "Between the Sun and the Moon, identify the stronger luminary. The lord of its Drekkāṇa (D3 decanate) indicates the realm from which the soul arrived: Jupiter indicates Devaloka, Venus/Moon Pitṛloka, Sun/Mars Mṛtyuloka, Mercury/Saturn Pātāla.",
        "source_url": "https://vedic-astro.s3.amazonaws.com/books/bhrihat_parasara_hora_shastra.pdf",
        "epistemic_layer": "Traditional Astrological Interpretation",
    },
    {
        "id": "BG-2.22",
        "tradition": "Vedānta / Itihāsa",
        "text": "Bhagavad Gītā",
        "chapter": "2",
        "verse": "22",
        "sanskrit": "वासांसि जीर्णानि यथा विहाय नवानि गृह्णाति नरोऽपराणि। तथा शरीराणि विहाय जीर्णान्यन्यानि संयाति नवानि देही॥",
        "iast": "vāsāṁsi jīrṇāni yathā vihāya navāni gṛhṇāti naro 'parāṇi | tathā śarīrāṇi vihāya jīrṇāny anyāni saṁyāti navāni dehī",
        "translation": "As a person discards worn-out garments and dons new ones, the embodied soul discards worn-out bodies and enters into other new ones.",
        "source_url": "https://www.gitasupersite.iitk.ac.in/srimad?field_chapter_value=2&field_nsutra_value=22",
        "epistemic_layer": "Philosophical Metaphor",
    },
    {
        "id": "BG-4.5",
        "tradition": "Vedānta / Itihāsa",
        "text": "Bhagavad Gītā",
        "chapter": "4",
        "verse": "5",
        "sanskrit": "बहूनि मे व्यतीतानि जन्मानि तव चार्जुन। तान्यहं वेद सर्वाणि न त्वं वेत्थ परन्तप॥",
        "iast": "bahūni me vyatītāni janmāni tava cārjuna | tāny ahaṁ veda sarvāṇi na tvaṁ vettha parantapa",
        "translation": "Many births have passed for Me and for you, O Arjuna. I know them all, but you do not know them, O scorcher of foes.",
        "source_url": "https://vedabase.io/en/library/bg/4/5/",
        "epistemic_layer": "Epistemic Distinction (Human Forgetting vs Transmigration)",
    },
    {
        "id": "BU-4.4.5",
        "tradition": "Upaniṣad",
        "text": "Bṛhadāraṇyaka Upaniṣad",
        "chapter": "4",
        "verse": "4.5",
        "sanskrit": "यथाकारी यथाचारी तथा भवति — साधुकारी साधुर्भवति, पापकारी पापो भवति...",
        "iast": "yathākārī yathācārī tathā bhavati — sādhukārī sādhur bhavati, pāpakārī pāpo bhavati...",
        "translation": "According as one acts and according as one conducts oneself, so does one become. The doer of good becomes good, the doer of evil becomes evil.",
        "source_url": "https://www.wisdomlib.org/hinduism/book/the-brihadaranyaka-upanishad/d/doc122058.html",
        "epistemic_layer": "Causal Karma Ontology",
    },
]

# UVA DOPS Literature Reference Case Archetypes
UVA_DOPS_CASE_ARCHETYPES: list[dict[str, Any]] = [
    {
        "case_id": "UVA-ARCH-01",
        "archetype": "Spontaneous Technical & Linguistic Precocity",
        "domain": "Intellectual / Craft Mastery",
        "salient_features": [
            "unlearned_engineering_instinct",
            "early_facility_with_languages",
            "affinity_for_system_architecture",
        ],
        "literature_precedent": "Documented cases of spontaneous mechanical proficiency and unlearned linguistic affinity reported before age 6 (Tucker 2005, Stevenson 1987).",
        "epistemic_note": "Observed correlation with early childhood cognitive variance, non-assertive match.",
    },
    {
        "case_id": "UVA-ARCH-02",
        "archetype": "Specific Geographic & Cultural Gravitation",
        "domain": "Environmental Affinity",
        "salient_features": [
            "unprompted_cultural_comfort",
            "historical_era_resonance",
            "foreign_land_gravitation",
        ],
        "literature_precedent": "Subjects demonstrating pronounced behavioral comfort in distant cultural or geographical frameworks without domestic exposure (Stevenson 1997).",
        "epistemic_note": "Psychological affinity metric; does not establish physical identity.",
    },
    {
        "case_id": "UVA-ARCH-03",
        "archetype": "Innate Specific Phobia & Environmental Aversion",
        "domain": "Autonomic / Sensorial Reactivity",
        "salient_features": [
            "unexplained_water_aversion",
            "extreme_cold_sensitivity",
            "confinement_discomfort",
        ],
        "literature_precedent": "Children reporting specific past-life trauma exhibiting autonomic phobias congruent with reported circumstances (Stevenson 1990).",
        "epistemic_note": "Autonomic stress reflex; multiple psychological explanations exist.",
    },
    {
        "case_id": "UVA-ARCH-04",
        "archetype": "Contemplative & Ascetic Detachment",
        "domain": "Philosophical / Spiritual Orientation",
        "salient_features": [
            "innate_disregard_for_trivial_status",
            "preference_for_solitude",
            "unlearned_ethical_gravity",
        ],
        "literature_precedent": "Spontaneous ascetic preferences and early-onset religious rituals observed in pediatric subjects prior to family instruction (Haraldsson 2000).",
        "epistemic_note": "Dispositional trait profile; consistent with end-cycle detachment.",
    },
]


def _get_sign_index(sign: str) -> int:
    return ZODIAC_SIGNS.index(sign) if sign in ZODIAC_SIGNS else 0


def _compute_drekkana_lord(sign: str, degree_in_sign: float) -> tuple[str, int, str]:
    """
    Computes Drekkāṇa (D3) decanate (1 to 3), the resulting sign, and its lord.
    - Decanate 1 (0° to 10°): Same sign
    - Decanate 2 (10° to 20°): 5th sign from current
    - Decanate 3 (20° to 30°): 9th sign from current
    """
    base_idx = _get_sign_index(sign)
    if degree_in_sign < 10.0:
        decanate = 1
        d3_sign_idx = base_idx
    elif degree_in_sign < 20.0:
        decanate = 2
        d3_sign_idx = (base_idx + 4) % 12
    else:
        decanate = 3
        d3_sign_idx = (base_idx + 8) % 12

    d3_sign = ZODIAC_SIGNS[d3_sign_idx]
    d3_lord = SIGN_LORDS[d3_sign]
    return d3_lord, decanate, d3_sign


def compute_drekkana_loka(natal: dict[str, Any]) -> dict[str, Any]:
    """
    Evaluates Sun vs Moon dignity/strength, computes D3 Drekkāṇa decanate,
    identifies the Drekkāṇa lord, and classifies the Pūrva Janma Loka (BPHS Ch. 84).
    """
    planets = natal.get("planets", {})
    sun = planets.get("Sun", {})
    moon = planets.get("Moon", {})

    sun_deg = sun.get("degree_in_sign", 15.0)
    sun_sign = sun.get("sign", "Aries")
    sun_dignity = sun.get("dignity", "Neutral")

    moon_deg = moon.get("degree_in_sign", 15.0)
    moon_sign = moon.get("sign", "Taurus")
    moon_dignity = moon.get("dignity", "Neutral")

    # Evaluate stronger luminary between Sun and Moon
    dignity_ranks = {
        "Exalted (Uccha)": 5,
        "Own Sign (Swakshetra)": 4,
        "Moolatrikona": 4,
        "Neutral": 2,
        "Debilitated (Neecha)": 1,
    }
    sun_score = dignity_ranks.get(sun_dignity, 2)
    moon_score = dignity_ranks.get(moon_dignity, 2)

    if sun_score > moon_score:
        stronger_luminary = "Sun"
        target_sign = sun_sign
        target_deg = sun_deg
        luminary_dignity = sun_dignity
    elif moon_score > sun_score:
        stronger_luminary = "Moon"
        target_sign = moon_sign
        target_deg = moon_deg
        luminary_dignity = moon_dignity
    else:
        # Tie-breaker: Moon has higher degree in sign (maturation)
        if moon_deg >= sun_deg:
            stronger_luminary = "Moon"
            target_sign = moon_sign
            target_deg = moon_deg
            luminary_dignity = moon_dignity
        else:
            stronger_luminary = "Sun"
            target_sign = sun_sign
            target_deg = sun_deg
            luminary_dignity = sun_dignity

    drekkana_lord, decanate_num, d3_sign = _compute_drekkana_lord(
        target_sign, target_deg
    )
    loka_info = LOKA_MAPPING.get(
        drekkana_lord,
        {
            "loka": "Mṛtyuloka",
            "sanskrit": "मृत्युलोक",
            "description": "Terrestrial human plane of action and development.",
            "epistemic_grade": "Terrestrial",
            "traditional_realm_lord": drekkana_lord,
        },
    )

    return {
        "stronger_luminary": stronger_luminary,
        "luminary_sign": target_sign,
        "luminary_degree": round(target_deg, 2),
        "luminary_dignity": luminary_dignity,
        "decanate": decanate_num,
        "drekkana_sign": d3_sign,
        "drekkana_lord": drekkana_lord,
        "purva_janma_loka": loka_info["loka"],
        "loka_sanskrit": loka_info["sanskrit"],
        "loka_description": loka_info["description"],
        "loka_epistemic_grade": loka_info["epistemic_grade"],
        "citation": "BPHS Ch. 84:1-4 & Bṛhat Jātaka",
    }


def evaluate_purva_punya_houses(natal: dict[str, Any]) -> dict[str, Any]:
    """
    Analyzes House 9 (Pūrva Puṇya / Past Virtue), House 5 (Pūrva Janma Saṃskāras),
    and House 12 (Moksha & Dissolution) to map karmic heritage themes.
    """
    lagna = natal.get("lagna", {})
    lagna_sign = lagna.get("sign", "Taurus")
    lagna_idx = _get_sign_index(lagna_sign)
    planets = natal.get("planets", {})

    # Compute signs for H5, H9, H12
    h5_sign = ZODIAC_SIGNS[(lagna_idx + 4) % 12]
    h9_sign = ZODIAC_SIGNS[(lagna_idx + 8) % 12]
    h12_sign = ZODIAC_SIGNS[(lagna_idx + 11) % 12]

    h5_lord = SIGN_LORDS[h5_sign]
    h9_lord = SIGN_LORDS[h9_sign]
    h12_lord = SIGN_LORDS[h12_sign]

    def occupants_of_house(house_num: int) -> list[str]:
        occ = []
        for p_name, p_data in planets.items():
            if p_data.get("house") == house_num:
                occ.append(p_name)
        return occ

    h5_planets = occupants_of_house(5)
    h9_planets = occupants_of_house(9)
    h12_planets = occupants_of_house(12)

    # Assess 9th House Pūrva Puṇya Vector
    h9_theme = (
        f"House 9 in {h9_sign} (Lord: {h9_lord}). Occupants: {', '.join(h9_planets) if h9_planets else 'None'}. "
        "Governs pre-accumulated spiritual credits, philosophical inclinations, and ancestral merit."
    )
    if "Ketu" in h9_planets:
        h9_theme += " Ketu in House 9 indicates pre-learned instinctual detachment from ritual dogma and pre-acquired metaphysical wisdom."

    # Assess 5th House Saṃskāra Vector
    h5_theme = (
        f"House 5 in {h5_sign} (Lord: {h5_lord}). Occupants: {', '.join(h5_planets) if h5_planets else 'None'}. "
        "Governs creative intelligence seeds and mental impressions carried from prior embodiments."
    )

    # Assess 12th House Vyaya/Moksha Vector
    h12_theme = (
        f"House 12 in {h12_sign} (Lord: {h12_lord}). Occupants: {', '.join(h12_planets) if h12_planets else 'None'}. "
        "Governs the dissolution of residual debt (Nirjara), foreign relocation, and transcendent release."
    )
    if "Saturn" in h12_planets or "Sun" in h12_planets:
        h12_theme += " Heavy luminaries/malefics in 12th signify structural exhaustion of past worldly ties through solitude or cross-border displacement."

    return {
        "house_5": {
            "sign": h5_sign,
            "lord": h5_lord,
            "occupants": h5_planets,
            "theme": h5_theme,
        },
        "house_9": {
            "sign": h9_sign,
            "lord": h9_lord,
            "occupants": h9_planets,
            "theme": h9_theme,
        },
        "house_12": {
            "sign": h12_sign,
            "lord": h12_lord,
            "occupants": h12_planets,
            "theme": h12_theme,
        },
    }


def _normalize_feature_lists(
    user_features: Optional[dict[str, Any]],
) -> tuple[list[str], list[str], list[str]]:
    if not user_features:
        return [], [], []
    affinities = [str(x).strip() for x in (user_features.get("affinities") or []) if str(x).strip()]
    fears = [
        str(x).strip()
        for x in (user_features.get("fears_or_sensitivities") or [])
        if str(x).strip()
    ]
    talents = [
        str(x).strip()
        for x in (user_features.get("spontaneous_talents") or [])
        if str(x).strip()
    ]
    return affinities, fears, talents


def profile_samskara_latent_impressions(
    user_features: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """
    Yoga Sūtra 3.18 Saṃskāra Profiler.
    Ingests the querent's own self-reported affinities / fears / talents.
    Never invents a personal default profile (no operator / demo-identity fallback).
    """
    affinities, fears, talents = _normalize_feature_lists(user_features)
    awaiting = {
        "status": "AWAITING_USER_FEATURES",
        "declared_affinities": affinities,
        "declared_fears_and_sensitivities": fears,
        "declared_spontaneous_talents": talents,
        "dominant_samskara_archetype": None,
        "archetype_description": (
            "Saṃskāra impression profiling needs this person's own affinities, "
            "fears, and talents. No personal defaults are applied, so the result "
            "cannot be biased toward any demo profile."
        ),
        "vector_scores": {},
        "sutra_reference": "YS 3.18 (saṃskāra-sākṣātkaraṇāt pūrva-jāti-jñānam)",
    }
    if not (affinities or fears or talents):
        return awaiting

    intellectual_score = 0.0
    strategic_score = 0.0
    ascetic_score = 0.0
    relational_score = 0.0

    all_text = " ".join(affinities + fears + talents).lower()

    if any(
        k in all_text
        for k in ["system", "architecture", "shastra", "code", "engineering"]
    ):
        intellectual_score += 0.85
    if any(
        k in all_text
        for k in ["strategy", "leadership", "duty", "endurance", "protect"]
    ):
        strategic_score += 0.75
    if any(
        k in all_text
        for k in ["metaphysics", "solitude", "autonomy", "ascetic", "detach"]
    ):
        ascetic_score += 0.80
    if any(
        k in all_text
        for k in ["relational", "boundary", "intimacy", "sincerity", "love"]
    ):
        relational_score += 0.65

    scores = {
        "Jnāna-Mārga (The Scholar-Architect)": intellectual_score,
        "Kṣatriya-Rakṣaka (The Sovereign Strategist)": strategic_score,
        "Tapasvī-Yogi (The Detached Contemplative)": ascetic_score,
        "Rasajña-Bandhu (The Sincere Harmonizer)": relational_score,
    }
    peak = max(scores.values())
    if peak <= 0.0:
        return {
            **awaiting,
            "status": "NO_ARCHETYPE_KEYWORD_MATCH",
            "declared_affinities": affinities,
            "declared_fears_and_sensitivities": fears,
            "declared_spontaneous_talents": talents,
            "archetype_description": (
                "Features were provided, but none matched the registered archetype "
                "keyword table. No dominant archetype is assigned by default."
            ),
            "vector_scores": {k: round(v, 2) for k, v in scores.items()},
        }

    dominant_archetype = max(scores, key=scores.get)

    archetype_descriptions = {
        "Jnāna-Mārga (The Scholar-Architect)": (
            "Deeply rooted latent impression (saṃskāra) toward technical deconstruction, "
            "synthesizing high-dimensional models, and codifying knowledge. Instinctively treats the cosmos as an auditable code base."
        ),
        "Kṣatriya-Rakṣaka (The Sovereign Strategist)": (
            "Latent impressions oriented around protective stewardship, enduring heavy operational pressure, "
            "and maintaining firm structural boundaries against chaos."
        ),
        "Tapasvī-Yogi (The Detached Contemplative)": (
            "Pre-learned detachment and solitude tolerance. Indifferent to trivial social accolades, "
            "prioritizing inner liberation, self-discipline, and resolution of lingering karmic threads."
        ),
        "Rasajña-Bandhu (The Sincere Harmonizer)": (
            "Latent impressions exploring deep relational integrity, honoring mutual contracts, and clearing past relational debts."
        ),
    }

    return {
        "status": "PROFILED_FROM_USER_FEATURES",
        "declared_affinities": affinities,
        "declared_fears_and_sensitivities": fears,
        "declared_spontaneous_talents": talents,
        "dominant_samskara_archetype": dominant_archetype,
        "archetype_description": archetype_descriptions.get(dominant_archetype, ""),
        "vector_scores": {k: round(v, 2) for k, v in scores.items()},
        "sutra_reference": "YS 3.18 (saṃskāra-sākṣātkaraṇāt pūrva-jāti-jñānam)",
    }


def match_historical_case_benchmark(
    features: Optional[dict[str, Any]] = None,
) -> list[dict[str, Any]]:
    """
    Mode 3: Empirical Case Matching against UVA DOPS Research Literature.
    Ranks benchmark case patterns by keyword overlap with the querent's features.
    Without features, returns no matches (never a hardcoded High Fit for any case).
    """
    affinities, fears, talents = _normalize_feature_lists(features)
    if not (affinities or fears or talents):
        return []

    all_text = " ".join(affinities + fears + talents).lower()
    # Lightweight token overlap against each case's salient_features labels
    matches: list[dict[str, Any]] = []
    for case in UVA_DOPS_CASE_ARCHETYPES:
        tokens = [
            t.replace("_", " ")
            for t in case.get("salient_features", [])
        ]
        hits = sum(1 for t in tokens if any(part in all_text for part in t.split()))
        if hits <= 0:
            similarity = "Low / No Keyword Overlap"
        elif hits == 1:
            similarity = "Moderate Baseline"
        else:
            similarity = "High Fit (Qualitative Congruence)"
        matches.append(
            {
                "case_id": case["case_id"],
                "archetype": case["archetype"],
                "domain": case["domain"],
                "keyword_hits": hits,
                "conceptual_similarity": similarity,
                "literature_reference": case["literature_precedent"],
                "epistemic_safety_note": case["epistemic_note"],
            }
        )
    matches.sort(key=lambda m: m["keyword_hits"], reverse=True)
    return matches


def generate_samskara_report(
    natal: dict[str, Any],
    user_features: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """
    Master Coordinator for Engine 11: Saṃskāra & Karmic Trace Engine.
    Combines:
    1. Deterministic Jyotiṣa Drekkāṇa (D3) Loka & Pūrva Puṇya analysis
    2. Yoga Sūtra 3.18 Saṃskāra latent impression profiling (user features only)
    3. UVA DOPS academic literature benchmark matching (user features only)
    4. Exact Sanskrit source citations with 3-layer epistemic boundaries.
    """
    drekkana_loka = compute_drekkana_loka(natal)
    purva_punya = evaluate_purva_punya_houses(natal)
    samskara_profile = profile_samskara_latent_impressions(user_features)
    case_benchmarks = match_historical_case_benchmark(user_features)
    features_ready = samskara_profile.get("status") == "PROFILED_FROM_USER_FEATURES"

    return {
        "engine_id": "11",
        "engine_name": "Saṃskāra & Karmic Trace Engine (Karma-Trace)",
        "version": "1.1.0",
        "status": "OPERATIONAL",
        "features_status": samskara_profile.get("status", "AWAITING_USER_FEATURES"),
        "epistemic_status": {
            "traditional_interpretation": True,
            "empirical_confirmation": False,
            "literal_identity_claimed": False,
            "scientific_classification": "RESEARCH_PHENOMENOLOGY_ONLY",
            "personal_defaults_forbidden": True,
            "epistemic_notice": (
                "Path A (Drekkāṇa / Pūrva Puṇya) is chart-derived. "
                "Paths B/C only run on the querent's own declared features — "
                "never on a developer or demo identity. "
                "Classical Sanskrit rules and qualitative case matching provide reflective archetypal models. "
                "Neither software nor scripture asserts verifiable historical identity."
            ),
        },
        "path_a_jyotisha": {
            "drekkana_loka": drekkana_loka,
            "purva_punya_houses": purva_punya,
        },
        "path_b_samskara": samskara_profile,
        "path_c_research_benchmark": {
            "benchmark_corpus": "University of Virginia Division of Perceptual Studies (UVA DOPS)",
            "case_matches": case_benchmarks,
            "status": "MATCHED" if features_ready else "AWAITING_USER_FEATURES",
        },
        "shastric_citations": SAMSKARA_SHASTRA_CITATIONS,
    }
