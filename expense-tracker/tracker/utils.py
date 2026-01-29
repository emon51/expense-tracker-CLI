"""
Utility functions for parsing and validation.
"""

from datetime import datetime


def parse_date(date_str: str) -> str:
    """
    Parse and validate date string.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        Validated date string
        
    Raises:
        ValueError: If date format is invalid
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValueError("date must be YYYY-MM-DD")


def parse_amount(amount) -> float:
    """
    Parse and validate amount.
    
    Args:
        amount: Amount to validate
        
    Returns:
        Validated amount as float
        
    Raises:
        ValueError: If amount is invalid or not positive
    """
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("amount must be > 0")
        return amount
    except (TypeError, ValueError) as e:
        if "amount must be > 0" in str(e):
            raise
        raise ValueError("amount must be a valid number")


def parse_category(category: str) -> str:
    """
    Parse and validate category.
    
    Args:
        category: Category string
        
    Returns:
        Validated category (lowercase, stripped)
        
    Raises:
        ValueError: If category is empty
    """
    if not category or not category.strip():
        raise ValueError("category cannot be empty")
    return category.strip().lower()


def format_expense_output(expense) -> str:
    """
    Format expense for display.
    
    Args:
        expense: Expense object
        
    Returns:
        Formatted string
    """
    return f"{expense.id} | {expense.date} | {expense.category} | {expense.amount:.2f} {expense.currency} | {expense.note}"


def format_summary_output(summary: dict) -> str:
    """
    Format summary for display.
    
    Args:
        summary: Summary dictionary with count, grand_total, totals_by_category
        
    Returns:
        Formatted summary string
    """
    output = []
    output.append("=" * 60)
    output.append("EXPENSE SUMMARY")
    output.append("=" * 60)
    output.append(f"Total Expenses: {summary['count']}")
    output.append(f"Grand Total: {summary['grand_total']:.2f} BDT")
    output.append("")
    
    if summary['totals_by_category']:
        output.append("By Category:")
        output.append("-" * 60)
        for category, total in sorted(summary['totals_by_category'].items()):
            output.append(f"  {category.capitalize():20} {total:>10.2f} BDT")
        output.append("=" * 60)
    else:
        output.append("No expenses found")
    
    return "\n".join(output)