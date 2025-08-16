from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app import crud, schemas
from backend.database import get_db

router = APIRouter(prefix="/summary", tags=["summary"])


@router.get("/monthly/{year}/{month}", response_model=schemas.MonthlySummary)
def get_monthly_summary(year: int, month: int, db: Session = Depends(get_db)):
    """Получить месячную сводку доходов и расходов"""
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="Месяц должен быть от 1 до 12")
    summary = crud.get_monthly_summary(db, year=year, month=month)
    return summary


@router.get("/category-summary", response_model=List[schemas.CategorySummary])
def get_category_summary(
    start_date: Optional[date] = Query(None, description="Начальная дата (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Конечная дата (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Получить сводку по категориям расходов"""
    summary = crud.get_category_summary(db, start_date=start_date, end_date=end_date)
    return summary
