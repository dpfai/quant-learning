"""Risk and performance metric calculations."""
from __future__ import annotations

from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd

from config.settings import RISK_FREE_RATE


def _clean_series(series: pd.Series) -> pd.Series:
    """Return numeric, finite values while preserving the original index."""
    cleaned = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan)
    return cleaned.dropna()


def calculate_returns(prices: pd.Series) -> pd.Series:
    """Calculate simple period-over-period returns."""
    return _clean_series(prices).pct_change(fill_method=None).dropna()


def calculate_annualized_return(
    returns: pd.Series,
    periods_per_year: int = 252,
) -> float:
    """Calculate compounded annualized return."""
    clean_returns = _clean_series(returns)
    if clean_returns.empty:
        return float("nan")

    growth = float((1 + clean_returns).prod())
    if growth <= 0:
        return -1.0
    return float(growth ** (periods_per_year / len(clean_returns)) - 1)


def calculate_annualized_volatility(
    returns: pd.Series,
    periods_per_year: int = 252,
) -> float:
    """Calculate annualized sample standard deviation of returns."""
    clean_returns = _clean_series(returns)
    if len(clean_returns) < 2:
        return float("nan")
    return float(clean_returns.std(ddof=1) * np.sqrt(periods_per_year))


def calculate_max_drawdown(
    prices: pd.Series,
) -> Tuple[float, Optional[pd.Timestamp], Optional[pd.Timestamp]]:
    """Return maximum drawdown and its peak/trough dates."""
    clean_prices = _clean_series(prices)
    if clean_prices.empty:
        return float("nan"), None, None

    running_peak = clean_prices.cummax()
    drawdowns = clean_prices / running_peak - 1
    trough_index = drawdowns.idxmin()
    peak_index = clean_prices.loc[:trough_index].idxmax()
    return float(drawdowns.loc[trough_index]), peak_index, trough_index


def calculate_sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = RISK_FREE_RATE,
    periods_per_year: int = 252,
) -> float:
    """Calculate annualized Sharpe ratio using a daily risk-free rate."""
    clean_returns = _clean_series(returns)
    if len(clean_returns) < 2:
        return float("nan")

    volatility = float(clean_returns.std(ddof=1))
    if np.isclose(volatility, 0):
        return float("nan")

    excess_returns = clean_returns - risk_free_rate / periods_per_year
    return float(excess_returns.mean() / volatility * np.sqrt(periods_per_year))


def calculate_sortino_ratio(
    returns: pd.Series,
    risk_free_rate: float = RISK_FREE_RATE,
    periods_per_year: int = 252,
) -> float:
    """Calculate annualized Sortino ratio using downside deviation."""
    clean_returns = _clean_series(returns)
    if clean_returns.empty:
        return float("nan")

    excess_returns = clean_returns - risk_free_rate / periods_per_year
    downside = np.minimum(excess_returns, 0)
    downside_deviation = float(np.sqrt(np.mean(np.square(downside))))
    if np.isclose(downside_deviation, 0):
        return float("nan")

    return float(excess_returns.mean() / downside_deviation * np.sqrt(periods_per_year))


def calculate_beta(stock_returns: pd.Series, market_returns: pd.Series) -> float:
    """Calculate beta after aligning stock and market returns by index."""
    aligned = pd.concat(
        [
            _clean_series(stock_returns).rename("stock"),
            _clean_series(market_returns).rename("market"),
        ],
        axis=1,
        join="inner",
    ).dropna()
    if len(aligned) < 2:
        return float("nan")

    market_variance = float(aligned["market"].var(ddof=1))
    if np.isclose(market_variance, 0):
        return float("nan")

    covariance = float(aligned["stock"].cov(aligned["market"]))
    return covariance / market_variance


def calculate_correlation_matrix(
    returns_dict: Dict[str, pd.Series],
) -> pd.DataFrame:
    """Calculate an aligned correlation matrix for multiple assets."""
    if not returns_dict:
        return pd.DataFrame()

    returns = pd.concat(
        {ticker: _clean_series(series) for ticker, series in returns_dict.items()},
        axis=1,
    )
    return returns.corr()


def calculate_all_risk_metrics(
    prices: pd.Series,
    benchmark_prices: Optional[pd.Series] = None,
    risk_free_rate: float = RISK_FREE_RATE,
) -> Dict[str, object]:
    """Calculate the dashboard's standard risk and return metrics."""
    clean_prices = _clean_series(prices)
    returns = calculate_returns(clean_prices)
    max_drawdown, max_dd_start, max_dd_end = calculate_max_drawdown(clean_prices)

    beta = None
    if benchmark_prices is not None:
        calculated_beta = calculate_beta(returns, calculate_returns(benchmark_prices))
        beta = calculated_beta if np.isfinite(calculated_beta) else None

    total_return = float("nan")
    if len(clean_prices) >= 2 and clean_prices.iloc[0] != 0:
        total_return = float(clean_prices.iloc[-1] / clean_prices.iloc[0] - 1)

    gains = returns[returns > 0]
    losses = returns[returns < 0]

    return {
        "total_return": total_return,
        "ann_return": calculate_annualized_return(returns),
        "ann_volatility": calculate_annualized_volatility(returns),
        "max_drawdown": max_drawdown,
        "max_dd_start": max_dd_start,
        "max_dd_end": max_dd_end,
        "sharpe_ratio": calculate_sharpe_ratio(returns, risk_free_rate),
        "sortino_ratio": calculate_sortino_ratio(returns, risk_free_rate),
        "beta": beta,
        "win_rate": float((returns > 0).mean()) if not returns.empty else float("nan"),
        "avg_gain": float(gains.mean()) if not gains.empty else float("nan"),
        "avg_loss": float(losses.mean()) if not losses.empty else float("nan"),
    }
