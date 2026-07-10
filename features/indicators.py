"""
Technical indicator calculations.
"""
from __future__ import annotations

import pandas as pd


def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add the standard indicator set used by the dashboard."""
    data = df.copy()
    data = add_moving_averages(data)
    data = add_rsi(data)
    data = add_macd(data)
    data = add_bollinger_bands(data)
    data = add_atr(data)
    return data


def add_moving_averages(df: pd.DataFrame, periods: list[int] | None = None) -> pd.DataFrame:
    """Add simple moving averages for the requested periods."""
    data = df.copy()
    periods = periods or [20, 50, 200]
    for period in periods:
        data[f"MA{period}"] = data["Close"].rolling(window=period, min_periods=period).mean()
    return data


def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Add Relative Strength Index."""
    data = df.copy()
    delta = data["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss
    data[f"RSI{period}"] = 100 - (100 / (1 + rs))
    data.loc[avg_loss == 0, f"RSI{period}"] = 100
    data[f"RSI{period}"] = data[f"RSI{period}"].clip(lower=0, upper=100)
    return data


def add_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """Add MACD line, signal line, and histogram."""
    data = df.copy()
    ema_fast = data["Close"].ewm(span=fast, adjust=False).mean()
    ema_slow = data["Close"].ewm(span=slow, adjust=False).mean()
    data["MACD"] = ema_fast - ema_slow
    data["MACD_signal"] = data["MACD"].ewm(span=signal, adjust=False).mean()
    data["MACD_hist"] = data["MACD"] - data["MACD_signal"]
    return data


def add_bollinger_bands(df: pd.DataFrame, period: int = 20, std_dev: float = 2) -> pd.DataFrame:
    """Add Bollinger Band middle, upper, lower, and width columns."""
    data = df.copy()
    middle = data["Close"].rolling(window=period, min_periods=period).mean()
    rolling_std = data["Close"].rolling(window=period, min_periods=period).std()
    data["BB_middle"] = middle
    data["BB_upper"] = middle + std_dev * rolling_std
    data["BB_lower"] = middle - std_dev * rolling_std
    data["BB_width"] = (data["BB_upper"] - data["BB_lower"]) / middle
    return data


def add_atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Add Average True Range."""
    data = df.copy()
    high_low = data["High"] - data["Low"]
    high_close = (data["High"] - data["Close"].shift()).abs()
    low_close = (data["Low"] - data["Close"].shift()).abs()
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    data[f"ATR{period}"] = true_range.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    return data
