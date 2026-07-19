"""Price momentum factors."""
from __future__ import annotations

import pandas as pd


def _skip_recent_return(prices: pd.DataFrame | pd.Series, lookback: int, skip: int = 21):
    return prices.shift(skip) / prices.shift(lookback) - 1


def momentum_12_1(prices: pd.DataFrame | pd.Series) -> pd.DataFrame | pd.Series:
    """Approximate 12-to-1 month momentum using 252 and 21 trading days."""
    return _skip_recent_return(prices, 252)


def momentum_6_1(prices: pd.DataFrame | pd.Series) -> pd.DataFrame | pd.Series:
    """Approximate 6-to-1 month momentum using 126 and 21 trading days."""
    return _skip_recent_return(prices, 126)


def cross_sectional_rank(factor: pd.DataFrame | pd.Series, pct: bool = True):
    """Rank securities within each date; a Series is ranked as one cross-section."""
    return factor.rank(axis=1, pct=pct) if isinstance(factor, pd.DataFrame) else factor.rank(pct=pct)
