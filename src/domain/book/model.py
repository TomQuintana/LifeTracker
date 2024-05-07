from uuid import UUID, uuid4
from datetime import datetime

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


class Book(SQLModel, table=True):
    __tablename__ = "books"
    uuid: UUID = Field(sa_column=Column(pg.UUID, primary_key=True, unique=True, default=uuid4))
    title: str
    author: str
    type: str | None = None
    status: str = "unread"
    description: str | None = None
    created_date: datetime = datetime.now().date()
