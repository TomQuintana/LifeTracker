from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.modelRequest.book import BookRequest
from src.services.book import BookService

router = APIRouter(prefix="/api/book", tags=["Book"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookRequest, session: AsyncSession = Depends(get_session)):
    book_service = BookService(session)
    book_created = await book_service.create_book(book)
    return book_created


@router.get("/data", status_code=status.HTTP_200_OK)
async def get_books(session: AsyncSession = Depends(get_session)):
    book_service = BookService(session)
    books = await book_service.get_books()
    return books


@router.get("/filter/{filter}", status_code=status.HTTP_200_OK)
async def get_books_by_filter(filter: str, session: AsyncSession = Depends(get_session)):
    book_service = BookService(session)
    books = await book_service.get_books_by_filter(filter)
    return books


@router.post("/upload-csv", status_code=status.HTTP_201_CREATED)
async def upload_csv(file: UploadFile = File(...), session: AsyncSession = Depends(get_session)):
    file_contents = await file.read()
    book_service = BookService(session)
    await book_service.upload_books_by_csv(file_contents)
    return {"message": "File uploaded successfully"}
