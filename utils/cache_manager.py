"""
Cache management helpers for local market data.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional


class CacheManager:
    """Manage file-based cache freshness and cleanup."""

    def __init__(self, cache_dir: str = "data/cache") -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def is_valid(self, path: Path, max_age_hours: int = 24) -> bool:
        """Return True when a cache file exists and is not expired."""
        if not path.exists():
            return False

        modified_at = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        return datetime.now(timezone.utc) - modified_at <= timedelta(hours=max_age_hours)

    def clear(self, pattern: Optional[str] = None) -> None:
        """Delete cache files matching a pattern, or all parquet cache files."""
        file_pattern = pattern or "*.parquet"
        for path in self.cache_dir.glob(file_pattern):
            if path.is_file():
                path.unlink()
