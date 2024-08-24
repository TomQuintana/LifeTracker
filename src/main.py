from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.middleware.verify_token_middleware import verify_token_middleware
from src.middleware.origins import origins

from .db.db_manager import init_db
from .routes.book import router as book_router
from .routes.expense import router as expense_router
from .routes.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting")
    await init_db()
    print("server docc - http://localhost:3000/docs")
    yield
    print("server is shutting down")


app = FastAPI(title="Life Tracker", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(verify_token_middleware)

app.include_router(user_router)
app.include_router(expense_router)
app.include_router(book_router)
