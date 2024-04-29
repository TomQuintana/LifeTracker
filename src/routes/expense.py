from http import HTTPStatus

from fastapi import APIRouter, Depends

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
async def get_total(expense_service=Depends(dependency_manager.get_expense_service)):
    total_response = await expense_service.calculate_total()
    return total_response


@router.get("/data", status_code=HTTPStatus.OK)
async def get_data(expense_service=Depends(dependency_manager.get_expense_service)):
    data_spend = await expense_service.obtain_data()
    return data_spend
