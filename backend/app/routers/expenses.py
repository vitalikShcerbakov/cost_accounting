from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from database import get_db
from auth.crud import get_current_active_user
from auth.schemas import User

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/", response_model=List[schemas.Expense])
def read_expenses(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = Query(None, description="Начальная дата (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Конечная дата (YYYY-MM-DD)"),
    category_id: Optional[int] = Query(None, description="ID категории"),
    expense_type_id: Optional[int] = Query(None, description="ID вида трат"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получить список расходов с возможностью фильтрации"""
    expenses = crud.get_expenses(
        db,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        category_id=category_id,
        expense_type_id=expense_type_id,
        user_id=current_user.id
    )
    return expenses


@router.post("/", response_model=schemas.Expense)
def create_expense(
    expense: schemas.ExpenseCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Создать новый расход"""
    # Устанавливаем user_id из токена аутентификации
    expense.user_id = current_user.id
    return crud.create_expense(db=db, expense=expense)


@router.get("/{expense_id}", response_model=schemas.Expense)
def read_expense(
    expense_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получить расход по ID"""
    db_expense = crud.get_expense(db, expense_id=expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Расход не найден")
    # Проверяем, что расход принадлежит текущему пользователю
    if db_expense.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    return db_expense


@router.put("/{expense_id}", response_model=schemas.Expense)
def update_expense(
    expense_id: int, 
    expense: schemas.ExpenseUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Обновить расход"""
    # Проверяем, что расход принадлежит текущему пользователю
    db_expense = crud.get_expense(db, expense_id=expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Расход не найден")
    if db_expense.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    # Устанавливаем user_id из токена аутентификации
    expense.user_id = current_user.id
    db_expense = crud.update_expense(db, expense_id=expense_id, expense=expense)
    return db_expense


@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Удалить расход"""
    # Проверяем, что расход принадлежит текущему пользователю
    db_expense = crud.get_expense(db, expense_id=expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Расход не найден")
    if db_expense.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    db_expense = crud.delete_expense(db, expense_id=expense_id)
    return {"message": "Расход удален"}
