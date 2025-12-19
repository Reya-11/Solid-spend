import uuid
from sqlalchemy import Column, String, DECIMAL, Date, DateTime, Float, Integer, JSON
from sqlalchemy.sql import func
from .database import Base

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = Column(DECIMAL(precision=10, scale=2), nullable=False)
    currency = Column(String(3), nullable=false)
    normalized_amount = Column(DECIMAL(precision=10, scale=2), nullable=False)
    category = Column(String(50), nullable=False)
    merchant = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    notes = Column(String, nullable=True)
    ocr_confidence = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Add this new class for user preferences
class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True) # Simple ID for single-user
    base_currency = Column(String(3), nullable=False, default="USD")
    theme = Column(String, default="light")
    # custom_categories can be stored as JSON
    custom_categories = Column(JSON, nullable=True)
