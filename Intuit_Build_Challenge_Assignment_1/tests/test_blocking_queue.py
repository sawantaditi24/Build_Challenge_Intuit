"""
Unit tests for BlockingQueue class.
Tests thread synchronization, blocking behavior, and wait/notify mechanism.
"""

import unittest
import threading
import time
from src.blocking_queue import BlockingQueue


class TestBlockingQueue(unittest.TestCase):
    """Test cases for BlockingQueue implementation."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.queue = BlockingQueue(max_size=3)

    def test_initialization(self):
        """Test queue initialization with valid size."""
        self.assertEqual(self.queue.max_size(), 3)
        self.assertTrue(self.queue.is_empty())
        self.assertFalse(self.queue.is_full())
        self.assertEqual(self.queue.size(), 0)

    def test_initialization_invalid_size(self):
        """Test queue initialization with invalid size raises ValueError."""
        with self.assertRaises(ValueError):
            BlockingQueue(max_size=0)
        with self.assertRaises(ValueError):
            BlockingQueue(max_size=-1)

    def test_put_and_get_single_item(self):
        """Test basic put and get operations."""
        item = "test_item"
        self.assertTrue(self.queue.put(item))
        self.assertEqual(self.queue.size(), 1)
        self.assertFalse(self.queue.is_empty())
        
        retrieved_item = self.queue.get()
        self.assertEqual(retrieved_item, item)
        self.assertEqual(self.queue.size(), 0)
        self.assertTrue(self.queue.is_empty())

    def test_put_and_get_multiple_items(self):
        """Test putting and getting multiple items."""
        items = ["item1", "item2", "item3"]
        for item in items:
            self.assertTrue(self.queue.put(item))
        
        self.assertEqual(self.queue.size(), 3)
        self.assertTrue(self.queue.is_full())
        
        retrieved_items = []
        for _ in range(3):
            retrieved_items.append(self.queue.get())
        
        self.assertEqual(retrieved_items, items)
        self.assertTrue(self.queue.is_empty())

    def test_fifo_ordering(self):
        """Test that queue maintains FIFO (First In First Out) ordering."""
        items = ["first", "second", "third"]
        for item in items:
            self.queue.put(item)
        
        retrieved_items = []
        for _ in range(3):
            retrieved_items.append(self.queue.get())
        
        self.assertEqual(retrieved_items, items)

    def test_blocking_put_when_full(self):
        """Test that put operation blocks when queue is full."""
        # Fill the queue
        for i in range(3):
            self.queue.put(f"item{i}")
        
        self.assertTrue(self.queue.is_full())
        
        # Try to put with timeout - should fail quickly
        result = self.queue.put("blocked_item", timeout=0.1)
        self.assertFalse(result)

    def test_blocking_get_when_empty(self):
        """Test that get operation blocks when queue is empty."""
        # Try to get with timeout - should return None
        result = self.queue.get(timeout=0.1)
        self.assertIsNone(result)

    def test_producer_consumer_synchronization(self):
        """Test synchronization between producer and consumer threads."""
        items_produced = []
        items_consumed = []
        production_complete = threading.Event()
        consumption_complete = threading.Event()

        def producer():
            """Producer thread function."""
            for i in range(5):
                item = f"item{i}"
                self.queue.put(item)
                items_produced.append(item)
                time.sleep(0.01)
            production_complete.set()

        def consumer():
            """Consumer thread function."""
            while not production_complete.is_set() or not self.queue.is_empty():
                item = self.queue.get(timeout=0.5)
                if item is not None:
                    items_consumed.append(item)
                time.sleep(0.01)

        # Start threads
        producer_thread = threading.Thread(target=producer)
        consumer_thread = threading.Thread(target=consumer)

        producer_thread.start()
        consumer_thread.start()

        producer_thread.join()
        consumer_thread.join()

        # Verify all items were consumed
        self.assertEqual(len(items_produced), 5)
        self.assertEqual(len(items_consumed), 5)
        self.assertEqual(set(items_produced), set(items_consumed))

    def test_multiple_producers_single_consumer(self):
        """Test multiple producers with single consumer."""
        items_consumed = []
        num_producers = 3
        items_per_producer = 5
        producers_complete = threading.Event()

        def producer(producer_id):
            """Producer thread function."""
            for i in range(items_per_producer):
                item = f"P{producer_id}-item{i}"
                self.queue.put(item)
                time.sleep(0.01)
            producers_complete.set()

        def consumer():
            """Consumer thread function."""
            consumed_count = 0
            expected_total = num_producers * items_per_producer
            while consumed_count < expected_total:
                item = self.queue.get(timeout=1.0)
                if item is not None:
                    items_consumed.append(item)
                    consumed_count += 1
                time.sleep(0.01)

        # Start threads
        producer_threads = [
            threading.Thread(target=producer, args=(i,))
            for i in range(num_producers)
        ]
        consumer_thread = threading.Thread(target=consumer)

        for thread in producer_threads:
            thread.start()
        consumer_thread.start()

        for thread in producer_threads:
            thread.join()
        consumer_thread.join()

        # Verify all items were consumed
        expected_total = num_producers * items_per_producer
        self.assertEqual(len(items_consumed), expected_total)

    def test_single_producer_multiple_consumers(self):
        """Test single producer with multiple consumers."""
        items_produced = []
        items_consumed = []
        num_consumers = 3
        total_items = 15
        production_complete = threading.Event()

        def producer():
            """Producer thread function."""
            for i in range(total_items):
                item = f"item{i}"
                self.queue.put(item)
                items_produced.append(item)
                time.sleep(0.01)
            production_complete.set()

        def consumer(consumer_id):
            """Consumer thread function."""
            while not production_complete.is_set() or not self.queue.is_empty():
                item = self.queue.get(timeout=0.5)
                if item is not None:
                    items_consumed.append(item)
                time.sleep(0.01)

        # Start threads
        producer_thread = threading.Thread(target=producer)
        consumer_threads = [
            threading.Thread(target=consumer, args=(i,))
            for i in range(num_consumers)
        ]

        producer_thread.start()
        for thread in consumer_threads:
            thread.start()

        producer_thread.join()
        for thread in consumer_threads:
            thread.join()

        # Verify all items were consumed
        self.assertEqual(len(items_produced), total_items)
        self.assertEqual(len(items_consumed), total_items)
        self.assertEqual(set(items_produced), set(items_consumed))

    def test_thread_safety_concurrent_operations(self):
        """Test thread safety with concurrent put and get operations."""
        num_threads = 10
        items_per_thread = 20
        results = []

        def worker(thread_id):
            """Worker thread that both produces and consumes."""
            for i in range(items_per_thread):
                item = f"T{thread_id}-item{i}"
                self.queue.put(item)
                retrieved = self.queue.get()
                if retrieved is not None:
                    results.append((thread_id, retrieved))

        threads = [
            threading.Thread(target=worker, args=(i,))
            for i in range(num_threads)
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Verify no data loss
        self.assertEqual(len(results), num_threads * items_per_thread)

    def test_queue_size_limits(self):
        """Test that queue respects maximum size limit."""
        max_size = 3
        queue = BlockingQueue(max_size=max_size)

        # Fill queue to capacity
        for i in range(max_size):
            self.assertTrue(queue.put(f"item{i}"))

        self.assertTrue(queue.is_full())
        self.assertEqual(queue.size(), max_size)

        # Try to exceed capacity with timeout
        result = queue.put("excess_item", timeout=0.1)
        self.assertFalse(result)
        self.assertEqual(queue.size(), max_size)

    def test_empty_queue_operations(self):
        """Test operations on empty queue."""
        self.assertTrue(self.queue.is_empty())
        self.assertFalse(self.queue.is_full())
        self.assertEqual(self.queue.size(), 0)

        # Get from empty queue should block and timeout
        result = self.queue.get(timeout=0.1)
        self.assertIsNone(result)

    def test_full_queue_operations(self):
        """Test operations on full queue."""
        # Fill queue
        for i in range(3):
            self.queue.put(f"item{i}")

        self.assertTrue(self.queue.is_full())
        self.assertFalse(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 3)

        # Put to full queue should block and timeout
        result = self.queue.put("blocked", timeout=0.1)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()

