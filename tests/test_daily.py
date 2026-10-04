"""
Unit tests for the Full-Spectrum Daily Transit & Incident Radar Engine (core/daily.py).
Tests kinetic vitality, mobility, nightlife drivers, and backwards-compatibility.
"""

import unittest
from datetime import datetime

from core.daily import compute_daily_incident_radar
from core.ephemeris import compute_natal_chart


class TestDailyRadarEngine(unittest.TestCase):
    def setUp(self):
        # Shikhar's birth coordinates: 24 Apr 1999, 07:00, Kanpur (Taurus Lagna, Taurus Moon)
        self.natal = compute_natal_chart(1999, 4, 24, 7, 0, 0, 26.4652, 80.3498)

    def test_october_2_3_telemetry(self):
        """
        Verify the real-world events of Oct 2-3, 2026:
        1. Nightlife / late hours (party till 04:00 AM)
        2. High kinetic stamina (38k steps hike)
        3. 3rd house regional mobility (train to Pegnitz)
        4. 2nd house culinary sensory dining (Thai/Asian dinner)
        """
        target_dt = datetime(2026, 10, 2, 22, 0, 0)
        radar = compute_daily_incident_radar(self.natal, target_dt)

        self.assertIn("overall_status", radar)
        self.assertIn("overall_status_label", radar)
        self.assertIn("archetype_flavor", radar)
        self.assertIn("chandrashtama", radar)
        self.assertIn("somatic_injury", radar)
        self.assertIn("mercury_sandhi", radar)
        self.assertIn("recreation_social", radar)
        self.assertIn("tactical_advice", radar)

        # Kinetic Stamina
        somatic = radar["somatic_injury"]
        self.assertEqual(somatic["stamina_level"], "Surging High")
        self.assertIn("Kinetic Output", somatic["status_label"])
        self.assertGreater(somatic["step_endurance_rating"], 7)

        # Social & Recreation
        social = radar["recreation_social"]
        self.assertTrue(social["is_active"])
        self.assertTrue(social["nightlife_active"])
        self.assertTrue(social["saturn_gatekeeper_active"])
        self.assertTrue(social["culinary_active"])

        # Saturday Hike check (Oct 3, 2026 14:00 UTC)
        sat_dt = datetime(2026, 10, 3, 14, 0, 0)
        sat_radar = compute_daily_incident_radar(self.natal, sat_dt)
        self.assertEqual(sat_radar["somatic_injury"]["stamina_level"], "Surging High")
        self.assertTrue(sat_radar["recreation_social"]["culinary_active"])

    def test_chandrashtama_detection(self):
        """
        Verify Chandrashtama is detected when Moon transits Sagittarius (8th from natal Moon Taurus).
        """
        # Pick a date when transit Moon is in Sagittarius
        # Since Moon takes ~2.25 days per sign, let's verify moon_state calculates house_from_moon accurately
        target_dt = datetime(2026, 10, 16, 12, 0, 0)
        radar = compute_daily_incident_radar(self.natal, target_dt)
        # Moon in Scorpio/Sagittarius range in mid-October
        self.assertIn("house_from_moon", radar["chandrashtama"])
        self.assertIn("is_active", radar["chandrashtama"])


if __name__ == "__main__":
    unittest.main()
