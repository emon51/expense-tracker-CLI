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

## Arguments
- --date (optional): Date in YYYY-MM-DD format (default: today)
- --category (required): Category name (e.g., food, transport, rent)
- --amount (required): Amount (must be positive number)
- --note (optional): Description or note
- --currency (optional): Currency code (default: BDT)

## Usage

### Add Expense
```
   python3 -m tracker add --category food --amount 250.5 --note "Lunch"

   python3 -m tracker add --date 2026-01-26 --category transport --amount 80
```

### List Expenses
```
   python3 -m tracker list

   python3 -m tracker list --month 2026-01 --category food

   python3 -m tracker list --sort amount --desc --limit 10
```

### Summary
```
   python3 -m tracker summary
   python3 -m tracker summary --month 2026-01
   python3 -m tracker summary --from 2026-01-01 --to 2026-01-31
```

###  Edit/Delete
```
   python3 -m tracker edit --id EXP-20260126-0001 --amount 300
   python3 -m tracker delete --id EXP-20260126-0001
```

### Data Format
```
    {
    "version": 1,
    "expenses": [
        {
        "id": "EXP-20260126-102345",
        "date": "2026-01-26",
        "category": "food",
        "amount": 250.5,
        "currency": "BDT",
        "note": "Lunch",
        "created_at": "2026-01-26T10:23:45"
        }
    ]
    }
```

### Validation

- Date: YYYY-MM-DD format
- Amount: Must be > 0
- Category: Required, non-empty string
- ID: Auto-generated (EXP-YYYYMMDD-HHMMSS)

### Examples
```
    # Add expenses
    python3 -m tracker add --date 2026-01-25 --category transport --amount 80 --note "Rickshaw"
    python3 -m tracker add --category food --amount 250.5 --note "Lunch"
    python3 -m tracker add --category rent --amount 400 --note "Room rent"

    # View all
    python3 -m tracker list

    # Monthly summary
    python3 -m tracker summary --month 2026-01
```

### Output
```
    ============================================================
    EXPENSE SUMMARY
    ============================================================
    Total Expenses: 3
    Grand Total: 730.50 BDT

    By Category:
    ------------------------------------------------------------
    Food                     250.50 BDT
    Rent                     400.00 BDT
    Transport                 80.00 BDT
    ============================================================
```

**Need help?** Check the logs at `logs/tracker.log` or run commands with `--help`:
```
python3 -m tracker --help
python3 -m tracker add --help
python3 -m tracker list --help
python3 -m tracker summary --help
```













