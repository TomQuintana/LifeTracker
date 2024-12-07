from abc import ABC, abstractmethod


from src.domain.products.model import Products

from .model import Expense


class ExpenseRepository(ABC):
    @abstractmethod
    async def create_expenses(self, expense: Expense):
        pass

    @abstractmethod
    async def create_products(self, product: Products):
        pass

    @abstractmethod
    async def get_expenses_by_month(self, month: int, cursor: int, limit: int):
        pass

    @abstractmethod
    async def get_all_expenses_by_month(self, month: int):
        pass

    @abstractmethod
    async def get_products_by_expense_id(self, expense_uuid: str):
        pass

    @abstractmethod
    async def cuotes(self):
        pass

    @abstractmethod
    async def delete_expense(self, id: int):
        pass
