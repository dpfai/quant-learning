"""Unified market data loading interface."""
from __future__ import annotations

from typing import Dict, List, Optional

import pandas as pd

from config.settings import DEFAULT_PERIOD
from utils.data_providers.base import DataProvider
from utils.data_providers.yfinance_provider import YFinanceProvider


class DataLoader:
    """Provider-independent facade for loading market data."""

    def __init__(self, provider: str = "yfinance", **provider_kwargs) -> None:
        self._provider = self._get_provider(provider, **provider_kwargs)

    @property
    def provider_name(self) -> str:
        """Return the active provider name."""
        return self._provider.provider_name

    def _get_provider(self, name: str, **kwargs) -> DataProvider:
        normalized_name = name.strip().lower()
        if normalized_name == "yfinance":
            return YFinanceProvider(**kwargs)
        raise ValueError(f"Unknown provider: {name}")

    def download(
        self,
        ticker: str,
        period: str = DEFAULT_PERIOD,
        use_cache: bool = True,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """Download data for a single ticker."""
        return self._provider.fetch_ohlcv(
            ticker,
            period=period,
            start_date=start_date,
            end_date=end_date,
            use_cache=use_cache,
        )

    def download_batch(
        self,
        tickers: List[str],
        period: str = DEFAULT_PERIOD,
    ) -> Dict[str, pd.DataFrame]:
        """Download data for multiple tickers."""
        return self._provider.fetch_batch(tickers, period=period)

    def is_cache_valid(
        self,
        ticker: str,
        max_age_hours: Optional[int] = None,
        period: str = DEFAULT_PERIOD,
    ) -> bool:
        """Check whether the active provider has fresh cached data."""
        return self._provider.is_cache_valid(ticker, max_age_hours, period)

    def clear_cache(self, ticker: Optional[str] = None) -> None:
        """Clear cached data through the active provider."""
        self._provider.clear_cache(ticker)
