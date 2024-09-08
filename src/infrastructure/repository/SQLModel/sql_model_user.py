from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.user.model import User
from src.domain.user.user_repository import UserRepository


class SqlModelUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_expenses(self, user: User):
        print("create user", user)

    async def get_expenses_by_month(self, id: str):
        print("get user")
