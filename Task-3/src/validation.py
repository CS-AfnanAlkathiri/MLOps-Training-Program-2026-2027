REQUIRED_COLUMNS = [
    "order_purchase_timestamp",
    "order_estimated_delivery_date",
    "customer_state",
    "seller_state",
    "item_count",
    "total_price",
    "total_freight_value",
    "unique_products",
    "unique_sellers",
    "payment_count",
    "total_payment_value",
    "max_installments",
    "payment_type_count",
    "distance_km",
]


def validate_input(data):
    """Check that incoming order data contains the required fields."""
    if data.empty:
        raise ValueError("Input data is empty.")

    missing_columns = [
        column for column in REQUIRED_COLUMNS if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    return True
