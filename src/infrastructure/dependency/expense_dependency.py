from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.db_manager import get_session
from ...infrastructure.repository.SQLModel.sql_model_expenses import SqlModelExpenseRepository
from ..services.expense_service import ExpenseService


def get_repository(session: AsyncSession = Depends(get_session)):
    return SqlModelExpenseRepository(session)


def get_expense_service(repository: SqlModelExpenseRepository = Depends(get_repository)):
    return ExpenseService(repository)
