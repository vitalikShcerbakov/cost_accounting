from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app import crud, schemas
from backend.database import get_db

router = APIRouter(prefix="/categories_income", tags=["categories_income"])


@router.get("/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех категорий"""
    categories = crud.get_categories_income(db, skip=skip, limit=limit)
    return categories


@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Создать новую категорию"""
    return crud.create_category_income(db=db, category=category)


@router.get("/{category_id}", response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """Получить категорию по ID"""
    db_category = crud.get_category_income(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return db_category


@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    """Обновить категорию"""
    db_category = crud.update_category_income(db, category_id=category_id, category=category)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return db_category


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Удалить категорию"""
    db_category = crud.delete_category_income(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return {"message": "Категория удалена"}
