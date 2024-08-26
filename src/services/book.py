from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.book.model import Book
from src.utils.alert import not_found_resource
from src.utils.format_data import format_data_dict

from ..repository.queries import (
    create_data_db,
    delete_books_by_uuid,
    get_books_by_filter,
    get_books_db,
)


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_book(self, book_model) -> Book:
        book = Book(**book_model.model_dump())

        try:
            await create_data_db(self.session, book)
        except Exception as e:
            raise e

        return book

    async def get_books(self):
        try:
            book_data = await get_books_db(self.session)
        except Exception as e:
            raise e

        book_response = book_data.all()
        return book_response

    async def get_books_by_filter(self, uuid: str):
        book_data = await get_books_by_filter(self.session, uuid)
        book_response = book_data

        if book_response is None:
            print("Book not found")
            not_found_resource("Book not found")

        book_response = format_data_dict(book_data)
        return book_response

    async def delete_books_by_uuid(self, uuid: str):
        try:
            await get_books_by_filter(self.session, uuid)
            book_to_delete = await delete_books_by_uuid(self.session, uuid)
            return book_to_delete

        except Exception as e:
            raise e

    async def update_books_by_uuid(self, data: dict, uuid: str):
        query = select(Book).where(Book.uuid == uuid)
        result = await self.session.exec(query)
        book_to_update = result.one()

        if not book_to_update:
            not_found_resource("Book not found")

        book_to_update.status = data.status  # type: ignore
        book_to_update.sqlmodel_update(data)

        await self.session.commit()
        return self.session.refresh(book_to_update)
