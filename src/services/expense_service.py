from ..domain.expenses.expenses_repository import ExpenseRepository
from ..domain.expenses.model import Expense
from ..domain.products.model import Products
from ..utils.alert import bad_request
from ..utils.valid_type_input import valid_type_input
from .cotization import Cotization

crypto_currency = "USDT"


class ExpenseService:
    def __init__(self, repository: ExpenseRepository):
        self.repository = repository
        self.cotization_service = Cotization(crypto_currency)

    async def create_expense(self, data):
        if not valid_type_input(data.type):
            raise ValueError("Invalid type input")

        try:
            cotization = await self.cotization_service.calculate_cotization(data.price_ARS)
            expense_data = data.dict()
            expenses_entity = Expense(**expense_data)
            expenses_entity.price_USDT = cotization

            await self.repository.create_expenses(expenses_entity)

            if len(data.products) == 0:
                cotization = await self.cotization_service.calculate_cotization(
                    expenses_entity.price_ARS
                )

                product_data = {
                    "name": expenses_entity.name,
                    "price_ARS": expenses_entity.price_ARS,
                    "price_USDT": cotization,
                    "expense_id": expenses_entity.id,
                }

                product_data = Products(**product_data)
                await self.repository.create_products(product_data)

                return expenses_entity

            for product in expense_data["products"]:
                product_data = Products(**product)
                cotization = await self.cotization_service.calculate_cotization(
                    product_data.price_ARS
                )
                product_data.price_USDT = cotization
                product_data.expense_id = expenses_entity.id

                await self.repository.create_products(product_data)

            return expenses_entity

        except Exception as e:
            raise e

    async def fetch_data(self, month: int):
        if not month:
            bad_request("Month is required")

        expenses = await self.repository.get_expenses_by_month(month)

        data_response = []
        for expense in expenses:
            products = await self.repository.get_products_by_expense_id(expense.id)

            if len(products) > 1:
                expenses_data = {
                    "id": expense.id,
                    "name": expense.name,
                    "price_ARS": expense.price_ARS,
                    "price_USDT": expense.price_USDT,
                    "type": expense.type,
                    "date": expense.date,
                    "coutes": expense.coutes,
                    "products": products,
                }
            else:
                expenses_data = {
                    "id": expense.id,
                    "name": expense.name,
                    "price_ARS": expense.price_ARS,
                    "price_USDT": expense.price_USDT,
                    "type": expense.type,
                    "date": expense.date,
                    "coutes": expense.coutes,
                }

            data_response.append(expenses_data)

        return data_response
