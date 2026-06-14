"""Yahoo Finance market data provider."""
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
from utils.data_providers.base import DataProvider


class YFinanceProvider(DataProvider):
    """Yahoo Finance provider with local parquet caching."""

    REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]

    def __init__(
        self,
        cache_dir: str = DATA_CACHE_DIR,
        max_age_hours: int = CACHE_MAX_AGE_HOURS,
    ) -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_age_hours = max_age_hours
        self.cache_manager = CacheManager(str(self.cache_dir))

    @property
    def provider_name(self) -> str:
        return "yfinance"

    def fetch_ohlcv(
        self,
        ticker: str,
        period: str = DEFAULT_PERIOD,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        use_cache: bool = True,
    ) -> pd.DataFrame:
        """Fetch OHLCV data, using a fresh cache entry when requested."""
        cache_period = self._cache_period(period, start_date, end_date)

        if use_cache and self.is_cache_valid(ticker, period=cache_period):
            cached = self._load_from_cache(ticker, period=cache_period)
            if cached is not None:
                return cached

        download_kwargs = {
            "auto_adjust": False,
            "progress": False,
        }
        if start_date is not None or end_date is not None:
            download_kwargs.update(start=start_date, end=end_date)
        else:
            download_kwargs["period"] = period

        symbol = self._normalize_ticker(ticker)
        data = yf.download(symbol, **download_kwargs)
        data = self._prepare_dataframe(data)

        if data.empty:
            raise ValueError(f"No data returned for ticker: {ticker}")

        self._save_to_cache(ticker, data, period=cache_period)
        return data

    def fetch_batch(
        self,
        tickers: List[str],
        period: str = DEFAULT_PERIOD,
    ) -> Dict[str, pd.DataFrame]:
        """Fetch multiple tickers."""
        return {ticker: self.fetch_ohlcv(ticker, period=period) for ticker in tickers}

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
        """Clear cache for a ticker, or all cached parquet files."""
        if ticker is None:
            self.cache_manager.clear()
            return

        self.cache_manager.clear(f"{self._safe_ticker(ticker)}_*.parquet")

    def _load_from_cache(
        self,
        ticker: str,
        period: str = DEFAULT_PERIOD,
    ) -> Optional[pd.DataFrame]:
        path = self._cache_path(ticker, period)
        if not path.exists():
            return None
        return pd.read_parquet(path)

    def _save_to_cache(
        self,
        ticker: str,
        data: pd.DataFrame,
        period: str = DEFAULT_PERIOD,
    ) -> None:
        data.to_parquet(self._cache_path(ticker, period))

    def _cache_path(self, ticker: str, period: str = DEFAULT_PERIOD) -> Path:
        filename = CACHE_FILE_FORMAT.format(
            ticker=self._safe_ticker(ticker),
            period=self._safe_cache_value(period),
        )
        return self.cache_dir / filename

    def _normalize_ticker(self, ticker: str) -> str:
        normalized = ticker.strip().upper()
        return TICKER_ALIASES.get(normalized, normalized)

    def _safe_ticker(self, ticker: str) -> str:
        return ticker.strip().upper().replace("^", "").replace("/", "-")

    def _safe_cache_value(self, value: str) -> str:
        return value.replace("/", "-").replace(":", "-").replace(" ", "_")

    def _cache_period(
        self,
        period: str,
        start_date: Optional[str],
        end_date: Optional[str],
    ) -> str:
        if start_date is None and end_date is None:
            return period
        return f"{start_date or 'start'}_{end_date or 'end'}"

    def _prepare_dataframe(self, data: pd.DataFrame) -> pd.DataFrame:
        if data is None or data.empty:
            return pd.DataFrame(columns=self.REQUIRED_COLUMNS)

        prepared = data.copy()
        if isinstance(prepared.columns, pd.MultiIndex):
            prepared.columns = prepared.columns.get_level_values(0)

        prepared.index = pd.to_datetime(prepared.index)
        prepared = prepared.sort_index()

        if "Adj Close" not in prepared.columns and "Close" in prepared.columns:
            prepared["Adj Close"] = prepared["Close"]

        columns = [
            column
            for column in ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
            if column in prepared.columns
        ]
        return prepared[columns].dropna(
            subset=["Open", "High", "Low", "Close"],
            how="any",
        )
