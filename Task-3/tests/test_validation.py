import pandas as pd
import pytest
from src.validation import validate_input


def test_valid_input_passes():
    data = pd.DataFrame(
        [
            {
                "order_purchase_timestamp": "2018-06-21 08:29:29",
                "order_estimated_delivery_date": "2018-07-17",
                "customer_state": "MG",
                "seller_state": "SP",
                "item_count": 1,
                "total_price": 46.0,
                "total_freight_value": 18.42,
                "unique_products": 1,
                "unique_sellers": 1,
                "payment_count": 2,
                "total_payment_value": 64.42,
                "max_installments": 1,
                "payment_type_count": 2,
                "distance_km": 635.24,
            }
        ]
    )

    assert validate_input(data) is True


def test_missing_required_column_raises_error():
    data = pd.DataFrame(
        [
            {
                "order_purchase_timestamp": "2018-06-21 08:29:29",
                "order_estimated_delivery_date": "2018-07-17",
                "customer_state": "MG",
                "seller_state": "SP",
                "item_count": 1,
                "total_price": 46.0,
                "total_freight_value": 18.42,
                "unique_products": 1,
                "unique_sellers": 1,
                "payment_count": 2,
                "total_payment_value": 64.42,
                "max_installments": 1,
                "payment_type_count": 2,
            }
        ]
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_input(data)
