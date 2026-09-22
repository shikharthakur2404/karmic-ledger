from datetime import datetime, timedelta
from typing import Any

from core.confluence import classify_event_domain, evaluate_event_confluence
from core.dasha import compute_vimshottari_timeline, get_active_dasha_at_date
from core.ephemeris import compute_natal_chart
from core.transits import get_planet_transit_positions
from core.verifier import parse_event_date


def run_rectification_scan(
    name: str,
    date_str: str,
    lat: float,
    lon: float,
    milestones: list[dict[str, str]],
    is_historical: bool = False,
    debug: bool = False,
) -> dict[str, Any]:
    """
    Scans a 24-hour period at 5-minute intervals to find probabilistic time windows
    where historical milestones align with Parashari heuristics (Dasha & Transit).
    """
    if not debug:
        return {
            "status": "FEATURE_SUSPENDED_PENDING_VALIDATION",
            "epistemic_warning": "Rectification engine is suspended due to insufficient empirical separation from chance. A held-out validation study (N=30) is required before surfacing candidate Lagnas or VCS scores.",
            "candidates": [],
        }

    if len(milestones) < 5:
        raise ValueError(
            "Insufficient milestones. Rectification requires a minimum of 5 verified life events."
        )

    # Pre-flight check: Vague milestones (noise) score artificially high due to broad house rules.
    # We strictly require distinct categorized events for a valid mathematical baseline.
    for m in milestones:
        domain = classify_event_domain(
            m["event"], is_historical_benchmark=is_historical
        )
        if domain == "GENERAL_SIGNIFICANT_EVENT":
            raise ValueError(
                f"Milestone '{m['event']}' is too vague. Rectification requires specific categorized events "
                "(e.g., 'Marriage', 'Job Loss', 'Childbirth', 'Relocation')."
            )

    date_parts = [int(p) for p in date_str.split("-")]
    year, month, day = date_parts[0], date_parts[1], date_parts[2]

    # Pre-parse transits since they don't change based on birth time (saving CPU)
    parsed_milestones = []
    for m in milestones:
        edt = parse_event_date(m["date"])
        parsed_milestones.append(
            {
                "event": m["event"],
                "event_dt": edt,
                "transits": get_planet_transit_positions(edt),
            }
        )

    start_time = datetime(year, month, day, 0, 0, 0)
    end_time = datetime(year, month, day, 23, 55, 0)

    results = []
    curr = start_time

    while curr <= end_time:
        try:
            natal = compute_natal_chart(
                year=year,
                month=month,
                day=day,
                hour=curr.hour,
                minute=curr.minute,
                second=0,
                lat=lat,
                lon=lon,
                tz_offset_hours=5.5,
            )
            moon_nak = natal["planets"]["Moon"]["nakshatra"]
            timeline = compute_vimshottari_timeline(
                birth_dt=curr,
                moon_nakshatra_lord=moon_nak["lord"],
                fraction_elapsed=moon_nak["fraction_elapsed"],
            )

            total_score = 0.0
            for pm in parsed_milestones:
                d_active = get_active_dasha_at_date(timeline, pm["event_dt"])
                conf = evaluate_event_confluence(
                    natal=natal,
                    dasha_active=d_active,
                    transits_active=pm["transits"],
                    event_name=pm["event"],
                    is_historical_benchmark=is_historical,
                )
                total_score += conf.get("confluence_score", 75.0)

            avg_score = total_score / len(parsed_milestones)

            results.append(
                {"time": curr, "score": avg_score, "lagna": natal["lagna"]["sign"]}
            )
        except Exception:
            pass  # Skip mathematically impossible times

        curr += timedelta(minutes=5)

    if not results:
        return {
            "status": "FAILED_EVALUATION",
            "epistemic_warning": "Engine failed to evaluate any valid planetary combinations for this date/location.",
            "candidate_windows": [],
        }

    # Group adjacent high scores into windows
    THRESHOLD = 65.0
    candidate_windows = []

    current_window = []
    for r in results:
        if r["score"] >= THRESHOLD:
            current_window.append(r)
        else:
            if current_window:
                candidate_windows.append(current_window)
                current_window = []
    if current_window:
        candidate_windows.append(current_window)

    if not candidate_windows:
        return {
            "status": "NO_HIGH_CONFIDENCE_WINDOWS",
            "epistemic_warning": "Heuristic geometric alignments only. Not a definitive biological timestamp.",
            "candidate_windows": [],
        }

    scores = [r["score"] for r in results]
    mean_score = sum(scores) / len(scores)
    import math

    variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
    std_dev = math.sqrt(variance) if variance > 0 else 1.0

    processed_windows = []
    for win in candidate_windows:
        peak = max(win, key=lambda x: x["score"])
        lagnas = [x["lagna"] for x in win]
        dominant_lagna = max(set(lagnas), key=lagnas.count)

        peak_score = peak["score"]
        z_score = (peak_score - mean_score) / std_dev

        processed_windows.append(
            {
                "lagna": dominant_lagna,
                "peak_vcs": round(peak_score, 1),
                "z_score": round(z_score, 2),
            }
        )

    # Deduplicate by Lagna (since adjacent windows might share the same Lagna but were split by a minor dip)
    unique_lagnas = {}
    for w in processed_windows:
        lagna_key = w["lagna"]
        if (
            lagna_key not in unique_lagnas
            or w["z_score"] > unique_lagnas[lagna_key]["z_score"]
        ):
            unique_lagnas[lagna_key] = w

    final_candidates = sorted(
        unique_lagnas.values(), key=lambda x: x["z_score"], reverse=True
    )

    return {
        "status": "CANDIDATES_GENERATED",
        "epistemic_warning": "Heuristic geometric alignments only. Insufficient empirical separation from chance.",
        "baseline_stats": {"mean": round(mean_score, 1), "std_dev": round(std_dev, 1)},
        "candidates": final_candidates[:3],
    }
