"""
Integration tests for the complete producer-consumer system.
Tests end-to-end functionality and data integrity.
"""

import unittest
import threading
import time
from src.container import Container
from src.blocking_queue import BlockingQueue
from src.producer import Producer
from src.consumer import Consumer


class TestProducerConsumerIntegration(unittest.TestCase):
    """Integration test cases for producer-consumer pattern."""

    def test_basic_producer_consumer_flow(self):
        """Test basic producer-consumer data transfer."""
        source_items = [f"Item-{i}" for i in range(1, 11)]
        source_container = Container("Source", source_items)
        destination_container = Container("Destination")
        shared_queue = BlockingQueue(max_size=5)

        producer = Producer(
            producer_id="P1",
            source_container=source_container,
            shared_queue=shared_queue,
            production_delay=0.01
        )

        consumer = Consumer(
            consumer_id="C1",
            destination_container=destination_container,
            shared_queue=shared_queue,
            consumption_delay=0.01
        )

        consumer.start()
        producer.start()

        producer.join()
        time.sleep(0.2)
        consumer.stop()
        consumer.join(timeout=2)

        self.assertEqual(producer.get_items_produced(), 10)
        self.assertEqual(consumer.get_items_consumed(), 10)
        self.assertEqual(destination_container.size(), 10)
        self.assertTrue(source_container.is_empty())
        self.assertTrue(shared_queue.is_empty())

    def test_data_integrity(self):
        """Test that all data is correctly transferred without loss."""
        num_items = 50
        source_items = [f"Item-{i}" for i in range(1, num_items + 1)]
        source_container = Container("Source", source_items)
        destination_container = Container("Destination")
        shared_queue = BlockingQueue(max_size=10)

        producer = Producer(
            producer_id="P1",
            source_container=source_container,
            shared_queue=shared_queue,
            production_delay=0.01
        )

        consumer = Consumer(
            consumer_id="C1",
            destination_container=destination_container,
            shared_queue=shared_queue,
            consumption_delay=0.01
        )

        consumer.start()
        producer.start()

        producer.join()
        time.sleep(0.5)
        consumer.stop()
        consumer.join(timeout=3)

        source_items_set = set(source_items)
        destination_items = destination_container.get_all_items()
        destination_items_set = set(destination_items)

        self.assertEqual(len(destination_items_set), num_items)
        self.assertEqual(source_items_set, destination_items_set)

    def test_multiple_producers_single_consumer(self):
        """Test multiple producers with single consumer."""
        source1 = Container("Source1", [f"A-{i}" for i in range(1, 6)])
        source2 = Container("Source2", [f"B-{i}" for i in range(1, 6)])
        destination = Container("Destination")
        shared_queue = BlockingQueue(max_size=10)

        producer1 = Producer(
            producer_id="P1",
            source_container=source1,
            shared_queue=shared_queue,
            production_delay=0.01
        )

        producer2 = Producer(
            producer_id="P2",
            source_container=source2,
            shared_queue=shared_queue,
            production_delay=0.01
        )

        consumer = Consumer(
            consumer_id="C1",
            destination_container=destination,
            shared_queue=shared_queue,
            consumption_delay=0.01
        )

        consumer.start()
        producer1.start()
        producer2.start()

        producer1.join()
        producer2.join()
        time.sleep(0.3)
        consumer.stop()
        consumer.join(timeout=3)

        total_produced = producer1.get_items_produced() + producer2.get_items_produced()
        total_consumed = consumer.get_items_consumed()
        total_in_destination = destination.size()

        self.assertEqual(total_produced, 10)
        self.assertEqual(total_consumed, total_in_destination)
        self.assertGreaterEqual(total_consumed, 8)

    def test_single_producer_multiple_consumers(self):
        """Test single producer with multiple consumers."""
        source = Container("Source", [f"Item-{i}" for i in range(1, 21)])
        destination1 = Container("Destination1")
        destination2 = Container("Destination2")
        shared_queue = BlockingQueue(max_size=10)

        producer = Producer(
            producer_id="P1",
            source_container=source,
            shared_queue=shared_queue,
            production_delay=0.01
        )

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
        producer.start()

        producer.join()
        time.sleep(0.5)
        consumer1.stop()
        consumer2.stop()
        consumer1.join(timeout=3)
        consumer2.join(timeout=3)

        total_consumed = consumer1.get_items_consumed() + consumer2.get_items_consumed()
        total_in_destinations = destination1.size() + destination2.size()

        self.assertEqual(producer.get_items_produced(), 20)
        self.assertEqual(total_consumed, total_in_destinations)
        self.assertGreaterEqual(total_consumed, 15)

    def test_queue_size_limitation(self):
        """Test that queue size limitation works correctly."""
        source = Container("Source", [f"Item-{i}" for i in range(1, 21)])
        destination = Container("Destination")
        small_queue = BlockingQueue(max_size=3)

        producer = Producer(
            producer_id="P1",
            source_container=source,
            shared_queue=small_queue,
            production_delay=0.05
        )

        consumer = Consumer(
            consumer_id="C1",
            destination_container=destination,
            shared_queue=small_queue,
            consumption_delay=0.05
        )

        consumer.start()
        producer.start()

        time.sleep(0.3)
        queue_size = small_queue.size()
        self.assertLessEqual(queue_size, 3)

        producer.join()
        time.sleep(0.5)
        consumer.stop()
        consumer.join(timeout=3)

        self.assertLessEqual(small_queue.size(), 3)

    def test_different_production_consumption_rates(self):
        """Test system with different production and consumption rates."""
        source = Container("Source", [f"Item-{i}" for i in range(1, 11)])
        destination = Container("Destination")
        shared_queue = BlockingQueue(max_size=5)

        producer = Producer(
            producer_id="P1",
            source_container=source,
            shared_queue=shared_queue,
            production_delay=0.05
        )

        consumer = Consumer(
            consumer_id="C1",
            destination_container=destination,
            shared_queue=shared_queue,
            consumption_delay=0.1
        )

        consumer.start()
        producer.start()

        producer.join()
        time.sleep(1.0)
        consumer.stop()
        consumer.join(timeout=3)

        self.assertEqual(producer.get_items_produced(), 10)
        self.assertEqual(consumer.get_items_consumed(), destination.size())

    def test_concurrent_producer_consumer_operations(self):
        """Test concurrent operations with timing variations."""
        source = Container("Source", [f"Item-{i}" for i in range(1, 31)])
        destination = Container("Destination")
        shared_queue = BlockingQueue(max_size=8)

        producer = Producer(
            producer_id="P1",
            source_container=source,
            shared_queue=shared_queue,
            production_delay=0.02
        )

        consumer = Consumer(
            consumer_id="C1",
            destination_container=destination,
            shared_queue=shared_queue,
            consumption_delay=0.03
        )

        consumer.start()
        time.sleep(0.05)
        producer.start()

        producer.join()
        time.sleep(0.8)
        consumer.stop()
        consumer.join(timeout=3)

        total_accounted = (
            destination.size() +
            source.size() +
            shared_queue.size()
        )

        self.assertEqual(total_accounted, 30)
        self.assertEqual(producer.get_items_produced() + source.size(), 30)


if __name__ == "__main__":
    unittest.main()

