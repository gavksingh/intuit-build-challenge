# Intuit Build Challenge

This repository contains solutions to the Intuit coding challenge assignments implemented in Python.

## Table of Contents

- [Setup Instructions](#setup-instructions)
- [PC-001: Producer-Consumer Pattern](#pc-001-producer-consumer-pattern)
- [SA-001: Sales Analysis](#sa-001-sales-analysis)

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/gavksingh/intuit-build-challenge.git
   cd intuit-build-challenge
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Verify installation:
   ```bash
   python --version
   pytest --version
   ```

### Running the Code

- **PC-001**: Run the demo with `python -m pc_001.producer_consumer`
- **PC-001 Tests**: Run tests with `pytest pc_001/test_producer_consumer.py -v`
- **SA-001**: (To be implemented)

---

## PC-001: Producer-Consumer Pattern

### Overview

Implementation of a classic producer-consumer pattern demonstrating thread synchronization and communication. The program simulates concurrent data transfer between a producer thread that reads from a source container and places items into a shared queue, and a consumer thread that reads from the queue and stores items in a destination container.

### Implementation Details

#### Components

1. **SharedBuffer** (`pc_001/producer_consumer.py`)
   - Bounded buffer acting as a blocking queue
   - Uses `threading.Condition` for thread synchronization
   - Implements blocking `put()` and `get()` methods
   - Blocks when buffer is full (put) or empty (get)
   - Uses `deque` for efficient FIFO operations

2. **Producer** (`pc_001/producer_consumer.py`)
   - Extends `threading.Thread`
   - Reads items from a source list
   - Places items into the shared buffer
   - Sends a sentinel value (`object()`) to signal completion

3. **Consumer** (`pc_001/producer_consumer.py`)
   - Extends `threading.Thread`
   - Reads items from the shared buffer
   - Stores items in a destination list
   - Stops gracefully upon receiving the sentinel value

#### Key Features

- **Thread Synchronization**: Uses `Condition.wait()` and `notify_all()` for proper thread coordination
- **Bounded Buffer**: Configurable capacity prevents unbounded memory growth
- **Blocking Operations**: Producer blocks when buffer is full, consumer blocks when buffer is empty
- **Graceful Shutdown**: Sentinel pattern ensures clean thread termination
- **Type Safety**: Uses `object()` as sentinel to allow legitimate `None` values in data

#### Design Decisions

- **Sentinel Pattern**: Using `object()` instead of `None` allows legitimate `None` payloads to be transferred safely
- **Condition Variables**: Proper wait/notify mechanism ensures thread-safe operations
- **Context Managers**: Automatic lock management with `with self.condition:`
- **FIFO Order**: Maintains item order using `deque` with `append()` and `popleft()`

### Testing

Comprehensive unit tests cover:

- ✅ Basic put/get operations
- ✅ FIFO order preservation
- ✅ Blocking behavior when buffer is full/empty
- ✅ Basic transfer between producer/consumer
- ✅ Order preservation with large datasets
- ✅ Edge cases: empty source, single item, large datasets
- ✅ Sentinel handling
- ✅ Different data types (including `None`)
- ✅ Bounded buffer capacity enforcement

**Test Results**: 12 tests passing, 2 skipped (0.35s)

Run tests:
```bash
pytest pc_001/test_producer_consumer.py -v
```

### Sample Output

```
Source:      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Destination: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Verification Screenshots

_(Terminal screenshots will be added here)_

---

## SA-001: Sales Analysis

_(To be implemented)_

---

## Requirements Coverage

### PC-001 Testing Objectives ✅

- ✅ **Thread synchronization**: Condition variables with wait/notify mechanism
- ✅ **Concurrent programming**: Multiple threads running simultaneously
- ✅ **Blocking queues**: Bounded buffer with blocking put/get operations
- ✅ **Wait/Notify mechanism**: Proper use of `condition.wait()` and `notify_all()`

---

## License

This project is part of the Intuit Build Challenge.
