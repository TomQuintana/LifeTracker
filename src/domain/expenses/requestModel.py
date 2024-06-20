from pydantic import BaseModel
from .model import Expense as expense_model


class ExpenseRequest(BaseModel):
    """
    This class is used to validate the request when creating or updating a book
    """

    name: str
    price_ARS: int
    price_USDT: float | None = None
    type: str
    coutes: str | None = None
    date: str | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Lapicera Uniball",
                "price_ARS": 20,
            }
        }
    }


class ExpenseResponse(expense_model):
    """
    This class is used to validate the response when getting book objects
    """

    pass
