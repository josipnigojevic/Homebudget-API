from pydantic import BaseModel, Field, ConfigDict
from datetime import date

typedef_OptionalDate = date | None

class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=2, max_length=80)
    password: str = Field(..., min_length=3)
    starting_budget: float = Field(..., ge=0)

class UserLoginSchema(BaseModel):
    username: str
    password: str

class CategorySchema(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class CategoryCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)

class ExpenseSchema(BaseModel):
    id: int
    description: str
    amount: float
    date: date
    category: CategorySchema
    model_config = ConfigDict(from_attributes=True)

class ExpenseCreateSchema(BaseModel):
    description: str = Field(..., min_length=1)
    amount: float
    category_id: int
    date: typedef_OptionalDate = None

class StatsResponseSchema(BaseModel):
    start_date: date | None
    end_date: date | None
    total_spent: float
    total_earned: float
    net_flow: float
