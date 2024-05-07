from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.book.model import Book


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # REF: pass this to general service
    async def _create_data_db(self, data):
        self.session.add(data)
        await self.session.commit()

    async def create_book(self, book_model) -> Book:
        book = Book(**book_model.model_dump())
        await self._create_data_db(book)

        return book
