import pandas as pd


def load_csv_data(file_path):
    """Load order data from a CSV file."""
    return pd.read_csv(file_path)
