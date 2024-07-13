from http import HTTPStatus

from fastapi import APIRouter, Depends, Header
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.services.expense_service import ExpenseService

from ..dependency.dependency_manager import DependencyManager
from ..domain.expenses.requestModel import ExpenseRequest

router = APIRouter(prefix="/api/expense", tags=["Expense"])

dependency_manager = DependencyManager()


@router.post("/create", status_code=HTTPStatus.CREATED)
async def create_expense(
    expense_data: ExpenseRequest,
    session_db: AsyncSession = Depends(get_session),
):
    expense_service = ExpenseService(session_db)
    expense = await expense_service.create_expense(expense_data)
    return expense


@router.get("/total-spend", status_code=HTTPStatus.OK)
async def get_total(
    month: int = Header(),
    expense_service=Depends(dependency_manager.get_expense_service),
):
    total_response = await expense_service.calculate_total(month)
    return total_response


@router.get("/data", status_code=HTTPStatus.OK)
async def get_data(
    session_db: AsyncSession = Depends(get_session),
    month: int = Header(),
):
    expense_service = ExpenseService(session_db)
    data_spend = await expense_service.obtain_data(month)
    return data_spend
