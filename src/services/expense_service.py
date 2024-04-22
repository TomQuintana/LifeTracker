from sqlmodel.ext.asyncio.session import AsyncSession

from ..domain.expenses.model import Expense
from ..domain.expenses.requestModel import ExpenseRequest


class ExpenseService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_expense(self, expense_data: ExpenseRequest):
        new_expense = Expense(**expense_data.model_dump())

        self.session.add(new_expense)

        await self.session.commit()

        return new_expense
