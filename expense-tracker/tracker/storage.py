"""
Storage layer for expense tracker application.
Handles reading/writing expenses to JSON file with version control.
"""

import json
import os
from typing import List
from tracker.models import Expense


class ExpenseStorage:
    """
    Handles persistent storage of expenses in JSON format.
    """
    
    VERSION = 1  # JSON schema version
    
    def __init__(self, data_dir: str = "data", filename: str = "expenses.json"):
        """
        Initialize storage with data directory and filename.
        
        Args:
            data_dir: Directory to store data files
            filename: Name of the JSON file
        """
        self.data_dir = data_dir
        self.filename = filename
        self.filepath = os.path.join(data_dir, filename)
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _ensure_file_exists(self):
        """Create empty expenses file if it doesn't exist."""
        self._ensure_data_dir()
        if not os.path.exists(self.filepath):
            self._write_data({"version": self.VERSION, "expenses": []})
    
    def load_expenses(self) -> List[Expense]:
        """
        Load all expenses from JSON file.
        
        Returns:
            List of Expense objects
            
        Raises:
            Exception: If file is corrupted or cannot be read
        """
        self._ensure_file_exists()
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both old format (list) and new format (dict with version)
            if isinstance(data, list):
                # Old format: convert to new format
                expense_list = data
            else:
                # New format: extract expenses list
                expense_list = data.get("expenses", [])
            
            # Convert dictionaries to Expense objects
            expenses = [Expense.from_dict(item) for item in expense_list]
            return expenses
            
        except json.JSONDecodeError as e:
            raise Exception(f"Corrupted data file: {e}")
        except Exception as e:
            raise Exception(f"Error reading expenses: {e}")
    
    def save_expense(self, expense: Expense):
        """
        Add a new expense to the storage.
        
        Args:
            expense: Expense object to save
            
        Raises:
            Exception: If file cannot be written
        """
        # Load existing expenses
        expenses = self.load_expenses()
        
        # Add new expense
        expenses.append(expense)
        
        # Write back to file
        self._write_expenses(expenses)
    
    def save_all_expenses(self, expenses: List[Expense]):
        """
        Replace all expenses with the provided list.
        
        Args:
            expenses: List of Expense objects to save
            
        Raises:
            Exception: If file cannot be written
        """
        self._write_expenses(expenses)
    
    def _write_expenses(self, expenses: List[Expense]):
        """
        Write expenses to JSON file with version.
        
        Args:
            expenses: List of Expense objects to write
            
        Raises:
            Exception: If file cannot be written
        """
        try:
            # Convert Expense objects to dictionaries
            expense_list = [expense.to_dict() for expense in expenses]
            
            # Create data structure with version
            data = {
                "version": self.VERSION,
                "expenses": expense_list
            }
            
            # Write to file
            self._write_data(data)
                
        except Exception as e:
            raise Exception(f"Error writing expenses: {e}")
    
    def _write_data(self, data: dict):
        """
        Write data to JSON file.
        
        Args:
            data: Dictionary to write
            
        Raises:
            Exception: If file cannot be written
        """
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Error writing to file: {e}")
    
    def delete_expense(self, expense_id: str) -> bool:
        """
        Delete an expense by ID.
        
        Args:
            expense_id: ID of the expense to delete
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            Exception: If file cannot be written
        """
        expenses = self.load_expenses()
        
        # Filter out the expense with matching ID
        initial_count = len(expenses)
        expenses = [exp for exp in expenses if exp.id != expense_id]
        
        # Check if anything was deleted
        if len(expenses) == initial_count:
            return False
        
        # Save updated list
        self._write_expenses(expenses)
        return True
    
    def update_expense(self, expense_id: str, updated_expense: Expense) -> bool:
        """
        Update an existing expense.
        
        Args:
            expense_id: ID of the expense to update
            updated_expense: New expense data
            
        Returns:
            True if updated, False if not found
            
        Raises:
            Exception: If file cannot be written
        """
        expenses = self.load_expenses()
        
        # Find and update the expense
        found = False
        for i, exp in enumerate(expenses):
            if exp.id == expense_id:
                expenses[i] = updated_expense
                found = True
                break
        
        if not found:
            return False
        
        # Save updated list
        self._write_expenses(expenses)
        return True
    
    def get_expense_by_id(self, expense_id: str) -> Expense:
        """
        Get a single expense by ID.
        
        Args:
            expense_id: ID of the expense to retrieve
            
        Returns:
            Expense object if found, None otherwise
        """
        expenses = self.load_expenses()
        
        for exp in expenses:
            if exp.id == expense_id:
                return exp
        
        return None