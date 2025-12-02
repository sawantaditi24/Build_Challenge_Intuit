"""
Unit tests for Producer class.
Tests producer thread functionality, item production, and synchronization.
"""

import unittest
import threading
import time
from src.producer import Producer
from src.container import Container
from src.blocking_queue import BlockingQueue


class TestProducer(unittest.TestCase):
    """Test cases for Producer implementation."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.source_container = Container("TestSource", ["item1", "item2", "item3"])
        self.shared_queue = BlockingQueue(max_size=10)
        self.producer = Producer(
            producer_id="TEST",
            source_container=self.source_container,
            shared_queue=self.shared_queue,
            production_delay=0.01
        )

    def test_producer_initialization(self):
        """Test producer thread initialization."""
        self.assertEqual(self.producer.producer_id, "TEST")
        self.assertEqual(self.producer.source_container, self.source_container)
        self.assertEqual(self.producer.shared_queue, self.shared_queue)
        self.assertEqual(self.producer.production_delay, 0.01)
        self.assertEqual(self.producer.items_produced, 0)
        self.assertFalse(self.producer.is_alive())

    def test_producer_name(self):
        """Test that producer thread has correct name."""
        self.assertEqual(self.producer.name, "Producer-TEST")

    def test_producer_produces_items(self):
        """Test that producer successfully produces items from source."""
        self.producer.start()
        self.producer.join()

        self.assertEqual(self.producer.get_items_produced(), 3)
        self.assertEqual(self.shared_queue.size(), 3)
        self.assertTrue(self.source_container.is_empty())

    def test_producer_places_items_in_queue(self):
        """Test that producer places items into shared queue."""
        self.producer.start()
        self.producer.join()

        items_in_queue = []
        while not self.shared_queue.is_empty():
            items_in_queue.append(self.shared_queue.get())

        self.assertEqual(len(items_in_queue), 3)
        self.assertIn("item1", items_in_queue)
        self.assertIn("item2", items_in_queue)
        self.assertIn("item3", items_in_queue)

    def test_producer_with_empty_source(self):
        """Test producer behavior with empty source container."""
        empty_container = Container("Empty")
        producer = Producer(
            producer_id="EMPTY",
            source_container=empty_container,
            shared_queue=self.shared_queue
        )

        producer.start()
        producer.join()

        self.assertEqual(producer.get_items_produced(), 0)
        self.assertTrue(self.shared_queue.is_empty())

    def test_producer_with_max_items_limit(self):
        """Test producer with maximum items limit."""
        large_container = Container("Large", [f"item{i}" for i in range(10)])
        producer = Producer(
            producer_id="LIMITED",
            source_container=large_container,
            shared_queue=self.shared_queue,
            max_items=5
        )

        producer.start()
        producer.join()

        self.assertEqual(producer.get_items_produced(), 5)
        self.assertEqual(self.shared_queue.size(), 5)
        self.assertEqual(large_container.size(), 5)

    def test_producer_stop_signal(self):
        """Test that producer responds to stop signal."""
        large_container = Container("Large", [f"item{i}" for i in range(100)])
        producer = Producer(
            producer_id="STOPPABLE",
            source_container=large_container,
            shared_queue=self.shared_queue,
            production_delay=0.1
        )

        producer.start()
        time.sleep(0.3)
        producer.stop()
        producer.join(timeout=2)

        items_produced = producer.get_items_produced()
        self.assertGreater(items_produced, 0)
        self.assertLess(items_produced, 100)

    def test_producer_with_full_queue(self):
        """Test producer behavior when queue is full."""
        small_queue = BlockingQueue(max_size=2)
        producer = Producer(
            producer_id="FULL_QUEUE",
            source_container=self.source_container,
            shared_queue=small_queue,
            production_delay=0.05
        )

        producer.start()
        time.sleep(0.2)
        producer.stop()
        producer.join(timeout=2)

        self.assertEqual(small_queue.size(), 2)
        self.assertLessEqual(producer.get_items_produced(), 3)

    def test_producer_statistics(self):
        """Test producer statistics tracking."""
        self.producer.start()
        self.producer.join()

        self.assertEqual(self.producer.get_items_produced(), 3)
        self.assertEqual(self.producer.items_produced, 3)

    def test_multiple_producers(self):
        """Test multiple producers working concurrently."""
        container1 = Container("Source1", ["A1", "A2", "A3"])
        container2 = Container("Source2", ["B1", "B2", "B3"])
        shared_queue = BlockingQueue(max_size=20)

        producer1 = Producer(
            producer_id="P1",
            source_container=container1,
            shared_queue=shared_queue,
            production_delay=0.01
        )
        producer2 = Producer(
            producer_id="P2",
            source_container=container2,
            shared_queue=shared_queue,
            production_delay=0.01
        )

        producer1.start()
        producer2.start()

        producer1.join()
        producer2.join()

        self.assertEqual(producer1.get_items_produced(), 3)
        self.assertEqual(producer2.get_items_produced(), 3)
        self.assertEqual(shared_queue.size(), 6)
        self.assertTrue(container1.is_empty())
        self.assertTrue(container2.is_empty())

    def test_producer_with_zero_delay(self):
        """Test producer with zero production delay."""
        producer = Producer(
            producer_id="NO_DELAY",
            source_container=self.source_container,
            shared_queue=self.shared_queue,
            production_delay=0.0
        )

        producer.start()
        producer.join()

        self.assertEqual(producer.get_items_produced(), 3)


if __name__ == "__main__":
    unittest.main()

