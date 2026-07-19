"""Constraint builders for scipy portfolio optimization."""
from __future__ import annotations

import numpy as np


def weight_bounds(n_assets: int, max_weight: float = 1.0, allow_short: bool = False):
    """Return per-asset scipy bounds."""
    if not 0 < max_weight <= 1:
        raise ValueError("max_weight must be in (0, 1]")
    return [(-max_weight if allow_short else 0.0, max_weight)] * n_assets


def sector_cap_constraints(sectors, sector_caps: dict):
    """Build scipy inequalities enforcing sum(weights in sector) <= cap."""
    sectors = np.asarray(sectors)
    return [{"type": "ineq", "fun": lambda w, mask=sectors == sector, cap=cap: cap - w[mask].sum()} for sector, cap in sector_caps.items()]


def factor_exposure_constraints(exposures, bounds):
    """Build lower/upper bounds for each named portfolio factor exposure."""
    constraints = []
    for name, (lower, upper) in bounds.items():
        values = np.asarray(exposures[name], dtype=float)
        constraints.extend([{"type": "ineq", "fun": lambda w, v=values, lo=lower: w @ v - lo}, {"type": "ineq", "fun": lambda w, v=values, hi=upper: hi - w @ v}])
    return constraints
