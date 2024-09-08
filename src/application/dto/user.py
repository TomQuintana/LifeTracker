from pydantic import BaseModel


class UserSchema(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    is_active: bool = True
    budget_ARS: float
    budget_USDT: float | None = None


class UserLogin(BaseModel):
    email: str
    password: str
