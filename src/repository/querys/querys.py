from sqlmodel.ext.asyncio.session import AsyncSession
from src.domain.book.model import Book
# from src.useCases.book_use_cases import BookQueryUseCase


class QueryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _create_data_db(self, data: Book) -> None:
        self.session.add(data)
        return await self.session.commit()
