
import argparse
import sys
from datetime import date
from tracker.models import Expense
from tracker.service import ExpenseService
from tracker.logger import log_command, log_validation_error, log_error


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        prog='tracker',
        description='Expense Tracker - Track your expenses from the command line'
    )


     # Create subparsers
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # hello command 
    hello_parser = subparsers.add_parser("hello", help="Print Hello World")
    hello_parser.add_argument("--name", default="World", help="Name to greet")

    args = parser.parse_args()
    print(f"args ---> {args}")
    


if __name__ == '__main__':
    main()