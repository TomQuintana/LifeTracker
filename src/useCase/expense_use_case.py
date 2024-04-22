from ..repository.expense_interface import ExpenseInterface


class ExpenseUseCase:
    def __init__(self, expense_repository: ExpenseInterface) -> None:
        self.expense_repository = expense_repository

    async def create_spent(self, expense):
        expense_created = await self.expense_repository.register_spend(expense)
        return expense_created
