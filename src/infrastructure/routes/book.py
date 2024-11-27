from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.security import OAuth2PasswordBearer

from ...application.dto.books import BookToCreate, BookToUpdate
from ..dependency.book_dependecy import get_book_service
from ..services.auth import Auth
from ..services.book_services import BookService
from ..utils.alerts import success_book_deleted

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
auth_service = Auth()
router = APIRouter(prefix="/api/books", tags=["Book"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(
    data: BookToCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
    book_service: BookService = Depends(get_book_service),
):
    book_created = await book_service.create_book(data, token)
    return book_created


@router.get("/", status_code=status.HTTP_200_OK)
async def get_books(
    token: Annotated[str, Depends(oauth2_scheme)],
    # limit: int = Query(None, description="The limit of data per page"),
    # offset: int = Query(None, description="The month for filtering expenses"),
    cursor: int,
    book_service: BookService = Depends(get_book_service),
):
    books = await book_service.get_books(token, cursor)
    return books


@router.get("/topics", status_code=status.HTTP_200_OK)
async def get_books_types(book_service: BookService = Depends(get_book_service)):
    list_types = await book_service.list_types()
    return {"book Topic": list_types}


@router.get("/filter", status_code=status.HTTP_200_OK)
async def get_books_by_type(
    type: str = Query(None, description="The month for filtering expenses"),
    book_service: BookService = Depends(get_book_service),
):
    books = await book_service.get_books_by_filter(type)
    return books


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_books_by_uuid(id: int, book_service: BookService = Depends(get_book_service)):
    await book_service.delete_books_by_uuid(id)
    return success_book_deleted()


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_books_by_uuid(
    uuid: str, data: BookToUpdate, book_service: BookService = Depends(get_book_service)
):
    # book_service = BookService(session)
    await book_service.update_books_by_uuid(uuid, data)
    return {"message": "Book updated successfully"}


@router.get("/search", status_code=status.HTTP_200_OK)
async def search_book(
    title: str = Query(None, description="The month for filtering expenses"),
    book_service: BookService = Depends(get_book_service),
):
    books = await book_service.search_book(title)
    return books
