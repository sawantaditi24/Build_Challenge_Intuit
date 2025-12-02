"""
Main application demonstrating the producer-consumer pattern.
Simulates concurrent data transfer between producer and consumer threads.
"""

import time
from src.container import Container
from src.blocking_queue import BlockingQueue
from src.producer import Producer
from src.consumer import Consumer


def main():
    """
    Main function that demonstrates the producer-consumer pattern.
    Creates source and destination containers, a shared blocking queue,
    and starts producer and consumer threads.
    """
    print("=" * 80)
    print("Producer-Consumer Pattern Demonstration")
    print("=" * 80)
    print()

    # Configuration parameters
    queue_size = 5
    num_items = 20
    production_delay = 0.1
    consumption_delay = 0.15

    # Create source container with initial items
    source_items = [f"Item-{i}" for i in range(1, num_items + 1)]
    source_container = Container("Source", source_items)
    print(f"Initialized source container with {source_container.size()} items")
    print(f"Source items: {source_container.get_all_items()}")
    print()

    # Create destination container (initially empty)
    destination_container = Container("Destination")
    print(f"Initialized destination container (empty)")
    print()

    # Create shared blocking queue
    shared_queue = BlockingQueue(max_size=queue_size)
    print(f"Created shared blocking queue with max size: {queue_size}")
    print()

    # Create producer thread
    producer = Producer(
        producer_id="P1",
        source_container=source_container,
        shared_queue=shared_queue,
        production_delay=production_delay
    )
    print(f"Created producer thread: {producer.name}")
    print(f"Production delay: {production_delay} seconds")
    print()

    # Create consumer thread
    consumer = Consumer(
        consumer_id="C1",
        destination_container=destination_container,
        shared_queue=shared_queue,
        consumption_delay=consumption_delay
    )
    print(f"Created consumer thread: {consumer.name}")
    print(f"Consumption delay: {consumption_delay} seconds")
    print()

    print("=" * 80)
    print("Starting Producer-Consumer Simulation")
    print("=" * 80)
    print()

    # Start consumer first to demonstrate blocking behavior
    consumer.start()
    time.sleep(0.05)  # Small delay to ensure consumer starts first

    # Start producer
    producer.start()

    # Wait for producer to finish
    producer.join()
    print()

    # Give consumer time to process remaining items
    time.sleep(1)

    # Signal consumer to stop (in case it's waiting for more items)
    consumer.stop()
    consumer.join(timeout=2)

    print()
    print("=" * 80)
    print("Simulation Results")
    print("=" * 80)
    print()

    # Display results
    print(f"Source container status: {source_container}")
    print(f"Source container remaining items: {source_container.get_all_items()}")
    print()

    print(f"Destination container status: {destination_container}")
    print(f"Destination container items: {destination_container.get_all_items()}")
    print()

    print(f"Shared queue status:")
    print(f"  - Current size: {shared_queue.size()}")
    print(f"  - Is empty: {shared_queue.is_empty()}")
    print(f"  - Is full: {shared_queue.is_full()}")
    print()

    print(f"Producer statistics:")
    print(f"  - Items produced: {producer.get_items_produced()}")
    print()

    print(f"Consumer statistics:")
    print(f"  - Items consumed: {consumer.get_items_consumed()}")
    print()

    # Verify data integrity
    total_expected = num_items
    total_produced = producer.get_items_produced()
    total_consumed = consumer.get_items_consumed()
    total_in_destination = destination_container.size()
    total_remaining_in_source = source_container.size()
    total_in_queue = shared_queue.size()

    print("=" * 80)
    print("Data Integrity Verification")
    print("=" * 80)
    print(f"Total items initially: {total_expected}")
    print(f"Items produced: {total_produced}")
    print(f"Items consumed: {total_consumed}")
    print(f"Items in destination: {total_in_destination}")
    print(f"Items remaining in source: {total_remaining_in_source}")
    print(f"Items in queue: {total_in_queue}")
    print()

    # Calculate totals
    total_accounted = total_in_destination + total_remaining_in_source + total_in_queue

    if total_accounted == total_expected:
        print("SUCCESS: All items are accounted for. Data integrity maintained.")
    else:
        print(f"WARNING: Item count mismatch. Expected {total_expected}, accounted for {total_accounted}")

    print()
    print("=" * 80)
    print("Simulation Complete")
    print("=" * 80)


if __name__ == "__main__":
    main()

