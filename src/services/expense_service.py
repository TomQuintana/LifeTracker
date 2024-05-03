from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..domain.expenses.model import Expense
from ..domain.expenses.requestModel import ExpenseRequest
from .cotization import Cotization


class ExpenseService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # NOTE: define a return type for principal methods
    async def _create_expense_db(self, expense_data):
        self.session.add(expense_data)
        await self.session.commit()

    async def create_expense(self, expense_data: ExpenseRequest):
        crypto_currency = "USDT"
        cotization_service = Cotization(crypto_currency)
        cotization = await cotization_service.calculate_cotization(expense_data.price_ARS)

        expense = Expense(**expense_data.model_dump())
        expense.price_USDT = cotization

        return await self._create_expense_db(expense)

    async def _obtatin_total(self, data) -> dict[str, float]:
        total_spend_ars = 0
        total_spend_usdt = 0

        for spend_data in data:
            total_spend_ars += spend_data.price_ARS
            # total_spend_usdt += spend_data.price_USDT

        data_reponse = {
            "Total Spend in ARS": total_spend_ars,
            "Total Spend in USDT": total_spend_usdt,
        }

        return data_reponse

    async def calculate_total(self, month: int):
        month_expense = int(month)  # REF: pass a query separeted method
        query = select(Expense).where(Expense.month == month_expense)
        data = await self.session.exec(query)
        return await self._obtatin_total(data)

    def process_data(self, data):
        data_reponse = []
        for formatted_data in data:
            data_list = {
                "name": formatted_data.name,
                "price_ARS": formatted_data.price_ARS,
                "price_USDT": formatted_data.price_USDT,
                "type": formatted_data.type,
                "date": formatted_data.date,
            }

            data_reponse.append(data_list)
        return data_reponse

    async def obtain_data(self, month: int):
        month_expense = int(month)  # REF: pass a separeted method
        query = select(Expense).where(Expense.month == month_expense)
        data = await self.session.exec(query)
        return self.process_data(data)
