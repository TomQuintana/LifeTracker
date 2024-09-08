from pydantic import BaseModel
from sqlmodel import SQLModel


class BookSchema(BaseModel):
    title: str | None = None
    author: str | None = None
    type: str | None = None
    description: str | None = None
    status: str | None = None
    physically: bool | None = None


class BookToUpdate(SQLModel):
    title: str | None = None
    author: str | None = None
    type: str | None = None
    description: str | None = None
    status: str | None = None
    physically: bool | None = None


class BookToCreate(BookSchema):
    pass
