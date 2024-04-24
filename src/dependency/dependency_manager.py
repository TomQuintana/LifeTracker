from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.services.expense_service import ExpenseService

from ..db.main import get_session


class DependencyManager:
    def __init__(self):
        pass

    async def get_expense_service(self, session: AsyncSession = Depends(get_session)):
        return ExpenseService(session)
