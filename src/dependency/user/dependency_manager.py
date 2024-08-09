from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.services.user_service import UserService

from ...db.manage_db import get_session


class DependencyManager:
    def __init__(self):
        pass

    async def use_user_service(self, session_db: AsyncSession = Depends(get_session)):
        return UserService(session_db)
