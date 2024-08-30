from fastapi import APIRouter, Depends, status

from src.dto.books import BookToCreate
from src.services.auth import Auth
from src.services.book_services import BookService

from ..infrastructure.dependecy import get_book_service
from ..interfaces.response_schemas import BookResponse
from ..infrastructure.utils.alert import success_book_deleted

auth_service = Auth()
router = APIRouter(prefix="/api/books", tags=["Book"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(
    data: BookToCreate,
    book_service: BookService = Depends(get_book_service),
):
    book_created = await book_service.create_book(data)
    return BookResponse(**book_created.model_dump())


@router.get("/", status_code=status.HTTP_200_OK)
async def get_books(book_service: BookService = Depends(get_book_service)):
    books = await book_service.get_books()
    return books


@router.get("/{uuid}", status_code=status.HTTP_200_OK)
async def get_books_by_filter(uuid: str, book_service: BookService = Depends(get_book_service)):
    book = await book_service.get_books_by_filter(uuid)
    return book


@router.delete("/{uuid}", status_code=status.HTTP_200_OK)
async def delete_books_by_uuid(uuid: str, book_service: BookService = Depends(get_book_service)):
    await book_service.delete_books_by_uuid(uuid)
    return success_book_deleted()


# @router.put("/{uuid}", status_code=status.HTTP_200_OK)
# async def update_books_by_uuid(
#     uuid: str,
#     data: BookToUpdat,
#     session: AsyncSession = Depends(get_session),
# ):
#     #book_service = BookService(session)
#     await book_service.update_books_by_uuid(data, uuid)  # type: ignore
#     return {"message": "Book updated successfully"}
