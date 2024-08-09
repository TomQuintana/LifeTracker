from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.db.db_manager import init_db

# from src.infrastructure.routes.expense import router as expense_router
from src.infrastructure.routes.user import router as user_router
from src.infrastructure.routes.book import router as book_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting")
    await init_db()
    yield
    print("server is shutting down")


app = FastAPI(title="Life Tracker", lifespan=lifespan)
# app.include_router(expense_router)
app.include_router(user_router)
app.include_router(book_router)
