from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.db_manager import get_session
from ..infrastructure.repository.sqlModel import SqlModelRepository
from ..services.book_services import BookService

# from ..infrastructure.repository.sqlModel import SqlModelRepository


# session: AsyncSession = Depends(get_session),


def get_repository(session: AsyncSession = Depends(get_session)):
    return SqlModelRepository(session)


def get_book_service(repository: SqlModelRepository = Depends(get_repository)):
    return BookService(repository)
