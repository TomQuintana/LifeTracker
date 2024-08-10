from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.book.model import Book
from src.utils.format_data import format_data_list, format_data_dict
from src.utils.alert import not_found_resource


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # REF: pass this to general service
    async def _create_data_db(self, data: Book) -> None:
        self.session.add(data)
        return await self.session.commit()

    async def create_book(self, book_model) -> Book:
        book = Book(**book_model.model_dump())
        await self._create_data_db(book)
        return book

    async def get_books(self):
        query = select(Book)
        book_data = await self.session.exec(query)
        book_response = format_data_list(book_data)
        return book_response

    async def get_books_by_filter(self, uuid: str):
        query = select(Book).where(Book.uuid == uuid)
        book_data = await self.session.exec(query)
        book_response = format_data_dict(book_data)
        return book_response

    async def delete_books_by_uuid(self, uuid: str):
        query = select(Book).where(Book.uuid == uuid)
        result = await self.session.exec(query)
        book_to_delete = result.one()
        await self.session.delete(book_to_delete)
        await self.session.commit()
        return book_to_delete

    async def update_books_by_uuid(self, data: dict, uuid: str):
        query = select(Book).where(Book.uuid == uuid)
        result = await self.session.exec(query)

        book_to_update = result.one()
        if not book_to_update:
            not_found_resource("Book not found")

        book_to_update.status = data.status  # type: ignore

        return await self.session.commit()
