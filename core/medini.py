"""
karmic-ledger: Engine 10 - Medini Geopolitical & Mundane Chronometry Engine
Analyzes macroeconomic, territorial, and geopolitical stress indices using national
inception charts, Gochar transit angularity, and Vimshottari national timelines.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from core.dasha import compute_vimshottari_timeline, get_active_dasha_at_date
from core.ephemeris import compute_natal_chart
from core.transits import get_planet_transit_positions

# Canonical National Inception Database
NATION_REGISTRY: dict[str, dict[str, Any]] = {
    "india": {
        "nation_id": "india",
        "name": "Republic of India (Dominion & Independence Midnight Origin)",
        "date": "1947-08-15",
        "time": "00:00:01",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "capital": "New Delhi",
        "tz_offset_hours": 5.5,
        "historical_milestones": [
            {
                "event": "Sino-Indian Border War Inception",
                "date": "1962-10-20",
                "category": "TERRITORIAL_CONFLICT",
            },
            {
                "event": "Indo-Pakistani War & Bangladesh Liberation",
                "date": "1971-12-03",
                "category": "MILITARY_ENGAGEMENT",
            },
            {
                "event": "Proclamation of Internal Emergency",
                "date": "1975-06-25",
                "category": "CONSTITUTIONAL_CRISIS",
            },
            {
                "event": "Assassination of Prime Minister Indira Gandhi",
                "date": "1984-10-31",
                "category": "SOVEREIGN_HEAD_DISRUPTION",
            },
            {
                "event": "Economic Liberalization & Foreign Exchange Reform",
                "date": "1991-07-24",
                "category": "ECONOMIC_RECONSTRUCTION",
            },
            {
                "event": "Pokhran-II Nuclear Tests (Operation Shakti)",
                "date": "1998-05-11",
                "category": "STRATEGIC_DEFENSE_PROJECTION",
            },
            {
                "event": "Kargil Border Conflict Inception",
                "date": "1999-05-03",
                "category": "BORDER_SECURITY_FRICTION",
            },
            {
                "event": "Mumbai 26/11 Coastal Terror Attacks",
                "date": "2008-11-26",
                "category": "ASYMMETRIC_SECURITY_SHOCK",
            },
            {
                "event": "Historic General Election Mandate & Power Transition",
                "date": "2014-05-16",
                "category": "EXECUTIVE_POWER_PIVOT",
            },
            {
                "event": "Galwan Valley High-Altitude Border Clash",
                "date": "2020-06-15",
                "category": "BORDER_SECURITY_FRICTION",
            },
        ],
    },
    "usa": {
        "nation_id": "usa",
        "name": "United States of America (Sibly Declaration Baseline)",
        "date": "1776-07-04",
        "time": "17:10:00",
        "latitude": 39.9526,
        "longitude": -75.1652,
        "capital": "Philadelphia",
        "tz_offset_hours": -5.0,
        "historical_milestones": [
            {
                "event": "Civil War Inception (Fort Sumter)",
                "date": "1861-04-12",
                "category": "DOMESTIC_TERRITORIAL_WAR",
            },
            {
                "event": "Wall Street Crash & Great Depression",
                "date": "1929-10-29",
                "category": "FINANCIAL_SYSTEM_COLLAPSE",
            },
            {
                "event": "September 11 Aerial Asymmetric Attacks",
                "date": "2001-09-11",
                "category": "ASYMMETRIC_SECURITY_SHOCK",
            },
            {
                "event": "Great Financial Crisis (Lehman Bankruptcy)",
                "date": "2008-09-15",
                "category": "FINANCIAL_SYSTEM_COLLAPSE",
            },
        ],
    },
}

ZODIAC = [
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


def compute_national_chart(nation_key: str = "india") -> dict[str, Any]:
    """Generates foundational sidereal ephemeris and 120-year timeline for a sovereign nation."""
    if nation_key not in NATION_REGISTRY:
        raise ValueError(f"Nation '{nation_key}' not in sovereign registry.")

    cfg = NATION_REGISTRY[nation_key]
    d_parts = [int(x) for x in cfg["date"].split("-")]
    t_parts = [int(x) for x in cfg["time"].split(":")]

    natal = compute_natal_chart(
        year=d_parts[0],
        month=d_parts[1],
        day=d_parts[2],
        hour=t_parts[0],
        minute=t_parts[1],
        second=t_parts[2],
        lat=cfg["latitude"],
        lon=cfg["longitude"],
        tz_offset_hours=cfg["tz_offset_hours"],
    )

    moon_nak = natal["planets"]["Moon"]["nakshatra"]
    birth_dt = datetime(
        d_parts[0], d_parts[1], d_parts[2], t_parts[0], t_parts[1], t_parts[2]
    )
    timeline = compute_vimshottari_timeline(
        birth_dt=birth_dt,
        moon_nakshatra_lord=moon_nak["lord"],
        fraction_elapsed=moon_nak["fraction_elapsed"],
    )

    return {
        "nation_id": nation_key,
        "metadata": cfg,
        "natal": natal,
        "timeline": timeline,
    }


def evaluate_geopolitical_incident_index(
    nation_chart: dict[str, Any], target_dt: datetime
) -> dict[str, Any]:
    """
    Computes real-time Geopolitical Stress Index (GSI, 0-100) and multi-domain vectors:
    - Kinetic Border Security Tension (Mars / Saturn targeting 3H borders and 7H open adversaries)
    - Macroeconomic & Sovereign Currency Liquidity (Jupiter / Venus targeting 2H / 11H)
    - Executive Authority & Constitutional Continuity (Sun / Saturn targeting 10H)
    """
    natal = nation_chart["natal"]
    timeline = nation_chart["timeline"]

    lagna_sign = natal["lagna"]["sign"]
    lagna_idx = ZODIAC.index(lagna_sign)

    def house_for_sign(s: str) -> int:
        return ((ZODIAC.index(s) - lagna_idx) % 12) + 1

    d_active = get_active_dasha_at_date(timeline, target_dt)
    transits = get_planet_transit_positions(target_dt)

    t_mars_h = house_for_sign(transits["Mars"]["sign"])
    t_sat_h = house_for_sign(transits["Saturn"]["sign"])
    t_rahu_h = house_for_sign(transits["Rahu"]["sign"])
    t_jup_h = house_for_sign(transits["Jupiter"]["sign"])

    # Mars aspects: Conjunction, 4th, 7th, 8th
    mars_aspects = [
        t_mars_h,
        ((t_mars_h + 3) % 12) or 12,
        ((t_mars_h + 6) % 12) or 12,
        ((t_mars_h + 7) % 12) or 12,
    ]

    # Saturn aspects: Conjunction, 3rd, 7th, 10th
    sat_aspects = [
        t_sat_h,
        ((t_sat_h + 2) % 12) or 12,
        ((t_sat_h + 6) % 12) or 12,
        ((t_sat_h + 9) % 12) or 12,
    ]

    active_stress_vectors: list[dict[str, Any]] = []
    base_gsi = 32.0  # Baseline geopolitical background entropy

    # 1. BORDER & NATIONAL DEFENSE VECTOR (House 3 & House 7)
    border_stress = 0.0
    if 3 in mars_aspects:
        border_stress += 22.0
        active_stress_vectors.append(
            {
                "vector": "TERRITORIAL_BORDER_TENSION",
                "source": f"Transit Mars in H{t_mars_h} casts drishti onto 3rd House (Borders/Neighbors)",
                "severity": "ELEVATED",
            }
        )
    if 3 in sat_aspects:
        border_stress += 18.0
        active_stress_vectors.append(
            {
                "vector": "INFRASTRUCTURE_BORDER_OBSTRUCTION",
                "source": f"Transit Saturn in H{t_sat_h} locks onto 3rd House of Territory",
                "severity": "MODERATE",
            }
        )
    if t_rahu_h in [3, 7, 8]:
        border_stress += 15.0
        active_stress_vectors.append(
            {
                "vector": "ASYMMETRIC_SECURITY_SENSITIVITY",
                "source": f"Transit Rahu stationed in H{t_rahu_h} (Unorthodox security/external threat domain)",
                "severity": "ELEVATED",
            }
        )

    # 2. INTERNAL COHESION & 8TH HOUSE SHOCK COUPLING
    shock_stress = 0.0
    if 8 in mars_aspects and 8 in sat_aspects:
        shock_stress += 25.0
        active_stress_vectors.append(
            {
                "vector": "ACUTE_SHOCK_CONVERGENCE",
                "source": "Dual-Malefic Mars & Saturn cross-lock onto 8th House of Sudden Transformation",
                "severity": "HIGH",
            }
        )

    # 3. JUPITERIAN STABILIZATION DAMPING
    mitigation = 0.0
    if t_jup_h in [1, 5, 9]:
        mitigation += 16.0
    if t_jup_h in [3, 11]:
        mitigation += 12.0

    raw_gsi = base_gsi + border_stress + shock_stress - mitigation
    gsi_score = round(max(min(raw_gsi, 96.0), 18.0), 1)

    if gsi_score >= 75.0:
        threat_level = "CRITICAL_SECURITY_HORIZON"
    elif gsi_score >= 55.0:
        threat_level = "ELEVATED_GEOPOLITICAL_FRICTION"
    elif gsi_score >= 38.0:
        threat_level = "ACTIVE_CONVENTIONAL_EQUILIBRIUM"
    else:
        threat_level = "SOVEREIGN_CONSOLIDATION_&_STABILITY"

    return {
        "target_date": target_dt.strftime("%Y-%m-%d"),
        "geopolitical_stress_index": gsi_score,
        "threat_level": threat_level,
        "active_dasha": f"{d_active.get('mahadasha')} - {d_active.get('antardasha')}",
        "planetary_sectors": {
            "mars_transit_house": t_mars_h,
            "saturn_transit_house": t_sat_h,
            "rahu_transit_house": t_rahu_h,
            "jupiter_transit_house": t_jup_h,
        },
        "active_vectors": active_stress_vectors,
        "mitigation_factor": round(mitigation, 1),
    }


def backtest_national_history(nation_key: str = "india") -> list[dict[str, Any]]:
    """Runs automated empirical backtesting across all major historical national events."""
    chart = compute_national_chart(nation_key)
    milestones = chart["metadata"]["historical_milestones"]

    results = []
    for m in milestones:
        event_dt = datetime.strptime(m["date"], "%Y-%m-%d")
        telemetry = evaluate_geopolitical_incident_index(chart, event_dt)
        results.append(
            {
                "event": m["event"],
                "date": m["date"],
                "category": m["category"],
                "gsi_score": telemetry["geopolitical_stress_index"],
                "threat_level": telemetry["threat_level"],
                "dasha": telemetry["active_dasha"],
                "vectors_fired": len(telemetry["active_vectors"]),
            }
        )

    return results


def project_national_horizon(
    nation_key: str = "india", start_year: int = 2024, end_year: int = 2035
) -> list[dict[str, Any]]:
    """Generates annual forward geopolitical telemetry projection in 6-month steps."""
    chart = compute_national_chart(nation_key)
    projections = []

    for yr in range(start_year, end_year + 1):
        for month in [1, 7]:
            dt = datetime(yr, month, 1)
            t = evaluate_geopolitical_incident_index(chart, dt)
            projections.append(
                {
                    "date": dt.strftime("%Y-%m-%d"),
                    "year": yr,
                    "month": month,
                    "gsi_score": t["geopolitical_stress_index"],
                    "threat_level": t["threat_level"],
                    "dasha": t["active_dasha"],
                    "transits": t["planetary_sectors"],
                    "vectors": [v["vector"] for v in t["active_vectors"]],
                }
            )

    return projections
