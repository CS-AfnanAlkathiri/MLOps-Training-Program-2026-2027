import json
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

from src.config import PROJECT_ROOT

LOG_FILE = PROJECT_ROOT / "logs" / "prediction_events.jsonl"
WRITE_LOCK = Lock()


def save_prediction_event(result: dict) -> None:
    """Save one prediction per line for future evaluation."""
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prediction_id": result["prediction_id"],
        "prediction": result["prediction"],
        "probability": result["probability"],
        "model_version": result["model_version"],
    }

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with WRITE_LOCK, Path(LOG_FILE).open("a", encoding="utf-8") as file:
        file.write(json.dumps(event) + "\n")
