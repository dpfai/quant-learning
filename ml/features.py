"""Leakage-aware feature engineering for market classification."""
from __future__ import annotations

from typing import List, Tuple

import numpy as np
import pandas as pd


def create_price_features(
    df: pd.DataFrame,
    windows: List[int] | None = None,
) -> pd.DataFrame:
    """Create trailing price, volatility, range, and volume features."""
    windows = windows or [5, 10, 20, 60]
    features = pd.DataFrame(index=df.index)
    daily_returns = df["Close"].pct_change(fill_method=None)

    for window in windows:
        rolling_mean = df["Close"].rolling(window).mean()
        features[f"return_{window}d"] = df["Close"].pct_change(
            window,
            fill_method=None,
        )
        features[f"volatility_{window}d"] = daily_returns.rolling(window).std()
        features[f"ma_dist_{window}d"] = (
            (df["Close"] - rolling_mean) / rolling_mean
        )
        features[f"high_low_ratio_{window}d"] = (
            df["High"].rolling(window).max() / df["Low"].rolling(window).min()
        )
        features[f"volume_change_{window}d"] = df["Volume"].pct_change(
            window,
            fill_method=None,
        )
    return features.replace([np.inf, -np.inf], np.nan)


def create_technical_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create trailing technical indicator features."""
    features = pd.DataFrame(index=df.index)
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
    features["rsi_14"] = 100 - (100 / (1 + avg_gain / avg_loss))

    ema_12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema_26 = df["Close"].ewm(span=26, adjust=False).mean()
    features["macd"] = ema_12 - ema_26
    features["macd_signal"] = features["macd"].ewm(span=9, adjust=False).mean()
    features["macd_hist"] = features["macd"] - features["macd_signal"]

    ma_20 = df["Close"].rolling(20).mean()
    std_20 = df["Close"].rolling(20).std()
    features["bb_position"] = (df["Close"] - ma_20) / (2 * std_20)

    previous_close = df["Close"].shift()
    true_range = pd.concat(
        [
            df["High"] - df["Low"],
            (df["High"] - previous_close).abs(),
            (df["Low"] - previous_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    features["atr_ratio"] = (
        true_range.ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
        / df["Close"]
    )
    return features.replace([np.inf, -np.inf], np.nan)


def create_target(
    df: pd.DataFrame,
    forward_days: int = 5,
    target_type: str = "binary",
) -> pd.Series:
    """Create a forward return, binary direction, or quantile target."""
    if forward_days < 1:
        raise ValueError("forward_days must be positive")
    future_return = df["Close"].shift(-forward_days) / df["Close"] - 1
    if target_type == "return":
        return future_return
    if target_type == "binary":
        target = (future_return > 0).astype(float)
        target[future_return.isna()] = np.nan
        return target
    if target_type == "bucket":
        return pd.qcut(future_return, 5, labels=False, duplicates="drop")
    raise ValueError(f"Unknown target type: {target_type}")


def prepare_ml_data(
    df: pd.DataFrame,
    forward_days: int = 5,
    test_ratio: float = 0.2,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Create features and perform a chronological train/test split."""
    if not 0 < test_ratio < 1:
        raise ValueError("test_ratio must be between 0 and 1")

    features = pd.concat(
        [create_price_features(df), create_technical_features(df)],
        axis=1,
    )
    target = create_target(df, forward_days, target_type="binary")
    valid = ~(features.isna().any(axis=1) | target.isna())
    features = features.loc[valid]
    target = target.loc[valid].astype(int)
    if len(features) < 10:
        raise ValueError("Not enough valid observations for ML training")

    split_index = int(len(features) * (1 - test_ratio))
    if split_index < 1 or split_index >= len(features):
        raise ValueError("Train/test split produced an empty partition")
    return (
        features.iloc[:split_index],
        features.iloc[split_index:],
        target.iloc[:split_index],
        target.iloc[split_index:],
    )


def create_latest_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return the most recent fully populated feature row for inference."""
    features = pd.concat(
        [create_price_features(df), create_technical_features(df)],
        axis=1,
    ).dropna()
    if features.empty:
        raise ValueError("Not enough history to create current features")
    return features.iloc[[-1]]
