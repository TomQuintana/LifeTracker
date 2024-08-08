from uuid import UUID, uuid4

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


class Book(SQLModel, table=True):
    __tablename__ = "books"  # type: ignore
    uuid: UUID = Field(sa_column=Column(pg.UUID, primary_key=True, unique=True, default=uuid4))
    title: str
    author: str
    type: str | None = None
    status: str
    physically: bool
    description: str | None = None
    notes: str | None = None
