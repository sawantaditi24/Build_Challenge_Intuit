# Data Analysis with Functional Programming

## Overview

This project implements a comprehensive data analysis application using functional programming paradigms. The application delivers to expectations of provisioning Stream operations, data aggregation, and lambda expressions by performing various analytical queries on sales data provided in CSV format.

The program reads data from a CSV file containing Intuit business sales data and executes multiple analytical queries using functional programming patterns including map, filter, reduce operations, and lambda expressions.

## Features

- Functional programming implementation using Python generators (Stream-like operations)
- Comprehensive data aggregation operations
- Lambda expressions for data transformation and filtering
- Multiple analytical queries on sales data
- CSV data processing with lazy evaluation
- Comprehensive unit tests covering all analysis methods
- Production-ready code with proper error handling
- Complete documentation and setup instructions

## Project Structure

```
Intuit_Build_Challenge_Assignment_2/
├── src/
│   ├── __init__.py
│   ├── csv_reader.py          # CSV reading with stream-like operations
│   └── data_analyzer.py       # Data analysis using functional programming
├── tests/
│   ├── __init__.py
│   ├── test_csv_reader.py     # Unit tests for CSV reader
│   └── test_data_analyzer.py  # Unit tests for data analyzer
├── data/
│   └── sales_data.csv          # Sales data CSV file
├── main.py                     # Main application entry point
├── README.md                   # This file
├── SETUP.md                    # Detailed setup instructions
├── DESIGN_DECISION.md          # Design decisions and thought process
└── requirements.txt            # Python dependencies
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

### 2. Navigate to Project Directory

```bash
cd Intuit_Build_Challenge_Assignment_2
```

### 3. Verify Project Structure

Ensure all files are present in the project directory as shown in the Project Structure section above.

### 4. Run the Application

```bash
python3 main.py
```

This will perform all data analyses and print results to the console.

### 5. Run Unit Tests

To run all unit tests:

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

To run a specific test file:

```bash
python3 -m unittest tests.test_csv_reader -v
python3 -m unittest tests.test_data_analyzer -v
```

## Sample Output

When running `main.py`, you should see output similar to:

```
================================================================================
Intuit Sales Data Analysis
================================================================================

Analyzing data from: data/sales_data.csv
Using functional programming: Streams, Lambdas, and Aggregations

================================================================================
Analysis 1: Total Revenue
================================================================================

Total Revenue: $7,316,831.70

================================================================================
Analysis 2: Revenue by Product Category
================================================================================

Revenue by Category:
--------------------------------------------------------------------------------
  Accounting Software           :   $2,891,422.70
  Payment Services              :      $13,717.00
  Payroll Services              :     $525,150.00
  Tax Software                  :   $3,886,542.00

================================================================================
Analysis 3: Revenue by Region
================================================================================

Revenue by Region:
--------------------------------------------------------------------------------
  East                          :   $1,991,469.00
  Midwest                       :   $1,676,334.30
  South                         :   $1,632,679.00
  West                          :   $2,016,349.40

... (additional analyses)
```

## Console Output

<img width="1707" height="856" alt="Console output 1" src="https://github.com/user-attachments/assets/5ccb3127-777b-4b85-9ff4-48e397d9b74b" />

<img width="1691" height="680" alt="Console Output 2" src="https://github.com/user-attachments/assets/b55b1d1a-b7f4-4e87-b757-7cd93e29b27c" />

<img width="1710" height="762" alt="Console Output 3" src="https://github.com/user-attachments/assets/8bab5194-713e-416e-87df-bed39549eca5" />

<img width="1710" height="850" alt="Console Output 4" src="https://github.com/user-attachments/assets/345b246e-f406-4a17-b110-b2becda22b0c" />

<img width="1710" height="548" alt="Console Output 5" src="https://github.com/user-attachments/assets/578d6112-1a90-4e70-a868-d1b49b8c1d60" />

## Key Components

### CSVReader

Stream-like CSV reader that provides functional programming operations:
- `read_records()`: Generator that yields records (lazy evaluation)
- `filter_records(predicate)`: Filter records using predicate function
- `map_records(transform)`: Transform records using mapping function

### DataAnalyzer

Data analyzer using functional programming patterns:
- `get_total_revenue()`: Calculate total revenue using reduce operation
- `get_revenue_by_category()`: Group revenue by category using aggregation
- `get_revenue_by_region()`: Group revenue by region
- `get_revenue_by_customer_type()`: Group revenue by customer type
- `get_top_products_by_revenue(n)`: Get top products using sorting with lambda
- `get_average_revenue_per_transaction()`: Calculate average using map and reduce
- `get_sales_by_month()`: Group sales by month
- `get_products_by_category()`: Group products by category
- `get_high_value_transactions(threshold)`: Filter high-value transactions using lambda
- `get_revenue_by_product_and_region()`: Nested grouping operations
- `get_total_quantity_sold()`: Calculate total quantity using reduce
- `get_average_quantity_per_transaction()`: Calculate average quantity

## Functional Programming Features

This implementation demonstrates:

1. **Stream Operations**: Using Python generators for lazy evaluation
2. **Lambda Expressions**: Used throughout for data transformation and filtering
3. **Map Operations**: Transforming data using map functions
4. **Filter Operations**: Filtering data using predicate functions
5. **Reduce Operations**: Aggregating data using reduce operations
6. **Data Aggregation**: Grouping and summarizing data functionally

## Testing

The project includes comprehensive unit tests covering:

- CSV reading functionality and stream-like operations
- All data analysis methods
- Functional programming patterns (map, filter, reduce)
- Lambda expression usage
- Edge cases (empty data, invalid values)
- Error handling

All tests can be run using Python's unittest framework.

## CSV Dataset

The included CSV file (`data/sales_data.csv`) contains sales data reflecting Intuit's business:
- **Products**: TurboTax (various versions), QuickBooks (Online/Desktop), Intuit Payroll, Payment Processing
- **Categories**: Tax Software, Accounting Software, Payroll Services, Payment Services
- **Regions**: West, East, South, Midwest
- **Customer Types**: Individual, Small Business, Enterprise
- **Time Period**: January through December 2024

This dataset demonstrates awareness of Intuit's core business areas and provides realistic data for analysis.

## Design Decisions

For detailed information about design decisions, assumptions, and thought process, please refer to **[DESIGN_DECISION.md](DESIGN_DECISION.md)**.

This document is crucial for understanding the implementation approach, as it explains:
- **Functional programming approach**: How Stream-like operations are implemented in Python
- **Data structure choices**: Why specific data structures were chosen
- **Lambda expression usage**: Where and why lambdas are used
- **Aggregation strategies**: How data aggregation is performed functionally
- **CSV dataset design**: Rationale behind the Intuit business data structure
- **Testing approach**: Comprehensive test coverage strategy
- **Assumptions and constraints**: Key considerations during development

## Best Practices

- All operations use functional programming patterns
- Proper error handling and validation
- Comprehensive unit tests
- Clear code documentation
- Modular and extensible design
- Production-ready code quality
- Lazy evaluation for memory efficiency

## License

This project is part of the Intuit Build Challenge assignment.

