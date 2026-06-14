"""Relative performance calculations for stocks and benchmarks."""
from __future__ import annotations

from typing import Dict, Iterable

import numpy as np
import pandas as pd


def _aligned_prices(
    stock_prices: pd.Series,
    benchmark_prices: pd.Series,
) -> pd.DataFrame:
    aligned = pd.concat(
        [
            pd.to_numeric(stock_prices, errors="coerce").rename("stock"),
            pd.to_numeric(benchmark_prices, errors="coerce").rename("benchmark"),
        ],
        axis=1,
        join="inner",
    )
    return aligned.replace([np.inf, -np.inf], np.nan).dropna()


def _period_return(prices: pd.Series, periods: int) -> float:
    if len(prices) <= periods or prices.iloc[-periods - 1] == 0:
        return float("nan")
    return float(prices.iloc[-1] / prices.iloc[-periods - 1] - 1)


def calculate_relative_performance(
    stock_prices: pd.Series,
    benchmark_prices: pd.Series,
    periods: Iterable[int] = (5, 20, 60, 252),
) -> Dict[str, float]:
    """Calculate stock, benchmark, and excess returns over several horizons."""
    aligned = _aligned_prices(stock_prices, benchmark_prices)
    results: Dict[str, float] = {}

    for period in periods:
        label = f"{period}d"
        stock_return = _period_return(aligned["stock"], period)
        benchmark_return = _period_return(aligned["benchmark"], period)
        results[f"stock_{label}"] = stock_return
        results[f"benchmark_{label}"] = benchmark_return
        results[f"alpha_{label}"] = stock_return - benchmark_return

    current_year = aligned.index[-1].year if not aligned.empty else None
    year_data = aligned[aligned.index.year == current_year] if current_year else aligned
    if len(year_data) >= 2 and year_data.iloc[0].ne(0).all():
        stock_ytd = float(year_data["stock"].iloc[-1] / year_data["stock"].iloc[0] - 1)
        benchmark_ytd = float(
            year_data["benchmark"].iloc[-1] / year_data["benchmark"].iloc[0] - 1
        )
    else:
        stock_ytd = benchmark_ytd = float("nan")

    results.update(
        {
            "stock_ytd": stock_ytd,
            "benchmark_ytd": benchmark_ytd,
            "alpha_ytd": stock_ytd - benchmark_ytd,
        }
    )
    return results


def calculate_rolling_alpha(
    stock_returns: pd.Series,
    benchmark_returns: pd.Series,
    window: int = 20,
) -> pd.Series:
    """Calculate rolling mean annualized excess return."""
    aligned = _aligned_prices(stock_returns, benchmark_returns)
    active_returns = aligned["stock"] - aligned["benchmark"]
    return active_returns.rolling(window).mean() * 252


def calculate_tracking_error(
    stock_returns: pd.Series,
    benchmark_returns: pd.Series,
) -> float:
    """Calculate annualized volatility of active returns."""
    aligned = _aligned_prices(stock_returns, benchmark_returns)
    if len(aligned) < 2:
        return float("nan")
    active_returns = aligned["stock"] - aligned["benchmark"]
    return float(active_returns.std(ddof=1) * np.sqrt(252))


def calculate_information_ratio(
    stock_returns: pd.Series,
    benchmark_returns: pd.Series,
) -> float:
    """Calculate annualized active return divided by tracking error."""
    aligned = _aligned_prices(stock_returns, benchmark_returns)
    if aligned.empty:
        return float("nan")
    tracking_error = calculate_tracking_error(
        aligned["stock"],
        aligned["benchmark"],
    )
    if not np.isfinite(tracking_error) or np.isclose(tracking_error, 0):
        return float("nan")
    annualized_active_return = float(
        (aligned["stock"] - aligned["benchmark"]).mean() * 252
    )
    return annualized_active_return / tracking_error
