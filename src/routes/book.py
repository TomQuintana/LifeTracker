from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.db_manager import get_session
from src.services.auth import Auth
from src.services.book import BookService

# from src.modelRequest.book import BookRequest
from ..interfaces.requests_schemas import CreateBookRequest, UpdateBookRequest
from ..interfaces.response_schemas import BookResponse, BookResponseAll

auth_service = Auth()

router = APIRouter(prefix="/api/books", tags=["Book"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(
    book: CreateBookRequest,
    session: AsyncSession = Depends(get_session),
):
    book_service = BookService(session)
    book_created = await book_service.create_book(book)
    return BookResponse(**book_created.model_dump())


@router.get("/", status_code=status.HTTP_200_OK)
async def get_books(
    session: AsyncSession = Depends(get_session),
):
    book_service = BookService(session)
    books = await book_service.get_books()
    return [BookResponseAll(**book.model_dump()) for book in books]


@router.get("/{uuid}", status_code=status.HTTP_200_OK)
async def get_books_by_filter(uuid: str, session: AsyncSession = Depends(get_session)):
    book_service = BookService(session)
    book = await book_service.get_books_by_filter(uuid)
    return book


@router.delete("/{uuid}", status_code=status.HTTP_200_OK)
async def delete_books_by_uuid(uuid: str, session: AsyncSession = Depends(get_session)):
    book_service = BookService(session)
    await book_service.delete_books_by_uuid(uuid)
    return {"message": "Book deleted successfully"}


@router.put("/{uuid}", status_code=status.HTTP_200_OK)
async def update_books_by_uuid(
    uuid: str,
    data: UpdateBookRequest,
    session: AsyncSession = Depends(get_session),
):
    book_service = BookService(session)
    await book_service.update_books_by_uuid(data, uuid)  # type: ignore
    return {"message": "Book updated successfully"}
