"""Seeded cohort sampling (prereg section 2).

Hash-rank sampling: every eligible subject is ranked by sha256(f"{seed}|{subject_id}").
The first N are the cohort; the rest, in rank order, are the replacement queue.
Deterministic, independent of input order, and independent of Python/NumPy RNG versions.
"""
from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


def _rank_key(seed: int, subject_id: str) -> str:
    return hashlib.sha256(f"{seed}|{subject_id}".encode("utf-8")).hexdigest()


def ids_hash(ids: Iterable[str]) -> str:
    """Order-independent hash of an id set (register this for the frame and the exclusions)."""
    return hashlib.sha256("\n".join(sorted(set(ids))).encode("utf-8")).hexdigest()


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_ids(path: str | Path, column: str = "subject_id") -> list[str]:
    """Read ids from a .csv (named column) or a .json list of strings."""
    p = Path(path)
    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
        return [str(x) for x in data]
    with open(p, newline="", encoding="utf-8") as fh:
        return [row[column].strip() for row in csv.DictReader(fh) if row[column].strip()]


@dataclass(frozen=True)
class Draw:
    seed: int
    n: int
    frame_hash: str
    exclusion_hash: str
    ranked: tuple[str, ...]  # full eligible ranking; cohort = first n, rest = replacement queue

    @property
    def cohort(self) -> tuple[str, ...]:
        return self.ranked[: self.n]

    @property
    def replacement_queue(self) -> tuple[str, ...]:
        return self.ranked[self.n :]


def draw_cohort(
    frame_ids: Sequence[str], *, seed: int, n: int, exclusions: Iterable[str] = ()
) -> Draw:
    ids = list(frame_ids)
    if len(ids) != len(set(ids)):
        raise ValueError("frame contains duplicate subject ids; dedupe upstream and log it")
    excl = set(exclusions)
    eligible = [i for i in ids if i not in excl]
    if len(eligible) < n:
        raise ValueError(f"only {len(eligible)} eligible subjects for n={n}")
    ranked = tuple(sorted(eligible, key=lambda i: (_rank_key(seed, i), i)))
    return Draw(
        seed=seed,
        n=n,
        frame_hash=ids_hash(ids),
        exclusion_hash=ids_hash(excl),
        ranked=ranked,
    )


def effective_cohort(draw: Draw, failed: Iterable[str] = ()) -> tuple[tuple[str, ...], list[tuple[str, str]]]:
    """Apply the registered replacement policy: drop failed ids, take the next in rank order.

    Returns (cohort, swap_log) where swap_log is [(failed_id, replacement_id), ...] for the
    deviations log (prereg section 12).
    """
    failed_set = set(failed)
    remaining = [r for r in draw.ranked if r not in failed_set]
    cohort = tuple(remaining[: draw.n])
    dropped = [i for i in draw.cohort if i in failed_set]
    added = [i for i in cohort if i not in draw.cohort]
    return cohort, list(zip(dropped, added))


def assert_disjoint(cohort: Iterable[str], exclusions: Iterable[str]) -> None:
    overlap = set(cohort) & set(exclusions)
    if overlap:
        raise AssertionError(f"cohort overlaps hard exclusions: {sorted(overlap)}")
