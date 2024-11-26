from uuid import UUID

from sqlmodel import Field, SQLModel


class Book(SQLModel, table=True):
    __tablename__ = "books"  # type: ignore
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str
    type: str | None = None
    status: str = "unread"
    physically: bool = False
    description: str | None = None
    notes_location: str | None = None
    cover: str | None = None
    user_id: UUID
