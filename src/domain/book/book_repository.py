from typing import Optional
from abc import abstractmethod, ABC
from ...domain.book.model import Book
from ...dto.books import BookSchema


class BookRepository(ABC):
    @abstractmethod
    async def findBookById(self, uuid: str) -> Optional[BookSchema]:
        pass

    @abstractmethod
    async def findBooks(self) -> list[BookSchema]:
        pass

    @abstractmethod
    async def removeBookById(self, uuid: str) -> None:
        pass

    @abstractmethod
    async def createBook(self, book: Book) -> Book:
        pass