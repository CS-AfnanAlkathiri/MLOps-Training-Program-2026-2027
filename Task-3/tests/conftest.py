import pytest


@pytest.fixture(autouse=True)
def use_local_model(monkeypatch):
    """Use local model artifacts during tests."""
    monkeypatch.setenv("MODEL_SOURCE", "local")
