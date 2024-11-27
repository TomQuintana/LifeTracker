from src.domain.book.model import Book
from src.infrastructure.constants.books_types import BOOKS_TYPES
from src.infrastructure.services.auth import Auth

from ...domain.book.book_repository import BookRepository
from ..utils.alerts import alert_book, alert_not_found_resource


class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository
        self.auth = Auth()

    async def _is_book_exist(self, uuid: str) -> bool:
        try:
            book = await self.repository.findBookById(uuid)
            if book is not None:
                return True
            return False
        except Exception as e:
            raise e

    async def create_book(self, data, token) -> Book:
        book_exist = await self.repository.findBookByTitle(data.title)
        if book_exist:
            alert_book("Book already exist", 409)

        valid_type = data.type in BOOKS_TYPES
        if not valid_type:
            alert_book("Book topic not valid", 400)

        try:
            token_decoded = self.auth.check_payload(token)
            user_id = token_decoded.get("user_id")

            book_data = data.dict()
            book_data["user_id"] = user_id
            book_entity = Book(**book_data)

            await self.repository.createBook(book_entity)
            return book_entity

        except Exception as e:
            print(e)
            raise e

    async def get_books(self, token: str, cursor: int):
        try:
            token_decoded = self.auth.check_payload(token)
            user_id = token_decoded.get("user_id")

            next_video = 1
            books_per_page = 10
            limit = books_per_page + next_video

            book_data = await self.repository.findBooks(user_id, cursor, limit)

            next_cursor = None
            if len(book_data) == limit:
                next_cursor = book_data.pop().id

        except Exception as e:
            raise e

        return {"data": book_data, "cursor": next_cursor}

    async def get_books_by_filter(self, type: str):
        print(type)
        try:
            book_data = await self.repository.filterBooks(type)

            if book_data is None:
                alert_not_found_resource("Book not found")

            return book_data
        except Exception as e:
            raise e

    async def delete_books_by_uuid(self, id: int):
        try:
            is_book_exist = await self.repository.findBookById(id)

            if is_book_exist is None:
                alert_not_found_resource("Book not found")

            book_to_delete = await self.repository.removeBookById(id)

            return book_to_delete
        except Exception as e:
            raise e

    async def update_books_by_uuid(self, uuid: str, data):
        try:
            books_status = await self._is_book_exist(uuid)

            if not books_status:
                alert_not_found_resource("Book not found")

            book_data = await self.repository.findBookById(uuid)
            data_to_updated = data.dict()
            print(data_to_updated)

            for key, value in data_to_updated.items():
                setattr(book_data, key, value)

            book_updated = await self.repository.updateBookById(book_data)
            return book_updated

        # for key, value in data_to_updated.items():
        #     # Solo actualizar si el campo no es None o se preserva el valor actual
        #     if value is not None:
        #         setattr(book_data, key, value)
        #     else:
        #         # Mantener el valor existente si no se proporciona uno nuevo
        #         current_value = getattr(book_data, key)
        #         setattr(book_data, key, current_value)
        #
        except Exception as e:
            raise e

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

    async def list_types(self):
        print("types")
        return BOOKS_TYPES

    async def search_book(self, book_title: str):
        print(book_title)
        try:
            book_data = await self.repository.searchBook(book_title)
            return book_data
        except Exception as e:
            raise e
