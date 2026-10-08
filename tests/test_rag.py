"""Tests for grounded śāstra RAG (retrieve → card, no invented verses)."""

from __future__ import annotations

import unittest

from core.rag import generate_shastra_rag_card, synthesize_offline_card


class TestShastraRag(unittest.TestCase):
    def test_retrieval_card_has_hits(self):
        out = generate_shastra_rag_card("maitreya OR marriage", limit=5, allow_llm=False)
        self.assertGreater(out["hit_count"], 0)
        self.assertEqual(out["grounding"], "retrieval_only")
        self.assertEqual(out["engine_source"], "offline_retrieval_card")
        self.assertIn("Retrieved", out["card"])
        for hit in out["hits"]:
            self.assertTrue(hit.get("citation") or hit.get("rule_id"))

    def test_empty_retrieval_does_not_invent(self):
        out = generate_shastra_rag_card(
            "zzzxqnonexistentverse999", limit=3, allow_llm=False
        )
        self.assertEqual(out["hit_count"], 0)
        self.assertIn("will not invent", out["card"].lower())

    def test_offline_card_lists_citations(self):
        hits = [
            {
                "citation": "BPHS 1:1",
                "provenance": "CLASSICAL",
                "sanskrit": "athaikadA...",
                "translation": "",
            }
        ]
        card = synthesize_offline_card("test", hits)
        self.assertIn("BPHS 1:1", card)
        self.assertIn("no English translation pinned", card)


if __name__ == "__main__":
    unittest.main()
