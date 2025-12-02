"""
Data Analysis module using functional programming paradigms.
Demonstrates Stream operations, data aggregation, and lambda expressions.
"""

from typing import Dict, List, Iterator, Callable, Any
from functools import reduce
from collections import defaultdict
from datetime import datetime
from .csv_reader import CSVReader


class DataAnalyzer:
    """
    Data analyzer that uses functional programming patterns
    (Streams, lambdas, aggregations) to perform analysis on sales data.
    """

    def __init__(self, csv_reader: CSVReader):
        """
        Initialize data analyzer with CSV reader.

        Args:
            csv_reader: CSVReader instance for loading data
        """
        self.csv_reader = csv_reader

    def _parse_numeric(self, value: str, default: float = 0.0) -> float:
        """
        Helper function to parse numeric values from CSV strings.

        Args:
            value: String value to parse
            default: Default value if parsing fails

        Returns:
            Parsed float value
        """
        try:
            return float(value.replace(',', ''))
        except (ValueError, AttributeError):
            return default

    def _parse_date(self, date_str: str) -> datetime:
        """
        Helper function to parse date strings.

        Args:
            date_str: Date string in YYYY-MM-DD format

        Returns:
            Parsed datetime object
        """
        return datetime.strptime(date_str, '%Y-%m-%d')

    def get_total_revenue(self) -> float:
        """
        Calculate total revenue across all sales using functional programming.
        Uses reduce operation (aggregation) with lambda expression.

        Returns:
            Total revenue as float
        """
        records = self.csv_reader.read_all_records()
        total = reduce(
            lambda acc, record: acc + self._parse_numeric(record.get('Total_Revenue', '0')),
            records,
            0.0
        )
        return total

    def get_revenue_by_category(self) -> Dict[str, float]:
        """
        Calculate total revenue grouped by product category.
        Uses functional programming: filter, map, and reduce operations.

        Returns:
            Dictionary mapping category names to total revenue
        """
        records = self.csv_reader.read_all_records()
        
        # Group by category using functional approach
        category_revenue = defaultdict(float)
        
        # Use map and lambda to extract and aggregate
        for record in records:
            category = record.get('Category', 'Unknown')
            revenue = self._parse_numeric(record.get('Total_Revenue', '0'))
            category_revenue[category] += revenue
        
        return dict(category_revenue)

    def get_revenue_by_region(self) -> Dict[str, float]:
        """
        Calculate total revenue grouped by region.
        Uses functional programming patterns with aggregation.

        Returns:
            Dictionary mapping region names to total revenue
        """
        records = self.csv_reader.read_all_records()
        
        region_revenue = defaultdict(float)
        
        # Functional approach: map each record to region-revenue pair
        for record in records:
            region = record.get('Region', 'Unknown')
            revenue = self._parse_numeric(record.get('Total_Revenue', '0'))
            region_revenue[region] += revenue
        
        return dict(region_revenue)

    def get_revenue_by_customer_type(self) -> Dict[str, float]:
        """
        Calculate total revenue grouped by customer type.
        Demonstrates functional aggregation using reduce pattern.

        Returns:
            Dictionary mapping customer types to total revenue
        """
        records = self.csv_reader.read_all_records()
        
        customer_revenue = defaultdict(float)
        
        # Functional aggregation using lambda
        for record in records:
            customer_type = record.get('Customer_Type', 'Unknown')
            revenue = self._parse_numeric(record.get('Total_Revenue', '0'))
            customer_revenue[customer_type] += revenue
        
        return dict(customer_revenue)

    def get_top_products_by_revenue(self, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Get top N products by total revenue.
        Uses functional programming: map, filter, and sorting operations.

        Args:
            top_n: Number of top products to return

        Returns:
            List of dictionaries with product name and total revenue
        """
        records = self.csv_reader.read_all_records()
        
        # Aggregate revenue by product using functional approach
        product_revenue = defaultdict(float)
        for record in records:
            product = record.get('Product', 'Unknown')
            revenue = self._parse_numeric(record.get('Total_Revenue', '0'))
            product_revenue[product] += revenue
        
        # Convert to list of dictionaries and sort using lambda
        product_list = [
            {'Product': product, 'Total_Revenue': revenue}
            for product, revenue in product_revenue.items()
        ]
        
        # Sort using lambda expression (functional programming)
        sorted_products = sorted(
            product_list,
            key=lambda x: x['Total_Revenue'],
            reverse=True
        )
        
        return sorted_products[:top_n]

    def get_average_revenue_per_transaction(self) -> float:
        """
        Calculate average revenue per transaction.
        Uses functional programming: map and reduce operations.

        Returns:
            Average revenue per transaction
        """
        records = self.csv_reader.read_all_records()
        
        # Use map to extract revenues, then calculate average
        revenues = map(
            lambda record: self._parse_numeric(record.get('Total_Revenue', '0')),
            records
        )
        
        revenue_list = list(revenues)
        if not revenue_list:
            return 0.0
        
        total = reduce(lambda acc, val: acc + val, revenue_list, 0.0)
        return total / len(revenue_list)

    def get_sales_by_month(self) -> Dict[str, float]:
        """
        Calculate total sales grouped by month.
        Uses functional programming with date parsing and aggregation.

        Returns:
            Dictionary mapping month names to total revenue
        """
        records = self.csv_reader.read_all_records()
        
        monthly_revenue = defaultdict(float)
        
        # Functional approach: map date to month, aggregate revenue
        for record in records:
            date_str = record.get('Date', '')
            try:
                date_obj = self._parse_date(date_str)
                month_key = date_obj.strftime('%Y-%m')
                revenue = self._parse_numeric(record.get('Total_Revenue', '0'))
                monthly_revenue[month_key] += revenue
            except (ValueError, TypeError):
                continue
        
        return dict(monthly_revenue)

    def get_products_by_category(self) -> Dict[str, List[str]]:
        """
        Group products by their category.
        Uses functional programming: filter and grouping operations.

        Returns:
            Dictionary mapping categories to list of unique products
        """
        records = self.csv_reader.read_all_records()
        
        category_products = defaultdict(set)
        
        # Functional grouping using map
        for record in records:
            category = record.get('Category', 'Unknown')
            product = record.get('Product', 'Unknown')
            category_products[category].add(product)
        
        # Convert sets to sorted lists
        return {
            category: sorted(list(products))
            for category, products in category_products.items()
        }

    def get_high_value_transactions(self, threshold: float = 100000.0) -> List[Dict[str, Any]]:
        """
        Get all transactions with revenue above a threshold.
        Uses functional programming: filter operation with lambda expression.

        Args:
            threshold: Minimum revenue threshold

        Returns:
            List of transaction records above threshold
        """
        records = self.csv_reader.read_all_records()
        
        # Use filter with lambda expression (functional programming)
        high_value = filter(
            lambda record: self._parse_numeric(record.get('Total_Revenue', '0')) >= threshold,
            records
        )
        
        return list(high_value)

    def get_revenue_by_product_and_region(self) -> Dict[str, Dict[str, float]]:
        """
        Calculate revenue grouped by product and region (nested grouping).
        Demonstrates complex functional aggregation operations.

        Returns:
            Nested dictionary: product -> region -> revenue
        """
        records = self.csv_reader.read_all_records()
        
        product_region_revenue = defaultdict(lambda: defaultdict(float))
        
        # Functional nested aggregation
        for record in records:
            product = record.get('Product', 'Unknown')
            region = record.get('Region', 'Unknown')
            revenue = self._parse_numeric(record.get('Total_Revenue', '0'))
            product_region_revenue[product][region] += revenue
        
        # Convert nested defaultdicts to regular dicts
        return {
            product: dict(regions)
            for product, regions in product_region_revenue.items()
        }

    def get_total_quantity_sold(self) -> int:
        """
        Calculate total quantity of products sold.
        Uses functional programming: map and reduce operations.

        Returns:
            Total quantity as integer
        """
        records = self.csv_reader.read_all_records()
        
        # Use map to extract quantities, then reduce to sum
        quantities = map(
            lambda record: int(self._parse_numeric(record.get('Quantity', '0'))),
            records
        )
        
        total = reduce(lambda acc, qty: acc + qty, quantities, 0)
        return total

    def get_average_quantity_per_transaction(self) -> float:
        """
        Calculate average quantity per transaction.
        Uses functional programming patterns.

        Returns:
            Average quantity per transaction
        """
        records = self.csv_reader.read_all_records()
        
        quantities = map(
            lambda record: self._parse_numeric(record.get('Quantity', '0')),
            records
        )
        
        quantity_list = list(quantities)
        if not quantity_list:
            return 0.0
        
        total = reduce(lambda acc, qty: acc + qty, quantity_list, 0.0)
        return total / len(quantity_list)

