"""Risk-parity and custom risk-budget allocation."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize


def risk_contributions(weights, covariance):
    """Return each asset's share of total portfolio variance."""
    covariance = np.asarray(covariance, dtype=float)
    variance = weights @ covariance @ weights
    return weights * (covariance @ weights) / variance if variance > 0 else np.zeros_like(weights)


def risk_budget_allocation(covariance: pd.DataFrame, budgets=None, max_weight: float = 1.0) -> pd.Series:
    """Find long-only weights whose variance contributions match budgets."""
    n_assets = len(covariance)
    target = np.repeat(1 / n_assets, n_assets) if budgets is None else np.asarray(budgets, dtype=float) / np.sum(budgets)
    result = minimize(lambda w: np.sum((risk_contributions(w, covariance.to_numpy()) - target) ** 2), np.repeat(1 / n_assets, n_assets), method="SLSQP", bounds=[(1e-8, max_weight)] * n_assets, constraints={"type": "eq", "fun": lambda w: w.sum() - 1})
    if not result.success:
        raise ValueError(f"Risk-budget optimization failed: {result.message}")
    return pd.Series(result.x, index=covariance.index, name="weight")


def risk_parity(covariance: pd.DataFrame, max_weight: float = 1.0) -> pd.Series:
    """Allocate equal portfolio variance contribution to every asset."""
    return risk_budget_allocation(covariance, max_weight=max_weight)
