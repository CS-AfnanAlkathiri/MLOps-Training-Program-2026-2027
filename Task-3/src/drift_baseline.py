import json
from datetime import datetime, timezone

import pandas as pd

from src.config import PROJECT_ROOT, load_config
from src.model_loader import load_artifacts
from src.preprocessing import preprocess_for_model


def main():
    validation_path = PROJECT_ROOT.parent / "Task-2" / "artifacts" / "validation.csv"
    output_path = PROJECT_ROOT / "config" / "drift_baseline.json"

    data = pd.read_csv(validation_path)

    config = load_config()
    artifacts = load_artifacts()

    features = preprocess_for_model(data, artifacts)

    probabilities = artifacts["model"].predict_proba(features)[:, 1]

    threshold = config["prediction"]["threshold"]
    predictions = probabilities >= threshold

    baseline = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "model_version": artifacts["model_version"],
        "threshold": threshold,
        "sample_size": len(data),
        "late_prediction_rate": float(predictions.mean()),
        "mean_late_probability": float(probabilities.mean()),
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(baseline, file, indent=2)

    print("Drift baseline created successfully.")
    print(json.dumps(baseline, indent=2))


if __name__ == "__main__":
    main()
