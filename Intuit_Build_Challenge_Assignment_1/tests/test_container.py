"""
Unit tests for Container class.
Tests thread-safe container operations and data integrity.
"""

import unittest
import threading
from src.container import Container


class TestContainer(unittest.TestCase):
    """Test cases for Container implementation."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.container = Container("TestContainer")

    def test_container_initialization_empty(self):
        """Test container initialization with no initial items."""
        self.assertEqual(self.container.name, "TestContainer")
        self.assertTrue(self.container.is_empty())
        self.assertEqual(self.container.size(), 0)

    def test_container_initialization_with_items(self):
        """Test container initialization with initial items."""
        initial_items = ["item1", "item2", "item3"]
        container = Container("TestContainer", initial_items)
        
        self.assertEqual(container.size(), 3)
        self.assertFalse(container.is_empty())
        self.assertEqual(container.get_all_items(), initial_items)

    def test_add_item(self):
        """Test adding items to container."""
        self.container.add_item("item1")
        self.assertEqual(self.container.size(), 1)
        self.assertFalse(self.container.is_empty())

        self.container.add_item("item2")
        self.assertEqual(self.container.size(), 2)

    def test_get_item(self):
        """Test retrieving items from container by index."""
        self.container.add_item("item1")
        self.container.add_item("item2")
        self.container.add_item("item3")

        self.assertEqual(self.container.get_item(0), "item1")
        self.assertEqual(self.container.get_item(1), "item2")
        self.assertEqual(self.container.get_item(2), "item3")

    def test_get_item_invalid_index(self):
        """Test retrieving item with invalid index."""
        self.assertIsNone(self.container.get_item(0))
        self.assertIsNone(self.container.get_item(-1))
        self.assertIsNone(self.container.get_item(10))

    def test_remove_item(self):
        """Test removing items from container by index."""
        self.container.add_item("item1")
        self.container.add_item("item2")
        self.container.add_item("item3")

        removed = self.container.remove_item(1)
        self.assertEqual(removed, "item2")
        self.assertEqual(self.container.size(), 2)
        self.assertEqual(self.container.get_all_items(), ["item1", "item3"])

    def test_remove_item_invalid_index(self):
        """Test removing item with invalid index."""
        self.assertIsNone(self.container.remove_item(0))
        self.assertIsNone(self.container.remove_item(-1))
        self.assertIsNone(self.container.remove_item(10))

    def test_remove_item_from_beginning(self):
        """Test removing item from beginning of container."""
        self.container.add_item("item1")
        self.container.add_item("item2")

        removed = self.container.remove_item(0)
        self.assertEqual(removed, "item1")
        self.assertEqual(self.container.size(), 1)
        self.assertEqual(self.container.get_item(0), "item2")

    def test_is_empty(self):
        """Test empty container check."""
        self.assertTrue(self.container.is_empty())
        self.container.add_item("item1")
        self.assertFalse(self.container.is_empty())
        self.container.remove_item(0)
        self.assertTrue(self.container.is_empty())

    def test_size(self):
        """Test container size tracking."""
        self.assertEqual(self.container.size(), 0)
        for i in range(5):
            self.container.add_item(f"item{i}")
            self.assertEqual(self.container.size(), i + 1)

    def test_get_all_items(self):
        """Test retrieving all items from container."""
        items = ["item1", "item2", "item3"]
        for item in items:
            self.container.add_item(item)

        all_items = self.container.get_all_items()
        self.assertEqual(all_items, items)
        self.assertIsInstance(all_items, list)

    def test_get_all_items_returns_copy(self):
        """Test that get_all_items returns a copy, not reference."""
        self.container.add_item("item1")
        all_items = self.container.get_all_items()
        all_items.append("item2")

        self.assertEqual(self.container.size(), 1)
        self.assertEqual(len(all_items), 2)

    def test_clear(self):
        """Test clearing all items from container."""
        for i in range(5):
            self.container.add_item(f"item{i}")

        self.assertEqual(self.container.size(), 5)
        self.container.clear()
        self.assertEqual(self.container.size(), 0)
        self.assertTrue(self.container.is_empty())

    def test_string_representation(self):
        """Test string representation of container."""
        self.container.add_item("item1")
        container_str = str(self.container)
        self.assertIn("TestContainer", container_str)
        self.assertIn("items: 1", container_str)

    def test_thread_safety_concurrent_add(self):
        """Test thread safety with concurrent add operations."""
        num_threads = 10
        items_per_thread = 100

        def add_items(thread_id):
            """Add items from a thread."""
            for i in range(items_per_thread):
                self.container.add_item(f"T{thread_id}-item{i}")

        threads = [
            threading.Thread(target=add_items, args=(i,))
            for i in range(num_threads)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        expected_size = num_threads * items_per_thread
        self.assertEqual(self.container.size(), expected_size)

    def test_thread_safety_concurrent_remove(self):
        """Test thread safety with concurrent remove operations."""
        num_items = 1000
        for i in range(num_items):
            self.container.add_item(f"item{i}")

        removed_items = []
        lock = threading.Lock()

        def remove_items():
            """Remove items from a thread."""
            while not self.container.is_empty():
                item = self.container.remove_item(0)
                if item is not None:
                    with lock:
                        removed_items.append(item)

        num_threads = 5
        threads = [
            threading.Thread(target=remove_items)
            for _ in range(num_threads)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(len(removed_items), num_items)
        self.assertTrue(self.container.is_empty())

    def test_thread_safety_mixed_operations(self):
        """Test thread safety with mixed concurrent operations."""
        results = []
        lock = threading.Lock()

        def worker(thread_id):
            """Worker thread performing mixed operations."""
            for i in range(50):
                self.container.add_item(f"T{thread_id}-item{i}")
                item = self.container.get_item(0)
                if item is not None:
                    with lock:
                        results.append(item)

        num_threads = 5
        threads = [
            threading.Thread(target=worker, args=(i,))
            for i in range(num_threads)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self.assertGreater(len(results), 0)
        self.assertGreater(self.container.size(), 0)

    def test_initial_items_are_copied(self):
        """Test that initial items are copied, not referenced."""
        original_list = ["item1", "item2"]
        container = Container("Test", original_list)

        original_list.append("item3")
        self.assertEqual(container.size(), 2)
        self.assertEqual(container.get_all_items(), ["item1", "item2"])


if __name__ == "__main__":
    unittest.main()

