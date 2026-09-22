"""
karmic-ledger: Manuscript & Telemetry Dossier Generator
Compiles comprehensive, layman-friendly, visual dossiers with mantras, primer, and SVG Kundlis.
"""

import json
import os
from datetime import datetime

from core.dasha import compute_vimshottari_timeline, get_active_dasha_at_date
from core.ephemeris import compute_natal_chart
from core.mantras import DOMAIN_MANTRAS, recommend_remedies_for_chart
from core.primer import explain_planet_placement
from core.verifier import verify_profile_milestones


def generate_markdown_dossier(profile_path: str, output_path: str) -> str:
    """Generates a complete, publication-grade Markdown dossier for a subject."""
    with open(profile_path, encoding="utf-8") as f:
        data = json.load(f)

    bdata = data.get("birth_data", {})
    date_parts = [int(p) for p in bdata.get("date", "2000-01-01").split("-")]
    time_str = bdata.get("time") or bdata.get("rectified_time", "07:00:00")

    hour, minute, second = 7, 0, 0
    if ":" in time_str:
        clean_time = time_str.split()[0]
        t_parts = clean_time.split(":")
        hour = int(t_parts[0])
        minute = int(t_parts[1]) if len(t_parts) > 1 else 0
        second = int(t_parts[2]) if len(t_parts) > 2 else 0

    lat = float(bdata.get("latitude", 20.0))
    lon = float(bdata.get("longitude", 78.0))

    # 1. Ephemeris & Dasha Math
    natal = compute_natal_chart(
        year=date_parts[0],
        month=date_parts[1],
        day=date_parts[2],
        hour=hour,
        minute=minute,
        second=second,
        lat=lat,
        lon=lon,
        tz_offset_hours=5.5,
    )

    birth_dt = datetime(
        date_parts[0], date_parts[1], date_parts[2], hour, minute, second
    )
    moon_nak = natal["planets"]["Moon"]["nakshatra"]

    timeline = compute_vimshottari_timeline(
        birth_dt=birth_dt,
        moon_nakshatra_lord=moon_nak["lord"],
        fraction_elapsed=moon_nak["fraction_elapsed"],
    )

    # Active Dasha Right Now (2026)
    current_dt = datetime(2026, 9, 20)
    current_dasha = get_active_dasha_at_date(timeline, current_dt)

    # 2. Verification
    res = verify_profile_milestones(profile_path)
    if res.get("status") == "PROCESSING_HALTED":
        locked_content = f"# 🔒 KARMIC LEDGER | DOSSIER LOCKED\n\n**STATUS:** {res.get('error')}\n**REASON:** {res.get('reason')}\n\nExecution halted. Affirmative subject consent is mandatory before compiling dossiers on private individuals.\n"
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(locked_content)
        return output_path
    remedies = recommend_remedies_for_chart(
        active_mahadasha=current_dasha.get("mahadasha", "Mercury"),
        active_antardasha=current_dasha.get("antardasha", "Jupiter"),
    )

    # 4. Layman Explanations
    planet_explanations = []
    for p_name, p_val in natal["planets"].items():
        exp = explain_planet_placement(p_name, p_val["house"], p_val["sign"])
        planet_explanations.append(
            f"* **{p_name} in {p_val['formatted']} (House {p_val['house']})**: {exp}"
        )

    # Build Content
    md_content = f"""# 🪐 KARMIC LEDGER | Master Dossier: {res["subject"]}
*Scientific Telemetry Engine | Lahiri Sidereal Ephemeris | Sanskrit Sastra Grounding*

---

## 1. Core Natal Coordinates & Ascendant
* **Ascendant (Lagna):** `{res["lagna"]}` — Your physical operating system and how you engage with reality.
* **Moon Sign (Rashi):** `{natal["planets"]["Moon"]["sign"]}` | **Nakshatra:** `{res["moon_nakshatra"]}`
* **Currently Active Dasha (2026):** **`{current_dasha.get("mahadasha")} - {current_dasha.get("antardasha")}`** (Active until `{current_dasha.get("period_end")}`)
* **Average Vedic Correlation Score (VCS):** **`{res["average_vedic_correlation_score"]}`**

---

## 2. Plain-English "Planet Primer" (What Your Chart Actually Does)

{chr(10).join(planet_explanations)}

---

## 3. Verified Milestone Backtesting Matrix

| Milestone Event | Active Dasha Cycle | Transit Saturn | Classical Shastra Citation | Correlation Score |
|---|---|---|---|---|
"""
    for m in res["calibration_results"]:
        dasha_str = f"{m['active_mahadasha']} - {m['active_antardasha']}"
        md_content += f"| **{m['event']}** | `{dasha_str}` ({m['dasha_span']}) | `{m['saturn_transit']}` | `[{m['shastra_citation']}]` | **{m['correlation_score']:.0f}%** |\n"

    md_content += f"""
---

## 4. Sacred Sanskrit Mantras & Remedial Protocols (Shanti Sastra)

### A. Active Dasha Shield (To Pacify Current Pressures)
* **Target Planetary Cycle:** `{remedies["active_dasha_shield"]["period"]}`
* **Deity:** **{remedies["active_dasha_shield"]["deity"]}**
* **Mantra:** `{remedies["active_dasha_shield"]["primary_mantra"]}`
* **Pronunciation (Transliteration):** *"{remedies["active_dasha_shield"]["transliteration"]}"*
* **Recitation Protocol:** {remedies["active_dasha_shield"]["protocol"]}

---

### B. Domain-Specific Success Anchors (*Karya Siddhi Mantras*)

#### 1. For Studies, Coding Mastery & University Exams
* **Deity:** {DOMAIN_MANTRAS["studies_and_exams"]["deity"]}
* **Mantra:** `{DOMAIN_MANTRAS["studies_and_exams"]["sanskrit"]}`
* **Pronunciation:** *"{DOMAIN_MANTRAS["studies_and_exams"]["transliteration"]}"*
* **When to Recite:** {DOMAIN_MANTRAS["studies_and_exams"]["protocol"]}

#### 2. For Career Breakthroughs & Unblocking Interviews
* **Deity:** {DOMAIN_MANTRAS["career_breakthrough"]["deity"]}
* **Mantra:** `{DOMAIN_MANTRAS["career_breakthrough"]["sanskrit"]}`
* **Pronunciation:** *"{DOMAIN_MANTRAS["career_breakthrough"]["transliteration"]}"*
* **When to Recite:** {DOMAIN_MANTRAS["career_breakthrough"]["protocol"]}

#### 3. For Emergency Protection & Overcoming Adversity
* **Deity:** {DOMAIN_MANTRAS["crisis_and_protection"]["deity"]}
* **Mantra:** `{DOMAIN_MANTRAS["crisis_and_protection"]["sanskrit"]}`
* **Pronunciation:** *"{DOMAIN_MANTRAS["crisis_and_protection"]["transliteration"]}"*
* **When to Recite:** {DOMAIN_MANTRAS["crisis_and_protection"]["protocol"]}

---

## 5. Methodological Note & Scholarly Defense
1. **Zero Fortune-Cookie Boilerplate:** Every interpretation cites its classical Sanskrit source (*BPHS*, *Phaladeepika*, *Saravali*).
2. **Algorithmic Sensitivity Evaluation:** Event correlation is evaluated against heuristic astronomical patterns (Double-Transit configurations). Controlled double-blind studies (e.g. Carlson, Nature, 1985) demonstrate celestial positions do not physically govern terrestrial events; metrics represent symbolic algorithmic alignment rather than physical causation.
3. **No Superstition:** Mantras are provided as vibrational focus anchors (*Chitta Shuddhi*), free from commercial gemstone marketing.

---
*Generated by Karmic Ledger System | Built for Sovereignty, Truth, & Self-Mastery*
"""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    return output_path
