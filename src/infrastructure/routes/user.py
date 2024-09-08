from fastapi import APIRouter, Depends, status

from src.application.dto.user import UserSchema

from ..dependency.user_dependency import get_user_service
from ..services.user_service import UserService

router = APIRouter(prefix="/api/user", tags=["User"])


# class UserRequest(BaseModel):
#     email: str
#     password: str
#
#
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(data: UserSchema, user_service: UserService = Depends(get_user_service)):
    user = await user_service.create_user(data)
    print(user)
    return user


# @router.post("/login")
# async def authenticate(request_user: UserRequest, session: AsyncSession = Depends(get_session)):
#     user_service = UserService(session)
#     token_user = await user_service.login(request_user.email, request_user.password)
#     # return JSONResponse(content={'token': token_user}, status_code=200)
#     return {"token": token_user}
