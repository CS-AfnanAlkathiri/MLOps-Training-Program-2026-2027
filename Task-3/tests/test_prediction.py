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
