import logging
import time

from src.config import load_config
from src.gx_validation import validate_with_gx
from src.logging_config import setup_logging
from src.model_loader import load_artifacts
from src.preprocessing import preprocess_for_model
from src.validation import validate_input

setup_logging()
logger = logging.getLogger(__name__)


def predict_order(data):
    """Predict whether an order will be late or on time."""
    start_time = time.perf_counter()

    config = load_config()
    artifacts = load_artifacts()

    try:
        validate_input(data)
        validate_with_gx(data)
    except Exception:
        logger.error(
            "Input validation failed | input=%s",
            data.to_dict(orient="records"),
        )
        raise

    model = artifacts["model"]
    threshold = config["prediction"]["threshold"]
    model_version = artifacts["model_version"]

    features = preprocess_for_model(data, artifacts)

    late_probability = model.predict_proba(features)[:, 1]
    prediction = (late_probability >= threshold).astype(int)

    results = []

    for pred, probability in zip(prediction, late_probability):
        results.append(
            {
                "prediction": "late" if pred == 1 else "on_time",
                "probability": float(probability),
                "model_version": model_version,
            }
        )

    latency_ms = (time.perf_counter() - start_time) * 1000

    logger.info(
        "Prediction completed | input=%s | output=%s | latency_ms=%.2f | model_version=%s",
        data.to_dict(orient="records"),
        results,
        latency_ms,
        model_version,
    )

    return results
