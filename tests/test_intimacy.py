"""Tests for symbolic intimacy / desire telemetry."""

from __future__ import annotations

import unittest

from core.dasha import compute_vimshottari_timeline, get_active_dasha_at_date
from core.ephemeris import compute_natal_chart
from core.intimacy import evaluate_intimacy_telemetry
from datetime import datetime


class TestIntimacyTelemetry(unittest.TestCase):
    def setUp(self):
        self.natal = compute_natal_chart(1999, 4, 24, 7, 0, 0, 26.4652, 80.3498)
        moon = self.natal["planets"]["Moon"]["nakshatra"]
        birth = datetime(1999, 4, 24, 7, 0, 0)
        timeline = compute_vimshottari_timeline(
            birth, moon["lord"], moon["fraction_elapsed"]
        )
        self.dasha = get_active_dasha_at_date(timeline, datetime(2026, 10, 9, 12, 0, 0))

    def test_profile_ok(self):
        out = evaluate_intimacy_telemetry(self.natal, active_dasha=self.dasha)
        self.assertEqual(out["status"], "OK")
        self.assertIsInstance(out["desire_index"], float)
        self.assertGreaterEqual(out["desire_index"], 20.0)
        self.assertLessEqual(out["desire_index"], 92.0)
        self.assertTrue(out["venus_style"])
        self.assertTrue(out["mars_style"])
        self.assertGreaterEqual(len(out["factors"]), 5)
        self.assertIn("consent", out["epistemic_notice"].lower())

    def test_unknown_birth_time_suppresses_houses(self):
        out = evaluate_intimacy_telemetry(
            self.natal, active_dasha=self.dasha, birth_time_unknown=True
        )
        self.assertEqual(out["status"], "LAGNA_SUPPRESSED")
        self.assertIsNone(out["desire_index"])


if __name__ == "__main__":
    unittest.main()
