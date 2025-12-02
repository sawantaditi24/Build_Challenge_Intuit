# Setup Instructions for Producer-Consumer Pattern Implementation

This document provides detailed step-by-step instructions for setting up and running the Producer-Consumer Pattern implementation.

## Prerequisites

### System Requirements
- Operating System: macOS, Linux, or Windows
- Python Version: Python 3.7 or higher
- Memory: Minimum 512 MB RAM (recommended: 1 GB or more)
- Disk Space: Minimum 10 MB free space

### Python Installation Verification

1. Check if Python is installed:
```bash
python3 --version
```

Expected output should show Python 3.7 or higher:
```
Python 3.9.7
```

2. If Python is not installed, download and install from [python.org](https://www.python.org/downloads/)

3. Verify pip is available (usually comes with Python):
```bash
python3 -m pip --version
```

## Project Setup

### Step 1: Navigate to Project Directory

Open a terminal or command prompt and navigate to the project directory:

```bash
cd "/Intuit_Build _Challenge/Intuit_Build_Challenge_Assignment_1"
```

### Step 2: Verify Project Structure

Ensure the following directory structure exists:

```
Intuit_Build_Challenge_Assignment_1/
├── src/
│   ├── __init__.py
│   ├── blocking_queue.py
│   ├── container.py
│   ├── producer.py
│   └── consumer.py
├── tests/
│   ├── __init__.py
│   ├── test_blocking_queue.py
│   ├── test_container.py
│   ├── test_producer.py
│   ├── test_consumer.py
│   └── test_integration.py
├── main.py
├── README.md
├── SETUP.md
├── DESIGN_DECISION.md
└── requirements.txt
```

### Step 3: Verify Dependencies

This project uses only Python standard library modules. No external dependencies are required.

The following standard library modules are used:
- `threading` - For thread management and synchronization
- `collections.deque` - For efficient queue operations
- `typing` - For type hints
- `unittest` - For unit testing
- `time` - For delays and timing

No installation of external packages is needed.

### Step 4: Verify Python Path

Ensure you can import the project modules:

```bash
python3 -c "import sys; sys.path.insert(0, '.'); from src.blocking_queue import BlockingQueue; print('Import successful')"
```

Expected output:
```
Import successful
```

## Running the Application

### Running the Main Application

Execute the main application to see the producer-consumer pattern in action:

```bash
python3 main.py
```

This will:
1. Create a source container with 20 items
2. Create an empty destination container
3. Create a shared blocking queue with size 5
4. Start a producer thread that reads from source and places items in queue
5. Start a consumer thread that reads from queue and stores items in destination
6. Display detailed output showing the transfer process
7. Verify data integrity at the end

### Expected Runtime

The application typically completes in 2-5 seconds, depending on system performance and the configured delays.

## Running Unit Tests

### Running All Tests

To run all unit tests with verbose output:

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

This will execute all test files and display detailed results.

### Running Individual Test Files

Run specific test suites:

```bash
# Test blocking queue implementation
python3 -m unittest tests.test_blocking_queue -v

# Test container implementation
python3 -m unittest tests.test_container -v

# Test producer implementation
python3 -m unittest tests.test_producer -v

# Test consumer implementation
python3 -m unittest tests.test_consumer -v

# Test integration scenarios
python3 -m unittest tests.test_integration -v
```

### Running Specific Test Cases

To run a specific test method:

```bash
python3 -m unittest tests.test_blocking_queue.TestBlockingQueue.test_put_and_get_single_item -v
```

## Verification Steps

### Step 1: Verify Application Runs Successfully

1. Run the main application:
```bash
python3 main.py
```

2. Check that:
   - No errors are displayed
   - All 20 items are produced
   - All 20 items are consumed
   - Data integrity verification shows "SUCCESS"
   - Final queue is empty

### Step 2: Verify All Tests Pass

1. Run all tests:
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

2. Check that:
   - All tests pass (no failures)
   - Test coverage includes all major components
   - No warnings or errors are displayed

### Step 3: Verify Thread Synchronization

The application demonstrates thread synchronization by:
- Producer blocking when queue is full
- Consumer blocking when queue is empty
- Proper wait/notify mechanism using Condition variables
- No race conditions or data corruption

## Troubleshooting

### Issue: Import Errors

**Problem**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you are in the project root directory and Python can find the modules:
```bash
cd "/Applications/Intuit_Build _Challenge/Intuit_Build_Challenge_Assignment_1"
python3 -c "import sys; print(sys.path)"
```

### Issue: Python Version Too Old

**Problem**: Syntax errors or `ImportError` related to typing module

**Solution**: Upgrade to Python 3.7 or higher:
```bash
python3 --version
```

If version is below 3.7, install a newer version from [python.org](https://www.python.org/downloads/)

### Issue: Tests Hang or Timeout

**Problem**: Tests appear to hang indefinitely

**Solution**: This may indicate a deadlock. Check:
1. Ensure all threads are properly stopped
2. Verify timeout values in tests are reasonable
3. Check system resources (CPU, memory)

### Issue: Permission Denied

**Problem**: `PermissionError` when running scripts

**Solution**: Ensure files have execute permissions:
```bash
chmod +x main.py
```

Or run with explicit Python interpreter:
```bash
python3 main.py
```

## Development Environment Setup (Optional)

### Using Virtual Environment (Recommended for Development)

While not required for this project, using a virtual environment is a best practice:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Verify activation
which python3  # Should point to venv/bin/python3

# Deactivate when done
deactivate
```

### Using IDE

This project can be opened in any Python IDE:
- PyCharm
- VS Code
- Sublime Text
- Vim/Emacs

Ensure the IDE is configured to use Python 3.7+.

## Performance Considerations

### System Load

The application uses minimal system resources:
- CPU: Low to moderate usage during execution
- Memory: Less than 50 MB typically
- Disk I/O: None (all operations in memory)

### Scaling

The implementation supports:
- Multiple producers and consumers
- Configurable queue sizes
- Adjustable production/consumption delays

To test with different configurations, modify parameters in `main.py`:
- `queue_size`: Maximum queue capacity
- `num_items`: Number of items to process
- `production_delay`: Delay between productions
- `consumption_delay`: Delay between consumptions

## Additional Resources

- Python Threading Documentation: https://docs.python.org/3/library/threading.html
- Producer-Consumer Pattern: Standard concurrent programming pattern
- Condition Variables: Used for thread synchronization

## Support

For issues or questions:
1. Review the README.md for project overview
2. Check DESIGN_DECISION.md for design decisions, thought process, and implementation rationale
3. Review test files for usage examples
4. Examine source code comments for implementation details

