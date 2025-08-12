from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend import crud, schemas

router = APIRouter(prefix="/expense-types", tags=["expense-types"])

@router.get("/", response_model=List[schemas.ExpenseType])
def read_expense_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех видов трат"""
    expense_types = crud.get_expense_types(db, skip=skip, limit=limit)
    return expense_types

@router.get("/monthly", response_model=List[schemas.ExpenseType])
def read_monthly_expense_types(db: Session = Depends(get_db)):
    """Получить список ежемесячных видов трат"""
    expense_types = crud.get_monthly_expense_types(db)
    return expense_types

@router.post("/", response_model=schemas.ExpenseType)
def create_expense_type(expense_type: schemas.ExpenseTypeCreate, db: Session = Depends(get_db)):
    """Создать новый вид трат"""
    return crud.create_expense_type(db=db, expense_type=expense_type)

@router.get("/{expense_type_id}", response_model=schemas.ExpenseType)
def read_expense_type(expense_type_id: int, db: Session = Depends(get_db)):
    """Получить вид трат по ID"""
    db_expense_type = crud.get_expense_type(db, expense_type_id=expense_type_id)
    if db_expense_type is None:
        raise HTTPException(status_code=404, detail="Вид трат не найден")
    return db_expense_type

@router.put("/{expense_type_id}", response_model=schemas.ExpenseType)
def update_expense_type(expense_type_id: int, expense_type: schemas.ExpenseTypeUpdate, db: Session = Depends(get_db)):
    """Обновить вид трат"""
    db_expense_type = crud.update_expense_type(db, expense_type_id=expense_type_id, expense_type=expense_type)
    if db_expense_type is None:
        raise HTTPException(status_code=404, detail="Вид трат не найден")
    return db_expense_type

@router.delete("/{expense_type_id}")
def delete_expense_type(expense_type_id: int, db: Session = Depends(get_db)):
    """Удалить вид трат"""
    db_expense_type = crud.delete_expense_type(db, expense_type_id=expense_type_id)
    if db_expense_type is None:
        raise HTTPException(status_code=404, detail="Вид трат не найден")
    return {"message": "Вид трат удален"} 