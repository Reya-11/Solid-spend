from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
import io
import csv

from . import crud, models, ocr, analytics  # Added analytics import
from .database import engine, Base, get_db


app = FastAPI(
    title="Expense Tracker API",
    description="API for tracking expenses, processing receipts, and providing analytics.",
    version="0.1.0"
)

# startup event to connect to the db
@app.on_event("startup")
async def on_startup():
    """
    Create database tables on startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  
        # For production, you would use a migration tool like Alembic
        await conn.run_sync(Base.metadata.create_all)


@app.post("/ocr/receipt")
async def ocr_receipt(file: UploadFile = File(...)):
    """
    Accepts a receipt image, performs OCR, and returns the extracted text.
    """
    image_data = await file.read()
    extracted_text = await ocr.extract_text_from_image(image_data)
    return {"text": extracted_text}


@app.get("/")
def read_root():
    """
    Root endpoint for health check.
    """
    return {"status": "ok", "message": "Welcome to the Expense Tracker API!"}


@app.get("/expenses/", response_model=List[models.Expense])
async def read_expenses(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of all expenses.
    """
    expenses = await crud.get_expenses(db, skip=skip, limit=limit)
    return expenses


@app.get("/expenses/{expense_id}", response_model=models.Expense)
async def read_expense(expense_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a single expense by its ID.
    """
    db_expense = await crud.get_expense(db, expense_id=expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense


@app.put("/expenses/{expense_id}", response_model=models.Expense)
async def update_expense_endpoint(
    expense_id: UUID, 
    expense_data: models.ExpenseUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing expense.
    """
    updated_expense = await crud.update_expense(db, expense_id=expense_id, expense_data=expense_data)
    if updated_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return updated_expense


@app.delete("/expenses/{expense_id}", response_model=models.Expense)
async def delete_expense_endpoint(expense_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Delete an expense.
    """
    deleted_expense = await crud.delete_expense(db, expense_id=expense_id)
    if deleted_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return deleted_expense


@app.post("/expenses/", response_model=models.Expense)
async def create_expense_endpoint(
    expense: models.ExpenseCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new expense.
    """
    return await crud.create_expense(db=db, expense=expense)


@app.get("/preferences/", response_model=models.UserPreferences)
async def read_user_preferences(db: AsyncSession = Depends(get_db)):
    """
    Retrieve the current user preferences.
    """
    return await crud.get_user_preferences(db)


@app.put("/preferences/", response_model=models.UserPreferences)
async def update_user_preferences(
    prefs_data: models.UserPreferences, 
    db: AsyncSession = Depends(get_db)
):
    """
    Update user preferences.
    """
    return await crud.update_user_preferences(db=db, prefs_data=prefs_data)


@app.get("/analytics/", response_model=models.AnalyticsResponse)
async def read_analytics(db: AsyncSession = Depends(get_db)):
    """
    Retrieve aggregated analytics data for all expenses.
    """
    # Get the analytics data
    analytics_data = await analytics.get_full_analytics(db)
    
    # Get the user's base currency to include in the response
    user_prefs = await crud.get_user_preferences(db)
    
    return {
        "by_category": analytics_data["by_category"],
        "by_merchant": analytics_data["by_merchant"],
        "over_time": analytics_data["over_time"],
        "base_currency": user_prefs.base_currency,
    }


@app.get("/export/csv")
async def export_expenses_to_csv(db: AsyncSession = Depends(get_db)):
    """
    Exports all expenses to a CSV file.
    """
    # Use io.StringIO to create an in-memory text file
    string_io = io.StringIO()
    writer = csv.writer(string_io)

    # Write the header row
    writer.writerow([
        "ID", "Date", "Merchant", "Category", "Amount", 
        "Currency", "Normalized Amount", "Base Currency", "Notes"
    ])

    # Fetch all expenses (adjust limit as needed for very large datasets)
    expenses = await crud.get_expenses(db, limit=10000) 
    user_prefs = await crud.get_user_preferences(db)
    base_currency = user_prefs.base_currency

    # Write data rows
    for expense in expenses:
        writer.writerow([
            expense.id,
            expense.date,
            expense.merchant,
            expense.category,
            expense.amount,
            expense.currency,
            expense.normalized_amount,
            base_currency,
            expense.notes
        ])

    # Seek to the beginning of the stream
    string_io.seek(0)
    
    # Return the CSV file as a streaming response
    return StreamingResponse(
        iter([string_io.read()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=expenses.csv"}
    )
