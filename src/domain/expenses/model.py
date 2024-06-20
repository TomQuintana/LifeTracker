from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel

month = datetime.now().month
date_expense = datetime.now().date()


class Expense(SQLModel, table=True):
    __tablename__ = "expenses"
    uuid: UUID = Field(sa_column=Column(pg.UUID, primary_key=True, unique=True, default=uuid4))
    name: str
    price_ARS: float
    price_USDT: float | None = None
    type: str = "others"
    coutes: str | None = None
    month: int = datetime.now().month
    date: str | None = None
