# Producer-Consumer Pattern Implementation

## Overview

This project implements a classic producer-consumer pattern demonstrating thread synchronization and communication in Python. The program simulates concurrent data transfer between a producer thread that reads from a source container and places items into a shared queue, and a consumer thread that reads from the queue and stores items in a destination container.

## Features

- Thread-safe blocking queue implementation using Condition variables
- Producer thread that reads from source container and places items in shared queue
- Consumer thread that reads from shared queue and stores items in destination container
- Comprehensive unit tests covering all components
- Integration tests for end-to-end functionality
- Proper thread synchronization using wait/notify mechanism
- Data integrity verification

## Project Structure

```
Intuit_Build_Challenge_Assignment_1/
├── src/
│   ├── __init__.py
│   ├── blocking_queue.py      # Thread-safe blocking queue implementation
│   ├── container.py           # Thread-safe container for source/destination
│   ├── producer.py            # Producer thread implementation
│   └── consumer.py            # Consumer thread implementation
├── tests/
│   ├── __init__.py
│   ├── test_blocking_queue.py # Unit tests for blocking queue
│   ├── test_container.py      # Unit tests for container
│   ├── test_producer.py       # Unit tests for producer
│   ├── test_consumer.py       # Unit tests for consumer
│   └── test_integration.py    # Integration tests
├── main.py                    # Main application entry point
├── README.md                  # This file
├── SETUP.md                   # Detailed setup instructions
└── DESIGN_DECISION.md         # Design decisions, thought process, and assumptions
```

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only Python standard library)

## Setup Instructions

### 1. Verify Python Installation

```bash
python3 --version
```

Ensure Python 3.7 or higher is installed.

### 2. Clone or Navigate to Project Directory

```bash
cd Intuit_Build_Challenge_Assignment_1
```

### 3. Verify Project Structure

Ensure all files are present in the project directory as shown in the Project Structure section above.

### 4. Run the Application

```bash
python3 main.py
```

### 5. Run Unit Tests

To run all unit tests:

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

To run a specific test file:

```bash
python3 -m unittest tests.test_blocking_queue -v
python3 -m unittest tests.test_producer -v
python3 -m unittest tests.test_consumer -v
python3 -m unittest tests.test_container -v
python3 -m unittest tests.test_integration -v
```

## Sample Output

When running `main.py`, you should see output similar to:

```
================================================================================
Producer-Consumer Pattern Demonstration
================================================================================

Initialized source container with 20 items
Source items: ['Item-1', 'Item-2', 'Item-3', ...]

Initialized destination container (empty)

Created shared blocking queue with max size: 5

Created producer thread: Producer-P1
Production delay: 0.1 seconds

Created consumer thread: Consumer-C1
Consumption delay: 0.15 seconds

================================================================================
Starting Producer-Consumer Simulation
================================================================================

[Producer-P1] Produced item: Item-1 (Total: 1)
[Consumer-C1] Consumed item: Item-1 (Total: 1)
[Producer-P1] Produced item: Item-2 (Total: 2)
[Consumer-C1] Consumed item: Item-2 (Total: 2)
...

================================================================================
Simulation Results
================================================================================

Source container status: Source (items: 0)
Source container remaining items: []

Destination container status: Destination (items: 20)
Destination container items: ['Item-1', 'Item-2', 'Item-3', ...]

Shared queue status:
  - Current size: 0
  - Is empty: True
  - Is full: False

Producer statistics:
  - Items produced: 20

Consumer statistics:
  - Items consumed: 20

================================================================================
Data Integrity Verification
================================================================================
Total items initially: 20
Items produced: 20
Items consumed: 20
Items in destination: 20
Items remaining in source: 0
Items in queue: 0

SUCCESS: All items are accounted for. Data integrity maintained.

================================================================================
Simulation Complete
================================================================================
```


## Console Outputs:

Producer-Consumer pattern demonstration
<img width="1306" height="325" alt="Demonstration - Console" src="https://github.com/user-attachments/assets/911058c3-8e82-4c5d-a7fe-38cf18cb7603" />

Producer-Consumer simulation
<img width="1298" height="938" alt="Simulation - Console" src="https://github.com/user-attachments/assets/76a80f37-fcd8-40be-a864-d0b21fa52f1a" />

Simulation results and Data Integrity verification
<img width="1300" height="554" alt="Screenshot 2025-12-02 at 12 54 08 AM" src="https://github.com/user-attachments/assets/9e54a7f1-5b76-438a-b0e5-f4d48e5f2f96" />


## Key Components

### BlockingQueue

Thread-safe blocking queue that supports blocking put and get operations. Uses Condition variables to implement wait/notify mechanism for thread synchronization.

- `put(item, timeout=None)`: Add item to queue, blocking if full
- `get(timeout=None)`: Remove and return item from queue, blocking if empty
- `size()`: Get current queue size
- `is_empty()`: Check if queue is empty
- `is_full()`: Check if queue is full

### Producer

Thread that reads items from a source container and places them into a shared blocking queue.

- Reads items from source container
- Places items into shared queue (blocking operation)
- Tracks items produced
- Supports production delay simulation

### Consumer

Thread that reads items from a shared blocking queue and stores them in a destination container.

- Reads items from shared queue (blocking operation)
- Stores items in destination container
- Tracks items consumed
- Supports consumption delay simulation

### Container

Thread-safe container for storing items, used as both source and destination containers.

- Thread-safe add, get, and remove operations
- Supports initial items on creation
- Provides size and empty checks

## Testing

The project includes comprehensive unit tests covering:

- Blocking queue operations and thread synchronization
- Producer thread functionality
- Consumer thread functionality
- Container thread safety
- Integration tests for complete producer-consumer flow
- Multiple producer/consumer scenarios
- Data integrity verification

All tests can be run using Python's unittest framework.

## Design Decisions

For detailed information about design decisions, assumptions, and thought process, please refer to **[DESIGN_DECISION.md](DESIGN_DECISION.md)**.

This document is crucial for understanding the implementation approach, as it explains:
- **Architecture decisions**: Why specific design patterns were chosen
- **Implementation rationale**: Trade-offs and alternatives considered
- **Thread synchronization strategy**: How wait/notify mechanism was implemented
- **Testing approach**: Comprehensive test coverage strategy
- **Assumptions and constraints**: Key considerations during development

## Thread Synchronization

The implementation uses Python's `threading.Condition` variables to implement the wait/notify mechanism:

- Producers wait when queue is full (`_not_full` condition)
- Consumers wait when queue is empty (`_not_empty` condition)
- Proper notification when conditions change
- Thread-safe operations using locks

## Best Practices

- All operations are thread-safe
- Proper error handling and validation
- Comprehensive unit tests
- Clear code documentation
- Modular and extensible design
- Production-ready code quality

## License

This project is part of the Intuit Build Challenge assignment.

