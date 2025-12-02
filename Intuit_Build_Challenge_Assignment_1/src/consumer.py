"""
Consumer thread implementation for the producer-consumer pattern.
Reads items from a shared blocking queue and stores them in a destination container.
"""

import threading
import time
from typing import Optional
from .container import Container
from .blocking_queue import BlockingQueue


class Consumer(threading.Thread):
    """
    Consumer thread that reads items from a shared blocking queue
    and stores them in a destination container.
    """

    def __init__(
        self,
        consumer_id: str,
        destination_container: Container,
        shared_queue: BlockingQueue,
        consumption_delay: float = 0.1,
        max_items: Optional[int] = None
    ):
        """
        Initialize the consumer thread.

        Args:
            consumer_id: Unique identifier for this consumer
            destination_container: Container to store consumed items
            shared_queue: Shared blocking queue to read items from
            consumption_delay: Delay between consuming items in seconds (default: 0.1)
            max_items: Maximum number of items to consume (None for unlimited)
        """
        super().__init__(name=f"Consumer-{consumer_id}", daemon=False)
        self.consumer_id = consumer_id
        self.destination_container = destination_container
        self.shared_queue = shared_queue
        self.consumption_delay = consumption_delay
        self.max_items = max_items
        self.items_consumed = 0
        self._stop_event = threading.Event()

    def run(self) -> None:
        """
        Main execution method for the consumer thread.
        Reads items from shared queue and stores them in destination container.
        """
        items_consumed_count = 0
        # Use a short timeout to allow checking stop event periodically
        queue_timeout = 0.1

        while not self._stop_event.is_set():
            # Check if we've reached the maximum items to consume
            if self.max_items is not None and items_consumed_count >= self.max_items:
                break

            # Get item from shared queue with timeout to allow stop event checking
            item = self.shared_queue.get(timeout=queue_timeout)
            if item is None:
                # Timeout occurred - check stop event and continue loop
                continue

            # Store item in destination container
            self.destination_container.add_item(item)
            items_consumed_count += 1
            self.items_consumed = items_consumed_count
            print(f"[{self.name}] Consumed item: {item} (Total: {items_consumed_count})")

            # Simulate consumption delay with interruptible sleep
            # Break sleep into small chunks to allow stop event checking
            if self.consumption_delay > 0:
                sleep_interval = 0.05  # Check stop event every 50ms
                elapsed = 0.0
                while elapsed < self.consumption_delay and not self._stop_event.is_set():
                    time.sleep(min(sleep_interval, self.consumption_delay - elapsed))
                    elapsed += sleep_interval
            
            # Check stop event after processing item
            if self._stop_event.is_set():
                break

        print(f"[{self.name}] Finished consuming. Total items consumed: {items_consumed_count}")

    def stop(self) -> None:
        """
        Signal the consumer to stop consuming items.
        """
        self._stop_event.set()

    def get_items_consumed(self) -> int:
        """
        Get the number of items consumed by this consumer.

        Returns:
            Number of items consumed
        """
        return self.items_consumed

