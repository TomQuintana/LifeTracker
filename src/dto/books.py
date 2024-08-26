from pydantic import BaseModel


class BookSchema(BaseModel):
    title: str | None = None
    author: str | None = None
    type: str | None = None
    description: str | None = None
    status: str = "unread"
    physically: bool | None = None


class BookToUpdat(BookSchema):
    pass
