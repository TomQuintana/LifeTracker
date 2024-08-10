from pydantic import BaseModel
from uuid import UUID


class BookResponse(BaseModel):
    uuid: UUID
    title: str
    author: str
    status: str
    type: str


class BookResponseAll(BaseModel):
    uuid: UUID
    title: str
    status: str
    type: str


class BookByUuidResponse(BookResponse):
    notes: str | None = None
