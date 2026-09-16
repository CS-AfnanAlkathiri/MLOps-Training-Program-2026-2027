import pandas as pd


def build_features(data):
    """Create the same engineered features used in Task 2."""
    df = data.copy()

    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

    df["order_estimated_delivery_date"] = pd.to_datetime(
        df["order_estimated_delivery_date"]
    )

    df["purchase_month"] = df["order_purchase_timestamp"].dt.month
    df["purchase_weekday"] = df["order_purchase_timestamp"].dt.dayofweek
    df["purchase_hour"] = df["order_purchase_timestamp"].dt.hour

    df["estimated_window_days"] = (
        df["order_estimated_delivery_date"] - df["order_purchase_timestamp"]
    ).dt.total_seconds() / (60 * 60 * 24)

    df["same_state"] = (df["customer_state"] == df["seller_state"]).astype(int)

    return df
