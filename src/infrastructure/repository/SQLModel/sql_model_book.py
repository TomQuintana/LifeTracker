from sqlalchemy.sql.operators import like_op
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.book.model import Book

from ....application.dto.books import BookSchema
from ....domain.book.book_repository import BookRepository


class SqlModelBookRepository(BookRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def findBookById(self, id: str) -> BookSchema | None:
        query = select(Book).where(Book.id == id)
        result = await self.session.exec(query)
        return result.first()

    async def findBookByTitle(self, title: str):
        query = select(Book).where(Book.title == title)
        result = await self.session.exec(query)
        return result.first()

    async def findBooks(self, user_id, cursor, limit) -> list[BookSchema]:
        query = select(Book).where(Book.id >= cursor).limit(limit)
        result = await self.session.exec(query)
        return result.all()

    async def removeBookById(self, id) -> None:
        query = select(Book).where(Book.id == id)
        result = await self.session.exec(query)
        book_to_delete = result.one()
        await self.session.delete(book_to_delete)
        await self.session.commit()
        return book_to_delete

    async def createBook(self, book: Book) -> Book:
        book_created = self.session.add(book)
        await self.session.commit()
        return book_created

    async def updateBookById(self, data) -> None:
        book_updated = self.session.add(data)
        await self.session.commit()
        return book_updated

    async def filterBooks(self, filter_type: str):
        query = select(Book).where(filter_type == Book.type)
        result = await self.session.exec(query)
        return result.all()

    async def filter_books_by_status(self, books_status: str):
        query = select(Book).where(books_status == Book.status)
        result = await self.session.exec(query)
        return result.all()

    async def searchBook(self, book_title: str):
        query = select(Book).filter(like_op(Book.title, f"%{book_title}%"))
        result = await self.session.exec(query)
        return result.all()
