"""
Retrieval-Augmented Generation for śāstra cards.

Pipeline: hybrid retrieve (FTS + TF–IDF vectors) → grounded plain-language card.
The generator may only paraphrase retrieved rows. It never invents verses,
citations, or Sanskrit. If retrieval is empty, the card says so explicitly.
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from typing import Any

from core.corpus_store import search_corpus, semantic_search
from core.vector_index import retrieval_mode


def _rrf_merge(
    fts_hits: list[dict[str, Any]],
    vec_hits: list[dict[str, Any]],
    *,
    limit: int,
    k: int = 60,
) -> list[dict[str, Any]]:
    """Reciprocal rank fusion over FTS and vector result lists."""
    scores: dict[str, float] = {}
    by_id: dict[str, dict[str, Any]] = {}
    for rank, hit in enumerate(fts_hits):
        rid = hit.get("rule_id")
        if not rid:
            continue
        scores[rid] = scores.get(rid, 0.0) + 1.0 / (k + rank + 1)
        by_id[rid] = hit
    for rank, hit in enumerate(vec_hits):
        rid = hit.get("rule_id")
        if not rid:
            continue
        scores[rid] = scores.get(rid, 0.0) + 1.0 / (k + rank + 1)
        by_id.setdefault(rid, hit)
    ordered = sorted(scores.items(), key=lambda kv: -kv[1])
    out: list[dict[str, Any]] = []
    for rid, score in ordered[:limit]:
        row = dict(by_id[rid])
        row["hybrid_score"] = score
        out.append(row)
    return out


def retrieve_rules(query: str, *, limit: int = 5) -> list[dict[str, Any]]:
    """Retrieve ranked rules (FTS, vector, or hybrid — see CORPUS_RETRIEVAL)."""
    q = (query or "").strip()
    if not q:
        return []
    mode = retrieval_mode()
    fetch_n = max(limit * 3, 12)
    fts_hits: list[dict[str, Any]] = []
    vec_hits: list[dict[str, Any]] = []
    try:
        if mode in {"fts", "hybrid"}:
            fts_hits = search_corpus(q, limit=fetch_n)
    except FileNotFoundError:
        fts_hits = []
    try:
        if mode in {"vector", "hybrid"}:
            vec_hits = semantic_search(q, limit=fetch_n)
    except FileNotFoundError:
        vec_hits = []

    if mode == "fts":
        return fts_hits[:limit]
    if mode == "vector":
        return vec_hits[:limit] if vec_hits else fts_hits[:limit]
    if not vec_hits:
        return fts_hits[:limit]
    if not fts_hits:
        return vec_hits[:limit]
    return _rrf_merge(fts_hits, vec_hits, limit=limit)


def shastra_query_from_chart(
    natal: dict[str, Any],
    active_dasha: dict[str, Any] | None = None,
    soul_telemetry: dict[str, Any] | None = None,
    intimacy_telemetry: dict[str, Any] | None = None,
) -> str:
    """Build a grounded FTS/hybrid query from chart context (server + UI seed)."""
    parts: list[str] = []
    if active_dasha:
        for key in ("mahadasha", "antardasha"):
            lord = str(active_dasha.get(key) or "").strip()
            if lord and lord.lower() not in {"none", "n/a"}:
                parts.append(lord.split()[0])
    moon = (natal or {}).get("planets", {}).get("Moon", {})
    moon_lord = (moon.get("nakshatra") or {}).get("lord")
    if moon_lord:
        parts.append(str(moon_lord))
    if soul_telemetry:
        ak = soul_telemetry.get("atmakaraka_planet") or soul_telemetry.get(
            "atmakaraka"
        )
        if ak:
            parts.append(str(ak))
    if intimacy_telemetry and intimacy_telemetry.get("status") == "OK":
        seed = intimacy_telemetry.get("rag_seed") or ""
        for tok in re.split(r"\s+OR\s+|[,\s]+", seed, flags=re.I):
            tok = tok.strip()
            if tok:
                parts.append(tok)
    uniq: list[str] = []
    seen: set[str] = set()
    for p in parts:
        key = p.lower()
        if key in seen or len(key) < 2:
            continue
        seen.add(key)
        uniq.append(p)
        if len(uniq) >= 5:
            break
    return " OR ".join(uniq)


def synthesize_offline_card(query: str, hits: list[dict[str, Any]]) -> str:
    """Deterministic grounded card — no model required."""
    if not hits:
        return (
            f'No pinned verse matched “{query}”. '
            "The engine will not invent a shloka. "
            "Try another keyword, or expand the corpus (python3 scripts/build_corpus.py)."
        )

    lines = [
        f"Query: {query}",
        f"Retrieved {len(hits)} pinned rule(s). Summary uses only these rows:",
        "",
    ]
    for i, h in enumerate(hits, 1):
        citation = h.get("citation") or h.get("rule_id") or "unspecified"
        provenance = h.get("provenance") or "UNTAGGED"
        sanskrit = (h.get("sanskrit") or "").strip()
        translation = (h.get("translation") or "").strip()
        lines.append(f"{i}. {citation}  [{provenance}]")
        if sanskrit:
            lines.append(f"   Sanskrit: {sanskrit}")
        if translation:
            lines.append(f"   Meaning: {translation}")
        else:
            lines.append(
                "   Meaning: (no English translation pinned yet — Sanskrit only)"
            )
        lines.append("")
    lines.append(
        "Note: This is classical / corpus text for reflection, not medical or legal advice."
    )
    return "\n".join(lines)


def _gemini_grounded_rewrite(query: str, hits: list[dict[str, Any]]) -> str | None:
    """Optional Gemini pass. Returns None if unavailable or unsafe to call."""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key or not hits:
        return None

    payload_hits = [
        {
            "citation": h.get("citation"),
            "provenance": h.get("provenance"),
            "sanskrit": h.get("sanskrit"),
            "translation": h.get("translation"),
        }
        for h in hits
    ]
    prompt = f"""You rewrite retrieved Jyotish/śāstra rows into a short plain-English card.

HARD RULES:
- Use ONLY the JSON rows below. Do not add verses, citations, or Sanskrit not present.
- If a row has empty translation, say so; do not invent one.
- Do not claim fate, medicine, or certainty.
- Keep under 180 words.
- End with a bullet list of citations used.

User query: {query}

Retrieved rows (JSON):
{json.dumps(payload_hits, ensure_ascii=False, indent=2)}
"""
    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.5-flash:generateContent?key={api_key}"
    )
    body = json.dumps(
        {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.1, "maxOutputTokens": 512},
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            parts = (
                res_data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])
            )
            text = parts[0].get("text", "") if parts else ""
            return text.strip() or None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError):
        return None


def generate_shastra_rag_card(
    query: str,
    *,
    limit: int = 5,
    allow_llm: bool = True,
) -> dict[str, Any]:
    """
    Full RAG slice: retrieve → grounded card (+ optional LLM paraphrase).
    """
    q = (query or "").strip()
    hits = retrieve_rules(q, limit=limit) if q else []
    offline = synthesize_offline_card(q or "(empty)", hits)
    engine = "offline_retrieval_card"
    api_status = "NOT_USED"
    card = offline

    if allow_llm and hits:
        rewritten = _gemini_grounded_rewrite(q, hits)
        if rewritten:
            card = rewritten
            engine = "gemini_grounded_paraphrase"
            api_status = "ONLINE_LIVE"
        else:
            api_status = "OFFLINE_OR_UNAVAILABLE"

    return {
        "query": q,
        "hit_count": len(hits),
        "hits": [
            {
                "rule_id": h.get("rule_id"),
                "citation": h.get("citation"),
                "provenance": h.get("provenance"),
                "sanskrit": h.get("sanskrit"),
                "translation": h.get("translation"),
            }
            for h in hits
        ],
        "card": card,
        "engine_source": engine,
        "api_key_status": api_status,
        "grounding": "retrieval_only",
        "retrieval_mode": retrieval_mode(),
    }
