from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total number of API requests.",
    ["endpoint", "method", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "api_request_duration_seconds",
    "Time spent processing API requests.",
    ["endpoint", "method"],
)

PREDICTION_COUNT = Counter(
    "model_predictions_total",
    "Total number of predictions by predicted outcome.",
    ["prediction"],
)
