import json
from collections import deque

from src.config import PROJECT_ROOT

BASELINE_FILE = PROJECT_ROOT / "config" / "drift_baseline.json"
PREDICTION_LOG = PROJECT_ROOT / "logs" / "prediction_events.jsonl"

WINDOW_SIZE = 100
ALERT_THRESHOLD = 0.10


def main():
    with BASELINE_FILE.open("r", encoding="utf-8") as file:
        baseline = json.load(file)

    if not PREDICTION_LOG.exists():
        print("INSUFFICIENT DATA: No prediction logs found.")
        return

    recent_predictions = deque(maxlen=WINDOW_SIZE)

    with PREDICTION_LOG.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            event = json.loads(line)

            if event["model_version"] == baseline["model_version"]:
                recent_predictions.append(event)

    count = len(recent_predictions)

    if count < WINDOW_SIZE:
        print(f"INSUFFICIENT DATA: {count}/{WINDOW_SIZE} predictions available.")
        return

    late_count = sum(event["prediction"] == "late" for event in recent_predictions)

    current_rate = late_count / count
    baseline_rate = baseline["late_prediction_rate"]
    difference = abs(current_rate - baseline_rate)

    print(f"Baseline late prediction rate: {baseline_rate:.2%}")
    print(f"Current late prediction rate:  {current_rate:.2%}")
    print(f"Absolute difference:          {difference:.2%}")

    if difference >= ALERT_THRESHOLD:
        print("ALERT: Prediction distribution drift detected.")
    else:
        print("OK: No drift alert triggered.")


if __name__ == "__main__":
    main()
