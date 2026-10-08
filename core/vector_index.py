"""
Lane B: offline TF–IDF vector index over the śāstra corpus.

No neural embeddings, no network. Built by scripts/build_corpus.py into
corpus/db/shastra.vectors.npz. Used by hybrid retrieval in core/rag.py.
"""

from __future__ import annotations

import math
import os
import re
import sqlite3
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "corpus" / "db" / "shastra.fts.sqlite"
DEFAULT_VECTORS = ROOT / "corpus" / "db" / "shastra.vectors.npz"

_TOKEN_RE = re.compile(r"[a-z0-9_]+|[^\W\d_]+", re.UNICODE)
_MAX_VOCAB = 8000
_MIN_DF = 2


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text or "") if len(t) > 1]


def _doc_text(row: sqlite3.Row | dict[str, Any]) -> str:
    parts = [
        str(row["citation"] or ""),
        str(row["keywords"] or ""),
        str(row["translation"] or ""),
        str(row["sanskrit"] or "")[:400],
        str(row["text_name"] or ""),
    ]
    return " ".join(parts)


def build_vector_index(
    db_path: Path | None = None,
    out_path: Path | None = None,
    *,
    max_vocab: int = _MAX_VOCAB,
    min_df: int = _MIN_DF,
) -> dict[str, Any]:
    """Fit TF–IDF on all rules and write .npz. Returns build stats."""
    db = db_path or DEFAULT_DB
    out = out_path or DEFAULT_VECTORS
    if not db.exists():
        raise FileNotFoundError(f"Corpus DB missing at {db}")

    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT rule_id, text_name, citation, sanskrit, translation, keywords
            FROM rules ORDER BY rule_id
            """
        ).fetchall()
    finally:
        conn.close()

    if not rows:
        raise ValueError("No rules to embed")

    rule_ids = [r["rule_id"] for r in rows]
    docs = [tokenize(_doc_text(r)) for r in rows]
    n_docs = len(docs)

    df: dict[str, int] = {}
    for toks in docs:
        for t in set(toks):
            df[t] = df.get(t, 0) + 1

    vocab_terms = sorted(
        (t for t, c in df.items() if c >= min_df),
        key=lambda t: (-df[t], t),
    )[:max_vocab]
    vocab = {t: i for i, t in enumerate(vocab_terms)}
    dim = len(vocab)
    if dim == 0:
        raise ValueError("Empty vocabulary after min_df filter")

    idf = np.zeros(dim, dtype=np.float32)
    for t, i in vocab.items():
        idf[i] = math.log((1.0 + n_docs) / (1.0 + df[t])) + 1.0

    matrix = np.zeros((n_docs, dim), dtype=np.float32)
    for i, toks in enumerate(docs):
        if not toks:
            continue
        tf: dict[int, float] = {}
        for t in toks:
            j = vocab.get(t)
            if j is not None:
                tf[j] = tf.get(j, 0.0) + 1.0
        if not tf:
            continue
        max_tf = max(tf.values())
        for j, c in tf.items():
            matrix[i, j] = (0.5 + 0.5 * c / max_tf) * idf[j]
        norm = float(np.linalg.norm(matrix[i]))
        if norm > 0:
            matrix[i] /= norm

    out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out,
        rule_ids=np.array(rule_ids, dtype=object),
        matrix=matrix,
        vocab_terms=np.array(vocab_terms, dtype=object),
        idf=idf,
    )
    return {
        "path": str(out),
        "n_docs": n_docs,
        "dim": dim,
        "bytes": out.stat().st_size if out.exists() else 0,
    }


class VectorIndex:
    def __init__(self, path: Path | None = None):
        self.path = path or DEFAULT_VECTORS
        if not self.path.exists():
            raise FileNotFoundError(
                f"Vector index missing at {self.path}. "
                "Run: python3 scripts/build_corpus.py"
            )
        data = np.load(self.path, allow_pickle=True)
        self.rule_ids: list[str] = [str(x) for x in data["rule_ids"].tolist()]
        self.matrix: np.ndarray = data["matrix"].astype(np.float32)
        self.vocab_terms: list[str] = [str(x) for x in data["vocab_terms"].tolist()]
        self.vocab = {t: i for i, t in enumerate(self.vocab_terms)}
        self.idf: np.ndarray = data["idf"].astype(np.float32)

    def encode(self, query: str) -> np.ndarray:
        toks = tokenize(query)
        vec = np.zeros(len(self.vocab), dtype=np.float32)
        if not toks:
            return vec
        tf: dict[int, float] = {}
        for t in toks:
            j = self.vocab.get(t)
            if j is not None:
                tf[j] = tf.get(j, 0.0) + 1.0
        if not tf:
            return vec
        max_tf = max(tf.values())
        for j, c in tf.items():
            vec[j] = (0.5 + 0.5 * c / max_tf) * self.idf[j]
        norm = float(np.linalg.norm(vec))
        if norm > 0:
            vec /= norm
        return vec

    def search(self, query: str, *, limit: int = 20) -> list[tuple[str, float]]:
        q = self.encode(query)
        if float(np.linalg.norm(q)) == 0.0:
            return []
        scores = self.matrix @ q
        if limit >= len(scores):
            order = np.argsort(-scores)
        else:
            # partial top-k
            idx = np.argpartition(-scores, limit)[:limit]
            order = idx[np.argsort(-scores[idx])]
        out: list[tuple[str, float]] = []
        for i in order[:limit]:
            s = float(scores[i])
            if s <= 0:
                continue
            out.append((self.rule_ids[int(i)], s))
        return out


_INDEX: VectorIndex | None = None


def get_vector_index(path: Path | None = None) -> VectorIndex | None:
    global _INDEX
    p = path or DEFAULT_VECTORS
    if not p.exists():
        return None
    if _INDEX is None or _INDEX.path != p:
        _INDEX = VectorIndex(p)
    return _INDEX


def retrieval_mode() -> str:
    """fts | hybrid | vector — default hybrid when index exists."""
    mode = (os.getenv("CORPUS_RETRIEVAL") or "").strip().lower()
    if mode in {"fts", "hybrid", "vector"}:
        return mode
    return "hybrid" if DEFAULT_VECTORS.exists() else "fts"
