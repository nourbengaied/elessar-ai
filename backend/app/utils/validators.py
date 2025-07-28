import re
from typing import Dict, Any, List
from datetime import datetime
from fastapi import HTTPException

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> bool:
    """Validate password strength"""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True

def validate_csv_data(data: List[Dict[str, Any]]) -> List[str]:
    """Validate CSV transaction data"""
    errors = []
    
    for i, row in enumerate(data, 1):
        # Check required fields
        if 'date' not in row or not row['date']:
            errors.append(f"Row {i}: Missing date")
            continue
        
        if 'description' not in row or not row['description']:
            errors.append(f"Row {i}: Missing description")
            continue
        
        if 'amount' not in row:
            errors.append(f"Row {i}: Missing amount")
            continue
        
        # Validate date format
        try:
            datetime.strptime(str(row['date']), '%Y-%m-%d')
        except ValueError:
            errors.append(f"Row {i}: Invalid date format (use YYYY-MM-DD)")
        
        # Validate amount
        try:
            amount = float(row['amount'])
            if amount <= 0:
                errors.append(f"Row {i}: Amount must be positive")
        except (ValueError, TypeError):
            errors.append(f"Row {i}: Invalid amount format")
        
        # Validate currency (if provided)
        if 'currency' in row and row['currency']:
            if len(str(row['currency'])) != 3:
                errors.append(f"Row {i}: Currency must be 3 characters (e.g., USD)")
    
    return errors

def sanitize_string(value: str) -> str:
    """Sanitize string input"""
    if not value:
        return ""
    # Remove potentially dangerous characters
    return re.sub(r'[<>"\']', '', str(value).strip())

def validate_file_size(file_size: int, max_size: int) -> bool:
    """Validate file size"""
    return file_size <= max_size

def validate_file_type(filename: str, allowed_types: List[str]) -> bool:
    """Validate file type"""
    if not filename:
        return False
    file_extension = filename.lower().split('.')[-1]
    return f".{file_extension}" in allowed_types

def validate_transaction_data(transaction: Dict[str, Any]) -> List[str]:
    """Validate individual transaction data"""
    errors = []
    
    # Required fields
    required_fields = ['date', 'description', 'amount']
    for field in required_fields:
        if field not in transaction or not transaction[field]:
            errors.append(f"Missing required field: {field}")
    
    # Validate amount
    if 'amount' in transaction:
        try:
            amount = float(transaction['amount'])
            if amount <= 0:
                errors.append("Amount must be positive")
        except (ValueError, TypeError):
            errors.append("Invalid amount format")
    
    # Validate date
    if 'date' in transaction and transaction['date']:
        try:
            datetime.strptime(str(transaction['date']), '%Y-%m-%d')
        except ValueError:
            errors.append("Invalid date format (use YYYY-MM-DD)")
    
    return errors 