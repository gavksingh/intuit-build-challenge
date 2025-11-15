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
- **SA-001**: Run the analysis with `python -m sa_001.sales_analysis`
- **SA-001 Tests**: Run tests with `pytest sa_001/test_sales_analysis.py -v`

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

### Overview

Data analysis application demonstrating proficiency with pandas and functional programming paradigms. The program performs various aggregation and grouping operations on sales data from CSV format, using lambda expressions, method chaining, and stream-like operations.

### Implementation Details

#### Components

1. **load_sales_data()** (`sa_001/sales_analysis.py`)
   - Loads CSV data into pandas DataFrame
   - Parses date column automatically
   - Returns structured data ready for analysis

2. **add_revenue_column()** (`sa_001/sales_analysis.py`)
   - Uses `.assign()` with lambda expression
   - Calculates revenue: `quantity * unit_price * (1 - discount)`
   - Returns new DataFrame without modifying original (immutable)

3. **Aggregation Functions** (`sa_001/sales_analysis.py`)
   - `total_revenue()`: Sum of all revenue
   - `revenue_by_region()`: Groupby region
   - `revenue_by_product()`: Groupby product
   - `monthly_revenue()`: Temporal grouping using `.dt.to_period()`
   - `top_n_products_by_revenue()`: Sorting and limiting
   - `average_discount_by_category()`: Mean aggregation by category

4. **print_analysis()** (`sa_001/sales_analysis.py`)
   - Formatted console output of all analyses
   - Clear sections with visual separators
   - Currency and percentage formatting

#### Dataset

**CSV File**: `sa_001/data/sales_sample.csv` (25 rows)

**Columns**:
- `order_id`: Unique order identifier
- `date`: Transaction date (2024-01 to 2024-03)
- `region`: Sales region (North, South, East, West)
- `product`: Product name (11 different products)
- `category`: Product category (Electronics, Furniture, Accessories)
- `quantity`: Units sold
- `unit_price`: Price per unit
- `discount`: Discount rate (0-30%)
- `salesperson`: Sales representative name

**Dataset Choices**:
- 3-month period to demonstrate temporal analysis
- 4 regions for geographic analysis
- 3 categories for classification analysis
- Realistic pricing ($12.99 - $899.99)
- Varying discounts to show promotion impact

### Key Features

- **Functional Programming**: Lambda expressions in `.assign()` and method chaining
- **Stream Operations**: Pandas groupby, map, filter, and aggregate (similar to Java Streams)
- **Data Aggregation**: Multiple aggregation types (sum, mean, count)
- **Immutability**: Functions return new DataFrames without modifying inputs
- **Type Safety**: Full type hints for all functions

### Testing

Comprehensive unit tests with hardcoded sample DataFrame (4 rows):

- ✅ Revenue calculation accuracy
- ✅ Original DataFrame immutability
- ✅ Total revenue calculation
- ✅ Empty DataFrame handling
- ✅ Region-based grouping
- ✅ Product-based grouping
- ✅ Monthly temporal grouping
- ✅ Top N products ordering
- ✅ Average discount by category
- ✅ CSV file loading
- ✅ Date parsing
- ✅ Functional programming patterns (immutability)

**Test Results**: 13 tests passing (1.13s)

Run tests:
```bash
pytest sa_001/test_sales_analysis.py -v
```

### Sample Output

```
============================================================
=== Sales Analysis ===
============================================================

Total Revenue: $15,704.94

------------------------------------------------------------
Revenue by Region:
------------------------------------------------------------
  East            $    4,164.65
  North           $    4,405.39
  South           $    2,849.14
  West            $    4,285.76

------------------------------------------------------------
Revenue by Product:
------------------------------------------------------------
  Desk Lamp                 $      651.84
  HDMI Cable                $      427.79
  Keyboard Mechanical       $      845.91
  Laptop Pro                $    4,823.95
  Monitor 27inch            $    2,610.93
  Mouse Pad                 $      509.66
  Office Chair              $    2,387.40
  Standing Desk             $    1,589.97
  USB Cable                 $      444.26
  Webcam HD                 $    1,015.87
  Wireless Mouse            $      397.37

------------------------------------------------------------
Monthly Revenue:
------------------------------------------------------------
  2024-01         $    4,639.54
  2024-02         $    5,963.43
  2024-03         $    5,101.97

------------------------------------------------------------
Top 5 Products by Revenue:
------------------------------------------------------------
  1. Laptop Pro              $    4,823.95
  2. Monitor 27inch          $    2,610.93
  3. Office Chair            $    2,387.40
  4. Standing Desk           $    1,589.97
  5. Webcam HD               $    1,015.87

------------------------------------------------------------
Average Discount by Category:
------------------------------------------------------------
  Accessories                   5.0%
  Electronics                  10.7%
  Furniture                    12.9%

============================================================
```

### Run the Analysis

```bash
python -m sa_001.sales_analysis
```

---

## Requirements Coverage

### PC-001 Testing Objectives ✅

- ✅ **Thread synchronization**: Condition variables with wait/notify mechanism
- ✅ **Concurrent programming**: Multiple threads running simultaneously
- ✅ **Blocking queues**: Bounded buffer with blocking put/get operations
- ✅ **Wait/Notify mechanism**: Proper use of `condition.wait()` and `notify_all()`

### SA-001 Testing Objectives ✅

- ✅ **Functional programming**: Lambda expressions, immutable operations, method chaining
- ✅ **Stream operations**: Pandas groupby, map, filter, aggregate operations
- ✅ **Data aggregation**: Sum, mean, count, groupby operations
- ✅ **Lambda expressions**: Used extensively in `.assign()` and transformations

---

## License

This project is part of the Intuit Build Challenge.
