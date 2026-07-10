"""Tests for risk and performance metrics."""

import numpy as np
import pandas as pd
import pytest

from features.risk_metrics import (
    calculate_all_risk_metrics,
    calculate_annualized_return,
    calculate_beta,
    calculate_correlation_matrix,
    calculate_max_drawdown,
    calculate_returns,
    calculate_sharpe_ratio,
)


def test_calculate_returns():
    prices = pd.Series([100, 102, 101, 103, 105])

    returns = calculate_returns(prices)

    assert len(returns) == len(prices) - 1
    assert abs(returns.iloc[0] - 0.02) < 0.001


def test_annualized_return_compounds_period_returns():
    returns = pd.Series([0.01] * 252)

    result = calculate_annualized_return(returns)

    assert result == pytest.approx(1.01**252 - 1)


def test_max_drawdown_returns_peak_and_trough_dates():
    index = pd.date_range("2024-01-01", periods=6)
    prices = pd.Series([100, 110, 90, 95, 85, 100], index=index)

    max_drawdown, start, end = calculate_max_drawdown(prices)

    assert max_drawdown == pytest.approx(-0.22727, abs=0.001)
    assert start == index[1]
    assert end == index[4]


def test_sharpe_ratio_returns_float():
    returns = pd.Series([0.01, -0.005, 0.02, 0.015, -0.01] * 50)

    sharpe = calculate_sharpe_ratio(returns)

    assert isinstance(sharpe, float)
    assert np.isfinite(sharpe)


def test_beta_aligns_dates():
    dates = pd.date_range("2024-01-01", periods=5)
    market = pd.Series([0.008, 0.015, -0.005, 0.012, 0.003], index=dates)
    stock = market * 1.5

    beta = calculate_beta(stock, market)

    assert beta == pytest.approx(1.5)


def test_correlation_matrix_uses_ticker_labels():
    returns = pd.Series([0.01, 0.02, -0.01])

    matrix = calculate_correlation_matrix({"SPY": returns, "QQQ": returns * 2})

    assert list(matrix.columns) == ["SPY", "QQQ"]
    assert matrix.loc["SPY", "QQQ"] == pytest.approx(1.0)


def test_all_metrics_includes_beta_and_summary_fields():
    index = pd.date_range("2024-01-01", periods=6)
    benchmark = pd.Series([100, 101, 100, 102, 103, 104], index=index)
    prices = 100 * (benchmark / benchmark.iloc[0]) ** 1.2

    metrics = calculate_all_risk_metrics(prices, benchmark)

    expected = {
        "total_return",
        "ann_return",
        "ann_volatility",
        "max_drawdown",
        "sharpe_ratio",
        "sortino_ratio",
        "beta",
        "win_rate",
        "avg_gain",
        "avg_loss",
    }
    assert expected.issubset(metrics)
    assert metrics["beta"] is not None
