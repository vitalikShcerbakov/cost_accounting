from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String, Text)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class CategoryExpense(Base):
    __tablename__ = "categories_expenses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String, nullable=True)  # Для UI цветового кодирования
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    # Отношения
    expenses = relationship("Expense", back_populates="categories_expense")
    user = relationship("Users", back_populates='categories_expense')


class CategoryIncome(Base):
    __tablename__ = "categories_incomes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String, nullable=True)  # Для UI цветового кодирования
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    # Отношения
    incomes = relationship("Income", back_populates="categories_income")
    user = relationship("Users", back_populates='categories_income')


class ExpenseType(Base):
    __tablename__ = "expense_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    is_monthly = Column(Boolean, default=False)  # True для ежемесячных трат
    monthly_budget = Column(Float, nullable=True)  # Бюджет на месяц для ежемесячных трат
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    # Отношения
    expenses = relationship("Expense", back_populates="expense_type")
    user = relationship("Users", back_populates='expense_type')


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False)
    category_id = Column(Integer, ForeignKey("categories_expenses.id"), nullable=False)
    expense_type_id = Column(Integer, ForeignKey("expense_types.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    # Отношения
    categories_expense = relationship("CategoryExpense", back_populates="expenses")
    expense_type = relationship("ExpenseType", back_populates="expenses")
    user = relationship("Users", back_populates='expenses')


class Income(Base):
    __tablename__ = "incomes"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False)
    category_id = Column(Integer, ForeignKey("categories_incomes.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    # Отношения
    categories_income = relationship("CategoryIncome", back_populates="incomes")
    user = relationship("Users", back_populates='incomes')
