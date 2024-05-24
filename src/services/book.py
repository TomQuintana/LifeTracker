from sqlmodel import select
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
        print(book_model)
        book = Book(**book_model.model_dump())
        print(book)
        await self._create_data_db(book)

        return book

    async def get_books(self):
        query = select(Book)
        book_data = await self.session.exec(query)

        book_response = []
        for book in book_data:
            book_response.append(book)

        return book_response

    # TODO: review
    async def get_books_by_filter(self, filter_value: str):
        query = select(Book).where(Book.filter_value)
        book_data = await self.session.exec(query)

        book_response = []
        for book in book_data:
            book_response.append(book)

        return book_response

        # query = select(Expense).where(Expense.month == month_expense)
