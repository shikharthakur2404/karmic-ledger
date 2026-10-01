"""
Unit tests for Engine 11: Saṃskāra & Karmic Trace Engine (Karma-Trace v1.0.0).
Zero external dependencies; fully executable via standard library unittest.
"""

import json
import unittest

from core.ephemeris import compute_natal_chart
from core.samskara import (
    compute_drekkana_loka,
    evaluate_purva_punya_houses,
    generate_samskara_report,
    profile_samskara_latent_impressions,
)
from server import SamskaraAnalysisRequest, analyze_samskara_trace, get_samskara_profile


class TestSamskaraEngine(unittest.TestCase):
    def setUp(self):
        # Shikhar's birth coordinates: 24 Apr 1999, 07:00, Kanpur
        self.natal = compute_natal_chart(1999, 4, 24, 7, 0, 0, 26.4652, 80.3498)

    def test_drekkana_loka_calculation(self):
        loka_report = compute_drekkana_loka(self.natal)

        self.assertIn("stronger_luminary", loka_report)
        self.assertIn(loka_report["stronger_luminary"], ("Sun", "Moon"))
        self.assertIn("purva_janma_loka", loka_report)
        self.assertIn("drekkana_lord", loka_report)
        self.assertIn(loka_report["decanate"], (1, 2, 3))
        self.assertIn("BPHS", loka_report["citation"])
        # For Shikhar: Sun is stronger (Exalted in Aries 9.60°, Decanate 1 = Aries, Lord Mars -> Mṛtyuloka / Tiryagloka)
        self.assertEqual(loka_report["stronger_luminary"], "Sun")
        self.assertEqual(loka_report["drekkana_lord"], "Mars")
        self.assertIn("Mṛtyuloka", loka_report["purva_janma_loka"])

    def test_purva_punya_houses(self):
        purva = evaluate_purva_punya_houses(self.natal)

        self.assertIn("house_5", purva)
        self.assertIn("house_9", purva)
        self.assertIn("house_12", purva)
        # Taurus Lagna: H5=Virgo, H9=Capricorn, H12=Aries
        self.assertEqual(purva["house_5"]["sign"], "Virgo")
        self.assertEqual(purva["house_9"]["sign"], "Capricorn")
        self.assertEqual(purva["house_12"]["sign"], "Aries")
        self.assertIn("Ketu", purva["house_9"]["occupants"])

    def test_samskara_latent_impressions_profiler(self):
        features = {
            "affinities": [
                "System Architecture & Engineering",
                "Classical Metaphysics",
                "DACH Geography",
            ],
            "fears_or_sensitivities": ["Cold Ambient Temperature"],
            "spontaneous_talents": [
                "High Psychological Endurance",
                "Rapid Complex System Synthesis",
            ],
        }
        profile = profile_samskara_latent_impressions(features)

        self.assertIn("dominant_samskara_archetype", profile)
        self.assertIn("vector_scores", profile)
        self.assertIn("YS 3.18", profile["sutra_reference"])
        self.assertEqual(
            profile["dominant_samskara_archetype"],
            "Jnāna-Mārga (The Scholar-Architect)",
        )

    def test_epistemic_safety_boundaries(self):
        report = generate_samskara_report(self.natal)
        epistemic = report["epistemic_status"]

        self.assertTrue(epistemic["traditional_interpretation"])
        self.assertFalse(epistemic["empirical_confirmation"])
        self.assertFalse(epistemic["literal_identity_claimed"])
        self.assertEqual(
            epistemic["scientific_classification"], "RESEARCH_PHENOMENOLOGY_ONLY"
        )
        self.assertIn(
            "verifiable historical identity",
            report["epistemic_status"]["epistemic_notice"],
        )

    def test_api_handlers_direct(self):
        # 1. Test profile GET handler
        res_prof = get_samskara_profile("shikhar")
        data_prof = json.loads(res_prof.body.decode("utf-8"))
        self.assertEqual(data_prof["engine_id"], "11")
        self.assertIn("path_a_jyotisha", data_prof)
        self.assertIn("path_b_samskara", data_prof)
        self.assertIn("shastric_citations", data_prof)

        # 2. Test analyze POST handler
        req = SamskaraAnalysisRequest(
            name="Test Querent",
            date="1999-04-24",
            time="07:00:00",
            latitude=26.4652,
            longitude=80.3498,
            affinities=["Systems Engineering", "Sanskrit"],
            fears_or_sensitivities=["Cold"],
            spontaneous_talents=["Focus"],
        )
        res_post = analyze_samskara_trace(req)
        data_post = json.loads(res_post.body.decode("utf-8"))
        self.assertEqual(data_post["subject"], "Test Querent")
        self.assertEqual(data_post["engine_id"], "11")


if __name__ == "__main__":
    unittest.main()
