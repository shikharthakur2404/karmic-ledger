from __future__ import annotations

import asyncio
import os
from datetime import datetime
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, field_validator

from core.ayurdaya import compute_ayurdaya_telemetry
from core.confluence import evaluate_event_confluence
from core.consent import is_historical_benchmark_subject
from core.daily import compute_daily_incident_radar
from core.dasha import compute_vimshottari_timeline, get_active_dasha_at_date
from core.ephemeris import compute_natal_chart
from core.frictions import audit_live_frictions
from core.geocoding import geocode_location
from core.mantras import DOMAIN_MANTRAS, recommend_remedies_for_chart
from core.primer import explain_planet_placement
from core.registry import get_system_manifest
from core.shastra import search_shastra
from core.soul import evaluate_soul_telemetry
from core.transits import get_planet_transit_positions
from core.verifier import parse_event_date
from core.visuals import generate_dasha_progress_bar_svg, generate_diamond_kundli_svg

app = FastAPI(
    title="Karmic Ledger API",
    description="Analytical Jyotish Telemetry & Algorithmic Sensitivity Engine",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

DEMO_PROFILES = {
    "indira": {
        "name": "Indira Gandhi (Historical Benchmark)",
        "date": "1917-11-19",
        "time": "23:11:00",
        "latitude": 25.4358,
        "longitude": 81.8463,
        "city": "Allahabad",
        "country": "India",
        "is_deceased": True,
        "death_date": "1984-10-31",
        "milestones": [
            {"event": "Marriage to Feroze Gandhi", "date": "1942-03-26"},
            {"event": "Sworn in as Prime Minister of India", "date": "1966-01-24"},
            {"event": "Proclamation of National Emergency", "date": "1975-06-25"},
            {"event": "Electoral Defeat & Loss of Office", "date": "1977-03-22"},
            {"event": "Historic Re-election & Return to Power", "date": "1980-01-14"},
            {"event": "Assassination / Violent Physical Exit", "date": "1984-10-31"},
        ],
    },
    "anonymous": {
        "name": "Synthetic Archetype 01 (De-Identified Calibration)",
        "date": "2000-01-01",
        "time": "12:00:00",
        "latitude": 52.5200,
        "longitude": 13.4050,
        "city": "Berlin",
        "country": "Germany",
        "milestones": [
            {"event": "Higher Education Milestone", "date": "2022-09-01"},
            {"event": "Major Career Pivot & Elevation", "date": "2025-03-15"},
        ],
    },
    "soham": {
        "name": "Soham Deokar (WG Fun Kundli)",
        "date": "2000-11-10",
        "time": "09:10:00",
        "latitude": 17.6370,
        "longitude": 74.4018,
        "city": "Khatav, Satara",
        "country": "India",
        "consent": True,
        "milestones": [
            {"event": "First Romantic Relationship", "date": "2016-07-01"},
            {"event": "High School Completion & B.Tech Entrance", "date": "2018-07-15"},
            {"event": "College Breakup (First Year)", "date": "2018-09-01"},
            {"event": "Current Partner Commitment", "date": "2020-08-12"},
            {
                "event": "B.Tech Grad & Senior Software Engineer Role",
                "date": "2022-06-15",
            },
            {"event": "Departure from Corporate Job in India", "date": "2024-07-15"},
            {
                "event": "International Relocation to Germany (Master's)",
                "date": "2024-10-01",
            },
        ],
    },
    "shikhar": {
        "name": "Shikhar Thakur (System Architect)",
        "date": "1999-04-24",
        "time": "07:00:00",
        "latitude": 26.4652,
        "longitude": 80.3498,
        "city": "Kanpur",
        "country": "India",
        "consent": True,
        "milestones": [
            {
                "event": "FytlY 99k LOC Architecture & Systems Launch",
                "date": "2024-06-15",
            },
            {
                "event": "Foreign Relocation to Germany / DACH",
                "date": "2024-10-03",
            },
            {
                "event": "Karmic Ledger 2.0 Autonomous Engine Deployment",
                "date": "2026-09-26",
            },
        ],
    },
}


class MilestoneInput(BaseModel):
    event: str
    date: str

    @field_validator("date")
    @classmethod
    def valid_date(cls, v):
        try:
            parse_event_date(v)
        except Exception:
            raise ValueError("Date must be parsable (YYYY-MM-DD, YYYY-MM, or YYYY)")
        return v


class ChartRequest(BaseModel):
    name: str = "Subject"
    date: str = "2000-01-01"
    time: str = "07:00:00"
    latitude: float = 28.6139
    longitude: float = 77.2090
    city: str = "New Delhi"
    country: str = "India"
    consent: bool = False
    is_deceased: bool = False
    death_date: Optional[str] = None
    milestones: list[MilestoneInput] = []

    @field_validator("latitude")
    @classmethod
    def valid_lat(cls, v):
        if not (-90.0 <= v <= 90.0):
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    @classmethod
    def valid_lon(cls, v):
        if not (-180.0 <= v <= 180.0):
            raise ValueError("Longitude must be between -180 and 180")
        return v

    @field_validator("date")
    @classmethod
    def valid_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                "Date must be in YYYY-MM-DD format and be a valid calendar date"
            )
        return v

    @field_validator("time")
    @classmethod
    def valid_time(cls, v):
        if not v.strip():
            return ""
        try:
            datetime.strptime(v, "%H:%M:%S")
        except ValueError:
            try:
                datetime.strptime(v, "%H:%M")
                return v + ":00"
            except ValueError:
                raise ValueError("Time must be in HH:MM:SS or HH:MM format")
        return v


def run_chart_pipeline(data: ChartRequest) -> dict[str, Any]:
    """
    ==============================================================================
    MAIN TELEMETRY PIPELINE (run_chart_pipeline)
    ==============================================================================
    The central coordinator of the Karmic Ledger engine.
    Ingests raw birth data (date, time, lat/lon) and coordinates 11 sequential engines:
      Step 0: Epistemic Consent & Privacy Validation
      Step 1: Swiss Ephemeris C-library Astronomical Calculations (Nirayana Longitudes)
      Step 2: 120-Year Vimshottari Dasha Mathematical Timeline
      Step 3: Temporal Horizon & Demise/Historical Handling
      Step 4: Ayurdaya Classical Longevity Horizon (Fun Kundli Engine)
      Step 5: Event Backtesting & Vedic Correlation Score (VCS %)
      Step 6: Shastric Remedial Mantras & Astrological Balance
      Step 7: Real-Time Vector Visualizations (Diamond Kundli & Dasha Bar SVGs)
      Step 8: Planetary Positions, Cusps, and Dignities Matrix
      Step 9: Soul Age & Archetype Telemetry (Ātmakāraka Odometer)
      Step 10: Live Multi-Year Karmic Frictions Diagnostic
      Step 11: 24-Hour Real-Time Somatic & Daily Incident Radar
    ==============================================================================
    """
    raw_dict = data.dict() if hasattr(data, "dict") else data.model_dump()
    is_historical = is_historical_benchmark_subject(raw_dict, data.name)

    # --------------------------------------------------------------------------
    # STEP 0: MANDATORY PRIVACY & ETHICAL CONSENT GATE
    # Ensures no private living individual is analyzed without affirmative consent.
    # --------------------------------------------------------------------------
    if not data.consent and not is_historical:
        raise HTTPException(
            status_code=403,
            detail="Affirmative epistemic consent required. Processing halted under zero-diagnostic research boundary.",
        )

    # Normalize birth time (defaulting to 12:00 PM if querent does not know exact minute)
    birth_time_unknown = not data.time.strip()
    actual_time = "12:00:00" if birth_time_unknown else data.time

    date_parts = [int(p) for p in data.date.split("-")]
    t_parts = actual_time.split(":")
    hour = int(t_parts[0])
    minute = int(t_parts[1]) if len(t_parts) > 1 else 0
    second = int(t_parts[2]) if len(t_parts) > 2 else 0

    # --------------------------------------------------------------------------
    # STEP 1: COMPUTE EXACT CELESTIAL COORDINATES (SWISS EPHEMERIS)
    # Uses high-precision C library (pyswisseph) with Lahiri Ayanamsha to determine
    # exact positions of Lagna, Moon Nakshatra, Bhavas (Houses), and all 9 Grahas.
    # --------------------------------------------------------------------------
    try:
        natal = compute_natal_chart(
            year=date_parts[0],
            month=date_parts[1],
            day=date_parts[2],
            hour=hour,
            minute=minute,
            second=second,
            lat=data.latitude,
            lon=data.longitude,
            tz_offset_hours=5.5,
        )
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Ephemeris calculation failed (possibly invalid coordinates or polar latitude): {e!s}",
        )

    birth_dt = datetime(
        date_parts[0], date_parts[1], date_parts[2], hour, minute, second
    )
    moon_nak = natal["planets"]["Moon"]["nakshatra"]

    # --------------------------------------------------------------------------
    # STEP 2: GENERATE 120-YEAR VIMSHOTTARI DASHA TIMELINE
    # Computes exact chronological life chapters (Mahadashas & Antardashas)
    # based on the exact degree elapsed in the natal Moon Nakshatra at birth.
    # --------------------------------------------------------------------------
    timeline = compute_vimshottari_timeline(
        birth_dt=birth_dt,
        moon_nakshatra_lord=moon_nak["lord"],
        fraction_elapsed=moon_nak["fraction_elapsed"],
    )

    # --------------------------------------------------------------------------
    # STEP 3: TEMPORAL HORIZON & ACTIVE DASHA RESOLUTION
    # Identifies which planetary period is currently active right now (or at death
    # for historical benchmark subjects like Indira Gandhi).
    # --------------------------------------------------------------------------
    is_deceased = data.is_deceased or (
        is_historical
        and ("indira" in data.name.lower() or "benchmark" in data.name.lower())
    )
    death_date_str = data.death_date or (
        "1984-10-31" if is_deceased and "indira" in data.name.lower() else None
    )

    if is_deceased and death_date_str:
        exit_dt = datetime.strptime(death_date_str, "%Y-%m-%d")
        age_years = round((exit_dt - birth_dt).days / 365.25, 1)
        effective_dt = exit_dt
        age_display = f"{age_years} Years (1917–1984)"
        age_label = "Lifespan (Historical Record)"
        dasha_label = "Terminal Life Chapter (At Demise, 1984)"
    else:
        current_dt = datetime.now()
        age_years = round((current_dt - birth_dt).days / 365.25, 1)
        effective_dt = current_dt
        age_display = f"{age_years} Years"
        age_label = "Current Age"
        dasha_label = "Current Life Chapter (Active Period)"

    current_dasha = get_active_dasha_at_date(timeline, effective_dt)

    # 4. Layman Explanations
    primer_cards = []
    for p_name, p_val in natal["planets"].items():
        if birth_time_unknown:
            exp = f"{p_name} is stationed in {p_val['sign']} (House placement suppressed due to unknown birth time)."
            primer_cards.append(
                {
                    "planet": p_name,
                    "house": "Unknown",
                    "formatted": p_val["formatted"],
                    "explanation": exp,
                    "dignity": p_val["dignity"],
                }
            )
        else:
            exp = explain_planet_placement(p_name, p_val["house"], p_val["sign"])
            primer_cards.append(
                {
                    "planet": p_name,
                    "house": p_val["house"],
                    "formatted": p_val["formatted"],
                    "explanation": exp,
                    "dignity": p_val["dignity"],
                }
            )

    # 5. Backtest Milestones & VCS Score
    verified_milestones = []
    total_score = 0.0
    is_historical = is_historical_benchmark_subject(data.dict(), data.name)

    for m in data.milestones:
        event_dt = parse_event_date(m.date)
        d_active = get_active_dasha_at_date(timeline, event_dt)
        t_active = get_planet_transit_positions(event_dt)

        # Evaluate mathematical confluence & shastra citation
        confluence_res = evaluate_event_confluence(
            natal=natal,
            dasha_active=d_active,
            transits_active=t_active,
            event_name=m.event,
            is_historical_benchmark=is_historical,
        )
        score = confluence_res.get("confluence_score", 75.0)
        total_score += score
        cit = confluence_res.get("shastra_citation", "BPHS 24:14")

        # Shastra text retrieval
        refs = []
        name_lower = m.event.lower()
        if "marriage" in name_lower or "wedding" in name_lower:
            refs = search_shastra("marriage")
        elif (
            "mother" in name_lower
            or "maternal" in name_lower
            or "bereavement" in name_lower
            or "assassination" in name_lower
        ):
            refs = search_shastra("pushya")
        elif (
            "fired" in name_lower
            or "defeat" in name_lower
            or "loss" in name_lower
            or "emergency" in name_lower
        ):
            refs = search_shastra("chhidra")
        elif (
            "foreign" in name_lower
            or "relocation" in name_lower
            or "abroad" in name_lower
        ):
            refs = search_shastra("foreign")
        elif (
            "prime minister" in name_lower
            or "sworn" in name_lower
            or "power" in name_lower
        ):
            refs = search_shastra("career")

        sanskrit = (
            refs[0]["sanskrit"]
            if refs
            else "स्वक्षेमगे भूमिसुते न दोषो भवेत् कदाचित् किल मानवानाम्।"
        )
        translation = (
            refs[0]["translation"]
            if refs
            else "Classical Parashari astronomical telemetry baseline."
        )

        verified_milestones.append(
            {
                "event": m.event,
                "date": m.date,
                "mahadasha": d_active.get("mahadasha", "N/A"),
                "antardasha": d_active.get("antardasha", "N/A"),
                "span": f"{d_active.get('period_start', '')} to {d_active.get('period_end', '')}",
                "saturn_transit": t_active["Saturn"]["formatted"],
                "jupiter_transit": t_active["Jupiter"]["formatted"],
                "citation": cit,
                "sanskrit": sanskrit,
                "translation": translation,
                "vcs": score,
            }
        )

    if not is_historical:
        for vm in verified_milestones:
            t_lower = vm["translation"].lower()
            if any(
                w in t_lower
                for w in [
                    "death",
                    "assassination",
                    "dispute",
                    "disorientation",
                    "infidelity",
                    "divorce",
                    "loss of post",
                    "disease",
                    "illness",
                    "pathology",
                    "surgery",
                ]
            ):
                vm["translation"] = (
                    "Classical astronomical baseline: symbolic developmental transition period."
                )
                vm["citation"] = (
                    "Ayur-Jyotish & Parampara: Symbolic Pacing Theme (Zero Clinical/Fatalistic Claim)"
                )

    milestone_count = len(data.milestones)
    if milestone_count >= 5:
        avg_vcs = round(total_score / milestone_count, 1)
        vcs_badge_text = f"Benchmark Match: {avg_vcs}% (N={milestone_count})"
        vcs_score_val = f"{avg_vcs}%"
        vcs_status = "CALIBRATED_BENCHMARK"
    elif milestone_count > 0:
        vcs_badge_text = (
            f"Astronomical Baseline (N={milestone_count} Below Statistical Floor N≥5)"
        )
        vcs_score_val = None
        vcs_status = "INSUFFICIENT_MILESTONE_FLOOR"
    else:
        vcs_badge_text = "Astronomical Ephemeris // Exact Coordinates"
        vcs_score_val = None
        vcs_status = "ZERO_MILESTONE_EPHEMERIS"

    # 6. Sastra Mantras & Remedies
    remedies = recommend_remedies_for_chart(
        active_mahadasha=current_dasha.get("mahadasha", "Mercury"),
        active_antardasha=current_dasha.get("antardasha", "Jupiter"),
    )

    # 7. Visuals (SVG Kundli & Progress Bar)
    planets_by_house: dict[int, list[str]] = {i: [] for i in range(1, 13)}
    for p_name, p_val in natal["planets"].items():
        planets_by_house[p_val["house"]].append(p_name[:2])

    zodiac_indices = [
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
    lagna_idx = zodiac_indices.index(natal["lagna"]["sign"])
    kundli_svg = generate_diamond_kundli_svg(lagna_idx, planets_by_house)
    dasha_bar_svg = generate_dasha_progress_bar_svg(
        timeline,
        age_years,
        is_deceased=is_deceased,
        reticle_label=f"{age_years}Y (1984)" if is_deceased else "",
    )

    # 8. Planets Table for Sector 05
    planets_table = []
    for p_name, p_data in natal["planets"].items():
        planets_table.append(
            {
                "planet": p_name,
                "sign": p_data["sign"],
                "degree": f"{p_data['degree_in_sign']:.2f}°",
                "house": p_data["house"],
                "dignity": p_data.get("dignity", "Neutral"),
            }
        )

    # 9. Soul Age & Archetype Telemetry
    soul_telemetry = evaluate_soul_telemetry(natal)

    # 10. Live Karmic Friction & Crisis Diagnostic
    frictions = audit_live_frictions(natal, timeline, effective_dt)

    if is_deceased:
        frictions["status"] = "HISTORICAL_ARCHIVE_LOCKED"
        frictions["tension_count"] = 0
        frictions["crisis_count"] = 0
        frictions["active_crises"] = []
        frictions["active_strain_indices"] = []
        frictions["threat_vectors"] = []
    elif birth_time_unknown:
        frictions["status"] = "UNKNOWN_TIME_SUPPRESSED"
        frictions["active_crises"] = []
        frictions["active_strain_indices"] = []
        frictions["threat_vectors"] = []

    # 11. Daily Somatic & Micro-Incident Telemetry Radar
    daily_radar = compute_daily_incident_radar(natal, datetime.utcnow())

    if is_deceased:
        daily_radar["overall_status"] = "HISTORICAL_ARCHIVE_LOCKED"
        daily_radar["overall_status_label"] = "Historical Subject — Radar Archived"
        daily_radar["active_vector_count"] = 0

    remedies_list = (
        remedies.get("items", remedies) if isinstance(remedies, dict) else remedies
    )

    return {
        "subject": data.name,
        "is_deceased": is_deceased,
        "age_label": age_label,
        "age_display": age_display,
        "dasha_label": dasha_label,
        "birth_time_confidence": "unknown_defaulted"
        if birth_time_unknown
        else "confirmed",
        "city": f"{data.city}, {data.country}",
        "lagna": "Unknown (Requires exact birth time)"
        if birth_time_unknown
        else natal["lagna"]["formatted"],
        "lagna_sign": "Unknown" if birth_time_unknown else natal["lagna"]["sign"],
        "moon_sign": natal["planets"]["Moon"]["sign"],
        "moon_nakshatra": f"{moon_nak['name']} (Pada {moon_nak['pada']}, Lord: {moon_nak['lord']})",
        "current_dasha": f"{current_dasha.get('mahadasha')} - {current_dasha.get('antardasha')}",
        "current_dasha_end": current_dasha.get("period_end"),
        "current_age": round(age_years, 1),
        "vcs_badge": vcs_badge_text,
        "vcs_score": vcs_score_val,
        "vcs_status": vcs_status,
        "kundli_svg": kundli_svg,
        "planets_table": planets_table,
        "dasha_bar_svg": dasha_bar_svg,
        "primer_cards": primer_cards,
        "milestones": verified_milestones,
        "remedies": remedies_list,
        "raw_remedies": remedies,
        "domain_mantras": DOMAIN_MANTRAS,
        "soul_telemetry": soul_telemetry,
        "frictions": frictions,
        "daily_radar": daily_radar,
        "ayurdaya": compute_ayurdaya_telemetry(natal),
        "system_manifest": get_system_manifest(),
    }


@app.get("/api/system/engines")
def get_engine_registry_manifest():
    """Returns the canonical version numbers, statuses, and before/after metadata for all 8 engines."""
    return JSONResponse(get_system_manifest())


@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "manifest": get_system_manifest()})


@app.post("/api/analyze")
def analyze_chart(data: ChartRequest):
    return run_chart_pipeline(data)


class RectificationRequest(BaseModel):
    name: str = "Subject"
    date: str
    latitude: float
    longitude: float
    milestones: list[MilestoneInput]

    @field_validator("latitude")
    @classmethod
    def valid_lat(cls, v):
        if not (-90.0 <= v <= 90.0):
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator("longitude")
    @classmethod
    def valid_lon(cls, v):
        if not (-180.0 <= v <= 180.0):
            raise ValueError("Longitude must be between -180 and 180")
        return v

    @field_validator("date")
    @classmethod
    def valid_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                "Date must be in YYYY-MM-DD format and be a valid calendar date"
            )
        return v


@app.post("/api/rectify")
def rectify_birth_time(data: RectificationRequest):
    from core.rectification import run_rectification_scan

    try:
        is_historical = is_historical_benchmark_subject(
            data.model_dump() if hasattr(data, "model_dump") else data.dict(), data.name
        )
        milestones_list = [{"event": m.event, "date": m.date} for m in data.milestones]

        return run_rectification_scan(
            name=data.name,
            date_str=data.date,
            lat=data.latitude,
            lon=data.longitude,
            milestones=milestones_list,
            is_historical=is_historical,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/demo/{name}")
def get_demo_profile(name: str):
    profile_data = DEMO_PROFILES.get(name.lower(), DEMO_PROFILES["indira"])
    req = ChartRequest(**profile_data)
    return run_chart_pipeline(req)


@app.websocket("/ws/telemetry/{name}")
async def websocket_telemetry(websocket: WebSocket, name: str):
    await websocket.accept()

    profile_data = DEMO_PROFILES.get(name.lower(), DEMO_PROFILES["indira"])
    req = ChartRequest(**profile_data)

    date_parts = [int(p) for p in req.date.split("-")]
    t_parts = req.time.split(":")
    hour = int(t_parts[0])
    minute = int(t_parts[1]) if len(t_parts) > 1 else 0
    second = int(t_parts[2]) if len(t_parts) > 2 else 0

    natal = compute_natal_chart(
        year=date_parts[0],
        month=date_parts[1],
        day=date_parts[2],
        hour=hour,
        minute=minute,
        second=second,
        lat=req.latitude,
        lon=req.longitude,
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

    is_deceased = req.is_deceased or ("indira" in req.name.lower())
    death_date_str = req.death_date or (
        "1984-10-31" if is_deceased and "indira" in req.name.lower() else None
    )

    try:
        while True:
            if is_deceased and death_date_str:
                exit_dt = datetime.strptime(death_date_str, "%Y-%m-%d")
                age_years = round((exit_dt - birth_dt).days / 365.25, 1)
                current_dasha = get_active_dasha_at_date(timeline, exit_dt)
                payload = {
                    "status": "HISTORICAL_RECORD_LOCKED",
                    "current_age": age_years,
                    "age_display": f"{age_years} Years (1917–1984)",
                    "current_dasha": f"{current_dasha.get('mahadasha')} - {current_dasha.get('antardasha')} (At Demise, 1984)",
                    "timestamp": "1984-10-31 09:20:00 IST",
                }
                await websocket.send_json(payload)
                await asyncio.sleep(3600.0)
            else:
                current_dt = datetime.now()
                current_dasha = get_active_dasha_at_date(timeline, current_dt)
                age_years = (current_dt - birth_dt).days / 365.25
                transits = get_planet_transit_positions(current_dt)
                frictions = audit_live_frictions(natal, timeline, current_dt)
                daily_radar = compute_daily_incident_radar(natal, current_dt)

                payload = {
                    "timestamp": current_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "current_age": round(age_years, 8),
                    "current_dasha": f"{current_dasha.get('mahadasha')} - {current_dasha.get('antardasha')}",
                    "transits": {p: transits[p]["formatted"] for p in transits},
                    "frictions": frictions,
                    "daily_radar": daily_radar,
                }
                await websocket.send_json(payload)
                await asyncio.sleep(60.0)
    except (WebSocketDisconnect, asyncio.CancelledError):
        pass


@app.get("/api/adversarial/{name}")
def get_adversarial_test(name: str):
    from core.adversarial import run_adversarial_stress_test

    name_clean = name.lower()

    if name_clean in ["indira", "historical_indira_gandhi"]:
        if os.path.exists("benchmarks/historical_indira_gandhi.json"):
            return run_adversarial_stress_test(
                "benchmarks/historical_indira_gandhi.json"
            )

    if name_clean in ["anonymous", "example_anonymous", "synthetic_archetype_01"]:
        if os.path.exists("profiles/example_anonymous.json"):
            return run_adversarial_stress_test("profiles/example_anonymous.json")

    # Strict Privacy Safeguard: Private profiles are never exposed via the public REST API.
    # Fall back to public historical benchmark.
    if os.path.exists("benchmarks/historical_indira_gandhi.json"):
        return run_adversarial_stress_test("benchmarks/historical_indira_gandhi.json")

    return JSONResponse(
        status_code=404, content={"error": "Benchmark profile not found"}
    )


@app.get("/api/geocode")
def geocode_api(q: str = ""):
    return geocode_location(q)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
