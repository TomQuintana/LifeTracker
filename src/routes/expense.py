from http import HTTPStatus

from fastapi import APIRouter, Depends, Header

from ..dependency.dependency_manager import DependencyManager
from ..domain.expenses.requestModel import ExpenseRequest

router = APIRouter(prefix="/api/expense", tags=["Expense"])

dependency_manager = DependencyManager()


@router.post("/create", status_code=HTTPStatus.CREATED)
async def create_expense(
    expense_data: ExpenseRequest,
    expense_service=Depends(dependency_manager.get_expense_service),
):
    new_expense = await expense_service.create_expense(expense_data)
    return new_expense


@router.get("/total-spend", status_code=HTTPStatus.OK)
async def get_total(
    month: int = Header(), expense_service=Depends(dependency_manager.get_expense_service)
):
    total_response = await expense_service.calculate_total(month)
    return total_response


@router.get("/data/{date_expense}", status_code=HTTPStatus.OK)
async def get_data(
    date_expense: str, expense_service=Depends(dependency_manager.get_expense_service)
):
    data_spend = await expense_service.obtain_data(date_expense)
    return data_spend
