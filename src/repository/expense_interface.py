from abc import ABC, abstractmethod


class ExpenseInterface(ABC):
    @abstractmethod
    async def register_spend(self, spent):
        pass
