from sqlmodel import UUID, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.expenses.model import Expense
from src.domain.expenses.expenses_repository import ExpenseRepository
from src.domain.products.model import Products


class SqlModelExpenseRepository(ExpenseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_expenses(self, expense: Expense):
        expense_created = self.session.add(expense)
        await self.session.commit()
        return expense_created

    async def create_products(self, product: Products):
        product_created = self.session.add(product)
        await self.session.commit()
        return product_created

    async def get_expenses_by_month(self, month: int, user_id: UUID):
        print(month, user_id)
        query = select(Expense).where(Expense.user_id == user_id, Expense.month == month)
        result = await self.session.exec(query)
        return result.all()

    async def get_products_by_expense_id(self, expense_uuid: str):
        query = select(Products).where(Products.expense_id == expense_uuid)
        result = await self.session.exec(query)
        return result.all()
