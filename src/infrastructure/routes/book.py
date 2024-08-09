from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.db_manager import get_session
from src.modelRequest.book import BookRequest

from ..services.auth import Auth
from ..services.book import BookService

auth_service = Auth()

router = APIRouter(
    prefix="/api/book", tags=["Book"], dependencies=[Depends(auth_service.get_token)]
)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_book(
    book: BookRequest,
    session: AsyncSession = Depends(get_session),
):
    book_service = BookService(session)
    book_created = await book_service.create_book(book)
    return book_created


@router.get("/info", status_code=status.HTTP_200_OK)
async def get_books(
    session: AsyncSession = Depends(get_session),
):
    book_service = BookService(session)
    books = await book_service.get_books()
    return books
