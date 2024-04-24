from uuid import UUID, uuid4

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


class Expense(SQLModel, table=True):
    __tablename__ = "expenses"
    uuid: UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, unique=True, default=uuid4)
    )
    name: str
    price_ARS: float
    price_USDT: float | None = None
    type: str | None = None
    coutes: int | None = None
    date: str
