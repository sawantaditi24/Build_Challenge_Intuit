"""
Unit tests for CSVReader class.
Tests CSV reading functionality and stream-like operations.
"""

import unittest
import tempfile
import os
from pathlib import Path
from src.csv_reader import CSVReader


class TestCSVReader(unittest.TestCase):
    """Test cases for CSVReader implementation."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary CSV file for testing
        self.test_data = """Date,Product,Category,Region,Customer_Type,Quantity,Unit_Price,Total_Revenue
2024-01-15,TurboTax Deluxe,Tax Software,West,Individual,100,59.99,5999.00
2024-01-18,QuickBooks Online,Accounting Software,East,Small Business,200,25.00,5000.00
2024-01-20,TurboTax Premier,Tax Software,South,Individual,150,79.99,11998.50"""
        
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

    def tearDown(self):
        """Clean up test fixtures after each test method."""
        if os.path.exists(self.temp_file_path):
            os.unlink(self.temp_file_path)

    def test_csv_reader_initialization(self):
        """Test CSV reader initialization with valid file."""
        reader = CSVReader(self.temp_file_path)
        self.assertEqual(reader.file_path, Path(self.temp_file_path))

    def test_csv_reader_file_not_found(self):
        """Test CSV reader raises error for non-existent file."""
        with self.assertRaises(FileNotFoundError):
            CSVReader("nonexistent_file.csv")

    def test_read_records(self):
        """Test reading records from CSV file."""
        reader = CSVReader(self.temp_file_path)
        records = list(reader.read_records())
        
        self.assertEqual(len(records), 3)
        self.assertIsInstance(records[0], dict)
        self.assertEqual(records[0]['Product'], 'TurboTax Deluxe')
        self.assertEqual(records[0]['Category'], 'Tax Software')

    def test_read_all_records(self):
        """Test reading all records into a list."""
        reader = CSVReader(self.temp_file_path)
        records = reader.read_all_records()
        
        self.assertEqual(len(records), 3)
        self.assertIsInstance(records, list)

    def test_filter_records(self):
        """Test filtering records using predicate function."""
        reader = CSVReader(self.temp_file_path)
        
        # Filter by category using lambda (functional programming)
        tax_records = list(reader.filter_records(
            lambda record: record['Category'] == 'Tax Software'
        ))
        
        self.assertEqual(len(tax_records), 2)
        for record in tax_records:
            self.assertEqual(record['Category'], 'Tax Software')

    def test_map_records(self):
        """Test mapping records using transform function."""
        reader = CSVReader(self.temp_file_path)
        
        # Map to extract product names using lambda (functional programming)
        products = list(reader.map_records(
            lambda record: record['Product']
        ))
        
        self.assertEqual(len(products), 3)
        self.assertIn('TurboTax Deluxe', products)
        self.assertIn('QuickBooks Online', products)

    def test_stream_like_behavior(self):
        """Test that read_records behaves like a stream (lazy evaluation)."""
        reader = CSVReader(self.temp_file_path)
        
        # Get iterator (should not load all data)
        records_iter = reader.read_records()
        self.assertTrue(hasattr(records_iter, '__iter__'))
        
        # Consume first record
        first_record = next(records_iter)
        self.assertIsInstance(first_record, dict)
        
        # Should be able to continue
        second_record = next(records_iter)
        self.assertIsInstance(second_record, dict)


if __name__ == "__main__":
    unittest.main()

