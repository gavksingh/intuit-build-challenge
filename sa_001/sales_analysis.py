# sa_001/sales_analysis.py
from pathlib import Path
import pandas as pd


def load_sales_data(csv_path: Path) -> pd.DataFrame:
    """Load sales data from CSV into a DataFrame."""
    return pd.read_csv(csv_path, parse_dates=["date"])


def add_revenue_column(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df with a new 'revenue' column.
    
    Revenue = quantity * unit_price * (1 - discount)
    """
    return df.assign(
        revenue=lambda d: d["quantity"] * d["unit_price"] * (1 - d["discount"])
    )


def total_revenue(df: pd.DataFrame) -> float:
    """Calculate total revenue across all sales."""
    df = add_revenue_column(df)
    return float(df["revenue"].sum())


def revenue_by_region(df: pd.DataFrame) -> pd.Series:
    """Calculate total revenue grouped by region."""
    df = add_revenue_column(df)
    return df.groupby("region")["revenue"].sum()


def revenue_by_product(df: pd.DataFrame) -> pd.Series:
    """Calculate total revenue grouped by product."""
    df = add_revenue_column(df)
    return df.groupby("product")["revenue"].sum()


def monthly_revenue(df: pd.DataFrame) -> pd.Series:
    """Calculate total revenue grouped by month."""
    df = add_revenue_column(df)
    return (
        df.assign(month=lambda d: d["date"].dt.to_period("M"))
          .groupby("month")["revenue"]
          .sum()
    )


def top_n_products_by_revenue(df: pd.DataFrame, n: int = 5) -> pd.Series:
    """Return top N products by revenue in descending order."""
    return revenue_by_product(df).sort_values(ascending=False).head(n)


def average_discount_by_category(df: pd.DataFrame) -> pd.Series:
    """Calculate average discount grouped by category."""
    return df.groupby("category")["discount"].mean()


def print_analysis(df: pd.DataFrame) -> None:
    """Print results of all analyses to console."""
    df = add_revenue_column(df)
    
    print("=" * 60)
    print("=== Sales Analysis ===")
    print("=" * 60)
    print()
    
    print(f"Total Revenue: ${total_revenue(df):,.2f}")
    print()
    
    print("-" * 60)
    print("Revenue by Region:")
    print("-" * 60)
    for region, revenue in revenue_by_region(df).items():
        print(f"  {region:15s} ${revenue:>12,.2f}")
    print()
    
    print("-" * 60)
    print("Revenue by Product:")
    print("-" * 60)
    for product, revenue in revenue_by_product(df).items():
        print(f"  {product:25s} ${revenue:>12,.2f}")
    print()
    
    print("-" * 60)
    print("Monthly Revenue:")
    print("-" * 60)
    for month, revenue in monthly_revenue(df).items():
        print(f"  {str(month):15s} ${revenue:>12,.2f}")
    print()
    
    print("-" * 60)
    print("Top 5 Products by Revenue:")
    print("-" * 60)
    for idx, (product, revenue) in enumerate(top_n_products_by_revenue(df, n=5).items(), 1):
        print(f"  {idx}. {product:23s} ${revenue:>12,.2f}")
    print()
    
    print("-" * 60)
    print("Average Discount by Category:")
    print("-" * 60)
    for category, discount in average_discount_by_category(df).items():
        print(f"  {category:25s} {discount:>8.1%}")
    print()
    
    print("=" * 60)


if __name__ == "__main__":
    data_path = Path(__file__).parent / "data" / "sales_sample.csv"
    df = load_sales_data(data_path)
    print_analysis(df)
