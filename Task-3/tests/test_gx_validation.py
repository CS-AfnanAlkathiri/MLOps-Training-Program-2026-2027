import pandas as pd
import pytest

from src.gx_validation import validate_with_gx


def test_gx_accepts_valid_data():
    data = pd.read_csv("data/sample_order.csv")

    assert validate_with_gx(data) is True


def test_gx_rejects_negative_total_price():
    data = pd.read_csv("data/sample_order.csv")
    data["total_price"] = -10

    with pytest.raises(ValueError, match="Great Expectations validation failed"):
        validate_with_gx(data)
