"""Print KL-N30-001 freeze-gate status (human + CI readable)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from core.dasha import DASHA_YEAR_DAYS  # noqa: E402


def main() -> None:
    jh = ROOT / "tests" / "fixtures" / "jh_vimshottari_golden.json"
    jh_data = json.loads(jh.read_text(encoding="utf-8")) if jh.exists() else {}
    charts = jh_data.get("charts") or []
    populated = bool(jh_data.get("populated")) and len(charts) >= int(
        jh_data.get("min_charts_required", 4)
    )

    gates = {
        "dasha_year_days_365_25": DASHA_YEAR_DAYS == 365.25,
        "vcs_study_profile_exists": True,  # covered by tests/test_vcs_profile.py
        "jh_golden_populated": populated,
        "jh_chart_count": len(charts),
        "score_heldout_script": (
            ROOT / "studies" / "kl_n30_001" / "score_heldout.py"
        ).exists(),
        "domain_map_script": (
            ROOT / "studies" / "kl_n30_001" / "domain_map.py"
        ).exists(),
        "power_sim_script": (
            ROOT / "studies" / "kl_n30_001" / "power_sim.py"
        ).exists(),
        "discrimination_audit_script": (
            ROOT / "studies" / "kl_n30_001" / "discrimination_audit.py"
        ).exists(),
        "terms_gate": "HUMAN — tick Astro-Databank terms in prereg §2",
        "engine_freeze_tag": "HUMAN — git tag study/KL-N30-001-engine-freeze after JH green",
        "kl_n30_freeze_run_env": os.getenv("KL_N30_FREEZE_RUN", "0"),
    }
    code_ready = all(
        [
            gates["dasha_year_days_365_25"],
            gates["score_heldout_script"],
            gates["domain_map_script"],
            gates["power_sim_script"],
            gates["discrimination_audit_script"],
        ]
    )
    freeze_ready = code_ready and populated
    report = {
        "study_id": "KL-N30-001",
        "code_scaffolding_ready": code_ready,
        "engine_freeze_ready": freeze_ready,
        "blocker": None
        if freeze_ready
        else (
            "Populate tests/fixtures/jh_vimshottari_golden.json from Jagannatha Hora "
            "(≥4 charts), then: KL_N30_FREEZE_RUN=1 pytest tests/test_dasha.py"
            if not populated
            else "Unknown blocker"
        ),
        "gates": gates,
    }
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if freeze_ready else 2)


if __name__ == "__main__":
    main()
