from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db.db_manager import init_db
from .routes.expense import router as expense_router
from .routes.user import router as user_router
from .routes.book import router as book_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting")
    await init_db()
    yield
    print("server is shutting down")


app = FastAPI(title="Life Tracker", lifespan=lifespan)
app.include_router(expense_router)
app.include_router(user_router)
app.include_router(book_router)
