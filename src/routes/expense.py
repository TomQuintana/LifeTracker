from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.services.auth import Auth
from src.services.expense_service import ExpenseService

from ..dependency.dependency_manager import DependencyManager
from ..domain.expenses.requestModel import ExpenseRequest

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_service = Auth()
router = APIRouter(
    prefix="/api/expense",
    tags=["Expense"],
    dependencies=[Depends(auth_service.get_token)],
)

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
    token: Annotated[str | None, Depends(oauth2_scheme)] = None,
):
    payload = auth_service.check_payload(token)
    total_response = await expense_service.calculate_total(month, budget=payload.get("user_budge"))
    return total_response


@router.get("/data", status_code=HTTPStatus.OK)
async def get_data(
    session_db: AsyncSession = Depends(get_session),
    month: int = Header(),
):
    expense_service = ExpenseService(session_db)
    data_spend = await expense_service.obtain_data(month)
    return data_spend
