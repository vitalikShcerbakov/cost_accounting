from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from database import get_db
from auth.crud import get_current_active_user
from auth.schemas import User

router = APIRouter(prefix="/categories_expense", tags=["categories_expense"])


@router.get("/", response_model=List[schemas.Category])
def read_categories(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получить список всех категорий"""
    categories = crud.get_categories_expense(db, skip=skip, limit=limit, user_id=current_user.id)
    return categories


@router.post("/", response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Создать новую категорию"""
    # Устанавливаем user_id из токена аутентификации
    category.user_id = current_user.id
    return crud.create_category_expense(db=db, category=category)


@router.get("/{category_id}", response_model=schemas.Category)
def read_category(
    category_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Получить категорию по ID"""
    db_category = crud.get_category_expense(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    # Проверяем, что категория принадлежит текущему пользователю
    if db_category.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    return db_category


@router.put("/{category_id}", response_model=schemas.Category)
def update_category(
    category_id: int, 
    category: schemas.CategoryUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Обновить категорию"""
    # Проверяем, что категория принадлежит текущему пользователю
    db_category = crud.get_category_expense(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    if db_category.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    # Устанавливаем user_id из токена аутентификации
    category.user_id = current_user.id
    db_category = crud.update_category_expense(db, category_id=category_id, category=category)
    return db_category


@router.delete("/{category_id}")
def delete_category(
    category_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Удалить категорию"""
    # Проверяем, что категория принадлежит текущему пользователю
    db_category = crud.get_category_expense(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    if db_category.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    db_category = crud.delete_category_expense(db, category_id=category_id)
    return {"message": "Категория удалена"}
