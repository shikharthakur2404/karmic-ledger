"""Demo 404 guard + Lagna cusp warning."""

from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from core.ephemeris import compute_natal_chart, lagna_boundary_warning
from server import app


class TestDemoGuard(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_unknown_demo_is_404(self):
        res = self.client.get("/api/demo/hemant")
        self.assertEqual(res.status_code, 404)
        body = res.json()
        detail = body.get("detail") or ""
        self.assertIn("not found", detail.lower())

    def test_known_demo_ok(self):
        res = self.client.get("/api/demo/soham")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Soham", res.json().get("subject", ""))


class TestLagnaBoundary(unittest.TestCase):
    def test_hemant_edge_warns(self):
        # ~05:00 Aurangabad → Aquarius ~0.6° (cusp edge)
        natal = compute_natal_chart(2000, 3, 16, 5, 0, 0, 19.8762, 75.3433)
        warn = lagna_boundary_warning(natal)
        self.assertIsNotNone(warn)
        assert warn is not None
        self.assertEqual(warn["level"], "cusp_edge")

    def test_unknown_time_warns(self):
        natal = compute_natal_chart(2000, 3, 16, 12, 0, 0, 19.8762, 75.3433)
        warn = lagna_boundary_warning(natal, birth_time_unknown=True)
        self.assertIsNotNone(warn)
        assert warn is not None
        self.assertEqual(warn["level"], "unknown_time")


if __name__ == "__main__":
    unittest.main()
