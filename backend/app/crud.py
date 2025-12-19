from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from uuid import UUID
from . import models, schemas, currency

async def get_user_preferences(db: AsyncSession) -> schemas.UserPreferences:
    """
    Retrieves the user preferences. For this single-user app, it fetches the row with id=1.
    If it doesn't exist, it creates a default one.
    """
    prefs = await db.get(schemas.UserPreferences, 1)
    if not prefs:
        print("No preferences found, creating default entry.")
        prefs = schemas.UserPreferences(id=1, base_currency="USD", theme="light")
        db.add(prefs)
        await db.commit()
        await db.refresh(prefs)
    return prefs

async def update_user_preferences(db: AsyncSession, prefs_data: models.UserPreferences) -> schemas.UserPreferences:
    """
    Updates the user preferences.
    """
    prefs = await get_user_preferences(db) # Use our get function to ensure it exists
    
    # Update fields from the request data
    prefs_update_data = prefs_data.model_dump(exclude_unset=True)
    for key, value in prefs_update_data.items():
        setattr(prefs, key, value)
        
    db.add(prefs)
    await db.commit()
    await db.refresh(prefs)
    return prefs

async def create_expense(db: AsyncSession, expense: models.ExpenseCreate) -> schemas.Expense:
    """
    Creates a new expense in the database, including currency conversion.
    """
    # Fetch user preferences to get the base currency
    user_prefs = await get_user_preferences(db)
    user_base_currency = user_prefs.base_currency

    # Get the exchange rate
    exchange_rate = await currency.get_exchange_rate(
        base_currency=expense.currency,
        target_currency=user_base_currency
    )

    if exchange_rate is None:
        # If we can't get a rate, we can't create the expense correctly.
        raise HTTPException(
            status_code=400, 
            detail=f"Could not retrieve exchange rate for currency '{expense.currency}'. Please try again."
        )

    # Calculate the normalized amount
    normalized_amount = expense.amount * exchange_rate

    db_expense = schemas.Expense(
        **expense.model_dump(),
        normalized_amount=normalized_amount
    )
    
    db.add(db_expense)
    await db.commit()
    await db.refresh(db_expense)
    return db_expense

async def get_expense(db: AsyncSession, expense_id: UUID) -> schemas.Expense | None:
    """Retrieves a single expense by its ID."""
    return await db.get(schemas.Expense, expense_id)

async def get_expenses(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[schemas.Expense]:
    """Retrieves a list of expenses with pagination."""
    query = select(schemas.Expense).order_by(schemas.Expense.date.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def update_expense(db: AsyncSession, expense_id: UUID, expense_data: models.ExpenseUpdate) -> schemas.Expense | None:
    """Updates an existing expense."""
    db_expense = await get_expense(db, expense_id)
    if not db_expense:
        return None

    update_data = expense_data.model_dump(exclude_unset=True)
    
    recalculate_normalized = False
    for key, value in update_data.items():
        setattr(db_expense, key, value)
        if key in ["amount", "currency"]:
            recalculate_normalized = True

    if recalculate_normalized:
        user_prefs = await get_user_preferences(db)
        exchange_rate = await currency.get_exchange_rate(db_expense.currency, user_prefs.base_currency)
        if exchange_rate is None:
            # Or handle this error more gracefully
            raise HTTPException(status_code=400, detail="Could not retrieve exchange rate for update.")
        db_expense.normalized_amount = db_expense.amount * exchange_rate

    await db.commit()
    await db.refresh(db_expense)
    return db_expense

async def delete_expense(db: AsyncSession, expense_id: UUID) -> schemas.Expense | None:
    """Deletes an expense."""
    db_expense = await get_expense(db, expense_id)
    if not db_expense:
        return None
    
    await db.delete(db_expense)
    await db.commit()
    return db_expense