from abc import ABC, abstractmethod
from typing import Optional

from ...application.dto.books import BookSchema
from ...domain.book.model import Book


class BookRepository(ABC):
    @abstractmethod
    async def findBookById(self, uuid: str) -> Optional[BookSchema]:
        pass

    @abstractmethod
    async def findBookByTitle(self, uuid: str) -> Optional[BookSchema]:
        pass

    @abstractmethod
    async def findBooks(self, user_id) -> list[BookSchema]:
        pass

    @abstractmethod
    async def removeBookById(self, uuid: str) -> None:
        pass

    @abstractmethod
    async def createBook(self, book: Book) -> Book:
        pass

    @abstractmethod
    async def updateBookById(self, data) -> None:
        pass
