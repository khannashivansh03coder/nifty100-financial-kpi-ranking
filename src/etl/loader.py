"""
Excel loader utilities for NIFTY100 ETL project.
"""

from pathlib import Path
import pandas as pd


RAW_DATA_DIR = Path("data/raw")


def load_excel_file(file_name: str, header: int = 1) -> pd.DataFrame:
    """
    Load an Excel file from the data/raw folder.

    Parameters:
        file_name: Name of the Excel file.
        header: Row number to use as column names.

    Returns:
        pandas DataFrame
    """
    file_path = RAW_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_excel(file_path, header=header)
    return df


def load_companies() -> pd.DataFrame:
    """
    Load companies.xlsx file.
    """
    return load_excel_file("companies.xlsx", header=1)


if __name__ == "__main__":
    companies = load_companies()
    print(companies.head())
    print(companies.shape)
