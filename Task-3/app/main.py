import pandas as pd
from app.schemas import (
    BatchPredictionRequest,
    OrderInput,
    PredictionResponse,
)
from fastapi import FastAPI
from src.model_loader import load_artifacts
from src.prediction import predict_order

app = FastAPI(
    title="Olist Late Delivery API",
    version="1.0.0",
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

    return result


@app.post("/predict-batch", response_model=list[PredictionResponse])
def predict_batch(batch: BatchPredictionRequest):
    data = pd.DataFrame([order.model_dump() for order in batch.orders])

    return predict_order(data)
