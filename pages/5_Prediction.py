"""Educational machine-learning experiment page."""
from __future__ import annotations

import plotly.express as px
import streamlit as st

from ml.experiments import record_experiment
from ml.features import create_latest_features, prepare_ml_data
from ml.models import evaluate_model, get_feature_importance, get_model
from utils.data_loader import DataLoader


st.title("Prediction Experiments")
st.caption(
    "This page evaluates historical direction classification. "
    "It does not predict with certainty and is not financial advice."
)

ticker = st.text_input("Ticker", "SPY").strip().upper()
forward_days = st.slider("Prediction Horizon (trading days)", 1, 20, 5)
model_type = st.selectbox(
    "Model",
    ["random_forest", "logistic", "gradient_boost"],
)

if st.button("Train and Evaluate", type="primary"):
    try:
        with st.spinner("Preparing data and training model..."):
            data = DataLoader().download(ticker, period="5y")
            X_train, X_test, y_train, y_test = prepare_ml_data(
                data,
                forward_days=forward_days,
            )
            model = get_model(model_type)
            model.fit(X_train, y_train)
            metrics = evaluate_model(model, X_test, y_test)
            latest_features = create_latest_features(data)
            prediction = int(model.predict(latest_features)[0])
            probabilities = model.predict_proba(latest_features)[0]
            probability = float(probabilities[prediction])

        st.write(
            f"Training samples: {len(X_train)} | Test samples: {len(X_test)}"
        )
        columns = st.columns(4)
        for column, label, key in zip(
            columns,
            ["Accuracy", "Precision", "Recall", "F1 Score"],
            ["accuracy", "precision", "recall", "f1"],
        ):
            column.metric(label, f"{metrics[key]:.1%}")

        importance = get_feature_importance(model, X_train.columns.tolist())
        if importance is not None:
            st.subheader("Feature Importance")
            figure = px.bar(
                importance.head(15).sort_values("importance"),
                x="importance",
                y="feature",
                orientation="h",
            )
            st.plotly_chart(figure, use_container_width=True)

        st.subheader("Latest Model Output")
        message = (
            f"UP class ({probability:.1%} model probability)"
            if prediction == 1
            else f"DOWN class ({probability:.1%} model probability)"
        )
        st.info(message)
        st.caption(
            "Model probability is an experimental score based on historical data, "
            "not a calibrated forecast or recommendation."
        )

        record_experiment(
            f"{ticker}-{model_type}",
            {"forward_days": forward_days, "model": model_type},
            metrics,
        )
    except Exception as exc:
        st.error(f"Prediction experiment failed: {exc}")
