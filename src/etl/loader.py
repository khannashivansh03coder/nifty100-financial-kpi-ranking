import pandas as pd
import os


def load_financials():
    """
    Loads raw NIFTY 100 financial data
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data_path = os.path.join(base_dir, "data", "raw", "nifty100_financials.csv")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Raw data file not found at {data_path}")

    df = pd.read_csv(data_path)
    return df