"""Pre-freeze discrimination audit (prereg §5).

Runs ONLY on excluded tuning / synthetic charts — never held-out AA.
Abort freeze if VCS SD < 5.0 or ≥80% mass in a single 5-point bin.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from core.confluence import evaluate_event_confluence  # noqa: E402
from core.dasha import (  # noqa: E402
    compute_vimshottari_timeline,
    get_active_dasha_at_date,
)
from core.ephemeris import compute_natal_chart  # noqa: E402
from core.transits import get_planet_transit_positions  # noqa: E402

# Public historical tuning chart (Gandhi) — not held-out
TUNING = {
    "label": "gandhi_tuning_excluded",
    "y": 1869,
    "m": 10,
    "d": 2,
    "h": 7,
    "mi": 11,
    "s": 0,
    "lat": 21.7645,
    "lon": 72.1519,
}


def _score_date(natal, timeline, event_dt: datetime) -> float:
    dasha = get_active_dasha_at_date(timeline, event_dt)
    transits = get_planet_transit_positions(event_dt)
    out = evaluate_event_confluence(
        natal,
        dasha,
        transits,
        "Audit random date",
        category_hint="CAREER_OR_POWER_ELEVATION",
        is_historical_benchmark=True,
        vcs_profile="kl_n30_001",
        domain_override="CAREER_OR_POWER_ELEVATION",
    )
    return float(out["confluence_score"])


def run_audit(*, n_dates: int, seed: int) -> dict:
    natal = compute_natal_chart(
        TUNING["y"],
        TUNING["m"],
        TUNING["d"],
        TUNING["h"],
        TUNING["mi"],
        TUNING["s"],
        TUNING["lat"],
        TUNING["lon"],
    )
    birth = datetime(
        TUNING["y"], TUNING["m"], TUNING["d"], TUNING["h"], TUNING["mi"], TUNING["s"]
    )
    moon = natal["planets"]["Moon"]["nakshatra"]
    timeline = compute_vimshottari_timeline(
        birth, moon["lord"], moon["fraction_elapsed"]
    )

    rng = np.random.default_rng(seed)
    start = date(1885, 1, 1)
    end = date(1947, 12, 31)
    span = (end - start).days
    scores = []
    for _ in range(n_dates):
        d = start + timedelta(days=int(rng.integers(0, span + 1)))
        scores.append(
            _score_date(natal, timeline, datetime(d.year, d.month, d.day, 12, 0, 0))
        )

    arr = np.asarray(scores, dtype=float)
    sd = float(arr.std(ddof=1))
    q75, q25 = np.percentile(arr, [75, 25])
    iqr = float(q75 - q25)
    # 5-point bins
    bins = np.floor(arr / 5.0).astype(int)
    _, counts = np.unique(bins, return_counts=True)
    max_mass = float(counts.max() / len(arr)) if len(arr) else 1.0

    abort = sd < 5.0 or max_mass >= 0.80
    payload = {
        "study_id": "KL-N30-001",
        "chart": TUNING["label"],
        "n_dates": n_dates,
        "seed": seed,
        "mean": float(arr.mean()),
        "sd": sd,
        "iqr": iqr,
        "max_5pt_bin_mass": max_mass,
        "abort_freeze": abort,
        "threshold": {"min_sd": 5.0, "max_bin_mass": 0.80},
    }
    raw = json.dumps(payload, sort_keys=True) + "\n"
    payload["sha256"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return payload


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n-dates", type=int, default=500)
    ap.add_argument("--seed", type=int, default=0x4B4C4E36)
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parent / "outputs" / "discrimination_audit.json",
    )
    args = ap.parse_args()
    report = run_audit(n_dates=args.n_dates, seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if report["abort_freeze"]:
        raise SystemExit("ABORT: discrimination audit failed freeze gates")


if __name__ == "__main__":
    main()
