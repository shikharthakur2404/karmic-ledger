"""Power / MDE simulation for KL-N30-001 (prereg §2).

Uses synthetic paired excess-VCS draws — never held-out AA subjects.
Register the printed MDE in the preregistration before freeze.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy import stats  # type: ignore


def power_at_dz(
    *,
    n: int,
    dz: float,
    alpha: float,
    n_sims: int,
    rng: np.random.Generator,
) -> float:
    """Monte Carlo power of two-sided one-sample t on mean of N paired deltas."""
    # Under H1: Δ_i ~ N(dz * σ, σ²) with σ=1 → mean dz
    rejects = 0
    for _ in range(n_sims):
        sample = rng.normal(loc=dz, scale=1.0, size=n)
        t_stat, p = stats.ttest_1samp(sample, 0.0)
        if p < alpha and t_stat > 0:
            rejects += 1
    return rejects / n_sims


def mde_for_power(
    *,
    n: int,
    alpha: float,
    target_power: float,
    n_sims: int,
    rng: np.random.Generator,
    grid: np.ndarray | None = None,
) -> float:
    """Smallest dz on grid with empirical power ≥ target_power."""
    if grid is None:
        grid = np.arange(0.20, 1.01, 0.05)
    for dz in grid:
        pwr = power_at_dz(n=n, dz=float(dz), alpha=alpha, n_sims=n_sims, rng=rng)
        if pwr >= target_power:
            return float(dz)
    return float(grid[-1])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=30)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--sims", type=int, default=5000)
    ap.add_argument("--seed", type=int, default=0x4B4C4E35)
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    dz_grid = [0.2, 0.3, 0.5, 0.8]
    powers = {
        str(dz): power_at_dz(
            n=args.n, dz=dz, alpha=args.alpha, n_sims=args.sims, rng=rng
        )
        for dz in dz_grid
    }
    mde = mde_for_power(
        n=args.n,
        alpha=args.alpha,
        target_power=0.80,
        n_sims=args.sims,
        rng=rng,
    )
    # Analytic floor (prereg): ~0.53 at N=30, α=0.05, 80%
    analytic = float(stats.norm.ppf(1 - args.alpha / 2) + stats.norm.ppf(0.80))
    analytic /= np.sqrt(args.n)

    report = {
        "study_id": "KL-N30-001",
        "n": args.n,
        "alpha": args.alpha,
        "n_sims": args.sims,
        "seed": args.seed,
        "power_at_dz": powers,
        "registered_mde_dz_approx": mde,
        "analytic_detection_floor_dz": round(analytic, 3),
        "note": (
            "MDE is a design finding, not an astrology effect-size claim. "
            "Synthetic paired-t simulation only — never run on held-out AA."
        ),
    }
    text = json.dumps(report, indent=2)
    print(text)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
