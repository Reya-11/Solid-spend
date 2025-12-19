from pydantic import BaseModel, Field, Json
from uuid import UUID
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

# For single-user MVP
class UserPreferences(BaseModel):
    base_currency: str = Field(default="USD", max_length=3)
    theme: str = "light"
    custom_categories: Json | None = None

# Pydantic model for creating an expense (input)
class ExpenseCreate(BaseModel):
    amount: Decimal
    currency: str = Field(..., max_length=3)
    category: str
    merchant: str
    date: date
    notes: str | None = None

# Pydantic model for representing an expense in the database (output)
class Expense(BaseModel):
    id: UUID
    amount: Decimal
    currency: str = Field(..., max_length=3)
    normalized_amount: Decimal
    category: str
    merchant: str
    date: date
    notes: str | None = None
    ocr_confidence: float | None = None
    created_at: datetime

    class Config:
        from_attributes = True

class ExpenseUpdate(BaseModel):
    amount: Decimal | None = None
    currency: str | None = None
    category: str | None = None
    merchant: str | None = None
    date: date | None = None
    notes: str | None = None

# --- Add these new models for Analytics ---

class AnalyticsTotal(BaseModel):
    """A generic model for aggregated totals."""
    name: str  # e.g., category name or merchant name
    total: Decimal

class AnalyticsOverTime(BaseModel):
    """Model for time-series data."""
    date: date # The start of the period (e.g., first day of the month)
    total: Decimal

class AnalyticsResponse(BaseModel):
    """The final structure for the analytics endpoint response."""
    by_category: List[AnalyticsTotal]
    by_merchant: List[AnalyticsTotal]
    over_time: List[AnalyticsOverTime]
    base_currency: str