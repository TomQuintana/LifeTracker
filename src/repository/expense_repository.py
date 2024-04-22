from src.repository.expense_interface import ExpenseInterface

class ExpenseRepository(ExpenseInterface):
    async def register_spend(self, spent: dict):
        return {"Save data in db"}
