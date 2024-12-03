from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel

month = datetime.now().month
date_expense = datetime.now().date()


class Expense(SQLModel, table=True):
    __tablename__ = "expenses"
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price_ARS: float
    price_USDT: float | None = None
    type: str = "others"
    coutes: str | None = None
    month: int = datetime.now().month
    date: str | None = None
    user_id: UUID
