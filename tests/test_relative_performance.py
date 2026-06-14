"""Tests for relative performance calculations."""

import numpy as np
import pandas as pd
import pytest

from utils.relative_performance import (
    calculate_information_ratio,
    calculate_relative_performance,
    calculate_rolling_alpha,
    calculate_tracking_error,
)


def test_relative_performance_calculates_excess_returns():
    index = pd.date_range("2025-01-01", periods=70, freq="D")
    stock = pd.Series(np.linspace(100, 140, 70), index=index)
    benchmark = pd.Series(np.linspace(100, 120, 70), index=index)

    result = calculate_relative_performance(stock, benchmark)

    assert result["alpha_5d"] == pytest.approx(
        result["stock_5d"] - result["benchmark_5d"]
    )
    assert result["stock_60d"] > result["benchmark_60d"]
    assert result["alpha_ytd"] > 0


def test_short_history_returns_nan_for_unavailable_period():
    index = pd.date_range("2025-01-01", periods=10, freq="D")
    prices = pd.Series(range(100, 110), index=index)

    result = calculate_relative_performance(prices, prices)

    assert np.isnan(result["stock_20d"])


def test_tracking_error_and_information_ratio():
    index = pd.date_range("2025-01-01", periods=5)
    stock = pd.Series([0.01, 0.02, -0.01, 0.03, 0.00], index=index)
    benchmark = pd.Series([0.005, 0.01, -0.005, 0.01, 0.002], index=index)

    assert calculate_tracking_error(stock, benchmark) > 0
    assert np.isfinite(calculate_information_ratio(stock, benchmark))


def test_rolling_alpha_preserves_index():
    index = pd.date_range("2025-01-01", periods=30)
    stock = pd.Series(0.01, index=index)
    benchmark = pd.Series(0.005, index=index)

    alpha = calculate_rolling_alpha(stock, benchmark, window=20)

    assert alpha.index.equals(index)
    assert alpha.notna().sum() == 11
