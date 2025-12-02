"""
Unit tests for Consumer class.
Tests consumer thread functionality, item consumption, and synchronization.
"""

import unittest
import threading
import time
from src.consumer import Consumer
from src.container import Container
from src.blocking_queue import BlockingQueue


class TestConsumer(unittest.TestCase):
    """Test cases for Consumer implementation."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.destination_container = Container("TestDestination")
        self.shared_queue = BlockingQueue(max_size=10)
        self.consumer = Consumer(
            consumer_id="TEST",
            destination_container=self.destination_container,
            shared_queue=self.shared_queue,
            consumption_delay=0.01
        )

    def test_consumer_initialization(self):
        """Test consumer thread initialization."""
        self.assertEqual(self.consumer.consumer_id, "TEST")
        self.assertEqual(self.consumer.destination_container, self.destination_container)
        self.assertEqual(self.consumer.shared_queue, self.shared_queue)
        self.assertEqual(self.consumer.consumption_delay, 0.01)
        self.assertEqual(self.consumer.items_consumed, 0)
        self.assertFalse(self.consumer.is_alive())

    def test_consumer_name(self):
        """Test that consumer thread has correct name."""
        self.assertEqual(self.consumer.name, "Consumer-TEST")

    def test_consumer_consumes_items(self):
        """Test that consumer successfully consumes items from queue."""
        items = ["item1", "item2", "item3"]
        for item in items:
            self.shared_queue.put(item)

        self.consumer.start()
        time.sleep(0.2)
        self.consumer.stop()
        self.consumer.join(timeout=2)

        self.assertEqual(self.consumer.get_items_consumed(), 3)
        self.assertEqual(self.destination_container.size(), 3)
        self.assertTrue(self.shared_queue.is_empty())

    def test_consumer_stores_items_in_destination(self):
        """Test that consumer stores items in destination container."""
        items = ["item1", "item2", "item3"]
        for item in items:
            self.shared_queue.put(item)

        self.consumer.start()
        time.sleep(0.2)
        self.consumer.stop()
        self.consumer.join(timeout=2)

        destination_items = self.destination_container.get_all_items()
        self.assertEqual(len(destination_items), 3)
        self.assertIn("item1", destination_items)
        self.assertIn("item2", destination_items)
        self.assertIn("item3", destination_items)

    def test_consumer_blocks_when_queue_empty(self):
        """Test that consumer blocks when queue is empty."""
        self.consumer.start()
        time.sleep(0.1)
        self.assertEqual(self.consumer.get_items_consumed(), 0)

        self.shared_queue.put("item1")
        time.sleep(0.1)
        self.consumer.stop()
        self.consumer.join(timeout=2)

        self.assertEqual(self.consumer.get_items_consumed(), 1)

    def test_consumer_with_max_items_limit(self):
        """Test consumer with maximum items limit."""
        for i in range(10):
            self.shared_queue.put(f"item{i}")

        consumer = Consumer(
            consumer_id="LIMITED",
            destination_container=self.destination_container,
            shared_queue=self.shared_queue,
            max_items=5
        )

        consumer.start()
        consumer.join()

        self.assertEqual(consumer.get_items_consumed(), 5)
        self.assertEqual(self.destination_container.size(), 5)
        self.assertEqual(self.shared_queue.size(), 5)

    def test_consumer_statistics(self):
        """Test consumer statistics tracking."""
        items = ["item1", "item2", "item3"]
        for item in items:
            self.shared_queue.put(item)

        self.consumer.start()
        time.sleep(0.2)
        self.consumer.stop()
        self.consumer.join(timeout=2)

        self.assertEqual(self.consumer.get_items_consumed(), 3)
        self.assertEqual(self.consumer.items_consumed, 3)

    def test_multiple_consumers(self):
        """Test multiple consumers working concurrently."""
        destination1 = Container("Dest1")
        destination2 = Container("Dest2")
        shared_queue = BlockingQueue(max_size=20)

        for i in range(10):
            shared_queue.put(f"item{i}")

        consumer1 = Consumer(
            consumer_id="C1",
            destination_container=destination1,
            shared_queue=shared_queue,
            consumption_delay=0.01
        )
        consumer2 = Consumer(
            consumer_id="C2",
            destination_container=destination2,
            shared_queue=shared_queue,
            consumption_delay=0.01
        )

        consumer1.start()
        consumer2.start()

        time.sleep(0.5)
        consumer1.stop()
        consumer2.stop()

        consumer1.join(timeout=2)
        consumer2.join(timeout=2)

        total_consumed = consumer1.get_items_consumed() + consumer2.get_items_consumed()
        total_in_destinations = destination1.size() + destination2.size()

        self.assertEqual(total_consumed, total_in_destinations)
        self.assertGreaterEqual(total_consumed, 5)

    def test_consumer_with_zero_delay(self):
        """Test consumer with zero consumption delay."""
        items = ["item1", "item2", "item3"]
        for item in items:
            self.shared_queue.put(item)

        consumer = Consumer(
            consumer_id="NO_DELAY",
            destination_container=self.destination_container,
            shared_queue=self.shared_queue,
            consumption_delay=0.0
        )

        consumer.start()
        time.sleep(0.1)
        consumer.stop()
        consumer.join(timeout=2)

        self.assertEqual(consumer.get_items_consumed(), 3)

    def test_consumer_timeout_handling(self):
        """Test consumer handling of timeout scenarios."""
        consumer = Consumer(
            consumer_id="TIMEOUT",
            destination_container=self.destination_container,
            shared_queue=self.shared_queue,
            consumption_delay=0.01
        )

        consumer.start()
        time.sleep(0.05)
        self.assertEqual(consumer.get_items_consumed(), 0)

        self.shared_queue.put("item1")
        time.sleep(0.1)
        consumer.stop()
        consumer.join(timeout=2)

        self.assertEqual(consumer.get_items_consumed(), 1)


if __name__ == "__main__":
    unittest.main()

