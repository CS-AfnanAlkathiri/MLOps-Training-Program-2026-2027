from datetime import datetime

from pydantic import BaseModel, Field


class OrderInput(BaseModel):
    order_purchase_timestamp: datetime
    order_estimated_delivery_date: datetime
    customer_state: str
    seller_state: str
    item_count: float = Field(ge=0)
    total_price: float = Field(ge=0)
    total_freight_value: float = Field(ge=0)
    unique_products: float = Field(ge=0)
    unique_sellers: float = Field(ge=0)
    payment_count: float = Field(ge=0)
    total_payment_value: float = Field(ge=0)
    max_installments: float = Field(ge=0)
    payment_type_count: float = Field(ge=0)
    distance_km: float = Field(ge=0)


class BatchPredictionRequest(BaseModel):
    orders: list[OrderInput]


class PredictionResponse(BaseModel):
    prediction: str
    probability: float
    model_version: int
