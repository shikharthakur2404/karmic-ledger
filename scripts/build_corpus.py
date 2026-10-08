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
SOURCES_DIR = ROOT / "corpus" / "sources"

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


def _is_chapter_header(line: str) -> int | None:
    """Return chapter number if this line opens an adhyāya; else None."""
    if "||" not in line:
        return None
    low = line.lower()
    if "\\section{" in line or "adhyaya" in low or "adhyAya" in line:
        m = re.search(r"\|\|\s*(\d+)\s*\|\|", line)
        if m:
            return int(m.group(1))
    # Older packs: "atha ... || 21||" without the word adhyAya on every title
    if re.match(r"^atha\b", low) and re.search(r"\|\|\s*\d+\s*\|\|\s*$", line):
        m = re.search(r"\|\|\s*(\d+)\s*\|\|", line)
        if m:
            num = int(m.group(1))
            # Chapter titles use larger numbers; skip tiny mangala verses
            if num >= 1:
                return num
    return None


def parse_bphs_itx(path: Path) -> list[dict]:
    """Extract chapter/verse units from Sanskrit Documents ITRANS file.

    Supports both \\section{... || N||} packs and plain `atha ... || N||` titles,
    including multi-line verses that only close on the final || n||.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    body = text.split(r"\begin{document}", 1)[-1]
    source_tag = path.stem
    rows: list[dict] = []
    chapter = 0
    buf: list[str] = []

    for raw in body.splitlines():
        line = raw.strip()
        if not line:
            continue
        # Skip TeX noise (keep \\section lines for chapter detection)
        if line.startswith("\\") and "\\section{" not in line:
            continue
        if line.startswith("%") or line.startswith("#"):
            continue

        ch = _is_chapter_header(line)
        if ch is not None and (
            "\\section{" in line
            or "adhyAya" in line
            or "adhyaya" in line.lower()
            or re.match(r"^atha\b", line, re.I)
        ):
            # Prefer title lines; avoid treating verse ||21|| as a chapter when
            # already inside a chapter unless it looks like a title.
            if (
                "\\section{" in line
                or "adhyAya" in line
                or "adhyaya" in line.lower()
                or (
                    re.match(r"^atha\b", line, re.I)
                    and ("adhyAya" in line or "adhyaya" in line.lower() or len(line) < 80)
                )
            ):
                chapter = ch
                buf = []
                continue

        if chapter <= 0:
            continue

        buf.append(line)
        joined = " ".join(buf)
        vm = re.search(r"^(.*?)\s*\|\|\s*(\d+)\s*\|\|\s*$", joined)
        if not vm:
            # Keep buffering; verses often span two lines
            if len(buf) > 6:
                buf = buf[-3:]
            continue

        sanskrit = " ".join(vm.group(1).split())
        verse = int(vm.group(2))
        buf = []
        if len(sanskrit) < 8:
            continue
        # Skip mangala / colophon-ish repeats that reuse chapter numbers as verse 0
        rows.append(
            {
                "rule_id": f"bphs_sd:{source_tag}:ch{chapter:02d}:v{verse:03d}",
                "text_name": "Brihat Parashara Hora Shastra",
                "chapter": chapter,
                "verse": verse,
                "citation": f"BPHS {chapter}:{verse} ({source_tag})",
                "provenance": "CLASSICAL",
                "edition": f"sanskritdocuments.org {path.name} (ITRANS; study use)",
                "sanskrit": sanskrit,
                "translation": "",
                "keywords": f"bphs chapter_{chapter} verse_{verse} parashara {source_tag}",
            }
        )
    return rows


def ingest_all_itx(conn: sqlite3.Connection) -> int:
    total = 0
    for path in sorted(SOURCES_DIR.glob("*.itx")):
        rows = parse_bphs_itx(path)
        for row in rows:
            _insert(conn, row)
        print(f"  {path.name}: {len(rows)} verses")
        total += len(rows)
    return total


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
        print("engine citations:", n1)
        n2 = ingest_all_itx(conn)
        rebuild_fts(conn)
        conn.commit()
        total = conn.execute("SELECT COUNT(*) FROM rules").fetchone()[0]
        print(f"built {DB_PATH}")
        print(f"  total rules: {total} (engine {n1} + itx {n2})")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
