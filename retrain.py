"""Retrain weekly ML models used by the Quant Learning Trading Arena source."""
from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path

import joblib
import pandas as pd

from ml.features import create_price_features, create_target, create_technical_features
from ml.models import get_model
from ml.validation import walk_forward_validate
from trading_arena_common import TRADE_TICKERS, download_history


MODEL_DIR = Path("ml/trained_models")


def prepare_full_dataset(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Create a full leakage-aware feature/target set for retraining."""
    features = pd.concat(
        [create_price_features(frame), create_technical_features(frame)],
        axis=1,
    )
    target = create_target(frame, forward_days=5, target_type="binary")
    valid = ~(features.isna().any(axis=1) | target.isna())
    return features.loc[valid], target.loc[valid].astype(int)


def main() -> None:
    parser = argparse.ArgumentParser(description="Retrain Trading Arena ML models.")
    parser.add_argument("--end", default=date.today().isoformat())
    parser.add_argument("--model-dir", default=str(MODEL_DIR))
    parser.add_argument("--splits", type=int, default=5)
    args = parser.parse_args()

    end = date.fromisoformat(args.end)
    start = end - timedelta(days=900)
    model_dir = Path(args.model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)
    history = download_history(TRADE_TICKERS, start=start, end=end, warmup_days=0)
    metrics = {}

    for ticker, frame in history.items():
        features, target = prepare_full_dataset(frame)
        model = get_model("random_forest")
        validation = walk_forward_validate(model, features, target, splits=args.splits)
        model.fit(features, target)
        model_path = model_dir / f"{ticker}_random_forest.joblib"
        joblib.dump(model, model_path)
        metrics[ticker] = {
            "rows": int(len(features)),
            "model_path": str(model_path),
            "walk_forward": validation.to_dict(orient="records"),
            "mean_f1": float(validation["f1"].mean()),
        }

    metrics_path = model_dir / "training_metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Retrained {len(metrics)} models and wrote metrics to {metrics_path}")


if __name__ == "__main__":
    main()
