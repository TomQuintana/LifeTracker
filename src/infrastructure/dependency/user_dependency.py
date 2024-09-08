from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.db_manager import get_session
from ...infrastructure.repository.SQLModel.sql_model_user import SqlModelUserRepository
from ..services.user_service import UserService


def get_repository(session: AsyncSession = Depends(get_session)):
    return SqlModelUserRepository(session)


def get_expense_service(repository: SqlModelUserRepository = Depends(get_repository)):
    return UserService(repository)
