"""
karmic-ledger: Event Verification & Vedic Correlation Score (VCS) Engine
Replaces subjective fortune-telling with a mathematical event-backtesting pipeline.
"""

import json
import re
from datetime import datetime
from typing import Any

from core.confluence import evaluate_event_confluence
from core.consent import is_historical_benchmark_subject, verify_subject_consent
from core.dasha import compute_vimshottari_timeline, get_active_dasha_at_date
from core.ephemeris import compute_natal_chart
from core.frictions import audit_live_frictions
from core.soul import evaluate_soul_telemetry
from core.transits import get_planet_transit_positions


def parse_event_date(date_str: str) -> datetime:
    """Parses various event date formats (YYYY, YYYY-MM, YYYY-MM-DD) even with text notes."""
    # Find all sequences of digits
    digits = re.findall(r"\d+", date_str.strip())
    if not digits:
        return datetime(2000, 1, 1, 12, 0)

    year = int(digits[0])
    month = int(digits[1]) if len(digits) > 1 and 1 <= int(digits[1]) <= 12 else 7
    day = int(digits[2]) if len(digits) > 2 and 1 <= int(digits[2]) <= 31 else 15

    return datetime(year, month, day, 12, 0)


def verify_profile_milestones(profile_path: str) -> dict[str, Any]:
    """
    Ingests a profile fixture and backtests its milestones against
    Vimshottari sub-dashas, planetary transits, and classical shastra rules.
    """
    with open(profile_path, encoding="utf-8") as f:
        data = json.load(f)

    # Consent Enforcement Gate
    has_consent, consent_msg = verify_subject_consent(data, profile_path)
    if not has_consent:
        return {
            "status": "PROCESSING_HALTED",
            "error": "CONSENT_GATE_LOCKED",
            "reason": consent_msg,
            "subject": "REDACTED // CONSENT REQUIRED",
            "lagna": "N/A",
            "moon_nakshatra": "N/A",
            "average_vedic_correlation_score": "0.0%",
            "calibration_results": [],
            "soul_telemetry": {},
            "frictions": [],
        }

    is_historical = is_historical_benchmark_subject(data, profile_path)
    subject_name = data.get("name", "Unknown Subject")
    bdata = data.get("birth_data", {})

    # Extract date & time
    date_parts = [int(p) for p in bdata.get("date", "2000-01-01").split("-")]
    time_str = bdata.get("time") or bdata.get("rectified_time", "07:00:00")

    # Default 07:00:00 if unparseable
    hour, minute, second = 7, 0, 0
    if ":" in time_str:
        # Extract the first valid HH:MM
        clean_time = time_str.split()[0]
        t_parts = clean_time.split(":")
        hour = int(t_parts[0])
        minute = int(t_parts[1]) if len(t_parts) > 1 else 0
        second = int(t_parts[2]) if len(t_parts) > 2 else 0

    lat = float(bdata.get("latitude", 20.0))
    lon = float(bdata.get("longitude", 78.0))
    tz_offset = float(bdata.get("timezone_offset", 5.5))

    # 1. Compute Natal Coordinates
    natal = compute_natal_chart(
        year=date_parts[0],
        month=date_parts[1],
        day=date_parts[2],
        hour=hour,
        minute=minute,
        second=second,
        lat=lat,
        lon=lon,
        tz_offset_hours=tz_offset,
    )

    birth_dt = datetime(
        date_parts[0], date_parts[1], date_parts[2], hour, minute, second
    )
    moon_nak = natal["planets"]["Moon"]["nakshatra"]

    # 2. Compute 120-Year Vimshottari Timeline
    dasha_timeline = compute_vimshottari_timeline(
        birth_dt=birth_dt,
        moon_nakshatra_lord=moon_nak["lord"],
        fraction_elapsed=moon_nak["fraction_elapsed"],
    )

    # 3. Backtest Milestones
    raw_milestones = (
        data.get("biographical_milestones")
        or data.get("biographical_calibrations")
        or data.get("biographical_event_locking")
        or []
    )

    verified_results: list[dict[str, Any]] = []
    total_score = 0.0
    evaluated_count = 0

    for item in raw_milestones:
        event_name = item.get("event") or item.get("milestone", "Unnamed Event")
        date_val = item.get("date") or str(item.get("year", "2020"))
        event_dt = parse_event_date(date_val)

        # Determine active Dasha on that date
        dasha_active = get_active_dasha_at_date(dasha_timeline, event_dt)

        # Check active planetary transits
        transits_active = get_planet_transit_positions(event_dt)

        # Calculate Vedic Correlation Score (VCS) via Astrological Event Confluence
        confluence = evaluate_event_confluence(
            natal=natal,
            dasha_active=dasha_active,
            transits_active=transits_active,
            event_name=event_name,
            category_hint=item.get("category"),
            is_historical_benchmark=is_historical,
        )
        score = confluence["confluence_score"]
        citation_str = confluence["shastra_citation"]

        verified_results.append(
            {
                "event": event_name,
                "domain": confluence["domain"],
                "target_date": event_dt.strftime("%Y-%m-%d"),
                "active_mahadasha": dasha_active.get("mahadasha", "N/A"),
                "active_antardasha": dasha_active.get("antardasha", "N/A"),
                "dasha_span": f"{dasha_active.get('period_start', '')} to {dasha_active.get('period_end', '')}",
                "saturn_transit": transits_active["Saturn"]["formatted"],
                "jupiter_transit": transits_active["Jupiter"]["formatted"],
                "shastra_citation": citation_str,
                "correlation_score": score,
                "confluence_mechanics": confluence["confluence_mechanics"],
            }
        )

        total_score += score
        evaluated_count += 1

    avg_vcs = round(total_score / max(evaluated_count, 1), 1)
    soul_telemetry = evaluate_soul_telemetry(natal)
    frictions = audit_live_frictions(natal, dasha_timeline)

    return {
        "subject": subject_name,
        "lagna": natal["lagna"]["formatted"],
        "moon_nakshatra": f"{moon_nak['name']} (Pada {moon_nak['pada']}, Lord: {moon_nak['lord']})",
        "average_vedic_correlation_score": f"{avg_vcs}%",
        "calibration_results": verified_results,
        "soul_telemetry": soul_telemetry,
        "frictions": frictions,
    }
