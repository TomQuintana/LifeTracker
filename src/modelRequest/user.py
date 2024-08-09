from pydantic import BaseModel


class UserRequestModel(BaseModel):
    email: str
    password: str
    budget_ARS: float
    first_name: str
    last_name: str
