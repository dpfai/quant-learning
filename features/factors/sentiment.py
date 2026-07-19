"""Convert structured NLP output into ticker/date factor panels."""
from __future__ import annotations

import pandas as pd


def sentiment_factor(records, weights: dict | None = None) -> pd.DataFrame:
    """Aggregate structured LLM records to a date-by-ticker factor matrix."""
    weights = weights or {"sentiment": 0.5, "forward_looking": 0.25, "certainty": 0.15, "impact": 0.10}
    frame = pd.DataFrame(records).copy()
    if frame.empty:
        return pd.DataFrame()
    missing = {"ticker", "date"} - set(frame.columns)
    if missing:
        raise ValueError(f"records missing required fields: {sorted(missing)}")
    frame["date"] = pd.to_datetime(frame["date"])
    frame["factor"] = sum(frame.get(column, 0.0) * weight for column, weight in weights.items())
    return frame.pivot_table(index="date", columns="ticker", values="factor", aggfunc="mean").sort_index()


def align_sentiment_to_dates(factor: pd.DataFrame, dates, max_age_days: int = 90) -> pd.DataFrame:
    """Forward-fill point-in-time sentiment without carrying stale values forever."""
    target = pd.DatetimeIndex(dates)
    return factor.reindex(factor.index.union(target)).sort_index().ffill(limit=max_age_days).reindex(target)
