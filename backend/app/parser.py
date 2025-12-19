import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Optional

def parse_amount(text: str) -> Optional[Decimal]:
    """
    Finds the total amount by looking for keywords like 'total' or 'amount'
    and then finding the largest number on that line.
    Falls back to finding the largest number in the text if no keywords are found.
    """
    lines = text.lower().split('\n')
    amount_pattern = r'(\d+\.\d{2})'
    # Keywords to look for
    keyword_pattern = r'total|amount|balance|due'

    potential_amounts = []

    # --- New, Smarter Logic ---
    # First, try to find amounts on lines that contain a keyword
    for line in lines:
        if re.search(keyword_pattern, line):
            matches = re.findall(amount_pattern, line)
            for match in matches:
                try:
                    # Add any numbers found on this line to our list
                    potential_amounts.append(Decimal(match))
                except InvalidOperation:
                    continue
    
    # If we found any amounts on keyword lines, return the largest one.
    if potential_amounts:
        return max(potential_amounts)

    # --- Fallback Logic ---
    # If we didn't find any keywords, revert to the original strategy.
    all_matches = re.findall(r'\b\d+\.\d{2}\b', text)
    if not all_matches:
        return None
    
    fallback_amounts = []
    for match in all_matches:
        try:
            fallback_amounts.append(Decimal(match))
        except InvalidOperation:
            continue
            
    return max(fallback_amounts) if fallback_amounts else None

def parse_date(text: str) -> Optional[datetime.date]:
    """
    Finds a date in various common formats (MM/DD/YY, YYYY-MM-DD, etc.).
    """
    # Regex for formats like 01/25/2023, 25-01-23, etc.
    pattern = r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})'
    match = re.search(pattern, text)
    
    if match:
        try:
            # Use datetime.strptime to parse the found date string
            date_str = "/".join(match.groups())
            # This handles multiple formats, but you might need to make it smarter
            # For now, we assume a common format like MM/DD/YYYY
            dt_object = datetime.strptime(date_str, '%m/%d/%Y')
            return dt_object.date()
        except ValueError:
            # Try another format, e.g., MM/DD/YY
            try:
                dt_object = datetime.strptime(date_str, '%m/%d/%y')
                return dt_object.date()
            except ValueError:
                return None
    return None

def parse_merchant(text: str) -> Optional[str]:
    """
    A simple heuristic to find the merchant: assume it's the first line.
    """
    lines = text.split('\n')
    for line in lines:
        if line.strip():
            # Return the first non-empty line
            return line.strip()
    return None

def parse_receipt(text: str) -> dict:
    """
    Orchestrates the parsing of the entire receipt text.
    """
    return {
        "amount": parse_amount(text),
        "date": parse_date(text),
        "merchant": parse_merchant(text),
    }
