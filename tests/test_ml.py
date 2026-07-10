"""Tests for ML feature engineering and model helpers."""

import numpy as np
import pandas as pd

from ml.features import create_target, prepare_ml_data
from ml.models import evaluate_model, get_feature_importance, get_model
from ml.validation import walk_forward_validate


def sample_frame(rows: int = 320) -> pd.DataFrame:
    index = pd.date_range("2020-01-01", periods=rows, freq="D")
    trend = np.linspace(100, 180, rows)
    cycle = np.sin(np.arange(rows) / 5) * 3
    close = pd.Series(trend + cycle, index=index)
    return pd.DataFrame(
        {
            "Open": close - 0.5,
            "High": close + 1,
            "Low": close - 1,
            "Close": close,
            "Volume": 1_000 + np.arange(rows) * 10,
        },
        index=index,
    )


def test_target_drops_unknown_future_values():
    target = create_target(sample_frame(), forward_days=5)

    assert target.tail(5).isna().all()


def test_prepare_ml_data_is_chronological():
    X_train, X_test, y_train, y_test = prepare_ml_data(sample_frame())

    assert X_train.index.max() < X_test.index.min()
    assert X_train.index.equals(y_train.index)
    assert X_test.index.equals(y_test.index)


def test_models_train_evaluate_and_report_importance():
    X_train, X_test, y_train, y_test = prepare_ml_data(sample_frame())
    model = get_model("random_forest")
    model.fit(X_train, y_train)

    metrics = evaluate_model(model, X_test, y_test)
    importance = get_feature_importance(model, X_train.columns.tolist())

    assert set(metrics) == {"accuracy", "precision", "recall", "f1"}
    assert importance is not None
    assert len(importance) == X_train.shape[1]


def test_walk_forward_validation_returns_each_fold():
    X_train, X_test, y_train, y_test = prepare_ml_data(sample_frame())
    features = pd.concat([X_train, X_test])
    target = pd.concat([y_train, y_test])

    result = walk_forward_validate(get_model("logistic"), features, target, splits=3)

    assert list(result["fold"]) == [1, 2, 3]
