from typing import List, Dict, Optional
from datetime import datetime
from tracker.models import Expense
from tracker.storage import ExpenseStorage
from tracker.logger import (
    log_expense_added,
    log_expense_deleted,
    log_expense_updated,
    log_info,
    log_error
)


class ExpenseService:
    
    def __init__(self, storage: ExpenseStorage = None):
        self.storage = storage if storage else ExpenseStorage()
    
    def add_expense(self, expense: Expense) -> Expense:
 
        try:
            self.storage.save_expense(expense)
            log_expense_added(expense.id, expense.category, expense.amount)
            return expense
        except Exception as e:
            log_error("AddExpenseError", str(e))
            raise
    
    def list_expenses(
        self,
        month: str = None,
        category: str = None,
        min_amount: float = None,
        max_amount: float = None,
        sort_by: str = None,
        descending: bool = False,
        limit: int = None
    ) -> List[Expense]:

        try:
            expenses = self.storage.load_expenses()
            
            # Apply filters
            expenses = self._apply_filters(
                expenses,
                month=month,
                category=category,
                min_amount=min_amount,
                max_amount=max_amount
            )
            
            # Apply sorting
            if sort_by:
                expenses = self._sort_expenses(expenses, sort_by, descending)
            
            # Apply limit
            if limit:
                expenses = expenses[:limit]
            
            log_info(f"Listed {len(expenses)} expense(s)")
            return expenses
            
        except Exception as e:
            log_error("ListExpensesError", str(e))
            raise
    
    def summary(
        self,
        month: str = None,
        from_date: str = None,
        to_date: str = None,
        category: str = None
    ) -> Dict:

        try:
            expenses = self.storage.load_expenses()
            
            # Apply filters
            expenses = self._apply_filters(
                expenses,
                month=month,
                from_date=from_date,
                to_date=to_date,
                category=category
            )
            
            # Calculate summary
            summary = self._calculate_summary(expenses)
            
            log_info(f"Generated summary: {summary['count']} expenses, total {summary['grand_total']}")
            return summary
            
        except Exception as e:
            log_error("SummaryError", str(e))
            raise
    
    def delete_expense(self, expense_id: str) -> bool:
        try:
            success = self.storage.delete_expense(expense_id)
            log_expense_deleted(expense_id, success)
            return success
        except Exception as e:
            log_error("DeleteExpenseError", str(e))
            raise
    
    def update_expense(
        self,
        expense_id: str,
        amount: float = None,
        note: str = None,
        category: str = None,
        date: str = None
    ) -> bool:
        
        try:
            # Get existing expense
            existing = self.storage.get_expense_by_id(expense_id)
            if not existing:
                log_expense_updated(expense_id, success=False)
                return False
            
            # Create updated expense with new values
            updated_expense = Expense(
                date=date if date else existing.date,
                category=category if category else existing.category,
                amount=amount if amount else existing.amount,
                note=note if note is not None else existing.note,
                currency=existing.currency,
                expense_id=existing.id
            )
            
            success = self.storage.update_expense(expense_id, updated_expense)
            log_expense_updated(expense_id, success)
            return success
            
        except Exception as e:
            log_error("UpdateExpenseError", str(e))
            raise
    
    def _apply_filters(
        self,
        expenses: List[Expense],
        month: str = None,
        from_date: str = None,
        to_date: str = None,
        category: str = None,
        min_amount: float = None,
        max_amount: float = None
    ) -> List[Expense]:

        filtered = expenses
        
        # Filter by month
        if month:
            filtered = [e for e in filtered if e.date.startswith(month)]
        
        # Filter by date range
        if from_date:
            filtered = [e for e in filtered if e.date >= from_date]
        if to_date:
            filtered = [e for e in filtered if e.date <= to_date]
        
        # Filter by category
        if category:
            filtered = [e for e in filtered if e.category.lower() == category.lower()]
        
        # Filter by amount range
        if min_amount is not None:
            filtered = [e for e in filtered if e.amount >= min_amount]
        if max_amount is not None:
            filtered = [e for e in filtered if e.amount <= max_amount]
        
        return filtered
    
    def _sort_expenses(
        self,
        expenses: List[Expense],
        sort_by: str,
        descending: bool = False
    ) -> List[Expense]:

        # Map sort field to expense attribute
        sort_keys = {
            'date': lambda e: e.date,
            'amount': lambda e: e.amount,
            'category': lambda e: e.category
        }
        
        if sort_by not in sort_keys:
            return expenses
        
        return sorted(expenses, key=sort_keys[sort_by], reverse=descending)
    
    def _calculate_summary(self, expenses: List[Expense]) -> Dict:
        count = len(expenses)
        grand_total = sum(e.amount for e in expenses)
        
        # Calculate totals by category
        totals_by_category = {}
        for expense in expenses:
            cat = expense.category
            if cat not in totals_by_category:
                totals_by_category[cat] = 0
            totals_by_category[cat] += expense.amount
        
        return {
            'count': count,
            'grand_total': grand_total,
            'totals_by_category': totals_by_category
        }