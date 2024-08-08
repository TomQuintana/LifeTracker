from datetime import datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.helper.helper import valid_type_input

from ..domain.expenses.model import Expense

# from ..domain.expenses.requestModel import ExpenseRequest
from ..domain.products.model import Products
from .cotization import Cotization
from .email_service import EmailService


class ExpenseService:
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def _save_expense_data(self, expense_data):
        self.session.add(expense_data)
        await self.session.commit()

    async def _save_product_data(self, expense_data):
        self.session.add(expense_data)
        await self.session.commit()

    async def create_expense(self, expense_data):
        print(expense_data.products)
        if not valid_type_input(expense_data.type):
            raise ValueError("Invalid type input")

        if expense_data.date is None:
            expense_data.date = str(datetime.now().date())

        crypto_currency = "USDT"
        cotization_service = Cotization(crypto_currency)
        cotization = await cotization_service.calculate_cotization(expense_data.price_ARS)

        expense = Expense(**expense_data.model_dump())
        expense.price_USDT = cotization
        await self._save_expense_data(expense)

        for product in expense_data.products:
            product_data = Products(**product)
            cotization = await cotization_service.calculate_cotization(product_data.price_ARS)
            product_data.price_USDT = cotization
            product_data.expense_id = expense.uuid
            await self._save_product_data(product_data)

        return expense

    async def _obtatin_total(self, data, budget: float) -> dict[str, float]:
        total_spend_ars = 0
        total_spend_usdt: float = 0

        for spend_data in data:
            total_spend_ars += spend_data.price_ARS
            total_spend_usdt += spend_data.price_USDT

        data_reponse = {
            "Budget": budget,
            "Total Spend in ARS": total_spend_ars,
            "Total Spend in USDT": round(total_spend_usdt, 2),
            "Remaining Budget": round(budget - total_spend_usdt, 2),
        }

        return data_reponse

    async def calculate_total(self, month: int, budget: float):
        month_expense = int(month)  # REF: pass a query separeted method
        query = select(Expense).where(Expense.month == month_expense)
        data = await self.session.exec(query)
        return await self._obtatin_total(data, budget)

    async def get_products_by_expense_uuid(self, expense_uuid: str):
        statement = select(Products).join(Expense).where(Expense.uuid == expense_uuid)
        data_product_to_expense = await self.session.exec(statement)

        data_reponse_products = []

        for formatted_data_products in data_product_to_expense:
            product_list = {
                "name": formatted_data_products.name,
                "price_ARS": formatted_data_products.price_ARS,
                "price_USDT": formatted_data_products.price_USDT,
            }
            data_reponse_products.append(product_list)

        return data_reponse_products

    async def process_data(self, data_expenses):
        data_reponse = []
        for formatted_data in data_expenses:
            products = await self.get_products_by_expense_uuid(formatted_data.uuid)

            data_list = {
                "name": formatted_data.name,
                "price_ARS": formatted_data.price_ARS,
                "price_USDT": formatted_data.price_USDT,
                "type": formatted_data.type,
                "date": formatted_data.date,
                "coutes": formatted_data.coutes,
                "products": products,
            }

            data_reponse.append(data_list)
        return data_reponse

    async def obtain_data(self, month: int):
        month_expense = int(month)
        query_expenses = select(Expense).where(Expense.month == month_expense)

        data_expenses = await self.session.exec(query_expenses)
        return await self.process_data(data_expenses)

    async def send_email(self, user_email, password):
        email_service = EmailService("tomquintana20@gmail.com", password)
        email_service.send(user_email)
        pass
