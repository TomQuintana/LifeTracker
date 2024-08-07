from datetime import timedelta
from os import error

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.services.auth import Auth
from src.services.cotization import Cotization

from ..domain.user.model import User
from ..modelRequest.user import UserRequestModel


class UserService:
    auth_service = Auth()

    def __init__(self, session_db: AsyncSession):
        self.sesion = session_db
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30

    async def create_user(self, user_data: UserRequestModel) -> User:
        crypto_currency = "USDT"
        cotization_service = Cotization(crypto_currency)
        cotization = await cotization_service.calculate_cotization(user_data.budget_ARS)

        user = User(**user_data.model_dump())
        user.budget_USDT = cotization

        hasheg_password = self.auth_service.hash_password(user_data.password)
        user.password = hasheg_password

        self.sesion.add(user)
        await self.sesion.commit()
        return user

    async def _search_user_by_email(self, email_user: str):
        query = select(User).where(User.email == email_user)
        user_exist = await self.sesion.exec(query)
        return user_exist.first()

    async def login(self, email: str, password: str) -> str:
        try:
            is_user_exist = await self._search_user_by_email(email)
            if not is_user_exist:
                raise error

            is_password_valid = self.auth_service.verify_password(password, is_user_exist.password)
            if not is_password_valid:
                raise error

            budget_usdt = is_user_exist.budget_USDT
            if budget_usdt is None:
                budget_usdt = 0.0

            access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

            token = self.auth_service.generate_token(
                email,
                budget_usdt,
                access_token_expires,
            )
            return token

        except Exception as e:
            raise e
