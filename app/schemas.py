from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date

# Category schemas
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    color: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ExpenseType schemas
class ExpenseTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_monthly: bool = False
    monthly_budget: Optional[float] = None

class ExpenseTypeCreate(ExpenseTypeBase):
    pass

class ExpenseTypeUpdate(ExpenseTypeBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_monthly: Optional[bool] = None
    monthly_budget: Optional[float] = None

class ExpenseType(ExpenseTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Expense schemas
class ExpenseBase(BaseModel):
    amount: float = Field(..., gt=0)
    description: Optional[str] = None
    date: datetime
    category_id: int
    expense_type_id: int

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    date: Optional[datetime] = None
    category_id: Optional[int] = None
    expense_type_id: Optional[int] = None

class Expense(ExpenseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Category
    expense_type: ExpenseType
    
    class Config:
        from_attributes = True

# Income schemas
class IncomeBase(BaseModel):
    amount: float = Field(..., gt=0)
    description: Optional[str] = None
    date: date
    category_id: int

class IncomeCreate(IncomeBase):
    pass

class IncomeUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    date: Optional[datetime] = None
    category_id: Optional[int] = None

class Income(IncomeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Category
    
    class Config:
        from_attributes = True

# Summary schemas
class MonthlySummary(BaseModel):
    month: str
    total_income: float
    total_expenses: float
    balance: float
    monthly_expenses: float
    other_expenses: float

class CategorySummary(BaseModel):
    category_id: int
    category_name: str
    total_amount: float
    count: int 