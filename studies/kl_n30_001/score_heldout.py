"""Primary scoring entrypoint for KL-N30-001 (prereg §10).

Pins vcs_profile=kl_n30_001 and section-4 settings. Does not draw cohort or
touch held-out data until events.jsonl exists after the prereg tag.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from core.confluence import evaluate_event_confluence  # noqa: E402
from core.dasha import (  # noqa: E402
    DASHA_YEAR_DAYS,
    compute_vimshottari_timeline,
    event_window_half_width_from_natal,
    get_active_dasha_at_date,
)
from core.ephemeris import compute_natal_chart  # noqa: E402
from core.transits import get_planet_transit_positions  # noqa: E402
from studies.kl_n30_001.domain_map import map_event_domain  # noqa: E402

STUDY_ID = "KL-N30-001"
VCS_PROFILE = "kl_n30_001"
OUTPUTS = Path(__file__).resolve().parent / "outputs"


def _parse_date(s: str) -> date:
    return date.fromisoformat(s[:10])


def score_subject_events(
    *,
    birth_utc: datetime,
    lat: float,
    lon: float,
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    """Score one subject: mean max-VCS over per-event windows (study path)."""
    natal = compute_natal_chart(
        birth_utc.year,
        birth_utc.month,
        birth_utc.day,
        birth_utc.hour,
        birth_utc.minute,
        birth_utc.second,
        lat,
        lon,
    )
    moon = natal["planets"]["Moon"]["nakshatra"]
    timeline = compute_vimshottari_timeline(
        birth_utc, moon["lord"], moon["fraction_elapsed"], year_days=DASHA_YEAR_DAYS
    )
    half = event_window_half_width_from_natal(natal)

    per_event: list[dict[str, Any]] = []
    for ev in events:
        etype = ev["event_type"]
        domain = map_event_domain(etype)
        d0 = _parse_date(ev["date"])
        best = 0.0
        best_day = d0.isoformat()
        for offset in range(-half, half + 1):
            d = d0 + timedelta(days=offset)
            event_dt = datetime(d.year, d.month, d.day, 12, 0, 0)
            d_active = get_active_dasha_at_date(timeline, event_dt)
            t_active = get_planet_transit_positions(event_dt)
            result = evaluate_event_confluence(
                natal=natal,
                dasha_active=d_active,
                transits_active=t_active,
                event_name=etype,
                is_historical_benchmark=True,
                vcs_profile=VCS_PROFILE,
                domain_override=domain,
            )
            score = float(result.get("confluence_score") or 0.0)
            if score > best:
                best = score
                best_day = d.isoformat()
        per_event.append(
            {
                "event_type": etype,
                "domain": domain,
                "event_date": d0.isoformat(),
                "window_half_days": half,
                "best_day": best_day,
                "vcs": best,
            }
        )

    scores = [e["vcs"] for e in per_event]
    return {
        "window_half_days": half,
        "n_events": len(per_event),
        "mean_vcs": float(sum(scores) / len(scores)) if scores else 0.0,
        "events": per_event,
        "vcs_profile": VCS_PROFILE,
        "dasha_year_days": DASHA_YEAR_DAYS,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--events",
        type=Path,
        default=Path(__file__).resolve().parent / "events.jsonl",
        help="Blind-extracted events.jsonl (required for a real run)",
    )
    ap.add_argument("--out", type=Path, default=OUTPUTS / "primary.json")
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate pins and exit without scoring (safe pre-freeze check)",
    )
    args = ap.parse_args()

    pins = {
        "study_id": STUDY_ID,
        "vcs_profile": VCS_PROFILE,
        "dasha_year_days": DASHA_YEAR_DAYS,
        "ayanamsha": "Lahiri",
        "node": "true",
        "house_system": "whole_sign",
        "domain_map": "studies/kl_n30_001/domain_map.py",
    }
    if args.dry_run:
        print(json.dumps({"status": "DRY_RUN_OK", "pins": pins}, indent=2))
        return

    if not args.events.exists():
        raise SystemExit(
            f"Missing {args.events}. Extract events blind after prereg tag; "
            "or pass --dry-run to validate pins only."
        )

    by_subj: dict[str, list[dict[str, Any]]] = {}
    meta: dict[str, dict[str, Any]] = {}
    with args.events.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            sid = row["subject_id"]
            by_subj.setdefault(sid, []).append(row)
            if sid not in meta and "birth_utc" in row:
                meta[sid] = row

    results = []
    for sid, events in sorted(by_subj.items()):
        m = meta.get(sid) or events[0]
        birth = datetime.fromisoformat(m["birth_utc"].replace("Z", "+00:00"))
        scored = score_subject_events(
            birth_utc=birth.replace(tzinfo=None),
            lat=float(m["lat"]),
            lon=float(m["lon"]),
            events=events,
        )
        results.append({"subject_id": sid, **scored})

    payload = {
        "study_id": STUDY_ID,
        "pins": pins,
        "n_subjects": len(results),
        "subjects": results,
    }
    raw = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(raw, encoding="utf-8")
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    print(json.dumps({"wrote": str(args.out), "sha256": digest, **pins}, indent=2))


if __name__ == "__main__":
    main()
