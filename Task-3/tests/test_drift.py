import json

import pytest

from src import drift_check


@pytest.mark.parametrize(
    ("late_count", "expected_message"),
    [
        (8, "OK: No drift alert triggered."),
        (30, "ALERT: Prediction distribution drift detected."),
    ],
)
def test_drift_detection(tmp_path, monkeypatch, capsys, late_count, expected_message):
    baseline_file = tmp_path / "baseline.json"
    prediction_log = tmp_path / "predictions.jsonl"

    baseline_file.write_text(
        json.dumps(
            {
                "model_version": 1,
                "late_prediction_rate": 0.083,
            }
        ),
        encoding="utf-8",
    )

    with prediction_log.open("w", encoding="utf-8") as file:
        for index in range(100):
            event = {
                "model_version": 1,
                "prediction": "late" if index < late_count else "on_time",
            }
            file.write(json.dumps(event) + "\n")

    monkeypatch.setattr(drift_check, "BASELINE_FILE", baseline_file)
    monkeypatch.setattr(drift_check, "PREDICTION_LOG", prediction_log)

    drift_check.main()

    assert expected_message in capsys.readouterr().out
