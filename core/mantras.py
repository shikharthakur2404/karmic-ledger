"""
karmic-ledger: Classical Vedic Mantra & Remedial Engine (Sastra Shanti)
Based on Rigvedic suktas, BPHS Dasha Shanti Adhyaya, and authentic Puranic sources.
Strictly authentic Sanskrit mantras with phonetic transliteration, meaning, and counts.
"""

from typing import Any

# Navagraha Beej and Gayatri Mantras for Dasha Pacification
PLANETARY_MANTRAS: dict[str, dict[str, Any]] = {
    "Sun": {
        "deity": "Surya Dev (Aditya)",
        "beej_mantra": "ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः",
        "transliteration": "Om Hraam Hreem Hroum Sah Sooryaaya Namah",
        "gayatri_mantra": "ॐ भास्कराय विद्महे महाद्युतिकराय धीमहि तन्नो सूर्यः प्रचोदयात्।",
        "ideal_count": "108 times at Sunrise on Sundays",
        "primary_benefit": "Confidence, health of father, vitality, government & administrative authority.",
    },
    "Moon": {
        "deity": "Chandra Dev / Shiva",
        "beej_mantra": "ॐ श्रां श्रीं श्रौं सः चन्द्रमसे नमः",
        "transliteration": "Om Shraam Shreem Shroum Sah Chandramase Namah",
        "gayatri_mantra": "ॐ क्षीरपुत्राय विद्महे अमृतत्त्वाय धीमहि तन्नो सोमः प्रचोदयात्।",
        "ideal_count": "108 times on Mondays or during evening",
        "primary_benefit": "Mental peace, emotional stability, mother's wellbeing, curing insomnia & overthinking.",
    },
    "Mars": {
        "deity": "Mangal Dev / Kartikeya / Hanuman Ji",
        "beej_mantra": "ॐ क्रां क्रीं क्रौं सः भौमाय नमः",
        "transliteration": "Om Kraam Kreem Kroum Sah Bhoumaaya Namah",
        "ideal_count": "108 times on Tuesdays facing South or East",
        "primary_benefit": "Courage, physical vitality, clearing property disputes, overcoming passive inertia.",
    },
    "Mercury": {
        "deity": "Budh Dev / Vishnu",
        "beej_mantra": "ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः",
        "transliteration": "Om Braam Breem Broum Sah Budhaaya Namah",
        "gayatri_mantra": "ॐ सौम्यरूपाय विद्महे वाणेशाय धीमहि तन्नो सौम्यः प्रचोदयात्।",
        "ideal_count": "108 times on Wednesdays facing North",
        "primary_benefit": "Computational logic, coding mastery, languages, eloquence, passing exams.",
    },
    "Jupiter": {
        "deity": "Brihaspati / Dakshinamurthy",
        "beej_mantra": "ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः",
        "transliteration": "Om Graam Greem Groum Sah Gurave Namah",
        "gayatri_mantra": "ॐ वृषभध्वजाय विद्महे करुणारूपाय धीमहि तन्नो गुरुः प्रचोदयात्।",
        "ideal_count": "108 times on Thursdays facing North-East",
        "primary_benefit": "Higher education, university admission, career promotion, wisdom, ethical wealth.",
    },
    "Venus": {
        "deity": "Shukracharya / Mahalakshmi",
        "beej_mantra": "ॐ द्रां द्रीं द्रौं सः शुक्राय नमः",
        "transliteration": "Om Draam Dreem Droum Sah Shukraaya Namah",
        "gayatri_mantra": "ॐ भृगुपुत्राय विद्महे दिव्यदेहाय धीमहि तन्नो शुक्रः प्रचोदयात्।",
        "ideal_count": "108 times on Fridays facing East",
        "primary_benefit": "Romantic harmony, marriage stabilization, artistic elegance, financial abundance.",
    },
    "Saturn": {
        "deity": "Shani Dev / Hanuman Ji",
        "beej_mantra": "ॐ प्रां प्रीं प्रौं सः शनैश्चराय नमः",
        "transliteration": "Om Praam Preem Proum Sah Shanaishcharaaya Namah",
        "mahamantra": "ॐ शं शनैश्चराय नमः",
        "ideal_count": "108 times on Saturdays after Sunset",
        "primary_benefit": "Patience, endurance through career struggles, protection from delays & litigation.",
    },
    "Rahu": {
        "deity": "Rahu / Durga / Bhairava",
        "beej_mantra": "ॐ भ्रां भ्रीं भ्रौं सः राहवे नमः",
        "transliteration": "Om Bhraam Bhreem Bhroum Sah Raahave Namah",
        "ideal_count": "108 times after Sunset facing South-West",
        "primary_benefit": "Neutralizing sudden corporate shocks, dispelling illusions, overseas foreign settlement.",
    },
    "Ketu": {
        "deity": "Ketu / Ganesha",
        "beej_mantra": "ॐ स्रां स्रीं स्रौं सः केतवे नमः",
        "transliteration": "Om Sraam Sreem Sroum Sah Ketave Namah",
        "ideal_count": "108 times at Dawn or Dusk",
        "primary_benefit": "Spiritual insight, resolving mysterious ailments, breaking cycles of grief & detachment.",
    },
}

# Domain-Specific Shanti and Karya Siddhi Mantras
DOMAIN_MANTRAS: dict[str, dict[str, Any]] = {
    "studies_and_exams": {
        "title": "Saraswati & Hayagriva Vidyaprapti Mantra",
        "deity": "Maa Saraswati & Lord Hayagriva (God of Learning)",
        "sanskrit": "ॐ ऐं वाग्देव्यै च विद्महे कामराजाय धीमहि। तन्नो देवी प्रचोदयात्॥",
        "transliteration": "Om Aim Vaagdevyai Cha Vidmahe Kaamaraajaaya Dheemahi | Tanno Devee Prachodayaat ||",
        "alternate": "ॐ ह्रीं श्रीं क्लीं सरस्वत्यै नमः",
        "context": "Ideal for Computer Science, engineering, mathematics, memory retention, and cracking exams.",
        "protocol": "Chant 11 or 21 times every morning before studying.",
    },
    "crisis_and_protection": {
        "title": "Sankatmochan Hanuman Raksha Mantra",
        "deity": "Sri Hanuman Ji",
        "sanskrit": "ॐ हं हनुमते नमः। कवन सो काज कठिन जग माहीं, जो नहिं होत तात तुम्ह पाहीं॥",
        "transliteration": "Om Ham Hanumate Namah | Kavana So Kaaja Kathina Jaga Maaheen, Jo Nahin Hota Taata Tumha Paaheen ||",
        "context": "For sudden hospitalizations, severe stress, legal battles, fear, and feeling trapped.",
        "protocol": "Recite 11 times or read Hanuman Chalisa on Tuesdays and Saturdays.",
    },
    "career_breakthrough": {
        "title": "Ganesha Vighna Nashaka Mantra",
        "deity": "Lord Ganesha",
        "sanskrit": "ॐ गं गणपतये नमः। वक्रतुण्ड महाकाय सूर्यकोटि समप्रभ। निर्विघ्नं कुरु मे देव सर्वकार्येषु सर्वदा॥",
        "transliteration": "Om Gam Ganapataye Namah | Vakratunda Mahaakaaya Sooryakoti Samaprabha | Nirvighnam Kuru Me Deva Sarva-Kaaryeshu Sarvadaa ||",
        "context": "For unblocking stalled job applications, starting a new job, or overcoming interview rejections.",
        "protocol": "Chant 21 times before submitting applications or entering interviews.",
    },
    "healing_and_longevity": {
        "title": "Maha Mrityunjaya Amrita Mantra",
        "deity": "Lord Shiva (Tryambaka)",
        "sanskrit": "ॐ त्र्यम्बकं यजामहे सुगन्धिं पुष्टिवर्धनम्। उर्वारुकमिव बन्धनान्मृ त्योर्मुक्षीय मामृतात्॥",
        "transliteration": "Om Tryambakam Yajaamahe Sugandhim Pushti-Vardhanam | Urvaarukam-Iva Bandhanaan Mrityor-Muksheeya Maamritaat ||",
        "context": "For serious chronic disease, parental health crises, and neutralizing critical maraka periods.",
        "protocol": "Recite 108 times using a Rudraksha mala.",
    },
    "financial_wealth": {
        "title": "Maha Lakshmi Kripa Mantra",
        "deity": "Goddess Mahalakshmi",
        "sanskrit": "ॐ श्रीं ह्रीं क्लीं श्रीं सिद्ध लक्ष्म्यै नमः॥",
        "transliteration": "Om Shreem Hreem Kleem Shreem Siddha Lakshmyai Namah ||",
        "context": "For cashflow instability, financial sovereignty, and stable savings.",
        "protocol": "Chant 108 times on Friday evenings.",
    },
}


def recommend_remedies_for_chart(
    active_mahadasha: str, active_antardasha: str, challenging_houses: list[int] = None
) -> dict[str, Any]:
    """
    Synthesizes custom remedial mantras based on the active dasha lords and life priorities.
    """
    maha_remedy = PLANETARY_MANTRAS.get(active_mahadasha, {})
    antar_remedy = PLANETARY_MANTRAS.get(active_antardasha, {})

    recommendations = {
        "active_dasha_shield": {
            "period": f"{active_mahadasha} - {active_antardasha}",
            "primary_mantra": antar_remedy.get("beej_mantra")
            or maha_remedy.get("beej_mantra"),
            "transliteration": antar_remedy.get("transliteration")
            or maha_remedy.get("transliteration"),
            "deity": antar_remedy.get("deity") or maha_remedy.get("deity"),
            "protocol": antar_remedy.get("ideal_count") or "108 times daily",
        },
        "karya_siddhi_anchors": [
            DOMAIN_MANTRAS["career_breakthrough"],
            DOMAIN_MANTRAS["studies_and_exams"],
            DOMAIN_MANTRAS["crisis_and_protection"],
        ],
    }

    return recommendations
