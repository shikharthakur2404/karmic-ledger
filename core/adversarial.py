"""
karmic-ledger: Adversarial Stress-Testing & Sensitivity Engine
Evaluates algorithmic sensitivity to input parameter perturbations:
temporal desynchronization, Lagna rotation, and AM/PM inversion.
Measures whether the internal rule matrix demonstrates input discrimination
or exhibits trivial confirmation bias.
"""

import json
from datetime import datetime, timedelta
from typing import Any

from core.confluence import evaluate_event_confluence
from core.consent import is_historical_benchmark_subject, verify_subject_consent
from core.dasha import compute_vimshottari_timeline, get_active_dasha_at_date
from core.ephemeris import compute_natal_chart
from core.transits import get_planet_transit_positions
from core.verifier import parse_event_date, verify_profile_milestones


def run_adversarial_stress_test(profile_path: str) -> dict[str, Any]:
    """
    Executes an adversarial battery against a profile:
    1. Baseline ground truth calibration.
    2. +3 Years Temporal Shift (Dasha Desynchronization).
    3. -3 Years Temporal Shift.
    4. +6 Hours Shift (Bhava/Lagna Rotation by ~3 signs).
    5. 12-Hour AM/PM Inversion (180° Bhavachakra Flip).
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
            "baseline_vcs": "0.0%",
            "average_corrupted_vcs": "0.0%",
            "discrimination_margin": "0.0%",
            "resilience_verdict": "CONSENT_DENIED",
            "mutations_tested": 0,
            "falsification_pass_rate": "0/0",
            "evaluations": [],
        }

    is_historical = is_historical_benchmark_subject(data, profile_path)
    subject_name = data.get("name", "Unknown Subject")
    bdata = data.get("birth_data", {})

    # 1. Baseline Evaluation
    baseline_result = verify_profile_milestones(profile_path)
    baseline_vcs = float(
        baseline_result["average_vedic_correlation_score"].replace("%", "")
    )

    # Define Adversarial Mutations
    mutations = [
        {
            "mutation_id": "SHIFT_PLUS_3Y",
            "name": "Date Shift (+3 Years Later)",
            "description": "Shifts birth year forward by 3 years. Tests if the life timeline completely desynchronizes.",
            "date_delta_years": 3,
            "hour_delta": 0,
        },
        {
            "mutation_id": "SHIFT_MINUS_3Y",
            "name": "Date Shift (-3 Years Earlier)",
            "description": "Shifts birth year back by 3 years. Tests if planetary periods misalign with real life events.",
            "date_delta_years": -3,
            "hour_delta": 0,
        },
        {
            "mutation_id": "LAGNA_ROTATION_6H",
            "name": "Time Shift (+6 Hours Later)",
            "description": "Shifts birth time forward by 6 hours. Rotates the rising sign by ~3 signs, scrambling all life house areas.",
            "date_delta_years": 0,
            "hour_delta": 6,
        },
        {
            "mutation_id": "INVERSION_12H",
            "name": "Day/Night Flip (12-Hour Shift)",
            "description": "Inverts AM and PM by 12 hours, reversing day and night to test sensitivity to exact birth hour.",
            "date_delta_years": 0,
            "hour_delta": 12,
        },
    ]

    date_str = bdata.get("date", "2000-01-01")
    time_str = bdata.get("time") or bdata.get("rectified_time", "07:00:00")
    lat = float(bdata.get("latitude", 20.0))
    lon = float(bdata.get("longitude", 78.0))

    tz_offset = float(bdata.get("timezone_offset", 5.5))

    base_parts = [int(p) for p in date_str.split("-")]
    t_clean = time_str.split()[0]
    t_parts = [int(p) for p in t_clean.split(":")]
    base_h = t_parts[0]
    base_m = t_parts[1] if len(t_parts) > 1 else 0
    base_s = t_parts[2] if len(t_parts) > 2 else 0

    raw_milestones = (
        data.get("biographical_milestones")
        or data.get("biographical_calibrations")
        or data.get("biographical_event_locking")
        or []
    )

    adversarial_evaluations: list[dict[str, Any]] = []

    for mut in mutations:
        # Construct corrupted birth time
        mut_year = base_parts[0] + mut["date_delta_years"]
        mut_dt = datetime(
            mut_year, base_parts[1], base_parts[2], base_h, base_m, base_s
        ) + timedelta(hours=mut["hour_delta"])

        # Compute corrupted natal chart
        corrupted_natal = compute_natal_chart(
            year=mut_dt.year,
            month=mut_dt.month,
            day=mut_dt.day,
            hour=mut_dt.hour,
            minute=mut_dt.minute,
            second=mut_dt.second,
            lat=lat,
            lon=lon,
            tz_offset_hours=tz_offset,
        )

        moon_nak = corrupted_natal["planets"]["Moon"]["nakshatra"]
        corrupted_timeline = compute_vimshottari_timeline(
            birth_dt=mut_dt,
            moon_nakshatra_lord=moon_nak["lord"],
            fraction_elapsed=moon_nak["fraction_elapsed"],
        )

        # Score milestones against corrupted chart
        total_corrupted_score = 0.0
        event_breakdown = []

        for item in raw_milestones:
            event_name = item.get("event") or item.get("milestone", "Event")
            date_val = item.get("date") or str(item.get("year", "2020"))
            event_dt = parse_event_date(date_val)

            d_active = get_active_dasha_at_date(corrupted_timeline, event_dt)
            t_active = get_planet_transit_positions(event_dt)

            confluence = evaluate_event_confluence(
                natal=corrupted_natal,
                dasha_active=d_active,
                transits_active=t_active,
                event_name=event_name,
                category_hint=item.get("category"),
                is_historical_benchmark=is_historical,
            )
            score = confluence["confluence_score"]
            total_corrupted_score += score
            event_breakdown.append(
                {
                    "event": event_name,
                    "corrupted_dasha": f"{d_active.get('mahadasha')}-{d_active.get('antardasha')}",
                    "corrupted_score": score,
                }
            )

        corrupted_avg = round(total_corrupted_score / max(len(raw_milestones), 1), 1)
        delta_vcs = round(baseline_vcs - corrupted_avg, 1)

        adversarial_evaluations.append(
            {
                "mutation_id": mut["mutation_id"],
                "name": mut["name"],
                "description": mut["description"],
                "corrupted_birth_dt": mut_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "corrupted_lagna": corrupted_natal["lagna"]["formatted"],
                "corrupted_vcs": corrupted_avg,
                "delta_vcs": delta_vcs,
                "falsified_successfully": delta_vcs > 15.0,
                "event_breakdown": event_breakdown,
            }
        )

    avg_corrupted_vcs = round(
        sum(m["corrupted_vcs"] for m in adversarial_evaluations)
        / len(adversarial_evaluations),
        1,
    )
    mean_discrimination_margin = round(baseline_vcs - avg_corrupted_vcs, 1)

    # Engine demonstrates sensitivity if corrupted data produces significant score degradation
    is_sensitive = mean_discrimination_margin >= 20.0

    return {
        "subject": subject_name,
        "baseline_vcs": f"{baseline_vcs}%",
        "average_corrupted_vcs": f"{avg_corrupted_vcs}%",
        "discrimination_margin": f"+{mean_discrimination_margin}%",
        "resilience_verdict": "MEASURABLY SENSITIVE TO BIRTH DATA"
        if is_sensitive
        else "LOW SENSITIVITY // INSUFFICIENT SEPARATION",
        "mutations_tested": len(adversarial_evaluations),
        "falsification_pass_rate": f"{sum(1 for m in adversarial_evaluations if m['falsified_successfully'])}/{len(adversarial_evaluations)}",
        "evaluations": adversarial_evaluations,
    }
