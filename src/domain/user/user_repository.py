from abc import abstractmethod, ABC

from .model import User


class UserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: User):
        pass

    @abstractmethod
    async def get_user_by_id(self, id: str):
        pass
