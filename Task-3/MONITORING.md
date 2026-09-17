# Monitoring Plan

## 1. API Monitoring

The FastAPI application exposes Prometheus metrics at `/metrics`.

- `api_requests_total`: Counts requests by endpoint, method, and HTTP status.
- `api_request_duration_seconds`: Records request latency.
- HTTP 5xx responses can be used to calculate the server error rate.

Proposed operational alert thresholds:
- Error rate: Above 5% over a 5-minute window.
- Latency: 95th-percentile response time above 2 seconds for 5 minutes.

These thresholds are initial recommendations, not configured automatic
alerts. They should be adjusted using real traffic measurements.

## 2. Prediction Monitoring

`model_predictions_total` counts predictions classified as `late` or
`on_time`, including individual orders in batch requests.

Each prediction is also saved to `logs/prediction_events.jsonl` with:
- UTC timestamp
- Unique prediction ID
- Predicted outcome
- Late-delivery probability
- Model version

The prediction ID must be retained when an actual delivery outcome
becomes available so the prediction can be evaluated later.

Logs are local and excluded from Git. Production deployment requires
persistent, access-controlled storage.

## 3. Prediction Drift

The reference baseline uses 14,471 historical validation orders.

- Model version: 1
- Classification threshold: 0.70
- Baseline predicted late-delivery rate: approximately 8.30%
- Monitoring window: Latest 100 predictions from the baseline model version
- Alert threshold: Absolute difference of at least 10 percentage points

Run the checker:

    python -m src.drift_check

It reports insufficient data until 100 predictions are available.

A drift alert indicates a change in the prediction distribution.
It does not prove that model accuracy has decreased.

The drift threshold is an initial heuristic and should be reviewed
when sufficient production data becomes available.

## 4. Response to Alerts

When an alert occurs:
1. Check API errors, latency, and recent deployment changes.
2. Review prediction volumes and distribution changes.
3. Check input data quality and missing values.
4. Compare predictions with actual outcomes when available.
5. Investigate before deciding whether retraining is necessary.

The drift checker currently runs manually. Automatic scheduling,
notifications, and a monitoring dashboard are not yet configured.