# from fastapi import Depends
# from sqlmodel.ext.asyncio.session import AsyncSession
#
# from ..infrastructure.services.expense_service import ExpenseService
#
# from ..db.db_manager import get_session
#
#
# class DependencyManager:
#     def __init__(self):
#         pass
#
#     async def get_expense_service(self, session: AsyncSession = Depends(get_session)):
#         return ExpenseService(session)
