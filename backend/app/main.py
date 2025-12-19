from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from . import crud, models, ocr
from .database import engine, Base, get_db


app = FastAPI(
    title="Expense Tracker API",
    description="API for tracking expenses, processing receipts, and providing analytics.",
    version="0.1.0"
)

#startup event to connect to the db
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
