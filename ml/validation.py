"""Time-series validation helpers."""
from __future__ import annotations

import pandas as pd
from sklearn.base import clone
from sklearn.model_selection import TimeSeriesSplit

from ml.models import evaluate_model


def walk_forward_validate(
    model,
    features: pd.DataFrame,
    target: pd.Series,
    splits: int = 5,
) -> pd.DataFrame:
    """Evaluate expanding-window time-series splits."""
    if splits < 2:
        raise ValueError("splits must be at least 2")
    rows = []
    splitter = TimeSeriesSplit(n_splits=splits)
    for fold, (train_indices, test_indices) in enumerate(
        splitter.split(features),
        start=1,
    ):
        fold_model = clone(model)
        fold_model.fit(features.iloc[train_indices], target.iloc[train_indices])
        metrics = evaluate_model(
            fold_model,
            features.iloc[test_indices],
            target.iloc[test_indices],
        )
        rows.append({"fold": fold, **metrics})
    return pd.DataFrame(rows)
