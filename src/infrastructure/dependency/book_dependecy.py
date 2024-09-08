from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.db_manager import get_session
from ...infrastructure.repository.SQLModel.sql_model_book import SqlModelBookRepository
from ..services.book_services import BookService


def get_repository(session: AsyncSession = Depends(get_session)):
    return SqlModelBookRepository(session)


def get_book_service(repository: SqlModelBookRepository = Depends(get_repository)):
    return BookService(repository)
