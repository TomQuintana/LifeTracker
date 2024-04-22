from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db.main import init_db
from .routes.expense import router as expense_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting")
    await init_db()
    yield
    print("server is shutting down")

app = FastAPI(title='Life Tracker', lifespan=lifespan)
app.include_router(expense_router)
