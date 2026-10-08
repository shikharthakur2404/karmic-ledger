"""KL-N30-001 domain map + freeze scaffolding."""

from __future__ import annotations

import unittest

from studies.kl_n30_001.domain_map import EVENT_TYPES, map_event_domain
from studies.kl_n30_001.score_heldout import STUDY_ID, VCS_PROFILE
from core.dasha import DASHA_YEAR_DAYS


class TestKlN30DomainMap(unittest.TestCase):
    def test_all_event_types_map(self):
        for et in EVENT_TYPES:
            domain = map_event_domain(et)
            self.assertTrue(domain)

    def test_unknown_raises(self):
        with self.assertRaises(ValueError):
            map_event_domain("ENGAGEMENT")

    def test_score_pins(self):
        self.assertEqual(STUDY_ID, "KL-N30-001")
        self.assertEqual(VCS_PROFILE, "kl_n30_001")
        self.assertEqual(DASHA_YEAR_DAYS, 365.25)


if __name__ == "__main__":
    unittest.main()
