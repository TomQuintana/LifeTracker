from ...domain.habits.habits_repository import HabitsRepository


class HabitsService:
    def __init__(self, repository: HabitsRepository):
        self.repository = repository

    async def create_habits(self, data, token):
        return "ok"
