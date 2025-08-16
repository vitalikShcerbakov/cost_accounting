from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app import crud, schemas
from backend.database import get_db

router = APIRouter(prefix="/incomes", tags=["incomes"])


@router.get("/", response_model=List[schemas.Income])
def read_incomes(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = Query(None, description="Начальная дата (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Конечная дата (YYYY-MM-DD)"),
    category_id: Optional[int] = Query(None, description="ID категории"),
    db: Session = Depends(get_db)
):
    """Получить список доходов с возможностью фильтрации"""
    incomes = crud.get_incomes(
        db,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        category_id=category_id
    )
    return incomes


@router.post("/", response_model=schemas.Income)
def create_income(income: schemas.IncomeCreate, db: Session = Depends(get_db)):
    """Создать новый доход"""
    return crud.create_income(db=db, income=income)


@router.get("/{income_id}", response_model=schemas.Income)
def read_income(income_id: int, db: Session = Depends(get_db)):
    """Получить доход по ID"""
    db_income = crud.get_income(db, income_id=income_id)
    if db_income is None:
        raise HTTPException(status_code=404, detail="Доход не найден")
    return db_income


@router.put("/{income_id}", response_model=schemas.Income)
def update_income(income_id: int, income: schemas.IncomeUpdate, db: Session = Depends(get_db)):
    """Обновить доход"""
    db_income = crud.update_income(db, income_id=income_id, income=income)
    if db_income is None:
        raise HTTPException(status_code=404, detail="Доход не найден")
    return db_income


@router.delete("/{income_id}")
def delete_income(income_id: int, db: Session = Depends(get_db)):
    """Удалить доход"""
    db_income = crud.delete_income(db, income_id=income_id)
    if db_income is None:
        raise HTTPException(status_code=404, detail="Доход не найден")
    return {"message": "Доход удален"}
