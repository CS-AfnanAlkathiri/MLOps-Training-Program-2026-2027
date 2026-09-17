from time import perf_counter

import pandas as pd
from fastapi import FastAPI, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.monitoring import PREDICTION_COUNT, REQUEST_COUNT, REQUEST_LATENCY
from app.schemas import (
    BatchPredictionRequest,
    OrderInput,
    PredictionResponse,
)
from src.model_loader import load_artifacts
from src.prediction import predict_order

app = FastAPI(
    title="Olist Late Delivery API",
    version="1.0.0",
)


@app.middleware("http")
async def record_request_metrics(request: Request, call_next):
    start_time = perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        # Use the route template to avoid creating a new metric
        # for every unknown URL.
        route = request.scope.get("route")
        endpoint = route.path if route is not None else "unmatched"

        # Exclude Prometheus scrapes from application traffic metrics.
        if endpoint != "/metrics":
            REQUEST_COUNT.labels(
                endpoint=endpoint,
                method=request.method,
                status_code=str(status_code),
            ).inc()

            REQUEST_LATENCY.labels(
                endpoint=endpoint,
                method=request.method,
            ).observe(perf_counter() - start_time)


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/model-info")
def model_info():
    artifacts = load_artifacts()
    return {
        "model_name": "olist-late-delivery",
        "model_version": artifacts["model_version"],
        "alias": "champion",
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(order: OrderInput):
    data = pd.DataFrame([order.model_dump()])
    result = predict_order(data)[0]
    PREDICTION_COUNT.labels(prediction=result["prediction"]).inc()
    return result


@app.post("/predict-batch", response_model=list[PredictionResponse])
def predict_batch(batch: BatchPredictionRequest):
    data = pd.DataFrame([order.model_dump() for order in batch.orders])
    results = predict_order(data)

    for result in results:
        PREDICTION_COUNT.labels(prediction=result["prediction"]).inc()

    return results
