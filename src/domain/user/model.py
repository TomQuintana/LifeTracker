from uuid import UUID, uuid4

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: UUID = Field(sa_column=Column(pg.UUID, primary_key=True, unique=True, default=uuid4))
    email: str
    password: str
    first_name: str
    last_name: str
    is_active: bool = True
    budget_ARS: float
    budget_USDT: float | None = None
