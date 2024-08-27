from datetime import datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


from ..utils.valid_type_input import valid_type_input

from ..domain.expenses.model import Expense
from ..domain.products.model import Products
from .cotization import Cotization
from ..utils.alert import bad_request


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
            product_data = Products(**product.model_dump())
            cotization = await cotization_service.calculate_cotization(product_data.price_ARS)
            product_data.price_USDT = cotization
            product_data.expense_id = expense.uuid
            await self._save_product_data(product_data)

        return expense

    async def _obtatin_total(self, data, budget: float) -> dict[str, float]:
        total_spend_ars = 0
        total_spend_usdt: float = 0

        for spend_data in data:
            print(spend_data)
            total_spend_ars += spend_data.price_ARS
            total_spend_usdt += spend_data.price_USDT

        data_reponse = {
            "Budget": budget,
            "Total Spend in ARS": total_spend_ars,
            "Total Spend in USDT": round(total_spend_usdt, 2),
            "Remaining Budget": round(budget - total_spend_usdt, 2),
        }

        return data_reponse

    async def _obtatin_total_02(self, data, budget: float):
        types = ["others", "food", "goOut", "fixed", "clothes", "books", "fubol"]

        totals = {types_expense: 0 for types_expense in types}

        for item in data:
            if item.type in totals:
                totals[item.type] += item.price_ARS

        for types_expense, total in totals.items():
            print(f"Total para {types_expense}: {total} ARS")

        total_globall = await self._obtatin_total(data, budget)
        print(total_globall)
        return {
            "Total Spend by Type": totals,
        }

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
                "uuid": formatted_data.uuid,
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

    async def process_data_all(self, data_expenses):
        data_reponse = []

        for element in data_expenses:
            data_list = {
                "uuid": element.uuid,
                "name": element.name,
                "price_ARS": element.price_ARS,
                "price_USDT": element.price_USDT,
                "type": element.type,
                "date": element.date,
                "coutes": element.coutes,
            }

            data_reponse.append(data_list)

        return data_reponse

    async def obtain_data(self, month: int | None = None):
        if month is None:
            bad_request("Month is required")

        month_expense = int(month)
        query_expenses = select(Expense).where(Expense.month == month_expense)

        data_expenses = await self.session.exec(query_expenses)
        return await self.process_data_all(data_expenses)

    async def get_expense_by_uuid(self, uuid: str):
        statement = select(Expense).where(Expense.uuid == uuid)
        query_expense = await self.session.exec(statement)
        data_expenses = await self.process_data(query_expense)
        return data_expenses

    async def get_total_by_type(self, month: int, budget: float):
        month_expense = int(month)  # REF: pass a query separeted method
        query = select(Expense).where(Expense.month == month_expense)
        data = await self.session.exec(query)
        return await self._obtatin_total_02(data, budget)

    async def delete_expense_by_uuid(self, uuid: str):
        query = select(Expense).where(Expense.uuid == uuid)
        result = await self.session.exec(query)
        expense_to_delete = result.one()
        await self.session.delete(expense_to_delete)
        await self.session.commit()
        return {"message": "Expense deleted successfully"}
