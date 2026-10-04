import hashlib
from datetime import date, datetime, timedelta, timezone

import numpy as np
import pytest

from studies.kl_n30_001 import nulls, sampling

UTC = timezone.utc


# ------------------------------------------------------------------ sampling
def _frame(n=200):
    return [f"AA{i:04d}" for i in range(n)]


def test_draw_is_deterministic_and_order_independent():
    f = _frame()
    a = sampling.draw_cohort(f, seed=20261006, n=30)
    b = sampling.draw_cohort(list(reversed(f)), seed=20261006, n=30)
    assert a.cohort == b.cohort and a.frame_hash == b.frame_hash
    assert len(set(a.cohort)) == 30


def test_different_seed_changes_cohort():
    f = _frame()
    assert sampling.draw_cohort(f, seed=1, n=30).cohort != sampling.draw_cohort(f, seed=2, n=30).cohort


def test_exclusions_are_respected_and_hashed():
    f = _frame()
    excl = f[:50]
    d = sampling.draw_cohort(f, seed=7, n=30, exclusions=excl)
    sampling.assert_disjoint(d.cohort, excl)
    assert d.exclusion_hash == sampling.ids_hash(excl)
    with pytest.raises(AssertionError):
        sampling.assert_disjoint(d.cohort, d.cohort[:1])


def test_duplicate_frame_ids_rejected():
    with pytest.raises(ValueError):
        sampling.draw_cohort(["a", "a", "b"], seed=1, n=1)


def test_replacement_policy_takes_next_in_rank_order():
    d = sampling.draw_cohort(_frame(), seed=3, n=30)
    failed = {d.cohort[4], d.cohort[17]}
    cohort, swaps = sampling.effective_cohort(d, failed)
    assert len(cohort) == 30 and not (set(cohort) & failed)
    assert [new for _, new in swaps] == list(d.replacement_queue[:2])
    assert [old for old, _ in swaps] == [d.cohort[4], d.cohort[17]]


def test_failed_id_outside_cohort_changes_nothing():
    d = sampling.draw_cohort(_frame(), seed=3, n=30)
    cohort, swaps = sampling.effective_cohort(d, {d.replacement_queue[5]})
    assert cohort == d.cohort and swaps == []


# ------------------------------------------------------------------ nulls
def _subjects(n=12, n_events=5):
    out = []
    for i in range(n):
        birth = datetime(1950 + 3 * i, 1 + i % 12, 10 + i, 6 + i % 10, 15, tzinfo=UTC)
        start = (birth + timedelta(days=16 * 365)).date()
        end = date(2020, 1, 1)
        evs = tuple(start + timedelta(days=700 * (k + 1) + 13 * i) for k in range(n_events))
        out.append(nulls.Subject(f"S{i:02d}", birth, 49.45 + i * 0.1, 11.08, evs, start, end))
    return out


def _noise(birth, lat, lon, events):
    key = f"{birth.isoformat()}|{lat:.3f}|{lon:.3f}|{sorted(e.isoformat() for e in events)}"
    return int(hashlib.sha256(key.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF * 100.0


def _signal_fn(subjects, bonus=40.0):
    truth = {(s.birth_utc, s.lat, s.lon): tuple(sorted(s.events)) for s in subjects}

    def fn(birth, lat, lon, events):
        base = _noise(birth, lat, lon, events)
        if truth.get((birth, lat, lon)) == tuple(sorted(events)):
            base += bonus
        return base

    return fn


def test_rng_streams_independent_of_subject_set_and_order():
    s = _subjects()
    r1 = nulls.random_dates(s[3], nulls.derive_rng(9, "random_date", s[3].subject_id))
    r2 = nulls.random_dates(s[3], nulls.derive_rng(9, "random_date", s[3].subject_id))
    assert r1 == r2
    a = nulls.run_random_date_null(s, _noise, master_seed=9, k=20)
    b = nulls.run_random_date_null(list(reversed(s)), _noise, master_seed=9, k=20)
    assert np.allclose(a.null, b.null[::-1])


def test_random_dates_in_pool_distinct_and_count_matched():
    s = _subjects()[0]
    rng = nulls.derive_rng(1, "x")
    for _ in range(200):
        d = nulls.random_dates(s, rng)
        assert len(d) == len(s.events) == len(set(d))
        assert all(s.pool_start <= x <= s.pool_end for x in d)


def test_pool_too_small_raises():
    s = _subjects()[0]
    tiny = nulls.Subject(s.subject_id, s.birth_utc, s.lat, s.lon, s.events, s.pool_start, s.pool_start)
    with pytest.raises(ValueError):
        nulls.random_dates(tiny, nulls.derive_rng(1, "x"))


def test_perturbation_bounds():
    b = datetime(1980, 5, 5, 12, 0, tzinfo=UTC)
    rng = nulls.derive_rng(1, "p")
    for _ in range(500):
        p = nulls.perturb_birth(b, rng, date_offset_years=3.0, time_offset_hours=12.0)
        assert abs((p - b).total_seconds()) <= (3 * 365.25 * 86400 + 12 * 3600 + 1)


def test_all_three_nulls_detect_planted_signal():
    s = _subjects()
    fn = _signal_fn(s)
    rd = nulls.run_random_date_null(s, fn, master_seed=11, k=300)
    rc = nulls.run_random_chart_null(s, fn, master_seed=11, k=300, date_offset_years=3.0, time_offset_hours=12.0)
    wc = nulls.run_wrong_chart_control(s, fn, master_seed=11, permutations=2000)
    for p in (
        rd.p_value(alternative="greater"),
        rc.p_value(alternative="greater"),
        wc.p_value(alternative="greater"),
    ):
        assert p < 0.01


def test_no_signal_gives_unremarkable_p_values():
    s = _subjects()
    rd = nulls.run_random_date_null(s, _noise, master_seed=11, k=300)
    rc = nulls.run_random_chart_null(s, _noise, master_seed=11, k=300, date_offset_years=3.0, time_offset_hours=12.0)
    wc = nulls.run_wrong_chart_control(s, _noise, master_seed=11, permutations=2000)
    for p in (
        rd.p_value(alternative="two-sided"),
        rc.p_value(alternative="two-sided"),
        wc.p_value(alternative="two-sided"),
    ):
        assert p > 0.01


def test_alternative_must_be_explicit():
    s = _subjects(4)
    rd = nulls.run_random_date_null(s, _noise, master_seed=1, k=10)
    with pytest.raises(ValueError):
        rd.p_value(alternative="less")


def test_wrong_chart_matrix_shape_and_diag():
    s = _subjects(5)
    wc = nulls.run_wrong_chart_control(s, _noise, master_seed=2, permutations=50)
    assert wc.matrix.shape == (5, 5)
    assert np.isclose(wc.t_obs, np.diag(wc.matrix).mean())
    assert wc.delta_per_subject.shape == (5,)
