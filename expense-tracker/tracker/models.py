from datetime import datetime
from typing import Optional


class Expense:
    """
    Represents a single expense entry.
    
    Attributes:
        id: Unique identifier in format EXP-YYYYMMDD-NNNN
        date: Date of expense in YYYY-MM-DD format
        category: Category of expense (e.g., food, transport, rent)
        amount: Amount spent (must be positive)
        note: Optional description of the expense
        currency: Currency code (default: BDT)
    """
    
    def __init__(
        self,
        date: str,
        category: str,
        amount: float,
        note: str = "",
        currency: str = "BDT",
        expense_id: Optional[str] = None
    ):
        """
        Initialize an Expense instance.
        
        Args:
            date: Date string in YYYY-MM-DD format
            category: Category name (string)
            amount: Expense amount (positive float)
            note: Optional note/description
            currency: Currency code (default: BDT)
            expense_id: Optional ID (auto-generated if not provided)
        
        Raises:
            ValueError: If validation fails
        """
        self.date = self._validate_date(date)
        self.category = self._validate_category(category)
        self.amount = self._validate_amount(amount)
        self.note = note
        self.currency = currency
        self.id = expense_id if expense_id else self._generate_id()
    
    def _validate_date(self, date: str) -> str:
        """
        Validate date format (YYYY-MM-DD).
        
        Args:
            date: Date string to validate
            
        Returns:
            Validated date string
            
        Raises:
            ValueError: If date format is invalid
        """
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            raise ValueError("date must be YYYY-MM-DD")
    
    def _validate_category(self, category: str) -> str:
        """
        Validate category (must be non-empty string).
        
        Args:
            category: Category string to validate
            
        Returns:
            Validated category string (lowercase)
            
        Raises:
            ValueError: If category is empty
        """
        if not category or not category.strip():
            raise ValueError("category cannot be empty")
        return category.strip().lower()
    
    def _validate_amount(self, amount: float) -> float:
        """
        Validate amount (must be positive).
        
        Args:
            amount: Amount to validate
            
        Returns:
            Validated amount
            
        Raises:
            ValueError: If amount is not positive
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
    
    def _generate_id(self) -> str:
        """
        Generate a unique ID in format EXP-YYYYMMDD-NNNN.
        
        Returns:
            Generated ID string
        """
        # Extract date part without hyphens
        date_part = self.date.replace("-", "")
        # Generate a timestamp-based sequence number
        timestamp = datetime.now().strftime("%H%M%S%f")[:6]
        return f"EXP-{date_part}-{timestamp}"
    
    def to_dict(self) -> dict:
        """
        Convert expense to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the expense
        """
        return {
            "id": self.id,
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "note": self.note,
            "currency": self.currency
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Expense':
        """
        Create an Expense instance from a dictionary.
        
        Args:
            data: Dictionary containing expense data
            
        Returns:
            Expense instance
        """
        return cls(
            date=data["date"],
            category=data["category"],
            amount=data["amount"],
            note=data.get("note", ""),
            currency=data.get("currency", "BDT"),
            expense_id=data.get("id")
        )
    
    def __str__(self) -> str:
        """String representation for display."""
        return f"{self.id} | {self.date} | {self.category} | {self.amount:.2f} {self.currency} | {self.note}"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Expense(id={self.id}, date={self.date}, category={self.category}, amount={self.amount})"