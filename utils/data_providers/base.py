"""Abstract base class for market data providers."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

import pandas as pd


class DataProvider(ABC):
    """Abstract interface for market data providers."""

    @abstractmethod
    def fetch_ohlcv(
        self,
        ticker: str,
        period: str = "2y",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        use_cache: bool = True,
    ) -> pd.DataFrame:
        """Fetch OHLCV data for a single ticker."""

    @abstractmethod
    def fetch_batch(
        self,
        tickers: List[str],
        period: str = "2y",
    ) -> Dict[str, pd.DataFrame]:
        """Fetch OHLCV data for multiple tickers."""

    @abstractmethod
    def is_cache_valid(
        self,
        ticker: str,
        max_age_hours: Optional[int] = None,
        period: str = "2y",
    ) -> bool:
        """Return whether cached data is available and fresh."""

    @abstractmethod
    def clear_cache(self, ticker: Optional[str] = None) -> None:
        """Clear cached data for one ticker or all tickers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name."""
