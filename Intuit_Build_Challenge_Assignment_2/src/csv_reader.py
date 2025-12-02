"""
CSV Reader module for loading and parsing sales data.
Provides functional-style data loading operations.
"""

import csv
from typing import Iterator, Dict, List, Optional
from pathlib import Path


class CSVReader:
    """
    Functional-style CSV reader that provides stream-like operations
    for processing sales data.
    """

    def __init__(self, file_path: str):
        """
        Initialize CSV reader with file path.

        Args:
            file_path: Path to the CSV file to read
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

    def read_records(self) -> Iterator[Dict[str, str]]:
        """
        Read CSV file and yield records as dictionaries.
        Uses generator pattern (similar to Streams) for lazy evaluation.

        Yields:
            Dictionary representing a single CSV record
        """
        with open(self.file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for record in reader:
                yield record

    def read_all_records(self) -> List[Dict[str, str]]:
        """
        Read all CSV records into a list.
        Useful when all data needs to be in memory.

        Returns:
            List of dictionaries representing all CSV records
        """
        return list(self.read_records())

    def filter_records(self, predicate) -> Iterator[Dict[str, str]]:
        """
        Filter records using a predicate function (functional programming pattern).

        Args:
            predicate: Function that takes a record and returns True/False

        Yields:
            Filtered records that match the predicate
        """
        return filter(predicate, self.read_records())

    def map_records(self, transform) -> Iterator:
        """
        Transform records using a mapping function (functional programming pattern).

        Args:
            transform: Function that transforms a record

        Yields:
            Transformed records
        """
        return map(transform, self.read_records())

