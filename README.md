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
    └── (Assignment 2 files will be here)
```

## Assignments Overview

### Assignment 1: Producer-Consumer Pattern with Thread Synchronization

**Status:** ✅ Complete

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

### Assignment 2: [To be completed]

**Status:** 🚧 In Progress

[Assignment 2 description will be added here]

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
   cd Intuit_Build_Challenge_Assignment_1
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
# Assignment 1
cd Intuit_Build_Challenge_Assignment_1
python3 -m unittest discover -s tests -p "test_*.py" -v
```

## Code Quality

- ✅ Production-level code quality
- ✅ Comprehensive unit test coverage
- ✅ Proper error handling and validation
- ✅ Thread-safe operations
- ✅ Modular and extensible design
- ✅ Detailed code documentation
- ✅ Best programming practices followed

## Documentation

Each assignment includes:
- **README.md**: Overview, features, and usage instructions
- **SETUP.md**: Detailed setup and installation instructions
- **DESIGN_DECISION.md**: Comprehensive design decisions, thought process, assumptions, and implementation rationale

> **Note:** The DESIGN_DECISION.md file is particularly important as it demonstrates the engineering thought process, architectural decisions, trade-offs considered, and the depth of analysis applied to the solution. This document helps evaluators understand not just *what* was implemented, but *why* it was implemented that way.

## Deliverables

### Assignment 1 Deliverables:
- ✅ Complete source code
- ✅ Comprehensive unit tests
- ✅ README with setup instructions and sample output
- ✅ Results of all analyses printed to console
- ✅ Design documentation

### Assignment 2 Deliverables:
- [To be completed]

## Author

[Your Name]

## License

This project is part of the Intuit Build Challenge assignment.

