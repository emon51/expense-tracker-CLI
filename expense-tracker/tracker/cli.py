"""
CLI interface with argparse commands.
"""

import argparse
import sys
from datetime import date
from tracker.models import Expense
from tracker.service import ExpenseService
from tracker.logger import log_command, log_validation_error, log_error


def create_parser():
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog='tracker',
        description='Expense Tracker - Track your expenses from the command line'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new expense')
    add_parser.add_argument('--date', type=str, default=None, help='Date (YYYY-MM-DD), default: today')
    add_parser.add_argument('--category', type=str, required=True, help='Category (e.g., food, transport, rent)')
    add_parser.add_argument('--amount', type=float, required=True, help='Amount (must be positive)')
    add_parser.add_argument('--note', type=str, default='', help='Optional note/description')
    add_parser.add_argument('--currency', type=str, default='BDT', help='Currency code (default: BDT)')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List expenses with filters')
    list_parser.add_argument('--month', type=str, help='Filter by month (YYYY-MM)')
    list_parser.add_argument('--category', type=str, help='Filter by category')
    list_parser.add_argument('--min', type=float, dest='min_amount', help='Minimum amount')
    list_parser.add_argument('--max', type=float, dest='max_amount', help='Maximum amount')
    list_parser.add_argument('--sort', type=str, choices=['date', 'amount', 'category'], help='Sort by field')
    list_parser.add_argument('--desc', action='store_true', help='Sort in descending order')
    list_parser.add_argument('--limit', type=int, help='Limit number of results')
    
    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Generate expense summary')
    summary_parser.add_argument('--month', type=str, help='Filter by month (YYYY-MM)')
    summary_parser.add_argument('--from', type=str, dest='from_date', help='Start date (YYYY-MM-DD)')
    summary_parser.add_argument('--to', type=str, dest='to_date', help='End date (YYYY-MM-DD)')
    summary_parser.add_argument('--category', type=str, help='Filter by category')
    
    # Delete command (optional)
    delete_parser = subparsers.add_parser('delete', help='Delete an expense')
    delete_parser.add_argument('--id', type=str, required=True, dest='expense_id', help='Expense ID to delete')
    
    # Edit command (optional)
    edit_parser = subparsers.add_parser('edit', help='Edit an expense')
    edit_parser.add_argument('--id', type=str, required=True, dest='expense_id', help='Expense ID to edit')
    edit_parser.add_argument('--amount', type=float, help='New amount')
    edit_parser.add_argument('--note', type=str, help='New note')
    edit_parser.add_argument('--category', type=str, help='New category')
    edit_parser.add_argument('--date', type=str, help='New date (YYYY-MM-DD)')
    
    return parser


def handle_add(service: ExpenseService, args):
    """Handle add command."""
    log_command('add', vars(args))
    
    # Use today's date if not provided
    expense_date = args.date if args.date else date.today().strftime('%Y-%m-%d')
    
    try:
        # Create expense
        expense = Expense(
            date=expense_date,
            category=args.category,
            amount=args.amount,
            note=args.note,
            currency=args.currency
        )
        
        # Add to storage
        service.add_expense(expense)
        
        # Print confirmation
        print(f"Added: {expense}")
        
    except ValueError as e:
        raise ValueError(str(e))


def handle_list(service: ExpenseService, args):
    """Handle list command."""
    log_command('list', vars(args))
    
    # Get expenses with filters
    expenses = service.list_expenses(
        month=args.month,
        category=args.category,
        min_amount=args.min_amount,
        max_amount=args.max_amount,
        sort_by=args.sort,
        descending=args.desc,
        limit=args.limit
    )
    
    # Display results
    if not expenses:
        print("No expenses found")
    else:
        print(f"Found {len(expenses)} expense(s):")
        print("-" * 80)
        for expense in expenses:
            print(expense)
        print("-" * 80)
        print(f"Total: {sum(e.amount for e in expenses):.2f} BDT")


def handle_summary(service: ExpenseService, args):
    """Handle summary command."""
    log_command('summary', vars(args))
    
    # Generate summary
    summary = service.summary(
        month=args.month,
        from_date=args.from_date,
        to_date=args.to_date,
        category=args.category
    )
    
    # Display summary
    print("=" * 60)
    print("EXPENSE SUMMARY")
    print("=" * 60)
    print(f"Total Expenses: {summary['count']}")
    print(f"Grand Total: {summary['grand_total']:.2f} BDT")
    print()
    
    if summary['totals_by_category']:
        print("By Category:")
        print("-" * 60)
        for category, total in sorted(summary['totals_by_category'].items()):
            print(f"  {category.capitalize():20} {total:>10.2f} BDT")
        print("=" * 60)
    else:
        print("No expenses found")


def handle_delete(service: ExpenseService, args):
    """Handle delete command."""
    log_command('delete', vars(args))
    
    success = service.delete_expense(args.expense_id)
    
    if success:
        print(f"Deleted: {args.expense_id}")
    else:
        print(f"Error: Expense {args.expense_id} not found")
        sys.exit(1)


def handle_edit(service: ExpenseService, args):
    """Handle edit command."""
    log_command('edit', vars(args))
    
    # Check if at least one field is being updated
    if not any([args.amount, args.note is not None, args.category, args.date]):
        print("Error: Please provide at least one field to update (--amount, --note, --category, or --date)")
        sys.exit(1)
    
    success = service.update_expense(
        expense_id=args.expense_id,
        amount=args.amount,
        note=args.note,
        category=args.category,
        date=args.date
    )
    
    if success:
        print(f"Updated: {args.expense_id}")
    else:
        print(f"Error: Expense {args.expense_id} not found")
        sys.exit(1)


def run():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Show help if no command provided
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize service
    service = ExpenseService()
    
    # Execute command
    try:
        if args.command == 'add':
            handle_add(service, args)
        elif args.command == 'list':
            handle_list(service, args)
        elif args.command == 'summary':
            handle_summary(service, args)
        elif args.command == 'delete':
            handle_delete(service, args)
        elif args.command == 'edit':
            handle_edit(service, args)
    except ValueError as e:
        print(f"Error: {e}")
        log_validation_error("command", args.command, str(e))
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        log_error("CommandError", str(e))
        sys.exit(1)