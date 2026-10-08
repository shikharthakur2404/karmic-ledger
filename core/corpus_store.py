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
