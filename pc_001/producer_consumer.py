# pc_001/producer_consumer.py
from threading import Thread, Condition
from collections import deque
from typing import Deque, List, Any


class SharedBuffer:
    """Bounded buffer acting as a blocking queue for producer-consumer."""

    def __init__(self, capacity: int = 10) -> None:
        self.capacity = capacity
        self.buffer: Deque[Any] = deque()
        self.condition = Condition()

    def put(self, item: Any) -> None:
        """Blocking put: waits if buffer is full."""
        with self.condition:
            while len(self.buffer) >= self.capacity:
                self.condition.wait()
            self.buffer.append(item)
            self.condition.notify_all()

    def get(self) -> Any:
        """Blocking get: waits if buffer is empty."""
        with self.condition:
            while not self.buffer:
                self.condition.wait()
            item = self.buffer.popleft()
            self.condition.notify_all()
            return item


# Sentinel value to signal end of data.
# Using a unique object allows legitimate None payloads to be transferred safely.
SENTINEL = object()


class Producer(Thread):
    """Reads from a source list and pushes items into the shared buffer."""

    def __init__(self, source: List[Any], buffer: SharedBuffer) -> None:
        super().__init__()
        self.source = source
        self.buffer = buffer

    def run(self) -> None:
        """Read from source and put items into buffer, then send sentinel."""
        for item in self.source:
            self.buffer.put(item)
        # Signal consumer that production is complete
        self.buffer.put(SENTINEL)


class Consumer(Thread):
    """Reads items from the shared buffer and stores them in destination list."""

    def __init__(self, buffer: SharedBuffer, destination: List[Any]) -> None:
        super().__init__()
        self.buffer = buffer
        self.destination = destination

    def run(self) -> None:
        """Read from buffer and store in destination until sentinel is received."""
        while True:
            item = self.buffer.get()
            if item is SENTINEL:
                # End of data signal received, stop consuming
                break
            self.destination.append(item)


def run_demo() -> None:
    """Run a simple producer-consumer demo."""
    # Create source data
    source = list(range(10))
    destination: List[int] = []
    
    # Create shared buffer with small capacity to demonstrate blocking
    buffer = SharedBuffer(capacity=3)
    
    # Create producer and consumer threads
    producer = Producer(source, buffer)
    consumer = Consumer(buffer, destination)
    
    # Start both threads
    producer.start()
    consumer.start()
    
    # Wait for both threads to complete
    producer.join()
    consumer.join()
    
    # Display results
    print("Source:     ", source)
    print("Destination:", destination)


if __name__ == "__main__":
    run_demo()
