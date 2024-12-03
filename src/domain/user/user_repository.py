from abc import ABC, abstractmethod

from .model import User


class UserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str):
        pass

    @abstractmethod
    async def modify_badged(self, email: str, badge: float) -> User:
        pass
