from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException, status

from fastapi.responses import JSONResponse

from .db.db_manager import init_db

# from .routes.expense import router as expense_router
from .routes.user import router as user_router
from .routes.book import router as book_router
from .middleware.verify_token import verify_token


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting")
    await init_db()
    yield
    print("server is shutting down")


app = FastAPI(title="Life Tracker", lifespan=lifespan)


@app.middleware("http")
async def verify_token_middleware(request: Request, call_next):
    protected_routes = ["/api/books"]

    token = request.headers.get("Authorization")

    if any(request.url.path.startswith(route) for route in protected_routes):
        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization token is missing"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            await verify_token(token)
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
                headers=e.headers,
            )

    response = await call_next(request)
    return response


app.include_router(user_router)
# app.include_router(expense_router)
app.include_router(book_router)
