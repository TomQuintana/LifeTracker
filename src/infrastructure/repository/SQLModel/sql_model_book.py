from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.book.model import Book

from ....application.dto.books import BookSchema
from ....domain.book.book_repository import BookRepository


class SqlModelBookRepository(BookRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def findBookById(self, uuid: str) -> BookSchema | None:
        query = select(Book).where(Book.uuid == uuid)
        result = await self.session.exec(query)
        return result.first()

    async def findBooks(self) -> list[BookSchema]:
        query = select(Book)
        result = await self.session.exec(query)
        return result.all()

    async def removeBookById(self, uuid: str) -> None:
        query = select(Book).where(Book.uuid == uuid)
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
