from pydantic import BaseModel


class CreateBookRequest(BaseModel):
    title: str
    author: str
    type: str
    description: str | None = None
    status: str | None = None
    physically: bool | None = None


class UpdateBookRequest(BaseModel):
    title: str | None = None
    author: str | None = None
    type: str | None = None
    description: str | None = None
    status: str | None = None
    physically: bool | None = None
