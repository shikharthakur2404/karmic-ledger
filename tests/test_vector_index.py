"""Lane B TF–IDF vector index + hybrid retrieval."""

from __future__ import annotations

import os
import unittest
from pathlib import Path

from core.corpus_store import semantic_search
from core.rag import retrieve_rules, shastra_query_from_chart
from core.vector_index import DEFAULT_VECTORS, build_vector_index, get_vector_index


class TestVectorIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not DEFAULT_VECTORS.exists():
            build_vector_index()

    def test_index_loads_and_searches(self):
        idx = get_vector_index()
        self.assertIsNotNone(idx)
        assert idx is not None
        hits = idx.search("marriage venus kalatra", limit=5)
        self.assertGreater(len(hits), 0)
        self.assertTrue(all(score > 0 for _, score in hits))

    def test_semantic_search_returns_rows(self):
        rows = semantic_search("maitreya", limit=3)
        self.assertGreater(len(rows), 0)
        self.assertIn("rule_id", rows[0])
        self.assertIn("vector_score", rows[0])

    def test_hybrid_retrieve(self):
        os.environ["CORPUS_RETRIEVAL"] = "hybrid"
        try:
            hits = retrieve_rules("maitreya OR marriage", limit=5)
            self.assertGreater(len(hits), 0)
        finally:
            os.environ.pop("CORPUS_RETRIEVAL", None)

    def test_shastra_query_from_chart(self):
        natal = {
            "planets": {"Moon": {"nakshatra": {"lord": "Venus"}}},
        }
        q = shastra_query_from_chart(
            natal,
            active_dasha={"mahadasha": "Jupiter", "antardasha": "Saturn"},
            soul_telemetry={"atmakaraka_planet": "Mars"},
        )
        self.assertIn("Jupiter", q)
        self.assertIn("Venus", q)
        self.assertIn(" OR ", q)


if __name__ == "__main__":
    unittest.main()
