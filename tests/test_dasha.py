"""Tests for Vimshottari year length, invariants, windows, and JH golden-master hook."""

from __future__ import annotations

import json
import unittest
from datetime import datetime
from pathlib import Path

from core.dasha import (
    DASHA_MAP,
    DASHA_ORDER,
    DASHA_YEAR_DAYS,
    TOTAL_DASHA_CYCLE,
    compute_vimshottari_timeline,
    dasha_boundary_shift_days_per_minute,
    event_window_half_width_days,
    get_active_dasha_at_date,
    years_to_timedelta,
)


class TestDashaYearLength(unittest.TestCase):
    def test_year_constant(self):
        self.assertEqual(DASHA_YEAR_DAYS, 365.25)

    def test_full_cycle_sums_to_120(self):
        self.assertEqual(sum(span for _, span in DASHA_ORDER), TOTAL_DASHA_CYCLE)

    def test_antardasha_sum_matches_mahadasha(self):
        birth = datetime(1950, 1, 15, 10, 30, 0)
        # fraction_elapsed=0 ⇒ full first mahadasha
        timeline = compute_vimshottari_timeline(birth, "Venus", 0.0)
        for maha in timeline:
            ad_sum = sum(a["duration_years"] for a in maha["antardashas"])
            self.assertAlmostEqual(ad_sum, maha["duration_years"], places=2)

    def test_timeline_uses_365_25_spacing(self):
        birth = datetime(2000, 6, 1, 12, 0, 0)
        timeline = compute_vimshottari_timeline(birth, "Sun", 0.0)
        sun_maha = timeline[0]
        self.assertEqual(sun_maha["mahadasha"], "Sun")
        self.assertAlmostEqual(sun_maha["duration_years"], 6.0, places=3)
        # 6 * 365.25 = 2191.5 days exactly in timedelta space
        self.assertAlmostEqual(
            years_to_timedelta(6.0).total_seconds() / 86400.0, 2191.5, places=5
        )

    def test_active_dasha_lookup(self):
        birth = datetime(1990, 3, 21, 8, 0, 0)
        timeline = compute_vimshottari_timeline(birth, "Moon", 0.25)
        active = get_active_dasha_at_date(timeline, birth)
        self.assertEqual(active["mahadasha"], "Moon")
        self.assertNotIn("error", active)

    def test_boundary_shift_range(self):
        # ~1.5–5 days per minute across lords
        shifts = {
            lord: dasha_boundary_shift_days_per_minute(lord) for lord, _ in DASHA_ORDER
        }
        self.assertGreater(min(shifts.values()), 1.3)
        self.assertLess(max(shifts.values()), 5.2)
        self.assertAlmostEqual(shifts["Venus"] / shifts["Sun"], DASHA_MAP["Venus"] / DASHA_MAP["Sun"], places=5)

    def test_event_window_formula_covers_long_lords(self):
        # Flat ±3 would under-cover Venus; formula must widen
        self.assertGreaterEqual(event_window_half_width_days("Venus"), 9)
        self.assertGreaterEqual(event_window_half_width_days("Saturn"), 8)
        self.assertLessEqual(event_window_half_width_days("Sun"), 4)


class TestJagannathaHoraGoldenMaster(unittest.TestCase):
    FIXTURE = Path(__file__).parent / "fixtures" / "jh_vimshottari_golden.json"

    def test_jh_golden_master(self):
        data = json.loads(self.FIXTURE.read_text(encoding="utf-8"))
        if not data.get("populated") or len(data.get("charts", [])) < 4:
            self.skipTest(
                "JH golden-master not populated yet. Export 4–5 charts from "
                "Jagannatha Hora by hand into tests/fixtures/jh_vimshottari_golden.json"
            )

        self.assertEqual(data["settings"]["dasha_year_days"], 365.25)
        for chart in data["charts"]:
            birth = datetime.fromisoformat(chart["birth_iso"])
            timeline = compute_vimshottari_timeline(
                birth,
                chart["moon_nakshatra_lord"],
                float(chart["fraction_elapsed"]),
            )
            for expected in chart["expected_boundaries"]:
                maha = next(
                    m for m in timeline if m["mahadasha"] == expected["mahadasha"]
                )
                if "antardasha" in expected:
                    antar = next(
                        a
                        for a in maha["antardashas"]
                        if a["antardasha"] == expected["antardasha"]
                    )
                    self.assertEqual(antar["start_date"], expected["start_date"])
                    self.assertEqual(antar["end_date"], expected["end_date"])
                else:
                    self.assertEqual(maha["start_date"], expected["start_date"])
                    self.assertEqual(maha["end_date"], expected["end_date"])


if __name__ == "__main__":
    unittest.main()
