"""
Unit tests for DataAnalyzer class.
Tests all analysis methods using functional programming patterns.
"""

import unittest
import tempfile
import os
from src.csv_reader import CSVReader
from src.data_analyzer import DataAnalyzer


class TestDataAnalyzer(unittest.TestCase):
    """Test cases for DataAnalyzer implementation."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create test CSV data
        self.test_data = """Date,Product,Category,Region,Customer_Type,Quantity,Unit_Price,Total_Revenue
2024-01-15,TurboTax Deluxe,Tax Software,West,Individual,100,59.99,5999.00
2024-01-18,QuickBooks Online,Accounting Software,East,Small Business,200,25.00,5000.00
2024-01-20,TurboTax Premier,Tax Software,South,Individual,150,79.99,11998.50
2024-02-01,QuickBooks Desktop,Accounting Software,West,Small Business,50,299.99,14999.50
2024-02-05,Intuit Payroll,Payroll Services,East,Small Business,300,45.00,13500.00"""
        
        # Create temporary file
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.csv',
            delete=False,
            encoding='utf-8'
        )
        self.temp_file.write(self.test_data)
        self.temp_file.close()
        self.temp_file_path = self.temp_file.name
        
        # Initialize reader and analyzer
        csv_reader = CSVReader(self.temp_file_path)
        self.analyzer = DataAnalyzer(csv_reader)

    def tearDown(self):
        """Clean up test fixtures after each test method."""
        if os.path.exists(self.temp_file_path):
            os.unlink(self.temp_file_path)

    def test_get_total_revenue(self):
        """Test total revenue calculation using reduce operation."""
        total = self.analyzer.get_total_revenue()
        expected = 5999.00 + 5000.00 + 11998.50 + 14999.50 + 13500.00
        self.assertAlmostEqual(total, expected, places=2)

    def test_get_revenue_by_category(self):
        """Test revenue grouping by category."""
        revenue_by_category = self.analyzer.get_revenue_by_category()
        
        self.assertIsInstance(revenue_by_category, dict)
        self.assertIn('Tax Software', revenue_by_category)
        self.assertIn('Accounting Software', revenue_by_category)
        self.assertIn('Payroll Services', revenue_by_category)
        
        # Verify tax software revenue
        tax_revenue = revenue_by_category['Tax Software']
        expected_tax = 5999.00 + 11998.50
        self.assertAlmostEqual(tax_revenue, expected_tax, places=2)

    def test_get_revenue_by_region(self):
        """Test revenue grouping by region."""
        revenue_by_region = self.analyzer.get_revenue_by_region()
        
        self.assertIsInstance(revenue_by_region, dict)
        self.assertIn('West', revenue_by_region)
        self.assertIn('East', revenue_by_region)
        self.assertIn('South', revenue_by_region)

    def test_get_revenue_by_customer_type(self):
        """Test revenue grouping by customer type."""
        revenue_by_customer = self.analyzer.get_revenue_by_customer_type()
        
        self.assertIsInstance(revenue_by_customer, dict)
        self.assertIn('Individual', revenue_by_customer)
        self.assertIn('Small Business', revenue_by_customer)

    def test_get_top_products_by_revenue(self):
        """Test getting top products by revenue using sorting with lambda."""
        top_products = self.analyzer.get_top_products_by_revenue(top_n=3)
        
        self.assertIsInstance(top_products, list)
        self.assertLessEqual(len(top_products), 3)
        
        # Verify products are sorted by revenue (descending)
        if len(top_products) > 1:
            for i in range(len(top_products) - 1):
                self.assertGreaterEqual(
                    top_products[i]['Total_Revenue'],
                    top_products[i + 1]['Total_Revenue']
                )

    def test_get_average_revenue_per_transaction(self):
        """Test average revenue calculation using map and reduce."""
        avg_revenue = self.analyzer.get_average_revenue_per_transaction()
        
        self.assertIsInstance(avg_revenue, float)
        self.assertGreater(avg_revenue, 0)
        
        # Verify calculation
        total = self.analyzer.get_total_revenue()
        records = self.analyzer.csv_reader.read_all_records()
        expected_avg = total / len(records)
        self.assertAlmostEqual(avg_revenue, expected_avg, places=2)

    def test_get_sales_by_month(self):
        """Test sales grouping by month."""
        sales_by_month = self.analyzer.get_sales_by_month()
        
        self.assertIsInstance(sales_by_month, dict)
        self.assertIn('2024-01', sales_by_month)
        self.assertIn('2024-02', sales_by_month)

    def test_get_products_by_category(self):
        """Test grouping products by category."""
        products_by_category = self.analyzer.get_products_by_category()
        
        self.assertIsInstance(products_by_category, dict)
        self.assertIn('Tax Software', products_by_category)
        self.assertIsInstance(products_by_category['Tax Software'], list)
        
        # Verify products are in correct category
        tax_products = products_by_category['Tax Software']
        self.assertIn('TurboTax Deluxe', tax_products)
        self.assertIn('TurboTax Premier', tax_products)

    def test_get_high_value_transactions(self):
        """Test filtering high value transactions using lambda filter."""
        high_value = self.analyzer.get_high_value_transactions(threshold=10000.0)
        
        self.assertIsInstance(high_value, list)
        for transaction in high_value:
            revenue = float(transaction.get('Total_Revenue', '0'))
            self.assertGreaterEqual(revenue, 10000.0)

    def test_get_revenue_by_product_and_region(self):
        """Test nested grouping by product and region."""
        product_region_revenue = self.analyzer.get_revenue_by_product_and_region()
        
        self.assertIsInstance(product_region_revenue, dict)
        
        # Verify nested structure
        for product, regions in product_region_revenue.items():
            self.assertIsInstance(regions, dict)
            for region, revenue in regions.items():
                self.assertIsInstance(revenue, (int, float))
                self.assertGreaterEqual(revenue, 0)

    def test_get_total_quantity_sold(self):
        """Test total quantity calculation using map and reduce."""
        total_quantity = self.analyzer.get_total_quantity_sold()
        
        self.assertIsInstance(total_quantity, int)
        expected = 100 + 200 + 150 + 50 + 300
        self.assertEqual(total_quantity, expected)

    def test_get_average_quantity_per_transaction(self):
        """Test average quantity calculation."""
        avg_quantity = self.analyzer.get_average_quantity_per_transaction()
        
        self.assertIsInstance(avg_quantity, float)
        self.assertGreater(avg_quantity, 0)
        
        # Verify calculation
        total_qty = self.analyzer.get_total_quantity_sold()
        records = self.analyzer.csv_reader.read_all_records()
        expected_avg = total_qty / len(records)
        self.assertAlmostEqual(avg_quantity, expected_avg, places=2)

    def test_empty_data_handling(self):
        """Test handling of empty CSV data."""
        # Create empty CSV
        empty_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.csv',
            delete=False,
            encoding='utf-8'
        )
        empty_file.write("Date,Product,Category,Region,Customer_Type,Quantity,Unit_Price,Total_Revenue\n")
        empty_file.close()
        
        csv_reader = CSVReader(empty_file.name)
        analyzer = DataAnalyzer(csv_reader)
        
        # Should handle empty data gracefully
        total_revenue = analyzer.get_total_revenue()
        self.assertEqual(total_revenue, 0.0)
        
        avg_revenue = analyzer.get_average_revenue_per_transaction()
        self.assertEqual(avg_revenue, 0.0)
        
        os.unlink(empty_file.name)

    def test_invalid_numeric_handling(self):
        """Test handling of invalid numeric values in CSV."""
        # CSV with invalid numeric values should be handled
        invalid_data = """Date,Product,Category,Region,Customer_Type,Quantity,Unit_Price,Total_Revenue
2024-01-15,Product1,Category1,West,Individual,invalid,59.99,5999.00"""
        
        invalid_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.csv',
            delete=False,
            encoding='utf-8'
        )
        invalid_file.write(invalid_data)
        invalid_file.close()
        
        csv_reader = CSVReader(invalid_file.name)
        analyzer = DataAnalyzer(csv_reader)
        
        # Should handle invalid values gracefully
        total_quantity = analyzer.get_total_quantity_sold()
        self.assertIsInstance(total_quantity, int)
        
        os.unlink(invalid_file.name)


if __name__ == "__main__":
    unittest.main()

