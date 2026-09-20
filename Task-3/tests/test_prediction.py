import pandas as pd

from src.prediction import predict_order


def test_prediction_output():
    data = pd.read_csv("data/sample_order.csv")

    result = predict_order(data)

    assert isinstance(result, list)
    assert len(result) == 1

    prediction = result[0]

    assert prediction["prediction"] in ["late", "on_time"]
    assert 0.0 <= prediction["probability"] <= 1.0
    assert prediction["model_version"] == 1


def test_task2_task3_model_parity(monkeypatch):
    import json
    from pathlib import Path

    import joblib
    import pytest

    from src.config import load_config
    from src.model_loader import load_artifacts
    from src.preprocessing import preprocess_for_model

    # Use Task 3's local model so the test does not require MLflow.
    monkeypatch.setenv("MODEL_SOURCE", "local")

    task2_artifacts = Path(__file__).resolve().parents[2] / "Task-2" / "artifacts"

    task2_model = joblib.load(task2_artifacts / "final_logistic_regression.joblib")

    with open(
        task2_artifacts / "final_model_results.json",
        encoding="utf-8",
    ) as file:
        task2_results = json.load(file)

    data = pd.read_csv("data/sample_order.csv")
    artifacts = load_artifacts()
    features = preprocess_for_model(data, artifacts)

    task2_probability = task2_model.predict_proba(features)[:, 1][0]
    task3_probability = artifacts["model"].predict_proba(features)[:, 1][0]

    assert task3_probability == pytest.approx(
        task2_probability,
        abs=1e-10,
    )

    assert load_config()["prediction"]["threshold"] == pytest.approx(
        task2_results["threshold"]
    )

    task2_prediction = (
        "late" if task2_probability >= task2_results["threshold"] else "on_time"
    )

    task3_prediction = predict_order(data)[0]["prediction"]

    assert task3_prediction == task2_prediction
