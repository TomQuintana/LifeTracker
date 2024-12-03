from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer

from ...application.dto.expenses import ExpenseRequest
from ..dependency.expense_dependency import get_expense_service
from ..services.auth import Auth
from ..services.expense_service import ExpenseService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_service = Auth()
router = APIRouter(
    prefix="/api/expense",
    tags=["Expense"],
    dependencies=[Depends(auth_service.get_token)],
)


@router.get("/", status_code=HTTPStatus.OK)
async def get_data(
    token: Annotated[str, Depends(oauth2_scheme)],
    cursor: int = Query(0, description="The cursor for pagination"),
    month: int = Query(None, description="The month for filtering expenses"),
    expense_service: ExpenseService = Depends(get_expense_service),
):
    data_spend = await expense_service.fetch_data(month, token, cursor)
    return data_spend


@router.get("/total", status_code=HTTPStatus.OK)
async def get_total(
    token: Annotated[str, Depends(oauth2_scheme)],
    month: int = Query(None, description="The month for filtering expenses"),
    expense_service: ExpenseService = Depends(get_expense_service),
):
    total = await expense_service.fetch_total(month, token)
    return total


@router.get("/coutes", status_code=HTTPStatus.OK)
async def search_book(
    expense_service: ExpenseService = Depends(get_expense_service),
):
    result = await expense_service.coutes_expenses()
    return result


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_expense(
    token: Annotated[str, Depends(oauth2_scheme)],
    data: ExpenseRequest,
    expense_service: ExpenseService = Depends(get_expense_service),
):
    expense = await expense_service.create_expense(data, token)
    return expense


@router.delete("/{id}", status_code=HTTPStatus.OK)
async def delete_expense(
    id: int,
    token: Annotated[str, Depends(oauth2_scheme)],
    expense_service: ExpenseService = Depends(get_expense_service),
):
    await expense_service.delete_expense(id)
    return {"message": "Expense deleted successfully"}
