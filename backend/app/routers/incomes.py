from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from database import get_db
from auth.crud import get_current_active_user
from auth.schemas import User

router = APIRouter(prefix="/incomes", tags=["incomes"])


@router.get("/", response_model=List[schemas.Income])
def read_incomes(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = Query(None, description="Начальная дата (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Конечная дата (YYYY-MM-DD)"),
    category_id: Optional[int] = Query(None, description="ID категории"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получить список доходов с возможностью фильтрации"""
    incomes = crud.get_incomes(
        db,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        category_id=category_id,
        user_id=current_user.id
    )
    return incomes


@router.post("/", response_model=schemas.Income)
def create_income(
    income: schemas.IncomeCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Создать новый доход"""
    # Устанавливаем user_id из токена аутентификации
    income.user_id = current_user.id
    return crud.create_income(db=db, income=income)


@router.get("/{income_id}", response_model=schemas.Income)
def read_income(
    income_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получить доход по ID"""
    db_income = crud.get_income(db, income_id=income_id)
    if db_income is None:
        raise HTTPException(status_code=404, detail="Доход не найден")
    # Проверяем, что доход принадлежит текущему пользователю
    if db_income.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    return db_income


@router.put("/{income_id}", response_model=schemas.Income)
def update_income(
    income_id: int, 
    income: schemas.IncomeUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Обновить доход"""
    # Проверяем, что доход принадлежит текущему пользователю
    db_income = crud.get_income(db, income_id=income_id)
    if db_income is None:
        raise HTTPException(status_code=404, detail="Доход не найден")
    if db_income.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    # Устанавливаем user_id из токена аутентификации
    income.user_id = current_user.id
    db_income = crud.update_income(db, income_id=income_id, income=income)
    return db_income


@router.delete("/{income_id}")
def delete_income(
    income_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Удалить доход"""
    # Проверяем, что доход принадлежит текущему пользователю
    db_income = crud.get_income(db, income_id=income_id)
    if db_income is None:
        raise HTTPException(status_code=404, detail="Доход не найден")
    if db_income.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    db_income = crud.delete_income(db, income_id=income_id)
    return {"message": "Доход удален"}
