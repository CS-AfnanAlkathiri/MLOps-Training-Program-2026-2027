import json
import os

import joblib
import mlflow.sklearn
from mlflow import MlflowClient
from src.config import PROJECT_ROOT, load_config


def load_artifacts():
    """Load the model and fitted preprocessing artifacts."""
    config = load_config()
    paths = config["paths"]

    if os.getenv("MODEL_SOURCE") == "local":
        # Unit tests can use the existing model without Docker or MLflow.
        model = joblib.load(PROJECT_ROOT / paths["model"])
        model_version = 1
    else:
        # Production loads the registered champion model from MLflow.
        client = MlflowClient()
        registered_model = client.get_model_version_by_alias(
            "olist-late-delivery", "champion"
        )
        model = mlflow.sklearn.load_model("models:/olist-late-delivery@champion")
        model_version = int(registered_model.version)

    imputer = joblib.load(PROJECT_ROOT / paths["imputer"])
    encoder = joblib.load(PROJECT_ROOT / paths["encoder"])
    scaler = joblib.load(PROJECT_ROOT / paths["scaler"])

    with open(PROJECT_ROOT / paths["feature_list"], "r", encoding="utf-8") as file:
        feature_list = json.load(file)

    return {
        "model": model,
        "imputer": imputer,
        "encoder": encoder,
        "scaler": scaler,
        "feature_list": feature_list,
        "model_version": model_version,
    }
