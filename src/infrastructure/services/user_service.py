from datetime import timedelta

from sqlmodel import select

from src.domain.user.user_repository import UserRepository
from src.infrastructure.utils.alerts import alert_not_found_resource

from ...domain.user.model import User
from ..services.auth import Auth
from ..services.cotization import Cotization


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.auth_service = Auth()

    async def create_user(self, user_data) -> User:
        crypto_currency = "USDT"
        cotization_service = Cotization(crypto_currency)
        cotization = await cotization_service.calculate_cotization(user_data.budget_ARS)

        user = User(**user_data.model_dump())
        user.budget_USDT = cotization

        hasheg_password = self.auth_service.hash_password(user_data.password)
        user.password = hasheg_password

        try:
            await self.repository.create_user(user)
            return user

        except Exception as e:
            raise e

    def fetch_user(self, email: str):
        return self.repository.get_user_by_email(email)

    async def _search_user_by_email(self, email_user: str):
        query = select(User).where(User.email == email_user)
        user_exist = await self.sesion.exec(query)
        return user_exist.first()

    async def login(self, email: str, password: str):
        print(password, email)
        try:
            user = await self.repository.get_user_by_email(email)
            print("user", user)

            if not user:
                alert_not_found_resource(detail="User not found")

            is_password_valid = self.auth_service.verify_password(password, user.password)
            if not is_password_valid:
                alert_not_found_resource(detail="Invalid Credentials")

            access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
            user_id_str = str(user.id)

            token = self.auth_service.generate_token(
                email,
                user_id_str,
                access_token_expires,
            )

            return token

        except Exception as e:
            raise e

    async def update_badge(self, data):
        try:
            user = await self.repository.get_user_by_email(data.email)
            if not user:
                alert_not_found_resource(detail="User not found")

            modify_badge = await self.repository.modify_badged(data.email, data.badge)
            print("data", modify_badge)
            return modify_badge
        except Exception as e:
            raise e
