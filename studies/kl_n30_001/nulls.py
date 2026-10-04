"""Seeded null generators (prereg section 6).

Contract with the engine: ScoreFn(birth_utc, lat, lon, event_dates) -> float
  Builds the chart from birth data (vcs_profile="kl_n30_001", frozen engine tag), applies the
  per-lord window of THAT chart's birth Moon, and returns the registered per-subject score
  (e.g. mean VCS over the supplied dates). It must be deterministic and must not read events
  from anywhere else.

RNG streams are derived per (master_seed, null, subject), so adding/removing/reordering
subjects never changes another subject's stream.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Callable, Sequence

import numpy as np

ScoreFn = Callable[[datetime, float, float, Sequence[date]], float]


@dataclass(frozen=True)
class Subject:
    subject_id: str
    birth_utc: datetime  # timezone-aware, UTC
    lat: float
    lon: float
    events: tuple[date, ...]
    pool_start: date  # random-date pool, from the registered rule (e.g. birth + min age)
    pool_end: date  # e.g. min(death, data cutoff)


def derive_rng(master_seed: int, *labels: str) -> np.random.Generator:
    digest = hashlib.sha256("|".join(labels).encode("utf-8")).digest()
    key = int.from_bytes(digest[:8], "big")
    return np.random.default_rng(np.random.SeedSequence([int(master_seed), key]))


def _score(fn: ScoreFn, s: Subject, events: Sequence[date]) -> float:
    return float(fn(s.birth_utc, s.lat, s.lon, events))


def cohort_p_value(real: np.ndarray, null: np.ndarray, *, alternative: str) -> float:
    """Cohort-level empirical p. real: (n,), null: (n, K); column k is replicate k for all subjects."""
    if alternative not in ("greater", "two-sided"):
        raise ValueError("alternative must be 'greater' or 'two-sided' (registered, no default)")
    t_obs = float(real.mean())
    t_null = null.mean(axis=0)
    k = t_null.shape[0]
    p_hi = (1 + int(np.sum(t_null >= t_obs))) / (1 + k)
    if alternative == "greater":
        return p_hi
    p_lo = (1 + int(np.sum(t_null <= t_obs))) / (1 + k)
    return min(1.0, 2.0 * min(p_hi, p_lo))


@dataclass(frozen=True)
class ReplicateNull:
    name: str
    subject_ids: tuple[str, ...]
    real: np.ndarray  # (n,)
    null: np.ndarray  # (n, K)

    @property
    def delta_per_subject(self) -> np.ndarray:
        return self.real - self.null.mean(axis=1)

    def p_value(self, *, alternative: str) -> float:
        return cohort_p_value(self.real, self.null, alternative=alternative)


# ---------------------------------------------------------------- null 1: random dates
def random_dates(s: Subject, rng: np.random.Generator) -> tuple[date, ...]:
    n_days = (s.pool_end - s.pool_start).days + 1
    n_ev = len(s.events)
    if n_ev == 0 or n_days < n_ev:
        raise ValueError(f"{s.subject_id}: pool of {n_days} days cannot hold {n_ev} events")
    offs = rng.choice(n_days, size=n_ev, replace=False)
    return tuple(sorted(s.pool_start + timedelta(days=int(o)) for o in offs))


def run_random_date_null(
    subjects: Sequence[Subject], score_fn: ScoreFn, *, master_seed: int, k: int
) -> ReplicateNull:
    real = np.empty(len(subjects))
    null = np.empty((len(subjects), k))
    for i, s in enumerate(subjects):
        real[i] = _score(score_fn, s, s.events)
        rng = derive_rng(master_seed, "random_date", s.subject_id)
        for j in range(k):
            null[i, j] = _score(score_fn, s, random_dates(s, rng))
    return ReplicateNull("random_date", tuple(s.subject_id for s in subjects), real, null)


# ---------------------------------------------------------------- null 2: perturbed charts
def perturb_birth(
    birth_utc: datetime,
    rng: np.random.Generator,
    *,
    date_offset_years: float,
    time_offset_hours: float,
) -> datetime:
    max_days = int(round(date_offset_years * 365.25))
    days = int(rng.integers(-max_days, max_days + 1))
    hours = float(rng.uniform(-time_offset_hours, time_offset_hours))
    return birth_utc + timedelta(days=days, hours=hours)


def run_random_chart_null(
    subjects: Sequence[Subject],
    score_fn: ScoreFn,
    *,
    master_seed: int,
    k: int,
    date_offset_years: float,
    time_offset_hours: float,
) -> ReplicateNull:
    real = np.empty(len(subjects))
    null = np.empty((len(subjects), k))
    for i, s in enumerate(subjects):
        real[i] = _score(score_fn, s, s.events)
        rng = derive_rng(master_seed, "random_chart", s.subject_id)
        for j in range(k):
            b = perturb_birth(
                s.birth_utc, rng, date_offset_years=date_offset_years, time_offset_hours=time_offset_hours
            )
            null[i, j] = float(score_fn(b, s.lat, s.lon, s.events))
    return ReplicateNull("random_chart", tuple(s.subject_id for s in subjects), real, null)


# ---------------------------------------------------------------- null 3: wrong-chart control
@dataclass(frozen=True)
class WrongChartResult:
    subject_ids: tuple[str, ...]
    matrix: np.ndarray  # matrix[i, j] = score of subject i's events on subject j's chart
    t_obs: float
    t_perm: np.ndarray  # (B,)

    @property
    def wrong_mean_per_subject(self) -> np.ndarray:
        n = self.matrix.shape[0]
        off = self.matrix.copy()
        np.fill_diagonal(off, np.nan)
        return np.nanmean(off, axis=1)

    @property
    def delta_per_subject(self) -> np.ndarray:
        return np.diag(self.matrix) - self.wrong_mean_per_subject

    def p_value(self, *, alternative: str) -> float:
        if alternative not in ("greater", "two-sided"):
            raise ValueError("alternative must be 'greater' or 'two-sided' (registered, no default)")
        b = self.t_perm.shape[0]
        p_hi = (1 + int(np.sum(self.t_perm >= self.t_obs))) / (1 + b)
        if alternative == "greater":
            return p_hi
        p_lo = (1 + int(np.sum(self.t_perm <= self.t_obs))) / (1 + b)
        return min(1.0, 2.0 * min(p_hi, p_lo))


def run_wrong_chart_control(
    subjects: Sequence[Subject], score_fn: ScoreFn, *, master_seed: int, permutations: int
) -> WrongChartResult:
    n = len(subjects)
    m = np.empty((n, n))
    for i, si in enumerate(subjects):
        for j, sj in enumerate(subjects):
            m[i, j] = float(score_fn(sj.birth_utc, sj.lat, sj.lon, si.events))
    rng = derive_rng(master_seed, "wrong_chart", "permutations")
    perms = np.stack([rng.permutation(n) for _ in range(permutations)])
    t_perm = m[np.arange(n)[None, :], perms].mean(axis=1)
    return WrongChartResult(tuple(s.subject_id for s in subjects), m, float(np.diag(m).mean()), t_perm)
