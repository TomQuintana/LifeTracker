from sqlalchemy.sql.operators import is_not, like_op
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.expenses.expenses_repository import ExpenseRepository
from src.domain.expenses.model import Expense
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

    async def get_expenses_by_month(self, month: int, cursor: int, limit: int):
        # query = select(Expense).where(
        #     Expense.user_id == user_id, Expense.month == month
        # )

        # query = select(Book).where(Book.id >= cursor).limit(limit)
        query = select(Expense).where(Expense.id >= cursor).limit(limit)
        result = await self.session.exec(query)
        return result.all()

    async def get_all_expenses_by_month(self, month: int):
        query = select(Expense).where(Expense.month == month)
        result = await self.session.exec(query)
        return result.all()

    async def get_products_by_expense_id(self, expense_uuid: str):
        query = select(Products).where(Products.expense_id == expense_uuid)
        result = await self.session.exec(query)
        return result.all()

    async def search(self, book_title: str):
        query = select(Expense).filter(like_op(Expense.title, f"%{book_title}%"))
        result = await self.session.exec(query)
        return result.all()

    async def cuotes(self):
        query = select(Expense).where(is_not(Expense.coutes, None))
        result = await self.session.exec(query)
        return result.all()

    async def delete_expense(self, id: int):
        query = select(Expense).where(Expense.id == id)
        result = await self.session.exec(query)
        id_expense = result.one()
        await self.session.delete(id_expense)
        await self.session.commit()
        return
