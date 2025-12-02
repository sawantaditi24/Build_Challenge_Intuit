"""
Container classes for source and destination storage.
Provides thread-safe operations for data storage and retrieval.
"""

from typing import List, Any, Optional
from threading import Lock


class Container:
    """
    Thread-safe container for storing items.
    Used as both source and destination containers in the producer-consumer pattern.
    """

    def __init__(self, name: str, initial_items: Optional[List[Any]] = None):
        """
        Initialize the container with a name and optional initial items.

        Args:
            name: Name identifier for the container
            initial_items: Optional list of items to initialize the container with
        """
        self.name = name
        self._items: List[Any] = initial_items.copy() if initial_items else []
        self._lock = Lock()

    def add_item(self, item: Any) -> None:
        """
        Add an item to the container in a thread-safe manner.

        Args:
            item: The item to add to the container
        """
        with self._lock:
            self._items.append(item)

    def get_item(self, index: int = 0) -> Optional[Any]:
        """
        Retrieve an item from the container by index in a thread-safe manner.

        Args:
            index: Index of the item to retrieve (default: 0)

        Returns:
            The item at the specified index, or None if index is out of range
        """
        with self._lock:
            if 0 <= index < len(self._items):
                return self._items[index]
            return None

    def remove_item(self, index: int = 0) -> Optional[Any]:
        """
        Remove and return an item from the container by index in a thread-safe manner.

        Args:
            index: Index of the item to remove (default: 0)

        Returns:
            The removed item, or None if index is out of range
        """
        with self._lock:
            if 0 <= index < len(self._items):
                return self._items.pop(index)
            return None

    def is_empty(self) -> bool:
        """
        Check if the container is empty in a thread-safe manner.

        Returns:
            True if container is empty, False otherwise
        """
        with self._lock:
            return len(self._items) == 0

    def size(self) -> int:
        """
        Get the number of items in the container in a thread-safe manner.

        Returns:
            Number of items in the container
        """
        with self._lock:
            return len(self._items)

    def get_all_items(self) -> List[Any]:
        """
        Get a copy of all items in the container in a thread-safe manner.

        Returns:
            A copy of the list of all items
        """
        with self._lock:
            return self._items.copy()

    def clear(self) -> None:
        """
        Clear all items from the container in a thread-safe manner.
        """
        with self._lock:
            self._items.clear()

    def __str__(self) -> str:
        """
        String representation of the container.

        Returns:
            String representation showing container name and item count
        """
        with self._lock:
            return f"{self.name} (items: {len(self._items)})"

