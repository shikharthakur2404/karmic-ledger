#!/usr/bin/env python3
"""Build corpus/db/shastra.fts.sqlite from core/shastra.py + corpus/sources/*.itx."""

from __future__ import annotations

import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.shastra import SHASTRA_DATABASE  # noqa: E402

DB_PATH = ROOT / "corpus" / "db" / "shastra.fts.sqlite"
ITX_PATH = ROOT / "corpus" / "sources" / "bphs_01_10.itx"

SCHEMA = """
DROP TABLE IF EXISTS rules_fts;
DROP TABLE IF EXISTS rules;

CREATE TABLE rules (
  rule_id TEXT PRIMARY KEY,
  text_name TEXT NOT NULL,
  chapter INTEGER,
  verse INTEGER,
  citation TEXT,
  provenance TEXT NOT NULL,
  edition TEXT,
  sanskrit TEXT,
  translation TEXT,
  keywords TEXT
);

CREATE VIRTUAL TABLE rules_fts USING fts5(
  rule_id UNINDEXED,
  text_name,
  chapter UNINDEXED,
  verse UNINDEXED,
  citation,
  provenance UNINDEXED,
  sanskrit,
  translation,
  keywords,
  content='rules',
  content_rowid='rowid'
);
"""


def _insert(conn: sqlite3.Connection, row: dict) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO rules (
          rule_id, text_name, chapter, verse, citation, provenance,
          edition, sanskrit, translation, keywords
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            row["rule_id"],
            row["text_name"],
            row.get("chapter"),
            row.get("verse"),
            row.get("citation"),
            row["provenance"],
            row.get("edition"),
            row.get("sanskrit") or "",
            row.get("translation") or "",
            row.get("keywords") or "",
        ),
    )


def ingest_engine_citations(conn: sqlite3.Connection) -> int:
    n = 0
    for key, entry in SHASTRA_DATABASE.items():
        _insert(
            conn,
            {
                "rule_id": f"engine:{key}",
                "text_name": entry["text"],
                "chapter": entry.get("chapter"),
                "verse": entry.get("verse"),
                "citation": entry.get("citation"),
                "provenance": "MODERN_PRACTITIONER",
                "edition": "unpinned — verify before study freeze",
                "sanskrit": entry.get("sanskrit", ""),
                "translation": entry.get("translation", ""),
                "keywords": " ".join(entry.get("keywords") or []),
            },
        )
        n += 1
    return n


def parse_bphs_itx(path: Path) -> list[dict]:
    """Extract chapter/verse units from Sanskrit Documents ITRANS file."""
    text = path.read_text(encoding="utf-8", errors="replace")
    # Strip TeX preamble noise lightly
    body = text.split(r"\begin{document}", 1)[-1]
    chapter = 0
    rows: list[dict] = []
    # section lines mark chapters; verse lines end with || N||
    section_re = re.compile(r"\\section\{[^}]*\|\|\s*(\d+)\s*\|\|")
    verse_re = re.compile(
        r"^(.+?)\s*\|\|\s*(\d+)\s*\|\|\s*$", re.MULTILINE
    )

    pos = 0
    for sec in section_re.finditer(body):
        chapter = int(sec.group(1))
        # verses until next section or end
        start = sec.end()
        nxt = section_re.search(body, start)
        chunk = body[start : nxt.start() if nxt else len(body)]
        for vm in verse_re.finditer(chunk):
            sanskrit = " ".join(vm.group(1).split())
            verse = int(vm.group(2))
            if len(sanskrit) < 8:
                continue
            rows.append(
                {
                    "rule_id": f"bphs_sd:ch{chapter:02d}:v{verse:03d}",
                    "text_name": "Brihat Parashara Hora Shastra",
                    "chapter": chapter,
                    "verse": verse,
                    "citation": f"BPHS {chapter}:{verse} (sanskritdocuments par0110)",
                    "provenance": "CLASSICAL",
                    "edition": "sanskritdocuments.org par0110.itx (ITRANS; study use)",
                    "sanskrit": sanskrit,
                    "translation": "",
                    "keywords": f"bphs chapter_{chapter} verse_{verse} parashara",
                }
            )
        pos = start
    _ = pos
    return rows


def ingest_itx(conn: sqlite3.Connection) -> int:
    if not ITX_PATH.exists():
        print(f"skip missing {ITX_PATH}")
        return 0
    rows = parse_bphs_itx(ITX_PATH)
    for row in rows:
        _insert(conn, row)
    return len(rows)


def rebuild_fts(conn: sqlite3.Connection) -> None:
    conn.execute("INSERT INTO rules_fts(rules_fts) VALUES('rebuild')")


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(str(DB_PATH))
    try:
        conn.executescript(SCHEMA)
        n1 = ingest_engine_citations(conn)
        n2 = ingest_itx(conn)
        rebuild_fts(conn)
        conn.commit()
        total = conn.execute("SELECT COUNT(*) FROM rules").fetchone()[0]
        print(f"built {DB_PATH}")
        print(f"  engine citations: {n1}")
        print(f"  BPHS ITX verses:  {n2}")
        print(f"  total rules:      {total}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
