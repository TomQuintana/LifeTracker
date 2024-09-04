from uuid import UUID, uuid4

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


class Products(SQLModel, table=True):
    __tablename__ = "products"
    id: UUID = Field(sa_column=Column(pg.UUID, primary_key=True, unique=True, default=uuid4))
    name: str
    quantity: int = 1
    price_ARS: float
    price_USDT: float | None = None
    expense_id: UUID = Field(default=None, foreign_key="expenses.id")
