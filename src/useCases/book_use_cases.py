from abc import ABC, abstractmethod
from typing import List
from ..domain.book.model import Book


class BookUseCase(ABC):
    """BookUseCase usecase/bussiness logic of Book."""

    @abstractmethod
    async def get_books(self) -> List[Book]:
        pass

    @abstractmethod
    async def create_book(self, book_model: Book) -> Book:
        pass
