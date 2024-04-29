from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..domain.expenses.model import Expense
from ..domain.expenses.requestModel import ExpenseRequest
from .cotization import Cotization


class ExpenseService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_expense(self, expense_data: ExpenseRequest):
        crypto_currency = "USDT"
        cotization_service = Cotization(crypto_currency)
        cotization = await cotization_service.calculate_cotization(expense_data.price_ARS)

        new_expense = Expense(**expense_data.model_dump())
        new_expense.price_USDT = cotization

        self.session.add(new_expense)

        await self.session.commit()

        return new_expense

    # TODO: define type of data
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

    async def calculate_total(self):
        statament = select(Expense)
        data = await self.session.exec(statament)
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

    async def obtain_data(self):
        statament = select(Expense)  # NOTE: improve statament for dont get uuid
        data = await self.session.exec(statament)
        return self.process_data(data)
