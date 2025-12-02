"""
Thread-safe blocking queue implementation using Condition variables.
Demonstrates wait/notify mechanism for producer-consumer synchronization.
"""

from typing import Any, Optional
from threading import Condition, Lock
from collections import deque


class BlockingQueue:
    """
    Thread-safe blocking queue that supports blocking put and get operations.
    Uses Condition variables to implement wait/notify mechanism for thread synchronization.
    """

    def __init__(self, max_size: int = 10):
        """
        Initialize the blocking queue with a maximum size.

        Args:
            max_size: Maximum number of items the queue can hold (default: 10)
        """
        if max_size <= 0:
            raise ValueError("Queue size must be greater than 0")
        self._max_size = max_size
        self._queue = deque()
        self._lock = Lock()
        self._not_empty = Condition(self._lock)  # Condition for consumer waiting
        self._not_full = Condition(self._lock)   # Condition for producer waiting

    def put(self, item: Any, timeout: Optional[float] = None) -> bool:
        """
        Add an item to the queue, blocking if the queue is full.
        Uses wait/notify mechanism to synchronize with consumer threads.

        Args:
            item: The item to add to the queue
            timeout: Optional timeout in seconds (None for indefinite wait)

        Returns:
            True if item was successfully added, False if timeout occurred
        """
        with self._lock:
            # Wait until queue is not full
            while len(self._queue) >= self._max_size:
                if timeout is not None:
                    if not self._not_full.wait(timeout=timeout):
                        return False
                else:
                    self._not_full.wait()

            # Add item to queue
            self._queue.append(item)

            # Notify waiting consumers that queue is not empty
            self._not_empty.notify()
            return True

    def get(self, timeout: Optional[float] = None) -> Optional[Any]:
        """
        Remove and return an item from the queue, blocking if the queue is empty.
        Uses wait/notify mechanism to synchronize with producer threads.

        Args:
            timeout: Optional timeout in seconds (None for indefinite wait)

        Returns:
            The item removed from the queue, or None if timeout occurred
        """
        with self._lock:
            # Wait until queue is not empty
            while len(self._queue) == 0:
                if timeout is not None:
                    if not self._not_empty.wait(timeout=timeout):
                        return None
                else:
                    self._not_empty.wait()

            # Remove and return item from queue
            item = self._queue.popleft()

            # Notify waiting producers that queue is not full
            self._not_full.notify()
            return item

    def size(self) -> int:
        """
        Get the current number of items in the queue in a thread-safe manner.

        Returns:
            Number of items currently in the queue
        """
        with self._lock:
            return len(self._queue)

    def is_empty(self) -> bool:
        """
        Check if the queue is empty in a thread-safe manner.

        Returns:
            True if queue is empty, False otherwise
        """
        with self._lock:
            return len(self._queue) == 0

    def is_full(self) -> bool:
        """
        Check if the queue is full in a thread-safe manner.

        Returns:
            True if queue is full, False otherwise
        """
        with self._lock:
            return len(self._queue) >= self._max_size

    def max_size(self) -> int:
        """
        Get the maximum size of the queue.

        Returns:
            Maximum number of items the queue can hold
        """
        return self._max_size

