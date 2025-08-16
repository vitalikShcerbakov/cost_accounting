from datetime import date
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.app import models, schemas


# Category expense CRUD operations
def get_category_expense(db: Session, category_id: int):
    return db.query(models.CategoryExpense).filter(models.CategoryExpense.id == category_id).first()


def get_categories_expense(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CategoryExpense).offset(skip).limit(limit).all()


def create_category_expense(db: Session, category: schemas.CategoryCreate):
    db_category = models.CategoryExpense(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category_expense(db: Session, category_id: int, category: schemas.CategoryUpdate):
    db_category = get_category_expense(db, category_id)
    if db_category:
        update_data = category.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category_expense(db: Session, category_id: int):
    db_category = get_category_expense(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category


# Category income CRUD operations
def get_category_income(db: Session, category_id: int):
    return db.query(models.CategoryIncome).filter(models.CategoryIncome.id == category_id).first()


def get_categories_income(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CategoryIncome).offset(skip).limit(limit).all()


def create_category_income(db: Session, category: schemas.CategoryCreate):
    db_category = models.CategoryIncome(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category_income(db: Session, category_id: int, category: schemas.CategoryUpdate):
    db_category = get_category_income(db, category_id)
    if db_category:
        update_data = category.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category_income(db: Session, category_id: int):
    db_category = get_category_income(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category


# ExpenseType CRUD operations
def get_expense_type(db: Session, expense_type_id: int):
    return db.query(models.ExpenseType).filter(models.ExpenseType.id == expense_type_id).first()


def get_expense_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ExpenseType).offset(skip).limit(limit).all()


def get_monthly_expense_types(db: Session):
    return db.query(models.ExpenseType).filter(models.ExpenseType.is_monthly is True).all()


def create_expense_type(db: Session, expense_type: schemas.ExpenseTypeCreate):
    db_expense_type = models.ExpenseType(**expense_type.dict())
    db.add(db_expense_type)
    db.commit()
    db.refresh(db_expense_type)
    return db_expense_type


def update_expense_type(db: Session, expense_type_id: int, expense_type: schemas.ExpenseTypeUpdate):
    db_expense_type = get_expense_type(db, expense_type_id)
    if db_expense_type:
        update_data = expense_type.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_expense_type, field, value)
        db.commit()
        db.refresh(db_expense_type)
    return db_expense_type


def delete_expense_type(db: Session, expense_type_id: int):
    db_expense_type = get_expense_type(db, expense_type_id)
    if db_expense_type:
        db.delete(db_expense_type)
        db.commit()
    return db_expense_type


# Expense CRUD operations
def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()


def get_expenses(db: Session, skip: int = 0, limit: int = 100,
                 start_date: Optional[date] = None, end_date: Optional[date] = None,
                 category_id: Optional[int] = None, expense_type_id: Optional[int] = None):
    query = db.query(models.Expense)
    if start_date:
        query = query.filter(models.Expense.date >= start_date)
    if end_date:
        query = query.filter(models.Expense.date <= end_date)
    if category_id:
        query = query.filter(models.Expense.category_id == category_id)
    if expense_type_id:
        query = query.filter(models.Expense.expense_type_id == expense_type_id)
    return query.offset(skip).limit(limit).all()


def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def update_expense(db: Session, expense_id: int, expense: schemas.ExpenseUpdate):
    db_expense = get_expense(db, expense_id)
    if db_expense:
        update_data = expense.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_expense, field, value)
        db.commit()
        db.refresh(db_expense)
    return db_expense


def delete_expense(db: Session, expense_id: int):
    db_expense = get_expense(db, expense_id)
    if db_expense:
        db.delete(db_expense)
        db.commit()
    return db_expense


# Income CRUD operations
def get_income(db: Session, income_id: int):
    return db.query(models.Income).filter(models.Income.id == income_id).first()


def get_incomes(db: Session, skip: int = 0, limit: int = 100,
                start_date: Optional[date] = None, end_date: Optional[date] = None,
                category_id: Optional[int] = None):
    query = db.query(models.Income)
    if start_date:
        query = query.filter(models.Income.date >= start_date)
    if end_date:
        query = query.filter(models.Income.date <= end_date)
    if category_id:
        query = query.filter(models.Income.category_id == category_id)
    return query.offset(skip).limit(limit).all()


def create_income(db: Session, income: schemas.IncomeCreate):
    db_income = models.Income(**income.dict())
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income


def update_income(db: Session, income_id: int, income: schemas.IncomeUpdate):
    db_income = get_income(db, income_id)
    if db_income:
        update_data = income.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_income, field, value)
        db.commit()
        db.refresh(db_income)
    return db_income


def delete_income(db: Session, income_id: int):
    db_income = get_income(db, income_id)
    if db_income:
        db.delete(db_income)
        db.commit()
    return db_income


# Summary operations
def get_monthly_summary(db: Session, year: int, month: int):
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    # Общие доходы и расходы
    total_income = db.query(func.sum(models.Income.amount)).filter(
        models.Income.date >= start_date,
        models.Income.date < end_date
    ).scalar() or 0

    total_expenses = db.query(func.sum(models.Expense.amount)).filter(
        models.Expense.date >= start_date,
        models.Expense.date < end_date
    ).scalar() or 0

    # Ежемесячные расходы
    monthly_expenses = db.query(func.sum(models.Expense.amount)).join(models.ExpenseType).filter(
        models.Expense.date >= start_date,
        models.Expense.date < end_date,
        models.ExpenseType.is_monthly is True
    ).scalar() or 0

    # Остальные расходы
    other_expenses = total_expenses - monthly_expenses

    return {
        "month": f"{year}-{month:02d}",
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": total_income - total_expenses,
        "monthly_expenses": monthly_expenses,
        "other_expenses": other_expenses
    }


def get_category_summary(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None):
    query = db.query(
        models.CategoryExpense.id,
        models.CategoryExpense.name,
        func.sum(models.Expense.amount).label('total_amount'),
        func.count(models.Expense.id).label('count')
    ).join(models.Expense)

    if start_date:
        query = query.filter(models.Expense.date >= start_date)
    if end_date:
        query = query.filter(models.Expense.date <= end_date)

    return query.group_by(models.CategoryExpense.id, models.CategoryExpense.name).all()
