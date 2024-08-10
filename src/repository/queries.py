from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.book.model import Book


async def create_data_db(session, data: Book) -> None:
    try:
        session.add(data)
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e


async def get_books_db(session: AsyncSession):
    query = select(Book)
    book_data = await session.exec(query)
    return book_data


async def get_books_by_filter(session: AsyncSession, uuid: str):
    query = select(Book).where(Book.uuid == uuid)
    book_data = await session.exec(query)
    return book_data


async def delete_books_by_uuid(session: AsyncSession, uuid: str):
    query = select(Book).where(Book.uuid == uuid)
    result = await session.exec(query)
    book_to_delete = result.one()
    print("book_to_delete", book_to_delete)
    await session.delete(book_to_delete)
    await session.commit()
    return
