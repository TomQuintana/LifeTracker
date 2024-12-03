from abc import ABC, abstractmethod


from .model import Habits


class HabitsRepository(ABC):
    @abstractmethod
    async def create_habit(self, data: Habits):
        pass
