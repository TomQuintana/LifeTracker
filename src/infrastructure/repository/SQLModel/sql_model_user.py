from sqlmodel import select
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

    async def get_user_by_email(self, email: str):
        query = select(User).where(User.email == email)
        user_result = await self.session.exec(query)
        print(user_result.first())
        return user_result.first()

    # FIX: modify_badged
    async def modify_badged(self, email: str, badge: float):
        query = select(User).where(User.email == email)
        user = await self.session.exec(query)
        print(user.first())
        user.first().budget_ARS = badge
        user.budget_ARS = badge
        await self.session.commit()
        return user
