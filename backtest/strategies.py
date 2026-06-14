"""Signal generators for educational backtests."""
from __future__ import annotations

import pandas as pd

from features.indicators import add_rsi


def ma_crossover_signal(
    df: pd.DataFrame,
    fast_period: int = 20,
    slow_period: int = 50,
) -> pd.Series:
    """Return long/short signals from a moving-average crossover."""
    if fast_period >= slow_period:
        raise ValueError("fast_period must be less than slow_period")
    fast_ma = df["Close"].rolling(fast_period).mean()
    slow_ma = df["Close"].rolling(slow_period).mean()
    signal = pd.Series(0.0, index=df.index)
    signal[fast_ma > slow_ma] = 1.0
    signal[fast_ma < slow_ma] = -1.0
    return signal


def rsi_mean_reversion_signal(
    df: pd.DataFrame,
    rsi_period: int = 14,
    oversold: float = 30,
    overbought: float = 70,
) -> pd.Series:
    """Buy oversold readings and sell overbought readings."""
    data = add_rsi(df, period=rsi_period)
    rsi = data[f"RSI{rsi_period}"]
    signal = pd.Series(0.0, index=df.index)
    signal[rsi < oversold] = 1.0
    signal[rsi > overbought] = -1.0
    return signal


def bollinger_band_signal(
    df: pd.DataFrame,
    period: int = 20,
    std_dev: float = 2,
) -> pd.Series:
    """Buy below the lower band and sell above the upper band."""
    moving_average = df["Close"].rolling(period).mean()
    rolling_std = df["Close"].rolling(period).std()
    upper = moving_average + std_dev * rolling_std
    lower = moving_average - std_dev * rolling_std
    signal = pd.Series(0.0, index=df.index)
    signal[df["Close"] < lower] = 1.0
    signal[df["Close"] > upper] = -1.0
    return signal
