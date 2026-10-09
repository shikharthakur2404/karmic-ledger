"""Tests for symbolic shaadi / partnership timing windows."""

from __future__ import annotations

import unittest
from datetime import datetime

from core.dasha import compute_vimshottari_timeline
from core.ephemeris import compute_natal_chart
from core.timing_windows import evaluate_shaadi_timing_windows, seventh_lord


class TestTimingWindows(unittest.TestCase):
    def test_seventh_lord_aquarius(self):
        self.assertEqual(seventh_lord("Aquarius"), "Sun")

    def test_windows_for_soham_like_chart(self):
        natal = compute_natal_chart(2000, 11, 10, 9, 10, 0, 17.6370, 74.4018)
        moon = natal["planets"]["Moon"]["nakshatra"]
        birth = datetime(2000, 11, 10, 9, 10, 0)
        timeline = compute_vimshottari_timeline(
            birth, moon["lord"], moon["fraction_elapsed"]
        )
        out = evaluate_shaadi_timing_windows(
            natal, timeline, as_of=datetime(2026, 10, 9)
        )
        self.assertEqual(out["status"], "OK")
        self.assertTrue(out["seventh_lord"])
        self.assertIsInstance(out["windows"], list)
        self.assertIn("consent", out["epistemic_notice"].lower())


if __name__ == "__main__":
    unittest.main()
