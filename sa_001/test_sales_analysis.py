# sa_001/test_sales_analysis.py
import pytest
import pandas as pd
from pathlib import Path
from sa_001.sales_analysis import (
    add_revenue_column,
    total_revenue,
    revenue_by_region,
    revenue_by_product,
    monthly_revenue,
    average_discount_by_category,
    top_n_products_by_revenue,
    load_sales_data,
)


def _sample_df():
    """Create a small hardcoded DataFrame for testing."""
    data = [
        # order_id, date, region, product, category, quantity, unit_price, discount, salesperson
        (1, "2024-01-01", "North", "Widget A", "Gadgets", 10, 10.0, 0.1, "Alice"),
        (2, "2024-01-15", "South", "Widget B", "Gadgets", 5, 20.0, 0.0, "Bob"),
        (3, "2024-02-01", "North", "Gizmo C", "Accessories", 2, 30.0, 0.0, "Charlie"),
        (4, "2024-02-15", "East", "Widget A", "Gadgets", 3, 10.0, 0.2, "Diana"),
    ]
    df = pd.DataFrame(
        data,
        columns=[
            "order_id", "date", "region", "product", "category",
            "quantity", "unit_price", "discount", "salesperson",
        ],
    )
    df["date"] = pd.to_datetime(df["date"])
    return df


class TestAddRevenueColumn:
    """Test cases for add_revenue_column function."""

    def test_revenue_calculation(self):
        """Test that revenue is calculated correctly."""
        df = _sample_df()
        df_with_revenue = add_revenue_column(df)
        
        # Verify revenue column exists
        assert "revenue" in df_with_revenue.columns
        
        # Verify calculations for each row
        # Row 0: 10 * 10.0 * (1 - 0.1) = 90.0
        assert df_with_revenue.iloc[0]["revenue"] == pytest.approx(90.0)
        # Row 1: 5 * 20.0 * (1 - 0.0) = 100.0
        assert df_with_revenue.iloc[1]["revenue"] == pytest.approx(100.0)
        # Row 2: 2 * 30.0 * (1 - 0.0) = 60.0
        assert df_with_revenue.iloc[2]["revenue"] == pytest.approx(60.0)
        # Row 3: 3 * 10.0 * (1 - 0.2) = 24.0
        assert df_with_revenue.iloc[3]["revenue"] == pytest.approx(24.0)

    def test_original_dataframe_unchanged(self):
        """Test that original DataFrame is not modified."""
        df = _sample_df()
        original_columns = df.columns.tolist()
        add_revenue_column(df)
        
        # Original DataFrame should not have revenue column
        assert "revenue" not in df.columns
        assert df.columns.tolist() == original_columns


class TestTotalRevenue:
    """Test cases for total_revenue function."""

    def test_total_revenue_calculation(self):
        """Test total revenue calculation."""
        df = _sample_df()
        # Expected: 90.0 + 100.0 + 60.0 + 24.0 = 274.0
        assert total_revenue(df) == pytest.approx(274.0)

    def test_empty_dataframe(self):
        """Test total revenue with empty DataFrame."""
        df = pd.DataFrame(columns=[
            "order_id", "date", "region", "product", "category",
            "quantity", "unit_price", "discount", "salesperson"
        ])
        assert total_revenue(df) == pytest.approx(0.0)


class TestRevenueByRegion:
    """Test cases for revenue_by_region function."""

    def test_revenue_by_region_grouping(self):
        """Test revenue grouped by region."""
        df = _sample_df()
        result = revenue_by_region(df)
        
        # North: 90.0 + 60.0 = 150.0
        assert result["North"] == pytest.approx(150.0)
        # South: 100.0
        assert result["South"] == pytest.approx(100.0)
        # East: 24.0
        assert result["East"] == pytest.approx(24.0)
        
        # Verify it's a Series
        assert isinstance(result, pd.Series)
        assert result.name == "revenue"


class TestRevenueByProduct:
    """Test cases for revenue_by_product function."""

    def test_revenue_by_product_grouping(self):
        """Test revenue grouped by product."""
        df = _sample_df()
        result = revenue_by_product(df)
        
        # Widget A: 90.0 + 24.0 = 114.0
        assert result["Widget A"] == pytest.approx(114.0)
        # Widget B: 100.0
        assert result["Widget B"] == pytest.approx(100.0)
        # Gizmo C: 60.0
        assert result["Gizmo C"] == pytest.approx(60.0)
        
        assert isinstance(result, pd.Series)


class TestMonthlyRevenue:
    """Test cases for monthly_revenue function."""

    def test_monthly_revenue_grouping(self):
        """Test revenue grouped by month."""
        df = _sample_df()
        result = monthly_revenue(df)
        
        # 2024-01: 90.0 + 100.0 = 190.0
        jan_2024 = pd.Period("2024-01", freq="M")
        assert result[jan_2024] == pytest.approx(190.0)
        
        # 2024-02: 60.0 + 24.0 = 84.0
        feb_2024 = pd.Period("2024-02", freq="M")
        assert result[feb_2024] == pytest.approx(84.0)
        
        assert isinstance(result, pd.Series)


class TestTopNProducts:
    """Test cases for top_n_products_by_revenue function."""

    def test_top_n_products_ordering(self):
        """Test top N products are correctly ordered."""
        df = _sample_df()
        result = top_n_products_by_revenue(df, n=2)
        
        # Should return top 2: Widget A (114.0) and Widget B (100.0)
        assert len(result) == 2
        assert result.iloc[0] == pytest.approx(114.0)  # Widget A
        assert result.iloc[1] == pytest.approx(100.0)  # Widget B
        assert result.index[0] == "Widget A"
        assert result.index[1] == "Widget B"

    def test_top_n_with_n_greater_than_products(self):
        """Test when N is greater than number of products."""
        df = _sample_df()
        result = top_n_products_by_revenue(df, n=10)
        
        # Should return all 3 products
        assert len(result) == 3


class TestAverageDiscountByCategory:
    """Test cases for average_discount_by_category function."""

    def test_average_discount_calculation(self):
        """Test average discount by category."""
        df = _sample_df()
        result = average_discount_by_category(df)
        
        # Gadgets: (0.1 + 0.0 + 0.2) / 3 = 0.1
        assert result["Gadgets"] == pytest.approx(0.1)
        
        # Accessories: 0.0 / 1 = 0.0
        assert result["Accessories"] == pytest.approx(0.0)
        
        assert isinstance(result, pd.Series)


class TestLoadSalesData:
    """Test cases for load_sales_data function."""

    def test_load_csv_file(self):
        """Test loading data from CSV file."""
        # Use the actual sales_sample.csv file
        csv_path = Path(__file__).parent / "data" / "sales_sample.csv"
        df = load_sales_data(csv_path)
        
        # Verify DataFrame is not empty
        assert len(df) > 0
        
        # Verify expected columns exist
        expected_columns = [
            "order_id", "date", "region", "product", "category",
            "quantity", "unit_price", "discount", "salesperson"
        ]
        for col in expected_columns:
            assert col in df.columns
        
        # Verify date column is datetime type
        assert pd.api.types.is_datetime64_any_dtype(df["date"])

    def test_date_parsing(self):
        """Test that dates are properly parsed."""
        csv_path = Path(__file__).parent / "data" / "sales_sample.csv"
        df = load_sales_data(csv_path)
        
        # Verify first date is parsed correctly
        first_date = df.iloc[0]["date"]
        assert isinstance(first_date, pd.Timestamp)


class TestFunctionalProgrammingPatterns:
    """Test that functional programming patterns are used correctly."""

    def test_immutability(self):
        """Test that functions don't modify the input DataFrame."""
        df = _sample_df()
        original_shape = df.shape
        original_columns = df.columns.tolist()
        
        # Call various functions
        total_revenue(df)
        revenue_by_region(df)
        revenue_by_product(df)
        monthly_revenue(df)
        top_n_products_by_revenue(df)
        average_discount_by_category(df)
        
        # Verify original DataFrame is unchanged
        assert df.shape == original_shape
        assert df.columns.tolist() == original_columns
        assert "revenue" not in df.columns


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
