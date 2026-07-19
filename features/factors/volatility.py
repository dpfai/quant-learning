"""Low-volatility and market beta factors."""
from __future__ import annotations

import numpy as np
import pandas as pd


def realized_volatility(returns: pd.DataFrame | pd.Series, window: int = 21, annualization: int = 252):
    """Annualized rolling standard deviation of returns."""
    return returns.rolling(window).std() * np.sqrt(annualization)


def beta(returns: pd.DataFrame | pd.Series, market_returns: pd.Series, window: int = 60):
    """Rolling beta versus a market return series."""
    covariance = returns.rolling(window).cov(market_returns)
    variance = market_returns.rolling(window).var().replace(0, np.nan)
    return covariance.div(variance, axis=0) if isinstance(covariance, pd.DataFrame) else covariance / variance
