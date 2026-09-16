import pandas as pd

from src.model_loader import load_artifacts
from src.preprocessing import preprocess_for_model


def test_preprocessing_output_shape_and_columns():
    data = pd.read_csv("data/sample_order.csv")

    artifacts = load_artifacts()
    processed = preprocess_for_model(data, artifacts)

    assert processed.shape == (1, 64)
    assert list(processed.columns) == artifacts["feature_list"]


def test_preprocessing_has_no_missing_values():
    data = pd.read_csv("data/sample_order.csv")

    artifacts = load_artifacts()
    processed = preprocess_for_model(data, artifacts)

    assert processed.isna().sum().sum() == 0
