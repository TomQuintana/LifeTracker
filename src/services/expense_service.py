from sqlmodel.ext.asyncio.session import AsyncSession

from ..domain.expenses.model import Expense
from ..domain.expenses.requestModel import ExpenseRequest
from .cotization import Cotization


class ExpenseService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_expense(self, expense_data: ExpenseRequest):

        crypto_currency = 'USDT'
        cotization_service = Cotization(crypto_currency)
        cotization = await cotization_service.calculate_cotization(expense_data.price_ARS)

        new_expense = Expense(**expense_data.model_dump())
        new_expense.price_USDT = cotization

        self.session.add(new_expense)

        await self.session.commit()

        return new_expense
