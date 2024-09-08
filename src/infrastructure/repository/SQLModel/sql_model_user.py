from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.user.model import User
from src.domain.user.user_repository import UserRepository


class SqlModelUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: User) -> User:
        user_created = self.session.add(user)
        await self.session.commit()
        return user_created
