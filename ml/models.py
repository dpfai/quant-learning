"""Model construction, evaluation, and feature importance."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def get_model(model_type: str = "random_forest"):
    """Return a deterministic classifier for the requested model type."""
    if model_type == "logistic":
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(max_iter=1000, random_state=42)),
            ]
        )
    if model_type == "random_forest":
        return RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
        )
    if model_type == "gradient_boost":
        return GradientBoostingClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=42,
        )
    raise ValueError(f"Unknown model type: {model_type}")


def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """Evaluate binary classification predictions."""
    predictions = model.predict(X_test)
    return {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(precision_score(y_test, predictions, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, zero_division=0)),
        "f1": float(f1_score(y_test, predictions, zero_division=0)),
    }


def get_feature_importance(
    model,
    feature_names: list[str],
) -> pd.DataFrame | None:
    """Return absolute model feature importance when available."""
    if hasattr(model, "feature_importances_"):
        importance = model.feature_importances_
    elif hasattr(model, "named_steps") and "model" in model.named_steps:
        importance = model.named_steps["model"].coef_[0]
    else:
        return None
    return pd.DataFrame(
        {
            "feature": feature_names,
            "importance": np.abs(importance),
        }
    ).sort_values("importance", ascending=False)
