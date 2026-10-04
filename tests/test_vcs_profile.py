"""Tests for KL-N30-001 VCS study profile vs production heuristics."""

from __future__ import annotations

import unittest
from datetime import datetime

from core.confluence import evaluate_event_confluence
from core.dasha import compute_vimshottari_timeline, get_active_dasha_at_date
from core.ephemeris import compute_natal_chart
from core.transits import get_planet_transit_positions


class TestVcsProfiles(unittest.TestCase):
    def setUp(self):
        # Public historical fixture coordinates (Gandhi) — tuning cohort, not held-out
        self.natal = compute_natal_chart(1869, 10, 2, 7, 11, 0, 21.7645, 72.1519)
        birth = datetime(1869, 10, 2, 7, 11, 0)
        moon = self.natal["planets"]["Moon"]["nakshatra"]
        self.timeline = compute_vimshottari_timeline(
            birth, moon["lord"], moon["fraction_elapsed"]
        )
        self.event_dt = datetime(1947, 8, 15, 12, 0, 0)
        self.dasha = get_active_dasha_at_date(self.timeline, self.event_dt)
        self.transits = get_planet_transit_positions(self.event_dt)

    def test_study_weights_sum_to_100(self):
        result = evaluate_event_confluence(
            self.natal,
            self.dasha,
            self.transits,
            "Independence of India",
            category_hint="CAREER_OR_POWER_ELEVATION",
            is_historical_benchmark=True,
            vcs_profile="kl_n30_001",
        )
        breakdown = result["scores_breakdown"]
        self.assertEqual(breakdown["component_weight_sum"], 100.0)
        self.assertEqual(breakdown["transit_cap"], 20.0)
        self.assertLessEqual(breakdown["mahadasha_score"], 40.0)
        self.assertLessEqual(breakdown["antardasha_score"], 40.0)
        self.assertLessEqual(breakdown["transit_score"], 20.0)
        self.assertLessEqual(result["confluence_score"], 100.0)
        self.assertGreaterEqual(result["confluence_score"], 0.0)

    def test_study_excludes_dual_bonus_and_void_language(self):
        result = evaluate_event_confluence(
            self.natal,
            self.dasha,
            self.transits,
            "Independence of India",
            category_hint="CAREER_OR_POWER_ELEVATION",
            is_historical_benchmark=True,
            vcs_profile="kl_n30_001",
        )
        joined = " | ".join(result["confluence_mechanics"])
        self.assertNotIn("Dual Dasha Confluence", joined)
        self.assertNotIn("Primary House Void", joined)
        self.assertNotIn("Pada Orb Lock", joined)
        self.assertNotIn("SAV Bindus", joined)

    def test_study_dasha_error_is_zero_not_five(self):
        result = evaluate_event_confluence(
            self.natal,
            {"error": "out of range"},
            self.transits,
            "Synthetic",
            category_hint="CAREER_OR_POWER_ELEVATION",
            is_historical_benchmark=True,
            vcs_profile="kl_n30_001",
        )
        self.assertEqual(result["confluence_score"], 0.0)

    def test_production_still_clips_to_floor(self):
        result = evaluate_event_confluence(
            self.natal,
            {"error": "out of range"},
            self.transits,
            "Synthetic",
            category_hint="CAREER_OR_POWER_ELEVATION",
            is_historical_benchmark=True,
            vcs_profile="production",
        )
        self.assertEqual(result["confluence_score"], 15.0)
        self.assertEqual(result["scores_breakdown"]["component_weight_sum"], 105.0)


if __name__ == "__main__":
    unittest.main()
