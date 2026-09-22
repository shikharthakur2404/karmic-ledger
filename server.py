import asyncio
import os
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, field_validator

from core.confluence import evaluate_event_confluence
from core.consent import is_historical_benchmark_subject
from core.dasha import compute_vimshottari_timeline, get_active_dasha_at_date
from core.ephemeris import compute_natal_chart
from core.frictions import audit_live_frictions
from core.mantras import DOMAIN_MANTRAS, recommend_remedies_for_chart
from core.primer import explain_planet_placement
from core.shastra import search_shastra
from core.soul import evaluate_soul_telemetry
from core.transits import get_planet_transit_positions
from core.verifier import parse_event_date
from core.visuals import generate_dasha_progress_bar_svg, generate_diamond_kundli_svg

app = FastAPI(
    title="Karmic Ledger API",
    description="Analytical Jyotish Telemetry & Algorithmic Sensitivity Engine",
)

templates = Jinja2Templates(directory="templates")

DEMO_PROFILES = {
    "indira": {
        "name": "Indira Gandhi (Historical Benchmark)",
        "date": "1917-11-19",
        "time": "23:11:00",
        "latitude": 25.4358,
        "longitude": 81.8463,
        "city": "Allahabad",
        "country": "India",
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
    raw_dict = data.dict() if hasattr(data, "dict") else data.model_dump()
    is_historical = is_historical_benchmark_subject(raw_dict, data.name)

    # Mandatory Server-Side Affirmative Consent Gate
    if not data.consent and not is_historical:
        raise HTTPException(
            status_code=403,
            detail="Affirmative epistemic consent required. Processing halted under zero-diagnostic research boundary.",
        )

    birth_time_unknown = not data.time.strip()
    actual_time = "12:00:00" if birth_time_unknown else data.time

    date_parts = [int(p) for p in data.date.split("-")]
    t_parts = actual_time.split(":")
    hour = int(t_parts[0])
    minute = int(t_parts[1]) if len(t_parts) > 1 else 0
    second = int(t_parts[2]) if len(t_parts) > 2 else 0

    # 1. Compute Natal Coordinates
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

    # 2. 120-Year Vimshottari Timeline
    timeline = compute_vimshottari_timeline(
        birth_dt=birth_dt,
        moon_nakshatra_lord=moon_nak["lord"],
        fraction_elapsed=moon_nak["fraction_elapsed"],
    )

    # 3. Active Dasha in 2026
    current_dt = datetime.now()
    current_dasha = get_active_dasha_at_date(timeline, current_dt)
    age_years = (current_dt - birth_dt).days / 365.25

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
    dasha_bar_svg = generate_dasha_progress_bar_svg(timeline, age_years)

    # 8. Soul Age & Archetype Telemetry
    soul_telemetry = evaluate_soul_telemetry(natal)

    # 9. Live Karmic Friction & Crisis Diagnostic
    frictions = audit_live_frictions(natal, timeline, current_dt)

    if birth_time_unknown:
        frictions["status"] = "UNKNOWN_TIME_SUPPRESSED"
        frictions["active_crises"] = []
        frictions["active_strain_indices"] = []
        frictions["threat_vectors"] = []

    return {
        "subject": data.name,
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
        "dasha_bar_svg": dasha_bar_svg,
        "primer_cards": primer_cards,
        "milestones": verified_milestones,
        "remedies": remedies,
        "domain_mantras": DOMAIN_MANTRAS,
        "soul_telemetry": soul_telemetry,
        "frictions": frictions,
    }


@app.get("/", response_class=HTMLResponse)
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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

    try:
        while True:
            current_dt = datetime.now()
            current_dasha = get_active_dasha_at_date(timeline, current_dt)
            age_years = (current_dt - birth_dt).days / 365.25
            transits = get_planet_transit_positions(current_dt)
            frictions = audit_live_frictions(natal, timeline, current_dt)

            payload = {
                "timestamp": current_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
                "current_age": round(age_years, 8),
                "current_dasha": f"{current_dasha.get('mahadasha')} - {current_dasha.get('antardasha')}",
                "transits": {p: transits[p]["formatted"] for p in transits},
                "frictions": frictions,
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
