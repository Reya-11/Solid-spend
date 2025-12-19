from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from . import schemas
import asyncio

async def get_spending_by_category(db: AsyncSession):
    """Calculates total spending for each category."""
    query = (
        select(
            schemas.Expense.category.label("name"),
            func.sum(schemas.Expense.normalized_amount).label("total")
        )
        .group_by(schemas.Expense.category)
        .order_by(func.sum(schemas.Expense.normalized_amount).desc())
    )
    result = await db.execute(query)
    return result.all()

async def get_spending_by_merchant(db: AsyncSession):
    """Calculates total spending for each merchant."""
    query = (
        select(
            schemas.Expense.merchant.label("name"),
            func.sum(schemas.Expense.normalized_amount).label("total")
        )
        .group_by(schemas.Expense.merchant)
        .order_by(func.sum(schemas.Expense.normalized_amount).desc())
        .limit(20) # Limit to top 20 merchants for clarity
    )
    result = await db.execute(query)
    return result.all()

async def get_spending_over_time(db: AsyncSession):
    """Calculates total spending per month."""
    query = (
        select(
            func.date_trunc('month', schemas.Expense.date).label("date"),
            func.sum(schemas.Expense.normalized_amount).label("total")
        )
        .group_by(func.date_trunc('month', schemas.Expense.date))
        .order_by(func.date_trunc('month', schemas.Expense.date))
    )
    result = await db.execute(query)
    return result.all()

async def get_full_analytics(db: AsyncSession):
    """Runs all analytics queries concurrently and combines the results."""
    # Use asyncio.gather to run queries in parallel
    results = await asyncio.gather(
        get_spending_by_category(db),
        get_spending_by_merchant(db),
        get_spending_over_time(db)
    )
    return {
        "by_category": results[0],
        "by_merchant": results[1],
        "over_time": results[2],
    }