from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.db_manager import get_session

# from src.modelRequest.book import BookRequest
from src.services.auth import Auth
from src.services.book import BookService

auth_service = Auth()

router = APIRouter(prefix="/api/books", tags=["Book"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(
    book,
    session: AsyncSession = Depends(get_session),
):
    book_service = BookService(session)
    book_created = await book_service.create_book(book)
    return book_created


@router.get("/", status_code=status.HTTP_200_OK)
async def get_books(
    session: AsyncSession = Depends(get_session),
):
    book_service = BookService(session)
    books = await book_service.get_books()
    return books


@router.get("/{filter}", status_code=status.HTTP_200_OK)
async def get_books_by_filter(filter: str, session: AsyncSession = Depends(get_session)):
    book_service = BookService(session)
    books = await book_service.get_books_by_filter(filter)
    return books


# @router.post("/upload-csv", status_code=status.HTTP_201_CREATED)
# async def upload_csv(file: UploadFile = File(...), session: AsyncSession = Depends(get_session)):
#     file_contents = await file.read()
#     book_service = BookService(session)
#     await book_service.upload_books_by_csv(file_contents)
#     return {"message": "File uploaded successfully"}
