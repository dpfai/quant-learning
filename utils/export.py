"""Data export helpers."""
from __future__ import annotations

import pandas as pd


def dataframe_to_csv(data: pd.DataFrame, include_index: bool = True) -> bytes:
    """Serialize a DataFrame as UTF-8 CSV bytes."""
    return data.to_csv(index=include_index).encode("utf-8")
