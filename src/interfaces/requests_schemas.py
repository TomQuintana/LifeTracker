from pydantic import BaseModel


class CreateBookRequest(BaseModel):
    title: str
    author: str
    type: str
    description: str | None = None
    status: str | None = None
    physically: bool | None = None


class UpdateBookRequest(BaseModel):
    title: str
    author: str
    published_date: str
