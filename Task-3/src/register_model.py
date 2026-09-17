import json

import joblib
import mlflow
import mlflow.sklearn

from src.config import PROJECT_ROOT, load_config


def register_model():
    """Log and register the existing Task 2 model in MLflow."""
    config = load_config()

    model_path = PROJECT_ROOT / config["paths"]["model"]
    results_path = PROJECT_ROOT / config["paths"]["model_results"]

    model = joblib.load(model_path)

    with open(results_path, "r", encoding="utf-8") as file:
        results = json.load(file)

    mlflow.set_experiment("olist-late-delivery")

    with mlflow.start_run():
        mlflow.log_param("prediction_threshold", config["prediction"]["threshold"])

        for key, value in results.items():
            if isinstance(value, (int, float)):
                mlflow.log_metric(key, value)

        mlflow.sklearn.log_model(
            sk_model=model, name="model", registered_model_name="olist-late-delivery"
        )


if __name__ == "__main__":
    register_model()
