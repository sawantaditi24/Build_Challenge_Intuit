"""
Producer thread implementation for the producer-consumer pattern.
Reads items from a source container and places them into a shared blocking queue.
"""

import threading
import time
from typing import Optional
from .container import Container
from .blocking_queue import BlockingQueue


class Producer(threading.Thread):
    """
    Producer thread that reads items from a source container
    and places them into a shared blocking queue.
    """

    def __init__(
        self,
        producer_id: str,
        source_container: Container,
        shared_queue: BlockingQueue,
        production_delay: float = 0.1,
        max_items: Optional[int] = None
    ):
        """
        Initialize the producer thread.

        Args:
            producer_id: Unique identifier for this producer
            source_container: Container to read items from
            shared_queue: Shared blocking queue to place items into
            production_delay: Delay between producing items in seconds (default: 0.1)
            max_items: Maximum number of items to produce (None for all items in source)
        """
        super().__init__(name=f"Producer-{producer_id}", daemon=False)
        self.producer_id = producer_id
        self.source_container = source_container
        self.shared_queue = shared_queue
        self.production_delay = production_delay
        self.max_items = max_items
        self.items_produced = 0
        self._stop_event = threading.Event()

    def run(self) -> None:
        """
        Main execution method for the producer thread.
        Reads items from source container and places them into the shared queue.
        """
        items_to_produce = self.max_items if self.max_items is not None else self.source_container.size()
        items_produced_count = 0
        # Use a short timeout to allow checking stop event periodically
        queue_timeout = 0.1

        while items_produced_count < items_to_produce and not self._stop_event.is_set():
            # Check if source container has items
            if self.source_container.is_empty():
                break

            # Get item from source container
            item = self.source_container.remove_item(0)
            if item is None:
                break

            # Place item into shared queue with timeout to allow stop event checking
            success = self.shared_queue.put(item, timeout=queue_timeout)
            if success:
                items_produced_count += 1
                self.items_produced = items_produced_count
                print(f"[{self.name}] Produced item: {item} (Total: {items_produced_count})")
            else:
                # Timeout occurred - check stop event and continue loop
                if self._stop_event.is_set():
                    break
                continue

            # Simulate production delay with interruptible sleep
            # Break sleep into small chunks to allow stop event checking
            if self.production_delay > 0:
                sleep_interval = 0.05  # Check stop event every 50ms
                elapsed = 0.0
                while elapsed < self.production_delay and not self._stop_event.is_set():
                    time.sleep(min(sleep_interval, self.production_delay - elapsed))
                    elapsed += sleep_interval

        print(f"[{self.name}] Finished producing. Total items produced: {items_produced_count}")

    def stop(self) -> None:
        """
        Signal the producer to stop producing items.
        """
        self._stop_event.set()

    def get_items_produced(self) -> int:
        """
        Get the number of items produced by this producer.

        Returns:
            Number of items produced
        """
        return self.items_produced

