from pydantic import BaseModel


class BookRequest(BaseModel):
    title: str
    author: str
    type: str
    status: str | None = "unread"
    physically: bool | None = False
