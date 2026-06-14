"""Persistent JSON-backed watchlist management."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional


class WatchlistManager:
    """Create and maintain named ticker watchlists."""

    DEFAULT_WATCHLISTS = {
        "Tech Growth": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META"],
        "ETFs": ["SPY", "QQQ", "DIA", "IWM"],
        "Sectors": ["XLK", "XLF", "XLV", "XLE", "XLY"],
    }

    def __init__(self, storage_path: str = "data/watchlists.json") -> None:
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self._save(self.DEFAULT_WATCHLISTS.copy())

    def _load(self) -> Dict[str, List[str]]:
        try:
            with self.storage_path.open(encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError):
            data = self.DEFAULT_WATCHLISTS.copy()
            self._save(data)
        return {
            str(name): [self._normalize_ticker(ticker) for ticker in tickers]
            for name, tickers in data.items()
        }

    def _save(self, watchlists: Dict[str, List[str]]) -> None:
        with self.storage_path.open("w", encoding="utf-8") as file:
            json.dump(watchlists, file, indent=2, sort_keys=True)

    def _normalize_ticker(self, ticker: str) -> str:
        normalized = ticker.strip().upper()
        if not normalized:
            raise ValueError("Ticker cannot be empty")
        return normalized

    def get_watchlist(self, name: str) -> List[str]:
        """Return a copy of a named watchlist."""
        watchlists = self._load()
        if name not in watchlists:
            raise KeyError(f"Unknown watchlist: {name}")
        return list(watchlists[name])

    def add_ticker(self, watchlist_name: str, ticker: str) -> None:
        """Add a normalized ticker unless it is already present."""
        watchlists = self._load()
        if watchlist_name not in watchlists:
            raise KeyError(f"Unknown watchlist: {watchlist_name}")
        normalized = self._normalize_ticker(ticker)
        if normalized not in watchlists[watchlist_name]:
            watchlists[watchlist_name].append(normalized)
            self._save(watchlists)

    def remove_ticker(self, watchlist_name: str, ticker: str) -> None:
        """Remove a ticker when present."""
        watchlists = self._load()
        if watchlist_name not in watchlists:
            raise KeyError(f"Unknown watchlist: {watchlist_name}")
        normalized = self._normalize_ticker(ticker)
        watchlists[watchlist_name] = [
            item for item in watchlists[watchlist_name] if item != normalized
        ]
        self._save(watchlists)

    def create_watchlist(
        self,
        name: str,
        tickers: Optional[List[str]] = None,
    ) -> None:
        """Create a new uniquely named watchlist."""
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("Watchlist name cannot be empty")
        watchlists = self._load()
        if clean_name in watchlists:
            raise ValueError(f"Watchlist already exists: {clean_name}")
        normalized = []
        for ticker in tickers or []:
            value = self._normalize_ticker(ticker)
            if value not in normalized:
                normalized.append(value)
        watchlists[clean_name] = normalized
        self._save(watchlists)

    def delete_watchlist(self, name: str) -> None:
        """Delete a named watchlist."""
        watchlists = self._load()
        if name not in watchlists:
            raise KeyError(f"Unknown watchlist: {name}")
        del watchlists[name]
        self._save(watchlists)

    def list_watchlists(self) -> List[str]:
        """List watchlist names alphabetically."""
        return sorted(self._load())
