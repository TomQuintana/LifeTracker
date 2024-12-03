from sqlmodel.ext.asyncio.session import AsyncSession


# from src.domain.user.user_repository import UserRepository


class SqlModelHabitsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_habits(self, data):
        habit_created = self.session.add(data)
        await self.session.commit()
        return habit_created
