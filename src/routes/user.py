from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.db_manager import get_session
from src.services.user_service import UserService

router = APIRouter(prefix="/api/auth", tags=["User"])


class UserRequest(BaseModel):
    email: str
    password: str


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user():
    raise NotImplementedError("Not implemented yet")
    # await user_service.create_user(user_request)


@router.post("/login")
async def authenticate(request_user: UserRequest, session: AsyncSession = Depends(get_session)):
    user_service = UserService(session)
    token_user = await user_service.login(request_user.email, request_user.password)
    # return JSONResponse(content={'token': token_user}, status_code=200)
    return {"token": token_user}
