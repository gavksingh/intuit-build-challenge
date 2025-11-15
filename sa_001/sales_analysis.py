# sa_001/sales_analysis.py
from pathlib import Path
import pandas as pd


def load_sales_data(csv_path: Path) -> pd.DataFrame:
    """Load sales data from CSV into a DataFrame."""
    raise NotImplementedError


def add_revenue_column(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df with a new 'revenue' column."""
    raise NotImplementedError


def total_revenue(df: pd.DataFrame) -> float:
    raise NotImplementedError


def revenue_by_region(df: pd.DataFrame) -> pd.Series:
    raise NotImplementedError


def revenue_by_product(df: pd.DataFrame) -> pd.Series:
    raise NotImplementedError


def monthly_revenue(df: pd.DataFrame) -> pd.Series:
    raise NotImplementedError


def top_n_products_by_revenue(df: pd.DataFrame, n: int = 5) -> pd.Series:
    raise NotImplementedError


def average_discount_by_category(df: pd.DataFrame) -> pd.Series:
    raise NotImplementedError


def print_analysis(df: pd.DataFrame) -> None:
    """Print results of all analyses to console."""
    raise NotImplementedError


if __name__ == "__main__":
    data_path = Path(__file__).parent / "data" / "sales_sample.csv"
    df = load_sales_data(data_path)
    print_analysis(df)
