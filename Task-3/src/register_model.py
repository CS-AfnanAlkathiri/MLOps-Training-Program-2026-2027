import json

import joblib
import mlflow
import mlflow.sklearn
from mlflow import MlflowClient

from src.config import PROJECT_ROOT, load_config


def register_model():
    """Register the model once and ensure the champion alias exists."""
    config = load_config()
    model_name = "olist-late-delivery"

    client = MlflowClient()
    versions = list(client.search_model_versions(f"name='{model_name}'"))

    # If champion already exists, do not register another version.
    for version in versions:
        if "champion" in version.aliases:
            print(f"Champion already exists: {model_name} version {version.version}")
            return

    # An existing model may be registered without an alias.
    if versions:
        latest = max(versions, key=lambda item: int(item.version))
        client.set_registered_model_alias(
            model_name,
            "champion",
            latest.version,
        )
        print(f"Assigned champion alias to version {latest.version}.")
        return

    # On a fresh registry, register the saved Task 2 model.
    model_path = PROJECT_ROOT / config["paths"]["model"]
    results_path = PROJECT_ROOT / config["paths"]["model_results"]

    model = joblib.load(model_path)

    with results_path.open("r", encoding="utf-8") as file:
        results = json.load(file)

    mlflow.set_experiment(model_name)

    with mlflow.start_run():
        mlflow.log_param(
            "prediction_threshold",
            config["prediction"]["threshold"],
        )

        for key, value in results.items():
            if isinstance(value, (int, float)):
                mlflow.log_metric(key, value)

        mlflow.sklearn.log_model(
            sk_model=model,
            name="model",
            registered_model_name=model_name,
        )

    versions = list(client.search_model_versions(f"name='{model_name}'"))

    if not versions:
        raise RuntimeError("Model registration failed.")

    latest = max(versions, key=lambda item: int(item.version))

    client.set_registered_model_alias(
        model_name,
        "champion",
        latest.version,
    )

    print(f"Registered {model_name} version {latest.version} as champion.")


if __name__ == "__main__":
    register_model()
