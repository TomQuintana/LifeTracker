import csv
import io

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

    async def create_book(self, book_model) -> Book:
        book = Book(**book_model.model_dump())
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

    async def upload_books_by_csv(self, file):
        print(file)
        content_str = file.decode("utf-8")  # Convert bytes to string
        csv_books = io.StringIO(content_str)  # Create a file-like object
        reader = csv.DictReader(csv_books)
        for row in reader:
            print(row)
            book = Book(
                title=row.get("\ufefftitle", ""),
                author=row.get("author", ""),
                type=row.get("type", ""),
                description=row.get("description", ""),
                status=row.get("status", ""),
                physically=row.get("physically ", "").lower() == "true",
            )

            self.session.add(book)
            await self.session.commit()
