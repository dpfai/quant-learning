"""Tests for strategies and the backtest engine."""

import pandas as pd
import pytest

from backtest.engine import BacktestEngine
from backtest.strategies import (
    bollinger_band_signal,
    ma_crossover_signal,
    rsi_mean_reversion_signal,
)


def sample_frame(rows: int = 100) -> pd.DataFrame:
    index = pd.date_range("2024-01-01", periods=rows)
    close = pd.Series(range(100, 100 + rows), index=index, dtype=float)
    return pd.DataFrame(
        {
            "Open": close,
            "High": close + 1,
            "Low": close - 1,
            "Close": close,
            "Volume": 1000,
        }
    )


def test_ma_signal_validates_periods():
    with pytest.raises(ValueError, match="fast_period"):
        ma_crossover_signal(sample_frame(), fast_period=50, slow_period=20)


def test_strategies_return_aligned_signals():
    data = sample_frame()

    for signal in [
        ma_crossover_signal(data),
        rsi_mean_reversion_signal(data),
        bollinger_band_signal(data),
    ]:
        assert signal.index.equals(data.index)
        assert set(signal.unique()).issubset({-1.0, 0.0, 1.0})


def test_engine_shifts_signal_to_avoid_lookahead():
    index = pd.date_range("2024-01-01", periods=4)
    prices = pd.Series([100, 110, 121, 133.1], index=index)
    signals = pd.Series([1, 1, 1, 1], index=index)

    result = BacktestEngine(commission=0, slippage=0).run(prices, signals)

    assert result["positions"].iloc[0] == 0
    assert result["positions"].iloc[1] == 1
    assert result["equity_curve"].iloc[0] == pytest.approx(100_000)
    assert result["equity_curve"].iloc[-1] == pytest.approx(133_100)


def test_costs_reduce_equity_and_trades_are_counted():
    index = pd.date_range("2024-01-01", periods=4)
    prices = pd.Series([100, 100, 100, 100], index=index)
    signals = pd.Series([1, -1, 0, 0], index=index)

    result = BacktestEngine(commission=0.001, slippage=0).run(prices, signals)

    assert result["equity_curve"].iloc[-1] < 100_000
    assert result["metrics"]["num_trades"] == 3
