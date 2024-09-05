from src.domain.book.model import Book
from ..utils.alerts import alert_not_found_resource

from ...domain.book.book_repository import BookRepository


class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository

    async def create_book(self, book_model) -> Book:
        try:
            book_data = book_model.dict()
            book_entity = Book(**book_data)
            await self.repository.createBook(book_entity)

            return book_entity

        except Exception as e:
            raise e

    async def get_books(self):
        try:
            book_data = await self.repository.findBooks()
        except Exception as e:
            raise e

        return book_data

    async def get_books_by_filter(self, uuid: str):
        try:
            book_data = await self.repository.findBookById(uuid)

            if book_data is None:
                alert_not_found_resource("Book not found")

            return book_data
        except Exception as e:
            raise e

    async def delete_books_by_uuid(self, uuid: str):
        try:
            is_book_exist = await self.repository.findBookById(uuid)

            if is_book_exist is None:
                alert_not_found_resource("Book not found")

            book_to_delete = await self.repository.removeBookById(uuid)

            return book_to_delete
        except Exception as e:
            raise e

    #
    # async def update_books_by_uuid(self, update_data: BookToUpdat, uuid: str):
    #     query = select(Book).where(Book.uuid == uuid)
    #     result = await self.session.exec(query)
    #     book_to_update = result.one()
    #
    #     if not book_to_update:
    #         alert_not_found_resource("Book not found")
    #
    #     update_data_dict = update_data.model_dump()
    #     for key, value in update_data_dict.items():
    #         setattr(book_to_update, key, value)
    #
    #     await self.session.commit()
    #     return self.session.refresh(book_to_update)
