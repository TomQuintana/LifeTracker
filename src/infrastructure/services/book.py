from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.book.model import Book


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # REF: pass this to general service
    async def _create_data_db(self, data: Book) -> None:
        self.session.add(data)
        return await self.session.commit()

    async def create_book(self, book_data) -> Book:
        book = Book(**book_data.model_dump())
        await self._create_data_db(book)
        return book

    async def get_books(self):
        query = select(Book)
        book_data = await self.session.exec(query)

        book_response = []
        for book in book_data:
            book_response.append(book)

        return book_response
