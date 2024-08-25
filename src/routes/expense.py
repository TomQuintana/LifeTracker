from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.db_manager import get_session
from src.dto.expenses import ExpenseRequest
from src.services.auth import Auth
from src.services.expense_service import ExpenseService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_service = Auth()
router = APIRouter(
    prefix="/api/expense",
    tags=["Expense"],
    dependencies=[Depends(auth_service.get_token)],
)


@router.get("/", status_code=HTTPStatus.OK)
async def get_data(
    session_db: AsyncSession = Depends(get_session),
    month: int = Header(default=None, alias="Month"),
    type: str = Header(default=None, alias="Type"),
):
    expense_service = ExpenseService(session_db)
    data_spend = await expense_service.obtain_data(month, type)
    return data_spend


@router.get("/total", status_code=HTTPStatus.OK)
async def get_total(
    month: int = Header(),
    session: AsyncSession = Depends(get_session),
    token: Annotated[str | None, Depends(oauth2_scheme)] = None,
):
    payload = auth_service.check_payload(token)
    expense_service = ExpenseService(session)
    total_response = await expense_service.calculate_total(month, budget=payload.get("user_budge"))
    return total_response


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_expense(
    data: ExpenseRequest,
    session_db: AsyncSession = Depends(get_session),
):
    expense_service = ExpenseService(session_db)
    expense = await expense_service.create_expense(data)
    return expense
