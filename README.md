# Expense Tracker CLI
A professional command-line expense tracking application built with Python. Track your expenses, generate summaries and manage your finances efficiently from the terminal.

## Features
- Add expenses with date, category, amount and notes
- List expenses with powerful filters (month, category, amount range)
- Sort expenses by date, amount or category
- Generate expense summaries with category breakdowns
- Edit and delete existing expenses
- Persistent storage using JSON with versioning
- Comprehensive logging of all operations
- Input validation and error handling
- Auto-generated unique expense IDs
- Timestamps for expense creation tracking


# Project Structure
```
expense-tracker/
            ├── tracker/                # Main package
            │   ├── __init__.py         # Package initializer
            │   ├── __main__.py         # Entry point: python -m tracker
            │   ├── cli.py              # CLI commands with argparse
            │   ├── models.py           # Expense data model with validation
            │   ├── storage.py          # JSON persistence layer
            │   ├── service.py          # Business logic (filtering, sorting, summary)
            │   ├── utils.py            # Parsing and validation helpers
            │   └── logger.py           # Logging configuration
            ├── data/                   # Data storage (auto-created)
            │   └── expenses.json       # Expense data with version control
            ├── logs/                   # Application logs (auto-created)
            │   └── tracker.log         # Operation logs
            ├── .gitignore              # Git ignore rules
            └── README.md               # This file
```


## Installation
### Requirements
- Python 3.8 or higher
- No external dependencies (uses only Python standard library)

### Setup 
1. Clone this project or download the zip file
2. Change the directory
```
cd expense-tracker
```


















