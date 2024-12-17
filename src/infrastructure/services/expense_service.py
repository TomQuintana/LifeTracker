from src.infrastructure.services.auth import Auth

from ...domain.expenses.expenses_repository import ExpenseRepository
from ...domain.expenses.model import Expense
from ...domain.products.model import Products
from ...infrastructure.constants.cryptocurrency import crypto_currency_usdt
from ...infrastructure.constants.types_expenses import EXPENSE_TYPES

# from ...infrastructure.utils.alerts import bad_request
from ...infrastructure.utils.decoed_user_id import decoded_user_id

# from ...infrastructure.utils.valid_type_input import valid_type_input
from .cotization import Cotization

# from ...infrastructure.utils.expenses_utils import valid_is_month_pass


class ExpenseService:
    def __init__(self, repository: ExpenseRepository):
        self.repository = repository
        self.cotization_service = Cotization(crypto_currency_usdt)
        self.auth = Auth()

    async def create_expense(self, data, token):
        # if not valid_type_input(data.type):
        #     raise ValueError("Invalid type input")
        #
        try:
            user_id = decoded_user_id(token)

            cotization = await self.cotization_service.calculate_cotization(data.price_ARS)
            expense_data = data.dict()
            expenses_entity = Expense(**expense_data)
            expenses_entity.user_id = user_id
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

    async def fetch_data(self, month: int, token: str, cursor: int):
        # valid_month = valid_is_month_pass(month)
        # if not valid_month:
        #     bad_request("Month is required")

        # user_id = decoded_user_id(token)

        next_expenses = 1
        expenses_per_page = 8
        limit = expenses_per_page + next_expenses

        expenses = await self.repository.get_expenses_by_month(month, cursor, limit)

        if expenses is None:
            raise ValueError("No se pudieron obtener los gastos")

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
        next_cursor = None

        # NOTE: tengo un error el id cuando itero con los productos
        if len(expenses) == limit:
            next_cursor = expenses.pop().id

        return {"data": expenses, "cursor": next_cursor}

    async def fetch_total(self, month: int, token):
        # user_id = decoded_user_id(token)
        # valid_month = valid_is_month_pass(month)
        # if not valid_month:
        #     bad_request("Month is required")

        #
        #             book_data = await self.repository.findBooks(user_id, cursor, limit)
        #
        #             next_cursor = None
        #             if len(book_data) == limit:
        #                 next_cursor = book_data.pop().id
        #

        expenses_data = await self.repository.get_all_expenses_by_month(month)

        totals = {types_expense: 0 for types_expense in EXPENSE_TYPES}

        for expense in expenses_data:
            totals[expense.type] += expense.price_ARS

        final_totals = 0
        for key, value in totals.items():
            final_totals += value

        return {
            "total": final_totals,
            "rest": 560000 - final_totals,
            "expenses": totals,
        }

    async def coutes_expenses(self):
        try:
            expense_result = await self.repository.cuotes()
            return expense_result
        except Exception as e:
            raise e

    async def delete_expense(self, id: int):
        try:
            await self.repository.delete_expense(id)
        except Exception as e:
            raise e
