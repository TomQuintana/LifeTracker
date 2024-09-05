from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from ..config.dev_env import settings

async_engine = create_async_engine(settings.POSTGRESQL_URL, future=True)


async def init_db():
    async with async_engine.begin() as session_db:
        await session_db.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:  # type: ignore
    """Dependency to provide the session object"""
    async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session
