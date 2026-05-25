"""
Data loading module.

Downloads OHLCV market data with yfinance and stores a local parquet cache
to avoid repeated network requests during exploration.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
import yfinance as yf

from config.settings import (
    CACHE_FILE_FORMAT,
    CACHE_MAX_AGE_HOURS,
    DATA_CACHE_DIR,
    DEFAULT_PERIOD,
    TICKER_ALIASES,
)
from utils.cache_manager import CacheManager


class DataLoader:
    """Download and cache OHLCV data for one or more tickers."""

    REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]

    def __init__(self, cache_dir: str = DATA_CACHE_DIR, max_age_hours: int = CACHE_MAX_AGE_HOURS) -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_age_hours = max_age_hours
        self.cache_manager = CacheManager(str(self.cache_dir))

    def download(self, ticker: str, period: str = DEFAULT_PERIOD, use_cache: bool = True) -> pd.DataFrame:
        """Download a single ticker, using cache first when available."""
        symbol = self._normalize_ticker(ticker)

        if use_cache and self.is_cache_valid(ticker, period=period):
            cached = self._load_from_cache(ticker, period=period)
            if cached is not None:
                return cached

        df = yf.download(symbol, period=period, auto_adjust=False, progress=False)
        df = self._prepare_dataframe(df)

        if df.empty:
            raise ValueError(f"No data returned for ticker: {ticker}")

        self._save_to_cache(ticker, df, period=period)
        return df

    def download_batch(self, tickers: List[str], period: str = DEFAULT_PERIOD) -> Dict[str, pd.DataFrame]:
        """Download multiple tickers and return a ticker-to-DataFrame mapping."""
        return {ticker: self.download(ticker, period=period) for ticker in tickers}

    def _load_from_cache(self, ticker: str, period: str = DEFAULT_PERIOD) -> Optional[pd.DataFrame]:
        """Load cached ticker data from parquet."""
        path = self._cache_path(ticker, period)
        if not path.exists():
            return None
        return pd.read_parquet(path)

    def _save_to_cache(self, ticker: str, df: pd.DataFrame, period: str = DEFAULT_PERIOD) -> None:
        """Save ticker data to parquet cache."""
        df.to_parquet(self._cache_path(ticker, period))

    def is_cache_valid(
        self,
        ticker: str,
        max_age_hours: Optional[int] = None,
        period: str = DEFAULT_PERIOD,
    ) -> bool:
        """Check whether cached data exists and is not expired."""
        age_hours = max_age_hours if max_age_hours is not None else self.max_age_hours
        return self.cache_manager.is_valid(self._cache_path(ticker, period), age_hours)

    def clear_cache(self, ticker: Optional[str] = None) -> None:
        """Clear cache for a ticker, or clear all cached parquet files."""
        if ticker is None:
            self.cache_manager.clear()
            return

        safe_ticker = self._safe_ticker(ticker)
        self.cache_manager.clear(f"{safe_ticker}_*.parquet")

    def _cache_path(self, ticker: str, period: str = DEFAULT_PERIOD) -> Path:
        filename = CACHE_FILE_FORMAT.format(ticker=self._safe_ticker(ticker), period=period)
        return self.cache_dir / filename

    def _normalize_ticker(self, ticker: str) -> str:
        normalized = ticker.strip().upper()
        return TICKER_ALIASES.get(normalized, normalized)

    def _safe_ticker(self, ticker: str) -> str:
        return ticker.strip().upper().replace("^", "").replace("/", "-")

    def _prepare_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        if df is None or df.empty:
            return pd.DataFrame(columns=self.REQUIRED_COLUMNS)

        data = df.copy()
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data.index = pd.to_datetime(data.index)
        data = data.sort_index()

        if "Adj Close" not in data.columns and "Close" in data.columns:
            data["Adj Close"] = data["Close"]

        columns = [col for col in ["Open", "High", "Low", "Close", "Adj Close", "Volume"] if col in data.columns]
        return data[columns].dropna(subset=["Open", "High", "Low", "Close"], how="any")
