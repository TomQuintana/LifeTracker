from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...infrastructure.repository.SQLModel.sql_model_habits import (
    SqlModelHabitsRepository,
)
from ..db.db_manager import get_session
from ..services.user_service import UserService


def get_repository(session: AsyncSession = Depends(get_session)):
    return SqlModelHabitsRepository(session)


def get_habits_service(repository: SqlModelHabitsRepository = Depends(get_repository)):
    return UserService(repository)
