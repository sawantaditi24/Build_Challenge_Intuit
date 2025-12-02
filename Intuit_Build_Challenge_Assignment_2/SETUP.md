# Setup Instructions for Data Analysis Application

This document provides detailed step-by-step instructions for setting up and running the Data Analysis application using functional programming.

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
cd "/Applications/Intuit_Build _Challenge/Intuit_Build_Challenge_Assignment_2"
```

### Step 2: Verify Project Structure

Ensure the following directory structure exists:

```
Intuit_Build_Challenge_Assignment_2/
├── src/
│   ├── __init__.py
│   ├── csv_reader.py
│   └── data_analyzer.py
├── tests/
│   ├── __init__.py
│   ├── test_csv_reader.py
│   └── test_data_analyzer.py
├── data/
│   └── sales_data.csv
├── main.py
├── README.md
├── SETUP.md
├── DESIGN_DECISION.md
└── requirements.txt
```

### Step 3: Verify Dependencies

This project uses only Python standard library modules. No external dependencies are required.

The following standard library modules are used:
- `csv` - For reading CSV files
- `functools` - For reduce operations (functional programming)
- `collections` - For defaultdict and grouping operations
- `typing` - For type hints
- `unittest` - For unit testing
- `pathlib` - For file path operations
- `datetime` - For date parsing

No installation of external packages is needed.

### Step 4: Verify Python Path

Ensure you can import the project modules:

```bash
python3 -c "import sys; sys.path.insert(0, '.'); from src.csv_reader import CSVReader; print('Import successful')"
```

Expected output:
```
Import successful
```

## Running the Application

### Running the Main Application

Execute the main application to see all data analyses:

```bash
python3 main.py
```

This will:
1. Load sales data from the CSV file
2. Perform 12 different analytical queries
3. Display all results formatted to the console
4. Show summary statistics

### Expected Runtime

The application typically completes in less than 1 second, depending on system performance and data size.

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
# Test CSV reader implementation
python3 -m unittest tests.test_csv_reader -v

# Test data analyzer implementation
python3 -m unittest tests.test_data_analyzer -v
```

### Running Specific Test Cases

To run a specific test method:

```bash
python3 -m unittest tests.test_data_analyzer.TestDataAnalyzer.test_get_total_revenue -v
```

## Verification Steps

### Step 1: Verify Application Runs Successfully

1. Run the main application:
```bash
python3 main.py
```

2. Check that:
   - No errors are displayed
   - All 12 analyses are performed
   - Results are formatted and printed to console
   - Summary statistics are displayed

### Step 2: Verify All Tests Pass

1. Run all tests:
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

2. Check that:
   - All tests pass (no failures)
   - Test coverage includes all major components
   - No warnings or errors are displayed

### Step 3: Verify Functional Programming Features

The application demonstrates functional programming by:
- Using generators for stream-like operations
- Using lambda expressions for transformations
- Using map, filter, and reduce operations
- Performing data aggregation functionally

## Troubleshooting

### Issue: Import Errors

**Problem**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you are in the project root directory and Python can find the modules:
```bash
cd "/Applications/Intuit_Build _Challenge/Intuit_Build_Challenge_Assignment_2"
python3 -c "import sys; print(sys.path)"
```

### Issue: CSV File Not Found

**Problem**: `FileNotFoundError: CSV file not found`

**Solution**: Verify the CSV file exists:
```bash
ls -la data/sales_data.csv
```

If missing, ensure the `data/` directory and `sales_data.csv` file are present.

### Issue: Python Version Too Old

**Problem**: Syntax errors or `ImportError` related to typing module

**Solution**: Upgrade to Python 3.7 or higher:
```bash
python3 --version
```

If version is below 3.7, install a newer version from [python.org](https://www.python.org/downloads/)

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
- CPU: Low usage during execution
- Memory: Less than 50 MB typically
- Disk I/O: Minimal (reads CSV file once)

### Data Size

The implementation handles:
- Current dataset: 90 records
- Can handle larger datasets efficiently using lazy evaluation
- Memory usage scales with analysis operations, not data size

## Additional Resources

- Python CSV Documentation: https://docs.python.org/3/library/csv.html
- Functional Programming in Python: https://docs.python.org/3/howto/functional.html
- Lambda Expressions: Python documentation on anonymous functions

## Support

For issues or questions:
1. Review the README.md for project overview
2. Check DESIGN_DECISION.md for design decisions, thought process, and implementation rationale
3. Review test files for usage examples
4. Examine source code comments for implementation details

