from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer

from ...application.dto.expenses import ExpenseRequest
from ..services.auth import Auth
from ..services.expense_service import ExpenseService
from ..dependency.expense_dependency import get_expense_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_service = Auth()
router = APIRouter(
    prefix="/api/expense",
    tags=["Expense"],
    # dependencies=[Depends(auth_service.get_token)],
)


@router.get("/", status_code=HTTPStatus.OK)
async def get_data(
    token: Annotated[str, Depends(oauth2_scheme)],
    month: int = Query(None, description="The month for filtering expenses"),
    expense_service: ExpenseService = Depends(get_expense_service),
):
    data_spend = await expense_service.fetch_data(month, token)
    return data_spend


@router.get("/total", status_code=HTTPStatus.OK)
async def get_total(
    token: Annotated[str, Depends(oauth2_scheme)],
    month: int = Query(None, description="The month for filtering expenses"),
    expense_service: ExpenseService = Depends(get_expense_service),
):
    total = await expense_service.fetch_total(month, token)
    return total


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_expense(
    token: Annotated[str, Depends(oauth2_scheme)],
    data: ExpenseRequest,
    expense_service: ExpenseService = Depends(get_expense_service),
):
    expense = await expense_service.create_expense(data, token)
    return expense
