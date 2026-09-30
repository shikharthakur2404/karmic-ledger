"""
karmic-ledger: Engine 10 - Medini Geopolitical & Mundane Chronometry Engine
Comprehensive multi-domain terrestrial telemetry for sovereign states:
1. Geopolitical Stress Index (GSI): Kinetic border friction, asymmetric threats, defense posture.
2. Ecological & Hydrological Disaster Index (EDI): Floods, tsunamis, seismic shocks, monsoon volatility.
3. Diplomatic Prestige Index (DPI): Global summits, multilateral alliances, international statecraft.
4. Macroeconomic Stability Index (MSI): Treasury liquidity, currency shocks, structural reform.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from core.dasha import compute_vimshottari_timeline, get_active_dasha_at_date
from core.ephemeris import compute_natal_chart
from core.transits import get_planet_transit_positions

# Canonical National Inception Database with Expanded Multi-Domain Milestones
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
            # 1. Territorial & Kinetic Conflicts
            {
                "event": "Sino-Indian Border War Inception",
                "date": "1962-10-20",
                "domain": "GEOPOLITICAL_DEFENSE",
                "category": "TERRITORIAL_CONFLICT",
            },
            {
                "event": "Indo-Pakistani War & Bangladesh Liberation",
                "date": "1971-12-03",
                "domain": "GEOPOLITICAL_DEFENSE",
                "category": "MILITARY_ENGAGEMENT",
            },
            {
                "event": "Proclamation of Internal Emergency",
                "date": "1975-06-25",
                "domain": "GOVERNANCE_CONSTITUTIONAL",
                "category": "CONSTITUTIONAL_CRISIS",
            },
            {
                "event": "Assassination of Prime Minister Indira Gandhi",
                "date": "1984-10-31",
                "domain": "GOVERNANCE_CONSTITUTIONAL",
                "category": "SOVEREIGN_HEAD_DISRUPTION",
            },
            {
                "event": "Pokhran-II Nuclear Tests (Operation Shakti)",
                "date": "1998-05-11",
                "domain": "STRATEGIC_PRESTIGE",
                "category": "STRATEGIC_DEFENSE_PROJECTION",
            },
            {
                "event": "Kargil Border Conflict Inception",
                "date": "1999-05-03",
                "domain": "GEOPOLITICAL_DEFENSE",
                "category": "BORDER_SECURITY_FRICTION",
            },
            {
                "event": "Mumbai 26/11 Coastal Terror Attacks",
                "date": "2008-11-26",
                "domain": "GEOPOLITICAL_DEFENSE",
                "category": "ASYMMETRIC_SECURITY_SHOCK",
            },
            {
                "event": "Historic General Election Mandate & Power Transition",
                "date": "2014-05-16",
                "domain": "GOVERNANCE_CONSTITUTIONAL",
                "category": "EXECUTIVE_POWER_PIVOT",
            },
            {
                "event": "Galwan Valley High-Altitude Border Clash",
                "date": "2020-06-15",
                "domain": "GEOPOLITICAL_DEFENSE",
                "category": "BORDER_SECURITY_FRICTION",
            },
            # 2. Ecological & Hydrological Cataclysms
            {
                "event": "Indian Ocean Mega-Tsunami & Coastal Deluge",
                "date": "2004-12-26",
                "domain": "ECOLOGICAL_DISASTER",
                "category": "HYDROLOGICAL_CATACLYSM",
            },
            {
                "event": "Kedarnath Himalayan Cloudburst & Flash Floods",
                "date": "2013-06-16",
                "domain": "ECOLOGICAL_DISASTER",
                "category": "HYDROLOGICAL_CATACLYSM",
            },
            {
                "event": "Kerala Super-Floods & Monsoon Inundation",
                "date": "2018-08-15",
                "domain": "ECOLOGICAL_DISASTER",
                "category": "HYDROLOGICAL_CATACLYSM",
            },
            {
                "event": "North India & Yamuna Delhi Flood Inundation",
                "date": "2023-07-09",
                "domain": "ECOLOGICAL_DISASTER",
                "category": "HYDROLOGICAL_CATACLYSM",
            },
            # 3. Diplomatic & Multilateral Summits
            {
                "event": "G20 New Delhi Leaders' Summit & Global Consensus",
                "date": "2023-09-09",
                "domain": "DIPLOMATIC_PRESTIGE",
                "category": "MULTILATERAL_SUMMIT_APEX",
            },
            # 4. Scientific & Technological Triumphs
            {
                "event": "Chandrayaan-3 Historic Lunar South Pole Landing",
                "date": "2023-08-23",
                "domain": "STRATEGIC_PRESTIGE",
                "category": "AEROSPACE_SCIENTIFIC_TRIUMPH",
            },
            # 5. Macroeconomic Shocks & Reforms
            {
                "event": "Economic Liberalization & Foreign Exchange Reform",
                "date": "1991-07-24",
                "domain": "MACROECONOMIC_POLICY",
                "category": "ECONOMIC_RECONSTRUCTION",
            },
            {
                "event": "Overnight Currency Demonetization Liquidity Freeze",
                "date": "2016-11-08",
                "domain": "MACROECONOMIC_POLICY",
                "category": "CURRENCY_LIQUIDITY_SHOCK",
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
                "domain": "GEOPOLITICAL_DEFENSE",
                "category": "DOMESTIC_TERRITORIAL_WAR",
            },
            {
                "event": "Wall Street Crash & Great Depression",
                "date": "1929-10-29",
                "domain": "MACROECONOMIC_POLICY",
                "category": "FINANCIAL_SYSTEM_COLLAPSE",
            },
            {
                "event": "September 11 Aerial Asymmetric Attacks",
                "date": "2001-09-11",
                "domain": "GEOPOLITICAL_DEFENSE",
                "category": "ASYMMETRIC_SECURITY_SHOCK",
            },
            {
                "event": "Great Financial Crisis (Lehman Bankruptcy)",
                "date": "2008-09-15",
                "domain": "MACROECONOMIC_POLICY",
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

# Element classification for mundane environmental & disaster physics
WATER_SIGNS = ["Cancer", "Scorpio", "Pisces"]  # Jala Tattva (Floods, Cyclones, Oceans)
EARTH_SIGNS = [
    "Taurus",
    "Virgo",
    "Capricorn",
]  # Prithvi Tattva (Land, Seismic faults)
FIRE_SIGNS = ["Aries", "Leo", "Sagittarius"]  # Agni Tattva (War, Explosions, Heat)
AIR_SIGNS = [
    "Gemini",
    "Libra",
    "Aquarius",
]  # Vayu Tattva (Storms, Aviation, Media)


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
    Computes a 4-dimensional mundane telemetry suite:
    1. Geopolitical Stress Index (GSI): Kinetic military friction, border tension, defense shocks.
    2. Ecological Disaster Index (EDI): Affliction to Jala Rasis (Water Signs) & 4th House (Land/Rainfall).
    3. Diplomatic Prestige Index (DPI): Multilateral leadership, treaty consensus, foreign alliances (H7/H10/H11).
    4. Macroeconomic Stability Index (MSI): Currency liquidity, treasury reserves, economic reform (H2/H11).
    """
    natal = nation_chart["natal"]
    timeline = nation_chart["timeline"]

    lagna_sign = natal["lagna"]["sign"]
    lagna_idx = ZODIAC.index(lagna_sign)

    def house_for_sign(s: str) -> int:
        return ((ZODIAC.index(s) - lagna_idx) % 12) + 1

    d_active = get_active_dasha_at_date(timeline, target_dt)
    transits = get_planet_transit_positions(target_dt)

    t_mars_s = transits["Mars"]["sign"]
    t_sat_s = transits["Saturn"]["sign"]
    t_rahu_s = transits["Rahu"]["sign"]
    t_ketu_s = transits["Ketu"]["sign"]
    t_jup_s = transits["Jupiter"]["sign"]
    t_ven_s = transits["Venus"]["sign"]
    t_sun_s = transits["Sun"]["sign"]

    t_mars_h = house_for_sign(t_mars_s)
    t_sat_h = house_for_sign(t_sat_s)
    t_rahu_h = house_for_sign(t_rahu_s)
    t_ketu_h = house_for_sign(t_ketu_s)
    t_jup_h = house_for_sign(t_jup_s)
    t_ven_h = house_for_sign(t_ven_s)
    t_sun_h = house_for_sign(t_sun_s)

    # Planetary aspects (Drishtis)
    mars_aspects = [
        t_mars_h,
        ((t_mars_h + 3) % 12) or 12,
        ((t_mars_h + 6) % 12) or 12,
        ((t_mars_h + 7) % 12) or 12,
    ]
    sat_aspects = [
        t_sat_h,
        ((t_sat_h + 2) % 12) or 12,
        ((t_sat_h + 6) % 12) or 12,
        ((t_sat_h + 9) % 12) or 12,
    ]
    jup_aspects = [
        t_jup_h,
        ((t_jup_h + 4) % 12) or 12,
        ((t_jup_h + 6) % 12) or 12,
        ((t_jup_h + 8) % 12) or 12,
    ]

    active_stress_vectors: list[dict[str, Any]] = []

    # =========================================================================
    # 1. GEOPOLITICAL STRESS INDEX (GSI, 0-100)
    # =========================================================================
    base_gsi = 32.0
    border_stress = 0.0

    if 3 in mars_aspects:
        border_stress += 22.0
        active_stress_vectors.append(
            {
                "vector": "TERRITORIAL_BORDER_TENSION",
                "source": f"Transit Mars in H{t_mars_h} ({t_mars_s}) casts drishti onto 3rd House (Borders/Neighbors)",
                "severity": "ELEVATED",
            }
        )
    if 3 in sat_aspects:
        border_stress += 18.0
        active_stress_vectors.append(
            {
                "vector": "INFRASTRUCTURE_BORDER_OBSTRUCTION",
                "source": f"Transit Saturn in H{t_sat_h} ({t_sat_s}) locks onto 3rd House of Territory",
                "severity": "MODERATE",
            }
        )
    if t_rahu_h in [3, 7, 8]:
        border_stress += 15.0
        active_stress_vectors.append(
            {
                "vector": "ASYMMETRIC_SECURITY_SENSITIVITY",
                "source": f"Transit Rahu in H{t_rahu_h} ({t_rahu_s}) activates irregular threat vectors",
                "severity": "ELEVATED",
            }
        )

    shock_stress = 0.0
    if 8 in mars_aspects and 8 in sat_aspects:
        shock_stress += 25.0
        active_stress_vectors.append(
            {
                "vector": "ACUTE_SHOCK_CONVERGENCE",
                "source": "Dual-Malefic Mars & Saturn cross-lock onto 8th House of National Security Shocks",
                "severity": "HIGH",
            }
        )

    gsi_mitigation = 0.0
    if t_jup_h in [1, 5, 9]:
        gsi_mitigation += 16.0
    if t_jup_h in [3, 11]:
        gsi_mitigation += 12.0

    raw_gsi = base_gsi + border_stress + shock_stress - gsi_mitigation
    gsi_score = round(max(min(raw_gsi, 96.0), 18.0), 1)

    # =========================================================================
    # 2. ECOLOGICAL & HYDROLOGICAL DISASTER INDEX (EDI, 0-100)
    # Severe affliction to Water Signs (Cancer H3, Scorpio H7, Pisces H11) & H4 (Land)
    # =========================================================================
    base_edi = 25.0
    hydro_stress = 0.0

    # Check malefic transits in Water Signs (Jala Rasis: Cancer, Scorpio, Pisces)
    for p_name, p_sign in [
        ("Saturn", t_sat_s),
        ("Mars", t_mars_s),
        ("Rahu", t_rahu_s),
        ("Ketu", t_ketu_s),
    ]:
        if p_sign in WATER_SIGNS:
            hydro_stress += 16.0
            active_stress_vectors.append(
                {
                    "vector": "HYDROLOGICAL_VULNERABILITY",
                    "source": f"Malefic {p_name} occupies Water Sign {p_sign} (Oceanic/Monsoon Turbulence)",
                    "severity": "ELEVATED",
                }
            )

    # Affliction to 4th House (Land / Domestic Territory / Agriculture)
    if 4 in mars_aspects or 4 in sat_aspects:
        hydro_stress += 14.0
        active_stress_vectors.append(
            {
                "vector": "TERRITORIAL_LAND_SATURATION",
                "source": "Malefic aspect locks onto 4th House (Land/Shelter)",
                "severity": "MODERATE",
            }
        )

    # Water-sign Moon afflictions (India has Moon in Cancer)
    if t_sat_s == "Cancer" or t_mars_s == "Cancer":
        hydro_stress += 20.0
        active_stress_vectors.append(
            {
                "vector": "NATAL_WATER_STELLIUM_COMPRESSION",
                "source": "Transit Saturn/Mars directly compresses Natal Moon in Cancer (Extreme Deluge / Tsunami)",
                "severity": "HIGH",
            }
        )

    edi_mitigation = 12.0 if t_jup_s in WATER_SIGNS and t_sat_s != t_jup_s else 0.0
    raw_edi = base_edi + hydro_stress - edi_mitigation
    edi_score = round(max(min(raw_edi, 95.0), 15.0), 1)

    # =========================================================================
    # 3. DIPLOMATIC PRESTIGE & MULTILATERAL CONSENSUS INDEX (DPI, 0-100)
    # Benefic activation of 7th (Foreign Alliances), 10th (Leadership), 11th (Global Coalitions)
    # =========================================================================
    base_dpi = 35.0
    prestige_lift = 0.0

    # Jupiter supporting 7th, 10th, or 11th
    if 7 in jup_aspects or t_jup_h == 7:
        prestige_lift += 24.0
        active_stress_vectors.append(
            {
                "vector": "MULTILATERAL_DIPLOMATIC_ELEVATION",
                "source": f"Jupiter in H{t_jup_h} casts benefic drishti onto 7th House of Foreign Alliances",
                "severity": "POSITIVE_ALIGNMENT",
            }
        )
    if 10 in jup_aspects or t_jup_h == 10:
        prestige_lift += 18.0
    if 11 in jup_aspects or t_jup_h == 11:
        prestige_lift += 16.0

    # Venus and Mercury (Diplomatic architects) in favorable houses
    if t_ven_h in [1, 3, 5, 9, 11]:
        prestige_lift += 10.0
    if t_sun_h in [3, 10, 11]:  # Sovereign presence
        prestige_lift += 12.0

    # Dasha synergy: Mercury or Moon or Venus sub-periods
    ad_lord = d_active.get("antardasha", "")
    if ad_lord in ["Mercury", "Jupiter", "Venus"]:
        prestige_lift += 10.0

    raw_dpi = base_dpi + prestige_lift
    dpi_score = round(max(min(raw_dpi, 98.0), 20.0), 1)

    # =========================================================================
    # 4. MACROECONOMIC STABILITY INDEX (MSI, 0-100)
    # 2nd House (Treasury/Currency) & 11th House (Revenue/Gains)
    # =========================================================================
    base_msi = 50.0
    econ_variance = 0.0

    if 2 in sat_aspects or 2 in mars_aspects:
        econ_variance -= 18.0
        active_stress_vectors.append(
            {
                "vector": "TREASURY_LIQUIDITY_COMPRESSION",
                "source": "Malefic aspect locks onto 2nd House (Treasury / Currency Notes)",
                "severity": "ELEVATED",
            }
        )
    if t_ketu_h == 2 or t_rahu_h == 2:
        econ_variance -= 22.0
        active_stress_vectors.append(
            {
                "vector": "CURRENCY_DEMONETIZATION_DISRUPTION",
                "source": "Nodal axis across 2nd House of Currency (Sudden Financial Paradigm Pivot)",
                "severity": "HIGH",
            }
        )
    if t_jup_h in [2, 11] or 11 in jup_aspects:
        econ_variance += 25.0
        active_stress_vectors.append(
            {
                "vector": "SOVEREIGN_REVENUE_EXPANSION",
                "source": "Jupiter supports 2nd/11th wealth houses (Economic Growth / Foreign Reserves)",
                "severity": "POSITIVE_ALIGNMENT",
            }
        )

    raw_msi = base_msi + econ_variance
    msi_score = round(max(min(raw_msi, 95.0), 15.0), 1)

    # Determine dominant threat/opportunity classification
    if gsi_score >= 75.0:
        overall_status = "CRITICAL_SECURITY_HORIZON"
    elif edi_score >= 70.0:
        overall_status = "ECOLOGICAL_DISASTER_ALERT"
    elif dpi_score >= 75.0:
        overall_status = "DIPLOMATIC_PRESTIGE_APEX"
    elif msi_score <= 35.0:
        overall_status = "MACROECONOMIC_LIQUIDITY_STRAIN"
    else:
        overall_status = "BALANCED_SOVEREIGN_EQUILIBRIUM"

    return {
        "target_date": target_dt.strftime("%Y-%m-%d"),
        "overall_status": overall_status,
        "geopolitical_stress_index": gsi_score,
        "ecological_disaster_index": edi_score,
        "diplomatic_prestige_index": dpi_score,
        "macroeconomic_stability_index": msi_score,
        "active_dasha": f"{d_active.get('mahadasha')} - {d_active.get('antardasha')}",
        "planetary_sectors": {
            "mars_sign": t_mars_s,
            "saturn_sign": t_sat_s,
            "rahu_sign": t_rahu_s,
            "jupiter_sign": t_jup_s,
            "mars_transit_house": t_mars_h,
            "saturn_transit_house": t_sat_h,
            "rahu_transit_house": t_rahu_h,
            "jupiter_transit_house": t_jup_h,
        },
        "active_vectors": active_stress_vectors,
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
                "domain": m["domain"],
                "category": m["category"],
                "overall_status": telemetry["overall_status"],
                "gsi_score": telemetry["geopolitical_stress_index"],
                "edi_score": telemetry["ecological_disaster_index"],
                "dpi_score": telemetry["diplomatic_prestige_index"],
                "msi_score": telemetry["macroeconomic_stability_index"],
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
                    "overall_status": t["overall_status"],
                    "gsi_score": t["geopolitical_stress_index"],
                    "edi_score": t["ecological_disaster_index"],
                    "dpi_score": t["diplomatic_prestige_index"],
                    "msi_score": t["macroeconomic_stability_index"],
                    "dasha": t["active_dasha"],
                    "transits": t["planetary_sectors"],
                    "vectors": [v["vector"] for v in t["active_vectors"]],
                }
            )

    return projections
