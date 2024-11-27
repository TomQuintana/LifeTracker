from abc import ABC, abstractmethod
from typing import Optional, Sequence

from ...application.dto.books import BookSchema
from ...domain.book.model import Book


class BookRepository(ABC):
    @abstractmethod
    async def findBookById(self, id) -> Optional[BookSchema]:
        pass

    @abstractmethod
    async def findBookByTitle(self, uuid: str) -> Optional[BookSchema]:
        pass

    @abstractmethod
    async def findBooks(self, user_id, cursor, limit) -> list[BookSchema]:
        pass

    @abstractmethod
    async def removeBookById(self, id) -> None:
        pass

    @abstractmethod
    async def createBook(self, book: Book) -> Book:
        pass

    @abstractmethod
    async def updateBookById(self, data) -> None:
        pass

    @abstractmethod
    async def filterBooks(self, filter_type: str) -> Sequence[Book]:
        pass

    @abstractmethod
    async def searchBook(self, book_title: str) -> Sequence[Book]:
        pass
