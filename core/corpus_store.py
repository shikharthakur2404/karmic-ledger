"""
Local śāstra / natal-rule corpus backed by SQLite FTS5.

Fast keyword fetch for Kundli engines — no PDF parsing at request time.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "corpus" / "db" / "shastra.fts.sqlite"


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or DEFAULT_DB
    if not path.exists():
        raise FileNotFoundError(
            f"Corpus DB missing at {path}. Run: python3 scripts/build_corpus.py"
        )
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn


def search_corpus(
    query: str,
    *,
    limit: int = 20,
    db_path: Path | None = None,
) -> list[dict[str, Any]]:
    """Full-text search over Sanskrit, translation, keywords, and citation."""
    q = (query or "").strip()
    if not q:
        return []
    conn = connect(db_path)
    try:
        # FTS5: simple token query; escape quotes
        safe = q.replace('"', " ").replace("'", " ")
        rows = conn.execute(
            """
            SELECT rule_id, text_name, chapter, verse, citation, provenance,
                   sanskrit, translation, keywords, rank
            FROM rules_fts
            WHERE rules_fts MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (safe, limit),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_rule(rule_id: str, db_path: Path | None = None) -> dict[str, Any] | None:
    conn = connect(db_path)
    try:
        row = conn.execute(
            """
            SELECT rule_id, text_name, chapter, verse, citation, provenance,
                   edition, sanskrit, translation, keywords
            FROM rules
            WHERE rule_id = ?
            """,
            (rule_id,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_rules_by_ids(
    rule_ids: list[str],
    *,
    db_path: Path | None = None,
) -> list[dict[str, Any]]:
    """Fetch rule rows preserving the order of rule_ids."""
    if not rule_ids:
        return []
    conn = connect(db_path)
    try:
        placeholders = ",".join("?" for _ in rule_ids)
        rows = conn.execute(
            f"""
            SELECT rule_id, text_name, chapter, verse, citation, provenance,
                   sanskrit, translation, keywords
            FROM rules
            WHERE rule_id IN ({placeholders})
            """,
            rule_ids,
        ).fetchall()
        by_id = {r["rule_id"]: dict(r) for r in rows}
        return [by_id[rid] for rid in rule_ids if rid in by_id]
    finally:
        conn.close()


def semantic_search(
    query: str,
    *,
    limit: int = 20,
    db_path: Path | None = None,
) -> list[dict[str, Any]]:
    """Lane B: TF–IDF cosine search over the vector index."""
    from core.vector_index import get_vector_index

    q = (query or "").strip()
    if not q:
        return []
    index = get_vector_index()
    if index is None:
        return []
    ranked = index.search(q, limit=limit)
    if not ranked:
        return []
    rows = get_rules_by_ids([rid for rid, _ in ranked], db_path=db_path)
    score_map = {rid: score for rid, score in ranked}
    for row in rows:
        row["rank"] = -float(score_map.get(row["rule_id"], 0.0))
        row["vector_score"] = float(score_map.get(row["rule_id"], 0.0))
    return rows
