from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from http import HTTPStatus
from ..db.main import get_session
from ..services.expense_service import ExpenseService
from ..domain.expenses.requestModel import ExpenseRequest
from ..dependency.dependency_manager import DependencyManager


router = APIRouter(prefix="/api/expense", tags=['Expense'])

dependency_manager = DependencyManager()

# def get_expense_service(session: AsyncSession = Depends(get_session)):
#     return ExpenseService(session)


@router.post("/create", status_code = HTTPStatus.CREATED)
async def create_expense(expense_data: ExpenseRequest, expense_service = Depends(dependency_manager.get_expense_service)):
    new_expense = await expense_service.create_expense(expense_data)
    return new_expense

@router.get('/total-spend', status_code=HTTPStatus.OK)
async def get_total(expense_service = Depends(dependency_manager.get_expense_service)):
    total_response = await expense_service.calculate_total()
    return total_response
