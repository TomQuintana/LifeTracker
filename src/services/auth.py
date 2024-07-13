from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from ..config.config import settings


class Auth:
    """
    Service for managing auth operations with users.
    """

    secret_key = settings.SECRECT_KEY
    algorithm = settings.ALGORITHM

    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self):
        pass

    def hash_password(self, password: str):
        return self.bcrypt_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.bcrypt_context.verify(plain_password, hashed_password)

    def generate_token(
        self,
        email: str,
        budget_usdt: float,
        expires_delta: timedelta | None = None,
    ) -> str:
        encode = {"email_user": email, "user_budge": budget_usdt}

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        encode["exp"] = expire

        return jwt.encode(encode, self.secret_key, self.algorithm)

    def check_payload(self, token):
        decoded_token = jwt.decode(token, self.secret_key)
        return decoded_token
