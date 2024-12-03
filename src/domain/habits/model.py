from datetime import datetime
from uuid import UUID, uuid4

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel

month = datetime.now().month
date_expense = datetime.now().date()


class Habits(SQLModel, table=True):
    __tablename__ = "habits"  # type: ignore
    id: UUID = Field(sa_column=Column(pg.UUID, primary_key=True, unique=True, default=uuid4))
    type: str
    quantity: int
    user_id: UUID
    month: int = datetime.now().month
