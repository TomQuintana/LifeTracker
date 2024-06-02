from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.services.user_service import UserService

from ..dependency.user.dependency_manager import DependencyManager
from ..modelRequest.user import UserRequestModel

router = APIRouter(prefix="/api/user", tags=["User"])


dependency_inyection = DependencyManager()


class UserRequest(BaseModel):
    email: str
    password: str


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_request: UserRequestModel,
    user_service=Depends(dependency_inyection.use_user_service),
):
    await user_service.create_user(user_request)


@router.post("/login")
async def authenticate(request_user: UserRequest, session: AsyncSession = Depends(get_session)):
    user_service = UserService(session)
    token_user = await user_service.login(request_user.email, request_user.password)

    return JSONResponse(content={"token": token_user}, status_code=200)
