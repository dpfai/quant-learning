"""Mean-variance portfolio optimization using scipy."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from portfolio.constraints import factor_exposure_constraints, sector_cap_constraints, weight_bounds


class PortfolioOptimizer:
    """Long-only mean-variance optimizer with optional factor and sector limits."""

    def __init__(self, expected_returns, covariance):
        self.expected_returns = pd.Series(expected_returns, dtype=float)
        self.covariance = pd.DataFrame(covariance, index=self.expected_returns.index, columns=self.expected_returns.index).astype(float)

    def optimize(self, risk_aversion: float = 1.0, max_weight: float = 1.0, sectors=None, sector_caps=None, factor_exposures=None, factor_bounds=None) -> pd.Series:
        """Maximize expected return minus risk_aversion times variance."""
        n_assets = len(self.expected_returns)
        if max_weight * n_assets < 1 - 1e-12:
            raise ValueError("max_weight is infeasible for the number of assets")
        constraints = [{"type": "eq", "fun": lambda w: w.sum() - 1.0}]
        if sectors is not None and sector_caps:
            constraints += sector_cap_constraints(sectors, sector_caps)
        if factor_exposures is not None and factor_bounds:
            constraints += factor_exposure_constraints(pd.DataFrame(factor_exposures, index=self.expected_returns.index), factor_bounds)
        mu, cov = self.expected_returns.to_numpy(), self.covariance.to_numpy()
        result = minimize(lambda w: risk_aversion * (w @ cov @ w) - w @ mu, np.repeat(1 / n_assets, n_assets), method="SLSQP", bounds=weight_bounds(n_assets, max_weight), constraints=constraints)
        if not result.success:
            raise ValueError(f"Optimization failed: {result.message}")
        return pd.Series(result.x, index=self.expected_returns.index, name="weight")

    def factor_constrained(self, factor_exposures, factor_bounds, **kwargs) -> pd.Series:
        """Convenience wrapper for exposure-constrained optimization."""
        return self.optimize(factor_exposures=factor_exposures, factor_bounds=factor_bounds, **kwargs)

    def risk_report(self, weights, confidence: float = 0.95) -> dict:
        """Return annualized expected return, volatility and normal one-day VaR."""
        w = pd.Series(weights).reindex(self.expected_returns.index).to_numpy()
        annual_return = float(w @ self.expected_returns.to_numpy())
        annual_volatility = float(np.sqrt(w @ self.covariance.to_numpy() @ w))
        daily_var = 1.645 * annual_volatility / np.sqrt(252) - annual_return / 252 if confidence == 0.95 else annual_volatility / np.sqrt(252)
        return {"expected_return": annual_return, "volatility": annual_volatility, "var_1d": max(float(daily_var), 0.0)}
