"""Tests for Vimshottari year length, invariants, windows, and JH golden-master hook."""

from __future__ import annotations

import json
import os
import unittest
from datetime import datetime
from pathlib import Path

from core.dasha import (
    AA_UNCERTAINTY_MINUTES,
    DASHA_MAP,
    DASHA_ORDER,
    DASHA_YEAR_DAYS,
    MEAN_MOON_DEG_PER_HOUR,
    TOTAL_DASHA_CYCLE,
    WINDOW_ROUNDING,
    compute_vimshottari_timeline,
    dasha_boundary_shift_days_per_minute,
    event_window_half_width_days,
    event_window_half_width_from_natal,
    get_active_dasha_at_date,
    years_to_timedelta,
)
from core.ephemeris import compute_natal_chart


# Pinned mean-Moon (0.55°/h) table at t_AA=2 with math.ceil (reviewer arithmetic).
MEAN_MOON_WINDOW_TABLE = {
    "Sun": 4,
    "Mars": 4,
    "Ketu": 4,
    "Moon": 6,
    "Jupiter": 9,
    "Mercury": 9,
    "Rahu": 10,
    "Saturn": 10,
    "Venus": 11,
}


class TestDashaYearLength(unittest.TestCase):
    def test_year_constant(self):
        self.assertEqual(DASHA_YEAR_DAYS, 365.25)

    def test_full_cycle_sums_to_120(self):
        self.assertEqual(sum(span for _, span in DASHA_ORDER), TOTAL_DASHA_CYCLE)

    def test_antardasha_sum_matches_mahadasha(self):
        birth = datetime(1950, 1, 15, 10, 30, 0)
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
        self.assertAlmostEqual(
            years_to_timedelta(6.0).total_seconds() / 86400.0, 2191.5, places=5
        )

    def test_active_dasha_lookup(self):
        birth = datetime(1990, 3, 21, 8, 0, 0)
        timeline = compute_vimshottari_timeline(birth, "Moon", 0.25)
        active = get_active_dasha_at_date(timeline, birth)
        self.assertEqual(active["mahadasha"], "Moon")
        self.assertNotIn("error", active)


class TestEventWindowFormula(unittest.TestCase):
    def test_registered_constants(self):
        self.assertEqual(AA_UNCERTAINTY_MINUTES, 2.0)
        self.assertEqual(MEAN_MOON_DEG_PER_HOUR, 0.55)
        self.assertEqual(WINDOW_ROUNDING, "ceil")

    def test_aa_default_reads_module_constant(self):
        # Default arg is None → reads AA_UNCERTAINTY_MINUTES (single source of truth)
        self.assertEqual(
            event_window_half_width_days("Venus"),
            event_window_half_width_days("Venus", aa_uncertainty_min=AA_UNCERTAINTY_MINUTES),
        )

    def test_mean_moon_window_table_pinned(self):
        for lord, expected in MEAN_MOON_WINDOW_TABLE.items():
            got = event_window_half_width_days(
                lord, moon_deg_per_hour=MEAN_MOON_DEG_PER_HOUR
            )
            self.assertEqual(got, expected, msg=f"{lord}: got {got}, expected {expected}")

    def test_ceil_artifact_documented(self):
        # Sun continuous ≈ 3.01 → ceil → 4 (not 3)
        raw = AA_UNCERTAINTY_MINUTES * dasha_boundary_shift_days_per_minute(
            "Sun", moon_deg_per_hour=MEAN_MOON_DEG_PER_HOUR
        )
        self.assertGreater(raw, 3.0)
        self.assertLess(raw, 4.0)
        self.assertEqual(event_window_half_width_days("Sun"), 4)

    def test_uses_birth_nakshatra_lord_not_event_dasha(self):
        # Venus birth balance ⇒ Venus-span window even if we later score a Sun-MD event
        birth_lord_window = event_window_half_width_days("Venus")
        self.assertEqual(birth_lord_window, MEAN_MOON_WINDOW_TABLE["Venus"])
        self.assertNotEqual(birth_lord_window, MEAN_MOON_WINDOW_TABLE["Sun"])

    def test_faster_moon_widens_window(self):
        mean_w = event_window_half_width_days("Venus", moon_deg_per_hour=0.55)
        fast_w = event_window_half_width_days("Venus", moon_deg_per_hour=0.64)
        self.assertGreater(fast_w, mean_w)
        self.assertGreaterEqual(fast_w, 12)

    def test_window_from_natal_uses_ephemeris_moon_speed(self):
        natal = compute_natal_chart(1999, 4, 24, 7, 0, 0, 26.4652, 80.3498)
        moon = natal["planets"]["Moon"]
        self.assertIn("speed_deg_per_hour", moon)
        w = event_window_half_width_from_natal(natal)
        expected = event_window_half_width_days(
            moon["nakshatra"]["lord"],
            moon_deg_per_hour=moon["speed_deg_per_hour"],
        )
        self.assertEqual(w, expected)

    def test_boundary_shift_scales_with_lord_years(self):
        shifts = {
            lord: dasha_boundary_shift_days_per_minute(lord)
            for lord, _ in DASHA_ORDER
        }
        self.assertAlmostEqual(
            shifts["Venus"] / shifts["Sun"],
            DASHA_MAP["Venus"] / DASHA_MAP["Sun"],
            places=5,
        )


class TestJagannathaHoraGoldenMaster(unittest.TestCase):
    FIXTURE = Path(__file__).parent / "fixtures" / "jh_vimshottari_golden.json"

    def _load(self):
        return json.loads(self.FIXTURE.read_text(encoding="utf-8"))

    def test_jh_golden_master(self):
        data = self._load()
        freeze_run = os.environ.get("KL_N30_FREEZE_RUN") == "1"
        charts = data.get("charts", [])
        min_charts = int(data.get("min_charts_required", 4))
        populated = bool(data.get("populated")) and len(charts) >= min_charts

        if not populated:
            msg = (
                "JH golden-master fixture empty or incomplete. Export 4–5 charts "
                "from Jagannatha Hora (365.25 year, Lahiri, true node, explicit UTC) "
                "into tests/fixtures/jh_vimshottari_golden.json"
            )
            if freeze_run:
                self.fail(
                    f"KL_N30_FREEZE_RUN=1 but golden-master not ready: {msg}"
                )
            self.skipTest(msg)

        self.assertEqual(data["settings"]["dasha_year_days"], 365.25)
        tolerance = float(data.get("tolerance_days", 1))
        lords = {c["moon_nakshatra_lord"].title() for c in charts}
        self.assertTrue(lords & {"Venus", "Saturn"}, "need ≥1 long-lord birth Moon")
        self.assertTrue(lords & {"Sun", "Ketu"}, "need ≥1 short-lord birth Moon")

        for chart in charts:
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
                    got_start, got_end = antar["start_date"], antar["end_date"]
                else:
                    got_start, got_end = maha["start_date"], maha["end_date"]

                for label, got, exp in (
                    ("start", got_start, expected["start_date"]),
                    ("end", got_end, expected["end_date"]),
                ):
                    delta = abs(
                        (
                            datetime.strptime(got, "%Y-%m-%d")
                            - datetime.strptime(exp, "%Y-%m-%d")
                        ).days
                    )
                    self.assertLessEqual(
                        delta,
                        tolerance,
                        msg=(
                            f"{chart.get('id', '?')} {expected} {label}: "
                            f"engine={got} jh={exp} delta={delta}d > {tolerance}d"
                        ),
                    )


if __name__ == "__main__":
    unittest.main()
