from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price_ARS: float
    price_USDT: float | None = None


class ExpenseRequest(BaseModel):
    name: str
    price_ARS: float
    products: list[Product]
    type: str
    coutes: str | None = None
    date: str | None = None


class ExpenseCreate(ExpenseRequest):
    pass
