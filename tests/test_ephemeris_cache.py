"""Ephemeris LRU cache smoke tests."""

from __future__ import annotations

import unittest

from core.ephemeris import clear_ephemeris_cache, compute_natal_chart


class TestEphemerisCache(unittest.TestCase):
    def setUp(self):
        clear_ephemeris_cache()

    def test_repeated_call_is_stable(self):
        a = compute_natal_chart(1999, 4, 24, 7, 0, 0, 26.4652, 80.3498)
        b = compute_natal_chart(1999, 4, 24, 7, 0, 0, 26.4652, 80.3498)
        self.assertEqual(a["lagna"]["sign"], b["lagna"]["sign"])
        self.assertEqual(
            a["planets"]["Moon"]["nakshatra"]["lord"],
            b["planets"]["Moon"]["nakshatra"]["lord"],
        )

    def test_caller_mutation_does_not_poison_cache(self):
        a = compute_natal_chart(1999, 4, 24, 7, 0, 0, 26.4652, 80.3498)
        a["planets"]["Moon"]["sign"] = "MUTATED"
        b = compute_natal_chart(1999, 4, 24, 7, 0, 0, 26.4652, 80.3498)
        self.assertNotEqual(b["planets"]["Moon"]["sign"], "MUTATED")


if __name__ == "__main__":
    unittest.main()
