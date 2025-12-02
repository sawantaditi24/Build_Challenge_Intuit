# Intuit Build Challenge

This repository contains the complete implementation of the Intuit Build Challenge assignments, demonstrating proficiency in concurrent programming, thread synchronization, and software engineering best practices.

## Repository Structure

```
Intuit_Build _Challenge/
├── Intuit_Build_Challenge_Assignment_1/
│   ├── src/                    # Source code
│   ├── tests/                  # Unit tests
│   ├── main.py                 # Main application entry point
│   ├── README.md               # Assignment 1 detailed documentation
│   ├── SETUP.md                # Setup instructions
│   ├── DESIGN_DECISION.md     # Design decisions, thought process, and assumptions
│   └── requirements.txt        # Python dependencies
│
└── Intuit_Build_Challenge_Assignment_2/
    ├── src/                    # Source code (functional programming)
    ├── tests/                  # Unit tests
    ├── data/                   # CSV dataset (Intuit business data)
    ├── main.py                 # Main application entry point
    ├── README.md               # Assignment 2 detailed documentation
    ├── SETUP.md                # Setup instructions
    ├── DESIGN_DECISION.md     # Design decisions, thought process, and assumptions
    └── requirements.txt        # Python dependencies
```

## Assignments Overview

### Assignment 1: Producer-Consumer Pattern with Thread Synchronization

**Status:** Complete

Implements a classic producer-consumer pattern demonstrating thread synchronization and communication. The program simulates concurrent data transfer between a producer thread that reads from a source container and places items into a shared queue, and a consumer thread that reads from the queue and stores items in a destination container.

**Key Features:**
- Thread-safe blocking queue implementation using Condition variables
- Wait/notify mechanism for thread synchronization
- Comprehensive unit tests (53+ tests)
- Production-ready code with proper error handling
- Complete documentation and setup instructions

**Quick Start:**
```bash
cd Intuit_Build_Challenge_Assignment_1
python3 main.py
```

**For detailed information, see:** [Assignment 1 README](Intuit_Build_Challenge_Assignment_1/README.md)

### Assignment 2: Data Analysis with Functional Programming

**Status:** Complete

Implements a comprehensive data analysis application using functional programming paradigms. The application demonstrates proficiency with Stream operations, data aggregation, and lambda expressions by performing various analytical queries on sales data provided in CSV format.

**Key Features:**
- Functional programming implementation using Python generators (Stream-like operations)
- Comprehensive data aggregation operations (12 analysis methods)
- Lambda expressions used throughout (20+ occurrences)
- CSV data processing with lazy evaluation
- Intuit business sales data dataset (92 records)
- Comprehensive unit tests (21 tests)
- Production-ready code with proper error handling
- Complete documentation and setup instructions

**Quick Start:**
```bash
cd Intuit_Build_Challenge_Assignment_2
python3 main.py
```

**For detailed information, see:** [Assignment 2 README](Intuit_Build_Challenge_Assignment_2/README.md)

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only Python standard library)

## Quick Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd Intuit_Build_Challenge
   ```

2. Navigate to the assignment you want to run:
   ```bash
   # For Assignment 1
   cd Intuit_Build_Challenge_Assignment_1
   
   # For Assignment 2
   cd Intuit_Build_Challenge_Assignment_2
   ```

3. Run the application:
   ```bash
   python3 main.py
   ```

4. Run tests:
   ```bash
   python3 -m unittest discover -s tests -p "test_*.py" -v
   ```

## Testing

Each assignment includes comprehensive unit tests. To run tests for a specific assignment:

```bash
# Assignment 1: Producer-Consumer Pattern
cd Intuit_Build_Challenge_Assignment_1
python3 -m unittest discover -s tests -p "test_*.py" -v

# Assignment 2: Data Analysis with Functional Programming
cd Intuit_Build_Challenge_Assignment_2
python3 -m unittest discover -s tests -p "test_*.py" -v
```

## Code Quality

Both assignments demonstrate:
- Production-level code quality
- Comprehensive unit test coverage (60+ tests total)
- Proper error handling and validation
- Modular and extensible design
- Detailed code documentation
- Best programming practices followed
- Functional programming patterns (Assignment 2)
- Thread synchronization (Assignment 1)

## Documentation

Each assignment includes:
- **README.md**: Overview, features, and usage instructions
- **SETUP.md**: Detailed setup and installation instructions
- **DESIGN_DECISION.md**: Comprehensive design decisions, thought process, assumptions, and implementation rationale

> **Note:** The DESIGN_DECISION.md file is particularly important as it demonstrates the engineering thought process, architectural decisions, trade-offs considered, and the depth of analysis applied to the solution. This document helps evaluators understand not just *what* was implemented, but *why* it was implemented that way.

## Deliverables

### Assignment 1 Deliverables:
- Complete source code
- Comprehensive unit tests
- README with setup instructions and sample output
- Results of all analyses printed to console
- Design documentation

### Assignment 2 Deliverables:
- Complete source code
- Comprehensive unit tests (21 tests)
- README with setup instructions and sample output
- Results of all analyses printed to console
- Design documentation
- CSV dataset reflecting Intuit's business

## Author

[Your Name]

## License

This project is part of the Intuit Build Challenge assignment.

